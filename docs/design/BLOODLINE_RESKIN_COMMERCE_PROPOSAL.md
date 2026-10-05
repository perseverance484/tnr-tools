# Bloodline Reskins — Commercial Cosmetic Entitlement Proposal

**Status:** PROPOSAL / NOT CANON / AWAITING USER RULINGS  
**Date:** 2026-10-05  
**Lead:** Content / System Design  
**Implementation owner if approved:** Fable / Claude Code  
**TNR Tools base:** `ad6044612ed516119852e925bba7b5a75516194c`  
**Game source inspected:** `studie-tech/TheNinjaRPG@2f5cf6bb5c0965e5834d3cf25db9ba3c07295cc5`  
**Live requests / writes:** 0 / 0

## 1. Proposal in one sentence

Turn the bloodline-reskin support that already exists in TNR into a player-owned, non-tradeable cosmetic entitlement system: a reskin is pinned to one canonical bloodline, overrides only its presentation, requires the matching bloodline to use, and can be purchased for real money or granted directly without creating or maintaining a duplicate bloodline.

This gives the **H-rank customization fantasy without H-rank maintenance**.

## 2. Why this is unusually well suited to TNR

A bloodline is one of the strongest identity surfaces a character has. That makes it a natural cosmetic product, but duplicating a bloodline solely to change its name/art creates permanent maintenance:

- balance changes have to remain synchronized;
- mechanical fixes have to be copied;
- downstream jutsu/content references can drift;
- duplicate records clutter bloodline selection and administration;
- a cosmetic release becomes a long-term gameplay maintenance obligation.

A reskin avoids all of that. The canonical bloodline remains the only mechanical source. The skin is presentation attached to it.

Commercially, that creates a repeatable cosmetic release format which:

- does not sell combat power;
- can increase average order value as a pack upgrade;
- can be released repeatedly for popular bloodlines;
- has low ongoing balance cost after release;
- is naturally collectible;
- does not lose value to a secondary market when ownership is account-bound.

## 3. Important discovery: most of the presentation system already exists

Current game source already contains a bloodline-reskin feature.

### Existing model

`app/drizzle/schema.ts` defines a global `BloodlineReskin` with:

- `bloodlineId`
- `name`
- `description`
- `image`
- creator / timestamps

The source comment explicitly describes these as staff-curated reskins assignable to users.

`userData` already carries `bloodlineReskinId` as the active reskin pointer.

### Existing behavior

`app/src/libs/bloodline.ts` applies a reskin by copying the canonical bloodline and overriding only:

- name;
- image;
- description.

The underlying bloodline mechanics remain canonical.

The current manual UI says the same thing explicitly: bloodline reskins are staff-curated cosmetics that change presentation but not mechanics.

Profile and combat flows already resolve the active reskin into the displayed bloodline, including combat initialization.

### What is missing

The current feature is **assignment**, not **ownership**.

There is no per-user bloodline-reskin entitlement table. Staff can create/edit reskins and staff can set a user's active `bloodlineReskinId`, but players do not have an owned-skins catalogue or a purchase/grant path.

That means this proposal should be treated as **productizing an existing feature**, not designing bloodline reskins from zero.

## 4. Recommended product model

Separate the system into three concepts.

### A. BloodlineReskin — global cosmetic definition

One staff-curated definition pinned to one canonical `bloodlineId`.

It contains presentation only.

Recommended V1 presentation fields:

- display name;
- bloodline image;
- flavor/lore description.

Do not copy mechanical fields into the reskin.

Do not create another Bloodline row.

### B. UserBloodlineReskin — permanent entitlement

Add a per-user ownership record, conceptually:

- userId;
- reskinId;
- grantedAt;
- grant source;
- optional purchase/grant reference;
- optional revokedAt / revocation reason.

Unique ownership should be enforced on `(userId, reskinId)`.

Suggested grant-source categories:

- real-money purchase;
- bundle;
- event/reward;
- staff grant;
- migration.

The exact schema is an engineering decision, but **ownership must exist independently of the active skin pointer**.

### C. userData.bloodlineReskinId — active cosmetic

Keep the existing pointer as the currently selected appearance.

The active pointer is not ownership. It is only the equipped choice.

This is analogous to owning several skins but wearing one.

## 5. Player rules

### Cosmetic-only invariant

A reskin must never alter:

- bloodline effects;
- stats;
- regen;
- rank;
- rarity/difficulty;
- elements;
- jutsu access;
- mechanical descriptions generated from effects;
- combat calculations.

A mechanical update to the base bloodline therefore updates every reskin automatically.

### Base-bloodline requirement

Recommended rule:

- A standalone cash purchase is offered only when the player owns the matching base bloodline.
- A reskin can only be equipped while the matching bloodline is the player's active bloodline.
- If a bundle grants the base bloodline and its skin together, both can be granted as one commercial outcome.
- Direct awards may grant the entitlement before the base is active, but it remains unusable until the base is owned/active.

For TNR, the recommended interpretation of “owns the bloodline” for purchase eligibility is **the bloodline exists in the player's retained/historic owned pool**, not merely “currently equipped.” Equipping the reskin still requires that bloodline to be current.

This ownership predicate is a user-owned product ruling and should be confirmed before implementation.

### Bloodline switching

When the user switches to a different base bloodline:

- the reskin entitlement remains permanently owned;
- the mismatched reskin must not render;
- recommended V1 behavior is to clear the active reskin pointer and let the player reselect it when they return.

### Non-tradeability

Bloodline reskins should never enter ordinary item inventory.

Do not model the paid skin as:

- an item;
- a consumable token;
- a market listing;
- a transferable voucher.

The entitlement is assigned directly to the account/character and cannot be traded or gifted unless a future gifting system is designed explicitly.

## 6. Why direct entitlement is better than the current jutsu-reskin shape

Current jutsu reskins are player-specific customization rows and are limited/charged through the reskin-slot system.

That is useful precedent for overlay behavior, but the commercial bloodline product should use a global cosmetic definition plus a user entitlement.

The newer item-variant system is the closer ownership model:

- the variant definition is global;
- an explicit per-user unlock persists;
- reacquiring/using the base object restores access to what the user already unlocked.

A paid bloodline skin should follow that same ownership principle: **you keep what you paid for**.

## 7. Monetization proposal

### Product A — Bloodline Reskin

A permanent real-money cosmetic for one bloodline.

Requirements:

- player owns the base bloodline;
- no mechanical benefit;
- permanently unlocked after a successful purchase;
- non-tradeable;
- can be equipped/unequipped freely while using the matching bloodline.

This should be the cleanest standalone product.

### Product B — Bloodline Pack cosmetic upgrade

For a bloodline-specific sales pack, offer the reskin as an upgrade.

The reskin is especially effective here because the buyer is already expressing interest in that exact bloodline fantasy.

Suggested commercial ladder:

1. **Base bloodline offer**
2. **Reskin upgrade** — adds the permanent bloodline skin
3. **Premium upgrade** — permanent skin plus one month of Gold Federal at a discounted bundle rate

Exact prices and discount percentages are intentionally **unset**. Pricing is user-owned.

### Gold Federal bundle note

Current game source already has store-backed Federal subscription products, including Gold, and an idempotent purchase ledger.

Commercially the player can see one bloodline-themed premium offer, but implementation should preserve the existing Federal purchase/entitlement rules rather than invent a second Federal system. Depending on sales channel, the cosmetic and Federal component may settle as separate entitlements even if presented together.

### Release cadence

This creates a practical recurring release strategy:

- choose a popular or newly refreshed bloodline;
- commission one strong premium visual identity;
- release its reskin;
- pair it with a bloodline-targeted offer;
- optionally rotate older skins back into promotions.

The important permanence rule is: **sale availability can rotate; ownership should not.**

## 8. Store / purchase architecture

TNR already has an idempotent real-money purchase pipeline.

Current store grants recognize reputation products and Federal products. The purchase ledger uses transaction IDs as idempotency guards and already records grant/revocation state.

Recommended direction:

- extend the existing purchase-grant framework with cosmetic product mappings rather than creating a separate checkout;
- map a store product/SKU to a `BloodlineReskin`;
- successful settlement inserts the user entitlement exactly once;
- repeated webhook/payment delivery must be harmless;
- the storefront must recognize “already owned” and prevent a second purchase where possible.

A paid skin should behave as a durable one-time entitlement, not as a reputation-like consumable.

## 9. Refunds, revocations and deletion

This is the largest lifecycle change required by monetization.

### Refund / chargeback

Recommended rule:

- if the paid entitlement is revoked by the payment system, revoke the user skin entitlement;
- if it is currently active, clear the active pointer;
- do not touch the underlying bloodline.

Awarded/non-purchase skins can follow separate staff moderation rules.

### Hard deletion becomes unsafe

The current staff `deleteReskin` behavior clears the skin from every user and hard-deletes the definition.

That is acceptable for a staff-only cosmetic scaffold. It is **not acceptable once users have paid real money for the skin**.

After commercial launch, sold/granted reskins should normally be:

- retired from sale;
- hidden from new acquisition;
- retained for existing owners.

Hard deletion should be limited to never-granted/test content or exceptional legal/safety cases with an explicit owner-remediation policy.

Recommended future state is an availability/retirement field rather than destructive deletion.

## 10. Editing a sold skin

A global reskin definition is valuable because fixes propagate to every owner.

Staff should still be able to correct:

- broken image assets;
- spelling;
- formatting;
- lore mistakes;
- presentation defects.

But a paid cosmetic's **identity should be stable**. A major thematic replacement after sale is materially different from correcting the product somebody bought.

Recommended product policy:

- ordinary corrections may update in place;
- substantial redesigns should become a new reskin unless there is a compelling remediation reason.

Existing ActionLog behavior is useful audit precedent.

## 11. Description discipline

Because the reskin can override `description`, it is possible for flavor prose to become misleading if it repeats exact mechanics.

Recommended rule:

- bloodline reskin descriptions are flavor/lore only;
- mechanical effects remain rendered from the canonical bloodline;
- do not put exact balance values into reskin flavor text.

This preserves the “updates itself” promise even when the underlying bloodline is rebalanced.

## 12. Player-facing UX

Recommended V1 surface on the bloodline page:

**Appearance**

- Default
- Owned reskin cards
- selected/equipped indicator
- preview of art, name and flavor description
- Equip / Use Default controls

Each skin should make the invariant visible:

> Cosmetic appearance only. Uses the mechanics of [Base Bloodline].

Store states:

- **Owned**
- **Available** — user owns required bloodline
- **Requires [Bloodline]** — previewable but not purchasable, unless the displayed bundle also grants the base bloodline
- **Retired** — not buyable but remains usable by owners

Do not make players visit staff/manual surfaces to manage purchased cosmetics.

## 13. Important server guards

At minimum:

1. The requested reskin exists.
2. The user owns the reskin entitlement.
3. `reskin.bloodlineId` matches the user's active `bloodlineId`.
4. The entitlement is not revoked.
5. Retired-from-sale does not invalidate prior ownership.
6. Selecting default clears only the active pointer, not ownership.
7. Changing bloodlines cannot leave a mismatched visual active.
8. Purchase settlement is idempotent.
9. A player cannot trade, list, transfer, consume, or sell an entitlement.

Never rely on UI-only gating for these rules.

## 14. Current-source issues that implementation must address

The existing scaffold is close but not commerce-ready:

- no per-user ownership table;
- player self-selection does not exist;
- assignment is staff-controlled;
- no purchase/grant mapping for bloodline skins;
- current hard-delete behavior destroys assigned cosmetics;
- profile staff editing is an assignment mechanism, not an entitlement check;
- commerce grant outcomes currently cover reputation/Federal, not permanent cosmetics.

These are productization gaps, not a reason to replace the existing reskin renderer.

## 15. Suggested implementation phases

### Phase 1 — entitlement foundation

- add user ownership model;
- server-side ownership/matching guards;
- active equip/unequip procedures;
- preserve existing staff-created global reskin definitions;
- enforce non-tradeability by architecture.

### Phase 2 — player UX and direct grants

- Appearance picker;
- owned/locked/default states;
- staff/event grant tooling;
- retirement semantics;
- migration for any already-assigned reskins if needed.

### Phase 3 — real-money products

- store SKU/product mapping;
- extend idempotent purchase grants;
- refund/revocation handling;
- already-owned protection;
- purchase analytics.

### Phase 4 — bloodline pack merchandising

- cosmetic upgrade option;
- premium skin + Gold Federal offer;
- campaign presentation;
- conversion/attach-rate reporting.

This order allows the entitlement model to be tested independently before money depends on it.

## 16. Success metrics

Useful commercial and product metrics:

- bloodline-pack attach rate for the reskin upgrade;
- premium upgrade attach rate;
- standalone skin conversion;
- average order value change;
- percentage of owners who equip the skin;
- Gold Federal attach rate from the premium offer;
- repeat cosmetic purchasers across later bloodline releases;
- refund/chargeback rate.

These should measure whether the skins create incremental revenue rather than simply moving existing spend between products.

## 17. Risks and mitigations

### “Pay-to-win” perception

**Risk:** paid bloodline product is mistaken for a stronger bloodline.  
**Mitigation:** mechanically impossible overlay; explicit cosmetic-only UI.

### Paid content disappears

**Risk:** staff deletes/replaces a sold reskin.  
**Mitigation:** retire instead of delete; ownership survives sale removal.

### Wrong bloodline displays

**Risk:** active pointer references a reskin for another bloodline.  
**Mitigation:** server match guard and pointer clearing on bloodline switch.

### Duplicate purchase

**Risk:** a retry or repeated checkout grants/charges value incorrectly.  
**Mitigation:** existing store transaction idempotency plus unique user/reskin entitlement.

### Flavor becomes stale after balance patch

**Risk:** reskin description contains obsolete numeric mechanics.  
**Mitigation:** flavor-only skin description; canonical mechanics rendered separately.

### Custom/private bloodlines

**Risk:** a commercial skin is created against a user-owned custom bloodline without owner approval.  
**Mitigation:** preserve TNR doctrine: custom user-owned bloodlines/reskins require the appropriate go-ahead before modification or commercialization.

## 18. Recommended rulings before Fable implementation

These are still user-owned decisions.

### Decision A — what counts as owning the required bloodline?

**Recommendation:** base bloodline is present in the player's retained/historic owned bloodline pool. The skin is usable only while that bloodline is active.

### Decision B — can an award be granted before base ownership?

**Recommendation:** yes. The entitlement may exist dormant, but it cannot be equipped until the base bloodline is owned and active. Standalone cash checkout should still require ownership.

### Decision C — sale permanence

**Recommendation:** permanent player ownership; sales availability may rotate.

### Decision D — paid-skin deletion

**Recommendation:** no ordinary hard deletion after any paid/granted entitlement exists. Retire from sale instead.

### Decision E — refunds / chargebacks

**Recommendation:** revoke a purchase-backed skin entitlement and clear it if active.

### Decision F — commercial ladder

**Recommendation:** support both standalone skin purchase and bloodline-pack upgrade; add a premium option pairing the permanent skin with one month of discounted Gold Federal.

### Decision G — price

**Recommendation:** leave as a deliberate commercial tuning decision after deciding the value ladder and reviewing existing purchase conversion. No price is canon from this document.

## 19. Verdict

**PROPOSE / ADVANCE.**

The core idea is stronger than it initially appears because the current TNR source already implements the hardest presentation invariant: a bloodline reskin overlays name/image/description onto the same canonical bloodline in profile and combat.

The right project is therefore not “build bloodline reskins.” It is:

> **Turn the existing staff-only bloodline-reskin layer into a durable player-owned cosmetic product system.**

That preserves one mechanical bloodline, eliminates duplicate-bloodline maintenance, creates a repeatable real-money cosmetic category, and gives bloodline-specific sales packs a natural permanent upgrade.
