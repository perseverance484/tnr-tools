# Catalog and template generation provenance

Catalog: `catalog-1caefb53206168966f10`. Templates: Aerathiel v1 and Night Parade v1. Normalizer v1. Player jutsu level 25, bloodline level 100, summon abilities at captured equipped level 1. These are display inputs, not claims about the author’s account.

Game mechanics/guide contract source: `studie-tech/TheNinjaRPG@36c5873b7b6ee5fd3af717008d7c51b0f185b756`. Data records are separately timestamped public captures; source code and live balance data are intentionally distinct provenance. Design contract: `87fb673938d915c0732351d2efb208d05ef38c7c`.

Scope: two complete five-jutsu bloodlines; 35 normalized jutsu; four summon records; 41 official cached images. The support picker covers the two supplied guide references. Expanding to all game jutsu/bloodlines requires an operator refresh and complete reviewed templates; unknown effects fail closed.

## Inputs

| Committed safe input | SHA-256 |
|---|---|
| `fixtures/tnr_results_1789188714166.json` | `3907637224a3b1a8c3f3bda1c475decc5b36866b6ef443a3cb32532b9d63fc88` |
| `fixtures/tnr_results_1789271613950.json` | `b21de9a746fc3d75d848cd6f9ac695cf429eec8a8358fd581c2eeaf999f5d76d` |
| `fixtures/tnr_results_1789273598969.json` | `20a75bb19df3db4473957992c1f74bb7ef5837e425100de82efd4dbcd50fdc86` |
| `fixtures/public-refresh-2026-09-13.json` | `fc7cd7b55451b73d49c9d994c65207c1367f5d17173a1b4e8a60422821627858` |
| `fixtures/bloodline-refresh-2026-09-13.json` | `91a7ab9be32b337c34a60195131eb2eff83f861cf7a34ef1aebb8919adebffe2` |

The three `tnr_results_*` inputs are content-only projections of existing `harvests/inbox/` captures at the base SHA. Only bloodline/jutsu records and summon identity/art/equipped jutsu are retained. Unrelated runtime state and player/session data are excluded. Original capture hashes:

- `tnr_results_1789188714166.json`: `97f09e518efaea2d7b1ca1b634c698c7641601927a996abdfd90ce158d117b6e`
- `tnr_results_1789271613950.json`: `8856a192ed0ba07c7e48bdea5929fa59d056ea9d31b0f44c49d379ea5a9b8b62`
- `tnr_results_1789273598969.json`: `54a24f2631dd34cb15342155ba117d73799f1523112c6ae4b6a37c1f9d60286e`

`public-refresh-2026-09-13.json` contains two public, credential-free GETs for the missing Aerathiel bloodline and Death’s March. `bloodline-refresh-2026-09-13.json` contains four public GETs (`bloodline.get` and complete `jutsu.getAll` for each bloodline); both jutsu pages ended with null nextCursor. Total game API requests made for this task: six read-only GETs; zero mutations.

Official art was downloaded separately from the captured CDN URLs, with ordinary image GETs and retries. Each image records source URL, original SHA-256, transformed SHA-256, dimensions and transformation. Existing repository/reference art guided the design; the implementation uses cached official records, without requiring player uploads of official images.

## Reproduction

```sh
node scripts/catalog.mjs --check
node scripts/fixtures.mjs --check
node scripts/compatibility.mjs --check
npm run fixtures
python3 scripts/card-gallery.py
```

Refresh is separate from build/authoring: `python3 scripts/refresh.py --output <new-snapshot.json> --bloodline <id>`. It allows only the two public read procedures, refuses redirects and incomplete pagination, and refuses to overwrite a snapshot. Add a new snapshot deliberately to the producer’s input list, cache official art using `scripts/assets.py`, generate a new catalog, and review affected templates. No refresh runs from the public app, Worker, gate or importer.

Asset acquisition uses Pillow 12.3.0 (thumbnail <=768px, WebP quality 88). Card gallery uses CairoSVG 2.9.1. Committed image bytes, not a potentially changed CDN, are the reproducible build inputs. Catalog hashing canonicalizes object keys. All submissions pin the exact catalog and template.

## Browser delivery projection

`scripts/catalog.mjs` also generates `catalog/browser.v1.json` from the canonical catalog: all normalized records, templates, provenance and version are preserved; `imageData` is removed and replaced by `assetHashes`, derived from `fixtures/official-assets.json`. This is a delivery projection, not a new balance/template version. `--check` mechanically re-derives both outputs from the same pinned inputs. No input captures or official bytes changed in the review correction.

The public app loads ordinary artwork through `/assets/<hash>.webp`. On preview, `src/preview-assets.mjs` fetches only art used by the complete selected foundation and build, refuses redirects, omits credentials, and verifies the recorded SHA-256 before embedding it into self-contained SVGs. Successful/in-flight loads are shared; failures are retryable. Browser and server fixture artifacts remain byte-identical, including their package hashes. The Worker still uses the complete canonical catalog and needs no runtime CDN/TNR fetch.

## Mechanical interpretation

- Effect target and semantic direction remain separate from the engine offence/defence stat axis. Black Thorn Rose emits enemy HEALING REDUCTION 50% and self DAMAGE TAKEN reduction 30%, both for two rounds; no offensive DAMAGE/POWER classification.
- General/stat types, damage multipliers and bloodline damage modifier flags are preserved. Pinned `combat/tags.ts` treats zero multiplier fields as inactive, not zero damage.
- Healing’s static display uses the pinned engine’s ×10 pool conversion; shields display health separately from chance; stun displays AP reduction separately from chance.
- Nue and Jurogumo share the captured hidden self-OHKO routine, shown as Summon Departure. Shuten-Doji’s self-departure effect remains in Unbearable Hunger. The complete equipped summon sets, including this routine, are validated.
- Captured Gate links associate Famine with Shuten-Doji and Death with Jurogumo. The visual reference posters swap those names; the implementation follows captured records. AI rule cadence/order is not established by equipped-jutsu lists, so the template does not promise a fixed rotation.

## Design fixtures

Aerathiel fixture: adapted from `aerathiel_guide_v2_SELF_CONTAINED (1).html`, 15 selected jutsu, 15 notes and eight chapters. Night Parade fixture: adapted from `Guide to Night Parade of a Thousand Demons_260912_130148.pdf`, 12 selected jutsu, 12 notes and eight thematic chapters. Both use Example author to avoid implying a real submitted endorsement.

The supplied reference files were inspected from the user’s available files. Only adapted strategy fixtures and source-verified mechanics are committed here. Foundation copy and visual treatment are implementation proposals for independent/director review.
