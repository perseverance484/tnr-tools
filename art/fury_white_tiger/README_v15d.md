# Fury of The White Tiger v15d: upload package (prepared 2026-11-09, nothing uploaded, created or submitted)

dauntless approved the look of v15d ("Looks right", Nov 9 18:48Z). That approves the look only. Every step below waits for his own go.

## Art (112 px frames, alpha pre-compensated where the engine stacks appear clips twice)
| file | frames | ms/frame | KB | slot on jutsu QXE9J0fnu1t-DAGTGbaCX |
|---|---|---|---|---|
| anim_tiger_fury_v15d_target_damage.webp | 36 | 50 | 242 | damage.appearAnimation (replaces stock re4P1TqEXbfs5rCZOz67m; hit sound yGzPWg1cLQc6dYd1EpCsl stays) |
| anim_tiger_fury_v15d_caster_afterburn.webp | 36 | 60 | 78 | afterburn.appearAnimation (empty today) |
| anim_tiger_fury_v15d_caster_buff.webp | 16 | 70 | 8 | increasedamagegiven.staticAnimation (replaces stock 1HQecvAYR-TkK11ELt7HM) |
No staticAssetPath on any effect. Stun keeps no visuals. Text, numbers and targeting unchanged.

sha256:
- b0af05effbee2638cde94e9ebedd0b5ab035607a225e9c4db21032b8add31f77 caster_afterburn
- e5fc38eaf2b23bead59a2b4b4414c09b59d80dc59062ab36d8bc5b01f9dde851 caster_buff
- d69d9e2c4ee47764f945986639a4b7f202dc7e798e7cea55c120cb304727ab45 target_damage

## Steps (same route as the DKI v7b smoulder, Nov 9)
1. Commit art to tnr-tools main (art/fury_white_tiger/exports/v15d).
2. Upload the 3 strips through duet/moe-uploadthing (run.txt "go"), read uploaded.json.
3. Create 3 ANIMATION assets hidden, set image (literal ufs.sh URL), frames, speed; read back; unhide (hidden assets don't play).
4. Either (a) review desk ticket: fill the 3 ids into tiger_v15d_ticket_DRAFT.json, re-read the live jutsu first (live_jutsu_2026-11-09.json is the capture this draft was built from), contentReview.create, read back PENDING, never approve ourselves; or (b) direct jutsu edit of the 3 slots only, read back.
5. Bundle + commit; release the run lock.

## Checks run
- overlap.py (burst, both stacked plays) 0 px on the body; overlap_loop.py (sparks, every frame x cast 4-6 + every idle frame, both facings) 0 px.
- Board sim previews in preview/. Battle lighting not simulated.
- Draft diff vs live: exactly the 3 slots above.
