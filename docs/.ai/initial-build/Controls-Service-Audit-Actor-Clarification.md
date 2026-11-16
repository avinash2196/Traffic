# Q34 — Service actor in rejected controls publication audit

## Human Review

**Approved by user on 2026-10-30.** This resolves one representation gap in approved Q32 / API-Contract CT-13.2 and is incorporated into that contract and the controls clarification addendum. It authorizes no implementation, test execution, service permission or spending.

## Verified gap

CT-13.2 requires audit of authenticated HTTP publication attempts, including forbidden callers, and defines each audit item's actor as the actor object above its table. Only a traffic-web human actor and the controls-bootstrap system actor are defined. CT-12 classifies a valid service token used on a human/control-management operation as authenticated but forbidden (403). Such a rejected attempt cannot truthfully use either currently defined actor variant.

## Exact recommended clarification

For a rejected authenticated service-client publication attempt, permit audit actor exactly:

```json
{"type":"service","issuer":"https://auth.traffic.localhost/realms/traffic","subject":"exact validated JWT sub","client_id":"traffic-completion"}
```

The subject is the exact validated token subject, not the illustrative string. client_id is the validated fixed CT-12 azp of the actual service caller, not necessarily the example traffic-completion. issuer is the validated fixed issuer. These values never come from the submitted publication body, an inferred service-account username or an arbitrary client string.

Only rejection audit entries may use this service variant. The request remains 403 FORBIDDEN; its outcome is rejected, error_code FORBIDDEN, reason Publication rejected, publication_revision null and old_values/new_values null under CT-13.2. An invalid token remains 401 and follows the existing unauthenticated failure-signal rule.

Published snapshots and publication audit retain human actors; the baseline retains the existing system actor. Services cannot publish controls, replay a human publication, gain human grants or alter snapshots. No route, client identity, scope, permission or milestone ownership is added.

If approved, record Q34 in requirements.md and incorporate this exact audit-only variant into CT-13.2 and the approved Q32 addendum before completing the Runtime Controls RED Implementation Plan. Q31–Q33 and all other existing contract decisions remain unchanged.
