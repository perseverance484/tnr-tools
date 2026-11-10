# Target cooldowns (director rule, 2026-11-09)

"Dont pick on the same person too much. After 1 fight, put them on CD for 5 minutes. Add an additional 5 for each
time you fight them consecutively in a day. Them attacking back resets this."

- After a fight that I started, the target is off-limits for 5 minutes x (number of consecutive fights I started
  against them today).
- If they attack me, their count resets to 0.
- Check this file before every `combat.attackUser`, along with `do_not_attack.md`.

| Player | Fights I started today (consecutive) | Last fight ended (UTC) | Off-limits until (UTC) |
|---|---|---|---|
| Thronaris | 2 (2026-11-10 02:44, 03:53) | 04:01 | 04:11 |
| Arashii | 1 | 03:34 | 03:39 (expired) |
| IndraUchiha | 1 | 03:13 | 03:18 (expired) |

(Korin attacked me at 02:49: no cooldown from that fight.)
