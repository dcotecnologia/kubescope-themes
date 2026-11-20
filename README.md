# KubeScope Themes

[![CI](https://github.com/dcotecnologia/kubescope-themes/actions/workflows/ci.yml/badge.svg)](https://github.com/dcotecnologia/kubescope-themes/actions/workflows/ci.yml)
[![Coverage](https://img.shields.io/endpoint?url=https%3A%2F%2Fraw.githubusercontent.com%2Fdcotecnologia%2Fkubescope-themes%2Fbadges%2Fcoverage.json)](https://github.com/dcotecnologia/kubescope-themes/actions/workflows/ci.yml)
[![Release](https://img.shields.io/github/v/release/dcotecnologia/kubescope-themes)](https://github.com/dcotecnologia/kubescope-themes/releases)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python 3.15](https://img.shields.io/badge/python-3.15-3776AB.svg?logo=python&logoColor=white)](pyproject.toml)
[![Code style: ruff](https://img.shields.io/badge/code%20style-ruff-D7FF64.svg?logo=ruff&logoColor=black)](https://docs.astral.sh/ruff/)
[![KubeScope extension](https://img.shields.io/badge/KubeScope-extension-326CE5.svg?logo=kubernetes&logoColor=white)](https://github.com/dcotecnologia/kubescope)

Color themes for [KubeScope](https://github.com/dcotecnologia/kubescope), the Kubernetes desktop console: the
themes that come besides **Light** and **Dark**, which are built into the app.

It is an **extension** written against the [KubeScope SDK](https://github.com/dcotecnologia/kubescope-sdk)
and nothing else of the app. KubeScope installs it on the first run, and you can uninstall and reinstall it in
**Settings → Extensions**. The themes show in **Settings → Theme** with the others.

## The themes

| Theme | Base | Theme | Base |
| ----- | ---- | ----- | ---- |
| Abyss | dark | Quiet Light | light |
| Dark Modern | dark | Sepia | light |
| High Contrast | dark | Solarized Dark | dark |
| Light Modern | light | Solarized Light | light |
| macOS Dark | dark | Tomorrow Night Blue | dark |
| macOS Light | light | Midnight | dark |
| Monokai | dark | | |

Every theme keeps the text readable: a test checks a contrast of at least 4.5:1 between the text and the page.

## Use

Open **Settings → Theme**, pick one and save. The themes of the extension cannot be deleted from there (they go
away with the extension); to change one, choose it and press **New theme...** to start from a copy that is yours.
If you chose one of these themes and uninstall the extension, KubeScope goes back to the default theme.

## Add a theme

1. In KubeScope, **Settings → New theme...**, pick the colors and save; the theme is written to your themes
   folder (**Open the themes folder**).
2. Copy that file to `src/kubescope/theme_pack/themes/` with a short, lowercase name (`my-theme.json`): the file
   name is the id of the theme.
3. Run `make test FILE=tests/test_themes.py`: it checks that the theme is valid and readable.
4. Open a pull request, ideally with a screenshot.

A theme is JSON with a `name`, a `base` (`light` or `dark`) and the `colors` it changes by role; everything else
comes from its base. An optional `opacity` object gives a role an opacity from `0` (clear) to `1` (solid). See
[the format](https://github.com/dcotecnologia/kubescope#themes) in the README of KubeScope.

## Permissions

| Permission | Why |
| ---------- | --- |
| `ui.theme` | Offer color themes to the app. The extension reads no cluster and runs no program |

## Develop

```text
workspace/
├── kubescope/          # the app
├── kubescope-sdk/      # the SDK
└── kubescope-themes/   # this project
```

```bash
make setup                            # dependencies and the pre-commit hook
make test FILE=tests/test_themes.py   # one test file; `make test` runs them all
make lint typecheck
```

To see your changes in the app as you make them, tick **Development mode** in **Settings → Extensions** and
install this folder: the app runs it in place and reloads it when a file changes.

### Layout

| Path | What it is |
| ---- | ---------- |
| `kubescope-extension.toml` | The manifest the app reads before installing |
| `src/kubescope/theme_pack/__init__.py` | `activate(ctx)`: offers each theme of the folder |
| `src/kubescope/theme_pack/themes/` | The themes, one `*.json` each |
| `tests/` | The tests |

## License

MIT. See [LICENSE](LICENSE).
