// Where Forge runs, and how it gets there.
//
// WHAT CHANGED AND WHY. Forge 0.3.0 booted on /forge and took the whole document over at
// document-start. /forge is an unmatched path, so from source it renders through
// global-not-found.tsx: next.config.mjs sets experimental.globalNotFound, proxy.ts returns
// immediately for every pathname other than "/", and global-not-found.tsx is a bare
// <html><body> with one Link. That is why it was chosen - no provider tree to fight, no game
// requests on mount - and it is also exactly why protected work failed there. layout.tsx mounts
// ClerkProvider and TrpcClientProvider for VALID application routes only, so on /forge the
// page's own Clerk runtime never starts, nothing refreshes the session the browser holds, and
// createAppTRPCContext's auth() finds no userId: every protectedProcedure answers UNAUTHORIZED.
// Two Forge 0.3.0 runs proved it, five profile.getAi reads each, all five UNAUTHORIZED
// (harvests/inbox/tnr_results_1789066888093.json and tnr_results_1789067111434.json).
//
// THE REPAIR, in the brief's preferred shape (section B):
//
//   ENTRY (/forge)   unchanged for the operator, but no longer where the app runs. It arms a
//                    per-tab marker and hands off to the carrier. It is still a providerless
//                    404, so stopping and emptying it costs nothing.
//   CARRIER (/)      a real application route, so the root layout mounts ClerkProvider and
//                    TrpcClientProvider and clerk-js runs. Forge does NOT take this document
//                    over: it appends one fixed, full-screen overlay and leaves the React tree,
//                    the providers and the auth runtime mounted and untouched underneath. The
//                    provider tree staying alive is the entire fix; destroying it would put us
//                    back on /forge with extra steps.
//
// WHY "/" IS THE CARRIER. It is the one route repository-held source evidence names positively:
// proxy.ts's callback special-cases it (`if (pathname !== "/") return;`), so it is a matched
// route rather than a global-not-found render, and the tRPC context carries two A/B variants
// that "steer landing-page layout" (client_contract.json, feasibility_gates.G4), which is a
// landing page rendering under the root layout. It is also the lightest such route this audit
// can name, which matters because the carrier's own tRPC traffic is outside Forge's budget
// accounting (see BUILDER_APP_NOTES.md). No route NAME is compiled into the activation logic
// though: the marker is a per-tab flag, not a URL, so if the app navigates away from "/", Forge
// activates on wherever it lands. That is not hypothetical - HomeLanding.tsx:27-45 at the task pin
// pushes a signed-in operator to /profile (or /register, or /500) once user data resolves. It is a
// CLIENT-side router.push inside the Next root, so the document, the providers and this overlay
// (appended to document.body outside that root) all survive it. The carrier constant is a hint,
// and being wrong about it costs a navigation, not the repair.
//
// WHY "BODY EXISTS" IS NOT "CARRIER READY" (0.4.1, state/prompt_forge_disappearing_overlay.md).
// 0.4.0 mounted the overlay as soon as the parser produced <body>, which on a document-start
// userscript is BEFORE the game's own JavaScript has run. The carrier's root layout
// (app/src/app/layout.tsx at 98d0eca5) renders <html> and <body> as React elements, so Next
// hydrates the whole document: React walks the server-rendered body children and matches them
// against the client tree. In React 19 <body> is a "singleton" scope, where a foreign node whose
// tag does not match the next expected element is skipped - but a foreign node that DOES match
// the tag is claimed. Forge's host is a <div>, and the first React child of the game's body that
// is a <div> is the layout shell, so when the host lands ahead of it React claims the host as
// that shell, finds none of the shell's children inside it, throws a hydration mismatch, and
// recovers by client-rendering the root: clearContainerSparingly() removes every body child that
// is not a <script>, <style> or stylesheet <link>, and acquireSingletonInstance() strips the
// body's attributes (our scroll lock among them) before re-rendering the game. That is the
// operator's "splash, then the plain game": the overlay was mounted and then reconciled away.
// Reproduced against react-dom@19.2.8 (the pinned version) in forge/test/carrier.react.test.mjs.
//
// The stable condition is therefore "React has taken ownership of <body>", not "body exists":
// react-dom stamps every node it hydrates or creates with an own property named
// __reactFiber$<random> (and __reactProps$<random>) - ReactDOMComponentTree's internalInstanceKey,
// unchanged since React 17 - and the container is cleared exactly once, on the root's first
// commit, so a node appended to body AFTER that stamp appears is never touched by React again
// (the /  -> /profile client navigation only re-renders inside the layout shell). The fallback
// readiness signal, used only if that internal name ever changes, is the page's own runtime
// having finished starting (window.Clerk.loaded) on a fully loaded document. A bounded host-loss
// watcher is defence in depth: if the overlay is nonetheless removed, Forge waits for readiness
// and remounts ONCE; a second loss stops it and records a diagnostic for the /forge splash.
//
// The overlay covers the carrier; it does not restyle it. The stylesheet is scoped to .f-app
// and the document reset is installed on the entry splash only, so the game page underneath is
// returned exactly as it was when Forge is closed.

import { h, clear } from "./dom.mjs";

export const ENTRY_PATH = "/forge";
export const CARRIER_PATH = "/";
// Per-TAB, in sessionStorage: a second tab is not dragged into Forge, and closing the tab ends
// it. It holds a hop counter and, after a failed attempt, one line of diagnostic - no auth
// material, no session data, no id.
export const ARM_KEY = "tnr_forge_armed_v1";
export const MAX_HOPS = 2; // a redirect that lands somewhere unexpected must not loop
// How many times the carrier may remove a mounted overlay before Forge stops remounting. One
// remount covers "the readiness signal was early"; a second loss means the page is actively
// reconciling body and a third attempt would be the tug-of-war the brief forbids.
export const MAX_HOST_LOSSES = 1;
// After the document has fully loaded, how long to keep waiting for the carrier to become ready
// before giving up and recording why. This bounds a diagnostic, not the readiness condition:
// hydration follows the app chunks, which load before `load` fires, so on a real carrier the
// wait ends long before this.
export const CARRIER_GRACE_MS = 15000;
const CARRIER_POLL_MS = 50;
const OLD_BUILDER_CLASSES = ["k-fab", "k-pn"]; // builder_bundle.js root nodes
export const OVERLAY_CLASS = "f-host";

export function onEntryPath(loc = location) {
  return loc.pathname === ENTRY_PATH || loc.pathname.startsWith(ENTRY_PATH + "/");
}

// ---------------------------------------------------------------- the per-tab marker
function readArm(win) {
  try { return JSON.parse(win.sessionStorage.getItem(ARM_KEY) || "null"); } catch { return null; }
}
export function isArmed(win) { const a = readArm(win); return !!(a && a.armed); }
export function armHops(win) { const a = readArm(win); return a && Number.isInteger(a.hops) ? a.hops : 0; }
/** The diagnostic recorded by the last failed host attempt in this tab, or null. */
export function armFailure(win) { const a = readArm(win); return a && typeof a.failure === "string" ? a.failure : null; }

/**
 * Arm this tab and count the hop. Returns the hop count after arming.
 *   hops     null counts one more hop; a number sets the counter (0 = a host reached stability).
 *   failure  undefined keeps the recorded diagnostic, null clears it, a string records one.
 */
export function arm(win, { hops = null, failure = undefined } = {}) {
  const next = hops == null ? armHops(win) + 1 : hops;
  const record = { armed: true, hops: next };
  const kept = failure === undefined ? armFailure(win) : failure;
  if (typeof kept === "string" && kept) record.failure = kept;
  try { win.sessionStorage.setItem(ARM_KEY, JSON.stringify(record)); } catch { /* private mode: the redirect still happens, activation just will not stick */ }
  return next;
}
export function disarm(win) { try { win.sessionStorage.removeItem(ARM_KEY); } catch { /* nothing to clean up */ } }

// ---------------------------------------------------------------- the entry page
/**
 * The /forge entry. The document here is the providerless 404, so it is stopped and emptied as
 * before; the difference is that nothing is mounted into it. The caller redirects.
 */
export function entryTakeover(doc = document, win = window) {
  try { win.stop(); } catch { /* not fatal */ }
  const html = doc.documentElement || doc.appendChild(doc.createElement("html"));
  clear(html);
  const head = h("head", {}, h("meta", { charset: "utf-8" }), h("meta", { name: "viewport", content: "width=device-width, initial-scale=1, viewport-fit=cover" }), h("title", {}, "TNR forge"));
  const body = h("body", {});
  html.append(head, body);
  return { html, head, body };
}

// ---------------------------------------------------------------- the carrier page
/**
 * Wait until the carrier document actually HAS a body.
 *
 * The loader runs at document-start and now matches the whole origin. On the entry page that is
 * harmless, because entryTakeover() builds its own body - but the carrier is the real app
 * document, and at document-start a normal page is not guaranteed to have been parsed as far as
 * <body> yet. mountHost() reads doc.body, so calling it too early throws, the top-level boot
 * wrapper swallows the rejection, and the operator is left looking at the game with the tab still
 * armed and Forge never mounted. That is independent review FPA-1, and it defeats the repair in
 * exactly the workflow the repair exists for.
 *
 * document-start is still the right run-at: it is what lets the entry page be stopped before it
 * renders. The fix is to wait here rather than to run later.
 *
 * Nothing is written to the page while waiting. Three signals race, because a userscript sandbox
 * may support any subset of them, and every one of them re-checks doc.body rather than assuming
 * the event means what it says:
 *   - a MutationObserver on documentElement, which sees the parser insert <body>;
 *   - DOMContentLoaded / readystatechange, for the case where the body already arrived;
 *   - an interval, only when MutationObserver could not be constructed at all.
 * Whichever fires first resolves exactly once; the others are torn down.
 *
 * There is deliberately no timeout. A document that never gets a body is one Forge must not
 * touch, and staying pending leaves the page untouched, which is the safe failure.
 */
export function whenBodyReady(doc = document, win = window) {
  return new Promise((resolve) => {
    if (doc.body) return resolve(doc.body);
    let settled = false;
    let mo = null;
    let timer = null;
    const cleanup = () => {
      if (mo) { try { mo.disconnect(); } catch { /* already gone */ } mo = null; }
      if (timer != null) { try { win.clearInterval(timer); } catch { /* already gone */ } timer = null; }
      try { doc.removeEventListener("DOMContentLoaded", check); } catch { /* not supported */ }
      try { doc.removeEventListener("readystatechange", check); } catch { /* not supported */ }
    };
    function check() {
      if (settled || !doc.body) return;   // an event is a hint, doc.body is the answer
      settled = true;
      cleanup();
      resolve(doc.body);
    }
    try {
      mo = new win.MutationObserver(check);
      mo.observe(doc.documentElement || doc, { childList: true, subtree: true });
    } catch { mo = null; }
    try { doc.addEventListener("DOMContentLoaded", check); } catch { /* not supported */ }
    try { doc.addEventListener("readystatechange", check); } catch { /* not supported */ }
    if (!mo) { try { timer = win.setInterval(check, 25); } catch { timer = null; } }
    check();   // the body may have arrived between the first test and the listeners going up
  });
}

/**
 * Has the page's framework taken ownership of <body>? react-dom stamps every DOM node it
 * hydrates or creates with an own property whose name starts with __reactFiber$ (and a sibling
 * __reactProps$): ReactDOMComponentTree's internalInstanceKey / internalPropsKey, present in
 * react-dom 17, 18 and 19.2.8. For <body> the stamp lands when React completes the body element -
 * after every child under it hydrated, or during the client-render commit that replaces them -
 * and the root container is cleared at most once, on that first commit. So once this is true a
 * node appended to body is outside anything React will ever reconcile.
 *
 * Reads property NAMES only; nothing of React's internals is dereferenced or kept.
 */
export function carrierHydrated(doc = document) {
  const body = doc.body;
  if (!body) return false;
  let keys;
  try { keys = Object.keys(body); } catch { return false; }
  return keys.some((k) => k.startsWith("__reactFiber$") || k.startsWith("__reactProps$"));
}

/**
 * The fallback readiness signal, for a carrier whose framework stopped stamping its nodes: the
 * page's own auth runtime finished starting (clerk-js is loaded by ClerkProvider's client code,
 * so its `loaded` flag proves the provider tree has run on the client) on a document that has
 * fully loaded. It is not equated with DOM stability - it is only accepted after the primary
 * signal has had every chance to appear, and the host-loss watcher stands behind it.
 */
export function carrierRuntimeSettled(doc = document, win = window) {
  if (doc.readyState !== "complete") return false;
  const c = win && win.Clerk;
  return !!(c && c.loaded === true);
}

/** null while the carrier is not ready; otherwise which signal said it was. */
export function carrierReadiness(doc = document, win = window) {
  if (!doc.body) return null;
  if (carrierHydrated(doc)) return "hydrated";
  if (carrierRuntimeSettled(doc, win)) return "runtime";
  return null;
}

/**
 * Wait until the carrier is safe for a persistent external overlay (see carrierReadiness).
 *
 * The primary signal is a JavaScript property, which no DOM observer can see, so this samples:
 * a MutationObserver on documentElement (hydration and the parser both mutate the tree, and a
 * check is cheap), readystatechange/DOMContentLoaded/load, and an interval. Whichever finds the
 * carrier ready resolves exactly once with the signal's name; the rest are torn down.
 *
 * Unlike whenBodyReady this does give up, but only AFTER the document has fully loaded and a
 * grace period has passed with no readiness: it resolves null, nothing has been written to the
 * page, and the caller records why so the /forge splash can say it. Resolving null rather than
 * mounting anyway is the point - an overlay that hydration will delete is worse than none.
 */
export function whenCarrierReady(doc = document, win = window, { graceMs = CARRIER_GRACE_MS, pollMs = CARRIER_POLL_MS } = {}) {
  return new Promise((resolve) => {
    const now = carrierReadiness(doc, win);
    if (now) return resolve(now);
    let settled = false;
    let mo = null;
    let timer = null;
    let deadline = null;
    const cleanup = () => {
      if (mo) { try { mo.disconnect(); } catch { /* already gone */ } mo = null; }
      if (timer != null) { try { win.clearInterval(timer); } catch { /* already gone */ } timer = null; }
      if (deadline != null) { try { win.clearTimeout(deadline); } catch { /* already gone */ } deadline = null; }
      for (const ev of ["DOMContentLoaded", "readystatechange"]) { try { doc.removeEventListener(ev, check); } catch { /* not supported */ } }
      try { win.removeEventListener("load", check); } catch { /* not supported */ }
    };
    const finish = (value) => { if (settled) return; settled = true; cleanup(); resolve(value); };
    function check() {
      if (settled) return;
      const via = carrierReadiness(doc, win);
      if (via) return finish(via);
      // the grace period starts when the document is complete, not when Forge started waiting
      if (deadline == null && doc.readyState === "complete") {
        try { deadline = win.setTimeout(() => finish(null), graceMs); } catch { deadline = null; }
      }
    }
    try {
      mo = new win.MutationObserver(check);
      mo.observe(doc.documentElement || doc, { childList: true, subtree: true });
    } catch { mo = null; }
    for (const ev of ["DOMContentLoaded", "readystatechange"]) { try { doc.addEventListener(ev, check); } catch { /* not supported */ } }
    try { win.addEventListener("load", check); } catch { /* not supported */ }
    try { timer = win.setInterval(check, pollMs); } catch { timer = null; }
    check();
  });
}

/** Is Forge already mounted in this document? One overlay per document, always. */
export function alreadyMounted(doc = document) { return !!doc.querySelector("." + OVERLAY_CLASS); }

/**
 * Mount point on a live application route. One fixed, opaque, full-screen element appended to
 * the body, plus a scroll lock on the carrier while it is up. Nothing is removed, no provider is
 * unmounted, no game node is touched; release() puts the page back exactly as it was.
 *
 * The old builder's loader matches the whole origin at document-idle and appends its panel here
 * too. Its root nodes are removed WHILE FORGE IS MOUNTED only, which is the contract 0.3.0
 * already had ("both scripts can stay installed"), and the observer is disconnected on release
 * so the operator gets the old builder back on this page the moment Forge is closed.
 *
 * onLost, when given, is called once if the host leaves the document without release() - the
 * body observer sees it removed, or the documentElement observer sees <body> itself replaced.
 * Both observers are disconnected BEFORE the callback runs, so the lost host never reports
 * twice and a release() that follows has nothing left to fight.
 */
export function mountHost(doc = document, win = window, { onLost = null } = {}) {
  const host = h("div", { class: OVERLAY_CLASS });
  const root = doc.documentElement;
  const body = doc.body;
  const prevHtmlOverflow = root ? root.style.overflow : "";
  const prevBodyOverflow = body ? body.style.overflow : "";
  if (root) root.style.overflow = "hidden";
  if (body) body.style.overflow = "hidden";
  body.appendChild(host);

  let bodyMo = null;
  let rootMo = null;
  let released = false;
  let lost = false;
  const disconnect = () => {
    if (bodyMo) { try { bodyMo.disconnect(); } catch { /* already gone */ } bodyMo = null; }
    if (rootMo) { try { rootMo.disconnect(); } catch { /* already gone */ } rootMo = null; }
  };
  const attached = () => !released && host.isConnected && doc.body === body && body.contains(host);
  const reportLost = () => {
    if (released || lost || attached()) return;
    lost = true;
    disconnect();
    if (onLost) { try { onLost(host); } catch { /* the caller's problem, not the page's */ } }
  };
  try {
    bodyMo = new win.MutationObserver((muts) => {
      for (const m of muts) {
        for (const n of m.addedNodes) {
          if (n && n.nodeType === 1 && OLD_BUILDER_CLASSES.some((c) => n.classList && n.classList.contains(c))) n.remove();
        }
        for (const n of m.removedNodes) if (n === host) return reportLost();
      }
    });
    bodyMo.observe(body, { childList: true });
  } catch { bodyMo = null; }
  try {
    rootMo = new win.MutationObserver(() => { if (doc.body !== body) reportLost(); });
    if (root) rootMo.observe(root, { childList: true });
  } catch { rootMo = null; }

  const release = () => {
    released = true;
    disconnect();
    host.remove();
    if (root) root.style.overflow = prevHtmlOverflow;
    if (doc.body) doc.body.style.overflow = prevBodyOverflow;
  };
  return { body: host, observer: bodyMo, attached, release };
}

/**
 * The page's own auth runtime, read as three booleans and nothing else. clerk-js publishes
 * window.Clerk when ClerkProvider mounts; `loaded` says its startup finished and the PRESENCE of
 * `session`/`user` says somebody is signed in. No token, no cookie, no claim is read here, and
 * nothing read here is stored - AuthState keeps only its own state string.
 */
export function pageAuthRuntime(win = window) {
  return () => {
    const c = win && win.Clerk;
    if (!c) return null;
    const loaded = c.loaded === true;
    let signedIn = null;
    if (loaded) signedIn = !!(c.session || c.user);
    return { loaded, signedIn };
  };
}
