# Icon overhaul: director scores and player feedback

Started 2026-10-23, after the revert (push/227). The director scores each of the 51 reverted icons and records player feedback;
this log feeds the one-at-a-time premium rework. Cards: `review/NN_<slug>.png` (built by `make_cards.py` from `queue.json`;
originals and ours downloaded to `src/`). Scores and feedback are the director's; nothing here is a decision by Claude Code.

| # | Jutsu | Family | Score | Player feedback |
|---|---|---|---|---|
| 1 | Abyss of Shadows | Event | 8/10 | Circular shape and red/black scheme make it hard to tell apart from BEE icons (Ring of Spilled Blood, Hemocure); visual register overlaps too much |
| 2 | Blazing Fang Strike | Event | 10/10 | No notes; well liked |
| 3 | Celestial Dew | Event | 10/10 | No notes; well liked |
| 4 | Drops of Renewal | Event | 6/10 | Too realistic: the drop reads as plain water, not restorative energy; does not read well as a skill icon |
| 5 | Earthen Bastion | Event | 4/10 | Does not read well as a skill icon; too busy and noisy |
| 6 | Hollow Veil | Event | 9/10 | Very good; maybe a small silhouette upgrade |
| 7 | Subaku Palace | Event | 6/10 | Good enough rendering, but does not read clearly as a skill icon |
| 8 | Tempest Cleave | Event | 0/10 | Total fail, do not reuse at all. Reads as a shuriken skill, not Tempest Cleave; not intimidating enough; wrong shape and art direction. Inspiration: an older version, a blue-white slicing whirlwind with lightning and cloud curls (`refs/08_tempest_cleave_older_version.png`, director's screenshot) |
| 9 | Ethereal Nexus | Forbidden | 3/10 | Decent quality, but looks like a Shakunetsu Sakura skill (pink/magenta) and does not reflect the ability |
| 10 | Ethereal Rebirth | Forbidden | 0/10 | Players really disliked it. Reads as a poisonous energy explosion, not an ethereal rebirth; bad direction and quality. Direction: swirling restorative energy |
| 11 | Poisonous Senbon | Normal | 5/10 | Decent idea, but the art style does not read as TNR premium pixel art |
| 12 | Replacement Technique | Normal | 3/10 | Good image on its own, but players missed the old one, which captured the skill better. Direction: try working the two together |
| 13 | Searing Might | Normal | 2/10 | Too literal with the shield; art does not read as TNR premium pixel art |
| 14 | Soul Shackles | Normal | 4/10 | Decent, but the shackles go nowhere and stop midair. Direction: chains spread straight across the icon |
| 15 | Venomous Phobia. | Normal | 7/10 | Pretty good; needs a better silhouette, that's it |
| 16 | Crimson Impact | Blood-Enchanted Eyes | 8/10 | Needs silhouette refinement |
| 17 | Crimson Tithe | Blood-Enchanted Eyes | 10/10 | No notes |
| 18 | Hemocure | Blood-Enchanted Eyes | 10/10 | No notes |
| 19 | Reaper's Embrace | Blood-Enchanted Eyes | 10/10 | No notes |
| 20 | Ring of Spilled Blood | Blood-Enchanted Eyes | 10/10 | No notes |
| 21 | Sanguine Plague | Blood-Enchanted Eyes | 10/10 | No notes |
| 22 | Thousand Strike | Blood-Enchanted Eyes | 10/10 | No notes |
| 23 | Unholy Enhancement | Blood-Enchanted Eyes | 10/10 | No notes |
| 24 | Blast Shield | Bakuhatsu | 6/10 | Pretty good, but reads as a generic shield with a recolor. Direction: show the actual blast/shockwave, and the ring of earth the jutsu kicks up around the user as a physical barrier |
| 25 | Charge 4 Explosion | Bakuhatsu | 4/10 | Unique and creative (the blasts spell C4), but not high quality or premium |
| 26 | Howitzer Crash | Bakuhatsu | 6/10 | Decent execution, but lacks real pop or skill identity |
| 27 | Inferno Cataclysm | Bakuhatsu | 6/10 | Visuals do not look premium; reads as a lava skill rather than an explosion skill |
| 28 | Kinetic Nova | Bakuhatsu | 9/10 | Pretty good; maybe a little polish |
| 29 | Atomic Shield | Aerathiel | 1/10 | Not premium pixel art; wrong color scheme for Aerathiel; loses most of the teal and the particle-barrier look of the original for a generic bubble |
| 30 | Death's March | Aerathiel | 1/10 | Same art-style problem as the other Aerathiel icons; too similar to Windshear Decay and Atomic Shield |
| 31 | Decaying Touch | Aerathiel | 1/10 | Same art-style problem as the other Aerathiel icons; the hand looks unnatural |
| 32 | Particle Cannon | Aerathiel | 4/10 | Decent execution, but needs an art-style improvement |
| 33 | Windshear Decay | Aerathiel | 1/10 | Same Aerathiel art-style problem; resembles Death's March and Atomic Shield too much |
| 34 | Azure Dragon Palm | Vaporia | 6/10 | Needs more premium art |
| 35 | Drowning Strike | Vaporia | 6/10 | Needs more premium art |
| 36 | Liquid Ember Shell | Vaporia | 8/10 | May just need updating to the same art style as the other Vaporia icons once they are reworked |
| 37 | Scorch Break | Vaporia | 6/10 | Needs more premium art |
| 38 | Surfing Strike | Vaporia | 6/10 | Needs more premium art; resembles Azure Dragon Palm too much at thumbnail size |
| 39 | Crystal Cave | Crystal Essence | 10/10 | No notes |
| 40 | Crystal Sphere | Crystal Essence | 10/10 | No notes |
| 41 | Kōsai Shippū | Crystal Essence | 10/10 | No notes |
| 42 | Prism | Crystal Essence | 10/10 | No notes |
| 43 | Summoning: Jade | Crystal Essence | 10/10 | No notes |
| 44 | Arctic Frost | Blue Blade Eyes | 8/10 | Good, but the background is too noisy and makes the skill hard to make out (shared flaw across all Blue Blade Eyes icons) |
| 45 | Blade Resonance | Blue Blade Eyes | 8/10 | Good, but the background is too noisy and makes the skill hard to make out (shared flaw across all Blue Blade Eyes icons) |
| 46 | Blue Crimson | Blue Blade Eyes | 8/10 | Good, but the background is too noisy and makes the skill hard to make out (shared flaw across all Blue Blade Eyes icons) |
| 47 | Glacial Volley | Blue Blade Eyes | 8/10 | Good, but the background is too noisy and makes the skill hard to make out (shared flaw across all Blue Blade Eyes icons) |
| 48 | Ice Shackles | Blue Blade Eyes | 8/10 | Good, but the background is too noisy and makes the skill hard to make out (shared flaw across all Blue Blade Eyes icons) |
| 49 | Icebound Might | Blue Blade Eyes | 8/10 | Good, but the background is too noisy and makes the skill hard to make out (shared flaw across all Blue Blade Eyes icons); the original's looming Susano'o-like ice summon reads better than our zoomed-in ice sculpture, which is hard to make out |
| 50 | Quintessential Flake | Blue Blade Eyes | 8/10 | Good, but the background is too noisy and makes the skill hard to make out (shared flaw across all Blue Blade Eyes icons) |
| 51 | Sapphire Command | Blue Blade Eyes | 8/10 | Good, but the background is too noisy and makes the skill hard to make out (shared flaw across all Blue Blade Eyes icons) |

## Summary (review complete, 2026-10-23)

Family averages: Crystal Essence 10.0, Blood-Enchanted Eyes 9.8, Blue Blade Eyes 8.0, Event 6.6, Vaporia 6.4, Bakuhatsu 6.2,
Normal 4.2, Aerathiel 1.6, Forbidden 1.5.

| Band | Count | Jutsu |
|---|---|---|
| 10/10 | 14 | Blazing Fang Strike, Celestial Dew, Crimson Tithe, Hemocure, Reaper's Embrace, Ring of Spilled Blood, Sanguine Plague, Thousand Strike, Unholy Enhancement, Crystal Cave, Crystal Sphere, Kōsai Shippū, Prism, Summoning: Jade |
| 5-9 | 24 | Abyss of Shadows, Drops of Renewal, Hollow Veil, Subaku Palace, Poisonous Senbon, Venomous Phobia., Crimson Impact, Blast Shield, Howitzer Crash, Inferno Cataclysm, Kinetic Nova, the five Vaporia, the eight Blue Blade Eyes |
| 0-4 | 13 | Earthen Bastion, Tempest Cleave, Ethereal Nexus, Ethereal Rebirth, Replacement Technique, Searing Might, Soul Shackles, Charge 4 Explosion, all five Aerathiel |

Recurring feedback (Claude Code's reading of the notes above; the notes themselves are the record):
1. **Premium pixel art**: the most common complaint (Poisonous Senbon, Searing Might, Charge 4 Explosion, Inferno Cataclysm, all Aerathiel, four Vaporia).
2. **Reads as a skill icon**: busy, noisy or scenic images fail (Earthen Bastion, Subaku Palace, Drops of Renewal; the Blue Blade Eyes backgrounds).
3. **Distinct within its family and against other families**: Aerathiel's three wind swirls, Surfing Strike vs Azure Dragon Palm, Abyss of Shadows vs BEE, Ethereal Nexus vs Shakunetsu Sakura, Tempest Cleave reading as shuriken.
4. **Skill identity over a generic shape**: generic shield/bubble/explosion loses what the jutsu does (Blast Shield, Atomic Shield, Howitzer Crash, Ethereal Rebirth).
5. **Family palette**: Aerathiel's teal particle look was lost.
6. **Keep what players loved in the original**: Replacement Technique, Icebound Might's looming summon, Tempest Cleave's older whirlwind.
