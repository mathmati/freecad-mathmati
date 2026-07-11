# Materials data — 21 curated, cross-checked engineering material cards

This directory mirrors FreeCAD's own material-card taxonomy
(`Standard/Metal/Steel/`, `Standard/Metal/Aluminum/`, etc.). All files named `EngSTD-*.FCMat` are this
addon's deliverable: 21 `.FCMat` cards covering the common engineering
materials an engineer/maker actually reaches for (structural steels,
stainless, aluminum, titanium, copper alloys, cast/ductile iron, one
polymer, one magnesium alloy). This was originally a 28-card set; a
2026-07-10 prior-art pass against FreeCAD's live core source found 7 were
exact duplicates of core cards and removed them pre-release. See
`../../README.md`'s three-tier breakdown (net-new / equivalent /
removed) and `../../DATA_PROVENANCE.md` for the full record.

Every mechanical property in every card was cross-checked against **at
least two independent public sources** before being written — see
`../../DATA_PROVENANCE.md` for the full material × property × source ×
agreement table, including the handful of values flagged for human
review rather than silently resolved. Field names/units/model UUIDs were
copied from FreeCAD's own shipped cards (`Resources/Materials/Standard/**`
in a real FreeCAD 1.1 install) so these are drop-in compatible with
FreeCAD's own `Materials.MaterialManager`.

Every `.FCMat` file placed anywhere under this directory (any subfolder
depth) is picked up automatically by `freecad/StandardsLibraryWB/sync.py`
and copied into FreeCAD's writable User material library on next FreeCAD
start (or by calling `sync.install_materials()` directly, e.g. from the
verify harness).

See `../../DATA_PROVENANCE.md` for the sourcing, licensing, and
accuracy-gate record.
