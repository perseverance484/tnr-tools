# Crownhold build

Generator: `push/crownhold.gen.py` (source: `package/`, the approved Silent Bastion design from
`claude/silent-bastion-authoring-69za5u@6271e1f`). Fresh reads: `source_check_2026-10-25.md`.

| Step | Manifest | Status |
|---|---|---|
| 1 | push/271: The Last Directive, Extermination Order, Countermand | ready (exception RUL-2026-10-25-013) |
| 2 | push/272: the 20 AIs | written once `ids.json` has push/271's three ids (law 17) |
| 3 | Crownbreaker badge | made by hand in the game editor (Forge has no badge recipe); id goes in `ids.json` as `badge:crownbreaker` |
| 4 | push/273: the quest | `quest.preview.json` now; final once `ids.json` has the 20 AI ids (`@ai:<slot>`) and the badge |

`ids.json` keys: `@jutsu:last_directive`, `@jutsu:extermination_order`, `@item:countermand`, `@ai:D2.BOSS` ... `@ai:D5.REG4`,
`badge:crownbreaker`.

Quest (preview, 76 objectives): the package's `alt99_f4gate` graph without its recovery lane (RUL-2026-10-25-010: a lost
fight fails the run; Arakane's loss keeps its own fail text), plus one beat per wrong puzzle answer (a menu may not send
two options to one node) and the shared fail node. 16 to 20 fights per run. Medical = `givePools: 100`; Security Alert
= +10% damage taken 2r; Combat Protocols as approved (stun prevent, +25% damage given, seal prevent, debuff prevent).
Ending: ladder VI (5,000 exp, Sealed Treasury 6%). Pick 1: Skyglass Coffer x2 / Crownhold's Honor (1,000 village
tokens, PROPOSAL) / Crownbreaker badge / Lastlight jutsu. Entry: Lastlight Lantern. Prose: "Silent Bastion" is now
Crownhold, the Bastion Proving Proctor is the Crownhold Proving Proctor, and Arakane's intros and the aftermath carry
the Command Crown (RUL-2026-10-25-011). Scenes borrow the Skyglass set until Crownhold's six are drawn.
