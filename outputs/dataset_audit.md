# Dataset audit

Read-only audit of the extracted original file. No rows or columns were changed. No model was trained.

## Download record

| Item | Record |
| --- | --- |
| Source page | https://archive.ics.uci.edu/dataset/697/predict |
| Archive URL | https://archive.ics.uci.edu/static/public/697/predict+students+dropout+and+academic+success.zip |
| Download date | 2026-11-14 |
| Archive filename | `predict+students+dropout+and+academic+success.zip` |
| Archive size | 533344 bytes |
| Archive SHA-256 | `e90e55fd65ec462ae283ebeb2cca409319e3460ed898d8754f62fb35cc83a65d` |
| Extracted filename | `data.csv` |
| Extracted path | `data/raw/data.csv` |
| Extracted size | 533230 bytes |
| Extracted SHA-256 | `3ef126de5cefff26eb11fbb4237f1a1401cb64b488e2f1d598c23cedeb4c45ae` |
| Licence | Creative Commons Attribution 4.0 International (CC BY 4.0) |
| Licence source | UCI dataset page, checked 2026-11-14. The page says the dataset is licensed under a Creative Commons Attribution 4.0 International (CC BY 4.0) licence and links to https://creativecommons.org/licenses/by/4.0/legalcode. |
| DOI | https://doi.org/10.24432/C5MC89 |

The project file is the `data.csv` extracted from that official zip. It was not edited after extraction.

UCI also publishes https://archive.ics.uci.edu/static/public/697/data.csv. On 2026-11-14 that direct file was 495,642 bytes, comma-separated, and not byte-identical to the zip extract. It had the same measured shape, 4,424 rows by 37 columns, and the same target counts: Graduate 2,209, Dropout 1,421, Enrolled 794. Its `Daytime/evening attendance` header does not contain a tab, and it spells `Marital Status` with a capital S. That comparison file was not kept, so this script does not re-download it.

## File format

- Encoding: UTF-8 with BOM.
- Delimiter: semicolon. This was detected from the header. It was not assumed.
- Measured shape: 4424 rows by 37 columns.
- Input features, treating `Target` as separate from the features: 36.

## Comparison with UCI metadata

UCI metadata is not a local measurement. The local measurement is the table above.

| Check | UCI metadata | Local measurement | Agreement |
| --- | --- | --- | --- |
| Instances | 4424 | 4424 | Yes |
| Input features | 36 | 36 | Yes |
| Target column present | Target | Yes | Yes |
| UCI missing-values flag | no | See the missing-value section | Compared below |

## Target

Pandas dtype: `str`.

| Class | Count | Percentage of rows |
| --- | --- | --- |
| Graduate | 2209 | 49.9322% |
| Dropout | 1421 | 32.1203% |
| Enrolled | 794 | 17.9476% |

Expected classes present: Dropout, Enrolled, Graduate.
Unexpected target labels: none.
Percentages are `count / number of rows × 100`, shown to four decimal places.

## Missing values

Total missing cells reported by pandas: 0.

| Column | Missing cells |
| --- | --- |
| Marital status | 0 |
| Application mode | 0 |
| Application order | 0 |
| Course | 0 |
| Daytime/evening attendance\t | 0 |
| Previous qualification | 0 |
| Previous qualification (grade) | 0 |
| Nacionality | 0 |
| Mother's qualification | 0 |
| Father's qualification | 0 |
| Mother's occupation | 0 |
| Father's occupation | 0 |
| Admission grade | 0 |
| Displaced | 0 |
| Educational special needs | 0 |
| Debtor | 0 |
| Tuition fees up to date | 0 |
| Gender | 0 |
| Scholarship holder | 0 |
| Age at enrollment | 0 |
| International | 0 |
| Curricular units 1st sem (credited) | 0 |
| Curricular units 1st sem (enrolled) | 0 |
| Curricular units 1st sem (evaluations) | 0 |
| Curricular units 1st sem (approved) | 0 |
| Curricular units 1st sem (grade) | 0 |
| Curricular units 1st sem (without evaluations) | 0 |
| Curricular units 2nd sem (credited) | 0 |
| Curricular units 2nd sem (enrolled) | 0 |
| Curricular units 2nd sem (evaluations) | 0 |
| Curricular units 2nd sem (approved) | 0 |
| Curricular units 2nd sem (grade) | 0 |
| Curricular units 2nd sem (without evaluations) | 0 |
| Unemployment rate | 0 |
| Inflation rate | 0 |
| GDP | 0 |
| Target | 0 |

Empty strings in object columns: 0.

## Duplicates

Duplicate column names: none.
Fully duplicate rows: 0.

## Column dictionary

Integer codes are not treated as continuous numbers. The interpretation follows the UCI variable type and description. Pandas dtypes are reported separately because they only describe storage.

| Column | Pandas dtype | Missing | Unique values | UCI type | Interpretation | Prediction-time note |
| --- | --- | --- | --- | --- | --- | --- |
| Marital status | `int64` | 0 | 6 | Integer | categorical code | Known at enrolment, from the UCI description. |
| Application mode | `int64` | 0 | 18 | Integer | categorical code | Known at enrolment, from the UCI description. |
| Application order | `int64` | 0 | 8 | Integer | ordinal integer (0 = first choice through 9 = last choice) | Known at enrolment, from the UCI description. |
| Course | `int64` | 0 | 17 | Integer | categorical code | Known at enrolment, from the UCI description. |
| Daytime/evening attendance\t | `int64` | 0 | 2 | Integer | binary category | Known at enrolment, from the UCI description. |
| Previous qualification | `int64` | 0 | 17 | Integer | categorical code | Known at enrolment, from the UCI description. |
| Previous qualification (grade) | `float64` | 0 | 101 | Continuous | continuous grade | Known at enrolment, from the UCI description. |
| Nacionality | `int64` | 0 | 21 | Integer | categorical code | Known at enrolment. UCI marks this as demographic (nationality). |
| Mother's qualification | `int64` | 0 | 29 | Integer | categorical code | Known at enrolment. UCI marks this as demographic (education level). |
| Father's qualification | `int64` | 0 | 34 | Integer | categorical code | Known at enrolment. UCI marks this as demographic (education level). |
| Mother's occupation | `int64` | 0 | 32 | Integer | categorical code | Known at enrolment. UCI marks this as demographic (occupation). |
| Father's occupation | `int64` | 0 | 46 | Integer | categorical code | Known at enrolment. UCI marks this as demographic (occupation). |
| Admission grade | `float64` | 0 | 620 | Continuous | continuous grade | Known at enrolment, from the UCI description. |
| Displaced | `int64` | 0 | 2 | Integer | binary category | Described as a yes/no student attribute. UCI does not give a measurement date. |
| Educational special needs | `int64` | 0 | 2 | Integer | binary category | Described as a yes/no student attribute. UCI does not give a measurement date. |
| Debtor | `int64` | 0 | 2 | Integer | binary category | Measurement date is not stated. Possible later administrative status. |
| Tuition fees up to date | `int64` | 0 | 2 | Integer | binary category | Measurement date is not stated. Possible later administrative status. |
| Gender | `int64` | 0 | 2 | Integer | binary category | Known at enrolment. UCI marks this as demographic (gender). |
| Scholarship holder | `int64` | 0 | 2 | Integer | binary category | Described as a yes/no student attribute. UCI does not give a measurement date. |
| Age at enrollment | `int64` | 0 | 46 | Integer | numerical count | Known at enrolment, from the UCI description. |
| International | `int64` | 0 | 2 | Integer | binary category | Described as a yes/no student attribute. UCI does not give a measurement date. |
| Curricular units 1st sem (credited) | `int64` | 0 | 21 | Integer | numerical count | End of the first semester, so available after the second semester. |
| Curricular units 1st sem (enrolled) | `int64` | 0 | 23 | Integer | numerical count | End of the first semester, so available after the second semester. |
| Curricular units 1st sem (evaluations) | `int64` | 0 | 35 | Integer | numerical count | End of the first semester, so available after the second semester. |
| Curricular units 1st sem (approved) | `int64` | 0 | 23 | Integer | numerical count | End of the first semester, so available after the second semester. |
| Curricular units 1st sem (grade) | `float64` | 0 | 805 | Integer | numerical grade average | End of the first semester, so available after the second semester. |
| Curricular units 1st sem (without evaluations) | `int64` | 0 | 11 | Integer | numerical count | End of the first semester, so available after the second semester. |
| Curricular units 2nd sem (credited) | `int64` | 0 | 19 | Integer | numerical count | End of the second semester, the approved prediction point. |
| Curricular units 2nd sem (enrolled) | `int64` | 0 | 22 | Integer | numerical count | End of the second semester, the approved prediction point. |
| Curricular units 2nd sem (evaluations) | `int64` | 0 | 30 | Integer | numerical count | End of the second semester, the approved prediction point. |
| Curricular units 2nd sem (approved) | `int64` | 0 | 20 | Integer | numerical count | End of the second semester, the approved prediction point. |
| Curricular units 2nd sem (grade) | `float64` | 0 | 786 | Integer | numerical grade average | End of the second semester, the approved prediction point. |
| Curricular units 2nd sem (without evaluations) | `int64` | 0 | 10 | Integer | numerical count | Column name says second semester. The UCI description text says first semester, which conflicts with the name. |
| Unemployment rate | `float64` | 0 | 10 | Continuous | continuous context variable | Reference period is not stated by UCI. |
| Inflation rate | `float64` | 0 | 9 | Continuous | continuous context variable | Reference period is not stated by UCI. |
| GDP | `float64` | 0 | 10 | Continuous | continuous context variable | Reference period is not stated by UCI. |
| Target | `str` | 0 | 3 | Categorical | target category | Eventual outcome at the end of the normal course duration. This is after the second semester and must not be an input. |

## Categorical and numerical candidates

Categorical candidates, including binary and ordinal codes:

- `Marital status`
- `Application mode`
- `Application order`
- `Course`
- `Daytime/evening attendance\t`
- `Previous qualification`
- `Nacionality`
- `Mother's qualification`
- `Father's qualification`
- `Mother's occupation`
- `Father's occupation`
- `Displaced`
- `Educational special needs`
- `Debtor`
- `Tuition fees up to date`
- `Gender`
- `Scholarship holder`
- `International`
- `Target`

Numerical candidates, including counts, grades, and context rates:

- `Previous qualification (grade)`
- `Admission grade`
- `Age at enrollment`
- `Curricular units 1st sem (credited)`
- `Curricular units 1st sem (enrolled)`
- `Curricular units 1st sem (evaluations)`
- `Curricular units 1st sem (approved)`
- `Curricular units 1st sem (grade)`
- `Curricular units 1st sem (without evaluations)`
- `Curricular units 2nd sem (credited)`
- `Curricular units 2nd sem (enrolled)`
- `Curricular units 2nd sem (evaluations)`
- `Curricular units 2nd sem (approved)`
- `Curricular units 2nd sem (grade)`
- `Curricular units 2nd sem (without evaluations)`
- `Unemployment rate`
- `Inflation rate`
- `GDP`

Constant columns: none.

## Values outside the captured UCI lists or ranges

Age at enrollment ranges from 17 to 70. UCI does not publish an allowed age range. Values below 16 or above 90 are flagged here only as a review heuristic.
Rows outside that heuristic: 0.

No observed value fell outside the captured UCI code lists or the stated grade and application-order ranges.

A code that is absent from the captured list is a documentation mismatch to review. It is not, by itself, a reason to delete the row.

## Prediction-time review

The approved prediction point is after the second semester. No feature was removed.

Features whose UCI descriptions place them at enrolment, or at the end of the first or second semester, are available by that prediction point. The target is the later outcome and is not an input.

Items that need a later decision:

- `Debtor` and `Tuition fees up to date` are yes/no fields. UCI does not say whether they were measured at enrolment, during the second semester, or later.
- `Unemployment rate`, `Inflation rate`, and `GDP` have no stated reference date. They may be enrolment-year context, or they may not line up with the prediction point.
- `Curricular units 2nd sem (without evaluations)` is named as a second-semester count, but the UCI description says "in the 1st semester". The column was kept. The description conflict is unresolved.
- The zip extract names `Daytime/evening attendance` with a trailing tab character inside the header. The UCI direct CSV does not. The tab is preserved because this audit does not edit the raw file. Later loading code must match the actual header.
- `Marital status` in the zip extract does not use the capital S shown in the UCI API name `Marital Status`.

No column other than `Target` is described by UCI as the final dropout, enrolled, or graduate outcome.

## What this audit did not do

No plots, cleaning, train/test split, or model training was done. Class counts above are counts of this file, not a model result.
