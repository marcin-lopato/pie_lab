"""Start here: a deliberately small, finite, uncalibrated demonstration.

Run `python run.py` from the project folder. It works before you solve any task.
Read the comments in main() to find where your completed pieces will connect.
"""
import logging
import sys
from pathlib import Path

from analysis import basic_summary, select_series
from logging_service import configure_logging
from readers import read_data
from storage import save_json

# Paths start beside this script, not in whichever directory your terminal uses.
ROOT = Path(__file__).resolve().parent
LOGGER = logging.getLogger(__name__)

# These intentionally visible choices become a JSON configuration in Extension 1.
INPUT_PATH = ROOT / "data" / "tiny.csv"
INPUT_FORMAT = "csv"
SELECTION = {"room": "laboratory", "sensor_id": "station-01", "metric": "temperature"}
OUTPUT_PATH = ROOT / "output" / "baseline.json"


def main() -> None:
    """Read -> select -> summarise -> save. Keep the order visible and easy to edit."""
    configure_logging()
    readings = read_data(INPUT_PATH, INPUT_FORMAT)
    LOGGER.info("Read %d records from %s", len(readings), INPUT_PATH.name)

    # After E1, inspect all readings here, before you narrow the data to one series.
    selected = select_series(readings, **SELECTION)
    LOGGER.info("Selected %d records for %s", len(selected), SELECTION)

    # After C1, build a NEW calibrated list here; never modify readings in place.
    # This baseline deliberately does not call the unfinished calibration task.
    LOGGER.warning("Baseline only: calibration is NOT applied.")
    values = [reading["value"] for reading in selected]
    summary = basic_summary(values)
    print("Uncalibrated summary:", summary)

    # A small envelope records what this result means; False is not a placeholder.
    save_json(OUTPUT_PATH, {"calibration_applied": False, "series": SELECTION,
                            "readings": selected, "summary": summary})
    LOGGER.info("Saved %s", OUTPUT_PATH)
    # After W1, also save your processed readings as a separate CSV snapshot.


if __name__ == "__main__":
    # Reject extra arguments rather than pretend the future configuration mode works.
    if len(sys.argv) > 1:
        raise SystemExit("Run only: python run.py. Configuration arguments are your X4 task.")
    # Imports remain quiet. A failed run has a nonzero exit code, not a false success.
    try:
        main()
    except (OSError, ValueError, NotImplementedError) as error:
        LOGGER.error("Run stopped: %s", error)
        raise SystemExit(1) from error
