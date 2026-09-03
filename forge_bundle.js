// TNR forge bundle v0.1.0 - full-page content builder, loaded via @require by forge_loader_user.js.
// Built from forge/src by forge/build.mjs (esbuild, IIFE). Do not edit by hand.
// Host: any unmatched path on the game origin (/forge). Layers: storage, transport, budget, runner, reconcile, ui.
// Pinned engine facts: studie-tech/TheNinjaRPG@345d18accf6d8ea8d8d47ef0e61b5aff7d5a1cf9.
(() => {
  // src/storage/journal.mjs
  var JOURNAL_VERSION = 1;
  var KEY_PREFIX = "tnr_forge_job_v1:";
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
  var JOB_STATES = Object.freeze(["RUNNING", "PAUSED", "DONE", "ABORTED"]);
  var TRANSITIONS = Object.freeze({
    PLANNED: ["SENT", "FAILED", "SKIPPED"],
    SENT: ["CONFIRMED", "ORPHANED", "FAILED"],
    CONFIRMED: ["SENT", "VERIFIED", "FAILED"],
    // SENT again only for phase 2 of a two-phase create
    VERIFIED: [],
    FAILED: [],
    ORPHANED: ["CONFIRMED", "FAILED", "SKIPPED"],
    // CONFIRMED = adopted by the user
    SKIPPED: []
  });
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
  function newItem(idx, spec) {
    return {
      idx,
      entity: spec.entity,
      op: spec.op,
      // "create" | "update"
      name: spec.name ?? null,
      // display only
      srcId: spec.srcId ?? null,
      // manifest key for @refs
      targetId: spec.targetId ?? null,
      payloadHash: spec.payloadHash,
      state: "PLANNED",
      phase: spec.op === "create" ? "create" : "update",
      // two-phase create: "create" then "update"
      entityId: spec.targetId ?? null,
      snapshotKey: null,
      sentAt: null,
      confirmedAt: null,
      verifiedAt: null,
      error: null
    };
  }
  var Journal = class {
    /**
     * @param {Storage} storage  a localStorage-compatible object
     * @param {() => number} clock  epoch ms; injectable so tests are deterministic
     */
    constructor(storage, clock = () => Date.now()) {
      if (!storage || typeof storage.setItem !== "function") {
        throw new JournalError("Journal needs a Storage-like object");
      }
      this.storage = storage;
      this.clock = clock;
    }
    // ------------------------------------------------------------------ persistence
    _key(jobId) {
      return KEY_PREFIX + jobId;
    }
    _write(job) {
      job.v = JOURNAL_VERSION;
      job.updatedAt = nowIso(this.clock);
      const text = JSON.stringify(job);
      try {
        this.storage.setItem(this._key(job.jobId), text);
      } catch (e) {
        throw new JournalError("journal write failed: " + (e && e.message ? e.message : String(e)), {
          jobId: job.jobId,
          bytes: text.length,
          cause: e
        });
      }
      return job;
    }
    _read(jobId) {
      const text = this.storage.getItem(this._key(jobId));
      if (text == null) return null;
      let job;
      try {
        job = JSON.parse(text);
      } catch (e) {
        throw new JournalError("journal record is not JSON: " + jobId, { jobId, cause: e });
      }
      return migrate(job);
    }
    // ------------------------------------------------------------------ jobs
    listJobIds() {
      const ids = [];
      for (let i = 0; i < this.storage.length; i++) {
        const k = this.storage.key(i);
        if (k && k.startsWith(KEY_PREFIX)) ids.push(k.slice(KEY_PREFIX.length));
      }
      return ids;
    }
    listJobs() {
      return this.listJobIds().map((id) => this._read(id)).filter(Boolean).sort((a, b) => a.startedAt < b.startedAt ? 1 : -1);
    }
    get(jobId) {
      return this._read(jobId);
    }
    /**
     * Open a new job. items are specs: {entity, op, name, srcId, targetId, payloadHash}.
     */
    open({ jobId, manifestPath, manifestNumber: manifestNumber2, manifestHash, items }) {
      if (!jobId) throw new JournalError("jobId required");
      if (this._read(jobId)) throw new JournalError("job already exists: " + jobId, { jobId });
      const job = {
        v: JOURNAL_VERSION,
        jobId,
        manifestPath: manifestPath ?? null,
        manifestNumber: manifestNumber2 ?? null,
        manifestHash: manifestHash ?? null,
        startedAt: nowIso(this.clock),
        updatedAt: null,
        state: "RUNNING",
        pause: null,
        // { reason, path, until } when PAUSED
        items: items.map((spec, i) => newItem(i, spec))
      };
      return this._write(job);
    }
    setJobState(jobId, state, extra = {}) {
      if (!JOB_STATES.includes(state)) throw new JournalError("bad job state: " + state);
      const job = this._mustRead(jobId);
      job.state = state;
      job.pause = state === "PAUSED" ? extra.pause ?? job.pause ?? null : null;
      return this._write(job);
    }
    remove(jobId) {
      this.storage.removeItem(this._key(jobId));
    }
    _mustRead(jobId) {
      const job = this._read(jobId);
      if (!job) throw new JournalError("no such job: " + jobId, { jobId });
      return job;
    }
    // ------------------------------------------------------------------ items
    /**
     * Transition one item. Validates against TRANSITIONS, applies patch, flushes synchronously.
     * Returns the updated job. Throws JournalError on an illegal transition.
     */
    transition(jobId, idx, to, patch = {}) {
      const job = this._mustRead(jobId);
      const item = job.items[idx];
      if (!item) throw new JournalError("no such item: " + idx, { jobId, idx });
      const from = item.state;
      if (!TRANSITIONS[from] || !TRANSITIONS[from].includes(to)) {
        throw new JournalError(`illegal transition ${from} -> ${to}`, { jobId, idx, from, to });
      }
      Object.assign(item, patch);
      item.state = to;
      const at = nowIso(this.clock);
      if (to === "SENT") item.sentAt = at;
      if (to === "CONFIRMED") item.confirmedAt = at;
      if (to === "VERIFIED") item.verifiedAt = at;
      return this._write(job);
    }
    /**
     * The write-ahead primitive. Flush SENT to disk, THEN run the thunk that issues the request.
     * The thunk cannot run before the flush because it is only invoked after _write returns.
     * If the flush throws, the thunk never runs and nothing left the device.
     *
     * @returns {Promise<any>} whatever the thunk resolves to
     */
    async withSent(jobId, idx, patch, thunk) {
      if (typeof patch === "function") {
        thunk = patch;
        patch = {};
      }
      this.transition(jobId, idx, "SENT", patch);
      return await thunk();
    }
    /** Set a field on an item without a state change. Still flushes. */
    annotate(jobId, idx, patch) {
      const job = this._mustRead(jobId);
      const item = job.items[idx];
      if (!item) throw new JournalError("no such item: " + idx, { jobId, idx });
      Object.assign(item, patch);
      return this._write(job);
    }
    // ------------------------------------------------------------------ resume
    /** Jobs that have any item not in a terminal state, or that are PAUSED. */
    resumable() {
      return this.listJobs().filter((job) => job.state === "PAUSED" || job.items.some((it) => !TERMINAL_ITEM_STATES.includes(it.state)));
    }
    /** Items in SENT. These are ambiguous and must go through reconciliation, never retried. */
    ambiguous(jobId) {
      return this._mustRead(jobId).items.filter((it) => it.state === "SENT");
    }
    // ------------------------------------------------------------------ export
    exportText() {
      return JSON.stringify({ exportedAt: nowIso(this.clock), version: JOURNAL_VERSION, jobs: this.listJobs() }, null, 1);
    }
  };
  var MIGRATIONS = {};
  function migrate(job) {
    let v = job.v ?? 1;
    while (v < JOURNAL_VERSION) {
      const step = MIGRATIONS[v];
      if (!step) throw new JournalError("no migration from journal v" + v);
      job = step(job);
      v = job.v;
    }
    return job;
  }

  // src/storage/captures.mjs
  var DB_NAME = "tnr_forge";
  var STORE = "captures";
  var DB_VERSION = 1;
  function captureKey(path, id) {
    return `${path}:${id ?? ""}`;
  }
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
    /**
     * @param {IDBFactory} idb  window.indexedDB or fake-indexeddb
     * @param {() => number} clock
     */
    constructor(idb, clock = () => Date.now()) {
      if (!idb || typeof idb.open !== "function") throw new Error("CaptureCache needs an IDBFactory");
      this.idb = idb;
      this.clock = clock;
      this._db = null;
    }
    async _open() {
      if (this._db) return this._db;
      const req = this.idb.open(DB_NAME, DB_VERSION);
      req.onupgradeneeded = () => {
        const db = req.result;
        if (!db.objectStoreNames.contains(STORE)) {
          const store = db.createObjectStore(STORE, { keyPath: "key" });
          store.createIndex("entity", "entity", { unique: false });
          store.createIndex("path", "path", { unique: false });
        }
      };
      this._db = await reqToPromise(req);
      this._db.onversionchange = () => {
        this._db.close();
        this._db = null;
      };
      return this._db;
    }
    async _tx(mode, fn) {
      const db = await this._open();
      const tx = db.transaction(STORE, mode);
      const store = tx.objectStore(STORE);
      const result = await fn(store);
      await new Promise((resolve, reject) => {
        tx.oncomplete = () => resolve();
        tx.onerror = () => reject(tx.error);
        tx.onabort = () => reject(tx.error);
      });
      return result;
    }
    /** Store a decoded response. */
    async put({ path, id, input, data }) {
      const rec = {
        key: captureKey(path, id),
        path,
        id: id ?? null,
        entity: entityOfPath(path),
        input: input ?? null,
        data,
        at: new Date(this.clock()).toISOString(),
        bytes: JSON.stringify(data ?? null).length
      };
      await this._tx("readwrite", (s) => reqToPromise(s.put(rec)));
      return rec;
    }
    async get(path, id) {
      const rec = await this._tx("readonly", (s) => reqToPromise(s.get(captureKey(path, id))));
      return rec ?? null;
    }
    async has(path, id) {
      return await this.get(path, id) != null;
    }
    async delete(path, id) {
      await this._tx("readwrite", (s) => reqToPromise(s.delete(captureKey(path, id))));
    }
    /** Drop every capture belonging to an entity type (all paths, all ids). */
    async invalidateEntity(entity) {
      return this._tx("readwrite", async (s) => {
        const idx = s.index("entity");
        const keys = await reqToPromise(idx.getAllKeys(entity));
        for (const k of keys) await reqToPromise(s.delete(k));
        return keys.length;
      });
    }
    /**
     * Drop captures affected by a write to one record: that record's own gets on every path,
     * plus every list capture for the entity (getAll, getAllNames), since lists carry names.
     */
    async invalidateRecord(entity, id) {
      return this._tx("readwrite", async (s) => {
        const idx = s.index("entity");
        const recs = await reqToPromise(idx.getAll(entity));
        let n = 0;
        for (const r of recs) {
          if (r.id === id || r.id === null || r.id === "") {
            await reqToPromise(s.delete(r.key));
            n++;
          }
        }
        return n;
      });
    }
    async list() {
      const recs = await this._tx("readonly", (s) => reqToPromise(s.getAll()));
      return recs.map(({ key, path, id, entity, at, bytes }) => ({ key, path, id, entity, at, bytes }));
    }
    async size() {
      const recs = await this.list();
      return { count: recs.length, bytes: recs.reduce((a, r) => a + (r.bytes || 0), 0) };
    }
    async clear() {
      await this._tx("readwrite", (s) => reqToPromise(s.clear()));
    }
    close() {
      if (this._db) {
        this._db.close();
        this._db = null;
      }
    }
  };

  // src/transport/session.mjs
  var Session = class {
    /** @returns {Promise<Response>} */
    async fetch(_url, _init) {
      throw new Error("Session.fetch not implemented");
    }
    /** Human-readable, for the Settings screen. Must never include a secret. */
    describe() {
      return { kind: "abstract" };
    }
  };
  var CookieSession = class extends Session {
    /**
     * @param {object} opts
     * @param {(url: string, init: object) => Promise<Response>} opts.fetchImpl  the page's fetch
     * @param {string} [opts.origin]  "" for same-origin relative URLs (the userscript case)
     */
    constructor({ fetchImpl, origin = "" } = {}) {
      super();
      if (typeof fetchImpl !== "function") throw new Error("CookieSession needs fetchImpl");
      this.fetchImpl = fetchImpl;
      this.origin = origin;
    }
    async fetch(url, init = {}) {
      const headers = new Headers(init.headers ?? {});
      if (headers.has("authorization")) {
        throw new Error("CookieSession refuses an Authorization header on a game request");
      }
      return this.fetchImpl(this.origin + url, { ...init, headers, credentials: "same-origin" });
    }
    describe() {
      return { kind: "cookie", origin: this.origin || "(same-origin)" };
    }
  };

  // node_modules/superjson/dist/double-indexed-kv.js
  var DoubleIndexedKV = class {
    constructor() {
      this.keyToValue = /* @__PURE__ */ new Map();
      this.valueToKey = /* @__PURE__ */ new Map();
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

  // node_modules/superjson/dist/registry.js
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

  // node_modules/superjson/dist/class-registry.js
  var ClassRegistry = class extends Registry {
    constructor() {
      super((c) => c.name);
      this.classToAllowedProps = /* @__PURE__ */ new Map();
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

  // node_modules/superjson/dist/util.js
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

  // node_modules/superjson/dist/custom-transformer-registry.js
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

  // node_modules/superjson/dist/is.js
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

  // node_modules/superjson/dist/pathstringifier.js
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

  // node_modules/superjson/dist/transformer.js
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
      // (sets only exist in es6+)
      // eslint-disable-next-line es5/no-es6-methods
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
  ].reduce((obj, ctor) => {
    obj[ctor.name] = ctor;
    return obj;
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

  // node_modules/superjson/dist/accessDeep.js
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
  var getDeep = (object, path) => {
    validatePath(path);
    for (let i = 0; i < path.length; i++) {
      const key = path[i];
      if (isSet(object)) {
        object = getNthKey(object, +key);
      } else if (isMap(object)) {
        const row = +key;
        const type = +path[++i] === 0 ? "key" : "value";
        const keyOfRow = getNthKey(object, row);
        switch (type) {
          case "key":
            object = keyOfRow;
            break;
          case "value":
            object = object.get(keyOfRow);
            break;
        }
      } else {
        object = object[key];
      }
    }
    return object;
  };
  var setDeep = (object, path, mapper) => {
    validatePath(path);
    if (path.length === 0) {
      return mapper(object);
    }
    let parent = object;
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
    return object;
  };

  // node_modules/superjson/dist/plainer.js
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
      const object = getDeep(plain, parsePath(path, legacyPaths));
      identicalPaths.map((path2) => parsePath(path2, legacyPaths)).forEach((identicalObjectPath) => {
        plain = setDeep(plain, identicalObjectPath, () => object);
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
  var isDeep = (object, superJson) => isPlainObject(object) || isArray(object) || isMap(object) || isSet(object) || isError(object) || isInstanceOfRegisteredClass(object, superJson);
  function addIdentity(object, path, identities) {
    const existingSet = identities.get(object);
    if (existingSet) {
      existingSet.push(path);
    } else {
      identities.set(object, [path]);
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
  var walker = (object, identities, superJson, dedupe, path = [], objectsInThisPath = [], seenObjects = /* @__PURE__ */ new Map()) => {
    const primitive = isPrimitive(object);
    if (!primitive) {
      addIdentity(object, path, identities);
      const seen = seenObjects.get(object);
      if (seen) {
        return dedupe ? {
          transformedValue: null
        } : seen;
      }
    }
    if (!isDeep(object, superJson)) {
      const transformed2 = transformValue(object, superJson);
      const result2 = transformed2 ? {
        transformedValue: transformed2.value,
        annotations: [transformed2.type]
      } : {
        transformedValue: object
      };
      if (!primitive) {
        seenObjects.set(object, result2);
      }
      return result2;
    }
    if (includes(objectsInThisPath, object)) {
      return {
        transformedValue: null
      };
    }
    const transformationResult = transformValue(object, superJson);
    const transformed = transformationResult?.value ?? object;
    const transformedValue = isArray(transformed) ? [] : {};
    const innerAnnotations = {};
    forEach(transformed, (value, index) => {
      if (index === "__proto__" || index === "constructor" || index === "prototype") {
        throw new Error(`Detected property ${index}. This is a prototype pollution risk, please remove it from your object.`);
      }
      const recursiveResult = walker(value, identities, superJson, dedupe, [...path, index], [...objectsInThisPath, object], seenObjects);
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
      seenObjects.set(object, result);
    }
    return result;
  };

  // node_modules/copy-anything/dist/index.js
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
    const clones = /* @__PURE__ */ new Map();
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

  // node_modules/superjson/dist/index.js
  var SuperJSON = class {
    /**
     * @param dedupeReferentialEqualities  If true, SuperJSON will make sure only one instance of referentially equal objects are serialized and the rest are replaced with `null`.
     */
    constructor({ dedupe = false } = {}) {
      this.classRegistry = new ClassRegistry();
      this.symbolRegistry = new Registry((s) => s.description ?? "");
      this.customTransformerRegistry = new CustomTransformerRegistry();
      this.allowedErrorProps = [];
      this.dedupe = dedupe;
    }
    serialize(object) {
      const identities = /* @__PURE__ */ new Map();
      const output = walker(object, identities, this, this.dedupe);
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
    stringify(object) {
      return JSON.stringify(this.serialize(object));
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

  // src/transport/envelope.mjs
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
  function decodeResponse(status, text, expectedCount) {
    let body;
    try {
      body = JSON.parse(text);
    } catch (e) {
      throw new TransportError("response is not JSON", { httpStatus: status, snippet: String(text).slice(0, 200) });
    }
    if (!Array.isArray(body)) {
      throw new TransportError("response is not a batch array", { httpStatus: status, snippet: String(text).slice(0, 200) });
    }
    if (expectedCount != null && body.length !== expectedCount) {
      throw new TransportError(`batch length mismatch: expected ${expectedCount}, got ${body.length}`, { httpStatus: status });
    }
    return body.map((el, i) => decodeElement(el, i, status));
  }
  function decodeElement(el, i, status) {
    if (el && el.result && el.result.data !== void 0) {
      const { json, meta } = el.result.data;
      return { ok: true, data: dist_default.deserialize({ json, meta }) };
    }
    if (el && el.error) {
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

  // src/transport/procedures.mjs
  var PROCEDURES = Object.freeze({
    "ai.createAiProfile": { kind: "mutation", limited: false, mcp: false },
    "ai.getAiProfile": { kind: "query", limited: false, mcp: true },
    "ai.toggleAiProfile": { kind: "mutation", limited: false, mcp: false },
    "ai.updateAiProfile": { kind: "mutation", limited: false, mcp: false },
    "bloodline.create": { kind: "mutation", limited: false, mcp: false },
    "bloodline.delete": { kind: "mutation", limited: false, mcp: false },
    "bloodline.get": { kind: "query", limited: true, mcp: true },
    "bloodline.getAll": { kind: "query", limited: true, mcp: true },
    "bloodline.getAllNames": { kind: "query", limited: true, mcp: true },
    "bloodline.update": { kind: "mutation", limited: false, mcp: false },
    "gameAsset.create": { kind: "mutation", limited: false, mcp: false },
    "gameAsset.delete": { kind: "mutation", limited: false, mcp: false },
    "gameAsset.get": { kind: "query", limited: true, mcp: true },
    "gameAsset.getAll": { kind: "query", limited: true, mcp: true },
    "gameAsset.getAllNames": { kind: "query", limited: true, mcp: true },
    "gameAsset.update": { kind: "mutation", limited: false, mcp: false },
    "item.clone": { kind: "mutation", limited: false, mcp: false },
    "item.create": { kind: "mutation", limited: false, mcp: false },
    "item.delete": { kind: "mutation", limited: false, mcp: false },
    "item.get": { kind: "query", limited: true, mcp: true },
    "item.getAll": { kind: "query", limited: true, mcp: true },
    "item.getAllNames": { kind: "query", limited: true, mcp: true },
    "item.update": { kind: "mutation", limited: false, mcp: false },
    "jutsu.create": { kind: "mutation", limited: false, mcp: false },
    "jutsu.delete": { kind: "mutation", limited: false, mcp: false },
    "jutsu.get": { kind: "query", limited: true, mcp: true },
    "jutsu.getAll": { kind: "query", limited: true, mcp: true },
    "jutsu.getAllNames": { kind: "query", limited: true, mcp: true },
    "jutsu.update": { kind: "mutation", limited: false, mcp: false },
    "profile.cloneAi": { kind: "mutation", limited: false, mcp: false },
    "profile.create": { kind: "mutation", limited: false, mcp: true },
    "profile.delete": { kind: "mutation", limited: false, mcp: true },
    "profile.getAi": { kind: "query", limited: false, mcp: true },
    "profile.getAllAiNames": { kind: "query", limited: true, mcp: true },
    "profile.updateAi": { kind: "mutation", limited: false, mcp: true },
    "quests.checkRewards": { kind: "mutation", limited: false, mcp: true },
    "quests.clone": { kind: "mutation", limited: false, mcp: true },
    "quests.create": { kind: "mutation", limited: false, mcp: true },
    "quests.delete": { kind: "mutation", limited: false, mcp: true },
    "quests.get": { kind: "query", limited: true, mcp: true },
    "quests.getAll": { kind: "query", limited: true, mcp: true },
    "quests.getAllNames": { kind: "query", limited: true, mcp: true },
    "quests.update": { kind: "mutation", limited: false, mcp: true }
  });
  function procedure(path) {
    const p = PROCEDURES[path];
    if (!p) throw new Error("unknown procedure: " + path + " (not in the audited crud surface)");
    return p;
  }
  var LIMITED_PATHS = Object.freeze(Object.keys(PROCEDURES).filter((p) => PROCEDURES[p].limited));
  var MUTATION_PATHS = Object.freeze(Object.keys(PROCEDURES).filter((p) => PROCEDURES[p].kind === "mutation"));

  // src/transport/client.mjs
  var NetworkError = class extends Error {
    constructor(cause, info = {}) {
      super("network: " + (cause && cause.message ? cause.message : String(cause)));
      this.name = "NetworkError";
      this.cause = cause;
      Object.assign(this, info);
    }
  };
  var TrpcClient = class {
    /**
     * @param {Session} session
     * @param {object} [opts]
     * @param {number} [opts.maxBatch=20]   items per HTTP request. The route handler has
     *   maxDuration = 90 s per request; batching shares one request scope server-side, but every
     *   procedure still pays its own limiter token, so batching is for latency, not budget.
     * @param {number} [opts.maxUrlLength=8000]  GET batches longer than this are split.
     * @param {(rec: object) => void} [opts.onExchange]  observer for the UI/journal (no secrets).
     */
    constructor(session, { maxBatch = 20, maxUrlLength = 8e3, onExchange = null, endpoint } = {}) {
      if (!(session instanceof Session)) throw new TransportError("TrpcClient needs a Session");
      this.session = session;
      this.maxBatch = maxBatch;
      this.maxUrlLength = maxUrlLength;
      this.onExchange = onExchange;
      this.endpoint = endpoint;
    }
    /** One call. Resolves to a decoded element {ok, data} | {ok:false, error}; rejects NetworkError. */
    async call(path, input) {
      const [r] = await this.batch([{ path, input }]);
      return r;
    }
    /**
     * Many calls. All must be the same kind (the adapter cannot mix GET and POST in one request).
     * Returns decoded elements in input order. Splits by maxBatch and by URL length.
     */
    async batch(calls) {
      if (!calls.length) return [];
      const kinds = new Set(calls.map((c) => procedure(c.path).kind));
      if (kinds.size !== 1) throw new TransportError("a batch must be all queries or all mutations");
      const kind = [...kinds][0];
      const out = new Array(calls.length);
      for (const chunk of this._chunks(calls, kind)) {
        const results = await this._send(chunk.map((c) => c.call), kind);
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
      let res, text;
      try {
        res = await this.session.fetch(req.url, { method: req.method, headers: req.headers, body: req.body });
        text = await res.text();
      } catch (e) {
        this._observe({ kind, paths: calls.map((c) => c.path), status: null, error: String(e && e.message) });
        throw new NetworkError(e, { paths: calls.map((c) => c.path), kind });
      }
      const decoded = decodeResponse(res.status, text, calls.length);
      this._observe({
        kind,
        paths: calls.map((c) => c.path),
        status: res.status,
        outcomes: decoded.map((d) => d.ok ? "ok" : d.error.code)
      });
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

  // src/transport/upload.mjs
  var UT_VERSION = "7.7.4";
  var SLUGS = Object.freeze({
    imageUploader: { mime: "image", maxBytes: 512 * 1024 },
    // core.ts:89
    conceptArtFrameUploader: { mime: "image", maxBytes: 256 * 1024 },
    // core.ts:95
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
  var Uploader = class {
    /**
     * @param {object} o
     * @param {import("./session.mjs").Session} o.session  same-origin, for the presign call
     * @param {(url: string, init: object) => Promise<Response>} o.fetchImpl  plain fetch for the ingest host
     * @param {string} [o.slug="imageUploader"]
     */
    constructor({ session, fetchImpl, slug = "imageUploader" }) {
      if (!SLUGS[slug]) throw new UploadError("unknown slug " + slug);
      this.session = session;
      this.fetchImpl = fetchImpl;
      this.slug = slug;
    }
    ceiling() {
      return SLUGS[this.slug].maxBytes;
    }
    /** @param {File|Blob & {name?: string, lastModified?: number}} file  @returns {Promise<{ufsUrl: string, key: string}>} */
    async upload(file) {
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
      return { ufsUrl: done.ufsUrl, key: p.key, fileHash: done.fileHash ?? null };
    }
  };

  // src/budget/bucket.mjs
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
      return arr.filter((t) => now - t < windowMs);
    }
    /** Timestamps in the window for a path, oldest first. */
    inWindow(path, windowMs) {
      const now = this.clock();
      return this._prune(this._load()[path] || [], windowMs, now).sort((a, b) => a - b);
    }
    /** Append n sends for path, prune, flush synchronously. Returns the count in window after. */
    record(path, n, windowMs) {
      const now = this.clock();
      const log = this._load();
      const arr = this._prune(log[path] || [], windowMs, now);
      for (let i = 0; i < n; i++) arr.push(now);
      log[path] = arr;
      this._save(log);
      return arr.length;
    }
    /** Persisted trip marker so a restart within the window still shows the countdown. */
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
    /**
     * @param {object} o
     * @param {Storage} o.storage
     * @param {() => number} [o.clock]
     * @param {(ms: number) => Promise<void>} [o.sleep]
     * @param {number} [o.margin]  fraction of the server limit to allow locally (0 < margin <= 1)
     * @param {string[]} [o.limitedPaths]
     */
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
    /** How many more sends on path fit right now without waiting. */
    available(path) {
      if (!this.isLimited(path)) return Infinity;
      return Math.max(0, this.allowance - this.log.inWindow(path, this.windowMs).length);
    }
    /**
     * Acquire n tokens for path. Waits (never fails) until the local window has room, then records
     * the sends WRITE-AHEAD and resolves. Unlimited paths resolve immediately and record nothing.
     * A persisted trip (server 429 within the window) refuses with RateLimited: the caller must
     * not send at all until `until`.
     */
    async acquire(path, n = 1) {
      if (!this.isLimited(path)) return;
      if (n > this.allowance) throw new Error(`cannot acquire ${n} > allowance ${this.allowance} on ${path}; chunk smaller`);
      const t = this.log.tripped();
      if (t) throw new RateLimited({ path: t.path, until: t.until, message: `limiter tripped on ${t.path}; wait until ${new Date(t.until).toISOString()}` });
      for (; ; ) {
        const inWin = this.log.inWindow(path, this.windowMs);
        if (inWin.length + n <= this.allowance) break;
        const need = inWin.length + n - this.allowance;
        const wakeAt = inWin[need - 1] + this.windowMs;
        this.waits++;
        await this.sleep(Math.max(1, wakeAt - this.clock()));
      }
      this.log.record(path, n, this.windowMs);
    }
    /**
     * Inspect decoded batch results. If ANY index is TOO_MANY_REQUESTS, persist the trip and
     * throw RateLimited for that index. Never retries. Call this AFTER caching any ok results,
     * so the successful indices are not wasted.
     */
    observe(results, paths) {
      for (let i = 0; i < results.length; i++) {
        const r = results[i];
        if (r && r.ok === false && r.error && r.error.code === "TOO_MANY_REQUESTS") {
          const path = r.error.path || paths[i];
          const until = this.clock() + this.windowMs;
          this.log.trip(path, until);
          throw new RateLimited({ path, until, index: i, message: r.error.message });
        }
      }
    }
    /** Live view for the Run screen. */
    status() {
      const now = this.clock();
      const out = {};
      for (const path of this.limited) {
        const inWin = this.log.inWindow(path, this.windowMs);
        out[path] = {
          used: inWin.length,
          allowance: this.allowance,
          serverLimit: this.limit,
          resetInMs: inWin.length ? Math.max(0, inWin[0] + this.windowMs - now) : 0
        };
      }
      return { paths: out, tripped: this.log.tripped(), waits: this.waits, margin: this.margin };
    }
  };

  // src/budget/reader.mjs
  var INPUT_FOR = Object.freeze({
    "profile.getAi": (id) => ({ userId: id })
  });
  function readInput(path, id) {
    const f = INPUT_FOR[path];
    return f ? f(id) : { id };
  }
  var CachedReader = class {
    constructor({ client, cache, budget, maxBatch = 20 }) {
      this.client = client;
      this.cache = cache;
      this.budget = budget;
      this.maxBatch = maxBatch;
      this.stats = { hits: 0, misses: 0, requests: 0 };
    }
    /** One record, cache-first. Returns the decoded element {ok, data|error}. */
    async get(path, id, { fresh = false } = {}) {
      const [r] = await this.getMany(path, [id], { fresh });
      return r;
    }
    /**
     * Many records of one path, cache-first, batched under the budget. Returns decoded elements
     * in id order. Throws RateLimited if the server trips (after caching whatever succeeded).
     */
    async getMany(path, ids, { fresh = false } = {}) {
      if (procedure(path).kind !== "query") throw new Error("getMany is for queries: " + path);
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
        const room = Math.min(this.maxBatch, this.budget.isLimited(path) ? this.budget.allowance : this.maxBatch);
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
    /** A list procedure (getAll / getAllNames / getAllAiNames): cached under id "". */
    async list(path, { fresh = false } = {}) {
      if (procedure(path).kind !== "query") throw new Error("list is for queries: " + path);
      const hit = fresh ? null : await this.cache.get(path, "");
      if (hit) {
        this.stats.hits++;
        return { ok: true, data: hit.data, cached: true, at: hit.at };
      }
      this.stats.misses++;
      await this.budget.acquire(path, 1);
      this.stats.requests++;
      const [r] = await this.client.batch([{ path, input: void 0 }]);
      if (r.ok) await this.cache.put({ path, id: "", input: null, data: r.data });
      this.budget.observe([r], [path]);
      return r;
    }
  };

  // src/runner/validate.mjs
  var AI_EXTRA_KEYS = Object.freeze(["jutsus", "items", "primaryElement", "secondaryElement", "rules", "includeDefaultRules"]);
  var SERVER_OWNED = Object.freeze(["id", "userId", "createdAt", "updatedAt", "aiProfileId"]);
  var SCHEMA_ENTITY = Object.freeze({ jutsu: "jutsu", item: "item", bloodline: "bloodline", quest: "quest", asset: "gameAsset" });
  var Validator = class {
    /** @param {object} schemas  the parsed 45d file ({entities: {name: {fields: {...}}}}) or null */
    constructor(schemas) {
      this.fields = {};
      const ents = schemas && schemas.entities ? schemas.entities : {};
      for (const [name, e] of Object.entries(ents)) {
        if (e && e.fields && typeof e.fields === "object") this.fields[name] = new Set(Object.keys(e.fields));
      }
      this.schemaMissing = Object.keys(this.fields).length === 0;
    }
    knownFields(entity) {
      const s = SCHEMA_ENTITY[entity];
      return s ? this.fields[s] ?? null : null;
    }
    /**
     * Validate the ASSERTED keys of one item's data before merge and send.
     * @param {string} entity   manifest entity
     * @param {object} data     the manifest's data (refs already resolved)
     * @param {object|null} live  the live record when known (required for ai)
     * @returns {string[]} problems (empty = ok)
     */
    problems(entity, data, live = null) {
      const out = [];
      if (!data || typeof data !== "object") return ["data is not an object"];
      const keys = Object.keys(data);
      if (entity === "ai" || entity === "aiProfile") {
        const allowed = new Set(AI_EXTRA_KEYS);
        if (live) for (const k of Object.keys(live)) allowed.add(k);
        const check = entity === "aiProfile" ? /* @__PURE__ */ new Set(["rules", "includeDefaultRules"]) : allowed;
        for (const k of keys) if (!check.has(k)) out.push(`unknown key "${k}" for ${entity}${live ? "" : " (no live record to check against)"}`);
        if (Array.isArray(data.rules)) out.push(...ruleProblems(data.rules));
      } else {
        const known = this.knownFields(entity);
        if (!known) out.push(`no field schema for entity ${entity}`);
        else for (const k of keys) if (!known.has(k) && !SERVER_OWNED.includes(k)) out.push(`unknown key "${k}" for ${entity} (would be silently dropped by the server)`);
      }
      if (data.image === "") out.push("image is an empty string: omit the key so fetch-merge keeps the current value");
      for (const [k, v] of Object.entries(data)) if (typeof v === "string" && /^@\w+:@\w+:/.test(v)) out.push(`${k}: doubled ref prefix`);
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
  function diffAsserted(entity, asserted, live) {
    const diffs = [];
    for (const k of Object.keys(asserted)) {
      if (SERVER_OWNED.includes(k)) continue;
      if (entity === "ai" && ["rules", "includeDefaultRules", "jutsus", "items"].includes(k)) continue;
      const s = asserted[k], l = live ? live[k] : void 0;
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

  // src/transport/outcome.mjs
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
    if (!decoded.ok) return { kind: "error", message: decoded.error.message, error: decoded.error };
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
    if (code === "NOT_FOUND") return "NOT_FOUND";
    return "SERVER";
  }

  // src/storage/compat.mjs
  var IDMAP_KEY = "tnr_bk_idmap_v1";
  var GH_KEY = "tnr_bk_gh_v1";
  function readJson(storage, key, fallback) {
    try {
      return JSON.parse(storage.getItem(key) || "null") ?? fallback;
    } catch {
      return fallback;
    }
  }
  function readIdmap(storage) {
    return readJson(storage, IDMAP_KEY, {});
  }
  function writeIdmap(storage, idmap) {
    storage.setItem(IDMAP_KEY, JSON.stringify(idmap));
  }
  function readGh(storage) {
    return readJson(storage, GH_KEY, {});
  }
  function writeGh(storage, gh) {
    storage.setItem(GH_KEY, JSON.stringify(gh));
  }

  // src/runner/recipes.mjs
  var RECIPES = Object.freeze({
    jutsu: {
      create: { path: "jutsu.create", input: () => void 0 },
      // jutsu.ts:391
      get: "jutsu.get",
      update: "jutsu.update",
      names: "jutsu.getAllNames",
      idKey: "id",
      nameKey: "name",
      placeholder: (id) => `New Jutsu - ${id}`,
      cacheEntity: "jutsu"
    },
    item: {
      create: { path: "item.create", input: (d) => ({ type: d.itemType ?? "CONSUMABLE" }) },
      // item.ts:235-236
      get: "item.get",
      update: "item.update",
      names: "item.getAllNames",
      idKey: "id",
      nameKey: "name",
      placeholder: (id) => `New Item - ${id}`,
      cacheEntity: "item"
    },
    bloodline: {
      create: { path: "bloodline.create", input: () => void 0 },
      // bloodline.ts:144
      get: "bloodline.get",
      update: "bloodline.update",
      names: "bloodline.getAllNames",
      idKey: "id",
      nameKey: "name",
      placeholder: (id) => `New Bloodline - ${id}`,
      cacheEntity: "bloodline"
    },
    asset: {
      create: { path: "gameAsset.create", input: () => void 0 },
      // asset.ts:194
      get: "gameAsset.get",
      update: "gameAsset.update",
      names: "gameAsset.getAllNames",
      idKey: "id",
      nameKey: "name",
      placeholder: () => "Placeholder",
      cacheEntity: "asset",
      placeholderIsAnonymous: true
      // every orphan is named "Placeholder": the snapshot diff is the only signal
    },
    quest: {
      create: { path: "quests.create", input: () => void 0 },
      // quests.ts:866
      get: "quests.get",
      update: "quests.update",
      names: "quests.getAllNames",
      idKey: "id",
      nameKey: "name",
      placeholder: (id) => `New Quest - ${id}`,
      cacheEntity: "quest"
    },
    ai: {
      create: { path: "profile.create", input: () => void 0 },
      // profile.ts:1138
      get: "profile.getAi",
      update: "profile.updateAi",
      names: "profile.getAllAiNames",
      idKey: "userId",
      nameKey: "username",
      placeholder: (id) => `New AI - ${id}`,
      cacheEntity: "ai"
    },
    aiProfile: {
      // update-only. targetId is the AI's userId. Rules live on a separate row reached through
      // profile.getAi().aiProfileId; ai.toggleAiProfile {aiId} creates that row when missing.
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
  function recipe(entity) {
    const r = RECIPES[entity];
    if (!r) throw new Error("no recipe for entity " + entity);
    return r;
  }
  function mergeForUpdate(entity, live, data, fields) {
    if (entity === "ai") return mergeAi(live, data);
    const src = { ...live ?? {}, ...data };
    if (!fields) return src;
    const out = {};
    for (const k of fields) if (src[k] !== void 0) out[k] = src[k];
    return out;
  }
  var AI_OMIT = /* @__PURE__ */ new Set([
    // omitted from insertAiSchema at schema.ts:2578-2591
    "trainingStartedAt",
    "occupationSignupAt",
    "currentlyTraining",
    "deletionAt",
    "travelFinishAt",
    "questData",
    "occupation",
    "stealthActivatedAt",
    "stealthCooldownAt",
    "lastSensoryAt",
    "covertTrainingType",
    "covertTrainingStartedAt",
    "covertTrainingMinutes",
    // relation objects and routing keys that are not columns
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
      out.items = live.items.map((r) => typeof r === "string" ? { ids: [r], number: 1 } : r && Array.isArray(r.ids) ? r : r ? { ids: [r.itemId ?? r.id].filter(Boolean), number: r.number ?? r.quantity ?? 1 } : null).filter((x) => x && x.ids.length);
    }
    for (const [k, v] of Object.entries(data)) if (!["rules", "includeDefaultRules"].includes(k)) out[k] = v;
    if (Array.isArray(out.jutsus)) out.jutsus = out.jutsus.map((j) => typeof j === "string" ? j : j && (j.jutsuId || j.id)).filter(Boolean);
    if (Array.isArray(out.items)) out.items = out.items.map((t) => typeof t === "string" ? { ids: [t], number: 1 } : t && Array.isArray(t.ids) ? t : t ? { ids: [t.itemId || t.id].filter(Boolean), number: t.number ?? t.quantity ?? 1 } : null).filter((x) => x && x.ids.length);
    out.isAi = true;
    if (out.userId == null && live && live.userId) out.userId = live.userId;
    return out;
  }

  // src/runner/refs.mjs
  var REF_RE = /^@(jutsu|ai|scene|item|quest|bloodline|img):(.+)$/;
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

  // src/storage/hash.mjs
  function stableStringify(v) {
    if (v === null || typeof v !== "object") return JSON.stringify(v);
    if (Array.isArray(v)) return "[" + v.map(stableStringify).join(",") + "]";
    const keys = Object.keys(v).sort();
    return "{" + keys.map((k) => JSON.stringify(k) + ":" + stableStringify(v[k])).join(",") + "}";
  }
  function fnv1a32(str) {
    let h2 = 2166136261;
    for (let i = 0; i < str.length; i++) {
      h2 ^= str.charCodeAt(i);
      h2 = Math.imul(h2, 16777619) >>> 0;
    }
    return h2.toString(16).padStart(8, "0");
  }
  function payloadHash(payload) {
    return fnv1a32(stableStringify(payload === void 0 ? null : payload));
  }

  // src/runner/manifest.mjs
  var ENTITIES = Object.freeze(["jutsu", "item", "bloodline", "asset", "quest", "ai", "aiProfile"]);
  var SLOT_TO_OP = Object.freeze({ create: "create", edit: "update", convert: "update" });
  var ManifestError = class extends Error {
    constructor(message, info = {}) {
      super(message);
      this.name = "ManifestError";
      Object.assign(this, info);
    }
  };
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
    const capture = m.capture && typeof m.capture === "object" ? { before: Array.isArray(m.capture.before) ? m.capture.before : [], after: Array.isArray(m.capture.after) ? m.capture.after : [] } : { before: [], after: [] };
    for (const c of [...capture.before, ...capture.after]) {
      if (!c || typeof c !== "object" || !(c.proc || c.procedure)) throw new ManifestError("capture entry missing proc");
    }
    if (!raw.length && !capture.before.length && !capture.after.length) throw new ManifestError("manifest has no items and no captures");
    const items = raw.map((it, i) => normalizeItem(it, i));
    const problems = [];
    const srcIds = /* @__PURE__ */ new Set();
    for (const it of items) {
      if (it.op === "create" && !it.srcId) problems.push(`item ${it.idx} (${it.name}): a create needs srcId`);
      if (it.op === "update" && !it.targetId) problems.push(`item ${it.idx} (${it.name}): an edit needs targetId`);
      if (it.srcId) {
        if (srcIds.has(it.srcId)) problems.push(`duplicate srcId ${it.srcId}`);
        srcIds.add(it.srcId);
      }
      if (it.entity === "aiProfile" && it.op === "create") problems.push(`item ${it.idx}: aiProfile cannot be created directly; create an ai with rules`);
    }
    if (problems.length) throw new ManifestError("manifest problems:\n" + problems.join("\n"), { problems });
    return {
      items,
      capture,
      note: typeof m._note === "string" ? m._note : null,
      skipPreflight: !!m.skipPreflight,
      dedupNames: !!m.dedupNames,
      readBack: m.readBack !== false,
      imgSizes: m.imgSizes && typeof m.imgSizes === "object" ? m.imgSizes : {},
      hash: fnv1a32(stableStringify({ items: raw, capture }))
    };
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
      data
    };
  }
  function planOrder(manifest, idmap = {}) {
    const bySrc = new Map(manifest.items.filter((it) => it.srcId).map((it) => [it.srcId, it]));
    const nodes = manifest.items.map((it) => {
      const refs = collectRefs({ data: it.data, targetId: it.targetId });
      const deps = [];
      for (const r of refs) {
        if (r.pfx === "img") continue;
        if (idmap[r.key]) continue;
        const src = bySrc.get(r.key);
        if (!src) throw new ManifestError(`item ${it.idx} (${it.name}): @${r.pfx}:${r.key} is unknown (no srcId in this manifest, not in idmap)`, { idx: it.idx, ref: r });
        if (src.idx === it.idx) throw new ManifestError(`item ${it.idx} references itself`);
        deps.push(src.srcId);
      }
      return { it, deps };
    });
    const order = [];
    const state = /* @__PURE__ */ new Map();
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

  // src/runner/runner.mjs
  var Paused = class extends Error {
    constructor(reason, info = {}) {
      super(`paused: ${reason}`);
      this.name = "Paused";
      this.reason = reason;
      Object.assign(this, info);
    }
  };
  var Runner = class {
    /**
     * @param {object} d  dependencies
     * @param {import("../storage/journal.mjs").Journal} d.journal
     * @param {import("../transport/client.mjs").TrpcClient} d.client
     * @param {import("../budget/reader.mjs").CachedReader} d.reader
     * @param {import("../storage/captures.mjs").CaptureCache} d.cache
     * @param {import("./validate.mjs").Validator} d.validator
     * @param {object} [d.uploader]      {upload(file) -> {ufsUrl}}
     * @param {object} [d.reconciler]    {beforeCreate(job, item, entity), resolveSent(job, item)}
     * @param {Storage} d.storage        for the retained idmap
     * @param {(msg: string, item?: object) => void} [d.log]
     */
    constructor(d) {
      for (const k of ["journal", "client", "reader", "cache", "validator", "storage"]) if (!d[k]) throw new Error("Runner needs " + k);
      Object.assign(this, d);
      this.log = d.log ?? (() => {
      });
      this.files = /* @__PURE__ */ new Map();
      this.manifests = /* @__PURE__ */ new Map();
    }
    // ------------------------------------------------------------------ lifecycle
    /** Plan a manifest and open a job. Returns the journal job. Does not send anything. */
    plan(manifestSource, { jobId, manifestPath = null, manifestNumber: manifestNumber2 = null } = {}) {
      const manifest = parseManifest(manifestSource);
      const order = planOrder(manifest, readIdmap(this.storage));
      const job = this.journal.open({ jobId, manifestPath, manifestNumber: manifestNumber2, manifestHash: manifest.hash, items: toJournalSpecs(order) });
      this.manifests.set(jobId, { manifest, order });
      return job;
    }
    /** Attach the parsed manifest to an existing (resumed) job. */
    attach(jobId, manifestSource) {
      const manifest = parseManifest(manifestSource);
      const job = this.journal.get(jobId);
      if (!job) throw new Error("no such job " + jobId);
      if (job.manifestHash && manifest.hash !== job.manifestHash) {
        throw new Error(`manifest changed under job ${jobId}: journal hash ${job.manifestHash}, file hash ${manifest.hash}`);
      }
      const order = planOrder(manifest, readIdmap(this.storage));
      if (order.length !== job.items.length) throw new Error("manifest item count differs from the journal");
      this.manifests.set(jobId, { manifest, order });
    }
    /** Run every non-terminal item in order. Returns a summary. */
    async run(jobId) {
      const { manifest, order } = this._m(jobId);
      let job = this.journal.get(jobId);
      if (job.state === "PAUSED") {
        const t = this.budget && this.budget.log && this.budget.log.tripped();
        if (t) return this._pause(jobId, "TOO_MANY_REQUESTS", { path: t.path, until: t.until });
        job = this.journal.setJobState(jobId, "RUNNING");
      }
      if (job.items.some((it) => it.state === "SENT")) {
        throw new Error("job has SENT items; call resume() so they are reconciled before anything else is sent");
      }
      if (manifest.capture.before.length && !job.capturesBefore) {
        await this._captures(jobId, manifest.capture.before, "before");
      }
      try {
        for (let i = 0; i < job.items.length; i++) {
          job = this.journal.get(jobId);
          const item = job.items[i];
          if (["VERIFIED", "FAILED", "SKIPPED", "ORPHANED"].includes(item.state)) continue;
          await this._runItem(jobId, item, order[i], manifest);
        }
        if (manifest.capture.after.length) await this._captures(jobId, manifest.capture.after, "after");
      } catch (e) {
        if (e instanceof Paused) return this._pause(jobId, e.reason, e);
        throw e;
      }
      this.journal.setJobState(jobId, "DONE");
      if (this.reconciler && typeof this.reconciler.forget === "function") this.reconciler.forget(jobId);
      return this.summary(jobId);
    }
    /** Reconcile SENT items through the reconciler, then run. */
    async resume(jobId) {
      if (!this.reconciler) throw new Error("resume needs a reconciler");
      const { order } = this._m(jobId);
      const job = this.journal.get(jobId);
      for (const item of job.items) {
        if (item.state !== "SENT") continue;
        const r = await this.reconciler.resolveSent(job, item, { planned: order[item.idx] });
        if (r.action === "confirm") {
          this.journal.transition(jobId, item.idx, "CONFIRMED", { entityId: r.entityId ?? item.entityId, phase: r.landed ? "verify" : r.phase ?? item.phase, reconciled: r.note ?? "confirmed by reconciliation" });
          if (r.entityId && item.srcId) this._remember(item.srcId, r.entityId);
        } else if (r.action === "orphan") {
          this.journal.transition(jobId, item.idx, "ORPHANED", { error: r.note ?? "ambiguous after crash", candidates: r.candidates ?? [] });
        } else {
          throw new Error("reconciler returned unknown action " + r.action);
        }
      }
      return this.run(jobId);
    }
    /** User decision on an ORPHANED item: adopt an id (continue at update) or skip. */
    adopt(jobId, idx, entityId) {
      const item = this.journal.get(jobId).items[idx];
      this.journal.transition(jobId, idx, "CONFIRMED", { entityId, phase: item.op === "create" ? "update" : item.phase, adopted: true });
      if (item.srcId) this._remember(item.srcId, entityId);
    }
    skip(jobId, idx) {
      this.journal.transition(jobId, idx, "SKIPPED");
    }
    summary(jobId) {
      const job = this.journal.get(jobId);
      const counts = {};
      for (const it of job.items) counts[it.state] = (counts[it.state] ?? 0) + 1;
      return { jobId, state: job.state, pause: job.pause, counts, items: job.items.map((it) => ({ idx: it.idx, name: it.name, entity: it.entity, state: it.state, phase: it.phase, entityId: it.entityId, error: it.error ?? null, diffs: it.diffs ?? null })) };
    }
    // ------------------------------------------------------------------ items
    async _runItem(jobId, item, planned, manifest) {
      const ent = item.entity;
      try {
        if (item.state === "CONFIRMED" && item.phase === "verify") {
          if (manifest.readBack) await this._verify(jobId, item, planned);
          else this.journal.transition(jobId, item.idx, "VERIFIED", { verify: "skipped" });
          return;
        }
        if (item.op === "create" && item.state === "PLANNED") {
          await this._create(jobId, item, planned);
          item = this.journal.get(jobId).items[item.idx];
          if (item.state !== "CONFIRMED") return;
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
        if (item.state === "CONFIRMED" && manifest.readBack) await this._verify(jobId, item, planned);
      } catch (e) {
        if (e instanceof Paused) throw e;
        if (e instanceof RateLimited) throw new Paused("TOO_MANY_REQUESTS", { path: e.path, until: e.until, idx: item.idx });
        const cur = this.journal.get(jobId).items[item.idx];
        if (cur.state === "SENT") {
          throw new Paused(e instanceof NetworkError ? "NETWORK" : e instanceof TransportError ? "UNDECODABLE_RESPONSE" : "AMBIGUOUS", { idx: item.idx, detail: String(e && e.message) });
        }
        this.journal.transition(jobId, item.idx, "FAILED", { error: String(e && e.message ? e.message : e) });
        this.log(`item ${item.idx} failed: ${e && e.message}`, item);
      }
    }
    async _create(jobId, item, planned) {
      const rc = recipe(item.entity);
      if (this.reconciler) {
        const key = await this.reconciler.beforeCreate(this.journal.get(jobId), item, item.entity);
        if (key) this.journal.annotate(jobId, item.idx, { snapshotKey: key });
      }
      const input = rc.create.input(planned.data);
      const decoded = await this.journal.withSent(jobId, item.idx, { phase: "create" }, () => this.client.call(rc.create.path, input));
      const o = readCreate(decoded);
      if (o.kind === "ok") {
        this.journal.transition(jobId, item.idx, "CONFIRMED", { entityId: o.id, phase: "update" });
        this._remember(item.srcId, o.id);
        await this.cache.invalidateEntity(rc.cacheEntity);
        this.log(`created ${item.entity} ${o.id} (placeholder)`, item);
        return;
      }
      this._failFromOutcome(jobId, item, o, "create");
    }
    async _fill(jobId, item, planned) {
      const rc = recipe(item.entity);
      const id = item.entityId ?? item.targetId;
      if (!id) throw new Error("no id to fill");
      const data = await this._resolved(planned.data);
      const live = await this.reader.get(rc.get, id, { fresh: true });
      if (!live.ok) {
        const cls = classifyError(live.error);
        if (cls === "SESSION") throw new Paused("SESSION", { detail: live.error.message });
        throw new Error(`${rc.get} failed: ${live.error.code} ${live.error.message}`);
      }
      if (live.data == null) throw new Error(`${rc.get} returned no record for ${id}`);
      const problems = this.validator.problems(item.entity, data, live.data);
      if (problems.length) throw new Error("pre-send validation: " + problems.join("; "));
      const payload = mergeForUpdate(item.entity, live.data, data, this.validator.knownFields(item.entity));
      const decoded = await this.journal.withSent(jobId, item.idx, { phase: "update" }, () => this.client.call(rc.update, { id, data: payload }));
      const o = readMutation(decoded);
      await this.cache.invalidateRecord(rc.cacheEntity, id);
      if (o.kind === "ok") {
        this.journal.transition(jobId, item.idx, "CONFIRMED", { entityId: id, phase: "update", asserted: Object.keys(data) });
        return;
      }
      this._failFromOutcome(jobId, item, o, "update");
    }
    async _rules(jobId, item, planned, userId) {
      const rc = recipe("aiProfile");
      const rules = planned.data.rules ?? [];
      const includeDefaultRules = planned.data.includeDefaultRules !== false;
      if (item.entity === "aiProfile") {
        const problems = this.validator.problems("aiProfile", planned.data, null);
        if (problems.length) throw new Error("pre-send validation: " + problems.join("; "));
      }
      let live = await this.reader.get(rc.get, userId, { fresh: true });
      if (!live.ok || !live.data) throw new Error(`profile.getAi failed for ${userId}`);
      let apid = live.data.aiProfileId;
      if (!apid) {
        const decoded2 = await this.journal.withSent(jobId, item.idx, { phase: "rules-toggle" }, () => this.client.call(rc.profileToggle, { aiId: userId }));
        const o2 = readMutation(decoded2);
        if (o2.kind !== "ok") {
          this._failFromOutcome(jobId, item, o2, "toggle");
          return;
        }
        this.journal.transition(jobId, item.idx, "CONFIRMED", { phase: "rules" });
        live = await this.reader.get(rc.get, userId, { fresh: true });
        apid = live.ok && live.data ? live.data.aiProfileId : null;
        if (!apid) throw new Error("no aiProfileId after toggle");
      }
      const decoded = await this.journal.withSent(jobId, item.idx, { phase: "rules", aiProfileId: apid }, () => this.client.call(rc.profileUpdate, { id: apid, rules, includeDefaultRules }));
      const o = readMutation(decoded);
      await this.cache.invalidateEntity("ai");
      if (o.kind === "ok") {
        this.journal.transition(jobId, item.idx, "CONFIRMED", { entityId: userId, phase: "rules", aiProfileId: apid, asserted: ["rules", "includeDefaultRules"] });
        return;
      }
      this._failFromOutcome(jobId, item, o, "rules");
    }
    async _verify(jobId, item, planned) {
      const rc = recipe(item.entity);
      const data = await this._resolved(planned.data);
      const diffs = [];
      if (item.entity !== "aiProfile") {
        const live = await this.reader.get(rc.get, item.entityId, { fresh: true });
        if (!live.ok || !live.data) {
          this.journal.annotate(jobId, item.idx, { verify: "unread" });
          return;
        }
        diffs.push(...diffAsserted(item.entity, data, live.data));
      }
      if (item.entity === "ai" && Array.isArray(planned.data.rules) || item.entity === "aiProfile") {
        const pr = await this.reader.get("ai.getAiProfile", item.aiProfileId, { fresh: true });
        if (pr.ok && pr.data) {
          if (JSON.stringify(pr.data.rules ?? []) !== JSON.stringify(planned.data.rules ?? [])) diffs.push({ key: "rules", sent: planned.data.rules, live: pr.data.rules });
          if (planned.data.includeDefaultRules !== void 0 && pr.data.includeDefaultRules !== planned.data.includeDefaultRules) diffs.push({ key: "includeDefaultRules", sent: planned.data.includeDefaultRules, live: pr.data.includeDefaultRules });
        } else {
          this.journal.annotate(jobId, item.idx, { verify: "unread" });
          return;
        }
      }
      if (diffs.length) this.journal.annotate(jobId, item.idx, { diffs, verify: "drift" });
      else this.journal.transition(jobId, item.idx, "VERIFIED", { diffs: [], verify: "match" });
    }
    async _captures(jobId, list, phase) {
      const out = [];
      for (const c of list) {
        const path = c.proc || c.procedure;
        try {
          const id = c.input && (c.input.id ?? c.input.userId);
          const r = id != null ? await this.reader.get(path, id, { fresh: true }) : await this.reader.list(path, { fresh: true });
          out.push({ phase, proc: path, input: c.input ?? null, ok: r.ok, rows: Array.isArray(r.data) ? r.data.length : r.data ? 1 : 0, error: r.ok ? null : r.error.code });
        } catch (e) {
          if (e instanceof RateLimited) throw new Paused("TOO_MANY_REQUESTS", { path: e.path, until: e.until });
          out.push({ phase, proc: path, input: c.input ?? null, ok: false, error: String(e && e.message) });
        }
      }
      const job = this.journal.get(jobId);
      const patch = phase === "before" ? { capturesBefore: out } : { capturesAfter: out };
      Object.assign(job, patch);
      this.journal._write(job);
      return out;
    }
    // ------------------------------------------------------------------ helpers
    _m(jobId) {
      const m = this.manifests.get(jobId);
      if (!m) throw new Error("no manifest attached for job " + jobId + "; call plan() or attach()");
      return m;
    }
    _pause(jobId, reason, info) {
      this.journal.setJobState(jobId, "PAUSED", { pause: { reason, path: info.path ?? null, until: info.until ?? null, idx: info.idx ?? null, detail: info.detail ?? null } });
      this.log(`paused: ${reason}${info.path ? " on " + info.path : ""}`);
      return this.summary(jobId);
    }
    _failFromOutcome(jobId, item, o, step) {
      if (o.kind === "refused") {
        this.journal.transition(jobId, item.idx, "FAILED", { error: `${step} refused: ${o.message}` });
        return;
      }
      const cls = classifyError(o.error);
      if (cls === "SESSION") throw new Paused("SESSION", { detail: o.error.message, idx: item.idx });
      const issues = o.error.zodError ? " " + o.error.zodError.map((z) => `${(z.path || []).join(".")}: ${z.message}`).join("; ") : "";
      this.journal.transition(jobId, item.idx, "FAILED", { error: `${step} ${cls}: ${o.error.message}${issues}`, zodError: o.error.zodError ?? null });
    }
    _remember(srcId, id) {
      if (!srcId || !id) return;
      const map = readIdmap(this.storage);
      map[srcId] = id;
      writeIdmap(this.storage, map);
    }
    async _resolved(data) {
      const refs = collectRefs(data).filter((r) => r.pfx === "img");
      for (const r of refs) {
        const map2 = readIdmap(this.storage);
        if (map2[r.key]) continue;
        const file = this.files.get(r.key);
        if (!file) throw new Error(`@img:${r.key} has no file picked`);
        if (!this.uploader) throw new Error("no uploader configured for @img refs");
        const up = await this.uploader.upload(file);
        map2[r.key] = up.ufsUrl;
        writeIdmap(this.storage, map2);
      }
      const map = readIdmap(this.storage);
      const { value, unresolved } = resolveRefs(data, (pfx, key) => map[key]);
      if (unresolved.length) throw new Error("unresolved refs: " + unresolved.map((u) => `@${u.pfx}:${u.key} at ${u.path}`).join(", "));
      return value;
    }
  };

  // src/reconcile/reconciler.mjs
  var SNAP_PREFIX = "tnr_forge_snap_v1:";
  var Reconciler = class {
    /**
     * @param {object} o
     * @param {Storage} o.storage
     * @param {import("../budget/reader.mjs").CachedReader} o.reader
     * @param {() => number} [o.clock]
     */
    constructor({ storage, reader, clock = () => Date.now() }) {
      this.storage = storage;
      this.reader = reader;
      this.clock = clock;
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
    /** Called by the runner before every create; takes the snapshot once per (job, entity). */
    async beforeCreate(job, item, entity) {
      const key = this.snapKey(job.jobId, entity);
      if (this.storage.getItem(key)) return key;
      const rc = recipe(entity);
      const list = await this.reader.list(rc.names, { fresh: true });
      if (!list.ok || !Array.isArray(list.data)) throw new Error(`snapshot failed: ${rc.names} ${list.ok ? "returned no list" : list.error.code}`);
      const ids = list.data.map((r) => r[rc.idKey]).filter(Boolean);
      this.storage.setItem(key, JSON.stringify({ entity, at: new Date(this.clock()).toISOString(), path: rc.names, count: ids.length, ids }));
      return key;
    }
    /** Drop a job's snapshots (after the job is DONE or removed). */
    forget(jobId) {
      const keys = [];
      for (let i = 0; i < this.storage.length; i++) {
        const k = this.storage.key(i);
        if (k && k.startsWith(SNAP_PREFIX + jobId + ":")) keys.push(k);
      }
      for (const k of keys) this.storage.removeItem(k);
      return keys.length;
    }
    /**
     * Decide what a SENT item became.
     * @param {object} job     journal job
     * @param {object} item    the SENT item
     * @param {object} ctx     {planned} the planned item (data with refs unresolved is fine here)
     * @returns {Promise<{action:"confirm", entityId?, phase?, landed?, note} | {action:"orphan", candidates, note}>}
     */
    async resolveSent(job, item, ctx = {}) {
      const rc = recipe(item.entity);
      if (item.phase === "create" || !item.entityId) return this._resolveCreate(job, item, rc);
      if (item.phase === "rules-toggle") return this._resolveToggle(item, rc);
      if (item.phase === "rules") return this._resolveRules(item, ctx);
      return this._resolveUpdate(item, rc, ctx);
    }
    async _resolveCreate(job, item, rc) {
      const key = item.snapshotKey || this.snapKey(job.jobId, item.entity);
      const snap = this.readSnapshot(key);
      if (!snap) return { action: "orphan", candidates: [], note: "no pre-create snapshot for this entity type; cannot tell which row is ours" };
      const list = await this.reader.list(rc.names, { fresh: true });
      if (!list.ok || !Array.isArray(list.data)) return { action: "orphan", candidates: [], note: `${rc.names} unavailable: ${list.ok ? "no list" : list.error.code}` };
      const before = new Set(snap.ids);
      const confirmedThisJob = new Set(job.items.filter((it) => it.entity === item.entity && it.entityId && it.idx !== item.idx).map((it) => it.entityId));
      const rows = list.data.filter((r) => !before.has(r[rc.idKey]) && !confirmedThisJob.has(r[rc.idKey]));
      const pending = job.items.filter((it) => it.entity === item.entity && it.state === "SENT" && (it.phase === "create" || !it.entityId));
      const candidates = rows.map((r) => ({ id: r[rc.idKey], name: r[rc.nameKey] ?? null, placeholderName: rc.placeholder ? rc.placeholder(r[rc.idKey]) === (r[rc.nameKey] ?? null) : null }));
      if (candidates.length === 1 && pending.length === 1) {
        const c = candidates[0];
        return { action: "confirm", entityId: c.id, phase: "update", note: `adopted the single new ${item.entity} ${c.id}` + (c.placeholderName === false ? " (name is not the placeholder pattern; check it)" : "") };
      }
      return { action: "orphan", candidates, note: `${candidates.length} new ${item.entity} row(s) since the snapshot, ${pending.length} create(s) pending: ambiguous` };
    }
    async _resolveUpdate(item, rc, ctx) {
      const planned = ctx.planned;
      if (!planned) return { action: "orphan", candidates: [], note: "no planned data to compare against" };
      const live = await this.reader.get(rc.get, item.entityId, { fresh: true });
      if (!live.ok || !live.data) return { action: "orphan", candidates: [], note: `${rc.get} ${item.entityId}: ${live.ok ? "no record" : live.error.code}` };
      const data = stripRefs(planned.data);
      const diffs = diffAsserted(item.entity, data, live.data);
      if (!diffs.length) return { action: "confirm", entityId: item.entityId, phase: "verify", landed: true, note: "update already landed: asserted keys match live" };
      return { action: "orphan", candidates: [], note: "update may not have landed: live differs on " + diffs.map((d) => d.key).join(", "), diffs };
    }
    async _resolveToggle(item, rc) {
      const live = await this.reader.get(rc.get, item.entityId, { fresh: true });
      if (live.ok && live.data && live.data.aiProfileId) return { action: "confirm", entityId: item.entityId, phase: "rules", note: "profile row exists; continue at rules" };
      return { action: "orphan", candidates: [], note: "no aiProfileId after a sent toggle" };
    }
    async _resolveRules(item, ctx) {
      if (!item.aiProfileId) return { action: "orphan", candidates: [], note: "rules sent but no aiProfileId recorded" };
      const prof = await this.reader.get("ai.getAiProfile", item.aiProfileId, { fresh: true });
      if (!prof.ok || !prof.data) return { action: "orphan", candidates: [], note: "ai.getAiProfile unavailable" };
      const want = ctx.planned ? ctx.planned.data.rules ?? [] : null;
      if (want && JSON.stringify(prof.data.rules ?? []) === JSON.stringify(want)) return { action: "confirm", entityId: item.entityId, phase: "verify", landed: true, note: "rules already landed" };
      return { action: "orphan", candidates: [], note: "rules may not have landed: profile rules differ" };
    }
  };
  function stripRefs(data) {
    const out = {};
    for (const [k, v] of Object.entries(data)) if (!/@(jutsu|ai|scene|item|quest|bloodline|img):/.test(JSON.stringify(v) ?? "")) out[k] = v;
    return out;
  }

  // src/github.mjs
  var GH = Object.freeze({ owner: "perseverance484", repo: "tnr-tools", branch: "main", pushDir: "push", inboxDir: "harvests/inbox" });
  var GithubError = class extends Error {
    constructor(message, info = {}) {
      super(message);
      this.name = "GithubError";
      Object.assign(this, info);
    }
  };
  var Github = class {
    /**
     * @param {object} o
     * @param {(url: string, init: object) => Promise<Response>} o.fetchImpl  a plain fetch (NOT the Session)
     * @param {Storage} o.storage  where tnr_bk_gh_v1 lives
     */
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
    /** List a directory: [{name, path, sha, size, type}] */
    async list(dir = this.cfg.pushDir) {
      const r = await this.fetchImpl(this._url(dir), { headers: this._headers() });
      if (!r.ok) throw new GithubError(`list ${dir}: HTTP ${r.status}`, { status: r.status });
      const j = await r.json();
      if (!Array.isArray(j)) throw new GithubError(`${dir} is not a directory`);
      return j.map(({ name, path, sha, size, type }) => ({ name, path, sha, size, type }));
    }
    /** Fetch a file's raw bytes. */
    async raw(path, ref) {
      const r = await this.fetchImpl(this._url(path, ref), { headers: this._headers("application/vnd.github.raw+json") });
      if (!r.ok) throw new GithubError(`fetch ${path}: HTTP ${r.status}`, { status: r.status });
      return r.arrayBuffer();
    }
    async text(path, ref) {
      return new TextDecoder().decode(await this.raw(path, ref));
    }
    /** Create or update a file (sha-aware). Returns {sha, htmlUrl} or throws. */
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
      const items = Array.isArray(m.items) ? m.items : Array.isArray(m.jutsu) ? m.jutsu : [];
      const caps = m.capture && (m.capture.before || []).length + (m.capture.after || []).length || 0;
      const title = typeof m._note === "string" ? m._note.split(/\.\s|\n/)[0].slice(0, 80) : items[0] && items[0].name || "";
      const creates = items.filter((i) => i && i.slot === "create").length;
      return { ok: true, title, items: items.length, creates, captures: caps };
    } catch (e) {
      return { ok: false, title: "(not JSON: " + e.message.slice(0, 40) + ")", items: 0, creates: 0, captures: 0 };
    }
  }

  // src/ui/dom.mjs
  function h(tag, attrs = {}, ...children) {
    const el = document.createElement(tag);
    for (const [k, v] of Object.entries(attrs || {})) {
      if (v == null || v === false) continue;
      if (k === "class") el.className = v;
      else if (k === "style" && typeof v === "object") Object.assign(el.style, v);
      else if (k.startsWith("on") && typeof v === "function") el.addEventListener(k.slice(2).toLowerCase(), v);
      else if (k === "dataset") Object.assign(el.dataset, v);
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

  // src/ui/styles.mjs
  var CSS = `
:root { color-scheme: dark; --bg:#0f1115; --panel:#171a21; --line:#2a2f3a; --ink:#e8eaf0; --mute:#9aa3b2; --ok:#5fbf8a; --warn:#d9a441; --bad:#e0655f; --acc:#7aa2ff; --sent:#b08cff; }
html, body { margin:0; padding:0; background:var(--bg); color:var(--ink); font: 15px/1.45 system-ui, -apple-system, "Segoe UI", Roboto, sans-serif; -webkit-text-size-adjust:100%; }
* { box-sizing:border-box; }
.f-app { min-height:100vh; display:flex; flex-direction:column; }
.f-top { position:sticky; top:0; z-index:10; background:var(--panel); border-bottom:1px solid var(--line); display:flex; align-items:center; gap:8px; padding:8px 10px; }
.f-title { font-weight:700; letter-spacing:.02em; }
.f-ver { color:var(--mute); font-size:12px; margin-left:auto; }
.f-nav { display:flex; gap:4px; overflow-x:auto; padding:6px 8px; background:var(--panel); border-bottom:1px solid var(--line); }
.f-nav button { flex:1 0 auto; min-height:40px; }
.f-nav button[aria-current="page"] { background:var(--acc); color:#0b0d12; }
.f-main { flex:1; padding:12px 10px 80px; max-width:760px; width:100%; margin:0 auto; }
h2 { font-size:17px; margin:14px 0 8px; } h3 { font-size:14px; color:var(--mute); margin:12px 0 6px; text-transform:uppercase; letter-spacing:.06em; }
button, .f-btn { font:inherit; min-height:44px; padding:8px 14px; border:1px solid var(--line); border-radius:8px; background:#222733; color:var(--ink); cursor:pointer; }
button:disabled { opacity:.45; cursor:default; }
button.f-primary { background:var(--acc); color:#0b0d12; border-color:transparent; font-weight:600; }
button.f-danger { border-color:var(--bad); color:var(--bad); }
input[type=text], input[type=password], input[type=search], textarea { font:inherit; width:100%; min-height:44px; padding:8px 10px; border:1px solid var(--line); border-radius:8px; background:#0b0d12; color:var(--ink); }
textarea { min-height:160px; font-family: ui-monospace, Menlo, monospace; font-size:12px; }
.f-card { background:var(--panel); border:1px solid var(--line); border-radius:10px; padding:10px 12px; margin:8px 0; }
.f-row { display:flex; align-items:center; gap:10px; padding:10px 0; border-bottom:1px solid var(--line); }
.f-row:last-child { border-bottom:0; }
.f-row.f-tap { cursor:pointer; } .f-row.f-tap:active { background:#1d2230; }
.f-grow { flex:1; min-width:0; } .f-mute { color:var(--mute); font-size:13px; } .f-mono { font-family: ui-monospace, Menlo, monospace; font-size:12px; word-break:break-all; }
.f-pill { display:inline-block; padding:2px 8px; border-radius:999px; font-size:12px; font-weight:600; border:1px solid var(--line); color:var(--mute); }
.f-pill.PLANNED { color:var(--mute); } .f-pill.SENT { color:var(--sent); border-color:var(--sent); } .f-pill.CONFIRMED { color:var(--acc); border-color:var(--acc); }
.f-pill.VERIFIED, .f-pill.DONE { color:var(--ok); border-color:var(--ok); } .f-pill.FAILED, .f-pill.ABORTED { color:var(--bad); border-color:var(--bad); }
.f-pill.ORPHANED, .f-pill.PAUSED { color:var(--warn); border-color:var(--warn); } .f-pill.SKIPPED { color:var(--mute); }
.f-banner { padding:10px 12px; border-radius:10px; margin:8px 0; border:1px solid; }
.f-banner.warn { border-color:var(--warn); background:#2a2312; } .f-banner.bad { border-color:var(--bad); background:#2a1515; } .f-banner.ok { border-color:var(--ok); background:#12261c; } .f-banner.info { border-color:var(--acc); background:#141b2e; }
.f-bar { height:6px; background:#0b0d12; border-radius:4px; overflow:hidden; margin:6px 0; } .f-bar > i { display:block; height:100%; background:var(--acc); }
.f-bar.warn > i { background:var(--warn); }
.f-actions { display:flex; gap:8px; flex-wrap:wrap; margin-top:8px; }
.f-kv { display:grid; grid-template-columns: auto 1fr; gap:4px 12px; font-size:13px; } .f-kv b { color:var(--mute); font-weight:500; }
.f-err { white-space:pre-wrap; font-family: ui-monospace, Menlo, monospace; font-size:12px; color:#ffb4b0; }
.f-toast { position:fixed; left:10px; right:10px; bottom:12px; z-index:20; }
details summary { cursor:pointer; color:var(--mute); }
`;

  // src/ui/screens.mjs
  var pill = (state) => h("span", { class: "f-pill " + state }, state);
  function JobsScreen(app) {
    const jobs = app.journal.listJobs();
    const open = app.journal.resumable();
    const orphans = jobs.flatMap((j) => j.items.filter((it) => it.state === "ORPHANED").map((it) => ({ job: j, it })));
    const root = h("section", {});
    if (open.length) {
      for (const j of open) {
        root.appendChild(h(
          "div",
          { class: "f-banner warn" },
          h("div", {}, h("b", {}, "Open job: "), j.manifestPath || j.jobId, " ", pill(j.state)),
          j.pause ? h("div", { class: "f-mute" }, `Paused: ${j.pause.reason}${j.pause.path ? " on " + j.pause.path : ""}${j.pause.until ? " \xB7 retry allowed in " + fmtCountdown(j.pause.until, app.now()) : ""}${j.pause.detail ? " \xB7 " + j.pause.detail : ""}`) : null,
          h(
            "div",
            { class: "f-actions" },
            h("button", { class: "f-primary", onClick: () => app.resumeJob(j.jobId) }, j.items.some((i) => i.state === "SENT") ? "Reconcile & resume" : "Resume"),
            h("button", { onClick: () => app.go("run", { jobId: j.jobId }) }, "Open")
          )
        ));
      }
    }
    if (orphans.length) {
      root.appendChild(h("h2", {}, `Orphans needing a decision (${orphans.length})`));
      for (const { job, it } of orphans) root.appendChild(OrphanCard(app, job, it));
    }
    root.appendChild(h("h2", {}, "Recent runs"));
    if (!jobs.length) root.appendChild(h("div", { class: "f-mute" }, "No jobs yet. Pick a manifest to start one."));
    for (const j of jobs.slice(0, 20)) {
      const counts = {};
      for (const it of j.items) counts[it.state] = (counts[it.state] ?? 0) + 1;
      root.appendChild(h(
        "div",
        { class: "f-row f-tap", onClick: () => app.go("run", { jobId: j.jobId }) },
        h(
          "div",
          { class: "f-grow" },
          h("div", {}, j.manifestPath || j.jobId, " ", pill(j.state)),
          h("div", { class: "f-mute" }, `${j.items.length} items \xB7 ${Object.entries(counts).map(([k, v]) => `${v} ${k.toLowerCase()}`).join(", ")} \xB7 ${fmtAgo(j.startedAt, app.now())}`)
        )
      ));
    }
    return root;
  }
  function OrphanCard(app, job, it) {
    const cands = it.candidates || [];
    const card = h(
      "div",
      { class: "f-card" },
      h("div", {}, h("b", {}, it.name), " ", h("span", { class: "f-mute" }, `${it.entity} \xB7 ${job.manifestPath || job.jobId} \xB7 item ${it.idx}`)),
      h("div", { class: "f-mute" }, it.error || "ambiguous")
    );
    if (cands.length) {
      card.appendChild(h("h3", {}, "Candidates on the server"));
      for (const c of cands) {
        const id = typeof c === "string" ? c : c.id;
        const name = typeof c === "string" ? "" : c.name;
        card.appendChild(h(
          "div",
          { class: "f-row" },
          h("div", { class: "f-grow" }, h("div", { class: "f-mono" }, id), name ? h("div", { class: "f-mute" }, name) : null),
          h("button", { onClick: () => app.confirm(`Adopt ${id} as "${it.name}"? The job will continue with its update.`, () => app.adopt(job.jobId, it.idx, id)) }, "Adopt")
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
  function ManifestsScreen(app) {
    const root = h("section", {});
    const q = h("input", { type: "search", placeholder: "search filename, number, title", value: app.state.pickerQuery || "", onInput: (e) => {
      app.state.pickerQuery = e.target.value;
      renderList();
    } });
    const list = h("div", {});
    const status = h("div", { class: "f-mute" });
    root.append(h("div", { class: "f-actions" }, q, h("button", { onClick: () => app.loadPicker(true) }, "Refresh")), status, list);
    function renderList() {
      const entries = app.state.picker || [];
      const needle = (app.state.pickerQuery || "").toLowerCase();
      const seen = new Set(app.journal.listJobs().map((j) => j.manifestPath));
      const rows = entries.filter((e) => !needle || e.name.toLowerCase().includes(needle) || String(e.number ?? "").includes(needle) || (e.summary?.title || "").toLowerCase().includes(needle));
      replace(list, rows.length ? rows.map((e) => h(
        "div",
        { class: "f-row f-tap", onClick: () => app.selectManifest(e) },
        h(
          "div",
          { class: "f-grow" },
          h("div", {}, e.number != null ? h("b", {}, "#" + e.number + " ") : null, e.name, seen.has(e.path) ? h("span", { class: "f-pill VERIFIED", style: { marginLeft: "6px" } }, "ran") : null),
          h("div", { class: "f-mute" }, e.summary ? `${e.summary.title || "(untitled)"} \xB7 ${e.summary.items} item${e.summary.items === 1 ? "" : "s"}${e.summary.creates ? ` (${e.summary.creates} create)` : ""}${e.summary.captures ? ` \xB7 ${e.summary.captures} capture` : ""}` : e.loading ? "loading\u2026" : e.error || "")
        )
      )) : h("div", { class: "f-mute" }, app.state.pickerError ? "" : "nothing matches"));
      replace(status, app.state.pickerError ? h("div", { class: "f-banner bad" }, "Could not list push/: ", app.state.pickerError) : `${entries.length} file${entries.length === 1 ? "" : "s"} in push/` + (app.state.pickerAt ? ` \xB7 listed ${fmtAgo(app.state.pickerAt, app.now())}` : ""));
    }
    renderList();
    app.state._renderPicker = renderList;
    if (!app.state.picker) app.loadPicker(false);
    if (app.state.selected) root.appendChild(SelectedManifest(app));
    return root;
  }
  function SelectedManifest(app) {
    const s = app.state.selected;
    const card = h("div", { class: "f-card" }, h("h2", {}, s.entry.name), h("div", { class: "f-mute" }, `${s.plan.length} items \xB7 manifest hash ${s.manifest.hash}`));
    if (s.problems.length) card.appendChild(h("div", { class: "f-banner bad" }, h("b", {}, "Cannot run: "), h("div", { class: "f-err" }, s.problems.join("\n"))));
    for (const it of s.plan) {
      card.appendChild(h(
        "div",
        { class: "f-row" },
        h("div", { class: "f-grow" }, h("div", {}, `${it.idx}. ${it.name}`), h("div", { class: "f-mute" }, `${it.entity} \xB7 ${it.op}${it.targetId ? " \u2192 " + it.targetId : ""}${it.deps?.length ? " \xB7 after " + it.deps.join(", ") : ""} \xB7 keys: ${Object.keys(it.data).join(", ").slice(0, 120)}`))
      ));
    }
    const imgs = s.images || [];
    if (imgs.length) {
      card.appendChild(h("h3", {}, `Images to pick (${imgs.length})`));
      for (const name of imgs) {
        const have = app.runner.files.has(name);
        const inp = h("input", { type: "file", accept: "image/*", style: { display: "none" }, onChange: (e) => {
          const f = e.target.files[0];
          if (f) {
            app.runner.files.set(name, f);
            app.refresh();
          }
        } });
        card.appendChild(h("div", { class: "f-row" }, h("div", { class: "f-grow f-mono" }, name, " ", have ? h("span", { class: "f-pill VERIFIED" }, "picked") : h("span", { class: "f-pill FAILED" }, "missing")), h("button", { onClick: () => inp.click() }, "Pick"), inp));
      }
    }
    const missingImgs = imgs.filter((n) => !app.runner.files.has(n));
    card.appendChild(h(
      "div",
      { class: "f-actions" },
      h("button", { class: "f-primary", disabled: s.problems.length > 0 || missingImgs.length > 0, onClick: () => app.confirm(`Start job for ${s.entry.name}: ${s.plan.length} items (${s.plan.filter((i) => i.op === "create").length} creates)? This writes to the game.`, () => app.startJob()) }, "Start job"),
      h("button", { onClick: () => {
        app.state.selected = null;
        app.refresh();
      } }, "Clear")
    ));
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
    const done = job.items.filter((i) => ["VERIFIED", "FAILED", "SKIPPED"].includes(i.state)).length;
    root.append(
      h("div", {}, h("b", {}, job.manifestPath || job.jobId), " ", pill(job.state), h("span", { class: "f-mute" }, ` \xB7 started ${fmtAgo(job.startedAt, app.now())}`)),
      h("div", { class: "f-bar" + (job.state === "PAUSED" ? " warn" : "") }, h("i", { style: { width: Math.round(done / (job.items.length || 1) * 100) + "%" } }))
    );
    if (job.pause) root.appendChild(h(
      "div",
      { class: "f-banner " + (job.pause.reason === "TOO_MANY_REQUESTS" ? "bad" : "warn") },
      h("b", {}, `Paused: ${job.pause.reason}`),
      job.pause.path ? ` on ${job.pause.path}` : "",
      job.pause.until ? ` \xB7 wait ${fmtCountdown(job.pause.until, app.now())}` : "",
      job.pause.detail ? h("div", { class: "f-err" }, job.pause.detail) : null
    ));
    if (app.state.running === jobId) root.appendChild(h("div", { class: "f-banner info" }, "Running\u2026 ", app.state.runningNote || ""));
    root.appendChild(h(
      "div",
      { class: "f-actions" },
      job.state === "PAUSED" || job.state === "RUNNING" && app.state.running !== jobId && job.items.some((i) => !["VERIFIED", "FAILED", "SKIPPED"].includes(i.state)) ? h("button", { class: "f-primary", onClick: () => app.resumeJob(jobId) }, job.items.some((i) => i.state === "SENT") ? "Reconcile & resume" : "Resume") : null,
      app.state.running === jobId ? h("button", { onClick: () => app.requestPause() }, "Pause after this item") : null,
      h("button", { onClick: () => app.exportJob(jobId) }, "Export bundle")
    ));
    root.appendChild(h("h3", {}, "Budget (limited reads, per path, this minute)"));
    const st = app.budget.status();
    const used = Object.entries(st.paths).filter(([, v]) => v.used > 0);
    root.appendChild(h("div", { class: "f-card" }, used.length ? used.map(([p, v]) => h("div", { class: "f-kv" }, h("b", {}, p), h("span", {}, `${v.used} / ${v.allowance} (server ${v.serverLimit}) \xB7 resets in ${fmtCountdown(app.now() + v.resetInMs, app.now())}`))) : h("span", { class: "f-mute" }, "nothing spent"), st.tripped ? h("div", { class: "f-err" }, `TRIPPED on ${st.tripped.path} until ${new Date(st.tripped.until).toLocaleTimeString()}`) : null));
    root.appendChild(h("h3", {}, "Items"));
    for (const it of job.items) {
      const phase = it.state === "SENT" || it.state === "CONFIRMED" ? ` \xB7 phase ${it.phase}` : "";
      const row = h(
        "div",
        { class: "f-row" },
        h(
          "div",
          { class: "f-grow" },
          h("div", {}, `${it.idx}. ${it.name} `, pill(it.state), h("span", { class: "f-mute" }, ` ${it.entity}${phase}`)),
          it.entityId ? h("div", { class: "f-mono" }, it.entityId) : null,
          it.error ? h("div", { class: "f-err" }, it.error) : null,
          it.diffs && it.diffs.length ? h("details", {}, h("summary", {}, `drift on ${it.diffs.length} key(s)`), h("div", { class: "f-err" }, it.diffs.map((d) => `${d.key}: sent ${JSON.stringify(d.sent)} live ${JSON.stringify(d.live)}`).join("\n"))) : null,
          it.reconciled ? h("div", { class: "f-mute" }, it.reconciled) : null
        )
      );
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
      h("div", { class: "f-card f-kv" }, h("b", {}, "game"), h("span", {}, JSON.stringify(app.session.describe())), h("b", {}, "budget"), h("span", {}, `${app.budget.allowance} / ${app.budget.limit} per path per minute (margin ${app.budget.margin})`), h("b", {}, "persisted storage"), h("span", { id: "f-persist" }, app.state.persisted == null ? "unknown" : String(app.state.persisted))),
      h("h2", {}, "Journal"),
      h(
        "div",
        { class: "f-card" },
        h(
          "div",
          { class: "f-actions" },
          h("button", { onClick: () => app.showExport(app.journal.exportText(), "journal export") }, "Export journal as text"),
          h("button", { class: "f-danger", onClick: () => app.confirm("Delete ALL finished jobs from the journal? Open jobs are kept.", () => {
            for (const j of app.journal.listJobs()) if (j.state === "DONE" || j.state === "ABORTED") app.journal.remove(j.jobId);
            app.refresh();
          }) }, "Delete finished jobs")
        ),
        app.cacheSize ? h("div", { class: "f-mute" }, `capture cache: ${app.cacheSize}`) : null
      ),
      h("h2", {}, "About"),
      h("div", { class: "f-card f-mute" }, `forge ${app.version} \xB7 pinned to studie-tech/TheNinjaRPG@345d18ac \xB7 journal v1 \xB7 keys tnr_forge_job_v1:*, tnr_forge_sendlog_v1, tnr_forge_snap_v1:*`)
    );
    return root;
  }

  // src/ui/app.mjs
  var SCREENS = { jobs: ["Jobs", JobsScreen], manifests: ["Manifests", ManifestsScreen], run: ["Run", RunScreen], captures: ["Captures", CapturesScreen], settings: ["Settings", SettingsScreen] };
  var App = class {
    /**
     * @param {object} d  { version, storage, journal, cache, budget, reader, client, session, runner, reconciler, github, validator, now }
     */
    constructor(d) {
      Object.assign(this, d);
      this.now = d.now ?? (() => Date.now());
      this.state = { screen: "jobs", jobId: null, picker: null, selected: null, running: null, persisted: null };
      this.root = null;
    }
    mount(container, doc = document) {
      installCss(CSS, doc);
      this.root = h("div", { class: "f-app" });
      this.$top = h("div", { class: "f-top" }, h("span", { class: "f-title" }, "TNR forge"), h("span", { class: "f-ver" }, this.version));
      this.$nav = h("nav", { class: "f-nav" });
      this.$main = h("main", { class: "f-main" });
      this.$toast = h("div", { class: "f-toast" });
      this.root.append(this.$top, this.$nav, this.$main, this.$toast);
      container.appendChild(this.root);
      const open = this.journal.resumable();
      if (open.length) this.state.screen = "jobs";
      this.refresh();
      this._persist();
      return this.root;
    }
    go(screen, patch = {}) {
      Object.assign(this.state, patch, { screen });
      this.refresh();
    }
    refresh() {
      replace(this.$nav, Object.entries(SCREENS).map(([k, [label]]) => h("button", { "aria-current": this.state.screen === k ? "page" : null, onClick: () => this.go(k) }, label)));
      try {
        replace(this.$main, SCREENS[this.state.screen][1](this));
      } catch (e) {
        replace(this.$main, h("div", { class: "f-banner bad" }, h("b", {}, "This screen failed to render. "), h("div", { class: "f-err" }, String(e && e.stack || e))));
      }
    }
    toast(text, kind = "info", ms = 4e3) {
      const el = h("div", { class: "f-banner " + kind }, text);
      this.$toast.appendChild(el);
      setTimeout(() => el.remove(), ms);
    }
    fail(context, e) {
      const msg = e instanceof JournalError ? `journal: ${e.message}` : e && e.message || String(e);
      this.toast(`${context}: ${msg}`, "bad", 9e3);
      this.log(`${context}: ${msg}`);
    }
    log(msg) {
      (this.logs ??= []).push({ at: new Date(this.now()).toISOString(), msg });
    }
    confirm(text, fn) {
      if (globalThis.confirm ? globalThis.confirm(text) : true) Promise.resolve().then(fn).catch((e) => this.fail("action", e));
    }
    showExport(text, title) {
      const ta = h("textarea", { readOnly: true, value: text });
      const card = h("div", { class: "f-card" }, h("h2", {}, title), ta, h(
        "div",
        { class: "f-actions" },
        h("button", { onClick: async () => {
          try {
            await navigator.clipboard.writeText(text);
            this.toast("copied", "ok");
          } catch {
            ta.focus();
            ta.select();
            this.toast("select-all and copy", "warn");
          }
        } }, "Copy"),
        h("button", { onClick: () => card.remove() }, "Close")
      ));
      this.$main.prepend(card);
    }
    // ------------------------------------------------------------------ picker
    async loadPicker(force) {
      if (this.state.picker && !force) return;
      this.state.pickerError = null;
      try {
        const entries = (await this.github.list(GH.pushDir)).filter((e) => e.type === "file" && /\.json$/i.test(e.name)).map((e) => ({ ...e, number: manifestNumber(e.name), summary: null, loading: true }));
        entries.sort((a, b) => (b.number ?? -1) - (a.number ?? -1) || a.name.localeCompare(b.name));
        this.state.picker = entries;
        this.state.pickerAt = new Date(this.now()).toISOString();
        this.state._renderPicker && this.state._renderPicker();
        await Promise.all(entries.map(async (e) => {
          try {
            const key = `gh:${e.path}@${e.sha}`;
            const hit = await this.cache.get("github.contents", key);
            const text = hit ? hit.data : await this.github.text(e.path);
            if (!hit) await this.cache.put({ path: "github.contents", id: key, data: text });
            e.text = text;
            e.summary = manifestSummary(text);
          } catch (err) {
            e.error = err.message;
          }
          e.loading = false;
          this.state._renderPicker && this.state._renderPicker();
        }));
      } catch (e) {
        this.state.picker = this.state.picker || [];
        this.state.pickerError = e.message;
        this.state._renderPicker && this.state._renderPicker();
      }
    }
    async selectManifest(entry) {
      try {
        const text = entry.text ?? await this.github.text(entry.path);
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
        this.state.selected = { entry, text, manifest, plan, problems, images };
        this.refresh();
      } catch (e) {
        this.fail("select manifest", e instanceof ManifestError ? e : e);
      }
    }
    // ------------------------------------------------------------------ jobs
    async startJob() {
      const s = this.state.selected;
      if (!s) return;
      const jobId = `${s.entry.number ?? "m"}-${Date.now().toString(36)}`;
      try {
        this.runner.plan(s.text, { jobId, manifestPath: s.entry.path, manifestNumber: s.entry.number });
      } catch (e) {
        return this.fail("plan", e);
      }
      this.state.selected = null;
      this.go("run", { jobId });
      await this._drive(jobId, () => this.runner.run(jobId));
    }
    async resumeJob(jobId) {
      const job = this.journal.get(jobId);
      if (!this.runner.manifests.has(jobId)) {
        try {
          const text = job.manifestPath ? await this.github.text(job.manifestPath) : null;
          if (!text) throw new Error("no manifest path recorded; cannot resume");
          this.runner.attach(jobId, text);
        } catch (e) {
          return this.fail("resume: fetch manifest", e);
        }
      }
      this.go("run", { jobId });
      const hasSent = job.items.some((i) => i.state === "SENT");
      await this._drive(jobId, () => hasSent ? this.runner.resume(jobId) : this.runner.run(jobId));
    }
    async _drive(jobId, fn) {
      if (this.state.running) return this.toast("a job is already running", "warn");
      this.state.running = jobId;
      this.state.runningNote = "";
      this.refresh();
      const tick = setInterval(() => {
        if (this.state.screen === "run") this.refresh();
      }, 1500);
      try {
        const s = await fn();
        this.toast(`job ${s.state}: ${Object.entries(s.counts).map(([k, v]) => `${v} ${k.toLowerCase()}`).join(", ")}`, s.state === "DONE" ? "ok" : "warn", 8e3);
        if (s.state === "DONE") await this.exportJob(jobId, { auto: true });
      } catch (e) {
        this.fail("run", e);
      } finally {
        clearInterval(tick);
        this.state.running = null;
        this.refresh();
      }
    }
    requestPause() {
      this.toast("pause is not yet wired to the runner; use Resume later", "warn");
    }
    adopt(jobId, idx, id) {
      try {
        this.runner.adopt(jobId, idx, id);
        this.refresh();
      } catch (e) {
        this.fail("adopt", e);
      }
    }
    skip(jobId, idx) {
      try {
        this.runner.skip(jobId, idx);
        this.refresh();
      } catch (e) {
        this.fail("skip", e);
      }
    }
    /** Results bundle in the shape harvests/inbox/ already holds, committed via GitHub when Sync is on. */
    async exportJob(jobId, { auto = false } = {}) {
      const job = this.journal.get(jobId);
      const bundle = {
        builder: this.version,
        at: new Date(this.now()).toISOString(),
        cfg: "forge",
        checks: null,
        postflight: { match: job.items.filter((i) => i.verify === "match").length, diff: job.items.filter((i) => i.verify === "drift").length, unverified: job.items.filter((i) => i.verify === "unread").length },
        entries: job.items.map((i) => ({ name: i.name, srcId: i.srcId, entity: i.entity, slot: i.op, state: i.state, phase: i.phase, detail: i.error || i.reconciled || "", verdict: i.verify || null, diffs: i.diffs || [], id: i.entityId || i.targetId || null })),
        captures: [...job.capturesBefore || [], ...job.capturesAfter || []],
        idmap: JSON.parse(this.storage.getItem("tnr_bk_idmap_v1") || "{}"),
        journal: job
      };
      const name = `tnr_results_${Date.now()}.json`;
      const text = JSON.stringify(bundle, null, 1);
      const gh = readGh(this.storage);
      if (gh.on && gh.pat) {
        try {
          const r = await this.github.put(`${GH.inboxDir}/${name}`, text, `results: ${name} (forge)`);
          this.toast(`committed ${name}${r.sha ? " @" + r.sha.slice(0, 7) : ""}`, "ok");
          return;
        } catch (e) {
          this.fail("commit results", e);
        }
      }
      if (!auto || !(gh.on && gh.pat)) this.showExport(text, name);
    }
    async _persist() {
      try {
        if (navigator.storage && navigator.storage.persist) {
          this.state.persisted = await navigator.storage.persist();
          const el = document.getElementById("f-persist");
          if (el) el.textContent = String(this.state.persisted);
        }
      } catch {
      }
    }
  };

  // src/ui/takeover.mjs
  var HOST_PATH = "/forge";
  var OLD_BUILDER_CLASSES = ["k-fab", "k-pn"];
  function takeover(doc = document, win = window) {
    try {
      win.stop();
    } catch {
    }
    const html = doc.documentElement || doc.appendChild(doc.createElement("html"));
    clear(html);
    const head = h("head", {}, h("meta", { charset: "utf-8" }), h("meta", { name: "viewport", content: "width=device-width, initial-scale=1, viewport-fit=cover" }), h("title", {}, "TNR forge"));
    const body = h("body", {});
    html.append(head, body);
    const mo = new win.MutationObserver((muts) => {
      for (const m of muts) for (const n of m.addedNodes) {
        if (n && n.nodeType === 1 && OLD_BUILDER_CLASSES.some((c) => n.classList && n.classList.contains(c))) n.remove();
      }
    });
    mo.observe(body, { childList: true });
    return { html, head, body, observer: mo };
  }
  function onHostPath(loc = location) {
    return loc.pathname === HOST_PATH || loc.pathname.startsWith(HOST_PATH + "/");
  }

  // src/main.mjs
  var VERSION = "forge 0.1.0";
  var SCHEMA_URL = "https://raw.githubusercontent.com/perseverance484/tnr-tools/main/skills/building-tnr-content/data/45d_DATA_entity_schemas.json";
  async function boot(win = window) {
    if (!onHostPath(win.location)) return null;
    const { body } = takeover(win.document, win);
    const status = h("div", { style: { padding: "16px", fontFamily: "system-ui", color: "#e8eaf0", background: "#0f1115", minHeight: "100vh" } }, "TNR forge: starting\u2026");
    body.appendChild(status);
    const storage = win.localStorage;
    const fetchImpl = win.fetch.bind(win);
    const clock = () => Date.now();
    const deps = {};
    try {
      deps.journal = new Journal(storage, clock);
      deps.cache = new CaptureCache(win.indexedDB, clock);
      deps.session = new CookieSession({ fetchImpl, origin: "" });
      deps.client = new TrpcClient(deps.session, { onExchange: (r) => deps.app && deps.app.log(`${r.kind} ${r.paths.join(",")} -> ${r.status ?? r.error}`) });
      deps.budget = new Budget({ storage, clock });
      deps.reader = new CachedReader({ client: deps.client, cache: deps.cache, budget: deps.budget });
      deps.reconciler = new Reconciler({ storage, reader: deps.reader, clock });
      deps.github = new Github({ fetchImpl, storage });
      deps.uploader = new Uploader({ session: deps.session, fetchImpl });
      let schemas = null;
      try {
        const r = await fetchImpl(SCHEMA_URL, { cache: "no-cache" });
        if (r.ok) schemas = await r.json();
      } catch {
        schemas = null;
      }
      deps.validator = new Validator(schemas);
      deps.runner = new Runner({ journal: deps.journal, client: deps.client, reader: deps.reader, cache: deps.cache, budget: deps.budget, validator: deps.validator, uploader: deps.uploader, reconciler: deps.reconciler, storage, log: (m) => deps.app && deps.app.log(m) });
      deps.app = new App({ version: VERSION, storage, now: clock, ...deps });
      status.remove();
      deps.app.mount(body, win.document);
      if (deps.validator.schemaMissing) deps.app.toast("45d field schemas could not be fetched; runs are blocked until they load. Refresh to retry.", "bad", 12e3);
      return deps.app;
    } catch (e) {
      status.textContent = "";
      status.append(h("div", {}, h("b", {}, "TNR forge failed to start")), h("pre", { style: { whiteSpace: "pre-wrap", fontSize: "12px" } }, String(e && e.stack || e)));
      return null;
    }
  }
  if (typeof window !== "undefined" && typeof document !== "undefined") boot(window);
})();
