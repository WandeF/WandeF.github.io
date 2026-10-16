# 系统架构

Hydro-CPS-Sim 由水力仿真、PLC 控制、SCADA、网络和攻击模块组成。各模块通过数据交换和状态同步共同完成闭环仿真。

## 平台总体架构

<figure>
<a href="../../assets/hydro_cps_sim_architecture.png" target="_blank" rel="noopener"><img src="../../assets/hydro_cps_sim_architecture.png" alt="Hydro-CPS-Sim 场景配置、编排、物理、控制、网络、同步与记录模块架构图" loading="lazy" width="4978" height="3116"></a>
<figcaption>平台总体架构：场景配置、联合仿真编排与各运行模块。</figcaption>
</figure>

| 模块 | 功能 |
| --- | --- |
| 场景配置 | YAML 描述水网、PLC/SCADA 映射、控制规则、网络、攻击与运行参数 |
| 联合仿真编排 | 生成 ST 程序、编译 PLC、生成网络环境、启动进程并导出结果 |
| 物理过程 | DHALSIM-epynet / EPANET 推进水力状态，接收泵阀动作 |
| 控制与监控 | OpenPLC 执行控制逻辑；PLC Adapter 衔接输入输出；SCADA 通过 Modbus TCP 采集与转发数据 |
| 网络通信 | Linux network namespace 提供独立网络身份，经 TAP/veth 接入 ns-3 |
| 攻击执行 | 在配置的协议、网络或控制入口执行 MITM、DoS 或逻辑注入 |
| 同步 | 通过文件系统标志协调多进程，按实验轮次交换状态 |
| 数据记录 | 汇集攻击、通信、控制、执行器与水力记录，供基线对照使用 |

## 闭环运行流程

<figure>
<a href="../../assets/closed_loop_experiment_workflow.png" target="_blank" rel="noopener"><img src="../../assets/closed_loop_experiment_workflow.png" alt="场景生成、启动、SCADA 采集、PLC 控制与水力反馈闭环流程" loading="lazy" width="2888" height="1818"></a>
<figcaption>闭环运行流程：场景生成、数据采集、控制执行与水力反馈。</figcaption>
</figure>

1. **环境生成**：读取水网和 YAML 配置，生成控制程序、地址映射、ns-3 拓扑与命名空间配置。
2. **初始化**：启动 OpenPLC、SCADA 与网络进程，准备物理状态和同步目录。
3. **采集与转发**：水力模块提供当前传感器状态，SCADA 通过 Modbus TCP 采集数据并转发跨 PLC 控制依赖。
4. **控制执行**：OpenPLC 根据当前输入和有效规则生成泵阀命令。
5. **水力反馈**：执行器状态进入下一步水力求解，产生新的水位、压力和流量。
6. **保存结果**：记录当前轮次的数据，然后进入下一轮仿真。

## 网络连接

每个 PLC、SCADA 和攻击节点运行在各自的 Linux network namespace 中，拥有独立接口和协议栈。ns-3 为这些端点提供可配置的链路、路由与网络动态。正常 Modbus 通信和攻击流量通过配置的网络路径交互。

SCADA 通过 Modbus TCP 访问 PLC 的寄存器和线圈，完成传感器采集和控制数据下发。网络参数影响这些请求和响应，你可以通过日志查看通信、数据更新与控制输出。

## 代码入口

- `scripts/run_all.sh`：环境准备、运行和清理的总入口。
- `src/control/`：ST 程序生成、编译与 OpenPLC 启动。
- `src/network/`：命名空间与 ns-3 拓扑生成。
- `src/runtime/`、`src/sync/`：闭环协调与同步。
- `src/scada/`、`src/plc/`、`src/comm/`：数据采集、适配与 Modbus 交互。
- `src/attack/`：攻击启动与执行。
- `src/io/`：水力接口与结果导出。

使用方法参见[快速开始](quickstart.html)，运行参数参见[配置说明](configuration.html)。
