"""Output boundary: save results without performing any analysis or calibration.

These are small file-writing services, not servers. Raw input stays in data/;
new products go to output/. The finite snapshot writers replace their target.
"""
import json
from pathlib import Path
from typing import Union


# Union[dict, list] means a dictionary or a list, without Python 3.10 union syntax.
def save_json(path: Path, data: Union[dict, list]) -> None:
    """WORKED EXAMPLE: write a readable JSON snapshot and create its parent folder."""
    # Serialise first: a non-serialisable value must not truncate an existing file.
    text = json.dumps(data, indent=2, ensure_ascii=False, allow_nan=False)
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text + "\n", encoding="utf-8")


def save_csv(path: Path, readings: list[dict]) -> None:
    """YOUR TASK W1: write a header and standard records, including for empty input.

    Use the FIELDS order from records.py, UTF-8, newline="", and csv.DictWriter.
    Create the parent folder. Replace the target; do not append duplicate snapshots.
    """
    # This output must be readable again by read_csv with the same record values.
    raise NotImplementedError("W1: implement the CSV writer in storage.py")


def save_jsonl(path: Path, readings: list[dict]) -> None:
    """YOUR TASK W2: write one complete JSON record per line, without an outer array.

    Create the parent folder. Replace the target. Empty input creates an empty file.
    Use allow_nan=False. Incremental appending belongs to the later streaming stage.
    """
    # This output must be readable again by your R2 reader.
    raise NotImplementedError("W2: implement the JSON Lines writer in storage.py")
