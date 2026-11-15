"""Test-set metrics for the three Phase 5 estimators.

Metrics are computed from predictions. This module does not fit a model and
does not choose parameters.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
from sklearn.metrics import (
    accuracy_score,
    balanced_accuracy_score,
    confusion_matrix,
    f1_score,
    precision_recall_fscore_support,
    precision_score,
    recall_score,
)

from preprocessing import ALLOWED_LABELS

CLASS_LABELS = tuple(ALLOWED_LABELS)
METRIC_DECIMALS = 6


def evaluate_predictions(y_true, y_pred) -> dict[str, Any]:
    """Score one fitted estimator. Class order is Dropout, Enrolled, Graduate.

    Balanced accuracy is the recall summary. Macro recall is computed only to
    confirm it is the same number, and it is not returned as a second metric.
    """
    actual = _label_array(y_true, "y_true")
    predicted = _label_array(y_pred, "y_pred")
    if len(actual) != len(predicted):
        raise ValueError("Actual labels and predictions have different lengths.")
    if len(actual) == 0:
        raise ValueError("There are no rows to evaluate.")
    missing = set(CLASS_LABELS) - set(actual)
    if missing:
        raise ValueError(f"Evaluation labels are missing {sorted(missing)}.")
    unknown = set(predicted) - set(CLASS_LABELS)
    if unknown:
        raise ValueError(f"Predictions contain labels outside {CLASS_LABELS}: {sorted(unknown)}.")

    labels = list(CLASS_LABELS)
    precision, recall, f1, support = precision_recall_fscore_support(
        actual,
        predicted,
        labels=labels,
        average=None,
        zero_division=0,
    )
    macro_f1 = float(f1_score(actual, predicted, average="macro", labels=labels, zero_division=0))
    macro_precision = float(
        precision_score(actual, predicted, average="macro", labels=labels, zero_division=0)
    )
    macro_recall = float(
        recall_score(actual, predicted, average="macro", labels=labels, zero_division=0)
    )
    balanced = float(balanced_accuracy_score(actual, predicted))
    if abs(balanced - macro_recall) > 1e-12:
        raise ValueError(
            "Balanced accuracy and macro recall differ, so they cannot be reported as one recall summary."
        )
    matrix = confusion_matrix(actual, predicted, labels=labels)
    if matrix.shape != (len(CLASS_LABELS), len(CLASS_LABELS)):
        raise ValueError(f"Confusion matrix shape is {matrix.shape}, expected {(3, 3)}.")

    per_class = []
    for label, class_precision, class_recall, class_f1, class_support in zip(
        labels, precision, recall, f1, support
    ):
        per_class.append(
            {
                "label": label,
                "precision": float(class_precision),
                "recall": float(class_recall),
                "f1": float(class_f1),
                "support": int(class_support),
            }
        )
    metrics = {
        "macro_f1": macro_f1,
        "balanced_accuracy": balanced,
        "macro_precision": macro_precision,
        "accuracy": float(accuracy_score(actual, predicted)),
        "confusion_matrix": matrix.astype(int).tolist(),
        "labels": labels,
        "per_class": per_class,
        "macro_recall_equals_balanced_accuracy": True,
    }
    assert_metrics_consistent(metrics)
    return metrics


def assert_metrics_consistent(metrics: dict[str, Any]) -> None:
    matrix = np.asarray(metrics["confusion_matrix"], dtype=int)
    if matrix.shape != (3, 3):
        raise ValueError("Confusion matrix must be 3 by 3.")
    if list(metrics["labels"]) != list(CLASS_LABELS):
        raise ValueError("Class-label order is not Dropout, Enrolled, Graduate.")
    per_class = metrics["per_class"]
    if [row["label"] for row in per_class] != list(CLASS_LABELS):
        raise ValueError("Per-class rows are not in Dropout, Enrolled, Graduate order.")
    row_sums = matrix.sum(axis=1).tolist()
    supports = [int(row["support"]) for row in per_class]
    if row_sums != supports:
        raise ValueError("Confusion-matrix row sums do not match per-class support.")
    if abs(float(np.mean([row["f1"] for row in per_class])) - metrics["macro_f1"]) > 1e-9:
        raise ValueError("Macro F1 is not the unweighted mean of the class F1 scores.")
    if abs(float(np.mean([row["precision"] for row in per_class])) - metrics["macro_precision"]) > 1e-9:
        raise ValueError("Macro precision is not the unweighted mean of the class precision scores.")
    if abs(float(np.mean([row["recall"] for row in per_class])) - metrics["balanced_accuracy"]) > 1e-9:
        raise ValueError("Balanced accuracy is not the unweighted mean of the class recall scores.")


def _label_array(values, name: str) -> np.ndarray:
    array = np.asarray(values).astype(str)
    if array.ndim != 1:
        raise ValueError(f"{name} must be one-dimensional.")
    return array


def test_metrics_frame(named_metrics: dict[str, dict[str, Any]]) -> pd.DataFrame:
    rows = []
    for model_name, metrics in named_metrics.items():
        rows.append(
            {
                "model": model_name,
                "macro_f1": metrics["macro_f1"],
                "balanced_accuracy": metrics["balanced_accuracy"],
                "macro_precision": metrics["macro_precision"],
                "accuracy": metrics["accuracy"],
            }
        )
    return pd.DataFrame(rows)


def per_class_frame(named_metrics: dict[str, dict[str, Any]]) -> pd.DataFrame:
    rows = []
    for model_name, metrics in named_metrics.items():
        for row in metrics["per_class"]:
            rows.append({"model": model_name, **row})
    return pd.DataFrame(rows)


def confusion_frame(named_metrics: dict[str, dict[str, Any]]) -> pd.DataFrame:
    rows = []
    for model_name, metrics in named_metrics.items():
        matrix = metrics["confusion_matrix"]
        for actual, counts in zip(metrics["labels"], matrix):
            row = {"model": model_name, "actual_label": actual}
            for predicted, count in zip(metrics["labels"], counts):
                row[f"predicted_{predicted}"] = int(count)
            rows.append(row)
    return pd.DataFrame(rows)


def predictions_frame(y_true, named_predictions: dict[str, Any], row_index) -> pd.DataFrame:
    frame = pd.DataFrame({"row_index": np.asarray(row_index), "actual": _label_array(y_true, "y_true")})
    for model_name, predicted in named_predictions.items():
        values = _label_array(predicted, model_name)
        if len(values) != len(frame):
            raise ValueError(f"{model_name} predictions do not match the test row count.")
        frame[model_name] = values
    return frame


def render_report(payload: dict[str, Any]) -> str:
    """Markdown report from a measured payload. This does not rank the test scores."""
    logistic = payload["selected"]["logistic_regression"]
    forest = payload["selected"]["random_forest"]
    metrics = payload["test_metrics"]
    lines = [
        "# Phase 5 evaluation report",
        "",
        "This report was written by `src/run_phase5.py` from the fitted estimators and their predictions. "
        "The experimental design was not changed. Phase 5 is not marked complete by this file.",
        "",
        f"Evaluation timestamp: `{payload['evaluation_timestamp']}`.",
        "",
        "## Methodology",
        "",
        "The run reused the approved Phase 4 split and preprocessing in `src/preprocessing.py`. "
        "The split is an 80/20 stratified split on `Target` with `random_state=42`. "
        "Grid search used `make_training_cv()`: five-fold `StratifiedKFold`, `shuffle=True`, `random_state=42`, "
        "on the training portion only. Each search estimator was a pipeline, so every fold fit its own "
        "encoder and, for logistic regression, its own scaler.",
        "",
        "Logistic Regression used `max_iter=2000` and `solver=\"lbfgs\"`. `penalty` was not passed. "
        "Random Forest used `random_state=42` and `n_jobs=1`. "
        "Both searches used `scoring=\"f1_macro\"`, `refit=True`, `error_score=\"raise\"`, and `n_jobs=1`. "
        "The dummy baseline was `DummyClassifier(strategy=\"most_frequent\")`, fit once on the training portion, with no grid.",
        "",
        "The parameter grids were passed as one dictionary per declared configuration. "
        "That keeps `class_weight` changing fastest, which a single dictionary would not do for the forest "
        "because `ParameterGrid` sorts keys alphabetically. "
        "On an exact tie of mean validation macro F1, the earliest configuration in that declared list is kept. "
        "The installed scikit-learn assigns tied ranks with `method=\"min\"` and `best_index_` is the first of those ranks. "
        "The run checked that this index was the first exact maximum. It did not fit an extra model to resolve a tie.",
        "",
        "The test portion was not passed to `GridSearchCV.fit` and was not used to choose parameters, features, or preprocessing. "
        "`cv_results_` names the training-fold validation score `test_score`. Those values are not the 885-row holdout.",
        "",
        "Class order for the confusion matrix and the per-class metrics is Dropout, Enrolled, Graduate. "
        "Balanced accuracy is the recall summary. In this three-class evaluation it equals macro recall, "
        "so macro recall is not listed as a separate result.",
        "",
        "## Data checked during the run",
        "",
        f"- Raw SHA-256 before the run: `{payload['raw_sha256_before']}`.",
        f"- Raw SHA-256 after the run: `{payload['raw_sha256_after']}`.",
        f"- Training rows: {payload['train_rows']}. Test rows: {payload['test_rows']}.",
        f"- Training class counts: {payload['train_class_counts']}.",
        f"- Test class counts: {payload['test_class_counts']}.",
        f"- Logistic scaler rows seen at the training refit: {payload['logistic_scaler_rows_seen']}.",
        f"- Forest numerical step is a scaler: {payload['forest_numeric_is_scaler']}.",
        f"- scikit-learn version: `{payload['sklearn_version']}`.",
        "",
        "## Limitations carried from the approved plan",
        "",
        payload["timing_assumption"],
        "",
        "Recorded semester grades of 0 stayed numeric zero. Standardising numerical columns inside the logistic pipeline "
        "changes the units of that transformed matrix. It does not impute, replace, or drop those zeros, and this run "
        "is not a zero-grade sensitivity analysis.",
        "",
        "## Cross-validation selection",
        "",
        "The table below is the training-fold selection. It is not a test result, and it is not a ranking of the two algorithms against each other.",
        "",
        _selection_table(logistic, forest),
        "",
        _tie_sentence("Logistic Regression", logistic),
        "",
        _tie_sentence("Random Forest", forest),
        "",
        f"Completed logistic cross-validation fits: {logistic['cv_fits_completed']}.",
        f"Completed forest cross-validation fits: {forest['cv_fits_completed']}.",
        f"Training-set refits: {int(logistic['training_refit_completed']) + int(forest['training_refit_completed'])}.",
        "The dummy baseline is not included in those counts. It was fit once on the training portion.",
        "",
        "Fold scores and the GridSearchCV standard deviation of those fold scores are in the cross-validation CSV files. "
        "That standard deviation is the square root of the mean squared deviation of the five fold scores.",
        "",
        "## Test evaluation",
        "",
        "Each fitted estimator predicted the same untouched test rows once. "
        "These three results are reported independently. This run does not select a single winning algorithm. "
        "The test scores were not used to change parameters, features, class weights, or preprocessing.",
        "",
        _metrics_table(metrics),
        "",
        "Scores in this markdown table are shown to 6 decimal places. The JSON file stores the measured floats.",
        "",
        "### Confusion matrices",
        "",
        "Rows are actual labels and columns are predicted labels, in the order Dropout, Enrolled, Graduate.",
        "",
        _confusion_section(metrics),
        "",
        "### Per-class precision, recall, and F1",
        "",
        _per_class_section(metrics),
        "",
        "## Warnings recorded while fitting",
        "",
        _warning_section(payload["warnings"]),
        "",
        "## Output files",
        "",
    ]
    for path in payload["output_files"]:
        lines.append(f"- `{path}`")
    lines.extend(
        [
            "",
            "No single test-set winner is designated in this report.",
            "",
        ]
    )
    return "\n".join(lines)


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, allow_nan=False) + "\n", encoding="utf-8")


def _fmt(value: float) -> str:
    return f"{float(value):.{METRIC_DECIMALS}f}"


def _selection_table(logistic: dict[str, Any], forest: dict[str, Any]) -> str:
    header = (
        "| Model | Declared order | Parameters | Mean CV macro F1 | Fold SD |\n"
        "| --- | ---: | --- | ---: | ---: |"
    )
    rows = [
        _selection_row("Logistic Regression", logistic),
        _selection_row("Random Forest", forest),
    ]
    return "\n".join([header, *rows])


def _selection_row(label: str, record: dict[str, Any]) -> str:
    parameters = ", ".join(f"`{key}`={_display_value(value)}" for key, value in record["parameters"].items())
    return (
        f"| {label} | {record['declared_order']} | {parameters} | "
        f"{_fmt(record['mean_cv_macro_f1'])} | {_fmt(record['std_cv_macro_f1'])} |"
    )


def _display_value(value: Any) -> str:
    if value is None:
        return "`None`"
    if isinstance(value, str):
        return f"`{value}`"
    return f"`{value}`"


def _tie_sentence(label: str, record: dict[str, Any]) -> str:
    tied = record["tied_declared_indices"]
    if tied == [record["declared_index"]]:
        return (
            f"{label}: one configuration had the highest mean cross-validated macro F1. "
            f"Declared index {record['declared_index']} (order {record['declared_order']}) was selected."
        )
    orders = ", ".join(str(index + 1) for index in tied)
    return (
        f"{label}: declared orders {orders} had exactly equal mean cross-validated macro F1. "
        f"The earliest, order {record['declared_order']}, was selected. No extra refit was run to break the tie."
    )


def _metrics_table(metrics: dict[str, dict[str, Any]]) -> str:
    header = (
        "| Model | Macro F1 | Balanced accuracy | Macro precision | Accuracy |\n"
        "| --- | ---: | ---: | ---: | ---: |"
    )
    labels = {
        "logistic_regression": "Logistic Regression",
        "random_forest": "Random Forest",
        "dummy_most_frequent": "Dummy most-frequent",
    }
    rows = []
    for model_name, label in labels.items():
        row = metrics[model_name]
        rows.append(
            f"| {label} | {_fmt(row['macro_f1'])} | {_fmt(row['balanced_accuracy'])} | "
            f"{_fmt(row['macro_precision'])} | {_fmt(row['accuracy'])} |"
        )
    return "\n".join([header, *rows])


def _confusion_section(metrics: dict[str, dict[str, Any]]) -> str:
    labels = {
        "logistic_regression": "Logistic Regression",
        "random_forest": "Random Forest",
        "dummy_most_frequent": "Dummy most-frequent",
    }
    blocks = []
    for model_name, title in labels.items():
        matrix = metrics[model_name]["confusion_matrix"]
        blocks.append(f"#### {title}")
        blocks.append("")
        blocks.append("| Actual \\ Predicted | Dropout | Enrolled | Graduate |")
        blocks.append("| --- | ---: | ---: | ---: |")
        for actual, counts in zip(CLASS_LABELS, matrix):
            blocks.append(f"| {actual} | {counts[0]} | {counts[1]} | {counts[2]} |")
        blocks.append("")
    return "\n".join(blocks).rstrip()


def _per_class_section(metrics: dict[str, dict[str, Any]]) -> str:
    labels = {
        "logistic_regression": "Logistic Regression",
        "random_forest": "Random Forest",
        "dummy_most_frequent": "Dummy most-frequent",
    }
    blocks = []
    for model_name, title in labels.items():
        blocks.append(f"#### {title}")
        blocks.append("")
        blocks.append("| Class | Precision | Recall | F1 | Support |")
        blocks.append("| --- | ---: | ---: | ---: | ---: |")
        for row in metrics[model_name]["per_class"]:
            blocks.append(
                f"| {row['label']} | {_fmt(row['precision'])} | {_fmt(row['recall'])} | "
                f"{_fmt(row['f1'])} | {row['support']} |"
            )
        blocks.append("")
    return "\n".join(blocks).rstrip()


def _warning_section(warnings: list[dict[str, Any]]) -> str:
    if not warnings:
        return "No warnings were recorded during the three fits."
    lines = ["These warnings were counted and left unchanged. `max_iter` was not increased.", ""]
    for item in warnings:
        lines.append(f"- {item['count']} × {item['message']}")
    return "\n".join(lines)
