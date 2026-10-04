# Bloodright batch rebalance — 2026-10-04

Roster-wide design pass under `BALANCE_REVIEW_METHOD.md` on every tree except the protected ones (Taiyo Kami, Ethereal Monarch, Blood-Enchanted Eyes, Shakunetsu Sakura, Arashima). Before values are the previous handoff `95204fc6bc1bef59f2da9aeb52f27df3f19523be`. Every rebalanced tree is a **Fable proposal**, not director-approved. Each tree's Markdown carries its full Damage-tier table, every legal fourth purchase and route-overlap notes; `REBALANCE_AUDIT.md` gives the roster view.

## Roster summary

- Trees changed: 39 — Aerathiel, Ancient Tailed Demon, Bakuhatsu, Blue Blade Eyes, Cosmic Ascendant, Crystal Essence, Dai Kenja, Eyes of the Forsaken King, Godstorm Eclipse, Ha Yanagi, Heavenly Sonata, Houkyuken, Hyouga Yui, Itojinsei, Kyuko-sei, Loup-Garou, Lycanthropy, Megumi Kijo, Musashi Ken, Namikaze, Nature's Blessing, Night Parade of A Thousand Demons, Oblivion Seal, Primal Radiance, Reptilian, Sands of Time, Sea-King's Blessing, Shadow Weaver, Shinrai Ou, Shinseina Ki, Shiroi Youso, Suragu, Teno Yuki, Tenohira Musei, Terra Nova, Tetsugan, Vaporia, Voltara Divine, Yaketsuku Netsu.
- Structurally rewired: 14 — Aerathiel, Ancient Tailed Demon, Bakuhatsu, Dai Kenja, Ha Yanagi, Kyuko-sei, Lycanthropy, Megumi Kijo, Musashi Ken, Night Parade of A Thousand Demons, Oblivion Seal, Primal Radiance, Shinseina Ki, Voltara Divine.
- Damage routes reduced: 41 — Aerathiel (+5 → +0), Ancient Tailed Demon (+5 → +2), Arashima (+5 → +2), Bakuhatsu (+5 → +0), Blood-Enchanted Eyes (+5 → +2), Blue Blade Eyes (+5 → +2), Cosmic Ascendant (+5 → +0), Crystal Essence (+5 → +0), Dai Kenja (+5 → +2), Eyes of the Forsaken King (+5 → +0), Godstorm Eclipse (+5 → +0), Ha Yanagi (+5 → +2), Heavenly Sonata (+5 → +2), Houkyuken (+5 → +0), Hyouga Yui (+5 → +3), Itojinsei (+5 → +3), Kyuko-sei (+5 → +0), Loup-Garou (+5 → +3), Lycanthropy (+5 → +0), Megumi Kijo (+5 → +2), Musashi Ken (+5 → +4), Namikaze (+5 → +2), Nature's Blessing (+5 → +3), Night Parade of A Thousand Demons (+5 → +2), Oblivion Seal (+5 → +0), Primal Radiance (+5 → +0), Sands of Time (+5 → +0), Sea-King's Blessing (+5 → +3), Shadow Weaver (+5 → +2), Shakunetsu Sakura (+5 → +2), Shinrai Ou (+5 → +0), Shinseina Ki (+5 → +0), Shiroi Youso (+5 → +2), Suragu (+5 → +2), Teno Yuki (+5 → +2), Tenohira Musei (+5 → +2), Terra Nova (+5 → +2), Tetsugan (+5 → +0), Vaporia (+5 → +2), Voltara Divine (+5 → +0), Yaketsuku Netsu (+5 → +2).
- +5 Damage retained: Ethereal Monarch (protected): ; Taiyo Kami (protected): .
- 50 → 55 results remaining: 2 — Ethereal Monarch: Tamashī no Sakeme 50 → 55; Taiyo Kami: Incandescent Nova 50 → 55.
- Results above the 50 Nuke tier (any size): 6 — Blood-Enchanted Eyes: Reaper's Embrace 50 → 52; Ethereal Monarch: Tamashī no Sakeme 50 → 52; Ethereal Monarch: Tamashī no Sakeme 50 → 55; Shakunetsu Sakura: Hiru-Sakura: Sakura-ame 50 → 52; Taiyo Kami: Incandescent Nova 50 → 52; Taiyo Kami: Incandescent Nova 50 → 55.
- 45 → 50 results remaining: 0 — none.
- Unusually high downstream leverage: Aerathiel: Increase Damage Given: Atomic Shield's two rows compound on every caster hit (Dust, highest-offence-stat and element-less) for two rounds from one 40 AP cast, so +p on both is roughly +2p on a single row. Increase Damage Taken: the Windshear Decay and Death's March exposure rows compound on a target under both and raise every attacker's hits, allies' and weapons' included.; Ancient Tailed Demon: Afterburn and Increase Damage Taken on Demonic Embrace: one application changes every instant non-pierce hit the marked target takes from anyone, allies included, for 2 rounds (IDT also reaches residual ticks). Increase Damage Given on Demonic Vitae: 3 rounds on every hit the caster lands on every target, including Roar's whole circle.; Bakuhatsu: Increase Damage Given: two 35% self buffs (Charge 4 Explosion, Howitzer Crash) compound when both are live and multiply every matching caster hit, including area attacks on several targets, weapons and off-kit jutsu. Because of this the route is held at +8%: the window goes from x1.82 to x2.04. Afterburn and Increase Damage Taken: one Charge 4 Explosion application raises every hit the party lands on the marked target for two rounds.; Blue Blade Eyes: Increase Damage Given (four self rows on four jutsu that compound with each other and with the 28.75% IDG passive) and Increase Damage Taken (three enemy rows, and every attacker on the target benefits, allies included). Three rows up at once give x1.40^3 ≈ x2.74 against x2.46 at base, so both are held to +5%. Lifesteal on Arctic Frost leeches from every hit in its two-round window, pierce included.; Cosmic Ascendant: Decrease Damage Taken: three compounding self rows at a 30-35% base, so each point is worth about twice a point of Increase Damage Taken; this is the leverage the review found and the reason the Fortress was cut to +7%. Afterburn on Cosmic Intent: one application drives every non-pierce hit on the mark, from anyone. Lifesteal on Intent includes pierce and is not counted in the trade diagnostic.; Crystal Essence: Increase Damage Taken: two 2-round marks (Sphere single target, Cave area). They amplify every attacker's matching hits, allies' included, and compound on a doubly marked enemy (×1.82 base -> ×2.04 at +8%). Increase Damage Given: one Shippū self row that multiplies every matching caster hit for two rounds and compounds with the 28.75% bloodline passive (×1.45 × 1.29 ≈ ×1.87). Reflect: includes pierce, bypasses shields, 60% per-hit cap.; Dai Kenja: Increase Damage Given: Overloaded Impact's self buff multiplies every Ninjutsu or non-elemental hit the caster lands in the 2 rounds after the cast. Decrease Damage Given: Chakra Cannon is an AOE circle (ally hazard) and compounds with Chakra Overload on one target. Increase Damage Taken: Chakra Overload's exposure raises every attacker's Ninjutsu or non-elemental hits on the target, and the same tag raises the caster's own adverse self row.; Eyes of the Forsaken King: Increase Damage Taken: three native 35% rows (two from one 40 AP Chrono Stasis cast) compound on every attacker's non-pierce hits, x1.35^3 ≈ x2.46. The tree deliberately holds it at the Foundation's +2% (x1.37^3 ≈ x2.57). Afterburn: one Imperial Swords row adds to every later non-pierce hit on the target from any attacker. illuminance's Increase Damage Given: one row multiplies every caster hit on every target, including off-kit Fire/Lightning/Wind and element-less hits.; Godstorm Eclipse: Increase Damage Given has the most leverage. Three Godstorm Aegis self buffs (Wall, Tempest, Bulwark) compound on each of the caster's hits: ×2.46 at 35%, ×2.74 at 40% and ×2.86 at 42%. Increase Damage Taken comes next. Its two Aegis exposure rows (Wall, Heart) also multiply allies' hits: ×1.82 at base, ×2.04 at 43%. Afterburn (one Tempest row that feeds every later non-pierce hit) has the same downstream reach but is deliberately left unamplified.; Ha Yanagi: Decrease Damage Given: two compounding enemy rows (Wailing Bark, Petal Nightmare) cut every non-pierce hit the target lands to x0.55 x 0.60 = x0.33 at +10%. Increase Damage Taken: the one Blighted Tree mark multiplies every attacker's non-pierce hits, allies included. Increase Damage Given: the one Wailing Bark self window multiplies every non-pierce hit the caster lands, weapons and basic attacks included.; Heavenly Sonata: Increase Damage Taken (Foreboding Interlude: one debuff multiplies every attacker's Genjutsu or element-less non-pierce hit on the target, allies' hits included). Decrease Damage Given (Harmonic Chamber: cuts every non-pierce hit the target deals, against anyone). Flat Damage is multiplied by both offensive windows and then by the 25% Yin-Yang bloodline passive, which applies last.; Houkyuken: Increase Damage Taken: two separate enemy debuffs (Morning Star, which matches any stat type, and Magnetic Assignment) compound on one target. Every non-pierce hit that target takes from the player, allies and weapons is raised for 2 rounds. Reflect: one self row answers every attacker's hit, pierce included, for 2 rounds, so its value grows with the number of attackers.; Hyouga Yui: IDT: Spear's element-less exposure raises every non-pierce hit, from any attacker including allies, on every enemy in its circle for two rounds. With Cocytus a target can carry ×1.45 × 1.45 ≈ ×2.10. IDG: Avalanche's and Glacier's Will's self buffs compound on every own hit in the window (Glacier's Will's row reaches weapons and normal jutsu). DDT: the Cocytus and Glacier's Will guards apply in sequence, ×0.55 × 0.60 = ×0.33, and the ground guard also covers allies on the tiles.; Itojinsei: Increase Damage Taken: one Lightning Threads row multiplies every matching non-pierce hit on the target from every attacker for two rounds. Decrease Damage Given: two area rows reduce in sequence on every non-pierce hit from each enemy caught (x0.455 -> x0.33 at +10%), protecting the whole party. The self IDG pair also compounds and reaches off-kit element-less hits.; Kyuko-sei: Increase Damage Taken has the most downstream leverage. One Temporal Erosion or Abysmal End cast multiplies every matching later hit on the target for 2 rounds, from the caster, allies and weapons. The two rows compound on one target (x1.82 at base, x2.04 at +8). Abysmal End applies it in an area, allies included. Increase Damage Given's two self buffs compound the same way on the caster's own hits. Both are therefore held at +8% rather than +10%.; Loup-Garou: IDG (Nature's Hunter's 2-round self buff multiplies every element-less or Taijutsu non-pierce hit the caster lands on any target) and IDT (Life reaver's 2-round exposure multiplies every qualifying hit on one target, allies' hits and the strike included). The two compound, and both casts together cost exactly 100 AP.; Lycanthropy: Increase Damage Given. The kit has two 35% self rows (Frenzy Assault, Feral Wrath). Each one multiplies every element-less hit the caster lands for the two rounds after its cast: basic attacks, weapons, normal jutsu and Moonlit Fury. The two rows also compound with each other when both are up. That is why this route is held at +8% (x1.43 x 1.43 ≈ x2.04 against x1.82 at base) rather than the +10% guardrail (x2.10).; Megumi Kijo: None unusual. Two tags reach beyond their single rows. Decrease Damage Given on Phantom Realm Oblivion: one application cuts every non-pierce hit the target deals, to anyone, for 2 rounds. Increase Heal on the Kijo's Benevolence field: it reaches allies and every heal, lifesteal, vamp and absorb in the window. Both stop at +10%, and no fourth purchase can stack either one.; Musashi Ken: increasedamagegiven: three 35% self rows (one per jutsu) that compound on every element-less hit for the 2 rounds after each cast. The Bukijutsu filter is not binding, so +1% reaches filler, weapons and both strikes. Held to +5% on the Tempo route and +3% everywhere else.; Namikaze: Two tags. Afterburn: Tempest Shroud's single row adds a percentage to every later non-pierce hit the target takes from anyone (allies and weapons included) for 2 rounds, up to the 60% per-hit cap. It also lands on allies inside the circle. Increase Damage Given: two self-buff rows (Cutting Tempest is Wind-only; the hidden Soaring Fujin matches nearly every hit) multiply each other and the bloodline's Wind passive. At +6% that is x1.41 x 1.2725 ≈ x1.79, against x1.64 unmodified.; Nature's Blessing: increasedamagetaken: Nature's Fury's single exposure row (up to 45%) multiplies every non-pierce hit the marked target takes for the 2 rounds after the cast, allies' hits included; Night Parade of A Thousand Demons: Increase Damage Taken on Herald of the Black Night. Its exposure amplifies every non-pierce hit from any source on each marked enemy, and one cast can mark several enemies, so it stops at +5% (35 -> 40%) as Burst setup. Otherworldly Conduit concentrates Increase Damage Given, Decrease Damage Taken and Lifesteal on one 40 AP cast.; Oblivion Seal: Increase Damage Taken: Shadowrend's element-less exposure amplifies every non-pierce hit the target takes in its 2-round window from any source, allies included, and two owners stack x1.43 x 1.43 ~ x2.04. Lifesteal: one Shadow Surge row heals off every hit the caster lands for 2 rounds, including Shadowrend's 58 pierce.; Primal Radiance: Afterburn: one 40 AP Primal Incineration cast adds its percentage to every non-pierce hit the target takes from anyone for 2 rounds. Increase Damage Taken on the same cast raises the hits that Afterburn then reads, so the setup enlarges its own payoff; this is why exposure is held at the Foundation's +2%. Beast's self Increase Damage Given affects every target in its window, not one.; Reptilian: Increase Damage Given. Its two rows (Reptile Chimera self, Cool-Blooded Empowerment circle) compound on a caster carrying both buffs: x1.42 x 1.42 is about x2.02 on the Jaws route, against x1.82 unenhanced. Empowerment's IDG and Lifesteal also reach every same-village ally in the radius-1 circle. Lifesteal leeches from every hit the recipients land, pierce included, and shares the 60% budget with the 10% Ninjutsu passive.; Sands of Time: Increase Damage Taken: two enemy rows (Timeshift broad, Momentum Shift Earth/None/Sand/Wind) compound on one hit and amplify every ally's non-pierce hits on the target for 2 rounds. Decrease Damage Given: the Timelapse circle hits several enemies at once and protects allies.; Sea-King's Blessing: Increase Damage Taken. One cast of Crushing Abyss's row (radius-1 circle, all four stat types, no element) amplifies effectively every hit any ally lands on each marked enemy for two rounds. With Water Dome's Water-only row, the two compound on Water hits: x1.40 x 1.45 = about x2.03 at +10%, against x1.755 at base.; Shadow Weaver: Increase Damage Given. Its three 35% self buffs (Domain, Step, Shell) compound when their windows overlap: x1.35^3 ≈ x2.46 at base, x1.41^3 ≈ x2.80 on the Burst route and x1.42^3 ≈ x2.86 at the +7% maximum. Each +1% lifts three multipliers. The Domain and Step rows also raise Fire, Lightning and element-less hits (basic attacks included). Shell's row is element-less (its Bukijutsu filter is not binding). Secondary: Severance's DDG and Shell's DDT each cover every non-pierce hit in their 2-round window (one application, many hits), but each is a single row on a cooldown-7 cast.; Shinrai Ou: Increase Damage Given: three 35% rows, two of them on one 40 AP Storm Cloak cast, compound on every hit the caster lands in their two-round windows, including normal jutsu and weapons, so each point counts two or three times on one hit (x2.46 -> x2.86 at +7%). Increase Damage Taken: Hammer's ground exposure covers a spiral around the caster and multiplies every matching hit by anyone, allies included.; Shinseina Ki: Increase Damage Given: Forest Wisdom's two rows are both live in the same 2-round window and compound, so every +1% printed counts twice. They also lift basic attacks, weapons and any element-less or Wood/Earth/Water hit. Increase Damage Taken: Grove's single row multiplies every attacker's hits, allies included, on every enemy in the circle.; Shiroi Youso: Increase Damage Given and Increase Damage Taken are the high-leverage tags. Each has two five-element rows that compound (×1.35² ≈ ×1.82 unmodified), and every five-element hit in the 2-round window is multiplied, including the five injected children. If they are in scope, Voltari's own self Increase Damage Given row and Rising Water Slicer's exposure row can add a third compounding row. Afterburn also has high leverage: one application reads every non-pierce hit on the target, including the children cast into Lightning Release's 2-round stun. It is limited by the 60% per-hit cap, which the two native burns already pass together.; Suragu: Afterburn: one application on Eruption Strike raises every non-pierce hit the target takes from any source, allies included, for two rounds, and it takes its share of the hit after the multipliers. Increase Damage Taken: Blow of Devastation multiplies every non-pierce hit on the target from anyone. Increase Damage Given: Lava Wave's self buff covers every caster hit of Lava, Earth, Fire or None element for two rounds. All three compound with each other.; Teno Yuki: Increase Damage Taken on Ice Palace: one 60 AP area cast exposes everyone in the circle for 2 rounds and multiplies every matching hit from the caster and allies (Ice/Water/Wind/element-less, not pierce). It compounds with Frostbound's IDG and the IDG passive, and two Palaces compound to about x2.10. Flat Damage is high-leverage per point because every % layer and the passive multiply it, and Imperial Freeze's stun gives free follow-up rounds.; Tenohira Musei: Increase Damage Taken. Moonlit Inferno's row lists all four stat types and no element, so one 40 AP cast multiplies every non-pierce hit on the target, allies' hits included. Moonlit plus Cascade (100 AP) put both IDT rows live for two rounds from one turn. More broadly, the kit's four stage-2 multiplier rows (2 IDG, 2 IDT) compound on one hit: ×1.35^4 ≈ ×3.32 before potency.; Terra Nova: Decrease Damage Given: Earthen Fortitude's debuff also cuts the struck enemy's damage to the caster's allies, so in team battles Pressure of Ages is worth more than its one row suggests. It is single-target, on cooldown 7.; Tetsugan: Two kinds. First, Increase Damage Given and Decrease Damage Taken, because three stance rows compound on two 40 AP casts. At +8%, Increase Damage Given gives ×1.19 with both stances up; Decrease Damage Taken gives ×0.77 with both stances up and ×0.68 with all three rows. Second, Afterburn: one application row (Crimson Thrust) drives every later non-pierce hit on the target, allied hits included.; Vaporia: Afterburn and Increase Damage Given, both on the one Liquid Ember Shell cast. One Afterburn application scales every matching non-pierce hit on the branded target for 2 rounds, allies' hits included. The Shell's IDG multiplies every matching hit the caster lands, and so also feeds Afterburn and Lifesteal. The tree holds IDG at +2% and gives Afterburn one route of +10%. Drowning Strike's area IDT also has high leverage (it multiplies allies' matching hits) and is an ally hazard.; Voltara Divine: increasedamagegiven: Whispers' element-less 35% self row, which lists all four stat types, amplifies every non-pierce hit the caster lands for 2 rounds (weapons, basic attacks, normal and off-kit jutsu). Bind's Lightning row amplifies every Lightning hit. Bind and Whispers are both 60 AP casts, so they cannot share a 100 AP turn, and their windows overlap only in one round, when both strikes are on cooldown.; Yaketsuku Netsu: Increase Damage Taken on Forbidden Chakra Fury: one cast exposes the target for 2 rounds to every non-pierce hit from any attacker, allies included, and two casters' exposures stack. Increase Damage Given on Forgotten Ember Blade is similar but caster-only: its Bukijutsu filter is not binding on an element-less row, so it lifts every element-less non-pierce hit the caster lands in its 2-round window. On a hit landed in both windows the two compound (×(1+p) each)..
- Director review recommended: Ancient Tailed Demon, Bakuhatsu, Blood-Enchanted Eyes, Dai Kenja, Ethereal Monarch, Godstorm Eclipse, Ha Yanagi, Primal Radiance, Shakunetsu Sakura, Shinseina Ki, Shiroi Youso, Taiyo Kami, Tetsugan, Voltara Divine.

## Trees

### Aerathiel

*Fable proposal (2026-10-04 batch rebalance); not director-approved*

Foundations: **Scouring Veil** — How do I turn my Atomic Shield into the weapon: strike harder, or strike back?; **Entropic Grasp** — How do I make the enemy decay: open them to every blow, or too weak to land their own?.
Advanced routes: **Total Disintegration** — burst: the Atomic Shield window as a kill window (self amplification); **Atomic Reprisal** — retaliation; **Terminal Decay** — exposure: team-wide pressure on a marked target; **Requiem of Dust** — suppression.
Changes: 01 Entropic Grasp: +2% IDG, +2% IDT → +2% IDT, +2% DDG; 02 Particle Collapse: moved Hidden Art under 01 → Hidden Art under 06; +2 Damage → +2% IDG; 03 Total Disintegration: +3 Damage → +3% IDG; 05 Terminal Decay: +5% IDT, +3% IDG → +3% IDT; 06 Scouring Veil: +2% REF, +2% DDG → +2% IDG, +2% REF; 08 Atomic Reprisal: +5% REF, +3% IDG → +5% REF; 09 Withering Gale: moved Hidden Art under 06 → Hidden Art under 01; 10 Requiem of Dust: +5% DDG, +2% IDT → +5% DDG.
Damage: no flat Damage.
Strongest fourth purchase: Total Disintegration + Entropic Grasp (+7% IDG, +2% DDG, +2% IDT, +2% REF); Terminal Decay + Scouring Veil (+2% IDG, +2% DDG, +8% IDT, +2% REF); Atomic Reprisal + Entropic Grasp (+2% IDG, +2% DDG, +2% IDT, +10% REF); Requiem of Dust + Scouring Veil (+2% IDG, +10% DDG, +2% IDT, +2% REF).
Concerns: No flat Damage route on a damage-led kit: Particle Cannon is 50 EP, so any Damage bonus passes the Nuke tier. If the director prefers the Blood-Enchanted Eyes pattern (percentage setup into +2 Damage, Particle Cannon 50 → 52), Total Disintegration is where it would go. Burst (+7% on two compounding rows from one cast) and Exposure (+8% on two compounding rows from two casts) are set by multiplier, not printed total; rotation and uptime were not simulated. Suppression and half of Exposure depend on Windshear Decay being classified Dust by authored jutsu classification (G1).
Director review: none.

### Ancient Tailed Demon

*Fable proposal (2026-10-04 batch rebalance); not director-approved*

Foundations: **Demon's Grasp** — How do I make the one enemy I have marked take more from every hit, mine and my allies'?; **Demon's Marrow** — How do I strengthen the host: hit everything harder or refuse to fall?.
Advanced routes: **Consuming Malice** — marked prey: one target takes more from every instant hit, allies' included; **Unyielding Husk** — fortress; **Primordial Rampage** — field rampage: every own hit on any target harder, Roar's whole circle heaviest.
Changes: 02 Rending Bellow: removed; 03 Howl of Annihilation: removed; 08 Unyielding Husk: +5% DDT, +2% IDG → +5% DDT; 10 Primordial Rampage: +5% IDG, +2% DDT → +3% IDG, +2 Damage.
Damage: Ancient Demon Roar 45 → 47.
Strongest fourth purchase: Consuming Malice + Demon's Marrow (+2% IDG, +5% IDT, +2% DDT, +10% AB); Unyielding Husk + Demon's Grasp (+2% IDG, +2% IDT, +10% DDT, +2% AB); Primordial Rampage + Demon's Grasp (+2 Damage, +8% IDG, +2% IDT, +2% DDT, +2% AB).
Concerns: Demon's Marrow is in every legal build, so the Consuming Malice build's fourth purchase is fixed and every build carries Vitae 37% / 27%. Consuming Malice and Primordial Rampage are close in 1v1 by arithmetic (Malice ≈ +3.6% on the caster's non-Roar hits in Embrace's window, Rampage ≈ +4.4% in Vitae's third round, Roar on the marked target about even); not simulated. Classification extension ('Ancient Tailed Demon' jutsu classification) remains a director/engine decision.
Director review: Structural: the tree drops from four Advanced Arts to three (narrow-kit exception) because Afterburn and Increase Damage Taken on Demonic Embrace are one marked-prey lever; Flayed Quarry and Howl of Annihilation are removed and Demon's Marrow becomes universal..

### Arashima (protected)

*Director-approved (RUL-2026-10-04-003); protected from the 2026-10-04 batch*

Foundations: **Tempest Hymn** — How do I win the storm offensively?; **Stillness in the Squall** — How do I outlast the storm?.
Advanced routes: **Sundered Sky** — burst; **The Storm's Due** — sustain offense; **Unbroken Horizon** — fortress; **Silence After Thunder** — suppression.
Damage: Reapers Storm 45 → 47; Demons Strike 45 → 47.
Strongest fourth purchase: Sundered Sky + Stillness in the Squall (+2 Damage, +8% IDG, +2% DDG, +2% DDT); The Storm's Due + Stillness in the Squall (+8% IDG, +2% DDG, +2% DDT, +5% LS); Unbroken Horizon + Deadwind Dirge (+5% DDG, +10% DDT, +2% LS); Silence After Thunder + Stormwarden's Hide (+10% DDG, +7% DDT).
Director review: none.

### Bakuhatsu

*Fable proposal (2026-10-04 batch rebalance); not director-approved*

Foundations: **Primed Fuse** — How do I make the detonation land harder: charge myself or mark the target?; **Eye of the Blast** — How do I survive at the centre of my own blasts?.
Advanced routes: **Critical Mass** — area burst: both self buffs charged, every blast in the window lands harder on all it hits; **Chain Reaction** — mark: exposure and Afterburn on one target, paid out by every hit from the party; **Siege Battery** — fortress that keeps firing.
Changes: 02 Shaped Charge: removed; 03 Ground Zero: removed; 04 Powder Keg: +3% IDG → +2% IDG; 05 Eye of the Blast: renamed Smoke and Shrapnel → Eye of the Blast; +2% DDT, +2% AB → +2% DDT; 08 Slow Burn: moved Hidden Art under 05 → Hidden Art under 01; +3% AB → +5% AB; 10 Critical Mass: +5% IDG → +4% IDG.
Damage: no flat Damage.
Strongest fourth purchase: Siege Battery + Primed Fuse (the only legal fourth) (+4% IDG, +2% IDT, +10% DDT); Chain Reaction + Powder Keg (self buffs 39%); the alternative is Eye of the Blast (DDT +2%) (+4% IDG, +5% IDT, +10% AB); Critical Mass + Slow Burn (Afterburn 40%); the alternative is Eye of the Blast (DDT +2%) (+8% IDG, +2% IDT, +5% AB).
Concerns: Critical Mass is held at +8% Increase Damage Given because the two self buffs compound; it remains the strongest solo route against targets other than the mark. Primed Fuse is universal, so the fortress's fourth purchase is forced; the kit has no second defensive tag for a leaf under Eye of the Blast. Every amplified row except the exposure depends on the proposed jutsu-classification resolver.
Director review: Structural: flat Damage is removed rather than re-cut (any flat Damage lifts Kinetic Nova past 50), leaving three Advanced Arts with Primed Fuse in every build. Confirm the narrow-kit exception, or choose the Blood-Enchanted Eyes pattern as a fourth route (Shaped Charge +3% Increase Damage Taken → Ground Zero +2 Damage, Kinetic Nova 50 → 52)..

### Blood-Enchanted Eyes (protected)

*Director-reviewed (RUL-2026-10-04-001); protected from the 2026-10-04 batch*

Foundations: **Scarlet Gaze** — How do I win offensively: amplify myself or expose them?; **Iron in the Blood** — How do I win defensively: protect myself or suppress them?.
Advanced routes: **Rite of Exsanguination** — burst: exposure set up, controlled raw-Damage payoff; **Feast of the Fallen** — sustain offense; **Deathless Vitality** — fortress; **Red Pestilence** — suppression.
Damage: Ring of Spilled Blood 40 → 42; Crimson Tithe 40 → 42; Reaper's Embrace 50 → 52; Crimson Impact 40 → 42.
Strongest fourth purchase: Rite of Exsanguination + Iron in the Blood (+2 Damage, +2% IDG, +2% DDG, +5% IDT, +2% DDT); Red Pestilence + Scarlet Gaze (+2% IDG, +10% DDG, +2% IDT, +5% DDT); Deathless Vitality + Scarlet Gaze (+2% IDG, +5% DDG, +2% IDT, +10% DDT); Feast of the Fallen + Opened Veins (+7% IDG, +5% IDT, +5% LS).
Director review: Reaper's Embrace 50 → 52 under Rite of Exsanguination (above the Nuke tier) is recorded for confirmation..

### Blue Blade Eyes

*Fable proposal (2026-10-04 batch rebalance); not director-approved*

Foundations: **Sapphire Edge** — How do I win the trade of blows: sharpen mine or dull theirs?; **Unblinking Sapphire** — How do I outlast them: refuse their blows, or drink them dry?.
Advanced routes: **Stroke That Splits Stone** — burst: amplification set up, controlled raw-Damage payoff; **Numb to the Marrow** — suppression (guard rider); **Glacier Does Not Yield** — fortress; **Winter Takes Its Due** — sustain offense: drain with exposure.
Changes: 02 Honed Crescent: +2 Damage → +3% IDG; 03 Stroke That Splits Stone: +3 Damage → +2 Damage; 05 Numb to the Marrow: +5% DDG, +3% IDG → +5% DDG, +2% DDT; 08 Glacier Does Not Yield: +5% DDT, +3% IDT → +5% DDT; 10 Winter Takes Its Due: +3% LS, +5% IDT → +3% LS, +3% IDT.
Damage: Icebound Might 40 → 42; Glacial Volley 40 → 42; Ice Shackles 45 → 47; Blade Resonance 45 → 47; Blue Crimson 40 → 42.
Strongest fourth purchase: Stroke That Splits Stone + Unblinking Sapphire (+2 Damage, +5% IDG, +2% DDG, +2% IDT, +2% DDT); Numb to the Marrow + Honed Crescent (+5% IDG, +10% DDG, +2% DDT); Glacier Does Not Yield + Sapphire Edge (+2% IDG, +2% DDG, +2% IDT, +10% DDT); Winter Takes Its Due + Sapphire Edge (+2% IDG, +2% DDG, +5% IDT, +2% DDT, +5% LS).
Concerns: Suppression and Drain primaries each reach one row on one weapon (Icebound Might on The Threefold Gaze; Arctic Frost on The Blue Blade), so a single-weapon owner can play only one of them; their +10% / +5% values follow the director-approved single-row precedents. Nine of 16 rows, including every Decrease Damage Given, Decrease Damage Taken and Lifesteal row, need the jutsu-classification resolver (G1); with the current element-matching resolver only the five Damage rows, Arctic Frost's damage buff and Blade Resonance's exposure would be reachable. Burst and Drain both reach ×1.40 on three compounding rows (self buffs versus exposure); Burst adds +2 Damage, Drain adds Lifesteal. Exposure also helps allies' hits, which the row arithmetic does not measure. Off-kit Ice jutsu receive Stroke That Splits Stone's +2 Damage; any off-kit 50 EP Ice strike would read 52 (the off-kit catalog is unverified).
Director review: none.

### Cosmic Ascendant

*Fable proposal (2026-10-04 batch rebalance); not director-approved*

Foundations: **Celestial Alignment** — How do I make the enemy I mark fall faster?; **Gravity Well** — How do I outlast the exchange: harden myself, or drain and blunt them?.
Advanced routes: **Supernova Unbound** — burst: charge yourself, open both marks, detonate into the window; **Light of Dead Stars** — pressure: one Intent cast makes every hit on the mark burn, party-wide; **Heart of the Singularity** — fortress: all three guard casts; **Hunger of the Void** — drain and suppression: leech from your hits while Aura blunts theirs.
Changes: 02 Collapsing Star: +2 Damage → +3% IDG; 03 Supernova Unbound: +3 Damage, +3% IDT → +3% IDT, +3% IDG; 05 Light of Dead Stars: +7% AB, +3% IDT → +7% AB; 07 Event Horizon: +3% DDT → +2% DDT; 08 Heart of the Singularity: +5% DDT, +3% IDG → +3% DDT.
Damage: no flat Damage.
Strongest fourth purchase: Supernova Unbound + Gravity Well (Searing Starlight is the all-offence alternative) (+8% IDG, +5% IDT, +2% DDT, +2% DDG: Intent/Chains IDT 40%, Energy IDG 43%, DDT 37/37/32%, Aura DDG 32%); Light of Dead Stars + Gravity Well by diagnostic; Collapsing Star is the offensive fourth (+2% IDG, +2% IDT, +10% Afterburn, +2% DDT, +2% DDG: Intent Afterburn 45%, IDT 37%, Energy IDG 37%, DDT 37/37/32%); Heart of the Singularity + Celestial Alignment (+7% DDT, +2% DDG, +2% IDT, +2% IDG: DDT 42/42/37% (x0.89 / x0.90 per cast alone, about x0.21 all three, x0.72 against base), Aura DDG 32%, IDT/IDG 37%); Hunger of the Void + Event Horizon. The audit's row-weighted measure ties it with Celestial Alignment at 24; the trade diagnostic favours Event Horizon. (+5% Lifesteal, +7% DDG, +4% DDT: Intent Lifesteal 45%, Aura DDG 37% (target deals x0.90, party-wide), DDT 39/39/34%).
Concerns: No flat Damage on a Burst-trait kit: Cosmic Explosion (50 EP) is the only Damage row, so any Damage bonus would pass the Nuke tier; Burst is built from multipliers instead. For reference only, the Blood-Enchanted Eyes pattern (+2 Damage) would give Explosion 50 → 52 and need an above_nuke_rationale; it is not proposed. The Fortress still leads the mitigation diagnostic (1.50 / 1.11 against 1.34 / 1.08 for Hunger + Event Horizon); that is its identity, and Hunger's Lifesteal is not counted. Not simulated. Gravity Well (+2% Decrease Damage Taken on three rows) is the strongest fourth for both offensive capstones (Supernova + Gravity Well 1.29 against 1.16 with Searing Starlight); it is a defensive hedge that adds no offense, not a stacked payoff. Burst beats the burn on the caster's own hits only with both marks live; with Intent's mark and Energy's buff but no Chains, the burn is ahead (×1.11 against ×1.10). The 'Cosmic Ascendant' classification extension remains a director/engine decision; off-kit coverage is unverified.
Director review: none.

### Crystal Essence

*Fable proposal (2026-10-04 batch rebalance); not director-approved*

Foundations: **Prismatic Focus** — How do I make my Crystal strikes count: sharpen myself or crack them open?; **Jade Lattice** — How do I hold my ground: endure the blows or turn them back?.
Advanced routes: **Splintered Mountain Heart** — burst window: self amplification (Shippū window into Prism); **Break Along the Flaw** — exposure: team-wide marks that compound on one target; **Adamant Core** — fortress; **Entombed in Crystal** — retaliation.
Changes: 02 Razor Lattice: +2 Damage → +3% IDG; 03 Splintered Mountain Heart: +3 Damage → +5% IDG; 05 Break Along the Flaw: +5% IDT, +3% IDG → +3% IDT; 08 Adamant Core: +5% DDT, +3% IDG → +5% DDT; 10 Entombed in Crystal: +5% REF, +3% IDG → +5% REF.
Damage: no flat Damage.
Strongest fourth purchase: Splintered Mountain Heart + Flaw in the Stone (+10% IDG, +5% IDT); Break Along the Flaw + Jade Lattice (+2% IDG, +8% IDT, +2% DDT, +2% REF); Adamant Core + Prismatic Focus (+2% IDG, +2% IDT, +10% DDT, +2% REF); Entombed in Crystal + Prismatic Focus (+2% IDG, +2% IDT, +2% DDT, +10% REF).
Concerns: No flat Damage on a kit whose attacks are 50/40/40 EP: Prism is 50, so any Damage bonus passes the Nuke tier. If the director prefers the Blood-Enchanted Eyes pattern (exposure setup into +2 Damage, Prism 50 → 52, Shippū and Cave 40 → 42), Break Along the Flaw is where it would go. Burst window (+10% on one self row from one cast) and Exposure (+8% on two compounding, team-wide rows from two casts) are set by multiplier and uptime, not printed total; rotation was not simulated. Fortress, Retaliation and half of Exposure depend on Crystal Sphere's authored classification or the element-less Cave Reflect row reaching the proposed resolver (G1).
Director review: none.

### Dai Kenja

*Fable proposal (2026-10-04 batch rebalance); not director-approved*

Foundations: **Brimming Cup** — How do I make the window after Overloaded Impact hit harder?; **Sage's Rebuke** — How do I break the enemy: blunt their blows, or crack them open for my strike?.
Advanced routes: **Boundless Reservoir** — sustained amplification: the caster's own hits in the two rounds after the strike; **Edict of Silence** — suppression: both control casts, compounding on one target; **Shattered Vessel** — exposure into a controlled strike: Chakra Overload cracks the target, Overloaded Impact lands into it.
Changes: 02 Chakra Surcharge: removed; 03 Breaking Point: removed; 09 Cracked Vessel: +2% IDT → +3% IDT; 10 Shattered Vessel: +3% IDT, +3% DDG → +2 Damage, +2% IDT.
Damage: Overloaded Impact 40 → 42.
Strongest fourth purchase: Boundless Reservoir + Sage's Rebuke (+10% IDG, +2% DDG); Edict of Silence + Cracked Vessel (+10% DDG, +3% IDT); Shattered Vessel + Smothered Current (+2 Damage, +5% DDG, +5% IDT).
Concerns: Shattered Vessel against Boundless Reservoir one-on-one (like-for-like 4-BP builds): damage dealt is about even with one strike-sized window hit per round and Boundless Reservoir leads from the third window hit, while Shattered Vessel's caster takes ×1.04 in the two rounds after the strike; allies hitting the marked target favour Shattered Vessel. Arithmetic only, not simulated. The exposure half of Shattered Vessel is slightly net-negative one-on-one (target ×1.037, caster ×1.04); its solo value is the +2 Damage strike. Sage's Rebuke is in every legal 4-BP build, so Boundless Reservoir's fourth purchase is fixed at +2% Decrease Damage Given.
Director review: Structural: four Advanced Arts become three (narrow-kit exception); the Burst route (Chakra Surcharge → Breaking Point) and the Exposure capstone merge into one exposure → strike route (Cracked Vessel +3% → Shattered Vessel +2 Damage, +2% Increase Damage Taken). The adverse Overloaded Impact self row (25 → 30%) is proposed under OPEN_DECISIONS D11, still open, at its drafted +5% size..

### Ethereal Monarch (protected)

*Director-corrected (2026-10-03); protected from the 2026-10-04 batch*

Damage: Tamashī no Sakeme 50 → 52 / 55; Celestial Sealing 40 → 42 / 45.
Strongest fourth purchase: Ethereal Coronation + Veil of the Monarch (+5 Damage, +2% IDG, +2% IDT, +2% DDT, +2% REF); Rain of Fallen Stars + Veil of the Monarch (+5% IDG, +5% IDT, +2% DDT, +10% AB, +2% REF); Immovable Throne + Sovereign's Decree (+5% IDG, +2% IDT, +10% DDT, +2% REF); Monarch's Retribution + Sovereign's Decree (+2% IDG, +5% IDT, +4% DDT, +10% REF).
Director review: Tamashī no Sakeme 50 → 55 under the Burst route is flagged under BALANCE_REVIEW_METHOD.md; not retuned..

### Eyes of the Forsaken King

*Fable proposal (2026-10-04 batch rebalance); not director-approved*

Foundations: **Gaze of the Deposed** — How do I win offensively: amplify my own strikes, or brand the target so every hit on it burns?; **Mantle of Exile** — How do I win defensively: outlast the blow, or return it?.
Advanced routes: **Throne of Broken Light** — self-amplification: my own hits on any target, no mark needed; **Judgment of the Forsaken** — branding: every attacker's hits on one target burn; **Kingdom of One** — fortress that still strikes; **Usurper's Reckoning** — retaliation.
Changes: 02 Edge of the Regalia: +2 Damage → +3% IDG; 03 Throne of Broken Light: +3 Damage → +5% IDG; 05 Judgment of the Forsaken: +7% AB, +3% IDT → +7% AB; 08 Kingdom of One: +5% DDT, +3% IDG → +5% DDT, +2% IDG; 10 Usurper's Reckoning: +5% REF, +2% IDT → +5% REF.
Damage: no flat Damage.
Strongest fourth purchase: Throne of Broken Light + Mantle of Exile (+10% IDG, +2% IDT, +2% DDT, +2% REF); Judgment of the Forsaken + Mantle of Exile (+2% IDG, +2% IDT, +2% DDT, +10% AB, +2% REF); Kingdom of One + Gaze of the Deposed (+4% IDG, +2% IDT, +10% DDT, +2% REF); Usurper's Reckoning + Gaze of the Deposed (+2% IDG, +2% IDT, +2% DDT, +10% REF).
Concerns: No flat Damage on a Burst-trait kit: Lux is a 50 EP Nuke, so any Damage bonus passes the tier. If the director prefers the Blood-Enchanted Eyes pattern, a +2 Damage payoff would sit on Throne of Broken Light (Lux 50 → 52, Shattered Reflection and Imperial Swords 40 → 42). Exposure is held at the Foundation's +2% on purpose; the offensive routes trade on paper within a few percent (Throne with Searing ahead on targets that are not burning, Judgment with Edge ahead on burning ones), but rotation and uptime were not simulated. Judgment's Afterburn, Kingdom's reduction, Usurper's Reflect and two of the three exposure rows depend on the proposed jutsu-classification resolver (G1); under the current resolver only illuminance's damage buff (Throne's payoff and Kingdom's secondary) and Chrono Stasis row 1 are reachable. The defensive fourths overlap by design (Kingdom with Mirrored Crown and Usurper with Halo of the Unbowed both hold reduction and Reflect); the choice is which one is primary.
Director review: none.

### Godstorm Eclipse

*Fable proposal (2026-10-04 batch rebalance); not director-approved*

Foundations: **Black Sun Rising** — How do I hit harder: amplify my own strikes, or expose the target to everyone's?; **Stormgod's Marrow** — How do I outlast them: refuse the blow, or drink it back?.
Advanced routes: **Total Eclipse** — exposure: the marked target takes more from every source, allies included; **Storm-God Ascendant** — self-amplification: three compounding Mantle buffs raise every hit I land, on any target; **Pillar of Heaven** — fortress; **Eater of Suns** — sustain offense.
Changes: 02 Hammer of the Heavens: +2 Damage → +2% IDT; 03 Total Eclipse: +3 Damage → +4% IDT; 04 Charged Firmament: +3% AB → +2% IDG; 05 Storm-God Ascendant: renamed Lingering Corona → Storm-God Ascendant; +7% AB, +3% IDT → +3% IDG; 08 Pillar of Heaven: +5% DDT, +3% IDG → +5% DDT, +2% LS; 10 Eater of Suns: +3% LS, +2% AB, +2% IDG → +3% LS, +3% IDG.
Damage: no flat Damage.
Strongest fourth purchase: Total Eclipse + Charged Firmament (+4% IDG, +8% IDT); Storm-God Ascendant + Hammer of the Heavens (+7% IDG, +4% IDT); Pillar of Heaven + Black Sun Rising (+2% IDG, +2% IDT, +10% DDT, +2% LS); Eater of Suns + Black Sun Rising (+5% IDG, +2% IDT, +2% DDT, +5% LS).
Concerns: Damage and Afterburn are supported tags with no node: flat Damage would put Raijin's Cage above 50 because potency cannot separate the keystone sides, and Afterburn does the exposure job. Storm-God Ascendant leads on the caster's own Aegis hits (×1.20 against ×1.17 at 3 BP) and Total Eclipse on allies' hits and on Eclipse Marrow; the split rests on a two-round multiplier model with every buff live. Storm-God Ascendant prints +3% Increase Damage Given, the same as Eater of Suns' rider; its value is the route total (+7%, 42%) on three compounding Aegis rows.
Director review: The Shadow + Storm multi-element classification (one element, both or an extension) is the only director decision here; no value needs an exception and no Damage row moves (Raijin's Cage stays at 50)..

### Ha Yanagi

*Fable proposal (2026-10-04 batch rebalance); not director-approved*

Foundations: **Mourning Boughs** — How do I wither the enemy: blunt their blows or open them to every strike?; **Whispering Canopy** — How do I make my own blows land harder: a heavier Blighted Tree or a stronger Wailing Bark window?.
Advanced routes: **Grave Willow's Hush** — suppression; **Hollow at the Heart** — exposure: marks the target for every attacker; **Thousand-Leaf Dream** — sustained amplification of the Wailing Bark window.
Changes: 05 Hollow at the Heart: +7% IDT, +2% DDG → +5% IDT; 08 Nightmare in Bloom: removed; 09 Rising Sap: +3% IDG → +2% IDG; 10 Thousand-Leaf Dream: +4% IDG → +5% IDG.
Damage: Blighted Tree 40 → 42; Petal Nightmare 40 → 42.
Strongest fourth purchase: Grave Willow's Hush + Whispering Canopy (+3% IDG, Wailing Bark self buff 38%); the alternative is Blight Takes Root (+3% IDT, exposure 33%) (+3% IDG, +10% DDG); Hollow at the Heart + Veil of Falling Petals (the route's +2% DDG becomes +5%: suppression 40% / 35%); the alternative is Whispering Canopy (+3% IDG) (+5% DDG, +8% IDT); Thousand-Leaf Dream + Hardened Heartwood (+2 Damage: Blighted Tree 40 -> 42 EP, x1.05; cast inside the window, x1.45 x 1.05 ≈ x1.52 against an unbuffed cast); the alternative is Mourning Boughs (+2% DDG, 37% / 32%) (+2 Damage, +10% IDG).
Concerns: Hardened Heartwood is +2 flat Damage on a Hidden Art leaf. It reaches one meaningful row (Blighted Tree 40 → 42 EP, Normal) and exists so the self root completes a full build and Amplifier has an offensive fourth beside Mourning Boughs' suppression; it is a fourth purchase, not a setup. A Damage-focused player has no capstone. Restoring Nightmare in Bloom would give a near-dominated niche route; raising it to +5 Damage would lift Blighted Tree 40 → 45 (Normal → High). Exposure stops at +8% against Amplifier's +10% (both single rows) because exposure also multiplies allies' hits; Hollow at the Heart +7% (exposure +10%) is the alternative if the director wants parity. Suppression +10% on two compounding rows (×0.33 on a target under both) is the strongest defensive package; it matches the director-approved Blood-Enchanted Eyes suppression on the same 35% / 30% bases. The generated Damage-tier table gives Petal Nightmare's static row an EP tier (40 Normal → 42 Normal); that row is a fixed 40 HP outside the player-jutsu EP ladder, so the label is a renderer limitation.
Director review: Structural: the Burst capstone Nightmare in Bloom is removed (narrow-kit exception, nine nodes and three Advanced Arts) because flat Damage reaches one meaningful row, Blighted Tree; Petal Nightmare's Damage row is static, a fixed 40 HP. Hardened Heartwood stays as a +2 Damage leaf (Blighted Tree 40 → 42 EP). Confirm the three-route tree, or keep Burst as a recorded niche route (+3 Damage, ×1.075 on one Blighted Tree hit every 7 rounds, near-dominated by Thousand-Leaf Dream)..

### Heavenly Sonata

*Fable proposal (2026-10-04 batch rebalance); not director-approved*

Foundations: **Opening Measure** — How do I win offensively: amplify my own song or expose the target?; **Harmonic Balance** — How do I win defensively: shelter myself or silence them?.
Advanced routes: **Fortissimo Finale** — burst: self-amplification set up, controlled raw-Damage payoff; **Prelude to Ruin** — exposure: marks the target for every attacker; **Celestial Sanctum** — fortress; **Final Rest** — suppression.
Changes: 02 Rising Crescendo: +2 Damage → +3% IDG; 03 Fortissimo Finale: +3 Damage → +2 Damage; 05 Prelude to Ruin: +5% IDT, +3% IDG → +5% IDT.
Damage: Foreboding Interlude 40 → 42; Frozen Melody 45 → 47; Lullaby 40 → 42.
Strongest fourth purchase: Fortissimo Finale + Harmonic Balance (+2 Damage, +5% IDG, +2% DDG, +2% IDT, +2% DDT); Prelude to Ruin + Harmonic Balance (+2% IDG, +2% DDG, +10% IDT, +2% DDT); Celestial Sanctum + Opening Measure (+2% IDG, +4% DDG, +2% IDT, +10% DDT); Final Rest + Opening Measure (+2% IDG, +10% DDG, +2% IDT, +4% DDT).
Concerns: Exposure keeps +10% on its single row (Foreboding Interlude 35 → 45%) because it balances the Burst route by multiplier; if the director wants single-row exposure below the self-side routes, Prelude to Ruin +3% (route +8%) is the alternative. The two all-offense 4-BP builds (Burst plus Dissonant Chord, Exposure plus Rising Crescendo) both stack Lullaby's buff with Interlude's exposure; they differ by +2 Damage against +5% more exposure. Fortress and Suppression with their sibling Hidden Art mirror each other (45/42% and 42/45%), as in the director-approved Blood-Enchanted Eyes defensive half.
Director review: none.

### Houkyuken

*Fable proposal (2026-10-04 batch rebalance); not director-approved*

Foundations: **Lodestone Draw** — How do I make each blow land harder: strengthen my own fist, or drag the target onto it?; **Repelling Field** — How do I answer the blows aimed at me: blunt them, or throw them back?.
Advanced routes: **Starfall Hammer** — burst: a self-amplified strike window (own hits on every target); **Inexorable Pull** — exposure: mark one target for every attacker; **Absolute Alignment** — fortress: the Magnetic Assignment window as armour that still swings; **Violent Repulsion** — retaliation: every blow in the window costs the attacker.
Changes: 02 Polarized Fist: +2 Damage → +2% IDG; 03 Starfall Hammer: +3 Damage → +4% IDG; 04 Reversed Polarity: +3% IDT → +2% IDT; 05 Inexorable Pull: +5% IDT, +2% IDG → +4% IDT.
Damage: no flat Damage.
Strongest fourth purchase: Starfall Hammer + Reversed Polarity (all-in; ties Repelling Field at row-weighted 24) (+8% IDG, +4% IDT (both self buffs 43%, both exposure rows 39%)); Inexorable Pull + Polarized Fist (all-in; ties Repelling Field at row-weighted 24) (+4% IDG, +8% IDT (both exposure rows 43%, both self buffs 39%)); Absolute Alignment + Lodestone Draw (+4% IDG, +2% IDT, +10% DDT, +2% REF (DDT 45%, self buffs 39%, exposure 37%, Reflect 42%)); Violent Repulsion + Magnetized Guard (Lodestone Draw is the highest row-weighted fourth at 22) (+7% DDT, +10% REF (Rising Star Reflect 50%, Magnetic Assignment DDT 42%)).
Concerns: No flat Damage on a Burst-trait kit: Magnetic Pulse Strike is 50 EP, so any Damage bonus passes the Nuke tier. If the director prefers the Blood-Enchanted Eyes pattern (+2 Damage payoff; Pulse Strike 50 → 52, Houkyu Dance 45 → 47), Starfall Hammer is where it would go in place of its +4% Increase Damage Given. Burst and Exposure converge at 4 BP: a capstone plus the sibling Hidden Art gives the same ×3.95 on a fully set-up solo strike. They differ only in reach (own hits on every target, Houkyu Dance's area included, against every attacker's hits on the marked target); party-size effects were not simulated. Retaliation keeps Reflect at +10% (50%) on one row; its value scales with the number of attackers in the window and was not simulated.
Director review: none.

### Hyouga Yui

*Fable proposal (2026-10-04 batch rebalance); not director-approved*

Foundations: **Permafrost Heart** — How do I make my Ice strikes land harder: crack them for heavier strikes, or stoke my own window?; **Cocytus Vigil** — How do I control the exchange: open them to every blow, or shut us off from theirs?.
Advanced routes: **Buried in the Avalanche** — burst: exposure set up, then +3 raw Damage on all three circle strikes on every cast; **The Glacier Advances** — sustained amplification: both self buffs compound on every own hit in the window; **Nine Hells Opened** — exposure: a deep mark on Spear's circle and Cocytus's target that lifts allies' hits too; **Locked in Cocytus** — fortress: pure guard for the caster under Cocytus and the party on Glacier's Will's tiles.
Changes: 02 Weight of the Avalanche: +2 Damage → +3% IDT; 05 The Glacier Advances: +5% IDG, +2% DDT → +5% IDG; 08 Nine Hells Opened: +5% IDT, +2 Damage → +5% IDT; 10 Locked in Cocytus: +5% DDT, +2% IDT → +5% DDT.
Damage: Nine Hell's Spear 45 → 48; Cerulean Storm: Avalanche 40 → 43; Glacial Shatter: Purgatory 45 → 48.
Strongest fourth purchase: Buried in the Avalanche + Cocytus Vigil (+3 Damage, +3% IDG, +5% IDT, +2% DDT); The Glacier Advances + Cocytus Vigil (+10% IDG, +2% IDT, +2% DDT); Nine Hells Opened + Rime Mantle (+10% IDT, +5% DDT); Locked in Cocytus + Cracks in the Ice (+5% IDT, +10% DDT).
Concerns: Burst and the Amplifier are deliberately close: with Cocytus Vigil, the R1 Avalanche + Glacier's Will / R2 Spear + Cocytus / R3 Purgatory opener gives 313.6 against 312.2 strike power; Burst adds +6.7 to 7.5% on any strike outside a window and ×(1.40 / 1.37)² ≈ ×1.044 on allies' hits on a target holding both marks, the Amplifier ×1.104 on every other own hit in its window (×1.057 on a target holding Burst's marks). Not simulated. Buried in the Avalanche is a single +3 Damage step, one point above the exemplars' +2 payoffs, because +2 leaves Burst behind the Amplifier on the opener's strikes (306.9 against 312.2); it crosses no tier (48 / 48 / 43) and is the tree's only Damage. Two Hidden Arts print +3% Increase Damage Taken (Weight of the Avalanche as Burst's setup, Cracks in the Ice as Exposure's step); 01+02+06+07 reaches +8% without a capstone and is dominated by Exposure + Permafrost Heart. Both percentage pairs compound when cast in one turn (≈ ×2.10 at 45%), and Spear's exposure lifts allies' hits on every enemy in its circle; not simulated. Five of the nine supported rows depend on the proposed jutsu-classification resolver; off-kit Ice coverage is unverified.
Director review: none.

### Itojinsei

*Fable proposal (2026-10-04 batch rebalance); not director-approved*

Foundations: **Taut Filament** — How do I make my own wires cut harder: a keener strand, or a stronger hand?; **Tangling Snare** — How do I bind the target: blunt its blows, or lay it open to ours?.
Advanced routes: **Severing Lattice** — burst: raw Damage on every Magnet strike, every cast, no setup window; **Weaver Ascendant** — sustained amplification: both self buffs compound on every own hit in the window; **Iron Cocoon** — suppression: every enemy caught in the circles hits softer, for the whole party; **Galvanic Marionette** — exposure: one target marked for every attacker.
Changes: 02 Razor Strands: +2 Damage → +1 Damage; 03 Severing Lattice: +3 Damage → +2 Damage; 04 Threadbound Vigor: +3% IDG → +2% IDG; 05 Weaver Ascendant: +5% IDG, +2% IDT → +4% IDG.
Damage: Iron Web Entrapment 45 → 46 / 48; Wire Blast Plus 40 → 41 / 43; Spiraling Wires 40 → 41 / 43; Lightning Threads 40 → 41 / 43.
Strongest fourth purchase: Severing Lattice + Tangling Snare (highest diagnostic); Threadbound Vigor is the all-offense alternative (+3 Damage, +4% IDG) (+3 Damage, +2% IDG, +2% DDG, +2% IDT); Weaver Ascendant + Tangling Snare; Razor Strands (+1 Damage) is the all-offense alternative (+8% IDG, +2% DDG, +2% IDT); Iron Cocoon + Conductive Seam (lockdown; Taut Filament scores highest row-weighted at 28 vs 27) (+10% DDG, +7% IDT (or +2% IDG, +10% DDG, +4% IDT with Taut Filament)); Galvanic Marionette + Constricting Coils (+7% DDG, +10% IDT).
Concerns: Burst is +3 Damage (+1 Hidden, +2 Advanced) rather than the exemplars' +2 behind a percentage setup: this root's only self tags are Damage and Increase Damage Given, and an Increase Damage Given setup would duplicate Threadbound Vigor. No tier is crossed (40 → 43, 45 → 48); if +2 is wanted as the ceiling, Severing Lattice drops to +1. The control capstones mirror each other's riders (the Iron in the Blood pattern), so with the sibling Hidden Art they converge at 4 BP on +10% / +7% of the same two tags; each still leans its own way. Increase Damage Taken stays at +10% on one row because that row multiplies every matching hit on the target from every attacker; its party value was not simulated.
Director review: none.

### Kyuko-sei

*Fable proposal (2026-10-04 batch rebalance); not director-approved*

Foundations: **Hush of the Void** — How do I make myself the dying star: strike harder or take less?; **Weight of Eons** — How do I wear the enemy down: make them take more or deal less?.
Advanced routes: **Heat Death** — burst: a self-amplified strike window (two compounding self buffs on the caster's hits); **Outlasting Eternity** — fortress: a timed guard on Temporal Erosion; **Collapse of Ages** — exposure: the marked target takes more from every source, allies included; **All Returns to Dust** — suppression: the struck enemy deals less to everyone.
Changes: 01 Weight of Eons: +2% IDG, +2% IDT → +2% IDT, +2% DDG; 02 Shattered Firmament: moved Hidden Art under 01 → Hidden Art under 06; +2 Damage → +2% IDG; 03 Heat Death: +3 Damage → +4% IDG; 04 Aeons Laid Bare: +3% IDT → +2% IDT; 05 Collapse of Ages: +5% IDT, +3% IDG → +4% IDT; 06 Hush of the Void: +2% DDT, +2% DDG → +2% IDG, +2% DDT; 08 Outlasting Eternity: +5% DDT, +3% IDG → +5% DDT; 09 Dimming of Stars: moved Hidden Art under 06 → Hidden Art under 01; 10 All Returns to Dust: +5% DDG, +2% IDT → +5% DDG.
Damage: no flat Damage.
Strongest fourth purchase: Heat Death + Weight of Eons (row-weighted 24); alternative Dilated Moment gives +8% IDG, +5% DDT (+8% IDG, +2% IDT, +2% DDT, +2% DDG); Collapse of Ages + Hush of the Void (row-weighted 24); alternative Dimming of Stars gives +8% IDT, +5% DDG (+8% IDT, +2% IDG, +2% DDT, +2% DDG); Outlasting Eternity + Weight of Eons (row-weighted 20) for defence (+2% DDG on Particle Storm); alternative Shattered Firmament gives +4% IDG (+10% DDT, +2% IDG, +2% IDT, +2% DDG); All Returns to Dust + Hush of the Void (row-weighted 20); alternative Aeons Laid Bare gives +10% DDG, +4% IDT (+10% DDG, +2% IDT, +2% IDG, +2% DDT).
Concerns: No flat Damage node on a kit with four Damage rows and the Burst trait: Ethereal Particle Storm is 50 EP, so any flat Damage passes the Nuke tier. If the director prefers the Blood-Enchanted Eyes pattern, Heat Death is where +2 Damage would go (40 → 42 on three rows, Particle Storm 50 → 52). In a duel Heat Death and Collapse of Ages both multiply the caster's hits on the target; they separate in group play (a self buff on any target and Singularity's area versus a debuff that also multiplies allies' hits) and by Foundation. Rotation and uptime were not simulated. The defensive routes rest on one row each, live 2 rounds per 7-round cooldown. Five of the six buff/debuff rows depend on the proposed jutsu-classification resolver.
Director review: none.

### Loup-Garou

*Fable proposal (2026-10-04 batch rebalance); not director-approved*

Foundations: **Scent of Blood** — How do I bring down the marked quarry: strike it myself or open it to the pack?; **Hunter's Moon** — How do I unleash the beast in myself?.
Advanced routes: **Killing Bite** — burst / execution that feeds: the strike and its heal on one cast; **The Pack Closes** — exposure: one marked target takes more from every attacker, allies included; **Beast Unchained** — sustained amplification: the frenzy after the strike, every own hit on any target.
Changes: 02 Rending Claws: +2 Damage → +1 Damage; 03 Killing Bite: +3 Damage → +2 Damage, +3% HEAL; 05 The Pack Closes: +5% IDT, +3% IDG → +5% IDT; 08 Beast Unchained: +5% IDG, +3% HEAL → +5% IDG.
Damage: Nature's Hunter 40 → 41 / 43.
Strongest fourth purchase: Killing Bite + Hunter's Moon (alternative: Run to Ground -> +3 Damage, +5% IDT, +3% Heal) (+3 Damage, +2% IDG, +2% IDT, +5% Heal (strike 43 EP into 37% exposure, Heal 300 HP per tick, buff 37%)); The Pack Closes + Hunter's Moon (alternative: Rending Claws -> +1 Damage, +10% IDT) (+2% IDG, +10% IDT, +2% Heal (x1.45 x 1.37 = about x1.99 when both windows are up)); Beast Unchained + Scent of Blood (the only legal fourth) (+10% IDG, +2% IDT, +2% Heal (x1.45 x 1.37 = about x1.99 when both windows are up)).
Concerns: Killing Bite is the lightest route in throughput (+3 EP on one strike per 6 rounds, +60 HP per cast); its case is a strike that needs no follow-up window. More flat Damage would put the strike at 44, one point under the High tier; a larger Heal rider is the safer lever if the director wants it stronger. Rending Claws keeps +1 flat Damage on a Hidden Art (40 → 41) because an exposure setup there would stack with The Pack Closes to +13%. Scent of Blood is universal (Hunter's Moon roots a single chain), so Frenzy's fourth purchase is fixed. The 'Loup-Garou' classification extension and off-kit coverage remain director/engine decisions.
Director review: none.

### Lycanthropy

*Fable proposal (2026-10-04 batch rebalance); not director-approved*

Foundations: **The Beast Within** — How do I make the frenzy hit harder?; **Moonbound Vigor** — How do I outlast the fight?.
Advanced routes: **Red Moon Rising** — sustained amplification: the full frenzy; **Undying Hunger** — regeneration: a bigger heal that keeps a frenzy.
Changes: 02 Gnashing Fangs: removed; 03 Jaws of the Alpha: removed; 04 Blood on the Wind: +3% IDG → +2% IDG; 05 Red Moon Rising: +5% IDG → +4% IDG; 08 Undying Hunger (Advanced Art, under 07): added — +5% HEAL, +3% IDG.
Damage: no flat Damage.
Strongest fourth purchase: Red Moon Rising + Moonbound Vigor (+8% IDG, +2% HEAL); Undying Hunger + The Beast Within (+5% IDG, +10% HEAL).
Concerns: Regeneration is the weaker route in raw value: static Heal is 10 HP per point, so its +10% Heal is 100 HP per Frenzy Assault cast; the +3% frenzy rider keeps it a choice rather than a trap. Both Foundations are in every legal full build (two 3-node chains); the choice is which chain to finish. Damage is left unamplified; a +2 Damage payoff would lift Feral Wrath 50 → 52, above the Nuke tier.
Director review: none.

### Megumi Kijo

*Fable proposal (2026-10-04 batch rebalance); not director-approved*

Foundations: **Hagmother's Welcome** — How do I make my guest harmless?; **Mountain Hag's Mercy** — How do I keep the hag fed and whole: feed on my guests or tend my hearth?.
Advanced routes: **Appetite of Oblivion** — sustain offense: Laughter's heal set up, controlled +2 Damage payoff; **Cradle of the Kijo** — suppression; **The Ever-Lit Hearth** — healing field for the caster and allies.
Changes: 02 Teeth Behind the Smile: moved Hidden Art under 01 → Hidden Art under 06; +2 Damage → +3% HEAL; 03 Appetite of Oblivion: +3 Damage → +2 Damage; 05 Cradle of the Kijo: +5% DDG, +2% HEAL → +5% DDG; 08 The Ever-Lit Hearth: renamed Laughter That Mends → The Ever-Lit Hearth; +3% HEAL, +3% IH → +5% IH.
Damage: Phantom Realm Oblivion 40 → 42; Onibaba's Laughter 45 → 47.
Strongest fourth purchase: Appetite of Oblivion + Nursed by Demon Hands (+2 Damage, +5% IH, +5% HEAL); Cradle of the Kijo + Mountain Hag's Mercy (+10% DDG, +2% IH, +2% HEAL); The Ever-Lit Hearth + Teeth Behind the Smile (+10% IH, +5% HEAL).
Concerns: Appetite of Oblivion is the leanest payoff (+2 EP on two cooldown-7 attacks with a 450 HP tick); a sharper +3 (40 → 43, 45 → 48) would still cross no tier if the director wants it. The Ever-Lit Hearth's 40% Increase Heal reaches allies in the field and Benevolence's own absorb; its same-window effect on Laughter's tick and on lifesteal past the leech budget is unverified. The 'Megumi Kijo' classification extension is a director/engine decision; off-kit coverage is unverified.
Director review: none.

### Musashi Ken

*Fable proposal (2026-10-04 batch rebalance); not director-approved*

Foundations: **Drawn Steel** — How do I win with the drawn blade: make the draw itself land harder, or keep a chain of buffs multiplying every cut?; **Reading the Field** — How do I hold Heiho's guard?.
Advanced routes: **Cut of No Return** — burst / execution: the draw lands at Normal tier on its own cast; **Two Heavens as One** — sustained amplification: three compounding self buffs; **Victory in the Sheath** — fortress: Heiho's guard.
Changes: 02 Single Stroke: +2 Damage → +1 Damage; 05 Two Heavens as One: +2% IDG, +2% DDT → +2% IDG; 08 Victory in the Sheath: +5% DDT, +1% IDG → +5% DDT; 09 Answering Cut: removed.
Damage: Iaido 38 → 39 / 42; Iaijutsu 38 → 39 / 42.
Strongest fourth purchase: Cut of No Return + Second Sword (+4 Damage, +3% IDG); Two Heavens as One + Reading the Field (+5% IDG, +2% DDT); Victory in the Sheath + Drawn Steel (+2% IDG, +10% DDT).
Concerns: Burst and Tempo are close in throughput by design (rough model: within about 1% either way over a no-tree build, depending on how much damage the strikes carry); Burst's case is immediacy and the Light → Normal step on two strikes (38 → 42), Tempo's is ×1.40 per live buff on every element-less hit. If the director wants Burst sharper, Cut of No Return at +4 (38 → 43) still stays below High but would put Burst level with Tempo in filler-heavy rotations and ahead in strike-heavy ones. Single Stroke keeps flat Damage on a Hidden Art (+1, 38 → 39, no tier crossing) because both percentage setups fail: Increase Damage Given stacks with Two Heavens as One and Decrease Damage Taken twins Reading the Field. Drawn Steel is universal now that Answering Cut is gone; the Fortress build is fixed (01, 06, 07, 08) and is pure guard. The 'Musashi Ken' classification extension and off-kit coverage remain director/engine decisions.
Director review: none.

### Namikaze

*Fable proposal (2026-10-04 batch rebalance); not director-approved*

Foundations: **Wind at the Back** — How do I turn the wind into killing pressure: cut harder myself, or make every hit on them burn?; **Eye of the Storm** — How do I win the exchange defensively: weather their blows, or smother them?.
Advanced routes: **Cleaving Cyclone** — burst: self-buff setup, controlled raw-Damage payoff; **Fanning the Flames** — burn pressure: team-wide downstream Afterburn; **Heart of the Tempest** — fortress: guard the caster; **Dead Calm** — suppression: blunt every enemy in the zone for the whole party.
Changes: 02 Razor Crosswind: +2 Damage → +3% IDG; 03 Cleaving Cyclone: +3 Damage → +2 Damage; 05 Fanning the Flames: +7% AB, +2% IDG → +7% AB; 08 Heart of the Tempest: +5% DDT, +2% IDG → +5% DDT; 10 Dead Calm: +5% DDG, +1 Damage → +5% DDG.
Damage: Wind Step 40 → 42; Tempest Shroud 40 → 42; Cutting Tempest 45 → 47.
Strongest fourth purchase: Cleaving Cyclone + Eye of the Storm (+2 Damage, +6% IDG, +2% DDG, +2% DDT); Fanning the Flames + Razor Crosswind (+6% IDG, +10% AB); Heart of the Tempest + Wind at the Back (+3% IDG, +2% DDG, +10% DDT); Dead Calm + Wind at the Back (+3% IDG, +10% DDG, +2% DDT).
Concerns: Heart of the Tempest and Dead Calm are single-effect capstones; if a rider is wanted, the Arashima pattern (+2% of the sibling defensive tag) fits, but it makes the two all-defense 4-BP builds converge (+10% / +7% mirrors). Fanning the Flames plus Razor Crosswind (+6% Increase Damage Given, +10% Afterburn) is the strongest offence allocation; Afterburn is team-wide, so its edge over Cleaving Cyclone grows with party size and was not simulated. Soaring Fujin's obtainability is unverified; without it Increase Damage Given is one Wind-only row and Razor Crosswind is a thin setup.
Director review: none.

### Nature's Blessing

*Fable proposal (2026-10-04 batch rebalance); not director-approved*

Foundations: **Thorn and Rot** — How do I bring down the marked target?; **Sap of the Grove** — How do I keep the grove standing?.
Advanced routes: **Old Growth's Wrath** — burst: the Fury → Curse one-two with controlled raw Damage; **Blight and Harvest** — exposure: a deeper mark for every hit on one target; **Everbloom Sanctuary** — sanctuary: sustained healing for everyone in the circle.
Changes: 02 Ironwood Lash: +2 Damage → +1 Damage; 03 Old Growth's Wrath: +3 Damage → +2 Damage; 05 Blight and Harvest: +5% IDT, +3% IH → +5% IDT; 08 Everbloom Sanctuary: +3% HEAL, +3% IH → +5% IH; 09 Sudden Greening: renamed Bramble Warden → Sudden Greening; +1 Damage, +1% IH → +3% HEAL.
Damage: Nature's Fury 40 → 41 / 43; Nature's Curse 40 → 41 / 43.
Strongest fourth purchase: Old Growth's Wrath + Stripped Bark (Fury marks at 40%; Curse 43 EP x1.40, so the one-two is about 103 EP) (+3 Damage, +5% IDT); Blight and Harvest + Ironwood Lash for offence (41 + 41 x1.45 is about 100 EP); Sap of the Grove for the example's hybrid (420 HP tick, IH 32%) (+1 Damage, +10% IDT (Lash) or +10% IDT, +2% IH, +2% Heal (Sap)); Everbloom Sanctuary + Sudden Greening (450 HP tick; 450 x1.40 = 630 HP on the tiles vs 520 at base) (+10% IH, +5% Heal).
Concerns: Healing is the kit's low-leverage side: +1% Heal is +10 HP once per Bastion cast and Increase Heal only multiplies healing in a 2-round, positional window, so Everbloom Sanctuary is the trait-identity pick rather than the power pick; the kit has no Decrease Damage, Reflect or Lifesteal rows to give it more weight. Exposure (45%) is a single row but multiplies every non-pierce hit the marked target takes from anyone for 2 rounds; in team play Blight and Harvest is the strongest route even as a single-effect capstone. Burst at +3 Damage (43 EP) is deliberately below the 45 High tier, and its +2 Damage capstone reads lighter on the poster than Blight and Harvest's +5%; in EP terms it leads the Fury → Curse one-two, and +4 (44) is the most it could take without reaching the High tier. Damage +3 and Increase Damage Taken +10% reach every Wood jutsu; off-kit Wood coverage is unverified.
Director review: none.

### Night Parade of A Thousand Demons

*Fable proposal (2026-10-04 batch rebalance); not director-approved*

Foundations: **Hour of the Ox** — How do I let the Conduit carry me through the fight: feed on it or wall it out?; **Oni's Heavy Hand** — How do I break the enemy: mark them for the kill or crush the strength out of them?.
Advanced routes: **Feast of a Thousand Mouths** — sustain offense; **Barred Gate of Yomi** — fortress; **March of a Thousand Demons** — burst: exposure set up, controlled raw-Damage payoff; **Toll of the Night Bell** — suppression.
Changes: 05 Barred Gate of Yomi: +5% DDT, +2% LS → +5% DDT; 07 Dread of the Procession: renamed Grip of the Yurei → Dread of the Procession; +2 Damage → +3% DDG; 08 March of a Thousand Demons: moved Advanced Art under 07 → Advanced Art under 09; +3 Damage → +2 Damage; 10 Toll of the Night Bell: moved Advanced Art under 09 → Advanced Art under 07; +5% IDT, +3% DDG → +5% DDG.
Damage: Possessing Yurei 45 → 47; Oni Hammer Swing 45 → 47.
Strongest fourth purchase: Feast of a Thousand Mouths + Hide of the Oni (01, 02, 03, 04). Oni's Heavy Hand is the highest diagnostic (row-weighted 16). (+5% IDG, +5% DDT, +5% LS (Conduit IDG 40 / DDT 40 / LS 45). With Oni's Heavy Hand: +5% IDG, +2% DDG, +2% IDT, +2% DDT, +5% LS.); Barred Gate of Yomi + Oni's Heavy Hand (01, 04, 05, 06) (+2% IDG, +2% DDG, +2% IDT, +10% DDT (Conduit DDT 45; a hit from a suppressed enemy is cut x0.68 x 0.55 ~ x0.37). With Hungry Ghost's Draught: +2% IDG, +10% DDT, +2% LS (LS 42).); March of a Thousand Demons + Hour of the Ox (01, 06, 08, 09) (+2 Damage, +2% IDG, +2% DDG, +5% IDT, +2% DDT. A marked target inside the Conduit window takes x1.40 x 1.37 ~ x1.92, or x2.00 with the +2 EP.); Toll of the Night Bell + Marked by the Herald (06, 07, 09, 10). Hour of the Ox is the highest diagnostic (row-weighted 16). (+10% DDG, +5% IDT (Hammer suppression 40%, Herald exposure 40%). With Hour of the Ox: +2% IDG, +10% DDG, +2% IDT, +2% DDT (a suppressed enemy's hit in the Conduit window is cut x0.60 x 0.63 ~ x0.38).).
Concerns: The old Pressure route (+10% Herald exposure) is dropped; exposure now stops at +5% as Burst setup. If the director wants a dedicated team-exposure route, it would replace Suppression and should stay well under +10% because the exposure reaches every source's hits. Burst's distinct value is narrow. Suppression's realistic fourth (Marked by the Herald, 06, 07, 09, 10) takes Burst's whole 40% exposure setup, so against Burst with Dread of the Procession (06, 07, 08, 09) the only difference is +2 EP (×1.044 on two 60 AP, cooldown 7 hits) versus +5% Hammer suppression. This mirrors the director-accepted Blood-Enchanted Eyes pattern (Feast of the Fallen with Opened Veins); widening exposure past +5% to make it unique was rejected because exposure reaches every source's hits. Not simulated. Barred Gate of Yomi and Toll of the Night Bell are single-tag capstones, lighter than the Blood-Enchanted Eyes and Arashima fortress / suppression capstones. Each rider the kit offers either stacks with a sibling route within 4 BP (Lifesteal or Increase Damage Given on the Fortress into Feast via Hungry Ghost's Draught; Decrease Damage Given on the Fortress and Decrease Damage Taken on Toll into each other across the roots; Increase Damage Taken on Toll into Burst via Marked by the Herald) or hands one route's payoff to another (flat Damage; Lifesteal on Toll). Feast keeps +3% Increase Damage Given (route +5%), below the +5% capstone in the Blood-Enchanted Eyes and Arashima templates. At +5% Feast with Oni's Heavy Hand (×1.42 × 1.37 ≈ ×1.95 with 45% Lifesteal) would come within 3% of Burst with Hour of the Ox (≈ ×2.00) on the two kit hits and pass it on every other hit; the director may still prefer the template value. Suppression raises the Hammer's ally-hazard Decrease Damage Given to 40% for allies standing in the circle as well as enemies.
Director review: none.

### Oblivion Seal

*Fable proposal (2026-10-04 batch rebalance); not director-approved*

Foundations: **Brand of Oblivion** — How do I press the attack: hit harder in the beast's window, or feed on every blow I land?; **Umbral Refuge** — How do I control the exchange: refuse their blows, or brand them to take more while I hold?.
Advanced routes: **Absolute Erasure** — self-amplification burst: the beast window multiplies every hit I land, on any target; **Maw of Oblivion** — drain (sustain offense): every hit I land in Surge's window heals me; **Sealed Against Ruin** — fortress; **Writ of Oblivion** — combat dominance: the branded foe takes more from every attacker while Surge's reduction holds.
Changes: 02 Umbral Claws: +2 Damage → +3% IDG; 03 Absolute Erasure: +3 Damage → +5% IDG; 04 Unraveled Wards: moved Hidden Art under 01 → Hidden Art under 06; +3% IDT → +2% IDT; 05 Writ of Oblivion: +5% IDT, +3% IDG → +4% IDT, +2% DDT; 08 Sealed Against Ruin: +5% DDT, +3% IDG → +5% DDT; 09 Hungering Shade: moved Hidden Art under 06 → Hidden Art under 01; 10 Maw of Oblivion: +3% LS, +2% DDT, +3% IDG → +3% LS.
Damage: no flat Damage.
Strongest fourth purchase: Absolute Erasure + Hungering Shade (+10% IDG, +2% IDT, +2% LS); Writ of Oblivion + Brand of Oblivion (+2% IDG, +8% IDT, +4% DDT); Sealed Against Ruin + Brand of Oblivion (+2% IDG, +2% IDT, +10% DDT); Maw of Oblivion + Umbral Claws (+5% IDG, +2% IDT, +5% LS).
Concerns: Solo offense is close to additive in Increase Damage Given and Increase Damage Taken points, so Absolute Erasure with Umbral Refuge (×1.45 × 1.37 ≈ ×1.99, 37% reduction) and Writ of Oblivion with Brand of Oblivion (×1.37 × 1.43 ≈ ×1.96, 39% reduction) trade about 1.4% offense for 2% reduction alone; with allies on the branded target Writ is the stronger build. Absolute Erasure with Hungering Shade and Maw of Oblivion with Umbral Claws share three nodes; the capstone decides +5% Increase Damage Given (burst) or +3% Lifesteal (drain), the Blood-Enchanted Eyes and Arashima sibling pattern. Damage is left unamplified, so the Burst trait rides on multipliers; restoring any raw-Damage payoff would lift Shadow Tether past 50 and need an above_nuke_rationale.
Director review: none.

### Primal Radiance

*Fable proposal (2026-10-04 batch rebalance); not director-approved*

Foundations: **Hunter's Brand** — How do I make the branded prey pay for every hit?; **Hide and Fang** — How do I empower the beast itself: hit harder or refuse to fall?.
Advanced routes: **Pyre of the Hunted** — attrition: one brand makes every hit on the prey burn, allies' included; **Den of Embers** — fortress; **Primal Rampage** — sustained amplification: the caster's hits land harder on every target.
Changes: 02 Fang and Ember: removed; 03 Apex Conflagration: removed; 05 Pyre of the Hunted: +7% AB, +3% IDT → +7% AB; 08 Den of Embers: +5% DDT, +2% IDG → +5% DDT; 10 Primal Rampage: +5% IDG, +2% DDT → +5% IDG.
Damage: no flat Damage.
Strongest fourth purchase: Pyre of the Hunted + Hide and Fang (+2% IDG, +2% IDT, +2% DDT, +10% AB); Den of Embers + Kindled Fury (+5% IDG, +10% DDT); Primal Rampage + Radiant Hide (+10% IDG, +5% DDT).
Concerns: Pyre of the Hunted and Primal Rampage are close in solo (a Squirrel hit on the mark ×2.72 against ×2.68 with their best fourths); Pyre leads in team play because Afterburn adds to allies' hits of any element, Rampage on every other target. Not simulated. Hide and Fang is universal, so Pyre of the Hunted's fourth purchase is forced; Hunter's Brand roots one chain because Afterburn and exposure share one cast. Increase Damage Taken reaches only +2% (Hunter's Brand): exposure is kept near base so the brand's setup does not compound its own Afterburn payoff. Two of three routes (Pyre of the Hunted, Den of Embers) amplify element-less rows the current row-element resolver cannot reach; they depend on the proposed jutsu-classification resolver.
Director review: Structural: flat Damage is removed rather than re-cut (any flat Damage lifts Fire Style: Beast past 50), leaving three Advanced Arts with Hide and Fang in every build. Confirm the narrow-kit exception, or choose the Blood-Enchanted Eyes pattern as a fourth route (Fang and Ember +3% Increase Damage Taken → Apex Conflagration +2 Damage: Beast 50 → 52, Squirrel 40 → 42)..

### Reptilian

*Fable proposal (2026-10-04 batch rebalance); not director-approved*

Foundations: **Chimeric Blood** — How do I win the exchange: bite harder or harden the hide?; **Blood of the Brood** — How do I keep the brood fed?.
Advanced routes: **Jaws of the Chimera** — burst: stack both Increase Damage Given buffs into one amplified window; **Basilisk Carapace** — fortress; **Feast of Scales** — pack sustain: the circle leeches deeper from harder hits.
Changes: 02 Apex Instinct: +1% IDG → +2% IDG; 03 Jaws of the Chimera: +2% IDG, +2% LS → +3% IDG; 05 Basilisk Carapace: +5% DDT, +2% LS → +5% DDT; 08 Feast of Scales: +2% LS, +2% DDT → +2% LS, +2% IDG.
Strongest fourth purchase: Jaws of the Chimera + Hardened Scales (+3% DDT; the same Chimera window becomes a 40% hide); alternative Blood of the Brood (+1% LS) (+7% IDG, +5% DDT (row-weighted 19)); Basilisk Carapace + Apex Instinct (+2% IDG; both IDG rows 39%); alternative Blood of the Brood (+1% LS) (+4% IDG, +10% DDT (row-weighted 18)); Feast of Scales + Chimeric Blood (the only legal fourth) (+4% IDG, +2% DDT, +5% LS (row-weighted 15)).
Concerns: Jaws of the Chimera rises from +5% to +7% IDG on two rows that compound on the caster (×1.96 → ×2.02 with both buffs); it matches Feast of the Fallen's 35 → 42% on two self IDG rows. Pack sustain is team-dependent: solo the circle reaches only the caster, so it is likely the weakest 1v1 route (not simulated). Chimeric Blood stays universal (all 8 legal builds), as in Draft 4. The Reptilian classification extension and off-kit coverage remain director/engine decisions.
Director review: none.

### Sands of Time

*Fable proposal (2026-10-04 batch rebalance); not director-approved*

Foundations: **Borrowed Hours** — How do I turn time into damage: quicken my own hand or age my target?; **Suspended Moment** — How do I hold back the hour: shelter myself or slow the hands raised against us?.
Advanced routes: **Sovereign of the Hour** — self-amplification: my own hits in the window, on any target; **The Inevitable Hour** — exposure: one marked target takes more from everyone; **Timeless Bastion** — fortress: endure and recover; **Stilled Hourglass** — suppression: blunt every enemy in the circle.
Changes: 02 Quickened Sands: renamed Grinding Sands → Quickened Sands; +2 Damage → +3% IDG; 03 Sovereign of the Hour: renamed Erosion of Eternity → Sovereign of the Hour; +3 Damage → +5% IDG; 04 Brittle with Age: +3% IDT → +2% IDT; 05 The Inevitable Hour: +5% IDT, +3% IDG → +4% IDT; 06 Suspended Moment: +2% DDT, +2% HEAL → +2% DDT, +2% DDG; 08 Timeless Bastion: +5% DDT, +3% HEAL → +5% DDT, +5% HEAL; 10 Stilled Hourglass: +7% DDG, +2% DDT → +5% DDG, +2% DDT.
Damage: no flat Damage.
Strongest fourth purchase: Sovereign of the Hour + Suspended Moment (+10% IDG, +2% DDG, +2% IDT, +2% DDT); The Inevitable Hour + Suspended Moment (+2% IDG, +2% DDG, +8% IDT, +2% DDT); Timeless Bastion + Borrowed Hours (+2% IDG, +2% DDG, +2% IDT, +10% DDT, +5% HEAL); Stilled Hourglass + Borrowed Hours (+2% IDG, +10% DDG, +2% IDT, +4% DDT).
Concerns: Damage is left unamplified on a kit with three Sand Damage rows (40/40/50); a narrow +2 payoff would need an above_nuke_rationale for Eternity Flux 50 → 52. Increase Damage Taken +8% on two compounding, team-wide rows is above the +5% the director accepted for exposure on Blood-Enchanted Eyes and Shakunetsu Sakura; it is the kit's primary Control identity and carries no Damage payoff here. Increase Damage Given reaches +10% on one self row with no secondary, as on Shakunetsu Sakura's approved routes; the narrow-coverage rule would also allow +8% with a rider.
Director review: none.

### Sea-King's Blessing

*Fable proposal (2026-10-04 batch rebalance); not director-approved*

Foundations: **Scales of the Deep** — How do I win the exchange myself: hit harder, or take less?; **Salt in the Wound** — How do I make them take more from everyone?.
Advanced routes: **Weight of the Trench** — burst: unconditional raw Damage on every Water hit, no setup; **Hull of the Leviathan** — fortress; **Wrath of the Sea-King** — exposure: team-wide amplification on marked targets.
Changes: 02 Grip of the Riptide: +2 Damage → +1 Damage; 03 Weight of the Trench: +3 Damage → +2 Damage; 05 Hull of the Leviathan: +5% DDT, +1 Damage → +5% DDT; 08 Wrath of the Sea-King: +5% IDT, +1 Damage → +5% IDT.
Damage: Sea King's Armor 38 → 39 / 41; Crushing Abyss 38 → 39 / 41.
Strongest fourth purchase: Weight of the Trench + Salt in the Wound (+2% IDT; alternative Deepwater Carapace +3% DDT) (+3 Damage, +2% IDT, +2% DDT (Armor/Abyss 41 EP, Abyss 32%, Dome 37%, Armor DDT 32%)); Hull of the Leviathan + Salt in the Wound (+2% IDT; alternative Grip of the Riptide +1 Damage) (+10% DDT, +2% IDT (Armor 40% for 2 rounds per cooldown 7; Abyss 32%, Dome 37%)); Wrath of the Sea-King + Scales of the Deep (the only legal fourth) (+10% IDT, +2% DDT (Abyss 40%, Dome 45%, compounding x2.03 on Water hits; Armor 32%)).
Concerns: Exposure keeps +10% Increase Damage Taken on two compounding, team-wide rows; it ties Burst on the caster's own rotation and leads in groups. +8% (Wrath of the Sea-King +3%) is the fallback if the director wants it below Burst solo. Scales of the Deep stays a universal node: Exposure's fourth purchase is forced to +2% Decrease Damage Taken. Both kit hits cross Light → Normal (38 → 41) under Weight of the Trench; off-kit Water damage rows reached by +3 are unverified.
Director review: none.

### Shadow Weaver

*Fable proposal (2026-10-04 batch rebalance); not director-approved*

Foundations: **Loom of Dusk** — How do I win the exchange: strike harder or blunt their strikes?; **Cloak of Woven Night** — How do I fight from inside my own weave: thicken it or sharpen it?.
Advanced routes: **Night Unraveled** — burst: sharpened self buffs into a controlled raw-Damage payoff; **Strings Cut Short** — suppression: sever one enemy's offense; **Seamless Shroud** — fortress: armour inside Shadow Shell.
Changes: 02 Barbed Thread: +2 Damage → +2% IDG; 03 Night Unraveled: +3 Damage → +2 Damage, +2% IDG; 05 Strings Cut Short: +5% DDG, +3% IDG → +5% DDG, +2% DDT.
Damage: Shadow Domain 40 → 42; Shadow Severance 40 → 42; Shadow Step 40 → 42; Shadow Dance 40 → 42.
Strongest fourth purchase: Night Unraveled + Cloak of Woven Night (+2 Damage, +6% IDG, +2% DDG, +3% DDT); Strings Cut Short + Barbed Thread (+4% IDG, +10% DDG, +2% DDT); Seamless Shroud + Umbral Whetstone (+5% IDG, +10% DDT).
Concerns: Increase Damage Given rises from a +5% maximum to +7% (Loom of Dusk, Barbed Thread, Cloak of Woven Night, Umbral Whetstone) and +6% on the Burst route; it is the tree's highest-leverage tag because the three self buffs compound (×1.42³ ≈ ×2.86 against ×2.46 when all three windows overlap). Burst trades raw Damage for buff leverage: over one assumed rotation (Shell with Domain, then Step, Severance, Dance) it is estimated at about +14% against about +16% for the old +5 Damage route, with no tier jump (not simulated). If the director wants Burst to read as raw burst, +3 Damage on Night Unraveled (40 → 43, still Normal) instead of its +2% Increase Damage Given is the alternative. Suppression and Fortress each rest on one element-less row that the current resolver cannot reach (G1).
Director review: none.

### Shakunetsu Sakura (protected)

*Director-approved (RUL-2026-10-04-002); protected from the 2026-10-04 batch*

Foundations: **Ember Dragon's Roots** — How do I increase my killing pressure?; **Falling Ember Petals** — How do I control the exchange?.
Advanced routes: **Dragon in Full Blossom** — sustained amplification; **Scorching Hanami** — combat dominance; **Conflagration in Bloom** — exposure into a narrow burst; **Deluge of Burning Petals** — suppression with sustain.
Damage: Hiru-Sakura: Sakuragari 40 → 42; Hiru-Sakura: Sakura-ame 50 → 52.
Strongest fourth purchase: Dragon in Full Blossom + Blossom Dominion (+13% IDG, +5% HEAL); Conflagration in Bloom + Smothering Petal Rain (+2 Damage, +5% DDG, +5% IDT); Scorching Hanami + Kindled Boughs (+13% IDG, +3% DDG); Deluge of Burning Petals + Burning Petal Carpet (+10% DDG, +2% IDT, +5% HEAL).
Director review: Two mechanical consequences recorded for confirmation: +13% Increase Damage Given with a capstone plus the sibling Hidden Art, and Sakura-ame 50 → 52 under Conflagration in Bloom..

### Shinrai Ou

*Fable proposal (2026-10-04 batch rebalance); not director-approved*

Foundations: **Mandate of Thunder** — How do I make my thunder land harder: charge myself or expose them?; **Raiment of Storms** — How do I make attackers pay for striking me?.
Advanced routes: **Thunder King's Wrath** — burst: the Cloak and Raijin self buffs compound on every hit in their windows; **Judgement from Above** — exposure: Hammer marks the field and every matching hit on it lands harder, allies' included; **Thunder Answers Thunder** — retaliation: the Storm Cloak returns half of every blow.
Changes: 02 Vajra Tempering: +2 Damage → +2% IDG; 03 Thunder King's Wrath: +3 Damage → +3% IDG; 05 Judgement from Above: +5% IDT, +3% IDG → +5% IDT; 08 Thunder Answers Thunder: +5% REF, +3% IDG → +5% REF.
Damage: no flat Damage.
Strongest fourth purchase: Thunder King's Wrath + Lightning Rod (+7% IDG, +5% IDT); Judgement from Above + Vajra Tempering (+4% IDG, +10% IDT); Thunder Answers Thunder + Mandate of Thunder (+2% IDG, +2% IDT, +10% REF).
Concerns: Damage is a supported tag with no node; the kit's Burst trait is expressed through compounding Increase Damage Given. The Blood-Enchanted Eyes pattern (+2 Damage capstone) would put Daibutsu Thunder at 52. Thunder King's Wrath is held at +7% Increase Damage Given because three rows compound (×1.16 when the Cloak and Raijin windows overlap); it remains the strongest solo route. Mandate of Thunder is universal, so the Retaliation route's fourth purchase is forced; the kit has no second defensive tag for a leaf under Raiment of Storms. The Reflect row and two of the three Increase Damage Given rows are element-less and depend on the proposed jutsu-classification resolver.
Director review: none.

### Shinseina Ki

*Fable proposal (2026-10-04 batch rebalance); not director-approved*

Foundations: **Hallowed Seed** — How do I make my own strikes land harder?; **Grasping Roots** — How do I make the grove mark them for everyone?.
Advanced routes: **Heartwood Awakened** — self amplification: every own hit, any target, in the Forest Wisdom window; **Judgement of the Grove** — exposure: the Grove circle multiplies every attacker's hits (team, area).
Changes: 02 Fangs of Heartwood: removed; 03 The Forest Devours: removed; 04 Rooted in Wisdom: +3% IDG → +1% IDG; 05 Heartwood Awakened: +5% IDG → +3% IDG; 08 Judgement of the Grove: +5% IDT, +1 Damage → +5% IDT.
Damage: no flat Damage.
Strongest fourth purchase: Heartwood Awakened + Grasping Roots (+6% IDG, +2% IDT); Judgement of the Grove + Hallowed Seed (+2% IDG, +10% IDT).
Concerns: Heartwood Awakened is held at +6% because both Forest Wisdom rows compound; Rooted in Wisdom at +2% (route +7%, about ×1.12 in a duel) would make self amplification the default even in duels. Rooted in Wisdom's +1% is a small printed step; it keeps the no-capstone hybrid (about ×1.08 in a duel) clearly below both capstones (about ×1.11). Exposure's advantage is team play; in solo fights against several enemies self amplification is stronger because it does not depend on the circle.
Director review: Structural: the Damage route (Fangs of Heartwood → The Forest Devours) is removed rather than re-cut, because any flat Damage lifts Eternal Forest past 50; the tree shrinks to two chains with both Foundations universal. Confirm, or choose the Blood-Enchanted Eyes pattern as a third route (exposure setup → +2 Damage payoff, Serpent and Grove 40 → 42, Eternal Forest 50 → 52)..

### Shiroi Youso

*Fable proposal (2026-10-04 batch rebalance); not director-approved*

Foundations: **Fivefold Kindling** — How do I break the target: one decisive strike, or a burn that every hit feeds?; **Pale Vessel** — How do I strengthen myself: strike harder or stand firmer?.
Advanced routes: **Divine Convergence** — burst / execution: exposure set up, controlled +2 Damage payoff; **White Immolation** — attrition: a burn that every hit on the target feeds; **White Maelstrom** — sustained amplification: two compounding self buffs on every five-element hit, injected children included; **Eye of the Tempest** — fortress with sustain.
Changes: 01 Fivefold Kindling: +2% IDG, +2% IDT → +2% IDT; 02 Opened to the Elements: renamed Pale Lightning → Opened to the Elements; +2 Damage → +3% IDT; 03 Divine Convergence: +3 Damage → +2 Damage; 05 White Immolation: +7% AB, +2% IDT → +7% AB; 06 Pale Vessel: renamed Bedrock and Tide → Pale Vessel; +2% DDT, +2% HEAL → +2% IDG, +2% DDT; 08 Eye of the Tempest: +5% DDT, +3% IDG → +5% DDT, +5% HEAL; 09 Rising Currents: renamed Tidal Mending → Rising Currents; +3% HEAL → +2% IDG; 10 White Maelstrom: renamed Pull of the Undertow → White Maelstrom; +5% IDT, +2% DDT → +4% IDG.
Damage: Lightning Release 40 → 42; Element Divine 45 → 47.
Strongest fourth purchase: Divine Convergence + Pale Vessel (+2 Damage, +2% IDG, +5% IDT, +2% DDT); White Immolation + Pale Vessel (+2% IDG, +2% IDT, +2% DDT, +10% AB); Eye of the Tempest + Rising Currents (+4% IDG, +10% DDT, +5% HEAL); White Maelstrom + Gale Bulwark (+8% IDG, +5% DDT).
Concerns: White Maelstrom is held at +8% Increase Damage Given because the two self buffs compound; if Voltari's own self buff is in scope, three buffs can compound (×1.43³ ≈ ×2.92), not simulated. The two native burns already pass the 60% per-hit Afterburn cap together, so White Immolation's value depends on alternating Lightning Release and Element Divine. Fivefold Kindling and Opened to the Elements raise Element Divine's area exposure, which also lands on allies in the circle. Earth Release's Decrease Damage Taken and Water Release's Heal are reachable only through an authored jutsu classification (ENGINE_GAP_REGISTER G1).
Director review: Classification only: the Fire + Lightning multi-element scope remains a director decision (unchanged by this batch). No director exception and no Damage row above 50..

### Suragu

*Fable proposal (2026-10-04 batch rebalance); not director-approved*

Foundations: **Magma Vein** — How do I win offensively: empower my own Lava strikes or set the enemy burning?; **Cooling Crust** — How do I stay standing in a long fight: harden the crust or drink the flow?.
Advanced routes: **Pyroclastic Surge** — burst: Lava Wave buff window into a narrow raw-Damage payoff; **The Mountain Wakes** — burn pressure: one Eruption makes every later hit on the target burn, allies' included; **Heart of the Caldera** — fortress: a team mitigation tile; **Unquenchable Furnace** — sustain: leech and endure.
Changes: 02 Scalding Tide: +2 Damage → +3% IDG; 03 Pyroclastic Surge: +3 Damage, +1% LS → +3% IDG, +2 Damage; 05 The Mountain Wakes: +7% AB, +3% IDT, +3% IDG → +7% AB; 08 Heart of the Caldera: +5% DDT, +3% IDG → +5% DDT, +2% IDG.
Damage: Magma Slayer 45 → 47; Infernal Stream 40 → 42.
Strongest fourth purchase: Pyroclastic Surge + Clinging Slag (+2 Damage, +8% IDG, +2% IDT, +3% AB); The Mountain Wakes + Scalding Tide (+5% IDG, +2% IDT, +10% AB); Heart of the Caldera + Magma Vein (+4% IDG, +2% IDT, +10% DDT); Unquenchable Furnace + Magma Vein (+2% IDG, +2% IDT, +4% DDT, +5% LS).
Concerns: Burst and Burn are set by multiplier and delivery, not printed totals: Burst's edge is the caster's own Lava strikes (Magma Slayer 47 in PVP), Burn's is every non-pierce hit on the target, allies' included. Rotation, AP and uptime were not simulated. Only Burst works under the current resolver (Lava Wave's buff row and both Damage rows carry Lava); Burn, Fortress, Sustain and Blow's exposure need the jutsu-classification resolver (G1 for Blow). +2 Damage reaches every Lava Damage row in scope; off-kit Lava jutsu are unverified, so an off-kit 50 EP Lava attack would become 52.
Director review: none.

### Taiyo Kami (protected)

*Approved worked reference; protected from the 2026-10-04 batch (values unchanged)*

Damage: Solar Reverb 40 → 42 / 45; Incandescent Nova 50 → 52 / 55; Stellar Inferno 40 → 42 / 45.
Strongest fourth purchase: Solar Cataclysm + Sunward Oath (+5 Damage, +2% IDG, +2% DDG, +2% IDT, +2% DDT); Eternal Noon + Crown of Cinders (+2 Damage, +5% IDG, +5% IDT, +10% AB); Sovereign Sun + Dawnheart (+5% IDG, +2% DDG, +2% IDT, +10% DDT); Dying Light + Dawnheart (+2% IDG, +10% DDG, +7% IDT, +2% DDT).
Director review: Incandescent Nova 50 → 55 under the Burst route is flagged under BALANCE_REVIEW_METHOD.md; not retuned..

### Teno Yuki

*Fable proposal (2026-10-04 batch rebalance); not director-approved*

Foundations: **First Snow of Heaven** — How do I win offensively: sharpen my own strikes or expose them to everyone's?; **Vigil of Winter** — How do I win defensively: protect myself or suppress them?.
Advanced routes: **Reign of Absolute Zero** — burst: self-buff setup, controlled raw-Damage payoff; **Court of Splintered Ice** — exposure: party-wide area amplification; **Still Heart of Winter** — fortress: guard and mend on one cast; **Silence of Falling Snow** — suppression: blunt one enemy's blows for the whole party.
Changes: 02 Killing Frost: +2 Damage → +3% IDG; 03 Reign of Absolute Zero: +3 Damage → +2 Damage; 05 Court of Splintered Ice: +5% IDT, +3% IDG → +5% IDT; 10 Silence of Falling Snow: +5% DDG, +2% HEAL → +5% DDG.
Damage: Imperial Freeze 45 → 47; Ice Coffin 40 → 42; Ice Palace 40 → 42.
Strongest fourth purchase: Reign of Absolute Zero + Vigil of Winter (+2 Damage, +5% IDG, +2% DDG, +2% IDT, +2% DDT); Court of Splintered Ice + Vigil of Winter (+2% IDG, +2% DDG, +10% IDT, +2% DDT); Still Heart of Winter + First Snow of Heaven (+2% IDG, +2% DDG, +2% IDT, +10% DDT, +3% HEAL); Silence of Falling Snow + First Snow of Heaven (+2% IDG, +10% DDG, +2% IDT, +2% DDT).
Concerns: Silence of Falling Snow now carries one effect while Still Heart of Winter keeps a Heal rider; if a rider is wanted, +2% Decrease Damage Taken (the Arashima suppression pattern) fits, Heal does not. Exposure keeps +10% Increase Damage Taken on one area row; in group play it is the highest-leverage route in the tree.
Director review: none.

### Tenohira Musei

*Fable proposal (2026-10-04 batch rebalance); not director-approved*

Foundations: **Waxing Crescent** — How do I make my own strikes count for more: charge my hand or open them for the blow?; **Waning Crescent** — How do I turn Moonlit Inferno on them: blunt their strikes or bare them to every hit?.
Advanced routes: **Deafening Silence** — burst: exposure set up, controlled raw-Damage payoff on the cast itself; **Tipping the Balance** — sustained self amplification, solo and area; **Eclipse in Hand** — suppression; **Stillness Breaks** — exposure: one target bared to the whole party.
Changes: 02 Quiet Opening: renamed Unspoken Blow → Quiet Opening; +2 Damage → +3% IDT; 03 Deafening Silence: +3 Damage → +2 Damage; 10 Stillness Breaks: +5% IDT, +2 Damage → +4% IDT.
Damage: Silent Rift 40 → 42; Yin-Yang Cascade 40 → 42; Silent Palm Strike 40 → 42.
Strongest fourth purchase: Deafening Silence + Waning Crescent (+2 Damage, +3% IDG, +2% DDG, +5% IDT); Tipping the Balance + Waning Crescent (+10% IDG, +4% DDG, +2% IDT); Eclipse in Hand + Bared to the Moon (+2% IDG, +10% DDG, +5% IDT); Stillness Breaks + Waxing Crescent (+3% IDG, +2% DDG, +9% IDT).
Concerns: Stillness Breaks is +4% (Exposure +9%) so Exposure + Waxing Crescent does not out-damage Amplifier + Quiet Opening on a single target on top of its party reach; +5% (45%) restores the round number if the director prefers it. Deafening Silence is a lean payoff (+2 EP on three cooldown-7 attacks); +3 (40 → 43) would still cross no tier if the director wants a sharper burst. Quiet Opening puts an enemy debuff under the self-side Foundation as the Burst setup, which also lets Amplifier take exposure 38% as its fourth. Only Suppression is defensive; the kit's Defensive and Control rows cannot be reached by potency.
Director review: none.

### Terra Nova

*Fable proposal (2026-10-04 batch rebalance); not director-approved*

Foundations: **Fault Line** — How do I make my Earth strikes decide the exchange: hit harder, or leave the struck enemy weaker?; **Bedrock Stance** — How do I use Earth Wall's two rounds: hold behind it, or strike from it?.
Advanced routes: **Continental Rift** — burst: raw Damage on every Earth strike, no setup window; **Pressure of Ages** — suppression: the struck enemy hits softer for the whole party; **Unmoved Mountain** — fortress: take less from nearly every hit in the wall's window; **Landslide Momentum** — sustained amplification: Earth hits timed into the wall's window land hardest.
Changes: 02 Rending Strata: +2 Damage → +1 Damage; 03 Continental Rift: +3 Damage → +1 Damage; 05 Pressure of Ages: +5% DDG, +1 Damage → +5% DDG; 08 Unmoved Mountain: +5% DDT, +2% IDG → +5% DDT; 10 Landslide Momentum: +5% IDG, +2% DDT → +5% IDG.
Damage: Earthen Fortitude 38 → 39 / 40; Terra Spire 38 → 39 / 40.
Strongest fourth purchase: Continental Rift + Bedrock Stance (+2 Damage, +2% IDG, +2% DDG, +2% DDT); Pressure of Ages + Bedrock Stance (+2% IDG, +10% DDG, +2% DDT); Unmoved Mountain + Weight Behind the Blow (+5% IDG, +10% DDT); Landslide Momentum + Rampart Discipline (+10% IDG, +5% DDT).
Concerns: Off-kit flat Damage is unverified: Continental Rift's +2 reaches every Earth Damage row, so an off-kit Earth row at 50 would read 52; the validator checks kit rows only. Landslide Momentum's in-window lead over Burst plus Bedrock Stance is narrow on the kit's 38 EP attacks (55.1 against 54.8 EP-equivalent, about 0.5%) and widens with base (72.5 against 71.2 on a 50 row); Burst leads 40 to 38 outside the window. Not simulated. Burst is two +1 Damage steps (×1.026 each): its value is uptime, not size. Rending Strata keeps the +1 commit because every non-Damage alternative breaks the window split, the +10% Decrease Damage Given ceiling or Fault Line's sentence (design notes). Two of four routes (Pressure of Ages, Unmoved Mountain) amplify element-less rows that the current row-element resolver cannot reach; they depend on the proposed jutsu-classification resolver.
Director review: none.

### Tetsugan

*Fable proposal (2026-10-04 batch rebalance); not director-approved*

Foundations: **Eye of Iron** — How do I win offensively: sharpen my own strikes or brand the enemy?; **Tempered Stance** — How do I win defensively: endure the blow or send it back?.
Advanced routes: **One Cut Decides** — self-amplification: sharpen my own strikes; **Branding Iron** — attrition: brand the target so every hit burns; **Hammer and Anvil** — fortress: endure the blow; **Every Blow Returned** — retaliation: parry and send the blow back.
Changes: 01 Tempered Stance: +2% IDG, +2% DDT → +2% DDT, +2% DDG; 03 Hammer and Anvil: +5% DDT, +3% IDG → +3% DDT; 06 Eye of Iron: +2% IDT, +2% DDG → +2% IDT; 07 Honed Edge: +2 Damage → +3% IDG; 08 One Cut Decides: +3 Damage → +5% IDG.
Damage: no flat Damage.
Strongest fourth purchase: Hammer and Anvil + Eye of Iron (+2% DDG, +2% IDT, +8% DDT); Every Blow Returned + Folded Steel (+5% DDG, +5% DDT, +10% REF); One Cut Decides + Tempered Stance (+8% IDG, +2% DDG, +2% IDT, +2% DDT); Branding Iron + Tempered Stance (+2% DDG, +5% IDT, +2% DDT, +10% AB).
Concerns: One Cut Decides applies no coverage discount: +8% is Arashima's single-row value on three compounding rows (×1.19 against ×1.06–×1.11 for the protected self-amplification routes), offset only by the stances' two-round windows on cooldown 7 and Inner Peace's sword gate. Cutting it would also leave it behind Branding Iron; with the all-offence fourth purchases and every row up the two are level today (×1.27 against ×1.28). Hammer and Anvil's three-row case (×0.68) still exceeds Blood-Enchanted Eyes' two-row fortress; it needs both the sword and the staff, and simultaneous wield was not read at the pin (ENGINE_GAP_REGISTER G7). Every Blow Returned's suppression trims its own Reflect (×1.07 under both suppression rows, ×0.99 with Folded Steel and a stance up): the retaliation route leans defensive rather than returning much more damage. The seven Metal strikes are unamplified: no node targets Damage, because every flat point lifts Phantom Slash past the 50 Nuke tier.
Director review: Two stance-kit magnitudes need the director, because three compounding rows make them the largest gains among the protected references. (1) One Cut Decides: +8% Increase Damage Given gives ×1.19 with both stances (×1.12 in Inner Peace alone), above Blood-Enchanted Eyes' Feast of the Fallen ×1.11, Shakunetsu Sakura ×1.07/×1.10 and Arashima ×1.06/×1.07; +5% (Honed Edge +2%, One Cut Decides +3%) would give ×1.12. (2) Hammer and Anvil, cut to +8% Decrease Damage Taken: both stances ×0.77 against Blood-Enchanted Eyes' Deathless Vitality ×0.75, but all three rows (sword, staff and a third cast) reach ×0.68..

### Vaporia

*Fable proposal (2026-10-04 batch rebalance); not director-approved*

Foundations: **Rising Steam** — How do I make the rush hit harder: scald everyone around me or brand one target?; **Vapor Shroud** — How do I outlast the exchange: heal through my own hits or punish theirs?.
Advanced routes: **Caldera Burst** — area burst: spiral exposure set up, controlled +2 Damage payoff; **Boiling Point** — branded-target attrition (Afterburn); **Dew of the Dragon** — sustain (Lifesteal with a palm Heal rider); **Wall of Steam** — retaliation fortress (Reflect behind Decrease Damage Taken).
Changes: 02 Geyser Fist: +2 Damage → +3% IDT; 03 Caldera Burst: +3 Damage → +2 Damage; 05 Boiling Point: +7% AB, +3% IDT, +3% IDG → +7% AB; 06 Vapor Shroud: +2% DDT, +2% HEAL → +2% DDT.
Damage: Drowning Strike 40 → 42; Surfing Strike 45 → 47; Scorch Break 40 → 42.
Strongest fourth purchase: Caldera Burst + Blistering Mist (+2 Damage, +2% IDG, +5% IDT, +3% AB); Boiling Point + Geyser Fist (+2% IDG, +5% IDT, +10% AB); Dew of the Dragon + Rising Steam (+2% IDG, +2% IDT, +2% DDT, +5% LS, +5% HEAL); Wall of Steam + Rising Steam (+2% IDG, +2% IDT, +5% DDT, +10% REF).
Concerns: Geyser Fist raises Drowning Strike's ally-hazard exposure to 40% on everyone standing in the spiral, allies and a caster who steps onto it included. Burn and Sustain both deepen the one Liquid Ember Shell cast; their realized value depends on sequencing and was not simulated.
Director review: none.

### Voltara Divine

*Fable proposal (2026-10-04 batch rebalance); not director-approved*

Foundations: **Anointed by Lightning** — How do I keep the storm's blessing on every blow?; **Halo of Static** — How do I hold my ground once the blitz carries me in?.
Advanced routes: **Apotheosis of Thunder** — sustained amplification: both self buffs at 45%, every hit in the windows; **Unassailable Radiance** — fortress: Blitz guard at 40%, the kit's only defence.
Changes: 02 Dragon's Whispered Wrath: removed; 03 Ethereal Dragon Unbound: removed; 05 Apotheosis of Thunder: +5% IDG, +2% DDT → +5% IDG; 08 Unassailable Radiance: +5% DDT, +1 Damage → +5% DDT; 09 Heaven's Retort: removed.
Damage: no flat Damage.
Strongest fourth purchase: Apotheosis of Thunder + Halo of Static (+10% IDG, +2% DDT); Unassailable Radiance + Anointed by Lightning (+2% IDG, +10% DDT).
Concerns: Apotheosis of Thunder is the tree's only offensive route and its highest-leverage one; it keeps +10% for the reasons in the design notes, and a +2/+3/+4 cut (+9%) is the trim if the director wants one. Both Foundations are in every legal full build (two 3-node chains); the choice is which chain to finish, or the no-capstone hybrid. Damage is left unamplified: the strike pair is primed only through the buff rows, and any flat Damage would lift Whispers 50 past the Nuke tier.
Director review: Structural: the flat-Damage route is removed rather than kept at Whispers 50 → 52, because with names hidden it read as the amplification route with +5% Increase Damage Given swapped for +2 Damage (about 2% on the strike pair). The tree shrinks to two 3-node chains (6 nodes, two Advanced Arts) with both Foundations universal, and no Damage row changes. Confirm the two-route tree..

### Yaketsuku Netsu

*Fable proposal (2026-10-04 batch rebalance); not director-approved*

Foundations: **Heat in the Steel** — How do I make my own strikes land harder: open the target for my blade, or run my blade hotter?; **Blistered Guard** — How do I open the target for everyone who hits it?.
Advanced routes: **Blade That Never Cools** — burst: exposure set up, controlled raw-Damage payoff on both attacks; **White-Hot Blood** — sustained self amplification: the heat window lifts every hit I land; **Nothing Left Forbidden** — team exposure: the opened target takes more from every attacker.
Changes: 02 Searing Edge: +2 Damage → +3% IDT; 03 Blade That Never Cools: +3 Damage → +2 Damage; 08 Nothing Left Forbidden: +5% IDT, +1 Damage → +5% IDT.
Damage: Forgotten Ember Blade 40 → 42; Forbidden Chakra Fury 40 → 42.
Strongest fourth purchase: Blade That Never Cools + Fever Pitch (+2 Damage, +5% IDG, +3% IDT); White-Hot Blood + Searing Edge (+10% IDG, +3% IDT); Nothing Left Forbidden + Heat in the Steel (+2% IDG, +10% IDT).
Concerns: Heat in the Steel stays in every legal full build (narrow-kit exception carried forward): the kit has no fourth tag for a leaf under Blistered Guard that would not blur or twin a route. Exposure leverage: on a hit landed in both windows the three full packages sit within ×1.80–×1.86, but Nothing Left Forbidden also lifts every ally hit on the target by ×1.40, so it is the strongest route in a party. Party value was not simulated. The Heat route's best fourth is its sibling Searing Edge (exposure 33%), one point over Blistered Guard (32%), so Heat + Blistered Guard is numerically dominated. Accepted to keep the 2/3/5 exposure chain unchanged. Every amplified row depends on the proposed Yaketsuku Netsu classification extension and the jutsu-classification resolver (G1); none carries an element today.
Director review: none.

