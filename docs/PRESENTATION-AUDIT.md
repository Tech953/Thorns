# THORNS presentation audit

Reviewed 30 September 2026 against all five uploaded DOCX world references and the v0.4 interface source. The updated source package is v0.4.1.

The CRT foundation suits the requested text RPG, but its original uniform green palette and interchangeable generated descriptions flatten the setting. The documents describe several distinct cultures, materials, institutions, and degrees of uncertainty. The interface should preserve those distinctions while keeping actions and numerical rules readable.

This audit distinguishes direct source evidence from design interpretation. The DOCX files are world references, not a complete UI specification: they do not prescribe screen layouts, fonts, button designs, or hexadecimal palettes. All five were inspected through their DOCX paragraphs; none contains embedded inline illustrations. The separate map photos remain the geographic visual references. This is a source and implementation review, not a completed visual browser audit.

## Source to presentation mapping

| Reference and section | Documented aesthetic or narrative cue | Presentation treatment |
|---|---|---|
| WN_TOWER Reference — Sap Core; Greatweb; Undercroft.Beta | Sterile corporate advertising contrasts with darkwood ash, bio-plast, infrastructure overlays, and precarious civilian life | Ash-dark surfaces, restrained warm highlights, contract/verification language; reserve sterile treatment for specific corporate content |
| WN_TOWER Reference — Fractech; Druid-Sec; ANC.NI | Mathematical overlays, geometric feedback nodes, fractals, and signed bio-nano ink | Fine structural lines and bounded node motifs; do not substitute generic occult runes for the explicitly more precise craft |
| CITY_CLOUD_S — ED.NET; Plat.EN_MID; PEAK.EN_PERCEPT | Mountain metallurgy, geometric learning infrastructure, functional utility, and sharply different access conditions | Cool metallic palette and compact indexed survey grid; distinguish learning, survival, and restricted nodes in future district interfaces |
| ENACT_HILLS — FOOTHILL CUSP; UPPER RUNEHILLS; GRAVESITE | Ordinary washing, cooking, farming, crafted metal-kin, voluntary teaching, and strict archival boundaries | Warm residential base with a restrained archival accent; distinguish everyday provision from institutional authority |
| AETHERGALE — introduction; OMNICUSP; CHECKPOINT.GALE | Explicit jade and rose contrails, dust, tent-constructs, crystalline energy forms | Jade structural accents and rose highlights over dark dust-toned surfaces; retain text legibility |
| NULL_FIELD.OMNI — NODE>CONNECT; END_LINE_signpost; HELIX.BALANCE | Misleading scale, changing records, uncertain geometry and percept, structures not fully understood | A distinct remote-percept state, dashed uncertainty marker, and generated descriptions that preserve uncertainty |
| AETHERGALE — RED>GATE>; CHECKPOINT.UNDERTOW | Resistance to crossing and integration; observation does not establish ordinary access | Explicit remote-projection label; no visual implication that a normal grid step proves entry |

Only the jade/rose relationship is a direct regional color instruction. The other screen palettes, spacing, and typographic choices are design interpretations of the prose. Scarlet, gold, crimson, and other source colors belong to specific phenomena and must not become universal faction branding without support.

## Findings and disposition

| Priority | Finding in v0.4 | v0.4.1 disposition |
|---|---|---|
| High | All regions used essentially the same terminal palette | Added five regional CSS palettes driven by the displayed region, retaining a shared CRT framework |
| High | Procedural description fragments were largely interchangeable | Added region-specific material and atmospheric fragments; generated site names and placements remain adaptations |
| High | Generated terrain could be read as verified source geography | Added persistent procedural-survey and remote-percept labels above the grid |
| High | The chapter creation text implied its bio-mod activation rule also governed open world | Reworded the helper text to distinguish chapter registration from clinic installation |
| Medium | Supply, care, contracts, and mod actions competed in one long flow | Added provision and care headings and explicit installation cost/status on mod buttons |
| Medium | Grid used 11 px text and had no visible orientation explanation | Increased grid text to 12 px, added north/distance/occupancy legend, and improved narrow-screen button wrapping; browser zoom and mobile validation remain necessary |
| Medium | CRT scanlines covered all content with a relatively strong overlay | Reduced overlay opacity; retained manual CRT off switch and suppressed overlay for reduced-motion preference |
| Medium | Textareas lacked the explicit keyboard focus treatment applied to other inputs | Added textarea focus outline |
| Medium | Checkboxes inherited full-width text-input presentation | Added compact checkbox dimensions and alignment |
| Low | Character builder still advertised rules v0.2 in a v0.4 app | Replaced stale version copy with an adapted-rules label; footer now identifies v0.4.1 |
| Low | Health meter maximum could remain 100 after returning to chapter presentation | Chapter rendering now restores its 10-point maximum |

## Remaining alignment gaps

**Regional institutions need more than recoloring.** Sap Core advertising, WN_MED contracted treatment, ANC.NI artist signatures, and MOD_OP verifiable exchanges merit distinct content modules. The current generic clinic and credit economy must not be presented as a literal implementation of every institution. WN_MED excludes the general population; MOD_OP describes exchanges in which ordinary currency is meaningless. These require gameplay/content decisions beyond this presentation patch.

**Free provision at CHECKPOINT.RESID is not represented by the generic paid sanctuary.** The authored chapter's named checkpoint and the open-world generator's generic sanctuary should remain visibly distinct. A future named location implementation should honor the document's specific provision and death-state claims while identifying any balance adaptation.

**CITY_CLOUD_S has meaningful internal divisions.** A single metallic theme does not communicate the differences between ED.NET, Plat.EN_MID, and PEAK.EN_PERCEPT. District-level layouts should distinguish learning access, functional survival environments, and permission-governed interfaces without inventing universal safety or authority.

**ENACT_HILLS needs ordinary life alongside control.** Cooking, repairs, farming, and craft are direct source details. They should appear through encounter and location variety, not only through warm colors. PYRI's voluntary offer language should remain specific and should not be used to soften the documented coercive institutions elsewhere.

**Procedural descriptions remain a small combinatorial set.** The patch provides regional framing, not exhaustive ecological or architectural generation. Eight-coordinate sanctuary spacing, region quadrants, shared 5 m tiles, contract rewards, and distant projection traversal are explicit game abstractions.

**Information density still needs human testing.** Character creation is lengthy; sheets, 25 reputation tracks, and many action controls remain dense. A future pass should introduce progressive disclosure with a persistent build summary and a compact personal-status strip. Do not hide consequences or required information merely to achieve visual minimalism.

**The complete interaction vocabulary needs a consistency pass.** Keep source proper names and their distinctive punctuation; use plain language for player verbs. Reserve uppercase terminal labels for navigation and short states, rather than every paragraph. “Install,” “inspect,” “accept,” and “decline” should remain understandable without a glossary.

## Validation and acceptance criteria

All 24 existing automated tests pass after the presentation changes; JavaScript syntax checks pass for app.js and openworld.js. The tests cover rules and HTTP delivery, not visual correctness. No new Windows EXE was built. A Playwright browser executable is unavailable in this workspace, so screenshots and native browser interaction are not claimed.

Before considering presentation approved, inspect actual rendered screens at 390, 768, and 1366 px widths and at 200% zoom. Check each regional theme in both chapter and open-world contexts; verify long player names, populated grids, encounters, mod lists, empty and full inventories, and errors. Confirm keyboard focus stays visible, status is understandable without color, controls do not overlap, and CRT off persists. Measure rendered text contrast before claiming accessibility compliance.

The next visual pass should prioritize the character creator and open-world action panel, then district-specific treatments. This patch establishes the regional visual language and corrects misleading copy; it does not complete that visual acceptance gate.
