# SPDX-License-Identifier: MIT
"""OpenAI provider -- key-based cloud option, `images.edit` (vision-
language image edit model, e.g. gpt-image-1 / the newer gpt-image-2).
This is a good "quick style pass" but has no explicit ControlNet/depth-style structural conditioning,
so structural fidelity is looser than the ComfyUI/Stability channels --
disclosed in the README, not hidden.

Docs: https://platform.openai.com/docs/api-reference/images/createEdit
"""
import base64
import json

from . import http_client
from .base import Provider, ProviderError, RenderResult
from .. import keystore

DEFAULT_API_BASE = "https://api.openai.com"
DEFAULT_MODEL = "gpt-image-1"  # set to "gpt-image-2" once available on your account


class OpenAIProvider(Provider):
    name = "openai"
    display_name = "OpenAI (images.edit)"

    def __init__(self, key_file=None, key_command=None, api_base=DEFAULT_API_BASE,
                 model=DEFAULT_MODEL):
        self.key_file = key_file
        self.key_command = key_command
        self.api_base = (api_base or DEFAULT_API_BASE).rstrip("/")
        self.model = model or DEFAULT_MODEL

    def is_configured(self):
        return bool(self.key_file or self.key_command)

    def configuration_hint(self):
        return (
            "No OpenAI key configured. Get a key at platform.openai.com, "
            "save it to a file only you can read, and point this "
            "provider's 'key file' setting at that path (never pasted "
            "directly into FreeCAD's own preferences)."
        )

    def build_request_payload(self, request):
        return {
            "url": self.api_base + "/v1/images/edits",
            "fields": {"prompt": request.prompt, "model": self.model, "n": 1,
                       "size": "{}x{}".format(request.width, request.height)},
            "files": {"image": "color_image (viewport capture)"},
        }

    def render(self, request):
        if not self.is_configured():
            raise ProviderError(self.configuration_hint())

        try:
            key = keystore.resolve_key(self.key_file, self.key_command)
        except keystore.KeyError_ as exc:
            raise ProviderError("{} {}".format(exc, self.configuration_hint()))

        # OpenAI's images.edit takes the image to edit; we pass the color
        # viewport capture (the vision-language edit model works on the
        # rendered image itself, not a separate control channel -- see
        # module docstring on structural-fidelity limits).
        with open(request.color_image_path, "rb") as f:
            image_bytes = f.read()

        payload = self.build_request_payload(request)
        headers = {"Authorization": "Bearer {}".format(key)}

        try:
            status, body = http_client.post_multipart(
                payload["url"],
                fields={k: str(v) for k, v in payload["fields"].items()},
                files={"image": ("color.png", image_bytes, "image/png")},
                headers=headers,
            )
        except http_client.HTTPError as exc:
            raise ProviderError("OpenAI request failed: {}".format(exc))

        response = json.loads(body.decode("utf-8"))
        data = response.get("data") or []
        images = []
        for item in data:
            if "b64_json" in item:
                images.append(base64.b64decode(item["b64_json"]))
            elif "url" in item:
                status, content = http_client.get_bytes(item["url"])
                images.append(content)
        if not images:
            raise ProviderError(
                "OpenAI response had no usable image data: {}".format(response)
            )

        return RenderResult(
            images=images,
            request_payload={"url": payload["url"], "fields": payload["fields"]},
            response_meta={"model": self.model},
        )
