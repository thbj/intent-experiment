"""Golden tests for the harness itself (the OQ7 discipline: the lab's
own machinery gets the same scrutiny it imposes).

Each test copies the repo to a temp dir, applies one mutation, and
asserts the harness reacts exactly as specified.
"""

import pathlib
import shutil
import subprocess
import sys
import tempfile
import unittest

REPO = pathlib.Path(__file__).resolve().parent.parent.parent


def run(script, cwd):
    return subprocess.run(
        [sys.executable, str(pathlib.Path(cwd) / "experiment" / script)],
        cwd=cwd, capture_output=True, text=True,
    )


class HarnessTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="intent-exp-")
        self.root = pathlib.Path(self.tmp) / "repo"
        shutil.copytree(REPO, self.root, ignore=shutil.ignore_patterns(".git", "__pycache__"))

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def checks_then_intent(self):
        run_result = run("run_checks.py", self.root)
        intent_result = run("ci_intent_check.py", self.root)
        return run_result, intent_result

    def test_baseline_passes_with_excepted_carveout(self):
        run_result, intent_result = self.checks_then_intent()
        self.assertEqual(run_result.returncode, 0, run_result.stdout + run_result.stderr)
        self.assertEqual(intent_result.returncode, 0, intent_result.stdout + intent_result.stderr)
        self.assertIn("EXCEPTED", intent_result.stdout)
        self.assertNotIn("INT-001: PASS", intent_result.stdout)

    def test_dangling_reference_fails(self):
        (self.root / "checks.yaml").write_text("checks: []\n", encoding="utf-8")
        _, intent_result = self.checks_then_intent()
        self.assertEqual(intent_result.returncode, 1)
        self.assertIn("dangling", intent_result.stderr)

    def test_vacuous_check_fails(self):
        shutil.rmtree(self.root / "sample" / "red_proofs" / "INT-001")
        _, intent_result = self.checks_then_intent()
        self.assertEqual(intent_result.returncode, 1)
        self.assertIn("VACUOUS", intent_result.stderr)

    def test_expired_ledger_entry_fails(self):
        ledger = self.root / "deviations.yaml"
        ledger.write_text(ledger.read_text(encoding="utf-8").replace("2027-01-31", "2020-01-01"),
                          encoding="utf-8")
        _, intent_result = self.checks_then_intent()
        self.assertEqual(intent_result.returncode, 1)
        self.assertIn("expired", intent_result.stderr)

    def test_real_violation_goes_red(self):
        bad = self.root / "sample" / "src" / "Billing" / "Sneaky.cs"
        bad.write_text("class S { void F() { var h = new HttpClient(); } }\n", encoding="utf-8")
        run_result, intent_result = self.checks_then_intent()
        self.assertEqual(run_result.returncode, 1)
        self.assertIn("FAIL (check red)", intent_result.stdout)

    def test_seal_verify_detects_tamper(self):
        subprocess.run(
            [sys.executable, "experiment/seal.py", "seal", "intents/INT-001.yaml", "checks.yaml"],
            cwd=self.root, capture_output=True, text=True, check=True,
        )
        intent = self.root / "intents" / "INT-001.yaml"
        intent.write_text(intent.read_text(encoding="utf-8").replace("MUST", "ASSUME"),
                          encoding="utf-8")
        verify = subprocess.run(
            [sys.executable, "experiment/seal.py", "verify"],
            cwd=self.root, capture_output=True, text=True,
        )
        self.assertEqual(verify.returncode, 1)
        self.assertIn("MISMATCH", verify.stderr)


if __name__ == "__main__":
    unittest.main()
