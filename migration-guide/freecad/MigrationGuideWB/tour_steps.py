# SPDX-License-Identifier: MIT

"""Step definitions for the guided "first real part" tour.

Each step pairs an instruction (what to do + WHY, in FreeCAD 1.1 terms) with
a lenient document-state check function. The tour tells whether a step is
done by inspecting the live FreeCAD document via the Python API -- never by
watching for a specific click or highlighting a specific widget. This is the
"check-after-each-step" model SPEC.md section 4 asks for (the same approach
the FPA Sketcher-tutorial addon uses), deliberately without the brittle
overlay/highlight machinery section 6.3 explicitly recommends against for
v0.1.

Checks are intentionally lenient (per the build brief): they ask "does the
right *kind* of object exist yet", not "is it exactly correct", so an
imperfect sketch or an extra feature never traps the user. Every step also
has an explicit "Skip step" escape hatch, wired in tour_panel.py.
"""


class TourStep(object):
    """One tour step: display copy + a doc-state predicate."""

    __slots__ = ("key", "title", "instruction", "why", "check")

    def __init__(self, key, title, instruction, why, check):
        self.key = key
        self.title = title
        self.instruction = instruction
        self.why = why
        self.check = check  # callable(doc_or_None) -> bool


def _objects_of_type(doc, type_id):
    """All objects of an exact TypeId in doc, or [] if there's no document."""
    if doc is None:
        return []
    return [o for o in doc.Objects if o.TypeId == type_id]


# -- individual checks, each robust to doc=None / half-built documents ------


def check_new_document(doc):
    return doc is not None


def check_body_exists(doc):
    return len(_objects_of_type(doc, "PartDesign::Body")) > 0


def check_sketch_in_body(doc):
    sketches = _objects_of_type(doc, "Sketcher::SketchObject")
    if not sketches:
        return False
    bodies = _objects_of_type(doc, "PartDesign::Body")
    if not bodies:
        # Lenient: a bare sketch still counts as progress (e.g. the Body
        # hasn't recomputed into the tree yet). Never trap the user on a
        # containment check.
        return True
    for body in bodies:
        group = list(getattr(body, "Group", []) or [])
        if any(s in group for s in sketches):
            return True
    return True


def check_profile_drawn(doc):
    sketches = _objects_of_type(doc, "Sketcher::SketchObject")
    return any(getattr(s, "GeometryCount", 0) > 0 for s in sketches)


def check_pad_exists(doc):
    pads = _objects_of_type(doc, "PartDesign::Pad")
    if not pads:
        return False
    bodies = _objects_of_type(doc, "PartDesign::Body")
    if not bodies:
        return True
    return any(getattr(b, "Tip", None) is not None for b in bodies)


def check_pocket_exists(doc):
    return len(_objects_of_type(doc, "PartDesign::Pocket")) > 0


def check_saved(doc):
    if doc is None:
        return False
    return bool(getattr(doc, "FileName", ""))


STEPS = [
    TourStep(
        key="new_document",
        title="Create a New Document",
        instruction=(
            "Click <b>File &rarr; New</b> (or the New toolbar button). A "
            "FreeCAD document holds every object in your model, the same "
            "role a Fusion 360 design or a SolidWorks part file plays."
        ),
        why=(
            "Nothing else in this tour can happen without an active "
            "document -- almost every FreeCAD command operates on "
            "<code>App.ActiveDocument</code>."
        ),
        check=check_new_document,
    ),
    TourStep(
        key="body",
        title="Switch to Part Design and Create a Body",
        instruction=(
            "Switch the workbench selector (top toolbar) to <b>Part "
            "Design</b>, then click <b>Create body</b> "
            "(<code>PartDesign_Body</code>)."
        ),
        why=(
            "In Fusion 360 / SolidWorks your part IS the container. In "
            "FreeCAD, a <b>PartDesign Body</b> is the container that holds "
            "one continuous, linear feature history -- this is the #1 "
            "migration confusion point (a Part container and a PartDesign "
            "Body are different things). Everything you build in this tour "
            "lives inside this Body."
        ),
        check=check_body_exists,
    ),
    TourStep(
        key="sketch",
        title="New Sketch on a Plane",
        instruction=(
            "With the Body active, click <b>Create sketch</b> "
            "(<code>PartDesign_NewSketch</code>) and pick the <b>XY "
            "plane</b> when prompted."
        ),
        why=(
            "PartDesign features are built from sketches -- the same idea "
            "as a Fusion sketch on a construction plane. Everything "
            "downstream (the Pad, the Pocket) traces back to a sketch."
        ),
        check=check_sketch_in_body,
    ),
    TourStep(
        key="profile",
        title="Draw a Closed Rectangle",
        instruction=(
            "In the Sketcher, draw a simple closed rectangle (the "
            "<b>Rectangle</b> tool), then close the sketch editor. Detailed "
            "constraint teaching is out of scope for this tour -- see the "
            "FPA-funded Sketcher-tutorial addon for a deep dive on "
            "constraints. This tour only needs any closed profile to pad."
        ),
        why=(
            "A Pad needs a closed profile to become a solid, the same "
            "requirement Fusion's Extrude has. One naming note: what "
            "SolidWorks calls a <b>Collinear</b> constraint is FreeCAD's "
            "<b>Tangent</b> constraint applied to two lines."
        ),
        check=check_profile_drawn,
    ),
    TourStep(
        key="pad",
        title="Pad the Sketch",
        instruction=(
            "Select the sketch and click <b>Pad</b> "
            "(<code>PartDesign_Pad</code>). Any positive length works."
        ),
        why=(
            "This is Fusion's <b>Extrude</b> (boss / add material). It's "
            "your first real solid, and it becomes the Body's <b>Tip</b> -- "
            "the feature that represents the Body's current shape."
        ),
        check=check_pad_exists,
    ),
    TourStep(
        key="pocket",
        title="Sketch on a Face and Pocket a Hole",
        instruction=(
            "Select the top face of your new solid, create another sketch "
            "on it, draw a circle, then click <b>Pocket</b> "
            "(<code>PartDesign_Pocket</code>) to cut a hole through it."
        ),
        why=(
            "This is the teachable moment for FreeCAD's <b>toponaming</b> "
            "reality: this feature now references geometry produced by an "
            "earlier feature. FreeCAD 1.0+'s new naming algorithm reduces "
            "-- but does not eliminate -- toponaming breakage, so get in "
            "the habit of sketching on faces/datum planes deliberately, the "
            "same discipline that keeps a Fusion timeline healthy."
        ),
        check=check_pocket_exists,
    ),
    TourStep(
        key="save",
        title="Save the Document",
        instruction=(
            "Click <b>File &rarr; Save</b> (or Ctrl+S) and choose a "
            "<code>.FCStd</code> location."
        ),
        why=(
            "<code>.FCStd</code> is FreeCAD's native document format -- it "
            "keeps your full parametric feature history, unlike a dumb "
            "STEP/IGES export. You now have a real, saved PartDesign part, "
            "built the same way experienced FreeCAD users build one."
        ),
        check=check_saved,
    ),
]
