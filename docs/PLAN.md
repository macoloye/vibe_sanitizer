# Roadmap

This document tracks the public roadmap for `vibe-sanitizer`.

## Current Scope

The project currently provides:

- Git-aware scanning for `working-tree`, `staged`, `tracked`, and `commit`
- in-place sanitization for findings that are safe to rewrite
- export of a separate sanitized copy
- starter config generation through `.vibe-sanitizer.yml`
- modular detector structure for future expansion

## Near-Term Priorities

### 1. Detector Coverage

Expand built-in coverage for:

- more cloud credentials
- more provider-specific API keys
- SSH and certificate-related material
- framework-specific config file patterns

### 2. False Positive Controls

Improve:

- allowlist ergonomics
- detector-specific suppression
- path-based exclusions
- clearer review-required classification

### 3. Export UX

Improve:

- export summaries
- preview mode
- better placeholder customization
- public-safe export examples

### 4. Integrations

Planned integrations include:

- `pre-commit`
- GitHub Actions
- example CI workflows

### 5. Documentation

Planned documentation improvements:

- install instructions for `pipx` or `uvx`
- example configs
- before-and-after examples
- screenshots or demo GIFs

## Design Principles

- never print full secret values in reports
- keep pre-commit rewrites conservative
- treat machine-specific paths as first-class sensitive data
- keep the detector system easy to extend

## Out of Scope

The project is not trying to:

- rewrite Git history
- replace full DLP or enterprise secret-scanning platforms
- guarantee that exported repos are runnable after redaction

## Contributing To The Roadmap

If you want to contribute a feature, detector, or integration, open an issue or pull request with:

- the user problem
- the expected behavior
- tradeoffs or false-positive risk
- proposed tests
