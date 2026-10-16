# Installation

Use `install.sh` to install Hydro-CPS-Sim and its dependencies. The installer configures system packages, a Conda environment, the OpenPLC command-line runtime, ns-3 and DHALSIM-epynet.

## Environment requirements

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

Run the installer:

```bash
bash install.sh
conda activate hydro-cps
```

Building ns-3 and OpenPLC may take some time. The default environment is named `hydro-cps`; see `bash install.sh --help` for `--env`, `--jobs`, and `--parent` options.

## Run the tests

The installer checks EPANET library loading and runs the Python test suite. You can also run the tests manually:

```bash
python -m unittest discover -s tests
```

After installation, follow [Quick Start](quickstart.html) to run the C-Town example.

The installer rewrites five top-level path keys in every C-Town YAML and saves changed originals under `output/install-backups/`. Update the paths when moving to another machine or dependency directory.
