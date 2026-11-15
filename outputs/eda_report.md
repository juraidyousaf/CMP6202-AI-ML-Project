# Exploratory data analysis report

Date: 2026-11-14  
Source file: `data/raw/data.csv`  
Notebook: `notebooks/01_exploratory_data_analysis.ipynb`  
Figures: `figures/eda/`

The notebook loaded the original semicolon-separated file with UTF-8-SIG encoding. It removed a trailing tab from the daytime/evening attendance header in memory only. After that rename there were no duplicate column names. The raw file hash was unchanged after the run (`3ef126de5cefff26eb11fbb4237f1a1401cb64b488e2f1d598c23cedeb4c45ae`, 533,230 bytes).

No rows were dropped, encoded, scaled, or split. No model was trained. Associations below are descriptions of this file. They are not causal claims.

## 1. EDA objectives

Describe the target balance, separate category codes from numerical measurements, and compare academic and background features across Dropout, Enrolled, and Graduate. The approved prediction point remains after the second semester.

## 2. Dataset overview

The table has 4,424 rows and 37 columns: 36 inputs and `Target`.

Eighteen columns are categorical candidates. They are integer codes, including two-level fields and the ordinal application order. Eighteen columns are numerical candidates: age, entry grades, curricular-unit counts and grade averages, and the three macroeconomic fields. `Target` is a text category.

This split follows the UCI descriptions. An integer dtype is not treated as evidence that a column is a continuous measurement. Course, marital status, nationality, qualifications, and occupations are codes. Age is a count in years. Admission grade and previous-qualification grade use a 0–200 scale. Semester grade averages use a 0–20 scale and are stored as decimals in this file, although UCI labels them as integers.

## 3. Target distribution

| Class | Students | Percentage of rows |
| --- | ---: | ---: |
| Graduate | 2,209 | 49.9322% |
| Dropout | 1,421 | 32.1203% |
| Enrolled | 794 | 17.9476% |

Percentages are `count / 4,424 × 100`, shown to four decimal places. Figure `figures/eda/figure_01_target_distribution.png` shows the same counts. Graduate is about half the sample, and Enrolled is the smallest class.

## 4. Univariate findings

Age at enrolment has mean 23.265 years, median 20, minimum 17, and maximum 70.

Admission grade has mean 126.978 on the 0–200 scale (minimum 95, maximum 190). Previous-qualification grade has mean 132.613 on the same scale (minimum 95, maximum 190).

First-semester grade average has mean 10.641 and median 12.286. Second-semester grade average has mean 10.230 and median 12.200. Both have a minimum of 0 and a maximum below 19.

A grade of 0 is tied to units approved. All 718 first-semester grades of 0 also have 0 first-semester units approved. All 870 second-semester grades of 0 also have 0 second-semester units approved. The file stores 0 rather than a missing value. UCI does not say whether 0 is a real average or a placeholder for students with no graded units.

Credited units and units without evaluations have median 0. Enrolled units have median 6 in both semesters. Evaluations have median 8 in the first semester and 8 in the second.

Unemployment rate, inflation rate, and GDP have 10, 9, and 10 distinct values. They are repeated context figures, not a different number for every student. Inflation ranges from -0.80 to 3.70. GDP ranges from -4.06 to 3.51.

Figure `figures/eda/figure_02_numerical_distributions.png` shows age, the two entry grades, both semester grade averages, and second-semester units approved.

## 5. Bivariate findings

Means by target class:

| Measure | Dropout | Enrolled | Graduate |
| --- | ---: | ---: | ---: |
| Age at enrolment (years) | 26.069 | 22.369 | 21.784 |
| Admission grade (0–200) | 124.961 | 125.534 | 128.794 |
| Previous qualification grade (0–200) | 131.114 | 131.208 | 134.083 |
| First-semester grade average (0–20) | 7.257 | 11.125 | 12.644 |
| Second-semester grade average (0–20) | 5.899 | 11.117 | 12.697 |
| First-semester units approved | 2.552 | 4.319 | 6.232 |
| Second-semester units approved | 1.940 | 4.058 | 6.177 |
| First-semester units enrolled | 5.821 | 5.965 | 6.670 |
| Second-semester units enrolled | 5.780 | 5.938 | 6.628 |
| First-semester evaluations | 7.752 | 9.341 | 8.277 |
| Second-semester evaluations | 7.174 | 9.436 | 8.142 |

Median second-semester units approved are 0 for Dropout, 4 for Enrolled, and 6 for Graduate. Median ages are 23, 20, and 19.

The share of students with a second-semester grade of 0 is 51.16% for Dropout, 8.56% for Enrolled, and 3.40% for Graduate. For the first semester those shares are 40.11%, 8.94%, and 3.49%.

Within each code, the target mix is:

| Group | Students | Dropout | Enrolled | Graduate |
| --- | ---: | ---: | ---: | ---: |
| Female (UCI code 0) | 2,868 | 25.10% | 16.98% | 57.91% |
| Male (UCI code 1) | 1,556 | 45.05% | 19.73% | 35.22% |
| No scholarship | 3,325 | 38.71% | 19.97% | 41.32% |
| Scholarship holder | 1,099 | 12.19% | 11.83% | 75.98% |
| Not a debtor | 3,921 | 28.28% | 17.95% | 53.76% |
| Debtor | 503 | 62.03% | 17.89% | 20.08% |
| Tuition fees not up to date | 528 | 86.55% | 7.95% | 5.49% |
| Tuition fees up to date | 3,896 | 24.74% | 19.30% | 55.95% |
| Evening attendance (code 0) | 483 | 42.86% | 15.53% | 41.61% |
| Daytime attendance (code 1) | 3,941 | 30.80% | 18.24% | 50.95% |

Gender labels follow the UCI description. Scholarship, debtor, and tuition use 1 for yes and 0 for no.

The five most common parental qualification and occupation codes have graduate shares mostly between 43.4% and 58.9%. That range is narrower than the gap for tuition status or units approved. Mother's occupation code 9, the most common occupation code (1,577 students), has a dropout share of 31.1% and a graduate share of 52.2%.

Marital status code 1 covers 3,919 students. Codes 3, 5, and 6 cover 4, 25, and 6 students. International students number 110. Students with special educational needs number 51. Percentages for those small groups are unstable.

Mean unemployment is 11.616 for Dropout, 11.273 for Enrolled, and 11.639 for Graduate. Mean inflation is 1.284, 1.212, and 1.198. Mean GDP is -0.151, 0.053, and 0.082.

Among numerical features, the strongest Pearson correlations are between the matching semester-1 and semester-2 measures: credited units 0.945, enrolled units 0.943, approved units 0.904, grades 0.837, and evaluations 0.779. Same-semester approved units and grade correlate at 0.696 in semester 1 and 0.761 in semester 2. Previous-qualification grade and admission grade correlate at 0.580. Admission grade correlates at 0.074 with each semester grade average. Age correlates at -0.173 with the second-semester grade average.

## 6. Important visualisation interpretations

`figure_01_target_distribution.png` shows Graduate as the largest bar and Enrolled as the smallest. The imbalance is large enough that accuracy alone would be a weak later summary.

`figure_02_numerical_distributions.png` shows age piled toward the early twenties with a tail to 70, entry grades spread through the middle of the 0–200 scale, and semester grades with a visible mass at 0.

`figure_03_semester_grades_by_target.png` shows higher grade boxes for Graduate than for Dropout in both semesters. Enrolled sits between them. Outliers were hidden on that chart so the boxes stay readable; the zero-grade shares above are calculated from the full column.

`figure_04_academic_progression_by_target.png` shows that the mean number of units approved, not the mean number enrolled, is where the classes separate. Enrolled students have the highest mean number of evaluations, so more evaluations do not line up with graduation in this file.

`figure_05_age_by_target.png` shows a higher age box for Dropout than for Graduate. The medians are 23, 20, and 19.

`figure_06_selected_categoricals_by_target.png` shows the target mix inside gender, scholarship, debtor, and tuition codes. Tuition not up to date and debtor status have the largest dropout shares in that figure. Those two fields still have no measurement date.

`figure_07_numerical_correlation_heatmap.png` shows the semester-to-semester block of strong correlations. The short axis labels are defined in the notebook. Category codes are not in this heatmap.

## 7. Research question findings

**RQ1 — approved.** This exploration does not answer how effective Logistic Regression or Random Forest would be, because neither model was trained. It does show that the classes are imbalanced and that semester approval and grades differ across the classes, while some integer fields are codes rather than measurements. Those facts support keeping the planned metric set, and they support keeping the two planned algorithms as different families to compare later. They do not produce a performance result. The planned pair still stands as the plan. Training has not started.

**RQ2 — proposed, pending approval.** In this file, graduates have higher mean semester grades and more units approved than enrolled students, who in turn are ahead of dropout students on those measures. Units enrolled differ only modestly. A second-semester grade of 0 is common for dropout students and uncommon for graduates, and every such zero sits with zero approved units. This is a group difference, not evidence that the grade caused the outcome. The question is not approved.

**RQ3 — proposed, pending approval.** Gender, scholarship, daytime/evening attendance, debtor status, and tuition status show different target mixes. Age is higher on average in the dropout group. The most common parental education and occupation codes differ less. Entry grades are only weakly correlated with later semester grades. Macroeconomic means are close across classes, and their dates are unknown. These are observed associations. The question is not approved.

## 8. Data limitations

- `Debtor` and `Tuition fees up to date` have no measurement date. Their target associations are large, and the timing is still unresolved. No explanation of when they were recorded was added.
- `Unemployment rate`, `Inflation rate`, and `GDP` have no reference date. Class means are close, which does not identify the date.
- The UCI text for `Curricular units 2nd sem (without evaluations)` says the first semester, while the column name says the second. The column was not edited. Its median is 0 in every target class.
- The zip header for daytime/evening attendance contains a tab. Only the in-memory name was cleaned.
- Several category codes have very small counts, so their target percentages should not be treated as stable.
- A grade of 0 is exactly aligned with zero approved units. Whether 0 means "no graded units" or a genuine average is not stated.
- No relationship in this report is a causal effect.

## 9. Implications for preprocessing and modelling

- Keep Logistic Regression and Random Forest as the planned comparison. Do not train them in the EDA step.
- Keep macro-averaged metrics and a confusion matrix. Do not rely on accuracy alone.
- Encode integer category codes as categories. Do not scale those codes as continuous magnitudes.
- Decide later what a semester grade of 0 means before imputing or replacing it. This report does not change those values.
- Do not treat debtor status, tuition status, or the macroeconomic fields as known at the end of the second semester until their dates are justified.
- Course, nationality, and occupation codes have many levels. Any later encoding needs a documented rule. Rare marital-status levels should not drive that rule by themselves.

## 10. Summary of findings

The extracted file matches the audited shape of 4,424 students and 37 columns. Graduate is the largest class and Enrolled is the smallest. Semester grades and units approved differ much more across the three outcomes than units enrolled, entry grades, or the most common parental occupation codes. First-semester and second-semester records of the same kind are strongly correlated. Debtor status and tuition status also separate the outcomes, but their measurement dates remain unknown, as do the dates of the macroeconomic fields and the conflicting UCI wording for second-semester units without evaluations.
