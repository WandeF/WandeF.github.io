# Hydro-CPS-Sim Documentation

中英文文档网站，沿用 GitHub Pages 部署结构。软件代码在相邻 `hydro-cps-sim` 项目；本仓库维护网站内容、导航、搜索与静态产物。

## 构建与预览

```bash
.venv/bin/python build.py
.venv/bin/python check_site.py
.venv/bin/python -m http.server 8765 --bind 127.0.0.1 --directory site
```

新环境使用 Python 3.10+ 安装 `requirements-docs.txt`。中文入口为 `/zh/latest/index.html`，英文入口为 `/en/latest/index.html`。每种语言 16 个页面，含本页目录、语言切换和本地全文搜索。

## 内容结构

- 项目概览：首页、项目简介、系统架构。
- 使用指南：安装与环境、快速开始。
- 实验与配置：攻防实验、水网配置结构、网络配置、攻击配置。
- 扩展实验：扩展概览、UPSI 原理与接口、接入物理仿真器、UPSI 配置、电网与恒温箱实验。
- 社区与研究：论文与引用、贡献与反馈。

`content/zh/` 和 `content/en/` 是 Markdown 源文件；`build.py` 的 PAGES 定义双语导航与页面清单。`assets/` 与 `template.html` 保存样式、脚本、图和模板。`site/` 是自包含部署产物。

## UPSI 架构图与独立说明

新版图源及 PNG/SVG/PDF、独立原理说明存放在论文作图目录：

```text
/home/lzh/MASTER/CODE/output/10_figures_and_manuscript/upsi/
  draw_upsi_architecture.py
  hydro_cps_sim_architecture_upsi.{png,svg,pdf}
  UPSI原理与实现说明.md
```

网站使用同一 SVG，保留原论文图资产。原图来源和更新范围见 ASSET_SOURCES.md。当前接口与配置内容核对代码提交 d7fafbd，维护记录见 SOURCE_REVIEW.md。

## 部署与检查

`.github/workflows/pages.yml` 在 PR 上构建检查，在推送 main 时部署 site/。本地构建不会触发发布。GitHub Pages 使用 GitHub Actions Source，不配置 CNAME 或旧自定义域名。

check_site.py 从 PAGES 校验双语页面、搜索条目、链接和目录锚点；新增页面不再依赖写死的旧页面数。网站为基于 Mistune 的静态生成器，结构借鉴 CPSim 的概览、入门、扩展、示例与 API 阅读路径，未迁移到 Sphinx 或复制其代码。
