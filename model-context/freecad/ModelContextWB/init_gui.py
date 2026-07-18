# SPDX-License-Identifier: MIT
"""Workbench registration for the Model Context addon. Auto-discovered by
FreeCAD's Modern-layout loader. No network access or expensive work at
import/startup; commands act only on explicit user activation."""
import os

import FreeCADGui as Gui


class ModelContextWorkbench(Gui.Workbench):
    MenuText = "Model Context"
    ToolTip = ("Serialize the document's semantic model (feature tree + sketch "
               "constraints + parameters + materials) as grounding context for AI tools")
    Icon = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
        "Resources", "Icons", "modelcontext.svg")

    def Initialize(self):
        from . import commands
        commands.register()
        tools = ["ModelContext_Export", "ModelContext_CopyMarkdown",
                 "ModelContext_DiffSaved", "ModelContext_DiffFiles"]
        self.appendToolbar("Model Context", tools)
        self.appendMenu("Model Context", tools)

    def Activated(self):
        pass

    def Deactivated(self):
        pass

    def GetClassName(self):
        return "Gui::PythonWorkbench"  # exact string, mandatory, do not change


Gui.addWorkbench(ModelContextWorkbench())
