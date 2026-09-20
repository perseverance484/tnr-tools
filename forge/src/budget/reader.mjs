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

/**
 * The input a list procedure must be called with when the caller asks for no filter: the registry's
 * canonical input for an EMPTY request. Five name lists declare no `.input()` at source and get
 * `undefined`; gameAsset.getAllNames declares `z.object({type?, folderPrefix?})` with the OBJECT
 * required, so it gets `{}` - the shape whose absence was the live BAD_REQUEST that killed the
 * Godstorm Stormcourt creates at their pre-create name snapshot (harvests/inbox/
 * tnr_results_1789829183863.json, items 0-2 and 27; asset.ts:50-57 at the pin).
 *
 * Derived from the audited row rather than kept as a second table here, so the shape Forge sends
 * for a bare list and the shape the research registry validates a capture against cannot disagree.
 * The members are deliberately NOT defaulted: dedupNames and the pre-create reconciliation snapshot
 * need the unfiltered list under the plain `name`, and `folderPrefix: true` would hand back
 * "folder/Name" and make every live name look new.
 */
export function listInput(path) { return canonicalInput(path, undefined) ?? undefined; }

// Order-insensitive structural comparison, used only to decide whether a caller's list input is
// the default one. Keys are sorted and undefined-valued keys dropped, so {} and {type: undefined}
// are the same request.
function stableInput(v) {
  if (Array.isArray(v)) return "[" + v.map(stableInput).join(",") + "]";
  if (v && typeof v === "object") {
    return "{" + Object.keys(v).filter((k) => v[k] !== undefined).sort()
      .map((k) => JSON.stringify(k) + ":" + stableInput(v[k])).join(",") + "}";
  }
  return v === undefined ? "undefined" : JSON.stringify(v) ?? "null";
}
function sameInput(a, b) { return a === b || stableInput(a) === stableInput(b); }

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

  /**
   * A list procedure (getAllNames / getAllAiNames): cached under id "".
   *
   * The wire input is listInput(path) unless the caller supplies one. A caller-supplied input is
   * a FILTER (a capture's {type, folderPrefix}), and it answers a different question than the
   * default list does, so it is neither served from nor written into the single id-"" cache slot:
   * one slot per path cannot hold two different answers, and the write-invalidation rule reads
   * that slot by its empty id. A filtered list therefore always costs one token and is always
   * fresh, which is the safe direction for a read whose whole purpose is evidence.
   */
  async list(path, { fresh = false, input } = {}) {
    if (procedure(path).kind !== "query") throw new Error("list is for queries: " + path);
    // getAll takes a required {limit, cursor} input (jutsu.ts:266-285); only the name lists take none
    if (!/\.getAll(Ai)?Names$/.test(path)) throw new Error("list() is for getAllNames/getAllAiNames; " + path + " needs a paged input");
    const sent = input === undefined ? listInput(path) : input;
    const cacheable = sameInput(sent, listInput(path));
    const hit = fresh || !cacheable ? null : await this.cache.get(path, "");
    if (hit) { this.stats.hits++; return { ok: true, data: hit.data, cached: true, at: hit.at }; }
    this.stats.misses++;
    await this.budget.acquire(path, 1);
    this.stats.requests++;
    const [r] = await this.client.batch([{ path, input: sent }]);
    if (r.ok && cacheable) await this.cache.put({ path, id: "", input: sent ?? null, data: r.data });
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
    // When it does throw, the decoded element is already in hand and would otherwise be lost with
    // the stack, so it rides on the error. That is what lets the walk above report the page that
    // tripped the limiter instead of reporting nothing (independent review FN5).
    try { this.budget.observe([r], [path]); }
    catch (e) { e.page = { ...r, input: canonical, key }; throw e; }
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
    const record = (n, pin, r) => ({
      n, input: pin, key: r.key ?? canonicalKey(pin), ok: !!r.ok, cached: !!r.cached,
      rows: Array.isArray(r.data) ? r.data.length : r.data == null ? 0 : 1,
      at: r.at ?? null, error: r.ok ? null : (r.error && r.error.code) || null,
    });
    for (let n = 0; n < want; n++) {
      const pin = n === 0 ? canonical : pageInput(path, canonical, n);
      let r;
      try {
        r = await this._page(path, pin, { fresh });
      } catch (e) {
        // A throw here is a rate limit or a transport failure, and it ends the walk. Everything the
        // walk actually asked for is attached to the error so the caller can journal it: without
        // this, pages already read live only in these local variables and vanish with the stack,
        // which is the evidence loss requirement 7.8 forbids (independent review FN5).
        e.pages = [...out, e.page ? record(n, pin, e.page) : { n, input: pin, key: canonicalKey(pin), ok: false, cached: false, rows: 0, at: null, error: e.name === "RateLimited" ? "TOO_MANY_REQUESTS" : e.name || "ERROR" }];
        e.walkComplete = false;
        e.rowCount = rows.length;
        throw e;
      }
      const count = Array.isArray(r.data) ? r.data.length : r.data == null ? 0 : 1;
      out.push(record(n, pin, r));
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
