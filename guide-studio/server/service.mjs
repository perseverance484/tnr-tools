import { z } from "zod";
import { createArtifact, verifyArtifact, exportZip } from "../src/artifact.mjs";
import { sha256, stableStringify } from "../src/hash.mjs";
import { DraftSchema, decodeBase64 } from "../src/schema.mjs";
const response = (data, status = 200) =>
  new Response(JSON.stringify(data), {
    status,
    headers: {
      "Content-Type": "application/json",
      "Cache-Control": "no-store",
      "X-Content-Type-Options": "nosniff",
    },
  });
const statuses = [
  "Submitted",
  "In review",
  "Changes requested",
  "Approved for import",
  "Imported",
  "Rejected/archived",
];
const transitions = {
  Submitted: ["In review", "Rejected/archived"],
  "In review": [
    "Changes requested",
    "Approved for import",
    "Rejected/archived",
  ],
  "Changes requested": ["In review", "Rejected/archived"],
  "Approved for import": ["Imported"],
  Imported: [],
  "Rejected/archived": [],
};
async function body(request) {
  if (!request.headers.get("Content-Type")?.startsWith("application/json"))
    throw Error("Send JSON");
  if (Number(request.headers.get("Content-Length")) > 2_200_000)
    throw Error("Submission too large");
  const reader = request.body?.getReader();
  if (!reader) throw Error("Missing request body");
  let length = 0,
    chunks = [];
  for (;;) {
    const { done, value } = await reader.read();
    if (done) break;
    length += value.length;
    if (length > 2_200_000) {
      await reader.cancel();
      throw Error("Submission too large");
    }
    chunks.push(value);
  }
  const joined = new Uint8Array(length);
  let offset = 0;
  for (const c of chunks) {
    joined.set(c, offset);
    offset += c.length;
  }
  return JSON.parse(new TextDecoder().decode(joined));
}
const receiptSchema = z
  .object({
    guideId: z.string().min(1).max(191),
    packageHash: z.string().length(64),
    verified: z.literal(true),
    published: z.literal(false),
    mutationResults: z
      .array(
        z
          .object({
            operation: z.enum(["guide.create", "guide.update", "guide.get"]),
            success: z.boolean(),
            message: z.string().max(8000),
          })
          .strict(),
      )
      .min(2)
      .max(6),
  })
  .strict();
export function createService({
  store,
  bucket,
  registry,
  origin,
  authenticate,
  verifyTurnstile,
  signApproval,
  now = () => new Date().toISOString(),
}) {
  const load = async (key) => {
    const x = await bucket.get(key);
    if (!x) throw Error("Stored artifact is unavailable");
    return JSON.parse(await x.text());
  };
  return async (request) => {
    const url = new URL(request.url),
      path = url.pathname;
    try {
      if (request.method !== "GET" && request.headers.get("Origin") !== origin)
        return response({ error: "Origin not allowed" }, 403);
      if (path === "/api/submissions" && request.method === "POST") {
        const input = z
          .object({
            draft: DraftSchema,
            turnstileToken: z.string().max(2048),
            parentId: z.string().max(64).optional(),
            parentToken: z.string().max(100).optional(),
          })
          .strict()
          .parse(await body(request));
        await verifyTurnstile(input.turnstileToken);
        if (input.parentId) {
          const parent = await store.get(input.parentId);
          if (
            !parent ||
            parent.status !== "Changes requested" ||
            (await sha256(input.parentToken || "")) !== parent.receiptTokenHash
          )
            throw Error("The revision receipt is not valid");
        }
        const id = crypto.randomUUID(),
          token = crypto.randomUUID() + crypto.randomUUID(),
          artifact = await createArtifact(input.draft, registry, origin, id);
        const artifactKey = `snapshots/${id}/${artifact.metadata.packageHash}.json`;
        await bucket.put(artifactKey, JSON.stringify(artifact));
        const record = {
          id,
          revision: 1,
          status: "Submitted",
          author: artifact.submission.author,
          bloodline: artifact.rendered.template.name,
          createdAt: now(),
          artifactKey,
          packageHash: artifact.metadata.packageHash,
          receiptTokenHash: await sha256(token),
          parentId: input.parentId ?? null,
          notes: "",
          history: [{ status: "Submitted", at: now() }],
        };
        await store.create(record);
        return response(
          { id, token, status: record.status, packageHash: record.packageHash },
          201,
        );
      }
      if (path.startsWith("/api/receipt/") && request.method === "POST") {
        const input = z
            .object({ token: z.string().max(100) })
            .strict()
            .parse(await body(request)),
          r = await store.get(path.split("/").at(-1));
        if (!r || (await sha256(input.token)) !== r.receiptTokenHash)
          return response({ error: "Receipt not found" }, 404);
        const artifact = await load(r.artifactKey);
        return response({
          id: r.id,
          status: r.status,
          notes: r.notes,
          parentId: r.parentId,
          submission: artifact.submission,
        });
      }
      if (path.startsWith("/guide-assets/") && request.method === "GET") {
        const parts = path.slice("/guide-assets/".length).split("/"),
          [ownerId, file] = parts;
        const owner = /^[a-f0-9-]{36}$/.test(ownerId)
          ? await store.get(ownerId)
          : null;
        if (
          parts.length !== 2 ||
          !owner?.approval ||
          !["Approved for import", "Imported"].includes(owner.status) ||
          !/^[a-f0-9]{64}\.(svg|webp)$/.test(file)
        )
          return response({ error: "Not found" }, 404);
        const object = await bucket.get(
          "approved-assets/" + ownerId + "/" + file,
        );
        if (!object) return response({ error: "Not found" }, 404);
        return new Response(await object.arrayBuffer(), {
          headers: {
            "Content-Type": file.endsWith(".svg")
              ? "image/svg+xml"
              : "image/webp",
            "Cache-Control": "public,max-age=31536000,immutable",
            "X-Content-Type-Options": "nosniff",
            "Content-Security-Policy":
              "default-src 'none'; img-src data:; style-src 'unsafe-inline'; sandbox",
          },
        });
      }
      if (!path.startsWith("/api/staff/"))
        return response({ error: "Not found" }, 404);
      let staff;
      try {
        staff = await authenticate(request);
      } catch {
        return response({ error: "Content staff sign-in required" }, 401);
      }
      if (path === "/api/staff/submissions" && request.method === "GET") {
        const list = await store.list(url.searchParams.get("cursor") || "");
        return response({
          records: list.records.map(
            ({ receiptTokenHash, artifactKey, ...r }) => r,
          ),
          next: list.next,
        });
      }
      const match = path.match(
        /^\/api\/staff\/submissions\/([a-f0-9-]+)(?:\/(transition|package))?$/,
      );
      if (!match) return response({ error: "Not found" }, 404);
      const [, id, action] = match,
        r = await store.get(id);
      if (!r) return response({ error: "Not found" }, 404);
      if (!action && request.method === "GET") {
        const { receiptTokenHash, ...record } = r;
        const artifact = await load(r.artifactKey);
        await verifyArtifact(artifact);
        return response({ record, artifact });
      }
      if (action === "package" && request.method === "GET") {
        if (!r.approval) return response({ error: "Approval required" }, 409);
        const artifact = await load(r.artifactKey);
        await verifyArtifact(artifact);
        return new Response(exportZip(artifact, r.approval), {
          headers: {
            "Content-Type": "application/zip",
            "Content-Disposition": `attachment; filename="tnr-guide-${id}.zip"`,
            "Cache-Control": "no-store",
          },
        });
      }
      if (action === "transition" && request.method === "POST") {
        const input = z
          .object({
            revision: z.number().int(),
            status: z.enum(statuses),
            packageHash: z.string().length(64),
            notes: z.string().trim().max(4000).default(""),
            receipt: receiptSchema.optional(),
          })
          .strict()
          .parse(await body(request));
        if (
          r.revision !== input.revision ||
          r.packageHash !== input.packageHash
        )
          return response(
            {
              error:
                "This review changed. Reopen the current artifact before acting.",
            },
            409,
          );
        if (!transitions[r.status].includes(input.status))
          return response(
            { error: "This state transition is not allowed." },
            409,
          );
        if (input.status === "Changes requested" && !input.notes)
          throw Error("Explain the requested changes");
        const next = {
          ...r,
          revision: r.revision + 1,
          status: input.status,
          notes: input.notes,
          history: [
            ...r.history,
            {
              status: input.status,
              at: now(),
              staffId: staff.id,
              notes: input.notes,
            },
          ],
        };
        if (input.status === "Approved for import") {
          const artifact = await load(r.artifactKey);
          await verifyArtifact(artifact);
          const claims = {
            packageHash: r.packageHash,
            contentHash: artifact.metadata.contentHash,
            submissionId: id,
            sourceSha: registry.sourceSha,
            approvedAt: now(),
            staffId: staff.id,
          };
          const signature = await signApproval(claims);
          next.approval = { ...claims, signature };
          // Content-addressed, never overwritten with different bytes. Identical concurrent puts are safe.
          for (const a of artifact.rendered.assets)
            await bucket.put(
              "approved-assets/" + id + "/" + a.url.split("/").at(-1),
              a.body ?? decodeBase64(a.data.split(",")[1]),
            );
        }
        if (input.status === "Imported") {
          if (
            !input.receipt ||
            input.receipt.packageHash !== r.packageHash ||
            input.receipt.mutationResults.some((x) => !x.success) ||
            !input.receipt.mutationResults.some(
              (x) => x.operation === "guide.get",
            )
          )
            throw Error("A verified importer receipt is required");
          next.importReceipt = input.receipt;
        }
        if (!(await store.cas(id, r.revision, next)))
          return response(
            { error: "Another reviewer changed this submission. Reopen it." },
            409,
          );
        const { receiptTokenHash, ...publicRecord } = next;
        return response(publicRecord);
      }
      return response({ error: "Method not allowed" }, 405);
    } catch (error) {
      return response(
        {
          error:
            error instanceof z.ZodError
              ? "Check the submitted fields and their length limits."
              : String(error.message || "Request failed"),
        },
        400,
      );
    }
  };
}
