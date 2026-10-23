# Jutsu upgrade priority targets (2026-10-23)

- **Goal (director):** heavily used jutsu that still need the premium treatment given to the event jutsu and the
  BEE/bloodline families: a BEE-standard emblem icon plus a description and battle line in the house style.
- **Data:** public reads only (session read access granted by the director, no credentials): usage per jutsu from
  `data.getJutsuBalanceStatistics` (summed battle uses, all battle types; plus players with it equipped) and the full
  non-AI catalog, in `harvests/inbox/tnr_results_1792732003454.json`.
- **Excluded as already done:** the starter 6, the 13 overhaul-register jutsu, the event 10 (scroll-jutsu set),
  Tenryūseigan, and the Vaporia, Bakuhatsu, Aerathiel and BEE families (names found in `docs/design`, `docs/handoffs`
  or the style references).
- **Icon need:** nearly every remaining top-40 icon is the old full-scene style (a posed ninja in a landscape), which
  does not read at 32 px. The text need varies: some lines were already rewritten in the 2026-10 battle-line pass.

## Recommended batch 1: the ten most-used NORMAL jutsu (any player can learn them)

| # | Jutsu | Uses | Equipped | Icon | Text |
|---|---|---|---|---|---|
| 1 | Chakra Overflow | 107,720 | 298 | off-style portrait (glowing monk) | battle line over-long, explains mechanics |
| 2 | Summoning: Titanoboa | 23,126 | 322 | cartoon snake scene | fine; premium pass |
| 3 | Crimson Vein | 19,452 | 166 | posed figure | fine; premium pass |
| 4 | Abyssal Wraith | 13,512 | 144 | posed scene | battle line rambles, repeats itself |
| 5 | Clone Technique | 12,565 | 252 | posed figure | fine; premium pass |
| 6 | Faint Shadow | 11,731 | 145 | silhouette | fine; premium pass |
| 7 | Body Flicker | 11,476 | 145 | generic running ninja | fine; premium pass |
| 8 | Terra Shift | 11,085 | 40 | posed scene | battle line long, misses the damage |
| 9 | Crescent Strike | 10,790 | 156 | posed figure | fine; premium pass |
| 10 | Rotting Bite | 10,409 | 158 | posed scene | battle line names "lifesteal" (mechanics) |

## Batch 2 candidates (NORMAL / FORBIDDEN)

Glyph Blade, Liver Shot, Molten Fury (one-line mechanical descriptions), Dragon King's Impact (forbidden; premium
tier), Lightning Release: Holy Strike, Swallow's Flight, Chakra Invigoration, Cyclone Palm Strike, Spectral Counter,
Earth Release: Dragon's Tomb, Burning Coil, Shrapnel Clone Barrage (training warning missing its line break and colour).

## Bloodline family sets (do as sets, like Aerathiel)

- **Shinrai Ou:** Izanagi's Hammer, Indra's Storm Cloak, Storm Style: Daibutsu Thunder, Storm Style: Divine Railgun
  (about 50k uses across four jutsu in the top 40).
- **Musashi Ken:** Iaijutsu (35,559 uses, third overall) and Iaido.
- **Tenohira Musei:** Yin-Yang Cascade, Silent Rift, Silent Palm Strike.
- **Shiroi Youso:** Element Divine, Wind Release (both share an icon with other jutsu).
- Singles: Petal Nightmare (Ha Yanagi), Shadow Tether (Oblivion Seal), Chakra Overload (Dai Kenja), Life reaver
  (Loup-Garou), Cerulean Storm: Avalanche (Hyouga Yui), Wind Step (Namikaze), Luminous Illusion Bind (Voltara Divine).

## Before any ticket

Each ticket re-reads its jutsu (Forge capture) and checks AI equips: approving a suggestion severs AI links (laws 18,
60). Text and icons follow `docs/design/jutsu_overhaul/WRITING_STYLE.md` and the BEE emblem direction; final prose
and art direction are the director's (CLAUDE.md section 10).
