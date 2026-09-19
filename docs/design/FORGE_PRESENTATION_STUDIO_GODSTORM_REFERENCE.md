# Godstorm — Presentation Studio evidence and reference layout

**Status:** verified design reference, 2026-09-19; proposed summary copy; no P1 implementation/fixture approval.

**Baseline:** `main@eefefd1afd67111a90c332951a8dd9f83cb99cbd`. **Contract:** [Presentation Studio design contract](FORGE_PRESENTATION_STUDIO_DESIGN_CONTRACT.md).

This is a bounded, immutable reference for the first golden fixture. It is not a current-content database or an input to a loader that scrapes prose. Fable must derive the fixture from the pinned captures and asset records below. All facts here are relative to selected repository evidence; no live game or asset-CDN request was made in this design session.

## 1. Source lock

| Key | Path at baseline | SHA-256 | Evidence use |
| --- | --- | --- | --- |
| H23 | `harvests/inbox/tnr_results_1789401726302.json` | `4686c6247f14c57341e72dabc2ab9e892cca98a577d705e0a392edc98312d12b` | Historical quest facts; archival art URL provenance only |
| H24 | `harvests/inbox/tnr_results_1789402842027.json` | `25224da3fde7acdc30284a5f750ddd84dce29bb43466d131af8742117d3fa4a7` | 18 full AI captures; thirteen unchanged avatar/name records selected |
| H52 | `harvests/inbox/tnr_results_1789829183863.json` | `178109b3280935a1acb39df15b0733a58e9ee57f23535e13b0434109270584c6` | Marrow current quest capture only; overall run INCOMPLETE/failed |
| H53 | `harvests/inbox/tnr_results_1789842714086.json` | `a4b79cf9cbcc7f79008e52b3175d5f3218cea9027251dd15248bfba3e7b91670` | Completed repair; five updated avatars and current Stormcourt quest |

| Selected quest | Entity ID | Exact capture | Captured at |
| --- | --- | --- | --- |
| Marrow Vaults | `2yvE9PUQqlD8lbYNfgX-b` | H52 `/captures/2/data`, snapshot `52-mu8i2pd8::after::2` | 2026-09-19T14:46:23.568Z |
| Stormcourt | `OSADdXqostbyVliCxWk6k` | H53 `/captures/5/data`, snapshot `53-mu8q43ck::after::5` | 2026-09-19T18:31:53.962Z |

H52 is a partially failed write run. Its Marrow `quests.get` capture independently reports `ok: true`, `persist: full`, `persistOk: true`, matching input/response identity; the Marrow update entry reports `match`. Those scoped facts admit this capture. The run itself must not be promoted to successful. The older Stormcourt capture in H52 is superseded by H53.

H53 is DONE/success, nine VERIFIED/match entries and six successful full captures. H24 is DONE/success; its thirteen selected avatar records were captured September 14, while the five replacements were captured September 19. A later `ai.getAiProfile` record is rules evidence, not a replacement `profile.getAi` avatar record. Show the mixed dates.

Art pack: `archive/spent-manifests/push-2026-09-19/53_godstorm_failed_items_repair.json` at the baseline, `imagePack.ref = 10fb25704dff1bab8105cd83631e0d524193ef0d`. Eight file hashes and sizes were rechecked against those committed blobs.

Recovered archive: `1bca57eeb0c1836a49334dc2f49196a5a3db24c7`, `art/godstorm_sources/capture-2026-09-14/index.json`; original archival commit `3f11dcd325df8d2fd27110999c39f4bab430b000`. The archive contains thirteen avatars, two listing images and four background candidates, all 19 files rechecked for SHA-256, byte length and full image decoding. Its two capture-source hashes also match the baseline files. This reference selects thirteen avatars and two listing images from it.

These archived bytes were acquired September 15 from URLs captured September 14; they do not prove capture-time bytes or original generation masters. Listing URLs were rebound to the selected September 19 quest fields by equality. The older filenames/titles do not supply current display names. The contract’s exact-current class means exact source for this selected snapshot, with capture/acquisition dates visible; it does not approve new artwork or certify the live CDN today.

The recovery archive and source-art-pack branch hold the same relevant source hashes in different layouts. This reference deliberately pins one archive, never picks whichever filename looks convenient. Do not merge an old art branch wholesale. The eight `art/godstorm/` processed files remain the source for the repair; never replace them with recovered/default/master candidates.

## 2. Verified structural and reward population

| Measure | Marrow Vaults | Stormcourt | Total |
| --- | ---: | ---: | ---: |
| Reachable objectives | 53 | 53 | 106 |
| Dialogue objectives | 26 | 26 | 52 |
| Battle objectives | 25 | 25 | 50 |
| Keeper fights | 5 | 5 | 10 |
| Distinct recurring / ascendant AIs | 4 | 4 | 8 |
| Distinct keeper AIs | 5 | 5 | 10 |
| Distinct AIs | 9 | 9 | 18 |
| Fail / win terminal nodes | 1 / 1 | 1 / 1 | 2 / 2 |
| Intermediate cash-out nodes | 0 | 0 | 0 |
| Item reward entries | 0 | 0 | 0 |

Walked all next/choice/failure links from the unique start of each graph: 53/53 reachable in each. The success route has five groups of four ordinary battles then one keeper, followed by the victory dialogue and the win terminal. Ordinary identities rotate; every floor uses the same component-specific four-AI set once. All 50 battle references resolve to the 18 selected records.

| Full clear | Reward-bearing objective | Ryo | Tokens | Prestige | Reward items |
| --- | --- | ---: | ---: | ---: | --- |
| Marrow Vaults | `d5_victory` (`dialog`) | 125,000 | 25 | 10 | Empty |
| Stormcourt | `d10_victory` (`dialog`) | 250,000 | 150 | 60 | Empty |

**Extraction trap:** both `win` terminals and both root `content.reward` blocks contain neutral rewards. The nonzero rewards are on the final reachable dialogue nodes. Scanning only `win_quest` or the root would incorrectly produce zero. These are captured quest-authored rewards, not a claim about incidental combat drops or unrelated global rewards.

The absence check scanned all 106 objectives plus both root reward blocks. All 106 `reward_items` arrays and both root arrays are empty; exactly two objectives carry non-neutral rewards. No early cash-out node exists in either selected graph. Both quest captures report `hidden: true`; publication was not checked or performed.

## 3. Complete named roster / deterministic order

Rows are grouped by component, then first ordinary encounter order, then keeper encounter order. IDs and names below were emitted from capture data by script. The final keeper is included in the keeper count.

| Component | Role | Exact name | AI ID | Battle objective IDs | Name/avatar record |
| --- | --- | --- | --- | --- | --- |
| Marrow Vaults | Recurring | Umbral Reaver | 9uDe65Qt90xnT-fM5vJZ7 | b1_1, b2_4, b3_3, b4_2, b5_1 | H53 /captures/0/data |
| Marrow Vaults | Recurring | Hollow Lantern | IG5Mbfi_2lpUTnUU4_XhZ | b1_2, b2_1, b3_4, b4_3, b5_2 | H53 /captures/1/data |
| Marrow Vaults | Recurring | Starless Monk | qQ6jMh8w6aiyr4pevwDh- | b1_3, b2_2, b3_1, b4_4, b5_3 | H53 /captures/2/data |
| Marrow Vaults | Recurring | Nightveil Sentinel | YvinZCoMWiz0RY8ZBP5EW | b1_4, b2_3, b3_2, b4_1, b5_4 | H53 /captures/3/data |
| Marrow Vaults | Keeper 1 | Warden of the First Dark | oi4bHe3upEhLkI-ElJuMX | b1_boss | H53 /captures/4/data |
| Marrow Vaults | Keeper 2 | Keeper of Hushed Hours | s6LjnqhSW85pIxYRM76Fw | b2_boss | H24 /captures/5/data |
| Marrow Vaults | Keeper 3 | The Moth Tyrant | jGHpkz2pgLu8loti6pZZi | b3_boss | H24 /captures/6/data |
| Marrow Vaults | Keeper 4 | Chained Chorister | QV1PwoQR9JImZL2_fcOsk | b4_boss | H24 /captures/7/data |
| Marrow Vaults | Keeper 5 / final boss | Warden of the Half Eclipse | 3XMsIV6Yv4jy-uaJAe52f | b5_boss | H24 /captures/8/data |
| Stormcourt | Ascendant | Hollow Lantern Ascendant | b8PGgZl8zNNr6UdWH9dBv | b6_1, b7_4, b8_3, b9_2, b10_1 | H24 /captures/9/data |
| Stormcourt | Ascendant | Starless Monk Ascendant | JU2BgfdcWsBYGeHUgHMi_ | b6_2, b7_1, b8_4, b9_3, b10_2 | H24 /captures/10/data |
| Stormcourt | Ascendant | Nightveil Sentinel Ascendant | 9yLEi0OoYxcIL0a2XYkWk | b6_3, b7_2, b8_1, b9_4, b10_3 | H24 /captures/11/data |
| Stormcourt | Ascendant | Umbral Reaver Ascendant | k4qMHSTHHZBVsijP5FJ6E | b6_4, b7_3, b8_2, b9_1, b10_4 | H24 /captures/12/data |
| Stormcourt | Keeper 1 | The Gloaming Judge | axTRSadaZbUepfT40-7cM | b6_boss | H24 /captures/13/data |
| Stormcourt | Keeper 2 | Widow of the Waning Moon | HEjtNpXmuU4ShrOOPg8XK | b7_boss | H24 /captures/14/data |
| Stormcourt | Keeper 3 | The Candlewright | pln436P8g2ocUBCHavcdb | b8_boss | H24 /captures/15/data |
| Stormcourt | Keeper 4 | Herald of the Last Dusk | aL1Gf1JmVaP8iWi2zHJoO | b9_boss | H24 /captures/16/data |
| Stormcourt | Keeper 5 / final boss | Sovereign Echo of the Godstorm | i8oFdDcneF7YE-8VpQsu3 | b10_boss | H24 /captures/17/data |

## 4. Exact asset binding inventory

P = the immutable repair pack ref above. R = the immutable recovered-archive ref above. For R rows the file is `art/godstorm_sources/capture-2026-09-14/originals/<SHA-256>.png`; for P rows the exact file path is shown. Source-field joins were checked, not inferred from the name.

| Entity | Source | Exact path or archive key | SHA-256 | Dimensions |
| --- | --- | --- | --- | --- |
| Umbral Reaver | Pack; H53 avatar | `art/godstorm/ai_godstorm_marrow_umbral_reaver.webp` | `30693d5dc252f8ce61638a0b4c191523ef7df8461b8252ff309e21192154bfcc` | 1492×1492 |
| Hollow Lantern | Pack; H53 avatar | `art/godstorm/ai_godstorm_marrow_hollow_lantern.webp` | `50d1786fb6f5c2a2350b04dd27ec1ff8b0e1d58237e98337c0a2065e226b6055` | 1476×1476 |
| Starless Monk | Pack; H53 avatar | `art/godstorm/ai_godstorm_marrow_starless_monk.webp` | `877eef3b0cecc914d4e3300e21cb50c87030093c5730d4feb54b71a7e7cdc870` | 1477×1477 |
| Nightveil Sentinel | Pack; H53 avatar | `art/godstorm/ai_godstorm_marrow_nightveil_sentinel.webp` | `d5c5a8c8a2be20700a7df16b9ac38e4b9cd6a7a2917efa5d7d815d19deebd9e2` | 1429×1429 |
| Warden of the First Dark | Pack; H53 avatar | `art/godstorm/ai_godstorm_marrow_warden_of_the_first_dark.webp` | `0d2bf09980ec6c99226d3528606cf07a112ccf0c843363f5d0761ae0ca997453` | 1490×1490 |
| Keeper of Hushed Hours | Recovery; H24 avatar | `R originals/c5e672d74a9e9d0cf1670bbf9bee6d89109c5b82ae1294fc77f91c4a90211fc1.png` | `c5e672d74a9e9d0cf1670bbf9bee6d89109c5b82ae1294fc77f91c4a90211fc1` | 196×256 |
| The Moth Tyrant | Recovery; H24 avatar | `R originals/edd633f65a0f368ac11cef87733fb38f349d6da7a87c78a3e072744bf4e837ce.png` | `edd633f65a0f368ac11cef87733fb38f349d6da7a87c78a3e072744bf4e837ce` | 220×256 |
| Chained Chorister | Recovery; H24 avatar | `R originals/05d2317e411be50a159c9371181d6cf54e12ac5926d5ceed080e675fa450c8bd.png` | `05d2317e411be50a159c9371181d6cf54e12ac5926d5ceed080e675fa450c8bd` | 177×256 |
| Warden of the Half Eclipse | Recovery; H24 avatar | `R originals/5bd6d083fe8a0114480abeaf03fb5c6519c38ad4165788bad4c453731a7717f8.png` | `5bd6d083fe8a0114480abeaf03fb5c6519c38ad4165788bad4c453731a7717f8` | 207×256 |
| Hollow Lantern Ascendant | Recovery; H24 avatar | `R originals/74b14e775a7904efdeecc639a8570692bdaf4a5a4f7ddfd96a1bab81dbc2521c.png` | `74b14e775a7904efdeecc639a8570692bdaf4a5a4f7ddfd96a1bab81dbc2521c` | 213×256 |
| Starless Monk Ascendant | Recovery; H24 avatar | `R originals/33de67c58f07c98c77bdcca1ebea7e17ca494885463afd6bc4b61deba10d9ef1.png` | `33de67c58f07c98c77bdcca1ebea7e17ca494885463afd6bc4b61deba10d9ef1` | 186×256 |
| Nightveil Sentinel Ascendant | Recovery; H24 avatar | `R originals/5d69dab2bd4f943a79aee0a9634bfde7bedcdd573c31f528d208925adf232107.png` | `5d69dab2bd4f943a79aee0a9634bfde7bedcdd573c31f528d208925adf232107` | 227×256 |
| Umbral Reaver Ascendant | Recovery; H24 avatar | `R originals/b8bd99eba111ccd3849702c7b24b373e966bbc221f8ae9add6e0f5167bd4da40.png` | `b8bd99eba111ccd3849702c7b24b373e966bbc221f8ae9add6e0f5167bd4da40` | 224×256 |
| The Gloaming Judge | Recovery; H24 avatar | `R originals/bc2b8ccdb0a86a316ec371e48d9ff518afb6b189db4a25d10a415be7b539516b.png` | `bc2b8ccdb0a86a316ec371e48d9ff518afb6b189db4a25d10a415be7b539516b` | 225×256 |
| Widow of the Waning Moon | Recovery; H24 avatar | `R originals/a891746acc0e4db00a59aa504b90419b303b7d5c62e38b5f6d7fb0196d7f95ae.png` | `a891746acc0e4db00a59aa504b90419b303b7d5c62e38b5f6d7fb0196d7f95ae` | 230×256 |
| The Candlewright | Recovery; H24 avatar | `R originals/957ff5aa1ed14bfcf267ff435bf7ae509ebd31750c8053eaf51bfd24dc689d25.png` | `957ff5aa1ed14bfcf267ff435bf7ae509ebd31750c8053eaf51bfd24dc689d25` | 229×256 |
| Herald of the Last Dusk | Recovery; H24 avatar | `R originals/4533bbc496ffd7e0880423bf45b114219577405e2edeae368a9df9f90e08d75b.png` | `4533bbc496ffd7e0880423bf45b114219577405e2edeae368a9df9f90e08d75b` | 232×256 |
| Sovereign Echo of the Godstorm | Recovery; H24 avatar | `R originals/d73cb67dcc5b1b8442b8198736a8af0e177c97099ab3a24e4dfc986389282a04.png` | `d73cb67dcc5b1b8442b8198736a8af0e177c97099ab3a24e4dfc986389282a04` | 239×256 |

For the five P avatars, manifest target IDs match H53 profile identities and captured `avatar` URLs equal the corresponding job image mappings. The archive closeout on main records a post-run served-byte rehash for all eight pack files; this session verified the committed bytes and record joins, but did not repeat those CDN reads. Do not describe the idmap by itself as a live read-back.

| Location | Quest ID | Current image field | Exact R file | SHA-256 |
| --- | --- | --- | --- | --- |
| Marrow Vaults | `2yvE9PUQqlD8lbYNfgX-b` | H52 /captures/2/data/image | `art/godstorm_sources/capture-2026-09-14/originals/fa3b9abaf7069e19b757aa89dc843debd019373831fb4c32b23b071be683be72.webp` | `fa3b9abaf7069e19b757aa89dc843debd019373831fb4c32b23b071be683be72` |
| Stormcourt | `OSADdXqostbyVliCxWk6k` | H53 /captures/5/data/image | `art/godstorm_sources/capture-2026-09-14/originals/8cc058177cb900544d229ff2f6eaee841ff850ddf85fab17fc87b680d1164e01.webp` | `8cc058177cb900544d229ff2f6eaee841ff850ddf85fab17fc87b680d1164e01` |

Both listing images are 1536 × 1536 and were individually inspected. The Warden of the First Dark and Sovereign Echo were also inspected individually as representatives of the new large square art and older transparent non-square art. This was composition inspection, not a new production-art approval. The future renderer must retain all 18 portraits and both listing images unchanged and satisfy its own visual gate.

## 5. Anchored summary copy / proposed for acceptance

### Marrow Vaults

Beneath Stormcourt, the Unbroken Thread’s records reveal the elder sister’s captivity through chambers of silence, stolen light and ritual bindings. Beyond the divided threshold, the last Warden falls and the stair opens toward the younger sister’s bound storm.

All anchors below are qualified by quest `2yvE9PUQqlD8lbYNfgX-b`, H52, capture 2. The field is `description`; hashes are SHA-256 of that UTF-8 string.

| Objective | JSON pointer in bundle | Selected passage hash |
| --- | --- | --- |
| `d1_1` | `/captures/2/data/content/objectives/0/description` | `739a7819bd29b96803d9d614edd8c21571055fec777d8d6f5faf1f8b00681665` |
| `d2_1` | `/captures/2/data/content/objectives/10/description` | `a879858e6643a8883418b522c0d54fc1c967eff6611a27c6fdf528a71ddcce3a` |
| `d3_1` | `/captures/2/data/content/objectives/20/description` | `ae45804d0de57b0124b2a6985d61af865584ae7f11cdcdd4489341d3cd501316` |
| `d4_1` | `/captures/2/data/content/objectives/30/description` | `4d37df591c42a73545f1709aa773154fb87a03d34ddce23e3309fece7353c49a` |
| `d5_1` | `/captures/2/data/content/objectives/40/description` | `04efdadbe873715f7b1661662bc98b75577563c1068a973abeebaf8c51490d17` |
| `d5_boss` | `/captures/2/data/content/objectives/48/description` | `183d4cf9bd6e94d09af2aef4f7a1eb6902940db00597b561e7ef6f27ec841152` |
| `d5_victory` | `/captures/2/data/content/objectives/50/description` | `02ffcaa9e5afbf8de83b08ee6e689ff35bc508ddb29c122e1dc928ce5d2a07e3` |

### Stormcourt

Stormcourt’s tribunal and tireless light-keeper expose the Thread’s efforts to contain the younger sister’s weather. Past the circling winds and binding instruments, the Sovereign Echo falls, releasing the storm from the empty armor and breaking the binding above the vaults.

All anchors below are qualified by quest `OSADdXqostbyVliCxWk6k`, H53, capture 5. The field is `description`; hashes are SHA-256 of that UTF-8 string.

| Objective | JSON pointer in bundle | Selected passage hash |
| --- | --- | --- |
| `d6_1` | `/captures/5/data/content/objectives/0/description` | `b885776a097a5b09f40210a0f7f454b8fd437cd82e98bc54caa4d93eb306d1b6` |
| `d6_boss` | `/captures/5/data/content/objectives/8/description` | `e67ab42a9b4a3bf55ee35629ec733c4c23a648685be640ea5c47650053f84c77` |
| `d8_boss` | `/captures/5/data/content/objectives/28/description` | `1463f8770a4061ed1465e88904a83cffc059f89039b5b6b3b49106984df0f3d9` |
| `d9_1` | `/captures/5/data/content/objectives/30/description` | `8def4fb94e46ff5e4337a2fdb0a654e571f40565fb0091e9ac760a757e407331` |
| `d10_1` | `/captures/5/data/content/objectives/40/description` | `55a4bc5f57dc5cbafd21885de0878215b1810cd19cb423768f138099a7053675` |
| `d10_boss` | `/captures/5/data/content/objectives/48/description` | `cb8d5678bca1e75dc492eb0c2c980e347a2c4cfd44a573cfa138878675202ff9` |
| `d10_victory` | `/captures/5/data/content/objectives/50/description` | `0f4aebe3e3e516e2cdb14b61e26600d58461848db4a8943b3995810cc164febb` |

All 52 current dialogue descriptions were read before proposing these summaries. The Marrow rite is still being maintained in the middle of the quest; the blurb does not invent a failed machine there. The Stormcourt summary ties the tribunal to the younger sister, the weather suppression to the light-keeper, and the ending to the Echo and binding instruments. Stable IDs do not preserve validity if the text changes.

## 6. Scene semantics and exclusions

| Scene asset | Captured/resolved asset ID | Current Stormcourt dialogue uses | Exact pack file |
| --- | --- | --- | --- |
| Godstorm Stormcourt Upper Court | 7xVJ55rsqarfRmPqLdv98 | d6_1, d6_2, d6_3, d6_4, d6_boss, d7_1, d7_2, d7_3, d7_4, d7_boss, d8_1, d8_2, d8_3, d8_4, d8_boss, d9_1, d9_2, d9_3, d9_4, d9_boss | art/godstorm/bg_godstorm_stormcourt_upper_court.webp |
| Godstorm Stormcourt Binding Dais Active | L_ziMXaLeT9FSdyQ9hkDi | d10_1, d10_2, d10_3, d10_4, d10_boss | art/godstorm/bg_godstorm_stormcourt_binding_dais_active.webp |
| Godstorm Stormcourt Binding Dais Released | _vK9jDEE0zyop_t23Ijgy | d10_victory | art/godstorm/bg_godstorm_stormcourt_binding_dais_released.webp |

These three rows are scene detail, not additional locations. The default poster uses the two quest listing images. Current top-level `content.sceneBackground` is empty in both quest captures; a renderer must not guess a location from that field or repair game scene wiring during presentation work.

StormCourtyard (`cKHhHoboreP88iH5WjDe7`) is excluded for Godstorm use. The recovered archive’s `REVIEW_STATUS.md` points to AR-001 and RUL-2026-09-15-004 at `c7055bc56683fc00abcd5ceb6a2fb41459c0589e`: it is from SkychainMonastery and was rejected for this subject. Its successful retrieval is not approval. The archive records remain historical evidence.

H23 is the negative reward/branding source: older Marrow/Stormcourt each have 61 objectives, intermediate cash-outs and item rewards; the same final victory IDs also contain item rewards there. H23 additionally contains the Dawnless Crown quest. None can enlarge the current two-component set or override current names, summaries or rewards. Use these real contradictory records for P1 regression fixtures.

## 7. Verification record and next gate

- `harvest.py verify harvests/inbox/tnr_results_1789842714086.json`: exit 0; 9 ok, 0 fail, 0 unverified, 0 skipped; verified.
- `node --test --test-reporter=spec forge/test/imgpack.tool.test.mjs`: 8 passed, 0 failed, 0 skipped; includes the archived push/53 committed-blob guard.
- Repository-only diagnostic extraction walked both graphs, joined all 18 roster identities and 20 required image bindings, checked all eight pack files and all 19 recovery files, and validated all 14 proposed summary anchors. No production module or test was authored.
- `node forge/tools/check_bundle_budget.mjs`: 451,847 raw / 470,000; 88,356 gzip / 92,000. P0 is still required. No bundle was rebuilt or changed.
- Session bootstrap: lawmap 0 errors / 5 pre-existing warnings; doctrine and pack/TOC projections current. The parity step fails at `skills/building-tnr-content/scripts/validate.py:201`: `set(json.load(open(path)).get("checks", []))` receives `None` because H53 contains `checks: null`. Reproduced with the exact absolute bundle path from the skill data directory. This is a baseline checker defect; it does not negate the dedicated harvest result and was not fixed in this design lane.
- Android save/share, renderer overflow and full Forge regression suite were not run. Existing main closeout’s 418-test claim is historical evidence, not this session’s test result.

The next design gate is director acceptance/adjustment of the contract and copy. The next engineering gate is Fable’s frozen P0/P1 handoff, including its actual generated golden fixture and adversarial tests. This document is not a substitute for that independent review. Live requests/writes: ZERO. Credentials: none requested or used for game access.
