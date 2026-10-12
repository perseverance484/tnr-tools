/**
 * Negative self-test for gate enforcement (not part of the evidence suite).
 * Records one deliberately failing required check; `requireClean` must fail
 * this file, `flush` must set a nonzero exit code, and the written evidence
 * must report failed: 1 so tools/check_evidence.py rejects it.
 */
import { afterAll, it } from "bun:test";
import { Evidence, requireClean } from "../tnr_ghost_ship_stage2/lib/report";

const NEG = new Evidence("NEG");
afterAll(() => NEG.flush({ note: "deliberate failure; gate-enforcement self-test" }));

it("records a passing and a deliberately failing required check", () => {
  NEG.check("control: passing check", true);
  NEG.check("deliberate failure", false);
});

requireClean(NEG);
