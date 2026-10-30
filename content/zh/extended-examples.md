# 电网与恒温箱实验

下面的示例展示如何使用 UPSI 运行电网和恒温箱。你可以直接运行示例，也可以修改模型和控制规则开展自己的实验。

## 四母线电网

模型为 20 kV 径向馈线，包含 grid、feeder、control、flexible 四个母线，0.2 MW 基础负荷和 0.8 MW 可切负荷。PLC1 采集电压和功率；PLC2 接收远程 `V_CONTROL`，低于 0.95 pu 断开负荷支路，高于 1.03 pu 恢复。

```bash
python -m pip install -r requirements-power.txt
python -m src.physics.contract --config examples/power_feeder/config_v2.yaml
PYTHON_BIN="$(command -v python)" bash scripts/run_power_experiments.sh
python scripts/check_power_results.py
```

| 配置 | 用途 |
| --- | --- |
| `examples/power_feeder/config.yaml` | 无攻击基线 |
| `config_mitm_transparent.yaml` | 相同代理与路径，偏移量为 0 |
| `config_mitm.yaml` | 3–6 轮，对 SCADA→PLC2 的 `PLC1_V_CONTROL` FC16 请求减去 0.15 pu |
| `config_v2.yaml` | 显式 UPSI v2 格式的基线 |

在示例设置中，透明代理与基线的物理曲线一致；MITM 第 3 轮改变实际线圈，第 4 轮可切负荷功率从 0.8 MW 降为 0。失电母线电压的 0 值带 `unsupplied` 质量标记。

## IEEE 33 节点标准电网

`examples/ieee33_bw/model.yaml` 使用 `pandapower.networks.case33bw()`，保持公开 Baran–Wu 模型的源电压、阻抗、原始负荷及五条停运联络线。模型为 12.66 kV、33 母线、37 线路，总负荷 3.715 MW / 2.300 MVAr。

```bash
python scripts/ieee33_reference.py
python -m src.physics.contract --config examples/ieee33_bw/config_baseline.yaml
PYTHON_BIN="$(command -v python)" bash scripts/run_ieee33_experiments.sh
python scripts/check_ieee33_results.py
```

PLC1 采集 Bus2 电压，PLC2 监测远端电压，PLC3 接收 Bus2 远程测量并控制 Bus24 原有的 0.420 MW / 0.200 MVAr 负荷。20–40 轮对下行电压减去 0.10 pu，触发实验阈值。

| 项目 | 示例结果 |
| --- | --- |
| 原始最低电压 | 约 0.91309048 pu，Bus18 |
| 原始线损 | 约 202.677 kW |
| baseline / transparent / MITM | 各 100 控制轮；透明代理与基线一致 |
| 首次命令/物理快照偏离 | 20 / 21 |
| Bus24 负荷 | 0.420 → 0 MW；母线仍带电 |

负荷遥控、PLC 阈值和网络攻击为平台的派生实验设置，标准模型来源见 [MATPOWER case33bw](https://matpower.org/docs/ref/matpower6.0/case33bw.html)。潮流结果是 AC 准稳态快照，不包含电磁或频率暂态。

## 恒温箱插件

`examples/thermal_box/adapter.py` 在核心目录外实现独立插件：

```text
dT/dt = -0.1 × (T - 18) + 0.8 × HEATER
heater power = 800 × HEATER W
```

初始温度 19 °C，环境温度 18 °C。PLC1 提供温度和功率；PLC2 在低于 20 °C 时开启加热，高于 22 °C 时关闭，两阈值间保持状态。

```bash
python -m src.physics.contract --config examples/thermal_box/config.yaml
PYTHON_BIN="$(command -v python)" bash scripts/run_all.sh \
  --config examples/thermal_box/config.yaml --logic-wait 0.3
```

运行 10 轮时，第 6 轮关闭加热，第 7 个物理快照开始降温，10 s 温度约 20.7874 °C。温度通过解析积分计算，不依赖 EPANET 或 pandapower。

## 结果与图表

| 场景 | 结果根目录 | 绘图入口 |
| --- | --- | --- |
| 四母线 | `examples/power_feeder/output/` | `python scripts/plot_example_results.py --example power_feeder` |
| IEEE33 | `output/ieee33_bw/` | `python scripts/plot_ieee33_results.py` |
| 恒温箱 | `examples/thermal_box/output/baseline/` | `python scripts/plot_example_results.py --example thermal_box` |

绘图可安装 `requirements-power-plots.txt`，使用同一 Python 环境。结果目录保存物理状态、PLC 输入输出和攻击事件。可以沿着测量变化、控制动作和物理响应查看实验过程。

更多运行结果见项目 `docs/upsi-validation.md`、`docs/upsi-hardening-validation.md` 和 `docs/ieee33-validation.md`。添加模型与插件的步骤见[接入物理仿真器](adapter-guide.html)。
