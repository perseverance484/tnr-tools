# TNR combat engine: how a fight resolves

Pinned to `studie-tech/TheNinjaRPG` @ `29cd91b` (2026-11-21). Paths are under `app/`; `tags.ts`, `process.ts`,
`actions.ts`, `util.ts`, `turn.ts`, `damagePipeline.ts`, `diffuse.ts`, `curse.ts`, `power.ts` and `constants.ts`
are under `src/libs/combat/`, and `drizzle/constants.ts` is `app/drizzle/constants.ts`. Every claim here is
**source-verified** (file and line cited) unless marked otherwise, and was re-read line by line in the PR #129
review (Nov 22 2026). Per-tag detail is in `tags/<tag>.yaml`; tag-to-tag links are in `interactions.json`.
`docs/ENGINE_LAWS.md` stays the law text of record; this file agrees with laws 9, 10, 11, 75 and 76 and gives
their mechanism.

## 1. Round and turn

| Step | What happens | Source |
|---|---|---|
| R1 round start | Every fighter's AP refills to 100. `battle.round` advances. | `turn.ts:64` (`alignBattle` :25) |
| R2 order | Turn ring = `usersState` order (sorted by initiative, highest first, at battle start), skipping fighters no longer in battle. The turn passes cyclically to the next fighter when the 60 s timer ends, the actor has no affordable action besides End Turn, or the actor left. In non-PvP battles the attacker acts first. A summon is its own actor: it copies its summoner's `initiative` and is inserted before the first fighter with lower initiative, so it acts after the summoner and anyone tied. No other combat tag reads or changes initiative. | `actions.ts:1697-1733` (`calcActiveUser`); `turn.ts:140-157`; `tags.ts:2755-2767`; `server/api/routers/combat.ts:3276-3280` |
| R3 turn clock | 60 s per turn. | `constants.ts:62` |
| R4 what you may use | `availableUserActions` filters. Stealth hides every jutsu and the basic attack, meditate, heal, clear, cleanse, both stances and flee; move, replacement, End Turn and items stay. Disarm hides weapons and weapon jutsu. Moveprevent hides move, replacement and move-tag jutsu. Summonprevent hides summon jutsu (items with a summon tag stay). Elementalseal hides jutsu with an authored 60 AP cost that are elemental. These hiding gates need the effect active with rounds > 0 and not cast this round, and the server enforces them. Injectjutsus adds jutsu without that wait: action selection reads only `isEffectEnabled` (active, not sealed), so a grant that has resolved can expose its jutsu later in its own casting round (`actions.ts:148-160`). Mastery, cooldown and battle-type gates also apply. End Turn shows only while available AP > 0. | `actions.ts:111-300` (stealth `:163-184`, `:230`; gates `:122-125`, `:231-266`); `util.ts:695-713`; `server/api/routers/combat.ts:756-759` |
| R5 AP | Available AP = max(0, AP left − strongest stun `apReduction`). Only one stun counts, the strongest of two kinds: the holder's active, unsealed stun effects not cast this round, and active stun ground effects on the holder's tile not cast this round that pass `checkFriendlyFire` for the holder (this read makes no land roll). An action is allowed while available AP − its cost ≥ 0. Jutsu AP is ± 10 under timecompression/timedilation (`TEMPORAL_AP_DELTA`). | `actions.ts:1569-1597`, `turn.ts:159-182`, `util.ts:681-692`, `drizzle/constants.ts:4581` |
| R6 each action | Cast → effects created (`isNew`, `castThisRound`) → `applyEffects` resolves **all live effects** (section 2). Runs after every action, not once a round. | `process.ts:357` |
| R7 round end | For every user and ground effect not cast this round: `rounds = max(0, rounds-1)`; then `isNew=false`, `castThisRound=false`. Curses with 1 round left settle (pay stored heal) if an enemy is still in the fight. Ground effects expire. Masteries refresh. Sage exhaustion applies. | `turn.ts:58-121` |

## 2. One action: applyEffects stages

Order is from `performAction` (cast prep) and `applyEffects` (`process.ts:357-711`). Inside a pass, effects sort
by `EFFECT_SORT_RANK` (`util.ts:1062-1131`), and unranked types sort last (`util.ts:1016-1017`). The pass a tag
runs in decides when it acts; its rank only orders it inside that pass. Each `tags/<tag>.yaml` has its `stage`.

| Stage | Contents |
|---|---|
| S0 cast prep | Before `applyEffects`. `elementaldamage` becomes `damage` with the caster's element (`actions.ts:1071`, `elementalDamage.ts:23`). Potency rewrites cast tags' power (`actions.ts:1068`, `potency.ts:71`). Barriers on the path set `barrierAbsorb` (`actions.ts:1079-1081`, `:1104`). Tags become ground effects (`actions.ts:1087-1124`) or user effects. A stealthed enemy target is skipped (`actions.ts:1157`). |
| S1 ground pass | `applyGroundEffects` (`process.ts:379`, body `:713-873`), in sortEffects order. move (`:770`), clone (`:774`) and summon (`:776`) resolve here, and a barrier with a fighter on its tile ends (`:778`). barrier, clone, summon, move and visual are ground-only (`constants.ts:97-103`) and have no main-pass handler. Every other ground tag on an occupied tile that passes `checkFriendlyFire` becomes a `fromGround` user effect (`:788-802`): damage, heal and pierce get rounds 0 and the current round, others rounds 1 and the previous round. Ground damage on a barrier tile becomes barrier damage (`:806-817`). |
| S2 copy and mirror | `process.ts:417`. |
| S3 main pass | Filter `process.ts:426-431`, run `:453`. Excludes copy/mirror, the four damage modifiers (`constants.ts:246`), `POST_DAMAGE_MODIFIER_TYPES` (`drizzle/constants.ts:2497-2508`: consume, siphon, vamp and the post-pierce readers), pierce, increaseheal and decreaseheal. Effective order: (1) prevents, stealth, disarm, weakness; (2) pre-modifiers, elementalseal … increasemastery; (3) shield and finalstand land rolls, diffuse handler text (`process.ts:1698`); (4) redirection; (5) damage writes the raw consequence, and barrier-target damage resolves (`process.ts:1468-1483`); (6) flee; (7) heal writes its consequence; (8) **onehitkill sets HP to 0 directly** (`process.ts:1559-1567`, `tags.ts:2324`); (9) rob, seal, stun; (10) **drain and poison write their consequences here** (`process.ts:1544`, `:1671`), despite their post-pierce rank; (11) timecompression, timedilation; (12) unranked: curse, immunity, increase/decreasemaxpools, increaserange, increase/decreasecooldown. |
| S4 instant-kill accounting | `process.ts:455-467`. Credits the HP that S3 removed to Curse and drops the bookkeeping consequence. |
| S5 Consume/Siphon register | `process.ts:469-477`. Live from their casting action. |
| S6 Diffuse repayment | `process.ts:480-506`, `diffuse.ts:95-133`. Only the actor's own debts, at most once per round (so on the holder's *acting* rounds). Pays `remaining/turnsLeft` straight to HP: skips shields, DR and Absorb, goes through Final Stand (`diffuse.ts:117`), credits Curse and Consume/Siphon. Skipped at HP ≤ 0. |
| S7 damage pipeline | `process.ts:525-533` (`damagePipeline.ts:655`): every damage/residual consequence through `computeDamagePacket` (section 4). Modifier log loop `:535-598`, carry-forward `:600-614`. |
| S8 pierce | `process.ts:618`. After the pipeline, so no damage modifier touches it. Reads the stat snapshot from before S3 (`process.ts:1528-1534`). |
| S9 Parry split | `process.ts:621-625`, split at `:877-904`. |
| S10 post-damage readers | `process.ts:630-639`, in rank order: lifesteal, afterburn, absorb, recoil, reflect, wound, then vamp (unranked, last). Absorb is held for S13 when the action has Parry returns or its holder has active Diffuse. |
| S11 Parry returns | Inserted as consequences (`process.ts:641`). |
| S12 Diffuse deferral | `applyDiffuseToConsequences` (`process.ts:643-650`, `damagePipeline.ts:381`, `diffuse.ts:19`). Section 4c. |
| S13 delayed Absorb | The Absorbs held in S10 (`process.ts:651-656`). |
| S14 heal adjustments | increaseheal, decreaseheal (`process.ts:661`). |
| S15 mitigate and apply | Curse-holder set fixed (`process.ts:664-674`). `mitigateConsequence` runs on **every** consequence before any is merged (`process.ts:677-683`, body `:956-1077`): Consume credit, shields soak or Pierce destroys them, Final Stand (`:1018`). Then `collapseConsequences` (`util.ts:1180`) merges per target and damageSource, and `applyConsequence` (`process.ts:1080-1373`) changes pools with no further floor: damage plus the Vamp heal, residual and wound, heals, reflect, recoil, afterburn, lifesteal, absorb, drain (`:1325`), poison (`:1349`). Curse, enmity and Siphon credit go through `recordHpLoss` (`:1117`). |
| S16 wrap-up | Newly cast curses become ready (`process.ts:685-688`); conversion shields granted (`:690`); pool sync (`:692`); mastery refresh (`:696`). |

Curse HP-loss storage happens at several points: instant kills (S4, `process.ts:458`), debt repayment (S6,
`:492`), consequence application (S15, `:1117-1121`) and reflect (`:1203`).

## 3. Effect lifecycle rules

- **Two apply groups** (`process.ts:1514` and `:1595`, `util.ts:848-876`). *Ticking* tags (damage and pierce residual, heal, drain, clear, cleanse, flee, rob, seal, stun, wound, onehitkill, pool cost, aggro) apply when new and then once a round, on the holder's first action of the round. *Always-apply* tags (stats, mastery, damage and heal modifiers, potency, absorb, reflect, parry, recoil, afterburn, lifesteal, vamp, prevents, shield, curse, copy, mirror, time shift, redirection, finalstand, **poison**) run on every action resolution. Poison therefore deals damage on every action its holder takes from the next round.
- **When an effect starts to count** (each tag's `live_from`). Damage modifiers need `!isNew && startRound !== curRound` and no blocking prevent (`damagePipeline.ts:166-185`); stats, mastery, absorb, reflect, parry, recoil, afterburn, lifesteal and heal modifiers gate on `!isNew && !castThisRound`. Law 75. Exceptions: potency gates on `isNew` only, so it affects the holder's next jutsu cast, later in the same round included (`potency.ts:93`, `process.ts:1745`). Seal counts as active as soon as it lands, inside its own casting action (`util.ts:938-940`). Consume, Siphon and Diffuse work from their casting action. Range and cooldown modifiers count as soon as they are on the holder. `damage`, `heal`, `pierce` with rounds 0 are instant; with rounds > 0 the casting action does nothing and they tick from the holder's first action of the next round (`tags.ts:1447-1449`, `:1588-1591`).
- **rounds**: 0 = instant. N = lasts N round changes after the cast round. Effects end early by removal (Clear and Cleanse set the removed effects' rounds to 0, `tags.ts:1104-1127`; Pierce zeros the shields it destroys, `process.ts:1004-1016`), a blocked prevent check (`rounds = 0`, `tags.ts:2821-2826`) or a failed land roll. The only tag that resets its own rounds is a bloodline Final Stand, which re-arms to rounds 1 when it fires (`tags.ts:2220-2221`). No tag lengthens, shortens or otherwise adjusts a surviving effect's rounds.
- **Land rolls.** Many tags roll `power%` once on landing and set `rounds = 0` on a miss: prevents, stun, seal, stealth, elementalseal, weakness, shield, timecompression, timedilation. Three differ. Final Stand rolls every time its handler runs, which is every action resolution while it lasts, and sets `rounds = 0` the first time a roll fails (`tags.ts:2238-2255`). Copy and Mirror roll once, in their casting action, and a miss only reports failure without zeroing `rounds` (`tags.ts:462, 507-518, 547, 621-626`). Clear, cleanse and flee re-roll every tick until they hit.
- **Prevents** (`tags.ts:2991 preventCheck`, `:338 applyPreventTag`). A prevent rolls power% to land. On success its power latches at 100 (`tags.ts:350-353`), so every later check blocks. It counts only while it is enabled and not cast this round (`util.ts:681`), a bloodline-sourced one is off while its holder is sealed, and preventCheck reads only the first matching one. Each tag's `prevent_check` says which of three kinds applies:
  - **Age-compared:** handlers that pass the checked effect block it only if it was created in a later round than the prevent. Effects already on the holder, or cast the same round, get through. This covers every buff and debuff (buffprevent, debuffprevent), Heal, Lifesteal and Absorb (healprevent), Stun, and Redirection (moveprevent).
  - **Any age:** Clear, Cleanse, Flee, Rob, Seal, One Hit Kill, Move and the Curse expiry payout pass no effect, so any active prevent blocks them, including a multi-round effect cast before it (`tags.ts:1155, 1165, 1531, 2356, 2402, 2317, 2273, 1690`). Ticking effects re-check on the holder's turn, so a Sealprevent that lands later ends an existing Seal. Move checks the mover's own moveprevent. Vamp is blocked if its caster has any active healprevent, with no roll (`tags.ts:1962`). A block sets the effect's `rounds` to 0.
  - **Action gates:** summonprevent, disarm and moveprevent hide actions in `availableUserActions` (R4); summonprevent and disarm have no handler check. Elementalseal is also a gate. In `interactions.json` these are kind `hides`.
  - Immunity cancels a new prevent of its `blocks` type (`tags.ts:230`).
- **Polarity** (`validators/combat.ts:1298` positive, `:1332` negative). Clear removes all positive, Cleanse all negative, except effects from persistent sources: pre-battle gear, keystones, skill, village, ranked, elementalMastery, bloodline, sageMode, sageModeAfter (`drizzle/constants.ts:4659`). Clear is itself negative, so Cleanse removes a pending Clear. Unclassified (neither can touch): clearprevent, cleanseprevent, injectjutsus, finalstand, diffuse, barrier, clone, copy, mirror, vamp, activatesagemode.
- **Seal** disables every bloodline-sourced effect on the holder from the moment it lands (`util.ts:921 isEffectEnabled`, `:938-945 sealCheck`): bloodline effects resolved later in its own casting action are already off.

## 4. Damage formula (one packet)

Raw value: `tags.ts:1352 damageCalc` via `tags.ts:1435 damageUser`. Pipeline: `damagePipeline.ts:655
applyDamageModifierPipelineToConsequences` → `damagePipeline.ts:501 computeDamagePacket`. Default config
`drizzle/constants.ts:4568-4575` (`stats_scaling` 1, `base_hits` 10, `curve` 1.6, `amplitude` 0.75,
`ep_normalization` 40, `gen_weight` 2, `advantage_min` 0.01, `advantage_max` 10); a battle may override it
(`process.ts:1450`).

```
# --- raw (damage, elementaldamage and pierce) ---
P = power + level*powerPerLevel; percentage → clamp [-100,100]          # power.ts:4-9 (PowerAttributes keeps power >= 0)
if calculation == formula and caster known:                             # tags.ts:1362
    atk = stats_scaling*sqrt(max(0,caster.offence)) + gen_weight*Σ sqrt(max(0,caster.gen))   # tags.ts:1364-1385
    def = stats_scaling*sqrt(max(0,target.defence)) + gen_weight*Σ sqrt(max(0,target.gen))   # gens = lower generals of effect.generalTypes, present on both
    adv = 1                                         if atk == 0 and def == 0                 # tags.ts:1336-1338
        = clamp(1 + amplitude*((atk/max(1,def))^curve - 1), advantage_min, advantage_max)  # tags.ts:1339-1345
    raw = calcHP(caster.level)/max(1,base_hits) * P/max(1,ep_normalization) * adv          # tags.ts:1331-1348
else:
    raw = P                                         # static, percentage, or no caster: flat  # tags.ts:1360
raw *= residualModifier   if not cast this round and residualModifier != 0                  # tags.ts:1392-1394
raw *= dmgModifier        if dmgModifier != 0                                                # tags.ts:1397-1399
raw *= weakness           dmgModifier of the highest-power matching Weakness (1 if none/0)  # tags.ts:1405-1431, process.ts:1516,1527
raw *= 1 - barrierAbsorb  instant only (cast this round, rounds 0)                           # tags.ts:1447-1452
# rounds > 0: nothing in the cast round; a residual packet on the holder's first action of each later round  # tags.ts:1447-1449,1464

# --- pipeline (damage/elementaldamage packets only; Pierce never enters) ---
# ratio(m) = 1 if m has no elements, else 1 if any m.element is in the packet's elements
#            (none = "None"), else 0. Generals ignored.                                    # tags.ts:2928-2935
# m counts only if active, not isNew, not cast this round, not blocked by its prevent        # damagePipeline.ts:166-185
d  = raw * Π(1 + curse.damageBonusPercent/100)   attacker's unsettled, enabled Curses       # damagePipeline.ts:701-712, curse.ts:12-29
# p = effective power in percentage points (25 = 25%); every % modifier divides by 100       # damagePipeline.ts:543-557
d *= Π(1 + p/100*ratio)    stage-1 % increases: skill/village/ranked/elementalMastery       # damagePipeline.ts:560, 320
d *= 1 + (60 + atkGearIncGiven + defGearIncTaken + Σ elemGearInc*ratio)/100   gear pool    # damagePipeline.ts:562-567
d *= Π(1 + p/100*ratio)    in-battle % increases: increasedamagegiven (attacker), increasedamagetaken (defender)  # :569, 322
B  = d                                                                                       # :571
d *= max(0, 1 - (50 + defGearDR + atkGearDRgiven + Σ|elemGearDR|*ratio)/100)   gear DR pool # :573-581
d *= Π max(0, 1 - |p|/100*ratio)   stage-1 % DR, then in-battle % DR (decreasedamagetaken defender, decreasedamagegiven attacker)  # :583-584
floor = B * max(0, 1 - 0.50) * (1 - 0.9)    # 5% of B = 10% of the post-system-DR hit       # :586-590, drizzle/constants.ts:4576,4583
d = max(d, floor)                                                                            # :591
d += Σ static increase*ratio                (bloodline: seal skips, opt-out respected)        # :593-602
d  = max(floor, d - Σ |static DR|*ratio)    (bloodline: seal skips, opt-out respected)        # :604-613
d *= 1 + (atkKeystoneIncGiven + defKeystoneIncTaken + Σ elemKeystoneInc*ratio)/100   keystone pool  # :615-619
d *= max(0, 1 - (defKeystoneDR + atkKeystoneDRgiven + Σ|elemKeystoneDR|*ratio)/100); d = max(floor, d)  # :621-628 (DR part skipped in the Diffuse test)
d *= Π(1 + p/100*ratio)  bloodline % increases; d *= Π max(0, 1 - |p|/100*ratio) bloodline % DR   # :630-646 (seal skips, opt-outs)
d  = max(floor, d)                                                                           # :648
```

Notes.
- Two point pools, both folded at battle start from unscoped percentage modifiers (`damagePipeline.ts:83-136`).
  **Gear** points are added to the 60 increase / 50 DR base points and applied before static modifiers.
  **Keystone** points are a separate pool, applied as one multiplier each way after static DR (`:615-628`), and
  keystone DR is skipped when DR is ignored (the Diffuse lethality test). Element-scoped gear and keystone
  modifiers join their own pool per packet, scaled by `ratio`. The stage-1 multiplicative list holds only skill, village, ranked and
  elementalMastery (`damagePipeline.ts:75-77, 320`).
- Gear and ordinary percentage DR run **before** static DR. Keystone and bloodline percentage DR run after it.
- Every percentage reduction multiplier is clamped at 0. The 10% floor is enforced after static DR, after
  keystones and after bloodline DR.
- Bloodline opt-outs (`allowBloodlineDamageIncrease/Decrease` on the damage tag, kept through the elementaldamage
  conversion) and Seal skip bloodline-sourced static and percentage modifiers (`damagePipeline.ts:214-229`).
- **Pierce** uses `raw` only: no Curse bonus, no pipeline, no floor (`process.ts:525` then `:618`), and reads the
  pre-pass stat snapshot (`process.ts:1528-1534`), so a stat change resolved in the same action reaches Damage
  but not Pierce.
- Drain, poison, wound, afterburn, reflect, recoil and parry returns don't use this formula.

### 4a. Mitigation is per packet

Final Stand checks each HP amount of each consequence separately against HP before the action's damage
(`process.ts:677-683, 1018`; `tags.ts:2209-2235`). Two 60-damage hits on a 100-HP Final Stand holder each pass
(100 − 60 ≥ 1), merge to 120 in `collapseConsequences` and kill; 60 damage plus 60 wound in one consequence
does the same. Mitigation also needs both the consequence's user and target present (`process.ts:1035`).

| Damage path | Shields soak? | Final Stand? | Source |
|---|---|---|---|
| Direct damage / elementaldamage (instant) | yes, holder's shields | yes, per packet | `process.ts:1038-1039, 981-1003, 1018` |
| Residual damage tick | yes | yes | `process.ts:1041-1042` |
| Pierce (instant or residual), not deferred | no; every enabled shield set to 0 | yes | `process.ts:1004-1018` |
| Wound in its own consequence | no | yes | `tags.ts:1825-1837`; `process.ts:984, 1044-1045` |
| Wound merged into another consequence from the same creator (residual tick, drain, poison) | yes, by the host's types; destroys shields if the host is Pierce | yes | `tags.ts:1821-1823, 1841` |
| Afterburn, HP drain, poison (ordinary) | no | no | `process.ts:1047, 1247-1256, 1325-1360` |
| Reflect, not deferred | quirk: the **reflector's own** remaining shields soak it (destroyed instead on a Pierce hit) | yes, the attacker's | `process.ts:965-971, 1054-1055, 1196-1236` |
| Recoil, not deferred | quirk: the shields of the **player the recoil holder hit**; never on Pierce hits | yes, the recoil holder's | `process.ts:965-971, 1057-1058, 1238-1246` |
| Parry return | yes, the attacker's shields | yes | `process.ts:887-896, 1038-1039` |
| Diffuse immediate part (any HP key, Pierce included) | yes, as ordinary damage; a deferred Pierce destroys the holder's shields only if positive Reflect is still on the original Pierce consequence when mitigation runs (if the attacker's own Diffuse defers that Reflect, it moves to a separate Reflect-typed consequence and the original field is cleared) | yes | `process.ts:1036-1060`; `damagePipeline.ts:460-474` |
| Diffuse immediate part of reflect or recoil aimed at a Diffuse holder | yes, the recipient's own shields | yes | `damagePipeline.ts:460-474` |
| Diffuse repayment | no | yes (bloodline Final Stand re-armed) | `diffuse.ts:111-119` |
| One Hit Kill | no | no (HP set in the main pass) | `process.ts:455-467, 1559-1569` |

The two quirk rows come from `targetShields` being built for `c.targetId` while `calcAdjustedDamage(user, …)` is
passed the attacker. It looks like a game bug but is current behaviour; see section 7.

### 4b. Post-damage readers and caps, in application order

D = a packet's `damage` after barrier, pipeline, Pierce and Parry split, before Diffuse and shields.
g = generals match, 0 or 1 (`tags.ts:2914-2927`): elements are never checked, no generals means 1, Pierce means 1.

```
1. Reader handlers (S10, process.ts:618-639). Each reads instant `damage` only, never residual.
   - lifesteal: lifesteal_hp += floor(D*p/100)*g                                       tags.ts:1944
   - reflect:   reflect += floor(D*p/100) or floor(min(p,D)), times g                  tags.ts:1773, :2856
   - recoil:    recoil = floor(...)*g. Overwrite: the last one wins (0 if generals miss). Pierce skipped.  tags.ts:1878-1879
   - afterburn: afterburn = min(prev + floor(...)*g, floor(0.6*D)). Pierce skipped.     tags.ts:1906-1912
   - vamp (casting action only): vampRatio += p/100 on each outgoing D>0 packet, Pierce included.  tags.ts:1971, :2974-2981
   - absorb:    absorb_<pool> += ceil(amt*g)/nPools, amt = D*p/100 (or the immediate part); runs after
                step 2 when the holder has Diffuse or the action has a Parry return.    tags.ts:205-211; process.ts:633-657
2. Diffuse (damagePipeline.ts:413-486): reflect pre-capped at 0.6*D (:424); lifesteal_hp *= remaining/D (:482);
   preShieldDamage := remaining, preDiffuseDamage := D (:478-479).
3. Heal modifiers (S14, tags.ts:1035-1069), unrounded: the healer's scale heal_hp, lifesteal_hp and vampRatio;
   the defender's scale absorb_hp. CP/SP heal and absorb are untouched.
4. mitigateConsequence, per packet (process.ts:956-1076): Consume credit = sum of HP keys before shields, if not
   self and not recoil (:1022-1031). Shields and Final Stand on damage, residual and wound; on the full uncapped
   reflect and recoil (quirk: see 4a) (:1055-1060). preShieldDamage recorded (:1063).
5. collapse per target and damageSource (util.ts:1180-1240): sums. vampHeal = Σ vampRatio*preShieldDamage (:1248).
   heal_hp/sp/cp take the max, not the sum (:1242).
6. applyConsequence (process.ts:1104-1340), in this order:
   leechBudget = floor(0.6*preShieldDamage)                                             :1107
   damage; then Vamp = min(floor(vampHeal), budget) if attacker HP>0 and uncursed (no target check)  :1141-1153
   residual, wound; heals (HP only if target alive)
   reflect = min(reflect, 0.6*(preDiffuse ?? preShield)), not rounded                    :1196-1236
   recoil: no cap                                                                        :1238
   afterburn: no further cap; no shields or Final Stand unless on the Diffuse path       :1247
   lifesteal = min(lifesteal_hp, budget - vampPaid) if target alive, attacker alive, attacker uncursed  :1261-1279
   absorb_hp = min(absorb_hp, 0.6*immediate damage), not rounded, if target alive and uncursed  :1281-1298
   absorb_sp/cp: no cap, curse check only                                                :1300-1323
   Siphon credit = HP actually lost from enemies, recoil excluded (:923-953). Reflect also credits Consume
   and Siphon (:1215-1228).
7. grantConversionShields (S16, process.ts:1380-1394): per alive recipient; the shared Consume+Siphon ratio is
   normalised to 100% when over (process.ts:916). New shields totalling over 100,000 are scaled
   proportionally, then each rounded down.
```

### 4c. Diffuse

`applyDiffuseToConsequences` (`damagePipeline.ts:381`, `diffuse.ts:19-84`). Active means rounds > 0 and not
sealed; there is no next-round wait (`process.ts:509-515`, `util.ts:905-913`). Only the strongest Diffuse counts
(highest power, ties by id), fraction `min(99, power)/100`, its `delayRounds` (1-20, default 3).

- **Lethality test, all or nothing per action.** Every HP packet heading to the holder in the action (damage,
  residual, wound, afterburn, drain, poison) plus reflect and recoil aimed at them is summed. If the sum ≥
  current HP (shields not counted), nothing is deferred (`diffuse.ts:26-48`). Two individually non-lethal packets
  can make deferral fail.
- **Two damage bases.** For the test, damage and residual packets (not Pierce) are recomputed without the
  holder's DR (stage-1, in-battle, static, bloodline, gear and keystone DR dropped), keeping the 50% system DR,
  all increases, the Curse bonus, the floor and the Parry fraction (`damagePipeline.ts:427-449`). Everything else
  counts as it stands; reflect is first capped at 60%. The **deferred** amount comes from the normally modified
  packet: debt = current value × fraction (`damagePipeline.ts:454`; `diffuse.ts:62`).
- **Pierce** can be deferred. Its immediate part is then soaked by shields as ordinary damage (`process.ts:1036-1040`).
  The shields are still destroyed if positive Reflect is left on the original Pierce consequence when mitigation
  runs, because reflect is mitigated with the hit's own types (`process.ts:1054-1055`). If the attacker's own
  Diffuse defers that Reflect, it moves to a separate Reflect-typed consequence and the original field is
  cleared (`damagePipeline.ts:460-474`), so nothing is destroyed.
- **The immediate part** goes through shields and Final Stand, including afterburn, drain and poison, which
  otherwise skip both (`process.ts:1047-1053`). Absorb and Lifesteal see only the immediate part.
- **Repayment** is S6: the holder's next `delayRounds` acting rounds, `remaining/turnsLeft` each, through Final
  Stand only.

## 5. Stacking and caps

Numbers are in `rules.json`, read from source by `_build/rules.py`.

| Rule | Value | Source |
|---|---|---|
| Same tag, same caster, same target | stacks (`BATTLE_TAG_STACKING = true`) | `drizzle/constants.ts:2437`, `util.ts:962` |
| % increases | multiply: Π(1 + p/100), p in percentage points (law 9); gear and keystone points are summed into their own pools first | `damagePipeline.ts:560-569` |
| % reductions | multiply: Π max(0, 1 − p/100), floor 10% of the post-system hit (law 10) | `damagePipeline.ts:573-648`, `drizzle/constants.ts:4576` |
| Copy / Mirror | 4 held per caster; priority tiers; no passive or gear sources | `drizzle/constants.ts:4610-4690` |
| Lifesteal + vamp | floor(0.6 × pre-shield immediate hit), shared, Vamp paid first | `constants.ts:80`, `process.ts:1107` |
| Reflect | 0.6 × pre-Diffuse hit, not rounded, after the shield soak | `constants.ts:86`, `process.ts:1196-1200` |
| Absorb | HP share only: 0.6 × immediate hit, not rounded; CP/SP uncapped | `constants.ts:89`, `process.ts:1281-1323` |
| Afterburn | floor(0.6 × hit) per hit, at handler time | `constants.ts:92`, `tags.ts:1906-1912` |
| Recoil, poison, drain | no cap | `process.ts:1238-1246` |
| Parry | sums to 100% | `drizzle/constants.ts:4578` |
| Diffuse | strongest one only, power ≤ 99%; delayRounds 1–20, default 3; all or nothing per action against current HP | `drizzle/constants.ts:4579-4580`, `validators/combat.ts:846-851`, `diffuse.ts:33-50` |
| Consume + Siphon | one shared 100% conversion ratio per fighter per action; new conversion shields ≤ 100,000 per fighter per action, scaled then rounded down | `process.ts:916, 1386-1390` |
| Only one counts | strongest stun; highest-power matching weakness; strongest Diffuse; largest range bonus and lowest signed cooldown modifier per basic action; one timecompression and one timedilation at a time | `turn.ts:160`, `tags.ts:1405`, `diffuse.ts:33`, `actions.ts:434-485`, `tags.ts:2499` |
| Heals in one action | largest per pool, not the sum | `util.ts:1242` |
| Shield HP | a shield tag's health ≤ 100,000 | `drizzle/constants.ts:2491`, `validators/combat.ts:768` |

## 6. Base fields every combat tag has

`validators/combat.ts:121 BaseAttributes`: `rounds` (int 0-100), `power` (−100..100; PowerAttributes makes it ≥0),
`powerPerLevel`, `direction`, `target` (INHERIT | SELF | COORDINATES), `coordinateTargeting`, `friendlyFire`
(ALL | FRIENDLY | ENEMIES), `calculation`, `timeTracker`, plus animation and sound fields. Effective power =
`power + level * powerPerLevel`. Each `tags/<tag>.yaml` lists the tag's own and inherited fields, with where each
inherited one comes from.

## 7. Likely game bugs (current behaviour, not intended)

Recorded so tools model what the engine does. Game code is read-only for us; raise these with the director.

- **Reflect and recoil are soaked by the wrong shields.** In `mitigateConsequence`, `targetShields` holds the
  shields of the consequence's target (the original defender), while `calcAdjustedDamage(user, c.reflect, …)`
  and the recoil call are passed the attacker (`process.ts:965-971, 1043, 1054-1058`). So reflected damage is
  soaked by the reflector's own remaining shields, and recoil by the shields of the player the recoil holder hit.
  The `"reflect"` shield bypass at `process.ts:983` never fires, because `c.types` comes from the original hit.
- **A deferred Pierce with Reflect still breaks shields.** When the defender's Diffuse defers a Pierce and
  positive Reflect is still on that original consequence when mitigation runs, reflect mitigation runs with
  `c.types` containing `"pierce"`, which runs the destroy branch on the defender's shields after they soaked the
  immediate part (`process.ts:1004-1016, 1054-1055`). If the attacker's own Diffuse defers the Reflect, it is
  moved to a separate Reflect-typed consequence and cleared from the original (`damagePipeline.ts:460-474`), and
  the shields survive.
- **A blocked Curse payout is lost** (may be intended). `settleCurse` zeroes `storedHealing` before the healprevent check
  (`tags.ts:1690`, called from `turn.ts:100`).
- **Stale comment.** `constants.ts:251` says lifesteal matches "generals and elements"; the code checks generals
  only (`tags.ts:2914-2927`).
