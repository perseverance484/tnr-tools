# Implementation brief — durable TNR visual reference pack

**Repository:** `perseverance484/tnr-tools`  
**Lane:** A — art tooling / skill infrastructure  
**Implementation owner:** Fable / Claude Code  
**Independent reviewer:** ChatGPT  
**Base SHA at freeze:** `90aac9f132b6190ca505ae6b851647f2b7e77ba9`  
**Suggested branch:** `fable/tnr-art-reference-pack`  
**Integration target:** `main` after re-verifying live head  
**Live-game policy:** no TNR API/tRPC/game-page requests and no game writes. Downloading image bytes only from image URLs already persisted in the committed art-style capture is allowed for materializing the reference corpus; do not perform fresh game reads.

## Objective

Create a durable, repository-owned TNR visual-reference pack so every future art-production session can inspect the same approved live artwork before generation instead of reconstructing “TNR style” from chat memory or prose alone.

The pack must provide:

1. exact local copies of the already-captured live reference images;
2. provenance back to the live `gameAsset` records and capture that supplied them;
3. a lightweight machine-readable index inside `skills/producing-tnr-art/`;
4. a deterministic selector/verification helper for choosing a small target-specific reference set at session start;
5. art-skill/workflow instructions that make reference inspection a required bootstrap step when references exist.

This is a **calibration layer**, not a replacement for `25x_DATA_art_spec.json`. The art spec remains the authority for house-style clauses, numerical target contracts, client rendering, dimensions, formats, chroma, byte ceilings, and the existing measured signature.

## Governing evidence

Read before implementation:

- `CLAUDE.md`
- `docs/00_INDEX.md`
- `docs/RULINGS.md`
- `docs/DEVELOPMENT_WORKFLOW.md`
- `docs/workflows/IMPLEMENTATION_HANDOFF.md`
- `docs/workflows/ART_PRODUCTION.md`
- `skills/producing-tnr-art/SKILL.md`
- `skills/producing-tnr-art/references/prompts.md`
- `skills/producing-tnr-art/data/25x_DATA_art_spec.json`
- `state/art_backlog.md`
- `state/art_produced.md`
- `state/wiring_live_assets.json`
- `push/03_tnr_art_style_reference_capture.json`

The current art spec names the house style **“painted figures with pixel discipline”** and owns the prompt clauses. Do not rewrite those clauses into a new authority. In particular, do not resurrect the struck `smooth painterly shading` or full `rim lighting` language.

## Source capture

Use the committed read-only capture represented by:

`push/03_tnr_art_style_reference_capture.json`

At implementation time, locate the committed result in `harvests/inbox/` by reading result journals and selecting the result whose `journal.manifestPath` equals that manifest path. Fail closed if there is not exactly one suitable successful result or if the expected full bodies were not persisted.

The expected capture set is exactly 18 `gameAsset.get` reads and zero mutation items:

### Scene characters

1. Commander Okabe — `sO1qvvahyR_l3IsWCFVt5`
2. Forsworn Scene - Winter Crow — `cSZBQ23AVVuLmKDaA2jh2`
3. Forsworn Scene - Warehouse Clerk — `1TjPakroW5q8m6nylQRcT`
4. Forsworn Scene - Squad Survivor — `asvKeN5HIBRJ2-fzg9Und`
5. Forsworn Scene - Principal — `gIU6lE4RWWwV8FbP3Fkvs`
6. Forsworn Scene - Pale Fang — `CbU3BRjOLX-Ad5PnbUfxM`
7. Forsworn Scene - Old Ghost — `5QsG6MvGvGlzelOx_g0JN`
8. Forsworn Scene - Keeper — `AM0saNTIIl1FPgc5pAzxc`
9. Forsworn Scene - Grain Merchant — `8mDurYQYmy3G0vb862mkO`
10. Forsworn Scene - Deputy — `rkdd7b_84F_NYq1YUMEl_`

### Scene backgrounds

11. Warehouse Loading Floor — `bBV9I0DcmYGcxVGaBdWL0`
12. Pass Road Dusk — `nmrMHmz9xWojzyIV2mAR8`
13. Waystation Door — `kmDsQUEHSub9GIX5ulO6i`
14. East Road Ambush Site — `E4VJ-IeIQMwbmGGfKc-sn`
15. Drying Shed — `c1e60fERuLUxzt9WY4U37`
16. Drying Yard — `TUtC7yPymsp2GyWwZhoTf`
17. Rooftop Eastern Quarter — `eXoh3W7Q_KaWec02TB17n`
18. Canal Frontage — `JUb5wIdMC0o7VwVVOx1zm`

Do not substitute catalog rows for these captures. The capture owns the live image URL and record state used for this pack.

## Repository layout

Use this separation so the skill ZIP remains small:

```text
art/style_refs/
  scene_characters/
    <reference files>
  scene_backgrounds/
    <reference files>

skills/producing-tnr-art/data/style_refs.json
skills/producing-tnr-art/scripts/style_refs.py
```

The **binary reference images must not live under `skills/`**. The current package builder has a 2 MiB per-skill guard and only excludes specific archive-only directories; do not bloat `dist/producing-tnr-art.zip` with the reference corpus.

The index and selector are small runtime files and should remain packaged with the skill.

Do not modify `.github/scripts/pack_skills.py` merely to make this task fit. The layout above avoids needing a packaging-policy change.

## Reference-byte materialization

Implement a narrow maintainer path in `style_refs.py` or a companion script if cleaner. It may fetch **only** the `image` URLs already present in the committed full-capture bodies.

For each reference:

1. read the captured `gameAsset` record;
2. assert the expected asset id and type;
3. obtain its captured `image` URL;
4. download the image bytes from that URL;
5. do **not** transcode or cosmetically modify the reference image;
6. use Pillow only to inspect file format/dimensions/mode if needed;
7. choose the local extension from the actual decoded format/magic rather than guessing from an extensionless CDN URL;
8. write the exact downloaded bytes to `art/style_refs/...`;
9. calculate SHA-256 over those exact bytes;
10. record dimensions, format, source URL, source asset id/name/type, and source capture path in the index.

If a captured URL cannot be downloaded or decoded, fail rather than silently substituting another image.

Report total reference-pack byte size in the handoff. Do not invent a new hard repository-size policy in this task.

## `style_refs.json` contract

Design a small, versioned JSON format. At minimum each entry must carry:

- stable reference key/slug;
- display name;
- `gameAsset` id;
- target/type (`SCENE_CHARACTER` or `SCENE_BACKGROUND` in v1);
- optional register/category tags;
- priority (`PRIMARY` / `SUPPORTING` or equivalent);
- repository-relative local path;
- captured source image URL;
- committed source-capture path;
- SHA-256 of local bytes;
- width;
- height;
- decoded format;
- concise `use_for` notes;
- concise `do_not_use_for` note where a reference has a known limitation.

Do not duplicate the art spec’s numeric contracts or house-style clauses into this JSON.

### Scene-character registers for v1

Use the already-settled two-register art direction:

**NINJA**
- Commander Okabe
- Winter Crow
- Squad Survivor
- Pale Fang
- Old Ghost

**CIVILIAN**
- Warehouse Clerk
- Principal
- Keeper
- Grain Merchant
- Deputy

These tags are selection metadata, not a new art-style authority.

### Selection priorities

For a new **NINJA scene character**, default selection should include:

- Commander Okabe as a rendering/face/detail quality anchor;
- 2–3 current full-body Forsworn NINJA references for framing, silhouette, costume register, and current mission consistency.

The art spec explicitly notes that Commander Okabe is square and is the weakest exemplar on soft-edge share. Therefore its index entry must say **do not use it as the framing/aspect or alpha-edge quality target**.

For a new **CIVILIAN scene character**, choose 3–4 current CIVILIAN references, biased toward Keeper / Grain Merchant / Deputy for the established earth-tone civilian register.

For a **SCENE_BACKGROUND**, choose 2–4 backgrounds closest to the intended location/composition. Add useful category tags such as interior, rural-road, waystation, ambush-road, rural-structure, yard, rooftop, canal without turning those tags into canon.

Do not include `Nameless Ninja` anywhere in the positive reference pack. It is explicitly rejected/deprecated for new-quality work.

## Selector / verifier CLI

`skills/producing-tnr-art/scripts/style_refs.py` should be simple and deterministic.

Required behaviours:

### `verify`

Example:

```bash
python3 skills/producing-tnr-art/scripts/style_refs.py verify --repo-root .
```

It should fail nonzero if:

- JSON schema/version is invalid;
- duplicate keys or asset ids exist;
- a referenced local file is missing;
- SHA-256 differs;
- decoded dimensions/format differ from the index;
- target/type is unsupported;
- a required v1 reference is absent.

### `list`

List references and metadata by target/register.

### `select`

Example:

```bash
python3 skills/producing-tnr-art/scripts/style_refs.py select \
  --target SCENE_CHARACTER \
  --register NINJA \
  --limit 4
```

Output should be easy to paste into an art-production session and should include:

- selected reference names;
- local repo paths;
- raw-GitHub URL or deterministic repository URL usable when the caller has no local checkout;
- concise per-reference calibration note.

Selection must be stable for the same arguments. Do not add randomness.

When local binaries are unavailable because only the installed skill ZIP exists, `list`/`select` should still be useful from the packaged JSON by emitting repository/raw URLs. `verify` may require a repo checkout.

A `--json` or equivalent machine-readable output mode is encouraged if it stays small and obvious.

Add a socket-free selftest/unit test for parsing, selection ordering, duplicate rejection, and hash/dimension mismatch detection using temporary fixture files. Tests must not depend on the real CDN.

## Art-session bootstrap rule

Update the canonical art-production guidance so a fresh art session follows this order before generation:

1. identify target/type and register;
2. read the current `25x_DATA_art_spec.json` target + `house_style` authority;
3. run/use `style_refs.py select` for the target;
4. visually inspect the selected **individual reference images**;
5. only then compose/generate the new asset.

Add this to the appropriate locations in:

- `skills/producing-tnr-art/SKILL.md`;
- `skills/producing-tnr-art/references/prompts.md`;
- `docs/workflows/ART_PRODUCTION.md` if needed to make the cross-chat bootstrap explicit.

Important wording constraints:

- “References calibrate; the spec governs.”
- Do not say the reference pack replaces `spec.house_style`.
- Do not state that merely placing a URL in a prompt guarantees an image generator consumed the pixels.
- When the generation surface supports actual image references, use the selected **individual images**, not a collage/contact sheet.
- When it does not, the assistant must still inspect the images itself and ground the art-direction prompt from what it actually sees.
- Avoid carrying prior unrelated generated images into a new asset-class generation context. A new asset class should start from a clean generation context with only relevant refs.

This final point is meant to prevent the observed context-contamination failures where Forge UI imagery displaced an icon request and a previously generated cabbage displaced an Ittetsu character request.

## Optional human overview

A contact sheet may be generated for quick human inspection only if it is deterministic and inexpensive. If added:

- label it in metadata/documentation as `HUMAN_OVERVIEW_ONLY`;
- do not return it from `select` by default;
- do not recommend it as an image-generation reference because multi-subject sheets increase composition/subject contamination risk.

This is optional and must not expand the task if individual references + selector already solve the workflow.

## Explicit non-goals

Do **not** in this task:

- regenerate or edit production art;
- change the One Perfect Crop content graph/manifest;
- contact the live TNR API or run Forge;
- fresh-capture assets;
- change `25x_DATA_art_spec.json` house-style measurements/exemplar set;
- remeasure the house style;
- redesign the art registers;
- add deprecated/rejected assets as positive examples;
- redesign skill packaging beyond what is necessary to keep the existing 2 MiB guard green;
- build an automatic image-generation service or assume a raw URL is automatically ingested by `image_gen`;
- add external franchise references to prompts or metadata.

The pack is repository calibration/provenance infrastructure only.

## Acceptance criteria

The implementation is acceptable when all of the following are true:

1. All 18 expected references are materialized from the committed capture’s image URLs, with exact-byte hashes recorded.
2. The 10 scene-character and 8 background entries are present with correct target/register metadata.
3. `style_refs.py verify --repo-root .` exits 0 on the checked-in pack.
4. Tampering with a fixture hash, dimensions, duplicate key/id, or required reference makes the test/verification fail.
5. `select --target SCENE_CHARACTER --register NINJA --limit 4` deterministically returns Commander Okabe plus current full-body NINJA references and explicitly carries Okabe’s framing/soft-edge limitation.
6. A CIVILIAN selection uses current civilian-register mission art and never `Nameless Ninja`.
7. Background selection works independently of scene-character selection.
8. The art skill states that target-specific reference inspection is required before production generation when the pack exists.
9. The art spec remains the sole owner of house-style clauses/numeric contracts; no conflicting restatement is introduced.
10. The reference binaries are not included in `dist/producing-tnr-art.zip` and the existing 2 MiB package guard remains green.
11. No live-game/API request occurs; only already-captured image URLs may be fetched.
12. Existing art-processing behaviour and selftests remain green.

## Required verification before handoff

Run and report exact results for at least:

```bash
python3 skills/producing-tnr-art/scripts/style_refs.py --selftest
python3 skills/producing-tnr-art/scripts/style_refs.py verify --repo-root .
python3 skills/producing-tnr-art/scripts/style_refs.py select --target SCENE_CHARACTER --register NINJA --limit 4
python3 skills/producing-tnr-art/scripts/style_refs.py select --target SCENE_CHARACTER --register CIVILIAN --limit 4
python3 skills/producing-tnr-art/scripts/style_refs.py select --target SCENE_BACKGROUND --limit 3
python3 skills/producing-tnr-art/scripts/rawqc.py --selftest
python3 skills/producing-tnr-art/scripts/artpreflight_selftest.py
python3 skills/building-tnr-content/scripts/doctrinemap.py
python3 skills/building-tnr-content/scripts/render_doctrine.py --check
python3 skills/building-tnr-content/scripts/build_packs.py --check
python3 .github/scripts/pack_skills.py
python3 .github/scripts/pack_skills.py
# compare the two dist hashes to prove deterministic packaging remains intact
git diff --check
```

If actual script names/flags differ in the current repo, use the current canonical equivalents and explain the substitution rather than inventing a compatibility shim.

Also report:

- total bytes added under `art/style_refs/`;
- final `dist/producing-tnr-art.zip` size;
- whether the skillpack workflow auto-committed generated `dist/` changes on the branch.

Because `skills/**` changes trigger `skillpack.yml`, verify the **remote branch head after automation settles** and freeze that final exact SHA for review. Do not hand off a pre-automation SHA if the workflow advanced the branch.

## Handoff

Return using `docs/workflows/IMPLEMENTATION_HANDOFF.md`:

- repository;
- Fable branch;
- exact base SHA;
- exact final remote head SHA after any workflow auto-commit;
- intended integration target;
- changed files;
- capture/result path selected as provenance;
- reference-pack byte count;
- commands/results above;
- generated artifact/package evidence;
- deviations/known debt;
- browser/live checks not performed;
- explicit statement that no live TNR request/write/session credential was used.

Freeze the head until ChatGPT review returns.

## Review focus

ChatGPT will independently attack:

- provenance from the exact committed capture rather than catalogs;
- whether local bytes really match captured source URLs/hashes;
- whether selection metadata accidentally turns into competing art doctrine;
- inclusion of rejected/deprecated references;
- deterministic selection and failure behaviour;
- installed-skill fallback when local binaries are unavailable;
- skill ZIP growth/regression;
- whether the bootstrap actually prevents prose-only/context-contaminated art starts;
- any hidden network/live dependency in tests or normal session selection.
