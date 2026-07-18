# SPDX-License-Identifier: MIT
"""The "AI Render..." dialog: AIRender's primary (only) command surface.

Capture (color + line-art control image) always runs synchronously on the
main/GUI thread, because it touches FreeCAD's document/view API (not
thread-safe -- same constraint SiteContext's add_location_dialog.py
documents for its own geometry-build half). The provider network call
runs on a background QThread (RenderWorker below) so the UI stays
responsive during a potentially slow img2img request.

Uses FreeCAD's own Qt wrapper (`from PySide import ...`), never PySide6
directly, per the Addon-Academy Qualities checklist.
"""
import datetime
import json
import os
import traceback

import FreeCAD as App
import FreeCADGui as Gui
from PySide import QtCore, QtWidgets

from . import capture, presets, settings, keystore
from .providers import PROVIDER_CLASSES, PROVIDER_BY_NAME, RenderRequest, ProviderError
from .providers.comfyui import ComfyUIProvider
from .providers.stability import StabilityProvider
from .providers.openai_provider import OpenAIProvider
from .results_panel import ResultsDialog


class RenderWorker(QtCore.QThread):
    """Runs provider.render(request) -- network I/O only, no FreeCAD-API
    calls -- off the GUI thread."""

    finished_ok = QtCore.Signal(object)  # RenderResult
    failed = QtCore.Signal(str)

    def __init__(self, provider, request, parent=None):
        super(RenderWorker, self).__init__(parent)
        self.provider = provider
        self.request = request

    def run(self):
        try:
            result = self.provider.render(self.request)
            self.finished_ok.emit(result)
        except ProviderError as exc:
            self.failed.emit(str(exc))
        except Exception as exc:  # noqa: BLE001
            self.failed.emit("{}\n{}".format(exc, traceback.format_exc()))


class AIRenderDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(AIRenderDialog, self).__init__(parent)
        self.setWindowTitle("AI Render...")
        self.resize(560, 700)

        self._worker = None
        self._last_color_path = None
        self._last_control_path = None
        self._last_channel_used = None
        self.last_result_paths = []  # populated after a successful render,
        # read by verify drivers/tests.

        self._build_ui()
        self._load_settings()

    # ------------------------------------------------------------------ UI
    def _build_ui(self):
        layout = QtWidgets.QVBoxLayout(self)

        intro = QtWidgets.QLabel(
            "Capture the active 3D view and generate a styled AI render. "
            "Bring your own provider -- a local ComfyUI endpoint (no key "
            "needed) by default, or Stability AI / OpenAI with your own key."
        )
        intro.setWordWrap(True)
        layout.addWidget(intro)

        # --- style / prompt ---
        preset_row = QtWidgets.QHBoxLayout()
        preset_row.addWidget(QtWidgets.QLabel("Style preset:"))
        self.preset_combo = QtWidgets.QComboBox()
        for p in presets.STYLE_PRESETS:
            self.preset_combo.addItem(p["label"])
        self.preset_combo.currentIndexChanged.connect(self._on_preset_changed)
        preset_row.addWidget(self.preset_combo, 1)
        layout.addLayout(preset_row)

        layout.addWidget(QtWidgets.QLabel("Prompt:"))
        self.prompt_edit = QtWidgets.QPlainTextEdit()
        self.prompt_edit.setFixedHeight(70)
        layout.addWidget(self.prompt_edit)

        # --- provider ---
        provider_row = QtWidgets.QHBoxLayout()
        provider_row.addWidget(QtWidgets.QLabel("Provider:"))
        self.provider_combo = QtWidgets.QComboBox()
        for cls in PROVIDER_CLASSES:
            self.provider_combo.addItem(cls.display_name, cls.name)
        self.provider_combo.currentIndexChanged.connect(self._on_provider_changed)
        provider_row.addWidget(self.provider_combo, 1)
        layout.addLayout(provider_row)

        self.provider_stack = QtWidgets.QStackedWidget()
        self.provider_stack.addWidget(self._build_comfyui_settings())
        self.provider_stack.addWidget(self._build_stability_settings())
        self.provider_stack.addWidget(self._build_openai_settings())
        layout.addWidget(self.provider_stack)

        # --- strength / resolution / line-art channel ---
        row2 = QtWidgets.QHBoxLayout()
        row2.addWidget(QtWidgets.QLabel("Strength:"))
        self.strength_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.strength_slider.setRange(0, 100)
        self.strength_slider.valueChanged.connect(self._on_strength_changed)
        row2.addWidget(self.strength_slider, 1)
        self.strength_label = QtWidgets.QLabel("0.65")
        self.strength_label.setFixedWidth(36)
        row2.addWidget(self.strength_label)
        layout.addLayout(row2)

        row3 = QtWidgets.QHBoxLayout()
        row3.addWidget(QtWidgets.QLabel("Resolution:"))
        self.width_spin = QtWidgets.QSpinBox()
        self.width_spin.setRange(64, 4096)
        self.width_spin.setSingleStep(64)
        row3.addWidget(self.width_spin)
        row3.addWidget(QtWidgets.QLabel("x"))
        self.height_spin = QtWidgets.QSpinBox()
        self.height_spin.setRange(64, 4096)
        self.height_spin.setSingleStep(64)
        row3.addWidget(self.height_spin)
        row3.addStretch(1)
        row3.addWidget(QtWidgets.QLabel("Line-art channel:"))
        self.channel_combo = QtWidgets.QComboBox()
        self.channel_combo.addItem("GUI draw-style (Wireframe, camera-matched, default)", "drawstyle")
        self.channel_combo.addItem("Vector (TechDraw projectToSVG, headless-safe)", "vector")
        row3.addWidget(self.channel_combo)
        layout.addLayout(row3)

        # --- output folder ---
        out_row = QtWidgets.QHBoxLayout()
        out_row.addWidget(QtWidgets.QLabel("Output folder:"))
        self.output_edit = QtWidgets.QLineEdit()
        self.output_edit.setPlaceholderText("(default: <document folder>/airender/)")
        out_row.addWidget(self.output_edit, 1)
        browse_button = QtWidgets.QPushButton("Browse...")
        browse_button.clicked.connect(self._on_browse_output)
        out_row.addWidget(browse_button)
        layout.addLayout(out_row)

        # --- action buttons ---
        button_row = QtWidgets.QHBoxLayout()
        self.capture_button = QtWidgets.QPushButton("Capture only")
        self.capture_button.setToolTip(
            "Run just the capture pipeline (color + line-art) without calling any provider -- "
            "useful to preview/verify the control images."
        )
        self.capture_button.clicked.connect(self._on_capture_only)
        button_row.addWidget(self.capture_button)

        self.render_button = QtWidgets.QPushButton("Render")
        self.render_button.clicked.connect(self._on_render)
        button_row.addWidget(self.render_button)
        layout.addLayout(button_row)

        # --- previews ---
        preview_row = QtWidgets.QHBoxLayout()
        self.color_preview = QtWidgets.QLabel("(color capture)")
        self.color_preview.setFixedSize(220, 165)
        self.color_preview.setAlignment(QtCore.Qt.AlignCenter)
        self.color_preview.setStyleSheet("border:1px solid palette(mid);")
        preview_row.addWidget(self.color_preview)
        self.control_preview = QtWidgets.QLabel("(line-art control)")
        self.control_preview.setFixedSize(220, 165)
        self.control_preview.setAlignment(QtCore.Qt.AlignCenter)
        self.control_preview.setStyleSheet("border:1px solid palette(mid);")
        preview_row.addWidget(self.control_preview)
        layout.addLayout(preview_row)

        self.progress_bar = QtWidgets.QProgressBar()
        self.progress_bar.setRange(0, 1)
        layout.addWidget(self.progress_bar)

        self.status_label = QtWidgets.QLabel("Ready.")
        self.status_label.setWordWrap(True)
        layout.addWidget(self.status_label)

        footer = QtWidgets.QLabel(
            "Images may be sent to a third-party provider you configure (or "
            "stay entirely local with ComfyUI). No API keys are ever stored "
            "in FreeCAD's own preferences -- see README 'Key storage'."
        )
        footer.setWordWrap(True)
        footer.setStyleSheet("color: palette(mid); font-size: 10px;")
        layout.addWidget(footer)

        close_row = QtWidgets.QHBoxLayout()
        close_row.addStretch(1)
        close_button = QtWidgets.QPushButton("Close")
        close_button.clicked.connect(self.accept)
        close_row.addWidget(close_button)
        layout.addLayout(close_row)

        self._on_provider_changed(0)

    def _build_comfyui_settings(self):
        w = QtWidgets.QWidget()
        form = QtWidgets.QFormLayout(w)
        self.comfyui_endpoint_edit = QtWidgets.QLineEdit()
        form.addRow("Endpoint URL:", self.comfyui_endpoint_edit)
        self.comfyui_checkpoint_edit = QtWidgets.QLineEdit()
        form.addRow("Checkpoint name:", self.comfyui_checkpoint_edit)
        self.comfyui_controlnet_edit = QtWidgets.QLineEdit()
        form.addRow("ControlNet (lineart) name:", self.comfyui_controlnet_edit)
        note = QtWidgets.QLabel(
            "No API key needed. Run ComfyUI locally; edit the checkpoint/"
            "ControlNet names above to match models you have installed."
        )
        note.setWordWrap(True)
        note.setStyleSheet("color: palette(mid); font-size: 10px;")
        form.addRow(note)
        return w

    def _build_stability_settings(self):
        w = QtWidgets.QWidget()
        form = QtWidgets.QFormLayout(w)
        self.stability_key_file_edit = QtWidgets.QLineEdit()
        self.stability_key_file_edit.setPlaceholderText("~/.secrets/stability.key")
        form.addRow("Key file:", self.stability_key_file_edit)
        self.stability_key_command_edit = QtWidgets.QLineEdit()
        self.stability_key_command_edit.setPlaceholderText("e.g. pass show stability-ai")
        form.addRow("Key command (alt.):", self.stability_key_command_edit)
        note = QtWidgets.QLabel(
            "Key is read fresh from the file/command every call, never "
            "cached or stored in FreeCAD's own preferences."
        )
        note.setWordWrap(True)
        note.setStyleSheet("color: palette(mid); font-size: 10px;")
        form.addRow(note)
        return w

    def _build_openai_settings(self):
        w = QtWidgets.QWidget()
        form = QtWidgets.QFormLayout(w)
        self.openai_key_file_edit = QtWidgets.QLineEdit()
        self.openai_key_file_edit.setPlaceholderText("~/.secrets/openai.key")
        form.addRow("Key file:", self.openai_key_file_edit)
        self.openai_key_command_edit = QtWidgets.QLineEdit()
        self.openai_key_command_edit.setPlaceholderText("e.g. pass show openai")
        form.addRow("Key command (alt.):", self.openai_key_command_edit)
        self.openai_model_edit = QtWidgets.QLineEdit()
        form.addRow("Model:", self.openai_model_edit)
        note = QtWidgets.QLabel(
            "images.edit is a vision-language edit model -- a good quick "
            "style pass, looser geometry fidelity than the ControlNet "
            "channels (see README)."
        )
        note.setWordWrap(True)
        note.setStyleSheet("color: palette(mid); font-size: 10px;")
        form.addRow(note)
        return w

    # --------------------------------------------------------- settings
    def _load_settings(self):
        self.prompt_edit.setPlainText(
            settings.get_string("prompt") or presets.STYLE_PRESETS[0]["prompt"]
        )
        preset_label = settings.get_string("style_preset")
        idx = self.preset_combo.findText(preset_label)
        if idx >= 0:
            self.preset_combo.blockSignals(True)
            self.preset_combo.setCurrentIndex(idx)
            self.preset_combo.blockSignals(False)

        provider_name = settings.get_string("provider")
        idx = self.provider_combo.findData(provider_name)
        if idx >= 0:
            self.provider_combo.setCurrentIndex(idx)

        strength = settings.get_float("strength")
        self.strength_slider.setValue(int(round(strength * 100)))

        self.width_spin.setValue(settings.get_int("width"))
        self.height_spin.setValue(settings.get_int("height"))

        channel = settings.get_string("lineart_channel")
        idx = self.channel_combo.findData(channel)
        if idx >= 0:
            self.channel_combo.setCurrentIndex(idx)

        self.output_edit.setText(settings.get_string("output_folder"))

        self.comfyui_endpoint_edit.setText(settings.get_string("comfyui_endpoint"))
        self.comfyui_checkpoint_edit.setText(settings.get_string("comfyui_checkpoint"))
        self.comfyui_controlnet_edit.setText(settings.get_string("comfyui_controlnet"))

        self.stability_key_file_edit.setText(settings.get_string("stability_key_file"))
        self.stability_key_command_edit.setText(settings.get_string("stability_key_command"))

        self.openai_key_file_edit.setText(settings.get_string("openai_key_file"))
        self.openai_key_command_edit.setText(settings.get_string("openai_key_command"))
        self.openai_model_edit.setText(settings.get_string("openai_model"))

    def _save_settings(self):
        settings.set_string("prompt", self.prompt_edit.toPlainText())
        settings.set_string("style_preset", self.preset_combo.currentText())
        settings.set_string("provider", self.provider_combo.currentData())
        settings.set_float("strength", self.strength_slider.value() / 100.0)
        settings.set_int("width", self.width_spin.value())
        settings.set_int("height", self.height_spin.value())
        settings.set_string("lineart_channel", self.channel_combo.currentData())
        settings.set_string("output_folder", self.output_edit.text().strip())
        settings.set_string("comfyui_endpoint", self.comfyui_endpoint_edit.text().strip())
        settings.set_string("comfyui_checkpoint", self.comfyui_checkpoint_edit.text().strip())
        settings.set_string("comfyui_controlnet", self.comfyui_controlnet_edit.text().strip())
        settings.set_string("stability_key_file", self.stability_key_file_edit.text().strip())
        settings.set_string("stability_key_command", self.stability_key_command_edit.text().strip())
        settings.set_string("openai_key_file", self.openai_key_file_edit.text().strip())
        settings.set_string("openai_key_command", self.openai_key_command_edit.text().strip())
        settings.set_string("openai_model", self.openai_model_edit.text().strip())

    # ------------------------------------------------------------- slots
    def _on_preset_changed(self, index):
        preset = presets.STYLE_PRESETS[index]
        self.prompt_edit.setPlainText(preset["prompt"])

    def _on_provider_changed(self, index):
        self.provider_stack.setCurrentIndex(index)

    def _on_strength_changed(self, value):
        self.strength_label.setText("{:.2f}".format(value / 100.0))

    def _on_browse_output(self):
        path = QtWidgets.QFileDialog.getExistingDirectory(self, "Output folder")
        if path:
            self.output_edit.setText(path)

    # ------------------------------------------------------- provider build
    def _current_provider(self):
        name = self.provider_combo.currentData()
        if name == "comfyui":
            return ComfyUIProvider(
                endpoint=self.comfyui_endpoint_edit.text().strip(),
                checkpoint_name=self.comfyui_checkpoint_edit.text().strip(),
                controlnet_name=self.comfyui_controlnet_edit.text().strip(),
            )
        elif name == "stability":
            return StabilityProvider(
                key_file=self.stability_key_file_edit.text().strip(),
                key_command=self.stability_key_command_edit.text().strip(),
            )
        elif name == "openai":
            return OpenAIProvider(
                key_file=self.openai_key_file_edit.text().strip(),
                key_command=self.openai_key_command_edit.text().strip(),
                model=self.openai_model_edit.text().strip(),
            )
        raise ValueError("Unknown provider: {}".format(name))

    # ------------------------------------------------------------ output
    def _output_dir(self):
        override = self.output_edit.text().strip()
        if override:
            return override
        doc = App.ActiveDocument
        if doc is not None and doc.FileName:
            return os.path.join(os.path.dirname(doc.FileName), "airender")
        # Unsaved document fallback -- documented in README, not silent.
        base = App.getUserAppDataDir() if hasattr(App, "getUserAppDataDir") else "."
        return os.path.join(base, "AIRenderOutput", "unsaved")

    def _timestamp(self):
        return datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

    # ----------------------------------------------------------- capture
    def _run_capture(self):
        doc = App.ActiveDocument
        if doc is None:
            raise ValueError("No active document.")
        view = Gui.ActiveDocument.ActiveView

        out_dir = self._output_dir()
        os.makedirs(out_dir, exist_ok=True)
        ts = self._timestamp()

        width = self.width_spin.value()
        height = self.height_spin.value()

        color_path = os.path.join(out_dir, "{}_color.png".format(ts))
        capture.capture_color(view, color_path, width, height, background="White")

        channel = self.channel_combo.currentData()
        control_path = os.path.join(out_dir, "{}_control.png".format(ts))
        if channel == "drawstyle":
            control_path, restored = capture.capture_drawstyle_lineart(
                view, control_path, width, height
            )
            if not restored:
                self.status_label.setText(
                    "Warning: draw-style restore may have failed; check the 3D view."
                )
        else:
            control_path, edge_count = capture.capture_vector_lineart(
                doc, control_path, width, height, view=view
            )
            if edge_count == 0:
                self.status_label.setText(
                    "Warning: vector line-art had 0 edges -- is anything visible in the document?"
                )

        self._last_color_path = color_path
        self._last_control_path = control_path
        self._last_channel_used = channel
        self._update_previews()
        return color_path, control_path

    def _update_previews(self):
        from PySide import QtGui

        if self._last_color_path and os.path.exists(self._last_color_path):
            pm = QtGui.QPixmap(self._last_color_path).scaled(
                self.color_preview.width(), self.color_preview.height(),
                QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation,
            )
            self.color_preview.setPixmap(pm)
        if self._last_control_path and os.path.exists(self._last_control_path):
            pm = QtGui.QPixmap(self._last_control_path).scaled(
                self.control_preview.width(), self.control_preview.height(),
                QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation,
            )
            self.control_preview.setPixmap(pm)

    def _on_capture_only(self):
        self._save_settings()
        try:
            self.status_label.setText("Capturing...")
            QtWidgets.QApplication.processEvents()
            self._run_capture()
            self.status_label.setText(
                "Capture complete: {}".format(os.path.dirname(self._last_color_path))
            )
        except Exception as exc:  # noqa: BLE001
            self.status_label.setText("Capture failed: {}".format(exc))
            QtWidgets.QMessageBox.critical(self, "AI Render", "Capture failed:\n{}".format(exc))

    # ------------------------------------------------------------- render
    def _set_busy(self, busy):
        self.render_button.setEnabled(not busy)
        self.capture_button.setEnabled(not busy)

    def _on_render(self):
        self._save_settings()
        try:
            self.status_label.setText("Capturing...")
            QtWidgets.QApplication.processEvents()
            self._run_capture()
        except Exception as exc:  # noqa: BLE001
            self.status_label.setText("Capture failed: {}".format(exc))
            QtWidgets.QMessageBox.critical(self, "AI Render", "Capture failed:\n{}".format(exc))
            return

        provider = self._current_provider()
        if not provider.is_configured():
            # Graceful no-key/no-endpoint degradation (v1 scope item 3):
            # capture already ran and previews are populated; tell the
            # user how to finish setup rather than failing/crashing.
            self.status_label.setText(
                "Capture done. {} is not configured yet.".format(provider.display_name)
            )
            QtWidgets.QMessageBox.information(
                self, "AI Render - provider not configured", provider.configuration_hint()
            )
            return

        request = RenderRequest(
            prompt=self.prompt_edit.toPlainText().strip(),
            color_image_path=self._last_color_path,
            control_image_path=self._last_control_path,
            strength=self.strength_slider.value() / 100.0,
            width=self.width_spin.value(),
            height=self.height_spin.value(),
        )

        self._set_busy(True)
        self.progress_bar.setRange(0, 0)
        self.status_label.setText("Sending to {}...".format(provider.display_name))

        self._worker = RenderWorker(provider, request, self)
        self._worker.finished_ok.connect(lambda result: self._on_render_finished(provider, request, result))
        self._worker.failed.connect(self._on_render_failed)
        self._worker.start()

    def _on_render_failed(self, message):
        self._set_busy(False)
        self.progress_bar.setRange(0, 1)
        self.progress_bar.setValue(0)
        self.status_label.setText("Render failed: {}".format(message))
        QtWidgets.QMessageBox.critical(self, "AI Render", "Render failed:\n{}".format(message))

    def _on_render_finished(self, provider, request, result):
        self._set_busy(False)
        self.progress_bar.setRange(0, 1)
        self.progress_bar.setValue(1)

        out_dir = os.path.dirname(self._last_color_path)
        ts = self._timestamp()
        saved_paths = []
        for i, image_bytes in enumerate(result.images):
            path = os.path.join(out_dir, "{}_result_{}.png".format(ts, i))
            with open(path, "wb") as f:
                f.write(image_bytes)
            saved_paths.append(path)

        sidecar = {
            "provider": provider.name,
            "provider_display_name": provider.display_name,
            "prompt": request.prompt,
            "strength": request.strength,
            "resolution": [request.width, request.height],
            "color_image": self._last_color_path,
            "control_image": self._last_control_path,
            "lineart_channel": self._last_channel_used,
            "request_payload": _json_safe(result.request_payload),
            "response_meta": _json_safe(result.response_meta),
            "result_images": saved_paths,
            "timestamp": ts,
        }
        sidecar_path = os.path.join(out_dir, "{}_request.json".format(ts))
        with open(sidecar_path, "w") as f:
            json.dump(sidecar, f, indent=2)

        self.last_result_paths = saved_paths
        self.status_label.setText(
            "Done: {} image(s) saved to {}".format(len(saved_paths), out_dir)
        )

        info_text = (
            "Provider: {}\nPrompt: {}\nStrength: {}\nControl channel: {}\n"
            "Sidecar: {}"
        ).format(
            provider.display_name, request.prompt, request.strength,
            self._last_channel_used, sidecar_path,
        )
        results = ResultsDialog(saved_paths, info_text, self)
        results.setModal(False)
        results.show()
        Gui.getMainWindow()._airender_results = results


def _json_safe(obj):
    try:
        json.dumps(obj)
        return obj
    except TypeError:
        return json.loads(json.dumps(obj, default=str))
