# 网络配置

`network` 描述软件通信拓扑，和 INP 或电网中的物理拓扑分别维护。PLC、SCADA 和攻击端点必须有一致的名称、namespace、IP 和接入链路。

## 网络层结构

| 字段 | 类型／含义 |
| --- | --- |
| `backend` | 使用 ns3 |
| `topology_name` | 拓扑名称标识；输出程序名由生成/运行流程组织 |
| `scheduler` | realtime 启用 ns-3 RealtimeSimulatorImpl，用于真实进程通信 |
| `routing` | global 调用全局路由表填充 |
| `pcap` | bool，默认 false；启用对应链路的抓包 |
| `ascii_trace` | 预留字段；抓包使用 pcap |
| `nodes` | routers、switches、endpoints 三类节点列表 |
| `backbone_links` | 点到点主干链路列表 |
| `lans` | 含路由器、桥接交换机及端点的 LAN 列表 |
| `taps` | 显式端点接入说明；当前生成器主要读取 nodes.endpoints 的 tap/tap_mode，不能仅改 taps 期待切换实际接入 |
| `applications` | 记录预期通信；Modbus 流量由 SCADA 和 PLC 进程产生 |
| `attack_points` | 记录攻击路径；攻击目标和参数填写在 attacks 中 |

## 节点与端点

| 字段 | 含义 |
| --- | --- |
| `nodes.routers[].name` | 唯一路由器名，如 r0、r1 |
| `nodes.switches[].name` | 桥接交换机名，如 s1 |
| `nodes.endpoints[].name` | PLC1、scada、mitm 等端点名 |
| `role` | router/switch 元数据或端点角色 plc/scada/attacker；攻击解析也使用角色定位 |
| `endpoints[].namespace` | Linux 命名空间名 |
| `endpoints[].tap` | 主机 TAP 设备名，ns-3 TapBridge 使用同名设备 |
| `endpoints[].tap_mode` | use_bridge（默认）或 use_local；由 ns-3 端点读取的有效模式 |

Linux 接口名称受系统长度约束，生成器对部分派生 veth 名做截断。不要将不同端点配置为相同 namespace/TAP/IP。

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

这是端点片段；完整场景还需要 SCADA、主干和相应 LAN。

## 主干链路

`backbone_links[]` 的每项包含：

| 字段 | 含义 |
| --- | --- |
| `name` | 唯一链路名 |
| `type` | 示例 point_to_point；当前该列表按 PointToPointHelper 构建，不根据任意 type 自动选择模型 |
| `endpoints` | 两个已声明节点名 |
| `subnet` | CIDR 子网，如 10.0.1.0/24 |
| `data_rate` | ns-3 数据率字符串，如 100Mbps |
| `delay` | 非负时间字符串，支持 ns/us/ms/s，如 2ms |
| `mtu` | 链路 MTU 字节数，示例 1500 |
| `interfaces.<node>.ip` | 指定节点在此链路上的 CIDR 地址 |
| `interfaces.<node>.ifname` | 示例中的接口标签；ns-3 使用设备对象，Linux 端点实际 veth 名由生成器派生 |

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

## LAN 与地址

`lans[]` 使用 CSMA 和桥接交换机，要求一个路由器、一个交换机、至少一个端点。

| 字段 | 含义 |
| --- | --- |
| `name` / `type` | LAN 名及示例标识 csma；当前固定按 CSMA/Bridge 构建 |
| `members` | 同一 LAN 的节点名列表 |
| `subnet` / `data_rate` / `delay` / `mtu` | 子网、共享信道速率、延迟和 MTU |
| `interfaces.<router>.ip` | LAN 网关地址 |
| `interfaces.<endpoint>.ip` | 端点 CIDR 地址，运行配置从这里提取 PLC IP |
| `interfaces.<endpoint>.gateway` | namespace 的默认路由网关 |
| `interfaces.<node>.ifname` | 文档接口标签；不是生成器对实际 veth 名的覆盖字段 |

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

## 描述性字段

`taps[]` 常见字段为 `endpoint`、`tap_name`、`mode`、`host_namespace`；应与节点端点保持一致，但实际接入模式以 `nodes.endpoints[].tap_mode` 为准。`applications[]` 使用 `name`、`src`、`dst`、`protocol`、`dst_port` 描述预期通信。`attack_points[]` 使用 `name`、`type`、`targets` 描述路径。这些元数据不代替真实端点、程序或攻击配置。

## 修改后检查

名称必须在节点表、主干/LAN 成员、接口和攻击目标之间一致。IP 与网关要在对应子网内，主干与 LAN 避免重叠。新攻击者也需要真实 endpoint 和 LAN 地址。

当前生成器支持上述带宽与延迟字段；没有通用的 `packet_loss` YAML 开关，也没有根据 `applications` 自动生成业务流量的机制。需要随机丢包或其他 ns-3 模型时，先扩展生成器并检查实际生成的 C++，再配置实验。

使用 `python -m src.run.config_info --config ...` 查看命名空间等解析值；构建流程会生成 ns-3 C++ 与 Linux 网络脚本。完整字段起点见[配置说明](configuration.html)，攻击配置见[攻击配置](configuration-attacks.html)。
