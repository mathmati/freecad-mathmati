# SPDX-License-Identifier: MIT
"""Provider registry: BYO-key adapters the "AI Render..." dialog can pick
from. Local ComfyUI is listed first / is the v1 default (no key needed at
all); Stability and OpenAI are key-based cloud options. See each module's
docstring for why.
"""
from .base import Provider, ProviderError, RenderRequest, RenderResult
from .comfyui import ComfyUIProvider
from .stability import StabilityProvider
from .openai_provider import OpenAIProvider

PROVIDER_CLASSES = [ComfyUIProvider, StabilityProvider, OpenAIProvider]

PROVIDER_BY_NAME = {cls.name: cls for cls in PROVIDER_CLASSES}

__all__ = [
    "Provider",
    "ProviderError",
    "RenderRequest",
    "RenderResult",
    "ComfyUIProvider",
    "StabilityProvider",
    "OpenAIProvider",
    "PROVIDER_CLASSES",
    "PROVIDER_BY_NAME",
]
