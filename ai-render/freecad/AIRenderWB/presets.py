# SPDX-License-Identifier: MIT
"""Style presets for the "AI Render..." dialog's prompt field.

Each preset is a starting prompt the user can freely edit before
rendering -- these are not locked templates, just useful defaults for the
four style families named in this addon's v1 scope.
"""

STYLE_PRESETS = [
    {
        "label": "Photorealistic product shot",
        "prompt": (
            "photorealistic product photography, studio lighting, soft "
            "shadows, clean seamless background, sharp focus, high detail, "
            "8k render"
        ),
    },
    {
        "label": "Architectural render",
        "prompt": (
            "architectural visualization, realistic materials, natural "
            "daylight, soft global illumination, context landscaping, "
            "professional archviz render"
        ),
    },
    {
        "label": "Clay render",
        "prompt": (
            "clean matte clay render, uniform neutral gray material, soft "
            "studio lighting, ambient occlusion, no textures, form study"
        ),
    },
    {
        "label": "Blueprint",
        "prompt": (
            "technical blueprint drawing, white line-art on deep blue "
            "background, drafting style, crisp linework, dimension-style "
            "annotations"
        ),
    },
]


def preset_by_label(label):
    for p in STYLE_PRESETS:
        if p["label"] == label:
            return p
    return None
