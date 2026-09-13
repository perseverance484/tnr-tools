import { cp, mkdtemp, rm } from "node:fs/promises";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { execFileSync } from "node:child_process";

// Run after npm ci has populated its cache. Outside the repository, Node cannot
// accidentally resolve the development checkout's hoisted dependencies.
const directory = await mkdtemp(join(tmpdir(), "guide-studio-production-"));
try {
  for (const path of [
    "package.json",
    "package-lock.json",
    "compatibility/runtime",
    "src",
  ])
    await cp(path, join(directory, path), { recursive: true });
  execFileSync(
    "npm",
    [
      "ci",
      "--ignore-scripts",
      "--omit=dev",
      "--offline",
      "--no-audit",
      "--no-fund",
    ],
    { cwd: directory, stdio: "pipe" },
  );
  execFileSync(
    process.execPath,
    [
      "--input-type=module",
      "--eval",
      `
    import assert from "node:assert/strict";
    import { createRequire } from "node:module";
    import { readFile } from "node:fs/promises";
    import { htmlToPlainText } from "./compatibility/runtime/sanitize.mjs";
    import { prepareGuideHtml } from "./compatibility/runtime/guide-html.mjs";
    import { GuideArticleValidator } from "./compatibility/runtime/guide-validator.mjs";
    import { GuideCategories, GUIDE_RESERVED_SLUGS } from "./compatibility/runtime/constants.mjs";
    import { createArtifact, verifyArtifact } from "./src/artifact.mjs";
    const require = createRequire(import.meta.url);
    assert.throws(() => require.resolve("jsdom"));
    const pkg = JSON.parse(await readFile("package.json"));
    const lock = JSON.parse(await readFile("package-lock.json"));
    assert.equal(pkg.dependencies.entities, "8.0.0");
    assert.equal(lock.packages["node_modules/entities"].version, "8.0.0");
    assert.equal(htmlToPlainText("<p>A &amp; B &NotEqualTilde;</p>"), "A & B ≂̸");
    assert.deepEqual(prepareGuideHtml("<h2>A &amp; B</h2>").headings,
      [{ id: "a-b", text: "A & B", level: 2 }]);
    assert.deepEqual(GuideArticleValidator.shape.category.options, GuideCategories);
    for (const slug of GUIDE_RESERVED_SLUGS)
      assert.equal(GuideArticleValidator.shape.slug.safeParse(slug).success, false);
    assert.equal(typeof createArtifact, "function");
    assert.equal(typeof verifyArtifact, "function");
  `,
    ],
    { cwd: directory, stdio: "pipe" },
  );
  console.log(
    "Isolated npm ci --omit=dev --offline: pinned entities 8.0.0, validator, sanitizer, headings and artifact modules passed.",
  );
} catch (error) {
  throw Error(
    "Production install smoke failed: " +
      (error.stderr?.toString() || error.message),
  );
} finally {
  await rm(directory, { recursive: true, force: true });
}
