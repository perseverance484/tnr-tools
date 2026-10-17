# Bloodright website import: source audit

## Recommendation

Extend Forge with a small Bloodright import adapter using the game's existing `skillTree` tRPC procedures. No new game CRUD endpoint or direct database writer is needed. A one-off script in the user's authenticated game page can call the same procedures, but repeated roster imports benefit from Forge's journal, reference resolution, interrupted-create recovery, and read-back verification.

This audit preceded implementation; see [the implemented importer and pilot workflow](../../forge/bloodright/README.md). The pilot package is not yet a validated live push. No live mutations were performed. Repository deployment is not proof of the game website's deployed source version.

## Evidence

- Game source: [studie-tech/TheNinjaRPG@1ccdaf078a58101872675e459c8e755b495d4c83](https://github.com/studie-tech/TheNinjaRPG/tree/1ccdaf078a58101872675e459c8e755b495d4c83).
- Tools baseline: [perseverance484/tnr-tools@5963810895aae4e2deaa61b72424c203752f50c1](https://github.com/perseverance484/tnr-tools/tree/5963810895aae4e2deaa61b72424c203752f50c1).
- Historical Fable tree source (not the current BEE import baseline): [7c1dfdd5e3ee163b90c22694dbb2de94ede08866](https://github.com/perseverance484/tnr-tools/tree/7c1dfdd5e3ee163b90c22694dbb2de94ede08866/docs/design/bloodright/trees).
- Public GET observations on 2026-10-08: `skillTree.getAllFolders({includeHidden:true})` returned five publicly visible folders, including **Blood-Enchanted Eyes**, ID `kvxMu9ntHbNcD6FFHKGo3`, visible, order 120. Public permission filtering still applies despite `includeHidden:true`.
- The BEE design identifies bloodline `ovZIWu28ANn-Cij5TjT8S`. This is a bloodline ID, not the folder ID.
- Public `getAll` reads for Hungry Pulse under both `SKILL` and `BLOODRIGHT`, and a `BLOODRIGHT` listing scoped to that bloodline, each returned zero rows and `nextCursor:null`. This does not establish absence: hidden skills and skills in hidden folders require an eligible staff session. The user supplied Hungry Pulse's [edit URL](https://www.theninja-rpg.com/manual/skillTree/edit/HWq7986PPhl5emkAM3L4a), identifying skill ID `HWq7986PPhl5emkAM3L4a`. A public `skillTree.get` for that exact ID returned undefined (HTTP 200); the later user-provided screenshots establish the visible editor settings listed below. A screenshot is editor evidence, not an API read-back; use the supplied ID for the existing-record binding and fetch its complete current record in the authenticated import preflight.

## Hungry Pulse editor reference

The user supplied four screenshots of the Bloodright editor (`1000018024.jpg`, `1000018025.jpg`, `1000018027.jpg`, and `1000018029.jpg`). Observed fields:

| Field | Editor value |
|---|---|
| Existing skill ID (user's edit URL) | `HWq7986PPhl5emkAM3L4a` |
| Skill target | `SELF` |
| Tier | `1` |
| Bloodline selection | Blood-Enchanted Eyes |
| Folder selection | Blood-Enchanted Eyes |
| Seichi Silver cost | `20` |
| Hidden switch | Appears enabled |
| Prerequisites | No selections shown |
| Skill description | `New skill description` |
| Effect type | `increasepotency` |
| Rounds | `99` |
| Power / power per level | `2` / `0` |
| Effect target | `INHERIT` |
| Friendly fire | Unselected; preserve absence rather than invent a value |
| Calculation | `static` |
| Affected Tag | Lifesteal (`lifesteal`) |
| Affected Elements | Shadow (`["Shadow"]`) |
| Effect description | `placeholder` |
| Effect art/animation/SFX selectors | No selections shown |

The selected image is visible, but its URL is not. Do not infer an image URL from pixels. Fetch the existing row and preserve its image and any fields not explicitly being changed. The name field is visually clipped; use the name from the user's identification and design source, then confirm the full stored string at import time.

These screenshots support `rounds:99` and `seichiSilverCost:20` for Hungry Pulse. They do not by themselves establish those values as universal rules for all nodes or tiers. Treat them as reference settings, without silently applying a roster-wide economic decision. Both descriptions are unfinished draft text, not a wording template for new nodes.

## Website contract

Bloodright nodes are rows in `SkillTree`, with `pathType:"BLOODRIGHT"`. Folders are separate `SkillTreeFolder` rows; folders have no bloodline association. Each node must carry both its own `bloodlineId` and the desired `folderId`.

Source: [skillTree router](https://github.com/studie-tech/TheNinjaRPG/blob/1ccdaf078a58101872675e459c8e755b495d4c83/app/src/server/api/routers/skillTree.ts), [SkillTreeValidator](https://github.com/studie-tech/TheNinjaRPG/blob/1ccdaf078a58101872675e459c8e755b495d4c83/app/src/validators/combat.ts#L1464), [folder/create validators](https://github.com/studie-tech/TheNinjaRPG/blob/1ccdaf078a58101872675e459c8e755b495d4c83/app/src/validators/skillTree.ts), [database schema](https://github.com/studie-tech/TheNinjaRPG/blob/1ccdaf078a58101872675e459c8e755b495d4c83/app/drizzle/schema.ts#L574).

| Operation | Procedure and input | Relevant behavior |
|---|---|---|
| Find existing nodes | `skillTree.getAll({pathType:"BLOODRIGHT",bloodlineId,limit:500,cursor})` | Returns `{data,nextCursor}`; follow every page. Omit `hidden` to include both states accessible to the viewer. Default path is `SKILL`. |
| Read a node | `skillTree.get({id})` | Returns the row with `folder`; subject to hidden-content permissions. |
| Find/reuse folder | `skillTree.getAllFolders({includeHidden:true})` | Returns an array; hidden folders still require permission. Folder names are not unique. |
| Create folder | `skillTree.createFolder({name,image,description,hidden:true,order})` | Returns `{success,message:id}`. Defaults to visible if `hidden` is omitted. |
| Create Bloodright placeholder | `skillTree.create({bloodlineId})` | Returns `{success,message:id}`; starts hidden with no effects, tier 1. |
| Fill/update node | `skillTree.update({id,data})` | Full validator payload; preserves the existing path type. Check `success`, then read back. |
| Update folder | `skillTree.updateFolder({id,data})` | Send the complete desired folder state; omitted optional fields can reset existing values. |

Do not use `skillTree.getAllNames` for Bloodright discovery: it explicitly selects only `SKILL`. For global name conflicts, collect both paths with staff visibility. Skill names are globally unique, including hidden records. Do not adopt a name match without verifying path, bloodline, and identity.

**Creation must pass `bloodlineId`.** Calling `create()` without it makes a `SKILL` placeholder. `update` refuses changing `pathType`, so the ordinary Forge no-input create recipe cannot be copied verbatim.

## Design-to-record mapping

| Design value | Website field |
|---|---|
| Stable local node ID | Import ledger key; resolve to the server-generated skill ID |
| Node name | `name` |
| Flavor and mechanical explanation | `description` |
| Approved node image | `image`; preserve existing image on edits unless explicitly replacing it |
| Foundation / Hidden Art / Advanced Art | `tier` 1 / 2 / 3 for these three-level designs |
| Parent node IDs | `requiredSkillIds`, resolved to actual server IDs |
| Tree bloodline | `bloodlineId` |
| Organizational folder | `folderId` |
| Bloodright mode | `pathType:"BLOODRIGHT"`, `skillType:"DEFAULT"` |
| Self potency modifier | Node `target:"SELF"`, effect `target:"INHERIT"` to match Hungry Pulse |
| Silver purchase price | `seichiSilverCost`; requires an explicit value |
| Ordinary skill-point field | `costSkillPoints:1` satisfies the schema; Bloodright purchasing does not spend this field |
| Draft visibility | `hidden:true` |

Prerequisites use **ALL**, not OR. Parents must be existing lower-tier nodes with the same path and bloodline. Build and finish parents before dependent children. There are no persisted category labels, branch positions, SVG coordinates, or separate tree-title fields. The player Bloodright view renders tier cards with prerequisites; importing records does not import the poster layout. Source: [Bloodright.tsx](https://github.com/studie-tech/TheNinjaRPG/blob/1ccdaf078a58101872675e459c8e755b495d4c83/app/src/layout/Bloodright.tsx).

Purchased Bloodright nodes cannot change bloodline, tier, or prerequisites without refunds. Changes that invalidate dependents are also rejected. An importer must surface these conflicts; it must not automatically refund player purchases or delete existing nodes.

## Effect mapping and runtime issues

Source: [potency tag schemas](https://github.com/studie-tech/TheNinjaRPG/blob/1ccdaf078a58101872675e459c8e755b495d4c83/app/src/validators/combat.ts#L152), [potency resolver](https://github.com/studie-tech/TheNinjaRPG/blob/1ccdaf078a58101872675e459c8e755b495d4c83/app/src/libs/combat/potency.ts), [combat initialization](https://github.com/studie-tech/TheNinjaRPG/blob/1ccdaf078a58101872675e459c8e755b495d4c83/app/src/server/api/routers/combat.ts#L3096).

For the October 8 example's Hungry Pulse bonus, the screenshots show these relevant modifier fields:

```json
{
  "type": "increasepotency",
  "affectedTag": "lifesteal",
  "affectedElements": ["Shadow"],
  "calculation": "static",
  "power": 2,
  "powerPerLevel": 0,
  "rounds": 99,
  "target": "INHERIT"
}
```

This is a field-mapping illustration, **not a complete or validated write payload**. The observed duration is 99 rounds. `INHERIT` follows the skill's self-targeting here. `static` adds two power points: an existing 20% Lifesteal row becomes 22%. `percentage` would multiply it to 20.4%. A plain `lifesteal` tag instead grants a direct passive and is not equivalent to strengthening selected jutsu tags. Positive improvements to `decreasedamagegiven`, `decreasedamagetaken`, etc. still use `increasepotency`: they increase that tag's power. Their display role does not make the Bloodright node enemy-targeted.

The current resolver matches the selected tag AND either the jutsu's authored `elementClassification` or the individual effect row's elements. Thus the old claim that it only checks row elements is stale. Verify classifications of elementless BEE jutsu, especially Hemocure and Unholy Enhancement, from live records before asserting coverage. Row-element fallback remains broader than a strict classification-only selector.

**Hungry Pulse explicitly uses a supported 99-round duration.** Potency's `rounds` schema requires 1–100 and defaults to 3. The skill update retains effects as parsed; self-skill initialization and `realizeTag` retain rounds; round advancement decrements them. Preserve `99` for this record rather than omitting the field and receiving the three-round default. No duration-related engine change is needed to reproduce this reference. Ninety-nine rounds remains finite; an unlimited-passive requirement would be a separate engine change, not a blocker to reproducing the shown setup.

Bloodright effects inherit skill suppression in `RANKED_PVP` and `RANKED_SPARRING`. Hiding a node controls visibility/purchasing; combat initialization does not use hidden flags to remove effects of already purchased nodes. Hidden status is not a substitute for handling existing ownership.

## Current BEE source and historical roster

The user identified the newer five-point SVG design as the intended source. The persisted copy is on `main` at [5963810895aae4e2deaa61b72424c203752f50c1](https://github.com/perseverance484/tnr-tools/commit/5963810895aae4e2deaa61b72424c203752f50c1), committed October 8 UTC. Its [mechanical JSON](../design/bloodright/examples/blood_enchanted_eyes_structural.json) and [structural SVG](../design/bloodright/examples/blood_enchanted_eyes_structural.svg) are the **BEE import baseline for this task**. The surviving `chatgpt/bloodright-*` heads are October 2–4 revisions; inspection of the exposed ChatGPT branch heads and main history located this newer source on main, without establishing its original ChatGPT branch name.

The updated BEE tree has 12 nodes, four independent three-node chains, one point per node, and a five-point budget:

| Foundation | Hidden Art | Advanced Art |
|---|---|---|
| Breaking Point | Opened Veins | Rite of Exsanguination |
| Hungry Pulse | Crimson Thirst | Feast of the Fallen |
| Steady Guard | Closed Wounds | Deathless Vitality |
| Still Pressure | Carrion Fever | Red Pestilence |

Hungry Pulse is local node `p2_t1`: tier 1, no prerequisites, cost 1, and `lifesteal:2`. Bind it to user-supplied existing skill ID `HWq7986PPhl5emkAM3L4a`, subject to staff-session verification, and use that real ID for Crimson Thirst's prerequisite. The snapshot scopes supported bonuses to Shadow jutsu.

Exhaustive enumeration found 106 prerequisite-valid allocations costing at most five points. At most one Advanced Art is reachable; two require six points. All 12 JSON skill names occur in the SVG. The snapshot's `max_advanced:2` does not imply two are reachable: its separate `max_advanced_reachable:1` matches the actual prerequisite graph. The five-point budget agrees with the current game source. **The previous four-versus-five warning does not apply to this BEE revision.**

The older Fable BEE source has 10 nodes, Scarlet Gaze and Iron in the Blood foundations, no Hungry Pulse, no dedicated Afterburn path, and a four-point budget. It must not replace or be blended with the selected BEE source. The main-branch October 3 ruling also describes an older numerical revision; this audit does not alter the ruling ledger.

For historical comparison only, a mechanical scan of all 44 Fable tree JSON files found 408 nodes, all with acquisition cap 4, and no duplicate node names within that population. At five purchases, 42 of those older trees permit two Advanced Arts. That result describes the old roster, not the updated BEE design or an established current roster. Locate each remaining bloodline's latest intended source before compiling it; the BEE example is not a universal balance template.

Ten historical Fable sources have empty qualifying-element lists: Ancient Tailed Demon, Cosmic Ascendant, Dai Kenja, Ha Yanagi, Loup-Garou, Lycanthropy, Megumi Kijo, Musashi Ken, Reptilian, and Yaketsuku Netsu. Whether newer revisions resolve these remains unverified. The importer must reject unresolved classifications: an empty `affectedElements` with a selected tag means unrestricted potency, while `None` reaches unrelated non-elemental rows.

## Forge extension scope

Runtime inspection of the tools baseline confirmed that `skillTree` is absent from the entity list, recipes, procedure registry, and field contract. Both potency effect types are absent from its nested effect contract. It cannot currently execute this import simply by supplying a new manifest.

1. Add audited `skillTree` read/create/update procedures with authentication and rate-limit metadata. Pre-check both `canChangeContent` and `canAccessHiddenSkillTree`; a role denial can return tRPC `UNAUTHORIZED`, which current Forge may misclassify as a lost session.
2. Add a `skillTree` entity and create recipe forwarding `{bloodlineId}`. Add a paginated Bloodright inventory adapter; do not map its names lookup to `getAllNames`.
3. Add field contracts and current potency nested schemas through the existing generators and structural-diff adoption gates. Cover the authoring factory and both validator paths; do not bypass validation.
4. Add `@skillTree:...` references and dependency sorting, plus folder binding. Initially reuse captured folder IDs; generic folder creation needs its own one-step create recipe and duplicate-name handling.
5. Add audited `skillTree.get` full snapshots and folder-specific verification. Existing full-capture allowlisting does not include skill-tree reads; do not broadly allow arbitrary list or user-data persistence.
6. Compile one frozen design revision into full payloads, with explicit prices, duration policy, classifications, hidden status, and mappings for already-made nodes.
7. Reuse create/update journaling, ambiguous-outcome reconciliation, per-entry `success` checks, and fresh read-back comparison. No blind retry after an uncertain create response.

The direct alternative is a user-run page adapter using the same authenticated tRPC APIs. It still needs all payload validation, ID bindings, pagination, outcome checks, and recovery behavior. Direct SQL would discard the router's permissions, hierarchy guards, purchased-node checks, and content notifications; it is not recommended.

## First import acceptance check

Capture Hungry Pulse and the full staff-visible BEE inventory; bind its existing ID and folder instead of recreating it. Use the selected five-point BEE JSON at `5963810895aae4e2deaa61b72424c203752f50c1`. Generate a dry-run diff listing creates, edits, reuse, and conflicts. Preserve Hungry Pulse's observed 20 Silver price and 99-round duration; make each new node's price and duration explicit in the dry-run rather than treating the reference as automatic approval of global defaults. Execute parents before children with nodes hidden, then read back every node and verify bloodline, folder, prerequisites, effects, visibility, and price. Re-running the same import should create zero duplicates. The website's normal publish step remains separate.

The analysis used source inspection, public read-only API checks, direct inspection of Forge's runtime exports/contracts, exhaustive subset enumeration of the 44 historical design trees, a separate enumeration and SVG-name check of the selected five-point BEE source, and inspection of the four user-provided Hungry Pulse editor screenshots. It did not run the game, database tests, authenticated browser checks, or a write/read-back trial. No importer or game code was changed.
