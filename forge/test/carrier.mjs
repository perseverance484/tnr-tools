// Doubles for the carrier's framework (state/prompt_forge_disappearing_overlay.md).
//
// The game hydrates the whole document: app/src/app/layout.tsx renders <html> and <body> as React
// elements, so react-dom's hydrateRoot(document, ...) walks the server-rendered body children and
// matches them against the client tree. hydrateLikeReact() below models the three react-dom@19.2.8
// behaviours that carrier.react.test.mjs verifies against the real package, so the lifecycle tests
// can drive them synchronously and at chosen moments:
//
//   1. <body> is a singleton scope: a foreign child whose TAG does not match the next expected
//      element is skipped (canHydrateInstance with inRootOrSingleton), and unhydrated tail nodes
//      are left alone (popHydrationState exempts HostSingleton). This is why a host appended
//      before the game's first <script>, or after everything, survives in React 19.
//   2. A foreign child whose tag DOES match is claimed as that element; its children then fail
//      to match and hydration throws. React recovers by client-rendering the root, which runs
//      clearContainerSparingly() - every body child that is not a <script>, <style> or stylesheet
//      <link> is removed - and acquireSingletonInstance() - the singleton's attributes are stripped
//      and its props re-applied - before the tree is rendered fresh with new node identities.
//   3. Whichever path ran, react-dom stamps the nodes it owns with own properties named
//      __reactFiber$<key> / __reactProps$<key> (ReactDOMComponentTree). That stamp on <body> is
//      the readiness signal takeover.mjs waits for; the container is cleared at most once, on
//      that first commit, so a node appended afterwards is never reconciled.
//
// No React is imported here; nothing here reaches a network.

export const FIBER_KEY = "__reactFiber$fake";
export const PROPS_KEY = "__reactProps$fake";

/** What react-dom's first commit leaves on <body>: the ownership stamp, and nothing else. */
export function stampHydrated(doc) {
  if (!doc.body) throw new Error("no body to stamp");
  doc.body[FIBER_KEY] = { tag: "HostSingleton" };
  doc.body[PROPS_KEY] = { className: "h-full" };
}
export function isStamped(doc) { return !!(doc.body && Object.keys(doc.body).some((k) => k.startsWith("__reactFiber$"))); }

/** The game's server-rendered body children, as the React tree expects them, in order. */
export const SHELL = [
  { tag: "script", attrs: { type: "application/ld+json" }, text: "{}" },   // StructuredData
  { tag: "div", attrs: { id: "__next" }, text: "the game" },              // the layout shell
  { tag: "section", attrs: { "aria-label": "toasts" } },                  // Toaster
];

/** Render SHELL into a document as the parser would have. Returns the nodes in order. */
export function parseShell(doc, into = doc.body, shell = SHELL) {
  return shell.map((s) => { const el = doc.createElement(s.tag); for (const [k, v] of Object.entries(s.attrs || {})) el.setAttribute(k, v); if (s.text) el.textContent = s.text; into.appendChild(el); return el; });
}

/**
 * React hydrating a document root whose body was server-rendered from `shell`.
 * Returns { fallback, reason } and stamps body either way.
 */
export function hydrateLikeReact(doc, shell = SHELL, { onRecoverableError = null } = {}) {
  const body = doc.body;
  let next = body.firstElementChild;
  let reason = null;
  for (const want of shell) {
    // behaviour 1: inside the body singleton, mismatched tags are skipped, not deleted
    while (next && next.tagName.toLowerCase() !== want.tag) next = next.nextElementSibling;
    if (!next) { reason = `expected <${want.tag}> was not found`; break; }
    // behaviour 2: the first tag match is claimed; a stranger's children then fail to match
    const expectedId = want.attrs && want.attrs.id;
    if (expectedId && next.id !== expectedId) { reason = `claimed a foreign <${want.tag}> as #${expectedId}`; break; }
    next = next.nextElementSibling;
  }
  if (!reason) { stampHydrated(doc); return { fallback: false, reason: null }; }
  if (onRecoverableError) onRecoverableError(new Error("Hydration failed because the server rendered HTML didn't match the client: " + reason));
  // client-render fallback: clearContainerSparingly on body ...
  for (const node of [...body.childNodes]) {
    const n = node.nodeName;
    if (n === "SCRIPT" || n === "STYLE" || (n === "LINK" && String(node.rel).toLowerCase() === "stylesheet")) continue;
    body.removeChild(node);
  }
  // ... acquireSingletonInstance on <html> and <body>: attributes stripped, props re-applied ...
  for (const el of [doc.documentElement, body]) for (const a of [...el.attributes]) el.removeAttribute(a.name);
  doc.documentElement.setAttribute("lang", "en");
  body.className = "h-full";
  // ... and the tree rendered fresh, with new identities.
  parseShell(doc, body, shell.filter((s) => s.tag !== "script"));
  stampHydrated(doc);
  return { fallback: true, reason };
}

/** HomeLanding's router.push("/profile"): a client navigation that re-renders inside the shell. */
export function clientNavigate(win, path = "/profile") {
  win.history.pushState({}, "", path);
  const shell = win.document.getElementById("__next");
  if (shell) shell.textContent = "profile page";
  return shell;
}
