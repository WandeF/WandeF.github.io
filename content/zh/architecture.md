# 系统架构

Hydro-CPS-Sim 将物理过程、PLC 控制、SCADA、网络和攻击连接起来。传感器数据进入控制器，控制器输出作用于设备，设备状态再影响物理过程。

## 平台总体架构

<figure><img src="../../assets/hydro_cps_sim_architecture_upsi.svg" alt="在原平台架构中增加 UPSI 的 Hydro-CPS-Sim 架构图"><figcaption>Hydro-CPS-Sim 总体架构。UPSI 连接物理仿真器与控制闭环。</figcaption></figure>

| 模块 | 功能 |
| --- | --- |
| 场景配置 | 设置水网或其他物理模型、控制规则、网络和攻击 |
| 联合仿真调度 | 生成程序、准备网络、启动各模块并收集结果 |
| 物理层 | 计算水位、压力、流量，或其他模型的物理状态 |
| UPSI | 将物理模型的测量和控制输入连接到平台，统一变量、单位和时间 |
| 控制与 SCADA | OpenPLC 执行控制规则，SCADA 采集数据并转发跨 PLC 依赖 |
| 网络层 | 使用 namespace、TAP/veth 与 ns-3 连接各通信节点 |
| 攻击层 | 提供 MITM、DoS 和 PLC 逻辑注入 |
| 同步与记录 | 协调各模块，保存状态、通信、控制与攻击数据 |

## 物理模型与 UPSI

水网使用 EPANET 计算水力状态。需要研究其他系统时，可以通过 UPSI 选择 pandapower、恒温箱或自己的适配器。各模型使用不同的方程和求解方法，但都向控制器提供测量，并接收控制输入。

模型的端口、单位和步进方式由适配器说明。平台使用这些信息调用模型，不需要为每个求解器重新编写控制和网络流程。具体用法见[扩展实验](extensions.html)。

## 闭环运行流程

1. 读取配置和模型，生成 PLC 程序与网络拓扑。
2. 启动各模块，准备初始测量和执行器状态。
3. PLC Adapter 将物理测量写入本地 PLC；SCADA 采集数据并转发远程依赖。
4. OpenPLC 根据输入执行控制规则，输出泵阀或其他设备命令。
5. 物理模型接收命令，计算下一状态。
6. 保存结果，进入下一轮。

PLC Adapter 通过本地 Modbus 接口连接 OpenPLC。SCADA 与各 PLC 之间的通信经过配置的 ns-3 网络，时延、拥塞和攻击会影响这条通信路径。

## 查看和扩展代码

| 目录 | 内容 |
| --- | --- |
| scripts/run_all.sh | 完整实验入口 |
| src/control/ | PLC 程序生成、编译和启动 |
| src/physics/ | 物理模型接口和适配器 |
| src/plc/、src/scada/、src/comm/ | 数据采集、转发与 Modbus 交互 |
| src/network/ | namespace 与 ns-3 拓扑 |
| src/attack/ | 攻击调度和执行 |
| src/runtime/、src/sync/ | 闭环运行与同步 |
| src/io/ | 数据保存与结果导出 |

开始运行请查看[快速开始](quickstart.html)。水网参数见[配置说明](configuration.html)，新增物理模型见[接入物理仿真器](adapter-guide.html)。
