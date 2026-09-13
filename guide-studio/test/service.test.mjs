import test from "node:test";
import assert from "node:assert/strict";
import { createService } from "../server/service.mjs";
import { MemoryStore, MemoryBucket, D1Store } from "../server/store.mjs";
import {
  approvalSigner,
  accessVerifier,
  turnstileVerifier,
} from "../server/auth.mjs";
import { generateKeyPair, exportJWK, createLocalJWKSet, SignJWT } from "jose";
import { registry, aerathiel, origin } from "./helpers.mjs";
import { readPackageZip } from "../src/artifact.mjs";
import { verifyApproval } from "../importer/engine.mjs";
import { DatabaseSync } from "node:sqlite";
import { readFile } from "node:fs/promises";
const keys = await generateKeyPair("EdDSA", { extractable: true }),
  publicJwk = await exportJWK(keys.publicKey),
  privateJwk = await exportJWK(keys.privateKey);
function setup() {
  const store = new MemoryStore(),
    bucket = new MemoryBucket();
  const handler = createService({
    store,
    bucket,
    registry,
    origin,
    authenticate: async (r) => {
      if (r.headers.get("test-staff") !== "yes") throw Error("No");
      return { id: "staff-1" };
    },
    verifyTurnstile: async (token) => {
      if (token !== "valid") throw Error("Captcha failed");
    },
    signApproval: approvalSigner(JSON.stringify(privateJwk)),
  });
  const call = (path, data, { staff = false, from = origin } = {}) =>
    handler(
      new Request(origin + path, {
        method: data === undefined ? "GET" : "POST",
        headers: {
          Origin: from,
          "Content-Type": "application/json",
          ...(staff ? { "test-staff": "yes" } : {}),
        },
        ...(data === undefined ? {} : { body: JSON.stringify(data) }),
      }),
    );
  return { store, bucket, call };
}
async function submit(h, draft = aerathiel) {
  const r = await h.call("/api/submissions", {
    draft,
    turnstileToken: "valid",
  });
  assert.equal(r.status, 201);
  return r.json();
}
async function transition(h, r, status, extra = {}) {
  return h.call(
    "/api/staff/submissions/" + r.id + "/transition",
    { revision: r.revision, packageHash: r.packageHash, status, ...extra },
    { staff: true },
  );
}
test("submission → final review → immutable approval → signed package; publication remains false", async () => {
  const h = setup(),
    receipt = await submit(h),
    id = receipt.id;
  assert.equal((await h.call("/api/staff/submissions")).status, 401);
  const detail = await (
    await h.call("/api/staff/submissions/" + id, undefined, { staff: true })
  ).json();
  const before = structuredClone(detail.artifact.files);
  assert.equal(
    (
      await h.call("/api/staff/submissions/" + id + "/package", undefined, {
        staff: true,
      })
    ).status,
    409,
  );
  assert.equal(
    (await h.call(detail.artifact.rendered.assets[0].url.replace(origin, "")))
      .status,
    404,
  );
  let r = await (await transition(h, detail.record, "In review")).json();
  assert.equal(
    (await transition(h, detail.record, "Rejected/archived")).status,
    409,
    "stale review",
  );
  r = await (await transition(h, r, "Approved for import")).json();
  assert.ok(r.approval.signature);
  const download = await h.call(
    "/api/staff/submissions/" + id + "/package",
    undefined,
    { staff: true },
  );
  assert.equal(download.status, 200);
  const parsed = await readPackageZip(
    new Uint8Array(await download.arrayBuffer()),
  );
  await verifyApproval(parsed.artifact, parsed.approval, {
    publicJwk,
    studioOrigin: origin,
  });
  assert.deepEqual(parsed.artifact.files, before);
  assert.equal(
    (await h.call(detail.artifact.rendered.assets[0].url.replace(origin, "")))
      .status,
    200,
  );
  assert.equal(
    (await transition(h, r, "In review")).status,
    409,
    "approved bytes never reopen for editing",
  );
  assert.equal(
    (await transition(h, r, "Imported")).status,
    400,
    "no unaudited import claims",
  );
  const importReceipt = {
    guideId: "mock-game-id",
    packageHash: r.packageHash,
    verified: true,
    published: false,
    mutationResults: [
      { operation: "guide.update", success: true, message: "mock" },
      { operation: "guide.get", success: true, message: "exact match" },
    ],
  };
  r = await (
    await transition(h, r, "Imported", { receipt: importReceipt })
  ).json();
  assert.equal(r.status, "Imported");
  assert.equal(r.importReceipt.published, false);
});
test("competing approval/rejection has one CAS winner and cannot expose rejected assets", async () => {
  const h = setup(),
    receipt = await submit(h);
  let r = await h.store.get(receipt.id);
  r = await (await transition(h, r, "In review")).json();
  const results = await Promise.all([
    transition(h, r, "Approved for import"),
    transition(h, r, "Rejected/archived"),
  ]);
  assert.deepEqual(results.map((r) => r.status).sort(), [200, 409]);
  const winner = await h.store.get(r.id),
    object = JSON.parse(await (await h.bucket.get(winner.artifactKey)).text());
  assert.equal(
    (await h.call(object.rendered.assets[0].url.replace(origin, ""))).status,
    winner.approval ? 200 : 404,
  );
});
test("private receipt and changes-requested revisions preserve original snapshot", async () => {
  const h = setup(),
    receipt = await submit(h);
  let r = await h.store.get(receipt.id);
  r = await (await transition(h, r, "In review")).json();
  r = await (
    await transition(h, r, "Changes requested", {
      notes: "Explain the opening",
    })
  ).json();
  assert.equal(
    (await h.call("/api/receipt/" + r.id, { token: "wrong" })).status,
    404,
  );
  const feedback = await (
    await h.call("/api/receipt/" + r.id, { token: receipt.token })
  ).json();
  assert.equal(feedback.notes, "Explain the opening");
  assert.deepEqual(feedback.submission, aerathiel);
  const revised = { ...aerathiel, summary: "Revised plan" };
  const result = await h.call("/api/submissions", {
    draft: revised,
    turnstileToken: "valid",
    parentId: r.id,
    parentToken: receipt.token,
  });
  assert.equal(result.status, 201);
  assert.equal((await h.store.get(r.id)).packageHash, r.packageHash);
});
test("strict validation rejects forged mechanics/credentials, missing notes, bad captcha, cross-origin writes", async () => {
  const h = setup();
  for (const draft of [
    { ...aerathiel, cookie: "not-a-real-cookie" },
    { ...aerathiel, loadout: [{ ...aerathiel.loadout[0], howIUseIt: "" }] },
    { ...aerathiel, template: { ...aerathiel.template, version: 99 } },
  ])
    assert.equal(
      (await h.call("/api/submissions", { draft, turnstileToken: "valid" }))
        .status,
      400,
    );
  assert.equal(
    (
      await h.call("/api/submissions", {
        draft: aerathiel,
        turnstileToken: "bad",
      })
    ).status,
    400,
  );
  assert.equal(
    (
      await h.call(
        "/api/submissions",
        { draft: aerathiel, turnstileToken: "valid" },
        { from: "https://attacker.test" },
      )
    ).status,
    403,
  );
});
test("Cloudflare boundaries fail closed and Turnstile validates hostname/action", async () => {
  assert.throws(() =>
    accessVerifier({ domain: "https://attacker.test", audience: "x" }),
  );
  await assert.rejects(
    accessVerifier({
      domain: "https://staff.cloudflareaccess.com",
      audience: "x",
    })(new Request(origin)),
    /sign-in/,
  );
  const check = (result) =>
    turnstileVerifier(
      { secret: "mock-secret", hostname: "studio.example.test" },
      async (url, opts) => {
        assert.equal(
          url,
          "https://challenges.cloudflare.com/turnstile/v0/siteverify",
        );
        assert.equal(JSON.parse(opts.body).response, "mock-token");
        return Response.json(result);
      },
    )("mock-token");
  await check({
    success: true,
    hostname: "studio.example.test",
    action: "guide-submit",
  });
  await assert.rejects(
    check({ success: true, hostname: "elsewhere", action: "guide-submit" }),
  );
  await assert.rejects(
    check({ success: true, hostname: "studio.example.test", action: "login" }),
  );
  await assert.rejects(turnstileVerifier({})("mock-token"));
});
test("D1 production adapter executes actual SQLite schema and conditional transition SQL", async () => {
  const sqlite = new DatabaseSync(":memory:");
  sqlite.exec(await readFile("server/schema.sql", "utf8"));
  const db = {
    prepare: (sql) => ({
      bind: (...args) => ({
        run: async () => ({
          meta: { changes: Number(sqlite.prepare(sql).run(...args).changes) },
        }),
        first: async () => sqlite.prepare(sql).get(...args),
        all: async () => ({ results: sqlite.prepare(sql).all(...args) }),
      }),
    }),
  };
  const store = new D1Store(db),
    r = { id: "one", revision: 1, status: "Submitted", author: "x" };
  await store.create(r);
  assert.deepEqual(await store.get("one"), r);
  assert.equal(
    await store.cas("one", 1, { ...r, revision: 2, status: "In review" }),
    true,
  );
  assert.equal(
    await store.cas("one", 1, {
      ...r,
      revision: 2,
      status: "Rejected/archived",
    }),
    false,
  );
  assert.equal((await store.list()).records[0].status, "In review");
  sqlite.close();
});

test("Access verifies signature, issuer, audience and expiry with local JWKS", async () => {
  const pair = await generateKeyPair("RS256"),
    jwk = await exportJWK(pair.publicKey),
    domain = "https://staff.cloudflareaccess.com";
  const verifier = accessVerifier({
    domain,
    audience: "staff-only",
    trustedKeys: createLocalJWKSet({ keys: [jwk] }),
  });
  const token = async (audience) =>
    new SignJWT({ sub: "reviewer" })
      .setProtectedHeader({ alg: "RS256" })
      .setIssuer(domain)
      .setAudience(audience)
      .setExpirationTime("1m")
      .sign(pair.privateKey);
  assert.deepEqual(
    await verifier(
      new Request(origin, {
        headers: { "Cf-Access-Jwt-Assertion": await token("staff-only") },
      }),
    ),
    { id: "reviewer" },
  );
  await assert.rejects(
    verifier(
      new Request(origin, {
        headers: { "Cf-Access-Jwt-Assertion": await token("wrong-audience") },
      }),
    ),
  );
  await assert.rejects(
    verifier(
      new Request(origin, { headers: { "Cf-Access-Jwt-Assertion": "forged" } }),
    ),
  );
});

test("expired Access assertion is rejected", async () => {
  const pair = await generateKeyPair("RS256"),
    jwk = await exportJWK(pair.publicKey),
    domain = "https://staff.cloudflareaccess.com";
  const verifier = accessVerifier({
    domain,
    audience: "staff-only",
    trustedKeys: createLocalJWKSet({ keys: [jwk] }),
  });
  const token = await new SignJWT({ sub: "reviewer" })
    .setProtectedHeader({ alg: "RS256" })
    .setIssuer(domain)
    .setAudience("staff-only")
    .setExpirationTime(1)
    .sign(pair.privateKey);
  await assert.rejects(
    verifier(
      new Request(origin, { headers: { "Cf-Access-Jwt-Assertion": token } }),
    ),
  );
});
