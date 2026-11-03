# Item Icon Overhaul — Durable Register

**Status:** intake/planning, 2026-11-03. **Authority:** captured live records for historical image facts, `25x_DATA_art_spec.json` for production, `docs/design/premium_seichi_item_icons/V10_STYLE.md` for pilot art quality. Director owns selection and acceptance.
**Workflow:** `docs/workflows/ITEM_ICON_OVERHAUL.md`; wave manifest `docs/design/item_icon_overhaul/W01_ELEMENTAL_KUNAI.json`.
**Live-game requests/writes during creation:** **0/0**. Historical references are not fresh verification.

## Benchmark / approval ledger

| Reference | Role | Provenance | Status |
|---|---|---|---|
| **Tatsumaki's Bellow V10** | Illustrative pixel craftsmanship; sculpted green spirit-wind, cool steel, hue-shifted light, purposeful pixel clusters | Director-supplied 2026-11-03 PNG; SHA-256 `bd359f3d678ce9bb361ffb3097f19fb99d7a190ea2a417a18c81a4ff8119d017`; attached to initiating conversation, **not committed** | **STYLE BENCHMARK** only; native/source archive and lossless export still pending |
| Bloodthorn Kunai | Existing recognizable kunai construction / family comparator | `art/item_icons/kunai/refs/ref_bloodthorn_kunai_live.webp` | Context reference; **not V10-quality certification** |
| Plain Kunai | Baseline ring/handle silhouette reference | `art/item_icons/kunai/refs/ref_kunai_live.webp` | Context reference only |

## Proposed replacement wave W01 — Elemental Kunai

This continues the existing `docs/design/kunai_family/PROJECT.md` and its prior Ikazuchi pilot proposal, **without assuming that proposal or any source icon is newly approved**. Five elemental siblings are the *candidate set*; Bloodthorn and the plain Kunai are *context*, not W01 replacement targets. The IDs below come from the 2026-10-25 family plan; recapture before claiming current status.

| Item (id) | Current/source icon reference | Replacement wave/family | Benchmark family | Status | Export / QC / live-wiring notes |
|---|---|---|---|---|---|
| **Ikazuchi Kunai** (`GMF1JZ0MChUHc7AtnKABw`) | `art/item_icons/kunai/refs/ref_ikazuchi_kunai_live.webp` (historical) | W01 / elemental kunai; **pilot** | V10 craft / kunai anatomy | **PILOT PROPOSED — RECAPTURE** | Historical black tile/noisy lightning; lock or explicitly approve silhouette changes; no accepted new export; no wiring |
| **Katon Kunai** (`sXaqXBYXGHvK75D7Bpo1h`) | `art/item_icons/kunai/refs/ref_katon_kunai_live.webp` (historical) | W01 / elemental kunai | V10 craft / kunai pilot | **CAPTURE NEEDED** | Keep fire identity distinct; no approved export or wiring |
| **Stonefall Kunai** (`4ILs8HFIRQG56ygG-uGrW`) | **Not archived / not verified** (family plan noted census gap) | W01 / elemental kunai | V10 craft / kunai pilot | **CAPTURE NEEDED** | Verify identity, type, current image and earth treatment before brief |
| **Wave Kunai** (`tFH-9RLeCUcVByQbqd2ic`) | **Not archived / not verified** | W01 / elemental kunai | V10 craft / kunai pilot | **CAPTURE NEEDED** | Verify identity, type, current image and water treatment before brief |
| **Zephyrfang Kunai** (`RIK6tVrKHPEJHz8B_y9dK`) | **Not archived / not verified** | W01 / elemental kunai | V10 craft / kunai pilot | **CAPTURE NEEDED** | Verify identity, type, current image and wind treatment; compare distinctness with Tatsumaki, never clone its swirls |

## Per-item register fields and state gates

Every new wave row must record: **exact item name and ID; source/current icon URL plus captured bundle/snapshot and local SHA-256 when materialized; replacement wave/family; style benchmark and subject/family references with explicit roles; stage/status; native/raw approval; exported filename/hash; `ICON` preflight; 256/125/64/32 and transparency QC; family-sheet approval; @img/live-wiring/read-back notes**. Mark each absent field `PENDING` rather than inventing it.

Suggested status progression: `PROPOSED` → `SOURCE_CAPTURED` → `IDENTITY_LOCKED` → `PILOT_APPROVED` (pilot only) → `RAW_APPROVED` → `EXPORT_QC_PASS` → `FAMILY_APPROVED` → `READY_FOR_OPERATOR` → `LIVE_VERIFIED`. Different rows can be in different states; do not skip gates or equate a sheet with acceptance.

## First intake decision

**Proposed first pilot: Ikazuchi Kunai**, based on the existing research and stored live-reference bytes. The director must accept its identity-lock/redesign exception, pilot artwork and eventual 5-item family presentation. Current full `item.get` records and snapshots still must be captured by an operator-approved workflow; no source URL is inferred from an old catalog. **No batch is ready for live wiring.**
