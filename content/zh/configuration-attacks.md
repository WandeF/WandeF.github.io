# 攻击配置

使用 `attacks` 设置 MITM、UDP DoS 或 PLC 逻辑注入。你可以选择攻击目标、调整参数，并设置开始和结束轮次。

## 总开关与生效窗口

| 字段 | 类型／默认 | 含义 |
| --- | --- | --- |
| `attacks.enabled` | bool；false | 攻击总开关 |
| `attacks.scenarios` | list | 攻击场景列表，可同时安排多个独立场景 |
| `scenarios[].name` | string | 唯一名称，用于进程和事件记录 |
| `enabled` | bool；true | 单场景开关 |
| `type` | string | modbus_mitm / udp_dos / openplc_logic_injection |
| `trigger.type` | iteration_window | 推荐轮次触发；还兼容 iteration / round / round_window |
| `trigger.start_iteration` | int；0 | 首个生效轮次，包含该轮 |
| `trigger.end_iteration` | int 或省略 | 最后生效轮次，包含该轮；省略持续到结束 |

旧别名 `schedule`、start_round/end_round、start/end 仍有兼容读取。新配置统一使用 trigger 与 iteration 字段。没有轮次触发器时使用启动/停止的默认策略，建议显式写窗口。

`trigger` 使用控制轮次；规则的 `window` 和 DoS 的 `start_after_sec` 使用进程启动后的墙钟秒数。这两类时钟与物理模型的 `sim_time` 分别记录。

## Modbus MITM

| 字段 | 含义 |
| --- | --- |
| `attacker.endpoint` | 网络中存在的攻击者端点 |
| `attacker.namespace` / `ip` | 说明性身份字段，应与网络一致；MITM 实际从 endpoint/LAN 解析，不以此覆盖 |
| `intercept.source` | 通常为 scada；当前实际固定定位 SCADA 命名空间，不据此选择任意客户端 |
| `intercept.targets` | 目标 PLC 名列表 |
| `intercept.protocol` | modbus_tcp 描述标识；当前实际执行 Modbus TCP 代理 |
| `intercept.port` | 原目标 Modbus TCP 端口，默认 502 |
| `intercept.listen_port_base` | 每目标代理监听端口起点；默认回退 15020；示例 15030 |
| `intercept.listen_ports.<PLC>` | 可选显式指定每目标监听端口 |
| `intercept.redirect` | 当前固定执行 iptables_output_dnat，不根据该字符串切换其他重定向机制 |
| `rules[].name` | 规则名；省略时生成 rule_N |
| `rules[].target` | 对应目标 PLC，可用于筛选同场景的规则 |
| `rules[].variable` | 目标实际生成 ST 中的 REAL `%MD` 变量，如 PLC8_T7 |
| `rules[].direction` | response（默认）或 request |
| `rules[].function_codes` | 支持 3/4/16 的列表或单个整数；response 默认 3/4，request 默认 16 |
| `rules[].operation` | set/replace；add/offset/bias；multiply/scale |
| `rules[].value` | 数值或比例，默认 0；按目标寄存器值的逻辑单位 |
| `rules[].window.start_after_sec` | 相对代理启动的延迟秒数，默认 0 |
| `rules[].window.duration_sec` | 可选持续秒数；未设则不加此时限 |
| `rules[].max_events` | 可选每条规则最多匹配次数 |

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

上例对应 C-Town 的 PLC4 下行水位攻击：将转发的 T7 水位设为 5.2。修改其他目标时，一起更新 PLC 名、端点地址和寄存器变量。要运行透明代理对照，可以使用 add 并将 value 设为 0。

## UDP DoS

| 字段 | 含义 |
| --- | --- |
| `attacker.endpoint` / `namespace` / `ip` | 实际发送端点及身份 |
| `target.endpoint` / `namespace` / `ip` | 目标端点及身份，配置地址需要与场景匹配 |
| `target.protocol` | 当前 udp |
| `target.port` | UDP 目的端口；默认 502，与同号 TCP Modbus 端口不是同一传输协议 |
| `traffic.mode` | 当前仅 cbr，默认 cbr |
| `traffic.rate` | 速率字符串，默认 500kbps，示例 120Mbps |
| `traffic.packet_size` | UDP 负载字节数，默认 512，示例 1400 |
| `traffic.start_after_sec` | 攻击进程启动后延迟，默认 0 |

```yaml
type: udp_dos
trigger: {type: iteration_window, start_iteration: 5, end_iteration: 90}
attacker: {endpoint: ns_bot1, namespace: ns-bot1, ip: 192.168.255.201}
target: {endpoint: PLC2, namespace: ns-plc2, ip: 192.168.2.1, protocol: udp, port: 502}
traffic: {mode: cbr, rate: 120Mbps, packet_size: 1400, start_after_sec: 0.0}
```

这是原水网攻击场景条目的片段；完整网络见 `examples/c_town/config_dos_plc2_single.yaml`。多个发送者使用多个场景条目及独立 endpoint。流量能否改变控制取决于实际路径、瓶颈、超时与控制规则，应检查真实事件和缓存状态。

## PLC 逻辑注入

目标必须是存在的 PLC，`target.namespace` 与 network endpoint 保持一致。

| 字段 | 含义 |
| --- | --- |
| `target.endpoint` / `namespace` | 目标 PLC 与实际命名空间 |
| `injection.mode` | threshold_shift / invert_condition / force_actuator |
| `injection.restore_on_stop` | 默认 true；窗口结束时恢复原程序与进程状态 |
| `injection.rule.actuator` | threshold_shift/invert_condition 的执行器 |
| `injection.rule.dependant` | 要匹配的传感器依赖 |
| `injection.rule.type` | below/above，定位原规则 |
| `injection.rule.original_value` | threshold_shift 的原阈值；帮助定位原规则 |
| `injection.rule.injected_value` | threshold_shift 的替换阈值 |
| `injection.rule.value` | invert_condition 的匹配阈值，可回退 original_value |
| `injection.actuator` | force_actuator 的逻辑执行器 |
| `injection.state` | force_actuator 的强制 BOOL/兼容状态；还兼容 value |

```yaml
type: openplc_logic_injection
target: {endpoint: PLC4, namespace: ns-plc4}
injection:
  mode: threshold_shift
  rule: {actuator: PU10, dependant: T7, type: above, original_value: 4.8, injected_value: 999.0}
  restore_on_stop: true
```

该路径修改、编译并重启实际 OpenPLC 程序，不是在物理层替换输出。规则匹配失败应排查传感器拥有者、阈值和生成 ST。

## 查看结果

先查看 attack_schedule.csv 和 attack_events.csv，了解攻击何时开始、修改了哪些数据；再比较 SCADA 观测、PLC 输出和水力结果。通信超时可从 scada_timeout_events.csv 查找。

MITM 下的客户端写入确认与目标 PLC 实际收到的值可能不同，可以结合代理记录和寄存器读回查看。电网等扩展实验的数据质量设置见 [UPSI 配置](upsi-configuration.html)。

完整运行方式见[攻防实验](experiments.html)，基础字段见[配置说明](configuration.html)，网络端点见[网络配置](configuration-network.html)。
