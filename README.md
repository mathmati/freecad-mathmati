# FreeCAD add-ons by mathmati

A small suite of FreeCAD 1.1 add-ons aimed at one goal: **make FreeCAD
approachable** — easier to learn, better equipped, and able to work with the
real world. Each add-on is independent, installable via the FreeCAD Add-on
Manager, and developed here as the shared source of truth.

Built with disclosed AI assistance, human-reviewed and human-accountable, in
line with FreeCAD's `AI_POLICY.md` (each add-on carries an `Assisted-by:`
trailer and a `submission/DISCLOSURE.md`). Every add-on was verified in a real
FreeCAD 1.1 install (headless + GUI screenshots) and prior-art-checked before
release — see each add-on's `submission/` folder and the notes below.

## The add-ons

| Add-on | What it does | Status |
|--------|--------------|--------|
| **[migration-guide](migration-guide/)** | *Learn it.* Two dockable panels for people arriving from Fusion 360 / SolidWorks: a searchable concept-map (Part-container vs PartDesign Body, terminology bridges, an honest toponaming note) and an interactive 7-step guided "first real part" tour that validates against the live document. | v0.x, verified |
| **[standards-library](standards-library/)** | *Equip it.* 21 cross-checked engineering material cards (steels, stainless, aluminium, titanium, copper alloys, cast irons, polymers, magnesium — incl. AZ31B, not otherwise in core or the official supplemental repo). Every property cross-checked against ≥2 public sources with a provenance table. | v0.4.0, verified |
| **[site-context](site-context/)** | *Build in the real world.* A SketchUp-style "Add Location": place-search or coordinates → OpenStreetMap buildings (with courtyards) extruded at real heights on SRTM terrain. The maintained, 1.x-verified evolution of the GeoData→GeoData2 lineage. | v0.2, verified |
| **[push-pull](push-pull/)** | *Model it easily.* SketchUp-style direct modelling: click a face, drag along its normal with a live ghost preview and numeric readout, release to commit a **parametric** PartDesign Pad/Pocket. Type a number for precision. | v0.1.0, verified |

An **AI Render** add-on (viewport → styled image via your own AI provider /
local ComfyUI) is in final verification and will be added when confirmed.

## Honesty notes

- **Not "first/only."** Where prior work exists it is named and credited
  (site-context credits the GeoData lineage; standards-library removed 7 cards
  that duplicated FreeCAD core before release). See each `submission/` folder.
- **Prepared, not yet submitted.** The Add-on Index submissions and any
  community coordination notes in each `submission/` folder are drafts awaiting
  their author's final review.
- **Data licensing:** site-context uses OpenStreetMap data (© OpenStreetMap
  contributors, ODbL) and open elevation data; attribution is embedded in
  generated documents.

## Licence

Code is MIT (see each add-on's `LICENSE`/SPDX headers and the repo `LICENSE`).
Material data in standards-library is CC-BY-4.0.
