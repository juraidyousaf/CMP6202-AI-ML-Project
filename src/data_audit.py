"""Read-only audit of the original UCI student-dropout extract.

The script reads data/raw/data.csv and writes outputs/dataset_audit.md.
It does not modify the raw archive or the extracted CSV.
"""

from __future__ import annotations

import csv
import hashlib
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW_CSV = ROOT / "data" / "raw" / "data.csv"
RAW_ZIP = ROOT / "data" / "raw" / "predict+students+dropout+and+academic+success.zip"
REPORT_PATH = ROOT / "outputs" / "dataset_audit.md"

UCI_INSTANCES = 4424
UCI_FEATURES = 36
TARGET_COLUMN = "Target"
EXPECTED_CLASSES = ("Dropout", "Enrolled", "Graduate")

# Official code lists copied from the UCI dataset API on 2026-11-14.
# A value is reported only when it is absent from the list captured here.
CODE_LISTS: dict[str, set[int]] = {
    "marital status": {1, 2, 3, 4, 5, 6},
    "application mode": {1, 2, 5, 7, 10, 15, 16, 17, 18, 26, 27, 39, 42, 43, 44, 51, 53, 57},
    "course": {33, 171, 8014, 9003, 9070, 9085, 9119, 9130, 9147, 9238, 9254, 9500, 9556, 9670, 9773, 9853, 9991},
    "daytime/evening attendance": {0, 1},
    "previous qualification": {1, 2, 3, 4, 5, 6, 9, 10, 12, 14, 15, 19, 38, 39, 40, 42, 43},
    "nacionality": {1, 2, 6, 11, 13, 14, 17, 21, 22, 24, 25, 26, 32, 41, 62, 100, 101, 103, 105, 108, 109},
    "mother's qualification": {1, 2, 3, 4, 5, 6, 9, 10, 11, 12, 14, 18, 19, 22, 26, 27, 29, 30, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44},
    "father's qualification": {1, 2, 3, 4, 5, 6, 9, 10, 11, 12, 13, 14, 18, 19, 20, 22, 25, 26, 27, 29, 30, 31, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44},
    "mother's occupation": {0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 90, 99, 122, 123, 125, 131, 132, 134, 141, 143, 144, 151, 152, 153, 171, 173, 175, 191, 192, 193, 194},
    "father's occupation": {0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 90, 99, 101, 102, 103, 112, 114, 121, 122, 123, 124, 131, 132, 134, 135, 141, 143, 144, 151, 152, 153, 154, 161, 163, 171, 172, 174, 175, 181, 182, 183, 192, 193, 194, 195},
    "displaced": {0, 1},
    "educational special needs": {0, 1},
    "debtor": {0, 1},
    "tuition fees up to date": {0, 1},
    "gender": {0, 1},
    "scholarship holder": {0, 1},
    "international": {0, 1},
}

# kind is the modelling interpretation, not the pandas dtype.
# timing is relative to the approved prediction point: after the second semester.
COLUMN_GUIDE: dict[str, dict[str, str]] = {
    "marital status": {"kind": "categorical code", "timing": "Known at enrolment, from the UCI description.", "uci_type": "Integer"},
    "application mode": {"kind": "categorical code", "timing": "Known at enrolment, from the UCI description.", "uci_type": "Integer"},
    "application order": {"kind": "ordinal integer (0 = first choice through 9 = last choice)", "timing": "Known at enrolment, from the UCI description.", "uci_type": "Integer"},
    "course": {"kind": "categorical code", "timing": "Known at enrolment, from the UCI description.", "uci_type": "Integer"},
    "daytime/evening attendance": {"kind": "binary category", "timing": "Known at enrolment, from the UCI description.", "uci_type": "Integer"},
    "previous qualification": {"kind": "categorical code", "timing": "Known at enrolment, from the UCI description.", "uci_type": "Integer"},
    "previous qualification (grade)": {"kind": "continuous grade", "timing": "Known at enrolment, from the UCI description.", "uci_type": "Continuous"},
    "nacionality": {"kind": "categorical code", "timing": "Known at enrolment. UCI marks this as demographic (nationality).", "uci_type": "Integer"},
    "mother's qualification": {"kind": "categorical code", "timing": "Known at enrolment. UCI marks this as demographic (education level).", "uci_type": "Integer"},
    "father's qualification": {"kind": "categorical code", "timing": "Known at enrolment. UCI marks this as demographic (education level).", "uci_type": "Integer"},
    "mother's occupation": {"kind": "categorical code", "timing": "Known at enrolment. UCI marks this as demographic (occupation).", "uci_type": "Integer"},
    "father's occupation": {"kind": "categorical code", "timing": "Known at enrolment. UCI marks this as demographic (occupation).", "uci_type": "Integer"},
    "admission grade": {"kind": "continuous grade", "timing": "Known at enrolment, from the UCI description.", "uci_type": "Continuous"},
    "displaced": {"kind": "binary category", "timing": "Described as a yes/no student attribute. UCI does not give a measurement date.", "uci_type": "Integer"},
    "educational special needs": {"kind": "binary category", "timing": "Described as a yes/no student attribute. UCI does not give a measurement date.", "uci_type": "Integer"},
    "debtor": {"kind": "binary category", "timing": "Measurement date is not stated. Possible later administrative status.", "uci_type": "Integer"},
    "tuition fees up to date": {"kind": "binary category", "timing": "Measurement date is not stated. Possible later administrative status.", "uci_type": "Integer"},
    "gender": {"kind": "binary category", "timing": "Known at enrolment. UCI marks this as demographic (gender).", "uci_type": "Integer"},
    "scholarship holder": {"kind": "binary category", "timing": "Described as a yes/no student attribute. UCI does not give a measurement date.", "uci_type": "Integer"},
    "age at enrollment": {"kind": "numerical count", "timing": "Known at enrolment, from the UCI description.", "uci_type": "Integer"},
    "international": {"kind": "binary category", "timing": "Described as a yes/no student attribute. UCI does not give a measurement date.", "uci_type": "Integer"},
    "curricular units 1st sem (credited)": {"kind": "numerical count", "timing": "End of the first semester, so available after the second semester.", "uci_type": "Integer"},
    "curricular units 1st sem (enrolled)": {"kind": "numerical count", "timing": "End of the first semester, so available after the second semester.", "uci_type": "Integer"},
    "curricular units 1st sem (evaluations)": {"kind": "numerical count", "timing": "End of the first semester, so available after the second semester.", "uci_type": "Integer"},
    "curricular units 1st sem (approved)": {"kind": "numerical count", "timing": "End of the first semester, so available after the second semester.", "uci_type": "Integer"},
    "curricular units 1st sem (grade)": {"kind": "numerical grade average", "timing": "End of the first semester, so available after the second semester.", "uci_type": "Integer"},
    "curricular units 1st sem (without evaluations)": {"kind": "numerical count", "timing": "End of the first semester, so available after the second semester.", "uci_type": "Integer"},
    "curricular units 2nd sem (credited)": {"kind": "numerical count", "timing": "End of the second semester, the approved prediction point.", "uci_type": "Integer"},
    "curricular units 2nd sem (enrolled)": {"kind": "numerical count", "timing": "End of the second semester, the approved prediction point.", "uci_type": "Integer"},
    "curricular units 2nd sem (evaluations)": {"kind": "numerical count", "timing": "End of the second semester, the approved prediction point.", "uci_type": "Integer"},
    "curricular units 2nd sem (approved)": {"kind": "numerical count", "timing": "End of the second semester, the approved prediction point.", "uci_type": "Integer"},
    "curricular units 2nd sem (grade)": {"kind": "numerical grade average", "timing": "End of the second semester, the approved prediction point.", "uci_type": "Integer"},
    "curricular units 2nd sem (without evaluations)": {"kind": "numerical count", "timing": "Column name says second semester. The UCI description text says first semester, which conflicts with the name.", "uci_type": "Integer"},
    "unemployment rate": {"kind": "continuous context variable", "timing": "Reference period is not stated by UCI.", "uci_type": "Continuous"},
    "inflation rate": {"kind": "continuous context variable", "timing": "Reference period is not stated by UCI.", "uci_type": "Continuous"},
    "gdp": {"kind": "continuous context variable", "timing": "Reference period is not stated by UCI.", "uci_type": "Continuous"},
    "target": {"kind": "target category", "timing": "Eventual outcome at the end of the normal course duration. This is after the second semester and must not be an input.", "uci_type": "Categorical"},
}

RANGE_CHECKS: dict[str, tuple[float, float]] = {
    "previous qualification (grade)": (0, 200),
    "admission grade": (0, 200),
    "application order": (0, 9),
    "curricular units 1st sem (grade)": (0, 20),
    "curricular units 2nd sem (grade)": (0, 20),
}


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def normalise_name(name: str) -> str:
    return " ".join(name.replace("\t", " ").split()).casefold()


def detect_encoding(raw: bytes) -> str:
    if raw.startswith(b"\xef\xbb\xbf"):
        return "utf-8-sig"
    try:
        raw.decode("utf-8")
    except UnicodeDecodeError:
        return "cp1252"
    return "utf-8"


def detect_delimiter(header_line: str) -> str:
    """Choose a delimiter from separators that occur outside quotation marks."""
    counts = {",": 0, ";": 0, "\t": 0}
    in_quotes = False
    for character in header_line:
        if character == '"':
            in_quotes = not in_quotes
        elif not in_quotes and character in counts:
            counts[character] += 1
    best = max(counts, key=counts.get)
    if counts[best] == 0:
        raise ValueError("No comma, semicolon, or tab delimiter was found in the header.")
    return best


def load_dataset(path: Path) -> tuple[pd.DataFrame, dict[str, str]]:
    if not path.is_file():
        raise FileNotFoundError(f"Original dataset was not found at {path}.")
    raw = path.read_bytes()
    encoding = detect_encoding(raw)
    text = raw.decode("utf-8-sig" if encoding == "utf-8-sig" else encoding)
    header_line = text.splitlines()[0]
    delimiter = detect_delimiter(header_line)
    frame = pd.read_csv(path, sep=delimiter, encoding=encoding)
    details = {
        "encoding": "UTF-8 with BOM" if encoding == "utf-8-sig" else encoding,
        "pandas_encoding": encoding,
        "delimiter": {",": "comma", ";": "semicolon", "\t": "tab"}[delimiter],
        "delimiter_char": delimiter,
    }
    return frame, details


def markdown_cell(value: object) -> str:
    text = str(value).replace("\t", "\\t").replace("|", "\\|")
    return text


def percentage(count: int, total: int) -> str:
    if total == 0:
        return "undefined"
    return f"{(count / total) * 100:.4f}%"


def outside_code_list(series: pd.Series, allowed: set[int]) -> list[str]:
    observed = pd.to_numeric(series, errors="coerce")
    unexpected = sorted({value for value in observed.dropna().unique() if int(value) not in allowed and float(value).is_integer()})
    non_integer = int((observed.dropna() % 1 != 0).sum())
    notes = [str(value) for value in unexpected]
    if non_integer:
        notes.append(f"{non_integer} non-integer values")
    return notes


def main() -> None:
    frame, details = load_dataset(RAW_CSV)
    row_count, column_count = frame.shape
    feature_count = column_count - (1 if TARGET_COLUMN in frame.columns else 0)
    duplicate_names = frame.columns[frame.columns.duplicated()].tolist()
    duplicate_rows = int(frame.duplicated().sum())
    missing_by_column = frame.isna().sum()
    total_missing = int(missing_by_column.sum())
    empty_strings = {
        column: int((frame[column].astype(str).str.strip() == "").sum())
        for column in frame.columns
        if frame[column].dtype == object
    }

    lines: list[str] = []
    add = lines.append
    add("# Dataset audit")
    add("")
    add("Read-only audit of the extracted original file. No rows or columns were changed. No model was trained.")
    add("")
    add("## Download record")
    add("")
    add("| Item | Record |")
    add("| --- | --- |")
    add("| Source page | https://archive.ics.uci.edu/dataset/697/predict |")
    add("| Archive URL | https://archive.ics.uci.edu/static/public/697/predict+students+dropout+and+academic+success.zip |")
    add("| Download date | 2026-11-14 |")
    add("| Archive filename | `predict+students+dropout+and+academic+success.zip` |")
    add(f"| Archive size | {RAW_ZIP.stat().st_size} bytes |")
    add(f"| Archive SHA-256 | `{file_sha256(RAW_ZIP)}` |")
    add("| Extracted filename | `data.csv` |")
    add("| Extracted path | `data/raw/data.csv` |")
    add(f"| Extracted size | {RAW_CSV.stat().st_size} bytes |")
    add(f"| Extracted SHA-256 | `{file_sha256(RAW_CSV)}` |")
    add("| Licence | Creative Commons Attribution 4.0 International (CC BY 4.0) |")
    add("| Licence source | UCI dataset page, checked 2026-11-14. The page says the dataset is licensed under a Creative Commons Attribution 4.0 International (CC BY 4.0) licence and links to https://creativecommons.org/licenses/by/4.0/legalcode. |")
    add("| DOI | https://doi.org/10.24432/C5MC89 |")
    add("")
    add("The project file is the `data.csv` extracted from that official zip. It was not edited after extraction.")
    add("")
    add("UCI also publishes https://archive.ics.uci.edu/static/public/697/data.csv. On 2026-11-14 that direct file was 495,642 bytes, comma-separated, and not byte-identical to the zip extract. It had the same measured shape, 4,424 rows by 37 columns, and the same target counts: Graduate 2,209, Dropout 1,421, Enrolled 794. Its `Daytime/evening attendance` header does not contain a tab, and it spells `Marital Status` with a capital S. That comparison file was not kept, so this script does not re-download it.")
    add("")
    add("## File format")
    add("")
    add(f"- Encoding: {details['encoding']}.")
    add(f"- Delimiter: {details['delimiter']}. This was detected from the header. It was not assumed.")
    add(f"- Measured shape: {row_count} rows by {column_count} columns.")
    add(f"- Input features, treating `{TARGET_COLUMN}` as separate from the features: {feature_count}.")
    add("")
    add("## Comparison with UCI metadata")
    add("")
    add("UCI metadata is not a local measurement. The local measurement is the table above.")
    add("")
    add("| Check | UCI metadata | Local measurement | Agreement |")
    add("| --- | --- | --- | --- |")
    add(f"| Instances | {UCI_INSTANCES} | {row_count} | {'Yes' if row_count == UCI_INSTANCES else 'No'} |")
    add(f"| Input features | {UCI_FEATURES} | {feature_count} | {'Yes' if feature_count == UCI_FEATURES else 'No'} |")
    add(f"| Target column present | Target | {'Yes' if TARGET_COLUMN in frame.columns else 'No'} | {'Yes' if TARGET_COLUMN in frame.columns else 'No'} |")
    add("| UCI missing-values flag | no | See the missing-value section | Compared below |")
    add("")
    add("## Target")
    add("")
    if TARGET_COLUMN not in frame.columns:
        add(f"`{TARGET_COLUMN}` is not in the file. The audit cannot confirm the classes.")
    else:
        counts = frame[TARGET_COLUMN].value_counts(dropna=False)
        observed = set(counts.index.astype(str))
        add(f"Pandas dtype: `{frame[TARGET_COLUMN].dtype}`.")
        add("")
        add("| Class | Count | Percentage of rows |")
        add("| --- | --- | --- |")
        for label, count in counts.items():
            add(f"| {markdown_cell(label)} | {int(count)} | {percentage(int(count), row_count)} |")
        add("")
        missing_classes = [label for label in EXPECTED_CLASSES if label not in observed]
        extra_classes = [label for label in observed if label not in EXPECTED_CLASSES]
        add(f"Expected classes present: {', '.join(EXPECTED_CLASSES) if not missing_classes else 'missing ' + ', '.join(missing_classes)}.")
        add(f"Unexpected target labels: {', '.join(extra_classes) if extra_classes else 'none'}.")
        add("Percentages are `count / number of rows × 100`, shown to four decimal places.")
    add("")
    add("## Missing values")
    add("")
    add(f"Total missing cells reported by pandas: {total_missing}.")
    add("")
    add("| Column | Missing cells |")
    add("| --- | --- |")
    for column, missing_count in missing_by_column.items():
        add(f"| {markdown_cell(column)} | {int(missing_count)} |")
    blank_total = sum(empty_strings.values())
    add("")
    add(f"Empty strings in object columns: {blank_total}.")
    add("")
    add("## Duplicates")
    add("")
    add(f"Duplicate column names: {duplicate_names if duplicate_names else 'none'}.")
    add(f"Fully duplicate rows: {duplicate_rows}.")
    add("")
    add("## Column dictionary")
    add("")
    add("Integer codes are not treated as continuous numbers. The interpretation follows the UCI variable type and description. Pandas dtypes are reported separately because they only describe storage.")
    add("")
    add("| Column | Pandas dtype | Missing | Unique values | UCI type | Interpretation | Prediction-time note |")
    add("| --- | --- | --- | --- | --- | --- | --- |")
    for column in frame.columns:
        key = normalise_name(column)
        guide = COLUMN_GUIDE.get(key, {"kind": "unlisted in the captured UCI guide", "timing": "Not matched to a UCI variable name.", "uci_type": "not matched"})
        add(
            f"| {markdown_cell(column)} | `{frame[column].dtype}` | {int(missing_by_column[column])} | "
            f"{int(frame[column].nunique(dropna=False))} | {guide['uci_type']} | {guide['kind']} | {guide['timing']} |"
        )
    add("")
    add("## Categorical and numerical candidates")
    add("")
    categorical = []
    numerical = []
    other = []
    for column in frame.columns:
        kind = COLUMN_GUIDE.get(normalise_name(column), {}).get("kind", "")
        if "categorical" in kind or "binary" in kind or "ordinal" in kind or kind == "target category":
            categorical.append(column)
        elif "numerical" in kind or "continuous" in kind:
            numerical.append(column)
        else:
            other.append(column)
    add("Categorical candidates, including binary and ordinal codes:")
    add("")
    for column in categorical:
        add(f"- `{markdown_cell(column)}`")
    add("")
    add("Numerical candidates, including counts, grades, and context rates:")
    add("")
    for column in numerical:
        add(f"- `{markdown_cell(column)}`")
    if other:
        add("")
        add("Columns not matched to the captured UCI guide:")
        add("")
        for column in other:
            add(f"- `{markdown_cell(column)}`")
    add("")
    constant = [column for column in frame.columns if frame[column].nunique(dropna=False) <= 1]
    add(f"Constant columns: {', '.join(repr(column) for column in constant) if constant else 'none'}.")
    add("")
    add("## Values outside the captured UCI lists or ranges")
    add("")
    findings = []
    for column in frame.columns:
        key = normalise_name(column)
        if key in CODE_LISTS:
            unexpected = outside_code_list(frame[column], CODE_LISTS[key])
            if unexpected:
                findings.append(f"- `{markdown_cell(column)}`: values not in the captured UCI code list: {', '.join(unexpected)}.")
        if key in RANGE_CHECKS:
            low, high = RANGE_CHECKS[key]
            numeric = pd.to_numeric(frame[column], errors="coerce")
            outside = int(((numeric < low) | (numeric > high)).sum())
            if outside:
                findings.append(f"- `{markdown_cell(column)}`: {outside} values outside the UCI-described range {low} to {high}.")
    age_key = "age at enrollment"
    age_column = next((column for column in frame.columns if normalise_name(column) == age_key), None)
    if age_column is not None:
        age = pd.to_numeric(frame[age_column], errors="coerce")
        add(f"Age at enrollment ranges from {age.min()} to {age.max()}. UCI does not publish an allowed age range. Values below 16 or above 90 are flagged here only as a review heuristic.")
        unusual_age = int(((age < 16) | (age > 90)).sum())
        add(f"Rows outside that heuristic: {unusual_age}.")
        add("")
    if findings:
        add("Code-list and range findings:")
        add("")
        lines.extend(findings)
    else:
        add("No observed value fell outside the captured UCI code lists or the stated grade and application-order ranges.")
    add("")
    add("A code that is absent from the captured list is a documentation mismatch to review. It is not, by itself, a reason to delete the row.")
    add("")
    add("## Prediction-time review")
    add("")
    add("The approved prediction point is after the second semester. No feature was removed.")
    add("")
    add("Features whose UCI descriptions place them at enrolment, or at the end of the first or second semester, are available by that prediction point. The target is the later outcome and is not an input.")
    add("")
    add("Items that need a later decision:")
    add("")
    add("- `Debtor` and `Tuition fees up to date` are yes/no fields. UCI does not say whether they were measured at enrolment, during the second semester, or later.")
    add("- `Unemployment rate`, `Inflation rate`, and `GDP` have no stated reference date. They may be enrolment-year context, or they may not line up with the prediction point.")
    add("- `Curricular units 2nd sem (without evaluations)` is named as a second-semester count, but the UCI description says \"in the 1st semester\". The column was kept. The description conflict is unresolved.")
    add("- The zip extract names `Daytime/evening attendance` with a trailing tab character inside the header. The UCI direct CSV does not. The tab is preserved because this audit does not edit the raw file. Later loading code must match the actual header.")
    add("- `Marital status` in the zip extract does not use the capital S shown in the UCI API name `Marital Status`.")
    add("")
    add("No column other than `Target` is described by UCI as the final dropout, enrolled, or graduate outcome.")
    add("")
    add("## What this audit did not do")
    add("")
    add("No plots, cleaning, train/test split, or model training was done. Class counts above are counts of this file, not a model result.")
    add("")

    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {REPORT_PATH.relative_to(ROOT)}")
    print(f"shape={row_count}x{column_count} features={feature_count} missing={total_missing} duplicate_rows={duplicate_rows}")


if __name__ == "__main__":
    main()
