# Network Configuration

The network section describes communication topology separately from the INP or electrical model. PLC, SCADA and attacker endpoint names, namespaces, IPs and access paths must agree.

## Top-level network fields

| Field | Meaning |
| --- | --- |
| backend | Use ns3 |
| topology_name | Topology identifier; generated program naming follows the build workflow |
| scheduler | realtime enables RealtimeSimulatorImpl for real process traffic |
| routing | global populates routing tables |
| pcap | BOOL, false by default; enables link captures |
| ascii_trace | Reserved field; use pcap for packet capture |
| nodes | routers, switches and endpoints lists |
| backbone_links | Point-to-point backbone links |
| lans | Router/bridge/endpoint LANs |
| taps | Descriptive endpoint access list; active generation reads endpoint tap/tap_mode |
| applications | Expected communication; SCADA and PLC processes produce Modbus traffic |
| attack_points | Attack paths; set targets and parameters under attacks |

## Nodes and endpoints

| Field | Meaning |
| --- | --- |
| nodes.routers[].name | Unique router name |
| nodes.switches[].name | Bridge-switch name |
| nodes.endpoints[].name | PLC1, scada, mitm etc. |
| role | Router/switch metadata or endpoint plc/scada/attacker role, also used by attack lookup |
| endpoints[].namespace | Linux network namespace |
| endpoints[].tap | TAP name used by TapBridge |
| endpoints[].tap_mode | use_bridge by default or use_local; effective ns-3 endpoint mode |

Linux interface names have length constraints; generated veth names may be shortened. Keep namespace, TAP and IP assignments unique.

```yaml
network:
  backend: ns3
  scheduler: realtime
  routing: global
  pcap: false
  nodes:
    routers: [{name: r1}]
    switches: [{name: s1}]
    endpoints:
      - {name: PLC1, role: plc, namespace: ns-demo-plc1, tap: tap-demo-plc1, tap_mode: use_bridge}
```

This is a fragment; a complete scene also needs SCADA and connected backbone/LAN definitions.

## Backbone links

| Field in backbone_links[] | Meaning |
| --- | --- |
| name | Unique link name |
| type | point_to_point metadata; the current list is built using PointToPointHelper rather than arbitrary type dispatch |
| endpoints | Exactly two declared nodes |
| subnet | CIDR network |
| data_rate | ns-3 rate string such as 100Mbps |
| delay | Nonnegative ns/us/ms/s string, such as 2ms |
| mtu | Bytes, commonly 1500 |
| interfaces.NODE.ip | Exact CIDR interface address |
| interfaces.NODE.ifname | Example label; ns-3 uses device objects, and Linux endpoint veth names are generated |

```yaml
backbone_links:
  - name: r0-r1
    type: point_to_point
    endpoints: [r0, r1]
    subnet: 10.0.1.0/24
    data_rate: 100Mbps
    delay: 2ms
    mtu: 1500
    interfaces:
      r0: {ip: 10.0.1.1/24}
      r1: {ip: 10.0.1.2/24}
```

## LANs and addresses

Each CSMA/bridge LAN requires one router, one bridge switch and at least one endpoint.

| Field in lans[] | Meaning |
| --- | --- |
| name / type | LAN name and csma label; current construction uses CSMA/Bridge |
| members | Declared nodes in the LAN |
| subnet / data_rate / delay / mtu | Network, shared-medium rate, delay and MTU |
| interfaces.ROUTER.ip | Router/gateway address |
| interfaces.ENDPOINT.ip | Endpoint CIDR address; runtime extracts PLC IPs here |
| interfaces.ENDPOINT.gateway | Namespace default route |
| interfaces.NODE.ifname | Descriptive label, not an actual generated-veth-name override |

```yaml
lans:
  - name: plc1_lan
    type: csma
    members: [r1, s1, PLC1]
    subnet: 192.168.1.0/24
    data_rate: 100Mbps
    delay: 100us
    mtu: 1500
    interfaces:
      r1: {ip: 192.168.1.254/24}
      PLC1: {ip: 192.168.1.1/24, gateway: 192.168.1.254}
```

## Descriptive fields

`taps[]` commonly contains endpoint, tap_name, mode and host_namespace. Keep it consistent, but actual endpoint mode follows nodes.endpoints[].tap_mode. applications[] contains name, src, dst, protocol and dst_port. attack_points[] contains name, type and targets. Metadata does not replace real endpoints, applications or attacks.

## Checking a changed network

Match node names across members, interfaces and attacks. Keep addresses/gateways in their subnet and avoid overlapping link/LAN subnets. Add a real endpoint and LAN address for every attacker.

The current generator supports bandwidth and delay as listed; there is no generic packet_loss YAML switch or automatic application traffic from applications. Additional ns-3 error models require generator implementation and inspection of generated C++.

Use `python -m src.run.config_info --config ...` to inspect parsed settings. The build produces ns-3 C++ and Linux setup scripts. Continue with [Configuration](configuration.html) and [Attacks](configuration-attacks.html).
