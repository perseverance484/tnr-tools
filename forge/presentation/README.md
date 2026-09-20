# Presentation dossier and lint (Forge Presentation Studio, phase P1)

Repository-side tooling that turns **selected committed evidence** into a source-bound read model a
presentation can be built from, and refuses to build one it cannot source.

Governing plan: `docs/plans/FORGE_PRESENTATION_STUDIO_UPGRADE_PLAN.md`
(`chatgpt/forge-presentation-studio-plan@99f1aa8a6fe7cc7361aa613cdcad258bafb9c83e`).

This is **P1 only**. There is no renderer, no Forge UI, no publish action and no export here.

## Why

Forge can execute content packages safely. What it could not do was produce an explanatory artifact
that was true. The finished Godstorm event shipped correctly and the poster that explained it did
not: five enemies shown for an eighteen-enemy roster, per-floor cash-outs that had been removed,
scene backgrounds presented as the event's locations, named characters redrawn by an image model,
and stage wording inherited from a superseded draft.

None of those was carelessness. They happened because the presentation was assembled from whatever
was nearest — chat context, planning prose, scattered image files — and nothing in the pipeline was
in a position to disagree with it. This library is that missing position.

Two independent reviews shaped the contracts below: the first
(`docs/reviews/REVIEW_2026-09-20_forge_presentation_studio_p0_p1.md`) reproduced seven bypasses, the
re-review (`..._p1_correction.md`) three residuals. Evidence and spec schemas are at **v2** because
the shapes changed.

## The three rules everything here follows

1. **Facts are derived.** Battle counts, keeper counts, roster membership, reward values, locations
   and current art come out of captured records. The spec parser refuses a `rewards`, `battles`,
   `keepers` or `rosterNames` key **by name**, and says which dossier key owns it.
2. **Prose carries anchors.** A summary cites the objective ids it summarises, those ids must exist
   and be reachable in the current capture, and the summary may not introduce proper nouns that
   appear nowhere in the selected evidence. An anchor check alone would not have caught the stale
   Tower/Dawnless wording, because stale prose can cite perfectly real ids.
3. **Named art is exact pixels.** For an entity whose art shipped from this repository the whole
   chain is checked offline: working-tree file → blob at the pack's immutable commit → the URL that
   blob was uploaded as → the art the live record currently serves. No step consults a byte count,
   which is why a wrong file of exactly the right size fails — and an *unreadable* commit makes the
   binding `unverified`, never verified.

A fourth rule runs underneath all of them: **only admissible captures are evidence, and only at a
known commit.** A record is admitted when a supported read actually happened, persisted in full,
and answered about the entity it was asked about; the package names `repoCommit` and every record
names its `sha256`, and both are checked before a single fact is derived.

And a fifth: **selection must be unambiguous, never positional.** One current record per quest, one
capture per selector, freshness by each capture's own timestamp, and two equally-recent observations
that disagree about *any* fact a presentation consumes — name as much as image — are a conflict to
resolve, not a race to win by array order.

## The route is walked over success edges

A quest record's edges come in two kinds: where the player goes on a win, and where they go on a
loss. Almost everything a presentation says about *sequence* depends on keeping them apart.

`successPath` is one traversal over success edges from the entry, entering only nodes that can still
reach a `win_quest`, so membership and order come from the same walk and cannot drift. The full
clear is the last payout on it; everything else is an intermediate, an optional branch, a failure
payout or an unreachable remnant, each named separately. Cadence counts **route** battles only —
an optional fight is listed, numbered `null`, and excluded from the rhythm of the clear.

A loop through success edges on the route is refused: there is then no order in which a player walks
it. A loop that exists only through a failure link is reported instead — the pinned flow validator
rejects such a record, but the route itself is still well defined.

## Layout

| File | Owns |
| --- | --- |
| `evidence.mjs` | the package schema, the source lock, capture admission and conflict-aware selection |
| `structure.mjs` | graph-derived entry and order, reachability, the success path, cadence derivation |
| `rewards.mjs` | rewards classified against the route to a win: full clear, intermediate, optional, failure, unreachable |
| `roster.mjs` | the derived roster and the validation of the spec's role annotations |
| `assets.mjs` | the asset registry: WHICH art (status) and WHETHER we hold it (bytes), kept apart |
| `narrative.mjs` | anchor resolution, the unsupported-name check, and the source fingerprint |
| `spec.mjs` | the versioned spec parser, closed key set, facts refused by name |
| `dossier.mjs` | assembly, provenance map, content-addressed hash |
| `lint.mjs` | the fatal/warning rules of plan §4.5 |
| `build.mjs` | spec file in, dossier plus lint out |
| `gitblob.mjs` | the one place that shells out: `git cat-file` for a blob at a commit |

`packages/godstorm/` holds the worked example: `evidence.json` selects seven committed records at a pinned commit,
`spec.json` carries only presentation choices.

## Boundary

**None of this is in `forge_bundle.js`**, and three checks keep it that way:

- `tools/check_boundaries.mjs` fails if anything under `src/` imports `presentation/`, and fails if
  anything under `presentation/` issues a request or names a game host;
- `test/presentation.boundary.test.mjs` asserts the built bundle carries no presentation marker, and
  shows the gate catching both violations rather than trusting it;
- the dependency runs one way on purpose: `presentation/` reuses `src/runner/imgpack.mjs` for the
  image-pack contract, so there is one owner for those rules rather than a second copy.

**Zero live requests.** Every source is a file under the repository root plus `git cat-file`, which
reads the local object database.

An entity whose only current art is a remote URL is `exact-current` with `bytes.bound: false`:
correct, provenanced, and not renderable. **It does not follow that those bytes require a live
fetch** — an earlier claim in this file said so and was wrong. `chatgpt/godstorm-art-recovery`
carries a committed content-addressed archive
(`art/godstorm_sources/capture-2026-09-14/index.json` at `1bca57eeb0c1836a49334dc2f49196a5a3db24c7`)
whose entries join to the remaining portraits and to both listing images by entity id and captured
URL. Wiring it in as a `sourceArchive` evidence kind is the named next step for this library and is
deliberately not part of the correction pass; until then the lint says "resolve it from a committed
source archive or materialise and hash it", which is the honest instruction.

## Asset statuses, and byte availability

Two independent axes, because conflating them is what let an unverifiable binding pass as
renderable art.

`status` — WHICH art this is:

| Status | Means |
| --- | --- |
| `exact-current` | the art this entity currently serves |
| `approved-derivative` | an approved repository derivative rather than the live bytes |
| `historical-only` | this entity's art, from **before** it was replaced |
| `mismatch` | not this entity's current art: a swap, or a working tree that has drifted from the commit the pack names |
| `missing` | no selected evidence records any art for it |

`bytes` — WHETHER we hold and verified those pixels: `{bound, path, ref, sha256, length, available,
verified, verifiedAgainst, reason}`. `renderable` is `status === exact-current && bytes.verified`,
and it is the only thing a deterministic renderer may consume. A bound asset that is not verified is
a **fatal** lint finding, not a note: an absent verifier is not verification.

`historical-only` and `mismatch` are kept apart deliberately — the remedies differ, and a single
equality check cannot tell "stale" from "somebody else's".

## Use

```sh
node tools/presentation.mjs presentation/packages/godstorm/spec.json
node tools/presentation.mjs presentation/packages/godstorm/spec.json --json > dossier.json
node tools/presentation.mjs presentation/packages/godstorm/spec.json --require-exact-bytes
```

Exit 0 when the lint has no fatal finding. `--require-exact-bytes` is what a deterministic renderer
must pass; on Godstorm it currently fails on the eighteen entities whose bytes are not bound, which
is the honest state of the selected evidence rather than a defect.

A spec's story blocks carry `sourceDigest`. When the dialogue behind an anchor changes, the build
fails and prints the current digest; update the summary and the digest together after re-reading.

## Tests

- `test/presentation.golden.test.mjs` — the Godstorm golden fixture, every assertion of plan §8.
- `test/presentation.adversarial.test.mjs` — the negative fixtures, each a mutation of the real
  Godstorm evidence in a throwaway root rather than a hand-written miniature. Cases marked `F1`–`F7`
  and `R1`–`R3` are the reviewers' own witnesses, kept in their shape so a re-review can check them
  one for one.
- `test/presentation.boundary.test.mjs` — containment, plus a check that the repository's approved
  Godstorm art still matches the pack byte for byte.
