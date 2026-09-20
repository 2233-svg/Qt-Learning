# QTouchEvent

> Qt 6.11.1 · Qt GUI · 来自 `QTouchEvent`

## 1. 先建立直觉

`QTouchEvent` 描述触摸屏或触控设备产生的多触点事件。它继承自 `QPointerEvent`，核心不是“一个触摸坐标”，而是一组 `QEventPoint`：每个触点都有自己的 ID、位置、状态、压力和运动轨迹。

触摸交互和鼠标最大的不同在于“并发”。两个手指可以同时按下、移动、释放；一个触点结束时，另一个触点还在继续。`QTouchEvent` 的设计就是为了让你按触点集合来思考，而不是强行压成鼠标那样的单点流程。

## 2. 类说明

`QTouchEvent` 继承自 `QPointerEvent`。它本身的 API 不多，真正丰富的数据来自父类的 `points()`、`pointCount()`、`pointById()` 和每个 `QEventPoint`。

类说明只用于表明这些 API 来自 `QTouchEvent`：构造触摸事件、读取目标对象、汇总触点状态，以及判断触摸事件阶段。触点坐标和设备信息仍要结合 `QPointerEvent` 与 `QEventPoint` 一起看。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `QTouchEvent(eventType, device, modifiers, touchPoints)` | 构造触摸事件，通常用于测试、输入转发或自定义平台层。 |
| `target() const` | 返回事件在窗口内对应的目标对象，常见为 `QWidget` 或 `QQuickItem`。 |
| `touchPointStates() const` | 返回所有触点状态的按位 OR，用于快速判断是否含有按下、移动、释放等状态。 |
| `isBeginEvent() const` | 判断事件是否包含新按下的触点。 |
| `isUpdateEvent() const` | 判断事件是否只是触点更新，没有新按下或新释放。 |
| `isEndEvent() const` | 判断事件是否包含新释放的触点。 |
| `points() const` | 来自父类，读取本次事件包含的全部触点。 |
| `pointById(int)` | 来自父类，按触点 ID 查找持续跟踪中的某个点。 |
| `pointCount() const` | 来自父类，读取触点数量。 |

## 4. 关键用法

### 启用触摸事件

Widgets 默认不一定把触摸事件直接交给控件。自定义控件通常需要启用触摸属性。

```cpp
TouchCanvas::TouchCanvas(QWidget *parent)
    : QWidget(parent)
{
    setAttribute(Qt::WA_AcceptTouchEvents);
}
```

然后可以在 `event()` 里接收 `QEvent::TouchBegin`、`TouchUpdate`、`TouchEnd`、`TouchCancel`。

```cpp
bool TouchCanvas::event(QEvent *event)
{
    switch (event->type()) {
    case QEvent::TouchBegin:
    case QEvent::TouchUpdate:
    case QEvent::TouchEnd:
    case QEvent::TouchCancel:
        return handleTouch(static_cast<QTouchEvent *>(event));
    default:
        return QWidget::event(event);
    }
}
```

### 按触点 ID 跟踪，而不是按列表顺序

多触点列表顺序不应该成为业务状态的唯一依据。更稳妥的方式是用 `QEventPoint::id()` 关联持续轨迹。

```cpp
bool TouchCanvas::handleTouch(QTouchEvent *event)
{
    for (const QEventPoint &point : event->points()) {
        switch (point.state()) {
        case QEventPoint::State::Pressed:
            m_strokes.insert(point.id(), Stroke(point.position()));
            break;
        case QEventPoint::State::Updated:
            m_strokes[point.id()].append(point.position());
            break;
        case QEventPoint::State::Released:
            finishStroke(point.id(), point.position());
            m_strokes.remove(point.id());
            break;
        default:
            break;
        }
    }

    event->accept();
    return true;
}
```

### 用状态汇总快速分流

`touchPointStates()` 适合做轻量级判断：本次事件是否包含新按下、是否包含释放、是否只是移动。

```cpp
if (event->touchPointStates().testFlag(QEventPoint::State::Pressed))
    prepareGesture(event->points());
```

之后仍应遍历每个点，因为同一个事件可能同时包含一个触点释放、另一个触点更新。

## 5. 使用场景

`QTouchEvent` 适合触屏白板、图片查看器、地图、POS/工控大屏、教育软件、音乐控制台、游戏 UI、多指缩放旋转和多指绘制。

它也适合构建自己的手势识别器。Qt 有 `QGestureEvent` 和现成手势，但当你需要精确控制两指旋转、三指切换、多人同时绘制时，直接处理 `QTouchEvent` 更可控。

在混合输入应用中，触摸事件常和鼠标合成事件同时出现。你需要决定控件是接受触摸、让 Qt 合成鼠标，还是两者分别处理；这个策略要统一，否则容易出现一次触摸触发两套逻辑。

## 6. 常见坑与经验

不要只取 `points().first()`。单指场景当然能跑，但双指缩放、误触处理、多用户触控都会被破坏。

不要假设 `TouchEnd` 表示所有手指都离开了。它表示本次事件包含释放点；是否仍有其他点存在，要看 `points()` 和各点状态。

不要忽略 `TouchCancel`。系统可能因为窗口切换、手势被平台接管、设备中断等原因取消触摸；取消时应清理临时状态。

不要把触摸和鼠标处理完全混在一起。可以共享底层工具逻辑，但入口层要明确事件来源，否则合成鼠标事件可能让一次操作执行两遍。

## 7. 知识点覆盖

学习 `QTouchEvent` 应覆盖触摸事件启用、触点 ID、触点状态、多点列表、触摸开始/更新/结束/取消、目标对象、触摸与鼠标合成、手势识别、事件接受策略、设备能力和跨平台触控行为。
