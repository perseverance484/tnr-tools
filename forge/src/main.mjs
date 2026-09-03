// Composition root. The only file that touches window.*; every layer is constructed here
// with the real localStorage, indexedDB and fetch, and nothing else in src/ reaches for them.
// Build: node build.mjs -> ../forge_bundle.js (IIFE), loaded by forge_loader_user.js.

import { Journal } from "./storage/journal.mjs";
import { CaptureCache } from "./storage/captures.mjs";
import { CookieSession } from "./transport/session.mjs";
import { TrpcClient } from "./transport/client.mjs";
import { Uploader } from "./transport/upload.mjs";
import { Budget } from "./budget/bucket.mjs";
import { CachedReader } from "./budget/reader.mjs";
import { Validator } from "./runner/validate.mjs";
import { Runner } from "./runner/runner.mjs";
import { Reconciler } from "./reconcile/reconciler.mjs";
import { Github } from "./github.mjs";
import { App } from "./ui/app.mjs";
import { takeover, onHostPath } from "./ui/takeover.mjs";
import { h } from "./ui/dom.mjs";

export const VERSION = "forge 0.1.0";
// 45d is fetched from the repo at boot (same source as the old builder's 45c/45g fetch): the
// field sets for pre-send validation. If the fetch fails the app still boots, and validation
// reports "no field schema" for every non-ai item, which blocks a run rather than guessing.
const SCHEMA_URL = "https://raw.githubusercontent.com/perseverance484/tnr-tools/main/skills/building-tnr-content/data/45d_DATA_entity_schemas.json";

export async function boot(win = window) {
  if (!onHostPath(win.location)) return null;
  const { body } = takeover(win.document, win);
  const status = h("div", { style: { padding: "16px", fontFamily: "system-ui", color: "#e8eaf0", background: "#0f1115", minHeight: "100vh" } }, "TNR forge: starting…");
  body.appendChild(status);

  const storage = win.localStorage;
  const fetchImpl = win.fetch.bind(win);
  const clock = () => Date.now();
  const deps = {};
  try {
    deps.journal = new Journal(storage, clock);
    deps.cache = new CaptureCache(win.indexedDB, clock);
    deps.session = new CookieSession({ fetchImpl, origin: "" });
    deps.client = new TrpcClient(deps.session, { onExchange: (r) => deps.app && deps.app.log(`${r.kind} ${r.paths.join(",")} -> ${r.status ?? r.error}`) });
    deps.budget = new Budget({ storage, clock });
    deps.reader = new CachedReader({ client: deps.client, cache: deps.cache, budget: deps.budget });
    deps.reconciler = new Reconciler({ storage, reader: deps.reader, clock });
    deps.github = new Github({ fetchImpl, storage });
    deps.uploader = new Uploader({ session: deps.session, fetchImpl });
    let schemas = null;
    try { const r = await fetchImpl(SCHEMA_URL, { cache: "no-cache" }); if (r.ok) schemas = await r.json(); } catch { schemas = null; }
    deps.validator = new Validator(schemas);
    deps.runner = new Runner({ journal: deps.journal, client: deps.client, reader: deps.reader, cache: deps.cache, budget: deps.budget, validator: deps.validator, uploader: deps.uploader, reconciler: deps.reconciler, storage, log: (m) => deps.app && deps.app.log(m) });
    deps.app = new App({ version: VERSION, storage, now: clock, ...deps });
    status.remove();
    deps.app.mount(body, win.document);
    if (deps.validator.schemaMissing) deps.app.toast("45d field schemas could not be fetched; runs are blocked until they load. Refresh to retry.", "bad", 12000);
    return deps.app;
  } catch (e) {
    status.textContent = "";
    status.append(h("div", {}, h("b", {}, "TNR forge failed to start")), h("pre", { style: { whiteSpace: "pre-wrap", fontSize: "12px" } }, String(e && e.stack || e)));
    return null;
  }
}

if (typeof window !== "undefined" && typeof document !== "undefined") boot(window);
