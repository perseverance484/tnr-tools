#!/usr/bin/env python3
"""Delivery copies of the Skyglass boss strips (boss_fx.py, 2026-10-28) in the AN-set asset convention (push/376,
exports/an_v1.json), for the ship of the boss set pieces (push/470+).

    python3 art/skyglass_boss_fx/deliver_boss.py

Reads exports/anim_<id>_v1.webp (50 px frames, 50 ms each; the strips previewed in boss_reel.mp4) and writes
exports/anim_<id>_v1_x3d.webp plus exports/boss_v1_x3d.json. Two mechanical changes, nothing redrawn:
  * x3: each 50 px frame enlarged x3 by nearest neighbour to 150 px (animate_an.py DELIVER_SCALE; the art spec's
    ANIMATION target needs a 112 px minimum frame width, and the CDN's ?width=50 rendition is an exact 3:1 reduction).
  * d: the reel's 130-alpha fade pixels become an ordered dither of full-alpha pixels (animate_an.py dither(), 4x4
    Bayer at 130/255, frame-local), as the AN set does, so the strips pass the spec's soft-edge ceiling
    (25x_DATA_art_spec.json house_style.measured_signature.soft_edge_share_max). Alpha is then 0 or 255 only.
Fresh filenames (law 32): no *_x3d name was ever uploaded. anim_maw_v1_x3.webp (push/379, the Little Maw, undithered
full-size maw) is a different file and is not reused here: Maw of the Deep is arena-wide and takes the field variant.
"""
import json
import os

import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
EXPORTS = os.path.join(HERE, 'exports')
N, SCALE, MS, MAX_BYTES = 50, 3, 50, 460800
BAYER = np.array([[0, 8, 2, 10], [12, 4, 14, 6], [3, 11, 1, 9], [15, 7, 13, 5]]) / 16 + 1 / 32

# strip id -> (use, design id / move it was drawn for; SKYGLASS_ART_AUDIT.md H2, RUL-2026-10-30-061 item 10,
#              RUL-2026-10-28-028 item 6)
STRIPS = {
    'ships_bell': ('appear', "cp_bell_toll: Ship's Bell damage hit"),
    'broadside_field': ('appear', 'cp_broadside: Broadside damage hit (arena field variant, 24 hexes)'),
    'command_absolute_field': ('appear', 'cc_command_absolute: Command Absolute damage hit (arena field variant)'),
    'crownfall': ('appear', 'cc_crownfall: Crownfall damage hit'),
    'maw_field': ('appear', 'ch_maw: Maw of the Deep damage hit (arena field variant)'),
    'quench': ('appear', 'fw_quench: Quench damage hit'),
    'exposed': ('static', 'the shared burst window (ch_exposed, fw_cracked, Lowered Guard): weakness SELF loop'),
    'recall': ('appear', 'cc_recall: Recall and Stonebound Summons summon flourish'),
    'crown_aura': ('static', "cc_crown_aura: The Crown's Will aura loop (portrait kept clear)"),
    'crimson_strike': ('appear', 'Final Command damage hit'),
    'chain_wrap': ('appear', 'Keelbind, Chain Hook (Mould Cage) and the violet Binding blast (Binding: Seal Cross)'),
}


def deliver(src):
    s = np.array(Image.open(src).convert('RGBA'))
    h, w = s.shape[:2]
    assert w == N and h % N == 0, (src, w, h)
    levels = set(np.unique(s[..., 3]).tolist())
    assert levels <= {0, 130, 255}, (src, levels)
    m = np.tile(BAYER, (N // 4 + 1, N // 4 + 1))[:N, :N]
    m = np.tile(m, (h // N, 1))  # frame-local pattern
    a = s[..., 3].copy()
    s[..., 3] = np.where(a == 130, np.where(m < 130 / 255, 255, 0), a)
    im = Image.fromarray(s)
    return im.resize((w * SCALE, h * SCALE), Image.NEAREST), h // N, int((a == 130).sum())


def main():
    rows = []
    for sid, (use, note) in STRIPS.items():
        src = os.path.join(EXPORTS, f'anim_{sid}_v1.webp')
        out, frames, dithered = deliver(src)
        p = os.path.join(EXPORTS, f'anim_{sid}_v1_x3d.webp')
        out.save(p, lossless=True, quality=100, method=6)
        size = os.path.getsize(p)
        assert size < MAX_BYTES, (p, size)
        rows.append({'id': sid, 'file': f'art/skyglass_boss_fx/exports/anim_{sid}_v1_x3d.webp',
                     'source': f'art/skyglass_boss_fx/exports/anim_{sid}_v1.webp', 'type': 'ANIMATION',
                     'frames': frames, 'speed': MS, 'speed_unit': 'ms per frame (gameAsset.speed)',
                     'duration_ms': frames * MS, 'frame_px': N * SCALE, 'drawn_grid_px': N, 'bytes': size,
                     'dithered_px': dithered, 'use': use, 'note': note})
        print(f'{sid}: {frames} frames, {size} bytes, {dithered} fade px dithered')
    meta = {'source': 'art/skyglass_boss_fx/boss_fx.py strips (2026-10-28; boss_reel.mp4)',
            'builder': 'art/skyglass_boss_fx/deliver_boss.py',
            'layout': 'vertical strip, one square frame per row',
            'speed_note': 'gameAsset.speed is ms per frame (as exports/an_v1.json)',
            'use_values': 'appear = effect appearAnimation (plays once); static = staticAnimation loop',
            'assets': rows}
    with open(os.path.join(EXPORTS, 'boss_v1_x3d.json'), 'w') as f:
        json.dump(meta, f, indent=1)
        f.write('\n')


if __name__ == '__main__':
    main()
