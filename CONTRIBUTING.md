# Contributing to KubeScope Themes

Thanks for helping. This page gets you from a clone to a pull request. The commit format, the code of
conduct and the standards of the whole project are those of
[KubeScope](https://github.com/dcotecnologia/kubescope):

- [COMMITING.md](https://github.com/dcotecnologia/kubescope/blob/main/COMMITING.md): Conventional Commits, in English.
- [CODE_OF_CONDUCT.md](https://github.com/dcotecnologia/kubescope/blob/main/CODE_OF_CONDUCT.md).
- [AGENTS.md](https://github.com/dcotecnologia/kubescope/blob/main/AGENTS.md): the code standards, for people and AI assistants alike.

## Set up

```text
workspace/
├── kubescope/        # the app (branch `dev/v2` while the extension API is unstable)
├── kubescope-sdk/    # the SDK
└── kubescope-themes/   # this project
```

```bash
git clone https://github.com/dcotecnologia/kubescope-themes.git
cd kubescope-themes
make setup          # uv sync and the pre-commit hook
```

The tests of an extension run it in the window of the app, so the app is a development dependency
(`kubescope = { path = "../kubescope", editable = true }`); the extension itself imports only
`kubescope.sdk` and its own package, and a test keeps it so.

## Workflow

1. Create a branch from `main`. Do not commit to `main` directly.
2. Make one focused change per commit, with its tests.
3. Run the checks below, and add an entry to `CHANGELOG.md` under **[Unreleased]**.
4. Open a pull request that says what changed and why. The pipeline runs the same checks.

## Checks

```bash
make test FILE=tests/test_x.py   # the test file of your change
make lint typecheck
```

Run one test file at a time while you work (`make test FILE=...` leaves the coverage out); `make test`
runs them all with the coverage, which stays at **100%** (`--cov-fail-under=100`): cover the code with tests, and never
lower the threshold or widen the omissions to get green.

## Releases

A release is a tag. Bump the version in `pyproject.toml` and `kubescope-extension.toml`, move the **[Unreleased]**
entries of `CHANGELOG.md` under the new version, merge, and push the tag `vX.Y.Z`. The release pipeline
checks that the tag, the versions and the changelog agree, lints and tests, and publishes the release with the hash KubeScope pins for that tag.
