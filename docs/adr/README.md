# Architecture decision records

Each file here records one decision: its context, what was decided, and the consequences.

## Writing an ADR

1. Copy [`template.md`](template.md) to `NNN-short-title.md`, using the next unused three-digit number.
2. Give it a title that states the decision, without the number.
3. Fill in each section, replacing the prompts.

## Status

An ADR is Proposed while the decision is open, and Accepted or Rejected once it's made. An ADR written after the
decision starts as Accepted or Rejected. Keep rejected ADRs: they record why an option wasn't taken.

Once an ADR is accepted or rejected, change only its status:

- Deprecated: the decision no longer applies, and nothing replaces it.
- `Superseded by [NNN](NNN-short-title.md)`: a newer ADR replaces it. To change a decision, write that new ADR.
