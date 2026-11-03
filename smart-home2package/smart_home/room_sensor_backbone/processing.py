"""EXTENSION 1: one pure function to connect your finite-data calculations.

Do this after the individual tasks. This file is not a second application runner.
Reading files, configuring logs, printing and saving still belong in run.py.
"""
from collections.abc import Iterable


def process_readings(readings: Iterable[dict], selection: dict,
                     calibration: dict) -> dict:
    """YOUR TASK X3: select -> optionally calibrate -> calculate extended_summary.

    Return {"readings": processed_records, "summary": statistics,
            "calibration_applied": calibration["enabled"]}.
    Use the selection keys room/sensor_id/metric and calibration keys
    enabled/scale/offset. Apply the coefficients ONLY to the selected series.
    Leave all input records and settings unchanged. Consume the source once.
    The output is a finite snapshot: it is not an infinite-stream processor.
    """
    # Reuse select_series, calibrate_reading and extended_summary.
    # A clear list comprehension is functional Python too; no large lambda is needed.
    raise NotImplementedError("X3: connect the pure processing steps in processing.py")
