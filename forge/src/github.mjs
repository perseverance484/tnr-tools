// GitHub repository transport. This is the ONLY place a GitHub bearer token is used, and it is
// sent to api.github.com only. It never touches the game Session (spec section 7: two auth paths).
//
// Historical callers use the default `main` branch for manifest discovery and harvest result
// persistence. Quest Studio adds EXPLICIT branch-scoped operations; it must never silently turn a
// draft/build request into a write to main.

import { readGh } from "./storage/compat.mjs";

export const GH = Object.freeze({ owner: "perseverance484", repo: "tnr-tools", branch: "main", pushDir: "push", inboxDir: "harvests/inbox" });

export class GithubError extends Error {
  constructor(message, info = {}) { super(message); this.name = "GithubError"; Object.assign(this, info); }
}

function assertBranch(branch) {
  if (typeof branch !== "string" || !branch || branch.startsWith("/") || branch.endsWith("/") || branch.includes("..") || !/^[A-Za-z0-9._/-]+$/.test(branch)) {
    throw new GithubError(`unsafe branch name ${JSON.stringify(branch)}`);
  }
  return branch;
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
  _repo(path) { return `https://api.github.com/repos/${this.cfg.owner}/${this.cfg.repo}/${path}`; }
  _url(path, ref = this.cfg.branch) {
    return this._repo(`contents/${path}?ref=${encodeURIComponent(assertBranch(ref))}`);
  }

  /** List a directory: [{name, path, sha, size, type}] */
  async list(dir = this.cfg.pushDir, ref = this.cfg.branch) {
    const r = await this.fetchImpl(this._url(dir, ref), { headers: this._headers() });
    if (!r.ok) throw new GithubError(`list ${dir}: HTTP ${r.status}`, { status: r.status });
    const j = await r.json();
    if (!Array.isArray(j)) throw new GithubError(`${dir} is not a directory`);
    return j.map(({ name, path, sha, size, type }) => ({ name, path, sha, size, type }));
  }

  /** Fetch a file's raw bytes. */
  async raw(path, ref = this.cfg.branch) {
    const r = await this.fetchImpl(this._url(path, ref), { headers: this._headers("application/vnd.github.raw+json") });
    if (!r.ok) throw new GithubError(`fetch ${path}: HTTP ${r.status}`, { status: r.status });
    return r.arrayBuffer();
  }
  async text(path, ref = this.cfg.branch) { return new TextDecoder().decode(await this.raw(path, ref)); }
  async json(path, ref = this.cfg.branch) {
    const text = await this.text(path, ref);
    try { return JSON.parse(text); }
    catch (e) { throw new GithubError(`fetch ${path}: response is not JSON (${e.message})`); }
  }

  /** Read branch metadata. Returns null only for a real 404. */
  async branch(name) {
    const branch = assertBranch(name);
    const r = await this.fetchImpl(this._repo(`branches/${encodeURIComponent(branch)}`), { headers: this._headers() });
    if (r.status === 404) return null;
    if (!r.ok) throw new GithubError(`branch ${branch}: HTTP ${r.status}`, { status: r.status });
    const j = await r.json();
    return { name: j.name ?? branch, sha: j.commit?.sha ?? null };
  }

  /**
   * Create a branch from an existing base if it does not already exist. This is intentionally
   * explicit; ordinary Forge writes continue to target cfg.branch (`main`) unless a caller opts in.
   */
  async ensureBranch(name, base = this.cfg.branch) {
    if (!this._pat()) throw new GithubError("no PAT stored; Settings > GitHub");
    const branch = assertBranch(name);
    const baseBranch = assertBranch(base);
    const existing = await this.branch(branch);
    if (existing) return { ...existing, created: false };
    const source = await this.branch(baseBranch);
    if (!source?.sha) throw new GithubError(`base branch ${baseBranch} was not found`);
    const r = await this.fetchImpl(this._repo("git/refs"), {
      method: "POST",
      headers: { ...this._headers(), "content-type": "application/json" },
      body: JSON.stringify({ ref: `refs/heads/${branch}`, sha: source.sha }),
    });
    if (r.status === 422) {
      // A concurrent tab may have won the create. Re-read once rather than turning a benign race
      // into an operator error.
      const raced = await this.branch(branch);
      if (raced) return { ...raced, created: false };
    }
    if (r.status !== 201) {
      const t = await r.text();
      throw new GithubError(`create branch ${branch}: HTTP ${r.status} ${t.slice(0, 140)}`, { status: r.status });
    }
    const j = await r.json();
    return { name: branch, sha: j.object?.sha ?? source.sha, created: true };
  }

  /**
   * Create or update a file (sha-aware). Historical callers omit options and therefore retain the
   * exact `main` behavior. Quest Studio MUST pass {branch: ...} explicitly.
   * Returns {sha, htmlUrl, commitSha} or throws.
   */
  async put(path, contentText, message, { branch = this.cfg.branch } = {}) {
    if (!this._pat()) throw new GithubError("no PAT stored; Settings > GitHub");
    branch = assertBranch(branch);
    let sha = null;
    try {
      const r = await this.fetchImpl(this._url(path, branch), { headers: this._headers() });
      if (r.ok) sha = (await r.json()).sha ?? null;
    } catch { sha = null; }
    const body = { message, content: b64utf8(contentText), branch };
    if (sha) body.sha = sha;
    const r = await this.fetchImpl(this._repo(`contents/${path}`), {
      method: "PUT", headers: { ...this._headers(), "content-type": "application/json" }, body: JSON.stringify(body),
    });
    const t = await r.text();
    if (r.status !== 200 && r.status !== 201) throw new GithubError(`put ${path}: HTTP ${r.status} ${t.slice(0, 140)}`, { status: r.status });
    let j = {}; try { j = JSON.parse(t); } catch { /* ignore */ }
    return { sha: j.content?.sha ?? null, htmlUrl: j.content?.html_url ?? null, commitSha: j.commit?.sha ?? null };
  }

  /** Dispatch an allowlisted repository workflow; callers choose the workflow/ref explicitly. */
  async dispatch(workflow, { ref = this.cfg.branch, inputs = {} } = {}) {
    if (!this._pat()) throw new GithubError("no PAT stored; Settings > GitHub");
    if (typeof workflow !== "string" || !/^[A-Za-z0-9._-]+$/.test(workflow)) {
      throw new GithubError(`unsafe workflow name ${JSON.stringify(workflow)}`);
    }
    ref = assertBranch(ref);
    if (!inputs || typeof inputs !== "object" || Array.isArray(inputs)) throw new GithubError("workflow inputs must be an object");
    const r = await this.fetchImpl(this._repo(`actions/workflows/${encodeURIComponent(workflow)}/dispatches`), {
      method: "POST",
      headers: { ...this._headers(), "content-type": "application/json" },
      body: JSON.stringify({ ref, inputs }),
    });
    if (r.status !== 204) {
      const t = await r.text();
      throw new GithubError(`dispatch ${workflow}: HTTP ${r.status} ${t.slice(0, 140)}`, { status: r.status });
    }
    return { ok: true };
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
