> **STALE - archived 2026-08-28 (rollout Stage 1).** moved to building skill references/pipeline.md.
> Do not build from this file.

# 11_TECH_source_map.md - Where data lives and which copy to trust

Three tiers of data, with a hard rule about which one you may write from.

## Tier 1: the trimmed catalogs (40, 41, 42, 43, 47)

**LOOKUP ONLY. Never compose a write payload from these.**

They answer: does this name already exist, what id is it, what level is that AI, which quests use this enemy, what does this jutsu roughly do, is this asset real art or a placeholder.

Every one carries a `_coverage` block naming exactly how many fields the full record has, how many are kept, and what was dropped. Read it before assuming a field is absent from the game rather than absent from the file. The most dangerous omissions:

- **Jutsu and item effects are display strings, not payload objects.** A real effect row has 16 fields including `appearAnimation`, `appearSfx`, `calculation`, `direction`, `generalTypes`, `statTypes`, `powerPerLevel`. The catalog shows `"damage 45"`. Composing from that produces a record the server rejects, or worse, accepts with silent cosmetic loss.
- **The quest catalog contains NO objective graph.** `nodes` and `tasks` are counts. Node ids, descriptions, dialog choices, edges, scenes and per-node rewards are all absent.
- **The AI catalog carries 3 of 12 stat fields**, offence only.

## Tier 2: the full exemplars (49)

One complete untrimmed record per entity: jutsu, item, asset, quest, AI. Every field, real values, straight from a live harvest.

**This is the shape reference.** When you need to know what a payload looks like, read this, not a guide's field table and not a trimmed catalog. The AI exemplar alone has 160 fields.

The quest exemplar keeps one objective per task type so it stays readable, but every field on each objective is complete.

## Tier 3: the harvest dumps

Full fidelity, every record, ~25 MB per set. Not stored in this stack. dauntless runs `TNR_harvester.js` and uploads them; they live in the working folder for the session.

**Pull from a harvest when:** you are editing a specific record and need its exact current state, you are reproducing an effects array, you are reading or rewriting a quest graph, or the catalogs are older than the last push.

## Regeneration

```
python3 refresh_catalogs.py <folder of harvests> <output folder>
```

Picks the newest dump of each kind and rewrites catalogs 40, 41, 42, 43 and 47 with fresh contents and a fresh `_coverage` block. Shapes never change, only contents, so a refresh is a drop-in replacement.

Run it after any session with pushes. The catalogs are snapshots and say so; an id looked up in a stale catalog is the same class of error as an invented field.

## The rule in one line

Catalogs to find it, exemplars to shape it, harvests to write it.
