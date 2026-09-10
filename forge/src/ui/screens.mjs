// The five screens (spec section 11). Each is a function (app) => Element and re-renders on
// app.refresh(). Errors are surfaced in the UI with context; nothing is only in the console.
import { h, replace, fmtAgo, fmtBytes, fmtCountdown } from "./dom.mjs";
import { manifestNumber, manifestSummary } from "../github.mjs";
import { readGh, writeGh } from "../storage/compat.mjs";
import { jobOutcome } from "../storage/journal.mjs";

const pill = (state) => h("span", { class: "f-pill " + state }, state);

// ------------------------------------------------------------------ 1. Jobs
export function JobsScreen(app) {
  const jobs = app.journal.listJobs();
  const open = app.journal.resumable();
  const orphans = jobs.flatMap((j) => j.items.filter((it) => it.state === "ORPHANED").map((it) => ({ job: j, it })));
  const root = h("section", {});
  if (open.length) {
    for (const j of open) {
      root.appendChild(h("div", { class: "f-banner warn" },
        h("div", {}, h("b", {}, "Open job: "), j.manifestPath || j.jobId, " ", pill(j.state)),
        j.state === "INCOMPLETE" ? h("div", { class: "f-mute" }, `Finished unverified: ${j.items.filter((i) => !["VERIFIED", "FAILED", "SKIPPED"].includes(i.state)).length} item(s) still owe a read-back. Resuming re-reads them and cannot re-send.`) : null,
        j.pause ? h("div", { class: "f-mute" }, `Paused: ${j.pause.reason}${j.pause.path ? " on " + j.pause.path : ""}${j.pause.until ? " · retry allowed in " + fmtCountdown(j.pause.until, app.now()) : ""}${j.pause.detail ? " · " + j.pause.detail : ""}`) : null,
        h("div", { class: "f-actions" },
          h("button", { class: "f-primary", onClick: () => app.resumeJob(j.jobId) }, j.items.some((i) => i.state === "SENT") ? "Reconcile & resume" : j.state === "INCOMPLETE" ? "Re-read unverified items" : "Resume"),
          h("button", { onClick: () => app.go("run", { jobId: j.jobId }) }, "Open"),
        )));
    }
  }
  if (orphans.length) {
    root.appendChild(h("h2", {}, `Orphans needing a decision (${orphans.length})`));
    for (const { job, it } of orphans) root.appendChild(OrphanCard(app, job, it));
  }
  root.appendChild(h("h2", {}, "Recent runs"));
  if (!jobs.length) root.appendChild(h("div", { class: "f-mute" }, "No jobs yet. Pick a manifest to start one."));
  for (const j of jobs.slice(0, 20)) {
    const counts = {}; for (const it of j.items) counts[it.state] = (counts[it.state] ?? 0) + 1;
    root.appendChild(h("div", { class: "f-row f-tap", onClick: () => app.go("run", { jobId: j.jobId }) },
      h("div", { class: "f-grow" }, h("div", {}, j.manifestPath || j.jobId, " ", pill(j.state)),
        h("div", { class: "f-mute" }, `${j.items.length} items · ${Object.entries(counts).map(([k, v]) => `${v} ${k.toLowerCase()}`).join(", ")} · ${fmtAgo(j.startedAt, app.now())}`)),
    ));
  }
  return root;
}

function OrphanCard(app, job, it) {
  const cands = it.candidates || [];
  const card = h("div", { class: "f-card" },
    h("div", {}, h("b", {}, it.name), " ", h("span", { class: "f-mute" }, `${it.entity} · ${job.manifestPath || job.jobId} · item ${it.idx}`)),
    h("div", { class: "f-mute" }, it.error || "ambiguous"),
  );
  if (cands.length) {
    card.appendChild(h("h3", {}, "Candidates on the server"));
    for (const c of cands) {
      const id = typeof c === "string" ? c : c.id;
      const name = typeof c === "string" ? "" : c.name;
      card.appendChild(h("div", { class: "f-row" },
        h("div", { class: "f-grow" }, h("div", { class: "f-mono" }, id), name ? h("div", { class: "f-mute" }, name) : null),
        h("button", { onClick: () => app.confirm(`Adopt ${id} as "${it.name}"? The job will continue with its update.`, () => app.adopt(job.jobId, it.idx, id)) }, "Adopt"),
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
export function ManifestsScreen(app) {
  const root = h("section", {});
  const q = h("input", { type: "search", placeholder: "search filename, number, title", value: app.state.pickerQuery || "", onInput: (e) => { app.state.pickerQuery = e.target.value; renderList(); } });
  const list = h("div", {});
  const status = h("div", { class: "f-mute" });
  root.append(h("div", { class: "f-actions" }, q, h("button", { onClick: () => app.loadPicker(true) }, "Refresh")), status, list);
  function renderList() {
    const entries = app.state.picker || [];
    const needle = (app.state.pickerQuery || "").toLowerCase();
    const seen = new Set(app.journal.listJobs().map((j) => j.manifestPath));
    const rows = entries.filter((e) => !needle || e.name.toLowerCase().includes(needle) || String(e.number ?? "").includes(needle) || (e.summary?.title || "").toLowerCase().includes(needle));
    replace(list, rows.length ? rows.map((e) => h("div", { class: "f-row f-tap", onClick: () => app.selectManifest(e) },
      h("div", { class: "f-grow" },
        h("div", {}, e.number != null ? h("b", {}, "#" + e.number + " ") : null, e.name, seen.has(e.path) ? h("span", { class: "f-pill VERIFIED", style: { marginLeft: "6px" } }, "ran") : null),
        h("div", { class: "f-mute" }, e.summary ? `${e.summary.title || "(untitled)"} · ${e.summary.items} item${e.summary.items === 1 ? "" : "s"}${e.summary.creates ? ` (${e.summary.creates} create)` : ""}${e.summary.captures ? ` · ${e.summary.captures} capture` : ""}` : (e.loading ? "loading…" : e.error || "")),
      ))) : h("div", { class: "f-mute" }, app.state.pickerError ? "" : "nothing matches"));
    replace(status, app.state.pickerError ? h("div", { class: "f-banner bad" }, "Could not list push/: ", app.state.pickerError) : `${entries.length} file${entries.length === 1 ? "" : "s"} in push/` + (app.state.pickerAt ? ` · listed ${fmtAgo(app.state.pickerAt, app.now())}` : ""));
  }
  renderList();
  app.state._renderPicker = renderList;
  if (!app.state.picker) app.loadPicker(false);

  if (app.state.selected) root.appendChild(SelectedManifest(app));
  return root;
}

function SelectedManifest(app) {
  const s = app.state.selected;
  const captureCount = s.manifest.capture.before.length + s.manifest.capture.after.length;
  const readOnly = s.plan.length === 0;
  const card = h("div", { class: "f-card" }, h("h2", {}, s.entry.name), h("div", { class: "f-mute" }, `${s.plan.length} items${captureCount ? ` · ${captureCount} capture${captureCount === 1 ? "" : "s"}` : ""} · manifest hash ${s.manifest.hash}`));
  if (readOnly) card.appendChild(h("div", { class: "f-banner info" }, "Read-only capture job. This sends queries only; zero mutations."));
  if (s.problems.length) card.appendChild(h("div", { class: "f-banner bad" }, h("b", {}, "Cannot run: "), h("div", { class: "f-err" }, s.problems.join("\n"))));
  if (s.manifest.poolResolved) card.appendChild(h("div", { class: "f-mute" }, `${s.manifest.poolResolved} pool code(s) resolved to ids and gates`));
  // advisories: worth reading, not worth blocking. A blocking lint is already in `problems`.
  if (s.manifest.warnings && s.manifest.warnings.length) {
    card.appendChild(h("div", { class: "f-banner warn" }, h("b", {}, `${s.manifest.warnings.length} advisory: `), h("div", {}, s.manifest.warnings.join("\n"))));
  }
  for (const it of s.plan) {
    card.appendChild(h("div", { class: "f-row" },
      h("div", { class: "f-grow" }, h("div", {}, `${it.idx}. ${it.name}`), h("div", { class: "f-mute" }, `${it.entity} · ${it.op}${it.targetId ? " → " + it.targetId : ""}${it.deps?.length ? " · after " + it.deps.join(", ") : ""} · keys: ${Object.keys(it.data).join(", ").slice(0, 120)}`))));
  }
  const imgs = s.images || [];
  if (imgs.length) {
    card.appendChild(h("h3", {}, `Images to pick (${imgs.length})`));
    for (const name of imgs) {
      const have = app.runner.files.has(name);
      const inp = h("input", { type: "file", accept: "image/*", style: { display: "none" }, onChange: (e) => { const f = e.target.files[0]; if (f) { app.runner.files.set(name, f); app.refresh(); } } });
      card.appendChild(h("div", { class: "f-row" }, h("div", { class: "f-grow f-mono" }, name, " ", have ? h("span", { class: "f-pill VERIFIED" }, "picked") : h("span", { class: "f-pill FAILED" }, "missing")), h("button", { onClick: () => inp.click() }, "Pick"), inp));
    }
  }
  const missingImgs = imgs.filter((n) => !app.runner.files.has(n));
  card.appendChild(h("div", { class: "f-actions" },
    h("button", { class: "f-primary", disabled: s.problems.length > 0 || missingImgs.length > 0, onClick: () => app.confirm(
      readOnly
        ? `Run read-only capture job for ${s.entry.name}: ${captureCount} capture${captureCount === 1 ? "" : "s"}? No mutations will be sent.`
        : `Start job for ${s.entry.name}: ${s.plan.length} items (${s.plan.filter((i) => i.op === "create").length} creates)? This writes to the game.`,
      () => app.startJob()),
    }, readOnly ? "Run captures" : "Start job"),
    h("button", { onClick: () => { app.state.selected = null; app.refresh(); } }, "Clear"),
  ));
  return card;
}

// ------------------------------------------------------------------ 3. Run
export function RunScreen(app) {
  const jobId = app.state.jobId;
  const job = jobId ? app.journal.get(jobId) : null;
  const root = h("section", {});
  if (!job) { root.appendChild(h("div", { class: "f-mute" }, "No job selected. Pick one on Jobs.")); return root; }
  const done = job.items.filter((i) => ["VERIFIED", "FAILED", "SKIPPED"].includes(i.state)).length;
  root.append(
    h("div", {}, h("b", {}, job.manifestPath || job.jobId), " ", pill(job.state), h("span", { class: "f-mute" }, ` · started ${fmtAgo(job.startedAt, app.now())}`)),
    h("div", { class: "f-bar" + (job.state === "PAUSED" ? " warn" : "") }, h("i", { style: { width: Math.round(done / (job.items.length || 1) * 100) + "%" } })),
  );
  const outcome = jobOutcome(job);
  if ((job.state === "DONE" || job.state === "INCOMPLETE") && job.items.length === 0) {
    const captures = [...(job.capturesBefore || []), ...(job.capturesAfter || [])];
    const failed = captures.filter((capture) => !capture.ok).length;
    root.appendChild(outcome === "success"
      ? h("div", { class: "f-banner ok" }, h("b", {}, "Read-only capture complete. "), `${captures.length}/${captures.length} reads succeeded; zero mutations were sent.`)
      : h("div", { class: "f-banner bad" }, h("b", {}, "Read-only capture failed. "), `${failed} of ${captures.length} reads failed; zero mutations were sent.`));
  } else if (job.state === "DONE" || job.state === "INCOMPLETE") {
    const drift = job.items.filter((i) => i.verify === "drift").length;
    const unread = job.items.filter((i) => i.verify === "unread").length;
    const failed = job.items.filter((i) => i.state === "FAILED").length;
    const skipped = job.items.filter((i) => i.state === "SKIPPED").length;
    root.appendChild(outcome === "success"
      ? h("div", { class: "f-banner ok" }, h("b", {}, "Verified. "), "every item read back equal on its asserted keys.")
      : h("div", { class: "f-banner " + (outcome === "failed" ? "bad" : "warn") },
          h("b", {}, outcome === "failed" ? "Finished with failures. " : "Finished UNVERIFIED. "),
          [failed ? `${failed} failed` : null, drift ? `${drift} drifted` : null, unread ? `${unread} could not be read back` : null, skipped ? `${skipped} skipped` : null].filter(Boolean).join(", "),
          ". These writes are not proven. ",
          job.state === "INCOMPLETE" ? "Resume to re-read them; resuming can only read, never re-send." : ""));
  }
  if (job.pause) root.appendChild(h("div", { class: "f-banner " + (job.pause.reason === "TOO_MANY_REQUESTS" ? "bad" : "warn") },
    h("b", {}, `Paused: ${job.pause.reason}`), job.pause.path ? ` on ${job.pause.path}` : "", job.pause.until ? ` · wait ${fmtCountdown(job.pause.until, app.now())}` : "", job.pause.detail ? h("div", { class: "f-err" }, job.pause.detail) : null));
  if (app.state.running === jobId) root.appendChild(h("div", { class: "f-banner info" }, "Running… ", app.state.runningNote || ""));
  root.appendChild(h("div", { class: "f-actions" },
    job.state === "PAUSED" || job.state === "INCOMPLETE" || (job.state === "RUNNING" && app.state.running !== jobId && job.items.some((i) => !["VERIFIED", "FAILED", "SKIPPED"].includes(i.state)))
      ? h("button", { class: "f-primary", onClick: () => app.resumeJob(jobId) }, job.items.some((i) => i.state === "SENT") ? "Reconcile & resume" : job.state === "INCOMPLETE" ? "Re-read unverified items" : "Resume") : null,
    app.state.running === jobId ? h("button", { onClick: () => app.requestPause() }, "Pause after this item") : null,
    h("button", { onClick: () => app.exportJob(jobId) }, "Export bundle"),
  ));
  root.appendChild(h("h3", {}, "Budget (limited reads, per path, this minute)"));
  const st = app.budget.status();
  const used = Object.entries(st.paths).filter(([, v]) => v.used > 0);
  root.appendChild(h("div", { class: "f-card" }, used.length ? used.map(([p, v]) => h("div", { class: "f-kv" }, h("b", {}, p), h("span", {}, `${v.used} / ${v.allowance} (server ${v.serverLimit}) · resets in ${fmtCountdown(app.now() + v.resetInMs, app.now())}`))) : h("span", { class: "f-mute" }, "nothing spent"), st.tripped ? h("div", { class: "f-err" }, `TRIPPED on ${st.tripped.path} until ${new Date(st.tripped.until).toLocaleTimeString()}`) : null));
  root.appendChild(h("h3", {}, "Items"));
  for (const it of job.items) {
    const phase = it.state === "SENT" || it.state === "CONFIRMED" ? ` · phase ${it.phase}` : "";
    const row = h("div", { class: "f-row" },
      h("div", { class: "f-grow" },
        h("div", {}, `${it.idx}. ${it.name} `, pill(it.state), h("span", { class: "f-mute" }, ` ${it.entity}${phase}`)),
        it.entityId ? h("div", { class: "f-mono" }, it.entityId) : null,
        it.error ? h("div", { class: "f-err" }, it.error) : null,
        it.diffs && it.diffs.length ? h("details", {}, h("summary", {}, `drift on ${it.diffs.length} key(s)`), h("div", { class: "f-err" }, it.diffs.map((d) => `${d.key}: sent ${JSON.stringify(d.sent)} live ${JSON.stringify(d.live)}`).join("\n"))) : null,
        it.reconciled ? h("div", { class: "f-mute" }, it.reconciled) : null,
      ));
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
    h("div", { class: "f-card f-kv" }, h("b", {}, "game"), h("span", {}, JSON.stringify(app.session.describe())), h("b", {}, "budget"), h("span", {}, `${app.budget.allowance} / ${app.budget.limit} per path per minute (margin ${app.budget.margin})`), h("b", {}, "persisted storage"), h("span", { id: "f-persist" }, app.state.persisted == null ? "unknown" : String(app.state.persisted))),
    h("h2", {}, "Journal"),
    h("div", { class: "f-card" },
      h("div", { class: "f-actions" },
        h("button", { onClick: () => app.showExport(app.journal.exportText(), "journal export") }, "Export journal as text"),
        h("button", { class: "f-danger", onClick: () => app.confirm("Delete ALL finished jobs from the journal? Open jobs are kept.", () => { for (const j of app.journal.listJobs()) if (j.state === "DONE" || j.state === "ABORTED") app.journal.remove(j.jobId); app.refresh(); }) }, "Delete finished jobs")),
      app.cacheSize ? h("div", { class: "f-mute" }, `capture cache: ${app.cacheSize}`) : null,
    ),
    h("h2", {}, "About"),
    h("div", { class: "f-card f-mute" }, `forge ${app.version} · pinned to studie-tech/TheNinjaRPG@345d18ac · journal v1 · keys tnr_forge_job_v1:*, tnr_forge_sendlog_v1, tnr_forge_snap_v1:*`),
  );
  return root;
}
