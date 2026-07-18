# SPDX-License-Identifier: MIT
"""Capture pipeline: color viewport image + a geometry-faithful "control"
line-art image, the two inputs AI Render hands to a provider as
img2img/ControlNet-style conditioning.

Both line-art channels were verified against a real FreeCAD 1.1.0 install
under Xvfb+llvmpipe software rendering (2026-07):

1. **GUI draw-style line-art** (`capture_drawstyle_lineart`) -- switches the
   live 3D view's Coin3D override draw style, grabs a raster screenshot,
   then restores the original style. The addon originally defaulted this
   to "Hidden Line" mode; it was then verified that "Hidden Line" (and
   "Flat Lines") silently degrade to plain Shaded under a software
   rasterizer -- zero edge lines, pixel-identical to a shaded capture.
   BUT **"Wireframe" mode was verified to work correctly** in the exact
   same environment (real white background, real black edges, same
   isometric framing as the color capture) -- see
   docs/screenshots/drawstyle_during_wireframe.png.
   So the fix was not the switch-and-restore machinery (that part was
   already correct: `setOverrideMode()` + `Gui.updateGui()`/
   `processEvents()` pump + `saveImage()`) -- it is the MODE NAME. This
   channel now defaults to "Wireframe" and is exact-camera-matched by
   construction (it *is* the live 3D view), so it is now the DEFAULT
   line-art channel.
2. **Vector line-art** (`capture_vector_lineart`) -- `TechDraw.projectToSVG`
   computes an exact geometric hidden-line projection along an arbitrary
   direction, wrapped in a synthesized `<svg viewBox=...>` and rasterized
   via Qt's QSvgRenderer. Verified empirically: `TechDraw.projectToSVG`
   wraps each group of paths in its own `transform="scale(1, -1)"` --
   the old bounding-box code parsed the RAW (pre-transform) M/L/A
   coordinates out of the fragment with a regex, so the computed viewBox
   was vertically inverted/offset relative to what Qt actually paints
   (post-transform), leaving almost the entire rendered image outside the
   viewBox -- hence the near-empty output with only a sliver of geometry
   visible. Fixed by wrapping the whole fragment in a single `<g>` and
   asking Qt's own `QSvgRenderer.boundsOnElement()` for THAT wrapper's
   bounds (NOT per-path bounds -- boundsOnElement skips parent
   transforms, so per-path queries return the same wrong pre-transform
   space; a wrapper's bounds do include its descendants' transforms) --
   so the computed bbox now matches what is actually painted regardless
   of whatever internal projection frame TechDraw used. Also fixed: the old
   code stretched the content bbox to fill width x height with NO regard
   for aspect ratio, non-uniformly distorting the drawing (circles ->
   ellipses); the bbox is now padded on its shorter axis to match the
   target aspect ratio before rasterizing, so scaling is uniform.
   This channel runs with NO GPU/OpenGL context at all (works under plain
   `freecadcmd`, no Xvfb), so it remains useful as an optional,
   headless-safe secondary channel -- but its projection direction is only
   an approximation of the live camera (see `direction` param), so it is
   no longer the default now that the GUI channel has a real, verified fix.

Depth capture is explicitly OUT of v1 scope; nothing in this module
attempts it.
"""
import os
import re

import FreeCAD as App

DRAW_STYLE_MODES = (
    "As Is",
    "Points",
    "Wireframe",
    "Hidden Line",
    "No Shading",
    "Shaded",
    "Flat Lines",
)

DEFAULT_RESTORE_MODE = "As Is"  # see module docstring / README: no public
# getter for the *current* override mode exists on View3DInventorViewerPy,
# so restoration targets FreeCAD's normal shaded default rather than a
# captured prior state. Flagged as a known limitation, not hidden.


def capture_color(view, path, width, height, background="White"):
    """Plain color viewport capture. Returns `path`.

    `view` is a Gui.View3DInventor (Gui.ActiveDocument.ActiveView).
    """
    _ensure_parent_dir(path)
    view.saveImage(path, int(width), int(height), background)
    return path


def capture_drawstyle_lineart(view, path, width, height, mode="Wireframe",
                               background="White", restore_mode=DEFAULT_RESTORE_MODE):
    """Switch-and-restore GUI draw-style capture -- the DEFAULT line-art
    control channel (see module docstring: "Hidden Line" was verified
    broken under software rendering, "Wireframe" was verified to work).
    Returns (path, restored: bool).

    Any exception during capture still attempts the restore before
    re-raising, so a failed capture never leaves the live viewport stuck
    in Hidden-Line/Wireframe mode.
    """
    _ensure_parent_dir(path)
    viewer = view.getViewer()
    restored = False
    try:
        viewer.setOverrideMode(mode)
        _pump_gui()
        view.saveImage(path, int(width), int(height), background)
    finally:
        try:
            viewer.setOverrideMode(restore_mode)
            _pump_gui()
            restored = True
        except Exception:  # noqa: BLE001 - best-effort restore
            restored = False
    return path, restored


def _pump_gui(cycles=6, delay=0.05):
    """Give Coin3D a few real repaint cycles before/after a draw-style
    switch -- a bare setOverrideMode() call with no pump can screenshot a
    stale frame (observed to matter under software rendering)."""
    try:
        import FreeCADGui as Gui
        from PySide import QtWidgets
        import time

        app = QtWidgets.QApplication.instance()
        if app is None:
            return
        for _ in range(cycles):
            Gui.updateGui()
            app.processEvents()
            time.sleep(delay)
    except Exception:  # noqa: BLE001 - never fatal, just best-effort
        pass


def visible_shape_compound(doc):
    """Build a single Part compound of every visible, shape-bearing object
    in `doc` -- the input to the vector line-art projection. Returns None
    if there is nothing visible with a Shape.
    """
    import Part
    import FreeCADGui as Gui

    shapes = []
    gdoc = Gui.getDocument(doc.Name) if hasattr(Gui, "getDocument") else None
    for obj in doc.Objects:
        shape = getattr(obj, "Shape", None)
        if shape is None or shape.isNull():
            continue
        vobj = getattr(obj, "ViewObject", None)
        if vobj is not None and not vobj.Visibility:
            continue
        # Skip children that are only shown via a visible parent (Body/
        # PartDesign features hide their intermediate solids); a simple
        # heuristic good enough for v1: include only top-level-visible,
        # non-suppressed shapes; duplicate-geometry overlap in the
        # compound does not affect projectToSVG's outline correctness.
        shapes.append(shape)
    if not shapes:
        return None
    return Part.makeCompound(shapes)


def capture_vector_lineart(doc, path, width, height, direction=None, view=None):
    """Headless-safe vector line-art capture: TechDraw.projectToSVG the
    document's visible geometry along `direction` (defaults to the active
    3D view's current camera direction, matching the color capture's
    framing), wrap it in a properly-sized <svg>, rasterize to PNG via
    FreeCAD's own Qt (PySide) QtSvg -- no GL context required, works under
    plain freecadcmd. Returns (path, edge_count).
    """
    import TechDraw

    _ensure_parent_dir(path)

    compound = visible_shape_compound(doc)
    if compound is None:
        raise ValueError("No visible shape-bearing objects in the active document")

    if direction is None:
        if view is not None:
            direction = view.getViewDirection()
        else:
            direction = App.Vector(-1, -1, -1)

    svg_fragment = TechDraw.projectToSVG(compound, App.Vector(direction))
    edge_count = svg_fragment.count("<path")

    min_x, min_y, max_x, max_y = _svg_fragment_bbox(svg_fragment)
    margin_x = max((max_x - min_x) * 0.08, 1.0)
    margin_y = max((max_y - min_y) * 0.08, 1.0)
    vb_x = min_x - margin_x
    vb_y = min_y - margin_y
    vb_w = (max_x - min_x) + 2 * margin_x
    vb_h = (max_y - min_y) + 2 * margin_y

    # Pad the shorter axis so the viewBox aspect ratio matches the target
    # width:height -- otherwise QSvgRenderer scales x/y independently to
    # fill the raster and the drawing comes out non-uniformly stretched
    # (e.g. circular holes rendered as ellipses), which would no longer
    # match the color capture's framing.
    target_aspect = float(width) / float(height) if height else 1.0
    content_aspect = (vb_w / vb_h) if vb_h else target_aspect
    if content_aspect > target_aspect:
        new_h = vb_w / target_aspect
        vb_y -= (new_h - vb_h) / 2.0
        vb_h = new_h
    elif content_aspect < target_aspect:
        new_w = vb_h * target_aspect
        vb_x -= (new_w - vb_w) / 2.0
        vb_w = new_w

    # TechDraw.projectToSVG always emits stroke-width="1.0" in raw model
    # units, regardless of how large the projected geometry is -- on a
    # small part that renders as a very heavy/bold line once scaled up to
    # fill the raster. Rescale it so the on-screen stroke is a consistent,
    # legible ~1.5px regardless of model size.
    px_per_unit = int(width) / vb_w if vb_w else 1.0
    stroke_width = max(1.5 / px_per_unit, 1e-6)
    svg_fragment = re.sub(
        r'stroke-width="[^"]*"', 'stroke-width="{:.6g}"'.format(stroke_width), svg_fragment
    )

    full_svg = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<svg xmlns="http://www.w3.org/2000/svg" '
        'viewBox="{x} {y} {w} {h}" width="{pw}" height="{ph}">\n'
        '<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="white"/>\n'
        "{frag}\n</svg>\n"
    ).format(x=vb_x, y=vb_y, w=vb_w, h=vb_h, pw=int(width), ph=int(height), frag=svg_fragment)

    svg_path = os.path.splitext(path)[0] + ".svg"
    with open(svg_path, "w") as f:
        f.write(full_svg)

    _rasterize_svg(full_svg, path, int(width), int(height))
    return path, edge_count


def _svg_fragment_bbox(svg_fragment):
    """Compute the real, POST-TRANSFORM bounding box of a
    TechDraw.projectToSVG fragment's painted content.

    BUG FIX history: the original implementation parsed the raw M/L/A
    coordinates straight out of the path `d` attributes with a regex. But
    TechDraw.projectToSVG wraps each `<g>` of paths in its own
    `transform="scale(1, -1)"`, so those raw coordinates are NOT what
    ends up on screen -- the bbox was computed in the wrong (pre-
    transform) coordinate space, causing a vertically inverted/offset
    viewBox and a near-blank rendered image. A first fix attempt queried
    `QSvgRenderer.boundsOnElement()` per `<path>` -- but Qt documents (and
    it was re-verified empirically) that boundsOnElement does NOT apply
    the transforms of PARENT elements, so per-path bounds come back in the
    same wrong pre-transform space. What parent-relative bounds DO include
    is the transforms of the queried element's own descendants: so wrap
    the ENTIRE fragment in one `<g id="airlineartroot">` whose only parent
    is the `<svg>` root, and ask for THAT element's bounds -- the interior
    `scale(1, -1)` groups are then descendants and are resolved by Qt
    itself, giving the true painted bbox with no assumptions about
    TechDraw's transform conventions.
    """
    from PySide import QtSvg

    if "<path" not in svg_fragment:
        return (-10.0, -10.0, 10.0, 10.0)

    probe_svg = (
        '<svg xmlns="http://www.w3.org/2000/svg">\n'
        '<g id="airlineartroot">\n' + svg_fragment + "\n</g>\n</svg>\n"
    )
    probe_path = None
    try:
        import tempfile

        fd, probe_path = tempfile.mkstemp(suffix=".svg")
        with os.fdopen(fd, "w") as f:
            f.write(probe_svg)
        renderer = QtSvg.QSvgRenderer(probe_path)
        if not renderer.isValid():
            return (-10.0, -10.0, 10.0, 10.0)
        rect = renderer.boundsOnElement("airlineartroot")
        if rect.isNull() or rect.isEmpty():
            return (-10.0, -10.0, 10.0, 10.0)
        return (rect.x(), rect.y(), rect.x() + rect.width(), rect.y() + rect.height())
    finally:
        if probe_path is not None:
            try:
                os.remove(probe_path)
            except OSError:
                pass


def _rasterize_svg(svg_text, out_path, width, height):
    """Render an SVG string to a PNG using FreeCAD's bundled Qt (PySide)
    QtSvg -- verified to work with no GUI/display at all (plain
    freecadcmd), so this is safe to call from headless regression tests
    as well as from inside the live GUI dialog."""
    from PySide import QtSvg, QtGui

    tmp_svg = out_path + ".tmp.svg"
    with open(tmp_svg, "w") as f:
        f.write(svg_text)
    try:
        renderer = QtSvg.QSvgRenderer(tmp_svg)
        if not renderer.isValid():
            raise ValueError("QSvgRenderer could not parse the generated SVG")
        image = QtGui.QImage(width, height, QtGui.QImage.Format_ARGB32)
        image.fill(QtGui.QColor("white"))
        painter = QtGui.QPainter(image)
        try:
            renderer.render(painter)
        finally:
            painter.end()
        if not image.save(out_path):
            raise IOError("QImage.save failed for %s" % out_path)
    finally:
        try:
            os.remove(tmp_svg)
        except OSError:
            pass


def _ensure_parent_dir(path):
    parent = os.path.dirname(os.path.abspath(path))
    if parent and not os.path.isdir(parent):
        os.makedirs(parent)
