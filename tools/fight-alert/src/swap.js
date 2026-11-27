// Pre-battle jutsu swap for a fight someone else started.
//
// Off unless SWAP_ENABLED = "true" and the owner has signed the Worker in through /auth/start.
// Per fight it makes two game calls through the game's own MCP endpoint, and nothing else:
//   1. combat.getBattle   -> who moves first (activeUserId) and when round 1 starts
//   2. combat.updateCombatLoadout -> the P1 set when moving first, the P2 set when second
// It never attacks, moves, uses items, marks ready or acts after round 1 has started.

const META_PATH = "/.well-known/oauth-authorization-server";

const b64url = (bytes) =>
  btoa(String.fromCharCode(...new Uint8Array(bytes)))
    .replace(/\+/g, "-")
    .replace(/\//g, "_")
    .replace(/=+$/, "");

const randomString = (n = 32) => b64url(crypto.getRandomValues(new Uint8Array(n)));

const sha256 = async (text) =>
  b64url(await crypto.subtle.digest("SHA-256", new TextEncoder().encode(text)));

/** Pick the loadout for the turn order. Returns null when it should not swap. */
export function chooseLoadout(battle, me, env, now = Date.now()) {
  if (!battle || !battle.activeUserId) return null;
  if (battle.battleType && battle.battleType !== "COMBAT") return null;
  const roundStart = new Date(battle.roundStartAt).getTime();
  if (!Number.isFinite(roundStart) || now >= roundStart - 500) return null;
  return battle.activeUserId === me ? env.P1_LOADOUT_ID : env.P2_LOADOUT_ID;
}

/** Read the JSON-RPC result from a JSON or an SSE response body. */
export function parseRpcBody(text) {
  const trimmed = text.trim();
  if (trimmed.startsWith("{")) return JSON.parse(trimmed);
  const lines = trimmed.split("\n").filter((l) => l.startsWith("data:"));
  for (let i = lines.length - 1; i >= 0; i--) {
    try {
      const msg = JSON.parse(lines[i].slice(5).trim());
      if (msg.result || msg.error) return msg;
    } catch {}
  }
  throw new Error("no JSON-RPC result in response");
}

/** Turn a callEndpoint tool result into the endpoint's JSON output. */
export function toolOutput(rpc) {
  if (rpc.error) throw new Error(`rpc ${rpc.error.code}: ${rpc.error.message}`);
  const text = rpc.result?.content?.find((c) => c.type === "text")?.text ?? "";
  try {
    return JSON.parse(text);
  } catch {
    throw new Error(text.slice(0, 200) || "empty tool result");
  }
}

export class GameSession {
  constructor(storage, env, fetchImpl = (...args) => fetch(...args)) {
    this.storage = storage;
    this.env = env;
    this.fetch = fetchImpl;
  }

  origin() {
    return this.env.GAME_ORIGIN || "https://www.theninja-rpg.com";
  }

  async metadata() {
    const res = await this.fetch(this.origin() + META_PATH);
    if (!res.ok) throw new Error(`oauth metadata ${res.status}`);
    return res.json();
  }

  async signedIn() {
    const auth = await this.storage.get("oauth");
    return !!auth?.refresh_token || !!auth?.access_token;
  }

  /** Step 1 of sign-in: register this Worker as a client and send the owner to approve it. */
  async start(workerOrigin) {
    const meta = await this.metadata();
    const redirectUri = `${workerOrigin}/auth/callback`;
    const supported = meta.scopes_supported || [];
    const scope = ["openid", "profile", "email", "offline_access"]
      .filter((s) => !supported.length || supported.includes(s))
      .join(" ");
    let client = await this.storage.get("oauth_client");
    // The scope has to be in the registration: the game's sign-in (Clerk) gives a client
    // that registers without one only its default scopes, and refuses anything more with
    // invalid_scope.
    if (!client || client.redirect_uri !== redirectUri || client.scope !== scope) {
      if (!meta.registration_endpoint) throw new Error("game sign-in has no client registration");
      const res = await this.fetch(meta.registration_endpoint, {
        method: "POST",
        headers: { "content-type": "application/json" },
        body: JSON.stringify({
          client_name: "TNR fight alert",
          redirect_uris: [redirectUri],
          grant_types: ["authorization_code", "refresh_token"],
          response_types: ["code"],
          token_endpoint_auth_method: "none",
          scope,
        }),
      });
      if (!res.ok) throw new Error(`client registration ${res.status}: ${await res.text()}`);
      const reg = await res.json();
      // Ask only for what the registration was granted, in case it trimmed the list.
      client = { client_id: reg.client_id, redirect_uri: redirectUri, scope, granted: reg.scope || scope };
      await this.storage.put("oauth_client", client);
    }
    const verifier = randomString(48);
    const state = randomString(24);
    await this.storage.put("oauth_pending", { verifier, state, at: Date.now() });
    const url = new URL(meta.authorization_endpoint);
    url.searchParams.set("response_type", "code");
    url.searchParams.set("client_id", client.client_id);
    url.searchParams.set("redirect_uri", redirectUri);
    url.searchParams.set("state", state);
    url.searchParams.set("code_challenge", await sha256(verifier));
    url.searchParams.set("code_challenge_method", "S256");
    const ask = client.granted || scope;
    if (ask) url.searchParams.set("scope", ask);
    return url.toString();
  }

  /** Step 2 of sign-in: swap the code for tokens and check it is the watched account. */
  async finish(code, state) {
    const pending = await this.storage.get("oauth_pending");
    const client = await this.storage.get("oauth_client");
    if (!pending || pending.state !== state || Date.now() - pending.at > 10 * 60 * 1000) {
      throw new Error("sign-in link expired; start again");
    }
    await this.storage.delete("oauth_pending");
    const meta = await this.metadata();
    const tokens = await this.tokenRequest(meta.token_endpoint, {
      grant_type: "authorization_code",
      code,
      redirect_uri: client.redirect_uri,
      client_id: client.client_id,
      code_verifier: pending.verifier,
    });
    await this.storage.put("oauth", tokens);
    const me = await this.call("profile.getUser", {}, ["userData.userId", "userData.username"]);
    if (me["userData.userId"] !== this.env.WATCH_USER_ID) {
      await this.storage.delete("oauth");
      throw new Error(`signed in as ${me["userData.username"] || "another account"}, not the watched account`);
    }
    return me["userData.username"];
  }

  /** Forget the registered client so the next sign-in registers a fresh one. */
  async resetClient() {
    await this.storage.delete("oauth_client");
  }

  async signOut() {
    await this.storage.delete("oauth");
  }

  async tokenRequest(endpoint, params) {
    const res = await this.fetch(endpoint, {
      method: "POST",
      headers: { "content-type": "application/x-www-form-urlencoded" },
      body: new URLSearchParams(params).toString(),
    });
    if (!res.ok) throw new Error(`token ${res.status}: ${(await res.text()).slice(0, 200)}`);
    const t = await res.json();
    return {
      access_token: t.access_token,
      refresh_token: t.refresh_token || params.refresh_token || null,
      expires_at: Date.now() + (t.expires_in ? t.expires_in * 1000 : 50 * 60 * 1000),
    };
  }

  async accessToken(force = false) {
    // One refresh at a time: refresh tokens may rotate, and two parallel refreshes would
    // leave a used one stored.
    if (this.refreshing) await this.refreshing.catch(() => {});
    const auth = await this.storage.get("oauth");
    if (!auth) throw new Error("not signed in");
    if (!force && auth.access_token && Date.now() < auth.expires_at - 60000) {
      return auth.access_token;
    }
    if (!auth.refresh_token) throw new Error("sign-in expired; sign in again");
    // Another call may have started a refresh while this one read storage.
    if (this.refreshing) return this.refreshing;
    this.refreshing = (async () => {
      const meta = await this.metadata();
      const client = await this.storage.get("oauth_client");
      const tokens = await this.tokenRequest(meta.token_endpoint, {
        grant_type: "refresh_token",
        refresh_token: auth.refresh_token,
        client_id: client.client_id,
      });
      await this.storage.put("oauth", tokens);
      return tokens.access_token;
    })();
    const pending = this.refreshing;
    try {
      return await pending;
    } finally {
      if (this.refreshing === pending) this.refreshing = null;
    }
  }

  /** Keep the token fresh outside a fight so the swap does not wait on a refresh. */
  async keepFresh() {
    const auth = await this.storage.get("oauth");
    if (auth && Date.now() > auth.expires_at - 5 * 60 * 1000) await this.accessToken(true);
  }

  async call(endpointName, input, select) {
    const url = this.env.MCP_URL || `${this.origin()}/api/mcp`;
    const body = JSON.stringify({
      jsonrpc: "2.0",
      id: Date.now(),
      method: "tools/call",
      params: { name: "callEndpoint", arguments: { endpointName, input, ...(select ? { select } : {}) } },
    });
    for (const force of [false, true]) {
      const res = await this.fetch(url, {
        method: "POST",
        headers: {
          authorization: `Bearer ${await this.accessToken(force)}`,
          "content-type": "application/json",
          accept: "application/json, text/event-stream",
          "mcp-protocol-version": "2025-06-18",
        },
        body,
      });
      if (res.status === 401 && !force) continue;
      if (!res.ok) throw new Error(`game ${res.status}`);
      return toolOutput(parseRpcBody(await res.text()));
    }
    throw new Error("game refused the sign-in");
  }

  /** The swap itself. Returns a short description of what happened. */
  async swapForBattle(battleId) {
    const out = await this.call("combat.getBattle", { battleId }, [
      "battle.activeUserId",
      "battle.roundStartAt",
      "battle.battleType",
    ]);
    const battle = {
      activeUserId: out["battle.activeUserId"],
      roundStartAt: out["battle.roundStartAt"],
      battleType: out["battle.battleType"],
    };
    const loadoutId = chooseLoadout(battle, this.env.WATCH_USER_ID, this.env);
    if (!loadoutId) return { swapped: false, reason: "not in the lobby or not a PvP fight" };
    const first = battle.activeUserId === this.env.WATCH_USER_ID;
    const res = await this.call("combat.updateCombatLoadout", {
      battleId,
      jutsuLoadoutId: loadoutId,
    });
    const already = /already have this loadout/i.test(res?.message || "");
    const ok = res?.success !== false || already;
    return {
      swapped: ok,
      set: first ? "P1" : "P2",
      reason: ok ? undefined : res?.message || "game refused the swap",
    };
  }
}
