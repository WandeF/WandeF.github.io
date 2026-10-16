# Quick Start

After installation, run your first closed-loop simulation with the C-Town example.

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

This command limits the simulation to 10 iterations to check startup and result export.

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

Results are exported to `reports/csv` under `output_path`. Logs and stage timings are saved in `logs/` and `timing/`. At completion, the script prints:

```text
[DONE] Results: <output_path>/reports/csv
```

The actual path comes from `output_path` in the configuration. The placeholder above is not a literal path.

Continue with [experiments](experiments.html) and [configuration](configuration.html).
