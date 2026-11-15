"""Checks for the approved preprocessing path. No model is trained."""

from __future__ import annotations

import hashlib
import sys
import unittest
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.model_selection import StratifiedKFold, train_test_split
from sklearn.preprocessing import FunctionTransformer, OneHotEncoder, StandardScaler

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

import preprocessing as prep  # noqa: E402

RAW_SHA256 = "3ef126de5cefff26eb11fbb4237f1a1401cb64b488e2f1d598c23cedeb4c45ae"
FIRST_SEMESTER_ZERO_GRADES = 718
SECOND_SEMESTER_ZERO_GRADES = 870


def _synthetic_frame(rows_per_class: int = 6) -> pd.DataFrame:
    labels = [label for label in prep.ALLOWED_LABELS for _ in range(rows_per_class)]
    n_rows = len(labels)
    data = {column: np.arange(n_rows) % 7 for column in prep.RETAINED_FEATURES}
    for column in prep.BINARY_FEATURES:
        data[column] = np.arange(n_rows) % 2
    data["Application order"] = np.arange(n_rows) % 10
    data["Course"] = np.where(np.arange(n_rows) == n_rows - 1, 9991, 33)
    for column in prep.EXCLUDED_FEATURES:
        data[column] = np.arange(n_rows)
    data[prep.TARGET_COLUMN] = labels
    return pd.DataFrame(data)


class OfficialFileTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.before_hash = hashlib.sha256(prep.RAW_CSV.read_bytes()).hexdigest()
        cls.split = prep.prepare_from_raw()

    def test_raw_file_is_unchanged(self):
        after_hash = hashlib.sha256(prep.RAW_CSV.read_bytes()).hexdigest()
        self.assertEqual(self.before_hash, RAW_SHA256)
        self.assertEqual(after_hash, RAW_SHA256)

    def test_feature_matrix_excludes_forbidden_columns(self):
        features = self.split.features
        self.assertEqual(list(features.columns), list(prep.RETAINED_FEATURES))
        self.assertEqual(len(features.columns), 30)
        self.assertFalse(set(prep.EXCLUDED_FEATURES).intersection(features.columns))
        self.assertNotIn(prep.TARGET_COLUMN, features.columns)
        self.assertTrue(set(prep.PROVISIONAL_FEATURES).issubset(features.columns))
        self.assertIn("unverified", prep.TIMING_ASSUMPTION)

    def test_rows_and_zero_grades_are_preserved(self):
        frame = self.split.frame
        self.assertEqual(len(frame), 4424)
        self.assertEqual(self.split.duplicate_row_count, 0)
        self.assertEqual(len(self.split.features), len(frame))
        self.assertEqual(len(self.split.X_train) + len(self.split.X_test), len(frame))
        self.assertTrue(self.split.X_train.index.intersection(self.split.X_test.index).empty)
        for column, expected in (
            ("Curricular units 1st sem (grade)", FIRST_SEMESTER_ZERO_GRADES),
            ("Curricular units 2nd sem (grade)", SECOND_SEMESTER_ZERO_GRADES),
        ):
            self.assertEqual(int((frame[column] == 0).sum()), expected)
            self.assertEqual(int((self.split.features[column] == 0).sum()), expected)
            split_zeros = int((self.split.X_train[column] == 0).sum()) + int(
                (self.split.X_test[column] == 0).sum()
            )
            self.assertEqual(split_zeros, expected)

    def test_split_is_stratified_with_seed_42(self):
        features = self.split.features
        target = self.split.target
        expected_train, expected_test, _, _ = train_test_split(
            features,
            target,
            test_size=0.2,
            stratify=target,
            random_state=42,
        )
        other_train, _, _, _ = train_test_split(
            features,
            target,
            test_size=0.2,
            stratify=target,
            random_state=0,
        )
        self.assertTrue(self.split.X_train.index.equals(expected_train.index))
        self.assertTrue(self.split.X_test.index.equals(expected_test.index))
        self.assertFalse(self.split.X_train.index.equals(other_train.index))
        self.assertEqual(len(self.split.X_train) + len(self.split.X_test), 4424)
        overall = target.value_counts(normalize=True).sort_index()
        test_share = self.split.y_test.value_counts(normalize=True).sort_index()
        self.assertTrue(np.allclose(overall.to_numpy(), test_share.to_numpy(), atol=0.02))
        self.assertEqual(set(self.split.y_train.unique()), set(prep.ALLOWED_LABELS))
        self.assertEqual(set(self.split.y_test.unique()), set(prep.ALLOWED_LABELS))

    def test_cross_validation_uses_training_rows_only(self):
        cv = self.split.cv
        self.assertIsInstance(cv, StratifiedKFold)
        self.assertEqual(cv.n_splits, 5)
        self.assertTrue(cv.shuffle)
        self.assertEqual(cv.random_state, 42)
        reference = list(
            StratifiedKFold(n_splits=5, shuffle=True, random_state=42).split(
                self.split.X_train, self.split.y_train
            )
        )
        folds = list(
            prep.iter_training_folds(self.split.X_train, self.split.y_train, self.split.X_test)
        )
        self.assertEqual(len(folds), 5)
        seen_valid = []
        test_ids = set(self.split.X_test.index)
        for fold_id, fold_train, fold_valid in folds:
            train_pos, valid_pos = reference[fold_id]
            self.assertTrue(fold_train.index.equals(self.split.X_train.iloc[train_pos].index))
            self.assertTrue(fold_valid.index.equals(self.split.X_train.iloc[valid_pos].index))
            self.assertTrue(set(fold_train.index).isdisjoint(set(fold_valid.index)))
            self.assertTrue(set(fold_train.index).isdisjoint(test_ids))
            self.assertTrue(set(fold_valid.index).isdisjoint(test_ids))
            seen_valid.extend(fold_valid.index.tolist())
        self.assertEqual(sorted(seen_valid), sorted(self.split.X_train.index.tolist()))

    def test_scaling_is_fitted_on_training_rows_only(self):
        logistic = prep.fit_preprocessor(self.split.logistic_preprocessor, self.split.X_train)
        forest = prep.fit_preprocessor(self.split.forest_preprocessor, self.split.X_train)
        logistic_numeric = logistic.named_steps["preprocess"].named_transformers_["numeric"]
        forest_numeric = forest.named_steps["preprocess"].named_transformers_["numeric"]
        self.assertIsInstance(logistic_numeric, StandardScaler)
        self.assertIsInstance(forest_numeric, FunctionTransformer)
        self.assertIsNone(forest_numeric.func)
        self.assertEqual(list(logistic_numeric.feature_names_in_), list(prep.NUMERIC_FEATURES))
        self.assertTrue(
            set(logistic_numeric.feature_names_in_).isdisjoint(prep.BINARY_FEATURES)
        )
        self.assertTrue(
            set(logistic_numeric.feature_names_in_).isdisjoint(prep.NOMINAL_FEATURES)
        )
        train_means = self.split.X_train[list(prep.NUMERIC_FEATURES)].astype(float).mean().to_numpy()
        full_means = self.split.features[list(prep.NUMERIC_FEATURES)].astype(float).mean().to_numpy()
        np.testing.assert_allclose(logistic_numeric.mean_, train_means)
        self.assertFalse(np.allclose(logistic_numeric.mean_, full_means))
        self.assertEqual(int(logistic_numeric.n_samples_seen_), len(self.split.X_train))
        logistic.transform(self.split.X_test)
        self.assertEqual(int(logistic_numeric.n_samples_seen_), len(self.split.X_train))

        names = list(forest.named_steps["preprocess"].get_feature_names_out())
        grade = "numeric__Curricular units 2nd sem (grade)"
        zero_rows = self.split.X_test.index[
            self.split.X_test["Curricular units 2nd sem (grade)"] == 0
        ]
        transformed = forest.transform(self.split.X_test.loc[zero_rows[:1]])
        self.assertEqual(transformed[0, names.index(grade)], 0.0)
        scaled = logistic.transform(self.split.X_test.loc[zero_rows[:1]])
        self.assertNotEqual(scaled[0, names.index(grade)], 0.0)

    def test_fold_scaler_does_not_see_validation_rows(self):
        fold_id, fold_train, fold_valid = next(
            prep.iter_training_folds(self.split.X_train, self.split.y_train, self.split.X_test)
        )
        self.assertEqual(fold_id, 0)
        fitted = prep.fit_preprocessor(self.split.logistic_preprocessor, fold_train)
        scaler = fitted.named_steps["preprocess"].named_transformers_["numeric"]
        fold_means = fold_train[list(prep.NUMERIC_FEATURES)].astype(float).mean().to_numpy()
        training_means = (
            self.split.X_train[list(prep.NUMERIC_FEATURES)].astype(float).mean().to_numpy()
        )
        np.testing.assert_allclose(scaler.mean_, fold_means)
        self.assertFalse(np.allclose(scaler.mean_, training_means))
        self.assertEqual(int(scaler.n_samples_seen_), len(fold_train))
        fitted.transform(fold_valid)
        self.assertEqual(int(scaler.n_samples_seen_), len(fold_train))

    def test_nominal_encoder_is_fit_on_training_levels(self):
        fitted = prep.fit_preprocessor(self.split.logistic_preprocessor, self.split.X_train)
        encoder = fitted.named_steps["preprocess"].named_transformers_["nominal"]
        self.assertIsInstance(encoder, OneHotEncoder)
        self.assertEqual(encoder.handle_unknown, "ignore")
        course_index = list(prep.NOMINAL_FEATURES).index("Course")
        learned = set(int(value) for value in encoder.categories_[course_index])
        train_levels = set(int(value) for value in self.split.X_train["Course"].unique())
        test_only = set(int(value) for value in self.split.X_test["Course"].unique()) - train_levels
        self.assertEqual(learned, train_levels)
        self.assertTrue(set(test_only).isdisjoint(learned))
        names = fitted.named_steps["preprocess"].get_feature_names_out()
        binary_names = [name for name in names if name.startswith("binary__")]
        self.assertEqual(len(binary_names), len(prep.BINARY_FEATURES))

    def test_pipelines_contain_no_classifier(self):
        source = Path(prep.__file__).read_text(encoding="utf-8")
        for banned in ("LogisticRegression", "RandomForest", "SimpleImputer", "fit_transform"):
            self.assertNotIn(banned, source)
        for pipeline in (
            self.split.logistic_preprocessor,
            self.split.forest_preprocessor,
        ):
            self.assertEqual([name for name, _ in pipeline.steps], ["preprocess"])


class GuardTests(unittest.TestCase):
    def test_missing_values_are_not_imputed(self):
        frame = _synthetic_frame()
        frame.loc[0, "Admission grade"] = np.nan
        with self.assertRaises(ValueError):
            prep.prepare_approved_split(frame)

    def test_forbidden_column_is_rejected(self):
        frame = _synthetic_frame()
        prepared = prep.prepare_approved_split(frame)
        contaminated = prepared.X_train.copy()
        contaminated["Debtor"] = 0
        with self.assertRaises(ValueError):
            prep.fit_preprocessor(prepared.logistic_preprocessor, contaminated)

    def test_unknown_category_is_ignored(self):
        frame = _synthetic_frame()
        prepared = prep.prepare_approved_split(frame)
        fitted = prep.fit_preprocessor(prepared.logistic_preprocessor, prepared.X_train)
        novel = prepared.X_test.copy()
        novel.loc[:, "Marital status"] = 99
        transformed = fitted.transform(novel)
        self.assertEqual(transformed.shape[0], len(novel))
        self.assertTrue(np.isfinite(transformed).all())

    def test_bad_target_label_is_rejected(self):
        frame = _synthetic_frame()
        frame.loc[0, prep.TARGET_COLUMN] = "Withdrawn"
        with self.assertRaises(ValueError):
            prep.prepare_approved_split(frame)


if __name__ == "__main__":
    unittest.main()
