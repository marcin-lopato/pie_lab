"""EXTENSION 1: a small configuration-file service, not a framework.

Leave this module alone until your first finite pipeline works. The default run
uses explicit choices in run.py and does not call these unfinished functions.
The exact contract and an example are in EXTENSION_1.md and config/example.json.
"""
import json
from pathlib import Path


def validate_config(config: dict) -> None:
    """YOUR TASK X1: validate required sections, values, and supported choices.

    Raise ValueError with a useful field name for bad configuration. Do not silently
    replace a bad value with a default. Do not change the supplied dictionary.
    See the validation table in EXTENSION_1.md for the deliberately small schema.
    """
    # Separate this pure validation step from reading the configuration file.
    raise NotImplementedError("X1: validate configuration in configuration.py")


def resolve_paths(config: dict, base_dir: Path) -> dict:
    """YOUR TASK X2: return a copy with file paths resolved against base_dir.

    Resolve input.path, output.readings_path, output.summary_path, and the optional
    logging.path. Do not change config. Keep a null log path as None. Reject any
    collision between the input, output and log files after resolving their paths.
    This step computes paths only: do not create directories or write files.
    """
    # A nested dictionary needs nested copies (or deepcopy), not just config.copy().
    raise NotImplementedError("X2: resolve configuration paths in configuration.py")


def load_config(path: Path) -> dict:
    """Assembly is supplied: read once, validate, resolve; return prepared settings."""
    path = Path(path).resolve()
    with path.open(encoding="utf-8") as stream:
        config = json.load(stream)
    validate_config(config)
    result = resolve_paths(config, path.parent)
    # Protect the configuration file itself from becoming an output or log target.
    targets = [result["output"]["readings_path"], result["output"]["summary_path"],
               result["logging"]["path"]]
    if path in targets:
        raise ValueError("An output/log path must not overwrite the configuration file.")
    return result
