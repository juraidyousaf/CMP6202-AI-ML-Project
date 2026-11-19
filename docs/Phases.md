# Project Phases and Milestones

Task-oriented roadmap for CMP6202. Check a box only when the artefact exists and has been verified. Leaving a box open is correct while the work is unfinished.

Student ID: s24156365  
Repository: CMP6202-AI-ML-Project

The dataset, task type, and target are selected. Logistic Regression, Random Forest, and the most-frequent dummy baseline were trained and evaluated under the frozen Phase 5 design. Measured scores are in `outputs/evaluation/`. Do not complete later phases by assuming new results, class counts, or a different split.

**Leakage rule after approved Phase 5.** The frozen run used the 885-row holdout once, after grid search on the training portion only. Those test scores must not be used to change parameters, features, preprocessing, or the model set. The historical Phase 6–8 modelling checklists below are not active and must not be executed.

---

## Phase 0 — Planning & Repository Setup

- [x] Create repository structure — `data/raw/`, `data/interim/`, `data/processed/`, `notebooks/`, `src/`, `figures/`, `outputs/`, and `references/` exist. They are empty apart from `.gitkeep`. The dataset file is not in `data/raw/`. This sentence describes the repository at setup on 2026-11-14. The dataset, notebook, figures, and model outputs were added in later approved phases.
- [x] Create documentation files (`docs/PRD.md`, `docs/Architecture.md`, `docs/Rules.md`, `docs/Phases.md`, `docs/Design.md`, `docs/Memory.md`) — student stated on 2026-11-14 that Phase 0 is complete and approved
- [x] Create README — `README.md` added 2026-11-14
- [x] Create `.gitignore` — Python environment, caches, checkpoints, and secret files. `data/raw/` is not ignored.
- [x] Decide Python environment — Python 3.13.7, virtual environment at `.venv/`, direct packages pinned in `requirements.txt`

**Exit criteria:** Planning docs reviewed and approved by the student. README and `.gitignore` exist. The Phase 1 dataset is a real UCI dataset, not a placeholder.

**Decision status:** The student stated on 2026-11-14 that Phase 0 is complete and approved. The setup files and environment exist.

## Phase 1 — Dataset & Problem Selection

Dataset-selection decision recorded on 2026-11-14. This phase is not fully closed. The report audience and title were decided on 2026-11-17. The earlier proposed RQ2 and RQ3 remain unapproved. The seven other shortlisted datasets stay alternatives. Their names were not supplied in the documentation update, so they are not listed here.

- [x] Shortlist candidate open-access datasets — active dataset selected; seven alternatives retained but not named in these files
- [x] Verify an open-access licence for the preferred dataset — CC BY 4.0, as approved for UCI 697
- [x] Confirm the row count is at least 3,000 (about 3,000–5,000 recommended) — UCI reports 4,424; the local file is not measured yet. That clause described Phase 1 before the file was audited. Phase 2, met on 2026-11-14, measured 4,424 rows by 37 columns in `outputs/dataset_audit.md`.
- [x] Identify the target variable — `Target`
- [x] Choose classification or regression from that target — multiclass classification
- [x] Identify one explicit target audience for the report — approved on 2026-11-17: academic and technical readers familiar with introductory machine learning
- [ ] Formulate 2–3 research questions the data can answer — the report presentation is resolved: predictive RQ1 beside two descriptive EDA questions. That presentation does not guarantee that the descriptive questions satisfy the brief's count. The earlier proposed RQ2 and RQ3 remain unapproved.
- [x] Define a provisional project title — approved on 2026-11-17: Predicting Student Academic Outcomes Using Logistic Regression and Random Forest

**Exit criteria:** Dataset and problem formally selected. Source URL, licence, row count, target, task type, audience, and research questions are written down from real sources. Status in `docs/Memory.md` updated.

**Decision status:** The dataset decision is complete and approved: UCI 697, CC BY 4.0, target `Target`, multiclass classification, recorded on 2026-11-14. The report audience and title were approved on 2026-11-17. At the dataset decision, RQ1 was the only approved research question. On 2026-11-16 the student approved two descriptive EDA questions in addition to RQ1. The earlier proposed RQ2 and RQ3 remain unapproved. The report presentation of predictive RQ1 beside the two descriptive questions is resolved. That presentation does not guarantee that the descriptive questions satisfy the brief's two-or-three research-question requirement. Do not mark Phase 1 fully complete.

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

RQ2 and RQ3 were proposed on 2026-11-14 and are not approved. At that date, RQ1 was the only approved research question. Two descriptive EDA questions were approved later, on 2026-11-16. The proposed RQ2 and RQ3 remain unapproved.

- [x] Univariate analysis of the target and key features — notebook executed 2026-11-14
- [x] Bivariate analysis against the target — notebook executed 2026-11-14
- [x] Multivariate analysis where it informs the question — numerical correlation heatmap
- [x] Relevant plots, labelled and saved — seven figures in `figures/eda/`
- [x] Statistical summaries saved or clearly printed — notebook outputs and `outputs/eda_report.md`
- [x] Evidence linked back to the research questions — RQ2 and RQ3 marked proposed, not approved
- [x] EDA conclusions written from those outputs — `outputs/eda_report.md`

**Exit criteria:** Conclusions cite actual tables or figures. Logistic Regression and Random Forest are the planned pair. This phase must say whether that pair still stands after the data are explored. Training does not start here.

**Decision status:** Complete. The student reviewed and approved Phase 3 on 2026-11-15. The notebook, seven figures, and `outputs/eda_report.md` stand. At that approval, RQ1 was the only approved research question, and RQ2 and RQ3 stayed proposed and unapproved. The planned model pair still stands. At Phase 3 approval, no preprocessing, train/test split, training, or tuning had started. That sentence describes 2026-11-15 at the EDA review. Preprocessing was later approved in Phase 4, and training was later approved in Phase 5. On 2026-11-16 two descriptive EDA questions were approved. The earlier proposed RQ2 and RQ3 remain unapproved.

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

**Decision status:** Complete. The student reviewed the implementation and approved Phase 4 on 2026-11-15. Methodology remains frozen. `src/preprocessing.py` is the path, and `tests/test_preprocessing.py` passed 13 tests. Missing cells stay unimputed. Duplicate rows and outlier rows are not removed: the audited duplicate count is 0, and the frozen plan does not authorise an outlier filter. No derived features were added. The raw file hash was unchanged. The in-memory split has 3,539 training rows and 885 test rows. Training class counts are Graduate 1,767, Dropout 1,137, and Enrolled 635. Test class counts are Graduate 442, Dropout 284, and Enrolled 159. These are split counts, not model scores. At Phase 4 approval, no classifier had been trained. That sentence describes 2026-11-15 at the preprocessing review. The approved classifiers were later fit in Phase 5.

## Phase 5 — Experimental Design

The approved working name is Phase 5 — Model Development and Evaluation. The checklist below is the design gate. Its implementation and results were approved with it on 2026-11-15.

- [x] Define the train/test strategy, including test size and `random_state`, with a stratified split on `Target`
- [x] Define the baseline algorithm
- [x] Select a minimum of two algorithms from different families
- [x] Confirm the planned metrics: macro F1, precision, recall, balanced accuracy, accuracy, and a confusion matrix. There is no single positive class.
- [x] Justify the algorithms in writing
- [x] Justify the metrics in writing

**Exit criteria:** A short experimental-design note exists before the final test evaluation is treated as evidence.

**Decision status:** Complete and approved on 2026-11-15. The student reviewed and approved the implementation, model results, evaluation metrics, report, and generated artefacts. The design in `docs/phase-5-experimental-design.md` stays frozen and was not changed: the 8-cell logistic grid (40 CV fits plus one refit), the 36-cell forest grid (180 CV fits plus one refit), `n_jobs=1` on both the forest and `GridSearchCV`, `error_score="raise"`, tie-break by declared grid order, independent test evaluation with no single winner, and output directories `outputs/models/` and `outputs/evaluation/`. `.\.venv\Scripts\python.exe -m unittest discover -s tests -v` passed 27 tests. `.\.venv\Scripts\python.exe src\run_phase5.py` exited 0 and completed 220 cross-validation fits, two training-set refits, and one Dummy baseline fit. Both tuned models and the baseline were evaluated independently on the untouched test set. Measured scores remain in `outputs/evaluation/phase5_evaluation_report.md`. No single winner was designated.

## Phase 6 — Results Interpretation and Coursework Report Preparation

**Status:** Started on 2026-11-15. Not complete. The student reviewed and approved `docs/phase-6-results-interpretation.md` on 2026-11-16, including the interpretation and the evidence map. The inspected template has nested contents. The 13 content headings are mapped to those contents entries in `docs/phase-6-report-outline.md`. RQ1 remains the only approved predictive research question. Two descriptive EDA questions are approved and mapped to existing EDA evidence. The earlier proposed RQ2 and RQ3 remain unapproved. The workstream boxes below stay unchecked because this phase is still open: no report has been drafted. Report-preparation decisions were recorded on 2026-11-17, and unresolved report requirements remain. Do not mark this phase complete from this heading.

**Objective.** Interpret the approved Phase 5 evidence and prepare a coursework report outline. Do not repeat Phase 5 modelling.

**Scope.** Training-fold cross-validation results, kept separate from the 885-row test results. The three saved test evaluations, with no overall winner. Per-class precision, recall, and F1. Confusion-matrix error patterns. Existing EDA findings as associations, not causes. The frozen preprocessing and experimental design. Limitations already required by the approved documents. A map from report sections to existing files.

**Workstreams**

- [ ] Interpret the saved cross-validation results as training-fold scores, not as holdout scores
- [ ] Compare the three saved test evaluations without naming a winner
- [ ] Interpret per-class precision, recall, and F1
- [ ] Discuss the saved confusion matrices and error patterns
- [ ] Interpret `outputs/eda_report.md` without causal claims
- [ ] Explain the frozen preprocessing and experimental-design decisions
- [ ] State the approved limitations, including undated binary features, zero grades, excluded columns, and the absence of coefficient, importance, and fairness experiments
- [ ] Map the Phase 10 report sections to existing evidence and prepare a report outline

**Deliverables.** The approved interpretation and evidence map is `docs/phase-6-results-interpretation.md`. It cites saved files and does not add a score. It is not the graded report. No report has been drafted.

**Dependencies.** `docs/phase-4-preprocessing-plan.md`, `docs/phase-5-experimental-design.md`, `outputs/eda_report.md`, and `outputs/evaluation/`. The CMP6202 Assessment Brief 2026–27 and Individual Report Template 2026–27 were reviewed on 2026-11-16 and inspected again on 2026-11-17. Both files are at the repository root: `CMP6202 Assessment Brief  2026-27.docx` and `CMP6202 Individual Report Template 2026-27.docx`. The brief sets a maximum of 3,000 words with a +10% margin only; nothing beyond that margin is marked. Page 1 also says 3,000 words excluding references. The word-count section includes headings, tables, citations, quotes, and lists in the main body, and it excludes material before the body and references, bibliographies, and appendices. It does not state a lower margin. The brief also requires 11-point font, 1.5 line spacing, anonymous marking by student number only, BCU Harvard referencing, a cover sheet completed and appended, and the printed deadline fields 4th December 2026 and 03:00PM. On 2026-11-17 the approved preparation package became a separate Word report, a technical project ZIP, and the public GitHub link in the report. The final Moodle instructions have not been verified. The report has not been drafted.

**Risks.** Naming a winner, adding feature importance or coefficients, rerunning Phase 5, or editing generated evaluation files to change their completion flags would break the frozen record.

**Exit criteria.** Every interpretive sentence cites an existing file. Cross-validation and holdout results stay distinct. Balanced accuracy is the only recall summary. No new score, model, feature, or parameter exists. The student reviews the writing before any completion checkbox is marked.

## Superseded historical tasks — do not execute.

Baseline training, hyperparameter tuning, and the independent holdout evaluation were completed in approved Phase 5 on 2026-11-15. The three checklists below are the earlier roadmap. They are not active work. Their boxes stay unchecked so this file does not record those old phase numbers as separately completed. Written interpretation from the old Phase 7 list belongs to the active Phase 6 above. That interpretation and evidence map were reviewed and approved on 2026-11-16. These historical boxes stay unchecked. Feature-engineering experiments and a single final-model choice in the old Phase 8 list are not authorised by the frozen design.

### Historical Phase 6 — Baseline Model Development

- [ ] Train model 1 (baseline)
- [ ] Train model 2
- [ ] Train an optional model 3, only if justified
- [ ] Save baseline metrics from the run
- [ ] Compare baseline behaviour in words tied to those metrics

**Historical exit criteria:** Untuned results are saved before any tuning run overwrites them. The approved Phase 5 design did not save a separate untuned Logistic Regression or Random Forest. The fitted untuned baseline is the most-frequent dummy. Do not create the missing untuned scores now.

### Historical Phase 7 — Evaluation

- [ ] Evaluate the chosen models on the held-out test set (final pass, after tuning choices are frozen)
- [ ] Produce a confusion matrix or residual analysis, as appropriate to the task
- [ ] Build a comparison table
- [ ] Interpret the table in plain language
- [ ] Perform error analysis on where the models fail

**Historical exit criteria:** Every reported test metric is traceable to a saved output. The holdout metrics, confusion matrices, and comparison table already exist under `outputs/evaluation/`. Interpretation and error analysis are active Phase 6 work, not a reason to evaluate again.

### Historical Phase 8 — Improvement

- [ ] Run cross-validation on the training data
- [ ] Tune hyperparameters without using the test set
- [ ] Run feature-engineering experiments only where EDA supports them
- [ ] Compare tuned models with the baseline on the same metrics
- [ ] Choose a final model and state the selection rule

**Historical exit criteria:** The selection rule was fixed before reading the final test comparison, or any deviation is disclosed as a limitation. Cross-validation and tuning were completed inside approved Phase 5. No further feature-engineering experiment is approved. The frozen design does not authorise a single overall winner.

## Phase 9 — Certification & Reflection

- [ ] Complete the selected AI/ML certifications
- [ ] Save certificates or badge evidence in `certificates/` or record a stable link
- [ ] Write short learning notes
- [ ] Record technical challenges
- [ ] Record how those challenges were solved
- [ ] Record limitations of the data, method, and results

**Exit criteria:** Certification files are real. Reflection notes refer to this project's actual blockers and results. Which certifications to take remains an open student decision until selected.

## Phase 10 — Report

Write the report from project outputs. This phase has not started, and no report has been drafted. The inspected brief and template are at the repository root. The brief sets a maximum of 3,000 words with a +10% margin only. Page 1 also says 3,000 words excluding references. Headings, tables, citations, quotes, and lists in the main body count. Material before the body, and references, bibliographies, and appendices, do not. The brief does not state a lower margin. It also requires 11-point font, 1.5 line spacing, anonymous marking by student number only, BCU Harvard referencing, a cover sheet completed and appended, and the printed deadline fields 4th December 2026 and 03:00PM. The template contents are nested. The 13 content headings are mapped to those contents entries in `docs/phase-6-report-outline.md`. The evidence for those headings remains in `docs/phase-6-results-interpretation.md`. The checklist below is the earlier planning list and stays unchecked. Do not name a single winning model. The frozen Phase 5 design does not authorise that conclusion. The approved preparation package is a separate Word report, a technical project ZIP, and the public GitHub link in the report. The final Moodle instructions have not been verified.

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

**Phase 5 — Model Development and Evaluation is complete, approved, and frozen on 2026-11-15. Phase 6 started on 2026-11-15 and remains open. The interpretation and evidence map were reviewed and approved on 2026-11-16. No report has been drafted. Phases 9–12 have not started.**

Phase 4 preprocessing remains complete and approved. Its frozen methodology and `src/preprocessing.py` stand. The Phase 5 design in `docs/phase-5-experimental-design.md` remains frozen and was not changed. The student approved the implementation, the 220 cross-validation fits, the two training-set refits, the one Dummy baseline fit, the independent test evaluation of both tuned models, the 27 passing tests, and the generated model and evaluation artefacts. RQ1 remains the only approved predictive research question. Two descriptive EDA questions were approved on 2026-11-16 and are mapped to existing EDA evidence. The earlier proposed RQ2 and RQ3 remain unapproved. The report title and audience were approved on 2026-11-17. The active Phase 6 is Results Interpretation and Coursework Report Preparation. Its approved note is `docs/phase-6-results-interpretation.md`. The historical Phase 6–8 modelling checklists are not active. The official brief and report template were reviewed on 2026-11-16. On 2026-11-17 both files were inspected and are stored at the repository root as `CMP6202 Assessment Brief  2026-27.docx` and `CMP6202 Individual Report Template 2026-27.docx`.
