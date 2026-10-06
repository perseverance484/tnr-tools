# Genin Battle Pyramids — Narrative Design Plan

**Status:** PROPOSAL — revised after director feedback; approval required before manifest/build work  
**Design owner:** ChatGPT, Content Designer lead  
**Implementation owner after approval:** Fable / Claude Code  
**Frozen evidence baseline:** `main@b6f719dc5241f2b4fefc553670a61ea0c4a16d6e`  
**Fresh live quest census:** `harvests/inbox/tnr_results_1791233210169.json` (DONE / success)  
**Live requests/writes in this design pass:** 0 / 0

## Design goal

Create three entry-level Genin `battlepyramid` challenges at levels 15, 20 and 30 that feel like **real pieces of TNR's world**, not combat tutorials wearing a thin theme.

The three challenges form a loose roadside arc:

1. **The Quiet Mile** — a missing cart looks like a wildlife problem until the scene says otherwise.
2. **The False Toll** — a road gang is exploiting trade traffic with forged authority.
3. **The Burned Crest** — low-grade rogue shinobi are teaching ordinary criminals how to resist village patrols.

The escalation is intentionally grounded:

**hazard -> crime -> shinobi crime**

The player is not saving Seichi from a supernatural catastrophe. They are becoming a more capable field shinobi: first clearing a road, then reading a criminal operation, then confronting the people enabling it.

Each pyramid must also work independently. Later entries can refer to "recent route reports" or "recovered ledgers" without requiring the player to have completed the earlier challenge.

## Why this fits current Genin content

Fresh live Genin content already establishes a strong low-rank vocabulary:

- Mission halls and case desks assign mundane work.
- Trade roads, carts and waystations are recurring spaces.
- Route watches, missing transports, stolen seals and unidentified operatives are normal Genin/C-rank concerns.
- Genin Trials move from technique training at level 14 into active field duty in the low 20s.
- Existing missions such as **The Long Road**, **The Waystation**, **The Empty Contract**, and the Genin case-work content make ordinary logistics and criminal intelligence feel native to TNR.

These pyramids should sit beside that material, not compete with it by introducing another secret world-ending faction.

## Mechanical doctrine for all three

- **Quest type:** `battlepyramid`.
- **Fixed encounters:** `opponent_scaled_to_user: false`.
- **Level windows:** 15–30, 20–30, 25–30.
- **Quest ranks:** D / C / C.
- **AI rank:** GENIN for all proposed enemies.
- **AI multipliers:** `statsMultiplier: 1`, `poolsMultiplier: 1`.
- **Passive AI tags:** none.
- **Hard gimmicks:** none.
- **No:** seal, reliable hard stun chains, movement lock, absorb checks, reflect, redirection, one-hit kills, summons, cleanse prevention, or build-specific counters.
- **Shared AI pool only:** no one-off jutsu minting.
- **Failure behavior:** retry the current fight, not the whole run.
- **Flow law:** every fight is gated by a non-battle node. Use `dialog -> start_battle -> dialog`; never consecutive `start_battle`.
- **Rewards:** terminal victory only; exact values remain user-owned.
- **Publishing:** hidden on creation.

The player should lose because they mismanaged range, AP, cooldowns, or target priority, not because they failed to bring one specific answer.

---

# I. The Quiet Mile

**Gate:** Level 15–30  
**Quest rank:** D  
**Combat shape:** 3 solo fights  
**Core fantasy:** A routine road-clearance job becomes a small field investigation.

## Opening premise

A supply cart missed its scheduled arrival at the next waystation. Nobody has raised an alarm yet. The mission board pays a Genin to walk the quiet stretch, find the cart, and reopen the road if possible.

The road is too quiet.

The first evidence suggests animals attacked the cart. By the end, the player understands the opposite: the animals were drawn in **after someone deliberately wrecked and stripped it**.

This teaches an important low-rank shinobi fantasy: the job is not merely "kill three animals." It is **notice what happened while surviving what is still there**.

## Narrative / battle flow

### Beat 1 — Spilled grain

The player finds sacks torn open across the road and deep hoof marks around the ditch. A boar is still rooting through the cargo.

**Fight 1:** **Brush Boar — Lv12**

Combat identity:
- slow, direct bruiser;
- basic damage only;
- heavier hit on a longer cooldown;
- no status effects.

After the fight, the player inspects the wagon. The axle is not splintered from impact. It has a clean cut.

### Beat 2 — The harness

Farther down the road, the missing draft harness is caught in brush. The straps have been removed with a blade. A wolf circles the smell of food and blood left behind.

**Fight 2:** **Ridge Wolf — Lv13**

Combat identity:
- faster than the boar;
- lighter attacks;
- more reach / lunging pressure;
- no defensive gimmick.

After the fight, human bootprints appear beneath the animal tracks. The thieves left the road in a hurry.

### Beat 3 — The rocky cut

The trail ends at a narrow rock cut where several stolen provisions were dumped to lighten the load. The food has attracted a large bear that now blocks the way forward.

**Fight 3:** **Black Bear — Lv15**

Combat identity:
- durable solo capstone;
- ordinary heavy attacks;
- perhaps one mild `Fighter's Poise`-style stance if needed;
- no armor, passive steroid, or inflated pool multiplier.

## Resolution

Past the bear, the player finds the stripped remains of the cart and one small piece the thieves missed: a crude stamped token claiming passage through an old toll road.

The report matters more than the token itself:

> The wildlife did not stop the cart. Someone stopped the cart, and the wildlife came afterward.

The waystation can reopen the mile. The stamped token goes into the route report.

## Player-facing lesson

- Learn basic battle pacing against three readable solo opponents.
- Learn that TNR field work contains observation and evidence, not only combat.
- Introduce the road / waystation vocabulary used elsewhere in Genin content.
- Softly foreshadow the level-20 challenge without making it a prerequisite.

## Art direction

Prefer two environments rather than one repeated room:

1. quiet woodland trade road with the overturned cart;
2. rocky road cut with abandoned provisions.

AI visuals: grounded local wildlife, no fantasy mutations required.

---

# II. The False Toll

**Gate:** Level 20–30  
**Quest rank:** C  
**Combat shape:** 4 fights; first simple 1v2  
**Core fantasy:** Break a petty criminal operation that survives by impersonating legitimate authority.

## Opening premise

The stamped token recovered in recent route reports matches an abandoned tollhouse that has no current authority to collect anything.

Travelers have nevertheless been paying.

The gang operating it has rebuilt the barrier, copied old road signage, and carved crude versions of village seals into payment chits. Most civilians cannot tell the difference from a distance.

This is still a basic criminal problem, but it is a specifically shinobi-world crime: the gang knows that **the appearance of village authority is sometimes enough to stop a traveler before a weapon is drawn**.

## Narrative / battle flow

### Beat 1 — The barrier

The player reaches a barricade made from scavenged official road boards. A cutter steps out and demands payment.

**Fight 1:** **Tollroad Cutter — Lv17**

Combat identity:
- straightforward melee;
- Quick / Lunging / Heavy Strike family;
- no control.

Afterward, the player notices the "official" seal is carved backward on one board.

### Beat 2 — The roof

A second gang member fires from the tollhouse roof while someone inside starts pulling ledgers from the desk.

**Fight 2:** **Tollroad Slinger — Lv18**

Combat identity:
- basic ranged pressure;
- Twin Shot / Rapid Fire-style pool entries;
- teaches closing distance;
- no reliable stun.

Inside the office are names, amounts, cart descriptions, and patrol times. The gang has been watching the road long enough to know when shinobi escorts usually pass.

### Beat 3 — The storehouse

Two gang members try to move the stolen goods through the rear storehouse before the player can secure them.

**Fight 3:** **Tollroad Cutter Lv17 + Tollroad Slinger Lv18**

This is the first deliberate 1v2 of the new ladder.

The player now makes a meaningful but simple decision: remove the ranged pressure first, or eliminate the melee threat already closing in.

### Beat 4 — The ledger fire

The gang's captain is in the cellar trying to burn the account book.

**Fight 4:** **Tollhouse Captain — Lv20**

Combat identity:
- competent but mundane fighter;
- basic strike kit;
- one mild stance such as `Fighter's Poise` or `Minor Overflow`;
- AI Light armor is acceptable only if needed after testing;
- no exotic jutsu.

## Resolution

Most of the ledger is ruined, but one page survives.

It includes recurring payments marked only as **yard fees**, alongside purchases of practice weapons, medicine and travel provisions. The gang was not inventing its shinobi countermeasures on its own. Someone has been selling them instruction.

The false toll is dismantled. The stolen seals go into evidence. The surviving page is forwarded with the report.

## Player-facing lesson

- Introduce range as a tactical identity.
- Introduce the first multi-target fight without jumping to three-enemy pressure.
- Show how ordinary criminals operate inside a shinobi society.
- Make the player feel like they are dismantling a place, not clearing four arbitrary floors.

## Art direction

Two scene families:

1. improvised toll barricade / road approach;
2. cramped tollhouse interior and cellar.

Human enemies should look like practical road criminals, not elite assassins: layered travel clothes, cheap weapons, scavenged protection, no theatrical faction uniforms.

---

# III. The Burned Crest

**Gate:** Level 30  
**Quest rank:** C  
**Combat shape:** 5 fights; max 2 enemies  
**Core fantasy:** Discover the low-grade rogue shinobi supplying ordinary road crime with real fieldcraft.

## Opening premise

Route patrols follow the tollhouse ledger to a disused private training yard.

The compound has no flag.

Inside, old village crests have been scraped from storage boxes, training gear and armor plates. A few were burned rather than removed cleanly.

Whoever is here came from the shinobi world and does not want to advertise where.

The danger is not an elite rogue order. It is smaller and more believable: **deserters and castoffs selling basic combat instruction, patrol timings and practical shinobi knowledge to criminals who normally could not stand against a village response.**

That is an appropriate level-25 Genin threat. It also shows the player why rogue shinobi matter even when they are nowhere near Jonin strength.

## Narrative / battle flow

### Beat 1 — The outer yard

A fighter is drilling footwork against marked posts and immediately attacks when the player enters.

**Fight 1:** **Wayward Striker — Lv21**

Combat identity:
- close-range mobile pressure;
- Quick / Lunging / Opening Strike family;
- no hard control.

The drill marks are disciplined. This is not a roadside thug learning by trial and error.

### Beat 2 — The practice line

Another trainee uses simple elemental chakra against range markers.

**Fight 2:** **Wayward Adept — Lv22**

Combat identity:
- one basic 45-power elemental bolt from the shared pool;
- otherwise ordinary ranged pressure;
- no high-tier elemental combo or exotic status mechanic.

The player finds practice slates recording distance, timing and patrol-response drills.

### Beat 3 — Paired drills

Two fighters move together from opposite sides of the yard.

**Fight 3:** **Wayward Striker Lv21 + Wayward Guard Lv22**

Guard identity:
- sturdier frontliner;
- simple damage;
- one light defensive option;
- no absorb/reflect.

This introduces the first real target-priority puzzle: durable screen or mobile damage dealer.

### Beat 4 — The hall

The remaining trainees fall back into the main hall. A guard protects the elemental adept while records are carried toward the furnace.

**Fight 4:** **Wayward Guard Lv23 + Wayward Adept Lv22**

This reverses the previous pairing. The player now recognizes both roles and decides which one matters first.

### Beat 5 — The furnace room

The person running the yard is burning account books and scraped crest plates.

**Fight 5:** **Rogue Instructor — Lv25**

Combat identity:
- broad but ordinary Genin kit;
- basic melee attack;
- one ranged or elemental option;
- one mild stance;
- one light shield at most;
- GENIN rank, multiplier 1/1;
- no elite/boss passive package.

The final opponent should feel **experienced**, not superhuman.

## Resolution

The recovered records make the operation clear.

The yard was not building an army and was not serving one village. Its instructors sold whatever they still knew: how to approach a guarded road, how to pressure a ranged shinobi, how long patrols usually take to answer a flare, how to hold formation long enough to escape.

That knowledge was enough to turn ordinary thieves into a bigger problem.

The player closes the yard and files the surviving records. The story ends at the correct Genin scale: one criminal network has lost its teachers, several roads become safer, and the shinobi villages have a better picture of how their discarded knowledge is leaking into the world.

## Player-facing lesson

- First basic shinobi-vs-shinobi pyramid.
- Introduces mild buffs/defenses and a simple elemental identity.
- Uses two-enemy compositions to teach role recognition rather than raw swarm pressure.
- Broadens the player's understanding of TNR's setting without prematurely escalating to major villains, demons or endgame factions.

## Art direction

Two environments:

1. weathered outdoor practice yard with posts, worn targets and scraped insignia;
2. dim training hall / furnace room with discarded equipment and burned records.

The rogue shinobi should look like people who removed affiliation from old gear, not like a unified new faction. No shared grand insignia. Their lack of uniformity is part of the story.

---

# Progression summary

| Feature | Lv15 — Quiet Mile | Lv20 — False Toll | Lv30 — Burned Crest |
|---|---|---|---|
| Threat | displaced wildlife | organized road gang | low-grade rogue shinobi |
| Story question | What happened to the cart? | Who is impersonating authority? | Who taught the criminals? |
| Battles | 3 | 4 | 5 |
| Max enemies | 1 | 2 | 2 |
| Highest AI level | 15 | 20 | 25 |
| Range lesson | basic | melee vs ranged | role combinations |
| Utility | almost none | one mild stance | mild stance / light defense |
| Hard gimmicks | none | none | none |
| Scaling | fixed | fixed | fixed |
| Failure | retry current floor | retry current floor | retry current floor |

The important progression is not merely numeric:

**survive -> observe -> prioritize**

That is a stronger Genin fantasy than simply increasing enemy health.

# Story delivery standards

These are battle pyramids, not full story quests. Keep the prose disciplined.

- Each pre-fight dialog should be 1–3 short paragraphs.
- Every dialog must change the player's understanding of the location or situation.
- Do not insert fake choices that converge immediately to the same battle.
- Avoid lore dumps.
- Environmental evidence should carry the story wherever possible.
- The final resolution should be concise and report-like, consistent with Genin mission work.
- No major named faction needs to claim responsibility.
- Do not imply the three incidents are part of a world-scale conspiracy.

# AI / shared-pool direction

Exact kits belong in implementation, but use only the low-complexity portion of the shared pool.

Appropriate examples:
- `S01 Heavy Strike`
- `S02 Quick Strike`
- `S03 Lunging Strike`
- `S04 Opening Strike`
- `S06 Twin Shot`
- `S07 Rapid Fire`
- `B37 Fighter's Poise`
- `B38 Minor Overflow`
- `B39 Light Barrier`
- one of `EA01 / EE01 / EF01 / EL01 / EW01` for the Wayward Adept

Do not use stronger boss/control entries simply to differentiate enemies.

# Production scope

Preferred quality target if suitable reusable live assets are not found:

- **The Quiet Mile:** 3 enemy avatars, 2 scene backgrounds.
- **The False Toll:** 3 enemy avatars, 2 scene backgrounds.
- **The Burned Crest:** 4 enemy avatars, 2 scene backgrounds.

Before commissioning art, point-read existing candidate AI/assets. Existing wildlife or bandit art may be reusable even when the combat AI record itself should be new.

# Rewards / recurrence — unresolved

User-owned.

Recommended shape:
- all reward at terminal victory;
- no exclusive progression-critical item or jutsu;
- clear 15 < 20 < 30 progression;
- tuned as optional repeatable Genin PvE, not a windfall;
- cadence and exact reward values still require approval.

# Decisions required before Fable implementation

1. Approve or rename **The Quiet Mile / The False Toll / The Burned Crest**.
2. Approve the loose three-part roadside arc.
3. Approve fixed enemy levels rather than user scaling.
4. Approve 3 / 4 / 5 battles with max headcount 1 / 2 / 2.
5. Approve `maxLevel: 30`.
6. Decide whether continuity remains soft/independent (recommended) or becomes prerequisite-chained.
7. Decide reward values and repeat cadence.


---

# Reuse Audit — Existing AI, Lore and Scene Assets

**Status:** REUSE DIRECTION PROPOSED — this section supersedes the bespoke enemy/art assumptions above where they conflict.  
**Fresh usage evidence:** `harvests/inbox/tnr_results_1791233210169.json` (2026-10-05 quest census).  
**Profile evidence:** `harvests/inbox/tnr_results_1788235198666.json` (2026-09-01 mission-AI audit).  
**Asset evidence:** committed mission captures plus `skills/producing-tnr-art/data/style_refs.json`.  
**Live requests/writes for this audit:** 0 / 0.

## Lore boundary

The archived `The Unwritten War` roadmap is explicitly marked stale and must not be revived as operative canon.

The current live low-rank continuity is safer and more useful:

- C-rank missions already deploy **Unmarked Stray**, **Unmarked Blade**, and **Unmarked Shadow**.
- Their mission prose presents them as mouth-wrapped, affiliation-less paid operatives who care about route marks, schedules, caches and the job more than the fight.
- The higher reusable covert-line doctrine exists separately in current `references/lines.md`.
- Therefore these pyramids should expand the **existing Unmarked field pattern** without naming a hidden parent organization unless the user later rules one.

This keeps mystery intact and adds lore without importing a superseded arc.

## Verified reusable AI

| AI | Level / Rank | Existing role evidence | Reuse verdict |
|---|---|---|---|
| **GENIN 01** | Lv20 GENIN | Used by `Poachers' Due`; basic Quick/Steady/Rapid kit | Mechanically usable, but generic displayed name and Flaming Sword make it a weaker narrative choice |
| **Marauder** | Lv25 CHUNIN | Used by `The Long Road`; simple Opening Strike kit | **Strong reuse** as local hired muscle / road criminal |
| **Unmarked Stray** | Lv25 GENIN | Used by `The Empty Contract`; older Waystation build used multiple Strays | **Primary reuse**; simple low-rank operative |
| **Unmarked Blade** | Lv30 GENIN | Used by `Protection` and `The Waystation` | **Primary reuse**; natural Genin capstone operative |
| **Unmarked Shadow** | Lv35 CHUNIN | Used by `Chalk and Corner` | **Primary Lv30-pyramid boss reuse**; stronger operative but already used by low-rank C content |
| **Syndicate Thief** | Lv27 CHUNIN | Used by `Night Watch Shadow` | Existing art/profile but no equipped jutsu in audit; avoid unless separately repaired/verified |
| **Seichi Bandit** | Lv15 GENIN | Existing generic bandit record | Reject for now: no AI profile/jutsu and default avatar in captured state |
| **KGK Rogue** | Lv10 GENIN | Blacksteel/Genin Trials continuity | Mechanically reusable but faction-specific; do not dilute Kuroganekai identity into this arc |

All three Unmarked records already have non-default battle avatars and shared-pool kits. Reusing them eliminates new AI-avatar production and avoids one-off jutsu work.

### Unmarked combat profiles

**Unmarked Stray — Lv25 GENIN**
- 1x stats / 1x pools; 1300 HP.
- Quick Strike, Steady Strike, Venom Strike, Fighter's Poise, Bruising Blow.
- Reads as a basic paid fighter with one mild status rider.

**Unmarked Blade — Lv30 GENIN**
- 1x stats / 1x pools; 1550 HP.
- Twin Shot, Enervating Strike, Minor Overflow, Searing Strike, Heavy Cut.
- Reads as a trained mixed-range operative and is almost perfectly placed at the Genin level cap.

**Unmarked Shadow — Lv35 CHUNIN**
- 1x stats / 1x pools; 1800 HP.
- Withering Weave, Sundering Blow, Numbing Shot, Warrior's Poise, Lingering Strike.
- Too strong to be a normal Genin floor, but a good final threat for the level-30 pyramid because current C-rank content already deploys it against level-20 players.

## Existing wildlife candidates

The fresh quest census verifies these existing AIs as the targets of **D-rank hunting quests**:

- **MossWolf** — `AkGY27OK7lNmxvGAcGtJr`
- **Moonprowler** — `ld7Cd-yHU15NwRKyjToZs`
- **OwlCat** — `HS5pnbz_JDK43lNDBEoig`
- **Rust Ferret** — `R9JRTtK3cZubEWUMbEkfL`
- **Badgertle** — `gHPiwKQMYdf5-M1kfdom_`

This is strong evidence that TNR already has a native low-rank wildlife vocabulary. Their exact current level/profile/avatar suitability is **not** established by the quest census, so final floor assignment requires one read-only candidate capture before implementation.

Preferred direction: retire the invented Brush Boar / Ridge Wolf / Black Bear trio and build The Quiet Mile from three existing D-hunt creatures. That gives the pyramid actual TNR fauna and potentially removes all three new wildlife avatars.

## Verified reusable scene assets

### Existing low-rank mission art

| Asset | Existing use / read | Best reuse |
|---|---|---|
| **DM Long Road Dusk** — `7XdeP3QA1DqHqttxvg2iS` | `The Long Road` | **The Quiet Mile** primary road scene |
| **DM Road Merchant** — `xsikTqetvzo5OXKdTicK6` | `The Long Road` | Optional witness / stranded merchant |
| **DM Mission Counter** — `O2MokayxTOH32-smnzFL2` | D-rank mission framing | Optional pyramid briefing scene |
| **DM Mission Clerk** — `XsLLy8awDAtaE6hXVIi_0` | D-rank mission framing | Optional common briefing NPC |
| **DM Night Walls** — `a9ZwaJtcrwxHS1sJKDsfV` | `Night Watch Shadow` | Night approach / surveillance scene |
| **Genin Trials Case Office** — `_Ca4nBppDdevDwBICFPUF` | Genin case-contract content | Optional connective briefing/debrief |
| **Hall Steps Before Dawn** — `JAh1c6Ykf_nUfM5Xk67DW` | live C-rank Unmarked missions | C-rank briefing / threshold |
| **Market Road Pre-Dawn** — `gXpaJL3VnawaQ5PGqSoAB` | live C-rank investigation | Road / checkpoint investigation |
| **Back Alley Night** — `wyMQkpiugsLs8BQpDdTf2` | live Unmarked encounters | Unmarked surveillance / fight staging |

### Existing approved scene-background reference assets already in the game

- **Pass Road Dusk** — excellent Quiet Mile alternate stage.
- **East Road Ambush Site** — road encounter composition.
- **Waystation Door** — strong False Toll threshold/checkpoint substitute.
- **Drying Shed** — modest rural road structure.
- **Drying Yard** — extremely strong Burned Crest training-yard substitute.
- **Warehouse Loading Floor** — plausible Burned Crest interior/store room.

These are not merely style inspiration; they are captured existing `SCENE_BACKGROUND` game assets and can be literal reuse candidates.

## Revised narrative and encounter plan

### I. The Quiet Mile — Lv15 D

Keep the investigative premise, but make the animals **native TNR hunting fauna**.

The cart is found abandoned along the same kind of trade route already established in `The Long Road`. Wildlife has moved onto the spilled cargo and into the disturbed roadside.

The deeper clue is not a new faction token. A milestone beside the wreck carries a fresh **chalk route mark** like the marks investigated later in `Chalk and Corner`.

The player does not know what it means yet.

**Proposed combat:** three existing D-hunt wildlife AIs, chosen after profile capture.

**Preferred scenes:** DM Long Road Dusk + East Road Ambush Site / Pass Road Dusk.

**New assets if candidates pass capture:** **0**.

### II. The False Toll — Lv20 C

Reframe the tollhouse as a **route-control job run by local muscle for anonymous Unmarked operatives**, rather than a wholly new road-gang faction.

The false toll is valuable because it records who travels, when escorts pass, and which carts can be redirected. The money is useful; the information is the real product.

The player first meets ordinary hired muscle, then discovers the people managing the operation are the same affiliation-less fighters appearing in other C-rank investigations.

**Proposed floors:**
1. **Marauder — Lv25**: local hired muscle.
2. **Unmarked Stray — Lv25**: the first professional cutout.
3. **Marauder + Unmarked Stray**: local crime and professional fieldcraft together.
4. **Unmarked Blade — Lv30**: the operative protecting the ledger / route schedule.

This is not a new difficulty precedent:
- `The Long Road` is D-rank Lv20 and already uses Marauder Lv25.
- `The Empty Contract` is C-rank Lv20 and already uses Unmarked Stray Lv25.
- `Protection` / `The Waystation` are C-rank Lv20 and already use Unmarked Blade Lv30.

**Preferred scenes:** Waystation Door or Drying Shed for the structure; Market Road Pre-Dawn for approach.

**New AI/art required:** **0**.

### III. The Burned Crest — Lv30 C

The training yard becomes an **Unmarked staging yard** rather than a new rogue-shinobi faction.

Old affiliation marks are scraped or burned from gear because the people passing through are expected to become untraceable paid hands. Some are disposable Strays; Blades receive more deliberate training; a Shadow supervises the site.

This adds useful low-level lore: "Unmarked" is not necessarily a village, clan or grand conspiracy. It is a **method of doing deniable work**. The player sees a labor pipeline that explains why the same kind of anonymous operative appears across unrelated C-rank jobs.

**Proposed floors:**
1. **Unmarked Stray — Lv25**
2. **Unmarked Blade — Lv30**
3. **2x Unmarked Stray — Lv25**
4. **Unmarked Stray + Unmarked Blade**
5. **Unmarked Shadow — Lv35** final overseer

The level-35 Shadow is deliberately boss-only. `Chalk and Corner` already uses this exact AI in current C-rank Lv20 content, so a Lv30 capstone use is conservative relative to existing deployment.

**Preferred scenes:** Drying Yard for the exterior/training yard; Warehouse Loading Floor for the interior records/equipment area.

**New AI/art required:** **0**.

## Asset-count consequence

Original bespoke direction implied approximately:

- 10 new enemy avatars;
- 6 new scene backgrounds;
- optional scene characters.

With the reuse direction:

- **False Toll:** 0 new AI, 0 new battle avatars, likely 0 new backgrounds.
- **Burned Crest:** 0 new AI, 0 new battle avatars, likely 0 new backgrounds.
- **Quiet Mile:** potentially 0 new AI/avatars if three D-hunt wildlife candidates pass profile/art verification; 0 new backgrounds.
- Briefing/witness characters can reuse DM Mission Clerk / DM Road Merchant or be omitted.

**Best case: zero new production art.**  
Realistic fallback: **1–2 new assets total**, only if the wildlife art/profile capture shows a mismatch.

## Next evidence gate

Before manifest design is frozen, run one small **read-only** capture containing:

1. the five D-hunt wildlife candidate AIs above;
2. Unmarked Stray / Blade / Shadow (fresh profile confirmation);
3. Marauder (fresh confirmation);
4. the selected scene assets if exact current image/type confirmation is desired.

The Unmarked profile numbers above come from the 2026-09-01 mission-AI audit; the 2026-10-05 quest census proves they are still referenced by live missions but does not prove their profiles were unchanged.

No write manifest should be authored until that reuse capture resolves the wildlife shortlist.
