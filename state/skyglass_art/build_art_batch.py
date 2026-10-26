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
add(5,"Crownbreaker (badge)","ICON","magenta","icon-badge-crownbreaker.webp",[("SUBJECT: keep the crown exactly","arakane"),("STYLE: icon rendering only","crown")],
 "Crownbreaker: Supreme Commander Arakane's Command Crown at the moment it breaks. Keep the crown from the avatar exactly: "
 "the spiked blackened-gold circlet, the halo of floating skyglass blades with the seal ring at the centre, the glowing "
 "control threads. The circlet is split down the middle through the seal, the two halves pushed apart; a white-hot crack "
 "of light bursts from the broken centre; the blades scatter and tumble outward; the threads are snapped, their loose ends "
 "curling and fading. No hands, no figure.",
 ICON_STYLE.replace("near-black iron and dark wood, ONE accent of pale cyan faceted skyglass with a soft inner glow","blackened gold and pale cyan skyglass, one white-hot burst of light at the broken centre").replace("lime-green chroma key background (#00FF00)","magenta chroma key background (#FF00FF)").replace("no question mark.","no question mark, no medal border, no ribbon, no magenta spill."))
add(6,"Lastlight (jutsu icon)","JUTSU_ICON","none","icon-jutsu-lastlight.webp",[("STYLE: jutsu icon register","bbe"),("MOTIF: the lantern's light","lantern")],
 "Lastlight: Crownhold's final signal turned into a weapon. One straight beam of pale cyan-white skyglass light fired "
 "from a small lantern-shaped flare at the lower left, burning diagonally through the frame; faint ember-red wounds "
 "where the beam has cut, fading at the edges.",JUTSU_STYLE)
add(7,"Foundry Warden (AI avatar)","AI_AVATAR","magenta","avatar_skyglass_foundry_warden.webp",[(BLK["reference_character"],"deck_warden")],
 "The Foundry Warden: keeper of the drowned skyglass foundry under the wreck's keel. A broad shipwright-smith shinobi: a "
 "dark tenugui headwrap and a cloth mask, a scorched dark leather apron over an indigo kimono, sleeves tied back with a "
 "rope tasuki cord, soaked to the knees; long iron crucible tongs in one hand, a small iron ladle of glowing pale cyan "
 "molten skyglass in the other. Accent: molten skyglass cyan.",CHAR_STYLE)

NEWNAME={"Master of Arms": "Armsmaster", "Crownhold Proving Proctor": "Trialmaster", "Ordnance Quartermaster": "Tagwright", "Prototype Lancer Unit": "Lancer", "Calibration Duelist": "Duelist", "Skyglass Archive Keeper": "Archivist", "Impression Containment Warden": "Binder", "Unstable Echo Subject": "Echo", "Failed Reconstruction Prototype": "Stonebound", "The Grand Marshal": "The Second", "Command Signal Adjutant": "Signaller", "High Command Staff Tactician": "Tactician", "Honor Guard Commandant": "Honor Guard", "Strategist's Aide-de-Camp": "Runner", "Sanctum Vanguard": "Vanguard", "Directive Herald": "Herald", "Last Watch Executor": "Last Watch", "Order-Bearer of the Sanctum": "Sealbearer"}  # role names without the live "Crown " prefix: the word draws crowns
AVATARS=[
 ("Master of Arms","Division I commander. A broad weapons-master shinobi: a plain dark iron jingasa over a hood, a cloth mask with thin forge-orange trim; a heavy dark haori over laced lacquered plates; a yari in one hand and a short ono axe in the other, katana and bundles of kunai strapped across his back; calm and exacting. Accent: forge-orange.",True),
 ("Replicant Zero","Division II commander. A tall, composed medical-nin: a plain dark grey hood and a dark cloth mask, both eyes lit pale violet; a long layered dark haori with a high stiff collar, a medic's scroll case and a row of sealing-tag pouches across the chest; a small ball of pale violet healing chakra held above his open left palm, the hand drawn normally; the first successful recall; calm and curious. No sword. Accent: pale violet.",True),
 ("The Grand Marshal","Division III commander, the Supreme Commander's deputy. An older senior shinobi officer: a wide flat kasa hat shading a plain dark cloth mask, a short grey beard visible below it; a plain dark long haori over light laced plates, a katana drawn and held low and calm in one hand; thoughtful and severe; the deputy who could question orders. Accent: muted brass, only as the hat cord and sword fittings.",True),
 ("Crownhold Proving Proctor","Division I. An armoury proctor: a grey tenugui headwrap and cloth mask, a faded grey drill kimono with tied-back sleeves, a wooden board of trial slips in one hand, two bokken at the obi, a small signal bell on a cord. Accent: drill-yellow.",False),
 ("Ordnance Quartermaster","Division I. A soot-stained short work haori, bandoliers of paper explosive tags glowing faintly at their edges, soot-dark gloves holding a lacquered tray of tags. Accent: tag-orange.",False),
 ("Prototype Lancer Unit","Division I. A lean spear specialist in light laced plates and a hood, a long cross-bladed yari with lightning chakra running along its blade, burn-scarred forearms wrapped in cloth. Accent: electric yellow.",False),
 ("Calibration Duelist","Division I. A young duelist in sparring wraps and a tenugui headwrap, a bokken with wind chakra curling along its edge, an apprentice cord on the shoulder. Accent: wind-green.",False),
 ("Skyglass Archive Keeper","Division II. An archivist-nin with a satchel of scrolls and a bound ledger, ink-stained gloves, a writing brush behind the ear of the hood, a small skyglass reading lens on a cord. Accent: archive blue.",False),
 ("Impression Containment Warden","Division II. A sealing specialist in a deep hood, a heavy iron ring of seal keys and tag-wrapped scroll cases on chains, a corked ceramic seal jar of glowing water at the hip. Accent: water teal.",False),
 ("Unstable Echo Subject","Division II. A shinobi caught mid-step splitting into an imperfect shadow clone: the clone a half-step behind and out of line, shadow chakra trailing between them, both figures solid. Accent: shadow violet.",False),
 ("Failed Reconstruction Prototype","Division II. A hulking earth-style shinobi half-encased in his own stone armour technique, rock plating cracked over one arm and shoulder, rope-bound, a tetsubo in hand. Accent: stone ochre.",False),
 ("Command Signal Adjutant","Division III. A signals shinobi: a war fan (gunbai) raised in one hand and a small nobori signal flag in the other, a message-scroll tube across the back, a rank cord. Accent: signal green.",False),
 ("High Command Staff Tactician","Division III. A tactician in a kasa hat with a campaign map case under one arm and a brush wet with glowing chakra ink, the Second's aide's cord on the shoulder. Accent: ink blue.",False),
 ("Honor Guard Commandant","Division III. A tall guard in ceremonial stone-grey laced armour and a plain jingasa, holding a naginata upright beside him. Accent: polished iron.",False),
 ("Strategist's Aide-de-Camp","Division III. A swift courier-shinobi with sealed scroll dispatch tubes on the back crackling with lightning chakra, light lacquered plates, an aide's sash. Accent: lightning white.",False),
 ("Sanctum Vanguard","Division IV. A front-line shinobi in obsidian-black laced plates and a kabuto with a menpo, fire chakra running along the edge of his katana, a short banner pole on the back. Accent: ember red.",False),
 ("Directive Herald","Division IV. Long dark ceremonial kimono and a hood, an unrolled scroll of orders in one hand marked with glowing unreadable brush marks, lightning-lit eyes. Accent: lightning gold.",False),
 ("Last Watch Executor","Division IV. A tattered night-watch cloak and hood, twin kusarigama with wind chakra along the blades, a blank mask stamped with an unreadable seal. Accent: night blue.",False),
 ("Order-Bearer of the Sanctum","Division IV. Deep-blue Sanctum wraps and a hood, a sealed scroll case on the back, a blank command seal tablet held up in one hand. Accent: deep-sea blue.",False),
]
n=8
for name,look,boss in AVATARS:
    fname="avatar_crownhold_"+name.lower().removeprefix("crownhold ").replace("'","").replace(" ","_").replace("-","_")+".webp"  # file stem keeps the original name
    name=NEWNAME.get(name,name)  # RUL-2026-10-26-003
    add(n,name+(" (commander)" if boss else ""),"AI_AVATAR","magenta",fname,[(BLK["reference_character"],"deck_warden")],
        name+": "+look+((" "+BLK["commander"]) if boss else ""),CHAR_STYLE)
    n+=1
SCENES=[
 ("Crownhold gate","scene_bg_crownhold_gate.webp","A snow-drifted parade ground before an open gate cut into a mountain wall; the gate stands open and unguarded; no banners; deep, unbroken snow; faint cyan light deep inside. (Used by: the fail node, 'you wake outside the gate in the snow'.)"),
 ("Armory proving hall","scene_bg_crownhold_proving_hall.webp","Inside the Experimental Armory: rows of weapon racks humming behind glass, a live-fire trial range with targets, a brass placard by the first rack, cold stone and military brass. (Used by: Division I opening, the Proving Proctor.)"),
 ("Ordnance store","scene_bg_crownhold_ordnance_store.webp","An open ordnance store past the trial range: a counter with a ledger, shelves of sealed explosive tags glowing with heat, scorch marks on the stone. (Used by: the Ordnance Quartermaster.)"),
 ("Test gallery","scene_bg_crownhold_test_gallery.webp","A narrow test gallery: an empty heavy firing rig bolted to the floor with lightning-scorched clamps and capacitor cables, crackling yellow sparks. (Used by: the Prototype Lancer Unit.)"),
 ("Armory command terminal","scene_bg_crownhold_armory_terminal.webp","A glowing Military Command Terminal set into the armory wall beside a sealed door, a maintenance crawlway hatch behind live-fire racks with a three-switch lock. (Used by: Division I terminal, puzzle, protocols.)"),
 ("Forge wall","scene_bg_crownhold_forge_wall.webp","The armory's heart: a towering forge wall hung with every weapon type ever tested, a glowing forge, an anvil, sealed door behind. (Used by: the Master of Arms.)"),
 ("Archive of impressions","scene_bg_crownhold_archive_of_impressions.webp","A library of glass: tall shelves of crystal cores, each holding a faint sleeping light, cold blue air, a reading desk with an open ledger. (Used by: Division II opening, the Archive Keeper.)"),
 ("Vat halls","scene_bg_crownhold_vat_halls.webp","Halls of tall glowing specimen tanks lit by one tall Skyglass lamp column; chains of vat keys on hooks; one tank cracked and dark. (Used by: the Containment Warden, the Unstable Echo Subject.)"),
 ("Research command terminal","scene_bg_crownhold_research_terminal.webp","A command terminal beside the door of the reconstruction theatre, a plaque on the door, a locked maintenance stair behind the specimen tanks. (Used by: Division II terminal, puzzle, protocols.)"),
 ("Reconstruction theatre","scene_bg_crownhold_reconstruction_theatre.webp","An operating theatre seen from behind observation glass: a central operating floor ringed by tiered seats, a reconstruction rig of light and crystal over an empty table. (Used by: Replicant Zero.)"),
 ("High Command signal room","scene_bg_crownhold_signal_room.webp","A signal room: a long relay board of brass switches and paper tape, a sheet of paper printing itself line by line, maps of borders that no longer exist on the walls; empty of people. (Used by: Division III opening, the Signal Adjutant, and the aftermath; whoever sends the order is NEVER shown.)"),
 ("Planning hall","scene_bg_crownhold_planning_hall.webp","A planning hall set for a war council no one will attend: a long table with campaign maps, empty chairs, an inkwell of glowing chakra ink. (Used by: the Staff Tactician.)"),
 ("Honor guard corridor","scene_bg_crownhold_honor_guard_corridor.webp","A long corridor lined with suits of ceremonial stone-plated armour on stands, a tower shield with a plain circled-cross seal, leading to a closed office door. (Used by: the Honor Guard Commandant.)"),
 ("High Command terminal","scene_bg_crownhold_high_command_terminal.webp","A command terminal outside a senior officer's office door, a narrow service corridor beside it, dispatch tubes on a rack. (Used by: Division III terminal, puzzle, protocols.)"),
 ("The Grand Marshal's office","scene_bg_crownhold_marshals_office.webp","A severe, unadorned office: a folding map table, a single chair, a window onto snow, thirty years of annotated orders pinned to the wall. (Used by: the Grand Marshal.)"),
 ("Sanctum gate","scene_bg_crownhold_sanctum_gate.webp","The summit: a gate of dark obsidian lit by ember light at the top of a long stair, ember braziers, the Supreme Command banner. (Used by: Division IV opening, the Sanctum Vanguard.)"),
 ("Sanctum antechamber","scene_bg_crownhold_antechamber.webp","An obsidian antechamber with a lectern for a herald's scroll, lightning-blue light on black stone, ember lamps. (Used by: the Directive Herald.)"),
 ("Outer ring and terminal","scene_bg_crownhold_outer_ring.webp","The curved night-watch corridor of the Sanctum's outer ring, the last Military Command Terminal glowing in the wall, a sealed door ahead, a maintenance channel grille in the floor. (Used by: the Last Watch Executor, Division IV terminal, puzzle, protocols.)"),
 ("Throne room","scene_bg_crownhold_throne_room.webp","An obsidian throne room lit by ember light, a tall summit window looking out over a whole mountain range at night, an empty command seat; faint cyan threads of light run from the floor up toward where the commander stands (he is not shown). (Used by: Supreme Commander Arakane.)"),
]
for title,fname,brief in SCENES:
    add(n,"Scene: "+title,"SCENE_BACKGROUND","none",fname,[("COLOUR AND LIGHTING only (it is painted: do not copy its rendering)","gallery"),("PIXEL STYLE: rendering only, not the character","captain_portrait")],
        brief,SCENE_STYLE); n+=1
add(n,"The Last Directive (jutsu icon)","JUTSU_ICON","none","icon-jutsu-the-last-directive.webp",[("STYLE: jutsu icon register","bbe"),("MOTIF: the Command Crown","arakane")],
 "The Last Directive: a commander's final order to himself. The Command Crown's seal ring blazing white-gold above a single upright blade planted point-down, an unbreakable shield of light around it.",JUTSU_STYLE); n+=1
add(n,"Extermination Order (jutsu icon)","JUTSU_ICON","none","icon-jutsu-extermination-order.webp",[("STYLE: jutsu icon register","bbe"),("MOTIF: the Command Crown","arakane")],
 "Extermination Order: a killing command. Seven taut cyan threads converging from the edges onto one point, where a sealed elemental sigil cracks apart.",JUTSU_STYLE); n+=1
add(n,"Countermand (item icon)","ICON","lime","icon-countermand.webp",[("SUBJECT AND PIXEL STYLE: the seal tablet at Arakane's belt","arakane")],
 "Countermand: Crownhold's command seal. The rectangular gold-framed seal tablet that hangs from Arakane's belt, on a short chain, its face carved with a plain circled-cross seal glowing pale cyan.",ICON_STYLE); n+=1

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
        [("SUBJECT: redraw this exact icon","redraw_"+f),("PIXEL STYLE: rendering only, not the character","arakane")],
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
        [("SUBJECT: redraw this exact icon","redraw_"+f),("PIXEL STYLE: rendering only, not the character","arakane")],
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
  "The foundry's intake hall inside the wreck, half flooded: dark water at knee height, empty seal canisters bobbing "
  "against the walls, iron pipes and valve wheels, pale cyan light glinting off the water.",
  None,"lower_hull","Drowned Foundry d_intake, b_intake"),
 ("Cooling racks","scene_bg_skyglass_foundry_racks.webp",
  "A long hall of iron cooling racks stacked with freshly cast, glowing pale cyan Skyglass ingots that no one has "
  "collected; water at ankle height across the floor; a sealed hatch high on the far wall.",
  None,"hold","Drowned Foundry d_racks"),
 ("Pour hall","scene_bg_skyglass_foundry_pour_hall.webp",
  "The pour hall: rows of stone casting moulds wired together with seal charges, an inspector's ledger desk, knee-deep "
  "water, and an orange-white crucible glow coming up through iron floor grates from below.",
  None,"lower_hull","Drowned Foundry d_hall, b_hall, d_gate"),
 ("Crucible chamber","scene_bg_skyglass_foundry_crucible.webp",
  "The crucible chamber, the only dry room in the works, kept dry by heat: a great tilting crucible of molten pale cyan "
  "Skyglass hung in heavy pouring gear, glowing moulds, steam rising where water seeps in at the edges.",
  None,"hold","Drowned Foundry d_crucible, b_warden, d_pour"),
 ("Rebuilding lower hull","scene_bg_skyglass_lower_hull.webp",
  "Below the waterline inside the wreck: the hull is rebuilding itself out of timber and cable that do not belong "
  "together, half-formed frames knitting in pale cyan seal light; a ladder down to a severed, pulsing conduit.",
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

L=[]
L.append("# Art batch: Skyglass event and Crownhold (%d images)\n" % len(items))
L.append("- **Director, 2026-10-25:** \"Draft up a design document for the art director to pull each prompt from and use references. Then a short compact hand off for each image in sequence and I hand you back the approved image.\"")
L.append("- **Style (director, 2026-10-25):** every image in this batch is PREMIUM PIXEL ART, the same rendering as the Crownhold/crew avatars. Painted references (the Coffer, the charts, the jutsu exemplar) supply subject, materials and colours only; Arakane's avatar supplies the pixel rendering.")
L.append("- **Protocol:** `docs/workflows/ISOLATED_ART_GENERATION.md`. One image per fresh session, at most two reference images (never a collage), one candidate at a time. The art director returns the RAW image; Claude Code keys, crops, exports and QCs it (`skills/producing-tnr-art`), then swaps the placeholder in game by manifest.")
L.append("- **Pixel redraws (#36 to #46):** the event icons already live were painted; each is redrawn as pixel art from its own approved image so the whole set matches (director, 2026-10-25).")
L.append("- **More pixel art (#47 onward):** the six Skyglass item icons inside the Coffer (redraws), then one scene per location the hunts actually depict (14; the wreck is now beached, and each Foundry room gets its own). Each scene lists the nodes that use it so the quests can be repointed when the art lands. Already pixel art and NOT redrawn: every crew avatar, the four scene portraits, the map structure. Left out: the retired Reliquary and old chests, and the retiring Ghost Ship quest icon.")
L.append("- **Not in this batch:** Arakane (done, `art/crownhold/avatar_crownhold_arakane.webp`); the Sealwright and Oathkeeper scene portraits (already exist). **Deferred:** the Lastlight hit animation (a vertical strip sprite sheet; its placeholder is KGK: Black Fang Lance's).")
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
            slug = "%02d_%s" % (it["no"], _re.sub(r"[^a-z0-9]+", "_", it["name"].lower()).strip("_")[:40])
            refs_txt = []
            for i, (role, r) in enumerate(it["refs"]):
                path = REF[r]; b, w, h, sh = meta(path)
                fname = "ref%d_%s" % (i + 1, os.path.basename(path))
                z.write(REPO + path, f"{slug}/{fname}")
                refs_txt.append(f"{i+1}. {fname}  ({role}; original {w} x {h}, the app may resize uploads)")
            sec = doc[doc.index("### %d. " % it["no"]):]
            prompt = sec[sec.index("~~~text\n") + 8: sec.index("\n~~~", sec.index("~~~text\n") + 8)]
            head = (f"Art batch #{it['no']}: {it['name']}  |  target {it['target']}  |  key {it['key']}  |  deliver {it['deliver']}\n"
                    "The operator has attached these references in this order (you have no network; do not download):\n"
                    + "\n".join(refs_txt) +
                    "\nBefore generating: confirm each reference is attached and shows the described subject. Size is informational: "
                    "uploads are often resized, so do not stop over size or file bytes. "
                    "If any is missing or wrong, STOP and report which. Then run the prompt below verbatim.\n\n---\n\n")
            z.writestr(f"{slug}/prompt.txt", head + prompt + "\n")
    print("zip:", zpath, os.path.getsize(zpath))
