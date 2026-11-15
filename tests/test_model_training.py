"""Checks for the frozen Phase 5 grids, search, and training-only fits."""

from __future__ import annotations

import inspect
import json
import sys
import tempfile
import unittest
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, ClassifierMixin
from sklearn.model_selection import GridSearchCV, ParameterGrid
from sklearn.preprocessing import FunctionTransformer, StandardScaler

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

import model_training as training  # noqa: E402
import preprocessing as prep  # noqa: E402
import run_phase5  # noqa: E402


def _synthetic_frame(rows_per_class: int = 10) -> pd.DataFrame:
    labels = [label for label in prep.ALLOWED_LABELS for _ in range(rows_per_class)]
    n_rows = len(labels)
    data = {column: np.arange(n_rows) % 7 for column in prep.RETAINED_FEATURES}
    for column in prep.BINARY_FEATURES:
        data[column] = np.arange(n_rows) % 2
    data["Application order"] = np.arange(n_rows) % 10
    for column in prep.EXCLUDED_FEATURES:
        data[column] = np.arange(n_rows)
    data[prep.TARGET_COLUMN] = labels
    return pd.DataFrame(data)


def _tag_data() -> tuple[pd.DataFrame, pd.Series]:
    labels = [label for label in prep.ALLOWED_LABELS for _ in range(5)]
    frame = pd.DataFrame({"a": np.arange(len(labels))})
    target = pd.Series(labels, index=frame.index)
    return frame, target


class TaggedClassifier(BaseEstimator, ClassifierMixin):
    fit_calls = 0

    def __init__(self, tag: int = 0):
        self.tag = tag

    def fit(self, X, y):
        type(self).fit_calls += 1
        self.classes_ = np.unique(y)
        return self

    def predict(self, X):
        return np.full(len(X), self.classes_[0])


class FailingClassifier(BaseEstimator, ClassifierMixin):
    def __init__(self, tag: int = 0):
        self.tag = tag

    def fit(self, X, y):
        raise RuntimeError("deliberate fit failure")

    def predict(self, X):
        return np.asarray(["Dropout"] * len(X))


class GridConfigurationTests(unittest.TestCase):
    def test_logistic_grid_has_eight_declared_configurations(self):
        configurations = training.logistic_declared_configurations()
        self.assertEqual(
            list(training.LOGISTIC_C_VALUES),
            [0.01, 0.1, 1, 10],
        )
        self.assertEqual(list(training.LOGISTIC_CLASS_WEIGHTS), [None, "balanced"])
        self.assertEqual(len(configurations), 8)
        self.assertEqual(training.planned_cv_fits(configurations), 40)
        self.assertEqual(configurations[0]["classifier__C"], 0.01)
        self.assertIsNone(configurations[0]["classifier__class_weight"])
        self.assertEqual(configurations[1]["classifier__class_weight"], "balanced")
        self.assertEqual(configurations[1]["classifier__C"], 0.01)
        self.assertEqual(configurations[-1]["classifier__C"], 10)
        self.assertEqual(configurations[-1]["classifier__class_weight"], "balanced")
        self.assertTrue(
            training.configurations_match(
                training.parameter_grid_order(configurations),
                configurations,
            )
        )

    def test_forest_grid_has_thirty_six_declared_configurations(self):
        configurations = training.forest_declared_configurations()
        self.assertEqual(list(training.FOREST_N_ESTIMATORS), [200, 400])
        self.assertEqual(list(training.FOREST_MAX_DEPTHS), [None, 10, 20])
        self.assertEqual(list(training.FOREST_MIN_SAMPLES_LEAF), [1, 2, 4])
        self.assertEqual(list(training.FOREST_CLASS_WEIGHTS), [None, "balanced"])
        self.assertEqual(len(configurations), 36)
        self.assertEqual(training.planned_cv_fits(configurations), 180)
        first = configurations[0]
        last = configurations[-1]
        self.assertEqual(first["classifier__n_estimators"], 200)
        self.assertIsNone(first["classifier__max_depth"])
        self.assertEqual(first["classifier__min_samples_leaf"], 1)
        self.assertIsNone(first["classifier__class_weight"])
        self.assertEqual(last["classifier__n_estimators"], 400)
        self.assertEqual(last["classifier__max_depth"], 20)
        self.assertEqual(last["classifier__min_samples_leaf"], 4)
        self.assertEqual(last["classifier__class_weight"], "balanced")
        self.assertTrue(
            training.configurations_match(
                training.parameter_grid_order(configurations),
                configurations,
            )
        )

    def test_single_dictionary_forest_grid_is_not_the_declared_order(self):
        declared = training.forest_declared_configurations()
        alphabetical = list(
            ParameterGrid(
                {
                    "classifier__n_estimators": [200, 400],
                    "classifier__max_depth": [None, 10, 20],
                    "classifier__min_samples_leaf": [1, 2, 4],
                    "classifier__class_weight": [None, "balanced"],
                }
            )
        )
        self.assertFalse(training.configurations_match(alphabetical, declared))
        self.assertEqual(alphabetical[1]["classifier__n_estimators"], 400)
        self.assertIsNone(alphabetical[1]["classifier__class_weight"])
        self.assertEqual(declared[1]["classifier__n_estimators"], 200)
        self.assertEqual(declared[1]["classifier__class_weight"], "balanced")

    def test_estimator_and_search_settings_match_the_approved_design(self):
        logistic = training.make_logistic_estimator().named_steps["classifier"]
        forest = training.make_forest_estimator().named_steps["classifier"]
        dummy = training.make_dummy_estimator()
        self.assertEqual(logistic.max_iter, 2000)
        self.assertEqual(logistic.solver, "lbfgs")
        self.assertIsNone(logistic.random_state)
        self.assertIsNone(logistic.n_jobs)
        self.assertEqual(logistic.get_params()["penalty"], "deprecated")
        self.assertNotIn("multi_class", logistic.get_params())
        self.assertEqual(forest.random_state, 42)
        self.assertEqual(forest.n_jobs, 1)
        self.assertEqual(forest.criterion, "gini")
        self.assertEqual(forest.max_features, "sqrt")
        self.assertEqual(forest.min_samples_split, 2)
        self.assertTrue(forest.bootstrap)
        self.assertEqual(forest.ccp_alpha, 0.0)
        self.assertEqual(dummy.strategy, "most_frequent")

        search = training.build_grid_search(
            training.make_logistic_estimator(),
            training.logistic_declared_configurations(),
        )
        self.assertIsInstance(search, GridSearchCV)
        self.assertEqual(search.scoring, "f1_macro")
        self.assertIs(search.refit, True)
        self.assertEqual(search.error_score, "raise")
        self.assertEqual(search.n_jobs, 1)
        self.assertFalse(search.return_train_score)
        self.assertEqual(search.cv.n_splits, 5)
        self.assertTrue(search.cv.shuffle)
        self.assertEqual(search.cv.random_state, 42)
        self.assertEqual(search.param_grid[0]["classifier__C"], [0.01])
        self.assertEqual(len(search.param_grid), 8)

    def test_search_fit_does_not_accept_the_test_split(self):
        parameters = inspect.signature(training.fit_search).parameters
        self.assertNotIn("X_test", parameters)
        self.assertNotIn("y_test", parameters)
        dummy_parameters = inspect.signature(training.fit_dummy).parameters
        self.assertNotIn("X_test", dummy_parameters)
        self.assertNotIn("y_test", dummy_parameters)


class TieBreakTests(unittest.TestCase):
    def _fit_tagged(self, score_for_tag: dict[int, float]) -> GridSearchCV:
        TaggedClassifier.fit_calls = 0

        def scorer(estimator, X, y):
            return score_for_tag[estimator.tag]

        features, target = _tag_data()
        configurations = [{"tag": 1}, {"tag": 2}, {"tag": 3}]
        search = GridSearchCV(
            estimator=TaggedClassifier(),
            param_grid=training.as_parameter_grid(configurations),
            scoring=scorer,
            cv=prep.make_training_cv(),
            refit=True,
            error_score="raise",
            n_jobs=1,
        )
        search.fit(features, target)
        completed = training.accept_fitted_search(search, configurations)
        self.assertEqual(completed, 15)
        self.assertEqual(TaggedClassifier.fit_calls, 16)
        return search

    def test_exact_tie_keeps_the_earliest_declared_configuration(self):
        search = self._fit_tagged({1: 0.25, 2: 0.5, 3: 0.5})
        self.assertEqual(int(search.best_index_), 1)
        self.assertEqual(search.best_params_["tag"], 2)
        self.assertEqual(list(search.cv_results_["rank_test_score"]), [3, 1, 1])
        self.assertEqual(training.first_exact_maximum_index(search.cv_results_["mean_test_score"]), 1)

    def test_complete_tie_keeps_the_first_declared_configuration(self):
        search = self._fit_tagged({1: 0.5, 2: 0.5, 3: 0.5})
        self.assertEqual(int(search.best_index_), 0)
        self.assertEqual(search.best_params_["tag"], 1)
        self.assertEqual(list(search.cv_results_["rank_test_score"]), [1, 1, 1])


class TrainingSeparationTests(unittest.TestCase):
    def test_shared_row_index_is_rejected(self):
        split = prep.prepare_approved_split(_synthetic_frame())
        training.assert_no_shared_rows(split.X_train, split.X_test)
        overlapped = split.X_train.copy()
        overlapped.index = [split.X_test.index[0], *split.X_train.index[1:]]
        with self.assertRaises(ValueError):
            training.assert_no_shared_rows(overlapped, split.X_test)

    def test_refit_uses_training_rows_only(self):
        split = prep.prepare_approved_split(_synthetic_frame())
        search = training.fit_search(
            training.make_logistic_estimator(),
            training.logistic_declared_configurations(),
            split.X_train,
            split.y_train,
        )
        self.assertEqual(training.completed_cv_fit_count(search), 40)
        scaler = search.best_estimator_.named_steps["preprocess"].named_transformers_["numeric"]
        self.assertIsInstance(scaler, StandardScaler)
        self.assertEqual(int(scaler.n_samples_seen_), len(split.X_train))
        self.assertNotEqual(int(scaler.n_samples_seen_), len(split.features))

        fast_forest = dict(training.forest_declared_configurations()[0])
        fast_forest["classifier__n_estimators"] = 2
        forest_search = training.fit_search(
            training.make_forest_estimator(),
            [fast_forest],
            split.X_train,
            split.y_train,
        )
        numeric = forest_search.best_estimator_.named_steps["preprocess"].named_transformers_["numeric"]
        self.assertIsInstance(numeric, FunctionTransformer)
        self.assertIsNone(numeric.func)
        self.assertFalse(isinstance(numeric, StandardScaler))

    def test_failed_fit_is_raised(self):
        features, target = _tag_data()
        with self.assertRaises(RuntimeError) as caught:
            training.fit_search(
                FailingClassifier(),
                [{"tag": 0}],
                features,
                target,
                require_approved_columns=False,
            )
        self.assertIn("deliberate fit failure", str(caught.exception))

    def test_output_files_round_trip(self):
        split = prep.prepare_approved_split(_synthetic_frame())
        logistic_search = training.fit_search(
            training.make_logistic_estimator(),
            [training.logistic_declared_configurations()[0]],
            split.X_train,
            split.y_train,
        )
        forest_configuration = dict(training.forest_declared_configurations()[0])
        forest_configuration["classifier__n_estimators"] = 2
        forest_search = training.fit_search(
            training.make_forest_estimator(),
            [forest_configuration],
            split.X_train,
            split.y_train,
        )
        dummy = training.fit_dummy(split.X_train, split.y_train)
        fitted = {
            "logistic_search": logistic_search,
            "forest_search": forest_search,
            "logistic_grid": [training.logistic_declared_configurations()[0]],
            "forest_grid": [forest_configuration],
            "estimators": {
                training.LOGISTIC_MODEL_NAME: logistic_search.best_estimator_,
                training.FOREST_MODEL_NAME: forest_search.best_estimator_,
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
            "logistic_scaler_rows_seen": len(split.X_train),
            "forest_numeric_is_scaler": False,
            "warnings": [],
        }
        evaluated = run_phase5.evaluate_phase5(split, fitted)
        metadata = {
            "evaluation_timestamp": "2026-11-15T00:00:00+00:00",
            "raw_sha256_before": "synthetic",
            "raw_sha256_after": "synthetic",
            "train_rows": len(split.X_train),
            "test_rows": len(split.X_test),
            "train_class_counts": run_phase5.class_counts(split.y_train),
            "test_class_counts": run_phase5.class_counts(split.y_test),
            "logistic_scaler_rows_seen": len(split.X_train),
            "forest_numeric_is_scaler": False,
            "sklearn_version": "test",
            "timing_assumption": prep.TIMING_ASSUMPTION,
            "warnings": [],
            "output_files": [],
            "selected": fitted["selected"],
            "test_metrics": {},
        }
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            written = run_phase5.write_outputs(
                split,
                fitted,
                evaluated,
                metadata,
                models_dir=root / "models",
                evaluation_dir=root / "evaluation",
                display_root=root,
            )
            self.assertIn("models/logistic_regression.joblib", written)
            self.assertIn("evaluation/phase5_evaluation_report.md", written)
            run_phase5.verify_saved_models(split, evaluated, root / "models")
            report = (root / "evaluation" / "phase5_evaluation_report.md").read_text(encoding="utf-8")
            measured = f"{evaluated['test_metrics'][training.LOGISTIC_MODEL_NAME]['macro_f1']:.6f}"
            self.assertIn(measured, report)
            self.assertIn("does not select a single winning algorithm", report)
            stored = json.loads((root / "evaluation" / "test_metrics.json").read_text(encoding="utf-8"))
            self.assertEqual(set(stored), set(run_phase5.MODEL_FILES))


if __name__ == "__main__":
    unittest.main()
