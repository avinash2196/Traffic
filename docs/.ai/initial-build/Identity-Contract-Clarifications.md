# Identity contract clarifications — initial-build

## Status and authority

**Approved by user on 2026-10-26 — Q29 and Q30.** The approved identity-profile decisions below are incorporated into API-Contract.md CT-12 and its CT-02/07/08/10 references. This approval resolves contract expectations for DP-M03 planning; it does not approve a future Implementation Plan, test execution, production change or spending.

Baseline: requirements.md Status/IB-R07/IB-R08/IB-R12/IB-R18/IB-R20; Architecture-Proposal.md approved AP-D01/AP-D02/AP-D06; Plan.md Status, External Contract Requirements and DP-M03/04; API-Contract.md approved Status, CT-01/02/07/08/10. Foundation 001 Human Review and 002/003 execution status, DP-M02-Browser-Execution-2026-10-26.md and Local-Git-CI-Deferral.md establish completed local prerequisites and pending DP-M03, with hosted CI deferred by Q28, not passed. This document continues clarification numbering after Q28; it does not alter those decisions.

Repository evidence: tools/local.py:74–80 defines exactly six realm roles (`citizen`, `admin`, `settings-admin`, `review:write`, `evidence:export`, `controls:write`) and the public `traffic-web` PKCE client. It does not yet provision service clients, audience mappers or users. bootstrap.py exposes only Foundation readiness. Therefore none of the proposed response/claim/service mappings below is claimed as implemented or verified. Foundation 001 explicitly defers fixture user/service provisioning and audience/scope assertions to Identity RED/GREEN.

## Q29 — approved `/me` and human claim mapping

The following exact additions to CT-02 were approved.

`GET /api/v1/me` is a human operation, returning 200 JSON with exactly three required, non-null fields; no additional fields:

```json
{
  "subject": "35a26b15-0ae4-4caf-ad87-d97a664b17e3",
  "roles": ["citizen", "admin"],
  "permissions": ["citizen:own", "reports:read:any", "review:write"]
}
```

The example represents `realm_access.roles` containing `citizen`, `admin`, `review:write`; it does **not** imply that admin grants review permission. `subject` is the exact validated JWT `sub` string (nonempty, no normalization; not constrained to UUID). Ownership remains the exact `(iss, sub)` pair from CT-01; issuer is fixed and is not an additional response field. No username, email or Keycloak profile is returned.

| Response field | Exact schema and computation proposed |
|---|---|
| subject | Nonempty JSON string, exact `sub` |
| roles | Unique JSON string array; subset of `citizen`, `admin`, `settings-admin`, in that fixed order; only base roles present in `realm_access.roles` |
| permissions | Unique JSON string array; subset of the six literals in the table below, in table order; computed from conjunctions below, never copied from an untrusted request or arbitrary JWT permission field |

| Ordered effective permission literal | Required realm roles | Meaning already bounded by the contract |
|---|---|---|
| citizen:own | citizen | Own reporting/evidence/clarification/history and awards operations in CT-02/04 |
| reports:read:any | admin | Admin report/private evidence reads in CT-02/04 |
| review:write | admin **and** review:write | Clarification request, decision and authorized recovery |
| evidence:export | admin **and** evidence:export | Create/read/download ZIP |
| controls:read | settings-admin **and** controls:write | CT-08 GET controls and audit, preserving CT-02's combined grant requirement |
| controls:write | settings-admin **and** controls:write | CT-08 publication |

These literals describe existing powers only; `citizen:own`, `reports:read:any` and `controls:read` are proposed output vocabulary, not new realm roles. `review:write`, `evidence:export`, `controls:write` remain separately granted realm roles. CT-08's settings-admin shorthand is interpreted consistently with CT-02's combined settings-admin/control-write requirement: both grants are required for reading controls/audit and for publication. No read-only authority is added to a bare settings-admin role.

Recognize roles only from `realm_access.roles`; never from `resource_access`, a generic `roles`/`permissions` claim, `scope`, username or groups. Unknown role strings (including Keycloak defaults) are ignored; duplicate role strings collapse. Missing `realm_access` or missing `roles` means no recognized roles. Present `realm_access` must be an object, and present `roles` an array of strings; null/wrong types invalidate authentication (401). Base roles combine by union; permission-like roles without their matching base role confer nothing. An authenticated human with no recognized roles gets 200 `/me` with `roles:[]`, `permissions:[]`; protected business operations deny 403. Admin alone cannot review/export; citizen+admin has both base powers but self-review/finalization/export still denies 403 `SELF_REVIEW_FORBIDDEN`. No base role implies another.

### Proposed minimum token claim contract for both questions

These are explicit application token-profile choices, not assertions about every default Keycloak token. Signature/issuer/RS256/audiences, <=30-second skew, <=5-minute access lifetime, key refresh/cache/coalescing/outage behavior and CT-01 authentication errors remain unchanged.

- Require JOSE `alg="RS256"`, nonempty string `kid`; if JOSE `typ` is present it must be `JWT`. Require payload `typ="Bearer"` as the access-token discriminator; missing/other payload type, including `ID`, denies 401. An ID token never becomes acceptable merely by having an audience or valid signature.
- Require `iss`, `sub`, `azp` as nonempty strings; `iss` exactly CT-01 issuer. Require `exp` and `iat` as integer NumericDate seconds (JSON booleans are not integers). Require `exp>iat`, `exp-iat<=300`; validate expiry and future issuance with the existing <=30-second skew.
- `nbf` is optional; if present require integer NumericDate and validate with that skew. Absence does not fail validation. This clarifies CT-02's `nbf` validation without requiring an optional claim to exist.
- Require `aud` as a nonempty string or nonempty array of nonempty strings containing the receiver's fixed audience. Arrays must contain no duplicates. Other audience values confer no additional access. Validate receiver audience and allowed `azp` independently.
- Human tokens require `azp="traffic-web"` and reporting audience `traffic-api`. They cannot authorize any service operation even when given service-looking scopes or extra audiences. Human `scope` is not a source of application permissions; if present it must be a string. Unused standard claims are ignored and confer no authority.
- Service tokens require the fixed `azp`/audience/scope mapping in Q30. Service identity is classified by this configured client allowlist, never by a `service-account-` username, role presence or arbitrary `sub` prefix. `sub` remains required for audit identity; neither caller-supplied nor dynamically discovered client identities are accepted.

Missing/malformed/invalid authentication claims, unknown `azp`, wrong receiver audience or token type use 401 `UNAUTHENTICATED`; valid authenticated principal of the wrong human/service class or lacking a required permission/scope uses 403 `FORBIDDEN`. For this distinction, authentication recognizes only the globally fixed client IDs in Q30 plus traffic-web and validates the receiving boundary's audience. Authorization then requires an allowed client/receiver/operation row: a recognized client presenting a valid receiver-audience token but lacking that row is denied 403, even if it copies another client's scope. This does not permit dynamic client IDs or grant authority from an audience alone. CT-01 error envelope, cache headers and request IDs apply. Existing JWKS-unavailable cases remain 503, not converted to 401.

## Q30 — approved fixed service identities and scope matrix

These literal client IDs and scopes are the approved CT-02 responsibility mapping, including CT-07 `assessment:create`. Each is a confidential client with client-credentials enabled, browser/interactive grants disabled and private injected secret per CT-10. Replicas of the same role use the same configured client ID. No gateway outbound OIDC client is needed: provider credentials remain solely gateway-owned under the existing CT-07/09 rules.

| Caller / fixed `azp` = configured client ID | Receiver audience | Exact allowed application scopes | Existing CT-02 responsibility |
|---|---|---|---|
| reporting / traffic-reporting | traffic-media | media:ingest media:read media:export | Ingest, authorized private read, export assembly |
| media worker / traffic-media-worker | traffic-media | media:original | Read originals for screening |
| AI review / traffic-ai-review | traffic-media | media:derivative | Read scoped derivatives only |
| AI review / traffic-ai-review | traffic-gateway | assessment:create | CT-07 POST /internal/v1/assessments |
| reporting completion consumer / traffic-completion | traffic-api | completion:consume | CT-06 completion boundary |

The client allowlist is exactly the table plus human `traffic-web`; no arbitrary configured string becomes authorized. Receiver audience configuration is `traffic-api` for reporting/completion reception, `traffic-media` for media reception, `traffic-gateway` for gateway reception. Outbound `OIDC_SERVICE_CLIENT_ID` is `traffic-reporting`, `traffic-media-worker`, `traffic-ai-review`, or `traffic-completion` for the respective role; no outbound client secret is assigned to gateway. Audience is the receiving boundary, not the caller's name. These are proposed CT-10 mappings; provisioning/configuration changes require later milestone review.

Service `scope` is required as a string of distinct, case-sensitive ASCII-space-separated scope tokens (no leading/trailing/repeated spaces); an empty string is valid authentication but authorizes no service operation. Only a scope listed for that exact client/receiver pair grants access; unrelated scopes are ignored and never expand the allowlist. Each operation requires its row's applicable scope in addition to the client/audience checks; the three reporting media scopes authorize only their corresponding ingest/read/export purpose, not one another. A token may carry multiple listed scopes/audiences, but each receiver independently applies only its own row. Gateway assessment creation requires `azp=traffic-ai-review`, audience `traffic-gateway`, and `assessment:create` together. No other service client acquires this power through a copied scope.

Service clients receive no human realm role grants; even an accidentally role-bearing service token cannot call `/me`, citizen/admin/controls operations (403). Human clients cannot call media/assessment/completion service operations (403 after valid authentication for that receiver); a human token with wrong receiver audience first fails authentication (401). Service private-media access also requires the already-approved <=60-second caller/evidence/report/round/purpose capability and current authorization; a scope never replaces it. No new media/completion routes or message transport are defined here, and no service may finalize reports, grant awards, manage roles, publish controls or bypass ownership.

## Traceability and approval effect

| Decision | Approved baseline and gap resolved | Consequence of approval |
|---|---|---|
| Q29 | CT-02 `/me`, allowed principals; CT-01 identity/errors; CT-08 read/publication; existing six realm roles | Fixes response schema/order, canonical human claim source, conjunctions, no-role behavior and minimum JWT types for executable Identity expectations |
| Q30 | CT-02 fixed service responsibilities/audiences; CT-07 AI-review service scope; CT-10 deployment names | Fixes literal client/audience/scope pairs and human/service denials without adding business authority |

The user approved these **two contract decisions only** on 2026-10-26. They are recorded in API-Contract.md CT-12 and the requirements Clarification Log before fresh-context DP-M03 planning. No future Implementation Plan or test execution is approved; DP-M03 remains Pending.

Document-only review: checked six existing realm roles against tools/local.py; all effective permissions require the existing base/grant combinations; no admin-to-review/export inheritance; Q30 rows map one-for-one to CT-02 responsibilities; gateway uses only `assessment:create`; optional `nbf` is not required. Existing issuer/signature/cache/skew/errors/self-review/ownership/provider boundaries remain constraints. No test dry run applies to a contract-only proposal. No source, test, configuration, service, container or provider call was changed or run.
