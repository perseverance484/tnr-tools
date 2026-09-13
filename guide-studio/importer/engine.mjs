import { importJWK, jwtVerify } from "jose";
import { verifyArtifact } from "../src/artifact.mjs";
import { stableStringify } from "../src/hash.mjs";

export async function verifyApproval(
  artifact,
  approval,
  { publicJwk, studioOrigin },
) {
  const checked = await verifyArtifact(artifact);
  if (!publicJwk || !studioOrigin)
    throw Error(
      "The operator must configure the trusted approval key and Studio origin.",
    );
  const { payload } = await jwtVerify(
    approval.signature,
    await importJWK(publicJwk, "EdDSA"),
    {
      algorithms: ["EdDSA"],
      issuer: "tnr-guide-studio",
      audience: "tnr-guide-importer",
    },
  );
  for (const field of [
    "packageHash",
    "contentHash",
    "submissionId",
    "sourceSha",
  ])
    if (
      payload[field] !== checked.meta[field] ||
      approval[field] !== payload[field]
    )
      throw Error("Approval does not match this package.");
  if (
    new URL(checked.game.sourceUrl).origin !== studioOrigin ||
    checked.manifest.generated.some(
      (a) => new URL(a.url).origin !== studioOrigin,
    )
  )
    throw Error("Package asset origin is not trusted.");
  return checked;
}
const nullable = [
  "subtitle",
  "excerpt",
  "seoTitle",
  "seoDescription",
  "image",
  "relatedBloodlineId",
  "relatedItemId",
  "relatedJutsuId",
  "sourceUrl",
  "reviewNotes",
];
export function comparable(value, expected) {
  const result = {};
  for (const key of Object.keys(expected)) result[key] = value[key];
  for (const key of nullable) if (!result[key]) result[key] = null;
  if (!result.faq?.length) result.faq = null;
  return stableStringify(result);
}
export function exactReadback(actual, expected) {
  return (
    !!actual &&
    !actual.published &&
    comparable(actual, expected) === comparable(expected, expected)
  );
}
export class StorageJournal {
  constructor(storage) {
    this.storage = storage;
  }
  async read(hash) {
    const value = this.storage.getItem("tnr-import:" + hash);
    return value ? JSON.parse(value) : null;
  }
  async write(hash, value) {
    this.storage.setItem("tnr-import:" + hash, JSON.stringify(value));
  }
}
// Call only inside a TNR/Forge-owned content-staff action. No automatic retries.
export async function importApproved({
  artifact,
  approval,
  trust,
  api,
  journal,
}) {
  const { meta, game } = await verifyApproval(artifact, approval, trust),
    hash = meta.packageHash;
  let state = (await journal.read(hash)) || {
    phase: "new",
    mutationResults: [],
  };
  const save = async (patch) => {
    state = { ...state, ...patch };
    await journal.write(hash, state);
  };
  const log = async (operation, result) =>
    save({
      mutationResults: [
        ...state.mutationResults,
        {
          operation,
          success: !!result.success,
          message: String(result.message ?? "").slice(0, 8000),
        },
      ].slice(-6),
    });
  if (["create-pending", "ambiguous-create"].includes(state.phase))
    throw Error(
      "Create outcome is unknown. Do not retry creation. A staff member must reconcile the placeholder draft in TNR before continuing.",
    );
  if (state.phase === "imported") {
    const actual = await api.get({ id: state.guideId });
    if (!exactReadback(actual, game))
      throw Error(
        "The imported guide has since changed or been published. No changes were made.",
      );
    return state.receipt;
  }
  // A deterministic slug lets another device recognize a completed import.
  if (!state.guideId && api.findBySlug) {
    const existing = await api.findBySlug(game.slug);
    if (existing) {
      if (!exactReadback(existing, game))
        throw Error(
          "This slug already exists with different content. Review it in TNR.",
        );
      await save({ guideId: existing.id, phase: "verified-existing" });
    }
  }
  if (!state.guideId) {
    await save({ phase: "create-pending" }); // durable before the non-idempotent mutation
    let created;
    try {
      created = await api.create();
    } catch (error) {
      await save({ phase: "ambiguous-create" });
      throw Error(
        "Create response was lost. Creation will not be retried; reconcile in TNR.",
      );
    }
    if (
      !created?.success ||
      typeof created.message !== "string" ||
      !created.message
    ) {
      await save({ phase: "ambiguous-create" });
      throw Error(
        "Creation was not confirmed. Reconcile in TNR before another attempt.",
      );
    }
    await save({ guideId: created.message, phase: "created" });
    await log("guide.create", created);
  }
  const id = state.guideId;
  // Always read before overwriting: a published or repurposed draft is never changed.
  const before = await api.get({ id });
  if (!before || before.published)
    throw Error(
      "The destination is missing or published. No update was attempted.",
    );
  if (!exactReadback(before, game)) {
    if (!["created", "update-pending", "update-failed"].includes(state.phase))
      throw Error("Unexpected destination state.");
    // Only our freshly created placeholder or our deterministic slug may be resumed.
    if (
      before.slug !== game.slug &&
      !(
        before.slug?.startsWith("new-guide-") &&
        before.title === "New guide article" &&
        before.content === "<p>Write the guide here.</p>" &&
        before.category === "reference"
      )
    )
      throw Error(
        "The destination was edited outside this import. Review it in TNR.",
      );
    await save({ phase: "update-pending" });
    let result;
    try {
      result = await api.update({ id, data: game });
    } catch {
      const recovered = await api.get({ id }).catch(() => null);
      if (!exactReadback(recovered, game)) {
        await save({ phase: "update-failed" });
        throw Error(
          "Update outcome is uncertain. The guide ID is saved; retry will read it before updating.",
        );
      }
      result = {
        success: true,
        message: "Update confirmed by exact readback after lost response",
      };
    }
    await log(
      "guide.update",
      result || { success: false, message: "Empty update response" },
    );
    if (!result?.success) {
      await save({ phase: "update-failed" });
      throw Error(result?.message || "Native guide.update rejected the guide.");
    }
  }
  const actual = await api.get({ id });
  if (!exactReadback(actual, game)) {
    await save({ phase: "update-failed" });
    throw Error(
      "Native readback differs from the approved artifact. Import is unverified; inspect TNR sanitization/moderation.",
    );
  }
  // A later successful retry supersedes failed attempts in the operator receipt.
  const results = state.mutationResults.filter((r) => r.success);
  results.push({
    operation: "guide.get",
    success: true,
    message: "Every approved field and content byte matched; published=false",
  });
  if (!results.some((r) => r.operation === "guide.update"))
    results.unshift({
      operation: "guide.update",
      success: true,
      message:
        "Existing draft already matches the approved artifact; no update required",
    });
  const receipt = {
    guideId: id,
    packageHash: hash,
    verified: true,
    published: false,
    mutationResults: results.slice(-6),
  };
  await save({ phase: "imported", receipt });
  return receipt;
}

// Exceptional recovery after an ambiguous native create. Staff supplies the ID
// found in TNR; only the untouched native placeholder is eligible.
export async function reconcileCreation({
  artifact,
  approval,
  trust,
  api,
  journal,
  guideId,
}) {
  const { meta } = await verifyApproval(artifact, approval, trust),
    state = await journal.read(meta.packageHash);
  if (!state || !["create-pending", "ambiguous-create"].includes(state.phase))
    throw Error("No ambiguous creation to reconcile.");
  if (typeof guideId !== "string" || !guideId.trim() || guideId.length > 191)
    throw Error("Enter the placeholder guide ID from TNR.");
  const draft = await api.get({ id: guideId });
  if (
    !draft ||
    draft.published ||
    !draft.slug?.startsWith("new-guide-") ||
    draft.title !== "New guide article" ||
    draft.content !== "<p>Write the guide here.</p>" ||
    draft.category !== "reference"
  )
    throw Error("The selected guide is not an untouched native placeholder.");
  await journal.write(meta.packageHash, {
    ...state,
    guideId,
    phase: "created",
    mutationResults: [
      {
        operation: "guide.create",
        success: true,
        message: "Staff reconciled native placeholder " + guideId,
      },
    ],
  });
  return guideId;
}
