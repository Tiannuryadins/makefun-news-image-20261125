#!/usr/bin/env python3
"""Entry point for the news-image-20261125 submission.

The poster artwork is produced by render_poster.py and saved as
poster.png beside this file. This entrypoint's only job is to place
that finished poster at the path the grader expects:
$MAKEFUN_OUTPUT_DIR/entry.png (or ./output/entry.png when the
environment variable is absent), then report the file's size and
SHA-256 digest so the run log can be checked for reproducibility.
"""

import hashlib
import os
import sys
from pathlib import Path


def script_folder() -> Path:
    """Folder holding this file, resolved without symlinks."""
    return Path(__file__).resolve().parent


def destination_folder() -> Path:
    """Where the graded entry image must land.

    Honours MAKEFUN_OUTPUT_DIR when the harness sets it; otherwise
    falls back to an 'output' folder next to this script.
    """
    configured = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if configured:
        return Path(configured).expanduser()
    return script_folder() / "output"


def digest_file(path: Path) -> str:
    """SHA-256 hex digest of a file, streamed in 64 KiB chunks."""
    hasher = hashlib.sha256()
    with path.open("rb") as handle:
        while True:
            block = handle.read(65536)
            if not block:
                break
            hasher.update(block)
    return hasher.hexdigest()


def place_poster() -> int:
    """Copy poster.png to the graded location and describe it."""
    here = script_folder()
    source = here / "poster.png"
    if not source.is_file():
        print(f"missing source poster: {source}", file=sys.stderr)
        return 1

    target_dir = destination_folder()
    target_dir.mkdir(parents=True, exist_ok=True)
    target = target_dir / "entry.png"

    # Byte-for-byte transfer through pathlib (no shutil dependency).
    target.write_bytes(source.read_bytes())

    size = target.stat().st_size
    fingerprint = digest_file(target)
    print(f"wrote {target} ({size} bytes)")
    print(f"sha256: {fingerprint}")
    return 0


if __name__ == "__main__":
    raise SystemExit(place_poster())
