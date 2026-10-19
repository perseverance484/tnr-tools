# Bloodline Jutsu Art Studio — minimal handoff templates

**Status:** ZIP-first studio handoff examples under RUL-2026-10-17-020 / RUL-2026-10-19-005 D4. Fill only from verified target/register/source evidence; no guessed mechanics, names, IDs or hashes. The operative art gate is **`docs/workflows/ISOLATED_ART_GENERATION.md` (P0 A–F)**. Executable field and output contracts belong to `skills/producing-tnr-art/scripts/jutsu_studio.py` (PR #66) and its skill/spec; these templates do not define new policy.

## A. Studio → ONE isolated image-generation conversation

~~~text
Repository: perseverance484/tnr-tools
Role: IMAGE PRODUCTION (support: Art Director)
Session: ISOLATED GENERATION — ONE jutsu only
Workflow: docs/workflows/ISOLATED_ART_GENERATION.md (P0)
Studio ref: <exact branch@SHA, if applicable>
Bloodline: <name + exact ID>
Target: <jutsu name + exact ID>
Source evidence: <captured record/pinned kit + evidence_level>
Target lock: <locks.json version / lock_sha256 / director approval evidence>
Raw state: NOT YET APPROVED

Technique/action: <source-supported combat action>
Dominant unique silhouette AND action: <one reserved identity>
Camera/perspective and motion axis: <near/far, aim, direction>
Secondary effect: <one active supporting effect>
Composition: <orientation, negative space, focal hierarchy>
Family material/renderer: <approved treatment from inspected pixels>
Sibling silhouettes/actions excluded: <all other target reservations>
Wrong-subject exclusions: <concrete prohibited compositions>
Anatomy exception: NONE, unless exact target is director-approved
References attached as actual INDIVIDUAL files (maximum two):
1. <exact file and SHA> — IDENTITY ONLY, original jutsu
2. <exact file and SHA or none> — STYLE/MATERIAL ONLY
   (BBE/BEE pinned examples are style; not borrowed technique geometry)
No gallery, ZIP, rejected candidate or unseen URL as image reference.

Render exactly ONE premium square TNR jutsu icon candidate.
Use P0 fail-fast visual target/action, anatomy, chakra and
125/64/32 distinctness checks on returned pixels.
The director decides raw acceptance; log each attempt and reasons.
After 2 wrong-target/composition failures in the same isolated
session, restart with a clean session ID as P0 directs.
No processing, collage, repository modification, or game action here.
Live-game requests/writes: 0/0; credentials: none.
~~~

**Studio intake of a candidate:** preserve exact original bytes, actual decoded MIME/dimensions/bytes/SHA-256, director decision, attempt log outcome and any superseded predecessor. `lock-check` checks the `tnr.jutsu-studio.locks/1` target record and `attempts --locks ...` checks `tnr.jutsu-studio.attempts/1` consistency; neither tool replaces director visual judgment. Never call a screenshot the original accepted raw.

## B. Studio checkpoint after one target

~~~text
Bloodline ID/name: <exact>
Jutsu ID/name: <exact>
Direction lock: <lock SHA, director-approved or pending>
Technique silhouette/action: <unique reserved>
Raw visual state: APPROVED | PENDING | REJECTED
Original source: <real file/MIME/WxH/SHA-256>
Attempt record: <session ID; terminal outcome; count/reasons>
Previous raw superseded: <hash or none>
Current approved raws: <n>/<N>
Family gallery acceptance: PENDING (until exact gallery decision)
Next target: <name + ID>
Live-game requests/writes: 0/0
~~~

Record durable checkpoints at meaningful direction/approval/closeout milestones, not after each exploratory generator failure.

## C. Whole-family closeout — fielded handoff

~~~text
Repository: perseverance484/tnr-tools
Workstream: BLOODLINE JUTSU ICON ART (NOT Bloodright tier icons)
Bloodline: <ID / name>
Branch/Base/Merge-base/Frozen Head: <verified SHAs>
Current exact roster: <N jutsu IDs; evidence level>
Director raw approvals: <N>/<N> (exact raw hashes)
DIRECTION_APPROVED: <per-jutsu lock/evidence, if supplied>
Attempts: <valid log/terminal approval/stats or NOT_RECORDED>
OUTPUT_LOCAL_QC: <actual checks/verdict>
CANONICAL_PREFLIGHT: <PASS|FAIL|NOT_RUN|NON_CANONICAL>
Preflight command/exit/pinned blobs: <actual run; not inferred>
Showcase PNG / manifest: <name; gallery file/pixel SHA>
Showcase members_sha256: <actual ordered member commitment>
FAMILY_SHOWCASE_ACCEPTED: <ACCEPTED|PENDING|INVALIDATED|REJECTED>
Director gallery acceptance evidence: <exact gallery or none>
Source/closeout ZIP: <filename / bytes / SHA-256>
Flat WebP ZIP: <filename / bytes / SHA-256 / PREFLIGHT verdict>
ZIP_DELIVERED: <BUILT_NOT_DELIVERED until actually handed off>
GIT_BINARY_PIN: NOT_PERFORMED | <separately proven>
USER_UPLOAD_READBACK: NOT_PERFORMED | <separately proven>
Credentials: none
Live-game requests/writes: 0/0
Next: <precise outstanding gate or new studio>
~~~

`jutsu_studio.py` uses the full **K gate vocabulary**:
`ORIGINAL_SOURCE_VERIFIED`, `DIRECTION_APPROVED`, `RAW_VISUAL_APPROVED`, `OUTPUT_LOCAL_QC`, `CANONICAL_PREFLIGHT`, `FAMILY_SHOWCASE_ACCEPTED`, `ZIP_DELIVERED`, `GIT_BINARY_PIN`, `USER_UPLOAD_READBACK`. A built ZIP is not delivered or production-uploaded; the CLI itself records Git pin and user readback as `NOT_PERFORMED`.

## D. Actual P1 family archives and acceptance record

After `jutsu_studio.py verify-approved ... --source-index ... --locks ... --attempts ...` and `finalize APPROVED.json --out DIR --label v1 ...`, the tool produces:

~~~text
dist/<fam>_jutsu_icons_closeout_<label>.zip
  manifest/approved.json
  manifest/studio_ledger.json
  manifest/locks.json             # only when supplied
  manifest/attempts.json          # only when supplied
  raws/raw_<slug>_v<version>.<decoded-format-extension> # original bytes (JPEG bytes named .png seal as .jpg)
  exports/icon_<fam>_<slug>_v<version>.webp        # current exports
  qc/export_qc_<label>.json
  qc/preflight_<label>.json
  showcase/<fam>_jutsu_showcase_<label>.png
  showcase/<fam>_jutsu_showcase_<label>_phone.png
  showcase/<fam>_jutsu_thumbs_125_64_32_<label>.png
  showcase/showcase_manifest.json
  SHA256SUMS
dist/<fam>_jutsu_icons_webps_PREFLIGHT_<VERDICT>_<N>webp_<label>.zip
  icon_<fam>_<slug>_v<version>.webp  # N flat WebPs only
~~~

**P0 gallery acceptance recording:** copy `gallery.sha256` (optionally `gallery.pixels_sha256`) and `members_sha256` from the **exact** `showcase_manifest.json` that the director accepted into `approved.json.family_acceptance`, with `status: ACCEPTED` and cited approval evidence; re-run finalize with a **new label** for the acceptance-sealed closeout. Member/raw/export changes invalidate previous acceptance. An `audit-gallery` VALID is mechanical fidelity only, not director acceptance.

Do not call a family “finished in game” from raw artistic acceptance, a locally valid WebP, an archived gallery or a noncanonical preflight. Flat ZIP names never say “upload”; `NOT_RUN`/`NON_CANONICAL` remain non-PASS, and the user alone performs any game upload or publication. **Aerathiel's pending gallery/preflight/Git/readback states are not changed by these templates.**
