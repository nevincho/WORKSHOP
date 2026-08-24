# TASK-008 — IMOU IPC-K7C LAN evidence — 2026-08-24

SOURCE: Direct human-run PowerShell evidence supplied by Vlad from the Windows machine on the same LAN.

## Device identity supplied
- Product label: CruiserSE+-F757
- Model: IPC-K7C
- Device SN: E6896BDPCG9F757
- Firmware: 2.801.0000000.1.R.240815
- Network name: NOMI-IPC-K7C-3H1WE1-F757
- MAC: 1C:4D:89:DA:58:6F
- Camera IPv4: 192.168.0.154/24
- Windows source IPv4 observed by Test-NetConnection: 192.168.0.31
- Link: Wi-Fi 2.4 GHz

## Direct connectivity evidence
PowerShell `Test-NetConnection` results supplied by Vlad:
- 192.168.0.154 TCP/554: `TcpTestSucceeded : True`
- 192.168.0.154 TCP/80: `TcpTestSucceeded : True`
- 192.168.0.154 TCP/443: `TcpTestSucceeded : False`
- Ping: success, reported RTT 3 ms

## What this proves
- Camera is reachable from the Windows host over the local LAN at 192.168.0.154.
- A TCP listener is reachable on port 554.
- A TCP listener is reachable on port 80.
- Standard HTTPS port 443 was not reachable in this test.

## What this does NOT prove
- RTSP stream endpoint/path: NOT VERIFIED.
- Successful RTSP authentication: NOT VERIFIED.
- Successful frame/video retrieval: NOT VERIFIED.
- ONVIF service endpoint/discovery on this exact device/firmware: NOT VERIFIED by direct local test.
- PTZ/control API: NOT VERIFIED.
- Local credentials: intentionally NOT stored in WORKSHOP.

## Security / handling
Do not commit camera passwords, safety codes, Imou account credentials, or other secrets. Runtime credentials must be handled outside the repository through the approved local secret/config mechanism once that mechanism is verified.

## TASK-008 impact
This evidence may be used when TASK-008 becomes eligible. It does NOT unblock TASK-008 by itself and does NOT constitute live operational PASS. TASK-008 prerequisites and dependency gates remain authoritative.
