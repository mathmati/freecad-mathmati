PREPARED DRAFT — awaiting user review and sign-off before any external submission.

# AI-Assistance Disclosure — FreeCAD Engineering Standards Library addon

This document is the standing AI-assistance disclosure for the FreeCAD
Engineering Standards Library addon, written to satisfy FreeCAD's
[`AI_POLICY.md`](https://github.com/FreeCAD/FreeCAD/blob/main/AI_POLICY.md)
(effective June 29, 2026). It is meant to be:

- linked from the addon's `README.md` (already done),
- pasted, adapted, into the description of any PR or Issue this addon's
  maintainer opens against FreeCAD-adjacent repositories, and
- kept accurate — update it if the tooling or process changes.

## Natural-language disclosure (paste into PR/issue descriptions)

> This contribution was drafted with the assistance of an AI coding
> assistant (Claude, by Anthropic). All code, data, documentation, and
> copy were reviewed and are fully understood by the named human
> maintainer below, who takes personal responsibility for this
> contribution and personally handles all reviewer communication on it —
> no AI-generated replies are posted under this account. This complies
> with FreeCAD's AI_POLICY.md disclosure requirement.

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

Do not check this box, and do not open the PR, until
mathmati has personally reviewed the diff and data
(including resolving the two flagged material-property values — see
`../DATA_PROVENANCE.md` §"Summary of flags requiring human review"),
tested it against a live FreeCAD install, and is prepared to answer
reviewer questions personally (not by relaying an AI's answers verbatim).

## What "human-reviewed" needs to mean in practice for this addon

This session performed (and this disclosure records honestly what was and
was not done):

- **Done, this session:** a clean-install test (fresh copy into an empty
  `Mod/` directory, not a symlink, matching what the Addon Manager does)
  under FreeCAD 1.1.0 under Xvfb, confirming all 21 material cards
  register in the real Material Editor and the real
  `Materials.MaterialManager` API, with zero parse errors, screenshot
  captured. Every mechanical property was cross-checked against ≥2
  independent public sources with a citation table
  (`../DATA_PROVENANCE.md`), plus a second-pass isotropic-consistency
  audit that corrected two values.
- **Also done, 2026-07-10:** an adversarial prior-art pass against
  FreeCAD's live core source and `FreeCAD/Supplemental-Materials`
  (`ops/novelty-standards-library.md`) found 7 of the original 28 cards
  were exact duplicates of already-shipped core cards; they were removed
  before this release (now 21 cards), and the above clean-install +
  headless enumeration checks were re-run against a genuinely clean
  install to confirm 21/21 pass post-removal.
- **NOT yet done — requires the named human maintainer before
  submission:** independently re-verifying the specific numeric values
  (this disclosure does not claim a domain engineer has re-derived every
  figure by hand from a primary standard document — it claims a
  documented, citation-backed cross-check process was followed); making
  the two explicitly flagged values (ASTM A36 Poisson's ratio, Gray Cast
  Iron G3000 yield strength) a deliberate human decision rather than an AI
  default (a third flag, PLA's tensile strength, is moot — the PLA card
  was removed pre-release as an exact duplicate of core); and all the
  human-only steps in `../RELEASE_CHECKLIST.md`.

## AI-assisted second-pass review, disclosed

One material-data accuracy audit (the isotropic-consistency check
recorded in `../DATA_PROVENANCE.md`'s "Fable orchestrator accuracy audit"
section, which corrected two values) was itself performed by a second,
independent AI review pass rather than a human — disclosed here rather
than presented as human-reviewed. The named human maintainer remains
responsible for accepting or revising those corrections before submission.

## Status

This addon has **not yet been submitted anywhere**. This disclosure is
prepared in advance so that whenever the maintainer does open the Index
issue, a PR, or a forum post, the disclosure language is already reviewed
and ready to attach — not written under time pressure at submission time.
