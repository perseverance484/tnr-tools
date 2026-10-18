// Bundle selected TheNinjaRPG combat functions into one offline ES module (no network, no live game).
// Usage: node scripts/bloodright_engine/build_engine.mjs GAME_CHECKOUT ENTRY.ts OUT.mjs
// GAME_CHECKOUT must be studie-tech/TheNinjaRPG at the Bloodright contract pin (94f9d84).
import { build } from "../../forge/node_modules/esbuild/lib/main.js";
const APP = `${process.argv[2]}/app`;
const entry = process.argv[3], out = process.argv[4];
const missing = new Set();
const pkgs = { name: "pkgs", setup(b) {
  b.onResolve({ filter: /^[^./@]|^@[^/]+\// }, a => {
    if (a.path === "zod" || a.path.startsWith("zod/")) return { path: a.path, external: true };
    missing.add(a.path); return { path: a.path, namespace: "stub" };
  });
  b.onLoad({ filter: /.*/, namespace: "stub" }, a => ({ contents: `const h={get:(t,k)=>k==="__esModule"?true:(k==="default"?p:p)};const p=new Proxy(function(){return p},{get:(t,k)=>k===Symbol.toPrimitive?()=>"":p,apply:()=>p,construct:()=>p});module.exports=p;`, loader: "js" }));
}};
await build({ entryPoints: [entry], absWorkingDir: APP, tsconfig: `${APP}/tsconfig.json`, bundle: true, format: "esm", platform: "node", outfile: out, plugins: [pkgs], logLevel: "error", jsx: "automatic", nodePaths: [new URL("../../forge/node_modules", import.meta.url).pathname] }).catch(e => { console.log(String(e.message).slice(0, 3000)); process.exit(1); });
console.log("stubbed:", [...missing].sort().join(", "));
