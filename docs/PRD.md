# Product Requirements Document — CMP6202 AI/ML Project

Internal planning document for module CMP6202 Artificial Intelligence and Machine Learning. This is not the final report. The report will be written later, at about 3,000 words, from verified project outputs.

Student ID: s24156365  
Repository name: CMP6202-AI-ML-Project

Where a modelling decision has not been made, this document marks it **TBD — to be decided after dataset selection.** Do not fill those gaps by inventing a dataset, target, algorithm, metric threshold, or result.

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

No final dataset, target variable, model, or result is selected in this document.

## 2. Academic Objective

The project must show that the student can do the following, and can show the working:

- **Dataset understanding** — describe where the data came from, what each important field means, how large it is, and which quality issues it has.
- **Research-question formulation** — turn the dataset into a clear supervised question, with a defined target and a reason that question matters.
- **Exploratory data analysis** — use summaries and plots to learn the data before locking model choices.
- **Supervised learning** — build a classification or regression solution. Unsupervised work is out of scope unless the chosen problem later requires it as a justified sub-step, which is not assumed.
- **Preprocessing** — handle missing values, duplicates, types, encoding, and scaling only where the data requires them, and document why.
- **Model development** — train a simple baseline and at least one further algorithm from a different model family.
- **Evaluation** — measure performance with metrics appropriate to the task and the class or error balance of the data.
- **Model improvement** — use cross-validation and hyperparameter tuning after a baseline exists, then compare tuned models with that baseline.
- **Reproducibility** — another reader must be able to install the documented environment and rerun the notebooks or scripts in the documented order.
- **Critical discussion** — conclusions must follow from saved outputs. Limitations must be stated in plain language.
- **Reflection** — the student records what they learned, what was difficult, and how those difficulties were handled. This section is student-owned.

## 3. Target Users / Audience

**Primary audience**

- The university marker and module tutor, who will check the coursework requirements against the report, the code, the repository, and the evidence of learning.

**Secondary audiences**

- A technical reader or data scientist who wants to understand the method, the metrics, and the limits of the findings.
- A student or developer who needs to reproduce the project from the README and the repository alone.

The final report must name **one explicit target audience** once the dataset and problem are chosen. Until then:

**Report target audience: TBD — to be decided after dataset selection.**

Writing for the marker and writing for a domain stakeholder are different. The report should not try to address every possible reader at once. Pick the audience that matches the problem, then keep terminology, figures, and recommendations consistent with that choice.

## 4. Problem Statement

**TBD — to be defined after dataset selection.**

After the dataset is chosen, the problem statement must document all of the following. None of these may be invented before the data is in hand:

- **Real-world problem** — what decision, prediction, or description the data can support.
- **Target variable** — the exact column or derived field being predicted, including its type and meaning.
- **Task type** — classification or regression, and why that type matches the target.
- **Significance** — who could use the result, and what a useful or poor prediction would mean. This must stay proportionate to a coursework study.
- **Dataset suitability** — confirmation that the dataset is open-access, publicly available, large enough (at least 3,000 rows; about 3,000–5,000 recommended), and fit for the question. If the chosen file is larger, document why it is still appropriate and how any sampling was done.

Until those items are filled from the actual dataset and its documentation, later notebooks must not assume a target, a positive class, or a success threshold.

## 5. Core Features / Deliverables

The finished project must contain the following. Items that depend on the dataset stay unspecified until selection.

| Deliverable | What "done" means |
| --- | --- |
| Dataset acquisition | A real open-access file, or a script/instructions that obtain the exact file from a stable source. |
| Dataset metadata | Name, source URL, retrieval date, row and column counts, and a short description. Counts must be measured, not guessed. |
| Licence verification | Licence name and a link or quotation of the permission that allows use. If the licence is unclear, the dataset is not selected. |
| Dataset dictionary | Field name, type, meaning, and notes on missingness or codes. Unknown meanings stay marked unknown. |
| Research questions | Two or three questions the EDA and models can actually address. |
| Exploratory data analysis | Univariate, bivariate, and multivariate checks, with interpretation. |
| Cleaning | Documented treatment of missing values, duplicates, types, and outliers. |
| Preprocessing pipeline | A leakage-safe, repeatable transformation from raw fields to model inputs. |
| Feature engineering | Only where a transformation is justified by the data or the question. If none is justified, record that decision. |
| Train/test split | One documented split, shared by every model in the comparison. |
| Baseline models | A simple, interpretable baseline trained before tuning. |
| Model comparison | At least two different algorithms, compared on the same data and metrics. |
| Evaluation metrics | Metrics chosen for the task, reported from code outputs. |
| Cross-validation | Used to estimate generalisation and/or to tune, on training data only. |
| Hyperparameter tuning | A documented search after the baseline, without using the test set to pick settings. |
| Final model comparison | A table of baseline and tuned results, with a justified preferred model. |
| Plots | Labelled figures exported for the report. |
| Conclusions | Claims that cite the project's own tables and figures. |
| Limitations | Sample, leakage, metric, and scope limits written explicitly. |
| Learning reflection | Student account of learning, challenges, and how challenges were addressed. |
| Certification evidence | Real AI/ML certificates or badges stored in the repository or linked, with the provider and date. |
| GitHub reproducibility | Public repository, README run steps, and code that matches the report. |
| References | BCU Harvard references to real, accessible sources. |
| AI-use declaration | A transparent account of generative-AI assistance, and what the student verified. |

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
- **FR-12** Hyperparameter tuning must start only after a baseline evaluation, and test-set scores must not be the criterion for choosing hyperparameters.
- **FR-13** Report figures and comparison tables must be produced by code and saved under `figures/` or `outputs/`.
- **FR-14** The README must state the Python version, install steps, data placement, and the order in which to run the work.
- **FR-15** Citations in the report must use BCU Harvard and must refer to sources the student can actually open.
- **FR-16** Generative AI use must be declared. AI-assisted code, text, and analysis must be run or read and checked by the student before it is treated as project evidence.
- **FR-17** The reflection must describe this project's actual work. It must not be a generic essay detached from the repository.
- **FR-18** Certification evidence must be genuine. Missing certificates stay listed as incomplete; they are never invented.

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

Success is requirement completion and evidential honesty. This document sets **no numeric score threshold**, because no dataset or baseline exists yet. Inventing a target accuracy, F1, or RMSE would be premature.

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

## 10. Open Decisions

Each item below is **TBD — to be decided after dataset selection**, except where another gate is named.

| Decision | Status | Gate |
| --- | --- | --- |
| Dataset | TBD — to be decided after dataset selection. | Open-access licence, source link, and at least 3,000 rows confirmed. |
| Classification or regression | TBD — to be decided after dataset selection. | Follows from the target variable, not from preference. |
| Target variable | TBD — to be decided after dataset selection. | Must exist in the data, or be a documented derivation. |
| Final research questions | TBD — to be decided after dataset selection. | Two or three questions the data can support. |
| Final algorithms | TBD — to be decided after dataset selection. | Choose only after EDA. Minimum two families. Baseline first. |
| Final metrics | TBD — to be decided after dataset selection. | Match the task and the error or class balance. |
| Final target audience for the report | TBD — to be decided after dataset selection. | One explicit audience, named in the report. |
| Certifications to complete | TBD — to be decided when the student selects approved AI/ML certification options. | Evidence must be real. |
| Project / report title | TBD — to be decided after dataset selection. | Must match the actual problem. |
