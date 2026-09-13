import registry from "../catalog/catalog.v1.json";
import { D1Store } from "./store.mjs";
import { createService } from "./service.mjs";
import { accessVerifier, approvalSigner, turnstileVerifier } from "./auth.mjs";
export default {
  async fetch(request, env) {
    if (!env.PUBLIC_ORIGIN || !env.DB || !env.ARTIFACTS)
      return new Response("Guide Studio is not configured", { status: 503 });
    try {
      return await createService({
        store: new D1Store(env.DB),
        bucket: env.ARTIFACTS,
        registry,
        origin: env.PUBLIC_ORIGIN,
        authenticate: accessVerifier({
          domain: env.ACCESS_DOMAIN,
          audience: env.ACCESS_AUDIENCE,
        }),
        verifyTurnstile: turnstileVerifier({
          secret: env.TURNSTILE_SECRET,
          hostname: new URL(env.PUBLIC_ORIGIN).hostname,
        }),
        signApproval: approvalSigner(env.APPROVAL_PRIVATE_JWK),
      })(request);
    } catch {
      return new Response("Service configuration is incomplete", {
        status: 503,
      });
    }
  },
};
