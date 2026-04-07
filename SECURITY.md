# Security Policy

`vibe-sanitizer` handles code and text that may contain credentials or other private data. Please report security issues responsibly.

## Please Report Privately

Do not open a public issue for:

- detector bypasses that could hide real secrets
- bugs that expose raw secret values in output
- unsafe redaction behavior
- export behavior that unintentionally preserves sensitive content

## What To Send

Please include:

- a short summary
- impact
- steps to reproduce
- affected version or commit
- sample input with all real secrets replaced by fake values

## What Not To Send

- live credentials
- private keys
- production customer data

## Response Policy

There is no formal SLA yet, but reports will be reviewed as quickly as possible.

Until a dedicated security contact is added, report issues privately to the repository owner.
