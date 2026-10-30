# Add a Physical Simulator

Wrap the solver as a `PhysicsBackend`, describe native ports and register it in the scene. Keep the adapter beside an example or in a separate Python package.

## Model and port design

Identify model files, initial conditions, writable inputs, readable outputs, engineering units, physical-time API and failure states. The thermal example declares:

| Port | Direction | Type | Unit |
| --- | --- | --- | --- |
| box.temperature | output | float | degC |
| box.heater_power | output | float | W |
| heater.enabled | input | bool | 1 |

EPANET uses node/link ports; pandapower uses result table, alias and column ports. Independent plugins can choose stable domain-specific names.

## Implement the lifecycle

`examples/thermal_box/adapter.py` is a complete analytical solver adapter. A new class has this structure; the initialization and solve methods must be connected to a real solver:

```python
from src.physics.base import PhysicsBackend
from src.physics.types import SignalSpec, StepResult

class PlantBackend(PhysicsBackend):
    def __init__(self, config):
        self.config = config

    def describe(self):
        return {'signals': {
            'plant.measurement': SignalSpec('plant.measurement', 'output', 'float', 'K'),
            'plant.enabled': SignalSpec('plant.enabled', 'input', 'bool', '1'),
        }, 'timing': 'target', 'model_kind': 'your_physical_model'}

    def initialize(self):
        raise NotImplementedError('Connect the real solver initialization')

    def advance(self, until_s, inputs):
        raise NotImplementedError('Connect the real solver step')

    def close(self):
        pass
```

This template produces no simulated results. Acquire solver resources in initialize, apply `config.initial_inputs`, and return `StepResult(actual_time_s, outputs, applied_inputs, diagnostics=...)`. Repeated initialization must not reset the model. Close safely after partial initialization and repeated calls.

Check input types, convergence, finite outputs and actual reached time. Do not relabel cached values as newly solved observations. Declare event_step for internal-event early returns, or target for reaching each request.

## Register the plugin

```yaml
physics:
  backend: my_plant
  plugins:
    my_plant:
      factory: my_package.adapter:PlantBackend
      # dependency: my_solver_package
```

An installed package can instead declare:

```toml
[project.entry-points."hydro_cps.physics"]
my_plant = "my_package.adapter:PlantBackend"
```

Select it with `entry_point: my_plant` instead of factory. Exactly one source is required. Install the package into the Python used by PYTHON_BIN. Built-in names and aliases cannot be replaced.

## Connect logical signals and PLCs

Merge this physical/control fragment into a scene containing complete network and runtime paths:

```yaml
schema_version: 2
physics:
  backend: my_plant
  plugins:
    my_plant: {factory: 'my_package.adapter:PlantBackend'}
  model: {path: model.yaml}
  timing: {mode: fixed_step, step_seconds: 1.0}
  signals:
    observations:
      TEMPERATURE: {port: plant.measurement, dtype: float, unit: K}
    commands:
      HEATER: {port: plant.enabled, dtype: bool, unit: '1'}
actuators:
  - {name: HEATER, initial_state: false}
plcs:
  - name: PLC1
    sensors: [TEMPERATURE]
    actuators: [HEATER]
    controls:
      - {dependant: TEMPERATURE, actuator: HEATER, type: below, value: 293.15, action: true}
      - {dependant: TEMPERATURE, actuator: HEATER, type: above, value: 295.15, action: false}
```

Ports, types and units must match describe. Remote dependencies follow sensor ownership and are forwarded by SCADA; adapters need no Modbus code.

## Run the adapter

```bash
python -m src.physics.contract --config examples/thermal_box/config.yaml
```

Replace the scene path for a new backend. The checker actually initializes and advances three times, validates complete data, applied inputs and physical time, and attempts cleanup. Missing declared optional dependencies are skipped; loading/model/solve errors fail.

Standalone applications can pass `registry = configure_plugins(raw)` into `BackendConfig.registry`, create the backend with `create_backend(name, config)` and reuse `exercise_backend(backend, initial_inputs, step_seconds)`.

## Run the real loop

```bash
PYTHON_BIN="$(command -v python)" bash scripts/run_all.sh \
  --config examples/thermal_box/config.yaml --logic-wait 0.3
```

Verify the existing example first, then substitute the new scene. A full run needs real OpenPLC, ns-3 and namespace privileges; the standalone contract check does not.

Inspect physical_state/signals CSV, actual PLC coils, raw SCADA data and signal_quality. Confirm command k is applied in the next returned physical snapshot. Cover known trajectories, repeated initialize/close, unit/type errors, failed solves, incorrect time/timestamps and cleanup.

## Troubleshooting

| Symptom | Check |
| --- | --- |
| Plugin not found | Importable package/module, same Python environment, factory or entry-point name |
| Port/direction error | Describe metadata versus scene mappings |
| Unit error | Explicit scale/offset and compatible dimensions |
| Missing inputs | Complete unique native-input mappings and initial commands |
| Stalled/backward time | Actual solver time and internal-event progress |
| New data after failed solve | Raise an error and use session-controlled publication |
| Native concurrency issue | Registry isolation does not make a solver thread-safe |
