// Fight alert for one TNR account.
//
// Listens on the account's own live channel on the game's Soketi (Pusher protocol) server,
// the same public channel the game's web page subscribes to. When the server announces a
// battle where the account is the defender, it sends a max-priority ntfy notification.
//
// Read-only: it makes no game API calls, holds no game credential and never acts in game.

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

export class FightWatcher {
  constructor(state, env) {
    this.state = state;
    this.env = env;
    this.sockets = new Map(); // id -> { ws, subscribed, openedAt, pingTimer }
    this.nextSocketId = 1;
    this.connecting = false;
    this.meta = null;
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
        connected: this.healthy(),
        sockets: this.sockets.size,
        lastSubscribedAt: m.lastSubscribedAt ? new Date(m.lastSubscribedAt).toISOString() : null,
        keyFound: !!m.key,
        lastEvent: m.lastEvent,
        lastAlert: m.lastAlert,
        alertsSent: m.alerts,
        lastError: m.lastError,
        lastNotify: m.lastNotify || null,
      });
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
    await this.notify(kind);
  }

  async notify(kind) {
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
        body: "Open the game to take your turn.",
        priority: "4",
        tags: "crossed_swords",
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
    };
    const msg = messages[kind];
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

const watcher = (env) => env.WATCHER.get(env.WATCHER.idFromName("main"));

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    if (url.pathname === "/status") return watcher(env).fetch("https://do/status");
    if (url.pathname === "/test") {
      // The topic doubles as the test secret: only someone who already receives the
      // alerts can trigger a test one.
      if (url.searchParams.get("key") !== env.NTFY_TOPIC) {
        return new Response("Forbidden", { status: 403 });
      }
      return watcher(env).fetch("https://do/test");
    }
    if (url.pathname === "/") {
      return new Response("Fight alert is running. See /status.", {
        headers: { "content-type": "text/plain" },
      });
    }
    return new Response("Not found", { status: 404 });
  },
  async scheduled(_event, env) {
    await watcher(env).fetch("https://do/ensure");
  },
};
