import json
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from validate_relationships import ValidationError, validate_dataset  # noqa: E402


SOURCE_DATA = ROOT / "examples" / "synthetic"


class ControlPlaneValidationTests(unittest.TestCase):
    def copy_dataset(self, target: Path) -> None:
        for source in SOURCE_DATA.glob("*.json"):
            target.joinpath(source.name).write_text(
                source.read_text(encoding="utf-8"), encoding="utf-8"
            )

    def test_expected_case_states(self) -> None:
        states = validate_dataset()
        self.assertEqual(states["INC-001"], "ATTENTION_REQUIRED")
        self.assertEqual(states["INC-002"], "CLOSED")

    def test_missing_reference_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            data_dir = Path(directory)
            self.copy_dataset(data_dir)
            incidents_path = data_dir / "incidents.json"
            incidents = json.loads(incidents_path.read_text(encoding="utf-8"))
            incidents[0]["operational_ticket_ids"].append("OPS-MISSING")
            incidents_path.write_text(json.dumps(incidents), encoding="utf-8")

            with self.assertRaises(ValidationError):
                validate_dataset(data_dir)

    def test_unverified_required_evidence_prevents_closure(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            data_dir = Path(directory)
            self.copy_dataset(data_dir)
            evidence_path = data_dir / "evidence.json"
            evidence = json.loads(evidence_path.read_text(encoding="utf-8"))
            for item in evidence:
                if item["id"] == "EVD-003":
                    item["status"] = "submitted"
            evidence_path.write_text(json.dumps(evidence), encoding="utf-8")

            states = validate_dataset(data_dir)
            self.assertEqual(states["INC-002"], "ATTENTION_REQUIRED")


if __name__ == "__main__":
    unittest.main()
