import contextlib
import io
import subprocess
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace

from vibe_sanitizer.commands import run_export, run_init_config, run_sanitize, run_scan
from vibe_sanitizer.constants import EXIT_ERROR, EXIT_FINDINGS, EXIT_OK


class CommandTests(unittest.TestCase):
    def test_init_config_writes_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            config_path = Path(tmp_dir) / ".vibe-sanitizer.yml"
            args = SimpleNamespace(path=str(config_path), force=False)
            with contextlib.redirect_stdout(io.StringIO()):
                result = run_init_config(args)
            self.assertEqual(result, EXIT_OK)
            self.assertTrue(config_path.exists())

    def test_scan_and_sanitize_workflow(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            repo_root = Path(tmp_dir)
            self._init_repo(repo_root)
            source = repo_root / "app.py"
            source.write_text(
                'api_key = "sk-abcdefghijklmnopqrstuvwxyz123456"\n'
                'password = "supersecret"\n',
                encoding="utf-8",
            )

            scan_args = SimpleNamespace(
                root=str(repo_root),
                config=None,
                scope="working-tree",
                commit=None,
                format="json",
            )
            with contextlib.redirect_stdout(io.StringIO()):
                result = run_scan(scan_args)
            self.assertEqual(result, EXIT_FINDINGS)

            sanitize_args = SimpleNamespace(
                root=str(repo_root),
                config=None,
                scope="working-tree",
                commit=None,
                mode="in-place",
            )
            with contextlib.redirect_stdout(io.StringIO()):
                result = run_sanitize(sanitize_args)
            self.assertEqual(result, EXIT_FINDINGS)
            updated = source.read_text(encoding="utf-8")
            self.assertIn("<REDACTED_OPENAI_KEY>", updated)
            self.assertIn('password = "supersecret"', updated)

    def test_export_writes_sanitized_copy_without_git(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            repo_root = Path(tmp_dir) / "repo"
            export_root = Path(tmp_dir) / "safe-share"
            self._init_repo(repo_root)
            tracked = repo_root / "tracked.py"
            tracked.write_text('token = "ghp_abcdefghijklmnopqrstuvwxyz123456"\n', encoding="utf-8")
            subprocess.run(["git", "add", "tracked.py"], cwd=repo_root, check=True)
            subprocess.run(["git", "commit", "-m", "init"], cwd=repo_root, check=True, capture_output=True)

            args = SimpleNamespace(
                root=str(repo_root),
                config=None,
                scope="tracked",
                commit=None,
                output=str(export_root),
                init_git=False,
            )
            with contextlib.redirect_stdout(io.StringIO()):
                result = run_export(args)
            self.assertEqual(result, EXIT_OK)
            exported = (export_root / "tracked.py").read_text(encoding="utf-8")
            self.assertIn("<REDACTED_GITHUB_TOKEN>", exported)
            self.assertFalse((export_root / ".git").exists())

    def test_export_inside_repo_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            repo_root = Path(tmp_dir) / "repo"
            self._init_repo(repo_root)
            (repo_root / "tracked.py").write_text("print('ok')\n", encoding="utf-8")
            output = io.StringIO()
            args = SimpleNamespace(
                root=str(repo_root),
                config=None,
                scope="working-tree",
                commit=None,
                output=str(repo_root / "sanitized"),
                init_git=False,
            )
            with contextlib.redirect_stderr(output):
                result = run_export(args)
            self.assertEqual(result, EXIT_ERROR)
            self.assertIn("outside the source repository", output.getvalue())

    def _init_repo(self, repo_root: Path) -> None:
        repo_root.mkdir(parents=True, exist_ok=True)
        subprocess.run(["git", "init", "-b", "main"], cwd=repo_root, check=True, capture_output=True)
        subprocess.run(["git", "config", "user.name", "Test User"], cwd=repo_root, check=True)
        subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=repo_root, check=True)


if __name__ == "__main__":
    unittest.main()
