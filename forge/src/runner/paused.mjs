// A job pause with its reason. Its own module so the reader and the MCP bridge can raise one
// (the run lock, RUL-2026-11-07-133) without importing the runner, which imports them.
export class Paused extends Error {
  constructor(reason, info = {}) { super(`paused: ${reason}`); this.name = "Paused"; this.reason = reason; Object.assign(this, info); }
}
