# Silent Bastion — Consolidated Commander Roster, Skills and AI Profiles

> **CURRENT FOUR-COMMANDER PYRAMID — 2026-10-15, RUL-2026-10-15-001.** This dossier retains all **five historical commander designs** as reference, but **The Gatewarden / Outer Garrison is not part of the selected Silent Bastion Pyramid**. Active roster (player-facing Divisions I–IV): **Master of Arms**, **Replicant Zero**, **The Grand Marshal**, **Supreme Commander Arakane**. Their kits, lore and existing approval/candidate distinctions remain unchanged. Total currently listed active kit memberships: **47** (10+11+12+14), not 53. The four full divisions have **16** regular encounter slots, 16–20 fights per winning run, and no outward garrison defenses. The selected `99`-node graph still requires native offline proof; original node counts and numbering in the historic tables below are **not current**. No deleted boss should be silently reassigned to an interior encounter.
>

**Status:** Current design snapshot, **not a live-game implementation, validated rule manifest, or full balance freeze**. Operator owns final balance, prose, rewards, publishing and game actions. This compiles director-approved decisions and explicitly marked candidates; it does not promote unapproved values.
**Repository:** `perseverance484/tnr-tools`; main reference `1da18301e8e4660cedf3daa3e80893a2ac918f2b`; design branch `chatgpt/silent-bastion-design-20261013`; pinned current game source `studie-tech/TheNinjaRPG@c82dc7f8ee76cb9ac498c0689f71b6f13bfe69dd` (rule-limit verification).
**Sources:** `state/silent_bastion_design.md`, `state/silent_bastion_arakane_ai_profile.md`, `skills/building-tnr-content/data/32b_DATA_pool.json` (shared jutsu effects/costs/cooldowns), prior director conversation.
**Naming decision:** Outer Garrison boss **The Gatewarden**, superseding `Garrison Marshal` (2026-10-14).

## Full commander progression

| Division | Encounter | Boss | Jutsus | Status |
| --- | --- | --- | ---: | --- |
| 1 | Outer Garrison · fight 5 | **The Gatewarden** | 6 | Roster accepted |
| 2 | Experimental Armory · fight 10 | **Master of Arms** | 10 | Roster accepted |
| 3 | Skyglass Research Division · fight 15 | **Replicant Zero** | 11 | Roster accepted |
| 4 | High Command · fight 20 | **The Grand Marshal** | 12 | Working kit |
| 5 | Command Sanctum · fight 25 | **Supreme Commander Arakane** | 14 | Roster accepted |

**Total equipped moves listed:** 53 jutsu (6+10+11+12+14, with deliberate reuse of shared-pool jutsu) plus Arakane's equipped **Countermand** item. The **20 regular enemies have not been individually specified**. No enemy stats, pool multipliers, innate IDG, loot, or per-rule executable JSON have been frozen.

**All five commanders:** Innate `sealprevent` **100 power / 99 rounds**. This prevents standard Seal from turning off their passive AI effects; it is not immunity to all control. Custom AI profiles must respect the game's verified **20-rule server cap** (`app/drizzle/constants.ts`, `app/src/server/api/routers/ai.ts` at game head `c82dc7f8ee76cb9ac498c0689f71b6f13bfe69dd`). Unconditional legal fallback required. Project law requires exact single-target range+1 gating. Shared-pool effects below reflect the **pinned registry**, not a fresh live record.

**Effect shorthand:** EP = flat ability damage; IDG = Increased Damage Given; IDT = Increased Damage Taken; DDT = Decreased Damage Taken; DDG = Decreased Damage Given. `/3r` means three rounds, without inventing an unrecorded percent/flat mode. **Pierce and other named effect powers are not ordinary 55/60/80 EP damage**, and should not be described as such.


## 1. The Gatewarden — Outer Garrison · fight 5

**Status:** Combat role and 6-move identity accepted; rename specifically approved 2026-10-14.
**Identity:** Defensive counter / introductory boss.

| Pool | Jutsu | Recorded effect / action parameters |
| --- | --- | --- |
| `B22` | **Compression Barrier** | 40 AP · SELF · CD 5 · absorb 20/3r; DDT 25/3r |
| `B34` | **Mirror Edge** | 60 AP · range 5 · CD 5 · damage 50; reflect 30/2r |
| `B33` | **Piercing Judgment** | 60 AP · range 5 · CD 7 · pierce 55; IDT 25/2r |
| `B28` | **Recoil Slam** | 60 AP · range 5 · CD 5 · damage 75; recoil 15 |
| `B19` | **Warrior's Poise** | 40 AP · SELF · CD 5 · IDG 30/3r; DDT 30/3r |
| `S07` | **Rapid Fire** | 60 AP · range 5 · CD 2 · damage 40 |

### Combat identity and AI priority — The Gatewarden

**Role:** First boss, defensive gatekeeper; deliberately the fairest of five. Punishes careless aggression and shields without sustained lockdown or healing.

**Intended rule priority (profile design, not executable AI JSON):**
1. **Opening:** Compression Barrier to establish Absorb20 + DDT25 for 3 rounds.
2. **Below ~40% HP:** Warrior's Poise (+30 IDG and +30 DDT for 3 rounds).
3. **Opponent has an active shield:** Piercing Judgment to remove it, then resume counterattacking. Its **55 Pierce is not ordinary IDG-scaled damage**.
4. **Against sustained attackers:** Mirror Edge, damaging while reflecting 30 for 2 rounds.
5. **Available high-impact attack:** Recoil Slam (75 EP + recoil).
6. **Fallback:** Rapid Fire (40 EP), chase as required, then safe end-turn.
7. **Restrictions:** No heal, no long Stun/Seal loops; test repeated Barrier/Poise refreshes so he does not stall.

**Division Combat Protocol:** **Fortification Protocol** — short defensive mitigation for boss (DDT proposed; strength/duration not frozen).

## 2. Master of Arms — Experimental Armory · fight 10

**Status:** Name, 10 moves and key combo behavior accepted.
**Identity:** Offensive combos / equipment specialist.

| Pool | Jutsu | Recorded effect / action parameters |
| --- | --- | --- |
| `B33` | **Piercing Judgment** | 60 AP · range 5 · CD 7 · pierce 55; IDT 25/2r |
| `B14` | **Cataclysm Detonation** | 60 AP · range 5 · CD 8 · damage 85 |
| `B28` | **Recoil Slam** | 60 AP · range 5 · CD 5 · damage 75; recoil 15 |
| — | **Tempest Cleave** | 45 EP damage; +35% Increased Damage Taken; 30% Afterburn. Director-supplied existing jutsu. **Exact ID, durations, AP/range/CD not supplied for this design**. |
| `B37` | **Fighter's Poise** | 40 AP · SELF · CD 4 · IDG 15/2r; DDT 15/2r |
| `S07` | **Rapid Fire** | 60 AP · range 5 · CD 2 · damage 40 |
| `B08` | **Tempo Fracture** | 60 AP · range 4 · CD 8 · Time Compression 100/2r |
| `B10` | **Sovereign Ascendance** | 40 AP · SELF · CD 10 · IDG 60/3r; IDG 60/3r; DDT 60/3r |
| `B16` | **Sovereign Fetters** | 60 AP · range 5 · CD 10 · damage 60; stun 100/2r; seal 100/2r |
| `B32` | **Nullifying Wave** | 60 AP · range 5 · CD 8 · Clear 100 |

### Combat identity and AI priority — Master of Arms

**Role:** High-pressure offensive weapons specialist. The major escalation after Gatewarden; combos deliberately **not** spaced apart to make the fight easy.

**Intended rule priority (profile design, not executable AI JSON):**
1. **HP below 60%:** Trigger Sovereign Ascendance (+60 IDG twice and 60 DDT, all for 3 rounds) when ready; do not wait until 35%.
2. **Opponent's positive damage buffs are high:** Nullifying Wave (Clear) on the working **IDG≥71** condition, subject to native condition tests.
3. **Opponent shielding:** Piercing Judgment (55 Pierce; IDT25 for 2 rounds) for defense breaking.
4. **Control combo:** Tempo Fracture (Time Compression100 for 2 rounds; intended to increase jutsu AP costs) and **Sovereign Fetters** (60 EP + Stun2r + Seal2r) as aggressively as available.
5. **Damage setup:** Director-specified **Tempest Cleave** applies IDT35 and Afterburn30; follow with **Cataclysm Detonation** (85 EP).
6. **Remaining offense:** Recoil Slam 75 EP/recoil; Fighter's Poise (+15 IDG/+15 DDT for 2 rounds) and Rapid Fire.
7. **Fallback:** Chase, range-check and end safely. Confirm the exact Tempest Cleave live record before any action-specific rules are authored.

**Division Combat Protocol:** **Weapons Calibration** — temporary offensive IDG to boss, values pending.

## 3. Replicant Zero — Skyglass Research Division · fight 15

**Status:** Name, origin, 11 moves and encounter direction accepted.
**Identity:** Replication, endurance and resource pressure.

| Pool | Jutsu | Recorded effect / action parameters |
| --- | --- | --- |
| `B06` | **Split Image** | 60 AP · GROUND · CD 6 · clone 100/3r |
| `B07` | **Stolen Form** | 60 AP · range 4 · CD 6 · copy 100/3r |
| `B13` | **Hexweave** | 60 AP · range 4 · CD 8 · damage 40; IDT 40/3r; HealGiven- 60/3r; Stats- 15/3r |
| `B15` | **Feast of Marrow** | 60 AP · range 5 · CD 8 · damage 50; drain 100/2r |
| `B22` | **Compression Barrier** | 40 AP · SELF · CD 5 · absorb 20/3r; DDT 25/3r |
| `B23` | **Bulwark Charge** | 40 AP · SELF · CD 6 · IDG 25/3r; shield 100/2r |
| `B29` | **Devouring Wave** | 60 AP · range 5 · CD 6 · damage 55; absorb 15/2r |
| `B34` | **Mirror Edge** | 60 AP · range 5 · CD 5 · damage 50; reflect 30/2r |
| `B35` | **Reaping Strike** | 60 AP · range 5 · CD 5 · damage 50; heal 15 |
| `S35` | **Second Wind** | 40 AP · SELF · CD 6 · heal 15 |
| `S07` | **Rapid Fire** | 60 AP · range 5 · CD 2 · damage 40 |

### Combat identity and AI priority — Replicant Zero

**Role:** The Skyglass scientist who became **its first successfully reconstructed human subject**. His original body died; his preserved chakra impression repeatedly reconstructs itself. First explicit revelation of the human preservation experiment, not undeath.

**Intended rule priority (profile design, not executable AI JSON):**
1. **Opening:** Compression Barrier plus Hexweave when in range.
2. **Round 2:** Split Image **once** (3-round clone); do not repeatedly recast without director reapproval.
3. **Player's IDG high (working threshold≥71):** Stolen Form copies transferable enhancements.
4. **Below ~65% HP:** Bulwark Charge (+25 IDG for 3 rounds, 100 Shield for 2 rounds).
5. **Below ~40% HP:** Second Wind (15 healing) when available.
6. **Resource and sustain cycle:** Hexweave (damage40, IDT40, reduced healing and stats) → Feast of Marrow (damage50, Drain100/2r) → Devouring Wave (damage55, Absorb15/2r); Reaping Strike heals 15 while attacking.
7. **Defensive retaliation:** Mirror Edge (damage50 + Reflect30/2r).
8. **Fallback:** Rapid Fire, approach and safe end-turn.

**Division Combat Protocol:** **Skyglass Barrier** — a temporary shield for boss; durability/timing not frozen. Clone scaling, heals, defenses, and stacking require offline testing.

## 4. The Grand Marshal — High Command · fight 20

**Status:** Name, epithet and role approved. 12-move combat kit and the priority order below are **RATIFIED** (RUL-2026-10-16-006, as natively translated on `claude/silent-bastion-authoring-69za5u`). Stats and balance remain subject to calibration.
**Identity:** Military suppression / control, candidate.

| Pool | Jutsu | Recorded effect / action parameters |
| --- | --- | --- |
| `B03` | **Sovereign Undertow** | 60 AP · range 5 · CD 6 · redirection 3 |
| `B12` | **Sovereign Ruin** | 60 AP · range 4 · CD 10 · DDG 60/3r; DDG 60/3r; HealGiven- 60/3r |
| `B11` | **Sovereign Malediction** | 60 AP · range 4 · CD 10 · seal 100/2r; IDT 60/3r; afterburn 60/3r |
| `B30` | **Suppressing Roar** | 60 AP · range 5 · CD 8 · damage 45; DDG 30/2r; stun 100/1r |
| `S31` | **Unraveling Strike** | 60 AP · range 3 · CD 5 · damage 40; Clear 100 |
| `B32` | **Nullifying Wave** | 60 AP · range 5 · CD 8 · Clear 100 |
| `B17` | **Worldbreaker Chorus** | 60 AP · range 5 · CD 10 · damage 70; stun 100/2r |
| `B14` | **Cataclysm Detonation** | 60 AP · range 5 · CD 8 · damage 85 |
| `B33` | **Piercing Judgment** | 60 AP · range 5 · CD 7 · pierce 55; IDT 25/2r |
| `B23` | **Bulwark Charge** | 40 AP · SELF · CD 6 · IDG 25/3r; shield 100/2r |
| `B22` | **Compression Barrier** | 40 AP · SELF · CD 5 · absorb 20/3r; DDT 25/3r |
| `S07` | **Rapid Fire** | 60 AP · range 5 · CD 2 · damage 40 |

### Combat identity and AI priority — The Grand Marshal ("The Second")

**Character:** The Supreme Commander's highest-ranking subordinate, indispensable strategic deputy, and **only officer permitted to question his orders** because his advice was trusted. Preserves independent tactical judgment. **Name and lore approved; below combat kit is a proposal, not a silently approved freeze.**

**Intended rule priority (profile design, not executable AI JSON):**
1. **Opening suppression:** Sovereign Ruin (two DDG60/3r effects + HealGiven-60/3r) to reduce player offense. **Both DDG effects can compound**; verify extreme mitigation against director balance expectations.
2. **Debuff/effect lockdown:** Sovereign Malediction (Seal100/2r, IDT60/3r, Afterburn60/3r). Neither Ruin nor Malediction does direct damage; AI must not spend an entire fight on setup.
3. **Strong enemy buffs:** Prefer **Unraveling Strike** (range3/CD5, damage40 + Clear100) when close; **Nullifying Wave** (range5/CD8, Clear100) if further away/high IDG. Clear shared cooldown may throttle both; avoid repeated useless Clear.
4. **Anti-kite:** Sovereign Undertow (range5, redirection3) when retreating opponents remain within reach. Must still move if actually beyond its range.
5. **Suppression-to-execute:** Suppressing Roar (damage45 + DDG30/2r + Stun1r) or Worldbreaker Chorus (damage70 + Stun2r), then Cataclysm Detonation (damage85) or Piercing Judgment against shields.
6. **Below ~55% HP:** Switch to proposed **Martial Law** phase — Bulwark Charge for shield/offense and active attack priority; Compression Barrier sparingly for defense.
7. **Fallback:** Rapid Fire, movement, end turn. **No healing.**

**Division Combat Protocol:** Proposed **Countermeasure Protocol = Seal Prevent2r**, but this is **redundant with all bosses' approved innate Seal Prevent99r**. **Must be changed/approved; do not silently implement a nonfunctional option.**

## 5. Supreme Commander Arakane — Command Sanctum · fight 25

**Status:** Name, lore, 14-move membership, signature effects and Countermand identity approved; exact AI profile/ability values still candidates.
**Identity:** Adaptive strategist / desperate final-phase offensive.

| Pool | Jutsu | Recorded effect / action parameters |
| --- | --- | --- |
| `B18` | **Apex Hunger** | 40 AP · SELF · CD 6 · IDG 60/99r; Stats+ 25/99r |
| `B07` | **Stolen Form** | 60 AP · range 4 · CD 6 · copy 100/3r |
| `S34` | **Purging Stance** | 40 AP · SELF · CD 5 · Cleanse 100 |
| `B09` | **Veilstep** | 40 AP · SELF · CD 6 · stealth 100/2r |
| `EA04` | **Zephyr Lance** | 60 AP · range 5 · CD 6 · pierce 60 |
| `B13` | **Hexweave** | 60 AP · range 4 · CD 8 · damage 40; IDT 40/3r; HealGiven- 60/3r; Stats- 15/3r |
| `B17` | **Worldbreaker Chorus** | 60 AP · range 5 · CD 10 · damage 70; stun 100/2r |
| — | **Extermination Order** *(working title; naming not approved)* | **80 EP damage**; Elemental Seal **2 rounds**; Cleanse Prevent **2 rounds**. **Only while Final Stand is actually active**. AP/range/CD and proc chances still unapproved. |
| `B27` | **Scorching Rend** | 60 AP · range 5 · CD 6 · damage 55; wound 15/2r; afterburn 25/2r |
| `B05` | **Devouring Grasp** | 60 AP · range 5 · CD 6 · damage 60; drain 25/2r |
| `B26` | **Braced Strike** | 60 AP · range 5 · CD 5 · damage 55; DDT 30/2r |
| `B20` | **Surging Overflow** | 40 AP · SELF · CD 5 · IDG 30/3r; Stats+ 25/3r |
| `S07` | **Rapid Fire** | 60 AP · range 5 · CD 2 · damage 40 |
| — | **The Last Directive** | Self: **Final Stand 5 rounds**, **Increased Damage Given 5 rounds**, **Clear Prevent 5 rounds**. Trigger under **30% HP**, once. Exact IDG magnitude unspecified. 40 AP / 99-round CD are **proposals**. |

### Combat identity and AI priority — Supreme Commander Arakane

**Character:** Dignified, ruthlessly pragmatic, highly adaptable leader and Skyglass military architect. The Grand Marshal was his closest confidant. **After Arakane falls**, a newly generated directive proves that neither he nor the historical command hierarchy is the ultimate origin of the Ghost Ship's new orders. Protect this surprise before the final scene.

**Approved signature — The Last Directive:** At **under 30% HP**: **Final Stand5r + IDG5r + Clear Prevent5r**. Activation must be given a real chance by pool tuning; don't invent pre-trigger invulnerability. Numeric IDG power and AP/CD are not frozen.

**Exclusive ultimate — Extermination Order (working name):** **80 EP damage + Elemental Seal2r + Cleanse Prevent2r**; only with **actually active Final Stand**. Elemental Seal targets the engine's eligible **60AP elemental jutsu**, not every elemental skill. Native `has_effect` checks need expired-effect boundary validation.

**Approved equipped item — Countermand:** Boss-only, reusable command seal that applies Clear to the enemy. Candidate settings: 40AP, range5, CD6, 100 Clear; confirm item/equipment fields before any manifest.

**Proposed supporting weapons (NOT yet specifically approved):** **Solar Bow** HAND_1: 40AP/range5/CD3; **Crossbow** HAND_2: 40AP/range3/CD0. Both from **historic item seed**, not a fresh capture. Aim is consistent actions during Veilstep's 2-round Stealth (jutsu and basic attacks disabled, equipped items/weapons allowed). Chakra Pill II is only a possibility and its current effects are unverified.

**20 ordered native AI rules — current candidate** (`includeDefaultRules:false`). Self and enemy target selectors/gates must be validated; every single-target range5 action is gated `distance≤6` in AI path units; r4→5, r3→4. This is a design rule sketch referencing real native predicates, not a saved game AI profile.

| # | Conditions | Action |
| ---: | --- | --- |
| 1 | Self HP<30% | **The Last Directive** (self) |
| 2 | Own `finalstand` effect≥1; enemy distance≤6 | **Extermination Order** (enemy) |
| 3 | Round<2 | **Apex Hunger** (self, one opening cast) |
| 4 | Round<5, distance≥7 | **Veilstep** (self, early anti-kite) |
| 5 | Own Stealth effect≥1, distance≤6 | **Countermand** (enemy, item) |
| 6 | Own Afterburn effect≥1 | **Purging Stance** (self, Cleanse) |
| 7 | Target Shield effect≥1, distance≤6 | **Zephyr Lance** (enemy, Pierce) |
| 8 | Target IDG≥71, distance≤5 | **Stolen Form** (enemy, Copy) |
| 9 | Target IDG≥71, distance≤6 | **Countermand** (enemy, Clear) |
| 10 | Distance≤5 | **Hexweave** (enemy) |
| 11 | Distance≤6 | **Worldbreaker Chorus** (enemy) |
| 12 | Distance≤6 | **Scorching Rend** (enemy) |
| 13 | Distance≤6 | **Devouring Grasp** (enemy) |
| 14 | Distance≤6 | **Braced Strike** (enemy) |
| 15 | Distance≤6 | **Rapid Fire** (enemy) |
| 16 | Distance≥7 | **Surging Overflow** (self) |
| 17 | Distance≤6 | **Solar Bow** (enemy, item) |
| 18 | Distance≤4 | **Crossbow** (enemy, item; CD0) |
| 19 | Distance≥3 | **Move toward opponent** |
| 20 | No conditions | **End turn** (fail-safe) |

**Technical gate:** `has_effect` / `target_has_effect` can sum raw stale/uncopyable effects. An inactive Final Stand must NEVER allow the ultimate. No generic strongest-damage rule, which could select it prematurely. Test whether Countermand uses an item slot, succeeds during Stealth, interacts with shared-Clear cooldown, and allows Copy60→Countermand40. Test multi-action AP, movement, range and expiry in offline fixtures before approving any executable profile.

**Division Combat Protocol:** Still **unspecified**; do not invent a name or buff.

## Pyramid and terminal context (approved direction, not full implementation)

- Five divisions × (four regular battles + commander) = **25 fights**, or **20** after five clean shortcuts. Skyglass Signal Beacon is a rare Ghost Ship source and is consumed **once on the first battle of an attempt**.
- Pools carry across victories and division transitions; no automatic full recovery. **Losing fights 1–24** restarts the **current division** with **HP/CP/SP set to 50%**, no extra Beacon. Defeat to Arakane on fight25 (or abandonment) ends the attempt.
- Terminal after the **third regular** encounter offers: **Maintenance Passage** (one logically solvable puzzle; correct→clean skip fourth fight; wrong→still skip with short Security Alert debuff, magnitude tentative); **Medical Protocol** (fight fourth enemy, commander battle starts with pools **fully healed (100%)**, RUL-2026-10-14-001; was 75%); **Combat Protocol** (fight fourth enemy; boss receives temporary division-specific buff; no player recovery). Medical/Combat are chosen in the dialog after the fourth fight.
- Security puzzle themes: patrol-route logic, Armory disable sequence, research original/copy identification, order authorization, historic/new order contradiction.
- Combat Protocol tentative buffs are listed in each boss section. Final numbers not accepted; Grand Marshal's Seal Prevent proposal is a flagged contradiction.
- Future staff/player graphics must show **The Gatewarden**, not `Garrison Marshal`. Never put speculative values or nonapproved art into a "final" publishable poster.
- **No implementation, live requests, credentials, publication or combat balance run is covered by this document.**

## Remaining approval/test work

1. Grand Marshal: ~~ratify twelve moves and exact priority order~~ ratified by RUL-2026-10-16-006; repair redundant Combat Protocol.
2. The Gatewarden/Master/Replicant: author schema-correct ≤20-rule AI profiles and test against verified records; the priorities above are design-level, not actual rule objects.
3. Arakane: verify 20-rule profile against engine and active effects, full Stealth and item loadout behavior, Final Stand/ultimate strict gate, Copy/Clear transfer behavior, and any future director corrections.
4. Freeze **all bosses'** numeric stats, multipliers, protocol effects, AI item records, full jutsu IDs (including director-supplied Tempest Cleave), exclusives' names/range/cooldown/AP/proc chances, and reward/entry economy only with the director.
5. Player narrative/art remain separate from these technical names/effects until accepted. Game actions exclusively user-owned.
