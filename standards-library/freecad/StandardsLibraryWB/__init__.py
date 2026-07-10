# SPDX-License-Identifier: MIT

"""FreeCAD Engineering Standards Library addon package.

Installs curated, sourced structural-section profiles and material
mechanical-property cards into FreeCAD's own writable Material and
BIM/Arch profile libraries (see ../../../FORMAT.md for exactly how those
two libraries are discovered, and sync.py for the install logic itself).

This file intentionally does nothing beyond making `freecad.StandardsLibraryWB`
importable -- see FORMAT.md section 4 for why: FreeCAD's headless
`freecadcmd` imports this bare package (for its own addon bookkeeping) but
does NOT automatically import the `Init` or `init_gui` submodules, so the
real logic lives in those files, not here.
"""
