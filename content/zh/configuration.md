# 配置说明

Hydro-CPS-Sim 使用 YAML 配置文件组织实验场景，默认配置为 `examples/c_town/config.yaml`。

## 配置文件

- 指定水网模型及其输入文件。
- 指向 OpenPLC、ns-3 等组件所在目录。
- 指定输出目录及仿真轮数。
- 保存水网控制、网络及实验设置。

安装程序会更新示例配置中的五个顶层路径字段：

| 路径键 | 用途 |
| --- | --- |
| `root_path` | 第三方依赖工作目录 |
| `openplc_path` | OpenPLC 源码或构建目录 |
| `ns3_path` | ns-3 源码或构建目录 |
| `inp_file` | EPANET 水网输入文件 |
| `output_path` | 实验结果输出目录 |

迁移环境或更换模型时，请更新这些路径，并确保 `output_path` 指向专用的实验输出目录。

## 创建场景

复制 `config.yaml` 作为新场景，修改其中的水网、控制或网络参数，然后通过 `--config` 指定配置文件运行。

## 传感器与控制映射

`plcs` 将水网中的传感器和执行器分配给各个 PLC。跨 PLC 的数据由 SCADA 转发。`network` 定义 PLC、SCADA 和攻击节点的网络端点、命名空间与连接关系。

## 仿真与控制参数

| 字段 | 当前基线值或作用 |
| --- | --- |
| `iterations` | 100；可由运行命令覆盖 |
| `noise_scale` | 0.0 |
| `time` | EPANET 总时长 86400 秒、水力步长 300 秒 |
| `physics` | `inp_controls: strip`、`step_order: next-run`、`init_flag: 0` |
| `plcs` | PLC1–PLC8 的传感器、执行器与控制规则 |
| `network` | ns-3 后端、实时调度、路由、节点、链路、LAN 和 TAP |
| `attacks.enabled` | 攻击配置的总开关 |
| `attacks.scenarios` | 场景类型、触发器、目标和类型特有参数 |

攻击类型包括 `modbus_mitm`、`udp_dos` 和 `openplc_logic_injection`。使用 `trigger.type: iteration_window` 设置轮次窗口，`start_iteration` 和 `end_iteration` 分别指定开始与结束轮次。各类型的节点、目标和规则可从[攻防实验](experiments.html)中的示例配置开始修改。
