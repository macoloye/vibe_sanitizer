import unittest
from pathlib import Path

from vibe_sanitizer.config import default_config
from vibe_sanitizer.scanner import ScanEngine


class ScannerTests(unittest.TestCase):
    def setUp(self) -> None:
        self.engine = ScanEngine(Path.cwd(), default_config())

    def test_detects_specific_secrets_and_paths(self) -> None:
        text = """
api_key = "sk-abcdefghijklmnopqrstuvwxyz123456"
token = "ghp_abcdefghijklmnopqrstuvwxyz123456"
path = "/Users/alice/Documents/project/secrets.txt"
"""
        findings = self.engine.scan_text("example.py", text)
        detector_ids = {finding.detector_id for finding in findings}
        self.assertIn("openai_key", detector_ids)
        self.assertIn("github_token", detector_ids)
        self.assertIn("home_path", detector_ids)

    def test_prefers_specific_detector_over_generic_secret_assignment(self) -> None:
        text = 'api_key = "sk-abcdefghijklmnopqrstuvwxyz123456"\n'
        findings = self.engine.scan_text("config.py", text)
        detector_ids = {finding.detector_id for finding in findings}
        self.assertIn("openai_key", detector_ids)
        self.assertNotIn("secret_assignment", detector_ids)


if __name__ == "__main__":
    unittest.main()
