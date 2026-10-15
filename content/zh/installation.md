# 安装与环境

这里的安装说明根据公开的 [`install.sh`](https://github.com/WandeF/hydro-cps-sim/blob/2406aa649738c585e635b3661d1b9431db73edb8/install.sh) 整理。执行前建议先阅读脚本，了解其对系统软件包和第三方仓库的修改。

## 支持的环境

| 项目 | 已确认要求 |
| --- | --- |
| 操作系统 | Ubuntu 22.04 / 24.04，x86_64 |
| Python | 3.10（安装脚本创建的 Conda 环境） |
| 环境管理 | Conda |
| 系统权限 | 安装和网络配置环节需要 `sudo` |
| 网络连接 | 安装依赖及克隆所需仓库 |
| 主体依赖 | OpenPLC 命令行运行时、ns-3、DHALSIM-epynet |

> **注意：** 脚本安装的是 OpenPLC 命令行运行时，不是 Web 管理服务。请不要将本说明理解为安装完整的 OpenPLC Web 界面。

## 获取源码

```bash
git clone https://github.com/WandeF/hydro-cps-sim.git
cd hydro-cps-sim
```

## 预检查

首先建议使用只读预演参数，查看计划执行的操作：

```bash
bash install.sh --dry-run
```

## 正式安装

确认环境及权限后再运行：

```bash
bash install.sh
conda activate hydro-cps
```

安装过程中可能需要较长时间编译 OpenPLC 和 ns-3。默认环境名为 `hydro-cps`；脚本也支持 `--env`、`--jobs`、`--parent` 等参数，详见 `bash install.sh --help`。

## 安装完成后的自检

安装脚本末尾包含基础测试过程；如需再次运行仓库中的 Python 单元测试：

```bash
python -m unittest discover -s tests
```

**请区分两种验证**：本站的文档构建成功不等于仿真平台安装成功。完整环境安装需要在符合条件的 Linux 计算机上单独进行。


源码核对：[hydro-cps-sim @ 2406aa6](https://github.com/WandeF/hydro-cps-sim/tree/2406aa649738c585e635b3661d1b9431db73edb8) · 2026-10-15.

安装脚本会更新所有 C-Town 示例 YAML 的五个顶层路径键，并将修改前的文件保存到 `output/install-backups/`。迁移机器后需重新检查路径；不要直接沿用源码中的开发者绝对路径。
