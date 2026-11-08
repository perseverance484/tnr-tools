# push/531 Mother of Echoes tuning: results (2026-11-08, Duet)

7/7 sent and read back (profile.getAi after each write).

| AI | HP | Damage given | Damage taken | Jutsu equipped |
|---|---|---|---|---|
| Sayo, Mother of Echoes (act 1) fJLcH1mpB1XHHGtNWwvzD | 6,060 (x1.2, was 10,100) | +200% | none (was -15%) | 13/13 |
| The Silence IhNR-W1FElTsrWw1KfuQ9 | 5,050 | +30% | none (was -25%) | 8/8 |
| Sayo, Glasswright (act 2) H3pNj2qUWpMpVRINiH6Vn | 20,200 (x4, was 60,600) | +27% (was +227%) | -35% (was -59%) | 23/23 |
| Sayo, Saint of Stillness (act 3) k0hgSrghl_KcYs9ATVDJT | 20,200 (x4, was 60,600) | +41% (was +241%) | -30% (was -25%) | 25/25 |
| The Gate Porter (Worn) wivZbMygCZo6c9pRKWvCI | 5,050 | +50% (was +350%) | - | 1/1 |
| Sister Hana (Worn) g6bNcftMcQ9pV_nMki7Wv | 5,050 | +50% (was +350%) | - | 1/1 |
| Cadet Tomo (Worn) KhFglnxE7ouIDywet3BPB | 5,050 | +50% (was +350%) | - | 1/1 |

Runner note: mcp_run sent the full AI row with date strings, which profile.updateAi rejects over the
connector ("expected date"), and the transcript answerer took a "persisted-output" 2 KB preview as a
complete getAi answer. The run was stopped before any write built from that preview; the edits were sent
by hand from fresh full reads with the 11 date fields dropped (same shape as the successful 512 writes).

## Follow-up the same day (531b)

First rerun (battle A-58lsyF7H7ciZZvBvV8J) showed The Silence casting The Hush, Unbridled and The Listening,
Unbridled from round 1. Her rules gate those on `target_has_effect HIGHEST_MAX_HEALTH_ALLY sealprevent`; with
Sayo at 5,050 she tied the Silence (5,050, who always carries sealprevent), so the Silence picked herself.
Sayo set to poolsMultiplier 1.2 (6,060 HP); fractional multipliers persist (read back 1.2 / 6,060, 13/13 jutsu).
dauntless then died R5 to the one-hit-kill roll on Far Refraction Breaks while a Feeler's Grasp held him on
the line (getBattleEntries: "dauntless was killed in one hit" at 5,686 HP).
