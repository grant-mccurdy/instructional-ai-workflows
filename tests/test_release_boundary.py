"""Exercise failed approvals at both public-output boundaries."""
import copy
import json
import tempfile
import unittest
from pathlib import Path

from demos.precalculus_frq.run_demo import write_student_feedback
from scripts.build_pages import learner_section

ROOT = Path(__file__).resolve().parents[1]


class ReleaseBoundaryTest(unittest.TestCase):
    def setUp(self):
        self.examples = json.loads((ROOT / "sample_outputs/precalculus_frq/structured-evaluations.json").read_text())

    def test_unapproved_or_empty_notes_never_reach_student_artifacts(self):
        for edits in ({"approved": False}, {}, {"approved": "true"}, {"approved": True, "release_note": " "}):
            with self.subTest(edits=edits), tempfile.TemporaryDirectory() as directory:
                examples = copy.deepcopy(self.examples)
                examples[1]["reviewer_edits"] = {"release_note": "UNREVIEWED SENTINEL", **edits}
                target = Path(directory) / "feedback.md"
                target.write_text("Previously approved artifact")
                with self.assertRaises(ValueError):
                    write_student_feedback(target, examples)
                self.assertEqual(target.read_text(), "Previously approved artifact")
                rendered = learner_section(examples[1])
                self.assertIn("Student-facing note withheld", rendered)
                self.assertNotIn("UNREVIEWED SENTINEL", rendered)
                self.assertNotIn("Approved student-facing note", rendered)

    def test_approved_export_excludes_private_notes(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "feedback.md"
            write_student_feedback(target, self.examples)
            text = target.read_text()
            for example in self.examples:
                self.assertIn(example["reviewer_edits"]["release_note"], text)
                self.assertIn("Teacher approved", learner_section(example))
                for criterion in example["criterion_results"]:
                    self.assertNotIn(criterion["private_note"], text)


if __name__ == "__main__":
    unittest.main()
