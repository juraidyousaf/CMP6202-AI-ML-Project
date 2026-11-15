# CMP6202 AI & ML Project

Student ID: s24156365  
Repository: [CMP6202-AI-ML-Project](https://github.com/juraidyousaf/CMP6202-AI-ML-Project)

Coursework project for CMP6202 Artificial Intelligence and Machine Learning. This repository is a reproducible classical machine-learning study. It is not a deployed application.

No model has been trained. No evaluation scores exist. The original dataset archive and its extracted CSV are in `data/raw/`.

## Project overview

The project uses one public dataset to study a supervised classification problem. Later work will load the file, explore it, preprocess it without leaking the test set, compare two planned algorithms, and report only results produced by that code.

The report audience, provisional title, train/test ratio, and random seed are not decided. Seven other datasets were shortlisted as alternatives. Their names are not stored here, and they are not part of this project.

## Research problem

How effectively can Logistic Regression and Random Forest classify students into Dropout, Enrolled, and Graduate categories using enrolment, demographic, socioeconomic, and first- and second-semester academic information?

The prediction point is after the second semester. Features must be limited to information available by that point. The target column must not be used as an input. This boundary still has to be checked against the loaded columns.

UCI describes the records as coming from one higher education institution. The report must discuss that limit and fairness where demographic fields are used. Those discussions have not been written.

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
| Extracted file | `data/raw/data.csv` (533,230 bytes), extracted unchanged from that zip |
| Encoding and delimiter | UTF-8 with BOM, semicolon-separated. This was detected from the file. |

## Planned classification task

Multiclass classification.

- Target column: `Target`
- Classes: Dropout, Enrolled, Graduate
- There is no single positive class.
- The train/test split must be stratified on `Target`.
- The test fraction and `random_state` are not chosen.
- UCI's example of an 80/20 split is not the split for this project.
- Measured class counts in `data/raw/data.csv`: Graduate 2,209 (49.9322%), Dropout 1,421 (32.1203%), Enrolled 794 (17.9476%). These are file counts, not model scores.
- Integer fields that store category codes must not automatically be treated as continuous numbers.

## Planned models

These models are planned. They have not been trained, and exploratory analysis can still challenge the pair.

1. Logistic Regression, as the interpretable baseline.
2. Random Forest, as the second algorithm from a different model family.

A third algorithm is not selected. Hyperparameter tuning has not been designed and must not use the test set.

## Planned evaluation metrics

No scores have been calculated.

- Macro F1-score
- Precision
- Recall
- Balanced accuracy
- Accuracy
- Confusion matrix

Accuracy must not be the only reported metric. No numeric success threshold is set.

## Project structure

```text
CMP6202-AI-ML-Project/
├── README.md
├── requirements.txt
├── .gitignore
├── data/
│   ├── raw/          # original UCI zip and extracted data.csv; not ignored by Git
│   ├── interim/
│   └── processed/
├── notebooks/
│   └── 01_exploratory_data_analysis.ipynb
├── src/
│   └── data_audit.py # read-only audit; does not edit data/raw/
├── figures/
│   └── eda/          # seven EDA figures written by the notebook
├── outputs/
├── docs/
└── references/
```

`docs/` holds the planning documents. They are not the graded report. The audit report is `outputs/dataset_audit.md`. The EDA report is `outputs/eda_report.md`.

Run the audit, then the exploratory notebook, from the repository root:

```powershell
.\.venv\Scripts\Activate.ps1
python src/data_audit.py
jupyter nbconvert --to notebook --execute --inplace notebooks/01_exploratory_data_analysis.ipynb
```

The notebook reads `data/raw/data.csv` and writes figures to `figures/eda/`. It does not modify the raw file. RQ1 is the only approved research question. RQ2 and RQ3 are proposed and are not approved. No model is trained.

## Setup and execution

The environment used to create this setup was Python 3.13.7 on Windows. The project asks for Python 3.11 or a later compatible release.

From the repository root in PowerShell:

```powershell
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

On macOS or Linux, activate the environment with `source .venv/bin/activate` instead.

Do not install `ucimlrepo`. The dataset is already stored under `data/raw/`. Model training is a later phase.

## Attribution and licence

UCI displays this dataset citation:

Realinho, V., Vieira Martins, M., Machado, J., and Baptista, L. (2021) *Predict Students' Dropout and Academic Success* [Dataset]. UCI Machine Learning Repository. https://doi.org/10.24432/C5MC89.

The report bibliography still needs BCU Harvard formatting and a check that each source opens. This README does not add that reference list.

**Licence status: quoted from the UCI dataset page on 2026-11-14.**

The page states: "This dataset is licensed under a Creative Commons Attribution 4.0 International (CC BY 4.0) license." It links to https://creativecommons.org/licenses/by/4.0/legalcode.

The raw files remain available to Git. `data/raw/` is not listed in `.gitignore`.

The official zip and UCI's direct `data.csv` URL are both on `archive.ics.uci.edu`, and they are not byte-identical. This project keeps the zip and the `data.csv` extracted from it. Details are in `outputs/dataset_audit.md`.
