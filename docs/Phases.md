# Project Phases and Milestones

Task-oriented roadmap for CMP6202. Check a box only when the artefact exists and has been verified. Leaving a box open is correct while the work is unfinished.

Student ID: s24156365  
Repository: CMP6202-AI-ML-Project

Dataset, task type, target, algorithms, and metrics are **TBD — to be decided after dataset selection.** Do not complete later phases by assuming those choices.

**Leakage-safe reading of Phases 6–8.** Phase 6 trains baselines and records training or validation metrics. Hyperparameter and feature choices in Phase 8 use cross-validation on the training data only. The held-out test set is for final evaluation. If an interim test score is computed early, it must not be used to pick hyperparameters, and the report must say that the test set was inspected early.

---

## Phase 0 — Planning & Repository Setup

- [ ] Create repository structure (only the folders a real file needs)
- [x] Create documentation files (`docs/PRD.md`, `docs/Architecture.md`, `docs/Rules.md`, `docs/Phases.md`, `docs/Design.md`, `docs/Memory.md`) — drafted 2026-10-17; student approval still open
- [ ] Create README skeleton
- [ ] Create `.gitignore`
- [ ] Decide Python environment later (record the version when it is created)

**Exit criteria:** Planning docs reviewed and approved by the student. README skeleton and `.gitignore` exist. No dataset has been pretended into existence.

## Phase 1 — Dataset & Problem Selection

- [ ] Shortlist candidate open-access datasets
- [ ] Verify an open-access licence for the preferred dataset
- [ ] Confirm the row count is at least 3,000 (about 3,000–5,000 recommended)
- [ ] Identify the target variable
- [ ] Choose classification or regression from that target
- [ ] Identify one explicit target audience for the report
- [ ] Formulate 2–3 research questions the data can answer
- [ ] Define a provisional project title

**Exit criteria:** Dataset and problem formally selected. Source URL, licence, row count, target, task type, audience, and research questions are written down from real sources. Status in `docs/Memory.md` updated.

## Phase 2 — Dataset Understanding

- [ ] Load the dataset with a reproducible relative path or documented download
- [ ] Inspect shape (rows and columns) and record the measured counts
- [ ] Inspect the schema (names and dtypes)
- [ ] Build a data dictionary
- [ ] Inspect missing values
- [ ] Inspect duplicates
- [ ] Inspect the target (type, balance or distribution, obvious coding issues)
- [ ] Identify initial risks (leakage, imbalance, leakage-prone columns, unclear fields)

**Exit criteria:** A data dictionary and a short risk list exist, based on this file, not on a generic description from the web.

## Phase 3 — Exploratory Data Analysis

- [ ] Univariate analysis of the target and key features
- [ ] Bivariate analysis against the target
- [ ] Multivariate analysis where it informs the question
- [ ] Relevant plots, labelled and saved
- [ ] Statistical summaries saved or clearly printed
- [ ] Evidence linked back to the research questions
- [ ] EDA conclusions written from those outputs

**Exit criteria:** Conclusions cite actual tables or figures. Algorithm choice is still open until these conclusions exist.

## Phase 4 — Preprocessing & Feature Engineering

- [ ] Decide missing-value treatment and record counts
- [ ] Decide duplicate treatment and record counts
- [ ] Decide outlier treatment and justify it
- [ ] Encode categorical variables in a leakage-safe way
- [ ] Scale numeric features where the chosen algorithms need it
- [ ] Engineer features only where justified; otherwise record "none"
- [ ] Apply feature selection only if justified
- [ ] Build a leakage-safe pipeline (`Pipeline` / `ColumnTransformer`, or an equivalent explicit fit on train only)

**Exit criteria:** Raw data is unchanged. The preprocessing path can be refit from the training split alone.

## Phase 5 — Experimental Design

- [ ] Define the train/test strategy, including test size and `random_state`
- [ ] Define the baseline algorithm
- [ ] Select a minimum of two algorithms from different families
- [ ] Define the metrics and the positive class or error units
- [ ] Justify the algorithms in writing
- [ ] Justify the metrics in writing

**Exit criteria:** A short experimental-design note exists before the final test evaluation is treated as evidence.

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

**Phase 0 — Planning & Repository Setup**

The six planning documents exist under `docs/` and still need student review. README skeleton, `.gitignore`, and the Python environment are not done. Later phases are not started. No dataset is selected.
