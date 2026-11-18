// livePatch: an edit whose new effects are derived from the live record at send time, so a
// manifest can change one key across a large record without carrying the record (job 593, the
// Mother of Echoes 2.5x pass: 57 jutsu, ~800 KB of effects). The runner still sends the whole
// record (full-record updates); only the derivation moves from the manifest to the send.
//
// Shape (an edit item):  "livePatch": {"animationScale": 2.5, "assets": ["<asset id>", ...]}
// Effect i is patched iff one of its appear/static/disappear animations is a listed asset; every
// other effect, and every other key, is sent exactly as live holds it.
//
// Second kind:  "livePatch": {"zeroInstantResidual": true}
// Sets residualModifier to 0 on every instant damage effect (type damage, pierce or
// elementaldamage with rounds exactly 0). The modifier only scales damage on rounds after the
// cast, so on an instant hit it changes nothing in combat; but the residual equip cap counts any
// nonzero residualModifier on any effect (game source libs/jutsu.ts matchesJutsuCategory), so it
// files an instant hit as a residual jutsu. Effects with rounds > 0, or no rounds at all, are real
// damage over time and pass through untouched; `mixed` counts the ones that still carry a nonzero
// modifier (the jutsu still counts as residual after the patch).

export const LIVE_PATCH_ENTITIES = Object.freeze(["jutsu", "item", "bloodline"]);
const ANIM = ["appearAnimation", "staticAnimation", "disappearAnimation"];

const DAMAGE_TYPES = new Set(["damage", "pierce", "elementaldamage"]);
const isResidualKind = (p) => p && typeof p === "object" && "zeroInstantResidual" in p;
const instantHit = (e) => e && typeof e === "object" && DAMAGE_TYPES.has(e.type) && e.rounds === 0;
const residualLeft = (e) => e && typeof e === "object" && DAMAGE_TYPES.has(e.type) && e.rounds !== 0 && !!e.residualModifier;

/** Structural problems with an item's livePatch (parse time). */
export function livePatchProblems(it) {
  const p = it.livePatch, out = [];
  if (!p || typeof p !== "object" || Array.isArray(p)) return ["livePatch must be an object"];
  if (it.op !== "update") out.push("livePatch is only for an edit (targetId)");
  if (!LIVE_PATCH_ENTITIES.includes(it.entity)) out.push(`livePatch takes ${LIVE_PATCH_ENTITIES.join(", ")}, not ${it.entity}`);
  if ("effects" in (it.data ?? {})) out.push("livePatch derives effects from live; do not also send data.effects");
  if (isResidualKind(p)) {
    const extra = Object.keys(p).filter((k) => k !== "zeroInstantResidual");
    if (extra.length) out.push(`livePatch does not know ${extra.join(", ")} alongside zeroInstantResidual`);
    if (p.zeroInstantResidual !== true) out.push("livePatch.zeroInstantResidual must be true");
    return out;
  }
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
  if (isResidualKind(patch)) {
    let changed = 0, hit = 0;
    const next = effects.map((e) => {
      if (!instantHit(e)) return e;
      hit++;
      if (!e.residualModifier) return e;
      changed++;
      return { ...e, residualModifier: 0 };
    });
    return { data: { effects: next }, targeted: hit, changed, mixed: effects.filter(residualLeft).length };
  }
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

/**
 * Read-back check: [] only when the live record has an effects array, at least one effect uses a
 * listed asset, and every such effect holds the scale. A record whose targets are gone is a diff,
 * never a match (review P2-1).
 */
export function livePatchDiffs(patch, live) {
  if (!patch) return [];
  if (!Array.isArray(live?.effects)) return [{ key: "effects", sent: "livePatch target", live: "no effects array" }];
  if (isResidualKind(patch)) {
    const hit = live.effects.map((e, i) => [i, e]).filter(([, e]) => instantHit(e));
    if (!hit.length) return [{ key: "effects.residualModifier", sent: 0, live: "no instant damage effect" }];
    const off = hit.filter(([, e]) => !!e.residualModifier);
    return off.length ? [{ key: "effects.residualModifier", sent: 0, live: off.map(([i, e]) => ({ i, residualModifier: e.residualModifier })) }] : [];
  }
  const assets = new Set(patch.assets);
  const hit = live.effects.map((e, i) => [i, e]).filter(([, e]) => targeted(e, assets));
  if (!hit.length) return [{ key: "effects.animationScale", sent: patch.animationScale, live: "no effect uses a listed asset" }];
  const off = hit.filter(([, e]) => e.animationScale !== patch.animationScale);
  return off.length ? [{ key: "effects.animationScale", sent: patch.animationScale, live: off.map(([i, e]) => ({ i, animationScale: e.animationScale ?? null })) }] : [];
}

/** The refusal when a patch finds nothing to act on (the runner fails the item unsent). */
export const livePatchMissMessage = (patch) => isResidualKind(patch)
  ? "livePatch: the live record has no instant damage effect (damage, pierce or elementaldamage with rounds 0); check the target"
  : "livePatch: no effect on the live record uses a listed asset; check the target and asset list";
