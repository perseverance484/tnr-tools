import test from "node:test";
import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import { GuideArticleValidator as actual } from "../compatibility/runtime/guide-validator.mjs";
import {
  GuideCategories,
  GUIDE_RESERVED_SLUGS,
} from "../compatibility/runtime/constants.mjs";
import { ZodError } from "zod";
import { createArtifact, verifyArtifact } from "../src/artifact.mjs";
import { registry, aerathiel, origin, id } from "./helpers.mjs";
import { sha256, stableStringify } from "../src/hash.mjs";
const artifact = await createArtifact(aerathiel, registry, origin, id);
const good = artifact.game;
const cases = [
  [good, true],
  ...GuideCategories.map((category) => [{ ...good, category }, true]),
  ...GUIDE_RESERVED_SLUGS.map((slug) => [{ ...good, slug }, false]),
  ...["CAPS", "bad space", "a".repeat(81), ""].map((slug) => [
    { ...good, slug },
    false,
  ]),
  [{ ...good, slug: "with-hyphen" }, true],
  [{ ...good, category: "unsupported-category" }, false],
];
for (const [field, max] of Object.entries({
  title: 191,
  subtitle: 255,
  excerpt: 500,
  seoTitle: 70,
  seoDescription: 160,
  reviewNotes: 4000,
  relatedBloodlineId: 191,
  content: 200000,
})) {
  const required = ["title", "content"].includes(field);
  for (const value of [undefined, null, ""])
    cases.push([{ ...good, [field]: value }, !required]);
  cases.push([{ ...good, [field]: "x".repeat(max) }, true]);
  cases.push([{ ...good, [field]: "x".repeat(max + 1) }, false]);
}
for (const [sortOrder, valid] of [
  [-1, false],
  [0, true],
  [10000, true],
  [10001, false],
  [1.5, false],
  ["42", true],
  ["x", false],
  [null, true],
])
  cases.push([{ ...good, sortOrder }, valid]);
for (const [faq, valid] of [
  [[], true],
  [null, true],
  [[{ question: " Q ", answer: " A " }], true],
  [Array(13).fill({ question: "q", answer: "a" }), false],
  [[{ question: "", answer: "a" }], false],
])
  cases.push([{ ...good, faq }, valid]);

test("native contract boundaries use the pinned categories and reserved slugs", () => {
  assert.deepEqual(actual.shape.category.options, GuideCategories);
  for (const [input, valid] of cases)
    assert.equal(actual.safeParse(input).success, valid);
  assert.equal(good.category, "bloodlines");
  assert.equal(good.published, false);
  assert.equal(good.relatedBloodlineId, registry.templates[0].bloodlineId);
});

// Recompute every file hash so malformed native fields reach the production
// validator instead of being rejected earlier by package integrity checks.
async function packageWithGame(game) {
  const files = { ...artifact.files };
  files["game-guide.json"] = stableStringify(game) + "\n";
  files["content.html"] = game.content || "";
  const { packageHash, ...meta } = structuredClone(artifact.metadata);
  meta.contentHash = await sha256(files["content.html"]);
  for (const name of Object.keys(meta.files))
    meta.files[name] = await sha256(files[name]);
  meta.packageHash = await sha256(stableStringify(meta));
  files["metadata.json"] = stableStringify(meta) + "\n";
  return { files };
}

test("production artifact verification enforces pinned native rules after hashes pass", async () => {
  for (const [input, valid] of cases) {
    if (
      !valid &&
      input.content !== undefined &&
      input.content !== null &&
      input.content !== ""
    )
      await assert.rejects(
        verifyArtifact(await packageWithGame(input)),
        ZodError,
      );
  }
  const verified = await verifyArtifact(
    await packageWithGame({ ...good, title: " A guide ", sortOrder: "42" }),
  );
  assert.equal(verified.game.title, "A guide");
  assert.equal(verified.game.sortOrder, 42);
  for (const category of GuideCategories.filter((c) => c !== "bloodlines"))
    await assert.rejects(
      verifyArtifact(await packageWithGame({ ...good, category })),
      /Invalid approved draft guide/,
    );
});
test("pinned source copies keep recorded byte hashes", async () => {
  const manifest = JSON.parse(
    await readFile("compatibility/source-manifest.json"),
  );
  for (const [f, hash] of Object.entries(manifest.files))
    assert.equal(await sha256(await readFile("compatibility/" + f)), hash, f);
});
