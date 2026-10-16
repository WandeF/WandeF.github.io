# Configuration

Hydro-CPS-Sim organizes experiments using YAML configuration files. The default is `examples/c_town/config.yaml`.

## Configuration files

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

## Creating a scenario

Copy `config.yaml` to create a scenario, change its water model, control or network settings, and select the file with `--config` when running the simulation.

## Sensor and control mappings

The `plcs` section assigns sensors and actuators from the water model to PLCs. SCADA forwards cross-PLC data. The `network` section defines endpoints, namespaces and connections for PLC, SCADA and attack nodes.

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

Attack types include `modbus_mitm`, `udp_dos` and `openplc_logic_injection`. Use `trigger.type: iteration_window` with `start_iteration` and `end_iteration` to set the active window. Start with the [experiment presets](experiments.html) to configure nodes, targets and rules for each type.
