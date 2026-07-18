# SPDX-License-Identifier: MIT

"""FreeCAD Gui.Command subclasses for the Migration Guide workbench."""
import os

import FreeCADGui as Gui

from . import migration_panel
from . import tour_panel

_ICON_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
    "Resources",
    "Icons",
)
_ICON_PATH = os.path.join(_ICON_DIR, "migration_guide.svg")


class ShowMigrationGuideCommand(object):
    """Opens (or raises) the dockable Migration Guide panel."""

    def GetResources(self):
        return {
            "MenuText": "Migration Guide",
            "ToolTip": "Opens the Fusion 360 / SolidWorks to FreeCAD migration guide",
            "Pixmap": _ICON_PATH,
        }

    def IsActive(self):
        return True

    def Activated(self):
        migration_panel.show_panel()


class StartTourCommand(object):
    """Opens (or raises) the step-driven guided "first real part" tour."""

    def GetResources(self):
        return {
            "MenuText": "Start Guided Tour...",
            "ToolTip": "Starts the step-by-step first-part tour (sketch, pad, pocket, save)",
            "Pixmap": _ICON_PATH,
        }

    def IsActive(self):
        return True

    def Activated(self):
        tour_panel.show_panel()


def register():
    Gui.addCommand("MigrationGuide_ShowPanel", ShowMigrationGuideCommand())
    Gui.addCommand("MigrationGuide_StartTour", StartTourCommand())
