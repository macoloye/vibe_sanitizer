---
name: vibe-sanitizer
description: Use this skill when an agent needs to scan a Git repository for secrets, credentials, or machine-specific file paths, then sanitize safe findings in place or export a sanitized shareable copy using the bundled Python source in ./src.
version: 0.1.0
---

# vibe-sanitizer

Use this skill when the user wants an agent to make a repository safer before commit, before sharing, or before publishing.

This skill is intended for local agent workflows in tools such as Codex, Claude Code, OpenClaw and similar coding agents that can read the repository and run shell commands.

## When To Use

Use this skill when the user wants to:

- scan a repository for secrets before commit
- scan staged files before opening a pull request
- sanitize safe findings in place without exposing raw secret values
- prepare a separate sanitized copy for sharing with another person or tool
- audit a tracked repository or a specific commit for obvious sensitive data
- check AI-assisted or vibe-coded repositories for leaked machine paths

Prefer this skill when the task is local repository hygiene, not when the goal is:

- rewriting Git history
- replacing a full enterprise secret scanning platform
- doing broad compliance or DLP analysis

## What It Catches

The bundled CLI currently detects:

- PEM-style private key blocks
- OpenAI-style API keys such as `sk-...`
- AWS access key ids such as `AKIA...` and `ASIA...`
- GitHub tokens such as `ghp_...` and `github_pat_...`
- Slack tokens such as `xoxb-...`
- bearer tokens
- URLs with embedded credentials
- quoted secret-like assignments such as `api_key = "..."`, `token = "..."`, or `password = "..."`
- absolute workspace paths
- home-directory paths such as `/Users/<name>/...` and `/home/<name>/...`
- temporary directory paths
- Windows user-directory paths such as `C:\Users\<name>\...`

The CLI classifies findings into:

- safe to rewrite in place
- review-required findings that should be flagged but not automatically rewritten in the original repository

## Distribution Model

The agent should run the bundled code directly with Python.

Primary command form:

```bash
cd {{skill_dir}}/src
python3 -m vibe_sanitizer.cli ...
```

If the current working directory is not the skill package, switch into `{{skill_dir}}/src` before running commands.

Because the CLI scans the current repository by default, the agent must either:
- run the command while the audited repository is the current working directory, or
- pass `--root <target-repo>` explicitly

## What This Skill Does

This skill teaches the agent to:

- run the bundled `vibe_sanitizer` CLI from the local `src/` directory
- choose the right Git-aware scan scope
- report findings without exposing raw secret values
- sanitize only the findings that are safe to rewrite in place
- export a separate sanitized copy when the user wants a shareable repository

## Runtime Setup

Run the module from the bundled source, but target the audited repository.

Verify the bundled CLI:

```bash
cd {{skill_dir}}/src
python3 -m vibe_sanitizer.cli --help
```

If this fails, confirm that:

- `{{skill_dir}}/src/vibe_sanitizer/cli.py` exists in the skill package
- `python3` is available
- the command is being run from `{{skill_dir}}/src`

## Workflow

1. Confirm the target repository root.
2. Run the bundled CLI from `{{skill_dir}}/src` with `python3 -m vibe_sanitizer.cli`.
3. If the current working directory is not the audited repository, pass `--root <target-repo>`.
4. Choose the narrowest useful Git scope:
   - `working-tree` for tracked and untracked files that are not ignored
   - `staged` for content about to be committed
   - `tracked` for a repo-wide audit of tracked files
   - `commit --commit <sha>` for a specific commit
5. Run `scan` first.
6. Summarize findings by file, detector, severity, and whether they are fixable or review-required.
7. Never print raw secret values in the response.
8. Use `sanitize --mode in-place` only for safe pre-commit cleanup in the original repository.
9. Use `export` when the user wants a separate sanitized copy for sharing or publishing.

## Commands

CLI verification:

```bash
cd {{skill_dir}}/src
python3 -m vibe_sanitizer.cli --help
```

Working tree scan:

```bash
cd {{skill_dir}}/src
python3 -m vibe_sanitizer.cli scan --root {{repo_dir}} --scope working-tree
```

Staged scan:

```bash
cd {{skill_dir}}/src
python3 -m vibe_sanitizer.cli scan --root {{repo_dir}} --scope staged
```

Tracked file audit:

```bash
cd {{skill_dir}}/src
python3 -m vibe_sanitizer.cli scan --root {{repo_dir}} --scope tracked --format json
```

Specific commit audit:

```bash
cd {{skill_dir}}/src
python3 -m vibe_sanitizer.cli scan --root {{repo_dir}} --scope commit --commit <sha>
```

Safe in-place cleanup:

```bash
cd {{skill_dir}}/src
python3 -m vibe_sanitizer.cli sanitize --root {{repo_dir}} --scope staged --mode in-place
```

Shareable export:

```bash
cd {{skill_dir}}/src
python3 -m vibe_sanitizer.cli export --root {{repo_dir}} --scope tracked --output {{repo_dir}}/safe-share
```

Starter config:

```bash
cd {{skill_dir}}/src
python3 -m vibe_sanitizer.cli init-config --path {{repo_dir}}/.vibe-sanitizer.yml
```

## Guardrails

- Never paste full secrets or full local paths into the response.
- Prefer masked snippets such as `sk-***abcd`.
- Prefer the narrowest scan scope that answers the user request.
- Treat local home paths, workspace paths, and temporary paths as sensitive when they leak machine context.
- Do not rewrite review-required findings automatically unless the user explicitly asks and understands the risk.
- Do not export into a directory inside the source repository.
- Do not treat an exported sanitized copy as the default replacement for the main development repository.
- Do not assume a global `vibe_sanitizer` install when the bundled `src/` code is available.

## Agent Response Style

When reporting results:

- mention the scope used
- summarize counts by severity when useful
- group findings by file when useful
- identify which findings are safe to fix in place
- identify which findings still need manual review
- avoid reproducing raw credentials

## Current Status

This skill targets the bundled Python implementation of the `vibe_sanitizer` CLI. The CLI supports:

- `scan`
- `sanitize`
- `export`
- `init-config`
