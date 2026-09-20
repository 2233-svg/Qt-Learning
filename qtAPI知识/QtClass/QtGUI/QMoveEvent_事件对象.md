# QMoveEvent：控件位置变更的前后坐标

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QMoveEvent>`  
> 模块：`Qt6::Gui`  
> 继承：`QEvent`  
> 常用接收端：`QWidget::moveEvent()`

`QMoveEvent` 是 widget 改变位置后收到的通知事件。它只报告位置从哪里变到哪里，不包含鼠标状态、移动原因或窗口管理器的完整几何信息。拖动、布局重排、调用 `move()`、调用 `setGeometry()` 和父对象位置变化都可能间接导致它出现。

## 它解决的问题

控件位置改变时，周边逻辑常需同步更新，例如：

- 重新定位依附于控件的浮层、标注、对齐线或预览框。
- 记录用户调整过的面板位置。
- 根据位置增量更新相邻的轻量绘制缓存。
- 判断顶层工具窗口是否被移动到指定屏幕区域。

这类工作应放在 `QWidget::moveEvent()`，而不是在每一处 `move()` 调用后额外复制一套同步逻辑。`QMoveEvent` 提供的新旧位置让接收者能计算本次变化的位移。

## 基本用法

```cpp
#include <QMoveEvent>
#include <QWidget>

class InspectorPanel : public QWidget
{
protected:
    void moveEvent(QMoveEvent *event) override
    {
        const QPoint delta = event->pos() - event->oldPos();

        updateAttachedOverlay(delta);
        savePositionDebounced(event->pos());

        QWidget::moveEvent(event);
    }
};
```

`pos()` 是移动后的新位置，`oldPos()` 是移动前的位置。它们都是相对于父 widget 的坐标；对于顶层 widget，`pos()` 是窗口客户区位置，不包含窗口边框和标题栏的 frame。

事件对象仅在 `moveEvent()` 或事件过滤器当前调用期间有效。不要保存 `QMoveEvent *`；若需要延迟处理，复制 `pos()`、`oldPos()` 或 `delta`。

## 它不等于鼠标拖动

`QMoveEvent` 不能说明位置为什么变化，也不能告诉你鼠标在哪里。它可能由：

- 用户拖动顶层窗口。
- 程序调用 `QWidget::move()`。
- 程序调用 `QWidget::setGeometry()`。
- 布局系统、父控件移动或窗口管理器调整位置。

如果业务需求是“用户正在拖动控件”，应在 `QMouseEvent` 中维护拖动状态并调用 `move()`；`moveEvent()` 则负责对任何最终位置变化做统一的后处理。

同理，尺寸改变使用 `QResizeEvent` 和 `resizeEvent()`，不要把大小变化的逻辑塞进 `moveEvent()`。

## 坐标边界

| 对象类型 | `event->pos()` / `oldPos()` 的含义 | 容易混淆的坐标 |
| --- | --- | --- |
| 有父对象的子 widget | 相对于父 widget 的左上角坐标 | 不是全局屏幕坐标，也不是自身局部 `(0, 0)`。 |
| 顶层 widget | 窗口客户区位置 | 不包含 window frame；需要完整窗口框位置时看 `frameGeometry()`。 |
| 依附于复杂布局的 widget | 布局计算后的实际位置 | 手动 `move()` 可能在下一次布局中被覆盖。 |

当需要与屏幕或其他顶层窗口对齐时，使用 `mapToGlobal(QPoint(0, 0))` 或 `frameGeometry()` 取得对应坐标，不要把 `event->pos()` 直接与 `QCursor::pos()` 比较。

## 和布局系统协作

被 `QLayout` 管理的子 widget 位置由布局决定。直接对它调用 `move()` 虽然可能立即产生 `QMoveEvent`，但在父控件 resize、样式变化或下一轮布局后，布局可以再次把它放回计算位置。

需要“让面板记住位置”的界面应先确认该面板没有被普通布局接管，或将位置记忆转化为布局参数、splitter 尺寸、dock 区域等更高层状态。不要在 `moveEvent()` 中反复把控件拉回保存位置，这会与布局系统争夺几何控制权。

## 避免递归与抖动

在 `moveEvent()` 里再次调用 `move()` 或 `setGeometry()` 可能继续触发新的 `QMoveEvent`。这在“吸附到网格”或“限制活动区域”中很常见。

安全策略是先计算目标位置，并且只在目标确实不同且不处于自发修正过程中时更新：

```cpp
void ToolPanel::moveEvent(QMoveEvent *event)
{
    if (m_adjustingPosition) {
        QWidget::moveEvent(event);
        return;
    }

    const QPoint snapped = snapToGrid(event->pos());
    if (snapped != event->pos()) {
        m_adjustingPosition = true;
        move(snapped);
        m_adjustingPosition = false;
    }

    QWidget::moveEvent(event);
}
```

更复杂的约束，例如根据多个兄弟控件统一排版，通常应推迟到布局计算或一次合并的定时更新，避免每一个中间移动位置都触发昂贵工作。

## 事件时机、线程与测试

`moveEvent()` 到达时，widget 的位置已经是新位置，因此 `pos()` 与 `widget->pos()` 应表达同一个当前位置。它是 GUI 线程中的 widget 事件；不能从工作线程直接移动 GUI 控件或手动调用它的事件处理函数。

测试中可构造 `QMoveEvent(newPos, oldPos)` 并通过 Qt 事件机制发送给对象，但这只验证接收者的事件分支。它不会替代布局、窗口管理器、屏幕 DPI、父子关系等真实几何环境。

## 常见错误

1. **把它当成鼠标移动。** 它没有按钮、修饰键和光标位置；鼠标输入使用 `QMouseEvent`。
2. **忘记 `pos()` 是相对父对象的。** 跨窗口定位前先映射到全局坐标。
3. **顶层窗口位置当作 frame 位置。** `pos()` 不包含窗口边框。
4. **在布局管理的子控件上强行记忆 `move()`。** 下一轮布局会覆盖结果。
5. **在回调中无条件再次 `move()`。** 会产生递归、抖动或不断重排。
6. **保存事件指针。** 只保存坐标值或计算后的状态。
7. **用 `moveEvent()` 处理尺寸变化。** 尺寸通知是 `QResizeEvent`。

## API 速查表

| API | 作用 | 使用时的语义与边界 |
| --- | --- | --- |
| `QMoveEvent(const QPoint &pos, const QPoint &oldPos)` | 构造包含新旧位置的移动事件。 | 用于测试或自定义事件派发；坐标应遵循接收 widget 的父对象坐标系。 |
| `pos()` | 返回 widget 的新位置。 | 对子 widget 相对父对象；对顶层 widget 不包含 window frame。 |
| `oldPos()` | 返回 widget 的旧位置。 | 与 `pos()` 在同一坐标系中；`pos() - oldPos()` 可得到本次位移。 |
| `QWidget::moveEvent(QMoveEvent *)` | `QWidget` 的移动通知处理点。 | 在这里同步依附 UI 或延迟持久化；避免无条件调用 `move()`。 |
| `QWidget::move()` / `setGeometry()` | 改变 widget 位置的常用入口。 | 会导致位置变化通知；布局管理的子 widget 可能被后续布局重置。 |
| `QWidget::pos()` / `geometry()` / `frameGeometry()` | 查询当前几何信息。 | `pos()` 与事件新位置一致；`frameGeometry()` 才包含顶层窗口边框。 |
| `mapToGlobal()` / `mapFromGlobal()` | 在局部与全局坐标间转换。 | 跨窗口或屏幕交互时使用，不要直接混比 `QMoveEvent::pos()` 和全局坐标。 |
| `QResizeEvent` / `resizeEvent()` | 尺寸变化事件。 | 与移动是不同维度；大小更新不要依赖 `QMoveEvent`。 |

## 一句话总结

`QMoveEvent` 是“控件已经从旧位置移动到新位置”的通知：新旧点都在父对象坐标系中，顶层窗口不含边框；它适合做同步后处理，不适合用来判断鼠标拖动或与布局系统争夺位置控制权。
