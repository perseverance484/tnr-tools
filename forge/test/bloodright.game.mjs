// Socket-free model of the scoped source contract at 1ccdaf07. Independent of recipes/compiler.
import { FakeGame, nanoidLike, CrashSignal } from "./fakegame.mjs";
export class BloodrightGame extends FakeGame {
  constructor() { super(); this.skills = new Map(); this.folders = new Map(); this.hiddenAccess = true; this.roleAllowed = true; this.crashPath = null; }
  handle(path, input) {
    if (!path.startsWith("skillTree.")) return super.handle(path, input);
    const n = this.calls.push({ path, input: structuredClone(input) });
    const ok = data => ({ ok: true, data: structuredClone(data) });
    const err = (code, message) => ({ ok: false, error: { code, message } });
    const visible = r => this.hiddenAccess || (!r.hidden && !this.folders.get(r.folderId)?.hidden);
    if (this.limitPath === path) return err("TOO_MANY_REQUESTS", "rate limited");
    if (this.signedOut && /\.(create|update)/.test(path)) return err("UNAUTHORIZED", "UNAUTHORIZED");
    if (!this.roleAllowed && /\.(create|update)/.test(path)) return err("UNAUTHORIZED", "You are not authorized to create skills");
    let result;
    switch (path) {
      case "skillTree.get": result = ok(visible(this.skills.get(input.id) ?? {}) ? this.skills.get(input.id) : undefined); break;
      case "skillTree.getAll": {
        const rows = [...this.skills.values()].filter(r => r.pathType === (input?.pathType ?? "SKILL") && visible(r)).sort((a,b) => a.tier-b.tier || a.name.localeCompare(b.name));
        const cursor = input?.cursor ?? 0, limit = input?.limit ?? 50;
        const data = rows.slice(cursor * limit, (cursor + 1) * limit);
        result = ok({ data, nextCursor: data.length < limit ? null : cursor + 1 }); break;
      }
      case "skillTree.getAllFolders": result = ok([...this.folders.values()].filter(r => !r.hidden || input?.includeHidden && this.hiddenAccess)); break;
      case "skillTree.create": {
        if (!input?.bloodlineId) throw new Error("test requires BLOODRIGHT create input");
        const id = nanoidLike();
        this.skills.set(id, { id, name: `New Skill - ${id}`, description: "New skill description", image: "https://example.test/default.webp", target: "SELF", tier: 1, costSkillPoints: 1, requiredSkillIds: [], pathType: "BLOODRIGHT", bloodlineId: input.bloodlineId, seichiSilverCost: 0, hidden: true, skillType: "DEFAULT", folderId: null, effects: [] });
        result = ok({ success: true, message: id }); break;
      }
      case "skillTree.update": {
        const row = this.skills.get(input.id), d = input.data;
        if (!row || d.pathType !== row.pathType || d.skillType !== "DEFAULT" || !d.image) throw new Error("invalid skill update");
        if ([...this.skills.values()].some(r => r.id !== input.id && r.name.toLowerCase() === d.name.toLowerCase())) result = ok({ success: false, message: "Name already exists" });
        else if (d.requiredSkillIds.some(id => { const p = this.skills.get(id); return !p || p.tier >= d.tier || p.bloodlineId !== d.bloodlineId; })) result = ok({ success: false, message: "Invalid prerequisites" });
        else { Object.assign(row, structuredClone(d)); result = ok({ success: true, message: "Skill updated successfully" }); }
        break;
      }
      case "skillTree.createFolder": {
        const id = nanoidLike(); this.folders.set(id, { id, name: input.name, image: input.image || "", description: input.description || null, hidden: input.hidden || false, order: input.order || 0 });
        result = ok({ success: true, message: id }); break;
      }
      case "skillTree.updateFolder": {
        const d = input.data; Object.assign(this.folders.get(input.id), { name: d.name, image: d.image || "", description: d.description || null, hidden: d.hidden || false, order: d.order || 0 });
        result = ok({ success: true, message: "Folder updated successfully" }); break;
      }
      default: throw new Error("unexpected Bloodright procedure " + path);
    }
    if (this.crashPath === path || n >= this.crashAt && this.armed) { this.crashPath = null; this.armed = false; throw new CrashSignal(n); }
    return result;
  }
}
