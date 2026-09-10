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
// though: the marker is a per-tab flag, not a URL, so if the app redirects "/" somewhere else
// for a signed-in operator, Forge activates on wherever it lands. That is deliberate - the
// carrier constant is a hint, and being wrong about it costs a navigation, not the repair.
//
// The overlay covers the carrier; it does not restyle it. The stylesheet is scoped to .f-app
// and the document reset is installed on the entry splash only, so the game page underneath is
// returned exactly as it was when Forge is closed.

import { h, clear } from "./dom.mjs";

export const ENTRY_PATH = "/forge";
export const CARRIER_PATH = "/";
// Per-TAB, in sessionStorage: a second tab is not dragged into Forge, and closing the tab ends
// it. It holds a hop counter and nothing else - no auth material, no session data, no id.
export const ARM_KEY = "tnr_forge_armed_v1";
export const MAX_HOPS = 2; // a redirect that lands somewhere unexpected must not loop
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

/** Arm this tab and count the hop. Returns the hop count after arming. */
export function arm(win, { hops = null } = {}) {
  const next = hops == null ? armHops(win) + 1 : hops;
  try { win.sessionStorage.setItem(ARM_KEY, JSON.stringify({ armed: true, hops: next })); } catch { /* private mode: the redirect still happens, activation just will not stick */ }
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
 * Mount point on a live application route. One fixed, opaque, full-screen element appended to
 * the body, plus a scroll lock on the carrier while it is up. Nothing is removed, no provider is
 * unmounted, no game node is touched; release() puts the page back exactly as it was.
 *
 * The old builder's loader matches the whole origin at document-idle and appends its panel here
 * too. Its root nodes are removed WHILE FORGE IS MOUNTED only, which is the contract 0.3.0
 * already had ("both scripts can stay installed"), and the observer is disconnected on release
 * so the operator gets the old builder back on this page the moment Forge is closed.
 */
export function mountHost(doc = document, win = window) {
  const host = h("div", { class: OVERLAY_CLASS });
  const root = doc.documentElement;
  const prevHtmlOverflow = root ? root.style.overflow : "";
  const prevBodyOverflow = doc.body ? doc.body.style.overflow : "";
  if (root) root.style.overflow = "hidden";
  if (doc.body) doc.body.style.overflow = "hidden";
  doc.body.appendChild(host);

  let mo = null;
  try {
    mo = new win.MutationObserver((muts) => {
      for (const m of muts) for (const n of m.addedNodes) {
        if (n && n.nodeType === 1 && OLD_BUILDER_CLASSES.some((c) => n.classList && n.classList.contains(c))) n.remove();
      }
    });
    mo.observe(doc.body, { childList: true });
  } catch { mo = null; }

  const release = () => {
    if (mo) { try { mo.disconnect(); } catch { /* already gone */ } }
    host.remove();
    if (root) root.style.overflow = prevHtmlOverflow;
    if (doc.body) doc.body.style.overflow = prevBodyOverflow;
  };
  return { body: host, observer: mo, release };
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
