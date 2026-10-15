<div class="hero">
<div class="hero-kicker">CPS² Lab · Water CPS Security</div>
<h1>Hydro-CPS-Sim</h1>
<p>面向供水网络的信息物理系统安全联合仿真平台。将水力过程、PLC 控制、SCADA 通信与网络仿真连接起来，为网络攻击评估、跨层影响分析和防御研究提供可扩展的实验环境。</p>
<div class="hero-buttons"><a href="quickstart.html">快速开始 →</a><a href="architecture.html" class="outline">了解系统架构</a><a class="outline" href="https://github.com/WandeF/hydro-cps-sim" target="_blank" rel="noopener">访问 GitHub ↗</a></div>
</div>

<span class="eyebrow">Project Overview</span>

## 研究平台能做什么？

<div class="feature-grid">
<div class="feature"><span class="glyph">▤</span><strong>跨层联合仿真</strong><p>连接水力模型、控制逻辑和通信过程，观察网络层事件如何影响物理水网。</p></div>
<div class="feature"><span class="glyph">⌁</span><strong>攻击影响评估</strong><p>为 MITM、DoS 与 PLC 逻辑篡改等研究场景提供实验与分析框架；实际可执行场景以源码和配置为准。</p></div>
<div class="feature"><span class="glyph">▦</span><strong>可复现实验流程</strong><p>以配置文件组织仿真，通过脚本启动多组件闭环，并导出运行日志与 CSV 结果。</p></div>
<div class="feature"><span class="glyph">◇</span><strong>面向研究扩展</strong><p>围绕控制、网络和物理层扩展实验设置，用于研究攻击传播、异常检测及防御策略。</p></div>
</div>

## 从网络事件到物理响应

<div class="layers"><div class="layer">攻击与扰动<small>MITM / DoS / Logic</small></div><div class="layer">通信仿真<small>ns-3 + Namespace</small></div><div class="layer">SCADA / PLC<small>采集与控制</small></div><div class="layer">水力计算<small>DHALSIM-epynet</small></div><div class="layer">结果分析<small>日志 / CSV</small></div></div>

平台关注一个核心问题：**网络攻击如何通过数据采集、控制决策和执行过程，逐步传播到物理水力系统？**

## 从哪里开始？

1. 阅读[项目简介](introduction.html)，了解研究问题与适用范围。
2. 查看[安装与环境](installation.html)，确认操作系统与依赖。
3. 跟随[快速开始](quickstart.html)，运行示例水网。
4. 参考[攻防实验](experiments.html)，设计基线与攻击对照。

> **版本提示：** 本站是已部署的研究软件文档初版。公开源码仓库目前仍在整理中，尚未核实的配置字段、论文信息与实验结论不会在这里当作已发布事实。
