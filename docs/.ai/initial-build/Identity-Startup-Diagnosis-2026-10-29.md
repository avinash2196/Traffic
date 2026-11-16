# Identity planning startup diagnosis — 2026-10-29

Planning diagnostics only; no DP-M03 execution, approval or GREEN evidence. No workspace executable changed. Exact 004 test contents were extracted into host scratch `C:/Users/avina/AppData/Local/Temp/traffic-identity-diagnose-72d4cb1586b0`; both matched their proposal after newline normalization. Project `traffic-31773e12e6b3` used newly initialized secrets, not root `.local`.

## Actual results

Native launcher was `C:/Users/avina/Downloads/avinash-repo/v11/Traffic/.venv/Scripts/python.exe`. Commands `tools/local.py init`, `compose config --quiet`, `compose build`, and `compose up -d` against the scratch script exited 0. Docker commands required sandbox escalation. Initial sandbox TEMP copy was inaccessible to native Python (`private.mkdir` WinError5); elevated host also could not see that virtual path. It started no containers. The host-visible scratch above replaced it.

All Docker commands below used `docker compose -f C:/Users/avina/AppData/Local/Temp/traffic-identity-diagnose-72d4cb1586b0/.local/compose.json`.

`run --rm runner python tools/check.py` exited 1, at line59: `assert discovery and discovery["issuer"] == "https://auth.traffic.localhost/realms/traffic"`. This unchanged prerequisite failure is retained, not treated as RED or rerun to obtain success. No pytest suite ran in this diagnostic attempt.

A scratch-only diagnostic, `run --rm runner python /workspace/diagnose.py`, exited 0 and printed only:

```text
discovery 502 0.066
admin_token 502 0.017 access_token_present False
```

That diagnostic used strict CA/hostname verification, trust_env=False, timeout60, and the exact admin URL/client/grant/username/password-file inputs from 004. It printed neither token, response body nor password. Requests occurred before Keycloak listened. Exit0 means diagnostic completion, not authenticated readiness.

Bounded `docker logs --tail 20 traffic-31773e12e6b3-auth-1` showed Quarkus augmentation completed in80770ms at02:10:23.412 UTC, schema initialization at02:10:56.215, master-realm initialization at02:12:03.669, realm import at02:12:18.866, temporary admin creation at02:12:19.626 and HTTP listening at02:12:20.936. Keycloak reported server startup116.415s, bootstrap89.436s. The prerequisite expired before this listening transition. This establishes the cause of this fresh prerequisite failure: provider startup exceeded the check's readiness period. It does **not** establish why the historical already-discoverable provider's admin token request timed out.

`docker stats --no-stream --format '{{.Name}} CPU={{.CPUPerc}} MEM={{.MemUsage}}' traffic-31773e12e6b3-auth-1 traffic-31773e12e6b3-db-1` exited0. During augmentation: auth677.59% CPU/533.5MiB of7.603GiB, DB10.23%/43.07MiB. Later schema initialization: auth218.05%/447.3MiB, DB8.36%/62.15MiB. These are observations, not proof of host resource exhaustion. Read-only `docker exec traffic-31773e12e6b3-db-1 psql -U postgres -d keycloak -Atc "SELECT state, wait_event_type, wait_event, left(query,180) FROM pg_stat_activity WHERE datname='keycloak';"` exited0: idle ClientRead COMMIT and idle-in-transaction ClientRead on databasechangeloglock SELECT FOR UPDATE; no blocked-query wait was observed.

After initial scoped teardown, the same project was started once more for diagnosis only, with recreated empty volumes. No test/check retry ran. Augmentation41439ms ended02:14:24.675, schema initialization began02:14:55.805; next observed progress was JDBC_PING discovery02:19:28.859. At02:19:30.787 UTC the fixed240s observation target was already exceeded; tool/turn latency meant elapsed time was longer than intended. No HTTP listener or successful authenticated request was established. Final pre-teardown logs reached master-realm initialization02:19:43.203 and full import request02:19:49.582. This second startup remained a failure of the diagnostic readiness bound. No post-listening token timing was obtained. Historical ReadTimeout cause remains unresolved.

## Concrete proposed next verification amendment

The exact protocol below was incorporated into 004_Implementation_Plan_Identity_RED.md following user approval on 2026-10-30. Its current authority and execution gate are recorded in that plan's Human Review section. The diagnostic results above remain historical; approval is not execution evidence.

Retain every existing Foundation and Identity assertion and exact test timeout. Before running unchanged Foundation checks in a new disposable project, run the following single bounded diagnostic in its runner. Its code is temporary input only; never add it to root executable files. This does not declare a previously failed check nonblocking. If it fails, stop and retain sanitized startup logs and timings. A successful result permits running the unchanged prerequisite suite, then the exact 004 baseline tests; it does not itself satisfy either suite.

```python
import ssl
import time
from pathlib import Path
import httpx

origin = "https://auth.traffic.localhost"
issuer = origin + "/realms/traffic"
deadline = time.monotonic() + 240
context = ssl.create_default_context(cafile="/private/ca.crt")
with httpx.Client(verify=context, trust_env=False, timeout=5) as client:
    while True:
        if time.monotonic() >= deadline:
            raise SystemExit("FAIL provider discovery readiness exceeded 240 seconds")
        try:
            response = client.get(issuer + "/.well-known/openid-configuration")
            if response.status_code == 200:
                discovery = response.json()
                assert discovery["issuer"] == issuer
                assert discovery["jwks_uri"] == issuer + "/protocol/openid-connect/certs"
                break
        except httpx.TransportError:
            pass
        time.sleep(min(2, max(0, deadline - time.monotonic())))
    started = time.monotonic()
    try:
        response = client.post(origin + "/realms/master/protocol/openid-connect/token",
            timeout=10, data={"client_id": "admin-cli", "grant_type": "password",
                "username": "foundation-admin",
                "password": Path("/private/keycloak-admin.password").read_text()})
    except httpx.TransportError as failure:
        print("FAIL single admin request", type(failure).__name__,
              round(time.monotonic() - started, 3))
        raise SystemExit(1) from None
    print("admin status", response.status_code, "elapsed seconds",
          round(time.monotonic() - started, 3))
    if response.status_code != 200 or not response.json().get("access_token"):
        raise SystemExit("FAIL admin issuance")
    print("PASS provider discovery and one authenticated admin issuance")
```

The discovery loop polls a readiness condition, not a failed test; the admin request occurs once, keeps the proposed fixture's10s bound, and any failure stops. Maximum elapsed includes at most one in-flight5s discovery request beyond240s, then one10s admin request if discovery became ready. No general retry of password grant is proposed. This amendment makes startup/administration prerequisites explicit; it is not yet evidence that the historical timeout is fixed. If the240s startup bound is exceeded again, investigate the environment or review a different bound; do not silently extend it.

The exact seven-test RED repeat, full scratch-only general implementation pass and inherited Foundation repeat/restart/validation/isolation/database checks remain outstanding. No Plan status changes are justified.

## Cleanup

Both teardown commands were project-scoped `down --volumes --remove-orphans`; first exited0. First label-filtered container/volume/network inventories were all empty. Root historical `.local` SHA256 comparison against a stable absolute snapshot inside host scratch passed after first teardown; hashes and secret values were never printed. Final cleanup verification is recorded below after completion.

Final second teardown exited0. Final project-label inventories for containers, volumes and networks each exited0 with empty output. Second root `.local` SHA256 comparison passed. The resolved host scratch was checked equal to the literal absolute path above, then removed with `Remove-Item -LiteralPath -Recurse -Force`; confirmed absent. Images/cache retained, unrelated project resources preserved. The earlier exact sandbox scratch path was also checked/removed if visible; its absence was verified, and the temporary documentation pointer was removed. Only this evidence document remains as the diagnostic change.
