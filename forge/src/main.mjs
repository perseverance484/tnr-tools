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
import { entryTakeover, mountHost, whenBodyReady, whenCarrierReady, carrierReadiness, alreadyMounted, onEntryPath, pageAuthRuntime, arm, disarm, isArmed, armHops, armFailure, ENTRY_PATH, CARRIER_PATH, MAX_HOPS, MAX_HOST_LOSSES, CARRIER_GRACE_MS } from "./ui/takeover.mjs";
import { CSS, CSS_DOC } from "./ui/styles.mjs";
import { h, installCss } from "./ui/dom.mjs";
import FIELDS from "./runner/fields.json" with { type: "json" };
import NESTED from "./runner/nested.json" with { type: "json" };

export const VERSION = "forge 0.4.1";
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
 *   HOST    an armed tab on any other path on the game origin. Wait for <body>, then wait for
 *           the carrier to be READY for a persistent overlay (its framework has taken ownership
 *           of body, see takeover.mjs), mount the overlay over the live application route with
 *           its provider tree untouched, then let the page's own auth runtime settle and probe
 *           the protected surface once.
 *   INERT   anything else. The loader now matches the whole game origin (it has to: the carrier
 *           route is not known in advance and the app may redirect), so on an ordinary game page
 *           in an unarmed tab Forge must do NOTHING - no stop(), no document edit, no request,
 *           no style. This branch returning null is the guarantee that installing Forge does not
 *           change the game for the operator who is not using it.
 *
 * @returns {Promise<App|null>} the mounted app, or null when this page is not Forge's to run on.
 */
export async function boot(win = window, { redirect = null, establish = true, readiness = {} } = {}) {
  const doc = win.document;
  if (onEntryPath(win.location)) return bootEntry(win, doc, redirect);
  if (!isArmed(win)) return null;
  return bootHost(win, doc, { establish, readiness });
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
    // A host attempt that failed AFTER reaching the carrier records why (a startup diagnostic,
    // not auth material); it is shown here, on the one page Forge owns outright, and then dropped
    // with the marker so the next attempt starts clean.
    const failure = armFailure(win);
    disarm(win);
    panel.append(
      h("div", {}, h("b", {}, failure ? "TNR forge could not stay on the game page." : "TNR forge could not reach an authenticated page.")),
      h("p", {}, failure
        ? `Forge reached a normal game page but could not keep its overlay there: ${failure}`
        : `Forge tried ${hops} times to hand off from ${ENTRY_PATH} to a normal game page and ended up back here. Open the game, sign in, and then open ${ENTRY_PATH} again.`),
      failure ? h("p", { class: "f-mute" }, `Open the game, make sure it has finished loading, and then open ${ENTRY_PATH} again. If this repeats, the game's page structure has changed under Forge and needs a Forge update.`) : null,
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
 *
 * Lifecycle (state/prompt_forge_disappearing_overlay.md):
 *
 *   1. wait for <body>                       nothing is written before it exists (FPA-1);
 *   2. wait for the carrier to be READY      React has taken ownership of body, or the page's
 *                                            own runtime has settled on a loaded document. 0.4.0
 *                                            skipped this step and mounted into a body that
 *                                            hydration then cleared;
 *   3. mount once, then confirm STABLE       the host is attached and the readiness signal still
 *                                            holds. Only then is the hop counter reset: an
 *                                            overlay that has not reached this point must not
 *                                            make /forge loop forever as though startup succeeded;
 *   4. watch for host loss                   if the page removes the host anyway, wait for
 *                                            readiness again and remount the SAME app once,
 *                                            keeping its state. A second loss stops: the hop
 *                                            counter is set to its limit and the reason recorded,
 *                                            so the next /forge shows a diagnostic instead of
 *                                            bouncing. No third attempt, no tug-of-war;
 *   5. Close                                 disconnects the watchers first, then removes the
 *                                            host, restores scrolling and disarms the tab.
 */
async function bootHost(win, doc, { establish = true, readiness = {} } = {}) {
  // The document-start body wait (independent review FPA-1). Nothing is written to the carrier
  // before this resolves, so an armed page that has not been parsed as far as <body> is as inert
  // as an unarmed one until it is ready.
  await whenBodyReady(doc, win);
  // One overlay per document. Belt and braces against a second boot() on the same page - a
  // re-entered bundle, or a test - stacking a second Forge on top of the first.
  if (alreadyMounted(doc)) return null;
  // The carrier readiness wait. Body existing is not body being safe to append to: the game
  // hydrates the whole document, and an overlay appended before that commit is reconciled away.
  const via = await whenCarrierReady(doc, win, readiness);
  if (!via) {
    // Nothing was written. Record why for the /forge splash rather than mounting into a page
    // that never became ready, and leave the hop counter alone: the next /forge counts it.
    arm(win, { hops: armHops(win), failure: `the game page never became ready to host an overlay (no framework ownership of <body> within ${Math.round(CARRIER_GRACE_MS / 1000)}s of the page finishing loading)` });
    return null;
  }
  if (alreadyMounted(doc)) return null;

  const clock = () => Date.now();
  // the job lease is keyed by tab; sessionStorage survives a reload or a restored tab, not a new one
  let tabId;
  try { tabId = win.sessionStorage.getItem("tnr_forge_tab") || null; if (!tabId) { tabId = Math.random().toString(36).slice(2, 12); win.sessionStorage.setItem("tnr_forge_tab", tabId); } } catch { tabId = undefined; }
  let deps = {};
  // host is created INSIDE the guard, so a failure to mount at all leaves the carrier untouched
  // rather than half-decorated with an overlay nothing could be rendered into.
  let host = null;
  let losses = 0;
  const log = (m) => { if (deps.app) deps.app.log(m); };

  // Step 4. Called by mountHost() at most once per host, with that host's watchers already
  // disconnected. Bounded by MAX_HOST_LOSSES, and every outcome is recorded.
  const onLost = async () => {
    losses += 1;
    log(`host lost (${losses}): the carrier removed the Forge overlay`);
    if (losses > MAX_HOST_LOSSES) {
      // Stop. The marker keeps the tab armed with the counter at its limit, so the very next
      // /forge shows the diagnostic and disarms; nothing further is written to this page.
      arm(win, { hops: MAX_HOPS, failure: `the game page removed the Forge overlay ${losses} times after it mounted; Forge stopped rather than fight the page for it` });
      log("host lost again after a remount; giving up on this page");
      return;
    }
    try {
      const again = await whenCarrierReady(doc, win, readiness);
      if (!again) {
        arm(win, { hops: MAX_HOPS, failure: "the game page removed the Forge overlay and then never became ready for it again" });
        return;
      }
      if (alreadyMounted(doc)) return;
      host = mountHost(doc, win, { onLost });
      // the app and its DOM survived the detachment; it is re-homed, not rebuilt
      host.body.appendChild(deps.app.root);
      log(`host remounted after loss (carrier ready via ${again})`);
    } catch (e) {
      arm(win, { hops: MAX_HOPS, failure: `remounting the Forge overlay failed: ${(e && e.message) || e}` });
    }
  };

  try {
    host = mountHost(doc, win, { onLost });
    deps = compose({
      storage: win.localStorage, indexedDB: win.indexedDB, fetchImpl: win.fetch.bind(win),
      clock, tabId, runtime: pageAuthRuntime(win), log,
    });
    deps.app = new App({
      version: VERSION, storage: win.localStorage, now: clock, ...deps,
      // Step 5. release() disconnects the loss watchers before it removes the host, so Close is
      // never mistaken for a loss; host is read at call time so a remounted host is the one released.
      exit: () => { disarm(win); host.release(); },
    });
    deps.app.mount(host.body, doc);
    log(`mounted on ${win.location.pathname} (carrier ready via ${via})`);
    // Step 3. The hop counter was counting towards a STABLE host, and that is what resets it -
    // not the mount by itself. Stable means the host is still attached and the carrier is still
    // ready, checked now rather than assumed; a host that does not pass leaves the counter as
    // the entry left it, so a vanishing overlay cannot turn /forge into an endless loop.
    if (host.attached() && carrierReadiness(doc, win)) arm(win, { hops: 0, failure: null });
    else log("mounted but not stable; the hop counter is left as it was");
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
