"""Use the existing G1 core without copying or mutating validated G1 source."""
import sys
from pathlib import Path

source = Path(__file__).resolve().parents[2] / "workshop_g1"
if str(source) not in sys.path:
    sys.path.insert(0, str(source))
from workshop_g1.core import create_workspace, inspect_workspace, verified_trust, safe_display  # noqa: E402


def trusted_bundle():
    if getattr(sys, "frozen", False):
        return Path(sys._MEIPASS) / "workshop_g1" / "trusted"
    return source / "workshop_g1" / "trusted"
