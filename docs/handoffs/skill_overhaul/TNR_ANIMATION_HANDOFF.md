# How we build combat animations for The Ninja RPG (TNR)

A handoff for an agent working on TNR combat art. It covers what the engine actually does with an animation, the art rules the director has set, the techniques that work, and the pipeline from idea to a live record. Everything here was learned building the Mother of Echoes boss and the Subaku Palace jutsu (Nov 2026).

**Repo:** `perseverance484/tnr-tools`. Read `CLAUDE.md` first.

**Game source:** `/home/claude/studie-tech/theninjarpg`. Read it with `git show <sha>:<path>`; never run it.

---

## 0. Ground rules

- **Zero live game requests. No credentials.** The director runs every manifest himself through the builder.
- **Verify engine behaviour in the source before relying on it.** Cite `file:line`. Notes and docs go stale, and the live game moves (see §1.6).
- **Art direction is the director's call.** Show him previews; never ship a look he hasn't seen.
- **Every batch gets an independent review** by a separate agent that didn't make the art. That reviewer renders its own frames rather than trusting the maker's GIFs. This has caught real bugs every time: blank hexes, broken wiring, stale exports, wrong colours.
- **Record durable decisions in `docs/RULINGS.md`.** The art direction rulings are RUL-2026-11-05-124 through RUL-2026-11-06-130.

---

## 1. What the engine does with an animation

These facts are from theninjarpg upstream `cb755375`. Key files:
- `app/src/libs/rendering/animation.ts`
- `app/src/libs/rendering/scenes/combatEffects.ts`
- `app/src/libs/rendering/primitives/animation.ts`
- `app/src/libs/rendering/scenes/combatActors.ts`
- `app/src/libs/combat/targeting.ts`
- `app/src/libs/combat/process.ts`
- `app/src/libs/combat/actions.ts`
- `app/src/validators/asset.ts`

### 1.1 Where a clip is drawn
- **Clip size.** A clip is a square **`EFFECT_ANIMATION_HEX_RATIO` × hex height**, centred on the hex.
  - We author for **2.5 h**. That makes it wider than the hex (hexes are drawn 2:1, w = 2h), so neighbouring clips overlap.
  - Upstream commit `338126cb` set the ratio to 1. The director is having it reverted. At ratio 1 a clip covers only the hex's middle half, and nothing can draw across a column seam.
  - Check the live value before you start.
- **Rendition.** The engine loads every clip at a **50 px** rendition with **linear filtering**. Design for 50 px: 1 px details blur away, and tiny glyphs read as noise. Always preview at true scale.
- **Strip format.** Animations are vertical strips of square frames. The asset validator enforces:
  - `frames` 1–100;
  - `speed` 1–100 (ms per frame; we use 50);
  - `name` 1–191 chars;
  - **`folder` matching `^[a-zA-Z0-9]*$`**: letters and digits only, no spaces or dashes.

### 1.2 Layering and timing
- **What draws where.**
  - Each ground effect has `staticAssetPath`, a static tile stretched to the **full hex box** (w × h). It draws **under** fighters.
  - `appearAnimation` (one-shot) and `staticAnimation` (loop) are clips. They draw **over fighters and their HP/SP/CP meters**.
  - Loops therefore cover people for as long as the effect lasts. Use them sparingly and keep them thin.
- **Start time.** An effect record becomes ready when **all its images have loaded**. Then its tile and clips appear together. The appear and the static start on the same frame, and the appear overdraws about 2–3×.
- **No delay mechanism.** You can't hold a static tile back until an appear finishes. A lingering floor is visible from frame 0 under its own payoff (see §3.4 for workarounds).
- **Per-record start.** Each record starts when *its own* images load, not when the cast happens.
  - **On a cold cache,** neighbouring hexes with different strips can start 0–3 frames apart.
  - **Hexes sharing one strip** share one load and start together.
  - **Design for skew:** use 3–4 frame holds wherever a picture crosses a hex seam. Preview everything at skew 0 *and* skew 2.
- **Effect lifetime.** A one-round effect is visible through round N+1. The killing blow is never animated, because the battle ends first.
- **Players** are layered LPC character sprites, about 1.35 h tall, feet about 0.23 h above the hex bottom, head above the hex top (`combatActors.ts:36, 604-618`). **AI** originals are 1.6 h tall, centred at 0.9 h. **A player's own meters are always visible to them.**

### 1.3 Visual tags (art-only effects)
- **What they are.** A tag with `type: "visual"` (power 2, no gameplay) carries art on chosen hexes. They're how we paint large set pieces.
- **Targeting.** Use `target: COORDINATES` with a coordinate list, and with `origin: CASTER` or no origin (fixed battlefield positions).
  - COORDINATES offsets are **col/row**, not axial (`targeting.ts:59-75`).
  - Relative to the caster, the same offset lands on different hexes depending on the caster's column parity.
  - **Fixed-position art slices exactly; caster-relative art can't.**
- **Lifetime.** **Visual ground effects are dropped at the first action of round N+1**, whatever their `rounds` (`combat.ts` ~851). They're for the cast moment only, never for lingering art.
- **They're player-visible.** Every tag is a line in the jutsu's details screen, which matters on player jutsu. For boss jutsu, descriptions are staff-only, so it doesn't matter there.
- **Cap.** Jutsu `effects` has no size cap. Our largest boss records have about 120 visual tags (about 60 KB) and work. Each tag costs one ground-effect row for one round, the same as an AoE.

### 1.4 AoE targeting
- **`AOE_SPIRAL_SHOOT`** covers every hex within `range` of the **caster**, excluding the caster's own hex (`targeting.ts:56-58`). It is not centred on a chosen point.
- **Hex counts.** A radius-4 domain is 60 hexes. 4 rim hexes per parity can't be reached by col/row tags.

### 1.5 Combat mechanics that shape art and design
- **Shared cooldowns** (upstream `b54541f1`, table per battle, admin-configurable).
  - Any action whose effects include a listed type (pierce, drain, stun, summon, seal, …) locks the caster's *other* actions with that type for 3 rounds, even actions with cooldown 0.
  - It does **not** lock the same jutsu; that needs the jutsu's own cooldown. Cooldown N means ready again once ≥N rounds have passed.
  - Plan pacing around this. Locks are per caster.
- **AI respects shared cooldowns** too. There's no AI exemption (`actions.ts:1408, 1468-1520`).
- **Lethal hits.** We use `onehitkill` power 100 with **target INHERIT**.
  - If you copy a captured donor record, check its target: one donor had SELF, so the boss "killed" herself.
  - OHKO produces no damage packet, so no recoil, reflect or absorb.
  - `onehitkill` power < 100 is a percent chance.
- **Plain damage** goes through player damage reduction, floored at 5% of the boosted hit. **Pierce** skips DR.
- **Ground effects bind** to whoever stands on the hex whenever any action resolves (`process.ts:396-412`). A pool cast on the player's own hex hits them instantly and can't be dodged. Never put a lingering hazard on the target's hex; telegraph it first, or offset it.

### 1.6 The live game moves
Upstream changed clip size, character art, shared cooldowns and AI combo logic within one week. Before trusting any engine fact, fetch upstream read-only and diff the files you rely on against the pin you're using.

---

## 2. The director's art rules

These are standing rulings; read the RULINGS entries for the full text.

1. **Quality bar:** the Mother of Echoes *Refraction line*, a single painting sliced across a row of hexes. Every ability should look that good.
2. **Omens** (the telegraph, the round before a hit) use the established ground language: circles and marks on the hex. Their job is clarity.
3. **Payoffs** (eruptions, breaks, real abilities) are **painted as one picture across the whole area they hit**, sliced across hexes. No per-hex toxic bubbles, no repeated stamps.
4. **Lingering ground** shows the floor as the ability left it: cracked, frozen, blackened glass, as one continuous static surface with a clear edge. It never covers a safe hex.
5. **The fight is a stage.** Abilities visibly reshape the terrain, and the player reacts to an evolving floor.
6. **No sickly green, ever.** Colours come from whoever owns the effect; danger reads through material and value contrast.
   - Fixed danger grammar: ember for heavy, violet for control, cyan **only** for safe hexes (exception: the Refraction line's Heartglass cyan), gold for etchings.
7. **Restraint.** Entrances stay inside the caster's own clip. Bosses spawn together, so big flourishes collide.
8. **Clutter budget.** Every round needs to show three things clearly: which hexes are dangerous next turn, where everyone is, and the boss's state.
   - Large pools and mark fields keep the floor tile but drop their loop.
   - One field-wide payoff per round.
   - Warnings draw on top.
   - Nothing paints over a safe hex.

---

## 3. Techniques that work

### 3.1 Slice mosaic (fixed-position payoffs)
1. Render one large composition over the whole region in hex-space.
2. Cut it into one strip per hex, each covering that hex plus a 1 px overlap.
3. Clip each slice to its own hex polygon, so nothing leaks onto safe hexes.
4. Wire one visual tag per hex: COORDINATES, no origin.
5. Deduplicate identical slices by content hash. They share a load and start in sync.

It reads as one picture. It works only for fixed board positions.

### 3.2 Lattice-periodic paintings (near-full-arena fields)
For floods and whole-hall effects, paint a pattern that repeats every 2 cols × 3 rows, with band-timed wave fronts. Far fewer unique strips; it's indistinguishable from unique art at that scale.

### 3.3 Caster-relative effects
- Make the pieces symmetric, or join them at hex vertices, which coincide in either parity.
- Use one centre clip plus ring pieces, or ring-band tags with leading delay frames for an outward spread.
- Accept about ±1 tick of timing error from parity.

### 3.4 Making a floor "arrive" (there's no delay)
- **Light-only (Subaku):** the resting tile is visible from frame 0, with dark unlit rails. The clips draw only light along the tile's own lines, then cool back to it. Nothing is covered and nothing pops.
- **Faint floor (Mother of Echoes):** the lingering tile is about 18% opacity. The payoff clip carries the vivid floor from the break, then fades down to the faint tile over about 7 frames.
- **Opaque cover:** only works where you know what's underneath (your own domain stone). It covers fighters, so the director rejected it.

### 3.5 Animation craft
- **Anticipation → held beat → settle.** Use 2–3 frame holds at the peak: stillness reads as power, and holds absorb load skew.
- **No glitter.** Decay by shortening connected runs; never leave isolated 1 px specks.
- **Keep 2 px clear of the clip edge.**
- **Ramp big flashes.** Never jump the whole domain on one frame, e.g. 18 → 40 → 75 → 100 → 70 → 40 → 15%.
- **Measure coverage** of fighter bodies and meter rows per frame, and keep it brief.

---

## 4. Pipeline

1. **Design.** One idea per move, from the character bible (`docs/design/SAYO_BIBLE.md` is the example). Get the director's direction first; a quick rough key sheet beats a polished wrong answer.
2. **Build programmatically** with Pillow (approved dependency). Builders live under `art/<subject>/`. Raw generated art, when needed, goes through the art skill (`skills/producing-tnr-art`: prompts, `chroma.py`, `rawqc.py`).
3. **Preview at true scale.** Composite on the real arena background with LPC stand-ins, on both light and dark boards, at skew 0 and 2, and at both column parities for caster-relative art.
   - Harness: `scratchpad/custom/qa_preview.py`. Set `LPC=1` and `CLIP_RATIO`.
   - Send GIFs and key-frame sheets.
4. **Preflight.** Run `skills/producing-tnr-art/scripts/artpreflight.py`; it must report 0 errors.
5. **Independent review.** A separate agent ranks findings BLOCKER / SHOULD / NIT, with evidence. Fix the blockers, then re-review.
6. **Name and file.** Library folders are CamelCase, letters and digits only (`SkyglassMotherOfEchoesActII`, `JutsuSubakuPalace`). Names are readable and unique (`MoE II: Recast Rime - slice c04r06`). Gate every build on both.
7. **Manifests:**
   - **Create assets hidden** (law 16b), then edit the jutsu and AI records, then **unhide** in a follow-up job. Hidden assets don't play in battle (16c), so run the unhide straight after.
   - **Editing a jutsu unequips it from any AI holding it** (law 18). Unequip, edit, re-equip.
   - **Jutsu edits replace the whole effects list.** Read the live record back first if you don't have a full copy.
   - **Asset ids** come from results bundles (`harvests/inbox`). List captures persist row counts only.
   - **Gates:** `skills/building-tnr-content/data` → `python3 ../scripts/validate.py --strict`; `forge/` → `node tools/check_manifest.mjs`; plus a `state/validate_exceptions/` ledger for any accepted diagnostics.
8. **The director runs it** and tests live. Watch the first cast in a fresh session for seam skew.

---

## 5. Where to look

- **Mother of Echoes art:**
  - `docs/design/MOTHER_OF_ECHOES_ART.md` (Art4, Stacking pass, Art direction)
  - `art/mother_of_echoes_fx/` (`build_fx*.py`, `exports/`, `moe_fx_final.json`)
  - `push/mother_of_echoes.gen.py` (`Build(final=True)`, `painted()`, the asset gates)
- **Subaku Palace:** `docs/design/SUBAKU_PALACE_ANIMATION.md`, `art/subaku_palace/` (`TIMING.md`, `classic.py`, `build_domain.py`, `gates/`), `push/subaku_palace.gen.py`
- **Engine notes:** `docs/design/COMBAT_ANIMATION_ENGINE.md`. Older than this file; prefer this file's §1 where they differ.
- **Rulings:** `docs/RULINGS.md` (RUL-2026-11-05-124 … RUL-2026-11-06-130)
