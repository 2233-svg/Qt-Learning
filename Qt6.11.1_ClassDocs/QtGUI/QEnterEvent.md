# QEnterEvent

> Qt 6.11.1 · Qt GUI · 来自 `QEnterEvent`

## 1. 先建立直觉

`QEnterEvent` 表示指针进入某个窗口、控件或图形项的区域。它不是“鼠标移动了一下”，而是“从外部进入到这个对象的命中范围内”。因此它常用于高亮、预热悬停状态、更新光标、显示轻量提示。

它继承自 `QSinglePointEvent`，所以可以读取 `position()`、`scenePosition()`、`globalPosition()`。进入事件发生的一瞬间，三套坐标能告诉你指针是从哪里进入的。

## 2. 类说明

`QEnterEvent` 继承自 `QSinglePointEvent`。在 Widgets 中通常对应 `QWidget::enterEvent()`；离开则通常由 `QEvent::Leave` 或 `leaveEvent()` 处理，而不是同一个类。

类说明只用于表明这些 API 来自 `QEnterEvent`：它自身只有构造函数，坐标、设备、指针类型等能力来自父类单点输入事件。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `QEnterEvent(localPos, scenePos, globalPos, device)` | 构造进入事件，指定局部、窗口/场景、全局三套坐标和来源设备。 |
| `position() const` | 来自父类，进入点相对于接收对象的坐标。 |
| `scenePosition() const` | 来自父类，进入点相对于窗口或场景的坐标。 |
| `globalPosition() const` | 来自父类，进入点在屏幕或虚拟桌面上的坐标。 |
| `pointingDevice() const` | 来自父类，查看产生进入事件的指针设备。 |

## 4. 关键用法

### 做轻量 hover 状态初始化

进入事件适合切换“鼠标在我里面”的状态，但不要把持续跟踪逻辑全塞在 enter 里。

```cpp
void ColorSwatch::enterEvent(QEnterEvent *event)
{
    m_hovered = true;
    update();
    QWidget::enterEvent(event);
}

void ColorSwatch::leaveEvent(QEvent *event)
{
    m_hovered = false;
    update();
    QWidget::leaveEvent(event);
}
```

进入和离开负责状态边界，`mouseMoveEvent()` 或 `QHoverEvent` 负责中间的连续移动。

### 进入点可以用于边缘感知

如果控件需要根据进入方向做动画，`position()` 能提供第一帧位置。

```cpp
void SidePanel::enterEvent(QEnterEvent *event)
{
    m_enterFromLeft = event->position().x() < width() * 0.25;
    startHoverAnimation(m_enterFromLeft);
}
```

这类逻辑适合增强反馈，但不要依赖它实现核心功能，因为键盘焦点进入不会产生同样的指针语义。

## 5. 使用场景

`QEnterEvent` 常用于按钮外观预热、自定义控件高亮、图形项拾取反馈、光标切换、状态栏提示、延迟加载悬停资源。

它也适合减少不必要的 mouse tracking。很多控件只需要知道指针是否进入，而不需要每一帧移动；用 enter/leave 比持续处理鼠标移动更轻。

在跨设备场景中，进入事件可能来自鼠标、触摸板或笔设备。需要区分设备时，可以从父类读取 `pointingDevice()` 或 `deviceType()`。

## 6. 常见坑与经验

不要把 `QEnterEvent` 当作连续移动事件。它只表示进入边界那一刻。

不要忘记配套处理 leave。只设置 hover 状态不清除，控件会卡在高亮状态。

不要把进入事件和焦点事件混用。鼠标进入不等于控件获得键盘焦点；键盘导航进入焦点也不等于指针进入。

不要为了普通高亮过度创建复杂动画。enter/leave 很高频地出现在控件之间切换时，反馈应快速、可中断。

## 7. 知识点覆盖

学习 `QEnterEvent` 应覆盖进入/离开事件、hover 状态、mouse tracking 区别、局部/场景/全局坐标、指针设备来源、控件重绘策略、焦点与指针命中的区别。
