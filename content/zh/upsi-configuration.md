# UPSI 配置

接入其他物理模型时，可以在原有场景配置中选择后端、声明信号，并设置采样间隔。下面介绍 UPSI 增加的配置写法。

## 填写配置

配置文件继续使用 YAML，在顶层添加 `schema_version: 2`，选择显式信号配置。模型、信号和时间参数写在 `physics` 中。

使用空格缩进，列表使用 `-`，布尔值写成 `true`/`false`，无量纲单位写成字符串 `'1'`。PyYAML 的隐式类型解析会把未加引号的 `on`/`off` 解释为布尔值；需要字符串时写成 `'on'`/`'off'`。避免重复键和含糊的数字字符串。

填写字段时使用下表中的名称；未识别的字段可能被忽略。运行前可以使用本页末尾的命令检查配置。语法参考 [YAML](https://yaml.org/spec/1.2.2/) 和 [PyYAML](https://pyyaml.org/wiki/PyYAMLDocumentation)。

## 整体结构

```yaml
schema_version: 2
output_path: output/baseline
openplc_path: ../../../OpenPLC_v3
ns3_path: ../../../ns-3-dev-git
iterations: 10
physics: {}       # 后端、模型、时间、信号映射
actuators: []     # 逻辑执行器及初始状态
plcs: []          # 本地信号、执行器、控制规则
scada: {name: scada}
network: {}       # 完整节点、链路、LAN、端点设置
attacks: {enabled: false, scenarios: []}
reporting: {key_variables: []}
```

这是结构示意，空的 `physics`、`plcs` 和 `network` 不能作为完整实验运行。可运行起点为 `examples/power_feeder/config_v2.yaml`、`examples/ieee33_bw/config_baseline.yaml` 和 `examples/thermal_box/config.yaml`。网络和攻击的完整字典分别在[网络配置](configuration-network.html)与[攻击配置](configuration-attacks.html)。

## 与原配置的关系

UPSI 沿用原有的 output_path、组件路径、plcs、network 和 attacks。需要更换物理模型时，再增加下面的字段：

| 字段 | 用法 |
| --- | --- |
| `schema_version: 2` | 使用显式物理信号配置 |
| `physics.backend` | 选择 EPANET、pandapower 或自己的适配器 |
| `physics.model.path` | 指定物理模型文件 |
| `physics.plugins` | 注册独立适配器 |
| `physics.timing` | 设置物理采样间隔 |
| `physics.signals` | 连接逻辑信号与物理端口 |
| `signals` | 可选的顶层信号类型、方向、单位和范围 |
| `actuators[].initial_state` | 按声明的命令类型填写，例如 BOOL 使用 true/false |
| `quality_policy` | 选择失电、旧数据或缺失数据的处理方法 |
| `initial_state` | 可选的初始输出类型声明；起始物理值由模型初始化产生 |

路径、PLC 规则、网络与攻击的基本写法见[配置说明](configuration.html)、[网络配置](configuration-network.html)和[攻击配置](configuration-attacks.html)。

## physics 通用字段

| 字段 | 类型／默认 | 含义 |
| --- | --- | --- |
| `backend` | string；v2 必填 | `dhalsim_epynet`、`pandapower` 或已声明的插件名；旧配置省略时使用水网；`epanet`/`epynet` 为别名 |
| `model` | mapping；v2 必填 | 模型声明，内置后端与恒温箱使用 `path`；插件可自定义模型参数 |
| `model.path` | path | 物理模型文件路径；相对 YAML 目录 |
| `plugins.<name>.factory` | `module:Class` | 适配器工厂，和 entry_point 二选一 |
| `plugins.<name>.entry_point` | string | 已安装 `hydro_cps.physics` 分组的命名入口 |
| `plugins.<name>.dependency` | module string；可选 | 选中后端时预检导入的依赖模块 |
| `init_style` | `current` / `dhalsim` | v2 默认 current；v1 水网默认 dhalsim；后者仅适用于声明兼容初始化的水网后端 |
| `timing.mode` | `fixed_step` | 当前单后端采样调度模式；不是求解器内部步进模式 |
| `timing.step_seconds` | finite number > 0；v2 必填 | 请求采样间隔，秒；EPANET 要求 1 s 的整数倍 |
| `timing.measurement_max_age_s` | number ≥ 0；默认 0 | 允许的测量年龄；非零时后端必须声明异步测量能力 |
| `timing.tolerance.absolute_s` | number ≥ 0 | 物理时间比较的绝对容差；默认 min(1e-9, step/8)，不能超过 step/4 |
| `timing.tolerance.relative` | number ≥ 0 | 相对容差；默认 8 倍浮点 epsilon，上限 1e-6；最终容差仍受步长限制 |
| `signals.observations` | mapping | 逻辑测量到原生输出端口的映射 |
| `signals.commands` | mapping | 逻辑执行器到原生输入端口的映射，必须完整且不重复 |
| `quality_policy` | mapping；可选 | 与顶层同名策略作用相同；重复声明时必须一致 |
| `model_file`、`timestep` | v1 兼容字段 | 分别对应模型路径和采样间隔；timestep 与 timing.step_seconds 同时出现时必须一致 |
| `sensors`、`actuators` | v1 电网兼容字段 | 按 `table`、`element`、`column` 声明结果读取和 BOOL 控制，归一化为 signals；可带 missing / invert |

`init_style: current` 从已求解的 time-zero 快照开始；旧水网 `dhalsim` 保留第 0 行零值和第 1 行配置初值，再进入历史控制轮次。因此旧 C-Town 的 100 轮上限对应 99 次控制周期，不能直接与 current 场景的快照数量混比。

后端 `describe().timing` 的 `target`/`event_step` 是后端能力，与配置中的 `fixed_step` 不同。控制轮次连续递增，物理请求使用上一实际返回时间；内部事件可以使一次物理推进短于采样间隔。

## 信号映射字段

下表用于 `physics.signals.observations.<name>` 和 `commands.<name>`：

| 字段 | 类型／默认 | 含义 |
| --- | --- | --- |
| `port` | string；必填 | 后端声明的原生端口，方向必须正确 |
| `dtype` | float/int/bool/str；v2 必填 | 可在顶层 signals 中补充；必须和原生类型一致 |
| `unit` | string；默认原生单位 | 逻辑单位，不能用未引号的数字 1 |
| `minimum`、`maximum` | finite number；可选 | 数值范围；BOOL/字符串不能设置数值边界 |
| `scale` | finite number ≠ 0；默认 1 | `logical = native * scale + offset` 的比例；命令逆转换 |
| `offset` | finite number；默认 0 | 同上；非恒等仿射转换仅支持 float |
| `invert` | bool；默认 false | BOOL 极性反转，仅用于布尔信号 |
| `missing` | 后端选项；默认 error | pandapower 支持 `zero_if_unsupplied`，只用于母线电压；不是通用缺失值补零 |
| `unit_context.density_kg_m3` | number > 0 | 水柱压力换算的显式密度 |
| `unit_context.gravity_m_s2` | number > 0 | 水柱压力换算的显式重力加速度 |
| `calibration_reason` | 非空字符串 | 同单位非恒等标定的原因；会写入信号 schema |

顶层 `signals.<name>` 可声明 `direction`、`dtype`、`unit`、`minimum`、`maximum`；方向和映射一致，重复元数据不得冲突。命令只能映射一次到同一原生输入，所有原生输入都必须覆盖。

```yaml
physics:
  signals:
    observations:
      P_GRID_KW:
        port: metrics.total.p_grid_mw
        dtype: float
        unit: kW
        scale: 1000
    commands:
      LOAD24_ENABLE:
        port: load.LOAD_BUS24.in_service
        dtype: bool
        unit: '1'
```

单位目录区分 `MW` 与 `Mvar`、电压与功率；`pu` 仅允许恒等单位转换，不自动猜基值。温度 `degC → K` 需显式 `offset: 273.15`。接口说明见 [UPSI](upsi.html)。

## 配置控制器

PLC 的传感器、执行器和阈值规则继续使用原来的写法。不同之处是：测量名来自 `physics.signals.observations`，命令名来自 `physics.signals.commands`，初始值要与声明类型一致。

```yaml
actuators:
  - {name: LOAD24_ENABLE, initial_state: true}
plcs:
  - {name: PLC1, sensors: [V_BUS02], actuators: [], controls: []}
  - name: PLC3
    sensors: [V_BUS24, P_LOAD24]
    actuators: [LOAD24_ENABLE]
    controls:
      - {dependant: V_BUS02, actuator: LOAD24_ENABLE, type: below, value: 0.95, action: false}
      - {dependant: V_BUS02, actuator: LOAD24_ENABLE, type: above, value: 1.03, action: true}
```

阈值使用逻辑信号的单位。这个示例中电压单位为 pu，`LOAD24_ENABLE: true` 表示投入负荷。改变命令极性时可在映射中使用 `invert`。

## 质量策略

```yaml
quality_policy:
  default: pass_through
  overrides:
    unsupplied: hold_last
    stale: fail_fast
    missing: skip_write
```

`default` 和每个 override 的动作可选 `pass_through`、`hold_last`、`skip_write`、`fail_fast`。`overrides` 的条件键为 `good`、`initial`、`unsupplied`、`invalid`、`missing`、`stale`。缺失/无效优先，其次是样本或网络陈旧，再按物理质量判断。默认透传保留兼容轨迹，但不会把不可用/非有限数据补成正常零值。保持缓存仅在 Modbus 写入成功后更新；无历史值时跳过。

## 各后端专用选项

### EPANET

原有 inp_controls、step_order、init_flag 和 also_set_setting 的用法见[水网配置](configuration.html)。显式水力端口可写为 `node.<id>.level/pressure/head/demand` 和 `link.<id>.flow/status/setting`；命令使用 `link.<id>.status`。工程单位来自 INP。

### pandapower

`solver.algorithm`（例如 nr）、`solver.max_iteration`、`solver.tolerance_mva` 传给真实 `runpp()`；未设置时使用 pandapower 默认值，固定 `numba=False`。solver 中未知选项会报错。

模型 YAML 有两种形式：

| 字段 | 含义 |
| --- | --- |
| `sn_mva` | 声明式模型系统基准，默认 1 MVA |
| `buses[]` | name、vn_kv，及 create_bus 支持的参数 |
| `ext_grids[]` | name、bus 别名、vm_pu，及 create_ext_grid 参数 |
| `lines[]` | name、from_bus/to_bus 别名、length_km、r_ohm_per_km、x_ohm_per_km、c_nf_per_km、max_i_ka，及原生线路参数 |
| `loads[]` | name、bus 别名、p_mw、q_mvar，及原生负荷参数 |
| `switches[]` | name、bus、element 别名、et（l 线路 / b 母线）、closed，及原生开关参数 |
| `load_profiles.<load>` | 非空非负 scaling 列表；按迭代索引取值，超出后保持末项 |
| `source` / `case` | 公开模型入口固定 `pandapower_builtin` / `case33bw` |
| `benchmark_mode` | 公开模型入口要求 original，不允许任意物理参数覆盖 |
| `source_citation` | 公开模型出处 |
| `aliases.<name>` | `table: bus`、`paper_bus_number`，按源名称映射论文节点 |
| `controlled_elements.<name>` | `table: load`、`bus_number`、`field: in_service`，要求该母线负荷唯一 |

公开模型保留原始数据；与手动声明式模型分支分别解析，不混写。具体原生建模参数见 [pandapower 文档](https://pandapower.readthedocs.io/en/v3.2.1/elements.html)。

读取端口为 `res_bus/res_line/res_load/res_ext_grid.<alias>.<column>`，例如 vm_pu、p_mw、q_mvar、pl_mw、loading_percent 等已支持列。派生 MW 端口为 `metrics.total.p_grid_mw/p_loss_mw/served_load_mw/unserved_load_mw`。命令端口为 `switch.<alias>.closed` 或 `load.<alias>.in_service`，均为 BOOL。

### 恒温箱

模型字段为 `ambient_c`（环境温度）、`initial_c`（初温）、`loss_per_s`（散热系数，s⁻¹）、`heater_c_per_s`（加热温升率，°C/s）、`heater_w`（额定功率 W）和 `input_dtype`（bool 或独立 API 的 float）。原生端口为 `box.temperature`、`box.heater_power` 和 `heater.enabled`。

## 验证与运行覆盖项

```bash
python -m src.run.config_info --config examples/power_feeder/config_v2.yaml
python -m src.physics.contract --config examples/power_feeder/config_v2.yaml
bash scripts/run_all.sh --config examples/power_feeder/config_v2.yaml --iterations 10 --logic-wait 0.3
```

`config_info` 校验并打印解析值，不启动求解器；contract 真实调用所选后端，不启动网络；run_all 才运行完整控制网络。`--logic-wait` 是等待 PLC 扫描的墙钟秒数，不是模型采样步长。通信超时、同步等待和工作线程参数通过运行器 CLI 设置。网络和攻击字段继续见[网络配置](configuration-network.html)、[攻击配置](configuration-attacks.html)。
