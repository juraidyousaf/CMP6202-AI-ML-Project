"""Plot the approved model-comparison figure from saved Phase 5 outputs.

Reads evaluation files only. Does not train, tune, predict, or evaluate a model.
"""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
EVALUATION_DIR = ROOT / "outputs" / "evaluation"
FIGURE_PATH = (
    ROOT / "figures" / "model_comparison" / "figure_01_model_comparison_f1.png"
)

CLASS_ORDER = ("Dropout", "Enrolled", "Graduate")
CV_MODELS = ("logistic_regression", "random_forest")
HOLDOUT_MODELS = ("dummy_most_frequent", "logistic_regression", "random_forest")
DISPLAY_NAMES = {
    "dummy_most_frequent": "Dummy (most frequent)",
    "logistic_regression": "Logistic Regression",
    "random_forest": "Random Forest",
}
COLOURS = {
    "dummy_most_frequent": "#B7791F",
    "logistic_regression": "#163A5F",
    "random_forest": "#4B5563",
}
HATCHES = {
    "dummy_most_frequent": "...",
    "logistic_regression": "",
    "random_forest": "//",
}


def _load_selected_cv(path: Path, model_name: str) -> float:
    frame = pd.read_csv(path)
    selected = frame.loc[frame["selected"] == True]  # noqa: E712 — saved boolean column
    if len(selected) != 1:
        raise ValueError(f"{path.name} must contain exactly one selected row.")
    row = selected.iloc[0]
    if model_name == "logistic_regression":
        if float(row["C"]) != 0.1 or str(row["class_weight"]) != "balanced":
            raise ValueError("Selected logistic row does not match the frozen parameters.")
    if model_name == "random_forest":
        if (
            int(row["n_estimators"]) != 200
            or int(row["max_depth"]) != 20
            or int(row["min_samples_leaf"]) != 1
            or str(row["class_weight"]) != "balanced"
        ):
            raise ValueError("Selected forest row does not match the frozen parameters.")
    return float(row["mean_cv_macro_f1"])


def _require_match(label: str, saved: float, other: float) -> None:
    if saved != other:
        raise ValueError(f"{label} differs between saved files: {saved} and {other}.")


def load_plot_values() -> dict[str, object]:
    parameters = json.loads(
        (EVALUATION_DIR / "selected_parameters.json").read_text(encoding="utf-8")
    )
    test_metrics = json.loads(
        (EVALUATION_DIR / "test_metrics.json").read_text(encoding="utf-8")
    )
    test_table = pd.read_csv(EVALUATION_DIR / "test_metrics.csv")
    per_class = pd.read_csv(EVALUATION_DIR / "per_class_metrics.csv")

    cv_means: dict[str, float] = {}
    for model_name, filename in (
        ("logistic_regression", "logistic_regression_cv_results.csv"),
        ("random_forest", "random_forest_cv_results.csv"),
    ):
        csv_value = _load_selected_cv(EVALUATION_DIR / filename, model_name)
        json_value = float(parameters["models"][model_name]["mean_cv_macro_f1"])
        _require_match(f"{model_name} CV macro F1", csv_value, json_value)
        cv_means[model_name] = csv_value

    if "dummy_most_frequent" in parameters["models"]:
        raise ValueError("A dummy CV score was saved, so this plot must not omit it.")

    holdout_macro: dict[str, float] = {}
    per_class_f1: dict[str, dict[str, float]] = {}
    for model_name in HOLDOUT_MODELS:
        json_macro = float(test_metrics[model_name]["macro_f1"])
        csv_rows = test_table.loc[test_table["model"] == model_name, "macro_f1"]
        if len(csv_rows) != 1:
            raise ValueError(f"{model_name} must have one holdout macro F1 row.")
        _require_match(f"{model_name} holdout macro F1", json_macro, float(csv_rows.iloc[0]))
        holdout_macro[model_name] = json_macro

        labels = tuple(test_metrics[model_name]["labels"])
        if labels != CLASS_ORDER:
            raise ValueError(f"{model_name} class order is {labels}, not {CLASS_ORDER}.")
        per_class_f1[model_name] = {}
        for item in test_metrics[model_name]["per_class"]:
            label = item["label"]
            json_f1 = float(item["f1"])
            csv_f1 = per_class.loc[
                (per_class["model"] == model_name) & (per_class["label"] == label),
                "f1",
            ]
            if len(csv_f1) != 1:
                raise ValueError(f"{model_name} {label} must have one per-class F1 row.")
            _require_match(f"{model_name} {label} F1", json_f1, float(csv_f1.iloc[0]))
            per_class_f1[model_name][label] = json_f1

    return {
        "cv_means": cv_means,
        "holdout_macro": holdout_macro,
        "per_class_f1": per_class_f1,
    }


def _label_bars(axis, bars, values: list[float]) -> None:
    for bar, value in zip(bars, values, strict=True):
        text = f"{value:.3f}"
        if value >= 0.12:
            axis.text(
                bar.get_x() + bar.get_width() / 2,
                value - 0.045,
                text,
                ha="center",
                va="top",
                color="white",
                fontsize=8,
            )
        else:
            axis.text(
                bar.get_x() + bar.get_width() / 2,
                value + 0.03,
                text,
                ha="center",
                va="bottom",
                color="#163A5F",
                fontsize=8,
            )


def _style_axis(axis) -> None:
    axis.set_ylim(0, 1.08)
    axis.set_yticks([0, 0.2, 0.4, 0.6, 0.8, 1.0])
    axis.spines["top"].set_visible(False)
    axis.spines["right"].set_visible(False)
    axis.grid(axis="y", color="#E5E7EB", linewidth=0.6)
    axis.set_axisbelow(True)


def plot_comparison(values: dict[str, object], destination: Path) -> None:
    cv_means = values["cv_means"]
    holdout_macro = values["holdout_macro"]
    per_class_f1 = values["per_class_f1"]

    plt.rcParams.update(
        {
            "figure.facecolor": "white",
            "axes.facecolor": "white",
            "axes.edgecolor": "#4B5563",
            "axes.labelcolor": "#163A5F",
            "axes.titlecolor": "#163A5F",
            "xtick.color": "#4B5563",
            "ytick.color": "#4B5563",
            "text.color": "#163A5F",
            "font.size": 11,
            "axes.titlesize": 12,
            "axes.labelsize": 11,
        }
    )

    figure = plt.figure(figsize=(11, 8.2))
    grid = figure.add_gridspec(2, 2, height_ratios=[1, 1.2], hspace=0.38, wspace=0.28)
    panel_a = figure.add_subplot(grid[0, 0])
    panel_b = figure.add_subplot(grid[0, 1])
    panel_c = figure.add_subplot(grid[1, :])

    cv_values = [cv_means[model] for model in CV_MODELS]
    cv_bars = panel_a.bar(
        [DISPLAY_NAMES[model] for model in CV_MODELS],
        cv_values,
        color=[COLOURS[model] for model in CV_MODELS],
        hatch=[HATCHES[model] for model in CV_MODELS],
        edgecolor="white",
        width=0.62,
    )
    _label_bars(panel_a, cv_bars, cv_values)
    panel_a.set_title("A. Validation: five-fold CV macro F1")
    panel_a.set_ylabel("Macro F1")
    panel_a.set_xlabel("Selected model")
    _style_axis(panel_a)
    panel_a.tick_params(axis="x", labelsize=9)

    holdout_values = [holdout_macro[model] for model in HOLDOUT_MODELS]
    holdout_bars = panel_b.bar(
        [DISPLAY_NAMES[model] for model in HOLDOUT_MODELS],
        holdout_values,
        color=[COLOURS[model] for model in HOLDOUT_MODELS],
        hatch=[HATCHES[model] for model in HOLDOUT_MODELS],
        edgecolor="white",
        width=0.72,
    )
    _label_bars(panel_b, holdout_bars, holdout_values)
    panel_b.set_title("B. Unseen test: holdout macro F1")
    panel_b.set_ylabel("Macro F1")
    panel_b.set_xlabel("Model")
    _style_axis(panel_b)
    panel_b.tick_params(axis="x", labelsize=8)

    positions = np.arange(len(CLASS_ORDER))
    width = 0.24
    for offset, model_name in enumerate(HOLDOUT_MODELS):
        class_values = [per_class_f1[model_name][label] for label in CLASS_ORDER]
        bars = panel_c.bar(
            positions + (offset - 1) * width,
            class_values,
            width=width,
            label=DISPLAY_NAMES[model_name],
            color=COLOURS[model_name],
            hatch=HATCHES[model_name],
            edgecolor="white",
        )
        _label_bars(panel_c, list(bars), class_values)
    panel_c.set_xticks(positions, CLASS_ORDER)
    panel_c.set_title("C. Unseen test: per-class holdout F1")
    panel_c.set_ylabel("F1")
    panel_c.set_xlabel("Class, in saved label order")
    _style_axis(panel_c)
    panel_c.legend(frameon=False, ncol=3, loc="upper left")

    figure.suptitle(
        "Model comparison using saved F1 values",
        fontsize=14,
        color="#163A5F",
    )
    figure.text(
        0.5,
        0.01,
        "Panels A and B are separate. Bar labels are rounded to 3 decimal places; bar heights use the saved values. "
        "The dummy was not cross-validated. Cross-validation is training-only validation, not training-set performance.",
        ha="center",
        va="bottom",
        fontsize=8,
        color="#4B5563",
    )
    destination.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(destination, dpi=200, bbox_inches="tight")
    plt.close(figure)


def main() -> None:
    values = load_plot_values()
    plot_comparison(values, FIGURE_PATH)
    print(FIGURE_PATH)
    print("cv", values["cv_means"])
    print("holdout", values["holdout_macro"])
    print("per_class", values["per_class_f1"])


if __name__ == "__main__":
    main()
