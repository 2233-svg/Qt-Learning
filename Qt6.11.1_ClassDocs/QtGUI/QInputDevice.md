# QInputDevice

> Qt 6.11.1 · Qt GUI · 来自 `QInputDevice`

## 1. 先建立直觉

`QInputDevice` 是 Qt 对系统输入设备的抽象。键盘、鼠标、触摸屏、触摸板、手写笔等设备都会以 `QInputDevice` 或其子类的形式出现在事件中。

它回答两类不同的问题：

- 这是什么设备：`type()`，例如 `Mouse`、`TouchScreen`、`Stylus`、`Keyboard`。
- 这个设备能提供什么数据：`capabilities()`，例如压力、倾斜、速度、滚动、悬停、旋转。

类型决定你如何理解输入来源，能力决定哪些事件字段值得读取。两者不要混用：触摸屏是设备类型，压力则是能力。

## 2. 类说明

`QInputDevice` 继承自 `QObject`，`QPointingDevice` 是它的直接子类。应用一般不手动创建真实设备，而是从 `QInputEvent::device()`、`QPointerEvent::pointingDevice()` 或 `QInputDevice::devices()` 取得由 Qt 平台插件维护的对象。

类说明只用于表明这些 API 来自 `QInputDevice`。设备对象通常由 Qt 及平台插件拥有，业务代码应把它当作只读描述对象，不要随意删除、移动线程或长期假设枚举结果在所有平台完全一致。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `enum DeviceType` | 说明设备大类：鼠标、触摸屏、触摸板、手写笔、键盘等。 |
| `enum Capability` | 说明设备能报告哪些扩展数据：位置、压力、速度、滚动、悬停、倾斜、旋转等。 |
| `devices()` | 返回 Qt 当前已注册的输入设备列表。 |
| `primaryKeyboard(seatName)` | 返回指定 seat 的主键盘设备。 |
| `seatNames()` | 返回已知的输入 seat 名称，适合多用户或多输入组环境。 |
| `type() const` | 返回设备类型。 |
| `capabilities() const` | 返回设备能力位标志集合。 |
| `hasCapability(capability) const` | 判断设备是否支持某项能力。 |
| `name() const` | 返回设备名称，适合日志和诊断展示。 |
| `systemId() const` | 返回平台相关的设备 ID，适合诊断，不宜作跨平台持久标识。 |
| `seatName() const` | 返回设备所属输入 seat 名称。 |
| `availableVirtualGeometry() const` | 返回设备可访问的虚拟桌面范围；空矩形通常表示整个虚拟桌面。 |
| `availableVirtualGeometryChanged(area)` | 设备可访问区域变化时发出。 |
| `capabilitiesChanged(capabilities)` | 设备能力变化时发出。 |

## 4. 关键用法

### 先判断能力，再读取可选数据

```cpp
void PaintTool::handle(QTabletEvent *event)
{
    const QInputDevice *device = event->device();

    const qreal pressure = device->hasCapability(QInputDevice::Capability::Pressure)
        ? event->pressure()
        : 1.0;

    paintAt(event->position(), pressure);
}
```

不要因为某个事件 API 存在，就假设硬件一定能给出有意义的值。缺少能力时，事件字段可能是默认值，例如 0 压力、0 倾斜或空接触区域。

### 区分触摸屏与触摸板

```cpp
void GestureRouter::handle(QPointerEvent *event)
{
    switch (event->deviceType()) {
    case QInputDevice::DeviceType::TouchScreen:
        enableDirectManipulation();
        break;
    case QInputDevice::DeviceType::TouchPad:
        enableIndirectScrolling();
        break;
    default:
        break;
    }
}
```

触摸屏是直接输入，手指位置通常直接对应屏幕位置；触摸板则是间接输入，手指位置经系统映射到当前光标。相同的两指动作，交互策略可能完全不同。

### 枚举设备主要用于诊断和配置

```cpp
for (const QInputDevice *device : QInputDevice::devices()) {
    qDebug() << device->name()
             << device->type()
             << device->capabilities()
             << device->seatName();
}
```

设备列表适合设置页、诊断日志和测试环境，不应作为唯一功能入口。某些平台只能在收到输入事件之后才暴露通用设备，热插拔信息的完整度也因平台而异。

## 5. 使用场景

`QInputDevice` 适合跨设备输入策略：绘图程序根据压力能力启用压感笔刷，地图根据触摸屏或触摸板选择直接拖动或滚动，工业触控界面根据可访问几何区域限制输入映射。

它也适合问题排查。用户报告“笔压无效”“触摸被当成鼠标”“双屏手写笔坐标错位”时，记录设备名称、类型、能力、虚拟几何和系统 ID 往往比只记录事件类型更有用。

多 seat 支持主要面向 Linux/Wayland/X11 等可把多套键鼠分配给不同用户或会话的环境。普通单用户桌面程序可以忽略它，但不应假设 `seatName()` 永远为空。

## 6. 常见坑与经验

不要手动删除从 `devices()` 或事件里取得的设备指针。它们通常由 Qt 平台层拥有。

不要把 `systemId()` 保存为跨平台、跨重启的永久身份。它是平台相关标识，设备重新连接或换系统后可能变化。

不要用 `type()` 推断全部能力。鼠标可能支持滚动，平板笔可能支持压力和倾斜，实际应以 `hasCapability()` 为准。

不要认为设备列表在每个平台都完整，也不要把热插拔事件支持当作统一行为。功能逻辑要能在“只有事件来源设备可见”的条件下正常工作。

## 7. 知识点覆盖

学习 `QInputDevice` 应覆盖设备类型、能力位标志、鼠标与触摸合成、触摸屏和触摸板区别、手写笔扩展数据、设备枚举、输入 seat、虚拟桌面映射、平台插件所有权和跨平台诊断。
