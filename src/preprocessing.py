"""Approved Phase 4 preprocessing. No model is trained here.

The raw CSV is read and left unchanged. Column names are cleaned in memory
only: the daytime/evening header has a trailing tab in the zip extract.

`Displaced`, `Educational special needs`, `Scholarship holder`, and
`International` are retained under an unverified timing assumption. Their
individual UCI descriptions do not give measurement dates. The dataset
narrative is being treated as evidence that they are available after the
second semester. That date has not been verified. The final report must
state this limitation.

Recorded semester grades of 0 stay numeric zero in the feature matrix.
Standardising those columns inside the logistic preprocessor changes the
units of the transformed matrix. It does not replace, impute, or delete
the stored zeros, and it is not a zero-grade sensitivity analysis.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import pandas as pd
from sklearn.base import clone
from sklearn.compose import ColumnTransformer
from sklearn.model_selection import StratifiedKFold, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

ROOT = Path(__file__).resolve().parents[1]
RAW_CSV = ROOT / "data" / "raw" / "data.csv"

TARGET_COLUMN = "Target"
ALLOWED_LABELS = ("Dropout", "Enrolled", "Graduate")
TEST_SIZE = 0.2
RANDOM_STATE = 42
CV_SPLITS = 5

TIMING_ASSUMPTION = (
    "Displaced, Educational special needs, Scholarship holder, and "
    "International are retained although their individual UCI descriptions "
    "do not state a measurement date. Availability after the second semester "
    "is an unverified modelling assumption, not a confirmed date."
)

PROVISIONAL_FEATURES = (
    "Displaced",
    "Educational special needs",
    "Scholarship holder",
    "International",
)

EXCLUDED_FEATURES = (
    "Debtor",
    "Tuition fees up to date",
    "Unemployment rate",
    "Inflation rate",
    "GDP",
    "Curricular units 2nd sem (without evaluations)",
)

BINARY_FEATURES = (
    "Daytime/evening attendance",
    "Displaced",
    "Educational special needs",
    "Gender",
    "Scholarship holder",
    "International",
)

ORDINAL_FEATURES = ("Application order",)

NOMINAL_FEATURES = (
    "Marital status",
    "Application mode",
    "Course",
    "Previous qualification",
    "Nacionality",
    "Mother's qualification",
    "Father's qualification",
    "Mother's occupation",
    "Father's occupation",
)

NUMERIC_FEATURES = (
    "Previous qualification (grade)",
    "Admission grade",
    "Curricular units 1st sem (grade)",
    "Curricular units 2nd sem (grade)",
    "Age at enrollment",
    "Curricular units 1st sem (credited)",
    "Curricular units 1st sem (enrolled)",
    "Curricular units 1st sem (evaluations)",
    "Curricular units 1st sem (approved)",
    "Curricular units 1st sem (without evaluations)",
    "Curricular units 2nd sem (credited)",
    "Curricular units 2nd sem (enrolled)",
    "Curricular units 2nd sem (evaluations)",
    "Curricular units 2nd sem (approved)",
)

RETAINED_FEATURES = (
    "Marital status",
    "Application mode",
    "Application order",
    "Course",
    "Daytime/evening attendance",
    "Previous qualification",
    "Previous qualification (grade)",
    "Nacionality",
    "Mother's qualification",
    "Father's qualification",
    "Mother's occupation",
    "Father's occupation",
    "Admission grade",
    "Displaced",
    "Educational special needs",
    "Gender",
    "Scholarship holder",
    "Age at enrollment",
    "International",
    "Curricular units 1st sem (credited)",
    "Curricular units 1st sem (enrolled)",
    "Curricular units 1st sem (evaluations)",
    "Curricular units 1st sem (approved)",
    "Curricular units 1st sem (grade)",
    "Curricular units 1st sem (without evaluations)",
    "Curricular units 2nd sem (credited)",
    "Curricular units 2nd sem (enrolled)",
    "Curricular units 2nd sem (evaluations)",
    "Curricular units 2nd sem (approved)",
    "Curricular units 2nd sem (grade)",
)

GRADE_FEATURES = (
    "Curricular units 1st sem (grade)",
    "Curricular units 2nd sem (grade)",
)


def _check_feature_lists() -> None:
    grouped = BINARY_FEATURES + ORDINAL_FEATURES + NOMINAL_FEATURES + NUMERIC_FEATURES
    if len(grouped) != len(set(grouped)):
        raise RuntimeError("Feature groups overlap.")
    if set(grouped) != set(RETAINED_FEATURES):
        raise RuntimeError("Retained features and feature groups do not match.")
    if set(RETAINED_FEATURES) & set(EXCLUDED_FEATURES):
        raise RuntimeError("A retained feature is also excluded.")
    if TARGET_COLUMN in RETAINED_FEATURES or TARGET_COLUMN in EXCLUDED_FEATURES:
        raise RuntimeError("Target must stay out of the feature lists.")
    if set(PROVISIONAL_FEATURES) - set(RETAINED_FEATURES):
        raise RuntimeError("A provisional feature is missing from the retained list.")


_check_feature_lists()


@dataclass(frozen=True)
class ApprovedSplit:
    """Unfitted preprocessors and the approved train/test split.

    The preprocessors are templates. Fit them on training rows only.
    """

    frame: pd.DataFrame
    features: pd.DataFrame
    target: pd.Series
    X_train: pd.DataFrame
    X_test: pd.DataFrame
    y_train: pd.Series
    y_test: pd.Series
    logistic_preprocessor: Pipeline
    forest_preprocessor: Pipeline
    cv: StratifiedKFold
    duplicate_row_count: int


def clean_column_names(frame: pd.DataFrame) -> pd.DataFrame:
    """Strip tab characters from column names in memory. Do not write the file."""
    cleaned = frame.copy()
    cleaned.columns = [str(name).replace("\t", "").strip() for name in cleaned.columns]
    duplicates = cleaned.columns[cleaned.columns.duplicated()].tolist()
    if duplicates:
        raise ValueError(f"Column names are not unique after tab stripping: {duplicates}")
    return cleaned


def load_raw_table(path: Path | None = None) -> pd.DataFrame:
    """Read the semicolon-separated extract without modifying it."""
    csv_path = RAW_CSV if path is None else Path(path)
    frame = pd.read_csv(csv_path, sep=";", encoding="utf-8-sig")
    return clean_column_names(frame)


def validate_source_table(frame: pd.DataFrame) -> int:
    """Check the loaded table. Return the duplicate-row count without dropping rows."""
    required = list(RETAINED_FEATURES) + list(EXCLUDED_FEATURES) + [TARGET_COLUMN]
    missing_columns = [column for column in required if column not in frame.columns]
    if missing_columns:
        raise ValueError(f"Required columns are missing: {missing_columns}")
    if frame.isna().to_numpy().any():
        raise ValueError("Missing values are present. The approved plan does not impute them.")
    labels = set(frame[TARGET_COLUMN].astype(str).unique())
    if labels != set(ALLOWED_LABELS):
        raise ValueError(f"Target labels must be {ALLOWED_LABELS}, found {sorted(labels)}.")
    for column in BINARY_FEATURES:
        values = set(pd.to_numeric(frame[column], errors="raise").unique())
        if not values.issubset({0, 1}):
            raise ValueError(f"{column} must stay a 0/1 code, found {sorted(values)}.")
    order = pd.to_numeric(frame[ORDINAL_FEATURES[0]], errors="raise")
    if order.lt(0).any() or order.gt(9).any():
        raise ValueError("Application order must stay in the documented range 0 through 9.")
    duplicate_row_count = int(frame.duplicated().sum())
    return duplicate_row_count


def select_features_and_target(frame: pd.DataFrame) -> tuple[pd.DataFrame, pd.Series]:
    """Copy the retained columns and the label. Do not drop rows."""
    forbidden = set(EXCLUDED_FEATURES) | {TARGET_COLUMN}
    features = frame.loc[:, list(RETAINED_FEATURES)].copy()
    target = frame[TARGET_COLUMN].copy()
    leaked = forbidden.intersection(features.columns)
    if leaked:
        raise ValueError(f"Forbidden columns entered the feature matrix: {sorted(leaked)}")
    if list(features.columns) != list(RETAINED_FEATURES):
        raise ValueError("Feature matrix columns differ from the approved list.")
    if len(features) != len(frame) or len(target) != len(frame):
        raise ValueError("Selecting features dropped rows.")
    return features, target


def reject_forbidden_columns(features: pd.DataFrame) -> None:
    forbidden = set(EXCLUDED_FEATURES) | {TARGET_COLUMN}
    found = forbidden.intersection(features.columns)
    if found:
        raise ValueError(f"Forbidden columns cannot be transformed: {sorted(found)}")
    missing = [column for column in RETAINED_FEATURES if column not in features.columns]
    if missing:
        raise ValueError(f"Approved features are missing: {missing}")


def make_training_cv() -> StratifiedKFold:
    """Five stratified folds for the training portion. Shuffle uses the approved seed."""
    return StratifiedKFold(n_splits=CV_SPLITS, shuffle=True, random_state=RANDOM_STATE)


def make_column_transformer(scale_numeric: bool) -> ColumnTransformer:
    numeric_step = StandardScaler() if scale_numeric else "passthrough"
    nominal = OneHotEncoder(handle_unknown="ignore", sparse_output=False)
    return ColumnTransformer(
        transformers=[
            ("binary", "passthrough", list(BINARY_FEATURES)),
            ("ordinal", "passthrough", list(ORDINAL_FEATURES)),
            ("nominal", nominal, list(NOMINAL_FEATURES)),
            ("numeric", numeric_step, list(NUMERIC_FEATURES)),
        ],
        remainder="drop",
        verbose_feature_names_out=True,
    )


def make_logistic_preprocessor() -> Pipeline:
    """Unfitted logistic preprocessor. Numerical columns are scaled. No classifier."""
    return Pipeline(steps=[("preprocess", make_column_transformer(scale_numeric=True))])


def make_forest_preprocessor() -> Pipeline:
    """Unfitted forest preprocessor. Same columns and encoding, without scaling."""
    return Pipeline(steps=[("preprocess", make_column_transformer(scale_numeric=False))])


def split_train_test(
    features: pd.DataFrame, target: pd.Series
) -> tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
    """80/20 split, stratified on the target, with the approved seed."""
    if len(features) != len(target):
        raise ValueError("Features and target have different numbers of rows.")
    if not features.index.equals(target.index):
        raise ValueError("Features and target indices differ.")
    X_train, X_test, y_train, y_test = train_test_split(
        features,
        target,
        test_size=TEST_SIZE,
        stratify=target,
        random_state=RANDOM_STATE,
    )
    return X_train, X_test, y_train, y_test


def prepare_approved_split(frame: pd.DataFrame) -> ApprovedSplit:
    """Validate, select, and split. Preprocessors are returned unfitted."""
    duplicate_row_count = validate_source_table(frame)
    features, target = select_features_and_target(frame)
    X_train, X_test, y_train, y_test = split_train_test(features, target)
    return ApprovedSplit(
        frame=frame,
        features=features,
        target=target,
        X_train=X_train,
        X_test=X_test,
        y_train=y_train,
        y_test=y_test,
        logistic_preprocessor=make_logistic_preprocessor(),
        forest_preprocessor=make_forest_preprocessor(),
        cv=make_training_cv(),
        duplicate_row_count=duplicate_row_count,
    )


def prepare_from_raw(path: Path | None = None) -> ApprovedSplit:
    return prepare_approved_split(load_raw_table(path))


def fit_preprocessor(pipeline: Pipeline, X_train: pd.DataFrame) -> Pipeline:
    """Fit a clone on training rows only. The target is not an argument."""
    reject_forbidden_columns(X_train)
    fitted = clone(pipeline)
    fitted.fit(X_train)
    return fitted


def iter_training_folds(
    X_train: pd.DataFrame, y_train: pd.Series, X_test: pd.DataFrame
):
    """Yield training-fold positions. Test indices are rejected if they appear."""
    if not X_train.index.intersection(X_test.index).empty:
        raise ValueError("Training indices overlap the test indices.")
    if len(X_train) != len(y_train) or not X_train.index.equals(y_train.index):
        raise ValueError("Training features and labels do not match.")
    test_ids = set(X_test.index)
    cv = make_training_cv()
    for fold_id, (train_positions, valid_positions) in enumerate(cv.split(X_train, y_train)):
        fold_train = X_train.iloc[train_positions]
        fold_valid = X_train.iloc[valid_positions]
        if set(fold_train.index).union(fold_valid.index) & test_ids:
            raise ValueError("A cross-validation fold includes test rows.")
        yield fold_id, fold_train, fold_valid
