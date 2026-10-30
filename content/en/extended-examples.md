# Power & Thermal Experiments

These examples show how to run power and thermal models with UPSI. Run them directly or change the models and control rules for your own experiments.

## Four-bus feeder

The 20 kV radial model has grid, feeder, control and flexible buses, a 0.2 MW essential load and a 0.8 MW switched load. PLC1 measures voltage and power; PLC2 receives V_CONTROL, disconnecting below 0.95 pu and reconnecting above 1.03 pu.

```bash
python -m pip install -r requirements-power.txt
python -m src.physics.contract --config examples/power_feeder/config_v2.yaml
PYTHON_BIN="$(command -v python)" bash scripts/run_power_experiments.sh
python scripts/check_power_results.py
```

| Configuration in examples/power_feeder | Purpose |
| --- | --- |
| config.yaml | Attack-free baseline |
| config_mitm_transparent.yaml | Same proxy/path, zero bias |
| config_mitm.yaml | −0.15 pu on SCADA→PLC2 PLC1_V_CONTROL FC16 writes, cycles 3–6 |
| config_v2.yaml | Explicit UPSI v2 baseline |

With these settings, the example shows transparent equality, the first actual coil deviation at cycle 3 and the first physical load-power change at 4: 0.8→0 MW. Disconnected bus voltage zero is explicitly marked unsupplied.

## IEEE33 benchmark

`examples/ieee33_bw/model.yaml` loads `pandapower.networks.case33bw()`, preserving public source voltage, impedances, loads and five open ties. The 12.66 kV model has 33 buses, 37 lines and 3.715 MW / 2.300 MVAr demand.

```bash
python scripts/ieee33_reference.py
python -m src.physics.contract --config examples/ieee33_bw/config_baseline.yaml
PYTHON_BIN="$(command -v python)" bash scripts/run_ieee33_experiments.sh
python scripts/check_ieee33_results.py
```

PLC1 measures Bus2, PLC2 monitors remote voltages, and PLC3 controls the existing Bus24 0.420 MW / 0.200 MVAr load using forwarded Bus2 voltage. The derived MITM subtracts 0.10 pu during cycles 20–40.

| Metric | Example result |
| --- | --- |
| Original minimum voltage | About 0.91309048 pu, Bus18 |
| Original line loss | About 202.677 kW |
| Baseline / transparent / MITM | 100 cycles each; transparent equals baseline |
| First command / physical difference | 20 / 21 |
| Bus24 load | 0.420→0 MW; bus stays energized |

PLC remote control, thresholds and attacks are derived platform experiments; [MATPOWER case33bw](https://matpower.org/docs/ref/matpower6.0/case33bw.html) supplies the benchmark network. Results are AC quasi-steady snapshots, without electromagnetic or frequency dynamics.

## Thermal-box plugin

The independent `examples/thermal_box/adapter.py` solves:

```text
dT/dt = -0.1 × (T - 18) + 0.8 × HEATER
heater power = 800 × HEATER W
```

Initial temperature is 19 °C and ambient temperature 18 °C. PLC1 provides temperature/power; PLC2 heats below 20 °C, stops above 22 °C and holds in between.

```bash
python -m src.physics.contract --config examples/thermal_box/config.yaml
PYTHON_BIN="$(command -v python)" bash scripts/run_all.sh \
  --config examples/thermal_box/config.yaml --logic-wait 0.3
```

In the ten-cycle real loop, heating stops at command 6, cooling first appears in physical snapshot 7, and temperature at 10 s is about 20.7874 °C. The backend uses analytical integration without EPANET or pandapower.

## Outputs and figures

| Scene | Output root | Plot command |
| --- | --- | --- |
| Four-bus | examples/power_feeder/output/ | python scripts/plot_example_results.py --example power_feeder |
| IEEE33 | output/ieee33_bw/ | python scripts/plot_ieee33_results.py |
| Thermal | examples/thermal_box/output/baseline/ | python scripts/plot_example_results.py --example thermal_box |

Install requirements-power-plots.txt for the shared plotting environment. The output directory contains physical states, PLC inputs/outputs and attack events. Follow the measurements, controller decisions and physical response to explore the experiment.

Detailed project records are docs/upsi-validation.md, docs/upsi-hardening-validation.md and docs/ieee33-validation.md. Follow [Add a Physical Simulator](adapter-guide.html) to implement another model or solver.
