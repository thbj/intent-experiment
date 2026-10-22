#!/usr/bin/env python3
"""seal — SHA-256 hash-commit of ground-truth files, and verification.

  seal.py seal <files...>   writes seals.json with one hash per file
  seal.py verify            recomputes and compares; non-zero on mismatch
"""

import hashlib
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
SEALS = ROOT / "seals.json"


def digest(path):
    return hashlib.sha256(pathlib.Path(path).read_bytes()).hexdigest()


def main(argv):
    if len(argv) >= 2 and argv[1] == "seal" and len(argv) > 2:
        seals = {str(pathlib.Path(p).resolve().relative_to(ROOT)): digest(p) for p in argv[2:]}
        SEALS.write_text(json.dumps(seals, indent=2, sort_keys=True), encoding="utf-8")
        print(f"sealed {len(seals)} files -> {SEALS.name}")
        return 0
    if len(argv) == 2 and argv[1] == "verify":
        seals = json.loads(SEALS.read_text(encoding="utf-8"))
        bad = [p for p, h in seals.items() if not (ROOT / p).exists() or digest(ROOT / p) != h]
        for p in bad:
            print(f"MISMATCH: {p}", file=sys.stderr)
        print("all seals intact" if not bad else f"{len(bad)} seal(s) broken")
        return 1 if bad else 0
    print(__doc__, file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))
