# QOpenGLPaintDevice 绘制设备笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QOpenGLPaintDevice>`  
> 所属模块：`Qt6::OpenGL`  
> 继承：`QPaintDevice`  
> 定位：让 `QPainter` 把绘制命令输出到当前 OpenGL context

## 它解决什么问题

`QOpenGLPaintDevice` 是 `QPainter` 和 OpenGL 之间的桥。普通 `QPainter` 需要一个 `QPaintDevice`，而 OpenGL 渲染目标通常是当前 context 的默认 framebuffer 或某个 FBO。这个类把当前 OpenGL context 包装成一个 paint device，让文字、路径、图片、基础 2D 图形可以用 `QPainter` 画进 OpenGL 渲染流程。

它不负责创建窗口、surface 或 FBO，也不是一个离屏图片容器。构造时它捕获当前 OpenGL context，之后 `QPainter` 在它上面绘制时会改动 OpenGL 状态。它适合“OpenGL 场景里叠 UI/文字/标注”或“Qt 绘制 API 输出到 FBO”的场景，不适合追求软件绘制完全一致的高质量排版/抗锯齿结果。

## 实际使用场景

- 在 `QOpenGLWidget::paintGL()` 末尾用 `QPainter` 绘制 FPS、坐标轴标签、调试文本；
- 先绑定一个 `QOpenGLFramebufferObject`，再用 `QOpenGLPaintDevice` 让 `QPainter` 画入离屏纹理；
- 在自定义 OpenGL 渲染管线中偶尔复用 Qt 的 2D 绘制能力，而不重写文字/路径绘制；
- 在不同 OpenGL 目标之间切换时，通过重写 `ensureActiveTarget()` 重新绑定目标 FBO。

## 最小使用模型

```cpp
#include <QOpenGLPaintDevice>
#include <QPainter>

void paintOverlay(const QSize &pixelSize)
{
    QOpenGLPaintDevice device(pixelSize);
    QPainter painter(&device);
    painter.setPen(Qt::white);
    painter.drawText(QPointF(12, 24), "OpenGL overlay");
}
```

这段代码必须运行在已有 current `QOpenGLContext` 的地方，例如 `QOpenGLWidget::paintGL()` 或手动 `makeCurrent()` 之后。`size` 是设备像素尺寸；高 DPI 下要同步设置 device pixel ratio。

## 核心语义

### 构造时绑定当前 context

`QOpenGLPaintDevice()`、`QOpenGLPaintDevice(const QSize &)`、`QOpenGLPaintDevice(int, int)` 都创建一个面向当前 context 的绘制设备。没有 current context，或者后续在另一个不匹配的 context 中使用，都会让行为变得不可预测。

### `QPainter` 会修改 OpenGL 状态

OpenGL paint engine 为了绘制会改 shader program、viewport、texture unit、buffer、blend、draw mode 等状态。文档明确提醒：不要假设绘制结束后 OpenGL 状态会自动恢复到原样。混合原生 OpenGL 与 `QPainter` 时，应使用 `QPainter::beginNativePainting()` / `endNativePainting()` 标记原生绘制区间。

### 性能强，质量边界不同

OpenGL paint engine 通常硬件加速，适合大量简单叠加绘制。但抗锯齿依赖 multisampling，质量可能不如软件 paint engine；频繁状态切换也会损害性能。绘制命令应按材质/状态尽量集中。

### `ensureActiveTarget()` 是目标重绑钩子

默认实现什么也不做。若你有多个 `QOpenGLPaintDevice` 轮流画入不同 FBO，可以派生并重写它，在 Qt 即将绘制时重新绑定正确 framebuffer 或 context。`beginNativePainting()` 也会触发该回调。

## API 速查表

| API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- |
| `QOpenGLPaintDevice()` | 创建没有显式尺寸的 OpenGL paint device。 | 构造时依赖当前 context；通常随后调用 `setSize()`。 |
| `QOpenGLPaintDevice(const QSize &size)` | 创建指定像素尺寸的绘制设备。 | `size` 是像素尺寸，不是逻辑点尺寸。 |
| `QOpenGLPaintDevice(int width, int height)` | 以宽高创建绘制设备。 | 与 `QSize` 构造等价；仍要求当前 context 有效。 |
| `~QOpenGLPaintDevice()` | 销毁绘制设备。 | 不拥有 context 或 FBO；不要把它当资源释放器。 |
| `context() const` | 返回构造时关联的 `QOpenGLContext`。 | 可用来排查是否在错误 context 中使用。 |
| `size() const` | 返回设备像素尺寸。 | 影响 `QPainter` viewport/metric。 |
| `setSize(const QSize &size)` | 修改设备像素尺寸。 | 窗口或 FBO resize 后要同步更新。 |
| `setDevicePixelRatio(qreal devicePixelRatio)` | 设置高 DPI 设备像素比。 | 让 `QPainter` 的逻辑坐标与实际像素匹配。 |
| `dotsPerMeterX() const` | 返回水平像素密度。 | 影响依赖物理尺寸的绘制度量。 |
| `dotsPerMeterY() const` | 返回垂直像素密度。 | 与字体/物理尺寸相关计算有关。 |
| `setDotsPerMeterX(qreal dpmx)` | 设置水平像素密度。 | 需要精确物理度量时再改，普通 overlay 通常不用。 |
| `setDotsPerMeterY(qreal dpmy)` | 设置垂直像素密度。 | 与 `setDotsPerMeterX()` 保持一致可避免比例异常。 |
| `setPaintFlipped(bool flipped)` | 设置绘制是否沿 Y 轴翻转。 | 用来协调 OpenGL 左下原点和 Qt 左上原点的差异。 |
| `paintFlipped() const` | 查询是否启用 Y 轴翻转。 | 排查文字/图像上下颠倒时先看它。 |
| `ensureActiveTarget()` | 绘制前确保目标 framebuffer/context 已激活。 | 默认无操作；多 FBO 轮流绘制时可重写。 |
| `paintEngine() const` | 返回 Qt 使用的 OpenGL paint engine。 | 通常由 `QPainter` 调用，业务代码很少直接用。 |
| `metric(QPaintDevice::PaintDeviceMetric metric) const` | 向 `QPainter` 提供尺寸、DPI、DPR 等设备指标。 | protected 重写；自定义派生类一般不必再改。 |

## 常见误区

### 在构造函数里创建并长期跨 context 使用

它捕获的是当前 context，而不是“未来会出现的任意 OpenGL 环境”。建议在 GL 生命周期明确的位置创建或更新，例如 `initializeGL()`/`paintGL()`。

### 以为 `QPainter` 结束后 OpenGL 状态完整恢复

`QPainter` 会改变当前 OpenGL 状态。绘完 2D 后继续原生渲染，要重新绑定 program、VAO、FBO、纹理和关键状态。

### 把它当成高质量打印/排版设备

它的优势是把 Qt 2D 绘制嵌进 GPU 管线；若目标是最高质量文本/矢量输出，软件 paint device 或专门的文本渲染路径通常更可控。

## 一句话总结

`QOpenGLPaintDevice` 让 `QPainter` 能画到当前 OpenGL 目标；它省掉 2D overlay 的大量底层工作，但也把 OpenGL 状态管理责任留给调用者。
