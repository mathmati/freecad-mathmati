# SPDX-License-Identifier: MIT

"""App-level (headless-safe) entry point.

Honest note, verified empirically this session (see ../../../FORMAT.md
section 4): as of FreeCAD 1.1.0, headless ``freecadcmd`` does NOT
automatically import this ``Init`` submodule -- only the bare
``freecad.StandardsLibraryWB`` namespace package (``__init__.py``) gets
imported on its own. This file is therefore *not* something you can rely
on firing by itself yet. It exists so a headless/CI/scripted caller can
explicitly opt in:

    import freecad.StandardsLibraryWB.Init

which is exactly what happens the moment this module is imported (the
sync call below is at module level, so merely importing this file runs
it -- no function call needed by the caller beyond the import itself).

The GUI path does not need this file: ``init_gui.py``'s module-level code
is confirmed to run automatically once per FreeCAD GUI startup for every
installed addon (proven via ``FreeCADGui.listWorkbenches()`` already
containing this workbench immediately after launch, before any manual
activation) -- that is the automatic path for normal desktop users.
"""

import FreeCAD

from . import sync

FreeCAD.Console.PrintLog("StandardsLibraryWB: running headless sync (explicit import)\n")
run_sync_result = sync.run_sync()
