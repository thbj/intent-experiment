#!/usr/bin/env python3
"""cost_report — sum the work log per task.

Pairs start/stop rows in order per task and prints minutes spent.
Unclosed starts are reported, not guessed.
"""

import csv
import datetime
import pathlib
import sys

LOG = pathlib.Path(__file__).resolve().parent.parent / "worklog.csv"


def main():
    if not LOG.exists():
        print("no worklog.csv yet", file=sys.stderr)
        return 2
    open_starts, totals, unclosed = {}, {}, []
    with open(LOG, newline="", encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            ts = datetime.datetime.fromisoformat(row["ts"])
            task = row["task"]
            if row["action"] == "start":
                if task in open_starts:
                    unclosed.append((task, open_starts.pop(task)))
                open_starts[task] = ts
            elif row["action"] == "stop" and task in open_starts:
                totals[task] = totals.get(task, 0.0) + (ts - open_starts.pop(task)).total_seconds() / 60
    unclosed.extend(open_starts.items())

    print("task,minutes")
    for task in sorted(totals):
        print(f"{task},{totals[task]:.1f}")
    if unclosed:
        print(f"\nWARNING: {len(unclosed)} unclosed start(s): "
              + ", ".join(t for t, _ in unclosed), file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
