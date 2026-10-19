// Does an image URL actually load? Asked in the operator's browser, where the game's images are
// served, by loading it into a detached <img>. An upload can be reported as done and then be
// deleted by the game (its moderation step removes the file when it cannot check it), so a URL
// on record is evidence of nothing until it loads.
//
// Answers true (loaded), false (failed to load) or null (no answer in time). Callers treat only
// false as dead: a probe that cannot decide must not trigger a re-upload storm. A failure is
// therefore confirmed by a second, cache-busted load after a pause, and an offline browser
// answers null, so a network blip cannot make a whole pack look dead.
export function browserImageProbe(win, { timeoutMs = 15000, confirmDelayMs = 1500 } = {}) {
  const seen = new Map();
  const load = (src) => new Promise((resolve) => {
    const img = new win.Image();
    const done = (v) => { win.clearTimeout(timer); img.onload = img.onerror = null; resolve(v); };
    const timer = win.setTimeout(() => done(null), timeoutMs);
    img.onload = () => done(img.naturalWidth > 0);
    img.onerror = () => done(false);
    img.src = src;
  });
  const offline = () => win.navigator && win.navigator.onLine === false;
  return (url) => {
    if (typeof url !== "string" || !/^https:\/\//.test(url)) return Promise.resolve(false);
    if (seen.has(url)) return seen.get(url);
    const answer = (async () => {
      if (offline()) return null;
      const first = await load(url);
      if (first !== false) return first;
      await new Promise((r) => win.setTimeout(r, confirmDelayMs));
      if (offline()) return null;
      return load(`${url}${url.includes("?") ? "&" : "?"}forge-probe=${Date.now()}`);
    })();
    // A definite answer is kept for the session; an undecided one may be asked again.
    seen.set(url, answer.then((v) => { if (v === null) seen.delete(url); return v; }));
    return seen.get(url);
  };
}
