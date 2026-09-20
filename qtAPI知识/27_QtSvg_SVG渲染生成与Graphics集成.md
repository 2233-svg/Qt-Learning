# Qt SVG：渲染、生成与 Graphics 集成

> Qt SVG 把 SVG 文档解析为可绘制内容，既能直接显示，也能渲染到 QImage、QWidget 或 Graphics View。核心选择是：只显示文件用 `QSvgWidget`，需要控制绘制区域/动画用 `QSvgRenderer`，需要放入场景图用 `QGraphicsSvgItem`。

## 1. 模块与基本显示

```cmake
find_package(Qt6 REQUIRED COMPONENTS Widgets Svg SvgWidgets)
target_link_libraries(mytarget PRIVATE Qt6::Widgets Qt6::Svg Qt6::SvgWidgets)
```

```cpp
#include <QSvgWidget>

auto *svg = new QSvgWidget(QStringLiteral(":/icons/logo.svg"));
svg->setMinimumSize(200, 80);
svg->show();
```

`QSvgWidget` 是显示 SVG 文件的便捷 QWidget。它会根据 widget 尺寸绘制内容，适合图标、标志和静态插图。

## 2. QSvgRenderer：绘制到任意 QPaintDevice

```cpp
#include <QPainter>
#include <QSvgRenderer>

QSvgRenderer renderer(QStringLiteral(":/images/diagram.svg"));
QImage image(QSize(800, 400), QImage::Format_ARGB32_Premultiplied);
image.fill(Qt::transparent);

QPainter painter(&image);
renderer.render(&painter, QRectF(QPointF(0, 0), QSizeF(image.size())));
image.save(QStringLiteral("diagram.png"));
```

渲染器可以绘制到 QWidget、QImage、QPrinter 等 `QPaintDevice`。传入目标矩形会对 SVG viewBox 进行缩放；若要保持比例，先计算目标矩形或使用合适的变换。

### 2.1 自定义 Widget 中渲染

```cpp
class SvgView : public QWidget
{
protected:
    void paintEvent(QPaintEvent *) override
    {
        QPainter painter(this);
        renderer.render(&painter, rect());
    }
private:
    QSvgRenderer renderer{QStringLiteral(":/images/map.svg")};
};
```

文件加载失败时检查 `renderer.isValid()`，并在 UI 中显示占位状态，而不是绘制空白。

## 3. viewBox、元素和动画

`QSvgRenderer::viewBox()`/`viewBoxF()` 描述 SVG 的逻辑坐标区域。复杂 SVG 可以按元素 ID 渲染：

```cpp
const QStringList ids = renderer.elementIds();
if (ids.contains(QStringLiteral("warning"))) {
    QRectF bounds = renderer.boundsOnElement(QStringLiteral("warning"));
    renderer.render(&painter, bounds, QStringLiteral("warning"));
}
```

动画 SVG 可通过 `animationDuration()`、`currentFrame()`、`setCurrentFrame()` 和 `repaintNeeded` 信号驱动：

```cpp
connect(&renderer, &QSvgRenderer::repaintNeeded,
        this, QOverload<>::of(&QWidget::update));
renderer.setAnimationEnabled(true);
```

动画帧更新会触发重绘，复杂 SVG 应控制尺寸和刷新频率。

## 4. QGraphicsSvgItem

```cpp
#include <QGraphicsScene>
#include <QGraphicsSvgItem>

auto *scene = new QGraphicsScene;
auto *svgItem = new QGraphicsSvgItem(QStringLiteral(":/icons/marker.svg"));
svgItem->setPos(40, 30);
scene->addItem(svgItem);
```

`QGraphicsSvgItem` 将 SVG 作为 Graphics Item 放入 `QGraphicsScene`，可参与变换、裁剪和层级。多个 item 显示同一 SVG 时可以共享一个 `QSvgRenderer`：

```cpp
auto *renderer = new QSvgRenderer(QStringLiteral(":/icons/symbols.svg"), scene);
auto *a = new QGraphicsSvgItem;
auto *b = new QGraphicsSvgItem;
a->setSharedRenderer(renderer);
b->setSharedRenderer(renderer);
a->setElementId(QStringLiteral("pin"));
b->setElementId(QStringLiteral("home"));
scene->addItem(a);
scene->addItem(b);
```

`setSharedRenderer()` 不转移 renderer 所有权，renderer 的生命周期必须覆盖所有 item。默认会使用设备坐标缓存；缩放或频繁变换时应评估缓存模式和内存占用。

## 5. SVG 生成：QSvgGenerator

```cpp
#include <QSvgGenerator>
#include <QPainter>

QSvgGenerator generator;
generator.setFileName(QStringLiteral("output.svg"));
generator.setSize(QSize(640, 360));
generator.setViewBox(QRect(0, 0, 640, 360));
generator.setTitle(QStringLiteral("统计图"));

QPainter painter(&generator);
painter.setPen(Qt::blue);
painter.drawLine(20, 20, 620, 340);
painter.end();
```

`QSvgGenerator` 是一个 paint device，任何使用 QPainter 的绘制代码都可以输出 SVG。输出的是矢量指令，不是把屏幕截图嵌入 SVG；复杂渐变、字体和混合模式可能因 SVG 版本而有差异。

## 6. SVG 支持范围与安全

Qt SVG 主要支持 SVG Tiny 1.2 的静态特性，并扩展支持部分 mask、filter、pattern、marker 等功能。不是所有浏览器 SVG 特性都能完整解析，尤其是脚本、外部资源和高级滤镜。

对不可信 SVG 文件应限制加载路径和资源访问，避免把外部引用、巨大路径或恶意 XML 当作普通图标处理。解析错误通过 `QSvgRenderer::load()` 返回值和日志发现。

## 7. 高 DPI 与资源策略

SVG 本身具有缩放优势，但复杂路径在极大尺寸下仍会增加栅格化成本。静态图标可以放入 Qt Resource System；需要主题换色时保留元素 ID 或使用多份主题资源。不要在每次 paintEvent 中重新解析文件，复用 renderer。

## 8. 与 QPainter 混用

```cpp
void Widget::paintEvent(QPaintEvent *)
{
    QPainter painter(this);
    painter.save();
    painter.translate(20, 20);
    renderer.render(&painter, QRectF(0, 0, 120, 120));
    painter.restore();
    painter.drawText(10, height() - 10, QStringLiteral("说明"));
}
```

使用 `save()`/`restore()` 隔离 renderer 改变的画笔状态和变换，避免影响之后的文本或其他图形。

## 9. 常见问题

| 现象 | 原因 | 处理 |
| --- | --- | --- |
| SVG 空白 | 文件路径错误或 renderer 无效 | 检查资源路径和 `isValid()` |
| 图标被拉伸 | 目标矩形比例与 viewBox 不同 | 计算等比目标矩形 |
| Graphics item 崩溃 | shared renderer 提前销毁 | 延长 renderer 生命周期 |
| 动画不刷新 | 未连接 repaintNeeded 或未启用动画 | 连接 update 并设置 animationEnabled |
| 复杂 SVG 很慢 | 每次重绘都解析或路径过多 | 复用 renderer，考虑缓存和简化资源 |
| 浏览器显示不同 | 使用了 Qt 不支持的 SVG 特性 | 查支持范围并提供降级资源 |

## 10. 自测题

1. QSvgWidget、QSvgRenderer 和 QGraphicsSvgItem 如何选择？
2. `setSharedRenderer()` 是否转移 renderer 所有权？
3. QSvgGenerator 输出的是位图还是矢量指令？
4. 为什么 paintEvent 中不应每次重新解析 SVG？
5. SVG 的 viewBox 解决什么问题？

### 参考答案

1. 直接显示用 QSvgWidget；自定义绘制用 QSvgRenderer；场景图集成用 QGraphicsSvgItem。
2. 不转移，调用者必须保证 renderer 生命周期足够长。
3. 输出 QPainter 矢量绘制指令形成的 SVG 文档。
4. 解析成本高，会导致频繁重绘卡顿。
5. 提供逻辑坐标系，使内容可以按目标矩形缩放。

## 11. 小结

Qt SVG 的关键是复用解析结果、明确坐标和生命周期。静态图标用便捷控件，复杂绘制用 renderer，场景图中共享 renderer；生成 SVG 时把 QPainter 代码直接导向 QSvgGenerator，并对不支持的 SVG 特性和不可信输入做边界处理。
