# playing-tnr: an AI player for the director's account

Status: APPROVED by the director, 2026-11-09 (RUL-2026-11-09-139, amended by RUL-2026-11-09-145). This file is the build contract for the skill (CLAUDE.md §11).

The director's account owner authorizes an AI to play his account as a real player would, PvE and
PvP, across all content. TNR's rules permit this through the official MCP server (rules §7.4, quoted
in §1). The point is twofold: a live tester that plays like a person and reports what it finds, and
an account that is actually played.

---

## 1. What the rules allow, and require (TheNinjaRPG `app/src/app/[shell]/rules/page.tsx`, read 2026-11-09)

**Allowed**

- §7.4 Official API: "With authorization from their human owner, AI players may choose and execute
  game actions through TNR's official API (the MCP server at /api/mcp) without the owner approving
  each action or remaining continuously present. This allowance covers every endpoint exposed by that
  server that the account is authorized to use under its normal access checks and gameplay
  prerequisites; there is no separate AI-only endpoint ban."
- §7.1: using an MCP client on the official server, as §7.4 permits, is authorized.
- §7.2: owner-authorized AI play "does not count as sharing an account".

**Required**

- §7.4 Identification and Responsibility: "Accounts played by an AI must clearly identify themselves
  as AI players in their public profile and be reported to moderators with their human owner
  identified. The human owner remains responsible for all actions and content of the account."
- §7.4 Same Rules: AI players follow all rules, including fair play and conduct.
- §7.4 Information Access: the AI player may use only what the account sees through normal gameplay
  or permitted API use, plus public resources. "Accessing or using hidden game data, private
  information the account is not authorized to see … is prohibited."
- §7.4 Bug Reporting: a bug or exploit the AI finds "must [be reported] through an official bug
  reporting channel and must not [be used]".
- §7.4 Rule Gaps: "Anything not explicitly covered by these rules is not automatically allowed. In
  ambiguous cases, ask a moderator and wait."
- §7.4 Human Control Outside the API: automated play outside the official API is prohibited, even
  supervised. **So the AI plays only through the MCP connector. Duet's browser, or any browser
  automation, must never play.** It may look (screenshots of what the account sees), not act.
- §7.4: follow the server's rate limits and game cooldowns; bypass nothing.
- §6.1 and §6.3 Staff: "A staff role does not grant any exemption." Staff may not use staff powers,
  tools or access to private information in any matter involving their own accounts. **This is the
  account's staff account, so the player must never use staff powers or staff knowledge to play.**
- §7.2: at most two accounts per person, counting AI-played ones. Never kill or farm one's own alt.

---

## 2. Prerequisites before the first live action

1. **Disclosure.** The director states (RUL-2026-11-09-145) that he arranged this AI play directly
   with the game's admin and owner, and that no public-profile notice or moderator report is needed
   for this account. Rules §7.4 as published still asks AI-played accounts to identify themselves
   and be reported. The director is responsible for that arrangement; agents do not announce or
   report on his behalf unless he asks. Never use the director's real name anywhere: profile text,
   logs, reports, commits or the repo.
2. **The endpoint allowlist** (§4.2): the director's go. The first live sessions use the draft list,
   and only gameplay endpoints.
3. **No communication with other players** (director, 2026-11-09): no chat, messages, forum posts,
   comments or trade requests.

## 3. Goal

A comprehensive player that engages with everything a real player does. It plays toward
self-chosen goals the way a person would, and produces a tester's record of what it found.

### Coverage

Taken from the live MCP router list on 2026-11-09. Each area gets a playbook (§4.4).

| Area | Routers |
|---|---|
| Combat (PvE) | combat, quests, villageMission, hunting, raids, coop, simulator, sparring, towerDefense, overworldAi |
| Combat (PvP) | combat (attackUser), pvpRank (ranked), sparring, tournament, war, territoryWar, shrine, bounty, anbu, clan battles |
| Progression | train, skillTree, bloodline, bloodright, sageMode, sensei, title, badge, activityStreak |
| Professions and economy | occupation, farming, hunting, item (shop, equip, consumables, crystals), bank, auction, blackmarket, rewardPackages |
| World | travel, worldMap, village, home, hospital, kage (as a player), shrine |
| Social | clan, anbu, marriage, pets, petSpecies, comments, forum (read; post only under §5) |
| Events | quests (journal pages, timed windows), raids, tournaments, war |

### Never in player mode

- **Staff and content routers:** create, update and delete on content; staff; contentReview;
  conceptart writes; reports and moderation actions.
- **Payments:** paypal, stripe, purchases, merch.
- **Account control:** accountDeletion, nativeAuth, register, parentalControls.
- Anything that changes another player's account outside normal play.

---

## 4. The skill

### 4.1 Architecture

- **A player loop:** observe → decide → act → record, run one session at a time.
  - **Observe:** the account's state and the current screen equivalents, read through gameplay
    endpoints: profile, battle state, quests, village and timers.
  - **Decide:** goals, then plans, then actions (§4.3).
  - **Act:** one MCP call per action, paced, through the run lock (§4.5).
  - **Record:** a session log plus findings (§4.6).
- **Player memory:** a per-account notebook (`state/player/<account>/`):
  - goals;
  - what it knows of the game, learned through play or public sources only;
  - its gear and resources over time;
  - its opponents' known behaviour (public information only);
  - open timers.
- **Two modes, never mixed in one session:**
  - **Play:** the account's normal life. Player knowledge only.
  - **Test:** directed checks of specific content the director names. These only cover content the
    account can reach as a player, under the same knowledge rule. Testing hidden or unreleased
    content stays a content-staff task outside this skill (§5.3).

### 4.2 Endpoint allowlist

`data/player_allowlist.json` lists every gameplay endpoint by router, with its kind (read or
action), its cooldown or rate notes, and the playbook that uses it. The runner refuses any endpoint
not on the list, and is generated from the MCP router list with the never-list (§3) removed. The
director approves the list; any change to it is a reviewed edit.

### 4.3 Decision-making

- **Goal layer:** what a real player wants this week. For example:
  - level and train toward a stat goal;
  - finish the Watch Log page;
  - climb the PvP rank;
  - earn ryo through a profession;
  - collect the four shards;
  - help the clan in war.

  Goals come from profile presets (§4.7) and from what the account sees: news, events, timers.
- **Plan layer:** turns goals into a day's routine: training timers, mission runs, profession
  cycles, travel, hospital, bank, shop.
- **Combat layer:** a battle policy that reads the battle state each turn:
  - HP, chakra and stamina;
  - statuses;
  - telegraphed and dangerous hexes;
  - cooldowns, including shared ones;
  - range;
  - the opponent's tendencies.

  It then picks the action a player of that profile would take, with realistic errors when the
  profile has them. PvE and PvP use different policies (§4.4).
- **Knowledge rule:** the decision layer may use only the account's observations, its notebook and
  public sources (public wiki, public channels, public lore). It does not read this repository's
  design documents, generated contracts or staff data while in play mode (§5.2).

### 4.4 Playbooks (`references/playbooks/`)

One page per area. Each covers:

- what a player does there and why;
- the endpoints involved;
- prerequisites and cooldowns;
- what "done" or "good" looks like;
- the common mistakes the average profile makes;
- what to record.

The areas:

- **Combat (PvE):** missions, hunts, quests, raids, dungeons, bosses.
- **Combat (PvP):**
  - **Who to fight:** choosing opponents fairly. No farming low-level players, no griefing,
    respect for rank brackets.
  - **How to fight:** ranked and unranked, tournaments, war and territory, shrine, bounties.
  - **After the fight:** etiquette.
- **Training and progression.**
- **Each profession:** a full cycle, plus the market sense a real player has.
- **Economy:** bank, shop, auction, black market. No manipulation; normal buying and selling only.
- **Travel and world.**
- **Clan, ANBU and village duties.**
- **Pets.**
- **Events and journal pages.**
- **Daily and weekly routine.**

### 4.5 Rate limits and sharing the account

- The account's game connection allows 30 calls a minute across every client: content runners,
  this player, and the director in the browser.
- **The player takes the run lock as `--holder player`** for each session and paces under a lower
  allowance (default 12 calls a minute).
- **It ends its session when a content job is queued** (`state/run_queue.json` shows a ready
  connector job), at a safe point: never mid-battle; it finishes the fight first.
- **It never runs while the director is playing in the browser.** The director starts or stops it.

### 4.6 What it records (`state/player/<account>/sessions/<date>.md`, plus findings)

- **Actions taken,** with reasons, and outcomes: battles won and lost, rewards, resources.
- **Findings, each with evidence** (the battle id, the endpoint response):
  - **Bugs:** reported through the official bug channel per §7.4, never exploited, and filed in the
    repo.
  - **Balance notes:** too hard, too easy, unrewarding.
  - **Confusion points:** what a player could not tell.
  - **Text issues.**
  - **Content suggestions.**
- **A weekly summary for the director:** progress, findings, and what it plans next.

### 4.7 Player profiles (`data/player_profiles.json`)

Each profile sets:

- skill (the error rates on telegraphs, positioning and cooldown use);
- risk taking;
- goal mix (PvE, PvP, profession, social);
- session length and frequency;
- spending habits.

Presets: casual, average, dedicated, competitive PvP, profession-focused. The director picks the
default for his account. Test sessions may run other profiles where content allows.

---

## 5. Conduct and limits (hard rules in the runner, not just guidance)

### 5.1 Fair play

- No exploits. A suspected bug is reported and avoided.
- No griefing:
  - no repeated attacks on the same player beyond what normal play does;
  - no farming much lower-level players;
  - no spawn-camping;
  - respect for war and PvP rules.
- No market manipulation.
- No chat or forum posting unless the director enables it. If he does, any post states that the
  account is AI-played.

### 5.2 No staff powers, no staff knowledge

- Player mode calls only allowlisted gameplay endpoints, never staff or content ones.
- It does not use hidden or unreleased information:
  - this repository's design docs;
  - hidden records;
  - generated contracts;
  - staff tools.

  Examples: it does not know the Mother of Echoes fight script when it meets her; it learns her by
  playing.
- Agents that do content work never shape content, rewards or balance to favour this account.
  Where a content decision affects the account, the director handles the conflict under §6.3.

### 5.3 Testing hidden content

Playing hidden or unreleased content (e.g. the practice quest 469 boss test) uses staff access, so
it is content-staff testing, not player mode.

- It runs as the existing content verification, outside this skill.
- It keeps no rewards that a player could not have earned.
- Where it leaves rewards on the account, the director decides how to handle them (§6.3 conflict).

### 5.4 Safety stops

The player stops and reports instead of acting when:

- an action would spend premium currency or real money;
- it would leave a clan or village, or delete or sell a rare item;
- it would start a marriage or other relationship action;
- any rule is ambiguous (§7.4 Rule Gaps).

---

## 6. Build plan

Lane A, `fable/*` branches, reviewed handoffs as for the overhaul.

| Phase | Delivers | Depends on |
|---|---|---|
| PL0 | Inventory of the MCP router surface: every endpoint's schema, kind and prerequisites → `data/player_allowlist.json` draft + the never-list check. | — |
| PL1 | Offline player: the battle policy and profiles running inside the encounter simulator (overhaul P4, engine execution per RUL-2026-11-09-137), measured against the existing clear-rate profiles. | overhaul P4 |
| PL2 | Live runner: the session loop over the connector with the allowlist, the run lock as `player`, pacing, safety stops, session logs. Read-only dry run first (observe and decide, no act). | PL0 |
| PL3 | Playbooks and plans: combat PvE and PvP, training, professions, economy, travel, social, events; notebook; weekly summary. | PL2 |
| PL4 | Findings pipeline: bug reports through the official channel, the repo findings log, the weekly summary. | PL2 |
| PL5 | Evals: scripted scenarios in the simulator, plus a week of live play reviewed with the director. | PL3, PL4 |

### Starting today

The skill needs PL0 and PL2 before it can play safely. Until then, a session agent can play by hand
through the connector:

- under the prerequisites (§2);
- under the allowlist draft;
- under the conduct rules (§5);
- with one session at a time;
- with a written log.

That uses the same rules, without the automation's safety checks, so keep those sessions short and
supervised.

### Research

R6 in `state/prompt_skill_research_program.md` covers how real players play browser and turn-based
RPGs: session patterns, common mistakes, PvP etiquette, how difficulty is felt. It grounds the
profiles in evidence.

---

## 7. Director decisions

2. Approve the endpoint allowlist after PL0.
3. Choose the default play profile and goals for your account.
4. Enable or disable chat and forum posting (default: off).
5. Decide the reward handling for staff test runs of hidden content (§5.3).
6. Decide the session windows when the player may run, and its share of the 30 calls a minute.
