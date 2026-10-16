# Introduction

Hydro-CPS-Sim is a research co-simulation platform for **water distribution cyber-physical systems**. It is designed for security experimentation, cross-layer impact assessment, and defense-method evaluation.

## Motivation

Hydraulic simulators capture the evolution of pressures, flows, and tank levels, while network simulators characterize topology, delays, and packet loss. Studying cyber-physical incidents requires combining both aspects with an actual control loop.

## Main components

| Component | Role |
| --- | --- |
| DHALSIM-epynet / EPANET | Hydraulic simulation and physical-state updates |
| OpenPLC | PLC control-program execution |
| ns-3 | Communication-network simulation |
| Linux Network Namespace | Isolated Linux network environments |
| Python orchestration modules | Configuration, process coordination, state exchange, and output |

## Example research questions

- At what control iteration does manipulated input data change a PLC decision?
- Does packet loss or timeout necessarily cause an actuator deviation?
- Can similar physical anomalies arise from different cyber or control causes?
- How can network traces, controller behavior, and physical trajectories be aligned?

## Scope

This is a research simulation tool, not software for operating a real water utility. Availability of specific attack configurations and parameter names must be checked against the corresponding repository version. Simulation results should not be interpreted directly as quantitative risk assessments for production systems.

Repository: <https://github.com/WandeF/hydro-cps-sim>

## Research goals and method

The project asks four connected questions: how attacks enter control inputs or rules; how different entry points create distinct propagation paths; when communication degradation becomes control deviation; and how layered observations and baseline comparisons explain physical consequences.

Experiments intervene at designated protocol, network or control interfaces while retaining hydraulic feedback and recording intermediate states. Analysis examines both where anomalies first appear and where propagation stops, without assuming that every cyberattack must cause a physical deviation.

## C-Town example and control dependencies

<figure>
<a href="../../assets/ctown_water_topology.png" target="_blank" rel="noopener"><img src="../../assets/ctown_water_topology.png" alt="C-Town network, PLC1 to PLC8 regions, cross-region tank-level dependencies and attack entry points" loading="lazy" width="6240" height="6675"></a>
<figcaption>C-Town network, control regions and cross-region dependencies. Attack annotations show the cross-layer analysis scenarios; see <a href="experiments.html">Experiments</a> for other presets and parameters. Click to view the original.</figcaption>
</figure>

| Measurement source | Control dependency forwarded through SCADA |
| --- | --- |
| T1 at PLC2 | PU1 and PU2 at PLC1 |
| T2 and T3 at PLC3 | Local V2, PU4 and PU5 |
| T5 at PLC6 | PU8 at PLC4 |
| T7 at PLC8 | PU10 and PU11 at PLC4 |
| T4 at PLC7 | PU6 and PU7 at PLC5 |

Local T6 at PLC4 is primarily monitored. Regions represent logical ownership, not necessarily a shared physical cabinet. Cross-region dependencies allow measurement integrity and freshness to influence actuator decisions in another region.

See [architecture](architecture.html) and [experiments](experiments.html). When using historical experiment archives, map PLC identifiers to the sensor assignments in the corresponding configuration.
