#!/usr/bin/env python3
"""Render the synthetic workflow output as a static reviewer demo."""

from __future__ import annotations

import html
import json
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from core.workflow import approved_release_note
OUTPUT = ROOT / ".pages"
DATA = ROOT / "sample_outputs" / "precalculus_frq" / "structured-evaluations.json"
RUBRIC = ROOT / "demos" / "precalculus_frq" / "rubric.json"


def esc(value: object) -> str:
    return html.escape(str(value))


def learner_section(evaluation: dict) -> str:
    note = approved_release_note(evaluation)
    status = "Teacher approved" if note is not None else "Awaiting teacher approval"
    status_class = "ready" if note is not None else "review"
    review_history = "Flagged by rubric checks; reviewed by the teacher." if evaluation["review_required"] else "Rubric checks passed; reviewed by the teacher."
    if note is None:
        review_history = "Draft held. Teacher review is required before release."
    note_heading = "Approved student-facing note" if note is not None else "Student-facing note withheld"
    note_text = note if note is not None else "No feedback is released until the teacher approves a completed note."
    rows = "".join(
        f"""
        <tr>
          <th scope="row">{esc(result['criterion_name'])}</th>
          <td><span class="level level-{esc(result['level'])}">{esc(result['level'])}</span></td>
          <td>{result['points']:g} / {result['max_points']:g}</td>
          <td>{esc(result['evidence'])}</td>
        </tr>"""
        for result in evaluation["criterion_results"]
    )
    return f"""
    <section class="learner" aria-labelledby="{esc(evaluation['submission_id'])}-title">
      <div class="learner-heading">
        <div>
          <p class="eyebrow">{esc(evaluation['submission_id'])}</p>
          <h2 id="{esc(evaluation['submission_id'])}-title">{esc(evaluation['learner_alias'])}</h2>
        </div>
        <div class="score-block">
          <strong>{evaluation['score']:g}<span> / {evaluation['max_score']:g}</span></strong>
          <span class="status {status_class}">{status}</span>
        </div>
      </div>
      <p class="review-history">{review_history}</p>
      <div class="table-wrap" role="region" aria-label="Rubric evidence for {esc(evaluation['learner_alias'])}" tabindex="0">
        <table>
          <thead><tr><th>Criterion</th><th>Level</th><th>Score</th><th>Teacher evidence</th></tr></thead>
          <tbody>{rows}</tbody>
        </table>
      </div>
      <div class="release-note">
        <p class="eyebrow">{note_heading}</p>
        <p>{esc(note_text)}</p>
      </div>
    </section>"""


def main() -> int:
    evaluations = json.loads(DATA.read_text(encoding="utf-8"))
    rubric = json.loads(RUBRIC.read_text(encoding="utf-8"))
    review_count = sum(item["review_required"] for item in evaluations)
    learners = "".join(learner_section(item) for item in evaluations)

    page = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="Synthetic, teacher-controlled instructional AI workflow demo.">
  <title>Instructional AI Workflow Demo</title>
  <link rel="stylesheet" href="styles.css">
</head>
<body>
  <header class="masthead">
    <nav aria-label="Project links">
      <a class="brand" href="#main">Instructional AI Workflows</a>
      <div>
        <a href="https://github.com/grant-mccurdy/instructional-ai-workflows">Source</a>
        <a href="https://grant-mccurdy.github.io/">Portfolio</a>
      </div>
    </nav>
    <div class="hero">
      <div>
        <p class="eyebrow">Workflow automation · Synthetic example</p>
        <h1>Consistent feedback.<br>Human judgment.</h1>
        <p class="lede">Turn rubric evidence into a review packet and approved feedback. Every release requires an explicit teacher decision.</p>
        <p class="demo-context">Static walkthrough · Three fictional learners · No live AI calls</p>
        <div class="hero-links"><a class="primary-link" href="#main">Inspect the workflow <span aria-hidden="true">↓</span></a><a href="https://github.com/grant-mccurdy/instructional-ai-workflows">Review the source</a></div>
      </div>
      <dl class="summary" aria-label="Demo summary">
        <div><dt>Submissions</dt><dd>{len(evaluations)}</dd></div>
        <div><dt>Flagged before review</dt><dd>{review_count}</dd></div>
        <div><dt>Teacher-approved notes</dt><dd>{sum(approved_release_note(item) is not None for item in evaluations)}</dd></div>
      </dl>
    </div>
  </header>
  <main id="main">
    <section class="workflow" aria-labelledby="workflow-title">
      <div>
        <p class="eyebrow">Control model</p>
        <h2 id="workflow-title">A visible human-review boundary</h2>
      </div>
      <ol>
        <li><span>01</span><strong>Define</strong><small>Teacher-authored rubric</small></li>
        <li><span>02</span><strong>Structure</strong><small>Rubric-aligned evidence</small></li>
        <li><span>03</span><strong>Draft</strong><small>Feedback and next steps</small></li>
        <li><span>04</span><strong>Review</strong><small>Teacher edits and approval</small></li>
        <li><span>05</span><strong>Release</strong><small>Student-safe artifact</small></li>
      </ol>
      <p class="policy"><strong>Review policy:</strong> {esc(rubric['review_policy'])}</p>
      <p class="policy">This saved example begins with teacher-authored observations and ends with recorded approvals. Rubric flags describe the initial review needs; approval determines whether a note may be exported.</p>
    </section>
    <div class="learner-list">{learners}</div>
  </main>
  <footer>
    <p>Public demo. All learners, observations, scores, and course context are synthetic.</p>
    <a href="https://github.com/grant-mccurdy/instructional-ai-workflows/blob/main/docs/privacy-and-safety.md">Privacy and safety notes</a>
  </footer>
</body>
</html>
"""
    OUTPUT.mkdir(parents=True, exist_ok=True)
    (OUTPUT / "index.html").write_text(page, encoding="utf-8")
    shutil.copyfile(ROOT / "pages" / "styles.css", OUTPUT / "styles.css")
    print(f"rendered {OUTPUT / 'index.html'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
