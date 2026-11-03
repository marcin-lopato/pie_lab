"""Input boundary: read a finite file and return a list of standard records.

The CSV reader is your worked example. You implement JSON and JSON Lines.
Readers must not calibrate measurements or calculate statistics.
"""
import csv
import json
from pathlib import Path

from records import FIELDS, parse_record


def read_csv(path: Path) -> list[dict]:
    """WORKED EXAMPLE: read a header-based CSV file, stopping at the first bad row."""
    records = []
    # newline="" lets the CSV parser handle line endings; UTF-8-sig accepts a BOM.
    with Path(path).open(encoding="utf-8-sig", newline="") as stream:
        reader = csv.DictReader(stream)
        if reader.fieldnames is None or not set(FIELDS) <= set(reader.fieldnames):
            raise ValueError(f"{path}: CSV header must contain {', '.join(FIELDS)}")
        for row in reader:
            try:
                if None in row:  # DictReader uses None for unexpected extra fields.
                    raise ValueError("Too many columns in this CSV row.")
                records.append(parse_record(row))
            except ValueError as error:
                # Keep the filename and row location so that you can repair the input.
                raise ValueError(f"{path}: CSV line {reader.line_num}: {error}") from error
    return records


def read_json(path: Path) -> list[dict]:
    """YOUR TASK R1: load a JSON array; validate each object with parse_record.

    Require a list at the top level. Preserve order. An empty array returns [].
    Raise ValueError for invalid content; let file-access errors propagate.
    """
    # Start with `with Path(path).open(encoding="utf-8") as stream:`.
    # Use json.load(stream), check the container, then transform each object.
    path = Path(path)
    with path.open(encoding="utf-8") as stream:
        try:
            data = json.load(stream)
        except json.JSONDecodeError as error:
            raise ValueError(f"{path}: Invalid JSON content: {error}") from error

    if not isinstance(data, list):
        raise ValueError(f"{path}: JSON root must be a list/array.")

    records = []
    for index, item in enumerate(data):
        try:
            records.append(parse_record(item))
        except ValueError as error:
            raise ValueError(f"{path}: Invalid record at index {index}: {error}") from error
    return records


def read_jsonl(path: Path) -> list[dict]:
    """YOUR TASK R2: read one JSON object per non-blank line, preserving order.

    Use json.loads(line) and parse_record. Include the line number in a bad-row
    error. This first version returns a finite list; streaming is a later task.
    """
    # Open the file with `with`, enumerate lines from 1, and skip empty lines.
    records = []
    path = Path(path)
    with path.open(encoding="utf-8") as stream:
        for line_num, line in enumerate(stream, start=1):
            line_str = line.strip()
            if not line_str:
                continue
            try:
                row = json.loads(line_str)
                records.append(parse_record(row))
            except (json.JSONDecodeError, ValueError) as error:
                raise ValueError(f"{path}: JSON Lines line {line_num}: {error}") from error
    return records


def read_data(path: Path, file_format: str) -> list[dict]:
    """Choose a reader explicitly; do not guess the format from the filename."""
    # A short conditional is enough here. You do not need a plugin framework.
    if file_format == "csv":
        return read_csv(path)
    if file_format == "json":
        return read_json(path)
    if file_format == "jsonl":
        return read_jsonl(path)
    raise ValueError(f"Unsupported input format: {file_format!r}")
