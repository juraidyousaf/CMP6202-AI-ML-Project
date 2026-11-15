"""Checks for Phase 5 test metrics and class-label order."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

import model_evaluation as evaluation  # noqa: E402
import preprocessing as prep  # noqa: E402


class MetricTests(unittest.TestCase):
    def test_hand_calculated_example(self):
        actual = ["Dropout", "Enrolled", "Graduate", "Dropout"]
        predicted = ["Dropout", "Graduate", "Graduate", "Enrolled"]
        metrics = evaluation.evaluate_predictions(actual, predicted)

        self.assertEqual(metrics["labels"], ["Dropout", "Enrolled", "Graduate"])
        self.assertEqual(metrics["confusion_matrix"], [[1, 1, 0], [0, 0, 1], [0, 0, 1]])
        self.assertEqual(len(metrics["confusion_matrix"]), 3)
        self.assertEqual(len(metrics["confusion_matrix"][0]), 3)
        self.assertAlmostEqual(metrics["macro_f1"], 4 / 9)
        self.assertAlmostEqual(metrics["macro_precision"], 0.5)
        self.assertAlmostEqual(metrics["balanced_accuracy"], 0.5)
        self.assertAlmostEqual(metrics["accuracy"], 0.5)
        self.assertTrue(metrics["macro_recall_equals_balanced_accuracy"])
        self.assertNotIn("macro_recall", metrics)

        by_label = {row["label"]: row for row in metrics["per_class"]}
        self.assertEqual(list(by_label), list(prep.ALLOWED_LABELS))
        self.assertAlmostEqual(by_label["Dropout"]["precision"], 1)
        self.assertAlmostEqual(by_label["Dropout"]["recall"], 0.5)
        self.assertAlmostEqual(by_label["Dropout"]["f1"], 2 / 3)
        self.assertEqual(by_label["Dropout"]["support"], 2)
        self.assertAlmostEqual(by_label["Enrolled"]["precision"], 0)
        self.assertAlmostEqual(by_label["Enrolled"]["recall"], 0)
        self.assertAlmostEqual(by_label["Enrolled"]["f1"], 0)
        self.assertEqual(by_label["Enrolled"]["support"], 1)
        self.assertAlmostEqual(by_label["Graduate"]["precision"], 0.5)
        self.assertAlmostEqual(by_label["Graduate"]["recall"], 1)
        self.assertAlmostEqual(by_label["Graduate"]["f1"], 2 / 3)
        self.assertEqual(by_label["Graduate"]["support"], 1)

    def test_missing_class_in_the_actual_labels_is_rejected(self):
        with self.assertRaises(ValueError):
            evaluation.evaluate_predictions(
                ["Dropout", "Graduate"],
                ["Dropout", "Graduate"],
            )

    def test_unknown_prediction_label_is_rejected(self):
        with self.assertRaises(ValueError):
            evaluation.evaluate_predictions(
                ["Dropout", "Enrolled", "Graduate"],
                ["Dropout", "Enrolled", "Other"],
            )


if __name__ == "__main__":
    unittest.main()
