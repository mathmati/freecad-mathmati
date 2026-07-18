# FreeCAD add-ons by mathmati

FreeCAD 1.1 add-ons that make FreeCAD easier to learn, better equipped, and
able to work with the real world. Each one is independent and installable via
the Addon Manager.

## The add-ons

| Add-on | What it does |
|--------|--------------|
| **[migration-guide](migration-guide/)** | A searchable concept map and a guided first-part tour for people coming from Fusion 360 or SolidWorks. |
| **[standards-library](standards-library/)** | 21 engineering material cards (steels, stainless, aluminium, titanium, copper alloys, cast iron, magnesium). Every value cross-checked against at least two public sources. |
| **[site-context](site-context/)** | Pick a place, get a 3D site model: OpenStreetMap buildings on real terrain, georeferenced. Like SketchUp's Add Location, on open data. |
| **[push-pull](push-pull/)** | Click a face and drag to extrude or cut it, SketchUp style. Commits a normal parametric Pad or Pocket. Type a number for an exact distance. |
| **[sketch-layer](sketch-layer/)** | Draw lines and rectangles in the 3D view with SketchUp-style colored snapping cues and type-to-dimension. Closed shapes become faces you can push/pull. |
| **[ai-render](ai-render/)** | Render the 3D view with an AI image model, using your own ComfyUI, Stability AI or OpenAI account. A line-art control image keeps the result true to your geometry. |
| **[model-context](model-context/)** | Exports a document's feature tree, parameters and sketch constraints as JSON or Markdown, so AI tools can read the model instead of guessing from screenshots. |
| **[freecad-diff](freecad-diff/)** | Shows what changed between two versions of a document: which dimension moved, which feature was added, plus a visual overlay of both shapes. Works from the GUI, the command line, and `git diff`. Early, feedback welcome. Also at [mathmati/freecad-diff](https://github.com/mathmati/freecad-diff). |

## Notes

- Prior work is credited, not claimed. Where similar work exists it is named
  in the relevant add-on's README (site-context credits the GeoData lineage;
  standards-library lists which cards are new and which duplicate core).
- site-context uses OpenStreetMap data (© OpenStreetMap contributors, ODbL)
  and open elevation data; attribution is embedded in generated documents.

## Licence

Code is MIT (see each add-on's `LICENSE` and SPDX headers). Material data in
standards-library is CC-BY-4.0.

## Transparency

Built with [Claude Code](https://claude.com/claude-code).
