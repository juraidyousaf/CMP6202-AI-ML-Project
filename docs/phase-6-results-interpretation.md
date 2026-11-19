# Phase 6 — Results Interpretation and Coursework Report Preparation

**Status: started on 2026-11-15. Not complete.** The interpretation in sections 2–9 was approved on 2026-11-16. A documentation update on 2026-11-17 records the approved report title, audience, seen-data reporting rule, comparison-figure approval, and submission package. The approved comparison figure was later created from the saved evaluation files. This note does not mark Phase 6 complete or draft the report.

This note interprets saved project evidence and maps it to a coursework report outline. It is not the graded report. It does not change the frozen Phase 4 methodology, the frozen Phase 5 design, or any saved score.

Numerical claims below are copied from the cited files. `outputs/evaluation/phase5_evaluation_report.md` states that its tables show six decimal places and that `outputs/evaluation/test_metrics.json` stores the measured floats. This note uses the JSON and CSV values. The six-decimal tables are a display of that same run, not a second measurement.

No model was trained, tuned, or evaluated for this note. `src/run_phase5.py` was not run.

---

## 1. Research question and prediction task

The only approved predictive research question is RQ1, recorded in `docs/phase-5-experimental-design.md`. Its wording is unchanged:

How effectively can Logistic Regression and Random Forest classify students into Dropout, Enrolled, and Graduate categories using enrolment, demographic, socioeconomic, and first- and second-semester academic information?

Two descriptive EDA questions were approved on 2026-11-16. They are not predictive modelling questions, and they do not authorise another experiment. They are answered only from the existing EDA evidence. Neither question establishes causation. `outputs/eda_report.md` says its associations are descriptions of the file, not causal claims.

**EDA Question 1.** How is the distribution of Dropout, Enrolled, and Graduate outcomes represented in the dataset?

Evidence: section 3 of `outputs/eda_report.md` and `figures/eda/figure_01_target_distribution.png`. The file counts are Graduate 2,209 (49.9322%), Dropout 1,421 (32.1203%), and Enrolled 794 (17.9476%). These are counts of the 4,424-row file, not model scores.

**EDA Question 2.** How do first- and second-semester academic progression measures, particularly grades and approved units, differ descriptively across the three outcome groups?

Evidence: section 5 of `outputs/eda_report.md`, `figures/eda/figure_03_semester_grades_by_target.png`, and `figures/eda/figure_04_academic_progression_by_target.png`. The reported means are:

| Measure | Dropout | Enrolled | Graduate |
| --- | ---: | ---: | ---: |
| First-semester grade average (0–20) | 7.257 | 11.125 | 12.644 |
| Second-semester grade average (0–20) | 5.899 | 11.117 | 12.697 |
| First-semester units approved | 2.552 | 4.319 | 6.232 |
| Second-semester units approved | 1.940 | 4.058 | 6.177 |

On these four measures, the Graduate mean is highest, the Dropout mean is lowest, and the Enrolled mean lies between them. That is a group difference in this file. It is not evidence that the grades or approved units caused the outcome.

The earlier proposed RQ2 and RQ3 in section 7 of `outputs/eda_report.md` remain unapproved. They are not the same text as EDA Question 1 or EDA Question 2, and this note does not approve them.

The report presentation is resolved. Predictive RQ1 is presented beside EDA Questions 1 and 2, and descriptive EDA stays distinct from predictive modelling. The reviewed assessment brief asks for two or three research questions. This presentation does not guarantee that the descriptive questions count toward that requirement. If that reading is unclear, it should be confirmed with the module leader.

The prediction point is after the second semester. The target is `Target`. The approved classes, in metric order, are Dropout, Enrolled, and Graduate. That order is `ALLOWED_LABELS` in `src/preprocessing.py` and the `labels` arrays in `outputs/evaluation/test_metrics.json`. There is no single positive class.

The comparison has three fitted estimators, named in `docs/phase-5-experimental-design.md`:

| Role | Estimator | Saved artefact |
| --- | --- | --- |
| Tuned linear model | `LogisticRegression` | `outputs/models/logistic_regression.joblib` |
| Tuned tree ensemble | `RandomForestClassifier` | `outputs/models/random_forest.joblib` |
| Baseline | `DummyClassifier(strategy="most_frequent")` | `outputs/models/dummy_most_frequent.joblib` |

The dummy classifier is the baseline. It is not a third competitive model, and the design does not name a single winner.

## 2. EDA findings relevant to the modelling results

The exploratory report is `outputs/eda_report.md`, dated 2026-11-14. Its notebook is `notebooks/01_exploratory_data_analysis.ipynb`. Its figures are in `figures/eda/`. The report states that no rows were dropped, encoded, scaled, or split, and that no model was trained. Its sentence that training had not started describes that EDA run. Training was later completed and approved in Phase 5. The associations remain descriptive. The report says they are not causal claims.

The audited file has 4,424 rows and 37 columns. Class counts in section 3 of the EDA report, also shown by `figures/eda/figure_01_target_distribution.png`:

| Class | Students | Percentage of rows |
| --- | ---: | ---: |
| Graduate | 2,209 | 49.9322% |
| Dropout | 1,421 | 32.1203% |
| Enrolled | 794 | 17.9476% |

These are file counts, not model scores. Graduate is the largest class and Enrolled is the smallest. That imbalance is why accuracy is not the only evaluation metric.

Section 5 of the EDA report gives means that separate the classes more clearly on academic progress than on entry grades:

| Measure | Dropout | Enrolled | Graduate |
| --- | ---: | ---: | ---: |
| Second-semester grade average (0–20) | 5.899 | 11.117 | 12.697 |
| Second-semester units approved | 1.940 | 4.058 | 6.177 |
| Second-semester units enrolled | 5.780 | 5.938 | 6.628 |
| Admission grade (0–200) | 124.961 | 125.534 | 128.794 |

Enrolled sits between Dropout and Graduate on semester grades and units approved. Units enrolled differ only modestly. `figures/eda/figure_03_semester_grades_by_target.png` and `figures/eda/figure_04_academic_progression_by_target.png` show the same pattern. The later test result, that Enrolled is the hardest class, is consistent with that overlap. The EDA does not cause the test result.

A recorded grade of 0 is tied to zero approved units. The EDA report states that all 718 first-semester grades of 0 also have 0 first-semester units approved, and all 870 second-semester grades of 0 also have 0 second-semester units approved. The share with a second-semester grade of 0 is 51.16% for Dropout, 8.56% for Enrolled, and 3.40% for Graduate. UCI does not say whether 0 is a real average or a placeholder. The file stores 0 rather than a missing value.

Matching semester measures are strongly correlated. The EDA report gives Pearson correlations of 0.945 for credited units, 0.943 for enrolled units, 0.904 for approved units, 0.837 for grades, and 0.779 for evaluations. `figures/eda/figure_07_numerical_correlation_heatmap.png` shows that block. Category codes are not in the heatmap.

`figures/eda/figure_06_selected_categoricals_by_target.png` includes debtor and tuition status. Among 528 students with tuition fees not up to date, 86.55% are in Dropout. Among 503 debtors, 62.03% are in Dropout. Those associations are large, and section 8 of the EDA report says neither field has a measurement date. They were excluded from the model matrix for that reason. Their descriptive association is not evidence that the fitted models used them.

Age at enrolment has mean 23.265 years. Mean age is 26.069 for Dropout, 22.369 for Enrolled, and 21.784 for Graduate. The stored column name is `Age at enrollment`. The notebook maps that column to the label "Age at enrolment (years)". This is a display label, not a second column.

Section 7 of the EDA report says the exploration does not answer RQ1, because the models had not been trained. The answer in section 9 of this note uses the later Phase 5 outputs. It does not treat the EDA report as a performance result.

## 3. Preprocessing and feature-engineering rationale

The frozen methodology is `docs/phase-4-preprocessing-plan.md`. The implementation is `src/preprocessing.py`. Phase 4 was approved on 2026-11-15. This note does not change it.

`RETAINED_FEATURES` lists 30 input columns. `EXCLUDED_FEATURES` lists six columns that stay out of the primary matrix:

- `Debtor`
- `Tuition fees up to date`
- `Unemployment rate`
- `Inflation rate`
- `GDP`
- `Curricular units 2nd sem (without evaluations)`

The first two lack a measurement date. The three macroeconomic fields lack a reference date. The last column has a name that says the second semester and a UCI sentence that says the first semester. Exclusion does not invent a date or decide which semester that column describes. The EDA report says its median is 0 in every target class.

Four binaries stay in the matrix under `TIMING_ASSUMPTION` in `src/preprocessing.py`: `Displaced`, `Educational special needs`, `Scholarship holder`, and `International`. Their individual UCI descriptions do not state a measurement date. Retention assumes they are available after the second semester. That date has not been verified. The EDA report says 110 students are international and 51 have special educational needs, so percentages for those small groups are unstable.

`Target` is not a predictor. The raw file is not edited. `clean_column_names()` in `src/preprocessing.py` copies the loaded table and, in memory only, removes tab characters and surrounding whitespace from every column name. It does not drop a column. The module comment records that the daytime/evening header in the zip extract has a trailing tab. No rows are dropped for duplicates or outliers: the audit recorded 0 duplicate rows, and the frozen plan does not authorise an outlier filter. Missing cells stay unimputed. The audit recorded 0 missing cells. Recorded semester grades of 0 stay numeric 0. No zero-grade sensitivity analysis was run.

No derived features were added. The Phase 4 plan rejects a semester-grade difference because the meaning of 0 would make that difference ambiguous. Nominal codes are one-hot encoded inside the training fold, with unknown codes ignored. `Application order` stays ordered. Binary 0/1 fields are not one-hot encoded and are not standardised. Numerical columns are standardised only in the logistic pipeline. The forest pipeline uses the same 30 columns and the same encoding, and it does not scale numerical columns. `docs/phase-5-experimental-design.md` records that split. The evaluation report checks that the forest numerical step is not a scaler and that the logistic scaler saw 3,539 rows at the training refit.

The approved split is 80/20, stratified on `Target`, with `random_state=42`. It is created in memory by `prepare_from_raw()`. It is not written to `data/processed/`. The evaluation report records 3,539 training rows and 885 test rows. Training counts are Graduate 1,767, Dropout 1,137, and Enrolled 635. Test counts are Graduate 442, Dropout 284, and Enrolled 159. These are split counts, not scores.

## 4. Experimental design and tuning methodology

The frozen design is `docs/phase-5-experimental-design.md`. The run that implemented it is described in `outputs/evaluation/phase5_evaluation_report.md`. Evaluation timestamp: `2026-11-15T19:45:33+05:00`. scikit-learn version recorded by that run: `1.9.1`. Raw SHA-256 before and after the run: `3ef126de5cefff26eb11fbb4237f1a1401cb64b488e2f1d598c23cedeb4c45ae`.

Grid search used `make_training_cv()`: five-fold `StratifiedKFold`, `shuffle=True`, `random_state=42`, on the training portion only. Each search estimator was a pipeline, so every fold fit its own encoder and, for logistic regression, its own scaler. Both searches used `scoring="f1_macro"`, `refit=True`, `error_score="raise"`, and `n_jobs=1`. The test portion was not passed to `GridSearchCV.fit`. `outputs/evaluation/run_metadata.json` records `"test_rows_used_for_tuning": 0` and `"test_rows": 885`.

Macro F1 is the primary metric and the selection metric. The other reported metrics are balanced accuracy, macro precision, accuracy, a confusion matrix, and per-class precision, recall, and F1. Balanced accuracy equals macro recall in this three-class evaluation. `outputs/evaluation/test_metrics.json` records `"macro_recall_equals_balanced_accuracy": true` for all three models. Macro recall is not a separate finding.

Logistic Regression used `max_iter=2000` and `solver="lbfgs"`. `penalty` was not passed. Its declared grid is eight configurations: `C` in {0.01, 0.1, 1, 10} and `class_weight` in {`None`, `"balanced"`}. That is 40 cross-validation fits plus one training refit.

Random Forest used `random_state=42` and `n_jobs=1`. Its declared grid is 36 configurations: `n_estimators` in {200, 400}, `max_depth` in {`None`, 10, 20}, `min_samples_leaf` in {1, 2, 4}, and `class_weight` in {`None`, `"balanced"`}. That is 180 cross-validation fits plus one training refit.

The grids were passed as one dictionary per declared configuration so `class_weight` changes fastest. On an exact tie of mean validation macro F1, the earliest declared configuration is kept. The run recorded one winning configuration for each search. Neither search had an exact tie. `tied_declared_indices` in `outputs/evaluation/selected_parameters.json` contains only the selected index for each model.

The dummy classifier was fit once on the training portion. It was not tuned and it is not part of the 220 cross-validation fits. The training split's largest class is Graduate, 1,767 of 3,539 rows, so a most-frequent rule predicts Graduate. That sentence describes the rule. It is not a macro F1.

`docs/phase-5-experimental-design.md` section 9 excludes feature importance, coefficient interpretation, resampling, a zero-grade sensitivity analysis, another classifier, and an alternative feature set. None of those analyses is added here.

The generated evaluation report says, "Phase 5 is not marked complete by this file." `run_metadata.json` still has `"phase_5_marked_complete": false`. Those sentences were written by the run, before the student approved Phase 5. The approval is in `docs/Phases.md` and `docs/Memory.md`. This note does not edit the generated files.

## 5. Cross-validation results

These values select the training configuration. They are not the 885-row holdout. `cv_results_` names the training-fold validation score `test_score`. That name is not the final test set.

Source: `outputs/evaluation/selected_parameters.json`. The six-decimal means in the generated markdown report are the same selection displayed to six places.

Logistic Regression, declared index 3, declared order 4:

- `classifier__C`: 0.1
- `classifier__class_weight`: `"balanced"`
- Mean CV macro F1: `0.6881125650673585`
- Fold standard deviation: `0.01991414406836082`
- Fold macro F1: `0.7120742318841323`, `0.7107293005075087`, `0.6832886203290932`, `0.6682840657995457`, `0.6661866068165126`
- Cross-validation fits completed: 40
- Training refit completed: true

Random Forest, declared index 13, declared order 14:

- `classifier__n_estimators`: 200
- `classifier__max_depth`: 20
- `classifier__min_samples_leaf`: 1
- `classifier__class_weight`: `"balanced"`
- Mean CV macro F1: `0.6998064617503175`
- Fold standard deviation: `0.012204693927217965`
- Fold macro F1: `0.7012925067243464`, `0.7078256956825489`, `0.7146554386714645`, `0.6786516024220942`, `0.696607065251133`
- Cross-validation fits completed: 180
- Training refit completed: true

Both selected configurations use `class_weight="balanced"`. That is a training-fold selection under macro F1. It is not a statement that class weighting won on the test set, because the test set was not used to choose it.

The forest mean is higher than the logistic mean, and its fold standard deviation is smaller. Those two means are not a test ranking. Each mean is the average of a different model's own training folds. The folds are not a shared paired test. Each fold standard deviation describes variation across that model's own five validation folds. It does not establish statistical significance, superiority, or a formal cross-model stability comparison. The full fold tables are `outputs/evaluation/logistic_regression_cv_results.csv` and `outputs/evaluation/random_forest_cv_results.csv`.

The dummy classifier has no cross-validation score in `selected_parameters.json`. It was not part of the search.

## 6. Test-set comparison

Each fitted estimator predicted the same untouched 885 test rows once. The test scores were not used to change parameters, features, class weights, or preprocessing. The three results stay independent. No universal winning model is declared.

Source: `outputs/evaluation/test_metrics.json`. The same models, metrics, and rounded displays are in `outputs/evaluation/test_metrics.csv` and `outputs/evaluation/phase5_evaluation_report.md`.

| Model | Macro F1 | Balanced accuracy | Macro precision | Accuracy |
| --- | ---: | ---: | ---: | ---: |
| Logistic Regression | 0.6892903420183808 | 0.7023012029890147 | 0.697566135029276 | 0.727683615819209 |
| Random Forest | 0.7016908329335929 | 0.7018610663191801 | 0.7079859524582094 | 0.7548022598870057 |
| Dummy most-frequent | 0.22205476011052497 | 0.3333333333333333 | 0.1664783427495292 | 0.4994350282485876 |

Macro F1 is the primary metric. On that metric, Random Forest is higher than Logistic Regression, and both are higher than the dummy. That ordering is not a licence to discard the other columns. Logistic Regression's balanced accuracy, `0.7023012029890147`, is slightly higher than Random Forest's `0.7018610663191801`. Random Forest's macro precision and accuracy are higher. A report that quotes only accuracy would overstate the forest. Graduate is the largest test class, with support 442 of 885, so it contributes the greatest number of observations to overall accuracy. That can obscure weaker performance on the smaller classes.

The dummy is a baseline, not a competitive model. Its test macro F1 is `0.22205476011052497`. Its accuracy, `0.4994350282485876`, equals the Graduate share of this test split, because every test row was predicted Graduate. The full-data Graduate share of 49.9322% is a different quantity. It is the share of all 4,424 rows in `outputs/eda_report.md`, not this test accuracy.

Logistic Regression's test macro F1, `0.6892903420183808`, is close to its training-fold mean, `0.6881125650673585`. Random Forest's test macro F1, `0.7016908329335929`, is close to its training-fold mean, `0.6998064617503175`. Closeness is not a formal statistical test. It does say that the holdout did not produce a large drop from the selection scores. The two kinds of score still answer different questions: the cross-validation means chose the settings, and the test metrics estimate those frozen settings once.

## 7. Per-class performance and confusion matrices

Per-class values are copied from `outputs/evaluation/per_class_metrics.csv`. They match `per_class` in `outputs/evaluation/test_metrics.json`. Confusion counts are copied from `outputs/evaluation/confusion_matrices.csv`. Rows are actual labels and columns are predicted labels, in the order Dropout, Enrolled, Graduate.

### Logistic Regression

| Class | Precision | Recall | F1 | Support |
| --- | ---: | ---: | ---: | ---: |
| Dropout | 0.8050847457627118 | 0.6690140845070423 | 0.7307692307692307 | 284 |
| Enrolled | 0.4163265306122449 | 0.6415094339622641 | 0.504950495049505 | 159 |
| Graduate | 0.8712871287128713 | 0.7963800904977375 | 0.8321513002364066 | 442 |

| Actual \ Predicted | Dropout | Enrolled | Graduate |
| --- | ---: | ---: | ---: |
| Dropout | 190 | 69 | 25 |
| Enrolled | 30 | 102 | 27 |
| Graduate | 16 | 74 | 352 |

### Random Forest

| Class | Precision | Recall | F1 | Support |
| --- | ---: | ---: | ---: | ---: |
| Dropout | 0.8277310924369747 | 0.6936619718309859 | 0.7547892720306514 | 284 |
| Enrolled | 0.4574468085106383 | 0.5408805031446541 | 0.4956772334293948 | 159 |
| Graduate | 0.8387799564270153 | 0.8710407239819005 | 0.8546059933407325 | 442 |

| Actual \ Predicted | Dropout | Enrolled | Graduate |
| --- | ---: | ---: | ---: |
| Dropout | 197 | 54 | 33 |
| Enrolled | 32 | 86 | 41 |
| Graduate | 9 | 48 | 385 |

### Dummy most-frequent

| Class | Precision | Recall | F1 | Support |
| --- | ---: | ---: | ---: | ---: |
| Dropout | 0.0 | 0.0 | 0.0 | 284 |
| Enrolled | 0.0 | 0.0 | 0.0 | 159 |
| Graduate | 0.4994350282485876 | 1.0 | 0.6661642803315749 | 442 |

| Actual \ Predicted | Dropout | Enrolled | Graduate |
| --- | ---: | ---: | ---: |
| Dropout | 0 | 0 | 284 |
| Enrolled | 0 | 0 | 159 |
| Graduate | 0 | 0 | 442 |

Graduate is the strongest class for both tuned models. Its F1 is `0.8321513002364066` for Logistic Regression and `0.8546059933407325` for Random Forest. Dropout is next. Enrolled is the weakest class for both, with F1 `0.504950495049505` and `0.4956772334293948`. Enrolled is the smallest class and its EDA measures overlap with the other two classes. These observations are consistent with the weaker Enrolled-class results, but this analysis does not establish the cause. The macro F1 values in section 6 do not mean each class is classified equally well.

Logistic Regression is slightly better on the Enrolled F1. It is not better on every Enrolled metric. Its Enrolled recall, `0.6415094339622641`, is higher than the forest recall, `0.5408805031446541`. Its Enrolled precision, `0.4163265306122449`, is lower than the forest precision, `0.4574468085106383`. The matrix shows the same trade. Logistic Regression places 102 of the 159 enrolled students on the Enrolled diagonal, and 69 actual dropout students in the Enrolled column. Random Forest places 86 enrolled students on that diagonal, and 54 actual dropout students in the Enrolled column. The saved Enrolled precision values are `0.4163265306122449` and `0.4574468085106383`, so many students predicted as Enrolled are not enrolled.

The main off-diagonal pattern for both tuned models is confusion with a neighbouring academic outcome, not a swap of Dropout and Graduate. For Logistic Regression, 69 of 284 actual dropout students are predicted Enrolled and 25 are predicted Graduate. For Random Forest, those counts are 54 and 33. Actual graduates are more often predicted Enrolled than Dropout: 74 versus 16 for Logistic Regression, and 48 versus 9 for Random Forest. Actual enrolled students split across both other classes.

The dummy matrix has no correct Dropout or Enrolled prediction. All 284 dropout rows, all 159 enrolled rows, and all 442 graduate rows fall in the predicted-Graduate column. Its Graduate recall of 1.0 is the recall of a constant prediction. Its Dropout and Enrolled F1 values are 0.0. That is why its macro F1 is `0.22205476011052497` even though its accuracy is `0.4994350282485876`. The row-level predictions are stored in `outputs/evaluation/predictions.csv`. This note does not recompute them.

## 8. Limitations and threats to validity

These limits are already documented. This section does not add an experiment to close them.

- **One institution.** Planning documents record that UCI describes the records as coming from one higher education institution. The result does not establish the same performance at another institution. No external cohort was evaluated.
- **Class imbalance.** Enrolled is 794 of 4,424 rows in the EDA report and 159 of 885 test rows. Macro F1 and balanced accuracy were used because accuracy follows the largest class. The dummy accuracy shows that failure mode.
- **Enrolled overlap.** Semester grades and units approved place Enrolled between the other two classes in the EDA means. Both tuned models have their lowest F1 on Enrolled, and Enrolled precision is weak.
- **Undated binaries.** `Displaced`, `Educational special needs`, `Scholarship holder`, and `International` are in the 30-column matrix under an unverified timing assumption. If any of them was recorded after the prediction point, the models could use information that would not have been available then.
- **Six exclusions.** `Debtor`, `Tuition fees up to date`, `Unemployment rate`, `Inflation rate`, `GDP`, and `Curricular units 2nd sem (without evaluations)` are excluded. Debtor and tuition have large descriptive associations and no measurement date. Leaving them out avoids an undated field. It also means the models do not use those associations. The macroeconomic dates and the conflicting semester sentence remain unresolved.
- **Zero grades.** 718 first-semester and 870 second-semester grades of 0 stay numeric 0, each aligned with 0 approved units. Standardising the logistic matrix changes units. It does not impute those zeros. What 0 means is still unknown. No sensitivity analysis was run.
- **Correlated semester features.** Matching first- and second-semester measures have Pearson correlations from 0.779 to 0.945 in the EDA report. Both semesters remain in the matrix because the prediction point is after the second semester. This note does not partial out that redundancy. Coefficient or importance analysis would be a new experiment and is not authorised.
- **Small coded groups.** International students number 110 and students with special educational needs number 51. Rare marital-status codes cover 4, 25, and 6 students. Their target percentages are unstable. Rare levels were not merged.
- **Single split.** The holdout is one stratified 885-row split with `random_state=42`. Cross-validation varies the training folds. It does not create a second external test set. The test set was used once.
- **No resampling and no extra model.** Class imbalance was handled by the metric and by the `class_weight` grid, not by SMOTE or another sampler. No third classifier was fitted.
- **No fairness audit.** Gender, age, nationality, and the other demographic fields are in the matrix or were described in EDA. `figures/eda/figure_06_selected_categoricals_by_target.png` shows different target mixes. That is descriptive. A fairness audit was not run, and this note does not invent one.
- **Generated completion flags.** The evaluation report and `run_metadata.json` still say the run file itself did not mark Phase 5 complete. The student approval is recorded elsewhere. Editing those generated flags would change an approved artefact.
- **Report rules.** The CMP6202 Assessment Brief 2026–27 and Individual Report Template 2026–27 were reviewed on 2026-11-16. On 2026-11-17 both files were inspected and are stored at the repository root as `CMP6202 Assessment Brief  2026-27.docx` and `CMP6202 Individual Report Template 2026-27.docx`. The brief sets a maximum of 3,000 words with a +10% margin only; nothing beyond that margin is marked. Page 1 also says 3,000 words excluding references. The word-count section includes headings, tables, citations, quotes, and lists in the main body, and it excludes material before the body and references, bibliographies, and appendices. It does not state a lower margin. The brief also requires 11-point font, 1.5 line spacing, anonymous marking by student number only, BCU Harvard referencing, a cover sheet completed and appended, and the printed deadline fields 4th December 2026 and 03:00PM. The template contents are nested. The 13 content headings are mapped to those contents entries in `docs/phase-6-report-outline.md`. The items this repository cannot yet satisfy remain in sections 10 and 11.

## 9. Concise answer to RQ1

Logistic Regression and Random Forest can classify Dropout, Enrolled, and Graduate more effectively than a most-frequent baseline, on the approved 30-column feature set and on the untouched 885-row test split. Using macro F1, the primary metric, Random Forest scores `0.7016908329335929`, Logistic Regression scores `0.6892903420183808`, and the dummy scores `0.22205476011052497`. All three values are in `outputs/evaluation/test_metrics.json`.

That effectiveness is uneven. Graduate is classified best, Dropout next, and Enrolled clearly worse. Logistic Regression has the slightly higher Enrolled F1, `0.504950495049505` against `0.4956772334293948`, with higher Enrolled recall and lower Enrolled precision. Random Forest has the higher overall test macro F1, macro precision, and accuracy. Logistic Regression has the slightly higher balanced accuracy. These differences do not make either tuned model a universal winner.

The cross-validation means chose the settings and are not this answer. The answer uses the single test evaluation made after those settings were frozen. It is a descriptive classification result for one institution's records. It is not a causal claim about what makes a student drop out, remain enrolled, or graduate.

## 10. Coursework report evidence map

The student reviewed the CMP6202 Assessment Brief 2026–27 and the Individual Report Template 2026–27 on 2026-11-16. On 2026-11-17 both files were inspected and are stored at the repository root as `CMP6202 Assessment Brief  2026-27.docx` and `CMP6202 Individual Report Template 2026-27.docx`. This map follows those inspected template sections. The evidence-map revision initially left `docs/Phases.md`, `docs/Memory.md`, `docs/PRD.md`, and `README.md` unchanged. A subsequent documentation synchronization updated those four files. The current project documentation distinguishes predictive RQ1 from the two approved descriptive EDA questions. The earlier proposed RQ2 and RQ3 remain unapproved. The report must follow the official template. The section-by-section writing plan is `docs/phase-6-report-outline.md`. This map is not the report, and it is not a claim that every template requirement is already satisfied.

Formatting and submission requirements recorded from the inspected brief:

- Maximum 3,000 words, with a +10% margin only. Nothing beyond that margin is marked. Page 1 also says 3,000 words excluding references. Headings, tables, citations, quotes, and lists in the main body count. Material before the body, and references, bibliographies, and appendices, do not. The brief does not state a lower margin.
- 11-point font and 1.5 line spacing.
- Anonymous marking: student number only. The recorded student number is s24156365. The student name must not appear in the report.
- BCU Harvard referencing.
- The brief requires the cover sheet to be completed and appended. That sheet has not been completed in this repository.
- The brief prints the deadline as 4th December 2026 and 03:00PM.

Approved report-preparation decisions, recorded on 2026-11-17:

- **Title.** Predicting Student Academic Outcomes Using Logistic Regression and Random Forest.
- **Audience.** Academic and technical readers familiar with introductory machine learning.
- **Questions.** The report presents predictive RQ1 beside the two approved descriptive EDA questions. Predictive modelling and descriptive EDA stay distinct. The earlier proposed RQ2 and RQ3 remain unapproved.
- **Seen data.** Five-fold training-only cross-validation is validation evidence. The 885-row holdout is unseen test evidence. Cross-validation results are not training-set performance. Separate final-model training-set metrics were not produced and are not calculated here.
- **Comparison figure.** Created and verified at `figures/model_comparison/figure_01_model_comparison_f1.png` by `src/plot_model_comparison.py` from the saved results only. Panel A is five-fold training-only cross-validation macro F1 for the selected Logistic Regression and Random Forest. No dummy cross-validation score was saved, so none is shown. Panel B is holdout macro F1 for the dummy, Logistic Regression, and Random Forest. Panel C is holdout F1 for Dropout, Enrolled, and Graduate. It must not name an overall winner.
- **Submission package.** Prepare a separate Word report and a technical project ZIP, and include the public GitHub repository link in the report. The final Moodle submission instructions still have to be verified when the actual submission is prepared. This decision does not claim that those instructions have been checked.

The report must not introduce a score, a model, a feature, or a citation that is not already supported. The earlier proposed RQ2 and RQ3 must not be written as approved questions. EDA Questions 1 and 2 may be answered only as descriptive questions.

### 10.1 Report introduction and target audience

**Purpose.** Introduce the approved title, the task, predictive RQ1, the two descriptive EDA questions, and the explicit audience.

**Claims.** The title is Predicting Student Academic Outcomes Using Logistic Regression and Random Forest. The audience is academic and technical readers familiar with introductory machine learning. The task is multiclass classification of `Target` after the second semester. RQ1 is the only predictive question. EDA Questions 1 and 2 are descriptive. The study compares Logistic Regression, Random Forest, and a most-frequent dummy without naming a winner.

**Evidence.** `docs/phase-5-experimental-design.md` section 1. Section 1 of this note. `README.md` for the dataset citation and the single-institution description recorded from UCI. Section 11.A of this note for the 2026-11-17 title and audience decision.

**Missing.** The introduction text is not written. See section 11.A.

### 10.2 Dataset identification, source, licence, and every attribute

**Purpose.** Identify the dataset and describe every attribute by name, data type, and meaning.

**Claims.** The dataset is Predict Students' Dropout and Academic Success, UCI 697, DOI https://doi.org/10.24432/C5MC89. The local audit measured 4,424 rows and 37 columns, with 0 missing cells. The licence quotation recorded on 2026-11-14 is CC BY 4.0.

**Evidence.** `README.md` dataset table, citation, and licence quotation. `outputs/dataset_audit.md`, including its column dictionary. `data/raw/data.csv` and the preserved zip.

**Missing.** The report still has to present every attribute from that dictionary and from the UCI documentation. Meanings and types must be copied from those sources. They must not be invented. See section 11.I. The audit header for daytime/evening attendance still contains the trailing tab present in the raw file. `clean_column_names()` removes that tab in memory and does not drop the column.

### 10.3 Supervised learning task and target variable

**Purpose.** State the supervised task and the target.

**Claims.** The task is multiclass classification. The target is `Target`, with classes Dropout, Enrolled, and Graduate. There is no single positive class. The target is not an input. The prediction point is after the second semester.

**Evidence.** `docs/phase-5-experimental-design.md` section 1. `src/preprocessing.py` (`TARGET_COLUMN`, `ALLOWED_LABELS`). `outputs/dataset_audit.md` target section. `outputs/evaluation/test_metrics.json` label order.

**Missing.** None in the saved evidence. The approved audience is recorded in section 11.A. The task section of the report is not written.

### 10.4 Generative AI declaration

**Purpose.** State why generative AI was used, what it produced, which tools were used, and how the student checked the material.

**Claims.** The declaration must be truthful. ChatGPT and Cursor were used. A statement that no generative AI was used would be false. The student must verify the submitted work and take ownership of it.

**Evidence.** `docs/Memory.md` section 14 records Cursor assistance. It does not yet contain a complete declaration covering ChatGPT.

**Missing.** The declaration text is not written. See section 11.G.

### 10.5 Exploratory data analysis

**Purpose.** Answer EDA Questions 1 and 2 from the saved exploration, without causal claims.

**Claims.** Use the class counts and the semester grade and approved-unit means in section 1. Graduate is the largest class and Enrolled is the smallest. On the four cited progression measures, Graduate has the highest mean and Dropout the lowest. A grade of 0 aligns with zero approved units. These are file descriptions.

**Evidence.** `outputs/eda_report.md` sections 3 and 5. `notebooks/01_exploratory_data_analysis.ipynb`. `figures/eda/figure_01_target_distribution.png`, `figures/eda/figure_03_semester_grades_by_target.png`, and `figures/eda/figure_04_academic_progression_by_target.png`. The other saved figures may support context, not a new question: `figure_02_numerical_distributions.png`, `figure_05_age_by_target.png`, `figure_06_selected_categoricals_by_target.png`, and `figure_07_numerical_correlation_heatmap.png`.

**Missing.** Report captions are not written. The EDA report's statement that training had not started describes 2026-11-14, before Phase 5. The proposed RQ2 and RQ3 text in that report stays unapproved.

### 10.6 Experimental design

**Purpose.** Explain the split, the three estimators, the primary metric, and the rule that the test set was not used for tuning.

**Claims.** The split is 80/20, stratified, `random_state=42`, with 3,539 training rows and 885 test rows. Macro F1 is primary. Balanced accuracy is the recall summary. The dummy predicts the most frequent training class and is not tuned. No single winner is authorised.

**Evidence.** `docs/phase-5-experimental-design.md` sections 1 and 4–9. `docs/phase-4-preprocessing-plan.md`. `outputs/evaluation/phase5_evaluation_report.md`. `outputs/evaluation/run_metadata.json` for `test_rows` 885 and `test_rows_used_for_tuning` 0.

**Missing.** The report text is not written. The approved reporting rule is in section 11.B. Five-fold training-only cross-validation is validation evidence. The 885-row holdout is unseen test evidence. Separate final-model training-set metrics were not produced.

### 10.7 Predictive modelling / model development

**Purpose.** Explain the frozen preprocessing and the training-only search.

**Claims.** Thirty columns are retained and six are excluded. Four binaries are provisional. Zeros stay zero. No derived feature was added. Logistic Regression standardises numerical columns. Random Forest does not. The selected training settings are logistic order 4, `C=0.1`, `class_weight="balanced"`, and forest order 14, `n_estimators=200`, `max_depth=20`, `min_samples_leaf=1`, `class_weight="balanced"`. The search completed 40 and 180 cross-validation fits, two training refits, and one dummy fit.

**Evidence.** `src/preprocessing.py`. `docs/phase-4-preprocessing-plan.md`. `docs/phase-5-experimental-design.md` sections 2, 3, and 5. `outputs/evaluation/selected_parameters.json`. `outputs/models/logistic_regression.joblib`, `outputs/models/random_forest.joblib`, and `outputs/models/dummy_most_frequent.joblib`.

**Missing.** Feature importance and coefficient analysis were not part of the frozen design. See section 11.D. A separate untuned Logistic Regression or Random Forest was not saved.

### 10.8 Evaluation and further modelling improvements

**Purpose.** Report the one holdout comparison and state which further analyses were not run.

**Claims.** Use the test table in section 6 and the class tables in section 7. Random Forest has the higher test macro F1. Logistic Regression has the slightly higher Enrolled F1 and the slightly higher balanced accuracy. Enrolled is the weak class. The dummy predicts every test row as Graduate. Cross-validation results stay distinct from this holdout. No further modelling improvement was approved after Phase 5.

**Evidence.** `outputs/evaluation/test_metrics.json`, `test_metrics.csv`, `per_class_metrics.csv`, `confusion_matrices.csv`, `predictions.csv`, and `phase5_evaluation_report.md`. Training-fold selection: `outputs/evaluation/selected_parameters.json`. The comparison figure is `figures/model_comparison/figure_01_model_comparison_f1.png`.

**Missing.** Separate final-model training-set metrics were not produced. See sections 11.B and 11.C. Further improvements must not be invented. The report text that discusses the figure is not written.

### 10.9 Conclusion

**Purpose.** Answer RQ1 from section 9, and keep EDA Questions 1 and 2 descriptive.

**Claims.** Both tuned models beat the most-frequent baseline on test macro F1. Performance is strongest for Graduate and weakest for Enrolled. Neither tuned model is a universal winner. The class distribution and the semester-progression differences describe the file. They do not cause the classification result.

**Evidence.** Section 9 of this note. `outputs/evaluation/test_metrics.json` and `per_class_metrics.csv`. Section 1 of this note for the EDA answers. Section 8 for the limitations.

**Missing.** The conclusion text is not written. The approved audience is academic and technical readers familiar with introductory machine learning. No deployment claim is supported.

### 10.10 Reflection on individual learning

**Purpose.** Record the student's own learning, the technical challenges, and how those challenges were addressed.

**Claims.** Only experiences the student can verify. This note does not supply them.

**Evidence.** None yet. `docs/Memory.md` records project decisions and blockers, not a personal reflection.

**Missing.** The reflection is unwritten. See section 11.F.

### 10.11 Certification evidence in AI/ML

**Purpose.** Provide genuine certification evidence if the template requires certificates achieved during the project.

**Claims.** None. No certificate is stored, and none is claimed.

**Evidence.** No `certificates/` files are in the repository.

**Missing.** The student has not selected certificates. Dates would have to be checked against the project period before any certificate could be said to meet an "achieved during the project" condition. See section 11.F.

### 10.12 Mandatory public GitHub repository link

**Purpose.** Give the marker the public repository that holds the code and evidence.

**Claims.** The link recorded in `README.md` is https://github.com/juraidyousaf/CMP6202-AI-ML-Project. The local folder name `CMP6202-AI-ML` differs from that repository name.

**Evidence.** `README.md`. `docs/Memory.md` naming note.

**Missing.** Public accessibility and completeness have not been independently verified. See section 11.E. The approved package in section 11.H includes this link in the Word report. The final Moodle instructions have not been verified.

### 10.13 BCU Harvard references

**Purpose.** Attribute the dataset and any other source the report actually uses, in BCU Harvard form.

**Claims.** The dataset citation currently recorded is Realinho, Vieira Martins, Machado, and Baptista (2021), DOI https://doi.org/10.24432/C5MC89. The licence quotation recorded on 2026-11-14 is CC BY 4.0, https://creativecommons.org/licenses/by/4.0/legalcode. References are excluded from the 3,000-word count.

**Evidence.** `README.md` attribution section. `outputs/dataset_audit.md`.

**Missing.** `references/` does not hold a formatted bibliography. BCU Harvard formatting has not been checked against a source opened for this revision. Scikit-learn 1.9.1 is a recorded library version, not a formatted reference. The inspected brief and template are available locally as `CMP6202 Assessment Brief  2026-27.docx` and `CMP6202 Individual Report Template 2026-27.docx`. A formatted BCU Harvard reference for either file has not been prepared and must not be invented.

## 11. Outstanding requirements and decisions

Items decided on 2026-11-17 are marked decided. The other items remain unresolved. This revision does not mark Phase 6 complete and does not draft the report.

### 11.A Report title and target audience

Decided on 2026-11-17. The report title is Predicting Student Academic Outcomes Using Logistic Regression and Random Forest. The explicit audience is academic and technical readers familiar with introductory machine learning. The report has not been drafted. This decision does not change the wording of RQ1.

### 11.B Seen-data reporting

Decided on 2026-11-17. The report will present the five-fold training-only cross-validation as validation evidence and the 885-row holdout as unseen test evidence. Cross-validation results must not be called training-set performance. Separate final-model training-set metrics were not produced. They were not calculated for this decision, and the models were not rerun.

### 11.C Model comparison visualisation

Created and verified from the saved results only. The file is `figures/model_comparison/figure_01_model_comparison_f1.png`, written by `src/plot_model_comparison.py`.

- Panel A uses the selected-row `mean_cv_macro_f1` in `outputs/evaluation/logistic_regression_cv_results.csv` and `outputs/evaluation/random_forest_cv_results.csv`. Those values also match `outputs/evaluation/selected_parameters.json`. No dummy cross-validation score was saved, so the dummy is not in this panel. These are validation scores, not training-set performance.
- Panel B uses holdout `macro_f1` for `dummy_most_frequent`, `logistic_regression`, and `random_forest` in `outputs/evaluation/test_metrics.json` and `outputs/evaluation/test_metrics.csv`.
- Panel C uses holdout per-class `f1` for Dropout, Enrolled, and Graduate, in that saved label order, from `outputs/evaluation/per_class_metrics.csv` and `outputs/evaluation/test_metrics.json`.

The figure does not retrain a model, change a result, or name an overall winner. Bar labels are rounded to three decimal places. The bar heights use the saved values.

### 11.D Feature impact

The template may invite discussion of feature importance or feature impact. The frozen Phase 5 design did not include Random Forest feature importance or Logistic Regression coefficient analysis. Those analyses remain limitations or possible future work. They were not calculated.

### 11.E GitHub

The recorded repository link is https://github.com/juraidyousaf/CMP6202-AI-ML-Project. Public accessibility and completeness have not been independently verified. The checks still required are: Python code is present, the README contains reproduction instructions, the dataset or its exact source link is present, and the relevant project evidence is present.

### 11.F Reflection and certification evidence

The reflection must come from the student's actual learning, the technical challenges, and how they were addressed. This note does not invent those experiences. Certification evidence must be genuine and verifiable. No certificate is claimed to meet an "achieved during the project" condition, because no certificate file has been checked against the project period.

### 11.G Generative AI declaration

The declaration must truthfully cover why generative AI was used, what it was used for, which tools were used, and how the generated material was checked. The student has used ChatGPT and Cursor. The declaration must not say that no generative AI was used. The student must verify and take ownership of all submitted work.

### 11.H Submission format discrepancy

Decided on 2026-11-17 as the preparation package: a separate Word report, a technical project ZIP, and the public GitHub repository link inside the report. The earlier brief and template described different Moodle routes. The final Moodle submission instructions still have to be verified when the actual submission is prepared. This decision does not claim that those instructions have been checked, and it does not claim that the Word report or the ZIP exists.

### 11.I Dataset attribute descriptions

The template asks for every attribute's name, data type, and meaning. That remains a report-preparation task. The source is the column dictionary in `outputs/dataset_audit.md` and the authoritative UCI documentation already used by that audit. Attribute meanings and data types must not be invented. Unresolved notes in the audit, including undated fields and the conflicting semester sentence, stay unresolved.

## 12. What this document does not do

- It does not mark Phase 6 complete.
- It does not draft the full report.
- It does not change the wording of RQ1 or the approved Phase 5 conclusions in section 9.
- It does not approve the earlier proposed RQ2 or RQ3.
- It records the approved report title and audience. It does not draft either into the report.
- It does not name a winning model.
- It does not add feature importance, coefficients, a fairness audit, resampling, a zero-grade sensitivity analysis, or another classifier.
- It records that separate final-model training-set metrics were not produced, and it does not calculate them.
- It records the comparison figure created from the saved evaluation files. It does not treat that figure as a new measurement.
- It does not change `src/`, `tests/`, `notebooks/`, `data/`, `figures/`, `outputs/`, or the frozen Phase 4 and Phase 5 documents.
