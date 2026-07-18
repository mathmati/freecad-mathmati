# SPDX-License-Identifier: MIT
"""AIRender workbench package (Modern namespaced layout).

Importing this package has no side effects beyond making the submodules
importable -- workbench/command registration happens in init_gui.py,
auto-discovered by FreeCAD's Modern-layout addon loader from
Mod/<addon>/freecad/AIRenderWB/. Per the Qualities checklist, nothing here
does network access or expensive work at import time -- the "AI Render..."
command only touches the network (ComfyUI/Stability/OpenAI) on explicit
user action (the dialog's Render button).
"""
