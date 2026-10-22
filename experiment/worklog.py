#!/usr/bin/env python3
"""worklog — start/stop logging for the cost ledger.

  worklog.py start <task-id> [note]
  worklog.py stop  <task-id> [note]

Appends to worklog.csv: timestamp, action, task, note.
"""

import csv
import datetime
import pathlib
import sys

LOG = pathlib.Path(__file__).resolve().parent.parent / "worklog.csv"


def main(argv):
    if len(argv) < 3 or argv[1] not in ("start", "stop"):
        print(__doc__, file=sys.stderr)
        return 2
    new = not LOG.exists()
    with open(LOG, "a", newline="", encoding="utf-8") as fh:
        writer = csv.writer(fh)
        if new:
            writer.writerow(["ts", "action", "task", "note"])
        writer.writerow([
            datetime.datetime.now().isoformat(timespec="seconds"),
            argv[1],
            argv[2],
            " ".join(argv[3:]),
        ])
    print(f"{argv[1]} {argv[2]} logged")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
