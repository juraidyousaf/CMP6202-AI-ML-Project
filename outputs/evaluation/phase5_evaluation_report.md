# Phase 5 evaluation report

This report was written by `src/run_phase5.py` from the fitted estimators and their predictions. The experimental design was not changed. Phase 5 is not marked complete by this file.

Evaluation timestamp: `2026-11-15T19:45:33+05:00`.

## Methodology

The run reused the approved Phase 4 split and preprocessing in `src/preprocessing.py`. The split is an 80/20 stratified split on `Target` with `random_state=42`. Grid search used `make_training_cv()`: five-fold `StratifiedKFold`, `shuffle=True`, `random_state=42`, on the training portion only. Each search estimator was a pipeline, so every fold fit its own encoder and, for logistic regression, its own scaler.

Logistic Regression used `max_iter=2000` and `solver="lbfgs"`. `penalty` was not passed. Random Forest used `random_state=42` and `n_jobs=1`. Both searches used `scoring="f1_macro"`, `refit=True`, `error_score="raise"`, and `n_jobs=1`. The dummy baseline was `DummyClassifier(strategy="most_frequent")`, fit once on the training portion, with no grid.

The parameter grids were passed as one dictionary per declared configuration. That keeps `class_weight` changing fastest, which a single dictionary would not do for the forest because `ParameterGrid` sorts keys alphabetically. On an exact tie of mean validation macro F1, the earliest configuration in that declared list is kept. The installed scikit-learn assigns tied ranks with `method="min"` and `best_index_` is the first of those ranks. The run checked that this index was the first exact maximum. It did not fit an extra model to resolve a tie.

The test portion was not passed to `GridSearchCV.fit` and was not used to choose parameters, features, or preprocessing. `cv_results_` names the training-fold validation score `test_score`. Those values are not the 885-row holdout.

Class order for the confusion matrix and the per-class metrics is Dropout, Enrolled, Graduate. Balanced accuracy is the recall summary. In this three-class evaluation it equals macro recall, so macro recall is not listed as a separate result.

## Data checked during the run

- Raw SHA-256 before the run: `3ef126de5cefff26eb11fbb4237f1a1401cb64b488e2f1d598c23cedeb4c45ae`.
- Raw SHA-256 after the run: `3ef126de5cefff26eb11fbb4237f1a1401cb64b488e2f1d598c23cedeb4c45ae`.
- Training rows: 3539. Test rows: 885.
- Training class counts: {'Dropout': 1137, 'Enrolled': 635, 'Graduate': 1767}.
- Test class counts: {'Dropout': 284, 'Enrolled': 159, 'Graduate': 442}.
- Logistic scaler rows seen at the training refit: 3539.
- Forest numerical step is a scaler: False.
- scikit-learn version: `1.9.1`.

## Limitations carried from the approved plan

Displaced, Educational special needs, Scholarship holder, and International are retained although their individual UCI descriptions do not state a measurement date. Availability after the second semester is an unverified modelling assumption, not a confirmed date.

Recorded semester grades of 0 stayed numeric zero. Standardising numerical columns inside the logistic pipeline changes the units of that transformed matrix. It does not impute, replace, or drop those zeros, and this run is not a zero-grade sensitivity analysis.

## Cross-validation selection

The table below is the training-fold selection. It is not a test result, and it is not a ranking of the two algorithms against each other.

| Model | Declared order | Parameters | Mean CV macro F1 | Fold SD |
| --- | ---: | --- | ---: | ---: |
| Logistic Regression | 4 | `classifier__C`=`0.1`, `classifier__class_weight`=`balanced` | 0.688113 | 0.019914 |
| Random Forest | 14 | `classifier__class_weight`=`balanced`, `classifier__max_depth`=`20`, `classifier__min_samples_leaf`=`1`, `classifier__n_estimators`=`200` | 0.699806 | 0.012205 |

Logistic Regression: one configuration had the highest mean cross-validated macro F1. Declared index 3 (order 4) was selected.

Random Forest: one configuration had the highest mean cross-validated macro F1. Declared index 13 (order 14) was selected.

Completed logistic cross-validation fits: 40.
Completed forest cross-validation fits: 180.
Training-set refits: 2.
The dummy baseline is not included in those counts. It was fit once on the training portion.

Fold scores and the GridSearchCV standard deviation of those fold scores are in the cross-validation CSV files. That standard deviation is the square root of the mean squared deviation of the five fold scores.

## Test evaluation

Each fitted estimator predicted the same untouched test rows once. These three results are reported independently. This run does not select a single winning algorithm. The test scores were not used to change parameters, features, class weights, or preprocessing.

| Model | Macro F1 | Balanced accuracy | Macro precision | Accuracy |
| --- | ---: | ---: | ---: | ---: |
| Logistic Regression | 0.689290 | 0.702301 | 0.697566 | 0.727684 |
| Random Forest | 0.701691 | 0.701861 | 0.707986 | 0.754802 |
| Dummy most-frequent | 0.222055 | 0.333333 | 0.166478 | 0.499435 |

Scores in this markdown table are shown to 6 decimal places. The JSON file stores the measured floats.

### Confusion matrices

Rows are actual labels and columns are predicted labels, in the order Dropout, Enrolled, Graduate.

#### Logistic Regression

| Actual \ Predicted | Dropout | Enrolled | Graduate |
| --- | ---: | ---: | ---: |
| Dropout | 190 | 69 | 25 |
| Enrolled | 30 | 102 | 27 |
| Graduate | 16 | 74 | 352 |

#### Random Forest

| Actual \ Predicted | Dropout | Enrolled | Graduate |
| --- | ---: | ---: | ---: |
| Dropout | 197 | 54 | 33 |
| Enrolled | 32 | 86 | 41 |
| Graduate | 9 | 48 | 385 |

#### Dummy most-frequent

| Actual \ Predicted | Dropout | Enrolled | Graduate |
| --- | ---: | ---: | ---: |
| Dropout | 0 | 0 | 284 |
| Enrolled | 0 | 0 | 159 |
| Graduate | 0 | 0 | 442 |

### Per-class precision, recall, and F1

#### Logistic Regression

| Class | Precision | Recall | F1 | Support |
| --- | ---: | ---: | ---: | ---: |
| Dropout | 0.805085 | 0.669014 | 0.730769 | 284 |
| Enrolled | 0.416327 | 0.641509 | 0.504950 | 159 |
| Graduate | 0.871287 | 0.796380 | 0.832151 | 442 |

#### Random Forest

| Class | Precision | Recall | F1 | Support |
| --- | ---: | ---: | ---: | ---: |
| Dropout | 0.827731 | 0.693662 | 0.754789 | 284 |
| Enrolled | 0.457447 | 0.540881 | 0.495677 | 159 |
| Graduate | 0.838780 | 0.871041 | 0.854606 | 442 |

#### Dummy most-frequent

| Class | Precision | Recall | F1 | Support |
| --- | ---: | ---: | ---: | ---: |
| Dropout | 0.000000 | 0.000000 | 0.000000 | 284 |
| Enrolled | 0.000000 | 0.000000 | 0.000000 | 159 |
| Graduate | 0.499435 | 1.000000 | 0.666164 | 442 |

## Warnings recorded while fitting

No warnings were recorded during the three fits.

## Output files

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

No single test-set winner is designated in this report.
