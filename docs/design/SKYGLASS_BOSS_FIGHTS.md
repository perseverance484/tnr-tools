# Skyglass boss fights: The Captain, the Core Horror, the Crowned Captain

A full design pass to make these three fights memorable. Director, 2026-10-28: "named jutsu, animations, mechanics, anything
and everything we've got". This file owns the fight design. Inputs:
- the approved structure, numbers and toolkit: `SKYGLASS_WRECK_ENCOUNTERS.md`;
- names and voice: `SKYGLASS_STORY_BIBLE.md`;
- animation ids and readability rules: `SKYGLASS_BOSS_ANIMATIONS.md`.

Every boss move is a **dungeon- or Crownhold-only copy**, with its own name, battle text and animations. Shared crew
records stay untouched.

## The tools we have (engine-checked unless marked PROBE)

| Tool | Engine | Use |
|---|---|---|
| Marked set piece | visual ground mark, then a 100 AP detonation next turn (harness-confirmed) | the core of every boss |
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
| **Ship's Bell** | set piece | Violet ring (radius 2) around him; next turn the bell tolls: push 3 and a 1-round stun | tg_control, then cp_bell_toll shockwave | leave the ring, or be thrown and stunned |
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

*Skyglass Wreck, floor 4, alone. Harness: 25,250 HP, two +100% rows, about 5 rounds.*

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

*Crownhold, the last fight, solo. Tuning in progress: a hard win in 12-15 rounds that fails if the marks are ignored.*

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
| **Command Absolute** | set piece, phase 2 | Violet over the whole arena except three stars; next turn every unsafe hex is stunned and sealed | tg_control field, tg_safe, then cc_command_absolute | reach a star |
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
| **Script Lines** | set piece | Marks a cross of four seal lines from the reliquary; next turn they close: seal, plus an elemental seal on anyone standing in them | tg_control lines, then sw_script | step off the lines |
| **Archive Lock** | set piece, signature | Violet over the whole archive except three tiles in the reliquary's light; next turn a 2-round stun and seal everywhere else | tg_control field, tg_safe, then sw_lock | get into the light |
| **Called to the Archive** | summon | One Skyglass Sentinel echo steps out of a frame (one at a time) | cc_recall reused | kill it, or ignore it and pressure him |
| **Mending Seal** | sustain | Heals and cleanses himself | soft seal glow | interrupt with burst |
| **He Lowers His Seals** | window, under 30% | Once: for 1 round he takes x3 damage. "He lowers his seals for one breath, as if hoping you will end it." | sw_lowered | end it |

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

- **Jutsu are shared.** One set of jutsu and rules per enemy, used by the hunts, the endgame dungeon and the level 40-60
  dungeon. Only AI records differ, and only for stats:
  - the live crew records, used by the hunts, are upgraded in place with solo-tuned stats;
  - the dungeon copies carry the party-tuned stats;
  - the level-50 copies carry the lower stats.
- **No copies to rename.** Live jutsu are used as they are wherever only the name or battle text would change; the Captain uses the old Crowned Captain's live kit.
- **Fewer patterns.** At most two per set piece, with lingering pools built into the base blast.
- **Budget:** about 35 new jutsu for the Wreck crew and bosses, 10 for the Crowned Captain, and about 15 for the hunt bosses.

## 6. Engine recipe (harness-confirmed)

- **Marks:** a mark is a visual ground jutsu with a 1-round life.
- **Marker for the next turn:** each set piece puts its own marker type on the boss. Use a type outside the shared 3-round cooldown list: increasecooldown with no actions, or increaserange.
- **Turn cost:** the mark and the blast both cost 100 AP. A two-marker chain (a 60 AP mark plus a 40 AP follow-up) works.
- **Ground jutsu land only damage.** A blast that stuns or pushes targets CHARACTER, with the rule targeting SELF; that spares the boss and the safe tiles.
- **Patterns:** rings use the spiral method; arena patterns use battlefield coordinates. The boss stays put so his patterns line up.
- **Range** caps at 5.
- **Shared cooldowns:** stun moves (and other shared types) lock each other.
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
