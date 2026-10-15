# Quick Start

This guide uses the project's C-Town example as an entry point. The commands follow the currently published run script and assume a successful installation.

> Each run clears `runtime/`, `reports/`, `st/`, and `plcs/` under the configured output directory. Copy results to a separate directory before the next experiment. Start as a normal user; the script requests sudo when needed.

## Run a simulation

```bash
cd hydro-cps-sim
conda activate hydro-cps
bash scripts/run_all.sh --logic-wait 0.3
```

You may override the configured number of iterations to try a shorter run:

```bash
bash scripts/run_all.sh --iterations 10 --logic-wait 0.3
```

The value `10` is illustrative, not a validated benchmark configuration.

## Select a configuration

```bash
bash scripts/run_all.sh --config examples/c_town/config.yaml
```

| Option | Purpose |
| --- | --- |
| `--config PATH` | YAML configuration file |
| `--iterations N` | Number of iterations |
| `--logic-wait SECONDS` | Wait after SCADA downlink before reading control outputs |
| `--poll-interval SECONDS` | Marker polling interval |
| `--scada-modbus-workers N` | Concurrent SCADA Modbus workers |

Run `bash scripts/run_all.sh --help` for the definitive interface.

## Outputs

According to the runner, the exported CSV files are located under the configured output directory in `reports/csv`. At completion, the script prints a message resembling:

```text
[DONE] Results: <output_path>/reports/csv
```

The actual path comes from `output_path` in the configuration. The placeholder above is not a literal path.

Continue with [experiments](experiments.html) and [configuration](configuration.html).


Source review: [hydro-cps-sim @ 2406aa6](https://github.com/WandeF/hydro-cps-sim/tree/2406aa649738c585e635b3661d1b9431db73edb8) · 2026-10-15.
