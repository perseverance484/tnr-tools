# Player jutsu text sweep, 2026-10-21

- **Asked by:** dauntless, 2026-10-21 (RUL-2026-10-21-021): "analyze all jutsu in the census for edits and create one master manifest to submit tickets for each."
- **Records:** the 2026-10-21 census (push/178-181). Eligible: visible, no bloodline, not AI or BLOODLINE type, not equipped by any AI (push/158-161), no test/staff name, no open suggestion. 385 eligible; Liquid Palm was already approved, the other 384 were reviewed.
- **Style:** `docs/design/jutsu_overhaul/WRITING_STYLE.md`. **Engine reads:** studie-tech/TheNinjaRPG@a744c04.
- **Method:** eight parallel drafting passes (48 jutsu each) against one brief, then a linter over every new text, a hand review of a random 24, two cross-checks (area wording on single-target jutsu, element words), and hand fixes to Crimson Spires, Dragon Breath and Crescent Reaper Fang.
- **Output:** `push/196_jutsu_text_sweep.json`, 342 suggestions (Liquid Palm + 341 edits). Every verdict, defect list and draft is in `JUTSU_TEXT_SWEEP_2026-10-21.json` next to this file.
- **Live-game requests/writes:** 0.

## Counts

| Verdict | Jutsu |
|---|---|
| EDIT (in push/196) | 341 + Liquid Palm |
| OK (text already accurate) | 29 |
| SKIP (not edited) | 14 |

## Engine facts found during the sweep (source-verified, a744c04)

1. **Damage modifiers ignore `statTypes`.** `increasedamagegiven`, `decreasedamagegiven`, `increasedamagetaken` and `decreasedamagetaken` apply to all damage unless the effect lists `elements`, in which case only hits of those elements (`libs/combat/tags.ts` `getEfficiencyRatio`: "Damage modifiers are universal unless explicitly limited to matching elements"). A "Taijutsu" or "Bukijutsu" limit on these effects does nothing. Many old texts said "more vulnerable to taijutsu"; the new texts say what the engine does.
2. **A missing `friendlyFire` means ALL** (`libs/combat/process.ts` ~176): an area effect without it lands on allies too. Where that applies, the new texts say "everyone caught" rather than "enemies"; the affected jutsu are in the mechanics list below.
3. Lifesteal, recoil, reflect, afterburn, absorb and similar "after" effects only act from the round after the cast.

**Correction to one submitted ticket:** push/188 (Bedrock Stance, suggestion `H5owbVykZkUFsjyOGfGua`, PENDING) says "their taijutsu lands harder". By fact 1 its damage boost applies to all damage. A one-word fix ("their blows land harder") should follow once that suggestion resolves, or the reviewer can edit it at approval. Black Thorn Rose (push/190) has damage reduction limited to the None element (non-elemental hits only); its text ("thorns close around the user as armour") is not wrong, only unspecific.

These two facts also belong in the jutsu text guide once its review returns (the frozen review SHA does not have them).

## Skipped (decisions for the director)

| Jutsu | Why |
|---|---|
| Frictional force | Joke content: the battle line is a riddle about kittens on a slide and the description is a stub; part of a Student-gated S-rank event set. Effect is a 30% damage-dealt debuff on the target for 2 rounds if the desk wants it written. |
| Hogs gone Wild | Joke content: the battle line is a scarecrow pun referring to 'his field' and the description is a stub; same Student-gated S-rank event set. Effect is a 30% absorb into health for 3 rounds on the user. |
| Earth Release: Boulder Crush | Description carries a staff-authored HTML warning ('DON'T TRAIN. ALREADY CAPPED. IT HAS NO POWER PER LEVEL'); a text ticket should not silently drop it, and the mechanics look broken. Needs a director decision first. |
| Retribution | The absorb effect has no rounds set. In a744c04, absorb only converts damage when castThisRound is false, and castThisRound is only cleared for effects with numeric rounds, so this absorb may never trigger. Its real behaviour needs confirming before the text can describe it. |
| Wind Release: Whirlwind Demise | The description embeds a deliberate staff training notice in red HTML; removing or keeping it is a staff decision, not a text fix. Effects: +40% stats (offence, defence, highest generals) and +40% Wind damage, both SELF for 2 rounds. |
| Aqua Dragon Barrage | The description embeds a deliberate staff training notice in red HTML ('DON'T TRAIN. ALREADY CAPPED...'); removing or keeping it is a staff decision. Otherwise only 'your wounds' needs fixing; the battle line is accurate (Water damage, self heal on the next round). |
| Parry | Description carries a staff-authored player warning in HTML ('DON'T TRAIN. ALREADY CAPPED...'); whether to keep or remove it is a staff call, so the record was not rewritten. |
| Marshmallow Inferno | Joke content (marshmallow, chocolate and graham crackers); whether to keep the whimsical theme is a director call. Note: effects are Fire damage plus increased damage taken (+10%, 2 rounds), and the text calls it an illusion although damage scales on Ninjutsu. |
| Corpse Jutsu | Apparent test/joke content: near-zero costs (2 chakra, 2 stamina), no cooldown, and copy-pasted second-person horror text unrelated to its friendly heal and self heal boost. |
| Crep wall | Apparent test content: misspelt name ('Crep wall'), 1 chakra/1 stamina cost, no cooldown, and a 60% damage reduction; text describes movement it does not have. |
| FBA | Apparent test copy: 0.05 costs, no cooldown, acronym name and battle line 'HKD Copy'; description claims a bloodline seal the effects do not have. |
| TGC | Likely staff content in the same acronym family as FBA/TFG; the text claims lightning but the hit is non-elemental, and a 50-power hit at 40 AP needs staff confirmation before any copy. |
| Flash Pulse | Record has no effects at all, so there is nothing accurate to describe. |
| TFG | Apparent test/joke content: 0.05 costs, no cooldown, 300 health cost and stub text ('8 gates'). |

## Name flags (not renamed; your call)

| Jutsu | Note |
|---|---|
| Aegis of Shadows | 'Aegis' promises protection, but the jutsu only weakens the target; no defensive effect. |
| Black Coffin | 'Black Coffin' and the old incantation ('know your own powerlessness') echo a well-known Bleach kido; not a ninja franchise, flagged for the director's awareness. |
| Blazing Fang Strike | 'Blazing' suggests Fire, but the pierce damage is non-elemental; text keeps heat imagery tied to the afterburn without naming an element. |
| Subaku Palace | 'Subaku' is one letter from 'Sabaku' (desert), a recurring technique prefix in a well-known ninja anime; flag only. |
| Tempest Cleave | 'Tempest' implies wind, but the damage is non-elemental. |
| Moose Cleave | 'Cleave' suggests a cutting blow, but the fiction and old text describe an eye beam; possibly an in-joke name from the same Student-gated S-rank event set as two joke jutsu. |
| Moose Prime | Possibly an in-joke name from the same Student-gated S-rank event set as two joke jutsu; flag only. |
| Fury of The White Tiger | The old text (opening seven inner gates, a tiger-shaped punch shockwave) closely echoes a signature technique from a well-known ninja anime franchise. |
| Crescent  Reaper Fang | The name contains a doubled space ('Crescent  Reaper Fang'); not renamed, flagged for a name fix. |
| Eight Fist Style: Lotus Dance | 'Eight' plus 'Lotus' taijutsu echoes signature taijutsu names from a well-known ninja anime franchise; flag only. |
| Inferno Leech | 'Inferno' suggests fire, but nothing in the jutsu is Fire. |
| Amaterasu's Renewal | 'Amaterasu' is the name of a signature technique in a well-known ninja anime franchise. |
| Chakra Ignition Strike | 'Strike' promises a hit, but the jutsu deals no damage. |
| Draconic Assasult | Typo in name: 'Assasult' (Assault). Not renamed. |
| Dust Dismanting | Typo in name: 'Dismanting' (Dismantling). Not renamed. |
| First Chakra Gate | 'First Chakra Gate' closely echoes the first of the Eight Inner Gates from a well-known ninja anime franchise. |
| Fist of 10 ,000 Volts | Spacing typo in name: '10 ,000'. Not renamed. |
| Gust Armor | 'Armor' promises protection; the jutsu has no defensive effect (a Wind damage boost and an enemy vulnerability). |
| Lightning Ward | 'Ward' promises protection; the jutsu has no defensive effect. |
| Pressure Damage | 'Pressure Damage' closely echoes a wind technique name from a well-known ninja anime franchise, and the old description paraphrased that technique's wiki text. |
| Wind Release: Whirlwind Demise | 'Wind Release:' prefix echoes the naming convention of a well-known ninja anime franchise; 'Demise' also suggests damage on a pure self buff. |
| Wind Style: Sky Dragon | 'Wind Style:' prefix echoes the naming convention of a well-known ninja anime franchise. |
| Body Flicker | 'Body Flicker' closely echoes a technique name from a well-known ninja anime franchise. |
| Cyclone Prison | 'Prison' promises a hold, but no effect stops enemies moving or acting. |
| Debilitating Sword Strike | 'Debilitating' promises an enemy debuff; the only secondary effect is a self damage boost. |
| Earth Release: Crushing Boulder | 'Earth Release:' prefix closely echoes the elemental-release naming of a well-known ninja anime franchise. |
| Earth Release: Earthquake | 'Earth Release:' prefix closely echoes the elemental-release naming of a well-known ninja anime franchise. |
| Earth Release: Seven Heavenly Pillars | 'Earth Release:' prefix closely echoes the elemental-release naming of a well-known ninja anime franchise. |
| Fire Release: Inferno | 'Fire Release:' prefix echoes a well-known franchise naming pattern, and 'Inferno' promises a damaging blaze on a jutsu with no damage effect |
| Lightning Release: Charged Senbon | 'Lightning Release:' prefix echoes a well-known franchise naming pattern |
| Purifying Wave | 'Purifying' implies a cleanse the jutsu does not have |
| Quicksand Trap | 'Trap' suggests immobilising the enemy; there is no moveprevent |
| Senbon Sakura | 'Senbon Sakura' and the shattering blade of petals closely echo Senbonzakura from Bleach. |
| Suijin Gir | 'Suijin Gir' looks truncated (possibly 'Giri'); not renamed. |
| Water Release: Whirlpool Water Blade | Name uses the 'X Release:' prefix, a naming convention closely echoing a well-known ninja anime franchise. |
| Cyclone Palm Strike | Named 'Strike' but has no damage effect; it is two debuffs only. |
| Earth Release: Palm Push | Name uses the 'X Release:' prefix, a naming convention closely echoing a well-known ninja anime franchise. |
| Earth Release: Stone Fist Strike | Name uses the 'X Release:' prefix, a naming convention closely echoing a well-known ninja anime franchise. |
| Earth Style: Shattering Kick | 'Earth Style:' prefix echoes a well-known ninja anime franchise's element-release naming convention. |
| Fire Release: Burning Soil | Name uses the 'X Release:' prefix, a naming convention closely echoing a well-known ninja anime franchise. |
| Lightning Release: Holy Strike | Name uses the 'X Release:' prefix, a naming convention closely echoing a well-known ninja anime franchise. |
| Spectral Counter | 'Counter' suggests a counter-attack or reflect; the jutsu only raises the target's damage taken. |
| Water Release: Heavy Rain | 'Water Release:' prefix echoes the franchise's elemental naming convention; director's call. |
| Wind Release: Mighty Gust | 'Wind Release:' prefix echoes the franchise's elemental naming convention; director's call. |
| Wind Release: Tempest Edge | 'Wind Release:' prefix echoes the franchise's elemental naming convention; director's call. |
| Summon: Totem of Amaterasu | 'Amaterasu' is also a well-known technique name in a major ninja anime franchise (here it names the deity). |
| Summon: Totem of Tsukuyomi | 'Tsukuyomi' is also a well-known technique name in a major ninja anime franchise (here it names the deity). |
| TFG | Stub text '8 gates' echoes the Eight Gates from a well-known ninja anime franchise. |

## Mechanics flags (effects untouched; the text describes what the effects actually do)

| Jutsu | Note |
|---|---|
| Black Coffin | damage and afterburn have no friendlyFire limit (default ALL), so allies in the circle are hit; only the damage-taken debuff is enemies-only. |
| Tempest Cleave | damage, afterburn and damage-taken debuff are all friendlyFire ALL, so allies in the circle are hit and debuffed too. |
| Moose Cleave | damage and the stat debuff have no friendlyFire limit (default ALL), so allies in the circle are hit and weakened; only afterburn is enemies-only. |
| Black Crow | afterburn lands on the user (SELF): the caster takes extra burn from hits for 2 rounds; likely an intended forbidden-jutsu drawback, confirm |
| Black Crow | damage, vamp and debuff have no friendlyFire limit (default ALL), so allies in the circle are hit. |
| Dark World | afterburn lands on the user (SELF): the caster takes extra burn from hits for 2 rounds; likely an intended forbidden-jutsu drawback, confirm |
| Dragon King's Impact | afterburn lands on the user (SELF): the caster takes extra burn from hits for 2 rounds; likely an intended forbidden-jutsu drawback, confirm |
| Ethereal Nexus | increasedamagetaken lands on the user (SELF) for 2 rounds; likely an intended forbidden drawback, confirm. |
| Ethereal Rebirth | decreasedamagegiven lands on the user (SELF) for 2 rounds; likely an intended forbidden drawback, confirm. |
| Fury of The White Tiger | afterburn lands on the user (SELF): the caster takes extra burn from hits for 2 rounds; likely an intended forbidden-jutsu drawback, confirm |
| Gaze into Yomi | afterburn lands on the user (SELF): the caster takes extra burn from hits for 2 rounds; likely an intended forbidden-jutsu drawback, confirm |
| Chakra Overflow | Two separate increasedamagegiven tags on the user (25% all schools and 25% Highest); confirm the stacking is intended. |
| Echoing Rift | afterburn lands on the user (SELF) on a NORMAL A-rank jutsu, a harmful tag on the caster; confirm intended. |
| Shrapnel Clone Barrage | damage is friendlyFire ALL (wound unset), so allies in the circle are hit and wounded. |
| Summoning Poison Salamander | summon carries friendlyFire ENEMIES, unusual for a summon; confirm it behaves as intended. |
| Crushing Tides | damage has rounds 2, so by damageUser it deals nothing on the cast round and lands as residual damage on the following rounds; confirm intended. |
| Drowning Mire | Neither the damage nor the increasedamagetaken has friendlyFire set (defaults to ALL), so the mire also damages and exposes the user's allies, and the user if they stand in it. |
| Earth Release: Boulder Crush | Guaranteed stun (power 100, 60 AP reduction) plus guaranteed movement prevention (power 110), both 2 rounds, on 40 damage at 25 chakra/stamina; looks far stronger than its peers. |
| Raijin Puncture | The pierce has no friendlyFire set (defaults to ALL), so the circular blast also hits the user's allies; comparable area jutsu use ENEMIES. |
| Retribution | absorb (30%, SELF, Health) has no rounds value; by source reading it may never fire. Probably needs rounds: 2 like its siblings. |
| Torturing Flame Coil | second damage effect is power 300 over 2 rounds with no element, against 35 for the instant Scorch hit; looks like a data error. |
| Arcbound Vortex | the only damage effect has rounds 2 (residual only), so this 60 AP attack deals nothing on the cast round; may be intended, worth confirming. |
| Flame Burst Punch | second damage effect has power 120 over 2 rounds against an instant hit of 20; the residual burn is six times the punch, which looks unintended |
| Inferno Burst | increasedamagetaken (Fire) effect has no friendlyFire key, so it defaults to ALL and also lands on allies inside the area, while the damage hits enemies only |
| Inferno Kunai Barrage | afterburn effect has no friendlyFire key, so it defaults to ALL and also lands on allies inside the area, while the damage hits enemies only |
| Majestic Flame | afterburn effect has no friendlyFire key, so it defaults to ALL and also lands on allies inside the area, while the damage hits enemies only |
| Phoenix Heart | damage and wound have no friendlyFire key, so they default to ALL and also hit allies inside the area |
| Quaking Fist | decreasedamagegiven effect has no friendlyFire key, so it defaults to ALL and also lands on allies inside the area, while the damage hits enemies only |
| Seal of Nullification | decreasedamagegiven 1% with friendlyFire FRIENDLY on an OPPONENT single-target jutsu can never land; looks like an inert filler effect. |
| Corrupting Miasma | Aimed at an enemy area (OTHER_USER, AOE_CIRCLE_SPAWN) but its only effect is a self buff; the area does nothing. |
| Herald of the Apocalypse | increasestat 25% lists no statTypes or generalTypes, so adjustStats applies nothing; appears inert. |
| Anchor the Storm | finalstand has no friendlyFire filter (defaults to ALL), so enemies standing in the circle also cannot drop below 1 health for that round. |
| FBA | Description claims a bloodline seal; effects are a hit and a 1-round health drain only. |
| KGK: Black Fang Lance | pierce has no friendlyFire filter on a line attack, so allies standing in the line are hit too. |
| TGC | damage on an area jutsu with no friendlyFire filter also hits allies in the circle. |
| Flash Pulse | No effects on the record; the jutsu does nothing when cast. |

## Already accurate (no ticket)

Fireball, Typhoon Tear, Aqua Barrier, Stormguard Aura, Tempestual Rend, Aqua Fang, Arashi Ikari, Blazing Chains, Bolt of Terror, Boulder Crush, Chakra Siphon, Crimson Surge, Crimson Tides, Dancing Wind, Divine Pulse, Dreamshell, Drowning Illusion, Emberbane Cocoon, Ethereal Bloom, Fiend Fire, Gale Blade, Inferno Dragon's Wrath, Inferno Slash, Lunar Descent, Molten Manipulation, Netherblight, Phantom Scythe, Skybreaker Palm, KGK: Veilguard Pulse.

