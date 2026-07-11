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
round-trips as JSON. A GUI check confirms the workbench and both commands
auto-register with zero Report-View errors.

## License

Code is MIT (see `LICENSE-Code` and the SPDX headers). The schema in
`SCHEMA.md` is free to implement/adopt.
