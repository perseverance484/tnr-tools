// Read-only content census (docs/handoffs/ELEMENTALDAMAGE_WEAPON_CENSUS_CAPTURE_IMPLEMENTATION_20261020.md).
//
// A census answers "which records of this kind exist RIGHT NOW, in every visibility partition",
// which no capture list can: a manifest names its reads in advance, and the whole point here is
// that nobody knows the ids in advance. It runs in two stages inside one ordinary Forge job:
//
//   Stage A  inventory. Pages the game's own list query (item.getAll) through the budgeted
//            reader for EVERY partition, twice, and keeps only a field-allowlisted PROJECTION of
//            each row (projectRow). The raw list body is never stored or exported: the full-
//            persistence boundary in storage/captures.mjs (FULL_PERSIST_PATHS) is unchanged and
//            still admits point reads only.
//   Stage B  full point reads. Every inventoried row whose parsed effects carry the census tag
//            gets one item.get through the existing persist:"full" snapshot path, and is checked
//            against its own inventory row.
//
// Nothing here can write. Both procedures are public queries in the audited registry; a kind
// that named anything else is refused by assertCensusKinds() at module load.
//
// Source contract, studie-tech/TheNinjaRPG@6524d0fbd7c0b80ecfd28ca63e9c4becdfb210eb (routers/item.ts and
// validators/item.ts are byte-identical at 85cecae, the Forge contract pin since PR #76):
//   item.getAll   routers/item.ts:1101-1132  publicProcedure, input itemFilteringSchema +
//                 {cursor: number nullish, limit: 1..500}; offset = cursor * limit; ordered by
//                 cost, repsCost, id; nextCursor = rows < limit ? null : cursor + 1.
//   hidden        routers/item.ts:4452-4455  an absent `hidden` is eq(hidden, false): a crawl that
//                 omits it silently skips every hidden record. Both partitions are always sent.
//   effect        routers/item.ts:4418-4428  JSON_SEARCH(effects,'one',x): ANY string value equal
//                 to x anywhere in the effects document, not effects[*].type. That is why the
//                 filtered query is only a cross-check and the exact tag test is done here.
//   item.get      routers/item.ts:347-360    publicProcedure; a missing row answers null.

import { procedure } from "../transport/procedures.mjs";
import { stableStringify, fnv1a32 } from "../storage/hash.mjs";

export const CENSUS_KINDS = Object.freeze({
  "item.weapon.elementaldamage": Object.freeze({
    listPath: "item.getAll", getPath: "item.get", itemType: "WEAPON", tag: "elementaldamage",
    partitions: Object.freeze([false, true]),
  }),
});
export const DEFAULT_PAGE_LIMIT = 100;
// item.getAll's own ceiling (validators/item.ts itemFilteringSchema limit max 500).
const MAX_PAGE_LIMIT = 500;
// A crawl that has not terminated after this many pages of one partition is not a crawl.
const MAX_PAGES = 2000;

for (const [k, v] of Object.entries(CENSUS_KINDS)) {
  for (const p of [v.listPath, v.getPath]) {
    const proc = procedure(p);
    if (proc.kind !== "query" || proc.auth !== "public") throw new Error(`census ${k}: ${p} is not a public query`);
  }
}

/** Validate a manifest's `census` block. Returns {kind, pageLimit} or a list of problems. */
export function normalizeCensus(raw) {
  if (!raw || typeof raw !== "object" || Array.isArray(raw)) return { problems: ["census must be an object {kind, pageLimit?}"] };
  const problems = [];
  if (!CENSUS_KINDS[raw.kind]) problems.push(`census.kind must be one of ${Object.keys(CENSUS_KINDS).join(", ")}`);
  const pageLimit = raw.pageLimit ?? DEFAULT_PAGE_LIMIT;
  if (!Number.isInteger(pageLimit) || pageLimit < 1 || pageLimit > MAX_PAGE_LIMIT) problems.push(`census.pageLimit must be an integer 1-${MAX_PAGE_LIMIT}`);
  const extra = Object.keys(raw).filter((k) => !["kind", "pageLimit"].includes(k));
  if (extra.length) problems.push(`census takes only kind and pageLimit, not ${extra.join(", ")}`);
  return problems.length ? { problems } : { kind: raw.kind, pageLimit };
}

// superjson decodes timestamps to Date; the bundle and the ledger compare ISO strings.
export const iso = (v) => (v instanceof Date ? v.toISOString() : v ?? null);

/**
 * The ONLY fields of a list row that are kept. Everything else in the row is dropped here, so no
 * list body, and nothing that is not item content, can reach storage or the bundle by this path.
 */
export function projectRow(row) {
  const fx = row?.effects;
  const ok = Array.isArray(fx);
  const types = ok ? fx.map(effectType) : null;
  return {
    id: row?.id ?? null, name: typeof row?.name === "string" ? row.name : null,
    itemType: row?.itemType ?? null, hidden: row?.hidden ?? null, updatedAt: iso(row?.updatedAt),
    effectTypes: types,
    // Malformed is the whole effects value OR any one member: `[null]`, `[{power:30}]` and
    // `["elementaldamage"]` cannot be ruled out as the tag, so such a row is captured, never
    // silently dropped from the target set (census review F1).
    effectsMalformed: !ok || types.some((t) => t === null),
  };
}

/** A member's type when it is a plain object with a non-empty string `type`, else null. */
export const effectType = (e) =>
  (e && typeof e === "object" && !Array.isArray(e) && typeof e.type === "string" && e.type ? e.type : null);

const hasTag = (row, tag) => !!row.effectTypes?.includes(tag);

/**
 * Page one partition to nextCursor:null. Every page is checked against the source contract; the
 * first contract violation stops the crawl with a problem rather than a guess. A failed read
 * (ok:false) does the same. RateLimited and transport errors propagate: the job pauses and Stage
 * A restarts from cursor 0 on resume, because half an offset crawl proves nothing.
 */
async function crawl(page, k, hidden, limit, extra, seen, checkpoint) {
  const rows = [], pages = [];
  for (let cursor = 0; ; cursor++) {
    if (cursor >= MAX_PAGES) return { problem: `hidden:${hidden}: no terminating page after ${MAX_PAGES} pages` };
    const input = { itemType: k.itemType, hidden, ...extra, limit, cursor };
    // Before EVERY page read: the runner's Pause throws here (census review F3). Nothing of a
    // half-finished Stage A is kept, so the resume crawls again from cursor 0.
    checkpoint?.({ hidden, cursor, filtered: !!extra.effect });
    const r = await page(input);
    const where = `hidden:${hidden}${extra.effect ? " (filtered)" : ""} cursor ${cursor}`;
    if (!r.ok) return { problem: `${where}: read failed ${r.error?.code ?? "?"}: ${r.error?.message ?? ""}` };
    const d = r.data;
    if (!d || !Array.isArray(d.data) || !("nextCursor" in d)) return { problem: `${where}: malformed page (expected {data:[], nextCursor})` };
    const n = d.data.length, next = d.nextCursor;
    pages.push({ hidden, cursor, rows: n, nextCursor: next ?? null });
    if (n > limit) return { problem: `${where}: ${n} rows for limit ${limit}` };
    // nextCursor is null exactly when the page is short (routers/item.ts:1127).
    if (n < limit ? next != null : next !== cursor + 1) return { problem: `${where}: nextCursor ${JSON.stringify(next)} after ${n}/${limit} rows` };
    for (const raw of d.data) {
      const row = projectRow(raw);
      if (typeof row.id !== "string" || !row.id) return { problem: `${where}: row without an id` };
      if (row.itemType !== k.itemType) return { problem: `${where}: ${row.id} is ${row.itemType}, not ${k.itemType}` };
      if (row.hidden !== hidden) return { problem: `${where}: ${row.id} has hidden:${row.hidden} in the hidden:${hidden} partition` };
      if (seen.has(row.id)) return { problem: `${where}: ${row.id} repeated (rows shifted under the crawl)` };
      seen.add(row.id); rows.push(row);
    }
    if (next == null) return { rows, pages };
  }
}

async function scan(page, k, limit, extra = {}, checkpoint) {
  const seen = new Set(), rows = [], pages = [];
  for (const hidden of k.partitions) {
    const c = await crawl(page, k, hidden, limit, extra, seen, checkpoint);
    if (c.pages) pages.push(...c.pages);
    if (c.problem) return { problem: c.problem, pages };
    rows.push(...c.rows);
  }
  return { rows, pages };
}

const byId = (rows) => new Map(rows.map((r) => [r.id, r]));
function scanDiff(a, b) {
  const A = byId(a), B = byId(b), cap = (x) => x.slice(0, 50);
  return {
    added: cap([...B.keys()].filter((id) => !A.has(id))),
    removed: cap([...A.keys()].filter((id) => !B.has(id))),
    changed: cap([...B.keys()].filter((id) => A.has(id) && stableStringify(A.get(id)) !== stableStringify(B.get(id)))),
    reordered: a.length === b.length && a.some((r, i) => r.id !== b[i].id),
  };
}

/**
 * Stage A. Two complete unfiltered scans that must agree exactly (an offset crawl is not a
 * snapshot, so one pass cannot be called complete), then one tag-filtered scan as a cross-check.
 * Returns the projection rows plus a summary; `inventory` is "COMPLETE", "UNSTABLE" or "FAILED".
 */
export async function runInventory(page, { kind, pageLimit }, { checkpoint } = {}) {
  const k = CENSUS_KINDS[kind];
  const out = { inventory: "FAILED", problems: [], scans: [], rows: [], targets: [] };
  for (let n = 0; n < 2; n++) {
    const s = await scan(page, k, pageLimit, {}, checkpoint);
    out.scans.push({ pages: s.pages, rows: s.rows?.length ?? null, digest: s.rows ? digest(s.rows) : null });
    if (s.problem) { out.problems.push(`scan ${n + 1}: ${s.problem}`); return out; }
    out.rows = n ? out.rows : s.rows;
    if (n && digest(s.rows) !== out.scans[0].digest) {
      out.inventory = "UNSTABLE";
      out.diff = scanDiff(out.rows, s.rows);
      out.problems.push("the two complete scans disagree; records changed during the census. Coordinate editing and run a fresh census.");
      return out;
    }
  }
  const rows = out.rows;
  const f = await scan(page, k, pageLimit, { effect: [k.tag] }, checkpoint);
  const exact = rows.filter((r) => hasTag(r, k.tag)).map((r) => r.id);
  if (f.problem) out.problems.push(`cross-check: ${f.problem}`);
  else {
    const fIds = new Set(f.rows.map((r) => r.id)), inv = byId(rows);
    out.crossCheck = {
      filteredRows: f.rows.length,
      // a row the server's string search finds but whose effects carry no such TYPE: expected
      // when the word appears as some other value; listed so it is seen, never treated as a hit
      filterOnly: [...fIds].filter((id) => !exact.includes(id)).sort(),
      // an exact hit the server's own filter misses, or a filtered row missing from the inventory:
      // either means the two answers are not of the same population, so nothing is complete
      missedByFilter: exact.filter((id) => !fIds.has(id)).sort(),
      notInInventory: [...fIds].filter((id) => !inv.has(id)).sort(),
    };
    if (out.crossCheck.missedByFilter.length || out.crossCheck.notInInventory.length) out.problems.push("cross-check: the tag-filtered crawl and the inventory disagree");
  }
  out.counts = Object.fromEntries(k.partitions.map((h) => [`hidden:${h}`, rows.filter((r) => r.hidden === h).length]));
  out.counts.total = rows.length;
  out.counts.tagged = exact.length;
  out.counts.malformed = rows.filter((r) => r.effectsMalformed).length;
  out.digest = digest(rows);
  // A row whose effects could not be read is captured too: it cannot be ruled out.
  out.targets = rows.filter((r) => hasTag(r, k.tag) || r.effectsMalformed)
    .map((r) => ({ id: r.id, updatedAt: r.updatedAt, reason: r.effectsMalformed ? "effectsMalformed" : k.tag }))
    .sort((a, b) => (a.id < b.id ? -1 : a.id > b.id ? 1 : 0));
  if (!out.problems.length) out.inventory = "COMPLETE";
  return out;
}

export const digest = (rows) => "fnv1a32:" + fnv1a32(stableStringify(rows));

/**
 * Stage B acceptance of ONE point read, per the brief: read ok, one row, body persisted, same id,
 * right type, an effects array, the tag still present, and the same updatedAt the inventory saw.
 * A changed updatedAt is STALE: the body is kept (it is what the game said), but it is not the
 * record the inventory classified, so it needs a recapture before anything is decided from it.
 */
export function acceptPoint(kind, target, r, entry) {
  const k = CENSUS_KINDS[kind], d = r.ok ? r.data : null, problems = [];
  if (!r.ok) problems.push(`read failed ${r.error?.code ?? ""}`);
  else if (!d) problems.push("record not found (item.get answered null)");
  else {
    if (d.id !== target.id) problems.push(`answered id ${d.id}`);
    if (d.itemType !== k.itemType) problems.push(`itemType ${d.itemType}`);
    // A malformed target is read to CAPTURE its body as evidence: whatever shape it has is what
    // the game holds, so it is not refused here. It can never make the census COMPLETE: the
    // verdict is AMBIGUOUS until someone resolves it explicitly (storage/journal.mjs censusVerdict).
    if (target.reason !== "effectsMalformed") {
      if (!Array.isArray(d.effects)) problems.push("effects is not an array");
      else if (!d.effects.some((e) => effectType(e) === k.tag)) problems.push(`no ${k.tag} effect any more`);
    }
  }
  if (entry.persistOk !== true) problems.push(`body not persisted: ${entry.persistError ?? "?"}`);
  const stale = !!d && iso(d.updatedAt) !== target.updatedAt;
  if (stale) problems.push(`STALE: updatedAt ${iso(d.updatedAt)} != inventoried ${target.updatedAt}; recapture required`);
  return { updatedAt: d ? iso(d.updatedAt) : null, expectUpdatedAt: target.updatedAt, stale, accepted: !problems.length, problems };
}
