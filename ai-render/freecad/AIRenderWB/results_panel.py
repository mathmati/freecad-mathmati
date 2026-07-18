# SPDX-License-Identifier: MIT
"""A simple results panel: shows the returned styled image(s) plus the
provider/model/prompt/control-image audit trail, per this addon's v1
scope item 4 ("show returned image(s) in a simple results panel").
"""
from PySide import QtCore, QtGui, QtWidgets


class ResultsDialog(QtWidgets.QDialog):
    def __init__(self, image_paths, info_text, parent=None):
        super(ResultsDialog, self).__init__(parent)
        self.setWindowTitle("AI Render - Result")
        self.resize(560, 640)

        layout = QtWidgets.QVBoxLayout(self)

        scroll = QtWidgets.QScrollArea()
        scroll.setWidgetResizable(True)
        inner = QtWidgets.QWidget()
        inner_layout = QtWidgets.QVBoxLayout(inner)

        if not image_paths:
            inner_layout.addWidget(QtWidgets.QLabel("No images returned."))
        for path in image_paths:
            label = QtWidgets.QLabel()
            pixmap = QtGui.QPixmap(path)
            if not pixmap.isNull():
                pixmap = pixmap.scaledToWidth(520, QtCore.Qt.SmoothTransformation)
                label.setPixmap(pixmap)
            else:
                label.setText("(could not load {})".format(path))
            label.setAlignment(QtCore.Qt.AlignCenter)
            inner_layout.addWidget(label)
            path_label = QtWidgets.QLabel(path)
            path_label.setWordWrap(True)
            path_label.setStyleSheet("color: palette(mid); font-size: 10px;")
            inner_layout.addWidget(path_label)

        inner_layout.addStretch(1)
        scroll.setWidget(inner)
        layout.addWidget(scroll, 1)

        info = QtWidgets.QPlainTextEdit()
        info.setReadOnly(True)
        info.setPlainText(info_text)
        info.setMaximumHeight(140)
        layout.addWidget(info)

        button_row = QtWidgets.QHBoxLayout()
        button_row.addStretch(1)
        close_button = QtWidgets.QPushButton("Close")
        close_button.clicked.connect(self.accept)
        button_row.addWidget(close_button)
        layout.addLayout(button_row)
