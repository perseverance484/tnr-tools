import test from "node:test";
import assert from "node:assert/strict";
import { initTRPC } from "@trpc/server";
import { fetchRequestHandler } from "@trpc/server/adapters/fetch";
import superjson from "superjson";
import { z } from "zod";
import { signedFixture, memoryJournal } from "./helpers.mjs";
import {
  importApproved,
  reconcileCreation,
  verifyApproval,
} from "../importer/engine.mjs";
import { nativeTransport } from "../importer/transport.mjs";
import { GuideArticleValidator } from "../compatibility/runtime/guide-validator.mjs";
import sanitize from "../compatibility/runtime/sanitize.mjs";
const signed = await signedFixture();
function harness(mode = {}) {
  let created = 0,
    updates = 0;
  const docs = new Map(),
    requests = [];
  const t = initTRPC.create({ transformer: superjson });
  const router = t.router({
    guide: t.router({
      create: t.procedure.mutation(() => {
        created++;
        const id = "native-" + created;
        docs.set(id, {
          id,
          slug: "new-guide-" + created,
          title: "New guide article",
          content: "<p>Write the guide here.</p>",
          category: "reference",
          published: false,
        });
        return { success: true, message: id };
      }),
      update: t.procedure
        .input(z.object({ id: z.string(), data: GuideArticleValidator }))
        .mutation(({ input: { id, data } }) => {
          updates++;
          if (mode.reject)
            return { success: false, message: "Mock moderation rejection" };
          docs.set(id, {
            id,
            ...data,
            content: mode.mangle
              ? "<p>Changed by sanitizer</p>"
              : sanitize(data.content),
          });
          return { success: true, message: "Native-shaped update response" };
        }),
      get: t.procedure
        .input(z.object({ id: z.string() }))
        .query(({ input }) => docs.get(input.id)),
      getAll: t.procedure
        .input(z.object({ includeDrafts: z.boolean() }))
        .query(() => [...docs.values()]),
    }),
  });
  const api = nativeTransport({
    origin: "https://www.theninja-rpg.com",
    fetcher: async (url, options) => {
      requests.push({
        url: String(url),
        credentials: options.credentials,
        method: options.method,
      });
      return fetchRequestHandler({
        endpoint: "/api/trpc",
        req: new Request(url, options),
        router,
        createContext: () => ({}),
      });
    },
  });
  return { api, docs, requests, counts: () => ({ created, updates }) };
}
test("actual tRPC native transport mocked locally: verify, create, update, exact get, retry idempotence", async () => {
  const h = harness(),
    journal = memoryJournal(),
    receipt = await importApproved({ ...signed, api: h.api, journal });
  assert.equal(receipt.verified, true);
  assert.equal(receipt.published, false);
  assert.deepEqual(h.counts(), { created: 1, updates: 1 });
  assert.ok(
    h.requests.every(
      (r) =>
        r.url.startsWith("https://www.theninja-rpg.com/api/trpc/") &&
        r.credentials === "same-origin",
    ),
  );
  assert.deepEqual(
    await importApproved({ ...signed, api: h.api, journal }),
    receipt,
  );
  assert.deepEqual(h.counts(), { created: 1, updates: 1 });
  // Another browser can recognize the deterministic slug without repeating either mutation.
  const second = await importApproved({
    ...signed,
    api: h.api,
    journal: memoryJournal(),
  });
  assert.equal(second.guideId, receipt.guideId);
  assert.deepEqual(h.counts(), { created: 1, updates: 1 });
  h.docs.get(receipt.guideId).published = true;
  await assert.rejects(
    importApproved({ ...signed, api: h.api, journal }),
    /published/,
  );
});
test("ambiguous create is never retried", async () => {
  const h = harness(),
    journal = memoryJournal();
  const api = {
    ...h.api,
    create: async () => {
      await h.api.create();
      throw Error("Lost response");
    },
  };
  await assert.rejects(
    importApproved({ ...signed, api, journal }),
    /response was lost/,
  );
  await assert.rejects(
    importApproved({ ...signed, api, journal }),
    /outcome is unknown/,
  );
  assert.equal(h.counts().created, 1);
});
test("rejected update resumes saved ID after staff resolves issue", async () => {
  const mode = { reject: true },
    h = harness(mode),
    journal = memoryJournal();
  await assert.rejects(
    importApproved({ ...signed, api: h.api, journal }),
    /moderation rejection/,
  );
  mode.reject = false;
  await importApproved({ ...signed, api: h.api, journal });
  assert.deepEqual(h.counts(), { created: 1, updates: 2 });
});
test("lost update response is verified by readback without repeating mutation", async () => {
  const h = harness(),
    journal = memoryJournal(),
    api = {
      ...h.api,
      update: async (input) => {
        await h.api.update(input);
        throw Error("Lost response");
      },
    };
  const r = await importApproved({ ...signed, api, journal });
  assert.equal(r.verified, true);
  assert.equal(h.counts().updates, 1);
});
test("sanitized or moderated differences cannot be reported as imported", async () => {
  const h = harness({ mangle: true });
  await assert.rejects(
    importApproved({ ...signed, api: h.api, journal: memoryJournal() }),
    /readback differs/,
  );
});
test("unsigned, wrong-key, wrong-origin, and changed packages never mutate", async () => {
  const h = harness(),
    another = await signedFixture();
  await assert.rejects(
    importApproved({
      ...signed,
      trust: another.trust,
      api: h.api,
      journal: memoryJournal(),
    }),
  );
  await assert.rejects(
    verifyApproval(signed.artifact, signed.approval, {
      ...signed.trust,
      studioOrigin: "https://elsewhere.test",
    }),
  );
  const bad = structuredClone(signed.artifact);
  bad.files["content.html"] += "x";
  await assert.rejects(
    importApproved({
      ...signed,
      artifact: bad,
      api: h.api,
      journal: memoryJournal(),
    }),
    /hash mismatch/,
  );
  assert.deepEqual(h.counts(), { created: 0, updates: 0 });
});
test("journal write failure occurs before native create", async () => {
  const h = harness(),
    journal = {
      read: async () => null,
      write: async () => {
        throw Error("Storage full");
      },
    };
  await assert.rejects(
    importApproved({ ...signed, api: h.api, journal }),
    /Storage full/,
  );
  assert.equal(h.counts().created, 0);
});

test("ambiguous creation can be explicitly reconciled to its untouched placeholder", async () => {
  const h = harness(),
    journal = memoryJournal(),
    api = {
      ...h.api,
      create: async () => {
        await h.api.create();
        throw Error("Lost");
      },
    };
  await assert.rejects(importApproved({ ...signed, api, journal }));
  await reconcileCreation({
    ...signed,
    api: h.api,
    journal,
    guideId: "native-1",
  });
  const r = await importApproved({ ...signed, api: h.api, journal });
  assert.equal(r.guideId, "native-1");
  assert.deepEqual(h.counts(), { created: 1, updates: 1 });
});
