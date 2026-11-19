# Predicting Student Academic Outcomes Using Logistic Regression and Random Forest

**Draft note, not part of the report body.** This is a revised technical draft for Phase 6. It is not submission-ready. Phase 6 is not complete. Placeholders in square brackets require student input. The report-body word count excludes this note and the reference list.

Student number: s24156365

Audience: academic and technical readers familiar with introductory machine learning.

## 1. Report Introduction

This report tests whether two standard classifiers can separate Dropout, Enrolled, and Graduate after the second semester.

The only approved predictive question is:

How effectively can Logistic Regression and Random Forest classify students into Dropout, Enrolled, and Graduate categories using enrolment, demographic, socioeconomic, and first- and second-semester academic information?

Two further questions are descriptive only. They are not claimed to meet the brief's request for two or three research questions, and that count has not been confirmed with the module leader.

**EDA Question 1.** How is the distribution of Dropout, Enrolled, and Graduate outcomes represented in the dataset?

**EDA Question 2.** How do first- and second-semester academic progression measures, particularly grades and approved units, differ descriptively across the three outcome groups?

The predictive answer uses one untouched test set. The exploratory answers use the full file and do not establish causes.

### 1.1 Dataset identification

The file is *Predict Students' Dropout and Academic Success*, UCI dataset 697 (Realinho et al., 2021). The project copy is the zip downloaded on 2026-11-14 and the extracted `data.csv`, stored at `data/raw/`. It has 4,424 rows and 37 columns: 36 inputs plus `Target`, with 0 missing cells and 0 duplicate rows. The delimiter is a semicolon and the encoding is UTF-8 with a byte-order mark. A direct UCI CSV was not byte-identical, so it was not kept.

The UCI page, as quoted in the project on 2026-11-14, states that the dataset is licensed under Creative Commons Attribution 4.0 International (CC BY 4.0): https://creativecommons.org/licenses/by/4.0/legalcode. The project record says the rows come from one higher education institution. No second institution was evaluated.

`Target` contains Graduate 2,209 (49.9322%), Dropout 1,421 (32.1203%), and Enrolled 794 (17.9476%). These are file counts, not model scores. Integer fields store category codes and must not be read as continuous measurements. The meaning of a grade of 0 is not stated by UCI.

The table copies the audit dictionary, not a new definition, and lists every input name.

| Attributes | Stored type | Meaning from the audit |
| --- | --- | --- |
| Marital status; Application mode; Course; Previous qualification; Nacionality; Mother's qualification; Father's qualification; Mother's occupation; Father's occupation | int64 | Categorical codes known at enrolment. `Nacionality` is the stored spelling. `Marital status` differs from the UCI API name `Marital Status`. |
| Application order | int64 | Ordinal integer: 0 = first choice through 9 = last choice. Known at enrolment. |
| Daytime/evening attendance; Gender | int64 | Binary categories known at enrolment. The raw daytime/evening header has a trailing tab. Cleaning strips it in memory and does not drop the column. |
| Previous qualification (grade); Admission grade | float64 | Continuous grades known at enrolment. |
| Age at enrollment | int64 | Numerical count known at enrolment. The EDA label is "Age at enrolment (years)". |
| Displaced; Educational special needs; Scholarship holder; International | int64 | Yes/no attributes. UCI gives no measurement date. |
| Debtor; Tuition fees up to date | int64 | Yes/no attributes. Date unknown. Possible later administrative status. |
| Curricular units 1st sem (credited); Curricular units 1st sem (enrolled); Curricular units 1st sem (evaluations); Curricular units 1st sem (approved); Curricular units 1st sem (without evaluations) | int64 | Counts available at the end of semester 1. |
| Curricular units 1st sem (grade) | float64 | Grade average available at the end of semester 1. The UCI type cell says Integer. |
| Curricular units 2nd sem (credited); Curricular units 2nd sem (enrolled); Curricular units 2nd sem (evaluations); Curricular units 2nd sem (approved) | int64 | Counts available at the prediction point. |
| Curricular units 2nd sem (grade) | float64 | Grade average available at the prediction point. |
| Curricular units 2nd sem (without evaluations) | int64 | Count. The name says semester 2. The UCI description text says semester 1. |
| Unemployment rate; Inflation rate; GDP | float64 | Repeated context values. Reference period not stated. |
| Target | str | Dropout, Enrolled, or Graduate. Not an input. |

The remaining challenges are class imbalance, rare codes, undated fields, and the unresolved semester wording.

### 1.2 Supervised learning task identification

The task is multiclass classification, not regression, and there is no single positive class. `Target` is the label, in the order Dropout, Enrolled, Graduate, and it is not an input. The prediction point is the end of the second semester, when both semesters' academic fields are known. The comparison does not establish the same performance at another institution.

### 1.3 Declaration of Generative AI Use

I used ChatGPT and Cursor throughout this coursework to help me understand the assessment requirements, plan the project, and work through machine-learning concepts and technical decisions. They also supported me during Python development, debugging, evaluation, interpretation of results, and report preparation.

I mainly used ChatGPT to discuss project planning, research questions, and decisions about the dataset and experimental design, and to understand evaluation metrics, interpret results, and improve my technical explanations. I used Cursor mainly for Python implementation, including preprocessing, the Logistic Regression, Random Forest, and Dummy Classifier workflows, cross-validation, hyperparameter tuning, automated tests, visualisations, and project documentation.

I used some AI-generated code and written material with only minor changes, while other outputs were substantially adapted before I included them. I reviewed the material and checked relevant outputs against the original dataset, the UCI documentation, the saved evaluation results, the automated tests, and the approved project decisions. I also checked the report against the assessment brief and template. I recognise that not every generated line or statement was independently verified.

## 2. Exploratory Data Analysis

### 2.1 Question(s) identification

The two questions above describe the file. They do not identify a cause, and they were not used to choose a model.

### 2.2 Splitting the dataset

Exploration used all 4,424 rows and did not create the split. Section 3 uses a later 80/20 stratified split, not the template's 70/30 example. Full-file charts cannot estimate unseen performance.

### 2.3 Exploratory Data Analysis process and results

`notebooks/01_exploratory_data_analysis.ipynb` produced `outputs/eda_report.md` and seven figures. It did not train a model.

`figures/eda/figure_01_target_distribution.png` shows the class counts in section 1.1. Enrolled is the smallest class, so accuracy alone would favour Graduate.

Figure 1. Distribution of student academic outcomes

Age at enrolment runs from 17 to 70, with mean 23.265 and median 20. `figures/eda/figure_02_numerical_distributions.png` shows age, the two entry grades, both semester grade averages, and second-semester units approved. Semester grades have a visible mass at 0. A grade of 0 is not a missing cell: all 718 first-semester zeros, and all 870 second-semester zeros, have 0 approved units in that semester. UCI does not say whether 0 is a real average or a placeholder. Second-semester zero shares are 51.16%, 8.56%, and 3.40% for Dropout, Enrolled, and Graduate.

Figure 2. Distributions of selected numerical features

Means from the EDA report, in Dropout, Enrolled, Graduate order:

| Measure | Dropout | Enrolled | Graduate |
| --- | ---: | ---: | ---: |
| First-semester grade | 7.257 | 11.125 | 12.644 |
| Second-semester grade | 5.899 | 11.117 | 12.697 |
| First-semester units approved | 2.552 | 4.319 | 6.232 |
| Second-semester units approved | 1.940 | 4.058 | 6.177 |

`figures/eda/figure_03_semester_grades_by_target.png` shows higher grade boxes for Graduate than for Dropout, with Enrolled between them. Outliers were hidden on that chart. The zero shares use the full columns. `figures/eda/figure_04_academic_progression_by_target.png` shows that approved units separate the groups, while mean enrolled units stay between 5.780 and 6.670. Median ages are 23, 20, and 19. `figures/eda/figure_05_age_by_target.png` shows the higher age box for Dropout.

Figure 3. First- and second-semester grades by academic outcome

Figure 4. Academic progression measures by academic outcome

Figure 5. Student age distribution by academic outcome

`figures/eda/figure_06_selected_categoricals_by_target.png` shows different target mixes. Among 503 debtors, 62.03% are Dropout. Among 528 students whose tuition is not up to date, 86.55% are Dropout. Those fields have no measurement date, and the models did not use them. International students number 110, and students with special educational needs number 51. Percentages for those small groups are unstable. `figures/eda/figure_07_numerical_correlation_heatmap.png` shows semester-to-semester Pearson correlations of 0.945 for credited units, 0.943 for enrolled units, 0.904 for approved units, 0.837 for grades, and 0.779 for evaluations. Category codes are not in that heatmap.

Figure 6. Selected categorical features by academic outcome

Figure 7. Correlation matrix of selected numerical features

### 2.4 EDA conclusions

These patterns describe the file and do not show a cause. Debtor status, tuition status, the macroeconomic fields, and the conflicting semester sentence remain unresolved. The median of that column is 0 in every target class.

## 3. Experimental Design

### 3.1 Identification of your chosen supervised learning algorithm(s)

The comparison uses three estimators. No third competitive classifier was authorised.

The baseline is a most-frequent dummy. It predicts the largest training class for every row and was not tuned. Logistic Regression estimates a separate linear score for each class. Random Forest averages decision trees and does not scale its inputs.

### 3.2 Identification of appropriate evaluation techniques

Macro F1 is the primary metric and the selection metric because it weights each class equally. The other reported measures are balanced accuracy, macro precision, accuracy, a confusion matrix, and per-class precision, recall, and F1. Here, balanced accuracy equals macro recall, so macro recall is not a second finding. Settings were chosen by five-fold stratified cross-validation on the training rows only, shuffled with `random_state=42`. The 885-row holdout was not used to choose a parameter, a feature, or a preprocessor. In the cross-validation output, `test_score` means a training-fold validation score. It is not the holdout.

### 3.3 Data cleaning and pre-processing transformations

Nothing was imputed or deleted. No outlier filter and no derived feature were added. Grade zeros stayed numeric 0.

Six inputs were excluded: Debtor, Tuition fees up to date, Unemployment rate, Inflation rate, GDP, and Curricular units 2nd sem (without evaluations). The first five have no measurement or reference date. The last has a column name and a UCI sentence that refer to different semesters. Exclusion does not invent the missing date, and the models cannot use the debtor and tuition associations in section 2.

Four yes/no fields stay under an unverified timing assumption: Displaced, Educational special needs, Scholarship holder, and International. If any was recorded after the prediction point, the model could use information that would not have been available then.

Thirty inputs remain. Nominal codes are one-hot encoded inside each training fold. Application order stays ordered. Binary 0/1 fields are neither one-hot encoded nor scaled. Numerical columns are standardised only in the logistic pipeline. The forest pipeline does not scale them. `prepare_from_raw()` creates the split in memory and does not write `data/processed/`.

The split is 80/20, stratified on `Target`, with `random_state=42`. Training has 3,539 rows: Graduate 1,767, Dropout 1,137, and Enrolled 635. Testing has 885 rows: Graduate 442, Dropout 284, and Enrolled 159. The logistic scaler saw 3,539 rows. The run recorded `test_rows_used_for_tuning` as 0.

### 3.4 Limitations and Options

The frozen design excludes a third classifier, a single overall winner, resampling, a zero-grade sensitivity analysis, coefficients, and feature importance. A fairness audit was not run. The category chart in section 2 remains descriptive.

## 4. Predictive Modelling / Model Development

### 4.1 The predictive modelling process

Each competitive model was a pipeline, so each validation fold fit its own encoder and, for logistic regression, its own scaler. The searches scored macro F1, refitted the selected pipeline on the training rows, and used one job. Logistic Regression used `max_iter=2000` and `solver="lbfgs"`, without the penalty argument. Random Forest used `random_state=42`. Configurations were stored separately so alphabetical sorting could not reorder the forest. An exact tie would keep the earlier declared configuration. Both searches had a unique maximum.

The dummy was fit once on the 3,539 training rows and was not searched. Logistic Regression searched 8 configurations (40 cross-validation fits) and was refit once. The selected settings were `C=0.1` and `class_weight="balanced"`, declared order 4. Mean validation macro F1 was 0.688113, with fold standard deviation 0.019914. Random Forest searched 36 configurations (180 cross-validation fits) and was refit once. The selected settings were 200 trees, maximum depth 20, `min_samples_leaf=1`, and `class_weight="balanced"`, declared order 14. Mean validation macro F1 was 0.699806, with fold standard deviation 0.012205. These six-decimal figures are the display in `outputs/evaluation/phase5_evaluation_report.md`. The full values are in `outputs/evaluation/selected_parameters.json`.

The run completed 220 cross-validation fits, two training refits, and one dummy fit. The evaluation report records no warnings during the three fits. The pipelines are `outputs/models/dummy_most_frequent.joblib`, `outputs/models/logistic_regression.joblib`, and `outputs/models/random_forest.joblib`.

Panel A of `figures/model_comparison/figure_01_model_comparison_f1.png` shows the two validation means. No dummy cross-validation score was saved, so the dummy is not in that panel. The fold standard deviations describe each model's own five folds. They do not establish a significant difference.

Figure 8. Model comparison using cross-validation and holdout macro F1 scores

### 4.2 Evaluation results on "seen" data

The saved seen-data evidence is the training-fold cross-validation above. Separate scores of the final refitted models on the 3,539 training rows were not produced and are not reported. Those cross-validation means are not training-set performance. The unseen comparison is the 885-row holdout in section 5.

## 5. Evaluation and further modelling improvements

After the settings were fixed, each saved model predicted the same 885 test rows once. Those scores did not change a parameter, a feature, or a class weight. The six-decimal figures are the Phase 5 evaluation report display. `outputs/evaluation/test_metrics.json` stores the full values.

| Model | Macro F1 | Balanced accuracy | Macro precision | Accuracy |
| --- | ---: | ---: | ---: | ---: |
| Logistic Regression | 0.689290 | 0.702301 | 0.697566 | 0.727684 |
| Random Forest | 0.701691 | 0.701861 | 0.707986 | 0.754802 |
| Dummy, most frequent | 0.222055 | 0.333333 | 0.166478 | 0.499435 |

Panel B of `figures/model_comparison/figure_01_model_comparison_f1.png` shows these three holdout macro F1 values. Random Forest is higher on macro F1, macro precision, and accuracy. Logistic Regression is slightly higher on balanced accuracy. Neither difference makes one model an overall winner. The dummy predicts every test row as Graduate, so its accuracy is the test Graduate share, 442 of 885, not the full-file share of 49.9322%.

Per-class holdout F1, from the same report, is:

| Model | Dropout | Enrolled | Graduate |
| --- | ---: | ---: | ---: |
| Dummy | 0.000000 | 0.000000 | 0.666164 |
| Logistic Regression | 0.730769 | 0.504950 | 0.832151 |
| Random Forest | 0.754789 | 0.495677 | 0.854606 |

Panel C of the same figure shows these holdout F1 scores. Its bar labels are rounded to three decimal places. Graduate is strongest, Dropout is next, and Enrolled is weakest. Logistic Regression's Enrolled recall is 0.641509 and its Enrolled precision is 0.416327. Random Forest's are 0.540881 and 0.457447.

Rows of each confusion matrix are the actual class and columns are the prediction, in the order Dropout, Enrolled, Graduate. The counts are from `outputs/evaluation/confusion_matrices.csv`. There is no separate confusion-matrix image.

| Model | Actual | Predicted Dropout | Predicted Enrolled | Predicted Graduate |
| --- | --- | ---: | ---: | ---: |
| Logistic Regression | Dropout | 190 | 69 | 25 |
| Logistic Regression | Enrolled | 30 | 102 | 27 |
| Logistic Regression | Graduate | 16 | 74 | 352 |
| Random Forest | Dropout | 197 | 54 | 33 |
| Random Forest | Enrolled | 32 | 86 | 41 |
| Random Forest | Graduate | 9 | 48 | 385 |
| Dummy | Dropout | 0 | 0 | 284 |
| Dummy | Enrolled | 0 | 0 | 159 |
| Dummy | Graduate | 0 | 0 | 442 |

The matrices show Enrolled confused with the other classes. The dummy never predicts Dropout or Enrolled.

Enrolled is the smallest class and its EDA measures overlap with the other two classes. These observations are consistent with the weaker Enrolled-class results, but this analysis does not establish the cause. No threshold, feature-importance, or coefficient analysis was run. A zero-grade check or a second institution would be new work. Tuning again on these 885 rows would remove the unseen evaluation.

## 6. Conclusion

### 6.1 Summary of results

On the 30-column set and the 885-row holdout, both tuned models are more effective than the most-frequent dummy on macro F1: 0.701691 for Random Forest, 0.689290 for Logistic Regression, and 0.222055 for the dummy. Graduate is strongest and Enrolled is weakest. The differences do not make either an overall winner. Cross-validation selected the settings and is not this answer.

The EDA description does not establish a cause. The result is one institution, one split, and one prediction point. Four retained fields have unverified dates, and the excluded fields were left out because their dates or wording are unresolved. Grade zeros stayed zeros. No fairness or feature-impact analysis was run, and the study does not recommend an intervention.

### 6.2 Reflection on Individual Learning

This project showed me how a supervised classification study fits together, from reading the dataset and fixing the prediction point through to preprocessing, fitting, and interpretation. Working through the 36 inputs, and asking which could be known after the second semester, taught me to understand a feature before keeping it. Graduate is about half the file, so I learned not to rely on accuracy alone. Macro F1, balanced accuracy, precision, recall, and the confusion matrices were what showed the weaker class.

I excluded six columns whose timing or wording was unclear, including debtor and tuition status and the units-without-evaluations field whose name and UCI sentence disagree. That did not discover the missing dates. It only avoided treating an unknown date as known, and four other yes/no fields remain under an unverified timing assumption. Grade zeros line up with zero approved units, but the documentation does not define zero, so I kept them as zeros. One-hot encoding and scaling were fit only on training rows or on each training fold, which kept validation and test information out of those steps. Logistic Regression and Random Forest then shared one 80/20 stratified split, with five-fold stratified cross-validation on the training data only. Enrolled was easy to over-explain. It is the smallest class, and its grades and approved units sit between the other groups, but that overlap does not establish a cause.

The audit and exploratory analysis made those limits visible, and unresolved points were recorded instead of being filled in. The 30-column set was then frozen. Pipelines and a column transformer fitted the transformations without the test rows. Automated tests checked preprocessing, training, and evaluation, tuning stayed on the training folds, and the 885-row holdout was used once. I checked the confusion matrices against the saved files.

Both classifiers were well above the most-frequent dummy on that holdout. Macro F1 was 0.222055, 0.689290, and 0.701691 for the dummy, Logistic Regression, and Random Forest. Random Forest was slightly higher overall, and higher for Dropout (0.754789 against 0.730769) and Graduate (0.854606 against 0.832151). Logistic Regression was slightly higher for Enrolled (0.504950 against 0.495677). Neither model was equally strong on every class. Accuracies of 0.499435, 0.727684, and 0.754802 would have hidden the weak Enrolled result. The preferable model depends on the question being asked, and I do not treat the small gap as statistically significant.

In a later study I would examine the undated fields before using them again, and I would estimate coefficients or feature importance. A separate look at Enrolled, another model, or another reliable data source could be justified, but none of that was part of this frozen comparison. Clearer records would also make the work easier to rerun.

**Certification evidence:** No certifications are claimed as part of this coursework.

## 7. GitHub link

The recorded repository is https://github.com/juraidyousaf/CMP6202-AI-ML-Project.

The repository is publicly accessible. Its published `main` branch contains the five verified publication files and the saved project evidence. The Word report and technical ZIP have not yet been produced. Moodle submission instructions have not yet been checked.

## 8. References

Realinho, V., Vieira Martins, M., Machado, J. and Baptista, L. (2021) Predict Students' Dropout and Academic Success. [dataset] UCI Machine Learning Repository. Available at: https://doi.org/10.24432/C5MC89 [Accessed 14 November 2026].
