import test from "node:test";
import assert from "node:assert/strict";
import { registry, aerathiel, nightParade, origin, id } from "./helpers.mjs";
import { assertTemplate } from "../src/template.mjs";
import { newDraft, validateDraft, validateHighlight } from "../src/schema.mjs";
import { normalizeEffect, effectText } from "../src/effects.mjs";
import { renderGuide, previewDocument } from "../src/render.mjs";
import {
  createArtifact,
  verifyArtifact,
  exportZip,
  readPackageZip,
} from "../src/artifact.mjs";
import { sha256 } from "../src/hash.mjs";
import { JSDOM } from "jsdom";
import { readFile } from "node:fs/promises";
import sanitize, {
  htmlToModerationText,
} from "../compatibility/runtime/sanitize.mjs";
import { prepareGuideHtml } from "../compatibility/runtime/guide-html.mjs";
for (const fixture of [aerathiel, nightParade])
  test(
    fixture.template.slug +
      " complete foundation independent of build; reproducible export",
    async () => {
      const t = registry.templates.find(
        (t) => t.slug === fixture.template.slug,
      );
      assertTemplate(t, registry);
      assert.equal(t.coreKit.length, 5);
      const blank = await renderGuide(newDraft(t, registry), registry, origin),
        full = await createArtifact(fixture, registry, origin, id);
      assert.deepEqual(
        blank.assets.filter((a) => a.role === "core-kit").map((a) => a.sha256),
        full.rendered.assets
          .filter((a) => a.role === "core-kit")
          .map((a) => a.sha256),
      );
      assert.equal(
        full.rendered.assets.filter((a) => a.role === "build").length,
        fixture.loadout.length,
      );
      assert.equal(
        full.rendered.assets.filter((a) => a.role === "summon").length,
        t.slug === "night-parade" ? 3 : 0,
      );
      assert.equal(
        full.rendered.assets.filter((a) => a.role === "summon-ability").length,
        t.slug === "night-parade" ? 4 : 0,
      );
      assert.equal(
        sanitize(full.game.content),
        full.game.content,
        "native sanitizer byte identity",
      );
      assert.equal(
        prepareGuideHtml(full.game.content).html,
        full.game.content,
        "native heading preparation identity",
      );
      for (const j of fixture.loadout)
        assert.ok(
          htmlToModerationText(full.game.content).includes(j.howIUseIt),
          "every player note remains native accessible/moderated text",
        );
      assert.ok(
        full.game.content.indexOf("bloodline-kit") <
          full.game.content.indexOf("my-build"),
      );
      assert.ok(
        full.game.content.indexOf("my-build") <
          full.game.content.indexOf('id="strategy"'),
      );
      assert.deepEqual(
        full,
        await createArtifact(fixture, registry, origin, id),
      );
      await verifyArtifact(full);
      const zip = exportZip(full, { signature: "test-only" }),
        parsed = await readPackageZip(zip);
      assert.deepEqual(parsed.artifact.files, full.files);
      assert.equal(
        await sha256(zip),
        await sha256(exportZip(full, { signature: "test-only" })),
      );
      const dom = new JSDOM(previewDocument(full.rendered));
      assert.equal(
        dom.window.document.querySelectorAll("img").length,
        full.rendered.assets.length,
      );
      assert.ok(
        [...dom.window.document.querySelectorAll("img")].every(
          (i) => i.src.startsWith("data:") && i.alt,
        ),
      );
    },
  );
test("Black Thorn Rose target/direction regression", () => {
  const j = registry.jutsu.find((j) => j.name === "Kinjutsu: Black Thorn Rose");
  assert.ok(j);
  assert.deepEqual(
    j.effects.map((e) => [e.label, e.target, e.direction, e.value]),
    [
      ["HEALING REDUCTION", "enemy", "reduction", 50],
      ["DAMAGE TAKEN", "self", "reduction", 30],
    ],
  );
  assert.ok(
    !j.effects.some((e) =>
      ["DAMAGE", "POWER", "DAMAGE GIVEN"].includes(e.label),
    ),
  );
  assert.ok(j.effects.every((e) => e.statDirection === "offence"));
});
test("unknown mechanics fail closed; chance, healing, and self departure retain semantics", () => {
  assert.throws(
    () => normalizeEffect({ type: "future-balance-tag" }, {}),
    /Unmapped/,
  );
  const hunger = registry.jutsu.find((j) => j.name === "Unbearable Hunger");
  assert.ok(
    hunger.effects.some(
      (e) => e.label === "SUMMON DEPARTURE" && e.target === "self",
    ),
  );
  assert.ok(
    hunger.effects.some(
      (e) => e.label === "POOL COST" && e.pools.includes("Health"),
    ),
  );
  const shield = registry.jutsu
    .flatMap((j) => j.effects)
    .find((e) => e.type === "shield");
  assert.match(effectText(shield), /health.*chance/);
});
test("incomplete templates are refused, exact versions enforced, unknown author mechanic fields rejected", () => {
  const r = structuredClone(registry);
  r.templates[0].coreKit.pop();
  assert.throws(() => assertTemplate(r.templates[0], r), /membership/);
  assert.throws(
    () => validateDraft({ ...aerathiel, catalogVersion: "old" }, registry),
    /different catalog/,
  );
  assert.throws(() =>
    validateDraft({ ...aerathiel, mechanics: { damage: 9000 } }, registry),
  );
  assert.throws(
    () =>
      validateDraft(
        { ...aerathiel, loadout: [aerathiel.loadout[0], aerathiel.loadout[0]] },
        registry,
      ),
    /twice/,
  );
  assert.throws(
    () =>
      validateDraft(
        {
          ...aerathiel,
          loadout: [
            {
              jutsuId: registry.jutsu.find((j) => j.type === "AI").id,
              howIUseIt: "x",
            },
          ],
        },
        registry,
      ),
    /not available/,
  );
});
test("optional chapter omission and template rename/reorder/hide are real renderer behavior", async () => {
  const r = structuredClone(registry),
    t = r.templates[0];
  t.chapters.reverse();
  t.chapters.find((c) => c.id === "philosophy").title =
    "A custom thematic chapter";
  t.chapters.find((c) => c.id === "opening").hidden = true;
  const d = structuredClone(aerathiel);
  delete d.strategy.opening;
  delete d.strategy.mistakes;
  const { html } = await renderGuide(d, r, origin);
  assert.ok(!html.includes("chapter-opening"));
  assert.ok(!html.includes("chapter-mistakes"));
  assert.match(html, /A custom thematic chapter/);
  assert.ok(
    html.indexOf("chapter-matchups") < html.indexOf("chapter-philosophy"),
  );
});
test("authored markup remains inert in HTML, SVG, and preview", async () => {
  const d = structuredClone(aerathiel),
    attack =
      "<img src=x onerror=alert(1)><script>alert(1)</script> & \" ' " +
      String.fromCharCode(0xd800);
  d.author = "Safe Author";
  d.strategy.philosophy = attack;
  d.loadout[0].howIUseIt = attack;
  const r = await renderGuide(d, registry, origin),
    doc = new JSDOM(previewDocument(r));
  assert.equal(
    doc.window.document.querySelectorAll("script,[onerror]").length,
    0,
  );
  assert.ok(doc.window.document.body.textContent.includes("<script>"));
  assert.ok(r.assets.every((a) => !a.body?.includes("onerror=")));
});
test("highlight validates real WebP and rejects active/oversized/malformed content", async () => {
  const bytes = await readFile("public" + registry.templates[0].hero.url),
    data = "data:image/webp;base64," + bytes.toString("base64");
  assert.ok(validateHighlight({ data }).width > 0);
  for (const bad of [
    "data:image/svg+xml;base64,PHN2Zz4=",
    data.slice(0, -4),
    "data:image/webp;base64," + Buffer.alloc(350001).toString("base64"),
  ])
    assert.throws(() => validateHighlight({ data: bad }));
});

test("staff preview and export cannot disagree through altered snapshot aliases", async () => {
  const a = await createArtifact(aerathiel, registry, origin, id);
  a.rendered.html = "<p>A different guide</p>";
  await assert.rejects(verifyArtifact(a), /Preview content differs/);
});

test("summon utility and damage flags remain in the complete normalized foundation", async () => {
  const t = registry.templates.find((t) => t.slug === "night-parade"),
    r = await renderGuide(newDraft(t, registry), registry, origin);
  assert.equal(r.assets.filter((a) => a.role === "summon-link").length, 3);
  assert.equal(r.assets.filter((a) => a.role === "summon-utility").length, 1);
  const r2 = structuredClone(registry);
  r2.templates.find(
    (t) => t.slug === "night-parade",
  ).modules[0].summons[0].utilityJutsuIds = [];
  assert.throws(
    () => assertTemplate(r2.templates[1], r2),
    /incomplete summon abilities/,
  );
  const cleave = registry.jutsu
    .find((j) => j.name === "Tempest Cleave")
    .effects.find((e) => e.type === "damage");
  assert.equal(cleave.allowBloodlineDamageDecrease, false);
  assert.equal(cleave.damageModifier, 0);
  assert.deepEqual(cleave.generalTypes, ["Highest"]);
  assert.match(effectText(cleave), /bloodline damage decreases excluded/);
  assert.doesNotMatch(effectText(cleave), /damage multiplier 0/);
});
