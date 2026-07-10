# SPDX-License-Identifier: MIT

"""Gui-level entry point for the Standards Library addon.

Confirmed empirically (see ../../../FORMAT.md section 4): importing this
module is exactly what FreeCAD's Gui does, once, automatically, for every
installed addon at startup -- proven by building a throwaway probe addon
with this same layout, copying it into FreeCAD's real Mod/ directory, and
observing ``FreeCADGui.listWorkbenches()`` already contained it right
after launch, with no manual workbench activation. That is why the data
sync below is a plain module-level call (not tucked inside
``Workbench.Initialize()``, which only runs when/if the user actually
switches to this workbench) -- this is the one place proven to run
automatically on every FreeCAD start, matching the mission's ask that the
addon "registers it so FreeCAD discovers it".
"""

import os

import FreeCAD
import FreeCADGui as Gui

from . import sync

_sync_summary = sync.run_sync()
FreeCAD.Console.PrintLog(
    "StandardsLibraryWB: startup sync -- materials={materials} profile_rows={rows} errors={errors}\n".format(
        materials=_sync_summary["materials_installed"],
        rows=_sync_summary["profile_rows_installed"],
        errors=_sync_summary["errors"],
    )
)


class StandardsLibraryWorkbench(Gui.Workbench):
    MenuText = "Standards Library"
    ToolTip = "Engineering standards & materials data library (materials + structural profiles)"
    Icon = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
        "Resources",
        "Icons",
        "standards_library.svg",
    )

    def Initialize(self):
        # Import side effect registers the command with Gui.addCommand.
        from . import commands

        commands.register()
        self.appendToolbar("Standards Library", ["StandardsLibrary_Resync"])
        self.appendMenu("Standards Library", ["StandardsLibrary_Resync"])

    def Activated(self):
        pass

    def Deactivated(self):
        pass

    def GetClassName(self):
        return "Gui::PythonWorkbench"  # exact string, mandatory, do not change


Gui.addWorkbench(StandardsLibraryWorkbench())
