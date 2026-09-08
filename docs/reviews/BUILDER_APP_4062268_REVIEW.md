# Builder App narrow correction review — 4062268

**Repository:** `perseverance484/tnr-tools`  
**Implementation branch:** `builder-app`  
**Reviewed SHA:** `4062268f433ffd4d1f9b7b1e2678367ecad9119c` (frozen during review)  
**Parent / prior reviewed SHA:** `a1f91446324f924953108e9f66928e4ece6b8c78`  
**Main observed during review:** `1e3f0c08611d419ed819c8108a25b518f8a7e790`  
**Review mode:** narrow re-check of the four HIGH findings from the prior independent review, plus regressions introduced by those corrections.  
**Verdict:** **CHANGES REQUIRED**.

No live-game requests, writes, cookies, or credentials were used for this review. The pinned game source remained `studie-tech/TheNinjaRPG@345d18accf6d8ea8d8d47ef0e61b5aff7d5a1cf9` and was read only.

## Closure status

### F1 — persisted SENT create can be hand-edited back to PLANNED

**Status: CLOSED in this correction.**

`forge/src/storage/journal.mjs` now runs `repairHistory()` during read/migration. A PLANNED item carrying `sentAt`, `createSentAt`, `confirmedAt`, or `verifiedAt` is restored conservatively to SENT before the runner sees it. The repair does not invent an entity id or rewind terminal states. The added F1/F1b regressions exercise the original hand-edited create reproduction and the proof-field cases.

### F2 — production reconciliation/adoption can use another job's row

**Status: CLOSED in this correction.**

`forge/src/main.mjs` now owns one exported `compose()` graph and wires the same `Journal` into `Reconciler`. `Reconciler` refuses construction without a journal. `Runner.adopt()` uses journal-global `findHolder()`, and `_resolveCreate()` excludes `knownEntityIds()` across jobs. The new test composition calls production `compose()` rather than recreating safer wiring in the harness. F2/F2b/F2c cover production composition, automatic cross-job exclusion, and manual adoption.

### F3 — unknown AI key can mint a placeholder before local failure

**Status: CLOSED in this correction.**

`forge/tools/derive_fields.mjs` derives the effective top-level `insertAiSchema` field set from the pinned `userData` table plus `.omit()` / `.extend()`. The pinned source has the expected direct table object and the 13-key omit plus 22-key extension. `fields.json` carries the derived AI set and `Validator.problems()` uses it without requiring a live row. `_preflight()` runs before `_create()`. The F3 regression proves a typo is rejected before `profile.create` is called.

### F4 — undecodable mutation response can become a definite failure

**Status: NOT CLOSED. HIGH blocker remains.**

The correction handles a response element such as `[{}]`: `decodeElement()` throws, `decodeResponse(..., { mutation: true })` converts that to a `TransportError`, and the runner leaves the item SENT.

However `decodeElement()` still accepts **any truthy `el.error` object** as a decoded tRPC error. It does not apply the exact adapter-shape predicate used for request-level errors. For example:

```js
decodeResponse(200, '[{"error":{}}]', 1, { mutation: true })
```

does **not** throw. The `el.error` branch uses `{}` as `err`, synthesizes `code: "UNKNOWN"`, and returns a normal `{ ok:false, error }` outcome. `readMutation()` only has an ambiguity guard for `MALFORMED_ELEMENT`, so `UNKNOWN` is returned as a normal error. `Runner._failFromOutcome()` then classifies it as SERVER and transitions the already-SENT item to FAILED.

That recreates the safety consequence of the original F4: the HTTP response arrived after a mutation request that may have executed, but an undecodable/malformed per-index error is converted into a terminal negative verdict instead of preserving ambiguity for reconciliation.

The checked-in `forge_bundle.js` contains the same permissive `if (el && el.error)` branch, so this is present in the shipped artifact as well as source.

#### Minimal correction

Validate per-element errors before decoding them. The same exact adapter predicate is sufficient for the pinned protocol:

```diff
 function decodeElement(el, i, status) {
   if (el && el.result && el.result.data !== undefined) {
     ...
   }
   if (el && el.error) {
+    if (!isTrpcErrorBody(el)) {
+      throw new TransportError(`batch element ${i} has a malformed tRPC error`, {
+        httpStatus: status,
+        element: el,
+      });
+    }
     const err = el.error.json !== undefined
       ? superjson.deserialize({ json: el.error.json, meta: el.error.meta })
       : el.error;
     ...
   }
 }
```

For a mutation, the existing `decodeResponse()` catch then converts this into a request-level `TransportError`; for a query, it remains `MALFORMED_ELEMENT` and sibling salvage is preserved.

Add regressions at minimum for:

- mutation `[{"error":{}}]` => throws / runner remains SENT and PAUSED;
- mutation error JSON missing numeric JSON-RPC `code` => throws;
- mutation error JSON missing `data.code` => throws;
- the same malformed error element in a query => `MALFORMED_ELEMENT`, with well-formed siblings retained;
- existing valid adapter error fixtures continue decoding normally.

After the fix, rebuild `forge_bundle.js` and update the notes that currently claim all four independent-review findings are closed.

## Verification notes

The Fable commit reports 168 tests passing, byte-identical fixture regeneration, byte-identical `fields.json` derivation from the pinned checkout, and a deterministic bundle rebuild. No CI status checks are attached to this SHA. This reviewer inspected the correction diff, relevant source, new regression tests, pinned `insertAiSchema`, recorded tRPC error fixture, and checked-in bundle, but did not independently execute the npm/test/build/fixture commands because no runnable repository checkout/dependency tree is available in the review environment.

The branch remained at the exact reviewed SHA at the end of the audit.

## Next step

Fable should make only the narrow F4 correction above on `builder-app`, rerun the Forge tests/fixtures/field derivation/bundle build-diff gates, and return a new exact frozen SHA. A narrow re-check remains appropriate if no other architecture or assumptions change.
