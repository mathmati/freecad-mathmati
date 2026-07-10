# SPDX-License-Identifier: MIT

"""Static content for the Migration Guide panel.

All copy lives here, separate from the Qt plumbing in migration_panel.py, so
it is easy to extend/correct without touching widget code. Terminology was
checked against a live FreeCAD 1.1.0 install (workbench names via
Gui.listWorkbenches(), command names via Gui.listCommands()) rather than
assumed -- see build/freecad-onboarding/ verification notes.
"""

# Each row: (Fusion 360 / SolidWorks term, FreeCAD equivalent, explanatory note)
CONCEPT_MAP_ROWS = [
    (
        "Timeline (linear history)",
        "Model tree + per-Body feature history",
        "There is no single global timeline. Each PartDesign Body keeps its "
        "own linear feature history (visible as a sub-list in the tree); the "
        "overall document tree is a hierarchy of containers, not one strip.",
    ),
    (
        "Component / Body",
        "Part container (Std_Part) <i>vs.</i> PartDesign Body",
        "The #1 source of confusion for new users -- see the dedicated "
        "section below.",
    ),
    (
        "Joint / Mate",
        "Assembly workbench",
        "Ex-Ondsel Assembly workbench, shipped in FreeCAD 1.0. Functional, "
        "but still young: expect rough edges on large or heavily-constrained "
        "assemblies (solver performance and joint-drag bugs are known, "
        "actively-tracked issues).",
    ),
    (
        "Extrude",
        "Pad (PartDesign) or Extrude (Part)",
        "Pad is the PartDesign-workbench equivalent (adds solid material to "
        "a Body from a sketch, part of a feature history). Part workbench's "
        "Extrude is the non-parametric-history cousin, closer to a one-off "
        "boolean operation.",
    ),
    (
        "Collinear constraint",
        "Tangent constraint (applied to two lines)",
        "FreeCAD's Sketcher has no separate “Collinear” constraint. "
        "Applying Tangent to two straight line segments forces them onto the "
        "same infinite line -- same effect, different name. (Coincident, for "
        "matching two points, is named the same in both systems.)",
    ),
    (
        "Single unified environment",
        "Workbench switching",
        "FreeCAD splits functionality into workbenches (Part, PartDesign, "
        "Sketcher, Assembly, Draft, ...) that you switch between per task, "
        "rather than one toolset that shows everything at once. See the "
        "quick-reference below.",
    ),
    (
        "Robust feature references",
        "Toponaming (the honest reality)",
        "FreeCAD 1.0 shipped a new, more stable naming algorithm that "
        "significantly reduces broken references when earlier features "
        "change -- but it does not eliminate the problem. Regressions are "
        "still reported. Build the habit of sketching on datum planes / "
        "local coordinate systems rather than raw model faces where "
        "possible; it is cheap insurance.",
    ),
    (
        ".f3d / .sldprt reopen",
        "No native import -- use STEP",
        "FreeCAD cannot read Fusion 360 (.f3d) or SolidWorks (.sldprt) files "
        "directly. Export STEP (.stp/.step) or IGES from the source app and "
        "import that. You get a dumb solid (BREP geometry) with no "
        "parametric feature history -- plan to rebuild history-dependent "
        "edits in FreeCAD from that point forward.",
    ),
]

WORKBENCH_QUICKREF = [
    ("Sketching 2D profiles", "Sketcher"),
    ("Solid, single-body parametric parts", "Part Design"),
    ("Quick booleans, primitives, non-parametric solids", "Part"),
    ("Multi-part assemblies, joints/mates", "Assembly"),
    ("2D drafting, annotation-style geometry", "Draft"),
    ("Engineering drawings / sheets", "TechDraw"),
    ("Simulation / FEA setup", "FEM"),
    ("CNC toolpaths", "CAM"),
    ("Architecture / building elements", "BIM"),
]

LINKS_OUT = [
    (
        "FreeCAD wiki: Migrating to FreeCAD from Fusion 360",
        "https://wiki.freecad.org/Migrating_to_FreeCAD_from_Fusion360",
    ),
    (
        "Brodie Fairhall -- “Fusion 360 to FreeCAD” video series",
        "https://www.youtube.com/results?search_query=brodie+fairhall+fusion+360+to+freecad",
    ),
    (
        "CAD Rosetta Stone (community wiki, work in progress)",
        "https://wiki.freecad.org/CAD_Rosetta_Stone",
    ),
    (
        "Miss your ribbon toolbar? FreeCAD-Ribbon (install via Addon Manager)",
        "https://github.com/APEbbers/FreeCAD-Ribbon",
    ),
]

_STYLE = """
<style>
  body { font-family: -apple-system, "Segoe UI", sans-serif; font-size: 13px; }
  h2 { color: #2b6cb0; border-bottom: 1px solid #cbd5e0; padding-bottom: 3px;
       margin-top: 18px; margin-bottom: 6px; }
  h3 { color: #2c5282; margin-top: 14px; margin-bottom: 4px; }
  p { line-height: 1.45; margin: 4px 0 10px 0; }
  table { border-collapse: collapse; width: 100%; margin: 6px 0 14px 0; }
  th { background-color: #2b6cb0; color: #ffffff; text-align: left;
       padding: 5px 8px; font-size: 12px; }
  td { border-bottom: 1px solid #e2e8f0; padding: 5px 8px; vertical-align: top;
       font-size: 12px; }
  tr:nth-child(even) td { background-color: #f7fafc; }
  .note { color: #4a5568; }
  .pill { background-color: #ebf8ff; color: #2b6cb0; border-radius: 4px;
          padding: 1px 6px; font-size: 11px; }
  .toc a, .links a { text-decoration: none; color: #2b6cb0; }
  .toc li, .links li { margin-bottom: 3px; }
  .callout { background-color: #fffaf0; border-left: 4px solid #dd6b20;
             padding: 8px 10px; margin: 8px 0 14px 0; }
</style>
"""


def _concept_table_html(filter_text):
    filter_text = (filter_text or "").strip().lower()
    rows_html = []
    for source, freecad, note in CONCEPT_MAP_ROWS:
        haystack = (source + freecad + note).lower()
        if filter_text and filter_text not in haystack:
            continue
        rows_html.append(
            "<tr><td><b>{0}</b></td><td>{1}</td><td class='note'>{2}</td></tr>".format(
                source, freecad, note
            )
        )
    if not rows_html:
        return "<p class='note'><i>No concept-map rows match “{0}”.</i></p>".format(
            filter_text
        )
    return (
        "<table><tr><th>Fusion 360 / SolidWorks</th><th>FreeCAD</th>"
        "<th>What to know</th></tr>" + "".join(rows_html) + "</table>"
    )


def _quickref_html():
    rows = "".join(
        "<tr><td>{0}</td><td>{1}</td></tr>".format(task, wb)
        for task, wb in WORKBENCH_QUICKREF
    )
    return (
        "<table><tr><th>If you want to&#8230;</th><th>Switch to workbench</th></tr>"
        + rows
        + "</table>"
    )


def _links_html():
    items = "".join(
        '<li><a href="{0}">{1}</a></li>'.format(url, label) for label, url in LINKS_OUT
    )
    return "<ul class='links'>" + items + "</ul>"


def build_html(filter_text=""):
    """Return the full HTML document rendered into the QTextBrowser.

    filter_text, if non-empty, narrows the concept-map table only (search
    box behaviour); the rest of the guide always renders in full so the
    surrounding explanations stay readable.
    """
    concept_table = _concept_table_html(filter_text)
    quickref = _quickref_html()
    links = _links_html()

    return """<html><head>{style}</head><body>
<h2 id="top">Migration Guide -- Fusion 360 / SolidWorks &#8594; FreeCAD</h2>
<p>You already know CAD. This page is a translation layer, not a tutorial:
it maps what you already know onto FreeCAD's terms so the model stops
feeling arbitrary. Use the search box above to filter the concept table.</p>

<div class="toc">
<b>On this page:</b>
<ul>
  <li><a href="#partvsbody">Part container vs. PartDesign Body (read this first)</a></li>
  <li><a href="#conceptmap">Concept map</a></li>
  <li><a href="#workbenches">Why workbenches? (quick reference)</a></li>
  <li><a href="#toponaming">The toponaming reality</a></li>
  <li><a href="#importing">Importing files from Fusion 360 / SolidWorks</a></li>
  <li><a href="#links">Keep learning</a></li>
</ul>
</div>

<h3 id="partvsbody">Part container vs. PartDesign Body <span class="pill">the crucial distinction</span></h3>
<p>This is the single most common point of confusion for people arriving
from Fusion 360 or SolidWorks, because both of those tools blur the idea
that FreeCAD splits cleanly in two:</p>
<div class="callout">
<b>PartDesign Body</b> (<code>PartDesign::Body</code>) is a single continuous
feature history that produces <b>one final solid</b> (its "Tip"). This is
the closest match to a Fusion 360 "Component" that contains exactly one
timeline of solid-modeling features -- Sketch, Pad, Pocket, Fillet, all
chained together.<br><br>
<b>Part container</b> (<code>App::Part</code>, the <i>Std_Part</i> command)
is a plain grouping folder: it holds other objects -- one or more Bodies,
sketches, even other Parts -- and gives them a shared placement/origin.
It has no feature history of its own. This is closer to a Fusion
"assembly" or a SolidWorks assembly-level grouping of components.</div>
<p><b>Rule of thumb:</b> one solid part with a modeling history &#8594; a
PartDesign <i>Body</i>. A product made of several such parts positioned
together &#8594; wrap those Bodies in a <i>Part</i> container (or hand them
to the Assembly workbench once you need real joints).</p>

<h3 id="conceptmap">Concept map</h3>
{concept_table}

<h3 id="workbenches">Why workbenches? <span class="pill">quick reference</span></h3>
<p>Fusion 360 and SolidWorks show most tools in one ribbon/toolbar at all
times. FreeCAD instead groups tools into <i>workbenches</i> -- switch to the
one that matches your current task via the workbench selector in the
toolbar. It looks like extra friction at first; in practice it keeps each
toolbar small and focused. Quick reference:</p>
{quickref}

<h3 id="toponaming">The toponaming reality</h3>
<p>In parametric CAD, every feature needs to refer back to specific edges/
faces/vertices of earlier features. FreeCAD historically named those
sub-elements in a fragile way (e.g. "Face3") that could silently point at
the wrong geometry after an earlier feature changed -- this is
"toponaming" breakage, and it is the most-cited FreeCAD pain point online.
<b>FreeCAD 1.0 shipped a new, much more stable reference algorithm that
significantly reduces this</b>, but it does not claim to eliminate it
entirely; regressions are still occasionally reported upstream. Practical
habit: sketch on dedicated datum planes / local coordinate systems instead
of directly on faces of prior features where you can -- it costs one extra
click and meaningfully reduces how often a downstream feature breaks.</p>

<h3 id="importing">Importing files from Fusion 360 / SolidWorks</h3>
<p>FreeCAD cannot open <code>.f3d</code> or <code>.sldprt</code> files
directly -- there is no native reader for either format. The supported
path is a neutral interchange format:</p>
<ol>
  <li>In Fusion 360 or SolidWorks, export the part/assembly as
  <b>STEP</b> (<code>.stp</code>/<code>.step</code>) -- IGES also works but
  STEP is the better-supported, more modern choice.</li>
  <li>In FreeCAD, use <b>File &#8594; Import&#8230;</b> and pick the STEP
  file.</li>
  <li>You get a "dumb solid": accurate BREP geometry, but <b>no
  parametric feature history</b> comes across. Treat it as a starting
  shape -- use PartDesign's <i>Sub-shape Binder</i> if you need to build new
  parametric features that reference the imported geometry.</li>
</ol>

<h3 id="links">Keep learning</h3>
<p>This guide is a router, not the whole story -- these are actively
maintained, more detailed resources:</p>
{links}

</body></html>""".format(
        style=_STYLE, concept_table=concept_table, quickref=quickref, links=links
    )
