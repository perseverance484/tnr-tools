> **STALE - archived 2026-08-28 (rollout Stage 2).** Superseded by the skill references and generated data under /skills/, and by /docs/ENGINE_LAWS.md. Do not build from this file.

# 27 - LORE: The World of Seichi (canon reference and non-canon registry)

The first stop before naming, theming, or writing anything player-facing. Three tiers of truth apply to every entry here:
- **[CANON]**: verified from the TNR source code or live game data. Safe to build on.
- **[NON-CANON CANDIDATE]**: our generated content. It has NOT entered the core game; it is hidden candidate material awaiting the Content Admin. Treat as placeholder lore: internally consistent, externally unratified, renameable or removable at review.
- **[PLACEHOLDER]**: an open lore decision reserved for the Content Admin. Never resolve one silently; carry it and flag it.

---

## 1. The world [CANON]

The game is set in **the ninja world of Seichi** (the game's own quest-generation prompt names it; the premium currency is Seichi Silver; the welcome theme is "Welcome to Seichi"). Players are shinobi progressing Student -> Genin -> Chunin -> Jonin -> Elite Jonin -> Elder, running errands, missions (D through S rank), and crimes, joining clans and ANBU squads, and fighting wars between villages.

**The five core villages [CANON]:** Shirohana, Tsukimori, Hyorin, Akasumi, Akikaze.
**The legacy villages [CANON as history]:** Shine, Glacier, Shroud, Current persist in the code from an earlier age of the game; usable in lore as the old names of a prior era.
**[RULED by Content Admin]:** legacy names are in-universe history. **Hyorin inherits ALL of Glacier's lore**: Glacier is Hyorin's identity in the old age, and Hyorin content may reference "when the village was called Glacier" as established history. [PLACEHOLDER: whether the other three legacy names map to core villages the same way.]
**Outlaw life [CANON]:** outlaw factions and towns are first-class structures; **Freedom State** exists in live data as one such faction. Missing-nin and bounty systems are native to the world.
**Village identities [PLACEHOLDER]:** one-paragraph identity per core village (climate, temperament, what a D-rank chore looks like there) awaits the Content Admin's direction or community canon not visible in source.

## 2. Institutions [CANON where coded, names flexible]

- **Mission halls** issue rank-gated missions and errands; the engine caps missions per day globally. [CANON]
- **ANBU squads**, clans, kage leadership, hospitals, banks, shrines (shrine reward boosts exist engine-side), and village structures are all coded systems. [CANON]
- **Story missions surface in the global ANBU building.** [CANON, live-observed]
- **The quartermaster** (Act I chain) and **the magistrate** (D-rank missions) are our inventions layered on the mission-hall institution. [NON-CANON CANDIDATE; PLACEHOLDER: ratify or rename to Seichi-native titles.]

## 3. Our antagonist factions [NON-CANON CANDIDATE]

### The Unbroken Thread (endgame, the Tower)

A cult of the high crags where the old world's borders met: scavengers of a darker sort, chasing echoes of lost gods and forbidden techniques in the ash of the Great War. They raised two orphaned sisters as keys, not daughters: **Eclipse**, whose chakra pooled black and light-devouring and whose bones slid from her flesh as ivory blades, and **Aegis**, storm-marked before ten, who heard a dying storm god in the thunder. On the sisters' nineteenth winter the Thread bound them in the metal vaults beneath the mountain and siphoned their bloodlines to wake the dormant constructs buried there. The sisters broke the ritual, brought the stronghold down, and died of the poisoned needles in a muddy ditch, where they forced their fused inheritance into a nameless scavenger girl with clear eyes: **the Vanguard**. "Live for us. Carry the sky."

**The Tower of Endless Night IS the Thread's woken stronghold**: the vault machinery, risen through the clouds, saturated with what was siphoned. Its endless dark is Eclipse's stolen light-devouring chakra; the storms that wreathe its summit are the echo of Aegis's god. The keepers are the Thread's ritualists and constructs, and **The Endless Night** enthroned on the tenth floor is the crown of the machine wearing the stolen lineage. The Endless Night Chests are reliquaries from the siphon vaults; the rarest carry a sealed strand of the stolen bloodline, which is why the Tower is climbed.

Spelling note: the lore document's "Sechi" is normalized to the canon **Seichi**.

### The Unwritten Hand (owned by The Unwritten War arc; see 28_ARC)

**[RULED]: the standalone Unwritten Hand program is replaced by The Unwritten War quest chain (28_ARC_the_unwritten_war.md), which absorbs all of its lore and its existing missions as chapters 1-4.** The lore below persists as the arc's guiding force; new writing anchors to the arc document, not to an independent Act I chain.

The campaign villain of the Act I story chain. Doctrine: it never commands in the open; it moves the village by changing what the village hears, believes, records, and follows. It falsifies records, rings false signals, steals the materials that make movement and records official (route seals, ration tags, mission papers). Breadcrumbs advance by METHOD, never by identity: each mission reveals a new way the Hand manipulates, never who it is.

**The Act I chain [NON-CANON CANDIDATE]:** Mission 1 "Training Grounds" and Mission 2 "The First Mark" exist in the game (pre-date our pipeline); Mission 3 "The Bell That Lied" is our build (live, hidden); Mission 4 "The Courier Who Never Arrived" is designed-not-built. Chain links via prerequisiteQuestId. [PLACEHOLDER: The First Mark's live quest id for the chain wire.]

## 4. Non-canon candidate content registry (ours, all hidden)

| Content | Prefix | State |
|---|---|---|
| The Wyrmspire Nest event: dragon brood story mission, 5 AIs, 23 jutsu, 2 items | `Wyrmspire` | live hidden; art pass pending |
| The Wayward missing-nin trio: Blade, Ember, Gale, level 70 daily-grind enemies | `Wayward` / `dw_` | live hidden, fully tuned, full art |
| ANBU Bounty: The Wayward Contracts, weekly three-contract bounty board | `waycon_` assets | live hidden, final structure |
| The Bell That Lied, Act I Mission 3, Unwritten Hand chain | `Unwritten` / `uh_` | live hidden |
| The Magistrate's Runaway Cat, repeatable D-rank, Lord Dumpling | `Dumpling` / `cat_` | manifest ready |
| The Frost Lantern Route, repeatable D-rank Hyorin errand, no combat | `drank_lantern` | manifest ready |
| Drowned Fleet battlepyramid (pre-stack build) | `Drowned` | live |
| The Tower of Endless Night: daily split battlepyramid, 18 AIs, 56 jutsu, Endless Night Chest, Unbroken Thread lore | `tn_` / tower names | AIs and chest live hidden; Lower quest manifest delivered; Upper pending Lower id |
| Eclipse Marrow / Aegis of the God's Torment bloodline(s): the sisters' fused inheritance, the Tower's grand prize | n/a (admin-created) | [PLACEHOLDER: Content Admin creates the record(s); design, stats, and rates reserved] |

None of the above is core-game canon. Cross-references BETWEEN candidates are allowed (the bounty board hunts the Wayward trio) but no candidate may be treated as established world fact in new writing; each new piece must stand if another candidate is cut.

## 5. Rules of the universe (writing law for all content)

1. **Franchise law [HARD]:** everything is original. No Naruto names, symbols, gear, creatures, or recognizable marks, in text or art. Seichi is its own world.
2. **Tone bands [PLACEHOLDER, proposed]:** D-rank missions may be comedic; C-B adventurous; A-S and the story chain grim and grounded; events set their own band on the design sheet. Awaiting ratification.
3. **Naming:** every content set carries a unique prefix, dedup-checked against catalogs 40-42; the prefix registry lives in section 4 and in `44_DATA_id_registry.md`.
4. **No em dashes in player-facing dialog text.**
5. **Anchoring:** every quest either names its village or is universal (all villages); recurring NPCs must be registered here so the same clerk is the same clerk. [Current NPC registry: the mission hall clerk, the fish stall keeper, the magistrate + Lord Dumpling, the quartermaster, the ANBU bounty handler, the Hyorin lantern keeper (an old man who tends the pass lanterns, snowed in each deep winter), the sisters Eclipse and Aegis (deceased, the Tower's stolen lineage), the Vanguard (the nameless scavenger girl carrying their fused inheritance, unspent story hook); all NON-CANON CANDIDATE.]
6. **Village anchor for our content [PLACEHOLDER]:** the Act I chain and D-rank set are currently written village-neutral ("the village"). The Content Admin decides a home village or ratifies universal framing.

## 6. Builder checklist (lore gate, before any new content)

- [ ] Read this file; new names dedup against section 4 and the catalogs.
- [ ] New setting facts either derive from [CANON] or are explicitly introduced as [NON-CANON CANDIDATE] here (hand back the updated 27 with the build).
- [ ] No candidate treated as established fact; no franchise content; tone band matches the content type.
- [ ] Every [PLACEHOLDER] touched by the build appears in the delivery decision list.


## Addendum (Jul 10 2026): legacy village mapping is SOURCE CANON

`app/src/validators/rewards.ts` (`LEGACY_STARTER_VILLAGE_MAP`) resolves the standing PLACEHOLDER: **SHINE -> SHIROHANA, GLACIER -> HYORIN, SHROUD -> AKASUMI, CURRENT -> AKIKAZE.** All four legacy names map to core villages in the engine itself (legacy reward values are transformed to these). The earlier ruling (Hyorin inherits Glacier) is confirmed and extended: each core village except Tsukimori has a legacy-age identity usable as in-world history. [CANON, source-verified 2026-07-10. Tsukimori has no legacy mapping in source.]

## Addendum (2026-07-27): Haishiro and the Concord [NON-CANON CANDIDATE]

The Ashen Concord arc is set in **Haishiro**, a kiln city built around a treaty. Everything here is ours, hidden, and pending Content Admin promotion.

**The five clans.** The **Shirakotsu** keep the Boneyard and the registry of the dead, bone-white and unhurried. The **Ryokin** keep the Vault and every account in the city, brass and coin-scale. The **Itokage** keep the Archive, dusk-violet, and answer in thread. The **Hagane** keep the Pit, forge-black and ember, and pay for work rather than talk. The **Nemori** keep the Rootway, moss-green, and tend what returns.

**The two matriarchs.** The **Gravemother** speaks for the Shirakotsu. The **Debtkeeper** speaks for the Ryokin and is owed by everyone, which is a kind of authority.

**The three fighting lines**, which are how a person fights rather than who they serve: **Charterbound**, the wall that stands and holds; **Ashrisen**, the blade that ends things early; **Veilspun**, the quickening that is elsewhere when the blow lands. A player chooses once and builds toward it at the forge.

**The kilnyard.** One yard, five hearths, one per house, at working heat (furnace) or with the fires up (crucible). Working another clan's fire is not trespass; it is what the treaty bought. This is the campaign's whole farm fiction and it is deliberately simple.

**Writing law for this arc:** no em dashes in any player-facing dialog, no franchise references, and the clans speak in their own registers (ledger, thread, bone, forge, root) without becoming caricatures.
