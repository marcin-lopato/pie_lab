# Your first assignment: a finite sensor-data pipeline

You have received a folder containing a small working program. Your task is to
extend it without turning every file into a second copy of the main script. Each
function should have a job that you can describe in one sentence.

By the end of this assignment you should be able to run a finite analysis that
reads one of several file formats, reports what data is present, selects a
measurement series, calibrates it, calculates statistics, and saves both results
and an operational log. You are not building a continuously running service yet.

## Step 0 — Follow one reading through the code

Run `python run.py` before changing anything. Open `data/tiny.csv`, then
`output/baseline.json`. Match the three values by hand. The mean should be 21 C.
The word **uncalibrated** is intentional: the baseline does not pretend that your
unfinished calibration already works.

Read `run.py` from top to bottom. It is the place where actions are ordered. Then
open the function that each line calls. Notice that importing `analysis.py` does
not read a file or print a result. That behaviour belongs to calling a function,
not importing its definition.

Make a prediction before each small experiment. Change the selected room to
`office` while still reading `tiny.csv`: what should happen? You should obtain an
empty selection, a count of zero and `None` statistics, not fabricated zero-valued
measurements. Restore the selection before continuing.

**Your first checkpoint:** explain the difference between the raw readings,
selected readings, numerical values, summary dictionary and saved JSON file.
They are related, but they are not the same object.

## R1 — Add a JSON reader

Open `readers.py`. The CSV example already supplies the pattern: open a file,
decode its contents, pass each raw row through `parse_record`, return records.
Implement `read_json(path)` using the same common parser.

The agreed JSON format is a top-level **array of reading objects**. It is not an
object containing a `readings` field. Check the top-level container so that a
wrongly structured document produces a useful `ValueError`, rather than a
confusing failure somewhere later in the pipeline. An empty array is valid.
Preserve record order. Let a file-access error, such as a missing file, remain an
error; do not convert it into an empty dataset.

You will need `json.load`, so add the corresponding import. Use `with` to make
ownership of the open file clear. The parser handles the difference between CSV
text values and JSON numbers; you should not duplicate that logic.

After implementing your function, try this in a Python session opened in the
project folder:

```python
from pathlib import Path
from readers import read_csv, read_json

csv_records = read_csv(Path("data/readings.csv"))
json_records = read_json(Path("data/readings.json"))
print(len(json_records))                 # Expect 36.
print(csv_records == json_records)       # Expect True.
```

**You are done when:** the two files produce equal lists, `[]` produces an empty
list, and malformed JSON, a wrong top-level container and a bad record do not
quietly succeed.

## R2 — Add a JSON Lines reader

A JSON Lines file has one complete JSON object on each non-blank line. The file
as a whole is not a single JSON array. Implement `read_jsonl(path)` by reading
lines, decoding one line at a time with `json.loads`, and using `parse_record`.

Skip blank lines. Do not skip malformed non-blank lines. Include the filename
and line number in your error message. Keep the first version straightforward:
return a list, just like the other readers. You will revisit this function when
you introduce generators.

Check that all three readers return the same 36 records. Then make a temporary
copy of the JSON Lines file, insert an invalid line, and check that you can locate
the problem from the error. Do not damage the supplied reference input.

**Think about it:** reading lines one at a time is not enough to guarantee bounded
memory. Your function still appends every reading to a list. That is acceptable
for this assignment; recognising the limitation is important for the next one.

## E1 — Explore the dataset before interpreting it

Implement `explore_data(readings)` in `analysis.py`. The function returns a
dictionary; it does not print the report. You may print or save that dictionary
in `run.py`. Keeping those responsibilities separate lets you reuse the function
later in a notebook or another interface.

Return the following keys:

| Key | Required result |
|---|---|
| `record_count` | Total number of records. |
| `rooms` | Sorted list of unique room names. |
| `sensor_ids` | Sorted list of unique station IDs. |
| `metrics` | Sorted list of unique metric names. |
| `time_start`, `time_end` | Earliest/latest timestamp text, or `None` for empty input. |
| `series` | Sorted list of `{room, sensor_id, metric, unit, count}` dictionaries. |

Find the actual time bounds; do not assume the first and last rows are already
ordered. Use parsed timestamps for time comparisons. Sort the series list by
`(room, sensor_id, metric)` so that repeated runs are easy to compare.

For the larger dataset you should find **36 records, two rooms, two stations,
three metrics and six distinct series**, each with six observations. The time
bounds are 12:00 to 12:05 UTC on 1 October 2026. For an empty input, return zero,
empty lists and `None` time bounds.

Do not calculate an overall mean of all 36 values. Such a number would mix C,
percent and hPa, and would not answer a meaningful physical question. Exploration
starts with understanding identity, coverage and quantity, not merely calling a
statistical function on every number available.

**You are done when:** your report is correct for the normal file, a reversed copy
of the records, and an empty list. Your function must not change its argument.
A plot is not required yet; the structured report is your exploration product.

## C1 — Calibrate records without losing the originals

Open `calibration.py`. The supplied `calibrate_value` demonstrates the correction:

```text
corrected value = scale × measured value + offset
```

The scale is dimensionless. The offset has the same unit as the selected physical
quantity. Here you use supplied teaching coefficients; you are not fitting a
calibration curve or estimating uncertainty from reference measurements.

Implement `calibrate_reading(reading, scale, offset)`. Reuse the scalar function.
Return a **new dictionary** with the corrected value. Leave the original
untouched, and preserve its timestamp, room, sensor ID, metric and unit.

Try scale 1.02 and offset -0.4 on the tiny temperature series. Your new values
should be approximately 20.00, 21.02 and 22.04 C. Ordinary floating-point arithmetic
may display more decimal digits; compare with a tolerance rather than requiring
identical decimal text. Round for display, not before the statistical analysis.

Use separate names such as `raw_readings`, `selected_readings`, and
`calibrated_readings`. For now, select one series **before** applying its
coefficients. A temperature offset must not accidentally be applied to humidity
and pressure just because they came from the same station.

**You are done when:** the new values are right, the original list/dictionaries are
unchanged, and calling the function twice on the same raw record gives equal
results. Also check scale 1 and offset 0: it still returns a new record.

## S1 — Extend the summary

Implement `extended_summary(values)` in `analysis.py`. Start with the existing
`basic_summary` result and add `median` and `sample_sd`. Do not copy its mean/min/max
implementation into a second function.

Use the **sample standard deviation**, with denominator n-1. The `statistics`
module calls this `stdev`; `pstdev` is a different calculation. Handle small
samples before calling functions that require more values.

| Input | Important expected values |
|---|---|
| `[20.0, 21.0, 22.0]` | count 3, mean 21, median 21, sample_sd 1. |
| `[20.0]` | mean/median/minimum/maximum 20, sample_sd `None`. |
| `[]` | count 0; all numerical summary fields `None`. |

Why `None` instead of zero? Zero is a measured or calculated value. `None` says
that this statistic is not defined from the available observations. JSON will
represent it as `null` when you save the result.

**You are done when:** all three cases behave as specified, and your input list is
unchanged. Keep this function free of printing, logging and file operations.

## S2 — Analyse multiple series without mixing them

Implement `summarise_by_series(readings)`. Group using the complete
`(room, sensor_id, metric)` key. Extract values from one group at a time and reuse
`extended_summary`. Return a sorted list of dictionaries containing `room`,
`sensor_id`, `metric`, `unit`, and a nested `summary` dictionary. Empty input
returns an empty list.

The supplied full dataset must produce six summaries. Its laboratory temperature
mean is 21 C; its office temperature mean is 23.5 C. These are separate results.
Do not first compute a combined mean and copy it into six output dictionaries.

This task analyses the values you give it. For an initial all-series exploration,
you may supply raw readings and label the results as uncalibrated. To analyse
calibrated series later, supply appropriately corrected records. The analysis
function must not guess or secretly apply calibration.

**You are done when:** each summary includes its physical identity and unit, six
input series produce six outputs, and the result order is reproducible.

## W1 and W2 — Save data that your own readers can read

`save_json` is supplied. Use it to save reports and metadata. Implement
`save_csv` and `save_jsonl` in `storage.py` for processed measurement records.
These writers should not select, calibrate or analyse data.

For CSV, use `csv.DictWriter` with the `FIELDS` order from `records.py`. Write a
header even for an empty list. Open with UTF-8 encoding and `newline=""`. Create
the parent directory when necessary.

For JSON Lines, serialise each record on its own line. There is no outer array,
and no extra commas between objects. Use `allow_nan=False` to avoid emitting
non-standard JSON values. Empty input should create an empty file.

Both functions write a **snapshot**: rerunning with the same data should replace
the old snapshot, not double its number of rows. Continuous append-only storage
is a different requirement, reserved for the streaming stage.

Test a round trip: save calibrated records in `output/`, read them back, and
compare the reconstructed records with what you wrote. Re-run a writer with an
empty list to check that the old data does not remain.

**You are done when:** the round trips work, output directories can be created,
empty data is handled, and no raw file is overwritten. Keep calibration settings
and whether they were applied in an accompanying JSON summary; the CSV schema is
still deliberately small.

## L1 — Keep a useful operational log

`configure_logging` already configures console output. Extend its optional
`log_path` branch with a UTF-8 `logging.FileHandler`. Create the parent directory
and use append mode. Keep the existing console handler so that you still see what
the application is doing. Calling configuration twice should not duplicate every
message; retain the supplied `force=True` setup for this small entry point.

Put log messages in `run.py` around important actions: input file/format, number
of records read, selected series/count, calibration applied or deliberately
skipped, and output paths. Include enough context to understand a failed run.
Do not make a low-level function catch every exception and pretend it succeeded.

Distinguish a **log** from a **data product**. The log explains what happened;
your CSV or JSON contains the measurements and statistics. You should not have
to parse human-readable log messages to reconstruct sensor data.

Call logging configuration once during application startup. Do not configure
handlers when a module is imported. Do not add logging inside `calibrate_reading`
or `extended_summary`; their results should depend only on their arguments.

**You are done when:** two runs retain both sets of messages in the log, each
message appears once per destination, and an invalid logging level is rejected.

## I1 — Connect your completed pieces in run.py

Implement and check each function before you connect it. Then evolve `run.py`
into this still-finite sequence:

```text
configure logging
    → read the chosen finite input
    → explore all raw readings
    → select one room / sensor / metric
    → calibrate that series into new records
    → calculate its extended summary
    → write processed readings and summary metadata
```

Use the larger `readings.csv` when you want to exercise selection and exploration.
While you are still in this assignment, keep choices visibly near the top of
`run.py`. Do not introduce a configuration framework yet.

When you enable calibration, update the log wording and `calibration_applied`
metadata truthfully. Include the actual scale/offset in your summary. Do not
leave an unconditional "uncalibrated" warning after adding real calibration.
Use a fresh output filename instead of treating raw input as a writable cache.

There is no need for classes, inheritance, a dispatcher service, or a large
pipeline engine. A short sequence of ordinary function calls is the goal. The
application may have side effects; the individual numerical functions should not.

## How to check and show your progress

Start with the examples above and read their output. When you are comfortable,
run the optional check commands from the README. A task check reports `skipped`
while its function still raises `NotImplementedError`; this is not evidence that
you have completed the task. After implementation, a wrong result is a test
failure rather than a skip.

Record your decisions in `PROGRESS.md`: what works, which examples you tried,
what happens for an empty input, and what is still incomplete. Add at least one
small check of your own. An unusual case you can explain is more useful than a
large amount of unexamined output.

Before moving on, demonstrate that the three input formats produce the same raw
records; calibration preserves originals; summaries keep units/series separate;
your saved data can be read back; and failures are visible. Keep your folder
local for now. Packaging and Git work are later steps, not part of this assignment.

## Useful standard-library reading

Use these references when you need to check a function, rather than copying a
large framework into your project:

- CSV reader/writer: https://docs.python.org/3.13/library/csv.html
- JSON load/dump: https://docs.python.org/3.13/library/json.html
- Statistical functions: https://docs.python.org/3.13/library/statistics.html
- Logging tutorial: https://docs.python.org/3.13/howto/logging.html
