# Implementation Memory and Working State

Living project state for CMP6202. Update this file after every meaningful work session. A later AI agent should read this file before changing the repository.

Student-facing rule: never mark work complete unless it exists and has been verified.

**Memory update rule.** Whenever implementation changes meaningfully, update all of the following sections before ending the session:

- Current Status
- Current Phase
- Current Task
- Current File Being Worked On
- Completed
- In Progress
- Next Actions
- Decisions Made
- Files Created
- Issues / Blockers
- AI Assistance Log
- Session Handoff

The dataset decision is closed. If a later value is unknown, write **TBD**. Do not invent a score, class count, citation, split ratio, or certificate.

---

## 1. Project Identity

| Field | Value |
| --- | --- |
| Module | CMP6202 Artificial Intelligence and Machine Learning |
| Repository | CMP6202-AI-ML-Project |
| Student ID | s24156365 |
| Workspace folder at time of writing | `CMP6202-AI-ML` (local working copy). The GitHub repository name to use is `CMP6202-AI-ML-Project`. |

## 2. Current Status

Dataset selected: Predict Students' Dropout and Academic Success, UCI dataset 697. Phase 3 EDA was reviewed and approved on 2026-11-15. Target counts remain Graduate 2,209 (49.9322%), Dropout 1,421, and Enrolled 794. RQ1 is the only approved research question. RQ2 and RQ3 are proposed and not approved. Phase 4 preprocessing was reviewed and approved as complete on 2026-11-15. The methodology stays frozen in `docs/phase-4-preprocessing-plan.md`, and the path is `src/preprocessing.py`. Phase 5 — Model Development and Evaluation is complete and approved on 2026-11-15. The experimental design was formally approved and frozen on 2026-11-15 and was not changed. The implementation and independent test evaluation were completed on 2026-11-15: 27 tests passed, 220 cross-validation fits, two training-set refits, and one Dummy baseline fit. The student approved the measured results and the generated artefacts in `outputs/models/` and `outputs/evaluation/`. No later phase has been started.

## 3. Current Phase

Phase 4 — complete and approved on 2026-11-15. Phase 5 — Model Development and Evaluation is complete and approved on 2026-11-15. The experimental design remains frozen. No later phase has been started.

## 4. Current Task

None. Phase 5 is complete and approved on 2026-11-15. Do not start Phase 6 or any later phase until the student asks. Do not change the frozen design or the measured results.

## 5. Current File Being Worked On

`docs/Phases.md`, `docs/Memory.md`, and the status lines of `docs/phase-5-experimental-design.md`. No source file, test, dataset, model, or evaluation output was edited.

## 6. Completed

Items marked done from the student's own start-of-project notes are labelled as student-reported. This session did not independently verify the GitHub account.

- [x] GitHub account created (student-reported; not re-verified in this session)
- [x] Repository name selected: CMP6202-AI-ML-Project (student-reported)
- [x] Coursework requirements reviewed (student-reported, and reflected in `docs/PRD.md`)
- [x] Documentation architecture planned
- [x] Six planning documents drafted in `docs/` (files exist on disk; student approval of the original draft text is still open)
- [x] Phase 1 dataset-selection decision recorded on 2026-11-14 (UCI 697). This does not close audience, title, or a second research question.
- [x] Phase 0 setup files created on 2026-11-14: `README.md`, `.gitignore`, `requirements.txt`, `.venv/`, and the project folders. The student stated that Phase 0 is complete and approved.
- [x] Phase 2 audit on 2026-11-14. Official zip preserved. `src/data_audit.py` exited 0 and wrote `outputs/dataset_audit.md`. `ucimlrepo` was not installed.
- [x] EDA notebook executed on 2026-11-14. Seven figures saved. Report written.
- [x] Phase 3 reviewed and approved on 2026-11-15. RQ1 remains the only approved research question. RQ2 and RQ3 were not approved.
- [x] Phase 4 reviewed and approved as complete on 2026-11-15. The frozen methodology was not changed.
- [x] Phase 5 — Model Development and Evaluation reviewed and approved as complete on 2026-11-15. The frozen experimental design was not changed. 27 tests passed. The run completed 220 cross-validation fits, two training-set refits, and one Dummy baseline fit. Both tuned models were evaluated independently on the untouched test set. The student approved the generated model and evaluation artefacts.

## 7. In Progress

- [ ] Approval decision for proposed RQ2 and RQ3
- [ ] Remaining writing items: one explicit report audience and a provisional title
- [ ] Names of the seven alternative datasets, if they are to be stored in the repository

## 8. Next Actions

1. Do not start Phase 6 or any later phase until the student asks. Keep the frozen Phase 5 design and the measured results unchanged.
2. Carry the approved modelling notes below into later writing. The full-data Graduate share of 49.9322% is still not a model score. The dummy test metrics are separate and are stored in `outputs/evaluation/test_metrics.json`.
3. Keep `data/raw/data.csv` and the zip unchanged. The second-semester "without evaluations" wording stays unresolved.

## 9. Decisions Made

| Date | Decision | Reason |
| --- | --- | --- |
| 2026-10-17 | The repository will be public. | Coursework requires a public GitHub repository. |
| 2026-10-17 | A personal GitHub account is acceptable. | Student decision recorded at planning start. |
| 2026-10-17 | The final dataset had not been selected at that date. | Historical planning decision. Superseded on 2026-11-14. |
| 2026-11-14 | Active dataset: Predict Students' Dropout and Academic Success, UCI ID 697, CC BY 4.0, DOI https://doi.org/10.24432/C5MC89. | Student-approved Phase 1 selection. UCI reports 4,424 instances and 36 features. |
| 2026-11-14 | Task: multiclass classification. Target: `Target`. Classes: Dropout, Enrolled, Graduate. Prediction point: after the second semester. | Follows the approved research question and the UCI task definition. |
| 2026-11-14 | Planned models: Logistic Regression, then Random Forest. Planned metrics: macro F1, precision, recall, balanced accuracy, accuracy, and a confusion matrix. | Named in the approved plan. Not trained. No scores exist. EDA can still challenge the pair. |
| 2026-11-14 | The split must be stratified. Ratio and `random_state` are not chosen. UCI's 80/20 example is not adopted. | Prevents an unapproved split from being copied out of the UCI notes. |
| 2026-11-14 | Seven other shortlisted datasets remain alternatives only. | Their names were not included in this update, so they are not written here. |
| 2026-10-17 | The final report will not be generated until the ML work is sufficiently complete. | The report must be built from real outputs. These markdown files are planning documents only. |
| 2026-10-17 | The default modelling stack is Python with pandas, numpy, scikit-learn, and matplotlib. | Conservative coursework stack. Other libraries need a written justification. See `docs/Rules.md`. |
| 2026-10-17 | No numeric success threshold will be set before a baseline exists. | A threshold would be an invented target. See `docs/PRD.md` section 8. |
| 2026-11-14 | Initial environment is Python 3.13.7 in `.venv/`, with numpy 2.5.4, pandas 3.1.1, matplotlib 3.11.2, seaborn 0.13.2, scikit-learn 1.9.1, and jupyter 1.1.1. | Versions were read from the environment after installation. seaborn is included because this setup task required it. `ucimlrepo` was not installed. |
| 2026-11-14 | Raw data is the official UCI zip and the unmodified `data.csv` extracted from it. | Direct UCI `data.csv` URL was also downloaded for comparison, differed in delimiter and header text, and was not kept. |
| 2026-11-14 | Local audit: 4,424 rows, 37 columns, 0 missing cells, 0 duplicate rows. Target: Graduate 2,209; Dropout 1,421; Enrolled 794. | Counts come from `src/data_audit.py` run against `data/raw/data.csv`. |
| 2026-11-14 | RQ2 and RQ3 are proposed only. They are not approved. | The student labelled them pending approval. |
| 2026-11-14 | EDA used the original file in memory. Seven figures were saved. The planned model pair was not trained. | `jupyter nbconvert --execute` finished with exit code 0. Raw SHA-256 was unchanged. |
| 2026-11-15 | Phase 3 EDA was reviewed and approved. | Student review of the notebook, seven figures, and `outputs/eda_report.md`. |
| 2026-11-15 | Modelling notes from that review: debtor and tuition dates are unknown; macroeconomic reference dates are unknown; a semester grade of 0 must not automatically be treated as missing; matching semester features are strongly correlated; balanced accuracy and macro recall are equivalent for this multiclass task; the majority-class share is about 49.93% (Graduate, 49.9322%). | Recorded for later design. No model has been trained, so these are not performance scores. |
| 2026-11-15 | Provisionally retain `Displaced`, `Educational special needs`, `Scholarship holder`, and `International`. | Student Option A. Their individual UCI descriptions do not give measurement dates. Retention assumes the dataset narrative makes them available after the second semester. That date is not verified. The final report must state the assumption. |
| 2026-11-15 | Keep recorded semester grade zeros as numeric zero. Exclude a zero-grade sensitivity analysis from the initial implementation. | Student decision. The meaning of 0 remains ambiguous. Do not impute, replace, or drop rows because of those zeros. |
| 2026-11-15 | Phase 4 methodology approved and frozen. Supersedes the 2026-11-14 note that the split ratio and seed were unchosen. | Student approval of the six remaining decisions: dated features retained and the six unresolved columns excluded; encoding fixed; no derived features; 80/20 stratified split with seed 42 and 5-fold stratified cross-validation on the training data; most-frequent dummy baseline and the metric list; scaling for Logistic Regression only. The four provisional binaries and the zero-grade rule stay in force. Completion of Phase 4 is recorded in the next row. |
| 2026-11-15 | Implement the frozen preprocessing path without training a model. | `src/preprocessing.py` selects 30 features, splits 3,539/885 with seed 42, and builds unfitted logistic and forest preprocessors. Tests passed, 13 of 13. Raw SHA-256 was unchanged. |
| 2026-11-15 | Phase 4 is complete and approved. Current phase is Phase 5 — Model Development and Evaluation, and its implementation has not started. | The student reviewed and verified the preprocessing implementation. The frozen methodology was not changed. No model was trained. |
| 2026-11-15 | Phase 5 configuration decisions, later frozen the same day. | Student approval of the grids, `max_iter=2000`, `solver="lbfgs"`, forest `random_state=42`, `n_jobs=1` on the forest and on `GridSearchCV`, `refit=True`, `error_score="raise"`, tie-break by declared grid order, no single winner, and output directories `outputs/models/` and `outputs/evaluation/`. Planned size: 40 + 180 = 220 CV fits, plus two training-set refits. Not run. |
| 2026-11-15 | Phase 5 experimental design formally approved and frozen. Implementation had not started when this row was written. | The student marked `docs/phase-5-experimental-design.md` final. The grids, fit counts, tie-break, metrics, and evaluation rules were not changed. |
| 2026-11-15 | Implement the frozen Phase 5 design and leave the phase open for review. | The student asked for the training run. `src/run_phase5.py` completed 40 logistic and 180 forest cross-validation fits, two training refits, and one dummy fit. Test scores were not used to change parameters. Phase 5 was not marked complete at that point. |
| 2026-11-15 | Phase 5 — Model Development and Evaluation is complete and approved. | The student reviewed and approved the implementation, model results, evaluation metrics, report, and generated artefacts. 27 tests had passed. The run had completed 220 cross-validation fits, two training-set refits, and one Dummy baseline fit. Both tuned models were evaluated independently on the untouched test set. The frozen design was not changed. No later phase was started. |

## 10. Open Decisions

Closed by the 2026-11-14 decision: dataset, task type, and target column. The items below are still open.

- Further research questions beyond the one approved question
- RQ2 and RQ3, which remain proposed and are not approved
- A third algorithm, if any
- The final model-selection rule
- Certifications to complete
- Project / report title
- Explicit report target audience
- Whether later analysis stays on Python 3.13.7 or moves to another 3.11+ release
- Names of the seven alternative datasets

## 11. Files Created

| Path | Purpose | Status |
| --- | --- | --- |
| `docs/PRD.md` | Requirements, selected problem, open decisions | Updated 2026-11-14 for the dataset decision; pending student review |
| `docs/Architecture.md` | ML workflow, planned models, leakage rules | Updated 2026-11-14; no code added |
| `docs/Rules.md` | Engineering and dataset-specific constraints | Updated 2026-11-14 |
| `docs/Phases.md` | Checkbox roadmap; Phase 1 dataset items checked | Updated 2026-11-14; phase not fully closed |
| `docs/Design.md` | Chart rules, including three-class labels | Updated 2026-11-14; no figures created |
| `docs/Memory.md` | Living project state | Updated 2026-11-14 after Phase 0 setup |
| `README.md` | Project overview, dataset, setup, and licence caveat | Created 2026-11-14 |
| `.gitignore` | Virtual environment, caches, checkpoints, and secrets. Does not ignore `data/raw/`. | Created 2026-11-14 |
| `requirements.txt` | Pinned direct dependencies measured from `.venv` | Created 2026-11-14 |
| `.venv/` | Local Python 3.13.7 environment | Created 2026-11-14; ignored by Git |
| `data/raw/predict+students+dropout+and+academic+success.zip` | Official UCI archive, 533,344 bytes, downloaded 2026-11-14 | Preserved |
| `data/raw/data.csv` | Unmodified extract from that zip, 533,230 bytes | Audited; not cleaned |
| `src/data_audit.py` | Read-only audit script | Run on 2026-11-14, exit code 0 |
| `outputs/dataset_audit.md` | Measured audit findings | Generated by the script |
| `notebooks/01_exploratory_data_analysis.ipynb` | Executed EDA notebook | Ran 2026-11-14, exit code 0 |
| `outputs/eda_report.md` | EDA findings from that run | Reviewed and approved 2026-11-15 |
| `docs/phase-4-preprocessing-plan.md` | Frozen Phase 4 methodology. | Methodology unchanged. Status note updated 2026-11-15 when the student approved Phase 4 as complete. |
| `docs/phase-5-experimental-design.md` | Frozen Phase 5 experimental design. | Formally approved and frozen on 2026-11-15. The student approved the implementation and results on 2026-11-15. Grids and rules were not changed. |
| `src/preprocessing.py` | Approved feature selection, split, and unfitted preprocessors. | Added 2026-11-15. Not modified by the Phase 5 run. |
| `src/model_training.py` | Approved estimators, grids, and training-only search. | Added 2026-11-15. |
| `src/model_evaluation.py` | Test metrics, confusion matrices, and the report text. | Added 2026-11-15. |
| `src/run_phase5.py` | Runs the frozen experiment and writes the outputs. | Exit code 0 on 2026-11-15. |
| `tests/test_preprocessing.py` | Checks for leakage, exclusions, zeros, split, and scaling. | Included in the 27-test suite on 2026-11-15. |
| `tests/test_model_training.py` | Grid order, tie-break, leakage, failure, and output checks. | Included in the 27-test suite on 2026-11-15. |
| `tests/test_model_evaluation.py` | Hand-calculated metrics and class order. | Included in the 27-test suite on 2026-11-15. |
| `outputs/models/` | Fitted logistic, forest, and dummy pipelines. | Written by the 2026-11-15 run and approved by the student the same day. |
| `outputs/evaluation/` | CV tables, test metrics, predictions, and the evaluation report. | Written by the 2026-11-15 run and approved by the student the same day. Scores were not typed by hand. |
| `figures/eda/` | Seven EDA figures | Written by the notebook |
| `data/interim/` | Future intermediate data | Empty |
| `data/processed/` | Future model-ready data | Empty |
| `notebooks/` | Future analysis notebooks | Empty |
| `src/` | Shared Python modules | Contains the audit, preprocessing, training, evaluation, and Phase 5 runner. |
| `figures/` | EDA figures | `figures/eda/` holds the seven EDA figures. |
| `outputs/` | Audit, EDA, and Phase 5 results | Contains `dataset_audit.md`, `eda_report.md`, `models/`, and `evaluation/`. |
| `references/` | Future checked citation notes | Empty |

Not created, on purpose: `ucimlrepo`, processed datasets, and the graded report. Fitted model files now exist under `outputs/models/`.

## 12. Experimental Results

Phase 5 scores from 2026-11-15 are recorded below. They were copied from the run outputs. The full-data Graduate share of 49.9322% remains a class share, not a model score.

Verified file audit on 2026-11-14, from `src/data_audit.py`:

- 4,424 data rows and 37 columns in `data/raw/data.csv`.
- Target counts: Graduate 2,209 (49.9322%), Dropout 1,421 (32.1203%), Enrolled 794 (17.9476%).
- Missing cells: 0. Fully duplicate rows: 0. Duplicate column names: none.

EDA run on 2026-11-14, from `notebooks/01_exploratory_data_analysis.ipynb`:

- Mean second-semester units approved: Dropout 1.940, Enrolled 4.058, Graduate 6.177.
- Mean second-semester grade: Dropout 5.899, Enrolled 11.117, Graduate 12.697.
- Every zero semester grade occurs with zero units approved in that semester: 718 rows in semester 1 and 870 in semester 2.
- Tuition fees not up to date: 528 students, of whom 86.55% are in the Dropout class. The measurement date is still unknown.

Approved split created in memory on 2026-11-15 by `prepare_from_raw()` in `src/preprocessing.py`. This is not a model score. `python -m unittest discover -s tests -v` exited 0 with 13 tests. The raw SHA-256 remained `3ef126de5cefff26eb11fbb4237f1a1401cb64b488e2f1d598c23cedeb4c45ae`.

- Training rows: 3,539. Graduate 1,767, Dropout 1,137, Enrolled 635.
- Test rows: 885. Graduate 442, Dropout 284, Enrolled 159.
- Duplicate rows dropped: 0. Grade zeros removed: 0. The split was not written to `data/processed/`.

Later entries in this section must contain verified results only. Each entry needs the date, the command or notebook that produced it, the metric names, the values copied from output, and the file they were saved to. If a run fails, record the failure. Do not fill this section with expected or typical scores.

Phase 5 run on 2026-11-15, command `.\.venv\Scripts\python.exe src\run_phase5.py` from the repository root. Exit code 0. Before that command, `.\.venv\Scripts\python.exe -m unittest discover -s tests -v` exited 0 with 27 tests. Raw SHA-256 before and after the run was `3ef126de5cefff26eb11fbb4237f1a1401cb64b488e2f1d598c23cedeb4c45ae`. The logistic scaler saw 3,539 training rows at the refit. The forest numerical step was not a scaler. No warnings were recorded. `test_rows_used_for_tuning` in `outputs/evaluation/run_metadata.json` is 0. Balanced accuracy is the recall summary; it matched macro recall, so macro recall is not listed again.

Cross-validation selection, from `outputs/evaluation/selected_parameters.json`. Neither maximum had an exact tie.

- Logistic Regression, declared order 4: `C=0.1`, `class_weight="balanced"`. Mean CV macro F1 `0.6881125650673585`. Fold standard deviation `0.01991414406836082`. Fold scores `0.7120742318841323`, `0.7107293005075087`, `0.6832886203290932`, `0.6682840657995457`, `0.6661866068165126`.
- Random Forest, declared order 14: `n_estimators=200`, `max_depth=20`, `min_samples_leaf=1`, `class_weight="balanced"`. Mean CV macro F1 `0.6998064617503175`. Fold standard deviation `0.012204693927217965`. Fold scores `0.7012925067243464`, `0.7078256956825489`, `0.7146554386714645`, `0.6786516024220942`, `0.696607065251133`.

Completed fits recorded by the run: 40 logistic cross-validation fits, 180 forest cross-validation fits, 2 training-set refits, and 1 dummy training fit. The dummy fit is not part of the 220.

Test metrics, from `outputs/evaluation/test_metrics.json`. These three results are independent. No winner was designated.

- Logistic Regression: macro F1 `0.6892903420183808`, balanced accuracy `0.7023012029890147`, macro precision `0.697566135029276`, accuracy `0.727683615819209`.
- Random Forest: macro F1 `0.7016908329335929`, balanced accuracy `0.7018610663191801`, macro precision `0.7079859524582094`, accuracy `0.7548022598870057`.
- Dummy most-frequent: macro F1 `0.22205476011052497`, balanced accuracy `0.3333333333333333`, macro precision `0.1664783427495292`, accuracy `0.4994350282485876`.

The dummy confusion matrix in that file has every test row in the Graduate column: Dropout 284, Enrolled 159, Graduate 442. Per-class precision, recall, F1, and both other confusion matrices are in `outputs/evaluation/per_class_metrics.csv` and `outputs/evaluation/confusion_matrices.csv`.

## 13. Issues / Blockers

No modelling blocker. The following conflicts were kept open instead of being overwritten:

1. Phase 1 asked for two or three research questions. One question was approved. The others stay open.
2. Report audience and provisional title were not part of this decision.
3. The student stated on 2026-11-14 that Phase 0 is complete and approved.
4. UCI metadata and the local file now agree on 4,424 instances, 36 input features, and no missing values. The agreement is recorded separately from the UCI claim. The zip extract and UCI's direct CSV URL are not byte-identical.
5. UCI states a strong class imbalance without giving class counts on the dataset summary. The local file counts are now measured: Graduate 2,209, Dropout 1,421, Enrolled 794.
6. UCI's creator example used an 80/20 split. On 2026-11-15 the student approved an 80/20 stratified split with seed 42. That split is created in memory by `prepare_from_raw()` and is not written to `data/processed/`. The UCI example is not itself the approval.
7. The seven alternative datasets were not named in the update instruction, so their names are absent on purpose.
8. Logistic Regression, Random Forest, and the most-frequent dummy were fit on 2026-11-15 under the frozen Phase 5 design. The student approved the measured scores in `outputs/evaluation/` and the model artefacts on 2026-11-15. Phase 5 is complete. The test scores were not used to change the design.
9. UCI's download example uses `ucimlrepo`. That package is not approved and was not installed.
10. On 2026-11-14 the UCI dataset page licence section was quoted: Creative Commons Attribution 4.0 International (CC BY 4.0), linking to https://creativecommons.org/licenses/by/4.0/legalcode.

The local folder name (`CMP6202-AI-ML`) and the GitHub repository name (`CMP6202-AI-ML-Project`) differ. This is a naming note, not a blocker.

## 14. AI Assistance Log

| Date | AI Tool | Task | Verification Performed |
| --- | --- | --- | --- |
| 2026-10-17 | Cursor (coding agent) | Project planning and documentation: drafted the six files in `docs/` from the student's coursework constraints. No dataset, model, or result was selected. | Human review required. The student must read the six documents against the official brief before treating them as approved. No code was run. No statistics were produced. |
| 2026-11-14 | Cursor (coding agent) | Updated the six planning documents to record the approved UCI 697 dataset decision. Checked the public UCI dataset page for ID, size, feature count, missing-values flag, task, and DOI. Did not download the CSV, install packages, run EDA, or train models. | Student must compare this write-up with their Phase 1 notes. The UCI page check supports the recorded size and task. The licence line was not re-quoted from that fetch. No model output was produced. |
| 2026-11-14 | Cursor (coding agent) | Created `README.md`, `.gitignore`, `requirements.txt`, the empty project folders, and `.venv`. Installed the six direct packages and checked their imports. Did not download the dataset, install `ucimlrepo`, run EDA, or train models. | Package versions were read with `pip show`. Import check printed numpy 2.5.4, pandas 3.1.1, matplotlib 3.11.2, seaborn 0.13.2, and scikit-learn 1.9.1. `pip show ucimlrepo` reported that the package was not found. |
| 2026-11-14 | Cursor (coding agent) | Downloaded the official UCI zip for dataset 697, extracted `data.csv` without editing it, and ran `src/data_audit.py`. | Script exit code 0. Reported shape 4424 by 37, missing cells 0, duplicate rows 0, and target counts Graduate 2209, Dropout 1421, Enrolled 794. Licence sentence was read from the UCI dataset page. No model was trained. |
| 2026-11-14 | Cursor (coding agent) | Built and executed the EDA notebook, saved seven figures, and wrote `outputs/eda_report.md` from the notebook results. | `jupyter nbconvert --execute` exit code 0. Raw file SHA-256 remained `3ef126de5cefff26eb11fbb4237f1a1401cb64b488e2f1d598c23cedeb4c45ae`. No model was trained. RQ2 and RQ3 were not marked approved. |
| 2026-11-15 | Cursor (coding agent) | Recorded the student's approval of Phase 3 in `docs/Phases.md` and `docs/Memory.md`. | The student stated that the notebook, seven figures, and EDA report had been reviewed and approved. No data, notebook, figure, or report file was edited. No model was trained. |
| 2026-11-15 | Cursor (coding agent) | Applied two student decisions to `docs/phase-4-preprocessing-plan.md` and aligned `docs/Phases.md` and `docs/Memory.md`. | Documentation only. The four binary features stay provisionally retained under an unverified timing assumption. Zero grades stay numeric zero, with no sensitivity analysis in the initial implementation. No data, notebook, script, split, encoder, scaler, or model was changed. Phase 4 was not marked complete. |
| 2026-11-15 | Cursor (coding agent) | Recorded approval of the remaining Phase 4 methodology in `docs/phase-4-preprocessing-plan.md`, `docs/Phases.md`, and `docs/Memory.md`. | Documentation only. The six methodology decisions are frozen, the six unresolved columns stay excluded, and the earlier binary and zero-grade decisions stay in force. No data, notebook, script, split, encoder, scaler, or model was changed. Phase 4 was not marked complete. Phase 5 was not started. |
| 2026-11-15 | Cursor (coding agent) | Added `src/preprocessing.py` and `tests/test_preprocessing.py` for the frozen Phase 4 plan. Updated `docs/Phases.md` and `docs/Memory.md`. | `python -m unittest discover -s tests -v` passed 13 tests. Raw SHA-256 was unchanged. No classifier was fit. Phase 4 was not marked complete. Phase 5 was not started. |
| 2026-11-15 | Cursor (coding agent) | Recorded the student's approval of completed Phase 4 in `docs/Phases.md`, `docs/Memory.md`, and the status notes of `docs/phase-4-preprocessing-plan.md`. | Documentation only. The student stated that the implementation had been reviewed and verified. The frozen methodology was not edited. No source file, test, dataset, or model was changed. Phase 5 implementation was not started. |
| 2026-11-15 | Cursor (coding agent) | Wrote the Phase 5 experimental-design proposal and updated `docs/Phases.md` and `docs/Memory.md`. | Documentation only. Grid sizes were checked as 8×5=40 and 36×5=180. No script was added or run. No model was trained. Phase 5 was not marked approved or complete. |
| 2026-11-15 | Cursor (coding agent) | Recorded the remaining Phase 5 configuration decisions in `docs/phase-5-experimental-design.md`, `docs/Phases.md`, and `docs/Memory.md`. | Documentation only. Fit totals checked as 220 CV fits plus two refits. The proposal was not marked frozen or formally approved. No script, dataset, or model was changed or run. |
| 2026-11-15 | Cursor (coding agent) | Marked the Phase 5 experimental design formally approved and frozen in `docs/phase-5-experimental-design.md`, `docs/Phases.md`, and `docs/Memory.md`. | Documentation only. The student stated that the design was final. Grids, fit counts, the tie-break, metrics, and evaluation rules were left unchanged. No script, dataset, or model was changed or run. Implementation was not started. |
| 2026-11-15 | Cursor (coding agent) | Implemented the frozen Phase 5 experiment in `src/model_training.py`, `src/model_evaluation.py`, `src/run_phase5.py`, and the new tests. Ran the suite and `src/run_phase5.py`. Updated `docs/Phases.md`, `docs/Memory.md`, and factual status lines in `docs/phase-5-experimental-design.md`. | `python -m unittest discover -s tests -v` passed 27 tests. `src/run_phase5.py` exited 0 and wrote `outputs/evaluation/`. The run recorded 40 and 180 finite cross-validation fits, two training refits, and one dummy fit. Raw SHA-256 was unchanged. Phase 5 was not marked complete at that point. |
| 2026-11-15 | Cursor (coding agent) | Recorded the student's approval of completed Phase 5 in `docs/Phases.md`, `docs/Memory.md`, and the status lines of `docs/phase-5-experimental-design.md`. | Documentation only. The student stated that the implementation, model results, evaluation metrics, report, and generated artefacts had been reviewed and approved. The frozen design was not edited. No source file, test, dataset, model, or evaluation output was changed. No later phase was started. |

Add a row whenever an AI tool drafts code, analysis, citations, or report text. Verification means what the student (or a rerun) actually checked.

## 15. Session Handoff

**Completed this session**

- Recorded the student's approval of Phase 5 — Model Development and Evaluation on 2026-11-15.
- Left the frozen experimental design and the measured results unchanged.
- Did not start Phase 6 or any later phase.
- Did not edit source code, tests, data, models, or evaluation outputs.

**Currently being worked on**

- Nothing. Phase 5 is complete and approved. No later phase has been started.

**Exact next task**

- Wait for the student before starting any later phase. Do not change the frozen design or the measured results.

**Constraints the next session must keep**

- Active dataset only: UCI 697, CC BY 4.0, target `Target`, classes Dropout, Enrolled, and Graduate.
- Prediction point: after the second semester, using only information available then.
- RQ1 is the only approved research question. RQ2 and RQ3 stay proposed.
- Models fit under the frozen design: Logistic Regression, Random Forest, and `DummyClassifier(strategy="most_frequent")`. Scores are only the values in `outputs/evaluation/`.
- Balanced accuracy and macro recall are equivalent for this multiclass task. The full-data majority-class share is about 49.93% (Graduate, 49.9322%). That share is not a model score. The dummy test accuracy is a separate measured result.
- A semester grade of 0 stays numeric zero. Do not impute it or run a zero-grade sensitivity analysis in the initial implementation. What 0 means is still unresolved.
- `Displaced`, `Educational special needs`, `Scholarship holder`, and `International` are provisionally retained. Their measurement dates are not verified.
- `Debtor`, `Tuition fees up to date`, `Unemployment rate`, `Inflation rate`, `GDP`, and `Curricular units 2nd sem (without evaluations)` are excluded from the primary matrix. Their dates, or the semester wording, remain unresolved.
- Matching first- and second-semester features are strongly correlated.
- Approved metrics: macro F1, balanced accuracy, macro precision, accuracy, confusion matrix, and per-class precision, recall, and F1. Balanced accuracy and macro recall are one recall summary. The measured values are in section 12 and `outputs/evaluation/`.
- Approved split: 80/20, stratified on `Target`, `random_state=42`, then 5-fold stratified cross-validation on the training portion. `src/preprocessing.py` creates that split in memory. It is not saved as a processed file. Fit preprocessors on training data only. Do not use `Target` as a feature.
- Approved encoding: binaries stay 0/1, nominals are one-hot, `Application order` stays ordered, rare levels are not merged. No derived features. Scale numerical columns for Logistic Regression only.
- Strip the tab in the daytime-attendance header in memory. Do not edit the raw file.
- Integer codes are not automatically continuous.
- Account for class imbalance without inventing class counts.
- Document the single-institution limit and fairness later, from the actual data and outputs.
- Seven alternatives stay inactive. Do not invent their names.
- No fabricated results. The initial six packages are already installed in `.venv`. Do not install `ucimlrepo` unless a later decision says to.
- Update this file at the end of the next meaningful session.
