# Configuration

Hydro-CPS-Sim organizes experiments using YAML configuration files. The default is `examples/c_town/config.yaml`.

## What configuration controls

- Input hydraulic network files and simulation settings.
- External paths for OpenPLC and ns-3.
- Output directories and run length.
- Network, control, and experiment settings.

The installer updates five top-level path fields in the example configurations:

| Key | Purpose |
| --- | --- |
| `root_path` | Working directory for external dependencies |
| `openplc_path` | OpenPLC checkout or build directory |
| `ns3_path` | ns-3 checkout or build directory |
| `inp_file` | EPANET input file |
| `output_path` | Directory for generated results |

Update these paths when moving environments or replacing a model. Set `output_path` to a dedicated experiment output directory.

## Recommended practice

Keep the original validated baseline configuration intact. Make copies for new experiments and record the git commit, exact YAML, invocation, and outputs for each run.

## Configuration constraints

PLC sensor and actuator names must match the water model, and cross-PLC dependencies must be forwarded through SCADA. Use consistent identifiers for network endpoints, namespaces and attack targets. When copying a scenario, check its model, control mapping and network topology together.

## Simulation and control parameters

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

Attack types include `modbus_mitm`, `udp_dos`, and `openplc_logic_injection`. An `iteration_window` trigger uses `start_iteration` and `end_iteration`. Scenarios also need matching network endpoints, interception rules or logic injection settings; adding only a switch to the baseline is insufficient. See actual presets under [experiments](experiments.html).
