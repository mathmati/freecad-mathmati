# SPDX-License-Identifier: MIT
"""FreeCAD Gui.Command subclasses for the AIRender workbench."""
import os

import FreeCADGui as Gui

_ICON_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
    "Resources",
    "Icons",
)
_ICON_PATH = os.path.join(_ICON_DIR, "airender.svg")


class AIRenderOpenCommand(object):
    """Opens the "AI Render..." dialog: AIRender's single command surface."""

    def GetResources(self):
        return {
            "MenuText": "AI Render…",
            "ToolTip": (
                "Capture the active 3D view (color + line-art control image) "
                "and generate a styled AI render via a BYO-key provider"
            ),
            "Pixmap": _ICON_PATH,
        }

    def IsActive(self):
        import FreeCADGui as Gui

        return Gui.ActiveDocument is not None

    def Activated(self):
        from . import dialog

        dlg = dialog.AIRenderDialog(Gui.getMainWindow())
        dlg.setModal(False)
        dlg.show()
        # Keep a reference on the main window so the (non-modal) dialog
        # isn't garbage-collected once this method returns -- same pattern
        # used by SiteContext's verify drivers, needed here too since the
        # provider call happens on a background thread the dialog owns.
        Gui.getMainWindow()._airender_dialog = dlg


def register():
    Gui.addCommand("AIRender_Open", AIRenderOpenCommand())
