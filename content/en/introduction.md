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
