# Forge Presentation Studio P1 — R1–R3 closure review

**Verdict: approved for integration within the reviewed P0/P1 scope. R1, R2, and R3 are closed. No remaining merge blocker was found in the agreed correction surface. P0 is unchanged and retains its passing review.**

Reviewed on 2026-09-20. This is technical review approval, not a merge, release, publishing action, final design acceptance, or renderer/Android acceptance. Live-game requests **0**; live-game writes **0**; asset-CDN requests **0**. No implementation, capture, manifest, art, or Fable branch ref was changed by the reviewer.

## Target and authority

| Ref | Independently verified value |
| --- | --- |
| Repository | `perseverance484/tnr-tools` |
| Live main, base, merge-base | `eefefd1afd67111a90c332951a8dd9f83cb99cbd` |
| Fable branch | `claude/forge-presentation-studio-p1-y1wbiq` |
| Frozen local/remote head | `5ac0e947196f88c695d0cdee7aabe75a2f0278b2` |
| Commits above base | `05e71564d693a8505f98df4400502abee7517a3c` (P0), `8830443977122253a956fb77392a7d2925d6cb6f` (P1), `ac792ef1085c8350fda7bf79050d90ca0ce41879` (F1–F7), `5ac0e947196f88c695d0cdee7aabe75a2f0278b2` (R1–R3) |
| ChatGPT branch, based on frozen head | `chatgpt/review-forge-presentation-studio-p1-r3` |
| Previous review | `chatgpt/review-forge-presentation-studio-p1-r2@fb47225a150e89ee74028b38cb31b0aed809c20a` |
| Governing plan | `chatgpt/forge-presentation-studio-plan@99f1aa8a6fe7cc7361aa613cdcad258bafb9c83e`, `docs/plans/FORGE_PRESENTATION_STUDIO_UPGRADE_PLAN.md` |
| Separate design proposal | `chatgpt/forge-presentation-studio-design@4532ef917a1dfb40d00c554fd7f065e13216afc7` |
| Pinned game-source contract | `studie-tech/TheNinjaRPG@345d18accf6d8ea8d8d47ef0e61b5aff7d5a1cf9` |

Live main's state and router were reconstructed again; the required rulings, operating guide, role/workflow documents, and art-production sources remain byte-identical to the main already read in this review session. The governing plan and previous findings remain pinned. `CHATGPT.md`, `docs/DEVELOPMENT_WORKFLOW.md`, and `docs/workflows/FABLE_REVIEW.md` govern this review. Content Designer remains the lead lens, supported by Engineering Auditor, UI/UX Reviewer, and Art Director. No director decision blocks closure of these engineering findings.

The new diff is exactly **nine files, 468 additions / 58 deletions**: presentation modules/README and two presentation test files. Source selection, dossier assembly, route/encounter/reward consumers, and their tests were checked together as requested by the [previous report](https://github.com/perseverance484/tnr-tools/blob/fb47225a150e89ee74028b38cb31b0aed809c20a/docs/reviews/REVIEW_2026-09-20_forge_presentation_studio_p1_correction.md). P0/runtime/build/tooling, package lock, loader, bundle, and committed Godstorm evidence/art did not change.

## Findings closed

### R1 — Closed: one selected current record per quest

The [package guard](https://github.com/perseverance484/tnr-tools/blob/5ac0e947196f88c695d0cdee7aabe75a2f0278b2/forge/presentation/evidence.mjs#L150) refuses overlapping quest IDs and identifies both records/capture selectors. The [dossier guard and map](https://github.com/perseverance484/tnr-tools/blob/5ac0e947196f88c695d0cdee7aabe75a2f0278b2/forge/presentation/dossier.mjs#L52) enforce the invariant again before assembly. Rewards now use the same selected structure/source as the other quest facts.

Independently reproduced:

- An identical Marrow selection under another record ID is refused before it can inflate totals.
- The actual older and current Stormcourt captures are refused together, with the optional story removed, in both record orders. This uses unchanged committed capture bytes and digests, so the story fingerprint and byte-lock checks cannot mask selection behavior.
- Calling `buildDossier()` directly with an already-loaded map containing a duplicate quest is also refused. This directly exercises the lower-level guard rather than relying on the parser path.
- Reordering valid, nonoverlapping evidence records preserves the keyed structures, rewards, and totals.

### R2 — Closed: tied names receive the same conflict treatment as tied images

Both within-record and across-record merges now use [the same comparison](https://github.com/perseverance484/tnr-tools/blob/5ac0e947196f88c695d0cdee7aabe75a2f0278b2/forge/presentation/evidence.mjs#L409) for the consumed `name`, `url`, and `field` facts. Conflicting observations are refused or become fatal lint findings; equivalent observations can coalesce.

The original `Alternate Keeper` witness now fails within one record and across records. Additional checks covered AI and game-asset name conflicts across separately selected bundles in both record orders, with the entity ID, image URL, and capture timestamp held equal. Equivalent same-time observations with different snapshot keys still produce a valid 18-member roster.

These changed-capture probes use the scenario helper's explicitly simulated committed evidence. They are not working-file hash bypasses or claims that conflicting names exist in current Godstorm captures.

### R3 — Closed: success-route order drives rewards and cadence

The [route traversal](https://github.com/perseverance484/tnr-tools/blob/5ac0e947196f88c695d0cdee7aabe75a2f0278b2/forge/presentation/structure.mjs#L206) now follows success edges independently of all-edge reachability. [Encounter assembly](https://github.com/perseverance484/tnr-tools/blob/5ac0e947196f88c695d0cdee7aabe75a2f0278b2/forge/presentation/structure.mjs#L267) numbers route battles and marks other reachable battles `onSuccessPath:false`, `index:null`. Cadence and keeper counts use route battles; the complete roster still includes other reachable battles.

The original forward failure link plus 20,000-ryo intermediate payout now keeps `d5_victory` as full clear (**125,000 ryo / 25 tokens / 10 prestige**) and `d3_1` as intermediate. The valid 145,000 success-route total remains. Four forward failure targets (`d1_4`, `d3_1`, `d5_victory`, `win`) preserve the entire normal success-route order and 4+1 cadence.

An optional opening battle no longer adds a fifth recurring fight to that cadence. An additional independently constructed keeper appearing only in an optional battle confirms that:

- Marrow has 25 route battles plus one separately counted off-route battle; total reachable battle count is 26.
- The route still has five keepers and the event's route totals remain 50 battles / 10 keepers.
- Complete roster coverage rises to 19 distinct AIs; the optional keeper remains required.
- Removing only that keeper's admissible capture is fatal under `coverage:"all"`.

Branching clear routes still fail `ambiguous-full-clear`; they are not approved as a single ordered route. A success-edge cycle on the clear route is refused. The earlier rooted failure-cycle observation is now explicitly warned as a malformed record, while retaining the separately well-defined success route. That warning is not a claim the record would pass the pinned game's save validator.

## Retained protections and golden facts

The prior F1/F2/F6/F7 closures remain intact. Replays confirm refusal of unavailable bound image blobs, failed AI captures, uncommitted reward edits, changed same-ID narrative text, and invalid quest/scene art bindings. Stale before-captures do not replace the selected current reward; storage permutations preserve route facts; optional-exit rewards remain separate. The stale Tower/Dawnless, roster omission, image swap, and scene-as-location regressions remain green in the full suite.

The nonblocking `Ultimately, ` wording case now passes. The ordinary-word list remains a bounded editorial heuristic, not a semantic guarantee; narrative source fingerprints remain required.

The unchanged Godstorm golden package still derives **two pyramids, 25+25 route battles, 18 distinct AIs, five keepers each, 4+1 repeated five times**, current rewards **125,000/25/10** and **250,000/150/60**, no intermediate cash-outs or reward items, and two semantic locations: Marrow Vaults and Stormcourt. Both quests remain hidden in the selected captures. Scene/background assets do not create additional locations. These are committed-capture facts, not fresh live-game observations.

## Verification at the frozen SHA

Environment: Node `v24.19.0`, npm `11.9.0`. Dependencies installed from the unchanged lockfile using `npm ci --offline --ignore-scripts`. Repository and dependency-audit access only; no game or image-CDN access. Scratch scenarios use isolated temporary roots and are not committed.

| Check | Result |
| --- | --- |
| `cd forge && npm test` | **522 passed, 0 failed, 0 skipped** |
| `npm run build`; diff `forge_bundle.js` | Pass; artifact byte-identical |
| `npm run fixtures`; envelope/screens diffs | Pass; no drift; 14 screen fixtures regenerated |
| Import gate | 40 modules / 71 cross-layer imports; 0 violations |
| Boundary gate | 40 source + 13 presentation modules; 0 violations |
| Bundle budget | **339,669 / 354,000 raw; 74,926 / 78,000 gzip** |
| Release-pin check | Clean |
| `npm audit --omit=dev --audit-level=high` | 0 vulnerabilities |
| Default Godstorm CLI | Exit 0; **0 fatal / 22 warnings** |
| Godstorm CLI `--require-exact-bytes` | Expected exit 1; **18 fatal / 4 warnings** |
| Independent previous-witness replay | 19 observations completed; R1–R3 closure and retained protections inspected |
| Additional focused assertions | **17 checks passed**: duplicate selection/direct assembly, tied names, route order, optional roster coverage, branching and cycles |
| `harvest.py verify harvests/inbox/tnr_results_1789842714086.json` | Verified, exit 0; 9 OK / 0 failed / 0 unverified / 0 skipped |
| Session source guards | Lawmap 0 errors / 5 existing warnings; doctrine and packs current; baseline parity adapter remains red |

Scratch commands were `node /workspace/scratch/9b09e6cf21d0/evidence/p1-r3-previous-witnesses.mjs` and `node /workspace/scratch/9b09e6cf21d0/evidence/p1-r3-focused-checks.mjs`. The previous report preserves the original core input recipes; at this SHA their expected outcomes are the closures recorded above. Committed regression cases are in [presentation.adversarial.test.mjs](https://github.com/perseverance484/tnr-tools/blob/5ac0e947196f88c695d0cdee7aabe75a2f0278b2/forge/test/presentation.adversarial.test.mjs#L915), with the strengthened golden route assertions in `presentation.golden.test.mjs`.

## Limits carried forward

- **Global parity is not green.** The pre-existing session adapter still crashes when `validate.py` iterates `checks:null` in the already-committed Forge results bundle. It is unchanged from base main and outside this correction. The dedicated harvest verifier succeeds. This known baseline failure is not a new P0/P1 integration blocker.
- **Default lint is not render readiness.** The registry has 23 entries but verified bytes for only five portraits. Its 18 unbound entries comprise 13 portraits, two quest listing images, and three Marrow scene images; strict exact-byte lint correctly refuses them. Required named-art bindings cannot be silently ignored. Capture admission checks presentation-relevant fields, not the entire server record schema.
- **Finish the existing art contract before claiming a deterministic renderer.** Resolve the already-pinned source archive at `1bca57eeb0c1836a49334dc2f49196a5a3db24c7`, handle approved derivatives, and expose MIME/dimensions as tracked previously. Preserve exact source pixels; never redraw a named game entity generatively. Prior archive verification remains separately pinned evidence; no new remote-byte verification is claimed here.
- **Design and product acceptance stay separate.** The contract/reference at design commit `4532ef9` remains a proposal awaiting director acceptance. No renderer, final poster, Android preview/export/share flow, publishing operation, or live session was exercised or approved by this P1 review.

## Next step

The exact frozen implementation is eligible for the normal reviewed integration path. Re-verify main and the implementation head immediately before integration; any changed implementation SHA needs review of its delta. Keep the ChatGPT review branches as evidence, rather than merging their session records into Fable's implementation. Carry the explicit design/art prerequisites into the P2 brief. No further R1–R3 correction is requested.
