# 接入物理仿真器

将求解器封装为 `PhysicsBackend`，声明原生端口，并通过场景配置注册。适配器可以放在示例目录或独立 Python 包中。

## 准备模型与端口

先确认求解器的模型格式、初始条件、可写输入、可读输出、工程单位、时间接口和错误状态。例如恒温箱定义：

| 端口 | 方向 | 类型 | 单位 |
| --- | --- | --- | --- |
| `box.temperature` | output | float | degC |
| `box.heater_power` | output | float | W |
| `heater.enabled` | input | bool | 1 |

EPANET 端口按节点/链接命名；pandapower 端口按结果表、别名、列命名；插件可以定义适合自身模型的稳定端口名。

## 编写适配器

完整示例位于项目的 `examples/thermal_box/adapter.py`。接口结构如下，其中 `solver` 表示待接入的真实求解器 API，需替换为对应实现：

```python
from src.physics.base import PhysicsBackend
from src.physics.types import SignalSpec, StepResult

class PlantBackend(PhysicsBackend):
    def __init__(self, config):
        self.config = config
        # 保存配置；把求解器资源的获取放在 initialize()。

    def describe(self):
        return {
            'signals': {
                'plant.measurement': SignalSpec(
                    'plant.measurement', 'output', 'float', 'K'),
                'plant.enabled': SignalSpec(
                    'plant.enabled', 'input', 'bool', '1'),
            },
            'timing': 'target',
            'model_kind': 'your_physical_model',
        }

    def initialize(self):
        # 加载模型、应用 self.config.initial_inputs，返回初始 StepResult。
        # 重复调用应返回当前初始结果的独立副本，不重新加载。
        raise NotImplementedError('Connect the real solver initialization')

    def advance(self, until_s, inputs):
        # 应用完整 inputs，求解到目标时间，再返回实际时间与完整结果。
        raise NotImplementedError('Connect the real solver step')

    def close(self):
        # 释放已获取的资源，允许初始化失败后调用和重复调用。
        pass
```

模板只展示接口，不产生模拟结果。实际返回示例为 `StepResult(actual_time_s, outputs, applied_inputs, diagnostics=...)`。必须检查实际输入类型、求解收敛、输出有限性和实际时间；不能用“上次成功值”冒充新求解结果。对内部事件提前返回的求解器，声明 `timing: event_step`；普通定点推进声明 `target`。

## 注册插件

模块方式：

```yaml
physics:
  backend: my_plant
  plugins:
    my_plant:
      factory: my_package.adapter:PlantBackend
      # dependency: my_solver_package  # 可选的依赖预检模块
```

安装包方式，在包的 `pyproject.toml` 中声明：

```toml
[project.entry-points."hydro_cps.physics"]
my_plant = "my_package.adapter:PlantBackend"
```

场景中使用 `entry_point: my_plant` 代替 `factory`，二者只能选一个。安装插件的 Python 必须与 `PYTHON_BIN` 指向的运行环境一致。内置的 `dhalsim_epynet`、`pandapower` 和别名不可被场景覆盖。

## 连接信号与控制器

下例是插件物理部分的配置片段，需合入包含完整 `network` 和运行路径的场景：

```yaml
schema_version: 2
physics:
  backend: my_plant
  plugins:
    my_plant:
      factory: my_package.adapter:PlantBackend
  model:
    path: model.yaml
  timing:
    mode: fixed_step
    step_seconds: 1.0
  signals:
    observations:
      TEMPERATURE:
        port: plant.measurement
        dtype: float
        unit: K
    commands:
      HEATER:
        port: plant.enabled
        dtype: bool
        unit: '1'
actuators:
  - {name: HEATER, initial_state: false}
plcs:
  - name: PLC1
    sensors: [TEMPERATURE]
    actuators: [HEATER]
    controls:
      - {dependant: TEMPERATURE, actuator: HEATER, type: below, value: 293.15, action: true}
      - {dependant: TEMPERATURE, actuator: HEATER, type: above, value: 295.15, action: false}
```

`port`、类型与单位必须和 `describe()` 一致。多个 PLC 的远程依赖通过传感器拥有者推导，SCADA 自动转发；不需要在后端编写 Modbus 逻辑。

## 运行适配器

已有恒温箱可以直接运行：

```bash
python -m src.physics.contract --config examples/thermal_box/config.yaml
```

新后端使用相同命令并替换配置路径。这个命令会初始化模型并推进三次，检查输入、输出与物理时间，最后释放资源。声明的可选依赖未安装时返回 `skipped`；加载、模型或求解失败时返回 `failed`。

独立 SDK 调用可使用 `configure_plugins(raw)` 创建注册上下文，将其传入 `BackendConfig.registry`，再通过 `create_backend(name, config)` 创建实例。`exercise_backend(backend, initial_inputs, step_seconds)` 提供相同的可复用测试入口。

## 接入真实闭环

先运行已有恒温箱，确认环境：

```bash
PYTHON_BIN="$(command -v python)" bash scripts/run_all.sh \
  --config examples/thermal_box/config.yaml --logic-wait 0.3
```

然后替换为新场景。完整运行需要真实 OpenPLC、ns-3 和 namespace 权限，单独运行适配器时不需要这些组件。

检查 `physics_state.csv`、`physics_signals.csv`、PLC 线圈读回、SCADA 原始记录及 `signal_quality.csv`，确认命令在下一返回物理快照中生效。新求解器至少覆盖已知轨迹、初始化重复调用、单位/类型错误、求解失败、错误时间戳和清理行为。

## 常见接入问题

| 现象 | 检查项 |
| --- | --- |
| 找不到插件 | 模块是否可导入、包是否安装到同一 Python、factory/entry point 名称 |
| 端口或方向错误 | `describe().signals` 与 `physics.signals` 是否一致 |
| 单位变换失败 | 是否显式填写 scale/offset，量纲是否可转换 |
| 输入缺失 | 是否覆盖全部原生输入且没有重复映射，初始执行器是否齐全 |
| 时间停止或倒退 | 是否返回求解器实际时间，内部事件后是否确实前进 |
| 失败后仍有新数据 | 是否抛出异常而非伪造成功结果，是否使用会话发布流程 |
| 原生库有并发问题 | 注册隔离只保护配置上下文，需另行处理求解器线程/进程约束 |
