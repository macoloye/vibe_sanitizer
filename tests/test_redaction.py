import unittest

from vibe_sanitizer.models import Finding
from vibe_sanitizer.redaction import apply_replacements


class RedactionTests(unittest.TestCase):
    def test_in_place_applies_only_fixable_findings(self) -> None:
        text = 'api_key = "sk-abcdefghijklmnopqrstuvwxyz123456"\npassword = "supersecret"\n'
        findings = [
            Finding(
                path="config.py",
                line=1,
                column=12,
                detector_id="openai_key",
                title="OpenAI-style API key",
                category="secret",
                severity="high",
                message="",
                preview="sk-***3456",
                replacement_text="<REDACTED_OPENAI_KEY>",
                editable_in_place=True,
                review_required=False,
                start_offset=11,
                end_offset=47,
            ),
            Finding(
                path="config.py",
                line=2,
                column=13,
                detector_id="secret_assignment",
                title="Secret-like assignment",
                category="secret",
                severity="medium",
                message="",
                preview="su***et",
                replacement_text="<REDACTED_SECRET>",
                editable_in_place=False,
                review_required=True,
                start_offset=61,
                end_offset=72,
            ),
        ]

        sanitized = apply_replacements(text, findings, in_place_only=True)
        self.assertIn("<REDACTED_OPENAI_KEY>", sanitized)
        self.assertIn('password = "supersecret"', sanitized)

    def test_export_applies_all_replacements(self) -> None:
        text = 'password = "supersecret"\n'
        findings = [
            Finding(
                path="config.py",
                line=1,
                column=12,
                detector_id="secret_assignment",
                title="Secret-like assignment",
                category="secret",
                severity="medium",
                message="",
                preview="su***et",
                replacement_text="<REDACTED_SECRET>",
                editable_in_place=False,
                review_required=True,
                start_offset=12,
                end_offset=23,
            )
        ]

        sanitized = apply_replacements(text, findings, in_place_only=False)
        self.assertEqual(sanitized, 'password = "<REDACTED_SECRET>"\n')


if __name__ == "__main__":
    unittest.main()
