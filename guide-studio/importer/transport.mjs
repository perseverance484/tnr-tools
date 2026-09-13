import { createTRPCUntypedClient, httpBatchLink } from "@trpc/client";
import superjson from "superjson";
export function nativeTransport({ origin, fetcher = fetch }) {
  if (origin !== "https://www.theninja-rpg.com")
    throw Error("The native adapter only runs on the approved TNR origin.");
  const client = createTRPCUntypedClient({
    links: [
      httpBatchLink({
        url: origin + "/api/trpc",
        transformer: superjson,
        fetch: (url, options) =>
          fetcher(url, { ...options, credentials: "same-origin" }),
      }),
    ],
  });
  return {
    create: () => client.mutation("guide.create"),
    update: (input) => client.mutation("guide.update", input),
    get: (input) => client.query("guide.get", input),
    findBySlug: async (slug) => {
      const data = await client.query("guide.getAll", { includeDrafts: true });
      return data.find((g) => g.slug === slug) || null;
    },
  };
}
