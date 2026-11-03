# A small fix for older Python interpreters

An import can fail before your program starts if your interpreter tries to evaluate
`Path | None` or `dict | list`. That union-type spelling requires Python 3.10 or newer.
Check the interpreter actually used to run your file with:

```bash
python --version
python -c "import sys; print(sys.executable)"
```

This copy changes only two Python modules:

- `logging_service.py` imports `Optional` from `typing` and uses `Optional[Path]`.
- `storage.py` imports `Union` from `typing` and uses `Union[dict, list]`.

Those annotations describe the same allowed argument types as before. The function
bodies, supplied datasets, and student exercises are unchanged. In particular, this
patch does not implement any unfinished task.

When you have already edited these modules, apply the import and annotation changes
by hand. Do not replace your work with the original task stubs in this archive.

## Version scope

The original classroom target is Python 3.11 or newer. This patch removes the two
Python-3.10-specific union expressions. Other annotations such as `list[dict]` and
`Iterable[dict]` still require Python 3.9 or newer without further changes.
This is a targeted annotation fix, not a promise that all Python 3.11 behaviour
has been backported. For example, ISO timestamp forms accepted by
`datetime.fromisoformat` differ across versions. The supplied fixtures use explicit
numeric UTC offsets such as `+00:00`.

## Checks actually run for this patch

- Python 3.13.5 on Linux: `python run.py` completed with the expected mean of 21.0.
- All 12 baseline checks passed.
- All 20 exercise checks were skipped because their student tasks remain unfinished.
- The entry point also ran from a different working directory.
- Both replacement annotations resolved with `typing.get_type_hints`.
- All Python source files parsed using Python 3.9's grammar setting. This is only
  a syntax check, not a run under Python 3.9.

A Python 3.9 runtime was not available in this environment, and an attempted runtime
download failed due to network restrictions. No Python 3.9 execution is claimed.

References:
- Python 3.10 typing documentation (Union and Optional):
  https://docs.python.org/3.10/library/typing.html
- Python 3.9 generic-type syntax:
  https://docs.python.org/3.9/whatsnew/3.9.html#type-hinting-generics-in-standard-collections
