# 扩展实验

除了 C-Town 水网，Hydro-CPS-Sim 还可以连接电网、热系统或自己的物理模型。UPSI 为这些模型提供相同的调用方式，PLC、SCADA、网络和攻击仍按原来的流程运行。

## 添加一个物理模型

你可以从已有示例开始，或为新的求解器编写适配器：

- [了解 UPSI](upsi.html)：模型如何交换测量与控制输入。
- [编写适配器](adapter-guide.html)：实现初始化、步进和结果读取。
- [填写 UPSI 配置](upsi-configuration.html)：选择后端、连接变量、设置单位和时间。
- [运行电网与恒温箱示例](extended-examples.html)：了解完整的配置和运行过程。

## 可以修改哪些内容

| 想要做什么 | 修改位置 |
| --- | --- |
| 换一个水网 | INP 文件与 inp_file，见[配置说明](configuration.html) |
| 换用其他物理模型 | physics.backend 与 physics.model.path |
| 使用模型中的其他测量 | physics.signals.observations |
| 改变控制输入或单位 | physics.signals.commands 和信号映射 |
| 调整控制阈值 | plcs 中的 controls |
| 更换网络或攻击设置 | network 与 attacks |
| 接入新的仿真器 | 编写适配器，并在 physics.plugins 中注册 |

## 运行自己的实验

先运行模型，确认初值和单位，再运行无攻击场景。需要研究攻击时，可以添加透明代理和攻击配置，与基线比较。

目前每个场景选择一个物理后端。物理模型负责计算系统状态，平台负责将状态送入控制器，并把控制输出交回模型。
