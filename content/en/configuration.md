# Configuration

Hydro-CPS-Sim uses YAML files to configure the water network, controllers, communication and attacks. Copy an example, change the settings you need and run it with `--config`.

This page introduces the original `examples/c_town/config.yaml` water scene. To connect another physical simulator, see [UPSI Configuration](upsi-configuration.html) under Extended Experiments.

## File structure

| Section | Purpose |
| --- | --- |
| Model and component paths | INP, OpenPLC, ns-3 and output directories |
| iterations, time | Run limit and hydraulic step |
| initial_tank_values, actuators | Initial tank levels and pump/valve states |
| physics | EPANET control and stepping options |
| plcs | Sensors, actuators and control rules |
| network | Communication nodes, links and addresses |
| attacks | Attack settings and active windows |

The following fragment shows the main fields. Copy the complete C-Town example for its PLC list and network topology.

```yaml
root_path: /path/to/workspace
inp_file: ctown_map.inp
output_path: output/baseline
openplc_path: ../../../OpenPLC_v3
ns3_path: ../../../ns-3-dev-git
iterations: 100
initial_tank_values:
  T1: '3'
  T2: '.5'
actuators:
  - {name: PU1, initial_state: closed}
  - {name: PU2, initial_state: open}
physics:
  inp_controls: strip
  step_order: next-run
  init_flag: 0
time:
  - duration: [EN_DURATION, 86400]
  - hydraulic_timestep: [EN_HYDSTEP, 300]
```

## Paths and runtime

| Field | Meaning |
| --- | --- |
| root_path | Installation workspace |
| inp_file | EPANET model with pipes, equipment and demand patterns |
| output_path | This experiment's output directory |
| openplc_path | OpenPLC root |
| ns3_path | ns-3 root |
| iterations | Run limit, 100 in the example; override with --iterations |
| network_topology_type | complex label in examples; network contains the actual connections |

Relative paths normally start beside the YAML file. Check paths when moving a scene, and give experiments separate output directories. The retained noise_scale/log_level fields are not used as generic noise or logging controls by the current runner.

## Hydraulic time and initial conditions

Each time entry contains an EPANET parameter name and a value. hydraulic_timestep: [EN_HYDSTEP, 300] sets the nominal step to 300 s. The example retains duration; the current runner configures the hydraulic horizon from step and iteration count.

initial_tank_values assigns initial levels by tank name in INP units. C-Town uses T1–T7. Actuator names must match pump/valve links.

| Actuator field | Meaning |
| --- | --- |
| name | Pump/valve name, such as PU1 or V2 |
| initial_state | open or closed; open enables the link and closed disables it |

Equipment without an automatic rule holds its initial state unless another experiment control changes it. Use hydraulic sim_time for physical-time plots and iteration to find the corresponding control record.

## EPANET options

| Field under physics | Default | Meaning |
| --- | --- | --- |
| inp_controls | strip | Remove runtime INP CONTROLS/RULES for external OpenPLC control; keep retains them |
| step_order | next-run | Native stepping order: next-run or run-next |
| init_flag | 0 | Hydraulic initialization flag |
| also_set_setting | false | Also write the native link setting when controlling it |

These fields can also be nested under physics.epynet; that subsection takes precedence when present. Usually keep the defaults while changing models, thresholds or attacks.

## PLCs and measurements

plcs assigns sensors and outputs. One PLC owns each measurement; SCADA forwards it to other controllers when required.

| Field | Meaning |
| --- | --- |
| name | PLC identifier matching its network endpoint |
| sensors | Locally measured tags |
| actuators | Locally controlled pumps/valves |
| controls | Ordered control rules |

Tank names such as T1 mean level, junction names such as J285 mean pressure, and tags ending in F such as PU1F mean link flow. Units follow INP.

For example, PLC2 measures T1 and PLC1 uses it to control PU1:

```yaml
plcs:
  - name: PLC1
    sensors: [PU1F]
    actuators: [PU1]
    controls:
      - {dependant: T1, actuator: PU1, type: below, value: 4.0, action: open}
      - {dependant: T1, actuator: PU1, type: above, value: 6.3, action: closed}
  - name: PLC2
    sensors: [T1]
    actuators: []
    controls: []
```

Combine this fragment with actuator initial values and a full network. scada.name identifies SCADA; namespaces and addresses belong to network endpoints/LANs.

## Control rules

| Field | Meaning |
| --- | --- |
| dependant | Measurement used by the rule |
| actuator | Controlled pump/valve |
| type | below or above the threshold |
| value | Threshold in the measurement's units |
| action | open or closed when the condition holds |

The example opens PU1 below 4.0 and closes it above 6.3. Between the thresholds it holds state. Comparisons are strict; equality does not trigger. Later assignments can override earlier ones when several conditions hold, so avoid conflicting rules.

## Network and attacks

See [Network Configuration](configuration-network.html). Match PLC, SCADA and attacker names across endpoints, LAN addresses and targets.

Use attacks.enabled and attacks.scenarios to select attacks, targets and iteration windows. See [Attack Configuration](configuration-attacks.html) and [Experiments](experiments.html).

## Outputs

Results go to output_path: physics.csv, actuator_state.csv, SCADA observations and attack events. Optional reporting.key_variables selects key columns such as PLC2.PLC2_T1; otherwise water defaults apply.

```bash
bash scripts/run_all.sh --config examples/c_town/config.yaml --iterations 100 --logic-wait 0.3
```

logic-wait is wall-clock PLC scan waiting, separate from the hydraulic step. For power, thermal or another solver, continue with [Extended Experiments](extensions.html).
