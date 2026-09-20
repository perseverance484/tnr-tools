// Remove comments from the BUILT bundle. The source keeps every word.
//
// Why this exists. esbuild at minify:false strips `//` line comments but preserves `/** ... */`
// blocks, so the shipped bundle was carrying ~34 KB raw / ~10 KB gzip of JSDoc that nothing at
// runtime reads. The Forge size pass was asked to find headroom without moving explanatory
// comments out of the code that needs them; stripping them from the ARTIFACT instead of from the
// SOURCE is strictly better than that trade - forge/src loses nothing, and the userscript the
// operator downloads stops paying for documentation only a reviewer reads.
//
// Why a tokenizer rather than a regex. A comment cannot be recognised without also recognising
// strings, template literals and regex literals: `"// not a comment"`, `` `${x /* here */}` ``
// and `/[/]/` all contain sequences a regex would mistake for one. This walks the text once in
// the four states that matter and tracks `${}` depth inside templates, which can nest.
//
// Why that is safe enough to ship. It is NOT trusted: build.mjs proves the result with esbuild
// itself, by transforming the original and the stripped text with minifyWhitespace (which removes
// comments and normalises whitespace through a real JS parser) and asserting the two normalise to
// the identical string. Anything this file removed that was not a comment - or any comment it
// removed that changed how the rest parsed - makes those two differ and fails the build. The
// bundle is therefore never shipped on this file's own say-so.

/**
 * Whether a `/` at `i` begins a regex literal rather than a division operator.
 *
 * Decided by the previous significant character, which is the standard heuristic: after a value
 * (identifier, number, `)`, `]`, a quote) a slash divides; after an operator, `(`, `,`, `=`, `:`,
 * `[`, `!`, `&`, `|`, `?`, `{`, `;` or one of the keywords below, it opens a regex.
 *
 * `}` is the known-ambiguous case (`}` can close a block, after which a regex may start, or an
 * object literal, after which it cannot). It is treated as "regex may start", which is the safe
 * direction here: reading a division as a regex would swallow text and the build oracle would
 * catch it immediately, whereas esbuild output does not contain `}` followed by a division.
 */
function regexAllowedAfter(text, i) {
  let j = i - 1;
  while (j >= 0 && /\s/.test(text[j])) j--;
  if (j < 0) return true;
  const c = text[j];
  if (/[)\]]/.test(c)) return false;
  if (/[\w$]/.test(c)) {
    let k = j;
    while (k >= 0 && /[\w$]/.test(text[k])) k--;
    const word = text.slice(k + 1, j + 1);
    // keywords a regex may legally follow; everything else ending in a word character is a value
    return /^(return|typeof|instanceof|in|of|new|delete|void|throw|case|do|else|yield|await)$/.test(word);
  }
  if (c === '"' || c === "'" || c === "`") return false;
  return true;
}

/**
 * Strip every comment from JavaScript source.
 *
 * Lines that consisted only of a comment are removed entirely; lines that were already blank are
 * kept, so the stripped bundle keeps the shape esbuild gave it instead of collapsing into a wall.
 *
 * @param {string} text  JavaScript source
 * @returns {string} the same source with comments removed
 */
export function stripComments(text) {
  let out = "";
  // lines that lost a comment, so a line left blank by stripping can be told from an originally
  // blank one and dropped
  const touched = new Set();
  let line = 0;
  let i = 0;
  const n = text.length;
  // depth of `${` inside template literals; templateStack tracks whether each nesting level is
  // currently inside the literal text or inside a substitution expression
  const templates = [];

  while (i < n) {
    const c = text[i];
    const next = text[i + 1];

    // ---- template literal TEXT -----------------------------------------------------------------
    // FIRST, before anything else: inside the text part of a template nothing is a comment, a
    // string or a regex, and the only characters that mean anything are a backslash, `${` and the
    // closing backtick. Checking this after the generic cases is the bug that made the first
    // version of this file read a CLOSING backtick as an opening one.
    if (templates.length && templates[templates.length - 1] === 0) {
      if (c === "\\") { out += text.slice(i, i + 2); i += 2; continue; }
      if (c === "$" && next === "{") { templates[templates.length - 1] = 1; out += "${"; i += 2; continue; }
      if (c === "`") { templates.pop(); out += c; i++; continue; }
      if (c === "\n") line++;
      out += c; i++;
      continue;
    }

    if (c === "\n") { out += c; line++; i++; continue; }

    // ---- comments ----------------------------------------------------------------------------
    if (c === "/" && next === "/") {
      touched.add(line);
      while (i < n && text[i] !== "\n") i++;
      continue;
    }
    if (c === "/" && next === "*") {
      touched.add(line);
      i += 2;
      while (i < n && !(text[i] === "*" && text[i + 1] === "/")) {
        if (text[i] === "\n") { out += "\n"; line++; touched.add(line); }
        i++;
      }
      i += 2;
      continue;
    }

    // ---- strings -----------------------------------------------------------------------------
    if (c === '"' || c === "'") {
      const quote = c;
      out += c; i++;
      while (i < n) {
        if (text[i] === "\\") { out += text.slice(i, i + 2); i += 2; continue; }
        if (text[i] === "\n") line++;            // only legal in a string via a line continuation
        out += text[i];
        if (text[i] === quote) { i++; break; }
        i++;
      }
      continue;
    }

    // ---- template literals -------------------------------------------------------------------
    // Only reached OUTSIDE template text, so this backtick always opens one (a nested template
    // inside a `${...}` substitution included).
    if (c === "`") {
      templates.push(0);
      out += c; i++;
      continue;
    }
    if (templates.length && c === "}") {
      // a `}` inside a substitution closes it only at depth 0 of that substitution's own braces
      const top = templates.length - 1;
      if (templates[top] === 1) { templates[top] = 0; out += c; i++; continue; }
      templates[top] -= 1;
      out += c; i++;
      continue;
    }
    if (templates.length && c === "{" && templates[templates.length - 1] >= 1) {
      templates[templates.length - 1] += 1;
      out += c; i++;
      continue;
    }

    // ---- regex literals ----------------------------------------------------------------------
    if (c === "/" && regexAllowedAfter(text, i)) {
      out += c; i++;
      let inClass = false;
      while (i < n) {
        const r = text[i];
        if (r === "\\") { out += text.slice(i, i + 2); i += 2; continue; }
        if (r === "\n") break;                   // unterminated: not a regex after all, bail safely
        out += r; i++;
        if (r === "[") inClass = true;
        else if (r === "]") inClass = false;
        else if (r === "/" && !inClass) break;
      }
      continue;
    }

    out += c; i++;
  }

  // drop the lines that stripping emptied, keep the ones that were already empty
  return out
    .split("\n")
    .filter((text_, idx) => !(touched.has(idx) && text_.trim() === ""))
    .join("\n");
}
