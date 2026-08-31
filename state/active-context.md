<!-- PROJECTION of state/digest.json - edit the digest, run session_close.py; never edit this file -->
# active-context.md - read this first, then the board

**State in one line:** ICONS WAVE CLOSED on art: four shared quest-rank icons (D/C/B/A) generated, graded and banked - all four rawqc ACCEPT on listing_icon_framed. Design pivoted mid-wave from dedicated-icon-per-mission to ONE SHARED ICON PER RANK (dauntless): fewer generations, reads at a glance, future quests wire an existing icon with no art work. Rank is carried by the frame finish - bare wood D, red urushi lacquer C, black lacquer + mother-of-pearl inlay B, black lacquer + worn gold leaf A - over a shared interior (overhead mission brief, hanko seal in cinnabar, rank letter in the seal). The rank set REPLACES existing per-mission icons; migration list beyond the twelve not yet enumerated. NOT SHIPPED: no upload, no wiring, no push this session. Lane ARTWORK ONLY; publish gate content admin; everything hidden:true.

**Verified at close (exact runs):**
- lawmap -> 93 laws, 93 matrix rows, 77 citations across 34 files; 0 errors, 5 warnings
- doctrine projections -> all projections current (exit 0)
- packs/TOCs -> all packs and TOCs current (exit 0)
- parity tnr_results_1788128500937.json -> 0 errors, 0 warnings

**Start ritual:** per the mounted instructions - clone, repo-local identity,
session_open.py (verify any new inbox bundle FIRST). No clone means no state.

**In progress:** wave: wave: ICONS. Art complete, shipping not started. Two methods were built and both are banked. (1) COMPOSITE plates in data/frames/ - the live D-rank border was proven composited (per-pixel std 3.8 in the band vs 40.4 interior across nine live icons), so the wood plate was extracted from their median and three lacquer plates keyed and masked to its alpha. (2) FULLY GENERATED icons in data/rank_icons/ - RULED to supersede (1) for the rank set after the first full gen came back with correct frame geometry AND a crisp letter. Claude argued against generating frames and letters and was wrong on the evidence; the reference image did the constraining, so fresh prompts without it should NOT be expected to behave the same. C/B/A each generated from TWO references: the finished D plus that rank's flattened plate. Grade of record: gamma 0.88 applied post-gen, identical across all four. B's inlay overshoots (frame-band bright 0.079 vs A's 0.036) - LEFT AS IS by ruling. Discord status post written and handed over with contact sheet.

**Open items, by owner:**
- dauntless: VM refresh to v4.31 (bundles still stamp v4.29); e16 pronoun sweep (prose, not Claude's lane); publish flip rides content admin; everything hidden:true; enumerate which existing per-mission icons migrate to the rank set
- claude: law-94 authoring via the law process; rawqc --frame path: a keyed plate runs to the image edge, so RING rejects every one at 100% dirty-ring; all plates hand-verified on aspect/coverage instead; port the frame compositing pipeline to stdlib - it ran ad hoc on PIL/numpy and the toolchain is stdlib-only

**Rulings open:** - laws 18/61 reclass knowledge->validate(partial); laws 16d/37/69 annotate-or-reclass
- WO-08 answers sharding: defer/skip (clone-first ritual makes two-fetch moot; scripts grep locally, tokens paid on hits only; keep hot.json) - or proceed as planned?
- art micro-rulings: g30/g36/x1 silent-portrait per node; x22-x28 speaker handler vs village official; handler pronouns

**Next:** Ship the icons: enumerate the FULL migration list from a live capture (the twelve in scope plus every existing per-mission icon being replaced), upload four raw URLs, wire quest.image by rank, verify by read-back per-entry json.success. Twelve in scope: C x4 Chalk and Corner / The Empty Contract / Protection / The Waystation; B x4 Nothing to Report / The Loud Way / Copies Not Thefts (d-94cxrGW91o1SJCr9rsq) / Witness Detail (dfeXwdrnvyvGGETiCMgu-); A x4 Three Rounds / The Long Winter / Old Ghost / The Tenth Name. Owed (dauntless): VM refresh to v4.31 (bundles still stamp v4.29), e16 pronoun sweep, publish flip rides content admin. Owed (Claude): law-94 authoring via law process; rawqc needs a --frame path (a keyed plate runs to the edge, so RING rejects every one at 100% dirty-ring - all plates hand-verified on aspect/coverage instead); port the frame compositing pipeline to stdlib (it ran ad hoc on PIL/numpy, toolchain is stdlib-only). DONE this session: rawqc --opaque path + measured exposure_bands, artpreflight bg_ inference.

Container quirks and cross-cutting laws live in the mounted instructions.

## Icons wave - shipping (handed over 2026-08-30)

- `push/22_rank_icon_wiring_wave1.zip` - 10 quest edits (C x4, B x2, A x4, ranks read live from
  `tnr_results_1788127352899.json`), each setting only `image` to `@img:icon_rank_<R>.webp`. The three icons ride
  the zip with a byte ledger, so the builder uploads them and no raw URL is passed by hand. Generator:
  `push/22_rank_icon_wiring_wave1.gen.py` (ids extracted, never transcribed). validate.py: 0 errors.
- `capture.before` reads 21 quests whose rank is unread: the ten D-set missions, Case Contract x4,
  Blacksteel Contract x5, Copies Not Thefts, Witness Detail. Wave 2 wires them from that capture.
- Delete list so far: the ten `dmissionicons` gameAssets (ids in the wave-1 handover). Case/Blacksteel icons
  are NOT deletable - reused by Genin Trials. Copies/Witness icon ids pending the capture.
- validate.py now warns instead of erroring on a quest edit that carries no `content` (fetch-merge patch).

## Hide-wave scope (requested 2026-08-30, not built)

- Ours = the 31 authored missions (12 Forsworn C/B/A, 10 D-set, Case Contract x4, Blacksteel Contract x5).
- Everything else that is a mission gets `hidden: true`, earmarked for upgrade or retirement.
- HAZARDS to settle before any hide manifest is built:
  1. `hidden` fails eligibility EVERYWHERE for non-staff (quest.md 398/409), including a granted ACTIVE quest,
     which is silently dropped on the next touch. Players mid-mission lose it.
  2. Our 31 are all still `hidden: true`. Hiding the rest before ours publish leaves the mission hall thin or
     empty in some level windows, and the random mission generators draw from the same pool.
  3. Scale: ~380 non-ours missions. Classification must come from a live census, not from names.
- push 22 carries two `quests.getAll` shape probes (limit 25) to size the census before pulling 500 fat rows
  through a mobile browser and the sync token.

## Order of operations (ruled 2026-08-30)

1. `push/23_our_missions_census.json` - capture-only, 32 reads. Live rank for all 31 of ours, plus every
   mission's pre-swap `image` URL and a fresh 445-row asset table.
2. Icon swap, all 31, built on live rank only - no asserted ranks this time.
3. dauntless runs the asset deleter against the final list (the ten `dmissionicons` plus whatever the
   census turns up; Case/Blacksteel icons excluded, reused by Genin Trials).
4. Publish + hide as one combined final push. Still gated on the content admin, and on the hazards logged
   in the hide-wave section above.

## Census results (2026-08-31, bundle tnr_results_1788134455342)

- Live rank, all 31: **D 15** (10 D-set + Case Contract x4 + Blacksteel Shard Salvage), **C 8**
  (4 Forsworn + Blacksteel Cleanup/Iron Hunt/Perimeter Breach/Supply Raid), **B 4**, **A 4**.
- **19 of the 31 are already `hidden:false`** - every contract, eight of the D-set, and Copies Not Thefts.
  Only 12 remain hidden. The later publish step is smaller than the board assumed.
- Icon provenance: nine D-set missions point at their `dmissionicons` asset. Everything else points at a raw
  uploadthing URL with no gameAsset record - the twelve Forsworn at a shared placeholder ('Zeps house' URL),
  the nine contracts at ONE shared contract icon, and Copies / Witness / One White Ear each at their own.
- Consequence for the deleter: the list is exactly the ten `dmissionicons` assets and nothing else. The
  contract icon has no asset record, so it cannot be deleted from the asset manager and the Genin Trials
  reuse is safe by construction.

## Icon swap shipped 2026-08-31 (bundle tnr_results_1788135094828)

- 31 quest edits, 31 ok / 0 fail, asserted read-back per entry, plus an independent pre/post record diff.
- Four distinct icon URLs, one per rank, wired across A 4 / B 4 / C 8 / D 15.
- Content, questRank, hidden, description and successDescription byte-identical to the census on all 31.
- Manifest carried `skipPreflight:true` (builder qBad gap on partial quest edits). Generator:
  `push/24_rank_icon_swap_all31.gen.py`.
- The nine D-set `dmissionicons` references are now released; the ten assets are free to delete.

## Earmarked for upgrade or retirement (not in this release)

- **One White Ear** - questType event, d1/d2/d3 converging dialog menus, stray .jpg icon before the swap.
- **Witness Detail** - bmissions-era B mission, stays hidden.
- **Copies, Not Thefts** - already public, and its a1/a2/f1 dialog menus converge. Live record fails
  validate.py today, before any edit of ours.
