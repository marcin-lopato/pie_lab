# Extension 1 — Configure a run and keep processing functional

Start this extension after your finite readers, calibration, summaries, writers
and logging work. You now have a genuine maintenance problem: you have to edit
Python source whenever you change the input file or selected measurement.

Your next goal is to describe **which run you want** in a configuration file,
without rewriting **how a reading is processed**. You will use an ordinary JSON
file and a few functions. You do not need a configuration class hierarchy,
metaprogramming, environment-variable overlays, or plugin discovery.

## Understand the supplied specimen

Open `config/example.json`. It specifies input format/path, one selected series,
whether its calibration is enabled, scale/offset, two output paths and logging.
The file is an example of the target interface. The initial `run.py` does not read
it, and your configuration functions are still tasks.

JSON was chosen so that you can reuse your new file-reading experience. This is
an application settings file, **not packaging metadata**. JSON has no comments,
uses lowercase `true`/`false`/`null`, and does not allow a trailing comma. Keep
explanations here rather than adding invalid comment syntax to the file.

The example chooses laboratory / station-01 / temperature. Its scale and offset
belong to that selection only. Changing the selected physical quantity also
requires choosing appropriate calibration coefficients, or disabling calibration.
One pair of coefficients is not a universal calibration for every station/metric.

## X1 — Validate before you do any output work

Implement `validate_config(config)` in `configuration.py`. Require a dictionary
at the top level and dictionaries for each section. The required sections and
leaf keys are exactly those listed below; reject both missing and unknown keys.
A misspelled option should fail, not silently leave a setting unchanged.

| Setting | Rule |
|---|---|
| `input.path` | Non-empty string. |
| `input.format` | Exactly `csv`, `json`, or `jsonl`. |
| `selection.room`, `selection.sensor_id` | Non-empty strings. |
| `selection.metric` | Exactly `temperature`, `humidity`, or `pressure`. |
| `calibration.enabled` | A real boolean, not the string `"false"` or integer 0. |
| `calibration.scale`, `calibration.offset` | Finite int/float values, not booleans or numeric strings. |
| `output.readings_path`, `output.summary_path` | Non-empty strings. |
| `logging.level` | One of `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`. |
| `logging.path` | Non-empty string or `null` for console-only logging. |

Treat whitespace-only text as empty. For accepted non-empty strings, preserve
what the user wrote; do not silently strip a path or change letter case. Exact
choice fields must match their permitted spelling. Scale/offset remain required
and validated even when calibration is disabled, keeping the schema predictable.

The function returns `None` on success and raises `ValueError` on failure. Include
the relevant field name in the error. It must not read files, change the supplied
dictionary, create directories, or configure logging. Whether an input file
actually exists is checked when it is opened, not by this pure validator.

Try a valid config, an unsupported format, a missing key, `"false"` instead of
`false`, and a non-finite coefficient. These are configuration failures, not empty
sensor datasets. Do not silently fall back to the CSV demonstration when the user
has asked for something invalid.

## X2 — Resolve file paths predictably

Implement `resolve_paths(config, base_dir)`. Paths inside the configuration are
relative to the **configuration file's directory**, not the terminal's current
working directory and not necessarily the project root.

For example, `config/example.json` contains `../data/readings.csv`. Starting from
`config/`, go up one directory and then into `data/`. The resolved path should be
the same whether you launch the project from its own directory or elsewhere.
Absolute paths remain absolute.

Return a new settings dictionary with `Path` objects for `input.path`, both output
paths and any non-null log path. Use resolved absolute paths so spelling such as
`output/../data/readings.csv` cannot bypass a collision check. Keep a null log
path as `None`. Do not change the original nested dictionary. A top-level shallow
copy alone would still share its nested sections; make the necessary copies.

Reject any collision between input, processed-data output, summary output and
log destinations. The supplied `load_config` additionally prevents an output or
log from overwriting the configuration file itself. These are teaching safeguards,
not a complete filesystem security model: hard-link aliases and races are outside
this small exercise. Do not create files or directories while resolving paths.

The assembly in `load_config(path)` is supplied: read JSON once, validate, resolve,
then return the prepared settings. Your readers and calibration functions must
not each open the config file again.

## X3 — Make the calculation a pure function

Implement `process_readings(readings, selection, calibration)` in `processing.py`.
Reuse the functions you have already written. Select one series, optionally
calibrate its records, extract values and calculate `extended_summary`.

Return this structure:

```text
{
    "readings": [the finite processed records],
    "summary": {the extended statistics},
    "calibration_applied": true or false
}
```

The sketch uses JSON-style booleans; your Python return value uses `True`/`False`.
The function must not open files, print, log, read globals or modify its inputs.
It receives already chosen settings as arguments. Turning calibration off should
leave values uncorrected, not apply scale/offset anyway. An empty selection
returns an empty record list and the defined empty statistics.

This is the practical functional-programming idea: express the calculation as
small transformations of values and return new results. A list comprehension is
a good tool. A clear `for` loop with local variables can be equally appropriate.
You do not need nested lambdas or a general-purpose `compose` function to make
the design functional.

Accept an `Iterable` and consume the source only once. Your first operation can
materialise the selected series, after which you can reuse that finite list for
both output and statistics. This is still a finite-data algorithm: selecting all
records from a never-ending source would never finish.

For the larger supplied file and example calibration, expect six selected
records, mean approximately 21.02 C, and `calibration_applied` equal to `True`.
With calibration disabled, expect mean 21.0 C. Check both calls on the same raw
list and confirm that the list has not changed.

## X4 — Let run.py manage the effects

Refactor `run.py` so that it now performs this sequence:

```text
load and validate configuration once
    → configure logging
    → read the finite input
    → call process_readings with explicit settings
    → save processed readings as CSV
    → save summary and calibration/series metadata as JSON
    → log what was saved
```

Keep exploration available as a separate report of the raw data. Do not hide
input/output operations inside `process_readings`. A common mistake is to pass
only a filename into it and have it perform the entire run; that removes the
separation you are trying to achieve.

First call `load_config(ROOT / "config" / "example.json")` in your main function.
Only after that works, add an optional positional configuration path with
`argparse`. Your target commands are:

```bash
python run.py
python run.py config/example.json
```

These two commands are the **target after X4**, not two different modes already
implemented in the distributed baseline. The initial starter supports the first
command only. A relative config argument is relative to the terminal's working
directory; paths *inside* that file are relative to the file's directory.

Do not dump the whole prepared settings dictionary directly to JSON: it now
contains `Path` objects. Select the metadata you need and convert any recorded
path to text. At minimum, preserve the selected identity, physical unit, whether
calibration was applied, the scale/offset and the summary. The saved CSV contains
the corresponding processed readings.

Run first with a small input. Change only `input.format` and `input.path` to use
the matching JSON and JSON Lines files: the calculations should stay the same.
Change the selected series, keeping calibration appropriate. Try a missing
selection: it should remain a valid empty result, not switch to another sensor.

## What you should be able to explain

You should be able to point to the one place where settings are loaded, the one
place where logging is configured, and the boundary between external actions and
pure calculations. You should be able to test a calculation without a config file
and load a config file without reading any sensor data.

Once this works, you have a useful foundation for generators. You have not yet
built an infinite service, background collector, database, package distribution
or browser. Those can be separate later iterations, each solving a new need.

For reference: Python's functional-programming discussion is at
https://docs.python.org/3.13/howto/functional.html and path handling is documented
at https://docs.python.org/3.13/library/pathlib.html.
