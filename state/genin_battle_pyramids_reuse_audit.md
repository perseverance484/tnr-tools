# Genin Battle Pyramids — Reuse Audit

**Status:** PROPOSAL / reuse-first redesign  
**Frozen current main:** `b6f719dc5241f2b4fefc553670a61ea0c4a16d6e`  
**Fresh quest-state evidence:** `harvests/inbox/tnr_results_1791233210169.json` (DONE/success)  
**AI profile evidence:** `harvests/inbox/tnr_results_1788235198666.json`, `tnr_results_1789124514980.json`, One Perfect Crop hidden-core/readback records  
**Art authority:** `skills/producing-tnr-art/data/style_refs.json` + `25x_DATA_art_spec.json`  
**Live requests/writes for this audit:** 0 / 0

## Executive finding

The three Genin pyramids can be reoriented around pre-existing TNR content with a realistic target of:

- **0 new scene backgrounds**
- **0 new combat jutsu**
- **0 new lv20/lv30 combat AI**
- **0 new lv20/lv30 enemy avatars**
- likely **0 new lv15 combat art** if approved wildlife / Road Bandit reuse passes final visual QA

The better lore structure is not three unrelated gangs. It is a gradual reveal of the anonymous criminal/operative ecosystem already present in current missions:

**ordinary road incident -> Unmarked field layer -> Faceless / Unsigned professional layer**

This adds context to existing missions without requiring the new pyramids as prerequisites.

## Canon / naming guardrail

Do not silently revive the archived `The Unwritten War` plan. That document is explicitly marked STALE / NON-CANON CANDIDATE.

Current live material uses several distinct terms:

- **Unmarked Stray / Blade / Shadow** — current C-rank enemy records.
- **Unsigned** — current `Witness Detail` prose describes the professional chalk-lane operatives this way.
- **Faceless Stray / Shadow / Blade** — current higher-tier AI usernames.
- **Forsworn** — current higher-rank mission prose uses this broader name, including `Nothing to Report`.

Safest interpretation for these pyramids:

- Unmarked = cheap / deniable outer-layer field assets.
- Faceless / Unsigned = more professional operatives used for sensitive jobs.
- The pyramids should **not** declare either layer to be direct Forsworn members unless dauntless approves that lore relationship.
- If dauntless wants **Unwritten** restored as the umbrella faction name, record a new ruling before final prose.

The new content can establish operational links without prematurely settling the entire organizational chart.

---

## AI reuse inventory

### Low-rank road / generic combat

| AI | Live profile | Current use | Reuse read |
|---|---|---|---|
| **Marauder** `n8EP0t5NN3zhzxXiDdZIY` | Lv25 CHUNIN, 1x/1x, Opening Strike only | D20 `The Long Road`, fixed | Very simple road criminal. Good identity, but too high for fixed Lv15 without scaling. |
| **Syndicate Thief** `97U7ui81xEMFFVz1Isn-z` | Lv27 CHUNIN, 1x/1x, no equipped jutsu in Sep audit | D20 `Night Watch Shadow` | Intentionally basic; usable but profile should be re-read before build. |
| **GENIN 01** `fPHbAdToPNequ4j99Cpxp` | Lv20 GENIN, 1x stats / 1.5x pools | D20 `Poachers' Due` | Valid low-rank human opponent, but generic identity. |
| **Seichi Bandit** `UrAEVY5QvtQqKs-XB92PX` | Lv15 GENIN, no equipped jutsu / no AiProfile | existing generic bandit | Good name/art donor; poor combat reuse as-is. |
| **Road Bandit** `dKEz_VsgZjrfbtxt4ldo8` | technical Lv100 JONIN, simple three-move kit, designed for user scaling | One Perfect Crop | Excellent modern-art / simple-kit reuse if the pyramid fight is scaled. |

One Perfect Crop already has accepted Road Bandit combat art:
`art/one_perfect_crop/one_perfect_crop_road_bandit_avatar.webp`.

### Wildlife

Existing public D-rank hunting creatures include:

- MossWolf — `AkGY27OK7lNmxvGAcGtJr`
- OwlCat — `HS5pnbz_JDK43lNDBEoig`
- Badgertle — `gHPiwKQMYdf5-M1kfdom_`
- Rust Ferret — `R9JRTtK3cZubEWUMbEkfL`
- Moonprowler — `ld7Cd-yHU15NwRKyjToZs`

Other useful existing battle-pyramid ecology:

- Wild Boar — `clik9wzuy000109l650ds0x6x`
- Dark Wolf — current Howling Hills roster
- White Wolf — current Howling Hills roster

**Confirmed art precedent:** One Perfect Crop deliberately reused the existing Wild Boar avatar for Harvest Boar. No new boar image is needed.

Wild Boar / Dark Wolf / White Wolf are the best thematic candidates for Quiet Mile. Point-read profiles before deciding fixed vs scaled use.

### C-rank Unmarked layer

Fresh October census confirms all three are currently used in public C20 missions with `opponent_scaled_to_user: true`.

#### Unmarked Stray — `bCTTWqMLn_clRjR21aB2N`
- Lv25 GENIN
- stats/pools: 1x / 1x
- kit: Quick Strike, Steady Strike, Venom Strike, Fighter's Poise, Bruising Blow
- current use: `The Empty Contract`
- excellent entry operative

#### Unmarked Blade — `JBTjl1mvOWRfTPX0Igj03`
- Lv30 GENIN
- stats/pools: 1x / 1x
- kit: Twin Shot, Enervating Strike, Minor Overflow, Searing Strike, Heavy Cut
- current use: `The Waystation`, `Protection`
- ideal stronger Unmarked / lv30 anchor

#### Unmarked Shadow — `I6bph15IwA0--iAwacxIn`
- Lv35 CHUNIN
- stats/pools: 1x / 1x
- kit: Withering Weave, Sundering Blow, Numbing Shot, Warrior's Poise, Lingering Strike
- current use: `Chalk and Corner`
- more complex capstone; scaled C20 precedent exists

All have existing avatars and working AiProfiles.

### Higher-tier Faceless / Unsigned layer

#### Faceless Stray — `rKWmoT0Ez1q4r8jEqprWP`
- live username: **Faceless Stray**
- Lv40 CHUNIN
- 1.5x stats / 1.5x pools
- kit: Quick Strike, Veilstep, Minor Overflow, Fighter's Poise, Gale Bolt
- current B25 use: `Copies, Not Thefts`, `Witness Detail`
- those missions use it **unscaled**

#### Faceless Shadow — `2ZF5jMvECgiNBgrr4icqk`
- live username: **Faceless Shadow**
- Lv55 JONIN
- 1.5x stats / 1.5x pools
- kit: Lunging Strike, Hushed Hours, Numbing Shot, Marking Volley, Braced Strike
- current B25 use: `Copies, Not Thefts`, `Witness Detail`, `The Loud Way`
- both fixed and scaled precedents exist

#### Faceless Blade — `SJs7nn-cUwy-VtLt_vMwC`
- Lv50 CHUNIN
- 2x stats / 2x pools
- kit: Unraveling Strike, Compression Barrier, Mirror Edge, Heavy Strike, Suppressing Roar, Braced Strike
- current B25 use: `Nothing to Report`
- current battle is **scaled-to-user**
- strongest candidate for a scaled lv30 boss if dauntless wants the professional layer revealed here

Note: the answer catalog still carries old rename-work text for Stray/Shadow, but the committed full captures prove their live usernames are clean: **Faceless Stray** and **Faceless Shadow**.

---

# Reuse-first pyramid redesign

## Lv15 — The Quiet Mile

Preserve the approved investigation premise: wildlife is scavenging a deliberately wrecked cart.

### Recommended zero-new roster

1. **Wild Boar**
2. **Dark Wolf** (or MossWolf if its profile fits better)
3. **Road Bandit** — returning to strip the final cargo / evidence

Why this is stronger than three wildlife fights:
- battle 1–2 make the obvious explanation look plausible;
- the third fight proves a human operation caused the wreck;
- the player still starts with basic threats;
- it directly hands the narrative into False Toll.

Road Bandit is preferred over Marauder if reuse is allowed because its modern accepted art and deliberately simple kit already meet the quality target. Because it is a technical Lv100/JONIN record, reuse it only with `opponent_scaled_to_user: true`.

### Story clue

The bandit carries no faction mark. What matters is a route chit / chalk notation / blank collection instruction that links the sabotage to a larger anonymous logistics system.

Do not name Unmarked/Forsworn yet.

### Asset reuse

Backgrounds:
- Pass Road Dusk — `nmrMHmz9xWojzyIV2mAR8`
- East Road Ambush Site — `E4VJ-IeIQMwbmGGfKc-sn`
- optional Waystation Door — `kmDsQUEHSub9GIX5ulO6i`

Enemy art:
- existing Wild Boar
- existing wolf
- existing Road Bandit

**New production target: 0** if all three avatars pass visual QA.

---

## Lv20 — The False Toll

Reframe the tollhouse as an **Unmarked collection / route-control node**, not an unrelated gang.

### Recommended roster

1. **Unmarked Stray**
2. **Unmarked Blade**
3. **Unmarked Stray + Unmarked Blade**
4. **Unmarked Shadow**

Use scaling, matching their current C20 mission precedent.

### Lore integration

The operation combines practices already shown separately in existing missions:

- anonymous collection/extortion — `Protection`
- road caches / staged route control — `The Waystation`
- blank / deniable contracts — `The Empty Contract`
- chalk timing codes — `Chalk and Corner`

The pyramid's lore contribution is simple:

> These were not four unrelated incidents. The same low-level field network uses collections, caches, route timing and anonymous contracts to service jobs without its crews needing to know one another.

Do not reveal the client/broader faction yet.

### Asset reuse

Backgrounds:
- Waystation Door
- Drying Shed — `c1e60fERuLUxzt9WY4U37`
- Drying Yard — `TUtC7yPymsp2GyWwZhoTf`
- Warehouse Loading Floor — `bBV9I0DcmYGcxVGaBdWL0`
- East Road Ambush Site

Optional recurring civilians, only if they are the same NPCs:
- Keeper — `AM0saNTIIl1FPgc5pAzxc`
- Grain Merchant — `8mDurYQYmy3G0vb862mkO`
- Warehouse Clerk — `1TjPakroW5q8m6nylQRcT`

**New AI/art: 0.**

---

## Lv30 — The Burned Crest

This should now become the **professional-layer reveal**.

The training yard is not a new faction HQ. It is a place where anonymous crews are drilled, briefed or staged by better operators.

### Preferred roster: Faceless / Unsigned escalation

1. **Faceless Stray**
2. **Faceless Shadow**
3. **2x Faceless Stray**
4. **Faceless Stray + Faceless Shadow**
5. **Faceless Blade**

Why this works:
- B25 missions already prove Stray/Shadow in exactly these kinds of counts;
- `Witness Detail` explicitly calls this professional operative ecosystem **the Unsigned**;
- `Nothing to Report` gives us the Faceless Blade as a stronger scaled confrontation;
- no new instructor AI is needed.

### Balance handling

This is still a **C-rank quest**, because GENIN can only start D/C quests even at level 30.

Suggested first-pass behavior:
- Floors 1–4: reuse existing fixed records as B25 missions already do.
- Floor 5 Faceless Blade: scaled-to-user, matching `Nothing to Report`.

If testing says the fixed Faceless floors are too severe or too easy at lv30, change the encounter scaling before cloning new AI.

### Lore contribution

The yard shows an operational hierarchy without over-explaining it:

- Unmarked crews handle cheap, deniable field work.
- Faceless/Unsigned operatives are trained professionals used when a contract matters.
- The burned/scraped crests are removed affiliations, not a new faction insignia.
- Records at the site reference familiar categories: collection, escort disruption, route timing, evidence removal, archive work.
- The player learns the tollhouse crew had professional handlers.

Do **not** state in this pyramid that the Unsigned are direct Forsworn members unless separately ruled. Let the current B-rank missions retain room for that deeper reveal.

### Gentler fallback

If Faceless Shadow/Blade feel too advanced for a Genin pyramid after testing:

1. Unmarked Stray
2. Unmarked Blade
3. 2x Unmarked Stray
4. Stray + Blade
5. Unmarked Shadow (scaled)

This keeps the entire pyramid inside the Unmarked layer.

### Asset reuse

Backgrounds:
- Drying Yard
- Warehouse Loading Floor
- Drying Shed / Waystation Door for exterior threshold

Do not repurpose named Winter Crow / Pale Fang / Old Ghost scene portraits as generic operatives. They remain style references / their own characters.

**New AI/art: 0.**

---

# Production savings

Compared with the original bespoke concept:

| Category | Original | Reuse-first |
|---|---:|---:|
| New enemy AI records | ~10 | **0 target** |
| New enemy jutsu | potentially several | **0** |
| New enemy avatars | ~10 | **0 target** |
| New scene backgrounds | ~6 | **0** |
| New scene-character portraits | several possible | **0 required** |

The approved Wayward Striker generation can remain a **visual calibration asset**. It no longer needs to become production content unless dauntless specifically prefers a bespoke named instructor over the existing Faceless/Unmarked roster.

---

# Required verification before implementation

No new live capture was run for this audit. Before Fable composes the manifest:

1. Point-read current Wild Boar + chosen wolf if fixed-level use is desired.
2. Point-read Road Bandit if cross-content reuse is selected.
3. Point-read Unmarked Stray / Blade / Shadow.
4. Point-read Faceless Stray / Shadow / Blade.
5. Visually inspect each reused avatar against the current TNR art bible; mechanical reuse does not automatically equal visual acceptance.
6. Confirm final lore terminology: keep Unsigned/Forsworn separation, or make a new ruling if `Unwritten` is to become an umbrella name.
7. Playtest / review scaled-vs-fixed encounter choices before rewards are finalized.

## Recommendation

Adopt this reuse-first direction.

It improves the pyramids twice:

- **production:** dramatically fewer new assets and combat records;
- **worldbuilding:** existing D/C/B missions become more connected because the pyramids show the infrastructure behind events players already encounter.

The story ladder becomes:

**The Quiet Mile** — somebody is using the roads.  
**The False Toll** — the Unmarked maintain the anonymous field network.  
**The Burned Crest** — professional Faceless/Unsigned operators stand behind that network.

That is more TNR-native than introducing a separate road gang and a separate rogue-school faction.
