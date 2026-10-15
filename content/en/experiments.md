# Security Experiments

A core research goal is to trace how cyber events propagate through **communication → information freshness/integrity → controller decisions → hydraulic behavior**.

## Research scenarios

| Scenario | Primary disturbance | Evidence of interest |
| --- | --- | --- |
| Man-in-the-Middle (MITM) | Altered communication values | Input corruption, PLC decisions, physical deviations |
| Denial of Service (DoS) | Delay, packet loss, or timeout | Data freshness, cached values, control timing |
| PLC logic manipulation | Modified control rules | Logic integrity, actuator outputs, physical trajectories |

## Published configuration files

The table reflects actual YAML contents. Windows are control iterations. These presets were reviewed in source but were not executed as full simulations for this website.

| Configuration | Target or purpose | Attack iterations |
| --- | --- | --- |
| [`config.yaml`](https://github.com/WandeF/hydro-cps-sim/blob/2406aa649738c585e635b3661d1b9431db73edb8/examples/c_town/config.yaml) | 无攻击基线 / Baseline | — |
| [`config_mitm_plc4.yaml`](https://github.com/WandeF/hydro-cps-sim/blob/2406aa649738c585e635b3661d1b9431db73edb8/examples/c_town/config_mitm_plc4.yaml) | PLC4 下发 / Downlink | 20–40 |
| [`config_mitm_plc9.yaml`](https://github.com/WandeF/hydro-cps-sim/blob/2406aa649738c585e635b3661d1b9431db73edb8/examples/c_town/config_mitm_plc9.yaml) | PLC8 T7 响应 / Response | 20–40 |
| [`config_mitm_composite_plc7_plc9.yaml`](https://github.com/WandeF/hydro-cps-sim/blob/2406aa649738c585e635b3661d1b9431db73edb8/examples/c_town/config_mitm_composite_plc7_plc9.yaml) | PLC6 T5 + PLC8 T7 | 20–40 / 30–50 |
| [`config_dos_plc2_single.yaml`](https://github.com/WandeF/hydro-cps-sim/blob/2406aa649738c585e635b3661d1b9431db73edb8/examples/c_town/config_dos_plc2_single.yaml) | PLC2 · 单源 / Single source | 5–90 |
| [`config_dos_plc2_three_bots.yaml`](https://github.com/WandeF/hydro-cps-sim/blob/2406aa649738c585e635b3661d1b9431db73edb8/examples/c_town/config_dos_plc2_three_bots.yaml) | PLC2 · 三源 / Three sources | 5–90 |
| [`config_openplc_logic_plc4.yaml`](https://github.com/WandeF/hydro-cps-sim/blob/2406aa649738c585e635b3661d1b9431db73edb8/examples/c_town/config_openplc_logic_plc4.yaml) | PLC4 · PU10 T7 阈值 / Threshold | 20–90 |

PLC7/PLC9 in filenames are historical names; the current targets are PLC6/PLC8 as defined by YAML. The older `README_attack_mitm.md` refers to missing `config_mitm.yaml` and `scripts/compare_attack_results.py`.

After installation, select an existing configuration in the simulation environment (source-checked command, not executed during this deployment):

```bash
bash scripts/run_all.sh --config examples/c_town/config_mitm_plc4.yaml --logic-wait 0.3
```

Run and preserve a baseline before the attack run. Exports under `reports/csv/` include `physics.csv`, `actuator_state.csv`, `scada_observed_long.csv`, `scada_observed_wide.csv`, `scada_observed_key.csv`, `attack_schedule.csv`, `attack_events.csv`, `scada_timeout_events.csv`, and `cycle_timing.csv`. Attack events or timeouts alone do not establish physical deviation; compare aligned baseline evidence.

## Suggested methodology

1. Fix hydraulic scenarios, control programs, time horizon, and random settings where applicable.
2. Record attack-free baseline results including CSV files and runtime logs.
3. Change only the attack variables under evaluation.
4. Align network-level, control-level, and hydraulic observations.
5. Analyze repeated runs, not just a single simulation trace.

## Why cross-layer evidence matters

The same tank-level deviation could reflect false sensor values, a stale observation after a timeout, or an unauthorized PLC logic change. Evidence from upstream layers is essential for attribution. In a DoS scenario, communication failure alone does not guarantee a control deviation; propagation depends in part on whether fresh data is required at the relevant control iteration.

## Documentation to add before release

- Runnable attack configurations and a field-by-field reference.
- Validated commands for both baseline and attack scenarios.
- Output-directory conventions and metric definitions.
- Reproducible plots, seeds, and versioned configurations.

> Experimental results and publication claims should be added only after verification and paper finalization.


Source review: [hydro-cps-sim @ 2406aa6](https://github.com/WandeF/hydro-cps-sim/tree/2406aa649738c585e635b3661d1b9431db73edb8) · 2026-10-15.
