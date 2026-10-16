# 贡献与反馈

欢迎围绕功能、安装流程和复现实验提出建议。项目开源许可和正式贡献流程需在发布计划明确后确定。

## 报告问题

如果遇到异常，建议通过项目的 [GitHub Issues](https://github.com/WandeF/hydro-cps-sim/issues) 反馈，并尽量提供：

1. 操作系统、Python / Conda 版本。
2. 所用 Git 提交号、配置文件（删除个人路径与敏感信息）。
3. 重现问题的命令与关键报错。
4. 预期结果与实际结果。

## 网站文档更新

文档仓库：[WandeF/WandeF.github.io](https://github.com/WandeF/WandeF.github.io)。修改位于 `content/zh/` 和 `content/en/` 的 Markdown 文件后执行：

```bash
python build.py
```

构建产物写入 `site/`。本地通过 `python -m http.server 8000 --directory site` 即可预览；推送到 `main` 后，GitHub Actions 自动构建并部署到 <https://wandef.github.io/>。

## 贡献范围

欢迎改进安装与配置说明、补充可复现示例、修复问题并完善中英文翻译。提交修改时，请说明用途、适用版本和验证方法；涉及实验数据时，附上配置与运行记录。
