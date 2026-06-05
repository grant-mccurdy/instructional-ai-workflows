# Human-In-The-Loop Review

The control point is teacher review.

The demo separates three surfaces:

- structured evidence for the teacher
- private reviewer notes
- approved student-facing feedback

Generated drafts are not considered released until the teacher approves or edits
the language. This keeps student-facing artifacts aligned with the teacher's
judgment, classroom context, and local expectations.

## Release Rule

A workflow implementation should treat generated feedback as private by default.
Only the reviewed `release_note` should be exported to student-facing formats.

## Review Triggers

The current deterministic demo marks a response for review whenever any rubric
criterion is below `secure`. A real implementation could add more triggers, but
the public scaffold keeps the rule simple and auditable.
