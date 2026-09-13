import test from "node:test";
import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import { GuideArticleValidator as actual } from "../compatibility/runtime/guide-validator.mjs";
import { GuideArticleValidator as mirror, CATEGORIES } from "../src/schema.mjs";
import { createArtifact } from "../src/artifact.mjs";
import { registry, aerathiel, origin, id } from "./helpers.mjs";
import { sha256 } from "../src/hash.mjs";
const good = (await createArtifact(aerathiel, registry, origin, id)).game;
test("pinned upstream validator and mirror agree at every boundary", () => {
  const cases = [
    good,
    ...CATEGORIES.map((category) => ({ ...good, category })),
    ...[
      "new",
      "edit",
      "CAPS",
      "bad space",
      "a".repeat(81),
      "with-hyphen",
      "",
    ].map((slug) => ({ ...good, slug })),
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
  }))
    for (const value of [
      undefined,
      null,
      "",
      "x".repeat(max),
      "x".repeat(max + 1),
    ])
      cases.push({ ...good, [field]: value });
  for (const sortOrder of [-1, 0, 10000, 10001, 1.5, "42", "x", null])
    cases.push({ ...good, sortOrder });
  for (const faq of [
    [],
    null,
    [{ question: " Q ", answer: " A " }],
    Array(13).fill({ question: "q", answer: "a" }),
    [{ question: "", answer: "a" }],
  ])
    cases.push({ ...good, faq });
  for (const c of cases) {
    const a = actual.safeParse(c),
      b = mirror.safeParse(c);
    assert.equal(b.success, a.success);
    if (a.success) assert.deepEqual(a.data, b.data);
  }
  assert.ok(actual.safeParse(good).success);
  assert.equal(good.category, "bloodlines");
  assert.equal(good.published, false);
  assert.equal(good.relatedBloodlineId, registry.templates[0].bloodlineId);
});
test("pinned source copies keep recorded byte hashes", async () => {
  const manifest = JSON.parse(
    await readFile("compatibility/source-manifest.json"),
  );
  for (const [f, hash] of Object.entries(manifest.files))
    assert.equal(await sha256(await readFile("compatibility/" + f)), hash, f);
});
