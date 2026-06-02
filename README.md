# Instructional AI Workflows

LMS-agnostic instructional workflow prototypes for teacher-controlled grading, feedback, review, and remediation artifacts.

This repository is intended to demonstrate controlled AI-assisted instructional workflows. It should not be framed as automatic test grading. The public framing is:

```text
teacher-defined rubric
-> structured evaluation
-> draft feedback
-> human review
-> student-facing feedback/review/remediation artifact
```

## What This Project Demonstrates

- Automated workflow support for test and assignment review
- Rubric-defined structured evaluation
- Draft feedback artifact generation
- Review artifact generation
- Remediation artifact generation
- Human-in-the-loop grading and feedback
- LMS adapter architecture
- Static HTML, Markdown, and PDF output options

## Planned Structure

```text
instructional-ai-workflows/
├── core/
│   ├── grading/
│   ├── feedback_generation/
│   ├── review_generation/
│   └── remediation_generation/
├── adapters/
│   ├── canvas/
│   ├── static_html/
│   └── markdown/
├── demos/
│   ├── precalculus_frq/
│   └── ap_statistics_frq/
├── prompts/
├── sample_outputs/
├── docs/
│   ├── workflow-overview.md
│   ├── human-in-the-loop.md
│   └── privacy-and-safety.md
├── screenshots/
└── README.md
```

## Public Safety Rules

Public demos must use synthetic submissions, synthetic rubrics, fake course identifiers, and public-safe sample outputs.

Do not publish real student submissions, feedback, grades, comments, Canvas user IDs, assignment IDs, course IDs, API tokens, private screenshots, or teacher-only review artifacts.

## Portfolio Framing

Canvas should be presented as one adapter, not the product. The core value is the instructional workflow design: a teacher-defined, auditable process that supports consistent feedback and targeted remediation while keeping final judgment with the teacher.

## Status

Planning and public-safe scaffolding in progress.
