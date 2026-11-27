# Fight alert

Sends a loud phone notification (ntfy) within a few seconds of a fight starting on a TNR
account, when someone else started it.

## How it works

- A Cloudflare Worker with one Durable Object keeps a websocket open to the game's live
  server (Soketi, Pusher protocol) and listens on the account's own public channel, which is
  the account's user id. The game's web page subscribes to the same channel.
- When the game creates a battle it sends `{type: "battle", battleId, isDefender}` on that
  channel (`app/src/server/api/routers/combat.ts` in studie-tech/TheNinjaRPG). With
  `isDefender: true` the Worker posts a priority-5 message to `ntfy.sh/<NTFY_TOPIC>`.
- The alert makes no game API calls. The Pusher app key is the public one the game
  page ships; the Worker finds it in the site's scripts (or set `PUSHER_KEY`).
- One alert per battle id (last 50 remembered). Fights the account starts are not alerted
  unless `ALERT_OWN_FIGHTS = "true"`.
- An outbound socket keeps a Durable Object alive for up to 15 minutes, so the socket is
  replaced every 14 minutes (the new one subscribes before the old one closes). A 1-minute
  alarm and a 1-minute cron reconnect after drops, deploys or evictions.
- After 2 minutes without a connection it sends one low-priority "offline" notice, and a
  "back online" notice when it recovers.

## Lobby jutsu swap

For a fight someone else starts, the Worker can load the right jutsu set during the
15-second lobby: the P1 set when the account moves first, the P2 set when it moves second.

- Per fight: the alert goes out first, then `combat.getBattle` (turn order and when round 1
  starts) and `combat.updateCombatLoadout` with the jutsu loadout only. Nothing else: no
  items, no ready, no attacks, nothing once round 1 has started (it stops 0.5 s before).
- A low-priority ntfy line follows with the set it loaded, or a louder one if it couldn't.
- It runs only with `SWAP_ENABLED = "true"`, both loadout ids set, and a game sign-in. To
  sign in, open `/auth/start?key=<NTFY_TOPIC>` on the phone and approve as the watched
  account. The Worker uses the game's own OAuth (the one its MCP endpoint uses), keeps the
  refresh token in the Durable Object's storage, and refuses a sign-in for any other
  account. `/auth/signout?key=<NTFY_TOPIC>` forgets it.
- Two game requests per fight count toward the game's 30-a-minute MCP limit for the account.

Endpoints: `/status` (connection state, last event, swap state, deploy id), `/test?key=<NTFY_TOPIC>` (sends a
sample alert).

Cost: one always-on Durable Object is about 10,800 GB-s a day, inside the free plan's
13,000 GB-s a day. ntfy.sh is free.

## Setup

1. Install the ntfy app on the phone and subscribe to the topic name (server ntfy.sh).
   On Android, turn on instant delivery for the topic and let it ignore battery
   optimisation.
2. In Cloudflare, create an API token from the "Edit Cloudflare Workers" template and note
   the account id. The account needs a workers.dev subdomain.
3. Add repository secrets `CLOUDFLARE_API_TOKEN`, `CLOUDFLARE_ACCOUNT_ID` and `NTFY_TOPIC`.
4. Run the `fight-alert-deploy` workflow. It runs the tests, deploys, waits for the Worker to
   connect and sends one test alert.

## Local test

```
npm ci
npm test
node test/mock-server.mjs 8788 &
npx wrangler dev --test-scheduled --var GAME_ORIGIN:http://127.0.0.1:8788 \
  --var SOKETI_URL:ws://127.0.0.1:8788 --var NTFY_URL:http://127.0.0.1:8788/ntfy \
  --var NTFY_TOPIC:testtopic --var MCP_URL:http://127.0.0.1:8788/api/mcp
curl localhost:8787/__scheduled
curl -L "localhost:8787/auth/start?key=testtopic"   # mock sign-in, auto-approved
curl "127.0.0.1:8788/_mock/fire?ch=user_37qazcrgUPldBPI65bb25DQiCjz&id=b1&def=1"
curl 127.0.0.1:8788/_mock/notifications
curl 127.0.0.1:8788/_mock/game                      # game calls the swap made
```

## Caveat

This relies on the game's per-player live channels staying public. If they become private,
the Worker stops receiving events and sends the offline notice.
