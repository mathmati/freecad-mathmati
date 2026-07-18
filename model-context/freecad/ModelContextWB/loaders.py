# SPDX-License-Identifier: MIT
"""Load a saved FreeCAD document into a model-context dict without touching
any document the user has open.

The trick: FreeCAD keys open documents by file path, so opening a file the
user is already editing (or opening the same path twice, as a two-version
diff of one file needs) would collide. We therefore copy the file to a
temporary path first, open THAT, serialize, and close it again. Works under
both the GUI and plain freecadcmd.
"""
import os
import shutil
import tempfile

import FreeCAD as App

from . import serialize as S


def model_from_file(path):
    """Open a saved .FCStd non-invasively and return its model-context dict
    (the document label is set to the original file's basename so diffs read
    naturally). Raises IOError/OSError on unreadable paths."""
    if not os.path.isfile(path):
        raise IOError("No such file: %s" % path)
    tmpdir = tempfile.mkdtemp(prefix="modelcontext_")
    tmp = os.path.join(tmpdir, os.path.basename(path))
    doc = None
    try:
        shutil.copy2(path, tmp)
        try:
            doc = App.openDocument(tmp, hidden=True)
        except TypeError:  # FreeCAD < 0.19: no hidden kwarg
            doc = App.openDocument(tmp)
        model = S.serialize_document(doc)
        model["document"]["label"] = os.path.basename(path)
        return model
    finally:
        if doc is not None:
            try:
                App.closeDocument(doc.Name)
            except Exception:
                pass
        shutil.rmtree(tmpdir, ignore_errors=True)
