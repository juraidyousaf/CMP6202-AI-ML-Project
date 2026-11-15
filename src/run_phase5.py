"""Run the frozen Phase 5 experiments and write the measured outputs.

The test portion is used only after both grid searches and the dummy fit have
finished. Test scores are not used to change parameters.
"""

from __future__ import annotations

import hashlib
import json
import sys
import warnings
from datetime import datetime
from pathlib import Path
from typing import Any

import joblib
import numpy as np
import sklearn
from sklearn.preprocessing import FunctionTransformer, StandardScaler

import model_evaluation as evaluation
import model_training as training
from preprocessing import (
    RAW_CSV,
    TARGET_COLUMN,
    TIMING_ASSUMPTION,
    prepare_from_raw,
)

ROOT = Path(__file__).resolve().parents[1]
MODELS_DIR = ROOT / "outputs" / "models"
EVALUATION_DIR = ROOT / "outputs" / "evaluation"
EXPECTED_RAW_SHA256 = "3ef126de5cefff26eb11fbb4237f1a1401cb64b488e2f1d598c23cedeb4c45ae"

EXPECTED_TRAIN_ROWS = 3539
EXPECTED_TEST_ROWS = 885
EXPECTED_TRAIN_COUNTS = {"Graduate": 1767, "Dropout": 1137, "Enrolled": 635}
EXPECTED_TEST_COUNTS = {"Graduate": 442, "Dropout": 284, "Enrolled": 159}

MODEL_FILES = {
    training.LOGISTIC_MODEL_NAME: "logistic_regression.joblib",
    training.FOREST_MODEL_NAME: "random_forest.joblib",
    training.DUMMY_MODEL_NAME: "dummy_most_frequent.joblib",
}


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def class_counts(labels) -> dict[str, int]:
    counts = {str(label): int(count) for label, count in labels.value_counts().items()}
    return {label: counts.get(label, 0) for label in ("Dropout", "Enrolled", "Graduate")}


def assert_official_split(split) -> None:
    if len(split.X_train) != EXPECTED_TRAIN_ROWS or len(split.X_test) != EXPECTED_TEST_ROWS:
        raise RuntimeError(
            f"Split sizes were {len(split.X_train)} and {len(split.X_test)}, "
            f"expected {EXPECTED_TRAIN_ROWS} and {EXPECTED_TEST_ROWS}."
        )
    if class_counts(split.y_train) != EXPECTED_TRAIN_COUNTS:
        raise RuntimeError(f"Training class counts were {class_counts(split.y_train)}.")
    if class_counts(split.y_test) != EXPECTED_TEST_COUNTS:
        raise RuntimeError(f"Test class counts were {class_counts(split.y_test)}.")
    if TARGET_COLUMN in split.X_train.columns or TARGET_COLUMN in split.X_test.columns:
        raise RuntimeError("Target entered the feature matrix.")


def logistic_rows_seen(estimator) -> int:
    scaler = estimator.named_steps["preprocess"].named_transformers_["numeric"]
    if not isinstance(scaler, StandardScaler):
        raise TypeError("The logistic numerical step is not a StandardScaler.")
    return int(scaler.n_samples_seen_)


def forest_numeric_is_scaler(estimator) -> bool:
    numeric = estimator.named_steps["preprocess"].named_transformers_["numeric"]
    if isinstance(numeric, StandardScaler):
        return True
    if not isinstance(numeric, FunctionTransformer) or numeric.func is not None:
        raise TypeError("The forest numerical step is not an unscaled passthrough.")
    return False


def warning_records(caught: list[warnings.WarningMessage]) -> list[dict[str, Any]]:
    counts: dict[str, int] = {}
    for item in caught:
        text = f"{item.category.__name__}: {item.message}"
        counts[text] = counts.get(text, 0) + 1
    return [{"message": message, "count": counts[message]} for message in sorted(counts)]


def fit_phase5(split, *, verbose: int = 1) -> dict[str, Any]:
    """Fit both searches and the dummy on training rows only."""
    training.assert_no_shared_rows(split.X_train, split.X_test)
    logistic_grid = training.logistic_declared_configurations()
    forest_grid = training.forest_declared_configurations()
    if training.planned_cv_fits(logistic_grid) != 40:
        raise RuntimeError("The logistic grid is not the approved 40 cross-validation fits.")
    if training.planned_cv_fits(forest_grid) != 180:
        raise RuntimeError("The forest grid is not the approved 180 cross-validation fits.")

    caught: list[warnings.WarningMessage] = []
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        print(
            "Fitting logistic regression: 8 configurations, 40 training-fold fits, then one training refit.",
            flush=True,
        )
        logistic_search = training.fit_search(
            training.make_logistic_estimator(),
            logistic_grid,
            split.X_train,
            split.y_train,
            verbose=verbose,
        )
        print(
            "Fitting random forest: 36 configurations, 180 training-fold fits, then one training refit.",
            flush=True,
        )
        forest_search = training.fit_search(
            training.make_forest_estimator(),
            forest_grid,
            split.X_train,
            split.y_train,
            verbose=verbose,
        )
        print("Fitting dummy most-frequent baseline on the training portion.", flush=True)
        dummy = training.fit_dummy(split.X_train, split.y_train)

    logistic_estimator = logistic_search.best_estimator_
    forest_estimator = forest_search.best_estimator_
    rows_seen = logistic_rows_seen(logistic_estimator)
    if rows_seen != len(split.X_train):
        raise RuntimeError(
            f"Logistic scaler saw {rows_seen} rows, expected the training size {len(split.X_train)}."
        )
    if rows_seen == len(split.X_train) + len(split.X_test):
        raise RuntimeError("Logistic scaler saw the combined training and test rows.")
    forest_scaled = forest_numeric_is_scaler(forest_estimator)
    if forest_scaled:
        raise RuntimeError("The forest pipeline scaled numerical columns.")

    return {
        "logistic_search": logistic_search,
        "forest_search": forest_search,
        "logistic_grid": logistic_grid,
        "forest_grid": forest_grid,
        "estimators": {
            training.LOGISTIC_MODEL_NAME: logistic_estimator,
            training.FOREST_MODEL_NAME: forest_estimator,
            training.DUMMY_MODEL_NAME: dummy,
        },
        "selected": {
            training.LOGISTIC_MODEL_NAME: training.selected_search_record(
                logistic_search, training.LOGISTIC_MODEL_NAME
            ),
            training.FOREST_MODEL_NAME: training.selected_search_record(
                forest_search, training.FOREST_MODEL_NAME
            ),
        },
        "logistic_scaler_rows_seen": rows_seen,
        "forest_numeric_is_scaler": forest_scaled,
        "warnings": warning_records(caught),
    }


def evaluate_phase5(split, fitted: dict[str, Any]) -> dict[str, Any]:
    """Predict the test portion once per fitted estimator."""
    named_predictions = {}
    named_metrics = {}
    for model_name, estimator in fitted["estimators"].items():
        predicted = estimator.predict(split.X_test)
        named_predictions[model_name] = predicted
        named_metrics[model_name] = evaluation.evaluate_predictions(split.y_test, predicted)
    return {"predictions": named_predictions, "test_metrics": named_metrics}


def write_outputs(
    split,
    fitted: dict[str, Any],
    evaluated: dict[str, Any],
    metadata: dict[str, Any],
    *,
    models_dir: Path = MODELS_DIR,
    evaluation_dir: Path = EVALUATION_DIR,
    display_root: Path = ROOT,
) -> list[str]:
    models_dir.mkdir(parents=True, exist_ok=True)
    evaluation_dir.mkdir(parents=True, exist_ok=True)
    written: list[Path] = []

    for model_name, estimator in fitted["estimators"].items():
        path = models_dir / MODEL_FILES[model_name]
        joblib.dump(estimator, path)
        written.append(path)

    cv_paths = {
        training.LOGISTIC_MODEL_NAME: evaluation_dir / "logistic_regression_cv_results.csv",
        training.FOREST_MODEL_NAME: evaluation_dir / "random_forest_cv_results.csv",
    }
    training.cv_results_frame(fitted["logistic_search"], fitted["logistic_grid"]).to_csv(
        cv_paths[training.LOGISTIC_MODEL_NAME], index=False
    )
    training.cv_results_frame(fitted["forest_search"], fitted["forest_grid"]).to_csv(
        cv_paths[training.FOREST_MODEL_NAME], index=False
    )
    written.extend(cv_paths.values())

    selected_path = evaluation_dir / "selected_parameters.json"
    evaluation.write_json(
        selected_path,
        {
            "scoring": training.SCORING,
            "tie_break": "first exact maximum of mean CV macro F1 in declared grid order",
            "models": fitted["selected"],
        },
    )
    written.append(selected_path)

    metrics_path = evaluation_dir / "test_metrics.json"
    evaluation.write_json(metrics_path, evaluated["test_metrics"])
    written.append(metrics_path)

    tables = {
        "test_metrics.csv": evaluation.test_metrics_frame(evaluated["test_metrics"]),
        "per_class_metrics.csv": evaluation.per_class_frame(evaluated["test_metrics"]),
        "confusion_matrices.csv": evaluation.confusion_frame(evaluated["test_metrics"]),
        "predictions.csv": evaluation.predictions_frame(
            split.y_test,
            evaluated["predictions"],
            split.X_test.index,
        ),
    }
    for name, frame in tables.items():
        path = evaluation_dir / name
        frame.to_csv(path, index=False)
        written.append(path)

    report_name = "phase5_evaluation_report.md"
    metadata_name = "run_metadata.json"
    relative_outputs = [_display_path(path, display_root) for path in written]
    relative_outputs.extend(
        [
            _display_path(evaluation_dir / metadata_name, display_root),
            _display_path(evaluation_dir / report_name, display_root),
        ]
    )
    metadata = dict(metadata)
    metadata["output_files"] = relative_outputs
    metadata["test_metrics"] = evaluated["test_metrics"]
    metadata["selected"] = fitted["selected"]

    report_path = evaluation_dir / report_name
    report_path.write_text(evaluation.render_report(metadata), encoding="utf-8")
    metadata_path = evaluation_dir / metadata_name
    public_metadata = {key: value for key, value in metadata.items() if key != "test_metrics"}
    public_metadata["test_metric_file"] = _display_path(metrics_path, display_root)
    evaluation.write_json(metadata_path, public_metadata)
    written.extend([report_path, metadata_path])
    return [_display_path(path, display_root) for path in written]


def _display_path(path: Path, display_root: Path) -> str:
    return str(path.relative_to(display_root)).replace("\\", "/")


def verify_saved_models(split, evaluated: dict[str, Any], models_dir: Path = MODELS_DIR) -> None:
    for model_name, filename in MODEL_FILES.items():
        loaded = joblib.load(models_dir / filename)
        reloaded = np.asarray(loaded.predict(split.X_test)).astype(str)
        original = np.asarray(evaluated["predictions"][model_name]).astype(str)
        if not np.array_equal(reloaded, original):
            raise RuntimeError(f"Reloaded predictions differ for {model_name}.")


def verify_tables(split, fitted: dict[str, Any], evaluated: dict[str, Any]) -> None:
    searches = {
        training.LOGISTIC_MODEL_NAME: fitted["logistic_search"],
        training.FOREST_MODEL_NAME: fitted["forest_search"],
    }
    for model_name, record in fitted["selected"].items():
        if record["mean_cv_macro_f1"] != float(searches[model_name].best_score_):
            raise RuntimeError(f"Stored CV macro F1 does not match GridSearchCV for {model_name}.")
    logistic_cv = training.cv_results_frame(fitted["logistic_search"], fitted["logistic_grid"])
    forest_cv = training.cv_results_frame(fitted["forest_search"], fitted["forest_grid"])
    if len(logistic_cv) != 8 or int(logistic_cv["selected"].sum()) != 1:
        raise RuntimeError("Logistic CV table does not contain the 8 declared configurations.")
    if len(forest_cv) != 36 or int(forest_cv["selected"].sum()) != 1:
        raise RuntimeError("Forest CV table does not contain the 36 declared configurations.")
    if any(len(predicted) != len(split.y_test) for predicted in evaluated["predictions"].values()):
        raise RuntimeError("A prediction vector does not match the test row count.")
    if len(split.y_test) != EXPECTED_TEST_ROWS:
        raise RuntimeError("The test portion does not have the approved 885 rows.")
    counted = class_counts(split.y_test)
    for model_name, predicted in evaluated["predictions"].items():
        recomputed = evaluation.evaluate_predictions(split.y_test, predicted)
        if recomputed != evaluated["test_metrics"][model_name]:
            raise RuntimeError(f"Stored test metrics do not match a fresh calculation for {model_name}.")
        supports = {row["label"]: row["support"] for row in recomputed["per_class"]}
        if supports != counted:
            raise RuntimeError(f"Per-class support does not match the test class counts for {model_name}.")


def build_metadata(split, fitted: dict[str, Any], raw_hash: str) -> dict[str, Any]:
    return {
        "evaluation_timestamp": datetime.now().astimezone().isoformat(timespec="seconds"),
        "raw_csv": str(RAW_CSV.relative_to(ROOT)).replace("\\", "/"),
        "raw_sha256_before": raw_hash,
        "raw_sha256_after": raw_hash,
        "train_rows": int(len(split.X_train)),
        "test_rows": int(len(split.X_test)),
        "train_class_counts": class_counts(split.y_train),
        "test_class_counts": class_counts(split.y_test),
        "test_size": 0.2,
        "random_state": 42,
        "cv_splits": 5,
        "cv_shuffle": True,
        "scoring": training.SCORING,
        "search_n_jobs": training.SEARCH_N_JOBS,
        "forest_n_jobs": 1,
        "refit": True,
        "error_score": "raise",
        "logistic_grid_size": 8,
        "forest_grid_size": 36,
        "logistic_cv_fits_completed": fitted["selected"][training.LOGISTIC_MODEL_NAME]["cv_fits_completed"],
        "forest_cv_fits_completed": fitted["selected"][training.FOREST_MODEL_NAME]["cv_fits_completed"],
        "training_refits_completed": 2,
        "dummy_training_fits": 1,
        "test_rows_used_for_tuning": 0,
        "logistic_scaler_rows_seen": fitted["logistic_scaler_rows_seen"],
        "forest_numeric_is_scaler": fitted["forest_numeric_is_scaler"],
        "timing_assumption": TIMING_ASSUMPTION,
        "warnings": fitted["warnings"],
        "sklearn_version": sklearn.__version__,
        "phase_5_marked_complete": False,
        "output_files": [],
        "selected": fitted["selected"],
        "test_metrics": {},
    }


def main() -> dict[str, Any]:
    raw_hash = file_sha256(RAW_CSV)
    if raw_hash != EXPECTED_RAW_SHA256:
        raise RuntimeError("The raw CSV hash is not the approved file hash. The run was stopped.")
    split = prepare_from_raw()
    assert_official_split(split)
    fitted = fit_phase5(split, verbose=2)
    evaluated = evaluate_phase5(split, fitted)
    if file_sha256(RAW_CSV) != raw_hash:
        raise RuntimeError("The raw CSV changed during fitting.")
    metadata = build_metadata(split, fitted, raw_hash)
    verify_tables(split, fitted, evaluated)
    written = write_outputs(split, fitted, evaluated, metadata)
    verify_saved_models(split, evaluated)
    raw_hash_after = file_sha256(RAW_CSV)
    if raw_hash_after != raw_hash:
        raise RuntimeError("The raw CSV changed while the outputs were written.")
    summary = {
        "raw_sha256": raw_hash_after,
        "logistic_cv_fits": fitted["selected"][training.LOGISTIC_MODEL_NAME]["cv_fits_completed"],
        "forest_cv_fits": fitted["selected"][training.FOREST_MODEL_NAME]["cv_fits_completed"],
        "training_refits": 2,
        "dummy_training_fits": 1,
        "selected": fitted["selected"],
        "test_metrics": {
            name: {
                "macro_f1": metrics["macro_f1"],
                "balanced_accuracy": metrics["balanced_accuracy"],
                "macro_precision": metrics["macro_precision"],
                "accuracy": metrics["accuracy"],
            }
            for name, metrics in evaluated["test_metrics"].items()
        },
        "warnings": fitted["warnings"],
        "output_files": written,
    }
    print("Phase 5 run finished. Phase 5 is not marked complete.", flush=True)
    return summary


if __name__ == "__main__":
    try:
        result = main()
    except Exception as exc:
        print(f"Phase 5 run failed: {exc}", file=sys.stderr, flush=True)
        raise
    print(json.dumps(result, indent=2), flush=True)
