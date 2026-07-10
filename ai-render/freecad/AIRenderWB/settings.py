# SPDX-License-Identifier: MIT
"""Non-secret preference storage for AIRender, using FreeCAD's normal
Parameter store. This is fine here because NOTHING secret is ever kept
here -- provider choice, endpoint URLs, key-FILE paths (not the key
itself), model/checkpoint names, output folder, resolution, strength,
line-art channel. See keystore.py's module docstring for why the actual
API keys deliberately do NOT live here.
"""
import FreeCAD as App

_GROUP_PATH = "User parameter:BaseApp/Preferences/Mod/AIRender"

_STRING_DEFAULTS = {
    "provider": "comfyui",
    "prompt": "",
    "style_preset": "Photorealistic product shot",
    "output_folder": "",  # empty => <doc-dir>/airender/
    "lineart_channel": "drawstyle",  # "drawstyle" (default, Wireframe draw
    # style, exact-camera-matched) or "vector" (TechDraw projectToSVG,
    # headless-safe secondary channel) -- see capture.py module docstring
    # for the 2026-07-10 bug-fix pass that established this default.
    "comfyui_endpoint": "http://127.0.0.1:8188",
    "comfyui_checkpoint": "sd_xl_base_1.0.safetensors",
    "comfyui_controlnet": "control_v11p_sd15_lineart.pth",
    "stability_key_file": "",
    "stability_key_command": "",
    "openai_key_file": "",
    "openai_key_command": "",
    "openai_model": "gpt-image-1",
}

_INT_DEFAULTS = {
    "width": 768,
    "height": 768,
}

_FLOAT_DEFAULTS = {
    "strength": 0.65,
}


def _group():
    return App.ParamGet(_GROUP_PATH)


def get_string(key):
    return _group().GetString(key, _STRING_DEFAULTS.get(key, ""))


def set_string(key, value):
    _group().SetString(key, value)


def get_int(key):
    return _group().GetInt(key, _INT_DEFAULTS.get(key, 0))


def set_int(key, value):
    _group().SetInt(key, int(value))


def get_float(key):
    return _group().GetFloat(key, _FLOAT_DEFAULTS.get(key, 0.0))


def set_float(key, value):
    _group().SetFloat(key, float(value))


def all_string_keys():
    return list(_STRING_DEFAULTS.keys())
