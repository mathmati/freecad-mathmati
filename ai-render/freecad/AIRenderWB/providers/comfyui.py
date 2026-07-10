# SPDX-License-Identifier: MIT
"""Local ComfyUI provider -- the v1 DEFAULT, since it needs no key
management at all. Plain REST against a user-run ComfyUI instance:

  POST /upload/image   -- send the color (init) and control (line-art)
                           images so the workflow graph can reference them
                           by the server-assigned filename
  POST /prompt          -- submit the workflow JSON, get back a prompt_id
  GET  /history/{id}    -- poll until the prompt has finished
  GET  /view            -- fetch the resulting image bytes

No API key of any kind -- just a URL (default http://127.0.0.1:8188,
user-configurable). This is also the channel exercised end-to-end against
a local stub ComfyUI server as part of this addon's automated
verification.
"""
import time
import uuid

from . import http_client
from .base import Provider, ProviderError, RenderResult

DEFAULT_ENDPOINT = "http://127.0.0.1:8188"


class ComfyUIProvider(Provider):
    name = "comfyui"
    display_name = "Local ComfyUI"

    def __init__(self, endpoint=DEFAULT_ENDPOINT, checkpoint_name="sd_xl_base_1.0.safetensors",
                 controlnet_name="control_v11p_sd15_lineart.pth", steps=20, cfg=7.0,
                 poll_timeout=180, poll_interval=1.0):
        self.endpoint = (endpoint or DEFAULT_ENDPOINT).rstrip("/")
        self.checkpoint_name = checkpoint_name
        self.controlnet_name = controlnet_name
        self.steps = steps
        self.cfg = cfg
        self.poll_timeout = poll_timeout
        self.poll_interval = poll_interval

    def is_configured(self):
        return bool(self.endpoint)

    def configuration_hint(self):
        return (
            "No ComfyUI endpoint reachable at {}. Install/run ComfyUI locally "
            "(https://github.com/comfyanonymous/ComfyUI) and confirm the URL in "
            "the AI Render dialog's provider settings -- default is "
            "http://127.0.0.1:8188. This is the only provider that needs no "
            "API key at all.".format(self.endpoint)
        )

    # ---------------------------------------------------------- workflow
    def build_request_payload(self, request, init_filename="airender_init.png",
                               control_filename="airender_control.png"):
        """The workflow graph: checkpoint -> positive/negative CLIP text ->
        control-net-conditioned img2img KSampler -> VAE decode -> save.
        Node IDs are strings, matching ComfyUI's own `/prompt` API shape.
        """
        workflow = {
            "1": {
                "class_type": "CheckpointLoaderSimple",
                "inputs": {"ckpt_name": self.checkpoint_name},
            },
            "2": {
                "class_type": "LoadImage",
                "inputs": {"image": init_filename},
            },
            "3": {
                "class_type": "LoadImage",
                "inputs": {"image": control_filename},
            },
            "4": {
                "class_type": "CLIPTextEncode",
                "inputs": {"text": request.prompt, "clip": ["1", 1]},
            },
            "5": {
                "class_type": "CLIPTextEncode",
                "inputs": {"text": request.negative_prompt, "clip": ["1", 1]},
            },
            "6": {
                "class_type": "ControlNetLoader",
                "inputs": {"control_net_name": self.controlnet_name},
            },
            "7": {
                "class_type": "ControlNetApplyAdvanced",
                "inputs": {
                    "positive": ["4", 0],
                    "negative": ["5", 0],
                    "control_net": ["6", 0],
                    "image": ["3", 0],
                    "strength": request.strength,
                    "start_percent": 0.0,
                    "end_percent": 1.0,
                },
            },
            "8": {
                "class_type": "VAEEncode",
                "inputs": {"pixels": ["2", 0], "vae": ["1", 2]},
            },
            "9": {
                "class_type": "KSampler",
                "inputs": {
                    "model": ["1", 0],
                    "positive": ["7", 0],
                    "negative": ["7", 1],
                    "latent_image": ["8", 0],
                    "seed": request.seed if request.seed is not None else 0,
                    "steps": self.steps,
                    "cfg": self.cfg,
                    "sampler_name": "euler",
                    "scheduler": "normal",
                    "denoise": request.strength,
                },
            },
            "10": {
                "class_type": "VAEDecode",
                "inputs": {"samples": ["9", 0], "vae": ["1", 2]},
            },
            "11": {
                "class_type": "SaveImage",
                "inputs": {"images": ["10", 0], "filename_prefix": "airender"},
            },
        }
        return workflow

    # ------------------------------------------------------------ render
    def render(self, request):
        if not self.is_configured():
            raise ProviderError(self.configuration_hint())

        client_id = uuid.uuid4().hex

        with open(request.color_image_path, "rb") as f:
            init_bytes = f.read()
        with open(request.control_image_path, "rb") as f:
            control_bytes = f.read()

        try:
            init_name = self._upload_image(init_bytes, "airender_init.png")
            control_name = self._upload_image(control_bytes, "airender_control.png")
        except http_client.HTTPError as exc:
            raise ProviderError(
                "ComfyUI image upload failed ({}). {}".format(exc, self.configuration_hint())
            )

        workflow = self.build_request_payload(
            request, init_filename=init_name, control_filename=control_name
        )
        payload = {"prompt": workflow, "client_id": client_id}

        try:
            status, body = http_client.post_json(self.endpoint + "/prompt", payload)
        except http_client.HTTPError as exc:
            raise ProviderError(
                "ComfyUI did not accept the workflow ({}). {}".format(
                    exc, self.configuration_hint()
                )
            )

        import json

        response = json.loads(body.decode("utf-8"))
        prompt_id = response.get("prompt_id")
        if not prompt_id:
            raise ProviderError(
                "ComfyUI /prompt response had no prompt_id: {}".format(response)
            )

        history = self._poll_history(prompt_id)
        images = self._collect_images(history, prompt_id)
        if not images:
            raise ProviderError(
                "ComfyUI reported the prompt finished but no output images were found."
            )

        return RenderResult(
            images=images,
            request_payload=payload,
            response_meta={"prompt_id": prompt_id, "endpoint": self.endpoint},
        )

    def _upload_image(self, content, filename):
        status, body = http_client.post_multipart(
            self.endpoint + "/upload/image",
            fields={"type": "input", "overwrite": "true"},
            files={"image": (filename, content, "image/png")},
        )
        import json

        info = json.loads(body.decode("utf-8"))
        return info.get("name", filename)

    def _poll_history(self, prompt_id):
        deadline = time.time() + self.poll_timeout
        while time.time() < deadline:
            try:
                status, history = http_client.get_json(
                    self.endpoint + "/history/" + prompt_id
                )
            except http_client.HTTPError:
                history = {}
            if prompt_id in history:
                return history[prompt_id]
            time.sleep(self.poll_interval)
        raise ProviderError(
            "Timed out after {}s waiting for ComfyUI to finish prompt {}.".format(
                self.poll_timeout, prompt_id
            )
        )

    def _collect_images(self, history, prompt_id):
        images = []
        outputs = history.get("outputs", {})
        for node_id, node_output in outputs.items():
            for img in node_output.get("images", []):
                params = {
                    "filename": img.get("filename"),
                    "subfolder": img.get("subfolder", ""),
                    "type": img.get("type", "output"),
                }
                url = self.endpoint + "/view?" + _urlencode(params)
                status, content = http_client.get_bytes(url)
                images.append(content)
        return images


def _urlencode(params):
    import urllib.parse

    return urllib.parse.urlencode(params)
