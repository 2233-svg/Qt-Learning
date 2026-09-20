# QWheelEvent：滚轮与触控板滚动事件

> 适用版本：Qt 6.11.1
> 头文件：`#include <QWheelEvent>`
> 所属模块：`Qt6::Gui`
> 继承：`QSinglePointEvent -> QPointerEvent -> QInputEvent -> QEvent`

## 它解决什么问题

`QWheelEvent` 把鼠标滚轮、触控板滚动和部分平台生成的滚动手势统一为一个输入事件。它同时提供指针位置、滚动增量、修饰键、当前按键、滚动阶段、滚动方向和事件来源，控件可以据此实现列表滚动、缩放、时间轴平移或画布导航。

Qt 6 中滚动已经不应只按“每次滚动固定几行”处理。精细触控板通常给出像素增量和连续 phase，传统鼠标滚轮更常只有角度增量，因此处理代码需要根据设备能力选择数据源。

## 实际使用场景

- `QAbstractScrollArea` 子类处理列表、画布或时间线滚动。
- 按 `Ctrl` + 滚轮缩放图片、图表或编辑器。
- 在自定义视图中支持触控板的平滑滚动和惯性滚动。
- 根据 `source()` 区分真实硬件输入与 Qt 合成事件。

## 增量、单位与方向

优先使用 `pixelDelta()`。当它不是空点时，它表示更适合直接用于内容位移的屏幕像素增量；传统鼠标常没有这个值，此时使用 `angleDelta()`。`angleDelta()` 的单位是度的八分之一，`DefaultDeltasPerStep` 为 `120`，也就是通常的一格滚轮约为 15 度。

不要假设 `angleDelta()` 一定能被 120 整除，也不要把它直接当像素。高分辨率滚轮和触控板可能产生小于一个传统 step 的增量，应用可以累积余数后再转换为离散行数，或直接实现连续位移。

`inverted()` 表示平台报告的滚动方向是否相对于常规内容滚动方向反转。它不是“用户是否按住反向快捷键”的状态；当平台无法提供可靠信息时，值可能没有设备级别的区分能力。

## 滚动阶段与事件处理

`phase()` 可以表示开始、更新、结束和动量阶段。开始或结束事件可能没有实际位移，不能只用 `pixelDelta().isNull()` 判断整个手势是否无效。使用 `isBeginEvent()`、`isUpdateEvent()` 和 `isEndEvent()` 可避免直接比较枚举时遗漏平台行为。

在 `wheelEvent()` 中，如果控件消费了滚动，应调用 `accept()`；需要让父控件或默认滚动区域继续处理时调用 `ignore()`。事件传播取决于接受状态和控件层级，不能通过“总是接受”来实现所有嵌套滚动场景。

## 关键边界

- `position()` 和 `globalPosition()` 是浮点坐标；不要依赖 Qt 5 时代的整数坐标接口。
- `pixelDelta()` 为空很常见，应准备 `angleDelta()` fallback。
- 两个方向的增量都可能非零；同时处理水平和垂直滚动，不能只读取 `y()`。
- 通过 `inverted()` 反转自定义滚动时，要明确内容坐标系的正方向，避免和 Qt 默认滚动区域重复反转。
- `QWheelEvent` 是瞬时事件对象。异步任务只保存复制后的数值，不保存事件指针。

## API 速查表

| API | 作用 | 重点注意 |
| --- | --- | --- |
| `QWheelEvent(...)` | 创建滚动事件，设置局部/全局位置、像素增量、角度增量、按键、修饰键、phase、方向和来源。 | 构造参数中的增量单位不同；`angleDelta` 不是像素。 |
| `QPoint pixelDelta() const` | 返回像素级滚动增量。 | 触控板更常提供；为空时必须 fallback。 |
| `QPoint angleDelta() const` | 返回八分之一度单位的滚动增量。 | 常见一格为 `120`；不要无条件转成一个固定像素值。 |
| `static constexpr int DefaultDeltasPerStep` | 传统滚轮每个 step 的默认角度增量，值为 `120`。 | 只是换算参考，不代表每个设备都按此步进。 |
| `Qt::ScrollPhase phase() const` | 返回当前滚动手势阶段。 | Begin/End 事件可能没有位移。 |
| `bool isBeginEvent() const` | 判断是否为滚动开始事件。 | 适合初始化惯性或拖动状态。 |
| `bool isUpdateEvent() const` | 判断是否为滚动更新事件。 | 通常在这里应用增量。 |
| `bool isEndEvent() const` | 判断是否为滚动结束事件。 | 适合清理手势状态；不要假设结束事件有 delta。 |
| `bool hasPixelDelta() const` | 判断 `pixelDelta()` 是否非空。 | 不能据此判断事件是否有意义，phase 事件仍可能无 delta。 |
| `bool inverted() const` | 返回平台报告的反向滚动标志。 | 用于统一自定义内容方向，避免重复反转。 |
| `bool isInverted() const` | `inverted()` 的同义接口。 | 新代码可选用语义更直观的名称。 |
| `Qt::MouseEventSource source() const` | 返回硬件、触摸板或合成事件来源。 | 只在确实需要区分输入来源时使用。 |
| `QPointF position() const` | 返回窗口/控件局部浮点位置。 | 高 DPI 和缩放场景不要过早转整数。 |
| `QPointF globalPosition() const` | 返回屏幕全局浮点位置。 | 跨窗口拖动或定位菜单时使用。 |
| `Qt::MouseButtons buttons() const` | 返回事件发生时处于按下状态的鼠标按钮集合。 | 它是位标志集合，不等于单个按钮。 |
| `Qt::KeyboardModifiers modifiers() const` | 返回事件发生时的键盘修饰键。 | 缩放等模式切换应读取事件快照。 |
| `const QPointingDevice *pointingDevice() const` | 返回产生事件的指针设备。 | 只读取设备信息，不要取得其所有权。 |
| `void accept()` / `void ignore()` | 控制事件是否由当前对象消费。 | 嵌套滚动和父控件回退依赖接受状态。 |

## 一句话总结

处理滚动时先取 `pixelDelta()`，没有再用 `angleDelta()`；同时关注 phase、方向和事件接受状态，才能兼容鼠标滚轮与触控板。
