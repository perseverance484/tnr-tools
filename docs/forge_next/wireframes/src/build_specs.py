#!/usr/bin/env python3
"""Builds specs.json for gen.py: Forge Next planning wireframes (phone 390 + desktop 1280).
Navigation labels are the IA recommendation's defaults and are marked PENDING K-20; every screen lists
the open decisions it depends on and the evidence rows it is drawn from."""
import json, os
HERE = os.path.dirname(os.path.abspath(__file__))

# ---- IA defaults (recommendation; PENDING K-20 / K-24) ----
NAV_PHONE = ["Home", "Work", "Capture", "Jobs", "More"]
NAV_DESK = ["Command Center", "Capture & Research", "Build & Update", "Quest Studio", "Content Admin", "Jobs & Recovery", "Projects", "Settings"]
MORE_ROWS = ["Content Admin", "Quest Studio", "Projects", "Captures library", "Settings & diagnostics", "Export journal"]
LANES = [
    {"label": "Quests & Events", "sub": "missions, events, story", "accent": "#e6b84f", "count": "3 hidden"},
    {"label": "Combat", "sub": "jutsu, AI, profiles", "accent": "#c0242f", "count": "1 hidden"},
    {"label": "Items & Bloodlines", "sub": "gear, consumables, lines", "accent": "#7ab8ff"},
    {"label": "Scenes & Assets", "sub": "backgrounds, characters, icons", "accent": "#2fb3a6", "count": "26 hidden"},
]
PEND_NAV = "K-20 exact destination lists and labels (pending predecessor-transcript reconciliation); K-24 lane taxonomy; K-21/K-22 mode taxonomy and colours (defaults shown)."

def brand(lamp="READY ✓"):
    return {"kind": "brand", "tag": "content operations", "actions": [lamp]}
def pnav(active):
    return {"kind": "nav", "items": NAV_PHONE, "active": active, "bottom": True}
def rail(active):
    return {"kind": "rail", "items": NAV_DESK, "active": active}
def health(session=("✓", "signed in · 2 m ago", "ok"), repo=("✓", "push/ listed 4 m ago", "ok"), budget=("✓", "12 % of window used", "ok")):
    return {"kind": "lamps", "head": "Readiness", "items": [
        {"glyph": session[0], "label": "SESSION", "value": session[1], "tone": session[2]},
        {"glyph": repo[0], "label": "REPO", "value": repo[1], "tone": repo[2]},
        {"glyph": budget[0], "label": "BUDGET", "value": budget[1], "tone": budget[2]}]}
def bar(title, sub="", chips=None):
    return {"kind": "bar", "title": title, "sub": sub, "chips": chips or []}
def note(text):
    return {"kind": "text", "text": text}

S = []
# ------------------------------------------------------------ WF-01
S.append({"id": "wf01_command_center", "title": "Command Center (home)", "default_theme": "forge",
 "purpose": "Home. Every block is fed from state Forge already holds (journal, auth probe result, GitHub listing cache, capture cache, review-queue file); nothing here spends live rate budget.",
 "flow": "Open Forge → readiness lamps → active work or empty state → quick actions → lanes → recent activity. One tap reaches a lane, a resumable job or the admin queue.",
 "mobile": [brand(), {"kind": "lamps", "head": "Reads and writes available", "items": [
    {"glyph": "✓", "label": "SESSION", "value": "signed in · dauntless", "tone": "ok"},
    {"glyph": "✓", "label": "REPO", "value": "push/ listed 4 m ago", "tone": "ok"},
    {"glyph": "✓", "label": "BUDGET", "value": "12 % used · resets 0:48", "tone": "ok"}]},
  {"kind": "card", "title": "Active work", "pill": "PAUSED", "sub": "46_mission_flatten.json", "risk": "recovery", "blocks": [
    {"kind": "seg", "cells": ["VERIFIED", "VERIFIED", "VERIFIED", "SENT", "PLANNED", "PLANNED", "PLANNED"], "label": "3 verified · 1 SENT unconfirmed · 3 planned · 7 total"},
    {"kind": "action", "label": "Reconcile & resume", "variant": "recovery", "hint": "reads first, never re-sends"}]},
  {"kind": "quick", "items": [
    {"label": "Run a manifest", "sub": "from push/ · 7 listed", "variant": "mutation"},
    {"label": "Capture from live", "sub": "read only", "variant": "read"},
    {"label": "Review queue", "sub": "3 waiting (repo file)", "variant": "publish"},
    {"label": "Quest Studio", "sub": "mission draft saved", "variant": "read"}]},
  {"kind": "lanes", "items": LANES},
  {"kind": "card", "title": "Recent activity", "sub": "journal + bundles", "blocks": [
    {"kind": "row", "title": "06_aerathiel_pvp_battle_logs", "sub": "capture-only · 44 reads · synced", "pills": ["DONE"]},
    {"kind": "row", "title": "05_aerathiel_pvp_research_stage1", "sub": "capture-only · 16 reads · synced", "pills": ["DONE"]},
    {"kind": "row", "title": "24_rank_icon_swap_all31", "sub": "31 quest edits · read back", "pills": ["VERIFIED"]}]},
  pnav("Home")],
 "desktop": {"columns": "220px minmax(420px,2fr) minmax(300px,1fr)", "regions": [
   {"name": "rail", "span": "1", "blocks": [rail("Command Center"), note("Active work chip + static badges: orphan count, SENT dot, review count (gold outline)")]},
   {"name": "main", "span": "2", "blocks": [bar("Command Center", "hero strip: CSS atmosphere only (K-31)"),
     {"kind": "quick", "items": [
       {"label": "Run a manifest", "sub": "push/ · 7 listed", "variant": "mutation"},
       {"label": "Capture from live", "sub": "read only", "variant": "read"},
       {"label": "Review queue", "sub": "3 waiting", "variant": "publish"},
       {"label": "Quest Studio", "sub": "1 draft", "variant": "read"}]},
     {"kind": "lanes", "items": LANES},
     {"kind": "card", "title": "Active work", "pill": "PAUSED", "sub": "46_mission_flatten.json · AMBIGUOUS", "risk": "recovery", "blocks": [
       {"kind": "seg", "cells": ["VERIFIED", "VERIFIED", "VERIFIED", "SENT", "PLANNED", "PLANNED", "PLANNED"], "label": "3 verified · 1 SENT unconfirmed · 3 planned"},
       {"kind": "action", "label": "Reconcile & resume", "variant": "recovery", "hint": "reads the server first; never re-sends"}]}]},
   {"name": "aside", "span": "3", "blocks": [health(),
     {"kind": "card", "title": "Content Admin", "pill": "ADMIN", "sub": "state/review", "blocks": [
       {"kind": "row", "title": "Old Ghost", "sub": "quest · hidden · ready for review", "pills": ["HIDDEN"]},
       {"kind": "row", "title": "Harvest Boar", "sub": "AI · no hidden column · containment by refs", "pills": ["DRAFT"]},
       {"kind": "row", "title": "Cabbage Seed", "sub": "item · hidden", "pills": ["HIDDEN"]}]},
     {"kind": "card", "title": "Recent activity", "blocks": [
       {"kind": "row", "title": "06_aerathiel_pvp_battle_logs", "sub": "44 reads · synced", "pills": ["DONE"]},
       {"kind": "row", "title": "24_rank_icon_swap_all31", "sub": "31 edits", "pills": ["VERIFIED"]}]}]}]},
 "notes": ["Readiness lamps come from AuthState.describe(), the picker cache (pickerAt/pickerError) and Budget.status(); a lamp that was never probed renders 'not checked', never green (D2.3 ReadinessCard; H R-16).",
           "The active-work card is the journal's resumable() job; its single primary action is the job's own recovery construction (no Retry anywhere).",
           "Lane cards carry colour and glow and no lifecycle state; status cards carry state and no glow (D2.3 LaneCard).",
           "Quick actions never fill with crimson, gold or green (departures 1, 2, 9); the mockup's 'Create Content' and 'Edit & Write' are not shown because no such capability exists (H R-16).",
           "'Review queue' count is read from the repository review file (section F queue model, K-09), never from a live poll."],
 "pending": [PEND_NAV, "K-31 hero art (CSS atmosphere shown)", "K-03/K-09 whether the admin block appears for an operator without the role"],
 "cites": ["D_VISUAL_SYSTEM D2.3 ReadinessCard, ActiveWorkCard, QuickActionTile, LaneCard", "forge/src/ui/app.mjs:137-150 (auth banner), forge/src/storage/journal.mjs (resumable)", "harvests/inbox/tnr_results_1789188714166.json and 1789189076617.json (05/06 Builder runs)"]})
# ------------------------------------------------------------ WF-02
S.append({"id": "wf02_lane_quests", "title": "Lane landing: Quests & Events", "purpose": "A content lane groups everything about one workflow class: hidden records (from committed captures and catalogs, zero live), manifests that touch the class, the Studio entry, and admin items.",
 "flow": "Command Center → lane → record or manifest or Studio. No live read happens on entry; 'Refresh from live' is an explicit read action with its cost shown.",
 "mobile": [brand(), bar("Quests & Events", "lane", ["3 hidden", "2 manifests"]),
  {"kind": "tabs", "items": ["Records", "Manifests", "Studio", "Admin"], "active": "Records"},
  {"kind": "list", "rows": [
    {"title": "Old Ghost", "sub": "quest · KmGPDnZ… · captured 2026-09-11", "pills": ["HIDDEN"], "actions": ["Open"]},
    {"title": "One Perfect Crop", "sub": "mission · 4 objectives · in Studio", "pills": ["DRAFT"], "actions": ["Open"]},
    {"title": "Forsworn scene characters", "sub": "quest edits · 16c pack", "pills": ["VERIFIED"], "actions": ["Open"]}]},
  {"kind": "action", "label": "Refresh list from live · 1 read", "variant": "read", "hint": "quests.getAllNames · public · costs 1 of 30"},
  {"kind": "card", "title": "Quest Studio", "sub": "one Studio, subtype adapters", "blocks": [
    {"kind": "row", "title": "Mission", "sub": "supported · 48 profiles", "pills": ["ok"], "actions": ["New draft"]},
    {"kind": "row", "title": "Event · Story · Raid · Pyramid · Daily", "sub": "needs compiler / recipe (registry)", "pills": ["PLANNED"]}]},
  pnav("Work")],
 "desktop": {"columns": "220px minmax(420px,2fr) minmax(300px,1fr)", "regions": [
   {"name": "rail", "span": "1", "blocks": [rail("Build & Update")]},
   {"name": "main", "span": "2", "blocks": [bar("Quests & Events", "lane", ["3 hidden", "2 manifests", "1 draft"]),
     {"kind": "tabs", "items": ["Records", "Manifests", "Studio", "Admin"], "active": "Records"},
     {"kind": "list", "rows": [
       {"title": "Old Ghost", "sub": "quest · KmGPDnZnGOCvATQqA5LI8 · captured 2026-09-11 (summary)", "pills": ["HIDDEN"], "actions": ["Open", "Capture full"]},
       {"title": "One Perfect Crop", "sub": "mission · Studio draft · compiled valid 09-12", "pills": ["DRAFT"], "actions": ["Open in Studio"]},
       {"title": "Forsworn scene characters", "sub": "16c pack · 9 quest edits read back", "pills": ["VERIFIED"], "actions": ["Results"]}]},
     {"kind": "action", "label": "Refresh list from live · 1 read", "variant": "read", "hint": "explicit; shows the budget cost before the tap"}]},
   {"name": "aside", "span": "3", "blocks": [health(), {"kind": "card", "title": "Manifests touching this lane", "blocks": [
       {"kind": "row", "title": "01_old_ghost_format_capture", "sub": "capture-only", "pills": ["READ-ONLY"]},
       {"title": "46_mission_flatten", "kind": "row", "sub": "7 quest edits", "pills": ["LIVE-WRITE"]}]}]}]},
 "notes": ["Lists are projections of committed captures/catalogs (answers/, harvests/), so entering a lane spends no budget (R-03).",
           "Unsupported Studio subtypes are shown as disabled with the registry maturity reason, never hidden and never enabled (registry-driven rule, section F).",
           "Lane names are illustrative until K-24; the grouping shown follows workflow classes (section C.3)."],
 "pending": [PEND_NAV, "K-27 subtype rollout order", "K-17 research-read registry expansion (which list reads are allowed)"],
 "cites": ["push/01_old_ghost_format_capture.json", "824c4d58:skills/building-tnr-content/data/49_DATA_quest_studio_subtypes.json", "D_VISUAL_SYSTEM D2.3 LaneCard"]})
# ------------------------------------------------------------ WF-03
S.append({"id": "wf03_manifest_discover", "title": "Manifest discover (picker)", "purpose": "Brief §7 steps 1-4: discover from push/ (repository), classify automatically, show title/provenance/entity count/operations before anything is loaded into a job.",
 "flow": "Build & Update → picker → tap a manifest → preflight (WF-04). Local import and zip packs are shown as disabled until parity rows P-02/P-06 are built.",
 "mobile": [brand(), bar("Manifests", "push/ on main", ["7 listed", "4 m ago"]),
  {"kind": "form", "fields": [["search", "type to filter (name, entity, note)"]]},
  {"kind": "list", "rows": [
    {"title": "00_forge_readonly_smoke", "sub": "capture-only · 2 reads · ran 3x", "pills": ["READ-ONLY", "DONE"]},
    {"title": "02_one_perfect_crop_asset_probe", "sub": "capture-only · 5 FULL reads", "pills": ["READ-ONLY", "FULL"]},
    {"title": "05_aerathiel_pvp_research_stage1", "sub": "combat.getBattleHistory + 15 jutsu.get", "pills": ["READ-ONLY", "NEEDS-DECISION"]},
    {"title": "46_mission_flatten", "sub": "7 quest edits · 0 creates", "pills": ["LIVE-WRITE"]}]},
  {"kind": "action", "label": "Import from device (.json / .zip)", "variant": "disabled", "hint": "needs P-02 / P-06 capability first"},
  pnav("Work")],
 "desktop": {"columns": "220px minmax(420px,2fr) minmax(300px,1fr)", "regions": [
   {"name": "rail", "span": "1", "blocks": [rail("Build & Update")]},
   {"name": "main", "span": "2", "blocks": [bar("Manifests", "push/ on main@305a28f", ["7 listed", "listed 4 m ago", "Refresh listing"]),
     {"kind": "list", "rows": [
       {"title": "00_forge_readonly_smoke", "sub": "capture-only · jutsu.getAllNames, quests.getAllNames · ran 3x", "pills": ["READ-ONLY", "DONE"], "actions": ["Preflight"]},
       {"title": "02_one_perfect_crop_asset_probe", "sub": "5 gameAsset.get persist:'full' · bodies to public repo", "pills": ["READ-ONLY", "FULL"], "actions": ["Preflight"]},
       {"title": "05_aerathiel_pvp_research_stage1", "sub": "combat.getBattleHistory (not in registry) + 15 jutsu.get", "pills": ["READ-ONLY", "NEEDS-DECISION"], "actions": ["Preflight"]},
       {"title": "46_mission_flatten", "sub": "7 quest edits · asserted keys · read-back", "pills": ["LIVE-WRITE"], "actions": ["Preflight"]}]}]},
   {"name": "aside", "span": "3", "blocks": [health(), {"kind": "kv", "pairs": [["source", "push/ (main)"], ["classification", "parseManifest → planOrder"], ["ran marker", "from journal history"], ["import", "disabled: P-02/P-06"]]}]}]},
 "notes": ["Classification (READ-ONLY / LIVE-WRITE / FULL / NEEDS-DECISION) is derived from the parsed plan, never chosen by the user (K-33 derived mode).",
           "A manifest whose procedure is outside the audited registry is listed and flagged, not hidden; preflight refuses it with the registry reason (P-10).",
           "'ran 3x' comes from the journal, replacing today's 'ran' pill that borrows the VERIFIED colour (screens.mjs:86)."],
 "pending": [PEND_NAV, "K-17 research reads", "K-11 retirement timing (import/zip parity gates)"],
 "cites": ["forge/src/ui/app.mjs:186-207 (picker lists push/*.json on main)", "parity rows P-02, P-03, P-06, P-10", "push/*.json"]})
# ------------------------------------------------------------ WF-04
S.append({"id": "wf04_preflight_live_write", "title": "Preflight: LIVE WRITE", "purpose": "Brief §7 steps 5-9: blockers and advisories, reads/writes/uploads distinct, live-state diff where safe, an unmistakable statement that this run mutates, and one explicit operator action.",
 "flow": "Picker → preflight → (fix blockers in the repository) → Start job → confirmation sheet (WF-13 style, LIVE WRITE construction) → run (WF-05).",
 "mobile": [brand(), bar("46_mission_flatten", "quest · edits", ["push/"]),
  {"kind": "opmode", "mode": "LIVE WRITE", "counts": [["updates", 7], ["creates", 0], ["reads", 7], ["uploads", 0]], "note": "Writes to the live game. Every write is journaled before it is sent and read back after."},
  {"kind": "banner", "tone": "warn", "head": "1 advisory", "body": "L07: objective text over 240 chars on 'Cabbage run'. Not a blocker."},
  {"kind": "card", "title": "Plan", "sub": "manifest order kept", "blocks": [
    {"kind": "row", "title": "One Perfect Crop", "sub": "quest · update · objectives, rewards", "pills": ["PLANNED"]},
    {"kind": "row", "title": "Cabbage run", "sub": "quest · update · objectives", "pills": ["PLANNED"]},
    {"kind": "row", "title": "… 5 more", "sub": "", "pills": []}]},
  {"kind": "card", "title": "Live diff (safe: 7 reads)", "sub": "read at 14:02", "blocks": [{"kind": "diff", "rows": [["objectives[0].task", "collect_item", "collect_item"], ["objectives[1]", "(4 objectives)", "(3 objectives)"], ["hidden", "true", "true"]]}]},
  {"kind": "action", "label": "Start job → writes 7 records", "variant": "mutation", "hint": "asks once; names the counts again"},
  pnav("Work")],
 "desktop": {"columns": "220px minmax(420px,2fr) minmax(300px,1fr)", "regions": [
   {"name": "rail", "span": "1", "blocks": [rail("Build & Update")]},
   {"name": "main", "span": "2", "blocks": [bar("46_mission_flatten.json", "quest · 7 edits", ["push/", "parsed 14:02"]),
     {"kind": "opmode", "mode": "LIVE WRITE", "counts": [["updates", 7], ["creates", 0], ["reads", 7], ["uploads", 0], ["publishes", 0]], "note": "Writes to the live game. Journaled before send; read back after. Nothing becomes player-visible (hidden stays true)."},
     {"kind": "banner", "tone": "warn", "head": "1 advisory, 0 blockers", "body": "L07 long objective text on 'Cabbage run'."},
     {"kind": "list", "rows": [
       {"title": "One Perfect Crop", "sub": "quest · update · objectives, rewards · id KmGP…", "pills": ["PLANNED"], "actions": ["Diff"]},
       {"title": "Cabbage run", "sub": "quest · update · objectives", "pills": ["PLANNED"], "actions": ["Diff"]},
       {"title": "Road Bandit ambush", "sub": "quest · update · objectives", "pills": ["PLANNED"], "actions": ["Diff"]}]},
     {"kind": "action", "label": "Start job → writes 7 records", "variant": "mutation", "hint": "one confirmation; counts restated; Cancel far end"}]},
   {"name": "aside", "span": "3", "blocks": [health(), {"kind": "tabs", "items": ["Summary", "Live diff", "Raw manifest", "Plan JSON"], "active": "Live diff"},
     {"kind": "diff", "rows": [["objectives[0].task", "collect_item", "collect_item"], ["objectives[1]", "(4 objectives)", "(3 objectives)"], ["hidden", "true", "true"]]},
     {"kind": "kv", "pairs": [["budget after reads", "7 of 30 used"], ["read-back keys", "objectives, rewards"], ["srcId idempotency", "per job (P-21)"]]}]}]},
 "notes": ["The mode band renders before the item list and its counts come from the parsed plan (planOrder), never from a user choice.",
           "Preflight reads (the live diff) are shown as reads in the band and charged to the budget meter before the tap.",
           "Blockers refuse the Start control (disabled with the reason); advisories do not. Fixes happen in the repository, not in Forge (RUL-2026-09-12-002).",
           "The confirmation is a ConfirmationSurface in the LIVE WRITE construction (D2.3), replacing window.confirm (H R-12)."],
 "pending": ["K-21/K-22 mode taxonomy and colours (defaults shown)", "K-12 confirmation level for publish is separate (this is a hidden write)"],
 "cites": ["forge/src/runner/manifest.mjs (parseManifest/planOrder)", "forge/src/ui/screens.mjs:104-125 (preflight lists today)", "SSC §2 axes; IRM R-classes; WFA preflight anatomy"]})
# ------------------------------------------------------------ WF-05
S.append({"id": "wf05_run_live", "title": "Run in progress", "purpose": "Brief §7 steps 10-11: live per-item progress, the budget, and a safe pause that the operator can always reach. Nothing on this screen can re-send.",
 "flow": "Start → RUNNING → per item SENT → CONFIRMED → read-back → VERIFIED. Pause after this item is always available; the halt card (WF-06) replaces the progress card on a pause.",
 "mobile": [brand(), bar("46_mission_flatten", "RUNNING", ["item 4 of 7"]),
  {"kind": "opmode", "mode": "LIVE WRITE", "counts": [["updates", 7], ["verified", 3], ["sent", 1]], "note": "Running. Leaving this page is safe: the journal resumes it."},
  {"kind": "seg", "cells": ["VERIFIED", "VERIFIED", "VERIFIED", "RUNNING", "PLANNED", "PLANNED", "PLANNED"], "label": "3 verified · 1 in flight · 3 planned · 7 total"},
  {"kind": "list", "rows": [
    {"title": "One Perfect Crop", "sub": "quest · update · read back: match", "pills": ["VERIFIED"]},
    {"title": "Cabbage run", "sub": "quest · update · read back: match", "pills": ["VERIFIED"]},
    {"title": "Road Bandit ambush", "sub": "quest · update", "pills": ["VERIFIED"]},
    {"title": "Harvest Boar hunt", "sub": "quest · update · request in flight", "pills": ["SENT"]},
    {"title": "Market Clerk", "sub": "quest · update", "pills": ["PLANNED"]}]},
  {"kind": "action", "label": "Pause after this item", "variant": "ghost", "hint": "never interrupts a request that already left"},
  {"kind": "card", "title": "Technical", "sub": "budget · journal", "blocks": [{"kind": "progress", "pct": 27, "label": "quests.update · 8 of 30 · resets 0:41"}]},
  pnav("Jobs")],
 "desktop": {"columns": "220px minmax(420px,2fr) minmax(300px,1fr)", "regions": [
   {"name": "rail", "span": "1", "blocks": [rail("Jobs & Recovery"), note("3 px --mut-edge underline on the shell while a mutation job runs")]},
   {"name": "main", "span": "2", "blocks": [bar("46_mission_flatten.json", "RUNNING · item 4 of 7", ["journal j_1789…"]),
     {"kind": "opmode", "mode": "LIVE WRITE", "counts": [["updates", 7], ["verified", 3], ["sent", 1], ["planned", 3]], "note": "Running. Every write is journaled before send."},
     {"kind": "seg", "cells": ["VERIFIED", "VERIFIED", "VERIFIED", "RUNNING", "PLANNED", "PLANNED", "PLANNED"], "label": "3 verified · 1 in flight · 3 planned · 7 total"},
     {"kind": "list", "rows": [
       {"title": "One Perfect Crop", "sub": "quest · update · KmGP… · read back: match", "pills": ["VERIFIED"]},
       {"title": "Cabbage run", "sub": "quest · update · read back: match", "pills": ["VERIFIED"]},
       {"title": "Road Bandit ambush", "sub": "quest · update · read back: match", "pills": ["VERIFIED"]},
       {"title": "Harvest Boar hunt", "sub": "quest · update · request in flight (SENT)", "pills": ["SENT"]},
       {"title": "Market Clerk", "sub": "quest · update", "pills": ["PLANNED"]}]},
     {"kind": "action", "label": "Pause after this item", "variant": "ghost"}]},
   {"name": "aside", "span": "3", "blocks": [{"kind": "lamps", "head": "Budget", "items": [{"glyph": "✓", "label": "quests.update", "value": "8 of 30 · resets 0:41", "tone": "ok"}, {"glyph": "✓", "label": "quests.get", "value": "7 of 30", "tone": "ok"}]},
     {"kind": "tabs", "items": ["Summary", "Journal", "Raw"], "active": "Summary"}, {"kind": "kv", "pairs": [["lease", "this tab"], ["persisted", "yes (navigator.storage)"], ["asserted keys", "objectives, rewards"]]}]}]},
 "notes": ["SegmentedProgress: one cell per item; only the in-flight cell carries motion; state pills never animate (D2.4).",
           "SENT is orchid hatch with a dashed rule and no action; CONFIRMED is blue and not terminal; VERIFIED is the only green.",
           "The bottom navigation stays during a run (D2.3 BottomNav); the shell underline carries the mode when the band scrolls away (CC-M2)."],
 "pending": ["K-21/K-22 colours (defaults shown)"],
 "cites": ["forge/src/runner/runner.mjs (SENT → CONFIRMED → read-back)", "forge/src/ui/screens.mjs:200-232 (run screen today)", "SSC §3-§5"]})
# ------------------------------------------------------------ WF-06
S.append({"id": "wf06_halt_sent", "title": "Halted: SENT reconciliation required", "purpose": "The ambiguous state made unmistakable: a request may have left the device; the only offered action reads the server first and can never re-send.",
 "flow": "Eviction / network loss mid-request → journal holds SENT → on reopen the halt card replaces progress → Reconcile & resume → per-item resolution → continue or orphan decision (WF-07).",
 "mobile": [brand(), bar("46_mission_flatten", "PAUSED · AMBIGUOUS", ["item 4"]),
  {"kind": "opmode", "mode": "RECOVERY", "counts": [["unconfirmed", 1], ["verified", 3], ["planned", 3]], "note": "One write may have reached the game. Nothing is retried."},
  {"kind": "banner", "tone": "warn", "head": "? 1 WRITE UNCONFIRMED", "body": "'Harvest Boar hunt' was sent at 14:06 and no answer was recorded. Reconcile reads the server first; it never re-sends."},
  {"kind": "card", "title": "Harvest Boar hunt", "pill": "SENT", "sub": "quest · update · sent 14:06:12", "risk": "recovery", "blocks": [
    {"kind": "kv", "pairs": [["what left", "quests.update {objectives, rewards}"], ["what is known", "no response recorded"], ["what resume does", "reads the record, compares asserted keys"]]}]},
  {"kind": "action", "label": "Reconcile & resume", "variant": "recovery", "hint": "reads first, never re-sends"},
  {"kind": "action", "label": "Export journal", "variant": "ghost"},
  pnav("Jobs")],
 "desktop": {"columns": "220px minmax(420px,2fr) minmax(300px,1fr)", "regions": [
   {"name": "rail", "span": "1", "blocks": [rail("Jobs & Recovery"), note("recovery hatch underline on the shell; SENT dot on the Jobs badge")]},
   {"name": "main", "span": "2", "blocks": [bar("46_mission_flatten.json", "PAUSED · reason AMBIGUOUS", ["journal j_1789…"]),
     {"kind": "opmode", "mode": "RECOVERY", "counts": [["unconfirmed", 1], ["verified", 3], ["planned", 3]], "note": "One write may have reached the game. Nothing is retried."},
     {"kind": "banner", "tone": "warn", "head": "? 1 WRITE UNCONFIRMED", "body": "Sent 14:06:12, no answer recorded. Reconcile reads the server first; it never re-sends."},
     {"kind": "seg", "cells": ["VERIFIED", "VERIFIED", "VERIFIED", "SENT", "PLANNED", "PLANNED", "PLANNED"], "label": "3 verified · 1 SENT unconfirmed · 3 planned"},
     {"kind": "list", "rows": [{"title": "Harvest Boar hunt", "sub": "quest · update · sent 14:06:12 · no response", "pills": ["SENT"], "actions": ["Details"]}]},
     {"kind": "action", "label": "Reconcile & resume", "variant": "recovery", "hint": "reads the record and compares asserted keys before anything continues"}]},
   {"name": "aside", "span": "3", "blocks": [health(), {"kind": "tabs", "items": ["Summary", "Journal", "Raw"], "active": "Journal"}, {"kind": "kv", "pairs": [["state", "SENT"], ["phase", "update"], ["sentAt", "14:06:12.410"], ["reason", "AMBIGUOUS"]]}]}]},
 "notes": ["No control on this screen is bound to a send path while any item is SENT (I: UI-contract test).",
           "Copy comes from the CPY label dictionary ('Reconcile & resume', 'never re-sent'); construction from D2.3 RecoveryCard.",
           "The journal already forbids SENT → PLANNED (journal.mjs:39-47); the screen only exposes what the reconciler does."],
 "pending": [PEND_NAV],
 "cites": ["forge/src/storage/journal.mjs:39-47", "forge/src/runner/runner.mjs:193 (refuses SENT jobs)", "forge/src/reconcile/reconciler.mjs", "SSC §3 SENT; MOB §7 recovery"]})
# ------------------------------------------------------------ WF-07
S.append({"id": "wf07_orphan_decision", "title": "Orphan decision", "purpose": "A two-phase create whose placeholder exists but whose second phase is unknown: the operator adopts a candidate, skips, or (exceptionally) re-sends. Name before id, one candidate per row, nothing preselected, no deletion.",
 "flow": "Reconcile finds a new record matching the pre-create snapshot diff → orphan card pinned above the job → decision → journal records adopt/skip/re-send with the operator's choice.",
 "mobile": [brand(), bar("16c_forsworn_pack", "ORPHANED", ["1 to decide"]),
  {"kind": "opmode", "mode": "RECOVERY", "counts": [["orphaned", 1], ["verified", 8]], "note": "A placeholder exists on the live game. Decide what it is."},
  {"kind": "card", "title": "DECIDE · Forsworn Sentinel (scene character)", "pill": "ORPHANED", "sub": "asset · create · phase 2 unknown", "risk": "recovery", "blocks": [
    {"kind": "kv", "pairs": [["known", "placeholder created 13:58; upload phase unconfirmed"], ["snapshot diff", "1 new gameAsset since pre-create"]]},
    {"kind": "row", "title": "Forsworn Sentinel", "sub": "id 8mDurYQY… · created 13:58:41 · hidden", "pills": ["HIDDEN"], "actions": ["Adopt"]},
    {"kind": "action", "label": "Skip · leave the live row; nothing deleted", "variant": "ghost"},
    {"kind": "action", "label": "Re-send phase 2 (exceptional)", "variant": "danger", "hint": "creates nothing new; sends the upload again"}]},
  pnav("Jobs")],
 "desktop": {"columns": "220px minmax(420px,2fr) minmax(300px,1fr)", "regions": [
   {"name": "rail", "span": "1", "blocks": [rail("Jobs & Recovery")]},
   {"name": "main", "span": "2", "blocks": [bar("16c_forsworn_scene_characters_pack", "ORPHANED · 1 decision", ["zip pack"]),
     {"kind": "opmode", "mode": "RECOVERY", "counts": [["orphaned", 1], ["verified", 8], ["planned", 0]], "note": "A placeholder exists on the live game. Nothing is deleted automatically."},
     {"kind": "card", "title": "DECIDE · Forsworn Sentinel", "pill": "ORPHANED", "sub": "gameAsset · two-phase create", "risk": "recovery", "blocks": [
       {"kind": "kv", "pairs": [["what is known", "create returned an id; the update/upload phase has no recorded answer"], ["candidates", "from the pre-create name snapshot diff (1)"]]},
       {"kind": "row", "title": "Forsworn Sentinel", "sub": "8mDurYQYmy3G0vb862mkO · 13:58:41 · hidden:true · no image", "pills": ["HIDDEN"], "actions": ["Adopt this record"]},
       {"kind": "action", "label": "Skip · leave the live row; nothing deleted", "variant": "ghost"},
       {"kind": "action", "label": "Re-send phase 2 (exceptional)", "variant": "danger", "hint": "sheet restates: no new create; upload again to 8mDurYQY…"}]}]},
   {"name": "aside", "span": "3", "blocks": [health(), {"kind": "kv", "pairs": [["deletion", "never (K-16)"], ["snapshot", "tnr_forge_snap_v1:…"], ["idmap", "srcId → id after adopt"]]}]}]},
 "notes": ["The three controls are spatially separated (MOB §7); Re-send is styled as exceptional and routes through a ConfirmationSurface naming phase and target (D2.3).",
           "Candidate name renders above the raw id (today the id comes first, screens.mjs:57).",
           "Skip repeats the consequence in its label: nothing is deleted and the live row may remain (K-16 policy stays open)."],
 "pending": ["K-16 deletion policy for placeholders and orphans"],
 "cites": ["forge/src/reconcile/reconciler.mjs (snapshot diff, adopt)", "forge/src/ui/screens.mjs:56-68 (today's orphan rows)", "SSC §4 orphan; MOB §7; WFA orphan anatomy"]})
# ------------------------------------------------------------ WF-08
S.append({"id": "wf08_results_sync", "title": "Results and sync", "purpose": "Brief §7 steps 12-13: read-back summary and the repository hand-off as two separate claims. A green game result never implies the bundle reached the repository.",
 "flow": "Job DONE → ResultSummary (compile n/a · execution · verification · sync · publication) → Sync to repository (GitHub PAT) or Export text → archive hint.",
 "mobile": [brand(), bar("46_mission_flatten", "DONE", ["7 items"]),
  {"kind": "lamps", "head": "Result", "items": [
    {"glyph": "✓", "label": "EXECUTION", "value": "7 updates confirmed", "tone": "ok"},
    {"glyph": "✓", "label": "VERIFIED", "value": "7 of 7 read back match", "tone": "ok"},
    {"glyph": "✕", "label": "SYNC", "value": "Results not synced · PAT not configured", "tone": "bad"},
    {"glyph": "–", "label": "PUBLISH", "value": "hidden stays true (no publish action)", "tone": "mute"}]},
  {"kind": "seg", "cells": ["VERIFIED"] * 7, "label": "7 verified · 7 total"},
  {"kind": "action", "label": "Sync results to repository", "variant": "primary", "hint": "harvests/inbox/tnr_results_….json · needs PAT"},
  {"kind": "action", "label": "Export bundle as text", "variant": "ghost"},
  pnav("Jobs")],
 "desktop": {"columns": "220px minmax(420px,2fr) minmax(300px,1fr)", "regions": [
   {"name": "rail", "span": "1", "blocks": [rail("Jobs & Recovery")]},
   {"name": "main", "span": "2", "blocks": [bar("46_mission_flatten.json", "DONE · 14:09", ["bundle 61 KB"]),
     {"kind": "lamps", "head": "Result summary (separate claims)", "items": [
       {"glyph": "✓", "label": "EXECUTION", "value": "7 updates confirmed by the server", "tone": "ok"},
       {"glyph": "✓", "label": "VERIFIED", "value": "7 of 7 asserted keys match on read-back", "tone": "ok"},
       {"glyph": "✕", "label": "SYNC", "value": "Repository sync failed: 409 on harvests/inbox (auto commit raced); journaled as job.sync=failed", "tone": "bad", "actions": ["Retry sync"]},
       {"glyph": "–", "label": "PUBLISH", "value": "not applicable: hidden stays true", "tone": "mute"}]},
     {"kind": "list", "rows": [{"title": "One Perfect Crop", "sub": "objectives, rewards · match", "pills": ["VERIFIED"]}, {"title": "Cabbage run", "sub": "objectives · match", "pills": ["VERIFIED"]}]},
     {"kind": "action", "label": "Retry sync (repository only)", "variant": "primary", "hint": "retry-safe: no game request"}]},
   {"name": "aside", "span": "3", "blocks": [health(), {"kind": "kv", "pairs": [["bundle", "tnr_results_1789…json"], ["harvest.py", "compatible (P-52)"], ["parity guard", "checks: null → fix R-19"], ["archive", "push/ → archive/ after tap"]]}]}]},
 "notes": ["The sync state is journaled (job.sync ∈ not_configured | pending | committed | failed) so an eviction after DONE cannot lose the fact that the bundle never landed (F; H R-07).",
           "'Retry sync' is allowed because it is a repository-only request (retry-safe class); no control retries a game write.",
           "The DONE pill is no longer green regardless of outcome (today styles.mjs:44); the outcome lamps carry the verdicts."],
 "pending": ["K-15 credential model for the repository bridge", "K-06 capture classification (what may persist)"],
 "cites": ["forge/src/ui/app.mjs:402-405 (sync toast + showExport today)", "forge/src/github.mjs:50 (sha-aware PUT, no retry)", "SSC §12 game vs repo claims; CPY §14"]})
# ------------------------------------------------------------ WF-09
S.append({"id": "wf09_capture_preflight", "title": "Research capture: READ ONLY with FULL advisory", "purpose": "Zero-mutation research runs stay easy while full-body persistence to the public repository is called out before the tap (capture classification K-06).",
 "flow": "Capture & Research → manifest 02 → preflight shows every read, its tier and persistence → Run 5 reads → capture rows with two verdicts (read ok / body persisted).",
 "mobile": [brand(), bar("02_one_perfect_crop_asset_probe", "capture-only", ["5 reads"]),
  {"kind": "opmode", "mode": "READ ONLY", "counts": [["reads", 5], ["FULL", 5], ["writes", 0]], "note": "No game record changes. Five full bodies will be committed to the public repository."},
  {"kind": "banner", "tone": "warn", "head": "▣ FULL capture", "body": "gameAsset.get bodies persist to harvests/inbox/ (public). Tier: content point read, 512 KiB ceiling."},
  {"kind": "list", "rows": [
    {"title": "gameAsset.get XsLLy8aw…", "sub": "public · limited · persist: full", "pills": ["FULL"]},
    {"title": "gameAsset.get xsikTqet…", "sub": "public · limited · persist: full", "pills": ["FULL"]},
    {"title": "… 3 more", "sub": "", "pills": []}]},
  {"kind": "action", "label": "Run 5 reads · zero mutations", "variant": "read", "hint": "no confirmation for reads; budget 5 of 30"},
  pnav("Capture")],
 "desktop": {"columns": "220px minmax(420px,2fr) minmax(300px,1fr)", "regions": [
   {"name": "rail", "span": "1", "blocks": [rail("Capture & Research")]},
   {"name": "main", "span": "2", "blocks": [bar("02_one_perfect_crop_asset_probe.json", "capture-only", ["5 reads", "persist: full"]),
     {"kind": "opmode", "mode": "READ ONLY", "counts": [["reads", 5], ["FULL", 5], ["writes", 0], ["uploads", 0]], "note": "No game record changes. Five full bodies will be committed to the public repository."},
     {"kind": "list", "rows": [
       {"title": "gameAsset.get XsLLy8awDAtaE6hXVIi_0", "sub": "public · rate-limited · persist: full · content tier", "pills": ["FULL"]},
       {"title": "gameAsset.get xsikTqetvzo5OXKdTicK6", "sub": "public · rate-limited · persist: full", "pills": ["FULL"]},
       {"title": "combat.getBattleHistory (push/05)", "sub": "protected · NOT in the 43-procedure registry · research tier pending K-17", "pills": ["NEEDS-DECISION"]}]},
     {"kind": "action", "label": "Run 5 reads · zero mutations", "variant": "read"}]},
   {"name": "aside", "span": "3", "blocks": [health(), {"kind": "card", "title": "After the run (capture rows)", "blocks": [
       {"kind": "row", "title": "gameAsset.get XsLLy8aw…", "sub": "read ok ✓ · body persisted ✓ (41 KB)", "pills": ["VERIFIED"]},
       {"kind": "row", "title": "gameAsset.get HgT0DKfi…", "sub": "read ok ✓ · NOT persisted ✕ (over 512 KiB)", "pills": ["INCOMPLETE"]}]}]}]},
 "notes": ["Reads never confirm (IRM R0); the FULL advisory is a banner, not a dialog.",
           "A successful read never stands in for a persisted body: two verdicts per capture row (D2.3 CaptureRow; screens.mjs:123-125 already splits them).",
           "Procedures outside the registry are listed with the reason and refused at run time until K-17 admits a research tier (P-10)."],
 "pending": ["K-06 capture classification tiers", "K-17 research-read registry expansion"],
 "cites": ["forge/src/storage/captures.mjs:58-84 (full-persist allowlist, 512 KiB)", "push/02, push/05", "parity rows P-09..P-14"]})
# ------------------------------------------------------------ WF-10
S.append({"id": "wf10_captures_library", "title": "Captures library", "purpose": "Reuse before re-reading: committed and local captures with their tier, persistence and age; a re-read is an explicit, budgeted action.",
 "flow": "Capture & Research → library → open a capture → use it in a lane/Studio or re-read from live.",
 "mobile": [brand(), bar("Captures", "local cache + committed", ["31 local", "42 bundles"]),
  {"kind": "tabs", "items": ["Recent", "By record", "By procedure", "FULL"], "active": "Recent"},
  {"kind": "list", "rows": [
    {"title": "quests.get Old Ghost", "sub": "summary · 2026-09-11 · committed", "pills": ["READ-ONLY"], "actions": ["Open"]},
    {"title": "gameAsset.get ×5 (crop probe)", "sub": "FULL · local + committed", "pills": ["FULL"], "actions": ["Open"]},
    {"title": "profile.getAi ×5 (bandit AI)", "sub": "FULL · 2026-09-11", "pills": ["FULL"], "actions": ["Open"]}]},
  {"kind": "action", "label": "Invalidate this entry", "variant": "ghost", "hint": "asks once (today: no confirmation, screens.mjs:275)"},
  pnav("Capture")],
 "desktop": {"columns": "220px minmax(420px,2fr) minmax(300px,1fr)", "regions": [
   {"name": "rail", "span": "1", "blocks": [rail("Capture & Research")]},
   {"name": "main", "span": "2", "blocks": [bar("Captures library", "IndexedDB tnr_forge v2 + harvests/", ["31 local", "42 bundles"]),
     {"kind": "list", "rows": [
       {"title": "quests.get KmGPDnZnGOCvATQqA5LI8 (Old Ghost)", "sub": "summary · read 2026-09-11 · committed in tnr_results_1789124514980", "pills": ["READ-ONLY"], "actions": ["Open", "Re-read · 1"]},
       {"title": "gameAsset.get ×5 (One Perfect Crop asset probe)", "sub": "FULL · snapshot immutable · 5 bodies", "pills": ["FULL"], "actions": ["Open"]},
       {"title": "combat.getBattleEntries ×44 (Aerathiel)", "sub": "Builder v4.32 run · not readable by Forge 0.4.0 (P-10)", "pills": ["NEEDS-DECISION"]}]}]},
   {"name": "aside", "span": "3", "blocks": [health(), {"kind": "kv", "pairs": [["tiers", "repo-safe / local-only / projected (F.5, K-06)"], ["invalidate", "per entry, confirmed"], ["snapshots", "immutable (captures.mjs)"]]}]}]},
 "notes": ["Privacy tier labels wait for K-06; the library shows persistence facts (where the bytes are) without inventing a taxonomy.",
           "Bundles produced by Builder are listed from harvests/ so research done there stays reachable while retirement gates are open (J)."],
 "pending": ["K-06", "K-17"],
 "cites": ["forge/src/storage/captures.mjs", "forge/src/ui/screens.mjs:238-280 (captures screen today)", "harvest-evidence rows"]})
# ------------------------------------------------------------ WF-11
S.append({"id": "wf11_admin_queue", "title": "Content Admin: review queue", "purpose": "The admin never sees a manifest. Items are hidden live records (or Studio builds) that a job finished, listed from the repository review file, with the current live pill read from committed captures.",
 "flow": "Content Admin → queue (filter by lane/state) → detail (WF-12) → approve / request changes → publish (WF-13). Approval state lives in the repository (K-09), never invented on the client.",
 "mobile": [brand("ADMIN ✓"), bar("Review queue", "state/review", ["3 waiting", "1 changes requested"]),
  {"kind": "tabs", "items": ["Waiting", "Changes", "Approved", "Published"], "active": "Waiting"},
  {"kind": "list", "rows": [
    {"title": "Old Ghost", "sub": "quest · hidden · job 24 verified 09-11", "pills": ["HIDDEN"], "actions": ["Review"]},
    {"title": "Cabbage Seed", "sub": "item · hidden · icon pending art", "pills": ["HIDDEN", "NEEDS-DECISION"], "actions": ["Review"]},
    {"title": "Harvest Boar", "sub": "AI · no hidden column · referenced by 1 hidden quest", "pills": ["DRAFT"], "actions": ["Review"]}]},
  {"kind": "banner", "tone": "info", "head": "Role", "body": "MODERATOR (from profile.getUser). Server enforces canChangeContent on every write; a refusal arrives as HTTP 200 success:false."},
  pnav("More")],
 "desktop": {"columns": "220px minmax(420px,2fr) minmax(300px,1fr)", "regions": [
   {"name": "rail", "span": "1", "blocks": [rail("Content Admin"), note("gold-outline pending count badge")]},
   {"name": "main", "span": "2", "blocks": [bar("Review queue", "state/review/*.json · read 3 m ago", ["3 waiting", "1 changes requested", "2 approved"]),
     {"kind": "tabs", "items": ["Waiting", "Changes requested", "Approved", "Published"], "active": "Waiting"},
     {"kind": "list", "rows": [
       {"title": "Old Ghost", "sub": "quest · HIDDEN (captured 09-11) · from job 24_rank_icon_swap · lane Quests & Events", "pills": ["HIDDEN"], "actions": ["Review"]},
       {"title": "Cabbage Seed", "sub": "item · HIDDEN · icon not yet in repository (art boundary)", "pills": ["HIDDEN", "NEEDS-DECISION"], "actions": ["Review"]},
       {"title": "Harvest Boar", "sub": "AI (userData isAi) · no hidden column · contained by refs", "pills": ["DRAFT"], "actions": ["Review"]}]}]},
   {"name": "aside", "span": "3", "blocks": [{"kind": "lamps", "head": "Admin readiness", "items": [{"glyph": "✓", "label": "SESSION", "value": "signed in · role MODERATOR", "tone": "ok"}, {"glyph": "✓", "label": "REPO", "value": "review file read 3 m ago", "tone": "ok"}, {"glyph": "✓", "label": "BUDGET", "value": "no live reads on this screen", "tone": "ok"}]},
     {"kind": "kv", "pairs": [["approval store", "repository file (K-09)"], ["queue source", "job results + Studio builds"], ["publish", "separate act (WF-13)"]]}]}]},
 "notes": ["Approval state is a repository record proposed in F; it is never derived on the client and never becomes a second canon (RUL-2026-09-12-002).",
           "Role is learned without credential material (profile.getUser); the client never gates by role, it only shapes copy. Denial rendering waits for E's source audit (K-34).",
           "This queue spends no live budget; the live pill is the last committed capture with its age."],
 "pending": ["K-03 admin permission scope", "K-04 admin write scope", "K-05 first-class classes", "K-09 approval store", "K-34 denial signal", "K-30 late admin visuals (pending predecessor-transcript reconciliation)"],
 "cites": ["deepdive game-auth-roles (permissions.ts canChangeContent; profile.getUser)", "E per-class publication axis", "WCM §23 AdminReviewCard"]})
# ------------------------------------------------------------ WF-12
S.append({"id": "wf12_admin_detail", "title": "Content Admin: detail, edit, preview", "purpose": "Human-readable record: what changed in plain terms, a preview in the class's own renderer where one exists, a narrow editorial edit, and the approval decision. No JSON.",
 "flow": "Queue → detail → (edit → hidden write, journaled like any job) → approve or request changes → publish (WF-13).",
 "mobile": [brand("ADMIN ✓"), bar("Old Ghost", "quest · HIDDEN", ["waiting"]),
  {"kind": "tabs", "items": ["Summary", "Preview", "Changes", "History"], "active": "Summary"},
  {"kind": "preview", "label": "player preview · quest card renderer", "body": "Old Ghost — Rank C — 3 objectives — rewards: 1,200 ryo. Reflects the LIVE hidden record read at 13:40."},
  {"kind": "diff", "rows": [["name", "New Quest - draft", "Old Ghost"], ["objectives", "0", "3"], ["hidden", "true", "true"]]},
  {"kind": "form", "fields": [["description (editorial)", "A ghost haunts the old mill road…", "area"], ["rank", "C", "ro"]]},
  {"kind": "action", "label": "Save edit → writes 1 hidden record", "variant": "mutation", "hint": "journaled; read back"},
  {"kind": "action", "label": "Approve for publish", "variant": "ghost", "hint": "records approval in the repository"},
  pnav("More")],
 "desktop": {"columns": "220px minmax(420px,2fr) minmax(300px,1fr)", "regions": [
   {"name": "rail", "span": "1", "blocks": [rail("Content Admin")]},
   {"name": "main", "span": "2", "blocks": [bar("Old Ghost", "quest · HIDDEN · KmGPDnZnGOCvATQqA5LI8", ["waiting", "job 24"]),
     {"kind": "preview", "label": "player preview · quest card renderer (client route)", "body": "Old Ghost — Rank C — 3 objectives — rewards 1,200 ryo. Preview reflects the LIVE hidden record read at 13:40."},
     {"kind": "diff", "rows": [["name", "New Quest - draft", "Old Ghost"], ["objectives", "0 objectives", "3 objectives"], ["rewards.money", "0", "1200"], ["hidden", "true", "true"]]},
     {"kind": "form", "fields": [["description (editorial edit)", "A ghost haunts the old mill road…", "area"], ["rank", "C", "ro"], ["rewards", "director-owned (K-04)", "ro"]]},
     {"kind": "action", "label": "Save edit → writes 1 hidden record", "variant": "mutation", "hint": "quests.update whole-record semantics: read-merge-write, asserted keys read back"}]},
   {"name": "aside", "span": "3", "blocks": [{"kind": "lamps", "head": "Decision", "items": [{"glyph": "△", "label": "DEPENDS", "value": "Harvest Boar (AI) still hidden-by-reference", "tone": "warn"}, {"glyph": "✓", "label": "VERIFIED", "value": "last job read back matched", "tone": "ok"}]},
     {"kind": "action", "label": "Approve for publish", "variant": "primary"}, {"kind": "action", "label": "Request changes", "variant": "ghost"},
     {"kind": "kv", "pairs": [["history", "actionLog (game) + bundles + git"], ["editor", "narrow fields only (K-04)"]]}]}]},
 "notes": ["Edits are ordinary journaled hidden writes: whole-record procedures are read-merge-write with asserted-key read-back (routers audit: validators drop unknown keys).",
           "Preview uses the class's existing client renderer when one exists (E per class); classes without a renderer show a neutral empty state, never an error.",
           "Balance/reward fields are read-only for the admin unless K-04 rules otherwise; the director owns those values (CLAUDE.md §10)."],
 "pending": ["K-04", "K-05", "K-08 (direct hidden edit vs staged package)", "K-09"],
 "cites": ["deepdive game-routers (quests.update whole-record; actionLog/contentBackups)", "game-client-editors-previews rows", "D2.3 PreviewFrame, DiffView"]})
# ------------------------------------------------------------ WF-13
S.append({"id": "wf13_publish_confirm", "title": "Publish: PUBLISH mode and confirmation", "purpose": "The one action that makes content player-visible: gold band, the exact flip in words, dependencies that are still hidden, one action in the publish construction, Cancel at the far end. Read back before the screen closes.",
 "flow": "Approved item → Publish → PUBLISH band + sheet → (typed name / hold: K-12) → hidden:false sent → read back → PUBLISHED pill only after read-back.",
 "mobile": [brand("ADMIN ✓"), bar("Old Ghost", "publish", ["approved"]),
  {"kind": "opmode", "mode": "PUBLISH", "counts": [["publishes", 1], ["reads", 2], ["writes", 1]], "note": "Makes 'Old Ghost' visible to players. hidden: true → false."},
  {"kind": "banner", "tone": "warn", "head": "▲ Dependency still hidden", "body": "Harvest Boar (AI) is referenced by this quest and is contained by references, not a hidden column. Players will meet it."},
  {"kind": "sheet", "title": "Publish Old Ghost → player-visible", "lines": ["hidden: true → false on KmGPDnZn…", "session READY · role MODERATOR", "read back after send; PUBLISHED only on read-back"], "action": {"label": "Publish 1 record", "variant": "publish", "state": "disabled"}, "cancel": "Cancel"},
  {"kind": "form", "fields": [["type the record name to arm (K-12 option b)", "Old Gh…"]]},
  pnav("More")],
 "desktop": {"columns": "220px minmax(420px,2fr) minmax(300px,1fr)", "regions": [
   {"name": "rail", "span": "1", "blocks": [rail("Content Admin"), note("gold underline on the shell while a publish is in flight")]},
   {"name": "main", "span": "2", "blocks": [bar("Old Ghost", "PUBLISH · approved by dauntless 09-12", ["quest"]),
     {"kind": "opmode", "mode": "PUBLISH", "counts": [["publishes", 1], ["reads", 2], ["writes", 1]], "note": "Makes 'Old Ghost' visible to players. quests.update with hidden:false (no dedicated toggle exists)."},
     {"kind": "banner", "tone": "warn", "head": "▲ 1 dependency still hidden", "body": "Harvest Boar (AI) has no hidden column; it is reachable once this quest is visible."},
     {"kind": "sheet", "title": "Publish Old Ghost → player-visible", "lines": ["hidden: true → false on KmGPDnZnGOCvATQqA5LI8", "session READY · role MODERATOR · budget 2 of 30", "the record is read back after the send; the PUBLISHED pill appears only when the read-back shows hidden:false"], "action": {"label": "Publish 1 record", "variant": "publish", "state": "disabled"}, "cancel": "Cancel"}]},
   {"name": "aside", "span": "3", "blocks": [health(), {"kind": "kv", "pairs": [["after send", "PUBLISH SENT · UNCONFIRMED until read-back"], ["refusal", "HTTP 200 success:false → 'Write refused' with server message"], ["audit", "actionLog + results bundle + review file"]]}]}]},
 "notes": ["Publish is a whole-record update carrying hidden:false for jutsu/item/bloodline/quest/gameAsset; guides use published; AI has no hidden column (E). The band and the sheet say which.",
           "The Confirm control is disabled for ~600 ms after the sheet appears (arming delay) and until the K-12 level is met; 'Deploy' is never used.",
           "Publication is distinct from technical success: PUBLISH SENT stays unconfirmed until the read-back proves hidden:false (SSC §11)."],
 "pending": ["K-07 which operations are eligible for few-tap publish", "K-12 confirmation level and wording (pending predecessor-transcript reconciliation)", "K-30 late publish visuals", "K-22 gold token"],
 "cites": ["deepdive game-routers-* (hidden flipped only by full-record update mutations)", "D2.3 ConfirmationSurface, ModeBand", "SSC §11; IRM publish rows; CPY §15"]})
# ------------------------------------------------------------ WF-14
S.append({"id": "wf14_quest_studio", "title": "Quest Studio: subtype, storyboard, compile result", "purpose": "One Studio with subtype adapters (RUL-2026-09-12-001). The browser translates and presents; the repository compiles (RUL-2026-09-12-002). Compile is not execution.",
 "flow": "Studio → choose subtype (registry maturity shown) → brief → storyboard → Compile in repository (typed operation; build states are a separate axis from job states) → valid | blocked (decision card) | failed → Promote to manifest run (journaled import into the same preflight, WF-04).",
 "mobile": [brand(), bar("Quest Studio", "Mission · One Perfect Crop", ["draft saved"]),
  {"kind": "tabs", "items": ["Brief", "Storyboard", "Policy", "Compile"], "active": "Storyboard"},
  {"kind": "story", "nodes": [
    {"kind": "dialog", "title": "Arrival at the market", "sub": "Market Clerk · scene market_day"},
    {"kind": "decision", "title": "Help the farmer?", "sub": "2 routes", "pills": ["NEEDS-DECISION"]},
    {"kind": "battle", "title": "Road Bandit ambush", "sub": "AI Road Bandit · profile bandit_c"},
    {"kind": "win", "title": "Deliver the crop", "sub": "rewards: director packet"}]},
  {"kind": "action", "label": "Compile in repository", "variant": "primary", "hint": "GitHub only · zero live-game requests"},
  {"kind": "lamps", "head": "Last build", "items": [{"glyph": "△", "label": "BLOCKED", "value": "decision_required: reward slot C.rank (48 profile)", "tone": "warn", "actions": ["Open decision"]}]},
  pnav("Work")],
 "desktop": {"columns": "220px minmax(420px,2fr) minmax(300px,1fr)", "regions": [
   {"name": "rail", "span": "1", "blocks": [rail("Quest Studio")]},
   {"name": "main", "span": "2", "blocks": [bar("Quest Studio · Mission", "One Perfect Crop · request q_20260912_…", ["draft saved · repo revision 3", "subtype: mission (supported)"]),
     {"kind": "tabs", "items": ["Brief", "Storyboard", "Semantic flow", "Encounters", "Scene & assets", "Policy", "Compile", "Review & package"], "active": "Storyboard"},
     {"kind": "story", "nodes": [
       {"kind": "dialog", "title": "Arrival at the market", "sub": "Market Clerk (reuse) · scene market_day (asset hidden)"},
       {"kind": "decision", "title": "Help the farmer?", "sub": "route A: escort · route B: refuse (ends)", "pills": ["NEEDS-DECISION"]},
       {"kind": "battle", "title": "Road Bandit ambush", "sub": "AI Road Bandit · combat profile from 48 · 1 battle node"},
       {"kind": "win", "title": "Deliver the crop", "sub": "win_quest · rewards from director packet"}]},
     {"kind": "action", "label": "Compile in repository", "variant": "primary", "hint": "typed repository operation; GitHub-only; the build result names the compiler SHA"}]},
   {"name": "aside", "span": "3", "blocks": [{"kind": "lamps", "head": "Build (separate axis from jobs)", "items": [
       {"glyph": "✓", "label": "SAVED", "value": "repository revision 3 · studio/quest/q_…", "tone": "ok"},
       {"glyph": "△", "label": "BLOCKED", "value": "decision_required · reward slot for rank C is AWAITING_RULING in 48", "tone": "warn", "actions": ["Decision card"]},
       {"glyph": "–", "label": "PROMOTE", "value": "available after a valid build · imports into preflight", "tone": "mute"}]},
     {"kind": "kv", "pairs": [["subtypes", "mission supported · event needs_compiler · 4 needs_recipe"], ["shape rules", "projection of mission.py/48, stamped with SHA (no UI rule tables)"], ["worker refusal", "must land as a result, never silence (K-38)"]]}]}]},
 "notes": ["Build states (saved / building / valid / blocked / failed / stale / repository unavailable) are the RB §11 vocabulary and never reuse job-outcome styling (RM-06).",
           "Blocked-by-decision routes to a decision card fed by a structured blocker code from the canonical compiler (K-36/F), not by prose matching.",
           "'Promote' is a journaled import into the same preflight as push/ manifests; no Start control lives in the Studio (K-39).",
           "The foundation implementation at 824c4d58 is evidence for this screen, not its spec: it ends at a text export and has a second shell; absorption into this token set is a roadmap item (RM-02, CF-22)."],
 "pending": ["K-25 Quest Source v2", "K-26 worker trigger (ratify dispatch or revert to source-push)", "K-27 rollout order", "K-46 graph depth", "K-42 flagship confirmation"],
 "cites": ["824c4d58:forge/src/studio/ui.mjs (draft, compile, poll, showExport)", "824c4d58:.github/workflows/quest_studio.yml", "QS §2, §4, §13; RB §6, §11; MS phone model"]})
# ------------------------------------------------------------ WF-15
S.append({"id": "wf15_project_workspace", "title": "Project workspace (read-only projection)", "purpose": "Projects the workstream roadmap.json without a second canonical database: readiness, needs-attention, work plan, launchers. v1 writes nothing (K-28).",
 "flow": "Projects → One Perfect Crop → readiness strip → needs attention → task → launcher (Studio, manifest, admin packet).",
 "mobile": [brand(), bar("One Perfect Crop", "workstream · quest", ["12 tasks"]),
  {"kind": "tiles", "items": [{"label": "complete", "value": "5", "tone": "ok"}, {"label": "ready", "value": "5", "tone": "info"}, {"label": "blocked", "value": "1", "tone": "bad"}, {"label": "planned", "value": "1", "tone": "warn"}]},
  {"kind": "card", "title": "Needs attention", "sub": "derived from roadmap.json", "risk": "recovery", "blocks": [
    {"kind": "row", "title": "art.intake_accepted_assets", "sub": "BLOCKED · accepted art not yet in the repository (manual boundary)", "pills": ["NEEDS-DECISION"]},
    {"kind": "row", "title": "admin.balance_and_eligibility", "sub": "READY · director packet", "pills": ["ADMIN"], "actions": ["Open packet"]}]},
  {"kind": "list", "rows": [
    {"title": "design.structure", "sub": "shared", "pills": ["DONE"]},
    {"title": "content.combat_ai_profiles", "sub": "ChatGPT", "pills": ["DONE"]},
    {"title": "build.final_freeze", "sub": "ChatGPT · after art + admin", "pills": ["PLANNED"]}]},
  pnav("More")],
 "desktop": {"columns": "220px minmax(420px,2fr) minmax(300px,1fr)", "regions": [
   {"name": "rail", "span": "1", "blocks": [rail("Projects")]},
   {"name": "main", "span": "2", "blocks": [bar("One Perfect Crop", "state/workstreams/one_perfect_crop/roadmap.json · rendered 09-12", ["quest", "12 tasks"]),
     {"kind": "tiles", "items": [{"label": "complete", "value": "5", "tone": "ok"}, {"label": "ready", "value": "5", "tone": "info"}, {"label": "blocked", "value": "1", "tone": "bad"}, {"label": "planned", "value": "1", "tone": "warn"}]},
     {"kind": "list", "rows": [
       {"title": "art.intake_accepted_assets", "sub": "BLOCKED · dauntless · accepted Ittetsu / Waystation Keeper / icon not in repository", "pills": ["NEEDS-DECISION"]},
       {"title": "art.scene_characters", "sub": "READY · ChatGPT · Road Bandit production", "pills": ["PLANNED"], "actions": ["Open"]},
       {"title": "admin.balance_and_eligibility", "sub": "READY · dauntless · director packet", "pills": ["ADMIN"], "actions": ["Open packet"]},
       {"title": "build.final_freeze", "sub": "PLANNED · ChatGPT", "pills": ["PLANNED"]}]}]},
   {"name": "aside", "span": "3", "blocks": [{"kind": "kv", "pairs": [["source", "roadmap.json (canonical)"], ["writes", "none in v1 (K-28)"], ["launchers", "Studio draft · manifest 46 · packet"], ["validation", "content_workstream.py validate (repository)"]]}]}]},
 "notes": ["The workspace is a projection plus launchers; any write goes through a typed, validated repository operation (K-28; RB §6).",
           "Task names and states are the roadmap's own; Forge adds no lifecycle vocabulary in v1 (K-44)."],
 "pending": ["K-28 edit scope", "K-40 Studio↔workstream reference", "K-43 project creation", "K-44 vocabulary"],
 "cites": ["state/workstreams/one_perfect_crop/roadmap.json", "scripts/content_workstream.py", "WSP §3-§4 (Tier B)"]})
# ------------------------------------------------------------ WF-16
S.append({"id": "wf16_jobs_settings", "title": "Jobs & Recovery and Settings & diagnostics", "purpose": "History with honest outcome lamps; storage, session, GitHub bridge, release pin and budget as health rows. Maintenance actions keep INCOMPLETE and PAUSED jobs and confirm before deleting finished ones.",
 "flow": "Jobs → resumable first (SENT / ORPHANED / PAUSED / INCOMPLETE), then finished; Settings → health rows with Re-check; Export journal; Delete finished jobs (confirmed).",
 "mobile": [brand(), bar("Jobs & Recovery", "journal", ["2 resumable", "9 finished"]),
  {"kind": "list", "rows": [
    {"title": "46_mission_flatten", "sub": "PAUSED · AMBIGUOUS · 1 SENT", "pills": ["SENT"], "actions": ["Open"]},
    {"title": "16c_forsworn_pack", "sub": "1 ORPHANED to decide", "pills": ["ORPHANED"], "actions": ["Open"]},
    {"title": "24_rank_icon_swap_all31", "sub": "DONE · 31 verified · synced", "pills": ["VERIFIED"]},
    {"title": "02_asset_probe", "sub": "DONE · 4 persisted · 1 not persisted", "pills": ["INCOMPLETE"]}]},
  {"kind": "action", "label": "Delete finished jobs (keeps INCOMPLETE / PAUSED)", "variant": "danger", "hint": "asks once"},
  pnav("Jobs")],
 "desktop": {"columns": "220px minmax(420px,2fr) minmax(300px,1fr)", "regions": [
   {"name": "rail", "span": "1", "blocks": [rail("Settings")]},
   {"name": "main", "span": "2", "blocks": [bar("Settings & diagnostics", "no live poll on this screen"),
     {"kind": "lamps", "head": "Health", "items": [
       {"glyph": "✓", "label": "SESSION", "value": "signed in · probe profile.getAi ok · 2 m ago", "tone": "ok", "actions": ["Re-check · 1 read"]},
       {"glyph": "✓", "label": "STORAGE", "value": "persisted (navigator.storage.persist) · journal v1 · IDB v2", "tone": "ok"},
       {"glyph": "–", "label": "GITHUB", "value": "PAT not configured · results export as text only", "tone": "mute", "actions": ["Configure"]},
       {"glyph": "✓", "label": "RELEASE", "value": "forge 0.4.0 · pin ce603def · main 305a28f", "tone": "ok"},
       {"glyph": "✓", "label": "BUDGET", "value": "sliding window 60/60 s · margin 0.5 · 0 trips", "tone": "ok"}]},
     {"kind": "form", "fields": [["GitHub token (device only; scope per K-15)", "••••••••", ""], ["images (per @img)", "3 picked · 0 missing"]]}]},
   {"name": "aside", "span": "3", "blocks": [{"kind": "kv", "pairs": [["export journal", "text (fail-closed for sensitive keys)"], ["invalidate cache", "per entry, confirmed"], ["delete finished", "confirmed; never INCOMPLETE/PAUSED"]]}]}]},
 "notes": ["'Re-check' is an explicit read that spends one request; Forge never re-probes on its own (CF-12).",
           "Health rows render only for wired data sources; 'Operational' never appears by default (WFA §12; R-16)."],
 "pending": ["K-15 credential model", "K-14 minified bundle (release row)"],
 "cites": ["forge/src/ui/screens.mjs:238-330 (jobs, captures, settings today)", "forge/src/transport/auth.mjs (four states)", "forge/src/storage/journal.mjs (repairHistory, migrate)"]})

spec = {"title": "Forge Next planning wireframes", "intro": "Static planning wireframes (phone 390 x 844 and desktop 1280 x 800) drawn from the approved visual direction, the D2.3 component inventory and the capability evidence. Not production UI. Navigation labels, mode names/colours and lane names are the recommendation's defaults and remain open director decisions (K-20 to K-24); every page lists the decisions it depends on.", "screens": S}
json.dump(spec, open(os.path.join(HERE, "specs.json"), "w"), indent=1)
print("screens:", len(S))
