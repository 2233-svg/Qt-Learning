# Qt QHoverEvent 深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QHoverEvent>`  
> 所属模块：`Qt6::Gui`  
> 继承：`QEvent -> QPointerEvent -> QSinglePointEvent -> QHoverEvent`  
> 定位：鼠标指针悬停进入、离开或移动时的位置事件

## 1. 它解决什么问题

`QHoverEvent` 用于没有按键动作的鼠标悬停交互。收到事件的 widget 开启 `Qt::WA_Hover` 属性后，可以通过 `HoverEnter`、`HoverMove`、`HoverLeave` 更新边框、图元高亮、预览和局部帮助。

它与 `QMouseEvent` 的关键区别是：hover 关注悬停状态而不是按钮按下；`HoverMove` 的传播规则也不同，事件会一直向顶层传播，是否 `accept()` 不会阻止这一传播，只有 `Qt::WA_NoMousePropagation` 才会停止。

常见场景：

- 自绘列表项或画布的悬停高亮；
- 进入/离开时触发局部 `update()`；
- 无需鼠标按下也显示可操作区域；
- 在深层子控件中让祖先了解指针悬停。

## 2. 启用与事件入口

```cpp
#include <QHoverEvent>
#include <QWidget>

class Swatch : public QWidget
{
public:
    Swatch()
    {
        setAttribute(Qt::WA_Hover, true);
    }

protected:
    bool event(QEvent *event) override
    {
        if (event->type() == QEvent::HoverEnter
            || event->type() == QEvent::HoverMove
            || event->type() == QEvent::HoverLeave) {
            auto *hover = static_cast<QHoverEvent *>(event);
            updateHover(hover->position(), hover->oldPosF());
            update();
            return true;
        }
        return QWidget::event(event);
    }
};
```

没有 `Qt::WA_Hover` 时，widget 默认不会收到这组 hover 事件。只启用 mouse tracking 不等于启用 hover；两者可配合使用，但各自有不同的事件模型。

## 3. 三种事件类型

| 类型 | 含义 | 位置注意事项 |
| --- | --- | --- |
| `QEvent::HoverEnter` | 指针进入 widget。 | `oldPos()` / `oldPosF()` 固定为 `(-1, -1)`。 |
| `QEvent::HoverMove` | 指针在 widget 内移动。 | 可用当前与旧位置计算局部增量。 |
| `QEvent::HoverLeave` | 指针离开 widget。 | 用于清除悬停状态；不要假设仍有有效命中对象。 |

`HoverEnter` 与 `HoverLeave` 的事件处理路径会触发 `update()`，因此适合在视觉状态变化时重绘。不要依赖“接受事件后祖先就不会再收到 hover”；传播规则与普通鼠标移动不同。

## 4. 坐标和历史位置

现代 API 来自 `QSinglePointEvent`：

- `position()`：相对于接收 widget 的当前位置；
- `scenePosition()`：相对于接收窗口或场景；
- `globalPosition()`：屏幕或虚拟桌面坐标；
- `device()`：产生事件的指针设备。

`oldPosF()` 和 `oldPos()` 表示相对于接收 widget 的上一个位置。没有前一位置时，旧位置通常等于当前位置；但 `HoverEnter` 的旧位置固定是 `(-1, -1)`，所以进入事件不能直接用 `position() - oldPosF()` 当作真实位移。

`oldPos()` 返回整数值，`oldPosF()` 保留浮点精度。Qt 6 新代码优先使用 `position()` 和 `oldPosF()`。

## 5. 传播与性能

在嵌套 A -> B -> C 的 widgets 中，指针进入 C 时，hover 移动事件可同时沿路径传到 C、B、A。即使子控件接受事件，祖先仍可能收到它；需要停止向上传播时设置 `Qt::WA_NoMousePropagation`。

hover 移动频率很高。事件中应只更新必要状态和脏区域，不要进行文件 I/O、网络请求或大规模布局重算。昂贵预览可以做节流，真正的业务操作应留给点击、拖放或明确命令。

## 6. 生命周期与设备边界

事件对象只在同步处理期间有效。需要延后使用时复制当前位置、旧位置和修饰键等值。

`QHoverEvent` 主要描述鼠标悬停，但构造函数仍接受 `QPointingDevice`，用于统一 Qt 指针事件体系。不要假设所有平台和所有输入设备都会提供同等 hover 能力。

## 7. 常见错误

- 忘记设置 `Qt::WA_Hover`；
- 把 mouse tracking 与 hover 当成同一种机制；
- 以为 `accept()` 能阻止 hover 向祖先传播；
- 在 `HoverEnter` 中把 `oldPosF()` 当作真实上一帧位置；
- 使用 `oldPos()` 丢失高 DPI 浮点精度；
- 每次 `HoverMove` 执行昂贵计算；
- 保存事件指针到定时器或异步任务。

## 8. 逐项 API 说明

### `QHoverEvent(...)`

```cpp
QHoverEvent(QEvent::Type type,
            const QPointF &scenePos,
            const QPointF &globalPos,
            const QPointF &oldPos,
            Qt::KeyboardModifiers modifiers = Qt::NoModifier,
            const QPointingDevice *device =
                QPointingDevice::primaryPointingDevice())
```

构造 hover 事件。`type` 必须是 `HoverEnter`、`HoverLeave` 或 `HoverMove`；`scenePos` 是接收窗口或场景坐标，`globalPos` 是绝对坐标，`oldPos` 是此前的窗口/场景位置。正常应用主要在测试时手动构造。

旧的只传局部 `pos`、`oldPos` 的构造函数从 Qt 6.3 起弃用。

### 本类 API

| API | 作用 | 关键边界 |
| --- | --- | --- |
| `QPoint oldPos() const` | 返回旧的局部整数位置。 | `HoverEnter` 固定为 `(-1, -1)`；会丢失小数精度。 |
| `QPointF oldPosF() const` | 返回旧的局部浮点位置。 | Qt 6 新代码优先使用；无旧位置时可等于当前位置。 |
| `bool isUpdateEvent() const` | 标识该事件属于更新事件。 | 不代表一定是 `HoverMove`，仍以 `type()` 区分。 |

### 从 `QSinglePointEvent` 继承

| API | 作用 | 关键边界 |
| --- | --- | --- |
| `position()` | 读取当前局部位置。 | 用于 widget 内命中测试。 |
| `scenePosition()` | 读取窗口或场景位置。 | 参考空间取决于接收层。 |
| `globalPosition()` | 读取屏幕位置。 | 用于跨窗口或屏幕级定位。 |
| `device()` | 读取指针设备。 | 平台能力可能不同。 |
| `modifiers()` | 读取触发时修饰键。 | 是事件快照。 |

## API 速查表

| 类别 | API | 解决什么问题 | 使用时重点注意 |
| --- | --- | --- | --- |
| 启用 | `setAttribute(Qt::WA_Hover, true)` | 让 widget 接收 hover 事件。 | mouse tracking 不能替代它。 |
| 类型 | `HoverEnter` / `HoverMove` / `HoverLeave` | 区分进入、移动、离开。 | `HoverEnter` 的旧位置为 `(-1, -1)`。 |
| 位置 | `position()` | 获取当前局部位置。 | 用于本地命中测试。 |
| 历史 | `oldPosF()` | 获取上一次局部位置。 | 计算增量时先排除 Enter。 |
| 兼容 | `oldPos()` | 获取整数旧位置。 | 会丢失浮点精度。 |
| 坐标 | `scenePosition()` / `globalPosition()` | 获取更高层坐标。 | 不要混用不同坐标系。 |
| 传播 | `Qt::WA_NoMousePropagation` | 阻止 hover 向祖先传播。 | `accept()` 本身不会阻止。 |
| 性能 | `update()` | 请求重绘悬停视觉。 | 高频事件只更新必要区域。 |

---

### 一句话总结

`QHoverEvent` 管理无按键的悬停交互：先启用 `WA_Hover`，用浮点位置更新局部反馈，并记住它会忽略接受状态继续向祖先传播。
