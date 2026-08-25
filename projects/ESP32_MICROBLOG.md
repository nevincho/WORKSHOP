# ESP32 MicroBlog + AGENT 32 — WORKSHOP Project Profile

STATUS: REGISTERED / NOT ACTIVE

## Authority
- Project documentation repository: `nevincho/nova`
- Documentation branch: `esp32-microblog-agent32`
- Documentation path: `ESP32_MICROBLOG/`
- Active local implementation workspace is authoritative for source/build/hardware state until a dedicated code repository is established: `D:\RaspberryPi5\ЕСП32_БЛОГ`
- Do not infer local implementation state from the documentation branch.

## Current documented engineering state
- Product is active development / pre-release validation.
- Current lean source direction: `ESP32_MicroBlog_v0.7_AGENT32_LEAN`.
- v0.6.1 physically worked and measured approximately 1,168,239 / 1,310,720 bytes application flash and 50,420 / 277,260 bytes RAM.
- v0.7 requested lean removals were implemented, but final v0.7 compile/runtime is NOT VERIFIED.
- Last proven blocker was environment/toolchain related: ESP32 core preprocess/library-detection stall reproduced with a minimal Wi-Fi sketch.
- ESP32 core/toolchain update to 3.3.11-era components was started; post-update result is NOT VERIFIED.

## Product boundaries
Keep the product small and local-first. Do not introduce SaaS, fleet management, public hosting, local LLM inference, database server, ecommerce, analytics platform, or broad cloud architecture without a new verified requirement.

## Release target
Primary release target should be Offline RC first. Connected Mode and Web Search are optional and must not block an otherwise stable offline release.

## Protected / preserve
- Preserve known working v0.6.1 baseline.
- Do not modify v0.7 merely because of the previously isolated toolchain stall.
- Preserve AP/local-site/admin/persistence behavior unless a verified defect requires change.
- Customer release archive must be binary-only; no source/internal artifacts.

## Execution routing
- Repository-only audit/planning may be autonomous.
- Local compile/upload/hardware validation requires an authorized Windows execution route and physical ESP32 access.
- Codex may be used only through Codex Gate for justified implementation/debugging work; do not spend Codex capacity on inventory or documentation-only work.
- Physical hardware validation is a human/live gate unless an explicitly verified automated hardware route exists.

## Current priority
NOT SET. Registration in WORKSHOP does not change the existing active project priority order.
