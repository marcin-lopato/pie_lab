"""Configure operational messages once, at application startup.

The supplied console setup works now. You extend it to keep a file log as well.
Do not add logging setup to readers or pure calculation functions.
"""
import logging
from pathlib import Path
from typing import Optional


LEVELS = {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}


# Optional[Path] means a Path or None; this spelling also works before Python 3.10.
def configure_logging(level: str = "INFO", log_path: Optional[Path] = None) -> None:
    """WORKED EXAMPLE + TASK L1: configure console and optional append-only file log."""
    if level not in LEVELS:
        raise ValueError(f"Unsupported logging level: {level!r}")
    handlers = [logging.StreamHandler()]
    if log_path is not None:
        # YOUR TASK L1: create the parent directory, then append a UTF-8 FileHandler.
        # Keep the StreamHandler too. Use append mode so earlier runs are retained.
        raise NotImplementedError("L1: add file logging in logging_service.py")

    # force=True prevents duplicate handlers when you rerun this small application.
    # This belongs to the entry point, not to a library imported by another program.
    logging.basicConfig(level=level, handlers=handlers, force=True,
                        format="%(levelname)s | %(name)s | %(message)s")
