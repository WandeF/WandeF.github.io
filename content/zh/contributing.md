# 贡献与反馈

欢迎提交问题、改进文档或参与功能开发。

## 报告问题

遇到问题时，可以在 [GitHub Issues](https://github.com/WandeF/hydro-cps-sim/issues) 中反馈。请附上：

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

欢迎改进安装与配置说明、补充可复现示例、修复问题并完善中英文翻译。提交修改时，简要说明改动和测试方法。实验示例可附上配置与运行记录。
