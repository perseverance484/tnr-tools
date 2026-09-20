// One error type for the presentation tooling, and the severities the lint reports.
//
// Everything in forge/presentation/ is repository-side: it reads committed evidence, derives a
// dossier and refuses to build one it cannot source. None of it is in forge_bundle.js and none of
// it opens a socket - see presentation/README.md for that boundary and the gate that holds it.

export class PresentationError extends Error {
  constructor(message, info = {}) {
    super(message);
    this.name = "PresentationError";
    Object.assign(this, info);
  }
}

/** A lint finding. `fatal` stops an export; `warn` is reported and does not. */
export const FATAL = "fatal";
export const WARN = "warn";

export function finding(severity, code, message, where = null) {
  return where ? { severity, code, message, where } : { severity, code, message };
}
