# Weapon effect-target audit (2026-11-26)

Scope: every weapon item, 95 visible + 56 hidden, read live through item.getAll. Each effect's receiver
(INHERIT = the item's target, SELF = the user) checked against the tag's polarity in docs/combat-engine/tags/*.yaml.

## Wrong (fixed in push/631)
| Weapon | Tag | Live | Fix | Why |
|---|---|---|---|---|
| Gale Fans | afterburn 10% 2r | SELF | INHERIT | debuff on the holder: the user was taking it |
| Soul Harvester | lifesteal 20% 2r | INHERIT | SELF | buff on the attacker: the enemy was healing off its hits |
| Flaming Sword | increasedamagegiven 10% 2r | INHERIT | SELF | buff: the enemy got +10% damage |
| Warden's Bracers | reflect 15% 2r | INHERIT | SELF | buff on the defender: the enemy was reflecting the user's hits |

## Checked and left alone
- Kuzenbo's Club: immunity (blocks debuffprevent) on the enemy. Looks deliberate: it stops the enemy shielding
  against debuffs for 2 rounds. Night's Testament and Skyglass Katana carry the mirror case (immunity to
  buffprevent on SELF). Flip only if it was meant as a self buff.
- Veilbreaker's Edge: recoil 10% on the enemy (they take back part of what they deal). Correct as a debuff.
- Ryo Distraction: flee on SELF by design (the item targets SELF).
- Ink of the Void: vamp on SELF; the engine reads vamp from the casting action with no target check, and most
  vamp jutsu use SELF.
- Every other weapon: buffs on SELF, debuffs on the enemy. Hidden weapons all clean.

## Manifest notes
- Effects re-sent verbatim from the live read with only the one target changed; craftingRequirements carried
  (Soul Harvester and Warden's Bracers have recipes; Gale Fans and Flaming Sword send []).
- validate.py errors on this manifest are all pre-existing live fields (direction, description, animationScale,
  animationOffsetY) the bundled schema does not list, and law 4 statTypes absent on the damage/pierce effects,
  which is how these weapons are live today. Nothing in the payload differs from live except the four targets.
