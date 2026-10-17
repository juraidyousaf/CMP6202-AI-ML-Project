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

If a value is unknown, write **TBD — to be decided after dataset selection.** Do not invent a dataset, target, score, citation, licence, or certificate.

---

## 1. Project Identity

| Field | Value |
| --- | --- |
| Module | CMP6202 Artificial Intelligence and Machine Learning |
| Repository | CMP6202-AI-ML-Project |
| Student ID | s24156365 |
| Workspace folder at time of writing | `CMP6202-AI-ML` (local working copy). The GitHub repository name to use is `CMP6202-AI-ML-Project`. |

## 2. Current Status

Planning stage. Six planning documents have been drafted under `docs/` and are waiting for student review. No dataset selected. No application code, notebooks, or dependencies installed. No experimental results exist.

## 3. Current Phase

Phase 0 — Planning & Repository Setup

Phase 0 exit criteria are not met yet. The documents still need student review. `README.md` and `.gitignore` do not exist yet.

## 4. Current Task

Student review of the initial planning documents.

## 5. Current File Being Worked On

None in progress. Last file written this session: `docs/Memory.md`.

## 6. Completed

Items marked done from the student's own start-of-project notes are labelled as student-reported. This session did not independently verify the GitHub account.

- [x] GitHub account created (student-reported; not re-verified in this session)
- [x] Repository name selected: CMP6202-AI-ML-Project (student-reported)
- [x] Coursework requirements reviewed (student-reported, and reflected in `docs/PRD.md`)
- [x] Documentation architecture planned
- [x] Six planning documents drafted in `docs/` (files exist on disk; student approval still open)

## 7. In Progress

- [ ] Student review and approval of the planning documents
- [ ] Rest of Phase 0: repository structure as needed, README skeleton, `.gitignore`, Python environment decision

## 8. Next Actions

1. Read `docs/PRD.md`, `docs/Architecture.md`, `docs/Rules.md`, `docs/Phases.md`, `docs/Design.md`, and this file. Correct anything that disagrees with the official module brief.
2. Approve the planning docs, or list changes. That approval is the Phase 0 content gate.
3. Add a README skeleton and a `.gitignore`. Create other folders only when a file is about to go in them.
4. Shortlist publicly available open-access datasets. Do not lock a dataset until the licence, the source URL, and a row count of at least 3,000 are checked.
5. After selection, define the target, classification or regression, one report audience, and 2–3 research questions. Update this file in the same session.

## 9. Decisions Made

| Date | Decision | Reason |
| --- | --- | --- |
| 2026-10-17 | The repository will be public. | Coursework requires a public GitHub repository. |
| 2026-10-17 | A personal GitHub account is acceptable. | Student decision recorded at planning start. |
| 2026-10-17 | The final dataset has not been selected. | Selection is Phase 1 and must follow a licence and size check. |
| 2026-10-17 | The final report will not be generated until the ML work is sufficiently complete. | The report must be built from real outputs. These markdown files are planning documents only. |
| 2026-10-17 | The default modelling stack is Python with pandas, numpy, scikit-learn, and matplotlib. | Conservative coursework stack. Other libraries need a written justification. See `docs/Rules.md`. |
| 2026-10-17 | No numeric success threshold will be set before a baseline exists. | A threshold would be an invented target. See `docs/PRD.md` section 8. |

## 10. Open Decisions

All of the following are **TBD — to be decided after dataset selection**, except certifications, which the student chooses from real AI/ML certification options.

- Dataset
- Task type (classification or regression)
- Target variable
- Research questions
- Algorithms
- Metrics
- Certifications to complete
- Project / report title
- Explicit report target audience
- Python environment location and exact package versions
- Train/test ratio and `random_state` (decide in Phase 5, then record them here)

## 11. Files Created

| Path | Purpose | Status |
| --- | --- | --- |
| `docs/PRD.md` | Requirements, deliverables, success criteria, open decisions | Drafted 2026-10-17; pending student review |
| `docs/Architecture.md` | ML workflow, intended repo layout, leakage and reproducibility rules | Drafted 2026-10-17; pending student review |
| `docs/Rules.md` | Engineering, data, ML, AI, and academic-integrity rules for later agents | Drafted 2026-10-17; pending student review |
| `docs/Phases.md` | Checkbox roadmap from planning through submission QA | Drafted 2026-10-17; pending student review |
| `docs/Design.md` | Chart, table, notebook, and report-figure standards | Drafted 2026-10-17; pending student review |
| `docs/Memory.md` | Living project state | Drafted 2026-10-17; pending student review |

Not created, on purpose: README, `.gitignore`, `requirements.txt`, notebooks, `src/`, data files, figures, models, and the report.

## 12. Experimental Results

No experiments have been performed yet.

Later entries in this section must contain verified results only. Each entry needs the date, the command or notebook that produced it, the metric names, the values copied from output, and the file they were saved to. If a run fails, record the failure. Do not fill this section with expected or typical scores.

## 13. Issues / Blockers

None.

The local folder name (`CMP6202-AI-ML`) and the intended GitHub repository name (`CMP6202-AI-ML-Project`) differ. This is a naming note, not a blocker. Keep using `CMP6202-AI-ML-Project` as the public repository name unless the student chooses otherwise.

## 14. AI Assistance Log

| Date | AI Tool | Task | Verification Performed |
| --- | --- | --- | --- |
| 2026-10-17 | Cursor (coding agent) | Project planning and documentation: drafted the six files in `docs/` from the student's coursework constraints. No dataset, model, or result was selected. | Human review required. The student must read the six documents against the official brief before treating them as approved. No code was run. No statistics were produced. |

Add a row whenever an AI tool drafts code, analysis, citations, or report text. Verification means what the student (or a rerun) actually checked.

## 15. Session Handoff

**Completed this session**

- Created `docs/PRD.md`, `docs/Architecture.md`, `docs/Rules.md`, `docs/Phases.md`, `docs/Design.md`, and `docs/Memory.md`.
- Left dataset, target, task type, algorithms, metrics, audience, title, and results undecided.

**Currently being worked on**

- Nothing. Waiting for the student to review the planning documents.

**Exact next task**

- Student reviews the six documents against the module brief. After approval, create the README skeleton and `.gitignore` only. Do not select a dataset in that same mechanical step unless the student has started Phase 1.

**Constraints the next session must keep**

- Academic ML coursework, not a production product.
- Public open-access dataset, at least 3,000 rows, about 3,000–5,000 recommended.
- Classification or regression, decided only after the dataset is known.
- At least two algorithms, appropriate metrics, cross-validation, hyperparameter tuning, and a fair comparison.
- No leakage: fit preprocessing and tuning on training data only.
- No fabricated data, scores, citations, licences, or certificates.
- No TensorFlow, PyTorch, boosting libraries, web frameworks, Docker, or agent frameworks unless a later written justification exists.
- AI-assisted work must be verified and logged in section 14.
- Do not write the final report yet.
- Update this file at the end of the next meaningful session.
