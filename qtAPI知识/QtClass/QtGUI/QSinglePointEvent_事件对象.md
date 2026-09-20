# Qt QSinglePointEvent：鼠标、触控和其他单点输入的共同事件接口

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QSinglePointEvent>`  
> 所属模块：`Qt6::Gui`  
> 继承：`QEvent -> QInputEvent -> QPointerEvent -> QSinglePointEvent`  
> 类型定位：为单点输入派生事件提供统一坐标、按钮和抓取 API 的抽象基类

## 1. 它解决什么问题

鼠标、触控、滚轮、悬停、原生手势和数位板事件有很多共同信息：

- 一个主输入点的位置；
- local、scene 和 global 三套坐标；
- 触发本次事件的按钮；
- 当前仍按下的按钮集合；
- 事件属于 begin、update 还是 end 阶段；
- 该点是否被某个对象独占抓取。

`QSinglePointEvent` 把这些共同语义集中起来，让派生类可以专注于自己的数据，例如 `QMouseEvent` 的鼠标源、`QWheelEvent` 的滚轮 delta 或 `QTabletEvent` 的压力。

它不是一个可以直接接收任意单点输入的具体事件类型。构造函数受保护，普通应用应处理它的派生类。

## 2. 继承结构与派生类

```text
QEvent
  -> QInputEvent
    -> QPointerEvent
      -> QSinglePointEvent
        -> QMouseEvent
        -> QWheelEvent
        -> QHoverEvent
        -> QEnterEvent
        -> QTabletEvent
        -> QNativeGestureEvent
```

不同派生类的事件类型决定 `isBeginEvent()`、`isUpdateEvent()` 和 `isEndEvent()` 的具体结果。不要因为一个事件继承自本类，就假设三个函数中只有一个永远为 true；应以具体派生类和事件阶段为准。

## 3. 为什么不能直接构造

头文件中的构造函数是 protected：

```cpp
QSinglePointEvent(Type type, const QPointingDevice *dev,
                  const QEventPoint &point,
                  Qt::MouseButton button,
                  Qt::MouseButtons buttons,
                  Qt::KeyboardModifiers modifiers,
                  Qt::MouseEventSource source);
```

以及：

```cpp
QSinglePointEvent(Type type, const QPointingDevice *dev,
                  const QPointF &localPos,
                  const QPointF &scenePos,
                  const QPointF &globalPos,
                  Qt::MouseButton button,
                  Qt::MouseButtons buttons,
                  Qt::KeyboardModifiers modifiers,
                  Qt::MouseEventSource source =
                      Qt::MouseEventNotSynthesized);
```

这些构造器供 Qt 的派生事件使用。应用需要手工生成测试事件时，应构造具体的 `QMouseEvent`、`QWheelEvent` 或其他派生类，而不是尝试从外部调用本类 protected 构造器。

## 4. 三套坐标

### 4.1 `position()`

返回主事件点的局部坐标。局部坐标相对于接收该事件的对象或事件点所在局部空间，具体基准由 Qt 的事件接收模型决定。

适合用于控件内部命中测试、绘制局部反馈和计算相对于控件左上角的位置。

### 4.2 `scenePosition()`

返回 scene 坐标。对 QWidget 应用，通常更常用 local/global；对 Qt Quick 或 scene 类输入路径，scene 坐标可用于在场景坐标系中处理输入。

### 4.3 `globalPosition()`

返回屏幕/全局坐标。适合创建上下文菜单、拖拽浮层或与屏幕坐标 API 协作。

三者都是 `QPointF`，保留小数坐标。不要在事件处理早期无条件转成 `QPoint`，否则高 DPI、缩放和触控输入的小数位会丢失。

```cpp
void Editor::mouseMoveEvent(QMouseEvent *event)
{
    const QPointF local = event->position();
    const QPointF screen = event->globalPosition();
    updateCursor(local);
    updateTooltipPosition(screen);
}
```

Qt 6 已将 `position()`、`scenePosition()` 和 `globalPosition()` 作为首选坐标 API。旧的整数坐标函数容易产生截断或舍入误差。

## 5. `button()` 与 `buttons()`

### `button()`

返回触发这一次事件的单个按钮。对于按下/释放事件，它通常表示本次发生变化的按钮；对于移动、悬停或某些非鼠标事件，可能是 `Qt::NoButton`。

### `buttons()`

返回事件发生时仍处于按下状态的所有鼠标按钮集合。移动事件中常见情况是：

```text
button()  == Qt::NoButton
buttons() 包含 Qt::LeftButton
```

因此：

- 判断“是哪一个按钮触发按下/释放”看 `button()`；
- 判断“当前有哪些按钮仍按下”看 `buttons()`；
- 不要用 `button()` 判断拖动期间左键是否仍然按下。

## 6. 单点抓取

### `exclusivePointGrabber : QObject*`

该属性表示主事件点的独占抓取对象。读取等价于查询 `QPointerEvent` 中第一个点的 exclusive grabber，写入则更新该点的抓取对象。

```cpp
QObject *grabber = event->exclusivePointGrabber();
if (grabber == this) {
    // 当前对象独占接收这个单点
}
```

### `exclusivePointGrabber() const`

返回主点的独占抓取对象。返回值可能为 `nullptr`。对象指针不代表当前事件对象拥有它。

### `setExclusivePointGrabber(QObject *exclusiveGrabber)`

设置主点的独占抓取对象。它只适合有效的单点事件；事件必须已经包含一个 point。普通应用更常通过 widget、pointer handler 或 Qt 的抓取 API 管理抓取，不应随意在事件过滤器中改写抓取关系。

抓取对象的生命周期由 QObject 对象树管理，事件不会延长它的生命周期。

## 7. begin/update/end 分类

### `isBeginEvent() const`

判断事件是否代表输入序列或点生命周期开始。例如鼠标按下、触点开始等具体事件可能返回 true。

### `isUpdateEvent() const`

判断事件是否代表正在进行的更新。例如鼠标移动、触点移动、滚轮更新或悬停事件可能属于 update。

### `isEndEvent() const`

判断事件是否代表输入序列或点生命周期结束。例如鼠标释放、触点结束等事件可能返回 true。

这些函数是 virtual，由派生类根据事件类型实现。它们是事件分类辅助，不会改变事件的 accepted 状态，也不会自动开始或结束抓取。

## 8. 实际使用场景

### 8.1 在自定义控件中统一处理鼠标派生事件

如果函数只需要位置和按钮信息，可以使用共同逻辑：

```cpp
void Canvas::handlePointEvent(QSinglePointEvent *event)
{
    const QPointF p = event->position();

    if (event->isBeginEvent())
        beginStroke(p);
    else if (event->isUpdateEvent())
        updateStroke(p);
    else if (event->isEndEvent())
        finishStroke(p);
}
```

具体的 `mousePressEvent()`、`mouseMoveEvent()` 和 `mouseReleaseEvent()` 再把事件传入。

### 8.2 高 DPI 和触控友好命中测试

使用 `QPointF` 的 local position 做命中测试，避免整数坐标在缩放界面中造成边界抖动。触控点和鼠标模拟事件也应按统一的坐标和阶段逻辑处理。

### 8.3 统一处理滚轮和手势位置

滚轮事件本身还带有 delta，原生手势还带有 value/delta，但它们都可以复用本类的坐标和生命周期判断。

## 9. 事件接受、传播和短生命周期

`QSinglePointEvent` 继承 `QEvent` 的 accepted 状态。调用 `accept()` 或 `ignore()` 影响事件传播和上层处理，但不会改变 `position()` 或抓取对象。

事件对象通常由 Qt 在 GUI 线程中临时创建并发送。不要在事件处理函数返回后保存 `QSinglePointEvent *` 或其中派生事件指针。若需要异步处理，复制需要的坐标、按钮、时间戳和业务数据。

## 10. 常见误区

- 把 `position()` 当成屏幕坐标：需要屏幕坐标时使用 `globalPosition()`。
- 把 `button()` 当成当前所有按键：拖动中应读取 `buttons()`。
- 认为单点事件一定能直接构造：本类构造器是 protected。
- 直接把 `QPointF` 截断成 `QPoint` 后再做高 DPI 命中测试。
- 把 begin/update/end 当作 accepted 状态。
- 在事件返回后保存事件指针。
- 在没有有效 point 的对象上调用 `setExclusivePointGrabber()`。
- 修改抓取对象却没有考虑对象树和线程归属。
- 把 `scenePosition()`、`globalPosition()` 和 `position()` 混用。

## API 速查表
| 类别 | API | 作用 | 关键边界 |
| --- | --- | --- | --- |
| 属性 | `exclusivePointGrabber : QObject*` | 读取/设置主点独占抓取对象 | 不拥有对象；事件需有有效 point |
| 构造 | protected `QSinglePointEvent(...)` | 供派生事件创建 | 普通应用不能直接构造 |
| 查询 | `button() const` | 获取本次变化的单个按钮 | 移动/悬停时可能是 `NoButton` |
| 查询 | `buttons() const` | 获取当前按下按钮集合 | 拖动判断应看它 |
| 坐标 | `position() const` | 获取局部小数坐标 | 不等于全局坐标 |
| 坐标 | `scenePosition() const` | 获取 scene 坐标 | 具体空间由事件模型决定 |
| 坐标 | `globalPosition() const` | 获取全局小数坐标 | 适合屏幕级定位 |
| 分类 | `isBeginEvent() const` | 判断输入开始 | 由派生类实现 |
| 分类 | `isUpdateEvent() const` | 判断输入更新 | 由派生类实现 |
| 分类 | `isEndEvent() const` | 判断输入结束 | 由派生类实现 |
| 抓取 | `exclusivePointGrabber() const` | 查询主点独占抓取者 | 可能为 `nullptr` |
| 抓取 | `setExclusivePointGrabber(QObject *)` | 设置主点抓取者 | 普通业务少量使用，需有效 point |
| 继承 | `accept()` / `ignore()` | 控制事件传播 | 不改变坐标和生命周期分类 |

---

### 一句话总结

`QSinglePointEvent` 是 Qt 单点输入事件的共同语义层：用 `position()`/`scenePosition()`/`globalPosition()` 区分坐标空间，用 `button()` 与 `buttons()` 区分触发按钮和按下集合，用 begin/update/end 判断阶段；本类不能直接构造，实际处理应面向具体派生事件。
