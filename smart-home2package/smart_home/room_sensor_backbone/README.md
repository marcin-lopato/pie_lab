# Your room-sensor project: start small

You are building a program that reads sensor measurements, helps you understand
what you have received, applies a calibration, calculates statistics, and saves
useful results. Later, you will use the same processing ideas on a stream of
measurements. **Today, you work with small, finite files.**

This folder is your starting point, not a finished application. You have one small
working example, clear interfaces, sample files, and tasks to complete. Functions
marked `YOUR TASK` deliberately raise `NotImplementedError` until you implement
them. The normal first run does not call those unfinished functions.

## 1. Run something before changing anything

**Annotation-fix edition:** this copy uses compatible `Optional` / `Union` type
hints in the logging and storage modules. See `COMPATIBILITY.md` if your interpreter
is older than the original classroom target. No exercise solutions were added.

Use Python 3.11 or newer. There are no third-party dependencies and no installation
step. Extract the folder, open a terminal inside it, and run:

```bash
python run.py
```

On a system where the command is named `python3`, use `python3 run.py`. On Windows,
`py -3 run.py` also works when the selected Python is 3.11 or newer. An editor's
Run button is fine too: choose `run.py`, not an individual helper module.

The program reads three temperatures: 20, 21, and 22 C. You should see:

```text
Uncalibrated summary: {'count': 3, 'mean': 21.0, 'minimum': 20.0, 'maximum': 22.0}
```

You will also see log messages and a new `output/baseline.json` file. **No
calibration is applied in this baseline.** Its warning and output metadata say so.
Repeated runs replace this small output snapshot; they do not change `data/`.
The log and print lines may interleave because they use different output streams.

## 2. Know what is already working

| Supplied working example | Work you will add |
|---|---|
| Read CSV and check the common record format | Read JSON and JSON Lines |
| Select a single room/sensor/metric | Explore and summarise all series separately |
| Apply a scalar calibration formula | Calibrate whole records without mutation |
| Calculate count, mean, minimum, maximum | Add median and sample standard deviation |
| Save a JSON snapshot | Save CSV and JSON Lines snapshots |
| Display console logs | Also keep an append-only file log |
| Use explicit choices in `run.py` | Load and validate a configuration file |

A sample configuration file is included for **Extension 1**. It is not read by the
baseline, and the configuration tasks are not yet implemented. Passing a config
argument to the starter is rejected rather than silently ignored. There is no hidden
completed solution and no automatic discovery mechanism.

## 3. Open only the files you need

```text
room_sensor_backbone/
    run.py                    Start here: the visible processing order
    records.py                Supplied common record parser
    readers.py                CSV example; JSON / JSON Lines tasks
    calibration.py            Scalar example; record-calibration task
    analysis.py               Selection / basic summary; exploration / stats tasks
    storage.py                JSON example; CSV / JSON Lines tasks
    logging_service.py        Console example; file-log task
    configuration.py          Extension 1: file configuration tasks
    processing.py             Extension 1: pure finite-pipeline task
    data/                     Tiny, larger, equivalent-format and broken inputs
    config/example.json       Extension 1 specimen, not a package manifest
    checks/                   Optional checks to use after trying the examples
    README.md                 This starting page
    DATA_CONTRACT.md           The record your modules agree to exchange
    STUDENT_GUIDE.md           Your first tasks, hints and acceptance examples
    EXTENSION_1.md             Configuration and functional processing
    NEXT_STEP.md              Preparation for generators; do not start here
    PROGRESS.md                Your short working notes
    VALIDATION.md              What was checked in the distributed starter
```

`output/` is created when you run the program. It is not supplied as input data.
You do not need to read the optional checks before understanding the first run.

## 4. Follow the progression

Read `DATA_CONTRACT.md`, then work through `STUDENT_GUIDE.md`. Complete and connect
one function at a time. After your finite pipeline works, move to `EXTENSION_1.md`.
Only then read `NEXT_STEP.md` to prepare for generator-based sources.

Here, a **service** means a function or small module with a clear job: read data,
load settings, or save results. It does not mean a web server or a background
process. There are no classes to subclass, decorators to register, web routes,
threads, asynchronous tasks, databases, or browser code to learn in this stage.

This is an ordinary folder of Python modules, not an installable distribution.
Do not create packaging metadata or initialise a Git repository yet. Your files
are already separated by responsibility, so both can be introduced later without
rewriting the scientific calculations.

## 5. Check your work when you are ready

The supplied working examples have a small optional check suite:

```bash
python -m unittest discover -s checks -p "test_*.py" -v
```

The task examples are separate:

```bash
python -m unittest discover -s checks -p "exercise_*.py" -v
```

At the beginning, task checks report `skipped` and the corresponding task ID. This
means **not implemented**, not passed. As you complete a task, its checks become
active. Passing these examples is a starting point; also try your own edge cases.
