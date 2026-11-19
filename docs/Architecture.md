# Project Architecture

Internal planning document for CMP6202. This describes the machine-learning workflow and the repository layout. It does not describe a deployed software system.

Student ID: s24156365  
Repository name: CMP6202-AI-ML-Project

The dataset and task are selected. Phases 0–5 are complete and approved. Phase 3 exploratory analysis, Phase 4 preprocessing, and Phase 5 model development and evaluation are complete. Logistic Regression and Random Forest were tuned and evaluated. The most-frequent dummy classifier is the baseline. The approved split is 80/20, stratified on `Target`, with `random_state=42`. A third competitive classifier is closed. Phase 5 results are frozen in `outputs/evaluation/`. No single overall winner was approved. Phase 6 is results interpretation and coursework report preparation. It remains open, and no report has been drafted.

The audited dataset is already in `data/raw/`. Do not edit those raw files.

---

## 1. Architecture Principles

- **Reproducibility** — a third party can recreate tables and figures from the README, the declared dependencies, and the saved data or its exact source.
- **Separation of raw and processed data** — `data/raw/` is the untouched source. Cleaning and transforms write to `data/interim/` or `data/processed/`.
- **Separation of concerns** — exploratory analysis, preprocessing, training, and evaluation stay in distinct notebooks or modules so a change in one step is visible.
- **Configuration where useful** — paths, split ratio, seed, and the target column name `Target` live in one obvious place once the ratio and seed are chosen. They are not copied as slightly different literals across notebooks.
- **No hidden manual steps** — a click, a spreadsheet edit, or an undocumented filter must not be required to obtain the reported result. If a manual step is unavoidable, the README states it.
- **Outputs generated from code** — figures and metric tables that appear in the report are written by the notebooks or scripts.

## 2. End-to-End Project Flow

```text
Problem Definition
        ↓
Dataset Selection
        ↓
License Verification
        ↓
Raw Data
        ↓
Initial Inspection
        ↓
EDA
        ↓
Data Cleaning
        ↓
Feature Engineering
        ↓
Train/Test Split
        ↓
Model Training
        ↓
Cross-Validation
        ↓
Hyperparameter Tuning
        ↓
Evaluation
        ↓
Model Comparison
        ↓
Interpretation
        ↓
Figures / Tables
        ↓
Report + Reflection
```

**Leakage warning.** Split and preprocessing decisions must avoid data leakage. Fit transformers, feature-selection rules, and resampling on training data only. Choose hyperparameters with cross-validation on the training portion. Leave the test set unseen until the final evaluation of already chosen models. Do not use `Target` as an input. Use only information available by the end of the second semester. The column check is recorded in `outputs/dataset_audit.md` and `docs/phase-4-preprocessing-plan.md`. Six unresolved columns stay excluded. Do not add a feature without a documented reason.

How this lines up with the approved phases in `docs/Phases.md`:

- The most-frequent dummy is the untuned baseline. The approved design did not save a separate untuned Logistic Regression or Random Forest.
- Logistic Regression and Random Forest were tuned with `GridSearchCV` and five-fold stratified cross-validation on the training data only, then refit on the full training portion.
- The 885-row test set was used once after those settings were frozen. It must not be used to change parameters, features, or preprocessing.

Feature engineering may be "none", if EDA shows no justified transform. Record that decision rather than adding features for their own sake.

## 3. Repository Structure

Current layout of the files that exist in this repository:

```text
CMP6202-AI-ML-Project/
├── CMP6202 Assessment Brief  2026-27.docx
├── CMP6202 Individual Report Template 2026-27.docx
├── README.md
├── requirements.txt
├── .gitignore
├── docs/
│   ├── PRD.md
│   ├── Architecture.md
│   ├── Rules.md
│   ├── Phases.md
│   ├── Design.md
│   ├── Memory.md
│   ├── phase-4-preprocessing-plan.md
│   ├── phase-5-experimental-design.md
│   ├── phase-6-results-interpretation.md
│   └── phase-6-report-outline.md
├── data/
│   └── raw/
│       ├── data.csv
│       └── predict+students+dropout+and+academic+success.zip
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
│   ├── test_preprocessing.py
│   ├── test_model_training.py
│   └── test_model_evaluation.py
├── figures/
│   ├── eda/
│   └── model_comparison/
│       └── figure_01_model_comparison_f1.png
├── outputs/
│   ├── dataset_audit.md
│   ├── eda_report.md
│   ├── models/
│   └── evaluation/
└── references/
```

`data/interim/` and `data/processed/` exist. They do not hold a saved model matrix. The approved split is created in memory by `src/preprocessing.py`.

Rules for this tree:

- `data/raw/` is immutable. The README points at the stored file and its UCI source.
- `src/` holds the audit, preprocessing, training, evaluation, the Phase 5 runner, and `src/plot_model_comparison.py`. The tests import the modelling modules. The plotting script only reads saved evaluation files.
- `figures/eda/` holds the seven exploratory figures written by the notebook.
- `figures/model_comparison/figure_01_model_comparison_f1.png` is the verified comparison figure. Panel A is selected Logistic Regression and Random Forest five-fold training-only cross-validation macro F1. No dummy cross-validation score was saved. Panel B is holdout macro F1 for the dummy, Logistic Regression, and Random Forest. Panel C is holdout F1 for Dropout, Enrolled, and Graduate.
- `outputs/models/` holds the three fitted estimators. `outputs/evaluation/` holds the saved Phase 5 metrics and reports.
- `references/` holds citation notes the student has actually used. Do not create placeholder citations. It currently contains only `.gitkeep`.
- `CMP6202 Assessment Brief  2026-27.docx` and `CMP6202 Individual Report Template 2026-27.docx` are the inspected official documents at the repository root. They are planning sources, not model inputs.
- `docs/phase-6-results-interpretation.md` is the approved Phase 6 interpretation. `docs/phase-6-report-outline.md` is the report outline. Neither file is the graded report.
- Do not draft the coursework report in this architecture note. Phase 6 remains open.

## 4. File Responsibilities

| Location | Responsibility |
| --- | --- |
| `notebooks/` | The exploratory notebook, `notebooks/01_exploratory_data_analysis.ipynb`. It reads the raw file and writes the EDA figures. It does not train the models. |
| `src/` | The audit, the leakage-safe preprocessing, the training and evaluation functions, `src/run_phase5.py`, and `src/plot_model_comparison.py`. |
| `data/raw/` | The original dataset file, or the exact file produced by the documented download. Never overwritten by cleaning. |
| `data/interim/` | Optional checkpoints between raw and model-ready data (for example after type fixes, before the model matrix). Safe to regenerate. |
| `data/processed/` | The model-ready outputs of the leakage-safe pipeline, if saving them helps reproduction. Prefer rebuilding them with a script or notebook over hand-edited files. |
| `figures/` | Charts exported by code. The exploratory figures are in `figures/eda/`. The comparison figure is `figures/model_comparison/figure_01_model_comparison_f1.png`. |
| `outputs/` | `outputs/dataset_audit.md`, `outputs/eda_report.md`, fitted models in `outputs/models/`, and Phase 5 evidence in `outputs/evaluation/`. These files are produced by a run, not typed by hand. |
| `docs/` | Planning and working-state documents: requirements, architecture, rules, phases, visual standards, and `Memory.md`. Phase 6 planning is `docs/phase-6-results-interpretation.md` and `docs/phase-6-report-outline.md`. These are not the graded report. |
| Repository root | `CMP6202 Assessment Brief  2026-27.docx` and `CMP6202 Individual Report Template 2026-27.docx`. Inspected on 2026-11-17. They are not model inputs. |
| Coursework report | Not drafted. There is no `report/` directory. When the report is written, its numbers must match `outputs/` and `figures/`. |

`README.md` is the front door: purpose, dataset source, setup, and run order. `requirements.txt` lists the libraries needed to run that order. `.gitignore` keeps caches, virtual environments, secrets, and oversized temporary files out of Git.

## 5. Tech Stack

Use a conservative Python machine-learning stack. Add a library only when a concrete step needs it.

**Core**

- Python 3.11+, or a stable version compatible with the pinned packages if 3.11 is unavailable on the student's machine. Record the actual version in the README once the environment exists.
- Jupyter Notebook or JupyterLab, for the documented analysis sequence.
- pandas, for tables and data inspection.
- numpy, for numerical work that pandas and scikit-learn rely on.
- scikit-learn, for splits, pipelines, classical models, metrics, cross-validation, and tuning.
- matplotlib, for figures.

**Conditional**

- seaborn, only if it makes a statistical chart clearer than matplotlib alone.
- scipy, if a required statistical test or distribution function is not already covered by the core stack.
- imbalanced-learn, only if measured class imbalance shows that ordinary training would be misleading, and the report explains that choice.
- joblib, if a fitted pipeline or model must be saved and reloaded.

**Development**

- Git and GitHub, for history and the public submission repository.
- VS Code or Cursor, as the editor. The project must still run without Cursor.

Do not add a framework that this coursework does not need. The avoid-list and the justification rule are in `docs/Rules.md`.

The library set above is decided. Exact package versions are chosen when the environment is created and recorded in `requirements.txt`. The dataset choice does not reopen the decision to use pandas, numpy, scikit-learn, and matplotlib.

## 6. Data Flow and Leakage Prevention

Intended flow once a dataset exists:

```text
source URL / local raw file
        ↓
data/raw/                     (unchanged)
        ↓
inspection + EDA              (read-only on raw, or copies)
        ↓
cleaning decisions            (documented)
        ↓
train / test split            (before fitting transforms)
        ↓
fit preprocessing on train
        ↓
transform train and test
        ↓
fit and tune models on train
        ↓
one final evaluation on test
        ↓
figures/ and outputs/
```

Required practices:

- Preserve the raw dataset unchanged. Write derived data elsewhere.
- Fit imputers, scalers, encoders, feature selectors, and resampling on training data only. Apply those fitted objects to the test data.
- The test set remains unseen until final evaluation. It is not a pool for trying ideas.
- Use scikit-learn `Pipeline` and `ColumnTransformer` where they make the fit/transform boundary explicit. A manual split is acceptable only if the same boundary is obvious in the code.
- Set `random_state` on the splitter and on estimators that use it. The approved split is 80/20, stratified on `Target`, with `random_state=42`. UCI's example is not itself that approval.
- Use a stratified split on `Target`. Do not replace the approved split.
- Treat integer feature codes as categorical unless a recorded reason says a particular integer column is continuous or ordinal. UCI's own variable table marks many integer columns as coded categories.
- UCI reports no missing values. Still inspect the loaded file before imputing. Do not skip that inspection because the repository page says none.
- If rows are removed, record how many, why, and whether the removal rule was chosen using training data only.
- The other seven shortlisted datasets stay unused. Their names are not stored in this file. Do not load one of them as a second project dataset.

## 7. Model Architecture

The task is multiclass classification. RQ1 is the only approved predictive research question. The two approved EDA questions are descriptive. The earlier proposed RQ2 and RQ3 remain unapproved. The approved comparison has been fit under `docs/phase-5-experimental-design.md`.

1. **Baseline** — `DummyClassifier(strategy="most_frequent")`, fitted once on the training portion and not tuned.
2. **Tuned logistic model** — Logistic Regression, selected by `GridSearchCV` on the training folds and refit on the training portion.
3. **Tuned forest** — Random Forest, selected by the same training-only search and refit on the training portion.
4. **No third competitive classifier** — closed by the frozen design. Do not add one.

The search used five-fold stratified cross-validation on the training data only. The 885-row test set was predicted once after the searches finished. No single overall winner was approved. Phase 6 may interpret the saved results. It must not refit the models or choose a winner from the test scores.

## 8. Reproducibility Architecture

The repository is reproducible when all of the following are true:

- `requirements.txt` lists the packages and versions used for the reported run.
- `README.md` gives setup commands, the data location or exact source link, the licence, and the execution order.
- Random seeds are fixed where they affect results, and the seed value is written down.
- Code uses paths relative to the repository root. There are no absolute Windows or personal home-directory paths.
- There is a documented execution order in `README.md`: the audit, the exploratory notebook, the tests, and `src/run_phase5.py`. `src/plot_model_comparison.py` redraws the saved comparison figure and does not refit the models.
- The dataset source URL and licence are in the README and in `outputs/dataset_audit.md`. The approved source is https://archive.ics.uci.edu/dataset/697/predict, DOI https://doi.org/10.24432/C5MC89, licence CC BY 4.0.
- Environment setup commands in the README match what a clean machine must run.
- Saved outputs can be regenerated by that order. Hand-edited metric files are not evidence. Rerunning `src/run_phase5.py` would replace the approved outputs, so that command is not a casual refresh.

The README already contains:

1. Project title and one-paragraph aim.
2. Dataset name, source URL, licence, and retrieval date.
3. Python version and install command.
4. Where to put the raw file if it is not downloaded by a script.
5. Notebook or script order.
6. Where figures and metric tables are written.
7. Student ID and a pointer to the AI-use declaration.
