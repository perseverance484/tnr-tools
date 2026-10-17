# Bloodright Jutsu Reference Library

Tool: `scripts/bloodright_reference.py` (tests: `scripts/test_bloodright_reference.py`).
Brief: `chatgpt/bloodright-reference-library-brief-20261016@1b3b93b` (`state/prompt_bloodright_reference_library.md`).
Pins: `state/bloodright_reference_library/sources.json`. Coverage report: `state/bloodright_reference_library/inventory.json`.

Builds one master ZIP that extracts once into a folder of per-bloodline ZIPs (29 bloodlines, 166 jutsu),
each holding the original jutsu artwork plus a provenance manifest, for upload to Art Studio.

## Pipeline

1. **Capture (operator, Forge).** A capture-only manifest of `jutsu.get` reads with `persist:"full"`
   (optionally one `bloodline.get` for the identity image) is placed in `push/` on `main` and run in Forge.
   Agents never run captures. Example: `push/101_bloodright_reference_ethereal_monarch_pilot_capture.json`.
2. **Pin.** Add the committed results bundle to `captures` in `sources.json` (manifest path/number/hash,
   bundle path + SHA-256, job id). A bundle is only adopted through this deliberate pin.
3. **Inventory (offline).** `python3 scripts/bloodright_reference.py inventory --write`
   Derives the cohort from the pinned roster blob and kit dossiers, checks every pinned bundle (manifest
   hash, DONE/success, zero mutations, persisted full bodies, id match), and marks each bloodline
   `READY` or `SOURCE_BLOCKED` with the exact missing IDs.
4. **Acquire (network, CDN only).**
   `python3 scripts/bloodright_reference.py acquire --pilot BR-023 --cache ~/br-cache --allow-network`
   Refuses blocked bloodlines before any request. Fetches only allowlisted asset-CDN HTTPS URLs (the
   `jutsu_art.py` host list, no credentials/port/query), at most 3 redirects, 8 MiB cap, full Pillow
   decode, single frame. Writes nothing unless every required image passes. Cached URLs are not
   refetched; `--recheck` refetches and fails on changed bytes rather than replacing them.
5. **Pack (offline).** `python3 scripts/bloodright_reference.py pack --pilot BR-023 --cache ~/br-cache --out ~/br-out`
   Deterministic (fixed order, 1980 timestamps, 0644, STORED, canonical JSON); the archive is verified
   in memory before it is atomically placed. A pilot is always `..._PILOT_<ids>.zip`; the full
   `Bloodright_Jutsu_Reference_Library.zip` is only produced by `--all` with 29/29 and 166/166 ready.
6. **Verify (offline).** `python3 scripts/bloodright_reference.py verify ~/br-out/<zip> --pilot BR-023 --cache ~/br-cache`

Requirements: Python 3.12+, Pillow, and a clone that has the pinned roster commit
(`git fetch origin fable/bloodright-planning-20261003`). The output ZIP is delivered outside Git.

## Network boundary

Only `acquire` opens connections, only with `--allow-network`, only to asset CDNs. Nothing in the
tool contacts `theninja-rpg.com`. Agent sandboxes whose egress proxy blocks the asset CDNs cannot run
step 4; the operator runs it on a machine with normal internet access (steps 3-6 need only Python).

## On an Android phone (Termux)

`build` runs acquire, pack and verify in one step. In Termux:

```sh
pkg update && pkg install -y python git python-pillow   # first time only
termux-setup-storage                                    # first time only: lets Termux write to Downloads
git clone -b fable/bloodright-reference-library-20261016 https://github.com/perseverance484/tnr-tools && cd tnr-tools
git fetch origin fable/bloodright-planning-20261003     # pinned roster objects (inventory needs them)
python scripts/bloodright_reference.py build --pilot BR-023 \
  --cache ~/br-cache --out ~/storage/downloads --allow-network
```

The ZIP lands in the phone's Downloads. (Clone `main` instead once this branch is integrated.) Later runs: `git pull`, then the same `build` line (use
`--all` for the full library once inventory shows 29/29). Cached images are not downloaded twice.
