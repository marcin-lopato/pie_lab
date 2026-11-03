"""Pure calibration functions: input values in, corrected values out.

Calibration never opens a file, reads configuration, prints, or writes a log.
You pass coefficients as arguments. See task C1 in STUDENT_GUIDE.md.
"""
from math import isfinite


def calibrate_value(value: float, scale: float = 1.0, offset: float = 0.0) -> float:
    """WORKED EXAMPLE: apply y = scale * x + offset in the same physical unit."""
    # These are supplied coefficients, not a fit to a reference measurement.
    result = scale * value + offset
    if not isfinite(result):
        raise ValueError("Calibration produced a non-finite value.")
    return result


def calibrate_reading(reading: dict, scale: float, offset: float) -> dict:
    """YOUR TASK C1: return a new record with only its value changed.

    Call calibrate_value. Keep time, room, sensor_id, metric, and unit unchanged.
    The original dictionary must remain untouched; never calibrate it in place.
    """
    # Copy the record, calculate the new value, and return your copy.
    raise NotImplementedError("C1: implement record calibration in calibration.py")
