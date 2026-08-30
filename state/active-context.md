<!-- PROJECTION of state/digest.json - edit the digest, run session_close.py; never edit this file -->
# active-context.md - read this first, then the board

**State in one line:** Backgrounds wave CLOSED end-to-end: eight scene backgrounds generated/QC'd/approved, sheet posted, shipped via push/21 as ONE pack (8 asset creates + 10 mission wiring, picker-free, single press) - 18 ok / 0 fail, postflight match 18 diff 0, every @scene ref resolved. Full node-by-node sweep of all 272 dialog nodes across ten missions: 144 rewritten (112 onto new plates, 32 generic mismatch repairs approved), 27 control nodes left empty by design. Board corrected: the wedge and push/6 RETIRED as never-real (our own rate limiter, since patched), Zod editor-page crash retired with them. Lane ARTWORK ONLY; publish gate: content admin; everything hidden:true.

**Verified at close (exact runs):**
- lawmap -> 93 laws, 93 matrix rows, 77 citations across 34 files; 0 errors, 5 warnings
- doctrine projections -> all projections current (exit 0)
- packs/TOCs -> all packs and TOCs current (exit 0)
- validate.py push/21 manifest -> 0 errors, 73 warnings (all law-49 snapshot-only, on sceneCharacters fields never touched; every flagged id resolves live in the capture)
- harvest.py verify tnr_results_1788128500937.json -> builder v4.29: 18 ok, 0 fail, 0 unverified, 0 skipped -> verified
- diff of every quest edit against the capture -> nothing changed outside sceneBackground; 299 sceneCharacters preserved byte-identical

**Start ritual:** per the mounted instructions - clone, repo-local identity,
session_open.py (verify any new inbox bundle FIRST). No clone means no state.

**In progress:** wave: Backgrounds wave CLOSED. Next wave: LISTING ICONS (10, one per mission) on the wave_workflow loop. RULED: dedicated icon per mission; STYLE CALL STILL OPEN - pin house-style family vs per-mission vignette. Field is quest.image, a RAW URL like pins (@img: resolves direct, no gameAsset record), STATIC target, 1:1.

**Open items, by owner:**
- dauntless: re-paste mounted from state/mounted_instructions.txt (stamp @17d6a71+06335a4); reinstall build skill from dist after skillpack rebuild (doctrine block + stack row changed); refresh ViolentMonkey (panel title v4.31; bundles still stamp v4.29)

**Rulings open:** - laws 18/61 reclass knowledge->validate(partial); laws 16d/37/69 annotate-or-reclass
- WO-08 answers sharding: defer/skip (clone-first ritual makes two-fetch moot; scripts grep locally, tokens paid on hits only; keep hot.json) - or proceed as planned?
- art micro-rulings: g30/g36/x1 silent-portrait per node; x22-x28 speaker handler vs village official; handler pronouns

**Next:** Open on the icons wave: settle the style call (pin family vs per-mission vignette) FIRST, then thread init + first card. Carry forward from backgrounds: BRIGHTNESS CAP clause in-card from card 1, style reference attached at thread init, vernacular named explicitly (generic vocabulary read as western barn). Owed (dauntless): VM refresh to v4.31 (bundles still stamp v4.29), e16 pronoun sweep, publish flip decision rides content admin. Owed (Claude): law-94 authoring via law process; rawqc/artpreflight background-target fix (held, see art_backlog queued tool fix) - do it BEFORE the icons wave, icons hit the same filename-inference path.

Container quirks and cross-cutting laws live in the mounted instructions.
