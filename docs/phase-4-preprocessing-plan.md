# Phase 4 preprocessing and feature engineering plan

**Status: methodology approved and frozen on 2026-11-15. The student reviewed the implementation and approved Phase 4 as complete on 2026-11-15. The path is `src/preprocessing.py`. The raw file was not edited. Phase 5 — Model Development and Evaluation has not started.**

Module: CMP6202 Artificial Intelligence and Machine Learning  
Student ID: s24156365  
Date: 2026-11-15

Approved research question (RQ1):

How effectively can Logistic Regression and Random Forest classify students into Dropout, Enrolled, and Graduate categories using enrolment, demographic, socioeconomic, and first- and second-semester academic information?

RQ2 and RQ3 remain proposed and are not approved. This plan does not add research questions.

The source file is `data/raw/data.csv`, extracted from the official UCI zip and left unchanged. It has 4,424 rows and 37 columns. UCI reports 36 input features. The extra column is `Target`. Column names below are the names in that file. The daytime/evening header contains a trailing tab; `\t` in the table marks that character.

Evidence comes from the UCI variable descriptions used in `outputs/dataset_audit.md` and from measurements in `outputs/eda_report.md`. Where a date is not stated, this plan does not invent one.

---

## 1. Phase 4 objectives

Preprocessing has to turn the approved file into predictor matrices for two later models without changing the raw file and without using information that is not available at the approved prediction point.

For RQ1, that means:

- Keep `Target` as a three-class label and keep it out of every predictor matrix.
- Use enrolment, demographic, socioeconomic, and first- and second-semester academic fields whose timing is supported by the UCI description.
- Provisionally include `Displaced`, `Educational special needs`, `Scholarship holder`, and `International`. Their individual UCI descriptions do not give measurement dates. The student decided on 2026-11-15 to retain them under an explicit modelling assumption: the dataset narrative treats these attributes as available by the prediction point after the second semester. That availability has not been independently verified. The final report must state this assumption as a limitation. It is not a confirmed measurement date.
- Exclude six unresolved fields from the primary matrix: `Debtor`, `Tuition fees up to date`, `Unemployment rate`, `Inflation rate`, `GDP`, and `Curricular units 2nd sem (without evaluations)`. The student approved that exclusion on 2026-11-15. Exclusion does not supply a measurement date or settle the conflicting semester sentence.
- Encode category codes as categories. Do not treat those integers as continuous measurements.
- Leave recorded zeros in semester grades unchanged. The initial implementation does not include a zero-grade sensitivity analysis.
- Fit every transformation on training data only, including inside cross-validation.
- Prepare two pipelines that differ where the algorithms differ: scaling for Logistic Regression, and no scaling for Random Forest.

No processed dataset, split, encoding, scaling, or model is created by this document.

## 2. Feature eligibility and prediction-time availability

The prediction point is after the second semester. A feature is **retain** when the UCI description places it at enrolment or at the end of the first or second semester. The student approved that retain list on 2026-11-15. Four binary features are also **retain**, by the earlier provisional decision. Their descriptions do not date them, so that retention is a modelling assumption, not a verified time. Six features are **exclude**. They stay out of the primary matrix because a date is missing or the semester wording conflicts. Exclusion does not resolve those uncertainties.

The stored daytime/evening name is `Daytime/evening attendance\t`. Later code should strip that tab in memory and then check that the cleaned names are unique. The raw file must not be rewritten.

| Exact column name | Meaning from UCI | Type | Eligibility | Reason | Timing or leakage concern |
| --- | --- | --- | --- | --- | --- |
| `Marital status` | Six marital-status codes, from single through legally separated. | Nominal code | Retain | Enrolment demographic attribute in the UCI description. | None stated. Rare codes 3, 5, and 6 have 4, 25, and 6 students. |
| `Application mode` | Coded application route, such as general contingent, transfer, or international student. | Nominal code | Retain | Known at application, before enrolment is complete. | None stated. 18 observed codes. |
| `Application order` | Choice rank. UCI says 0 is first choice and 9 is last choice. | Ordinal integer | Retain | Known at application. | The order is documented. Equal spacing between ranks is an assumption, not a UCI statement. |
| `Course` | Coded undergraduate course. | Nominal code | Retain | Known at enrolment. | 17 codes. No date concern. |
| `Daytime/evening attendance\t` | 1 = daytime, 0 = evening. | Binary | Retain | Attendance regime at enrolment. | The tab is a file-header defect, not a timing issue. Strip it in memory only. |
| `Previous qualification` | Coded highest previous qualification. | Nominal code | Retain | Known before the course starts. | 17 codes. |
| `Previous qualification (grade)` | Grade of the previous qualification, described as between 0 and 200. | Continuous grade | Retain | Known before the course starts. | None stated. |
| `Nacionality` | Country code. Spelling is UCI's. UCI marks it as nationality. | Nominal code | Retain | Demographic attribute known at enrolment. | 21 observed codes. The spelling must be kept when matching the file. |
| `Mother's qualification` | Coded education level. UCI marks it as demographic. | Nominal code | Retain | Family background known at enrolment. | 29 codes. Some levels are rare. |
| `Father's qualification` | Coded education level. UCI marks it as demographic. | Nominal code | Retain | Family background known at enrolment. | 34 codes. Some levels are rare. |
| `Mother's occupation` | Coded occupation. UCI marks it as demographic. | Nominal code | Retain | Family background known at enrolment. | 32 codes. High cardinality. |
| `Father's occupation` | Coded occupation. UCI marks it as demographic. | Nominal code | Retain | Family background known at enrolment. | 46 codes. Highest cardinality in the file. |
| `Admission grade` | Admission grade, described as between 0 and 200. | Continuous grade | Retain | Fixed at admission. | None stated. |
| `Displaced` | 1 = yes, 0 = no. | Binary | Retain | Provisional student decision, 2026-11-15. The individual description does not specify a measurement date. Retention uses the dataset narrative and the assumption that the attribute is available after the second semester. | Availability by the prediction point has not been independently verified. This is an unverified timing assumption, not a confirmed date. The final report must state it as a limitation. |
| `Educational special needs` | 1 = yes, 0 = no. | Binary | Retain | Same provisional decision as `Displaced`. The individual description does not specify a measurement date. | Same unverified timing assumption. The final report must state it as a limitation. Only 51 students have code 1. |
| `Debtor` | 1 = yes, 0 = no. | Binary | Exclude | Excluded from the primary matrix by the approved methodology, 2026-11-15. UCI does not state when debtor status was measured. | Possible later administrative status. EDA shows a large association with `Target`. That association does not date the field. Exclusion does not invent a date. |
| `Tuition fees up to date` | 1 = yes, 0 = no. | Binary | Exclude | Excluded from the primary matrix by the approved methodology, 2026-11-15. UCI does not state when fee status was measured. | Same timing gap as `Debtor`. Among 528 students with code 0, 86.55% are in Dropout. The association is not a measurement date. Exclusion does not invent a date. |
| `Gender` | 1 = male, 0 = female. | Binary | Retain | UCI marks it as demographic and the description is a fixed attribute. | None stated. Use the UCI labels. Do not infer a different coding. |
| `Scholarship holder` | 1 = yes, 0 = no. | Binary | Retain | Provisional student decision, 2026-11-15. The individual description does not specify a measurement date. Retention uses the dataset narrative and the assumption that the attribute is available after the second semester. | Availability by the prediction point has not been independently verified. This is an unverified timing assumption, not a confirmed date. The final report must state it as a limitation. |
| `Age at enrollment` | Age of the student at enrolment. | Numerical count | Retain | The description says the age is at enrolment. | None stated. Observed range is 17 to 70 years. |
| `International` | 1 = yes, 0 = no. | Binary | Retain | Same provisional decision as `Displaced`. The individual description does not specify a measurement date. | Same unverified timing assumption. The final report must state it as a limitation. 110 students have code 1. |
| `Curricular units 1st sem (credited)` | Number of curricular units credited in the first semester. | Numerical count | Retain | End of the first semester, so available after the second semester. | None beyond the usual semester timing. |
| `Curricular units 1st sem (enrolled)` | Number of curricular units enrolled in the first semester. | Numerical count | Retain | End of the first semester. | None stated. |
| `Curricular units 1st sem (evaluations)` | Number of evaluations of curricular units in the first semester. | Numerical count | Retain | End of the first semester. | None stated. |
| `Curricular units 1st sem (approved)` | Number of curricular units approved in the first semester. | Numerical count | Retain | End of the first semester. | Strongly aligned with the first-semester grade. Not the target. |
| `Curricular units 1st sem (grade)` | Grade average in the first semester, described as between 0 and 20. | Numerical grade | Retain | End of the first semester. | A stored 0 is ambiguous. See section 4. Do not drop the column because of that ambiguity. |
| `Curricular units 1st sem (without evaluations)` | Number of curricular units without evaluations in the first semester. | Numerical count | Retain | The name and the UCI sentence both say the first semester. | Median is 0. |
| `Curricular units 2nd sem (credited)` | Number of curricular units credited in the second semester. | Numerical count | Retain | End of the second semester, the approved prediction point. | Correlates 0.945 with the first-semester credited count. |
| `Curricular units 2nd sem (enrolled)` | Number of curricular units enrolled in the second semester. | Numerical count | Retain | End of the second semester. | Correlates 0.943 with the first-semester enrolled count. |
| `Curricular units 2nd sem (evaluations)` | Number of evaluations in the second semester. | Numerical count | Retain | End of the second semester. | Correlates 0.779 with the first-semester evaluation count. |
| `Curricular units 2nd sem (approved)` | Number of curricular units approved in the second semester. | Numerical count | Retain | End of the second semester. | Correlates 0.904 with the first-semester approved count. |
| `Curricular units 2nd sem (grade)` | Grade average in the second semester, described as between 0 and 20. | Numerical grade | Retain | End of the second semester. | A stored 0 is ambiguous. See section 4. Correlates 0.837 with the first-semester grade. |
| `Curricular units 2nd sem (without evaluations)` | The column name says the count is for the second semester. The UCI sentence says "in the 1st semester". | Numerical count | Exclude | Excluded from the primary matrix by the approved methodology, 2026-11-15. The name and the description conflict. | The exclusion does not decide which semester it belongs to. Median is 0 in every target class. |
| `Unemployment rate` | Unemployment rate (%). | Continuous context | Exclude | Excluded from the primary matrix by the approved methodology, 2026-11-15. UCI gives the unit and not the reference period. | The date may be the enrolment year, or it may not match the prediction point. Class means are close. That does not identify the year. Exclusion does not invent a year. |
| `Inflation rate` | Inflation rate (%). | Continuous context | Exclude | Excluded from the primary matrix by the approved methodology, 2026-11-15. Same gap as unemployment. | Observed values run from -0.80 to 3.70. No reference year is in the file. Exclusion does not invent a year. |
| `GDP` | GDP. UCI does not state the unit or the year. | Continuous context | Exclude | Excluded from the primary matrix by the approved methodology, 2026-11-15. Same gap as the other macroeconomic fields. | Observed values run from -4.06 to 3.51. The unit is not stated here and is not invented. |

`Target` is not one of the 36 inputs. It is handled in section 3.

## 3. Target handling

`Target` is the classification label. UCI defines it as the three-category outcome at the end of the normal course duration: Dropout, Enrolled, and Graduate. That outcome is after the prediction point, so the column is a label and not a predictor.

Rules for later implementation:

- Select `Target` into `y` only.
- Do not pass it to a scaler, encoder, or model feature list.
- Do not build a feature from it, including "is graduate" or any other recode of the label.
- Keep all three classes. Do not collapse Enrolled into another class. The approved question asks for three categories.
- The observed labels are exactly those three strings. Any other label in a later load is an error, not a fourth class to encode.

## 4. Missing values and zero-grade ambiguity

The audit found 0 missing cells and 0 empty strings in `data/raw/data.csv`. The primary pipeline therefore does not need an imputer for empty cells. A later check should still fail if a reload contains missing values, rather than silently filling them.

Semester grades of 0 must not automatically be treated as missing.

- The cells are filled. They are not null.
- UCI describes the grade as an average between 0 and 20. It does not say that 0 means "unknown".
- In this file, all 718 first-semester grades of 0 also have 0 approved units, and all 870 second-semester grades of 0 also have 0 approved units.
- That alignment is consistent with "no graded units" and also with a recorded average of 0. The file does not say which reading is correct.

**Primary treatment, student decision 2026-11-15:** preserve every recorded semester grade of 0 as the number 0. Do not replace zero with a missing value. Do not impute it. Do not remove a row because the grade is 0. This decision does not resolve what 0 means. The alignment with zero approved units is still consistent both with "no graded units" and with a recorded average of 0. That semantic ambiguity remains a limitation for the final report.

The initial implementation does not include a zero-grade sensitivity analysis. No alternative imputation or recoding of these zeros is part of the first pipeline.

## 5. Categorical feature encoding

Category codes are labels. The numeric gaps in course and occupation codes are not distances.

| Group | Columns | Approved encoding |
| --- | --- | --- |
| Binary | Daytime/evening attendance, Displaced, Educational special needs, Gender, Scholarship holder, International. `Debtor` and `Tuition fees up to date` are excluded. | Keep the documented 0/1 values. Do not one-hot a binary column into two columns. Do not standardise 0/1 codes. |
| Ordinal | `Application order` only. | Approved encoding: keep the documented integer order, 0 through 9. Equal spacing between choice ranks is an assumption. A one-hot alternative is not part of the frozen pipeline. |
| Nominal | Marital status, Application mode, Course, Previous qualification, Nacionality, both parents' qualification, both parents' occupation. | One-hot encoding, fitted on the training data. `handle_unknown="ignore"` so a code that appears only in a later fold becomes zeros rather than an error. Do not ordinal-encode these codes. |

High-cardinality fields are Course (17), Application mode (18), Previous qualification (17), Nacionality (21), Mother's qualification (29), Father's qualification (34), Mother's occupation (32), and Father's occupation (46). One-hot is still appropriate at this size. The resulting width is manageable for both planned models.

Rare categories are not merged in the frozen pipeline. Marital-status codes 3, 5, and 6, and the small counts for special educational needs and international status, make some percentages unstable. The limitation should be stated in the report.

Unknown categories belong to transformation, not to the raw file. The encoder sees training levels only. A test or validation level that was absent from that fit is ignored, not assigned a new coefficient from the test row.

## 6. Numerical preprocessing

Continuous grades in the frozen primary matrix:

- `Previous qualification (grade)`
- `Admission grade`
- `Curricular units 1st sem (grade)`
- `Curricular units 2nd sem (grade)`

`Unemployment rate`, `Inflation rate`, and `GDP` are excluded. They are not scaled because they are not in the matrix.

Count features:

- `Age at enrollment`
- The first-semester curricular counts other than the grade
- The second-semester curricular counts other than the grade, except `Curricular units 2nd sem (without evaluations)`, which is excluded

Logistic Regression uses a linear combination of the columns. Age in years, grades on a 0–20 scale, and grades on a 0–200 scale would otherwise dominate or shrink the coefficients for reasons of unit size. Standardise the numerical columns inside the logistic pipeline. Fit the scaler on training rows only.

Random Forest splits on thresholds. Those thresholds are invariant to a linear rescaling of one column, so the forest pipeline should not scale numerical columns. Scaling would not make the forest result wrong, but it is unnecessary and would make the two pipelines look more different than the algorithms require.

Do not standardise one-hot columns or 0/1 codes. A scaled gender code would no longer mean female versus male in the logistic coefficient.

## 7. Feature engineering

No derived feature is included in the frozen primary pipeline. The student approved that choice on 2026-11-15.

Matching semester columns are already strongly correlated: credited 0.945, enrolled 0.943, approved 0.904, grade 0.837, and evaluations 0.779. A ratio or a difference is a rearrangement of columns the model can already see. For Logistic Regression it adds collinearity. For Random Forest it duplicates a split the tree can make from the original pair.

Candidates considered and not recommended for the first implementation:

| Candidate | Calculation | Purpose | Leakage | Necessary? |
| --- | --- | --- | --- | --- |
| Semester approval rate | Approved units divided by enrolled units, only where enrolled units are greater than 0 | Express progress relative to load | Uses counts from that semester. No target is involved. Undefined when enrolled units are 0. | No. Both counts remain in the matrix. |
| Grade change | Second-semester grade minus first-semester grade | Show direction of change | Uses the two grade columns, both available by the prediction point if the zeros stay as recorded. | No. Both grades remain in the matrix. The meaning of 0 makes the difference ambiguous. |
| Any function of `Target` | — | — | Target leakage. | Forbidden. |

The frozen pipeline does not add a derived feature. Any later change would be a new decision, not part of this approval. Nothing is written back to `data/raw/`.

## 8. Train/test split and reproducibility

Approved configuration, **frozen on 2026-11-15 and implemented in `src/preprocessing.py`**. The split is created in memory and is not saved as a processed file:

- 80% training, 20% testing
- Stratified on `Target`
- `random_state=42`
- 5-fold `StratifiedKFold` on the training portion only, with the same fixed seed

Why this configuration fits this file:

- 4,424 rows can support a 20% holdout. The implemented split has 885 test rows, including 159 Enrolled students. Those counts were measured from `prepare_from_raw()` on 2026-11-15. They are split counts, not model scores.
- Stratification keeps Dropout, Enrolled, and Graduate in both partitions. A non-stratified split could move the smallest class by chance.
- Five folds on the training portion leave a validation slice near one fifth of the training rows, which is still large enough to see all three classes.
- Seed 42 makes the split repeatable. It is not a property of the students. The student has now fixed this seed. A different seed would be a new decision.

UCI says the creators used an 80/20 split. The student approved the same ratio, with stratification and seed 42, on 2026-11-15. The UCI example is not itself the approval. `src/preprocessing.py` creates that split in memory. It does not write a processed dataset.

The split must be made before any encoder or scaler is fitted. If the scaler is fitted on all 4,424 rows, the test rows affect the training means and standard deviations. The same rule applies to which category levels exist.

## 9. Leakage prevention

| Risk | Control |
| --- | --- |
| Target leakage | `Target` is `y` only. No encoder sees it. |
| Temporal leakage | The six excluded columns stay out of the primary matrix: `Debtor`, `Tuition fees up to date`, `Unemployment rate`, `Inflation rate`, `GDP`, and `Curricular units 2nd sem (without evaluations)`. Second-semester academic fields whose UCI descriptions date them at the end of that semester are allowed, because that is the prediction point. `Displaced`, `Educational special needs`, `Scholarship holder`, and `International` are included only under the provisional timing assumption in section 2. Their availability after the second semester has not been verified. The final report must say so. |
| Preprocessing leakage | `Pipeline` and `ColumnTransformer` fit on training rows and only transform the test rows. |
| Test-set contamination | The test partition is unused for fitting, feature decisions, and hyperparameter choice. |
| Cross-validation leakage | The whole pipeline is cloned inside each training fold. The fold's validation rows are not used to fit the scaler or the one-hot levels. |

`sklearn.pipeline.Pipeline` and `sklearn.compose.ColumnTransformer` are the approved objects. A manual sequence of `fit` on the full frame is not acceptable.

Header cleaning, the tab strip, happens before the split and does not use the target or any aggregate. It is safe to do on the loaded table. It must not be written back to `data/raw/data.csv`.

## 10. Model-specific preprocessing

The pipelines are implemented in `src/preprocessing.py` and were approved with Phase 4 on 2026-11-15. They contain no classifier. The primary column set includes the four provisionally retained binaries under the timing assumption in section 2, and it excludes the six columns named in section 9.

**Logistic Regression**

1. Column set: the approved retain list only.
2. Binaries stay 0/1.
3. `Application order` keeps its documented order.
4. Nominal codes go through `OneHotEncoder(handle_unknown="ignore")`.
5. Numerical grades and counts go through `StandardScaler`.
6. The estimator is the last pipeline step. It is not fitted in Phase 4 planning.

**Random Forest**

1. The same approved column set and the same categorical encoding, so the comparison is not a hidden change of features.
2. No `StandardScaler`.
3. The forest is the last step. It is not fitted in this plan.

A shared preprocessor class is acceptable only if the logistic pipeline adds a scaler and the forest pipeline does not. Fitting one preprocessor on the full training set and then reusing it across both models is fine for the final training pass. Inside cross-validation, each fold must refit the pipeline it is scoring.

## 11. Baseline and evaluation strategy

The approved comparison remains Logistic Regression and Random Forest. Neither has been trained.

Approved baseline, not trained: `DummyClassifier(strategy="most_frequent")`. It predicts the largest training class for every row. In this file that class is Graduate, 2,209 of 4,424 students, which is 49.9322%. A most-frequent rule therefore has an accuracy reference of about 49.93% if the test mix matches the full file. The actual baseline accuracy must be computed on the future test fold, not copied from this percentage.

Approved metrics:

- Macro F1, the primary comparison metric under class imbalance
- Balanced accuracy
- Macro precision
- Accuracy, reported with the majority-class reference and not used alone
- Confusion matrix with the class names Dropout, Enrolled, and Graduate
- Per-class precision, recall, and F1

Balanced accuracy and macro recall are the same quantity in this three-class task: each is the unweighted mean of the three per-class recalls. Report one of them as the recall summary and do not describe the other as a separate finding.

No score in this section is a model result.

## 12. Approved methodology

The methodology below is approved and frozen on 2026-11-15. A later change needs a new student decision. The student approved the implemented path, and Phase 4, on 2026-11-15. That approval does not change the rules below.

**Evidence already measured**

- 4,424 rows, 37 columns, 0 missing cells, three target classes with counts 2,209, 1,421, and 794.
- Semester grade 0 coincides with zero approved units in that semester.
- Matching semester features are strongly correlated, at the values cited in section 7.
- The individual UCI descriptions do not date `Displaced`, `Educational special needs`, `Scholarship holder`, `International`, `Debtor`, `Tuition fees up to date`, `Unemployment rate`, `Inflation rate`, or `GDP`.
- The column name and the UCI sentence for `Curricular units 2nd sem (without evaluations)` conflict.

**Earlier decisions, still in force**

These are modelling choices. They do not confirm a measurement date or a meaning for a grade of 0.

- `Displaced`, `Educational special needs`, `Scholarship holder`, and `International` are provisionally retained. The assumption is that the dataset narrative makes them available by the prediction point after the second semester. Their individual descriptions do not state that date, and the date has not been independently verified. The final report must record the assumption as a limitation.
- Recorded semester grade zeros stay numeric zero. They are not replaced, imputed, or used as a reason to drop a row.
- A zero-grade sensitivity analysis is excluded from the initial implementation. The ambiguity of those zeros remains documented.

**Six methodology decisions approved on 2026-11-15**

1. **Feature set.** Retain every feature whose UCI description dates it at or before the end of the second semester, plus the four provisional binaries. Exclude `Debtor`, `Tuition fees up to date`, `Unemployment rate`, `Inflation rate`, `GDP`, and `Curricular units 2nd sem (without evaluations)` from the primary matrix.
2. **Encoding.** Binary columns stay 0/1 and are not scaled. Nominal columns are one-hot encoded, with unknown levels ignored. Rare levels are not merged. `Application order` stays an ordered integer. Equal spacing between ranks remains an assumption.
3. **Feature engineering.** The primary pipeline has no derived features.
4. **Split and cross-validation.** Use 80% training and 20% testing, stratified on `Target`, with `random_state=42`. Use 5-fold `StratifiedKFold` on the training portion only. `src/preprocessing.py` creates this split in memory. It is not saved as a processed file.
5. **Baseline and metrics.** Use `DummyClassifier(strategy="most_frequent")`. Report macro F1, balanced accuracy, macro precision, accuracy, a confusion matrix, and per-class precision, recall, and F1. Balanced accuracy and macro recall are one recall summary.
6. **Pipelines.** Logistic Regression standardises numerical grades and counts. Random Forest uses the same columns and the same encoding and does not scale. Both use `Pipeline` and `ColumnTransformer`, fitted on training data only.

**Not assumed**

- A verified measurement date for the four provisionally retained binaries.
- A measurement date for debtor status, tuition status, unemployment, inflation, or GDP.
- Which semester `Curricular units 2nd sem (without evaluations)` describes.
- That a grade of 0 is missing.
- Any model score.

## 13. Phase 4 exit criteria

The methodology is approved and frozen. These rules bind the implementation:

- `Displaced`, `Educational special needs`, `Scholarship holder`, and `International` are provisionally retained. The timing assumption is explicit and unverified, and the final report must acknowledge it.
- Recorded semester grades of 0 stay numeric zero. The initial implementation does not impute them, replace them, drop rows because of them, or run a zero-grade sensitivity analysis.
- The six excluded columns stay out of the primary matrix.
- Encoding, the absence of derived features, the 80/20 stratified split with seed 42, 5-fold stratified cross-validation on the training data, the most-frequent dummy baseline, the metric list, and scaling for Logistic Regression only are fixed.

The student approved Phase 4 as complete on 2026-11-15. The leakage-safe path is `src/preprocessing.py`. It can be refit from the training split alone, and the raw file is unchanged. No classifier has been trained. Phase 5 — Model Development and Evaluation has not started.
