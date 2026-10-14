import { expect, it } from "bun:test";
import { mkdirSync, writeFileSync } from "node:fs";
import { join } from "node:path";

const OUT = process.env.TNR_OUT ?? "";

const stable = (_k: string, v: unknown) => {
  if (typeof v === "number" && !Number.isInteger(v)) return Math.round(v * 1000) / 1000;
  if (v && typeof v === "object" && !Array.isArray(v))
    return Object.fromEntries(Object.entries(v as object).sort(([a], [b]) => (a < b ? -1 : a > b ? 1 : 0)));
  return v;
};

/** Structured per-gate evidence; `volatile` keys (timings) are written to a separate file. */
export class Evidence {
  readonly data: Record<string, unknown> = {};
  readonly volatile: Record<string, unknown> = {};
  readonly checks: { name: string; pass: boolean; detail?: unknown }[] = [];
  /** Engine/design defects reproduced on purpose. Recorded, never counted as passes. */
  readonly findings: { id: string; summary: string; reproduced: boolean; detail?: unknown }[] = [];
  constructor(readonly gate: string) {}
  finding(id: string, summary: string, reproduced: boolean, detail?: unknown) {
    this.findings.push({ id, summary, reproduced, ...(detail === undefined ? {} : { detail }) });
  }
  put(key: string, value: unknown) { this.data[key] = value; }
  timing(key: string, value: unknown) { this.volatile[key] = value; }
  check(name: string, pass: boolean, detail?: unknown) {
    this.checks.push({ name, pass, ...(detail === undefined ? {} : { detail }) });
    return pass;
  }
  failures() { return this.checks.filter((c) => !c.pass).map((c) => c.name); }
  flush() {
    const failed = this.failures().length;
    if (failed > 0) process.exitCode = 1;
    if (!OUT) return;
    mkdirSync(OUT, { recursive: true });
    const base = { gate: this.gate, assertions: this.checks.length, failed, findings: this.findings };
    // Passing checks keep their names only; failures keep their detail for diagnosis.
    const checks = this.checks.map((c) => (c.pass ? { name: c.name, pass: true } : c));
    writeFileSync(join(OUT, `${this.gate}.json`), `${JSON.stringify({ ...base, data: this.data, checks }, stable, 1)}\n`);
    if (Object.keys(this.volatile).length)
      writeFileSync(join(OUT, `${this.gate}.timings.json`), `${JSON.stringify(this.volatile, stable, 1)}\n`);
  }
}

/** Last test of a file: fails `bun test` when any recorded check failed (or none ran). */
export const requireClean = (...gates: Evidence[]) =>
  it(`evidence: no failed checks (${gates.map((g) => g.gate).join(", ")})`, () => {
    for (const g of gates) {
      g.flush();
      expect(g.checks.length).toBeGreaterThan(0);
      expect(g.failures()).toEqual([]);
    }
  });
