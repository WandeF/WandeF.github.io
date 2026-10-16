# Contributing & Feedback

You are welcome to report issues, improve the documentation or contribute features.

## Reporting a problem

Please use the project's [GitHub Issues](https://github.com/WandeF/hydro-cps-sim/issues) and include:

1. OS and Python / Conda versions.
2. Git commit and sanitized configuration files.
3. Reproduction commands and relevant errors.
4. Expected and actual results.

## Updating the website

Documentation repository: [WandeF/WandeF.github.io](https://github.com/WandeF/WandeF.github.io). Edit Markdown pages under `content/zh/` and `content/en/`, then run:

```bash
python build.py
```

Generated files are written to `site/`. Preview locally with `python -m http.server 8000 --directory site`. Push to `main` in [WandeF/WandeF.github.io](https://github.com/WandeF/WandeF.github.io) to build and deploy automatically to <https://wandef.github.io/>.

## Contribution areas

Contributions can improve installation and configuration instructions, add reproducible examples, fix issues or refine translations. Briefly describe your changes and how you tested them. Include configurations and run records with experiment examples.
