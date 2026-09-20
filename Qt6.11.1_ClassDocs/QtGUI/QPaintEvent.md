# QPaintEvent

> Qt 6.11.1 · Qt GUI · 来自 `QPaintEvent`

## 1. 先建立直觉

`QPaintEvent` 表示某个绘制设备的指定区域需要重新绘制。它携带的是“脏区域”，也就是 Qt 认为这次必须更新的矩形或区域。真正绘制由你在 `paintEvent()` 中用 `QPainter` 完成。

它的核心价值不是告诉你“现在可以画了”这么简单，而是告诉你“尽量只画这些区域”。对于大画布、表格、图像查看器、实时图表，正确利用 `rect()` / `region()` 可以显著减少重绘成本。

## 2. 类说明

`QPaintEvent` 继承自 `QEvent`。Widgets 中通常通过 `QWidget::paintEvent()` 接收；窗口或其他绘制设备也可能有自己的绘制流程。

类说明只用于表明这些 API 来自 `QPaintEvent`：脏矩形和脏区域属于绘制事件本身；画笔、画刷、字体、变换和合成模式由 `QPainter` 管理。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `QPaintEvent(paintRect)` | 构造一个矩形脏区域的绘制事件。 |
| `QPaintEvent(paintRegion)` | 构造一个任意区域的绘制事件。 |
| `rect() const` | 返回需要重绘区域的包围矩形，快速裁剪时常用。 |
| `region() const` | 返回精确脏区域，适合复杂局部重绘。 |
| `type()` | 来自 `QEvent`，绘制事件通常为 `QEvent::Paint`。 |

## 4. 关键用法

### 在 `paintEvent()` 内创建 `QPainter`

```cpp
void MeterWidget::paintEvent(QPaintEvent *event)
{
    QPainter painter(this);
    painter.setClipRegion(event->region());

    drawBackground(&painter, event->rect());
    drawNeedle(&painter);
}
```

对 `QWidget` 来说，通常只应在 `paintEvent()` 内对该控件创建 `QPainter`。业务状态变化时调用 `update()`，让 Qt 稍后合并并派发绘制事件。

### 用脏区域减少绘制量

```cpp
void TileCanvas::paintEvent(QPaintEvent *event)
{
    QPainter painter(this);

    for (const QRect &tileRect : visibleTiles(event->rect()))
        paintTile(&painter, tileRect);
}
```

如果每次都绘制整个大画布，滚动和局部变化会变慢。`rect()` 是粗略但便宜的入口，`region()` 更精确但处理成本略高。

### 用 `update(rect)` 触发局部重绘

```cpp
void Waveform::setCursorPosition(int x)
{
    const QRect oldRect = cursorRect(m_cursorX);
    m_cursorX = x;
    update(oldRect | cursorRect(m_cursorX));
}
```

不要直接调用 `paintEvent()`。`update()` 会把多次请求合并，等事件循环合适时统一重绘；`repaint()` 会更急迫，通常只在极少数需要同步刷新的场景使用。

## 5. 使用场景

`QPaintEvent` 是所有自绘 Widgets 的基础：图表、仪表盘、流程图、图像编辑器、代码编辑器、波形、棋盘、地图、时间轴、CAD 视图等。

它也用于性能优化。复杂控件可以把静态背景缓存到 pixmap，把动态小区域通过 `update(rect)` 请求局部刷新，再在绘制事件里根据脏区域决定画什么。

在高 DPI 环境下，`QPaintEvent` 的坐标仍是设备无关坐标；真正像素缓存和图像资源要结合 `devicePixelRatioF()` 管理。

## 6. 常见坑与经验

不要在 `paintEvent()` 里修改会立即触发布局或重绘的业务状态。绘制应尽量是当前状态的纯呈现，否则容易产生更新循环。

不要长期保存 `QPainter` 或 `QPaintEvent`。绘制上下文只在当前绘制阶段有效。

不要忽略裁剪。即使你不手动设置 clip，Qt 也会做一定裁剪；但复杂控件自己根据 `rect()` / `region()` 少做工作，收益更明显。

不要在后台线程直接绘制 QWidget。后台线程可以准备 `QImage` 数据，最终显示仍应回到 GUI 线程。

不要把 `rect()` 当成唯一精确区域。它是 `region()` 的包围矩形，可能包含实际不需要更新的区域。

## 7. 知识点覆盖

学习 `QPaintEvent` 应覆盖 QWidget 绘制生命周期、`QPainter` 使用时机、脏矩形、脏区域、`update()` 合并、局部重绘、裁剪、高 DPI、缓存策略、GUI 线程绘制和避免重绘递归。
