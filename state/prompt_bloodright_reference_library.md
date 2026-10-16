# Bloodright Jutsu Reference Library — Approved Fable Implementation Brief

**Status:** DIRECTOR-APPROVED, 2026-10-16. **Type:** Lane A offline reference-asset tooling; *not* live-game work, icon generation, or Bloodright tree implementation.
**Lead implementation:** Fable / Claude Code on its own `fable/*` branch. **Independent review:** ChatGPT at frozen exact SHA.
**Brief base:** `perseverance484/tnr-tools main@99e86dc549b86f1f4a5846c0e509fa6bc15b3463`.
**Art design authority:** `chatgpt/bloodright-icon-studio-20261016@792742c264c70c29733306f22962d7b4aad48fad`, specifically `docs/workflows/BLOODRIGHT_ICON_STUDIO.md`, `docs/design/bloodright/ICON_PRODUCTION_TRACKER.md`, and director ruling `RUL-2026-10-16-004` **on that branch**. These files have not been presumed integrated into `main`.
**Pinned roster authority:** `fable/bloodright-planning-20261003@7c1dfdd5e3ee163b90c22694dbb2de94ede08866`: `docs/design/bloodright/roster.json` blob `64f6097cb65daccd636f98c8f35517941b67aebb` and relevant `kits/*.json`.
**Prior art lookup:** `scripts/jutsu_art.py`, `scripts/test_jutsu_art.py`, `docs/workflows/JUTSU_ART_LOOKUP.md` on the verified `main` base.
**No user-owned mechanics, publication or live-game operation decisions are delegated.**

## Goal and director-approved user experience

Create a reusable **Bloodright Jutsu Reference Packager** that assembles existing source-verified bloodline-jutsu artwork into **one downloadable master ZIP**. On Android/mobile the operator extracts the master **once** and sees a single folder containing **29 separately uploadable bloodline ZIPs**. When starting a bloodline's Art Studio, the operator uploads just its bloodline ZIP instead of searching game imagery manually.

The approved **first production population** is precisely **29 public A/S/H bloodlines: 19 A, 6 S, 4 H**. Direct inspection of the pinned roster found **166 linked jutsu records / 166 distinct exact jutsu IDs**. This count covers *all linked jutsu types*, including `SPECIAL` jutsu with an actual `bloodlineId`; do **not** filter solely to `jutsuType=BLOODLINE`. The pinned membership is an art-scope selection, not a claim of current live completeness; do not silently include 35 deferred or other excluded records. A source refresh or scope expansion needs a separate deliberate decision.

This work packages **source reference art**, not the new Foundation / Hidden Art / Advanced Art Bloodright emblems. The approved emblems remain separate and keep their opaque black backgrounds.

## Deliverable layout (outer ZIP; one extraction)

```text
Bloodright_Jutsu_Reference_Library.zip
  Bloodright_Jutsu_Reference_Library/
    README.md
    BLOODLINE_INDEX.json
    SHA256SUMS.txt
    BLOODLINE_PACKS/
      BR-011_Blood_Enchanted_Eyes.zip
      BR-015_Blue_Blade_Eyes.zip
      BR-023_Ethereal_Monarch.zip
      ...
      [29 individual ZIPs, one per approved bloodline]
```

Inside each independently usable bloodline ZIP:

```text
README.md
manifest.json
images/
  <exact-jutsu-id>_<safe-readable-slug>.<decoder-verified-extension>
  ...
```

Requirements:
- Each inner ZIP has **every** approved linked jutsu image for that bloodline, with stable unambiguous names based on exact IDs; manifest carries original display names, `review_id`, bloodline ID/name/rank, jutsu ID/type, source-record/capture provenance, actual decoded format/dimensions, original served-byte length and SHA-256.
- `BLOODLINE_INDEX.json` lists each ZIP, rank, approved linked jutsu count, actual packaged count, each inner-ZIP SHA-256, and source lock. `SHA256SUMS.txt` covers the 29 ZIPs and relevant top-level manifests (not itself).
- Preserve exact **fetched asset bytes**: no rescale, chroma key, conversion, re-encoding, renamed fake extension, or replacement by screenshots. Match extension to **actual decoded format**. CDN rendition bytes do not automatically prove uploader-original equivalence; label provenance accurately.
- An optional verified bloodline-identity image may be placed separately under `identity/` **only** where exact source/provenance exists. Never let a missing optional identity image block the required jutsu reference pack; never substitute a poster.
- ZIP paths/entry names must be safe and portable for Android unzip: short readable ASCII outer names, no `../`, absolute paths, device-path oddities, symlinks, or case-insensitive collisions. Stable manifest `UTF-8` names may retain Unicode. Outer extraction creates **one** top-level folder.
- Deliver the generated master ZIP to the operator as a **downloadable artifact outside Git**. Commit source/script/tests/fixture documentation, not the complete binary art library. Do not imply a usable download exists before the pack is actually constructed and validated.

## Source resolution and safety envelope

1. **Offline discovery first.** Derive the 29 / 166 exact membership from the pinned Bloodright `roster.json` and cross-check IDs/counts against its corresponding kit dossiers and the art-production tracker. The kit JSON is a mechanical projection; its record IDs and names do **not**, by themselves, prove image URLs or show original pixels.
2. Search **existing committed, verified full-record captures** and the pinned `kit_snapshot.json` for exact jutsu ID → record → `image` evidence. Record source path, source commit SHA, capture timestamp, `jutsu.get` input/id, completion/read-back evidence, and image URL. Reuse an existing capture only if it genuinely contains the image, matches the target ID/bloodline and its provenance gates pass. Do not assume `answers/jutsu_art.json` covers these jutsu: its current eligibility **explicitly excludes BLOODLINE jutsu and records with a bloodlineId**.
3. Where a URL is missing, null, unsupported, duplicate/ambiguous, or only inferred, **fail closed for that bloodline**. Emit a machine-readable **coverage report** with every missing exact ID, name, bloodline and the required source evidence. Do not fabricate an URL, guess from neighboring names, use a generic web/image search, or silently omit a jutsu and call the pack complete.
4. If missing image URLs require new `jutsu.get` captures, Fable may draft a **capture-only intake proposal/manifest for explicit operator review**, routed through the repository's normal validated read workflow. **Fable/ChatGPT do not execute these or make any live-game requests.** A capture requiring operator interaction is a separate user-controlled gate, not implicit permission from this packaging approval.
5. CDN acquisition is **explicit opt-in** only, performed after all source identities/URLs are verified. Restrict to public HTTPS asset CDN hosts supported by the current approved `jutsu_art.py` safety policy (evaluate any new actual host independently); reject game/app hosts, localhost, private/metadata addresses, non-HTTPS, and redirects outside the allowed asset hosts. No cookies, user credentials or TNR sessions. Bound redirects/timeouts/bytes, fully decode each image using Pillow, validate format/signature/dimensions/frames and content before storage. Do not follow arbitrary URLs supplied from JSON. Avoid writing secret-bearing URL tokens in portable manifests or logs.
6. Keep **acquisition distinct from packing**. Acquire to a local checksum-indexed cache with verified provenance; optionally reuse content-identical bytes but preserve a jutsu-ID-to-image record for *each* jutsu. Packaging and verification read cached bytes **offline with zero network**. If the remote bytes change under the same URL, surface the changed digest rather than silently replacing a previously accepted library.
7. Do not contact `theninja-rpg.com` or its tRPC endpoints, scrape browser pages, interact with live game account/admin UI, or modify game state. Any allowed CDN-only GETs must be reported **separately** from zero live-game requests.

## CLI/implementation boundaries

Fable owns the architecture; prefer a **small standalone Python script/module and test suite**, reusing the tested URL, decoding and provenance protections from `scripts/jutsu_art.py` where applicable without relaxing that corpus's exclusion policy or breaking `answers/jutsu_art.json` derivation.

Provide distinct operations equivalent to:
- `inventory/plan`: offline member enumeration and captured-image URL/evidence completeness report; no network.
- `acquire`: explicit allowlisted-CDN downloads, content validation and persistent local cache; no game calls.
- `pack`: deterministic per-bloodline inner ZIPs and deterministic master ZIP from verified cached inputs only; no network.
- `verify`: validate all 29/166 membership entries, file decodes, SHA-256s, nested ZIP member bytes, manifest IDs/counts, ZIP CRC and layout; no network.
- `--pilot BR-023` or equivalent: complete **Ethereal Monarch** end-to-end first (6 jutsu), using the exact same code path and evidence policy as the full collection.

**Fail-closed output rule:** by default, **no final `Bloodright_Jutsu_Reference_Library.zip` is marked complete or delivered until 29/29 inner ZIPs and 166/166 jutsu images pass verification**. Pilot and partial diagnostic files must have visibly different names/statuses, and never masquerade as the full deliverable. Build in temporary directories, atomic-replace final outputs on success, preserve an existing verified archive on any fetch/pack/verify failure.

The deterministic pack operation must fix ZIP member order, timestamps, permissions, compression choices and canonical JSON serialization. Acquisition time belongs in a separate ledger; it must not make repeated packing from identical verified cache bytes produce different ZIP hashes.

## Tests, operator UX, acceptance

Required adversarial tests use **in-process fixtures and injected fake transport; no socket to the game**:

- Cohort membership matches the pinned **29 / 166 distinct IDs**; include typed `SPECIAL` with bloodline ID; reject hidden/deferred/nonmember and unexpected duplicates.
- Ethereal Monarch fixture contains **six** exact IDs and has a working pilot ZIP; if actual six URLs cannot be proven, return a precise **SOURCE_BLOCKED** report instead of substituting fixtures into a supposedly complete production ZIP.
- Duplicate names/different IDs, Unicode names, unsafe filenames/traversal, case collision, source-ID mismatches, missing/null image, URL format and host/redirect violations; prohibit unverified completeness.
- HTML/error/truncated responses, signature/extension mismatch, oversize, decode failure, broken/multiframe images, remote byte drift, cache tamper, compromised manifest and duplicate ZIP entry.
- Verify extracted nested ZIP image bytes **exactly equal** acquired verified source bytes, manifest hashes/lengths and counts, ZIP CRC, and repeat output reproducibility (same inputs → **byte-identical inner and outer ZIPs**).
- Simulate failure midway through acquisition or packing and verify no old valid library is corrupted, no partial archive named complete, no user credentials/session content logged and **zero game-host requests**.
- Smoke-test operator-facing README instructions for a standard Android unzip: *download outer ZIP → extract once → upload the single chosen bloodline ZIP to Art Studio*. The Studio must **unpack and inspect** a user-provided ZIP and attach **one or two individual selected images** to each isolated image-generation conversation. A ZIP supplied to the image generator **alone is not proof that its image bytes were ingested**.

At handoff provide: exact branch/base/head/merge-base, script/README paths, source provenance and any unresolved image URLs, commands + results, pilot package/report if truly source-backed, full-package status, downloadable artifact location if complete, byte/format/hashes, tests and deterministic proof, network boundaries (game requests/writes and CDN GET counts), and explicit unresolved decisions. Freeze Fable's SHA for independent ChatGPT review before integration.

## Non-goals / sequencing

- Do **not** create or edit Bloodright trees, skill values, new emblems, poster artwork, live image bindings, Forge collection/write manifests, art preflight spec/validator or game-source code.
- Do **not** auto-upload/archive/publish art to the game or adopt new hidden/excluded bloodlines.
- The distinct opaque-black-emblem `ICON` preflight alpha conflict remains **open**; building a jutsu-*reference* library does not resolve it.
- Avoid UI/Forge bundle integration for this first pass. A CLI + repeatable output is sufficient.
- If source completeness prevents real packaging, finish the **tool + offline tests + exact inventory/gap report** and return the operator-controlled capture proposal as the next gate. Do not inflate an offline feasibility result into a delivered master ZIP.

**Director approval:** the proposal for a single-download, extract-once master ZIP of per-bloodline original-jutsu reference ZIPs, generated by reusable Fable tooling, was expressly accepted on 2026-10-16. The scope, source/production safety and acceptance gates above implement that approved intent without presuming any authorization to touch the production game.
