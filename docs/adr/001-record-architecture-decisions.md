# Record architecture decisions

## Status

Accepted

## Context

Some decisions in this fork can't be explained by the code alone. A choice not to do something, such as not fetching
pages through calibre's Camoufox browser, leaves nothing in the code at all. Without a record, the same question gets
asked and answered again, and the conditions that would change the answer are lost.

The existing places don't fit. `AGENTS.md` describes how to work in the repository, and issues track something that is
broken or missing until it is fixed. Neither holds a decision, its reasons, and when to revisit it.

## Decision

Record decisions as architecture decision records (ADRs) in `docs/adr/`, one file per decision, named
`NNN-short-title.md` and numbered in order.

Use the template from Michael Nygard's
[Documenting Architecture Decisions](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions), as
published in the
[architecture-decision-record](https://github.com/architecture-decision-record/architecture-decision-record/tree/86893bc0b2dc86e1b10dff953bfd0709f85fb63c/locales/en-001/templates/decision-record-template-by-michael-nygard)
repository. [`template.md`](template.md) holds the template section of that page, unchanged. It is CC0. Each ADR has
the sections Status, Context, Decision, and Consequences, under a title with no number.

Write a new ADR by copying `template.md` to the next number. Don't use
[adr-tools](https://github.com/npryce/adr-tools), which the source page suggests:

- It numbers files with four digits and puts the number in the title (`# 1. Title`).
- It only reads a template from `templates/template.md` that uses its own placeholders (`NUMBER`, `TITLE`, `DATE`,
  `STATUS`), so `template.md` couldn't stay as published.
- It has had no release since 3.0.0 in 2018 and no commits since 2020.

Once an ADR is accepted, don't rewrite its decision. To change a decision, write a new ADR and mark the old one as
superseded by it.

## Consequences

The reasons behind a decision, and what would change it, can be found next to the code.

Writing an ADR is an extra step when making a decision, and picking the next number and marking superseded ADRs are
done by hand. Older ADRs stay in place after they are superseded, so the directory keeps growing.
