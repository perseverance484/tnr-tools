import { mkdirSync, writeFileSync } from "node:fs";
import { join } from "node:path";

const OUT = process.env.TNR_OUT ?? "";

/**
 * Deterministic JSON: battle objects are omitted (they carry wall-clock
 * timestamps), object keys are sorted, non-integers rounded to 3 places.
 */
const stableReplacer = (_k: string, v: unknown) => {
  if (typeof v === "number" && !Number.isInteger(v)) return Math.round(v * 1000) / 1000;
  if (v && typeof v === "object" && !Array.isArray(v)) {
    if ("usersState" in (v as object)) return "[battle state omitted]";
    return Object.fromEntries(Object.entries(v as object).sort(([a], [b]) => (a < b ? -1 : a > b ? 1 : 0)));
  }
  return v;
};

/** Accumulates structured evidence per gate and writes it as JSON on flush. */
export class Evidence {
  readonly gate: string;
  readonly data: Record<string, unknown> = {};
  readonly assertions: { name: string; pass: boolean; detail?: unknown }[] = [];
  constructor(gate: string) {
    this.gate = gate;
  }
  put(key: string, value: unknown) {
    this.data[key] = value;
  }
  check(name: string, pass: boolean, detail?: unknown) {
    this.assertions.push({ name, pass, detail });
    return pass;
  }
  flush(extra: Record<string, unknown> = {}) {
    if (!OUT) return;
    mkdirSync(OUT, { recursive: true });
    const failed = this.assertions.filter((a) => !a.pass).length;
    writeFileSync(
      join(OUT, `${this.gate.toLowerCase()}.json`),
      `${JSON.stringify(
        { gate: this.gate, assertions: this.assertions.length, failed, ...extra, data: this.data, checks: this.assertions },
        stableReplacer,
        1,
      )}\n`,
    );
  }
}
