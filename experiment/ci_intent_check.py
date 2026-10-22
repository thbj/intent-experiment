#!/usr/bin/env python3
"""ci_intent_check — the ARM C machinery.

Validates the intent layer and fails CI when its guarantees do not
hold. Exit 0 = PASS (possibly with EXCEPTED scopes), 1 = FAIL,
2 = configuration error.

Performed, in order (see IMPLEMENTATION-PLAN.md in the research
workspace):
  1. intent-record schema validation
  2. dangling enforced_by references
  3. executed-check cross-check against the run manifest
  4. vacuity re-proof (each check must still fail on its known violation)
  5. deviation-ledger validation (schema, expiry, carve-out subset)
  6. conformance report (EXCEPTED for carved-out scopes, never PASS)
"""

import datetime
import fnmatch
import json
import pathlib
import subprocess
import sys

import yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent
INTENT_FIELDS = {"id", "statement", "modality", "scope", "rationale", "owner", "enforced_by"}
MODALITIES = {"MUST", "ASSUME"}
LEDGER_FIELDS = {"id", "intent", "carve_out", "reason", "owner", "expires"}


def load_yaml(path):
    with open(path, encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def validate_intent(path, record, errors):
    if not isinstance(record, dict):
        errors.append(f"{path}: not a mapping")
        return
    missing = INTENT_FIELDS - record.keys()
    extra = record.keys() - INTENT_FIELDS
    if missing:
        errors.append(f"{path}: missing fields {sorted(missing)}")
    if extra:
        errors.append(f"{path}: unknown fields {sorted(extra)}")
    if missing or extra:
        return
    if record["modality"] not in MODALITIES:
        errors.append(f"{path}: modality must be one of {sorted(MODALITIES)}")
    if len(str(record["statement"]).split()) > 50:
        errors.append(f"{path}: statement exceeds 50 words")
    if not isinstance(record["scope"], list) or not record["scope"]:
        errors.append(f"{path}: scope must be a non-empty list of globs")
    if not isinstance(record["enforced_by"], list) or not record["enforced_by"]:
        errors.append(f"{path}: enforced_by must be a non-empty list of check ids")


def validate_ledger(entries, intents_by_id, today, errors):
    """Returns {intent_id: [active carve-out globs]}."""
    carve_outs = {}
    for i, entry in enumerate(entries):
        where = f"deviations.yaml entry {i}"
        if not isinstance(entry, dict) or LEDGER_FIELDS - entry.keys():
            errors.append(f"{where}: must carry fields {sorted(LEDGER_FIELDS)}")
            continue
        try:
            expires = datetime.date.fromisoformat(str(entry["expires"]))
        except ValueError:
            errors.append(f"{where}: expires is not an ISO date")
            continue
        if expires < today:
            errors.append(f"{where} ({entry['id']}): expired {expires} — renew or remove")
            continue
        intent = intents_by_id.get(entry["intent"])
        if intent is None:
            errors.append(f"{where} ({entry['id']}): unknown intent {entry['intent']}")
            continue
        globs = entry["carve_out"]
        if not isinstance(globs, list) or not globs:
            errors.append(f"{where} ({entry['id']}): carve_out must be a non-empty list")
            continue
        # Subset check (pilot approximation): every carve-out glob must
        # fall under at least one scope glob of its intent.
        for g in globs:
            probe = g.replace("**", "x/x").replace("*", "x")
            if not any(fnmatch.fnmatch(probe, s.replace("**", "*")) for s in intent["scope"]):
                errors.append(
                    f"{where} ({entry['id']}): carve-out {g!r} is outside intent scope {intent['scope']}"
                )
        carve_outs.setdefault(entry["intent"], []).extend(globs)
    return carve_outs


def run_red_proof(check, errors):
    cmd = check.get("red_proof")
    if not cmd:
        errors.append(f"check {check['id']}: no red_proof registered")
        return
    result = subprocess.run(cmd, shell=True, cwd=ROOT, capture_output=True, text=True)
    if result.returncode == 0:
        errors.append(
            f"check {check['id']}: VACUOUS — passes its red-proof fixture "
            f"(the known violation no longer trips it)"
        )


def main():
    errors = []
    today = datetime.date.today()

    intent_files = sorted((ROOT / "intents").glob("*.yaml"))
    if not intent_files:
        print("ci_intent_check: no intent records found under intents/", file=sys.stderr)
        return 2
    intents_by_id = {}
    for path in intent_files:
        record = load_yaml(path)
        validate_intent(path.relative_to(ROOT), record, errors)
        if isinstance(record, dict) and "id" in record:
            intents_by_id[record["id"]] = record

    checks_doc = load_yaml(ROOT / "checks.yaml") or {}
    checks = {c["id"]: c for c in checks_doc.get("checks", [])}

    manifest_path = ROOT / "ci-run-manifest.json"
    if not manifest_path.exists():
        print("ci_intent_check: ci-run-manifest.json missing — run run_checks.py first", file=sys.stderr)
        return 2
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    executed = set(manifest.get("executed", []))

    # 2. dangling refs + 3. executed-check cross-check
    for intent in intents_by_id.values():
        for check_id in intent.get("enforced_by", []):
            if check_id not in checks:
                errors.append(f"intent {intent['id']}: dangling enforced_by reference {check_id!r}")
            elif check_id not in executed:
                errors.append(
                    f"intent {intent['id']}: check {check_id} did not execute in this CI run"
                )

    # 4. vacuity re-proofs (only for checks that are actually referenced)
    referenced = {cid for i in intents_by_id.values() for cid in i.get("enforced_by", []) if cid in checks}
    for check_id in sorted(referenced):
        run_red_proof(checks[check_id], errors)

    # 5. ledger
    ledger_doc = load_yaml(ROOT / "deviations.yaml") or {}
    carve_outs = validate_ledger(ledger_doc.get("deviations", []), intents_by_id, today, errors)

    # 6. conformance report
    failed_checks = set(manifest.get("failed", []))
    print("== intent conformance ==")
    for intent in intents_by_id.values():
        if any(c in failed_checks for c in intent["enforced_by"]):
            status = "FAIL (check red)"
        elif intent["id"] in carve_outs:
            status = f"EXCEPTED (active carve-out: {', '.join(carve_outs[intent['id']])})"
        else:
            status = "PASS"
        print(f"  {intent['id']}: {status}")

    if errors:
        print("\n== intent layer FAIL ==", file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
        return 1
    print("\nintent layer OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
