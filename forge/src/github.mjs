// GitHub contents API: the manifest picker's listing and file fetch, and the results-bundle
// commit to harvests/inbox/. This is the ONLY place a bearer token is used, and it is sent to
// api.github.com only. It never touches the game Session (spec section 7: two auth paths).

import { readGh } from "./storage/compat.mjs";

export const GH = Object.freeze({ owner: "perseverance484", repo: "tnr-tools", branch: "main", pushDir: "push", inboxDir: "harvests/inbox" });

export class GithubError extends Error {
  constructor(message, info = {}) { super(message); this.name = "GithubError"; Object.assign(this, info); }
}

export class Github {
  /**
   * @param {object} o
   * @param {(url: string, init: object) => Promise<Response>} o.fetchImpl  a plain fetch (NOT the Session)
   * @param {Storage} o.storage  where tnr_bk_gh_v1 lives
   */
  constructor({ fetchImpl, storage, config = GH }) { this.fetchImpl = fetchImpl; this.storage = storage; this.cfg = config; }

  _pat() { const g = readGh(this.storage); return g && g.pat ? g.pat : null; }
  _headers(accept = "application/vnd.github+json") {
    const h = { accept, "x-github-api-version": "2022-11-28" };
    const pat = this._pat();
    if (pat) h.authorization = "Bearer " + pat;
    return h;
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
  async text(path, ref) { return new TextDecoder().decode(await this.raw(path, ref)); }

  /** Create or update a file (sha-aware). Returns {sha, htmlUrl} or throws. */
  async put(path, contentText, message) {
    if (!this._pat()) throw new GithubError("no PAT stored; Settings > GitHub");
    let sha = null;
    try {
      const r = await this.fetchImpl(this._url(path), { headers: this._headers() });
      if (r.ok) sha = (await r.json()).sha ?? null;
    } catch { sha = null; }
    const body = { message, content: b64utf8(contentText), branch: this.cfg.branch };
    if (sha) body.sha = sha;
    const r = await this.fetchImpl(`https://api.github.com/repos/${this.cfg.owner}/${this.cfg.repo}/contents/${path}`, {
      method: "PUT", headers: { ...this._headers(), "content-type": "application/json" }, body: JSON.stringify(body),
    });
    const t = await r.text();
    if (r.status !== 200 && r.status !== 201) throw new GithubError(`put ${path}: HTTP ${r.status} ${t.slice(0, 140)}`, { status: r.status });
    let j = {}; try { j = JSON.parse(t); } catch { /* ignore */ }
    return { sha: j.content?.sha ?? null, htmlUrl: j.content?.html_url ?? null };
  }
}

export function b64utf8(s) {
  const bytes = new TextEncoder().encode(s);
  let bin = "";
  for (let i = 0; i < bytes.length; i += 0x8000) bin += String.fromCharCode.apply(null, bytes.subarray(i, i + 0x8000));
  return btoa(bin);
}

/** The manifest's own number from its filename: "45_mission_ai.json" -> 45. */
export function manifestNumber(name) { const m = /^(\d+)[a-z]?_/i.exec(name); return m ? Number(m[1]) : null; }

/** Cheap summary of a manifest for the picker row. */
export function manifestSummary(text) {
  try {
    const m = JSON.parse(text);
    const items = Array.isArray(m.items) ? m.items : Array.isArray(m.jutsu) ? m.jutsu : [];
    const caps = (m.capture && ((m.capture.before || []).length + (m.capture.after || []).length)) || 0;
    const title = typeof m._note === "string" ? m._note.split(/\.\s|\n/)[0].slice(0, 80) : (items[0] && items[0].name) || "";
    const creates = items.filter((i) => i && i.slot === "create").length;
    return { ok: true, title, items: items.length, creates, captures: caps };
  } catch (e) { return { ok: false, title: "(not JSON: " + e.message.slice(0, 40) + ")", items: 0, creates: 0, captures: 0 }; }
}
