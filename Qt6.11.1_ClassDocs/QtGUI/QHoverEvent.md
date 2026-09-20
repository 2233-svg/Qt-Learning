# QHoverEvent

> Qt 6.11.1 · Qt GUI · 来自 `QHoverEvent`

## 1. 先建立直觉

`QHoverEvent` 描述指针悬停在对象上方时的进入、移动和离开。它通常用于“不按鼠标按钮也要持续感知位置”的控件，例如自定义按钮、画布预览、图形项热区、时间轴游标。

它和 `QMouseEvent` 的差异在于语义：鼠标事件围绕按钮和移动，hover 事件围绕命中区域内的悬停状态。你可以把它看成“更适合做 UI 反馈的指针存在感知”。

## 2. 类说明

`QHoverEvent` 继承自 `QSinglePointEvent`。它自身提供上一位置 `oldPos()` / `oldPosF()`，当前坐标则由父类的 `position()`、`scenePosition()`、`globalPosition()` 提供。

类说明只用于表明这些 API 来自 `QHoverEvent`：旧位置和悬停事件构造属于悬停事件本身，设备、坐标、修饰键等来自输入事件基类体系。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `QHoverEvent(type, scenePos, globalPos, oldPos, modifiers, device)` | 构造悬停事件，类型必须是 HoverEnter、HoverMove 或 HoverLeave。 |
| `oldPos() const` | 返回上一局部位置的整数版本；旧代码兼容时使用。 |
| `oldPosF() const` | 返回上一局部位置的浮点版本，Qt 6 下更适合高 DPI 和精细交互。 |
| `position() const` | 来自父类，当前悬停点在接收对象内的位置。 |
| `scenePosition() const` | 来自父类，当前悬停点在窗口或场景中的位置。 |
| `globalPosition() const` | 来自父类，当前悬停点在屏幕中的位置。 |

## 4. 关键用法

### 启用 hover 感知

Widgets 里要接收 hover 事件，常见做法是设置 `Qt::WA_Hover`，再在 `event()` 中处理。

```cpp
HeatMap::HeatMap(QWidget *parent)
    : QWidget(parent)
{
    setAttribute(Qt::WA_Hover);
}

bool HeatMap::event(QEvent *event)
{
    if (event->type() == QEvent::HoverMove) {
        auto *hover = static_cast<QHoverEvent *>(event);
        updateHotCell(hover->position());
        return true;
    }

    return QWidget::event(event);
}
```

如果只需要鼠标按下拖动，不必使用 hover；如果需要无按钮移动反馈，hover 更贴合语义。

### 用 `oldPosF()` 计算悬停位移

当前点和旧点可以用于局部刷新、方向判断或小范围重绘。

```cpp
void Ruler::handleHover(QHoverEvent *event)
{
    const QRectF dirty = QRectF(event->oldPosF(), event->position())
        .normalized()
        .adjusted(-8, -8, 8, 8);

    update(dirty.toAlignedRect());
}
```

Qt 6 下优先使用浮点版本，避免高 DPI 缩放时出现边缘抖动。

### HoverEnter 的旧位置是哨兵值

进入时没有真实的上一个局部位置，`oldPosF()` 通常是 `(-1, -1)`。因此计算位移前要判断事件类型。

```cpp
if (event->type() == QEvent::HoverMove)
    movePreview(event->position() - event->oldPosF());
```

## 5. 使用场景

`QHoverEvent` 适合自定义控件高亮、图表数据点提示、时间轴预览、颜色拾取器、热点检测、图形编辑器辅助线、复杂按钮的分区反馈。

它也适合优化重绘。相比每次鼠标移动都全控件刷新，hover 事件提供旧位置，可以只刷新旧热点和新热点附近区域。

在 Graphics View 和 Qt Quick 风格的交互中，hover 是非常自然的输入层：指针还没有按下，但界面已经可以给出可点击、可拖拽、可编辑的暗示。

## 6. 常见坑与经验

不要忘记启用 hover。没有 `Qt::WA_Hover` 时，很多 Widgets 不会收到 `QHoverEvent`。

不要把 HoverLeave 的位置当作一定落在控件外的可靠坐标。离开语义本身比坐标更重要。

不要在 HoverMove 里做太重的计算。它可能非常频繁，应缓存命中结果、限制重绘范围。

不要用整数旧坐标做精细交互。`oldPos()` 会丢掉小数部分，优先用 `oldPosF()`。

## 7. 知识点覆盖

学习 `QHoverEvent` 应覆盖 hover 启用、HoverEnter/HoverMove/HoverLeave、上一位置、局部增量、高 DPI 浮点坐标、热点检测、局部重绘、鼠标移动事件区别和控件反馈设计。
