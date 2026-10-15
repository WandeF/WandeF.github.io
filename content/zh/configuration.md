# 配置说明

当前公开运行器使用 YAML 配置文件组织实验场景，默认入口为 `examples/c_town/config.yaml`。

## 配置文件在运行中的作用

- 指定水网模型及其输入文件。
- 指向 OpenPLC、ns-3 等组件所在目录。
- 指定输出目录及仿真轮数。
- 保存水网控制、网络及实验设置。

安装脚本会处理示例 YAML 中的若干路径键，源码中明确出现了：

| 路径键 | 用途 |
| --- | --- |
| `root_path` | 第三方依赖工作目录 |
| `openplc_path` | OpenPLC 源码或构建目录 |
| `ns3_path` | ns-3 源码或构建目录 |
| `inp_file` | EPANET 水网输入文件 |
| `output_path` | 实验结果输出目录 |

这些字段可在 [install.sh](https://github.com/WandeF/hydro-cps-sim/blob/2406aa649738c585e635b3661d1b9431db73edb8/install.sh) 中核对。其他 YAML 字段需要针对当前版本的真实配置文件补全，暂不在此猜测。

## 建议工作方式

不要直接修改唯一的基准配置；可以复制已验证的 `config.yaml`，然后在副本中改变实验参数。每次实验应记录所用源码提交、配置文件、启动命令与日志位置。

## 待完善内容

- 按模块给出完整 YAML 字段字典。
- 附一个可运行的 baseline 配置和一个已验证攻击配置。
- 解释配置与网络拓扑、PLC 映射、物理模型间的约束。


源码核对：[hydro-cps-sim @ 2406aa6](https://github.com/WandeF/hydro-cps-sim/tree/2406aa649738c585e635b3661d1b9431db73edb8) · 2026-10-15.

## 已核对的其他字段

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
