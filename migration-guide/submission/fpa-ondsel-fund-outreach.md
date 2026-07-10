PREPARED DRAFT — awaiting user review and sign-off before any external submission.

⚠ REVIEWER CAUTION: verify the named Sketcher-tutorial grant recipients and the
Design WG Discord invite against a current primary source before sending — these
specific names/links were gathered by an AI scout and must be confirmed (or
generalized to "the FPA-funded Sketcher-tutorial team") to avoid misattribution.

---

**Where this could go, when approved:** the FreeCAD Design Working Group's
Discord (`discord.gg/w2cTKGzccC`), and/or as context attached to the Addon
Index issue, and/or a note to the FreeCAD Project Association (FPA) if a
direct channel for the Ondsel Onwards Fund / Design WG is identified. This is
deliberately written as a *coordination* note, not a funding pitch — the
addon is already built; this is about not duplicating effort and being a
good citizen of the space, not about asking for money.

---

Subject: FreeCAD Migration Guide addon — built, complements the Sketcher
tutorial grant and Start's first-run wizard, would like to coordinate

Hi — I'm mathmati, maintainer of a small FreeCAD addon
called **FreeCAD Migration Guide**
(mathmati/FreeCAD-Migration-Guide, prepared for
the Addon Index). I wanted to reach out before submitting it, both as a
courtesy and because I think it's directly relevant to work the Design
Working Group and the FPA have already funded.

**What it is:** two dockable panels for FreeCAD 1.1 aimed at people
migrating from Fusion 360 / SolidWorks — a searchable concept-map guide
(Timeline vs. tree, Part container vs. PartDesign Body, terminology
bridges, an honest note on toponaming) and a 7-step guided tour of the core
PartDesign workflow (sketch → pad → sketch-on-face → pocket → save),
validated against the live document rather than watching for clicks.

**Why I'm writing rather than just filing the Index issue:** I read through
the FirstStartWidget/Start-page source before building this, specifically to
avoid rebuilding what's already shipped — this addon does not touch
language/units/theme/navigation-style configuration, which core's First
Start screen already owns. I also know the FPA funded an interactive
Sketcher-tutorial project (Amrita Vishwa Vidyapeetham team — Dr. Chittawadigi
and 2 co-PIs — confirmed in the FPA's Dec 2024 grants announcement and 2024
annual report, USD 6,000 over 9 months for "step-by-step instructions...
highlight mistakes after each step"), but as of 2026-07 I could not find a
shipped repository, Addon Index listing, or forum announcement for it — the
9-month deliverable window closed roughly Q3 2025 with no visible public
output, and a same-titled but separately-tracked grant-archive issue
(FPA-grant-proposals#12) is confusingly labeled "declined," so the public
GitHub trail is not entirely clean. My tour's Sketcher step is deliberately
shallow regardless — draw any closed rectangle, move on — specifically so it
doesn't compete with or duplicate that project's scope whenever it does
ship, and degrades gracefully (no broken promise) if it never does. I'd
rather coordinate up front than have two efforts independently reinvent
Sketcher teaching, or than imply a live addon exists when I couldn't find
one.

A full Addon Index and FPA-grant-archive prior-art search was performed
before this note was drafted (2026-07-10,
`ops/novelty-migration-guide.md` in my build record), which is also how I
found the above status detail.

**What I'm asking:**

1. Can anyone confirm the Sketcher-tutorial project's actual current status
   (shipped somewhere I didn't find, still in progress, or genuinely
   dormant)? If/when it ships, my tour's Sketcher step could link to or
   launch it instead of drawing its own rectangle — happy to adjust scope
   either way.
2. Is there an existing convention for onboarding-adjacent addons to
   register with the Design WG before an Index submission, or is the Index
   issue itself the right first touchpoint?
3. If any of this content (the concept-map terminology bridges, the
   Part-vs-Body explainer) would be useful folded into core documentation or
   the Start page itself down the line, I'd be glad to help with that — I
   have no attachment to it staying a separate addon forever. It's licensed
   MIT specifically so it's easy to absorb.

I'm not asking for funding — the addon is already built and I intend to
submit it to the Index regardless. This note is purely about not stepping on
toes and finding out if there's a better path than "build in isolation, file
an issue, hope reviewers notice the overlap."

Thanks for reading — happy to share the repo, screenshots, or anything else
useful before or instead of the formal Index submission.

mathmati
177616452+mathmati@users.noreply.github.com / mathmati
