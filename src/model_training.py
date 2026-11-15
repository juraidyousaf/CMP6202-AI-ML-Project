"""Phase 5 estimators, grids, and training-only search.

The grids and seeds come from the frozen design. This module fits on the
training portion only. It does not read the test set and it does not score it.
"""

from __future__ import annotations

from typing import Any

import numpy as np
import pandas as pd
from sklearn.base import clone
from sklearn.dummy import DummyClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV, ParameterGrid
from sklearn.pipeline import Pipeline

from preprocessing import (
    ALLOWED_LABELS,
    CV_SPLITS,
    RANDOM_STATE,
    make_forest_preprocessor,
    make_logistic_preprocessor,
    make_training_cv,
    reject_forbidden_columns,
)

SCORING = "f1_macro"
SEARCH_N_JOBS = 1
SEARCH_REFIT = True
SEARCH_ERROR_SCORE = "raise"

LOGISTIC_C_VALUES = (0.01, 0.1, 1, 10)
LOGISTIC_CLASS_WEIGHTS = (None, "balanced")
FOREST_N_ESTIMATORS = (200, 400)
FOREST_MAX_DEPTHS = (None, 10, 20)
FOREST_MIN_SAMPLES_LEAF = (1, 2, 4)
FOREST_CLASS_WEIGHTS = (None, "balanced")

LOGISTIC_MODEL_NAME = "logistic_regression"
FOREST_MODEL_NAME = "random_forest"
DUMMY_MODEL_NAME = "dummy_most_frequent"


def logistic_declared_configurations() -> list[dict[str, Any]]:
    """Eight configurations. `class_weight` changes fastest."""
    configurations = []
    for c_value in LOGISTIC_C_VALUES:
        for class_weight in LOGISTIC_CLASS_WEIGHTS:
            configurations.append(
                {
                    "classifier__C": c_value,
                    "classifier__class_weight": class_weight,
                }
            )
    return configurations


def forest_declared_configurations() -> list[dict[str, Any]]:
    """Thirty-six configurations. `class_weight` changes fastest."""
    configurations = []
    for n_estimators in FOREST_N_ESTIMATORS:
        for max_depth in FOREST_MAX_DEPTHS:
            for min_samples_leaf in FOREST_MIN_SAMPLES_LEAF:
                for class_weight in FOREST_CLASS_WEIGHTS:
                    configurations.append(
                        {
                            "classifier__n_estimators": n_estimators,
                            "classifier__max_depth": max_depth,
                            "classifier__min_samples_leaf": min_samples_leaf,
                            "classifier__class_weight": class_weight,
                        }
                    )
    return configurations


def planned_cv_fits(configurations: list[dict[str, Any]]) -> int:
    return len(configurations) * CV_SPLITS


def as_parameter_grid(configurations: list[dict[str, Any]]) -> list[dict[str, list[Any]]]:
    """One dictionary per declared configuration.

    `ParameterGrid` sorts keys inside a dictionary and varies the last key
    fastest. One dictionary for the forest would therefore follow alphabetical
    key order, not the declared order. A list of single-value dictionaries
    keeps the declared sequence. `GridSearchCV` breaks an exact score tie by
    the first rank in that sequence, so the one `refit=True` fit uses the
    declared winner. No second refit is added.
    """
    if not configurations:
        raise ValueError("The parameter grid is empty.")
    grid = []
    for configuration in configurations:
        if not configuration:
            raise ValueError("A declared configuration has no parameters.")
        grid.append({key: [value] for key, value in configuration.items()})
    return grid


def values_match(left: Any, right: Any) -> bool:
    if left is None or right is None:
        return left is None and right is None
    if isinstance(left, str) or isinstance(right, str):
        return left == right
    if isinstance(left, (bool, np.bool_)) or isinstance(right, (bool, np.bool_)):
        return left == right
    if isinstance(left, (int, float, np.number)) and isinstance(right, (int, float, np.number)):
        return float(left) == float(right)
    return left == right


def configurations_match(recorded: list[dict[str, Any]], declared: list[dict[str, Any]]) -> bool:
    if len(recorded) != len(declared):
        return False
    for left, right in zip(recorded, declared):
        if set(left) != set(right):
            return False
        for key, value in right.items():
            if not values_match(left[key], value):
                return False
    return True


def parameter_grid_order(configurations: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return list(ParameterGrid(as_parameter_grid(configurations)))


def make_logistic_estimator() -> Pipeline:
    """Unfitted logistic pipeline. Numerical columns are scaled."""
    preprocess = make_logistic_preprocessor().named_steps["preprocess"]
    classifier = LogisticRegression(max_iter=2000, solver="lbfgs")
    return Pipeline(steps=[("preprocess", preprocess), ("classifier", classifier)])


def make_forest_estimator() -> Pipeline:
    """Unfitted forest pipeline. Numerical columns are not scaled."""
    preprocess = make_forest_preprocessor().named_steps["preprocess"]
    classifier = RandomForestClassifier(random_state=RANDOM_STATE, n_jobs=1)
    return Pipeline(steps=[("preprocess", preprocess), ("classifier", classifier)])


def make_dummy_estimator() -> DummyClassifier:
    """Unfitted most-frequent baseline. The library default strategy is not used."""
    return DummyClassifier(strategy="most_frequent")


def validate_training_pair(
    X_train: pd.DataFrame,
    y_train: pd.Series,
    *,
    require_approved_columns: bool,
) -> None:
    if not isinstance(X_train, pd.DataFrame):
        raise TypeError("X_train must be a pandas DataFrame.")
    if not isinstance(y_train, pd.Series):
        raise TypeError("y_train must be a pandas Series.")
    if len(X_train) == 0:
        raise ValueError("Training data is empty.")
    if len(X_train) != len(y_train) or not X_train.index.equals(y_train.index):
        raise ValueError("Training features and labels do not match.")
    observed = {str(label) for label in y_train.unique()}
    if observed != set(ALLOWED_LABELS):
        raise ValueError(f"Training labels must be {ALLOWED_LABELS}, found {sorted(observed)}.")
    if require_approved_columns:
        reject_forbidden_columns(X_train)


def assert_no_shared_rows(X_train: pd.DataFrame, X_test: pd.DataFrame) -> None:
    shared = X_train.index.intersection(X_test.index)
    if not shared.empty:
        raise ValueError("Training indices overlap the test indices.")


def build_grid_search(
    estimator,
    configurations: list[dict[str, Any]],
    *,
    verbose: int = 0,
) -> GridSearchCV:
    """Search object using the approved splitter, metric, and fit policy."""
    if verbose < 0:
        raise ValueError("verbose must be non-negative.")
    return GridSearchCV(
        estimator=estimator,
        param_grid=as_parameter_grid(configurations),
        scoring=SCORING,
        cv=make_training_cv(),
        refit=SEARCH_REFIT,
        error_score=SEARCH_ERROR_SCORE,
        n_jobs=SEARCH_N_JOBS,
        return_train_score=False,
        verbose=verbose,
    )


def first_exact_maximum_index(scores: np.ndarray) -> int:
    """Index of the first exact maximum. Ties use equality, not a tolerance."""
    values = np.asarray(scores, dtype=float)
    if values.size == 0 or not np.isfinite(values).all():
        raise RuntimeError("Cross-validation scores must be finite before a configuration is selected.")
    maximum = float(np.max(values))
    matches = np.flatnonzero(values == maximum)
    return int(matches[0])


def accept_fitted_search(search: GridSearchCV, configurations: list[dict[str, Any]]) -> int:
    """Reject a search whose candidate order or tie-break differs from the declared list.

    Returns the number of completed cross-validation fits. The refit is not included.
    """
    if not hasattr(search, "cv_results_"):
        raise RuntimeError("The search has not been fit.")
    recorded = list(search.cv_results_["params"])
    if not configurations_match(recorded, configurations):
        raise RuntimeError(
            "GridSearchCV candidate order does not match the declared grid order."
        )
    if int(search.n_splits_) != CV_SPLITS:
        raise RuntimeError("The search did not use the approved five training folds.")
    selected = first_exact_maximum_index(search.cv_results_["mean_test_score"])
    if int(search.best_index_) != selected:
        raise RuntimeError(
            "GridSearchCV did not keep the first declared configuration among exact score ties. "
            f"Library index {int(search.best_index_)}, declared index {selected}."
        )
    if search.best_estimator_ is None:
        raise RuntimeError("The training-set refit did not produce an estimator.")
    completed = completed_cv_fit_count(search)
    expected = planned_cv_fits(configurations)
    if completed != expected:
        raise RuntimeError(f"Completed CV fits were {completed}, expected {expected}.")
    return completed


def completed_cv_fit_count(search: GridSearchCV) -> int:
    """Count finite validation-fold scores. A failed fit does not add a count."""
    n_candidates = len(search.cv_results_["params"])
    n_splits = int(search.n_splits_)
    for split_id in range(n_splits):
        scores = np.asarray(search.cv_results_[f"split{split_id}_test_score"], dtype=float)
        if scores.shape != (n_candidates,) or not np.isfinite(scores).all():
            raise RuntimeError("A cross-validation fit did not produce a finite score.")
    return n_candidates * n_splits


def fit_search(
    estimator,
    configurations: list[dict[str, Any]],
    X_train: pd.DataFrame,
    y_train: pd.Series,
    *,
    require_approved_columns: bool = True,
    verbose: int = 0,
) -> GridSearchCV:
    """Fit one grid on training rows. `X_test` is not an argument."""
    validate_training_pair(
        X_train,
        y_train,
        require_approved_columns=require_approved_columns,
    )
    search = build_grid_search(clone(estimator), configurations, verbose=verbose)
    search.fit(X_train, y_train)
    accept_fitted_search(search, configurations)
    return search


def fit_dummy(
    X_train: pd.DataFrame,
    y_train: pd.Series,
    *,
    require_approved_columns: bool = True,
) -> DummyClassifier:
    """Fit the most-frequent baseline once. There is no grid and no test row."""
    validate_training_pair(
        X_train,
        y_train,
        require_approved_columns=require_approved_columns,
    )
    model = make_dummy_estimator()
    if model.strategy != "most_frequent":
        raise RuntimeError("The dummy baseline must use strategy='most_frequent'.")
    model.fit(X_train, y_train)
    return model


def selected_search_record(search: GridSearchCV, model_name: str) -> dict[str, Any]:
    """Selected configuration and training-fold scores. No test metric is included."""
    index = int(search.best_index_)
    results = search.cv_results_
    fold_scores = [
        float(results[f"split{split_id}_test_score"][index])
        for split_id in range(int(search.n_splits_))
    ]
    means = np.asarray(results["mean_test_score"], dtype=float)
    maximum = float(np.max(means))
    tied = [int(position) for position in np.flatnonzero(means == maximum)]
    parameters = {key: _json_value(value) for key, value in search.best_params_.items()}
    return {
        "model": model_name,
        "declared_index": index,
        "declared_order": index + 1,
        "parameters": parameters,
        "mean_cv_macro_f1": float(results["mean_test_score"][index]),
        "std_cv_macro_f1": float(results["std_test_score"][index]),
        "fold_macro_f1": fold_scores,
        "tied_declared_indices": tied,
        "cv_fits_completed": completed_cv_fit_count(search),
        "training_refit_completed": True,
        "scoring": SCORING,
    }


def cv_results_frame(search: GridSearchCV, configurations: list[dict[str, Any]]) -> pd.DataFrame:
    """One row per declared configuration, in declared order."""
    if not configurations_match(list(search.cv_results_["params"]), configurations):
        raise RuntimeError("Cannot write CV results because the candidate order was not the declared order.")
    results = search.cv_results_
    rows = []
    for index, configuration in enumerate(configurations):
        row: dict[str, Any] = {
            "declared_index": index,
            "declared_order": index + 1,
            "mean_cv_macro_f1": float(results["mean_test_score"][index]),
            "std_cv_macro_f1": float(results["std_test_score"][index]),
            "rank_cv_macro_f1": int(results["rank_test_score"][index]),
            "selected": index == int(search.best_index_),
        }
        for split_id in range(int(search.n_splits_)):
            row[f"fold_{split_id}_macro_f1"] = float(results[f"split{split_id}_test_score"][index])
        for key, value in configuration.items():
            short_key = key.split("__", 1)[1]
            row[short_key] = "None" if value is None else value
        rows.append(row)
    return pd.DataFrame(rows)


def _json_value(value: Any) -> Any:
    if value is None or isinstance(value, (str, bool, int, float)):
        return value
    if isinstance(value, (np.integer,)):
        return int(value)
    if isinstance(value, (np.floating,)):
        return float(value)
    if isinstance(value, (np.bool_,)):
        return bool(value)
    raise TypeError(f"Cannot record parameter value {value!r}.")
