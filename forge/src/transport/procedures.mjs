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

export const PROCEDURES = Object.freeze({
  "ai.createAiProfile": { kind: "mutation", limited: false, mcp: false },
  "ai.getAiProfile": { kind: "query", limited: false, mcp: true },
  "ai.toggleAiProfile": { kind: "mutation", limited: false, mcp: false },
  "ai.updateAiProfile": { kind: "mutation", limited: false, mcp: false },
  "bloodline.create": { kind: "mutation", limited: false, mcp: false },
  "bloodline.delete": { kind: "mutation", limited: false, mcp: false },
  "bloodline.get": { kind: "query", limited: true, mcp: true },
  "bloodline.getAll": { kind: "query", limited: true, mcp: true },
  "bloodline.getAllNames": { kind: "query", limited: true, mcp: true },
  "bloodline.update": { kind: "mutation", limited: false, mcp: false },
  "gameAsset.create": { kind: "mutation", limited: false, mcp: false },
  "gameAsset.delete": { kind: "mutation", limited: false, mcp: false },
  "gameAsset.get": { kind: "query", limited: true, mcp: true },
  "gameAsset.getAll": { kind: "query", limited: true, mcp: true },
  "gameAsset.getAllNames": { kind: "query", limited: true, mcp: true },
  "gameAsset.update": { kind: "mutation", limited: false, mcp: false },
  "item.clone": { kind: "mutation", limited: false, mcp: false },
  "item.create": { kind: "mutation", limited: false, mcp: false },
  "item.delete": { kind: "mutation", limited: false, mcp: false },
  "item.get": { kind: "query", limited: true, mcp: true },
  "item.getAll": { kind: "query", limited: true, mcp: true },
  "item.getAllNames": { kind: "query", limited: true, mcp: true },
  "item.update": { kind: "mutation", limited: false, mcp: false },
  "jutsu.create": { kind: "mutation", limited: false, mcp: false },
  "jutsu.delete": { kind: "mutation", limited: false, mcp: false },
  "jutsu.get": { kind: "query", limited: true, mcp: true },
  "jutsu.getAll": { kind: "query", limited: true, mcp: true },
  "jutsu.getAllNames": { kind: "query", limited: true, mcp: true },
  "jutsu.update": { kind: "mutation", limited: false, mcp: false },
  "profile.cloneAi": { kind: "mutation", limited: false, mcp: false },
  "profile.create": { kind: "mutation", limited: false, mcp: true },
  "profile.delete": { kind: "mutation", limited: false, mcp: true },
  "profile.getAi": { kind: "query", limited: false, mcp: true },
  "profile.getAllAiNames": { kind: "query", limited: true, mcp: true },
  "profile.updateAi": { kind: "mutation", limited: false, mcp: true },
  "quests.checkRewards": { kind: "mutation", limited: false, mcp: true },
  "quests.clone": { kind: "mutation", limited: false, mcp: true },
  "quests.create": { kind: "mutation", limited: false, mcp: true },
  "quests.delete": { kind: "mutation", limited: false, mcp: true },
  "quests.get": { kind: "query", limited: true, mcp: true },
  "quests.getAll": { kind: "query", limited: true, mcp: true },
  "quests.getAllNames": { kind: "query", limited: true, mcp: true },
  "quests.update": { kind: "mutation", limited: false, mcp: true },
});

export function procedure(path) {
  const p = PROCEDURES[path];
  if (!p) throw new Error("unknown procedure: " + path + " (not in the audited crud surface)");
  return p;
}
export const LIMITED_PATHS = Object.freeze(Object.keys(PROCEDURES).filter((p) => PROCEDURES[p].limited));
export const MUTATION_PATHS = Object.freeze(Object.keys(PROCEDURES).filter((p) => PROCEDURES[p].kind === "mutation"));
