# TASK-009 — Echo Show 5 Gen 2 future research

Date: 2026-08-27
Status: FUTURE_RESEARCH / NO FLASH AUTHORIZED
Source: owner clarification plus preliminary web research; implementation/runtime remains NOT VERIFIED.

## Confirmed owner hardware

- Device: Amazon Echo Show 5, 2nd generation.
- Intended VK role is not primarily Alexa calling. Target role is a room multimodal endpoint:
  - microphone input for VK;
  - speaker/audio output for VK;
  - camera input as an additional VK vision sensor;
  - touchscreen/display as an optional VK/ChatGPT terminal.

## Candidate routes for research

1. Stock Fire OS / official Amazon integration.
   - Determine exactly which Alexa Skills / Smart Home / RTC / media interfaces can be used by VK.
   - Do not infer raw access to built-in microphone, camera, or speaker from ordinary Alexa consumer capabilities.

2. Echo Show 5 Gen 2 (`cronos`) community unlock / LineageOS route.
   - Investigate current repeatable bootloader/root/reflash procedure and hardware-revision/firmware prerequisites.
   - Verify recovery/rollback options before any destructive operation.
   - Verify actual LineageOS support separately for Wi-Fi, touchscreen, display, camera, microphone/audio capture, speaker/audio output, hardware privacy controls/buttons, suspend/wake, thermals, and long-running stability.
   - Camera support has promising community evidence but must be independently verified for the exact device/build before acceptance.

3. Dedicated VK satellite architecture if LineageOS route is viable.
   - Echo node performs only sensor/audio/UI endpoint duties.
   - Heavy AI inference remains on the authoritative VK Windows runtime.
   - Candidate data path: camera/microphone -> local VK node service -> LAN -> VK Core; VK TTS/audio/UI -> LAN -> Echo node.
   - Preserve VK Core, canonical personality, and approved-memory boundaries.

4. Optional ChatGPT Android terminal.
   - Research whether the selected LineageOS build/API level supports current ChatGPT Android requirements.
   - Verify GApps/Play Services compatibility if the official Android app requires them.
   - Browser access is a separate fallback.
   - ChatGPT application must remain architecturally separate from VK sensor/control interfaces unless a later task explicitly designs an integration.

## Required gates before reflashing

- Exact model/board/hardware revision verified.
- Current Fire OS build recorded.
- Known-compatible unlock/reflash path verified for that revision/build.
- Backup/recovery/rollback procedure verified.
- Camera + microphone + speaker support demonstrated for the proposed LineageOS build.
- Risk of permanent brick assessed and explicitly accepted by owner.
- No flash or destructive action without a new explicit human authorization.

## Current conclusion

Echo Show 5 Gen 2 is a credible candidate for a dedicated VK multimodal satellite, potentially more useful under a lightweight LineageOS installation than stock Fire OS. This is a research hypothesis, not validated implementation state. TASK-009 remains blocked until a permitted and technically verified integration route is established.
