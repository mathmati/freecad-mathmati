# SPDX-License-Identifier: MIT

"""The Migration Guide dockable panel: Qt widgets + first-run wiring.

Delivery matches SPEC.md section 5.1 (getMainWindow().addDockWidget) and 5.2
(the addon's own first-run parameter group, deferred via workbenchActivated +
QTimer.singleShot so it never races GUI start-up).
"""
import FreeCAD as App
import FreeCADGui as Gui
from PySide import QtCore, QtGui

from . import content

PARAM_GROUP_PATH = "User parameter:BaseApp/Preferences/Mod/MigrationGuideWB"
DOCK_OBJECT_NAME = "MigrationGuideDock"

# Module-level cache so re-activating the workbench (or re-running the
# command) doesn't create a second dock widget.
_state = {"dock": None, "hook_connected": False}


def _param_group():
    return App.ParamGet(PARAM_GROUP_PATH)


def has_seen_welcome():
    return _param_group().GetBool("SeenWelcome", False)


def mark_seen_welcome():
    _param_group().SetBool("SeenWelcome", True)


class MigrationGuidePanel(QtGui.QWidget):
    """The panel content: a filterable concept-map browser + tour launcher."""

    def __init__(self, parent=None):
        super(MigrationGuidePanel, self).__init__(parent)
        layout = QtGui.QVBoxLayout(self)
        layout.setContentsMargins(6, 6, 6, 6)
        layout.setSpacing(4)

        search_row = QtGui.QHBoxLayout()
        search_label = QtGui.QLabel("Filter concept map:")
        self.search_box = QtGui.QLineEdit()
        self.search_box.setPlaceholderText("e.g. toponaming, pad, joint, sketch...")
        self.search_box.textChanged.connect(self._on_filter_changed)
        clear_btn = QtGui.QPushButton("Clear")
        clear_btn.setMaximumWidth(60)
        clear_btn.clicked.connect(self._on_clear_filter)
        search_row.addWidget(search_label)
        search_row.addWidget(self.search_box, 1)
        search_row.addWidget(clear_btn)
        layout.addLayout(search_row)

        self.browser = QtGui.QTextBrowser()
        self.browser.setOpenExternalLinks(True)
        self.browser.setOpenLinks(True)
        self.browser.setHtml(content.build_html(""))
        layout.addWidget(self.browser, 1)

        tour_row = QtGui.QHBoxLayout()
        tour_row.addStretch(1)
        self.tour_button = QtGui.QPushButton("Start the guided tour...")
        self.tour_button.setToolTip(
            "Opens the step-by-step first-part tour: sketch, pad, pocket, save"
        )
        self.tour_button.clicked.connect(self._on_start_tour)
        tour_row.addWidget(self.tour_button)
        layout.addLayout(tour_row)

    def _on_filter_changed(self, text):
        # Preserve scroll position of the browser isn't critical here since
        # a filter is a deliberate narrowing action; re-render from top.
        self.browser.setHtml(content.build_html(text))

    def _on_clear_filter(self):
        self.search_box.setText("")

    def _on_start_tour(self):
        # Opens the step-driven guided "first real part" tour panel
        # (SPEC.md section 4): sketch -> pad -> pocket -> save, validated by
        # inspecting the live document rather than watching for clicks.
        from . import tour_panel

        tour_panel.show_panel()


def _build_dock(main_window):
    dock = QtGui.QDockWidget("Migration Guide", main_window)
    dock.setObjectName(DOCK_OBJECT_NAME)
    dock.setWidget(MigrationGuidePanel(dock))
    main_window.addDockWidget(QtCore.Qt.LeftDockWidgetArea, dock)
    return dock


def show_panel():
    """Create the dock on first use, or raise/reveal it if it already exists."""
    main_window = Gui.getMainWindow()
    if main_window is None:
        return None

    dock = _state["dock"]
    if dock is None:
        # The dock may already exist from a previous session's saved layout
        # (Qt state restore uses the objectName), so look before creating.
        existing = main_window.findChild(QtGui.QDockWidget, DOCK_OBJECT_NAME)
        dock = existing if existing is not None else _build_dock(main_window)
        _state["dock"] = dock

    dock.setVisible(True)
    dock.raise_()
    return dock


def _deferred_first_run_check():
    if not has_seen_welcome():
        show_panel()
        mark_seen_welcome()


def install_first_run_hook():
    """Show the panel automatically the first time a real workbench activates.

    init_gui.py module code runs before the GUI is fully up, and Init.py runs
    with no GUI at all, so we can't just pop the panel open immediately. We
    connect to workbenchActivated, skip the transient "NoneWorkbench" that
    fires during start-up, disconnect after the first real activation, and
    defer the actual UI work via QTimer.singleShot so the main window has
    finished settling. Matches SPEC.md section 5.2.
    """
    if _state["hook_connected"]:
        return
    main_window = Gui.getMainWindow()
    if main_window is None:
        return

    def _on_workbench_activated(name):
        if name == "NoneWorkbench":
            return
        try:
            main_window.workbenchActivated.disconnect(_on_workbench_activated)
        except (RuntimeError, TypeError):
            pass
        _state["hook_connected"] = False
        QtCore.QTimer.singleShot(0, _deferred_first_run_check)

    main_window.workbenchActivated.connect(_on_workbench_activated)
    _state["hook_connected"] = True
