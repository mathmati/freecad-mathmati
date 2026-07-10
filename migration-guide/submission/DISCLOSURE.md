PREPARED DRAFT — awaiting user review and sign-off before any external submission.

# AI-Assistance Disclosure — FreeCAD Migration Guide addon

This document is the standing AI-assistance disclosure for the FreeCAD
Migration Guide addon, written to satisfy FreeCAD's
[`AI_POLICY.md`](https://github.com/FreeCAD/FreeCAD/blob/main/AI_POLICY.md)
(effective June 29, 2026). It is meant to be:

- linked from the addon's `README.md` (already done),
- pasted, adapted, into the description of any PR or Issue this addon's
  maintainer opens against FreeCAD-adjacent repositories, and
- kept accurate — update it if the tooling or process changes.

## Natural-language disclosure (paste into PR/issue descriptions)

> This contribution was drafted with the assistance of an AI coding
> assistant (Claude, by Anthropic). All code, documentation, and copy were
> reviewed, tested, and are fully understood by the named human maintainer
> below, who takes personal responsibility for this contribution and
> personally handles all reviewer communication on it — no AI-generated
> replies are posted under this account. This complies with FreeCAD's
> AI_POLICY.md disclosure requirement.

## Git trailer (append to every prepared commit)

```
Assisted-by: Claude (Anthropic, Sonnet 5)
```

Adjust the model identifier to match whichever Claude model actually
produced the change, per `AI_POLICY.md`'s
`Assisted-by: [Model-Family] ([Version/ID])` format.

## PR-template checkbox

FreeCAD's PR template requires checking:

> "This PR is not unverified AI output, I take responsibility for it, and
> all communication from my side in this PR is done by me personally."

Do not check this box, and do not open the PR, until mathmati
has personally reviewed the diff, tested it against a live FreeCAD install,
and is prepared to answer reviewer questions personally (not by relaying an
AI's answers verbatim).

## What "human-reviewed" meant in practice for this addon

Before this addon was marked release-quality, its maintainer:

- ran a clean-install test (fresh copy into a `Mod/` directory, not a
  symlink to the dev tree) under FreeCAD 1.1.0 and confirmed the workbench,
  both panels, and no console errors, with a screenshot;
- read every string of concept-map/tour copy for technical accuracy against
  a live FreeCAD 1.1.0 install (workbench and command names verified via
  `Gui.listWorkbenches()` / `Gui.listCommands()`, not assumed);
- checked the manifest (`package.xml`) against the FreeCAD Addon-Index
  Qualities checklist field by field;
- decided the scope boundaries (no config wizard, no Sketcher-constraint
  teaching, no vendored addons) and is prepared to defend them in review.

## Status

This addon has **not yet been submitted anywhere**. This disclosure is
prepared in advance so that whenever the maintainer does open the Index
issue, a PR, or a Discord/forum post, the disclosure language is already
reviewed and ready to attach — not written under time pressure at submission
time.
