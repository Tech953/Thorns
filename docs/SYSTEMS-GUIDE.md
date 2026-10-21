> v0.4: This file describes the original chapter systems. For open-world changes, including independent duels, equipment, survival, contracts, and karma, see OPEN-WORLD-GUIDE.md.

# THORNS 0.2 — Characters, reputation and procedural encounters

This update integrates character creation and regional social systems into the existing 1–6 player game. All new statistics, thresholds, encounter prose, travel abstractions, dialogue and PvP rules are prototype adaptations. The uploaded previews describe capabilities and limits, but do not supply numeric attribute, damage, health, reputation or distance rules. The source’s institutional privileges and immutable boundaries remain constraints.

## Create a character

Start the server as described in README.md, then use the character creator above the expedition lobby. Choose a discipline preset, customize its four attributes and proficiencies, and describe your origin, embodiment, affiliation, affinity, history, goal and boundaries. Supply your name when creating or joining the room. Pronouns, form and origin never apply score modifiers.

A preset change replaces the current draft with that preset. Save your draft first if you want to retain it. You can save/load one browser draft or export/import a portable JSON character. Exports contain the concept and build only; they do not include room credentials, XP, reputation, live permissions or saved campaign progress. Importing a build never imports privileged access. The server validates allocations independently of browser validation.

Within a room, use **Edit my character** before the host starts. Editing locks on start. Party character sheets show each member's build, XP, permissions and recorded conditions. History and boundaries are shared with the party; these are roleplay guidance, not enforced content filters. At present there is no name-change control in the editor, though the authenticated lobby-edit API accepts a valid name.

## Measurements used by the game

| Measurement | Range / calculation | Effect |
|---|---|---|
| Body | Integer 1–4 | Physical movement and execution |
| Tech | Integer 1–4 | Technical integration, repair and craft |
| Percept | Integer 1–4 | Observation and pattern discrimination |
| Rapport | Integer 1–4 | Negotiation, cooperative teaching and speech |
| Attribute budget | Exactly 8 total | The original six presets remain available |
| Proficiency rank | Integer 0–3 | 0 untrained; 1 familiar; 2 practiced; 3 focused |
| Training budget | Up to 6 total | Unspent points are visible; no post-start spending yet |
| Experience | Non-negative earned XP | +1 XP per attempted expedition/encounter check |
| Experience bonus | min(2, floor(XP / 3)) | Adds to checks |
| Applicable training | min(2, highest relevant rank) | One skill contributes, not the sum of all skills |
| Bio-mod contribution | 0 or +1 | Only its listed chapter checks, with expedition registration |
| Practice bonus | min(2, training + bio-mod) | Prevents skill/equipment stacking beyond +2 |
| Findings bonus | 0–3 | Only the authored final-contact checks; not random encounters |
| Check target | Scene DC; encounter DC 10–13 before reputation | D20 + bonuses must reach target |
| Natural die | Integer 1–20 | 1 always fails; 20 always succeeds |
| Success probability | 5%–95%, calculated over all 20 outcomes | Shown for the currently selected specialist |
| Shared cohesion | 0–10 | Failed checks cost 2; 0 withdraws the expedition |
| Sanctuary recovery | Restore cohesion to 10 | On authored arrival at CHECKPOINT.RESID before defeat |
| Faction / relationship reputation | Integer −10 to +10 | Persistent party-level regional standing |
| Local scene position | Integer 0–4 | Abstract positions on a line, each separated by 5 m |
| PvP distance | 0–20 m | Absolute position difference × 5 |
| Duel composure | 6 + 2 × Body maximum | Non-lethal sparring resource, separate from cohesion |

Rank 3 is retained as a training distinction, but currently provides no greater chapter-roll bonus than rank 2. There is no skill-rank progression after creation yet. Individual HP, stamina, mana, armor damage reduction, encumbrance and generic resurrection charges are **not** documented numeric measurements in the provided files and are not simulated in this build. Composure is explicitly a new training mechanic, not an inferred biological measurement.

## Character lore and limits

The catalog covers 25 proficiency tracks. Each appears with its source document, source section, and current use in the creator. Ballistics is used in consensual ranged duels. medTech, necra-mod theory and Life Strings are recorded but have no expedition encounter mechanics yet. Training does not activate restricted equipment or override jurisdiction.

One optional mod can be selected: LEG|SPIKES, regulated Meta-Fingers, a Corded Bio-Glass interface, or a Crystallin< retrofit. Their +1 effects and the one-slot limit are new balance rules. They remain dormant until the expedition chooses registration. The game uses that flag only for the listed chapter interactions; it is not a universal authorization system.

Origins cover WN_TOWER, CITY_CLOUD_S, ENACT_HILLS, AETHERGALE and itinerant/unspecified. NULL_FIELD.OMNI is not offered as a confirmed native player origin. Metal-kin and lightPROKT< are available as embodiment concepts with explicit limitations: the prototype does not simulate their entire ontology, nutrition, resurrection, or creation prerequisites. It does not claim these are interchangeable canonical species.

Certification records track black.dot, Merc Tag, WN_EDU, ED.NET, MERC.DOT, admin.OS and adminENACT. Registration and the ED.NET lesson update narrowly scoped chapter records. Everything else remains unverified. A high reputation, chosen affiliation, imported JSON or high die cannot grant admin authority, exempt a necra-mod from MERC.DOT, open RED>GATE>, or nullify death outside a documented context.

Autonomia, neural plasticity, semblance, percept, power stance, fidelity, meta-break, omni-meta, infi-particle, ennerENACT, MMTX< and absolutENACT are contextual lore concepts, not all synonymous numerical meters. They are represented through descriptions, particular proficiencies, permissions, scene constraints and source notes. Unknown quantities remain unknown.

## Reputation

There are 25 independent faction/relationship records, shared by the expedition and starting at 0. Scores persist in the room database and appear beside a reasoned change log. Distinct records include regional institutions, residents, the THORNS, NanoClad, and personal/community relationships such as PYRI and Lila / CASC. These labels are game relationships, not a claim that every entry is a corporation or faction.

| Score | Standing | Random-encounter DC adjustment |
|---|---|---|
| −10 through −6 | Distrusted | +2 |
| −5 through −3 | Wary | +1 |
| −2 through +2 | Unknown / mixed | 0 |
| +3 through +5 | Welcomed | −1 |
| +6 through +10 | Trusted | −2 |

Successful authored contributions add +1 to a relevant relationship. Successful final contact and returning findings have additional explicit awards. Successful random-encounter commitments add +2 to the represented contact; failed commitments cost −1. Declining an encounter costs no reputation or cohesion. Failure is not a global morality judgment. Reputation never penalizes withdrawal from an invitation or duel.

Reputation currently changes random-encounter DCs and their contextual text. It does not change authored chapter DCs, prices, inventories, faction wars, or institutional permissions. Records without a matching authored event can still change through regional encounters. No reputation is awarded for PvP, preventing repeated sparring from producing faction influence.

## Procedural encounters and speech checks

The host can enable **Regional random encounters** when creating a room; it defaults on. After each authored transition to a non-ending scene, the server has a 60% chance to insert one encounter before that scene. There are no nested random encounters. Declining or resolving one returns to the pending authored scene. This applies on sanctuary arrival too; sanctuary recovery occurs first, and a subsequent encounter's failure represents lost expedition cohesion rather than a death event.

The generator selects from 12 authored situation templates, a regional atmosphere, a complication, a regional contact, a base difficulty and that contact's reputation reaction. It excludes the previous three template types from selection. A generated encounter is stored, so refreshing the browser does not reroll it. This is procedural assembly of authored material, not LLM text generation or an infinite world simulation.

Every encounter offers three approaches using different relevant skills—usually speech plus two practical or observational approaches—and an unconditional decline. The same party vote and specialist system handles them. A speech check uses Rapport, applicable training, experience and the faction-adjusted DC. It represents how an NPC interaction resolves in this game; it never forces another human player to agree or obey.

Templates include pilgrimage delays, salvage disputes, shelter repairs, uncertain echoes, teaching exercises, provision schedules, ink manifests, seam exercises, crystallin< references, darkwood records, light patterns and ambiguous contracts. All encounter situations are newly authored adaptations. Geographic context does not override RED>GATE> or create unexplained safe passage into NULL_FIELD.OMNI.

## Distance, local speech and PvP

Distances are deliberately abstract local staging, not measurements inferred from the drawn maps. All players begin each authored scene at position 0. Move left or right one position (5 m), once per shared turn. Each authored choice or random-encounter resolution advances the shared turn. Global party chat remains usable at any distance. Local targeted speech reaches 10 m and consumes the player's one local speech/duel action for that shared turn.

Duel flow: choose another player within 15 m → invite → the recipient accepts. Each player may have one pending or active duel. An invitation alone allows no attack. Either participant can decline or disengage without penalty, regardless of distance. Travel to a different authored scene cancels invitations/duels and restores composure; resolving a random encounter does not relocate anyone. Duels are unavailable after a chapter ending.

| Duel action | Maximum range | Roll bonus | Target | Composure effect on success |
|---|---|---|---|---|
| Close maneuver | 5 m | Body + capped Transversal + XP bonus | 10 + target Body | −2 |
| Ranged training | 15 m | Body + capped Ballistics + XP bonus | 10 + target Body | −2 |
| Verbal feint | 10 m | Rapport + capped Contract mediation + XP bonus | 10 + target Percept | −1 |

These are non-lethal practice abstractions, not a full weapon simulator. Natural 1/20 rules apply. Only one local speech or duel action is allowed per player per shared turn. There are no automatic PvP rounds: advancing the expedition refreshes action availability. A target at 0 composure concedes, ending the duel and resetting both participants. There is no theft, encap, permanent injury, forced allegiance, reputation gain or XP from duels. The verbal feint changes the agreed training score only, not the other player's beliefs or decisions.

## Compatibility and remaining scope

New rooms use the new creator and can enable encounters. Existing saved characters load with their original attributes and no free added training; existing rooms default encounters off. Before starting a legacy lobby, its players can explicitly edit their builds. Existing active campaigns retain locked characters.

This release is still Python source with a Windows launcher, not an EXE. Browser visual verification, actual multi-device LAN play, internet deployment and Windows packaging remain separate gates. The next production expansion could add navigable procedural regions, faction-specific encounter decks, persistent individual reputations, broader inventories, fully scoped certification quests and optional tactical combat. None of those is claimed to be present here.
