# AP1 live test 2: step 10 report (2026-11-12)

Frozen SHA 06358ca539372cae12d41b086a465719f403aba7 (fable/ai-player-ap1), checkout /home/claude/tnr-tools detached at that SHA. Nothing under player/ changed and nothing was pushed to fable/*.

## Result
9 fights across two runs: 8 won, 1 lost. 0 missed turns, 0 "Too Many Requests".

## Times (UTC)
- Run 1: 16:02:56 to 16:09:07. Ended on the director's word to restock and restart.
- Run 2: 16:18:46 to 17:26:31; hunt 16:19:35 to 17:22:18 (the hour ran out mid-fight 8, guard set after it ended); step 7 swap 17:24:37 to 17:25:45; asleep at sector 177 at 17:26:31.
- Restock between runs (director's yes): consumables to 100, 50 Dr. Kim's Miracle Potion, Elemental kunai in the thrown slot. The shop charged half its listed price on several items (Kim's 75k vs 150k listed, Smoke 25k vs 50k, Panacea 27.5k vs 55k, Full Potion 2k vs 10k, Chakra Pill 500 vs 1k).

## Fights
| # | Battle | Opponent | Result | Rounds | AP1 turns | Actions sent / accepted | Unseen > 20 s |
|---|---|---|---|---|---|---|---|
| R1-1 | BBd4YBPWrOrEj6Huxc-SW | Charon | won | 3 | 3 | 6 / 5 | none |
| 1 | BRDTs8o6wYkhX3cnj_le4 | Luka | won | 3 | 3 | 6 / 6 | R1 44.7 s |
| 2 | d9mEPhdio4ozIgIHy13qW | Laser | won | 2 | 2 | 4 / 4 | none |
| 3 | QC0alLwyLdFPiXtaCwWnh | Lokananta | won | 2 | 2 | 4 / 4 | none |
| 4 | yz3QvaKW5nbB9FRjjdVcq | Blackwing14 | won | 3 | 3 | 6 / 6 | none |
| 5 | fm1Ie6TRDPfhCHu1c5o3Z | 4qua | won | 5 | 5 | 13 / 13 | none |
| 6 | nnx6eUzQ7b6DYQcz2mrK6 | Luka | lost | 5 | 3 (R1, R2, R5) | 7 / 7 AP1 rounds | R5 22.5 s |
| 7 | Q0A4r_zFQaq79bk76Bs0m | lipan | won | 3 | 3 | 7 / 6 | none |
| 8 | PeMlBzyklGB6maKaWT0Zs | lipan | won | 7 | 7 | 17 / 17 | R5 22.8 s |

- Fight 6: the director played R3 and R4 by hand. The brain's 3 actions in R3 were refused ("Battle state changed") and its 2 in R4 ("Not your turn. Wait for Luka"). Those rounds are excluded from AP1 stats.
- Missed or unresolved turns: 0. fired_after over 20 s: none (all under 2 s).
- Full Potion used at the end of 4 fights (4555, 47, 4569 and 943 HP).

## Relays
23 relays (Haiku, RELAY.md prompt): run 1 relays 1 to 4, run 2 relays 5 to 23. Each was born fresh with the RELAY.md text.
- Most ended on the brain's "STOP rotate" after a fight or a long roam.
- Relay 2 (run 1) and relay 6 (run 2, Luka R1, waiting as P2 after 4 identical polls) quit on their own mid-fight with text. Each left a budget hold (3b9910-20, b5b256-17) that I released with `stopped`.
- Relay 5 was a dry start. Relay 22 ended "STOP superseded" during the swap, as expected; relay 23 ended "STOP session ended".

## Batches and tokens (tokens.jsonl)
- Run 1: 32 batches, 76 calls, 6,056,483 in, 24,079 out.
- Run 2: 323 batches, 870 calls, 104,544,311 in, 254,797 out.
- Fight batches: 167, 62.4M in, 146.5k out, about 1.9M in and 4.4k out per fight turn (33 turns).

## Findings (counts, both runs)
- Relay stall in a fight: 16 s x4, 18 s x1, 19 s x4.
- Battle read came back without the battle: 6.
- Fight unread before the turn was seen: 45 s (R1), 22 s, 23 s (both R5).
- Refusals: "Battle state changed" x3 (one a wait), "Captain's Decree no longer possible" x2, "Not your turn" x1.
- Budget holds after a relay quit: 2, both released.
- No-target stretch 16:47 to 17:01 roaming sectors 1335, 99, 1538, 1490.

## Departures from the brief
1. After relay 6 quit, I added one rule to the relay prompt: identical read-only batches are normal while the other player moves; never stop on your own, only a STOP line ends you. No relay quit after that.
2. Two runs instead of one, on the director's word (end, restock, restart).
3. The director played fight 6 R3 and R4 by hand.
4. Transcripts: besides scrubbing emails, I removed the harness context entries (system prompt snapshots, memory, skill listing, session context) because they carried personal context unrelated to the relay. The relay's own turns are complete. The 2026-11-11 AP1 relay transcripts were not at sessions/ap1_live/transcripts/; I added copies from my own session under transcripts/2026-11-11/.
5. After the session ended I banked pocket ryo down to 150k (director's rule below).

## Gap for Fable: pocket money
The brain carries all pocket ryo while roaming. After the restock about 9.8M was left in pocket and 2.9M was stolen during run 2. The director's rule: keep only 100k to 200k in pocket for hospital bills and ramen when out; bank or spend the rest. The brain did not bank on its own at any point.

## Evidence
Branch duet/ai-player-ap1-live2. Run 1 and run 2 live files (no locks, inbox or outbox), step 7 status copies, 23 + 3 relay transcripts, and the fight files the brain wrote. check_no_real_name.py and check_large_files.py both exit 0.
