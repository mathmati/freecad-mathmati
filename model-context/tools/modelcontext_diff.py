# SPDX-License-Identifier: MIT
"""Command-line FreeCAD model diff: what changed between two .FCStd files,
semantically (features added/removed, parameters changed, constraints
edited), rendered as git-style text.

Run under FreeCAD's own interpreter:

    MC_DIFF_OLD=old.FCStd MC_DIFF_NEW=new.FCStd freecadcmd modelcontext_diff.py

or with positional arguments:

    freecadcmd modelcontext_diff.py old.FCStd new.FCStd

Git integration, so `git diff` shows semantic changes for model files:

    git config diff.fcstd.command "freecadcmd /path/to/modelcontext_diff.py"
    echo "*.FCStd diff=fcstd" >> .gitattributes

Git invokes the driver as: <cmd> <path> <old-file> <old-hex> <old-mode>
<new-file> <new-hex> <new-mode>. The script detects that shape (last 7
arguments), handles /dev/null for added/deleted files, and ALWAYS exits 0
in git-driver mode (git treats a nonzero driver exit as fatal). Outside
git-driver mode the exit code is a contract for scripts: 0 = no semantic
changes, 1 = differences found, 2 = error.
"""
import functools
import os
import sys

print = functools.partial(print, flush=True)

_NULL_PATHS = ("/dev/null", "nul", "NUL")


def _find_addon_root():
    here = os.path.dirname(os.path.abspath(__file__))
    return os.path.dirname(here)  # tools/ -> addon root


def _pick_paths():
    """Returns (old_path, new_path, git_mode)."""
    old = os.environ.get("MC_DIFF_OLD")
    new = os.environ.get("MC_DIFF_NEW")
    if old and new:
        return old, new, False
    tail = sys.argv[1:]
    # git external-diff shape: ... path old-file old-hex old-mode new-file
    # new-hex new-mode  (freecadcmd keeps the script path in argv, so take
    # the LAST seven arguments regardless of what precedes them)
    if len(tail) >= 7:
        t = tail[-7:]
        return t[1], t[4], True
    cand = [a for a in tail if a.lower().endswith((".fcstd", ".fcstd1"))]
    if len(cand) >= 2:
        return cand[0], cand[1], False
    return None, None, False


def _load(loaders, path, side_label):
    """Load a model, treating git's /dev/null (added/deleted file) as an
    empty document."""
    if path in _NULL_PATHS or os.path.basename(path or "") in _NULL_PATHS:
        return {"schema": "freecad-model-context", "schema_version": "1.0",
                "document": {"name": side_label, "label": side_label},
                "objects": []}
    return loaders.model_from_file(path)


def main():
    old_path, new_path, git_mode = _pick_paths()
    if not old_path or not new_path:
        print("usage: MC_DIFF_OLD=a.FCStd MC_DIFF_NEW=b.FCStd freecadcmd "
              "modelcontext_diff.py   (or pass two .FCStd paths as arguments)")
        return 2

    sys.path.insert(0, os.path.join(_find_addon_root(), "freecad"))
    try:
        from ModelContextWB import diff as D
        from ModelContextWB import loaders
    except ImportError:
        # installed as an addon: the normal namespaced import works instead
        from freecad.ModelContextWB import diff as D
        from freecad.ModelContextWB import loaders

    old_model = _load(loaders, old_path, "(absent)")
    new_model = _load(loaders, new_path, "(absent)")

    d = D.diff_models(old_model, new_model)
    print("Model diff: %s -> %s" % (old_model["document"]["label"],
                                    new_model["document"]["label"]))
    sys.stdout.write(D.diff_to_text(d))
    if git_mode:
        return 0  # git treats nonzero driver exit as fatal
    return 0 if D.is_empty(d) else 1


# NB: freecadcmd does not execute scripts with __name__ == "__main__", so
# run unconditionally. os._exit propagates the exit code without tripping
# over freecadcmd's SystemExit handling; the tool is read-only so skipping
# FreeCAD's teardown is safe. ANY uncaught error must exit 2, never 0 --
# a crash that reads as "no changes" is the worst failure mode a diff tool
# can have.
try:
    rc = main()
except Exception as exc:  # noqa: BLE001
    print("modelcontext_diff: error: %s" % exc)
    rc = 2
sys.stdout.flush()
os._exit(rc)
