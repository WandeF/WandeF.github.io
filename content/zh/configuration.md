# 配置说明

Hydro-CPS-Sim 使用 YAML 配置文件组织实验场景，默认配置为 `examples/c_town/config.yaml`。

## 配置文件在运行中的作用

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

## 建议工作方式

不要直接修改唯一的基准配置；可以复制已验证的 `config.yaml`，然后在副本中改变实验参数。每次实验应记录所用源码提交、配置文件、启动命令与日志位置。

## 配置之间的约束

PLC 的传感器与执行器名称须与水网模型一致，跨 PLC 控制依赖须能通过 SCADA 转发。网络端点、命名空间和攻击目标应使用一致的标识。复制场景后，需同时检查模型、控制映射和网络拓扑。

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

攻击场景类型包括 `modbus_mitm`、`udp_dos`、`openplc_logic_injection`。`trigger.type: iteration_window` 使用 `start_iteration` / `end_iteration`；场景还需对应的攻击节点、拦截规则或逻辑注入设置，不应仅向基线追加一个开关。参见[攻防实验](experiments.html)中的实际配置。
