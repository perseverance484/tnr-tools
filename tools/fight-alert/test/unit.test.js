import { test } from "node:test";
import assert from "node:assert/strict";
import { classify, discoverKeys, parseFrame } from "../src/index.js";

test("parseFrame unwraps the nested JSON data string", () => {
  const raw = JSON.stringify({
    event: "event",
    channel: "user_x",
    data: JSON.stringify({ type: "battle", battleId: "b1", isDefender: true }),
  });
  assert.deepEqual(parseFrame(raw), {
    event: "event",
    channel: "user_x",
    data: { type: "battle", battleId: "b1", isDefender: true },
  });
  assert.equal(parseFrame("not json"), null);
});

test("classify alerts on defended battles only by default", () => {
  assert.equal(classify({ type: "battle", battleId: "b", isDefender: true }, false), "attacked");
  assert.equal(classify({ type: "battle", battleId: "b", isDefender: false }, false), null);
  assert.equal(classify({ type: "battle", battleId: "b", isDefender: false }, true), "own");
  assert.equal(classify({ type: "battleEnded" }, true), null);
  assert.equal(classify({ type: "battle" }, true), null);
});

test("discoverKeys finds the key next to the soketi host in a bundle", async () => {
  const pages = {
    "https://g.test/": '<script src="/_next/static/chunks/app.js"></script>',
    "https://g.test/profile": "",
    "https://g.test/combat": "",
    "https://g.test/_next/static/chunks/app.js":
      'x=new r.default("abc123KEY",{wsHost:"soketi.theninja-rpg.com",forceTLS:!0,disableStats:!0})',
  };
  const fakeFetch = async (u) => ({ text: async () => pages[u] ?? "" });
  const keys = await discoverKeys({ GAME_ORIGIN: "https://g.test" }, fakeFetch);
  assert.equal(keys[0], "abc123KEY");
  assert.equal(keys.at(-1), "tnr_soketi_key");
});

test("discoverKeys falls back when nothing is found", async () => {
  const keys = await discoverKeys({ GAME_ORIGIN: "https://g.test" }, async () => ({
    text: async () => "",
  }));
  assert.deepEqual(keys, ["tnr_soketi_key"]);
});

import { chooseLoadout, parseRpcBody, toolOutput, GameSession } from "../src/swap.js";

const env = { WATCH_USER_ID: "me", P1_LOADOUT_ID: "p1", P2_LOADOUT_ID: "p2" };

test("chooseLoadout picks P1 when moving first and P2 when second, only in the lobby", () => {
  const now = Date.parse("2026-11-27T12:00:00Z");
  const lobby = new Date(now + 10000).toISOString();
  assert.equal(chooseLoadout({ activeUserId: "me", roundStartAt: lobby, battleType: "COMBAT" }, "me", env, now), "p1");
  assert.equal(chooseLoadout({ activeUserId: "them", roundStartAt: lobby, battleType: "COMBAT" }, "me", env, now), "p2");
  // Round 1 has started (or is about to): never swap.
  assert.equal(chooseLoadout({ activeUserId: "me", roundStartAt: new Date(now - 1).toISOString(), battleType: "COMBAT" }, "me", env, now), null);
  assert.equal(chooseLoadout({ activeUserId: "me", roundStartAt: new Date(now + 200).toISOString(), battleType: "COMBAT" }, "me", env, now), null);
  // Not a PvP fight, or no battle.
  assert.equal(chooseLoadout({ activeUserId: "me", roundStartAt: lobby, battleType: "SPARRING" }, "me", env, now), null);
  assert.equal(chooseLoadout(null, "me", env, now), null);
});

test("parseRpcBody reads plain JSON and SSE bodies", () => {
  const rpc = { jsonrpc: "2.0", id: 1, result: { content: [{ type: "text", text: "{\"a\":1}" }] } };
  assert.deepEqual(parseRpcBody(JSON.stringify(rpc)), rpc);
  assert.deepEqual(parseRpcBody(`event: message\ndata: ${JSON.stringify(rpc)}\n\n`), rpc);
  assert.throws(() => parseRpcBody("data: nope"));
});

test("toolOutput returns the endpoint JSON and surfaces errors", () => {
  assert.deepEqual(toolOutput({ result: { content: [{ type: "text", text: "{\"x\":2}" }] } }), { x: 2 });
  assert.throws(() => toolOutput({ error: { code: -32600, message: "bad" } }), /bad/);
  assert.throws(() => toolOutput({ result: { content: [{ type: "text", text: "Unauthorized" }] } }), /Unauthorized/);
});

function memStorage() {
  const m = new Map();
  return {
    get: async (k) => m.get(k),
    put: async (k, v) => void m.set(k, v),
    delete: async (k) => void m.delete(k),
  };
}

test("swapForBattle reads turn order then sends only the jutsu loadout", async () => {
  const calls = [];
  const storage = memStorage();
  await storage.put("oauth", { access_token: "t", refresh_token: "r", expires_at: Date.now() + 3600e3 });
  const fakeFetch = async (_url, init) => {
    const body = JSON.parse(init.body);
    const { endpointName, input } = body.params.arguments;
    calls.push({ endpointName, input, auth: init.headers.authorization });
    const out = endpointName === "combat.getBattle"
      ? { "battle.activeUserId": "them", "battle.roundStartAt": new Date(Date.now() + 12000).toISOString(), "battle.battleType": "COMBAT" }
      : { success: true, message: "ok" };
    return new Response(JSON.stringify({ jsonrpc: "2.0", id: 1, result: { content: [{ type: "text", text: JSON.stringify(out) }] } }));
  };
  const s = new GameSession(storage, { ...env, MCP_URL: "https://game/api/mcp" }, fakeFetch);
  const r = await s.swapForBattle("b1");
  assert.deepEqual(r, { swapped: true, set: "P2", reason: undefined });
  assert.deepEqual(calls.map((c) => c.endpointName), ["combat.getBattle", "combat.updateCombatLoadout"]);
  assert.deepEqual(calls[1].input, { battleId: "b1", jutsuLoadoutId: "p2" });
  assert.equal(calls[0].auth, "Bearer t");
});

test("swapForBattle makes no change once round 1 has started", async () => {
  const calls = [];
  const storage = memStorage();
  await storage.put("oauth", { access_token: "t", refresh_token: "r", expires_at: Date.now() + 3600e3 });
  const fakeFetch = async (_url, init) => {
    calls.push(JSON.parse(init.body).params.arguments.endpointName);
    const out = { "battle.activeUserId": "me", "battle.roundStartAt": new Date(Date.now() - 1000).toISOString(), "battle.battleType": "COMBAT" };
    return new Response(JSON.stringify({ result: { content: [{ type: "text", text: JSON.stringify(out) }] } }));
  };
  const r = await new GameSession(storage, { ...env, MCP_URL: "https://g" }, fakeFetch).swapForBattle("b1");
  assert.equal(r.swapped, false);
  assert.deepEqual(calls, ["combat.getBattle"]);
});

test("sign-in is refused and forgotten when it is not the watched account", async () => {
  const storage = memStorage();
  await storage.put("oauth_pending", { verifier: "v", state: "s", at: Date.now() });
  await storage.put("oauth_client", { client_id: "c", redirect_uri: "https://w/auth/callback" });
  const fakeFetch = async (url) => {
    if (url.endsWith("/.well-known/oauth-authorization-server")) return Response.json({ token_endpoint: "https://g/token" });
    if (url === "https://g/token") return Response.json({ access_token: "a", refresh_token: "r", expires_in: 3600 });
    const out = { "userData.userId": "someone_else", "userData.username": "other" };
    return Response.json({ result: { content: [{ type: "text", text: JSON.stringify(out) }] } });
  };
  const s = new GameSession(storage, { ...env, GAME_ORIGIN: "https://g", MCP_URL: "https://g/api/mcp" }, fakeFetch);
  await assert.rejects(s.finish("code", "s"), /not the watched account/);
  assert.equal(await s.signedIn(), false);
});

test("an expired access token is refreshed once and the new refresh token kept", async () => {
  const storage = memStorage();
  await storage.put("oauth", { access_token: "old", refresh_token: "r1", expires_at: Date.now() - 1 });
  await storage.put("oauth_client", { client_id: "c" });
  let refreshes = 0;
  const fakeFetch = async (url) => {
    if (url.endsWith("/.well-known/oauth-authorization-server")) return Response.json({ token_endpoint: "https://g/token" });
    refreshes += 1;
    return Response.json({ access_token: "new", refresh_token: "r2", expires_in: 3600 });
  };
  const s = new GameSession(storage, { GAME_ORIGIN: "https://g" }, fakeFetch);
  const [a, b] = await Promise.all([s.accessToken(), s.accessToken()]);
  assert.equal(a, "new");
  assert.equal(b, "new");
  assert.equal(refreshes, 1);
  assert.equal((await storage.get("oauth")).refresh_token, "r2");
});

test("sign-in registers its scopes and asks only for what was granted", async () => {
  const storage = memStorage();
  // An older client registered without scopes must be replaced.
  await storage.put("oauth_client", { client_id: "old", redirect_uri: "https://w/auth/callback" });
  let registered;
  const fakeFetch = async (url, init) => {
    if (url.endsWith("/.well-known/oauth-authorization-server")) {
      return Response.json({
        authorization_endpoint: "https://g/authorize",
        registration_endpoint: "https://g/register",
        scopes_supported: ["openid", "profile", "email", "offline_access", "public_metadata"],
      });
    }
    registered = JSON.parse(init.body);
    return Response.json({ client_id: "new", scope: "openid profile email offline_access" });
  };
  const s = new GameSession(storage, { GAME_ORIGIN: "https://g" }, fakeFetch);
  const url = new URL(await s.start("https://w"));
  assert.equal(registered.scope, "openid profile email offline_access");
  assert.equal(url.searchParams.get("client_id"), "new");
  assert.equal(url.searchParams.get("scope"), "openid profile email offline_access");
});

test("own fights alert and run the lobby swap; defended fights still do", async () => {
  const { FightWatcher4, swapsFor } = await import("../src/index.js");
  assert.equal(swapsFor("attacked"), true);
  assert.equal(swapsFor("own"), true);
  assert.equal(swapsFor("test"), false);
  const env = { WATCH_USER_ID: "me", WATCH_NAME: "dauntless", ALERT_OWN_FIGHTS: "true" };
  const storage = memStorage();
  const w = new FightWatcher4({ storage }, env);
  const order = [];
  w.notify = async (kind) => {
    order.push(`notify:${kind}`);
    return { ok: true };
  };
  w.swap = async (battleId) => {
    order.push(`swap:${battleId}`);
  };
  await w.loadMeta();
  w.sockets.set(1, { ws: { send() {} }, subscribed: true, openedAt: Date.now() });
  const frame = (battleId, isDefender) =>
    JSON.stringify({ event: "event", channel: "me", data: JSON.stringify({ type: "battle", battleId, isDefender }) });
  await w.onMessage(1, frame("own1", false));
  await w.onMessage(1, frame("own1", false)); // same fight again: no second alert or swap
  await w.onMessage(1, frame("def1", true));
  assert.deepEqual(order, ["notify:own", "swap:own1", "notify:attacked", "swap:def1"]);
  assert.equal(w.meta.lastEvent.kind, "attacked");
});

test("own fights are ignored when ALERT_OWN_FIGHTS is off", async () => {
  const { FightWatcher4 } = await import("../src/index.js");
  const w = new FightWatcher4({ storage: memStorage() }, { WATCH_USER_ID: "me", ALERT_OWN_FIGHTS: "false" });
  const order = [];
  w.notify = async (kind) => order.push(kind);
  w.swap = async () => order.push("swap");
  await w.loadMeta();
  w.sockets.set(1, { ws: { send() {} }, subscribed: true, openedAt: Date.now() });
  await w.onMessage(1, JSON.stringify({ event: "event", channel: "me", data: JSON.stringify({ type: "battle", battleId: "x", isDefender: false }) }));
  assert.deepEqual(order, []);
});

test("wrangler.toml turns own-fight alerts on", async () => {
  const { readFile } = await import("node:fs/promises");
  const toml = await readFile(new URL("../wrangler.toml", import.meta.url), "utf8");
  assert.match(toml, /^ALERT_OWN_FIGHTS = "true"$/m);
  assert.match(toml, /^SWAP_ENABLED = "true"$/m);
});

test("fight alerts and swap notes retry ntfy refusals for up to 15 seconds", async () => {
  const { FightWatcher4, retryWaits } = await import("../src/index.js");
  for (const kind of ["attacked", "own", "swapped", "swapFailed"]) {
    const w = retryWaits(kind);
    assert.equal(w[0], 0);
    assert.equal(w.reduce((a, b) => a + b, 0), 15000);
  }
  assert.ok(retryWaits("online").length <= 3);

  const realFetch = globalThis.fetch;
  const realTimeout = globalThis.setTimeout;
  const waited = [];
  globalThis.setTimeout = (fn, ms) => {
    waited.push(ms);
    return realTimeout(fn, 0);
  };
  try {
    // Refused 5 times, then accepted: the alert still goes out.
    let n = 0;
    globalThis.fetch = async () => new Response("", { status: ++n <= 5 ? 429 : 200 });
    const w = new FightWatcher4({ storage: memStorage() }, { WATCH_USER_ID: "me", NTFY_TOPIC: "t" });
    await w.loadMeta();
    assert.deepEqual(await w.notify("own"), { ok: true });
    assert.equal(n, 6);
    assert.equal(w.meta.alerts, 1);

    // Refused every time: it stops after the 15-second budget and records why.
    n = 0;
    waited.length = 0;
    globalThis.fetch = async () => (n++, new Response("", { status: 429 }));
    const r = await w.notify("attacked");
    assert.equal(r.ok, false);
    assert.equal(n, retryWaits("attacked").length);
    assert.equal(waited.reduce((a, b) => a + b, 0), 15000);
    assert.match(r.error, /ntfy 429; gave up after 8 tries/);

    // A non-retryable refusal stops at once.
    n = 0;
    globalThis.fetch = async () => (n++, new Response("", { status: 403 }));
    assert.equal((await w.notify("attacked")).ok, false);
    assert.equal(n, 1);
  } finally {
    globalThis.fetch = realFetch;
    globalThis.setTimeout = realTimeout;
  }
});
