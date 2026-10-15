# Hydro-CPS-Sim · CPS² Lab Documentation

中英文研究软件文档网站，部署于 **https://wandef.github.io/**。

本仓库 `WandeF/WandeF.github.io` 已替换原博客，仅维护文档；沿用原 Git 历史。软件源码在 [WandeF/hydro-cps-sim](https://github.com/WandeF/hydro-cps-sim)，本次只读核查，未修改。

## 本地构建与预览

需要 Python 3.10+。使用 Mistune 渲染 Markdown，不是 Sphinx，也未复制 CPSim 的主题或代码。

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-docs.txt
python build.py
python check_site.py
python -m http.server 8000 --directory site
```

访问 http://localhost:8000/ ，根路径跳转中文。中文 `/zh/latest/`，英文 `/en/latest/`，章节支持对应语言切换和本地全文搜索。直接预览已有 `site/` 时无需安装依赖。

## 维护与部署

- `content/zh/`、`content/en/`：每种语言 9 个 Markdown 页面。
- `assets/`、`template.html`：样式、搜索、移动导航和页面模板。
- `build.py`：生成 `site/`；`check_site.py`：检查链接、语言页面、索引和域名配置。
- `.github/workflows/pages.yml`：PR 构建检查；推送 `main` 自动构建、检查并部署 `site/`。
- `SOURCE_REVIEW.md`：源码核对版本、发现的问题及验证范围。

GitHub Pages 的 Source 使用 **GitHub Actions**，不使用分支根目录发布。Pages 自定义域名留空，启用 HTTPS；仓库和构建产物均不应包含 `CNAME`。只上传 `site/`，源码、README 和本地配置不会进入站点产物。

修改后执行构建和检查，将源文件与 `site/` 一同提交到 `main`。在仓库 Actions 的 `Build and deploy documentation` 中查看构建和部署结果。恢复历史版本应使用 `git revert` 创建新提交，保留历史。

## 内容状态

安装和运行入口、配置文件与导出路径已根据软件提交 `2406aa649738c585e635b3661d1b9431db73edb8` 核查。本文档构建和在线检查不代表完整仿真已经复现。

待完善：Ubuntu 上的完整安装与基线/攻击复现、实验图表、完整配置字典、正式论文信息和经项目团队确认的许可证。未添加未经授权的许可证或虚构论文信息。
