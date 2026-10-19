# Human-In-The-Loop Review

The control point is teacher review.

The demo separates three surfaces:

- structured evidence for the teacher
- private reviewer notes
- approved student-facing feedback

Generated drafts are not considered released until the teacher explicitly approves
the final language. Editing alone does not authorize release. This keeps student-facing artifacts aligned with the teacher's
judgment, classroom context, and local expectations.

## Release Rule

The student-feedback export validates the entire batch before writing. Every
note must have `approved: true` (a boolean) and nonempty `release_note` text.
Missing, false, string-valued, or empty approvals block the export. The HTML
walkthrough withholds the note when the same release condition is not met.
Private reviewer notes remain outside the student-facing artifact.

## Review Triggers

The current deterministic demo marks a response for review whenever any rubric
criterion is below `secure`. A real implementation could add more triggers, but
the public scaffold keeps the rule simple and auditable. This flag records a
need found before teacher review; it is distinct from the final approval state.
