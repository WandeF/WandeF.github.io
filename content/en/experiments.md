# Security Experiments

A core research goal is to trace how cyber events propagate through **communication → information freshness/integrity → controller decisions → hydraulic behavior**.

## Research scenarios

| Scenario | Primary disturbance | Evidence of interest |
| --- | --- | --- |
| Man-in-the-Middle (MITM) | Altered communication values | Input corruption, PLC decisions, physical deviations |
| Denial of Service (DoS) | Delay, packet loss, or timeout | Data freshness, cached values, control timing |
| PLC logic manipulation | Modified control rules | Logic integrity, actuator outputs, physical trajectories |

## Three entry points and propagation mechanisms

<figure>
<a href="../../assets/attack_cross_layer_propagation_paths.png" target="_blank" rel="noopener"><img src="../../assets/attack_cross_layer_propagation_paths.png" alt="MITM, DoS and PLC logic injection paths through communication or control rules to actuators and hydraulic feedback" loading="lazy" width="4663" height="1993"></a>
<figcaption>Propagation paths from the manuscript draft. Arrows indicate possible paths, not guaranteed downstream effects in every run. Click to view the original.</figcaption>
</figure>

- **MITM changes input content.** The manuscript scenario modifies T7 data sent from SCADA to PLC4. A biased input can cross the PU10 pump-off threshold earlier; actual action changes depend on process state and rules.
- **DoS reduces input freshness.** Congestion on the PLC7 acquisition path can cause timeouts, leaving SCADA to retain an older T4 observation and forward it to PLC5. Propagation to PU6/PU7 and hydraulics requires the stale input to change a relevant control decision.
- **Logic injection changes effective rules.** Modifying the T7 pump-off threshold for PU10 at PLC4 models an attacker with program modification capability. Injection and first control deviation need not coincide: process state must trigger the modified rule.

An input may be shared by several rules. Changing that input and changing only one threshold can produce different subsequent behavior. Compare first deviation, state retention, reopening and other actuators consuming the same input.

## Manuscript scenarios versus public presets

The manuscript describes 80-iteration runs, an attack window of iterations 15–55 and a DoS scenario targeting the PLC7 acquisition path. The source table below describes public presets at the reviewed commit: for example, the DoS files target PLC2 during iterations 5–90. These settings are not interchangeable.

This page explains the research method without presenting unpublished manuscript settings as verified one-command reproductions. Reproduction requires the exact commit, complete YAML, water model, control mapping, attack window and archived data. Historical fields such as `PLC9_T7` also require mapping to the current T7 acquisition endpoint.

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


## Organizing cross-layer evidence

Record four possible first events: attack activation `t_A`, communication anomaly `t_C`, actuator deviation from baseline `t_U`, and physical deviation crossing a predefined threshold `t_P`. Logic injection may have no communication-anomaly stage, making `t_C` inapplicable. Mark events absent from the observation window as unobserved rather than assigning them to the last iteration.

| Layer | Suggested evidence | Distinctions to preserve |
| --- | --- | --- |
| Attack | Scheduling, modified frames and injected rules | Configured window versus actual activation |
| Communication and input | Timeouts, successful reads, held SCADA values and downlink records | Failed communication, stale values and inputs actually delivered to a controller |
| Control | Effective thresholds, previous state and actuator outputs | Baseline mismatch, nominal decisions from true inputs and expected execution from delivered inputs |
| Physical | Levels, pressures, flows and actual `sim_time` | Iteration-aligned versus equal-engine-time deviations |

For discrete control, report mismatched actuator states divided by comparable states. For continuous variables, consider RMSE, mean absolute deviation and peak absolute deviation. Define variables, windows, units, missing-data treatment and denominators. State whether RTT includes only successful requests and how repeated runs use seeds and aggregation.

**Time alignment:** Internal hydraulic events can make the same iteration correspond to different physical times. An iteration-aligned peak is not automatically a simultaneous net attack effect. When needed, compare common actual engine-time observations and report the number of matches. Wall-clock communication update frequency is also distinct from PLC scan frequency.

**Scalability scope:** The manuscript's PLC scalability tests are separate from C-Town attack experiments and exclude hydraulic computation. Communication and control throughput does not establish the performance of a full water-network loop.

## Documentation to add before release

- Runnable attack configurations and a field-by-field reference.
- Validated commands for both baseline and attack scenarios.
- Output-directory conventions and metric definitions.
- Reproducible plots, seeds, and versioned configurations.

> Experimental results and publication claims should be added only after verification and paper finalization.


Source review: [hydro-cps-sim @ 2406aa6](https://github.com/WandeF/hydro-cps-sim/tree/2406aa649738c585e635b3661d1b9431db73edb8) · 2026-10-15.
