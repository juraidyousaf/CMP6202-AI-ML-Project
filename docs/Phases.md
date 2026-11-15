# Project Phases and Milestones

Task-oriented roadmap for CMP6202. Check a box only when the artefact exists and has been verified. Leaving a box open is correct while the work is unfinished.

Student ID: s24156365  
Repository: CMP6202-AI-ML-Project

The dataset, task type, and target are selected. Logistic Regression, Random Forest, and the most-frequent dummy baseline were trained and evaluated under the frozen Phase 5 design. Measured scores are in `outputs/evaluation/`. Do not complete later phases by assuming new results, class counts, or a different split.

**Leakage-safe reading of Phases 6–8.** Phase 6 trains baselines and records training or validation metrics. Hyperparameter and feature choices in Phase 8 use cross-validation on the training data only. The held-out test set is for final evaluation. If an interim test score is computed early, it must not be used to pick hyperparameters, and the report must say that the test set was inspected early.

---

## Phase 0 — Planning & Repository Setup

- [x] Create repository structure — `data/raw/`, `data/interim/`, `data/processed/`, `notebooks/`, `src/`, `figures/`, `outputs/`, and `references/` exist. They are empty apart from `.gitkeep`. The dataset file is not in `data/raw/`.
- [x] Create documentation files (`docs/PRD.md`, `docs/Architecture.md`, `docs/Rules.md`, `docs/Phases.md`, `docs/Design.md`, `docs/Memory.md`) — student stated on 2026-11-14 that Phase 0 is complete and approved
- [x] Create README — `README.md` added 2026-11-14
- [x] Create `.gitignore` — Python environment, caches, checkpoints, and secret files. `data/raw/` is not ignored.
- [x] Decide Python environment — Python 3.13.7, virtual environment at `.venv/`, direct packages pinned in `requirements.txt`

**Exit criteria:** Planning docs reviewed and approved by the student. README and `.gitignore` exist. The Phase 1 dataset is a real UCI dataset, not a placeholder.

**Decision status:** The student stated on 2026-11-14 that Phase 0 is complete and approved. The setup files and environment exist.

## Phase 1 — Dataset & Problem Selection

Dataset-selection decision recorded on 2026-11-14. This phase is not fully closed. Audience, provisional title, and a second research question remain open. The seven other shortlisted datasets stay alternatives. Their names were not supplied in the documentation update, so they are not listed here.

- [x] Shortlist candidate open-access datasets — active dataset selected; seven alternatives retained but not named in these files
- [x] Verify an open-access licence for the preferred dataset — CC BY 4.0, as approved for UCI 697
- [x] Confirm the row count is at least 3,000 (about 3,000–5,000 recommended) — UCI reports 4,424; the local file is not measured yet
- [x] Identify the target variable — `Target`
- [x] Choose classification or regression from that target — multiclass classification
- [ ] Identify one explicit target audience for the report
- [ ] Formulate 2–3 research questions the data can answer — one question is approved; further questions are open
- [ ] Define a provisional project title

**Exit criteria:** Dataset and problem formally selected. Source URL, licence, row count, target, task type, audience, and research questions are written down from real sources. Status in `docs/Memory.md` updated.

**Decision status:** The dataset-selection part of this exit criterion is met. Audience, title, and the requested second or third research question are not met. Do not mark this phase fully complete.

## Phase 2 — Dataset Understanding

- [x] Load the dataset with a reproducible relative path or documented download — official zip downloaded 2026-11-14; `data/raw/data.csv` extracted unchanged
- [x] Inspect shape (rows and columns) and record the measured counts — 4,424 rows by 37 columns
- [x] Inspect the schema (names and dtypes) — recorded in `outputs/dataset_audit.md`
- [x] Build a data dictionary — column dictionary in `outputs/dataset_audit.md`, using the UCI variable descriptions
- [x] Inspect missing values — 0 missing cells
- [x] Inspect duplicates — 0 duplicate column names and 0 fully duplicate rows
- [x] Inspect the target (type, balance or distribution, obvious coding issues) — Graduate 2,209; Dropout 1,421; Enrolled 794
- [x] Identify initial risks (leakage, imbalance, leakage-prone columns, unclear fields) — recorded in the audit; no columns were removed

**Exit criteria:** A data dictionary and a short risk list exist, based on this file, not on a generic description from the web. UCI's reported shape, missing-value flag, and class imbalance are inputs to check, not substitutes for this inspection. Confirm which integer columns are category codes, and which columns would not have been known by the end of the second semester.

**Decision status:** Met on 2026-11-14. The dictionary, class counts, missing-value check, and prediction-time flags are in `outputs/dataset_audit.md`, produced by `src/data_audit.py` from `data/raw/data.csv`. Uncertain fields were flagged and not removed.

## Phase 3 — Exploratory Data Analysis

RQ2 and RQ3 were proposed on 2026-11-14 and are not approved. RQ1 remains the only approved research question.

- [x] Univariate analysis of the target and key features — notebook executed 2026-11-14
- [x] Bivariate analysis against the target — notebook executed 2026-11-14
- [x] Multivariate analysis where it informs the question — numerical correlation heatmap
- [x] Relevant plots, labelled and saved — seven figures in `figures/eda/`
- [x] Statistical summaries saved or clearly printed — notebook outputs and `outputs/eda_report.md`
- [x] Evidence linked back to the research questions — RQ2 and RQ3 marked proposed, not approved
- [x] EDA conclusions written from those outputs — `outputs/eda_report.md`

**Exit criteria:** Conclusions cite actual tables or figures. Logistic Regression and Random Forest are the planned pair. This phase must say whether that pair still stands after the data are explored. Training does not start here.

**Decision status:** Complete. The student reviewed and approved Phase 3 on 2026-11-15. The notebook, seven figures, and `outputs/eda_report.md` stand. RQ1 remains the only approved research question. RQ2 and RQ3 stay proposed and are not approved. The planned model pair still stands. No preprocessing, train/test split, training, or tuning has started.

## Phase 4 — Preprocessing & Feature Engineering

- [x] Decide missing-value treatment and record counts
- [x] Decide duplicate treatment and record counts
- [x] Decide outlier treatment and justify it
- [x] Encode categorical variables in a leakage-safe way, including integer codes that are categories rather than continuous measurements
- [x] Scale numeric features where the chosen algorithms need it
- [x] Engineer features only where justified; otherwise record "none"
- [x] Apply feature selection only if justified
- [x] Build a leakage-safe pipeline (`Pipeline` / `ColumnTransformer`, or an equivalent explicit fit on train only)

**Exit criteria:** Raw data is unchanged. The preprocessing path can be refit from the training split alone.

**Decision status:** Complete. The student reviewed the implementation and approved Phase 4 on 2026-11-15. Methodology remains frozen. `src/preprocessing.py` is the path, and `tests/test_preprocessing.py` passed 13 tests. Missing cells stay unimputed. Duplicate rows and outlier rows are not removed: the audited duplicate count is 0, and the frozen plan does not authorise an outlier filter. No derived features were added. The raw file hash was unchanged. The in-memory split has 3,539 training rows and 885 test rows. Training class counts are Graduate 1,767, Dropout 1,137, and Enrolled 635. Test class counts are Graduate 442, Dropout 284, and Enrolled 159. These are split counts, not model scores. No classifier was trained.

## Phase 5 — Experimental Design

- [x] Define the train/test strategy, including test size and `random_state`, with a stratified split on `Target`
- [x] Define the baseline algorithm
- [x] Select a minimum of two algorithms from different families
- [x] Confirm the planned metrics: macro F1, precision, recall, balanced accuracy, accuracy, and a confusion matrix. There is no single positive class.
- [x] Justify the algorithms in writing
- [x] Justify the metrics in writing

**Exit criteria:** A short experimental-design note exists before the final test evaluation is treated as evidence.

**Decision status:** Complete and approved on 2026-11-15. The student reviewed and approved the implementation, model results, evaluation metrics, report, and generated artefacts. The design in `docs/phase-5-experimental-design.md` stays frozen and was not changed: the 8-cell logistic grid (40 CV fits plus one refit), the 36-cell forest grid (180 CV fits plus one refit), `n_jobs=1` on both the forest and `GridSearchCV`, `error_score="raise"`, tie-break by declared grid order, independent test evaluation with no single winner, and output directories `outputs/models/` and `outputs/evaluation/`. `.\.venv\Scripts\python.exe -m unittest discover -s tests -v` passed 27 tests. `.\.venv\Scripts\python.exe src\run_phase5.py` exited 0 and completed 220 cross-validation fits, two training-set refits, and one Dummy baseline fit. Both tuned models and the baseline were evaluated independently on the untouched test set. Measured scores remain in `outputs/evaluation/phase5_evaluation_report.md`. No single winner was designated.

## Phase 6 — Baseline Model Development

- [ ] Train model 1 (baseline)
- [ ] Train model 2
- [ ] Train an optional model 3, only if justified
- [ ] Save baseline metrics from the run
- [ ] Compare baseline behaviour in words tied to those metrics

**Exit criteria:** Untuned results are saved before any tuning run overwrites them.

## Phase 7 — Evaluation

- [ ] Evaluate the chosen models on the held-out test set (final pass, after tuning choices are frozen)
- [ ] Produce a confusion matrix or residual analysis, as appropriate to the task
- [ ] Build a comparison table
- [ ] Interpret the table in plain language
- [ ] Perform error analysis on where the models fail

**Exit criteria:** Every reported test metric is traceable to a saved output. Interpretation does not go beyond that output.

## Phase 8 — Improvement

- [ ] Run cross-validation on the training data
- [ ] Tune hyperparameters without using the test set
- [ ] Run feature-engineering experiments only where EDA supports them
- [ ] Compare tuned models with the baseline on the same metrics
- [ ] Choose a final model and state the selection rule

**Exit criteria:** The selection rule was fixed before reading the final test comparison, or any deviation is disclosed as a limitation.

## Phase 9 — Certification & Reflection

- [ ] Complete the selected AI/ML certifications
- [ ] Save certificates or badge evidence in `certificates/` or record a stable link
- [ ] Write short learning notes
- [ ] Record technical challenges
- [ ] Record how those challenges were solved
- [ ] Record limitations of the data, method, and results

**Exit criteria:** Certification files are real. Reflection notes refer to this project's actual blockers and results. Which certifications to take remains an open student decision until selected.

## Phase 10 — Report

Write the report at about 3,000 words from project outputs. Do not start it as a substitute for missing experiments.

- [ ] Introduction
- [ ] Exploratory data analysis
- [ ] Experimental design
- [ ] Model development
- [ ] Evaluation and improvements
- [ ] Conclusion
- [ ] Reflection
- [ ] GitHub link
- [ ] References in BCU Harvard style
- [ ] Generative-AI declaration

**Exit criteria:** Each result section points at repository outputs. References were opened. The AI declaration matches `docs/Memory.md`.

## Phase 11 — Reproducibility & GitHub Finalisation

- [ ] Clean the repository of secrets, caches, and dead files
- [ ] Pin or declare dependencies in `requirements.txt`
- [ ] Update the README so it matches the real run steps
- [ ] Include run instructions a third party can follow
- [ ] Document the dataset file or the exact source link and licence
- [ ] Verify the repository is public
- [ ] Run the notebooks cleanly in order from a documented environment

**Exit criteria:** A clean run reproduces the saved figures and metric tables.

## Phase 12 — Submission QA

- [ ] Verify Student ID s24156365 is used where the submission requires it
- [ ] Remove the student name from the report if the submission is anonymous
- [ ] Remove leftover template or prompt text, including red instruction text from any official template
- [ ] Verify every reference
- [ ] Verify the GitHub link opens the public repository
- [ ] Verify figures are the ones generated by the project and are readable
- [ ] Verify the report word count against the module limit
- [ ] Verify formatting against the official template
- [ ] Make a final backup of the repository and the report export

**Exit criteria:** The submission pack matches the repository, and no placeholder, invented statistic, or unverified citation remains.

---

## Current Phase

**Phase 5 — Model Development and Evaluation is complete and approved on 2026-11-15. No later phase has been started.**

Phase 4 preprocessing remains complete and approved. Its frozen methodology and `src/preprocessing.py` stand. The Phase 5 design in `docs/phase-5-experimental-design.md` remains frozen and was not changed. The student approved the implementation, the 220 cross-validation fits, the two training-set refits, the one Dummy baseline fit, the independent test evaluation of both tuned models, the 27 passing tests, and the generated model and evaluation artefacts. RQ1 is the only approved research question. RQ2 and RQ3 remain proposed. Report audience and provisional title remain open. Phase 6 and later phases are not started.
