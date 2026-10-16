# 安装与环境

使用 `install.sh` 安装 Hydro-CPS-Sim 及其依赖。安装过程会配置系统软件包、Conda 环境、OpenPLC 命令行运行时、ns-3 和 DHALSIM-epynet。

## 支持的环境

| 项目 | 要求 |
| --- | --- |
| 操作系统 | Ubuntu 22.04 / 24.04，x86_64 |
| Python | 3.10（安装脚本创建的 Conda 环境） |
| 环境管理 | Conda |
| 系统权限 | 安装和网络配置环节需要 `sudo` |
| 网络连接 | 安装依赖及克隆所需仓库 |
| 主体依赖 | OpenPLC 命令行运行时、ns-3、DHALSIM-epynet |

> 安装包含 OpenPLC 命令行运行时，不包含 Web 管理服务。

## 获取源码

```bash
git clone https://github.com/WandeF/hydro-cps-sim.git
cd hydro-cps-sim
```

## 查看安装计划

查看安装计划，不修改系统：

```bash
bash install.sh --dry-run
```

## 正式安装

运行安装脚本：

```bash
bash install.sh
conda activate hydro-cps
```

安装过程中可能需要较长时间编译 OpenPLC 和 ns-3。默认环境名为 `hydro-cps`；脚本也支持 `--env`、`--jobs`、`--parent` 等参数，详见 `bash install.sh --help`。

## 安装完成后的自检

安装程序会检查 EPANET 动态库并运行 Python 单元测试。你也可以手动运行测试：

```bash
python -m unittest discover -s tests
```

安装完成后，继续[快速开始](quickstart.html)运行 C-Town 示例。

安装脚本会更新所有 C-Town 示例 YAML 的五个顶层路径键，并将修改前的文件保存到 `output/install-backups/`。更换机器或依赖目录时，更新配置中的路径。
