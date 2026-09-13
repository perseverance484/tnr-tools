import registry from "../catalog/catalog.v1.json" with { type: "json" };
import aerathiel from "../fixtures/aerathiel.submission.json" with { type: "json" };
import nightParade from "../fixtures/night-parade.submission.json" with { type: "json" };
import { generateKeyPair, exportJWK } from "jose";
import { approvalSigner } from "../server/auth.mjs";
import { createArtifact } from "../src/artifact.mjs";
export { registry, aerathiel, nightParade };
export const origin = "https://studio.example.test",
  id = "a2345678-1234-1234-1234-123456789abc";
export async function signedFixture(draft = aerathiel) {
  const artifact = await createArtifact(draft, registry, origin, id);
  const keys = await generateKeyPair("EdDSA", { extractable: true }),
    publicJwk = await exportJWK(keys.publicKey),
    privateJwk = await exportJWK(keys.privateKey);
  const claims = {
    ...Object.fromEntries(
      ["packageHash", "contentHash", "submissionId", "sourceSha"].map((k) => [
        k,
        artifact.metadata[k],
      ]),
    ),
    approvedAt: "2026-09-13T00:00:00Z",
    staffId: "test-staff",
  };
  return {
    artifact,
    approval: {
      ...claims,
      signature: await approvalSigner(JSON.stringify(privateJwk))(claims),
    },
    trust: { publicJwk, studioOrigin: origin },
  };
}
export function memoryJournal() {
  const map = new Map();
  return {
    map,
    read: async (k) => structuredClone(map.get(k) || null),
    write: async (k, v) => map.set(k, structuredClone(v)),
  };
}
