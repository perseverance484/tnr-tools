#!/usr/bin/env python3
"""Render the Mother of Echoes prompt cards (one paste-ready block per director-generated asset).

    python3 docs/handoffs/mother_of_echoes_art_prompts.py

Writes docs/handoffs/MOTHER_OF_ECHOES_ART_PROMPTS.md and docs/handoffs/mother_of_echoes_art_prompts.json (the same
cards as data, for the review page). Do not hand-edit either output.

Where the prompts come from (nothing is paraphrased):
- AI_AVATAR (humanoid) and SCENE_BACKGROUND: spec.prompt_scaffolds rendered by
  skills/producing-tnr-art/scripts/shotlist.py render_prompt(), [STYLE] expanded from spec.house_style.clauses
  verbatim and scoped per target; only [SUBJECT] is written here.
- Every other card follows docs/handoffs/SKYGLASS_ART_PROMPTS.md exactly: its fixed lines (Style, Framing, Canvas,
  Background, Avoid, the JI Palette and Thumbnail lines) are copied out of the named Skyglass block at run time,
  so they cannot drift from the approved Skyglass cards. Why each card uses which source is in its `source` field:
  - ICON (shards, quest icon, tokens, The Remainder variant): the spec ICON scaffold asks for a "dark background",
    which contradicts the ICON target's transparent padding rule and preflight's alpha check, so it cannot render a
    deliverable item icon; the Skyglass icon cards (the shards' live siblings) are used instead. Open question for
    the art-direction owner, recorded in docs/design/MOTHER_OF_ECHOES_ART.md.
  - The Silence and the Feeler: the AI_AVATAR scaffold opens "single ninja character", which these two are not
    (canon: a dread entity and its feeler, RUL-2026-11-01-093/-094); the Skyglass FX raw-layer card is used and the
    raw is keyed and padded to the avatar square afterwards.
  - JUTSU_ICON and ANIMATION have no scaffold in the spec: Skyglass JI and AN cards.
"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))
sys.path.insert(0, os.path.join(ROOT, 'skills/producing-tnr-art/scripts'))
import shotlist  # noqa: E402

SPEC = json.load(open(os.path.join(ROOT, 'skills/producing-tnr-art/data/25x_DATA_art_spec.json')))
SKY_MD = open(os.path.join(HERE, 'SKYGLASS_ART_PROMPTS.md')).read()
BLOCKS = {m.group(1): m.group(2).split('\n') for m in
          re.finditer(r'^### (\w+) · .*?\n```text\n(.*?)\n```', SKY_MD, re.S | re.M)}
END = 'Generate ONE image. Do not crop, key, resize or otherwise process it.'


def sky(code, key):
    for line in BLOCKS[code]:
        if line.startswith(key + ':'):
            return line
    raise KeyError(f'{code} has no {key} line')


def refs(files):
    return ('References attached: ' + ' '.join(f'{n + 1}. {os.path.basename(f)}: {r}.' for n, (f, r) in enumerate(files))
            + ' Follow each reference only for its stated role.')


CARDS = []


def card(code, name, family, target, files, ret, deliver, note, lines, prio, source, records):
    CARDS.append({'code': code, 'name': name, 'family': family, 'target': target, 'priority': prio,
                  'files': [{'f': f, 'role': r} for f, r in files], 'ret': ret, 'deliver': deliver, 'note': note,
                  'prompt': '\n'.join(lines), 'source': source, 'records': records})


# ------------------------------------------------------------------------------------------------ references
CREW = ('art/ghost_ship_skyglass/avatar_ghost_ship_crowned_captain_b.webp',
        "STYLE-ONLY: the Skyglass crew's rendering, palette, outline weight and how skyglass crystal sits on dark cloth; "
        "this is a different person, described by the text")
ECHO = ('art/crownhold/avatar_crownhold_unstable_echo_subject.webp',
        'STYLE-ONLY: how a Crownhold echo is drawn (cold violet-cyan chakra haze on dark cloth); not the figure')
SCENE_REF = ('art/ghost_ship_skyglass/scene_bg_ghost_ship_command_observation_gallery.webp',
             'STYLE-ONLY: colour and lighting of the approved Skyglass scenes; do not copy its room or layout')
SCENE_REF2 = ('art/style_refs/scene_backgrounds/warehouse_loading_floor.webp',
              'STYLE-ONLY: how a TNR interior stages depth with no figure (style_refs.py select --target SCENE_BACKGROUND --tag interior); not its room')
ICON_REF = ('art/ghost_ship_skyglass/icon_ghost_ship_skyglass_crystal.webp',
            'STYLE-ONLY: the pixel rendering and the skyglass cyan of the approved Skyglass icons; do not copy the crystal')
FX_REF = ('art/skyglass_boss_fx/raw/raw_fx_ships_bell.png',
          'STYLE-ONLY: the approved Skyglass boss-FX rendering and line weight; do not copy its subject')
JI_REF = ('art/style_refs/jutsu_icons/bee/icon_bee_hemocure_v1.webp',
          'STYLE-ONLY: the approved jutsu-icon register, its layout, dark background, rendering and detail density; '
          'do not copy its orb-in-claws composition or its red')
JI_FAM = ('art/skyglass_jutsu_icons/exports/icon-jutsu-the-last-directive.webp',
          'STYLE-ONLY: the live Skyglass jutsu icon family, its skyglass shards and night palette; not its katana or composition')
TOKEN_BASE = ('VT00_approved.png',
              'SUBJECT: the approved trophy-token base; keep it exactly and change only the window motif')
TOKEN_ALT = ('art/skyglass_event_icons/exports/icon-variant-token-captains-gunbai.webp',
             'SUBJECT, only if VT00_approved.png is not to hand: a delivered boss variant token; keep the tag exactly '
             '(shape, iron, rivets, cord, angle, size, colours) and replace only what is inside its oval window')

# ------------------------------------------------------------------------------------------------ avatars (scaffold)
AV_T = SPEC['targets']['AI_AVATAR']
WHO = "one AI battle avatar for The Ninja RPG's Skyglass uber fight, The Mother of Echoes"


def av_scaffold(code, name, ai, deliver, subject, note, prio='P1', files=(CREW,)):
    r = shotlist.render_prompt(SPEC, 'AI_AVATAR', subject=subject)
    lines = [f'Target: {name}, {WHO}.', refs(files), r['positive'], r['subject_line'],
             f"Costume grammar: {r['costume_grammar']}", f"Negative: {r['negative']}; {r['hard_negatives']}", END]
    card(code, name, 'Avatars', f"{name}, AI `{ai}` · AI_AVATAR (`userData.avatar`) · {AV_T['chroma_key']} key "
         f"(scaffold) · deliver {AV_T['delivered_width_px']}px square, source {AV_T['recommended_source_px']['value']}",
         files, f'{code}_raw_{deliver[:-5]}.png', deliver, note, lines, prio,
         'spec.prompt_scaffolds.AI_AVATAR via shotlist.render_prompt', [ai])


def av_fx(code, name, ai, deliver, subject, note, prio='P1'):
    files = (FX_REF,)
    lines = [f'Target: {name}, {WHO}; drawn as one element, later keyed and padded to the square avatar.', refs(files),
             sky('AN01', 'Style'), sky('AN01', 'Canvas'), f'Subject: {subject}', sky('AN01', 'Background'),
             sky('AN01', 'Avoid'), END]
    card(code, name, 'Avatars', f"{name}, AI `{ai}` · AI_AVATAR (`userData.avatar`) · alpha or magenta key "
         f"(FX raw-layer card) · deliver {AV_T['delivered_width_px']}px square", files,
         f'{code}_raw_{deliver[:-5]}.png', deliver, note, lines, prio,
         'SKYGLASS_ART_PROMPTS.md AN card lines (the AI_AVATAR scaffold names a ninja character; this is not one)', [ai])


SAYO = ('Sayo, Mother of Echoes, the Skyglass Project\'s Glasswright: a tall, slender woman, calm and terribly gentle, '
        'in a long near-black Project work-coat with its sleeves bound back by a cord, skyglass-cyan piping at the collar '
        'and cuffs, and the coat\'s hems turned to faceted pale-cyan skyglass as if the glass is slowly climbing her; long '
        'black hair; a precise, almost kind face with pale-cyan eyes; in one gloved hand a slim glassworker\'s lancet of '
        'clear skyglass, the other hand open at her side. Accent: skyglass cyan.')
av_scaffold('ME01', 'Sayo, Mother of Echoes', 'fJLcH1mpB1XHHGtNWwvzD', 'avatar_moe_sayo.webp', SAYO,
            'Act I. Generate FIRST: it locks Sayo\'s design. Her glass hems are allowed for her alone. ME03 and ME04 '
            'attach the approved raw of this card as SUBJECT (one design, three looks).')
av_fx('ME02', 'The Silence', 'IhNR-W1FElTsrWw1KfuQ9', 'avatar_moe_silence.webp',
      'The Silence, an ancient stillness from the deep mountain, not a person: a tall, faceless shape of flat, matte '
      'ink-black darkness with a soft, absolute outline, like a hole cut out of the picture in the rough shape of a '
      'hooded figure; no inner detail. Long pale bone-white feelers trail from its lower edge like roots, and a few '
      'motes of pale dust hang frozen beside it. No face, no eyes, no mouth, no hands. Dread, not monstrousness.',
      'Act I boss. Keep the dark mass flat and solid; it must read as a lack, not a ghost, demon or cloak with a face.')
SAYO_ALT = (('ME01_approved.png', "SUBJECT: Sayo, Mother of Echoes as approved; keep her face, build, coat cut and "
             "lancet exactly, change only what the Subject says"), CREW)
av_scaffold('ME03', 'Sayo, Glasswright of the Stilling', 'H3pNj2qUWpMpVRINiH6Vn', 'avatar_moe_sayo-stilling.webp',
            'the same woman as the attached Sayo, now at the Stilling: her skyglass hems have climbed to her waist and '
            'up one sleeve, the glass cut with thin, straight etched lines like a castle\'s floor plan; she holds the '
            'lancet point-down like a scribe\'s stylus; her hair is tied back hard; her face is focused and cold. '
            'Accent: skyglass cyan with a thin pale-gold glint along the etched lines.',
            'Act II (the Etching cycles). Starts only after ME01 is approved.', files=SAYO_ALT)
av_scaffold('ME04', 'Sayo, Saint of Stillness', 'k0hgSrghl_KcYs9ATVDJT', 'avatar_moe_saint.webp',
            'the same woman as the attached Sayo after she gives herself to the Silence: the skyglass on her coat has '
            'gone dark from the inside, near-black, with pale-cyan light only in a few thin cracks; pale bone-white '
            'root-like feelers trail from her hems; her hair hangs perfectly still; her eyes are closed and serene, '
            'both hands open at her sides, the lancet gone. Accent: a thin pale-cyan crack light.',
            'Act III. Starts only after ME01 is approved. Must read as the same woman, ended.', files=SAYO_ALT)
av_fx('ME05', 'A Feeler of the Deep', 'qFKcwTUkBtRiC-uM_8xG8', 'avatar_moe_feeler.webp',
      'one pale feeler of the Silence rising from below: a single tall bone-white root-like tendril, thick at the base '
      'and tapering, its tip curled as if listening, with small dark knots along it and a few motes of pale dust frozen '
      'in the air around it. No face, no eyes, no mouth.',
      'Summon (The Listening). Keep the base cut off flat at the bottom edge so it stands, not floats.')
av_scaffold('ME06', 'Your Likeness', 'zyOeF-rSpeXuMU7A3QQgo', 'avatar_moe_likeness.webp',
            'Your Likeness: a shinobi-shaped echo the glass makes of whoever it faces, a lean figure in a plain hooded '
            'wrap and cloth mask whose whole surface is silvered mirror-glass, faceless under the hood, with thin '
            'pale-cyan facet lines across the body like a cut gem; a plain kunai in one hand. Accent: skyglass cyan.',
            'Summon (Your Likeness, Stolen Form). Generic on purpose: it stands for the player.', prio='P1')
WORN = (' one of the Worn, an afterimage cast so many times there is almost nothing left: colours faded and washed out '
        'toward grey, the outline broken and missing in places like worn paint, eyes lit by a faint pale chakra.')
av_scaffold('ME07', 'The Gate Porter (Worn)', 'wivZbMygCZo6c9pRKWvCI', 'avatar_moe_worn-porter.webp',
            'The Gate Porter,' + WORN + ' A stooped old castle gate porter in a plain dark watchman\'s coat, a paper '
            'lantern on a short pole in one hand and a heavy iron-studded club in the other. Accent: lantern amber.',
            'Summon (Raise the Gate Porter). ME07-ME09 share the Worn treatment: judge ME08 and ME09 against ME07.', prio='P1',
            files=(CREW, ECHO))
av_scaffold('ME08', 'Sister Hana (Worn)', 'g6bNcftMcQ9pV_nMki7Wv', 'avatar_moe_worn-hana.webp',
            'Sister Hana,' + WORN + ' A young castle infirmary sister in a plain grey medic\'s kimono and white apron, '
            'sleeves tied back, a roll of bandages held in both hands. Accent: faded rose.',
            'Summon (Raise Sister Hana). Accent is rose, not green: the scaffold keys on lime.', prio='P1',
            files=(CREW, ECHO))
av_scaffold('ME09', 'Cadet Tomo (Worn)', 'KhFglnxE7ouIDywet3BPB', 'avatar_moe_worn-tomo.webp',
            'Cadet Tomo,' + WORN + ' A young castle cadet in an oversized dark training uniform and a too-big padded '
            'cap, a wooden practice sword held in both hands; an earnest, lost face. Accent: faded indigo.',
            'Summon (Raise Cadet Tomo). Keep him clearly young and non-threatening: a wooden sword, no blade.', prio='P1',
            files=(CREW, ECHO))

# ------------------------------------------------------------------------------------------------ scenes (scaffold)
SC_T = SPEC['targets']['SCENE_BACKGROUND']
QUEST = 'IBPNwhAzlAJPXoeEnp8gW'


def scene(code, name, deliver, subject, note, prio, files=(SCENE_REF, SCENE_REF2), nodes=''):
    r = shotlist.render_prompt(SPEC, 'SCENE_BACKGROUND', subject=subject)
    lines = [f"Target: {name}, one scene background for The Ninja RPG's Skyglass uber fight, The Mother of Echoes.",
             refs(files), r['positive'], f"Negative: {r['negative']}", END]
    card(code, name, 'Scenes', f"{name} · SCENE_BACKGROUND (`sceneBackground`, a gameAsset) · {SC_T['aspect']['value']}, "
         f"no key · deliver {SC_T['delivered_width_px']}px wide, {SC_T['format']} {SC_T['format_mode']}", files,
         f'{code}_raw_{deliver[:-5]}.png', deliver, note + ' ' + r['reserve_note'], lines, prio,
         'spec.prompt_scaffolds.SCENE_BACKGROUND via shotlist.render_prompt', [f'quest {QUEST} {nodes}'.strip()])


scene('ME10', 'The Heart of the Mother Glass', 'scene_bg_moe_heart_of_the_mother_glass.webp',
      'a vast cavern deep beneath an Edo mountain castle, its walls a single sheet of dark glass veined with pale-cyan '
      'light, hundreds of small pale lights suspended inside the glass like lanterns under ice, a smooth dark glass '
      'floor, thick pale roots of glass rising from below at the far right where the light falls away into flat darkness',
      'Act I, the opening and the quest\'s top-level scene (the travel popup shows only this one, law 25). Generate first; '
      'ME11 and ME12 attach it.', 'P1', nodes='content, d_open, b_act1, f_lost')
LAYOUT = ('ME10_approved.png', 'STYLE AND LAYOUT: the same cavern; keep its walls, floor and framing, change only what the text says')
scene('ME11', 'The Heart of the Mother Glass, the Stilling', 'scene_bg_moe_the_stilling.webp',
      'the same glass cavern dimmed almost to darkness, the pale lights inside the walls gone still and faint, and the '
      'glass floor scored with thin straight glowing pale-gold lines like the etched floor plan of a castle\'s rooms',
      'Act II. If short of time, Act II reuses ME10 (fallback).', 'P2', files=(LAYOUT, SCENE_REF), nodes='d_act2, b_act2')
scene('ME12', 'The Heart of the Mother Glass, A Good Impression', 'scene_bg_moe_a_good_impression.webp',
      'the same glass cavern breaking apart: great cracks through the walls and floor, ink-black stillness hanging out '
      'of the cracks like smoke frozen in place, shards of glass suspended motionless in the air, the lights in the '
      'walls gone dark',
      'Act III and the win node. If short of time, Act III reuses ME10 (fallback).', 'P2', files=(LAYOUT, SCENE_REF),
      nodes='d_act3, b_act3, w_clear')

# ------------------------------------------------------------------------------------------------ icons (Skyglass IC/VT/VS cards)


def icon(code, name, records, deliver, subject, note, prio='P1', files=(ICON_REF,), family='Icons', target_kind='ICON (`item.image`)'):
    lines = [f'Target: {name}, one square game item icon for The Ninja RPG.', refs(files), sky('IC08', 'Style'),
             sky('IC08', 'Framing'), f'Subject: {subject}', sky('IC08', 'Background'), sky('IC08', 'Avoid'), END]
    card(code, name, family, f'{name}, {records} · {target_kind} · lime key or alpha', files,
         f'{code}_raw_{deliver[:-5]}.png', deliver, note, lines, prio,
         'SKYGLASS_ART_PROMPTS.md IC card lines (IC08)', [records])


icon('ME13', 'The Mother of Echoes (quest icon)', f'quest `{QUEST}`', 'quest_icon_mother_of_echoes.webp',
     'The Mother of Echoes: the Mother Glass itself, held as an object. A tall, faceted seed of dark skyglass, '
     'narrow at both ends, pale-cyan light deep inside it, its lower end gripped by a few thick pale bone-white roots '
     'that curl round it; one fine crack runs up its face. Legendary: no tier seal.',
     'quest.image (a raw URL, no gameAsset). Generate before the shards: it sets the fight\'s look for the icon set.',
     target_kind='ICON (`quest.image`)')
SHARD_NOTE = ('The four shards are one object broken four ways: the same dark skyglass, the same cut, each carrying a '
              'trace of where it was found. Already dropping live with the engine default icon. Legendary: no tier seal.')
for code, nm, rid, sub in (
        ('ME14', 'Shard of the Keel', 'uKnlqlfyE_k1QjLuaVml_',
         'Shard of the Keel: one long sliver of dark, near-black skyglass with pale-cyan light inside it, its broad end '
         'still bound to a splinter of blackened ship\'s keel timber by a few turns of tarred rope.'),
        ('ME15', 'Shard of the Crown', '4UNvgWIDGD9QpNVtLr1aM',
         'Shard of the Crown: one jagged frost-point of dark skyglass with pale-cyan light inside it, broken from a '
         'crown; its base keeps a small curved band of storm-grey iron.'),
        ('ME16', 'Shard of the Tide', 'KHGZAfQFosLQJ29AN2ymC',
         'Shard of the Tide: one smooth, wave-worn sliver of dark skyglass with pale-cyan light inside it, a crust of '
         'dried sea salt along one edge and a strand of dark seaweed caught round it.'),
        ('ME17', 'Shard of the Ledger', 'cGrmhfe88ACBvFk2XqvSu',
         'Shard of the Ledger: one flat sliver of dark skyglass with pale-cyan light inside it, a torn scrap of '
         'yellowed ledger paper pressed into its surface with faded, unreadable brush strokes.')):
    icon(code, nm, f'item `{rid}`', 'icon-' + nm.lower().replace(' ', '-') + '.webp', sub,
         SHARD_NOTE + (' Generate ME14 first and judge ME15-ME17 against it.' if code == 'ME14' else ''))


def token(code, name, rid, deliver, motif, note):
    files = (TOKEN_BASE, TOKEN_ALT)
    lines = [f'Target: {name}, a boss variant token, one square game item icon for The Ninja RPG.', refs(files),
             sky('VT01', 'Style'), sky('VT01', 'Framing'),
             'Subject: the attached iron trophy tag, unchanged: same shape, iron, rivets, cord, angle, size and colours. '
             'Only the oval skyglass window changes: set into it, engraved and inlaid in pale cyan skyglass with dark '
             f'lines, {motif}. The motif fills the window and stays inside it; nothing else is added.',
             sky('VT01', 'Background'), sky('VT01', 'Avoid'), END]
    card(code, name, 'Icons', f'{name}, item `{rid}` · ICON (`item.image`) · Legendary; no seal · lime key', files,
         f'{code}_raw_{deliver[:-5]}.png', deliver, note, lines, 'P1',
         'SKYGLASS_ART_PROMPTS.md VT card (VT01 lines; the VT00_approved.png base)', [f'item {rid}'])


token('ME18', 'Heartglass (token)', 'FmQgVG5IX3q607wcHcOGy', 'icon-variant-token-heartglass.webp',
      'a small open folding fan whose leaves are panes of glass, a heart-shaped glass charm at its pivot',
      'Motif follows the final Heartglass variant (art/skyglass_variant_skins/exports/icon-variant-heartglass.webp). '
      'Drops on every clear (25%).')
token('ME19', 'The Remainder (token)', 'xCAtBCvbA2-TTV2eSe-jx', 'icon-variant-token-the-remainder.webp',
      'a small bow drawn as a flat black silhouette, pale root-like filaments trailing from its tips',
      'Motif must follow the director\'s The Remainder variant (ME20) once approved; adjust the motif words to it. '
      'Drops on every clear (25%).')
VS_FILES = (('base_ink_of_the_void.png', 'SUBJECT: the live Ink of the Void icon; keep its core form, proportions and '
             'angle so the weapon is recognisable; its colours and details change as the Subject says'),
            ('material_skyglass_crystal.png', 'MATERIAL-ONLY: how skyglass looks as an inlay; do not copy its shape'))
card('ME20', 'The Remainder', 'Icons',
     'The Remainder, item variant `f1trw5TAP7ItE-E7eh8b0` on Ink of the Void · ICON (item-variant image) · no tier seal · lime key',
     VS_FILES, 'ME20_raw_icon-variant-the-remainder.png', 'icon-variant-the-remainder.webp',
     'IN PROGRESS with the director (his own session); this card is kept so the token (ME19) and any regeneration '
     'share one description. Zip folder `15_variant_ink_of_the_void/` of skyglass_art_refs.zip.',
     ['Target: The Remainder, a skin of the weapon Ink of the Void, one square game item icon for The Ninja RPG.',
      refs(VS_FILES), sky('VS06', 'Style'), sky('VS06', 'Framing'),
      'Subject: The Remainder. Keep the attached Ink of the Void\'s core form, proportions and angle so it is '
      'recognisably the same weapon, then restyle it boldly so it reads as a new skin at 125 px: both limbs become flat '
      'matte ink-black stillness with no shine at all, as if cut out of the picture; no visible bowstring glint; pale '
      'bone-white root-like filaments trailing from the tips; a few motes of pale dust hanging frozen beside the grip. '
      'Add a thin pale-cyan edge light along the whole outline.',
      'It must read clearly apart from its sibling skin on the same base (Stargazer: parchment-white limbs inlaid with '
      'cyan chart lines, rigging-rope string and a brass compass charm); do not use that design.',
      sky('VS06', 'Background'), sky('VS06', 'Avoid'), sky('VS06', 'Thumbnail test'), END],
     'P1', 'SKYGLASS_ART_PROMPTS.md VS card (VS06 lines)', ['itemVariant f1trw5TAP7ItE-E7eh8b0'])

# ------------------------------------------------------------------------------------------------ jutsu icon families (Skyglass JI)
JI_FAMILIES = [
    ('ME21', 'Glass Lancet', 'jutsu_moe_fam_lancet.webp',
     ['Glass Lancet', 'The Glass Remembers', 'Lucid'],
     "Sayo's own hand: a needle of skyglass thrown hard, and the glass's memory turned on the room.",
     'one long, thin needle of clear skyglass, white-hot at its point, flying diagonally across the square',
     'side-on, the needle crossing from lower left to upper right, its point nearest the upper corner',
     'a short trail of fine pale-cyan glass dust behind it'),
    ('ME22', 'Refraction', 'jutsu_moe_fam_refraction.webp',
     ['Refraction', 'Far Refraction', 'Facet', 'Refraction Breaks', 'Far Refraction Breaks', 'Facet Breaks',
      'Lucid Refraction', 'Every Name in the Glass', 'The Names Flood In'],
     'Light caught in a prism and broken into lines across the floor, then the lines burst (marked rows and fields that erupt).',
     'one faceted skyglass prism in the centre, a single beam entering it and three hard-edged beams fanning out',
     'front-on, the beams spreading toward the lower edge of the square',
     'small ember-red sparks where the outgoing beams end (the eruption to come)'),
    ('ME23', 'Etching', 'jutsu_moe_fam_etching.webp',
     ['Etching: Rime', 'Etching: Ember', 'Etching: Seam', 'Etching: Heart', 'Etching: Hail',
      'Recast: Rime', 'Recast: Ember', 'Recast: Seam', 'Recast: Heart', 'Recast: Hail'],
     'Sayo scores a pattern into the glass floor; turns later, the pattern is recast as rising blades (a memory test).',
     'a pane of dark glass seen from above at an angle, scored with a lattice of thin pale-gold lines, three slim '
     'glass blades rising from where the lines cross',
     'three-quarter view from above, the pane filling the lower two thirds of the square',
     'a fine gold scribe-spark at the end of one line, still cutting'),
    ('ME24', 'Glassfall', 'jutsu_moe_fam_glassfall.webp',
     ['Shatterfall', 'Shatterfall Gives Way', 'Glassfall: First Pane', 'Glassfall: Second Pane',
      'Glassfall: Last Pane', 'Glassfall: Opening Pane', 'Glassfall: Heart Recast'],
     'Panes of the Mother Glass come down on marked ground.',
     'a fan of five long sharp panes of falling skyglass, points down, spread like a hand of cards',
     'front-on, falling straight down toward the lower edge',
     'a thin line of shattered glints along the lower edge where the first point lands'),
    ('ME25', 'The Hush', 'jutsu_moe_fam_hush.webp',
     ['The Hush', 'The Hush, Unbridled', 'The Hush Rises', 'Hush Where They Refused', 'No One Is Mended',
      'The Quiet', 'The Long Hush', 'The Glass Falls Quiet', 'Stillness', 'Nothing Moves', 'The Held Breath',
      'Breathless Pull', 'The Listening', 'The Listening, Unbridled', 'Cradle', 'Grasp'],
     'The Silence: pools that drink healing, stillness that stuns, and pale feelers that listen and hold.',
     'one flat pool of matte ink-black stillness seen from an angle, a single pale bone-white feeler rising out of it '
     'and curling at the tip',
     'three-quarter view from above, the pool low in the square, the feeler rising through the centre',
     'a few motes of pale dust hanging frozen in the air above the pool'),
    ('ME26', 'Echoes', 'jutsu_moe_fam_echoes.webp',
     ['Your Likeness', 'Your Own Strike', 'Raise the Gate Porter', 'Raise Sister Hana', 'Raise Cadet Tomo',
      'Doorward Sweep', 'Worn Mending', "Cadet's Tether"],
     "Afterimages Sayo casts from the stilled: your own likeness, and the Worn of Crownhold.",
     'one tall pane of skyglass standing upright, a faded pale outline pressed against it from inside like a reflection '
     'that has stayed, its edge already cracking where it steps out',
     'front-on, the pane upright in the centre',
     'thin pale-cyan cracks spreading from the pane\'s lower corner'),
]
JIDS = json.load(open(os.path.join(HERE, 'mother_of_echoes_record_ids.json')))['jutsu']
for code, fam, deliver, names, action, dom, cam, sec in JI_FAMILIES:
    files = (JI_REF, JI_FAM)
    lines = [f'Target: {fam}, one square jutsu icon for The Ninja RPG, shared by the {fam} family of AI-only boss '
             'techniques in The Mother of Echoes.', refs(files), sky('JI01', 'Style'), f'Action: {fam}: {action}',
             f'Dominant silhouette: {dom}.', f'Camera and motion: {cam}.', f'Secondary effect: {sec}.',
             sky('JI01', 'Palette'), sky('JI01', 'Background'), sky('JI01', 'Avoid'), END]
    card(code, f'{fam} (jutsu family icon)', 'Jutsu icons',
         f'{fam} family, {len(names)} AI jutsu · JUTSU_ICON (`jutsu.image`) · designed background, no key', files,
         f'{code}_raw_{deliver[:-5]}.png', deliver,
         'Covers: ' + '; '.join(f'{n} `{JIDS[n]}`' for n in names) + '. Each family must read apart from the other '
         'five at 125 px. Export with --type JUTSU_ICON.', lines, 'P2', 'SKYGLASS_ART_PROMPTS.md JI card lines (JI01)',
         [JIDS[n] for n in names])

# ------------------------------------------------------------------------------------------------ FX raw layers (Skyglass AN)


def fx(code, name, deliver, subject, note, prio, records):
    files = (FX_REF,)
    lines = [f"Target: one raw animation layer for The Ninja RPG's Skyglass uber fight, The Mother of Echoes: {name}.",
             refs(files), sky('AN01', 'Style'), sky('AN01', 'Canvas'), f'Subject: {subject}', sky('AN01', 'Background'),
             sky('AN01', 'Avoid'), END]
    card(code, name, 'Animation raw layers', f'{name} · ANIMATION raw layer · 1254 x 1254, magenta key or alpha', files,
         f'{code}_raw_{deliver}', deliver, note, lines, prio, 'SKYGLASS_ART_PROMPTS.md AN card lines (AN01)', records)


fx('ME27', 'moe_cradle: Cradle (folding dark)', 'raw_fx_moe_cradle.png',
   'two great soft folds of flat matte ink-black darkness curving inward from left and right like closing wings or '
   'cupped hands, leaving a clear open space between them, a few motes of pale dust frozen at their edges.',
   'Buff loop on the protected boss (decreasedamagetaken staticAnimation). Claude animates it in code '
   '(art/mother_of_echoes_fx) as a slow fold-and-breathe loop that frames the portrait, then uploads.', 'P2',
   ['Cradle DFcbOLSvYssjLzTHo_dw0'])
fx('ME28', 'moe_flood: The Names Flood In (faces alight)', 'raw_fx_moe_flood.png',
   'a tight cluster of small pale masks of light with closed eyes, rising together like paper lanterns, white-cyan '
   'edge light on each; each mask is a plain smooth oval with no features but closed eyes.',
   'OPTIONAL upgrade. The Names Flood In ships with the live Skyglass Eruption; this would be its signature version. '
   'Faces are masks of light, not people.', 'P3', ['The Names Flood In 4_dlB0conB-C6sfYqiU6Q'])

# ------------------------------------------------------------------------------------------------ write


def md():
    fam_order = ['Avatars', 'Scenes', 'Icons', 'Jutsu icons', 'Animation raw layers']
    out = ['# The Mother of Echoes: art prompts, one paste-ready block per asset', '',
           '- **For:** the art director (ChatGPT generates; Claude does intake, processing and upload manifests afterwards).',
           '- **Asset list, priorities and what is built in code or reused:** `docs/design/MOTHER_OF_ECHOES_ART.md`.',
           '- **Generated by** `docs/handoffs/mother_of_echoes_art_prompts.py`; do not hand-edit. AI_AVATAR and '
           'SCENE_BACKGROUND blocks are the spec scaffolds rendered by `shotlist.py render_prompt` (house style '
           'verbatim, only the subject written); every other block reuses the fixed lines of the named card in '
           '`SKYGLASS_ART_PROMPTS.md` verbatim (the script docstring says why per type).',
           '- **Protocol:** `docs/workflows/ISOLATED_ART_GENERATION.md`. **Live-game requests/writes:** 0. **Credentials:** none.',
           '', '## How to use', '',
           '1. Open a **fresh chat for each asset**; paste exactly one block (the text inside the fence) and nothing else.',
           '2. Attach **only the files the card names**, each as its own image (never a folder or a sheet). Repo paths '
           'are under `perseverance484/tnr-tools`; bare names (`VT00_approved.png`, `base_ink_of_the_void.png`, '
           '`material_skyglass_crystal.png`) are in `skyglass_art_refs.zip`.',
           '3. Generate **one candidate at a time**; approve, reject, or ask for a same-subject revision.',
           '4. **Two wrong-subject or wrong-composition results: close the chat** and start again with the same block.',
           '5. Return each **approved original unprocessed**, named by its code (`ME01_raw_...`).',
           '6. Order: **P1 first**, in the order below. ME01 before ME03/ME04 (save it as `ME01_approved.png`); ME10 '
           'before ME11/ME12 (save as `ME10_approved.png`); ME14 before ME15-ME17; ME20 before ME19.', '',
           '## Index', '', '| Code | Asset | Priority | Delivery file |', '|---|---|---|---|']
    for c in CARDS:
        out.append(f"| {c['code']} | {c['name']} | {c['priority']} | `{c['deliver']}` |")
    out.append('')
    out.append(f'**Total:** {len(CARDS)} cards: ' + ', '.join(
        f"{p} {sum(1 for c in CARDS if c['priority'] == p)}" for p in ('P1', 'P2', 'P3')) + '.')
    out.append('')
    for fam in fam_order:
        cs = [c for c in CARDS if c['family'] == fam]
        out += [f'## {fam}', '']
        for c in cs:
            att = '; '.join(f"`{f['f']}` ({f['role']})" for f in c['files'])
            out += [f"### {c['code']} · {c['name']}", '',
                    f"- **Target:** {c['target']} · priority: **{c['priority']}**",
                    f'- **Attach:** {att}', f"- **Return as:** `{c['ret']}` (delivery file `{c['deliver']}`)"]
            if c['note']:
                out.append(f"- **Note:** {c['note']}")
            out.append(f"- **Prompt source:** {c['source']}")
            out += ['', '```text', c['prompt'], '```', '']
    return '\n'.join(out)


if __name__ == '__main__':
    with open(os.path.join(HERE, 'MOTHER_OF_ECHOES_ART_PROMPTS.md'), 'w') as fh:
        fh.write(md())
    with open(os.path.join(HERE, 'mother_of_echoes_art_prompts.json'), 'w') as fh:
        json.dump({'generator': 'docs/handoffs/mother_of_echoes_art_prompts.py', 'cards': CARDS}, fh, indent=1, ensure_ascii=False)
        fh.write('\n')
    bad = [c['code'] for c in CARDS if '[STYLE]' in c['prompt'] or '[SUBJECT]' in c['prompt']]
    assert not bad, bad
    print(len(CARDS), 'cards')
