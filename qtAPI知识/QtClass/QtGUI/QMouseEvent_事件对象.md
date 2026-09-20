# QMouseEvent：一次鼠标输入的坐标、按键状态与来源

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QMouseEvent>`  
> 模块：`Qt6::Gui`  
> 继承链：`QEvent -> QInputEvent -> QPointerEvent -> QSinglePointEvent -> QMouseEvent`  
> 常用接收端：`QWidget`、`QGraphicsItem`、`QWindow`、事件过滤器

`QMouseEvent` 是 Qt 在鼠标按下、释放、双击和移动时派发的事件对象。它不负责“执行拖拽”或“点击按钮”，而是携带当前输入发生的位置、触发按键、仍按住的所有按键、键盘修饰键与设备信息，供接收者决定如何响应。

## 它解决的问题

鼠标交互需要同时回答几个不同的问题：

- 指针相对当前控件、窗口和屏幕分别在哪里？
- 本次事件由哪一个按钮触发？
- 此刻还有哪些按钮仍被按住？
- 是否同时按住了 Shift、Ctrl 或 Alt？
- 事件是实际鼠标输入还是由触摸板、系统或 Qt 合成？
- 当前控件处理不了时，父控件是否应当接手？

`QMouseEvent` 统一承载这些状态。常见使用场景包括选择、框选、拖动窗口、拖动画布、右键菜单、绘图工具、图表交互和自定义控件的点击命中测试。

## 在 QWidget 中处理事件

```cpp
#include <QMouseEvent>
#include <QWidget>

class Canvas : public QWidget
{
protected:
    void mousePressEvent(QMouseEvent *event) override
    {
        if (event->button() != Qt::LeftButton) {
            event->ignore();
            return;
        }

        m_dragStart = event->position();
        m_dragging = true;
        event->accept();
    }

    void mouseMoveEvent(QMouseEvent *event) override
    {
        if (!m_dragging || !(event->buttons() & Qt::LeftButton)) {
            event->ignore();
            return;
        }

        updateSelection(m_dragStart, event->position());
        event->accept();
    }

    void mouseReleaseEvent(QMouseEvent *event) override
    {
        if (event->button() == Qt::LeftButton && m_dragging) {
            m_dragging = false;
            finishSelection(event->position());
            event->accept();
            return;
        }

        event->ignore();
    }

private:
    QPointF m_dragStart;
    bool m_dragging = false;
};
```

`QMouseEvent *` 只在当前事件处理调用期间有效。不要把这个裸指针保存为成员、排入异步任务或跨线程传递；若之后还需要数据，复制 `position()`、`buttons()`、`modifiers()` 等值。

## `button()` 与 `buttons()`：单次触发和当前状态

这两个 API 的混淆是鼠标逻辑中最常见的错误。

| API | 回答的问题 | 典型结果 |
| --- | --- | --- |
| `button()` | “是哪一个按钮导致本次事件产生？” | 按下/释放/双击事件通常是 `LeftButton`、`RightButton` 等；`MouseMove` 必须是 `NoButton`。 |
| `buttons()` | “事件到达这一刻，有哪些按钮仍处于按下状态？” | 一个可组合的 `Qt::MouseButtons` 标志，例如同时含 `LeftButton` 与 `RightButton`。 |

因此，拖动中的 `mouseMoveEvent()` 必须看 `buttons()`：

```cpp
if (event->buttons() & Qt::LeftButton) {
    // 左键仍按住，继续拖动。
}
```

不要在移动事件里判断 `event->button() == Qt::LeftButton`，它会失败，因为移动事件的单次触发按钮是 `Qt::NoButton`。

键盘状态来自继承的 `modifiers()`：

```cpp
if ((event->modifiers() & Qt::ControlModifier)
    && (event->buttons() & Qt::LeftButton)) {
    // Ctrl + 左键拖动。
}
```

## 三套坐标：局部、窗口与全局

Qt 6 的浮点坐标 API 能避免高 DPI 下过早取整：

| API | 坐标系 | 用途 |
| --- | --- | --- |
| `position()` | 接收事件的 widget 或 item 局部坐标 | 命中测试、绘图、在控件内拖动。 |
| `scenePosition()` | 所在 window/scene 坐标 | 在窗口级布局、场景级转换或多层接收端之间传递位置。 |
| `globalPosition()` | 屏幕/桌面全局坐标 | 移动顶层窗口、跨控件拖动、显示弹出菜单。 |

旧的 `pos()`、`globalPos()`、`localPos()`、`windowPos()`、`screenPos()` 与整型 `x()`/`y()` 已在 Qt 6 中弃用或不应作为新代码入口。优先使用 `QPointF` 的新 API，到必须交给整型 API 时才调用 `toPoint()`。

移动控件本身时应从全局坐标计算增量。若在 `mouseMoveEvent()` 中一边移动 widget，一边使用相对 widget 的 `position()`，widget 原点变化会反过来改变下一次局部坐标，形成抖动。

```cpp
void FloatingPanel::mousePressEvent(QMouseEvent *event)
{
    if (event->button() == Qt::LeftButton)
        m_globalDragOffset = event->globalPosition() - frameGeometry().topLeft();
}

void FloatingPanel::mouseMoveEvent(QMouseEvent *event)
{
    if (event->buttons() & Qt::LeftButton)
        move((event->globalPosition() - m_globalDragOffset).toPoint());
}
```

## 移动事件、鼠标抓取与事件传播

在 `QWidget` 中：

- 默认只有在至少一个鼠标按钮按下时才会收到 `mouseMoveEvent()`。
- 调用 `setMouseTracking(true)` 后，即使没有按键按下，指针在控件上移动也会产生移动事件。
- 用户在控件内部按下某按钮后，Qt 会自动抓取鼠标；直到最后一个按下的鼠标按钮释放前，该控件会继续接收鼠标事件，即使光标离开了控件。

这一自动抓取正是拖拽通常不需要手动 `grabMouse()` 的原因。若逻辑在拖动中“突然中断”，先确认是否在 press 后改变了窗口状态、销毁了接收对象、显式释放抓取，或由原生窗口/平台抢走了输入。

事件有接受状态。无法处理的事件应调用 `ignore()`，使其继续向父 widget 链传播，直到某个父对象 `accept()` 或事件过滤器消耗它。若 widget 设置了 `Qt::WA_NoMousePropagation`，事件传播到该 widget 时不会再继续向上。

不要无条件吞掉所有按键。子控件只需要处理左键框选时，应 `ignore()` 未支持的右键或中键，这样父级容器仍可提供滚动、拖动或上下文菜单行为。

## 合成来源、设备与标志

`QMouseEvent` 也可由非传统鼠标设备或 Qt 合成。继承的 `pointingDevice()` 给出产生事件的 `QPointingDevice`；构造测试事件时可传入设备指针，省略时使用 `QPointingDevice::primaryPointingDevice()`。

`source()` 返回 `Qt::MouseEventSource`，可帮助诊断鼠标事件是否由系统或 Qt 从其他输入合成。`flags()` 返回 `Qt::MouseEventFlags`，携带额外事件信息，例如某些双击相关的标记。它们适合处理输入兼容性或调试，不应作为正常点击逻辑的首要判断条件。

使用事件过滤器时，仍遵守同样的生命周期和接受规则：

```cpp
bool InputFilter::eventFilter(QObject *watched, QEvent *event)
{
    if (event->type() != QEvent::MouseButtonPress)
        return QObject::eventFilter(watched, event);

    auto *mouseEvent = static_cast<QMouseEvent *>(event);
    if (mouseEvent->button() != Qt::RightButton)
        return false; // 未消费，交给原接收者。

    showContextMenu(mouseEvent->globalPosition().toPoint());
    return true;      // 已消费，原接收者不再处理。
}
```

只有已通过 `event->type()` 确认的情况下，才能把 `QEvent *` 转为 `QMouseEvent *`。

## 线程与合成事件边界

原生鼠标输入由 GUI 线程的事件循环派发。`QWidget`、`QWindow` 和 Qt Quick 项目的 UI 操作必须留在其所属 GUI 线程；不要从工作线程直接调用 `mousePressEvent()` 或将实际事件指针交给工作线程。

测试中可以构造 `QMouseEvent` 后用 `QCoreApplication::sendEvent()`/`postEvent()` 发送，但接收对象的线程归属、坐标真实性和事件类型仍需正确。构造的事件不会自动获得操作系统抓鼠标、窗口激活等外部副作用，不能把它当作完整的系统输入替身。

## 常见错误

1. **在移动事件检查 `button()`。** 移动事件的 `button()` 是 `NoButton`；检查 `buttons()`。
2. **拖动窗口时使用 `position()`。** 目标控件自身在移动，局部坐标会跳；使用 `globalPosition()`。
3. **未开启 mouse tracking 却期待悬停移动。** 调用 `setMouseTracking(true)`。
4. **保存 `QMouseEvent *`。** 事件处理结束后不再有效；复制所需字段。
5. **每个事件都 `accept()`。** 对未处理输入应 `ignore()`，保留父级传播机会。
6. **混用浮点与整型坐标。** 在高 DPI 和缩放场景中保留 `QPointF`，最后一步才取整。
7. **将 `mapRect()` 当作真实透视后的四边形。** 这不是 `QMouseEvent` 专有 API；若坐标经过复杂变换，分别映射指针点而不是猜测包围框。
8. **静态转换任意事件。** 必须先以 `QEvent::Type` 验证事件类型。

## API 速查表

| API | 作用 | 使用时的语义与边界 |
| --- | --- | --- |
| `QMouseEvent(type, localPos, globalPos, button, buttons, modifiers, device)` | 构造鼠标事件。 | `type` 只能是按下、释放、双击或移动；该重载将 window/scene 坐标视作局部坐标。 |
| `QMouseEvent(type, localPos, scenePos, globalPos, button, buttons, modifiers, device)` | 用完整三套坐标构造事件。 | 适合测试、转发或框架集成；传入坐标必须与接收者语义一致。 |
| `flags()` | 返回附加鼠标事件标志。 | 用于双击等额外信息和诊断；不替代 `button()`/`buttons()` 的常规判断。 |
| `source()` | 返回鼠标事件来源。 | 可区分真实或合成来源；不要将其作为所有平台上唯一可靠的输入分类依据。 |
| `button()` | 返回触发本次事件的单个按钮。 | `MouseMove` 返回 `Qt::NoButton`；按下、释放和双击用它识别主按钮。 |
| `buttons()` | 返回当前仍按下的全部鼠标按钮标志。 | 拖拽/移动判断用位与，例如 `buttons() & Qt::LeftButton`。 |
| `modifiers()` | 返回当前键盘修饰键。 | 继承自 `QInputEvent`；检查 Ctrl/Shift/Alt 时使用按位判断。 |
| `position()` | 返回接收端局部浮点坐标。 | 常规命中测试与控件内绘制首选；不要在移动该控件自身时作为拖动基准。 |
| `scenePosition()` | 返回窗口或场景坐标。 | 在窗口级或场景级空间中协调对象时使用。 |
| `globalPosition()` | 返回桌面/屏幕全局浮点坐标。 | 顶层窗口拖动、跨控件拖放和弹出菜单定位的首选。 |
| `pointingDevice()` | 返回产生事件的指针设备。 | 继承自 `QPointerEvent`；设备可能不是传统物理鼠标。 |
| `point()` / `points()` | 返回统一指针事件点数据。 | 继承接口；`QMouseEvent` 为单点事件，但使用它们可与触摸/笔输入建立统一处理层。 |
| `timestamp()` | 返回事件时间戳。 | 继承自 `QInputEvent`；用于速度或手势估算时处理时间回绕与事件合并。 |
| `accept()` / `ignore()` / `isAccepted()` | 管理事件接受状态。 | 未处理时 `ignore()` 可允许父 widget 链继续处理；过滤器返回 `true` 会直接消费事件。 |
| `type()` | 返回事件类型。 | 事件过滤器中先检查它，再 `static_cast<QMouseEvent *>`。 |
| `pos()`、`globalPos()`、`x()`、`y()` 等旧接口 | Qt 5 风格坐标访问。 | Qt 6 新代码避免使用；会丢失浮点精度或已被弃用。 |

## 一句话总结

处理 `QMouseEvent` 时，把“本次按钮”交给 `button()`，“拖动时仍按下哪些按钮”交给 `buttons()`；控件内交互用 `position()`，移动窗口或跨控件交互用 `globalPosition()`，未处理事件记得 `ignore()`。
