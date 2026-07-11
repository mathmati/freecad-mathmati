# FreeCAD add-ons by mathmati

A small suite of FreeCAD 1.1 add-ons with one goal: **make FreeCAD more
approachable** — easier to learn, better equipped, and able to work with the
real world. Each add-on is independent and installable via the FreeCAD Add-on
Manager.

## The add-ons

| Add-on | What it does |
|--------|--------------|
| **[migration-guide](migration-guide/)** | *Learn it.* Two dockable panels for people arriving from Fusion 360 / SolidWorks: a searchable concept-map (Part-container vs PartDesign Body, terminology bridges, an honest toponaming note) and an interactive 7-step guided "first real part" tour that validates against the live document. |
| **[standards-library](standards-library/)** | *Equip it.* 21 cross-checked engineering material cards (steels, stainless, aluminium, titanium, copper alloys, cast irons, polymers, magnesium — including AZ31B, not otherwise present in core or the official supplemental materials). Every property is cross-checked against at least two public sources. |
| **[site-context](site-context/)** | *Build in the real world.* A SketchUp-style "Add Location": place-search or coordinates → OpenStreetMap buildings (with courtyards) extruded at real heights on SRTM terrain. An actively-maintained, FreeCAD-1.x-verified evolution of the earlier GeoData / GeoData2 add-ons, which it credits. |
| **[push-pull](push-pull/)** | *Model it easily.* SketchUp-style direct modelling: click a face, drag along its normal with a live ghost preview and numeric readout, release to commit a **parametric** PartDesign Pad/Pocket — or extrude a standalone drawn face into a solid. Type a number for precision. |
| **[sketch-layer](sketch-layer/)** | *Draw it easily.* SketchUp-style inline drawing: line/rectangle in the 3D view with **colored inference cues** (on-axis, parallel, perpendicular, endpoint) and inline type-to-dimension. Closing a loop makes a face — ready to push/pull. Adds the colored-inference layer on top of FreeCAD's own Draft snapping. |
| **[ai-render](ai-render/)** | *Show it off.* Stylized AI rendering of the active 3D view: captures a color image plus a geometry-faithful line-art control image and sends both to a bring-your-own provider (local ComfyUI by default — free, keyless — or Stability AI / OpenAI with your own key). Complements the physically-accurate (and unmaintained) Render workbench with a fast, stylized alternative. |
| **[model-context](model-context/)** | *Bring your own AI.* Serializes a document's semantic model — feature tree, parameters (with expressions), and Sketcher geometry **with its constraint graph** — into a canonical, versioned, tool-agnostic JSON schema plus LLM-legible Markdown. Grounding context any LLM / agent / MCP tool can consume, published as a schema anyone can adopt rather than an ad-hoc per-tool dump. |

## Notes

- **Prior work is credited, not claimed.** Where similar work exists it is named
  in the relevant add-on's README (site-context credits the GeoData lineage;
  standards-library removed material cards that duplicated FreeCAD core before
  release, and lists which cards are genuinely new vs. equivalents).
- **Data licensing:** site-context uses OpenStreetMap data (© OpenStreetMap
  contributors, ODbL) and open elevation data; attribution is embedded in
  generated documents. standards-library material data is CC-BY-4.0.

## Licence

Code is MIT (see each add-on's `LICENSE` and SPDX headers). Material data in
standards-library is CC-BY-4.0.
