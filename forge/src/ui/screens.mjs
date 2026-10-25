// The five screens (spec section 11). Each is a function (app) => Element and re-renders on
// app.refresh(). Errors are surfaced in the UI with context; nothing is only in the console.
import { h, replace, fmtAgo, fmtBytes, fmtCountdown } from "./dom.mjs";
import { manifestNumber, manifestSummary, GH } from "../github.mjs";
import { readGh, writeGh, readIdmap } from "../storage/compat.mjs";
import { unresolvedBloodrightJob } from "../bloodright/jobs.mjs";
import { jobOutcome } from "../storage/journal.mjs";
import { imagePicks, unusablePicks } from "../core/facts.mjs";
import { packGateProblems } from "../core/imagepack.mjs";
import { packBinds } from "../runner/imgpack.mjs";

const pill = (state) => h("span", { class: "f-pill " + state }, state);
const plural = (n, one, many = one + "s") => `${n} ${n === 1 ? one : many}`;
const base = (p) => String(p || "").replace(/^push\//, "");
const TERMINAL = ["VERIFIED", "FAILED", "SKIPPED"];

// Pause reasons in the operator's words. The code itself stays in the journal and the bundle.
const PAUSE_WORDS = {
  USER: "Paused by you", SESSION: "Paused: signed out of the game", NETWORK: "Paused: connection problem",
  TOO_MANY_REQUESTS: "Paused: game rate limit reached", ORPHANED: "Paused: an item needs your decision",
  DEPENDENCY: "Paused: waiting on an earlier item", UNDECODABLE_RESPONSE: "Paused: unreadable game reply",
  AMBIGUOUS: "Paused: last write uncertain", VISIBILITY: "Paused: record not visible",
  STALE_PREVIEW: "Paused: a record changed since the preview", STALE_BINDINGS: "Paused: saved IDs out of date",
  UNRESOLVED_IMPORT: "Paused: earlier import unresolved",
};
export const pauseWords = (pause) => PAUSE_WORDS[pause.reason] ?? `Paused (${pause.reason})`;

/** What a job is, in words: the manifest, or the collection tree and bloodline it imported. */
export function jobLabel(job) {
  if (job.collection) return `${base(job.collection.path)} · tree ${job.collection.index + 1}/${job.collection.total}${job.collection.name ? ` · ${job.collection.name}` : ""}`;
  if (job.bloodrightImport) return `Bloodright · ${job.bloodlineName || job.bloodrightImport.bloodlineId}`;
  return base(job.manifestPath) || job.jobId;
}

/** A job's pill: its outcome once finished, and INTERRUPTED for a run that is no longer running. */
function jobPill(app, job) {
  if (job.state === "RUNNING" && app.state.running !== job.jobId) return h("span", { class: "f-pill PAUSED" }, "INTERRUPTED");
  if (job.state === "DONE") {
    const outcome = jobOutcome(job);
    if (outcome === "failed") return h("span", { class: "f-pill FAILED" }, "FAILURES");
    if (outcome === "unverified") return h("span", { class: "f-pill INCOMPLETE" }, "UNVERIFIED");
  }
  return pill(job.state);
}

const resumeLabel = (job) => job.items.some((i) => i.state === "SENT") ? "Reconcile & resume" : job.state === "INCOMPLETE" ? "Re-read unverified items" : "Resume";

function jobRow(app, j) {
  const counts = {}; for (const it of j.items) counts[it.state] = (counts[it.state] ?? 0) + 1;
  return h("div", { class: "f-row f-tap", onClick: () => app.go("run", { jobId: j.jobId }) },
    h("div", { class: "f-grow" }, h("div", {}, jobLabel(j), " ", jobPill(app, j)),
      h("div", { class: "f-mute" }, `${plural(j.items.length, "item")}${j.items.length ? ` · ${Object.entries(counts).map(([k, v]) => `${v} ${k.toLowerCase()}`).join(", ")}` : ""} · ${fmtAgo(j.startedAt, app.now())}`)));
}

// ------------------------------------------------------------------ 1. Jobs
export function JobsScreen(app) {
  const jobs = app.journal.listJobs();
  const open = app.journal.resumable();
  const orphans = jobs.flatMap((j) => j.items.filter((it) => it.state === "ORPHANED").map((it) => ({ job: j, it })));
  const root = h("section", {});
  for (const j of open) {
    const blockedReason = app.resumeBlockedReason ? app.resumeBlockedReason(j) : null;
    root.appendChild(h("div", { class: "f-banner warn" },
      h("div", {}, h("b", {}, "Open job: "), jobLabel(j), " ", jobPill(app, j)),
      j.state === "INCOMPLETE" ? h("div", { class: "f-mute" }, `Finished unverified: ${plural(j.items.filter((i) => !TERMINAL.includes(i.state)).length, "item")} still to read back. Resuming only re-reads; it cannot re-send.`) : null,
      j.pause ? h("div", { class: "f-mute" }, `${pauseWords(j.pause)}${j.pause.path ? " on " + j.pause.path : ""}${j.pause.until ? " · retry allowed in " + fmtCountdown(j.pause.until, app.now()) : ""}${j.pause.detail ? " · " + j.pause.detail : ""}`) : null,
      blockedReason ? h("div", { class: "f-err" }, blockedReason) : null,
      h("div", { class: "f-actions" },
        h("button", { class: "f-primary", disabled: !!blockedReason, onClick: () => app.resumeJob(j.jobId) }, resumeLabel(j)),
        h("button", { onClick: () => app.go("run", { jobId: j.jobId }) }, "Open"))));
  }
  if (orphans.length) {
    root.appendChild(h("h2", {}, `Orphans needing a decision (${orphans.length})`));
    for (const { job, it } of orphans) root.appendChild(OrphanCard(app, job, it));
  }
  root.appendChild(h("h2", {}, "Recent runs"));
  if (!jobs.length) root.appendChild(h("div", { class: "f-mute" }, "No jobs yet. Pick a manifest to start one."));
  // A collection's trees are one run to the operator: they fold under one line instead of filling
  // the list (and pushing older runs off it) one tree at a time.
  const rows = [], groups = new Map();
  for (const j of jobs) {
    const g = j.collection?.id;
    if (!g) { rows.push({ job: j }); continue; }
    if (!groups.has(g)) { groups.set(g, []); rows.push({ group: g }); }
    groups.get(g).push(j);
  }
  for (const r of rows.slice(0, 20)) {
    if (r.job) { root.appendChild(jobRow(app, r.job)); continue; }
    const trees = groups.get(r.group).sort((a, b) => a.collection.index - b.collection.index);
    const first = trees[0], ok = trees.filter((j) => j.state === "DONE" && jobOutcome(j) === "success").length;
    root.appendChild(h("details", { class: "f-group" },
      h("summary", {}, `${base(first.collection.path)} · collection · ${ok}/${first.collection.total} trees verified · ${fmtAgo(first.startedAt, app.now())}`),
      trees.map((j) => jobRow(app, j))));
  }
  return root;
}

function OrphanCard(app, job, it) {
  const cands = it.candidates || [];
  const card = h("div", { class: "f-card" },
    h("div", {}, h("b", {}, it.name), " ", h("span", { class: "f-mute" }, `${it.entity} · ${jobLabel(job)} · item ${it.idx + 1}`)),
    h("div", { class: "f-mute" }, it.error || "ambiguous"),
  );
  if (cands.length) {
    card.appendChild(h("h3", {}, "Candidates on the server"));
    for (const c of cands) {
      const id = typeof c === "string" ? c : c.id;
      const name = typeof c === "string" ? "" : c.name;
      // a dungeon candidate carries its comparison with the planned content; it is read back, never re-saved
      const evidence = typeof c === "object" && c.matches !== undefined ? (c.matches ? "matches the planned content (may still be someone else's)" : `differs on ${c.differs.join(", ")}`) : null;
      card.appendChild(h("div", { class: "f-row" },
        h("div", { class: "f-grow" }, h("div", { class: "f-mono" }, id), name ? h("div", { class: "f-mute" }, name) : null, evidence ? h("div", { class: "f-mute" }, evidence) : null),
        h("button", { onClick: () => app.confirm(`Adopt ${id} as "${it.name}"? ${evidence ? "It will be read back and verified; nothing is saved again." : "The job will continue with its update."}`, () => app.adopt(job.jobId, it.idx, id)) }, "Adopt"),
      ));
    }
  } else if (it.op === "create" || !it.entityId) {
    const inp = h("input", { type: "text", placeholder: "paste an id to adopt" });
    card.appendChild(h("div", { class: "f-actions" }, inp, h("button", { onClick: () => { const v = inp.value.trim(); if (v) app.confirm(`Adopt ${v}?`, () => app.adopt(job.jobId, it.idx, v)); } }, "Adopt id")));
  } else {
    card.appendChild(h("div", { class: "f-actions" },
      h("button", { onClick: () => app.confirm(`Re-send the ${it.phase} for "${it.name}" to ${it.entityId}? Only do this if you have checked the record.`, () => app.adopt(job.jobId, it.idx, it.entityId)) }, `Re-send ${it.phase}`)));
  }
  card.appendChild(h("div", { class: "f-actions" }, h("button", { class: "f-danger", onClick: () => app.confirm(`Skip "${it.name}"? Nothing is deleted; the server row (if any) stays.`, () => app.skip(job.jobId, it.idx)) }, "Skip (leave as is)")));
  return card;
}

// ------------------------------------------------------------------ 2. Manifests
function summaryText(e) {
  if (!e.summary) return e.loading ? "loading…" : e.error || "";
  const x = e.summary;
  if (x.trees) return `${x.title} · ${plural(x.trees, "tree")} · ${plural(x.skills, "skill")}`;
  return `${x.title || "(untitled)"} · ${plural(x.items, "item")}${x.creates ? ` (${x.creates} new)` : ""}${x.captures ? ` · ${plural(x.captures, "capture")}` : ""}`;
}

function listingHint(error) {
  return /HTTP 40[13]/.test(error)
    ? " GitHub refused the listing. Wait a few minutes (GitHub limits reads without a token) or add a GitHub token in Settings, then tap Refresh."
    : " Check the connection, then tap Refresh.";
}

export function ManifestsScreen(app) {
  const root = h("section", {});
  const q = h("input", { type: "search", placeholder: "search filename, number, title", value: app.view.pickerQuery || "", onInput: (e) => { app.view.pickerQuery = e.target.value; renderList(); } });
  const list = h("div", {});
  const status = h("div", { class: "f-mute" });
  root.append(h("div", { class: "f-actions" }, q, h("button", { onClick: () => app.loadPicker(true) }, "Refresh")));
  // The open manifest sits above the list, so Start is reachable without scrolling past every file.
  if (app.state.selected) root.appendChild(SelectedManifest(app));
  else if (app.state.opening) root.appendChild(h("div", { class: "f-card" }, h("h2", {}, app.state.opening.name),
    h("div", { class: "f-banner info" }, `Preparing: ${app.state.opening.step}… Nothing is written yet.`)));
  else if (app.state.openError) root.appendChild(h("div", { class: "f-card" }, h("h2", {}, app.state.openError.name),
    h("div", { class: "f-banner bad" }, h("b", {}, "Could not open: "), h("div", { class: "f-err" }, app.state.openError.text)),
    h("div", { class: "f-actions" }, h("button", { onClick: () => app.clearSelection() }, "Clear"))));
  root.append(status, list);
  const current = app.state.selected?.entry?.name ?? app.state.opening?.name ?? app.state.openError?.name ?? null;
  // Summaries arrive one file at a time. While the set of rows is unchanged only their text is
  // updated in place, so a row is never swapped out from under a finger mid-tap.
  const texts = new Map();
  let shown = null;
  function renderList() {
    const entries = app.state.picker || [];
    const needle = (app.view.pickerQuery || "").toLowerCase();
    const seen = new Set(app.journal.listJobs().map((j) => j.collection?.path ?? j.manifestPath));
    const rows = entries.filter((e) => !needle || e.name.toLowerCase().includes(needle) || String(e.number ?? "").includes(needle) || (e.summary?.title || "").toLowerCase().includes(needle));
    const key = rows.map((e) => e.path).join("\n");
    if (key === shown && rows.length) {
      for (const e of rows) { const t = texts.get(e.path), want = summaryText(e); if (t && t.textContent !== want) t.textContent = want; }
    } else {
      shown = key; texts.clear();
      replace(list, rows.length ? rows.map((e) => {
        const text = h("div", { class: "f-mute" }, summaryText(e));
        texts.set(e.path, text);
        return h("div", { class: "f-row f-tap" + (e.name === current ? " f-sel" : ""), onClick: () => app.selectManifest(e) },
          h("div", { class: "f-grow" },
            h("div", {}, e.number != null ? h("b", {}, "#" + e.number + " ") : null, e.name, seen.has(e.path) ? h("span", { class: "f-pill VERIFIED", style: { marginLeft: "6px" } }, "ran") : null),
            text));
      }) : h("div", { class: "f-mute" }, app.state.pickerError ? "" : "nothing matches"));
    }
    replace(status, app.state.pickerError
      ? h("div", { class: "f-banner bad" }, h("b", {}, "Could not list manifests: "), app.state.pickerError, listingHint(app.state.pickerError))
      : `${plural(entries.length, "manifest")}` + (app.state.pickerAt ? ` · listed ${fmtAgo(app.state.pickerAt, app.now())}` : ""));
  }
  renderList();
  app.view.renderPicker = renderList;
  if (!app.state.picker) app.loadPicker(false);
  return root;
}

/**
 * How a manifest's captures read on screen BEFORE it is run. "5 captures" and "5 full captures"
 * are different contracts - the second one writes five exact record bodies into a results bundle
 * that is committed to the repository - so they must never render the same way.
 */
export function captureLabel(captures) {
  const n = captures.length;
  if (!n) return "";
  const full = captures.filter((c) => c && c.persist === "full").length;
  const noun = `capture${n === 1 ? "" : "s"}`;
  if (!full) return `${n} ${noun}`;
  if (full === n) return `${n} full ${noun}`;
  return `${n} ${noun} (${full} full)`;
}

// Lists longer than this fold behind one "Show all" line.
const FOLD_AT = 12;
const fold = (rows, label) => rows.length > FOLD_AT ? [h("details", {}, h("summary", {}, label), rows)] : rows;
/** Whole keys up to ~120 characters, never a key cut mid-word. */
function keysText(data) {
  let out = "";
  for (const k of Object.keys(data)) { if ((out + k).length > 120) return out + "…"; out += (out ? ", " : "") + k; }
  return out;
}

function SelectedManifest(app) {
  const s = app.state.selected;
  const captures = [...s.manifest.capture.before, ...s.manifest.capture.after];
  const captureCount = captures.length;
  const fullCount = captures.filter((c) => c.persist === "full").length;
  const label = captureLabel(captures);
  // Read-only is a property of the MANIFEST (no items, not Bloodright), never of a plan that failed
  // to build: a write manifest whose planning failed must not be offered as a capture job.
  const itemCount = s.manifest.items?.length ?? s.plan.length;
  const readOnly = !s.bloodright && itemCount === 0;
  const count = (entity) => s.plan.filter((i) => i.entity === entity).length;
  const creates = s.plan.filter((i) => i.op === "create").length;
  const imgs = s.images || [];
  const scope = s.collection
    ? `${plural(s.collection.length, "tree")} · ${plural(count("skillTree"), "skill")} · ${plural(count("skillTreeFolder"), "folder")} · ${plural(imgs.length, "icon")}`
    : `${plural(itemCount, "item")}${captureCount ? ` · ${label}` : ""}`;
  const card = h("div", { class: "f-card" }, h("h2", {}, s.entry.name), h("div", { class: "f-mute" }, `${scope}${s.manifest.hash ? ` · manifest hash ${s.manifest.hash}` : ""}`));
  const suggest = !!s.manifest.policy?.suggest;
  if (readOnly) card.appendChild(h("div", { class: "f-banner info" }, "Read-only capture job: zero mutations."));
  if (suggest) card.appendChild(h("div", { class: "f-banner info" }, h("b", {}, "Suggest mode. "), "Each edit goes to the content review desk. Nothing changes in the game until a reviewer approves it."));
  if (fullCount) card.appendChild(h("div", { class: "f-banner warn" },
    h("b", {}, `${fullCount} full capture${fullCount === 1 ? "" : "s"}. `),
    `Each exact record body goes into the results bundle (committed to the repository when GitHub sync is on).${readOnly ? " Still queries only; zero mutations." : ""} Paths: ${[...new Set(captures.filter((c) => c.persist === "full").map((c) => c.proc))].join(", ")}.`));
  if (s.problems.length) card.appendChild(h("div", { class: "f-banner bad" }, h("b", {}, "Cannot run: "), h("div", { class: "f-err" }, s.problems.join("\n"))));
  const blocked = app.blockedPaths ? app.blockedPaths(s.plan, s.manifest) : [];
  if (blocked.length) card.appendChild(h("div", { class: "f-banner bad" },
    h("b", {}, "Blocked: TNR authentication is unavailable. "),
    `This manifest needs ${blocked.join(", ")}, which needs a signed-in session. Nothing will be sent. Sign in, then re-check above.`));
  // What the operator has actually selected, judged against the manifest's byte ledger BEFORE the
  // job opens. The picker used to show a green "picked" pill for any file at all, which is how a
  // 1.7 MB master PNG rode into a live run behind the name of a 207 KB .webp and failed five
  // avatar edits one upload at a time (facts.imagePick).
  const picks = imagePicks(imgs, app.runner.files, s.manifest.imgSizes, "imageUploader");
  const pack = s.pack || null;
  const packResult = s.packResult || null;
  const packEntry = (name) => (packResult && packResult.entries ? packResult.entries.find((e) => e.name === name) : null) || null;
  const badImgs = unusablePicks(picks);
  const imagesHead = h("h3", {}, `Images (${imgs.length})`);
  // The same gate startJob() re-reads at the tap, shown here so Start is not merely greyed out.
  const packProblems = packGateProblems(pack, imgs, app.runner);
  if (packProblems.length && pack && !packResult) {
    // Still fetching: this is the normal path, not a refusal.
    card.appendChild(h("div", { class: "f-banner info" }, `Verifying ${plural(packProblems.length, "image")}…`));
  } else if (packProblems.length) {
    card.appendChild(h("div", { class: "f-banner bad" }, h("b", {}, `Cannot run: ${plural(packProblems.length, "repo-backed image")} not verified. `),
      h("details", {}, h("summary", {}, "Show details"), h("div", { class: "f-err" }, packProblems.join("\n"))),
      h("div", { class: "f-actions" }, h("button", { onClick: () => app.prepareImages(true) }, "Re-fetch from repository"))));
  }
  const unpicked = badImgs.filter((p) => !packBinds(pack, p.name));
  if (unpicked.length) card.appendChild(h("div", { class: "f-banner warn" },
    h("b", {}, `Pick ${plural(unpicked.length, "image")} below to enable Start. `), unpicked.map((p) => p.name).join(", "),
    h("div", { class: "f-actions" }, h("button", { onClick: () => imagesHead.scrollIntoView({ block: "start" }) }, "Go to images"))));
  // Start sits near the top of the card, under the reasons it may be refused; the item, preview and
  // image detail follows, so a long plan never pushes the main action off screen.
  card.appendChild(h("div", { class: "f-actions" },
    h("button", { class: "f-primary", disabled: s.problems.length > 0 || badImgs.length > 0 || blocked.length > 0 || packProblems.length > 0, onClick: () => app.confirm(
      readOnly
        ? `Run read-only capture job for ${s.entry.name}: ${label}?${fullCount ? ` ${fullCount} exact record ${fullCount === 1 ? "body is" : "bodies are"} written into the results bundle.` : ""} No mutations will be sent.`
        : s.collection
          ? `Start ${plural(s.collection.length, "Bloodright tree")} (${plural(count("skillTree"), "skill")}, all hidden)? This writes to the game.`
          : suggest ? `Send ${plural(s.plan.length, "suggestion")} from ${s.entry.name} for review? Nothing changes until approved.`
          : `Start ${s.entry.name}: ${plural(s.plan.length, "item")} (${creates} new)${fullCount ? `, ${label}` : ""}? This writes to the game.`,
      () => app.startJob()),
    }, readOnly ? "Run captures" : s.collection ? "Start all trees" : suggest ? "Send for review" : "Start job"),
    h("button", { onClick: () => app.clearSelection() }, "Clear"),
  ));
  if (s.manifest.poolResolved) card.appendChild(h("div", { class: "f-mute" }, `${s.manifest.poolResolved} pool code(s) resolved to ids and gates`));
  // advisories: worth reading, not worth blocking. A blocking lint is already in `problems`.
  if (s.manifest.warnings && s.manifest.warnings.length) {
    card.appendChild(h("div", { class: "f-banner warn" }, h("b", {}, `${plural(s.manifest.warnings.length, "advisory", "advisories")}:`),
      h("ul", { class: "f-list" }, s.manifest.warnings.map((w) => h("li", {}, w)))));
  }
  card.append(...fold(s.plan.map((it) => h("div", { class: "f-row" },
    h("div", { class: "f-grow" }, h("div", {}, `${it.idx + 1}. ${it.name}`), h("div", { class: "f-mute" }, `${it.entity} · ${it.op}${it.targetId ? " → " + it.targetId : ""}${it.deps?.length ? " · after " + [...new Set(it.deps)].join(", ") : ""} · keys: ${keysText(it.data)}`)))), `Show all ${s.plan.length} items`));
  if (s.bloodright) {
    card.appendChild(h("div", { class: "f-banner info" }, s.collection
      ? `${plural(s.collection.length, "Bloodright tree")}, all hidden, run in order; a tree that does not verify stops the rest.`
      : `Bloodright preview · ${s.bloodright.allocations ?? "?"} legal builds · ${s.bloodright.maxAdvanced ?? "?"} reachable Advanced Art(s). New skills stay hidden.`));
    const trees = (s.bloodright.trees ?? []).map((tree) => h("div", { class: "f-mute" }, `${tree.name ?? tree.bloodlineId}: ${tree.allocations} legal builds · ${tree.maxAdvanced} reachable Advanced Art(s)`));
    if (trees.length) card.appendChild(h("details", {}, h("summary", {}, `Tree checks (${trees.length})`), trees));
    card.append(...fold(s.bloodright.preview.map((row) => h("details", {},
      h("summary", {}, `${row.operation}: ${row.name}${row.targetId ? " → " + row.targetId : ""} · ${row.changes.length} changed field(s)`),
      h("pre", { class: "f-err" }, JSON.stringify(row.changes, null, 2)))), `Show all ${s.bloodright.preview.length} preview rows`));
    card.appendChild(h("button", { class: "f-btn", onclick: () => app.selectManifest(s.entry) }, "Refresh Bloodright preview"));
  }
  if (pack) {
    const bound = imgs.filter((n) => packBinds(pack, n));
    const ready = bound.filter((n) => (packEntry(n) || {}).state === "ready").length;
    const kind = !packResult ? "info" : ready === bound.length ? "ok" : "bad";
    card.appendChild(h("div", { class: "f-banner " + kind },
      h("b", {}, `Repo-backed images: ${ready}/${bound.length} verified. `),
      `From ${GH.owner}/${GH.repo} @ ${pack.ref.slice(0, 12)}. Each file is checked against its SHA-256 before upload.`,
      h("div", { class: "f-actions" },
        h("button", { onClick: () => app.prepareImages(true) }, "Re-fetch from repository"))));
  }
  if (imgs.length) {
    card.appendChild(imagesHead);
    const rows = picks.map((p) => {
      const name = p.name;
      const bound = packBinds(pack, name);
      const e = bound ? packEntry(name) : null;
      const inp = h("input", { type: "file", accept: "image/*", style: { display: "none" }, onChange: (ev) => { const f = ev.target.files[0]; if (f) { app.runner.files.set(name, f); app.refresh(); } } });
      const pillFor = { ready: ["VERIFIED", bound ? "verified" : "picked"], refused: ["FAILED", "wrong file"], missing: ["FAILED", bound ? "not fetched" : "missing"] }[p.state];
      return h("div", { class: "f-row" },
        h("div", { class: "f-grow" },
          h("div", { class: "f-mono" }, name, " ", h("span", { class: "f-pill " + pillFor[0] }, pillFor[1])),
          // Provenance, for a bound image, is the whole point: the path, the commit and the digest
          // Forge actually computed, not a claim that it matched.
          bound ? h("div", { class: "f-mute f-mono" },
            `repo: ${pack.files[name].path} @ ${pack.ref.slice(0, 12)} · sha256 ${pack.files[name].sha256.slice(0, 16)}… · ${fmtBytes(pack.files[name].bytes)}${e && e.state === "ready" ? ` · verified from ${e.source}` : ""}`) : null,
          // the physical bytes, always, not only when they are wrong
          p.picked ? h("div", { class: "f-mute f-mono" },
            `selected: ${p.picked.name ?? "(unnamed)"} · ${fmtBytes(p.picked.size)}${p.expectedBytes != null ? ` · ledger ${fmtBytes(p.expectedBytes)}` : ""}${p.picked.type ? ` · ${p.picked.type}` : ""}`) : null,
          p.renamed && p.ok ? h("div", { class: "f-mute" }, "the device renamed this file; its bytes match the ledger exactly") : null,
          e && e.error ? h("div", { class: "f-err" }, e.error) : null,
          p.problems.length ? h("div", { class: "f-err" }, p.problems.join("\n")) : null),
        // A bound image has NO manual override. A provenance an operator can replace from a gallery
        // is not provenance, so the only button is the one that fetches the named bytes again.
        bound ? null : h("button", { onClick: () => inp.click() }, p.picked ? "Replace" : "Pick"),
        bound ? null : inp);
    });
    // Only a list with nothing left to do folds away; one needing picks stays open.
    card.append(...(picks.every((p) => p.state === "ready") ? fold(rows, `Show all ${imgs.length} images (all verified)`) : rows));
  }
  return card;
}

// ------------------------------------------------------------------ 3. Run
export function RunScreen(app) {
  const jobId = app.state.jobId;
  const job = jobId ? app.journal.get(jobId) : null;
  const root = h("section", {});
  if (!job) { root.appendChild(h("div", { class: "f-mute" }, "No job selected. Pick one on Jobs.")); return root; }
  const done = job.items.filter((i) => TERMINAL.includes(i.state)).length;
  if (job.collection) {
    // Overall progress across the whole collection, not only this tree.
    const c = job.collection, overall = (c.index + done / (job.items.length || 1)) / (c.total || 1);
    root.appendChild(h("div", { class: "f-banner info" },
      h("b", {}, `Collection ${base(c.path)}: tree ${c.index + 1} of ${c.total}${c.name ? ` (${c.name})` : ""}`),
      h("div", { class: "f-bar" }, h("i", { style: { width: Math.round(overall * 100) + "%" } })),
      h("div", { class: "f-mute" }, "Pause stops the rest. After a reload, resume this tree, then reopen the file.")));
  }
  root.append(
    h("div", {}, h("b", {}, jobLabel(job)), " ", jobPill(app, job), h("span", { class: "f-mute" }, ` · started ${fmtAgo(job.startedAt, app.now())}`)),
    h("div", { class: "f-bar" + (job.state === "PAUSED" ? " warn" : "") }, h("i", { style: { width: Math.round(done / (job.items.length || 1) * 100) + "%" } })),
  );
  const outcome = jobOutcome(job);
  if ((job.state === "DONE" || job.state === "INCOMPLETE") && job.items.length === 0) {
    const captures = [...(job.capturesBefore || []), ...(job.capturesAfter || [])];
    const failed = captures.filter((capture) => !capture.ok).length;
    const full = captures.filter((capture) => capture.persist === "full");
    const unpersisted = full.filter((capture) => capture.ok && capture.persistOk !== true);
    // Reading the record and shipping its exact body are two claims, and a full capture makes
    // both. They are reported separately so "the reads succeeded" can never stand in for
    // "the bodies are in the bundle".
    const persistLine = full.length ? `, ${full.length - unpersisted.length}/${full.length} full record ${full.length === 1 ? "body" : "bodies"} persisted into the bundle` : "";
    root.appendChild(outcome === "success"
      ? h("div", { class: "f-banner ok" }, h("b", {}, "Read-only capture complete. "), `${captures.length}/${captures.length} reads succeeded${persistLine}; zero mutations were sent.`)
      : h("div", { class: "f-banner bad" },
          h("b", {}, failed ? "Read-only capture failed. " : "Read-only capture incomplete. "),
          // read failures lead when there are any; otherwise the reason is the missing bodies.
          // The read wording is the fallback, so no arithmetic on an empty full-capture list can
          // produce a sentence about bodies nobody asked for.
          !failed && unpersisted.length
            ? `${captures.length}/${captures.length} reads succeeded, but ${unpersisted.length} of ${full.length} requested full ${full.length === 1 ? "body" : "bodies"} could not be persisted, so this bundle does not carry the record data the manifest asked for`
            : `${failed} of ${captures.length} reads failed`,
          "; zero mutations were sent.",
          unpersisted.length ? h("div", { class: "f-err" }, unpersisted.map((capture) => `${capture.proc} ${capture.snapshotKey || ""}: ${capture.persistError || "not persisted"}`).join("\n")) : null));
  } else if (job.state === "DONE" || job.state === "INCOMPLETE") {
    const drift = job.items.filter((i) => i.verify === "drift").length;
    const unread = job.items.filter((i) => i.verify === "unread").length;
    const failed = job.items.filter((i) => i.state === "FAILED").length;
    const skipped = job.items.filter((i) => i.state === "SKIPPED").length;
    root.appendChild(outcome === "success"
      ? h("div", { class: "f-banner ok" }, h("b", {}, "Verified. "), "Every item read back exactly as written.")
      : h("div", { class: "f-banner " + (outcome === "failed" ? "bad" : "warn") },
          h("b", {}, outcome === "failed" ? "Finished with failures. " : "Finished, not fully verified. "),
          [failed ? `${failed} failed` : null, drift ? `${drift} changed after writing` : null, unread ? `${unread} could not be read back` : null, skipped ? `${skipped} skipped` : null].filter(Boolean).join(", "), ". ",
          failed ? "Each failed item shows its reason below. " : "",
          drift || unread ? "The items that changed or could not be read back are not proven written. " : "",
          job.state === "INCOMPLETE" ? "Resume to re-read them; resuming can only read, never re-send." : ""));
  }
  if (job.pause && job.pause.reason === "SESSION") {
    // The one pause the operator can always fix, and the one 0.3.0 could not name. It says what
    // the game refused, that nothing further was sent, and what to do - never "read failed".
    root.appendChild(h("div", { class: "f-banner bad" },
      h("b", {}, "Paused: TNR authentication unavailable. "),
      job.pause.authRefused
        ? `The game refused ${job.pause.path ? job.pause.path : "a protected procedure"} as signed out. The server answered, so nothing was written.`
        : `Forge stopped before sending${job.pause.path ? ` ${job.pause.path}` : ""} because the game session is not available. Nothing further was sent.`,
      h("div", { class: "f-mute" }, "Sign in to The Ninja RPG in this browser, re-check the session above, then resume. Resuming re-reads before it re-sends anything."),
      job.pause.detail ? h("div", { class: "f-err" }, job.pause.detail) : null));
  } else if (job.pause) root.appendChild(h("div", { class: "f-banner " + (job.pause.reason === "TOO_MANY_REQUESTS" ? "bad" : "warn") },
    h("b", {}, pauseWords(job.pause)), job.pause.path ? ` on ${job.pause.path}` : "", job.pause.until ? ` · wait ${fmtCountdown(job.pause.until, app.now())}` : "", job.pause.detail ? h("div", { class: "f-err" }, job.pause.detail) : null));
  if (app.state.running === jobId) {
    const next = job.items.find((i) => !TERMINAL.includes(i.state));
    root.appendChild(h("div", { class: "f-banner info" }, next
      ? `Working on item ${next.idx + 1} of ${job.items.length}: ${next.name}`
      : app.state.runningNote || "All items sent; reading back and saving the results…"));
  }
  const resumeBlocked = app.resumeBlockedReason ? app.resumeBlockedReason(job) : null;
  if (resumeBlocked) root.appendChild(h("div", { class: "f-mute" }, resumeBlocked));
  root.appendChild(h("div", { class: "f-actions" },
    job.state === "PAUSED" || job.state === "INCOMPLETE" || (job.state === "RUNNING" && app.state.running !== jobId && job.items.some((i) => !["VERIFIED", "FAILED", "SKIPPED"].includes(i.state)))
      ? h("button", { class: "f-primary", disabled: !!resumeBlocked, onClick: () => app.resumeJob(jobId) }, resumeLabel(job)) : null,
    app.state.running === jobId ? h("button", { onClick: () => app.requestPause() }, "Pause after this item") : null,
    app.state.running === jobId ? null : h("button", { onClick: () => app.exportJob(jobId) }, "Export results"),
    app.state.running !== jobId && job.items.some((i) => i.suggestion?.id) ? h("button", { onClick: () => app.checkSuggestions(jobId) }, "Check suggestions") : null,
  ));
  root.appendChild(h("h3", {}, "Budget (limited reads, per path, this minute)"));
  const st = app.budget.status();
  const used = Object.entries(st.paths).filter(([, v]) => v.used > 0);
  root.appendChild(h("div", { class: "f-card" }, used.length ? used.map(([p, v]) => h("div", { class: "f-kv" }, h("b", {}, p), h("span", {}, `${v.used} / ${v.allowance} (server ${v.serverLimit}) · resets in ${fmtCountdown(app.now() + v.resetInMs, app.now())}`))) : h("span", { class: "f-mute" }, "nothing spent"), st.tripped ? h("div", { class: "f-err" }, `TRIPPED on ${st.tripped.path} until ${new Date(st.tripped.until).toLocaleTimeString()}`) : null));
  const allCaptures = [...(job.capturesBefore || []), ...(job.capturesAfter || [])];
  if (allCaptures.some((capture) => capture && capture.persist === "full")) {
    root.appendChild(h("h3", {}, "Full captures"));
    for (const capture of allCaptures.filter((capture) => capture.persist === "full")) {
      root.appendChild(h("div", { class: "f-row" }, h("div", { class: "f-grow" },
        h("div", {}, `${capture.proc} `, h("span", { class: "f-pill " + (capture.persistOk === true ? "VERIFIED" : "FAILED") }, capture.persistOk === true ? "body persisted" : "not persisted"), h("span", { class: "f-mute" }, capture.ok ? " · read ok" : " · read failed")),
        h("div", { class: "f-mono" }, `${capture.snapshotKey || ""}${capture.input && capture.input.id ? " · " + capture.input.id : ""}`),
        capture.persistError ? h("div", { class: "f-err" }, capture.persistError) : null)));
    }
  }
  if (job.items.length) root.appendChild(h("h3", {}, "Items"));
  const savedBindings = readIdmap(app.storage), bloodlineId = job.bloodrightImport?.bloodlineId;
  const bindingBlocked = bloodlineId && unresolvedBloodrightJob(app.journal, bloodlineId);
  if (Object.keys(job.forgottenBindings ?? {}).length) root.appendChild(h("div", { class: "f-banner warn" }, "A saved binding was forgotten. Export this job for evidence and prepare a fresh preview; this job cannot restore the old binding."));
  for (const it of job.items) {
    const phase = it.state === "SENT" || it.state === "CONFIRMED" ? ` · phase ${it.phase}` : "";
    const row = h("div", { class: "f-row" },
      h("div", { class: "f-grow" },
        h("div", {}, `${it.idx + 1}. ${it.name} `, it.suggestion ? h("span", { class: "f-pill " + (it.suggestion.status === "APPLIED" ? "VERIFIED" : /REJECTED|OUTDATED|REVERTED|NOT FOUND/.test(it.suggestion.status) ? "FAILED" : "SENT") }, it.suggestion.status === "PENDING" ? "IN REVIEW" : it.suggestion.status) : pill(it.state), h("span", { class: "f-mute" }, ` ${it.entity}${phase}`)),
        it.entityId ? h("div", { class: "f-mono" }, it.entityId) : null,
        it.suggestion ? h("div", { class: "f-mute" }, `suggestion ${it.suggestion.id ?? "(id not found)"}${it.suggestion.reviewedBy ? ` · by ${it.suggestion.reviewedBy}` : ""}${it.suggestion.note ? ` · ${it.suggestion.note}` : ""}`) : null,
        it.error ? h("div", { class: "f-err" }, it.error) : null,
        it.diffs && it.diffs.length ? h("details", {}, h("summary", {}, `drift on ${it.diffs.length} key(s)`), h("div", { class: "f-err" }, it.diffs.map((d) => `${d.key}: sent ${JSON.stringify(d.sent)} live ${JSON.stringify(d.live)}`).join("\n"))) : null,
        it.reconciled ? h("div", { class: "f-mute" }, it.reconciled) : null,
        it.resolution?.action === "operator-failed" ? h("div", { class: "f-mute" }, "Recovery stopped by operator; record left as is, verification not accepted.") : null,
      ));
    if (["skillTree", "skillTreeFolder"].includes(it.entity) && it.state === "CONFIRMED" && ["PAUSED", "INCOMPLETE"].includes(job.state)) {
      row.appendChild(h("button", { class: "f-danger", disabled: !!app.state.running || job.items.some(i => i.state === "SENT") || typeof globalThis.confirm !== "function",
        onClick: () => app.confirm(`Mark "${it.name}" (${it.entityId}) failed and stop recovery? The record and its saved ID stay as they are, the write is not verified, and dependent skills stay blocked.`, () => app.resolveConfirmed(jobId, it.idx, { confirmed: true })) }, "Mark failed (leave as is)"));
    }
    if (bloodlineId && ["skillTree", "skillTreeFolder"].includes(it.entity) && ["FAILED", "VERIFIED"].includes(it.state) && it.entityId && savedBindings[it.srcId] === it.entityId) {
      // A rare recovery tool: kept behind "More" so it is not one stray tap away on every row.
      row.appendChild(h("details", { class: "f-more" }, h("summary", {}, "More"), h("button", { class: "f-danger", disabled: !!app.state.running || job.state === "RUNNING" || !!bindingBlocked || typeof globalThis.confirm !== "function",
        onClick: () => app.confirm(`Forget saved binding for "${it.name}" (${it.entityId})? Only if the record was deleted or replaced: forgetting one that still exists can create duplicates. Nothing in the game is deleted; old jobs will need a fresh preview.`, () => app.forgetBinding(jobId, it.idx, { confirmed: true, expectedId: it.entityId })) }, "Forget saved binding")));
    }
    root.appendChild(row);
  }
  return root;
}

// ------------------------------------------------------------------ 4. Captures
export function CapturesScreen(app) {
  const root = h("section", {});
  const list = h("div", {});
  const head = h("div", { class: "f-mute" }, "loading…");
  root.append(head, h("div", { class: "f-actions" }, h("button", { class: "f-danger", onClick: () => app.confirm("Clear the whole capture cache? Reads will cost budget again.", async () => { await app.cache.clear(); app.refresh(); }) }, "Clear all")), list);
  // The two stores are shown separately on purpose. Clearing the read cache costs budget on the
  // next read and nothing else; deleting a full-capture snapshot destroys evidence a job has not
  // necessarily exported yet, so it gets its own section, its own wording and its own button.
  root.appendChild(SnapshotsSection(app));
  app.cache.list().then((recs) => {
    const bytes = recs.reduce((a, r) => a + (r.bytes || 0), 0);
    replace(head, `${recs.length} capture${recs.length === 1 ? "" : "s"} · ${fmtBytes(bytes)}`);
    recs.sort((a, b) => (a.at < b.at ? 1 : -1));
    replace(list, recs.map((r) => h("div", { class: "f-row" },
      h("div", { class: "f-grow" }, h("div", { class: "f-mono" }, r.key), h("div", { class: "f-mute" }, `${r.entity} · ${fmtBytes(r.bytes || 0)} · ${fmtAgo(r.at, app.now())}`)),
      h("button", { onClick: async () => { await app.cache.delete(r.path, r.id ?? ""); app.refresh(); } }, "Invalidate"))));
  }).catch((e) => replace(head, h("div", { class: "f-banner bad" }, "capture cache unavailable: ", e.message)));
  return root;
}

/** Immutable full-capture snapshots: the bodies an exported bundle is built from. */
function SnapshotsSection(app) {
  const section = h("div", {});
  const head = h("h3", {}, "Full-capture snapshots");
  const note = h("div", { class: "f-mute" }, "loading…");
  const list = h("div", {});
  section.append(head, note, h("div", { class: "f-actions" }, h("button", {
    class: "f-danger",
    onClick: () => app.confirm("Delete ALL full-capture snapshots? Exported bundles are built from them; an unexported job loses its evidence until the game is read again.", async () => { await app.cache.clearSnapshots(); app.refresh(); }),
  }, "Delete all snapshots")), list);
  app.cache.listSnapshots().then((recs) => {
    const bytes = recs.reduce((a, r) => a + (r.bytes || 0), 0);
    replace(note, `${recs.length} snapshot${recs.length === 1 ? "" : "s"} · ${fmtBytes(bytes)} · never invalidated by a write; deleted with their job`);
    recs.sort((a, b) => (a.at < b.at ? 1 : -1));
    replace(list, recs.map((r) => h("div", { class: "f-row" },
      h("div", { class: "f-grow" }, h("div", { class: "f-mono" }, r.key),
        h("div", { class: "f-mute" }, `${r.path}${r.id ? " " + r.id : ""} · ${r.phase} · ${fmtBytes(r.bytes || 0)} · ${fmtAgo(r.at, app.now())}`)),
      h("button", { onClick: () => app.confirm(`Delete snapshot ${r.key}? Its body can only come back from another read.`, async () => { await app.cache.deleteSnapshot(r.key); app.refresh(); }) }, "Delete"))));
  }).catch((e) => replace(note, h("div", { class: "f-banner bad" }, "capture snapshots unavailable: ", e.message)));
  return section;
}

// ------------------------------------------------------------------ 5. Settings
export function SettingsScreen(app) {
  const gh = readGh(app.storage);
  const pat = h("input", { type: "password", placeholder: "fine-grained PAT (contents: write on tnr-tools only)", value: gh.pat || "" });
  const sync = h("input", { type: "checkbox", checked: !!gh.on });
  const root = h("section", {},
    h("h2", {}, "GitHub"),
    h("div", { class: "f-card" },
      h("div", { class: "f-mute" }, "Sent to api.github.com only. Never to the game. Stored in this browser under tnr_bk_gh_v1 (same key as the old builder)."),
      pat,
      h("label", { class: "f-row" }, sync, h("span", {}, "Auto-commit results bundles to harvests/inbox/")),
      h("div", { class: "f-actions" }, h("button", { class: "f-primary", onClick: () => { writeGh(app.storage, { on: sync.checked, pat: pat.value.trim() }); app.toast("saved", "ok"); app.refresh(); } }, "Save"), h("button", { class: "f-danger", onClick: () => app.confirm("Forget the PAT?", () => { writeGh(app.storage, { on: false, pat: "" }); app.refresh(); }) }, "Forget")),
    ),
    h("h2", {}, "Session"),
    h("div", { class: "f-card f-kv" }, h("b", {}, "game"), h("span", {}, describeText(app.session.describe())),
      h("b", {}, "auth"), h("span", {}, app.auth ? describeText(app.auth.describe()) : "not wired"), h("b", {}, "budget"), h("span", {}, `${app.budget.allowance} / ${app.budget.limit} per path per minute (margin ${app.budget.margin})`), h("b", {}, "persisted storage"), h("span", { id: "f-persist" }, app.view.persisted == null ? "unknown" : String(app.view.persisted))),
    h("h2", {}, "Journal"),
    h("div", { class: "f-card" },
      h("div", { class: "f-actions" },
        h("button", { onClick: () => app.showExport(app.journal.exportText(), "journal export") }, "Export journal as text"),
        h("button", { class: "f-danger", onClick: () => app.confirm("Delete ALL finished jobs from the journal? Open jobs are kept, and each deleted job's full-capture snapshots go with it.", async () => { for (const j of app.journal.listJobs()) if (j.state === "DONE" || j.state === "ABORTED") { app.journal.remove(j.jobId); await app.cache.deleteSnapshotsForJob(j.jobId); } app.refresh(); }) }, "Delete finished jobs")),
      app.cacheSize ? h("div", { class: "f-mute" }, `capture cache: ${app.cacheSize}`) : null,
    ),
    h("h2", {}, "About"),
    h("div", { class: "f-card f-mute" }, `${app.version} · content fields pinned to studie-tech/TheNinjaRPG@94f9d84 (procedures 345d18ac) · journal v1 · keys tnr_forge_job_v1:*, tnr_forge_sendlog_v1, tnr_forge_snap_v1:*`),
  );
  return root;
}

/** A describe() object as "key: value" text; epoch timestamps read as local times. */
function describeText(obj) {
  return Object.entries(obj || {}).filter(([, v]) => v != null && v !== "")
    .map(([k, v]) => `${k}: ${typeof v === "number" && v > 1e12 ? new Date(v).toLocaleString() : typeof v === "object" ? JSON.stringify(v) : v}`).join(" · ") || "—";
}
