# QSinglePointEvent

> Qt 6.11.1 · Qt GUI · 来自 `QSinglePointEvent`

## 1. 先建立直觉

`QSinglePointEvent` 是“只有一个指针点”的输入事件基类。鼠标、滚轮、悬停、进入窗口、平板笔等事件都天然围绕一个点展开，因此它们共享同一套坐标、按钮和抓取逻辑。

它位于 `QPointerEvent` 和具体事件类之间：`QPointerEvent` 关心一个事件里可以有多个 `QEventPoint`，`QSinglePointEvent` 则把常用场景简化成“就看第一个点”。所以当你在 `QMouseEvent` 里调用 `position()`、`globalPosition()`、`button()`、`buttons()` 时，实际是在使用这个基类提供的语义。

## 2. 类说明

`QSinglePointEvent` 继承自 `QPointerEvent`，常见派生类包括 `QEnterEvent`、`QHoverEvent`、`QMouseEvent`、`QNativeGestureEvent`、`QTabletEvent` 和 `QWheelEvent`。

它保留类说明的价值在于告诉你这些 API 来自哪一层：坐标与按钮状态不是 `QMouseEvent` 独有的，而是一整类单点输入事件共享的抽象。写通用输入处理器时，可以面向 `QSinglePointEvent` 读取位置与按钮，而把滚轮角度、键值、触点列表等特殊信息交给具体子类。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `position() const` | 当前点相对于接收控件、窗口项或事件目标的局部坐标。 |
| `scenePosition() const` | 当前点相对于窗口或图形场景的坐标。 |
| `globalPosition() const` | 当前点在屏幕或虚拟桌面中的全局坐标。 |
| `button() const` | 触发本次按下、释放、双击等状态变化的那个按钮。移动事件通常是 `Qt::NoButton`。 |
| `buttons() const` | 事件发生时处于按下状态的全部鼠标按钮组合。 |
| `exclusivePointGrabber() const` | 查询当前单点的独占抓取对象。 |
| `setExclusivePointGrabber(QObject *)` | 设置当前单点后续更新事件的独占接收对象。 |
| `isBeginEvent() const` | 判断该事件是否表示一次单点交互开始，例如按下。 |
| `isUpdateEvent() const` | 判断该事件是否表示位置或状态更新，但不是开始或结束。 |
| `isEndEvent() const` | 判断该事件是否表示一次单点交互结束，例如释放。 |

## 4. 关键用法

### 正确选择三套坐标

`position()`、`scenePosition()`、`globalPosition()` 的区别经常决定交互是否稳定。

```cpp
void DraggableWidget::mousePressEvent(QMouseEvent *event)
{
    m_pressLocal = event->position();
    m_pressGlobal = event->globalPosition();
}

void DraggableWidget::mouseMoveEvent(QMouseEvent *event)
{
    const QPointF delta = event->globalPosition() - m_pressGlobal;
    move(m_originalTopLeft + delta.toPoint());
}
```

拖动窗口或控件时，优先用 `globalPosition()` 计算位移，因为控件本身移动后，局部坐标会跟着变化。绘制控件内部内容时，优先用 `position()`，因为它天然落在控件坐标系里。

### 区分 `button()` 和 `buttons()`

`button()` 表示“这次事件是谁触发的”，`buttons()` 表示“这一刻哪些按钮正按着”。

```cpp
void Canvas::mouseReleaseEvent(QMouseEvent *event)
{
    if (event->button() == Qt::LeftButton)
        finishStroke();

    if (event->buttons().testFlag(Qt::RightButton))
        keepContextPanning();
}
```

在 release 事件中，被释放的按钮通常不会再出现在 `buttons()` 里。如果你要判断“刚释放的是左键”，应该看 `button()`，不是 `buttons()`。

### 用 begin/update/end 抽象输入流程

当你写的是通用单点处理器，而不想关心具体事件类型时，`isBeginEvent()`、`isUpdateEvent()`、`isEndEvent()` 很有用。

```cpp
bool StrokeController::handle(QSinglePointEvent *event)
{
    if (event->isBeginEvent())
        begin(event->position());
    else if (event->isUpdateEvent())
        append(event->position());
    else if (event->isEndEvent())
        finish(event->position());
    else
        return false;

    event->accept();
    return true;
}
```

## 5. 使用场景

`QSinglePointEvent` 适合统一处理鼠标、笔、悬停和滚轮这类单点输入。比如画布控件可以用它处理指针位置，再让 `QTabletEvent` 补充压力、倾斜信息，让 `QWheelEvent` 补充滚动角度。

它也适合解释坐标问题。很多“拖动时控件抖动”“移动窗口时光标和控件错位”的 bug，本质上是把局部坐标当成全局坐标使用。读懂 `QSinglePointEvent`，这类问题会少很多。

对于 Qt Quick 或高级输入路由，`exclusivePointGrabber` 表示当前点未来更新会被哪个对象独占接收。普通 Widgets 代码很少主动设置它，但理解这个概念有助于排查“为什么释放事件没有回到原控件”。

## 6. 常见坑与经验

不要在拖动外部对象时只用 `position()`。接收控件或窗口移动后，局部坐标的参考系会变，位移计算就会出现跳动。

不要把 `button()` 当成“当前按着的按钮集合”。尤其是移动事件中，`button()` 通常是 `Qt::NoButton`，真正要看按住状态应使用 `buttons()`。

不要把 `scenePosition()` 理解成 `QGraphicsScene` 专属坐标。它在 Qt GUI 输入模型里泛指窗口或场景层面的坐标，具体含义取决于接收对象所在的事件系统。

不要随意设置 `exclusivePointGrabber`。常规控件用接受/忽略事件就足够，抓取者机制更适合输入分发框架和复杂手势系统。

## 7. 知识点覆盖

学习 `QSinglePointEvent` 应覆盖局部坐标、窗口或场景坐标、全局屏幕坐标、按钮触发与按钮状态、单点交互生命周期、事件点抓取、鼠标拖动稳定性、悬停与进入事件、滚轮和手写笔事件的共同基础。
