// GENERATED from reports/client_contract.json (branch client-contract-audit, commit e86c4b4),
// crud_surface, with the corrections from reports/client_contract_verification.md F4 applied
// (item.get and profile.create are MCP-enabled at source). The verification wins on disagreement.
// Anchored to studie-tech/TheNinjaRPG@345d18accf6d8ea8d8d47ef0e61b5aff7d5a1cf9.
//
// kind:    "query" is sent as GET, "mutation" as POST (derived by running the tRPC 11 adapter,
//          see tools/derive_envelope.mjs and test/fixtures/envelope/get_on_mutation_path_rejected.json).
// limited: true when the procedure is publicProcedure, which carries ratelimitMiddleware
//          (app/src/server/api/trpc.ts:211, slidingWindow(60, "60 s"), key `${path}-${userId}`).
//          protectedProcedure carries none, and no content mutation composes one at its call
//          site (verification F2). item.splitStack proves a limiter CAN be composed per procedure,
//          so this flag is per procedure and never inferred from the base builder.
// mcp:     reachable over the MCP surface (R9 capability boundary). Recorded, not acted on.
// auth:    "public" for publicProcedure, "protected" for protectedProcedure, transcribed from the
//          SAME audit's crud_surface[].auth, each of which carries its own file/line/match at the
//          pinned SHA (e.g. profile.getAi -> routers/profile.ts:1121 "getAi: protectedProcedure").
//          protectedProcedure = enforceUserIsAuthed + sentryMiddleware: it proves a logged-in user
//          and nothing more (trpc.ts:213). It is recorded EXPLICITLY rather than derived from
//          `limited`, even though the two are exact complements across all 45 rows here: `limited`
//          is a statement about the rate limiter, not about authentication, and item.splitStack
//          proves a limiter can be composed onto a protected procedure. Deriving one from the
//          other would make a future limiter change silently move the auth gate.

export const PROCEDURES = Object.freeze({
  "ai.createAiProfile": { kind: "mutation", limited: false, mcp: false, auth: "protected" },
  "ai.getAiProfile": { kind: "query", limited: false, mcp: true, auth: "protected" },
  "ai.toggleAiProfile": { kind: "mutation", limited: false, mcp: false, auth: "protected" },
  "ai.updateAiProfile": { kind: "mutation", limited: false, mcp: false, auth: "protected" },
  "bloodline.create": { kind: "mutation", limited: false, mcp: false, auth: "protected" },
  "bloodline.delete": { kind: "mutation", limited: false, mcp: false, auth: "protected" },
  "bloodline.get": { kind: "query", limited: true, mcp: true, auth: "public" },
  "bloodline.getAll": { kind: "query", limited: true, mcp: true, auth: "public" },
  "bloodline.getAllNames": { kind: "query", limited: true, mcp: true, auth: "public" },
  "bloodline.update": { kind: "mutation", limited: false, mcp: false, auth: "protected" },
  // combat.* are the Phase 1 research additions, audited at the pin above against
  // app/src/server/api/routers/combat.ts: getBattleEntries at :382 and getBattleHistory at :530.
  // Both are protectedProcedure (trpc.ts:230, enforceUserIsAuthed + sentryMiddleware) and neither
  // composes ratelimitMiddleware at its call site — the .use(ratelimitMiddleware) occurrences in
  // that file are at :565, :898, :960, :1410 and :1506, none of which is either procedure — so
  // `limited` is false for the same reason it is false for every other protected row here, and not
  // by inference from the base builder. Both carry .meta({ mcp: { enabled: true } }).
  // Admission to READ them is a separate question answered by research/registry.mjs, not by their
  // presence in this table.
  "combat.getBattleEntries": { kind: "query", limited: false, mcp: true, auth: "protected" },
  "combat.getBattleHistory": { kind: "query", limited: false, mcp: true, auth: "protected" },
  "gameAsset.create": { kind: "mutation", limited: false, mcp: false, auth: "protected" },
  "gameAsset.delete": { kind: "mutation", limited: false, mcp: false, auth: "protected" },
  "gameAsset.get": { kind: "query", limited: true, mcp: true, auth: "public" },
  "gameAsset.getAll": { kind: "query", limited: true, mcp: true, auth: "public" },
  "gameAsset.getAllNames": { kind: "query", limited: true, mcp: true, auth: "public" },
  "gameAsset.update": { kind: "mutation", limited: false, mcp: false, auth: "protected" },
  "item.clone": { kind: "mutation", limited: false, mcp: false, auth: "protected" },
  "item.create": { kind: "mutation", limited: false, mcp: false, auth: "protected" },
  "item.delete": { kind: "mutation", limited: false, mcp: false, auth: "protected" },
  "item.get": { kind: "query", limited: true, mcp: true, auth: "public" },
  "item.getAll": { kind: "query", limited: true, mcp: true, auth: "public" },
  "item.getAllNames": { kind: "query", limited: true, mcp: true, auth: "public" },
  "item.update": { kind: "mutation", limited: false, mcp: false, auth: "protected" },
  "jutsu.create": { kind: "mutation", limited: false, mcp: false, auth: "protected" },
  "jutsu.delete": { kind: "mutation", limited: false, mcp: false, auth: "protected" },
  "jutsu.get": { kind: "query", limited: true, mcp: true, auth: "public" },
  "jutsu.getAll": { kind: "query", limited: true, mcp: true, auth: "public" },
  "jutsu.getAllNames": { kind: "query", limited: true, mcp: true, auth: "public" },
  "jutsu.update": { kind: "mutation", limited: false, mcp: false, auth: "protected" },
  "profile.cloneAi": { kind: "mutation", limited: false, mcp: false, auth: "protected" },
  "profile.create": { kind: "mutation", limited: false, mcp: true, auth: "protected" },
  "profile.delete": { kind: "mutation", limited: false, mcp: true, auth: "protected" },
  "profile.getAi": { kind: "query", limited: false, mcp: true, auth: "protected" },
  "profile.getAllAiNames": { kind: "query", limited: true, mcp: true, auth: "public" },
  "profile.updateAi": { kind: "mutation", limited: false, mcp: true, auth: "protected" },
  "quests.checkRewards": { kind: "mutation", limited: false, mcp: true, auth: "protected" },
  "quests.clone": { kind: "mutation", limited: false, mcp: true, auth: "protected" },
  "quests.create": { kind: "mutation", limited: false, mcp: true, auth: "protected" },
  "quests.delete": { kind: "mutation", limited: false, mcp: true, auth: "protected" },
  "quests.get": { kind: "query", limited: true, mcp: true, auth: "public" },
  "quests.getAll": { kind: "query", limited: true, mcp: true, auth: "public" },
  "quests.getAllNames": { kind: "query", limited: true, mcp: true, auth: "public" },
  "quests.update": { kind: "mutation", limited: false, mcp: true, auth: "protected" },
});

export function procedure(path) {
  const p = PROCEDURES[path];
  if (!p) throw new Error("unknown procedure: " + path + " (not in the audited crud surface)");
  return p;
}
/**
 * Does this procedure require an authenticated Clerk session? Everything the auth gate does keys
 * off this and nothing else: a public read stays runnable while signed out, a protected read or
 * mutation does not. An unknown path throws rather than defaulting either way - guessing "public"
 * would let an unaudited write past the gate, and guessing "protected" would block a read the
 * server would have answered.
 */
export function isProtected(path) { return procedure(path).auth === "protected"; }

export const LIMITED_PATHS = Object.freeze(Object.keys(PROCEDURES).filter((p) => PROCEDURES[p].limited));
export const MUTATION_PATHS = Object.freeze(Object.keys(PROCEDURES).filter((p) => PROCEDURES[p].kind === "mutation"));
export const PROTECTED_PATHS = Object.freeze(Object.keys(PROCEDURES).filter((p) => PROCEDURES[p].auth === "protected"));
