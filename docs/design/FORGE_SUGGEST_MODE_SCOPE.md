# Forge "suggest" mode: scope

Status: option 1 IMPLEMENTED in Forge 0.8.0 (director's choice, 2026-10-19); options 2 and 3 not started. Source read at
studie-tech/TheNinjaRPG@b2efd10 (current main); Forge contracts are pinned to 94f9d84.

## How the game's suggestion feature works

**Where it lives:** the content review desk (`/manual/review`). Router `contentReview`
(`app/src/server/api/routers/contentReview.ts`), logic in `app/src/libs/contentReview/`,
input shapes in `app/src/validators/contentReview.ts`, editor button `app/src/layout/SuggestChange.tsx`.

**Submitting (`contentReview.create`, protected mutation, no rate limit):**

```
{ entityType, entityId | null, category, title (3-120), rationale (10-4000), data: {...whole form} }
```

- `entityType`: JUTSU, ITEM, BLOODLINE, QUEST, BADGE, TITLE, GAME_ASSET, AI.
  **Bloodright skill trees and folders are not supported.**
- `entityId` set = UPDATE an existing record; `null` = CREATE a new one.
- `category`: GRAMMAR, BALANCE, SOUND, ANIMATION, VISUAL, CONSISTENCY, NEW_CONTENT.
- `data` is the whole editor form. The server keeps only the fields that differ from the live
  record, validates the merged result with the same validator the normal save uses, and refuses
  "Nothing changed compared to the live version".
- One record per suggestion. (The automated audit can bundle up to four changes, but only
  through a cron-secret REST route, not available to staff.)
- Who may submit: `canSuggestContent` = any staff role except the moderator roles.
- The answer is `{ success, message: "Sent for review" }`. **It does not return the suggestion's
  id**; the submitter finds it again through `getQueue` (non-reviewers see only their own).

**Lifecycle:** PENDING → APPLIED, REJECTED (with a reason and note), OUTDATED, or later
REVERTED. An UPDATE records the target's content version when submitted; if anyone edits that
record before approval, the suggestion goes OUTDATED and can no longer be approved.

**Approving (`approve`):** content staff (`canChangeContent`) can untick fields, edit values,
then apply. Applying runs the normal create/update procedures as the approver. A CREATE makes
the record, then updates it with the suggested fields, so a suggested `hidden: true` stays
hidden after approval. The new record's id is written back onto the suggestion. **The server
does not stop someone approving their own suggestion**; the second pair of eyes is a team
practice, not a rule the game enforces.

**Reading back:** `getQueue({ status, entityType?, cursor, limit })` and `getProposal({ id })`
return the suggestion with its changes, status, reviewer, and (after approval) the record id.

## What this means for Forge

| Forge today | In suggest mode |
|---|---|
| Writes immediately, hidden | Nothing changes in the game until a reviewer approves |
| Verifies by reading the record back | Can only confirm "suggestion submitted"; the outcome comes later |
| New records get ids at once, so later items can reference them (`@jutsu:`, `@ai:`) | A suggested new record has **no id until approved**, so nothing can reference it yet |
| Many records per job | One suggestion per record |
| Bloodright trees supported | Not supported by the game; stay direct-hidden |

The biggest constraint is **references**. A typical manifest creates a jutsu, then an AI that
uses it, then a quest that uses the AI. In suggest mode the AI cannot name the jutsu until the
jutsu suggestion is approved.

## Options

1. **Suggest edits to existing records only.** Simplest and most useful first step. Covers
   balance passes and fixes (jutsu numbers, AI kits, item text, quest text). New content keeps
   the current create-hidden flow.
2. **Create hidden, suggest the reveal.** Forge creates everything hidden as today (all ids
   exist, references work), then submits one suggestion per record that flips `hidden` to
   false. The reviewer sees the full record, and approving it makes it live. It fits any
   manifest, but the reviewer reviews "make visible", not each field.
3. **Suggest new content in waves.** Forge suggests records with no references first, waits
   for approval, reads the new ids, then suggests the next layer. Most faithful, but slow
   (a job waits on a person between layers), and a rejection mid-way strands the rest.

Recommendation: build 1, then 2. Leave 3 unless reviews need field-by-field approval of new
content.

## Forge work involved (for option 1, then 2)

- Re-pin Forge's procedure contract to a game commit with `contentReview` (it postdates the
  current procedure pin; TITLE was added after 94f9d84).
- Manifest: a job-level `mode: "hidden" | "suggest"`, plus `title`, `category` and `rationale`
  per item (defaults derived from the manifest note).
- Runner: a suggest path that reads the live record, sends `contentReview.create`, then finds
  the new suggestion in `getQueue` by its unique title and records its id. A new item state,
  SUGGESTED, sits between sent and verified.
- A "Check suggestions" action that later reads each suggestion's status and, once APPLIED,
  reads the record back to verify it, as Forge does today.
- Preview shows which items will be suggested versus written, and refuses suggest mode for
  Bloodright.
- Results bundle records suggestion ids and outcomes.

## Decisions for the user

1. Which option(s) to build, and in what order.
2. Default category and how titles and rationales are written (per manifest, per item, or generated).
3. Who approves. Approval happens on the game's review desk, not in Forge, and the game lets
   an account approve its own suggestion, so "a second person approves" is a team rule.

## Implemented: option 1 (Forge 0.8.0)

A manifest opts in with a top-level `mode` and the suggestion's text:

```json
{
  "mode": "suggest",
  "suggestion": { "category": "BALANCE", "title": "Ember tune", "rationale": "Why the reviewer should approve this." },
  "items": [
    { "entity": "jutsu", "slot": "edit", "name": "Ember Step", "targetId": "<jutsu id>", "data": { "description": "..." } }
  ]
}
```

- Items must be edits (`slot: "edit"` with `targetId`) of jutsu, item, bloodline, asset or ai. Creates, captures and Bloodright imports are refused in suggest mode.
- **Quests are refused for now:** `quests.get` hides objective locations from staff who cannot save content (sector 1337), so a suggestion built from it would overwrite the real objectives if approved.
- **AI edits** may only touch the fields the review desk accepts (`aiEditableKeys` in the contract); anything else (e.g. `maxHealth`, `rules`) is refused rather than silently dropped.
- An item may carry its own `suggestion` (title, category, rationale) over the manifest's. Category defaults to BALANCE.
- **Write a specific rationale for every item** (RUL-2026-10-19-007). The manifest-level `suggestion` supplies the shared title and category; each item carries its own `suggestion.rationale`, a short blurb telling the reviewer what this record's change is and why (for an icon: what the new art shows, and what was wrong with or missing from the old one). The desk already shows the field diff, so the rationale explains the change rather than repeating it. A generic text shared by every item is only a fallback. Keep it short: one to three plain sentences that state what was wrong and what the fix changes, with no narrative (RUL-2026-10-21-012).

```json
{ "entity": "jutsu", "slot": "edit", "name": "Glacial Volley", "targetId": "<jutsu id>",
  "data": { "image": "@img:icon_bbe_glacial_volley_v2.webp" },
  "suggestion": { "rationale": "New icon for <bloodline>: <what the art shows>, matching <what the jutsu does>. Replaces <what was wrong with or missing from the old icon>." } }
```
- Forge reads the live record, merges the edit exactly as a save would, and sends it with `contentReview.create`. The title gets a short job tag (`[abc123-1]`) so Forge can find the suggestion in the review queue and record its id.
- An edit the live record already holds is verified instead of suggested.
- A lost response is settled on resume from the review queue (every status, staff suggestions, every page): found means it is not sent again; not found means it is sent again; a queue too long to search finishes without resending.
- The Run screen's **Check suggestions** button reads each suggestion's status (in review, applied, rejected, outdated, reverted) and the reviewer's note.
- Procedures and limits: `forge/src/review/contract.json`, pinned to studie-tech/TheNinjaRPG@2aed7e4.
