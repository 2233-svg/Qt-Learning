# QBackingStore

> Qt 6.11.1 · Qt GUI · 来自 `QBackingStore`

## 1. 先建立直觉

`QBackingStore` 是 `QWindow` 的软件后备缓冲。它让你先在离屏绘制设备上用 `QPainter` 完成绘制，再把指定区域一次性 flush 到窗口 surface，避免直接在屏幕表面逐笔绘制造成闪烁或平台差异。

它最适合没有 QWidget 层、但仍希望使用 `QPainter` 自己实现窗口渲染的场景。核心顺序固定：窗口尺寸变化时 `resize()`，绘制前 `beginPaint()`，在 `paintDevice()` 上绘制，调用 `endPaint()`，最后 `flush()`。

## 2. 类说明

`QBackingStore` 不继承 `QObject`，但与一个 `QWindow` 强绑定。`paintDevice()` 返回的设备只在 `beginPaint()` 和 `endPaint()` 之间有效；底层平台 handle 也只适合非常底层的插件/平台集成，普通应用不应直接依赖。

类说明只用于表明这些 API 来自 `QBackingStore`。它是软件渲染路径，不等同于 OpenGL/Vulkan/QRhi 的 swapchain；GPU 渲染窗口应使用对应图形后端的生命周期。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `QBackingStore(window)` | 为顶层 `QWindow` 创建后备缓冲。 |
| `resize(size)` | 调整后备缓冲尺寸，应随窗口尺寸变化调用。 |
| `size() const` | 返回当前后备缓冲逻辑尺寸。 |
| `beginPaint(region)` | 开始对指定脏区域进行绘制。 |
| `paintDevice()` | 返回当前可绘制设备，仅在 begin/end 之间有效。 |
| `endPaint()` | 结束绘制阶段。 |
| `flush(region, window, offset)` | 将区域提交到目标窗口或其子窗口。 |
| `scroll(area, dx, dy)` | 尝试在后备缓冲中移动已有像素，减少重绘。 |
| `setStaticContents(region)` | 标记静态内容区域，辅助优化 resize 或重绘。 |
| `staticContents()` / `hasStaticContents()` | 查询已声明的静态区域。 |
| `window() const` | 返回关联的顶层窗口。 |
| `handle() const` | 返回平台后备缓冲 handle，通常只供平台插件使用。 |

## 4. 关键用法

### 最小渲染循环

```cpp
void RasterWindow::renderNow()
{
    if (!isExposed())
        return;

    const QRegion dirty(rect());
    m_backingStore.beginPaint(dirty);

    QPainter painter(m_backingStore.paintDevice());
    painter.fillRect(rect(), Qt::white);
    painter.drawText(rect(), Qt::AlignCenter, tr("Software-rendered window"));

    m_backingStore.endPaint();
    m_backingStore.flush(dirty);
}
```

`QPainter` 的作用域必须在 `endPaint()` 前结束。最简单的写法是像示例这样把 painter 放在局部块中，确保其析构后再调用 `endPaint()`。

### resize 时同步后备缓冲

```cpp
void RasterWindow::resizeEvent(QResizeEvent *event)
{
    m_backingStore.resize(event->size());
    renderNow();
}
```

如果不 resize，后备缓冲尺寸与窗口不一致，轻则内容拉伸或缺边，重则绘制越界或提交异常。

### 用 `scroll()` 复用已有像素

```cpp
if (m_backingStore.scroll(viewportRegion, 0, -lineHeight)) {
    updateOnlyExposedStrip();
} else {
    repaintViewport();
}
```

它适合文本视图、终端、时间轴等大部分内容只是平移的情况。返回 false 时必须准备完整重绘，因为平台后备存储不一定支持像素滚动优化。

### 子窗口 flush 要传对 offset

如果为 transient 或 child `QWindow` flush，region 使用子窗口局部坐标，offset 是它相对于顶层 backing-store 窗口的位置。普通顶层窗口可直接使用默认参数。

## 5. 使用场景

`QBackingStore` 适合纯 `QWindow` 软件渲染、嵌入式设备 UI、简单 2D 可视化、无 Widgets 的工具窗口、平台插件开发和需要完全控制脏区域的渲染循环。

使用 `QWidget` 时，Qt 已经维护内部后备缓冲；使用 `QOpenGLWindow`、Vulkan 或 QRhi 时，有各自的 GPU 渲染路径。不要为了“更底层”而把成熟控件硬改成手工 backing store。

## 6. 常见坑与经验

不要缓存 `paintDevice()` 返回指针。它只在 begin/end 绘制区间内有效。

不要遗漏 `endPaint()` 或在它之后继续绘制。这样会破坏后备存储状态，后续 flush 行为不可预测。

不要只调用 `beginPaint()` 而从不 `flush()`。离屏缓冲里的内容不会自动显示到窗口。

不要在窗口未 exposed 时频繁 flush。结合 `QWindow::isExposed()` 合并渲染请求，可以避免最小化或遮挡时浪费绘制。

不要把 static contents 当成永远不会变的硬约束。只有确实长期不变的区域才标记，否则优化提示会反过来造成残影。

不要跨线程访问关联窗口或后备缓冲。窗口和 GUI 绘制必须遵守 GUI 线程规则。

## 7. 知识点覆盖

学习 `QBackingStore` 应覆盖软件双缓冲、`QWindow` 渲染循环、脏区域、begin/end/flush 协议、`QPainter` 生命周期、窗口 resize、像素滚动优化、静态内容、子窗口 offset、exposed 状态和 GUI 线程。
