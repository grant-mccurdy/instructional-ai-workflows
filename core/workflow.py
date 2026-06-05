"""Deterministic workflow helpers for public-safe instructional demos.

The demo intentionally uses teacher annotations as the input to structured
evaluation. It does not claim to grade raw student work automatically.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class CriterionResult:
    criterion_id: str
    criterion_name: str
    level: str
    points: float
    max_points: float
    evidence: str
    private_note: str


def evaluate_submission(rubric: dict[str, Any], submission: dict[str, Any]) -> dict[str, Any]:
    criteria = {criterion["id"]: criterion for criterion in rubric["criteria"]}
    observations = {item["criterion_id"]: item for item in submission["teacher_observations"]}
    results: list[CriterionResult] = []

    for criterion_id, criterion in criteria.items():
        observation = observations.get(
            criterion_id,
            {
                "criterion_id": criterion_id,
                "level": "missing",
                "evidence": "No rubric-aligned evidence was annotated.",
                "private_note": "Teacher review required because no evidence was recorded.",
            },
        )
        level = observation["level"]
        level_config = criterion["levels"][level]
        results.append(
            CriterionResult(
                criterion_id=criterion_id,
                criterion_name=criterion["name"],
                level=level,
                points=float(level_config["points"]),
                max_points=float(criterion["max_points"]),
                evidence=observation["evidence"],
                private_note=observation["private_note"],
            )
        )

    total = round(sum(result.points for result in results), 2)
    max_points = round(sum(result.max_points for result in results), 2)
    review_required = any(result.level != "secure" for result in results)

    strengths = [
        f"{result.criterion_name}: {result.evidence}"
        for result in results
        if result.level == "secure"
    ]
    next_steps = [
        criteria[result.criterion_id]["levels"][result.level]["next_step"]
        for result in results
        if result.level != "secure"
    ]

    return {
        "submission_id": submission["submission_id"],
        "learner_alias": submission["learner_alias"],
        "score": total,
        "max_score": max_points,
        "review_required": review_required,
        "criterion_results": [result.__dict__ for result in results],
        "draft_feedback": {
            "strengths": strengths or ["Your response shows a clear attempt to use the task structure."],
            "next_steps": next_steps or ["Continue explaining each algebraic decision with a sentence tied to the context."],
            "release_note": submission["reviewer_edits"]["release_note"],
        },
        "reviewer_edits": submission["reviewer_edits"],
    }


def build_remediation_plan(evaluations: list[dict[str, Any]], rubric: dict[str, Any]) -> list[dict[str, Any]]:
    needs: dict[str, int] = {}
    for evaluation in evaluations:
        for result in evaluation["criterion_results"]:
            if result["level"] != "secure":
                needs[result["criterion_id"]] = needs.get(result["criterion_id"], 0) + 1

    plan = []
    for criterion in rubric["criteria"]:
        count = needs.get(criterion["id"], 0)
        if count:
            plan.append(
                {
                    "criterion_id": criterion["id"],
                    "focus": criterion["name"],
                    "students_flagged": count,
                    "activity": criterion["remediation_activity"],
                }
            )
    return plan
