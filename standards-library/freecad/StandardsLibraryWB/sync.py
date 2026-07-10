# SPDX-License-Identifier: MIT

"""Install/merge this addon's curated data into FreeCAD's real, writable
material and BIM/Arch profile libraries.

Every path and mechanism used here was verified against a real, installed
FreeCAD 1.1.0 -- see ../../../FORMAT.md for the primary-source citations
(exact file/line references into FreeCAD's own Mod/Material and Mod/BIM
source) backing each design choice below. In short:

* Materials: FreeCAD's ``Materials.MaterialManager`` only recognizes two
  local library directories, "System" (read-only, ships with FreeCAD) and
  "User" (``FreeCAD.getUserAppDataDir() + "Material"``). There is no
  registration API for a third arbitrary local library -- an addon that
  wants its cards discovered has to copy them into the User library
  directory. We nest our copies under a fixed, addon-owned subfolder name
  (``NAMESPACE``) so re-running this sync is idempotent and so our
  content is visually distinguishable/collectable in the Material Editor
  tree, and so uninstalling only ever touches our own subfolder.

* BIM/Arch structural profiles: ``ArchProfile.readPresets()`` merges
  exactly three fixed CSV files, the third being
  ``FreeCAD.getUserAppDataDir() + "BIM/profiles.csv"``. That file is a
  single flat, shared, user-writable file -- other addons or the user's
  own customizations could already have rows in it, so we never overwrite
  it wholesale. Instead we maintain one clearly delimited, idempotent
  "managed block" (bounded by MARKER_BEGIN/MARKER_END) inside that file,
  replacing only our own block on every sync and leaving every other line
  untouched.

Every function here is a plain, directly-callable Python function with no
hidden magic-import side effects -- this lets the exact same logic be
triggered from three different places: (1) ``init_gui.py``'s module level
(confirmed to run automatically once per FreeCAD GUI startup for every
installed addon), (2) ``Init.py`` for anyone who explicitly imports it in
a headless/CI context, and (3) this repo's own verify harness
(``verify/verify_roundtrip.sh``), which calls these same functions
directly against a hand-made sample instead of the addon's bundled
(currently empty, M1) data -- proving the *mechanism*, independent of how
much real data exists yet.
"""

import os
import shutil

import FreeCAD

#: Subfolder name we own inside FreeCAD's writable User material library.
#: Keeps our cards organized/collectable and makes uninstall safe (only
#: ever touches this one subfolder, never anything else already there).
NAMESPACE = "EngineeringStandardsLibrary"

#: Delimiters bounding the block of profile rows we own inside the shared,
#: single, user-writable BIM profiles.csv file. Never touch anything
#: outside this block.
MARKER_BEGIN = "# --- BEGIN FreeCAD Engineering Standards Library (managed, do not hand-edit) ---"
MARKER_END = "# --- END FreeCAD Engineering Standards Library ---"


def _addon_root():
    """Absolute path to this addon's install root (three levels up from
    this file: freecad/StandardsLibraryWB/sync.py -> freecad -> <root>)."""
    return os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def default_material_source_dir():
    """This addon's own bundled (M1: empty) material-card tree."""
    return os.path.join(_addon_root(), "Resources", "Materials")


def default_profile_source_csv():
    """This addon's own bundled (M1: zero data rows) profile CSV."""
    return os.path.join(_addon_root(), "Resources", "Profiles", "profiles.csv")


def user_material_library_dir():
    """The one writable local material-library directory FreeCAD itself
    recognizes ("User"), found the robust way: ask the real Materials
    API for it rather than hardcoding path construction, so this keeps
    working even if FreeCAD changes its directory layout in a later
    release. Falls back to the documented construction
    (``FreeCAD.getUserAppDataDir() + "Material"``) if the Materials
    Python module can't be imported (e.g. a build without the Material
    workbench) or doesn't (yet) report a "User" library.
    """
    try:
        import Materials

        mm = Materials.MaterialManager()
        for lib in mm.MaterialLibraries:
            # MaterialLibraries entries are (Name, Directory, IconBytes) tuples.
            if lib[0] == "User":
                return lib[1]
    except Exception:
        pass
    return os.path.join(FreeCAD.getUserAppDataDir(), "Material")


def user_profiles_csv_path():
    """The one writable BIM/Arch profile CSV ``ArchProfile.readPresets()``
    reads (its third, user-writable search path). No dynamic API exists
    for this one (it's a plain file path baked into ArchProfile.py, not
    exposed through any Python module) -- see FORMAT.md section 2.1 for
    the exact source lines this was confirmed against.
    """
    return os.path.join(FreeCAD.getUserAppDataDir(), "BIM", "profiles.csv")


def install_materials(source_dir=None, dest_root=None):
    """Copy every ``*.FCMat`` file under ``source_dir`` (default: this
    addon's bundled Resources/Materials) into
    ``<dest_root>/<NAMESPACE>/<same relative path>`` (default dest_root:
    FreeCAD's real User material library directory), preserving whatever
    category subfolder structure the source uses.

    Returns the number of files copied. Safe to call with an empty/absent
    source_dir (M1's shipped state) -- just creates the (empty) namespace
    folder and copies nothing.
    """
    source_dir = source_dir or default_material_source_dir()
    dest_root = dest_root or user_material_library_dir()
    dest_namespace = os.path.join(dest_root, NAMESPACE)

    os.makedirs(dest_namespace, exist_ok=True)

    count = 0
    if os.path.isdir(source_dir):
        for dirpath, _dirnames, filenames in os.walk(source_dir):
            rel = os.path.relpath(dirpath, source_dir)
            for fname in filenames:
                if not fname.lower().endswith(".fcmat"):
                    continue
                src_file = os.path.join(dirpath, fname)
                dest_dir = os.path.join(dest_namespace, rel) if rel != "." else dest_namespace
                os.makedirs(dest_dir, exist_ok=True)
                shutil.copyfile(src_file, os.path.join(dest_dir, fname))
                count += 1
    return count


def _read_source_rows(source_csv):
    """Non-comment, non-blank lines from a profiles.csv-format file."""
    rows = []
    if os.path.isfile(source_csv):
        with open(source_csv, "r", encoding="utf-8") as f:
            for line in f:
                stripped = line.strip()
                if not stripped or stripped.startswith("#"):
                    continue
                rows.append(stripped)
    return rows


def install_profiles(source_csv=None, dest_csv=None):
    """Merge every data row from ``source_csv`` (default: this addon's
    bundled Resources/Profiles/profiles.csv) into ``dest_csv`` (default:
    FreeCAD's real user BIM/profiles.csv), replacing only our own
    previously-written managed block so any other content in that shared
    file (the user's own rows, another addon's rows) is left untouched.

    Returns the number of rows written into our managed block. Safe to
    call with zero source rows (M1's shipped state) -- writes an empty
    (header-only) managed block, a harmless no-op for readPresets().
    """
    source_csv = source_csv or default_profile_source_csv()
    dest_csv = dest_csv or user_profiles_csv_path()

    rows = _read_source_rows(source_csv)

    existing_lines = []
    if os.path.isfile(dest_csv):
        with open(dest_csv, "r", encoding="utf-8") as f:
            existing_lines = f.read().splitlines()

    # Strip any previous managed block (between markers, inclusive).
    kept_lines = []
    in_block = False
    for line in existing_lines:
        if line.strip() == MARKER_BEGIN:
            in_block = True
            continue
        if line.strip() == MARKER_END:
            in_block = False
            continue
        if not in_block:
            kept_lines.append(line)

    new_block = [MARKER_BEGIN] + rows + [MARKER_END]
    final_lines = kept_lines + ([""] if kept_lines and kept_lines[-1].strip() else []) + new_block

    os.makedirs(os.path.dirname(dest_csv), exist_ok=True)
    with open(dest_csv, "w", encoding="utf-8") as f:
        f.write("\n".join(final_lines) + "\n")

    return len(rows)


def run_sync(material_source=None, profile_source=None):
    """Run both installers, never raising -- startup-time sync must never
    crash FreeCAD. Returns a summary dict; logs failures via
    FreeCAD.Console so they're visible in the Report View / console
    without blocking anything.
    """
    summary = {"materials_installed": 0, "profile_rows_installed": 0, "errors": []}
    try:
        summary["materials_installed"] = install_materials(source_dir=material_source)
    except Exception as exc:  # pragma: no cover - defensive, logged not raised
        FreeCAD.Console.PrintWarning(
            "StandardsLibraryWB: material sync failed: {}\n".format(exc)
        )
        summary["errors"].append("materials: {}".format(exc))
    try:
        summary["profile_rows_installed"] = install_profiles(source_csv=profile_source)
    except Exception as exc:  # pragma: no cover - defensive, logged not raised
        FreeCAD.Console.PrintWarning(
            "StandardsLibraryWB: profile sync failed: {}\n".format(exc)
        )
        summary["errors"].append("profiles: {}".format(exc))
    return summary
