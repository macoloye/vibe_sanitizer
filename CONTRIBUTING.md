# Contributing

Thanks for contributing to `vibe-sanitizer`.

## What We Accept

- bug fixes
- new detectors
- redaction safety improvements
- performance improvements
- documentation updates
- tests for true positives, false positives, and edge cases

## Before Opening a PR

1. Make sure the change fits the scope of the project.
2. Add or update tests when behavior changes.
3. Keep reports safe: never print raw secret values in output.
4. Prefer narrow, well-explained pull requests over broad refactors.

## Development

Run the CLI locally:

```bash
pip install -e .
vibe_sanitizer --help
vibe_sanitizer scan --scope working-tree
```

Run tests:

```bash
PYTHONPATH=src python3 -m unittest discover -s tests -v
```

## Adding a Detector

New detectors should:

- live under `src/vibe_sanitizer/detectors/`
- have a clear detector id and message
- provide masked previews instead of raw values
- declare whether they are safe for in-place edits
- include tests that cover both detection and redaction behavior

## Pull Request Guidelines

- explain the user-facing problem
- describe the detection or redaction tradeoff
- include tests for the changed behavior
- avoid unrelated formatting-only changes

## Reporting Bugs

For normal bugs or feature requests, open an issue.

For security-sensitive issues, do not open a public issue with details. Use the process in [SECURITY.md](SECURITY.md).
