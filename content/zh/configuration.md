# 配置说明

Hydro-CPS-Sim 使用 YAML 文件设置水网、控制器、网络和攻击。你可以复制一个示例，修改需要的参数，再通过 `--config` 运行。

本页以 `examples/c_town/config.yaml` 为例介绍水网场景。接入其他物理仿真器时，再查看[扩展实验中的 UPSI 配置](upsi-configuration.html)。

## 配置文件的结构

一个水网场景由以下部分组成：

| 部分 | 用途 |
| --- | --- |
| 模型和组件路径 | 指定 INP、OpenPLC、ns-3 与结果目录 |
| `iterations`、`time` | 设置运行轮次和水力步长 |
| `initial_tank_values`、`actuators` | 设置初始水位和泵阀状态 |
| `physics` | 设置 EPANET 的控制和步进方式 |
| `plcs` | 分配传感器、执行器和控制规则 |
| `network` | 描述通信节点、链路和地址 |
| `attacks` | 选择攻击及其生效时间 |

下面的片段展示主要字段。完整配置还包括 PLC 列表和网络拓扑，可以直接从 C-Town 示例复制。

```yaml
root_path: /path/to/workspace
inp_file: ctown_map.inp
output_path: output/baseline
openplc_path: ../../../OpenPLC_v3
ns3_path: ../../../ns-3-dev-git
iterations: 100

initial_tank_values:
  T1: '3'
  T2: '.5'

actuators:
  - {name: PU1, initial_state: closed}
  - {name: PU2, initial_state: open}

physics:
  inp_controls: strip
  step_order: next-run
  init_flag: 0

time:
  - duration: [EN_DURATION, 86400]
  - hydraulic_timestep: [EN_HYDSTEP, 300]
```

## 路径与运行设置

| 字段 | 含义 |
| --- | --- |
| `root_path` | 安装时使用的工作目录 |
| `inp_file` | EPANET 水网输入文件，包含管网、设备、需水模式等数据 |
| `output_path` | 本次实验的结果目录 |
| `openplc_path` | OpenPLC 根目录 |
| `ns3_path` | ns-3 根目录 |
| `iterations` | 运行轮次上限，示例为 100；可用 `--iterations` 覆盖 |
| `network_topology_type` | 示例中的拓扑标识 complex；具体连接写在 network 中 |

相对路径通常从 YAML 所在目录开始计算。更换目录或复制场景后，先检查 INP、OpenPLC 和 ns-3 的位置。不同实验使用不同的 `output_path`，方便比较结果。

`noise_scale` 和 `log_level` 是示例保留字段，当前运行入口没有把它们作为通用噪声和日志设置使用。

## 水力时间与初始状态

`time` 中每项由 EPANET 参数名和数值组成。`hydraulic_timestep: [EN_HYDSTEP, 300]` 表示名义水力步长为 300 s。示例保留 `duration`；当前运行器会结合步长和轮数设置水力计算范围。

`initial_tank_values` 按水箱名称设置初始水位，单位与 INP 一致。C-Town 使用 T1–T7。`actuators` 中的名称应与 INP 的泵、阀门链接一致。

| 执行器字段 | 含义 |
| --- | --- |
| `name` | 泵或阀门名称，如 PU1、V2 |
| `initial_state` | 初始 open 或 closed；open 对应启用/开启，closed 对应关闭 |

没有自动控制规则的设备会保持初始状态，除非实验中的其他控制操作改变它。水力结果中的 `sim_time` 可用于画物理时间曲线，运行日志中的轮次用于查找对应控制过程。

## EPANET 设置

| `physics` 字段 | 默认值 | 用法 |
| --- | --- | --- |
| `inp_controls` | strip | 运行时移除 INP 副本中的 CONTROLS/RULES，让 OpenPLC 执行控制；keep 保留 INP 内部控制 |
| `step_order` | next-run | 选择 EPANET 步进调用顺序，支持 next-run、run-next |
| `init_flag` | 0 | 传给水力初始化接口的标志 |
| `also_set_setting` | false | 控制链接时同时写入 setting，通常保留默认值 |

这些设置也可放在 `physics.epynet` 中；存在该子节时从子节读取。日常修改模型、阈值或攻击时，通常不需要改变它们。

## PLC 与传感器

`plcs` 将测量和执行器分配给各 PLC。每个测量由一个 PLC 采集，其他 PLC 需要这个测量时由 SCADA 转发。

| 字段 | 含义 |
| --- | --- |
| `name` | PLC 名，如 PLC1；应与网络端点一致 |
| `sensors` | 本地采集的传感器名称列表 |
| `actuators` | 本地控制的泵阀名称列表 |
| `controls` | 按顺序执行的控制规则 |

水箱名 T1、T2 等表示水位，J285 等节点名表示压力，PU1F、V2F 等以 F 结尾的名称表示相应链接流量。测量单位由 INP 决定。

例如，PLC2 采集 T1，PLC1 使用 T1 控制 PU1：

```yaml
plcs:
  - name: PLC1
    sensors: [PU1F]
    actuators: [PU1]
    controls:
      - {dependant: T1, actuator: PU1, type: below, value: 4.0, action: open}
      - {dependant: T1, actuator: PU1, type: above, value: 6.3, action: closed}
  - name: PLC2
    sensors: [T1]
    actuators: []
    controls: []
```

这是控制映射片段，使用时与执行器初值和完整网络一起配置。SCADA 名称通过 `scada.name` 设置；各进程的 namespace 和 IP 写在 network 端点和 LAN 中。

## 控制规则

| 字段 | 含义 |
| --- | --- |
| `dependant` | 参与判断的测量名 |
| `actuator` | 被控制的泵阀 |
| `type` | below 表示低于阈值，above 表示高于阈值 |
| `value` | 阈值，使用对应测量的单位 |
| `action` | 满足条件时执行 open 或 closed |

上例中，T1 低于 4.0 时开启 PU1，高于 6.3 时关闭；两者之间保持状态。比较为严格的小于和大于，等于阈值时不触发。多个规则同时满足时，后面的赋值可能改变前面的结果，因此应避免相互冲突的规则。

## 网络与攻击

网络配置见[网络配置](configuration-network.html)。从示例修改时，让 PLC、SCADA 和攻击节点在端点、LAN 地址和攻击目标中使用相同名称。

攻击通过 `attacks.enabled` 开启，通过 `attacks.scenarios` 设置类型、目标与轮次窗口。MITM、DoS 和 PLC 逻辑注入的字段见[攻击配置](configuration-attacks.html)，运行示例见[攻防实验](experiments.html)。

## 保存和查看结果

结果写入 `output_path`。常用文件包括水力数据 `physics.csv`、泵阀状态 `actuator_state.csv`、SCADA 观测以及攻击事件。`reporting.key_variables` 可以选择关键观测列，例如 `PLC2.PLC2_T1`；没有设置时使用水网的默认选择。

```bash
bash scripts/run_all.sh --config examples/c_town/config.yaml --iterations 100 --logic-wait 0.3
```

`--logic-wait` 是每轮等待 PLC 扫描的秒数，和水力步长分别设置。添加电网、热模型或自己的求解器时，继续阅读[扩展实验](extensions.html)。
