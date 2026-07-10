# SPDX-License-Identifier: MIT

"""Workbench registration for the FreeCAD Migration Guide addon.

Importing this module (from the top-level InitGui.py shim) registers the
workbench with Gui.addWorkbench(...), matching SPEC.md section 4.2.
"""
import os

import FreeCADGui as Gui


class MigrationGuideWorkbench(Gui.Workbench):
    MenuText = "Migration Guide"
    ToolTip = "Fusion 360 / SolidWorks to FreeCAD migration guide and orientation"
    Icon = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
        "Resources",
        "Icons",
        "migration_guide.svg",
    )

    def Initialize(self):
        # Import side effect registers the commands with Gui.addCommand.
        from . import commands

        commands.register()
        self.appendToolbar(
            "Migration Guide", ["MigrationGuide_ShowPanel", "MigrationGuide_StartTour"]
        )
        self.appendMenu(
            "Migration Guide", ["MigrationGuide_ShowPanel", "MigrationGuide_StartTour"]
        )

        # First-run behaviour (SPEC.md 5.2): show the panel automatically the
        # first time any real workbench activates, using this addon's own
        # parameter group (never touching core's Mod/Start first-run flag).
        from . import migration_panel

        migration_panel.install_first_run_hook()

    def Activated(self):
        # Also show/raise the panel whenever a user explicitly switches into
        # this workbench -- it's a reference guide, not a modal step.
        from . import migration_panel

        migration_panel.show_panel()

    def Deactivated(self):
        pass

    def GetClassName(self):
        return "Gui::PythonWorkbench"  # exact string, mandatory, do not change


Gui.addWorkbench(MigrationGuideWorkbench())
