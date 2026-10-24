# Icon overhaul: batch plan

RUL-2026-10-23-008: everything ships in one batch. Nothing here is built yet.

## Restore unchanged (15)

The image is our earlier upload (`live_image_ours` in `state/jutsu_icon_revert/revert_2026-10-23.json`), sent with `injectableInBattle` at its live value (law 20).

| # | Jutsu | Family | Our image |
|---|---|---|---|
| 2 | Blazing Fang Strike | Event | https://ui0arpl8sm.ufs.sh/f/i7JYNmkFS4Q3zPMWH5l3w.webp |
| 3 | Celestial Dew | Event | https://ui0arpl8sm.ufs.sh/f/G-wjyAHTeK9vk6lnjUxRw.webp |
| 16 | Crimson Impact | Blood-Enchanted Eyes | https://ui0arpl8sm.ufs.sh/f/MQQ6Eov3AcXB1YImyEjmF.webp |
| 17 | Crimson Tithe | Blood-Enchanted Eyes | https://ui0arpl8sm.ufs.sh/f/g2SCTEz0Q1fPKM8KQjqz4.webp |
| 18 | Hemocure | Blood-Enchanted Eyes | https://ui0arpl8sm.ufs.sh/f/h1PiVus0VgjKb7KCJyPAy.webp |
| 19 | Reaper's Embrace | Blood-Enchanted Eyes | https://ui0arpl8sm.ufs.sh/f/b0UhHFlBfP-vdyBIX-d6i.webp |
| 20 | Ring of Spilled Blood | Blood-Enchanted Eyes | https://ui0arpl8sm.ufs.sh/f/vEOTwBTH7jkUZl3Mle6Se.webp |
| 21 | Sanguine Plague | Blood-Enchanted Eyes | https://ui0arpl8sm.ufs.sh/f/PUXg9NkuF6NANTNI-aElz.webp |
| 22 | Thousand Strike | Blood-Enchanted Eyes | https://ui0arpl8sm.ufs.sh/f/VUQo8X4xzF1fDp58wdakX.webp |
| 23 | Unholy Enhancement | Blood-Enchanted Eyes | https://ui0arpl8sm.ufs.sh/f/ejsOYmbnGHe9-xiRQobMw.webp |
| 39 | Crystal Cave | Crystal Essence | https://ui0arpl8sm.ufs.sh/f/QsMAIVjSkaEW6kuxu5R4M.webp |
| 40 | Crystal Sphere | Crystal Essence | https://ui0arpl8sm.ufs.sh/f/WoJbgO6RQTuUi-_HqQdoH.webp |
| 41 | Kōsai Shippū | Crystal Essence | https://ui0arpl8sm.ufs.sh/f/Lba0VnegJiA6J6SE0xRLw.webp |
| 42 | Prism | Crystal Essence | https://ui0arpl8sm.ufs.sh/f/jRiw0n1-GSuNPSq-HiSdj.webp |
| 43 | Summoning: Jade | Crystal Essence | https://ui0arpl8sm.ufs.sh/f/qqeUYO60QH-hVidW2xSPT.webp |

**AI links (law 18):** Prism is equipped by Mermaid Jade and " Jade" (push/228 capture), so the batch unequips it before the edit and re-equips it after (law 60), as push/229 did. Re-check every AI kit against the whole batch before building it.

## Rework (36)

Art direction for all 36: `docs/handoffs/ICON_OVERHAUL_ART_DIRECTION.md` (from `ICON_SCORES.md` and `STAFF_FEEDBACK.md`).

| # | Jutsu | Family | Status |
|---|---|---|---|
| 1 | Abyss of Shadows | Event |
| 4 | Drops of Renewal | Event |
| 5 | Earthen Bastion | Event |
| 6 | Hollow Veil | Event |
| 7 | Subaku Palace | Event |
| 8 | Tempest Cleave | Event | **pilot** (worked first): `tempest_cleave/PILOT.md` |
| 9 | Ethereal Nexus | Forbidden |
| 10 | Ethereal Rebirth | Forbidden |
| 11 | Poisonous Senbon | Normal |
| 12 | Replacement Technique | Normal | round 1 briefed: `docs/handoffs/REPLACEMENT_TECHNIQUE_REWORK_SESSION_PROMPT.md` |
| 13 | Searing Might | Normal |
| 14 | Soul Shackles | Normal |
| 15 | Venomous Phobia. | Normal |
| 24 | Blast Shield | Bakuhatsu |
| 25 | Charge 4 Explosion | Bakuhatsu |
| 26 | Howitzer Crash | Bakuhatsu |
| 27 | Inferno Cataclysm | Bakuhatsu |
| 28 | Kinetic Nova | Bakuhatsu |
| 29 | Atomic Shield | Aerathiel |
| 30 | Death's March | Aerathiel |
| 31 | Decaying Touch | Aerathiel |
| 32 | Particle Cannon | Aerathiel |
| 33 | Windshear Decay | Aerathiel |
| 34 | Azure Dragon Palm | Vaporia |
| 35 | Drowning Strike | Vaporia |
| 36 | Liquid Ember Shell | Vaporia |
| 37 | Scorch Break | Vaporia |
| 38 | Surfing Strike | Vaporia |
| 44 | Arctic Frost | Blue Blade Eyes |
| 45 | Blade Resonance | Blue Blade Eyes |
| 46 | Blue Crimson | Blue Blade Eyes |
| 47 | Glacial Volley | Blue Blade Eyes |
| 48 | Ice Shackles | Blue Blade Eyes |
| 49 | Icebound Might | Blue Blade Eyes |
| 50 | Quintessential Flake | Blue Blade Eyes |
| 51 | Sapphire Command | Blue Blade Eyes |
