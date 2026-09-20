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

## The three rules everything here follows

1. **Facts are derived.** Battle counts, keeper counts, roster membership, reward values, locations
   and current art come out of captured records. The spec parser refuses a `rewards`, `battles`,
   `keepers` or `rosterNames` key **by name**, and says which dossier key owns it.
2. **Prose carries anchors.** A summary cites the objective ids it summarises, those ids must exist
   and be reachable in the current capture, and the summary may not introduce proper nouns that
   appear nowhere in the selected evidence. An anchor check alone would not have caught the stale
   Tower/Dawnless wording, because stale prose can cite perfectly real ids.
3. **Named art is exact pixels.** For an AI whose art shipped from this repository the whole chain
   is checked offline: working-tree file → blob at the pack's immutable commit → the URL that blob
   was uploaded as → the avatar the live record currently serves. No step consults a byte count,
   which is why a wrong file of exactly the right size fails.

## Layout

| File | Owns |
| --- | --- |
| `evidence.mjs` | the evidence package schema and loader; every source is a committed repository path |
| `structure.mjs` | objective-graph reachability, counts, encounter sequence, cadence derivation |
| `rewards.mjs` | rewards from **reachable** nodes only; full clear vs intermediate cash-out |
| `roster.mjs` | the derived roster and the validation of the spec's role annotations |
| `assets.mjs` | the exact asset registry and its five statuses |
| `narrative.mjs` | anchor resolution and the unsupported-name check |
| `spec.mjs` | the versioned spec parser, closed key set, facts refused by name |
| `dossier.mjs` | assembly, provenance map, content-addressed hash |
| `lint.mjs` | the fatal/warning rules of plan §4.5 |
| `build.mjs` | spec file in, dossier plus lint out |
| `gitblob.mjs` | the one place that shells out: `git cat-file` for a blob at a commit |

`packages/godstorm/` holds the worked example: `evidence.json` selects six committed records,
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
reads the local object database. An entity whose only current art is a remote URL resolves as
`exact-current-remote`: correct, provenanced, and explicitly not yet renderable. Materialising those
into a content-addressed cache with digest verification is P2's job, and the lint says so.

## Asset statuses

| Status | Means |
| --- | --- |
| `exact-current-bytes` | the whole chain holds; renderable deterministically offline |
| `exact-current-remote` | current art from a committed capture, no repository bytes bound yet |
| `historical-only` | these bytes are this entity's art, from **before** it was replaced |
| `missing` | no selected evidence records any art for this entity |
| `mismatch` | the bound bytes are not this entity's current art (a swap, or a working tree that has drifted from the commit the pack names) |

`historical-only` and `mismatch` are separated deliberately: the remedies differ, and a single
equality check cannot tell "stale" from "somebody else's".

## Use

```sh
node tools/presentation.mjs presentation/packages/godstorm/spec.json
node tools/presentation.mjs presentation/packages/godstorm/spec.json --json > dossier.json
node tools/presentation.mjs presentation/packages/godstorm/spec.json --require-exact-bytes
```

Exit 0 when the lint has no fatal finding. `--require-exact-bytes` is what a deterministic renderer
must pass; on Godstorm it currently fails on the thirteen entities whose art is remote-only, which
is the honest state of the evidence rather than a defect.

## Tests

- `test/presentation.golden.test.mjs` — the Godstorm golden fixture, every assertion of plan §8.
- `test/presentation.adversarial.test.mjs` — the negative fixtures, each a mutation of the real
  Godstorm evidence in a throwaway root rather than a hand-written miniature.
- `test/presentation.boundary.test.mjs` — containment, plus a check that the repository's approved
  Godstorm art still matches the pack byte for byte.
