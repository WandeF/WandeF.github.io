# Architecture

The platform follows a **closed-loop, multi-layer co-simulation** approach. Sensor measurements inform controller decisions; PLC outputs affect actuators; and actuator states are fed back into the hydraulic model. Network simulation mediates communication in the cyber layer.

## Layers

| Layer | Major components | Focus |
| --- | --- | --- |
| Physical | DHALSIM-epynet / EPANET | Tank levels, pressures, flows |
| Control | OpenPLC | PLC logic and actuator commands |
| Supervisory | SCADA communication | Data acquisition, commands, and caching |
| Network | ns-3 and Linux Network Namespace | Topology and communication impairment |
| Orchestration | Python scripts | Configuration, synchronization, execution, export |

## Conceptual simulation cycle

1. Obtain the current hydraulic state and relevant sensor values.
2. Exchange observations through the cyber/control communication path.
3. Run the PLC control logic and compute new actuator actions.
4. Apply the actions to the hydraulic model and advance the simulation.
5. Save the observable evidence for subsequent analysis.

The exact execution sequence is defined by the runtime implementation; the cycle above is a conceptual explanation.

## Source-code entry points

- `scripts/run_all.sh`: top-level example runner.
- `src/network/`: network and topology generation.
- `src/control/`: PLC generation, compilation, and execution.
- `src/runtime/`: closed-loop runtime orchestration.
- `src/io/`: experiment result export.

See the published [run_all.sh](https://github.com/WandeF/hydro-cps-sim/blob/2406aa649738c585e635b3661d1b9431db73edb8/scripts/run_all.sh).

## Planned illustrations

Before final release, add an overall architecture figure, a single-iteration sequence diagram, and attack propagation diagrams. Clearly differentiate data flow, control flow, network traffic, and attack influence.
