# QQuickPaintedItem：用 QPainter 绘制 Qt Quick 自定义项

> Qt 6.11.1 | `#include <QQuickPaintedItem>` | CMake: `Qt6::Quick`

`QQuickPaintedItem` 让已有的 `QPainter` 绘制逻辑进入 QML scene graph。它解决快速复用 2D 绘制代码的需求，例如波形、图表、标注、打印风格图元，而无需直接实现 `QSGNode`。

代价是渲染通常先画到 `QImage` 再上传为纹理。对高频、大面积、性能敏感内容，直接 scene graph 节点或 RHI 自定义渲染通常更合适。

## 最小派生类

```cpp
class Sparkline final : public QQuickPaintedItem
{
    Q_OBJECT
    QML_ELEMENT

public:
    void paint(QPainter *painter) override
    {
        painter->setPen(Qt::cyan);
        painter->drawPolyline(m_points);
    }

    void setPoints(QPolygonF points)
    {
        m_points = std::move(points);
        update();
    }

private:
    QPolygonF m_points;
};
```

`paint()` 在 item 的局部坐标绘制。默认底层 texture 大小为 item 尺寸乘窗口 device pixel ratio；设置 `textureSize` 可覆盖它。`update(rect)` 只是排队请求下一帧的重绘，不能期望立即调用 `paint()`，且 item 不可见时不重绘。

## 线程与对象创建

在 threaded scene graph 上，`paint()` 运行在渲染线程，调用期间 GUI 线程被阻塞。因此直接读取 item 的 GUI 属性在此点是安全的，但不要在 `paint()` 中随意创建 QObject、发信号、启动 timer 或做会留下渲染线程亲和性对象的事。

属性 setter 中修改数据后调用 `update()`；绘制函数只根据已经准备好的状态发出 QPainter 命令。

## renderTarget 的质量和性能取舍

`Image` 是默认 target：QPainter 用 raster engine 画进 QImage，抗锯齿质量好、resize 快，但大纹理上传可能昂贵。

Qt 6.9 起，`FramebufferObject` 和 `InvertedYFramebufferObject` 在实际 OpenGL 后端可启用硬件加速；其它渲染 API 会忽略它们。FBO 避免图像上传，通常更快，但抗锯齿质量会下降，且 resize 很昂贵。Qt 6.0 到 6.8 中 FBO target 在所有后端都被忽略。

`FastFBOResizing` 在 Qt 6 已被忽略，不要把它当作优化开关。

## 绘制相关开关

- `fillColor`：`paint()` 前填充底图；透明内容通常设透明色。
- `setOpaquePainting(true)`：只有内容每像素都不透明时才设，可避免合成混合。
- `setMipmap(true)`：缩小时能减轻锯齿，也增加资源和生成成本。
- `setAntialiasing(true)`：请求 QPainter 抗锯齿。

## API 速查表

| API | 语义 | 关键边界 |
|---|---|---|
| `paint(QPainter *)` | 绘制 item 内容 | 纯虚；在渲染线程调用，避免创建线程亲和性 QObject |
| `update(QRect)` | 请求下帧重绘区域 | 异步调度，不立即 paint，item 不可见时可能不画 |
| `textureSize` | 指定底层 texture 尺寸 | 默认取 item size * DPR；过大增加内存与绘制成本 |
| `fillColor` | 绘制前的背景填充色 | 对透明图元使用透明色，避免不期望背景 |
| `Image` render target | 使用 QImage/raster paint engine | 默认，质量好但可能有上传成本 |
| `FramebufferObject` / `InvertedYFramebufferObject` | 选择 OpenGL FBO 目标及镜像版本 | Qt 6.9 起仅 OpenGL 有效；频繁 resize 成本高 |
| `setOpaquePainting()` | 标注内容不透明 | 仅在完全不透明时设置，否则合成结果错误 |
| `setMipmap()` / `setAntialiasing()` | 控制缩放质量与画笔抗锯齿 | 都可能增加处理或显存开销 |
| `FastFBOResizing` | 历史性能提示 | Qt 6 中已忽略 |

## 相关类型

- `QPainter`：实际 2D 绘制 API。
- `QSGNode`：需要更高性能或原生 scene graph 控制时的替代方案。
- `QQuickFramebufferObject`：遗留的 OpenGL FBO 自定义渲染通道，不同于 QPainter bridge。
