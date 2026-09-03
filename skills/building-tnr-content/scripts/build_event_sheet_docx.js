const fs = require('fs');
const {
  Document, Packer, Paragraph, TextRun, HeadingLevel, AlignmentType,
  BorderStyle, Table, TableRow, TableCell, WidthType, ShadingType,
  LevelFormat, convertInchesToTwip
} = require('docx');

const ACCENT = '7B2D26';
const GREY = '666666';
const RULE = { color: 'BFBFBF', space: 6, style: BorderStyle.SINGLE, size: 6 };

// A blank write-on line.
function line(count = 1) {
  const out = [];
  for (let i = 0; i < count; i++) {
    out.push(new Paragraph({
      spacing: { before: 40, after: 160 },
      border: { bottom: RULE },
      children: [new TextRun({ text: '', size: 22 })],
    }));
  }
  return out;
}

// Bold label, optional italic grey hint, then a write-on line.
function field(label, hint, lines = 1) {
  const runs = [new TextRun({ text: label, bold: true, size: 22 })];
  if (hint) runs.push(new TextRun({ text: '  ' + hint, italics: true, color: GREY, size: 20 }));
  return [
    new Paragraph({ spacing: { before: 160, after: 0 }, children: runs }),
    ...line(lines),
  ];
}

function h1(text) {
  return new Paragraph({
    heading: HeadingLevel.HEADING_1,
    spacing: { before: 360, after: 120 },
    border: { bottom: { color: ACCENT, space: 4, style: BorderStyle.SINGLE, size: 12 } },
    children: [new TextRun({ text, bold: true, size: 26, color: ACCENT })],
  });
}

function body(text, opts = {}) {
  return new Paragraph({
    spacing: { before: opts.before ?? 0, after: opts.after ?? 120 },
    children: [new TextRun({ text, size: 22, italics: !!opts.italics, bold: !!opts.bold })],
  });
}

// Indented italic guidance block with an accent left border.
function note(lines) {
  return lines.map((t, i) => new Paragraph({
    spacing: { before: i === 0 ? 200 : 0, after: i === lines.length - 1 ? 200 : 80 },
    indent: { left: convertInchesToTwip(0.25) },
    border: { left: { color: ACCENT, space: 10, style: BorderStyle.SINGLE, size: 12 } },
    children: [new TextRun({ text: t, size: 20, italics: true, color: '333333' })],
  }));
}

function tick(text) {
  return new Paragraph({
    spacing: { after: 60 },
    indent: { left: convertInchesToTwip(0.25) },
    children: [new TextRun({ text: '\u2610   ' + text, size: 22 })],
  });
}

function bullet(text) {
  return new Paragraph({
    numbering: { reference: 'sheet-bullets', level: 0 },
    spacing: { after: 80 },
    children: [new TextRun({ text, size: 22 })],
  });
}

// ---- Enemy table -------------------------------------------------------
const COLS = [1900, 1150, 2100, 2610, 1600]; // sums to 9360
const HEADERS = ['Name', 'Element', 'Role', 'Who they are, in one line', 'Signature move idea'];

function cell(text, { header = false, width } = {}) {
  return new TableCell({
    width: { size: width, type: WidthType.DXA },
    shading: header ? { type: ShadingType.CLEAR, fill: 'F2EDEC' } : undefined,
    margins: { top: 80, bottom: 80, left: 100, right: 100 },
    children: [new Paragraph({
      children: [new TextRun({ text, bold: header, size: header ? 19 : 21 })],
    })],
  });
}

function enemyTable(rows = 5) {
  const body = [];
  body.push(new TableRow({
    tableHeader: true,
    children: HEADERS.map((h, i) => cell(h, { header: true, width: COLS[i] })),
  }));
  for (let r = 0; r < rows; r++) {
    body.push(new TableRow({
      children: COLS.map((w) => cell('', { width: w })),
    }));
  }
  return new Table({
    columnWidths: COLS,
    width: { size: 9360, type: WidthType.DXA },
    rows: body,
  });
}

// ---- Document ----------------------------------------------------------
const children = [];

children.push(new Paragraph({
  spacing: { after: 80 },
  children: [new TextRun({ text: 'TNR Event Design Sheet', bold: true, size: 40, color: ACCENT })],
}));
children.push(body('Fill in what you know and send it back. That is the whole process.', { after: 200 }));

children.push(bullet('Leave a field blank or write AI to let the builder decide.'));
children.push(bullet('Write NONE to deliberately leave something out. Blank and NONE are not the same.'));
children.push(bullet('Fields marked [BALANCE] are proposals. The Content Admin sets the final numbers.'));
children.push(bullet('Attach anything you have: reference images, a rough draft, a sketch, a moodboard.'));
children.push(bullet('Plain language only. You never need field names, numbers or code.'));
children.push(bullet('No franchise references. Original content only.'));

children.push(...note([
  'Your event is built hidden, shown to you and the Content Admin, and published only once it is approved.',
]));

// 1
children.push(h1('1.  Basics'));
children.push(...field('Event name:'));
children.push(...field('In one line, what does the player get to do or feel?'));
children.push(...field('Naming word:', '(a unique word stamped on every enemy and ability so nothing collides with existing content, e.g. "Drowned")'));
children.push(...field('What are you attaching?', '(images, draft, sketch, nothing)'));
children.push(new Paragraph({ spacing: { before: 160, after: 100 }, children: [new TextRun({ text: 'Shape', bold: true, size: 22 }), new TextRun({ text: '  (tick one)', italics: true, color: GREY, size: 20 })] }));
children.push(tick('A chain of fights climbing to a boss'));
children.push(tick('A story with dialog, choices and scripted battles'));
children.push(tick('A short loop players run over and over for rewards'));
children.push(tick('One big boss fight'));
children.push(tick('You decide from the idea'));
children.push(...field('When does it run?', '(always / a set window, give dates / you decide)'));

// 2
children.push(h1('2.  Who can play it'));
children.push(...field('Level range:', '[BALANCE]'));
children.push(...field('Rank requirement:', '(e.g. Chunin and up)'));
children.push(...field('Village restriction:', '(or blank for everyone)'));
children.push(...field('Must they finish something first?', '(name it, or blank)'));
children.push(...field('How often can they play it?', '(once, daily, unlimited)  [BALANCE]'));

// 3
children.push(h1('3.  Story'));
children.push(...field('Premise:', '(2 to 4 sentences: what is happening, why the player is involved)', 4));
children.push(...field('Where does it go?', '(locations, in order if that matters)', 2));
children.push(...field('Who is in it?', '(villain, NPCs, the boss; a name and one line each)', 4));
children.push(...field('Opening hook:', '(the first thing the player is told)', 2));
children.push(...field('If they win, what changed?', '', 2));
children.push(...field('If they lose, what does that look like?', '', 2));
children.push(...field('Tone:', '(grim, mysterious, heroic, comedic)'));
children.push(...note([
  'One thing worth checking before you send it: every character needs a reason for doing it this way, and a reason they did not do the obvious cheaper thing.',
]));

// 4
children.push(h1('4.  Enemies'));
children.push(...field('How many regulars, elites and bosses?'));
children.push(...field('How hard should it feel?', '(pushover / fair / hard / brutal)  [BALANCE]'));
children.push(...field('Anything existing this should reuse?'));
children.push(body('Add rows as needed. Any blank column is the builder\u2019s call. Roles: bruiser, caster, assassin, tank, support.', { before: 160, after: 120, italics: true }));
children.push(enemyTable(5));
children.push(...field('Boss behaviour wishes:', '(e.g. enrages when hurt, opens with a shield, calls for help, punishes players who stay close)', 2));

// 5
children.push(h1('5.  Abilities'));
children.push(new Paragraph({ spacing: { before: 120, after: 100 }, children: [new TextRun({ text: 'Enemy movesets', bold: true, size: 22 })] }));
children.push(tick('You design them from role and element (default)'));
children.push(tick('I have ideas, below'));
children.push(...field('Specific ability ideas:', '(what it does, who uses it)', 3));
children.push(...field('Should winning teach the player a new jutsu?', '(describe it, or NONE)  [BALANCE]', 2));

// 6
children.push(h1('6.  Battle structure'));
children.push(...field('How many fights start to finish?'));
children.push(...field('Any fights against more than one enemy at once?'));
children.push(...field('Order:', '(who comes first, who guards the boss)', 2));
children.push(...field('On a loss:', '(retry the fight / restart the run / hard fail / you decide)'));
children.push(...field('Anything between fights?', '(dialog, choices, pickups, travel)', 2));

// 7
children.push(h1('7.  Rewards   [BALANCE]'));
children.push(...field('How big should the payout feel?', '(small / standard / finale, or name a mission to match)'));
children.push(...field('Currency, exp, tokens:', '(or blank)'));
children.push(...field('Item drops:', '(a chest? specific items? something new?)', 2));
children.push(...field('Anything unique?', '(a badge, a title, a one-off item)'));

// 8
children.push(h1('8.  Look and feel'));
children.push(...field('Palette and motifs:', '(colors, imagery, materials; e.g. "drowned ships, sickly green light, rusted anchors")', 2));
children.push(...field('Reference images:', '(attach them and say what each is for: palette, boss, location)', 2));
children.push(...field('Backgrounds needed:', '(one per location, or let the builder derive them)', 2));
children.push(...field('Boss portrait in dialog?', '(yes / no / you decide)'));
children.push(...field('What should the event icon evoke?'));
children.push(...note([
  'Images set colour and material well. They do not reliably set composition, so describe the layout in words too.',
]));

// 9
children.push(h1('9.  Anything else'));
children.push(...field('Off limits:', '(themes, imagery or mechanics to avoid)', 2));
children.push(...field('Is there a date this needs to hit?', '(or leave blank)'));
children.push(...field('Anything else worth knowing?', '', 2));
children.push(...field('Your name:'));

const doc = new Document({
  numbering: {
    config: [{
      reference: 'sheet-bullets',
      levels: [{
        level: 0,
        format: LevelFormat.BULLET,
        text: '\u2022',
        alignment: AlignmentType.LEFT,
        style: { paragraph: { indent: { left: convertInchesToTwip(0.3), hanging: convertInchesToTwip(0.18) } } },
      }],
    }],
  },
  styles: {
    default: {
      document: { run: { font: 'Calibri', size: 22 } },
    },
  },
  sections: [{
    properties: {
      page: {
        size: { width: 12240, height: 15840 },
        margin: { top: 1440, bottom: 1440, left: 1440, right: 1440 },
      },
    },
    children,
  }],
});

Packer.toBuffer(doc).then((buf) => {
  fs.writeFileSync('/home/claude/EVENT_SHEET.docx', buf);
  console.log('written', buf.length, 'bytes');
});
