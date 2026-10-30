# Hydro-CPS-Sim Documentation

A co-simulation platform for water cyber-physical system security research.

Hydro-CPS-Sim connects hydraulic dynamics, PLC control, SCADA communications, and network simulation to run attack experiments, explore system behavior and develop security methods.

Source code: [WandeF/hydro-cps-sim](https://github.com/WandeF/hydro-cps-sim)

## Overview

- **Cross-layer co-simulation**: Link hydraulic models, control logic, and communication processes to study how cyber events affect the physical network.
- **Attack experiments**: Use MITM, DoS and PLC logic injection scenarios with configurable targets, parameters and active windows.
- **Configuration and execution**: Set up scenarios with YAML, run simulations through scripts and export logs and CSV results.
- **Research extensibility**: Investigate control, network, and hydraulic effects within a modular experiment framework.

To get started, follow [Installation](installation.html), then run the C-Town example in [Quick Start](quickstart.html).

## Explore the platform

Explore the [architecture and closed-loop workflow](architecture.html), [C-Town control dependencies](introduction.html), and [attack types and example configurations](experiments.html) to understand how network, control and hydraulics interact.

## Documentation

- Overview
  - [Introduction](introduction.html)
  - [Architecture](architecture.html)
- Get Started
  - [Installation](installation.html)
  - [Quick Start](quickstart.html)
- Experiments & Configuration
  - [Security Experiments](experiments.html)
  - [Configuration](configuration.html)
- Research & Community
  - [Publications & Citation](publications.html)
  - [Contributing & Feedback](contributing.html)

## Extended experiments

Use [UPSI](upsi.html) to connect physical models. Start with [Extension Overview](extensions.html), [adapter development](adapter-guide.html) and [power/thermal scenes](extended-examples.html). Consult [water configuration](configuration.html), [network](configuration-network.html) and [attack](configuration-attacks.html) fields.

For other models, see the added fields in [UPSI Configuration](upsi-configuration.html).
