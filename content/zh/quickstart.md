# 快速开始

本页以仓库自带的 C-Town 示例配置为入口。以下命令来自当前公开运行脚本，建议在安装成功后执行。

> 每次运行会清理配置输出目录中的 `runtime/`、`reports/`、`st/` 和 `plcs/`。开始另一个实验前，请将需要比较的结果复制到独立目录。使用普通用户启动，脚本会按需请求 sudo。

## 运行一个示例

```bash
cd hydro-cps-sim
conda activate hydro-cps
bash scripts/run_all.sh --logic-wait 0.3
```

如果希望先缩短实验轮数，可以使用运行器的 `--iterations` 参数，例如：

```bash
bash scripts/run_all.sh --iterations 10 --logic-wait 0.3
```

这里的 `10` 只是用于演示运行参数的示例值，并不是已经验证的基准配置。

## 自定义配置入口

```bash
bash scripts/run_all.sh --config examples/c_town/config.yaml
```

运行器的可选参数包括：

| 参数 | 用途 |
| --- | --- |
| `--config PATH` | 指定 YAML 配置文件 |
| `--iterations N` | 覆盖仿真轮数 |
| `--logic-wait SECONDS` | SCADA 下发后、读取 PLC 输出前的等待间隔 |
| `--poll-interval SECONDS` | 文件标志轮询间隔 |
| `--scada-modbus-workers N` | SCADA Modbus 并行工作线程数 |

具体帮助信息可由 `bash scripts/run_all.sh --help` 查询。

## 查看输出

运行脚本会输出日志、时序统计等内容。根据当前公开入口，实验结果导出位置为配置所指定输出目录下的 `reports/csv`。

运行结束后，终端还会打印类似下面的提示：

```text
[DONE] Results: <output_path>/reports/csv
```

真实路径取决于配置文件中的 `output_path`，请勿直接复制上面的占位符作为命令。

## 下一步

请参考[攻防实验](experiments.html)了解如何组织基线与攻击条件对照，并在[配置说明](configuration.html)中核对场景文件。


源码核对：[hydro-cps-sim @ 2406aa6](https://github.com/WandeF/hydro-cps-sim/tree/2406aa649738c585e635b3661d1b9431db73edb8) · 2026-10-15.
