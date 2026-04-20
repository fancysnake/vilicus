import hashlib
import os
import re
import tempfile
from pathlib import Path

TMUX_CONF_PATH: Path = Path(__file__).parent.parent / "conf" / "tmux.conf"

_SLUG_CLEAN = re.compile(r"[^a-z0-9]+")
STEM_DIGEST_LENGTH = 6

IDLE_THRESHOLD_SECONDS = 3.0
ATTENTION_POLL_INTERVAL_SECONDS = 1.0
ATTENTION_WINDOW_STATUS_STYLE = "bg=red,fg=white,bold"


def _slug(value: str) -> str:
    cleaned = _SLUG_CLEAN.sub("-", value.lower()).strip("-")
    return cleaned or "root"


def stem_for_cwd(cwd: Path) -> str:
    absolute = cwd.resolve()
    name = _slug(absolute.name)
    digest = hashlib.sha256(str(absolute).encode()).hexdigest()[:STEM_DIGEST_LENGTH]
    return f"vekna-{name}-{digest}"


def daemon_socket_path() -> str:
    return str(Path(tempfile.gettempdir()) / f"vekna-{os.getuid()}.sock")
