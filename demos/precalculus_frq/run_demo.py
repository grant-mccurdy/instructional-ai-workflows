#!/usr/bin/env python3
"""Build public-safe Precalculus FRQ workflow demo outputs."""

from __future__ import annotations

import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))

from core.workflow import build_remediation_plan, evaluate_submission


DEMO_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = REPO_ROOT / "sample_outputs" / "precalculus_frq"


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data) -> None:
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def write_reviewer_packet(path: Path, evaluations: list[dict], rubric: dict) -> None:
    lines = [
        "# Reviewer Packet: Precalculus FRQ",
        "",
        "This packet is teacher-facing. It uses synthetic submissions and rubric-aligned annotations only.",
        "",
        f"Review policy: {rubric['review_policy']}",
        "",
    ]
    for evaluation in evaluations:
        lines.extend(
            [
                f"## {evaluation['learner_alias']}",
                "",
                f"Score: {evaluation['score']} / {evaluation['max_score']}",
                f"Review required: {'yes' if evaluation['review_required'] else 'no'}",
                "",
                "### Criterion Evidence",
                "",
            ]
        )
        for result in evaluation["criterion_results"]:
            lines.extend(
                [
                    f"- **{result['criterion_name']}**: {result['level']} ({result['points']} / {result['max_points']})",
                    f"  Evidence: {result['evidence']}",
                    f"  Private note: {result['private_note']}",
                ]
            )
        lines.extend(
            [
                "",
                "### Approved Student-Facing Note",
                "",
                evaluation["reviewer_edits"]["release_note"],
                "",
            ]
        )
    path.write_text("\n".join(lines), encoding="utf-8")


def write_student_feedback(path: Path, evaluations: list[dict]) -> None:
    lines = [
        "# Reviewed Student Feedback: Precalculus FRQ",
        "",
        "These notes are synthetic examples of student-facing feedback after teacher review.",
        "",
    ]
    for evaluation in evaluations:
        lines.extend(
            [
                f"## {evaluation['learner_alias']}",
                "",
                evaluation["reviewer_edits"]["release_note"],
                "",
            ]
        )
    path.write_text("\n".join(lines), encoding="utf-8")


def write_remediation_plan(path: Path, plan: list[dict]) -> None:
    lines = [
        "# Remediation Plan: Precalculus FRQ",
        "",
        "This plan is generated from synthetic rubric evidence and is intended as a teacher planning aid.",
        "",
    ]
    for item in plan:
        lines.extend(
            [
                f"## {item['focus']}",
                "",
                f"Students flagged: {item['students_flagged']}",
                "",
                item["activity"],
                "",
            ]
        )
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    rubric = load_json(DEMO_DIR / "rubric.json")
    submissions = load_json(DEMO_DIR / "synthetic_submissions.json")
    evaluations = [evaluate_submission(rubric, submission) for submission in submissions]
    remediation_plan = build_remediation_plan(evaluations, rubric)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    write_json(OUTPUT_DIR / "structured-evaluations.json", evaluations)
    write_reviewer_packet(OUTPUT_DIR / "reviewer-packet.md", evaluations, rubric)
    write_student_feedback(OUTPUT_DIR / "student-feedback.md", evaluations)
    write_remediation_plan(OUTPUT_DIR / "remediation-plan.md", remediation_plan)
    print(f"wrote {OUTPUT_DIR.relative_to(REPO_ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
