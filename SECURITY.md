# Security Policy

## Reporting a vulnerability

Please **do not open a public issue** for a vulnerability. Use
[GitHub private vulnerability reporting](https://github.com/dcotecnologia/kubescope-themes/security/advisories/new)
for this repository, or write to the maintainers listed in `pyproject.toml`. We acknowledge a report
within a few days, tell you what we found, and credit you in the release notes if you want.

## Supported versions

Only the latest release receives fixes.

## What it is

An extension is Python code that runs inside KubeScope with the same rights as the app. Its permissions
(`kubescope-extension.toml`) catch mistakes and tell you what it does; they are **not a sandbox**. Read
[the security notes of the SDK](https://github.com/dcotecnologia/kubescope-sdk/blob/main/docs/permissions.md)
before you install any extension.

## Guarantees this project keeps

- It asks for the least permissions it needs, and the README says why it asks for each one.
- It reads clusters and accounts only through the services the app lends it, and changes nothing outside the write mode.
- It never stores or logs credentials or secrets, and it makes no network request of its own beyond what the README says.
- Every release is a tag; KubeScope installs what it recommends only if the files are the ones whose hash it pinned.
