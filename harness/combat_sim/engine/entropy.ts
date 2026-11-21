/**
 * Seeded stand-in for node:crypto's randomInt, which the pinned combat router imports for opening spawn cells
 * (`import { randomInt as secureRandomInt } from "node:crypto"`). entropy_plugin.ts points that one import here
 * before the router loads; nothing else in the engine changes. A run installs its source with setRandomIntSource
 * (seedRun does); a draw with no source installed throws instead of falling back to real randomness.
 */
type Source = (span: number) => number;
let source: Source | null = null;
let draws = 0;

export const setRandomIntSource = (fn: Source | null) => {
  source = fn;
};
export const randomIntDraws = () => draws;

export function randomInt(a: number, b?: number | ((...x: unknown[]) => void), cb?: unknown): number {
  if (typeof b === "function" || cb !== undefined) throw new Error("SIM: callback form of randomInt is not supported");
  const [lo, hi] = b === undefined ? [0, a] : [a, b];
  if (!Number.isSafeInteger(lo) || !Number.isSafeInteger(hi) || hi <= lo) throw new RangeError(`SIM: randomInt(${a}, ${b}) range is empty`);
  if (!source) throw new Error("SIM: the engine drew node:crypto randomInt with no seeded source installed");
  const v = source(hi - lo);
  if (!Number.isInteger(v) || v < 0 || v >= hi - lo) throw new Error(`SIM: entropy source returned ${v} for span ${hi - lo}`);
  draws++;
  return lo + v;
}
