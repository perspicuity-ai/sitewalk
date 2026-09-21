# Sub-decision records

One file per consequential choice, named `YYYY-MM-DD-<slug>.md`.

The rules, the admission test and the skeleton to copy are in
[../RECORDS.md](../RECORDS.md). The parent of every record here is
[../../RECORD.md](../../RECORD.md), which also holds the decision index.

Check the mechanical parts with:

```sh
make records
```

This directory starts empty. It is not waiting for a particular first record: file one when a
choice meets the admission test in [../RECORDS.md](../RECORDS.md#when-a-record-is-required).
An earlier revision of this template asked for a process-conventions record as the first entry;
the installed skill does not require one, so that instruction was removed rather than inherited.
