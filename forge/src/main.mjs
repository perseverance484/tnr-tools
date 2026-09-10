// Composition root. The only file that touches window.*; every layer is constructed here
// with the real localStorage, indexedDB and fetch, and nothing else in src/ reaches for them.
// Build: node build.mjs -> ../forge_bundle.js (IIFE), loaded by forge_loader_user.js.

import { Journal } from "./storage/journal.mjs";
import { CaptureCache } from "./storage/captures.mjs";
import { CookieSession } from "./transport/session.mjs";
import { AuthState, AUTH } from "./transport/auth.mjs";
import { TrpcClient } from "./transport/client.mjs";
import { Uploader } from "./transport/upload.mjs";
import { Budget } from "./budget/bucket.mjs";
import { CachedReader } from "./budget/reader.mjs";
import { Validator } from "./runner/validate.mjs";
import { Runner } from "./runner/runner.mjs";
import { Reconciler } from "./reconcile/reconciler.mjs";
import { Github } from "./github.mjs";
import { App } from "./ui/app.mjs";
import { entryTakeover, mountHost, whenBodyReady, alreadyMounted, onEntryPath, pageAuthRuntime, arm, disarm, isArmed, armHops, ENTRY_PATH, CARRIER_PATH, MAX_HOPS } from "./ui/takeover.mjs";
import { CSS, CSS_DOC } from "./ui/styles.mjs";
import { h, installCss } from "./ui/dom.mjs";
import FIELDS from "./runner/fields.json" with { type: "json" };
import NESTED from "./runner/nested.json" with { type: "json" };

export const VERSION = "forge 0.4.0";
// Field sets for pre-send validation are bundled from src/runner/fields.json, derived from the
// PINNED validators by tools/derive_fields.mjs. 45d (2026-08-26) is stale against the pin, so it
// is not fetched at boot: the bundle validates against exactly the commit it was audited on.

/**
 * Build the whole dependency graph. THIS is the composition under test: every harness calls it,
 * so a wiring mistake here (a missing journal on the Reconciler, say) fails the suite instead of
 * shipping behind a safer test-only graph. Only the environment primitives and the transport
 * client are injectable; every wiring decision lives here and nowhere else.
 */
export function compose({ storage, indexedDB, fetchImpl, clock = () => Date.now(), tabId,
                          log = () => {}, client = null, sleep, runtime = null, authState = AUTH.UNKNOWN } = {}) {
  const deps = {};
  deps.journal = new Journal(storage, clock);
  deps.cache = new CaptureCache(indexedDB, clock);
  deps.session = new CookieSession({ fetchImpl, origin: "" });
  deps.client = client ?? new TrpcClient(deps.session, { onExchange: (r) => log(`${r.kind} ${r.paths.join(",")} -> ${r.status ?? r.error}`) });
  // The auth gate is part of the shipped graph, not a UI decoration: the Runner consults it
  // before every protected send, so a wiring mistake here fails the suite rather than shipping.
  deps.auth = new AuthState({ client: deps.client, runtime, clock, state: authState });
  deps.budget = new Budget({ storage, clock, ...(sleep ? { sleep } : {}) });
  deps.reader = new CachedReader({ client: deps.client, cache: deps.cache, budget: deps.budget });
  deps.reconciler = new Reconciler({ storage, reader: deps.reader, clock, journal: deps.journal });
  deps.github = new Github({ fetchImpl, storage });
  deps.uploader = new Uploader({ session: deps.session, fetchImpl });
  deps.validator = new Validator(FIELDS, NESTED);
  deps.runner = new Runner({
    journal: deps.journal, client: deps.client, reader: deps.reader, cache: deps.cache,
    budget: deps.budget, validator: deps.validator, uploader: deps.uploader,
    reconciler: deps.reconciler, auth: deps.auth, storage, clock, tabId, log,
  });
  return deps;
}

/**
 * Boot. Three outcomes, decided by where the tab is and whether this tab has been armed:
 *
 *   ENTRY   /forge. Arm this tab, show one line, hand off to the carrier. Nothing else runs
 *           here: this document has no providers, which is precisely the defect being repaired.
 *   HOST    an armed tab on any other path on the game origin. Wait for the page's own auth
 *           runtime, probe the protected surface once, then mount the overlay over the live
 *           application route with its provider tree untouched.
 *   INERT   anything else. The loader now matches the whole game origin (it has to: the carrier
 *           route is not known in advance and the app may redirect), so on an ordinary game page
 *           in an unarmed tab Forge must do NOTHING - no stop(), no document edit, no request,
 *           no style. This branch returning null is the guarantee that installing Forge does not
 *           change the game for the operator who is not using it.
 *
 * @returns {Promise<App|null>} the mounted app, or null when this page is not Forge's to run on.
 */
export async function boot(win = window, { redirect = null, establish = true } = {}) {
  const doc = win.document;
  if (onEntryPath(win.location)) return bootEntry(win, doc, redirect);
  if (!isArmed(win)) return null;
  return bootHost(win, doc, { establish });
}

/**
 * The /forge entry (brief section A: the operator keeps one URL to remember). It is still a
 * same-origin 404 with no providers, so it is stopped and emptied as before - but instead of
 * mounting the app into a document that cannot hold a session, it arms the tab and navigates to
 * a route that can. MAX_HOPS bounds it: if arming and navigating twice has not produced a usable
 * host, the splash says so rather than bouncing forever.
 */
function bootEntry(win, doc, redirect) {
  const { body } = entryTakeover(doc, win);
  installCss(CSS_DOC, doc);
  installCss(CSS, doc);
  const hops = armHops(win);
  const panel = h("div", { class: "f-boot" });
  body.appendChild(panel);
  if (hops >= MAX_HOPS) {
    disarm(win);
    panel.append(
      h("div", {}, h("b", {}, "TNR forge could not reach an authenticated page.")),
      h("p", {}, `Forge tried ${hops} times to hand off from ${ENTRY_PATH} to a normal game page and ended up back here. Open the game, sign in, and then open ${ENTRY_PATH} again.`),
    );
    return null;
  }
  arm(win);
  panel.append(
    h("div", {}, h("b", {}, "TNR forge")),
    h("p", {}, "Opening the game so Forge runs inside your signed-in session\u2026"),
    h("p", { class: "f-mute" }, `${ENTRY_PATH} has no game providers, so a session cannot live here. Forge continues on ${CARRIER_PATH}.`),
  );
  const go = redirect ?? ((url) => { win.location.replace(url); });
  go(CARRIER_PATH);
  return null;
}

/**
 * The carrier. Forge mounts as an overlay ON TOP of a live application route; the React tree,
 * ClerkProvider and TrpcClientProvider under it are never unmounted, which is the whole repair.
 * Protected operation is not offered until AuthState has been established, so nothing protected
 * can be sent "before the session is ready" - the gate in the Runner enforces the same rule for
 * every later send, in case the session dies mid-job.
 */
async function bootHost(win, doc, { establish = true } = {}) {
  // The document-start body wait (independent review FPA-1). Nothing is written to the carrier
  // before this resolves, so an armed page that has not been parsed as far as <body> is as inert
  // as an unarmed one until it is ready.
  await whenBodyReady(doc, win);
  // One overlay per document. Belt and braces against a second boot() on the same page - a
  // re-entered bundle, or a test - stacking a second Forge on top of the first.
  if (alreadyMounted(doc)) return null;

  const clock = () => Date.now();
  // the job lease is keyed by tab; sessionStorage survives a reload or a restored tab, not a new one
  let tabId;
  try { tabId = win.sessionStorage.getItem("tnr_forge_tab") || null; if (!tabId) { tabId = Math.random().toString(36).slice(2, 12); win.sessionStorage.setItem("tnr_forge_tab", tabId); } } catch { tabId = undefined; }
  let deps = {};
  // host is created INSIDE the guard, so a failure to mount at all leaves the carrier untouched
  // rather than half-decorated with an overlay nothing could be rendered into.
  let host = null;
  try {
    host = mountHost(doc, win);
    deps = compose({
      storage: win.localStorage, indexedDB: win.indexedDB, fetchImpl: win.fetch.bind(win),
      clock, tabId, runtime: pageAuthRuntime(win), log: (m) => deps.app && deps.app.log(m),
    });
    deps.app = new App({
      version: VERSION, storage: win.localStorage, now: clock, ...deps,
      exit: () => { disarm(win); host.release(); },
    });
    deps.app.mount(host.body, doc);
    // A host mount is what the hop counter was counting towards, so reset it here. Otherwise a
    // tab that has used Forge once would refuse the third trip through /forge as a redirect loop.
    arm(win, { hops: 0 });
  } catch (e) {
    // Nothing was mounted: say nothing and change nothing. Reporting into a page Forge does not
    // own would be the one behaviour an unarmed-page-is-inert contract cannot afford.
    if (!host) return null;
    const panel = h("div", { class: "f-boot" });
    panel.append(h("div", {}, h("b", {}, "TNR forge failed to start")), h("pre", { style: { whiteSpace: "pre-wrap", fontSize: "12px" } }, String(e && e.stack || e)));
    host.body.appendChild(panel);
    return null;
  }
  // One establish pass, after mount so the operator watches it happen rather than a blank screen.
  // It is deliberately not awaited by the caller: a slow Clerk boot must not stop the UI existing.
  if (establish) deps.app.establishAuth().catch((e) => deps.app.fail("auth check", e));
  return deps.app;
}

// The loader matches the whole game origin, so this runs on every game page. boot() returns
// immediately on an unarmed page; the catch is the last guarantee that a Forge bug can never
// break the game for the operator.
if (typeof window !== "undefined" && typeof document !== "undefined") {
  try { Promise.resolve(boot(window)).catch(() => {}); } catch { /* never break the host page */ }
}
