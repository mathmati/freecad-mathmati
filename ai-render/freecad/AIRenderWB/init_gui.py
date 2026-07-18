# SPDX-License-Identifier: MIT
"""Workbench registration for the AIRender addon.

Importing this module (auto-discovered by FreeCAD's Modern-layout addon
loader) registers the workbench with Gui.addWorkbench(...). Per the
Qualities checklist this does no network access or other expensive work
at import/startup time -- the "AI Render..." command only touches the
network on explicit user action (the dialog's Capture/Render buttons).
"""
import os

import FreeCADGui as Gui


class AIRenderWorkbench(Gui.Workbench):
    MenuText = "AI Render"
    ToolTip = "Capture the 3D view and generate a styled AI render (BYO provider)"
    Icon = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
        "Resources",
        "Icons",
        "airender.svg",
    )

    def Initialize(self):
        # Import side effect registers the command with Gui.addCommand.
        from . import commands

        commands.register()
        self.appendToolbar("AI Render", ["AIRender_Open"])
        self.appendMenu("AI Render", ["AIRender_Open"])

    def Activated(self):
        pass

    def Deactivated(self):
        pass

    def GetClassName(self):
        return "Gui::PythonWorkbench"  # exact string, mandatory, do not change


Gui.addWorkbench(AIRenderWorkbench())
