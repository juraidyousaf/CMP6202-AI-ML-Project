# Product Requirements Document — CMP6202 AI/ML Project

Internal planning document for module CMP6202 Artificial Intelligence and Machine Learning. This is not the final report. The CMP6202 Assessment Brief 2026–27 and Individual Report Template 2026–27 were reviewed on 2026-11-16 and inspected on 2026-11-17. They are stored at the repository root as `CMP6202 Assessment Brief  2026-27.docx` and `CMP6202 Individual Report Template 2026-27.docx`. The brief sets a maximum of 3,000 words with a +10% tolerance only, up to 3,300 words. There is no lower tolerance. Headings, tables, citations, quotes, and lists in the main body count. Material before the body, and references, bibliographies, and appendices, do not. The report has not been drafted.

Student ID: s24156365  
Repository name: CMP6202-AI-ML-Project

The dataset, supervised task, split, and Phase 5 models are recorded. Where a report decision has not been made, this document marks it **TBD**. Do not fill those gaps by inventing a metric threshold, a class count, or a result. Phase 5 training and evaluation are complete and approved. The measured scores stay in `outputs/evaluation/`.

The "product" in this document is a reproducible machine-learning coursework project: public data, supervised learning, documented experiments, and a report a marker can check against the code.

---

## 1. Project Overview

The project will select a real-world open-access dataset, formulate one supervised machine-learning problem, and carry that problem through a full, inspectable workflow.

The workflow is:

1. Choose a publicly available dataset and confirm that its licence allows this use.
2. Define a classification or regression question with an explicit target variable.
3. Explore the data and record what the exploration shows.
4. Clean and preprocess the data, with every material transformation justified.
5. Train at least two different algorithms under a fair comparison design.
6. Evaluate them with metrics that match the task.
7. Improve the models using cross-validation and hyperparameter tuning, without leaking the test set into those choices.
8. Compare the models and explain what the evidence supports.
9. State limitations, reflect on learning, and make the work reproducible from the GitHub repository.

The dataset and task are selected. The approved dataset is **Predict Students' Dropout and Academic Success** (UCI dataset 697). The task is multiclass classification of the `Target` column into Dropout, Enrolled, and Graduate. Phase 5 fitted Logistic Regression, Random Forest, and a most-frequent dummy classifier. The saved results are in `outputs/evaluation/`. The report that interprets them has not been written.

## 2. Academic Objective

The project must show that the student can do the following, and can show the working:

- **Dataset understanding** — describe where the data came from, what each important field means, how large it is, and which quality issues it has.
- **Research-question formulation** — turn the dataset into a clear supervised question, with a defined target and a reason that question matters.
- **Exploratory data analysis** — use summaries and plots to learn the data before locking model choices.
- **Supervised learning** — build a classification or regression solution. Unsupervised work is out of scope unless the chosen problem later requires it as a justified sub-step, which is not assumed.
- **Preprocessing** — handle missing values, duplicates, types, encoding, and scaling only where the data requires them, and document why.
- **Model development** — train a simple baseline and at least one further algorithm from a different model family.
- **Evaluation** — measure performance with metrics appropriate to the task and the class or error balance of the data.
- **Model improvement** — the approved Phase 5 design tuned Logistic Regression and Random Forest with training-only cross-validation, and fitted the most-frequent dummy separately. The saved comparison is the three test evaluations. A requirement for a separate untuned Logistic Regression or Random Forest artefact conflicts with that frozen design and is not outstanding work.
- **Reproducibility** — another reader must be able to install the documented environment and rerun the notebooks or scripts in the documented order.
- **Critical discussion** — conclusions must follow from saved outputs. Limitations must be stated in plain language.
- **Reflection** — the student records what they learned, what was difficult, and how those difficulties were handled. This section is student-owned.

## 3. Target Users / Audience

**Report audience, approved on 2026-11-17**

Academic and technical readers familiar with introductory machine learning.

The report uses that one audience for terminology, figures, and recommendations. The university marker checks the submitted coursework against the requirements. The marker is not a second writing audience. Do not write the report for a university support team or for a student who needs the project reproduced from the README alone.

## 4. Problem Statement

**Dataset selected on 2026-11-14. The local file was audited on 2026-11-14. Phase 5 models were trained and evaluated on 2026-11-15.**

- **Real-world problem** — estimate, after the second semester, which of three academic outcomes a student record falls into: Dropout, Enrolled, or Graduate. Predictors are limited to enrolment, demographic, socioeconomic, and first- and second-semester academic information available by that point. UCI describes the records as coming from one higher education institution. The report must state that single-institution limit and must discuss fairness where demographic information is used. Those discussions are not written yet, and no fairness audit has been run.
- **Target variable** — `Target`. The approved classes are Dropout, Enrolled, and Graduate. Phase 2 confirmed the column name and the stored class labels in `outputs/dataset_audit.md`. The target is not an input feature.
- **Task type** — multiclass classification. Three outcome categories require a classification task. This is not a regression problem, and there is no single positive class.
- **Significance** — the coursework question is how well the approved models separate these three outcomes from information available by the end of the second semester. A result that looks strong only because it favours the largest class would be a weak finding. No prediction system is being deployed.
- **Dataset suitability** — the approved source is public and open-access. UCI reports 4,424 instances. The local audit measured the same row count. The measured record is `outputs/dataset_audit.md`.

| Item | Approved record |
| --- | --- |
| Name | Predict Students' Dropout and Academic Success |
| Source | UCI Machine Learning Repository |
| Dataset ID | 697 |
| URL | https://archive.ics.uci.edu/dataset/697/predict |
| DOI | https://doi.org/10.24432/C5MC89 |
| Licence | Creative Commons Attribution 4.0 International (CC BY 4.0) |
| Instances | 4,424, reported by UCI and measured in `outputs/dataset_audit.md` |
| Features | 36 input columns plus `Target`, measured in the audit |
| Missing values | UCI reports none. The local audit also found 0 missing cells. |
| Local file | `data/raw/predict+students+dropout+and+academic+success.zip` and `data/raw/data.csv` |
| Retrieval date | 2026-11-14 |

**Approved predictive research question**

RQ1 is the only approved predictive research question. Its wording is unchanged:

How effectively can Logistic Regression and Random Forest classify students into Dropout, Enrolled, and Graduate categories using enrolment, demographic, socioeconomic, and first- and second-semester academic information?

**Approved descriptive EDA questions**

These questions are descriptive. They use the existing evidence in `outputs/eda_report.md` and the saved EDA figures. They do not authorise another predictive model or experiment, and they do not establish causation.

EDA Question 1: How is the distribution of Dropout, Enrolled, and Graduate outcomes represented in the dataset?

EDA Question 2: How do first- and second-semester academic progression measures, particularly grades and approved units, differ descriptively across the three outcome groups?

The report presentation is resolved: predictive RQ1 is presented beside these two descriptive questions, and the two kinds of question stay distinct. The earlier proposed RQ2 and RQ3 remain unapproved. They must not be written as approved predictive questions. The reviewed brief asks for two or three research questions. This presentation does not guarantee that the descriptive questions count toward that requirement. If that reading is unclear, it should be confirmed with the module leader.

**Approved models, already fitted**

Logistic Regression and Random Forest were tuned on the training split only. `DummyClassifier(strategy="most_frequent")` is the fitted untuned baseline. The design is `docs/phase-5-experimental-design.md`. Saved parameters and scores are under `outputs/models/` and `outputs/evaluation/`. A third algorithm is closed: the approved design does not add one. No single preferred model is authorised.

**Recorded evaluation**

The approved metrics are macro F1, balanced accuracy, macro precision, accuracy, a confusion matrix, and per-class precision, recall, and F1. Balanced accuracy is the recall summary. Accuracy is not the only reported metric. The measured class counts are in `outputs/dataset_audit.md`: Graduate 2,209, Dropout 1,421, Enrolled 794. Those counts are file counts, not model scores. No numeric success threshold is set. This section does not copy the scores. The saved values stay in `outputs/evaluation/`.

## 5. Core Features / Deliverables

The finished project must contain the following. Dataset choice, local measurement, EDA, preprocessing, and Phase 5 modelling are recorded. The report, reflection, certificates, references, and AI declaration remain outstanding.

| Deliverable | What "done" means |
| --- | --- |
| Dataset acquisition | Done. The zip and extracted CSV are in `data/raw/`. |
| Dataset metadata | Done. Name, URL, retrieval date, and measured counts are in `outputs/dataset_audit.md`. |
| Licence verification | Done for the quoted 2026-11-14 UCI sentence. The report bibliography still needs BCU Harvard checking. |
| Dataset dictionary | Done in the audit. Unknown meanings stay marked unknown. |
| Research questions | RQ1 is the approved predictive question. Two descriptive EDA questions are approved. The earlier proposed RQ2 and RQ3 remain unapproved. |
| Exploratory data analysis | Done. `notebooks/01_exploratory_data_analysis.ipynb`, `outputs/eda_report.md`, and `figures/eda/`. |
| Cleaning | Done as decisions in `docs/phase-4-preprocessing-plan.md`. No rows were removed. |
| Preprocessing pipeline | Done. `src/preprocessing.py` fits transformers on training data only. |
| Feature engineering | Done as a recorded decision: no derived features. Further experiments need a separate approval. |
| Train/test split | Done. 80/20 stratified split, `random_state=42`, created in memory. |
| Baseline models | Done under the frozen design. The fitted untuned baseline is the most-frequent dummy, not a separate untuned Logistic Regression. |
| Model comparison | Done as three saved test evaluations. No single preferred model is part of this requirement. |
| Evaluation metrics | Done. Saved under `outputs/evaluation/`. |
| Cross-validation | Done on the training portion during Phase 5 grid search. |
| Hyperparameter tuning | Done for Logistic Regression and Random Forest, without using the test set to pick settings. |
| Final model comparison | The saved comparison exists. The older demand for one justified preferred model conflicts with the frozen design and is not an active requirement. |
| Plots | EDA figures exist. Report selection and captions are outstanding. |
| Conclusions | Outstanding. They belong to the report and must cite saved outputs. |
| Limitations | The design records them. The report discussion is outstanding. |
| Learning reflection | Outstanding. Student-owned. |
| Certification evidence | Outstanding. None are stored. |
| GitHub reproducibility | The repository and README commands exist. A clean third-party reproduction has not been re-verified by the 2026-11-15 documentation sync. |
| References | Outstanding. `references/` does not yet hold the bibliography. |
| AI-use declaration | The project log is in `docs/Memory.md`. The report declaration is outstanding. |

## 6. Functional Requirements

- **FR-01** The dataset must load reproducibly from a documented relative path, or from a documented source command that saves it into `data/raw/`.
- **FR-02** The dataset source URL, retrieval date, and licence must be recorded before modelling begins.
- **FR-03** The pipeline must separate features and the target explicitly. The target column used at training time must match the problem statement.
- **FR-04** Data leakage must be prevented. Preprocessors, feature selection, and resampling fit on training data only. The test set stays unused until final evaluation.
- **FR-05** At least two different machine-learning algorithms must be trained and compared.
- **FR-06** Evaluation must use metrics appropriate to classification or regression, and to any class imbalance or error pattern the data shows.
- **FR-07** Results must be reproducible: pinned or declared dependency versions, fixed `random_state` where the library supports it, and saved metric outputs.
- **FR-08** Notebooks or scripts must have one documented execution order, and that order must succeed from a clean environment using the README.
- **FR-09** Exploratory analysis must be completed and interpreted before the final algorithm list is locked.
- **FR-10** Each cleaning and preprocessing choice that changes rows, columns, or values must be documented, including what was tried and what was kept.
- **FR-11** Cross-validation, where used, must run inside the training portion of the data.
- **FR-12** Test-set scores must not be the criterion for choosing hyperparameters. The frozen Phase 5 design tuned Logistic Regression and Random Forest on training folds and fitted the dummy separately. It did not save an untuned Logistic Regression or Random Forest before tuning. That older sequence is not outstanding work.
- **FR-13** Report figures and comparison tables must be produced by code and saved under `figures/` or `outputs/`.
- **FR-14** The README must state the Python version, install steps, data placement, and the order in which to run the work.
- **FR-15** Citations in the report must use BCU Harvard and must refer to sources the student can actually open.
- **FR-16** Generative AI use must be declared. AI-assisted code, text, and analysis must be run or read and checked by the student before it is treated as project evidence.
- **FR-17** The reflection must describe this project's actual work. It must not be a generic essay detached from the repository.
- **FR-18** Certification evidence must be genuine. Missing certificates stay listed as incomplete; they are never invented.
- **FR-19** The train/test split is stratified on `Target`, 80/20, with `random_state=42`. The student approved that split in Phase 4. It is recorded in `docs/phase-4-preprocessing-plan.md`.
- **FR-20** Preprocessing must be fit on training data only, preferably with a scikit-learn `Pipeline` and `ColumnTransformer`.
- **FR-21** Cross-validation must use training data only.
- **FR-22** `Target` must not be used as an input feature.
- **FR-23** Categorical variables stored as integer codes must be identified. Integer codes must not automatically be treated as continuous numbers.
- **FR-24** Class imbalance must be accounted for in the split and in the metrics. Accuracy alone is not an acceptable summary.
- **FR-25** The report must document the single-institution limitation and fairness considerations. Neither write-up exists yet.
- **FR-26** Features used for prediction must be information available by the end of the second semester. The column check is recorded in `outputs/dataset_audit.md` and `docs/phase-4-preprocessing-plan.md`. Six columns stay excluded. Four binary columns stay provisionally retained under an unverified timing assumption.

## 7. Non-Functional Requirements

- **Reproducibility** — a marker can follow the README and obtain the same tables and figures, allowing for tiny floating-point differences that are explained if they appear.
- **Clarity** — code, plots, and markdown use plain language. A reader should see why each step exists.
- **Maintainability** — repeated logic lives in functions under `src/` once it is used more than once. Notebooks stay readable.
- **Academic integrity** — results, citations, licences, and certificates come from real sources. Unverified AI output is not submitted as fact.
- **Traceability** — every report number that matters can be traced to a saved output, notebook cell, or script.
- **Portability** — paths are relative to the repository root. The project must not depend on one private machine layout.
- **Reasonable runtime** — the full documented run should finish on a normal student laptop. Heavy training needs a written justification and a simpler fallback.
- **No secret credentials** — the repository contains no API keys, passwords, tokens, or private local paths.
- **Deterministic seeds** — `random_state` (or the library equivalent) is set wherever randomness affects splits, models, or resampling, and the chosen seed is recorded.

## 8. Success Criteria

Success is requirement completion and evidential honesty. This document sets **no numeric score threshold**. The dataset is selected, and the approved Phase 5 models have been evaluated. Inventing a target macro F1, accuracy, or other score remains out of scope.

The project is successful when all of the following are true:

- The confirmed coursework requirements in the module brief are met.
- The documented code runs in the stated order on the documented data.
- Findings in the report are supported by inspected outputs.
- The split and preprocessing design does not leak test information into fitting or tuning.
- Models are compared on the same samples and the same metrics.
- Limitations of the data, method, and results are discussed.
- The public GitHub repository is complete enough for a third party to reproduce the work.
- The report can be written from the repository's figures, tables, and notes without adding undocumented results.

A high metric score is not, by itself, success. A modest score with a correct design, a fair comparison, and a clear discussion meets the academic aim better than an unexplained high score.

## 9. Out of Scope

The following are out of scope for this coursework project:

- Production deployment, monitoring, or a hosted prediction service.
- Paid cloud infrastructure, unless a later written justification shows the dataset cannot be handled locally and the module allows it. That need is not assumed.
- A web or mobile application.
- A real-time inference API.
- An LLM agent system, chatbot, or retrieval pipeline wrapped around the model.
- Deep learning, unless the selected problem cannot be addressed adequately by the agreed classical stack and the student records why. That need is not assumed.
- Scraping or collecting data without permission, or using a dataset whose licence does not allow this use.
- Fabricated results, placeholder metrics, synthetic stand-ins presented as the real dataset, or citations that were not opened.
- A third classifier, a single preferred model, feature-importance analysis, or coefficient analysis, unless the student later gives a separate approval. The default is that none of these are added.

## 10. Open Decisions

Closed decisions are marked selected. Remaining items stay **TBD**.

| Decision | Status | Gate |
| --- | --- | --- |
| Dataset | Selected: Predict Students' Dropout and Academic Success, UCI 697, CC BY 4.0. | Downloaded and measured on 2026-11-14. See `outputs/dataset_audit.md`. |
| Classification or regression | Selected: multiclass classification. | Three approved classes. |
| Target variable | Selected: `Target` (Dropout, Enrolled, Graduate). | Confirmed in the audit. |
| Research questions | Presentation resolved: predictive RQ1 beside two descriptive EDA questions. | The earlier proposed RQ2 and RQ3 remain unapproved. This presentation does not guarantee that the descriptive questions satisfy the brief's count. |
| Algorithms | Fitted: Logistic Regression, Random Forest, and a most-frequent dummy. | A third model is closed by the Phase 5 design. |
| Metrics | Saved in `outputs/evaluation/`. | No numeric threshold. A single overall winner is closed by the Phase 5 design. |
| Final target audience for the report | Selected: academic and technical readers familiar with introductory machine learning. | Approved on 2026-11-17. The report text is not written. |
| Certifications to complete | TBD — to be decided when the student selects approved AI/ML certification options. | Evidence must be real. |
| Project / report title | Selected: Predicting Student Academic Outcomes Using Logistic Regression and Random Forest. | Approved on 2026-11-17. The report text is not written. |
| Seen-data reporting | Selected: five-fold training-only cross-validation is validation evidence. The 885-row holdout is unseen test evidence. | Cross-validation results are not training-set performance. Separate final-model training-set metrics were not produced and must not be calculated from this decision. |
| Model comparison figure | Created and verified: `figures/model_comparison/figure_01_model_comparison_f1.png`, from `src/plot_model_comparison.py`. | Panel A is selected Logistic Regression and Random Forest five-fold training-only CV macro F1. No dummy CV score was saved. Panel B is holdout macro F1 for the dummy, Logistic Regression, and Random Forest. Panel C is holdout F1 for Dropout, Enrolled, and Graduate. Saved evaluation files only. Do not name a winner. |
| Submission package | Selected for preparation: a separate Word report, a technical project ZIP, and the public GitHub link in the report. | The final Moodle instructions have not been verified. Neither the Word report nor the ZIP exists. |
| Train/test ratio and `random_state` | Approved: 80/20 stratified split, `random_state=42`. | Approved in Phase 4. UCI's example is not itself the approval. |
| Seven alternative datasets | Retained as alternatives only. Names TBD in these files. | They are not active project datasets. Do not invent their names. |
