# TASK-008 — IMOU IPC-K7CP LAN / RTSP evidence

SOURCE: Direct human-run Windows and VLC evidence supplied by Vlad from the Windows machine on the same LAN.

## Device identity
- Product: IMOU Cruiser SE+
- Exact model from physical device label: `IPC-K7CP-3H1WE`
- Device SN: `E6896BDPCG9F757`
- Firmware previously supplied: `2.801.0000000.1.R.240815`
- MAC: `1C:4D:89:DA:58:6F`
- Camera IPv4: `192.168.0.154/24`
- Windows source IPv4: `192.168.0.31`
- Link: Wi-Fi 2.4 GHz

## Direct connectivity evidence
- TCP/554: VERIFIED reachable.
- TCP/80: VERIFIED reachable.
- TCP/443: connection failed in the supplied test.
- Ping: success, reported RTT 3 ms.

## Direct RTSP evidence
A local VLC test was performed against the camera.

Observed result:
- Local RTSP authentication accepted: VERIFIED.
- RTSP `channel=1`, `subtype=1` displayed real video successfully in VLC: VERIFIED.
- Local LAN video retrieval: VERIFIED.

Main stream observation:
- `subtype=0` timing advanced in VLC but no visible picture was obtained during the test.
- Main-stream decode/display: NOT VERIFIED.
- This does not invalidate the working `subtype=1` stream.

## Remaining NOT VERIFIED capabilities
- ONVIF discovery/service endpoint on this exact device/firmware.
- PTZ/control API.
- Main RTSP stream usable video.
- VK runtime ingestion of the stream.

## Security
Local camera authentication material was used successfully but is intentionally NOT stored in WORKSHOP/GitHub. Do not commit camera passwords, safety codes, account credentials, or other secrets.

## TASK-008 impact
The local-network video prerequisite for IMOU integration is now directly demonstrated for RTSP substream 1. This does not by itself establish VK integration or LIVE_VALIDATED status, and existing dependency gates remain authoritative.
