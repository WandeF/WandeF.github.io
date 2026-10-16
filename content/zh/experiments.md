# 攻防实验

Hydro-CPS-Sim 的研究重点之一，是沿着**网络事件 → 数据状态 → 控制决策 → 水力响应**的链路分析攻击传播机制。

## 研究场景

| 攻击类型 | 网络或控制层变化 | 重点观测 |
| --- | --- | --- |
| MITM（中间人攻击） | 通信内容可能遭到修改 | 输入数据与真实物理状态的偏差、决策变化 |
| DoS（拒绝服务） | 通信延迟、丢包或超时 | 数据新鲜度、缓存使用、控制时机 |
| PLC 逻辑篡改 | 控制规则可能发生变化 | PLC 逻辑、执行器输出、物理轨迹 |

## 三类入口与传播机制

<figure>
<a href="../../assets/attack_cross_layer_propagation_paths.png" target="_blank" rel="noopener"><img src="../../assets/attack_cross_layer_propagation_paths.png" alt="MITM、DoS 和 PLC 逻辑注入经通信或控制规则影响泵阀并反馈至水力过程的路径" loading="lazy" width="4663" height="1993"></a>
<figcaption>三类攻击的跨层传播路径。箭头表示可能的通路；后续影响取决于通信状态、控制条件和水力反馈。</figcaption>
</figure>

- **MITM：输入内容改变。** 跨层分析场景修改 SCADA 下发至 PLC4 的 T7 数据，偏移后的输入可能提前越过 PU10 的关泵阈值。是否产生动作变化，还取决于当前状态与控制规则。
- **DoS：输入新鲜度下降。** 跨层分析场景在 PLC7 的采集路径引入拥塞；超时后 SCADA 可能保持旧 T4，再将旧值转发给 PLC5。只有关键判断轮次的输入差异改变控制条件，才会进一步影响 PU6/PU7 和水力反馈。
- **逻辑注入：有效规则改变。** 修改 PLC4 中 PU10 的 T7 关闭阈值，模拟已获得程序修改能力的情况。修改发生与首次控制偏离可能相隔多个轮次，需要等待过程状态触发新规则。

同一输入可能供多个控制规则使用，改写输入与仅改写某条阈值规则的后续效果可能不同。比较时应关注首次偏离、状态保持、重新开启和其他依赖该输入的执行器。

## 场景设置与配置选择

跨层分析场景运行 80 轮，攻击窗口为第 15–55 轮，DoS 目标为 PLC7 的采集路径。下表中的示例配置采用各自的目标与窗口：例如 DoS 预设指向 PLC2，攻击窗口为第 5–90 轮。运行前应选择所需场景，检查目标、轮数和控制依赖。

复现实验时，应使用同一版本的源码、完整 YAML、水网输入、控制映射和基线数据。历史字段 `PLC9_T7` 需映射到相应配置中的 T7 采集端，不能仅凭文件名判断目标。

## 示例配置

下表列出[版本 `2406aa6`](https://github.com/WandeF/hydro-cps-sim/tree/2406aa649738c585e635b3661d1b9431db73edb8)的示例配置，窗口单位为控制轮次。

| 配置文件 | 目标或用途 | 攻击轮次 |
| --- | --- | --- |
| [`config.yaml`](https://github.com/WandeF/hydro-cps-sim/blob/2406aa649738c585e635b3661d1b9431db73edb8/examples/c_town/config.yaml) | 无攻击基线 / Baseline | — |
| [`config_mitm_plc4.yaml`](https://github.com/WandeF/hydro-cps-sim/blob/2406aa649738c585e635b3661d1b9431db73edb8/examples/c_town/config_mitm_plc4.yaml) | PLC4 下发 / Downlink | 20–40 |
| [`config_mitm_plc9.yaml`](https://github.com/WandeF/hydro-cps-sim/blob/2406aa649738c585e635b3661d1b9431db73edb8/examples/c_town/config_mitm_plc9.yaml) | PLC8 T7 响应 / Response | 20–40 |
| [`config_mitm_composite_plc7_plc9.yaml`](https://github.com/WandeF/hydro-cps-sim/blob/2406aa649738c585e635b3661d1b9431db73edb8/examples/c_town/config_mitm_composite_plc7_plc9.yaml) | PLC6 T5 + PLC8 T7 | 20–40 / 30–50 |
| [`config_dos_plc2_single.yaml`](https://github.com/WandeF/hydro-cps-sim/blob/2406aa649738c585e635b3661d1b9431db73edb8/examples/c_town/config_dos_plc2_single.yaml) | PLC2 · 单源 / Single source | 5–90 |
| [`config_dos_plc2_three_bots.yaml`](https://github.com/WandeF/hydro-cps-sim/blob/2406aa649738c585e635b3661d1b9431db73edb8/examples/c_town/config_dos_plc2_three_bots.yaml) | PLC2 · 三源 / Three sources | 5–90 |
| [`config_openplc_logic_plc4.yaml`](https://github.com/WandeF/hydro-cps-sim/blob/2406aa649738c585e635b3661d1b9431db73edb8/examples/c_town/config_openplc_logic_plc4.yaml) | PLC4 · PU10 T7 阈值 / Threshold | 20–90 |

部分 MITM 文件名保留了 PLC7/PLC9 的历史编号，对应配置内的目标为 PLC6/PLC8。选择场景时，以 YAML 中的目标、变量映射和触发窗口为准。

安装完成后，指定配置启动实验：

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

## 如何组织跨层证据

建议同时记录四类首次事件：攻击首次生效 `t_A`、通信首次异常 `t_C`、执行器首次偏离基线 `t_U`、物理变量首次越过预设偏差阈值 `t_P`。逻辑注入不一定存在通信异常阶段，`t_C` 可记为不适用；窗口内未出现的事件应记为“未观察到”，不能补成末轮。

| 观测层 | 建议证据 | 解释时需要区分 |
| --- | --- | --- |
| 攻击 | 调度记录、修改帧与注入规则 | 配置的时间窗口与实际生效事件 |
| 通信与输入 | 超时、成功读取、SCADA 保持值与下发记录 | 通信失败、旧值保持与控制器实际收到的输入 |
| 控制 | 有效阈值、上一轮状态与泵阀输出 | 相对基线不同的动作、依据真实输入的名义动作及依据已下发输入应有的动作 |
| 物理 | 水位、压力、流量、实际 `sim_time` | 按轮次对齐与按相同引擎时刻对齐的偏差 |

离散控制可报告“不同于基线的执行器状态数 / 可比较状态总数”。水位、压力等连续量可报告 RMSE、平均绝对偏差和最大绝对偏差；每项指标应给出变量范围、观察窗口、单位、缺失处理及分母。通信 RTT 应说明是否只统计成功请求，重复运行应说明随机种子与聚合口径。

**时间对齐限制：** 水力引擎的内部事件步可能使同一轮次对应不同物理时刻。按轮次计算的峰值不能直接解释为严格同时刻的净攻击效应；必要时在实际引擎时间的共同观测点重新比较，并报告匹配样本数。墙钟通信频率也不等于 PLC 扫描频率。

**规模实验边界：** PLC 规模测试独立于 C-Town 攻击实验，不包含水力计算。通信与控制吞吐不能直接当作完整水网闭环的运行性能。

## 保存与复现实验

每次运行保存源码版本、完整配置、输入模型、启动命令、随机种子与结果目录。攻击运行应与相同初始状态和网络条件下的基线配对。汇总多次运行时，说明种子是否独立、指标如何聚合，以及失败或缺失记录的处理方式。
