"""Hand-checked corrections layered over data.json by kb.py, and the link edits that edges.py applies to
interactions.json. Every line here was re-read against studie-tech/TheNinjaRPG @ 29cd91b during the PR #129
review (findings H1-H5, M1-M5, L2, Nov 22 2026). Cite-first: when the game moves, re-read the cited lines
before keeping a sentence.

kb.py reads STAGE, BEHAVIOR, LIVE, APPLIES and PREVENT_CHECK. edges.py reads KIND_DEFS and EDGE_OPS.
"""

# ---------------------------------------------------------------------------------------------------------
# Stages: engine.md section 2 (S0-S16). process.ts applyEffects :357-711, actions.ts performAction cast prep.
# ---------------------------------------------------------------------------------------------------------
STAGE_NAMES = {
    "S0": "cast prep", "S1": "ground pass", "S2": "copy and mirror", "S3": "main pass",
    "S4": "instant-kill accounting", "S5": "Consume/Siphon register", "S6": "Diffuse repayment",
    "S7": "damage pipeline", "S8": "pierce", "S9": "Parry split", "S10": "post-damage readers",
    "S11": "Parry returns", "S12": "Diffuse deferral", "S13": "delayed Absorb", "S14": "heal adjustments",
    "S15": "mitigate and apply", "S16": "wrap-up",
}

_MAIN = "S3 main pass"
STAGE = {
    "absorb": "S10 post-damage readers; S13 instead when the action has Parry returns or the holder has Diffuse; paid in S15",
    "activatesagemode": _MAIN,
    "afterburn": "S10 post-damage readers; paid in S15",
    "barrier": "S0 cast prep (path absorb) and S1 ground pass; no main-pass handler",
    "buffprevent": _MAIN, "cleanse": _MAIN, "cleanseprevent": _MAIN, "clear": _MAIN, "clearprevent": _MAIN,
    "clone": "S1 ground pass",
    "consume": "S5 register (casting action on); credited in S6 and S15; shield granted in S16",
    "copy": "S2 copy and mirror",
    "curse": "S3 main pass (unranked, last); HP-loss stored in S4, S6 and S15; a new curse is marked ready in S16",
    "damage": "S3 main pass (raw written) -> S7 damage pipeline -> S15 mitigate and apply",
    "debuffprevent": _MAIN, "decreaseaggro": _MAIN, "decreasecooldown": _MAIN + " (unranked)",
    "decreasedamagegiven": "S7 damage pipeline", "decreasedamagetaken": "S7 damage pipeline",
    "decreaseheal": "S14 heal adjustments (own pass, after Diffuse deferral and delayed Absorb)",
    "decreasemastery": _MAIN, "decreasemaxpools": _MAIN + " (unranked)", "decreasepoolcost": _MAIN,
    "decreasepotency": "S0 cast prep (rewrites cast power); handler in S3 main pass",
    "decreasestat": _MAIN,
    "diffuse": "S3 main pass (handler text only); S6 repayment; S12 deferral",
    "disarm": _MAIN + "; action gate in availableUserActions",
    "drain": "S3 main pass (writes the consequence despite its post-pierce rank); applied in S15",
    "elementaldamage": "S0 cast prep (becomes damage)",
    "elementalseal": _MAIN + "; action gate in availableUserActions",
    "finalstand": "S3 main pass (land roll); floors HP in S6 and S15",
    "flee": _MAIN, "fleeprevent": _MAIN,
    "heal": "S3 main pass -> S14 heal adjustments -> S15 applied",
    "healprevent": _MAIN, "immunity": _MAIN + " (unranked)", "increaseaggro": _MAIN,
    "increasecooldown": _MAIN + " (unranked)",
    "increasedamagegiven": "S7 damage pipeline", "increasedamagetaken": "S7 damage pipeline",
    "increaseheal": "S14 heal adjustments (own pass, after Diffuse deferral and delayed Absorb)",
    "increasemastery": _MAIN, "increasemaxpools": _MAIN + " (unranked)", "increasepoolcost": _MAIN,
    "increasepotency": "S0 cast prep (rewrites cast power); handler in S3 main pass",
    "increaserange": _MAIN + " (unranked)", "increasestat": _MAIN, "injectjutsus": _MAIN,
    "lifesteal": "S10 post-damage readers; paid in S15",
    "mirror": "S2 copy and mirror",
    "move": "S1 ground pass",
    "moveprevent": _MAIN + "; action gate in availableUserActions",
    "onehitkill": "S3 main pass (sets HP to 0 directly); S4 credits Curse",
    "onehitkillprevent": _MAIN,
    "parry": "S9 Parry split; S11 returns",
    "pierce": "S8 pierce (after the damage pipeline); applied in S15",
    "poison": "S3 main pass (writes the consequence despite its post-pierce rank); applied in S15",
    "recoil": "S10 post-damage readers; applied in S15",
    "redirection": _MAIN,
    "reflect": "S10 post-damage readers; applied in S15",
    "rob": _MAIN, "robprevent": _MAIN, "seal": _MAIN, "sealprevent": _MAIN,
    "shield": "S3 main pass (land roll); soaks in S15",
    "siphon": "S5 register (casting action on); credited in S6 and S15; shield granted in S16",
    "stealth": _MAIN,
    "stun": "S3 main pass (land roll); AP read outside applyEffects (turn.ts:159-182)",
    "stunprevent": _MAIN,
    "summon": "S1 ground pass",
    "summonprevent": _MAIN + "; action gate in availableUserActions",
    "timecompression": _MAIN, "timedilation": _MAIN,
    "vamp": "S10 post-damage readers (unranked, last); casting action only; paid in S15",
    "visual": "S1 ground pass (cosmetic)",
    "weakness": _MAIN,
    "wound": "S10 post-damage readers; applied in S15",
}

# ---------------------------------------------------------------------------------------------------------
# When the effect first changes damage, healing or what the holder may do (M4). Overrides kb.py's LIVE.
# ---------------------------------------------------------------------------------------------------------
_TICK_LIVE = "rounds 0: casting action; rounds > 0: holder's first action in the round after cast, then once per round"
_POT_LIVE = ("holder's next jutsu cast after the casting action (same round possible); ground: the next cast from "
             "the tile after the placing action")
LIVE = {
    "damage": _TICK_LIVE, "pierce": _TICK_LIVE, "heal": _TICK_LIVE,
    "increasepotency": _POT_LIVE, "decreasepotency": _POT_LIVE,
    "seal": ("casting action, right after its land roll (holder's bloodline effects resolved later in that action); "
             "then every later action"),
    "poison": "holder's first action in the round after cast; then every holder action",
    "consume": "its casting action (no next-round wait)",
    "siphon": "its casting action (no next-round wait)",
    "diffuse": "its casting action (no next-round wait)",
    "vamp": "its casting action only",
    "increaserange": "as soon as it is on the holder (no next-round wait)",
    "increasecooldown": "as soon as it is on the holder (no next-round wait)",
    "decreasecooldown": "as soon as it is on the holder (no next-round wait)",
    "summonprevent": "action gate while active with rounds left and not cast this round",
    "disarm": "action gate while active with rounds left and not cast this round",
    "elementalseal": "action gate while active with rounds left and not cast this round",
    "stun": "AP cut from the round after it lands",
    "injectjutsus": ("as soon as it has resolved and is enabled: no next-round wait, so the jutsu can be used later in "
                     "the casting round (actions.ts:148-160)"),
}

APPLIES = {
    "damage": "rounds 0: once, on cast; rounds > 0: nothing on cast, then once a round on the holder's first action",
    "pierce": "rounds 0: once, on cast; rounds > 0: nothing on cast, then once a round on the holder's first action",
    "heal": "rounds 0: once, on cast; rounds > 0: nothing on cast, then once a round on the holder's first action",
    "poison": "on every action the holder takes, from the round after cast (no once-a-round limit)",
}

# ---------------------------------------------------------------------------------------------------------
# How each prevent check runs (H5). tags.ts:2991 preventCheck compares createdRound only when passed the effect.
# ---------------------------------------------------------------------------------------------------------
_AGE = "age-compared: blocks only effects created in a later round than the prevent"
_ANY = "any age: any active prevent blocks it, including a pending effect cast earlier, which then ends"
PREVENT_CHECK = {
    "clear": _ANY + " (tags.ts:1155)", "cleanse": _ANY + " (tags.ts:1165)", "flee": _ANY + " (tags.ts:1531)",
    "rob": _ANY + " (tags.ts:2356)", "onehitkill": _ANY + " (tags.ts:2317)",
    "seal": _ANY + "; re-checked on each of the holder's turns (tags.ts:2402)",
    "move": "any age, the mover's own moveprevent (tags.ts:2273); moveprevent also hides move actions",
    "vamp": "any age, the Vamp caster's own healprevent, read directly with no roll (tags.ts:1962-1965)",
    "curse": "buffprevent age-compared on landing; healprevent any age on the expiry payout (tags.ts:1664, 1690)",
    "summon": "action gate only: summonprevent hides summon jutsu (actions.ts:231-237); no handler check",
    "copy": "age-compared, against the Copy caster's own buffprevent (tags.ts:456)",
    "redirection": _AGE + " (tags.ts:2561)",
}
PREVENT_CHECK_DEFAULT = _AGE

# ---------------------------------------------------------------------------------------------------------
# Behavior text (replaces data.py's). Sources are in the verification notes and each tag's source list.
# ---------------------------------------------------------------------------------------------------------
BEHAVIOR = {
    "copy": ("The caster's own buffprevent can block it. Otherwise it rolls power% once, in its casting action, to clone the target's best positive effects onto the caster for the copy's rounds; the target keeps theirs. It holds 4 at most at once, per caster. Order of preference: damage-given up or damage-taken down, then lifesteal, then absorb or reflect, then shield, then increaseheal, then increasestat. Passive and gear sources can't be copied. A miss copies nothing and does not set the Copy's rounds to 0 (tags.ts:462, 507-518)."),
    "mirror": ("Rolls power% once, in its casting action, to clone up to 4 of the caster's own active negative effects onto the target for the mirror's rounds. The caster keeps their copies. Order of preference: damage-taken up or damage-given down first, then afterburn, then poison or pool-cost, then wound, then anything else. Raw damage, pierce, clear, stun, time compression and four prevents are excluded, and so is anything from bloodline, gear or other passives. The target's debuffprevent blocks it. A miss passes nothing and does not set the Mirror's rounds to 0 (tags.ts:547, 621-626)."),
    "injectjutsus": ("Adds the listed jutsu to the holder's action list while it is active and enabled. Unlike the hiding gates it has no not-cast-this-round wait, so a grant that has resolved can expose its jutsu later in its own casting round (actions.ts:148-160). Neither Clear nor Cleanse can remove it."),
    "damage": (
        "Formula damage (the default) scales a baseline by power and by an attack-vs-defence advantage. The "
        "baseline is max HP at the attacker's level divided by base hits. Attack and defence are the square roots "
        "of the caster's Offence and the target's Defence plus double-weighted lower generals, with negatives "
        "treated as 0. The advantage is 1 when both sides are 0 and is otherwise clamped between 0.01 and 10. "
        "Static and percentage damage use effective power as a flat number, and percentage power is capped at "
        "100. A non-zero dmgModifier, the highest-power matching Weakness and, on later-round ticks, a non-zero "
        "residualModifier multiply the number. An instant hit through a barrier loses the barrier's share. It "
        "then runs the damage pipeline: the attacker's Curse bonus, increases, the 50% system reduction and other "
        "reductions, a floor at 10% of the post-system hit, static modifiers, keystones, and finally bloodline "
        "modifiers, subject to Seal and the allowBloodline opt-outs. With rounds 0 it hits on cast. With rounds "
        "above 0 the casting action deals nothing; it then ticks as residual damage (x residualModifier, no "
        "barrier cut) once per round on the holder's first action of each later round. A round in which the "
        "holder doesn't act gives no tick."),
    "pierce": (
        "Pierce computes its raw number the same way as Damage: formula, static or percentage, with dmgModifier, "
        "residualModifier, Weakness, and the barrier cut on instant hits. It resolves after the damage pipeline, "
        "so no Curse bonus, damage increase, damage reduction or damage floor applies. It reads the stats from "
        "before the action's main pass, so a stat change resolved in the same action doesn't reach it. It isn't "
        "soaked by shields. Instead it sets every enabled shield on the target to 0, and Final Stand still "
        "applies. If the target's Diffuse defers part of it, shields soak the immediate part like ordinary damage "
        "and are destroyed only if positive Reflect is still on that Pierce hit when mitigation runs (if the "
        "attacker's own Diffuse defers that Reflect, it moves to a separate hit and the shields survive). Parry, Recoil and Afterburn ignore Pierce. Lifesteal, Absorb, Reflect, Wound and "
        "Vamp read an instant Pierce hit, and Lifesteal, Absorb and Reflect skip their general filter for it. "
        "Curse stores HP lost to it. With rounds above 0 it deals nothing on cast and ticks on later rounds."),
    "decreasedamagetaken": (
        "Reduces Damage and Elemental Damage packets the holder takes. It doesn't touch Pierce, drain, poison, "
        "wound, afterburn or Diffuse repayment. It works from the round after it lands, and Buffprevent can block "
        "it. Each percentage effect multiplies by (1 - power%), clamped at 0, after all increases and the 50% "
        "system reduction. Percentages are percentage points, divided by 100 like increases. Pre-battle percentages sit in two "
        "pools: gear DR points join the 50 system points, before static values; keystone DR points are summed "
        "into a separate multiplier applied after static values, and skipped when DR is ignored (the Diffuse "
        "lethality test). Static values are subtracted after the ordinary percentage stage. Bloodline percentages "
        "apply last; Seal and the damage tag's allowBloodlineDamageDecrease opt-out can switch bloodline ones off. "
        "With elements set, it only affects packets that share an element, and packets without elements count as "
        "None. Damage never drops below 10% of the boosted hit after the system reduction."),
    "diffuse": (
        "While active (rounds above 0 and not sealed, from the action it is cast), the holder defers part of the "
        "damage aimed at them in each action. Only their strongest Diffuse counts, at most 99%, using its "
        "delayRounds (1-20, default 3). It is all or nothing per action. All HP damage, reflect and recoil heading "
        "to the holder in that action are added up, and if the total reaches current HP (shields not counted), "
        "nothing is deferred. For that test, ordinary and residual damage are recomputed without the holder's "
        "damage reduction but with the 50% system reduction, all increases and any Parry split. Everything else "
        "(Pierce, wound, afterburn, drain, poison, reflect, recoil) counts as it stands. When the test passes, "
        "power% of each already-reduced packet becomes debt. The debt is repaid in equal parts on the holder's own "
        "actions over their next delayRounds acting rounds, at the start of the action. Repayment skips shields, "
        "damage reduction and Absorb, respects Final Stand, and continues after the effect ends. The immediate "
        "part goes through shields and Final Stand as ordinary damage. That includes Pierce, which shields then "
        "soak instead of breaking unless positive Reflect is still on that Pierce hit when mitigation runs (the "
        "attacker's own Diffuse deferring the Reflect moves it off the hit), and afterburn, drain and poison, which otherwise skip both. Absorb and "
        "Lifesteal only see the immediate part. It can't be cleansed, prevented or copied."),
    "shield": (
        "Rolls power% to appear, then acts as a separate HP bar worth its health field (up to 100,000). Direct, "
        "residual and parry-return damage drain the holder's shields before HP, as does the immediate part of "
        "anything Diffuse deferred. Pierce isn't soaked: it sets every enabled shield on the target to 0. When the "
        "target's Diffuse deferred part of it, the immediate part is soaked instead, and the shields are still "
        "destroyed only if positive Reflect remains on that Pierce hit when mitigation runs. Afterburn, drain, poison, One Hit Kill and Diffuse repayment never touch "
        "shields. Wound skips them only when it arrives on its own rather than merged into another hit from the "
        "same caster. Quirk (likely a game bug): reflect and recoil damage are soaked by the shields of the other "
        "side of the original hit, not the shields of the player taking it. It's positive, so Clear removes it "
        "and Copy can take it."),
    "finalstand": (
        "Rolls power% every time it resolves, which is every action while it lasts, and the first failed roll "
        "sets its rounds to 0 and ends it (tags.ts:2238-2255). While active, each separate damage packet that would leave the holder below 1 "
        "HP is cut to leave exactly 1 HP. Each packet is checked against HP as it stood before the action's "
        "damage, so several packets that are each survivable can still kill together (two 60s on a 100-HP holder "
        "kill). It applies to direct, residual, Pierce, wound, parry return, reflect and recoil damage, to the "
        "immediate part of deferred damage and to Diffuse repayment. It does not apply to ordinary afterburn, "
        "drain, poison or One Hit Kill. A bloodline version needs to be active and unsealed, and re-arms for one "
        "round when it fires. Neither Clear nor Cleanse removes it."),
    "clearprevent": (
        "A prevent-type status that rolls power% once to land. Once landed, it blocks every Clear resolving on the "
        "holder, whenever that Clear was cast. A multi-round Clear that was already pending is stopped on its next "
        "tick and ends. Neither Clear nor Cleanse removes it, but Immunity can cancel a new one."),
    "cleanseprevent": (
        "A prevent-type status that rolls power% once to land. Once landed, it blocks every Cleanse resolving on "
        "the holder, whenever that Cleanse was cast. A multi-round Cleanse that was already pending is stopped on "
        "its next tick and ends. Neither Clear nor Cleanse removes it, but Immunity can cancel a new one."),
    "sealprevent": (
        "A prevent-type status that rolls power% once to land. While active, it blocks any Seal on the holder "
        "regardless of when the Seal was cast. Seal re-checks on each of the holder's turns, so a Sealprevent that "
        "lands after a Seal ends that Seal at the holder's next turn. A bloodline-sourced Sealprevent is itself "
        "switched off while a Seal is active. Clear removes it, and Immunity can cancel a new one."),
    "robprevent": (
        "A prevent-type status that rolls power% once to land. While active, it blocks every Rob attempt on the "
        "holder, including the per-round attempts of a Rob cast before it, and a blocked Rob ends. Rob only works "
        "on non-AI targets in COMBAT battles. Clear removes it, and Immunity can cancel a new one."),
    "onehitkillprevent": (
        "A prevent-type status that rolls power% once to land. While active, it blocks every One Hit Kill roll on "
        "the holder, including later ticks of a multi-round One Hit Kill cast before it, and a blocked One Hit "
        "Kill ends. Clear removes it, and Immunity can cancel a new one."),
    "summonprevent": (
        "A prevent-type status that rolls power% once to land. While it is active with rounds left (and not cast "
        "this round), jutsu with a summon tag are removed from the holder's action list, and the server enforces "
        "this. The summon handler never checks it, so summons already on the field stay, and items with a summon "
        "tag are not filtered. Cleanse removes it, Mirror can pass it, and Immunity can cancel a new one."),
    "fleeprevent": (
        "A prevent-type status that rolls power% once to land. While active, it blocks every Flee roll by the "
        "holder, including the per-round rolls of a Flee cast before it, and a blocked Flee ends. Immunity can "
        "cancel a new one."),
    "moveprevent": (
        "A prevent-type status that rolls power% once to land. While active with rounds left, it hides basic "
        "move, the replacement technique and every jutsu with a move tag (server-enforced). It also blocks any "
        "move ground effect the holder casts, whatever its age, and blocks Redirection cast on the holder in a "
        "later round. Immunity can cancel a new one."),
    "healprevent": (
        "A prevent-type status that rolls power% once to land. It blocks Heal, Lifesteal and Absorb cast on the "
        "holder in a later round (all pools). Any active healprevent on a Vamp caster blocks that Vamp outright, "
        "with no roll or age check, and any active healprevent on a Curse holder at expiry blocks the payout and "
        "the stored healing is lost. Immunity can cancel a new one."),
    "heal": (
        "Restores power x 10 if static, or power% of the target's max pool if percentage, to each listed pool. "
        "With rounds 0 it heals on the casting action. With rounds > 0 it heals nothing then, and heals once per "
        "round on the holder's (target's) first action of each later round. A healprevent from an earlier round "
        "blocks it on landing, and it blocks all pools. The healer's increaseheal/decreaseheal scale only the HP "
        "part. Several heals reaching one target in one action don't stack: the largest per pool applies. HP is "
        "restored only if the target is still alive, up to the effective max. Clear removes a heal-over-time."),
    "increaseheal": (
        "Scales the HP healing the holder produces: Heal's HP part, Lifesteal, Vamp, the Curse payout, and Absorb's "
        "HP part on the holder. Chakra and stamina healing are not changed. It runs in its own pass after Diffuse "
        "deferral, unrounded. Buffprevent blocks it, and Copy can take it."),
    "decreaseheal": (
        "Shrinks the HP healing the holder produces, the same way increaseheal grows it: Heal's HP part, "
        "Lifesteal, Vamp, the Curse payout and Absorb's HP part. Chakra and stamina healing are not changed. "
        "Debuffprevent blocks it."),
    "absorb": (
        "A buff on the holder, live from the round after it lands. For each instant hit on the holder whose "
        "generals match (elements ignored; Pierce always matches), it takes power% of the immediate damage: the "
        "hit after the pipeline and the Parry split, before shields. It is read after Diffuse when the holder has "
        "Diffuse or the action has a Parry return. The hit itself is not reduced. The amount is rounded up, then "
        "split evenly across poolsAffected with no further rounding, and stacked Absorbs add. The HP share is "
        "scaled by the holder's increaseheal/decreaseheal, capped at 0.6 x the immediate damage (not rounded), and "
        "paid only if the holder is still alive. The CP/SP shares have no cap, ignore heal modifiers and pay even "
        "on a killing hit. Residual ticks don't feed it. A healprevent from an earlier round blocks it, and an "
        "unsettled Curse on the holder stops all of it."),
    "lifesteal": (
        "A buff on the attacker, live from the round after it lands. For each instant hit the holder deals, Pierce "
        "included, it stores floor(hit x power/100), percentage only. The hit is taken after the pipeline and the "
        "Parry split, before Diffuse and shields. If lifesteal has generals, they must overlap the damage tag's "
        "generals ('Highest' expands), but Pierce always passes and elements are never checked. Diffuse scales "
        "the stored amount to the immediate part, and the attacker's heal modifiers scale it, unrounded. It pays "
        "min(stored, floor(0.6 x pre-shield immediate damage) - Vamp already paid). It pays only if the target is "
        "still alive after the whole packet (damage, reflect, recoil, afterburn), the attacker is alive and the "
        "attacker holds no unsettled Curse. Residual ticks don't feed it, and a healprevent from an earlier round "
        "blocks it. Copy can take it."),
    "vamp": (
        "Lives on the casting jutsu and acts only on the action that casts it, in the post-damage pass. It adds "
        "power/100 to every instant damage packet the caster deals to others in that action. Pierce counts; "
        "residual ticks don't. The caster's heal modifiers scale that ratio. Heal = floor(sum of ratio x "
        "pre-shield immediate damage), capped at floor(0.6 x that damage) and paid before Lifesteal from the same "
        "budget. It pays even when the hit kills the target, but not if the caster is at 0 HP or holds an "
        "unsettled Curse. Any active healprevent on the caster blocks it outright, with no roll and no "
        "creation-round check."),
    "afterburn": (
        "A debuff on the holder, live from the round after it lands, with no prevent check. For each instant "
        "non-Pierce hit the holder takes whose generals match (elements ignored), each Afterburn adds floor(hit x "
        "power/100), or floor(min(power, hit)) if static. The running total for that hit is clamped to floor(0.6 x "
        "hit), using the hit after the pipeline and Parry, before Diffuse. Diffuse can defer part of it. Otherwise "
        "it lands on the holder after Reflect and Recoil with no further cap, and neither shields nor Final Stand "
        "stop it. Afterburn from several hits in one action is summed, each hit under its own cap."),
    "recoil": (
        "A debuff on the attacker, live from the round after it lands. For each instant non-Pierce hit the holder "
        "deals, each Recoil sets (does not add) that hit's recoil to floor(hit x power/100), or floor(min(power, "
        "hit)) if static, times the generals match. The last Recoil in resolution order wins, and one whose "
        "generals don't match writes 0. There is no 60% or other cap. Quirk (likely a game bug): the amount is "
        "soaked by the shields of the player the holder hit, then the holder's Final Stand applies; it is applied "
        "after Reflect and summed across hits. A debuffprevent from an earlier round blocks it."),
    "reflect": (
        "A buff on the defender, live from the round after it lands. For each instant hit the holder takes whose "
        "generals match (elements ignored; Pierce always matches), each Reflect adds floor(hit x power/100), or "
        "floor(min(power, hit)) if static. The hit is taken after the pipeline and Parry, before Diffuse. The "
        "holder still takes the full hit. Quirk (likely a game bug): the uncapped total is first soaked by the "
        "reflecting holder's own remaining shields (destroying them instead if the hit was Pierce), then the "
        "attacker's Final Stand applies. Then it is capped at 0.6 x the pre-Diffuse hit (not rounded) and dealt to "
        "the attacker, even if the defender died. If the attacker has Diffuse, Reflect is capped at 0.6 x hit "
        "before the split. The returned damage credits Curse, enmity and Consume/Siphon. A buffprevent from an "
        "earlier round blocks it, and Copy can take it."),
    "consume": (
        "A buff on the caster with no prevent check, live from its own casting action. With rounds 0 it converts "
        "only that action. Each action, every active Consume and Siphon on one fighter adds power/100 to one "
        "shared ratio. If the total is over 100%, each is scaled to its share of 100%. Consume credits the "
        "caster's non-recoil damage to other fighters: per packet, the pre-shield, post-Diffuse sum of damage, "
        "residual, wound, afterburn, drain and poison, plus Reflect after its cap and repaid Diffuse debt. All "
        "Consume on a fighter merges into one shield with the longest shieldRounds. After the action, if the "
        "fighter is alive, the new conversion shields are scaled down proportionally when they total over 100,000 "
        "HP, then each is rounded down. The damage itself is not reduced. Heal modifiers don't apply."),
    "siphon": (
        "A buff on the holder, live from its casting action. A buffprevent from an earlier round blocks it. It "
        "credits HP the holder actually loses to other fighters in the action: after shields and Final Stand, "
        "limited to HP left, with recoil and self-damage excluded, plus Reflect taken and repaid Diffuse debt. The "
        "hit itself is not reduced. It shares the 100% conversion ratio (scaled when over) and the 100,000 HP "
        "new-shield cap (proportional, then rounded down) with Consume. Siphons with the same shieldRounds merge, "
        "and different ones make separate shields. Shields are granted after the action only if the holder is "
        "alive, and heal modifiers don't apply. Clear removes it."),
    "increasepotency": (
        "On the casting action its handler runs once; a buffprevent from an earlier round blocks it (rounds 0), "
        "and after that the handler only shows text. It changes power when the holder casts a jutsu (not a basic "
        "action or item) on any later action, later in the casting round included. Matching tags are affectedTag "
        "or 'all'; 'none' matches by element only. affectedElements match the tag's elements or the jutsu's "
        "elementClassification. A matching tag's power becomes max(0, base + sum of flat) x max(0, 1 + sum of "
        "%/100), with level scaling baked in at cast and percentage tags capped at 100. Potency on the ground "
        "applies to any fighter who casts from that tile, from the action after it was placed, if they pass its "
        "friendlyFire against its creator (default ALL). Bloodline potency is off under Seal."),
    "decreasepotency": (
        "Mirror of increasepotency with negative flat and % terms. A debuffprevent from an earlier round blocks it "
        "on landing. It applies to the holder's jutsu cast on any later action, same round included, using the "
        "same formula and clamps. The 0 floor means stacked decreases can't make power negative. Ground copies "
        "follow the same tile, not-new and friendlyFire rules."),
    "seal": (
        "Its handler runs on the casting action at the seal rank of the main pass: after damage, heal, onehitkill "
        "and rob, before stun and summon. Any active sealprevent on the holder rolls its power%, with no "
        "creation-round check; a landed one always blocks. Then the seal rolls power% to land. Once landed it "
        "counts as active at once, so the holder's bloodline effects resolved later in the same action are "
        "already off: Consume/Siphon registration, Diffuse, bloodline damage modifiers on this action's hits, "
        "Pierce, post-damage readers, heal modifiers and Final Stand. From the next action on, same round "
        "included, it also turns off bloodline potency, injected jutsu, range and cooldown. It re-runs once a "
        "round on the holder's first action, where an active sealprevent can still remove it."),
    "poison": (
        "Resolves in the main pass on every action. A debuffprevent from an earlier round blocks it (rounds 0); a "
        "newer one never does. In the casting round it only shows text. From the next round, every action the "
        "holder takes deals floor((CP cost + SP cost) x power/100) HP, with no once-per-round limit. The costs are "
        "that action's after pool-cost modifiers, each floored at 0, and HP cost is ignored. The damage is "
        "credited to the poison's caster and skips shields and Final Stand except on the Diffuse path."),
    "drain": (
        "Each round it removes a flat amount, or power% of the max, from the chosen pools (HP, chakra, stamina). "
        "It writes its consequence in the main pass, despite its post-pierce sort rank, and the HP part skips "
        "shields and Final Stand except on the Diffuse path. Debuffprevent from an earlier round blocks it. When "
        "mirrored, its power is divided by the mirror's rounds."),
    "wound": (
        "When cast, it records the damage its caster dealt to the target in that action (instant Pierce included). "
        "Each later round it deals power% of that recorded hit again. Ticking in its own consequence, that damage "
        "skips shields but not Final Stand; merged into another consequence from the same caster (a residual "
        "tick, drain or poison), it is soaked by shields like that host, and destroys them if the host is Pierce. "
        "It's mirror-eligible."),
    "onehitkill": (
        "Rolls power% to set the target's HP to 0 outright, directly in the main pass. It skips shields, damage "
        "reduction and Final Stand. Any active onehitkillprevent blocks it, including later ticks of an older "
        "multi-round One Hit Kill. The HP removed counts as damage dealt and is credited to Curse."),
    "weakness": (
        "Lands on a roll of power%. While active, damage or pierce from the listed jutsu, items, elements or "
        "general types has its raw damage multiplied by dmgModifier. Only the highest-power matching weakness "
        "counts, and a dmgModifier of 0 counts as 1. No prevent stops it."),
    "increaserange": (
        "Adds power to the range of each listed basic action whose base range is above 0. Range-0 actions are "
        "unaffected. Several range effects don't add up: each action takes the largest bonus. It is live as soon "
        "as it is on the holder (no next-round wait), and bloodline sources are off under Seal. A buffprevent from "
        "an earlier round blocks it."),
    "increasecooldown": (
        "Raises the cooldown of each listed basic action by power. Per action only the lowest signed modifier "
        "applies: any decreasecooldown on the holder overrides it completely, and among several increases only "
        "the smallest counts. The result is never below the action's shared cooldown lock. Jutsu cooldowns are "
        "untouched. A debuffprevent from an earlier round blocks it."),
    "decreasecooldown": (
        "Lowers the cooldown of each listed basic action by power, never below the action's shared cooldown lock "
        "or 0. Per action only the lowest signed modifier applies, so the strongest decrease wins and every "
        "increasecooldown on that action is ignored rather than netted. Jutsu cooldowns are untouched. A "
        "buffprevent from an earlier round blocks it."),
    "redirection": (
        "Instant only (rounds 0). It pulls the target toward the caster, stopping next to them, or pushes it away, "
        "by power hexes along the line. The landing is clamped to the board. Only the landing tile is checked: if "
        "a player, the caster or a barrier (any ground object with HP) is there, the target steps back toward its "
        "start to the first open tile, or stays put. Players and barriers in between are crossed. A moveprevent "
        "from an earlier round blocks it."),
    "stealth": (
        "Rolls power% to land. While it's active, other fighters' non-ground effects can't land on the holder, "
        "though ground effects still can. The holder can't use any jutsu or the basic attack, meditate, heal, "
        "clear, cleanse, stances or flee. They keep move, replacement, End Turn and items. It's positive, so Clear "
        "removes it."),
    "stun": (
        "Stunprevent can block it (age-compared). Otherwise it rolls power% to land. From the round after it "
        "lands, the holder's available AP drops by apReduction, but never below 0. Only the strongest stun counts. "
        "That includes stun ground effects on the holder's tile that are from an earlier round and pass "
        "friendly-fire for them; that read makes no land roll."),
    "summon": (
        "Spawns the chosen AI on the target tile, or on the nearest empty tile if that one is taken, with aiHp HP "
        "and stats scaled to power% of the summoner's total. It acts as a separate fighter. It copies the "
        "summoner's initiative and is inserted into the turn order right after the summoner and anyone tied with "
        "them. It can be player-piloted and leaves when its rounds end. Summonprevent hides summon jutsu."),
    "elementalseal": (
        "Rolls power% to land. While active with rounds left (and not cast this round), the holder's jutsu with an "
        "authored AP cost of exactly 60 are hidden if they are elemental: elementClassification set and not None, "
        "any elementaldamage tag, or any tag with a non-None element. Items and basic actions are never hidden. "
        "The server enforces it. No prevent stops it."),
    "disarm": (
        "A prevent-type status. While active with rounds left (and not cast this round) it hides the holder's "
        "weapon items and every jutsu that needs a weapon. It is only an action gate; no handler checks it."),
}

# ---------------------------------------------------------------------------------------------------------
# interactions.json: kind definitions and link edits (B, C, D verification notes).
# Ops: ("del", from, to, kind) | ("put", from, to, kind, note) upsert | ("rekind", from, to, old, new, note)
# ---------------------------------------------------------------------------------------------------------
KIND_DEFS = {
    "prevents": ("source is a prevent-type status; once landed it blocks the target tag on the holder: only "
                 "effects cast in a later round where the handler passes the effect, any active one otherwise "
                 "(see the note and the tag's prevent_check)"),
    "hides": ("while active on the holder, the source removes actions that carry the target tag from the holder's "
              "action list (availableUserActions, server-enforced); effects already cast are untouched"),
}
KIND_ORDER = ["prevents", "hides", "removes", "transfers", "boosts", "weakens", "counters", "bypasses", "feeds",
              "disables", "shares", "overlaps"]

_UNLESS_DIFFUSE = "unless Diffuse deferred part of the hit (process.ts:1047-1053)"
EDGE_OPS = [
    # H3 / H4: shields, Final Stand, Diffuse
    ("put", "pierce", "shield", "bypasses",
     "not soaked; sets every enabled shield on the target to 0. When the target's Diffuse deferred part of it, "
     "the immediate part is soaked, and the shields are destroyed only if positive Reflect is still on the "
     "original Pierce consequence when mitigation runs; the attacker's own Diffuse deferring that Reflect moves "
     "it to a separate Reflect-typed consequence and clears it (process.ts:1004-1016, 1036-1040, 1054-1055; "
     "damagePipeline.ts:460-474)"),
    ("put", "diffuse", "damage", "counters",
     "defers power% (<=99%, strongest Diffuse only) of the reduced hit; none if the action's combined incoming "
     "damage >= current HP"),
    ("put", "diffuse", "pierce", "counters",
     "defers part of a non-lethal Pierce; the immediate part is soaked by shields instead of breaking them, "
     "unless positive Reflect is still on the original Pierce consequence when mitigation runs (cleared if the "
     "attacker's own Diffuse defers it) (process.ts:1036-1060, damagePipeline.ts:460-474)"),
    ("del", "diffuse", "absorb", "feeds"),
    ("put", "diffuse", "absorb", "weakens",
     "Absorb on a Diffuse holder resolves after deferral and converts only the immediate part; its 60% cap uses "
     "the immediate part (process.ts:632-657, 1289-1290)"),
    ("put", "diffuse", "lifesteal", "weakens", "lifesteal_hp scaled to the immediate part (damagePipeline.ts:481-483)"),
    ("put", "finalstand", "diffuse", "counters", "repayment ticks can't take the holder below 1 HP (diffuse.ts:117)"),
    ("put", "finalstand", "damage", "counters",
     "floors each packet at 1 HP, checked against HP before the action's damage; packets that together exceed HP "
     "still kill (process.ts:677-683, 1018)"),
    ("put", "finalstand", "pierce", "counters", "floors HP at 1 against Pierce as well (process.ts:1018)"),
    ("put", "afterburn", "finalstand", "bypasses", _UNLESS_DIFFUSE),
    ("put", "drain", "finalstand", "bypasses", _UNLESS_DIFFUSE),
    ("put", "poison", "finalstand", "bypasses", _UNLESS_DIFFUSE),
    ("put", "afterburn", "shield", "bypasses", _UNLESS_DIFFUSE),
    ("put", "drain", "shield", "bypasses", _UNLESS_DIFFUSE),
    ("put", "poison", "shield", "bypasses", _UNLESS_DIFFUSE),
    ("put", "wound", "shield", "bypasses",
     "only when it gets its own consequence; merged into another consequence from the same caster, or "
     "Diffuse-deferred, it is soaked (tags.ts:1821-1841)"),
    ("put", "shield", "damage", "counters", "soaks direct, residual and parry-return damage before HP"),
    ("put", "shield", "reflect", "counters",
     "quirk, likely a game bug: reflected damage is soaked by the reflector's own remaining shields, not the "
     "attacker's (process.ts:965-971, 1054-1055)"),
    ("put", "shield", "recoil", "counters",
     "quirk, likely a game bug: recoil is soaked by the shields of the player the recoil holder hit "
     "(process.ts:965-971, 1057-1058)"),
    # H5: prevent checks
    ("put", "clearprevent", "clear", "prevents",
     "any active clearprevent blocks, including a pending multi-round Clear cast earlier; ends it (tags.ts:1155)"),
    ("put", "cleanseprevent", "cleanse", "prevents",
     "any active cleanseprevent blocks, including a pending Cleanse cast earlier; ends it (tags.ts:1165)"),
    ("put", "sealprevent", "seal", "prevents",
     "any age; re-checked each holder turn, so a later non-bloodline Sealprevent ends an existing Seal (tags.ts:2402)"),
    ("put", "robprevent", "rob", "prevents",
     "any age; blocks the per-round attempts of an earlier Rob and ends it (tags.ts:2356)"),
    ("put", "onehitkillprevent", "onehitkill", "prevents",
     "any age; blocks later ticks of an earlier One Hit Kill (tags.ts:2317)"),
    ("put", "fleeprevent", "flee", "prevents",
     "any age; blocks the per-round rolls of an earlier Flee and ends it (tags.ts:1531)"),
    ("put", "moveprevent", "move", "prevents", "checks the move's caster, any age (tags.ts:2273); also hides move actions"),
    ("put", "moveprevent", "move", "hides",
     "hides basic move, the replacement technique and move-tag jutsu while rounds > 0 (actions.ts:169, 180, 246-251)"),
    ("put", "healprevent", "vamp", "prevents", "checks the Vamp caster's own healprevent, any age, no roll (tags.ts:1962)"),
    ("put", "healprevent", "curse", "prevents",
     "blocks only the expiry payout; any active healprevent at expiry; stored healing lost (tags.ts:1690)"),
    ("put", "buffprevent", "copy", "prevents", "checks the Copy caster's buffprevent (tags.ts:456)"),
    ("rekind", "summonprevent", "summon", "prevents", "hides",
     "hides jutsu with a summon tag while rounds > 0; no handler check; items not filtered (actions.ts:231-237)"),
    # M3: elemental seal is an action gate; Pierce's positive links
    ("rekind", "elementalseal", "elementaldamage", "prevents", "hides",
     "only jutsu with authored AP cost exactly 60; elementaldamage is one of three triggers (also non-None "
     "elementClassification or any non-None tag element); needs rounds > 0; items and basic actions unaffected "
     "(actions.ts:252-266)"),
    ("put", "pierce", "curse", "bypasses",
     "gets no Curse damage bonus (bonus applied in the damage pipeline, which Pierce skips)"),
    ("put", "pierce", "curse", "feeds",
     "HP lost to Pierce (instant or residual, after shields and Final Stand) is stored by a Curse on either fighter"),
    ("put", "pierce", "lifesteal", "feeds",
     "instant Pierce only; read as a normal direct hit, always passes the generals filter, shares the 60% leech cap"),
    ("put", "pierce", "absorb", "feeds", "instant Pierce only; the holder's Absorb converts it; generals filter ignored"),
    ("put", "pierce", "reflect", "feeds", "instant Pierce only; generals filter ignored"),
    ("put", "pierce", "wound", "feeds",
     "a Wound cast in the same action records instant Pierce damage from its caster to its target"),
    ("put", "pierce", "vamp", "feeds", "instant Pierce from the Vamp jutsu counts as outgoing damage"),
    ("put", "barrier", "pierce", "counters",
     "reduces instant Pierce by the barrier fraction on its path or tile, and Pierce damages the barrier; residual "
     "ticks are not reduced"),
    # M2: readers are not damage counters; heal modifiers are HP only
    ("del", "absorb", "damage", "counters"),
    ("put", "damage", "absorb", "feeds",
     "each direct hit the holder takes (from the round after Absorb lands) refills chosen pools by power%; HP part "
     "capped at 60% of the immediate hit and needs the holder alive; the hit is not reduced"),
    ("del", "reflect", "damage", "counters"),
    ("put", "damage", "reflect", "feeds",
     "each direct hit the holder takes returns power% as separate damage to the attacker, capped at 60% of the "
     "pre-Diffuse hit; the holder still takes the full hit"),
    ("del", "siphon", "damage", "counters"),
    ("put", "damage", "siphon", "feeds",
     "enemy-caused HP loss the holder takes (after shields and Final Stand; not recoil or self-damage) becomes "
     "shield credit granted after the action; the hit is not reduced"),
    ("put", "increaseheal", "heal", "boosts", "scales only the HP part of Heals the holder casts; CP/SP heals unchanged"),
    ("put", "decreaseheal", "heal", "weakens", "scales only the HP part of Heals the holder casts; CP/SP heals unchanged"),
    ("put", "increaseheal", "absorb", "boosts", "scales only Absorb's HP part; CP/SP parts unchanged"),
    ("put", "decreaseheal", "absorb", "weakens", "scales only Absorb's HP part; CP/SP parts unchanged"),
    # M5: selectors
    ("del", "increasecooldown", "decreasecooldown", "counters"),
    ("put", "decreasecooldown", "increasecooldown", "counters",
     "per basic action the lowest signed modifier wins, so any decrease overrides every increase (no additive "
     "cancel); the result floors at the shared cooldown lock (actions.ts:458-485)"),
    ("put", "barrier", "redirection", "counters",
     "only a barrier on the computed landing tile matters: the target steps back toward its start to the first "
     "open tile; barriers between start and landing are crossed (tags.ts:2610-2636)"),
    ("put", "barrier", "damage", "counters",
     "instant damage (rounds 0) cast through barriers on the path is cut by barrierAbsorb; residual ticks are not "
     "(tags.ts:1448-1452)"),
]
