# Qt QEnterEvent 深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QEnterEvent>`  
> 所属模块：`Qt6::Gui`  
> 继承：`QEvent -> QSinglePointEvent -> QEnterEvent`  
> 定位：指针进入 widget 或窗口区域时的位置事件

## 1. 它解决什么问题

`QEnterEvent` 表示指针进入一个 widget 的可交互区域。它与 `QHoverEvent`、`QMouseEvent` 的职责不同：进入事件只描述“从外部进入”，适合启动悬停状态、显示提示或更新指针反馈，不应被当成一次鼠标按键。

实际场景：

- 自定义控件进入时显示 hover 边框；
- 根据进入位置预加载工具提示或局部预览；
- 图形编辑器进入某个图元区域时更新状态；
- 无鼠标按钮时启动悬停交互。

## 2. 事件入口与坐标

```cpp
void Canvas::enterEvent(QEnterEvent *event)
{
    setHovered(true);
    lastPointerPosition = event->position();
    QWidget::enterEvent(event);
}
```

`position()` 是接收对象局部坐标，`scenePosition()` 是窗口或场景坐标，`globalPosition()` 是屏幕全局坐标。三者必须根据接收对象和坐标系使用；不要把局部位置直接交给屏幕级 API。

Qt 6 使用 `QPointF` 位置，以保留高 DPI 和触控板的亚像素信息。旧的 `pos()`、`globalPos()`、`localPos()`、`windowPos()`、`screenPos()` 已弃用，应迁移到对应的新名称。

## 3. 它不是 hover 移动事件

`QEnterEvent` 通常只在跨越边界时到达。要在控件内部持续跟踪指针，应启用 mouse tracking 并处理 `QMouseEvent`，或启用 hover events 后处理 `QHoverEvent`。

它也不携带按钮按下语义。若需要“按住鼠标进入”或判断当前按钮，使用相应的鼠标事件状态，不要从 `QEnterEvent` 推断。

## 4. 生命周期与设备边界

事件对象只在 `enterEvent()` 调用期间有效。需要延后处理时复制位置值和必要状态，不要保存 `QEnterEvent *`。

触控、触笔或平台合成指针可能使用非鼠标的 `QPointingDevice`。`device()` 可以帮助识别设备，但不应假定每次 enter 都来自传统鼠标。

## 5. 常见错误

- 在 `QEnterEvent` 中读取鼠标按钮并据此执行业务；
- 把 enter 当作连续移动；
- 用 `globalPosition()` 做局部命中测试；
- 保存事件指针到定时器或异步任务；
- 继续使用已弃用的整数坐标接口而丢失精度。

## 6. 逐项 API 说明

### `QEnterEvent(...)`

```cpp
QEnterEvent(const QPointF &localPos,
            const QPointF &scenePos,
            const QPointF &globalPos,
            const QPointingDevice *device =
                QPointingDevice::primaryPointingDevice())
```

创建一个进入事件，主要用于测试或自定义事件注入。三个位置必须分别属于局部、场景/窗口和全局坐标系；`device` 描述指针设备，默认是主指针设备。普通程序不应依赖手动构造来模拟完整平台输入。

### 从 `QSinglePointEvent` 继承的现代坐标 API

| API | 作用 | 关键边界 |
| --- | --- | --- |
| `position() const` | 获取接收对象局部位置。 | 用于控件内命中测试。 |
| `scenePosition() const` | 获取窗口或场景坐标。 | 具体含义取决于事件接收层级。 |
| `globalPosition() const` | 获取屏幕全局位置。 | 用于屏幕级定位。 |
| `device() const` | 获取指针设备。 | 可能是鼠标、触控笔或其他设备。 |

### 兼容接口

| API | 作用 | 关键边界 |
| --- | --- | --- |
| `pos()` / `localPos()` | 获取局部位置。 | Qt 6 已弃用，使用 `position()`。 |
| `globalPos()` / `screenPos()` | 获取全局位置。 | Qt 6 已弃用，使用 `globalPosition()`。 |
| `windowPos()` | 获取场景或窗口位置。 | Qt 6 已弃用，使用 `scenePosition()`。 |
| `x()` / `y()` / `globalX()` / `globalY()` | 获取取整坐标分量。 | 已弃用且会丢失小数精度。 |

### 从 `QEvent` 继承

| API | 作用 | 关键边界 |
| --- | --- | --- |
| `accept()` / `ignore()` | 设置事件处理状态。 | 通常由 widget 事件流程决定。 |
| `isAccepted()` | 查询接受状态。 | 不表示 hover 是否开启。 |
| `type()` | 查询事件类型。 | 正常应为 `QEvent::Enter`。 |

## API 速查表

| 类别 | API | 解决什么问题 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造 | `QEnterEvent(localPos, scenePos, globalPos, device)` | 创建进入事件。 | 主要用于测试，三个坐标系要对应。 |
| 坐标 | `position()` | 获取局部坐标。 | Qt 6 推荐；用于局部命中。 |
| 坐标 | `scenePosition()` | 获取窗口或场景坐标。 | 不等同于屏幕坐标。 |
| 坐标 | `globalPosition()` | 获取屏幕坐标。 | 屏幕级定位使用。 |
| 设备 | `device()` | 识别指针设备。 | 不要假定必然是鼠标。 |
| 兼容 | `pos()` 等旧接口 | 兼容旧代码。 | 已弃用，可能丢失精度。 |
| 状态 | `accept()` / `ignore()` | 控制事件处理状态。 | 不表示连续 hover 追踪。 |

---

### 一句话总结

`QEnterEvent` 只回答“指针刚进入哪里、来自哪个设备”；连续移动和按钮语义应交给 hover 或鼠标事件处理。
