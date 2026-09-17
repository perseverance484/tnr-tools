// Cache-first reads under the budget (spec section 6, requirement 1). Every read goes:
// capture cache -> (miss) budget.acquire -> transport -> cache.put -> budget.observe.
// Ok results are cached BEFORE observe() may throw for a limited index, so a 207 that hides
// one 429 still keeps the other answers.

import { procedure } from "../transport/procedures.mjs";
import { canonicalInput, canonicalKey, pointInput, pageContract, pageInput, pageSize, requireRow, MAX_PAGES } from "../research/registry.mjs";

/**
 * The input for a point read. It is now the registry's canonical input rather than a second table
 * of shapes kept here: one representation feeds cache identity, transport and stored provenance
 * (Phase 1 requirement 7.3), so there is no way for the id Forge caches under to differ from the
 * one it actually sent. The key that names the record (`id`, or `userId` for profile.getAi) comes
 * off the audited row.
 */
export function readInput(path, id) { return pointInput(path, id); }

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

  // ---------------------------------------------------------------- filtered / paged query reads
  /**
   * ONE page of a filtered or paged query, cache-first. The canonical input is both what is sent
   * and what the cache row is keyed and stamped with, so the stored provenance is the request by
   * construction rather than by a parallel bookkeeping step that could drift.
   *
   * Returns the decoded element with `input` (exactly what was sent) and `key` (its cache identity)
   * attached, so a caller can journal the request without rebuilding it.
   */
  async _page(path, canonical, { fresh = false } = {}) {
    const key = canonicalKey(canonical);
    if (!fresh) {
      const hit = await this.cache.getQuery(path, key);
      if (hit) { this.stats.hits++; return { ok: true, data: hit.data, cached: true, at: hit.at, input: canonical, key }; }
    }
    this.stats.misses++;
    await this.budget.acquire(path, 1);
    this.stats.requests++;
    // The exact canonical object is what goes on the wire. `null` means the audited contract takes
    // no input at all, which tRPC expects as `undefined`, not as an empty object.
    const [r] = await this.client.batch([{ path, input: canonical === null ? undefined : canonical }]);
    if (r.ok) await this.cache.putQuery({ path, queryKey: key, input: canonical, data: r.data });
    // observe() may throw RateLimited; the ok body above is already cached, exactly as in getMany.
    this.budget.observe([r], [path]);
    return { ...r, input: canonical, key };
  }

  /**
   * A filtered and optionally paged read of one audited research procedure.
   *
   * `pages` is an explicit bound and there is no mode in which it is absent: a walk stops at the
   * requested page count, at the registry's MAX_PAGES ceiling, at the first short page, or at the
   * first page that is not ok — whichever comes first. Nothing here loops until the server runs out.
   *
   * The result is deliberately not collapsible to "it worked". `pages[]` keeps one honest record per
   * request — its exact input, whether it was served from cache, its row count and its error — and
   * `complete` is false whenever the walk stopped for any reason other than reaching the natural end
   * of the data. A partial or failed page therefore cannot be re-read later as a whole answer
   * (requirement 7.8).
   */
  async query(path, input, { fresh = false, pages = 1 } = {}) {
    // Admission comes FIRST, so an unapproved path gets the refusal that names why rather than
    // whatever the next check happens to say about it. Nothing is built or sent before this.
    requireRow(path);
    if (procedure(path).kind !== "query") throw new Error("query is for queries: " + path);
    const canonical = canonicalInput(path, input);
    const paged = pageContract(path);
    // Validate what was ASKED FOR before clamping it. Clamping first would silently turn "walk two
    // pages of an unpaged procedure" into a legal one-page read instead of refusing it.
    const asked = Number.isInteger(pages) && pages > 0 ? pages : 1;
    if (asked > 1 && !paged) throw new Error(`${path} is not paged at source; it cannot read ${asked} pages`);
    const want = Math.min(asked, paged ? MAX_PAGES : 1);
    if (paged && canonical && canonical[paged.limitKey] > paged.maxLimit) {
      throw new Error(`${path}: ${paged.limitKey} ${canonical[paged.limitKey]} is over the audited maximum of ${paged.maxLimit}`);
    }
    const size = paged ? pageSize(path, canonical) : null;
    const out = [];
    const rows = [];
    for (let n = 0; n < want; n++) {
      const pin = n === 0 ? canonical : pageInput(path, canonical, n);
      const r = await this._page(path, pin, { fresh });
      const count = Array.isArray(r.data) ? r.data.length : r.data == null ? 0 : 1;
      out.push({ n, input: pin, key: r.key, ok: r.ok, cached: !!r.cached, rows: count, at: r.at ?? null, error: r.ok ? null : r.error.code });
      if (!r.ok) {
        return { ok: false, complete: false, error: r.error, pages: out, data: null, tierPath: path, rowCount: rows.length };
      }
      if (Array.isArray(r.data)) rows.push(...r.data); else if (n === 0) rows.push(r.data);
      // A page shorter than the page size is the end of the data, and the only honest way to call a
      // walk complete without asking for a page that does not exist.
      if (!paged || !Array.isArray(r.data) || r.data.length < size) {
        return { ok: true, complete: true, pages: out, data: paged ? rows : r.data, rowCount: paged ? rows.length : count };
      }
    }
    // Ran out of the caller's page budget on a full page: there is more data and this is NOT the
    // whole answer, so it is reported as an incomplete walk rather than as a result.
    return { ok: true, complete: !paged, pages: out, data: paged ? rows : rows[0], rowCount: paged ? rows.length : 1, bounded: `stopped at the declared bound of ${want} page(s) on a full page; more rows exist` };
  }
}
