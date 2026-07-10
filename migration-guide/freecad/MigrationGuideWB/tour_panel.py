# SPDX-License-Identifier: MIT

"""The guided "first real part" tour: a step-driven dockable panel.

Delivery matches SPEC.md section 4 (step-driven panel, instruction + WHY,
document-state validation, "next" only advances on the expected object
appearing) and section 6.1 (Gui.getMainWindow().addDockWidget). Docked in
the Right Dock Area per section 7's Zones convention (interactive Tasks
panels, <=360px) -- the Migration Guide reference panel owns the Left Dock.

Deliberately no highlight/overlay widget (section 6.3 verdict: v0.1 ships
the lightweight instruction+validation tour only).
"""
import FreeCAD as App
import FreeCADGui as Gui
from PySide import QtCore, QtGui

from . import tour_steps

DOCK_OBJECT_NAME = "MigrationGuideTourDock"

# Module-level cache so re-activating the workbench (or re-running the
# command) doesn't create a second dock widget, mirroring migration_panel.py.
_state = {"dock": None, "panel": None}


class TourPanel(QtGui.QWidget):
    """Renders the current step and drives Next/Back/Check/Skip."""

    def __init__(self, parent=None):
        super(TourPanel, self).__init__(parent)
        self.steps = tour_steps.STEPS
        self.index = 0

        layout = QtGui.QVBoxLayout(self)
        layout.setContentsMargins(6, 6, 6, 6)
        layout.setSpacing(6)

        self.header = QtGui.QLabel()
        self.header.setStyleSheet("font-weight: bold; font-size: 11pt;")
        self.header.setWordWrap(True)
        layout.addWidget(self.header)

        self.body = QtGui.QTextBrowser()
        self.body.setOpenExternalLinks(True)
        layout.addWidget(self.body, 1)

        self.status = QtGui.QLabel()
        self.status.setWordWrap(True)
        layout.addWidget(self.status)

        btn_row = QtGui.QHBoxLayout()
        self.back_btn = QtGui.QPushButton("< Back")
        self.back_btn.clicked.connect(self._on_back)
        self.skip_btn = QtGui.QPushButton("Skip step")
        self.skip_btn.setToolTip(
            "Move on without this step's check passing -- the tour never "
            "traps you."
        )
        self.skip_btn.clicked.connect(self._on_skip)
        self.check_btn = QtGui.QPushButton("Check")
        self.check_btn.clicked.connect(self._on_check)
        self.next_btn = QtGui.QPushButton("Next >")
        self.next_btn.clicked.connect(self._on_next)
        btn_row.addWidget(self.back_btn)
        btn_row.addWidget(self.skip_btn)
        btn_row.addStretch(1)
        btn_row.addWidget(self.check_btn)
        btn_row.addWidget(self.next_btn)
        layout.addLayout(btn_row)

        self.progress = QtGui.QLabel()
        self.progress.setWordWrap(True)
        self.progress.setStyleSheet("color: gray; font-size: 8pt;")
        layout.addWidget(self.progress)

        # Poll the document state periodically so a step can auto-advance
        # when the user completes the action, without needing to press
        # "Check". This is a handful of cheap Python attribute look-ups on
        # the active document -- no I/O, no network -- so it doesn't run
        # afoul of the "avoid expensive work at import/startup" Quality;
        # it only starts once the user has opened the tour panel.
        self._timer = QtCore.QTimer(self)
        self._timer.setInterval(1000)
        self._timer.timeout.connect(lambda: self._poll(auto_advance=True))
        self._timer.start()

        self._render()

    # -- internals --------------------------------------------------------

    def _current(self):
        return self.steps[self.index]

    def _render(self):
        step = self._current()
        n = len(self.steps)
        self.header.setText(
            "Step {0} of {1}: {2}".format(self.index + 1, n, step.title)
        )
        self.body.setHtml(
            "<p>{0}</p><p><b>Why:</b> {1}</p>".format(step.instruction, step.why)
        )
        self.progress.setText(
            "  >  ".join(
                ("[{0}]".format(s.title) if i == self.index else s.title)
                for i, s in enumerate(self.steps)
            )
        )
        self.back_btn.setEnabled(self.index > 0)
        self.next_btn.setEnabled(self.index < n - 1)
        self._poll(auto_advance=False)

    def _poll(self, auto_advance):
        step = self._current()
        try:
            ok = bool(step.check(App.ActiveDocument))
        except Exception as exc:
            # A check function must never crash the tour -- fall back to
            # "not detected yet" and log for diagnosis.
            ok = False
            App.Console.PrintWarning(
                "MigrationGuideWB tour: step '{0}' check raised {1}\n".format(
                    step.key, exc
                )
            )
        if ok:
            self.status.setText(
                "Detected: this step's expected document state is present."
            )
            self.status.setStyleSheet("color: #1a7a1a;")
            if auto_advance and self.index < len(self.steps) - 1:
                self.index += 1
                self._render()
        else:
            self.status.setText(
                "Not detected yet. Do the action above, then press Check "
                "(or keep working -- this auto-advances)."
            )
            self.status.setStyleSheet("color: #a06a00;")
        return ok

    # -- button handlers ----------------------------------------------------

    def _on_check(self):
        self._poll(auto_advance=True)

    def _on_next(self):
        if self.index < len(self.steps) - 1:
            self.index += 1
            self._render()

    def _on_back(self):
        if self.index > 0:
            self.index -= 1
            self._render()

    def _on_skip(self):
        # Every step has an explicit escape hatch so the tour never traps
        # the user (SPEC.md section 4 requirement).
        if self.index < len(self.steps) - 1:
            self.index += 1
        self._render()

    def closeEvent(self, event):
        self._timer.stop()
        super(TourPanel, self).closeEvent(event)


def _build_dock(main_window):
    dock = QtGui.QDockWidget("Guided Tour", main_window)
    dock.setObjectName(DOCK_OBJECT_NAME)
    panel = TourPanel(dock)
    dock.setWidget(panel)
    main_window.addDockWidget(QtCore.Qt.RightDockWidgetArea, dock)
    _state["panel"] = panel
    return dock


def show_panel():
    """Create the tour dock on first use, or raise/reveal it if it exists."""
    main_window = Gui.getMainWindow()
    if main_window is None:
        return None

    dock = _state["dock"]
    if dock is None:
        existing = main_window.findChild(QtGui.QDockWidget, DOCK_OBJECT_NAME)
        dock = existing if existing is not None else _build_dock(main_window)
        _state["dock"] = dock
        if _state["panel"] is None:
            _state["panel"] = dock.widget()

    dock.setVisible(True)
    dock.raise_()
    return dock
