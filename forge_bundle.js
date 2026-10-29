// TNR forge bundle v0.11.0 - full-page content builder, loaded via @require by forge_loader_user.js.
// Built from forge/src by forge/build.mjs (esbuild, IIFE). Do not edit by hand.
// Comments are stripped from this artifact by forge/tools/strip_comments.mjs and the strip is proven
// equivalent to the unstripped build at build time; every comment is still in forge/src.
// Entry: /forge (a providerless 404) arms the tab and hands off; Forge then mounts as an overlay on a
// real application route so ClerkProvider and the tRPC provider stay alive under it. Layers: storage, transport, budget, runner, reconcile, ui.
// Legacy engine facts (procedures, budgets): studie-tech/TheNinjaRPG@345d18accf6d8ea8d8d47ef0e61b5aff7d5a1cf9.
// Content field contracts (fields.json, nested.json): studie-tech/TheNinjaRPG@2af4b32066c39e2868efae5dba6b339278701dca.
// Scoped Bloodright contract: studie-tech/TheNinjaRPG@94f9d84c770004172ba423ada3d6710849acc451.
(() => {
  var JOURNAL_VERSION = 1;
  var KEY_PREFIX = "tnr_forge_job_v1:";
  var MAX_TEXT = 512;
  var ITEM_STATES = Object.freeze([
    "PLANNED",
    "SENT",
    "CONFIRMED",
    "VERIFIED",
    "FAILED",
    "ORPHANED",
    "SKIPPED"
  ]);
  var TERMINAL_ITEM_STATES = Object.freeze(["VERIFIED", "FAILED", "SKIPPED"]);
  var JOB_STATES = Object.freeze(["RUNNING", "PAUSED", "DONE", "INCOMPLETE", "ABORTED"]);
  var OPS = Object.freeze(["create", "update"]);
  var TRANSITIONS = Object.freeze({
    PLANNED: ["SENT", "FAILED", "SKIPPED", "CONFIRMED"],
    SENT: ["CONFIRMED", "ORPHANED", "FAILED"],
    CONFIRMED: ["SENT", "VERIFIED", "FAILED"],
    VERIFIED: [],
    FAILED: [],
    ORPHANED: ["CONFIRMED", "FAILED", "SKIPPED"],
    SKIPPED: []
  });
  var RESERVED = Object.freeze(["state", "idx", "sentAt", "confirmedAt", "verifiedAt", "createSentAt"]);
  function captureOk(capture) {
    if (!capture || capture.ok !== true) return false;
    return capture.persist !== "full" || capture.persistOk === true;
  }
  function jobOutcome(job) {
    if (!job || !Array.isArray(job.items)) return "open";
    if (job.state === "RUNNING" || job.state === "PAUSED") return "open";
    const captures = [...job.capturesBefore || [], ...job.capturesAfter || []];
    if (!job.items.length) {
      if (!captures.length) return "unverified";
      return captures.every(captureOk) ? "success" : "failed";
    }
    if (job.items.some((it) => it.state === "FAILED")) return "failed";
    if (job.items.some((it) => !TERMINAL_ITEM_STATES.includes(it.state) || it.state === "SKIPPED" || it.verify && it.verify !== "match" && it.verify !== "suggested")) return "unverified";
    if (captures.some((capture) => capture && capture.persist === "full" && capture.persistOk !== true)) return "unverified";
    return "success";
  }
  var StaleItem = class extends Error {
    constructor(m) {
      super(m);
      this.name = "StaleItem";
    }
  };
  var JournalError = class extends Error {
    constructor(message, info) {
      super(message);
      this.name = "JournalError";
      this.info = info;
    }
  };
  function nowIso(clock) {
    return new Date(clock()).toISOString();
  }
  function capText(v) {
    return typeof v === "string" && v.length > MAX_TEXT ? v.slice(0, MAX_TEXT - 1) + "\u2026" : v;
  }
  function capPatch(patch) {
    const out = {};
    for (const [k, v] of Object.entries(patch || {})) out[k] = capText(v);
    return out;
  }
  function newItem(idx, spec) {
    if (!spec || typeof spec !== "object") throw new JournalError("item spec must be an object", { idx });
    if (!OPS.includes(spec.op)) throw new JournalError(`item ${idx}: op must be create or update, got ${spec.op}`, { idx });
    if (typeof spec.entity !== "string" || !spec.entity) throw new JournalError(`item ${idx}: entity required`, { idx });
    return {
      idx,
      entity: spec.entity,
      op: spec.op,
      name: spec.name ?? null,
      srcId: spec.srcId ?? null,
      targetId: spec.targetId ?? null,
      payloadHash: spec.payloadHash ?? null,
      state: "PLANNED",
      phase: spec.op === "create" ? "create" : "update",
      entityId: spec.targetId ?? null,
      snapshotKey: null,
      sentAt: null,
      createSentAt: null,
      confirmedAt: null,
      verifiedAt: null,
      error: null
    };
  }
  function repairHistory(job) {
    if (!job || !Array.isArray(job.items)) return job;
    for (const it of job.items) {
      if (!it || typeof it !== "object" || it.state !== "PLANNED") continue;
      const proof = ["sentAt", "createSentAt", "confirmedAt", "verifiedAt"].filter((k) => it[k]);
      if (!proof.length) continue;
      it.state = "SENT";
      if (it.createSentAt && !it.entityId) it.phase = "create";
      else if (!it.phase || it.phase === "create") it.phase = it.entityId ? "update" : "create";
      it.sentAt = it.sentAt || it.createSentAt || it.confirmedAt || it.verifiedAt;
      it.repaired = `state PLANNED contradicted by ${proof.join(", ")}; restored to SENT for reconciliation`;
    }
    return job;
  }
  function validateJobShape(job) {
    if (!job || typeof job !== "object" || Array.isArray(job)) throw new JournalError("journal record is not an object");
    if (typeof job.jobId !== "string" || !job.jobId) throw new JournalError("journal record has no jobId");
    if (!Array.isArray(job.items)) throw new JournalError("journal record has no items array", { jobId: job.jobId });
    if (!JOB_STATES.includes(job.state)) throw new JournalError("journal record has unknown job state " + job.state, { jobId: job.jobId });
    job.items.forEach((it, i) => {
      if (!it || typeof it !== "object") throw new JournalError(`item ${i} is not an object`, { jobId: job.jobId });
      if (!ITEM_STATES.includes(it.state)) throw new JournalError(`item ${i} has unknown state ${it.state}`, { jobId: job.jobId });
      if (it.idx !== i) throw new JournalError(`item ${i} has idx ${it.idx}`, { jobId: job.jobId });
    });
    return job;
  }
  var RECLAIM_AGE_MS = 24 * 60 * 60 * 1e3;
  var RECLAIM_HEADROOM = 256 * 1024;
  var isQuotaError = (e) => !!e && (e.name === "QuotaExceededError" || e.name === "NS_ERROR_DOM_QUOTA_REACHED" || e.code === 22 || e.code === 1014 || /quota/i.test(String(e.message)));
  var Journal = class {
    constructor(storage, clock = () => Date.now(), { yieldTask = () => new Promise((r) => setTimeout(r, 0)) } = {}) {
      if (!storage || typeof storage.setItem !== "function") {
        throw new JournalError("Journal needs a Storage-like object");
      }
      this.storage = storage;
      this.clock = clock;
      this.yieldTask = yieldTask;
    }
    _key(jobId) {
      return KEY_PREFIX + jobId;
    }
    _write(job) {
      job.v = JOURNAL_VERSION;
      job.updatedAt = nowIso(this.clock);
      const text = JSON.stringify(job);
      try {
        try {
          this.storage.setItem(this._key(job.jobId), text);
        } catch (e) {
          if (!isQuotaError(e) || !this.reclaim(job.jobId, text.length)) throw e;
          this.storage.setItem(this._key(job.jobId), text);
        }
      } catch (e) {
        throw new JournalError("journal write failed: " + (e && e.message ? e.message : String(e)), {
          jobId: job.jobId,
          bytes: text.length,
          cause: e
        });
      }
      return job;
    }
    reclaimable(exceptJobId = null) {
      const now = this.clock();
      return this.listJobs().filter((j) => j.jobId !== exceptJobId && (j.state === "DONE" || j.state === "ABORTED")).filter((j) => !j.items.some((it) => it.state === "SENT")).filter((j) => j.exportedAt || now - Date.parse(j.updatedAt || j.startedAt || 0) > RECLAIM_AGE_MS).sort((a, b) => String(a.updatedAt || a.startedAt).localeCompare(String(b.updatedAt || b.startedAt)));
    }
    reclaim(exceptJobId, bytes) {
      let freed = 0;
      const want = bytes + RECLAIM_HEADROOM;
      for (const j of this.reclaimable(exceptJobId)) {
        if (freed >= want) break;
        const raw = this.storage.getItem(this._key(j.jobId));
        this.storage.removeItem(this._key(j.jobId));
        freed += raw ? raw.length : 0;
        (this.reclaimed ??= []).push(j.jobId);
      }
      return freed > 0;
    }
    _read(jobId) {
      const text = this.storage.getItem(this._key(jobId));
      if (text == null) return null;
      let job;
      try {
        job = JSON.parse(text);
      } catch (e) {
        throw new JournalError("journal record is not JSON: " + jobId, { jobId, cause: e, raw: text });
      }
      return validateJobShape(migrate(job));
    }
    listJobIds() {
      const ids = [];
      for (let i = 0; i < this.storage.length; i++) {
        const k = this.storage.key(i);
        if (k && k.startsWith(KEY_PREFIX) && k.length > KEY_PREFIX.length) ids.push(k.slice(KEY_PREFIX.length));
      }
      return ids;
    }
    listJobs() {
      const jobs = [];
      this.broken = [];
      for (const id2 of this.listJobIds()) {
        try {
          const j = this._read(id2);
          if (j) jobs.push(j);
        } catch (e) {
          this.broken.push({ jobId: id2, error: e.message, raw: this.storage.getItem(this._key(id2)) });
        }
      }
      return jobs.sort((a, b) => String(b.startedAt).localeCompare(String(a.startedAt)) || a.jobId.localeCompare(b.jobId));
    }
    get(jobId) {
      return this._read(jobId);
    }
    open({ jobId, manifestPath, manifestNumber: manifestNumber2, manifestHash: manifestHash2, items, allowEmpty = false, bloodrightImport = null }) {
      if (!jobId) throw new JournalError("jobId required");
      if (!Array.isArray(items) || !items.length && !allowEmpty) throw new JournalError("a job needs at least one item unless it is an explicit capture-only job");
      if (this._read(jobId)) throw new JournalError("job already exists: " + jobId, { jobId });
      if (manifestHash2) {
        const dup = this.resumable().find((j) => j.manifestHash === manifestHash2 && !(j.bloodrightImport && Object.keys(j.forgottenBindings ?? {}).length));
        if (dup) throw new JournalError(`an open job for this manifest already exists (${dup.jobId}); resume it instead`, { jobId: dup.jobId });
      }
      const job = {
        v: JOURNAL_VERSION,
        jobId,
        manifestPath: manifestPath ?? null,
        manifestNumber: manifestNumber2 ?? null,
        manifestHash: manifestHash2 ?? null,
        ...bloodrightImport ? { bloodrightImport } : {},
        startedAt: nowIso(this.clock),
        updatedAt: null,
        state: "RUNNING",
        pause: null,
        items: items.map((spec, i) => newItem(i, spec))
      };
      return this._write(job);
    }
    setJobState(jobId, state, extra = {}) {
      if (!JOB_STATES.includes(state)) throw new JournalError("bad job state: " + state);
      const job = this._mustRead(jobId);
      if ((state === "DONE" || state === "INCOMPLETE") && job.items.some((it) => it.state === "SENT")) throw new JournalError(`cannot mark ${state} with SENT items`, { jobId });
      if (state === "DONE" && job.items.some((it) => !TERMINAL_ITEM_STATES.includes(it.state))) {
        throw new JournalError("cannot mark DONE with unresolved items; use INCOMPLETE", { jobId });
      }
      job.state = state;
      job.pause = state === "PAUSED" ? extra.pause ?? job.pause ?? { reason: "unspecified" } : null;
      return this._write(job);
    }
    remove(jobId, { force = false } = {}) {
      const job = this._read(jobId);
      if (job && !force && job.items.some((it) => it.state === "SENT")) {
        throw new JournalError("refusing to delete a job with SENT items; reconcile it first", { jobId });
      }
      this.storage.removeItem(this._key(jobId));
    }
    _mustRead(jobId) {
      const job = this._read(jobId);
      if (!job) throw new JournalError("no such job: " + jobId, { jobId });
      return job;
    }
    transition(jobId, idx, to, patch = {}) {
      const job = this._mustRead(jobId);
      const item = job.items[idx];
      if (!item) throw new JournalError("no such item: " + idx, { jobId, idx });
      const from = item.state;
      if (from === "PLANNED" && to === "CONFIRMED" && !(patch.reused === true && patch.phase === "verify" && !!item.targetId && patch.entityId === item.targetId && item.op === "update" && ["skillTree", "skillTreeFolder"].includes(item.entity))) {
        throw new JournalError("PLANNED -> CONFIRMED requires read-only Bloodright reuse", { jobId, idx });
      }
      if (!TRANSITIONS[from] || !TRANSITIONS[from].includes(to)) {
        throw new JournalError(`illegal transition ${from} -> ${to}`, { jobId, idx, from, to });
      }
      const p = capPatch(patch);
      for (const k of RESERVED) if (k in p) throw new JournalError(`transition patch may not set ${k}`, { jobId, idx });
      if (from === "CONFIRMED" && to === "SENT") {
        const entityId = p.entityId ?? item.entityId;
        const phase = p.phase ?? item.phase;
        if (!entityId) throw new JournalError("CONFIRMED -> SENT needs an entityId (phase 2 of a create)", { jobId, idx });
        if (phase === "create") throw new JournalError("CONFIRMED -> SENT may not re-enter the create phase", { jobId, idx });
      }
      if (to === "SENT" && job.state !== "RUNNING") throw new JournalError(`cannot send while job is ${job.state}`, { jobId, idx });
      Object.assign(item, p);
      item.state = to;
      const at = nowIso(this.clock);
      if (to === "SENT") {
        item.sentAt = at;
        if (item.phase === "create" && !item.createSentAt) item.createSentAt = at;
      }
      if (to === "CONFIRMED") item.confirmedAt = at;
      if (to === "VERIFIED") item.verifiedAt = at;
      return this._write(job);
    }
    async withSent(jobId, idx, patch, thunk, beforeDispatch = null) {
      if (typeof patch === "function") {
        beforeDispatch = thunk;
        thunk = patch;
        patch = {};
      }
      const prior = structuredClone(this._mustRead(jobId).items[idx]);
      const attempt = (prior.attempt ?? 0) + 1;
      this.transition(jobId, idx, "SENT", { ...patch, attempt });
      await this.yieldTask();
      const ours = () => {
        const job = this._mustRead(jobId), it = job.items[idx];
        return job.state === "RUNNING" && it.state === "SENT" && it.attempt === attempt;
      };
      if (!ours()) {
        const job = this._mustRead(jobId);
        throw new StaleItem(`item ${idx} is ${job.items[idx].state}, job ${job.state}: another tab took over; nothing sent`);
      }
      if (beforeDispatch) {
        try {
          beforeDispatch();
        } catch (e) {
          if (ours()) {
            const job = this._mustRead(jobId);
            job.items[idx] = { ...prior, attempt, withdrawn: { at: nowIso(this.clock), reason: String(e && e.message).slice(0, MAX_TEXT) } };
            this._write(job);
          }
          throw e;
        }
      }
      return await thunk();
    }
    annotate(jobId, idx, patch) {
      const job = this._mustRead(jobId);
      const item = job.items[idx];
      if (!item) throw new JournalError("no such item: " + idx, { jobId, idx });
      const p = capPatch(patch);
      for (const k of RESERVED) if (k in p) throw new JournalError(`annotate may not set ${k}; use transition()`, { jobId, idx, key: k });
      Object.assign(item, p);
      return this._write(job);
    }
    annotateJob(jobId, patch) {
      const job = this._mustRead(jobId);
      for (const k of ["items", "state", "jobId", "v"]) if (k in (patch || {})) throw new JournalError("annotateJob may not set " + k, { jobId });
      Object.assign(job, patch);
      return this._write(job);
    }
    resumable() {
      return this.listJobs().filter((job) => job.state === "PAUSED" || job.state === "INCOMPLETE" || job.state === "RUNNING" && job.items.some((it) => !TERMINAL_ITEM_STATES.includes(it.state)));
    }
    ambiguous(jobId) {
      return this._mustRead(jobId).items.filter((it) => it.state === "SENT");
    }
    findHolder(entity, entityId, { exceptJobId = null, exceptIdx = null } = {}) {
      if (!entityId) return null;
      for (const job of this.listJobs()) {
        for (const it of job.items) {
          if (job.jobId === exceptJobId && it.idx === exceptIdx) continue;
          if (it.entityId === entityId && (!entity || it.entity === entity)) return { jobId: job.jobId, idx: it.idx, name: it.name ?? null, state: it.state };
        }
      }
      return null;
    }
    knownEntityIds(entity = null) {
      const ids =  new Set();
      for (const job of this.listJobs()) for (const it of job.items) if (it.entityId && (!entity || it.entity === entity)) ids.add(it.entityId);
      return ids;
    }
    exportText() {
      const jobs = this.listJobs();
      return JSON.stringify({ exportedAt: nowIso(this.clock), version: JOURNAL_VERSION, jobs, broken: this.broken ?? [] }, null, 1);
    }
  };
  var MIGRATIONS = {};
  function migrate(job) {
    if (!job || typeof job !== "object") throw new JournalError("journal record is not an object");
    let v = job.v ?? 1;
    if (!Number.isInteger(v) || v < 1) throw new JournalError("journal record has an invalid version: " + String(job.v));
    if (v > JOURNAL_VERSION) throw new JournalError(`journal v${v} is newer than this bundle (v${JOURNAL_VERSION}); update the app`, { v });
    while (v < JOURNAL_VERSION) {
      const step = MIGRATIONS[v];
      if (!step) throw new JournalError("no migration from journal v" + v);
      job = step(job);
      if (job.v !== v + 1) throw new JournalError("migration did not advance the version");
      v = job.v;
    }
    job.v = v;
    return repairHistory(job);
  }

  var contract_default = JSON.parse('{"_meta":{"pin":"94f9d84c770004172ba423ada3d6710849acc451","scope":"Bloodright potency import only; other effects intentionally refused","sources":{"app/src/validators/combat.ts":"a7530df9e0537d19aaa2ae3ad06ebe0da6c3f12a636c79b93932f57b4a02ff0a","app/src/server/api/routers/skillTree.ts":"9c8a498cf847639b8638fd296284fc428b82cbf0f0826d0bc3d8de98dc52f374","app/drizzle/constants.ts":"40590ebb64d483677b5fc5cc2629169f6b7f4b6a5ed950d49ae3dae03200603b","app/src/validators/skillTree.ts":"7cea7b987f5db45a21f72717ebec0300ef865b453a7b448d1c5fa8dcc2b97040"}},"skillFields":["name","image","description","target","tier","requiredSkillIds","costSkillPoints","pathType","bloodlineId","seichiSilverCost","hidden","skillType","folderId","effects"],"folderFields":["name","image","description","hidden","order"],"effectFields":["staticAssetPath","staticAnimation","appearAnimation","disappearAnimation","appearSfx","disappearSfx","rounds","timeTracker","power","powerPerLevel","direction","target","coordinateTargeting","friendlyFire","calculation","affectedTag","affectedElements","type","description"],"tags":["damage","increasedamagegiven","decreasedamagegiven","increasedamagetaken","decreasedamagetaken","afterburn","lifesteal","reflect","increaseheal","heal","vamp","absorb","consume","shield","pierce","drain","poison"],"elements":["Fire","Water","Wind","Earth","Lightning","Ice","Crystal","Dust","Shadow","Wood","Scorch","Storm","Magnet","Yin-Yang","Lava","Explosion","Light","Boil","Metal","Sand","None"],"procedures":{"skillTree.get":{"kind":"query","limited":true,"mcp":true,"auth":"public"},"skillTree.getAll":{"kind":"query","limited":true,"mcp":true,"auth":"public"},"skillTree.getAllFolders":{"kind":"query","limited":true,"mcp":true,"auth":"public"},"skillTree.create":{"kind":"mutation","limited":false,"mcp":false,"auth":"protected"},"skillTree.update":{"kind":"mutation","limited":false,"mcp":false,"auth":"protected"},"skillTree.createFolder":{"kind":"mutation","limited":false,"mcp":false,"auth":"protected"},"skillTree.updateFolder":{"kind":"mutation","limited":false,"mcp":false,"auth":"protected"}}}');

  var contract_default2 = JSON.parse(`{"_meta":{"source":"studie-tech/TheNinjaRPG","pin":"2aed7e4903cc68e18c01e0adb7aec8f39ddffc64","files":{"router":"app/src/server/api/routers/contentReview.ts","validators":"app/src/validators/contentReview.ts","constants":"app/drizzle/constants.ts","submit":"app/src/libs/contentReview/submit.ts"},"citations":{"contentReview.create":"contentReview.ts:305 create: protectedProcedure, input staffCreateProposalSchema, output baseServerResponse {success, message:'Sent for review'}; canSuggestContent(role)","contentReview.getQueue":"contentReview.ts:91 getQueue: protectedProcedure, input reviewQueueSchema {status, entityType?, cursor?, limit<=50}; non-reviewers see only their own","contentReview.getProposal":"contentReview.ts:185 getProposal: protectedProcedure, input {id}; null when absent or not visible","aiEditableKeys":"libs/contentReview/entities.ts AI_EDITABLE_KEYS: the only AI fields the desk keeps (editableOf)"},"notSuggestible":{"quest":"quests.get masks hideLocation objectives (sector 1337) and tracked coordinates for callers who cannot change content (libs/quest.ts controlShownQuestLocationInformation); a suggestion built from it would overwrite the real objectives on approval"}},"procedures":{"contentReview.create":{"kind":"mutation","limited":false,"mcp":false,"auth":"protected"},"contentReview.getQueue":{"kind":"query","limited":false,"mcp":false,"auth":"protected"},"contentReview.getProposal":{"kind":"query","limited":false,"mcp":false,"auth":"protected"}},"entityTypes":{"jutsu":"JUTSU","item":"ITEM","bloodline":"BLOODLINE","asset":"GAME_ASSET","ai":"AI"},"categories":["GRAMMAR","BALANCE","SOUND","ANIMATION","VISUAL","CONSISTENCY","NEW_CONTENT"],"titleLength":{"min":3,"max":120},"rationaleLength":{"min":10,"max":4000},"statuses":["PENDING","APPLIED","REJECTED","OUTDATED","REVERTED"],"aiEditableKeys":["username","npcTitle","avatar","avatar3d","avatarFacing","gender","level","regeneration","rank","bloodlineId","offence","defence","ninjutsuMastery","genjutsuMastery","taijutsuMastery","bukijutsuMastery","bloodlineMastery","sageMastery","statsMultiplier","poolsMultiplier","strength","intelligence","willpower","speed","isSummon","inArena","inShrines","primaryElement","secondaryElement","preferredGeneral1","preferredGeneral2","anbuId","clanId","jutsus","items","effects"]}`);

  var contract_default3 = JSON.parse('{"_meta":{"pin":"107d7a86894f806a4c9cec89effef5992118a0ed","scope":"Dungeon definitions only (coop.dungeon.save / coop.dungeon.getAll); lobby, run and claim procedures are out of scope","sources":{"app/src/validators/dungeon.ts":"3ef77e9821e5b456a80c351b8fb91920d730be364d275d3927f6c22c23df0e27","app/src/server/api/routers/dungeon.ts":"6280604be39691695ea72c6e6026ba8f521586b847fd4130dc30463aee8b6ead","app/src/validators/coop.ts":"e4e3c2c5b8e2a7bb865967933b0c51ce5968199fee5e274a27b7b66edf95e450","app/src/validators/mapLocation.ts":"274f5a713ba37c6dea42102071a29fb3ecfca4d563d19a663e3fb6e9f8222b0e","app/drizzle/constants.ts":"4d3cf207812a7ef9403fb4b4e9a5bc74cc2baec8c5ea51b69d4f426bbcedab75","app/src/libs/dungeonRewards.ts":"4db0b8fb142c03d93021a6da08c4b090a4e4566e34c6638b21011a898d054ae8","app/src/server/api/root.ts":"6f1e67f3d56c9fc60f43fa557ab529c384970896325f1c0db779fa4f968259a9","app/src/server/api/routers/coop.ts":"2ef0395758c845fe4f5dbc093a3b1a9b38b8bd27915a07e511c8a51508eac898"}},"contentFields":["name","description","structureAssetId","structureScale","sector","longitude","latitude","expiresAt","hidden","background","tiers","rewards"],"rewardFields":["money","experience","tokens","prestige","drops"],"dropFields":["type","id","chance","quantity","package"],"floorFields":["kind","waves"],"waveFields":["aiIds","delayRounds"],"floorKinds":["floor","mini-boss","boss"],"dropTypes":["item","jutsu","cache","package"],"biomes":["ocean","ground","dessert","ice","snow","arena","default"],"bounds":{"nameMax":100,"descriptionMax":2000,"structureAssetIdMax":191,"structureScale":{"min":0.2,"max":5,"default":1},"sector":{"min":0,"max":1943},"longitude":{"min":0,"max":25},"latitude":{"min":0,"max":25},"maxTiers":4,"floorsPerTier":5,"maxWaves":5,"maxMobs":10,"maxWaveDelayRounds":20,"maxDrops":100,"chance":{"min":1,"max":100},"maxRewardQuantity":100,"maxRewardAmount":1000000000,"maxGrantedItems":2000},"defaults":{"content":{"description":"","structureAssetId":"","structureScale":1,"hidden":true,"background":"default"},"rewards":{"money":0,"experience":0,"tokens":0,"prestige":0,"drops":[]},"drop":{"quantity":1},"wave":{"delayRounds":0}},"facts":{"partySize":3,"runSeconds":3600,"inactiveRounds":3},"procedures":{"coop.dungeon.getAll":{"kind":"query","limited":false,"mcp":false,"auth":"protected"},"coop.dungeon.save":{"kind":"mutation","limited":true,"mcp":false,"auth":"protected"}}}');

  var PROCEDURES = Object.freeze({
    ...contract_default.procedures,
    ...contract_default2.procedures,
    ...contract_default3.procedures,
    "ai.createAiProfile": { kind: "mutation", limited: false, mcp: false, auth: "protected" },
    "ai.getAiProfile": { kind: "query", limited: false, mcp: true, auth: "protected" },
    "ai.toggleAiProfile": { kind: "mutation", limited: false, mcp: false, auth: "protected" },
    "ai.updateAiProfile": { kind: "mutation", limited: false, mcp: false, auth: "protected" },
    "badge.create": { kind: "mutation", limited: false, mcp: false, auth: "protected" },
    "badge.get": { kind: "query", limited: true, mcp: true, auth: "public" },
    "badge.getAllNames": { kind: "query", limited: true, mcp: true, auth: "public" },
    "badge.update": { kind: "mutation", limited: false, mcp: false, auth: "protected" },
    "title.create": { kind: "mutation", limited: false, mcp: false, auth: "protected" },
    "title.get": { kind: "query", limited: false, mcp: false, auth: "protected" },
    "title.getAll": { kind: "query", limited: false, mcp: false, auth: "protected" },
    "title.getAllNames": { kind: "query", limited: true, mcp: false, auth: "public" },
    "title.update": { kind: "mutation", limited: false, mcp: false, auth: "protected" },
    "bloodline.create": { kind: "mutation", limited: false, mcp: false, auth: "protected" },
    "bloodline.delete": { kind: "mutation", limited: false, mcp: false, auth: "protected" },
    "bloodline.get": { kind: "query", limited: true, mcp: true, auth: "public" },
    "bloodline.getAll": { kind: "query", limited: true, mcp: true, auth: "public" },
    "bloodline.getAllNames": { kind: "query", limited: true, mcp: true, auth: "public" },
    "bloodline.update": { kind: "mutation", limited: false, mcp: false, auth: "protected" },
    "gameAsset.create": { kind: "mutation", limited: false, mcp: false, auth: "protected" },
    "gameAsset.delete": { kind: "mutation", limited: false, mcp: false, auth: "protected" },
    "gameAsset.get": { kind: "query", limited: true, mcp: true, auth: "public" },
    "gameAsset.getAll": { kind: "query", limited: true, mcp: true, auth: "public" },
    "gameAsset.getAllNames": { kind: "query", limited: true, mcp: true, auth: "public" },
    "gameAsset.update": { kind: "mutation", limited: false, mcp: false, auth: "protected" },
    "item.clone": { kind: "mutation", limited: false, mcp: false, auth: "protected" },
    "item.create": { kind: "mutation", limited: false, mcp: false, auth: "protected" },
    "item.delete": { kind: "mutation", limited: false, mcp: false, auth: "protected" },
    "item.get": { kind: "query", limited: true, mcp: true, auth: "public" },
    "item.getAll": { kind: "query", limited: true, mcp: true, auth: "public" },
    "item.getAllNames": { kind: "query", limited: true, mcp: true, auth: "public" },
    "item.getItemWithCraftingRequirements": { kind: "query", limited: true, mcp: true, auth: "public" },
    "item.update": { kind: "mutation", limited: false, mcp: false, auth: "protected" },
    "jutsu.create": { kind: "mutation", limited: false, mcp: false, auth: "protected" },
    "jutsu.delete": { kind: "mutation", limited: false, mcp: false, auth: "protected" },
    "jutsu.get": { kind: "query", limited: true, mcp: true, auth: "public" },
    "jutsu.getAll": { kind: "query", limited: true, mcp: true, auth: "public" },
    "jutsu.getAllNames": { kind: "query", limited: true, mcp: true, auth: "public" },
    "jutsu.update": { kind: "mutation", limited: false, mcp: false, auth: "protected" },
    "petSpecies.create": { kind: "mutation", limited: false, mcp: false, auth: "protected" },
    "petSpecies.get": { kind: "query", limited: true, mcp: false, auth: "public" },
    "petSpecies.getAll": { kind: "query", limited: true, mcp: false, auth: "public" },
    "petSpecies.update": { kind: "mutation", limited: false, mcp: false, auth: "protected" },
    "profile.cloneAi": { kind: "mutation", limited: false, mcp: false, auth: "protected" },
    "profile.create": { kind: "mutation", limited: false, mcp: true, auth: "protected" },
    "profile.delete": { kind: "mutation", limited: false, mcp: true, auth: "protected" },
    "profile.getAi": { kind: "query", limited: false, mcp: true, auth: "protected" },
    "profile.getAllAiNames": { kind: "query", limited: true, mcp: true, auth: "public" },
    "profile.updateAi": { kind: "mutation", limited: false, mcp: true, auth: "protected" },
    "quests.checkRewards": { kind: "mutation", limited: false, mcp: true, auth: "protected" },
    "quests.clone": { kind: "mutation", limited: false, mcp: true, auth: "protected" },
    "quests.create": { kind: "mutation", limited: false, mcp: true, auth: "protected" },
    "quests.delete": { kind: "mutation", limited: false, mcp: true, auth: "protected" },
    "quests.get": { kind: "query", limited: true, mcp: true, auth: "public" },
    "quests.getAll": { kind: "query", limited: true, mcp: true, auth: "public" },
    "quests.getAllNames": { kind: "query", limited: true, mcp: true, auth: "public" },
    "quests.update": { kind: "mutation", limited: false, mcp: true, auth: "protected" }
  });
  function procedure(path) {
    const p = PROCEDURES[path];
    if (!p) throw new Error("unknown procedure: " + path + " (not in the audited crud surface)");
    return p;
  }
  function isProtected(path) {
    return procedure(path).auth === "protected";
  }
  function isLimited(path) {
    return procedure(path).limited === true;
  }
  var LIMITED_PATHS = Object.freeze(Object.keys(PROCEDURES).filter((p) => PROCEDURES[p].limited));
  var MUTATION_PATHS = Object.freeze(Object.keys(PROCEDURES).filter((p) => PROCEDURES[p].kind === "mutation"));
  var PROTECTED_PATHS = Object.freeze(Object.keys(PROCEDURES).filter((p) => PROCEDURES[p].auth === "protected"));

  var DB_NAME = "tnr_forge";
  var STORE = "captures";
  var SNAPSHOT_STORE = "capture_snapshots";
  var DB_VERSION = 2;
  function captureKey(path, id2) {
    return `${path}:${id2 ?? ""}`;
  }
  function snapshotKey(jobId, phase, ordinal) {
    return `${jobId}::${phase}::${ordinal}`;
  }
  var FULL_PERSIST_PATHS = Object.freeze([
    "skillTree.get",
    "gameAsset.get",
    "jutsu.get",
    "item.get",
    "item.getItemWithCraftingRequirements",
    "bloodline.get",
    "quests.get",
    "badge.get",
    "title.get",
    "profile.getAi",
    "ai.getAiProfile"
  ]);
  function canPersistFull(path) {
    return FULL_PERSIST_PATHS.includes(path);
  }
  var MAX_FULL_CAPTURE_BYTES = 512 * 1024;
  var ENTITY_OF_PATH = Object.freeze({
    jutsu: "jutsu",
    item: "item",
    bloodline: "bloodline",
    gameAsset: "asset",
    quests: "quest",
    profile: "ai",
    ai: "ai"
  });
  function entityOfPath(path) {
    const router = String(path).split(".")[0];
    return ENTITY_OF_PATH[router] ?? router;
  }
  function reqToPromise(req) {
    return new Promise((resolve, reject) => {
      req.onsuccess = () => resolve(req.result);
      req.onerror = () => reject(req.error);
    });
  }
  var CaptureCache = class {
    constructor(idb, clock = () => Date.now()) {
      if (!idb || typeof idb.open !== "function") throw new Error("CaptureCache needs an IDBFactory");
      this.idb = idb;
      this.clock = clock;
      this._db = null;
    }
    async _open() {
      if (this._db) return this._db;
      if (!this._opening) {
        this._opening = (async () => {
          const req = this.idb.open(DB_NAME, DB_VERSION);
          req.onupgradeneeded = () => {
            const db2 = req.result;
            if (!db2.objectStoreNames.contains(STORE)) {
              const store = db2.createObjectStore(STORE, { keyPath: "key" });
              store.createIndex("entity", "entity", { unique: false });
              store.createIndex("path", "path", { unique: false });
            }
            if (!db2.objectStoreNames.contains(SNAPSHOT_STORE)) {
              const snaps = db2.createObjectStore(SNAPSHOT_STORE, { keyPath: "key" });
              snaps.createIndex("jobId", "jobId", { unique: false });
            }
          };
          const db = await new Promise((resolve, reject) => {
            req.onsuccess = () => resolve(req.result);
            req.onerror = () => reject(req.error);
            req.onblocked = () => reject(new Error("tnr_forge open blocked by another connection"));
          });
          db.onversionchange = () => {
            db.close();
            if (this._db === db) this._db = null;
          };
          db.onclose = () => {
            if (this._db === db) this._db = null;
          };
          this._db = db;
          return db;
        })().finally(() => {
          this._opening = null;
        });
      }
      return this._opening;
    }
    async _tx(mode, fn, storeName = STORE) {
      let db = await this._open();
      let tx;
      try {
        tx = db.transaction(storeName, mode);
      } catch (e) {
        if (e && e.name === "InvalidStateError") {
          this._db = null;
          db = await this._open();
          tx = db.transaction(storeName, mode);
        } else throw e;
      }
      const store = tx.objectStore(storeName);
      const result = await fn(store);
      await new Promise((resolve, reject) => {
        tx.oncomplete = () => resolve();
        tx.onerror = () => reject(tx.error);
        tx.onabort = () => reject(tx.error);
      });
      return result;
    }
    async put({ path, id: id2, input, data }) {
      id2 = id2 == null || id2 === "" ? "" : String(id2);
      const rec = {
        key: captureKey(path, id2),
        path,
        id: id2 === "" ? null : id2,
        entity: entityOfPath(path),
        input: input ?? null,
        data,
        at: new Date(this.clock()).toISOString(),
        bytes: JSON.stringify(data ?? null).length
      };
      await this._tx("readwrite", (s) => reqToPromise(s.put(rec)));
      return rec;
    }
    async get(path, id2) {
      const rec = await this._tx("readonly", (s) => reqToPromise(s.get(captureKey(path, id2))));
      return rec ?? null;
    }
    async has(path, id2) {
      return await this.get(path, id2) != null;
    }
    async delete(path, id2) {
      await this._tx("readwrite", (s) => reqToPromise(s.delete(captureKey(path, id2))));
    }
    async invalidateEntity(entity) {
      return this._tx("readwrite", async (s) => {
        const idx = s.index("entity");
        const keys = await reqToPromise(idx.getAllKeys(entity));
        for (const k of keys) await reqToPromise(s.delete(k));
        return keys.length;
      });
    }
    async invalidateRecord(entity, id2) {
      return this._tx("readwrite", async (s) => {
        const idx = s.index("entity");
        const recs = await reqToPromise(idx.getAll(entity));
        let n = 0;
        const want = id2 == null ? "" : String(id2);
        for (const r of recs) {
          if (String(r.id ?? "") === want || r.id === null || r.id === "") {
            await reqToPromise(s.delete(r.key));
            n++;
          }
        }
        return n;
      });
    }
    async list() {
      const recs = await this._tx("readonly", (s) => reqToPromise(s.getAll()));
      return recs.map(({ key, path, id: id2, entity, at, bytes }) => ({ key, path, id: id2, entity, at, bytes }));
    }
    async size() {
      const recs = await this.list();
      return { count: recs.length, bytes: recs.reduce((a, r) => a + (r.bytes || 0), 0) };
    }
    async clear() {
      await this._tx("readwrite", (s) => reqToPromise(s.clear()));
    }
    async putSnapshot({ key, jobId, phase, ordinal, path, id: id2, input, data }) {
      const rec = {
        key,
        jobId,
        phase,
        ordinal,
        path,
        id: id2 == null || id2 === "" ? null : String(id2),
        entity: entityOfPath(path),
        input: input ?? null,
        data,
        at: new Date(this.clock()).toISOString(),
        bytes: JSON.stringify(data ?? null).length
      };
      await this._tx("readwrite", (s) => reqToPromise(s.put(rec)), SNAPSHOT_STORE);
      return rec;
    }
    async getSnapshot(key) {
      const rec = await this._tx("readonly", (s) => reqToPromise(s.get(key)), SNAPSHOT_STORE);
      return rec ?? null;
    }
    async listSnapshots() {
      const recs = await this._tx("readonly", (s) => reqToPromise(s.getAll()), SNAPSHOT_STORE);
      return recs.map(({ key, jobId, phase, ordinal, path, id: id2, entity, at, bytes }) => ({ key, jobId, phase, ordinal, path, id: id2, entity, at, bytes }));
    }
    async deleteSnapshot(key) {
      await this._tx("readwrite", (s) => reqToPromise(s.delete(key)), SNAPSHOT_STORE);
    }
    async deleteSnapshotsForJob(jobId) {
      return this._tx("readwrite", async (s) => {
        const keys = await reqToPromise(s.index("jobId").getAllKeys(jobId));
        for (const k of keys) await reqToPromise(s.delete(k));
        return keys.length;
      }, SNAPSHOT_STORE);
    }
    async clearSnapshots() {
      await this._tx("readwrite", (s) => reqToPromise(s.clear()), SNAPSHOT_STORE);
    }
    close() {
      if (this._db) {
        this._db.close();
        this._db = null;
      }
    }
  };

  var REPO_DB_NAME = "tnr_forge_repo";
  var REPO_DB_VERSION = 1;
  var STORE2 = "text";
  function reqToPromise2(req) {
    return new Promise((resolve, reject) => {
      req.onsuccess = () => resolve(req.result);
      req.onerror = () => reject(req.error || new Error("IndexedDB request failed"));
    });
  }
  var RepoTextCache = class {
    constructor(idb, clock = () => Date.now()) {
      this.idb = idb;
      this.clock = clock;
      this._db = null;
    }
    async _open() {
      if (this._db) return this._db;
      this._db = await new Promise((resolve, reject) => {
        const req = this.idb.open(REPO_DB_NAME, REPO_DB_VERSION);
        req.onupgradeneeded = () => {
          const db = req.result;
          if (!db.objectStoreNames.contains(STORE2)) db.createObjectStore(STORE2, { keyPath: "key" });
        };
        req.onsuccess = () => resolve(req.result);
        req.onerror = () => reject(req.error || new Error("could not open " + REPO_DB_NAME));
      });
      return this._db;
    }
    async _tx(mode, fn) {
      const db = await this._open();
      const tx = db.transaction(STORE2, mode);
      const out = await fn(tx.objectStore(STORE2));
      await new Promise((resolve, reject) => {
        tx.oncomplete = () => resolve();
        tx.onerror = () => reject(tx.error || new Error("repo text transaction failed"));
        tx.onabort = () => reject(tx.error || new Error("repo text transaction aborted"));
      });
      return out;
    }
    async put({ path, id: id2, data }) {
      const key = `${path}\0${id2}`;
      await this._tx("readwrite", (s) => reqToPromise2(s.put({ key, path, id: id2, data, at: this.clock() })));
      return key;
    }
    async get(path, id2) {
      const rec = await this._tx("readonly", (s) => reqToPromise2(s.get(`${path}\0${id2}`)));
      return rec ?? null;
    }
    async clear() {
      await this._tx("readwrite", (s) => reqToPromise2(s.clear()));
    }
    async size() {
      const recs = await this._tx("readonly", (s) => reqToPromise2(s.getAll()));
      return { count: recs.length, bytes: recs.reduce((a, r) => a + JSON.stringify(r.data ?? null).length, 0) };
    }
  };

  var ASSET_DB_NAME = "tnr_forge_assets";
  var ASSET_DB_VERSION = 1;
  var STORE3 = "bytes";
  var MAX_ASSET_BYTES = 2 * 1024 * 1024;
  var ASSET_UPLOADS_KEY = "tnr_forge_asset_uploads_v1";
  function reqToPromise3(req) {
    return new Promise((resolve, reject) => {
      req.onsuccess = () => resolve(req.result);
      req.onerror = () => reject(req.error || new Error("IndexedDB request failed"));
    });
  }
  var AssetCache = class {
    constructor(idb, clock = () => Date.now()) {
      this.idb = idb;
      this.clock = clock;
      this._db = null;
    }
    async _open() {
      if (this._db) return this._db;
      this._db = await new Promise((resolve, reject) => {
        const req = this.idb.open(ASSET_DB_NAME, ASSET_DB_VERSION);
        req.onupgradeneeded = () => {
          const db = req.result;
          if (!db.objectStoreNames.contains(STORE3)) db.createObjectStore(STORE3, { keyPath: "sha256" });
        };
        req.onsuccess = () => resolve(req.result);
        req.onerror = () => reject(req.error || new Error("could not open " + ASSET_DB_NAME));
      });
      return this._db;
    }
    async _tx(mode, fn) {
      const db = await this._open();
      const tx = db.transaction(STORE3, mode);
      const out = await fn(tx.objectStore(STORE3));
      await new Promise((resolve, reject) => {
        tx.oncomplete = () => resolve();
        tx.onerror = () => reject(tx.error || new Error("asset transaction failed"));
        tx.onabort = () => reject(tx.error || new Error("asset transaction aborted"));
      });
      return out;
    }
    async put({ sha256: sha2562, bytes, path = null, ref = null }) {
      const size = bytes.byteLength ?? bytes.length ?? 0;
      if (size > MAX_ASSET_BYTES) throw new Error(`asset ${sha2562.slice(0, 12)} is ${size} bytes, over the ${MAX_ASSET_BYTES}-byte cache limit`);
      await this._tx("readwrite", (s) => reqToPromise3(s.put({ sha256: sha2562, bytes, size, path, ref, at: this.clock() })));
      return sha2562;
    }
    async get(sha2562) {
      const rec = await this._tx("readonly", (s) => reqToPromise3(s.get(sha2562)));
      return rec ?? null;
    }
    async delete(sha2562) {
      await this._tx("readwrite", (s) => reqToPromise3(s.delete(sha2562)));
    }
    async clear() {
      await this._tx("readwrite", (s) => reqToPromise3(s.clear()));
    }
    async size() {
      const recs = await this._tx("readonly", (s) => reqToPromise3(s.getAll()));
      return { count: recs.length, bytes: recs.reduce((a, r) => a + (r.size || 0), 0) };
    }
  };
  function readJson(storage, key) {
    const raw = storage.getItem(key);
    if (raw == null || raw === "") return {};
    let v;
    try {
      v = JSON.parse(raw);
    } catch {
      v = void 0;
    }
    if (!v || typeof v !== "object" || Array.isArray(v)) return {};
    return v;
  }
  function readAssetUploads(storage) {
    return readJson(storage, ASSET_UPLOADS_KEY);
  }
  function forgetAssetUpload(storage, sha2562) {
    const map = readAssetUploads(storage);
    if (!(sha2562 in map)) return map;
    delete map[sha2562];
    storage.setItem(ASSET_UPLOADS_KEY, JSON.stringify(map));
    return map;
  }
  async function liveAssetUploads(storage, probe, shas = null, { forget = false } = {}) {
    const map = readAssetUploads(storage);
    if (typeof probe !== "function") return map;
    for (const [sha, rec] of Object.entries(map)) {
      if (shas && !shas.has(sha)) continue;
      if (await probe(rec?.url) === false) {
        delete map[sha];
        if (forget) forgetAssetUpload(storage, sha);
      }
    }
    return map;
  }
  function recordAssetUpload(storage, sha2562, url2, { path = null, ref = null, at = Date.now() } = {}) {
    const map = readAssetUploads(storage);
    map[sha2562] = { url: url2, at, path, ref };
    storage.setItem(ASSET_UPLOADS_KEY, JSON.stringify(map));
    return map;
  }

  var SessionRefused = class extends Error {
    constructor(message) {
      super(message);
      this.name = "SessionRefused";
      this.sent = false;
    }
  };
  var Session = class {
    async fetch(_url, _init) {
      throw new Error("Session.fetch not implemented");
    }
    describe() {
      return { kind: "abstract" };
    }
  };
  var CookieSession = class _CookieSession extends Session {
    constructor({ fetchImpl, origin = "" } = {}) {
      super();
      if (typeof fetchImpl !== "function") throw new Error("CookieSession needs fetchImpl");
      this.fetchImpl = (u, i) => fetchImpl(u, i);
      this.origin = origin;
    }
    static ALLOWED_PATHS = /^\/api\/(trpc\/|uploadthing(\?|$))/;
    static ALLOWED_HEADERS =  new Set(["content-type", "x-uploadthing-version", "accept"]);
    async fetch(url2, init = {}) {
      if (typeof url2 !== "string" || !_CookieSession.ALLOWED_PATHS.test(url2)) {
        throw new SessionRefused("CookieSession only issues same-origin /api/trpc and /api/uploadthing requests, got " + String(url2).slice(0, 80));
      }
      const headers = new Headers();
      new Headers(init.headers ?? {}).forEach((v, k) => {
        if (!_CookieSession.ALLOWED_HEADERS.has(k)) throw new SessionRefused(`CookieSession refuses header ${k} on a game request`);
        headers.set(k, v);
      });
      return this.fetchImpl(this.origin + url2, { ...init, headers, credentials: "same-origin" });
    }
    describe() {
      return { kind: "cookie", origin: this.origin || "(same-origin)" };
    }
  };

  var NANOID_RE = /^[A-Za-z0-9_-]{21}$/;
  var OutcomeError = class extends Error {
    constructor(message, info = {}) {
      super(message);
      this.name = "OutcomeError";
      Object.assign(this, info);
    }
  };
  function isBaseServerResponse(v) {
    return !!v && typeof v === "object" && typeof v.success === "boolean" && typeof v.message === "string";
  }
  function readMutation(decoded) {
    if (!decoded.ok) {
      if (decoded.error.code === "MALFORMED_ELEMENT") {
        throw new OutcomeError("mutation element is undecodable; the write may have landed: " + decoded.error.message, { error: decoded.error, ambiguous: true });
      }
      return { kind: "error", message: decoded.error.message, error: decoded.error };
    }
    const d = decoded.data;
    if (!isBaseServerResponse(d)) {
      throw new OutcomeError("mutation returned something other than baseServerResponse", { data: d });
    }
    if (!d.success) return { kind: "refused", message: d.message };
    const out = { kind: "ok", message: d.message };
    if (NANOID_RE.test(d.message)) out.id = d.message;
    return out;
  }
  function readCreate(decoded) {
    const o = readMutation(decoded);
    if (o.kind === "ok" && !o.id) {
      throw new OutcomeError("create reported success but message is not an id: " + JSON.stringify(o.message).slice(0, 80), { outcome: o });
    }
    return o;
  }
  function classifyError(error) {
    const code = error?.code;
    if (code === "TOO_MANY_REQUESTS") return "RATE_LIMITED";
    if (code === "UNAUTHORIZED") return "SESSION";
    if (code === "BAD_REQUEST" && error.zodError) return "VALIDATION";
    if (code === "METHOD_NOT_SUPPORTED") return "CLIENT_BUG";
    if (code === "NOT_FOUND") {
      const m = String(error.message || "");
      if (/^No procedure found on path/.test(m)) return "CLIENT_BUG";
      if (/Please complete registration\.$/.test(m)) return "SESSION";
      return "NOT_FOUND";
    }
    if (code === "MALFORMED_ELEMENT") return "CLIENT_BUG";
    if (code === "INTERNAL_SERVER_ERROR" && /Output validation failed/.test(String(error.message || ""))) return "CONTRACT";
    return "SERVER";
  }

  var AUTH = Object.freeze({ UNKNOWN: "unknown", PROBING: "probing", READY: "ready", SIGNED_OUT: "signed_out" });
  var PROBE_PATH = "profile.getAi";
  var PROBE_ID = "forge-auth-probe-0000";
  var AuthUnavailable = class extends Error {
    constructor(state, path) {
      super(`TNR authentication is ${state === AUTH.SIGNED_OUT ? "signed out" : "not confirmed"}; ${path} is a protected procedure and was not sent`);
      this.name = "AuthUnavailable";
      this.state = state;
      this.path = path;
      this.sent = false;
    }
  };
  var AuthRefused = class extends Error {
    constructor(path, error) {
      super(`the game refused ${path} as unauthenticated`);
      this.name = "AuthRefused";
      this.path = path;
      this.error = error;
    }
  };
  var AuthState = class {
    constructor({ client = null, runtime = null, clock = () => Date.now(), state = AUTH.UNKNOWN } = {}) {
      this.client = client;
      this.runtime = runtime;
      this.clock = clock;
      this.state = state;
      this.at = null;
      this.detail = null;
      this.listeners =  new Set();
    }
    get ready() {
      return this.state === AUTH.READY;
    }
    get signedOut() {
      return this.state === AUTH.SIGNED_OUT;
    }
    onChange(fn) {
      this.listeners.add(fn);
      return () => this.listeners.delete(fn);
    }
    _set(state, detail = null) {
      const changed = this.state !== state || this.detail !== detail;
      this.state = state;
      this.detail = detail;
      if (state === AUTH.READY || state === AUTH.SIGNED_OUT) this.at = this.clock();
      if (changed) for (const fn of this.listeners) {
        try {
          fn(this);
        } catch {
        }
      }
      return state;
    }
    runtimeStatus() {
      if (typeof this.runtime !== "function") return { present: false, loaded: false, signedIn: null };
      let r = null;
      try {
        r = this.runtime();
      } catch {
        r = null;
      }
      if (!r) return { present: false, loaded: false, signedIn: null };
      return { present: true, loaded: !!r.loaded, signedIn: r.signedIn === null || r.signedIn === void 0 ? null : !!r.signedIn };
    }
    async waitForRuntime({ timeoutMs = 15e3, pollMs = 100, sleep } = {}) {
      const wait = sleep ?? ((ms) => new Promise((r) => setTimeout(r, ms)));
      const deadline = this.clock() + timeoutMs;
      let status = this.runtimeStatus();
      while (!(status.present && status.loaded) && this.clock() < deadline) {
        await wait(pollMs);
        status = this.runtimeStatus();
      }
      return status;
    }
    async probe() {
      if (!this.client) return this._set(AUTH.UNKNOWN, "no transport is wired for the auth check");
      const status = this.runtimeStatus();
      if (status.present && status.loaded && status.signedIn === false) {
        return this._set(AUTH.SIGNED_OUT, "the page's Clerk runtime reports no signed-in session");
      }
      this._set(AUTH.PROBING);
      let decoded;
      try {
        decoded = await this.client.call(PROBE_PATH, { userId: PROBE_ID });
      } catch (e) {
        return this._set(AUTH.UNKNOWN, "the auth check could not reach the game: " + String(e && e.message || e).slice(0, 160));
      }
      if (decoded && decoded.ok) return this._set(AUTH.READY, "a protected procedure answered for this session");
      const cls = classifyError(decoded && decoded.error);
      if (cls === "SESSION") return this._set(AUTH.SIGNED_OUT, "the game refused a protected procedure: " + String(decoded.error.code));
      if (cls === "RATE_LIMITED") return this._set(AUTH.UNKNOWN, "the auth check was rate limited; sign-in state is unconfirmed");
      return this._set(AUTH.READY, "a protected procedure answered for this session");
    }
    async establish(opts = {}) {
      await this.waitForRuntime(opts);
      return this.probe();
    }
    refuse(detail = null) {
      return this._set(AUTH.SIGNED_OUT, detail ? String(detail).slice(0, 200) : "the game refused a protected procedure for this session");
    }
    assert(path) {
      if (!isProtected(path)) return;
      if (this.state !== AUTH.READY) throw new AuthUnavailable(this.state, path);
    }
    allows(path) {
      return !isProtected(path) || this.state === AUTH.READY;
    }
    describe() {
      return { state: this.state, detail: this.detail, at: this.at };
    }
  };

  var DoubleIndexedKV = class {
    constructor() {
      this.keyToValue =  new Map();
      this.valueToKey =  new Map();
    }
    set(key, value) {
      this.keyToValue.set(key, value);
      this.valueToKey.set(value, key);
    }
    getByKey(key) {
      return this.keyToValue.get(key);
    }
    getByValue(value) {
      return this.valueToKey.get(value);
    }
    clear() {
      this.keyToValue.clear();
      this.valueToKey.clear();
    }
  };

  var Registry = class {
    constructor(generateIdentifier) {
      this.generateIdentifier = generateIdentifier;
      this.kv = new DoubleIndexedKV();
    }
    register(value, identifier) {
      if (this.kv.getByValue(value)) {
        return;
      }
      if (!identifier) {
        identifier = this.generateIdentifier(value);
      }
      this.kv.set(identifier, value);
    }
    clear() {
      this.kv.clear();
    }
    getIdentifier(value) {
      return this.kv.getByValue(value);
    }
    getValue(identifier) {
      return this.kv.getByKey(identifier);
    }
  };

  var ClassRegistry = class extends Registry {
    constructor() {
      super((c) => c.name);
      this.classToAllowedProps =  new Map();
    }
    register(value, options) {
      if (typeof options === "object") {
        if (options.allowProps) {
          this.classToAllowedProps.set(value, options.allowProps);
        }
        super.register(value, options.identifier);
      } else {
        super.register(value, options);
      }
    }
    getAllowedProps(value) {
      return this.classToAllowedProps.get(value);
    }
  };

  function valuesOfObj(record) {
    if ("values" in Object) {
      return Object.values(record);
    }
    const values = [];
    for (const key in record) {
      if (record.hasOwnProperty(key)) {
        values.push(record[key]);
      }
    }
    return values;
  }
  function find(record, predicate) {
    const values = valuesOfObj(record);
    if ("find" in values) {
      return values.find(predicate);
    }
    const valuesNotNever = values;
    for (let i = 0; i < valuesNotNever.length; i++) {
      const value = valuesNotNever[i];
      if (predicate(value)) {
        return value;
      }
    }
    return void 0;
  }
  function forEach(record, run) {
    Object.entries(record).forEach(([key, value]) => run(value, key));
  }
  function includes(arr, value) {
    return arr.indexOf(value) !== -1;
  }
  function findArr(record, predicate) {
    for (let i = 0; i < record.length; i++) {
      const value = record[i];
      if (predicate(value)) {
        return value;
      }
    }
    return void 0;
  }

  var CustomTransformerRegistry = class {
    constructor() {
      this.transfomers = {};
    }
    register(transformer) {
      this.transfomers[transformer.name] = transformer;
    }
    findApplicable(v) {
      return find(this.transfomers, (transformer) => transformer.isApplicable(v));
    }
    findByName(name) {
      return this.transfomers[name];
    }
  };

  var getType = (payload) => Object.prototype.toString.call(payload).slice(8, -1);
  var isUndefined = (payload) => typeof payload === "undefined";
  var isNull = (payload) => payload === null;
  var isPlainObject = (payload) => {
    if (typeof payload !== "object" || payload === null)
      return false;
    if (payload === Object.prototype)
      return false;
    if (Object.getPrototypeOf(payload) === null)
      return true;
    return Object.getPrototypeOf(payload) === Object.prototype;
  };
  var isEmptyObject = (payload) => isPlainObject(payload) && Object.keys(payload).length === 0;
  var isArray = (payload) => Array.isArray(payload);
  var isString = (payload) => typeof payload === "string";
  var isNumber = (payload) => typeof payload === "number" && !isNaN(payload);
  var isBoolean = (payload) => typeof payload === "boolean";
  var isRegExp = (payload) => payload instanceof RegExp;
  var isMap = (payload) => payload instanceof Map;
  var isSet = (payload) => payload instanceof Set;
  var isSymbol = (payload) => getType(payload) === "Symbol";
  var isDate = (payload) => payload instanceof Date && !isNaN(payload.valueOf());
  var isError = (payload) => payload instanceof Error;
  var isNaNValue = (payload) => typeof payload === "number" && isNaN(payload);
  var isPrimitive = (payload) => isBoolean(payload) || isNull(payload) || isUndefined(payload) || isNumber(payload) || isString(payload) || isSymbol(payload);
  var isBigint = (payload) => typeof payload === "bigint";
  var isInfinite = (payload) => payload === Infinity || payload === -Infinity;
  var isTypedArray = (payload) => ArrayBuffer.isView(payload) && !(payload instanceof DataView);
  var isURL = (payload) => payload instanceof URL;

  var escapeKey = (key) => key.replace(/\\/g, "\\\\").replace(/\./g, "\\.");
  var stringifyPath = (path) => path.map(String).map(escapeKey).join(".");
  var parsePath = (string, legacyPaths) => {
    const result = [];
    let segment = "";
    for (let i = 0; i < string.length; i++) {
      let char = string.charAt(i);
      if (!legacyPaths && char === "\\") {
        const escaped = string.charAt(i + 1);
        if (escaped === "\\") {
          segment += "\\";
          i++;
          continue;
        } else if (escaped !== ".") {
          throw Error("invalid path");
        }
      }
      const isEscapedDot = char === "\\" && string.charAt(i + 1) === ".";
      if (isEscapedDot) {
        segment += ".";
        i++;
        continue;
      }
      const isEndOfSegment = char === ".";
      if (isEndOfSegment) {
        result.push(segment);
        segment = "";
        continue;
      }
      segment += char;
    }
    const lastSegment = segment;
    result.push(lastSegment);
    return result;
  };

  function simpleTransformation(isApplicable, annotation, transform, untransform) {
    return {
      isApplicable,
      annotation,
      transform,
      untransform
    };
  }
  var simpleRules = [
    simpleTransformation(isUndefined, "undefined", () => null, () => void 0),
    simpleTransformation(isBigint, "bigint", (v) => v.toString(), (v) => {
      if (typeof BigInt !== "undefined") {
        return BigInt(v);
      }
      console.error("Please add a BigInt polyfill.");
      return v;
    }),
    simpleTransformation(isDate, "Date", (v) => v.toISOString(), (v) => new Date(v)),
    simpleTransformation(isError, "Error", (v, superJson) => {
      const baseError = {
        name: v.name,
        message: v.message
      };
      if ("cause" in v) {
        baseError.cause = v.cause;
      }
      superJson.allowedErrorProps.forEach((prop) => {
        baseError[prop] = v[prop];
      });
      return baseError;
    }, (v, superJson) => {
      const e = new Error(v.message, { cause: v.cause });
      e.name = v.name;
      e.stack = v.stack;
      superJson.allowedErrorProps.forEach((prop) => {
        e[prop] = v[prop];
      });
      return e;
    }),
    simpleTransformation(isRegExp, "regexp", (v) => "" + v, (regex) => {
      const body = regex.slice(1, regex.lastIndexOf("/"));
      const flags = regex.slice(regex.lastIndexOf("/") + 1);
      return new RegExp(body, flags);
    }),
    simpleTransformation(
      isSet,
      "set",
      (v) => [...v.values()],
      (v) => new Set(v)
    ),
    simpleTransformation(isMap, "map", (v) => [...v.entries()], (v) => new Map(v)),
    simpleTransformation((v) => isNaNValue(v) || isInfinite(v), "number", (v) => {
      if (isNaNValue(v)) {
        return "NaN";
      }
      if (v > 0) {
        return "Infinity";
      } else {
        return "-Infinity";
      }
    }, Number),
    simpleTransformation((v) => v === 0 && 1 / v === -Infinity, "number", () => {
      return "-0";
    }, Number),
    simpleTransformation(isURL, "URL", (v) => v.toString(), (v) => new URL(v))
  ];
  function compositeTransformation(isApplicable, annotation, transform, untransform) {
    return {
      isApplicable,
      annotation,
      transform,
      untransform
    };
  }
  var symbolRule = compositeTransformation((s, superJson) => {
    if (isSymbol(s)) {
      const isRegistered = !!superJson.symbolRegistry.getIdentifier(s);
      return isRegistered;
    }
    return false;
  }, (s, superJson) => {
    const identifier = superJson.symbolRegistry.getIdentifier(s);
    return ["symbol", identifier];
  }, (v) => v.description, (_, a, superJson) => {
    const value = superJson.symbolRegistry.getValue(a[1]);
    if (!value) {
      throw new Error("Trying to deserialize unknown symbol");
    }
    return value;
  });
  var constructorToName = [
    Int8Array,
    Uint8Array,
    Int16Array,
    Uint16Array,
    Int32Array,
    Uint32Array,
    Float32Array,
    Float64Array,
    Uint8ClampedArray
  ].reduce((obj3, ctor) => {
    obj3[ctor.name] = ctor;
    return obj3;
  }, {});
  var typedArrayRule = compositeTransformation(isTypedArray, (v) => ["typed-array", v.constructor.name], (v) => [...v], (v, a) => {
    const ctor = constructorToName[a[1]];
    if (!ctor) {
      throw new Error("Trying to deserialize unknown typed array");
    }
    return new ctor(v);
  });
  function isInstanceOfRegisteredClass(potentialClass, superJson) {
    if (potentialClass?.constructor) {
      const isRegistered = !!superJson.classRegistry.getIdentifier(potentialClass.constructor);
      return isRegistered;
    }
    return false;
  }
  var classRule = compositeTransformation(isInstanceOfRegisteredClass, (clazz, superJson) => {
    const identifier = superJson.classRegistry.getIdentifier(clazz.constructor);
    return ["class", identifier];
  }, (clazz, superJson) => {
    const allowedProps = superJson.classRegistry.getAllowedProps(clazz.constructor);
    if (!allowedProps) {
      return { ...clazz };
    }
    const result = {};
    allowedProps.forEach((prop) => {
      result[prop] = clazz[prop];
    });
    return result;
  }, (v, a, superJson) => {
    const clazz = superJson.classRegistry.getValue(a[1]);
    if (!clazz) {
      throw new Error(`Trying to deserialize unknown class '${a[1]}' - check https://github.com/blitz-js/superjson/issues/116#issuecomment-773996564`);
    }
    return Object.assign(Object.create(clazz.prototype), v);
  });
  var customRule = compositeTransformation((value, superJson) => {
    return !!superJson.customTransformerRegistry.findApplicable(value);
  }, (value, superJson) => {
    const transformer = superJson.customTransformerRegistry.findApplicable(value);
    return ["custom", transformer.name];
  }, (value, superJson) => {
    const transformer = superJson.customTransformerRegistry.findApplicable(value);
    return transformer.serialize(value);
  }, (v, a, superJson) => {
    const transformer = superJson.customTransformerRegistry.findByName(a[1]);
    if (!transformer) {
      throw new Error("Trying to deserialize unknown custom value");
    }
    return transformer.deserialize(v);
  });
  var compositeRules = [classRule, symbolRule, customRule, typedArrayRule];
  var transformValue = (value, superJson) => {
    const applicableCompositeRule = findArr(compositeRules, (rule) => rule.isApplicable(value, superJson));
    if (applicableCompositeRule) {
      return {
        value: applicableCompositeRule.transform(value, superJson),
        type: applicableCompositeRule.annotation(value, superJson)
      };
    }
    const applicableSimpleRule = findArr(simpleRules, (rule) => rule.isApplicable(value, superJson));
    if (applicableSimpleRule) {
      return {
        value: applicableSimpleRule.transform(value, superJson),
        type: applicableSimpleRule.annotation
      };
    }
    return void 0;
  };
  var simpleRulesByAnnotation = {};
  simpleRules.forEach((rule) => {
    simpleRulesByAnnotation[rule.annotation] = rule;
  });
  var untransformValue = (json, type, superJson) => {
    if (isArray(type)) {
      switch (type[0]) {
        case "symbol":
          return symbolRule.untransform(json, type, superJson);
        case "class":
          return classRule.untransform(json, type, superJson);
        case "custom":
          return customRule.untransform(json, type, superJson);
        case "typed-array":
          return typedArrayRule.untransform(json, type, superJson);
        default:
          throw new Error("Unknown transformation: " + type);
      }
    } else {
      const transformation = simpleRulesByAnnotation[type];
      if (!transformation) {
        throw new Error("Unknown transformation: " + type);
      }
      return transformation.untransform(json, superJson);
    }
  };

  var getNthKey = (value, n) => {
    if (n > value.size)
      throw new Error("index out of bounds");
    const keys = value.keys();
    while (n > 0) {
      keys.next();
      n--;
    }
    return keys.next().value;
  };
  function validatePath(path) {
    if (includes(path, "__proto__")) {
      throw new Error("__proto__ is not allowed as a property");
    }
    if (includes(path, "prototype")) {
      throw new Error("prototype is not allowed as a property");
    }
    if (includes(path, "constructor")) {
      throw new Error("constructor is not allowed as a property");
    }
  }
  var getDeep = (object2, path) => {
    validatePath(path);
    for (let i = 0; i < path.length; i++) {
      const key = path[i];
      if (isSet(object2)) {
        object2 = getNthKey(object2, +key);
      } else if (isMap(object2)) {
        const row = +key;
        const type = +path[++i] === 0 ? "key" : "value";
        const keyOfRow = getNthKey(object2, row);
        switch (type) {
          case "key":
            object2 = keyOfRow;
            break;
          case "value":
            object2 = object2.get(keyOfRow);
            break;
        }
      } else {
        object2 = object2[key];
      }
    }
    return object2;
  };
  var setDeep = (object2, path, mapper) => {
    validatePath(path);
    if (path.length === 0) {
      return mapper(object2);
    }
    let parent = object2;
    for (let i = 0; i < path.length - 1; i++) {
      const key = path[i];
      if (isArray(parent)) {
        const index = +key;
        parent = parent[index];
      } else if (isPlainObject(parent)) {
        parent = parent[key];
      } else if (isSet(parent)) {
        const row = +key;
        parent = getNthKey(parent, row);
      } else if (isMap(parent)) {
        const isEnd = i === path.length - 2;
        if (isEnd) {
          break;
        }
        const row = +key;
        const type = +path[++i] === 0 ? "key" : "value";
        const keyOfRow = getNthKey(parent, row);
        switch (type) {
          case "key":
            parent = keyOfRow;
            break;
          case "value":
            parent = parent.get(keyOfRow);
            break;
        }
      }
    }
    const lastKey = path[path.length - 1];
    if (isArray(parent)) {
      parent[+lastKey] = mapper(parent[+lastKey]);
    } else if (isPlainObject(parent)) {
      parent[lastKey] = mapper(parent[lastKey]);
    }
    if (isSet(parent)) {
      const oldValue = getNthKey(parent, +lastKey);
      const newValue = mapper(oldValue);
      if (oldValue !== newValue) {
        parent.delete(oldValue);
        parent.add(newValue);
      }
    }
    if (isMap(parent)) {
      const row = +path[path.length - 2];
      const keyToRow = getNthKey(parent, row);
      const type = +lastKey === 0 ? "key" : "value";
      switch (type) {
        case "key": {
          const newKey = mapper(keyToRow);
          parent.set(newKey, parent.get(keyToRow));
          if (newKey !== keyToRow) {
            parent.delete(keyToRow);
          }
          break;
        }
        case "value": {
          parent.set(keyToRow, mapper(parent.get(keyToRow)));
          break;
        }
      }
    }
    return object2;
  };

  var enableLegacyPaths = (version) => version < 1;
  function traverse(tree, walker2, version, origin = []) {
    if (!tree) {
      return;
    }
    const legacyPaths = enableLegacyPaths(version);
    if (!isArray(tree)) {
      forEach(tree, (subtree, key) => traverse(subtree, walker2, version, [
        ...origin,
        ...parsePath(key, legacyPaths)
      ]));
      return;
    }
    const [nodeValue, children] = tree;
    if (children) {
      forEach(children, (child, key) => {
        traverse(child, walker2, version, [
          ...origin,
          ...parsePath(key, legacyPaths)
        ]);
      });
    }
    walker2(nodeValue, origin);
  }
  function applyValueAnnotations(plain, annotations, version, superJson) {
    traverse(annotations, (type, path) => {
      plain = setDeep(plain, path, (v) => untransformValue(v, type, superJson));
    }, version);
    return plain;
  }
  function applyReferentialEqualityAnnotations(plain, annotations, version) {
    const legacyPaths = enableLegacyPaths(version);
    function apply(identicalPaths, path) {
      const object2 = getDeep(plain, parsePath(path, legacyPaths));
      identicalPaths.map((path2) => parsePath(path2, legacyPaths)).forEach((identicalObjectPath) => {
        plain = setDeep(plain, identicalObjectPath, () => object2);
      });
    }
    if (isArray(annotations)) {
      const [root, other] = annotations;
      root.forEach((identicalPath) => {
        plain = setDeep(plain, parsePath(identicalPath, legacyPaths), () => plain);
      });
      if (other) {
        forEach(other, apply);
      }
    } else {
      forEach(annotations, apply);
    }
    return plain;
  }
  var isDeep = (object2, superJson) => isPlainObject(object2) || isArray(object2) || isMap(object2) || isSet(object2) || isError(object2) || isInstanceOfRegisteredClass(object2, superJson);
  function addIdentity(object2, path, identities) {
    const existingSet = identities.get(object2);
    if (existingSet) {
      existingSet.push(path);
    } else {
      identities.set(object2, [path]);
    }
  }
  function generateReferentialEqualityAnnotations(identitites, dedupe) {
    const result = {};
    let rootEqualityPaths = void 0;
    identitites.forEach((paths) => {
      if (paths.length <= 1) {
        return;
      }
      if (!dedupe) {
        paths = paths.map((path) => path.map(String)).sort((a, b) => a.length - b.length);
      }
      const [representativePath, ...identicalPaths] = paths;
      if (representativePath.length === 0) {
        rootEqualityPaths = identicalPaths.map(stringifyPath);
      } else {
        result[stringifyPath(representativePath)] = identicalPaths.map(stringifyPath);
      }
    });
    if (rootEqualityPaths) {
      if (isEmptyObject(result)) {
        return [rootEqualityPaths];
      } else {
        return [rootEqualityPaths, result];
      }
    } else {
      return isEmptyObject(result) ? void 0 : result;
    }
  }
  var walker = (object2, identities, superJson, dedupe, path = [], objectsInThisPath = [], seenObjects =  new Map()) => {
    const primitive = isPrimitive(object2);
    if (!primitive) {
      addIdentity(object2, path, identities);
      const seen = seenObjects.get(object2);
      if (seen) {
        return dedupe ? {
          transformedValue: null
        } : seen;
      }
    }
    if (!isDeep(object2, superJson)) {
      const transformed2 = transformValue(object2, superJson);
      const result2 = transformed2 ? {
        transformedValue: transformed2.value,
        annotations: [transformed2.type]
      } : {
        transformedValue: object2
      };
      if (!primitive) {
        seenObjects.set(object2, result2);
      }
      return result2;
    }
    if (includes(objectsInThisPath, object2)) {
      return {
        transformedValue: null
      };
    }
    const transformationResult = transformValue(object2, superJson);
    const transformed = transformationResult?.value ?? object2;
    const transformedValue = isArray(transformed) ? [] : {};
    const innerAnnotations = {};
    forEach(transformed, (value, index) => {
      if (index === "__proto__" || index === "constructor" || index === "prototype") {
        throw new Error(`Detected property ${index}. This is a prototype pollution risk, please remove it from your object.`);
      }
      const recursiveResult = walker(value, identities, superJson, dedupe, [...path, index], [...objectsInThisPath, object2], seenObjects);
      transformedValue[index] = recursiveResult.transformedValue;
      if (isArray(recursiveResult.annotations)) {
        innerAnnotations[escapeKey(index)] = recursiveResult.annotations;
      } else if (isPlainObject(recursiveResult.annotations)) {
        forEach(recursiveResult.annotations, (tree, key) => {
          innerAnnotations[escapeKey(index) + "." + key] = tree;
        });
      }
    });
    const result = isEmptyObject(innerAnnotations) ? {
      transformedValue,
      annotations: !!transformationResult ? [transformationResult.type] : void 0
    } : {
      transformedValue,
      annotations: !!transformationResult ? [transformationResult.type, innerAnnotations] : innerAnnotations
    };
    if (!primitive) {
      seenObjects.set(object2, result);
    }
    return result;
  };

  function assignProp(carry, key, newVal, originalObject) {
    if (Object.prototype.propertyIsEnumerable.call(originalObject, key)) {
      carry[key] = newVal;
      return;
    }
    Object.defineProperty(carry, key, {
      value: newVal,
      enumerable: false,
      writable: true,
      configurable: true
    });
  }
  function isPlainObject2(value) {
    return Object.getPrototypeOf(value) === Object.prototype && Object.prototype.toString.call(value) === "[object Object]";
  }
  function cloneRef(value, clones, sources, dests) {
    if (typeof value !== "object" || value === null)
      return value;
    const array = Array.isArray(value);
    if (!array && !isPlainObject2(value))
      return value;
    const existing = clones.get(value);
    if (existing !== void 0)
      return existing;
    const clone = array ? new Array(value.length) : {};
    clones.set(value, clone);
    sources.push(value);
    dests.push(clone);
    return clone;
  }
  function copy(target, options = {}) {
    if (typeof target !== "object" || target === null)
      return target;
    const clones =  new Map();
    const sources = [];
    const dests = [];
    const result = cloneRef(target, clones, sources, dests);
    const onlyProps = Array.isArray(options.props) ? options.props : void 0;
    const nonenumerable = options.nonenumerable === true;
    while (sources.length) {
      const source = sources.pop();
      const dest = dests.pop();
      if (Array.isArray(source)) {
        for (let i = 0; i < source.length; i++) {
          if (i in source)
            dest[i] = cloneRef(source[i], clones, sources, dests);
        }
        continue;
      }
      if (nonenumerable) {
        for (const key of Object.getOwnPropertyNames(source)) {
          if (key === "__proto__")
            continue;
          if (onlyProps && !onlyProps.includes(key))
            continue;
          const newVal = cloneRef(source[key], clones, sources, dests);
          assignProp(dest, key, newVal, source);
        }
      } else {
        for (const key in source) {
          if (!Object.prototype.hasOwnProperty.call(source, key))
            continue;
          if (key === "__proto__")
            continue;
          if (onlyProps && !onlyProps.includes(key))
            continue;
          dest[key] = cloneRef(source[key], clones, sources, dests);
        }
      }
      for (const key of Object.getOwnPropertySymbols(source)) {
        if (onlyProps && !onlyProps.includes(key))
          continue;
        if (!nonenumerable && !Object.prototype.propertyIsEnumerable.call(source, key))
          continue;
        const newVal = cloneRef(source[key], clones, sources, dests);
        assignProp(dest, key, newVal, source);
      }
    }
    return result;
  }

  var SuperJSON = class {
    constructor({ dedupe = false } = {}) {
      this.classRegistry = new ClassRegistry();
      this.symbolRegistry = new Registry((s) => s.description ?? "");
      this.customTransformerRegistry = new CustomTransformerRegistry();
      this.allowedErrorProps = [];
      this.dedupe = dedupe;
    }
    serialize(object2) {
      const identities =  new Map();
      const output = walker(object2, identities, this, this.dedupe);
      const res = {
        json: output.transformedValue
      };
      if (output.annotations) {
        res.meta = {
          ...res.meta,
          values: output.annotations
        };
      }
      const equalityAnnotations = generateReferentialEqualityAnnotations(identities, this.dedupe);
      if (equalityAnnotations) {
        res.meta = {
          ...res.meta,
          referentialEqualities: equalityAnnotations
        };
      }
      if (res.meta)
        res.meta.v = 1;
      return res;
    }
    deserialize(payload, options) {
      const { json, meta } = payload;
      let result = options?.inPlace ? json : copy(json);
      if (meta?.values) {
        result = applyValueAnnotations(result, meta.values, meta.v ?? 0, this);
      }
      if (meta?.referentialEqualities) {
        result = applyReferentialEqualityAnnotations(result, meta.referentialEqualities, meta.v ?? 0);
      }
      return result;
    }
    stringify(object2) {
      return JSON.stringify(this.serialize(object2));
    }
    parse(string) {
      return this.deserialize(JSON.parse(string), { inPlace: true });
    }
    registerClass(v, options) {
      this.classRegistry.register(v, options);
    }
    registerSymbol(v, identifier) {
      this.symbolRegistry.register(v, identifier);
    }
    registerCustom(transformer, name) {
      this.customTransformerRegistry.register({
        name,
        ...transformer
      });
    }
    allowErrorProps(...props) {
      this.allowedErrorProps.push(...props);
    }
  };
  SuperJSON.defaultInstance = new SuperJSON();
  SuperJSON.serialize = SuperJSON.defaultInstance.serialize.bind(SuperJSON.defaultInstance);
  SuperJSON.deserialize = SuperJSON.defaultInstance.deserialize.bind(SuperJSON.defaultInstance);
  SuperJSON.stringify = SuperJSON.defaultInstance.stringify.bind(SuperJSON.defaultInstance);
  SuperJSON.parse = SuperJSON.defaultInstance.parse.bind(SuperJSON.defaultInstance);
  SuperJSON.registerClass = SuperJSON.defaultInstance.registerClass.bind(SuperJSON.defaultInstance);
  SuperJSON.registerSymbol = SuperJSON.defaultInstance.registerSymbol.bind(SuperJSON.defaultInstance);
  SuperJSON.registerCustom = SuperJSON.defaultInstance.registerCustom.bind(SuperJSON.defaultInstance);
  SuperJSON.allowErrorProps = SuperJSON.defaultInstance.allowErrorProps.bind(SuperJSON.defaultInstance);
  var dist_default = SuperJSON;
  var serialize = SuperJSON.serialize;
  var deserialize = SuperJSON.deserialize;
  var stringify = SuperJSON.stringify;
  var parse = SuperJSON.parse;
  var registerClass = SuperJSON.registerClass;
  var registerCustom = SuperJSON.registerCustom;
  var registerSymbol = SuperJSON.registerSymbol;
  var allowErrorProps = SuperJSON.allowErrorProps;

  var ENDPOINT = "/api/trpc";
  var TransportError = class extends Error {
    constructor(message, info = {}) {
      super(message);
      this.name = "TransportError";
      Object.assign(this, info);
    }
  };
  function encodeInput(input) {
    const { json, meta } = dist_default.serialize(input);
    return meta ? { json, meta } : { json };
  }
  function buildRequest(calls, kind, { endpoint = ENDPOINT } = {}) {
    if (!Array.isArray(calls) || calls.length === 0) throw new TransportError("empty batch");
    const paths = calls.map((c) => c.path).join(",");
    const envelope = {};
    calls.forEach((c, i) => {
      envelope[String(i)] = encodeInput(c.input);
    });
    if (kind === "query") {
      const input = encodeURIComponent(JSON.stringify(envelope));
      return { method: "GET", url: `${endpoint}/${paths}?batch=1&input=${input}`, headers: {}, body: null };
    }
    if (kind === "mutation") {
      return {
        method: "POST",
        url: `${endpoint}/${paths}?batch=1`,
        headers: { "content-type": "application/json" },
        body: JSON.stringify(envelope)
      };
    }
    throw new TransportError("unknown kind: " + kind);
  }
  function decodeResponse(status, text, expectedCount, { mutation = false } = {}) {
    let body;
    try {
      body = JSON.parse(text);
    } catch (e) {
      throw new TransportError(`response is not JSON${status ? ` (HTTP ${status})` : ""}`, { httpStatus: status, snippet: String(text).slice(0, 200) });
    }
    if (!Array.isArray(body)) {
      if (isTrpcErrorBody(body)) {
        const el = decodeElement(body, 0, status);
        el.error.requestLevel = true;
        return Array.from({ length: expectedCount ?? 1 }, () => el);
      }
      throw new TransportError("response is not a batch array", { httpStatus: status, snippet: String(text).slice(0, 200) });
    }
    if (expectedCount != null && body.length !== expectedCount) {
      throw new TransportError(`batch length mismatch: expected ${expectedCount}, got ${body.length}`, { httpStatus: status });
    }
    return body.map((el, i) => {
      try {
        return decodeElement(el, i, status);
      } catch (e) {
        if (mutation) throw new TransportError(`mutation response element ${i} is not a tRPC result or error: ${e.message}`, { httpStatus: status, index: i, element: el });
        return { ok: false, error: { code: "MALFORMED_ELEMENT", httpStatus: status, message: e.message, path: null, zodError: null, raw: el } };
      }
    });
  }
  function isTrpcErrorBody(body) {
    const j = body && typeof body === "object" && body.error && typeof body.error === "object" ? body.error.json : null;
    return !!(j && typeof j === "object" && typeof j.message === "string" && typeof j.code === "number" && j.data && typeof j.data === "object" && typeof j.data.code === "string");
  }
  function decodeElement(el, i, status) {
    if (el && el.result && el.result.data !== void 0) {
      const { json, meta } = el.result.data;
      return { ok: true, data: dist_default.deserialize({ json, meta }) };
    }
    if (el && el.error) {
      if (!isTrpcErrorBody(el)) {
        throw new TransportError(`batch element ${i} has a malformed tRPC error`, { httpStatus: status, element: el });
      }
      const err = el.error.json !== void 0 ? dist_default.deserialize({ json: el.error.json, meta: el.error.meta }) : el.error;
      const data = err && err.data || {};
      return {
        ok: false,
        error: {
          code: data.code ?? "UNKNOWN",
          httpStatus: data.httpStatus ?? null,
          message: (err && err.message) ?? "",
          path: data.path ?? null,
          zodError: Array.isArray(data.zodError) ? data.zodError : null,
          raw: err
        }
      };
    }
    throw new TransportError(`batch element ${i} is neither result nor error`, { httpStatus: status, element: el });
  }

  var NetworkError = class extends Error {
    constructor(cause, info = {}) {
      const name = cause && cause.name ? cause.name + ": " : "";
      super("network: " + name + (cause && cause.message ? cause.message : String(cause)));
      this.name = "NetworkError";
      this.causeName = cause && cause.name ? String(cause.name) : null;
      Object.assign(this, { phase: "connect", httpStatus: null, received: false, results: null }, info);
    }
  };
  var TrpcClient = class {
    constructor(session, { maxBatch = 20, maxUrlLength = 8e3, onExchange = null, endpoint } = {}) {
      if (!(session instanceof Session)) throw new TransportError("TrpcClient needs a Session");
      if (!Number.isInteger(maxBatch) || maxBatch < 1) throw new TransportError("maxBatch must be an integer >= 1");
      if (!Number.isInteger(maxUrlLength) || maxUrlLength < 64) throw new TransportError("maxUrlLength must be an integer >= 64");
      this.session = session;
      this.maxBatch = maxBatch;
      this.maxUrlLength = maxUrlLength;
      this.onExchange = onExchange;
      this.endpoint = endpoint;
    }
    async call(path, input) {
      const [r] = await this.batch([{ path, input }]);
      return r;
    }
    async batch(calls) {
      if (!calls.length) return [];
      const kinds = new Set(calls.map((c) => procedure(c.path).kind));
      if (kinds.size !== 1) throw new TransportError("a batch must be all queries or all mutations");
      const kind = [...kinds][0];
      const out = new Array(calls.length);
      for (const chunk of this._chunks(calls, kind)) {
        let results;
        try {
          results = await this._send(chunk.map((c) => c.call), kind);
        } catch (e) {
          e.results = out.slice();
          e.failedIndices = chunk.map((c) => c.index);
          throw e;
        }
        chunk.forEach((c, j) => {
          out[c.index] = results[j];
        });
      }
      return out;
    }
    *_chunks(calls, kind) {
      const indexed = calls.map((call, index) => ({ call, index }));
      let cur = [];
      for (const c of indexed) {
        cur.push(c);
        const tooMany = cur.length > this.maxBatch;
        const tooLong = kind === "query" && buildRequest(cur.map((x) => x.call), kind, { endpoint: this.endpoint }).url.length > this.maxUrlLength;
        if (tooLong && cur.length === 1) throw new TransportError(`single call to ${c.call.path} exceeds maxUrlLength ${this.maxUrlLength}`, { paths: [c.call.path], sent: false });
        if ((tooMany || tooLong) && cur.length > 1) {
          cur.pop();
          yield cur;
          cur = [c];
        }
      }
      if (cur.length) yield cur;
    }
    async _send(calls, kind) {
      const req = buildRequest(calls, kind, { endpoint: this.endpoint });
      const paths = calls.map((c) => c.path);
      let res;
      try {
        res = await this.session.fetch(req.url, { method: req.method, headers: req.headers, body: req.body });
      } catch (e) {
        this._observe({ kind, paths, status: null, error: String(e && e.message) });
        if (e instanceof SessionRefused) throw new TransportError("not sent: " + e.message, { paths, kind, sent: false });
        throw new NetworkError(e, { paths, kind, phase: "connect" });
      }
      let text;
      try {
        text = await res.text();
      } catch (e) {
        this._observe({ kind, paths, status: res.status, error: "body: " + String(e && e.message) });
        throw new NetworkError(e, { paths, kind, phase: "body", httpStatus: res.status, received: true });
      }
      let decoded;
      try {
        decoded = decodeResponse(res.status, text, calls.length, { mutation: kind === "mutation" });
      } catch (e) {
        const ct = res.headers && res.headers.get ? res.headers.get("content-type") : null;
        Object.assign(e, {
          paths,
          kind,
          received: true,
          httpStatus: res.status,
          redirected: !!res.redirected,
          url: res.url ?? null,
          contentType: ct,
          looksLikeLogin: !!(ct && /text\/html/i.test(ct))
        });
        this._observe({ kind, paths, status: res.status, error: e.message, contentType: ct, redirected: !!res.redirected });
        throw e;
      }
      this._observe({ kind, paths, status: res.status, outcomes: decoded.map((d) => d.ok ? "ok" : d.error.code) });
      return decoded;
    }
    _observe(rec) {
      if (this.onExchange) {
        try {
          this.onExchange(rec);
        } catch {
        }
      }
    }
  };

  var UT_VERSION = "7.7.4";
  var SLUGS = Object.freeze({
    imageUploader: { mime: "image", maxBytes: 512 * 1024 },
    conceptArtFrameUploader: { mime: "image", maxBytes: 256 * 1024 },
    modelUploader: { mime: "model/gltf-binary", maxBytes: 256 * 1024 },
    tavernUploader: { mime: "image", maxBytes: 64 * 1024 }
  });
  var UploadError = class extends Error {
    constructor(message, info = {}) {
      super(message);
      this.name = "UploadError";
      Object.assign(this, info);
    }
  };
  var TRANSIENT = /unable to validate/i;
  var RETRY_DELAYS_MS = Object.freeze([1e4, 3e4, 6e4]);
  var MIN_GAP_MS = 3e3;
  var realSleep = (ms) => new Promise((r) => setTimeout(r, ms));
  var Uploader = class {
    constructor({ session, fetchImpl, slug = "imageUploader", sleep = realSleep, clock = () => Date.now(), retryDelays = RETRY_DELAYS_MS, minGapMs = MIN_GAP_MS }) {
      if (!SLUGS[slug]) throw new UploadError("unknown slug " + slug);
      this.session = session;
      this.fetchImpl = fetchImpl;
      this.slug = slug;
      this.sleep = sleep;
      this.clock = clock;
      this.retryDelays = retryDelays;
      this.minGapMs = minGapMs;
      this._last = null;
    }
    ceiling() {
      return SLUGS[this.slug].maxBytes;
    }
    async upload(file, { onWait = null } = {}) {
      for (let attempt = 0; ; attempt++) {
        if (this._last != null) {
          const wait = this._last + this.minGapMs - this.clock();
          if (wait > 0) await this._wait(wait, onWait);
        }
        try {
          return await this._once(file);
        } catch (e) {
          if (!(e instanceof UploadError && e.removed && TRANSIENT.test(e.reason ?? "")) || attempt >= this.retryDelays.length) throw e;
          await this._wait(this.retryDelays[attempt], onWait);
        } finally {
          this._last = this.clock();
        }
      }
    }
    async _wait(ms, onWait) {
      while (ms > 0) {
        if (onWait) onWait();
        const step = Math.min(ms, 1e4);
        await this.sleep(step);
        ms -= step;
      }
    }
    async _once(file) {
      const max = this.ceiling();
      if (file.size > max) throw new UploadError(`${file.name ?? "file"} is ${file.size} bytes; ${this.slug} ceiling is ${max}`, { size: file.size, max });
      const meta = { name: file.name ?? "upload", size: file.size, type: file.type || "application/octet-stream", lastModified: file.lastModified ?? 0 };
      const pres = await this.session.fetch(`/api/uploadthing?actionType=upload&slug=${encodeURIComponent(this.slug)}`, {
        method: "POST",
        headers: { "content-type": "application/json", "x-uploadthing-version": UT_VERSION },
        body: JSON.stringify({ files: [meta], input: null })
      });
      const presText = await pres.text();
      if (!pres.ok) throw new UploadError(`presign ${pres.status}: ${presText.slice(0, 160)}`, { status: pres.status });
      let presigneds;
      try {
        presigneds = JSON.parse(presText);
      } catch {
        throw new UploadError("presign response is not JSON");
      }
      const p = Array.isArray(presigneds) ? presigneds[0] : null;
      if (!p || !p.url || !p.key) throw new UploadError("presign response missing url/key", { body: presText.slice(0, 160) });
      let start = 0;
      try {
        const head = await this.fetchImpl(p.url, { method: "HEAD" });
        start = parseInt(head.headers.get("x-ut-range-start") ?? "0", 10) || 0;
      } catch {
        start = 0;
      }
      const fd = new FormData();
      fd.append("file", start > 0 ? file.slice(start) : file, meta.name);
      const put = await this.fetchImpl(p.url, { method: "PUT", headers: { "x-uploadthing-version": UT_VERSION }, body: fd });
      const putText = await put.text();
      if (!put.ok) throw new UploadError(`upload PUT ${put.status}: ${putText.slice(0, 160)}`, { status: put.status });
      let done;
      try {
        done = JSON.parse(putText);
      } catch {
        throw new UploadError("upload response is not JSON");
      }
      if (!done || typeof done.ufsUrl !== "string") throw new UploadError("upload response missing ufsUrl", { body: putText.slice(0, 160) });
      const verdict = done.serverData && typeof done.serverData === "object" ? done.serverData : null;
      if (verdict && (verdict.error || verdict.fileUrl === "")) {
        const reason = String(verdict.error || "the game removed the upload");
        throw new UploadError(`the game removed ${meta.name} after upload: ${reason}`, { removed: true, reason });
      }
      const url2 = verdict && typeof verdict.fileUrl === "string" && /^https:\/\//.test(verdict.fileUrl) ? verdict.fileUrl : done.ufsUrl;
      return { url: url2, ufsUrl: done.ufsUrl, key: p.key, fileHash: done.fileHash ?? null };
    }
  };

  function browserImageProbe(win, { timeoutMs = 15e3, confirmDelayMs = 1500 } = {}) {
    const seen =  new Map();
    const load = (src) => new Promise((resolve) => {
      const img = new win.Image();
      const done = (v) => {
        win.clearTimeout(timer);
        img.onload = img.onerror = null;
        resolve(v);
      };
      const timer = win.setTimeout(() => done(null), timeoutMs);
      img.onload = () => done(img.naturalWidth > 0);
      img.onerror = () => done(false);
      img.src = src;
    });
    const offline = () => win.navigator && win.navigator.onLine === false;
    return (url2) => {
      if (typeof url2 !== "string" || !/^https:\/\//.test(url2)) return Promise.resolve(false);
      if (seen.has(url2)) return seen.get(url2);
      const answer = (async () => {
        if (offline()) return null;
        const first = await load(url2);
        if (first !== false) return first;
        await new Promise((r) => win.setTimeout(r, confirmDelayMs));
        if (offline()) return null;
        return load(`${url2}${url2.includes("?") ? "&" : "?"}forge-probe=${Date.now()}`);
      })();
      seen.set(url2, answer.then((v) => {
        if (v === null) seen.delete(url2);
        return v;
      }));
      return seen.get(url2);
    };
  }

  var SENDLOG_KEY = "tnr_forge_sendlog_v1";
  var SERVER_LIMIT = 60;
  var SERVER_WINDOW_MS = 6e4;
  var DEFAULT_MARGIN = 0.5;
  var RateLimited = class extends Error {
    constructor({ path, until, index = null, message }) {
      super(message || `TOO_MANY_REQUESTS on ${path}`);
      this.name = "RateLimited";
      this.path = path;
      this.until = until;
      this.index = index;
    }
  };
  var SendLog = class {
    constructor(storage, clock) {
      this.storage = storage;
      this.clock = clock;
    }
    _load() {
      try {
        return JSON.parse(this.storage.getItem(SENDLOG_KEY) || "{}") || {};
      } catch {
        return {};
      }
    }
    _save(log) {
      this.storage.setItem(SENDLOG_KEY, JSON.stringify(log));
    }
    _prune(arr, windowMs, now) {
      return arr.filter((t) => now - t < 2 * windowMs);
    }
    inWindow(path, windowMs) {
      const now = this.clock();
      return this._prune(this._load()[path] || [], windowMs, now).filter((t) => now - t < windowMs).sort((a, b) => a - b);
    }
    recent(path, windowMs) {
      const now = this.clock();
      return this._prune(this._load()[path] || [], windowMs, now);
    }
    record(path, n, windowMs) {
      const now = this.clock();
      const log = this._load();
      const arr = this._prune(log[path] || [], windowMs, now);
      for (let i = 0; i < n; i++) arr.push(now);
      log[path] = arr;
      this._save(log);
      return arr.filter((t) => now - t < windowMs).length;
    }
    trip(path, until) {
      const log = this._load();
      log.__tripped = { path, until };
      this._save(log);
    }
    tripped() {
      const t = this._load().__tripped;
      if (!t) return null;
      if (this.clock() >= t.until) return null;
      return t;
    }
    clearTrip() {
      const log = this._load();
      delete log.__tripped;
      this._save(log);
    }
  };
  var Budget = class {
    constructor({
      storage,
      clock = () => Date.now(),
      sleep = (ms) => new Promise((r) => setTimeout(r, ms)),
      limit = SERVER_LIMIT,
      windowMs = SERVER_WINDOW_MS,
      margin = DEFAULT_MARGIN,
      limitedPaths = LIMITED_PATHS
    } = {}) {
      if (!(margin > 0 && margin <= 1)) throw new Error("margin must be in (0, 1]");
      this.log = new SendLog(storage, clock);
      this.clock = clock;
      this.sleep = sleep;
      this.limit = limit;
      this.windowMs = windowMs;
      this.margin = margin;
      this.limited = new Set(limitedPaths);
      this.waits = 0;
    }
    get allowance() {
      return Math.max(1, Math.floor(this.limit * this.margin));
    }
    isLimited(path) {
      return this.limited.has(path);
    }
    estimate(path, now = this.clock()) {
      const w = this.windowMs;
      const bucket = Math.floor(now / w);
      let prev = 0, cur = 0, strict = 0;
      for (const t of this.log.recent(path, w)) {
        const b = Math.floor(t / w);
        if (b === bucket) cur++;
        else if (b === bucket - 1) prev++;
        if (now - t < w) strict++;
      }
      const frac = now % w / w;
      const weighted = Math.floor((1 - frac) * prev) + cur;
      return { prev, cur, weighted, strict, bucketStart: bucket * w, used: Math.max(weighted, strict) };
    }
    available(path) {
      if (!this.isLimited(path)) return Infinity;
      return Math.max(0, this.allowance - this.estimate(path).used);
    }
    _wakeAt(path, n, now) {
      const w = this.windowMs, a = this.allowance;
      const est = this.estimate(path, now);
      if (est.used + n <= a) return now;
      let strictWake = now;
      const inWin = this.log.inWindow(path, w);
      if (inWin.length + n > a) strictWake = inWin[inWin.length + n - a - 1] + w;
      let weightedWake = now;
      if (est.weighted + n > a) {
        const need = a - n;
        let inThis = Infinity;
        if (est.cur <= need && est.prev > 0) {
          const f = 1 - (need - est.cur + 1) / est.prev;
          inThis = est.bucketStart + Math.ceil(f * w) + 1;
        }
        const nextStart = est.bucketStart + w;
        let inNext = nextStart + 1;
        if (est.cur > need) {
          const f = 1 - (need + 1) / est.cur;
          inNext = nextStart + Math.ceil(f * w) + 1;
        }
        weightedWake = inThis > now && inThis < nextStart ? inThis : inNext;
      }
      return Math.max(strictWake, weightedWake, now + 1);
    }
    assertNotTripped() {
      const t = this.log.tripped();
      if (t) throw new RateLimited({ path: t.path, until: t.until, message: `limiter tripped on ${t.path}; wait until ${new Date(t.until).toISOString()}` });
    }
    async acquire(path, n = 1) {
      if (!this.isLimited(path)) return;
      if (n > this.allowance) throw new Error(`cannot acquire ${n} > allowance ${this.allowance} on ${path}; chunk smaller`);
      for (let guard = 0; ; guard++) {
        this.assertNotTripped();
        const now = this.clock();
        const wakeAt = this._wakeAt(path, n, now);
        if (wakeAt <= now) break;
        if (guard >= 1e3) throw new RateLimited({ path, until: wakeAt, message: `no local budget room for ${path}; nothing sent` });
        this.waits++;
        await this.sleep(Math.max(1, wakeAt - now));
      }
      this.log.record(path, n, this.windowMs);
    }
    observe(results, paths) {
      for (let i = 0; i < results.length; i++) {
        const r = results[i];
        if (r && r.ok === false && r.error && r.error.code === "TOO_MANY_REQUESTS") {
          const path = r.error.path || paths[i];
          const until = (Math.floor(this.clock() / this.windowMs) + 2) * this.windowMs;
          this.log.trip(path, until);
          throw new RateLimited({ path, until, index: i, message: r.error.message });
        }
      }
    }
    status() {
      const now = this.clock();
      const out = {};
      for (const path of this.limited) {
        const inWin = this.log.inWindow(path, this.windowMs);
        const est = this.estimate(path, now);
        out[path] = {
          used: est.used,
          strict: inWin.length,
          weighted: est.weighted,
          allowance: this.allowance,
          serverLimit: this.limit,
          resetInMs: inWin.length ? Math.max(0, inWin[0] + this.windowMs - now) : 0,
          bucketEndsInMs: est.bucketStart + this.windowMs - now
        };
      }
      return { paths: out, tripped: this.log.tripped(), waits: this.waits, margin: this.margin };
    }
  };

  function stableStringify(v) {
    if (v && typeof v === "object" && typeof v.toJSON === "function") v = v.toJSON();
    if (v === void 0) return "null";
    if (v === null || typeof v !== "object") return JSON.stringify(v);
    if (Array.isArray(v)) return "[" + v.map(stableStringify).join(",") + "]";
    const keys = Object.keys(v).filter((k) => v[k] !== void 0).sort();
    return "{" + keys.map((k) => JSON.stringify(k) + ":" + stableStringify(v[k])).join(",") + "}";
  }
  function fnv1a32(str3) {
    let h2 = 2166136261;
    for (let i = 0; i < str3.length; i++) {
      h2 ^= str3.charCodeAt(i);
      h2 = Math.imul(h2, 16777619) >>> 0;
    }
    return h2.toString(16).padStart(8, "0");
  }
  function payloadHash(payload) {
    return fnv1a32(stableStringify(payload === void 0 ? null : payload));
  }

  var INPUT_FOR = Object.freeze({
    "profile.getAi": (id2) => ({ userId: id2 })
  });
  function readInput(path, id2) {
    const f = INPUT_FOR[path];
    return f ? f(id2) : { id: id2 };
  }
  var LIST_INPUT_FOR = Object.freeze({
    "gameAsset.getAllNames": () => ({})
  });
  function listInput(path) {
    const f = LIST_INPUT_FOR[path];
    return f ? f() : void 0;
  }
  function stableInput(v) {
    if (Array.isArray(v)) return "[" + v.map(stableInput).join(",") + "]";
    if (v && typeof v === "object") {
      return "{" + Object.keys(v).filter((k) => v[k] !== void 0).sort().map((k) => JSON.stringify(k) + ":" + stableInput(v[k])).join(",") + "}";
    }
    return v === void 0 ? "undefined" : JSON.stringify(v) ?? "null";
  }
  function sameInput(a, b) {
    return a === b || stableInput(a) === stableInput(b);
  }
  var CachedReader = class {
    constructor({ client, cache, budget, maxBatch = 20 }) {
      this.client = client;
      this.cache = cache;
      this.budget = budget;
      this.maxBatch = maxBatch;
      this.stats = { hits: 0, misses: 0, requests: 0 };
    }
    async get(path, id2, { fresh = false } = {}) {
      const [r] = await this.getMany(path, [id2], { fresh });
      return r;
    }
    async getMany(path, ids, { fresh = false } = {}) {
      if (procedure(path).kind !== "query") throw new Error("getMany is for queries: " + path);
      if (path === "skillTree.getAllFolders") {
        const r = await this.list(path, { fresh });
        return ids.map((id2) => r.ok ? { ok: true, data: r.data.find((row) => row.id === id2) } : r);
      }
      if (path === "coop.dungeon.getAll") {
        const r = await this.list(path, { fresh });
        if (r.ok && !Array.isArray(r.data)) throw new Error("coop.dungeon.getAll did not return an array");
        return ids.map((id2) => r.ok ? { ok: true, data: r.data.find((row) => row && row.id === id2) } : r);
      }
      const out = new Array(ids.length);
      const misses = [];
      for (let i = 0; i < ids.length; i++) {
        const hit = fresh ? null : await this.cache.get(path, ids[i]);
        if (hit) {
          this.stats.hits++;
          out[i] = { ok: true, data: hit.data, cached: true, at: hit.at };
        } else {
          this.stats.misses++;
          misses.push(i);
        }
      }
      let pos = 0;
      while (pos < misses.length) {
        let room = this.maxBatch;
        if (this.budget.isLimited(path)) {
          const cap = Math.min(this.maxBatch, 10, this.budget.allowance);
          const avail = this.budget.available(path);
          room = avail > 0 ? Math.min(cap, avail) : cap;
        }
        const idxs = misses.slice(pos, pos + room);
        await this.budget.acquire(path, idxs.length);
        this.stats.requests++;
        const results = await this.client.batch(idxs.map((i) => ({ path, input: readInput(path, ids[i]) })));
        for (let j = 0; j < idxs.length; j++) {
          const r = results[j];
          out[idxs[j]] = r;
          if (r.ok) await this.cache.put({ path, id: ids[idxs[j]], input: readInput(path, ids[idxs[j]]), data: r.data });
        }
        this.budget.observe(results, idxs.map(() => path));
        pos += idxs.length;
      }
      return out;
    }
    async list(path, { fresh = false, input } = {}) {
      if (procedure(path).kind !== "query") throw new Error("list is for queries: " + path);
      if (path === "skillTree.getAll" || path === "skillTree.getAllFolders") return this.skillInventory(path, { fresh, input });
      if (!/\.getAll(Ai)?Names$/.test(path) && !["coop.dungeon.getAll", "petSpecies.getAll", "title.getAll"].includes(path)) throw new Error("list() is for getAllNames/getAllAiNames; " + path + " needs a paged input");
      const sent = input === void 0 ? listInput(path) : input;
      const cacheable = sameInput(sent, listInput(path));
      const hit = fresh || !cacheable ? null : await this.cache.get(path, "");
      if (hit) {
        this.stats.hits++;
        return { ok: true, data: hit.data, cached: true, at: hit.at };
      }
      this.stats.misses++;
      await this.budget.acquire(path, 1);
      this.stats.requests++;
      const [r] = await this.client.batch([{ path, input: sent }]);
      if (r.ok && cacheable) await this.cache.put({ path, id: "", input: sent ?? null, data: r.data });
      this.budget.observe([r], [path]);
      return r;
    }
    async skillInventory(path, { fresh, input }) {
      const cacheable = input === void 0;
      const hit = fresh || !cacheable ? null : await this.cache.get(path, "");
      if (hit) {
        this.stats.hits++;
        return { ok: true, data: hit.data, cached: true };
      }
      this.stats.misses++;
      const query = async (sent) => {
        await this.budget.acquire(path, 1);
        this.stats.requests++;
        const [r] = await this.client.batch([{ path, input: sent }]);
        this.budget.observe([r], [path]);
        return r;
      };
      let rows = [];
      if (path === "skillTree.getAllFolders") {
        const r = await query({ includeHidden: true, ...input });
        if (!r.ok) return r;
        if (!Array.isArray(r.data)) throw new Error("folder inventory did not return an array");
        rows = r.data;
      } else {
        if (input?.cursor) throw new Error("complete skill inventory must start at cursor zero");
        const paths = input?.pathType ? [input.pathType] : ["SKILL", "BLOODRIGHT"];
        const scan = async () => {
          const ids =  new Set(), scanned = [];
          for (const pathType of paths) {
            let cursor = 0;
            for (; ; ) {
              const r = await query({ ...input, pathType, limit: 500, cursor });
              if (!r.ok) return r;
              if (!Array.isArray(r.data?.data) || !("nextCursor" in r.data)) throw new Error("malformed skill inventory page");
              for (const row of r.data.data) {
                if (!row?.id || ids.has(row.id) || row.pathType !== pathType) throw new Error("skill inventory shifted or repeated; refresh the preview");
                ids.add(row.id);
                scanned.push(row);
              }
              const next = r.data.nextCursor;
              if (next == null) break;
              if (!Number.isInteger(next) || next !== cursor + 1 || cursor >= 9999) throw new Error("invalid skill inventory cursor");
              cursor = next;
            }
          }
          return { ok: true, data: scanned };
        };
        const first = await scan();
        if (!first.ok) return first;
        const second = await scan();
        if (!second.ok) return second;
        if (stableStringify(first.data) !== stableStringify(second.data)) throw new Error("skill inventory changed between scans; coordinate editing and refresh the preview");
        rows = second.data;
      }
      if (cacheable) await this.cache.put({ path, id: "", input: input ?? null, data: rows });
      return { ok: true, data: rows };
    }
  };

  var fields_default = JSON.parse('{"_provenance":{"generator":"forge/tools/derive_fields.mjs","pin":"2af4b32066c39e2868efae5dba6b339278701dca","note":"top-level keys of each entity validator at the pinned commit; spreads are resolved into fields"},"entities":{"jutsu":{"source":"app/src/validators/combat.ts:1791","validator":"JutsuValidatorRawSchema","spreads":[],"fields":{"name":true,"image":true,"description":true,"battleDescription":true,"extraBaseCost":true,"jutsuWeapon":true,"jutsuType":true,"requiredPetSpeciesId":true,"jutsuRank":true,"requiredRank":true,"requiredLevel":true,"method":true,"coordinateTargeting":true,"methodSize":true,"target":true,"range":true,"statClassification":true,"elementClassification":true,"hidden":true,"injectableInBattle":true,"healthCost":true,"chakraCost":true,"staminaCost":true,"healthCostReducePerLvl":true,"chakraCostReducePerLvl":true,"staminaCostReducePerLvl":true,"actionCostPerc":true,"cooldown":true,"requiredSkillId":true,"bloodlineId":true,"requiredBloodlineItemId":true,"villageId":true,"effects":true,"battleUsageType":true,"reskinParentJutsuId":true,"bloodlineReskinId":true,"parentJutsuId":true,"requiredNinjutsuMastery":true,"requiredGenjutsuMastery":true,"requiredTaijutsuMastery":true,"requiredBukijutsuMastery":true,"requiredBloodlineMastery":true,"requiredSageMastery":true,"requiredStrength":true,"requiredSpeed":true,"requiredIntelligence":true,"requiredWillpower":true}},"item":{"source":"app/src/validators/combat.ts:1992","validator":"ItemValidatorRawSchema","spreads":["itemEconomySchema.shape","furnitureItemSchema.shape"],"fields":{"name":true,"image":true,"description":true,"battleDescription":true,"stackSize":true,"destroyOnUse":true,"chakraCost":true,"healthCost":true,"staminaCost":true,"healthCostReducePerLvl":true,"chakraCostReducePerLvl":true,"staminaCostReducePerLvl":true,"actionCostPerc":true,"canStack":true,"maxImbueNumber":true,"maxDurability":true,"inShop":true,"isEventItem":true,"preventBattleUsage":true,"hidden":true,"cooldown":true,"cost":true,"repsCost":true,"seichiSilverCost":true,"range":true,"maxEquips":true,"method":true,"coordinateTargeting":true,"methodSize":true,"target":true,"itemType":true,"weaponType":true,"rarity":true,"slot":true,"requiredLevel":true,"xpToLevel":true,"parentItemId":true,"requiredNinjutsuMastery":true,"requiredGenjutsuMastery":true,"requiredTaijutsuMastery":true,"requiredBukijutsuMastery":true,"requiredBloodlineMastery":true,"requiredSageMastery":true,"requiredStrength":true,"requiredSpeed":true,"requiredIntelligence":true,"requiredWillpower":true,"expireFromStoreAt":true,"effects":true,"canBeImbued":true,"canBeCrafted":true,"canBeHunted":true,"canBeGathered":true,"canBeTraded":true,"isFarmSeed":true,"farmGrowTimeSeconds":true,"farmYieldItemId":true,"farmMinLevel":true,"farmPlantExperience":true,"farmHarvestExperience":true,"farmSellValue":true,"farmExtractSeedItemId":true,"farmExtractSeedCount":true,"isFarmFertilizer":true,"farmTimeReductionSeconds":true,"farmFertilizerExperience":true,"cookingMinLevel":true,"cookingTimeSeconds":true,"cookingOutputQuantity":true,"cookingExperience":true,"mealDurationSeconds":true,"craftingExperience":true,"crystalTargetTypes":true,"requiredSkillId":true,"bloodlineId":true,"battleUsageType":true,"craftingRequirements":true,"auctionMinPrice":true,"auctionMaxPrice":true,"purchaseLimit":true,"purchaseLimitPeriod":true,"furnitureData":true}},"bloodline":{"source":"app/src/validators/combat.ts:1881","validator":"BloodlineValidator","spreads":[],"fields":{"name":true,"image":true,"description":true,"rank":true,"regenIncrease":true,"statClassification":true,"villageId":true,"hidden":true,"difficulty":true,"traits":true,"effects":true}},"quest":{"source":"app/src/validators/objectives.ts:892","validator":"QuestValidatorRawSchema","spreads":["masteryRequirementFields"],"fields":{"name":true,"image":true,"description":true,"successDescription":true,"questRank":true,"medicalRank":true,"huntingRank":true,"gatheringRank":true,"petTaskMinutes":true,"requiredLevel":true,"requiredFarmingLevel":true,"maxLevel":true,"maxAttempts":true,"maxCompletes":true,"requiredVillage":true,"requiredBloodlineId":true,"requiredSageModeId":true,"requiredSageRank":true,"prerequisiteQuestId":true,"tierLevel":true,"questType":true,"content":true,"hidden":true,"teamEnabled":true,"publicLocations":true,"retryDelay":true,"attemptDelay":true,"consecutiveObjectives":true,"endsAt":true,"startsAt":true,"raidBossMaxHealth":true,"raidBossCurrentHealth":true,"requiredNinjutsuMastery":true,"requiredGenjutsuMastery":true,"requiredTaijutsuMastery":true,"requiredBukijutsuMastery":true,"requiredBloodlineMastery":true,"requiredSageMastery":true}},"gameAsset":{"source":"app/src/validators/asset.ts:4","validator":"gameAssetValidator","spreads":[],"fields":{"name":true,"image":true,"frames":true,"speed":true,"type":true,"licenseDetails":true,"onInitialBattleField":true,"hidden":true,"url":true,"folder":true}},"petSpecies":{"source":"app/src/validators/petSpecies.ts:20","validator":"PetSpeciesValidator","spreads":[],"fields":{"name":true,"description":true,"artDirection":true,"rankConcepts":true,"rarity":true,"role":true,"preferredDamageElement":true,"isActive":true,"defaultJutsuIds":true,"aiRules":true,"includeDefaultRules":true,"effects":true,"skillTarget":true}},"badge":{"source":"app/src/validators/badge.ts:3","validator":"BadgeValidator","spreads":[],"fields":{"name":true,"image":true,"description":true}},"title":{"source":"app/src/validators/title.ts:22","validator":"TitleValidator","spreads":[],"fields":{"name":true,"description":true,"effects":true,"archived":true}},"ai":{"source":"app/src/validators/aiInput.ts:12","validator":"insertAiSchema","spreads":[],"columns":205,"omitted":["bracketImmunityPausedAt","covertTrainingMinutes","covertTrainingStartedAt","covertTrainingType","currentlyTrainingElement","currentlyTrainingMastery","deletionAt","elementalTrainingStartedAt","homeFurnitureRevision","lastSensoryAt","masteryTrainingStartedAt","occupation","occupationSignupAt","questData","stealthActivatedAt","stealthCooldownAt","travelFinishAt","warMission"],"extended":["bloodlineMastery","bukijutsuMastery","defence","effects","genjutsuMastery","intelligence","isSummon","items","jutsus","level","ninjutsuMastery","offence","poolsMultiplier","primaryElement","regeneration","sageMastery","secondaryElement","speed","statsMultiplier","strength","taijutsuMastery","willpower"],"fields":{"activeNpcQuestId":true,"activePetId":true,"activeTitleId":true,"activeTrainedElement":true,"aiCalls":true,"aiProfileId":true,"anbuId":true,"approvedTos":true,"avatar":true,"avatar3d":true,"avatarFacing":true,"avatarLight":true,"bank":true,"battleId":true,"bloodlineId":true,"bloodlineMastery":true,"bloodlineReskinId":true,"bloodright":true,"bloodrightSpent":true,"bracketImmunityLiftedUntil":true,"bukijutsuMastery":true,"buttonSfxOn":true,"clanId":true,"cookingExperience":true,"craftingExperience":true,"createdAt":true,"crimesA":true,"crimesB":true,"crimesC":true,"crimesD":true,"crimesH":true,"crimesS":true,"curChakra":true,"curEnergy":true,"curHealth":true,"curStamina":true,"dailyArenaFights":true,"dailyErrands":true,"dailyMedicalMissions":true,"dailyMissions":true,"dailyOverworldQuestRolls":true,"dailyPvpMissions":true,"dailySageActivations":true,"dailyTrainings":true,"dailyWarMissions":true,"dashboardContentPriority":true,"defaultAutoCombat":true,"defence":true,"earnedExperience":true,"effects":true,"elementalMastery":true,"elementalQueueHead":true,"elementalTrainingSpeed":true,"energyQueueHead":true,"energyQueueTail":true,"errands":true,"experience":true,"extraItemSlots":true,"extraJutsuSlots":true,"extraReskinSlots":true,"farmCurrency":true,"farmExtractorsOwned":true,"farmPlotsPurchased":true,"farmingExperience":true,"federalStatus":true,"gatheringExperience":true,"gender":true,"genjutsuMastery":true,"homeType":true,"huntingExperience":true,"iframesMuted":true,"immunityUntil":true,"inArena":true,"inShrines":true,"inboxNews":true,"intelligence":true,"isAi":true,"isBanned":true,"isEvent":true,"isOutlaw":true,"isSilenced":true,"isSummon":true,"isTradeBanned":true,"isWarCamp":true,"isWarned":true,"itemLoadout":true,"items":true,"joinedVillageAt":true,"jutsuLoadout":true,"jutsus":true,"lastIp":true,"latitude":true,"level":true,"location":true,"longitude":true,"marriageSlots":true,"masteryQueueHead":true,"masteryRanks":true,"maxChakra":true,"maxEnergy":true,"maxHealth":true,"maxStamina":true,"medicalExperience":true,"missionsA":true,"missionsB":true,"missionsC":true,"missionsD":true,"missionsH":true,"missionsS":true,"money":true,"monthlySkillResets":true,"movedTooFastCount":true,"musicOn":true,"nRecruited":true,"ninjutsuMastery":true,"npcTitle":true,"offence":true,"petAcquisitions":true,"petDailyClaims":true,"petExperience":true,"petSlots":true,"petTask":true,"poolsMultiplier":true,"preferredDamageElement":true,"preferredGeneral1":true,"preferredGeneral2":true,"primaryElement":true,"pveFights":true,"pvpExperience":true,"pvpExperienceDecayAt":true,"pvpFights":true,"pvpLosses":true,"pvpStreak":true,"pvpWins":true,"questFinishAt":true,"questPartyId":true,"rank":true,"rankedBattles":true,"rankedLoadout":true,"rankedLp":true,"rankedStreak":true,"rankedWins":true,"recruiterId":true,"regenAt":true,"regeneration":true,"rememberProfileTab":true,"reputationPoints":true,"reputationPointsTotal":true,"robImmunityUntil":true,"role":true,"sageMastery":true,"sageMasteryExperience":true,"sageModeId":true,"secondaryElement":true,"sector":true,"seichiSilver":true,"senseiId":true,"sensory":true,"sfxOn":true,"showBattleDescription":true,"showPvpRecord":true,"skillPoints":true,"speed":true,"staffAccount":true,"statsMultiplier":true,"status":true,"stealth":true,"stealthActive":true,"strength":true,"taijutsuMastery":true,"tavernMessages":true,"tavernTitleColor":true,"tavernUsernameColor":true,"towerDefensePoints":true,"trainingSpeed":true,"tutorialOn":true,"tutorialStep":true,"unreadNews":true,"unreadNotifications":true,"unreadRecruitRewards":true,"updatedAt":true,"userId":true,"username":true,"villageId":true,"villagePrestige":true,"warParticipantUntil":true,"weeklyPvpKills":true,"weeklyPvpKillsAt":true,"willpower":true}}}}');

  var isBloodrightEntity = (e) => e === "skillTree" || e === "skillTreeFolder";
  var bloodrightFields = (e) => new Set(e === "skillTree" ? contract_default.skillFields : contract_default.folderFields);
  var obj = (v) => v && typeof v === "object" && !Array.isArray(v);
  var str = (v) => typeof v === "string";
  var int = (v, min, max = Number.MAX_SAFE_INTEGER) => Number.isSafeInteger(v) && v >= min && v <= max;
  function bloodrightProblems(entity, data, live = null, { preCreate = false } = {}) {
    if (!obj(data)) return ["data must be an object"];
    const out = [];
    const fields = bloodrightFields(entity);
    for (const k of Object.keys(data)) if (!fields.has(k)) out.push(`unknown key ${k} for ${entity}`);
    const d = { ...live, ...data };
    const check = (ok, message) => {
      if (!ok) out.push(message);
    };
    check(str(d.name) && !!d.name.trim() && d.name.length <= 191, "name must contain 1..191 characters");
    check(d.image === void 0 || str(d.image) && d.image.length <= (entity === "skillTree" ? 191 : 512), "invalid image");
    check(d.description === void 0 || str(d.description) || entity === "skillTreeFolder" && d.description === null, "description must be text");
    check(d.hidden === void 0 || typeof d.hidden === "boolean", "hidden must be boolean");
    if (entity === "skillTreeFolder") {
      check(d.order === void 0 || Number.isSafeInteger(d.order), "folder order must be an integer");
      return out;
    }
    check(str(d.name) && d.name === d.name.trim(), "skill name must not have surrounding whitespace");
    check(d.pathType === "BLOODRIGHT" && str(d.bloodlineId) && !!d.bloodlineId && !d.bloodlineId.startsWith("@"), "requires a literal bloodlineId and pathType BLOODRIGHT");
    check(d.skillType === "DEFAULT", "Bloodright skillType must be DEFAULT");
    check(["SELF", "ENEMIES", "ALLIES"].includes(d.target), "invalid skill target");
    check(int(d.tier, 1, 10), "tier must be 1..10");
    check(int(d.costSkillPoints, 1), "costSkillPoints must be a positive integer");
    check(int(d.seichiSilverCost, 0, 2147483647), "explicit seichiSilverCost must be 0..2147483647");
    check(Array.isArray(d.requiredSkillIds) && d.requiredSkillIds.every((v) => str(v) && !!v) && new Set(d.requiredSkillIds).size === d.requiredSkillIds.length, "invalid prerequisite IDs");
    check(d.folderId == null || str(d.folderId) && !!d.folderId, "invalid folderId");
    check(Array.isArray(d.effects), "effects must be an array");
    for (const [i, e] of (Array.isArray(d.effects) ? d.effects : []).entries()) {
      const where = `effects[${i}]`;
      if (!obj(e)) {
        out.push(`${where} must be an object`);
        continue;
      }
      for (const k of Object.keys(e)) if (!contract_default.effectFields.includes(k)) out.push(`${where}: unknown key ${k}`);
      check(["increasepotency", "decreasepotency"].includes(e.type), `${where}: only audited potency effects supported`);
      check(Number.isFinite(e.power) && e.power >= 0, `${where}: power must be nonnegative`);
      check(Number.isFinite(e.powerPerLevel) && e.powerPerLevel >= 0 && e.powerPerLevel <= 1, `${where}: powerPerLevel must be 0..1`);
      check(int(e.rounds, 1, 100), `${where}: explicit rounds must be 1..100`);
      check(["static", "percentage"].includes(e.calculation), `${where}: invalid calculation`);
      check(["SELF", "INHERIT"].includes(e.target), `${where}: invalid target`);
      check(e.direction === "offence", `${where}: direction must be offence`);
      check(e.friendlyFire === void 0 || ["ALL", "FRIENDLY", "ENEMIES"].includes(e.friendlyFire), `${where}: invalid friendlyFire`);
      check(contract_default.tags.includes(e.affectedTag), `${where}: choose one supported affectedTag`);
      check(Array.isArray(e.affectedElements) && e.affectedElements.length > 0 && e.affectedElements.every((v) => contract_default.elements.includes(v)), `${where}: resolve affectedElements explicitly`);
      for (const k of ["description", "staticAssetPath", "staticAnimation", "appearAnimation", "disappearAnimation", "appearSfx", "disappearSfx"]) check(str(e[k]), `${where}: ${k} must be text`);
      check(e.timeTracker === void 0, `${where}: runtime timeTracker is not importable`);
      check(e.coordinateTargeting == null, `${where}: coordinateTargeting is not importable`);
    }
    if (!preCreate && live) check(str(d.image) && !!d.image, "skill image must be preserved or supplied");
    return out;
  }
  function writableSnapshot(entity, row) {
    const out = {};
    for (const key of bloodrightFields(entity)) if (row[key] !== void 0) out[key] = row[key];
    if (entity === "skillTreeFolder" && out.description == null) out.description = "";
    return out;
  }

  var isDungeonEntity = (e) => e === "dungeon";
  var dungeonFields = () => new Set(contract_default3.contentFields);
  var B = contract_default3.bounds;
  var D = contract_default3.defaults;
  var obj2 = (v) => v && typeof v === "object" && !Array.isArray(v);
  var str2 = (v) => typeof v === "string";
  var num = (v) => typeof v === "number" && Number.isFinite(v);
  var int2 = (v, min, max) => Number.isSafeInteger(v) && v >= min && v <= max;
  var isRef = (v) => str2(v) && v.startsWith("@");
  var ISO_INSTANT = /^\d{4}-\d{2}-\d{2}(?:T\d{2}:\d{2}(?::\d{2}(?:\.\d{1,9})?)?(?:Z|[+-]\d{2}:\d{2}))?$/;
  var validDate = (v) => v instanceof Date ? !Number.isNaN(v.getTime()) : str2(v) && ISO_INSTANT.test(v) && !Number.isNaN(Date.parse(v));
  var REF_FOR_DROP = Object.freeze({ item: ["item"], cache: ["item"], jutsu: ["jutsu"], package: [] });
  function idProblem(v, allowed, where) {
    if (!str2(v) || !v.trim()) return `${where} must be a non-empty id`;
    if (!isRef(v)) return null;
    const m = v.match(/^@(\w+):(.+)$/);
    if (!m || !allowed.includes(m[1])) {
      return allowed.length ? `${where}: ${v} is not a ${allowed.map((p) => `@${p}:`).join(" or ")} ref` : `${where}: ${v} must be a literal id (no ref type exists for it)`;
    }
    return null;
  }
  function unknownKeys(o, allowed, where, out, why = "the server's validator would drop it silently") {
    for (const k of Object.keys(o)) if (!allowed.includes(k)) out.push(`${where}: unknown key "${k}" (${why})`);
  }
  function liveDrift(content) {
    if (!obj2(content)) return ["live dungeon row has no content object; refusing to edit it"];
    const out = [];
    const why = "schema drift: the pinned contract does not know it and a save would delete it; re-derive src/dungeon/contract.json first";
    unknownKeys(content, contract_default3.contentFields, "live content", out, why);
    if (Array.isArray(content.tiers)) content.tiers.forEach((tier, ti) => Array.isArray(tier) && tier.forEach((f, fi) => {
      if (!obj2(f)) return;
      unknownKeys(f, contract_default3.floorFields, `live tiers[${ti}][${fi}]`, out, why);
      if (Array.isArray(f.waves)) f.waves.forEach((w, wi) => obj2(w) && unknownKeys(w, contract_default3.waveFields, `live tiers[${ti}][${fi}].waves[${wi}]`, out, why));
    }));
    if (obj2(content.rewards)) {
      unknownKeys(content.rewards, contract_default3.rewardFields, "live rewards", out, why);
      if (Array.isArray(content.rewards.drops)) content.rewards.drops.forEach((d, i) => obj2(d) && unknownKeys(d, contract_default3.dropFields, `live rewards.drops[${i}]`, out, why));
    }
    return out;
  }
  function packageDrops(content) {
    const drops = obj2(content) && obj2(content.rewards) && Array.isArray(content.rewards.drops) ? content.rewards.drops : [];
    return drops.filter((d) => obj2(d) && d.type === "package").map((d) => d.id);
  }
  function dungeonProblems(data, live = null, { preCreate = false, refreshPackages = false } = {}) {
    if (!obj2(data)) return ["data must be the dungeon content object"];
    const out = [];
    unknownKeys(data, contract_default3.contentFields, "content", out);
    if (preCreate && data.hidden !== true) out.push("a dungeon create must carry hidden:true (everything ships hidden; publishing is a separate step)");
    if (!preCreate && !live) return out;
    if (!preCreate) {
      const drift = liveDrift(live.content);
      if (drift.length) return [...out, ...drift];
    }
    const d = { ...preCreate ? {} : live.content, ...data };
    const check = (ok, message) => {
      if (!ok) out.push(message);
    };
    check(str2(d.name) && d.name.trim().length >= 1 && d.name.trim().length <= B.nameMax, `name must contain 1..${B.nameMax} characters`);
    check(!str2(d.name) || d.name === d.name.trim(), "name must not start or end with whitespace (the server trims it)");
    check(d.description === void 0 || str2(d.description) && d.description.length <= B.descriptionMax, `description must be text of at most ${B.descriptionMax} characters`);
    check(
      d.structureAssetId === void 0 || str2(d.structureAssetId) && d.structureAssetId.length <= B.structureAssetIdMax && !isRef(d.structureAssetId),
      "structureAssetId must be a literal map-structure asset id (a mapAsset row, not a gameAsset; no ref type exists for it) or empty"
    );
    check(
      d.structureScale === void 0 || num(d.structureScale) && d.structureScale >= B.structureScale.min && d.structureScale <= B.structureScale.max,
      `structureScale must be ${B.structureScale.min}..${B.structureScale.max}`
    );
    check(int2(d.sector, B.sector.min, B.sector.max), `sector must be an integer ${B.sector.min}..${B.sector.max}`);
    check(int2(d.longitude, B.longitude.min, B.longitude.max), `longitude must be an integer ${B.longitude.min}..${B.longitude.max}`);
    check(int2(d.latitude, B.latitude.min, B.latitude.max), `latitude must be an integer ${B.latitude.min}..${B.latitude.max}`);
    check(
      "expiresAt" in d && (d.expiresAt === null || validDate(d.expiresAt)),
      "expiresAt is required: null, YYYY-MM-DD, or a date-time with Z or an offset"
    );
    check(d.hidden === void 0 || typeof d.hidden === "boolean", "hidden must be boolean");
    check(d.background === void 0 || contract_default3.biomes.includes(d.background), `background must be one of ${contract_default3.biomes.join(", ")}`);
    tierProblems(d.tiers, out);
    rewardProblems(d.rewards, out, preCreate || "rewards" in data);
    const packages = packageDrops(d);
    if (!preCreate && packages.length && !refreshPackages) {
      out.push(`rewards: package drop(s) ${packages.join(", ")}: coop.dungeon.save re-copies every package snapshot from the CURRENT catalog, which Forge cannot read, so stored package rewards may change. Set "refreshPackages": true to accept that`);
    }
    return out;
  }
  function tierProblems(tiers, out) {
    if (!Array.isArray(tiers) || tiers.length < 1 || tiers.length > B.maxTiers) {
      out.push(`tiers must hold 1..${B.maxTiers} tiers`);
      return;
    }
    tiers.forEach((tier, ti) => {
      if (!Array.isArray(tier) || tier.length !== B.floorsPerTier) {
        out.push(`tiers[${ti}] must hold exactly ${B.floorsPerTier} floors`);
        return;
      }
      tier.forEach((floor, fi) => {
        const where = `tiers[${ti}][${fi}]`;
        if (!obj2(floor)) {
          out.push(`${where} must be an object`);
          return;
        }
        unknownKeys(floor, contract_default3.floorFields, where, out);
        const last = ti === tiers.length - 1 && fi === B.floorsPerTier - 1;
        const expected = last ? "boss" : fi === B.floorsPerTier - 1 ? "mini-boss" : "floor";
        if (!contract_default3.floorKinds.includes(floor.kind)) out.push(`${where}.kind must be one of ${contract_default3.floorKinds.join(", ")}`);
        else if (floor.kind !== expected) out.push(`${where}.kind must be "${expected}" (each non-final tier ends on a mini-boss, the last floor is the boss)`);
        const waves = floor.waves;
        if (!Array.isArray(waves) || waves.length < 1 || waves.length > B.maxWaves) {
          out.push(`${where}.waves must hold 1..${B.maxWaves} waves`);
          return;
        }
        waves.forEach((wave, wi) => {
          const w = `${where}.waves[${wi}]`;
          if (!obj2(wave)) {
            out.push(`${w} must be an object`);
            return;
          }
          unknownKeys(wave, contract_default3.waveFields, w, out);
          if (!Array.isArray(wave.aiIds) || wave.aiIds.length < 1 || wave.aiIds.length > B.maxMobs) out.push(`${w}.aiIds must hold 1..${B.maxMobs} enemies`);
          else wave.aiIds.forEach((id2, ai) => {
            const p = idProblem(id2, ["ai"], `${w}.aiIds[${ai}]`);
            if (p) out.push(p);
          });
          const delay = wave.delayRounds === void 0 ? D.wave.delayRounds : wave.delayRounds;
          if (!int2(delay, 0, B.maxWaveDelayRounds)) out.push(`${w}.delayRounds must be an integer 0..${B.maxWaveDelayRounds} (null is not accepted)`);
          else if (wi === 0 && delay !== 0) out.push(`${w}.delayRounds must be 0: the first wave starts immediately`);
        });
      });
    });
  }
  function rewardProblems(rewards, out, authored) {
    if (!obj2(rewards)) {
      out.push("rewards must be an object {money, experience, tokens, prestige, drops}");
      return;
    }
    unknownKeys(rewards, contract_default3.rewardFields, "rewards", out);
    for (const k of ["money", "experience"]) {
      const v = rewards[k];
      if (v !== void 0 && !(num(v) && v >= 0 && v <= B.maxRewardAmount)) out.push(`rewards.${k} must be 0..${B.maxRewardAmount}`);
    }
    for (const k of ["tokens", "prestige"]) {
      const v = rewards[k];
      if (v !== void 0 && !int2(v, 0, B.maxRewardAmount)) out.push(`rewards.${k} must be an integer 0..${B.maxRewardAmount}`);
    }
    const drops = rewards.drops === void 0 ? [] : rewards.drops;
    if (!Array.isArray(drops) || drops.length > B.maxDrops) {
      out.push(`rewards.drops must be a list of at most ${B.maxDrops} drops (null is not accepted)`);
      return;
    }
    let items = 0;
    drops.forEach((drop, i) => {
      const where = `rewards.drops[${i}]`;
      if (!obj2(drop)) {
        out.push(`${where} must be an object`);
        return;
      }
      unknownKeys(drop, contract_default3.dropFields, where, out);
      if ("package" in drop && authored) out.push(`${where}.package: the server copies the catalog snapshot at save and ignores a sent payload; omit it`);
      if (!contract_default3.dropTypes.includes(drop.type)) {
        out.push(`${where}.type must be one of ${contract_default3.dropTypes.join(", ")}`);
        return;
      }
      const p = idProblem(drop.id, REF_FOR_DROP[drop.type], `${where}.id`);
      if (p) out.push(p);
      if (!(num(drop.chance) && drop.chance >= B.chance.min && drop.chance <= B.chance.max)) out.push(`${where}.chance must be ${B.chance.min}..${B.chance.max}`);
      const quantity = drop.quantity === void 0 ? D.drop.quantity : drop.quantity;
      if (!int2(quantity, 1, B.maxRewardQuantity)) out.push(`${where}.quantity must be an integer 1..${B.maxRewardQuantity} (null is not accepted)`);
      else if (drop.type === "jutsu" && quantity !== 1) out.push(`${where}.quantity must be 1: jutsu rewards can only be learned once`);
      else if (drop.type === "item" || drop.type === "cache") items += quantity;
    });
    if (items > B.maxGrantedItems) out.push(`rewards: up to ${items} items per player exceeds ${B.maxGrantedItems} (dungeonRewardError)`);
  }
  function mergeDungeon(live, data) {
    const out = { ...obj2(live) && obj2(live.content) ? live.content : {}, ...data };
    if (obj2(out.rewards) && Array.isArray(out.rewards.drops)) {
      out.rewards = { ...out.rewards, drops: out.rewards.drops.map((d) => obj2(d) && "package" in d ? (({ package: _p, ...rest }) => rest)(d) : d) };
    }
    return out;
  }
  function normalizeDungeon(c) {
    if (!obj2(c)) return c;
    const fill = (defaults, o) => {
      const r = { ...o };
      for (const [k, v] of Object.entries(defaults)) if (r[k] === void 0) r[k] = structuredClone(v);
      return r;
    };
    const n = fill(D.content, c);
    if (str2(n.name)) n.name = n.name.trim();
    if (n.expiresAt !== null && validDate(n.expiresAt)) n.expiresAt = new Date(n.expiresAt).toISOString();
    if (Array.isArray(n.tiers)) {
      n.tiers = n.tiers.map((t) => Array.isArray(t) ? t.map((f) => obj2(f) && Array.isArray(f.waves) ? { ...f, waves: f.waves.map((w) => obj2(w) ? fill(D.wave, w) : w) } : f) : t);
    }
    if (obj2(n.rewards)) {
      n.rewards = fill(D.rewards, n.rewards);
      if (Array.isArray(n.rewards.drops)) n.rewards.drops = n.rewards.drops.map((d) => obj2(d) ? fill(D.drop, (({ package: _p, ...rest }) => rest)(d)) : d);
    }
    return n;
  }
  function dungeonDiffs(asserted, liveContent) {
    const a = normalizeDungeon(asserted), l = normalizeDungeon(obj2(liveContent) ? liveContent : {});
    const diffs = [];
    for (const k of Object.keys(asserted)) if (!deepEqualPayload(a[k], l[k])) diffs.push({ key: k, sent: asserted[k], live: obj2(liveContent) ? liveContent[k] : void 0 });
    return diffs;
  }
  function contentDiffKeys(planned, liveContent) {
    const a = normalizeDungeon(planned), l = normalizeDungeon(obj2(liveContent) ? liveContent : {});
    const keys =  new Set([...Object.keys(a), ...Object.keys(l)]);
    return [...keys].filter((k) => !deepEqualPayload(a[k], l[k]));
  }
  var dungeonName = (row) => obj2(row) && obj2(row.content) ? row.content.name : void 0;

  var PET_SLOTS = Object.freeze({ COMMON: 2, UNCOMMON: 3, RARE: 4, EPIC: 5, LEGENDARY: 6 });
  var PET_STRIPPED_OK = Object.freeze(["hidden"]);
  var ACTIVE_EFFECTS =  new Set([
    "damage",
    "elementaldamage",
    "heal",
    "shield",
    "increasestat",
    "decreasestat",
    "increasedamagegiven",
    "decreasedamagegiven",
    "increasedamagetaken",
    "decreasedamagetaken",
    "clear",
    "cleanse",
    "move"
  ]);
  var MASTERIES = [
    "requiredNinjutsuMastery",
    "requiredGenjutsuMastery",
    "requiredTaijutsuMastery",
    "requiredBukijutsuMastery",
    "requiredBloodlineMastery",
    "requiredSageMastery"
  ];
  var LINKS = ["bloodlineId", "bloodlineReskinId", "reskinParentJutsuId", "villageId", "requiredSkillId", "requiredBloodlineItemId"];
  var NON_NEGATIVE = [
    "healthCost",
    "chakraCost",
    "staminaCost",
    "healthCostReducePerLvl",
    "chakraCostReducePerLvl",
    "staminaCostReducePerLvl",
    "range",
    "cooldown"
  ];
  function normalizeSpecies(d) {
    if (!d || typeof d !== "object") return d;
    const out = { ...d };
    for (const k of ["name", "description"]) if (typeof out[k] === "string") out[k] = out[k].trim();
    if ("artDirection" in out) out.artDirection = typeof out.artDirection === "string" ? out.artDirection.trim() || null : out.artDirection ?? null;
    if (Array.isArray(out.rankConcepts)) {
      const kept = out.rankConcepts.map((c) => typeof c === "string" ? c.trim() : c ?? "");
      while (kept.length && !kept[kept.length - 1]) kept.pop();
      out.rankConcepts = kept;
    }
    return out;
  }
  function petSpeciesPayload(d) {
    const out = { ...d };
    for (const k of PET_STRIPPED_OK) delete out[k];
    return out;
  }
  function petSpeciesProblems(data, live, { preCreate = false } = {}) {
    const out = [];
    if ("hidden" in data && data.hidden !== true) out.push("hidden: species have no hidden column; a create carries hidden:true (law 16b) and isActive:false");
    if (preCreate && data.isActive !== false) out.push("isActive must be false on create: an active species is offered to players at once (publishing is a separate step)");
    const ids = data.defaultJutsuIds;
    if (ids !== void 0) {
      if (!Array.isArray(ids)) out.push("defaultJutsuIds must be an array");
      else {
        if (new Set(ids).size !== ids.length) out.push("defaultJutsuIds: choose each default pet jutsu only once");
        const rarity = data.rarity ?? live?.rarity;
        if (PET_SLOTS[rarity] !== void 0 && ids.length > PET_SLOTS[rarity]) out.push(`defaultJutsuIds: ${ids.length} defaults exceed the ${PET_SLOTS[rarity]} jutsu slots of a ${rarity} species`);
      }
    }
    for (const [i, f] of (Array.isArray(data.effects) ? data.effects : []).entries()) {
      if (f && (f.type === "barrier" || f.type === "move")) out.push(`effects[${i}]: ${f.type} needs an empty-ground action; an innate skill cannot carry it`);
      if (f && f.target === "COORDINATES") out.push(`effects[${i}]: an innate skill cannot target COORDINATES`);
    }
    return out;
  }
  function petJutsuProblems(data, live = null) {
    const j = { ...live ?? {}, ...data };
    const out = [];
    if (j.requiredPetSpeciesId && j.jutsuType !== "PETS") out.push("requiredPetSpeciesId needs jutsuType PETS (the server refuses it otherwise)");
    if (j.jutsuType !== "PETS") return out;
    const bad = (m) => out.push("PETS jutsu a pet could never equip: " + m);
    if (j.injectableInBattle === true) bad("injectableInBattle must be false");
    if (j.battleUsageType === "PVP") bad("battleUsageType PVP");
    if (j.jutsuRank === "H") bad("H rank");
    for (const k of LINKS) if (j[k]) bad(`${k} must be empty`);
    if (j.jutsuWeapon !== void 0 && j.jutsuWeapon !== "NONE") bad("jutsuWeapon must be NONE");
    if (j.elementClassification && j.elementClassification !== "None") bad("elementClassification must be None");
    for (const k of MASTERIES) if (j[k]) bad(`${k} must be empty`);
    for (const k of NON_NEGATIVE) if (j[k] !== void 0 && !(Number.isFinite(Number(j[k])) && Number(j[k]) >= 0)) bad(`${k} must be a finite number >= 0`);
    if (j.actionCostPerc !== void 0 && !(Number(j.actionCostPerc) >= 10 && Number(j.actionCostPerc) <= 100)) bad("actionCostPerc must be 10-100");
    if (Array.isArray(j.effects)) {
      if (!j.effects.length) bad("it has no effects");
      for (const [i, f] of j.effects.entries()) {
        if (!f || typeof f !== "object") continue;
        if (!ACTIVE_EFFECTS.has(f.type)) {
          bad(`effects[${i}] ${f.type} is not a pet effect`);
          continue;
        }
        const p = f.power ?? 1, ppl = f.powerPerLevel ?? 0;
        if (!(Number(p) >= 0) || !(Number(ppl) >= 0)) bad(`effects[${i}] power and powerPerLevel must be >= 0`);
        if (f.calculation === "percentage" && Number(p) > 100) bad(`effects[${i}] percentage power above 100`);
        if (Array.isArray(f.elements) && f.elements.some((e) => e !== "None")) bad(`effects[${i}] carries elements`);
      }
    }
    return out;
  }

  var HIDDENLESS = Object.freeze(["petSpecies", "badge", "title"]);
  var REQUIRED = { badge: ["name", "image", "description"], title: ["name", "archived"] };
  var MASTERY = ["Ninjutsu", "Genjutsu", "Taijutsu", "Bukijutsu", "Sage", "Bloodline"];
  var url = (s) => {
    try {
      return /^https?:\/\/\S+$/.test(s) && !!new URL(s);
    } catch {
      return false;
    }
  };
  function catalogProblems(entity, data, { preCreate = false } = {}) {
    const out = [], d = data, str3 = (v) => typeof v === "string";
    if ("hidden" in d && d.hidden !== true) out.push(`hidden: ${entity} has no hidden column; send hidden:true (law 16b)`);
    if (preCreate) {
      for (const k of REQUIRED[entity]) if (d[k] === void 0) out.push(`${k} is required on a ${entity} create`);
    }
    if ("name" in d && !(str3(d.name) && d.name && d.name === d.name.trim() && d.name.length <= 191)) out.push("name: 1-191 characters, no leading or trailing whitespace");
    const cap = entity === "badge" ? 500 : 512;
    if ("description" in d && !(str3(d.description) && d.description.length <= cap && (entity === "title" || d.description))) out.push(entity === "badge" ? "description: 1-500 characters (the Badge column holds 500)" : "description: at most 512 characters");
    if ("image" in d && !(str3(d.image) && (d.image.startsWith("@img:") || url(d.image) && d.image.length <= 191))) out.push("image: an @img ref or a URL of at most 191 characters");
    if ("archived" in d && typeof d.archived !== "boolean") out.push("archived must be a boolean");
    if ("effects" in d) {
      if (!Array.isArray(d.effects) || d.effects.length > 20) out.push("effects: an array of at most 20");
      else d.effects.forEach((f, i) => {
        if (!(typeof f?.power === "number" && Number.isFinite(f.power) && f.power >= 0)) out.push(`effects[${i}]: power must be a finite number >= 0`);
        if (f?.type === "increasemastery" && !(Array.isArray(f.masteryTypes) && f.masteryTypes.length && f.masteryTypes.every((m) => MASTERY.includes(m)))) out.push(`effects[${i}]: masteryTypes needs 1+ of ${MASTERY.join("/")}`);
      });
    }
    return out;
  }

  var AI_EXTRA_KEYS = Object.freeze(["jutsus", "items", "primaryElement", "secondaryElement", "rules", "includeDefaultRules"]);
  var AI_STRIPPED_OK = Object.freeze(["hidden"]);
  var AI_POST_0056_KEYS = Object.freeze([
    "offence",
    "defence",
    "ninjutsuMastery",
    "genjutsuMastery",
    "taijutsuMastery",
    "bukijutsuMastery",
    "bloodlineMastery",
    "sageMastery"
  ]);
  var SERVER_OWNED = Object.freeze(["id", "userId", "createdAt", "updatedAt", "aiProfileId"]);
  var AI_OMITTED = Object.freeze([...fields_default.entities.ai.omitted]);
  var SCHEMA_ENTITY = Object.freeze({ jutsu: "jutsu", item: "item", bloodline: "bloodline", quest: "quest", asset: "gameAsset", ai: "ai", petSpecies: "petSpecies", badge: "badge", title: "title" });
  function expandNested(raw) {
    if (!raw || typeof raw !== "object" || !Array.isArray(raw.sets) || !raw.effects) return null;
    const at = (i) => Number.isInteger(i) && i >= 0 && i < raw.sets.length && Array.isArray(raw.sets[i]) ? raw.sets[i] : null;
    const out = {};
    for (const [section, v] of Object.entries(raw)) {
      if (section === "_meta" || section === "sets") continue;
      if (typeof v === "number") {
        const set = at(v);
        if (!set) return null;
        out[section] = set;
        continue;
      }
      if (!v || typeof v !== "object" || Array.isArray(v)) return null;
      const byValue = {};
      for (const [discriminator, i] of Object.entries(v)) {
        const set = at(i);
        if (!set) return null;
        byValue[discriminator] = set;
      }
      out[section] = byValue;
    }
    return out.effects ? out : null;
  }
  var Validator = class {
    constructor(schemas, nested = null) {
      this.nested = expandNested(nested);
      this.fields = {};
      const ents = schemas && schemas.entities ? schemas.entities : {};
      for (const [name, e] of Object.entries(ents)) {
        if (e && e.fields && typeof e.fields === "object") this.fields[name] = new Set(Object.keys(e.fields));
      }
      this.schemaMissing = Object.keys(this.fields).length === 0;
    }
    knownFields(entity) {
      if (isBloodrightEntity(entity)) return bloodrightFields(entity);
      if (isDungeonEntity(entity)) return dungeonFields();
      const s = SCHEMA_ENTITY[entity];
      return s ? this.fields[s] ?? null : null;
    }
    problems(entity, data, live = null, { preCreate = false, refreshPackages = false } = {}) {
      if (isBloodrightEntity(entity)) return bloodrightProblems(entity, data, live, { preCreate });
      if (isDungeonEntity(entity)) return dungeonProblems(data, live, { preCreate, refreshPackages });
      const out = [];
      if (!data || typeof data !== "object") return ["data is not an object"];
      const keys = Object.keys(data);
      if (entity === "ai" || entity === "aiProfile") {
        const allowed =  new Set([...AI_EXTRA_KEYS, ...AI_STRIPPED_OK]);
        if (entity === "ai") {
          const pinned = this.knownFields("ai");
          if (!pinned) out.push("no pinned insertAiSchema field set: cannot validate ai keys");
          else for (const k of pinned) allowed.add(k);
          for (const k of AI_POST_0056_KEYS) allowed.add(k);
        }
        if (live) for (const k of Object.keys(live)) allowed.add(k);
        for (const k of AI_OMITTED) allowed.delete(k);
        for (const k of SERVER_OWNED) allowed.delete(k);
        const check = entity === "aiProfile" ?  new Set(["rules", "includeDefaultRules"]) : allowed;
        for (const k of keys) if (AI_OMITTED.includes(k) || entity === "ai" && SERVER_OWNED.includes(k)) out.push(`"${k}" is not writable on an ai (insertAiSchema omits it or the server owns it)`);
        for (const k of keys) if (!check.has(k) && !AI_OMITTED.includes(k) && !SERVER_OWNED.includes(k)) out.push(`unknown key "${k}" for ${entity}`);
        if (entity === "ai" && Array.isArray(data.items)) {
          for (const t of data.items) if (t && typeof t === "object" && !Array.isArray(t.ids) && t.itemId == null && t.id == null) out.push("items: each entry is {ids: [itemId], number: dropChancePerc} (law 69)");
        }
        if (Array.isArray(data.rules)) out.push(...ruleProblems(data.rules));
      } else {
        const known = this.knownFields(entity);
        if (!known) out.push(`no field schema for entity ${entity}`);
        else for (const k of keys) if (!known.has(k) && !SERVER_OWNED.includes(k) && !(k === "hidden" && HIDDENLESS.includes(entity))) out.push(`unknown key "${k}" for ${entity} (would be silently dropped by the server)`);
        if (entity === "petSpecies") {
          out.push(...petSpeciesProblems(data, live, { preCreate }));
          if (Array.isArray(data.aiRules)) out.push(...ruleProblems(data.aiRules).map((p) => "aiRules: " + p));
        }
        if (entity === "jutsu") out.push(...petJutsuProblems(data, live));
        if (entity === "badge" || entity === "title") out.push(...catalogProblems(entity, data, { preCreate }));
      }
      out.push(...this.nestedProblems(entity, data));
      if (data.image === "") out.push("image is an empty string: omit the key so fetch-merge keeps the current value");
      for (const [k, v] of Object.entries(data)) if (typeof v === "string" && /^@\w+:@\w+:/.test(v)) out.push(`${k}: doubled ref prefix`);
      return out;
    }
    nestedProblems(entity, data) {
      const out = [];
      if (!data || typeof data !== "object") return out;
      const families = [];
      if (Array.isArray(data.effects) && data.effects.length) families.push("effects");
      if (entity === "quest" && data.content && typeof data.content === "object" && Object.keys(data.content).length) families.push("quest content");
      const rules = entity === "petSpecies" ? data.aiRules : entity === "ai" || entity === "aiProfile" ? data.rules : null;
      if (Array.isArray(rules) && rules.length) families.push("ai rules");
      if (!families.length) return out;
      if (!this.nested) return [`no derived nested key set: refusing to send ${families.join(", ")} unchecked`];
      const check = (obj3, allowed, where) => {
        for (const k of Object.keys(obj3)) {
          if (allowed.includes(k)) continue;
          out.push(`${where}: unknown key "${k}" (the server's validator would drop it silently)`);
        }
      };
      const fx = (entity === "title" ? this.nested.titleEffects : this.nested.effects) ?? {};
      for (const [i, f] of (Array.isArray(data.effects) ? data.effects : []).entries()) {
        if (!f || typeof f !== "object") {
          out.push(`effects[${i}] is not an object`);
          continue;
        }
        const allowed = typeof f.type === "string" ? fx[f.type] : null;
        if (!allowed) {
          out.push(`effects[${i}]: unknown effect type ${JSON.stringify(f.type)} at the pin`);
          continue;
        }
        check(f, allowed, `effects[${i}] (${f.type})`);
      }
      if (entity === "quest" && data.content && typeof data.content === "object") {
        check(data.content, this.nested.questContent, "content");
        if (data.content.reward && typeof data.content.reward === "object") {
          check(data.content.reward, this.nested.objectiveReward, "content.reward");
        }
        for (const [i, o] of (Array.isArray(data.content.objectives) ? data.content.objectives : []).entries()) {
          if (!o || typeof o !== "object") {
            out.push(`content.objectives[${i}] is not an object`);
            continue;
          }
          const allowed = typeof o.task === "string" ? this.nested.objectives[o.task] : null;
          if (!allowed) {
            out.push(`content.objectives[${i}]: unknown task ${JSON.stringify(o.task)} at the pin`);
            continue;
          }
          const where = `content.objectives[${i}] (${o.task})`;
          check(o, allowed, where);
          if (Array.isArray(o.nextObjectiveId)) {
            for (const [j, c] of o.nextObjectiveId.entries()) {
              if (c && typeof c === "object") check(c, this.nested.objectiveChoice, `${where}.nextObjectiveId[${j}]`);
            }
          }
          for (const key of ["opponentAIs", "attackers"]) {
            for (const [j, e] of (Array.isArray(o[key]) ? o[key] : []).entries()) {
              if (e && typeof e === "object") check(e, this.nested.idsWithNumber, `${where}.${key}[${j}]`);
            }
          }
        }
      }
      if (Array.isArray(rules)) {
        for (const [i, r] of rules.entries()) {
          if (!r || typeof r !== "object") continue;
          for (const [j, c] of (Array.isArray(r.conditions) ? r.conditions : []).entries()) {
            if (!c || typeof c !== "object") continue;
            const allowed = typeof c.type === "string" ? this.nested.aiConditions[c.type] : null;
            if (!allowed) {
              out.push(`rules[${i}].conditions[${j}]: unknown condition type ${JSON.stringify(c.type)} at the pin`);
              continue;
            }
            check(c, allowed, `rules[${i}].conditions[${j}] (${c.type})`);
          }
          const a = r.action;
          if (a && typeof a === "object") {
            const allowed = typeof a.type === "string" ? this.nested.aiActions[a.type] : null;
            if (!allowed) out.push(`rules[${i}].action: unknown action type ${JSON.stringify(a.type)} at the pin`);
            else check(a, allowed, `rules[${i}].action (${a.type})`);
          }
        }
      }
      return out;
    }
  };
  function ruleProblems(rules) {
    const out = [];
    rules.forEach((r, i) => {
      if (!r || typeof r !== "object") {
        out.push(`rules[${i}] is not an object`);
        return;
      }
      if (!Array.isArray(r.conditions)) out.push(`rules[${i}].conditions must be an array`);
      if (!r.action || typeof r.action !== "object" || typeof r.action.type !== "string") out.push(`rules[${i}].action must be a tagged object with type`);
      for (const c of r.conditions || []) if (!c || typeof c.type !== "string") out.push(`rules[${i}] has a condition without type`);
      const extra = Object.keys(r).filter((k) => !["conditions", "action"].includes(k));
      if (extra.length) out.push(`rules[${i}] has keys outside {conditions, action}: ${extra.join(", ")} (law 16d: no flat triple)`);
    });
    return out;
  }
  function deepEqualPayload(a, b) {
    if (a === b) return true;
    if (typeof a === "number" && typeof b === "number") return Number.isNaN(a) && Number.isNaN(b);
    if (a instanceof Date || b instanceof Date) {
      return a instanceof Date && b instanceof Date && a.getTime() === b.getTime();
    }
    if (Array.isArray(a) || Array.isArray(b)) {
      if (!Array.isArray(a) || !Array.isArray(b) || a.length !== b.length) return false;
      return a.every((x, i) => deepEqualPayload(x, b[i]));
    }
    if (a && b && typeof a === "object" && typeof b === "object") {
      const ka = definedKeys(a);
      if (ka.length !== definedKeys(b).length) return false;
      return ka.every((k) => b[k] !== void 0 && deepEqualPayload(a[k], b[k]));
    }
    return false;
  }
  var definedKeys = (o) => Object.keys(o).filter((k) => o[k] !== void 0);
  function diffAsserted(entity, asserted, live) {
    if (isDungeonEntity(entity)) return dungeonDiffs(asserted, live ? live.content : void 0);
    if (entity === "petSpecies") {
      asserted = normalizeSpecies(asserted);
      live = live && normalizeSpecies(live);
    }
    const diffs = [];
    for (const k of Object.keys(asserted)) {
      if (SERVER_OWNED.includes(k)) continue;
      if (entity === "ai" && ["rules", "includeDefaultRules"].includes(k)) continue;
      if (entity === "ai" && AI_STRIPPED_OK.includes(k)) continue;
      if (k === "hidden" && HIDDENLESS.includes(entity)) continue;
      if (entity === "ai" && k === "jutsus") {
        const l2 = Array.isArray(live?.jutsus) ? live.jutsus.map((r) => typeof r === "string" ? r : r.jutsuId ?? r.id) : [];
        const s2 = (asserted.jutsus ?? []).map((j) => typeof j === "string" ? j : j?.jutsuId ?? j?.id);
        if (JSON.stringify([...s2].sort()) !== JSON.stringify([...l2].sort())) diffs.push({ key: k, sent: s2, live: l2 });
        continue;
      }
      if (entity === "ai" && k === "items") {
        const lm =  new Map();
        if (Array.isArray(live?.items)) for (const r of live.items) {
          if (typeof r === "string") lm.set(r, null);
          else if (r) lm.set(r.itemId ?? r.id, r.dropChancePerc ?? null);
        }
        const sm =  new Map();
        for (const t of asserted.items ?? []) {
          if (typeof t === "string") sm.set(t, null);
          else if (t && Array.isArray(t.ids)) for (const id2 of t.ids) sm.set(id2, t.number == null ? null : Number(t.number));
          else if (t) sm.set(t.itemId ?? t.id, t.number == null ? null : Number(t.number));
        }
        const l2 = [...lm.keys()].filter(Boolean), s2 = [...sm.keys()].filter(Boolean);
        const chanceDrift = s2.some((id2) => sm.get(id2) != null && lm.has(id2) && lm.get(id2) != null && Number(lm.get(id2)) !== sm.get(id2));
        if (chanceDrift) diffs.push({ key: "items.dropChancePerc", sent: Object.fromEntries(sm), live: Object.fromEntries(lm) });
        if (JSON.stringify([...s2].sort()) !== JSON.stringify([...l2].sort())) diffs.push({ key: k, sent: s2, live: l2 });
        continue;
      }
      const s = asserted[k], l = live ? live[k] : void 0;
      if (entity === "skillTree" && k === "effects") {
        if (!deepEqualPayload(s, l)) diffs.push({ key: k, sent: s, live: l });
        continue;
      }
      if (!eqLoose(s, l, entity)) diffs.push({ key: k, sent: s, live: l });
    }
    return diffs;
  }
  function eqLoose(a, b, entity) {
    if (a === b) return true;
    if (a === "" && b == null || a == null && b === "") return true;
    if (a instanceof Date || b instanceof Date) return new Date(a).getTime() === new Date(b).getTime();
    if (typeof a === "number" && typeof b === "number") return entity === "ai" ? Math.abs(a - b) <= 0.5 : a === b;
    if (Array.isArray(a) && Array.isArray(b)) return a.length === b.length && a.every((x, i) => eqLoose(x, b[i], entity));
    if (a && b && typeof a === "object" && typeof b === "object") {
      const ka = Object.keys(a);
      return ka.every((k) => eqLoose(a[k], b[k], entity));
    }
    return false;
  }

  var UNRESOLVED =  new Set(["SENT", "ORPHANED", "CONFIRMED"]);
  function unresolvedBloodrightJob(journal, bloodlineId, exceptJobId = null) {
    if (!bloodlineId) return null;
    if (!journal || typeof journal.listJobs !== "function") throw new Error("Bloodright import requires the persistent journal");
    return journal.listJobs().find((job) => job.jobId !== exceptJobId && (job.bloodrightImport?.bloodlineId === bloodlineId || job.items.some((it) => it.entity === "skillTree" && it.srcId?.startsWith(`br:${bloodlineId}:`))) && job.items.some((it) => UNRESOLVED.has(it.state))) ?? null;
  }
  function assertBloodrightAvailable(journal, bloodlineId) {
    const job = unresolvedBloodrightJob(journal, bloodlineId);
    if (job) throw new Error(`unresolved Bloodright job ${job.jobId}: resume or resolve its pending writes before preparing another import for this bloodline`);
  }

  var IDMAP_KEY = "tnr_bk_idmap_v1";
  var GH_KEY = "tnr_bk_gh_v1";
  function readJson2(storage, key, fallback) {
    const raw = storage.getItem(key);
    if (raw == null || raw === "") return fallback;
    let v;
    try {
      v = JSON.parse(raw);
    } catch {
      v = void 0;
    }
    if (!v || typeof v !== "object" || Array.isArray(v)) {
      try {
        storage.setItem(key + ".corrupt", raw);
      } catch {
      }
      return fallback;
    }
    return v;
  }
  function readIdmap(storage) {
    return readJson2(storage, IDMAP_KEY, {});
  }
  function writeIdmap(storage, idmap) {
    storage.setItem(IDMAP_KEY, JSON.stringify(idmap));
  }
  function readGh(storage) {
    return readJson2(storage, GH_KEY, {});
  }
  function writeGh(storage, gh) {
    storage.setItem(GH_KEY, JSON.stringify(gh));
  }

  var IMG_NAME_RE = /^[A-Za-z0-9_.\-]+$/;
  var COMMIT_RE = /^[0-9a-f]{40}$/;
  var SHA256_RE = /^[0-9a-f]{64}$/;
  var SEGMENT_RE = /^[A-Za-z0-9._-]+$/;
  var EXT_MIME = Object.freeze({
    webp: "image/webp",
    png: "image/png",
    jpg: "image/jpeg",
    jpeg: "image/jpeg",
    gif: "image/gif",
    avif: "image/avif"
  });
  var extOf = (n) => {
    const m = /\.([A-Za-z0-9]+)$/.exec(String(n ?? ""));
    return m ? m[1].toLowerCase() : null;
  };
  var mimeOf = (n) => EXT_MIME[extOf(n)] ?? "application/octet-stream";
  function toHex(buf) {
    const bytes = buf instanceof Uint8Array ? buf : new Uint8Array(buf);
    let out = "";
    for (let i = 0; i < bytes.length; i++) out += bytes[i].toString(16).padStart(2, "0");
    return out;
  }
  function pathProblem(path) {
    if (typeof path !== "string" || !path) return "path must be a non-empty string";
    if (path.length > 255) return "path is longer than 255 characters";
    if (path.includes("\\")) return "path contains a backslash";
    if (/^[A-Za-z][A-Za-z0-9+.-]*:/.test(path)) return "path looks like a URL, not a repository path";
    if (path.startsWith("/")) return "path must be repository-relative (no leading slash)";
    const segments = path.split("/");
    for (const s of segments) {
      if (!s) return "path has an empty segment";
      if (s === "." || s === "..") return `path segment ${JSON.stringify(s)} is not allowed`;
      if (!SEGMENT_RE.test(s)) return `path segment ${JSON.stringify(s)} has characters outside [A-Za-z0-9._-]`;
    }
    return null;
  }
  function normalizeImagePack(raw, { imgSizes = {}, names = [] } = {}) {
    const errors = [], warnings = [];
    if (raw === void 0 || raw === null) return { pack: null, errors, warnings };
    if (typeof raw !== "object" || Array.isArray(raw)) {
      errors.push("imagePack must be an object {ref, files}");
      return { pack: null, errors, warnings };
    }
    const ref = raw.ref;
    if (typeof ref !== "string" || !COMMIT_RE.test(ref)) {
      errors.push(`imagePack.ref must be a 40-hex commit sha (an immutable commit, not a branch or tag), got ${JSON.stringify(ref)}`);
    }
    const rawFiles = raw.files;
    if (!rawFiles || typeof rawFiles !== "object" || Array.isArray(rawFiles)) {
      errors.push("imagePack.files must be an object keyed by the logical @img filename");
      return { pack: null, errors, warnings };
    }
    const referenced = new Set(names);
    const files = {};
    for (const name of Object.keys(rawFiles).sort()) {
      const where = `imagePack.files[${JSON.stringify(name)}]`;
      const e = rawFiles[name];
      if (!IMG_NAME_RE.test(name)) {
        errors.push(`${where}: ${JSON.stringify(name)} is not a legal @img filename`);
        continue;
      }
      if (!e || typeof e !== "object" || Array.isArray(e)) {
        errors.push(`${where} must be an object {path, sha256, bytes}`);
        continue;
      }
      const problem = pathProblem(e.path);
      if (problem) {
        errors.push(`${where}: ${problem}`);
        continue;
      }
      if (typeof e.sha256 !== "string" || !SHA256_RE.test(e.sha256)) {
        errors.push(`${where}.sha256 must be 64 lowercase hex characters, got ${JSON.stringify(e.sha256)}`);
        continue;
      }
      if (!Number.isInteger(e.bytes) || e.bytes <= 0) {
        errors.push(`${where}.bytes must be a positive integer, got ${JSON.stringify(e.bytes)}`);
        continue;
      }
      if (extOf(e.path) !== extOf(name)) {
        errors.push(`${where}: repository file is a ${extOf(e.path) ?? "(no extension)"} but the @img name is a ${extOf(name) ?? "(no extension)"}; @img resolves by exact filename and the extension decides the upload's MIME`);
        continue;
      }
      const ledger = Object.prototype.hasOwnProperty.call(imgSizes, name) ? Number(imgSizes[name]) : null;
      if (ledger == null || !Number.isFinite(ledger)) {
        errors.push(`${where}: no imgSizes entry for ${name}; a pack entry must agree with the manifest byte ledger (L17)`);
        continue;
      }
      if (ledger !== e.bytes) {
        errors.push(`${where}.bytes is ${e.bytes} but imgSizes says ${name} is ${ledger}; the manifest contradicts itself about which file this is`);
        continue;
      }
      if (!referenced.has(name)) {
        warnings.push(`imagePack binds ${name}, which no @img reference in this manifest uses; it will not be fetched`);
      }
      files[name] = { path: e.path, sha256: e.sha256, bytes: e.bytes };
    }
    if (!Object.keys(files).length && !errors.length) errors.push("imagePack.files is empty; remove the key instead");
    if (errors.length) return { pack: null, errors, warnings };
    return { pack: { ref, files }, errors, warnings };
  }
  function packBinds(pack, name) {
    return !!(pack && pack.files && Object.prototype.hasOwnProperty.call(pack.files, name));
  }
  function packWork(pack, names) {
    if (!pack) return [];
    return [...new Set(names ?? [])].filter((n) => packBinds(pack, n)).sort().map((name) => ({ name, ref: pack.ref, ...pack.files[name] }));
  }
  function unboundNames(pack, names) {
    return [...new Set(names ?? [])].filter((n) => !packBinds(pack, n));
  }

  function catalogRecipe(e, label) {
    return {
      create: { path: e + ".create", input: () => void 0 },
      get: e + ".get",
      update: e + ".update",
      names: e + ".getAllNames",
      idKey: "id",
      nameKey: "name",
      placeholder: (id2) => `New ${label} - ${id2}`,
      cacheEntity: e
    };
  }
  var RECIPES = Object.freeze({
    skillTree: {
      create: { path: "skillTree.create", input: (d) => ({ bloodlineId: d.bloodlineId }) },
      get: "skillTree.get",
      update: "skillTree.update",
      names: "skillTree.getAll",
      idKey: "id",
      nameKey: "name",
      placeholder: (id2) => `New Skill - ${id2}`,
      cacheEntity: "skillTree"
    },
    skillTreeFolder: {
      create: { path: "skillTree.createFolder", input: (d) => d },
      oneStep: true,
      get: "skillTree.getAllFolders",
      update: "skillTree.updateFolder",
      names: "skillTree.getAllFolders",
      idKey: "id",
      nameKey: "name",
      cacheEntity: "skillTree"
    },
    jutsu: {
      create: { path: "jutsu.create", input: () => void 0 },
      get: "jutsu.get",
      update: "jutsu.update",
      names: "jutsu.getAllNames",
      idKey: "id",
      nameKey: "name",
      placeholder: (id2) => `New Jutsu - ${id2}`,
      cacheEntity: "jutsu"
    },
    item: {
      create: { path: "item.create", input: (d) => ({ type: d.itemType ?? "CONSUMABLE" }) },
      get: "item.get",
      update: "item.update",
      names: "item.getAllNames",
      idKey: "id",
      nameKey: "name",
      placeholder: (id2) => `New Item - ${id2}`,
      cacheEntity: "item"
    },
    bloodline: {
      create: { path: "bloodline.create", input: () => void 0 },
      get: "bloodline.get",
      update: "bloodline.update",
      names: "bloodline.getAllNames",
      idKey: "id",
      nameKey: "name",
      placeholder: (id2) => `New Bloodline - ${id2}`,
      cacheEntity: "bloodline"
    },
    asset: {
      create: { path: "gameAsset.create", input: () => void 0 },
      get: "gameAsset.get",
      update: "gameAsset.update",
      names: "gameAsset.getAllNames",
      idKey: "id",
      nameKey: "name",
      placeholder: () => "Placeholder",
      cacheEntity: "asset",
      placeholderIsAnonymous: true
    },
    quest: {
      create: { path: "quests.create", input: () => void 0 },
      get: "quests.get",
      update: "quests.update",
      names: "quests.getAllNames",
      idKey: "id",
      nameKey: "name",
      placeholder: (id2) => `New Quest - ${id2}`,
      cacheEntity: "quest"
    },
    ai: {
      create: { path: "profile.create", input: () => void 0 },
      get: "profile.getAi",
      update: "profile.updateAi",
      names: "profile.getAllAiNames",
      idKey: "userId",
      nameKey: "username",
      placeholder: (id2) => `New AI - ${id2}`,
      cacheEntity: "ai"
    },
    dungeon: {
      create: { path: "coop.dungeon.save", input: (d) => ({ content: d }) },
      oneStep: true,
      createdId: (data) => data && data.id,
      get: "coop.dungeon.getAll",
      update: "coop.dungeon.save",
      names: "coop.dungeon.getAll",
      updateInput: (id2, payload) => ({ id: id2, content: payload }),
      idKey: "id",
      nameKey: "name",
      nameOf: dungeonName,
      cacheEntity: "dungeon"
    },
    petSpecies: {
      create: { path: "petSpecies.create", input: petSpeciesPayload },
      oneStep: true,
      get: "petSpecies.get",
      update: "petSpecies.update",
      names: "petSpecies.getAll",
      idKey: "id",
      nameKey: "name",
      cacheEntity: "petSpecies"
    },
    badge: catalogRecipe("badge", "Badge"),
    title: catalogRecipe("title", "Title"),
    aiProfile: {
      get: "profile.getAi",
      names: "profile.getAllAiNames",
      idKey: "userId",
      nameKey: "username",
      cacheEntity: "ai",
      profileGet: "ai.getAiProfile",
      profileUpdate: "ai.updateAiProfile",
      profileToggle: "ai.toggleAiProfile"
    }
  });
  function recipeRows(rc, data) {
    const rows = Array.isArray(data) ? data : data && Array.isArray(data.data) ? data.data : [];
    return rc.row ? rows.map(rc.row) : rows;
  }
  var rowName = (rc, r) => rc.nameOf ? rc.nameOf(r) : r?.[rc.nameKey];
  function updateInput(rc, id2, payload) {
    return rc.updateInput ? rc.updateInput(id2, payload) : { id: id2, data: payload };
  }
  function recipe(entity) {
    const r = RECIPES[entity];
    if (!r) throw new Error("no recipe for entity " + entity);
    return r;
  }
  function mergeForUpdate(entity, live, data, fields) {
    if (entity === "ai") return mergeAi(live, data);
    if (entity === "dungeon") return mergeDungeon(live, data);
    const src = { ...live ?? {}, ...data };
    if (!fields) return src;
    const out = {};
    for (const k of fields) if (src[k] !== void 0) out[k] = src[k];
    if (entity === "skillTreeFolder" && out.description == null) out.description = "";
    return out;
  }
  var AI_OMIT =  new Set([
    ...AI_OMITTED,
    "rules",
    "includeDefaultRules"
  ]);
  function mergeAi(live, data) {
    const out = {};
    if (live) {
      for (const [k, v] of Object.entries(live)) if (!AI_OMIT.has(k)) out[k] = v;
    }
    if (live && Array.isArray(live.jutsus)) out.jutsus = live.jutsus.map((r) => typeof r === "string" ? r : r.jutsuId ?? r.id).filter(Boolean);
    if (live && Array.isArray(live.items)) {
      out.items = live.items.map((r) => typeof r === "string" ? { ids: [r], number: 0 } : r && Array.isArray(r.ids) ? r : r ? { ids: [r.itemId ?? r.id].filter(Boolean), number: r.dropChancePerc ?? r.number ?? 0 } : null).filter((x) => x && x.ids.length);
    }
    for (const [k, v] of Object.entries(data)) if (!["rules", "includeDefaultRules"].includes(k)) out[k] = v;
    if (Array.isArray(out.jutsus)) out.jutsus = out.jutsus.map((j) => typeof j === "string" ? j : j && (j.jutsuId || j.id)).filter(Boolean);
    if (Array.isArray(out.items)) out.items = out.items.map((t) => typeof t === "string" ? { ids: [t], number: 0 } : t && Array.isArray(t.ids) ? t : t ? { ids: [t.itemId || t.id].filter(Boolean), number: t.number ?? t.dropChancePerc ?? 0 } : null).filter((x) => x && x.ids.length);
    out.isAi = true;
    if (out.userId == null && live && live.userId) out.userId = live.userId;
    return out;
  }

  var REF_RE = /^@(jutsu|ai|scene|item|quest|bloodline|img|skillTree|skillTreeFolder|petSpecies|badge|title):(.+)$/;
  var DOUBLED_RE = /^@\w+:@\w+:/;
  function collectRefs(o, out = [], path = "") {
    if (Array.isArray(o)) o.forEach((x, i) => collectRefs(x, out, `${path}[${i}]`));
    else if (o && typeof o === "object") for (const k of Object.keys(o)) collectRefs(o[k], out, path ? `${path}.${k}` : k);
    else if (typeof o === "string") {
      if (DOUBLED_RE.test(o)) out.push({ pfx: "DOUBLED", key: o, path });
      else {
        const m = o.match(REF_RE);
        if (m) out.push({ pfx: m[1], key: m[2], path });
      }
    }
    return out;
  }
  function resolveRefs(o, lookup) {
    const unresolved = [];
    const walk = (v, path) => {
      if (Array.isArray(v)) return v.map((x, i) => walk(x, `${path}[${i}]`));
      if (v && typeof v === "object") {
        const n = {};
        for (const k of Object.keys(v)) n[k] = walk(v[k], path ? `${path}.${k}` : k);
        return n;
      }
      if (typeof v === "string") {
        if (DOUBLED_RE.test(v)) {
          unresolved.push({ pfx: "DOUBLED", key: v, path });
          return v;
        }
        const m = v.match(REF_RE);
        if (m) {
          const r = lookup(m[1], m[2]);
          if (r === void 0 || r === null || r === "") {
            unresolved.push({ pfx: m[1], key: m[2], path });
            return v;
          }
          return r;
        }
      }
      return v;
    };
    return { value: walk(o, ""), unresolved };
  }

  var b_DATA_pool_default = JSON.parse(`{"_meta":{"source":"32_REGISTRY_shared_ai_pool.md","generated":"2026-08-26","purpose":"Machine-readable pool. Reference kits by CODE; the tooling resolves id, range, gate (range+1), AP and cooldown. Kills id transcription and gate arithmetic as error classes.","ap_economy":"round = 100 AP. attacks 60, stances 40. one attack + one stance = a full round."},"records":{"A1":{"name":"Cleaving Line","id":"brzGw6WgHsrFPkL9JWGir","target":"r4","range":4,"gate":5,"cooldown":4,"ap":60,"effects":["damage 50"]},"A2":{"name":"Shattering Ring","id":"muGmYnLm8mWFrwoU4zsOE","target":"r3","range":3,"gate":4,"cooldown":4,"ap":60,"effects":["damage 50"]},"A3":{"name":"Erupting Ground","id":"jBRyl7F4UjTyxG5nnzLqj","target":"r3","range":3,"gate":4,"cooldown":5,"ap":60,"effects":["damage 55"]},"B01":{"name":"Cataclysm Fist","id":"I66lzvVHf8v4thxR6tEJn","target":"r5","range":5,"gate":6,"cooldown":8,"ap":60,"effects":["damage 70"]},"B02":{"name":"Annihilating Wave","id":"ZvPl6uyJfwF5EjmLHouQR","target":"r5","range":5,"gate":6,"cooldown":8,"ap":60,"effects":["damage 70"]},"B03":{"name":"Sovereign Undertow","id":"nOYLPmN3TXj6wEe_oE6HQ","target":"r5","range":5,"gate":6,"cooldown":6,"ap":60,"effects":["redirection 3"]},"B04":{"name":"Executioner Seal","id":"tRwJPlTZK9YSUV_0AacID","target":"r5","range":5,"gate":6,"cooldown":12,"ap":60,"effects":["onehitkill 100"]},"B05":{"name":"Devouring Grasp","id":"lft52q7DE_JjhR7PKXimB","target":"r5","range":5,"gate":6,"cooldown":6,"ap":60,"effects":["damage 60","drain 25/2r"]},"B06":{"name":"Split Image","id":"LQ26G2ANWkbTRL7Ry__F0","target":"ground","range":null,"gate":null,"cooldown":6,"ap":60,"effects":["clone 100/3r"]},"B07":{"name":"Stolen Form","id":"VuFuBtE7h5B1nnA2J1lFZ","target":"r4","range":4,"gate":5,"cooldown":6,"ap":60,"effects":["copy 100/3r"]},"B08":{"name":"Tempo Fracture","id":"ecRoSDPCDjO7zH-VBaFyY","target":"r4","range":4,"gate":5,"cooldown":8,"ap":60,"effects":["timecompression 100/2r"]},"B09":{"name":"Veilstep","id":"IBjVpLutojh3m9PRnIce-","target":"self","range":null,"gate":null,"cooldown":6,"ap":40,"effects":["stealth 100/2r"]},"B10":{"name":"Sovereign Ascendance","id":"yDznlfsnPaOSFtdjfCyTZ","target":"self","range":null,"gate":null,"cooldown":10,"ap":40,"effects":["increasedamagegiven 60/3r","increasedamagegiven 60/3r","decreasedamagetaken 60/3r"]},"B11":{"name":"Sovereign Malediction","id":"pJXJUSvq2kZU-tmgC12FL","target":"r4","range":4,"gate":5,"cooldown":10,"ap":60,"effects":["seal 100/2r","increasedamagetaken 60/3r","afterburn 60/3r"]},"B12":{"name":"Sovereign Ruin","id":"-M_BxzqB937XCdD1IMWW0","target":"r4","range":4,"gate":5,"cooldown":10,"ap":60,"effects":["decreasedamagegiven 60/3r","decreasedamagegiven 60/3r","decreaseheal 60/3r"]},"B13":{"name":"Hexweave","id":"_JRHgRL8pfUvt_-q1Xa3H","target":"r4","range":4,"gate":5,"cooldown":8,"ap":60,"effects":["damage 40","increasedamagetaken 40/3r","decreaseheal 60/3r","decreasestat 15/3r"]},"B14":{"name":"Cataclysm Detonation","id":"o-4SCAhJ4LHdCwcBDgJrV","target":"r5","range":5,"gate":6,"cooldown":8,"ap":60,"effects":["damage 85"]},"B15":{"name":"Feast of Marrow","id":"ubwtVj1o9q6VQ6VxOczxt","target":"r5","range":5,"gate":6,"cooldown":8,"ap":60,"effects":["damage 50","drain 100/2r"]},"B16":{"name":"Sovereign Fetters","id":"RPdeeWhFI5AIUUpJXwUlf","target":"r5","range":5,"gate":6,"cooldown":10,"ap":60,"effects":["damage 60","stun 100/2r","seal 100/2r"]},"B17":{"name":"Worldbreaker Chorus","id":"LisNuMJ2gncEByAxG6QPI","target":"r5","range":5,"gate":6,"cooldown":10,"ap":60,"effects":["damage 70","stun 100/2r"]},"B18":{"name":"Apex Hunger","id":"w4F7-w5ubgKsqYPBPvRuV","target":"self","range":null,"gate":null,"cooldown":6,"ap":40,"effects":["increasedamagegiven 60/99r","increasestat 25/99r"]},"B19":{"name":"Warrior's Poise","id":"taxbZNdm1Q7YL5AxaRssW","target":"self","range":null,"gate":null,"cooldown":5,"ap":40,"effects":["increasedamagegiven 30/3r","decreasedamagetaken 30/3r"]},"B20":{"name":"Surging Overflow","id":"AicYoMMpZmHAykb_5hYtY","target":"self","range":null,"gate":null,"cooldown":5,"ap":40,"effects":["increasedamagegiven 30/3r","increasestat 25/3r"]},"B21":{"name":"Hushed Hours","id":"cZrZDI-A4fL324nX1CGss","target":"self","range":null,"gate":null,"cooldown":5,"ap":40,"effects":["absorb 20/3r","increasedamagegiven 25/3r"]},"B22":{"name":"Compression Barrier","id":"6UE5jC71Y6nRjobkJ-UTV","target":"self","range":null,"gate":null,"cooldown":5,"ap":40,"effects":["absorb 20/3r","decreasedamagetaken 25/3r"]},"B23":{"name":"Bulwark Charge","id":"S_ix-gZcXi6RirSVpSLV0","target":"self","range":null,"gate":null,"cooldown":6,"ap":40,"effects":["increasedamagegiven 25/3r","shield 100/2r"]},"B24":{"name":"Veilstrike","id":"yOgwN1WGkwNL9qMImc9aY","target":"self","range":null,"gate":null,"cooldown":8,"ap":40,"effects":["stealth 100/1r","increasedamagegiven 60/3r","decreasedamagetaken 50/3r","heal 25"]},"B26":{"name":"Braced Strike","id":"WvLCyGsPCKSDYl6-e_D9o","target":"r5","range":5,"gate":6,"cooldown":5,"ap":60,"effects":["damage 55","decreasedamagetaken 30/2r"]},"B27":{"name":"Scorching Rend","id":"Uou0sCjZ1rwiMJZ-JWEI_","target":"r5","range":5,"gate":6,"cooldown":6,"ap":60,"effects":["damage 55","wound 15/2r","afterburn 25/2r"]},"B28":{"name":"Recoil Slam","id":"ElSK-RCrLjddEUm76FZrs","target":"r5","range":5,"gate":6,"cooldown":5,"ap":60,"effects":["damage 75","recoil 15"]},"B29":{"name":"Devouring Wave","id":"-45phqE2baTGC--lNSEx9","target":"r5","range":5,"gate":6,"cooldown":6,"ap":60,"effects":["damage 55","absorb 15/2r"]},"B30":{"name":"Suppressing Roar","id":"vWaGTnYOwiTiaMQW10y6A","target":"r5","range":5,"gate":6,"cooldown":8,"ap":60,"effects":["damage 45","decreasedamagegiven 30/2r","stun 100/1r"]},"B31":{"name":"Rallying Spiral","id":"tq_kaS3nJ4Rv4hDRRJJ6p","target":"r3","range":3,"gate":4,"cooldown":8,"ap":40,"effects":["decreasedamagetaken 25/3r","increasedamagegiven 25/3r"]},"B32":{"name":"Nullifying Wave","id":"JWZYiHKPNwYziWEFjw4Fn","target":"r5","range":5,"gate":6,"cooldown":8,"ap":60,"effects":["clear 100"]},"B33":{"name":"Piercing Judgment","id":"OyswJoalfNpmz7FsA8Hd8","target":"r5","range":5,"gate":6,"cooldown":7,"ap":60,"effects":["pierce 55","increasedamagetaken 25/2r"]},"B34":{"name":"Mirror Edge","id":"AEeRf7i9215twJ_iEugZT","target":"r5","range":5,"gate":6,"cooldown":5,"ap":60,"effects":["damage 50","reflect 30/2r"]},"B35":{"name":"Reaping Strike","id":"fuPRuLJ0vcBqSjrqdMi7o","target":"r5","range":5,"gate":6,"cooldown":5,"ap":60,"effects":["damage 50","heal 15"]},"B36":{"name":"Withering Weave","id":"-kMekZ4rR64vjMF2Jc4pe","target":"r4","range":4,"gate":5,"cooldown":5,"ap":60,"effects":["damage 30","increasedamagetaken 15/2r","decreaseheal 20/2r"]},"B37":{"name":"Fighter's Poise","id":"P0GcazZ6yvULoH4kGuh4T","target":"self","range":null,"gate":null,"cooldown":4,"ap":40,"effects":["increasedamagegiven 15/2r","decreasedamagetaken 15/2r"]},"B38":{"name":"Minor Overflow","id":"oQo27NtvRS29CABHGXP94","target":"self","range":null,"gate":null,"cooldown":4,"ap":40,"effects":["increasedamagegiven 15/2r","increasestat 12/2r"]},"B39":{"name":"Light Barrier","id":"05rH3kZNXbtFq9a9iRl-W","target":"self","range":null,"gate":null,"cooldown":5,"ap":40,"effects":["shield 100/2r"]},"EA01":{"name":"Gale Bolt","id":"SJwW0b5tO4PuBhNrLJIR2","target":"r5","range":5,"gate":6,"cooldown":3,"ap":60,"effects":["damage 45"]},"EA02":{"name":"Tempest Breaker","id":"d00wewEL2x6V3Th5gS0dh","target":"r3","range":3,"gate":4,"cooldown":5,"ap":60,"effects":["damage 60","redirection 3"]},"EA03":{"name":"Windlash Focus","id":"_9k7kSYUgMtB-AEFgRly5","target":"self","range":null,"gate":null,"cooldown":4,"ap":40,"effects":["increasedamagegiven 20/2r"]},"EA04":{"name":"Zephyr Lance","id":"A5HrHSzx4J3WM4Fln8Lbf","target":"r5","range":5,"gate":6,"cooldown":6,"ap":60,"effects":["pierce 60"]},"EE01":{"name":"Shale Bolt","id":"qymEx2jhCwmSZPJOnPuRD","target":"r5","range":5,"gate":6,"cooldown":3,"ap":60,"effects":["damage 45"]},"EE02":{"name":"Bedrock Breaker","id":"0qhjpBMtG9HSWoOWztAB1","target":"r3","range":3,"gate":4,"cooldown":5,"ap":60,"effects":["damage 60","moveprevent 100/2r","stun 100/1r"]},"EE03":{"name":"Stoneward","id":"V3WrfQ3pB-eCq2hojsxWe","target":"self","range":null,"gate":null,"cooldown":4,"ap":40,"effects":["decreasedamagetaken 20/2r"]},"EF01":{"name":"Cinder Bolt","id":"Sic286tbCpCjwaic0EX5q","target":"r5","range":5,"gate":6,"cooldown":3,"ap":60,"effects":["damage 45"]},"EF02":{"name":"Pyre Breaker","id":"EJOCWmrrUnECI2MikM8ho","target":"r3","range":3,"gate":4,"cooldown":5,"ap":60,"effects":["damage 60","wound 15/2r"]},"EF03":{"name":"Emberwake","id":"bLBu130QaqCaDlSIcEmUD","target":"r5","range":5,"gate":6,"cooldown":4,"ap":60,"effects":["damage 40","afterburn 20/2r"]},"EL01":{"name":"Arc Bolt","id":"Fkfa_oRbCPPOnBPPHlikF","target":"r5","range":5,"gate":6,"cooldown":3,"ap":60,"effects":["damage 45"]},"EL02":{"name":"Storm Breaker Volt","id":"hxNWprk1AYwH0OVX0rxaR","target":"r3","range":3,"gate":4,"cooldown":5,"ap":60,"effects":["damage 60","reflect 20/2r"]},"EL03":{"name":"Static Jolt","id":"3hMzYwiV8VOEx2XOm1CJe","target":"r5","range":5,"gate":6,"cooldown":4,"ap":60,"effects":["damage 40","stun 100/1r"]},"EL04":{"name":"Ion Lance","id":"xGVqWSX93hXZgfmlKZODp","target":"r5","range":5,"gate":6,"cooldown":6,"ap":60,"effects":["pierce 60"]},"EW01":{"name":"Tide Bolt","id":"UnQKfwq_JoRVu10aTX6Uv","target":"r5","range":5,"gate":6,"cooldown":3,"ap":60,"effects":["damage 45"]},"EW02":{"name":"Deluge Breaker","id":"UAgYZvo_7DUtmBsBAaAar","target":"r3","range":3,"gate":4,"cooldown":5,"ap":60,"effects":["damage 60","shield 100/2r"]},"EW03":{"name":"Springguard","id":"mOA1hXNf4CcuwOhnnN7ZK","target":"self","range":null,"gate":null,"cooldown":4,"ap":40,"effects":["absorb 20/2r"]},"S01":{"name":"Heavy Strike","id":"pUrUJX8Jml7fUIBXKsPwv","target":"r3","range":3,"gate":4,"cooldown":5,"ap":60,"effects":["damage 60"]},"S02":{"name":"Quick Strike","id":"FeYnH7BBw_usnc1K-TM-J","target":"r3","range":3,"gate":4,"cooldown":3,"ap":60,"effects":["damage 45"]},"S03":{"name":"Lunging Strike","id":"_nUaGHlWhn3-U0xbxJHFw","target":"r4","range":4,"gate":5,"cooldown":4,"ap":60,"effects":["damage 45"]},"S04":{"name":"Opening Strike","id":"Cw51Wm_Uy0GiIkiEjlQtn","target":"r4","range":4,"gate":5,"cooldown":3,"ap":60,"effects":["damage 40","increasedamagetaken 15/2r"]},"S06":{"name":"Twin Shot","id":"3v9c1SHlD2GLPF2HW1_Sc","target":"r5","range":5,"gate":6,"cooldown":3,"ap":60,"effects":["damage 45"]},"S07":{"name":"Rapid Fire","id":"Nrxc8m9utE9qaD_gWpLgf","target":"r5","range":5,"gate":6,"cooldown":2,"ap":60,"effects":["damage 40"]},"S08":{"name":"Numbing Shot","id":"m-ur3A8TS8r5jGb84L9x7","target":"r5","range":5,"gate":6,"cooldown":4,"ap":60,"effects":["damage 40","stun 30/1r"]},"S27":{"name":"Weakening Strike","id":"YiRdVytsdxFzZtqkEDs5Q","target":"r5","range":5,"gate":6,"cooldown":4,"ap":60,"effects":["damage 40","decreasedamagegiven 20/2r"]},"S28":{"name":"Enervating Strike","id":"mpHuTrJX7EonpuW_jBunt","target":"r5","range":5,"gate":6,"cooldown":4,"ap":60,"effects":["damage 40","decreasestat 15/2r"]},"S29":{"name":"Venom Strike","id":"LiVOnYq6qHzjB0XkIIA2e","target":"r5","range":5,"gate":6,"cooldown":5,"ap":60,"effects":["damage 40","poison 20/2r"]},"S30":{"name":"Searing Strike","id":"OWAm8o12bkZUMAAHLoGLz","target":"r5","range":5,"gate":6,"cooldown":4,"ap":60,"effects":["damage 40","afterburn 20/2r"]},"S31":{"name":"Unraveling Strike","id":"1OhP0StX4VTsosWtCxhsG","target":"r3","range":3,"gate":4,"cooldown":5,"ap":60,"effects":["damage 40","clear 100"]},"S32":{"name":"Lingering Strike","id":"YD9GEwXU6LDuIC06TGzWG","target":"r5","range":5,"gate":6,"cooldown":4,"ap":60,"effects":["damage 40","cleanseprevent 100/2r"]},"S33":{"name":"Marking Volley","id":"mQ7-q8q46ry5njNVBFpGp","target":"r5","range":5,"gate":6,"cooldown":5,"ap":60,"effects":["damage 50","increasedamagetaken 15/2r"]},"S34":{"name":"Purging Stance","id":"HcAs8gBtvopPZkjP8HCC2","target":"self","range":null,"gate":null,"cooldown":5,"ap":40,"effects":["cleanse 100"]},"S35":{"name":"Second Wind","id":"STu1VHNcfgeC3x-UiQDgt","target":"self","range":null,"gate":null,"cooldown":6,"ap":40,"effects":["heal 15"]},"S36":{"name":"Warding Stance","id":"hh-FMFv67CAL10DA35K2T","target":"self","range":null,"gate":null,"cooldown":5,"ap":40,"effects":["debuffprevent 100/2r"]},"S38":{"name":"Glancing Strike","id":"u7AMx4nbPsU_ev8mfi5yG","target":"r5","range":5,"gate":6,"cooldown":3,"ap":60,"effects":["damage 12"]},"S39":{"name":"Bruising Blow","id":"Rufs-Y-FZIDooXO7g6k0F","target":"r5","range":5,"gate":6,"cooldown":4,"ap":60,"effects":["damage 25"]},"S40":{"name":"Measured Strike","id":"kkGDat1XWUxhOQ1_T5025","target":"r5","range":5,"gate":6,"cooldown":3,"ap":60,"effects":["damage 20"]},"S41":{"name":"Steady Strike","id":"fKvCGRgzGNskgFWocQCAg","target":"r5","range":5,"gate":6,"cooldown":3,"ap":60,"effects":["damage 30"]},"S42":{"name":"Forceful Strike","id":"4TM6iS8P0qgNHsFpALFhg","target":"r5","range":5,"gate":6,"cooldown":3,"ap":60,"effects":["damage 40"]},"S43":{"name":"Heavy Cut","id":"Vo8N1luCT0p48y7JzKe84","target":"r5","range":5,"gate":6,"cooldown":4,"ap":60,"effects":["damage 45"]},"S44":{"name":"Sundering Blow","id":"b7ZOgdZmhZiUbCVrmQiwH","target":"r5","range":5,"gate":6,"cooldown":4,"ap":60,"effects":["damage 50"]}}}`);

  var POOL_RECORDS = Object.freeze(b_DATA_pool_default.records ?? {});
  var POOL_BY_ID = Object.freeze(Object.fromEntries(
    Object.entries(POOL_RECORDS).map(([code, r]) => [r.id, { ...r, code }])
  ));
  var POOLCODE = /^[A-Z]{1,2}\d{1,2}$/;
  var isCode = (v) => typeof v === "string" && POOLCODE.test(v);
  function resolvePoolCodes(data) {
    if (!data || typeof data !== "object") return { data, resolved: 0 };
    let resolved = 0;
    let out = data;
    const edit = () => out === data ? out = { ...data } : out;
    if (Array.isArray(data.jutsus)) {
      const next = data.jutsus.map((j) => {
        const rec = isCode(j) ? POOL_RECORDS[j] : null;
        if (!rec) return j;
        resolved++;
        return rec.id;
      });
      if (next.some((v, i) => v !== data.jutsus[i])) edit().jutsus = next;
    }
    if (Array.isArray(data.rules)) {
      const rules = data.rules.map((r) => {
        const a = r && typeof r === "object" ? r.action : null;
        const rec = a && isCode(a.jutsu) ? POOL_RECORDS[a.jutsu] : null;
        if (!rec) return r;
        resolved++;
        const { jutsu, ...restAction } = a;
        const action = { ...restAction, jutsuId: rec.id };
        const conditions = Array.isArray(r.conditions) ? r.conditions.map((c) => c && c.type === "distance_lower_than" && c.value == null && rec.gate != null ? { ...c, value: rec.gate } : c) : r.conditions;
        return { ...r, action, conditions };
      });
      if (rules.some((v, i) => v !== data.rules[i])) edit().rules = rules;
    }
    return { data: out, resolved };
  }
  function stuckPoolCodes(data) {
    const stuck = [];
    if (!data || typeof data !== "object") return stuck;
    for (const j of Array.isArray(data.jutsus) ? data.jutsus : []) {
      if (isCode(j)) stuck.push(`jutsus: "${j}" is an unresolved pool code (not in 32b_DATA_pool.json)`);
    }
    (Array.isArray(data.rules) ? data.rules : []).forEach((r, i) => {
      const a = r && typeof r === "object" ? r.action : null;
      if (a && typeof a.jutsu === "string") stuck.push(`rules[${i}].action.jutsu = "${a.jutsu}": the server takes jutsuId; this key is dropped`);
    });
    return stuck;
  }
  function kitProblems(data) {
    const errors = [], warnings = [];
    if (!data || typeof data !== "object") return { errors, warnings };
    const equipped = (Array.isArray(data.jutsus) ? data.jutsus : []).map(String);
    const eq = new Set(equipped);
    const ap = equipped.map((id2) => POOL_BY_ID[id2]?.ap).filter((v) => typeof v === "number");
    if (ap.length >= 3 && Math.min(...ap) >= 60) {
      warnings.push("kit is all 60 AP actions and no 40 AP stance: the AI will exhaust itself (a round is 100 AP; laws 61 to 63)");
    }
    (Array.isArray(data.rules) ? data.rules : []).forEach((r, i) => {
      if (!r || typeof r !== "object") return;
      const jid = r.action && r.action.jutsuId;
      if (!jid) return;
      if (equipped.length && !eq.has(String(jid))) {
        const nm = POOL_BY_ID[jid]?.name ?? jid;
        errors.push(`rules[${i}]: fires "${nm}" but that jutsu is NOT in the AI's jutsus array. The rule is inert and the log signature is identical to a severed equip link (law 18)`);
      }
      const rec = POOL_BY_ID[jid];
      if (!rec) return;
      for (const c of Array.isArray(r.conditions) ? r.conditions : []) {
        if (!c || c.type !== "distance_lower_than") continue;
        if (rec.gate != null && c.value !== rec.gate) {
          errors.push(`rules[${i}]: ${rec.name} is range ${rec.range}, so the gate must be ${rec.gate} (range+1, law 40). Found ${c.value}. A higher gate fires out of range and can strand a player in combat`);
        }
        if (rec.range == null) {
          warnings.push(`rules[${i}]: ${rec.name} is self/ground targeted; a distance gate is meaningless on it`);
        }
      }
    });
    return { errors, warnings };
  }

  var DATE_RE = /^\d{4}-\d{1,2}-\d{1,2}$/;
  var DASH_RE = /[–—]/;
  var IMG_REF_RE = /@img:([A-Za-z0-9_.\-]+)/g;
  var AI_CREATE_REQUIRED = ["rank", "regeneration", "preferredGeneral1", "preferredGeneral2"];
  var FORMULA_TAGS =  new Set(["damage", "pierce", "wound"]);
  var PCT_TAGS =  new Set(["increasedamagegiven", "decreasedamagetaken", "increasedamagetaken"]);
  var DIRECTIONS = { redirection: ["push", "pull"], increasestat: ["offence", "defence", "both"], decreasestat: ["offence", "defence", "both"] };
  function lintManifest(manifest) {
    const errors = [], warnings = [];
    const items = manifest.items ?? [];
    const E = (it, m) => errors.push(`item ${it.idx} (${it.name}): ${m}`);
    const W = (it, m) => warnings.push(`item ${it.idx} (${it.name}): ${m}`);
    const wrapped =  new Set();
    for (const it of items) {
      if (it.entity !== "item") continue;
      for (const f of Array.isArray(it.data.effects) ? it.data.effects : []) {
        if (!f || f.type !== "injectjutsus") continue;
        for (const m of JSON.stringify(f).matchAll(/@jutsu:([A-Za-z0-9_\-]+)/g)) wrapped.add(m[1]);
      }
    }
    for (const it of items) {
      const d = it.data ?? {};
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
        const objs = d.content && Array.isArray(d.content.objectives) ? d.content.objectives : null;
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
          if (d.itemType !== void 0 && d.itemType !== "CONSUMABLE") E(it, "L18 noncombatconsumereward requires itemType CONSUMABLE");
          if (d.target !== void 0 && d.target !== "SELF") E(it, "L18 noncombatconsumereward requires item target SELF");
          if (d.method !== void 0 && d.method !== "SINGLE") E(it, "L18 noncombatconsumereward requires method SINGLE");
          if (Array.isArray(f.reward_pets) && f.reward_pets.length && f.rewardMode === "weightedCache") E(it, "PET reward_pets requires rewardMode standard");
        }
      }
      if (it.entity === "item") {
        const pets = (Array.isArray(d.effects) ? d.effects : []).reduce((n, f) => n + (f && f.type === "noncombatconsumereward" && Array.isArray(f.reward_pets) ? f.reward_pets.length : 0), 0);
        if (pets > 1) E(it, `PET an item may grant at most 1 companion (${pets} across its effects)`);
        if (pets && (d.preventBattleUsage === false || it.op === "create" && d.preventBattleUsage !== true)) E(it, "PET companion rewards require preventBattleUsage true");
      }
      for (const [tp, n] of Object.entries(pct)) {
        if (n <= 4) continue;
        let p = 1;
        for (const f of d.effects) if (f && f.type === tp && (f.calculation === "percentage" || !f.calculation)) p *= 1 + (f.power ?? 0) / 100;
        W(it, `L08 ${n} ${tp} rows: product x${p.toFixed(1)}`);
      }
    }
    const jutsuBySrc = new Map(items.filter((it) => it.entity === "jutsu" && it.srcId).map((it) => [it.srcId, it]));
    for (const it of items) {
      if (it.entity !== "petSpecies" || !Array.isArray(it.data?.defaultJutsuIds)) continue;
      for (const ref of it.data.defaultJutsuIds) {
        const j = typeof ref === "string" && ref.startsWith("@jutsu:") ? jutsuBySrc.get(ref.slice(7)) : null;
        if (!j) continue;
        if (j.op === "create") E(it, `PET default ${ref} is created hidden in this manifest; the server refuses unpublished defaults. Publish it, then set the defaults in a later manifest`);
        const lock = j.data?.requiredPetSpeciesId;
        if (lock && it.op === "create") E(it, `PET default ${ref} is species-locked; a species create accepts only unlocked PETS jutsu`);
        if (lock && it.op === "update" && !lock.startsWith("@") && lock !== it.targetId) E(it, `PET default ${ref} is locked to another species (${lock})`);
      }
    }
    for (const t of items) if (t.entity === "title" && t.data?.archived === true) {
      const ref = JSON.stringify(t.op === "create" ? "@title:" + t.srcId : t.targetId);
      for (const it of items) if (JSON.stringify(it.data ?? {}).match(/"reward_titles":\[[^\]]*\]/g)?.some((m) => m.includes(ref))) E(it, `TITLE ${ref} is archived in this manifest; the server refuses rewarding it`);
    }
    const sizes = manifest.imgSizes ?? {};
    const needed =  new Set();
    for (const m of JSON.stringify(items).matchAll(IMG_REF_RE)) if (!(m[1] in sizes)) needed.add(m[1]);
    for (const f of needed) errors.push(`L17 @img:${f} has no imgSizes byte entry`);
    return { errors, warnings };
  }
  function lintObjectives(objs, it, E, W) {
    const edges = {}, incoming = {}, wins = [];
    for (const o of objs) {
      if (!o || !o.id) continue;
      const targets = [];
      const n = o.nextObjectiveId;
      if (typeof n === "string") targets.push(n);
      else if (Array.isArray(n)) {
        for (const c of n) if (c && c.nextObjectiveId) targets.push(c.nextObjectiveId);
      }
      if (o.failObjectiveId) targets.push(o.failObjectiveId);
      edges[o.id] = targets.filter(Boolean);
      for (const t of edges[o.id]) incoming[t] = 1;
      if (o.task === "win_quest") wins.push(o.id);
      const text = (o.description ?? "") + (Array.isArray(n) ? n.map((c) => c && c.text || "").join(" ") : "");
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

  var ENTITIES = Object.freeze(["jutsu", "item", "bloodline", "asset", "quest", "ai", "aiProfile", "skillTree", "skillTreeFolder", "dungeon", "petSpecies", "badge", "title"]);
  var SLOT_TO_OP = Object.freeze({ create: "create", edit: "update", convert: "update" });
  var MAX_DUNGEON_WRITES = 30;
  var IMG_REF_SCAN = /@img:([A-Za-z0-9_.\-]+)/g;
  var PERSIST_MODES = Object.freeze(["summary", "full"]);
  var DEFAULT_PERSIST = "summary";
  var ManifestError = class extends Error {
    constructor(message, info = {}) {
      super(message);
      this.name = "ManifestError";
      Object.assign(this, info);
    }
  };
  function suggestPolicy(m, items) {
    const problems = [];
    const s = m.suggestion && typeof m.suggestion === "object" ? m.suggestion : {};
    const check = (where, x) => {
      if (x.category !== void 0 && !contract_default2.categories.includes(x.category)) problems.push(`${where}: category must be one of ${contract_default2.categories.join(", ")}`);
      if (x.title !== void 0 && (typeof x.title !== "string" || x.title.trim().length < contract_default2.titleLength.min)) problems.push(`${where}: title needs at least ${contract_default2.titleLength.min} characters`);
      if (x.rationale !== void 0 && (typeof x.rationale !== "string" || x.rationale.trim().length < contract_default2.rationaleLength.min || x.rationale.length > contract_default2.rationaleLength.max)) problems.push(`${where}: rationale needs ${contract_default2.rationaleLength.min}-${contract_default2.rationaleLength.max} characters`);
    };
    check("suggestion", s);
    if (m.bloodrightImport || m.capture?.before?.length || m.capture?.after?.length) problems.push("suggest mode is for item edits only (no Bloodright import, no captures)");
    for (const it of items) {
      const where = `item ${it.idx + 1} (${it.name})`;
      if (it.op !== "update") problems.push(`${where}: suggest mode can only change existing records (slot "edit" with a targetId)`);
      if (!contract_default2.entityTypes[it.entity]) problems.push(`${where}: ${it.entity} cannot be suggested; the review desk takes ${Object.keys(contract_default2.entityTypes).join(", ")}${contract_default2._meta.notSuggestible[it.entity] ? ` (${it.entity}: ${contract_default2._meta.notSuggestible[it.entity].split(";")[0]})` : ""}`);
      if (it.entity === "ai") {
        const dropped = Object.keys(it.data ?? {}).filter((k) => !contract_default2.aiEditableKeys.includes(k));
        if (dropped.length) problems.push(`${where}: the review desk does not take ${dropped.join(", ")} for an AI; edit them directly instead`);
      }
      if (it.suggestion) check(where, it.suggestion);
      const merged = { ...s, ...it.suggestion ?? {} };
      if (!merged.title || !merged.rationale) problems.push(`${where}: needs a suggestion title and rationale (manifest "suggestion" or the item's own)`);
    }
    if (problems.length) throw new ManifestError("suggest mode problems:\n" + problems.join("\n"), { problems });
    return { category: s.category ?? "BALANCE", title: s.title ?? null, rationale: s.rationale ?? null };
  }
  function parseManifest(source) {
    let m = source;
    if (typeof source === "string") {
      try {
        m = JSON.parse(source);
      } catch (e) {
        throw new ManifestError("manifest is not JSON: " + e.message);
      }
    }
    if (!m || typeof m !== "object" || Array.isArray(m)) throw new ManifestError("manifest must be an object");
    const raw = Array.isArray(m.items) ? m.items : Array.isArray(m.jutsu) ? m.jutsu : [];
    const rawCapture = m.capture && typeof m.capture === "object" ? { before: Array.isArray(m.capture.before) ? m.capture.before : [], after: Array.isArray(m.capture.after) ? m.capture.after : [] } : { before: [], after: [] };
    const capture = {
      before: rawCapture.before.map((c, i) => normalizeCapture(c, "before", i)),
      after: rawCapture.after.map((c, i) => normalizeCapture(c, "after", i))
    };
    if (!raw.length && !capture.before.length && !capture.after.length) throw new ManifestError("manifest has no items and no captures");
    const items = raw.map((it, i) => normalizeItem(it, i));
    const problems = [];
    const srcIds =  new Set();
    for (const it of items) {
      if (it.op === "create" && !it.srcId) problems.push(`item ${it.idx} (${it.name}): a create needs srcId`);
      if (it.op === "update" && !it.targetId) problems.push(`item ${it.idx} (${it.name}): an edit needs targetId`);
      if (it.srcId) {
        if (srcIds.has(it.srcId)) problems.push(`duplicate srcId ${it.srcId}`);
        srcIds.add(it.srcId);
      }
      if (it.entity === "aiProfile" && it.op === "create") problems.push(`item ${it.idx}: aiProfile cannot be created directly; create an ai with rules`);
      if ("refreshPackages" in it && (it.refreshPackages !== true || it.entity !== "dungeon" || it.op !== "update")) problems.push(`item ${it.idx} (${it.name}): refreshPackages is true or absent, and only on a dungeon edit`);
    }
    let poolResolved = 0;
    for (const it of items) {
      if (it.entity !== "ai" && it.entity !== "aiProfile") continue;
      const r = resolvePoolCodes(it.data);
      it.data = r.data;
      poolResolved += r.resolved;
    }
    for (const it of items) {
      if (it.entity !== "ai" && it.entity !== "aiProfile") continue;
      for (const s of stuckPoolCodes(it.data)) problems.push(`item ${it.idx} (${it.name}): ${s}`);
      for (const e of kitProblems(it.data).errors) problems.push(`item ${it.idx} (${it.name}): ${e}`);
    }
    if (m.readBack === false && items.length) {
      problems.push("readBack:false is refused on a manifest with items: a write must be read back (remove the key, or split the captures into their own manifest)");
    }
    const imgSizes = m.imgSizes && typeof m.imgSizes === "object" ? m.imgSizes : {};
    const lint = lintManifest({ items, imgSizes });
    problems.push(...lint.errors);
    const warnings = [...lint.warnings];
    const imgNames = [...new Set([...JSON.stringify(items).matchAll(IMG_REF_SCAN)].map((x) => x[1]))];
    const packed = normalizeImagePack(m.imagePack, { imgSizes, names: imgNames });
    problems.push(...packed.errors);
    warnings.push(...packed.warnings);
    for (const it of items) {
      if (it.entity !== "ai" && it.entity !== "aiProfile") continue;
      for (const w of kitProblems(it.data).warnings) warnings.push(`item ${it.idx} (${it.name}): ${w}`);
    }
    if (problems.length) throw new ManifestError("manifest problems:\n" + problems.join("\n"), { problems });
    const policy = {
      dedupNames: !!m.dedupNames,
      readBack: m.readBack !== false,
      skipPreflight: !!m.skipPreflight,
      imgSizes
    };
    if (packed.pack) policy.imagePack = packed.pack;
    const dungeonWrites = items.filter((it) => it.entity === "dungeon").length;
    if (dungeonWrites > MAX_DUNGEON_WRITES) throw new ManifestError(`${dungeonWrites} dungeon writes: coop.dungeon.save is rate-limited by the server, so a manifest carries at most ${MAX_DUNGEON_WRITES}; split it`);
    if (items.some((it) => ["skillTree", "skillTreeFolder"].includes(it.entity)) && !m.bloodrightImport) throw new ManifestError("Bloodright writes require compiler provenance; prepare the design package in Forge");
    if (m.bloodrightImport) {
      const b = m.bloodrightImport;
      if (b.version !== 1 || b.gamePin !== contract_default._meta.pin || typeof b.bloodlineId !== "string" || !b.bloodlineId || !/^[a-f0-9]{40}$/.test(b.source?.ref ?? "") || typeof b.source?.path !== "string") throw new ManifestError("invalid or incompatible Bloodright import provenance");
      if (items.some((it) => !["skillTree", "skillTreeFolder"].includes(it.entity) || !it.srcId?.startsWith(`br:${b.bloodlineId}:`) || it.entity === "skillTree" && it.data.bloodlineId !== b.bloodlineId)) throw new ManifestError("Bloodright import items must belong to their declared bloodline scope");
      if (!policy.dedupNames) throw new ManifestError("Bloodright imports require dedupNames:true");
      if (typeof b.hiddenProbeId !== "string" || !b.hiddenProbeId || !b.bindings || typeof b.bindings !== "object" || Array.isArray(b.bindings)) throw new ManifestError("Bloodright import requires hidden-probe identity and explicit bindings");
      for (const it of items) if (it.op === "update" && (!it.expected || typeof it.expected !== "object" || Array.isArray(it.expected) || b.bindings[it.srcId] !== it.targetId)) throw new ManifestError(`Bloodright edit ${it.name} requires a frozen preimage and matching binding`);
      policy.bloodrightImport = b;
    }
    if (m.mode !== void 0 && m.mode !== "write") {
      if (m.mode !== "suggest") throw new ManifestError(`mode must be "write" or "suggest", got ${JSON.stringify(m.mode)}`);
      policy.suggest = suggestPolicy(m, items);
    }
    return {
      items,
      capture,
      warnings,
      poolResolved,
      policy,
      note: typeof m._note === "string" ? m._note : null,
      skipPreflight: policy.skipPreflight,
      dedupNames: policy.dedupNames,
      readBack: policy.readBack,
      imgSizes,
      imagePack: packed.pack,
      fullCaptures: [...capture.before, ...capture.after].filter((c) => c.persist === "full").length,
      hash: manifestHash(raw, rawCapture, policy),
      bodyHash: fnv1a32(stableStringify({ items: raw, capture: rawCapture }))
    };
  }
  var DEFAULT_POLICY = Object.freeze({ dedupNames: false, readBack: true, skipPreflight: false, imgSizes: {} });
  function isDefaultPolicy(policy) {
    return stableStringify(policy) === stableStringify(DEFAULT_POLICY);
  }
  function manifestHash(raw, rawCapture, policy) {
    const body = { items: raw, capture: rawCapture };
    return fnv1a32(stableStringify(isDefaultPolicy(policy) ? body : { ...body, policy }));
  }
  function normalizeCapture(c, phase, i) {
    const where = `capture.${phase}[${i}]`;
    if (!c || typeof c !== "object" || Array.isArray(c)) throw new ManifestError("capture entry missing proc");
    const proc = c.proc || c.procedure;
    if (!proc) throw new ManifestError("capture entry missing proc");
    const persist = c.persist === void 0 || c.persist === null ? DEFAULT_PERSIST : c.persist;
    if (!PERSIST_MODES.includes(persist)) {
      throw new ManifestError(`${where} (${proc}): persist must be ${PERSIST_MODES.map((p) => JSON.stringify(p)).join(" or ")}, got ${JSON.stringify(c.persist)}`, { phase, idx: i, proc, persist: c.persist });
    }
    const input = c.input && typeof c.input === "object" && !Array.isArray(c.input) ? c.input : null;
    const id2 = input ? input.id ?? input.userId : void 0;
    if (persist === "full") {
      if (!canPersistFull(proc)) {
        throw new ManifestError(`${where} (${proc}): persist "full" is only allowed for the audited content-record point reads ${FULL_PERSIST_PATHS.join(", ")}`, { phase, idx: i, proc });
      }
      if (typeof id2 !== "string" || !id2) {
        throw new ManifestError(`${where} (${proc}): persist "full" needs input.id (or input.userId) naming one record`, { phase, idx: i, proc });
      }
    }
    return { proc, input, persist, id: typeof id2 === "string" && id2 ? id2 : null };
  }
  function normalizeItem(it, idx) {
    if (!it || typeof it !== "object") throw new ManifestError(`item ${idx} is not an object`);
    const entity = it.entity || "jutsu";
    if (!ENTITIES.includes(entity)) throw new ManifestError(`item ${idx}: unknown entity "${entity}"`, { idx, entity });
    const slot = it.slot || (it.targetId ? "edit" : "create");
    const op = SLOT_TO_OP[slot];
    if (!op) throw new ManifestError(`item ${idx}: unknown slot "${slot}"`, { idx, slot });
    const data = it.data && typeof it.data === "object" ? it.data : {};
    if (typeof it.name === "string" && op === "create" && entity !== "aiProfile") {
      const nameKey = entity === "ai" ? "username" : "name";
      if (data[nameKey] === void 0) data[nameKey] = it.name;
    }
    return {
      idx,
      entity,
      op,
      slot,
      name: typeof it.name === "string" ? it.name : data.name ?? data.username ?? `item ${idx}`,
      srcId: typeof it.srcId === "string" && it.srcId ? it.srcId : null,
      targetId: typeof it.targetId === "string" && it.targetId ? it.targetId : null,
      phase: typeof it.phase === "number" ? it.phase : null,
      data,
      ...it.expected !== void 0 ? { expected: it.expected } : {},
      ...it.reassign === true ? { reassign: true } : {},
      ...it.refreshPackages !== void 0 ? { refreshPackages: it.refreshPackages } : {},
      ...it.suggestion && typeof it.suggestion === "object" ? { suggestion: it.suggestion } : {}
    };
  }
  function planOrder(manifest, idmap = {}) {
    const bySrc = new Map(manifest.items.filter((it) => it.srcId).map((it) => [it.srcId, it]));
    const nodes = manifest.items.map((it) => {
      const refs = collectRefs({ data: it.data, targetId: it.targetId });
      const deps = [];
      for (const r of refs) {
        if (r.pfx === "img") continue;
        if (idmap[r.key] && !(r.pfx.startsWith("skillTree") && bySrc.has(r.key))) continue;
        const src = bySrc.get(r.key);
        if (!src) throw new ManifestError(`item ${it.idx} (${it.name}): @${r.pfx}:${r.key} is unknown (no srcId in this manifest, not in idmap)`, { idx: it.idx, ref: r });
        if (r.pfx.startsWith("skillTree") && src.entity !== r.pfx) throw new ManifestError(`typed reference ${r.pfx}:${r.key} points to ${src.entity}`);
        if (src.idx === it.idx) throw new ManifestError(`item ${it.idx} references itself`);
        deps.push(src.srcId);
      }
      return { it, deps };
    });
    const order = [];
    const state =  new Map();
    const byIdx = new Map(nodes.map((n) => [n.it.idx, n]));
    const sorted = [...nodes].sort((a, b) => (a.it.phase ?? 5) - (b.it.phase ?? 5) || a.it.idx - b.it.idx);
    function visit(n, stack) {
      const key = n.it.srcId ?? `#${n.it.idx}`;
      if (state.get(key) === "done") return;
      if (state.get(key) === "visiting") throw new ManifestError("ref cycle: " + [...stack, key].join(" -> "));
      state.set(key, "visiting");
      for (const d of n.deps) visit(byIdx.get(bySrc.get(d).idx), [...stack, key]);
      state.set(key, "done");
      order.push({ ...n.it, deps: n.deps });
    }
    for (const n of sorted) visit(n, []);
    return order;
  }
  function toJournalSpecs(order) {
    return order.map((it) => ({
      entity: it.entity,
      op: it.op,
      name: it.name,
      srcId: it.srcId,
      targetId: it.targetId,
      payloadHash: payloadHash({ data: it.data, targetId: it.targetId, entity: it.entity, op: it.op })
    }));
  }

  var LEASE_PREFIX = "tnr_forge_lease_v1:";
  var LEASE_TTL_MS = 3e4;
  var LeaseHeld = class extends Error {
    constructor(jobId, lease) {
      super(`job ${jobId} is being driven by another tab (heartbeat ${Math.round((Date.now() - lease.at) / 1e3)}s ago); wait ${Math.ceil(LEASE_TTL_MS / 1e3)}s or close it`);
      this.name = "LeaseHeld";
      this.lease = lease;
    }
  };
  var randomTab = () => Math.random().toString(36).slice(2, 10) + Math.random().toString(36).slice(2, 6);
  var moved = (journal, jobId, e) => new StaleItem(`job ${jobId} is ${journal.get(jobId).state}: another tab moved it (${e?.message})`);
  var Paused = class extends Error {
    constructor(reason, info = {}) {
      super(`paused: ${reason}`);
      this.name = "Paused";
      this.reason = reason;
      Object.assign(this, info);
    }
  };
  var isTransport = (e) => e instanceof NetworkError || e instanceof TransportError;
  function protectedPathsFor(order, manifest) {
    const paths =  new Set();
    const captures = manifest && manifest.capture ? [...manifest.capture.before || [], ...manifest.capture.after || []] : [];
    for (const c of captures) {
      const path = c.proc || c.procedure;
      if (path && isProtected(path)) paths.add(path);
    }
    if (manifest?.policy?.suggest) {
      paths.add("contentReview.create");
      paths.add("contentReview.getQueue");
    }
    for (const planned of order || []) {
      const rc = recipe(planned.entity);
      for (const path of [rc.create && rc.create.path, rc.get, rc.update, rc.names, rc.profileToggle, rc.profileUpdate]) {
        if (path && isProtected(path)) paths.add(path);
      }
    }
    return [...paths];
  }
  var Runner = class {
    constructor(d) {
      for (const k of ["journal", "client", "reader", "cache", "validator", "storage"]) if (!d[k]) throw new Error("Runner needs " + k);
      Object.assign(this, d);
      this.log = d.log ?? (() => {
      });
      this.files =  new Map();
      this.imgProvenance =  new Map();
      this.manifests =  new Map();
      this.pauseRequested = false;
      this.tabId = d.tabId ?? randomTab();
      this.clock = d.clock ?? (() => Date.now());
      this._subs =  new Set();
    }
    on(fn) {
      if (typeof fn !== "function") throw new TypeError("Runner.on needs a function");
      this._subs.add(fn);
      return () => this._subs.delete(fn);
    }
    _emit(type, payload = {}) {
      if (!this._subs.size) return;
      const event = { type, at: this.clock(), ...payload };
      for (const fn of [...this._subs]) {
        try {
          fn(event);
        } catch {
        }
      }
    }
    _requireAuth(path, idx = null) {
      if (!this.auth || typeof this.auth.assert !== "function") return;
      try {
        this.auth.assert(path);
      } catch (e) {
        if (!(e instanceof AuthUnavailable)) throw e;
        throw new Paused("SESSION", { idx, path, detail: e.message, authState: e.state });
      }
    }
    _protectedPaths(order, manifest) {
      return protectedPathsFor(order, manifest);
    }
    _authRefused(error, info = {}) {
      const detail = error && error.message ? String(error.message) : "UNAUTHORIZED";
      if (this.auth && typeof this.auth.refuse === "function") {
        this.auth.refuse(`${info.path ? info.path + ": " : ""}${error && error.code ? error.code : "UNAUTHORIZED"}`);
      }
      this.log(`the game refused ${info.path || "a protected procedure"} as unauthenticated; auth state invalidated`);
      return new Paused("SESSION", { detail, authState: "signed_out", ...info });
    }
    _leaseKey(jobId) {
      const bloodline = this.manifests.get(jobId)?.manifest.policy.bloodrightImport?.bloodlineId ?? this.journal.get(jobId)?.bloodrightImport?.bloodlineId;
      return LEASE_PREFIX + (bloodline ? `bloodright:${bloodline}` : jobId);
    }
    _readLease(jobId) {
      try {
        return JSON.parse(this.storage.getItem(this._leaseKey(jobId)) || "null");
      } catch {
        return null;
      }
    }
    _lease(jobId) {
      const cur = this._readLease(jobId);
      const now = this.clock();
      if (cur && cur.tab !== this.tabId && typeof cur.at === "number" && now - cur.at < LEASE_TTL_MS) throw new LeaseHeld(jobId, cur);
      this.storage.setItem(this._leaseKey(jobId), JSON.stringify({ tab: this.tabId, at: now }));
    }
    _releaseLease(jobId) {
      const cur = this._readLease(jobId);
      if (cur && cur.tab === this.tabId) this.storage.removeItem(this._leaseKey(jobId));
    }
    plan(manifestSource, { jobId, manifestPath = null, manifestNumber: manifestNumber2 = null } = {}) {
      const manifest = parseManifest(manifestSource);
      assertBloodrightAvailable(this.journal, manifest.policy.bloodrightImport?.bloodlineId);
      const order = planOrder(manifest, readIdmap(this.storage));
      const captureOnly = order.length === 0 && manifest.capture.before.length + manifest.capture.after.length > 0;
      const job = this.journal.open({ jobId, manifestPath, manifestNumber: manifestNumber2, manifestHash: manifest.hash, items: toJournalSpecs(order), allowEmpty: captureOnly, bloodrightImport: manifest.policy.bloodrightImport });
      this.manifests.set(jobId, { manifest, order });
      return job;
    }
    attach(jobId, manifestSource) {
      const manifest = parseManifest(manifestSource);
      const job = this.journal.get(jobId);
      if (!job) throw new Error("no such job " + jobId);
      if (job.manifestHash && manifest.hash !== job.manifestHash) {
        if (manifest.bodyHash === job.manifestHash) {
          throw new Error(`job ${jobId} was opened before manifest identity covered execution policy (journal hash ${job.manifestHash} is this file's body hash). Its policy - dedupNames/readBack/skipPreflight/imgSizes - was never recorded, so it cannot be resumed safely under this bundle. Export the job for evidence and start a fresh one from the manifest.`);
        }
        throw new Error(`manifest changed under job ${jobId}: journal hash ${job.manifestHash}, file hash ${manifest.hash}`);
      }
      const order = planOrder(manifest, readIdmap(this.storage));
      if (order.length !== job.items.length) throw new Error("manifest item count differs from the journal");
      this.manifests.set(jobId, { manifest, order });
    }
    requestPause() {
      this.pauseRequested = true;
    }
    async run(jobId) {
      const { manifest, order } = this._m(jobId);
      let job = this.journal.get(jobId);
      if (job.state === "DONE" || job.state === "ABORTED") return this.summary(jobId);
      if (job.state === "PAUSED" || job.state === "INCOMPLETE") {
        const t = this.budget && this.budget.log && this.budget.log.tripped();
        if (t) return this._pause(jobId, "TOO_MANY_REQUESTS", { path: t.path, until: t.until });
        job = this.journal.setJobState(jobId, "RUNNING");
      }
      if (job.items.some((it) => it.state === "SENT")) {
        throw new Error("job has SENT items; call resume() so they are reconciled before anything else is sent");
      }
      for (const path of this._protectedPaths(order, manifest)) {
        try {
          this._requireAuth(path);
        } catch (e) {
          if (e instanceof Paused) return this._pause(jobId, e.reason, e);
          throw e;
        }
      }
      this._lease(jobId);
      const unresolvedJob = unresolvedBloodrightJob(this.journal, manifest.policy.bloodrightImport?.bloodlineId, jobId);
      if (unresolvedJob) return this._pause(jobId, "UNRESOLVED_IMPORT", { detail: `Resolve Bloodright job ${unresolvedJob.jobId} before this job can continue` });
      const bindingConflict = this._bindingConflict(job);
      if (bindingConflict) return this._pause(jobId, "STALE_BINDINGS", bindingConflict);
      this._syncIdmapFromJob(job);
      this.pauseRequested = false;
      this._emit("job:start", { jobId, items: job.items.length, mode: "run" });
      try {
        if (manifest.capture.before.length && !job.capturesBefore) await this._captures(jobId, manifest.capture.before, "before");
        if (manifest.dedupNames) await this._dedupNames(jobId, order);
        for (let i = 0; i < job.items.length; i++) {
          this._lease(jobId);
          job = this.journal.get(jobId);
          const item = job.items[i];
          if (["VERIFIED", "FAILED", "SKIPPED"].includes(item.state)) continue;
          if (item.state === "ORPHANED") throw new Paused("ORPHANED", { idx: i, detail: item.error ?? null });
          if (this.pauseRequested) throw new Paused("USER", { idx: i });
          this._emit("item:start", { jobId, idx: i, name: item.name ?? null, entity: item.entity ?? null, phase: item.phase ?? null });
          if (isBloodrightEntity(item.entity)) {
            for (const dep of order[i].deps ?? []) {
              const parent = job.items.find((it) => it.srcId === dep);
              if (!parent || parent.state !== "VERIFIED") throw new Paused("DEPENDENCY", { idx: i, detail: `${dep} must verify before ${item.name}` });
            }
          }
          await this._runItem(jobId, item, order[i], manifest);
          this._emit("item:end", { jobId, idx: i, state: this.journal.get(jobId).items[i]?.state ?? null });
        }
        if (manifest.capture.after.length && !job.capturesAfter) await this._captures(jobId, manifest.capture.after, "after");
      } catch (e) {
        if (!(e instanceof StaleItem) && this.journal.get(jobId).state !== "RUNNING") e = moved(this.journal, jobId, e);
        if (e instanceof Paused) return this._pause(jobId, e.reason, e);
        if (e instanceof AuthRefused) {
          const p = this._authRefused(e.error, { path: e.path });
          return this._pause(jobId, p.reason, p);
        }
        if (e instanceof RateLimited) return this._pause(jobId, "TOO_MANY_REQUESTS", { path: e.path, until: e.until });
        if (isTransport(e)) return this._pause(jobId, "NETWORK", { detail: String(e && e.message), httpStatus: e.httpStatus ?? null });
        this._releaseLease(jobId);
        throw e;
      }
      const finished = this.journal.get(jobId);
      const unresolved = finished.items.filter((it) => !TERMINAL_ITEM_STATES.includes(it.state));
      this.journal.setJobState(jobId, unresolved.length ? "INCOMPLETE" : "DONE");
      this._releaseLease(jobId);
      if (this.reconciler && typeof this.reconciler.forget === "function" && !unresolved.length) this.reconciler.forget(jobId);
      const summary = this.summary(jobId);
      this._emit("job:end", { jobId, state: summary.state ?? null });
      return summary;
    }
    async resume(jobId) {
      if (!this.reconciler) throw new Error("resume needs a reconciler");
      const { manifest, order } = this._m(jobId);
      const job = this.journal.get(jobId);
      for (const path of this._protectedPaths(order, manifest)) {
        try {
          this._requireAuth(path);
        } catch (e) {
          if (e instanceof Paused) return this._pause(jobId, e.reason, e);
          throw e;
        }
      }
      this._lease(jobId);
      const unresolvedJob = unresolvedBloodrightJob(this.journal, manifest.policy.bloodrightImport?.bloodlineId, jobId);
      if (unresolvedJob) return this._pause(jobId, "UNRESOLVED_IMPORT", { detail: `Resolve Bloodright job ${unresolvedJob.jobId} before this job can continue` });
      const bindingConflict = this._bindingConflict(job);
      if (bindingConflict) return this._pause(jobId, "STALE_BINDINGS", bindingConflict);
      this._syncIdmapFromJob(job);
      try {
        for (const item of job.items) {
          if (item.state !== "SENT") continue;
          const planned = order[item.idx];
          let r;
          if (item.phase === "suggest") {
            const f = await this._findSuggestion(item, contract_default2.statuses);
            r = f.hit || !f.complete ? { action: "confirm", entityId: item.entityId, phase: "suggest-find", note: f.hit ? "found in the review queue" : "queue too long to search; not resent" } : { action: "confirm", entityId: item.entityId, phase: "suggest", note: "not in the review queue; it will be suggested again" };
          } else r = await this.reconciler.resolveSent(this.journal.get(jobId), item, { planned, lookup: this._lookup(this.journal.get(jobId)) });
          if (r.action === "confirm") {
            const owesRules = item.phase === "update" && item.entity === "ai" && Array.isArray(planned?.data?.rules);
            const phase = r.landed ? owesRules ? "rules" : "verify" : r.phase ?? item.phase;
            this.journal.transition(jobId, item.idx, "CONFIRMED", { entityId: r.entityId ?? item.entityId, phase, reconciled: r.note ?? "confirmed by reconciliation" });
            if (r.entityId && item.srcId) this._remember(item.srcId, r.entityId);
          } else if (r.action === "orphan") {
            this.journal.transition(jobId, item.idx, "ORPHANED", { error: r.note ?? "ambiguous after crash", candidates: r.candidates ?? [] });
          } else {
            throw new Error("reconciler returned unknown action " + r.action);
          }
        }
      } catch (e) {
        if (e instanceof Paused) return this._pause(jobId, e.reason, e);
        if (e instanceof AuthRefused) {
          const p = this._authRefused(e.error, { path: e.path });
          return this._pause(jobId, p.reason, p);
        }
        if (e instanceof RateLimited) return this._pause(jobId, "TOO_MANY_REQUESTS", { path: e.path, until: e.until });
        if (isTransport(e)) return this._pause(jobId, "NETWORK", { detail: String(e && e.message), httpStatus: e.httpStatus ?? null });
        this._releaseLease(jobId);
        throw e;
      }
      return this.run(jobId);
    }
    adopt(jobId, idx, entityId) {
      const job = this.journal.get(jobId);
      const item = job.items[idx];
      if (!item) throw new Error("no such item " + idx);
      if (item.state !== "ORPHANED") throw new Error(`adopt needs an ORPHANED item; ${item.idx} is ${item.state}`);
      if (!entityId) throw new Error("adopt needs an id");
      const holder = this.journal.findHolder(item.entity, entityId, { exceptJobId: jobId, exceptIdx: idx });
      if (holder) throw new Error(`${entityId} is already held by job ${holder.jobId} item ${holder.idx} (${holder.name}) in state ${holder.state}`);
      const phase = item.phase === "create" || !item.entityId ? recipe(item.entity).oneStep ? "verify" : "update" : item.phase;
      this.journal.transition(jobId, idx, "CONFIRMED", { entityId, phase, adopted: true, error: null });
      if (item.srcId) this._remember(item.srcId, entityId);
    }
    skip(jobId, idx) {
      this.journal.transition(jobId, idx, "SKIPPED");
    }
    resolveConfirmed(jobId, idx, { confirmed = false } = {}) {
      if (confirmed !== true) throw new Error("operator confirmation required to leave an unverified write as failed");
      const job = this.journal.get(jobId), item = job?.items[idx];
      if (job?.items.some((it) => it.state === "SENT")) throw new Error("reconcile all SENT items before resolving a confirmed write");
      if (!["PAUSED", "INCOMPLETE"].includes(job?.state)) throw new Error("recovery requires a paused or incomplete job");
      if (!item || item.state !== "CONFIRMED" || !isBloodrightEntity(item.entity)) throw new Error("recovery requires a CONFIRMED Bloodright item");
      this._lease(jobId);
      try {
        if (item.srcId && item.entityId && !readIdmap(this.storage)[item.srcId]) this._remember(item.srcId, item.entityId);
        this.journal.transition(jobId, idx, "FAILED", {
          resolution: { action: "operator-failed", at: new Date(this.clock()).toISOString(), pauseReason: job.pause?.reason ?? null },
          error: item.error || "Operator stopped recovery; this write remains unverified and its server record is left as is"
        });
      } finally {
        this._releaseLease(jobId);
      }
      return this.summary(jobId);
    }
    forgetBinding(jobId, idx, { confirmed = false, expectedId } = {}) {
      if (confirmed !== true) throw new Error("operator confirmation required to forget a saved binding");
      const job = this.journal.get(jobId), item = job?.items[idx], bl = job?.bloodrightImport?.bloodlineId;
      if (!bl || !item?.srcId?.startsWith(`br:${bl}:`) || !isBloodrightEntity(item.entity) || !["FAILED", "VERIFIED"].includes(item.state)) throw new Error("forget binding requires a resolved Bloodright item with provenance");
      if (job.state === "RUNNING") throw new Error("pause the job before forgetting a binding");
      this._lease(jobId);
      try {
        assertBloodrightAvailable(this.journal, bl);
        const map = readIdmap(this.storage);
        if (!expectedId || expectedId !== item.entityId || map[item.srcId] !== expectedId) throw new Error("binding changed; refresh and inspect its current ID");
        const forgotten = { entityId: expectedId, at: new Date(this.clock()).toISOString() };
        for (const old of this.journal.listJobs()) if (old.items.some((it) => it.srcId === item.srcId)) {
          this.journal.annotateJob(old.jobId, { forgottenBindings: { ...old.forgottenBindings, [item.srcId]: forgotten } });
        }
        delete map[item.srcId];
        writeIdmap(this.storage, map);
      } finally {
        this._releaseLease(jobId);
      }
      return this.summary(jobId);
    }
    summary(jobId) {
      const job = this.journal.get(jobId);
      const counts = {};
      for (const it of job.items) counts[it.state] = (counts[it.state] ?? 0) + 1;
      const verify = { match: 0, drift: 0, unread: 0 };
      for (const it of job.items) if (it.verify && verify[it.verify] !== void 0) verify[it.verify]++;
      return { jobId, state: job.state, outcome: jobOutcome(job), pause: job.pause, counts, verify, items: job.items.map((it) => ({ idx: it.idx, name: it.name, entity: it.entity, state: it.state, phase: it.phase, entityId: it.entityId, error: it.error ?? null, diffs: it.diffs ?? null, verify: it.verify ?? null })) };
    }
    async _runItem(jobId, item, planned, manifest) {
      const ent = item.entity;
      try {
        if (manifest.policy?.suggest) return await this._suggestItem(jobId, item, planned, manifest);
        if (item.state === "CONFIRMED" && item.phase === "verify") return await this._verifyOrSkip(jobId, item, planned, manifest);
        if (item.state === "CONFIRMED" && (item.phase === "rules" || item.phase === "rules-toggle")) {
          await this._rules(jobId, item, planned, item.entityId ?? item.targetId);
          item = this.journal.get(jobId).items[item.idx];
          if (item.state === "CONFIRMED") await this._verifyOrSkip(jobId, item, planned, manifest);
          return;
        }
        if (item.op === "create" && item.state === "PLANNED") {
          await this._preflight(item, planned);
          await this._create(jobId, item, planned);
          item = this.journal.get(jobId).items[item.idx];
          if (item.state !== "CONFIRMED") return;
          if (recipe(ent).oneStep) return await this._verifyOrSkip(jobId, item, planned, manifest);
        }
        if (ent === "aiProfile") {
          await this._rules(jobId, item, planned, item.targetId);
        } else {
          await this._fill(jobId, item, planned);
          item = this.journal.get(jobId).items[item.idx];
          if (item.state !== "CONFIRMED") return;
          if (ent === "ai" && Array.isArray(planned.data.rules)) await this._rules(jobId, item, planned, item.entityId);
        }
        item = this.journal.get(jobId).items[item.idx];
        if (item.state === "CONFIRMED") await this._verifyOrSkip(jobId, item, planned, manifest);
      } catch (e) {
        if (e instanceof LeaseHeld || e instanceof StaleItem) throw e;
        if (this.journal.get(jobId).state !== "RUNNING") throw moved(this.journal, jobId, e);
        if (e instanceof Paused) throw e;
        if (e instanceof AuthRefused) throw this._authRefused(e.error, { idx: item.idx, path: e.path });
        if (e instanceof RateLimited) throw new Paused("TOO_MANY_REQUESTS", { path: e.path, until: e.until, idx: item.idx });
        const cur = this.journal.get(jobId).items[item.idx];
        if (cur.state === "SENT") {
          throw new Paused(
            e instanceof NetworkError ? "NETWORK" : e instanceof TransportError ? "UNDECODABLE_RESPONSE" : "AMBIGUOUS",
            { idx: item.idx, detail: String(e && e.message), httpStatus: e.httpStatus ?? null, received: e.received ?? null }
          );
        }
        if (isTransport(e)) {
          throw new Paused("NETWORK", { idx: item.idx, detail: String(e && e.message), httpStatus: e.httpStatus ?? null });
        }
        this.journal.transition(jobId, item.idx, "FAILED", { error: String(e && e.message ? e.message : e) });
        this.log(`item ${item.idx} failed: ${e && e.message}`, item);
      }
    }
    async _preflight(item, planned) {
      const refs = collectRefs(planned.data);
      for (const r of refs) {
        if (r.pfx === "DOUBLED") throw new Error(`doubled ref prefix at ${r.path}: ${r.key}`);
        if (r.pfx === "img") {
          this._imgPreflight(r.key);
          continue;
        }
        if (!this._lookup(this.journal.get(this._jobOf(item)))(r.pfx, r.key)) throw new Error(`@${r.pfx}:${r.key} is not resolvable yet (at ${r.path})`);
      }
      const problems = this.validator.problems(item.entity, planned.data, null, { preCreate: true });
      if (problems.length) throw new Error("pre-send validation: " + problems.join("; "));
    }
    _imgPreflight(name) {
      const prov = this.imgProvenance.get(name);
      if (prov) {
        if (readAssetUploads(this.storage)[prov.sha256]) return;
        const file = this.files.get(name);
        if (!file) throw new Error(`@img:${name} is bound to ${prov.path} but its verified bytes are not loaded`);
        if (file !== prov.file) throw new Error(`@img:${name} is not holding the exact file that was verified against ${prov.sha256.slice(0, 12)}; nothing was sent`);
        return;
      }
      if (!this.files.has(name) && !readIdmap(this.storage)[name]) throw new Error(`@img:${name} has no file picked`);
    }
    async _imgBytes(name, prov) {
      const file = this.files.get(name);
      if (!file) throw new Error(`@img:${name} is bound to ${prov.path} but its verified bytes are not loaded`);
      if (file !== prov.file) throw new Error(`@img:${name} is not holding the exact file that was verified against ${prov.sha256.slice(0, 12)}; nothing was uploaded`);
      if (typeof this.digest !== "function") throw new Error(`@img:${name} is repo-backed but no digest is wired, so its bytes cannot be re-verified; nothing was uploaded`);
      const hex = toHex(await this.digest(await file.arrayBuffer()));
      if (hex !== prov.sha256) throw new Error(`@img:${name} hashes to ${hex} at the moment of upload; the pack says ${prov.sha256}. Nothing was uploaded.`);
      return file;
    }
    async _create(jobId, item, planned) {
      const rc = recipe(item.entity);
      const expect = this._expect(jobId, item.idx);
      const reserved = await this._throttle(jobId, item.idx, rc.create.path, expect);
      if (this.reconciler) {
        const key = await this.reconciler.beforeCreate(this.journal.get(jobId), item, item.entity);
        if (key) this.journal.annotate(jobId, item.idx, { snapshotKey: key });
      }
      const pre = rc.oneStep || item.entity === "badge";
      const createData = pre ? await this._resolved(planned.data, jobId) : planned.data;
      if (pre) {
        const problems = this.validator.problems(item.entity, createData, null, { preCreate: true });
        if (problems.length) throw new Error("pre-send validation: " + problems.join("; "));
      }
      const decoded = await this._send(jobId, item, { phase: "create" }, rc.create.path, rc.create.input(createData), reserved, expect);
      const o = rc.createdId ? readCreatedId(rc, decoded) : readCreate(decoded);
      if (o.kind === "ok") {
        this.journal.transition(jobId, item.idx, "CONFIRMED", { entityId: o.id, phase: rc.oneStep ? "verify" : "update", ...rc.oneStep ? { asserted: Object.keys(planned.data) } : {} });
        this._remember(item.srcId, o.id);
        await this.cache.invalidateEntity(rc.cacheEntity);
        this.log(`created ${item.entity} ${o.id} (placeholder)`, item);
        return;
      }
      this._failFromOutcome(jobId, item, o, "create");
    }
    async _send(jobId, item, patch, path, input, reserved = false, expect = this._expect(jobId, item.idx)) {
      this._requireAuth(path, item.idx);
      if (!reserved) await this._throttle(jobId, item.idx, path, expect);
      this._fresh(jobId, item.idx, expect);
      const decoded = await this.journal.withSent(
        jobId,
        item.idx,
        patch,
        () => this.client.call(path, input),
        () => {
          this.budget?.assertNotTripped?.();
          this._lease(jobId);
        }
      );
      if (decoded && decoded.ok === false && decoded.error && decoded.error.code === "TOO_MANY_REQUESTS") {
        let limited = null;
        try {
          if (this.budget) this.budget.observe([decoded], [path]);
        } catch (e) {
          if (!(e instanceof RateLimited)) throw e;
          limited = e;
        }
        this.journal.transition(jobId, item.idx, "FAILED", { error: `${patch.phase} TOO_MANY_REQUESTS: ${decoded.error.message} (refused before it applied; not resent)` });
        throw new Paused("TOO_MANY_REQUESTS", { idx: item.idx, path, until: limited ? limited.until : null, detail: decoded.error.message });
      }
      return decoded;
    }
    async _throttle(jobId, idx, path, expect) {
      if (!isLimited(path)) return false;
      if (!this.budget) throw new Error(`${path} is rate-limited and no budget is wired; nothing sent`);
      await this.budget.acquire(path, 1);
      this._fresh(jobId, idx, expect);
      return true;
    }
    _expect(jobId, idx) {
      const it = this.journal.get(jobId).items[idx];
      return { state: it.state, phase: it.phase ?? null };
    }
    _fresh(jobId, idx, expect) {
      this.budget?.assertNotTripped?.();
      this._lease(jobId);
      const job = this.journal.get(jobId), it = job.items[idx];
      if (job.state !== "RUNNING" || it.state !== expect.state || (it.phase ?? null) !== expect.phase) {
        throw new StaleItem(`item ${idx} is ${it.state}/${it.phase}, job ${job.state}: another tab moved it; nothing sent`);
      }
    }
    async _fill(jobId, item, planned) {
      const rc = recipe(item.entity);
      const id2 = item.entityId ?? item.targetId;
      if (!id2) throw new Error("no id to fill");
      const data = await this._resolved(planned.data, jobId);
      const expect = this._expect(jobId, item.idx);
      const reserved = await this._throttle(jobId, item.idx, rc.update, expect);
      this._requireAuth(rc.get, item.idx);
      const live = await this.reader.get(rc.get, id2, { fresh: true });
      if (!live.ok) {
        const cls = classifyError(live.error);
        if (cls === "SESSION") throw this._authRefused(live.error, { path: rc.get, idx: item.idx });
        throw new Error(`${rc.get} failed: ${live.error.code} ${live.error.message}`);
      }
      if (live.data == null && isBloodrightEntity(item.entity)) throw new Paused("VISIBILITY", { idx: item.idx, detail: `${rc.get} returned no visible record for ${id2}; recheck the session, hidden-content access and target before resuming` });
      if (live.data == null) throw new Error(`${rc.get} returned no record for ${id2}`);
      if (isBloodrightEntity(item.entity)) {
        if (item.entity === "skillTree" && (live.data.pathType !== "BLOODRIGHT" || live.data.bloodlineId !== data.bloodlineId && !planned.reassign || !live.data.hidden)) throw new Error("Bloodright binding no longer identifies hidden content for this bloodline");
        if (item.op === "create" && item.entity === "skillTree" && live.data.name !== rc.placeholder(id2) && diffAsserted(item.entity, data, live.data).length) throw new Error("adopted skill is not the expected placeholder; refusing to overwrite it");
        if (!diffAsserted(item.entity, data, live.data).length) {
          const reuse = { entityId: id2, phase: "verify", reused: true, asserted: Object.keys(data) };
          if (item.state === "CONFIRMED") this.journal.annotate(jobId, item.idx, reuse);
          else this.journal.transition(jobId, item.idx, "CONFIRMED", reuse);
          this._remember(item.srcId, id2);
          return;
        }
        if (planned.expected && !deepEqualPayload(writableSnapshot(item.entity, live.data), planned.expected)) throw new Paused("STALE_PREVIEW", { idx: item.idx, detail: "record changed since preview; prepare a new job" });
      }
      const problems = this.validator.problems(item.entity, data, live.data, { refreshPackages: planned.refreshPackages === true });
      if (problems.length) throw new Error("pre-send validation: " + problems.join("; "));
      const payload = mergeForUpdate(item.entity, live.data, data, this.validator.knownFields(item.entity));
      const decoded = await this._send(jobId, item, { phase: "update" }, rc.update, updateInput(rc, id2, payload), reserved, expect);
      const o = readMutation(decoded);
      await this.cache.invalidateRecord(rc.cacheEntity, id2);
      if (o.kind === "ok") {
        const next = item.entity === "ai" && Array.isArray(planned.data.rules) ? "rules" : "verify";
        const refreshed = item.entity === "dungeon" ? packageDrops(payload) : [];
        this.journal.transition(jobId, item.idx, "CONFIRMED", { entityId: id2, phase: next, asserted: Object.keys(data), ...refreshed.length ? { packagesRefreshed: refreshed } : {} });
        if (isBloodrightEntity(item.entity)) this._remember(item.srcId, id2);
        return;
      }
      this._failFromOutcome(jobId, item, o, "update");
    }
    _suggestion(manifest, planned, jobId, item) {
      const s = { ...manifest.policy.suggest, ...planned.suggestion ?? {} };
      for (const k of ["title", "rationale", "category"]) if (s[k] == null) delete s[k];
      const merged = { ...manifest.policy.suggest, ...s };
      const tag = ` [${String(jobId).slice(-6)}-${item.idx + 1}]`;
      const base2 = `${merged.title} \xB7 ${item.name}`;
      return { category: merged.category ?? "BALANCE", rationale: merged.rationale, title: base2.slice(0, contract_default2.titleLength.max - tag.length) + tag };
    }
    async _findSuggestion(item, statuses = ["PENDING"]) {
      const entityType = contract_default2.entityTypes[item.entity], id2 = item.entityId ?? item.targetId;
      for (const status of statuses) {
        for (let cursor = 0, page = 0; ; page++) {
          if (page >= 60) return { hit: null, complete: false };
          this._requireAuth("contentReview.getQueue", item.idx);
          const r = await this.client.call("contentReview.getQueue", { status, entityType, source: "STAFF", cursor, limit: 50 });
          if (!r.ok && classifyError(r.error) === "SESSION") throw this._authRefused(r.error, { path: "contentReview.getQueue", idx: item.idx });
          if (!r.ok) throw new Paused("NETWORK", { idx: item.idx, detail: `contentReview.getQueue failed: ${r.error?.message ?? "error"}` });
          const hit = (r.data?.items ?? []).find((p) => p.title === item.suggestTitle && (p.targets ?? []).some((t) => t.entityId === id2));
          if (hit) return { hit, complete: true };
          if (r.data?.nextCursor == null) break;
          cursor = r.data.nextCursor;
        }
      }
      return { hit: null, complete: true };
    }
    async _suggestItem(jobId, item, planned, manifest) {
      const rc = recipe(item.entity), id2 = item.entityId ?? item.targetId;
      if (item.state === "CONFIRMED" && item.phase === "verify") return this._verifyOrSkip(jobId, item, planned, manifest);
      if (!(item.state === "CONFIRMED" && item.phase === "suggest-find")) {
        const data = await this._resolved(planned.data, jobId);
        this._requireAuth(rc.get, item.idx);
        const live = await this.reader.get(rc.get, id2, { fresh: true });
        if (!live.ok && classifyError(live.error) === "SESSION") throw this._authRefused(live.error, { path: rc.get, idx: item.idx });
        if (!live.ok || live.data == null) throw new Error(`${rc.get} returned no record for ${id2}`);
        const problems = this.validator.problems(item.entity, data, live.data);
        if (problems.length) throw new Error("pre-send validation: " + problems.join("; "));
        const payload = mergeForUpdate(item.entity, live.data, data, this.validator.knownFields(item.entity));
        if (item.entity === "item" && payload.expireFromStoreAt == null) payload.expireFromStoreAt = "";
        const s = this._suggestion(manifest, planned, jobId, item);
        const decoded = await this._send(
          jobId,
          item,
          { phase: "suggest", entityId: id2, suggestTitle: s.title },
          "contentReview.create",
          { entityType: contract_default2.entityTypes[item.entity], entityId: id2, category: s.category, title: s.title, rationale: s.rationale, data: payload }
        );
        const o = readMutation(decoded);
        if (o.kind !== "ok") {
          if (/nothing changed/i.test(o.message ?? "")) {
            this.journal.transition(jobId, item.idx, "CONFIRMED", { phase: "suggest-find" });
            this.journal.transition(jobId, item.idx, "VERIFIED", { verify: "match", reconciled: "the review desk reports the record already holds this edit" });
            return;
          }
          return this._failFromOutcome(jobId, item, o, "suggest");
        }
        this.journal.transition(jobId, item.idx, "CONFIRMED", { phase: "suggest-find" });
        item = this.journal.get(jobId).items[item.idx];
      }
      const { hit } = await this._findSuggestion(item, contract_default2.statuses);
      this.journal.transition(jobId, item.idx, "VERIFIED", {
        verify: "suggested",
        suggestion: { id: hit?.id ?? null, status: hit?.status ?? "PENDING" },
        ...hit ? {} : { reconciled: "sent for review; not found in the queue to record its id" }
      });
    }
    async _rules(jobId, item, planned, userId) {
      const rc = recipe("aiProfile");
      const rules = planned.data.rules ?? [];
      const includeDefaultRules = planned.data.includeDefaultRules !== false;
      if (item.entity === "aiProfile") {
        const problems = this.validator.problems("aiProfile", planned.data, null);
        if (problems.length) throw new Error("pre-send validation: " + problems.join("; "));
      }
      this._requireAuth(rc.get, item.idx);
      let live = await this.reader.get(rc.get, userId, { fresh: true });
      if (!live.ok && classifyError(live.error) === "SESSION") throw this._authRefused(live.error, { idx: item.idx, path: rc.get });
      if (!live.ok || !live.data) throw new Error(`profile.getAi failed for ${userId}`);
      let apid = live.data.aiProfileId;
      if (!apid) {
        const decoded2 = await this._send(jobId, item, { phase: "rules-toggle", entityId: userId }, rc.profileToggle, { aiId: userId });
        const o2 = readMutation(decoded2);
        if (o2.kind !== "ok") {
          this._failFromOutcome(jobId, item, o2, "toggle");
          return;
        }
        this.journal.transition(jobId, item.idx, "CONFIRMED", { phase: "rules" });
        live = await this.reader.get(rc.get, userId, { fresh: true });
        if (!live.ok && classifyError(live.error) === "SESSION") throw this._authRefused(live.error, { idx: item.idx, path: rc.get });
        apid = live.ok && live.data ? live.data.aiProfileId : null;
        if (!apid) throw new Error("no aiProfileId after toggle");
      }
      const decoded = await this._send(jobId, item, { phase: "rules", entityId: userId, aiProfileId: apid }, rc.profileUpdate, { id: apid, rules, includeDefaultRules });
      const o = readMutation(decoded);
      await this.cache.invalidateEntity("ai");
      if (o.kind === "ok") {
        this.journal.transition(jobId, item.idx, "CONFIRMED", { entityId: userId, phase: "verify", aiProfileId: apid, assertedRules: true });
        return;
      }
      this._failFromOutcome(jobId, item, o, "rules");
    }
    async _verifyOrSkip(jobId, item, planned, manifest) {
      if (!manifest.readBack) throw new Error("readBack:false reached item " + item.idx + "; a written item must be read back");
      await this._verify(jobId, item, planned);
    }
    async _verify(jobId, item, planned) {
      const rc = recipe(item.entity);
      const data = await this._resolved(planned.data, jobId, { readOnly: true });
      const diffs = [];
      if (item.entity !== "aiProfile") {
        this._requireAuth(rc.get, item.idx);
        const live = await this.reader.get(rc.get, item.entityId, { fresh: true });
        if (!live.ok && classifyError(live.error) === "SESSION") throw this._authRefused(live.error, { idx: item.idx, path: rc.get });
        if (live.ok && !live.data && isBloodrightEntity(item.entity)) throw new Paused("VISIBILITY", { idx: item.idx, detail: `${rc.get} returned no visible record for ${item.entityId}; recheck the session, hidden-content access and target before resuming` });
        if (!live.ok || !live.data) {
          this.journal.annotate(jobId, item.idx, { verify: "unread", phase: "verify" });
          return;
        }
        diffs.push(...diffAsserted(item.entity, data, live.data));
      }
      if (item.entity === "ai" && Array.isArray(planned.data.rules) || item.entity === "aiProfile") {
        if (!item.aiProfileId) {
          this.journal.annotate(jobId, item.idx, { verify: "unread", phase: "verify" });
          return;
        }
        this._requireAuth("ai.getAiProfile", item.idx);
        const pr = await this.reader.get("ai.getAiProfile", item.aiProfileId, { fresh: true });
        if (!pr.ok && classifyError(pr.error) === "SESSION") throw this._authRefused(pr.error, { idx: item.idx, path: "ai.getAiProfile" });
        if (pr.ok && pr.data) {
          if (!deepEqualPayload(planned.data.rules ?? [], pr.data.rules ?? [])) diffs.push({ key: "rules", sent: planned.data.rules, live: pr.data.rules });
          if (planned.data.includeDefaultRules !== void 0 && pr.data.includeDefaultRules !== planned.data.includeDefaultRules) diffs.push({ key: "includeDefaultRules", sent: planned.data.includeDefaultRules, live: pr.data.includeDefaultRules });
        } else {
          this.journal.annotate(jobId, item.idx, { verify: "unread", phase: "verify" });
          return;
        }
      }
      if (diffs.length) this.journal.annotate(jobId, item.idx, { diffs, verify: "drift", phase: "verify" });
      else this.journal.transition(jobId, item.idx, "VERIFIED", { diffs: [], verify: "match" });
    }
    async _dedupNames(jobId, order) {
      const byEntity =  new Map();
      for (const it of this.journal.get(jobId).items) {
        if (it.op !== "create" || it.state !== "PLANNED") continue;
        const rc = recipe(it.entity);
        if (!rc.names) continue;
        const planned = order[it.idx];
        const name = planned && planned.data ? planned.data[rc.nameKey] ?? it.name : it.name;
        if (typeof name !== "string" || !name.trim()) continue;
        if (!byEntity.has(it.entity)) byEntity.set(it.entity, []);
        byEntity.get(it.entity).push({ idx: it.idx, name: name.trim() });
      }
      for (const [entity, entries] of byEntity) {
        const rc = recipe(entity);
        const r = await this.reader.list(rc.names, { fresh: true });
        if (!r.ok) {
          const cls = classifyError(r.error);
          if (cls === "SESSION") throw this._authRefused(r.error, { path: rc.names });
          throw new Paused("NETWORK", { detail: `dedupNames: ${rc.names} failed: ${r.error.code} ${r.error.message}` });
        }
        const rows = recipeRows(rc, r.data);
        const live =  new Set();
        for (const row of rows) {
          const v = row && (rowName(rc, row) ?? row.name ?? row.username);
          if (typeof v === "string") live.add(v.trim().toLowerCase());
        }
        for (const e of entries) {
          if (!live.has(e.name.toLowerCase())) continue;
          this.journal.transition(jobId, e.idx, "FAILED", { error: `dedupNames: LIVE NAME COLLISION "${e.name}" already exists as a ${entity}; rename before pushing` });
          this.log(`item ${e.idx} failed: live name collision "${e.name}"`);
        }
      }
    }
    async _captures(jobId, list, phase) {
      const key = phase === "before" ? "capturesBefore" : "capturesAfter";
      const job = this.journal.get(jobId);
      const out = Array.isArray(job[key + "Partial"]) ? job[key + "Partial"] : [];
      for (let i = out.length; i < list.length; i++) {
        const c = list[i];
        const path = c.proc || c.procedure;
        const id2 = c.id ?? (c.input && (c.input.id ?? c.input.userId));
        const capInput = c.input == null ? void 0 : c.input;
        this._requireAuth(path, null);
        const r = id2 != null ? await this.reader.get(path, id2, { fresh: true }) : await this.reader.list(path, { fresh: true, input: capInput });
        if (!r.ok && classifyError(r.error) === "SESSION") throw this._authRefused(r.error, { path, phase, ordinal: i });
        const sentInput = (id2 != null ? readInput(path, id2) : capInput === void 0 ? listInput(path) : capInput) ?? null;
        const entry = { phase, proc: path, input: sentInput, ok: r.ok, rows: Array.isArray(r.data) ? r.data.length : r.data ? 1 : 0, error: r.ok ? null : r.error.code };
        if (c.persist === "full") Object.assign(entry, await this._persistFull(jobId, phase, i, path, id2, sentInput, r));
        out.push(entry);
        this.journal.annotateJob(jobId, { [key + "Partial"]: out });
      }
      this.journal.annotateJob(jobId, { [key]: out, [key + "Partial"]: null });
      return out;
    }
    async _persistFull(jobId, phase, ordinal, path, id2, input, r) {
      const fields = { persist: "full", snapshotKey: snapshotKey(jobId, phase, ordinal), persistOk: false, persistError: null };
      if (!r.ok) {
        fields.persistError = "read failed; there is no body to persist";
        return fields;
      }
      const bytes = JSON.stringify(r.data ?? null).length;
      fields.bytes = bytes;
      if (bytes > MAX_FULL_CAPTURE_BYTES) {
        fields.persistError = `body is ${bytes} bytes, over the ${MAX_FULL_CAPTURE_BYTES}-byte full-capture ceiling; it is NOT truncated and NOT persisted`;
        return fields;
      }
      try {
        await this.cache.putSnapshot({ key: fields.snapshotKey, jobId, phase, ordinal, path, id: id2, input, data: r.data });
      } catch (e) {
        fields.persistError = "capture snapshot write failed: " + (e && e.message ? e.message : String(e));
        return fields;
      }
      fields.persistOk = true;
      return fields;
    }
    _m(jobId) {
      const m = this.manifests.get(jobId);
      if (!m) throw new Error("no manifest attached for job " + jobId + "; call plan() or attach()");
      return m;
    }
    _jobOf(item) {
      for (const [jobId, m] of this.manifests) if (m.order.some((o) => o === item || o.idx === item.idx && this.journal.get(jobId)?.items[item.idx]?.srcId === item.srcId)) return jobId;
      return null;
    }
    _pause(jobId, reason, info) {
      this._emit("job:paused", { jobId, reason, path: info.path ?? null, idx: info.idx ?? null });
      this.journal.setJobState(jobId, "PAUSED", { pause: { reason, path: info.path ?? null, until: info.until ?? null, idx: info.idx ?? null, detail: info.detail ?? null, httpStatus: info.httpStatus ?? null, authState: info.authState ?? null, authRefused: info.authRefused ?? false } });
      this._releaseLease(jobId);
      this.log(`paused: ${reason}${info.path ? " on " + info.path : ""}`);
      return this.summary(jobId);
    }
    _failFromOutcome(jobId, item, o, step) {
      const roleMessages = ["You are not authorized to create skills", "You are not authorized to create hidden skills", "You are not authorized to edit this content", "You are not authorized to hide skills", "You are not authorized to create folders", "You are not authorized to create hidden folders", "You are not authorized to edit folders", "You are not authorized to hide folders"];
      if (isBloodrightEntity(item.entity) && roleMessages.includes(o.message)) {
        this.journal.transition(jobId, item.idx, "FAILED", { error: `${step} PERMISSION: ${o.message}` });
        throw new Paused("PERMISSION", { idx: item.idx, detail: o.message });
      }
      if (o.kind === "refused") {
        this.journal.transition(jobId, item.idx, "FAILED", { error: `${step} refused: ${o.message}` });
        return;
      }
      const cls = classifyError(o.error);
      if (cls === "SESSION") {
        this.journal.transition(jobId, item.idx, "FAILED", { error: `${step} SESSION: ${o.error.message}`, authRefused: true });
        this.log(`item ${item.idx} refused by the game as unauthenticated on ${step}`, item);
        throw this._authRefused(o.error, { idx: item.idx, authRefused: true });
      }
      const issues = o.error.zodError ? " " + o.error.zodError.map((z) => `${(z.path || []).join(".")}: ${z.message}`).join("; ") : "";
      this.journal.transition(jobId, item.idx, "FAILED", { error: `${step} ${cls}: ${o.error.message}${issues}`, zodError: o.error.zodError ?? null });
    }
    _bindingConflict(job) {
      if (!this.manifests.get(job.jobId)?.manifest.policy.bloodrightImport) return null;
      if (Object.keys(job.forgottenBindings ?? {}).length) return { detail: "a saved binding was explicitly forgotten; export this job and prepare a fresh preview" };
      const bindings = readIdmap(this.storage);
      for (const it of job.items) {
        const saved = bindings[it.srcId];
        if (saved && saved !== (it.entityId ?? it.targetId)) return { idx: it.idx, detail: "binding changed since preview; inspect the other job before continuing" };
      }
      return null;
    }
    _remember(srcId, id2) {
      if (!srcId || !id2) return;
      const map = readIdmap(this.storage);
      map[srcId] = id2;
      writeIdmap(this.storage, map);
    }
    _syncIdmapFromJob(job) {
      let map = null;
      for (const it of job.items) if (it.srcId && it.entityId) {
        map = map ?? readIdmap(this.storage);
        if (map[it.srcId] !== it.entityId) map[it.srcId] = it.entityId;
      }
      if (map) writeIdmap(this.storage, map);
    }
    _lookup(job) {
      const map = readIdmap(this.storage);
      return (pfx, key) => {
        const owned = job?.items.find((it) => it.srcId === key && it.entityId)?.entityId;
        return pfx.startsWith("skillTree") ? owned ?? map[key] : map[key] ?? owned;
      };
    }
    async _resolved(data, jobId, { readOnly = false } = {}) {
      const probe = readOnly ? null : this.imageProbe;
      const heartbeat = () => {
        if (jobId) this._lease(jobId);
      };
      const refs = collectRefs(data).filter((r) => r.pfx === "img");
      for (const r of refs) {
        const prov = this.imgProvenance.get(r.key) ?? null;
        const map = readIdmap(this.storage);
        let file;
        if (prov) {
          let known = readAssetUploads(this.storage)[prov.sha256];
          if (known && known.url && probe && await probe(known.url) === false) {
            forgetAssetUpload(this.storage, prov.sha256);
            known = null;
          }
          if (known && known.url) {
            if (map[r.key] !== known.url) {
              map[r.key] = known.url;
              writeIdmap(this.storage, map);
            }
            continue;
          }
          file = await this._imgBytes(r.key, prov);
        } else {
          if (map[r.key] && probe && await probe(map[r.key]) === false) {
            delete map[r.key];
            writeIdmap(this.storage, map);
          }
          if (map[r.key]) continue;
          file = this.files.get(r.key);
          if (!file) throw new Error(`@img:${r.key} has no file picked`);
        }
        if (readOnly) throw new Error(`@img:${r.key} has no recorded upload to verify against`);
        if (!this.uploader) throw new Error("no uploader configured for @img refs");
        const up = await this.uploader.upload(file, { onWait: heartbeat });
        const url2 = up.url ?? up.ufsUrl;
        if (probe && await probe(url2) === false) throw new Error(`@img:${r.key} uploaded but does not load (${url2}); nothing was saved with it`);
        map[r.key] = url2;
        writeIdmap(this.storage, map);
        if (prov) recordAssetUpload(this.storage, prov.sha256, url2, { path: prov.path, ref: prov.ref, at: this.clock() });
      }
      const job = jobId ? this.journal.get(jobId) : null;
      const { value, unresolved } = resolveRefs(data, this._lookup(job));
      if (unresolved.length) throw new Error("unresolved refs: " + unresolved.map((u) => `@${u.pfx}:${u.key} at ${u.path}`).join(", "));
      return value;
    }
  };
  function readCreatedId(rc, decoded) {
    const o = readMutation(decoded);
    if (o.kind !== "ok") return o;
    const id2 = rc.createdId(decoded.data);
    if (typeof id2 !== "string" || !NANOID_RE.test(id2)) throw new OutcomeError("create reported success without a well-formed id: " + JSON.stringify(decoded.data).slice(0, 120), { outcome: o });
    return { ...o, id: id2 };
  }

  var SNAP_PREFIX = "tnr_forge_snap_v1:";
  var Reconciler = class {
    constructor({ storage, reader, clock = () => Date.now(), journal }) {
      if (!journal || typeof journal.knownEntityIds !== "function") throw new Error("Reconciler needs the journal: without it cross-job adoption cannot be excluded");
      if (!storage || !reader) throw new Error("Reconciler needs storage and reader");
      this.storage = storage;
      this.reader = reader;
      this.clock = clock;
      this.journal = journal;
    }
    _ensureSession(path, r) {
      if (!r.ok && classifyError(r.error) === "SESSION") throw new AuthRefused(path, r.error);
      return r;
    }
    snapKey(jobId, entity) {
      return SNAP_PREFIX + jobId + ":" + entity;
    }
    readSnapshot(key) {
      try {
        return JSON.parse(this.storage.getItem(key) || "null");
      } catch {
        return null;
      }
    }
    async beforeCreate(job, item, entity) {
      const key = this.snapKey(job.jobId, entity);
      if (this.storage.getItem(key)) return key;
      const rc = recipe(entity);
      const list = this._ensureSession(rc.names, await this.reader.list(rc.names, { fresh: true }));
      if (!list.ok || !Array.isArray(list.data)) throw new Error(`snapshot failed: ${rc.names} ${list.ok ? "returned no list" : list.error.code}`);
      const ids = recipeRows(rc, list.data).map((r) => r[rc.idKey]).filter(Boolean);
      this.storage.setItem(key, JSON.stringify({ entity, at: new Date(this.clock()).toISOString(), path: rc.names, count: ids.length, ids }));
      return key;
    }
    forget(jobId) {
      const keys = [];
      for (let i = 0; i < this.storage.length; i++) {
        const k = this.storage.key(i);
        if (k && k.startsWith(SNAP_PREFIX + jobId + ":")) keys.push(k);
      }
      for (const k of keys) this.storage.removeItem(k);
      return keys.length;
    }
    async resolveSent(job, item, ctx = {}) {
      const rc = recipe(item.entity);
      if (item.phase === "create" || !item.entityId) return this._resolveCreate(job, item, rc, ctx);
      if (item.phase === "rules-toggle") return this._resolveToggle(item, rc);
      if (item.phase === "rules") return this._resolveRules(item, ctx);
      return this._resolveUpdate(item, rc, ctx);
    }
    async _resolveCreate(job, item, rc, ctx) {
      const key = item.snapshotKey || this.snapKey(job.jobId, item.entity);
      const snap = this.readSnapshot(key);
      if (!snap) return { action: "orphan", candidates: [], note: "no pre-create snapshot for this entity type; cannot tell which row is ours" };
      const list = this._ensureSession(rc.names, await this.reader.list(rc.names, { fresh: true }));
      if (!list.ok || !Array.isArray(list.data)) return { action: "orphan", candidates: [], note: `${rc.names} unavailable: ${list.ok ? "no list" : list.error.code}` };
      const before = new Set(snap.ids);
      const owned = new Set(job.items.filter((it) => it.entity === item.entity && it.entityId && it.idx !== item.idx).map((it) => it.entityId));
      for (const id2 of this.journal.knownEntityIds(item.entity)) owned.add(id2);
      const rows = recipeRows(rc, list.data).filter((r) => !before.has(r[rc.idKey]) && !owned.has(r[rc.idKey]));
      const pending = job.items.filter((it) => it.entity === item.entity && it.state === "SENT" && (it.phase === "create" || !it.entityId));
      const candidates = rows.map((r) => ({ id: r[rc.idKey], name: rowName(rc, r) ?? null, placeholderName: rc.placeholder ? rc.placeholder(r[rc.idKey]) === (r[rc.nameKey] ?? null) : null }));
      if (item.entity === "dungeon") return this._dungeonCreate(rows, candidates, pending, ctx);
      if (item.entity === "petSpecies") return this._petSpeciesCreate(rows, candidates, pending, ctx);
      if (item.entity === "badge" || item.entity === "title") return {
        action: "orphan",
        candidates,
        note: `lost ${item.entity} create: ${candidates.length} new row(s); adopt one (filled, never re-created) or skip`
      };
      if (candidates.length === 1 && pending.length === 1) {
        const c = candidates[0];
        if (item.entity === "skillTree" || item.entity === "skillTreeFolder") {
          const row = rows[0], planned = ctx.planned;
          if (!planned || item.entity === "skillTree" && (!c.placeholderName || row.pathType !== "BLOODRIGHT" || row.bloodlineId !== planned.data.bloodlineId || !row.hidden) || rc.oneStep && diffAsserted(item.entity, planned.data, row).length) return { action: "orphan", candidates, note: "new row does not match the planned Bloodright create" };
          return { action: "orphan", candidates, note: "matching Bloodright create found; confirm its ownership before adopting" };
        }
        return { action: "confirm", entityId: c.id, phase: "update", note: `adopted the single new ${item.entity} ${c.id}` + (c.placeholderName === false ? " (name is not the placeholder pattern; check it)" : "") };
      }
      return { action: "orphan", candidates, note: `${candidates.length} new ${item.entity} row(s) since the snapshot, ${pending.length} create(s) pending: ambiguous` };
    }
    _dungeonCreate(rows, candidates, pending, ctx) {
      let data = null, why = "";
      if (!ctx.planned) why = "; no planned data to compare against";
      else {
        const r = resolveRefs(ctx.planned.data, ctx.lookup ?? (() => void 0));
        if (r.unresolved.length) why = "; cannot compare: unresolved refs " + r.unresolved.map((u) => `@${u.pfx}:${u.key}`).join(", ");
        else data = r.value;
      }
      const evidence = candidates.map((c, i) => {
        if (!data) return c;
        const differs = contentDiffKeys(data, rows[i].content);
        return { ...c, matches: !differs.length, differs };
      });
      const n = evidence.filter((c) => c.matches).length;
      return {
        action: "orphan",
        candidates: evidence,
        note: `lost dungeon create: ${candidates.length} new row(s), ${n} matching the plan, ${pending.length} create(s) pending${why}. coop.dungeon.save has no idempotency key: a matching row may be someone else's. Check it, then adopt (read back, never re-saved) or skip`
      };
    }
    _petSpeciesCreate(rows, candidates, pending, ctx) {
      const r = ctx.planned ? resolveRefs(ctx.planned.data, ctx.lookup ?? (() => void 0)) : null;
      const data = r && !r.unresolved.length ? r.value : null;
      const evidence = candidates.map((c, i) => data ? { ...c, matches: !diffAsserted("petSpecies", data, rows[i]).length } : c);
      return {
        action: "orphan",
        candidates: evidence,
        note: `lost petSpecies create: ${candidates.length} new row(s), ${evidence.filter((c) => c.matches).length} matching the plan, ${pending.length} create(s) pending${data ? "" : "; cannot compare"}. Check it, then adopt (read back, never re-sent) or skip`
      };
    }
    async _resolveUpdate(item, rc, ctx) {
      const planned = ctx.planned;
      if (!planned) return { action: "orphan", candidates: [], note: "no planned data to compare against" };
      const live = this._ensureSession(rc.get, await this.reader.get(rc.get, item.entityId, { fresh: true }));
      if (!live.ok || !live.data) return { action: "orphan", candidates: [], note: `${rc.get} ${item.entityId}: ${live.ok ? "no record" : live.error.code}` };
      const { value: data, unresolved } = resolveRefs(planned.data, ctx.lookup ?? (() => void 0));
      if (unresolved.length) return { action: "orphan", candidates: [], note: "cannot compare: unresolved refs " + unresolved.map((u) => `@${u.pfx}:${u.key}`).join(", ") };
      const comparable = Object.keys(data).filter((k) => !SERVER_OWNED.includes(k));
      if (!comparable.length) return { action: "orphan", candidates: [], note: "cannot compare: no asserted keys to check" };
      const diffs = diffAsserted(item.entity, data, live.data);
      if (!diffs.length) return { action: "confirm", entityId: item.entityId, phase: "verify", landed: true, note: "update already landed: asserted keys match live" };
      return { action: "orphan", candidates: [], note: "update may not have landed: live differs on " + diffs.map((d) => d.key).join(", "), diffs };
    }
    async _resolveToggle(item, rc) {
      const live = this._ensureSession(rc.get, await this.reader.get(rc.get, item.entityId, { fresh: true }));
      if (live.ok && live.data && live.data.aiProfileId) return { action: "confirm", entityId: item.entityId, phase: "rules", note: "profile row exists; continue at rules" };
      return { action: "orphan", candidates: [], note: "no aiProfileId after a sent toggle" };
    }
    async _resolveRules(item, ctx) {
      if (!item.aiProfileId) return { action: "orphan", candidates: [], note: "rules sent but no aiProfileId recorded" };
      const prof = this._ensureSession("ai.getAiProfile", await this.reader.get("ai.getAiProfile", item.aiProfileId, { fresh: true }));
      if (!prof.ok || !prof.data) return { action: "orphan", candidates: [], note: "ai.getAiProfile unavailable" };
      const want = ctx.planned ? ctx.planned.data.rules ?? [] : null;
      const wantDefault = ctx.planned ? ctx.planned.data.includeDefaultRules : void 0;
      const rulesLanded = want && deepEqualPayload(want, prof.data.rules ?? []);
      const defaultLanded = wantDefault === void 0 || prof.data.includeDefaultRules === wantDefault;
      if (rulesLanded && defaultLanded) return { action: "confirm", entityId: item.entityId, phase: "verify", landed: true, note: "rules already landed" };
      return { action: "orphan", candidates: [], note: "rules may not have landed: profile rules differ" };
    }
  };

  var GH = Object.freeze({ owner: "perseverance484", repo: "tnr-tools", branch: "main", pushDir: "push", inboxDir: "harvests/inbox" });
  var GithubError = class extends Error {
    constructor(message, info = {}) {
      super(message);
      this.name = "GithubError";
      Object.assign(this, info);
    }
  };
  var Github = class {
    constructor({ fetchImpl, storage, config = GH }) {
      this.fetchImpl = fetchImpl;
      this.storage = storage;
      this.cfg = config;
    }
    _pat() {
      const g = readGh(this.storage);
      return g && g.pat ? g.pat : null;
    }
    _headers(accept = "application/vnd.github+json") {
      const h2 = { accept, "x-github-api-version": "2022-11-28" };
      const pat = this._pat();
      if (pat) h2.authorization = "Bearer " + pat;
      return h2;
    }
    _url(path, ref = this.cfg.branch) {
      return `https://api.github.com/repos/${this.cfg.owner}/${this.cfg.repo}/contents/${path}?ref=${encodeURIComponent(ref)}`;
    }
    async list(dir = this.cfg.pushDir) {
      const r = await this.fetchImpl(this._url(dir), { headers: this._headers() });
      if (!r.ok) throw new GithubError(`list ${dir}: HTTP ${r.status}`, { status: r.status });
      const j = await r.json();
      if (!Array.isArray(j)) throw new GithubError(`${dir} is not a directory`);
      return j.map(({ name, path, sha, size, type }) => ({ name, path, sha, size, type }));
    }
    async raw(path, ref) {
      const r = await this.fetchImpl(this._url(path, ref), { headers: this._headers("application/vnd.github.raw+json") });
      if (!r.ok) throw new GithubError(`fetch ${path}: HTTP ${r.status}`, { status: r.status });
      return r.arrayBuffer();
    }
    async text(path, ref) {
      return new TextDecoder().decode(await this.raw(path, ref));
    }
    async put(path, contentText, message) {
      if (!this._pat()) throw new GithubError("no PAT stored; Settings > GitHub");
      let sha = null;
      try {
        const r2 = await this.fetchImpl(this._url(path), { headers: this._headers() });
        if (r2.ok) sha = (await r2.json()).sha ?? null;
      } catch {
        sha = null;
      }
      const body = { message, content: b64utf8(contentText), branch: this.cfg.branch };
      if (sha) body.sha = sha;
      const r = await this.fetchImpl(`https://api.github.com/repos/${this.cfg.owner}/${this.cfg.repo}/contents/${path}`, {
        method: "PUT",
        headers: { ...this._headers(), "content-type": "application/json" },
        body: JSON.stringify(body)
      });
      const t = await r.text();
      if (r.status !== 200 && r.status !== 201) throw new GithubError(`put ${path}: HTTP ${r.status} ${t.slice(0, 140)}`, { status: r.status });
      let j = {};
      try {
        j = JSON.parse(t);
      } catch {
      }
      return { sha: j.content?.sha ?? null, htmlUrl: j.content?.html_url ?? null };
    }
  };
  function b64utf8(s) {
    const bytes = new TextEncoder().encode(s);
    let bin = "";
    for (let i = 0; i < bytes.length; i += 32768) bin += String.fromCharCode.apply(null, bytes.subarray(i, i + 32768));
    return btoa(bin);
  }
  function manifestNumber(name) {
    const m = /^(\d+)[a-z]?_/i.exec(name);
    return m ? Number(m[1]) : null;
  }
  function manifestSummary(text) {
    try {
      const m = JSON.parse(text);
      if (m.bloodrightCollection) {
        const trees = m.bloodrightCollection.trees ?? [];
        const title2 = typeof m._note === "string" ? m._note.split(/[.:;]\s|\n/)[0].slice(0, 80) : "Bloodright collection";
        return { ok: true, title: title2, items: 0, creates: 0, captures: 0, trees: trees.length, skills: trees.reduce((n, t) => n + Object.keys(t.nodes ?? {}).length, 0) };
      }
      if (m.bloodright) return { ok: true, title: m._note ?? "Bloodright design (prepare preview)", items: Object.keys(m.bloodright.nodes ?? {}).length, creates: 0, captures: 0 };
      const items = Array.isArray(m.items) ? m.items : Array.isArray(m.jutsu) ? m.jutsu : [];
      const caps = m.capture && (m.capture.before || []).length + (m.capture.after || []).length || 0;
      const title = typeof m._note === "string" ? m._note.split(/\.\s|\n/)[0].slice(0, 80) : items[0] && items[0].name || "";
      const creates = items.filter((i) => i && i.slot === "create").length;
      return { ok: true, title, items: items.length, creates, captures: caps };
    } catch (e) {
      return { ok: false, title: "(not JSON: " + e.message.slice(0, 40) + ")", items: 0, creates: 0, captures: 0 };
    }
  }

  var HTML_SINKS =  new Set(["innerHTML", "outerHTML", "srcdoc", "insertAdjacentHTML"]);
  var sinkKey = (k) => HTML_SINKS.has(k) || HTML_SINKS.has(String(k).toLowerCase());
  var DomSinkError = class extends Error {
    constructor(key) {
      super(`refusing to assign the HTML sink ${JSON.stringify(key)}; build nodes with h()/append() instead`);
      this.name = "DomSinkError";
      this.key = key;
    }
  };
  function h(tag, attrs = {}, ...children) {
    const el = document.createElement(tag);
    for (const [k, v] of Object.entries(attrs || {})) {
      if (sinkKey(k)) throw new DomSinkError(k);
      if (v == null || v === false) continue;
      if (k === "class") el.className = v;
      else if (k === "style" && typeof v === "object") Object.assign(el.style, v);
      else if (k.startsWith("on") && typeof v === "function") el.addEventListener(k.slice(2).toLowerCase(), v);
      else if (k === "dataset") Object.assign(el.dataset, v);
      else if (k === "value" && tag === "textarea") el.value = String(v);
      else if (k in el && typeof v !== "string") el[k] = v;
      else el.setAttribute(k, String(v));
    }
    append(el, children);
    return el;
  }
  function append(el, children) {
    for (const c of children.flat(Infinity)) {
      if (c == null || c === false) continue;
      el.appendChild(typeof c === "string" || typeof c === "number" ? document.createTextNode(String(c)) : c);
    }
    return el;
  }
  function clear(el) {
    while (el.firstChild) el.removeChild(el.firstChild);
    return el;
  }
  function replace(el, ...children) {
    clear(el);
    return append(el, children);
  }
  function installCss(cssText, doc = document) {
    try {
      const sheet = new CSSStyleSheet();
      sheet.replaceSync(cssText);
      doc.adoptedStyleSheets = [...doc.adoptedStyleSheets || [], sheet];
      return sheet;
    } catch {
      const style = doc.createElement("style");
      (doc.head || doc.documentElement).appendChild(style);
      const sheet = style.sheet;
      for (const rule of splitRules(cssText)) {
        try {
          sheet.insertRule(rule, sheet.cssRules.length);
        } catch {
        }
      }
      return sheet;
    }
  }
  function splitRules(css) {
    const out = [];
    let depth = 0, start = 0;
    for (let i = 0; i < css.length; i++) {
      const ch = css[i];
      if (ch === "{") depth++;
      else if (ch === "}") {
        depth--;
        if (depth === 0) {
          out.push(css.slice(start, i + 1).trim());
          start = i + 1;
        }
      }
    }
    return out.filter(Boolean);
  }
  var fmtAgo = (iso, now = Date.now()) => {
    if (!iso) return "";
    const s = Math.max(0, Math.round((now - new Date(iso).getTime()) / 1e3));
    if (s < 60) return s + "s ago";
    if (s < 3600) return Math.round(s / 60) + "m ago";
    if (s < 86400) return Math.round(s / 3600) + "h ago";
    return Math.round(s / 86400) + "d ago";
  };
  var fmtBytes = (n) => n < 1024 ? n + " B" : n < 1048576 ? (n / 1024).toFixed(1) + " KB" : (n / 1048576).toFixed(2) + " MB";
  var fmtCountdown = (untilMs, now = Date.now()) => {
    const s = Math.max(0, Math.ceil((untilMs - now) / 1e3));
    return s ? `${s}s` : "now";
  };

  var TOKENS = `color-scheme: dark; --bg:#0f1115; --panel:#171a21; --line:#2a2f3a; --ink:#e8eaf0; --mute:#9aa3b2; --ok:#5fbf8a; --warn:#d9a441; --bad:#e0655f; --acc:#7aa2ff; --sent:#b08cff;`;
  var CSS_DOC = `
html, body { margin:0; padding:0; background:#0f1115; color:#e8eaf0; font: 15px/1.45 system-ui, -apple-system, "Segoe UI", Roboto, sans-serif; -webkit-text-size-adjust:100%; }
`;
  var CSS = `
.f-host { ${TOKENS} position:fixed; inset:0; z-index:2147483000; overflow:auto; -webkit-overflow-scrolling:touch; background:var(--bg); color:var(--ink); font: 15px/1.45 system-ui, -apple-system, "Segoe UI", Roboto, sans-serif; }
.f-app { ${TOKENS} min-height:100%; display:flex; flex-direction:column; background:var(--bg); color:var(--ink); font: 15px/1.45 system-ui, -apple-system, "Segoe UI", Roboto, sans-serif; text-align:left; }
.f-app, .f-app * { box-sizing:border-box; }
.f-app .f-top { position:sticky; top:0; z-index:10; background:var(--panel); border-bottom:1px solid var(--line); display:flex; align-items:center; gap:8px; padding:8px 10px; }
.f-app .f-title { font-weight:700; letter-spacing:.02em; }
.f-app .f-ver { color:var(--mute); font-size:12px; margin-left:auto; }
.f-app .f-exit { min-height:44px; padding:4px 12px; font-size:13px; }
.f-app .f-nav { display:flex; gap:4px; overflow-x:auto; padding:6px 8px; background:var(--panel); border-bottom:1px solid var(--line); }
.f-app .f-nav button { flex:1 1 0; min-width:0; min-height:44px; padding:8px 4px; font-size:14px; }
.f-app .f-nav button[aria-current="page"] { background:var(--acc); color:#0b0d12; }
.f-app .f-main { flex:1; padding:12px 10px 80px; max-width:760px; width:100%; margin:0 auto; }
.f-app h2 { font-size:17px; margin:14px 0 8px; overflow-wrap:anywhere; } .f-app h3 { font-size:14px; color:var(--mute); margin:12px 0 6px; text-transform:uppercase; letter-spacing:.06em; }
.f-app button, .f-app .f-btn { font:inherit; min-height:44px; padding:8px 14px; border:1px solid var(--line); border-radius:8px; background:#222733; color:var(--ink); cursor:pointer; }
.f-app button:disabled { opacity:.45; cursor:default; }
.f-app button.f-primary { background:var(--acc); color:#0b0d12; border-color:transparent; font-weight:600; }
.f-app button.f-danger { border-color:var(--bad); color:var(--bad); }
.f-app input[type=text], .f-app input[type=password], .f-app input[type=search], .f-app textarea { font:inherit; width:100%; min-height:44px; padding:8px 10px; border:1px solid var(--line); border-radius:8px; background:#0b0d12; color:var(--ink); }
.f-app textarea { min-height:160px; font-family: ui-monospace, Menlo, monospace; font-size:12px; }
.f-app .f-card { background:var(--panel); border:1px solid var(--line); border-radius:10px; padding:10px 12px; margin:8px 0; }
.f-app .f-row { display:flex; align-items:center; gap:10px; padding:10px 0; border-bottom:1px solid var(--line); }
.f-app .f-row:last-child { border-bottom:0; }
.f-app .f-row.f-tap { cursor:pointer; } .f-app .f-row.f-tap:active { background:#1d2230; }
.f-app .f-row.f-sel { background:#1a2237; box-shadow: inset 3px 0 0 var(--acc); padding-left:8px; }
.f-app .f-list { margin:6px 0 0; padding-left:20px; } .f-app .f-list li { margin:4px 0; }
.f-app .f-more summary { font-size:13px; min-height:44px; display:flex; align-items:center; }
.f-app details.f-group { border-bottom:1px solid var(--line); } .f-app details.f-group > summary { padding:12px 0; color:var(--ink); }
.f-app .f-grow { flex:1; min-width:0; overflow-wrap:anywhere; } .f-app .f-mute { color:var(--mute); font-size:13px; } .f-app .f-mono { font-family: ui-monospace, Menlo, monospace; font-size:12px; word-break:break-all; }
.f-app .f-pill { display:inline-block; padding:2px 8px; border-radius:999px; font-size:12px; font-weight:600; border:1px solid var(--line); color:var(--mute); }
.f-app .f-pill.PLANNED { color:var(--mute); } .f-app .f-pill.SENT { color:var(--sent); border-color:var(--sent); } .f-app .f-pill.CONFIRMED { color:var(--acc); border-color:var(--acc); }
.f-app .f-pill.VERIFIED, .f-app .f-pill.DONE { color:var(--ok); border-color:var(--ok); } .f-app .f-pill.FAILED, .f-app .f-pill.ABORTED { color:var(--bad); border-color:var(--bad); }
.f-app .f-pill.ORPHANED, .f-app .f-pill.PAUSED, .f-app .f-pill.INCOMPLETE { color:var(--warn); border-color:var(--warn); } .f-app .f-pill.SKIPPED { color:var(--mute); }
.f-app .f-authbar { padding:0 10px; max-width:760px; width:100%; margin:0 auto; }
.f-app .f-authbar:empty { display:none; }
.f-app .f-banner { padding:10px 12px; border-radius:10px; margin:8px 0; border:1px solid; overflow-wrap:anywhere; }
.f-app .f-banner.f-compact { display:flex; align-items:center; justify-content:space-between; gap:8px; padding:2px 4px 2px 12px; }
.f-app .f-banner.f-compact .f-actions { margin:0; }
.f-app .f-banner.warn { border-color:var(--warn); background:#2a2312; } .f-app .f-banner.bad { border-color:var(--bad); background:#2a1515; } .f-app .f-banner.ok { border-color:var(--ok); background:#12261c; } .f-app .f-banner.info { border-color:var(--acc); background:#141b2e; }
.f-app .f-bar { height:6px; background:#0b0d12; border-radius:4px; overflow:hidden; margin:6px 0; } .f-app .f-bar > i { display:block; height:100%; background:var(--acc); }
.f-app .f-bar.warn > i { background:var(--warn); }
.f-app .f-actions { display:flex; gap:8px; flex-wrap:wrap; margin-top:8px; }
.f-app .f-kv { display:grid; grid-template-columns: auto 1fr; gap:4px 12px; font-size:13px; } .f-app .f-kv b { color:var(--mute); font-weight:500; }
.f-app .f-err { white-space:pre-wrap; overflow-wrap:anywhere; font-family: ui-monospace, Menlo, monospace; font-size:12px; color:#ffb4b0; }
.f-app .f-toast { position:fixed; left:10px; right:10px; bottom:12px; z-index:2147483001; }
.f-app .f-toast .f-banner { cursor:pointer; box-shadow:0 4px 16px #000a; }
.f-app details summary { cursor:pointer; color:var(--mute); }
.f-boot .f-mute { color:var(--mute); font-size:13px; }
.f-boot p { margin:8px 0; max-width:52ch; }
.f-boot { ${TOKENS} padding:16px; background:var(--bg); color:var(--ink); min-height:100vh; font: 15px/1.45 system-ui, -apple-system, "Segoe UI", Roboto, sans-serif; }
`;

  function harvestEntry(i) {
    const diffs = i.diffs || [];
    const assertedKeys = Array.isArray(i.asserted) ? i.asserted.length : i.assertedRules ? 1 : 0;
    const landed = i.state === "VERIFIED" || i.entityId && i.phase === "verify";
    const state = i.state === "FAILED" ? "error" : i.state === "SKIPPED" ? "skipped" : landed ? "ok" : "pending";
    return {
      name: i.name,
      srcId: i.srcId,
      entity: i.entity,
      slot: i.op === "create" ? "create" : "edit",
      op: i.op,
      state,
      forgeState: i.state,
      phase: i.phase,
      detail: i.error || i.reconciled || "",
      verdict: i.verify || null,
      asserted: assertedKeys || diffs.length ? {
        ok: Math.max(0, assertedKeys - diffs.length),
        fail: diffs.map((d) => ({ k: d.key, c: "mismatch", d: [`sent ${JSON.stringify(d.sent)}  live ${JSON.stringify(d.live)}`] }))
      } : null,
      diffs,
      id: i.entityId || i.targetId || null
    };
  }
  var EXT_MIME2 = Object.freeze({
    webp: "image/webp",
    png: "image/png",
    jpg: "image/jpeg",
    jpeg: "image/jpeg",
    gif: "image/gif",
    avif: "image/avif"
  });
  var extOf2 = (n) => {
    const m = /\.([A-Za-z0-9]+)$/.exec(String(n ?? ""));
    return m ? m[1].toLowerCase() : null;
  };
  function imagePick(name, file, imgSizes = {}, slug = "imageUploader") {
    const ceiling = (SLUGS[slug] ?? SLUGS.imageUploader).maxBytes;
    const has = imgSizes && Object.prototype.hasOwnProperty.call(imgSizes, name);
    const expectedBytes = has ? Number(imgSizes[name]) : null;
    if (!file) return { name, ok: false, state: "missing", expectedBytes, ceiling, picked: null, renamed: false, problems: [] };
    const picked = { name: file.name ?? null, size: Number(file.size), type: file.type || null };
    const problems = [];
    if (expectedBytes == null || !Number.isFinite(expectedBytes)) {
      problems.push(`the manifest has no imgSizes entry for ${name}, so these bytes cannot be checked against it`);
    } else if (picked.size !== expectedBytes) {
      problems.push(`selected file is ${picked.size} bytes; the manifest ledger says ${name} is ${expectedBytes}`);
    }
    if (Number.isFinite(picked.size) && picked.size > ceiling) {
      problems.push(`selected file is ${picked.size} bytes, over the ${slug} ceiling of ${ceiling}`);
    }
    const wantMime = EXT_MIME2[extOf2(name)] ?? null;
    if (picked.type && !picked.type.startsWith("image/")) problems.push(`selected file is ${picked.type}, not an image`);
    else if (picked.type && wantMime && picked.type !== wantMime) problems.push(`selected file is ${picked.type}; ${name} is a ${extOf2(name)}`);
    return {
      name,
      ok: !problems.length,
      state: problems.length ? "refused" : "ready",
      expectedBytes,
      ceiling,
      picked,
      renamed: !!(picked.name && picked.name !== name),
      problems
    };
  }
  function imagePicks(names, files, imgSizes = {}, slug = "imageUploader") {
    const get = files && typeof files.get === "function" ? (n) => files.get(n) : () => null;
    return (names ?? []).map((n) => imagePick(n, get(n) ?? null, imgSizes, slug));
  }
  function unusablePicks(picks) {
    return (picks ?? []).filter((p) => !p.ok);
  }
  function resumeBlockedReason(job, auth) {
    if (!job || !job.pause || job.pause.reason !== "SESSION") return null;
    if (!auth || auth.ready) return null;
    return "TNR authentication is still unavailable. Sign in to the game and re-check the session; resuming now would send nothing.";
  }
  function blockedPaths(auth, plan, manifest) {
    if (!auth) return [];
    try {
      return protectedPathsFor(plan, manifest).filter((path) => !auth.allows(path));
    } catch {
      return [];
    }
  }
  function authFacts(auth, busy) {
    if (!auth) return null;
    const state = auth.state;
    if (state === AUTH.READY) return { level: "ok", ready: true, probing: false, signedOut: false, detail: auth.detail ?? null };
    if (state === AUTH.PROBING || busy) return { level: "info", ready: false, probing: true, signedOut: false, detail: auth.detail ?? null };
    return { level: "bad", ready: false, probing: false, signedOut: state === AUTH.SIGNED_OUT, detail: auth.detail ?? null };
  }
  function runHeadline(job, summary) {
    const captures = [...job.capturesBefore || [], ...job.capturesAfter || []];
    const outcome = jobOutcome(job);
    const full = captures.filter((capture) => capture.persist === "full");
    const detail = job.items.length ? `${Object.entries(summary.counts).map(([k, v]) => `${v} ${k.toLowerCase()}`).join(", ")} \xB7 ${summary.verify.match} verified, ${summary.verify.drift} drift, ${summary.verify.unread} unread` : `${captures.filter((capture) => capture.ok).length}/${captures.length} captures read ok${full.length ? ` \xB7 ${full.filter((capture) => capture.persistOk === true).length}/${full.length} full bodies persisted` : ""} \xB7 zero mutations`;
    const kind = outcome === "success" ? "ok" : outcome === "failed" ? "bad" : "warn";
    if (job.pause && job.pause.reason === "SESSION") {
      return {
        outcome,
        kind: "bad",
        ms: 12e3,
        sessionPause: true,
        text: `job PAUSED: TNR authentication unavailable${job.pause.path ? ` on ${job.pause.path}` : ""}. Nothing further was sent. Sign in and resume.`
      };
    }
    const n = job.items.length;
    const parts = [
      ["failed", job.items.filter((i) => i.state === "FAILED").length],
      ["changed after writing", job.items.filter((i) => i.verify === "drift").length],
      ["could not be read back", job.items.filter((i) => i.verify === "unread").length],
      ["skipped", job.items.filter((i) => i.state === "SKIPPED").length]
    ].filter(([, c]) => c).map(([w, c]) => `${c} ${w}`).join(", ");
    const head = !n ? outcome === "success" ? "Capture finished" : "Capture finished with problems" : summary.state === "PAUSED" ? "Paused" : outcome === "success" && job.items.some((i) => i.verify === "suggested") ? `Finished: ${job.items.filter((i) => i.verify === "suggested").length} sent for review; nothing changes until approved` : outcome === "success" ? `Finished: ${n === 1 ? "1 item" : `all ${n} items`} written and verified` : outcome === "failed" ? `Finished with failures: ${parts}` : `Finished, not fully verified: ${parts || "verification outstanding"}`;
    return { outcome, kind, ms: 8e3, sessionPause: false, text: n ? `${head}.` : `${head}: ${detail}` };
  }
  function postflight(job) {
    return {
      match: job.items.filter((i) => i.verify === "match").length,
      diff: job.items.filter((i) => i.verify === "drift").length,
      unverified: job.items.filter((i) => i.verify === "unread").length,
      failed: job.items.filter((i) => i.state === "FAILED").length,
      skipped: job.items.filter((i) => i.state === "SKIPPED").length,
      unresolved: job.items.filter((i) => !["VERIFIED", "FAILED", "SKIPPED"].includes(i.state)).length
    };
  }

  function makeFile(bytes, name, type) {
    const F = globalThis.File;
    if (typeof F === "function") return new F([bytes], name, { type });
    const B2 = globalThis.Blob;
    if (typeof B2 === "function") {
      const blob = new B2([bytes], { type });
      return Object.defineProperties(blob, { name: { value: name }, lastModified: { value: 0 } });
    }
    throw new Error("this host has neither File nor Blob; repo-backed image packs need one to upload");
  }
  async function prepareImagePack({ github, assetCache, digest, now = () => Date.now() }, { pack, names = [], force = false } = {}) {
    const work = packWork(pack, names);
    const unbound = unboundNames(pack, names);
    const entries = [];
    const staged = [];
    for (const want of work) {
      const { entry, stage } = await one({ github, assetCache, digest, now }, want, force);
      entries.push(entry);
      if (stage) staged.push(stage);
    }
    return { ref: pack ? pack.ref : null, entries, unbound, ok: entries.length === staged.length, staged };
  }
  function commitImagePack(runner, { pack, names = [], staged = [] } = {}) {
    for (const { name } of packWork(pack, names)) {
      runner.files.delete(name);
      runner.imgProvenance.delete(name);
    }
    for (const { name, file, prov } of staged) {
      runner.files.set(name, file);
      runner.imgProvenance.set(name, { ...prov, file });
    }
    return staged.length;
  }
  async function one(ctx, want, force) {
    const { github, assetCache, digest, now } = ctx;
    const base2 = { name: want.name, path: want.path, ref: want.ref, sha256: want.sha256, bytes: want.bytes };
    const fail = (o) => ({ entry: { ...base2, source: null, size: null, digest: null, ...o }, stage: null });
    if (typeof digest !== "function") {
      return fail({ state: "error", error: "SHA-256 is not available in this context, so repo-backed bytes cannot be verified; Forge will not use them unverified" });
    }
    let cached = null;
    if (!force) {
      try {
        cached = await assetCache.get(want.sha256);
      } catch {
        cached = null;
      }
    }
    let source = cached ? "cache" : "repo";
    let bytes;
    for (let attempt = 0; attempt < 2; attempt++) {
      if (source === "cache") {
        bytes = cached.bytes;
      } else {
        try {
          bytes = await github.raw(want.path, want.ref);
        } catch (e) {
          return fail({ state: "error", source: "repo", error: `could not fetch ${want.path} at ${want.ref.slice(0, 12)}: ${e && e.message || e}` });
        }
      }
      const size = bytes.byteLength ?? bytes.length ?? 0;
      let hex = null;
      if (size === want.bytes) {
        try {
          hex = toHex(await digest(bytes));
        } catch (e) {
          return fail({ state: "error", source, size, error: `could not compute SHA-256 for ${want.name}: ${e && e.message || e}` });
        }
      }
      if (size === want.bytes && hex === want.sha256) {
        if (source === "repo") {
          try {
            await assetCache.put({ sha256: want.sha256, bytes, path: want.path, ref: want.ref });
          } catch {
          }
        }
        let file;
        try {
          file = makeFile(bytes, want.name, mimeOf(want.name));
        } catch (e) {
          return fail({ state: "error", source, size, digest: hex, error: e && e.message || String(e) });
        }
        return {
          entry: { ...base2, state: "ready", source, size, digest: hex, error: null },
          stage: { name: want.name, file, prov: { sha256: want.sha256, path: want.path, ref: want.ref, bytes: want.bytes, at: now() } }
        };
      }
      const why = size !== want.bytes ? `is ${size} bytes; the pack says ${want.bytes}` : `hashes to ${hex}; the pack says ${want.sha256}`;
      if (source === "cache") {
        try {
          await assetCache.delete(want.sha256);
        } catch {
        }
        cached = null;
        source = "repo";
        continue;
      }
      return fail({
        state: "refused",
        source,
        size,
        digest: hex,
        error: `${want.path} at ${want.ref.slice(0, 12)} ${why}. Nothing was uploaded and this image cannot be used; the manifest and the repository disagree about which file this is.`
      });
    }
    return fail({ state: "error", source, error: "verification did not settle" });
  }
  function packGateProblems(pack, names, runner) {
    const problems = [];
    for (const want of packWork(pack, names)) {
      const prov = runner.imgProvenance.get(want.name) ?? null;
      const file = runner.files.get(want.name) ?? null;
      if (!prov || !file) {
        problems.push(`${want.name} is bound to ${want.path} at ${want.ref.slice(0, 12)} but has not been fetched and verified`);
        continue;
      }
      if (prov.sha256 !== want.sha256) {
        problems.push(`${want.name} was verified as ${prov.sha256.slice(0, 12)} but the manifest now binds ${want.sha256.slice(0, 12)}`);
        continue;
      }
      if (prov.ref !== want.ref || prov.path !== want.path) {
        problems.push(`${want.name} was fetched from ${prov.path} at ${prov.ref.slice(0, 12)}, not ${want.path} at ${want.ref.slice(0, 12)}`);
        continue;
      }
      if (!prov.file || file !== prov.file) {
        problems.push(`${want.name} is no longer holding the exact file that was verified against ${want.sha256.slice(0, 12)}; re-fetch it from the repository`);
        continue;
      }
      const size = Number(file.size);
      if (size !== want.bytes) {
        problems.push(`${want.name} is holding ${size} bytes, not the ${want.bytes} the pack names`);
      }
    }
    return problems;
  }

  var pill = (state) => h("span", { class: "f-pill " + state }, state);
  var plural = (n, one2, many = one2 + "s") => `${n} ${n === 1 ? one2 : many}`;
  var base = (p) => String(p || "").replace(/^push\//, "");
  var TERMINAL = ["VERIFIED", "FAILED", "SKIPPED"];
  var PAUSE_WORDS = {
    USER: "Paused by you",
    SESSION: "Paused: signed out of the game",
    NETWORK: "Paused: connection problem",
    TOO_MANY_REQUESTS: "Paused: game rate limit reached",
    ORPHANED: "Paused: an item needs your decision",
    DEPENDENCY: "Paused: waiting on an earlier item",
    UNDECODABLE_RESPONSE: "Paused: unreadable game reply",
    AMBIGUOUS: "Paused: last write uncertain",
    VISIBILITY: "Paused: record not visible",
    STALE_PREVIEW: "Paused: a record changed since the preview",
    STALE_BINDINGS: "Paused: saved IDs out of date",
    UNRESOLVED_IMPORT: "Paused: earlier import unresolved"
  };
  var pauseWords = (pause) => PAUSE_WORDS[pause.reason] ?? `Paused (${pause.reason})`;
  function jobLabel(job) {
    if (job.collection) return `${base(job.collection.path)} \xB7 tree ${job.collection.index + 1}/${job.collection.total}${job.collection.name ? ` \xB7 ${job.collection.name}` : ""}`;
    if (job.bloodrightImport) return `Bloodright \xB7 ${job.bloodlineName || job.bloodrightImport.bloodlineId}`;
    return base(job.manifestPath) || job.jobId;
  }
  function jobPill(app, job) {
    if (job.state === "RUNNING" && app.state.running !== job.jobId) return h("span", { class: "f-pill PAUSED" }, "INTERRUPTED");
    if (job.state === "DONE") {
      const outcome = jobOutcome(job);
      if (outcome === "failed") return h("span", { class: "f-pill FAILED" }, "FAILURES");
      if (outcome === "unverified") return h("span", { class: "f-pill INCOMPLETE" }, "UNVERIFIED");
    }
    return pill(job.state);
  }
  var resumeLabel = (job) => job.items.some((i) => i.state === "SENT") ? "Reconcile & resume" : job.state === "INCOMPLETE" ? "Re-read unverified items" : "Resume";
  function jobRow(app, j) {
    const counts = {};
    for (const it of j.items) counts[it.state] = (counts[it.state] ?? 0) + 1;
    return h(
      "div",
      { class: "f-row f-tap", onClick: () => app.go("run", { jobId: j.jobId }) },
      h(
        "div",
        { class: "f-grow" },
        h("div", {}, jobLabel(j), " ", jobPill(app, j)),
        h("div", { class: "f-mute" }, `${plural(j.items.length, "item")}${j.items.length ? ` \xB7 ${Object.entries(counts).map(([k, v]) => `${v} ${k.toLowerCase()}`).join(", ")}` : ""} \xB7 ${fmtAgo(j.startedAt, app.now())}`)
      )
    );
  }
  function JobsScreen(app) {
    const jobs = app.journal.listJobs();
    const open = app.journal.resumable();
    const orphans = jobs.flatMap((j) => j.items.filter((it) => it.state === "ORPHANED").map((it) => ({ job: j, it })));
    const root = h("section", {});
    for (const j of open) {
      const blockedReason = app.resumeBlockedReason ? app.resumeBlockedReason(j) : null;
      root.appendChild(h(
        "div",
        { class: "f-banner warn" },
        h("div", {}, h("b", {}, "Open job: "), jobLabel(j), " ", jobPill(app, j)),
        j.state === "INCOMPLETE" ? h("div", { class: "f-mute" }, `Finished unverified: ${plural(j.items.filter((i) => !TERMINAL.includes(i.state)).length, "item")} still to read back. Resuming only re-reads; it cannot re-send.`) : null,
        j.pause ? h("div", { class: "f-mute" }, `${pauseWords(j.pause)}${j.pause.path ? " on " + j.pause.path : ""}${j.pause.until ? " \xB7 retry allowed in " + fmtCountdown(j.pause.until, app.now()) : ""}${j.pause.detail ? " \xB7 " + j.pause.detail : ""}`) : null,
        blockedReason ? h("div", { class: "f-err" }, blockedReason) : null,
        h(
          "div",
          { class: "f-actions" },
          h("button", { class: "f-primary", disabled: !!blockedReason, onClick: () => app.resumeJob(j.jobId) }, resumeLabel(j)),
          h("button", { onClick: () => app.go("run", { jobId: j.jobId }) }, "Open")
        )
      ));
    }
    if (orphans.length) {
      root.appendChild(h("h2", {}, `Orphans needing a decision (${orphans.length})`));
      for (const { job, it } of orphans) root.appendChild(OrphanCard(app, job, it));
    }
    root.appendChild(h("h2", {}, "Recent runs"));
    if (!jobs.length) root.appendChild(h("div", { class: "f-mute" }, "No jobs yet. Pick a manifest to start one."));
    const rows = [], groups =  new Map();
    for (const j of jobs) {
      const g = j.collection?.id;
      if (!g) {
        rows.push({ job: j });
        continue;
      }
      if (!groups.has(g)) {
        groups.set(g, []);
        rows.push({ group: g });
      }
      groups.get(g).push(j);
    }
    for (const r of rows.slice(0, 20)) {
      if (r.job) {
        root.appendChild(jobRow(app, r.job));
        continue;
      }
      const trees = groups.get(r.group).sort((a, b) => a.collection.index - b.collection.index);
      const first = trees[0], ok = trees.filter((j) => j.state === "DONE" && jobOutcome(j) === "success").length;
      root.appendChild(h(
        "details",
        { class: "f-group" },
        h("summary", {}, `${base(first.collection.path)} \xB7 collection \xB7 ${ok}/${first.collection.total} trees verified \xB7 ${fmtAgo(first.startedAt, app.now())}`),
        trees.map((j) => jobRow(app, j))
      ));
    }
    return root;
  }
  function OrphanCard(app, job, it) {
    const cands = it.candidates || [];
    const card = h(
      "div",
      { class: "f-card" },
      h("div", {}, h("b", {}, it.name), " ", h("span", { class: "f-mute" }, `${it.entity} \xB7 ${jobLabel(job)} \xB7 item ${it.idx + 1}`)),
      h("div", { class: "f-mute" }, it.error || "ambiguous")
    );
    if (cands.length) {
      card.appendChild(h("h3", {}, "Candidates on the server"));
      for (const c of cands) {
        const id2 = typeof c === "string" ? c : c.id;
        const name = typeof c === "string" ? "" : c.name;
        const evidence = typeof c === "object" && c.matches !== void 0 ? c.matches ? "matches the plan (may still be someone else's)" : `differs on ${c.differs.join(", ")}` : null;
        card.appendChild(h(
          "div",
          { class: "f-row" },
          h("div", { class: "f-grow" }, h("div", { class: "f-mono" }, id2), name ? h("div", { class: "f-mute" }, name) : null, evidence ? h("div", { class: "f-mute" }, evidence) : null),
          h("button", { onClick: () => app.confirm(`Adopt ${id2} as "${it.name}"? ${evidence ? "It is read back and verified, never re-saved." : "The job will continue with its update."}`, () => app.adopt(job.jobId, it.idx, id2)) }, "Adopt")
        ));
      }
    } else if (it.op === "create" || !it.entityId) {
      const inp = h("input", { type: "text", placeholder: "paste an id to adopt" });
      card.appendChild(h("div", { class: "f-actions" }, inp, h("button", { onClick: () => {
        const v = inp.value.trim();
        if (v) app.confirm(`Adopt ${v}?`, () => app.adopt(job.jobId, it.idx, v));
      } }, "Adopt id")));
    } else {
      card.appendChild(h(
        "div",
        { class: "f-actions" },
        h("button", { onClick: () => app.confirm(`Re-send the ${it.phase} for "${it.name}" to ${it.entityId}? Only do this if you have checked the record.`, () => app.adopt(job.jobId, it.idx, it.entityId)) }, `Re-send ${it.phase}`)
      ));
    }
    card.appendChild(h("div", { class: "f-actions" }, h("button", { class: "f-danger", onClick: () => app.confirm(`Skip "${it.name}"? Nothing is deleted; the server row (if any) stays.`, () => app.skip(job.jobId, it.idx)) }, "Skip (leave as is)")));
    return card;
  }
  function summaryText(e) {
    if (!e.summary) return e.loading ? "loading\u2026" : e.error || "";
    const x = e.summary;
    if (x.trees) return `${x.title} \xB7 ${plural(x.trees, "tree")} \xB7 ${plural(x.skills, "skill")}`;
    return `${x.title || "(untitled)"} \xB7 ${plural(x.items, "item")}${x.creates ? ` (${x.creates} new)` : ""}${x.captures ? ` \xB7 ${plural(x.captures, "capture")}` : ""}`;
  }
  function listingHint(error) {
    return /HTTP 40[13]/.test(error) ? " GitHub refused the listing. Wait a few minutes (GitHub limits reads without a token) or add a GitHub token in Settings, then tap Refresh." : " Check the connection, then tap Refresh.";
  }
  function ManifestsScreen(app) {
    const root = h("section", {});
    const q = h("input", { type: "search", placeholder: "search filename, number, title", value: app.view.pickerQuery || "", onInput: (e) => {
      app.view.pickerQuery = e.target.value;
      renderList();
    } });
    const list = h("div", {});
    const status = h("div", { class: "f-mute" });
    root.append(h("div", { class: "f-actions" }, q, h("button", { onClick: () => app.loadPicker(true) }, "Refresh")));
    if (app.state.selected) root.appendChild(SelectedManifest(app));
    else if (app.state.opening) root.appendChild(h(
      "div",
      { class: "f-card" },
      h("h2", {}, app.state.opening.name),
      h("div", { class: "f-banner info" }, `Preparing: ${app.state.opening.step}\u2026 Nothing is written yet.`)
    ));
    else if (app.state.openError) root.appendChild(h(
      "div",
      { class: "f-card" },
      h("h2", {}, app.state.openError.name),
      h("div", { class: "f-banner bad" }, h("b", {}, "Could not open: "), h("div", { class: "f-err" }, app.state.openError.text)),
      h("div", { class: "f-actions" }, h("button", { onClick: () => app.clearSelection() }, "Clear"))
    ));
    root.append(status, list);
    const current = app.state.selected?.entry?.name ?? app.state.opening?.name ?? app.state.openError?.name ?? null;
    const texts =  new Map();
    let shown = null;
    function renderList() {
      const entries = app.state.picker || [];
      const needle = (app.view.pickerQuery || "").toLowerCase();
      const seen = new Set(app.journal.listJobs().map((j) => j.collection?.path ?? j.manifestPath));
      const rows = entries.filter((e) => !needle || e.name.toLowerCase().includes(needle) || String(e.number ?? "").includes(needle) || (e.summary?.title || "").toLowerCase().includes(needle));
      const key = rows.map((e) => e.path).join("\n");
      if (key === shown && rows.length) {
        for (const e of rows) {
          const t = texts.get(e.path), want = summaryText(e);
          if (t && t.textContent !== want) t.textContent = want;
        }
      } else {
        shown = key;
        texts.clear();
        replace(list, rows.length ? rows.map((e) => {
          const text = h("div", { class: "f-mute" }, summaryText(e));
          texts.set(e.path, text);
          return h(
            "div",
            { class: "f-row f-tap" + (e.name === current ? " f-sel" : ""), onClick: () => app.selectManifest(e) },
            h(
              "div",
              { class: "f-grow" },
              h("div", {}, e.number != null ? h("b", {}, "#" + e.number + " ") : null, e.name, seen.has(e.path) ? h("span", { class: "f-pill VERIFIED", style: { marginLeft: "6px" } }, "ran") : null),
              text
            )
          );
        }) : h("div", { class: "f-mute" }, app.state.pickerError ? "" : "nothing matches"));
      }
      replace(status, app.state.pickerError ? h("div", { class: "f-banner bad" }, h("b", {}, "Could not list manifests: "), app.state.pickerError, listingHint(app.state.pickerError)) : `${plural(entries.length, "manifest")}` + (app.state.pickerAt ? ` \xB7 listed ${fmtAgo(app.state.pickerAt, app.now())}` : ""));
    }
    renderList();
    app.view.renderPicker = renderList;
    if (!app.state.picker) app.loadPicker(false);
    return root;
  }
  function captureLabel(captures) {
    const n = captures.length;
    if (!n) return "";
    const full = captures.filter((c) => c && c.persist === "full").length;
    const noun = `capture${n === 1 ? "" : "s"}`;
    if (!full) return `${n} ${noun}`;
    if (full === n) return `${n} full ${noun}`;
    return `${n} ${noun} (${full} full)`;
  }
  var FOLD_AT = 12;
  var fold = (rows, label) => rows.length > FOLD_AT ? [h("details", {}, h("summary", {}, label), rows)] : rows;
  function keysText(data) {
    let out = "";
    for (const k of Object.keys(data)) {
      if ((out + k).length > 120) return out + "\u2026";
      out += (out ? ", " : "") + k;
    }
    return out;
  }
  function SelectedManifest(app) {
    const s = app.state.selected;
    const captures = [...s.manifest.capture.before, ...s.manifest.capture.after];
    const captureCount = captures.length;
    const fullCount = captures.filter((c) => c.persist === "full").length;
    const label = captureLabel(captures);
    const itemCount = s.manifest.items?.length ?? s.plan.length;
    const readOnly = !s.bloodright && itemCount === 0;
    const count = (entity) => s.plan.filter((i) => i.entity === entity).length;
    const creates = s.plan.filter((i) => i.op === "create").length;
    const imgs = s.images || [];
    const scope = s.collection ? `${plural(s.collection.length, "tree")} \xB7 ${plural(count("skillTree"), "skill")} \xB7 ${plural(count("skillTreeFolder"), "folder")} \xB7 ${plural(imgs.length, "icon")}` : `${plural(itemCount, "item")}${captureCount ? ` \xB7 ${label}` : ""}`;
    const card = h("div", { class: "f-card" }, h("h2", {}, s.entry.name), h("div", { class: "f-mute" }, `${scope}${s.manifest.hash ? ` \xB7 manifest hash ${s.manifest.hash}` : ""}`));
    const suggest = !!s.manifest.policy?.suggest;
    if (readOnly) card.appendChild(h("div", { class: "f-banner info" }, "Read-only capture job: zero mutations."));
    if (suggest) card.appendChild(h("div", { class: "f-banner info" }, h("b", {}, "Suggest mode. "), "Each edit goes to the content review desk. Nothing changes in the game until a reviewer approves it."));
    if (fullCount) card.appendChild(h(
      "div",
      { class: "f-banner warn" },
      h("b", {}, `${fullCount} full capture${fullCount === 1 ? "" : "s"}. `),
      `Each exact record body goes into the results bundle (committed to the repository when GitHub sync is on).${readOnly ? " Still queries only; zero mutations." : ""} Paths: ${[...new Set(captures.filter((c) => c.persist === "full").map((c) => c.proc))].join(", ")}.`
    ));
    if (s.problems.length) card.appendChild(h("div", { class: "f-banner bad" }, h("b", {}, "Cannot run: "), h("div", { class: "f-err" }, s.problems.join("\n"))));
    const blocked = app.blockedPaths ? app.blockedPaths(s.plan, s.manifest) : [];
    if (blocked.length) card.appendChild(h(
      "div",
      { class: "f-banner bad" },
      h("b", {}, "Blocked: TNR authentication is unavailable. "),
      `This manifest needs ${blocked.join(", ")}, which needs a signed-in session. Nothing will be sent. Sign in, then re-check above.`
    ));
    const picks = imagePicks(imgs, app.runner.files, s.manifest.imgSizes, "imageUploader");
    const pack = s.pack || null;
    const packResult = s.packResult || null;
    const packEntry = (name) => (packResult && packResult.entries ? packResult.entries.find((e) => e.name === name) : null) || null;
    const badImgs = unusablePicks(picks);
    const imagesHead = h("h3", {}, `Images (${imgs.length})`);
    const packProblems = packGateProblems(pack, imgs, app.runner);
    if (packProblems.length && pack && !packResult) {
      card.appendChild(h("div", { class: "f-banner info" }, `Verifying ${plural(packProblems.length, "image")}\u2026`));
    } else if (packProblems.length) {
      card.appendChild(h(
        "div",
        { class: "f-banner bad" },
        h("b", {}, `Cannot run: ${plural(packProblems.length, "repo-backed image")} not verified. `),
        h("details", {}, h("summary", {}, "Show details"), h("div", { class: "f-err" }, packProblems.join("\n"))),
        h("div", { class: "f-actions" }, h("button", { onClick: () => app.prepareImages(true) }, "Re-fetch from repository"))
      ));
    }
    const unpicked = badImgs.filter((p) => !packBinds(pack, p.name));
    if (unpicked.length) card.appendChild(h(
      "div",
      { class: "f-banner warn" },
      h("b", {}, `Pick ${plural(unpicked.length, "image")} below to enable Start. `),
      unpicked.map((p) => p.name).join(", "),
      h("div", { class: "f-actions" }, h("button", { onClick: () => imagesHead.scrollIntoView({ block: "start" }) }, "Go to images"))
    ));
    card.appendChild(h(
      "div",
      { class: "f-actions" },
      h("button", {
        class: "f-primary",
        disabled: s.problems.length > 0 || badImgs.length > 0 || blocked.length > 0 || packProblems.length > 0,
        onClick: () => app.confirm(
          readOnly ? `Run read-only capture job for ${s.entry.name}: ${label}?${fullCount ? ` ${fullCount} exact record ${fullCount === 1 ? "body is" : "bodies are"} written into the results bundle.` : ""} No mutations will be sent.` : s.collection ? `Start ${plural(s.collection.length, "Bloodright tree")} (${plural(count("skillTree"), "skill")}, all hidden)? This writes to the game.` : suggest ? `Send ${plural(s.plan.length, "suggestion")} from ${s.entry.name} for review? Nothing changes until approved.` : `Start ${s.entry.name}: ${plural(s.plan.length, "item")} (${creates} new)${fullCount ? `, ${label}` : ""}? This writes to the game.`,
          () => app.startJob()
        )
      }, readOnly ? "Run captures" : s.collection ? "Start all trees" : suggest ? "Send for review" : "Start job"),
      h("button", { onClick: () => app.clearSelection() }, "Clear")
    ));
    if (s.manifest.poolResolved) card.appendChild(h("div", { class: "f-mute" }, `${s.manifest.poolResolved} pool code(s) resolved to ids and gates`));
    if (s.manifest.warnings && s.manifest.warnings.length) {
      card.appendChild(h(
        "div",
        { class: "f-banner warn" },
        h("b", {}, `${plural(s.manifest.warnings.length, "advisory", "advisories")}:`),
        h("ul", { class: "f-list" }, s.manifest.warnings.map((w) => h("li", {}, w)))
      ));
    }
    card.append(...fold(s.plan.map((it) => h(
      "div",
      { class: "f-row" },
      h("div", { class: "f-grow" }, h("div", {}, `${it.idx + 1}. ${it.name}`), h("div", { class: "f-mute" }, `${it.entity} \xB7 ${it.op}${it.targetId ? " \u2192 " + it.targetId : ""}${it.deps?.length ? " \xB7 after " + [...new Set(it.deps)].join(", ") : ""} \xB7 keys: ${keysText(it.data)}`))
    )), `Show all ${s.plan.length} items`));
    if (s.bloodright) {
      card.appendChild(h("div", { class: "f-banner info" }, s.collection ? `${plural(s.collection.length, "Bloodright tree")}, all hidden, run in order; a tree that does not verify stops the rest.` : `Bloodright preview \xB7 ${s.bloodright.allocations ?? "?"} legal builds \xB7 ${s.bloodright.maxAdvanced ?? "?"} reachable Advanced Art(s). New skills stay hidden.`));
      const trees = (s.bloodright.trees ?? []).map((tree) => h("div", { class: "f-mute" }, `${tree.name ?? tree.bloodlineId}: ${tree.allocations} legal builds \xB7 ${tree.maxAdvanced} reachable Advanced Art(s)`));
      if (trees.length) card.appendChild(h("details", {}, h("summary", {}, `Tree checks (${trees.length})`), trees));
      card.append(...fold(s.bloodright.preview.map((row) => h(
        "details",
        {},
        h("summary", {}, `${row.operation}: ${row.name}${row.targetId ? " \u2192 " + row.targetId : ""} \xB7 ${row.changes.length} changed field(s)`),
        h("pre", { class: "f-err" }, JSON.stringify(row.changes, null, 2))
      )), `Show all ${s.bloodright.preview.length} preview rows`));
      card.appendChild(h("button", { class: "f-btn", onclick: () => app.selectManifest(s.entry) }, "Refresh Bloodright preview"));
    }
    if (pack) {
      const bound = imgs.filter((n) => packBinds(pack, n));
      const ready = bound.filter((n) => (packEntry(n) || {}).state === "ready").length;
      const kind = !packResult ? "info" : ready === bound.length ? "ok" : "bad";
      card.appendChild(h(
        "div",
        { class: "f-banner " + kind },
        h("b", {}, `Repo-backed images: ${ready}/${bound.length} verified. `),
        `From ${GH.owner}/${GH.repo} @ ${pack.ref.slice(0, 12)}. Each file is checked against its SHA-256 before upload.`,
        h(
          "div",
          { class: "f-actions" },
          h("button", { onClick: () => app.prepareImages(true) }, "Re-fetch from repository")
        )
      ));
    }
    if (imgs.length) {
      card.appendChild(imagesHead);
      const rows = picks.map((p) => {
        const name = p.name;
        const bound = packBinds(pack, name);
        const e = bound ? packEntry(name) : null;
        const inp = h("input", { type: "file", accept: "image/*", style: { display: "none" }, onChange: (ev) => {
          const f = ev.target.files[0];
          if (f) {
            app.runner.files.set(name, f);
            app.refresh();
          }
        } });
        const pillFor = { ready: ["VERIFIED", bound ? "verified" : "picked"], refused: ["FAILED", "wrong file"], missing: ["FAILED", bound ? "not fetched" : "missing"] }[p.state];
        return h(
          "div",
          { class: "f-row" },
          h(
            "div",
            { class: "f-grow" },
            h("div", { class: "f-mono" }, name, " ", h("span", { class: "f-pill " + pillFor[0] }, pillFor[1])),
            bound ? h(
              "div",
              { class: "f-mute f-mono" },
              `repo: ${pack.files[name].path} @ ${pack.ref.slice(0, 12)} \xB7 sha256 ${pack.files[name].sha256.slice(0, 16)}\u2026 \xB7 ${fmtBytes(pack.files[name].bytes)}${e && e.state === "ready" ? ` \xB7 verified from ${e.source}` : ""}`
            ) : null,
            p.picked ? h(
              "div",
              { class: "f-mute f-mono" },
              `selected: ${p.picked.name ?? "(unnamed)"} \xB7 ${fmtBytes(p.picked.size)}${p.expectedBytes != null ? ` \xB7 ledger ${fmtBytes(p.expectedBytes)}` : ""}${p.picked.type ? ` \xB7 ${p.picked.type}` : ""}`
            ) : null,
            p.renamed && p.ok ? h("div", { class: "f-mute" }, "the device renamed this file; its bytes match the ledger exactly") : null,
            e && e.error ? h("div", { class: "f-err" }, e.error) : null,
            p.problems.length ? h("div", { class: "f-err" }, p.problems.join("\n")) : null
          ),
          bound ? null : h("button", { onClick: () => inp.click() }, p.picked ? "Replace" : "Pick"),
          bound ? null : inp
        );
      });
      card.append(...picks.every((p) => p.state === "ready") ? fold(rows, `Show all ${imgs.length} images (all verified)`) : rows);
    }
    return card;
  }
  function RunScreen(app) {
    const jobId = app.state.jobId;
    const job = jobId ? app.journal.get(jobId) : null;
    const root = h("section", {});
    if (!job) {
      root.appendChild(h("div", { class: "f-mute" }, "No job selected. Pick one on Jobs."));
      return root;
    }
    const done = job.items.filter((i) => TERMINAL.includes(i.state)).length;
    if (job.collection) {
      const c = job.collection, overall = (c.index + done / (job.items.length || 1)) / (c.total || 1);
      root.appendChild(h(
        "div",
        { class: "f-banner info" },
        h("b", {}, `Collection ${base(c.path)}: tree ${c.index + 1} of ${c.total}${c.name ? ` (${c.name})` : ""}`),
        h("div", { class: "f-bar" }, h("i", { style: { width: Math.round(overall * 100) + "%" } })),
        h("div", { class: "f-mute" }, "Pause stops the rest. After a reload, resume this tree, then reopen the file.")
      ));
    }
    root.append(
      h("div", {}, h("b", {}, jobLabel(job)), " ", jobPill(app, job), h("span", { class: "f-mute" }, ` \xB7 started ${fmtAgo(job.startedAt, app.now())}`)),
      h("div", { class: "f-bar" + (job.state === "PAUSED" ? " warn" : "") }, h("i", { style: { width: Math.round(done / (job.items.length || 1) * 100) + "%" } }))
    );
    const outcome = jobOutcome(job);
    if ((job.state === "DONE" || job.state === "INCOMPLETE") && job.items.length === 0) {
      const captures = [...job.capturesBefore || [], ...job.capturesAfter || []];
      const failed = captures.filter((capture) => !capture.ok).length;
      const full = captures.filter((capture) => capture.persist === "full");
      const unpersisted = full.filter((capture) => capture.ok && capture.persistOk !== true);
      const persistLine = full.length ? `, ${full.length - unpersisted.length}/${full.length} full record ${full.length === 1 ? "body" : "bodies"} persisted into the bundle` : "";
      root.appendChild(outcome === "success" ? h("div", { class: "f-banner ok" }, h("b", {}, "Read-only capture complete. "), `${captures.length}/${captures.length} reads succeeded${persistLine}; zero mutations were sent.`) : h(
        "div",
        { class: "f-banner bad" },
        h("b", {}, failed ? "Read-only capture failed. " : "Read-only capture incomplete. "),
        !failed && unpersisted.length ? `${captures.length}/${captures.length} reads succeeded, but ${unpersisted.length} of ${full.length} requested full ${full.length === 1 ? "body" : "bodies"} could not be persisted, so this bundle does not carry the record data the manifest asked for` : `${failed} of ${captures.length} reads failed`,
        "; zero mutations were sent.",
        unpersisted.length ? h("div", { class: "f-err" }, unpersisted.map((capture) => `${capture.proc} ${capture.snapshotKey || ""}: ${capture.persistError || "not persisted"}`).join("\n")) : null
      ));
    } else if (job.state === "DONE" || job.state === "INCOMPLETE") {
      const drift = job.items.filter((i) => i.verify === "drift").length;
      const unread = job.items.filter((i) => i.verify === "unread").length;
      const failed = job.items.filter((i) => i.state === "FAILED").length;
      const skipped = job.items.filter((i) => i.state === "SKIPPED").length;
      root.appendChild(outcome === "success" ? h("div", { class: "f-banner ok" }, h("b", {}, "Verified. "), "Every item read back exactly as written.") : h(
        "div",
        { class: "f-banner " + (outcome === "failed" ? "bad" : "warn") },
        h("b", {}, outcome === "failed" ? "Finished with failures. " : "Finished, not fully verified. "),
        [failed ? `${failed} failed` : null, drift ? `${drift} changed after writing` : null, unread ? `${unread} could not be read back` : null, skipped ? `${skipped} skipped` : null].filter(Boolean).join(", "),
        ". ",
        failed ? "Each failed item shows its reason below. " : "",
        drift || unread ? "The items that changed or could not be read back are not proven written. " : "",
        job.state === "INCOMPLETE" ? "Resume to re-read them; resuming can only read, never re-send." : ""
      ));
    }
    if (job.pause && job.pause.reason === "SESSION") {
      root.appendChild(h(
        "div",
        { class: "f-banner bad" },
        h("b", {}, "Paused: TNR authentication unavailable. "),
        job.pause.authRefused ? `The game refused ${job.pause.path ? job.pause.path : "a protected procedure"} as signed out. The server answered, so nothing was written.` : `Forge stopped before sending${job.pause.path ? ` ${job.pause.path}` : ""} because the game session is not available. Nothing further was sent.`,
        h("div", { class: "f-mute" }, "Sign in to The Ninja RPG in this browser, re-check the session above, then resume. Resuming re-reads before it re-sends anything."),
        job.pause.detail ? h("div", { class: "f-err" }, job.pause.detail) : null
      ));
    } else if (job.pause) root.appendChild(h(
      "div",
      { class: "f-banner " + (job.pause.reason === "TOO_MANY_REQUESTS" ? "bad" : "warn") },
      h("b", {}, pauseWords(job.pause)),
      job.pause.path ? ` on ${job.pause.path}` : "",
      job.pause.until ? ` \xB7 wait ${fmtCountdown(job.pause.until, app.now())}` : "",
      job.pause.detail ? h("div", { class: "f-err" }, job.pause.detail) : null
    ));
    if (app.state.running === jobId) {
      const next = job.items.find((i) => !TERMINAL.includes(i.state));
      root.appendChild(h("div", { class: "f-banner info" }, next ? `Working on item ${next.idx + 1} of ${job.items.length}: ${next.name}` : app.state.runningNote || "All items sent; reading back and saving the results\u2026"));
    }
    const resumeBlocked = app.resumeBlockedReason ? app.resumeBlockedReason(job) : null;
    if (resumeBlocked) root.appendChild(h("div", { class: "f-mute" }, resumeBlocked));
    root.appendChild(h(
      "div",
      { class: "f-actions" },
      job.state === "PAUSED" || job.state === "INCOMPLETE" || job.state === "RUNNING" && app.state.running !== jobId && job.items.some((i) => !["VERIFIED", "FAILED", "SKIPPED"].includes(i.state)) ? h("button", { class: "f-primary", disabled: !!resumeBlocked, onClick: () => app.resumeJob(jobId) }, resumeLabel(job)) : null,
      app.state.running === jobId ? h("button", { onClick: () => app.requestPause() }, "Pause after this item") : null,
      app.state.running === jobId ? null : h("button", { onClick: () => app.exportJob(jobId) }, "Export results"),
      app.state.running !== jobId && job.items.some((i) => i.suggestion?.id) ? h("button", { onClick: () => app.checkSuggestions(jobId) }, "Check suggestions") : null
    ));
    root.appendChild(h("h3", {}, "Budget (limited reads, per path, this minute)"));
    const st = app.budget.status();
    const used = Object.entries(st.paths).filter(([, v]) => v.used > 0);
    root.appendChild(h("div", { class: "f-card" }, used.length ? used.map(([p, v]) => h("div", { class: "f-kv" }, h("b", {}, p), h("span", {}, `${v.used} / ${v.allowance} (server ${v.serverLimit}) \xB7 resets in ${fmtCountdown(app.now() + v.resetInMs, app.now())}`))) : h("span", { class: "f-mute" }, "nothing spent"), st.tripped ? h("div", { class: "f-err" }, `TRIPPED on ${st.tripped.path} until ${new Date(st.tripped.until).toLocaleTimeString()}`) : null));
    const allCaptures = [...job.capturesBefore || [], ...job.capturesAfter || []];
    if (allCaptures.some((capture) => capture && capture.persist === "full")) {
      root.appendChild(h("h3", {}, "Full captures"));
      for (const capture of allCaptures.filter((capture2) => capture2.persist === "full")) {
        root.appendChild(h("div", { class: "f-row" }, h(
          "div",
          { class: "f-grow" },
          h("div", {}, `${capture.proc} `, h("span", { class: "f-pill " + (capture.persistOk === true ? "VERIFIED" : "FAILED") }, capture.persistOk === true ? "body persisted" : "not persisted"), h("span", { class: "f-mute" }, capture.ok ? " \xB7 read ok" : " \xB7 read failed")),
          h("div", { class: "f-mono" }, `${capture.snapshotKey || ""}${capture.input && capture.input.id ? " \xB7 " + capture.input.id : ""}`),
          capture.persistError ? h("div", { class: "f-err" }, capture.persistError) : null
        )));
      }
    }
    if (job.items.length) root.appendChild(h("h3", {}, "Items"));
    const savedBindings = readIdmap(app.storage), bloodlineId = job.bloodrightImport?.bloodlineId;
    const bindingBlocked = bloodlineId && unresolvedBloodrightJob(app.journal, bloodlineId);
    if (Object.keys(job.forgottenBindings ?? {}).length) root.appendChild(h("div", { class: "f-banner warn" }, "A saved binding was forgotten. Export this job for evidence and prepare a fresh preview; this job cannot restore the old binding."));
    for (const it of job.items) {
      const phase = it.state === "SENT" || it.state === "CONFIRMED" ? ` \xB7 phase ${it.phase}` : "";
      const row = h(
        "div",
        { class: "f-row" },
        h(
          "div",
          { class: "f-grow" },
          h("div", {}, `${it.idx + 1}. ${it.name} `, it.suggestion ? h("span", { class: "f-pill " + (it.suggestion.status === "APPLIED" ? "VERIFIED" : /REJECTED|OUTDATED|REVERTED|NOT FOUND/.test(it.suggestion.status) ? "FAILED" : "SENT") }, it.suggestion.status === "PENDING" ? "IN REVIEW" : it.suggestion.status) : pill(it.state), h("span", { class: "f-mute" }, ` ${it.entity}${phase}`)),
          it.entityId ? h("div", { class: "f-mono" }, it.entityId) : null,
          it.suggestion ? h("div", { class: "f-mute" }, `suggestion ${it.suggestion.id ?? "(id not found)"}${it.suggestion.reviewedBy ? ` \xB7 by ${it.suggestion.reviewedBy}` : ""}${it.suggestion.note ? ` \xB7 ${it.suggestion.note}` : ""}`) : null,
          it.error ? h("div", { class: "f-err" }, it.error) : null,
          it.diffs && it.diffs.length ? h("details", {}, h("summary", {}, `drift on ${it.diffs.length} key(s)`), h("div", { class: "f-err" }, it.diffs.map((d) => `${d.key}: sent ${JSON.stringify(d.sent)} live ${JSON.stringify(d.live)}`).join("\n"))) : null,
          it.reconciled ? h("div", { class: "f-mute" }, it.reconciled) : null,
          it.resolution?.action === "operator-failed" ? h("div", { class: "f-mute" }, "Recovery stopped by operator; record left as is, verification not accepted.") : null
        )
      );
      if (["skillTree", "skillTreeFolder"].includes(it.entity) && it.state === "CONFIRMED" && ["PAUSED", "INCOMPLETE"].includes(job.state)) {
        row.appendChild(h("button", {
          class: "f-danger",
          disabled: !!app.state.running || job.items.some((i) => i.state === "SENT") || typeof globalThis.confirm !== "function",
          onClick: () => app.confirm(`Mark "${it.name}" (${it.entityId}) failed and stop recovery? The record and its saved ID stay as they are, the write is not verified, and dependent skills stay blocked.`, () => app.resolveConfirmed(jobId, it.idx, { confirmed: true }))
        }, "Mark failed (leave as is)"));
      }
      if (bloodlineId && ["skillTree", "skillTreeFolder"].includes(it.entity) && ["FAILED", "VERIFIED"].includes(it.state) && it.entityId && savedBindings[it.srcId] === it.entityId) {
        row.appendChild(h("details", { class: "f-more" }, h("summary", {}, "More"), h("button", {
          class: "f-danger",
          disabled: !!app.state.running || job.state === "RUNNING" || !!bindingBlocked || typeof globalThis.confirm !== "function",
          onClick: () => app.confirm(`Forget saved binding for "${it.name}" (${it.entityId})? Only if the record was deleted or replaced: forgetting one that still exists can create duplicates. Nothing in the game is deleted; old jobs will need a fresh preview.`, () => app.forgetBinding(jobId, it.idx, { confirmed: true, expectedId: it.entityId }))
        }, "Forget saved binding")));
      }
      root.appendChild(row);
    }
    return root;
  }
  function CapturesScreen(app) {
    const root = h("section", {});
    const list = h("div", {});
    const head = h("div", { class: "f-mute" }, "loading\u2026");
    root.append(head, h("div", { class: "f-actions" }, h("button", { class: "f-danger", onClick: () => app.confirm("Clear the whole capture cache? Reads will cost budget again.", async () => {
      await app.cache.clear();
      app.refresh();
    }) }, "Clear all")), list);
    root.appendChild(SnapshotsSection(app));
    app.cache.list().then((recs) => {
      const bytes = recs.reduce((a, r) => a + (r.bytes || 0), 0);
      replace(head, `${recs.length} capture${recs.length === 1 ? "" : "s"} \xB7 ${fmtBytes(bytes)}`);
      recs.sort((a, b) => a.at < b.at ? 1 : -1);
      replace(list, recs.map((r) => h(
        "div",
        { class: "f-row" },
        h("div", { class: "f-grow" }, h("div", { class: "f-mono" }, r.key), h("div", { class: "f-mute" }, `${r.entity} \xB7 ${fmtBytes(r.bytes || 0)} \xB7 ${fmtAgo(r.at, app.now())}`)),
        h("button", { onClick: async () => {
          await app.cache.delete(r.path, r.id ?? "");
          app.refresh();
        } }, "Invalidate")
      )));
    }).catch((e) => replace(head, h("div", { class: "f-banner bad" }, "capture cache unavailable: ", e.message)));
    return root;
  }
  function SnapshotsSection(app) {
    const section = h("div", {});
    const head = h("h3", {}, "Full-capture snapshots");
    const note = h("div", { class: "f-mute" }, "loading\u2026");
    const list = h("div", {});
    section.append(head, note, h("div", { class: "f-actions" }, h("button", {
      class: "f-danger",
      onClick: () => app.confirm("Delete ALL full-capture snapshots? Exported bundles are built from them; an unexported job loses its evidence until the game is read again.", async () => {
        await app.cache.clearSnapshots();
        app.refresh();
      })
    }, "Delete all snapshots")), list);
    app.cache.listSnapshots().then((recs) => {
      const bytes = recs.reduce((a, r) => a + (r.bytes || 0), 0);
      replace(note, `${recs.length} snapshot${recs.length === 1 ? "" : "s"} \xB7 ${fmtBytes(bytes)} \xB7 never invalidated by a write; deleted with their job`);
      recs.sort((a, b) => a.at < b.at ? 1 : -1);
      replace(list, recs.map((r) => h(
        "div",
        { class: "f-row" },
        h(
          "div",
          { class: "f-grow" },
          h("div", { class: "f-mono" }, r.key),
          h("div", { class: "f-mute" }, `${r.path}${r.id ? " " + r.id : ""} \xB7 ${r.phase} \xB7 ${fmtBytes(r.bytes || 0)} \xB7 ${fmtAgo(r.at, app.now())}`)
        ),
        h("button", { onClick: () => app.confirm(`Delete snapshot ${r.key}? Its body can only come back from another read.`, async () => {
          await app.cache.deleteSnapshot(r.key);
          app.refresh();
        }) }, "Delete")
      )));
    }).catch((e) => replace(note, h("div", { class: "f-banner bad" }, "capture snapshots unavailable: ", e.message)));
    return section;
  }
  function SettingsScreen(app) {
    const gh = readGh(app.storage);
    const pat = h("input", { type: "password", placeholder: "fine-grained PAT (contents: write on tnr-tools only)", value: gh.pat || "" });
    const sync = h("input", { type: "checkbox", checked: !!gh.on });
    const root = h(
      "section",
      {},
      h("h2", {}, "GitHub"),
      h(
        "div",
        { class: "f-card" },
        h("div", { class: "f-mute" }, "Sent to api.github.com only. Never to the game. Stored in this browser under tnr_bk_gh_v1 (same key as the old builder)."),
        pat,
        h("label", { class: "f-row" }, sync, h("span", {}, "Auto-commit results bundles to harvests/inbox/")),
        h("div", { class: "f-actions" }, h("button", { class: "f-primary", onClick: () => {
          writeGh(app.storage, { on: sync.checked, pat: pat.value.trim() });
          app.toast("saved", "ok");
          app.refresh();
        } }, "Save"), h("button", { class: "f-danger", onClick: () => app.confirm("Forget the PAT?", () => {
          writeGh(app.storage, { on: false, pat: "" });
          app.refresh();
        }) }, "Forget"))
      ),
      h("h2", {}, "Session"),
      h(
        "div",
        { class: "f-card f-kv" },
        h("b", {}, "game"),
        h("span", {}, describeText(app.session.describe())),
        h("b", {}, "auth"),
        h("span", {}, app.auth ? describeText(app.auth.describe()) : "not wired"),
        h("b", {}, "budget"),
        h("span", {}, `${app.budget.allowance} / ${app.budget.limit} per path per minute (margin ${app.budget.margin})`),
        h("b", {}, "persisted storage"),
        h("span", { id: "f-persist" }, app.view.persisted == null ? "unknown" : String(app.view.persisted))
      ),
      h("h2", {}, "Journal"),
      h(
        "div",
        { class: "f-card" },
        h(
          "div",
          { class: "f-actions" },
          h("button", { onClick: () => app.showExport(app.journal.exportText(), "journal export") }, "Export journal as text"),
          h("button", { class: "f-danger", onClick: () => app.confirm("Delete ALL finished jobs from the journal? Open jobs are kept, and each deleted job's full-capture snapshots go with it.", async () => {
            for (const j of app.journal.listJobs()) if (j.state === "DONE" || j.state === "ABORTED") {
              app.journal.remove(j.jobId);
              await app.cache.deleteSnapshotsForJob(j.jobId);
            }
            app.refresh();
          }) }, "Delete finished jobs")
        ),
        app.cacheSize ? h("div", { class: "f-mute" }, `capture cache: ${app.cacheSize}`) : null
      ),
      h("h2", {}, "About"),
      h("div", { class: "f-card f-mute" }, `${app.version} \xB7 content fields pinned to studie-tech/TheNinjaRPG@94f9d84 (procedures 345d18ac) \xB7 journal v1 \xB7 keys tnr_forge_job_v1:*, tnr_forge_sendlog_v1, tnr_forge_snap_v1:*`)
    );
    return root;
  }
  function describeText(obj3) {
    return Object.entries(obj3 || {}).filter(([, v]) => v != null && v !== "").map(([k, v]) => `${k}: ${typeof v === "number" && v > 1e12 ? new Date(v).toLocaleString() : typeof v === "object" ? JSON.stringify(v) : v}`).join(" \xB7 ") || "\u2014";
  }

  var realSleep2 = (ms) => new Promise((r) => setTimeout(r, ms));
  var BOUND_READ_RETRY_MS = Object.freeze([3e3, 1e4]);
  async function readBoundSkills(reader, ids, { sleep = realSleep2, delays = BOUND_READ_RETRY_MS } = {}) {
    const found =  new Map();
    let pending = [...ids], lastError = null;
    for (let attempt = 0; pending.length; attempt++) {
      if (attempt > 0) {
        if (attempt > delays.length) throw new Error(`bound skill ${pending[0]} is unreadable${lastError ? `: ${lastError}` : ""}`);
        await sleep(delays[attempt - 1]);
      }
      try {
        const rows = typeof reader.getMany === "function" ? await reader.getMany("skillTree.get", pending, { fresh: true }) : await Promise.all(pending.map((id2) => reader.get("skillTree.get", id2, { fresh: true })));
        const next = [];
        rows.forEach((r, i) => {
          if (r && r.ok && r.data) found.set(pending[i], r.data);
          else {
            next.push(pending[i]);
            lastError = r?.error?.message ?? "no record returned";
          }
        });
        pending = next;
      } catch (e) {
        if (e && e.name === "RateLimited") throw e;
        lastError = e && e.message || String(e);
      }
    }
    return found;
  }
  var scopeKey = (bloodlineId, nodeId) => `br:${bloodlineId}:${nodeId}`;
  var object = (v) => !!v && typeof v === "object" && !Array.isArray(v);
  var id = (v) => typeof v === "string" && /^[A-Za-z0-9_-]+$/.test(v);
  var sameName = (a, b) => a.normalize("NFKC").trim().toLowerCase() === b.normalize("NFKC").trim().toLowerCase();
  function compileBloodright({ design, config, skills, folders, idmap = {}, imagePack, imgSizes = {}, uploads = {}, requireIcons = false }) {
    const problems = [], preview = [], items = [];
    const fail = (text) => problems.push(text);
    const bl = design?.bloodline?.id;
    if (!id(bl)) fail("design requires a literal bloodline ID");
    if (!/^[a-f0-9]{40}$/.test(config?.source?.ref ?? "") || !config?.source?.path) fail("source must name a repository path at an exact 40-character commit");
    const nodes = design?.nodes;
    for (const category of Object.keys(config.icons ?? {})) if (!["Foundation", "Hidden Art", "Advanced Art"].includes(category)) fail(`unknown icon category ${category}`);
    if (!Array.isArray(nodes) || !nodes.length || nodes.length > 24) return { problems: [...problems, "design needs 1..24 structural nodes"], preview, manifest: null };
    const rules = design.build_rules;
    if (rules?.max_bp !== 5 || rules?.skill_cost !== 1 || rules?.prerequisites !== "ALL") fail("this importer requires the approved five-BP, one-point, ALL-prerequisites design format");
    const elements = design.classification?.qualifying_elements;
    if (!Array.isArray(elements) || !elements.length || elements.some((v) => !contract_default.elements.includes(v))) fail("design qualifying elements are unresolved or unsupported");
    const byId =  new Map(), names =  new Set();
    for (const n of nodes) {
      if (!id(n.id) || n.id === "folder" || byId.has(n.id)) fail(`invalid or duplicate node ID: ${n.id}`);
      byId.set(n.id, n);
      if (typeof n.name !== "string" || !n.name.trim()) fail(`${n.id}: name required`);
      else if (n.name !== n.name.trim()) fail(`${n.id}: name must not have leading or trailing whitespace`);
      else {
        const name = n.name.normalize("NFKC").trim().toLowerCase();
        if (names.has(name)) fail(`duplicate design name: ${n.name}`);
        names.add(name);
      }
      if (n.cost !== 1 || n.parent_rule !== "ALL" || !Array.isArray(n.parents)) fail(`${n.id}: one point and ALL parents required`);
      if (!Number.isInteger(n.tier) || n.tier < 1 || n.tier > 10) fail(`${n.id}: tier must be 1..10`);
      if (!object(n.bonuses) || !Object.keys(n.bonuses).length) fail(`${n.id}: structural bonuses required; legacy modifiers are not implicitly converted`);
      for (const [tag, power] of Object.entries(n.bonuses ?? {})) if (!contract_default.tags.includes(tag) || !Number.isFinite(power) || power === 0) fail(`${n.id}: unsupported bonus ${tag}=${power}`);
    }
    for (const n of nodes) for (const p of n.parents ?? []) {
      if (!byId.has(p) || byId.get(p).tier >= n.tier) fail(`${n.id}: prerequisite ${p} must exist at a lower tier (cycles refused)`);
    }
    if (problems.length) return { problems, preview, manifest: null };
    const ordered = [...nodes].sort((a, b) => a.tier - b.tier || a.id.localeCompare(b.id));
    let allocations = 0, advanced = 0;
    function visit(i, chosen, adv) {
      if (i === ordered.length) {
        allocations++;
        advanced = Math.max(advanced, adv);
        return;
      }
      visit(i + 1, chosen, adv);
      const n = ordered[i];
      if (chosen.size < 5 && n.parents.every((p) => chosen.has(p))) {
        chosen.add(n.id);
        visit(i + 1, chosen, adv + (n.category === "Advanced Art" ? 1 : 0));
        chosen.delete(n.id);
      }
    }
    visit(0,  new Set(), 0);
    if (Number.isInteger(rules.max_advanced_reachable) && advanced !== rules.max_advanced_reachable) fail(`design reachable Advanced Art count is ${advanced}, expected ${rules.max_advanced_reachable}`);
    if (Number.isInteger(rules.max_advanced) && advanced > rules.max_advanced) fail("design exceeds its Advanced Art limit");
    const bindings = config.bindings ?? {};
    for (const key of Object.keys(bindings.nodes ?? {})) if (!byId.has(key)) fail(`binding names unknown node ${key}`);
    const reassign = new Set(Array.isArray(bindings.reassign) ? bindings.reassign : []);
    for (const key of reassign) if (!bindings.nodes?.[key]) fail(`reassign names ${key}, which has no explicit binding`);
    for (const key of Object.keys(config.nodes ?? {})) if (!byId.has(key)) fail(`settings name unknown node ${key}`);
    const bound = (node, explicit) => {
      const remembered = idmap[scopeKey(bl, node)];
      if (explicit && remembered && explicit !== remembered) fail(`${node}: explicit binding conflicts with saved ID ${remembered}`);
      return explicit || remembered || null;
    };
    const folderId = bound("folder", bindings.folderId);
    const folder = folders.find((f) => f.id === folderId);
    const folderKey = scopeKey(bl, "folder");
    if (folderId && !folder) fail(`bound folder ${folderId} is not visible; check hidden-content access and binding`);
    if (!folderId && !config.folder?.name) fail("bind an existing folder ID or explicitly configure a new folder");
    const folderData = folder ? writableSnapshot("skillTreeFolder", folder) : { image: "", description: "", order: 0, ...config.folder, hidden: true };
    const twin = !folderId && folders.find((f) => sameName(f.name, folderData.name ?? ""));
    if (twin) fail(`folder "${twin.name}" exists (${twin.id}, ${twin.hidden ? "hidden" : "visible"}); bind its ID explicitly`);
    if (folder || !folderId) {
      for (const p of bloodrightProblems("skillTreeFolder", folderData)) fail(`folder: ${p}`);
      const it = { entity: "skillTreeFolder", slot: folder ? "edit" : "create", srcId: folderKey, name: folderData.name, ...folder ? { targetId: folderId, expected: folderData } : {}, data: folderData };
      items.push(it);
      preview.push({ name: folderData.name, operation: folder ? "reuse" : "create", targetId: folderId, changes: [] });
    }
    const claimed =  new Set();
    for (const n of ordered) {
      const settings = config.nodes?.[n.id] ?? {};
      const icon = Object.hasOwn(settings, "image") ? settings.image : config.icons?.[n.category];
      if (requireIcons && icon === void 0) fail(`${n.name}: collection imports require an explicit node or category icon`);
      if (icon !== void 0 && (typeof icon !== "string" || !/^(@img:[A-Za-z0-9_.-]+|https:\/\/\S+)$/.test(icon))) fail(`${n.name}: icon must be an HTTPS URL or @img filename`);
      for (const key of Object.keys(settings)) if (!["rounds", "seichiSilverCost", "description", "image"].includes(key)) fail(`${n.name}: unsupported setting ${key}`);
      const targetId = bound(n.id, bindings.nodes?.[n.id]);
      const live = skills.find((s) => s.id === targetId);
      if (targetId) {
        if (claimed.has(targetId)) fail(`${n.name}: ID ${targetId} is bound twice`);
        claimed.add(targetId);
        if (!live) fail(`${n.name}: bound record ${targetId} is not visible; check access/binding`);
        else if (live.pathType !== "BLOODRIGHT" || live.bloodlineId !== bl && !reassign.has(n.id)) fail(`${n.name}: binding belongs to another bloodline or SKILL path (${live.pathType}, bloodline ${live.bloodlineId})`);
        else if (live.bloodlineId !== bl && skills.some((s) => s.id !== targetId && (s.requiredSkillIds ?? []).includes(targetId))) fail(`${n.name}: other skills require it`);
        else if (!live.hidden) fail(`${n.name}: bound skill is already visible; this importer stages hidden content only`);
      }
      if (skills.some((s) => s.id !== targetId && sameName(s.name, n.name))) fail(`${n.name}: global name collision; bind the intended record explicitly or rename the design`);
      const effects = Object.entries(n.bonuses).map(([tag, amount]) => ({
        type: amount > 0 ? "increasepotency" : "decreasepotency",
        target: "INHERIT",
        direction: "offence",
        rounds: settings.rounds,
        power: Math.abs(amount),
        powerPerLevel: 0,
        calculation: "static",
        affectedTag: tag,
        affectedElements: [...elements],
        staticAssetPath: "",
        staticAnimation: "",
        appearAnimation: "",
        disappearAnimation: "",
        appearSfx: "",
        disappearSfx: "",
        description: `${amount > 0 ? "Increase" : "Decrease"} ${tag} potency on ${elements.join("/")} jutsu by ${Math.abs(amount)} points.`
      }));
      const data = {
        name: n.name,
        description: settings.description ?? effects.map((e) => e.description).join(" "),
        target: "SELF",
        tier: n.tier,
        requiredSkillIds: n.parents.map((p) => `@skillTree:${scopeKey(bl, p)}`),
        costSkillPoints: n.cost,
        pathType: "BLOODRIGHT",
        bloodlineId: bl,
        seichiSilverCost: settings.seichiSilverCost,
        hidden: true,
        skillType: "DEFAULT",
        folderId: `@skillTreeFolder:${folderKey}`,
        effects,
        ...live?.image ? { image: live.image } : {},
        ...icon !== void 0 ? { image: icon } : {}
      };
      for (const p of bloodrightProblems("skillTree", data, null, { preCreate: true })) fail(`${n.name}: ${p}`);
      const resolved = { ...data, folderId: folderId ?? data.folderId, requiredSkillIds: n.parents.map((p) => bound(p, bindings.nodes?.[p]) ?? `@skillTree:${scopeKey(bl, p)}`) };
      const imageName = typeof data.image === "string" && data.image.startsWith("@img:") ? data.image.slice(5) : null;
      const asset = imagePack?.files?.[imageName];
      if (imageName && asset && uploads[asset.sha256]?.url) resolved.image = uploads[asset.sha256].url;
      const changes = live ? diffAsserted("skillTree", resolved, live) : Object.entries(data).map(([key, sent]) => ({ key, sent }));
      const it = { entity: "skillTree", srcId: scopeKey(bl, n.id), name: n.name, slot: targetId ? "edit" : "create", ...targetId ? { targetId, expected: live ? writableSnapshot("skillTree", live) : null } : {}, ...targetId && live && live.bloodlineId !== bl ? { reassign: true } : {}, data };
      items.push(it);
      preview.push({ nodeId: n.id, name: n.name, targetId, operation: targetId ? changes.length ? "update" : "reuse" : "create", changes });
    }
    const provenance = { version: 1, source: config.source, gamePin: contract_default._meta.pin, bloodlineId: bl, bindings: Object.fromEntries(items.filter((it) => it.targetId).map((it) => [it.srcId, it.targetId])), hiddenProbeId: config.hiddenProbeId };
    const packed = normalizeImagePack(imagePack, { imgSizes, names: items.map((it) => it.data.image).filter((v) => typeof v === "string" && v.startsWith("@img:")).map((v) => v.slice(5)) });
    problems.push(...packed.errors);
    return { problems, preview, allocations, maxAdvanced: advanced, bloodlineName: design.bloodline?.name ?? null, manifest: problems.length ? null : { _note: `Bloodright: ${design.title}`, dedupNames: true, bloodrightImport: provenance, items, ...packed.pack ? { imagePack: packed.pack } : {}, ...Object.keys(imgSizes).length ? { imgSizes } : {} } };
  }
  async function readBloodrightInventory({ reader, hiddenProbeId }) {
    if (!id(hiddenProbeId)) throw new Error("name a known hidden skill ID to verify staff-visible inventory");
    const probe = await reader.get("skillTree.get", hiddenProbeId, { fresh: true });
    if (!probe.ok || probe.data?.hidden !== true) throw new Error("hidden-content access not established: the known hidden skill is not visible; check the session, role, and probe ID");
    const all = await reader.list("skillTree.getAll", { fresh: true });
    const folders = await reader.list("skillTree.getAllFolders", { fresh: true });
    if (!all.ok || !folders.ok) throw new Error("Bloodright inventory failed; no preview or writes available");
    if (!all.data.some((s) => s.id === hiddenProbeId)) throw new Error("hidden probe missing from inventory; incomplete access or changed session");
    return { hiddenProbeId, skills: all.data, folders: folders.data };
  }
  async function prepareBloodright({ config, github, reader, storage, auth, journal, imagePack, imgSizes, requireIcons, inventory, imageProbe, sleep }) {
    if (config?.version !== 1) throw new Error("unsupported Bloodright package version");
    if (!/^[a-f0-9]{40}$/.test(config.source?.ref ?? "")) throw new Error("Bloodright source requires an exact commit");
    auth?.assert("skillTree.create");
    if (!id(config.hiddenProbeId)) throw new Error("name a known hidden skill ID to verify staff-visible inventory");
    if (inventory && inventory.hiddenProbeId !== config.hiddenProbeId) throw new Error("shared inventory was verified with a different hidden probe");
    const design = JSON.parse(await github.text(config.source.path, config.source.ref));
    assertBloodrightAvailable(journal, design?.bloodline?.id);
    const inv = inventory ?? await readBloodrightInventory({ reader, hiddenProbeId: config.hiddenProbeId });
    const all = { data: structuredClone(inv.skills) }, folders = { data: structuredClone(inv.folders) };
    const map = readIdmap(storage);
    const boundIds = [...new Set(design.nodes.map((n) => config.bindings?.nodes?.[n.id] || map[scopeKey(design.bloodline.id, n.id)]).filter(Boolean))];
    const bound = await readBoundSkills(reader, boundIds, sleep ? { sleep } : {});
    for (const target of boundIds) {
      const index = all.data.findIndex((s) => s.id === target);
      if (index < 0) throw new Error(`bound skill ${target} absent from complete inventory`);
      all.data[index] = bound.get(target);
    }
    const shas = new Set(Object.values(imagePack?.files ?? {}).map((f) => f?.sha256).filter(Boolean));
    const uploads = await liveAssetUploads(storage, imageProbe, shas, { forget: false });
    return compileBloodright({ design, config, skills: all.data, folders: folders.data, idmap: map, imagePack, imgSizes, requireIcons, uploads });
  }

  async function prepareCollection(ctx, pkg, { onProgress = () => {
  } } = {}) {
    const c = pkg.bloodrightCollection;
    if (pkg.bloodright || pkg.items || pkg.jutsu || pkg.capture || c?.version !== 1 || !Array.isArray(c.trees) || !c.trees.length || c.trees.length > 100) throw new Error("collection needs version 1 and 1..100 trees, without other manifest operations");
    const probes = [...new Set(c.trees.map((t) => t?.hiddenProbeId))];
    if (probes.length !== 1) throw new Error("every tree in a collection must name the same hidden probe");
    ctx.auth?.assert("skillTree.create");
    onProgress(`reading the live skill inventory (once for all ${c.trees.length} trees)`);
    const inventory = await readBloodrightInventory({ reader: ctx.reader, hiddenProbeId: probes[0] });
    const trees = [], problems = [], names =  new Map(), bloodlines =  new Set();
    for (const [index, config] of c.trees.entries()) {
      try {
        onProgress(`checking tree ${index + 1}/${c.trees.length}`);
        const bloodright = await prepareBloodright({ ...ctx, config, imagePack: pkg.imagePack, imgSizes: pkg.imgSizes, requireIcons: true, inventory });
        if (bloodright.problems.length) {
          problems.push(...bloodright.problems.map((p) => `tree ${index + 1}: ${p}`));
          continue;
        }
        const text = JSON.stringify(bloodright.manifest), manifest = parseManifest(text);
        const bl = manifest.policy.bloodrightImport.bloodlineId;
        if (bloodlines.has(bl)) problems.push(`duplicate bloodline ${bl} in collection`);
        bloodlines.add(bl);
        const plan = planOrder(manifest, readIdmap(ctx.storage));
        for (const it of plan) {
          const name = `${it.entity}:${it.name.normalize("NFKC").trim().toLowerCase()}`;
          const prior = names.get(name);
          if (prior && !(it.entity === "skillTreeFolder" && it.targetId && prior.targetId === it.targetId)) problems.push(`cross-tree name collision: ${it.name}`);
          names.set(name, it);
          problems.push(...ctx.validator.problems(it.entity, it.data, null).map((p) => `${it.name}: ${p}`));
        }
        const images = [...new Set(plan.flatMap((it) => collectRefs(it.data).filter((r) => r.pfx === "img").map((r) => r.key)))];
        for (const name of images) if (!manifest.imagePack?.files[name]) problems.push(`collection icon ${name} needs an immutable imagePack binding`);
        trees.push({ text, manifest, plan, images, bloodright, pack: manifest.imagePack, problems: [] });
      } catch (e) {
        problems.push(`tree ${index + 1}: ${e.message}`);
      }
    }
    return {
      trees,
      problems,
      plan: trees.flatMap((t) => t.plan),
      images: [...new Set(trees.flatMap((t) => t.images))],
      manifest: { capture: { before: [], after: [] }, imgSizes: pkg.imgSizes ?? {}, warnings: [], imagePack: trees[0]?.pack ?? null },
      bloodright: { preview: trees.flatMap((t) => t.bloodright.preview), trees: trees.map((t) => ({ bloodlineId: t.manifest.policy.bloodrightImport.bloodlineId, name: t.bloodright.bloodlineName, allocations: t.bloodright.allocations, maxAdvanced: t.bloodright.maxAdvanced })) }
    };
  }

  async function resolveCaptures({ journal, cache }, jobId) {
    const job = journal.get(jobId);
    const patch = {};
    const out = [];
    for (const key of ["capturesBefore", "capturesAfter"]) {
      if (!Array.isArray(job[key])) continue;
      const resolved = [];
      for (const capture of job[key]) resolved.push(await materialize(cache, capture));
      if (job[key].some((capture) => capture && capture.persist === "full")) {
        patch[key] = resolved.map(({ data, ...rest }) => rest);
      }
      out.push(...resolved);
    }
    if (Object.keys(patch).length) journal.annotateJob(jobId, patch);
    return out;
  }
  async function materialize(cache, capture) {
    if (!capture || typeof capture !== "object" || capture.persist !== "full") return capture;
    const c = { ...capture, persistOk: false, persistError: null };
    delete c.data;
    if (capture.ok !== true) {
      c.persistError = "read failed; there is no body to persist";
      return c;
    }
    if (capture.persistOk === false && capture.persistError) return { ...c, persistError: capture.persistError };
    const key = capture.snapshotKey || null;
    if (!key) {
      c.persistError = "no capture snapshot key was journaled for this full capture";
      return c;
    }
    let rec = null;
    try {
      rec = await cache.getSnapshot(key);
    } catch (e) {
      c.persistError = "capture snapshot read failed: " + (e && e.message || String(e));
      return c;
    }
    if (!rec) {
      c.persistError = `capture snapshot ${key} is gone, so the full body cannot be exported without a second read; it was not re-read`;
      return c;
    }
    const bytes = typeof rec.bytes === "number" ? rec.bytes : JSON.stringify(rec.data ?? null).length;
    c.bytes = bytes;
    if (bytes > MAX_FULL_CAPTURE_BYTES) {
      c.persistError = `body is ${bytes} bytes, over the ${MAX_FULL_CAPTURE_BYTES}-byte full-capture ceiling; it is NOT truncated and NOT persisted`;
      return c;
    }
    c.persistOk = true;
    c.at = rec.at ?? null;
    c.data = rec.data;
    return c;
  }
  function buildBundle({ version, storage, now }, job, captures) {
    return {
      builder: version,
      at: new Date(now()).toISOString(),
      cfg: "forge",
      checks: null,
      state: job.state,
      outcome: jobOutcome(job),
      postflight: postflight(job),
      entries: job.items.map((i) => harvestEntry(i)),
      captures,
      idmap: JSON.parse(storage.getItem("tnr_bk_idmap_v1") || "{}"),
      journal: job
    };
  }
  var bundleName = (now) => `tnr_results_${now()}.json`;
  function repoSyncReady(storage) {
    const gh = readGh(storage);
    return Boolean(gh.on && gh.pat);
  }
  var inboxPath = (name) => `${GH.inboxDir}/${name}`;

  var REQUIRED_DEPS = ["version", "storage", "journal", "cache", "repoCache", "assetCache", "digest", "runner", "github", "validator"];
  var OPTIONAL_DEPS = ["budget", "reader", "client", "session", "auth", "reconciler", "uploader", "imageProbe", "now"];
  var STATE_KEYS = ["screen", "jobId", "picker", "pickerAt", "pickerError", "selected", "opening", "openError", "running", "runningNote"];
  var SCREENS = ["jobs", "manifests", "run", "captures", "settings"];
  var GO_PATCH_KEYS = ["jobId"];
  var ForgeCore = class {
    constructor(d) {
      const missing = REQUIRED_DEPS.filter((k) => d[k] == null);
      if (missing.length) throw new Error(`ForgeCore is missing required dependencies: ${missing.join(", ")}`);
      for (const k of [...REQUIRED_DEPS, ...OPTIONAL_DEPS]) if (d[k] != null) this[k] = d[k];
      this.now = d.now ?? (() => Date.now());
      this.authBusy = false;
      this.state = { screen: "jobs", jobId: null, picker: null, pickerAt: null, pickerError: null, selected: null, opening: null, openError: null, running: null, runningNote: "" };
      this._listeners =  new Set();
    }
    static get ACTIONS() {
      return [
        "adopt",
        "blockedPaths",
        "changed",
        "checkSuggestions",
        "clearSelection",
        "drive",
        "establishAuth",
        "exportJob",
        "fail",
        "forgetBinding",
        "go",
        "loadPicker",
        "notify",
        "prepareImages",
        "recheckAuth",
        "requestPause",
        "resolveCaptures",
        "resolveConfirmed",
        "resumeBlockedReason",
        "resumeJob",
        "say",
        "selectManifest",
        "skip",
        "snapshot",
        "startJob",
        "subscribe"
      ];
    }
    snapshot() {
      const out = {};
      for (const k of STATE_KEYS) out[k] = this.state[k] === void 0 ? null : this.state[k];
      return JSON.parse(JSON.stringify(out));
    }
    static get STATE_KEYS() {
      return [...STATE_KEYS];
    }
    clearSelection() {
      this._selection = {};
      this.state.selected = null;
      this.state.opening = null;
      this.state.openError = null;
      this.changed();
    }
    subscribe(fn) {
      if (typeof fn !== "function") throw new TypeError("ForgeCore.subscribe needs a function");
      this._listeners.add(fn);
      return () => this._listeners.delete(fn);
    }
    notify(note) {
      for (const fn of [...this._listeners]) {
        try {
          fn(note);
        } catch {
        }
      }
    }
    fail(context, e) {
      const msg = e instanceof JournalError ? `journal: ${e.message}` : e && e.message || String(e);
      this.notify({ type: "error", context, text: `${context}: ${msg}`, level: "bad", ms: 9e3 });
      return msg;
    }
    say(text, level = "info", ms = 4e3) {
      this.notify({ type: "message", text, level, ms });
    }
    changed() {
      this.notify({ type: "changed" });
    }
    async establishAuth() {
      return this._auth(() => this.auth.establish());
    }
    async recheckAuth() {
      return this._auth(() => this.auth.probe());
    }
    async _auth(fn) {
      if (!this.auth || this.authBusy) return this.auth ? this.auth.state : null;
      this.authBusy = true;
      this.changed();
      try {
        return await fn();
      } finally {
        this.authBusy = false;
        this.changed();
      }
    }
    resumeBlockedReason(job) {
      return resumeBlockedReason(job, this.auth);
    }
    blockedPaths(plan, manifest) {
      return blockedPaths(this.auth, plan, manifest);
    }
    async loadPicker(force) {
      if (this.state.picker && !force) return;
      this.state.pickerError = null;
      try {
        const entries = (await this.github.list(GH.pushDir)).filter((e) => e.type === "file" && /\.json$/i.test(e.name)).map((e) => ({ ...e, number: manifestNumber(e.name), summary: null, loading: true }));
        entries.sort((a, b) => (b.number ?? -1) - (a.number ?? -1) || a.name.localeCompare(b.name));
        this.state.picker = entries;
        this.state.pickerAt = new Date(this.now()).toISOString();
        this.notify({ type: "picker" });
        await Promise.all(entries.map(async (e) => {
          try {
            const key = `gh:${e.path}@${e.sha}`;
            const hit = await this.repoCache.get("github.contents", key);
            const text = hit ? hit.data : await this.github.text(e.path);
            if (!hit) await this.repoCache.put({ path: "github.contents", id: key, data: text });
            e.text = text;
            e.summary = manifestSummary(text);
          } catch (err) {
            e.error = err.message;
          }
          e.loading = false;
          this.notify({ type: "picker" });
        }));
      } catch (e) {
        this.state.picker = this.state.picker || [];
        this.state.pickerError = e.message;
        this.notify({ type: "picker" });
      }
    }
    async selectManifest(entry) {
      if (this._starting || this.state.running) return this.say("Pause the running import before selecting another manifest", "warn");
      const selection = this._selection = {};
      this.state.selected = null;
      this.state.opening = { name: entry.name, step: "loading" };
      this.state.openError = null;
      this.changed();
      const progress = (step) => {
        if (selection === this._selection) {
          this.state.opening = { name: entry.name, step };
          this.changed();
        }
      };
      try {
        let text = entry.text ?? await this.github.text(entry.path);
        const packageData = JSON.parse(text);
        if (packageData.bloodrightCollection) {
          const result = await prepareCollection(this, packageData, { onProgress: progress });
          if (selection !== this._selection) return;
          this.state.selected = { ...result, entry, text: null, collection: result.trees, pack: result.manifest.imagePack, packResult: null };
          this._scopePackProvenance(this.state.selected.pack);
          this.changed();
          if (!result.problems.length && this.state.selected.pack) await this.prepareImages();
          return;
        }
        let bloodright = null;
        if (packageData.bloodright) {
          bloodright = await prepareBloodright({ config: packageData.bloodright, github: this.github, reader: this.reader, storage: this.storage, auth: this.auth, journal: this.journal, imagePack: packageData.imagePack, imgSizes: packageData.imgSizes, imageProbe: this.imageProbe });
          if (selection !== this._selection) return;
          if (bloodright.problems.length) {
            this.state.selected = { entry, text: null, manifest: { capture: { before: [], after: [] }, imgSizes: {} }, plan: [], problems: bloodright.problems, images: [], pack: null, bloodright };
            this.changed();
            return;
          }
          text = JSON.stringify(bloodright.manifest);
        }
        const manifest = parseManifest(text);
        const problems = [];
        let plan = [];
        try {
          plan = planOrder(manifest, JSON.parse(this.storage.getItem("tnr_bk_idmap_v1") || "{}"));
        } catch (e) {
          problems.push(e.message);
        }
        for (const it of plan) {
          const p = it.entity === "ai" || it.entity === "aiProfile" ? [] : this.validator.problems(it.entity, it.data, null);
          for (const x of p) problems.push(`item ${it.idx} (${it.name}): ${x}`);
        }
        const images = [...new Set(plan.flatMap((it) => collectRefs(it.data).filter((r) => r.pfx === "img").map((r) => r.key)))];
        if (selection !== this._selection) return;
        this.state.selected = { entry, text, manifest, plan, problems, images, ...bloodright ? { bloodright } : {}, pack: manifest.imagePack ?? null, packResult: null };
        this._scopePackProvenance(this.state.selected.pack);
        this.state.selected.blocked = this.blockedPaths(plan, manifest);
        this.changed();
        if (this.state.selected.pack) await this.prepareImages();
      } catch (e) {
        const msg = this.fail("select manifest", e);
        if (selection === this._selection) this.state.openError = { name: entry.name, text: msg };
      } finally {
        if (selection === this._selection) {
          this.state.opening = null;
          this.changed();
        }
      }
    }
    async prepareImages(force = false) {
      if (this._starting || this.state.running) return null;
      const s = this.state.selected;
      if (!s || !s.pack) return null;
      return this._queuePack(() => this._prepareImages(s, force));
    }
    _queuePack(fn) {
      const next = () => fn();
      this._packChain = (this._packChain ?? Promise.resolve()).then(next, next);
      return this._packChain;
    }
    _packEpoch = 0;
    _scopePackProvenance(pack) {
      this._packEpoch += 1;
      for (const name of [...this.runner.imgProvenance.keys()]) {
        if (packBinds(pack, name)) continue;
        this.runner.imgProvenance.delete(name);
        this.runner.files.delete(name);
      }
      return this._packEpoch;
    }
    async _prepareImages(s, force) {
      if (this.state.selected !== s) return null;
      const epoch = this._packEpoch;
      this._preparing = true;
      this.changed();
      try {
        const result = await prepareImagePack(this, { pack: s.pack, names: s.images, force });
        if (this.state.selected !== s || this._packEpoch !== epoch) {
          return { ref: result.ref, entries: result.entries, unbound: result.unbound, ok: false, stale: true };
        }
        commitImagePack(this.runner, { pack: s.pack, names: s.images, staged: result.staged });
        s.packResult = { ref: result.ref, entries: result.entries, unbound: result.unbound, ok: result.ok };
        const bad = result.entries.filter((e) => e.state !== "ready");
        if (!bad.length) {
          this.say(`${result.entries.length} repo-backed image(s) verified against ${s.pack.ref.slice(0, 7)}`, "ok");
        } else {
          this.say(`${bad.length} of ${result.entries.length} repo-backed image(s) could not be verified: ${bad.map((e) => `${e.name}: ${e.error}`).join(" | ")}`, "bad", 12e3);
        }
        return result;
      } catch (e) {
        this.fail("prepare repo-backed images", e);
        if (this.state.selected === s) s.packResult = { ref: s.pack.ref, entries: [], unbound: [], ok: false, error: e && e.message || String(e) };
        return null;
      } finally {
        this._preparing = false;
        this.changed();
      }
    }
    async startJob() {
      if (this._starting || this.state.running) return this.say("a job is already running", "warn");
      const s = this.state.selected;
      if (!s) return;
      this._starting = true;
      this._collectionStop = false;
      try {
        await this._startSelected(s);
      } finally {
        this._starting = false;
        this.changed();
      }
    }
    async _startSelected(s, collection = null) {
      if (s.problems.length) return this.say("Resolve the preview problems before starting", "bad");
      const blocked = this.blockedPaths(s.plan, s.manifest);
      if (blocked.length) {
        this.say(`TNR authentication is unavailable; ${blocked.join(", ")} ${blocked.length === 1 ? "is a protected procedure" : "are protected procedures"} and nothing was sent`, "bad", 9e3);
        s.blocked = blocked;
        return this.changed();
      }
      const badImgs = unusablePicks(imagePicks(s.images, this.runner.files, s.manifest.imgSizes, "imageUploader"));
      if (badImgs.length) {
        this.say(`${badImgs.length} image selection(s) do not match the manifest: ${badImgs.map((p) => p.problems[0] ?? `${p.name} is not picked`).join("; ")}. Nothing was sent.`, "bad", 12e3);
        return this.changed();
      }
      const packProblems = packGateProblems(s.pack, s.images, this.runner);
      if (packProblems.length) {
        this.say(`${packProblems.length} repo-backed image(s) are not verified: ${packProblems.join("; ")}. Nothing was sent.`, "bad", 12e3);
        return this.changed();
      }
      if (s.collection) {
        try {
          for (const t of s.collection) assertBloodrightAvailable(this.journal, t.manifest.policy.bloodrightImport.bloodlineId);
        } catch (e) {
          return this.fail("start collection", e);
        }
        const group = `collection-${Date.now().toString(36)}`;
        for (const [index, tree] of s.collection.entries()) {
          if (this._collectionStop) break;
          const jobId2 = await this._startSelected({ ...tree, entry: s.entry }, { id: group, index, total: s.collection.length, path: s.entry.path, name: tree.bloodright.bloodlineName ?? null });
          const job = jobId2 && this.journal.get(jobId2);
          if (!job || job.state !== "DONE" || !job.items.every((it) => it.state === "VERIFIED" && it.verify === "match")) {
            this.say(`Collection stopped at tree ${index + 1}/${s.collection.length}. Resolve this job, then reopen the collection for a fresh preview.`, "warn", 12e3);
            return;
          }
        }
        this.say(this._collectionStop ? "Collection paused. Reopen it for a fresh preview after resolving the current job." : `${s.collection.length} Bloodright trees verified. Results were exported per tree.`, this._collectionStop ? "warn" : "ok", 12e3);
        return;
      }
      const jobId = `${s.entry.number ?? "m"}-${Date.now().toString(36)}${collection ? `-${collection.index}` : ""}`;
      try {
        assertBloodrightAvailable(this.journal, s.manifest.policy?.bloodrightImport?.bloodlineId);
        let manifestPath = s.entry.path;
        if (s.bloodright) {
          manifestPath = `bloodright-job:${jobId}`;
          await this.repoCache.put({ path: "bloodright.manifest", id: manifestPath, data: s.text });
          const saved = await this.repoCache.get("bloodright.manifest", manifestPath);
          if (saved?.data !== s.text) throw new Error("compiled preview was not durably stored");
        }
        if (this._collectionStop) return;
        this.runner.plan(s.text, { jobId, manifestPath, manifestNumber: s.entry.number });
        if (s.bloodright) this.journal.annotateJob(jobId, { bloodrightImport: s.manifest.policy.bloodrightImport, preview: s.bloodright.preview, bloodlineName: s.bloodright.bloodlineName ?? null, ...collection ? { collection } : {} });
      } catch (e) {
        return this.fail("plan", e);
      }
      this.state.selected = null;
      this.go("run", { jobId });
      await this.drive(jobId, () => this.runner.run(jobId));
      return jobId;
    }
    async resumeJob(jobId) {
      if (this._starting || this.state.running) return this.say("a job is already running", "warn");
      const job = this.journal.get(jobId);
      const blocked = this.resumeBlockedReason(job);
      if (blocked) {
        this.say(blocked, "bad", 9e3);
        return this.changed();
      }
      if (!this.runner.manifests.has(jobId)) {
        try {
          const text = job.manifestPath?.startsWith("bloodright-job:") ? (await this.repoCache.get("bloodright.manifest", job.manifestPath))?.data : job.manifestPath ? await this.github.text(job.manifestPath) : null;
          if (!text) throw new Error("saved manifest unavailable; restore its exact exported text before resuming (never recompile an active job)");
          this.runner.attach(jobId, text);
        } catch (e) {
          return this.fail("resume: fetch manifest", e);
        }
      }
      try {
        const attached = this.runner.manifests.get(jobId);
        const pack = attached && attached.manifest ? attached.manifest.imagePack : null;
        const epoch = this._scopePackProvenance(pack);
        if (pack) {
          const names = [...new Set((attached.order || []).flatMap((it) => collectRefs(it.data).filter((r) => r.pfx === "img").map((r) => r.key)))];
          const result = await this._queuePack(async () => {
            const r = await prepareImagePack(this, { pack, names });
            if (this._packEpoch !== epoch) return { ...r, ok: false, stale: true, staged: [] };
            commitImagePack(this.runner, { pack, names, staged: r.staged });
            return r;
          });
          const bad = result.entries.filter((e) => e.state !== "ready");
          if (bad.length || result.stale) {
            const detail = result.stale ? "the selection changed while the images were being fetched, so nothing was installed" : bad.map((e) => `${e.name}: ${e.error}`).join(" | ");
            this.say(`resume refused: repo-backed image(s) could not be verified: ${detail}. Nothing was sent.`, "bad", 12e3);
            return this.changed();
          }
        }
      } catch (e) {
        return this.fail("resume: prepare repo-backed images", e);
      }
      this.go("run", { jobId });
      const hasSent = job.items.some((i) => i.state === "SENT");
      await this.drive(jobId, () => hasSent ? this.runner.resume(jobId) : this.runner.run(jobId));
    }
    go(screen, patch = {}) {
      if (!SCREENS.includes(screen)) throw new Error(`unknown screen ${JSON.stringify(screen)}`);
      if (patch === null || typeof patch !== "object" || Array.isArray(patch)) throw new TypeError("go() patch must be an object");
      const unknown = Object.keys(patch).filter((k) => !GO_PATCH_KEYS.includes(k));
      if (unknown.length) throw new Error(`go() refuses unknown state keys: ${unknown.join(", ")}; add a named action instead`);
      for (const k of GO_PATCH_KEYS) if (k in patch) this.state[k] = patch[k];
      this.state.screen = screen;
      this.changed();
    }
    async drive(jobId, fn) {
      if (this.state.running) return this.say("a job is already running", "warn");
      this.state.running = jobId;
      this.state.runningNote = "";
      this.changed();
      this.notify({ type: "driving", jobId });
      try {
        const s = await fn();
        if (s.state === "DONE" || s.state === "INCOMPLETE") {
          try {
            await resolveCaptures(this, jobId);
          } catch (e) {
            this.fail("resolve full captures", e);
          }
        }
        const job = this.journal.get(jobId);
        const head = runHeadline(job, s);
        this.say(head.text, head.kind, head.ms);
        if (s.state === "DONE" || s.state === "INCOMPLETE") await this.exportJob(jobId, { auto: true });
      } catch (e) {
        this.fail("run", e);
      } finally {
        this.state.running = null;
        this.notify({ type: "idle", jobId });
        this.changed();
      }
    }
    requestPause() {
      this._collectionStop = true;
      this.runner.requestPause();
      this.say("pausing after the current item finishes", "warn");
    }
    adopt(jobId, idx, id2) {
      try {
        this.runner.adopt(jobId, idx, id2);
        this.changed();
      } catch (e) {
        this.fail("adopt", e);
      }
    }
    skip(jobId, idx) {
      try {
        this.runner.skip(jobId, idx);
        this.changed();
      } catch (e) {
        this.fail("skip", e);
      }
    }
    resolveConfirmed(jobId, idx, options) {
      if (this._starting || this.state.running) return this.say("Pause the running job before resolving a write", "warn");
      try {
        this.runner.resolveConfirmed(jobId, idx, options);
        this.changed();
      } catch (e) {
        this.fail("resolve write", e);
      }
    }
    forgetBinding(jobId, idx, options) {
      if (this._starting || this.state.running) return this.say("Pause the running job before forgetting a binding", "warn");
      try {
        this.runner.forgetBinding(jobId, idx, options);
        this.clearSelection();
        this.say("Saved binding forgotten. Prepare a fresh preview before creating or rebinding the record.", "warn");
      } catch (e) {
        this.fail("forget binding", e);
      }
    }
    resolveCaptures(jobId) {
      return resolveCaptures(this, jobId);
    }
    async exportJob(jobId, { auto = false } = {}) {
      let captures;
      try {
        captures = await resolveCaptures(this, jobId);
      } catch (e) {
        this.fail("resolve full captures", e);
        const j = this.journal.get(jobId);
        captures = [...j.capturesBefore || [], ...j.capturesAfter || []];
      }
      const job = this.journal.get(jobId);
      const bundle = buildBundle(this, job, captures);
      if (job.manifestPath?.startsWith("bloodright-job:")) {
        try {
          const frozen = await this.repoCache.get("bloodright.manifest", job.manifestPath);
          bundle.compiledManifest = frozen?.data ? JSON.parse(frozen.data) : null;
        } catch (e) {
          bundle.compiledManifest = null;
          bundle.compiledManifestError = e.message;
        }
      }
      const name = job.collection ? bundleName(this.now).replace(".json", `_${job.collection.index + 1}.json`) : bundleName(this.now);
      const text = JSON.stringify(bundle, null, 1);
      const synced = repoSyncReady(this.storage);
      if (synced) {
        try {
          const r = await this.github.put(inboxPath(name), text, `results: ${name} (forge)`);
          this.say(`committed ${name}${r.sha ? " @" + r.sha.slice(0, 7) : ""}`, "ok");
          this._markExported(jobId, name, true);
          return;
        } catch (e) {
          this.fail("commit results", e);
        }
      }
      if (!auto || !synced) {
        this.notify({ type: "export", text, name });
        this._markExported(jobId, name, false);
      }
    }
    async checkSuggestions(jobId) {
      const job = this.journal.get(jobId);
      const items = (job?.items ?? []).filter((it) => it.suggestion?.id);
      if (!items.length) return this.say("This job has no suggestions to check", "warn");
      try {
        this.auth?.assert?.("contentReview.getProposal");
      } catch (e) {
        return this.fail("check suggestions", e);
      }
      const tally = {};
      for (const it of items) {
        const r = await this.client.call("contentReview.getProposal", { id: it.suggestion.id });
        if (!r.ok) {
          this.fail("check suggestions", new Error(r.error?.message ?? "read failed"));
          break;
        }
        const p = r.data;
        const status = p ? p.status : "NOT FOUND";
        tally[status] = (tally[status] ?? 0) + 1;
        this.journal.annotate(jobId, it.idx, { suggestion: { ...it.suggestion, status, reviewedBy: p?.reviewedBy ?? null, note: p?.reviewNote ?? p?.rejectReason ?? p?.outdatedReason ?? null, checkedAt: new Date(this.now()).toISOString() } });
      }
      this.say(`Suggestions: ${Object.entries(tally).map(([k, v]) => `${v} ${k.toLowerCase()}`).join(", ")}`, "ok", 8e3);
      this.changed();
    }
    _markExported(jobId, name, committed) {
      try {
        this.journal.annotateJob(jobId, { exportedAt: new Date(this.now()).toISOString(), exportName: name, exportCommitted: committed });
      } catch {
      }
    }
  };

  var SCREENS2 = { jobs: ["Jobs", JobsScreen], manifests: ["Manifests", ManifestsScreen], run: ["Run", RunScreen], captures: ["Captures", CapturesScreen], settings: ["Settings", SettingsScreen] };
  var App = class {
    constructor(d) {
      Object.assign(this, d);
      this.now = d.now ?? (() => Date.now());
      this.exit = d.exit ?? null;
      this.core = d.core ?? new ForgeCore({ ...d, now: this.now });
      this.view = { pickerQuery: "", renderPicker: null, persisted: null, exports: [] };
      this.root = null;
      this._tick = null;
      this._unsubscribe = this.core.subscribe((n) => this._onCore(n));
    }
    get state() {
      if (!this._stateView || this._stateViewOf !== this.core.state) {
        this._stateViewOf = this.core.state;
        this._stateView = new Proxy(this.core.state, {
          set(_t, k) {
            throw new TypeError(`core machine state is read-only from the view; ${String(k)} must change through a core action`);
          },
          defineProperty(_t, k) {
            throw new TypeError(`core machine state is read-only from the view; ${String(k)} must change through a core action`);
          },
          deleteProperty(_t, k) {
            throw new TypeError(`core machine state is read-only from the view; ${String(k)} must change through a core action`);
          }
        });
      }
      return this._stateView;
    }
    get authBusy() {
      return this.core.authBusy;
    }
    set authBusy(v) {
      this.core.authBusy = v;
    }
    _onCore(n) {
      switch (n.type) {
        case "changed":
          return this.refresh();
        case "message":
          return this.toast(n.text, n.level, n.ms);
        case "error": {
          this.toast(n.text, n.level, n.ms);
          this.log(n.text);
          return;
        }
        case "picker":
          return void (this.view.renderPicker && this.view.renderPicker());
        case "export":
          return this.showExport(n.text, n.name);
        case "driving": {
          if (this._tick) clearInterval(this._tick);
          this._tick = setInterval(() => {
            if (this.state.screen === "run") this.refresh();
          }, 1500);
          return;
        }
        case "idle": {
          if (this._tick) {
            clearInterval(this._tick);
            this._tick = null;
          }
          return;
        }
        default:
          return;
      }
    }
    mount(container, doc = document) {
      installCss(CSS, doc);
      this.root = h("div", { class: "f-app" });
      this.$top = h(
        "div",
        { class: "f-top" },
        h("span", { class: "f-title" }, "TNR forge"),
        h("span", { class: "f-ver" }, this.version),
        this.exit ? h("button", { class: "f-exit", onClick: () => this.close() }, "Close") : null
      );
      this.$nav = h("nav", { class: "f-nav" });
      this.$auth = h("div", { class: "f-authbar" });
      this.$main = h("main", { class: "f-main" });
      this.$toast = h("div", { class: "f-toast" });
      this.root.append(this.$top, this.$nav, this.$auth, this.$main, this.$toast);
      if (this.auth && typeof this.auth.onChange === "function") this._unwatchAuth = this.auth.onChange(() => this.refresh());
      container.appendChild(this.root);
      const open = this.journal.resumable();
      if (open.length) this.core.go("jobs");
      this.refresh();
      this._persist();
      return this.root;
    }
    go(screen, patch = {}) {
      this.core.go(screen, patch);
    }
    refresh() {
      replace(this.$nav, Object.entries(SCREENS2).map(([k, [label]]) => h("button", { "aria-current": this.state.screen === k ? "page" : null, onClick: () => this.go(k) }, label)));
      if (this.$auth) replace(this.$auth, this.authBanner());
      try {
        replace(this.$main, this.view.exports.length ? this.exportsCard() : null, SCREENS2[this.state.screen][1](this));
      } catch (e) {
        replace(this.$main, h("div", { class: "f-banner bad" }, h("b", {}, "This screen failed to render. "), h("div", { class: "f-err" }, String(e && e.stack || e))));
      }
    }
    toast(text, kind = "info", ms = 4e3) {
      const el = h("div", { class: "f-banner " + kind, title: "tap to dismiss", onClick: () => el.remove() }, text);
      this.$toast.appendChild(el);
      while (this.$toast.childElementCount > 2) this.$toast.firstElementChild.remove();
      setTimeout(() => el.remove(), ms);
    }
    fail(context, e) {
      this.core.fail(context, e);
    }
    log(msg) {
      (this.logs ??= []).push({ at: new Date(this.now()).toISOString(), msg });
    }
    close() {
      if (!this.exit) return;
      if (this.state.running) return this.toast("a job is running; pause it before closing Forge", "warn");
      if (this._unwatchAuth) {
        this._unwatchAuth();
        this._unwatchAuth = null;
      }
      if (this._tick) {
        clearInterval(this._tick);
        this._tick = null;
      }
      this.exit();
    }
    establishAuth() {
      return this.core.establishAuth();
    }
    recheckAuth() {
      return this.core.recheckAuth();
    }
    authBanner() {
      const facts = authFacts(this.auth, this.authBusy);
      if (!facts) return null;
      const recheck = h("button", { disabled: this.authBusy, onClick: () => this.recheckAuth() }, this.authBusy ? "Checking\u2026" : "Re-check");
      if (facts.ready) {
        return h("div", { class: "f-banner ok f-compact" }, h("span", {}, "TNR session active"), h("div", { class: "f-actions" }, recheck));
      }
      if (facts.probing) {
        return h("div", { class: "f-banner info" }, "Checking the TNR session\u2026");
      }
      return h(
        "div",
        { class: "f-banner bad" },
        h(
          "div",
          {},
          h("b", {}, facts.signedOut ? "TNR authentication unavailable. " : "TNR authentication not confirmed. "),
          facts.signedOut ? "Forge could not use a signed-in game session in this browser. Protected reads and writes are blocked and nothing protected will be sent." : "Forge could not confirm a signed-in session, so protected reads and writes are blocked. This is not a read failure."
        ),
        h("div", { class: "f-mute" }, "Sign in to the game in this browser (close Forge, sign in, reopen /forge), then re-check. Capture-only manifests can still run."),
        facts.detail ? h("div", { class: "f-mute" }, facts.detail) : null,
        h("div", { class: "f-actions" }, recheck)
      );
    }
    resumeBlockedReason(job) {
      return this.core.resumeBlockedReason(job);
    }
    blockedPaths(plan, manifest) {
      return this.core.blockedPaths(plan, manifest);
    }
    confirm(text, fn) {
      if (globalThis.confirm ? globalThis.confirm(text) : true) Promise.resolve().then(fn).catch((e) => this.fail("action", e));
    }
    showExport(text, title) {
      const name = /\.json$/.test(title) ? title : `${String(title).replace(/[^\w.-]+/g, "_")}.txt`;
      this.view.exports = [{ text, title, name }, ...this.view.exports.filter((x) => x.title !== title)].slice(0, 20);
      this.refresh();
      const scroller = this.root && this.root.parentElement;
      if (scroller && typeof scroller.scrollTo === "function") scroller.scrollTo(0, 0);
    }
    exportsCard() {
      const xs = this.view.exports;
      const download = (x) => {
        try {
          const url2 = URL.createObjectURL(new Blob([x.text], { type: x.name.endsWith(".json") ? "application/json" : "text/plain" }));
          const a = h("a", { href: url2, download: x.name, style: { display: "none" } });
          this.root.appendChild(a);
          a.click();
          a.remove();
          setTimeout(() => URL.revokeObjectURL(url2), 6e4);
          return true;
        } catch (e) {
          this.toast(`download failed: ${e.message}; use Copy`, "bad", 8e3);
          return false;
        }
      };
      const remove = (gone) => {
        this.view.exports = this.view.exports.filter((y) => !gone.includes(y));
        this.refresh();
      };
      const row = (x) => {
        const ta = h("textarea", { readOnly: true, value: x.text });
        const copy2 = async () => {
          try {
            await navigator.clipboard.writeText(x.text);
            this.toast("copied", "ok");
          } catch {
            details.open = true;
            ta.focus();
            ta.select();
            this.toast("Copy was blocked; the text is selected, copy it from the box", "warn", 8e3);
          }
        };
        const details = h("details", {}, h("summary", {}, "Show text"), ta);
        return h(
          "div",
          { class: "f-row" },
          h("div", { class: "f-grow" }, h("div", { class: "f-mono" }, x.title), details),
          h("button", { onClick: () => download(x) }, "Download"),
          h("button", { onClick: copy2 }, "Copy"),
          h("button", { title: "remove from this list", onClick: () => remove([x]) }, "\u2715")
        );
      };
      return h(
        "div",
        { class: "f-card f-exports" },
        h(
          "div",
          { class: "f-row" },
          h(
            "div",
            { class: "f-grow" },
            h("b", {}, `Results to save (${xs.length})`),
            h("div", { class: "f-mute" }, "Download keeps each as a file. Remove a row once it is saved.")
          ),
          h("button", { class: "f-primary", onClick: () => {
            for (const x of xs) download(x);
          } }, xs.length > 1 ? "Download all" : "Download"),
          h("button", { onClick: () => this.confirm(`Remove ${xs.length === 1 ? "this result" : `all ${xs.length} results`} from the list? Only do this once they are saved.`, () => remove([...xs])) }, "Clear")
        ),
        xs.length > 1 ? h("details", {}, h("summary", {}, `Show ${xs.length} files`), xs.map(row)) : row(xs[0])
      );
    }
    clearSelection() {
      return this.core.clearSelection();
    }
    loadPicker(force) {
      return this.core.loadPicker(force);
    }
    selectManifest(entry) {
      const scroller = this.root && this.root.parentElement;
      if (scroller && typeof scroller.scrollTo === "function") scroller.scrollTo(0, 0);
      return this.core.selectManifest(entry);
    }
    prepareImages(force) {
      return this.core.prepareImages(force);
    }
    startJob() {
      return this.core.startJob();
    }
    resumeJob(jobId) {
      return this.core.resumeJob(jobId);
    }
    requestPause() {
      return this.core.requestPause();
    }
    adopt(jobId, idx, id2) {
      return this.core.adopt(jobId, idx, id2);
    }
    skip(jobId, idx) {
      return this.core.skip(jobId, idx);
    }
    resolveConfirmed(jobId, idx, options) {
      return this.core.resolveConfirmed(jobId, idx, options);
    }
    forgetBinding(jobId, idx, options) {
      return this.core.forgetBinding(jobId, idx, options);
    }
    resolveCaptures(jobId) {
      return this.core.resolveCaptures(jobId);
    }
    exportJob(jobId, opts) {
      return this.core.exportJob(jobId, opts);
    }
    checkSuggestions(jobId) {
      return this.core.checkSuggestions(jobId);
    }
    async _persist() {
      try {
        if (navigator.storage && navigator.storage.persist) {
          this.view.persisted = await navigator.storage.persist();
          const el = document.getElementById("f-persist");
          if (el) el.textContent = String(this.view.persisted);
        }
      } catch {
      }
    }
  };

  var ENTRY_PATH = "/forge";
  var CARRIER_PATH = "/";
  var ARM_KEY = "tnr_forge_armed_v1";
  var MAX_HOPS = 2;
  var MAX_HOST_LOSSES = 1;
  var CARRIER_GRACE_MS = 15e3;
  var CARRIER_POLL_MS = 50;
  var OLD_BUILDER_CLASSES = ["k-fab", "k-pn"];
  var OVERLAY_CLASS = "f-host";
  function onEntryPath(loc = location) {
    return loc.pathname === ENTRY_PATH || loc.pathname.startsWith(ENTRY_PATH + "/");
  }
  function readArm(win) {
    try {
      return JSON.parse(win.sessionStorage.getItem(ARM_KEY) || "null");
    } catch {
      return null;
    }
  }
  function isArmed(win) {
    const a = readArm(win);
    return !!(a && a.armed);
  }
  function armHops(win) {
    const a = readArm(win);
    return a && Number.isInteger(a.hops) ? a.hops : 0;
  }
  function armFailure(win) {
    const a = readArm(win);
    return a && typeof a.failure === "string" ? a.failure : null;
  }
  function arm(win, { hops = null, failure = void 0 } = {}) {
    const next = hops == null ? armHops(win) + 1 : hops;
    const record = { armed: true, hops: next };
    const kept = failure === void 0 ? armFailure(win) : failure;
    if (typeof kept === "string" && kept) record.failure = kept;
    try {
      win.sessionStorage.setItem(ARM_KEY, JSON.stringify(record));
    } catch {
    }
    return next;
  }
  function disarm(win) {
    try {
      win.sessionStorage.removeItem(ARM_KEY);
    } catch {
    }
  }
  function entryTakeover(doc = document, win = window) {
    try {
      win.stop();
    } catch {
    }
    const html = doc.documentElement || doc.appendChild(doc.createElement("html"));
    clear(html);
    const head = h("head", {}, h("meta", { charset: "utf-8" }), h("meta", { name: "viewport", content: "width=device-width, initial-scale=1, viewport-fit=cover" }), h("title", {}, "TNR forge"));
    const body = h("body", {});
    html.append(head, body);
    return { html, head, body };
  }
  function whenBodyReady(doc = document, win = window) {
    return new Promise((resolve) => {
      if (doc.body) return resolve(doc.body);
      let settled = false;
      let mo = null;
      let timer = null;
      const cleanup = () => {
        if (mo) {
          try {
            mo.disconnect();
          } catch {
          }
          mo = null;
        }
        if (timer != null) {
          try {
            win.clearInterval(timer);
          } catch {
          }
          timer = null;
        }
        try {
          doc.removeEventListener("DOMContentLoaded", check);
        } catch {
        }
        try {
          doc.removeEventListener("readystatechange", check);
        } catch {
        }
      };
      function check() {
        if (settled || !doc.body) return;
        settled = true;
        cleanup();
        resolve(doc.body);
      }
      try {
        mo = new win.MutationObserver(check);
        mo.observe(doc.documentElement || doc, { childList: true, subtree: true });
      } catch {
        mo = null;
      }
      try {
        doc.addEventListener("DOMContentLoaded", check);
      } catch {
      }
      try {
        doc.addEventListener("readystatechange", check);
      } catch {
      }
      if (!mo) {
        try {
          timer = win.setInterval(check, 25);
        } catch {
          timer = null;
        }
      }
      check();
    });
  }
  function carrierHydrated(doc = document) {
    const body = doc.body;
    if (!body) return false;
    let keys;
    try {
      keys = Object.keys(body);
    } catch {
      return false;
    }
    return keys.some((k) => k.startsWith("__reactFiber$") || k.startsWith("__reactProps$"));
  }
  function carrierRuntimeSettled(doc = document, win = window) {
    if (doc.readyState !== "complete") return false;
    const c = win && win.Clerk;
    return !!(c && c.loaded === true);
  }
  function carrierReadiness(doc = document, win = window) {
    if (!doc.body) return null;
    if (carrierHydrated(doc)) return "hydrated";
    if (carrierRuntimeSettled(doc, win)) return "runtime";
    return null;
  }
  function whenCarrierReady(doc = document, win = window, { graceMs = CARRIER_GRACE_MS, pollMs = CARRIER_POLL_MS } = {}) {
    return new Promise((resolve) => {
      const now = carrierReadiness(doc, win);
      if (now) return resolve(now);
      let settled = false;
      let mo = null;
      let timer = null;
      let deadline = null;
      const cleanup = () => {
        if (mo) {
          try {
            mo.disconnect();
          } catch {
          }
          mo = null;
        }
        if (timer != null) {
          try {
            win.clearInterval(timer);
          } catch {
          }
          timer = null;
        }
        if (deadline != null) {
          try {
            win.clearTimeout(deadline);
          } catch {
          }
          deadline = null;
        }
        for (const ev of ["DOMContentLoaded", "readystatechange"]) {
          try {
            doc.removeEventListener(ev, check);
          } catch {
          }
        }
        try {
          win.removeEventListener("load", check);
        } catch {
        }
      };
      const finish = (value) => {
        if (settled) return;
        settled = true;
        cleanup();
        resolve(value);
      };
      function check() {
        if (settled) return;
        const via = carrierReadiness(doc, win);
        if (via) return finish(via);
        if (deadline == null && doc.readyState === "complete") {
          try {
            deadline = win.setTimeout(() => finish(null), graceMs);
          } catch {
            deadline = null;
          }
        }
      }
      try {
        mo = new win.MutationObserver(check);
        mo.observe(doc.documentElement || doc, { childList: true, subtree: true });
      } catch {
        mo = null;
      }
      for (const ev of ["DOMContentLoaded", "readystatechange"]) {
        try {
          doc.addEventListener(ev, check);
        } catch {
        }
      }
      try {
        win.addEventListener("load", check);
      } catch {
      }
      try {
        timer = win.setInterval(check, pollMs);
      } catch {
        timer = null;
      }
      check();
    });
  }
  var LAUNCHER_TAG = "tnr-forge-launch";
  function launcherShown(doc = document) {
    return !!doc.querySelector(LAUNCHER_TAG);
  }
  function mountLauncher(doc = document, win = window, { onOpen } = {}) {
    if (!doc.body || launcherShown(doc) || alreadyMounted(doc)) return null;
    const el = doc.createElement(LAUNCHER_TAG);
    el.setAttribute("style", "all:initial;position:fixed;left:12px;bottom:62px;z-index:2147482000;");
    let root = el;
    try {
      if (typeof el.attachShadow === "function") root = el.attachShadow({ mode: "open" });
    } catch {
      root = el;
    }
    const btn = doc.createElement("button");
    btn.type = "button";
    btn.textContent = "Forge";
    btn.title = "Open TNR forge";
    btn.setAttribute("aria-label", "Open TNR forge");
    btn.setAttribute("style", "all:initial;cursor:pointer;background:#2b4a7a;color:#fff;border-radius:10px;padding:11px 16px;font:600 14px system-ui,sans-serif;box-shadow:0 4px 16px #0008;");
    let used = false;
    for (const ev of ["pointerdown", "mousedown", "touchstart"]) {
      btn.addEventListener(ev, (e) => {
        try {
          e.stopPropagation();
        } catch {
        }
      });
    }
    btn.addEventListener("click", (e) => {
      try {
        e.preventDefault();
        e.stopPropagation();
      } catch {
      }
      if (used) return;
      used = true;
      el.remove();
      if (onOpen) {
        try {
          Promise.resolve(onOpen()).catch(() => {
          });
        } catch {
        }
      }
    });
    root.appendChild(btn);
    doc.body.appendChild(el);
    return el;
  }
  function alreadyMounted(doc = document) {
    return !!doc.querySelector("." + OVERLAY_CLASS);
  }
  function mountHost(doc = document, win = window, { onLost = null } = {}) {
    const host = h("div", { class: OVERLAY_CLASS });
    const root = doc.documentElement;
    const body = doc.body;
    const prevHtmlOverflow = root ? root.style.overflow : "";
    const prevBodyOverflow = body ? body.style.overflow : "";
    if (root) root.style.overflow = "hidden";
    if (body) body.style.overflow = "hidden";
    body.appendChild(host);
    let bodyMo = null;
    let rootMo = null;
    let released = false;
    let lost = false;
    const disconnect = () => {
      if (bodyMo) {
        try {
          bodyMo.disconnect();
        } catch {
        }
        bodyMo = null;
      }
      if (rootMo) {
        try {
          rootMo.disconnect();
        } catch {
        }
        rootMo = null;
      }
    };
    const attached = () => !released && host.isConnected && doc.body === body && body.contains(host);
    const reportLost = () => {
      if (released || lost || attached()) return;
      lost = true;
      disconnect();
      if (onLost) {
        try {
          onLost(host);
        } catch {
        }
      }
    };
    try {
      bodyMo = new win.MutationObserver((muts) => {
        for (const m of muts) {
          for (const n of m.addedNodes) {
            if (n && n.nodeType === 1 && OLD_BUILDER_CLASSES.some((c) => n.classList && n.classList.contains(c))) n.remove();
          }
          for (const n of m.removedNodes) if (n === host) return reportLost();
        }
      });
      bodyMo.observe(body, { childList: true });
    } catch {
      bodyMo = null;
    }
    try {
      rootMo = new win.MutationObserver(() => {
        if (doc.body !== body) reportLost();
      });
      if (root) rootMo.observe(root, { childList: true });
    } catch {
      rootMo = null;
    }
    const release = () => {
      released = true;
      disconnect();
      host.remove();
      if (root) root.style.overflow = prevHtmlOverflow;
      if (doc.body) doc.body.style.overflow = prevBodyOverflow;
    };
    return { body: host, observer: bodyMo, attached, release };
  }
  function pageAuthRuntime(win = window) {
    return () => {
      const c = win && win.Clerk;
      if (!c) return null;
      const loaded = c.loaded === true;
      let signedIn = null;
      if (loaded) signedIn = !!(c.session || c.user);
      return { loaded, signedIn };
    };
  }

  var nested_default = JSON.parse('{"_meta":{"generated_by":"forge/tools/derive_nested.mjs","pin":"2af4b32066c39e2868efae5dba6b339278701dca","files":{"combat":"app/src/validators/combat.ts","objectives":"app/src/validators/objectives.ts","rewards":"app/src/validators/rewards.ts","ai":"app/src/validators/ai.ts","base":"app/src/validators/base.ts","rewardPackages":"app/src/validators/rewardPackages.ts"},"searched":85,"note":"Allowed KEY SETS only, per discriminator value. No types, bounds or enums: a bound this tool cannot see is the 45g.tag_power_max mistake, and a key set is checkable without zod.","format":"Shared key-set table. `sets` holds every distinct allowed key set once; each section value is an index into it (or a map of discriminator value -> index). forge/src/runner/validate.mjs expandNested() restores the per-discriminator key sets and FAILS CLOSED on an index this file does not define."},"sets":[["appearAnimation","appearSfx","calculation","coordinateTargeting","description","direction","disappearAnimation","disappearSfx","friendlyFire","power","powerPerLevel","rounds","staticAnimation","staticAssetPath","target","timeTracker","type"],["appearAnimation","appearSfx","calculation","coordinateTargeting","description","direction","disappearAnimation","disappearSfx","elements","friendlyFire","generalTypes","poolsAffected","power","powerPerLevel","rounds","staticAnimation","staticAssetPath","target","timeTracker","type"],["appearAnimation","appearSfx","calculation","coordinateTargeting","description","direction","disappearAnimation","disappearSfx","elements","friendlyFire","generalTypes","power","powerPerLevel","rounds","staticAnimation","staticAssetPath","target","timeTracker","type"],["absorbPercentage","appearAnimation","appearSfx","calculation","coordinateTargeting","curHealth","description","direction","disappearAnimation","disappearSfx","friendlyFire","maxHealth","power","powerPerLevel","rounds","staticAnimation","staticAssetPath","target","timeTracker","type"],["appearAnimation","appearSfx","calculation","coordinateTargeting","description","direction","disappearAnimation","disappearSfx","friendlyFire","power","powerPerLevel","rounds","shieldRounds","staticAnimation","staticAssetPath","target","timeTracker","type"],["allowBloodlineDamageDecrease","allowBloodlineDamageIncrease","appearAnimation","appearSfx","calculation","coordinateTargeting","description","direction","disappearAnimation","disappearSfx","dmgModifier","elements","friendlyFire","generalTypes","power","powerPerLevel","residualModifier","rounds","statTypes","staticAnimation","staticAssetPath","target","timeTracker","type"],["aggroMode","appearAnimation","appearSfx","calculation","coordinateTargeting","description","direction","disappearAnimation","disappearSfx","friendlyFire","power","powerPerLevel","rounds","staticAnimation","staticAssetPath","target","timeTracker","type"],["actionsAffected","appearAnimation","appearSfx","calculation","coordinateTargeting","description","direction","disappearAnimation","disappearSfx","friendlyFire","power","powerPerLevel","rounds","staticAnimation","staticAssetPath","target","timeTracker","type"],["appearAnimation","appearSfx","calculation","coordinateTargeting","description","direction","disappearAnimation","disappearSfx","elements","friendlyFire","power","powerPerLevel","rounds","staticAnimation","staticAssetPath","target","timeTracker","type"],["affectedElements","affectedTag","appearAnimation","appearSfx","calculation","coordinateTargeting","description","direction","disappearAnimation","disappearSfx","friendlyFire","power","powerPerLevel","rounds","staticAnimation","staticAssetPath","target","timeTracker","type"],["appearAnimation","appearSfx","calculation","coordinateTargeting","description","direction","disappearAnimation","disappearSfx","friendlyFire","poolsAffected","power","powerPerLevel","rounds","staticAnimation","staticAssetPath","target","timeTracker","type"],["appearAnimation","appearSfx","calculation","coordinateTargeting","description","direction","disappearAnimation","disappearSfx","friendlyFire","masteryTypes","power","powerPerLevel","rounds","staticAnimation","staticAssetPath","target","timeTracker","type"],["appearAnimation","appearSfx","calculation","coordinateTargeting","description","direction","disappearAnimation","disappearSfx","elements","friendlyFire","generalTypes","power","powerPerLevel","rounds","statTypes","staticAnimation","staticAssetPath","target","timeTracker","type"],["appearAnimation","appearSfx","calculation","coordinateTargeting","delayRounds","description","direction","disappearAnimation","disappearSfx","friendlyFire","power","powerPerLevel","rounds","staticAnimation","staticAssetPath","target","timeTracker","type"],["allowBloodlineDamageDecrease","allowBloodlineDamageIncrease","appearAnimation","appearSfx","calculation","coordinateTargeting","description","direction","disappearAnimation","disappearSfx","dmgModifier","friendlyFire","generalTypes","power","powerPerLevel","residualModifier","rounds","statTypes","staticAnimation","staticAssetPath","target","timeTracker","type"],["appearAnimation","appearSfx","calculation","coordinateTargeting","description","direction","disappearAnimation","disappearSfx","friendlyFire","power","powerPerLevel","rank","rounds","staticAnimation","staticAssetPath","target","timeTracker","type"],["appearAnimation","appearSfx","calculation","coordinateTargeting","description","direction","disappearAnimation","disappearSfx","friendlyFire","jutsuIds","power","powerPerLevel","rounds","staticAnimation","staticAssetPath","target","timeTracker","type"],["appearAnimation","appearSfx","blocks","calculation","coordinateTargeting","description","direction","disappearAnimation","disappearSfx","friendlyFire","power","powerPerLevel","rounds","staticAnimation","staticAssetPath","target","timeTracker","type"],["appearAnimation","appearSfx","calculation","coordinateTargeting","description","direction","disappearAnimation","disappearSfx","friendlyFire","power","powerPerLevel","rewardMode","reward_anbupoints","reward_badges","reward_bloodline_experience","reward_bloodlines","reward_bukijutsu_experience","reward_clanpoints","reward_crafting_experience","reward_exp","reward_gathering_experience","reward_gathering_items","reward_gathering_items_ids","reward_genjutsu_experience","reward_hunter_items","reward_hunter_items_ids","reward_hunting_experience","reward_items","reward_jutsus","reward_mastery_rank","reward_mastery_stat","reward_medical_experience","reward_money","reward_ninjutsu_experience","reward_pet_experience","reward_pets","reward_prestige","reward_rank","reward_reputation","reward_sage_mastery_experience","reward_sage_modes","reward_sage_stat_experience","reward_seichi_silver","reward_skillpoints","reward_taijutsu_experience","reward_titles","reward_tokens","reward_village_membership","reward_war_damage","reward_war_healing","rounds","staticAnimation","staticAssetPath","target","timeTracker","type","weightedCache"],["appearAnimation","appearSfx","calculation","coordinateTargeting","description","direction","disappearAnimation","disappearSfx","friendlyFire","power","powerPerLevel","rounds","skillId","staticAnimation","staticAssetPath","target","timeTracker","type"],["appearAnimation","appearSfx","calculation","coordinateTargeting","description","direction","disappearAnimation","disappearSfx","friendlyFire","power","powerPerLevel","questId","rounds","staticAnimation","staticAssetPath","target","timeTracker","type"],["appearAnimation","appearSfx","calculation","coordinateTargeting","description","direction","disappearAnimation","disappearSfx","elements","friendlyFire","generalTypes","power","powerPerLevel","robPercentage","rounds","statTypes","staticAnimation","staticAssetPath","target","timeTracker","type"],["appearAnimation","appearSfx","calculation","coordinateTargeting","description","direction","disappearAnimation","disappearSfx","friendlyFire","health","power","powerPerLevel","rounds","staticAnimation","staticAssetPath","target","timeTracker","type"],["apReduction","appearAnimation","appearSfx","calculation","coordinateTargeting","description","direction","disappearAnimation","disappearSfx","friendlyFire","power","powerPerLevel","rounds","staticAnimation","staticAssetPath","target","timeTracker","type"],["aiHp","aiId","appearAnimation","appearSfx","calculation","coordinateTargeting","description","direction","disappearAnimation","disappearSfx","friendlyFire","playerControlled","power","powerPerLevel","rounds","staticAnimation","staticAssetPath","target","timeTracker","type"],["appearAnimation","appearSfx","calculation","coordinateTargeting","description","direction","disappearAnimation","disappearSfx","dmgModifier","elements","friendlyFire","generalTypes","items","jutsus","power","powerPerLevel","rounds","statTypes","staticAnimation","staticAssetPath","target","timeTracker","type"],["attackers","attackers_max_per_battle","attackers_scale_gains","attackers_scaled_to_user","description","durationSeconds","id","latitude","locationDescription","locationName","longitude","nextObjectiveId","overworldPlacementId","reward_anbupoints","reward_badges","reward_bloodline_experience","reward_bloodlines","reward_bukijutsu_experience","reward_clanpoints","reward_crafting_experience","reward_exp","reward_gathering_experience","reward_gathering_items","reward_gathering_items_ids","reward_genjutsu_experience","reward_hunter_items","reward_hunter_items_ids","reward_hunting_experience","reward_items","reward_jutsus","reward_level","reward_mastery_rank","reward_mastery_stat","reward_medical_experience","reward_money","reward_ninjutsu_experience","reward_packages","reward_pet_experience","reward_prestige","reward_rank","reward_reputation","reward_sage_mastery_experience","reward_sage_modes","reward_sage_stat_experience","reward_seichi_silver","reward_skillpoints","reward_stats","reward_taijutsu_experience","reward_titles","reward_tokens","reward_village_membership","reward_war_damage","reward_war_healing","sceneBackground","sceneCharacters","sector","structureAssetId","structureScale","successDescription","task","value"],["description","id","latitude","locationDescription","locationName","longitude","nextObjectiveId","overworldPlacementId","reward_anbupoints","reward_badges","reward_bloodline_experience","reward_bloodlines","reward_bukijutsu_experience","reward_clanpoints","reward_crafting_experience","reward_exp","reward_gathering_experience","reward_gathering_items","reward_gathering_items_ids","reward_genjutsu_experience","reward_hunter_items","reward_hunter_items_ids","reward_hunting_experience","reward_items","reward_jutsus","reward_level","reward_mastery_rank","reward_mastery_stat","reward_medical_experience","reward_money","reward_ninjutsu_experience","reward_packages","reward_pet_experience","reward_prestige","reward_rank","reward_reputation","reward_sage_mastery_experience","reward_sage_modes","reward_sage_stat_experience","reward_seichi_silver","reward_skillpoints","reward_stats","reward_taijutsu_experience","reward_titles","reward_tokens","reward_village_membership","reward_war_damage","reward_war_healing","sceneBackground","sceneCharacters","sector","structureAssetId","structureScale","successDescription","task"],["description","id","latitude","locationDescription","locationName","longitude","nextObjectiveId","overworldPlacementId","resetObjectiveId","reward_anbupoints","reward_badges","reward_bloodline_experience","reward_bloodlines","reward_bukijutsu_experience","reward_clanpoints","reward_crafting_experience","reward_exp","reward_gathering_experience","reward_gathering_items","reward_gathering_items_ids","reward_genjutsu_experience","reward_hunter_items","reward_hunter_items_ids","reward_hunting_experience","reward_items","reward_jutsus","reward_level","reward_mastery_rank","reward_mastery_stat","reward_medical_experience","reward_money","reward_ninjutsu_experience","reward_packages","reward_pet_experience","reward_prestige","reward_rank","reward_reputation","reward_sage_mastery_experience","reward_sage_modes","reward_sage_stat_experience","reward_seichi_silver","reward_skillpoints","reward_stats","reward_taijutsu_experience","reward_titles","reward_tokens","reward_village_membership","reward_war_damage","reward_war_healing","sceneBackground","sceneCharacters","sector","structureAssetId","structureScale","successDescription","task"],["description","id","latitude","locationDescription","locationName","longitude","newQuestIds","nextObjectiveId","overworldPlacementId","reward_anbupoints","reward_badges","reward_bloodline_experience","reward_bloodlines","reward_bukijutsu_experience","reward_clanpoints","reward_crafting_experience","reward_exp","reward_gathering_experience","reward_gathering_items","reward_gathering_items_ids","reward_genjutsu_experience","reward_hunter_items","reward_hunter_items_ids","reward_hunting_experience","reward_items","reward_jutsus","reward_level","reward_mastery_rank","reward_mastery_stat","reward_medical_experience","reward_money","reward_ninjutsu_experience","reward_packages","reward_pet_experience","reward_prestige","reward_rank","reward_reputation","reward_sage_mastery_experience","reward_sage_modes","reward_sage_stat_experience","reward_seichi_silver","reward_skillpoints","reward_stats","reward_taijutsu_experience","reward_titles","reward_tokens","reward_village_membership","reward_war_damage","reward_war_healing","sceneBackground","sceneCharacters","sector","structureAssetId","structureScale","successDescription","task"],["allyAIs","applyBuffs","applyDebuffs","completionOutcome","description","drawDescription","failDescription","failObjectiveId","fleeDescription","givePools","id","keepOriginalPools","latitude","locationDescription","locationName","longitude","nextObjectiveId","opponentAIs","opponent_scaled_to_user","overworldPlacementId","reward_anbupoints","reward_badges","reward_bloodline_experience","reward_bloodlines","reward_bukijutsu_experience","reward_clanpoints","reward_crafting_experience","reward_exp","reward_gathering_experience","reward_gathering_items","reward_gathering_items_ids","reward_genjutsu_experience","reward_hunter_items","reward_hunter_items_ids","reward_hunting_experience","reward_items","reward_jutsus","reward_level","reward_mastery_rank","reward_mastery_stat","reward_medical_experience","reward_money","reward_ninjutsu_experience","reward_packages","reward_pet_experience","reward_prestige","reward_rank","reward_reputation","reward_sage_mastery_experience","reward_sage_modes","reward_sage_stat_experience","reward_seichi_silver","reward_skillpoints","reward_stats","reward_taijutsu_experience","reward_titles","reward_tokens","reward_village_membership","reward_war_damage","reward_war_healing","scaleGains","sceneBackground","sceneCharacters","sector","structureAssetId","structureScale","successDescription","task"],["attackers","attackers_max_per_battle","attackers_scale_gains","attackers_scaled_to_user","completed","description","hideLocation","id","image","latitude","locationDescription","locationName","locationType","longitude","nextObjectiveId","overworldPlacementId","reward_anbupoints","reward_badges","reward_bloodline_experience","reward_bloodlines","reward_bukijutsu_experience","reward_clanpoints","reward_crafting_experience","reward_exp","reward_gathering_experience","reward_gathering_items","reward_gathering_items_ids","reward_genjutsu_experience","reward_hunter_items","reward_hunter_items_ids","reward_hunting_experience","reward_items","reward_jutsus","reward_level","reward_mastery_rank","reward_mastery_stat","reward_medical_experience","reward_money","reward_ninjutsu_experience","reward_packages","reward_pet_experience","reward_prestige","reward_rank","reward_reputation","reward_sage_mastery_experience","reward_sage_modes","reward_sage_stat_experience","reward_seichi_silver","reward_skillpoints","reward_stats","reward_taijutsu_experience","reward_titles","reward_tokens","reward_village_membership","reward_war_damage","reward_war_healing","sceneBackground","sceneCharacters","sector","sectorList","sectorType","structureAssetId","structureScale","successDescription","task"],["attackers","attackers_max_per_battle","attackers_scale_gains","attackers_scaled_to_user","collectItemIds","collect_time_minutes","completed","delete_on_complete","description","hideLocation","id","image","item_name","latitude","locationDescription","locationName","locationType","longitude","nextObjectiveId","overworldPlacementId","reward_anbupoints","reward_badges","reward_bloodline_experience","reward_bloodlines","reward_bukijutsu_experience","reward_clanpoints","reward_crafting_experience","reward_exp","reward_gathering_experience","reward_gathering_items","reward_gathering_items_ids","reward_genjutsu_experience","reward_hunter_items","reward_hunter_items_ids","reward_hunting_experience","reward_items","reward_jutsus","reward_level","reward_mastery_rank","reward_mastery_stat","reward_medical_experience","reward_money","reward_ninjutsu_experience","reward_packages","reward_pet_experience","reward_prestige","reward_rank","reward_reputation","reward_sage_mastery_experience","reward_sage_modes","reward_sage_stat_experience","reward_seichi_silver","reward_skillpoints","reward_stats","reward_taijutsu_experience","reward_titles","reward_tokens","reward_village_membership","reward_war_damage","reward_war_healing","sceneBackground","sceneCharacters","sector","sectorList","sectorType","structureAssetId","structureScale","successDescription","task"],["attackers","attackers_max_per_battle","attackers_scale_gains","attackers_scaled_to_user","completed","delete_on_complete","deliverItemIds","description","hideLocation","id","image","item_name","latitude","locationDescription","locationName","locationType","longitude","nextObjectiveId","overworldPlacementId","reward_anbupoints","reward_badges","reward_bloodline_experience","reward_bloodlines","reward_bukijutsu_experience","reward_clanpoints","reward_crafting_experience","reward_exp","reward_gathering_experience","reward_gathering_items","reward_gathering_items_ids","reward_genjutsu_experience","reward_hunter_items","reward_hunter_items_ids","reward_hunting_experience","reward_items","reward_jutsus","reward_level","reward_mastery_rank","reward_mastery_stat","reward_medical_experience","reward_money","reward_ninjutsu_experience","reward_packages","reward_pet_experience","reward_prestige","reward_rank","reward_reputation","reward_sage_mastery_experience","reward_sage_modes","reward_sage_stat_experience","reward_seichi_silver","reward_skillpoints","reward_stats","reward_taijutsu_experience","reward_titles","reward_tokens","reward_village_membership","reward_war_damage","reward_war_healing","sceneBackground","sceneCharacters","sector","sectorList","sectorType","structureAssetId","structureScale","successDescription","task"],["allyAIs","applyBuffs","applyDebuffs","attackers","attackers_max_per_battle","attackers_scale_gains","attackers_scaled_to_user","completed","completionOutcome","description","drawDescription","failDescription","failObjectiveId","fleeDescription","givePools","hideLocation","id","image","keepOriginalPools","latitude","locationDescription","locationName","locationType","longitude","nextObjectiveId","opponentAIs","opponent_scaled_to_user","overworldPlacementId","reward_anbupoints","reward_badges","reward_bloodline_experience","reward_bloodlines","reward_bukijutsu_experience","reward_clanpoints","reward_crafting_experience","reward_exp","reward_gathering_experience","reward_gathering_items","reward_gathering_items_ids","reward_genjutsu_experience","reward_hunter_items","reward_hunter_items_ids","reward_hunting_experience","reward_items","reward_jutsus","reward_level","reward_mastery_rank","reward_mastery_stat","reward_medical_experience","reward_money","reward_ninjutsu_experience","reward_packages","reward_pet_experience","reward_prestige","reward_rank","reward_reputation","reward_sage_mastery_experience","reward_sage_modes","reward_sage_stat_experience","reward_seichi_silver","reward_skillpoints","reward_stats","reward_taijutsu_experience","reward_titles","reward_tokens","reward_village_membership","reward_war_damage","reward_war_healing","scaleGains","sceneBackground","sceneCharacters","sector","sectorList","sectorType","structureAssetId","structureScale","successDescription","task"],["attackers","attackers_max_per_battle","attackers_scale_gains","attackers_scaled_to_user","description","id","image","latitude","locationDescription","locationName","longitude","nextObjectiveId","overworldPlacementId","reward_anbupoints","reward_badges","reward_bloodline_experience","reward_bloodlines","reward_bukijutsu_experience","reward_clanpoints","reward_crafting_experience","reward_exp","reward_gathering_experience","reward_gathering_items","reward_gathering_items_ids","reward_genjutsu_experience","reward_hunter_items","reward_hunter_items_ids","reward_hunting_experience","reward_items","reward_jutsus","reward_level","reward_mastery_rank","reward_mastery_stat","reward_medical_experience","reward_money","reward_ninjutsu_experience","reward_packages","reward_pet_experience","reward_prestige","reward_rank","reward_reputation","reward_sage_mastery_experience","reward_sage_modes","reward_sage_stat_experience","reward_seichi_silver","reward_skillpoints","reward_stats","reward_taijutsu_experience","reward_titles","reward_tokens","reward_village_membership","reward_war_damage","reward_war_healing","sceneBackground","sceneCharacters","sector","structureAssetId","structureScale","successDescription","task"],["applyBuffs","applyDebuffs","completionOutcome","description","drawDescription","failDescription","failObjectiveId","fleeDescription","givePools","id","image","keepOriginalPools","latitude","locationDescription","locationName","longitude","nextObjectiveId","opponentAIs","opponent_scaled_to_user","overworldPlacementId","reward_anbupoints","reward_badges","reward_bloodline_experience","reward_bloodlines","reward_bukijutsu_experience","reward_clanpoints","reward_crafting_experience","reward_exp","reward_gathering_experience","reward_gathering_items","reward_gathering_items_ids","reward_genjutsu_experience","reward_hunter_items","reward_hunter_items_ids","reward_hunting_experience","reward_items","reward_jutsus","reward_level","reward_mastery_rank","reward_mastery_stat","reward_medical_experience","reward_money","reward_ninjutsu_experience","reward_packages","reward_pet_experience","reward_prestige","reward_rank","reward_reputation","reward_sage_mastery_experience","reward_sage_modes","reward_sage_stat_experience","reward_seichi_silver","reward_skillpoints","reward_stats","reward_taijutsu_experience","reward_titles","reward_tokens","reward_village_membership","reward_war_damage","reward_war_healing","scaleGains","sceneBackground","sceneCharacters","sector","structureAssetId","structureScale","successDescription","task"],["craftItemIds","description","id","latitude","locationDescription","locationName","longitude","nextObjectiveId","overworldPlacementId","reward_anbupoints","reward_badges","reward_bloodline_experience","reward_bloodlines","reward_bukijutsu_experience","reward_clanpoints","reward_crafting_experience","reward_exp","reward_gathering_experience","reward_gathering_items","reward_gathering_items_ids","reward_genjutsu_experience","reward_hunter_items","reward_hunter_items_ids","reward_hunting_experience","reward_items","reward_jutsus","reward_level","reward_mastery_rank","reward_mastery_stat","reward_medical_experience","reward_money","reward_ninjutsu_experience","reward_packages","reward_pet_experience","reward_prestige","reward_rank","reward_reputation","reward_sage_mastery_experience","reward_sage_modes","reward_sage_stat_experience","reward_seichi_silver","reward_skillpoints","reward_stats","reward_taijutsu_experience","reward_titles","reward_tokens","reward_village_membership","reward_war_damage","reward_war_healing","sceneBackground","sceneCharacters","sector","structureAssetId","structureScale","successDescription","task","value"],["description","id","latitude","locationDescription","locationName","longitude","masteryType","nextObjectiveId","overworldPlacementId","reward_anbupoints","reward_badges","reward_bloodline_experience","reward_bloodlines","reward_bukijutsu_experience","reward_clanpoints","reward_crafting_experience","reward_exp","reward_gathering_experience","reward_gathering_items","reward_gathering_items_ids","reward_genjutsu_experience","reward_hunter_items","reward_hunter_items_ids","reward_hunting_experience","reward_items","reward_jutsus","reward_level","reward_mastery_rank","reward_mastery_stat","reward_medical_experience","reward_money","reward_ninjutsu_experience","reward_packages","reward_pet_experience","reward_prestige","reward_rank","reward_reputation","reward_sage_mastery_experience","reward_sage_modes","reward_sage_stat_experience","reward_seichi_silver","reward_skillpoints","reward_stats","reward_taijutsu_experience","reward_titles","reward_tokens","reward_village_membership","reward_war_damage","reward_war_healing","sceneBackground","sceneCharacters","sector","structureAssetId","structureScale","successDescription","task","trainJutsuIds","value"],["completeQuestIds","description","id","latitude","locationDescription","locationName","longitude","nextObjectiveId","overworldPlacementId","reward_anbupoints","reward_badges","reward_bloodline_experience","reward_bloodlines","reward_bukijutsu_experience","reward_clanpoints","reward_crafting_experience","reward_exp","reward_gathering_experience","reward_gathering_items","reward_gathering_items_ids","reward_genjutsu_experience","reward_hunter_items","reward_hunter_items_ids","reward_hunting_experience","reward_items","reward_jutsus","reward_level","reward_mastery_rank","reward_mastery_stat","reward_medical_experience","reward_money","reward_ninjutsu_experience","reward_packages","reward_pet_experience","reward_prestige","reward_rank","reward_reputation","reward_sage_mastery_experience","reward_sage_modes","reward_sage_stat_experience","reward_seichi_silver","reward_skillpoints","reward_stats","reward_taijutsu_experience","reward_titles","reward_tokens","reward_village_membership","reward_war_damage","reward_war_healing","sceneBackground","sceneCharacters","sector","structureAssetId","structureScale","successDescription","task","value"],["buyItemIds","description","id","latitude","locationDescription","locationName","longitude","nextObjectiveId","overworldPlacementId","reward_anbupoints","reward_badges","reward_bloodline_experience","reward_bloodlines","reward_bukijutsu_experience","reward_clanpoints","reward_crafting_experience","reward_exp","reward_gathering_experience","reward_gathering_items","reward_gathering_items_ids","reward_genjutsu_experience","reward_hunter_items","reward_hunter_items_ids","reward_hunting_experience","reward_items","reward_jutsus","reward_level","reward_mastery_rank","reward_mastery_stat","reward_medical_experience","reward_money","reward_ninjutsu_experience","reward_packages","reward_pet_experience","reward_prestige","reward_rank","reward_reputation","reward_sage_mastery_experience","reward_sage_modes","reward_sage_stat_experience","reward_seichi_silver","reward_skillpoints","reward_stats","reward_taijutsu_experience","reward_titles","reward_tokens","reward_village_membership","reward_war_damage","reward_war_healing","sceneBackground","sceneCharacters","sector","structureAssetId","structureScale","successDescription","task","value"],["description","id","latitude","locationDescription","locationName","longitude","nextObjectiveId","overworldPlacementId","reward_anbupoints","reward_badges","reward_bloodline_experience","reward_bloodlines","reward_bukijutsu_experience","reward_clanpoints","reward_crafting_experience","reward_exp","reward_gathering_experience","reward_gathering_items","reward_gathering_items_ids","reward_genjutsu_experience","reward_hunter_items","reward_hunter_items_ids","reward_hunting_experience","reward_items","reward_jutsus","reward_level","reward_mastery_rank","reward_mastery_stat","reward_medical_experience","reward_money","reward_ninjutsu_experience","reward_packages","reward_pet_experience","reward_prestige","reward_rank","reward_reputation","reward_sage_mastery_experience","reward_sage_modes","reward_sage_stat_experience","reward_seichi_silver","reward_skillpoints","reward_stats","reward_taijutsu_experience","reward_titles","reward_tokens","reward_village_membership","reward_war_damage","reward_war_healing","sceneBackground","sceneCharacters","sector","structureAssetId","structureScale","successDescription","task","useItemIds","value"],["combatType","description","id","latitude","locationDescription","locationName","longitude","masteryType","nextObjectiveId","overworldPlacementId","reward_anbupoints","reward_badges","reward_bloodline_experience","reward_bloodlines","reward_bukijutsu_experience","reward_clanpoints","reward_crafting_experience","reward_exp","reward_gathering_experience","reward_gathering_items","reward_gathering_items_ids","reward_genjutsu_experience","reward_hunter_items","reward_hunter_items_ids","reward_hunting_experience","reward_items","reward_jutsus","reward_level","reward_mastery_rank","reward_mastery_stat","reward_medical_experience","reward_money","reward_ninjutsu_experience","reward_packages","reward_pet_experience","reward_prestige","reward_rank","reward_reputation","reward_sage_mastery_experience","reward_sage_modes","reward_sage_stat_experience","reward_seichi_silver","reward_skillpoints","reward_stats","reward_taijutsu_experience","reward_titles","reward_tokens","reward_village_membership","reward_war_damage","reward_war_healing","sceneBackground","sceneCharacters","sector","structureAssetId","structureScale","successDescription","task","useJutsuIds","value"],["description","id","latitude","locationDescription","locationName","longitude","nextObjectiveId","overworldPlacementId","reward_anbupoints","reward_badges","reward_bloodline_experience","reward_bloodlines","reward_bukijutsu_experience","reward_clanpoints","reward_crafting_experience","reward_exp","reward_gathering_experience","reward_gathering_items","reward_gathering_items_ids","reward_genjutsu_experience","reward_hunter_items","reward_hunter_items_ids","reward_hunting_experience","reward_items","reward_jutsus","reward_level","reward_mastery_rank","reward_mastery_stat","reward_medical_experience","reward_money","reward_ninjutsu_experience","reward_packages","reward_pet_experience","reward_prestige","reward_rank","reward_reputation","reward_sage_mastery_experience","reward_sage_modes","reward_sage_stat_experience","reward_seichi_silver","reward_skillpoints","reward_stats","reward_taijutsu_experience","reward_titles","reward_tokens","reward_village_membership","reward_war_damage","reward_war_healing","sceneBackground","sceneCharacters","sector","structureAssetId","structureScale","successDescription","tagType","task","value"],["description","id","latitude","locationDescription","locationName","longitude","nextObjectiveId","overworldPlacementId","reward_anbupoints","reward_badges","reward_bloodline_experience","reward_bloodlines","reward_bukijutsu_experience","reward_clanpoints","reward_crafting_experience","reward_exp","reward_gathering_experience","reward_gathering_items","reward_gathering_items_ids","reward_genjutsu_experience","reward_hunter_items","reward_hunter_items_ids","reward_hunting_experience","reward_items","reward_jutsus","reward_level","reward_mastery_rank","reward_mastery_stat","reward_medical_experience","reward_money","reward_ninjutsu_experience","reward_packages","reward_pet_experience","reward_prestige","reward_rank","reward_reputation","reward_sage_mastery_experience","reward_sage_modes","reward_sage_stat_experience","reward_seichi_silver","reward_skillpoints","reward_stats","reward_taijutsu_experience","reward_titles","reward_tokens","reward_village_membership","reward_war_damage","reward_war_healing","sceneBackground","sceneCharacters","sector","singleBattle","structureAssetId","structureScale","successDescription","task","value"],["bloodlineRanks","description","id","latitude","locationDescription","locationName","longitude","nextObjectiveId","overworldPlacementId","reward_anbupoints","reward_badges","reward_bloodline_experience","reward_bloodlines","reward_bukijutsu_experience","reward_clanpoints","reward_crafting_experience","reward_exp","reward_gathering_experience","reward_gathering_items","reward_gathering_items_ids","reward_genjutsu_experience","reward_hunter_items","reward_hunter_items_ids","reward_hunting_experience","reward_items","reward_jutsus","reward_level","reward_mastery_rank","reward_mastery_stat","reward_medical_experience","reward_money","reward_ninjutsu_experience","reward_packages","reward_pet_experience","reward_prestige","reward_rank","reward_reputation","reward_sage_mastery_experience","reward_sage_modes","reward_sage_stat_experience","reward_seichi_silver","reward_skillpoints","reward_stats","reward_taijutsu_experience","reward_titles","reward_tokens","reward_village_membership","reward_war_damage","reward_war_healing","sceneBackground","sceneCharacters","sector","structureAssetId","structureScale","successDescription","task"],["description","type","value"],["description","target","type","value"],["description","type"],["description","effectType","threshold","type"],["description","effectType","target","threshold","type"],["description","maxRange","minRange","type"],["coordinates","description","target","type"],["coordinates","description","jutsuId","target","type"],["coordinates","description","itemId","target","type"],["coordinates","description","effect","target","type"],["comboIds","coordinates","description","target","type"],["action","conditions","group","id"],["nextObjectiveId","text"],["ids","number","quantity"],["reward_anbupoints","reward_badges","reward_bloodline_experience","reward_bloodlines","reward_bukijutsu_experience","reward_clanpoints","reward_crafting_experience","reward_exp","reward_gathering_experience","reward_gathering_items","reward_gathering_items_ids","reward_genjutsu_experience","reward_hunter_items","reward_hunter_items_ids","reward_hunting_experience","reward_items","reward_jutsus","reward_level","reward_mastery_rank","reward_mastery_stat","reward_medical_experience","reward_money","reward_ninjutsu_experience","reward_packages","reward_pet_experience","reward_prestige","reward_rank","reward_reputation","reward_sage_mastery_experience","reward_sage_modes","reward_sage_stat_experience","reward_seichi_silver","reward_skillpoints","reward_stats","reward_taijutsu_experience","reward_titles","reward_tokens","reward_village_membership","reward_war_damage","reward_war_healing"],["objectives","reward","sceneBackground","sceneCharacters","entryItems","isolated","rewardMode","rewardPickCount"],["masteryTypes","power","type"],["power","type"]],"effects":{"increaseregeneration":0,"absorb":1,"activatesagemode":0,"afterburn":2,"barrier":3,"buffprevent":0,"cleanseprevent":0,"cleanse":0,"clearprevent":0,"clear":0,"clone":0,"consume":4,"siphon":4,"copy":0,"damage":5,"debuffprevent":0,"decreaseaggro":6,"decreasecooldown":7,"decreasedamagegiven":8,"decreasedamagetaken":8,"decreaseheal":0,"decreasepotency":9,"decreasepoolcost":10,"decreasemaxpools":10,"decreasemastery":11,"decreasestat":12,"diffuse":13,"disarm":0,"drain":10,"elementaldamage":14,"elementalseal":0,"finalstand":0,"fleeprevent":0,"flee":0,"healprevent":0,"heal":10,"increaseaggro":6,"increasecooldown":7,"increasedamagegiven":8,"increasedamagetaken":8,"increaseheal":0,"increasepotency":9,"marriageslotincrease":15,"noncombatincreasereskins":15,"injectjutsus":16,"increasepoolcost":10,"increasemaxpools":10,"increaserange":7,"increasemastery":11,"increasestat":12,"immunity":17,"lifesteal":2,"mirror":0,"moveprevent":0,"move":0,"noncombatconsumereward":18,"noncombatgainskill":19,"noncombatquest":20,"repair":0,"onehitkillprevent":0,"onehitkill":0,"pierce":5,"poison":10,"recoil":2,"redirection":12,"reflect":2,"removebloodline":0,"robprevent":0,"rob":21,"rollbloodline":15,"rollsagemode":0,"sealprevent":0,"seal":0,"shield":22,"stealth":0,"stunprevent":0,"stun":23,"summonprevent":0,"summon":24,"timecompression":12,"timedilation":12,"unlockitemvariant":0,"unknown":0,"vamp":0,"visual":0,"weakness":25,"wound":2},"objectives":{"pvp_participated":26,"spars_participated":26,"ranked_wins":26,"ranked_participated":26,"overworld_ai_fought":26,"battle_pyramids_completed":26,"stories_completed":26,"events_completed":26,"overworld_quests_completed":26,"dungeons_completed":26,"raids_completed":26,"espionage":26,"sabotage":26,"siege_operation":26,"combined_mission_effort":26,"pvp_kills":26,"arena_kills":26,"minutes_passed":26,"days_as_kage":26,"errands_total":26,"a_missions_total":26,"b_missions_total":26,"c_missions_total":26,"d_missions_total":26,"a_crimes_total":26,"b_crimes_total":26,"c_crimes_total":26,"d_crimes_total":26,"minutes_training":26,"stats_trained":26,"days_in_village":26,"jutsus_mastered":26,"user_level":26,"reputation_points":26,"random_encounter_wins":26,"spars_won":26,"medical_experience":26,"medical_experience_gained":26,"crafting_experience":26,"crafting_experience_gained":26,"hunting_experience":26,"hunting_experience_gained":26,"gathering_experience":26,"gathering_experience_gained":26,"items_crafted":26,"creatures_hunted":26,"herbs_gathered":26,"seeds_planted":26,"plants_watered":26,"plants_fertilized":26,"plants_harvested":26,"farming_collection_log":26,"farming_level":26,"fail_quest":27,"win_quest":27,"reset_quest":28,"new_quest":29,"start_battle":30,"move_to_location":31,"collect_item":32,"deliver_item":33,"defeat_opponents":34,"dialog":35,"win_encounter_at_location":31,"open_raid":36,"exclusive_raid":36,"craft_specific_item":37,"train_specific_jutsu":38,"complete_specific_quest":39,"buy_item":40,"use_specific_item_combat":41,"use_specific_jutsu_combat":42,"tag_usage_win":43,"damage_dealt":44,"bloodline_collection":45},"aiConditions":{"health_below":46,"specific_round":46,"round_greater_than":46,"round_lower_than":46,"distance_higher_than":47,"distance_lower_than":47,"does_not_have_summon":48,"has_effect":49,"target_has_effect":50,"player_within_range":51,"summon_within_range":51},"aiActions":{"move_towards_opponent":52,"end_turn":48,"use_specific_jutsu":53,"use_specific_item":54,"use_random_jutsu":52,"use_random_item":52,"use_highest_power_action":55,"use_highest_power_jutsu":55,"use_highest_power_item":55,"use_combo_action":56},"aiRule":57,"objectiveChoice":58,"idsWithNumber":59,"objectiveReward":60,"questContent":61,"titleEffects":{"increasemastery":62,"increaseregeneration":63}}');

  var VERSION = "forge 0.11.0";
  function sha256(bytes, subtle = globalThis.crypto && globalThis.crypto.subtle) {
    if (!subtle || typeof subtle.digest !== "function") {
      return Promise.reject(new Error("crypto.subtle is unavailable (WebCrypto needs a secure context), so repo-backed image bytes cannot be verified"));
    }
    return subtle.digest("SHA-256", bytes);
  }
  function compose({
    storage,
    indexedDB,
    fetchImpl,
    clock = () => Date.now(),
    tabId,
    log = () => {
    },
    client = null,
    sleep,
    runtime = null,
    authState = AUTH.UNKNOWN,
    digest = sha256,
    imageProbe = null
  } = {}) {
    const deps = {};
    deps.journal = new Journal(storage, clock);
    deps.cache = new CaptureCache(indexedDB, clock);
    deps.repoCache = new RepoTextCache(indexedDB, clock);
    deps.assetCache = new AssetCache(indexedDB, clock);
    deps.digest = digest;
    deps.session = new CookieSession({ fetchImpl, origin: "" });
    deps.client = client ?? new TrpcClient(deps.session, { onExchange: (r) => log(`${r.kind} ${r.paths.join(",")} -> ${r.status ?? r.error}`) });
    deps.auth = new AuthState({ client: deps.client, runtime, clock, state: authState });
    deps.budget = new Budget({ storage, clock, ...sleep ? { sleep } : {} });
    deps.reader = new CachedReader({ client: deps.client, cache: deps.cache, budget: deps.budget });
    deps.reconciler = new Reconciler({ storage, reader: deps.reader, clock, journal: deps.journal });
    deps.github = new Github({ fetchImpl, storage });
    deps.uploader = new Uploader({ session: deps.session, fetchImpl, clock, ...sleep ? { sleep } : {} });
    deps.imageProbe = imageProbe;
    deps.validator = new Validator(fields_default, nested_default);
    deps.runner = new Runner({
      journal: deps.journal,
      client: deps.client,
      reader: deps.reader,
      cache: deps.cache,
      repoCache: deps.repoCache,
      budget: deps.budget,
      validator: deps.validator,
      uploader: deps.uploader,
      imageProbe,
      reconciler: deps.reconciler,
      auth: deps.auth,
      digest: deps.digest,
      storage,
      clock,
      tabId,
      log
    });
    return deps;
  }
  async function boot(win = window, { redirect = null, establish = true, readiness = {}, launcher = true } = {}) {
    const doc = win.document;
    if (onEntryPath(win.location)) return bootEntry(win, doc, redirect);
    if (!isArmed(win)) {
      if (launcher) offerLauncher(win, doc, { redirect, readiness });
      return null;
    }
    const app = await bootHost(win, doc, { establish, readiness });
    if (!app && launcher && !alreadyMounted(doc)) offerLauncher(win, doc, { redirect, readiness, armed: true });
    return app;
  }
  function offerLauncher(win, doc, opts) {
    (async () => {
      await whenBodyReady(doc, win);
      if (opts.armed) {
        if (!carrierReadiness(doc, win)) await whenLoaded(doc, win);
      } else if (!await whenCarrierReady(doc, win, opts.readiness)) return;
      showLauncher(win, doc, opts);
    })().catch(() => {
    });
  }
  function whenLoaded(doc, win) {
    if (doc.readyState === "complete") return Promise.resolve();
    return new Promise((resolve) => {
      try {
        win.addEventListener("load", () => resolve(), { once: true });
      } catch {
        resolve();
      }
    });
  }
  function showLauncher(win, doc, { redirect = null, armed = false } = {}) {
    if (onEntryPath(win.location) || isArmed(win) && !armed) return;
    const go = redirect ?? ((url2) => {
      win.location.assign(url2);
    });
    mountLauncher(doc, win, { onOpen: () => go(ENTRY_PATH) });
  }
  function bootEntry(win, doc, redirect) {
    const { body } = entryTakeover(doc, win);
    installCss(CSS_DOC, doc);
    installCss(CSS, doc);
    const hops = armHops(win);
    const panel = h("div", { class: "f-boot" });
    body.appendChild(panel);
    if (hops >= MAX_HOPS) {
      const failure = armFailure(win);
      disarm(win);
      panel.append(
        h("div", {}, h("b", {}, failure ? "TNR forge could not stay on the game page." : "TNR forge could not reach an authenticated page.")),
        h("p", {}, failure ? `Forge reached a normal game page but could not keep its overlay there: ${failure}` : `Forge tried ${hops} times to hand off from ${ENTRY_PATH} to a normal game page and ended up back here. Open the game, sign in, and then open ${ENTRY_PATH} again.`),
        failure ? h("p", { class: "f-mute" }, `Open the game, make sure it has finished loading, and then open ${ENTRY_PATH} again. If this repeats, the game's page structure has changed under Forge and needs a Forge update.`) : null
      );
      return null;
    }
    arm(win);
    panel.append(
      h("div", {}, h("b", {}, "TNR forge")),
      h("p", {}, "Opening the game so Forge runs inside your signed-in session\u2026"),
      h("p", { class: "f-mute" }, `${ENTRY_PATH} has no game providers, so a session cannot live here. Forge continues on ${CARRIER_PATH}.`)
    );
    const go = redirect ?? ((url2) => {
      win.location.replace(url2);
    });
    go(CARRIER_PATH);
    return null;
  }
  async function bootHost(win, doc, { establish = true, readiness = {} } = {}) {
    await whenBodyReady(doc, win);
    if (alreadyMounted(doc)) return null;
    const via = await whenCarrierReady(doc, win, readiness);
    if (!via) {
      arm(win, { hops: armHops(win), failure: `the game page never became ready to host an overlay (no framework ownership of <body> within ${Math.round(CARRIER_GRACE_MS / 1e3)}s of the page finishing loading)` });
      return null;
    }
    if (alreadyMounted(doc)) return null;
    const clock = () => Date.now();
    let tabId;
    try {
      tabId = win.sessionStorage.getItem("tnr_forge_tab") || null;
      if (!tabId) {
        tabId = Math.random().toString(36).slice(2, 12);
        win.sessionStorage.setItem("tnr_forge_tab", tabId);
      }
    } catch {
      tabId = void 0;
    }
    let deps = {};
    let host = null;
    let losses = 0;
    const log = (m) => {
      if (deps.app) deps.app.log(m);
    };
    const onLost = async () => {
      losses += 1;
      log(`host lost (${losses}): the carrier removed the Forge overlay`);
      if (losses > MAX_HOST_LOSSES) {
        arm(win, { hops: MAX_HOPS, failure: `the game page removed the Forge overlay ${losses} times after it mounted; Forge stopped rather than fight the page for it` });
        log("host lost again after a remount; giving up on this page");
        return;
      }
      try {
        const again = await whenCarrierReady(doc, win, readiness);
        if (!again) {
          arm(win, { hops: MAX_HOPS, failure: "the game page removed the Forge overlay and then never became ready for it again" });
          return;
        }
        if (alreadyMounted(doc)) return;
        host = mountHost(doc, win, { onLost });
        host.body.appendChild(deps.app.root);
        log(`host remounted after loss (carrier ready via ${again})`);
      } catch (e) {
        arm(win, { hops: MAX_HOPS, failure: `remounting the Forge overlay failed: ${e && e.message || e}` });
      }
    };
    try {
      host = mountHost(doc, win, { onLost });
      deps = compose({
        storage: win.localStorage,
        indexedDB: win.indexedDB,
        fetchImpl: win.fetch.bind(win),
        clock,
        tabId,
        runtime: pageAuthRuntime(win),
        log,
        imageProbe: browserImageProbe(win)
      });
      deps.app = new App({
        version: VERSION,
        storage: win.localStorage,
        now: clock,
        ...deps,
        exit: () => {
          disarm(win);
          host.release();
          try {
            showLauncher(win, doc);
          } catch {
          }
        }
      });
      deps.app.mount(host.body, doc);
      log(`mounted on ${win.location.pathname} (carrier ready via ${via})`);
      if (host.attached() && carrierReadiness(doc, win)) arm(win, { hops: 0, failure: null });
      else log("mounted but not stable; the hop counter is left as it was");
    } catch (e) {
      if (!host) return null;
      const panel = h("div", { class: "f-boot" });
      panel.append(h("div", {}, h("b", {}, "TNR forge failed to start")), h("pre", { style: { whiteSpace: "pre-wrap", fontSize: "12px" } }, String(e && e.stack || e)));
      host.body.appendChild(panel);
      return null;
    }
    if (establish) deps.app.establishAuth().catch((e) => deps.app.fail("auth check", e));
    return deps.app;
  }
  if (typeof window !== "undefined" && typeof document !== "undefined") {
    try {
      Promise.resolve(boot(window)).catch(() => {
      });
    } catch {
    }
  }
})();
