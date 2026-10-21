# THORNS v0.4 — Open world prototype

Choose **Open world grid** when creating a room. Select **Hardcore survival** if desired; both settings lock at creation. Assemble 1–6 players, then Begin Expedition. Existing saves retain chapter mode. The original adventure remains selectable.

## Grid and percept

Every player has independent integer X/Y coordinates. Each cardinal move advances one 5-metre interaction tile. The display shows a 5×5 neighborhood, north at the top, with player names on occupied tiles. Distance uses Manhattan steps, including for local speech (10 m) and mutually accepted training duels (5/10/15 m by approach). Global party chat works across the map. There is no real-time clock and no passive hunger while offline.

Locations are generated reproducibly from room seed and coordinates. Regions, facilities, names, and descriptive fragments produce a large but deliberately finite combinatorial backdrop, not unlimited authored narrative. Coordinates are bounded to ±1,000,000 on each axis. Quadrants and 5 m scale are gameplay adaptations, not a reconstruction of the drawings. Sanctuary exists at origin and every eight coordinates on both axes.

Beyond radius 40, generated OMNI-META-INFI-PARTICULATE locations are explicitly **remote percept projections / unverified semblances**. They do not establish entry through RED>GATE>, canonical interior geography, unrestricted admin privileges, or safe access to NULL_FIELD. Original references are included unchanged.

## Builds and bio-mod access

The existing four attributes and 25 proficiencies remain configurable. The creator's initial mod is a **chapter blueprint**; open-world equipment is installed separately at the sanctuary or a clinic. Eight options are available, using three slots. Installation costs 12 credits; removal is free with no refund. Players begin with 30 credits.

| Mod | Relevant proficiency / effect |
|---|---|
| LEG\|SPIKES | Transversal +1 on matching open-world checks |
| Meta-Fingers | Fractech +1 |
| Corded Bio-Glass | medTech +1 |
| Crystallin< retrofit | Crystallin +1 |
| Survey lens (adaptation) | Percept +1 |
| Filter graft (adaptation) | Fieldcraft +1; prevents particulate irritation from wilderness hazards |
| Rest regulator (adaptation) | Fieldcraft +1; sleep debt rises 2 rather than 3 per survival tick |
| Resonance link (adaptation) | Contract mediation +1 |

Matching mod bonuses cap at +2. Not every proficiency has a procedural check yet: transversal and medTech remain equipment/build records awaiting matching open-world encounters. Clinic care currently has a fixed credit cost, not a medTech roll. Mods do not modify training duels. These bounds are intentional prototype limitations.

## Contracts, karma, reputation

Relay, market, and sanctuary boards offer one survey contract at a time. Reach its coordinates and pass a Percept check (DC 10). Failure consumes a survival tick and permits retry. Success pays 18 credits, 1 XP, +2 faction reputation, +2 personal karma, and one care-benefit tier, capped at 3. Each tier reduces clinic cost by 3 credits, from 12 to a minimum of 3. Abandoning an accepted commitment costs 1 faction reputation and 1 karma.

Faction reputation is shared by the party; karma and benefits belong to each character. Karma ranges from −100 to +100 and records conduct; it does not yet gate dialogue or endings. Successful encounter assistance adds 1 karma and 5 credits. Declining a random encounter is neutral. The contract system currently has one reusable survey objective with changing destinations and faction contacts, not a full quest generator.

### Character context links

The board previews deterministic context notes before acceptance. Survey work recognizes whole-phrase, case-insensitive livelihood matches for route/survey work (courier, scout, surveyor, cartographer, mapmaker, route mapper/recorder, guide, pilgrim) and records/research work (researcher, archivist, historian, scholar, analyst, scribe, record keeper). A relationship thread appears only when the character's relationship/promise text contains the issuer's normalized name; explicit short aliases are KHO, ED.NET, FOOTHILL CUSP, CHECKPOINT.RESID, Lila, and CASC. These notes describe a possible point of familiarity, not trust or permission.

Procedural encounter notes use fixed template tags: pilgrims → route/survey; salvage → craft/repair or supply/trade; shelter → craft/repair, care, or ecology/stewardship; echo → records/research or teaching/learning; lesson → records/research or teaching/learning; provision → supply/trade or care; ink → records/research or supply/trade; seam and crystal → craft/repair or records/research; wood → records/research, supply/trade, or ecology/stewardship; light → records/research or teaching/learning; rhetoric → records/research or supply/trade. Recognized livelihood terms are mechanic, repairer, artisan, metalworker, craftsperson, technician, engineer, seamLLurgist, needlurgist; farmer, trader, merchant, supplier, provisioner, cook, caravan runner, vendor; medic, healer, nurse, caregiver, care worker, field medic; teacher, tutor, instructor, educator, student, apprentice; ecologist, botanist, cultivator, forager, gardener, and druid.

Local-contact dialogue has fixed topic tags: place → route/survey, records/research, ecology/stewardship; needs → craft/repair, supply/trade, care, ecology/stewardship; history → route/survey, records/research, teaching/learning; access → route/survey, records/research; contracts → route/survey, records/research, supply/trade; plans → route/survey, craft/repair, records/research, teaching/learning, ecology/stewardship. Matching tags appear beside the existing reply; an exact issuer-name match may also show a relationship thread. These annotations do not alter the reply, dialogue check, trust update, standing, access, stock, or permissions.

Context annotations do not change which contract or encounter is generated, the route, DC, die roll, rewards, reputation, standing, or permissions. Unrecognized free text remains visible on the character sheet but is not interpreted by these rules.

## Encounters and checks

With procedural encounters enabled, movement has a 30% encounter chance. Twelve templates avoid each character's three most recent encounters. Each provides three authored speech/skill approaches and a neutral decline. Encounters pause that character's other exploration actions until resolved; other players remain free to act.

D20 + attribute + training (max 2) + experience (max 2) + matching mods (max 2) − condition penalty. Natural 1 fails; natural 20 succeeds. Base DC 12, −2 with faction reputation ≥6 or +2 at ≤−6. Success grants +2 reputation; a failed commitment costs 1. The action log gives the actual roll and modifiers.

## Hardcore survival

Hunger, thirst, and sleep debt range from 0 (satisfied) to 100. Movement, scavenging, rest, and failed contract surveys advance personal time. Each tick adds 3 hunger, 5 thirst, and 3 sleep debt (2 with rest regulator). Each need at 90+ costs 4 health per tick, plus 1 per ailment. A need at 70+, an injury, or an ailment each impose −1 on open-world checks, capped at −5 overall.

Wilderness movement sometimes checks fieldcraft. Failure can cause abrasions/strained leg, 10 health damage, and particulate irritation unless a filter graft is installed. Injuries do not stack duplicates. Food/water reduce the matching need by 40. A medkit heals 25 and removes one injury. Rest at sanctuary resets sleep debt and heals 20 while consuming a tick. Clinic care restores health and clears injuries/ailments; it does not satisfy needs. Supplies can be purchased at markets/sanctuaries; successful scavenging in ruins/wilds gives one food or water.

Zero health during a tick triggers evacuation to origin, 35 health, needs reduced to 40, and a rescue fee of up to 15 credits. Injuries/ailments remain. **There is no permadeath.** All embodiment concepts currently use the same survival rules; this is a gameplay abstraction, not a biological claim about metal-kin or lightPROKT<.

## Player disputes

Players must invite and accept a non-lethal duel. Accepted duels alternate actions without requiring story votes. Either participant can disengage at any time. There is no forced theft, obedience, lethal PvP, or reward farming. Open-world travel is blocked while an invitation or duel is present; disengage before moving. Thus this version supports grid distance at initiation, not movement within a duel. Local speech can be sent once per personal movement/time step; party chat is unrestricted.

## Playtest priorities

Test independent movement and speech with six humans, survival pacing, supply scarcity, mod value, contract repetition, narrow screens, and reconnection after a host restart. Browser visual playtesting and Windows executable testing remain outstanding. This is an expanded source prototype, not a finished open-world RPG.
