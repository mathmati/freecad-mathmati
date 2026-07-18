# SPDX-License-Identifier: MIT
"""Stability AI provider -- key-based cloud option. Stability's
"Stable Image Control" family (structure/sketch-guided
endpoints) is the best "simple REST + real structural control" fit among
cloud providers for a line-art control image, so this adapter targets the
`stable-image/control/structure` endpoint (REST v2beta).

Docs: https://platform.stability.ai/docs/api-reference (Control -> Structure)
"""
import json

from . import http_client
from .base import Provider, ProviderError, RenderResult
from .. import keystore

DEFAULT_API_BASE = "https://api.stability.ai"
DEFAULT_MODEL_PATH = "/v2beta/stable-image/control/structure"


class StabilityProvider(Provider):
    name = "stability"
    display_name = "Stability AI (Control - Structure)"

    def __init__(self, key_file=None, key_command=None, api_base=DEFAULT_API_BASE,
                 output_format="png"):
        self.key_file = key_file
        self.key_command = key_command
        self.api_base = (api_base or DEFAULT_API_BASE).rstrip("/")
        self.output_format = output_format

    def is_configured(self):
        return bool(self.key_file or self.key_command)

    def configuration_hint(self):
        return (
            "No Stability AI key configured. Get a key at "
            "platform.stability.ai, save it to a file only you can read, "
            "and point this provider's 'key file' setting at that path "
            "(never pasted directly into FreeCAD's own preferences)."
        )

    def build_request_payload(self, request):
        """Returns the (non-file) form fields that WOULD be sent, plus a
        description of which file goes in which multipart field -- used
        for verification without needing a resolvable key."""
        return {
            "url": self.api_base + DEFAULT_MODEL_PATH,
            "fields": {
                "prompt": request.prompt,
                "negative_prompt": request.negative_prompt,
                "control_strength": request.strength,
                "output_format": self.output_format,
            },
            "files": {"image": "control_image (line-art capture)"},
        }

    def render(self, request):
        if not self.is_configured():
            raise ProviderError(self.configuration_hint())

        try:
            key = keystore.resolve_key(self.key_file, self.key_command)
        except keystore.KeyError_ as exc:
            raise ProviderError("{} {}".format(exc, self.configuration_hint()))

        with open(request.control_image_path, "rb") as f:
            control_bytes = f.read()

        payload = self.build_request_payload(request)
        headers = {
            "Authorization": "Bearer {}".format(key),
            "Accept": "application/json",
        }

        try:
            status, body = http_client.post_multipart(
                payload["url"],
                fields={k: str(v) for k, v in payload["fields"].items()},
                files={"image": ("control.png", control_bytes, "image/png")},
                headers=headers,
            )
        except http_client.HTTPError as exc:
            raise ProviderError("Stability AI request failed: {}".format(exc))

        response = json.loads(body.decode("utf-8"))
        image_b64 = response.get("image")
        if not image_b64:
            raise ProviderError(
                "Stability AI response had no 'image' field: {}".format(
                    {k: v for k, v in response.items() if k != "image"}
                )
            )
        import base64

        images = [base64.b64decode(image_b64)]
        return RenderResult(
            images=images,
            request_payload={"url": payload["url"], "fields": payload["fields"]},
            response_meta={"finish_reason": response.get("finish_reason"), "seed": response.get("seed")},
        )
