# Next step — Prepare for generators without starting an infinite service yet

Read this after your finite pipeline and configuration extension work. You do
not need to implement a sensor simulator for the current assignment. Your task
now is to recognise which design choices will remain useful when the data no
longer arrives as a complete list.

## A record-at-a-time calculation is already useful

Your `calibrate_reading` transforms one record. It does not care whether that
record came from a CSV file, a list, or a sensor. Keep it that way. In contrast,
a function that opens an input file, transforms all rows and writes another file
at once cannot be reused as easily in a streaming pipeline.

You can make a finite experiment without adding any source code files:

```python
from calibration import calibrate_value

values = [20.0, 21.0, 22.0]
corrected = (calibrate_value(value, 1.02, -0.4) for value in values)
print(next(corrected))   # One corrected value is requested now.
print(list(corrected))   # Consume only the remaining two values.
print(list(corrected))   # The iterator has been exhausted: [].
```

A generator expression does not eagerly build a complete result list. An iterator
is consumed as you request values; it is not automatically rewindable. Observe
that behaviour before connecting anything to a stream.

## Your future progression

First, write a finite `iter_csv` or `iter_jsonl` version that yields one standard
record at a time. Use `with` around the open file. Remember that a paused generator
can still own an open file: exhausting it or explicitly closing it releases that
resource. Do not make resource lifetime depend on an indefinite future cleanup.

Second, write a finite simulated source, with a fixed random seed and a fixed
number of timestamps. Keep it separate from calibration and statistics. Check
that the same seed and fixed starting timestamp reproduce the same sequence.
Only then consider a deliberately unbounded version.

Third, decide where acquisition pacing belongs. A wall-clock wait is an effect,
not a calibration operation. In an early generator demonstration you can produce
synthetic timestamps without sleeping; that makes examples and checks fast.
Actual pacing is a later requirement.

Finally, introduce an unbounded source only with a bounded consumer. The first
experiment should request a known number of readings with `itertools.islice` and
then stop. Do not run `list(unbounded_source)` to see what it contains.

## Not every finite calculation becomes a streaming calculation

Your current readers, selection function and pipeline return complete lists.
Your whole-file exploration and statistics require a finite input. Annotating a
parameter as `Iterable` does not remove these requirements.

To monitor a never-ending stream later, you will need a policy such as a finite
window per `(room, sensor_id, metric)`, or incremental state for selected
statistics. A global window over interleaved records can mix quantities or
unfairly represent a slow sensor. A window of ten samples is not necessarily a
window of ten seconds.

There is a second boundary to notice: your current writers replace finite
snapshots. Replacing a file once per reading would lose history; appending every
reading forever would grow disk use forever. You will have to choose batching,
flushing and retention deliberately. Do not silently change the snapshot
contract in this assignment.

Also avoid trying to iterate through the same one-use source independently for
logging, storage and statistics: the first consumer can exhaust it. Unlimited
iterator splitting can introduce hidden buffers. Later, choose an explicit
single-pass processing order or bounded hand-off rather than assuming every
consumer sees an independent copy.

## Before leaving the finite-data stage

Be ready to explain what consumes the source, what keeps records in memory,
which functions are pure, what happens when there are no records, and how a
consumer will stop. Those answers matter more than having a `while True` loop.
The simulator, rolling windows and continuous storage will be the next concrete
assignment, not hidden unfinished features of this folder.

References: https://docs.python.org/3.13/howto/functional.html and
https://docs.python.org/3.13/library/itertools.html.
