// The bundle comment stripper (tools/strip_comments.mjs).
//
// build.mjs already proves each build with esbuild's own parser, so these tests exist for the
// cases that oracle would only catch AFTER someone changed the source in a way that happened to
// contain one: a regex holding a slash, a comment marker inside a string, a nested template. Each
// case is checked twice - the expected text, and the same esbuild normalisation the build uses, so
// a test that agrees with a wrong expectation still fails.
import { test } from "node:test";
import assert from "node:assert/strict";
import { transform } from "esbuild";
import { stripComments } from "../tools/strip_comments.mjs";

const norm = async (t) => (await transform(t, { minifyWhitespace: true, legalComments: "none" })).code;

/** strip, then assert the program is unchanged in esbuild's eyes. */
async function equivalent(source) {
  const stripped = stripComments(source);
  assert.equal(await norm(stripped), await norm(source), "stripping changed the program:\n" + stripped);
  return stripped;
}

test("comments go and code stays", async () => {
  const out = await equivalent(`// leading\nconst a = 1; // trailing\n/** doc */\nfunction f() { /* inline */ return a; }\n`);
  assert.ok(!out.includes("leading"));
  assert.ok(!out.includes("trailing"));
  assert.ok(!out.includes("doc"));
  assert.ok(!out.includes("inline"));
  assert.match(out, /const a = 1;/);
  assert.match(out, /return a;/);
});

test("a comment marker inside a string is not a comment", async () => {
  const out = await equivalent(`const u = "https://x/y"; const s = '/* not a comment */'; const d = "// neither";\n`);
  assert.ok(out.includes("https://x/y"));
  assert.ok(out.includes("/* not a comment */"));
  assert.ok(out.includes("// neither"));
});

test("a regex literal holding slashes survives", async () => {
  // the shapes that actually appear in src/: a character class containing a slash, an escaped
  // slash, and a regex immediately after `return`
  const out = await equivalent(
    `const a = /[/]/.test(x);\nconst b = /a\\/b/g;\nfunction f() { return /^\\/forge$/.test(p); }\nconst c = (1 + 2) / 3 / 4;\n`,
  );
  assert.ok(out.includes("/[/]/"));
  assert.ok(out.includes("/a\\/b/g"));
  assert.ok(out.includes("(1 + 2) / 3 / 4"));
});

test("division after a value is not read as a regex", async () => {
  await equivalent(`const pct = total / count; const q = arr[0] / obj.n / f(1) / 2; // gone\n`);
});

test("template literals, substitutions and nesting", async () => {
  const out = await equivalent(
    "const t = `a ${x} b`;\n" +
    "const u = `outer ${ `inner ${y}` } end`;\n" +
    "const v = `${ obj[`k`] } // not a comment`;\n" +
    "const w = `braces ${ (() => { return 1; })() } done`; // gone\n",
  );
  assert.ok(out.includes("// not a comment"), "a comment marker in template TEXT stays");
  assert.ok(!out.includes("// gone"));
});

test("a comment inside a template substitution is still a comment", async () => {
  const out = await equivalent("const t = `a ${ /* drop me */ x } b`;\n");
  assert.ok(!out.includes("drop me"));
  assert.ok(out.includes("`a ${"));
});

test("a closing backtick is not read as an opening one", async () => {
  // the first version of the stripper checked the generic backtick case before the in-template
  // case, so every closing backtick opened a new template and the rest of the file was swallowed.
  // superjson's prototype-pollution message is where the real build caught it.
  const out = await equivalent(
    "throw new Error(`Detected property ${i}. Remove it.`);\nconst after = 1; // gone\n",
  );
  assert.ok(!out.includes("// gone"));
  assert.match(out, /const after = 1;/);
});

test("a line that was only a comment is removed, a line that was already blank is kept", () => {
  const out = stripComments("const a = 1;\n// whole line\n\nconst b = 2;\n");
  assert.equal(out, "const a = 1;\n\nconst b = 2;\n");
});

test("an unterminated block comment does not run off the end", async () => {
  assert.equal(stripComments("const a = 1;\n/* never closed\n").trimEnd(), "const a = 1;");
});

test("the built bundle carries no comments but the source still does", async () => {
  const { readFileSync } = await import("node:fs");
  const bundle = readFileSync(new URL("../../forge_bundle.js", import.meta.url), "utf8");
  // the banner is prepended after stripping and is the only comment the artifact keeps
  const body = bundle.split("\n").filter((l) => !l.startsWith("// ")).join("\n");
  assert.ok(!/^\s*\/\*\*/m.test(body), "JSDoc survived into the bundle body");
  assert.ok(!/^\s*\/\/ /m.test(body), "a line comment survived into the bundle body");
  const source = readFileSync(new URL("../src/runner/validate.mjs", import.meta.url), "utf8");
  assert.match(source, /^\s*\/\*\*/m, "the SOURCE must keep its documentation");
});
