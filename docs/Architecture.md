# Project Architecture

Internal planning document for CMP6202. This describes the machine-learning workflow and the repository layout. It does not describe a deployed software system.

Student ID: s24156365  
Repository name: CMP6202-AI-ML-Project

The dataset and task are selected. Planned models are named below and have not been trained. No result exists. Split ratio, `random_state`, and a third algorithm stay **TBD**.

Folders in the tree below are the intended layout. Create a folder when a phase needs it. Do not add empty placeholder trees "for later" unless a file is about to go in them. The dataset file is not in the repository yet. `data/raw/` must be created when that file is actually added.

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

**Leakage warning.** Split and preprocessing decisions must avoid data leakage. Fit transformers, feature-selection rules, and resampling on training data only. Choose hyperparameters with cross-validation on the training portion. Leave the test set unseen until the final evaluation of already chosen models. Do not use `Target` as an input. Use only information available by the end of the second semester. Which columns fail that rule is a Phase 2 check, not a finding recorded here.

How this lines up with the phase plan in `docs/Phases.md`:

- Baseline training records performance before tuning.
- Cross-validation and tuning select settings without using the test set.
- The test set is for the final comparison. An earlier look at the test set, if it happens, must not decide hyperparameters, and the report must disclose it.

Feature engineering may be "none", if EDA shows no justified transform. Record that decision rather than adding features for their own sake.

## 3. Proposed Repository Structure

Intended layout of `CMP6202-AI-ML-Project`:

```text
CMP6202-AI-ML-Project/
├── README.md
├── requirements.txt
├── .gitignore
├── docs/
│   ├── PRD.md
│   ├── Architecture.md
│   ├── Rules.md
│   ├── Phases.md
│   ├── Design.md
│   └── Memory.md
├── data/
│   ├── raw/
│   ├── interim/
│   └── processed/
├── notebooks/
│   ├── 01_data_understanding.ipynb
│   ├── 02_eda.ipynb
│   ├── 03_preprocessing.ipynb
│   ├── 04_model_training.ipynb
│   └── 05_model_evaluation.ipynb
├── src/
│   ├── data/
│   ├── features/
│   ├── models/
│   ├── evaluation/
│   └── utils/
├── figures/
├── outputs/
│   ├── metrics/
│   ├── models/
│   └── tables/
├── certificates/
├── report/
└── references/
```

Rules for this tree:

- Add a folder when the first real file needs it.
- Keep the five notebooks in that order. If a notebook is unnecessary after the dataset is known, document why it was merged or skipped. Do not renumber silently.
- `src/` holds reusable functions once logic is shared or worth testing. A short project may keep most steps in notebooks until duplication appears.
- `data/raw/` is immutable. Do not commit a huge file if the host or the licence makes a download step more appropriate. The README must still point at the exact source.
- `certificates/` stores real certification evidence only.
- `report/` holds the report source or export when writing starts. Do not draft the final report during planning.
- `references/` holds notes or exported citation details the student has actually used. Do not create placeholder citations.

## 4. File Responsibilities

| Location | Responsibility |
| --- | --- |
| `notebooks/` | The readable analysis path: load, EDA, preprocessing, training, evaluation. Each notebook starts with a short aim and ends with an interpretation. Notebooks call shared functions rather than pasting a second copy of the same cleaning code. |
| `src/` | Reusable Python: loading, validation, transforms, training helpers, metric tables. No notebook-only side effects hidden inside imports. |
| `data/raw/` | The original dataset file, or the exact file produced by the documented download. Never overwritten by cleaning. |
| `data/interim/` | Optional checkpoints between raw and model-ready data (for example after type fixes, before the model matrix). Safe to regenerate. |
| `data/processed/` | The model-ready outputs of the leakage-safe pipeline, if saving them helps reproduction. Prefer rebuilding them with a script or notebook over hand-edited files. |
| `figures/` | Report-ready charts exported by code, using the names in `docs/Design.md`. |
| `outputs/` | Saved metrics, comparison tables, and persisted models. These files are evidence. They are produced by a run, not typed by hand. |
| `docs/` | Planning and working-state documents: requirements, architecture, rules, phases, visual standards, and `Memory.md`. These are not the graded report. |
| `report/` | The coursework report and any figures pasted into it. Numbers in the report must match `outputs/` and `figures/`. |

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
- Set `random_state` on the splitter and on estimators that use it. Record the seed next to the split description. The seed and the test fraction are still **TBD** for Phase 5.
- Use a stratified split on `Target`. UCI says the creators used 80% train and 20% test. That ratio is not adopted until Phase 5 records it.
- Treat integer feature codes as categorical unless a recorded reason says a particular integer column is continuous or ordinal. UCI's own variable table marks many integer columns as coded categories.
- UCI reports no missing values. Still inspect the loaded file before imputing. Do not skip that inspection because the repository page says none.
- If rows are removed, record how many, why, and whether the removal rule was chosen using training data only.
- The other seven shortlisted datasets stay unused. Their names are not stored in this file. Do not load one of them as a second project dataset.

## 7. Model Architecture

The task is multiclass classification. The planned pair matches the original pattern and the approved research question. Nothing in this section has been fit.

1. **Planned baseline** — multinomial Logistic Regression, as the interpretable linear classifier. It has not been trained.
2. **Planned second algorithm** — Random Forest, from a different model family. It has not been trained.
3. **Optional third algorithm** — **TBD**. Add one only if EDA shows a gap the first two leave open.
4. **Tune only after baseline evaluation** — record untuned results first. Then search a small, stated hyperparameter space with cross-validation on the training data.

EDA can still challenge this pair before Phase 6. Do not treat the research question's wording as permission to skip that review. The preferred model, once results exist, is the one the evidence supports for the stated audience and metrics. It is not automatically Random Forest. No preferred model exists yet.

## 8. Reproducibility Architecture

The repository is reproducible when all of the following are true:

- `requirements.txt` lists the packages and versions used for the reported run.
- `README.md` gives setup commands, the data location or exact source link, the licence, and the execution order.
- Random seeds are fixed where they affect results, and the seed value is written down.
- Code uses paths relative to the repository root. There are no absolute Windows or personal home-directory paths.
- There is a single documented execution order (the numbered notebooks, or a script that replaces them).
- The dataset source URL and licence are in the README and in the data dictionary. The approved source is https://archive.ics.uci.edu/dataset/697/predict, DOI https://doi.org/10.24432/C5MC89, licence CC BY 4.0. The README and data dictionary do not exist yet.
- Environment setup commands in the README match what a clean machine must run.
- Saved outputs can be regenerated by that order. Hand-edited metric files are not evidence.

Suggested README sections, to be written when code exists, not during this planning step:

1. Project title and one-paragraph aim.
2. Dataset name, source URL, licence, and retrieval date.
3. Python version and install command.
4. Where to put the raw file if it is not downloaded by a script.
5. Notebook or script order.
6. Where figures and metric tables are written.
7. Student ID and a pointer to the AI-use declaration.
