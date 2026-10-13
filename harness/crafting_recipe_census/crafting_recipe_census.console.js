/*
 * TNR Crafting Recipe Census - operator-run, READ-ONLY browser console script.
 *
 * Paste into the DevTools console of any https://www.theninja-rpg.com/ tab and run:
 *
 *   await TNRCraftCensus.run()      // start, or resume after a halt / reload (re-paste first)
 *   await TNRCraftCensus.status()   // progress summary
 *   TNRCraftCensus.stop()           // stop after the in-flight request; state is kept
 *   await TNRCraftCensus.download() // save the raw capture JSON (any time; final once "complete")
 *   await TNRCraftCensus.reset()    // discard saved state and start over
 *
 * What it does (source pin studie-tech/TheNinjaRPG@641040531176f91a3076fe5f32592ba18197a8c0):
 *   1. item.getAll {canBeCrafted:true, hidden:false} then {hidden:true}, cursor 0,1,2... until
 *      nextCursor is null (app/src/server/api/routers/item.ts getAll; offset paging ordered by
 *      cost, repsCost, id). The three min*Cost filters are set to INT32_MIN because the list
 *      filter otherwise defaults them to 0 and would silently drop a negative-cost row.
 *   2. item.getItemWithCraftingRequirements {id} for every distinct id from step 1.
 *   3. Both list passes again; the builder compares them to step 1 to prove the snapshot held.
 *
 * Safety properties (enforced in code below, exercised by census_script.test.mjs):
 *   - GET only, to exactly the two procedures above, same origin, one procedure per request.
 *   - credentials:"omit": no cookie or session is sent, so the requests are anonymous. Both
 *     procedures are publicProcedure queries with no role check. Anonymous requests also mean
 *     the rate limiter keys on IP, never on the operator's account, so its logged-in penalty
 *     (1% money/bank, movedTooFastCount) cannot apply to the operator.
 *   - Throttled to one request per throttleMs (default 2500 ms, floor 1500 ms). The server limit
 *     is 60 per 60 s per procedure (trpc.ts ratelimit slidingWindow(60, "60 s")).
 *   - Any TOO_MANY_REQUESTS / 429, auth error or BAD_REQUEST halts immediately without retry.
 *     Network / 5xx errors retry at most maxRetries times with backoff, then halt.
 *   - State is saved to IndexedDB after every request, so a halt, stop, reload or closed tab
 *     resumes where it left off. Nothing is uploaded anywhere; download() saves a local file.
 */
(function (root, factory) {
  "use strict";
  const api = factory();
  if (typeof module === "object" && module.exports) module.exports = api;
  else root.TNRCraftCensus = api.install(api.browserEnv(root));
})(typeof globalThis !== "undefined" ? globalThis : this, function () {
  "use strict";

  const VERSION = "1.0.0";
  const SCHEMA = "tnr.crafting_census.raw.v1";
  const SOURCE_PIN = "studie-tech/TheNinjaRPG@641040531176f91a3076fe5f32592ba18197a8c0";
  const LIST_PROC = "item.getAll";
  const DETAIL_PROC = "item.getItemWithCraftingRequirements";
  const ALLOWED_PROCS = Object.freeze([LIST_PROC, DETAIL_PROC]);
  const ALLOWED_HOST = /(^|\.)theninja-rpg\.com$/;
  const STATE_KEY = "tnr_crafting_census_v1";
  const MIN_THROTTLE_MS = 1500;
  const RATE_LIMIT_COOLDOWN_MS = 65000;
  const INT32_MIN = -2147483648;
  const DEFAULTS = Object.freeze({ throttleMs: 2500, limit: 200, maxRetries: 3 });
  const PASSES = Object.freeze([
    { key: "hidden=false", hidden: false },
    { key: "hidden=true", hidden: true },
  ]);

  class Halt extends Error {
    constructor(reason, detail) {
      super(`${reason}: ${detail}`);
      this.reason = reason;
      this.detail = detail;
    }
  }

  const listInput = (hidden, cursor, limit) => ({
    canBeCrafted: true,
    hidden,
    minCost: INT32_MIN,
    minRepsCost: INT32_MIN,
    minSeichiSilverCost: INT32_MIN,
    cursor,
    limit,
  });

  const emptyPasses = () =>
    Object.fromEntries(PASSES.map((p) => [p.key, { pages: [], nextCursor: 0, done: false }]));

  const newState = (env, config) => ({
    schema: SCHEMA,
    scriptVersion: VERSION,
    sourcePin: SOURCE_PIN,
    origin: env.origin,
    config,
    status: "in_progress",
    phase: "list",
    createdAt: env.now(),
    updatedAt: env.now(),
    finishedAt: null,
    lastRequestAt: null,
    notBefore: null,
    seq: 0,
    lists: { main: emptyPasses(), confirm: emptyPasses() },
    detailIds: [],
    details: {},
    requestLog: [],
    halts: [],
  });

  function normalizeConfig(opts) {
    const c = Object.assign({}, DEFAULTS, opts || {});
    for (const k of Object.keys(c)) {
      if (!(k in DEFAULTS)) throw new Error(`unknown option ${k}`);
    }
    if (!Number.isInteger(c.limit) || c.limit < 1 || c.limit > 500) {
      throw new Error("limit must be an integer 1..500 (item.getAll schema)");
    }
    if (!Number.isFinite(c.throttleMs) || c.throttleMs < MIN_THROTTLE_MS) {
      throw new Error(`throttleMs must be >= ${MIN_THROTTLE_MS}`);
    }
    if (!Number.isInteger(c.maxRetries) || c.maxRetries < 0 || c.maxRetries > 5) {
      throw new Error("maxRetries must be an integer 0..5");
    }
    return c;
  }

  /** Classify one tRPC batch response. Returns {data} | {notFound} or throws Halt / retryable. */
  function classify(httpStatus, text) {
    let body;
    try {
      body = JSON.parse(text);
    } catch (_e) {
      if (httpStatus === 429) throw new Halt("RATE_LIMIT", "HTTP 429");
      return { retry: `unparseable body (HTTP ${httpStatus})` };
    }
    const entry = Array.isArray(body) ? body[0] : body;
    const err = entry && entry.error && (entry.error.json || entry.error);
    if (err) {
      const code = (err.data && err.data.code) || "UNKNOWN";
      const status = (err.data && err.data.httpStatus) || httpStatus;
      const msg = `${code} ${status} ${err.message || ""}`.trim();
      if (code === "TOO_MANY_REQUESTS" || status === 429) throw new Halt("RATE_LIMIT", msg);
      if (code === "UNAUTHORIZED" || code === "FORBIDDEN" || status === 401 || status === 403) {
        throw new Halt("AUTH", msg);
      }
      if (code === "NOT_FOUND") return { notFound: msg };
      if (code === "BAD_REQUEST" || code === "PARSE_ERROR" || status === 400) {
        throw new Halt("CONTRACT", msg);
      }
      return { retry: msg };
    }
    if (httpStatus === 429) throw new Halt("RATE_LIMIT", "HTTP 429");
    if (httpStatus === 401 || httpStatus === 403) throw new Halt("AUTH", `HTTP ${httpStatus}`);
    if (httpStatus < 200 || httpStatus >= 300) return { retry: `HTTP ${httpStatus}` };
    const result = entry && entry.result && entry.result.data;
    if (!result || !("json" in result)) return { retry: "no result.data.json in body" };
    return { data: result.json };
  }

  function create(env) {
    let state = null;
    let running = false;
    let stopRequested = false;

    const save = async () => {
      state.updatedAt = env.now();
      await env.store.set(STATE_KEY, state);
    };

    async function waitTurn() {
      const gates = [];
      if (state.lastRequestAt !== null) gates.push(state.lastRequestAt + state.config.throttleMs);
      if (state.notBefore !== null) gates.push(state.notBefore);
      const until = Math.max(env.now(), ...gates);
      if (state.notBefore !== null && state.notBefore > env.now()) {
        env.log(`[census] rate-limit cooldown: waiting ${Math.ceil((state.notBefore - env.now()) / 1000)} s`);
      }
      if (until > env.now()) await env.sleep(until - env.now());
    }

    /** The only network path in this script. */
    async function trpcGet(proc, input) {
      if (!ALLOWED_PROCS.includes(proc)) throw new Error(`refusing procedure ${proc}`);
      const url =
        `${env.origin}/api/trpc/${proc}?batch=1&input=` +
        encodeURIComponent(JSON.stringify({ 0: { json: input } }));
      for (let attempt = 1; ; attempt++) {
        await waitTurn();
        const seq = ++state.seq;
        const started = env.now();
        state.lastRequestAt = started;
        let httpStatus = 0;
        let outcome;
        try {
          const res = await env.fetch(url, {
            method: "GET",
            credentials: "omit",
            cache: "no-store",
            redirect: "error",
            headers: { accept: "application/json" },
          });
          httpStatus = res.status;
          outcome = classify(httpStatus, await res.text());
        } catch (e) {
          if (e instanceof Halt) {
            state.requestLog.push({ seq, at: started, proc, input, attempt, httpStatus, ms: env.now() - started, outcome: `halt:${e.reason}` });
            throw e;
          }
          outcome = { retry: `network: ${e && e.message ? e.message : String(e)}` };
        }
        const label = outcome.data !== undefined ? "ok" : outcome.notFound ? "not_found" : "retry";
        state.requestLog.push({ seq, at: started, proc, input, attempt, httpStatus, ms: env.now() - started, outcome: label });
        if (!outcome.retry) return outcome;
        if (attempt > state.config.maxRetries) {
          throw new Halt("TRANSIENT_EXHAUSTED", `${proc} after ${attempt} attempts: ${outcome.retry}`);
        }
        await save();
        await env.sleep(state.config.throttleMs * 2 ** attempt);
      }
    }

    function checkStop() {
      if (stopRequested) throw new Halt("STOPPED", "operator stop()");
    }

    async function listPasses(which) {
      for (const p of PASSES) {
        const pass = state.lists[which][p.key];
        while (!pass.done) {
          checkStop();
          const cursor = pass.nextCursor;
          const input = listInput(p.hidden, cursor, state.config.limit);
          const out = await trpcGet(LIST_PROC, input);
          if (out.notFound) throw new Halt("CONTRACT", `item.getAll NOT_FOUND at cursor ${cursor}`);
          const d = out.data;
          if (!d || !Array.isArray(d.data) || !("nextCursor" in d)) {
            throw new Halt("CONTRACT", "item.getAll response lacks data[] / nextCursor");
          }
          const nc = d.nextCursor;
          if (nc !== null && nc !== cursor + 1) {
            throw new Halt("CONTRACT", `nextCursor ${nc} after cursor ${cursor}`);
          }
          pass.pages.push({ cursor, input, fetchedAt: env.now(), nextCursor: nc, rows: d.data });
          if (nc === null) pass.done = true;
          else pass.nextCursor = nc;
          await save();
          env.log(`[census] ${which} ${p.key} cursor ${cursor}: ${d.data.length} rows, next ${nc}`);
        }
      }
    }

    async function fetchDetails() {
      for (const id of state.detailIds) {
        if (state.details[id]) continue;
        checkStop();
        const out = await trpcGet(DETAIL_PROC, { id });
        state.details[id] = out.notFound
          ? { status: "not_found", fetchedAt: env.now(), message: out.notFound }
          : { status: "ok", fetchedAt: env.now(), data: out.data };
        await save();
        const done = Object.keys(state.details).length;
        env.log(`[census] detail ${done}/${state.detailIds.length} ${id}`);
      }
    }

    async function load(opts) {
      const saved = await env.store.get(STATE_KEY);
      if (saved) {
        if (saved.schema !== SCHEMA || saved.scriptVersion !== VERSION) {
          throw new Error(`saved state is ${saved.schema} v${saved.scriptVersion}; download() it, then reset()`);
        }
        if (opts && Object.keys(opts).length) {
          throw new Error("options only apply to a fresh census; reset() first to change them");
        }
        state = saved;
      } else {
        state = newState(env, normalizeConfig(opts));
        await save();
      }
    }

    async function run(opts) {
      if (running) throw new Error("already running");
      if (!ALLOWED_HOST.test(env.hostname)) {
        throw new Error(`run this from a theninja-rpg.com tab (got ${env.hostname})`);
      }
      running = true;
      stopRequested = false;
      try {
        await load(opts);
        if (state.status === "complete") {
          env.log("[census] already complete; download() it or reset() to start over");
          return summary();
        }
        state.status = "in_progress";
        if (state.phase === "list") {
          await listPasses("main");
          const ids = new Set();
          for (const p of PASSES) {
            for (const pg of state.lists.main[p.key].pages) for (const r of pg.rows) ids.add(r.id);
          }
          state.detailIds = [...ids].sort();
          state.phase = "details";
          await save();
        }
        if (state.phase === "details") {
          await fetchDetails();
          state.phase = "confirm";
          await save();
        }
        if (state.phase === "confirm") {
          await listPasses("confirm");
          state.phase = "done";
        }
        state.status = "complete";
        state.finishedAt = env.now();
        await save();
        env.log("[census] complete - run TNRCraftCensus.download()");
      } catch (e) {
        if (!(e instanceof Halt)) throw e;
        state.status = "halted";
        state.halts.push({ at: env.now(), reason: e.reason, detail: e.detail, phase: state.phase });
        if (e.reason === "RATE_LIMIT") state.notBefore = env.now() + RATE_LIMIT_COOLDOWN_MS;
        await save();
        env.log(`[census] HALTED ${e.reason}: ${e.detail}. State saved; run() again to resume.`);
      } finally {
        running = false;
      }
      return summary();
    }

    function summary() {
      if (!state) return { status: "not_started" };
      const passRows = (which) =>
        Object.fromEntries(
          PASSES.map((p) => {
            const ps = state.lists[which][p.key];
            return [p.key, { pages: ps.pages.length, rows: ps.pages.reduce((n, pg) => n + pg.rows.length, 0), done: ps.done }];
          }),
        );
      return {
        status: state.status,
        phase: state.phase,
        requests: state.seq,
        main: passRows("main"),
        details: `${Object.keys(state.details).length}/${state.detailIds.length}`,
        confirm: passRows("confirm"),
        lastHalt: state.halts[state.halts.length - 1] || null,
      };
    }

    return {
      VERSION,
      run,
      stop() {
        stopRequested = true;
        return "stop requested";
      },
      async status() {
        if (!state) state = (await env.store.get(STATE_KEY)) || null;
        return summary();
      },
      async snapshot() {
        if (!state) state = (await env.store.get(STATE_KEY)) || null;
        return state ? JSON.parse(JSON.stringify(state)) : null;
      },
      async download() {
        if (!state) state = (await env.store.get(STATE_KEY)) || null;
        if (!state) throw new Error("nothing captured yet");
        const name = `tnr_crafting_census_raw_${state.createdAt}_${state.status}.json`;
        env.download(name, JSON.stringify(state, null, 1));
        return name;
      },
      async reset() {
        if (running) throw new Error("stop() first");
        state = null;
        await env.store.del(STATE_KEY);
        return "reset";
      },
    };
  }

  function idbStore(indexedDB) {
    const open = () =>
      new Promise((resolve, reject) => {
        const req = indexedDB.open("tnr_crafting_census", 1);
        req.onupgradeneeded = () => req.result.createObjectStore("kv");
        req.onsuccess = () => resolve(req.result);
        req.onerror = () => reject(req.error);
      });
    const tx = async (mode, fn) => {
      const db = await open();
      return new Promise((resolve, reject) => {
        const t = db.transaction("kv", mode);
        const req = fn(t.objectStore("kv"));
        t.oncomplete = () => {
          db.close();
          resolve(req.result);
        };
        t.onerror = () => reject(t.error);
      });
    };
    return {
      get: (k) => tx("readonly", (s) => s.get(k)),
      set: (k, v) => tx("readwrite", (s) => s.put(v, k)),
      del: (k) => tx("readwrite", (s) => s.delete(k)),
    };
  }

  function browserEnv(w) {
    return {
      origin: w.location.origin,
      hostname: w.location.hostname,
      fetch: w.fetch.bind(w),
      now: () => Date.now(),
      sleep: (ms) => new Promise((r) => setTimeout(r, ms)),
      store: idbStore(w.indexedDB),
      log: (m) => w.console.log(m),
      download(name, text) {
        const url = URL.createObjectURL(new Blob([text], { type: "application/json" }));
        const a = w.document.createElement("a");
        a.href = url;
        a.download = name;
        w.document.body.appendChild(a);
        a.click();
        a.remove();
        setTimeout(() => URL.revokeObjectURL(url), 10000);
      },
    };
  }

  function install(env) {
    const census = create(env);
    env.log(`[census] TNRCraftCensus ${VERSION} loaded (read-only). await TNRCraftCensus.run()`);
    return census;
  }

  return {
    VERSION, SCHEMA, SOURCE_PIN, ALLOWED_PROCS, DEFAULTS, MIN_THROTTLE_MS, INT32_MIN, STATE_KEY,
    create, classify, listInput, browserEnv, install,
  };
});
