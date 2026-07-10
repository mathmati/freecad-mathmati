# SPDX-License-Identifier: MIT

"""GUI commands for the Standards Library workbench."""

import FreeCAD
import FreeCADGui as Gui

from . import sync

_TRANSLATE = FreeCAD.Qt.translate
_NOOP = FreeCAD.Qt.QT_TRANSLATE_NOOP


class StandardsLibraryResyncCommand:
    """Manually re-run the material/profile sync (useful after updating
    the addon's bundled data pack, without restarting FreeCAD)."""

    def GetResources(self):
        return {
            "MenuText": _NOOP("StandardsLibrary_Resync", "Re-sync standards data"),
            "ToolTip": _NOOP(
                "StandardsLibrary_Resync",
                "Re-copy this addon's material cards and structural profiles "
                "into FreeCAD's Material and BIM profile libraries",
            ),
        }

    def IsActive(self):
        return True

    def Activated(self):
        summary = sync.run_sync()
        if Gui and hasattr(Gui, "getMainWindow"):
            from PySide import QtWidgets

            QtWidgets.QMessageBox.information(
                Gui.getMainWindow(),
                _TRANSLATE("StandardsLibrary", "Standards Library re-sync"),
                _TRANSLATE(
                    "StandardsLibrary",
                    "Materials installed: {materials}\n"
                    "Profile rows installed: {rows}\n"
                    "Errors: {errors}",
                ).format(
                    materials=summary["materials_installed"],
                    rows=summary["profile_rows_installed"],
                    errors=len(summary["errors"]) or "none",
                ),
            )


def register():
    Gui.addCommand("StandardsLibrary_Resync", StandardsLibraryResyncCommand())
