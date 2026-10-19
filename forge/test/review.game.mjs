// Socket-free model of the content review desk (src/review/contract.json): create records a
// PENDING suggestion of the fields that differ from the live row, refuses "Nothing changed",
// and answers getQueue/getProposal in the shapes contentReview.ts returns.
import { FakeGame, nanoidLike } from "./fakegame.mjs";

const ROUTER = { JUTSU: "jutsu", ITEM: "item", BLOODLINE: "bloodline", QUEST: "quest", GAME_ASSET: "asset", AI: "ai" };

export class ReviewGame extends FakeGame {
  constructor(o) { super(o); this.proposals = []; this.dropCreateResponse = false; this.failQueue = 0; }
  handle(path, input) {
    if (!path.startsWith("contentReview.")) return super.handle(path, input);
    this.calls.push({ path, input: structuredClone(input) });
    const ok = (data) => ({ ok: true, data });
    if (this.signedOut) return { ok: false, error: { code: "UNAUTHORIZED", httpStatus: 401, message: "UNAUTHORIZED", path, zodError: null } };
    if (path === "contentReview.create") {
      const row = this.tables[ROUTER[input.entityType]].get(input.entityId);
      if (!row) return ok({ success: false, message: "Jutsu not found" });
      const after = Object.fromEntries(Object.entries(input.data).filter(([k, v]) => JSON.stringify(row[k]) !== JSON.stringify(v)));
      if (!Object.keys(after).length) return ok({ success: false, message: "Nothing changed compared to the live version" });
      this.proposals.push({ id: nanoidLike(), source: "STAFF", title: input.title, category: input.category, status: "PENDING", rationale: input.rationale,
        targets: [{ entityType: input.entityType, entityId: input.entityId, operation: "UPDATE", fields: Object.keys(after) }], after });
      if (this.dropCreateResponse) { this.dropCreateResponse = false; throw new TypeError("Failed to fetch"); }
      return ok({ success: true, message: "Sent for review" });
    }
    if (path === "contentReview.getQueue") {
      if (this.failQueue > 0) { this.failQueue--; return { ok: false, error: { code: "INTERNAL_SERVER_ERROR", httpStatus: 500, message: "boom", path, zodError: null } }; }
      const rows = this.proposals.filter((p) => p.status === input.status && (!input.source || p.source === input.source) && (!input.entityType || p.targets.some((t) => t.entityType === input.entityType)));
      const start = input.cursor ?? 0, page = rows.slice(start, start + (input.limit ?? 25));
      return ok({ items: page, nextCursor: start + page.length < rows.length ? start + page.length : null, canReview: true });
    }
    if (path === "contentReview.getProposal") return ok(this.proposals.find((p) => p.id === input.id) ?? null);
    return { ok: false, error: { code: "NOT_FOUND", httpStatus: 404, message: "no such procedure", path, zodError: null } };
  }
}
