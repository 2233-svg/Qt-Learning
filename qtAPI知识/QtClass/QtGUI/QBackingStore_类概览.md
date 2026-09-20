# QBackingStore：为 QWindow 维护可局部刷新的光栅绘制缓冲

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QBackingStore>`  
> 模块：Qt GUI，链接 `Qt6::Gui`  
> 关联类型：`QWindow`、`QPainter`、`QRegion`

## 它解决什么问题

直接在窗口屏幕表面绘制会导致闪烁，也难以只更新变化的小区域。`QBackingStore` 为一个 `QWindow` 保存离屏的光栅内容：先用 `QPainter` 画到缓冲区，再将指定区域一次性提交到屏幕。

它适用于 `QWindow` 的 `RasterSurface` 路径。若渲染目标是 OpenGL，应使用 `QOpenGLContext` 等 OpenGL 体系；若使用 `QWidget` 或 `QGraphicsView`，它们已有完整的绘制与缓冲管理，通常无需手工创建 `QBackingStore`。

## 典型场景

自定义轻量窗口需要用 `QPainter` 绘制，但不想引入 Widgets 或 Graphics View 的完整栈时，`QBackingStore` 是常见基础设施。例如仪表盘、简单画布、嵌入式控制面板或专用光栅窗口。

```cpp
void RasterWindow::renderNow()
{
    if (!isExposed())
        return;

    const QRegion dirty(rect());
    m_backingStore->beginPaint(dirty);

    QPainter painter(m_backingStore->paintDevice());
    painter.fillRect(rect(), Qt::white);
    painter.drawText(rect(), Qt::AlignCenter, tr("Ready"));
    painter.end();

    m_backingStore->endPaint();
    m_backingStore->flush(dirty);
}

void RasterWindow::resizeEvent(QResizeEvent *event)
{
    m_backingStore->resize(event->size());
    QWindow::resizeEvent(event);
}
```

实际程序通常在 `QWindow::exposeEvent()` 或处理 `QEvent::UpdateRequest` 时调用渲染，并在 `resizeEvent()` 中同步缓冲区大小。

## 严格的绘制时序

一次绘制必须遵循以下顺序：

1. 确定需要重画的 `QRegion`。
2. 调用 `beginPaint(region)`。
3. 取得 `paintDevice()`，在其上创建并结束 `QPainter`。
4. 调用 `endPaint()`。
5. 调用 `flush(region)` 将已完成的区域提交到屏幕。

`paintDevice()` 返回的指针只在 `beginPaint()` 与 `endPaint()` 之间有效，不能缓存到成员变量，更不能在下一帧复用。调用 `endPaint()` 前也必须先销毁或 `end()` 掉 `QPainter`，否则平台后端可能仍持有绘制状态。

`beginPaint()` 的区域并不是“建议重画范围”。调用方应只依赖该区域内能被安全更新的内容，并在 `flush()` 时提交实际已完成的脏区。

## `flush()` 的窗口与坐标边界

省略 `window` 时，`flush()` 使用该 backing store 对应的顶层窗口。显式传入的窗口只能是这个顶层窗口，或它的非 transient 子窗口。

若刷新的目标是子窗口：

- `region` 使用**子窗口自身坐标**。
- `offset` 使用该子窗口相对 backing store 顶层窗口的偏移。

把顶层坐标区域与子窗口坐标混用，会出现内容偏移、裁剪或未更新。`flush()` 必须在 `endPaint()` 之后调用。

## 滚动与静态区域

`scroll(area, dx, dy)` 尝试在缓冲区内移动像素，成功返回 `true`。它只复制已有像素，不会生成移动后暴露出的新内容；调用方仍要把新暴露区域计入脏区并重绘。`dx`、`dy` 可以为负数。

`setStaticContents()` 用 `QRegion` 标明当前窗口中静态内容的区域，可供平台后端优化窗口表面的管理。它不是自动缓存或防止重绘的开关：标为静态的内容仍由应用保证正确，窗口尺寸、内容或设备像素比改变时也需要重新评估这一区域。

## 所有权与平台接口

构造函数只关联一个顶层 `QWindow`，不拥有窗口。窗口应在 backing store 存活期间有效，因此惯例是让 `QBackingStore` 成为窗口的成员或由与窗口同生命周期的智能指针管理。

`handle()` 返回底层 `QPlatformBackingStore`，属于平台插件实现细节。普通应用不应依赖它的具体类型或长期保存它；跨平台绘制应使用公开的 `QBackingStore` API。

这组对象应在拥有 `QWindow` 的 GUI 线程中创建和使用。不要在工作线程中同时调整窗口、绘制缓冲和提交表面。

## API 速查表

| API | 含义 | 重点边界 |
| --- | --- | --- |
| `QBackingStore(QWindow *window)` | 为顶层窗口创建空的光栅缓冲表面。 | 不拥有 `window`；窗口必须在缓冲对象存活期间有效。 |
| `~QBackingStore()` | 销毁缓冲表面。 | 应先结束正在进行的绘制。 |
| `QWindow *window() const` | 返回关联的顶层窗口。 | 返回非拥有指针。 |
| `void resize(const QSize &size)` | 改变缓冲表面尺寸。 | 通常在 `QWindow::resizeEvent()` 中同步调用。 |
| `QSize size() const` | 返回当前缓冲表面尺寸。 | 不等同于任意子窗口尺寸。 |
| `void beginPaint(const QRegion &region)` | 开始在指定区域绘制。 | 必须先于 `paintDevice()` 和 `QPainter` 使用。 |
| `QPaintDevice *paintDevice()` | 返回当前绘制目标。 | 仅在 `beginPaint()` 到 `endPaint()` 之间有效，不可缓存。 |
| `void endPaint()` | 结束一次绘制区间。 | 调用前先结束 `QPainter`；随后才能 `flush()`。 |
| `void flush(const QRegion &region, QWindow *window = nullptr, const QPoint &offset = {})` | 将区域提交到屏幕。 | 必须在 `endPaint()` 后；子窗口时 region 用子坐标，offset 用相对顶层偏移。 |
| `bool scroll(const QRegion &area, int dx, int dy)` | 在缓冲中移动已有像素。 | 成功只代表移动完成，暴露区域仍需重绘。 |
| `void setStaticContents(const QRegion &region)` | 标记静态内容区域。 | 只是优化提示，应用仍负责内容正确性。 |
| `QRegion staticContents() const` | 返回已标记的静态区域。 | 应在尺寸或内容变化后重新检查其有效性。 |
| `bool hasStaticContents() const` | 判断是否存在静态区域。 | 不表示区域一定无需重绘。 |
| `QPlatformBackingStore *handle() const` | 返回平台后端实现指针。 | 平台私有接口，普通应用不要依赖具体实现。 |
