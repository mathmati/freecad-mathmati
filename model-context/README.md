# FreeCAD Model Context

Serialize a FreeCAD document's **semantic model** — the feature tree, each
feature's parameters (with expressions), the Sketcher geometry **with its
constraint graph**, and assigned materials — into a **canonical, versioned,
tool-agnostic JSON schema**, plus an LLM-legible Markdown rendering.

It is grounding context for LLM / agent / MCP tools: a *published* schema
(see [`SCHEMA.md`](SCHEMA.md)) anyone can adopt, instead of the ad-hoc,
per-tool, undocumented dumps every FreeCAD AI/MCP integration reinvents today.
Screenshots tell an AI what the model *looks like*; this tells it what the
model *is* — the design intent encoded in the constraints and parametric
relationships.

## Why this exists

Across the FreeCAD AI ecosystem, each MCP server / AI workbench independently
reinvents a narrow "describe the document" feature (feedback screenshots,
`get_objects`, `inspect_object`, `get_document_graph`), and **none publishes a
shared, documented schema** — especially not one that serializes *sketch
constraints* as a legible graph. That convergence-without-coordination is the
gap this fills: one small, adoptable format, complementary to (not competing
with) the servers and agents that already exist.

The point-based-geometry + constraint-as-edge model follows the pattern from
*CAD-Assistant* (Mallis et al., ICCV 2025, arXiv:2412.13810); the contribution
here is packaging it as a documented, versioned, standalone library and schema.

## Use it (library)

```python
import FreeCAD as App
from freecad.ModelContextWB import serialize

model = serialize.serialize_document(App.ActiveDocument)   # -> dict (SCHEMA.md)
text  = serialize.to_markdown(model)                        # -> LLM-legible str
```

`model` is plain JSON-serializable data; feed it (or `text`) to any model or
MCP tool as context.

## Use it (GUI)

Activate the **Model Context** workbench:

- **Export Model Context** — writes `<document>.modelcontext.json` and
  `.modelcontext.md` next to the saved document.
- **Copy Model Context (Markdown)** — copies the Markdown to the clipboard,
  ready to paste into an AI chat.
- **Diff Against Saved** / **Diff Two Files…** — show what changed as a
  colored dialog, with **Export HTML Report…** to write a self-contained
  visual report (see below).

## What it captures (example)

```
# Model context: bracket
schema freecad-model-context v1.0

## Body "Body" (tip: Pad)
feature tree: Sketch -> Pad

### Sketch "Sketch"  (on XY_Plane)
geometry: 4 line
constraints:
- Coincident: geometry 0.end , geometry 1.start
- Horizontal: geometry 0
- Vertical: geometry 1
- DistanceX: geometry 0.start , geometry 0.end = 20

### Feature "Pad"  [PartDesign::Pad]
  Length = 15.0 mm  (= Spreadsheet.height)
  Profile -> Sketch
```

Note what survives: the ordered feature tree, the **constraint graph** (with
each constraint's geometry references and named point roles), dimensional
values, the expression driving `Length`, and the link to the profile —
while computed shapes, hidden/internal properties, and values left at their
defaults are omitted so the context stays semantic, not a property dump.

## Diff: what changed between two versions

Because both sides serialize to the same schema, diffing two versions of a
document is plain data comparison. The output reads like a semantic git
diff:

```
Model diff: bracket_v1.FCStd -> bracket_v2.FCStd
~ Pad: Length 15 mm -> 20 mm
+ Pocket (PartDesign::Pocket) added
- Sketch: constraint DistanceX: g0.start, g0.end = 20
~ Body: tip Pad -> Pocket
```

### Text is the default; visuals are there when you want them

The same structured diff renders four ways, so it fits both a terminal and a
review:

- **`text`** (default) — colored, terraform-plan-style terminal output: a
  `+N / ~N / −N` summary then changes grouped per object with aligned
  `old → new` rows. Color respects `NO_COLOR`, only paints real TTYs, and the
  `+ ~ -` glyphs always remain so it degrades losslessly. `MC_DIFF_SUMMARY=1`
  gives just the counts and one head per touched object.
- **`json`** — the canonical machine format (the diff dict itself), for
  scripting and CI.
- **`svg`** — a headless overlay that draws both versions as 2D line-art in
  one image: **added** solid green, **removed** dashed red, **changed** shows
  the old silhouette ghosted grey under the new one in solid blue. Color is
  never the only channel (line style carries the same information), and
  `MC_DIFF_PALETTE=okabe-ito` selects a colorblind-safe palette. Off by
  default but available: `MC_DIFF_CALLOUTS=1` circles and numbers each change
  with a revision cloud (the drafting convention for marking a revised region).
- **`html`** — a single self-contained file (no external assets, no build
  step): a sticky header with count chips, the visual overlay with
  iso/front/top view tabs, and a collapsible `old → new` row per object.
  Honors light/dark via `prefers-color-scheme` with a toggle.

Ways to use it:

- **In the GUI:** **Diff Against Saved** (what changed since the last save)
  and **Diff Two Files…**, each with **Export HTML Report…**.
- **From the command line** (exit code 0 = no changes, 1 = differences,
  2 = error). Options are set with `MC_DIFF_*` env vars, because `freecadcmd`
  owns the real command line:

  ```
  MC_DIFF_OLD=v1.FCStd MC_DIFF_NEW=v2.FCStd freecadcmd tools/modelcontext_diff.py
  MC_DIFF_FORMAT=html MC_DIFF_OUTPUT=diff.html \
      freecadcmd tools/modelcontext_diff.py v1.FCStd v2.FCStd
  MC_DIFF_FORMAT=svg  MC_DIFF_OUTPUT=diff.svg  MC_DIFF_PALETTE=okabe-ito \
      freecadcmd tools/modelcontext_diff.py v1.FCStd v2.FCStd
  ```

- **From git**, so `git diff` shows semantic changes for `.FCStd` files:

  ```
  git config diff.fcstd.command "freecadcmd /path/to/tools/modelcontext_diff.py"
  echo "*.FCStd diff=fcstd" >> .gitattributes
  ```

As a library: `diff.diff_models(old, new)` returns a structured dict (see
the appendix in `SCHEMA.md`); `diff_to_text`/`diff_to_markdown` (in `diff`),
`render.diff_to_terminal`/`diff_to_json`, `svgdiff.build_overlay_svg`, and
`htmlreport.diff_to_html` are the renderers.

Honest limits: sketch geometry is compared by position (GeoId), so
inserting an element mid-list reads as several edited elements, and
constraints that reference shifted geometry indices read as removed plus
added.

## Scope (v1)

- **Read-only context.** Captures enough to *describe and reason about* the
  model, round-tripping losslessly through JSON. Full geometric
  *reconstruction* of a live document from the schema is a deliberate non-goal
  of v1.
- **Covered:** PartDesign/Part feature tree + tip, parametric inputs +
  expressions, Sketcher geometry (line/circle/arc/point/ellipse/…) + the full
  constraint graph, attachments, and non-default materials.
- **Not yet:** assemblies/links across documents, TechDraw/FEM/BIM-specific
  semantics, and a formal JSON-Schema/`$schema` file (the spec is prose in
  `SCHEMA.md` for v1).

## Verification

A headless (`freecadcmd`) regression builds a representative parametric
document (Body → constrained rectangle Sketch → Pad whose `Length` is driven
by a spreadsheet expression), serializes it, and asserts the schema faithfully
captures the feature tree, the sketch constraint graph (constraint types +
geometry references + named point roles), dimensional values, the expression,
the support plane, that datum scaffolding stays minimal, and that the result
round-trips as JSON. A second regression covers the diff: identical models
diff to empty; a Length change (15 to 20 mm), an added feature, a removed
constraint, a renamed label, an expression change, and a dimensional-value
edit are each detected and rendered; the CLI tool is exercised end-to-end on
two saved files with its exit-code contract, and each presentation format is
checked (valid JSON schema, a headless SVG overlay with a legend, a
self-contained HTML report that embeds the overlay and references no external
assets, and the summary verbosity level). A GUI check confirms the workbench
and all four commands auto-register with zero Report-View errors.

## License

Code is MIT (see `LICENSE-Code` and the SPDX headers). The schema in
`SCHEMA.md` is free to implement/adopt.
