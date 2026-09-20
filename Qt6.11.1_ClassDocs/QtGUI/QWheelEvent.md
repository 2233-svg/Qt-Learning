# QWheelEvent

> Qt 6.11.1 · Qt GUI · 来自 `QWheelEvent`

## 1. 先建立直觉

`QWheelEvent` 描述滚轮、触摸板滚动和类似设备产生的滚动输入。它不是简单的“鼠标滚轮转了几格”：现代平台上滚动可能有像素级位移、滚动开始/更新/惯性/结束阶段，也可能受系统“自然滚动”设置影响。

写滚动交互时，最重要的判断顺序是：如果 `pixelDelta()` 有值，优先用它实现细腻滚动；否则再用 `angleDelta()` 按传统滚轮刻度换算。这样鼠标滚轮和高精度触摸板都能获得接近平台原生的手感。

## 2. 类说明

`QWheelEvent` 继承自 `QSinglePointEvent`。位置、按钮和修饰键状态来自父类；滚动距离、滚动阶段和方向反转状态来自 `QWheelEvent` 自身。

类说明只用来表明这些 API 来自 `QWheelEvent`：`pixelDelta()`、`angleDelta()`、`phase()`、`inverted()` 是滚动事件特有信息，和普通鼠标移动事件不是一回事。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `QWheelEvent(pos, globalPos, pixelDelta, angleDelta, buttons, modifiers, phase, inverted, source, device)` | 构造滚轮事件，常用于测试、自定义输入转发或事件合成。 |
| `pixelDelta() const` | 返回像素级滚动距离，高精度触摸板优先使用；可能为空。 |
| `angleDelta() const` | 返回滚轮角度增量，单位是 1/8 度；传统鼠标滚轮常见一步为 120。 |
| `phase() const` | 返回滚动阶段，如开始、更新、惯性、结束；平台支持程度不同。 |
| `inverted() const` | 表示 delta 是否受系统反向滚动设置影响。 |
| `isBeginEvent() const` | 判断滚动是否开始，或父类意义上的单点开始事件。 |
| `isUpdateEvent() const` | 判断滚动是否处于更新或惯性阶段。 |
| `isEndEvent() const` | 判断滚动是否结束，或父类意义上的单点结束事件。 |
| `position() const` | 来自父类，滚动发生时光标在接收对象中的位置。 |

## 4. 关键用法

### 优先使用 `pixelDelta()`

`pixelDelta()` 表示屏幕像素意义上的滚动距离，适合触摸板、Magic Mouse 等高精度设备。它为空时，再退回 `angleDelta()`。

```cpp
void ImageView::wheelEvent(QWheelEvent *event)
{
    const QPoint pixelDelta = event->pixelDelta();
    if (!pixelDelta.isNull()) {
        scrollBy(pixelDelta);
        event->accept();
        return;
    }

    const QPoint angleDelta = event->angleDelta();
    if (!angleDelta.isNull()) {
        scrollBy(QPoint(angleDelta.x(), angleDelta.y()) / 8 / 15 * m_lineHeight);
        event->accept();
        return;
    }

    event->ignore();
}
```

传统滚轮常见 120 表示 15 度，也就是一格。高分辨率滚轮可能发出小于 120 的值，这时可以累计增量，或实现部分滚动。

### `Ctrl + wheel` 常用于缩放

许多桌面应用把按住 Ctrl 的滚动解释为缩放，把普通滚动解释为移动视口。

```cpp
void Canvas::wheelEvent(QWheelEvent *event)
{
    if (event->modifiers().testFlag(Qt::ControlModifier)) {
        const qreal steps = event->angleDelta().y() / 120.0;
        zoomAt(event->position(), std::pow(1.15, steps));
        event->accept();
        return;
    }

    QAbstractScrollArea::wheelEvent(event);
}
```

缩放时通常使用 `position()` 作为锚点：用户滚哪里，就以哪里为中心缩放。

### 滚动阶段能改善触摸板体验

支持滚动阶段的平台会发送 `Qt::ScrollBegin`、`Qt::ScrollUpdate`、`Qt::ScrollMomentum`、`Qt::ScrollEnd`。开始和结束事件的 delta 可能为零，所以不要把零 delta 直接当作无效事件。

```cpp
void Timeline::wheelEvent(QWheelEvent *event)
{
    if (event->phase() == Qt::ScrollBegin)
        beginSmoothScroll();
    else if (event->phase() == Qt::ScrollEnd)
        endSmoothScroll();

    applyScrollDelta(event->pixelDelta().isNull()
        ? event->angleDelta() / 8
        : event->pixelDelta());

    event->accept();
}
```

## 5. 使用场景

`QWheelEvent` 适合滚动区域、图像查看器、地图、时间轴、代码编辑器、数据表、3D 视图缩放、音视频轨道浏览等所有连续浏览类交互。

在触摸板越来越普遍的桌面环境里，好的滚轮处理应避免只按“每次 120 一格”写死。支持 `pixelDelta()`、小增量累计和滚动阶段，能明显提升顺滑感。

它也经常和 `QScroller`、`QScrollArea`、`QAbstractScrollArea` 的默认行为协作。自定义控件不需要完全重写滚动体系；只有当默认滚动无法表达业务含义时，才拦截并接受事件。

## 6. 常见坑与经验

不要只处理 `angleDelta().y()`。一些设备支持水平滚动，`angleDelta().x()` 或 `pixelDelta().x()` 同样有意义。

不要假设 `pixelDelta()` 永远可靠。某些平台没有像素级滚动数据，某些 X11 驱动的数据也可能不稳定；稳妥做法是优先用，有则用，没有再退回角度。

不要忽略 `phase()` 中 delta 为零的开始和结束事件。它们对状态初始化、结束惯性动画、恢复吸附位置很有用。

不要随意反转 delta。系统已经根据用户设置给出了滚动方向，`inverted()` 是告诉你这种情况存在。只有少数控件，例如模拟实体旋钮或特殊滑块，才需要选择绕过系统习惯。

## 7. 知识点覆盖

学习 `QWheelEvent` 应覆盖传统滚轮刻度、高精度触摸板、像素滚动、角度滚动、水平滚动、滚动阶段、自然滚动方向、惯性滚动、缩放锚点、事件接受与默认滚动区域协作、高 DPI 坐标和跨平台输入差异。
