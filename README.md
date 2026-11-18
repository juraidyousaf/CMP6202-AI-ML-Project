# CMP6202 AI & ML Project

Student ID: s24156365  
Repository: [CMP6202-AI-ML-Project](https://github.com/juraidyousaf/CMP6202-AI-ML-Project)

Coursework project for CMP6202 Artificial Intelligence and Machine Learning. This repository is a reproducible classical machine-learning study. It is not a deployed application.

Phases 0–5 are complete and approved. Phase 5 results are frozen. The saved models are under `outputs/models/`. The saved metrics, including the confusion matrices, are under `outputs/evaluation/`. The Phase 6 interpretation and evidence map in `docs/phase-6-results-interpretation.md` were reviewed on 2026-11-16. A local report draft is in `docs/phase-6-report-draft.md`. Phase 6 is not complete, the graded Word report and technical ZIP have not been created, and this copy has not been published as the final submission. This README does not claim that a clean third-party reproduction was checked.

## Project overview

The project studies one public dataset with a supervised classification workflow: audit, exploratory analysis, leakage-safe preprocessing, and the approved Phase 5 comparison.

The approved report title is Predicting Student Academic Outcomes Using Logistic Regression and Random Forest. The approved audience is academic and technical readers familiar with introductory machine learning. The local draft is not the submitted report. Seven other datasets were shortlisted as alternatives. Their names are not stored here, and they are not part of this project.

## Research problem

How effectively can Logistic Regression and Random Forest classify students into Dropout, Enrolled, and Graduate categories using enrolment, demographic, socioeconomic, and first- and second-semester academic information?

The prediction point is after the second semester. The approved feature set is the 30 columns retained by `src/preprocessing.py`. The target column is not an input.

UCI describes the records as coming from one higher education institution. The local draft records that limit. No fairness audit has been run.

RQ1 is the only approved predictive research question. Two descriptive EDA questions are approved and use the existing EDA evidence. Predictive modelling and descriptive EDA stay distinct. The earlier proposed RQ2 and RQ3 remain unapproved. The CMP6202 Assessment Brief 2026–27 and Individual Report Template 2026–27 were reviewed on 2026-11-16 and inspected on 2026-11-17. They are stored at the repository root as `CMP6202 Assessment Brief  2026-27.docx` and `CMP6202 Individual Report Template 2026-27.docx`. The brief sets a maximum of 3,000 words with a +10% tolerance only, up to 3,300 words. There is no lower tolerance. Headings, tables, citations, quotes, and lists in the main body count. Material before the body, and references, bibliographies, and appendices, do not. The graded Word report has not been created.

Five-fold training-only cross-validation is validation evidence. The 885-row holdout is the unseen test evidence. Cross-validation results are not training-set performance. Separate final-model training-set metrics were not produced. The verified comparison figure is `figures/model_comparison/figure_01_model_comparison_f1.png`, written by `src/plot_model_comparison.py` from the saved evaluation files. Panel A is five-fold training-only cross-validation macro F1 for the selected Logistic Regression and Random Forest. No dummy cross-validation score was saved, so none is shown. Panel B is holdout macro F1 for the dummy, Logistic Regression, and Random Forest. Panel C is holdout F1 for Dropout, Enrolled, and Graduate. The planned submission package is a separate Word report, a technical project ZIP, and the public GitHub link in the report. The final Moodle instructions have not been verified.

## Approved dataset

| Item | Record |
| --- | --- |
| Name | Predict Students' Dropout and Academic Success |
| Source | UCI Machine Learning Repository |
| Dataset ID | 697 |
| URL | https://archive.ics.uci.edu/dataset/697/predict |
| DOI | https://doi.org/10.24432/C5MC89 |
| Instances | UCI reports 4,424. The extracted file also measures 4,424 rows. |
| Features | UCI reports 36 input features. The extracted file measures 37 columns: 36 inputs plus `Target`. |
| Missing values | UCI reports none. The local audit also found 0 missing cells. |
| Archive | `data/raw/predict+students+dropout+and+academic+success.zip` (533,344 bytes), downloaded 2026-11-14 |
| Extracted file | `data/raw/data.csv` (533,230 bytes), extracted unchanged from that zip. Approved SHA-256: `3ef126de5cefff26eb11fbb4237f1a1401cb64b488e2f1d598c23cedeb4c45ae`. |
| Encoding and delimiter | UTF-8 with BOM, semicolon-separated. This was detected from the file. |

## Classification task

Multiclass classification.

- Target column: `Target`
- Classes: Dropout, Enrolled, Graduate
- There is no single positive class.
- The approved split is an 80/20 split, stratified on `Target`, with `random_state=42`. Training has 3,539 rows: Graduate 1,767, Dropout 1,137, and Enrolled 635. The holdout has 885 rows: Graduate 442, Dropout 284, and Enrolled 159. The student approved the split in Phase 4. UCI's example is not itself that approval.
- `src/preprocessing.py` creates the split in memory. It does not write a processed matrix.
- Measured class counts in `data/raw/data.csv`: Graduate 2,209 (49.9322%), Dropout 1,421 (32.1203%), Enrolled 794 (17.9476%). These are file counts, not model scores.
- Integer fields that store category codes are not automatically treated as continuous numbers.

## Models and evaluation

The approved comparison is recorded in `docs/phase-5-experimental-design.md`.

1. Logistic Regression, tuned by grid search on the training split.
2. Random Forest, tuned by grid search on the training split.
3. `DummyClassifier(strategy="most_frequent")`, fitted once on the training split and not tuned.

No third classifier is authorised. No single overall winner is authorised. The holdout was used after tuning, not to choose the settings.

Settings were chosen by five-fold stratified cross-validation on the 3,539 training rows only. The 885-row holdout was not used to choose a parameter, a feature, or a preprocessor. In the cross-validation files, `test_score` is a training-fold validation score, not the holdout and not training-set performance. Separate scores of the final models on the training rows were not produced.

The selected validation macro F1 was 0.688113 for Logistic Regression (`C=0.1`, `class_weight="balanced"`) and 0.699806 for Random Forest (200 trees, maximum depth 20, `min_samples_leaf=1`, `class_weight="balanced"`). The fold standard deviations were 0.019914 and 0.012205. No dummy cross-validation score was saved.

The saved holdout metrics, shown to 6 decimal places as in `outputs/evaluation/phase5_evaluation_report.md`, are:

| Model | Macro F1 | Balanced accuracy | Macro precision | Accuracy |
| --- | ---: | ---: | ---: | ---: |
| Logistic Regression | 0.689290 | 0.702301 | 0.697566 | 0.727684 |
| Random Forest | 0.701691 | 0.701861 | 0.707986 | 0.754802 |
| Dummy, most frequent | 0.222055 | 0.333333 | 0.166478 | 0.499435 |

`outputs/evaluation/test_metrics.json` stores the full measured floats. Balanced accuracy equals macro recall in this three-class evaluation. Accuracy is not the only metric, and neither tuned model is an overall winner. No numeric success threshold is set.

Inspect these saved files without fitting the models again:

- Models: `outputs/models/logistic_regression.joblib`, `outputs/models/random_forest.joblib`, and `outputs/models/dummy_most_frequent.joblib`.
- Holdout metrics: `outputs/evaluation/test_metrics.json` and `outputs/evaluation/test_metrics.csv`.
- Per-class precision, recall, and F1: `outputs/evaluation/per_class_metrics.csv`.
- Confusion matrices: `outputs/evaluation/confusion_matrices.csv`. Rows are the actual class and columns are the prediction, in the order Dropout, Enrolled, Graduate.
- Cross-validation: `outputs/evaluation/logistic_regression_cv_results.csv`, `outputs/evaluation/random_forest_cv_results.csv`, and `outputs/evaluation/selected_parameters.json`.
- Written summary: `outputs/evaluation/phase5_evaluation_report.md`.
- EDA figures: `figures/eda/figure_01_target_distribution.png` through `figures/eda/figure_07_numerical_correlation_heatmap.png`.
- Comparison figure: `figures/model_comparison/figure_01_model_comparison_f1.png`, plotted from the saved values by `src/plot_model_comparison.py`. Panel A is the two validation macro F1 means. Panel B is holdout macro F1 for all three models. Panel C is holdout F1 by class. The dummy is not in Panel A.

## Project structure

```text
CMP6202-AI-ML-Project/
├── CMP6202 Assessment Brief  2026-27.docx
├── CMP6202 Individual Report Template 2026-27.docx
├── README.md
├── requirements.txt
├── .gitignore
├── data/
│   ├── raw/          # original UCI zip and extracted data.csv; not ignored by Git
│   ├── interim/
│   └── processed/    # no model matrix is written here
├── notebooks/
│   └── 01_exploratory_data_analysis.ipynb
├── src/
│   ├── data_audit.py
│   ├── preprocessing.py
│   ├── model_training.py
│   ├── model_evaluation.py
│   ├── run_phase5.py
│   └── plot_model_comparison.py
├── tests/
├── figures/
│   ├── eda/          # seven EDA figures written by the notebook
│   └── model_comparison/
│       └── figure_01_model_comparison_f1.png
├── outputs/
│   ├── dataset_audit.md
│   ├── eda_report.md
│   ├── models/
│   └── evaluation/
├── docs/
└── references/
```

`docs/` holds the planning documents. They are not the graded report. `src/preprocessing.py`, `src/model_training.py`, and `src/model_evaluation.py` are imported by the runner and the tests. They are not separate command-line programs.

## Commands

To inspect the approved results, open the files listed above. Do not run `src/run_phase5.py` for that inspection.

`src/run_phase5.py` checks the raw-file hash, fits the approved grids, evaluates the 885-row holdout, and writes `outputs/models/` and `outputs/evaluation/`. The approved outputs from the 2026-11-15 run already exist. Running the script again overwrites those saved models and evaluation outputs. The script does not itself mark Phase 5 complete. The approval is recorded in `docs/Phases.md` and `docs/Memory.md`.

```powershell
python src/run_phase5.py
```

Run the other commands from the repository root after the environment in the next section is active. None of these scripts reads extra command-line arguments. This documentation update did not execute them again.

The audit reads `data/raw/data.csv` and writes `outputs/dataset_audit.md`. It does not edit the raw file. Running it again replaces that report.

```powershell
python src/data_audit.py
```

The notebook reads `data/raw/data.csv`, writes figures to `figures/eda/`, and does not modify the raw file. This command executes the notebook in place, so it can change the notebook and replace the figures.

```powershell
jupyter nbconvert --to notebook --execute --inplace notebooks/01_exploratory_data_analysis.ipynb
```

The tests recorded on 2026-11-15 were 27 passing tests. Discover them with:

```powershell
python -m unittest discover -s tests -v
```

`src/plot_model_comparison.py` reads the saved evaluation files and writes `figures/model_comparison/figure_01_model_comparison_f1.png`. It does not train or evaluate a model. The figure already exists. Running the script again replaces that figure. This documentation update did not run the script again.

```powershell
python src/plot_model_comparison.py
```

## Setup

The environment used for the recorded work was Python 3.13.7 on Windows. The project asks for Python 3.11 or a later compatible release. Whether a later session stays on 3.13.7 is still open.

From the repository root in PowerShell:

```powershell
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

On macOS or Linux, activate the environment with `source .venv/bin/activate` instead.

`requirements.txt` pins numpy, pandas, matplotlib, seaborn, scikit-learn, and jupyter. SciPy and joblib are installed because scikit-learn requires them. Do not install `ucimlrepo`. The dataset is already stored under `data/raw/`.

## Attribution and licence

The dataset citation used in the local report draft is:

Realinho, V., Vieira Martins, M., Machado, J. and Baptista, L. (2021) Predict Students' Dropout and Academic Success. [dataset] UCI Machine Learning Repository. Available at: https://doi.org/10.24432/C5MC89 [Accessed 14 November 2026].

**Licence status: quoted from the UCI dataset page on 2026-11-14.**

The page states: "This dataset is licensed under a Creative Commons Attribution 4.0 International (CC BY 4.0) license." It links to https://creativecommons.org/licenses/by/4.0/legalcode.

The raw files remain available to Git. `data/raw/` is not listed in `.gitignore`.

The official zip and UCI's direct `data.csv` URL are both on `archive.ics.uci.edu`, and they are not byte-identical. This project keeps the zip and the `data.csv` extracted from it. Details are in `outputs/dataset_audit.md`.
