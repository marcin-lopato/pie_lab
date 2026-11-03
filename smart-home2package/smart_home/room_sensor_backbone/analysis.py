"""Pure selection and finite-data analysis. There is no file or logging code here.

An Iterable can be a list or an iterator. These functions still produce finite
results: accepting an Iterable does NOT make whole-data analysis safe on infinity.
"""
from collections.abc import Iterable
from statistics import fmean


def select_series(readings: Iterable[dict], room: str, sensor_id: str,
                  metric: str) -> list[dict]:
    """WORKED EXAMPLE: select exactly one room/sensor/metric combination."""
    # We create a new list, but do not copy or modify the contained dictionaries.
    return [r for r in readings
            if (r["room"], r["sensor_id"], r["metric"]) == (room, sensor_id, metric)]


def basic_summary(values: list[float]) -> dict:
    """WORKED EXAMPLE: count, mean, minimum and maximum for one finite series."""
    # An empty selection is not a collection of zero-valued measurements.
    if not values:
        return {"count": 0, "mean": None, "minimum": None, "maximum": None}
    return {"count": len(values), "mean": fmean(values),
            "minimum": min(values), "maximum": max(values)}


def explore_data(readings: list[dict]) -> dict:
    """YOUR TASK E1: describe what is present, before interpreting the values.

    Return record_count, sorted rooms, sorted sensor_ids, sorted metrics,
    time_start/time_end (None if empty), and series: a list of dictionaries with
    room, sensor_id, metric, unit, count. Sort series by room/sensor_id/metric.
    Use actual times, not row positions; input records need not be time-sorted.
    """
    # Count each (room, sensor_id, metric) separately. Do not calculate a mixed-unit mean.
    raise NotImplementedError("E1: implement data exploration in analysis.py")


def extended_summary(values: list[float]) -> dict:
    """YOUR TASK S1: extend basic_summary with median and sample_sd.

    sample_sd uses n-1, and is None for fewer than two values. For no values,
    median is also None. Reuse basic_summary instead of rewriting its fields.
    """
    # The statistics module supplies median and stdev; decide when they are defined.
    raise NotImplementedError("S1: implement the extended summary in analysis.py")


def summarise_by_series(readings: list[dict]) -> list[dict]:
    """YOUR TASK S2: return one independently calculated summary per series.

    Each output dictionary has room, sensor_id, metric, unit, and summary.
    summary is the result of extended_summary for that group's values.
    Sort the output by room/sensor_id/metric. Empty input returns [].
    """
    # Group by the complete three-part key, then analyse each group separately.
    raise NotImplementedError("S2: implement grouped summaries in analysis.py")
