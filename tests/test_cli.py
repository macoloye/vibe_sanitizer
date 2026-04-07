import unittest

from vibe_sanitizer.cli import build_parser


class CliParserTests(unittest.TestCase):
    def test_scan_parser_accepts_scope(self) -> None:
        parser = build_parser()
        args = parser.parse_args(["scan", "--scope", "tracked"])
        self.assertEqual(args.command, "scan")
        self.assertEqual(args.scope, "tracked")

    def test_export_parser_requires_output(self) -> None:
        parser = build_parser()
        args = parser.parse_args(["export", "--output", "../safe-share"])
        self.assertEqual(args.command, "export")
        self.assertEqual(args.output, "../safe-share")

    def test_sanitize_defaults_to_in_place(self) -> None:
        parser = build_parser()
        args = parser.parse_args(["sanitize"])
        self.assertEqual(args.mode, "in-place")

    def test_scan_parser_accepts_color_mode(self) -> None:
        parser = build_parser()
        args = parser.parse_args(["scan", "--color", "always"])
        self.assertEqual(args.color, "always")


if __name__ == "__main__":
    unittest.main()
