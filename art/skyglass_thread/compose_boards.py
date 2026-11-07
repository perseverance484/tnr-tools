#!/usr/bin/env python3
"""Compose the salvager's-thread boards: scene backgrounds for Wreck Sighted and At the Salvager's Fire (v2).

    python3 art/skyglass_thread/compose_boards.py       -> art/skyglass_thread/exports/board-*.webp, preview.png

Direction (RUL-2026-11-07-137): every scene is approved Skyglass scene art of the place the salvager is talking about,
with one lacquer panel in the clear zone carrying a serif heading, the real item icons and a few short captions. Nothing
here is generated art; the three new paintings in docs/handoffs/SKYGLASS_ART_PROMPTS.md section 12 replace the bases
marked PLACEHOLDER in BASES when they are approved (one line each).

Frame rules (ENGINE_LAWS 48-51, 79; layout/Logbook.tsx QuestDialogScene): 3:2, delivered at 512 px wide; the salvager
covers the left 40% and the dialog box the bottom third, so every panel sits in x 43-97%, y 3-64%. Boards are authored
at the delivered size so text is drawn once, at final size: headings 18 px, captions at least 12 px.
Fonts: Shippori Mincho and Inter (SIL OFL, font/). Pillow only.
"""
import os

from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ART = os.path.dirname(HERE)
OUT = os.path.join(HERE, "exports")
W, H = 512, 341
PX0, PX1, PY0, PY1 = 222, 498, 10, 216          # the panel zone
CY, IVORY, MUTED = (127, 211, 232), (243, 238, 226), (185, 198, 209)

SC = "ghost_ship_skyglass/scene_bg_ghost_ship_"
BASES = {  # board -> scene art (repo path)
    "menu": SC + "cache_site.webp",            # PLACEHOLDER: TP01 the salvager's camp
    "threes": SC + "deck_b.webp",
    "hulls": SC + "cache_site.webp",           # PLACEHOLDER: TP02 the broken Wreck from above
    "loot": SC + "hold.webp",
    "once": SC + "chart_room.webp",
    "ladder": SC + "lower_hull.webp",
    "pick": SC + "command_observation_gallery.webp",
    "chests": SC + "hold.webp",
    "supplies": SC + "deck_b.webp",
    "craft": SC + "reconstruction_chamber.webp",
    "seals": SC + "quarantined_archive.webp",
    "rot": SC + "reconstruction_chamber.webp",
    "lantern": "crownhold/scenes/exports/scene_bg_crownhold_gate.webp",
    "haul": SC + "hold.webp",
    "shards": SC + "helm.webp",
    "below": "mother_of_echoes/exports/scene_moe_stilling.webp",
    "trade": SC + "cache_site.webp",
    "token": SC + "exterior_keel_walk.webp",
    "logboard": "crownhold/scenes/exports/scene_bg_crownhold_planning_hall.webp",  # PLACEHOLDER: TP03 Information Board
    "orders": "crownhold/scenes/exports/scene_bg_crownhold_planning_hall.webp",    # PLACEHOLDER: TP03
}
EV = "skyglass_event_icons/exports/icon-"
MOE = "mother_of_echoes/exports/icon-shard-"
ICON = {
    "tide": EV + "tide-chart.webp", "roster": EV + "watch-roster.webp", "cache": EV + "chart-buried-cache.webp",
    "foundry": EV + "chart-drowned-foundry.webp", "archive": EV + "chart-quarantined-archive.webp",
    "watch": EV + "chart-captains-watch.webp", "seal": EV + "reliquary-seal.webp", "rseal": EV + "rotted-reliquary-seal.webp",
    "heading": EV + "the-last-heading.webp", "rot": EV + "core-rot.webp", "ledger": EV + "ledger-page.webp",
    "manifest": EV + "stores-manifest.webp", "token": EV + "skyglass-token.webp", "coffer": EV + "skyglass-coffer.webp",
    "stores": EV + "galley-stores.webp", "hoard": EV + "crowns-hoard.webp", "chest": EV + "rare-hunters-chest.webp",
    "katana": "ghost_ship_skyglass/icon_ghost_ship_skyglass_katana.webp", "keel": MOE + "keel.webp",
    "crown": MOE + "crown.webp", "tideshard": MOE + "tide.webp", "ledgershard": MOE + "ledger.webp",
    "log": "skyglass_journal/exports/icon-quest-watch-log.webp",
    "treasury": EV + "sealed-treasury.webp", "cargo": EV + "unmarked-cargo.webp", "pouch": EV + "tool-pouch-katon.webp",
    "jar": EV + "little-horrors-jar.webp", "filament": "ghost_ship_skyglass/icon_ghost_ship_skyglass_filament.webp",
    "crystal": "ghost_ship_skyglass/icon_ghost_ship_skyglass_crystal.webp",
    "fragment": "ghost_ship_skyglass/icon_ghost_ship_skyglass_crown_fragment.webp",
    "skycrown": "ghost_ship_skyglass/icon_ghost_ship_skyglass_crown.webp",
}


def F(name, size):
    return ImageFont.truetype(os.path.join(HERE, "font", f"{name}.ttf"), size)


def base(key):
    return Image.open(os.path.join(ART, BASES[key])).convert("RGB").resize((W, H), Image.LANCZOS).convert("RGBA")


class Board:
    def __init__(self, key):
        self.im = base(key)
        self.d = ImageDraw.Draw(self.im)

    def panel(self, x0=PX0, y0=PY0, x1=PX1, y1=PY1, title=None):
        sh = Image.new("RGBA", self.im.size, (0, 0, 0, 0))
        ImageDraw.Draw(sh).rounded_rectangle([x0 + 2, y0 + 4, x1 + 2, y1 + 4], 7, fill=(0, 0, 0, 150))
        self.im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(5)))
        layer = Image.new("RGBA", self.im.size, (0, 0, 0, 0))
        d = ImageDraw.Draw(layer)
        d.rounded_rectangle([x0, y0, x1, y1], 7, fill=(9, 14, 21, 225), outline=CY + (170,), width=1)
        d.rounded_rectangle([x0 + 3, y0 + 3, x1 - 3, y1 - 3], 5, outline=CY + (55,), width=1)
        for cx, cy in ((x0, y0), (x1, y0), (x0, y1), (x1, y1)):
            d.polygon([(cx, cy - 3), (cx + 3, cy), (cx, cy + 3), (cx - 3, cy)], fill=CY + (230,))
        self.im.alpha_composite(layer)
        self.d = ImageDraw.Draw(self.im)
        self.mx = (x0 + x1) // 2
        if title:
            self.d.text((self.mx, y0 + 9), title, font=F("ShipporiMincho-800", 18), fill=IVORY, anchor="mt")
            self.d.line([(x0 + 40, y0 + 33), (x1 - 40, y0 + 33)], fill=CY + (110,), width=1)
        return self

    def text(self, x, y, s, size=12, color=IVORY, font="Inter-700", anchor="mt"):
        self.d.text((x, y), s, font=F(font, size), fill=color, anchor=anchor)

    def big(self, x, y, s, size=40):
        self.d.text((x, y), s, font=F("ShipporiMincho-800", size), fill=IVORY, anchor="mt")

    def chip(self, key, x, y, size, cap=None, capsize=12):
        ic = Image.open(os.path.join(ART, ICON[key])).convert("RGBA").resize((size, size), Image.LANCZOS)
        shadow = Image.new("RGBA", (size, size), (0, 0, 0, 255))
        shadow.putalpha(ic.split()[3].point(lambda v: 160 if v > 20 else 0))
        g = Image.new("RGBA", (size + 16, size + 16), (0, 0, 0, 0))
        g.alpha_composite(shadow, (8, 11))
        self.im.alpha_composite(g.filter(ImageFilter.GaussianBlur(3)), (x - 8, y - 8))
        self.im.alpha_composite(ic, (x, y))
        if cap:
            self.text(x + size // 2, y + size + 3, cap, capsize)

    def row(self, keys, y, size, caps=None, gap=None, capsize=12):
        n = len(keys)
        gap = gap if gap is not None else 10
        total = n * size + (n - 1) * gap
        x = self.mx - total // 2
        for i, k in enumerate(keys):
            self.chip(k, x + i * (size + gap), y, size, caps[i] if caps else None, capsize)

    def arrow(self, x0, y, x1):
        self.d.line([(x0, y), (x1 - 2, y)], fill=CY, width=2)
        self.d.polygon([(x1 + 3, y), (x1 - 3, y - 4), (x1 - 3, y + 4)], fill=CY)

    def chevron(self, x, y):
        self.d.line([(x - 5, y - 2), (x, y + 3), (x + 5, y - 2)], fill=CY, width=2)

    def stars(self, cx, y, n=5, r=5):
        import math
        for i in range(n):
            x = cx + (i - (n - 1) / 2) * (2 * r + 4)
            pts = [(x + (r if k % 2 == 0 else r * 0.45) * math.sin(k * math.pi / 5),
                    y + r - (r if k % 2 == 0 else r * 0.45) * math.cos(k * math.pi / 5)) for k in range(10)]
            self.d.polygon(pts, fill=CY)


# --- the boards (captions: one or two words, 12 px or larger) ---------------------------------------------------------
def b_menu(b):
    b.panel(title="Ask the salvager")
    b.row(["log", "tide", "seal", "ledger"], 46, 38, ["ABOARD", "CHARTS", "DEEP", "HAUL"], gap=24)
    b.row(["crown", "token", "log"], 126, 38, ["SHARDS", "TRADE", "THE LOG"], gap=28)


def b_threes(b):
    b.panel(y1=170, title="Go in threes")
    b.big(b.mx, 44, "3", 54)
    b.text(b.mx, 110, "PLAYERS, EXACTLY", 13)
    b.text(b.mx, 132, "THE WRECK  ·  SECTOR 210", 12, MUTED, "Inter-600")


def b_hulls(b):
    b.panel(y1=180, title="She broke in two")
    b.text(b.mx, 50, "THE FADED WRECK", 14)
    b.text(b.mx, 70, "levels 40 to 60  ·  16/6", 12, MUTED, "Inter-600")
    b.d.line([(b.mx - 60, 98), (b.mx + 60, 98)], fill=CY + (90,), width=1)
    b.text(b.mx, 112, "THE SKYGLASS WRECK", 14)
    b.text(b.mx, 132, "level 100  ·  15/6", 12, MUTED, "Inter-600")


def b_loot(b):
    b.panel(y1=190, title="What comes back")
    b.row(["tide", "roster", "cache", "stores"], 52, 44, gap=12)
    b.text(b.mx, 112, "CHARTS AND STORES", 13)
    b.text(b.mx, 134, "ryo and EXP every clear", 12, MUTED, "Inter-600")


def b_once(b):
    b.panel(y1=196, title="Good once")
    b.chip("tide", b.mx - 92, 46, 54, "CHART")
    b.arrow(b.mx - 26, 72, b.mx + 4)
    b.text(b.mx + 54, 56, "BATTLE", 14)
    b.text(b.mx + 54, 74, "ARENA", 14)
    b.text(b.mx + 54, 96, "solo", 12, MUTED, "Inter-600")
    b.text(b.mx, 136, "SPENT AT THE START", 12)
    b.text(b.mx, 156, "a loss ends the run", 12, MUTED, "Inter-600")


def b_ladder(b):
    b.panel(title="Down through her decks")
    for name, keys, y in (("LOW TIDE", ["tide", "roster"], 44), ("THE CREW", ["cache", "foundry", "archive", "watch"], 100),
                          ("THE DEEP", ["seal", "heading"], 156)):
        b.text(PX0 + 70, y + 20, name, 12, MUTED, anchor="rm")
        for i, k in enumerate(keys):
            b.chip(k, PX0 + 80 + i * 48, y, 40)
    b.chevron(PX0 + 124, 92)
    b.chevron(PX0 + 124, 148)


def b_pick(b):
    b.panel(y1=196, title="Win, then choose")
    b.row(["coffer", "token", "stores"], 46, 52, gap=18)
    b.text(b.mx, 112, "PICK ONE", 14)
    b.stars(b.mx, 140)
    b.text(b.mx, 160, "every chart shows its stars", 12, MUTED, "Inter-600")


def b_chests(b):
    b.panel(y1=164, title="What the crates hold")
    b.row(["coffer", "treasury", "hoard", "cargo"], 48, 48, ["COFFER", "TREASURY", "HOARD", "CARGO"], gap=16)
    b.text(b.mx, 128, "glass \u00b7 ryo and metals \u00b7 both \u00b7 anything", 12, MUTED, "Inter-600")


def b_supplies(b):
    b.panel(y1=196, title="The crew's supplies")
    b.row(["pouch", "stores", "jar"], 46, 52, ["KUNAI", "PET EXP", "THE PET"], gap=26)
    b.text(b.mx, 130, "pills, potions, kunai", 12, MUTED, "Inter-600")
    b.text(b.mx, 150, "and a pet of your own", 12, MUTED, "Inter-600")


def b_craft(b):
    b.panel(y1=206, title="Working the glass")
    for y, a, n, c, cap in ((44, "filament", "12", "crystal", "CRYSTAL"), (110, "fragment", "5", "skycrown", "CROWN")):
        b.chip(a, PX0 + 54, y, 44)
        b.text(PX0 + 108, y + 15, f"\u00d7{n}", 14, anchor="lt")
        b.arrow(PX0 + 140, y + 22, PX0 + 168)
        b.chip(c, PX0 + 178, y, 44, cap)
    b.text(b.mx, 182, "needs a crafting rank", 12, MUTED, "Inter-600")


def b_seals(b):
    b.panel(y1=196, title="What the crew sealed")
    b.chip("seal", b.mx - 92, 48, 66, "RELIQUARY")
    b.chip("heading", b.mx + 26, 48, 66, "THE FALL")
    b.text(b.mx, 150, "the Epic runs", 12, MUTED, "Inter-600")


def b_rot(b):
    b.panel(y1=196, title="Steeped in rot")
    b.chip("seal", PX0 + 18, 50, 50)
    b.text(PX0 + 80, 68, "+", 18)
    for i in range(3):
        b.chip("rot", PX0 + 92 + i * 30, 58, 32)
    b.arrow(PX0 + 186, 75, PX0 + 204)
    b.chip("rseal", PX0 + 212, 50, 50)
    b.text(b.mx, 118, "WIN ONE FIGHT", 13)
    b.text(b.mx, 140, "tainted runs: pick two", 12, MUTED, "Inter-600")


def b_lantern(b):
    b.panel(y1=150, title="Follow the lantern")
    b.text(b.mx, 50, "LASTLIGHT LANTERN", 14)
    b.chevron(b.mx, 78)
    b.text(b.mx, 92, "CROWNHOLD", 14)
    b.text(b.mx, 116, "the castle she sailed from", 12, MUTED, "Inter-600")


def b_haul(b):
    b.panel(y1=200, title="The Haul")
    b.row(["ledger", "manifest"], 44, 46, gap=14)
    b.text(b.mx, 104, "CRATE · LOCKER · CUT · LEAVE", 12)
    b.text(b.mx, 124, "up to five steps", 12, MUTED, "Inter-600")
    b.chip("chest", b.mx - 20, 144, 40)


def b_shards(b):
    b.panel(y1=196, title="Four shards, one glass")
    b.row(["keel", "crown", "tideshard", "ledgershard"], 48, 52, ["KEEL", "CROWN", "TIDE", "LEDGER"], gap=14)
    b.text(b.mx, 136, "Wreck · Crownhold · deep · Haul", 12, MUTED, "Inter-600")


def b_below(b):
    b.panel(y1=184, title="Below Crownhold")
    b.row(["keel", "crown", "tideshard", "ledgershard"], 48, 40, gap=14)
    b.chevron(b.mx, 102)
    b.big(b.mx, 110, "?", 26)
    b.text(b.mx, 148, "alone · all four spent", 12, MUTED, "Inter-600")


def b_trade(b):
    b.panel(y1=196, title="Every chart has a buyer")
    b.row(["tide", "rot", "crown", "token"], 48, 46, gap=14)
    b.text(b.mx, 112, "CHARTS, ROT, SHARDS, TOKENS", 12)
    b.text(b.mx, 134, "Crown's Hoard stays with you", 12, MUTED, "Inter-600")


def b_token(b):
    b.panel(y1=184, title="Skyglass Tokens")
    b.chip("token", b.mx - 92, 46, 60, "TOKEN")
    b.arrow(b.mx - 22, 76, b.mx + 4)
    b.chip("katana", b.mx + 32, 46, 60, "12 SKINS")
    b.text(b.mx, 140, "on a weapon you own", 12, MUTED, "Inter-600")


def b_logboard(b):
    b.panel(y1=196, title="The watch log")
    b.chip("log", b.mx - 32, 44, 64)
    b.text(b.mx, 118, "INFORMATION BOARD", 13)
    b.text(b.mx, 138, "a new page each weekend", 12, MUTED, "Inter-600")
    b.text(b.mx, 158, "take it first", 12, MUTED, "Inter-600")


def b_orders(b):
    b.panel(y1=196, title="This weekend's orders")
    b.chip("log", PX0 + 20, 48, 58)
    for i, s in enumerate(["any order", "claim in your Logbook", "finish all for more"]):
        b.text(PX0 + 94, 54 + i * 20, s, 12, IVORY, "Inter-600", anchor="lt")
    b.text(b.mx, 140, "CLOSES TUESDAY 00:00 UTC", 12)
    b.text(b.mx, 160, "Monday 6 PM Central", 12, MUTED, "Inter-600")


BOARDS = {
    "menu": b_menu, "threes": b_threes, "hulls": b_hulls, "loot": b_loot, "once": b_once, "ladder": b_ladder,
    "pick": b_pick, "chests": b_chests, "supplies": b_supplies, "craft": b_craft, "seals": b_seals, "rot": b_rot, "lantern": b_lantern, "haul": b_haul, "shards": b_shards,
    "below": b_below, "trade": b_trade, "token": b_token, "logboard": b_logboard, "orders": b_orders,
}


def main():
    os.makedirs(OUT, exist_ok=True)
    cols = 3
    sheet = Image.new("RGB", (cols * (W + 4) + 4, ((len(BOARDS) + cols - 1) // cols) * (H + 4) + 4), (11, 15, 20))
    for i, (key, fn) in enumerate(BOARDS.items()):
        b = Board(key)
        fn(b)
        path = os.path.join(OUT, f"board-{key}.webp")
        b.im.convert("RGB").save(path, "WEBP", quality=90, method=6)
        r, c = divmod(i, cols)
        sheet.paste(b.im.convert("RGB"), (4 + c * (W + 4), 4 + r * (H + 4)))
        print(f"art/skyglass_thread/exports/board-{key}.webp: {os.path.getsize(path)} bytes")
    sheet.save(os.path.join(HERE, "preview.png"))


if __name__ == "__main__":
    main()
