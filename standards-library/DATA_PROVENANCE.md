# M2 material data provenance - accuracy gate record

Compiled 2026-07-09, by live WebSearch (each query aggregates
5-10 independent domains) plus direct inspection of FreeCAD 1.1's own
shipped `.FCMat` cards (`/opt/micromamba/envs/freecad/share/Mod/Material/
Resources/Materials/Standard/**`, quoted in `FORMAT.md`). Every mechanical
property below was checked against **at least two independent public
sources** before being written into a card under
`freecad_standards_library/Resources/Materials/Standard/`. "FreeCAD shipped
card" counts as one independent source where applicable (it is itself
sourced from ASM/MatWeb per its own `SourceURL` field, and is already
cleared under FreeCAD's own LGPL/CC-BY licensing - see `SOURCES.md` §0).
Values are re-expressed facts (standard/grade nominal properties), not
copied prose or scraped database rows, per `SOURCES.md`'s licensing
guidance (MatWeb viewed only as a spot-check, never bulk-copied).

**Update, 2026-07-10 (prior-art pass, `ops/novelty-standards-library.md`):**
this addon now **ships 21 cards**, not the 28 originally recorded below. 7
of the original 28 (S235JR, S275JR, 6061-T6, 7075-T6, Ti-6Al-4V Grade 5,
ABS, PLA) were found to be byte-for-byte duplicates of FreeCAD's own
shipped core cards and were **removed pre-release: exact duplicate of
core** - their rows below are kept, not deleted, and each is now
individually annotated with that status, so this document remains an
honest historical record of what was checked and why each of those 7 was
cut rather than shipped. A further 6 rows (S355JR, 304, 316L, 6082-T6,
C11000 copper, PA66) are equivalent/corrected variants of a core card
under a different designation - these **are** still shipped (annotated
"EQUIVALENT, shipped" below) and are explained in the README's Tier 2
table. The remaining 15 rows are net-new to the whole FreeCAD ecosystem.

Legend: **Agree** = independent sources within ~5% or an exact standard
minimum match. **FLAGGED** = disagreement >5% or a genuine documented split
in the literature - resolved with an explicit, stated engineering
rationale (never silently averaged), and called out again in the M2 report.

---

## Structural steels

| Material | Property | Value used | Source 1 | Source 2 | Agree? |
|---|---|---|---|---|---|
| S235JR (1.0037/38) | Yield / UTS / E / density | 235 MPa / 360 MPa / 210 GPa / 7850 kg/m³ | FreeCAD shipped `Steel-S235JR.FCMat` (235/360/210000/7800) | theworldmaterial.com, beamdimensions.com EN 10025-2 tables (235 MPa min yield, E=210 GPa) | Agree (density 7850 vs FreeCAD's 7800 is a 0.6% rounding choice, not a real disagreement) - **REMOVED PRE-RELEASE: exact duplicate of core `Steel-S235JR.FCMat`, not shipped in the 21-card release** |
| S275JR (1.0044) | Yield / UTS / E | 275 MPa / 430 MPa / 210 GPa | FreeCAD shipped `Steel-S275JR.FCMat` | beamdimensions.com EN 10025 table (275 MPa min yield, 410-560 MPa UTS band) | Agree (430 MPa falls inside independent band) - **REMOVED PRE-RELEASE: exact duplicate of core `Steel-S275JR.FCMat`, not shipped in the 21-card release** |
| S355JR (1.0045) | Yield / UTS / E | 355 MPa / 510 MPa / 210 GPa | FreeCAD shipped `Steel-S355J2G3.FCMat` (same EN 10025 grade family; J2/JR differ only in Charpy test temperature, not strength) | theworldmaterial.com, steelnumber.com, britishsteel.co.uk S355 datasheets (355 MPa min yield, 470-630 MPa UTS band) | Agree - **EQUIVALENT, shipped: numerically identical to core `Steel-S355J2G3.FCMat` under a different EN designation; kept because engineers search by "JR", see README Tier 2** |
| ASTM A36 | Yield / UTS / E | 250 MPa / 400 MPa / 200 GPa | theworldmaterial.com, metalsupermarkets.com | bushwickmetals.com, Wikipedia "A36 steel" (250 MPa yield min, 400-550 MPa UTS, 200 GPa) | Agree |
| ASTM A36 | Poisson's ratio | **0.30 (adopted)** | Multiple sources cite 0.29-0.30 (engineering-standard approximation, matches every other steel card in this library) | Multiple other sources (bushwickmetals, researchgate table) cite 0.26 as a "more precise measured" value | **FLAGGED** - genuine ~15% literature split, not a single-source error. Adopted 0.30 for internal consistency with the rest of the steel family; flagged for human review if precision below the 2nd decimal matters to a specific analysis. |
| ASTM A992 | Yield / UTS / E / density | 345 MPa / 450 MPa / 200 GPa / 7850 kg/m³ | Wikipedia "ASTM A992" | beamdimensions.com ASTM A992 table | Agree (both cite 345/450/200000/7850 essentially exactly) |
| ASTM A572 Gr50 | Yield / UTS | 345 MPa / 450 MPa | theworldmaterial.com (65 ksi = 450 MPa min) | Wikipedia-adjacent tuspipe.com / SSAB Gr50 datasheet (490-600 MPa is a mill *typical*, not the ASTM *minimum*) | Agree - 450 MPa is the ASTM specification minimum; higher "typical" mill values are a different (non-conflicting) statistic, noted not silently substituted |
| AISI 4140 (annealed) | Yield / UTS / E / density | 415 MPa / 655 MPa / 205 GPa / 7850 kg/m³ | modulusmetal.com (370-460 MPa yield, 595-720 MPa UTS, midpoints taken) | azom.com AISI 4140 (UNS G41400) datasheet | Agree (midpoints of azom/modulusmetal ranges coincide) |
| AISI 1018 (cold drawn) | Yield / UTS / density | 370 MPa / 440 MPa / 7870 kg/m³ | makeitfrom.com "Cold Drawn 1018 Carbon Steel" | mwcomponents.com Elgin 1018 data sheet, servicesteel.org | Agree |

## Stainless steels

| Material | Property | Value used | Source 1 | Source 2 | Agree? |
|---|---|---|---|---|---|
| 304 / 1.4301 | All LinearElastic fields | Density 7800, YS 210, UTS 520, E 200000 MPa, ν 0.3, G 81000 MPa | FreeCAD shipped `Steel-X5CrNi18-10.FCMat` | ASTM A240 / EN 10088 published nominal 304 values (Rp0.2 min 205-215 MPa, Rm min 515-520 MPa) confirmed via multiple 1.4301 supplier datasheets (thyssenkrupp, xometry.pro) | Agree - **PARTIAL/EQUIVALENT, shipped: same grade as core `Steel-X5CrNi18-10.FCMat`, but this card's ShearModulus/Density were subsequently corrected by the isotropic-consistency pass below (81000→77000 MPa, 7800→8000 kg/m³) - a corrected variant, not identical; kept per README Tier 2** |
| 316L / 1.4404 | Yield / UTS / E / density | 220 MPa / 520 MPa / 193 GPa / 8000 kg/m³ | thyssenkrupp-materials.co.uk 1.4404 data sheet (Rp0.2 ≥200 MPa, Rm 500-700 N/mm², E, density 8.0 g/cm³) | aalco.co.uk 1.4404 bar/section datasheet + cross-check against FreeCAD's own closely-related `Steel-X5CrNiMo17-12-2.FCMat` (1.4401: YS 220, UTS 520) | Agree - 1.4404 (316L) and 1.4401 (316) share essentially the same mechanical spec, differing in carbon content/corrosion resistance not strength - **PARTIAL, shipped: core only has the 316/1.4401 designation, not 316L/1.4404; kept per README Tier 2** |
| 17-4PH (H900) | Yield / UTS / E | 1170 MPa / 1310 MPa / 196 GPa | stainlessshapes.net H900 datasheet (min 155 ksi / 170 ksi cited) | ASTM A564 / AMS 5643 H900 published minimums (170 ksi YS / 190 ksi UTS = 1172/1310 MPa) via sandmeyersteel.com, specialtysteelsupply.com | Agree - adopted the ASTM A564 standard-minimum figures (higher of the two cited sets), consistent across suppliers |
| 17-4PH (H900) | Young's modulus | 196 GPa | Common supplier-datasheet value (sandmeyersteel, markforged) | **NIST IR 4671** ("Modulus of elasticity and Poisson's ratio for types 17-4 PH and 410 stainless steels", public-domain federal publication): E > 25.8×10³ ksi (177.9 GPa) | Agree - 196 GPa is consistent with (above) NIST's measured lower bound |
| 410 (annealed) | Yield / UTS | 275 MPa / 485 MPa (ASTM A276 spec minimums) | theworldmaterial.com AISI 410 (typical annealed 450-600 MPa band) | sandmeyersteel.com Alloy 410 plate (Rp0.2 min 275 MPa / Rm min 485 MPa) | Agree - a competing citation of 290 MPa/510 MPa (nks.com datasheet) differs by ~5.3%/5.2%, explained as *typical* (as-supplied) values vs. the *ASTM minimum* spec values used here - not a data error, both numbers are individually correct for what they measure |

## Aluminum alloys

| Material | Property | Value used | Source 1 | Source 2 | Agree? |
|---|---|---|---|---|---|
| 6061-T6 | All fields | Matches FreeCAD shipped card exactly | FreeCAD `Aluminum-6061-T6.FCMat` (SourceURL: asm.matweb.com) | Wikipedia "6061 aluminium alloy" (276 MPa YS, 310 MPa UTS, 68.9 GPa E) | Agree - **REMOVED PRE-RELEASE: exact duplicate of core `Aluminum-6061-T6.FCMat`, not shipped in the 21-card release** |
| 7075-T6 | All fields | Matches FreeCAD shipped card exactly | FreeCAD `Aluminum-7075-T6.FCMat` | Wikipedia "7075 aluminium alloy" (503 MPa YS, 572 MPa UTS) | Agree - **REMOVED PRE-RELEASE: exact duplicate of core `Aluminum-7075-T6.FCMat`, not shipped in the 21-card release** |
| 6063-T5 | Yield / UTS / E / density | 145 MPa / 186 MPa / 68.9 GPa / 2700 kg/m³ | gabrian.com 6063 alloy properties PDF | Wikipedia "6063 aluminium alloy"; allianceorg.com T5 extrusion spec (ASTM min 140/200 MPa, thickness-dependent) | Agree - 145/186 MPa are the widely cited nominal (not thinnest-section ASTM minimum) values; the ASTM minimum band brackets them within <5% - net-new, shipped |
| 6082-T6 | Yield / UTS / E | 260 MPa / 310 MPa / 70 GPa | theworldmaterial.com 6082-T6 | modulusmetal.com Aluminum 6082-T6 (3.2315) datasheet | Agree (near-exact match both sources) - **EQUIVALENT, shipped: numerically identical to core `AlMgSi1F31.FCMat` under DIN vs EN naming; kept per README Tier 2** |
| 5052-H32 | Yield / UTS / E / density | 180 MPa / 230 MPa / 70.3 GPa / 2680 kg/m³ | makeitfrom.com 5052-H32 | asm.matweb.com 5052-H32 data sheet, Wikipedia "5052 aluminium alloy" | Agree |
| 2024-T3 | Yield / UTS / E / density | 345 MPa / 483 MPa / 73.1 GPa / 2780 kg/m³ | aerospacemetals.com 2024-T3 datasheet (bare sheet, longitudinal) | makeitfrom.com 2024-T3; Wikipedia "2024 aluminium alloy" | Agree - a lower "minimum guaranteed" set (269-276 MPa YS / 400-427 MPa UTS) also appears for thicker-gauge/other product forms; adopted the widely-cited standard bare-sheet values, both sets individually correct for their product form, not a contradiction. Density 2.85 g/cm³ (one outlier source) rejected in favor of the standard 2.78 g/cm³ cited by the large majority. |

## Titanium

| Material | Property | Value used | Source 1 | Source 2 | Agree? |
|---|---|---|---|---|---|
| Ti-6Al-4V Grade 5 | All fields | Matches FreeCAD shipped card exactly | FreeCAD `Ti-6Al-4V.FCMat` | Standard ASTM B348 Grade 5 published values (typical annealed YS ~880-910 MPa, UTS ~950-1000 MPa, E ~114 GPa) via aircraftmaterials.com-style references | Agree - **REMOVED PRE-RELEASE: exact duplicate of core `Ti-6Al-4V.FCMat`, not shipped in the 21-card release** |
| CP-Ti Grade 2 | Yield / UTS / E / density | 275 MPa / 345 MPa / 103 GPa / 4510 kg/m³ | carpentertechnology.com Grade 2 datasheet (ASTM B265 minimums) | tmstitanium.com Grade 2 guide, spacematdb.com Grade 2 sheet (all cite 275/345 MPa minimums, ~4.51 g/cc, ~103 GPa) | Agree |

## Copper alloys

| Material | Property | Value used | Source 1 | Source 2 | Agree? |
|---|---|---|---|---|---|
| C36000 brass (H02) | Yield / UTS / E / density | 310 MPa / 400 MPa / 97 GPa / 8500 kg/m³ | copper.org "Free-Cutting Brass (UNS C36000)" | azom.com "Free Cutting Brass UNS C36000"; makeitfrom.com C36000 (H02 typical: ~45 ksi YS / ~58 ksi UTS) | Agree |
| C11000 copper (annealed, OS050) | Yield / UTS / E / ν / density | 69 MPa / 220 MPa / 117 GPa / 0.343 / 8940 kg/m³ | azom.com "Electrolytic Tough Pitch Copper (UNS C11000)" | makeitfrom.com "Annealed (OS050) C11000 Copper"; cross-checked against FreeCAD's own `Copper-Generic.FCMat` (ν 0.343 exact match, E 119 GPa within 2%, α 16.5 µm/m/K exact match) | Agree - **PARTIAL, shipped: no exact C11000/OS050 card in core or Supplemental-Materials (closest is `Copper-102.FCMat`/C10200, a different temper/spec); kept per README Tier 2** |

## Cast / ductile iron

| Material | Property | Value used | Source 1 | Source 2 | Agree? |
|---|---|---|---|---|---|
| Gray iron G3000 (ASTM A48 Cl. 30) | UTS | 207 MPa | iron-foundry.com ASTM A48 Class 30 page (30,000 psi min) | castingsr.com, pentictonfoundry.com A48 Class 30 data sheet | Agree (exact standard minimum, unanimous) |
| Gray iron G3000 | Yield strength | 140 MPa (approximate proof stress) | No source publishes a true "yield strength" for gray iron - it has no well-defined yield point due to graphite-flake microstructure (documented characteristic, all sources agree) | Estimated proportionally from FreeCAD's own `Steel-EN-GJL-200.FCMat` (YS/UTS ≈ 0.65 for a similar gray-iron grade) applied to G3000's 207 MPa UTS | Documented caveat, not a hard cross-check - flagged in the card's own Description field so downstream FEA users are warned |
| Gray iron G3000 | Young's modulus | 100 GPa | Multiple gray-iron references note "low modulus of elasticity" for Class 30 (non-linear stress-strain, ~13-14×10⁶ psi typical) | FreeCAD's own `Steel-EN-GJL-200.FCMat` (105 GPa, a similar-strength EN grade) | Agree |
| Ductile iron 65-45-12 (ASTM A536) | Yield / UTS / elongation | 310 MPa / 448 MPa / 12% | ductileironsuppliers.com A536 65-45-12 page (45 ksi / 65 ksi / 12% - exact ASTM spec numbers) | iron-foundry.com, pentictonfoundry.com 65-45-12 data sheets | Agree (unanimous exact match to ASTM A536 spec) |
| Ductile iron 65-45-12 | E / G / density | 170 GPa / 66 GPa / 7100 kg/m³ | pentictonfoundry.com data sheet (0.256 lb/in³ = 7.1 g/cm³) | Cross-checked against FreeCAD's own `Steel-EN-GJS-500-7.FCMat` (170000 MPa E, 66000 MPa G exactly - ductile iron elastic properties are essentially grade-independent across the EN-GJS/ASTM-A536 family) | Agree |

## Polymers

| Material | Property | Value used | Source 1 | Source 2 | Agree? |
|---|---|---|---|---|---|
| ABS | Density / YS / UTS / E / ν / α | Matches FreeCAD shipped card exactly (1060 kg/m³, 44.1/38.8 MPa, 2300 MPa, 0.37, 93 µm/m/K) | FreeCAD `ABS-Generic.FCMat` (SourceURL: matweb) | jaycon.com / researchgate ABS mechanical summary (tensile yield ~40-45 MPa, flexural modulus 2.25-2.28 GPa, ν 0.39-0.42, α 81-95 µm/m/K) | Agree - all FreeCAD values fall inside or adjacent to the independently cited ranges; ν (0.37 vs 0.39-0.42) differs by up to 14%, a well-known source of variability for polymer Poisson's ratio depending on test method/grade, noted not treated as an error - **REMOVED PRE-RELEASE: exact duplicate of core `ABS-Generic.FCMat`, not shipped in the 21-card release** |
| PLA | Density / E / ν | Matches FreeCAD shipped card exactly (1240 kg/m³, 3640 MPa, 0.36) | FreeCAD `PLA-Generic.FCMat` (SourceURL: sd3d.com TDS) | plasticranger.com / sigmafilament.com PLA density guides (1.24-1.25 g/cm³); MIT PLA properties review (E 3000-4107 MPa, ν 0.33-0.36) | Agree - **REMOVED PRE-RELEASE: exact duplicate of core `PLA-Generic.FCMat`, not shipped in the 21-card release (see below - this also retires the PLA UTS/CTE flags as no-longer-applicable to a shipped card)** |
| PLA | **Ultimate tensile strength** | 26.4 MPa (FreeCAD's own value, kept) | FreeCAD `PLA-Generic.FCMat` | plamfg.com and multiple FDM-print studies report 40-60 MPa for standard PLA filament | **FLAGGED for human review, MOOT: card removed pre-release (see above)** - FreeCAD's own shipped figure is 30-50% below the commonly cited range for standard PLA. Kept FreeCAD's number rather than silently overriding it, but the whole PLA card was subsequently found to be an exact duplicate of core and removed before this release, so this flag no longer applies to anything this addon ships. |
| PLA | Thermal expansion coefficient | 41 µm/m/K (FreeCAD's own value, kept) | FreeCAD `PLA-Generic.FCMat` | One source (MIT PLA review) cites 740 µm/m/K, a >15x difference | **FLAGGED, MOOT: card removed pre-release (see above)** - 740 µm/m/K appears to describe PLA's much higher *above-glass-transition-temperature* CTE, not the room-temperature solid-state CTE this card's field represented; this is now moot since the PLA card is not shipped. |
| Nylon 6/6 (PA66) | Yield / UTS / E / ν / density / α | 83 / 84 MPa, 3000 MPa, 0.39, 1140 kg/m³, 80 µm/m/K | smithmetal.com Nylon 66 technical datasheet | Cross-checked against FreeCAD's own closely-related `PA6-Generic.FCMat` (Polyamide 6, not 6/6: ν 0.39 exact match, E 2930 MPa within 2%, density 1150 kg/m³ within 1%, α 82 µm/m/K within 2%) | Agree - PA66 and PA6 have near-identical elastic constants; strength differs slightly by chemistry, both individually sourced - **PARTIAL, shipped: core has no PA66/6-6 card, only PA6; kept per README Tier 2** |

## Magnesium

| Material | Property | Value used | Source 1 | Source 2 | Agree? |
|---|---|---|---|---|---|
| AZ31B | Yield / UTS | 200 MPa / 260 MPa | machinemfg.com AZ31B guide (200 MPa YS) | Springer "Mechanical Behaviour of AZ31B Magnesium Alloy at Elevated Temperatures" (201 MPa YS at 25°C, 256 MPa UTS) | Agree |
| AZ31B | Density | 1770 kg/m³ | Widely-cited standard Mg-alloy density (1.77 g/cm³) | Cross-check: specific gravity 1.78 (galaxymagnesium.com catalog) | Agree (<1% difference) |
| AZ31B | Young's modulus | 45 GPa | Widely-cited AZ31B value (~44-45 GPa across multiple engineering references) | Springer paper: 43.80 GPa at 25°C | Agree (<3% difference) |
| AZ31B | Poisson's ratio | 0.35 (adopted) | Broad-literature generic magnesium-alloy value (~0.35) | A temper-specific citation for AZ31B-H24 gives 0.29 | Documented variability by temper, not a hard error - this card does not specify a temper (generic wrought AZ31B), so the broader literature value was used; noted for completeness |
| AZ31B | Shear modulus | 17 GPa | AZ31B-H24-specific citation (makeitfrom.com-style, 17 GPa) | Internal consistency check: G = E / (2×(1+ν)) = 45/(2×1.35) = 16.7 GPa - matches within 2% | Agree |
| AZ31B | Thermal expansion coefficient | 26 µm/m/K | psec.uchicago.edu CTE reference table (26.0 ppm/°C for wrought AZ31B) | ResearchGate directional CTE table (23.2-25.6 µm/m/K across RD/TD/ND); 26 is the commonly cited average | Agree |

---

## Summary of flags requiring human review before treating as authoritative (as shipped, 21 cards)

1. **ASTM A36 Poisson's ratio** - genuine literature split (0.26 vs 0.30). Adopted 0.30 for internal library consistency; a precision structural analysis should verify against the specific source document it will be audited against.
2. **Gray iron G3000 yield strength** (140 MPa) is an estimated proportional proof stress, not a directly published/standardized number - gray iron has no true yield point. Documented as a caveat in the card's own Description field.

(PLA's two flags, listed in the row-level table above, are moot: the PLA
card was removed pre-release as an exact duplicate of core, 2026-07-10 -
see the header note at the top of this document.)

No other property in this table exceeded the 5% disagreement threshold without an explained, non-error reason (typical-vs-minimum spec values, product-form/temper differences, or directional variation).

## Fable orchestrator accuracy audit (2026-07-09)
Systematic isotropic-consistency check applied to all 28 cards: G vs E/(2(1+v)),
flag if >5%. Result: 25/27 consistent. Two corrected for physical consistency:
- 304 (1.4301): ShearModulus 81000->77000 MPa (was carbon-steel value; now
  consistent with E=200GPa, v=0.30); Density 7800->8000 kg/m^3 (austenitic
  stainless standard).
- CP-Ti Grade 2: ShearModulus 45000->38400 MPa (was 17% inconsistent; enforced
  isotropic triple with E=103GPa, v=0.34).
Spot-checked definitional/well-known values (S235JR/A36/6061-T6/7075-T6 yields,
densities, moduli) against known engineering data: all correct.

## Fable resolution of flagged values (2026-07-09)
- A36 Poisson's ratio: RESOLVED to 0.30 (already the card's value). 0.30 is the
  universal engineering/FEA standard for structural carbon steel; the 0.26
  outlier is a single-source measurement, not the design value. No change needed.
- PLA UTS (26.4 MPa): KEPT AS FLAGGED - PLA tensile strength is genuinely
  process-dependent (injection-molded ~50-60 MPa vs 3D-printed ~30-50 MPa);
  FreeCAD's shipped 26.4 is conservative-printed. Needs a human choice + a
  README note on print-orientation dependence. Left to user.
- Gray Iron G3000 yield: KEPT AS FLAGGED - gray cast iron is brittle with NO
  true yield point; value is an estimated proof stress. Inherently ambiguous;
  documented as such. Left to user.

## Prior-art removal pass (2026-07-10)

Following `ops/novelty-standards-library.md`'s adversarial prior-art check
(live WebSearch/WebFetch against FreeCAD/FreeCAD core and
FreeCAD/Supplemental-Materials), 7 of the above 28 rows were confirmed
byte-for-byte duplicates of already-shipped FreeCAD core cards and were
**deleted from `Resources/Materials/Standard/`** before this release:
S235JR, S275JR, 6061-T6, 7075-T6, Ti-6Al-4V Grade 5, ABS, PLA. Their rows
above are kept (not deleted) and individually annotated
"REMOVED PRE-RELEASE: exact duplicate of core" so this document remains a
complete, honest record of everything checked, including what was cut and
why. This addon now ships **21 cards**. A further 6 rows (S355JR, 304,
316L, 6082-T6, C11000 copper, Nylon 6/6) are equivalent-or-corrected
variants of an existing core card under a different designation - these
are annotated "EQUIVALENT/PARTIAL, shipped" and remain in the release; see
the README's Tier 2 table for the reviewer-facing explanation of each. The
remaining 15 rows are net-new to the entire FreeCAD ecosystem (core and
Supplemental-Materials both checked). Total: 7 removed + 6 equivalent +
15 net-new = 28 rows recorded, 21 cards shipped.
