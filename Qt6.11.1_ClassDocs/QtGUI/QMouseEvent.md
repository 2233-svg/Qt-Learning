# QMouseEvent

> Qt 6.11.1 · Qt GUI · 来自 `QMouseEvent`

## 1. 先建立直觉

`QMouseEvent` 描述鼠标按下、释放、双击和移动。它继承自 `QSinglePointEvent`，所以大部分常用能力，如 `position()`、`globalPosition()`、`button()`、`buttons()`，其实来自单点输入事件模型。

鼠标事件的关键不是“鼠标在哪里”这么简单，而是要同时回答四个问题：事件类型是什么、这次变化由哪个按钮触发、事件发生时哪些按钮正按着、这个坐标属于哪个坐标系。只要这四个问题分清楚，绝大多数鼠标交互都会稳定很多。

## 2. 类说明

`QMouseEvent` 继承自 `QSinglePointEvent`。通常由 Qt 在事件循环中创建并分发给 `QWidget::mousePressEvent()`、`mouseReleaseEvent()`、`mouseMoveEvent()`、`mouseDoubleClickEvent()`，也可以在 `QWindow` 或事件过滤器中处理。

类说明只保留用来表明这些 API 来自 `QMouseEvent`：构造鼠标事件和读取鼠标事件标志属于鼠标事件本身；位置、按钮状态、设备来源则来自父类。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `QMouseEvent(type, localPos, globalPos, button, buttons, modifiers, device)` | 构造鼠标事件，窗口/场景位置默认与局部位置一致。 |
| `QMouseEvent(type, localPos, scenePos, globalPos, button, buttons, modifiers, device)` | 构造带局部、窗口/场景、全局三套坐标的鼠标事件。 |
| `flags() const` | 读取鼠标事件的附加标志，用于识别合成、来源或特殊分发信息。 |
| `position() const` | 来自父类，读取相对接收对象的局部坐标。 |
| `globalPosition() const` | 来自父类，读取屏幕或虚拟桌面坐标。 |
| `button() const` | 来自父类，读取触发本次事件的按钮。 |
| `buttons() const` | 来自父类，读取事件发生时所有按下的按钮。 |

## 4. 关键用法

### 按下、移动、释放是一条状态机

不要在每个事件里孤立处理鼠标。拖拽、框选、绘制都应该把 press 视为开始，move 视为更新，release 视为结束。

```cpp
void Canvas::mousePressEvent(QMouseEvent *event)
{
    if (event->button() != Qt::LeftButton) {
        event->ignore();
        return;
    }

    m_dragging = true;
    m_anchor = event->position();
    event->accept();
}

void Canvas::mouseMoveEvent(QMouseEvent *event)
{
    if (!m_dragging || !event->buttons().testFlag(Qt::LeftButton)) {
        event->ignore();
        return;
    }

    updateSelection(m_anchor, event->position());
    event->accept();
}

void Canvas::mouseReleaseEvent(QMouseEvent *event)
{
    if (m_dragging && event->button() == Qt::LeftButton) {
        m_dragging = false;
        commitSelection();
        event->accept();
        return;
    }

    event->ignore();
}
```

移动事件看 `buttons()`，释放事件看 `button()`，这是最常用也最容易写错的规则。

### 移动控件或窗口时使用全局坐标

如果你根据鼠标拖动移动接收控件本身，局部坐标会随着控件移动而改变，导致抖动。全局坐标不会受控件移动影响。

```cpp
void FloatingPanel::mousePressEvent(QMouseEvent *event)
{
    if (event->button() == Qt::LeftButton) {
        m_startGlobal = event->globalPosition();
        m_startPos = pos();
        event->accept();
    }
}

void FloatingPanel::mouseMoveEvent(QMouseEvent *event)
{
    if (event->buttons().testFlag(Qt::LeftButton)) {
        move(m_startPos + (event->globalPosition() - m_startGlobal).toPoint());
        event->accept();
    }
}
```

### 双击不是“两次单击”的简单替代

`MouseButtonDblClick` 会作为独立事件出现。很多控件需要决定单击动作是否延迟，因为第二次点击可能升级为双击。

```cpp
void ItemView::mouseDoubleClickEvent(QMouseEvent *event)
{
    if (event->button() == Qt::LeftButton) {
        openIndexAt(event->position());
        event->accept();
        return;
    }

    QWidget::mouseDoubleClickEvent(event);
}
```

如果单击立即执行不可逆动作，双击体验会很差。文件列表、时间轴、图形编辑器尤其要注意。

## 5. 使用场景

`QMouseEvent` 是自定义 Widgets 交互的主力：按钮之外的可点击区域、绘图画布、框选、拖动排序、节点编辑、图像查看器、标尺、时间轴、右键菜单触发等都依赖它。

它也常用于兼容触摸输入。Qt 可能把触摸转换成鼠标事件，让老控件可用；如果你的应用需要区分真实鼠标和触摸合成事件，应结合 `device()`、`deviceType()` 和 `flags()` 判断。

在精细 UI 中，鼠标事件常和 `setMouseTracking(true)` 配合使用。默认情况下，没有按钮按下时控件通常收不到移动事件；开启 mouse tracking 后，悬停移动才会持续进入 `mouseMoveEvent()`。

## 6. 常见坑与经验

不要用整数坐标作为第一选择。Qt 6 鼠标位置是 `QPointF`，高 DPI、缩放和触控板环境下小数坐标很常见；过早 `toPoint()` 会丢精度。

不要在处理后忘记 `accept()`，也不要无条件吞掉所有鼠标事件。自定义控件应处理自己负责的交互，其余交给基类，这样上下文菜单、选择、焦点和父级事件逻辑才不容易断。

不要用 `QCursor::pos()` 替代事件里的 `globalPosition()`。事件坐标代表事件发生时的位置，全局光标查询代表当前时刻的位置，两者在异步窗口系统和高频输入时可能不同。

不要假设鼠标移动事件一定伴随按钮。未开启 mouse tracking 时通常只有按键拖动才持续收到移动；开启后无按钮移动也会进入。

## 7. 知识点覆盖

学习 `QMouseEvent` 应覆盖鼠标事件类型、局部/场景/全局坐标、按钮变化与按钮状态、拖拽状态机、双击处理、mouse tracking、事件接受与传播、高 DPI 坐标、合成鼠标事件、输入设备判断以及与上下文菜单和拖放系统的边界。
