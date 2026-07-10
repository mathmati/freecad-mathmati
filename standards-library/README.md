# FreeCAD Engineering Standards Library

An Addon-Manager addon that fills FreeCAD 1.1's Material system with
**21 curated, cross-checked engineering material cards** — real, sourced
mechanical properties for the structural steels, stainless steels,
aluminum alloys, titanium, copper alloys, cast/ductile irons, one
polymer, and one magnesium alloy that engineers, FEM users, and makers
actually reach for.

Screenshot (FreeCAD 1.1.0, genuinely clean-install re-verify, 2026-07-10,
after the pre-release prior-art pass removed 7 duplicate cards — tree
shows 21/21):

![Material Editor showing the populated Standards Library, 21 cards, "17-4PH Stainless Steel (H900)" selected](../shots/m3_clean_install_material_editor.png)

## What this is

FreeCAD's own Material system ships with a good `LinearElastic` /
`MaterialStandard` data model, and — as of a 2026-07-10 prior-art pass
against FreeCAD's live core source tree — a *larger* pre-populated grade
set than this project's earlier drafts assumed (core's `Metal/Steel/`
alone ships roughly 90 files, including 7 stainless grades and several
EN-GJL/EN-GJS cast-iron grades filed under Steel; see "Prior art and
honest positioning" below for the full verified inventory). This addon
does not replace or duplicate FreeCAD's own material cards — it *extends*
the same taxonomy (`Standard/Metal/Steel`, `Standard/Metal/Aluminum`,
`Standard/Thermoplast`, etc.) with 21 additional grades, each
cross-checked against real published data before being added. 7 cards
that turned out to be exact duplicates of core cards were found and
removed pre-release (see below) rather than shipped as padding.

## Who this is for

- **FEM users** who need real yield/tensile/modulus numbers for a
  specific structural or stainless steel grade, an aluminum alloy, or a
  common 3D-printing polymer, without hand-typing values from a
  datasheet.
- **CAD/PartDesign users** who want a material assigned to a part to mean
  something (density for mass properties, etc.) beyond FreeCAD's default
  generic categories.
- **Makers/FDM users** who want Nylon 6/6 (PA66) properties alongside
  metal/alloy options (ABS and PLA are already shipped by FreeCAD core
  itself and are intentionally not duplicated here — see below).

## Prior art and honest positioning

A prior-art pass (2026-07, against `FreeCAD/FreeCAD` main and
`FreeCAD/Supplemental-Materials`) checked every one of this addon's
original 28 cards against FreeCAD 1.1's actual shipped core materials and
the official `FreeCAD/Supplemental-Materials` addon (the maintainer-run
"materials that extend core" repo, currently copper-family-only). Result:
**7 of the 28 were byte-for-byte duplicates of core cards, 6 were the same
grade family under a different national/standard designation (or a minor
correction), and 15 were genuinely new to the entire FreeCAD ecosystem**
(core or Supplemental-Materials). The 7 duplicates were removed before
this release; this addon now ships exactly the 21 cards that add real,
distinct value. This is a factual-accuracy correction made proactively,
not a response to external review.

### Tier 1 — Net-new (15): no equivalent anywhere in core or Supplemental-Materials

| Category | Material | Standard / designation |
|---|---|---|
| Steel | ASTM A36 | ASTM A36 |
| Steel | ASTM A572 Grade 50 | ASTM A572 |
| Steel | ASTM A992 | ASTM A992 |
| Steel | AISI 1018 (Cold Drawn) | AISI/SAE 1018 |
| Steel | AISI 4140 (Annealed) | AISI/SAE 4140 |
| Stainless steel | 410 (Annealed) | ASTM A276 / EN 10088 |
| Stainless steel | 17-4PH (H900) | ASTM A564 / AMS 5643 |
| Cast/ductile iron | Gray Cast Iron G3000 (Class 30) | ASTM A48 Class 30 |
| Cast/ductile iron | Ductile Iron 65-45-12 | ASTM A536 |
| Aluminum | 2024-T3 | UNS A92024 |
| Aluminum | 5052-H32 | UNS A95052 |
| Aluminum | 6063-T5 | UNS A96063 |
| Titanium | CP Titanium Grade 2 | ASTM B265 |
| Copper alloy | C36000 Free-Cutting Brass (H02) | ASTM B16 |
| **Magnesium** | **AZ31B** | **ASTM B90/B107** |

The five ASTM/AISI-designated steels fill a real gap: core only ships
EN/German/Chinese-series steel designations, so anyone searching by the
US/ASTM name they actually know finds nothing today. The two cast-iron
cards do the same for ASTM A48/A536 designations (core only has EN-GJL/
EN-GJS grades, filed under `Steel/`, not `Iron/`). **AZ31B is the
headline item: zero magnesium materials exist anywhere in FreeCAD core or
Supplemental-Materials today** — this is the first magnesium alloy
available in the FreeCAD ecosystem, core-or-supplemental, full stop.

### Tier 2 — Equivalent/corrected (6): same grade family already in core, different designation or a corrected value

| Material | Core counterpart | Why ours is still included |
|---|---|---|
| S355JR | `Steel-S355J2G3.FCMat` (numerically identical; JR vs J2G3 differ only in Charpy-impact test temperature, not strength) | Searchable under the EN 10025 "JR" designation engineers actually specify, with that provenance stated plainly |
| 6082-T6 | `AlMgSi1F31.FCMat` (numerically identical; same alloy, DIN vs EN naming) | Searchable under the EN/UNS "6082-T6" name rather than the DIN designation |
| 304 (X5CrNi18-10) | `Steel-X5CrNi18-10.FCMat` | Same grade, but this card's ShearModulus/Density were corrected by this project's own isotropic-consistency audit (`G = E/(2(1+ν))`) to a value consistent with an austenitic stainless's actual elastic constants — core's card was not; see `DATA_PROVENANCE.md` |
| 316L (X2CrNiMo17-12-2) | `Steel-X5CrNiMo17-12-2.FCMat` (that's 316, standard-carbon 1.4401, not low-carbon 1.4404/"L") | Distinct low-carbon designation engineers specifically call out for welding; core has no 1.4404 card at all |
| C11000 Copper (Annealed) | `Copper-102.FCMat` (C10200, different temper/spec) + `Copper-Generic.FCMat` | Distinct exact UNS designation and temper (OS050 annealed) from the closest core/Supplemental-Materials match |
| Nylon 6/6 (PA66) | `PA6-Generic.FCMat` (that's PA6, not PA66) | Distinct polymer chemistry (66 vs 6) with slightly different strength, near-identical elastic constants — core has no PA66 card |

### Removed pre-release (7): exact duplicates of core, not shipped

**S235JR, S275JR, 6061-T6, 7075-T6, Ti-6Al-4V (Grade 5), ABS, PLA** were
part of this project's original 28-card draft, used internally only as
cross-check anchors against known-good core values. The prior-art pass
found their mechanical properties are byte-for-byte identical to FreeCAD's
own shipped `Steel-S235JR.FCMat`, `Steel-S275JR.FCMat`,
`Aluminum-6061-T6.FCMat`, `Aluminum-7075-T6.FCMat`, `Ti-6Al-4V.FCMat`,
`ABS-Generic.FCMat`, and `PLA-Generic.FCMat` — adding them would have
created two near-identical-looking entries in the Material Editor tree for
zero new data. They were deleted before this release rather than shipped
as padding; their removal is recorded, not hidden, in
`DATA_PROVENANCE.md`.

Every remaining card exposes both FreeCAD's `LinearElastic` model
(Density, YoungsModulus, PoissonRatio, ShearModulus where independently
confirmed, YieldStrength, UltimateTensileStrength, UltimateStrain) and its
`MaterialStandard` model (KindOfMaterial, MaterialNumber, StandardCode),
so they sort, filter, and display in FreeCAD's Material Editor exactly
like any built-in card.

## Install

### Via the Addon Manager (once indexed / added as a custom repository)

`Tools → Addon manager` → search for "Engineering Standards Library"
(after this addon is indexed), or add this repository's URL under
**Addon Manager → Configure → Custom repositories** for early access
before it is indexed. Restart FreeCAD — no further action is needed, the
sync runs automatically (see "What this addon does" below).

### Manually (developer / local test install)

Copy (do not symlink, to reproduce exactly what the Addon Manager does)
this folder into your FreeCAD `Mod/` directory:

- Linux: `~/.local/share/FreeCAD/Mod/` (or `~/.local/share/FreeCAD/v1-1/Mod/`
  on some 1.1 installs)
- Windows: `%APPDATA%\FreeCAD\Mod\`
- macOS: `~/Library/Application Support/FreeCAD/Mod/`

Restart FreeCAD, then open **Material → Edit** — all 21 cards appear
under **User → EngineeringStandardsLibrary → Standard → …** in the
Material Editor's tree.

## What this addon does

On every FreeCAD GUI startup, it copies its own bundled
`Resources/Materials/**/*.FCMat` files into FreeCAD's real, writable User
material library (there is no manifest or path-registration API for
third-party material libraries as of FreeCAD 1.1.0 — copying into the
one writable "User" library directory is the only supported mechanism;
see `../FORMAT.md` for the primary-source verification of this). It also
merges its own (currently empty — see Scope below) bundled
`Resources/Profiles/profiles.csv` rows into FreeCAD's real, writable user
BIM `profiles.csv`, in a clearly delimited, idempotent managed block that
never touches anything else already in that shared file. See
`freecad/StandardsLibraryWB/sync.py` for the exact mechanism. A manual
"Re-sync standards data" command is also available under the "Standards
Library" workbench/toolbar.

## Verifying it worked (clean-install test, this session)

A fresh copy of this addon (no symlink) was installed into an empty
`Mod/` directory, FreeCAD 1.1.0 was launched under Xvfb from a clean
state (no pre-existing synced data), and:

- The Material Editor's tree showed **21/21** cards under
  `User → EngineeringStandardsLibrary`, programmatically counted via the
  tree widget's own model (not eyeballed) — re-verified after the 7
  duplicate cards were removed.
- A headless enumeration (`Materials.MaterialManager`, run once per
  material to work around a real FreeCAD 1.1.0 Materials-module crash
  found this session — see `../verify/m3_single_material_check.py`'s
  docstring) confirmed all 21 cards resolve by UUID, expose both
  `LinearElastic` and `MaterialStandard`, and have sane-range Density /
  YoungsModulus / PoissonRatio and a non-empty StandardCode.
- The Report View showed no parse errors or warnings.

See `../verify/` for the full scripted harness and `../shots/` for
screenshots.

## Data provenance and accuracy methodology

Every mechanical property in every card was cross-checked against **at
least two independent public sources** (manufacturer/mill datasheets,
ASTM/EN standard nominal values, or FreeCAD's own already-cleared shipped
cards used as one of the two sources) before being written. An
isotropic-consistency pass (`ShearModulus` vs. `E / (2·(1+ν))`, flagged if
>5% off) was additionally applied across the (then-28, now-21) cards,
correcting two values found inconsistent. Two values are flagged for
human review rather than silently resolved (a third, PLA's ultimate
tensile strength, no longer applies — the PLA card was removed pre-release
as an exact duplicate of FreeCAD's own core card; see "Removed pre-release"
above):

1. **ASTM A36 Poisson's ratio** — a genuine ~15% literature split
   (0.26 vs. 0.30); 0.30 was adopted for consistency with the rest of the
   steel family.
2. **Gray Cast Iron G3000 yield strength** (140 MPa) — an estimated
   proportional proof stress, not a directly published number (gray iron
   has no true yield point).

Full material × property × source × agreement table:
[`../DATA_PROVENANCE.md`](../DATA_PROVENANCE.md). Sourcing/licensing
landscape: [`../SOURCES.md`](../SOURCES.md). Nothing here is copied
prose or a scraped database row — every value is a re-expressed
standard/grade nominal property, cross-checked, not bulk-copied from any
single encumbered source (see `SOURCES.md` for the licensing reasoning).

## Scope (this release)

**Materials only.** The BIM/Arch structural-profile sync mechanism (HSS
sections, UK Blue Book, etc.) and thread/fastener data were proven
end-to-end at the mechanism level in an earlier milestone (see
`../FORMAT.md` §2, §3) but are **not yet populated with real data** —
`Resources/Profiles/profiles.csv` ships empty in this release. Filling
that gap, and the CAM machinability/chipload data gap noted in
`../SOURCES.md`, are future work, not silently dropped scope.

## Privacy / compliance

This addon makes **zero network connections** of any kind, has **zero**
required Python dependencies, and performs no `sys.path` manipulation.
Its only side effect is copying its own bundled data files into FreeCAD's
own writable library directories on startup (see "What this addon does"
above) — no telemetry, no external calls, nothing sent anywhere.

## License

Code: MIT (`LICENSE-Code`). Data: each `.FCMat` card carries its own
`General.License` field (currently `CC-BY-4.0` for every card added by
this addon) plus a matching `# SPDX-License-Identifier:` header comment,
per FreeCAD's Qualities-checklist guidance on consistent license
declaration. See [`../SOURCES.md`](../SOURCES.md) for per-source
licensing notes.

## Known limitations / roadmap

- Structural-profile (HSS/Blue-Book sections) and thread/fastener data
  are deferred — see Scope above.
- UI strings are not yet translation-wrapped (`FreeCAD.Qt.translate`);
  this addon's only user-facing string surface today is the one
  "Re-sync standards data" toolbar command.
- Two values are flagged for human review before being treated as
  fully authoritative for precision engineering analysis — see Data
  provenance above.

## Delivery path: also pursuing upstream contribution, not just the addon

`FreeCAD/Supplemental-Materials` is the official maintainer-run repo for
exactly this purpose ("a materials database that supplements the core
materials provided by the FreeCAD application"), already in the live
Addon Manager index, small and active, with a documented contribution
process (`Documentation/AddingMaterials.md`). The strongest Tier-1 net-new
cards here — especially **AZ31B** (fills a real, total gap) and the five
ASTM/AISI steels — are also being prepared as PRs to that repo as the
preferred, durable upstream route (landing in the official curated
channel rather than only a third-party addon). This addon remains the
convenient-install companion path: useful on its own, and not contingent
on those PRs being accepted.

## Contributing

Issues and pull requests are welcome once this repository is public (see
`../RELEASE_CHECKLIST.md` for what's still pending before that). Please
cross-check any new/changed material property against **at least two
independent sources** and record the citation, matching this project's
own practice, and disclose any AI assistance in your PR description with
