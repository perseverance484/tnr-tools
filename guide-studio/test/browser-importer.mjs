import { mountImporter } from "../importer/panel.mjs";
const guides = new Map();
let n = 0;
const api = {
  create: async () => {
    const id = "mock-guide-" + ++n;
    guides.set(id, {
      id,
      slug: "new-guide-" + n,
      title: "New guide article",
      content: "<p>Write the guide here.</p>",
      category: "reference",
      published: false,
    });
    return { success: true, message: id };
  },
  update: async ({ id, data }) => {
    guides.set(id, { id, ...data });
    return { success: true, message: "Local mock update" };
  },
  get: async ({ id }) => guides.get(id),
  findBySlug: async (slug) => [...guides.values()].find((g) => g.slug === slug),
};
mountImporter({ api });
