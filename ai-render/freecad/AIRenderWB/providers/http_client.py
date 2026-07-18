# SPDX-License-Identifier: MIT
"""Tiny stdlib-only HTTP client for the provider adapters.

FreeCAD's bundled Python does not ship `requests`, so this uses only
`urllib`/`http.client` from the standard library -- both for the real
providers and so the addon has zero extra pip dependencies to install.
"""
import json
import mimetypes
import uuid
import urllib.request
import urllib.error


class HTTPError(Exception):
    def __init__(self, message, status=None, body=None):
        super().__init__(message)
        self.status = status
        self.body = body


def post_json(url, payload, headers=None, timeout=30):
    data = json.dumps(payload).encode("utf-8")
    req_headers = {"Content-Type": "application/json"}
    req_headers.update(headers or {})
    req = urllib.request.Request(url, data=data, headers=req_headers, method="POST")
    return _do_request(req, timeout)


def get_json(url, headers=None, timeout=30):
    req = urllib.request.Request(url, headers=headers or {}, method="GET")
    status, body = _do_request(req, timeout)
    return status, json.loads(body.decode("utf-8"))


def get_bytes(url, headers=None, timeout=60):
    req = urllib.request.Request(url, headers=headers or {}, method="GET")
    return _do_request(req, timeout)


def post_multipart(url, fields, files, headers=None, timeout=60):
    """fields: dict[str,str]. files: dict[str, (filename, bytes, content_type)]."""
    boundary = uuid.uuid4().hex
    body = bytearray()

    def _add_field(name, value):
        body.extend(
            "--{}\r\nContent-Disposition: form-data; name=\"{}\"\r\n\r\n{}\r\n".format(
                boundary, name, value
            ).encode("utf-8")
        )

    def _add_file(name, filename, content, content_type):
        body.extend(
            (
                "--{}\r\nContent-Disposition: form-data; name=\"{}\"; "
                'filename="{}"\r\nContent-Type: {}\r\n\r\n'
            ).format(boundary, name, filename, content_type).encode("utf-8")
        )
        body.extend(content)
        body.extend(b"\r\n")

    for name, value in (fields or {}).items():
        _add_field(name, value)
    for name, (filename, content, content_type) in (files or {}).items():
        if content_type is None:
            content_type = mimetypes.guess_type(filename)[0] or "application/octet-stream"
        _add_file(name, filename, content, content_type)
    body.extend("--{}--\r\n".format(boundary).encode("utf-8"))

    req_headers = {"Content-Type": "multipart/form-data; boundary={}".format(boundary)}
    req_headers.update(headers or {})
    req = urllib.request.Request(url, data=bytes(body), headers=req_headers, method="POST")
    return _do_request(req, timeout)


def _do_request(req, timeout):
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.status, resp.read()
    except urllib.error.HTTPError as exc:
        body = exc.read()
        raise HTTPError(
            "HTTP {} from {}: {}".format(exc.code, req.full_url, body[:500]),
            status=exc.code,
            body=body,
        )
    except urllib.error.URLError as exc:
        raise HTTPError("Could not reach {}: {}".format(req.full_url, exc.reason))
