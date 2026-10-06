# Genin Battle Pyramids — Reuse Audit

**Status:** PROPOSAL / reuse analysis  
**Frozen current main:** `b6f719dc5241f2b4fefc553670a61ea0c4a16d6e`  
**Fresh quest-state evidence:** `harvests/inbox/tnr_results_1791233210169.json` (2026-10-05, DONE/success)  
**AI profile evidence:** `harvests/inbox/tnr_results_1788235198666.json` + `tnr_results_1788235395095.json` (2026-09-01 committed mission-AI audit)  
**Art reference authority:** `skills/producing-tnr-art/data/style_refs.json` + `25x_DATA_art_spec.json`  
**Live requests/writes for this audit:** 0 / 0

## Executive finding

The three Genin pyramids can plausibly be redesigned around existing content with:

- **0 new combat AI records**
- **0 new combat jutsu**
- **0 new scene backgrounds**
- **0 required scene-character assets**
- only a visual QA gate on the reused AI avatars before declaring the art scope truly zero-new

This also creates a stronger lore opportunity: the low-level road incidents can become the player's earliest contact with the **Unmarked** operative layer already used by current C-rank missions, and can foreshadow the higher-rank network currently called **Forsworn** in live mission prose.

Do **not** silently restore `Unwritten` as the current faction name. The repository's old **Unwritten War** document is archived/stale; current live higher-rank mission prose explicitly uses **Forsworn**, while the C-rank enemy line is named **Unmarked**. If the director wants “Unwritten” restored as operative canon, that needs a new lore ruling. Until then, the safest expansion is: **Unmarked = disposable/low-rank outer layer; Forsworn = broader network revealed later**.

## Existing low-rank human AI worth reusing

| AI | Level / Rank | Current low-rank use | Mechanical read | Reuse verdict |
|---|---|---|---|---|
| **GENIN 01** | Lv20 GENIN | D20 *Poachers' Due* | Quick Strike, Steady Strike, Rapid Fire; 1.5x pools; Flaming Sword | Usable, but visually/mechanically generic and flaming weapon may constrain theme |
| **Marauder** | Lv25 CHUNIN | D20 *The Long Road* | Extremely simple; Opening Strike + basic fallback | **Excellent road-criminal grunt** |
| **Syndicate Thief** | Lv27 CHUNIN | D20 *Night Watch Shadow* | No equipped jutsu in Sep-1 audit; default/basic AI behavior | Usable as intentionally basic criminal, but verify current profile before build |
| **Unmarked Stray** | Lv25 GENIN | C20 *The Empty Contract* | Quick/Steady/Bruising + Venom Strike + Fighter's Poise | **Excellent entry Unmarked operative** |
| **Unmarked Blade** | Lv30 GENIN | C20 *Protection*, *The Waystation* | Twin Shot, Enervating, Searing, Heavy Cut, Minor Overflow | **Excellent Lv30 anchor / instructor** |
| **Unmarked Shadow** | Lv35 CHUNIN | C20 *Chalk and Corner* | Withering, Sundering, Numbing, Lingering, Warrior's Poise | Strong capstone; more complex and above Genin cap, but existing C20 precedent proves the game already uses it against lower players |

All three Unmarked records have existing avatars and working AI profiles. Their committed audit shows `statsMultiplier: 1`, `poolsMultiplier: 1`; Stray and Blade are GENIN-ranked and therefore naturally fit this workstream.

## Existing wildlife AI worth reusing

Fresh quest census proves these records are currently referenced by live content:

| AI | Current use | Scaling evidence | Reuse verdict |
|---|---|---|---|
| **Wild Boar** | *The Silent Bloom* | scaled-to-user | **Best Quiet Mile opener** |
| **Dark Wolf** | *Howling Hills* battlepyramid | scaled-to-user | **Strong wolf reuse candidate** |
| **White Wolf** | *Howling Hills* battlepyramid | scaled-to-user | Good alternate/capstone wolf |
| **Grumpy Puppy / Sad Puppies** | old hidden D10 event | fixed | Too comedic / wrong tone |
| **Rabid Puppy** | starter + hidden story content | mixed | Mechanically reusable but narratively poor fit |

Wild Boar / Dark Wolf / White Wolf should be point-read before implementation if fixed-level encounters are desired. If we reuse them **scaled-to-user**, current live quest usage already demonstrates that pattern.

## Scene-background reuse

The current approved TNR reference pack already contains almost exactly the locations needed.

### Quiet Mile
- **Pass Road Dusk** — `nmrMHmz9xWojzyIV2mAR8`
- **East Road Ambush Site** — `E4VJ-IeIQMwbmGGfKc-sn`
- Optional current D-mission asset: **DM Long Road Dusk** — `7XdeP3QA1DqHqttxvg2iS`

These cover road approach, wreck/ambush space, and the grounded rural exterior register.

### False Toll
- **Waystation Door** — `kmDsQUEHSub9GIX5ulO6i`
- **Drying Shed** — `c1e60fERuLUxzt9WY4U37`
- Optional road transition: Pass Road Dusk / DM Long Road Dusk

A tollhouse does not need bespoke architecture if the fiction is an improvised checkpoint built around an old road shed/waystation threshold.

### Burned Crest
- **Drying Yard** — `TUtC7yPymsp2GyWwZhoTf`
- **Warehouse Loading Floor** — `bBV9I0DcmYGcxVGaBdWL0`
- Optional exterior threshold: Waystation Door / Drying Shed

Drying Yard is already the strongest approved visual precedent for a walled work compound and can convincingly become a disused private training yard through prose alone.

## Revised story direction

### Lv15 — The Quiet Mile
Keep the original missing-cart investigation, but make the hidden cause an **Unmarked dead-drop route** rather than a brand-new gang.

Proposed fights:
1. Wild Boar
2. Dark Wolf
3. White Wolf or second Dark Wolf composition

Story:
- A cart is found stripped.
- Animals are scavenging what was deliberately dumped.
- Human cuts / bootprints prove wildlife was secondary.
- The player finds a blank contract chit / unmarked courier token / coded route mark, but no faction name.
- This is a **clue**, not a reveal.

Reuse: 100% existing AI + existing road backgrounds.

### Lv20 — The False Toll
Reframe the toll operation as ordinary criminals being used to service the same anonymous network.

Proposed fights:
1. Marauder
2. Syndicate Thief
3. Marauder + Syndicate Thief
4. **Unmarked Stray** as the collector/handler who arrives when the tollhouse fails

Story:
- The toll gang uses forged authority to collect money and observe traffic.
- Their ledger includes patrol times and scheduled dead drops.
- The final opponent is not the gang leader but the **unmarked collector** who comes for the ledger.
- The player learns the road criminals are disposable infrastructure.

Reuse: 3 existing human AI, all existing avatars, existing road/waystation backgrounds.

### Lv30 — The Burned Crest
Make the training yard explicitly an **Unmarked field school**, where disposable operatives are drilled before being assigned to contracts like the existing C-rank missions.

Preferred no-new-AI ladder:
1. Unmarked Stray
2. Unmarked Stray
3. 2x Unmarked Stray
4. Unmarked Stray + Unmarked Blade
5. **Unmarked Shadow** capstone

Alternative gentler capstone:
- use **Unmarked Blade** as floor 5 and omit Shadow;
- this keeps every enemy at or below Lv30 except repeated Strays.

Story:
- The yard trains nameless cutouts in practical field work: watches, ambushes, escort disruption, evidence removal.
- Burned/scraped markings are not a new faction crest; they are deliberately **removed affiliations**.
- Recovered records can name contract types already seen in *Protection*, *The Empty Contract*, *The Waystation*, and *Chalk and Corner* without requiring those missions as prerequisites.
- The pyramid adds lore by showing **where Unmarked operatives are prepared**, while later higher-rank missions can reveal who pays them.

Reuse: Unmarked Stray / Blade / Shadow + Drying Yard / Warehouse backgrounds. No new combat assets required.

## Lore consequence / recommended ruling

The cleanest canon addition would be:

> **Unmarked operatives are not a separate faction. They are deniable field assets trained and contracted through the same broader network later encountered as the Forsworn. Their lack of affiliation is functional: if captured, they carry no village mark and no organizational insignia.**

This fits:
- the existing names Unmarked Stray / Blade / Shadow;
- existing mission prose built around false contracts, escorts, ledgers and anonymous payments;
- the current Forsworn visual register of dark layered garb without village insignia;
- the user's desire to deepen rather than replace existing low-rank content.

This is still a **proposal**, not operative lore, until approved.

## Art savings

If existing AI avatars pass visual QA:

| Original plan | Reuse-oriented plan |
|---|---:|
| 10 new enemy avatars | **0** |
| 6 new backgrounds | **0** |
| new human faction visual language | **0** |
| new AI kits | **0** |
| new combat AI records | **0** |

The already-approved Wayward Striker generation can remain a **style calibration asset** rather than becoming required production content, unless the director wants one bespoke named instructor.

## Remaining verification before build

1. Fresh point-read Wild Boar, Dark Wolf, White Wolf profiles if we want fixed levels.
2. Fresh point-read Unmarked Stray / Blade / Shadow before manifest construction to confirm Sep-1 profile data has not changed.
3. Visually inspect the existing AI avatars against the current TNR art bible. Mechanics are reusable now; art reuse is not declared final until this check.
4. Decide whether Burned Crest uses Shadow as Lv35 capstone or stays at Blade Lv30.
5. Approve the Unmarked/Forsworn lore relationship before writing it into player-facing prose.
