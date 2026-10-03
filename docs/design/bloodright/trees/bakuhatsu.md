# Bakuhatsu — Doctrine of Detonation

**Bloodline:** Bakuhatsu (BR-008, rank A, `RNUcHSH2c00IhOLc2C9aJ`) · **Revision:** Draft 3 / Explosion classification / forked tree · **Classification:** Explosion (element) · **Engine status:** proposal_requires_resolver_adjustment

**Emphasis:** primary Damage (Explosion area attacks) · secondary Afterburn and Increase Damage Taken (Charge 4 Explosion pressure) · tertiary Decrease Damage Taken and Increase Damage Given (Blast Shield / charge buffs).

Three of the eight supported rows are Explosion damage on 60 AP area attacks (Kinetic Nova 50, Inferno Cataclysm 40, Howitzer Crash 40 at jutsu level 25), so burst is the declared role. Charge 4 Explosion carries three supported rows on one 40 AP single-target cast (self Increase Damage Given 35%, enemy Increase Damage Taken 35%, Afterburn 35%, live the two rounds after the cast), which makes it the pressure hub; Howitzer Crash adds a second Increase Damage Given self buff, realized on the caster at cast time and never raising its own hit. Blast Shield's single Decrease Damage Taken row (35%, a caster-only self buff for two rounds) is the only defensive row. There are no heal, lifesteal, reflect or Decrease Damage Given rows, so no sustain or suppression route is invented.

> **Narrow-kit exception:** Nine nodes rather than ten. The kit's five supported tags (Damage 3 rows, Increase Damage Given 2, Increase Damage Taken 1, Decrease Damage Taken 1, Afterburn 1) give three distinct Advanced routes (burst, pressure, fortified). A fourth capstone was available above Powder Keg on Increase Damage Given, but +3 there would push the two-row tag to +8 in a full build, above the reference's +5 for two rows, so the tag is deliberately held at +5 (design note 2); an Increase Damage Taken capstone would sit on the same Charge 4 Explosion cast, target and two-round window as the Afterburn route and duplicate the pressure route rather than add a choice. Powder Keg is kept as a leaf Hidden Art so the burst route has an all-in fourth purchase and the charge buffs have an owner. Three complete builds are distinct.

All nodes cost 1 BP; the budget is 4 BP acquired with silver; each skill is bought once; forks only. Bonuses are static additions to existing supported tags of Explosion-classified Bakuhatsu jutsu under the proposed classification behavior; no row's combat scope changes. Baselines at jutsu level 25.

## Skills

| ID | Skill | Tier | Requires | Exact bonus and recipient | Coverage (jutsu / rows) |
|---|---|---|---|---|---|
| 01 | Primed Fuse | Foundation | None | +2% Increase Damage Given (self buff); +2% Increase Damage Taken (enemy debuff) | Charge 4 Explosion, Howitzer Crash / 3 |
| 02 | Shaped Charge | Hidden Art | Primed Fuse | +2 Damage power (damage) | Howitzer Crash, Inferno Cataclysm, Kinetic Nova / 3 |
| 03 | Ground Zero | Advanced Art | Shaped Charge | +3 Damage power (damage) | Howitzer Crash, Inferno Cataclysm, Kinetic Nova / 3 |
| 04 | Powder Keg | Hidden Art | Primed Fuse | +3% Increase Damage Given (self buff) | Charge 4 Explosion, Howitzer Crash / 2 |
| 05 | Smoke and Shrapnel | Foundation | None | +2% Decrease Damage Taken (self buff); +2% Afterburn (enemy debuff) | Blast Shield, Charge 4 Explosion / 2 |
| 06 | Hardened Casing | Hidden Art | Smoke and Shrapnel | +3% Decrease Damage Taken (self buff) | Blast Shield / 1 |
| 07 | Siege Battery | Advanced Art | Hardened Casing | +5% Decrease Damage Taken (self buff); +2% Increase Damage Given (self buff) | Blast Shield, Charge 4 Explosion, Howitzer Crash / 3 |
| 08 | Slow Burn | Hidden Art | Smoke and Shrapnel | +3% Afterburn (enemy debuff) | Charge 4 Explosion / 1 |
| 09 | Chain Reaction | Advanced Art | Slow Burn | +5% Afterburn (enemy debuff); +3% Increase Damage Taken (enemy debuff) | Charge 4 Explosion / 2 |

Connections: 01→02, 02→03, 01→04, 05→06, 06→07, 05→08, 08→09. Advanced Arts: 3; any two cost at least 5 BP including prerequisites (cap 4); maximum affordable Advanced Arts: 1.

- **Primed Fuse** — Every detonation begins as a held breath and a lit fuse. Charge 4 Explosion and Howitzer Crash self buffs (35→37%); Charge 4 Explosion exposure debuff (35→37%). 3 rows, no gates.
- **Shaped Charge** — The blast is not larger; it is aimed. Inferno Cataclysm, Kinetic Nova and Howitzer Crash Explosion damage (40/50/40 → 42/52/42 power). 3 area rows, all 60 AP, cooldown 7.
- **Ground Zero** — Where the charge lands, the map is redrawn. The same three Explosion damage rows; with Shaped Charge the route adds +5 power (Kinetic Nova 50→55, Cataclysm and Howitzer 40→45).
- **Powder Keg** — The body is a magazine; patience is the match. Both Increase Damage Given self buffs (35→38%, 40% with Primed Fuse): Charge 4 Explosion and Howitzer Crash, each realized at cast time.
- **Smoke and Shrapnel** — The blast is over. Its cloud and its fragments are not. Blast Shield damage reduction (35→37%; caster-only self buff, 2 rounds) and Charge 4 Explosion Afterburn (35→37%). 2 rows, 40 AP each.
- **Hardened Casing** — Debris packs into a wall that holds the second time, too. Blast Shield Decrease Damage Taken only (single caster-only row, 2 rounds per 40 AP cast): 35→38% alone, 40% with Smoke and Shrapnel.
- **Siege Battery** — Dug in behind the blast wall, the battery keeps firing. Blast Shield reduction route total 45%; both Increase Damage Given rows +2 (Charge 4 Explosion, Howitzer Crash: 37%, 39% with Fuse).
- **Slow Burn** — Shrapnel lodges hot and stays hot. Charge 4 Explosion Afterburn only (single target, range 4, 40 AP, 2 rounds): 35→38% alone, 40% with Smoke and Shrapnel.
- **Chain Reaction** — One blast primes the next. Nothing lands only once. Charge 4 Explosion Afterburn route total 45% and its exposure +3 (38%, 40% with Primed Fuse); one 40 AP cast raises both debuffs.

## Complete four-purchase examples

| Build | Purchases | DMG | IDG | IDT | DDT | AB |
|---|---|---:|---:|---:|---:|---:|
| Ground Zero (Burst) | Primed Fuse, Shaped Charge, Ground Zero, Powder Keg | +5 | +5% | +2% | — | — |
| Chain Reaction (Pressure) | Smoke and Shrapnel, Slow Burn, Chain Reaction, Primed Fuse | — | +2% | +5% | +2% | +10% |
| Siege Battery (Fortified) | Smoke and Shrapnel, Hardened Casing, Siege Battery, Primed Fuse | — | +4% | +2% | +10% | +2% |

Abbreviations: DMG = Damage · IDG = Increase Damage Given · IDT = Increase Damage Taken · DDT = Decrease Damage Taken · AB = Afterburn. Values are per-matching-row static additions, not final combat percentages.

- **Ground Zero:** The +5 power route on all three Explosion area attacks (Kinetic Nova 55, Inferno Cataclysm and Howitzer Crash 45) plus Primed Fuse. Powder Keg is the all-in fourth purchase: both Increase Damage Given self buffs reach 40%. Cast Charge 4 Explosion and Howitzer Crash (100 AP) in one round; a Kinetic Nova in either of the next two rounds gains 80% of staged base from the two buffs (additive) plus the 37% exposure. Smoke and Shrapnel (Blast Shield 37%, Afterburn 37%) is the balanced alternative.
- **Chain Reaction:** Charge 4 Explosion becomes the whole plan: Afterburn 45% (Shrapnel 2, Slow Burn 3, Chain Reaction 5) and exposure 40% (Fuse 2, Chain Reaction 3) on one 40 AP cast; in the two rounds after it, every non-pierce hit the target takes, from the caster, allies or weapons, is burned by Afterburn, and raised by the exposure when the hit is Earth, Explosion, Lightning or element-less. Primed Fuse is the fourth purchase because it adds the self buff (37%) and completes the exposure; Hardened Casing (Blast Shield 40%) is the defensive alternative.
- **Siege Battery:** Blast Shield's reduction rises to 45% on the caster (a self buff live the two rounds after each 40 AP cast; allies do not receive it), and Siege Battery's +2 Increase Damage Given keeps the self buffs at 39% with Primed Fuse, so the shielded caster still amplifies a Nova cast after the charge round. Primed Fuse also brings the 37% exposure; Slow Burn (Afterburn 40%) is the alternative fourth purchase for a bunker that still burns.

## Before/after effect rows

| Jutsu | Row | Tag | Recipient | Base | Burst | Pressure | Fortified |
|---|---:|---|---|---:|---:|---:|---:|
| Inferno Cataclysm | 0 | Damage | enemy | 40 | 45 (+5) | 40 | 40 |
| Inferno Cataclysm | 1 | recoil (unsupported) | enemy | 40% | 40% | 40% | 40% |
| Kinetic Nova | 0 | Damage | enemy | 50 | 55 (+5) | 50 | 50 |
| Kinetic Nova | 1 | wound (unsupported) | enemy | 25% | 25% | 25% | 25% |
| Blast Shield | 0 | Decrease Damage Taken | self | 35% | 35% | 37% (+2) | 45% (+10) |
| Blast Shield | 1 | barrier (unsupported) | self | 100 | 100 | 100 | 100 |
| Charge 4 Explosion | 0 | Increase Damage Given | self | 35% | 40% (+5) | 37% (+2) | 39% (+4) |
| Charge 4 Explosion | 1 | Increase Damage Taken | enemy | 35% | 37% (+2) | 40% (+5) | 37% (+2) |
| Charge 4 Explosion | 2 | Afterburn | enemy | 35% | 35% | 45% (+10) | 37% (+2) |
| Howitzer Crash | 0 | Damage | enemy | 40 | 45 (+5) | 40 | 40 |
| Howitzer Crash | 1 | move (unsupported) | self | 1 | 1 | 1 | 1 |
| Howitzer Crash | 2 | Increase Damage Given | self | 35% | 40% (+5) | 37% (+2) | 39% (+4) |

## Allocation audit

- Legal prerequisite-closed allocations by size: 0: 1, 1: 2, 2: 5, 3: 9, 4: 12
- Full-budget allocations: 12; numerically non-dominated (per-tag totals): 12; all nodes appear in a non-dominated build: True
- Maximum individually achievable additions: Damage +5, Increase Damage Given +5%, Increase Damage Taken +5%, Decrease Damage Taken +10%, Afterburn +10% (not jointly attainable)
- Supported rows in kit: 8 (AB 1, DMG 3, DDT 1, IDG 2, IDT 1)
- Strongest full build by row-weighted total: Primed Fuse, Shaped Charge, Ground Zero, Powder Keg (raw +12, row-weighted 27)
- Lowest row-weighted node: Hardened Casing (3)

### All legal full-budget allocations

| # | Nodes | Bonuses |
|---:|---|---|
| 1 | Primed Fuse, Shaped Charge, Ground Zero, Powder Keg | DMG +5, IDG +5, IDT +2 |
| 2 | Primed Fuse, Shaped Charge, Ground Zero, Smoke and Shrapnel | DMG +5, IDG +2, IDT +2, DDT +2, AB +2 |
| 3 | Primed Fuse, Shaped Charge, Powder Keg, Smoke and Shrapnel | DMG +2, IDG +5, IDT +2, DDT +2, AB +2 |
| 4 | Primed Fuse, Shaped Charge, Smoke and Shrapnel, Hardened Casing | DMG +2, IDG +2, IDT +2, DDT +5, AB +2 |
| 5 | Primed Fuse, Shaped Charge, Smoke and Shrapnel, Slow Burn | DMG +2, IDG +2, IDT +2, DDT +2, AB +5 |
| 6 | Primed Fuse, Powder Keg, Smoke and Shrapnel, Hardened Casing | IDG +5, IDT +2, DDT +5, AB +2 |
| 7 | Primed Fuse, Powder Keg, Smoke and Shrapnel, Slow Burn | IDG +5, IDT +2, DDT +2, AB +5 |
| 8 | Primed Fuse, Smoke and Shrapnel, Hardened Casing, Siege Battery | IDG +4, IDT +2, DDT +10, AB +2 |
| 9 | Primed Fuse, Smoke and Shrapnel, Hardened Casing, Slow Burn | IDG +2, IDT +2, DDT +5, AB +5 |
| 10 | Primed Fuse, Smoke and Shrapnel, Slow Burn, Chain Reaction | IDG +2, IDT +5, DDT +2, AB +10 |
| 11 | Smoke and Shrapnel, Hardened Casing, Siege Battery, Slow Burn | IDG +2, DDT +10, AB +5 |
| 12 | Smoke and Shrapnel, Hardened Casing, Slow Burn, Chain Reaction | IDT +3, DDT +5, AB +10 |

## Design notes

- Node split: the roots mirror the two support casts. Primed Fuse (both IDG self buffs, Charge 4 Explosion's exposure) forks into the Damage route (Shaped Charge → Ground Zero) and the leaf Powder Keg. Smoke and Shrapnel (Blast Shield reduction, Charge 4 Explosion Afterburn) forks into Fortify (Hardened Casing → Siege Battery) and Pressure (Slow Burn → Chain Reaction). The 'AoE Control' trait lives in unsupported rows (recoil, wound, barrier, move) and area shapes, which no node changes.
- Reference reuse: flats copy Taiyo Kami nearly verbatim (Primed Fuse = Dawnheart +2 IDG/+2 IDT; Shaped Charge → Ground Zero = Crown of Cinders → Solar Cataclysm, +5 Damage on three rows; Hardened Casing = Golden Mantle; Siege Battery ≈ Sovereign Sun) because the row pattern matches. Departures: no DDG rows, so Smoke and Shrapnel pairs DDT with Afterburn, run 2/3/5 to +10 (Taiyo 3/7); Powder Keg (+3 IDG leaf) replaces Emberwake; Battery's IDG is +2 (Taiyo +3), below Keg; IDT tops at +5 (Taiyo +7).
- Filters/passives: both IDG rows filter the Highest stat, no element, so they raise every element-less hit of any stat type and Highest-stat elemental hits; the exposure row lists Earth/Explosion/Lightning/None; Afterburn and Blast Shield rows take every non-pierce hit. The bloodline IDG passive (25% + 0.15/level, Lightning/Earth/Explosion/None) multiplies the enhanced Explosion damage rows beside the additive jutsu IDG rows; the Earth-only 15% DDT passive does not touch Blast Shield's row.
- Delivery and uptime: all five jutsu have cooldown 7. Damage casts cost 60 AP (Inferno Cataclysm spiral of radius 4 around the caster; Kinetic Nova circle spawn on a target, range 4; Howitzer Crash circle spawn on empty ground, range 5, moving the caster). Charge 4 Explosion: 40 AP, single target, range 4. Blast Shield: 40 AP. Every buff and debuff row is live only in the two rounds after its cast; the SELF rows (both IDG, Blast Shield's DDT) land on the caster at cast, not through tiles.
- Fourth purchase choices: Burst takes Powder Keg (Increase Damage Given +5 total, all-in) or Smoke and Shrapnel (reduction +2, Afterburn +2); Pressure takes Primed Fuse (self buff +2, exposure +5 total) or Hardened Casing (reduction +5); Fortified takes Primed Fuse (self buff +4, exposure +2) or Slow Burn (Afterburn +5). Hybrids with no Advanced Art (Fuse, Keg, Shrapnel, Casing) spread smaller gains across four tags. Keg and Battery cannot be bought together (5 BP), keeping the two-row tag at +5.
- Stacking (§3b): same-tag effects from different jutsu or casters all apply and add. Howitzer Crash plus Charge 4 Explosion in one 100 AP round leaves both IDG self buffs live for the next two rounds: 74% of staged base with Fuse, 78% with Fuse and Battery, 80% with Fuse and Keg. Cooldown 7 exceeds each two-round window, so one jutsu's windows never overlap. An ally's IDT or Afterburn on the charged target adds to the exposure and Afterburn (Afterburn capped at 60% per hit).

## Risks and unproven interactions

- Single-cast concentration: Chain Reaction raises both Charge 4 Explosion debuff rows (Afterburn 45%, exposure 38–40%) and Primed Fuse / Powder Keg / Siege Battery raise its self buff, so one 40 AP C-rank cast can carry three enhanced rows at once. Per-AP value of that cast rises more than the 60 AP damage route's; no combat simulation was run.
- Leakage: the enhanced Increase Damage Given rows add their percentage of staged base to every caster hit (jutsu, weapon, basic attack) passing their Highest-stat or element-less filter; the exposure and Afterburn debuffs raise damage dealt by allies and weapons to the charged target; Blast Shield's enhanced reduction is caster-only. Casting scope does not restrict downstream benefit.
- Afterburn value is downstream: it depends on how many non-pierce hits the charged target takes during the two-round window, and cumulative Afterburn per hit is capped at 60% of that hit, so a 45% debuff leaves only 15 points for any other Afterburn source. Pierce hits are skipped by Afterburn and by the exposure modifier alike.
- Howitzer Crash delivery: its Increase Damage Given row is SELF, realized on the caster at cast and live the two rounds after; not positional, never on allies, so Powder Keg and Siege Battery values on it need only an empty tile in range 5 (Charge 4 Explosion's need a living non-caster target). Its damage row (ENEMIES) and unsupported move row (Enemy hazard) are tile-delivered INHERIT rows.
- Friendly fire: damage rows are ENEMIES-only, so the Damage route never raises damage to allies; Kinetic Nova's unsupported wound row (ally hazard) is untouched. Charge 4 Explosion may be aimed at an ally (OTHER_USER): its enhanced exposure and Afterburn then land on the ally, the self buff still on the caster. Blast Shield's unsupported barrier row reaches anyone on its tiles, enemies included.
- Classification: the Explosion label collides with Bakuhatsu Suru Nendo (DEFER) in the census and the normal-jutsu collision is unverified, so eligibility must be bloodline-scoped, not a bare element match. Under the current resolver only 4 of 8 supported rows (three damage rows, the exposure row) match Explosion directly; both self buffs, the Afterburn row and the shield row fall back to None.
- Both Increase Damage Given rows and Blast Shield's reduction are percentage rows at 35% base; the route maxima (40% and 45%) are far from the 100 cap, but each is live only in the two rounds after its cast, so realised uptime, not the flat, decides their value.
- Ranked PvP and ranked sparring suppress skill-tree effects at the pin, so the whole tree is inert there. Normal-tree potency policy is not approved; a combined stacking audit is still required before any implementation.

## Limits

- Proposed potency classification behavior; not implemented or verified in the live engine.
- All existing supported tags of Bakuhatsu jutsu inherit Explosion potency eligibility; original combat elements and target scopes stay intact.
- Every matching row on a jutsu receives each matching modifier; repeated rows are counted separately.
- Damage values are raw power, not final-damage percentages; percentage-valued tags are capped at 100.
- Afterburn is an enemy debuff: for its existing duration, damage the target takes causes extra Afterburn damage at its percentage (60% cap per hit). It is not itself a damage instance; downstream instances were not simulated.
- Unsupported tags (e.g. wound, shield, stun, pierce, absorb, poison, drain, summon) receive no bonuses.
- No combat simulation. Budget and numerical non-dominance checks do not establish equal combat strength.
- Main-tree effects, bloodline passives, equipment, AP, uptime and modifier delivery are outside this audit.

