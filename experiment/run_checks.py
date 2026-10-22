#!/usr/bin/env python3
"""run_checks — execute every registered check and write the run manifest.

The manifest (ci-run-manifest.json) is what ci_intent_check.py uses for
its executed-check cross-check: an intent whose check never ran is a
meta-drift failure, not a pass. Exit non-zero if any check fails.
"""

import json
import pathlib
import subprocess
import sys

import yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent


def main():
    doc = yaml.safe_load((ROOT / "checks.yaml").read_text(encoding="utf-8")) or {}
    executed, failed = [], []
    for check in doc.get("checks", []):
        result = subprocess.run(check["run"], shell=True, cwd=ROOT, capture_output=True, text=True)
        executed.append(check["id"])
        status = "ok"
        if result.returncode != 0:
            failed.append(check["id"])
            status = "FAIL"
        print(f"  {check['id']}: {status}")
        if result.returncode != 0 and result.stdout.strip():
            print("    " + result.stdout.strip().replace("\n", "\n    "))

    manifest = {"executed": executed, "failed": failed}
    (ROOT / "ci-run-manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(f"manifest written: {len(executed)} executed, {len(failed)} failed")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
