# Forge repo-backed image packs — implementation handoff

**Lane:** A (tooling)
**Implementation owner:** Fable / Claude Code
**Repository:** `perseverance484/tnr-tools`
**Branch:** `claude/repo-backed-image-packs-qke6mb`
**Base:** `28bba70d0e14f74a768193881b592b92326f2867` (`main` at implementation start; verified with `git rev-parse HEAD`)
**Head:** see the handoff block at the end of this document
**Integration target:** `main`
**Review round 1:** `chatgpt/review-repo-backed-image-packs@2618043433e06519fbfad450cbd06a3314822c7a` reviewed `fbb4fb49ad49a9ef3063067fe3350fbce50fd265` — **CORRECTIONS REQUIRED** (F1, F2). Both accepted and corrected; see section 11.
**Live requests / writes / credentials:** none. Zero game requests, zero game writes, no session or cookie material obtained, requested or synthesised. Every test drives the fake game through `FakeClient`; the repository fetch is a fake in every test.

---

## 1. Objective

A manifest may bind each `@img:<name>` reference to an immutable repository blob — a path, a 40-hex commit and that blob's SHA-256 — so that opening the manifest in Forge fetches and verifies those exact bytes instead of asking the operator to find a file. The manual picker remains, as a fallback for images a pack does not bind.

The defect this answers is recorded evidence, not a hypothetical. In `harvests/inbox/tnr_results_1789829183863.json` (items 3-7) the manifest asked for `ai_godstorm_marrow_starless_monk.webp`; the picker keyed the chosen file under that expected name and showed a green "picked" pill; what had actually been selected was the unprocessed master `1000014259.png` at 1,709,179 bytes. Five Marrow avatar edits ran to their uploads inside a live run and failed one 524,288-byte ceiling refusal at a time.

The byte ledger (`imgSizes`, lint L17) already moved that discovery before Start. It cannot go further, because **a size is not an identity**: any file of the right length satisfies it. A pack names the bytes.

## 2. The contract

Canonical owner: `forge/src/runner/imgpack.mjs`. That file carries the rules and the reason for each; this section is a pointer and a shape, not a second authority.

```json
{
  "imgSizes": { "ai_godstorm_marrow_starless_monk.webp": 207410 },
  "imagePack": {
    "ref": "<40-hex commit sha>",
    "files": {
      "ai_godstorm_marrow_starless_monk.webp": {
        "path": "art/godstorm/ai_godstorm_marrow_starless_monk.webp",
        "sha256": "<64 lowercase hex>",
        "bytes": 207410
      }
    }
  }
}
```

Five rules, all **fail-closed at parse time**, so a malformed pack can never open a job:

| # | Rule | Why it is fatal rather than advisory |
|---|---|---|
| 1 | `ref` is a 40-hex **commit** sha | A branch or tag moves. A binding that can change after review is not provenance. `"main"` is the mistake the rule exists to stop. |
| 2 | `path` is repository-relative and plain | A pack arrives with a manifest. No leading slash, no `.`/`..`, no backslash, no scheme, segments limited to `[A-Za-z0-9._-]`. |
| 3 | `sha256` is 64 lowercase hex | The comparison against it is the only reason repository bytes are safe to upload. |
| 4 | `bytes` equals the `imgSizes` entry for the same name | Two ledgers disagreeing about one file means the manifest contradicts itself. Guessing which is authoritative is how the Godstorm run shipped the wrong file. Both numbers are named in the refusal. |
| 5 | The repository path's extension matches the logical name's | `@img` resolves by exact filename and the extension decides the declared MIME; a `.png` blob bound to a `.webp` name is a mismatch. |

A pack **need not** cover every `@img`. Uncovered names stay the manual picker's. A bound entry nothing references is an advisory and is never fetched.

**Manifest identity.** The pack decides which bytes a run uploads, so it is part of execution identity: it is folded into the policy `manifestHash` covers. It is added **only when present**, so every manifest written before packs existed — including one carrying a non-default policy such as push/53's `dedupNames` — keeps the exact hash it already had and its open jobs still resume. Re-spelling a pack (key order, whitespace) does not change identity.

## 3. Operator flow

1. **Open the manifest.** `ForgeCore.selectManifest()` parses it and, when it carries a pack, immediately runs `prepareImages()`. Fetching belongs to opening; Start only ever gates.
2. **Forge fetches and verifies.** Per bound image: look in the content cache, otherwise fetch `path` at `ref` through the existing GitHub contents client, check the length, then check the SHA-256. Verified bytes become a `File` held as **staged data**. Nothing reaches `runner.files` until the whole pass completes and the core confirms this manifest is still the selected one; the install then clears every bound name and sets every verified one in a single synchronous block. See section 11/F2.
3. **Start.** The manifests screen shows per-image provenance (path, commit, digest, and whether the bytes came from the cache or the repository) and refuses to enable Start until every bound image is verified.

A bound image has **no manual override**: the Pick button is not rendered for it, only "Re-fetch from repository". A provenance an operator can replace from a gallery is not provenance.

**Resume** re-prepares the pack. A page reload empties `runner.files`, so a resumed job that still owed an image upload used to need the operator to find the file again; with a pack it is deterministic. `attach()` has already refused a manifest whose identity — pack included — differs from the one the job was opened on.

## 4. The five properties a reviewer should attack

1. **Immutable provenance.** Rule 1 is enforced at parse time (`normalizeImagePack`), and `forge/tools/make_image_pack.mjs` resolves whatever revision it is given to a 40-hex commit before emitting anything.
2. **Hash verification.** Verified on **every** fetch *and* **every** cache hit, never once and remembered, and **again on the item's own send path** immediately before the bytes leave (section 11/F1). Size is checked first (it catches a truncated transfer without hashing). A repository blob that fails is refused and **not retried** — the blob at an immutable commit does not change between two requests, so a retry could only launder it. A *cache* entry that fails its own key is corrupt, so it is deleted and the repository is read once.
3. **Cache identity.** `storage/assets.mjs` keys on the SHA-256 and nothing else. A cache keyed by path, by `path@ref`, or by logical filename can answer a question nobody asked; keyed by digest, a hit either is the requested content or is not a hit. Path and commit ride along as reporting provenance and are deliberately not part of the key, so two manifests binding one blob share one cached copy. It is a **third** IndexedDB database (`tnr_forge_assets` v1) for the same reason `tnr_forge_repo` is a second one: a version bump on `tnr_forge` is a one-way door that would leave a rolled-back bundle unable to open the operator's journal.
4. **Fail-closed fetch behaviour.** Every failure is a reported per-image state, never a thrown error, so one unreachable blob does not abandon the other seven — and the Start gate refuses the job regardless of what the report says. No digest available means refusal, not unverified use. The install **clears** every bound name before setting the verified ones, in one synchronous block, so an image that failed verification ends the pass deleted: it cannot be left holding a file from an earlier preparation, an earlier manifest, or the manual picker.
5. **No bypass of the Start gate.** `startJob()` runs `packGateProblems()` **in addition to** the existing byte-ledger gate, reading the runner's own maps at the moment of the tap rather than the report drawn on screen. It refuses a mismatched digest, a provenance whose path or commit has moved, and a `File` swapped out from under a still-valid record — **including a replacement of exactly the right length**, because the gate binds the identity of the verified object, not its size (section 11/F1). A device file of exactly the ledgered length satisfies L17 and is still refused.

### The stale-URL defect this also closes

`tnr_bk_idmap_v1` maps a **filename** to an uploaded URL and is shared with the old builder. The runner used to skip an `@img` upload whenever that map held the name. Two different files have carried the same logical name across manifests, so for a pack-backed image that map is not evidence: reusing its URL would ship the previous picture behind this manifest's provenance, silently, behind a green row. Upload reuse for a bound image is now keyed by **content** (`tnr_forge_asset_uploads_v1`, keyed by SHA-256); the idmap is still written so `resolveRefs()` can substitute the URL, but it is never read as permission to skip the upload. An **unbound** image keeps the historical name-keyed behaviour exactly, and a test holds that too.

## 5. Authoring a pack

`forge/tools/make_image_pack.mjs` reads bytes with `git cat-file blob <commit>:<path>` — never from the working tree — so the binding is true by construction. A file that is staged, modified, untracked or simply absent at that commit cannot be bound, and the tool says which.

```sh
# 1. commit the processed art, then:
node forge/tools/make_image_pack.mjs push/53_godstorm_failed_items_repair.json \
     --root art/godstorm --ref HEAD            # print the block for inspection
node forge/tools/make_image_pack.mjs push/53_godstorm_failed_items_repair.json \
     --root art/godstorm --ref HEAD --write    # splice it in beside imgSizes
```

It also cross-checks `imgSizes` and refuses an entry that disagrees with the committed bytes, naming both numbers rather than taking the file's.

**Deliberately not done: no Python re-implementation of the pack rules.** `skills/building-tnr-content/scripts/validate.py` does not reject unknown top-level keys, so a manifest carrying `imagePack` passes the mandatory validate gate unchanged. Re-stating the five rules in Python would create a second authority that can drift from `imgpack.mjs` — the mistake `CLAUDE.md` §7 and the `00_INDEX.md` precedence table both warn about. The authoring gate is the tool above; the enforcement gate is Forge. A reviewer who wants validate.py to reject a malformed pack should say so, and the right shape for that is validate.py *invoking* the Node contract, not copying it.

## 6. First production fixture — push/53, and what is blocked

The proposal names push/53 (the Godstorm repair: 3 Stormcourt backgrounds + 5 Marrow avatars) as the first production fixture. **Its `imagePack` block is not in this change, and the manifest is byte-unchanged**, because the eight processed `.webp` files are not in the repository:

```
$ node forge/tools/make_image_pack.mjs push/53_godstorm_failed_items_repair.json --root art/godstorm
  REFUSED bg_godstorm_stormcourt_upper_court.webp: art/godstorm/bg_godstorm_stormcourt_upper_court.webp
          is not in commit 28bba70d0e14. Commit the file first; a pack must bind bytes the repository already holds.
  ... (8 of 8)
```

A SHA-256 cannot be authored for bytes nobody has. Inventing one would produce exactly the fiction this feature exists to prevent, so nothing was invented. To land the production fixture:

1. commit the eight processed `.webp` files (the ones whose byte counts push/53's `imgSizes` already records) under an art path, e.g. `art/godstorm/`;
2. run the `--write` command in section 5 against that commit;
3. re-run `python3 skills/building-tnr-content/scripts/validate.py push/53_godstorm_failed_items_repair.json` from the skill's `data/`;
4. open the manifest in Forge and confirm 8/8 verified before Start.

What **is** covered now: the full production shape is exercised against the real `push/53` text. The suite reads the committed manifest, asserts its ledger still holds exactly those eight names, splices a pack over its own `imgSizes`, and drives selection to a verified 8/8 with the Start gate clean — plus a test asserting the committed file still carries no pack, so this claim cannot rot.

## 7. Changed files

| File | Change |
|---|---|
| `forge/src/runner/imgpack.mjs` | **new.** The pack contract: normalization, the five rules, path validation, hex, MIME, work selection. Pure. |
| `forge/src/storage/assets.mjs` | **new.** `AssetCache` over `tnr_forge_assets` v1, keyed by SHA-256; the content-keyed upload ledger. |
| `forge/src/core/imagepack.mjs` | **new.** `prepareImagePack()` (cache → verify → stage, writes nothing), `commitImagePack()` (atomic clear-then-set) and `packGateProblems()` (the Start gate, binding File identity). |
| `forge/src/runner/manifest.mjs` | parses and validates `imagePack`; folds it into execution identity only when present. |
| `forge/src/runner/runner.mjs` | `imgProvenance` map; `_imgPreflight()`; `_imgBytes()` (identity + re-hash at the upload boundary); content-keyed upload reuse for bound images. |
| `forge/src/core/core.mjs` | `assetCache` + `digest` required deps; `prepareImages` action; pack gate in `startJob()`; pack preparation on `resumeJob()`; `_packEpoch` currency token and the single epoch-guarded commit point. |
| `forge/src/main.mjs` | `sha256()` (WebCrypto, no fallback); `AssetCache` and `digest` wired into `compose()`, `digest` also into the `Runner`; `VERSION` 0.5.0. |
| `forge/src/ui/screens.mjs` | pack banner, per-image provenance rows, no Pick button for a bound image, pack problems surfaced, Start disabled on them. |
| `forge/src/ui/app.mjs` | forwards `prepareImages`. |
| `forge/tools/make_image_pack.mjs` | **new.** Authoring tool; reads blobs out of git at a resolved commit. |
| `forge/tools/check_bundle_budget.mjs` | budget ratchet stepped, with the measurement and reasoning. |
| `forge/test/imgpack.test.mjs` | **new**, 33 tests: contract, identity, fetch/verify/cache, provenance scoping, the F1 same-size-swap regressions, the F2 deferred-fetch selection races, the Start gate, upload identity, the push/53 fixture. |
| `forge/test/storage.assets.test.mjs` | **new**, 5 tests: database isolation, digest-keyed identity, size limit, the upload ledger. |
| `forge/test/imgpack.tool.test.mjs` | **new**, 6 tests: the tool reads git, not the working tree; four refusals. |
| `forge/test/screen_scenarios.mjs` + 2 fixtures | `manifests_pack_verified` and `manifests_pack_refused` golden screens. |
| `forge/test/core.contract.test.mjs` | golden updated deliberately for the one new action. |
| `forge/package.json`, `forge_loader_user.js`, `forge_bundle.js` | 0.5.0 package + `@x-release-pending 0.5.0`; bundle rebuilt. |

## 8. Verification (exact commands, run on this branch)

| Command | Result |
|---|---|
| `cd forge && npm test` | **416 pass / 0 fail** (372 on `main` before this change: +44; 411 at the reviewed SHA) |
| `node forge/tools/check_imports.mjs` | 40 modules, 71 cross-layer imports scanned — 0 violations |
| `node forge/tools/check_boundaries.mjs` | 40 modules scanned; generated-contract pin `345d18accf6d8ea8d8d47ef0e61b5aff7d5a1cf9` — 0 violations |
| `node forge/tools/check_release_pin.mjs` | release pin ok |
| `node forge/build.mjs` | wrote `forge_bundle.js` (441.3 KB) |
| `node forge/tools/check_bundle_budget.mjs` | raw 451,847/470,000 (96.1%); gzip 88,356/92,000 (96.0%) — base on `main` was 424,642/81,344. Ceiling stepped a **second** time; see section 11 and the file's own comment |
| `node forge/tools/derive_screens.mjs` | wrote 14 screen fixtures (12 before); regenerated after the corrections and **byte-identical** to the committed set |
| `node forge/tools/make_image_pack.mjs <smoke> --root art/style_refs/scene_backgrounds` | bound `drying_yard.webp` @ `28bba70d0e14`, sha256 `68a6ae61b27be28d…`, 107,652 bytes |
| `node forge/tools/make_image_pack.mjs push/53_... --root art/godstorm` | exit 1, 8 refusals (the blobs are not committed) — see section 6 |

Nothing is piped in a way that masks an exit code.

**Bundle reproducibility.** `forge_bundle.js` is rebuilt from `forge/src` by `forge/build.mjs` (esbuild, IIFE, no minify) and the checked-in file is a fresh build of this tree's source. The budget numbers above are that file.

## 9. Gates NOT run, and why

- `scripts/doctrinemap.py`, `scripts/render_doctrine.py --check`, `scripts/build_packs.py --check`, `scripts/lawmap.py`: nothing under `skills/` or `docs/DOCTRINE.md`/`docs/ENGINE_LAWS.md` changed, and no law/code coverage relationship changed. This change adds a Forge-owned manifest key; it does not restate or alter a cross-surface law. If a reviewer judges the new key to be doctrine-adjacent, the routed gates should be run before integration.
- Any browser check. The overlay was not loaded in a real browser, no userscript was installed, and `crypto.subtle`'s secure-context behaviour on the operator's Firefox/Android is **inferred from the platform contract, not observed** (see section 10).

## 10. Risk, debt and open items

- **Unverified in a real browser.** The digest path uses WebCrypto, which needs a secure context; the game is HTTPS so it is expected to be present, and the code refuses rather than degrading where it is not. That refusal path is tested with an injected null digest, but no real Firefox/ViolentMonkey run was performed.
- **IndexedDB storing `ArrayBuffer`.** `AssetCache` stores structured-clonable `ArrayBuffer`s, which is standard, and is exercised under `fake-indexeddb`. It has not been exercised against a real browser's quota behaviour; a `put` failure is already treated as non-fatal (the digest is the contract, the cache is an optimization).
- **Eight blobs per open.** Opening a packed manifest issues one contents-API request per bound image on a cold cache. That is eight requests for push/53, unauthenticated-or-PAT against `api.github.com`, which is well inside any rate limit; it is warm on every later open.
- **Repository size.** Committing processed art puts image bytes in git history permanently. That is the cost of immutable provenance and it is the user's call whether `art/` is the right home; section 6 step 1 assumes it, reversibly (the path is per-entry).
- **No prefix allowlist on `path`.** Rule 2 refuses traversal and non-plain paths but does not restrict packs to `art/`. The SHA-256 is what binds the content, so a directory policy would add a second thing to keep in step. Say so if you want one.
- **Open user decision:** whether the eight Godstorm `.webp` files should be committed, and under which path. Section 6 is blocked on it.
- **State not rewritten.** `state/digest.json` / `state/active-context.md` are the session-close ritual's on `main`; this branch does not touch them.
- **Attack this hardest:** `core/imagepack.mjs` `one()`'s two-attempt loop, and whether any route exists from a failed verification to a populated `runner.files`. That is the whole safety property.

## 11. Correction round 1 — F1 and F2

Review: `chatgpt/review-repo-backed-image-packs@2618043433e06519fbfad450cbd06a3314822c7a`,
`docs/reviews/REVIEW_2026-09-19_repo_backed_image_packs.md`, against
`fbb4fb49ad49a9ef3063067fe3350fbce50fd265`. Verdict CORRECTIONS REQUIRED. **Both findings accepted
in full; neither is disputed.** Both were real and both were mine: section 4's claim that Start
"refuses a `File` swapped under a still-valid record" was true only when the swap changed the file's
length, which is the size-only trust boundary this whole feature exists to leave behind.

### F1 — Start did not bind provenance to the actual `File`

`packGateProblems()` compared the provenance digest, path and ref against the manifest and then
compared the current file's **size** against the pack. A different file of exactly the expected
length passed every check, was uploaded, and was then recorded in the content-keyed upload ledger
under the **correct** digest — so every later job that legitimately wanted those bytes would reuse
the wrong URL. The prior test only swapped in a 3-byte file, so the size check caught it and the
dangerous case was never exercised.

Corrected in three places:

1. `commitImagePack()` stores the verified `File` **on** the provenance record (`prov.file`), so the
   record and the object it vouches for cannot be installed apart.
2. `packGateProblems()` requires `runner.files.get(name) === prov.file`. A `File`/`Blob` is
   immutable, so holding the exact object is a complete answer to "are these still the bytes that
   were hashed" — this is the shape the review prescribed.
3. `Runner._imgBytes()` re-checks that identity **and re-hashes the bytes** immediately before the
   upload, and `_imgPreflight()` checks identity too.

**Point 3 is more than the review asked for** (it offered identity *or* a re-hash, and judged the
re-hash "probably unnecessary" given immutability). Two reasons I kept it, both concrete:

- `runner.files` is a public `Map` that the manual picker writes device files into. Identity is
  sound only under the assumption that everything in that map is an immutable `Blob`; the re-hash
  makes the property hold without depending on that.
- `_preflight` is **create-only** (`runner.mjs`: `item.op === "create" && item.state === "PLANNED"`).
  push/53's five Marrow avatars are **edits**, so `_resolved` is the only barrier their bytes pass.
  Putting the last check on the send path rather than at Start puts it where every item goes.

It costs a `digest` dependency on the `Runner` and hashing at most 512 KB (every upload slug's
ceiling) per image on its own send path. **If you want it removed, say so** — identity alone still
satisfies the finding, and dropping it also returns some bundle budget.

### F2 — a stale preparation could write into a newer selection

`prepareImagePack()` wrote each verified image into `runner.files`/`runner.imgProvenance` as it went,
and the caller's "is this still the selected manifest?" check ran **after** that mutation, so it
could only discard the result object, never the side effects. Hold manifest A's fetch, select B,
release A: A's writes land after B's scope cleanup, and a name B left to the manual picker inherits
A's file and A's provenance — which then routes B through the content-keyed upload path for A's
bytes.

Corrected exactly as the review prescribed:

1. `prepareImagePack()` performs **no** runner writes at all. It returns verified images as `staged`
   data. The tests hand it a context with no `runner` at all, which is the cheapest structural proof
   that it cannot.
2. `commitImagePack()` installs staged data synchronously, with no `await` inside it, clearing every
   bound name and setting every verified one in one block.
3. `ForgeCore` carries a monotonic `_packEpoch`, bumped by every act that changes which pack is
   authoritative (selection, resume scope). `_prepareImages()` captures it on entry and calls
   `commitImagePack()` only if both `state.selected` and the epoch are unchanged. A stale pass
   installs nothing — it does not even clear. `resumeJob()` commits under the same guard.

### Regression tests, and proof they are not vacuous

Five new tests (33 in `imgpack.test.mjs`, up from 28). Required coverage, all present:

| Required by the review | Test |
|---|---|
| same-size, same-MIME swap; Start refuses and opens no job; `ASSET_UPLOADS_KEY` untouched; `_resolved()` cannot upload; original file still starts | `F1: a SAME-SIZE swap after verification is refused by the Start gate, and nothing is uploaded` |
| `_resolved()` cannot upload the replacement (the no-preflight path) | `F1: the runner refuses a same-size swap even when no preflight runs` — covers identity, the re-hash, and no-digest-wired |
| deferred fetch, manifest switch, A binds / B unbound; no provenance, no file, Start blocked until a manual pick | `F2: a fetch still in flight when the selection changes installs NOTHING into the new manifest` |
| repeat with overlapping packs so the current selection always wins | `F2: with OVERLAPPING packs the current selection always wins` |
| — (structural) | `F2: preparation alone writes nothing; only the commit installs` |

Each fix was then reverted in isolation to confirm the tests are red without it — this repo's own
"the gate catches a violation when one exists" discipline:

| Reverted | Result |
|---|---|
| the F1 identity + re-hash checks | **3 fail** / 30 pass — both F1 tests and the pre-existing `packGateProblems` test |
| the F2 currency check (commit moved before it) | **1 fail** / 32 pass — the deferred-fetch selection race |
| nothing (restored) | 33 pass / 0 fail |

### Bundle budget, stepped a second time

The corrections measured raw 451,847 / gzip 88,356 — 97.2% / 98.2% of the ceiling set in the first
round. That passes, but 1.6 KB of gzip headroom is a tripwire for whatever lands next, not a
ratchet, so the ceiling moved to 470,000 / 92,000 (96.1% / 96.0%). **This is the second raise for
one feature**, and review observation 2 already named shrinking headroom as a concern. Whether Forge
needs a size pass of its own is a real open question and is deliberately **not** answered here.

### Scope

Only these corrections. No pack rules changed, no contract change, no manifest-identity change, no
UI change (the screen fixtures regenerated byte-identical). The Godstorm image pack is **not** staged
and manifest 53 was **not** run, per the review's closing instruction. No live request, no game
write, no credential material.

---

```text
Repository: perseverance484/tnr-tools
Branch: claude/repo-backed-image-packs-qke6mb
Base: 28bba70d0e14f74a768193881b592b92326f2867
Head: (see the branch head after push; freeze it for review)
Integration target: main @ 28bba70d0e14f74a768193881b592b92326f2867

Round: correction 1 (review F1 + F2 accepted and applied; narrow re-review requested)
Objective: bind @img references to immutable repository blobs (path + 40-hex commit + SHA-256),
           fetch and verify them when the manifest is opened, and gate Start on that verification.
Not begun / out of scope: push/53's own imagePack block (its blobs are not committed — section 6);
           any Python re-implementation of the pack rules (section 5); skills/ authoring docs;
           Forge Next Phase 1, Phase 2+, Quest Studio.
Live requests/writes/credentials used: none.
```
