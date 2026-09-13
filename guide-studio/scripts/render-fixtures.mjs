import { mkdir, writeFile, rm } from "node:fs/promises";
import { createArtifact } from "../src/artifact.mjs";
import { previewDocument } from "../src/render.mjs";
import registry from "../catalog/catalog.v1.json" with { type: "json" };
import aerathiel from "../fixtures/aerathiel.submission.json" with { type: "json" };
import night from "../fixtures/night-parade.submission.json" with { type: "json" };
await mkdir("test-output/fixtures", { recursive: true });
for (const draft of [aerathiel, night]) {
  const artifact = await createArtifact(
    draft,
    registry,
    "https://guide-studio.example.org",
    "a2345678-1234-1234-1234-123456789abc",
  );
  const root = "test-output/fixtures/" + draft.template.slug;
  await rm(root, { recursive: true, force: true });
  await mkdir(root, { recursive: true });
  await writeFile(root + "/preview.html", previewDocument(artifact.rendered));
  for (const [name, body] of Object.entries(artifact.files))
    await writeFile(root + "/" + name, body);
  let i = 0;
  for (const a of artifact.rendered.assets)
    if (a.body)
      await writeFile(
        `${root}/${String(i++).padStart(2, "0")}-${a.role}.svg`,
        a.body,
      );
  console.log(
    draft.template.slug +
      ": " +
      artifact.rendered.assets.length +
      " assets; " +
      artifact.game.content.length +
      " HTML characters; " +
      artifact.metadata.packageHash,
  );
}
