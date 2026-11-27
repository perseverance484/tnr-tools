// Local stand-in for the game site, its Soketi server and ntfy, for an end-to-end run
// with `wrangler dev`. Usage: node test/mock-server.mjs <port>
import http from "node:http";
import { WebSocketServer } from "ws";

const port = Number(process.argv[2] || 8788);
const GOOD_KEY = "goodkey123";
const notifications = [];
const gameCalls = [];
const battles = new Map(); // battleId -> { activeUserId, roundStartAt }
const WATCHED = "user_37qazcrgUPldBPI65bb25DQiCjz";
let issued = 0;

const readBody = (req) =>
  new Promise((r) => {
    let b = "";
    req.on("data", (c) => (b += c));
    req.on("end", () => r(b));
  });
const sockets = new Set();

const server = http.createServer((req, res) => {
  const url = new URL(req.url, `http://127.0.0.1:${port}`);
  if (url.pathname === "/") {
    res.end('<script src="/_next/static/chunks/layout.js"></script>');
  } else if (url.pathname === "/_next/static/chunks/layout.js") {
    res.end(`n=new P("${GOOD_KEY}",{wsHost:"soketi.theninja-rpg.com",forceTLS:!0})`);
  } else if (req.method === "POST" && url.pathname.startsWith("/ntfy/")) {
    let body = "";
    req.on("data", (c) => (body += c));
    req.on("end", () => {
      notifications.push({ topic: url.pathname.slice(6), title: req.headers.title,
        priority: req.headers.priority, click: req.headers.click, body, at: Date.now() });
      res.end("{}");
    });
  } else if (url.pathname === "/.well-known/oauth-authorization-server") {
    const o = `http://127.0.0.1:${port}`;
    res.end(JSON.stringify({ issuer: o, authorization_endpoint: `${o}/oauth/authorize`,
      token_endpoint: `${o}/oauth/token`, registration_endpoint: `${o}/oauth/register`,
      scopes_supported: ["openid", "profile", "email", "offline_access"] }));
  } else if (url.pathname === "/oauth/register") {
    readBody(req).then((b) => res.end(JSON.stringify({ client_id: "client1", ...JSON.parse(b) })));
  } else if (url.pathname === "/oauth/authorize") {
    // Auto-approve: send the browser straight back with a code.
    const back = new URL(url.searchParams.get("redirect_uri"));
    back.searchParams.set("code", "code1");
    back.searchParams.set("state", url.searchParams.get("state"));
    res.writeHead(302, { location: back.toString() });
    res.end();
  } else if (url.pathname === "/oauth/token") {
    readBody(req).then((b) => {
      issued += 1;
      gameCalls.push({ token: Object.fromEntries(new URLSearchParams(b)) });
      res.end(JSON.stringify({ access_token: `at${issued}`, refresh_token: `rt${issued}`, expires_in: 3600 }));
    });
  } else if (url.pathname === "/api/mcp") {
    readBody(req).then((b) => {
      const { endpointName, input } = JSON.parse(b).params.arguments;
      gameCalls.push({ endpointName, input, auth: req.headers.authorization, at: Date.now() });
      let out;
      if (endpointName === "profile.getUser") {
        out = { "userData.userId": WATCHED, "userData.username": "dauntless" };
      } else if (endpointName === "combat.getBattle") {
        const bt = battles.get(input.battleId);
        out = { "battle.activeUserId": bt.activeUserId, "battle.roundStartAt": bt.roundStartAt,
          "battle.battleType": "COMBAT" };
      } else {
        out = { success: true, message: "Loadout updated" };
      }
      const rpc = { jsonrpc: "2.0", id: 1, result: { content: [{ type: "text", text: JSON.stringify(out) }] } };
      res.setHeader("content-type", "text/event-stream");
      res.end(`event: message\ndata: ${JSON.stringify(rpc)}\n\n`);
    });
  } else if (url.pathname === "/_mock/game") {
    res.end(JSON.stringify(gameCalls));
  } else if (url.pathname === "/_mock/notifications") {
    res.end(JSON.stringify(notifications));
  } else if (url.pathname === "/_mock/fire") {
    battles.set(url.searchParams.get("id"), {
      activeUserId: url.searchParams.get("first") === "1" ? WATCHED : "user_attacker",
      roundStartAt: new Date(Date.now() + 15000).toISOString(),
    });
    const payload = {
      type: "battle",
      battleId: url.searchParams.get("id"),
      isDefender: url.searchParams.get("def") === "1",
    };
    for (const ws of sockets) {
      if (ws.channels.has(url.searchParams.get("ch"))) {
        ws.send(JSON.stringify({ event: "event", channel: url.searchParams.get("ch"),
          data: JSON.stringify(payload) }));
      }
    }
    res.end(JSON.stringify({ firedTo: [...sockets].filter((w) => w.channels.size).length,
      at: Date.now() }));
  } else if (url.pathname === "/_mock/sockets") {
    res.end(JSON.stringify([...sockets].map((w) => ({ key: w.key, channels: [...w.channels] }))));
  } else {
    res.statusCode = 404;
    res.end("");
  }
});

const wss = new WebSocketServer({ noServer: true });
server.on("upgrade", (req, socket, head) => {
  wss.handleUpgrade(req, socket, head, (ws) => {
    const key = new URL(req.url, "http://x").pathname.split("/")[2];
    ws.key = key;
    ws.channels = new Set();
    sockets.add(ws);
    ws.on("close", () => sockets.delete(ws));
    if (key !== GOOD_KEY) {
      ws.send(JSON.stringify({ event: "pusher:error",
        data: { code: 4001, message: `App key ${key} does not exist.` } }));
      ws.close();
      return;
    }
    ws.send(JSON.stringify({ event: "pusher:connection_established",
      data: JSON.stringify({ socket_id: "1.1", activity_timeout: 30 }) }));
    ws.on("message", (raw) => {
      const msg = JSON.parse(raw);
      if (msg.event === "pusher:subscribe") {
        ws.channels.add(msg.data.channel);
        ws.send(JSON.stringify({ event: "pusher_internal:subscription_succeeded",
          channel: msg.data.channel, data: "{}" }));
      }
    });
  });
});
server.listen(port, "127.0.0.1", () => console.log(`mock on ${port}`));
