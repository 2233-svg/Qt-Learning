# QInputEvent：用户输入的共同上下文

> Qt 版本：6.11.1  
> 模块：`Qt6::Gui`  
> 头文件：`#include <QInputEvent>`  
> 继承：`QEvent`

## 它解决什么问题

`QInputEvent` 是键盘、鼠标、滚轮、触摸、平板笔和原生手势等用户输入事件的共同基类。它不描述具体坐标、按键或触点，而是统一保存三类跨事件上下文：

- 输入来自哪个 `QInputDevice`；
- 事件发生前有哪些键盘修饰键；
- 窗口系统给出的事件时间戳。

实际事件处理通常接到的是 `QKeyEvent`、`QMouseEvent`、`QWheelEvent`、`QPointerEvent`、`QTabletEvent` 等派生类。直接把它当作可分发的“通用事件”意义有限；它的价值是让通用过滤器、手势框架和跨设备逻辑能够读取统一上下文。

## 实际使用场景

- 事件过滤器记录任何用户输入的来源设备、修饰键和时序。
- 同一输入处理函数根据 `device()` 区分真实鼠标与由触摸合成的鼠标事件。
- 快捷键、拖拽、多选逻辑读取本次事件的 modifier 快照。
- 手写或触摸输入分析使用时间戳计算相邻事件的时间间隔。
- 测试或受控合成事件环境按需要设置 modifier 和 timestamp。

## 修饰键是“发生前”快照

`modifiers()` 返回事件发生**紧前一刻**已有的 `Qt::KeyboardModifiers`。它应是处理单个事件时判断 Shift、Ctrl、Alt、Meta 的首选来源。

```cpp
void ListView::mousePressEvent(QMouseEvent *event)
{
    if (event->modifiers().testFlag(Qt::ControlModifier)) {
        toggleSelectionAt(event->position());
    } else {
        selectOnly(event->position());
    }
}
```

不要用 `QGuiApplication::keyboardModifiers()` 替代事件自己的 modifiers：后者是调用当下的全局状态，事件经过队列延迟后用户可能已松开或按下另一枚键。特别是对“按下 Ctrl 的瞬间”或“释放 Ctrl 的事件”，事件快照与当前全局状态可能不同。

## device() 保留原始来源，连合成事件也是如此

`device()` 返回产生原始事件的 `QInputDevice`。Qt 6 中，如果触摸事件被合成为鼠标事件，`device()` 仍指向触摸屏，而不伪装成鼠标。这使业务代码能区分“真实鼠标点击”和“触摸模拟的点击”。

```cpp
void Canvas::mousePressEvent(QMouseEvent *event)
{
    const QInputDevice *device = event->device();
    const bool synthesizedFromTouch =
        device && device->type() != QInputDevice::DeviceType::Mouse;

    beginStroke(event->position(), synthesizedFromTouch);
}
```

`deviceType()` 是 `device()->type()` 的安全便捷查询；当 device 指针为空时返回 `QInputDevice::DeviceType::Unknown`。更细的能力，例如 pressure、tilt、pixel scroll，不应只靠 type 判断，而应读取具体 device 的 `hasCapability()`。

返回的设备指针由 Qt/平台管理，不属于事件接收者。事件处理期间可读取它，不能删除或把它当成应用私有对象重新管理。

## 时间戳适合看相对时序，不是日期时间

`timestamp()` 是窗口系统的时间戳，通常是“自某个任意起点以来的毫秒数”，例如系统启动后经过的时间。它适合：

- 判断两个输入事件的先后和间隔；
- 计算手势速度或长按时长；
- 在同一事件流中做超时判断。

它不是 Unix epoch，不对应本地日期时间，也不承诺可在不同进程、不同平台后端或系统重启之间比较。数值为 0 时也不应假定它是当前时间；某些合成或测试事件可能没有原生窗口系统时间戳。

```cpp
if (lastTimestamp != 0 && event->timestamp() > lastTimestamp) {
    const quint64 elapsedMs = event->timestamp() - lastTimestamp;
    updateGestureTiming(elapsedMs);
}
lastTimestamp = event->timestamp();
```

计算差值时要处理无序、缺失或平台时间戳回绕的情况，不要把无符号相减直接解释为任意可靠的巨大时长。

## 事件对象的生命周期与修改

Qt 将事件对象交给目标对象、事件过滤器和可能的父级传播链处理。普通处理函数只能在调用期间使用指针；异步任务应复制自己需要的数据，例如位置、modifier、timestamp，而不是保存 `QInputEvent *`。

`setModifiers()` 和 `setTimestamp()` 是公共 API，主要服务于 Qt 内部、事件派生类和受控的合成/测试场景。对已投递的真实事件随意修改，会让后续过滤器或接收者看到与平台输入不一致的状态。应用层通常只读；若确需人工构造事件，应明确目标事件类型、设备寿命和事件接收者，并理解它不能复现完整平台输入状态机。

接受状态、事件类型、spontaneous 标记等行为继承自 `QEvent`。`accept()` / `ignore()` 表示该接收者是否处理当前事件，并不改变 `modifiers()`、设备来源或平台时间戳。

## 常见错误

- 用 `QGuiApplication::keyboardModifiers()` 判断历史事件，而不是 `event->modifiers()`。
- 把触摸合成的鼠标事件当作真实鼠标，导致触摸和鼠标路径的业务逻辑混乱。
- 以为 `timestamp()` 是可格式化为日期的 Unix 时间。
- 跨应用、跨后端或重启后比较两个窗口系统时间戳。
- 缓存事件指针给异步逻辑使用。
- 只凭 `deviceType()` 读取压感、倾斜或像素滚动，未检查能力。
- 在 event filter 中改写 delivered event 的 modifier/timestamp，却没有控制后续接收者语义。
- 用一个手工构造的基类 `QInputEvent` 期待模拟完整鼠标、触摸或键盘交互。

## API 速查表

| 类别 | API | 语义与边界 |
| --- | --- | --- |
| 构造 | `explicit QInputEvent(QEvent::Type, const QInputDevice *, Qt::KeyboardModifiers = Qt::NoModifier)` | 构造带类型、来源设备和 modifier 的输入基类事件；普通应用通常处理派生事件，而非直接投递它。 |
| 来源 | `device() const` | 返回原始来源设备。合成鼠标事件仍可返回原触摸设备，用于判断是否真实鼠标输入。 |
| 来源 | `deviceType() const` | 返回来源设备类型；device 为空时返回 `Unknown`，不能代替 capability 检查。 |
| 修饰键 | `modifiers() const` | 返回事件发生前的修饰键快照；处理历史事件时比全局键盘状态可靠。 |
| 修饰键 | `setModifiers(Qt::KeyboardModifiers)` | 修改事件携带的修饰键；主要用于受控合成/测试，避免更改真实已投递事件。 |
| 时序 | `timestamp() const` | 返回窗口系统时间戳，通常是任意起点后的毫秒数；只适合同一事件流的相对时序。 |
| 时序 | `virtual setTimestamp(quint64)` | 设置时间戳；派生事件可重写，应用层只应在明确的合成/测试场景使用。 |
| 继承 | `type()` | 从 `QEvent` 查询具体事件类型，实际通常是键盘、鼠标、触摸等派生类型。 |
| 继承 | `accept()` / `ignore()` / `isAccepted()` | 管理本次事件处理状态；不影响设备、修饰键和时间戳的原始语义。 |
| 继承 | `spontaneous()` | 查询是否由系统自然产生；手动 `sendEvent()` 的事件通常不具备相同的原生输入语义。 |

## 相关类

- `QInputDevice`：输入设备类别、能力、seat 和平台 ID。
- `QKeyEvent`：按键、文本与自动重复信息。
- `QMouseEvent`：鼠标或由其他设备合成的点输入。
- `QPointerEvent` / `QEventPoint`：多点输入、位置、速度、压力等细节。
- `QGuiApplication`：提供全局键盘 modifier，但其时间点不同于事件快照。

`QInputEvent` 提供的是“这次输入当时从哪里来、当时按着什么、何时发生”的上下文。把这些信息与具体派生事件的坐标和按钮数据结合，输入逻辑才能既准确又不把合成事件误判为真实硬件行为。
