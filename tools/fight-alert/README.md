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
- No game API calls and no game credentials. The Pusher app key is the public one the game
  page ships; the Worker finds it in the site's scripts (or set `PUSHER_KEY`).
- One alert per battle id (last 50 remembered). Fights the account starts are not alerted
  unless `ALERT_OWN_FIGHTS = "true"`.
- An outbound socket keeps a Durable Object alive for up to 15 minutes, so the socket is
  replaced every 14 minutes (the new one subscribes before the old one closes). A 1-minute
  alarm and a 1-minute cron reconnect after drops, deploys or evictions.
- After 2 minutes without a connection it sends one low-priority "offline" notice, and a
  "back online" notice when it recovers.

Endpoints: `/status` (connection state, last event), `/test?key=<NTFY_TOPIC>` (sends a
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
  --var NTFY_TOPIC:testtopic
curl localhost:8787/__scheduled
curl "127.0.0.1:8788/_mock/fire?ch=user_37qazcrgUPldBPI65bb25DQiCjz&id=b1&def=1"
curl 127.0.0.1:8788/_mock/notifications
```

## Caveat

This relies on the game's per-player live channels staying public. If they become private,
the Worker stops receiving events and sends the offline notice.
