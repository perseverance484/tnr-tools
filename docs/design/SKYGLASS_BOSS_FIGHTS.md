# Skyglass boss fights: The Captain, the Core Horror, the Crowned Captain

A full design pass to make these three fights memorable. Director, 2026-10-28: "named jutsu, animations, mechanics, anything
and everything we've got". This file owns the fight design. Inputs:
- the approved structure, numbers and toolkit: `SKYGLASS_WRECK_ENCOUNTERS.md`;
- names and voice: `SKYGLASS_STORY_BIBLE.md`;
- animation ids and readability rules: `SKYGLASS_BOSS_ANIMATIONS.md`.

Jutsu are **one shared set**: the hunts, both Wreck versions and Crownhold use the same jutsu and rules, and the live
crew records are upgraded in place. AI records differ only in stats. The canonical statement is §5.

## The tools we have (engine-checked unless marked PROBE)

| Tool | Engine | Use |
|---|---|---|
| Marked set piece | visual ground mark (40 AP, puts a 1-round marker on the boss), then a 100 AP detonation next turn gated on that marker (library_spec.json 5f6c3edb) | the core of every boss |
| Fixed patterns | COORDINATES: caster rings and lines, arena-wide EXCLUDE with safe hexes; one offset set per row parity | readable shapes |
| Two-marker chains | marker A sets up a 40 AP follow-up that applies marker B; B detonates next turn | PROBE: combos such as "mark, then drag into it" |
| Pull / push | `redirection` pull or push N hexes (blocked by a root) | Undertow, Bell Toll |
| Exposed window | `weakness` on SELF: x2-x50 damage taken from chosen generals, elements, jutsu or items | PROBE (self-target): "hit him now" windows after big attacks |
| Player-granted action | `injectjutsus` adds jutsu to a unit's action list while it lasts | PROBE: a ground effect granting it to whoever stands there |
| Barrier | `barrier` tag: a wall with its own HP bar, absorb % and sprite | the Captain's gunwale |
| Summon | one live summon per caster; any AI record | Recall, All Hands |
| Clone | `clone`: a full-HP copy for 2+ rounds (hits weakly, cause untraced) | decoys |
| Cooldown pressure | `increasecooldown`, `timecompression` (+10 AP per action) | tempo attacks |
| Stealth, reflect, mirror, copy | as live | the duelist's tricks |
| Voice | every jutsu's `battleDescription` prints in the battle log | the bosses talk mid-fight |
| Phase gates | `health_below`; `has_effect` on a phase marker | clean three-act fights |

Readability rules come from the animation spec. Every set piece has a mark (tg_*) and a payoff (dt_* or the boss's own
animation). Every boss line is short.

---

## 1. The Captain: "The Echo at the Helm"

*Skyglass Wreck, floor 5, wave 2, with the Sealwright. Harness: 12,625 HP, three +100% rows.*

**Fantasy.** A naval commander still running the ship's last battle: bells, broadsides, banners, discipline. He wears his
master's mask and fights like a man who has done this ten thousand times. **Theme of the fight:** command. He makes the
deck itself attack you, and the Sealwright keeps him standing.

**Arena:** the deck. The Captain holds a short patrol line and stays near his Sealwright.

**The kill-order puzzle:** the Sealwright's **Ward of Command** on the Captain. While the Sealwright lives, the Captain carries a
visible command banner (cp_command aura) and takes heavily reduced damage. Kill the Sealwright first, or fight through the
ward. The Sealwright's **Mending Seal** keeps the Captain topped up.

| Move | Kind | What it does | Mark / animation | Counterplay |
|---|---|---|---|---|
| **Hold the Line** | opener, self | Unbroken Command: +damage and stats for the fight; once | cp_command flourish | none; it marks the fight's start |
| **Broadside** | set piece | Marks two full rows of the arena red; next turn the ship's guns fire down them. Heavy damage | tg_heavy rows, then dt_heavy plus a cannon-flash variant | step to an unmarked row |
| **Ship's Bell** | set piece | Violet ring (radius 2) around him; next turn the bell tolls: push 3 and the set-piece lock (RUL-2026-10-28-015: `elementalseal`, `timecompression` +10 AP on every jutsu, `increasecooldown` +2 on Move and Replacement Technique) for 1 round | tg_control, then cp_bell_toll shockwave | leave the ring, or be thrown and locked |
| **Keelbind** | duel | Range-5 root and drain on the player with the most aggro; stops Replacement Technique | chain-wrap hit | cleanse, or stay close |
| **Final Command** | duel | Damage, a 3-round stun and a seal; his finisher | crimson strike | do not stand stunned next to him |
| **Raise the Gunwale** | utility | A barrier line between the players and the Sealwright; the barrier has its own health | timber-and-seal wall sprite | break it, or go around |
| **Last Stand at the Helm** | phase, under 50% | Battle Trance once, Broadside marks three rows, Ship's Bell comes faster | cc_phase_shift flash, recoloured | the fight speeds up |

**Battle log (his voice):**
- Hold the Line: "%user plants his blade on the deck. \"Hold the line.\""
- Broadside: "%user raises a hand. \"Run out the guns.\"" / "\"Fire.\""
- Ship's Bell: "\"All hands.\" The great bell answers."
- Final Command: "\"Stand down.\""
- Under 50%: "\"I have held this deck through worse than you.\""

---

## 2. The Core Horror: "What the Core Remembers Wrong"

*Skyglass Wreck, floor 4, alone. Harness: 25,250 HP, two +100% rows. Round target: pending harness rerun (retuned by
RUL-2026-10-28-008).*

This is the one canonical Core Horror kit. The two kit descriptions in `SKYGLASS_WRECK_ENCOUNTERS.md` (Rending Claw /
Bile Spit, and Rot Glyph / Horror Wail) are superseded.

**Fantasy.** A crew member the Core could not rebuild properly, now a mass of timber, rope, seawater and skyglass with a
half-remembered man somewhere inside. It never speaks. **Theme of the fight:** the ship itself is the boss. Every attack
comes out of the floor.

**Arena:** the flooded hold. He is rooted in the middle of it and never moves.

| Move | Kind | What it does | Mark / animation | Counterplay |
|---|---|---|---|---|
| **Splintered Grasp** | plain | Heavy melee and a wound (bleed) | ch_claw | do not stand next to him unprepared |
| **Bilge Spit** | plain | Range 4: damage and a poison (punishes chakra/stamina spent) | ch_bile_spit | spread out; cleanse |
| **Collapse** | set piece | Red ring (radius 2) around him; next turn the deck caves in | tg_heavy, then ch_collapse | step out of the ring |
| **Undertow** | set-piece add-on | During a Collapse mark: the farthest player is pulled 3 hexes toward him, into the ring | water-drag streak | PROBE two-marker chain; a root or a cleanse-ready ally saves you |
| **Rupture Field** | set piece | One of three fixed scatter patterns, rotating; next turn the rot erupts | tg_heavy, then ch_rupture | read the field and stand clear |
| **Maw of the Deep** | set piece, signature | Whole arena red except three cyan stars; next turn black water and teeth rise everywhere else. Once per phase | tg_heavy field, tg_safe stars, then ch_maw | reach a star |
| **Exposed Seam** | window | After the Maw resolves he splits open: for 1 round he takes x3 damage | ch_exposed glowing seam | burst him now (PROBE: weakness on SELF) |
| **The Core Rebuilds** | phase, under 50% | Heals once (a modest amount) and enrages. Rupture Field leaves lingering pools; set pieces come one round sooner | ch_enrage aura | pools punish standing still |

**The fight's rhythm:** plain hits, a mark, the dodge, a punish window after the Maw. He is the floor where players learn
the marks before the final bosses.

---

## 3. The Crowned Captain: "I control... many echoes"

*Crownhold, the last fight, solo. A hard win that fails if the marks are ignored. Crownhold carries HP between fights, so
he is tuned as the end of the chain (RUL-2026-10-28-013); HP doubled (RUL-2026-10-28-008). Round target: pending harness
rerun.*

**Fantasy.** The source of every echo. He has never left his throne room and never needed to. Calm, certain, faintly
amused. He believes he gave his people a gift. **Theme of the fight:** command over everything. Phase 1 he duels you
himself; phase 2 his echoes fight for him; phase 3 his crown fights for him.

**Arena:** the throne room. He stands at the throne, which keeps his patterns aligned.

| Move | Kind | What it does | Mark / animation | Counterplay |
|---|---|---|---|---|
| **The Crown's Will** | aura | Frost points and armour crystals glinting (phase 1-2) | cc_crown_aura | none; it tells you which phase you are in |
| **Final Command** | duel | Damage, a 3-round stun and a seal | crimson strike | do not stand stunned in his reach |
| **Keelbind** | duel | Range-5 root and drain | chain-wrap hit | stops kiting; cleanse |
| **Ruin Refrain** | duel | Hits every player, with a 2-round stun | cc_phase_shift-style pulse | stun immunity, or accept it |
| **Hexweave** | setup | +damage taken and -heal on the player | violet sigil | cleanse it before Final Command |
| **Crownfall** | set piece | A red fan of lines from the throne; next turn crown shards fall along them | tg_heavy lines, then cc_crownfall | step between the lines |
| **Recall** | phase 2 | One echo of a Crownhold officer you already beat rises; recast when it falls | cc_recall | kill it fast, or tank it and focus him |
| **Command Absolute** | set piece, phase 2 | Violet over the whole arena except three stars; next turn every unsafe hex takes the set-piece lock (RUL-2026-10-28-015: `elementalseal`, `timecompression` +10 AP on every jutsu, `increasecooldown` +2 on Move and Replacement Technique) for 2 rounds | tg_control field, tg_safe, then cc_command_absolute | reach a star |
| **Stolen Form** | phase 2 | Copies your buffs | mirror flicker | buff after it, not before |
| **Extermination Order** | phase 2-3 | Damage, an elemental seal and a cleanse-prevent | crimson sigil | expect it once he has the Last Directive |
| **The Last Directive** | phase 3, under 30% | He cannot fall for 5 rounds; damage up | cc_last_directive blaze | survive it |
| **Shardstorm** | set piece, phase 3 | Every round, one of three rotating scatter patterns rains crown shards; the safe hexes move each turn | tg_heavy field, then cc_shardstorm | keep moving to the clear hexes |

**Last Directive** keeps its clearprevent (director, 2026-10-28). Its five rounds are a pure survival test through
Shardstorm; he falls when it ends.

**Battle log (his voice):**
- Opening: "%user does not rise. \"Another echo come home.\""
- Recall: "\"Stand, soldier.\" An echo rises at his word."
- Command Absolute: "\"Kneel.\""
- The Last Directive: "\"Preserve command.\" The crown blazes."
- Defeat text: the aftermath dialog takes over (Crownhold d.aftermath).

---

## 4. The hunt bosses

Director, 2026-10-28: the hunts use these enemies, not weaker versions, and their bosses play like the PoE fights above.
Each gets at most two marked set pieces and one window, to keep the jutsu count down.

### 4a. The Foundry Warden: "The Last Pour" (Drowned Foundry, solo, with a Core Canister)

**Fantasy.** A master smelter fused with his pouring frame, standing in the one dry room of a flooding foundry. Molten
skyglass on one side, seawater on the other. **Arena:** the crucible chamber. He never leaves the crucible.

| Move | Kind | What it does | Mark / animation | Counterplay |
|---|---|---|---|---|
| **Pour Line** | set piece | Marks a straight channel from the crucible across the floor; next turn molten skyglass runs down it: heavy damage, and the channel keeps burning for 2 rounds | tg_heavy line, then fw_pour, leaving a tg_linger-style burning glass tile | stay out of the channel, and remember where it burns |
| **Quench** | set piece, signature | Marks the whole floor except three cooled tiles at the chamber's edge; next turn he tips seawater onto the melt and the room explodes in steam | tg_heavy field, tg_safe tiles, then fw_quench | get to a cooled tile |
| **Cooling Shell** | window | After Quench his shell cracks: 1 round at x3 damage taken | fw_cracked | burst him |
| **Mould Cage** | control | Roots the player beside the Core Canister he keeps by the crucible | chain-wrap hit | cleanse, or kill the Canister first |
| **Overpour** | phase, under 50% | Pour Line marks two channels at once | the same, doubled | the floor gets crowded |

### 4b. The Sealwright: "The Keeper of the Archive" (Quarantined Archive, solo)

**Fantasy.** The archive's conscience. He sealed away what command would not let him mend, and now guards it against
you, reluctantly. **Arena:** the archive. He stands before the chained reliquary and does not step away from it.

| Move | Kind | What it does | Mark / animation | Counterplay |
|---|---|---|---|---|
| **Script Lines** | set piece | Omen: Seal Lines, a diagonal cross from the reliquary; next turn they close: the set-piece lock (RUL-2026-10-28-015: `elementalseal`, `timecompression` +10 AP on every jutsu, `increasecooldown` +2 on Move and Replacement Technique) for 2 rounds on anyone standing in them | tg_control lines, then sw_script | step off the lines |
| **Archive Lock** | set piece, signature | Violet over the whole archive except three tiles in the reliquary's light; next turn the set-piece lock (RUL-2026-10-28-015: `elementalseal`, `timecompression` +10 AP on every jutsu, `increasecooldown` +2 on Move and Replacement Technique) for 2 rounds everywhere else | tg_control field, tg_safe, then sw_lock | get into the light |
| **Called to the Archive** | summon | One Crown Stonebound, a lighter bruiser than the Crowned Captain, steps out of a frame (one at a time). His Ward of Command lands on it as the highest-health ally (RUL-2026-10-28-013) | cc_recall reused | kill it, or ignore it and pressure him |
| **Mending Seal** | sustain | Heals and cleanses himself | soft seal glow | interrupt with burst |
| **He Lowers His Seals** | window, under 30% | Once: for 1 round he takes x3 damage. "He lowers his seals for one breath, as if hoping you will end it." | sw_lowered | end it |

The Sealwright keeps **Ward of Command** (RUL-2026-10-28-013). The Archive's alarm guard is its own record, **Crown
Archivist** (the Skyglass Archive Keeper), not the Skyglass Sentinel; the Cache Sentinel is unchanged (RUL-2026-10-28-013).

### 4c. The Skyglass Sentinel: "Tidewatch" (Buried Cache, solo)

**Fantasy.** A guardian of shell and stone, buried in the sand with the cache, and the tide is on its side. **Arena:** the
cove. It holds the dig site.

| Move | Kind | What it does | Mark / animation | Counterplay |
|---|---|---|---|---|
| **Tide Line** | set piece | Marks the two rows nearest the sea; next turn the surf hammers in: damage and a push up the beach | tg_heavy rows, then st_tide | stand above the line |
| **Shell Wall** | barrier | A shell-and-stone barrier between it and the player | barrier sprite | break it, or go around |
| **Counter Stance** | duel, under 60% | Reflect | as live | do not burst into it |
| **Low Tide** | window | After Tide Line the sand runs out from under it: 1 round at x3 damage taken | st_exposed | burst it |

### 4d. The Captain's Watch duels

- **The Wayfinder ("Still no home port").** Marks a scatter of "old coastline" tiles; next turn the coast moves and they
  erupt. Afterwards he repositions to empty ground (AI movement to EMPTY_GROUND is harness-confirmed). He opens with Chart
  Mark. **Counterplay:** read the scatter; follow him.
- **The First Blade ("Finally. Something new.").** He fades into stealth, marks a red ring around himself, and the next
  turn cuts everything inside it. **Window, under 25%:** "That was new." He lowers his blades to savour it, taking x3
  damage for 1 round.
- **The Captain** fights exactly as in section 1, minus the Sealwright's Ward. The Oathkeeper's terms still apply.

## 5. Sharing (director, 2026-10-28)

- **Jutsu are shared (canonical).** Boss and library jutsu are one set, used by the hunts, the endgame dungeon, the
  level 40-60 dungeon and Crownhold. There are no dungeon-only jutsu copies; this supersedes the dungeon-only copies in
  `SKYGLASS_WRECK_ENCOUNTERS.md`. Only AI records differ, and only for stats:
  - the live crew records, used by the hunts, are upgraded in place with solo-tuned stats;
  - the dungeon copies carry the party-tuned stats;
  - the level-50 copies carry the lower stats.
- **Upgrading in place means editing equipped jutsu.** push/319 must unequip every holder of a shared jutsu (live crew and
  any copy already equipped) before editing it, then re-equip, in that order (`docs/ENGINE_LAWS.md` laws 18 and 60; the
  build-order warnings are recorded in `state/validate_exceptions/319_skyglass_update.json`, RUL-2026-10-28-002).
- **No copies to rename.** Live jutsu are used as they are wherever only the name or battle text would change; the Captain uses the old Crowned Captain's live kit.
- **Fewer patterns.** At most two per set piece, with lingering pools built into the base blast.
- **Budget:** superseded by the set-piece library (5a): about 32 new jutsu in total.

### 5a. The set-piece library (director, 2026-10-28: "a pass of our setup to see how we can minimize new jutsu")

Every set piece is two jutsu, a mark and a blast. Most of the jutsu count is bosses each owning their own pair. The fix
is a small **shared library**: each pattern is built once and used by every boss that needs it. Bosses keep their
identity through their own kit, the battle-log line on their own moves, and one bespoke signature each.

**Shared marks.** A mark is pure warning, the same danger language everywhere, so marks are always shared. There is one
jutsu per pattern and icon. Each mark carries its own primed-marker type, so any two different marks can sit in one boss.

| Mark | Pattern | Icon | Used by |
|---|---|---|---|
| Omen: Ring | radius-2 ring around the caster | red | Collapse, First Blade's ring, Armsmaster |
| Omen: Binding Ring | radius-2 ring around the caster | violet | Ship's Bell |
| Omen: Rows A / B | two fixed row pairs | red | Broadside, Tide Line, the Second |
| Omen: Scatter A / B | two complementary halves: together they cover the arena | red | Rupture Field, the Wayfinder's coastline, Shardstorm, Armsmaster |
| Omen: Lines | a 3-ray fan from the caster, using the union of both row parities (the grid is pointy-topped with odd rows shifted) | red | Crownfall, Pour Line |
| Omen: Seal Lines | a diagonal cross from the caster | violet | Script Lines, Replicant Zero |
| Omen: Last Light | whole arena except three safe tiles | red field and cyan stars | Maw of the Deep, Quench |
| Omen: Last Light, Binding | whole arena except three safe tiles | violet field and cyan stars | Command Absolute, Archive Lock |

Library rules (RUL-2026-10-28-015; harness `fable/skyglass-wreck-sim` 5f6c3edb, `library_spec.json`): every blast and
signature move has cooldown 2, and offensive non-damage rows hit enemies only.

That is 10 marks. Mark names show in the battle log ("The Core Horror uses Omen: Ring"), and they double as a reading
lesson.

**Shared blasts.** A blast with no special effect is shared: one heavy blast per pattern, about 6 jutsu. It carries a
neutral battle-log line ("The marked ground erupts.") and the matching shared animation.

**Bespoke blasts, one signature per boss**, where the name, voice and animation are the payoff:
- Maw of the Deep (with Exposed Seam);
- Quench (with Cooling Shell);
- Command Absolute ("Kneel.");
- Crownfall;
- Broadside ("Fire.");
- Ship's Bell (push and the set-piece lock; RUL-2026-10-28-015).

**Windows.** A boss's 1-round x3 window rides on its signature blast, or on one shared "lowered guard" self-jutsu with
a neutral line, used by the Sealwright, the First Blade and the Second.

**What is never new:** phase buffs, heals, roots, duel moves. These come from live jutsu used as they are.

**Budget, everything** (Wreck, hunts, Crownhold):

| Group | New jutsu |
|---|---|
| Shared marks | 10 |
| Shared blasts | 6 |
| Bespoke signatures | 6 |
| Lowered guard | 1 |
| Crew additions (Chain Hook, Oath of Stillness, Chart Mark, Aegis, Mending Seal, Ward of Command) | 6 |
| Summons (Recall, Called to the Archive) | 2 |
| The Crown's Will | 1 |
| Barrier (or reuse a live barrier) | 0-1 |
| **Total** | **about 32-33**, against 108 in the first build |

## 7. Crownhold's commanders (director, 2026-10-28)

The three division bosses keep the kits Crownhold built for them. Each gains **one library set piece and one window**, so
they add no new jutsu of their own.

| Commander | Library set piece | Window | Flavour |
|---|---|---|---|
| **The Armsmaster** (armoury, war-axe) | **Racks Fall:** Omen: Scatter, then the shared scatter blast, as the weapon racks come down. Later, **Whirlwind:** Omen: Ring, then the shared ring blast | none; he is the straight fight that teaches the marks | "\"Every weapon the Project ever tested. Mind your footing.\"" |
| **Replicant Zero** (the first returned; clones, copies) | **Jar Seals:** Omen: Seal Lines, then a shared violet blast. Split Image clones stand on the lines with him | none; his trick is the clone: hit the one that casts a shadow | "\"I would like a copy.\"" |
| **The Second** (the only officer allowed to question the crown) | **Order of Battle:** Omen: Rows, then Sovereign Undertow (his live pull) drags the player into the rows before they fire (a two-marker chain) | **He questions the order**, under 30%, once: the shared lowered guard for 1 round. "\"I questioned his orders for thirty years.\"" | the line is the payoff |

Crownhold carries HP between fights, and the commanders are never fought alone, so their numbers are tuned for the chain
(RUL-2026-10-28-013): Armsmaster, then Replicant Zero, then the Second, then the Crowned Captain. Targets: every route
(shortcut, War Rite buff, Healing Rite) clears; the Healing Rite route clears highest and the alarm route lowest. Round
targets: pending harness rerun.

## 6. Engine recipe (harness-confirmed)

- **Marks:** a mark is a visual ground jutsu with a 1-round life.
- **Marker for the next turn:** each set piece puts its own marker type on the boss. Use a type outside the shared 3-round cooldown list: increasecooldown with no actions, or increaserange.
- **Turn cost (library, 5f6c3edb):** the mark costs 40 AP and puts a unique 1-round marker on the boss. The blast costs 100 AP; its rule (`has_effect <marker>`) sits at the top of the list, so it fires on the next turn. After marking, the boss's rule `has_effect <marker>` → plain attack, then end turn, spends the remaining 60 AP. That 60 AP also allows a two-marker chain. Earlier harness builds used 100 AP for both; superseded.
- **Ground jutsu land only damage.** A blast that stuns or pushes targets CHARACTER, with the rule targeting SELF; that spares the boss and the safe tiles.
- **Patterns:** rings use the spiral method; arena patterns use battlefield coordinates. The boss stays put so his patterns line up.
- **Range** caps at 5.
- **Shared cooldowns:** stun moves (and other shared types) lock each other. The set-piece lock uses non-shared types, so the bosses' own stun and seal moves (Final Command, Ruin Refrain, Sovereign Fetters, Keelbind) cannot block Ship's Bell, Command Absolute or the Seal Lines blast; Maw of the Deep keeps its true stun (RUL-2026-10-28-015).
- **Windows:** weakness on SELF gives a working 1-round x3 window. A cleanse in the same jutsu strips it.
- **Summons:** one live summon per caster.
- **Tiles do not grant jutsu.** A heal or buff tile has to be an ordinary ground effect, applied while an action resolves.

## Animations this adds (to `SKYGLASS_BOSS_ANIMATIONS.md`)

| Boss | New ids |
|---|---|
| The Captain | cp_broadside (row cannon fire), cp_gunwale (barrier sprite), cp_final_command (crimson strike) |
| The Core Horror | ch_claw, ch_undertow (drag streak), ch_exposed (open seam) |
| The Crowned Captain | cc_hexweave |

## Open questions for the harness (PROBE)

1. Does a two-marker chain (mark plus 40 AP follow-up, detonate next turn) fire in order?
2. Does `weakness` on SELF expose the caster as designed, for 1 round?
3. Can a ground effect grant `injectjutsus` to whoever ends a move on it? Is the injected jutsu preloaded into the battle? Does it disappear after one use? (Crown Shard is cut; director, 2026-10-28: "maybe for another fight. Or in another manner. Like standing on a tile to gain access to a heal or a teamwide buff". Kept as a toolkit question for later fights.)
4. Settled by the director: Last Directive keeps clearprevent, so no clear is needed.
5. Will players attack a barrier when it blocks their path?


## 8. Rare-run twists (RUL-2026-10-28-020; mechanics to be proven in the harness)

Each rare run gets one signature twist, so it doesn't replay the hunt bosses in the same way.
- **The Fall: spreading fire.**
  - Each round, the burning decks lay ember tiles on more hexes. Ground damage is instant and ground afterburn does nothing, so the embers are `drain` tiles: standing on one burns you on your next action.
  - Candidate engine route: an immobile hazard AI (Seal Charge pattern) that casts a growing ember pattern each round.
  - The safe ground shrinks toward the gangway.
- **The Sealed Reliquary: the reliquary remembers.**
  - Each echo that falls leaves its signature set piece behind. A static hazard echo keeps casting it during the next fight, so the gauntlet layers up: the Warden's pour lines under the Sealwright, then both under the Sentinel.
  - Candidate engine route: per-fight hazard records holding the previous boss's library mark-and-blast pair.

Tainted versions keep the same twist and add their own (loot tables §5).


## 9. Minor marks for regular enemies (RUL-2026-10-28-024)

Two shared library pairs teach the mark-then-blast language before the bosses use it at full scale:
- **Splash:** the target's hex and its six neighbours.
- **Short line:** three hexes from the caster toward the target.

Same recipe as the boss set pieces: a 40 AP mark with a unique 1-round marker on the caster, then a 100 AP blast next turn gated on the marker.
- Damage is modest; a step off the mark avoids it.
- No floor coverage and no safe tiles.
- The visuals reuse the existing mark and blast tiles.

Used by Wreck floors 1-3 crew, the common runs and the opening fights of the hunts. The library adds 4 jutsu for these.


## 10. Sound (RUL-2026-10-28-028: existing SFX only)

Effects carry `appearSfx` / `disappearSfx` (asset ids, `validators/combat.ts` BaseAttributes). New audio needs separate approval, so only the 16 live SFX assets are used.

| Moment | SFX (asset id) |
|---|---|
| Every mark (Omen) lands | WindSFX `oDdj-mBmiWTswFi_NkOqc` |
| Heavy ground blasts (Ring, Rows, Lines, Splash, Short Line, Broadside) | EarthSFX `XBlRonNjvwAZx1_HFpHdM` |
| Crownfall, Shardstorm (skyglass shards) | SwordSFX `muq1tu3xvolOsUHm-NqBr` |
| Control/lock blasts (Binding Ring, Seal Lines, Command Absolute, Ship's Bell) | LightningSFX `eJCEtS5_P_pW_VPc6ttRh` |
| Core Horror water/rot (Maw, Undertow, Collapse, Rupture) | WaterSFX `NThXOSKNDXPwNnGxDtH0Z` |
| Ember tiles, Pour Line, Quench | FireSFX `9-b8hbTXA019dgn8yyr3j` |
| Summons (Recall, Called to the Archive) | Shinobi Dash `gR2880EZVlWV4eam-ufei` |
| Burst windows open (lowered guard, Exposed Seam, Cooling Shell) | Sword Clash `PFY2oXpwIpNwUOx327WCm` |
