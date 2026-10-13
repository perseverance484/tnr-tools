// In-process stand-in for the two pinned procedures. No sockets: tests hand `fetch` straight
// to the census. Semantics mirror studie-tech/TheNinjaRPG@641040531 item.ts:
//   getAll: itemDatabaseFilter (hidden defaults to false; min*Cost default 0, gte), ordered by
//           cost, repsCost, id; offset = cursor*limit; nextCursor = rows<limit ? null : cursor+1.
//   getItemWithCraftingRequirements: item + craftingRequirements[{..., requirementItem}] +
//           requiredBloodline; NOT_FOUND when the id is absent.
// Responses use the superjson batch shape [{result:{data:{json}}}] / [{error:{json}}].

const it = (id, o = {}) => ({
  id, name: o.name ?? `Item ${id}`, itemType: "WEAPON", rarity: "COMMON", slot: "HAND",
  hidden: false, canBeCrafted: false, canBeHunted: false, canBeGathered: false,
  canBeTraded: false, canBeImbued: false, inShop: false, isEventItem: false,
  cost: 10, repsCost: 0, seichiSilverCost: 0, stackSize: 1, requiredLevel: 1,
  craftingExperience: 0, parentItemId: null, bloodlineId: null, effects: [], ...o,
});

/** A small world exercising every flag the builder knows. */
export function seedWorld() {
  const items = [
    // ingredients
    it("ing-ore", { name: "Iron Ore", itemType: "MATERIAL", slot: "ITEM", canBeGathered: true, cost: 1 }),
    it("ing-herb", { name: "Moon Herb", itemType: "MATERIAL", slot: "ITEM", canBeHunted: true, cost: 2 }),
    it("ing-secret", { name: "Sealed Shard", itemType: "MATERIAL", slot: "ITEM", hidden: true, cost: 3 }),
    it("ing-thread", { name: "Silver Thread", itemType: "MATERIAL", slot: "ITEM", canBeCrafted: true, cost: 4 }),
    // craftable, visible
    it("c-blade", { name: "Iron Blade", canBeCrafted: true, cost: 50, craftingExperience: 100 }),
    it("c-tonic", { name: "Field Tonic", itemType: "CONSUMABLE", slot: "ITEM", rarity: "RARE", canBeCrafted: true, cost: 20 }),
    it("c-stew", { name: "Hunter Stew", itemType: "COOKING", slot: "ITEM", canBeCrafted: true, cost: 5 }),
    it("c-empty", { name: "Unfinished Charm", itemType: "ACCESSORY", slot: "ITEM", canBeCrafted: true, cost: 30 }),
    it("c-ghost", { name: "Ghost Ref Mail", itemType: "ARMOR", slot: "CHEST", canBeCrafted: true, cost: 40 }),
    it("c-evo", { name: "Iron Blade II", canBeCrafted: true, parentItemId: "c-blade", cost: 60 }),
    it("c-neg", { name: "Debt Token", itemType: "MATERIAL", slot: "ITEM", canBeCrafted: true, cost: -5 }),
    // craftable, hidden
    it("h-crown", { name: "Storm Crown", itemType: "ARMOR", slot: "HEAD", rarity: "LEGENDARY", hidden: true, canBeCrafted: true, cost: 900, bloodlineId: "bl-1" }),
    it("h-dup", { name: "Twin Seal", itemType: "ACCESSORY", slot: "ITEM", rarity: "EPIC", hidden: true, canBeCrafted: true, cost: 70 }),
    it("h-self", { name: "Mirror Shard", itemType: "MATERIAL", slot: "ITEM", hidden: true, canBeCrafted: true, cost: 80 }),
    // not craftable decoys
    it("x-sword", { name: "Shop Sword", cost: 15, inShop: true }),
    it("x-hidden", { name: "Hidden Decoy", hidden: true, cost: 16 }),
  ];
  const reqs = [
    ["c-blade", "ing-ore", 4], ["c-blade", "ing-thread", 1],
    ["c-tonic", "ing-herb", 3],
    ["c-stew", "ing-herb", 2], ["c-stew", "ing-ore", 1],
    ["c-ghost", "deleted-item", 2], ["c-ghost", "ing-ore", 5],
    ["c-evo", "ing-ore", 7],
    ["c-neg", "ing-ore", 1],
    ["h-crown", "ing-secret", 12], ["h-crown", "ing-thread", 3],
    ["h-dup", "ing-herb", 2], ["h-dup", "ing-herb", 3],
    ["h-self", "h-self", 1], ["h-self", "ing-secret", 2],
    ["ing-thread", "ing-herb", 5],
  ].map(([craftItemId, requirementItemId, quantity], i) => ({
    id: `req-${i}`, craftItemId, requirementItemId, quantity,
  }));
  const bloodlines = { "bl-1": { id: "bl-1", name: "Storm Blood", hidden: false } };
  return { items, reqs, bloodlines };
}

const ok = (json) => ({ status: 200, body: [{ result: { data: { json } } }] });
const err = (code, httpStatus, message) => ({
  status: httpStatus,
  body: [{ error: { json: { message, code: -32600, data: { code, httpStatus } } } }],
});

/**
 * Build a fake fetch. `faults` maps request number (1-based) to a response override:
 * {status, body} | "network". `onRequest(n, world)` may mutate the world between requests.
 */
export function fakeFetch(world, { faults = {}, onRequest } = {}) {
  const calls = [];
  const fetch = async (url, init) => {
    const n = calls.length + 1;
    calls.push({ url, init });
    if (onRequest) onRequest(n, world);
    const f = faults[n];
    if (f === "network") throw new TypeError("Failed to fetch");
    const res = f ?? route(world, url, init);
    const text = typeof res.body === "string" ? res.body : JSON.stringify(res.body);
    return { status: res.status, text: async () => text };
  };
  return { fetch, calls };
}

function route(world, url, init) {
  if (init?.method !== "GET") return err("METHOD_NOT_SUPPORTED", 405, "GET only");
  const u = new URL(url);
  const m = u.pathname.match(/^\/api\/trpc\/([^/]+)$/);
  if (!m || u.searchParams.get("batch") !== "1") return err("NOT_FOUND", 404, "no route");
  const input = JSON.parse(u.searchParams.get("input"))["0"].json;
  if (m[1] === "item.getAll") return getAll(world, input);
  if (m[1] === "item.getItemWithCraftingRequirements") return detail(world, input);
  return err("NOT_FOUND", 404, `No procedure ${m[1]}`);
}

function getAll(world, input) {
  if (typeof input.limit !== "number" || input.limit < 1 || input.limit > 500) {
    return err("BAD_REQUEST", 400, "limit");
  }
  const cursor = input.cursor ? input.cursor : 0;
  const hidden = input.hidden !== undefined ? input.hidden : false;
  const rows = world.items
    .filter((r) => r.hidden === hidden)
    .filter((r) => input.canBeCrafted === undefined || r.canBeCrafted === input.canBeCrafted)
    .filter((r) => r.cost >= (input.minCost ?? 0))
    .filter((r) => r.repsCost >= (input.minRepsCost ?? 0))
    .filter((r) => r.seichiSilverCost >= (input.minSeichiSilverCost ?? 0))
    .sort((a, b) => a.cost - b.cost || a.repsCost - b.repsCost || (a.id < b.id ? -1 : a.id > b.id ? 1 : 0))
    .slice(cursor * input.limit, cursor * input.limit + input.limit);
  return ok({ data: rows, nextCursor: rows.length < input.limit ? null : cursor + 1 });
}

function detail(world, input) {
  const row = world.items.find((r) => r.id === input.id);
  if (!row) return err("NOT_FOUND", 404, "Item not found");
  const byId = new Map(world.items.map((r) => [r.id, r]));
  return ok({
    ...row,
    craftingRequirements: world.reqs
      .filter((q) => q.craftItemId === row.id)
      .map((q) => ({ ...q, requirementItem: byId.get(q.requirementItemId) ?? null })),
    requiredBloodline: row.bloodlineId ? world.bloodlines[row.bloodlineId] ?? null : null,
  });
}

export { ok, err };

/** Deterministic env: virtual clock (sleep advances it), structured-clone store, captured logs. */
export function fakeEnv(fetch, { store, t0 = 1790000000000, hostname = "www.theninja-rpg.com" } = {}) {
  let t = t0;
  const mem = store ?? new Map();
  const logs = [];
  const downloads = [];
  return {
    env: {
      origin: `https://${hostname}`,
      hostname,
      fetch,
      now: () => t,
      sleep: async (ms) => { t += Math.max(0, Math.ceil(ms)); },
      store: {
        get: async (k) => (mem.has(k) ? structuredClone(mem.get(k)) : undefined),
        set: async (k, v) => { mem.set(k, structuredClone(v)); },
        del: async (k) => { mem.delete(k); },
      },
      log: (m) => logs.push(m),
      download: (name, text) => downloads.push({ name, text }),
    },
    mem, logs, downloads,
    advance: (ms) => { t += ms; },
  };
}
