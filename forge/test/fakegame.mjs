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
const TABLE = { jutsu: "jutsu", item: "item", bloodline: "bloodline", gameAsset: "asset", quests: "quest", profile: "ai", ai: "aiProfile" };
const ID_KEY = { ai: "userId" };

export class FakeGame {
  constructor({ crashAt = Infinity, refuse = new Set(), limitPath = null } = {}) {
    this.tables = { jutsu: new Map(), item: new Map(), bloodline: new Map(), asset: new Map(), quest: new Map(), ai: new Map(), aiProfile: new Map() };
    this.calls = [];
    this.crashAt = crashAt;
    this.refuse = refuse;        // set of paths that answer success:false
    this.limitPath = limitPath;  // a path that answers TOO_MANY_REQUESTS
    this.armed = true;
  }
  count(entity) { return this.tables[entity].size; }
  rows(entity) { return [...this.tables[entity].values()]; }
  seed(entity, row) { const k = ID_KEY[entity] ?? "id"; this.tables[entity].set(row[k], row); return row; }

  /** Handle one procedure call; returns a decoded element. */
  handle(path, input) {
    const n = this.calls.push({ path, input });
    const [router, proc] = path.split(".");
    const table = this.tables[TABLE[router]];
    const ok = (data) => ({ ok: true, data });
    const err = (code, message, httpStatus) => ({ ok: false, error: { code, httpStatus, message, path, zodError: null } });
    let result;
    if (this.limitPath === path) return err("TOO_MANY_REQUESTS", "You are moving too fast! Incident logged for review", 429);
    if (PLACEHOLDER[path]) {
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
             if (router === "profile") { if (jutsus) row.jutsus = jutsus.map((j) => ({ jutsuId: j })); if (items) row.items = items.flatMap((t) => t.ids.map((i) => ({ itemId: i, quantity: t.number }))); }
             result = ok({ success: true, message: `Updated ${input.id}` }); }
    } else if (proc === "getAllNames" || proc === "getAllAiNames") {
      const k = ID_KEY[TABLE[router]] ?? "id", nk = TABLE[router] === "ai" ? "username" : "name";
      result = ok([...table.values()].map((r) => ({ [k]: r[k], [nk]: r[nk] })));
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
      else { p.rules = structuredClone(input.rules); p.includeDefaultRules = input.includeDefaultRules; result = ok({ success: true, message: "Rules updated" }); }
    } else {
      result = err("NOT_FOUND", "unknown procedure " + path, 404);
    }
    // the request was applied server-side; now maybe the tab dies before the response is seen
    if (n >= this.crashAt && this.armed) { this.armed = false; throw new CrashSignal(n); }
    return result;
  }
}

/** A Session-less TrpcClient stand-in with the same batch()/call() surface, backed by FakeGame. */
export class FakeClient {
  constructor(game) { this.game = game; }
  async call(path, input) { const [r] = await this.batch([{ path, input }]); return r; }
  async batch(calls) { return calls.map((c) => this.game.handle(c.path, c.input)); }
}

export { Session, TrpcClient };
