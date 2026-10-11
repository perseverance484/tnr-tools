/**
 * Negative self-test for the flush-only path (not part of the evidence suite).
 * No requireClean and no TNR_OUT: every bun test passes, but the failed
 * required check recorded here must still make `bun test` exit nonzero
 * through Evidence.flush setting process.exitCode.
 */
import { afterAll, it } from "bun:test";
import { Evidence } from "../tnr_ghost_ship_consume/lib/report";

const NEG = new Evidence("NEGFLUSH");
afterAll(() => NEG.flush());

it("records a deliberately failing required check without failing a bun assertion", () => {
  NEG.check("deliberate failure (flush-only)", false);
});
