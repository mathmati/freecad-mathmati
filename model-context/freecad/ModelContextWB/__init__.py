# SPDX-License-Identifier: MIT
"""FreeCAD Model Context -- a canonical, versioned, tool-agnostic
serialization of a FreeCAD document's semantic model (feature tree + sketch
geometry WITH constraints + parameters + expressions + materials), as
grounding context for LLM / agent / MCP tools.

The importable core is ``serialize`` (pure, headless):

    from freecad.ModelContextWB import serialize
    model = serialize.serialize_document(App.ActiveDocument)   # -> dict
    text  = serialize.to_markdown(model)                       # -> str

See SCHEMA.md for the published schema. A GUI "Export Model Context" command
(see commands.py) writes the JSON + Markdown for the active document.
"""
