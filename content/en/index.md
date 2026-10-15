# Hydro-CPS-Sim Documentation

A co-simulation platform for water cyber-physical system security research.

Hydro-CPS-Sim connects hydraulic dynamics, PLC control, SCADA communications, and network simulation to support attack-impact evaluation, cross-layer analysis, and defense research.

Source code: [WandeF/hydro-cps-sim](https://github.com/WandeF/hydro-cps-sim)

## Overview

- **Cross-layer co-simulation**: Link hydraulic models, control logic, and communication processes to study how cyber events affect the physical network.
- **Attack-impact evaluation**: Support research into MITM, DoS, and PLC logic modification scenarios. Runnable cases depend on the published code and configurations.
- **Reproducible workflows**: Organize experiments through configuration files and scripts, and export logs and CSV results for analysis.
- **Research extensibility**: Investigate control, network, and hydraulic effects within a modular experiment framework.

The key research question is: **How do cyberattacks propagate through sensing, control decisions, and actuation into physical water-system behavior?**

A typical research path: attacks and disturbances → network communication (ns-3 / Namespace) → SCADA / PLC → hydraulics (DHALSIM-epynet) → log and CSV analysis.

> **Documentation status:** This is the deployed working draft of the research software documentation. Unverified configuration keys, publication details, and experiment claims are deliberately left as follow-up work.

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
