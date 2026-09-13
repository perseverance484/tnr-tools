// Production queue transitions use D1 compare-and-swap; R2 holds immutable bytes.
export class D1Store {
  constructor(db) {
    this.db = db;
  }
  async create(record) {
    await this.db
      .prepare(
        "INSERT INTO guide_submissions (id, revision, status, document) VALUES (?, ?, ?, ?)",
      )
      .bind(record.id, record.revision, record.status, JSON.stringify(record))
      .run();
  }
  async get(id) {
    const row = await this.db
      .prepare("SELECT document FROM guide_submissions WHERE id = ?")
      .bind(id)
      .first();
    return row ? JSON.parse(row.document) : null;
  }
  async list(cursor = "") {
    const rows = await this.db
      .prepare(
        "SELECT document FROM guide_submissions WHERE id > ? ORDER BY id LIMIT 51",
      )
      .bind(cursor)
      .all();
    const records = rows.results.map((r) => JSON.parse(r.document));
    return {
      records: records.slice(0, 50),
      next: records.length > 50 ? records[49].id : null,
    };
  }
  async cas(id, revision, next) {
    const result = await this.db
      .prepare(
        "UPDATE guide_submissions SET revision = ?, status = ?, document = ? WHERE id = ? AND revision = ?",
      )
      .bind(next.revision, next.status, JSON.stringify(next), id, revision)
      .run();
    return result.meta.changes === 1;
  }
}
export class MemoryStore {
  records = new Map();
  async create(r) {
    if (this.records.has(r.id)) throw Error("Duplicate");
    this.records.set(r.id, structuredClone(r));
  }
  async get(id) {
    return structuredClone(this.records.get(id) ?? null);
  }
  async list(cursor = "") {
    const all = [...this.records.values()]
      .filter((r) => r.id > cursor)
      .sort((a, b) => a.id.localeCompare(b.id));
    return {
      records: structuredClone(all.slice(0, 50)),
      next: all.length > 50 ? all[49].id : null,
    };
  }
  async cas(id, revision, next) {
    if (this.records.get(id)?.revision !== revision) return false;
    this.records.set(id, structuredClone(next));
    return true;
  }
}
export class MemoryBucket {
  objects = new Map();
  async put(key, value) {
    this.objects.set(
      key,
      typeof value === "string" ? value : new Uint8Array(value),
    );
  }
  async get(key) {
    const value = this.objects.get(key);
    if (value === undefined) return null;
    return {
      text: async () =>
        typeof value === "string" ? value : new TextDecoder().decode(value),
      arrayBuffer: async () =>
        typeof value === "string"
          ? new TextEncoder().encode(value).buffer
          : value.buffer.slice(
              value.byteOffset,
              value.byteOffset + value.byteLength,
            ),
    };
  }
}
