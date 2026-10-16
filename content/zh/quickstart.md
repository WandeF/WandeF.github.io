# 快速开始

安装完成后，使用 C-Town 示例运行第一个闭环仿真实验。

> 每次运行会清理配置输出目录中的 `runtime/`、`reports/`、`st/` 和 `plcs/`。开始另一个实验前，请将需要比较的结果复制到独立目录。使用普通用户启动，脚本会按需请求 sudo。

## 运行一个示例

```bash
cd hydro-cps-sim
conda activate hydro-cps
bash scripts/run_all.sh --logic-wait 0.3
```

使用 `--iterations` 设置仿真轮数。下面运行 10 轮：

```bash
bash scripts/run_all.sh --iterations 10 --logic-wait 0.3
```

此命令将仿真缩短为 10 轮，适合检查启动与结果导出流程。

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

实验结果导出到 `output_path` 指定目录下的 `reports/csv`，日志与阶段耗时分别保存在 `logs/` 和 `timing/` 中。

运行结束后，终端显示结果位置：

```text
[DONE] Results: <output_path>/reports/csv
```

其中 `<output_path>` 对应配置中的输出目录。

## 下一步

请参考[攻防实验](experiments.html)了解如何组织基线与攻击条件对照，通过[配置说明](configuration.html)调整场景参数。
