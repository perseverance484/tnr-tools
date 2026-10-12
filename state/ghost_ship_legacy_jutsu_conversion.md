# Ghost Ship / Skyglass — retained jutsu conversion

> **Live baseline (2026-10-12):** the `protectedRecordSha256` values in the JSON packet are the October 1 rows and stay unchanged for the frozen harnesses. The current post-migration-0056 hashes (same method; schema-only delta, no mechanic change) are in `state/ghost_ship_legacy_jutsu_baseline_push86.json`, produced and verified by `harness/ghost_ship_legacy_baseline/`.
>
> **RUL-2026-10-12-010:** Counter Stance (`T3glZGcSd-jS8G-NB43GR`) and Battle Trance (`MG9ZujAV8lK7--YxThVbQ`) are NOT renamed. They keep their live text because 22 AIs outside Ghost Ship equip them. The "Rebounding Form" / "Remembered Form" text below is superseded; the scope is `state/ghost_ship_legacy_jutsu_edit_scope.json`.

**Roster:** eleven existing jutsu approved by dauntless under `RUL-2026-10-11-002`. **Conversion:** names, descriptions and battle text authored; final presentation acceptance remains with the director. Mechanics and IDs are preserved. Fable remains implementation owner; this is a design deliverable, not a Forge manifest.

Canonical text: `state/ghost_ship_legacy_jutsu_conversion.json`. This readable companion reproduces its `after` fields.

## Conversion copy

| Existing name | Skyglass name | Captured Ghost Ship users |
| --- | --- | --- |
| Explosion! | **Core Rupture** | Seal Charge, Core Canister |
| Ghostly Deep Six | **Suppression Writ** | Crowned Captain |
| Ghostly Final Fathom | **Final Command** | Crowned Captain |
| Death's Grasp | **Keelbind** | The Captain, Crowned Captain |
| Ghostly Shipwreck Delusion | **Ruin Refrain** | Crowned Captain |
| Counter Stance | **Rebounding Form** | Oathkeeper, Sentinel, Crowned Captain |
| Death's Door | **Unbroken Command** | The Captain, Crowned Captain |
| Ghostly Crossed Out | **Revocation Strike** | Arsenal Keeper |
| Ghostly Rigging Snare | **Rigging Snare** | Core Horror |
| Ghostly Strangling Weed | **Hollow Timber** | Core Horror |
| Battle Trance | **Remembered Form** | First Blade, The Captain |

### Core Rupture

Existing ID: `nCQETf-HNnbRec1OSY2-R`. Former name: Explosion!.

**Description:** A containment seal ruptures, destroying the casting device in a piercing chakra blast that staggers nearby enemies.

**Battle text:** %user's containment seal splits, consuming the device in a piercing chakra blast that tears through the surrounding battlefield.

### Suppression Writ

Existing ID: `ddbIyVtoxdPQwLRXxSBq8`. Former name: Ghostly Deep Six.

**Description:** A command seal weakens the target's attacks, leaves them more vulnerable, and impairs their healing ability.

**Battle text:** %user casts a suppression writ upon %target, its tightening script dulling their strikes, opening their guard, and disrupting their healing chakra.

### Final Command

Existing ID: `X2P22h8ApDmTZHjWpNO87`. Former name: Ghostly Final Fathom.

**Description:** A crushing command strike disrupts the target's actions and attempts to suppress their bloodline effects.

**Battle text:** %user drives a command seal toward %target with a crushing blow, its flaring script threatening to scatter their rhythm and suppress their bloodline power.

### Keelbind

Existing ID: `PdD44PGaNv4MN5fOALhAF`. Former name: Death's Grasp.

**Description:** Chakra moorings strike and anchor the target while draining health, chakra, and stamina over time.

**Battle text:** %user lashes chakra moorings at %target, the lines closing around their footing as a draining pulse runs through each strand.

### Ruin Refrain

Existing ID: `EQ93LX8wvuIAd5u75q_i1`. Former name: Ghostly Shipwreck Delusion.

**Description:** The ship's remembered destruction erupts across the battlefield as a chakra projection of shattering timbers and staggering impacts.

**Battle text:** %user releases the ship's memory of ruin, sending a storm of fractured timbers and concussive chakra across the battlefield.

### Rebounding Form

Existing ID: `T3glZGcSd-jS8G-NB43GR`. Former name: Counter Stance.

**Description:** A practiced chakra posture returns a portion of incoming direct damage to its source.

**Battle text:** %user settles into a measured form, shaping a retaliatory chakra field that answers incoming blows with returning force.

### Unbroken Command

Existing ID: `0Y10JpChssDwFUxNRk6p3`. Former name: Death's Door.

**Description:** An enduring command imprint sharpens offensive technique and lends greater force to attacks.

**Battle text:** %user draws upon an unbroken command imprint, old orders burning through their reconstructed form as their offensive power rises.

### Revocation Strike

Existing ID: `wMcoazoyXaEXViSCn5weF`. Former name: Ghostly Crossed Out.

**Description:** A strike of seal-marked metal attempts to suppress the target's bloodline effects.

**Battle text:** %user strikes at %target with seal-marked metal, its flaring script seeking to suppress their bloodline power.

### Rigging Snare

Existing ID: `1jXfTgrtGUaSfqTPSSa83`. Former name: Ghostly Rigging Snare.

**Description:** Seal-threaded rigging lashes the target and briefly pins them in place.

**Battle text:** %user lashes seal-threaded rigging at %target, the lines snapping shut around their footing.

### Hollow Timber

Existing ID: `Jz4Lb55NcpwZn3nUK5PrJ`. Former name: Ghostly Strangling Weed.

**Description:** Corrupted wooden growth strikes the target and drains health, chakra, and stamina over time.

**Battle text:** %user drives a surge of hollow timber toward %target, its splintered grain carrying a pulse that drains life, chakra, and stamina.

### Remembered Form

Existing ID: `MG9ZujAV8lK7--YxThVbQ`. Former name: Battle Trance.

**Description:** A preserved combat pattern sharpens the user's strongest offensive discipline.

**Battle text:** %user settles into a remembered combat form, each practiced movement sharpening their offensive technique.

## Preservation and implementation handoff

- Exactly three top-level fields change on each of the eleven existing records: `name`, `description`, `battleDescription`. No global-pool record is renamed. Explosion becomes Core Rupture on its original ID; no duplicate is created.
- The complete original effects arrays remain untouched, including nested placeholder descriptions and absent `generalTypes`. AP, cooldowns, range, target/method, pool costs, modifiers, element filters, effect order, durations and flags are not normalized. Image/animation fields also remain unchanged; any legacy art mismatch belongs to the separate art pass.
- Each conversion includes all matching capture pointers, original text, authored text, captured Ghost Ship users and a SHA-256 digest of every protected field. Replaying the three-field overlay against all matching historical records yielded **11 preserved IDs, 33 text-field changes, zero other field changes**.
- The eleven names are mutually unique and have zero case-insensitive exact collisions across 1491 captured/cataloged jutsu IDs in the listed evidence. This is an offline check, not fresh live uniqueness or dependency certification.
- Historical source: `harvests/inbox/tnr_results_1790826836406.json` (2026-10-01). Fresh operator full captures and an all-consumer audit remain required before edits. Do not overwrite newer mechanics with the old capture or silently retheme unknown external consumers.
- At implementation, Fable must preserve affected equipped links through the repository unequip/edit/re-equip workflow and compare complete post-edit records with the fresh before-images. Hybrid kits and AI rules remain open; these historical users do not authorize adding a retained move to a new enemy.
- Retaining Unbroken Command, Keelbind and Remembered Form also affects the regular Captain. Freeze its revised hybrid kit before final Sealwright parity tests. Sealwright retains all seven approved shared moves, including both Clears.
- No live-game requests/writes, runtime combat tests, engine modifications, art changes, deletion operations or full write manifest are included.

## Wording checks

Semantics were checked against `studie-tech/TheNinjaRPG@cddd7d91c9e6bdebc978ddcb61e5b8a305bd0f93`. These notes explain the wording; they do not modify the captured effects.

| Topic | Wording constraint | Source |
| --- | --- | --- |
| Seal | Suppresses bloodline effects; does not disable every technique. Revocation Strike describes an attempt. | `app/src/libs/combat/tags.ts:2531–2564` |
| Stun | Stagger/action disruption; no promise of complete paralysis or a movement root. | `app/src/libs/combat/tags.ts:2614–2643`; `util.ts:2712–2746` |
| Move Prevent | Only Keelbind and Rigging Snare describe anchoring. No forced pull or teleport. | `app/src/libs/combat/actions.ts:123–138,194–199` |
| Drain | Health/chakra/stamina depletion over time, without healing the caster. Hollow Timber does not claim a root. | `app/src/libs/combat/tags.ts:2026–2094`; `process.ts:973–991` |
| Reflect | Returns a portion of direct damage; does not block or reduce the incoming hit. | `app/src/libs/combat/tags.ts:1753–1784,3364–3404` |
| Damage/stat buffs | Offensive amplification; no resurrection, automatic low-health trigger, defense, speed or regeneration. | `app/src/libs/combat/tags.ts:626–677,3364–3373` |
| Healing suppression | Impairs healing ability; does not claim every heal received from another actor is reduced. | `app/src/libs/combat/tags.ts:1075–1131` |
| Elements | Revocation Strike retains Metal; Hollow Timber retains Wood. Core Rupture does not invent a Fire element. | Captured effect arrays |
| Battle tokens | Only `%user` and `%target`; SELF actions use `%user` only. ALL-method actions avoid singular agreement with a target list. | `app/src/libs/combat/actions.ts:1196–1263` |
