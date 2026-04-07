import unittest
from pathlib import Path

from vibe_sanitizer.formatters import format_scan_report
from vibe_sanitizer.models import Finding, ScanReport


class FormatterTests(unittest.TestCase):
    def test_text_formatter_uses_color_when_enabled(self) -> None:
        report = ScanReport(
            root=Path("/repo"),
            scope="working-tree",
            files_scanned=1,
            files_skipped=0,
            findings=[
                Finding(
                    path="app.py",
                    line=1,
                    column=1,
                    detector_id="openai_key",
                    title="OpenAI-style API key",
                    category="secret",
                    severity="high",
                    message="test message",
                    preview="sk-***3456",
                    replacement_text="<REDACTED_OPENAI_KEY>",
                    editable_in_place=True,
                    review_required=False,
                    start_offset=0,
                    end_offset=10,
                )
            ],
        )
        rendered = format_scan_report(report, "text", color_mode="always", is_tty=False)
        self.assertIn("\033[", rendered)
        self.assertIn("openai_key", rendered)

    def test_text_formatter_skips_color_when_disabled(self) -> None:
        report = ScanReport(
            root=Path("/repo"),
            scope="working-tree",
            files_scanned=0,
            files_skipped=0,
            findings=[],
        )
        rendered = format_scan_report(report, "text", color_mode="never", is_tty=False)
        self.assertNotIn("\033[", rendered)
        self.assertIn("Status:", rendered)


if __name__ == "__main__":
    unittest.main()
