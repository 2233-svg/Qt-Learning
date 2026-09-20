# QTouchEvent 类笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QTouchEvent>`  
> 所属模块：`Qt6::Gui`  
> 继承：`QPointerEvent`

## 1. 它解决什么问题

`QTouchEvent` 描述一次触摸输入事件：同一个事件里可能包含一个或多个 `QEventPoint`，每个点有自己的位置、压力、状态和 id。它解决的是“把触摸屏、触控板等设备上的多点接触，作为一个有序事件序列交给窗口、控件或场景项处理”的问题。

鼠标事件通常围绕一个指针位置展开；触摸事件的核心是“一组触点”。因此 `QTouchEvent` 更适合处理双指缩放、旋转、拖拽画布、多指按钮操作、手写板/触摸屏上的连续轨迹等场景。

## 2. 接收触摸事件的入口

`QWindow` 会接收触摸事件，通常重写 `QWindow::touchEvent(QTouchEvent *)`。`QWidget` 默认不主动接收触摸输入，需要设置 `Qt::WA_AcceptTouchEvents`；如果是 `QAbstractScrollArea` 派生类，要把属性设在 `viewport()` 上。Graphics View 中则通过 `QGraphicsItem::setAcceptTouchEvents(true)` 让图形项参与触摸投递。

常见入口如下：

```cpp
bool Canvas::event(QEvent *event)
{
    if (event->type() == QEvent::TouchBegin ||
        event->type() == QEvent::TouchUpdate ||
        event->type() == QEvent::TouchEnd ||
        event->type() == QEvent::TouchCancel) {
        auto *touch = static_cast<QTouchEvent *>(event);
        updateGesture(touch->points());
        event->accept();
        return true;
    }
    return QWidget::event(event);
}
```

`TouchBegin` 是整段触摸序列的入口。控件如果不处理这段触摸，应调用 `ignore()`，让事件沿父对象/场景传播；一旦接受，后续 `TouchUpdate` 和 `TouchEnd` 会投递给接受 `TouchBegin` 的对象。

## 3. 事件序列与触点语义

触摸事件类型主要是 `QEvent::TouchBegin`、`QEvent::TouchUpdate`、`QEvent::TouchEnd` 和 `QEvent::TouchCancel`。`isBeginEvent()`、`isUpdateEvent()`、`isEndEvent()` 是对事件内触点状态的快速分类：事件包含新按下点时是 begin，包含新释放点时是 end；既没有新按下也没有新释放时是 update。

通过继承自 `QPointerEvent` 的 `points()`、`pointCount()` 和 `point(i)` 读取触点。`points()` 对一个投递目标来说不是“只列出变化点”的增量列表，而是包含当前目标相关的整组物理触点；但在 `TouchCancel` 等情况下列表可能为空。处理手势时要同时看 `QEventPoint::state()`，不要只凭点数量推断动作。

Qt 会在第一次按下时自动抓取触点，使后续更新继续发给同一接收者。多个控件可以同时处理不同触摸序列；当新触点落在已有触摸目标的祖先或后代区域时，Qt 会把它们分到同一组，以保持序列一致。

## 4. 实际使用边界

`QTouchEvent` 是事件对象，主要在事件处理函数调用期间读取。不要长期保存事件指针；如果需要把触点轨迹交给后续逻辑，复制你真正需要的 `QEventPoint` 数据或业务坐标。

`target()` 返回窗口内部的目标对象，常见是 `QWidget` 或 `QQuickItem`，但没有明确目标时可能是 `nullptr`。`device()`/`pointingDevice()` 指向 Qt 管理的设备描述，不表示调用方拥有设备对象。

Qt 可在未处理的触摸和鼠标事件之间合成事件，受 `Qt::AA_SynthesizeMouseForUnhandledTouchEvents` 与 `Qt::AA_SynthesizeTouchForUnhandledMouseEvents` 控制。写触摸逻辑时要避免同一个业务动作既由触摸路径处理、又由合成鼠标路径重复处理。

触摸事件处理函数里不支持递归进入事件循环，例如直接调用 `QDialog::exec()` 或 `QMenu::exec()`。多目标触摸投递和嵌套事件循环组合时容易造成事件丢失、乱序或重入。

## API 速查表

| API | 用途与关键语义 | 边界、默认值或注意事项 |
| --- | --- | --- |
| `QTouchEvent(QEvent::Type, const QPointingDevice *, Qt::KeyboardModifiers, const QList<QEventPoint> &)` | 手动构造触摸事件，指定事件类型、设备、键盘修饰键和触点列表。 | 正常应用很少手动构造；平台插件/测试工具通常负责创建真实事件。 |
| `using TouchPoint = QEventPoint` | 兼容旧代码中 `QTouchEvent::TouchPoint` 的名称。 | Qt 6 的触点类型是 `QEventPoint`；新代码直接使用 `QEventPoint`。 |
| `target() const` | 返回窗口内部的触摸目标对象。 | 可能为 `nullptr`；不要假定一定是 `QWidget`，Qt Quick 中常是 `QQuickItem`。 |
| `touchPointStates() const` | 返回本事件所有触点状态的按位或。 | 只能说明本事件内有哪些状态类别；逐点逻辑仍应查看每个 `QEventPoint::state()`。 |
| `isBeginEvent() const` | 判断事件是否包含至少一个新按下的触点。 | 不等同于事件类型一定是 `TouchBegin`；语义来自触点状态集合。 |
| `isUpdateEvent() const` | 判断事件是否是不含新按下/新释放点的更新。 | 移动、保持不动等都可能落在更新序列中；结合点状态处理。 |
| `isEndEvent() const` | 判断事件是否包含至少一个新释放的触点。 | 多指场景下释放一个手指不一定意味着整段手势结束。 |
| 继承的 `points()` | 返回事件包含的 `QEventPoint` 列表。 | 对目标而言列表通常是完整触点组；`TouchCancel` 可为空。 |
| 继承的 `pointCount()` / `point(i)` | 按索引读取触点数量和单个触点。 | 索引必须在有效范围内；不要在列表为空时读取第一个点。 |
| 继承的 `device()` / `pointingDevice()` | 读取产生事件的指针设备。 | 设备对象由 Qt 管理，用于判断触摸屏、触控板、能力等。 |
| 继承的 `accept()` / `ignore()` | 控制 `TouchBegin` 是否被当前对象接收以及是否继续传播。 | 未接受的 `TouchBegin` 通常不会带来后续 update/end 序列。 |
| 废弃 `touchPoints()` | Qt 5 兼容接口，返回触点列表。 | Qt 6 新代码改用 `points()`。 |

## 5. 记忆重点

`QTouchEvent` 的重点不是“一个事件等于一个手指”，而是一段多触点序列。先让目标对象真正接收触摸，再在 `TouchBegin` 时明确接受或忽略；后续用 `points()` 加每个点的状态维护手势状态机。
