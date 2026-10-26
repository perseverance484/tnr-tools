import json, hashlib, os
from PIL import Image
REPO=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))+"/"
def meta(path):
    b=open(REPO+path,"rb").read(); w,h=Image.open(REPO+path).size
    return len(b), w, h, hashlib.sha256(b).hexdigest()
SHA="60b792ac19ba710d724a247127eb0482d967eeaf"
# Ghost Ship art bible blocks (docs/design/ghost_ship_art_bible/blocks.json, RUL-2026-10-26-002): pasted verbatim.
BLK=json.load(open(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),"docs/design/ghost_ship_art_bible/blocks.json")))
CHAR_STYLE="\n".join([BLK["style_character"],BLK["costume_character"],BLK["impression"],BLK["chakra"],BLK["key_avatar"],BLK["negative_character"]])
# Character identity register (roster.json, art bible v0.4): the only source of officer and Arakane designs.
ROSTER=json.load(open(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),"docs/design/ghost_ship_art_bible/roster.json")))
ARAKANE_V2="art/crownhold/avatar_crownhold_arakane_v2.webp"  # brief A delivers this; #5 and #46-#48 wait for it
ARAKANE_READY=os.path.exists(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),ARAKANE_V2))
CROWN=[c for c in ROSTER["characters"] if c.get("crown")][0]["crown"]
CROWN_GATE=("" if ARAKANE_READY else "BLOCKED until brief A (the Arakane v2 avatar) is approved and committed; then rerun "
            "the builder and the approved avatar joins this image as its SUBJECT reference. Do not generate before that.")
def char_subject(c):
    d=ROSTER["divisions"][c["division"]]
    rank=BLK["commander"] if c["rank"]!="regular" else BLK["regular"]
    if c["rank"]=="final_boss":
        assert "no gold, no crown." in rank
        rank=rank.replace("no gold, no crown.","no gold; he alone wears the Command Crown, and he stands tallest of all.")
    parts=[f"{c['title']}: Crownhold, Division {c['division']} ({d['name']}).",
           f"Head: {c['head']}.", f"Weapon or prop: {c['weapon_or_prop']}.", f"Stance: {c['stance']}."]
    if c.get("crown"): parts.append(c["crown"]["lock"]+" Crown constraints: "+c["crown"]["forbid"]+".")
    if c["constraints"]: parts.append("Keep: "+"; ".join(c["constraints"])+".")
    parts+= [rank, BLK["division_"+c["division"]], BLK["material_accent"].format(**d["material_accent"])]
    return " ".join(parts)
RAW="https://raw.githubusercontent.com/perseverance484/tnr-tools/"+SHA+"/"
import os
ROOT=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT=os.path.join(ROOT,"docs/handoffs/SKYGLASS_CROWNHOLD_ART_BATCH.md")
REF={
 "coffer":"art/skyglass_event_icons/exports/icon-skyglass-coffer.webp",
 "foundry_chart":"art/skyglass_event_icons/exports/icon-chart-drowned-foundry.webp",
 "lantern":"art/skyglass_event_icons/exports/icon-skyglass-signal-beacon.webp",
 "crown":"art/ghost_ship_skyglass/icon_ghost_ship_skyglass_crown.webp",
 "arakane":"art/crownhold/avatar_crownhold_arakane.webp",
 "arsenal":"art/ghost_ship_skyglass/avatar_ghost_ship_arsenal_keeper.webp",
 "deck_warden":"art/ghost_ship_skyglass/avatar_ghost_ship_deck_warden.webp",
 "captain":"art/ghost_ship_skyglass/avatar_ghost_ship_captain_b.webp",
 "seal_charge":"art/ghost_ship_skyglass/avatar_ghost_ship_seal_charge.webp",
 "bbe":"art/style_refs/jutsu_icons/bbe/icon_bbe_sapphire_command_v2.webp",
 "gallery":"art/ghost_ship_skyglass/scene_bg_ghost_ship_command_observation_gallery.webp",
 "helm":"art/ghost_ship_skyglass/scene_bg_ghost_ship_helm.webp",
 "captain_portrait":"art/ghost_ship_skyglass/scene_char_ghost_ship_captain_portrait_b.webp",
 "countermand_ref":"art/crownhold/avatar_crownhold_arakane.webp",
 "treasury_subject":"art/skyglass_event_icons/raw/subject_sealed_treasury_painted_v1.webp",
}
ICON_STYLE=("Style: PREMIUM PIXEL ART game item icon, the same pixel rendering as the PIXEL STYLE reference: crisp hard-edged "
 "pixels, clean dark outlines, flat cel shading with a few deliberate highlight steps, limited palette, no anti-aliased "
 "blur, no painterly gradients. Colours as the subject: cool blue-black wood and blue-grey iron, silver-grey metal "
 "highlights, ONE accent of pale cyan faceted skyglass with a small glow, cool cyan rim light. Camera at eye level, 3/4 "
 "view, strong readable silhouette at 125 px, centered, single object, small even margin. Square 1024 x 1024, on a true "
 "solid flat lime-green chroma key background (#00FF00) covering the entire canvas, not transparent, not checkerboard.\n"
 "Negative: no text, no letters, no numbers, no UI, no frame, no watermark, no table or surface, no shadow on the background, "
 "no glow halo, no second object, no question mark, no painted or smooth illustration look, no blur.")
AV_STYLE=("Style: single full-body character avatar, crisp pixel art with clean dark outlines and flat cel shading matching the "
 "style reference, front three-quarter view, whole figure inside the frame with a clear margin, on a true solid flat magenta "
 "chroma key background (#FF00FF) covering the entire canvas, not transparent, not checkerboard. Square 1024 x 1024.\n"
 "Negative: no text, no UI, no watermark, no scenery, no floor, no cast shadow on the magenta, no magenta spill, no second "
 "character, no undead imagery (no rot, bones, skulls or grave motifs), no realistic or painterly rendering, no blur, no "
 "gradient background, no sheet, no grid.")
# Officer and Foundry Warden prompts come from the art bible blocks (BLK / CHAR_STYLE above), RUL-2026-10-26-002.
SCENE_STYLE=("Style: PREMIUM PIXEL ART game scene background, the same pixel rendering as the PIXEL STYLE reference (crisp "
 "hard-edged pixels, clean dark outlines, flat cel shading with deliberate highlight steps, limited palette, no painterly "
 "blur), wide 3:2 landscape (1536 x 1024), no characters, no people, no text, no UI, no watermark, no frame. Leave the "
 "lower-left and lower-right thirds readable: dialog portraits stand there. Palette and lighting as the colour reference: "
 "night or dusk, deep blues, Skyglass cyan light.")
JUTSU_STYLE=("Style: PREMIUM PIXEL ART jutsu icon (crisp hard-edged pixels, clean dark outlines, flat cel shading, limited "
 "palette, no painterly blur), laid out like the attached exemplar: a single bold technique emblem on a designed dark "
 "background with the same framing, rendering and detail density; square 1024 x 1024; readable at 125 px. A designed "
 "background is allowed (no chroma key needed).\nNegative: no text, no letters, no UI, no watermark, no character portrait, "
 "no second emblem.")

items=[]
def add(no,name,target,key,deliver,refs,prompt,style,note=""):
    items.append(dict(no=no,name=name,target=target,key=key,deliver=deliver,refs=refs,prompt=prompt,style=style,note=note))

add(1,"Sealed Treasury","ICON","lime","icon-sealed-treasury.webp",[("SUBJECT: redraw this exact chest","treasury_subject"),("PIXEL STYLE: rendering only, not the character","arakane")],
 "The Sealed Treasury: redraw the chest in the SUBJECT reference almost exactly (same shape, proportions, iron bands, "
 "corner brackets, front hasp, round seal lock with its big faceted pale cyan crystal, and the gold coins and small cyan gem "
 "showing at the gap under the lid) as premium pixel art. Shift its colours cooler to fit the set: blue-black wood and "
 "blue-grey iron instead of brown and grey.",ICON_STYLE)
add(2,"Archive Chart Case","ICON","lime","icon-archive-chart-case.webp",[("CHART FAMILY: shape and materials (painted: redraw as pixel art)","foundry_chart"),("PIXEL STYLE: rendering only, not the character","arakane")],
 "The Archive Chart Case: a long cylindrical map case of dark lacquered wood with blackened iron end caps, lying at a "
 "slight angle; one end cap is open and the rolled edge of a dark chart with faint pale lines peeks out (the same chart "
 "paper as reference 1). Crossed pale paper seal strips bind the middle, with a small iron seal plate set with one faceted "
 "pale cyan skyglass bead.",ICON_STYLE)
add(3,"Chart of the Buried Cache","ICON","lime","icon-chart-buried-cache.webp",[("SHAPE AND LAYOUT (painted: redraw as pixel art)","foundry_chart"),("PIXEL STYLE: rendering only, not the character","arakane")],
 "The Chart of the Buried Cache: the same half-unrolled chart as the reference, sun-faded and salt-stained, sand caught in "
 "its folds. Instead of a ship plan, the unrolled part shows a stretch of coastline in faint pale lines with three small "
 "coves, older lines faintly visible beneath newer corrections. Beneath a tiny drawn stone shrine above one cove, a single "
 "cross mark is picked out in glowing pale cyan skyglass ink; the other two coves stay plain. A frayed rope cord with one "
 "faceted pale cyan skyglass bead ties the rolled end.",ICON_STYLE.replace("no question mark.","no question mark, no ship plan, no compass-rose lettering, no skull, no pirate imagery."))
add(4,"Unmarked Cargo","ICON","lime","icon-unmarked-cargo.webp",[("MATERIAL AND COLOURS (it is painted: do not copy its rendering)","coffer"),("PIXEL STYLE: rendering only, not the character","arakane")],
 "Unmarked Cargo: a plain wooden cargo crate hauled out of the Skyglass wreck, deliberately anonymous. Dark weathered "
 "planks, blackened iron corner brackets, wrapped twice in heavy iron chain held by one padlock. Every stencil and marking "
 "has been scraped off, leaving pale scratched patches. A thin line of pale cyan skyglass light leaks from one seam.",
 ICON_STYLE+" No stencil text, no shipping labels.")
add(5,"Crownbreaker (badge)","ICON","magenta","icon-badge-crownbreaker.webp",
 ([("SUBJECT: keep the Command Crown exactly","arakane_v2")] if ARAKANE_READY else [])+[(BLK["reference_object"],"seal_charge")],
 "Crownbreaker: Supreme Commander Arakane's Command Crown at the moment it breaks. "+CROWN["lock"]+" The iron ring is "
 "split through the cyan seal stone, the two halves pushed apart; a sharp white crack of light at the break; the seven "
 "skyglass blades scatter and tumble outward. No hands, no figure. Crown constraints: "+CROWN["forbid"]+".",
 ICON_STYLE.replace("lime-green chroma key background (#00FF00)","magenta chroma key background (#FF00FF)").replace("no question mark.","no question mark, no medal border, no ribbon, no magenta spill."),
 note=CROWN_GATE)
add(6,"Lastlight (jutsu icon)","JUTSU_ICON","none","icon-jutsu-lastlight.webp",[("STYLE: jutsu icon register","bbe"),("MOTIF: the lantern's light","lantern")],
 "Lastlight: Crownhold's final signal turned into a weapon. One straight beam of pale cyan-white skyglass light fired "
 "from a small lantern-shaped flare at the lower left, burning diagonally through the frame; faint ember-red wounds "
 "where the beam has cut, fading at the edges.",JUTSU_STYLE)
add(7,"Foundry Warden (AI avatar)","AI_AVATAR","magenta","avatar_skyglass_foundry_warden.webp",[(BLK["reference_character"],"deck_warden")],
 "The Foundry Warden: a Skyglass ship's crewman who keeps the drowned foundry under the wreck's keel. Head: a dark tenugui "
 "headwrap and a cloth mask. Weapon or tool: long iron crucible tongs, a small iron ladle of molten pale cyan skyglass "
 "hanging at the belt. Stance: a lean, braced working guard, tongs held forward like a polearm. Keep: a scorched dark "
 "leather apron over an indigo kimono, sleeves tied back with a tasuki cord, soaked to the knees; not bulky, not brown "
 "overall. "+BLK["regular"],CHAR_STYLE)

# Officers #8-#26 render from the register; batch numbers and delivery files come from it unchanged.
OFFICERS=sorted((c for c in ROSTER["characters"] if c["batch_no"]), key=lambda c: c["batch_no"])
assert [c["batch_no"] for c in OFFICERS]==list(range(8,27)), "register must route exactly #8-#26"
for c in OFFICERS:
    add(c["batch_no"],c["title"]+(" (commander)" if c["rank"]=="commander" else ""),"AI_AVATAR","magenta",c["deliver"],
        [(BLK["reference_character"],"deck_warden")],char_subject(c),CHAR_STYLE)
n=27
SCENES=[
 ("Crownhold gate","scene_bg_crownhold_gate.webp","A snow-drifted parade ground before an open gate cut into a mountain wall; the gate stands open and unguarded; no banners; deep, unbroken snow; faint cyan light deep inside. (Used by: the fail node, 'you wake outside the gate in the snow'.)"),
 ("Armory proving hall","scene_bg_crownhold_proving_hall.webp","Inside the castle armoury: long wooden racks of yari, naginata and katana, a straw-target trial range on packed earth, a wooden placard by the first rack, cold stone walls and worn tatami. (Used by: Division I opening, the Trialmaster.)"),
 ("Ordnance store","scene_bg_crownhold_ordnance_store.webp","An open ordnance store past the trial range: a wooden counter with a ledger, lacquered boxes of paper explosive tags glowing faintly at their edges, scorch marks on the stone. (Used by: the Tagwright.)"),
 ("Test gallery","scene_bg_crownhold_test_gallery.webp","A narrow stone spear-trial gallery: a heavy wooden thrusting post bound in iron bands and scorched by lightning chakra, split straw targets along the walls, a few crackling sparks. (Used by: the Lancer.)"),
 ("Armory command shrine","scene_bg_crownhold_armory_terminal.webp","A carved command shrine set into the armoury wall beside a sealed door: a lacquered seal desk with a glowing skyglass seal stone, and a low crawlway hatch behind the weapon racks closed by a three-bolt wooden lock. (Used by: Division I command node, puzzle, protocols.)"),
 ("Forge wall","scene_bg_crownhold_forge_wall.webp","The armoury's heart: a towering forge wall hung with every weapon type ever tested, a glowing charcoal forge, an anvil, a sealed door behind. (Used by: the Armsmaster.)"),
 ("Archive of impressions","scene_bg_crownhold_archive_of_impressions.webp","An archive hall of tall wooden shelves: paper-tagged boxes of skyglass record crystals, each holding a faint sleeping light, and racks of scrolls; cold blue air, a low reading desk with an open ledger. (Used by: Division II opening, the Archivist.)"),
 ("Sealing jar halls","scene_bg_crownhold_vat_halls.webp","Halls of tall sealed ceramic jars and lacquered wooden tubs bound in rope and paper seals, a few glowing faintly from within, lit by one tall skyglass lantern pillar; iron rings of seal keys on hooks; one jar cracked and dark. (Used by: the Binder, the Echo.)"),
 ("Research command shrine","scene_bg_crownhold_research_terminal.webp","A carved command seal desk beside the sliding door of the recall chamber, a wooden plaque on the door, a locked stair behind the sealing jars. (Used by: Division II command node, puzzle, protocols.)"),
 ("Recall chamber","scene_bg_crownhold_reconstruction_theatre.webp","A recall chamber seen from a raised wooden gallery behind half-open shoji panels: a central tatami floor ringed by low tiered benches, an empty healer's table under a frame of bamboo and paper seals with skyglass crystals hung on cords. (Used by: Replicant Zero.)"),
 ("High Command signal room","scene_bg_crownhold_signal_room.webp","A signal tower room: a long wooden board of signal bells and coloured cords, a taiko drum by the window, a scroll on the writing desk filling with brushed lines one by one as if an unseen hand writes, maps of borders that no longer exist on the walls; empty of people. (Used by: Division III opening, the Signaller, and the aftermath; whoever sends the order is NEVER shown.)"),
 ("Planning hall","scene_bg_crownhold_planning_hall.webp","A planning hall set for a war council no one will attend: a long table with campaign maps, empty chairs, an inkwell of glowing chakra ink. (Used by: the Tactician.)"),
 ("Honor guard corridor","scene_bg_crownhold_honor_guard_corridor.webp","A long corridor lined with suits of plain lacquered armour on wooden stands, naginata racked between them, leading to a closed sliding door. (Used by: the Honor Guard.)"),
 ("High Command shrine","scene_bg_crownhold_high_command_terminal.webp","A carved command seal desk outside a senior officer's sliding door, a narrow service corridor beside it, bamboo dispatch tubes on a rack. (Used by: Division III command node, puzzle, protocols.)"),
 ("The Second's office","scene_bg_crownhold_marshals_office.webp","A severe, unadorned office: a low folding map table, a single cushion, a window onto snow, thirty years of annotated orders pinned to the wall. (Used by: the Second.)"),
 ("Sanctum gate","scene_bg_crownhold_sanctum_gate.webp","The summit: a gate of dark obsidian lit by ember light at the top of a long stair, ember braziers, the Supreme Command banner. (Used by: Division IV opening, the Vanguard.)"),
 ("Sanctum antechamber","scene_bg_crownhold_antechamber.webp","An obsidian antechamber with a lectern for a herald's scroll, lightning-blue light on black stone, ember lamps. (Used by: the Herald.)"),
 ("Outer ring and shrine","scene_bg_crownhold_outer_ring.webp","The curved night-watch corridor of the Sanctum's outer ring, the last command shrine glowing in a wall niche, a sealed door ahead, a narrow drainage channel under an iron grate in the floor. (Used by: the Last Watch, Division IV command node, puzzle, protocols.)"),
 ("Throne room","scene_bg_crownhold_throne_room.webp","An obsidian throne room lit by ember light, a tall summit window looking out over a whole mountain range at night, an empty command seat; seven faint blade-shaped cyan glints hang in the dark above it (the commander is not shown). (Used by: Supreme Commander Arakane.)"),
]
SHRINE_NOTE="The quest text still calls this place a terminal (renaming it is a content decision); the art draws an Edo command shrine."
for title,fname,brief in SCENES:
    add(n,"Scene: "+title,"SCENE_BACKGROUND","none",fname,[("COLOUR AND LIGHTING only (it is painted: do not copy its rendering)","gallery"),("PIXEL STYLE: rendering only, not the character","captain_portrait")],
        brief,SCENE_STYLE,note=SHRINE_NOTE if "shrine" in title.lower() and "stone shrine" not in title.lower() else ""); n+=1
add(n,"The Last Directive (jutsu icon)","JUTSU_ICON","none","icon-jutsu-the-last-directive.webp",[("STYLE: jutsu icon register","bbe")]+([("MOTIF: the Command Crown","arakane_v2")] if ARAKANE_READY else []),
 "The Last Directive: a commander's final order to himself. The Command Crown's seven skyglass blades standing in a guarding circle around a single upright blade planted point-down, the blackened-iron ring and its cyan seal stone beneath. "+CROWN["lock"]+" No gold, no strings or threads.",JUTSU_STYLE,note=CROWN_GATE); n+=1
add(n,"Extermination Order (jutsu icon)","JUTSU_ICON","none","icon-jutsu-extermination-order.webp",[("STYLE: jutsu icon register","bbe")]+([("MOTIF: the Command Crown","arakane_v2")] if ARAKANE_READY else []),
 "Extermination Order: a killing command. The Command Crown's seven skyglass blades flying in from the edges and converging on one point, where a sealed elemental sigil cracks apart. No gold, no strings or threads.",JUTSU_STYLE,note=CROWN_GATE); n+=1
add(n,"Countermand (item icon)","ICON","lime","icon-countermand.webp",([("SUBJECT: the seal tablet at Arakane's belt","arakane_v2")] if ARAKANE_READY else [])+[(BLK["reference_object"],"seal_charge")],
 "Countermand: Crownhold's command seal. A rectangular blackwood tablet framed in blackened iron, hanging on a short chain, its face carved with one simple geometric seal and set with a small faceted pale cyan seal stone. No gold.",ICON_STYLE,note=CROWN_GATE); n+=1

REDRAW=[("Skyglass Coffer","icon-skyglass-coffer.webp"),("Katon Tool Pouch","icon-tool-pouch-katon.webp"),
 ("Wave Tool Pouch","icon-tool-pouch-wave.webp"),("Ikazuchi Tool Pouch","icon-tool-pouch-ikazuchi.webp"),
 ("Stonefall Tool Pouch","icon-tool-pouch-stonefall.webp"),("Zephyrfang Tool Pouch","icon-tool-pouch-zephyrfang.webp"),
 ("Chart of the Drowned Foundry","icon-chart-drowned-foundry.webp"),("Chart of the Quarantined Archive","icon-chart-quarantined-archive.webp"),
 ("Chart of the Captain's Watch","icon-chart-captains-watch.webp"),("Lastlight Lantern","icon-skyglass-signal-beacon.webp"),
 ("Armory Requisition","icon-armory-requisition.webp")]
for name,f in REDRAW:
    key="redraw_"+f
    REF[key]="art/skyglass_event_icons/exports/"+f
    st=ICON_STYLE
    if "zephyrfang" in f: st=ICON_STYLE.replace("lime-green chroma key background (#00FF00)","magenta chroma key background (#FF00FF)")
    add(n,name+" (pixel redraw)","ICON","magenta" if "zephyrfang" in f else "lime",f.replace(".webp","-pixel.webp"),
        [("SUBJECT: redraw this exact icon","redraw_"+f),(BLK["reference_object"],"seal_charge")],
        name+": redraw the SUBJECT reference almost exactly (same object, shape, proportions, details, colours and accent) as "
        "premium pixel art, so it matches the rest of the set. Change nothing about the design.",
        st.replace("Colours as the subject: cool blue-black wood and blue-grey iron, silver-grey metal highlights, ONE accent of pale cyan faceted skyglass with a small glow, cool cyan rim light. ","Colours exactly as the SUBJECT reference. "))
    n+=1

OLD_ICONS=[("Skyglass Crown","icon_ghost_ship_skyglass_crown.webp","lime"),("Skyglass Crown Fragment","icon_ghost_ship_skyglass_crown_fragment.webp","lime"),
 ("Skyglass Crystal","icon_ghost_ship_skyglass_crystal.webp","lime"),("Skyglass Filament","icon_ghost_ship_skyglass_filament.webp","lime"),
 ("Skyglass Katana","icon_ghost_ship_skyglass_katana.webp","lime"),("Skyglass Serum","icon_ghost_ship_skyglass_serum.webp","lime")]
for name,f,key in OLD_ICONS:
    REF["redraw_"+f]="art/ghost_ship_skyglass/"+f
    add(n,name+" (pixel redraw)","ICON",key,f.replace(".webp","_pixel.webp"),
        [("SUBJECT: redraw this exact icon","redraw_"+f),(BLK["reference_object"],"seal_charge")],
        name+": redraw the SUBJECT reference almost exactly (same object, shape, proportions, details, colours and accent) as "
        "premium pixel art, so it matches the rest of the set. Change nothing about the design.",
        ICON_STYLE.replace("Colours as the subject: cool blue-black wood and blue-grey iron, silver-grey metal highlights, ONE accent of pale cyan faceted skyglass with a small glow, cool cyan rim light. ","Colours exactly as the SUBJECT reference. "))
    n+=1
HUNT_SCENES=[
 # (title, file, brief, painted subject to base the composition on or None, colour ref, used by)
 ("Wreck keel and hatch","scene_bg_skyglass_wreck_keel.webp",
  "Outside the beached Skyglass warship at night: its split keel lies on wet sand and dark rocks at the waterline, iron bands "
  "and timber looming overhead; glowing pale cyan seal channels run along the hull into a low hatch rimmed with cooled "
  "crystal, and seawater pours past the hatch into the dark below.",
  "exterior_keel_walk","helm","Drowned Foundry d_arrive; Quarantined Archive d_arrive"),
 ("Flooded intake","scene_bg_skyglass_foundry_intake.webp",
  "The foundry's intake hall inside the wreck, half flooded: dark water at knee height, empty seal casks bobbing "
  "against the walls, bamboo-and-timber water channels and wooden sluice gates, pale cyan light glinting off the water.",
  None,"lower_hull","Drowned Foundry d_intake, b_intake"),
 ("Cooling racks","scene_bg_skyglass_foundry_racks.webp",
  "A long hall of iron cooling racks stacked with freshly cast, glowing pale cyan Skyglass ingots that no one has "
  "collected; water at ankle height across the floor; a sealed hatch high on the far wall.",
  None,"hold","Drowned Foundry d_racks"),
 ("Pour hall","scene_bg_skyglass_foundry_pour_hall.webp",
  "The pour hall: rows of stone casting moulds lashed together with rope-bound seal charges, an inspector's ledger desk, knee-deep "
  "water, and an orange-white crucible glow coming up through iron floor grates from below.",
  None,"lower_hull","Drowned Foundry d_hall, b_hall, d_gate"),
 ("Crucible chamber","scene_bg_skyglass_foundry_crucible.webp",
  "The crucible chamber, the only dry room in the works, kept dry by heat: a great tilting crucible of molten pale cyan "
  "Skyglass hung in heavy pouring gear, glowing moulds, steam rising where water seeps in at the edges.",
  None,"hold","Drowned Foundry d_crucible, b_warden, d_pour"),
 ("Rebuilding lower hull","scene_bg_skyglass_lower_hull.webp",
  "Below the waterline inside the wreck: the hull is rebuilding itself out of timber and rope that do not belong "
  "together, half-formed frames knitting in pale cyan seal light; a ladder down to a severed seal channel pulsing with cyan light.",
  "lower_hull","lower_hull","Quarantined Archive d_hull, b_horror, d_conduit"),
 ("Reconstruction chamber","scene_bg_skyglass_reconstruction_chamber.webp",
  "Rows of empty upright frames, each holding a faint human impression in seal light; a three-way seal plate in the "
  "centre of the floor.",
  "reconstruction_chamber","reconstruction_chamber","Quarantined Archive d_chamber, d_seal1, d_alarm1, b_alarm1"),
 ("Quarantined archive","scene_bg_skyglass_quarantined_archive.webp",
  "A narrow sealed archive not on any ship plan: tall index shelves of command records and route sheets, a handle-less "
  "door crossed with pale script, containment seals on every cabinet.",
  "quarantined_archive","quarantined_archive","Quarantined Archive d_seal2 onward, alarms 2-3, the Sealwright"),
 ("Night cove landing","scene_bg_skyglass_cove_landing.webp",
  "A quiet cove at night under a full moon: the Ghost Ship's longboat drawn up on the sand, oars shipped, a lantern on its "
  "bow; dark water and the silhouette of the wreck's masts beyond the headland.",
  "cache_site","cache_site","Captain's Watch d_landing"),
 ("Chart room","scene_bg_skyglass_chart_room.webp",
  "The ship's chart room: a big table buried in charts layered with decades of corrections, route pins and dividers, "
  "glowing pale cyan route lines redrawn over older ink.",
  "chart_room","chart_room","Captain's Watch fight 1 (Wayfinder)"),
 ("Open deck in a gale","scene_bg_skyglass_deck.webp",
  "The open upper deck in a rising gale: torn sails cracking, rigging lines singing, empty mess tables lashed down, "
  "pale cyan seal light along the rails.",
  "deck_b","deck_b","Captain's Watch fight 2 (First Blade)"),
 ("Helm and command dais","scene_bg_skyglass_helm.webp",
  "The raised command dais at the helm: the great wheel, core-link seals glowing pale cyan in the floor, the ship's "
  "seal sigil on a banner, night sky beyond.",
  "helm","helm","Captain's Watch fight 3 (the Captain)"),
 ("Observation gallery","scene_bg_skyglass_observation_gallery.webp",
  "A viewing gallery above the command deck: tall windows showing the whole ship's glowing seal network repairing "
  "itself, storage chests along the walls.",
  "command_observation_gallery","command_observation_gallery","Captain's Watch endings"),
 ("Three coves and the stone shrine","scene_bg_skyglass_buried_cache_shore.webp",
  "A stretch of night shore with three small coves: a split cliff breaking the tide on the left, an open beach past a "
  "reef in the middle, and on the right a small stone shrine on the cliff above a cove, its shadow falling across the "
  "sand where the cache is buried.",
  "cache_site","cache_site","The Buried Cache, every node"),
]
for title,f,brief,subj,colour,used in HUNT_SCENES:
    cref="scene_"+colour
    REF[cref]="art/ghost_ship_skyglass/scene_bg_ghost_ship_%s.webp"%colour
    if subj:
        sref="scene_"+subj
        REF[sref]="art/ghost_ship_skyglass/scene_bg_ghost_ship_%s.webp"%subj
        refs=[("COMPOSITION AND COLOUR base (painted: redraw, do not copy its rendering)",sref),("PIXEL STYLE: rendering only, not the character","captain_portrait")]
        lead="Use the first reference as the starting composition and colour, changed to match this brief exactly: "
    else:
        refs=[("COLOUR AND LIGHTING only (painted: do not copy its rendering or layout)",cref),("PIXEL STYLE: rendering only, not the character","captain_portrait")]
        lead="A new location: "
    add(n,"Scene: "+title,"SCENE_BACKGROUND","none",f,refs,lead+brief+" (Used by: "+used+".)",SCENE_STYLE)
    n+=1

ARAKANE=[c for c in ROSTER["characters"] if c.get("brief_id")=="A"][0]
if ARAKANE_READY: REF["arakane_v2"]=ARAKANE_V2
items.insert(0,dict(no="A",name="Supreme Commander Arakane",target="AI_AVATAR",key="magenta",deliver=ARAKANE["deliver"],
    refs=[(BLK["reference_character"],"deck_warden")],prompt=char_subject(ARAKANE),
    style=CHAR_STYLE.replace("no tassels, no crown, ","no tassels, no second crown, "),
    note="Prerequisite brief, outside the 79. Prerequisite for #5 and #46-#48. Replaces the gold design of avatar_crownhold_arakane.webp (kept as history; delivered under a new name)."))
assert "no second crown" in items[0]["style"]
NUMBERED=[it for it in items if isinstance(it["no"],int)]
L=[]
L.append("# Art batch: Skyglass event and Crownhold (%d images, plus prerequisite brief A)\n" % len(NUMBERED))
L.append("- **Director, 2026-10-25:** \"Draft up a design document for the art director to pull each prompt from and use references. Then a short compact hand off for each image in sequence and I hand you back the approved image.\"")
L.append("- **Style (director, 2026-10-25):** every image in this batch is PREMIUM PIXEL ART, the same rendering as the Crownhold/crew avatars. Painted references (the Coffer, the charts, the jutsu exemplar) supply subject, materials and colours only. **Art bible v0.4 (proposed):** `docs/design/ghost_ship_art_bible/` (ART_BIBLE.md, blocks.json, roster.json); the original crew is the rendering anchor: the Deck Warden for characters, the Seal Charge for objects, the Captain's portrait for scenes. Arakane's gold avatar is off-model and is not a reference.")
L.append("- **Protocol:** `docs/workflows/ISOLATED_ART_GENERATION.md`. One image per fresh session, at most two reference images (never a collage), one candidate at a time. The art director returns the RAW image; Claude Code keys, crops, exports and QCs it (`skills/producing-tnr-art`), then swaps the placeholder in game by manifest.")
L.append("- **Pixel redraws (#36 to #46):** the event icons already live were painted; each is redrawn as pixel art from its own approved image so the whole set matches (director, 2026-10-25).")
L.append("- **More pixel art (#47 onward):** the six Skyglass item icons inside the Coffer (redraws), then one scene per location the hunts actually depict (14; the wreck is now beached, and each Foundry room gets its own). Each scene lists the nodes that use it so the quests can be repointed when the art lands. Already pixel art and NOT redrawn: every crew avatar, the four scene portraits, the map structure. Left out: the retired Reliquary and old chests, and the retiring Ghost Ship quest icon.")
L.append("- **Prerequisite A:** Supreme Commander Arakane redrawn to the v0.4 crown lock (iron ring, seven skyglass blades, no gold); #5 and #46-#48 are BLOCKED until it is approved. **Not in this batch:** the Sealwright and Oathkeeper scene portraits (already exist). **Deferred:** the Lastlight hit animation (a vertical strip sprite sheet; its placeholder is KGK: Black Fang Lance's).")
L.append("- **How a session uses this file:** it is given the link to this file and an image number. It reads that image's section, downloads the reference images from the links there, attaches them in the order given, and runs the prompt exactly as written.")
L.append("- **Live-game requests/writes:** 0.\n")
L.append("## Session contract (every image, no exceptions)\n")
L.append("1. **The operator attaches the reference files from that image's folder** in `skyglass_art_batch.zip` (one folder per image: `ref1_*`, `ref2_*` in attach order, plus `prompt.txt`). Art sessions have no network access. The raw URLs below are the canonical source. Never use a text-only repository connector: it cannot return images.")
L.append("2. **Verify each attached file:** it is present and shows the described subject. Width x height, byte size and SHA-256 describe the original and are informational only: chat uploads are resized and recompressed.")
L.append("3. **Show each reference back** (display it) and confirm it is attached to the generation request, in the listed order, with its listed role.")
L.append("4. **Abort if any reference is missing, fails verification or cannot be attached.** Report which one and stop. Never generate without all references.")
L.append("5. **Copy the fenced prompt (or the folder's `prompt.txt`) verbatim.** Do not shorten, summarise or rewrite it.")
L.append("6. Generate exactly one candidate. Do not crop, key, resize or otherwise process it. Return the raw image under the name the prompt gives.\n")
L.append("## Targets (from `25x_DATA_art_spec.json`)\n")
L.append("| Target | Canvas to generate | Key | Delivered |\n|---|---|---|---|")
L.append("| ICON | 1024 x 1024 | lime (magenta when the subject is green or the brief says so) | 256 px webp |")
L.append("| JUTSU_ICON | 1024 x 1024 | none: designed background allowed (RUL-2026-10-14-001) | 256 px webp |")
L.append("| AI_AVATAR | 1024 x 1024 | magenta | square webp, up to 1024 px |")
L.append("| SCENE_BACKGROUND | 1536 x 1024 (3:2) | none | 512 x 341 webp |\n")
L.append("## Reference files\n")
L.append("Every link is pinned to commit `%s`, so it never changes. A fresh session downloads the images named in its section and attaches them.\n" % SHA)
L.append("| Key | Image link | Bytes | W x H | SHA-256 |\n|---|---|---|---|---|")
seen=set()
for k,v in REF.items():
    if v in seen or k=="countermand_ref": continue
    seen.add(v); b,w,h,sh=meta(v)
    L.append(f"| {k} | {RAW}{v} | {b} | {w} x {h} | `{sh}` |")
L.append("\n## Sequence\n")
L.append("| # | Image | Target | Key | References | Delivery file |\n|---|---|---|---|---|---|")
for it in items:
    L.append(f"| {it['no']} | {it['name']} | {it['target']} | {it['key']} | {', '.join(r for _,r in it['refs'])} | `{it['deliver']}` |")
L.append("\n## Prompts\n")
for it in items:
    L.append(f"### {it['no']}. {it['name']}\n")
    if it.get("note"): L.append(f"> {it['note']}\n")
    L.append("References (download and attach, in this order):\n")
    for i,(role,r) in enumerate(it['refs']):
        b,w,h,sh=meta(REF[r])
        L.append(f"{i+1}. {role}: {RAW}{REF[r]}  ({b} bytes, {w} x {h}, sha256 `{sh[:16]}…`)")
    L.append("")
    L.append("~~~text")
    L.append(f"Draw ONE image for The Ninja RPG: {it['name']}. Generate exactly one candidate. Do not crop, key or process it.")
    L.append("References attached: " + "; ".join(f"{i+1}. {role}" for i,(role,_) in enumerate(it['refs'])) + ". Follow each reference only for its stated role.\n")
    L.append("Subject: " + it['prompt'] + "\n")
    L.append(it['style'])
    L.append(f"\nReturn the raw image named raw_{it['deliver'].rsplit('.',1)[0]}.png.")
    L.append("~~~\n")
open(OUT,"w").write("\n".join(L)+"\n")
json.dump(items,open(os.path.join(ROOT,"state/skyglass_art/items.json"),"w"),indent=1)
print(len(items))


# ---- per-image folders: skyglass_art_batch.zip (built on request: python3 build_art_batch.py --zip OUTDIR)
import sys, zipfile, re as _re
if "--zip" in sys.argv:
    out = sys.argv[sys.argv.index("--zip") + 1]
    os.makedirs(out, exist_ok=True)
    zpath = os.path.join(out, "skyglass_art_batch.zip")
    doc = open(OUT).read()
    with zipfile.ZipFile(zpath, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("README.txt", (
            "Skyglass / Crownhold art batch. One folder per image, in order.\n"
            "In a fresh image session: attach ref1_*, then ref2_* (if present) from the folder, then paste prompt.txt verbatim.\n"
            "The session checks each reference is attached and shows its subject, and stops if one is missing.\n"
            "Art bible: docs/handoffs/SKYGLASS_CROWNHOLD_ART_BATCH.md\n"))
        for it in items:
            slug = "%s_%s" % (("%02d" % it["no"]) if isinstance(it["no"], int) else it["no"], _re.sub(r"[^a-z0-9]+", "_", it["name"].lower()).strip("_")[:40])
            refs_txt = []
            for i, (role, r) in enumerate(it["refs"]):
                path = REF[r]; b, w, h, sh = meta(path)
                fname = "ref%d_%s" % (i + 1, os.path.basename(path))
                z.write(REPO + path, f"{slug}/{fname}")
                refs_txt.append(f"{i+1}. {fname}  ({role}; original {w} x {h}, the app may resize uploads)")
            sec = doc[doc.index("### %s. " % it["no"]):]
            prompt = sec[sec.index("~~~text\n") + 8: sec.index("\n~~~", sec.index("~~~text\n") + 8)]
            head = (f"Art batch #{it['no']}: {it['name']}  |  target {it['target']}  |  key {it['key']}  |  deliver {it['deliver']}\n"
                    "The operator has attached these references in this order (you have no network; do not download):\n"
                    + "\n".join(refs_txt) +
                    "\nBefore generating: confirm each reference is attached and shows the described subject. Size is informational: "
                    "uploads are often resized, so do not stop over size or file bytes. "
                    "If any is missing or wrong, STOP and report which. Then run the prompt below verbatim.\n\n---\n\n")
            z.writestr(f"{slug}/prompt.txt", head + prompt + "\n")
    print("zip:", zpath, os.path.getsize(zpath))
