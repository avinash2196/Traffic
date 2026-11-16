# Gemini live-verification setup

Prepared 2026-11-09. This guide prepares your credentials and samples; it does not start the application or make API calls. The implementation plan must be approved before live verification runs.

## 1. Generate the API key

1. Sign in to [Google AI Studio's API Keys page](https://aistudio.google.com/api-keys).
2. Select **Create API key**, choose or create the Google Cloud project you want to use, and name the key for this RoadWatch demo. New accounts may already have a default project/key.
3. Keep this key dedicated to the demo. If API restrictions are offered, restrict it to the Gemini API (`generativelanguage.googleapis.com`).
4. Check that the project can access the approved model, `gemini-3.8-flash`. Creating a key alone does not confirm model access or available quota. Do not select a different model to bypass an access error.

Google's [API-key guide](https://ai.google.dev/gemini-api/docs/api-key) describes project/key creation and restrictions. Button names may vary with your account.

## 2. Check billing and access

In AI Studio, check the project's plan under **Usage & Billing**. If the selected model requires paid access, follow Google's current billing setup for that project. Account verification, payment or credits may be required; use the amounts shown in your account rather than an assumed amount. See [Google's billing guide](https://ai.google.dev/gemini-api/docs/billing).

The approved demo has no application spending cap. Google's quota and billing requirements still apply. The three-total-attempt limit per job remains in force.

## 3. Store the key privately

From the Traffic repository folder, create the already-ignored local folder:

```powershell
New-Item -ItemType Directory -Force -Path .local | Out-Null
notepad .local\gemini-api-key.txt
```

Paste **only the key** into that local text file, save it, and close the editor. Do not include quotes or `GEMINI_API_KEY=`. This is a local plaintext secret file; keep it private. Do not paste the key into chat, source files, screenshots, or shell commands.

The repository already ignores `/.local/`. You can confirm the file is ignored without displaying its contents:

```powershell
git check-ignore .local/gemini-api-key.txt
```

Expected output is the filename, never the key. Do not force-add this folder to Git.

The application uses the `GEMINI_API_KEY` environment variable; it does **not** automatically load this text file. During approved verification, the key can be read privately from your designated file into the verification process. If you later configure a local application process yourself, load it without printing it:

```powershell
$env:GEMINI_API_KEY = (Get-Content -LiteralPath .local\gemini-api-key.txt -Raw).Trim()
$env:GEMINI_MODEL = 'gemini-3.8-flash'
```

These variables apply only to that PowerShell session and its child processes. They do not configure a different terminal or an already-running application. Do not print the environment or run a live request yet.

## 4. Prepare authorized samples

Keep samples in a private folder, for example `.local\ai-live-samples\`. Use only files you authorize sending to Google's Gemini service.

- Minimum for the first live capability check: one JPEG/PNG photo and one MP4/MOV/AVI video, each nonempty and at most **10 MiB**.
- For category review, provide helmet, triple-riding and red-light examples where available. Give your expected interpretation and known limitations; a staged or compliant example is useful too.
- Include a clearly unrelated indoor/food example and an unclear or no-apparent-violation example for routing checks. Mixed evidence can reuse a relevant clip and an unrelated image.
- A red-light assessment needs movement/signal context; a single photo may appropriately remain uncertain. Do not stage unsafe road behavior to create evidence.

Retain original files locally. Samples and keys must remain outside committed test fixtures and documentation. A full scenario checklist belongs to the approved live-verification protocol; missing samples will be recorded rather than replaced with fake live evidence.

## 5. Tell me the paths, not the secret

When ready, send:

```text
Key file: C:\Users\avina\Downloads\avinash-repo\v11\Traffic\.local\gemini-api-key.txt
Photo path(s): <absolute local path(s)>
Video path(s): <absolute local path(s)>
Expected category/context: <helmet / triple-riding / red-light / irrelevant / unclear>
Authorized to send these samples to Google: yes
```

Do not include the actual API key. Supplying these paths prepares inputs; it does not approve an implementation plan that has not yet been reviewed. Live verification will use the approved model, record sanitized results and actual failures, and leave final violation/award decisions to officers.
