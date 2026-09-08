// The ONE way tests build the app. It calls the shipped compose() from src/main.mjs, so every
// wiring decision under test is the wiring that ships. The earlier harnesses each built their own
// graph and one of them passed the journal into the Reconciler when production did not, which hid
// a cross-job adoption defect through a whole adversarial pass (audit F2). Only the environment
// primitives and the transport client are substituted here; nothing else may be.
import { IDBFactory } from "fake-indexeddb";
import { compose } from "../src/main.mjs";
import { FakeGame, FakeClient } from "./fakegame.mjs";
import { MemoryStorage, fakeClock } from "./shim.mjs";

export function composeForTest({ game = new FakeGame(), storage = new MemoryStorage(), idb = new IDBFactory(),
                                 clock = fakeClock(), tabId = "tab", client = null, fetchImpl = null } = {}) {
  const deps = compose({
    storage, indexedDB: idb, clock, tabId,
    // no test may reach the network: the game is driven through the FakeClient
    fetchImpl: fetchImpl ?? (async () => { throw new Error("test fetch is not wired; drive the game through FakeClient"); }),
    client: client ?? new FakeClient(game),
    sleep: async (ms) => clock.tick(ms),
  });
  return { ...deps, game, storage, idb, clock };
}
