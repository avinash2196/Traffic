# Local Git and CI deferral — 2026-10-26

## User decision and authority

The user answered "yes" to "Shall we initialize local Git and defer hosted CI?" This records that specific decision (requirements Q28), not approval of a new executable plan or a hosted run. Existing reviewed requirements/Plan/Foundation documents are updated only for this CI gate and completion bookkeeping. All runtime checks, security rules, supported versions and later PDD review gates remain intact.

## Effective gate

Use local Git now. Retain .github/workflows/provider-free.yml for future GitHub publishing. Hosted execution is deferred and does not block Foundation completion or subsequent local PDD work. CI must remain provider-free when activated. No hosted run is claimed, and no publishing or remote creation is authorized here.

DP-M02 is complete against its revised gate: three full local checks passed, including repeat without cleanup and after restart; verified HTTPS/OIDC/JWKS, ten process identities, SQL/media/browser/telemetry, collector span receipt, all five empty domain databases, isolated internal networking and disabled AI. Actual commands/results and cleanup remain in DP-M02-Browser-Execution-2026-10-26.md. Earlier failures/waits remain historical evidence.

## Local Git evidence

- git init -b main: exit 0, initialized empty Git repository in this workspace.
- git check-ignore .local/private/tls.key .local/private/reporting.dsn .venv/Scripts/python.exe: exit 0, all three paths ignored.
- git remote -v: exit 0, empty output.
- No staging, commit, remote creation or push was performed. Existing .gitignore excludes generated private state and the virtual environment.
- Final verification used binary NUL-separated `git check-ignore -z --stdin`: all 24 actual generated private/environment paths were ignored. `git ls-files` and `git remote -v` were empty; `git symbolic-ref --short HEAD` returned main. Document checks confirmed Q28, completed DP-M02, and Pending DP-M03. The initial text-mode stdin probe included Windows carriage returns in its diagnostic input; the binary probe verified the actual paths without that translation.

## Next boundary

DP-M03 Identity RED remains Pending. Its own fresh-context Implementation Plan and human review are required before any test or product code is changed. Live AI spending remains disabled pending its independent approval.
