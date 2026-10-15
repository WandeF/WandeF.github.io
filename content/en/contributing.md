# Contributing & Feedback

Suggestions on functionality, installation, and reproducibility are welcome. A formal contribution policy and the open-source license will be established as the release plan is finalized.

## Reporting a problem

Please use the project's [GitHub Issues](https://github.com/WandeF/hydro-cps-sim/issues) and include:

1. OS and Python / Conda versions.
2. Git commit and sanitized configuration files.
3. Reproduction commands and relevant errors.
4. Expected and actual results.

## Updating the website

The website is intentionally separated from the simulator repository. Edit Markdown pages under `content/zh/` and `content/en/`, then run:

```bash
python build.py
```

Generated files are written to `site/`. Preview locally with `python -m http.server 8000 --directory site`. Push to `main` in [WandeF/WandeF.github.io](https://github.com/WandeF/WandeF.github.io) to build and deploy automatically to <https://wandef.github.io/>.

## Before an official public release

Consider adding `LICENSE`, `CONTRIBUTING.md`, version-management guidance, and a responsible security disclosure process.
