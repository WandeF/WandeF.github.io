# Installation

These instructions are based on the published [`install.sh`](https://github.com/WandeF/hydro-cps-sim/blob/2406aa649738c585e635b3661d1b9431db73edb8/install.sh). Review the script before running it, since it installs system packages and checks out external dependencies.

## Source-defined environment requirements

| Item | Requirement |
| --- | --- |
| Operating system | Ubuntu 22.04 / 24.04, x86_64 |
| Python | Python 3.10 in the Conda environment |
| Environment manager | Conda |
| Privileges | `sudo` is needed for installation and networking |
| Internet | Required for packages and source repositories |
| Main dependencies | OpenPLC command-line runtime, ns-3, DHALSIM-epynet |

> **Important:** The installer builds the OpenPLC command-line runtime, not the full web management service.

## Clone the repository

```bash
git clone https://github.com/WandeF/hydro-cps-sim.git
cd hydro-cps-sim
```

## Preview installation steps

```bash
bash install.sh --dry-run
```

## Install

After checking the required privileges and system compatibility:

```bash
bash install.sh
conda activate hydro-cps
```

Building ns-3 and OpenPLC may take some time. The default environment is named `hydro-cps`; see `bash install.sh --help` for `--env`, `--jobs`, and `--parent` options.

## Run the project test suite

```bash
python -m unittest discover -s tests
```

Successful documentation generation does **not** establish successful installation of the simulation runtime. The runtime must be tested separately on a compatible Linux machine.


Source review: [hydro-cps-sim @ 2406aa6](https://github.com/WandeF/hydro-cps-sim/tree/2406aa649738c585e635b3661d1b9431db73edb8) · 2026-10-15.

The installer rewrites five top-level path keys in every C-Town YAML and saves changed originals under `output/install-backups/`. Check paths after moving to a different machine; do not reuse developer-specific absolute paths from the source.
