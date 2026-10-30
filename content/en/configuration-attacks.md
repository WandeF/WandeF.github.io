# Attack Configuration

Use attacks to configure MITM, UDP DoS or PLC logic injection. Choose the target, adjust attack parameters and set the active iterations.

## Switches and windows

| Field | Meaning |
| --- | --- |
| attacks.enabled | Master BOOL, false by default |
| attacks.scenarios | List of independently scheduled scenarios |
| scenarios[].name | Unique process/event identifier |
| enabled | Per-scenario BOOL, true by default |
| type | modbus_mitm / udp_dos / openplc_logic_injection |
| trigger.type | Prefer iteration_window; iteration/round/round_window aliases exist |
| trigger.start_iteration | Inclusive first cycle, default 0 |
| trigger.end_iteration | Inclusive last cycle; omitted means no end limit |

Legacy schedule, start_round/end_round and start/end aliases remain readable. Use explicit trigger/iteration fields in new scenes. Without an iteration trigger, startup/stop defaults apply.

Trigger windows use controller iterations. Rule window and traffic start_after_sec use wall-clock seconds after process startup. Both differ from physical sim_time.

## Modbus MITM fields

| Field | Meaning |
| --- | --- |
| attacker.endpoint | Existing attacker node |
| attacker.namespace / ip | Descriptive identity; MITM resolves actual identity from endpoint/LAN rather than overriding it here |
| intercept.source | Usually scada; actual launcher resolves the SCADA namespace rather than selecting arbitrary clients here |
| intercept.targets | Target PLC list |
| intercept.protocol | Descriptive modbus_tcp label; current execution uses Modbus TCP |
| intercept.port | Original target port, default 502 |
| intercept.listen_port_base | Per-target listening base, fallback 15020; examples 15030 |
| intercept.listen_ports.PLC | Optional explicit per-target listen port |
| intercept.redirect | Execution is fixed to iptables_output_dnat, not dynamically switched by this label |
| rules[].name | Rule name; generated rule_N if omitted |
| rules[].target | Target PLC filter |
| rules[].variable | Actual generated REAL %MD variable on the target |
| rules[].direction | response by default or request |
| rules[].function_codes | Supported 3/4/16 list or integer; response defaults 3/4, request 16 |
| rules[].operation | set/replace, add/offset/bias or multiply/scale |
| rules[].value | Numeric replacement/offset/factor, default 0, using logical register units |
| rules[].window.start_after_sec | Delay from proxy startup, default 0 |
| rules[].window.duration_sec | Optional duration limit |
| rules[].max_events | Optional maximum matches per rule |

```yaml
attacks:
  enabled: true
  scenarios:
    - name: ctown_t7_bias
      enabled: true
      type: modbus_mitm
      trigger: {type: iteration_window, start_iteration: 20, end_iteration: 40}
      attacker: {endpoint: mitm, namespace: ns-attacker, ip: 192.168.4.100}
      intercept:
        source: scada
        targets: [PLC4]
        protocol: modbus_tcp
        port: 502
        listen_port_base: 15030
        redirect: iptables_output_dnat
      rules:
        - name: tank_level_downlink
          target: PLC4
          variable: PLC8_T7
          direction: request
          function_codes: [16]
          operation: set
          value: 5.2
          window: {start_after_sec: 0.0}
```

This C-Town fragment sets the T7 level forwarded to PLC4 to 5.2. Change names, addresses and register variables together for another target. For a transparent comparison, use add with value 0.

## UDP DoS fields

| Field | Meaning |
| --- | --- |
| attacker.endpoint / namespace / ip | Actual sender identity |
| target.endpoint / namespace / ip | Existing target identity |
| target.protocol | udp |
| target.port | UDP destination, default 502; distinct from same-number TCP Modbus |
| traffic.mode | cbr only, default cbr |
| traffic.rate | Rate string, default 500kbps; examples 120Mbps |
| traffic.packet_size | Payload bytes, default 512; examples 1400 |
| traffic.start_after_sec | Delay from attack-process startup, default 0 |

```yaml
type: udp_dos
trigger: {type: iteration_window, start_iteration: 5, end_iteration: 90}
attacker: {endpoint: ns_bot1, namespace: ns-bot1, ip: 192.168.255.201}
target: {endpoint: PLC2, namespace: ns-plc2, ip: 192.168.2.1, protocol: udp, port: 502}
traffic: {mode: cbr, rate: 120Mbps, packet_size: 1400, start_after_sec: 0.0}
```

This is a water-scene entry fragment; examples/c_town/config_dos_plc2_single.yaml contains the topology. Multiple senders use multiple entries/endpoints. Effects depend on actual bottlenecks, timeout/cache behavior and control thresholds.

## PLC logic injection

The target must be an existing PLC and its namespace must match the endpoint.

| Field | Meaning |
| --- | --- |
| target.endpoint / namespace | Actual PLC target |
| injection.mode | threshold_shift / invert_condition / force_actuator |
| injection.restore_on_stop | true by default; restore original program/runtime at window end |
| injection.rule.actuator | Rule actuator for threshold_shift/invert_condition |
| injection.rule.dependant | Rule observation |
| injection.rule.type | below/above rule match |
| injection.rule.original_value | Original threshold for threshold_shift matching |
| injection.rule.injected_value | Replacement threshold |
| injection.rule.value | invert_condition match threshold, falling back to original_value |
| injection.actuator | force_actuator output |
| injection.state | Forced BOOL/compatible state; value alias exists |

```yaml
type: openplc_logic_injection
target: {endpoint: PLC4, namespace: ns-plc4}
injection:
  mode: threshold_shift
  rule: {actuator: PU10, dependant: T7, type: above, original_value: 4.8, injected_value: 999.0}
  restore_on_stop: true
```

The path changes, compiles and restarts the real OpenPLC program. It does not substitute physical outputs. If matching fails, inspect ownership, thresholds and generated ST.

## Read the results

Use attack_schedule.csv and attack_events.csv to see when attacks ran and what data changed. Compare SCADA observations, PLC outputs and hydraulic states. Communication timeouts appear in scada_timeout_events.csv.

A client-confirmed MITM write can differ from the value received by the target PLC; inspect proxy records and register readback together. Data-quality settings for extended scenes are in [UPSI Configuration](upsi-configuration.html).

See [Experiments](experiments.html), [Configuration](configuration.html) and [Network Configuration](configuration-network.html).
