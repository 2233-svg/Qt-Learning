# QInputDevice：输入事件来源的设备描述

> Qt 版本：6.11.1  
> 模块：`Qt6::Gui`  
> 头文件：`#include <QInputDevice>`  
> 自 Qt 6.0 提供  
> 继承：`QObject`

## 它解决什么问题

`QInputDevice` 描述某个 `QInputEvent` 来自哪一类物理或逻辑输入设备，以及该设备能提供哪些数据。它把“这是触摸屏还是触控板、是否有压感、属于哪个 seat、能控制虚拟桌面的哪一块区域”等稳定信息，从单次鼠标、触摸、平板事件中抽取出来。

应用通常不自行创建或注册它。平台插件负责发现、注册并持续拥有实际设备；应用通过 `QInputEvent::device()` 或 `QInputDevice::devices()` 读取这些对象。这样同一套事件处理代码可根据设备能力降级，而不是把所有触控输入都误当作鼠标。

`QInputDevice` 是 `QObject`，但不是典型的“业务对象”。从 Qt 得到的 `const QInputDevice *` 是平台/Qt 管理的观察对象：不要删除、重新设 parent 或尝试借由 `devices()` 添加设备。

## 实际使用场景

- 绘图程序仅在手写笔支持 `Pressure`、倾斜或旋转时启用对应笔刷参数。
- 触摸交互根据 `TouchScreen` 与 `TouchPad` 区分直接触摸和间接指针式触摸。
- 多用户或多输入座席系统按 `seatName()` 选择主键盘。
- 多屏绘图板根据 `availableVirtualGeometry()` 显示当前映射到的屏幕区域。
- 滚动代码按 `PixelScroll` 区分触控板的像素级滚动与传统离散滚轮。
- 诊断工具列出已注册设备的名字、类型、平台 ID 与能力。

## 从事件拿设备，而不是猜事件类型

```cpp
void Canvas::tabletEvent(QTabletEvent *event)
{
    const QInputDevice *device = event->device();
    if (device && device->hasCapability(QInputDevice::Capability::Pressure)) {
        setBrushPressure(event->pressure());
    } else {
        setBrushPressure(1.0);
    }
}
```

先检查能力，再读取相应事件字段。设备类型只能说明“可能是哪类设备”，能力才说明驱动和平台实际上提供了什么。例如有些 stylus 没有倾斜或切向压力数据；不要因为 `type() == Stylus` 就假设所有 tablet 字段都有意义。

## 设备类型与能力是两条正交信息

`DeviceType` 描述设备类别，`Capabilities` 描述可报告的数据，两者不能互相替代。

| `DeviceType` | 实际含义 |
| --- | --- |
| `Mouse` | 鼠标或鼠标式指针设备。 |
| `TouchScreen` | 触控面与显示器一体，物理触点与屏幕坐标通常直接对应，可同时作用于多个目标。 |
| `TouchPad` | 触控面与显示器分离，通常相对当前指针位置工作，交互语义更接近间接指针。 |
| `Stylus` | 数位板或具独立笔感知能力的笔形设备。 |
| `Airbrush` | 带拇指滚轮、可提供切向压力的 stylus 类设备。 |
| `Puck` | 带准星窗口的扁平定位器。 |
| `Keyboard` | 键盘。 |
| `Unknown` | 平台不能识别的类型。 |
| `AllDevices` | flags 哨兵，用于“任意设备类型”的筛选表达，不是可观察到的具体硬件。 |

常用能力可以按数据域理解：

| 能力 | 事件处理时的含义 |
| --- | --- |
| `Position` / `NormalizedPosition` | 可用位置或归一化位置数据。 |
| `Area` | `QEventPoint::ellipseDiameters()` 等接触面积数据有效。 |
| `Pressure` / `TangentialPressure` | 有笔压或切向压力数据。 |
| `Velocity` | 可取得触点速度向量。 |
| `Rotation` | 可取得触点或工具旋转信息。 |
| `XTilt` / `YTilt` | 可取得平板笔 X/Y 倾斜。 |
| `ZPosition` | 可取得 Z 轴位置。 |
| `Hover` | 设备可悬停而不接触。 |
| `Scroll` / `PixelScroll` | 有滚动能力；后者通常表示触控板可提供像素精度 `pixelDelta()`。 |
| `MouseEmulation` | 设备会合成鼠标事件；应用应避免把一套物理操作重复处理两次。 |
| `None` / `All` | 分别表示未获能力信息与 flags 哨兵。 |

`capabilities()` 是 flags，检测单项时优先用 `hasCapability()`，不要把整个 flags 值与某一个枚举值直接相等比较。

## 注册表并非硬件设备管理 API

```cpp
for (const QInputDevice *device : QInputDevice::devices()) {
    qDebug() << device->name()
             << device->type()
             << device->systemId()
             << device->capabilities();
}
```

`devices()` 返回已注册的键盘与指针设备。它在 Linux 上启动及热插拔场景的信息相对完整；许多其他平台只能在已收到相应事件后提供通用设备，而且可能不通知拔出或运行时插入。因此它适合界面适配、日志与诊断，不适合做精确的系统硬件盘点或安全策略。

返回的列表只用于观察，不能用于添加模拟设备。自动化测试若需模拟触摸设备，应使用 `QTest::createTouchDevice()`；平台插件则使用 `QWindowSystemInterface::registerInputDevice()`，这两者都不是普通应用运行时注册入口。

## seat、主键盘和可访问区域

一个 seat 是一组一起服务于同一用户的输入设备。在 Wayland、X11 等支持多座席的平台上，鼠标、键盘与平板可共享 `seatName()`；不支持或未知时该名称为空。

`primaryKeyboard(seatName)` 返回指定 seat 的 core/master keyboard。空字符串请求默认 seat；返回值可能为空，调用方必须检查。`seatNames()` 自 Qt 6.3 起列出当前已注册设备涉及的 seat 名。

`availableVirtualGeometry()` 说明该设备能够控制虚拟桌面的哪块区域：

- 固定在单块屏幕上的触摸屏通常返回该屏的 geometry。
- 普通鼠标常可到达全部虚拟桌面。
- 绘图板可被用户配置为映射全部屏幕、单屏或特定窗口。
- 返回 null `QRect` 表示没有专门限制，即可访问整个虚拟桌面。

映射因显示器拓扑、校准或系统设置改变时，监听 `availableVirtualGeometryChanged()`，不要只在启动时缓存一次。

## 名称、系统 ID 与生命周期

`name()` 是设备模型名或其他可辨认名称，允许为空，适合日志和同机多设备的提示，不适合作为稳定主键。`systemId()` 是平台特定的、每设备唯一的标识，例如 X11 的 xinput ID；它适合在当前平台会话内关联事件，但不应当作跨平台或持久化的业务 ID。

`operator==` 提供两个 `QInputDevice` 描述的比较；对于来自 Qt 注册表的设备，若目的只是判断同一来源，通常比较事件中的 `device()` 指针或当前会话中的 `systemId()` 更直接。不要通过复制 `QInputDevice` 建立独立业务快照：此类禁止复制和移动。

设备实例由平台插件创建、注册并拥有。手动构造函数主要面向平台集成、模拟环境或受控测试；默认构造得到无效设备，带参数构造的能力初始为 `None`。普通应用若人为创建一个同名的 `QInputDevice`，它不会自动接收系统事件，也不会加入 Qt 的设备注册表。

## 常见错误

- 只根据 `DeviceType` 读取 pressure、tilt 或 pixel scroll，而未检查 capability。
- 把 `devices()` 当成所有平台都完整、实时的硬件清单。
- 删除或修改从 `QInputEvent::device()` / `devices()` 得到的设备对象。
- 将 `systemId()` 持久化为跨设备、跨重启或跨平台的用户标识。
- 对 `Capabilities` 做相等比较，导致含多个能力的设备被误判。
- 把 `MouseEmulation` 产生的鼠标事件与原始触摸事件并行执行业务逻辑。
- 假设 `primaryKeyboard()` 总能返回非空指针。
- 把 null `availableVirtualGeometry()` 当成“设备没有可用区域”，而不是“可访问整个虚拟桌面”。
- 在图形设置或热插拔后继续使用旧的 geometry 缓存。

## API 速查表

| 类别 | API | 语义与边界 |
| --- | --- | --- |
| 类型 | `DeviceType` | 设备类别枚举：鼠标、触摸屏、触控板、puck、stylus、airbrush、键盘、未知；`AllDevices` 是 flags 哨兵。 |
| 类型 | `DeviceTypes` | `QFlags<DeviceType>`，可组合表示类型集合。 |
| 类型 | `Capability` | 单项输入数据能力：位置、面积、压力、速度、滚动、悬停、旋转、倾斜、Z 轴等。 |
| 类型 | `Capabilities` | `QFlags<Capability>`；使用 `hasCapability()` 测单项，`All` 是哨兵。 |
| 构造 | `QInputDevice(QObject *parent = nullptr)` | 创建无效设备；普通应用通常不需要这样做。 |
| 构造 | `QInputDevice(name, systemId, type, seatName, parent)` | 创建带平台描述的设备，能力初始为 `None`；供平台集成/受控测试使用，不自动注册。 |
| 析构 | `~QInputDevice()` | 销毁对象；注册设备通常由平台插件拥有，不应由应用删除。 |
| 属性 | `name()` | 返回设备名称，可为空；适合显示和诊断，不是稳定 ID。 |
| 属性 | `type()` | 返回 `DeviceType`；类别不保证特定事件字段一定有效。 |
| 属性 | `capabilities()` | 返回能力 flags；可在运行期改变。 |
| 属性 | `hasCapability(Capability)` | 查询是否有单项能力；读取压感、倾斜等数据前使用。 |
| 属性 | `systemId()` | 返回平台特定且设备唯一的 ID；不应作跨平台持久化键。 |
| 属性 | `seatName()` | 返回关联 seat，未知或平台不支持时为空。 |
| 属性 | `availableVirtualGeometry()` | 返回可访问的虚拟桌面区域；null rect 表示整个虚拟桌面。 |
| 信号 | `availableVirtualGeometryChanged(QRect)` | 设备映射区域变化时发出；多屏/校准变化后更新 UI。 |
| 信号 | `capabilitiesChanged(Capabilities)` | Qt 6.9 起。能力集合变化时发出；不要假设设备能力永远不变。 |
| 注册表 | `static devices()` | 返回所有已注册键盘和指针设备的 const 指针列表；跨平台可能不完整，不能用于添加设备。 |
| 注册表 | `static seatNames()` | Qt 6.3 起。返回已注册设备涉及的 seat 名列表。 |
| 注册表 | `static primaryKeyboard(const QString &seatName = {})` | 返回指定或默认 seat 的主键盘；找不到时可能为 `nullptr`。 |
| 比较 | `operator==(const QInputDevice &)` | 比较两个设备描述；应用不应依赖复制对象来做注册表管理。 |
| 调试 | `operator<<(QDebug, const QInputDevice *)` | 输出设备调试描述；不是稳定序列化格式。 |

## 相关类

- `QInputEvent`：所有输入事件可通过 `device()` 指向其来源。
- `QPointingDevice`：带点输入特性的 `QInputDevice` 派生类。
- `QPointerEvent` / `QEventPoint`：位置、压力、速度、面积等具体数据的载体。
- `QTabletEvent`：手写笔、倾斜、切向压力等平板输入事件。
- `QScreen`：与 `availableVirtualGeometry()` 的屏幕映射协作。

`QInputDevice` 让应用用“此设备实际能报告什么”来处理输入，而不是用一堆平台专用假设去猜。对跨设备交互来说，能力检测比设备名称和类型更可靠。
