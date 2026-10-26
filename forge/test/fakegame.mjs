// An in-memory game that answers like TrpcClient.batch() would (decoded elements), with the
// create/update/get/getAllNames semantics read at source: create inserts a placeholder and
// returns the id in message; update merges; get returns the row. Records every call, and can
// CRASH (throw) at a chosen call number to simulate tab eviction mid-flight: the call has
// been applied server-side (the request left) but the client never sees the response.
//
// This is what lets the runner tests assert "resume never double-creates" against actual
// server-side row counts, which is the point of the project.

import { Session } from "../src/transport/session.mjs";
import { TrpcClient } from "../src/transport/client.mjs";
import { isProtected } from "../src/transport/procedures.mjs";
import { NetworkError } from "../src/transport/client.mjs";

let seq = 0;
export const nanoidLike = () => ("fk" + String(++seq).padStart(19, "0")).slice(0, 21);

export class CrashSignal extends Error { constructor(n) { super("crash at call " + n); this.name = "CrashSignal"; } }

const PLACEHOLDER = {
  "jutsu.create": (id) => ({ id, name: `New Jutsu - ${id}`, description: "New jutsu description", hidden: true, effects: [], createdAt: new Date(0), updatedAt: new Date(0) }),
  "item.create": (id, input) => ({ id, name: `New Item - ${id}`, itemType: input?.type ?? "CONSUMABLE", hidden: true, effects: [], createdAt: new Date(0), updatedAt: new Date(0) }),
  "bloodline.create": (id) => ({ id, name: `New Bloodline - ${id}`, hidden: true, effects: [], createdAt: new Date(0), updatedAt: new Date(0) }),
  "gameAsset.create": (id) => ({ id, name: "Placeholder", type: "STATIC", image: "", url: "", hidden: true, createdAt: new Date(0), updatedAt: new Date(0) }),
  "quests.create": (id) => ({ id, name: `New Quest - ${id}`, hidden: true, content: { objectives: [], reward: {}, sceneBackground: "", sceneCharacters: [] }, createdAt: new Date(0), updatedAt: new Date(0) }),
  "profile.create": (id) => ({ userId: id, username: `New AI - ${id}`, isAi: true, level: 1, rank: "STUDENT", aiProfileId: null, jutsus: [], items: [], createdAt: new Date(0), updatedAt: new Date(0) }),
};
const TABLE = { jutsu: "jutsu", item: "item", bloodline: "bloodline", gameAsset: "asset", quests: "quest", profile: "ai", ai: "aiProfile", dungeon: "dungeon" };
const ID_KEY = { ai: "userId" };

/**
 * Rebuild every object in a payload with its keys in a DIFFERENT order, the way zod re-emits a
 * validated document in schema order rather than the order the client sent. Semantically the same
 * document, structurally re-keyed - which is precisely what turned 18 landed Godstorm AI-profile
 * writes into reported "drift" against a JSON.stringify comparison
 * (harvests/inbox/tnr_results_1789829183863.json: every recorded rules diff parses equal).
 * Reversing is the cheapest re-keying that is deterministic and always different for >1 key.
 */
export const rekey = (v) => (Array.isArray(v) ? v.map(rekey)
  : v && typeof v === "object" && !(v instanceof Date)
    ? Object.fromEntries(Object.keys(v).reverse().map((k) => [k, rekey(v[k])]))
    : v);

export class FakeGame {
  constructor({ crashAt = Infinity, dropAt = Infinity, refuse = new Set(), limitPath = null, signedOut = false } = {}) {
    this.tables = { jutsu: new Map(), item: new Map(), bloodline: new Map(), asset: new Map(), quest: new Map(), ai: new Map(), aiProfile: new Map(), dungeon: new Map() };
    this.calls = [];
    this.crashAt = crashAt;
    // the connection fails at this call BEFORE the server applies it: nothing is written
    this.dropAt = dropAt;
    this.refuse = refuse;        // set of paths that answer success:false
    this.limitPath = limitPath;  // a path that answers TOO_MANY_REQUESTS
    // No Clerk session: every protectedProcedure answers UNAUTHORIZED before its resolver runs,
    // which is what enforceUserIsAuthed does at source (trpc.ts:213-216) and what the two failed
    // Forge 0.3.0 runs saw five times each. Public procedures are unaffected, exactly as they are
    // live: that asymmetry is the thing the auth tests exist to pin down.
    this.signedOut = signedOut;
    this.armed = true;
  }
  signOut() { this.signedOut = true; return this; }
  signIn() { this.signedOut = false; return this; }
  count(entity) { return this.tables[entity].size; }
  rows(entity) { return [...this.tables[entity].values()]; }
  seed(entity, row) { const k = ID_KEY[entity] ?? "id"; this.tables[entity].set(row[k], row); return row; }

  /** Handle one procedure call; returns a decoded element. */
  handle(path, input) {
    const n = this.calls.push({ path, input });
    if (n === this.dropAt) throw new NetworkError("connection reset before the request was applied");
    // Nested routers: root.ts mounts coopRouter at `coop`, and coop.ts mounts dungeonRouter at
    // `dungeon`. A bare "dungeon.*" path does not exist on the server (NOT_FOUND, as live on 2026-10-25).
    const nested = path.startsWith("coop.dungeon.");
    const [router, proc] = nested ? ["dungeon", path.slice("coop.dungeon.".length)] : path.split(".");
    if (!nested && router === "dungeon") return { ok: false, error: { code: "NOT_FOUND", httpStatus: 404, message: `No procedure found on path "${path}"`, path, zodError: null } };
    const table = this.tables[TABLE[router]];
    const ok = (data) => ({ ok: true, data });
    const err = (code, message, httpStatus) => ({ ok: false, error: { code, httpStatus, message, path, zodError: null } });
    let result;
    if (this.limitPath === path) return err("TOO_MANY_REQUESTS", "You are moving too fast! Incident logged for review", 429);
    if (this.signedOut && isProtected(path)) return err("UNAUTHORIZED", `UNAUTHORIZED: Data: ${JSON.stringify(input ?? null)}`, 401);
    if (router === "dungeon") result = this.dungeon(proc, input, ok, err);
    else if (PLACEHOLDER[path]) {
      if (this.refuse.has(path)) result = ok({ success: false, message: `Not allowed to create` });
      else { const id = nanoidLike(); const row = PLACEHOLDER[path](id, input); table.set(id, row); result = ok({ success: true, message: id }); }
    } else if (proc === "get" || proc === "getAi") {
      const id = input.id ?? input.userId;
      const row = table.get(id);
      result = row ? ok(structuredClone(row)) : (proc === "getAi" ? ok(null) : err("NOT_FOUND", `${router} not found`, 404));
    } else if (proc === "update" || proc === "updateAi") {
      const row = table.get(input.id);
      if (!row) result = ok({ success: false, message: `${router} not found` });
      else if (this.refuse.has(path)) result = ok({ success: false, message: "Not allowed" });
      else { const { jutsus, items, ...rest } = input.data; Object.assign(row, rest, { updatedAt: new Date(1) });
             if (router === "profile") { if (jutsus) row.jutsus = jutsus.map((j) => ({ jutsuId: j })); if (items) row.items = items.flatMap((t) => t.ids.map((i) => ({ itemId: i, quantity: (row.items ?? []).find((r) => r.itemId === i)?.quantity ?? 1, dropChancePerc: Number(t.number) }))); }
             result = ok({ success: true, message: `Updated ${input.id}` }); }
    } else if (proc === "getAllNames" || proc === "getAllAiNames") {
      // The name lists are NOT input-shape-equivalent. Only gameAsset.getAllNames declares an
      // .input(), z.object({type?, folderPrefix?}), and that object schema is not itself
      // .optional() (45f_DATA_procedures.json, routers/asset.getAllNames @ TheNinjaRPG bdec2883),
      // so an absent input fails zod before the resolver runs. That is the live BAD_REQUEST that
      // killed the three Godstorm Stormcourt asset creates at their pre-create snapshot; the
      // other lists declare no input and ignore whatever arrives.
      if (path === "gameAsset.getAllNames" && (input === null || typeof input !== "object" || Array.isArray(input))) {
        return err("BAD_REQUEST", "[{\"code\":\"invalid_type\",\"expected\":\"object\",\"received\":\"undefined\",\"path\":[],\"message\":\"Required\"}]", 400);
      }
      const k = ID_KEY[TABLE[router]] ?? "id", nk = TABLE[router] === "ai" ? "username" : "name";
      let rows = [...table.values()];
      if (path === "gameAsset.getAllNames" && input.type) rows = rows.filter((r) => r.type === input.type);
      const name = (r) => (path === "gameAsset.getAllNames" && input.folderPrefix ? `${r.folder ?? ""}/${r[nk]}` : r[nk]);
      result = ok(rows.map((r) => ({ [k]: r[k], [nk]: name(r) })));
    } else if (path === "ai.getAiProfile") {
      const p = this.tables.aiProfile.get(input.id); result = p ? ok(structuredClone(p)) : err("NOT_FOUND", "profile not found", 404);
    } else if (path === "ai.toggleAiProfile") {
      const ai = this.tables.ai.get(input.aiId);
      if (!ai) result = ok({ success: false, message: "AI not found" });
      else if (ai.aiProfileId) { this.tables.aiProfile.delete(ai.aiProfileId); ai.aiProfileId = null; result = ok({ success: true, message: "Profile removed" }); }
      else { const pid = nanoidLike(); this.tables.aiProfile.set(pid, { id: pid, userId: input.aiId, rules: [], includeDefaultRules: true }); ai.aiProfileId = pid; result = ok({ success: true, message: "Profile created" }); }
    } else if (path === "ai.updateAiProfile") {
      const p = this.tables.aiProfile.get(input.id);
      if (!p) result = ok({ success: false, message: "profile not found" });
      // stored as the server stores it: same document, schema key order (see rekey above)
      else { p.rules = rekey(structuredClone(input.rules)); p.includeDefaultRules = input.includeDefaultRules; result = ok({ success: true, message: "Rules updated" }); }
    } else {
      result = err("NOT_FOUND", "unknown procedure " + path, 404);
    }
    // the request was applied server-side; now maybe the tab dies before the response is seen
    if (n >= this.crashAt && this.armed) { this.armed = false; throw new CrashSignal(n); }
    return result;
  }
}

/**
 * coop.dungeon.getAll / coop.dungeon.save as routers/dungeon.ts answers at the pin in src/dungeon/contract.json:
 * getAll returns whole rows {id, content, updatedAt} (an empty list for non-staff); save without
 * an id creates, with an id upserts the WHOLE content, and answers {success, message, id}.
 *
 * The save input is parsed the way saveDungeonSchema parses it, written out here independently of
 * Forge's validator: unknown keys are STRIPPED at every level (zod objects are not strict), the
 * name is trimmed, `.prefault()` defaults fill only undefined members (an explicit null is a
 * BAD_REQUEST), and expiresAt is z.coerce.date(). Then the resolver: every package drop's sent
 * payload is dropped and the CURRENT catalog row (`game.packages`) is copied in; a missing one is
 * refused. The row is stored through JSON (the content column is json), so a Date reads back as
 * its ISO string, in schema key order (rekey).
 */
const DUNGEON_KEYS = {
  content: ["name", "description", "structureAssetId", "structureScale", "sector", "longitude", "latitude", "expiresAt", "hidden", "background", "tiers", "rewards"],
  rewards: ["money", "experience", "tokens", "prestige", "drops"], drop: ["type", "id", "chance", "quantity", "package"],
  floor: ["kind", "waves"], wave: ["aiIds", "delayRounds"],
};
class ZodIssue extends Error { constructor(path, message) { super(message); this.path = path; } }
function parseDungeon(content) {
  const pick = (o, keys, where) => {
    if (!o || typeof o !== "object" || Array.isArray(o)) throw new ZodIssue(where, "Expected object");
    return Object.fromEntries(keys.filter((k) => o[k] !== undefined).map((k) => [k, o[k]]));
  };
  const prefault = (o, k, v, where) => { if (o[k] === null) throw new ZodIssue([...where, k], "Expected value, received null"); if (o[k] === undefined) o[k] = v; };
  const c = pick(content, DUNGEON_KEYS.content, ["content"]);
  if (typeof c.name !== "string" || !c.name.trim()) throw new ZodIssue(["content", "name"], "Enter a dungeon name.");
  c.name = c.name.trim();
  for (const [k, v] of [["description", ""], ["structureAssetId", ""], ["structureScale", 1], ["hidden", true], ["background", "default"]]) prefault(c, k, v, ["content"]);
  if (!("expiresAt" in c)) throw new ZodIssue(["content", "expiresAt"], "Required");
  if (c.expiresAt !== null) { const d = new Date(c.expiresAt); if (Number.isNaN(d.getTime())) throw new ZodIssue(["content", "expiresAt"], "Invalid date"); c.expiresAt = d; }
  c.tiers = (c.tiers ?? []).map((t, ti) => t.map((f, fi) => {
    const floor = pick(f, DUNGEON_KEYS.floor, ["content", "tiers", ti, fi]);
    floor.waves = floor.waves.map((w, wi) => { const wave = pick(w, DUNGEON_KEYS.wave, ["content", "tiers", ti, fi, "waves", wi]); prefault(wave, "delayRounds", 0, ["content", "tiers", ti, fi, "waves", wi]); return wave; });
    return floor;
  }));
  c.rewards = pick(c.rewards, DUNGEON_KEYS.rewards, ["content", "rewards"]);
  for (const k of ["money", "experience", "tokens", "prestige"]) prefault(c.rewards, k, 0, ["content", "rewards"]);
  prefault(c.rewards, "drops", [], ["content", "rewards"]);
  c.rewards.drops = c.rewards.drops.map((d, i) => { const drop = pick(d, DUNGEON_KEYS.drop, ["content", "rewards", "drops", i]); prefault(drop, "quantity", 1, ["content", "rewards", "drops", i]); return drop; });
  return c;
}

FakeGame.prototype.dungeon = function (proc, input, ok, err) {
  const table = this.tables.dungeon;
  if (proc === "getAll") return ok(this.notStaff ? [] : [...table.values()].map((r) => structuredClone(r)));
  if (proc !== "save") return err("NOT_FOUND", "unknown procedure dungeon." + proc, 404);
  let c;
  try { c = parseDungeon(input.content); } catch (e) {
    if (!(e instanceof ZodIssue)) throw e;
    return { ok: false, error: { code: "BAD_REQUEST", httpStatus: 400, message: e.message, path: "coop.dungeon.save", zodError: [{ path: e.path, message: e.message }] } };
  }
  if (this.notStaff) return ok({ success: false, message: "You cannot edit dungeons." });
  if (this.refuse.has("coop.dungeon.save")) return ok({ success: false, message: "An enemy or reward no longer exists." });
  const packages = this.packages ?? new Map();
  if (c.rewards.drops.some((d) => d.type === "package" && !packages.has(d.id))) return ok({ success: false, message: "An enemy or reward no longer exists." });
  c.rewards.drops = c.rewards.drops.map(({ package: _ignored, ...d }) => {
    const src = d.type === "package" ? packages.get(d.id) : null;
    return src ? { ...d, package: { name: src.name, description: src.description, rewards: structuredClone(src.rewards) } } : d;
  });
  const id = input.id ?? nanoidLike();
  table.set(id, { id, content: rekey(JSON.parse(JSON.stringify(c))), updatedAt: new Date(1) });
  return ok({ success: true, message: "Dungeon saved.", id });
};

/** A Session-less TrpcClient stand-in with the same batch()/call() surface, backed by FakeGame. */
export class FakeClient {
  constructor(game) { this.game = game; }
  async call(path, input) { const [r] = await this.batch([{ path, input }]); return r; }
  async batch(calls) { return calls.map((c) => this.game.handle(c.path, c.input)); }
}

export { Session, TrpcClient };
