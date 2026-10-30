// Is a newer game-source commit RELEVANT to forge? (readiness brief section 7)
//
//   node tools/pin_relevance.mjs <checkout-of-pin> <checkout-of-newer>
//
// No network: both arguments are existing checkouts, read only. Prints a per-surface verdict and
// exits 0 when nothing forge relies on changed, 1 when something did.
//
// "Newer" is never a reason to move the pin. This tool answers the only question that is: does the
// client we are about to run still match the contracts it was audited against? It checks two kinds
// of evidence, and both must agree:
//
//   1. DERIVED CONTRACTS. Re-run the two derivation tools against both checkouts and compare the
//      output. This is the strong check: it is what the bundle actually validates against, so a
//      byte-identical result means the pre-send contract did not move, whatever else did.
//   2. DECLARED SURFACES. The files forge reads for behaviour rather than for field sets: the
//      limiter and procedure registration, the six content routers, the upload route, the host
//      page, and the dependency pins. Listed here explicitly so a surface cannot quietly stop
//      being checked; a change in one of them is a finding to read, not automatically a blocker.

import { execFileSync } from "node:child_process";
import { readFileSync, existsSync } from "node:fs";
import { join, dirname } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const [a, b] = process.argv.slice(2);
if (!a || !b || !existsSync(a) || !existsSync(b)) {
  console.error("usage: pin_relevance.mjs <checkout-of-pin> <checkout-of-newer>");
  process.exit(2);
}

// Every game-source file forge's behaviour depends on, and why.
const SURFACES = {
  "app/src/server/api/trpc.ts": "the sliding-window limiter, publicProcedure vs protectedProcedure",
  "app/src/server/api/root.ts": "which routers exist at which path",
  "app/src/server/api/routers/jutsu.ts": "create/update/get/getAllNames semantics",
  "app/src/server/api/routers/item.ts": "create takes {type}; update/get/getAllNames; getItemWithCraftingRequirements (recipe full-persist point read)",
  "app/src/server/api/routers/quests.ts": "create/update/get/getAllNames",
  "app/src/server/api/routers/profile.ts": "AI create, updateAi kit sync, getAi, getAllAiNames",
  "app/src/server/api/routers/ai.ts": "toggleAiProfile, getAiProfile, updateAiProfile",
  "app/src/server/api/routers/asset.ts": "gameAsset create (anonymous placeholder) and update",
  "app/src/server/api/routers/bloodline.ts": "create/update/get/getAllNames",
  "app/src/validators/combat.ts": "jutsu/item/bloodline validators and the effect tag union",
  "app/src/validators/objectives.ts": "quest validator and the objective union",
  "app/src/validators/ai.ts": "AI rule conditions and actions",
  "app/src/validators/asset.ts": "gameAsset validator",
  "app/src/server/api/routers/petSpecies.ts": "petSpecies create (one step, id in message)/update/get/getAll; default-jutsu refusals",
  "app/src/validators/petSpecies.ts": "PetSpeciesValidator and its refinements (mirrored in src/runner/pets.mjs)",
  "app/src/libs/pets/abilities.ts": "isPetJutsuAllowed: what a pet can equip (mirrored in src/runner/pets.mjs)",
  "app/src/server/api/routers/badge.ts": "badge placeholder create/update/get/getAllNames (src/runner/catalog.mjs)",
  "app/src/server/api/routers/title.ts": "title placeholder create/update/get/getAllNames (src/runner/catalog.mjs)",
  "app/src/validators/badge.ts": "BadgeValidator",
  "app/src/validators/title.ts": "TitleValidator and the inline TitleEffectSchema members",
  "app/src/server/utils/titleRewards.ts": "reward_titles must name unarchived titles (lints.mjs TITLE)",
  "app/src/validators/item.ts": "ItemVariantValidator and upsertItemVariantInputSchema (src/runner/variants.mjs)",
  // 3314d122 moved each router's database statements into src/queries/<router>.ts: placeholder
  // inserts, what get/list return, and the variant insert/update guards live there now
  "app/src/queries/jutsu.ts": "jutsu placeholder insert, get and name list",
  "app/src/queries/item.ts": "item placeholder insert, get, name list; variant insert/update/list (src/runner/variants.mjs)",
  "app/src/queries/quests.ts": "quest placeholder insert, get and name list",
  "app/src/queries/profile.ts": "AI placeholder insert, getAi and the name list",
  "app/src/queries/asset.ts": "gameAsset placeholder insert (\"Placeholder\"), get and name list",
  "app/src/queries/bloodline.ts": "bloodline placeholder insert, get and name list",
  "app/src/queries/petSpecies.ts": "species insert/update/get/getAll",
  "app/src/queries/badge.ts": "badge placeholder insert, get and name list",
  "app/src/queries/title.ts": "title placeholder insert, get/getAll and the reward-title check",
  "app/src/validators/rewards.ts": "the reward field block shared by objectives",
  "app/src/validators/base.ts": "idsWithNumberField (opponentAIs, attackers)",
  "app/drizzle/schema.ts": "userData columns behind insertAiSchema",
  "app/drizzle/constants.ts": "the enum VALUE lists the validators import. Forge derives key sets, "
    + "never enums (the 45g rule), so a change here cannot make forge reject what the server "
    + "accepts - but a reviewer should see it rather than have it sit outside the gate",
  "app/src/app/api/uploadthing/core.ts": "the image upload route",
  "app/src/proxy.ts": "whether an unmatched path still bypasses the Clerk layout",
  "app/next.config.mjs": "experimental.globalNotFound, which is what makes /forge a host",
  "app/src/app/global-not-found.tsx": "the host page: no ClerkProvider, no tRPC provider",
  "app/package.json": "the tRPC, superjson, zod and uploadthing versions the wire format follows",
};

const sha = (root) => {
  try { return execFileSync("git", ["-C", root, "rev-parse", "HEAD"], { encoding: "utf8" }).trim(); }
  catch { return "(not a git checkout)"; }
};
const derive = (tool, root) => execFileSync(process.execPath, [join(here, tool), root], { encoding: "utf8", maxBuffer: 64 << 20 });

let relevant = 0;
console.log(`pin      ${a}  ${sha(a)}`);
console.log(`newer    ${b}  ${sha(b)}`);

console.log("\n-- derived contracts (what the bundle validates against) --");
for (const tool of ["derive_fields.mjs", "derive_nested.mjs"]) {
  const same = derive(tool, a) === derive(tool, b);
  if (!same) relevant++;
  console.log(`${same ? "same    " : "CHANGED "} ${tool}`);
}

console.log("\n-- declared surfaces (behaviour forge reads rather than derives) --");
for (const [file, why] of Object.entries(SURFACES)) {
  const pa = join(a, file), pb = join(b, file);
  const ea = existsSync(pa), eb = existsSync(pb);
  const same = ea && eb && readFileSync(pa, "utf8") === readFileSync(pb, "utf8");
  if (!same) relevant++;
  console.log(`${same ? "same    " : !ea ? "ADDED   " : !eb ? "REMOVED " : "CHANGED "} ${file}  (${why})`);
}

console.log(relevant
  ? `\n${relevant} relevant surface(s) changed: read each one before deciding whether to move the pin.`
  : "\nNothing forge relies on changed. Keeping the pin is the evidence-backed choice, not inertia.");
process.exit(relevant ? 1 : 0);
