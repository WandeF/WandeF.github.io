# UPSI Configuration

Select a physical backend, connect its signals and choose a sampling interval to use another physical model. This page introduces the UPSI additions to the existing scene format.

## Write the configuration

Keep the YAML format and add `schema_version: 2` at the top level to use explicit signal configuration. Put model, signal and timing settings under `physics`.

Use spaces, lists with `-`, explicit true/false and the quoted dimensionless unit `'1'`. PyYAML implicitly resolves unquoted on/off as booleans; quote them when strings are intended. Avoid duplicate keys and ambiguous numeric strings. See [YAML](https://yaml.org/spec/1.2.2/) and [PyYAML](https://pyyaml.org/wiki/PyYAMLDocumentation).

Use the field names listed below. Unrecognized fields may be ignored. Before running a scene, check the configuration with the commands at the end of this page.

## Scene structure

```yaml
schema_version: 2
output_path: output/baseline
openplc_path: ../../../OpenPLC_v3
ns3_path: ../../../ns-3-dev-git
iterations: 10
physics: {}
actuators: []
plcs: []
scada: {name: scada}
network: {}
attacks: {enabled: false, scenarios: []}
reporting: {key_variables: []}
```

This is an outline, not a runnable empty scene. Complete starting points are examples/power_feeder/config_v2.yaml, examples/ieee33_bw/config_baseline.yaml and examples/thermal_box/config.yaml. See [Network Configuration](configuration-network.html) and [Attack Configuration](configuration-attacks.html) for their dictionaries.

## Reuse an existing scene

Keep the original output/component paths, PLC rules, network and attacks. Add the following when selecting another physical model:

| Field | Purpose |
| --- | --- |
| schema_version: 2 | Explicit physical-signal configuration |
| physics.backend | Select EPANET, pandapower or your adapter |
| physics.model.path | Physical model file |
| physics.plugins | Register an independent adapter |
| physics.timing | Physical sampling interval |
| physics.signals | Logical names mapped to native ports |
| signals | Optional top-level direction, type, unit and bounds |
| actuators[].initial_state | Initial command with its declared type, e.g. true/false |
| quality_policy | Handling unsupplied, old or missing samples |
| initial_state | Optional typed initial-output declarations; the model supplies solved initial values |

Common settings are described in [Configuration](configuration.html), [Network](configuration-network.html) and [Attacks](configuration-attacks.html).

## Common physics fields

| Field below physics | Type / default | Meaning |
| --- | --- | --- |
| backend | v2 required string | dhalsim_epynet, pandapower or a declared plugin; legacy default water, with epanet/epynet aliases |
| model | v2 required mapping | Model declaration; built-ins and thermal use path; plugins may define other parameters |
| model.path | path | Model file relative to scene directory |
| plugins.NAME.factory | module:Class | Exactly one of factory and entry_point |
| plugins.NAME.entry_point | string | Named installed hydro_cps.physics entry point |
| plugins.NAME.dependency | optional module | Selected-backend import preflight |
| init_style | current / dhalsim | v2 defaults current; legacy water defaults dhalsim, restricted to compatible water backends |
| timing.mode | fixed_step | Current single-backend sampling schedule, distinct from internal solver stepping |
| timing.step_seconds | finite number > 0; v2 required | Requested interval in seconds; EPANET needs multiples of 1 s |
| timing.measurement_max_age_s | number ≥ 0; 0 | Nonzero age requires backend asynchronous-measurement capability |
| timing.tolerance.absolute_s | number ≥ 0 | Default min(1e-9, step/8), at most step/4 |
| timing.tolerance.relative | number ≥ 0 | Default 8× floating epsilon, at most 1e-6; final tolerance is also step-bounded |
| signals.observations | mapping | Logical observations to native output ports |
| signals.commands | mapping | Complete, unique logical commands to native input ports |
| quality_policy | optional mapping | Same as top level; duplicate declarations must agree |
| model_file, timestep | legacy fields | Model path and interval; timestep and timing.step_seconds must agree if both present |
| sensors, actuators | legacy power mappings | table / element / column, with missing or invert where applicable; normalized to signals |

Current initialization starts from a solved time-zero snapshot. Legacy water dhalsim retains zero row 0 and configured row 1 before its historical cycle convention; a 100-round water limit therefore has 99 control cycles. Compare initialization semantics before counting snapshots.

Backend describe().timing target/event_step declares solver capability, whereas scene timing.mode fixed_step selects the sampling schedule. Requests start from the last actual reached time, so internal events may shorten advancement.

## Signal mapping fields

Applies below physics.signals.observations.NAME or commands.NAME:

| Field | Type / default | Meaning |
| --- | --- | --- |
| port | required string | Declared native port with correct direction |
| dtype | float/int/bool/str; v2 required | May be supplemented by top-level signals; must match native type |
| unit | native unit | String logical unit; use quoted '1' |
| minimum, maximum | optional finite numbers | Numerical bounds; not valid for BOOL/string |
| scale | finite nonzero number; 1 | logical = native*scale+offset; commands use inverse |
| offset | finite number; 0 | Nonidentity affine transforms require float |
| invert | bool; false | BOOL polarity inversion |
| missing | backend option; error | Power supports zero_if_unsupplied for bus voltage only, not generic zero fill |
| unit_context.density_kg_m3 | positive number | Explicit water-column pressure conversion context |
| unit_context.gravity_m_s2 | positive number | Explicit gravity for that conversion |
| calibration_reason | nonempty string | Reason for same-unit nonidentity calibration; recorded in schema |

Top-level signals.NAME accepts direction, dtype, unit, minimum and maximum. Direction and duplicate metadata must agree with mappings. Every native input needs exactly one command; duplicate command ports fail.

```yaml
physics:
  signals:
    observations:
      P_GRID_KW: {port: metrics.total.p_grid_mw, dtype: float, unit: kW, scale: 1000}
    commands:
      LOAD24_ENABLE: {port: load.LOAD_BUS24.in_service, dtype: bool, unit: '1'}
```

MW→kW uses scale 1000; degC→K uses offset 273.15. The unit catalog separates active/reactive power and incompatible dimensions. Per-unit voltage allows identity without guessing a voltage base. See [UPSI](upsi.html).

## Configure the controller

Sensor ownership and threshold rules keep their original structure. Measurement names now refer to physics.signals.observations and commands to physics.signals.commands. Match each initial value to its declared type.

```yaml
actuators:
  - {name: LOAD24_ENABLE, initial_state: true}
plcs:
  - {name: PLC1, sensors: [V_BUS02], actuators: [], controls: []}
  - name: PLC3
    sensors: [V_BUS24, P_LOAD24]
    actuators: [LOAD24_ENABLE]
    controls:
      - {dependant: V_BUS02, actuator: LOAD24_ENABLE, type: below, value: 0.95, action: false}
      - {dependant: V_BUS02, actuator: LOAD24_ENABLE, type: above, value: 1.03, action: true}
```

Thresholds use logical units, here pu. LOAD24_ENABLE true connects the load. Use invert in a BOOL mapping when the native command polarity differs.

## Quality policy

```yaml
quality_policy:
  default: pass_through
  overrides:
    unsupplied: hold_last
    stale: fail_fast
    missing: skip_write
```

Actions are pass_through, hold_last, skip_write and fail_fast. Override conditions are good, initial, unsupplied, invalid, missing and stale. Missing/invalid takes precedence, then stale sample/transport, then source quality. Default pass-through preserves compatible finite data but does not fill unusable values with good zeros. Hold caches update only on successful writes; without history they skip.

## Backend-specific options

### EPANET

See [water configuration](configuration.html) for inp_controls, step_order, init_flag and also_set_setting. Explicit ports use node.ID.level/pressure/head/demand and link.ID.flow/status/setting; commands use link.ID.status. Units follow INP.

### pandapower

Solver options algorithm, max_iteration and tolerance_mva are passed to real runpp; omitted values use pandapower defaults, with numba=False. Unknown solver options fail.

| Model YAML field | Meaning |
| --- | --- |
| sn_mva | Declarative network base, default 1 MVA |
| buses[] | name, vn_kv and native create_bus parameters |
| ext_grids[] | name, bus alias, vm_pu and native external-grid parameters |
| lines[] | name, from_bus/to_bus aliases, length_km, r_ohm_per_km, x_ohm_per_km, c_nf_per_km, max_i_ka and native line parameters |
| loads[] | name, bus alias, p_mw, q_mvar and native load parameters |
| switches[] | name, bus, element alias, et=l line or b bus, closed and native switch parameters |
| load_profiles.LOAD | Nonempty nonnegative scaling list indexed by iteration, holding its last value afterwards |
| source / case | Public-model whitelist: pandapower_builtin / case33bw |
| benchmark_mode | original required for public source; physical overrides rejected |
| source_citation | Public model provenance |
| aliases.NAME | table=bus and paper_bus_number; source-name-based paper mapping |
| controlled_elements.NAME | table=load, bus_number, field=in_service; exactly one load must match |

Public-source and manually declared models follow separate loading paths. Native parameters are documented in [pandapower](https://pandapower.readthedocs.io/en/v3.2.1/elements.html).

Result ports are res_bus/res_line/res_load/res_ext_grid.ALIAS.COLUMN, e.g. supported vm_pu, p_mw, q_mvar, pl_mw and loading_percent columns. Derived MW ports are metrics.total.p_grid_mw/p_loss_mw/served_load_mw/unserved_load_mw. BOOL commands use switch.ALIAS.closed or load.ALIAS.in_service.

### Thermal box

Model fields are ambient_c, initial_c, loss_per_s (s⁻¹), heater_c_per_s (°C/s), heater_w (W) and input_dtype (bool, or float for the standalone analog API). Ports are box.temperature, box.heater_power and heater.enabled.

## Check and run

```bash
python -m src.run.config_info --config examples/power_feeder/config_v2.yaml
python -m src.physics.contract --config examples/power_feeder/config_v2.yaml
bash scripts/run_all.sh --config examples/power_feeder/config_v2.yaml --iterations 10 --logic-wait 0.3
```

config_info validates/prints configuration without a solver run. Contract actually runs the backend without networking. run_all executes the full loop. logic-wait is wall-clock PLC scan waiting, not physical sampling time. Communication timeout, synchronization and worker options belong to runner CLI settings; do not invent equivalent YAML keys. Continue with [Network](configuration-network.html) and [Attack Configuration](configuration-attacks.html).
