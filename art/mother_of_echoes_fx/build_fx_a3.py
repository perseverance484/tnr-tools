#!/usr/bin/env python3
"""The Mother of Echoes art3 set: the material arc (director, 2026-11-05).

    python3 art/mother_of_echoes_fx/build_fx_a3.py

"When she starts out it's Skyglass, crystal, reflections and light. Then she gets corrupted by the Silence and it
becomes black corrupted shadow moves." Materials are measured from the two approved variants:
- Act I (light) = HEARTGLASS: faceted cyan panes in gunmetal frames with spiked finials, white facet lines, mirror
  glints (#5bc6e7 / #49a4c8, highlights #c8f7fc / #9ad0e3, frame #232231 / #3e3c54, steel #5b6786).
- Act II (the turn) = Heartglass panes with the Remainder's black cracks and smoke creeping in.
- Act III and the Silence (corrupted) = THE REMAINDER: black obsidian glass, smoke inside, thorned shards, glowing
  teal-cyan crack veins with a lit edge, bone-white cord (#080a0f / #12171e / #27323c, veins #2f5c6a lit #92b6bf).
Danger grammar is kept (SKYGLASS_BOSS_ANIMATIONS.md): heavy keeps its shape (a cracked faceted ring on the floor, shards
bursting up) and a constant EMBER outer rim and ember shard edge in every act (director: keep the rim); control keeps
its ring of links (violet), linger keeps the bile seep, safe keeps the cyan four-point star in a diamond.
Engine (docs/design/COMBAT_ANIMATION_ENGINE.md, theninjarpg@3314d122): 50 px rendition + linear stretch, so solid
2-3 px clusters and 1 px dark outlines on the 50 px grid; hard alpha (appears overdraw 2-3x); 1 px clear margin;
<= 80 frames. Mosaic pieces (visual COORDINATES tags) are the same burst with leading delay frames per band, so one
cast rolls out as a wave. Writes exports/*_a3.webp and exports/moe_fx_a3.json. Pillow only.
"""
import importlib.util
import json
import math
import os

from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
_s = importlib.util.spec_from_file_location("build_fx", os.path.join(HERE, "build_fx.py"))
F = importlib.util.module_from_spec(_s)
_s.loader.exec_module(F)
N, BEAT, ROOT = F.N, F.BEAT, F.ROOT
EMB, EMB_Y, SCORE, WHITE = F.EMBER_RED, F.EMBER_YEL, F.SCORE, F.WHITE

PAL = {
    "I": dict(deep=(16, 16, 26), body=(73, 164, 200), lite=(91, 198, 231), hot=(200, 247, 252), vein=(200, 247, 252),
              seam=(35, 34, 49), frame=(62, 60, 84), steel=(91, 103, 134), glint=(154, 208, 227)),
    "II": dict(deep=(14, 16, 22), body=(73, 164, 200), lite=(154, 208, 227), hot=(200, 247, 252), vein=(8, 10, 15),
               seam=(35, 34, 49), frame=(35, 34, 49), steel=(91, 103, 134), glint=(222, 184, 104), smoke=(39, 50, 60)),
    "III": dict(deep=(8, 10, 15), body=(18, 23, 30), lite=(39, 50, 60), hot=(146, 182, 191), vein=(96, 214, 236),
                seam=(8, 10, 15), frame=(20, 42, 51), steel=(107, 118, 129), glint=(235, 236, 235), smoke=(39, 50, 60)),
}
VEIN_LIT = (200, 250, 255)
BONE = (235, 236, 235)
BONE_S = (170, 172, 176)
BONE_D = (44, 46, 54)


def poly10(r, rot=18):
    return [(25 + r * math.cos(math.radians(k * 36 + rot)), 25 + r * math.sin(math.radians(k * 36 + rot))) for k in range(10)]


# ------------------------------------------------------------------------------------------------ heavy mark per act
def tile_heavy(act):
    p = PAL[act]
    t = F.frame()
    d = ImageDraw.Draw(t)
    d.polygon(poly10(24.8), fill=(*EMB, 255))                      # the constant hot accent: the ember rim
    d.polygon(poly10(23.2), fill=(*SCORE, 255))
    d.polygon(poly10(22.2), fill=(*p["body"], 255))
    d.polygon(poly10(20.2), fill=(*p["lite"], 255))
    d.polygon(poly10(18.6), fill=(*p["body"], 255))
    d.polygon(poly10(17), fill=(*SCORE, 255))
    d.polygon(poly10(16), fill=(*p["deep"], 255))
    if act in ("I", "II"):                                         # Heartglass frame bars and spiked finials
        for k in range(10):
            g = math.radians(k * 36 + 18)
            d.line([(25 + 16 * math.cos(g), 25 + 16 * math.sin(g)), (25 + 24 * math.cos(g), 25 + 24 * math.sin(g))],
                   fill=(*p["frame"], 255), width=2)
            F.blob(t, 25 + 23.6 * math.cos(g), 25 + 23.6 * math.sin(g), p["steel"], r=1)
    if act in ("II", "III"):                                       # smoke inside the glass
        for k in range(3):
            for u in range(14):
                a = math.radians(k * 120 + u * 18)
                r = 5 + u * 0.75
                F.px(t, 25 + r * math.cos(a), 25 + r * math.sin(a), p["smoke"])
    if act == "III":                                               # thorns on the rim
        for k in range(10):
            g = math.radians(k * 36)
            d.polygon([(25 + 22 * math.cos(g - 0.08), 25 + 22 * math.sin(g - 0.08)), (25 + 25.5 * math.cos(g), 25 + 25.5 * math.sin(g)),
                       (25 + 22 * math.cos(g + 0.08), 25 + 22 * math.sin(g + 0.08))], fill=(*p["lite"], 255))
    for k in (5, 6):
        g = math.radians(k * 36 + 36)
        F.blob(t, 25 + 21 * math.cos(g), 25 + 21 * math.sin(g), WHITE if act == "I" else p["glint"] if act == "III" else p["hot"])
    for a, wob in ((30, 16), (128, 13), (212, 17), (300, 14)):
        pts = F.jag(25, 25, 4.5, 17, a, wob, steps=5)
        if act == "I":
            d.line(pts, fill=(*p["lite"], 255), width=2)
            d.line(pts[1:4], fill=(*WHITE, 255), width=1)
        elif act == "II":                                          # black cracks creeping into the light
            d.line(pts, fill=(*p["lite"], 255), width=2)
            d.line(pts[:4], fill=(*p["vein"], 255), width=1)
        else:                                                      # glowing teal veins with a lit edge
            d.line(pts, fill=(*p["vein"], 255), width=2)
            d.line(pts[1:4], fill=(*VEIN_LIT, 255), width=1)
    d.ellipse([20, 20, 30, 30], fill=(*SCORE, 255))
    d.ellipse([21.5, 21.5, 28.5, 28.5], fill=(*EMB, 255))
    d.ellipse([23, 23, 27, 27], fill=(*(p["hot"] if act != "III" else VEIN_LIT), 255))
    return F.tile_out(t)


def glint_heavy(act):
    """Heavy loop at the ring's ends (portrait-clear), on the 0.8 s beat: ember flare plus the act's light (I: white
    mirror glints; II: a black crack ticks in; III: a teal vein pulses)."""
    p = PAL[act]
    fr = []
    for i in range(BEAT):
        f = F.frame()
        pu = F.pulse(i)
        for side in (-1, 1):
            for k in range(7):
                a = math.radians((180 if side < 0 else 0) + (k - 3) * 9)
                x, y = F.GC[0] + (F.GRX - 1) * math.cos(a), F.GC[1] + (F.GRY - 0.5) * math.sin(a)
                F.blob(f, x, y, EMB_Y if pu > 0.6 else EMB)
                F.px(f, x, y + 1.5, F.EMBER_D)
            x0 = F.GC[0] + side * (F.GRX - 4)
            if act == "I" and pu > 0.75:
                for s in range(1, 3):
                    for dx, dy in ((s, 0), (-s, 0), (0, s), (0, -s)):
                        F.px(f, x0 + dx, F.GC[1] - 4 + dy, WHITE)
            elif act == "II":
                L = int(2 + 4 * pu)
                F.seg(f, (x0, F.GC[1] - 2), (x0 + side * L, F.GC[1] + 1), p["vein"])
            elif act == "III":
                F.blob(f, x0, F.GC[1] - 3, VEIN_LIT if pu > 0.6 else p["vein"])
        fr.append(f)
    return F.mind_portrait(fr)


def appear_heavy(act):
    """Heavy mark arrives: a white (I), cracked (II) or teal (III) ring slams down wider than the hex and contracts
    onto the rim with its ember edge, then sparks kick off it. 10 frames."""
    p = PAL[act]
    ring = {"I": WHITE, "II": p["hot"], "III": VEIN_LIT}[act]
    fr = []
    sparks = [(k * 45 + 20, 1.0 + 0.3 * (k % 3)) for k in range(8)]
    for i in range(10):
        f = F.frame()
        if i <= 3:
            s = {0: 1.35, 1: 1.18, 2: 1.05, 3: 1.0}[i]
            F.ground_ring(f, (F.GRX - 1) * s, (F.GRY - 0.5) * s, [(0, ring), (1, EMB_Y), (-1, ring), (2, EMB)])
            if act == "II" and i >= 2:
                for a in (40, 160, 290):
                    g = math.radians(a)
                    F.seg(f, (25 + (F.GRX - 1) * math.cos(g), 25 + (F.GRY - .5) * math.sin(g)),
                          (25 + (F.GRX - 6) * math.cos(g + 0.2), 25 + (F.GRY - 3) * math.sin(g + 0.2)), p["vein"])
        if 3 <= i <= 9:
            t = i - 2
            for k, (a, sp) in enumerate(sparks):
                if t > 5 and k % 2:
                    continue
                g = math.radians(a)
                x0, y0 = 25 + (F.GRX - 1) * math.cos(g), 25 + (F.GRY - 0.5) * math.sin(g)
                n = F.frame()
                F.blob(n, x0 + math.cos(g) * t * 0.9, y0 - sp * t * 2.4 + 0.45 * t * t,
                       (ring if t < 2 else EMB_Y if t < 4 else EMB))
                F.outline_alpha(n, SCORE)
                f.alpha_composite(n)
        fr.append(f)
    return fr


# ------------------------------------------------------------------------------------------------ shards and bursts
def shard(f, cx, base, h, w, tilt, act, hot=False):
    """One act-material glass shard, point up, with the constant ember edge on its right face."""
    p = PAL[act]
    n = F.frame()
    d = ImageDraw.Draw(n)
    tip = (cx + tilt * h, base - h)
    mid = (cx + tilt * h * 0.5, base - h * 0.15)
    if act == "III":                                               # thorned: a notch on the left face
        d.polygon([(cx - w / 2, base), (cx - w * 0.75, base - h * 0.45), tip, mid], fill=(*p["lite"], 255))
    else:
        d.polygon([(cx - w / 2, base), tip, mid], fill=(*(WHITE if hot else p["lite"]), 255))
    d.polygon([mid, tip, (cx + w / 2, base)], fill=(*(p["lite"] if hot and act == "I" else p["body"]), 255))
    if act == "I":
        d.line([(cx - w / 2, base), tip], fill=(*WHITE, 255))
    elif act == "II":
        d.line([(cx - w * 0.1, base - 1), (tip[0] - 0.5, tip[1] + h * 0.35)], fill=(*p["vein"], 255))
        F.px(n, cx + w * 0.1, base - h * 0.3, p["smoke"])
    else:
        d.line([(cx - w * 0.15, base - 1), (tip[0], tip[1] + h * 0.25)], fill=(*p["vein"], 255))
        d.line([(cx - w / 2, base), (cx - w * 0.75, base - h * 0.45), tip], fill=(*VEIN_LIT, 255))   # lit edge
    d.line([tip, (cx + w / 2, base)], fill=(*EMB_Y, 255))           # the ember edge
    F.outline_alpha(n, SCORE)
    f.alpha_composite(n)


def chunks(f, cx, cy, t, act, n=10, sp=2.6, drop=4):
    p = PAL[act]
    for k in range(n):
        if drop and t > drop and k % 2:
            continue
        a = math.radians(-160 + k * (140 / max(1, n - 1)))
        s = sp * (0.8 + 0.25 * (k % 3))
        x, y = cx + math.cos(a) * s * t * 1.4, cy + math.sin(a) * s * t + 0.38 * t * t
        m = F.frame()
        col = (p["lite"] if k % 3 == 0 else EMB_Y if (k % 3 == 1 and t < 3) else p["body"]) if act != "III" else \
              (VEIN_LIT if k % 3 == 0 and t < 3 else p["lite"])
        F.blob(m, x, y, col, r=2 if (t < 3 and k % 2 == 0) else 1)
        F.outline_alpha(m, SCORE)
        f.alpha_composite(m)


def burst(act, scale=1.0, wide=False):
    """The heavy eruption in the act's material: anticipation (the rim heats), a white or teal impact frame, a burst of
    glass shards with the ember edge (I prismatic glints; II black smoke seeping up the shards; III a void bloom
    behind thorned black shards), chunks rain and the scorch settles. 14 frames."""
    p = PAL[act]
    fr = []
    spread = 1.35 if wide else 1.0
    for i in range(14):
        f = F.frame()
        if i <= 2:
            F.ground_ring(f, F.GRX - 1, F.GRY - 0.5, [(0, EMB_Y if i == 2 else EMB), (1, SCORE)])
            if act != "I":
                F.ground_ring(f, F.GRX - 5, F.GRY - 2.5, [(0, p["vein"])])
        if i == 3:
            n = F.frame()
            dd = ImageDraw.Draw(n)
            dd.ellipse([25 - 19, 25 - 9.5, 25 + 19, 25 + 9.5], fill=(*(WHITE if act == "I" else p["hot"] if act == "II" else VEIN_LIT), 255))
            dd.ellipse([25 - 12, 25 - 6, 25 + 12, 25 + 6], fill=(*(WHITE if act != "III" else (16, 10, 30)), 255))
            F.outline_alpha(n, EMB)
            f.alpha_composite(n)
        if 3 <= i <= 8:
            g = {3: 0.45, 4: 0.85, 5: 1.0, 6: 1.0, 7: 0.8, 8: 0.5}[i] * scale
            if act == "III" and 4 <= i <= 7:                        # void bloom behind the shards
                n = F.frame()
                ImageDraw.Draw(n).ellipse([25 - 11, 9, 25 + 11, 27], fill=(16, 8, 30, 255))
                F.outline_alpha(n, p["vein"])
                f.alpha_composite(n)
            for dx, h, w, tilt in ((-11, 11, 5, -0.35), (11, 12, 5, 0.35), (-6, 18, 6, -0.15), (6, 17, 6, 0.15), (0, 25, 7, 0.0)):
                shard(f, 25 + dx * spread, 28, h * g, w, tilt, act, hot=(i in (4, 5) and act == "I"))
            if act == "I" and i in (4, 5, 6):                       # prismatic glints off the facets
                for x, y, c in ((15, 10, (255, 170, 170)), (35, 9, (170, 255, 210)), (25, 3, (190, 180, 255)), (9, 18, WHITE)):
                    F.blob(f, x, y, c)
            if act == "II" and i >= 5:                              # the Remainder's smoke creeping up the shards
                for x in (19, 25, 31):
                    for k in range(int(6 * g)):
                        F.blob(f, x + (k % 2), 27 - k * 1.6, p["smoke"] if k % 2 else p["vein"], r=1)
        if i >= 6:
            chunks(f, 25, 14, i - 5, act, n=10 if not wide else 12, sp=2.6 * (1.2 if wide else 1.0))
        if i >= 9:
            F.ground_ring(f, F.GRX - 2, F.GRY - 1, [(0, F.EMBER_D if act != "III" else p["vein"])])
        fr.append(f)
    return fr


def pane_fall(act):
    """Glassfall pane (Act III): a thorned black pane with teal veins falls point-first over its growing shadow, the
    impact flashes teal-white with the ember rim, and the act-III burst follows. 15 frames."""
    p = PAL[act]
    fr = []
    tail = burst(act)
    for i in range(4):
        f = F.frame()
        r = 4 + i * 2.5
        ImageDraw.Draw(f).ellipse([25 - r * 1.4, 26 - r * 0.45, 25 + r * 1.4, 26 + r * 0.45], fill=(*p["deep"], 255))
        n = F.frame()
        d = ImageDraw.Draw(n)
        tip_y = -6 + i * 10.5
        top = tip_y - 26
        d.polygon([(18, top), (25, top), (25, tip_y)], fill=(*p["lite"], 255))
        d.polygon([(25, top), (32, top), (25, tip_y)], fill=(*p["body"], 255))
        d.line([(21, top + 3), (24, tip_y - 6)], fill=(*p["vein"], 255))
        d.line([(18, top), (25, tip_y)], fill=(*VEIN_LIT, 255))
        F.outline_alpha(n, SCORE)
        f.alpha_composite(n)
        fr.append(f)
    return fr + tail[3:]


def delayed(frames, lead):
    """A mosaic piece: the same clip with `lead` leading empty frames, so bands of hexes fire in a wave."""
    return [F.frame() for _ in range(lead)] + list(frames)


# ------------------------------------------------------------------------------------------------ Act II recast
def recast_a3():
    """Recast (Act II payoff): the etched lattice flashes back gold, Heartglass blades rise along it, then the
    Remainder's black cracks race up the blades and they shatter into dark-flecked shards. 13 frames."""
    p = PAL["II"]
    sites = [((25, 26), 18, 5)] + [((round(F.lerp(F.C, e, 0.55)[0]), round(F.lerp(F.C, e, 0.55)[1]) + 1), 11 if k in F.SIDE else 8, 3)
                                   for k, e in F.ENDS.items()]
    fr = []
    for i in range(13):
        f = F.frame()
        lat = F.frame()
        if i <= 1:
            F.etch_lines(lat, F.ENDS, F.C, widths=(3, 2, 1), cols=[(F.ETCH_DARK, F.ETCH_HOT, WHITE), (F.ETCH_DARK, WHITE, WHITE)])
        elif i <= 7:
            F.etch_lines(lat, F.ENDS, F.C, widths=(3, 2, 1))
        f.alpha_composite(F.clip(lat, F.poly_mask(F.HEX)))
        rise = {1: 0.3, 2: 0.65, 3: 0.95, 4: 1.0, 5: 1.0, 6: 0.95}
        if i in rise:
            for (bx, by), h, w in sorted(sites, key=lambda s: s[0][1]):
                shard(f, bx, by, h * rise[i], w + 1, 0, "II", hot=(i == 4))
                if i >= 5:                                         # black cracks race up the blade
                    F.seg(f, (bx, by - 1), (bx + 0.5, by - h * rise[i] * (0.4 + 0.2 * (i - 4))), p["vein"])
        if i >= 7:
            chunks(f, 25, 16, i - 6, "II", n=11, sp=2.4)
        fr.append(f)
    return fr


# ------------------------------------------------------------------------------------------------ dark control and linger
def tile_control_dark():
    """Control/lock in the Silence's material: a ring of obsidian links with violet lit edges round an ink ground, the
    closed eye with a teal vein. Same silhouette as the light control tile (a ring of links)."""
    t = F.frame()
    d = ImageDraw.Draw(t)
    d.ellipse([0.5, 0.5, 49.5, 49.5], fill=(*F.INK, 255))
    d.ellipse([12, 12, 38, 38], fill=(*F.VIOLET_D, 255))
    n = 14
    for k in range(n):
        g = math.radians(k * 360 / n)
        cx, cy = 25 + 19.2 * math.cos(g), 25 + 19.2 * math.sin(g)
        tang = g + math.pi / 2
        ux, uy, vx, vy = math.cos(tang), math.sin(tang), math.cos(g), math.sin(g)
        L, W = (4.6, 3.2) if k % 2 == 0 else (4.6, 2.0)
        c = [(cx + ux * L + vx * W, cy + uy * L + vy * W), (cx - ux * L + vx * W, cy - uy * L + vy * W),
             (cx - ux * L - vx * W, cy - uy * L - vy * W), (cx + ux * L - vx * W, cy + uy * L - vy * W)]
        d.polygon(c, fill=(*F.VIOLET_M, 255), outline=(*F.VIOLET_L, 255))
        inner = [(cx + (x - cx) * 0.5, cy + (y - cy) * 0.5) for x, y in c]
        d.polygon(inner, fill=(*(F.INK if k % 2 == 0 else PAL["III"]["body"]), 255))
    d.polygon([(13, 25), (19, 19), (31, 19), (37, 25), (31, 31), (19, 31)], fill=(*PAL["III"]["body"], 255), outline=(*F.VIOLET_L, 255))
    d.line([(14, 25), (36, 25)], fill=(*PAL["III"]["vein"], 255), width=3)
    d.line([(17, 25), (33, 25)], fill=(*VEIN_LIT, 255), width=1)
    for x in (18, 22, 26, 30, 33):
        d.line([(x, 27), (x - 1, 30)], fill=(*F.VIOLET_L, 255), width=1)
    return F.tile_out(F.clip(t, F.disc_mask(25, 25, 24.8)))


def tile_linger_dark():
    """Lingering pool in the corrupted material: bile seeping through crazed black glass, teal-lit crack web."""
    t = F.frame()
    d = ImageDraw.Draw(t)
    lumps = [(25, 25, 15), (14, 18, 8), (36, 17, 8), (39, 31, 8), (13, 33, 8), (25, 39, 8), (25, 10, 7), (8, 25, 6), (42, 24, 6)]
    for x, y, r in lumps:
        d.ellipse([x - r - 1.5, y - r - 1.5, x + r + 1.5, y + r + 1.5], fill=(*F.BILE_DEEP, 255))
    for x, y, r in lumps:
        d.ellipse([x - r, y - r, x + r, y + r], fill=(*PAL["III"]["body"], 255))
    for x, y, r in lumps[:6]:
        d.ellipse([x - r * 0.6, y - r * 0.6, x + r * 0.6, y + r * 0.6], fill=(96, 124, 26, 255))
    for a in (20, 80, 140, 200, 260, 320):
        pts = F.jag(25, 25, 2, 21, a, 13, steps=6)
        d.line(pts, fill=(*F.BILE, 255), width=2)
        d.line(pts[2:5], fill=(*PAL["III"]["vein"], 255), width=1)
    for x, y in ((17, 18), (33, 15), (37, 32), (17, 34), (26, 26), (9, 24), (41, 22), (25, 40)):
        F.blob(t, x, y, F.BILE_HOT)
    return F.tile_out(F.clip(t, F.disc_mask(25, 25, 24.5)))


# ------------------------------------------------------------------------------------------------ summons: rise out of the glass
def rise(kind):
    """Summon entrance (frames the avatar, never draws a second figure): the floor glass cracks open in the summon's
    material, a column of light or smoke rises around the portrait's sides and bone-white cords (the Remainder's
    cord) whip up and fall away. kind: 'feeler' (the Silence: ink + bone), 'likeness' (silvered Heartglass),
    'worn' (ash + Act II cracks). 15 frames."""
    (pcx, pcy), pr = F.AI_DISC
    body = {"feeler": (14, 10, 24), "likeness": PAL["I"]["lite"], "worn": F.ASH}[kind]
    edge = {"feeler": PAL["III"]["vein"], "likeness": WHITE, "worn": F.ASH_L}[kind]
    fr = []
    for i in range(15):
        f = F.frame()
        if i <= 5:                                                 # the floor cracks open
            r = 4 + i * 3
            F.ground_ring(f, r, r * 0.33, [(0, edge), (1, body), (2, SCORE)], cy=37)
            for a in (200, 250, 300, 340, 20):
                g = math.radians(a)
                F.seg(f, (25, 37), (25 + r * math.cos(g), 37 + r * 0.33 * math.sin(g)), body)
        if 2 <= i <= 11:                                           # columns rising at the portrait's sides
            h = min(1.0, (i - 1) / 4) * 26 if i <= 8 else 26 * (11 - i) / 3
            for side in (-1, 1):
                x = pcx + side * (pr + 2.5)
                for s in range(int(h)):
                    y = 37 - s
                    F.px(f, x, y, edge if s % 6 == 0 else body)
                    F.px(f, x + side, y, body)
                F.blob(f, x, 37 - h, edge)
        if 4 <= i <= 12:                                           # bone cords whip up and fall away
            t = i - 4
            for side, ph in ((-1, 0.0), (1, 1.4)):
                pts = []
                for s in range(18):
                    u = s / 17
                    y = 38 - u * min(30, 6 + t * 5) + (max(0, t - 5) ** 2) * 0.6 * u
                    x = pcx + side * (pr + 5 + 3 * math.sin(u * 5 + ph + t * 0.7))
                    pts.append((x, y))
                n = F.frame()
                for x, y in pts:
                    F.px(n, x, y, BONE)
                    F.px(n, x + 1, y, BONE_S)
                F.outline_alpha(n, BONE_D)
                f.alpha_composite(n)
        if i == 6:
            F.blob(f, pcx, 37, WHITE if kind == "likeness" else edge, r=2)
        fr.append(f)
    mask = Image.new("L", (N, N), 0)
    ImageDraw.Draw(mask).ellipse([pcx - pr + 2, pcy - pr + 2, pcx + pr - 2, pcy + pr - 2], fill=255)
    out = []
    for f in fr:
        a = f.getchannel("A")
        a.paste(0, (0, 0), mask)
        f.putalpha(a)
        out.append(f)
    return out


# ------------------------------------------------------------------------------------------------ boss auras and flourishes
def aura(which):
    """Boss aura loop (16 frames, 0.8 s beat), portrait-clear, aimed high (AI portrait centre ~0.4 h above the hex).
    'sayo1' prismatic Heartglass facets orbiting; 'silence' ink tendrils with teal veins; 'sayo2' a gold etch ring
    with the Remainder's black cracks creeping in; 'saint' black thorned shards and shadow tendrils with lit veins."""
    (pcx, pcy), pr = F.AI_DISC
    fr = []
    for i in range(BEAT):
        f = F.frame()
        ph = 2 * math.pi * i / BEAT
        pu = F.pulse(i)
        if which == "sayo1":
            for k in range(6):
                a = ph + k * math.pi / 3
                x, y = pcx + (pr + 4) * math.cos(a), pcy + (pr + 4) * math.sin(a) * 0.9
                n = F.frame()
                d = ImageDraw.Draw(n)
                d.polygon([(x, y - 3), (x + 2, y), (x, y + 3), (x - 2, y)], fill=(*PAL["I"]["lite"], 255))
                d.line([(x, y - 3), (x, y + 3)], fill=(*WHITE, 255))
                F.outline_alpha(n, PAL["I"]["seam"])
                f.alpha_composite(n)
            for k, c in enumerate(((255, 170, 170), (170, 255, 210), (190, 180, 255))):
                a = ph * 1.5 + k * 2.1
                F.blob(f, pcx + (pr + 7.5) * math.cos(a), pcy + (pr + 7.5) * math.sin(a) * 0.9, c)
        elif which == "sayo2":
            F.thick_arc(f, pcx, pcy, pr + 2, 0, 360, [(0, SCORE), (1, F.ETCH_MID if pu < 0.7 else F.ETCH_HOT), (2, SCORE)])
            for k in range(6):
                a = math.radians(k * 60 + 20)
                L = 3 + 5 * pu
                x0, y0 = pcx + (pr + 2) * math.cos(a), pcy + (pr + 2) * math.sin(a)
                F.blob(f, x0 + L * math.cos(a + 0.4), y0 + L * math.sin(a + 0.4), PAL["II"]["vein"], r=1)
                F.seg(f, (x0, y0), (x0 + L * math.cos(a + 0.4), y0 + L * math.sin(a + 0.4)), PAL["II"]["vein"])
                if k % 2 == 0:
                    F.blob(f, x0 + (L + 2) * math.cos(a + 0.6), y0 + (L + 2) * math.sin(a + 0.6), PAL["II"]["smoke"], r=1)
        else:
            vein = PAL["III"]["vein"]
            for k in range(4 if which == "saint" else 5):
                a0 = k * math.pi / 2 + ph * 0.5 + (0.3 if which == "silence" else 0)
                for s in range(12):
                    u = s / 11
                    r = pr + 1 + u * 8
                    a = a0 + u * 1.2 + 0.25 * math.sin(ph + u * 4)
                    x, y = pcx + r * math.cos(a), pcy + r * math.sin(a) * 0.95
                    F.blob(f, x, y, (14, 10, 24) if s < 8 else (VEIN_LIT if pu > 0.6 else vein), r=2 if s < 5 else 1)
                    if s < 8:
                        F.px(f, x, y - 1, vein)
            if which == "saint":
                for k in range(3):
                    a = -ph + k * 2.1
                    x, y = pcx + (pr + 5) * math.cos(a), pcy + (pr + 5) * math.sin(a)
                    n = F.frame()
                    d = ImageDraw.Draw(n)
                    d.polygon([(x, y - 4), (x + 2.5, y + 2), (x - 2.5, y + 2)], fill=(20, 20, 30, 255))
                    d.line([(x, y - 3), (x, y + 1)], fill=(*VEIN_LIT, 255))
                    F.outline_alpha(n, VEIN_LIT if pu > 0.6 else vein)
                    f.alpha_composite(n)
        fr.append(f)
    mask = Image.new("L", (N, N), 0)
    ImageDraw.Draw(mask).ellipse([pcx - pr, pcy - pr, pcx + pr, pcy + pr], fill=255)
    out = []
    for f in fr:
        a = f.getchannel("A")
        a.paste(0, (0, 0), mask)
        f.putalpha(a)
        out.append(f)
    return out


def flourish(which):
    """Act-start flourish (the aura buff's appear, once): the boss's material bursts outward from behind the portrait
    and settles into the aura. 14 frames."""
    (pcx, pcy), pr = F.AI_DISC
    col = {"sayo1": PAL["I"]["lite"], "sayo2": F.ETCH_HOT, "silence": (14, 10, 24), "saint": (20, 20, 30)}[which]
    edge = {"sayo1": WHITE, "sayo2": PAL["II"]["vein"], "silence": PAL["III"]["vein"], "saint": VEIN_LIT}[which]
    fr = []
    for i in range(14):
        f = F.frame()
        if i <= 7:
            r = pr + 1 + i * 2.2
            F.thick_arc(f, pcx, pcy, r, 0, 360, [(0, edge), (1, col), (2, col if i < 5 else SCORE)])
        if 2 <= i <= 12:
            t = i - 2
            for k in range(10):
                if t > 6 and k % 2:
                    continue
                a = math.radians(k * 36 + 10)
                rr = pr + 3 + t * 2.4
                n = F.frame()
                ImageDraw.Draw(n).polygon([(pcx + rr * math.cos(a), pcy + rr * math.sin(a) - 3),
                                           (pcx + rr * math.cos(a) + 2, pcy + rr * math.sin(a) + 2),
                                           (pcx + rr * math.cos(a) - 2, pcy + rr * math.sin(a) + 2)], fill=(*col, 255))
                F.outline_alpha(n, edge)
                f.alpha_composite(n)
        fr.append(f)
    mask = Image.new("L", (N, N), 0)
    ImageDraw.Draw(mask).ellipse([pcx - pr, pcy - pr, pcx + pr, pcy + pr], fill=255)
    out = []
    for f in fr:
        a = f.getchannel("A")
        a.paste(0, (0, 0), mask)
        f.putalpha(a)
        out.append(f)
    return out


# ------------------------------------------------------------------------------------------------ dialog portraits
SCENE_SRC = {  # SCENE_CHARACTER crops of the approved avatars (director: Sayo only; her act forms)
    "scene_moe_sayo_a3.webp": "art/mother_of_echoes/exports/avatar_moe_sayo_v2.webp",
    "scene_moe_sayo_stilling_a3.webp": "art/mother_of_echoes/exports/avatar_moe_sayo_stilling.webp",
    "scene_moe_saint_a3.webp": "art/mother_of_echoes/exports/avatar_moe_saint.webp",
}


def scene_character(src):
    """2:3 portrait (341 x 512 display; the Logbook draws it bottom-aligned at 2/5 width, object-contain): the
    figure's alpha bbox, padded to 2:3 around its centre, resized to fit 512 tall, hard alpha."""
    im = Image.open(os.path.join(ROOT, src)).convert("RGBA")
    a = im.getchannel("A").point(lambda v: 255 if v >= 128 else 0)
    im.putalpha(a)
    im = im.crop(a.getbbox())
    w, h = im.size
    H = max(h, int(math.ceil(w * 1.5)))
    W = int(round(H / 1.5))
    c = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    c.paste(im, ((W - w) // 2, H - h))                            # bottom-aligned like the Logbook
    c = c.resize((341, 512), Image.LANCZOS)
    c.putalpha(c.getchannel("A").point(lambda v: 255 if v >= 128 else 0))
    return F.fill_under(c)


ACTS = ("I", "II", "III")
WAVE_LEAD = 3          # frames between mosaic bands (150 ms)


def assets():
    """(file, frames list or image, kind, note)"""
    out = []
    for act in ACTS:
        out.append((f"tile_moe_heavy_{act.lower()}_a3.webp", tile_heavy(act), "STATIC", f"Heavy mark, Act {act} material, ember rim"))
        out.append((f"anim_moe_heavy_glint_{act.lower()}_a3.webp", glint_heavy(act), "ANIMATION", f"Heavy mark loop, Act {act}"))
        out.append((f"anim_moe_heavy_appear_{act.lower()}_a3.webp", appear_heavy(act), "ANIMATION", f"Heavy mark arrives, Act {act}"))
    out.append(("tile_moe_control_dark_a3.webp", tile_control_dark(), "STATIC", "Control/lock mark, the Silence's material"))
    out.append(("tile_moe_linger_dark_a3.webp", tile_linger_dark(), "STATIC", "Lingering pool, corrupted material"))
    out.append(("anim_moe_refraction_a3.webp", burst("I"), "ANIMATION", "Refraction Breaks (Act I): Heartglass shards, prismatic glints, ember edge"))
    out.append(("anim_moe_recast_a3.webp", recast_a3(), "ANIMATION", "Recast (Act II): etched lattice, Heartglass blades, black cracks race up and shatter"))
    for k in range(4):
        out.append((f"anim_moe_enrage_w{k}_a3.webp", delayed(burst("III", wide=True), k * WAVE_LEAD), "ANIMATION", f"The Glass Remembers mosaic band {k} (lead {k * WAVE_LEAD})"))
    for k in range(5):
        out.append((f"anim_moe_shatterfall_w{k}_a3.webp", delayed(burst("III", scale=1.2, wide=True), k * WAVE_LEAD), "ANIMATION", f"Shatterfall Gives Way mosaic band {k}"))
    for k in range(3):
        out.append((f"anim_moe_glassfall_w{k}_a3.webp", delayed(pane_fall("III"), k * WAVE_LEAD), "ANIMATION", f"Glassfall pane mosaic band {k}"))
    flood = F.build_flood_mask()
    for k in range(4):
        out.append((f"anim_moe_flood_w{k}_a3.webp", delayed(flood, k * WAVE_LEAD), "ANIMATION", f"The Names Flood In mosaic band {k}"))
    for kind in ("feeler", "likeness", "worn"):
        out.append((f"anim_moe_rise_{kind}_a3.webp", rise(kind), "ANIMATION", f"Summon entrance ({kind}): rises out of the glass"))
    for which in ("sayo1", "silence", "sayo2", "saint"):
        out.append((f"anim_moe_aura_{which}_a3.webp", aura(which), "ANIMATION", f"Boss aura loop ({which})"))
        out.append((f"anim_moe_flourish_{which}_a3.webp", flourish(which), "ANIMATION", f"Act-start flourish ({which})"))
    return out


def export():
    rows = []
    for name, obj, kind, note in assets():
        p = os.path.join(F.EXPORTS, name)
        if kind == "STATIC":
            img, frames = obj, 1
        else:
            assert len(obj) <= 80, (name, len(obj))
            img, frames = F.strip(obj), len(obj)
        img.save(p, lossless=True, quality=100, method=6)
        size = os.path.getsize(p)
        assert size < F.MAX_BYTES, (name, size)
        rows.append({"file": f"art/mother_of_echoes_fx/exports/{name}", "type": kind, "frames": frames,
                     "speed": F.MS if kind == "ANIMATION" else None, "bytes": size, "note": note})
    sc = []
    for name, src in SCENE_SRC.items():
        p = os.path.join(ROOT, "art", "mother_of_echoes", "exports", name)
        scene_character(src).save(p, lossless=True, quality=100, method=6)
        sc.append({"file": f"art/mother_of_echoes/exports/{name}", "type": "SCENE_CHARACTER", "source": src,
                   "bytes": os.path.getsize(p)})
    with open(os.path.join(F.EXPORTS, "moe_fx_a3.json"), "w") as fh:
        json.dump({"source": "art/mother_of_echoes_fx/build_fx_a3.py", "assets": rows, "scene_characters": sc}, fh, indent=1)
        fh.write("\n")
    print(f"{len(rows)} FX + {len(sc)} scene characters")


if __name__ == "__main__":
    export()
