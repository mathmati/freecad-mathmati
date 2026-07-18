# SPDX-License-Identifier: MIT
"""Shared provider interface. Every adapter (ComfyUI, Stability, OpenAI)
implements this so dialog.py can treat them uniformly.

BYO-everything posture: no bundled billing, no bundled
model weights, ever. Every provider here is either a local endpoint the
user already runs (ComfyUI) or a cloud API the user brings their own key
to (Stability, OpenAI).
"""


class ProviderError(Exception):
    """Raised for any provider failure the dialog should show to the user
    as a helpful message rather than a crash -- no endpoint reachable, no
    key configured, a non-2xx response, an unexpected response shape."""


class RenderRequest(object):
    """Everything a provider adapter needs to build its request. Capture
    paths point at PNGs already written to disk by capture.py."""

    def __init__(self, prompt, color_image_path, control_image_path,
                 strength=0.65, width=768, height=768, negative_prompt="",
                 seed=None):
        self.prompt = prompt
        self.color_image_path = color_image_path
        self.control_image_path = control_image_path
        self.strength = float(strength)
        self.width = int(width)
        self.height = int(height)
        self.negative_prompt = negative_prompt or ""
        self.seed = seed


class RenderResult(object):
    """What a provider call returns: raw image bytes (addon writes them to
    disk itself, so every provider's save path is identical) plus the
    request payload actually sent (for the audit-trail sidecar and for
    verification) and the raw response metadata."""

    def __init__(self, images, request_payload, response_meta=None):
        self.images = images  # list[bytes]
        self.request_payload = request_payload  # JSON-serializable dict
        self.response_meta = response_meta or {}


class Provider(object):
    name = "base"
    display_name = "Base provider"

    def is_configured(self):
        """Return True if this provider has enough settings (endpoint URL,
        or a resolvable API key) to attempt a call. Must NOT touch the
        network -- just check local configuration."""
        raise NotImplementedError

    def configuration_hint(self):
        """Human-readable string shown when is_configured() is False, or
        when a call fails for a configuration reason."""
        return "Configure {} in the AI Render dialog's provider settings.".format(
            self.display_name
        )

    def build_request_payload(self, request):
        """Return the JSON-serializable payload/workflow this provider
        WOULD send for `request`, without performing any network I/O.
        Used both by render() and directly by verification code so the
        request shape can be asserted without needing a live provider."""
        raise NotImplementedError

    def render(self, request):
        """Perform the real (or stub-server) network round trip and
        return a RenderResult. Raises ProviderError on any failure,
        with a message suitable to show directly to the user."""
        raise NotImplementedError
