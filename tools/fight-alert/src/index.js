// Fight alert for one TNR account.
//
// Listens on the account's own live channel on the game's Soketi (Pusher protocol) server,
// the same public channel the game's web page subscribes to. When the server announces a
// battle the account is in (attacked, or started by it when ALERT_OWN_FIGHTS = "true"), it
// sends a max-priority ntfy notification.
//
// The alert itself makes no game API calls. The optional lobby swap (src/swap.js) is off
// until SWAP_ENABLED = "true" and the owner has signed the Worker in to the game; it only
// changes the jutsu set in the 15-second lobby of a fight it alerted on.

import { GameSession } from "./swap.js";

const DEFAULTS = {
  GAME_ORIGIN: "https://www.theninja-rpg.com",
  SOKETI_URL: "wss://soketi.theninja-rpg.com",
  NTFY_URL: "https://ntfy.sh",
  // Key name in the game's public soketi/config.json; used only if discovery fails.
  FALLBACK_KEY: "tnr_soketi_key",
};

const ROTATE_MS = 14 * 60 * 1000; // outbound sockets keep a DO alive for up to 15 min
const WATCHDOG_MS = 60 * 1000;
const OFFLINE_AFTER_MS = 2 * 60 * 1000;
const KEY_TTL_MS = 6 * 60 * 60 * 1000;
const SEEN_MAX = 50;

const cfg = (env, name) => env[name] || DEFAULTS[name];

/** Find the Pusher app key that the game's web bundle ships. Returns candidates, best first. */
export async function discoverKeys(env, fetchImpl = fetch) {
  const origin = cfg(env, "GAME_ORIGIN");
  const configured = new URL(cfg(env, "SOKETI_URL")).hostname.replace(/\./g, "\\.");
  const host = `(?:${configured}|soketi\\.[\\w.-]+)`;
  const found = [];
  const scripts = new Set();
  for (const path of ["/", "/profile", "/combat"]) {
    try {
      const res = await fetchImpl(origin + path, { redirect: "follow" });
      const html = await res.text();
      for (const m of html.matchAll(/["'(](\/_next\/static\/[^"'()\s]+?\.js)/g)) {
        scripts.add(m[1]);
      }
    } catch {}
  }
  const patterns = [
    // new Pusher("KEY", { wsHost: "soketi.theninja-rpg.com", ... })
    new RegExp(`["'\`]([A-Za-z0-9_\\-]{6,80})["'\`]\\s*,\\s*\\{[^{}]{0,400}?${host}`),
    // key defined in a constant near the host
    new RegExp(`${host}[\\s\\S]{0,600}?NEXT_PUBLIC_PUSHER_APP_KEY["'\`]?\\s*[:=]\\s*["'\`]([A-Za-z0-9_\\-]{6,80})`),
    new RegExp(`NEXT_PUBLIC_PUSHER_APP_KEY["'\`]?\\s*[:=]\\s*["'\`]([A-Za-z0-9_\\-]{6,80})`),
  ];
  let checked = 0;
  for (const src of scripts) {
    if (checked++ >= 120 || found.length) break;
    try {
      const js = await (await fetchImpl(origin + src)).text();
      if (!js.includes("PUSHER") && !new RegExp(host).test(js)) continue;
      for (const p of patterns) {
        const m = js.match(p);
        if (m && !found.includes(m[1])) found.push(m[1]);
      }
    } catch {}
  }
  if (!found.includes(DEFAULTS.FALLBACK_KEY)) found.push(DEFAULTS.FALLBACK_KEY);
  return found;
}

/** Parse one Pusher protocol frame. `data` arrives as a JSON string inside the frame. */
export function parseFrame(raw) {
  let frame;
  try {
    frame = JSON.parse(raw);
  } catch {
    return null;
  }
  let data = frame.data;
  if (typeof data === "string") {
    try {
      data = JSON.parse(data);
    } catch {}
  }
  return { event: frame.event, channel: frame.channel, data };
}

/** Decide what a game event means for the alert. */
export function classify(data, alertOwnFights) {
  if (!data || typeof data !== "object" || data.type !== "battle" || !data.battleId) {
    return null;
  }
  if (data.isDefender) return "attacked";
  return alertOwnFights ? "own" : null;
}

/** The lobby swap runs on every fight the alert goes out for: attacked or started by us. */
export function swapsFor(kind) {
  return kind === "attacked" || kind === "own";
}

export class FightWatcher4 {
  constructor(state, env) {
    this.state = state;
    this.env = env;
    this.sockets = new Map(); // id -> { ws, subscribed, openedAt, pingTimer }
    this.nextSocketId = 1;
    this.connecting = false;
    this.meta = null;
    this.game = new GameSession(state.storage, env);
  }

  swapOn() {
    return this.env.SWAP_ENABLED === "true" && !!this.env.P1_LOADOUT_ID && !!this.env.P2_LOADOUT_ID;
  }

  async loadMeta() {
    if (!this.meta) {
      this.meta = (await this.state.storage.get("meta")) || {
        seen: [],
        key: null,
        keyAt: 0,
        keyCandidates: [],
        lastSubscribedAt: 0,
        lastEvent: null,
        lastAlert: null,
        offlineNotified: false,
        lastError: null,
        alerts: 0,
      };
    }
    return this.meta;
  }

  async saveMeta() {
    await this.state.storage.put("meta", this.meta);
  }

  healthy() {
    for (const s of this.sockets.values()) if (s.subscribed) return true;
    return false;
  }

  async fetch(request) {
    // A deploy does not replace an instance that holds an open outbound socket. Each deploy
    // carries a higher DEPLOY_ID; when a newer Worker calls, this instance resets itself so
    // the next call starts the new code (and picks up new secrets).
    const incoming = Number(request.headers.get("x-deploy-id") || 0);
    if (incoming > Number(this.env.DEPLOY_ID || 0) && typeof this.state.abort === "function") {
      for (const [id] of this.sockets) this.drop(id);
      this.state.abort("newer deploy");
    }
    const url = new URL(request.url);
    await this.loadMeta();
    if (url.pathname === "/ensure") {
      await this.ensure();
      return Response.json({ ok: true });
    }
    if (url.pathname === "/status") {
      await this.ensure();
      const m = this.meta;
      return Response.json({
        watching: this.env.WATCH_NAME || "account",
        deployId: this.env.DEPLOY_ID || null,
        connected: this.healthy(),
        sockets: this.sockets.size,
        lastSubscribedAt: m.lastSubscribedAt ? new Date(m.lastSubscribedAt).toISOString() : null,
        keyFound: !!m.key,
        lastEvent: m.lastEvent,
        lastAlert: m.lastAlert,
        alertsSent: m.alerts,
        lastError: m.lastError,
        lastNotify: m.lastNotify || null,
        swap: {
          enabled: this.swapOn(),
          signedIn: await this.game.signedIn(),
          account: m.swapAccount || null,
          last: m.lastSwap || null,
        },
      });
    }
    if (url.pathname === "/auth/start") {
      try {
        return Response.redirect(await this.game.start(url.searchParams.get("origin")), 302);
      } catch (err) {
        return page(`Could not start the game sign-in: ${err.message}`, 502);
      }
    }
    if (url.pathname === "/auth/callback") {
      const error = url.searchParams.get("error");
      if (error) {
        // A refused request usually means the registered client is wrong for the game's
        // sign-in; register a fresh one next time.
        if (error !== "access_denied") await this.game.resetClient();
        return page(`The game sign-in was not approved (${error}).`, 400);
      }
      try {
        const name = await this.game.finish(url.searchParams.get("code"), url.searchParams.get("state"));
        this.meta.swapAccount = name;
        await this.saveMeta();
        return page(`Signed in as ${name}. The lobby jutsu swap is ${this.swapOn() ? "on" : "off"}.`);
      } catch (err) {
        return page(`Sign-in failed: ${err.message}`, 400);
      }
    }
    if (url.pathname === "/auth/signout") {
      await this.game.signOut();
      this.meta.swapAccount = null;
      await this.saveMeta();
      return page("Signed out. The lobby jutsu swap will not run until you sign in again.");
    }
    if (url.pathname === "/test") {
      const result = await this.notify("test");
      return Response.json(result, { status: result.ok ? 200 : 502 });
    }
    return new Response("Not found", { status: 404 });
  }

  async alarm() {
    await this.loadMeta();
    await this.ensure();
    const now = Date.now();
    // Rotate before the 15 minute keep-alive window ends; the old socket closes once the
    // new one is subscribed, so there is no gap.
    for (const s of this.sockets.values()) {
      if (s.subscribed && now - s.openedAt > ROTATE_MS && this.sockets.size === 1) {
        await this.connect();
        break;
      }
    }
    const m = this.meta;
    if (!this.healthy() && m.lastSubscribedAt && now - m.lastSubscribedAt > OFFLINE_AFTER_MS) {
      if (!m.offlineNotified) {
        m.offlineNotified = true;
        await this.saveMeta();
        await this.notify("offline");
      }
    }
    if (this.swapOn()) {
      try {
        await this.game.keepFresh();
      } catch (err) {
        m.lastError = `game sign-in: ${err.message}`;
        await this.saveMeta();
      }
    }
    await this.state.storage.setAlarm(Date.now() + WATCHDOG_MS);
  }

  async ensure() {
    const current = await this.state.storage.getAlarm();
    if (!current) await this.state.storage.setAlarm(Date.now() + WATCHDOG_MS);
    if (this.healthy() || this.connecting) return;
    // Drop sockets that never subscribed.
    for (const [id, s] of this.sockets) {
      if (!s.subscribed && Date.now() - s.openedAt > 20000) this.drop(id);
    }
    if (this.sockets.size === 0) await this.connect();
  }

  async getKey(forceRefresh = false) {
    const m = this.meta;
    if (this.env.PUSHER_KEY) return this.env.PUSHER_KEY;
    if (!forceRefresh && m.key && Date.now() - m.keyAt < KEY_TTL_MS) return m.key;
    if (forceRefresh || !m.keyCandidates.length) {
      m.keyCandidates = await discoverKeys(this.env);
    }
    const key = m.key && !forceRefresh ? m.key : m.keyCandidates[0];
    return key;
  }

  async connect() {
    // Throttle so a bad key or a server outage can't spin; the 1-minute alarm retries.
    if (Date.now() - (this.lastConnectAt || 0) < 5000) return;
    this.lastConnectAt = Date.now();
    this.connecting = true;
    try {
      const key = await this.getKey();
      const base = cfg(this.env, "SOKETI_URL").replace(/^ws/, "http");
      const url = `${base}/app/${encodeURIComponent(key)}?protocol=7&client=js&version=8.4.0&flash=false`;
      const res = await fetch(url, { headers: { Upgrade: "websocket" } });
      const ws = res.webSocket;
      if (!ws) throw new Error(`upgrade failed (${res.status})`);
      ws.accept();
      const id = this.nextSocketId++;
      const sock = { ws, subscribed: false, openedAt: Date.now(), key, pingTimer: null };
      this.sockets.set(id, sock);
      ws.addEventListener("message", (e) => this.onMessage(id, e.data));
      ws.addEventListener("close", () => this.onClosed(id));
      ws.addEventListener("error", () => this.onClosed(id));
    } catch (err) {
      this.meta.lastError = `connect: ${err.message}`;
      await this.saveMeta();
    } finally {
      this.connecting = false;
    }
  }

  drop(id) {
    const s = this.sockets.get(id);
    if (!s) return;
    clearInterval(s.pingTimer);
    this.sockets.delete(id);
    try {
      s.ws.close(1000, "rotate");
    } catch {}
  }

  async onClosed(id) {
    if (!this.sockets.has(id)) return;
    const s = this.sockets.get(id);
    clearInterval(s.pingTimer);
    this.sockets.delete(id);
    if (this.healthy()) return;
    await this.connect();
    // If that attempt was throttled or failed, try once more shortly; the alarm covers the rest.
    setTimeout(() => {
      if (!this.healthy()) this.connect();
    }, 6000);
  }

  async onMessage(id, raw) {
    const sock = this.sockets.get(id);
    if (!sock) return;
    const msg = parseFrame(raw);
    if (!msg) return;
    const m = this.meta;
    switch (msg.event) {
      case "pusher:connection_established": {
        const timeout = Math.max(30, Math.min(120, msg.data?.activity_timeout || 120));
        sock.pingTimer = setInterval(() => {
          try {
            sock.ws.send(JSON.stringify({ event: "pusher:ping", data: {} }));
          } catch {}
        }, (timeout - 10) * 1000);
        sock.ws.send(
          JSON.stringify({ event: "pusher:subscribe", data: { channel: this.env.WATCH_USER_ID } }),
        );
        return;
      }
      case "pusher:ping":
        sock.ws.send(JSON.stringify({ event: "pusher:pong", data: {} }));
        return;
      case "pusher_internal:subscription_succeeded": {
        sock.subscribed = true;
        const wasOffline = m.offlineNotified;
        m.key = sock.key;
        m.keyAt = m.keyAt && m.key === sock.key ? m.keyAt : Date.now();
        m.lastSubscribedAt = Date.now();
        m.lastError = null;
        m.offlineNotified = false;
        await this.saveMeta();
        // A rotation is complete once the new socket is subscribed: close the older ones.
        for (const [otherId] of this.sockets) if (otherId !== id) this.drop(otherId);
        if (wasOffline) await this.notify("online");
        return;
      }
      case "pusher:error": {
        const code = msg.data?.code;
        m.lastError = `soketi ${code}: ${msg.data?.message || ""}`.trim();
        // 4001: the key is not valid. Move to the next discovered candidate.
        if (code === 4001 && !this.env.PUSHER_KEY) {
          const i = m.keyCandidates.indexOf(sock.key);
          m.key = m.keyCandidates[i + 1] || null;
          m.keyAt = Date.now();
          if (!m.key) m.keyCandidates = [];
        }
        await this.saveMeta();
        return;
      }
      default:
        break;
    }
    if (msg.channel !== this.env.WATCH_USER_ID) return;
    m.lastSubscribedAt = Date.now();
    const kind = classify(msg.data, this.env.ALERT_OWN_FIGHTS === "true");
    if (!kind) return;
    if (m.seen.includes(msg.data.battleId)) return;
    m.seen.push(msg.data.battleId);
    if (m.seen.length > SEEN_MAX) m.seen.splice(0, m.seen.length - SEEN_MAX);
    m.lastEvent = { kind, battleId: msg.data.battleId, at: new Date().toISOString() };
    await this.saveMeta();
    // The alert goes out first; the swap runs alongside it, never ahead of it.
    const alert = this.notify(kind);
    const swap = swapsFor(kind) ? this.swap(msg.data.battleId) : null;
    await alert;
    if (swap) await swap;
  }

  async swap(battleId) {
    if (!this.swapOn() || !(await this.game.signedIn())) return;
    const started = Date.now();
    let result;
    try {
      result = await this.game.swapForBattle(battleId);
    } catch (err) {
      result = { swapped: false, reason: err.message };
    }
    this.meta.lastSwap = { battleId, ...result, ms: Date.now() - started, at: new Date().toISOString() };
    await this.saveMeta();
    const set = result.set === "P1" ? "PvP 1 (you move first)" : "PvP 2 (you move second)";
    await this.notify(result.swapped ? "swapped" : "swapFailed", {
      body: result.swapped ? `Loaded ${set}.` : `Jutsu set not changed: ${result.reason}. Check it in the lobby.`,
    });
  }

  async notify(kind, extra = {}) {
    const name = this.env.WATCH_NAME || "Your ninja";
    const origin = cfg(this.env, "GAME_ORIGIN");
    const messages = {
      attacked: {
        title: `${name} is under attack`,
        body: "A fight just started. Open the game now.",
        priority: "5",
        tags: "rotating_light,crossed_swords",
        click: `${origin}/combat`,
      },
      own: {
        title: `${name} started a fight`,
        body: "A fight just started. Open the game now.",
        priority: "5",
        tags: "rotating_light,crossed_swords",
        click: `${origin}/combat`,
      },
      test: {
        title: "Fight alert test",
        body: "This is how a fight alert will look and sound.",
        priority: "5",
        tags: "rotating_light,crossed_swords",
        click: `${origin}/combat`,
      },
      offline: {
        title: "Fight alert offline",
        body: "Lost the game's live connection for 2 minutes. Retrying every minute.",
        priority: "3",
        tags: "warning",
      },
      online: {
        title: "Fight alert back online",
        body: "Listening for fights again.",
        priority: "2",
        tags: "white_check_mark",
      },
      swapped: {
        title: "Jutsu set loaded",
        priority: "3",
        tags: "scroll",
        click: `${origin}/combat`,
      },
      swapFailed: {
        title: "Jutsu swap failed",
        priority: "4",
        tags: "warning",
        click: `${origin}/combat`,
      },
    };
    const msg = { ...messages[kind], ...extra };
    const headers = { Title: msg.title, Priority: msg.priority, Tags: msg.tags };
    if (msg.click) headers.Click = msg.click;
    // ntfy.sh limits anonymous senders per IP, and Workers share IPs. A token from a free
    // ntfy account moves the limit to the account.
    if (this.env.NTFY_TOKEN) headers.Authorization = `Bearer ${this.env.NTFY_TOKEN}`;
    let lastErr = null;
    for (const wait of [0, 1000, 3000]) {
      if (wait) await new Promise((r) => setTimeout(r, wait));
      try {
        const res = await fetch(`${cfg(this.env, "NTFY_URL")}/${this.env.NTFY_TOPIC}`, {
          method: "POST",
          headers,
          body: msg.body,
        });
        if (res.ok) {
          if (kind === "attacked" || kind === "own") {
            this.meta.alerts += 1;
            this.meta.lastAlert = new Date().toISOString();
          }
          this.meta.lastNotify = { kind, ok: true, at: new Date().toISOString() };
          await this.saveMeta();
          return { ok: true };
        }
        lastErr = `ntfy ${res.status}`;
        if (res.status !== 429 && res.status < 500) break;
      } catch (err) {
        lastErr = err.message;
      }
    }
    this.meta.lastError = `notify: ${lastErr}`;
    this.meta.lastNotify = { kind, ok: false, error: lastErr, at: new Date().toISOString() };
    await this.saveMeta();
    return { ok: false, error: lastErr };
  }
}

/** Call the watcher, retrying once if it reset itself for a newer deploy. */
async function callWatcher(env, path, init = {}) {
  const headers = { "x-deploy-id": env.DEPLOY_ID || "0" };
  for (let attempt = 0; ; attempt++) {
    try {
      return await env.WATCHER.get(env.WATCHER.idFromName("main")).fetch(`https://do${path}`, {
        ...init,
        headers,
      });
    } catch (err) {
      if (attempt >= 2) throw err;
      await new Promise((r) => setTimeout(r, 500));
    }
  }
}

function page(text, status = 200) {
  const safe = text.replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" })[c]);
  return new Response(
    `<!doctype html><meta name="viewport" content="width=device-width"><title>Fight alert</title>` +
      `<p style="font:18px system-ui;margin:2em">${safe}</p>`,
    { status, headers: { "content-type": "text/html; charset=utf-8" } },
  );
}

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    if (url.pathname === "/status") return callWatcher(env, "/status");
    if (url.pathname === "/test") {
      // The topic doubles as the test secret: only someone who already receives the
      // alerts can trigger a test one.
      if (url.searchParams.get("key") !== env.NTFY_TOPIC) {
        return new Response("Forbidden", { status: 403 });
      }
      return callWatcher(env, "/test");
    }
    if (url.pathname === "/auth/start" || url.pathname === "/auth/signout") {
      // Same gate as /test: only someone who already has the topic can start or end a sign-in.
      if (url.searchParams.get("key") !== env.NTFY_TOPIC) {
        return new Response("Forbidden", { status: 403 });
      }
      const origin = encodeURIComponent(url.origin);
      // Hand the redirect to the browser instead of following it here.
      return callWatcher(env, `${url.pathname}?origin=${origin}`, { redirect: "manual" });
    }
    if (url.pathname === "/auth/callback") {
      // Protected by the one-time state value the sign-in started with.
      return callWatcher(env, `/auth/callback${url.search}`);
    }
    if (url.pathname === "/") {
      return new Response("Fight alert is running. See /status.", {
        headers: { "content-type": "text/plain" },
      });
    }
    return new Response("Not found", { status: 404 });
  },
  async scheduled(_event, env) {
    await callWatcher(env, "/ensure");
  },
};
