// First operator-facing Quest Studio slice. The UI owns human editing and local draft ergonomics;
// repository contracts/scripts remain authoritative for subtype support, policy and compilation.
// This workspace deliberately does NOT offer live execution: a Studio-branch generated manifest
// needs a separately reviewed promotion/resume contract before it can enter the existing runner.

import { h, installCss, replace } from "../ui/dom.mjs";
import { GithubError } from "../github.mjs";
import { QuestStudioRepository } from "./repository.mjs";

const DRAFT_KEY = "tnr_forge_quest_studio_draft_v1";

const STUDIO_CSS = `
.f-app .qs-launch { border-color:#40526c; font-weight:600; white-space:nowrap; }
.f-app .qs-shell { position:fixed; inset:0; z-index:2147483002; overflow:auto; background:#070b12; color:#f5f1e7; }
.f-app .qs-wrap { width:min(1100px,100%); margin:0 auto; padding:12px 12px 88px; }
.f-app .qs-head { position:sticky; top:0; z-index:2; display:flex; align-items:center; gap:10px; min-height:58px; padding:8px 12px; border-bottom:1px solid #29384d; background:#0b111bf2; backdrop-filter:blur(10px); }
.f-app .qs-head-title { font-size:18px; font-weight:750; letter-spacing:.02em; }
.f-app .qs-head-sub { color:#b7c0ce; font-size:12px; }
.f-app .qs-close { margin-left:auto; }
.f-app .qs-hero { padding:20px 2px 10px; }
.f-app .qs-hero h1 { margin:0 0 6px; font-size:26px; }
.f-app .qs-hero p { color:#b7c0ce; max-width:68ch; margin:0; }
.f-app .qs-grid { display:grid; grid-template-columns:1fr; gap:10px; margin:12px 0; }
.f-app .qs-card { border:1px solid #29384d; border-radius:12px; background:#111a28; padding:14px; }
.f-app .qs-card[data-ready="true"] { border-color:#40526c; }
.f-app .qs-card h2, .f-app .qs-card h3 { margin:0 0 6px; text-transform:none; letter-spacing:0; color:#f5f1e7; }
.f-app .qs-card p { margin:6px 0; }
.f-app .qs-eyebrow { color:#7f8b9c; font-size:11px; font-weight:700; text-transform:uppercase; letter-spacing:.08em; }
.f-app .qs-muted { color:#9aa6b8; font-size:13px; }
.f-app .qs-ready { color:#45c779; font-size:12px; font-weight:650; }
.f-app .qs-pending { color:#e6ad45; font-size:12px; font-weight:650; }
.f-app .qs-field { display:block; margin:12px 0; }
.f-app .qs-field > span { display:block; color:#b7c0ce; font-size:12px; font-weight:650; margin-bottom:5px; }
.f-app .qs-field input, .f-app .qs-field textarea, .f-app .qs-field select { width:100%; min-height:44px; padding:9px 10px; border:1px solid #40526c; border-radius:8px; background:#0b111b; color:#f5f1e7; font:inherit; }
.f-app .qs-field textarea { min-height:94px; resize:vertical; }
.f-app .qs-field select { appearance:auto; }
.f-app .qs-actions { display:flex; gap:8px; flex-wrap:wrap; margin:10px 0; }
.f-app .qs-primary { background:#6bb8ff; color:#07101a; border-color:transparent; font-weight:750; }
.f-app .qs-compile { background:#f97316; color:#130904; border-color:transparent; font-weight:750; }
.f-app .qs-beat { border-left:3px solid #6bb8ff; }
.f-app .qs-beat-top { display:flex; align-items:center; gap:8px; }
.f-app .qs-beat-num { width:28px; height:28px; display:grid; place-items:center; border-radius:50%; background:#172235; font-weight:750; }
.f-app .qs-beat-top strong { flex:1; }
.f-app .qs-end { border-left:3px solid #45c779; }
.f-app .qs-callout { border:1px solid #40526c; background:#101827; border-radius:10px; padding:10px 12px; margin:10px 0; }
.f-app .qs-callout.warn { border-color:#e6ad45; background:#2a2312; }
.f-app .qs-callout.bad { border-color:#e05f5f; background:#2a1515; }
.f-app .qs-callout.ok { border-color:#45c779; background:#12261c; }
.f-app .qs-callout.info { border-color:#6bb8ff; background:#141b2e; }
.f-app .qs-status-title { font-weight:750; margin-bottom:4px; }
.f-app .qs-list { margin:6px 0 0 18px; padding:0; }
.f-app .qs-list li { margin:4px 0; }
.f-app .qs-provenance { font-family:ui-monospace,Menlo,monospace; font-size:11px; color:#8994a5; word-break:break-all; }
.f-app .qs-two { display:grid; grid-template-columns:1fr; gap:10px; }
@media (min-width:760px) {
  .f-app .qs-grid { grid-template-columns:repeat(3,minmax(0,1fr)); }
  .f-app .qs-two { grid-template-columns:1fr 1fr; }
  .f-app .qs-wrap { padding:18px 22px 100px; }
}
`;

export function makeQuestRequestId(now = Date.now()) {
  return `quest-${Number(now).toString(36)}`;
}

export function newMissionDraft(now = Date.now()) {
  return {
    version: 1,
    requestId: makeQuestRequestId(now),
    subtype: "mission",
    profile: "",
    name: "",
    description: "",
    successDescription: "",
    beats: [],
    updatedAt: new Date(now).toISOString(),
    sourceCommit: null,
    lastResult: null,
  };
}

function cleanText(value) { return typeof value === "string" ? value.trim() : ""; }

const AWAITING_RULING = "AWAITING_RULING";

function containsAwaitingRuling(value) {
  if (value === AWAITING_RULING) return true;
  if (Array.isArray(value)) return value.some(containsAwaitingRuling);
  if (value && typeof value === "object") return Object.values(value).some(containsAwaitingRuling);
  return false;
}

function profileShapeNumber(profile, key) {
  const raw = profile?.shape?.[key];
  return typeof raw === "number" && Number.isFinite(raw) ? raw : null;
}

export function missionSourceFromDraft(draft) {
  const beats = Array.isArray(draft.beats) ? draft.beats : [];
  const objectives = beats.map((beat, i) => {
    const id = `n${i + 1}`;
    const next = i + 1 < beats.length ? `n${i + 2}` : `n${beats.length + 1}`;
    return {
      id,
      task: "dialog",
      description: cleanText(beat.description),
      nextObjectiveId: [{ text: cleanText(beat.choiceText) || "Continue", nextObjectiveId: next }],
    };
  });
  objectives.push({
    id: `n${beats.length + 1}`,
    task: "win_quest",
    description: cleanText(draft.successDescription),
    successDescription: cleanText(draft.successDescription),
  });
  const slug = String(draft.requestId).replace(/^quest-/, "").replace(/[^a-z0-9]+/g, "_");
  return {
    schemaVersion: 1,
    kind: "quest",
    requestId: draft.requestId,
    subtype: "mission",
    content: {
      rank: draft.profile,
      srcId: `studio_${slug}`,
      slug: `studio_${slug}`,
      folder: `studio${slug.replace(/_/g, "")}`,
      name: cleanText(draft.name),
      description: cleanText(draft.description),
      successDescription: cleanText(draft.successDescription),
      objectives,
    },
    meta: { authoredIn: "forge-quest-studio", draftVersion: draft.version ?? 1 },
  };
}

export function missionDraftProblems(draft, profiles) {
  const out = [];
  const profile = profiles?.ranks?.[draft.profile];
  if (!profile) out.push("Choose a repository Mission profile.");
  const unresolved = !!profile && containsAwaitingRuling(profile);
  const battles = profileShapeNumber(profile, "battle_nodes");
  if (unresolved) out.push(`The ${draft.profile} Mission profile is awaiting a director ruling; unresolved profile values cannot compile.`);
  else if (battles !== null && battles > 0) out.push("This profile needs combat authoring; the Encounter editor is not in this first UI slice yet.");
  if (!cleanText(draft.name)) out.push("Mission name is required.");
  if (!cleanText(draft.description)) out.push("Mission premise/description is required.");
  if (!cleanText(draft.successDescription)) out.push("Success outcome is required.");
  const beats = Array.isArray(draft.beats) ? draft.beats : [];
  if (!beats.length) out.push("Add at least one story beat.");
  for (let i = 0; i < beats.length; i++) if (!cleanText(beats[i]?.description)) out.push(`Beat ${i + 1} needs player-facing text.`);
  const expected = profileShapeNumber(profile, "objective_count");
  if (expected !== null && expected > 0 && beats.length + 1 !== expected) {
    out.push(`The ${draft.profile} profile owns an objective count of ${expected}; this draft currently has ${beats.length + 1}.`);
  }
  return out;
}

function profileLabel(key, profile) {
  if (containsAwaitingRuling(profile)) return `${key} · awaiting ruling`;
  const battles = profileShapeNumber(profile, "battle_nodes");
  const nodes = profileShapeNumber(profile, "objective_count");
  if (battles === null || nodes === null) return `${key} · profile shape unavailable`;
  return `${key} · ${nodes} nodes${battles ? ` · ${battles} battle${battles === 1 ? "" : "s"}` : " · no combat"}`;
}

function readDraft(storage) {
  try {
    const raw = storage.getItem(DRAFT_KEY);
    if (!raw) return null;
    const draft = JSON.parse(raw);
    return draft && draft.version === 1 && draft.subtype === "mission" ? draft : null;
  } catch { return null; }
}

function writeDraft(storage, draft, now = Date.now()) {
  draft.updatedAt = new Date(now).toISOString();
  try { storage.setItem(DRAFT_KEY, JSON.stringify(draft)); } catch { /* local draft persistence is best effort */ }
}

export class QuestStudioWorkspace {
  constructor({ app, repository = null, pollMs = 2000, maxPolls = 30 }) {
    this.app = app;
    this.repository = repository ?? new QuestStudioRepository({ github: app.github });
    this.pollMs = pollMs;
    this.maxPolls = maxPolls;
    this.registry = null;
    this.profiles = null;
    this.shell = null;
    this.pollToken = 0;
    this.view = "home";
    this.draft = readDraft(app.storage);
    this.buildState = null;
  }

  install() {
    const doc = this.app.root?.ownerDocument || document;
    installCss(STUDIO_CSS, doc);
    const button = h("button", { class: "qs-launch", onClick: () => this.open() }, "Quest Studio");
    const ver = this.app.$top?.querySelector(".f-ver");
    if (ver) this.app.$top.insertBefore(button, ver);
    else this.app.$top?.appendChild(button);
    this.launcher = button;
    return this;
  }

  async open() {
    if (!this.shell) {
      this.shell = h("section", { class: "qs-shell", role: "dialog", "aria-label": "Quest Studio" });
      this.app.root.appendChild(this.shell);
    }
    this.shell.hidden = false;
    this.renderLoading("Opening Quest Studio…");
    try {
      this.registry = await this.repository.registry();
      this.renderHome();
    } catch (e) {
      this.renderFatal("Quest Studio could not load repository recipes.", e);
    }
  }

  close() {
    this.pollToken++;
    if (this.shell) this.shell.hidden = true;
  }

  renderFrame(title, subtitle, ...body) {
    replace(this.shell,
      h("header", { class: "qs-head" },
        this.view !== "home" ? h("button", { onClick: () => { this.view = "home"; this.renderHome(); } }, "Back") : null,
        h("div", {}, h("div", { class: "qs-head-title" }, title), subtitle ? h("div", { class: "qs-head-sub" }, subtitle) : null),
        h("button", { class: "qs-close", onClick: () => this.close() }, "Close")),
      h("div", { class: "qs-wrap" }, ...body));
  }

  renderLoading(text) {
    this.view = this.view || "home";
    this.renderFrame("Quest Studio", "Repository-backed content authoring", h("div", { class: "qs-callout info" }, text));
  }

  renderFatal(title, error) {
    this.renderFrame("Quest Studio", "Repository-backed content authoring",
      h("div", { class: "qs-callout bad" }, h("div", { class: "qs-status-title" }, title), h("div", { class: "qs-muted" }, error?.message || String(error))));
  }

  renderHome() {
    this.view = "home";
    const subtypes = Object.entries(this.registry?.subtypes || {});
    const draftCard = this.draft ? h("div", { class: "qs-callout info" },
      h("div", { class: "qs-status-title" }, `Resume Mission draft: ${this.draft.name || "Untitled mission"}`),
      h("div", { class: "qs-muted" }, `Saved locally ${this.draft.updatedAt ? new Date(this.draft.updatedAt).toLocaleString() : ""}. Repository compile remains separate.`),
      h("div", { class: "qs-actions" }, h("button", { class: "qs-primary", onClick: () => this.openMission(false) }, "Resume draft"))) : null;

    const cards = subtypes.map(([id, item]) => {
      const ready = item?.maturity === "supported" && !!item?.compilerAdapter;
      return h("article", { class: "qs-card", dataset: { ready: String(ready), subtype: id } },
        h("div", { class: "qs-eyebrow" }, ready ? "Repository adapter ready" : String(item?.maturity || "not ready").replaceAll("_", " ")),
        h("h2", {}, item?.label || id),
        h("p", { class: "qs-muted" }, ready
          ? "Author here; canonical compile runs against repository tooling."
          : "Visible by design, but Forge will not pretend this recipe is executable before its repository adapter is audited."),
        h("div", { class: ready ? "qs-ready" : "qs-pending" }, ready ? "Supported end-to-end" : "Adapter pending"),
        h("div", { class: "qs-actions" }, h("button", {
          disabled: !ready || id !== "mission",
          class: ready && id === "mission" ? "qs-primary" : "",
          onClick: () => id === "mission" && this.openMission(!this.draft),
        }, id === "mission" && ready ? (this.draft ? "Open Mission" : "Create Mission") : "Not available yet")));
    });

    this.renderFrame("Quest Studio", "One authoring workspace · repository-owned facts and compilers",
      h("div", { class: "qs-hero" }, h("h1", {}, "Design the quest. Let the repository compile it."),
        h("p", {}, "Choose what you are making. Forge handles the human workflow; repository profiles, contracts, scripts and validation remain authoritative.")),
      draftCard,
      h("div", { class: "qs-grid" }, cards));
  }

  async openMission(forceNew = false) {
    this.view = "mission";
    if (forceNew || !this.draft) this.draft = newMissionDraft(this.app.now ? this.app.now() : Date.now());
    writeDraft(this.app.storage, this.draft, this.app.now ? this.app.now() : Date.now());
    this.renderLoading("Loading Mission profiles from the repository…");
    try {
      this.profiles = await this.repository.missionProfiles();
      this.seedProfileBeats();
      this.renderMission();
      if (this.draft.sourceCommit) this.refreshBuild(false).catch(() => {});
    } catch (e) {
      this.renderFatal("Mission profiles could not be loaded from the repository.", e);
    }
  }

  seedProfileBeats() {
    const profile = this.profiles?.ranks?.[this.draft.profile];
    if (!profile || this.draft.beats?.length) return;
    const objectiveCount = profileShapeNumber(profile, "objective_count");
    if (objectiveCount === null) return;
    const count = Math.max(1, objectiveCount - 1);
    this.draft.beats = Array.from({ length: count }, () => ({ description: "", choiceText: "Continue" }));
    this.saveDraft();
  }

  saveDraft() { writeDraft(this.app.storage, this.draft, this.app.now ? this.app.now() : Date.now()); }

  chooseProfile(key) {
    this.draft.profile = key;
    if (!this.draft.beats?.length) this.seedProfileBeats();
    this.buildState = null;
    this.saveDraft();
    this.renderMission();
  }

  matchProfileShape() {
    const expected = profileShapeNumber(this.profiles?.ranks?.[this.draft.profile], "objective_count");
    if (expected === null || expected <= 0) return;
    const target = Math.max(1, expected - 1);
    const beats = this.draft.beats || [];
    const apply = () => {
      while (beats.length < target) beats.push({ description: "", choiceText: "Continue" });
      while (beats.length > target) beats.pop();
      this.draft.beats = beats;
      this.buildState = null;
      this.saveDraft();
      this.renderMission();
    };
    if (beats.length > target && this.app.confirm) this.app.confirm(`This profile owns ${expected} objectives. Remove ${beats.length - target} trailing beat(s) to match it?`, apply);
    else apply();
  }

  startNewMission() {
    const make = () => {
      this.pollToken++;
      this.draft = newMissionDraft(this.app.now ? this.app.now() : Date.now());
      this.buildState = null;
      this.saveDraft();
      this.renderMission();
    };
    if (this.app.confirm) this.app.confirm("Start a new Mission draft? The current local draft will be replaced; repository revisions already submitted remain durable.", make);
    else make();
  }

  field(label, value, onInput, { multiline = false, placeholder = "" } = {}) {
    const control = multiline
      ? h("textarea", { value: value || "", placeholder, onInput: (e) => onInput(e.target.value) })
      : h("input", { type: "text", value: value || "", placeholder, onInput: (e) => onInput(e.target.value) });
    return h("label", { class: "qs-field" }, h("span", {}, label), control);
  }

  renderMission() {
    this.view = "mission";
    const ranks = this.profiles?.ranks || {};
    const options = [h("option", { value: "" }, "Choose profile…")];
    for (const [key, profile] of Object.entries(ranks)) {
      const unresolved = containsAwaitingRuling(profile);
      const battleNodes = profileShapeNumber(profile, "battle_nodes");
      const combat = battleNodes !== null && battleNodes > 0;
      const suffix = !unresolved && combat ? " · Encounter editor required" : "";
      options.push(h("option", { value: key, selected: this.draft.profile === key, disabled: combat || unresolved }, profileLabel(key, profile) + suffix));
    }
    const select = h("select", { value: this.draft.profile, onChange: (e) => this.chooseProfile(e.target.value) }, options);
    const profile = ranks[this.draft.profile];
    const expected = profileShapeNumber(profile, "objective_count");
    const battleNodes = profileShapeNumber(profile, "battle_nodes");
    const problems = missionDraftProblems(this.draft, this.profiles);

    const beats = (this.draft.beats || []).map((beat, i) => h("article", { class: "qs-card qs-beat" },
      h("div", { class: "qs-beat-top" }, h("div", { class: "qs-beat-num" }, i + 1), h("strong", {}, "Dialogue beat"),
        h("button", { disabled: this.draft.beats.length <= 1, onClick: () => { this.draft.beats.splice(i, 1); this.buildState = null; this.saveDraft(); this.renderMission(); } }, "Remove")),
      this.field("What the player reads", beat.description, (v) => { beat.description = v; this.buildState = null; this.saveDraft(); }, { multiline: true, placeholder: "Write the scene, instruction, reveal, or transition." }),
      this.field("Continue choice", beat.choiceText, (v) => { beat.choiceText = v; this.buildState = null; this.saveDraft(); }, { placeholder: "Continue" })));

    const profileCard = h("section", { class: "qs-card" },
      h("div", { class: "qs-eyebrow" }, "Repository policy"), h("h2", {}, "Mission profile"),
      h("label", { class: "qs-field" }, h("span", {}, "Profile"), select),
      profile ? h("div", { class: "qs-two" },
        h("div", { class: expected === null ? "qs-callout warn" : "qs-callout info" }, h("div", { class: "qs-status-title" }, expected === null ? "Awaiting ruling" : `${expected} objective${expected === 1 ? "" : "s"}`), h("div", { class: "qs-muted" }, "Owned by the selected Mission profile.")),
        h("div", { class: battleNodes === null ? "qs-callout warn" : "qs-callout info" }, h("div", { class: "qs-status-title" }, battleNodes === null ? "Awaiting ruling" : `${battleNodes} battle node${battleNodes === 1 ? "" : "s"}`), h("div", { class: "qs-muted" }, battleNodes === null ? "Repository profile is unresolved." : "Combat profiles unlock after the Encounter editor lands."))) : null,
      expected !== null && expected > 0 ? h("div", { class: "qs-actions" }, h("button", { onClick: () => this.matchProfileShape() }, "Match profile shape")) : null,
      h("div", { class: "qs-muted" }, "Profile values are read from 48_DATA_mission_profiles.json. Forge does not maintain a second copy."));

    const authorCard = h("section", { class: "qs-card" }, h("div", { class: "qs-eyebrow" }, "Authoring intent"), h("h2", {}, "Mission brief"),
      this.field("Mission name", this.draft.name, (v) => { this.draft.name = v; this.buildState = null; this.saveDraft(); }, { placeholder: "A player-facing title" }),
      this.field("Premise / assignment", this.draft.description, (v) => { this.draft.description = v; this.buildState = null; this.saveDraft(); }, { multiline: true, placeholder: "What is happening, and why is the player involved?" }),
      this.field("Success outcome", this.draft.successDescription, (v) => { this.draft.successDescription = v; this.buildState = null; this.saveDraft(); }, { multiline: true, placeholder: "What changed when the player succeeds?" }));

    const storyboard = h("section", {}, h("div", { class: "qs-hero" }, h("h1", {}, "Storyboard"), h("p", {}, "Write the player experience. Technical objective wiring is generated from this linear foundation and checked canonically in the repository.")),
      ...beats,
      h("article", { class: "qs-card qs-end" }, h("div", { class: "qs-beat-top" }, h("div", { class: "qs-beat-num" }, (this.draft.beats?.length || 0) + 1), h("strong", {}, "Success ending")),
        h("p", { class: "qs-muted" }, this.draft.successDescription || "The success outcome above becomes the final quest completion beat.")),
      h("div", { class: "qs-actions" }, h("button", { onClick: () => { this.draft.beats.push({ description: "", choiceText: "Continue" }); this.buildState = null; this.saveDraft(); this.renderMission(); } }, "Add dialogue beat")));

    const readiness = problems.length
      ? h("div", { class: "qs-callout warn" }, h("div", { class: "qs-status-title" }, `Draft needs ${problems.length} change${problems.length === 1 ? "" : "s"} before compile`), h("ul", { class: "qs-list" }, problems.map((p) => h("li", {}, p))))
      : h("div", { class: "qs-callout ok" }, h("div", { class: "qs-status-title" }, "Ready for repository compile"), h("div", { class: "qs-muted" }, "Compile will save an exact Quest Source revision on a Studio branch and run canonical repository tooling. It will not touch the live game."));

    const build = h("section", { class: "qs-card" }, h("div", { class: "qs-eyebrow" }, "Repository build"), h("h2", {}, "Compile"), readiness,
      h("div", { class: "qs-actions" },
        h("button", { class: "qs-compile", disabled: !!problems.length || this.buildState?.busy, onClick: () => this.compileMission() }, this.buildState?.busy ? "Building…" : "Compile in repository"),
        this.draft.sourceCommit ? h("button", { disabled: this.buildState?.busy, onClick: () => this.refreshBuild(true) }, "Refresh build status") : null,
        h("button", { onClick: () => this.startNewMission() }, "New Mission")),
      this.renderBuildState());

    this.renderFrame(this.draft.name || "Mission", `Quest Studio · Mission · ${this.draft.requestId}`,
      h("div", { class: "qs-hero" }, h("h1", {}, "Mission Studio inside Quest Studio"), h("p", {}, "This first usable slice covers repository-backed no-combat Mission authoring. Encounter, graph and additional subtype adapters will extend this same workspace rather than create new tools.")),
      h("div", { class: "qs-two" }, profileCard, authorCard), storyboard, build);
  }

  renderBuildState() {
    const state = this.buildState;
    if (!state) return h("div", { class: "qs-muted" }, "No repository build has been requested for the current draft revision.");
    if (state.busy) return h("div", { class: "qs-callout info" }, h("div", { class: "qs-status-title" }, "Building in the repository…"), h("div", { class: "qs-muted" }, "Forge saved the Quest Source and requested canonical compilation. You can keep this Studio open while the worker runs."));
    if (state.error) return h("div", { class: "qs-callout bad" }, h("div", { class: "qs-status-title" }, "Repository request failed"), h("div", { class: "qs-muted" }, state.error));
    if (state.waiting) return h("div", { class: "qs-callout info" }, h("div", { class: "qs-status-title" }, "Build result not available yet"), h("div", { class: "qs-muted" }, "No current result has landed. The worker may still be running, or it may have failed before result persistence. Refresh status before resubmitting the source."));
    if (!state.result) return h("div", { class: "qs-muted" }, "No build result loaded.");

    const result = state.result;
    const stale = state.stale;
    const cls = result.status === "valid" ? "ok" : result.status === "blocked" ? "warn" : "bad";
    const title = result.status === "valid" ? "Mechanically valid" : result.status === "blocked" ? "Build blocked" : "Build failed";
    const detail = [];
    if (result.status === "blocked") detail.push(...(result.blockers || []).map((x) => x.message || String(x)));
    if (result.status === "failed") detail.push(...(result.errors || []).map((x) => x.message || String(x)));
    const counts = result.generated?.entities?.counts || {};
    const summary = Object.entries(counts).map(([k, v]) => `${v} ${k}`).join(" · ");
    const artCount = Array.isArray(result.art?.shots) ? result.art.shots.length : 0;

    return h("div", {},
      stale ? h("div", { class: "qs-callout warn" }, h("div", { class: "qs-status-title" }, "Older build result"), h("div", { class: "qs-muted" }, "This result belongs to an earlier Quest Source revision and is evidence only.")) : null,
      h("div", { class: `qs-callout ${cls}` }, h("div", { class: "qs-status-title" }, title),
        result.status === "valid" ? h("div", { class: "qs-muted" }, `${summary || "Manifest generated"}${artCount ? ` · ${artCount} art requirement${artCount === 1 ? "" : "s"}` : ""}. Live game untouched.`) : null,
        detail.length ? h("ul", { class: "qs-list" }, detail.map((x) => h("li", {}, x))) : null,
        (result.warnings || []).length ? h("details", {}, h("summary", {}, `${result.warnings.length} warning${result.warnings.length === 1 ? "" : "s"}`), h("ul", { class: "qs-list" }, result.warnings.map((x) => h("li", {}, x.message || String(x))))) : null),
      result.status === "valid" && !stale ? h("div", { class: "qs-actions" }, h("button", { onClick: () => this.inspectManifest() }, "Inspect generated manifest")) : null,
      state.manifestText ? h("label", { class: "qs-field" }, h("span", {}, "Generated manifest · inspection only"), h("textarea", { value: state.manifestText, readOnly: true, rows: 18 })) : null,
      h("div", { class: "qs-provenance" }, `Source revision: ${result.provenance?.sourceRevision || "unknown"} · Compiler: ${result.provenance?.compilerRevision || "unknown"}`));
  }

  async compileMission() {
    const problems = missionDraftProblems(this.draft, this.profiles);
    if (problems.length) return;
    this.pollToken++;
    const token = this.pollToken;
    this.buildState = { busy: true };
    this.renderMission();
    try {
      const source = missionSourceFromDraft(this.draft);
      const submitted = await this.repository.submit(source);
      if (token !== this.pollToken) return;
      this.draft.sourceCommit = submitted.sourceCommit;
      this.draft.lastResult = null;
      this.saveDraft();
      this.buildState = { busy: true, sourceCommit: submitted.sourceCommit };
      this.renderMission();
      await this.pollBuild(submitted.sourceCommit, token);
    } catch (e) {
      if (token !== this.pollToken) return;
      this.buildState = { error: e?.message || String(e) };
      this.renderMission();
    }
  }

  async pollBuild(sourceCommit, token) {
    for (let i = 0; i < this.maxPolls; i++) {
      if (token !== this.pollToken || this.shell?.hidden) return;
      const got = await this.repository.buildResult(this.draft.requestId, { expectedSourceCommit: sourceCommit });
      if (got && !got.stale) {
        this.draft.lastResult = got.result;
        this.saveDraft();
        this.buildState = { result: got.result, stale: false, sourceCommit };
        this.renderMission();
        return;
      }
      if (i + 1 < this.maxPolls) await new Promise((resolve) => setTimeout(resolve, this.pollMs));
    }
    if (token === this.pollToken) {
      this.buildState = { waiting: true, sourceCommit };
      this.renderMission();
    }
  }

  async refreshBuild(renderBusy = true) {
    if (!this.draft?.sourceCommit) return;
    const token = ++this.pollToken;
    if (renderBusy) { this.buildState = { busy: true, sourceCommit: this.draft.sourceCommit }; this.renderMission(); }
    try {
      const got = await this.repository.buildResult(this.draft.requestId, { expectedSourceCommit: this.draft.sourceCommit });
      if (token !== this.pollToken) return;
      if (!got) this.buildState = { waiting: true, sourceCommit: this.draft.sourceCommit };
      else this.buildState = { result: got.result, stale: got.stale, sourceCommit: this.draft.sourceCommit };
      this.renderMission();
    } catch (e) {
      if (token !== this.pollToken) return;
      this.buildState = { error: e?.message || String(e) };
      this.renderMission();
    }
  }

  async inspectManifest() {
    try {
      const result = this.buildState?.result;
      if (!result || result.status !== "valid") return;
      const text = await this.repository.generatedManifest(this.draft.requestId, result);
      this.buildState = { ...this.buildState, manifestText: text };
      this.renderMission();
    } catch (e) {
      const msg = e instanceof GithubError ? e.message : (e?.message || String(e));
      this.buildState = { error: `Could not load generated manifest: ${msg}` };
      this.renderMission();
    }
  }
}

export function installQuestStudio(app, options = {}) {
  const workspace = new QuestStudioWorkspace({ app, ...options });
  workspace.install();
  return workspace;
}
