# Hydro-CPS-Sim 文档

面向供水网络信息物理系统安全研究的联合仿真平台。

Hydro-CPS-Sim 将水力过程、PLC 控制、SCADA 通信与网络仿真连接起来，用于运行攻击实验、观察系统行为和开发安全方法。

源代码：[WandeF/hydro-cps-sim](https://github.com/WandeF/hydro-cps-sim)

## 项目概览

- **跨层联合仿真**：连接水力模型、控制逻辑和通信过程，观察网络层事件如何影响物理水网。
- **攻击实验**：提供 MITM、DoS 和 PLC 逻辑注入场景，可调整目标、参数和时间窗口。
- **配置与运行**：使用 YAML 设置场景，通过脚本启动仿真并导出日志与 CSV 结果。
- **面向研究扩展**：围绕控制、网络和物理层扩展实验设置，用于研究攻击传播、异常检测及防御策略。

开始使用时，先完成[安装](installation.html)，再运行[快速开始](quickstart.html)中的 C-Town 示例。

## 了解平台

查看[系统架构与闭环流程](architecture.html)、[C-Town 控制依赖](introduction.html)以及[攻击类型与示例配置](experiments.html)，了解平台如何连接网络、控制与水力过程。

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
