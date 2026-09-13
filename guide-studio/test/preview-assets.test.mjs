import test from "node:test";
import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import browser from "../catalog/browser.v1.json" with { type: "json" };
import { registry, aerathiel, nightParade, origin, id } from "./helpers.mjs";
import { createPreviewLoader } from "../src/preview-assets.mjs";
import { newDraft, validateDraft } from "../src/schema.mjs";
import { renderGuide } from "../src/render.mjs";
import { createArtifact } from "../src/artifact.mjs";

test("browser projection preserves canonical records/version without inline image bytes", () => {
  const { imageData, ...canonical } = registry;
  const { assetHashes, ...projected } = browser;
  assert.deepEqual(projected, canonical);
  assert.equal(browser.imageData, undefined);
  assert.deepEqual(
    Object.keys(assetHashes).sort(),
    Object.keys(imageData).sort(),
  );
  assert.deepEqual(
    validateDraft(aerathiel, browser),
    validateDraft(aerathiel, registry),
  );
});

for (const draft of [aerathiel, nightParade])
  test(
    draft.template.slug +
      " loads only required art; preview and export remain byte-identical",
    async () => {
      const requests = [];
      const loader = createPreviewLoader(browser, async (url, options) => {
        requests.push(url);
        assert.match(url, /^\/assets\/[a-f0-9]{24}\.webp$/);
        assert.equal(options.credentials, "omit");
        assert.equal(options.redirect, "error");
        return new Response(await readFile("public" + url));
      });
      assert.equal(requests.length, 0);
      const t = browser.templates.find((t) => t.slug === draft.template.slug);
      const foundation = newDraft(t, browser);
      const [loaded] = await Promise.all([
        loader(foundation),
        loader(foundation),
      ]);
      assert.equal(
        new Set(requests).size,
        requests.length,
        "concurrent requests are shared",
      );
      assert.equal(requests.length, t.slug === "aerathiel" ? 6 : 17);
      const empty = await renderGuide(foundation, loaded, origin, id);
      assert.deepEqual(
        empty,
        await renderGuide(foundation, registry, origin, id),
      );
      const complete = await loader(draft);
      const artifact = await createArtifact(draft, complete, origin, id);
      assert.deepEqual(
        artifact,
        await createArtifact(draft, registry, origin, id),
      );
      assert.deepEqual(
        empty.assets.filter((a) => a.role === "core-kit"),
        artifact.rendered.assets.filter((a) => a.role === "core-kit"),
      );
      const usedArt = Object.entries(registry.imageData)
        .filter(([, data]) =>
          artifact.rendered.assets.some((a) => a.body?.includes(data)),
        )
        .map(([url]) => url);
      assert.deepEqual(
        [...requests].sort(),
        usedArt.sort(),
        "only artwork present in the final guide is fetched",
      );
      const count = requests.length;
      await loader({ ...draft, author: "Another player" });
      assert.equal(
        requests.length,
        count,
        "editing prose reuses verified artwork",
      );
    },
  );

test("failed or tampered artwork is refused and can be retried", async () => {
  for (const failure of ["missing", "tampered"]) {
    let fail = true;
    const hero = browser.templates[0].hero.url;
    const loader = createPreviewLoader(browser, async (url) => {
      if (fail && url === hero)
        return failure === "missing"
          ? new Response("", { status: 404 })
          : new Response("changed bytes");
      return new Response(await readFile("public" + url));
    });
    await assert.rejects(loader(aerathiel), /artwork/);
    fail = false;
    const loaded = await loader(aerathiel);
    assert.equal(loaded.imageData[hero], registry.imageData[hero]);
  }
});

test("public projection cannot render unresolved or off-origin official images", async () => {
  await assert.rejects(
    renderGuide(aerathiel, browser, origin),
    /Load official artwork/,
  );
  const changed = structuredClone(browser);
  const hero = changed.templates[0].hero;
  hero.url = "https://untrusted.invalid/asset.webp";
  changed.assetHashes[hero.url] = hero.sha256;
  let requests = 0;
  await assert.rejects(
    createPreviewLoader(changed, async () => {
      requests++;
    })(aerathiel),
    /not in this catalog/,
  );
  assert.equal(
    requests,
    0,
    "reject unapproved URLs before fetching any artwork",
  );
});
