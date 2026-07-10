PREPARED DRAFT — awaiting user review and sign-off before any external submission.

---

**Where this goes, when approved:** an issue of type "Addon - Addition" at
`https://github.com/FreeCAD/Addons/issues/new/choose` (or the Codeberg
mirror `https://codeberg.org/FreeCAD/Addons`), per the Addon-Academy
publishing guide.

**Before this can actually be filed:** the addon needs its own public repo
(currently it lives inside a private FableMax monorepo — see
`RELEASE_CHECKLIST.md`), a tagged release on a stable `main`/`release`
branch, and every `[PLACEHOLDER]` below filled in.

---

## Issue title

Addon Addition: FreeCAD Migration Guide

## Repository

`https://github.com/mathmati/FreeCAD-Migration-Guide`
(branch: `main`)

## Description

**FreeCAD Migration Guide** is a small workbench that helps people migrating
from Fusion 360 or SolidWorks (or similar parametric CAD tools) get
productive in FreeCAD. It ships two features:

1. A dockable **Migration Guide** panel: a searchable concept map that
   translates Fusion/SolidWorks terminology and mental models into FreeCAD's
   (Timeline → tree, Component/Body → Part container vs. PartDesign Body,
   Joint → Assembly workbench, Extrude → Pad, Collinear → Tangent, etc.),
   plus an honest note on the toponaming problem and workbench-switching
   quick-reference.
2. A dockable **Guided Tour**: a 7-step, hands-on walkthrough of the core
   PartDesign workflow (new document → Body → sketch → pad → sketch-on-face
   → pocket → save), validated against the user's live document rather than
   watching for clicks, with an explicit "Skip step" on every step.

It is explicitly scoped to **not** duplicate FreeCAD 1.1's own "Welcome to
FreeCAD" first-run configuration screen (language/units/theme/navigation
style), and to **not** re-teach Sketcher constraints — that is left to the
FPA-funded interactive Sketcher-tutorial project (Amrita Vishwa Vidyapeetham
team, funding confirmed Dec 2024, USD 6,000 over 9 months; as of 2026-07 no
shipped repository or Addon Index listing was found for it, so this addon's
tour is written to hand off cleanly whenever it ships and degrade gracefully
if it doesn't) so the two projects complement rather than compete. A full
Addon Index and FPA-grant-archive prior-art search was performed before this
issue was drafted (2026-07-10, `ops/novelty-migration-guide.md`) and found no
other shipped addon, core feature, or maintained project combining a
Fusion/SolidWorks concept map with a document-state-validated guided tour;
the closest adjacent project, FreeCAD-Beginner-Assistant, is a retrospective
best-practices critique of work already done, not a migration guide or fixed
tour (see the repository README's "See also, different job" note).

## How this addon meets the Qualities checklist

- **Governance:** named maintainer, `mathmati`
  (`177616452+mathmati@users.noreply.github.com`), actively watching issues/PRs on the
  repository above.
- **Compliance:** makes zero network connections of any kind; stores only
  two small local preference values (welcome-seen flag, current tour step)
  under its own `Mod/MigrationGuideWB` parameter group; never touches
  FreeCAD's own `Mod/Start` first-run parameters.
- **Licensing:** MIT, declared consistently in `package.xml`'s `<license>`
  element and the repository's `LICENSE-Code` file (exact SPDX id `MIT`).
- **Codebase:**
  - Modern namespaced layout (`freecad/MigrationGuideWB/`), no
    `Init.py`/`InitGui.py` legacy shim, no `sys.path` manipulation.
  - Uses FreeCAD's provided Qt wrapper (`from PySide import QtCore, QtGui`)
    exclusively — never imports PySide6 directly.
  - `<classname>MigrationGuideWorkbench</classname>` matches the registered
    `Gui.Workbench` subclass exactly; `GetClassName()` returns the required
    `"Gui::PythonWorkbench"`.
  - Confines all commands/toolbars/menus/panels to its own "Migration Guide"
    workbench menu and its own two dock widgets; does not modify, hide, or
    interfere with core FreeCAD UI or other addons' UI.
  - No expensive work, network access, or other global side effects at
    import/startup time; the one startup affordance (auto-opening the
    Migration Guide panel on first real-workbench activation) is a cheap,
    param-guarded, deferred (`QTimer.singleShot`) check, disclosed here per
    the Qualities note on avoiding startup side effects.
  - Declares `<freecadmin>1.1.0</freecadmin>` (built and clean-install
    verified on FreeCAD 1.1.0); zero required Python dependencies.
  - SVG-only icon (`Resources/Icons/migration_guide.svg`); no compiled Qt
    resources anywhere in the repository.
- **Best practices:** version/date (`0.1.0` / `2026-07-08`) will be bumped on
  every change reaching the release branch; repository will carry the
  `freecad` and `addon` topics.

**Known gap, disclosed up front rather than discovered in review:** UI
strings are not yet translation-wrapped (`FreeCAD.Qt.translate` /
`QT_TRANSLATE_NOOP`) — this is planned before/alongside this submission
lands, not hidden. Happy to hold the submission until that's done if
reviewers prefer.

## AI-assistance disclosure

This addon was drafted with the assistance of an AI coding assistant
(Claude, by Anthropic), reviewed, tested, and taken responsibility for by
the named human maintainer above, per FreeCAD's `AI_POLICY.md`. Full
disclosure text and the `Assisted-by:` trailer convention used on this
project's commits are in the repository's `DISCLOSURE.md` (mirrors
`submission/DISCLOSURE.md` in the build record). All review responses on
this issue and any follow-up PRs will be written personally by the
maintainer, not relayed AI output.

## Beta-testing note

Per the publishing guide's recommendation to beta-test with real users
before requesting indexing: [PLACEHOLDER — describe where this was shared
for real-user feedback, e.g. FreeCAD forum Addons subforum thread URL, or
state that beta-testing is still pending and this issue is filed as a
work-in-progress/PoC per the guide's allowance for clearly-marked WIP
addons].
