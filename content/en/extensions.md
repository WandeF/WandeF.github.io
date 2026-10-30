# Extended Experiments

Hydro-CPS-Sim can connect power systems, thermal systems and custom physical models as well as C-Town. UPSI gives these models a common interface while PLCs, SCADA, networking and attacks follow the same workflow.

## Add a physical model

Start with an example or write an adapter for another solver:

- [Learn about UPSI](upsi.html): exchange measurements and control inputs.
- [Write an adapter](adapter-guide.html): initialize, step and read results.
- [Configure UPSI](upsi-configuration.html): select the backend and connect variables, units and time.
- [Run power and thermal examples](extended-examples.html): try complete scenes.

## What you can customize

| Goal | Change |
| --- | --- |
| Use another water network | INP and inp_file; see [Configuration](configuration.html) |
| Use another physical model | physics.backend and physics.model.path |
| Select other measurements | physics.signals.observations |
| Change commands or units | physics.signals.commands and signal mappings |
| Adjust control thresholds | plcs.controls |
| Change network or attacks | network and attacks |
| Add a simulator | Implement an adapter and register it in physics.plugins |

## Run your experiment

Check model initial values and units, then run an attack-free scene. Add transparent-proxy and attack configurations when you want to compare attack behavior with the baseline.

Each scene currently selects one physical backend. The model calculates system states; the platform passes them to controllers and returns the resulting commands.
