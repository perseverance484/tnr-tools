// Cache-first reads under the budget (spec section 6, requirement 1). Every read goes:
// capture cache -> (miss) budget.acquire -> transport -> cache.put -> budget.observe.
// Ok results are cached BEFORE observe() may throw for a limited index, so a 207 that hides
// one 429 still keeps the other answers.

import { procedure } from "../transport/procedures.mjs";

// Input shape per read path. Everything takes {id} except the AI record read.
// Source: profile.ts:1121 getAi .input(z.object({ userId })), everything else .input(z.object({ id })).
const INPUT_FOR = Object.freeze({
  "profile.getAi": (id) => ({ userId: id }),
});
export function readInput(path, id) {
  const f = INPUT_FOR[path];
  return f ? f(id) : { id };
}

export class CachedReader {
  constructor({ client, cache, budget, maxBatch = 20 }) {
    this.client = client; this.cache = cache; this.budget = budget; this.maxBatch = maxBatch;
    this.stats = { hits: 0, misses: 0, requests: 0 };
  }

  /** One record, cache-first. Returns the decoded element {ok, data|error}. */
  async get(path, id, { fresh = false } = {}) {
    const [r] = await this.getMany(path, [id], { fresh });
    return r;
  }

  /**
   * Many records of one path, cache-first, batched under the budget. Returns decoded elements
   * in id order. Throws RateLimited if the server trips (after caching whatever succeeded).
   */
  async getMany(path, ids, { fresh = false } = {}) {
    if (procedure(path).kind !== "query") throw new Error("getMany is for queries: " + path);
    const out = new Array(ids.length);
    const misses = [];
    for (let i = 0; i < ids.length; i++) {
      const hit = fresh ? null : await this.cache.get(path, ids[i]);
      if (hit) { this.stats.hits++; out[i] = { ok: true, data: hit.data, cached: true, at: hit.at }; }
      else { this.stats.misses++; misses.push(i); }
    }
    // chunk misses by what the budget can hand out at once and by maxBatch
    let pos = 0;
    while (pos < misses.length) {
      // on a limited path, never put more in one request than the window has room for right
      // now, and never more than 10: at the limiter edge each element over the limit is a
      // separate 1% penalty, so a small chunk bounds the blast radius if the margin is wrong.
      // With no room at all, acquire() waits; then ask for a full capped chunk, not one id.
      let room = this.maxBatch;
      if (this.budget.isLimited(path)) {
        const cap = Math.min(this.maxBatch, 10, this.budget.allowance);
        const avail = this.budget.available(path);
        room = avail > 0 ? Math.min(cap, avail) : cap;
      }
      const idxs = misses.slice(pos, pos + room);
      await this.budget.acquire(path, idxs.length);
      this.stats.requests++;
      const results = await this.client.batch(idxs.map((i) => ({ path, input: readInput(path, ids[i]) })));
      // cache ok results first, then let observe() throw if any index was limited
      for (let j = 0; j < idxs.length; j++) {
        const r = results[j];
        out[idxs[j]] = r;
        if (r.ok) await this.cache.put({ path, id: ids[idxs[j]], input: readInput(path, ids[idxs[j]]), data: r.data });
      }
      this.budget.observe(results, idxs.map(() => path));
      pos += idxs.length;
    }
    return out;
  }

  /** A list procedure (getAll / getAllNames / getAllAiNames): cached under id "". */
  async list(path, { fresh = false } = {}) {
    if (procedure(path).kind !== "query") throw new Error("list is for queries: " + path);
    // getAll takes a required {limit, cursor} input (jutsu.ts:266-285); only the name lists take none
    if (!/\.getAll(Ai)?Names$/.test(path)) throw new Error("list() is for getAllNames/getAllAiNames; " + path + " needs a paged input");
    const hit = fresh ? null : await this.cache.get(path, "");
    if (hit) { this.stats.hits++; return { ok: true, data: hit.data, cached: true, at: hit.at }; }
    this.stats.misses++;
    await this.budget.acquire(path, 1);
    this.stats.requests++;
    const [r] = await this.client.batch([{ path, input: undefined }]);
    if (r.ok) await this.cache.put({ path, id: "", input: null, data: r.data });
    this.budget.observe([r], [path]);
    return r;
  }
}
