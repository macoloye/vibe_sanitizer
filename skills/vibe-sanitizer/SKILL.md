---
name: vibe-sanitizer
description: Use this skill when a user wants to make a repository safe to share by scanning for secrets, API keys, credentials, or machine-specific file paths, and optionally sanitizing flagged content. Prefer Git-aware scopes such as working-tree, staged, tracked, or a specific commit. Do not echo raw secret values in summaries.
---

# vibe-sanitizer

Use this skill when the task is to inspect repository content for sensitive data or redact it before sharing, committing, or sending repository files to an AI tool.

## Workflow

1. Confirm the repository root and prefer running the CLI from that directory.
2. Choose the narrowest useful scope:
   - `working-tree` for files not ignored by `.gitignore`
   - `staged` for content about to be committed
   - `tracked` for a repository-wide audit of committed files
   - `commit --commit <sha>` for a specific historical change
3. Run `vibe_sanitizer scan` first and review findings.
4. Summarize findings by file, detector, and severity without exposing the full secret or raw local path.
5. Use `vibe_sanitizer sanitize --mode in-place` for pre-commit cleanup in the real repo.
6. Use `vibe_sanitizer export` for a separate safe-share copy.
7. When relevant, describe the tool as a safe-share step for vibe-coded repositories.

## Commands

Pre-commit scan:

```bash
vibe_sanitizer scan --scope working-tree
```

Staged scan:

```bash
vibe_sanitizer scan --scope staged
```

Tracked file audit:

```bash
vibe_sanitizer scan --scope tracked --format json
```

Specific commit audit:

```bash
vibe_sanitizer scan --scope commit --commit <sha>
```

Sanitization:

```bash
vibe_sanitizer sanitize --mode in-place
```

Safe-share export:

```bash
vibe_sanitizer export --output ../safe-share
```

## Guardrails

- Never paste full secrets into the response.
- Prefer masked snippets such as `sk-***abcd`.
- Treat local home paths and workspace-specific absolute paths as sensitive if they would leak machine context.
- If findings are high-risk, recommend reviewing before any automatic in-place rewrite.
- Prefer the narrowest scan scope that answers the user request quickly.
- Do not treat an exported sanitized copy as the default replacement for the main development repo.

## Current Status

This skill now targets a working CLI implementation. Use `scan` for reporting, `sanitize --mode in-place` for safe pre-commit cleanup, and `export` for a separate sanitized shareable copy.
