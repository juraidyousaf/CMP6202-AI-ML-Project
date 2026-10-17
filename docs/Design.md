# Visual and Documentation Design System

Visual standards for this coursework project. There is no web UI. These rules apply to charts, tables, Markdown, notebooks, and figures that may appear in the report.

Student ID: s24156365  
Repository: CMP6202-AI-ML-Project

Do not invent chart findings to match this style guide. A figure is valid only after it is generated from the dataset and inspected.

---

## 1. Design Principles

- **Academic** — the work should look like a careful study, suitable for a marker.
- **Clean** — remove grid noise, decorative ink, and chartjunk.
- **Readable** — a reader can see the comparison without decoding the graphic.
- **Professional** — consistent sizes, labels, and file names.
- **Minimal** — one chart, one main message.
- **Consistent** — the same kind of chart uses the same size, type sizes, and colour roles across the project.
- **Data-first** — colour, annotations, and titles serve the measured data. They do not decorate an empty template.

## 2. Color & Theme

Custom colours are optional. Matplotlib defaults are acceptable when they stay readable. When a project palette is applied, use only these roles.

**Primary academic palette**

| Role | Hex | Use |
| --- | --- | --- |
| Deep navy | `#163A5F` | Titles, primary series, header rules |
| Slate | `#4B5563` | Axis labels, secondary text, secondary series |
| Light background | `#F8FAFC` | Figure or table background when a tint is needed |
| Border / light neutral | `#E5E7EB` | Spines, light gridlines, table borders |
| Success / accent | `#2E7D32` | A justified positive highlight |
| Warning / accent | `#B7791F` | A justified caution |
| Error / accent | `#B91C1C` | A justified negative or error series |

**Rules**

- Prefer white or light backgrounds.
- Avoid neon colours.
- Avoid highly saturated rainbow palettes. Use one colour per real category, not one colour per bar "to make it interesting".
- Charts should remain understandable in grayscale where possible. Differentiate series with line style or marker shape as well as colour.
- Do not imply meaning through colour alone. The legend, labels, or caption must carry the category.
- Use red and green together only with a second cue (label, marker, or pattern). Many readers cannot separate them.

## 3. Fonts

**Word / report**

- Use a university-compatible default: Arial 11, or whatever typeface and size the official template already sets.
- Do not override the official template to match this file.

**Markdown / code**

- Use the system sans-serif for rendered documentation.
- Use monospace for code, paths, column names, and metric identifiers.

## 4. Typography

- Use H1 for the document title only.
- Use H2 for major sections.
- Use H3 for subsections.
- Keep headings concise and descriptive.
- Use normal body text for explanation.
- Use bold for a short emphasis, not for whole paragraphs.
- Avoid decorative formatting: coloured body text, all caps headings, and ornamental separators.

Notebook and markdown heading order should not skip from H1 to H3 without an H2.

## 5. Chart Standards

Every figure that may enter the report must have:

- a descriptive title that states what is being compared
- an x-axis label
- a y-axis label
- units in the axis label or title when the quantity has units
- a readable legend when more than one series is shown
- tick labels that do not overlap
- a figure size that stays legible in a report column (a practical default is about 8 by 5 inches, adjusted when the chart needs to be wider)
- no 3D effects
- axes that are not truncated in a misleading way; if a truncated axis is necessary, the caption says so
- a high-resolution export when the figure is used in the report (for example 150–300 dpi PNG)

Additional rules:

- Sort bars by value or by a meaningful category order, and say which order was used if it matters.
- Histograms and bar charts of the target must use the real class names or a clearly defined binning.
- Correlation heatmaps need a colour bar and feature names that remain readable. Drop or abbreviate names only with a key.
- Save report figures into `figures/` using the names in section 8.
- Do not add a title that states a conclusion the plotted data does not show.

## 6. Table Standards

- Use concise headers.
- Put units in the header when the column has units (for example `RMSE (minutes)`).
- Use a consistent number of decimal places within a column. Four decimal places is a reasonable default for rates and scores; choose a coarser rounding when the unit does not support false precision.
- Keep tables narrow enough for the report. Split a wide comparison rather than shrinking the type below readability.
- Highlight a "best" model only when the selection rule is stated (for example highest F1 on the test set). Do not highlight a cell because it looks impressive.
- Give every report table a caption or label, and refer to that label in the text.
- Build comparison tables in code and save them under `outputs/tables/` or `outputs/metrics/`. Do not retype numbers by hand.

## 7. Notebook Presentation

Each analysis block should follow this order:

1. A Markdown heading.
2. A short explanation of the question this block answers.
3. The code.
4. The output.
5. A short interpretation of that output.

Further rules:

- Do not dump an entire dataframe, a full correlation printout of dozens of columns, or every tuning trial into the notebook as the final form. Show the summary that supports the decision, and save the full artefact if it is needed.
- State the assumption before a transform (for example why a median imputer was used).
- If a cell errors, fix it or remove it before submission. A notebook that stops halfway is not the documented path.
- Keep interpretation in Markdown so it is visible without reading the code.

## 8. Report Figure Naming

Use numbered, descriptive file names. Examples of the pattern:

- `figure_01_target_distribution.png`
- `figure_02_correlation_heatmap.png`
- `figure_03_model_comparison.png`

Rules:

- Continue the sequence as real figures are created (`figure_04_...`, and so on).
- The slug after the number should say what the chart contains.
- Do not create these files in advance with empty or placeholder images.
- If a figure is removed, do not silently reuse its number for a different chart in the same report draft. Note the change in `docs/Memory.md`.
- Match the file name, the notebook that writes it, and the caption in the report.

## 9. Accessibility

- Keep contrast high: dark text or lines on a light background.
- Avoid red/green-only distinctions. Add labels, markers, or line styles.
- Use readable font sizes in figures (axis labels and ticks should still be legible when the figure is placed in the report).
- Legends and nearby text should name the categories. Colour is a supplement.
- Do not place important information in a colour bar alone without a label and units.
