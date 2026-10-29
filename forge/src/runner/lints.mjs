// The safety and content-integrity lints, ported from the repository's current sources
// (readiness brief section 5a): builder_bundle.js v4.32 `lintRun` (:622-662) and
// skills/building-tnr-content/scripts/validate.py (:930-1025, :1120-1131), which are the two
// halves of the same generated rule set (13_LINT_rules). Each check names the lint it carries.
//
// Three deliberate differences from the builder's copy, each with a reason:
//
//  1. `skipPreflight` does NOT bypass these. In the builder it disables the whole lint pass,
//     which is why a partial quest edit (an entry with no `content`) had to turn off enum and
//     bounds checking for the entire manifest (state/status.json, open item). Here every check
//     fires only on data the entry actually carries, so a partial edit needs no bypass and a
//     safety rule cannot be switched off by a manifest.
//  2. L09 (per-tag illegal effect field) is not here. It was a hand-maintained whitelist; the
//     nested unknown-key check derives the same surface from the pinned validators instead.
//  3. L18's "clear/copy are excluded from the item union" half is NOT ported. docs/RULINGS.md
//     records that law 19 is CONTRADICTED at source: neither refiner mentions clear or copy, so
//     enforcing it would reject payloads the server accepts - the same mistake as the 45g power
//     cap. The noncombatconsumereward half IS ported and was re-verified at the pin
//     (app/src/validators/combat.ts:1151-1163: CONSUMABLE, target SELF, method SINGLE).

const DATE_RE = /^\d{4}-\d{1,2}-\d{1,2}$/;
const DASH_RE = /[–—]/;
const IMG_REF_RE = /@img:([A-Za-z0-9_.\-]+)/g;

// preferredStat is NOT required: migration 0056 dropped the column (live rows have no such key), so
// requiring it forced every AI create to send a key the server strips and Forge's read-back then
// reports as drift. It stays an accepted key (pinned field set) for manifests that still send it.
const AI_CREATE_REQUIRED = ["rank", "regeneration", "preferredGeneral1", "preferredGeneral2"];
const FORMULA_TAGS = new Set(["damage", "pierce", "wound"]);            // L06
const PCT_TAGS = new Set(["increasedamagegiven", "decreasedamagetaken", "increasedamagetaken"]); // L08
const DIRECTIONS = { redirection: ["push", "pull"], increasestat: ["offence", "defence", "both"], decreasestat: ["offence", "defence", "both"] };

/**
 * Lint one parsed manifest. Pure, no I/O.
 * @param {{items: Array, imgSizes: object}} manifest  from parseManifest, pool codes already resolved
 * @returns {{errors: string[], warnings: string[]}}
 */
export function lintManifest(manifest) {
  const errors = [], warnings = [];
  const items = manifest.items ?? [];
  const E = (it, m) => errors.push(`item ${it.idx} (${it.name}): ${m}`);
  const W = (it, m) => warnings.push(`item ${it.idx} (${it.name}): ${m}`);

  // srcIds of jutsu an item's injectjutsus effect wraps: those must be hidden:false, not true
  const wrapped = new Set();
  for (const it of items) {
    if (it.entity !== "item") continue;
    for (const f of Array.isArray(it.data.effects) ? it.data.effects : []) {
      if (!f || f.type !== "injectjutsus") continue;
      for (const m of JSON.stringify(f).matchAll(/@jutsu:([A-Za-z0-9_\-]+)/g)) wrapped.add(m[1]);
    }
  }

  for (const it of items) {
    const d = it.data ?? {};

    // L13 (law 16b): a half-built row must not be player-visible, so every create ships hidden.
    // The one exception is a wrapper jutsu an item injects, which must be visible to be injected.
    // The repo rule says "every entity; where the column does not exist the key is stripped
    // harmlessly" - but an ai has no `hidden` column at the pin (insertAiSchema over userData,
    // 157 keys, no hidden), and forge refuses unknown keys before a create, so demanding it on an
    // ai create would demand a key its own validator rejects. An ai create is therefore not
    // required to carry it; carrying `hidden: true` anyway is accepted (see validate.mjs) and a
    // deliberate `hidden: false` is still refused.
    if (it.op === "create") {
      if (it.entity === "jutsu" && it.srcId && wrapped.has(it.srcId)) {
        if (d.hidden !== false) E(it, "L13 injectjutsus wrapper must be hidden:false");
      } else if (it.entity === "ai" || it.entity === "aiProfile") {
        if ("hidden" in d && d.hidden !== true) E(it, "L13 create with hidden:" + JSON.stringify(d.hidden));
      } else if (d.hidden !== true) {
        E(it, "L13 create without hidden:true");
      }
    }

    if (it.entity === "quest") {
      if (it.op === "create" && d.consecutiveObjectives !== true) E(it, "L03 quest create needs consecutiveObjectives:true");
      for (const k of ["startsAt", "endsAt"]) {
        if (k in d && d[k] && !DATE_RE.test(String(d[k]))) E(it, `L04 ${k} must be plain YYYY-MM-DD`);
      }
      const objs = (d.content && Array.isArray(d.content.objectives)) ? d.content.objectives : null;
      if (objs && objs.length) lintObjectives(objs, it, E, W);
    }

    if (it.entity === "ai" && it.op === "create") {
      for (const k of AI_CREATE_REQUIRED) if (!(k in d)) E(it, `L05 AI create missing ${k}`);
    }

    if (it.entity === "jutsu") {
      if (d.cooldown != null && d.cooldown < 3) E(it, `L16 cooldown ${d.cooldown} below floor 3`);
      if (d.actionCostPerc != null && d.actionCostPerc > 70) W(it, `L10 EP ${d.actionCostPerc} above signature ceiling 70`);
    }

    const pct = {};
    for (const f of Array.isArray(d.effects) ? d.effects : []) {
      if (!f || !f.type) continue;
      if (FORMULA_TAGS.has(f.type) && (!Array.isArray(f.statTypes) || !f.statTypes.length || !Array.isArray(f.generalTypes) || !f.generalTypes.length)) {
        W(it, `L06 ${f.type} missing statTypes/generalTypes (a generalTypes gap can explode damage)`);
      }
      if ("direction" in f) {
        const ok = DIRECTIONS[f.type] ?? ["offence", "defence"];
        if (!ok.includes(f.direction)) E(it, `L07 ${f.type} direction "${f.direction}" (allowed: ${ok.join("/")})`);
      }
      if (f.type === "stun" && !("apReduction" in f)) W(it, "L15 stun without apReduction (defaults 10)");
      if (PCT_TAGS.has(f.type) && (f.calculation === "percentage" || !f.calculation)) pct[f.type] = (pct[f.type] ?? 0) + 1;
      if (it.entity === "item" && f.type === "noncombatconsumereward") {
        // combat.ts:1151-1163 at the pin, three separate addIssue() calls
        if (d.itemType !== undefined && d.itemType !== "CONSUMABLE") E(it, "L18 noncombatconsumereward requires itemType CONSUMABLE");
        if (d.target !== undefined && d.target !== "SELF") E(it, "L18 noncombatconsumereward requires item target SELF");
        if (d.method !== undefined && d.method !== "SINGLE") E(it, "L18 noncombatconsumereward requires method SINGLE");
        // combat.ts:867-893 at 2af4b320: pet grants require standard rewards
        if (Array.isArray(f.reward_pets) && f.reward_pets.length && f.rewardMode === "weightedCache") E(it, "PET reward_pets requires rewardMode standard");
      }
    }
    // combat.ts:1547-1559 at 2af4b320: the companion cap counts reward_pets across ALL of the item's
    // noncombatconsumereward effects, and any grant requires the item to prevent battle usage
    if (it.entity === "item") {
      const pets = (Array.isArray(d.effects) ? d.effects : []).reduce((n, f) => n + (f && f.type === "noncombatconsumereward" && Array.isArray(f.reward_pets) ? f.reward_pets.length : 0), 0);
      if (pets > 1) E(it, `PET an item may grant at most 1 companion (${pets} across its effects)`);
      if (pets && (d.preventBattleUsage === false || (it.op === "create" && d.preventBattleUsage !== true))) E(it, "PET companion rewards require preventBattleUsage true");
    }
    for (const [tp, n] of Object.entries(pct)) {
      if (n <= 4) continue;
      let p = 1;
      for (const f of d.effects) if (f && f.type === tp && (f.calculation === "percentage" || !f.calculation)) p *= 1 + (f.power ?? 0) / 100;
      W(it, `L08 ${n} ${tp} rows: product x${p.toFixed(1)}`);
    }
  }

  // PET (RUL-2026-10-28-012): species defaults must be published, compatible PETS jutsu
  // (routers/petSpecies.ts:56-67, :113-125 at 2af4b320). Every jutsu CREATED in this manifest ships
  // hidden, so naming one as a default is refused by the server; a create also refuses any
  // species-locked default, and an edit accepts only jutsu locked to that species.
  const jutsuBySrc = new Map(items.filter((it) => it.entity === "jutsu" && it.srcId).map((it) => [it.srcId, it]));
  for (const it of items) {
    if (it.entity !== "petSpecies" || !Array.isArray(it.data?.defaultJutsuIds)) continue;
    for (const ref of it.data.defaultJutsuIds) {
      const j = typeof ref === "string" && ref.startsWith("@jutsu:") ? jutsuBySrc.get(ref.slice(7)) : null;
      if (!j) continue;
      if (j.op === "create") E(it, `PET default ${ref} is created hidden in this manifest; the server refuses unpublished defaults. Publish it, then set the defaults in a later manifest`);
      const lock = j.data?.requiredPetSpeciesId;
      if (lock && it.op === "create") E(it, `PET default ${ref} is species-locked; a species create accepts only unlocked PETS jutsu`);
      // a ref names a species by srcId, the edit by literal id: only two literal ids are comparable offline
      if (lock && it.op === "update" && !lock.startsWith("@") && lock !== it.targetId) E(it, `PET default ${ref} is locked to another species (${lock})`);
    }
  }

  // TITLE (titleRewards.ts:9-37 at 2af4b320): quest and item saves refuse reward_titles naming an
  // archived title, so a title this manifest archives cannot be rewarded by it
  for (const t of items) if (t.entity === "title" && t.data?.archived === true) {
    const ref = JSON.stringify(t.op === "create" ? "@title:" + t.srcId : t.targetId);
    for (const it of items) if (JSON.stringify(it.data ?? {}).match(/"reward_titles":\[[^\]]*\]/g)?.some((m) => m.includes(ref))) E(it, `TITLE ${ref} is archived in this manifest; the server refuses rewarding it`);
  }

  // VARIANT (routers/item.ts at 3314d122, src/runner/variants.mjs). A token item's unlockitemvariant
  // names the variant it unlocks (variantId: null = any token variant without a required item); the
  // item must be a consumable destroyed on use, SELF/SINGLE, battle use prevented (SuperRefineItem).
  // At a variant's CREATE the server accepts a requiredItemId only if that item's unlockitemvariant has
  // a null variantId (the new id does not exist yet), so a 1:1 trophy is: token (variantId null),
  // variant (requiredItemId), then a token edit setting variantId.
  const bySrc = new Map(items.filter((it) => it.srcId).map((it) => [it.srcId, it]));
  const slots = new Set();
  for (const it of items) {
    const d = it.data ?? {}, unlock = (Array.isArray(d.effects) ? d.effects : []).filter((f) => f && f.type === "unlockitemvariant");
    if (it.entity === "item" && unlock.length) {
      for (const f of unlock) if (f.variantId != null && !(typeof f.variantId === "string" && (/^@variant:./.test(f.variantId) || /^[\w-]{21}$/.test(f.variantId)))) E(it, `VARIANT variantId ${JSON.stringify(f.variantId)}: null, a variant id or an @variant ref`);
      const need = { itemType: "CONSUMABLE", target: "SELF", method: "SINGLE", destroyOnUse: true, preventBattleUsage: true };
      for (const [k, v] of Object.entries(need)) if (d[k] !== undefined ? d[k] !== v : it.op === "create" && typeof v === "boolean") E(it, `VARIANT unlockitemvariant requires ${k} ${v}`);
    }
    if (it.entity !== "itemVariant" || it.op !== "create") continue;
    const key = JSON.stringify([d.itemId, d.order]);
    if (slots.has(key)) E(it, `VARIANT two variant creates on ${d.itemId} at order ${d.order}; (itemId, order) is unique`);
    slots.add(key);
    if (d.costType !== "VARIANT_TOKEN") W(it, `VARIANT costType ${d.costType}: a variant has no hidden switch, so owners of the item can buy it as soon as it exists`);
    else if (d.requiredItemId == null) W(it, "VARIANT no requiredItemId: any token whose unlockitemvariant has no variantId (every older Variant Token) unlocks it");
    const tok = typeof d.requiredItemId === "string" && d.requiredItemId.startsWith("@item:") ? bySrc.get(d.requiredItemId.slice(6)) : null;
    if (tok && tok.op === "create") {
      const fx = (Array.isArray(tok.data?.effects) ? tok.data.effects : []).filter((f) => f && f.type === "unlockitemvariant");
      if (!fx.some((f) => f.variantId == null)) E(it, `VARIANT ${d.requiredItemId} needs an unlockitemvariant with variantId null when this variant is created; set the variantId in a later edit of the token`);
    }
  }

  // L17: the Android picker matches a file by size when the name differs, so every @img ref needs
  // a byte entry or the upload cannot be checked against the file on disk.
  const sizes = manifest.imgSizes ?? {};
  const needed = new Set();
  for (const m of JSON.stringify(items).matchAll(IMG_REF_RE)) if (!(m[1] in sizes)) needed.add(m[1]);
  for (const f of needed) errors.push(`L17 @img:${f} has no imgSizes byte entry`);

  return { errors, warnings };
}

/** L11 (dialog dashes) and L12b (reachability) over one quest's objective graph. */
function lintObjectives(objs, it, E, W) {
  const edges = {}, incoming = {}, wins = [];
  for (const o of objs) {
    if (!o || !o.id) continue;
    const targets = [];
    const n = o.nextObjectiveId;
    if (typeof n === "string") targets.push(n);
    else if (Array.isArray(n)) for (const c of n) if (c && c.nextObjectiveId) targets.push(c.nextObjectiveId);
    if (o.failObjectiveId) targets.push(o.failObjectiveId);
    edges[o.id] = targets.filter(Boolean);
    for (const t of edges[o.id]) incoming[t] = 1;
    if (o.task === "win_quest") wins.push(o.id);
    const text = (o.description ?? "") + (Array.isArray(n) ? n.map((c) => (c && c.text) || "").join(" ") : "");
    if (DASH_RE.test(text)) E(it, `L11 em/en dash in dialog node ${o.id}`);
  }
  const first = objs.find((o) => o && o.id);
  if (!first) return;
  const seen = {}, stack = [first.id];
  while (stack.length) {
    const u = stack.pop();
    if (seen[u]) continue;
    seen[u] = 1;
    for (const x of edges[u] ?? []) stack.push(x);
  }
  for (const w of wins) if (!seen[w]) E(it, `L12b win node ${w} unreachable from the first objective`);
  for (const o of objs) if (o && o.id && !seen[o.id] && o.id !== first.id) W(it, `L12b orphan node ${o.id} (unreachable)`);
}
