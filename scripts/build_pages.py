#!/usr/bin/env python3
"""Render the synthetic workflow output as a static reviewer demo."""

from __future__ import annotations

import html
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / ".pages"
DATA = ROOT / "sample_outputs" / "precalculus_frq" / "structured-evaluations.json"
RUBRIC = ROOT / "demos" / "precalculus_frq" / "rubric.json"


def esc(value: object) -> str:
    return html.escape(str(value))


def learner_section(evaluation: dict) -> str:
    status = "Review required" if evaluation["review_required"] else "Ready after final check"
    status_class = "review" if evaluation["review_required"] else "ready"
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
      <div class="table-wrap">
        <table>
          <thead><tr><th>Criterion</th><th>Level</th><th>Score</th><th>Teacher evidence</th></tr></thead>
          <tbody>{rows}</tbody>
        </table>
      </div>
      <div class="release-note">
        <p class="eyebrow">Approved student-facing note</p>
        <p>{esc(evaluation['reviewer_edits']['release_note'])}</p>
      </div>
    </section>"""


def main() -> int:
    evaluations = json.loads(DATA.read_text(encoding="utf-8"))
    rubric = json.loads(RUBRIC.read_text(encoding="utf-8"))
    review_count = sum(item["review_required"] for item in evaluations)
    average = sum(item["score"] for item in evaluations) / sum(
        item["max_score"] for item in evaluations
    )
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
        <p class="eyebrow">Synthetic Precalculus FRQ</p>
        <h1>Teacher-controlled review, from rubric evidence to approved feedback.</h1>
        <p class="lede">A deterministic demonstration of how structured observations can support consistent feedback while keeping every release decision with the teacher.</p>
      </div>
      <dl class="summary" aria-label="Demo summary">
        <div><dt>Submissions</dt><dd>{len(evaluations)}</dd></div>
        <div><dt>Need review</dt><dd>{review_count}</dd></div>
        <div><dt>Points earned</dt><dd>{average:.0%}</dd></div>
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
