"""WORKSHOP Desktop V1 candidate: GUI and fixed isolated process entrypoints."""
import sys


def main():
    if len(sys.argv) >= 2 and sys.argv[1] == "--worker":
        from workshop_desktop.worker import main as worker
        return worker(sys.argv[2:])
    if len(sys.argv) >= 2 and sys.argv[1] == "--reviewer":
        from workshop_desktop.reviewer import main as reviewer
        return reviewer(sys.argv[2:])
    if len(sys.argv) == 2 and sys.argv[1] == "--selftest-g1":
        from workshop_desktop.g1_adapter import trusted_bundle, verified_trust
        verified_trust(trusted_bundle())
        return 0
    if len(sys.argv) == 2 and sys.argv[1] == "--revoke-credentials":
        from workshop_desktop.vault import WindowsVault, TARGET, SIGNING
        vault = WindowsVault()
        vault.delete(TARGET)
        vault.delete(SIGNING)
        return 0
    if len(sys.argv) != 1:
        print("Unsupported command", file=sys.stderr)
        return 2
    from workshop_desktop.gui import main as gui
    gui()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
