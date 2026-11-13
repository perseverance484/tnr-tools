// livePatch: an edit whose new effects are derived from the live record at send time, so a
// manifest can change one key across a large record without carrying the record (job 593, the
// Mother of Echoes 2.5x pass: 57 jutsu, ~800 KB of effects). The runner still sends the whole
// record (full-record updates); only the derivation moves from the manifest to the send.
//
// Shape (an edit item):  "livePatch": {"animationScale": 2.5, "assets": ["<asset id>", ...]}
// Effect i is patched iff one of its appear/static/disappear animations is a listed asset; every
// other effect, and every other key, is sent exactly as live holds it.

export const LIVE_PATCH_ENTITIES = Object.freeze(["jutsu", "item", "bloodline"]);
const ANIM = ["appearAnimation", "staticAnimation", "disappearAnimation"];

/** Structural problems with an item's livePatch (parse time). */
export function livePatchProblems(it) {
  const p = it.livePatch, out = [];
  if (!p || typeof p !== "object" || Array.isArray(p)) return ["livePatch must be an object"];
  if (it.op !== "update") out.push("livePatch is only for an edit (targetId)");
  if (!LIVE_PATCH_ENTITIES.includes(it.entity)) out.push(`livePatch takes ${LIVE_PATCH_ENTITIES.join(", ")}, not ${it.entity}`);
  if ("effects" in (it.data ?? {})) out.push("livePatch derives effects from live; do not also send data.effects");
  const extra = Object.keys(p).filter((k) => !["animationScale", "assets"].includes(k));
  if (extra.length) out.push(`livePatch does not know ${extra.join(", ")}`);
  const s = p.animationScale;
  if (typeof s !== "number" || !Number.isFinite(s) || s < 1 || s > 3) out.push("livePatch.animationScale must be a number from 1 to 3");
  if (!Array.isArray(p.assets) || !p.assets.length || !p.assets.every((a) => typeof a === "string" && a)) out.push("livePatch.assets must list at least one asset id");
  return out;
}

const targeted = (e, assets) => e && typeof e === "object" && ANIM.some((k) => typeof e[k] === "string" && assets.has(e[k]));
// An effect whose OTHER animation slots carry an unlisted clip: it is scaled as a whole, so the
// unlisted clip grows too. Reported, not refused, so the operator can see it in the journal.
const mixed = (e, assets) => ANIM.some((k) => typeof e[k] === "string" && e[k] && !assets.has(e[k]));

/**
 * Apply the patch to a live row. Returns {data: {effects}, targeted, changed, mixed}; changed 0
 * means live already holds the patch (the write is then a no-op); targeted 0 means
 * no effect uses a listed asset, which the runner refuses as a wrong target or asset list.
 */
export function applyLivePatch(patch, live) {
  const effects = Array.isArray(live?.effects) ? live.effects : null;
  if (!effects) throw new Error("livePatch: the live record has no effects array");
  const assets = new Set(patch.assets);
  let changed = 0, mix = 0, hit = 0;
  const next = effects.map((e) => {
    if (!targeted(e, assets)) return e;
    hit++;
    if (mixed(e, assets)) mix++;
    if (e.animationScale === patch.animationScale) return e;
    changed++;
    return { ...e, animationScale: patch.animationScale };
  });
  return { data: { effects: next }, targeted: hit, changed, mixed: mix };
}

/** Read-back check: every targeted effect holds the scale. [] when it all landed. */
export function livePatchDiffs(patch, live) {
  if (!patch) return [];
  const effects = Array.isArray(live?.effects) ? live.effects : [];
  const assets = new Set(patch.assets);
  const off = effects.map((e, i) => [i, e]).filter(([, e]) => targeted(e, assets) && e.animationScale !== patch.animationScale);
  return off.length ? [{ key: "effects.animationScale", sent: patch.animationScale, live: off.map(([i, e]) => ({ i, animationScale: e.animationScale ?? null })) }] : [];
}
