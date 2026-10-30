# Architecture

Hydro-CPS-Sim connects physical processes, PLC control, SCADA, networking and attacks. Measurements reach controllers, controller outputs operate equipment, and equipment states affect the physical process.

## Platform overview

<figure><img src="../../assets/hydro_cps_sim_architecture_upsi.svg" alt="Original Hydro-CPS-Sim architecture with UPSI added to the physical layer"><figcaption>UPSI connects physical simulators to the control loop.</figcaption></figure>

| Component | Purpose |
| --- | --- |
| Scenario configuration | Physical model, control rules, network and attacks |
| Orchestrator | Generate programs, prepare networking, start modules and collect results |
| Physical layer | Water levels, pressures and flows, or another model's states |
| UPSI | Connect model measurements and commands with shared variable, unit and time handling |
| Control and SCADA | OpenPLC rules, data collection and cross-PLC forwarding |
| Network | Namespaces, TAP/veth and ns-3 connections |
| Attacks | MITM, DoS and PLC logic injection |
| Synchronization and recording | Coordinate modules and save physical, communication, control and attack data |

## Physical models and UPSI

The water scene uses EPANET. For other systems, choose pandapower, the thermal box or your own adapter through UPSI. Models keep their own equations and solvers while providing measurements and accepting control inputs.

Adapters describe ports, units and stepping. The platform uses that information without requiring a new control/network workflow for every solver. See [Extended Experiments](extensions.html).

## Closed-loop workflow

1. Read configuration/model and generate PLC programs and network topology.
2. Start modules and prepare initial measurements and commands.
3. Write local PLC measurements; let SCADA collect and forward remote dependencies.
4. Run OpenPLC rules and read output commands.
5. Apply commands in the physical model and calculate the next state.
6. Save results and continue.

The PLC Adapter connects to OpenPLC through local Modbus. Remote SCADA–PLC traffic uses the configured ns-3 network, where delay, congestion and attacks affect communication.

## Code structure

| Path | Contents |
| --- | --- |
| scripts/run_all.sh | Complete experiment entry |
| src/control/ | Generate, compile and start PLC programs |
| src/physics/ | Physical interfaces and adapters |
| src/plc/, scada/, comm/ | Collection, forwarding and Modbus |
| src/network/ | Namespaces and ns-3 topology |
| src/attack/ | Attack scheduling and execution |
| src/runtime/, sync/ | Loop and synchronization |
| src/io/ | Recording and result export |

Start with [Quick Start](quickstart.html), use [Configuration](configuration.html) for water scenes and [Add a Physical Simulator](adapter-guide.html) for another model.
