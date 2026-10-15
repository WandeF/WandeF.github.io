# Configuration

The published runner accepts a YAML file and defaults to `examples/c_town/config.yaml`.

## What configuration controls

- Input hydraulic network files and simulation settings.
- External paths for OpenPLC and ns-3.
- Output directories and run length.
- Network, control, and experiment settings.

The installer explicitly processes several top-level path keys:

| Key | Purpose |
| --- | --- |
| `root_path` | Working directory for external dependencies |
| `openplc_path` | OpenPLC checkout or build directory |
| `ns3_path` | ns-3 checkout or build directory |
| `inp_file` | EPANET input file |
| `output_path` | Directory for generated results |

These keys can be verified against [install.sh](https://github.com/WandeF/hydro-cps-sim/blob/2406aa649738c585e635b3661d1b9431db73edb8/install.sh). Other keys have deliberately been left for a future source-verified reference.

## Recommended practice

Keep the original validated baseline configuration intact. Make copies for new experiments and record the git commit, exact YAML, invocation, and outputs for each run.

## To be completed

- Full field reference grouped by subsystem.
- Verified baseline and attack YAML examples.
- Mapping rules connecting network topology, PLC signals, and hydraulic elements.


Source review: [hydro-cps-sim @ 2406aa6](https://github.com/WandeF/hydro-cps-sim/tree/2406aa649738c585e635b3661d1b9431db73edb8) · 2026-10-15.

## Additional source-checked fields

| Field | Baseline value or role |
| --- | --- |
| `iterations` | 100; runner can override |
| `noise_scale` | 0.0 |
| `time` | EPANET duration 86400 seconds; hydraulic step 300 seconds |
| `physics` | `inp_controls: strip`, `step_order: next-run`, `init_flag: 0` |
| `plcs` | Sensors, actuators and control rules for PLC1–PLC8 |
| `network` | ns-3 backend, realtime scheduling, routing, nodes, links, LANs and TAPs |
| `attacks.enabled` | Global switch in attack presets |
| `attacks.scenarios` | Scenario types, triggers, targets and type-specific options |

Published types include `modbus_mitm`, `udp_dos`, and `openplc_logic_injection`. An `iteration_window` trigger uses `start_iteration` and `end_iteration`. Scenarios also need matching network endpoints, interception rules or logic injection settings; adding only a switch to the baseline is insufficient. See actual presets under [experiments](experiments.html).
