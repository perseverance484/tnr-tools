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
