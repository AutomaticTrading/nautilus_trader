"""Offline, non-publishing source-level guard for organizational workflow safety."""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[2]

class WorkflowGuardTests(unittest.TestCase):
    def test_upstream_only_guard_on_both_nightly_jobs(self):
        flow=(ROOT / ".github/workflows/nightly-merge.yml").read_text()
        self.assertEqual(flow.count("github.repository == 'nautechsystems/nautilus_trader'"),2)
        self.assertIn("  workflow_dispatch:",flow)
        self.assertIn("schedule:",flow)
        script=(ROOT / "scripts/ci/plan-nightly-merge.bash").read_text()
        self.assertIn("repos/nautechsystems/nautilus_trader/",script)

if __name__ == "__main__":
    unittest.main()
