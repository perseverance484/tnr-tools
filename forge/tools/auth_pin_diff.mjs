// Is Forge's auth classification the same at two game-source commits?
//
//   node tools/auth_pin_diff.mjs <checkout-a> <checkout-b> [--sha-a <sha>] [--sha-b <sha>]
//
// No network: both arguments are existing checkouts, read only. Exits 0 when every procedure in
// src/transport/procedures.mjs carries the same publicProcedure/protectedProcedure class at both
// commits, 1 when any of them differs.
//
// WHY THIS EXISTS. The auth gate decides whether a call needs a signed-in session, and it reads
// PROCEDURES[path].auth to do it. That table was transcribed from a client-contract audit taken
// at one commit, and a task brief may pin a different one; independent review FPA-3 rejected the
// first protected-auth handoff for asserting task-pin compliance while deriving the table
// elsewhere. Prose cannot settle that, so this re-derives the classification from both checkouts
// and prints the comparison. It is the auth-class counterpart to pin_relevance.mjs, which answers
// the broader "did anything forge relies on move" question.
//
// A procedure that exists at only one commit is reported and is NOT a failure: an added procedure
// Forge does not call cannot change what Forge sends. A procedure whose CLASS moved is a failure,
// in either direction - public -> protected means the gate would wave through a call the server
// will refuse, and protected -> public means the gate blocks work that would have succeeded.

import { execFileSync } from "node:child_process";
import { readFileSync, existsSync } from "node:fs";
import { join, dirname } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));

// router name as Forge addresses it -> the file it lives in. gameAsset is mounted from asset.ts
// (root.ts `gameAsset: gameAssetRouter`), which is why the two names differ.
const ROUTER_FILES = Object.freeze({
  jutsu: "jutsu.ts", item: "item.ts", quests: "quests.ts", profile: "profile.ts",
  ai: "ai.ts", gameAsset: "asset.ts", bloodline: "bloodline.ts",
});
const DECL = /^ {2}([A-Za-z0-9_]+):\s*(publicProcedure|protectedProcedure)\b/;

/**
 * Procedure declarations in one router file: `  name: publicProcedure` at exactly the router
 * literal's indentation. Deeper indentation is something else (an inner builder, a comment
 * example) and is deliberately not matched. Exported so the test suite pins this parser without
 * needing two game checkouts, and so there is one copy of it rather than two.
 */
export function parseRouterDecls(text) {
  const out = {};
  for (const line of text.split("\n")) { const m = DECL.exec(line); if (m) out[m[1]] = m[2]; }
  return out;
}

/** The declared auth class of every procedure in the seven content routers, at one checkout. */
export function authTable(root, sha = null) {
  const out = {};
  for (const [router, file] of Object.entries(ROUTER_FILES)) {
    const path = `app/src/server/api/routers/${file}`;
    let text;
    if (sha) {
      try { text = execFileSync("git", ["-C", root, "show", `${sha}:${path}`], { encoding: "utf8", maxBuffer: 64 * 1024 * 1024 }); }
      catch { continue; }
    } else {
      const abs = join(root, path);
      if (!existsSync(abs)) continue;
      text = readFileSync(abs, "utf8");
    }
    for (const [proc, klass] of Object.entries(parseRouterDecls(text))) out[`${router}.${proc}`] = klass;
  }
  return out;
}

/** Forge's own table: path -> "public" | "protected". */
export function forgeTable(file = join(here, "..", "src", "transport", "procedures.mjs")) {
  const src = readFileSync(file, "utf8");
  const out = {};
  const re = /"([A-Za-z]+\.[A-Za-z]+)":\s*\{[^}]*auth:\s*"(public|protected)"/g;
  for (let m; (m = re.exec(src)); ) out[m[1]] = m[2];
  return out;
}

const EXPECTED = { public: "publicProcedure", protected: "protectedProcedure" };

export function compareAuthPins({ rootA, shaA = null, rootB, shaB = null, forge = forgeTable() }) {
  const a = authTable(rootA, shaA);
  const b = authTable(rootB, shaB);
  const rows = [];
  for (const [path, klass] of Object.entries(forge).sort(([x], [y]) => x.localeCompare(y))) {
    const want = EXPECTED[klass];
    rows.push({ path, forge: klass, a: a[path] ?? null, b: b[path] ?? null, ok: a[path] === want && b[path] === want });
  }
  // whole-surface sweep, so a reclassification Forge does not currently call is still visible
  const moved = [];
  const added = [];
  for (const path of new Set([...Object.keys(a), ...Object.keys(b)])) {
    if (a[path] === b[path]) continue;
    (a[path] && b[path] ? moved : added).push({ path, a: a[path] ?? null, b: b[path] ?? null });
  }
  return { rows, moved: moved.sort((x, y) => x.path.localeCompare(y.path)), added: added.sort((x, y) => x.path.localeCompare(y.path)), counts: { a: Object.keys(a).length, b: Object.keys(b).length } };
}

if (import.meta.url === `file://${process.argv[1]}`) {
  const args = process.argv.slice(2);
  const flag = (name) => { const i = args.indexOf(name); return i === -1 ? null : args[i + 1]; };
  const positional = args.filter((v, i) => !v.startsWith("--") && !(i > 0 && args[i - 1].startsWith("--")));
  const [rootA, rootB] = positional;
  if (!rootA || !rootB || !existsSync(rootA) || !existsSync(rootB)) {
    console.error("usage: auth_pin_diff.mjs <checkout-a> <checkout-b> [--sha-a <sha>] [--sha-b <sha>]");
    process.exit(2);
  }
  const shaA = flag("--sha-a");
  const shaB = flag("--sha-b");
  const label = (sha) => (sha ? sha.slice(0, 8) : "worktree");
  const r = compareAuthPins({ rootA, shaA, rootB, shaB });
  console.log(`${label(shaA)}: ${r.counts.a} procedures declared    ${label(shaB)}: ${r.counts.b} procedures declared\n`);
  for (const row of r.rows) {
    console.log(`  ${row.ok ? "ok  " : "DIFF"} ${row.path.padEnd(26)} forge=${row.forge.padEnd(9)} ${label(shaA)}=${row.a} ${label(shaB)}=${row.b}`);
  }
  const bad = r.rows.filter((row) => !row.ok);
  console.log(`\n${bad.length} disagreement(s) across ${r.rows.length} Forge paths`);
  for (const m of r.moved) console.log(`  MOVED  ${m.path}: ${label(shaA)}=${m.a} -> ${label(shaB)}=${m.b}`);
  for (const m of r.added) console.log(`  only-at-one-pin  ${m.path}: ${label(shaA)}=${m.a} ${label(shaB)}=${m.b} (not called by forge unless listed above)`);
  console.log(`${r.moved.length} procedure(s) changed auth class across the whole content surface`);
  process.exit(bad.length || r.moved.length ? 1 : 0);
}
