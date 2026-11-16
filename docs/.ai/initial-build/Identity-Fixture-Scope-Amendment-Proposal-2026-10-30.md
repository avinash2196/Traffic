# Identity fixture scope amendment — proposal, 2026-10-30

**Approved by user on 2026-10-30; exact diff incorporated into the second proposed test block in 004_Implementation_Plan_Identity_RED.md.** Workspace executable files and Plan execution status remain unchanged. Current execution authority and the planning verification gate are recorded in 004's Human Review section. [Actual planning evidence](Identity-Readiness-Verification-2026-10-30.md) records the original fixture error preventing valid integration RED; approval does not establish that the corrected fixture passes.

The provider logged that the hardcoded scope assignment was ignored, and the verified service token carried only `email profile`. Replace that ineffective mapper with a fixture-owned OIDC client scope named `assessment:create`, included in token scope and linked as a default scope only to the fixture's `traffic-ai-review` client. Retain the gateway audience mapper, every issuance/signature/claim assertion, exact 10-second HTTP timeout and original `assessment:create` assertion. No realm-wide default is added.

Keycloak's [official client-scope documentation](https://github.com/keycloak/keycloak/blob/main/docs/documentation/server_admin/topics/clients/con-client-scopes.adoc) documents inclusion of a scope's name in tokens and application of client default scopes. The [26.8.1 Admin REST API](https://www.keycloak.org/docs-api/26.8.1/rest-api/index.html) documents POST client-scopes, GET client-scopes/{id}, PUT clients/{client-uuid}/default-client-scopes/{clientScopeId} (204), and GET of that binding (names/IDs). These support the proposed mechanism; no amended-fixture run establishes its behavior yet.

The exact unified diff below is against the complete proposed tests/test_identity_oidc.py in approved004. It removes the ineffective mapper and adds idempotent creation, fixture ownership/configuration assertions and binding readback. Unknown preexisting scope ownership/configuration fails rather than being silently changed. Fixture state remains confined to a fresh disposable realm; this uses existing CT-12 vocabulary.

```diff
--- a/tests/test_identity_oidc.py
+++ b/tests/test_identity_oidc.py
@@ -66,14 +66,25 @@
         assert service["serviceAccountsEnabled"] and not service["publicClient"]
         assert not service["standardFlowEnabled"] and not service["directAccessGrantsEnabled"]
         desired = [dict(mapper, name="identity-fixture-gateway", config={
-            "included.custom.audience": "traffic-gateway", "access.token.claim": "true", "id.token.claim": "false"}),
-            {"name": "identity-fixture-scope", "protocol": "openid-connect", "protocolMapper": "oidc-hardcoded-claim-mapper",
-             "config": {"claim.name": "scope", "claim.value": "assessment:create", "jsonType.label": "String",
-                        "access.token.claim": "true", "id.token.claim": "false"}}]
+            "included.custom.audience": "traffic-gateway", "access.token.claim": "true", "id.token.claim": "false"})]
         existing = get("/clients/" + service["id"] + "/protocol-mappers/models")
         for m in desired:
             if not any(x["name"] == m["name"] for x in existing):
                 post("/clients/" + service["id"] + "/protocol-mappers/models", m)
+        scopes = [s for s in get("/client-scopes") if s["name"] == "assessment:create"]
+        if not scopes:
+            post("/client-scopes", {"name": "assessment:create", "protocol": "openid-connect",
+                "attributes": {"include.in.token.scope": "true", "identity-fixture": "DP-M03"}})
+            scopes = [s for s in get("/client-scopes") if s["name"] == "assessment:create"]
+        assert len(scopes) == 1
+        scope = get("/client-scopes/" + scopes[0]["id"])
+        assert scope["protocol"] == "openid-connect"
+        assert scope["attributes"]["include.in.token.scope"] == "true"
+        assert scope["attributes"]["identity-fixture"] == "DP-M03"
+        binding = "/clients/" + service["id"] + "/default-client-scopes"
+        response = c.put(root + binding + "/" + scope["id"], headers=headers)
+        assert response.status_code == 204, response.status_code
+        assert any(s["id"] == scope["id"] and s["name"] == "assessment:create" for s in get(binding))
         secret = get("/clients/" + service["id"] + "/client-secret")["value"]
         service_token = c.post(discovery["token_endpoint"], data={"grant_type": "client_credentials",
             "client_id": "traffic-ai-review", "client_secret": secret}).raise_for_status().json()["access_token"]
```

File-only proposal verification regenerated this diff mechanically from the approved complete block, confirmed its before-context occurred exactly once, parsed the resulting Python with `compile` in memory, and confirmed the original token-scope assertion remained. Output: `PASS exact diff regenerated mechanically from approved block; proposal Python parses; existing scope assertion retained; no fixture executed`. No test file was written or imported.

After human approval, incorporate this exact diff into 004's complete test block and update its proposed-change/binding descriptions to name the real client scope and per-client binding. Then repeat the approved planning-time gate in a new host-visible disposable project: exact bounded readiness; unchanged Foundation; exact baseline tests; general scratch-only seven-test soundness; repeated baseline and every inherited validation/isolation/database/cleanup check. Stop on any prerequisite or fixture error. This proposal has not run those checks and does not authorize milestone execution or GREEN.
