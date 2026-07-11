# SPDX-License-Identifier: MIT
"""GUI commands: export the active document's model context to JSON +
Markdown, and copy the Markdown to the clipboard. Thin wrappers over the
headless ``serialize`` core -- all the real work is testable without a GUI.
"""
import json
import os

import FreeCAD as App
import FreeCADGui as Gui
from PySide import QtGui, QtWidgets

from . import serialize as S

_ICON_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
    "Resources", "Icons")


def _icon():
    return os.path.join(_ICON_DIR, "modelcontext.svg")


def _status(msg):
    try:
        Gui.getMainWindow().statusBar().showMessage(msg, 6000)
    except Exception:
        pass


def _output_base(doc):
    """Where to write the export: next to the saved .FCStd, else the user's
    home dir (surfaced in the status message, never silent)."""
    if doc.FileName:
        return os.path.splitext(doc.FileName)[0]
    return os.path.join(os.path.expanduser("~"), doc.Name)


class _ExportCommand(object):
    def GetResources(self):
        return {"MenuText": "Export Model Context",
                "ToolTip": ("Serialize the active document's semantic model "
                            "(feature tree + sketch constraints + parameters + "
                            "materials) to JSON + Markdown next to the document."),
                "Pixmap": _icon()}

    def IsActive(self):
        return App.ActiveDocument is not None

    def Activated(self):
        doc = App.ActiveDocument
        if doc is None:
            return
        model = S.serialize_document(doc)
        base = _output_base(doc)
        try:
            with open(base + ".modelcontext.json", "w") as f:
                json.dump(model, f, indent=2)
            with open(base + ".modelcontext.md", "w") as f:
                f.write(S.to_markdown(model))
        except Exception as exc:  # noqa: BLE001
            _status("Model Context: export failed (%s)" % exc)
            return
        _status("Model Context written to %s.modelcontext.json / .md" % base)


class _CopyMarkdownCommand(object):
    def GetResources(self):
        return {"MenuText": "Copy Model Context (Markdown)",
                "ToolTip": ("Copy the active document's model context as "
                            "Markdown to the clipboard, ready to paste into an "
                            "AI chat as grounding context."),
                "Pixmap": _icon()}

    def IsActive(self):
        return App.ActiveDocument is not None

    def Activated(self):
        doc = App.ActiveDocument
        if doc is None:
            return
        md = S.to_markdown(S.serialize_document(doc))
        try:
            QtWidgets.QApplication.clipboard().setText(md)
            _status("Model Context (Markdown) copied to clipboard.")
        except Exception as exc:  # noqa: BLE001
            _status("Model Context: copy failed (%s)" % exc)


def register():
    Gui.addCommand("ModelContext_Export", _ExportCommand())
    Gui.addCommand("ModelContext_CopyMarkdown", _CopyMarkdownCommand())
