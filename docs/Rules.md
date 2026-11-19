# Project Rules and Engineering Constraints

Rulebook for anyone writing code or prose in this repository, including Cursor and other AI coding agents.

Module: CMP6202 Artificial Intelligence and Machine Learning  
Student ID: s24156365  
Repository: CMP6202-AI-ML-Project

These rules override a request to "just pick something" when the something is a metric threshold, a class count, a citation, or a result. The dataset decision is closed: UCI dataset 697, `Target`, multiclass classification. If another decision is open, write **TBD**. Do not invent a value to keep working.

Related documents: `docs/PRD.md`, `docs/Architecture.md`, `docs/Phases.md`, `docs/Design.md`, `docs/Memory.md`.

---

## 1. General Rules

- Do not invent data, statistics, licences, certificates, citations, or model results.
- Do not silently alter raw data. Transformations are written to a new file or a new in-memory object, with the change explained.
- Logistic Regression, Random Forest, and the most-frequent dummy are the approved comparison. They were fitted under the frozen Phase 5 design. Do not train another algorithm, and do not change that experiment.
- Do not optimise prematurely. The approved search is the one already completed. Do not start a new search.
- Every important modelling decision must be explainable in a sentence a marker can check: what was done, why, and what evidence supported it.
- Prefer simple, reproducible solutions. Add complexity only when the data or the coursework requirement shows it is needed.
- Do not present this planning set as the final report.
- Do not mark a task complete in `docs/Memory.md` unless the artefact exists and has been checked.

## 2. Libraries to Prefer

Use these first:

- pandas
- numpy
- scikit-learn
- matplotlib
- scipy, when a statistical routine is actually required
- joblib, when a fitted object needs to be saved and loaded

Optional, with a reason recorded in the notebook or report:

- seaborn, for statistical charts that stay clearer than the matplotlib equivalent
- imbalanced-learn, when measured class imbalance justifies a resampling or specialised learner

## 3. Libraries / Technologies to Avoid Unless Explicitly Justified

Do not introduce the following unless the selected dataset or problem creates a real academic need, and that need is written down before the dependency is added:

- TensorFlow
- PyTorch
- XGBoost
- LightGBM
- CatBoost
- MLflow
- Docker
- FastAPI
- Flask
- Django
- React
- databases
- cloud services
- LangChain
- LlamaIndex
- agent frameworks

They are unnecessary for the default coursework path: classical supervised learning with scikit-learn, documented in notebooks. This is not a permanent ban. A later justification can allow one of them. "It might score higher" or "it is popular" is not a justification. An academic reason tied to this dataset is.

If a justified library is added, update `requirements.txt`, the README, `docs/Memory.md`, and the report's method section.

## 4. Data Handling Rules

- Never overwrite raw data in `data/raw/`.
- Keep raw, interim, and processed stages separate.
- Inspect missing values before imputing. Record counts and whether missingness looks structured.
- Inspect duplicates before removing them. Record how many rows a drop would remove.
- Justify outlier treatment. State the rule, the count affected, and whether the points are errors or rare real cases.
- Do not remove rows only because removal improves a metric.
- Preserve meaningful class distributions. If rows are filtered, show the target balance before and after.
- Document every transformation that changes values, rows, columns, or units.
- The approved dataset is UCI 697. UCI reports 4,424 instances, 36 features, and no missing values. Those figures are source metadata. Measure them again from the loaded file before treating them as project statistics.
- Identify categorical variables that are stored as integer codes. Do not automatically treat every integer column as a continuous number. Decide continuous, ordinal, or categorical only after the data dictionary is checked.
- Do not use `Target` as an input feature.
- Use only fields available by the end of the second semester. Confirm that boundary against the loaded columns before modelling.
- Keep the other seven shortlisted datasets as alternatives only. Their names are not in this repository yet. Do not swap in an alternative without a new decision.
- The approved licence is CC BY 4.0. Do not replace it with a guessed licence. If a later download page disagrees, stop and record the disagreement.

## 5. ML Rules

- The approved baseline is `DummyClassifier(strategy="most_frequent")`. It was fitted once on the training portion and was not tuned. The frozen design did not save a separate untuned Logistic Regression or Random Forest. An earlier instruction to save those untuned models before tuning is historical and is not current work.
- The two competitive classifiers are Logistic Regression and Random Forest. Both were tuned with `GridSearchCV`, `scoring="f1_macro"`, and five-fold `StratifiedKFold` on the training data only. The logistic grid has 8 configurations. The forest grid has 36. The completed search is 220 cross-validation fits plus two training-set refits. The dummy fit is not part of the 220.
- Use the same stratified test split for every model in the comparison. The approved split is 80/20 on `Target`, with `random_state=42`. The untouched test set has 885 rows and was evaluated once after tuning.
- The approved task is multiclass classification. The approved metrics are macro F1-score, balanced accuracy, macro precision, accuracy, a confusion matrix, and per-class precision, recall, and F1. Macro F1 is the primary metric. Balanced accuracy is the recall summary. The saved values are in `outputs/evaluation/`. Do not copy or recalculate them in this rulebook.
- There is no single positive class. Dropout, Enrolled, and Graduate are the three classes. Report precision, recall, and F1 in a way that does not hide a weak class. Macro F1 is the approved summary. No single overall winner is approved.
- ROC-AUC is not part of the approved metric list. Do not add it unless a later written reason explains why a multiclass AUC is needed.
- Regression metrics do not apply to this target. Do not report MAE, MSE, RMSE, R², or MAPE for `Target`.
- Do not use accuracy alone. The counted class shares are in `outputs/dataset_audit.md` and `outputs/eda_report.md`. Graduate is the largest class.
- Account for that imbalance in the split and in the metrics. Do not add resampling or imbalanced-learn. The frozen experiment did not use them.
- The completed cross-validation ran on the training portion. Do not run a new search.
- The historical instruction to start tuning only after a separate untuned Logistic Regression or Random Forest evaluation is not the approved workflow. The dummy baseline and the two training-only searches are the frozen workflow.
- Test data must not be used to choose hyperparameters, features, or preprocessing settings. The 885-row holdout was used once and must stay unused for any new choice.
- Compare the two tuned models and the dummy on the approved metric set, not on accuracy by itself.
- The comparison produced by the approved run is stored under `outputs/evaluation/`. Do not treat `outputs/tables/` or `outputs/metrics/` as the approved destination. Those folders are not part of this repository.
- Do not designate a single overall winner. Naming one metric, including test macro F1, does not authorise that conclusion.
- The report must document the single-institution limitation and fairness considerations for demographic fields. Do not write those conclusions before the data dictionary and the model outputs exist.

## 6. Coding Standards

- Use clear variable names (`X_train`, `y_test`, `target_column`). Avoid unexplained abbreviations.
- Put repeated logic in functions.
- Keep functions short and focused on one job.
- Add docstrings where a function's purpose or assumptions are not obvious from its name.
- Write comments that explain why a step exists. Do not comment an obvious assignment.
- Keep notebook cells small enough to rerun one idea at a time. Avoid giant cells that mix loading, plotting, and modelling.
- Use relative paths from the repository root. No hardcoded absolute Windows paths.
- No secrets, tokens, or personal credentials in code, notebooks, or markdown.
- No dead code and no commented-out experiments left as the final path. Move abandoned ideas to a short note in `docs/Memory.md` if they matter.
- No duplicated preprocessing logic across notebooks. Share one pipeline.
- No unexplained magic numbers. Name the seed, the test size, and the thresholds, and state why those values were used.
- Follow `docs/Design.md` for figures and tables that may enter the report.

## 7. Error Handling

- Fail clearly when an expected input file is missing. The message should name the path that was expected and point to the README data step.
- Validate that expected columns exist before modelling.
- Validate that the target column exists and is non-empty.
- Detect an invalid or empty dataset (zero rows, or no feature columns after preprocessing) and stop.
- Raise informative exceptions with enough context to fix the problem.
- Do not swallow exceptions with a bare `except:`.
- Do not continue training after a critical preprocessing failure.
- Do not replace a failed load with a synthetic dataframe and continue.

## 8. AI Boundaries

This section is binding for Cursor and any other generative-AI assistant used on this project.

**Cursor / AI may assist with:**

- project planning and these documents
- code scaffolding
- explaining algorithms
- debugging
- refactoring
- suggesting EDA checks
- suggesting tests or validation checks
- improving comments and docstrings
- checking report structure against the brief

**AI must not:**

- fabricate dataset statistics
- fabricate model scores
- fabricate citations
- fabricate licence information
- fabricate certification evidence
- invent experimental results
- write conclusions that the saved outputs do not support
- pretend code has run when it has not
- claim a chart shows a pattern without inspecting the actual data or the actual output
- silently choose a research question, dataset, or target on behalf of the student
- copy exemplar or template wording into the assessed report

**Whenever AI-generated code is used:**

1. Run it.
2. Inspect the output.
3. Verify statistical and technical correctness against the data and the library documentation.
4. Record meaningful AI assistance in `docs/Memory.md` so the later declaration is accurate.

If a result has not been produced by a run in this project, the only acceptable statement is that the result does not exist yet.

The student remains responsible for the submitted report, code, and reflection. AI assistance does not transfer authorship of the learning reflection.

## 9. Academic Integrity Rules

- The work remains student-owned. Planning help is allowed; submitting unread AI text as understanding is not.
- Cite borrowed ideas, definitions, and method descriptions.
- Cite coding tutorials or documentation where they materially shaped the implementation.
- Use real, accessible references. Open the source before citing it.
- Use BCU Harvard style for report references.
- Do not plagiarise course materials, papers, blogs, or other students.
- Do not fabricate sources, page numbers, or quotations.
- Any module exemplar is structural guidance only. Do not reuse its sentences, dataset, or results.
- The AI-use declaration must match the log in `docs/Memory.md` and the student's own memory of what was checked.

## 10. Git Rules

- Write meaningful commit messages that say why the change was made.
- Never commit secrets or credential files.
- Avoid committing unnecessary large temporary files, notebook checkpoints, virtual environments, and regenerated caches.
- The repository must be public before submission, unless the module office issues a different written instruction.
- Keep the README accurate as files and commands change.
- Do not rewrite published history unless there is a clear reason and the student agrees.
- Do not commit fabricated outputs so the repository "looks finished".

## 11. Definition of Done for Any Task

A task is done only when all of the following hold:

- The code runs.
- The outputs have been inspected.
- Assumptions are documented next to the step or in `docs/Memory.md`.
- The result is saved when a later phase or the report needs it.
- The relevant planning document is updated if the decision changed.
- `docs/Memory.md` is updated (status, phase, task, files, decisions, blockers, AI log, and session handoff).

A document that still says "TBD" is not a failed task. Filling a TBD with an invented value is a failed task.
