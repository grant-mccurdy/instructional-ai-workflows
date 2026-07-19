#!/usr/bin/env python3
"""Validate the public demo's schema, review gates, and privacy assumptions."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEMO = ROOT / "demos" / "precalculus_frq"
OUTPUT = ROOT / "sample_outputs" / "precalculus_frq"


def fail(message: str) -> None:
    raise SystemExit(f"validation failed: {message}")


def main() -> int:
    rubric = json.loads((DEMO / "rubric.json").read_text(encoding="utf-8"))
    submissions = json.loads(
        (DEMO / "synthetic_submissions.json").read_text(encoding="utf-8")
    )
    evaluations = json.loads(
        (OUTPUT / "structured-evaluations.json").read_text(encoding="utf-8")
    )

    criterion_ids = {criterion["id"] for criterion in rubric["criteria"]}
    if not criterion_ids or len(criterion_ids) != len(rubric["criteria"]):
        fail("rubric criterion IDs must be unique and non-empty")
    if len(submissions) != len(evaluations):
        fail("every synthetic submission must produce one evaluation")

    submission_ids = {submission["submission_id"] for submission in submissions}
    evaluation_ids = {evaluation["submission_id"] for evaluation in evaluations}
    if submission_ids != evaluation_ids:
        fail("evaluation IDs do not match the synthetic source set")

    for submission in submissions:
        if not submission["submission_id"].startswith("synthetic_"):
            fail("submission IDs must be visibly synthetic")
        if not submission["learner_alias"].startswith("Synthetic Learner"):
            fail("learner aliases must be visibly synthetic")
        if set(item["criterion_id"] for item in submission["teacher_observations"]) != criterion_ids:
            fail(f"{submission['submission_id']} does not cover every rubric criterion")
        if not submission["reviewer_edits"].get("approved"):
            fail(f"{submission['submission_id']} has no explicit reviewer approval")

    student_feedback = (OUTPUT / "student-feedback.md").read_text(encoding="utf-8")
    private_notes = {
        item["private_note"]
        for submission in submissions
        for item in submission["teacher_observations"]
    }
    leaked_notes = sorted(note for note in private_notes if note in student_feedback)
    if leaked_notes:
        fail("teacher-only notes appear in the student-facing artifact")

    print(
        "validated "
        f"{len(evaluations)} synthetic evaluations, "
        f"{len(criterion_ids)} rubric criteria, and the human-review release gate"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
