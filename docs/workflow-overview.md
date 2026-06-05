# Workflow Overview

This repository demonstrates a teacher-controlled instructional AI workflow
using synthetic public-safe artifacts.

The public demo pattern is:

```text
teacher-defined rubric
-> rubric-aligned teacher observations
-> structured evaluation
-> draft feedback
-> teacher review and edit
-> student-facing feedback and remediation plan
```

## Current Demo

`demos/precalculus_frq/` contains a synthetic Precalculus free-response task,
rubric, fake submissions, and a deterministic standard-library script.

Run:

```bash
make demo
```

Generated public-safe outputs are written to
`sample_outputs/precalculus_frq/`:

- `structured-evaluations.json`
- `reviewer-packet.md`
- `student-feedback.md`
- `remediation-plan.md`

## Design Boundary

The demo does not automatically grade raw student work. It starts from
rubric-aligned teacher observations so the public artifact shows the workflow
shape without claiming autonomous scoring.
