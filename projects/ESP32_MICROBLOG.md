# ESP32 MicroBlog + AGENT 32 — WORKSHOP Project Profile

STATUS: REGISTERED / NOT ACTIVE

## Project role
This is an independent commercial software product line. It is not an architectural dependency of TANGRA, VK, Horoscopes/Mysticarium, or any other project.

Primary business purpose: reach a sale-ready software product that can generate external revenue and help fund the user's other project lines. Any financial linkage is business-level only; there is no technical coupling.

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

## Commercial objective
Engineering decisions should optimize for shortest safe path to a supportable, sale-ready software package rather than feature expansion. Release quality, installer reliability, reproducibility, support burden, and customer acceptance are higher priority than optional capability growth.

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

## Scheduling / priority semantics
This project is managed as a separate commercial/funding track. It must not inherit dependencies from VK/Horoscopes/TANGRA and must not block their technical pipelines. Registration in WORKSHOP does not change the existing technical project priority order unless an explicit commercial-priority decision is recorded.
