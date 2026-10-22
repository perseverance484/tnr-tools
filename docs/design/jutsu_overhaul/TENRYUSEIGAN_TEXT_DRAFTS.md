# Tenryūseigan jutsu: names, icons and text (drafts)

- **Bloodline:** Tenryūseigan (`ieDD4S_zzLMmVadUuD69s`, H rank, hidden), a renamed copy of Ethereal Monarch's kit.
- **Icons:** `art/jutsu_icons/tenryuseigan/exports/` (director-supplied 2026-10-22, preflight clean).
- **Status:** DRAFT. The mapping is proposed except Celestial Bind (director: "Celestial Bind -> Celestial
  Sealing"). Text is written from the Ethereal Monarch records (bundle `tnr_results_1792212938515.json`,
  2026-10-17) and must be checked against the live Tenryūseigan copies from push/206 before any ticket.
  Names, final prose and acceptance are the director's (CLAUDE.md section 10).
- **Style:** `WRITING_STYLE.md`; signature bloodline jutsu, so battle lines get two sentences.

## Mapping

| Icon / new name | Ethereal Monarch jutsu | Why | Confidence |
|---|---|---|---|
| Celestial Bind | Celestial Sealing | director | given |
| Heavenly Barrier | Heavenly Constructs | dome = self shield (reflect, debuff immunity) | high |
| Dragon Eye Awakening | Starlight Veil | self power-up (damage up, damage down) | high |
| Storm Dragon | Founder's Wrath | the only area attack; a storm crashing down | high |
| Void Gaze | Stardust | debuff on the target (takes more damage, afterburn) | medium |
| Skyfang Burst | Tamashī no Sakeme | single burst of damage | medium |

## Drafts

### Celestial Bind (Celestial Sealing)
Effects: Yin-Yang damage; bloodline seal (90, grows to 100) 2 rounds; user damage given +25% 2 rounds.

- **Description:** A celestial dragon coils around the target in chains of starlight, striking deep and sealing away their bloodline. With their prey bound, the user's attacks hit harder for a short time.
- **Battle:** %user's eyes blaze with starlight as a celestial dragon unfurls from the heavens and coils around %target, its golden chains biting into flesh and chakra alike. With a final turn of the coils, the dragon seals %target's bloodline away.

### Heavenly Barrier (Heavenly Constructs)
Effects (self): debuff immunity 2 rounds; reflect 30% 2 rounds; injects a jutsu 2 rounds (in Ethereal Monarch, Stardust; to confirm on the copy).

- **Description:** The user seals themselves inside a dome of golden lattice and starlight that throws part of every blow back at its attacker. While it stands, no weakening effect can reach them, and Void Gaze opens to them for a short time.
- **Battle:** %user spreads their hands and the heavens answer, a dome of gold-ribbed starlight slamming down around them as storm clouds roil at its edges. Every strike that meets the barrier rings off it and rebounds on whoever threw it.

### Dragon Eye Awakening (Starlight Veil)
Effects (self): damage taken -25%, damage given +25%, 2 rounds; buffs cannot be cleared 1 round.

- **Description:** The user awakens the dragon's eye, and crimson starlight floods their body, making their attacks hit harder and the blows against them land softer. For a short time, no technique can strip this power away.
- **Battle:** %user's eyes split into blazing dragon pupils, and the shadow of a great serpent coils around them in a storm of crimson starlight. The awakened dragon gazes out through %user, and the whole battlefield feels its weight.

### Storm Dragon (Founder's Wrath)
Effects: area (circle) Yin-Yang pierce, enemies only; user damage taken -20% 2 rounds.

- **Description:** The user calls a storm dragon down from the heavens, its coiling body crashing into the area and piercing straight through any defense. Wrapped in its thunderheads, the user takes less damage for a short time.
- **Battle:** %user raises a hand to the darkening sky and a storm dragon descends, its coils churning the clouds into a golden-veined vortex. It crashes onto the battlefield in a torrent of light that tears through everything in its path.

### Void Gaze (Stardust)
Effects: user damage given +35%; target damage taken +35% and afterburn 30%; all 2 rounds.

- **Description:** The user drags the target's gaze into a spiraling black star, leaving them open to every strike and burning with each blow they take. Feeding on the void, the user's attacks hit harder for a short time.
- **Battle:** %user's eyes go black as a spiraling void tears open behind %target, its rim blazing violet and crimson. %target is dragged into the abyss's gaze, every defense unraveling as the dark stars begin to burn.

### Skyfang Burst (Tamashī no Sakeme)
Effects: Yin-Yang damage; `consume` 20% 1 round on INHERIT (see flag).

- **Description:** The user unleashes a roaring sky dragon of ink and starlight whose fangs tear through the target's body and spirit alike. Part of the damage it deals hardens into a shield around the user for a short time.
- **Battle:** %user bares their teeth as the spirit of a sky dragon tears free from their chakra, its jaws blazing crimson and gold. It lunges across the battlefield and its fangs rip into %target, rending flesh and soul in a single burst.

## Flags (mechanics, director's call)

1. **Tamashī no Sakeme's `consume` sits on the target.** `consume` turns a share of the damage its holder
   deals into shields on the holder (TheNinjaRPG@a744c04, `validators/combat.ts` ConsumeTag). On Ethereal
   Monarch it targets INHERIT, so the enemy hit gets the shield effect, not the caster. If the Tenryūseigan
   copy is the same, the description's second sentence is wrong and should be dropped, or the effect
   moved to SELF.
2. **Heavenly Constructs' injected jutsu.** The text names Void Gaze on the assumption that the copy injects
   Tenryūseigan's own Stardust copy; push/206 shows what it actually injects.
