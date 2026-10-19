// Does an image URL actually load? Asked in the operator's browser, where the game's images are
// served, by loading it into a detached <img>. An upload can be reported as done and then be
// deleted by the game (its moderation step removes the file when it cannot check it), so a URL
// on record is evidence of nothing until it loads.
//
// Answers true (loaded), false (failed to load) or null (no answer in time). Callers treat only
// false as dead: a probe that cannot decide must not trigger a re-upload storm.
export function browserImageProbe(win, { timeoutMs = 15000 } = {}) {
  const seen = new Map();
  return (url) => {
    if (typeof url !== "string" || !/^https:\/\//.test(url)) return Promise.resolve(false);
    if (seen.has(url)) return seen.get(url);
    const answer = new Promise((resolve) => {
      const img = new win.Image();
      const done = (v) => { win.clearTimeout(timer); img.onload = img.onerror = null; resolve(v); };
      const timer = win.setTimeout(() => done(null), timeoutMs);
      img.onload = () => done(img.naturalWidth > 0);
      img.onerror = () => done(false);
      img.src = url;
    });
    // A definite answer is kept for the session; an undecided one may be asked again.
    seen.set(url, answer.then((v) => { if (v === null) seen.delete(url); return v; }));
    return seen.get(url);
  };
}
