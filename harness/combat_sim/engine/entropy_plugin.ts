/**
 * Bun preload (run.sh passes it with --preload): before the pinned combat router is loaded, point its single
 * node:crypto randomInt import at ./entropy.ts, so opening spawn cells come from the run's seeded source and the
 * engine places every fighter, pet and pet passive itself. The rewrite is that one import line and nothing else;
 * if the line is not found exactly once (a different engine pin), the run stops.
 */
import { plugin } from "bun";

const IMPORT_LINE = 'import { randomInt as secureRandomInt } from "node:crypto";';
const ENTROPY = `${import.meta.dir}/entropy.ts`;

plugin({
  name: "tnr-sim-seeded-spawn-entropy",
  setup(build) {
    build.onLoad({ filter: /[\\/]src[\\/]server[\\/]api[\\/]routers[\\/]combat\.ts$/ }, async (args) => {
      const src = await Bun.file(args.path).text();
      const hits = src.split(IMPORT_LINE).length - 1;
      if (hits !== 1) throw new Error(`SIM: expected the router's node:crypto randomInt import once in ${args.path}, found ${hits}`);
      const contents = src.replace(IMPORT_LINE, `import { randomInt as secureRandomInt } from ${JSON.stringify(ENTROPY)};`);
      return { contents, loader: "ts" };
    });
  },
});
