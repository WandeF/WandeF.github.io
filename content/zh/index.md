# Hydro-CPS-Sim 文档

面向供水网络信息物理系统安全研究的联合仿真平台。

Hydro-CPS-Sim 将水力过程、PLC 控制、SCADA 通信与网络仿真连接起来，为网络攻击评估、跨层影响分析和防御研究提供可扩展的实验环境。

源代码：[WandeF/hydro-cps-sim](https://github.com/WandeF/hydro-cps-sim)

## 项目概览

- **跨层联合仿真**：连接水力模型、控制逻辑和通信过程，观察网络层事件如何影响物理水网。
- **攻击影响评估**：为 MITM、DoS 与 PLC 逻辑篡改等研究场景提供实验与分析框架；实际可执行场景以源码和配置为准。
- **可复现实验流程**：以配置文件组织仿真，通过脚本启动多组件闭环，并导出运行日志与 CSV 结果。
- **面向研究扩展**：围绕控制、网络和物理层扩展实验设置，用于研究攻击传播、异常检测及防御策略。

平台关注一个核心问题：**网络攻击如何通过数据采集、控制决策和执行过程，逐步传播到物理水力系统？**

典型研究链路：攻击与扰动 → 网络通信（ns-3 / Namespace）→ SCADA / PLC → 水力计算（DHALSIM-epynet）→ 日志与 CSV 分析。

> **文档状态：** 本站是已部署的研究软件文档初版。公开源码仓库目前仍在整理中，尚未核实的配置字段、论文信息与实验结论不会在这里当作已发布事实。

## 文档目录

- 项目概览
  - [项目简介](introduction.html)
  - [系统架构](architecture.html)
- 使用指南
  - [安装与环境](installation.html)
  - [快速开始](quickstart.html)
- 实验与配置
  - [攻防实验](experiments.html)
  - [配置说明](configuration.html)
- 社区与研究
  - [论文与引用](publications.html)
  - [贡献与反馈](contributing.html)
