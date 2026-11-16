# MP4 upload diagnostic — 2026-11-11

User authorized diagnostic logging only; no application behavior, test-source, dependency or runtime configuration changes. This is diagnosis, not M08D completion or live OpenAI acceptance.

## Findings

The originally failing synthetic MP4 is valid in the instrumented isolated runtime. One focused upload test passed in6.66s. The exact original15-node predecessor sequence then passed in24.15s, including JPEG/PNG, MP4, MOV, AVI and46-second MP4. This second run specifically examined preceding-test interaction; it was not an unchanged retry to erase a failure. The historical400 INVALID_MEDIA remains unresolved; neither successful run establishes its cause or demonstrates that it is fixed.

For the focused896-byte MP4 (SHA256 fd9083c5ca5abacecc023d4ab1ef38f33281b91eebea45ffeeb81068c66088f1), ffprobe returned0,16x16 video, duration1.0s, and empty stderr. Its complete application-side subprocess elapsed1.071s. ffmpeg full decode returned0, empty stdout/stderr, elapsed0.887s. Both consumed identical hash-verified synthetic bytes. The unchanged HTTP upload test established201 acceptance, returned file metadata/hash, and authenticated byte-for-byte media retrieval.

## Captured stages

Synthetic fixture bytes embedded in the existing test → real local HTTP upload/multipart parser → validation entry/MIME/length → temporary file → resolved decoder wrapper and exact arguments → private stdin forwarding into pinned offline FFmpeg/FFprobe container → exit codes/stdout/stderr/timing → unchanged HTTP assertions → JUnit named outcomes. `application.jsonl` includes exception trace events, should validation throw; none did in these runs. No actual file-generation process occurs during these tests: fixtures were generated earlier and embedded as base64. No AI/provider call, real user evidence, real database or key was used.

The diagnostic plugin observed subprocess execution and validation exceptions in the disposable copy; the decoder helper added logging around unchanged forwarded commands. No production file was patched. Trace observation can affect timing, so these runs cannot rule out scheduling/timing-sensitive failures. The original failing run did not retain decoder stderr, preventing retrospective root-cause confirmation.

## Artifacts

- [Single-case test log](MP4-Diagnostics-2026-11-11/single/pytest.log), [application trace](MP4-Diagnostics-2026-11-11/single/application.jsonl), [decoder trace](MP4-Diagnostics-2026-11-11/single/decoder.jsonl), [JUnit](MP4-Diagnostics-2026-11-11/single/result.xml).
- [Exact15-node sequence log](MP4-Diagnostics-2026-11-11/sequence/pytest.log), [application trace](MP4-Diagnostics-2026-11-11/sequence/application.jsonl), [decoder trace](MP4-Diagnostics-2026-11-11/sequence/decoder.jsonl), [JUnit](MP4-Diagnostics-2026-11-11/sequence/result.xml).
- Driver scripts, observation plugin, decoder helper and source hashes are retained in that directory to review the diagnostic setup. Events include exact commands, owned paths, image/tool versions and start/end state; no environment dump, credentials or external provider payloads.

## Isolation and limits

Exact pinned image sha256:f3b04288897b10d8d6f605460bd416fac376b3b13bd29797922f843bd88f05de, network none, zero mounts. Source-only copy, filtered environment, owned native Temp fixture root, explicit pytest-asyncio and local loopback. First child180s bound; predecessor sequence300s. Decoder production60s bounds unchanged. Checkout root/test Python hashes unchanged; owned carriers absent after each run. Diagnostic temporary copy removed after archiving only logs/scripts, not synthetic database/media state. No staging/commit.

Next useful step is to retain these diagnostics during any authorized remaining verification or a representative real-video run. No application fix is supported by current evidence. Full upload→AI→officer workflow remains unverified and is not claimed here.
