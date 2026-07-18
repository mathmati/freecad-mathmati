# FreeCAD add-ons by mathmati

A small suite of FreeCAD 1.1 add-ons with one goal: **make FreeCAD more
approachable** : easier to learn, friendlier when you open it, better equipped, and able to work with the
real world. Each add-on is independent and installable via the FreeCAD Add-on
Manager.

## The add-ons

| Add-on | What it does |
|--------|--------------|
| **[migration-guide](migration-guide/)** | A searchable concept map and a guided first-part tour for people coming from Fusion 360 or SolidWorks. [in uppercut, available as standalone on request] |
| **[standards-library](standards-library/)** | 21 engineering material cards (steels, stainless, aluminium, titanium, copper alloys, cast iron, magnesium). Every value cross-checked against at least two public sources. [draft not circulated] |
| **[site-context](site-context/)** | Pick a place, get a 3D site model: OpenStreetMap buildings on real terrain, georeferenced. Like SketchUp's Add Location, on open data. [in uppercut, available as standalone on request] |
| **[push-pull](push-pull/)** | Click a face and drag to extrude or cut it, SketchUp style. Commits a normal parametric Pad or Pocket. Type a number for an exact distance. [in uppercut, available as standalone on request] |
| **[sketch-layer](sketch-layer/)** | Draw lines and rectangles in the 3D view with SketchUp-style colored snapping cues and type-to-dimension. Closed shapes become faces you can push/pull. [in uppercut, available as standalone on request] |
| **[offset](https://github.com/mathmati/FreeCAD-Offset)** | Click a planar face and drag (or type a distance) to offset its boundary in its own plane, SketchUp style. Produces the inner face and ring, ready for Push/Pull. [in uppercut, available as standalone on request] |
| **[follow-me](https://github.com/mathmati/FreeCAD-FollowMe)** | Sweep a profile face along an edge or chain of edges, like SketchUp's Follow Me: click the face, click the path, press Enter. [in uppercut, available as standalone on request] |
| **[ai-render](ai-render/)** | Render the 3D view with an AI image model, using your own ComfyUI, Stability AI or OpenAI account. A line-art control image keeps the result true to your geometry. [draft not circulated] |
| **[model-context](model-context/)** | Exports a document's feature tree, parameters and sketch constraints as JSON or Markdown, so AI tools can read the model instead of guessing from screenshots. [draft not circulated] |
| **[freecad-diff](freecad-diff/)** | Shows what changed between two versions of a document: which dimension moved, which feature was added, plus a visual overlay of both shapes. Works from the GUI, the command line, and `git diff`. Early, feedback welcome. See: [mathmati/freecad-diff](https://github.com/mathmati/freecad-diff). [**beta - live for initial discussion and feedback**] |
| **[uppercut](https://github.com/mathmati/uppercut)** | A SketchUp-style interface for FreeCAD: one toolbar with Select, draw tools, Push/Pull, Eraser, Tape Measure and Paint Bucket, assembled from the companion add-ons above plus its own glue tools. SketchUp navigation and single-letter shortcuts, scoped to the workbench. [**beta - live for initial discussion and feedback**] |
| **[command-palette](https://github.com/mathmati/FreeCAD-CommandPalette)** | A searchable launcher for every FreeCAD command: one shortcut, type a few letters, Enter runs it. [**beta - live for initial discussion and feedback**] |
| **[origin-shift](https://github.com/mathmati/FreeCAD-OriginShift)** | Move a document's origin without breaking the model, for working far from 0,0,0 (georeferenced sites, large assemblies). [**beta - live for initial discussion and feedback**] |
| **[visibility-sets](https://github.com/mathmati/FreeCAD-VisibilitySets)** | Save named visibility states and switch between them, like layer states or SketchUp scenes for what is shown. [**beta - live for initial discussion and feedback**] |
| **[rib-tool](https://github.com/mathmati/FreeCAD-RibTool)** | Add stiffening ribs to a part from a sketch line, with thickness and draft. [**beta - live for initial discussion and feedback**] |

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
