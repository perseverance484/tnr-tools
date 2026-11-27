// Local stand-in for the game site, its Soketi server and ntfy, for an end-to-end run
// with `wrangler dev`. Usage: node test/mock-server.mjs <port>
import http from "node:http";
import { WebSocketServer } from "ws";

const port = Number(process.argv[2] || 8788);
const GOOD_KEY = "goodkey123";
const notifications = [];
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
  } else if (url.pathname === "/_mock/notifications") {
    res.end(JSON.stringify(notifications));
  } else if (url.pathname === "/_mock/fire") {
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
