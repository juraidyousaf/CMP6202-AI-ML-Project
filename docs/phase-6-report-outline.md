# Phase 6 — Report outline and evidence map

**Status: planning only. Phase 6 is not complete. This file is not the report.**

The outline follows the content headings in `CMP6202 Individual Report Template 2026-27.docx` and the requirements read from `CMP6202 Assessment Brief  2026-27.docx`. It does not draft report paragraphs. Approved interpretations stay in `docs/phase-6-results-interpretation.md`. Scores stay in `outputs/evaluation/`.

## How this outline uses the template

The template table of contents nests several headings. The thirteen items below are those content headings in reading order, not thirteen top-level chapters.

| Outline section | Exact template heading |
| --- | --- |
| 1. Report introduction | 1. Report Introduction |
| 2. Dataset identification | 1.1 Dataset identification |
| 3. Supervised learning task | 1.2 Supervised learning task identification |
| 4. Declaration of generative AI use | 1.3 Declaration of Generative AI Use |
| 5. Exploratory data analysis | 2. Exploratory Data Analysis, with 2.1 Question(s) identification, 2.2 Splitting the dataset, 2.3 Exploratory Data Analysis process and results, and 2.4 EDA conclusions |
| 6. Experimental design | 3. Experimental Design, with 3.1 Identification of your chosen supervised learning algorithm(s), 3.2 Identification of appropriate evaluation techniques, 3.3 Data cleaning and pre-processing transformations, and 3.4 Limitations and Options |
| 7. Predictive modelling / model development | 4. Predictive Modelling / Model Development, with 4.1 The predictive modelling process and 4.2 Evaluation results on “seen” data |
| 8. Evaluation and further modelling improvements | 5. Evaluation and further modelling improvements |
| 9. Conclusion | 6.1 Summary of results |
| 10. Reflection on individual learning | 6.2 Reflection on Individual Learning |
| 11. Certification evidence in AI/ML | Guidance inside 6.2. The contents list has no separate certification heading |
| 12. Public GitHub repository link | 7. GitHub link |
| 13. References | 8. References |

When the report is drafted, use the template's numbering. Do not renumber the submitted report as thirteen top-level chapters unless the template file itself is revised.

## Word allocation

The brief sets a maximum of 3,000 words and a +10% margin. Nothing beyond that margin is marked. The brief does not state a −10% floor. The count includes headings, tables, citations, quotes, and lists in the main body. It excludes material before the main body, including a title page, contents, and the cover sheet, and it excludes references, bibliographies, and appendices.

The allocations below sum to 3,000. They are planning targets, not a count of written text. The attribute table is inside the body, so its words count. Keep that table compact.

| Section | Target words |
| ---: | ---: |
| 1. Report introduction | 220 |
| 2. Dataset identification | 650 |
| 3. Supervised learning task | 160 |
| 4. Declaration of generative AI use | 140 |
| 5. Exploratory data analysis | 380 |
| 6. Experimental design | 340 |
| 7. Predictive modelling / model development | 260 |
| 8. Evaluation and further modelling improvements | 400 |
| 9. Conclusion | 170 |
| 10. Reflection on individual learning | 180 |
| 11. Certification evidence | 50 |
| 12. Public GitHub repository link | 50 |
| 13. References | Excluded |
| **Main-body target** | **3,000** |

The ceiling under the brief's +10% margin is 3,300. Do not plan to use that margin for extra analysis.

Formatting recorded from the brief: 11-point font, 1.5 line spacing, and anonymous marking by student number only. The recorded student number is s24156365. The student name must not appear. The brief says to complete the appropriate cover sheet and append the work. The deadline fields printed on the brief are 4th December 2026 and 03:00PM. Referencing is BCU Harvard: https://www.bcu.ac.uk/library/services-and-support/referencing

Approved title, for the title line only: Predicting Student Academic Outcomes Using Logistic Regression and Random Forest.

Approved audience: academic and technical readers familiar with introductory machine learning.

## 1. Report introduction

**Purpose.** Name the audience, state the prediction problem, and present the approved questions without writing the later results in full.

**Subsections.**

- Audience and the technical level that follows from it.
- What the study predicts, and when.
- Predictive RQ1 beside the two descriptive EDA questions.
- What the later sections will and will not claim.

**Evidence.**

- Title and audience: `docs/phase-6-results-interpretation.md` section 11.A.
- RQ1 wording, unchanged: `docs/phase-5-experimental-design.md` section 1 and `docs/phase-6-results-interpretation.md` section 1.
- EDA Question 1 and EDA Question 2, same section. They are descriptive. They are not predictive modelling questions.
- Single-institution description recorded from UCI: `README.md`.

**Figures or tables.** None required in this section.

**Cautions.**

- Do not write for a university support team, a student reproducing the repository, or the marker as a second audience. The marker assesses the coursework. The named audience is the approved one.
- The report presentation is resolved: RQ1 is predictive, and the two EDA questions are descriptive. This does not guarantee that the descriptive questions satisfy the brief's request for two or three research questions. The earlier proposed RQ2 and RQ3 in `outputs/eda_report.md` section 7 remain unapproved.
- Do not name an overall winning model.

**Words.** 220.

## 2. Dataset identification

**Purpose.** Identify the file, its source and licence, and every attribute by name, storage type, and meaning.

**Subsections.**

- What the rows represent, and the source.
- Size, missingness, and the target classes.
- Licence.
- Attribute table for all 36 inputs and `Target`.
- Why this file was suitable, and which challenges remain.

**Evidence.**

- `README.md` dataset table, citation, and licence quotation.
- `outputs/dataset_audit.md`: download record, file format, UCI comparison, target table, missing-value section, duplicate section, and the column dictionary.
- Raw files: `data/raw/predict+students+dropout+and+academic+success.zip` and `data/raw/data.csv`.
- DOI recorded in the README: https://doi.org/10.24432/C5MC89.
- Licence recorded from the UCI page on 2026-11-14: CC BY 4.0, https://creativecommons.org/licenses/by/4.0/legalcode.

Measured facts to copy, not recalculate: 4,424 rows; 37 columns; 36 inputs plus `Target`; 0 missing cells; 0 duplicate rows. Target counts in the audit: Graduate 2,209 (49.9322%), Dropout 1,421 (32.1203%), Enrolled 794 (17.9476%). These are file counts, not model scores.

**Attribute table.** Reproduce the column dictionary in `outputs/dataset_audit.md`. For each row, keep the column name, pandas dtype, UCI type, interpretation, and prediction-time note. Do not rewrite a meaning that is not in that dictionary or in the UCI documentation the audit used. The 36 input names, in dictionary order, are:

- Marital status
- Application mode
- Application order
- Course
- Daytime/evening attendance
- Previous qualification
- Previous qualification (grade)
- Nacionality
- Mother's qualification
- Father's qualification
- Mother's occupation
- Father's occupation
- Admission grade
- Displaced
- Educational special needs
- Debtor
- Tuition fees up to date
- Gender
- Scholarship holder
- Age at enrollment
- International
- Curricular units 1st sem (credited)
- Curricular units 1st sem (enrolled)
- Curricular units 1st sem (evaluations)
- Curricular units 1st sem (approved)
- Curricular units 1st sem (grade)
- Curricular units 1st sem (without evaluations)
- Curricular units 2nd sem (credited)
- Curricular units 2nd sem (enrolled)
- Curricular units 2nd sem (evaluations)
- Curricular units 2nd sem (approved)
- Curricular units 2nd sem (grade)
- Curricular units 2nd sem (without evaluations)
- Unemployment rate
- Inflation rate
- GDP

`Target` is the remaining column. It is not an input.

**Figures or tables.** One attribute table. No new figure.

**Cautions.**

- The raw daytime/evening header still contains a trailing tab in the audit dictionary. `clean_column_names()` strips tabs in memory and does not drop the column. Say that. Do not say the column was removed.
- The zip extract spells `Marital status` without the capital S in the UCI API name `Marital Status`. Use the stored name and note the difference.
- `Curricular units 1st sem (grade)` is stored as `float64` while the audit's UCI type cell says Integer. Copy both cells. Do not invent a resolution.
- `Nacionality` is the stored spelling.
- The direct UCI CSV was not kept. Do not describe it as a second project file. The audit records that it was not byte-identical to the zip extract.
- Integer codes are not continuous measurements. The audit says so.

**Words.** 650, including the attribute table.

## 3. Supervised learning task

**Purpose.** Define the predictive problem and the target.

**Subsections.**

- Multiclass classification, not regression.
- `Target` as the ground-truth column, with Dropout, Enrolled, and Graduate.
- Prediction point after the second semester.
- Why the task matters for the named audience, without a deployment claim.

**Evidence.**

- `docs/phase-5-experimental-design.md` section 1.
- `src/preprocessing.py`: `TARGET_COLUMN` and `ALLOWED_LABELS`.
- `outputs/dataset_audit.md` target section and the `Target` dictionary row.
- Label order in `outputs/evaluation/test_metrics.json`: Dropout, Enrolled, Graduate.

**Figures or tables.** None required.

**Cautions.**

- There is no single positive class.
- `Target` must not be an input.
- UCI describes one institution. That limit is a discussion point, not a result from a second dataset.
- Do not adopt the template's 70/30 example. The approved split is stated in section 6.

**Words.** 160.

## 4. Declaration of generative AI use

**Purpose.** Meet the template's WHY, WHAT, WHICH, and HOW requirements with a declaration the student can verify.

**Subsections.**

- Which tools were used.
- Why they were used.
- What they produced.
- How the student checked that material.

**Evidence.**

- The template section "Declaration of Generative AI Use" requires those four points. It also offers the sentence "No Generative AI was used in the production of this work." That sentence would be false for this project.
- The brief's "Use of Artificial Intelligence" section says use is permitted and requires a clear declaration. The extracted brief text lists WHY, WHAT, and WHICH.
- `docs/Memory.md` section 14 records Cursor assistance. It does not yet contain a complete declaration covering ChatGPT.
- The project record is that ChatGPT and Cursor were used. The specific tasks, reasons, and checks are not written in the repository.

**Figures or tables.** None.

**Cautions.**

- Do not draft this declaration from the repository alone. The student must supply the actual reasons, tasks, and checks.
- Declared AI use is marked on its merit. The declaration does not replace verification of the results.
- Borrowed material, including generative AI, must be referenced. The brief says copied tutorials, scripts, or images are not allowed.

**Words.** 140.

## 5. Exploratory data analysis

**Purpose.** Answer the two approved descriptive questions from the saved exploration, then state what that exploration does not show.

**Subsections.**

- 2.1 Question(s) identification: EDA Question 1 and EDA Question 2 only.
- 2.2 Splitting the dataset: EDA used the full raw file. The split is a modelling control and is specified in section 6.
- 2.3 Exploratory Data Analysis process and results: the seven existing figures.
- 2.4 EDA conclusions: descriptive class imbalance and semester-progression differences. No causal claim. No model score.

**Evidence.**

- `outputs/eda_report.md` sections 3, 4, 5, 6, and 8.
- `notebooks/01_exploratory_data_analysis.ipynb`.
- `docs/phase-6-results-interpretation.md` sections 1 and 2, including the four progression means already copied there.
- Figures, all under `figures/eda/`:
  - `figure_01_target_distribution.png`
  - `figure_02_numerical_distributions.png`
  - `figure_03_semester_grades_by_target.png`
  - `figure_04_academic_progression_by_target.png`
  - `figure_05_age_by_target.png`
  - `figure_06_selected_categoricals_by_target.png`
  - `figure_07_numerical_correlation_heatmap.png`

**Figures or tables.** Use the seven EDA figures that support the two questions. Figure 1 supports EDA Question 1. Figures 3 and 4 support EDA Question 2. Figures 2, 5, 6, and 7 are context. Do not create another EDA figure for the report. A short table may repeat the class counts and the four means already in the interpretation note. Copy them. Do not recompute them.

**Cautions.**

- `outputs/eda_report.md` section 7 says training had not started. That sentence describes 2026-11-14. Do not copy it as the current state.
- Enrolled lying between Dropout and Graduate on the four means is a file description. It does not establish a cause. The approved sentence is in `docs/phase-6-results-interpretation.md` section 7.
- Figure 6 includes debtor and tuition status. Those fields were excluded from the model matrix because their measurement dates are unknown. Their descriptive association is not evidence that the models used them.
- Grade zeros stay numeric zeros. Figure 3 hid outliers for readability. The zero-grade shares in the EDA report come from the full columns.
- If generative AI assisted the EDA code, the declaration must say how the charts were checked. Do not invent that check.

**Words.** 380.

## 6. Experimental design

**Purpose.** Justify the algorithms, the metrics, the leakage controls, and the limits of the design.

**Subsections.**

- 3.1 Identification of your chosen supervised learning algorithm(s): most-frequent dummy, Logistic Regression, and Random Forest. Two different model families, plus a baseline. No third competitive classifier.
- 3.2 Identification of appropriate evaluation techniques: macro F1 as the primary and selection metric. Balanced accuracy, macro precision, accuracy, confusion matrix, and per-class precision, recall, and F1. Balanced accuracy equals macro recall here, so it is not a second finding.
- 3.3 Data cleaning and pre-processing transformations: what was checked, what was excluded, and what was fit only on training data.
- 3.4 Limitations and Options: limits already fixed by the frozen design, including analyses that were not run.

**Evidence.**

- `docs/phase-4-preprocessing-plan.md`.
- `docs/phase-5-experimental-design.md`.
- `src/preprocessing.py` for the 30 retained columns, the six exclusions, the timing assumption, the in-memory split, and the two preprocessors.
- `outputs/evaluation/run_metadata.json` for 885 test rows and `test_rows_used_for_tuning` 0.
- `outputs/evaluation/phase5_evaluation_report.md` for the split counts and the check that the logistic scaler saw 3,539 training rows.

**Split to report.** 80/20, stratified on `Target`, `random_state=42`, created in memory by `prepare_from_raw()`. Training 3,539 rows: Graduate 1,767, Dropout 1,137, Enrolled 635. Test 885 rows: Graduate 442, Dropout 284, Enrolled 159. Five-fold `StratifiedKFold`, shuffle, `random_state=42`, on the training portion only.

**Preprocessing points that must stay attached to their evidence.**

- Six excluded columns: `Debtor`, `Tuition fees up to date`, `Unemployment rate`, `Inflation rate`, `GDP`, and `Curricular units 2nd sem (without evaluations)`. The reasons are missing dates or the conflicting semester sentence. Exclusion does not invent a date.
- Four binaries retained under an unverified timing assumption: `Displaced`, `Educational special needs`, `Scholarship holder`, and `International`.
- No missing-value imputation, because the audit found 0 missing cells.
- No duplicate-row deletion, because the audit found 0 duplicate rows.
- No outlier filter and no derived feature.
- Semester grade zeros stay numeric 0.
- Nominal codes are one-hot encoded inside the training fold. `Application order` stays ordered. Binary 0/1 fields are not one-hot encoded and are not scaled.
- Numerical columns are standardised only in the logistic pipeline.

**Figures or tables.** A small retained-versus-excluded table is enough. Do not redraw the EDA charts here.

**Cautions.**

- The template's 70/30 split is an example. This project uses the approved 80/20 split.
- Cross-validation is training-only validation. It is not training-set performance and it is not the 885-row holdout.
- `cv_results_` uses the name `test_score` for training-fold validation. Do not call that the holdout.
- The generated evaluation report and `run_metadata.json` still say Phase 5 is not marked complete by those files. Approval is in `docs/Phases.md` and `docs/Memory.md`. Do not edit the generated files to change that flag.
- Feature importance, coefficient analysis, resampling, a zero-grade sensitivity analysis, and another classifier were excluded by the frozen design.

**Words.** 340.

## 7. Predictive modelling / model development

**Purpose.** Explain how the saved models were fit, which parameters were selected, and how seen-data evidence is reported.

**Subsections.**

- 4.1 The predictive modelling process: pipelines, grids, training-only search, dummy fit, and the final training refit.
- Selected parameters.
- 4.2 Evaluation results on “seen” data: what can be reported, and what was not produced.

**Evidence.**

- `src/model_training.py`, `src/model_evaluation.py`, and `src/run_phase5.py`.
- `outputs/models/dummy_most_frequent.joblib`, `outputs/models/logistic_regression.joblib`, and `outputs/models/random_forest.joblib`.
- `outputs/evaluation/selected_parameters.json`.
- `outputs/evaluation/logistic_regression_cv_results.csv` and `outputs/evaluation/random_forest_cv_results.csv`.
- `docs/phase-6-results-interpretation.md` sections 4 and 5.

**Process to describe.**

- Dummy: `DummyClassifier(strategy="most_frequent")`, fit once on the training portion, not tuned, and not part of the 220 cross-validation fits.
- Logistic Regression: 8 configurations, 40 cross-validation fits, then one training refit. Selected settings: `C=0.1`, `class_weight="balanced"`, declared order 4. Mean validation macro F1 `0.6881125650673585`.
- Random Forest: 36 configurations, 180 cross-validation fits, then one training refit. Selected settings: `n_estimators=200`, `max_depth=20`, `min_samples_leaf=1`, `class_weight="balanced"`, declared order 14. Mean validation macro F1 `0.6998064617503175`.
- Search settings recorded in the interpretation note: `scoring="f1_macro"`, `refit=True`, `error_score="raise"`, `n_jobs=1`. Logistic Regression used `max_iter=2000` and `solver="lbfgs"`. `penalty` was not passed.

**Seen-data reporting.** Report the five-fold training-only cross-validation as validation evidence. Report the 885-row holdout in section 8 as unseen test evidence. Do not call the cross-validation results training-set performance. Separate final-model training-set metrics were not produced and must not be calculated for the report. The template asks for evaluation on seen or training data. The honest report is that the saved seen-data evidence is the training-fold validation, not a separate score of the refitted models on the 3,539 training rows.

**Figures or tables.** Panel A of `figures/model_comparison/figure_01_model_comparison_f1.png` belongs with this validation evidence. The script is `src/plot_model_comparison.py`. No dummy cross-validation score was saved, so Panel A does not show one. A short parameter table may quote `selected_parameters.json`.

**Code.** The template asks for focused snippets. Point them at the pipeline and grid construction in `src/model_training.py`. Do not paste the whole module.

**Cautions.**

- The fold standard deviations describe each model's own five validation folds. They do not establish significance or a formal stability comparison.
- Both selected models use `class_weight="balanced"`. That was a training-fold choice. The test set was not used to choose it.
- Do not rerun `src/run_phase5.py`. A rerun would replace the approved outputs.

**Words.** 260.

## 8. Evaluation and further modelling improvements

**Purpose.** Compare the three saved holdout evaluations and state which improvements were not run.

**Subsections.**

- Holdout comparison on the same 885 rows.
- Per-class precision, recall, and F1.
- Confusion matrices.
- Strengths and weaknesses, without an overall winner.
- Further improvements that were considered and not performed.

**Evidence.**

- `outputs/evaluation/test_metrics.json` and `outputs/evaluation/test_metrics.csv`.
- `outputs/evaluation/per_class_metrics.csv`.
- `outputs/evaluation/confusion_matrices.csv`.
- `outputs/evaluation/predictions.csv`.
- `outputs/evaluation/phase5_evaluation_report.md`.
- `docs/phase-6-results-interpretation.md` sections 6, 7, 8, and 9.
- Panels B and C of `figures/model_comparison/figure_01_model_comparison_f1.png`.

**Figures or tables.**

- The comparison figure, Panels B and C. Panel B is holdout macro F1 for the dummy, Logistic Regression, and Random Forest. Panel C is holdout F1 for Dropout, Enrolled, and Graduate. Bar labels are rounded to three decimal places. The report text should use the saved full values or state the rounding.
- A holdout metric table from `test_metrics.csv`.
- A per-class table from `per_class_metrics.csv`.
- Confusion matrices as a table from `confusion_matrices.csv`, with both axes labelled Dropout, Enrolled, and Graduate. There is no separate confusion-matrix image. Do not create one in this planning step.

**Cautions.**

- The test set was used once after tuning. Do not use it to propose a new selected parameter.
- Random Forest has the higher holdout macro F1. Logistic Regression has the slightly higher holdout balanced accuracy and the slightly higher Enrolled F1. Those differences do not authorise a single winner.
- The dummy predicts every test row as Graduate. Its accuracy equals the Graduate share of the test split. The full-file Graduate share of 49.9322% is a different quantity.
- Accuracy must not be the only reported metric.
- The template's improvement steps mention feature importance, extra feature engineering, and further tuning. Those were not part of the frozen result. They can be named only as future work or limitations. Do not calculate them for the report.
- Enrolled is the weakest tuned class. The approved non-causal sentence is already in the interpretation note. Do not replace it with a cause.

**Words.** 400.

## 9. Conclusion

**Purpose.** Answer RQ1 from the holdout evidence and close the two EDA questions as descriptions.

**Subsections.**

- Direct answer to RQ1.
- What the class pattern adds, without a cause.
- What the named audience should not infer.
- No deployment recommendation.

**Evidence.**

- `docs/phase-6-results-interpretation.md` section 9.
- The holdout files in section 8.
- The EDA counts and means for the descriptive close.

**Figures or tables.** None new. Refer back to the comparison figure.

**Cautions.**

- The cross-validation means chose the settings. They are not the answer to RQ1.
- The result is a classification result for one institution's records.
- Do not recommend an intervention, a threshold, or a deployed system. No such evaluation exists.

**Words.** 170.

## 10. Reflection on individual learning

**Purpose.** Leave space for the student's own account of learning, technical difficulty, and how those difficulties were handled.

**Subsections.**

- What the student learned.
- Specific technical challenges.
- How those challenges were addressed.
- Limitations that followed from them.

**Evidence.** None in the repository can supply this section. `docs/Memory.md` records project decisions and blockers. It is not a personal reflection.

**Figures or tables.** None, unless the student later supplies a genuine artefact.

**Cautions.**

- Do not invent experiences, challenges, or solutions.
- The brief's reflection criterion treats discussion of technical challenges as part of the reflection. Certification evidence is a separate demand inside that criterion. Do not use a certificate to stand in for the reflection, and do not use the reflection to stand in for a certificate.
- The student must write this section.

**Words.** 180.

## 11. Certification evidence in AI/ML

**Purpose.** Record only certificates the student can verify as achieved during the project.

**Subsections.**

- Whether any certificate is claimed.
- For each claimed certificate: what it is, the completion evidence, and the date check against the project period.

**Evidence.** No `certificates/` directory is in the repository. No certificate file or verification link has been checked.

**Figures or tables.** Only a genuine screenshot, PDF, or public verification link supplied by the student. The template gives a Credly badge URL as an example of a link type. It does not record that this student has one.

**Cautions.**

- The reflection marking bands refer to evidence for one, two, or three certifications. That scale does not establish eligibility. Do not assume a certificate exists or that its date falls inside the project.
- If none can be verified, the report must say that none is claimed. Do not insert a placeholder image.

**Words.** 50.

## 12. Public GitHub repository link

**Purpose.** Give the marker the public repository that holds the code, data, and instructions.

**Subsections.**

- The URL.
- What a reader should find there.
- What has not been independently checked.

**Evidence.**

- Recorded URL: https://github.com/juraidyousaf/CMP6202-AI-ML-Project.
- `README.md` for the run order.
- Local code: `notebooks/01_exploratory_data_analysis.ipynb`, `src/data_audit.py`, `src/preprocessing.py`, `src/model_training.py`, `src/model_evaluation.py`, `src/run_phase5.py`, and `src/plot_model_comparison.py`.
- Raw data under `data/raw/`.

**Figures or tables.** None.

**Cautions.**

- The template says only the Word report is submitted to Moodle and that technical files reside at the GitHub link.
- The brief says the submission includes the report, dataset, and Python scripts in one zip file. Its deliverables line also says "GitHub repo or ZIP file".
- The approved preparation package is a separate Word report, a technical project ZIP, and this link inside the report. The final Moodle instructions have not been verified. Do not claim that either route has been accepted by the module.
- Public accessibility and completeness have not been independently verified. The checks still required are that the Python code is present, the README contains reproduction instructions, the dataset or its exact source link is present, and the relevant evidence is present.
- The local folder name `CMP6202-AI-ML` differs from the repository name.

**Words.** 50.

## 13. References

**Purpose.** List, in BCU Harvard form, only sources the report actually uses.

**Subsections.**

- Dataset citation.
- Licence.
- Any library, tutorial, or method source that the report cites.
- The brief and template, if the report cites them.

**Evidence already recorded.**

- Realinho, V., Vieira Martins, M., Machado, J., and Baptista, L. (2021) Predict Students' Dropout and Academic Success [Dataset]. UCI Machine Learning Repository. https://doi.org/10.24432/C5MC89.
- CC BY 4.0 legal code, as quoted in `README.md` and `outputs/dataset_audit.md`.
- BCU Harvard guidance URL printed in the brief and template.

**Figures or tables.** The reference list itself. It is excluded from the 3,000-word count.

**Cautions.**

- Do not invent a citation. The brief and template warn that fabricated references are academic misconduct.
- `references/` does not hold a formatted bibliography.
- BCU Harvard formatting has not been checked against a source opened for this outline.
- Scikit-learn 1.9.1 is a recorded library version in the evaluation report. It is not yet a formatted reference.
- The outline does not add tutorial citations. If a tutorial was used, the student must identify it before it is cited.

**Words.** Excluded.

## Requirements that cannot currently be demonstrated

- A separate training-set metric table for the final refitted models. The template asks for seen-data evaluation. The saved evidence is training-fold cross-validation plus one holdout. New training metrics must not be calculated without a separate approval.
- Feature-importance or coefficient analysis. The template's evaluation steps invite feature impact. The frozen design did not include it.
- A personal reflection. The repository does not contain one.
- Certification evidence. None is stored, and eligibility has not been checked.
- A complete generative-AI declaration. The tools are known. The student's WHY, WHAT, and HOW are not.
- A BCU Harvard bibliography checked against opened sources.
- Independent verification that the GitHub repository is public and complete.
- Confirmation that descriptive EDA questions count toward the brief's two-or-three research-question requirement.
- The final Moodle upload instructions.

## Information the student still needs to provide

- The generative-AI declaration: why ChatGPT and Cursor were used, what each produced, and how the output was checked.
- The reflection: learning, technical challenges, and how they were addressed.
- Any certification achieved during the project, with a date that can be checked, or a confirmation that none will be claimed.
- Any tutorial or secondary source that must be cited.
- A check of the final Moodle instructions before submission.
- Module-leader confirmation if the brief's research-question count remains unclear.

## Conflicts between the brief and the template

- **Submission route.** The brief asks for the report, dataset, and Python scripts in one zip file, and its deliverables line also allows a GitHub repository or a ZIP. The template says only the Word document goes to Moodle and that technical files must be at the GitHub link. The approved package prepares both a Word report and a technical ZIP, and puts the GitHub link in the report. Moodle has not been checked.
- **Contents numbering.** The template nests dataset identification, the supervised task, and the AI declaration under the introduction. It nests the reflection under the conclusion. Certification is described inside the reflection guidance. The GitHub link and references are the last two numbered contents entries. This outline keeps those headings, but it does not claim they are thirteen top-level template chapters.
- **Seen data.** The template asks for evaluation on seen or training data and shows code and visualisations for that discussion. The approved project evidence does not include separate final-model training-set metrics. Cross-validation must not be relabelled as that missing table.
- **Split example.** The template gives 70% training and 30% testing as an example. The approved split is 80/20.
- **Feature impact.** The template's evaluation steps ask how features affect predictions. The frozen experiment did not estimate feature importance or coefficients.
- **Research-question count.** The brief asks for two or three research questions. The approved materials contain one predictive question and two descriptive EDA questions. Whether that meets the brief is not guaranteed by this outline.
- **Generative-AI declaration.** The brief requires WHY, WHAT, and WHICH. The template requires WHY, WHAT, WHICH, and HOW the output was checked. The template also supplies the sentence for a project that used no generative AI. That sentence does not apply here, because ChatGPT and Cursor were used. The declaration still has to be written by the student.
- **Word-count rule.** Page 1 of the brief says 3,000 words excluding references. The word-count section is the rule this outline uses: a maximum of 3,000 words, a +10% tolerance only, up to 3,300 words, and no lower tolerance. Headings, tables, citations, quotes, and lists in the main body count. Material before the body, and references, bibliographies, and appendices, do not. Both official files are stored at the repository root and were inspected on 2026-11-17.

## Outline audit

Audited on 2026-11-17 against `CMP6202 Individual Report Template 2026-27.docx` and `CMP6202 Assessment Brief  2026-27.docx`. This audit checks the outline. It does not draft the report, and it does not mark Phase 6 complete.

### Checks

1. The thirteen content headings follow the template in reading order. Dataset identification, the supervised-learning task, and the AI declaration are 1.1, 1.2, and 1.3 under Report Introduction. EDA is section 2, with 2.1 Question(s) identification, 2.2 Splitting the dataset, 2.3 Exploratory Data Analysis process and results, and 2.4 EDA conclusions. Experimental design is section 3, with 3.1 through 3.4. Predictive modelling is section 4, with 4.1 and 4.2 Evaluation results on “seen” data. Evaluation is section 5 and has no numbered child in the contents list. The conclusion's summary is 6.1. Reflection is 6.2. The GitHub link is section 7. References are section 8.
2. Dataset identification, the supervised-learning task, and the AI declaration stay under the introduction. They are not separate top-level chapters.
3. Reflection is 6.2, inside the conclusion. Certification evidence is guidance inside that reflection. The contents list has no separate certification heading.
4. The public GitHub link is the template's section 7. References are the template's section 8. References stay outside the word count.
5. The section targets sum to 3,000 words: 220, 650, 160, 140, 380, 340, 260, 400, 170, 180, 50, and 50. The ceiling is 3,300. These are planning targets, not a count of written text.
6. Sections 1–3 and 5–9 point at saved project files. Sections 4, 10, 11, and 13 state where the repository has no student-owned text yet.
7. All seven files under `figures/eda/` are named in section 5. `figures/model_comparison/figure_01_model_comparison_f1.png` is mapped by panel: Panel A with training-only validation, and Panels B and C with the 885-row holdout.
8. Five-fold cross-validation is training-only validation. The 885-row holdout is the unseen test. Separate final-model training-set metrics were not produced and are not treated as available.
9. Reflection, certification, the AI declaration, a formatted bibliography, public GitHub verification, and separate training-set metrics are recorded as missing. None is described as finished.
10. The outline presents one predictive RQ1 and two descriptive EDA questions. It does not claim that this presentation satisfies the brief's request for two or three research questions.

### Verified and complete

- The template heading order and nesting in the mapping table.
- The word-count rule and the 3,000-word planning total, within the 3,300-word ceiling.
- Paths for the dataset audit, EDA report, seven EDA figures, frozen Phase 4 and Phase 5 plans, saved models, CV tables, holdout metrics, per-class metrics, confusion-matrix table, and the comparison figure.
- The distinction between training-only cross-validation and the 885-row holdout.
- The approved title, audience, and the decision not to name an overall winner.

### Outstanding evidence

- The attribute table has a source in `outputs/dataset_audit.md`, but it has not been written into a report.
- No separate final-model training-set metrics exist. They must not be calculated for this outline.
- No feature-importance or coefficient analysis exists.
- No confusion-matrix image exists. The saved source is `outputs/evaluation/confusion_matrices.csv`.
- `references/` contains no formatted BCU Harvard bibliography.
- Public access to https://github.com/juraidyousaf/CMP6202-AI-ML-Project has not been independently verified.
- The Word report and the technical ZIP do not exist. The final Moodle instructions have not been checked.

### User input required

- The generative-AI declaration: why ChatGPT and Cursor were used, what each produced, and how the output was checked.
- The reflection, written from the student's own learning and technical challenges.
- Certificate evidence that can be date-checked, or a confirmation that none will be claimed.
- Any tutorial or secondary source that must be cited.
- Module-leader confirmation if the brief's two-or-three research-question count remains unclear.

### Limitations that must be disclosed

- The records come from one institution. No second cohort was evaluated.
- Four retained binaries have no verified measurement date. Six other columns were excluded, including debtor and tuition status.
- Semester grade zeros stay numeric zeros. No sensitivity analysis was run.
- Enrolled is the weakest tuned class. The EDA overlap does not establish a cause.
- Cross-validation chose the settings. It is not the answer to RQ1, and it is not training-set performance.
- The holdout is one 885-row split. It was used once after tuning.
- Random Forest has the higher holdout macro F1. Logistic Regression has the slightly higher holdout balanced accuracy and Enrolled F1. That is not an overall winner.
- Feature impact, resampling, and a third classifier were not part of the frozen result.
- The template's 70/30 split is an example. The approved split is 80/20.
- The brief and template describe different submission routes. The approved package is a Word report, a technical ZIP, and the GitHub link. Moodle has not confirmed either route.

## What this outline does not do

- It does not draft the report.
- It does not mark Phase 6 complete.
- It does not change RQ1, the frozen Phase 5 design, or any saved score.
- It does not approve the earlier proposed RQ2 or RQ3.
- It does not name a winning model.
- It does not calculate a new metric or create a new figure.
- It does not invent a reflection, an AI declaration, a certificate, or a citation.
