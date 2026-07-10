PREPARED DRAFT — awaiting user review and sign-off before any external submission.

---

**Where this goes, when approved:** an issue of type "Addon - Addition" at
`https://github.com/FreeCAD/Addons/issues/new/choose` (or the Codeberg
mirror `https://codeberg.org/FreeCAD/Addons`), per the Addon-Academy
publishing guide.

**Before this can actually be filed:** the addon needs its own public
repo (currently it lives inside a private FableMax monorepo — see
`RELEASE_CHECKLIST.md`), a tagged release on a stable `main`/`release`
branch, every `[PLACEHOLDER]` below filled in, and the two flagged
material-property values (§below) resolved by a human.

**Prior-art search performed:** a dedicated adversarial prior-art check
was run against FreeCAD's live core source tree and the official
`FreeCAD/Supplemental-Materials` addon before this issue was drafted
(`ops/novelty-standards-library.md`, 2026-07-10). It found 7 of this
addon's original 28 cards were exact duplicates of core cards; those 7
were removed pre-release (see below) rather than shipped as padding.

---

## Issue title

Addon Addition: FreeCAD Engineering Standards Library

## Repository

`https://github.com/mathmati/FreeCAD-Standards-Library`
(branch: `main`)

## Description

**FreeCAD Engineering Standards Library** adds 21 curated, cross-checked
material cards to FreeCAD's own Material system, honestly split into
three tiers (full detail and reasoning in the repo README):

- **15 net-new** (no equivalent anywhere in FreeCAD core or
  `FreeCAD/Supplemental-Materials`): the ASTM/AISI-designated steels
  (A36, A572 Gr50, A992, 1018 CD, 4140 Annealed), stainless 410 and
  17-4PH (H900), Gray Cast Iron G3000 and Ductile Iron 65-45-12, aluminum
  2024-T3/5052-H32/6063-T5, CP-Ti Grade 2, C36000 brass, and — the
  headline item — **AZ31B magnesium, the first magnesium alloy anywhere
  in FreeCAD core or Supplemental-Materials.**
- **6 equivalent/corrected** (same grade family already in core under a
  different designation, or a corrected value; kept for their searchable
  standard name): S355JR (≈core `Steel-S355J2G3`), 6082-T6 (≈core
  `AlMgSi1F31`), 304/1.4301 (core grade, but with a shear-modulus/density
  correction from this project's own isotropic-consistency audit), 316L
  (core only has 316/1.4401, not the low-carbon "L"/1.4404 designation),
  C11000 copper (core's closest match is a different temper/spec), and
  Nylon 6/6 (core only has PA6, not PA66).
- **7 removed pre-release**: a prior-art pass against FreeCAD's live core
  source (`ops/novelty-standards-library.md`, 2026-07-10) found S235JR,
  S275JR, 6061-T6, 7075-T6, Ti-6Al-4V Grade 5, ABS, and PLA were
  byte-for-byte duplicates of already-shipped core cards. These were part
  of this project's own cross-check methodology, not intended as
  contributions, and were deleted before this release rather than shipped
  as padding.

Every card follows FreeCAD's own `.FCMat` schema exactly (same
`LinearElastic` + `MaterialStandard` models FreeCAD's own shipped cards
use) and installs into the same writable "User" material library FreeCAD
itself defines — no new file format, no new UI, no core changes.

It fills a specific, previously-identified gap: FreeCAD 1.0's Materials
rework (new `.FCMat` schema, Material Editor, the `Materials` Python API)
is solid plumbing, but the *pre-populated data set*, while larger than
this project first assumed (core's `Metal/Steel/` alone ships roughly 90
files), has real, verified gaps in ASTM/AISI-designated grades and zero
magnesium anywhere (see FreeCAD/FreeCAD#16801 for the related
CAM-machinability-data gap, a different problem). This addon does not
touch the plumbing at all — it only adds sourced, cited data through the
exact same mechanism FreeCAD's own cards use.

## Also pursuing: direct upstream contribution to Supplemental-Materials

`FreeCAD/Supplemental-Materials` is the official maintainer-run repo for
this exact purpose, already in the live Addon Manager index, with a
documented contribution process (`Documentation/AddingMaterials.md`). The
strongest net-new cards here — especially AZ31B and the five ASTM/AISI
steels — are also being prepared as PRs to that repo as the preferred,
durable upstream route. This addon remains the convenient-install
companion path and is not contingent on those PRs landing; both paths are
offered so reviewers/maintainers can choose whichever they'd rather see
the data through.

## How this addon meets the Qualities checklist

- **Governance:** named maintainer, `mathmati`
  (`177616452+mathmati@users.noreply.github.com`), actively watching issues/PRs on the
  repository above.
- **Compliance:** makes zero network connections of any kind; stores
  nothing except copying its own bundled `.FCMat` files into FreeCAD's own
  writable User material library directory (and an empty, unused BIM
  profiles-CSV managed block reserved for a future release — see Scope
  below); never touches any FreeCAD core preference outside that.
- **Licensing:** code MIT (`package.xml` `<license>` + `LICENSE-Code`,
  exact SPDX id `MIT`); data CC-BY-4.0, declared both in each card's own
  `General.License` field and a matching `# SPDX-License-Identifier:`
  header comment on every `.FCMat` file — declared consistently
  everywhere per the checklist's licensing item.
- **Codebase:**
  - Modern namespaced layout (`freecad/StandardsLibraryWB/`), no
    `InitGui.py` legacy shim, no `sys.path` manipulation anywhere
    (verified by grep this session).
  - Uses FreeCAD's provided Qt wrapper (`from PySide import ...`)
    exclusively.
  - `<classname>StandardsLibraryWorkbench</classname>` matches the
    registered `Gui.Workbench` subclass exactly; `GetClassName()` returns
    the required `"Gui::PythonWorkbench"`.
  - Confines its one toolbar/menu command ("Re-sync standards data") to
    its own workbench; does not modify, hide, or interfere with core
    FreeCAD UI or other addons' UI.
  - The one startup side effect (copying bundled `.FCMat` files into the
    User library) is a fast local file-copy, not network access or
    expensive computation — disclosed here per the Qualities note on
    avoiding startup side effects, and it is idempotent (safe to run every
    launch).
  - Declares `<freecadmin>1.1.0</freecadmin>` (clean-install verified this
    session on FreeCAD 1.1.0 specifically); zero required Python
    dependencies (confirmed: `pyproject.toml` declares none).
  - SVG-only icon (`Resources/Icons/standards_library.svg`); no compiled
    Qt resources anywhere in the repository.
- **Best practices:** version/date bumped
  (`0.4.0`, 2026-07-10 / see `package.xml`) for this prior-art/honesty
  correction release; repository will carry the `freecad` and `addon`
  topics once created.

**Verification performed this session (not just claimed):** a genuinely
clean-install test — fresh copy (no symlink) into an empty `Mod/`
directory, FreeCAD 1.1.0 launched under Xvfb from a state with no
pre-existing synced data — confirmed all 21 cards auto-register (21/21,
counted programmatically from the Material Editor's own tree widget, not
eyeballed) with zero parse errors in the Report View, and a headless
`Materials.MaterialManager` enumeration confirmed every card resolves by
UUID and exposes sane `LinearElastic`/`MaterialStandard` values. Both
checks were re-run after the 7-card prior-art removal, against a
genuinely clean (re-wiped) install, not just the original 28-card run.

**Known gap, disclosed up front rather than discovered in review:** this
release ships **materials only**. The BIM/Arch structural-profile sync
mechanism was proven end-to-end at the mechanism level in an earlier
milestone but ships with an empty data file this release — no profile
rows are added to any user's BIM `profiles.csv` today. Thread/fastener
data and CAM machinability data are future work, not silently dropped
scope.

## Data provenance

Every mechanical property was cross-checked against ≥2 independent public
sources before being added; full citation table in
`DATA_PROVENANCE.md` (mirrors `../DATA_PROVENANCE.md` in the build
record). Two values are explicitly flagged for human review rather than
silently resolved (ASTM A36 Poisson's ratio, Gray Cast Iron G3000 yield
strength) — see that document's summary section. (A third flag, PLA's
ultimate tensile strength, is now moot: the PLA card was removed
pre-release as an exact duplicate of FreeCAD's own core card — see the
description above.) [PLACEHOLDER — confirm here whether these two have
been resolved by the maintainer before filing this issue, or note they
remain open and are disclosed as such.]

## AI-assistance disclosure

This addon was drafted with the assistance of an AI coding assistant
(Claude, by Anthropic), reviewed and taken responsibility for by the
named human maintainer above, per FreeCAD's `AI_POLICY.md`. Full
disclosure text and the `Assisted-by:` trailer convention used on this
project's commits are in the repository's `DISCLOSURE.md` (mirrors
`submission/DISCLOSURE.md` in the build record), including an honest note
that one data-accuracy audit pass was itself performed by a second AI
review, not a human. All review responses on this issue and any
follow-up PRs will be written personally by the maintainer, not relayed
AI output.

## Beta-testing note

Per the publishing guide's recommendation to beta-test with real users
before requesting indexing: [PLACEHOLDER — describe where this was shared
for real-user feedback, e.g. a FreeCAD forum Materials/CAM subforum
thread URL, or state that beta-testing is still pending and this issue is
filed as a work-in-progress/PoC per the guide's allowance for clearly
marked WIP addons].
