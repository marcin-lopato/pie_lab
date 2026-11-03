# What was checked in your starter

This folder is intentionally unfinished: you are expected to implement the task
functions. Do not interpret a green baseline check as completion of your tasks.

## Reproducible checks

The supplied working path was checked with Python 3.13.5 on Linux.

- `python run.py` reads three records and reports count 3, mean 21, minimum 20,
  maximum 22. Its saved metadata explicitly says calibration was not applied.
- The 12 optional baseline checks pass.
- The 20 optional task checks report skipped in the distributed starter because
  their task functions raise `NotImplementedError`. No task implementation is
  silently substituted to make these checks pass.
- The CSV, JSON and JSON Lines reference fixtures contain equivalent records
  after the supplied common parsing step. Your JSON/JSON Lines readers are still
  tasks; this fixture comparison is not a claim that they are implemented.
- Importing the modules does not start processing, create output files or emit logs.
- Running the entry-point script from another working directory still finds its
  input beside the script. Passing a configuration argument is explicitly
  rejected until you complete X4.
- A clean extracted copy runs without installation, including from a directory
  with spaces in its name. Generated output and bytecode are not included in the
  distribution. No packaging metadata, Git files or completed task solutions are
  included.

You can repeat the two check commands in README.md. The acceptance checks are
small examples, not an exhaustive test suite. Add your own cases when you change
behaviour.

## Scope

The intended minimum is Python 3.11. Source syntax was checked against that
version's grammar; runtime execution here used 3.13.5, not every supported Python
version. Windows and macOS were not directly executed.

This stage has no continuous acquisition, hardware integration, database,
background service, HTTP API, browser or installed package. Its file snapshots
are not transactional storage. Its supplied parser validates structure and
basic values, not physical plausibility or statistical outliers. Those limits
are deliberate so that you can understand and extend one requirement at a time.
