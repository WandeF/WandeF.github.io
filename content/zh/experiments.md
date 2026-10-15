# 攻防实验

Hydro-CPS-Sim 的研究重点之一，是沿着**网络事件 → 数据状态 → 控制决策 → 水力响应**的链路分析攻击传播机制。

## 研究场景

| 攻击类型 | 网络或控制层变化 | 重点观测 |
| --- | --- | --- |
| MITM（中间人攻击） | 通信内容可能遭到修改 | 输入数据与真实物理状态的偏差、决策变化 |
| DoS（拒绝服务） | 通信延迟、丢包或超时 | 数据新鲜度、缓存使用、控制时机 |
| PLC 逻辑篡改 | 控制规则可能发生变化 | PLC 逻辑、执行器输出、物理轨迹 |

## 源码中实际提供的配置

下表按 YAML 内容核对，窗口单位为控制轮次。仅核对了源码与配置，尚未完整运行这些仿真实验。

| 配置文件 | 目标或用途 | 攻击轮次 |
| --- | --- | --- |
| [`config.yaml`](https://github.com/WandeF/hydro-cps-sim/blob/2406aa649738c585e635b3661d1b9431db73edb8/examples/c_town/config.yaml) | 无攻击基线 / Baseline | — |
| [`config_mitm_plc4.yaml`](https://github.com/WandeF/hydro-cps-sim/blob/2406aa649738c585e635b3661d1b9431db73edb8/examples/c_town/config_mitm_plc4.yaml) | PLC4 下发 / Downlink | 20–40 |
| [`config_mitm_plc9.yaml`](https://github.com/WandeF/hydro-cps-sim/blob/2406aa649738c585e635b3661d1b9431db73edb8/examples/c_town/config_mitm_plc9.yaml) | PLC8 T7 响应 / Response | 20–40 |
| [`config_mitm_composite_plc7_plc9.yaml`](https://github.com/WandeF/hydro-cps-sim/blob/2406aa649738c585e635b3661d1b9431db73edb8/examples/c_town/config_mitm_composite_plc7_plc9.yaml) | PLC6 T5 + PLC8 T7 | 20–40 / 30–50 |
| [`config_dos_plc2_single.yaml`](https://github.com/WandeF/hydro-cps-sim/blob/2406aa649738c585e635b3661d1b9431db73edb8/examples/c_town/config_dos_plc2_single.yaml) | PLC2 · 单源 / Single source | 5–90 |
| [`config_dos_plc2_three_bots.yaml`](https://github.com/WandeF/hydro-cps-sim/blob/2406aa649738c585e635b3661d1b9431db73edb8/examples/c_town/config_dos_plc2_three_bots.yaml) | PLC2 · 三源 / Three sources | 5–90 |
| [`config_openplc_logic_plc4.yaml`](https://github.com/WandeF/hydro-cps-sim/blob/2406aa649738c585e635b3661d1b9431db73edb8/examples/c_town/config_openplc_logic_plc4.yaml) | PLC4 · PU10 T7 阈值 / Threshold | 20–90 |

文件名中的 PLC7/PLC9 是历史命名；当前配置中的实际目标为 PLC6/PLC8，应读取 YAML 内容确认。旧 `README_attack_mitm.md` 中的 `config_mitm.yaml` 和 `scripts/compare_attack_results.py` 在该版本中不存在。

安装成功后，可在仿真环境中选择实际配置（下例为源码核对命令，未在本次部署中运行）：

```bash
bash scripts/run_all.sh --config examples/c_town/config_mitm_plc4.yaml --logic-wait 0.3
```

先运行基线并保存结果，再运行攻击配置。导出目录 `reports/csv/` 包含 `physics.csv`、`actuator_state.csv`、`scada_observed_long.csv`、`scada_observed_wide.csv`、`scada_observed_key.csv`、`attack_schedule.csv`、`attack_events.csv`、`scada_timeout_events.csv` 和 `cycle_timing.csv`。攻击事件或超时记录并不等于已经产生物理偏离，需要与基线对齐分析。

## 推荐的对照流程

1. 固定水网、PLC 逻辑、仿真时长和必要的随机性设置。
2. 运行无攻击基线（baseline），保存每轮 CSV 与日志。
3. 仅改变准备考察的攻击变量，运行对照实验。
4. 对齐网络、PLC 和水力时间记录，分析关键轮次。
5. 汇总重复实验结果，而不仅是展示单次运行曲线。

## 跨层分析不应只看最终水位

同样的水箱水位偏差，可能来自错误传感数据、通信超时导致的陈旧数据，或者 PLC 控制规则改变。因此需要同时收集上游证据。对于 DoS，发生通信超时并不保证会导致控制偏离，实际传播还取决于控制所需数据是否及时更新。

## 发布前建议补充

- 攻击 YAML 示例与字段表（从实际代码中逐项核对）。
- 基线实验和各攻击实验的一键运行命令。
- 数据目录约定、时间戳含义及评价指标。
- 可复现实验图与必要的参数、随机种子说明。

> 实验数据、攻击成功率和论文结论应在论文定稿及验证后补入，避免把讨论中的结论误写成已经公开复现的结果。


源码核对：[hydro-cps-sim @ 2406aa6](https://github.com/WandeF/hydro-cps-sim/tree/2406aa649738c585e635b3661d1b9431db73edb8) · 2026-10-15.
