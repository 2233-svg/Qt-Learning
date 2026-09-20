# QNativeGestureEvent：系统触控板手势的增量事件

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QNativeGestureEvent>`  
> 模块：`Qt6::Gui`  
> 继承链：`QEvent -> QInputEvent -> QPointerEvent -> QSinglePointEvent -> QNativeGestureEvent`  
> Qt 版本：`delta()`、`fingerCount()` 与当前构造函数自 Qt 6.2 提供

`QNativeGestureEvent` 表示操作系统原生识别出的触控板手势，例如捏合缩放、旋转、三指平移、轻扫和智能缩放。它不是 `QGestureEvent` 的替代品：前者传递平台提供的高层原生增量，后者服务于 Qt 的手势框架与手势识别器。

## 它解决的问题

触控板输入不是简单的“多个鼠标点”。操作系统会将手指轨迹解释为缩放、旋转或平移，并把解释后的增量交给应用。`QNativeGestureEvent` 让画布、图片查看器、地图和 CAD 类界面能直接使用这些平台手势：

- 两指捏合缩放内容。
- 两指旋转图片或画布。
- 三指及以上手势平移视口。
- 对 Smart Zoom 或 Swipe 做平台风格的快捷操作。

手势类型和可用性取决于操作系统、桌面环境、驱动和用户设置。应用应提供鼠标滚轮、快捷键或触屏手势等替代交互，不能假定每台机器都会产生相同事件。

## 事件流与类型语义

原生手势通常以 `BeginNativeGesture` 开始、以 `EndNativeGesture` 结束。中间可交错出现不同类型的事件：一次两指捏合可能同时产生 Zoom 和 Rotate，平台也可能夹杂 Pan。不要把一个 begin/end 区间简单视为“只会有一种手势”。

| `gestureType()` | `value()` / `delta()` 的意义 | 常见平台输入 |
| --- | --- | --- |
| `ZoomNativeGesture` | `value()` 是本次缩放增量，通常远小于 1。 | macOS、Wayland 的两指捏合。 |
| `RotateNativeGesture` | `value()` 是本次旋转角度增量，单位为度。 | macOS、Wayland 的两指旋转。 |
| `PanNativeGesture` | `delta()` 是本次平移距离，单位为像素。 | Wayland 上通常为三指及以上共同移动。 |
| `SwipeNativeGesture` | `value()` 是轻扫角度，单位为度。 | macOS，受触控板设置影响。 |
| `SmartZoomNativeGesture` | 表示布尔式智能缩放状态。 | macOS 双击类手势。 |
| `BeginNativeGesture` / `EndNativeGesture` | 标记一组原生手势流的边界。 | 可以开始/结束事务、撤销分组或惯性状态。 |

触控板双指同向滑动通常保留给滚动。此类输入 Qt 通常派发 `QWheelEvent`，而不是 `PanNativeGesture`。完整的画布导航应同时实现 wheel/pixel delta 路径。

## 正确地应用增量

`value()` 和 `delta()` 表示“相对于上一事件的变化”，不是从手势开始累计到当前的绝对值。缩放要连乘，旋转要累加，平移要累加：

```cpp
bool Canvas::event(QEvent *event)
{
    if (event->type() != QEvent::NativeGesture)
        return QWidget::event(event);

    auto *gesture = static_cast<QNativeGestureEvent *>(event);

    switch (gesture->gestureType()) {
    case Qt::ZoomNativeGesture:
        m_scale *= 1.0 + gesture->value();
        m_scale = std::clamp(m_scale, 0.1, 16.0);
        update();
        return true;

    case Qt::RotateNativeGesture:
        m_rotationDegrees += gesture->value();
        update();
        return true;

    case Qt::PanNativeGesture:
        m_panOffset += gesture->delta();
        update();
        return true;

    case Qt::SmartZoomNativeGesture:
        toggleFitToView();
        return true;

    default:
        return QWidget::event(event);
    }
}
```

对于缩放，Qt 文档给出的常用更新方式是 `scale = scale * (1 + value)`。不要写成 `scale = value`，否则每个增量事件都会把现有缩放状态覆盖掉。

平移方向取决于你的 UI 语义：移动“内容”与移动“相机/视口”通常方向相反。先在一个固定坐标模型中定义 `m_panOffset` 的含义，再决定是否对 `delta()` 取负，避免不同输入设备方向不一致。

## 坐标与设备信息

和其他单点指针事件一样，手势附带三套浮点坐标：

| API | 坐标系 | 典型用途 |
| --- | --- | --- |
| `position()` | 接收 widget 或 item 的局部坐标 | 以手势中心为锚点缩放、旋转。 |
| `scenePosition()` | window/scene 坐标 | 场景或窗口级转换。 |
| `globalPosition()` | 屏幕/桌面坐标 | 顶层浮层、跨窗口交互和诊断。 |
| `pointingDevice()` | 产生事件的输入设备 | 按设备类型或能力做日志和兼容性处理。 |
| `fingerCount()` | 参与手势的手指数。 | 仅在已知时有效； Begin/End 常返回 0。 |

`fingerCount()` 是辅助信息，不是交互正确性的唯一条件。平台可能无法报告准确手指数；尤其 Begin/End 事件中，`0` 通常只表示未知，不表示“没有手指”。

## 与 QWheelEvent、QGestureEvent 的选择

| 需求 | 应优先处理的类型 |
| --- | --- |
| 鼠标滚轮与触控板双指滚动 | `QWheelEvent`，优先使用 `pixelDelta()`。 |
| 系统原生的捏合、旋转、平移增量 | `QNativeGestureEvent`。 |
| 使用 Qt 手势识别器并处理 `QPinchGesture`、`QPanGesture` | `QGestureEvent`。 |
| 原始多触点、笔或触摸屏输入 | `QTouchEvent`、`QTabletEvent` 或通用 `QPointerEvent` API。 |

不要在同一个手势上无条件同时处理 `QWheelEvent`、`QNativeGestureEvent` 和 `QGestureEvent`，否则一次输入可能缩放或平移多次。确定组件的手势策略后，对已经消费的事件返回已处理结果。

## 生命周期、线程与测试

系统输入事件由接收对象所属线程的事件循环派发，GUI widget 中通常就是 GUI 线程。`QNativeGestureEvent *` 只在当前 `event()` 或事件过滤器调用中可用；需要异步处理时复制 `gestureType()`、坐标、`value()`、`delta()` 与手指数。

测试可以使用 Qt 6.2 引入的构造函数创建事件并发送给目标对象，但这仅验证应用的分支逻辑。真实平台会决定手势类型、序列边界、可用手指数和数值粒度，特别是 Wayland/macOS 之外的环境不应假设完全相同的行为。

`delta()` 的内部存储使用单精度数据，因此读回的 `QPointF` 可能与构造时的值有微小差异。测试浮点值时使用容差，而不是精确相等。

## 常见错误

1. **把 `value()` 当作总缩放比例。** 它通常是增量；缩放应做连乘更新。
2. **把 `delta()` 当作全局位置。** 它是相邻事件之间的像素位移，手势锚点看 `position()`。
3. **期待双指滑动产生 Pan。** 两指滑动通常是 `QWheelEvent` 滚动。
4. **假定一段 begin/end 中只有 Zoom。** Zoom、Rotate 与 Pan 可能交错。
5. **用 `fingerCount() == 0` 丢弃 Begin/End。** 0 常表示未知，不是无效事件。
6. **强制将 Smart Zoom 作为普通倍率。** 它是平台级布尔式动作，应定义明确的应用行为。
7. **在未验证类型的情况下强转 `QEvent *`。** 先检查 `QEvent::NativeGesture`。
8. **保存事件裸指针或跨线程处理。** 只复制所需数据，并在 GUI 线程更新 UI。

## API 速查表

| API | 作用 | 使用时的语义与边界 |
| --- | --- | --- |
| `QNativeGestureEvent(type, device, fingerCount, localPos, scenePos, globalPos, value, delta, sequenceId)` | 构造原生手势事件。 | Qt 6.2 起提供，主要用于测试或框架集成；坐标与数值必须遵循类型语义。 |
| `gestureType()` | 返回 `Qt::NativeGestureType`。 | 先按类型解释 `value()`/`delta()`；不要将所有手势当作缩放。 |
| `value()` | 返回与手势相关的标量增量。 | Zoom 为缩放增量，Rotate/Swipe 为角度增量；不是统一单位也不是累计值。 |
| `delta()` | 返回相邻事件之间的二维像素位移。 | Qt 6.2 起提供；Pan 用它移动内容或视口；内部单精度导致可能存在微小误差。 |
| `fingerCount()` | 返回参与手势的手指数。 | Qt 6.2 起提供；未知时返回 0，Begin/End 常见此情况。 |
| `position()` | 返回接收端局部手势中心。 | 用于以手势中心作为缩放或旋转锚点。 |
| `scenePosition()` | 返回 window/scene 坐标。 | 跨 item 或窗口级变换时使用。 |
| `globalPosition()` | 返回屏幕全局坐标。 | 跨窗口交互与调试使用；不是 Pan 位移。 |
| `pointingDevice()` | 返回产生手势的设备。 | 可用于输入兼容性策略或日志；不应假定一定是某个固定设备类别。 |
| `timestamp()` | 返回事件时间戳。 | 用于速度、惯性或事件分析时处理时间精度与平台差异。 |
| `type()` / `accept()` / `ignore()` | 查询和管理事件处理状态。 | 过滤器中先检查 `QEvent::NativeGesture`；已处理则消费，未处理交给基类/其他机制。 |

## 一句话总结

`QNativeGestureEvent` 是平台手势的增量流：按 `gestureType()` 分支，缩放连乘、旋转累加、平移累加；两指滚动仍由 `QWheelEvent` 处理，且所有手势都应有跨平台替代交互。
