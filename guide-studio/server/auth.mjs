import { createRemoteJWKSet, jwtVerify, importJWK, SignJWT } from "jose";
export function accessVerifier({ domain, audience, trustedKeys }) {
  if (
    !domain ||
    !audience ||
    !/^https:\/\/[a-z0-9-]+\.cloudflareaccess\.com$/.test(domain)
  )
    throw Error("Staff authentication is not configured");
  const keys =
    trustedKeys ||
    createRemoteJWKSet(new URL(domain + "/cdn-cgi/access/certs"));
  return async (request) => {
    const token = request.headers.get("Cf-Access-Jwt-Assertion");
    if (!token) throw Error("Staff sign-in required");
    const { payload } = await jwtVerify(token, keys, {
      issuer: domain,
      audience,
      algorithms: ["RS256"],
    });
    if (!payload.sub) throw Error("Missing staff identity");
    return { id: payload.sub };
  };
}
export function approvalSigner(privateJwk) {
  return async (claims) => {
    const jwk = JSON.parse(privateJwk),
      key = await importJWK(jwk, "EdDSA");
    return new SignJWT(claims)
      .setProtectedHeader({ alg: "EdDSA", kid: jwk.kid })
      .setIssuer("tnr-guide-studio")
      .setAudience("tnr-guide-importer")
      .setIssuedAt()
      .sign(key);
  };
}
export function turnstileVerifier({ secret, hostname }, fetcher = fetch) {
  return async (token) => {
    if (!secret || !hostname) throw Error("Submissions are not configured");
    if (typeof token !== "string" || !token || token.length > 2048)
      throw Error("Complete the submission verification");
    const response = await fetcher(
      "https://challenges.cloudflare.com/turnstile/v0/siteverify",
      {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ secret, response: token }),
      },
    );
    const result = await response.json();
    if (
      !result.success ||
      result.hostname !== hostname ||
      result.action !== "guide-submit"
    )
      throw Error("Submission verification failed. Try again.");
  };
}
