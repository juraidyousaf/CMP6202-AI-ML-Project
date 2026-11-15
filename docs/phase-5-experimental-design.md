# Phase 5 experimental design

**Status: formally approved and frozen on 2026-11-15. The experimental design is final and was not changed. The student reviewed and approved the implementation, model results, evaluation metrics, report, and generated artefacts on 2026-11-15. Phase 5 — Model Development and Evaluation is complete and approved. No score in this document is a result.**

Module: CMP6202 Artificial Intelligence and Machine Learning  
Student ID: s24156365  
Date: 2026-11-15

Phase 4 was approved as complete on 2026-11-15. Its methodology stays frozen in `docs/phase-4-preprocessing-plan.md` and `src/preprocessing.py`. This note does not change that methodology.

The student formally approved this experimental design as final and froze it on 2026-11-15. The decisions below are unchanged. A later run implemented this design without changing it. Measured scores are in the evaluation report, not in this document.

---

## 1. Research question

The only approved research question is RQ1:

How effectively can Logistic Regression and Random Forest classify students into Dropout, Enrolled, and Graduate categories using enrolment, demographic, socioeconomic, and first- and second-semester academic information?

RQ2 and RQ3 stay proposed. This design does not approve them.

The comparison has three estimators. The implementation run fit them. Their scores are not copied here.

| Role | Estimator |
| --- | --- |
| Tuned linear model | `LogisticRegression` |
| Tuned tree ensemble | `RandomForestClassifier` |
| Baseline | `DummyClassifier(strategy="most_frequent")` |

The dummy classifier is the baseline. It is not a third advanced model. Both tuned models are evaluated on the test set independently. This design does not name a single winner.

## 2. Logistic Regression

**Student-approved configuration.**

Fixed arguments:

- `max_iter=2000`
- `solver="lbfgs"`

Do not pass `penalty`. In the installed scikit-learn 1.9.1 that argument is deprecated. Pass it only if a later, separate decision says a future library version requires it. `multi_class` is not a parameter on this version. Other `LogisticRegression` arguments stay at the library defaults, including `random_state=None` and `n_jobs=None`.

Hyperparameter grid, in this declared order. `class_weight` changes fastest:

| Order | `C` | `class_weight` |
| --- | ---: | --- |
| 1 | 0.01 | `None` |
| 2 | 0.01 | `"balanced"` |
| 3 | 0.1 | `None` |
| 4 | 0.1 | `"balanced"` |
| 5 | 1 | `None` |
| 6 | 1 | `"balanced"` |
| 7 | 10 | `None` |
| 8 | 10 | `"balanced"` |

That is 4 × 2 = 8 configurations and 8 × 5 = 40 cross-validation fits, plus one refit on the full training portion. The refit is not one of the 40.

The preprocessor is the existing Phase 4 logistic pipeline from `make_logistic_preprocessor()`: binaries stay 0/1, `Application order` stays an integer, nominal codes are one-hot encoded, and numerical columns are standardised. The search estimator is one pipeline with steps `preprocess` and `classifier`. Grid keys are `classifier__C` and `classifier__class_weight`.

## 3. Random Forest

**Student-approved configuration.**

Fixed arguments:

- `random_state=42`
- `n_jobs=1`

Hyperparameter grid, in this declared order. The last parameter changes fastest:

1. `n_estimators`: 200, then 400
2. `max_depth`: `None`, then 10, then 20
3. `min_samples_leaf`: 1, then 2, then 4
4. `class_weight`: `None`, then `"balanced"`

The first configuration is `n_estimators=200`, `max_depth=None`, `min_samples_leaf=1`, `class_weight=None`. The last is `n_estimators=400`, `max_depth=20`, `min_samples_leaf=4`, `class_weight="balanced"`.

That is 2 × 3 × 3 × 2 = 36 configurations and 36 × 5 = 180 cross-validation fits, plus one refit on the full training portion. The refit is not one of the 180.

In scikit-learn 1.9.1 the forest defaults that this design does not change are `criterion="gini"`, `max_features="sqrt"`, `min_samples_split=2`, `bootstrap=True`, and `ccp_alpha=0.0`.

The preprocessor is the existing Phase 4 forest pipeline from `make_forest_preprocessor()`. It uses the same 30 columns and the same encoding, and it does not scale numerical columns. The search estimator is one pipeline with steps `preprocess` and `classifier`.

`GridSearchCV` also uses `n_jobs=1`. The forest and the search therefore do not build nested worker pools.

## 4. Class imbalance

**Student-approved.** Compare unweighted and class-weighted fits through the `class_weight` values in the grids above. Macro F1 is the primary selection metric.

Do not use SMOTE, random oversampling, random undersampling, or any other resampling. `imbalanced-learn` is not installed and is not authorised.

The dummy baseline stays `strategy="most_frequent"`. It is not given a class weight and it is not tuned.

In the measured training split, Graduate is the largest class: 1,767 of 3,539 rows. A most-frequent rule therefore predicts Graduate. That statement describes the rule. It is not a macro F1.

## 5. Grid-search protocol

**Student-approved.** For both tuned estimators:

- Use `GridSearchCV`.
- `cv` is `make_training_cv()` from `src/preprocessing.py`: 5-fold `StratifiedKFold`, `shuffle=True`, `random_state=42`. Do not pass `cv=5` or `cv=None`.
- `scoring="f1_macro"`.
- `refit=True`.
- `error_score="raise"`.
- `n_jobs=1`.
- The estimator is the full pipeline, so each training fold fits its own encoder and, for logistic regression, its own scaler.
- Do not fit a preprocessor on all training rows and then reuse it across folds.
- Fit the search on `X_train` and `y_train` only.
- Do not pass `X_test` or `y_test` into the search or into any score used to choose parameters.

Approved size. The 2026-11-15 run completed this size. Fold scores are stored in the evaluation CSV files, not in this document:

| Model | Configurations | CV fits | Extra refit on all training rows |
| --- | ---: | ---: | --- |
| Logistic Regression | 8 | 40 | 1 |
| Random Forest | 36 | 180 | 1 |
| Total | 44 | 220 | 2 |

The 220 fits are the cross-validation fits only. The two refits are additional. Both refits use the training portion only. The dummy classifier is not part of either count.

On an exact tie of mean cross-validated macro F1, select the first configuration in the declared grid order in sections 2 and 3. scikit-learn's `ParameterGrid` sorts parameter names alphabetically, so that library order is not this declared order. Implementation must break the tie from the declared lists, not from an alphabetical key sort.

When a run exists, record for each tuned algorithm:

- The selected parameter dictionary.
- The best mean cross-validated macro F1.
- The five fold scores, their mean, and their standard deviation.

`cv_results_` uses the name "test score" for the validation fold inside training. That is not the held-out 885-row test set. The implementation stores those fold scores in the evaluation CSV files.

## 6. Dummy baseline

**Student-approved.** Use `DummyClassifier(strategy="most_frequent")`.

In scikit-learn 1.9.1 the constructor default for `strategy` is `"prior"`. Implementation must pass `"most_frequent"` explicitly.

The baseline is not tuned. It is not part of `GridSearchCV`. It is fit once on the training portion and then evaluated once on the test portion, as in section 7.

## 7. Final test evaluation

Cross-validation selects each tuned configuration. The test set is a separate, later step.

After both searches have finished:

1. Refit each selected pipeline on the complete training portion. `refit=True` does this inside `GridSearchCV`.
2. Fit `DummyClassifier(strategy="most_frequent")` on that same training portion.
3. Predict the untouched 885-row test portion once with each of the three fitted estimators.
4. Report each model's test results independently, using the metrics in section 8.
5. Do not designate one algorithm as the single selected winner.
6. Do not use the test scores to change parameters, features, class weights, or this methodology.

The measured split remains 3,539 training rows and 885 test rows. Those are split counts, not scores.

## 8. Evaluation metrics

Unchanged from Phase 4:

- Macro F1, the primary metric
- Balanced accuracy
- Macro precision
- Accuracy
- Confusion matrix
- Per-class precision, recall, and F1

Pass the class order `Dropout`, `Enrolled`, `Graduate` into the confusion matrix and the classification report. That is `ALLOWED_LABELS` in `src/preprocessing.py`.

Balanced accuracy and macro recall are the same quantity in this three-class task. Report one of them as the recall summary. Do not describe the other as a separate finding.

## 9. Additional experiments

**Student-approved.** There are no additional experiments.

This phase does not include:

- Random Forest feature importance as a separate experiment.
- Logistic Regression coefficient interpretation as a separate experiment.
- Resampling experiments.
- A zero-grade sensitivity analysis.
- Another classifier.
- An alternative feature set or an ablation.

Those analyses would be a new decision.

## 10. Output locations

**Student-approved** directories. This documentation task did not create the artefacts. The 2026-11-15 implementation later wrote the files below. Listing them does not change the design.

- `outputs/models/` for fitted model artefacts.
- `outputs/evaluation/` for cross-validation summaries, test metrics, predictions, and confusion matrices.

Implementation filenames:

- `outputs/models/logistic_regression.joblib`
- `outputs/models/random_forest.joblib`
- `outputs/models/dummy_most_frequent.joblib`
- `outputs/evaluation/logistic_regression_cv_results.csv`
- `outputs/evaluation/random_forest_cv_results.csv`
- `outputs/evaluation/selected_parameters.json`
- `outputs/evaluation/test_metrics.json`
- `outputs/evaluation/test_metrics.csv`
- `outputs/evaluation/per_class_metrics.csv`
- `outputs/evaluation/confusion_matrices.csv`
- `outputs/evaluation/predictions.csv`
- `outputs/evaluation/run_metadata.json`
- `outputs/evaluation/phase5_evaluation_report.md`

## 11. Phase 4 rules that stay in force

- 80/20 split, stratified on `Target`, `random_state=42`.
- Five-fold stratified cross-validation on the training portion only, through `make_training_cv()`.
- The raw CSV is not edited. The daytime/evening tab is stripped in memory.
- The feature matrix stays the approved 30 columns.
- These six columns stay out: `Debtor`, `Tuition fees up to date`, `Unemployment rate`, `Inflation rate`, `GDP`, and `Curricular units 2nd sem (without evaluations)`.
- `Target` is `y` only.
- Recorded semester grades of 0 stay numeric zero. There is no zero-grade sensitivity analysis.
- `Displaced`, `Educational special needs`, `Scholarship holder`, and `International` stay in the matrix under the unverified timing assumption. The final report must state that limitation.
- No derived features.
- Numerical columns are standardised only in the logistic pipeline.

## 12. Decision record

**Formally approved and frozen on 2026-11-15**

- RQ1, with Logistic Regression, Random Forest, and the most-frequent dummy.
- Logistic Regression `max_iter=2000`, `solver="lbfgs"`, and the 8-cell grid in section 2. Do not pass `penalty`.
- Random Forest `random_state=42`, `n_jobs=1`, and the 36-cell grid in section 3.
- `class_weight=None` compared with `class_weight="balanced"`. No resampling. Macro F1 is the selection metric.
- `GridSearchCV` with the Phase 4 training splitter, `scoring="f1_macro"`, `refit=True`, `error_score="raise"`, and `n_jobs=1`.
- Tie-break: the first configuration in the declared grid order.
- 220 cross-validation fits plus two training-set refits.
- Dummy strategy set explicitly to `"most_frequent"`, and not tuned.
- All three models evaluated independently on the untouched test set. No single winner.
- Metrics in section 8, with balanced accuracy and macro recall treated as one recall summary.
- No additional experiments.
- Later artefacts go under `outputs/models/` and `outputs/evaluation/`.

**Already approved in Phase 4, and not reopened**

- The 30-column matrix, the six exclusions, the zero-grade rule, and the four-feature timing assumption.
- The 80/20 stratified split and seed 42.
- Separate pipelines: scale numerical columns for Logistic Regression only.
- Class order Dropout, Enrolled, Graduate.

**Recorded after implementation**

- The filenames inside `outputs/models/` and `outputs/evaluation/` are the ones listed in section 10. The directories were already fixed. The methodology was not changed.

## 13. What this approval does not do

The experimental design remains formally approved and frozen. The 2026-11-15 implementation run fit the approved estimators and wrote `outputs/evaluation/phase5_evaluation_report.md`. The student reviewed and approved that implementation, the measured results, the evaluation metrics, the report, and the generated artefacts on 2026-11-15. Phase 5 — Model Development and Evaluation is complete. This text does not change a grid, a tie-break, or a metric. Measured scores stay in the evaluation files, not in this document.

The raw file, `src/preprocessing.py`, and `tests/test_preprocessing.py` were not edited by that run.
