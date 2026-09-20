# QMoveEvent

> Qt 6.11.1 · Qt GUI · 来自 `QMoveEvent`

## 1. 先建立直觉

`QMoveEvent` 表示控件或窗口的位置发生变化。它携带新位置和旧位置，适合根据几何变化同步附属对象：浮层、拖拽辅助线、外部窗口、缓存命中区域等。

它描述的是对象自身位置改变，不是鼠标移动。鼠标移动看 `QMouseEvent` 或 `QHoverEvent`；控件被布局、父窗口、用户拖动窗口或代码 `move()` 影响时，才会进入移动事件。

## 2. 类说明

`QMoveEvent` 继承自 `QEvent`。Widgets 常通过 `QWidget::moveEvent()` 接收，也可以在 `event()` 中处理 `QEvent::Move`。

类说明只用于表明这些 API 来自 `QMoveEvent`：它只关心新旧位置，尺寸变化由 `QResizeEvent` 表达，完整几何变化需要把 `moveEvent()` 和 `resizeEvent()` 一起看。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `QMoveEvent(pos, oldPos)` | 构造移动事件，指定新位置和旧位置。 |
| `pos() const` | 返回对象移动后的新位置。顶层窗口时不包含窗口装饰框。 |
| `oldPos() const` | 返回对象移动前的位置，可用于计算位移。 |
| `type()` | 来自 `QEvent`，移动事件通常为 `QEvent::Move`。 |

## 4. 关键用法

### 同步附属浮层

```cpp
void AnchorWidget::moveEvent(QMoveEvent *event)
{
    QWidget::moveEvent(event);

    if (m_popup && m_popup->isVisible())
        m_popup->move(mapToGlobal(QPoint(width(), 0)));
}
```

当锚点控件被布局移动时，浮层也要跟着更新。这里用当前几何重新计算位置，比简单套用 delta 更稳。

### 用新旧位置计算位移

```cpp
void Overlay::moveEvent(QMoveEvent *event)
{
    const QPoint delta = event->pos() - event->oldPos();
    m_cachedHotRect.translate(delta);
    QWidget::moveEvent(event);
}
```

如果缓存内容只和位置偏移有关，利用 delta 可以避免完整重算。

## 5. 使用场景

`QMoveEvent` 适合浮动工具条、弹出提示、停靠面板、图形覆盖层、外部原生窗口嵌入、窗口状态保存、屏幕边缘吸附和多窗口联动。

顶层窗口移动时，它还能帮助保存用户窗口位置；子控件移动时，它常由布局系统触发，用来同步依赖几何位置的辅助对象。

## 6. 常见坑与经验

不要在 `moveEvent()` 中无条件再次调用 `move()`，这很容易造成移动事件递归或布局抖动。

不要把 `pos()` 当成屏幕坐标。子控件的位置相对于父控件；顶层窗口位置也不包含平台窗口边框。

不要只监听移动事件来处理完整几何变化。大小变化不会由 `QMoveEvent` 表达，应同时处理 `QResizeEvent`。

不要在布局管理的子控件里强行移动自己。布局会在下一轮重新接管位置，造成看似无效或闪烁。

## 7. 知识点覆盖

学习 `QMoveEvent` 应覆盖控件几何、父子坐标、顶层窗口边框、布局系统、浮层同步、移动 delta、递归移动风险和窗口位置保存。
