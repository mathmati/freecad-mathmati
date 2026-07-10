PREPARED DRAFT — awaiting user review and sign-off before any external submission.

⚠ REVIEWER CAUTION: this note references FreeCAD/FreeCAD GitHub issue
#16801 and the general shape of the 1.0 Materials rework as verifiable,
public facts checked this session. It does NOT name specific individuals
or claim knowledge of an internal "Materials team" roster — no such
roster was verified this session. Before sending, confirm where the
actual current materials-data discussion is happening (the FreeCAD forum's
"Material" or "Developers" subforum, or a specific GitHub Discussion) and
adjust the addressee/channel accordingly rather than guessing.

---

**Where this could go, when approved:** the FreeCAD forum's Materials- or
Developers-related subforum (`forum.freecad.org`), and/or as a comment on
FreeCAD/FreeCAD issue #16801 ("Materials/CAM: new Machinability requires
coding changes for every Tool-Material & is missing Fz(chipload) data"),
and/or attached as context to the Addon Index issue itself. This is
deliberately written as a *coordination and offer* note, not a
funding pitch or a demand — the addon is already built and will be
submitted to the Index regardless; this is about checking whether the
data itself is wanted folded into anything more central first, and being
a good citizen of the space.

---

Subject: Engineering Standards Library addon — 21 cross-checked material
cards (after removing 7 exact duplicates found in a prior-art pass), built
as an Addon-Manager addon; would some of these be useful as direct PRs to
Supplemental-Materials instead/as well?

Hi — I'm mathmati, maintainer of a small FreeCAD
addon called **FreeCAD Engineering Standards Library**
(mathmati/FreeCAD-Standards-Library,
prepared for the Addon Index). I wanted to check in before/alongside
submitting it, because I think it's directly relevant to a gap the
Materials rework left open — and because I found your
`FreeCAD/Supplemental-Materials` repo partway through building this and
want to ask about it directly rather than route around it.

**What it is:** 21 `.FCMat` material cards (structural steels, stainless
steels, aluminum alloys, titanium, copper alloys, cast/ductile iron, one
polymer, one magnesium alloy) that install into FreeCAD's own "User"
material library through the same mechanism/schema FreeCAD's own shipped
cards use — no new format, no core changes. This started as a 28-card
set; a prior-art pass I ran against your live core source tree and
`Supplemental-Materials` (2026-07-10, `ops/novelty-standards-library.md`
in my build record) found 7 were byte-for-byte duplicates of cards you
already ship (S235JR, S275JR, 6061-T6, 7075-T6, Ti-6Al-4V Grade 5, ABS,
PLA) — I deleted those 7 before this release rather than ship them as
padding. A further 6 are same-grade-family equivalents under a different
designation (e.g. S355JR vs. your S355J2G3) or a corrected value, kept
because engineers search by that name. Every mechanical property was
cross-checked against at least two independent public sources before
being added, with a citation table and two values explicitly flagged for
expert review rather than silently resolved (a genuine ASTM A36
Poisson's-ratio literature split, and an estimated proof-stress figure for
gray cast iron, which has no true yield point).

**Why I'm writing rather than just filing the Index issue:** I read
through FreeCAD/FreeCAD issue #16801 before building this, which
documents the Materials system's data (not plumbing) gap. I also found
`Supplemental-Materials` — your own maintainer-run, documented
(`AddingMaterials.md`) channel for exactly this kind of contribution,
currently covering the copper family. My addon's strongest net-new cards
(especially AZ31B — zero magnesium exists anywhere in core or
Supplemental-Materials today — and the five ASTM/AISI-designated steels)
seem like better fits as direct PRs to that repo than as a parallel
third-party addon, so I'm preparing both: PRs there as the preferred
upstream route, and this addon as a convenient-install companion that
doesn't depend on the PRs landing.

**What I'm asking:**

1. Would you want PRs against `Supplemental-Materials` for the strongest
   net-new cards (AZ31B, the ASTM/AISI steels, 410, 17-4PH, the two cast
   irons)? I'm treating that as the preferred path and this addon as the
   fallback/companion, not a replacement for it.
2. Is there an active effort (core PR, another addon, a documented plan)
   already working on expanding FreeCAD's own bundled material catalog
   beyond what I found (the copper-family work in Supplemental-Materials)
   that this would duplicate? I found no other such effort in this
   session's research, but I'd rather ask than assume.
3. Is there a preferred venue (this forum thread, a GitHub Discussion, the
   issue itself) for this kind of "here's sourced data, is it wanted"
   conversation, or is the Addon Index issue itself the right first
   touchpoint?

I'm not asking for anything beyond a sanity check — the addon is already
built, verified against a real FreeCAD 1.1.0 install (clean-install test,
21/21 cards registering with zero parse errors, re-verified after the
duplicate-removal pass), and I intend to submit it to the Index
regardless. This note is purely about not duplicating effort and finding
out if there's a better home for the strongest data than "build in
isolation, file an issue, hope reviewers notice the overlap" — which is
exactly what my own prior-art pass was trying to avoid.

Thanks for reading — happy to share the repo, the full citation table, or
anything else useful before or instead of the formal Index submission.

mathmati
177616452+mathmati@users.noreply.github.com / mathmati
