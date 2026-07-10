# SPDX-License-Identifier: MIT
"""File-based / keychain-CLI secret handling for provider API keys.

Follows the precedent set by `ghbalf/freecad-ai`: NEVER write an API key
into FreeCAD's own
Parameter/XML store (`App.ParamGet(...)`) -- that store is plaintext and
often synced/backed-up in ways a secret shouldn't be. Instead:

  * a user-chosen **key file** path (supports `~` and `$ENV_VAR`
    expansion), re-read from disk on every call rather than cached in
    memory or written into the document, ideally `chmod 600` on Unix
    (checked, warned about, never silently fixed by us); or
  * a **key command** the user configures once (e.g. `pass show
    stability-ai`, `security find-generic-password -s stability -w`, or
    any OS-keychain CLI) -- we shell out to it and use stdout, again
    re-run per call, never cached.

Only the *non-secret* preferences (which provider is selected, the
ComfyUI endpoint URL, the key-file/key-command path itself, output
folder, etc.) are fine to keep in FreeCAD's normal Parameter store --
those aren't secrets, just settings. See dialog.py for where those live.
"""
import os
import stat
import subprocess


class KeyError_(Exception):
    """Raised for any key-retrieval failure; distinct name to avoid
    shadowing the Python builtin KeyError."""


def read_key_from_file(path):
    """Read an API key from a user-chosen file. Expands `~` and env vars.
    Re-reads from disk every call -- no in-memory caching -- so a key
    rotated on disk takes effect on the very next render without an addon
    restart. Warns (does not fail) if file permissions look loose."""
    if not path:
        raise KeyError_("No key file configured.")
    expanded = os.path.expanduser(os.path.expandvars(path.strip()))
    if not os.path.isfile(expanded):
        raise KeyError_("Key file not found: {}".format(expanded))

    _warn_if_permissive(expanded)

    with open(expanded, "r") as f:
        key = f.read().strip()
    if not key:
        raise KeyError_("Key file is empty: {}".format(expanded))
    return key


def read_key_from_command(command):
    """Run a user-configured shell command (e.g. a keychain CLI lookup)
    and use its stdout as the key. Re-run every call -- no caching."""
    if not command:
        raise KeyError_("No key command configured.")
    try:
        result = subprocess.run(
            command, shell=True, capture_output=True, text=True, timeout=15
        )
    except Exception as exc:  # noqa: BLE001
        raise KeyError_("Key command failed to run: {}".format(exc))
    if result.returncode != 0:
        raise KeyError_(
            "Key command exited {}: {}".format(result.returncode, result.stderr.strip())
        )
    key = result.stdout.strip()
    if not key:
        raise KeyError_("Key command produced no output.")
    return key


def resolve_key(key_file=None, key_command=None):
    """Try key_command first (if set), then key_file. Raises KeyError_
    with a helpful, user-facing message if neither is configured/works."""
    errors = []
    if key_command:
        try:
            return read_key_from_command(key_command)
        except KeyError_ as exc:
            errors.append(str(exc))
    if key_file:
        try:
            return read_key_from_file(key_file)
        except KeyError_ as exc:
            errors.append(str(exc))
    if not key_file and not key_command:
        raise KeyError_(
            "No API key configured. Set a key file or key command for this "
            "provider in the AI Render dialog's provider settings."
        )
    raise KeyError_(
        "Could not read an API key: " + "; ".join(errors)
    )


def _warn_if_permissive(path):
    """Best-effort chmod-600 check (Unix only); never raises, only used
    to surface a warning string the caller can log/show."""
    try:
        mode = stat.S_IMODE(os.stat(path).st_mode)
        if mode & (stat.S_IRWXG | stat.S_IRWXO):
            return (
                "warning: {} is readable by group/other (mode {}); "
                "consider `chmod 600 {}`".format(path, oct(mode), path)
            )
    except OSError:
        pass
    return None


def permission_warning(path):
    """Public helper mirroring _warn_if_permissive for callers (dialog)
    that want to show the warning string without triggering a read."""
    expanded = os.path.expanduser(os.path.expandvars(path.strip())) if path else None
    if not expanded or not os.path.isfile(expanded):
        return None
    return _warn_if_permissive(expanded)
