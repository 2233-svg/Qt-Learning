# QPaintEngine：把 QPainter 命令落到具体绘制后端的抽象

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QPaintEngine>`  
> CMake：`find_package(Qt6 REQUIRED COMPONENTS Gui)`，并链接 `Qt6::Gui`  
> 相关类型：`QPainter`、`QPaintDevice`、`QPaintEngineState`、`QImage`、`QPixmap`

`QPaintEngine` 定义 `QPainter` 如何在某个 `QPaintDevice` 上执行绘制。它是 Qt 绘制系统的后端接口：应用调用 `QPainter::drawPath()`、`drawImage()`、`setPen()`；Qt 将这些请求转发为绘制引擎的状态更新与图元绘制调用。

常规应用几乎不应直接创建或调用 `QPaintEngine`。Qt 已为光栅图像、控件、OpenGL、打印和 PDF 等目标提供实现。只有需要让 `QPainter` 输出到新的图形 API、专有硬件或自定义矢量文件格式时，才需要同时实现 `QPaintDevice` 与 `QPaintEngine`。

## 它解决的问题

同一段 `QPainter` 代码可画到 `QImage`、`QWidget`、打印机和 PDF，原因不是这些对象内部实现完全相同，而是它们通过 `QPaintEngine` 提供统一后端协议：

```cpp
QPainter painter(device);
painter.setPen(QPen(Qt::darkBlue, 2));
painter.setBrush(Qt::cyan);
painter.drawEllipse(QRectF(20, 20, 120, 80));
```

大致流程如下：

1. `QPainter::begin()` 从目标 `QPaintDevice` 获取其 paint engine；
2. 引擎的 `begin(QPaintDevice *)` 初始化底层目标；
3. 当 painter 状态变化，Qt 调用 `updateState(QPaintEngineState)`；
4. 当需要绘制图元，Qt 调用 `drawPath()`、`drawPixmap()`、`drawPolygon()` 等；
5. `QPainter::end()` 使引擎执行 `end()`，提交或结束后端绘制。

`QPaintEngine` 因而隔离了“应用想画什么”和“平台如何画出来”。

## 实际使用场景

### 1. 普通应用：通过 QPainter 间接使用

```cpp
QImage image(QSize(800, 500), QImage::Format_ARGB32_Premultiplied);
image.fill(Qt::white);

QPainter painter(&image);
painter.setRenderHint(QPainter::Antialiasing);
painter.drawRoundedRect(QRectF(40, 40, 220, 120), 12, 12);
```

这里应用不需要知道实际引擎是哪个，也不应根据 `engine->type()` 写业务分支。Qt 会选择与 `QImage` 相配的后端，并处理可用功能与回退。

### 2. 实现专有绘制后端

例如将 `QPainter` 命令转换为自定义命令流：

```cpp
class CommandDevice : public QPaintDevice
{
public:
    QPaintEngine *paintEngine() const override;

protected:
    int metric(PaintDeviceMetric metric) const override;
};

class CommandEngine : public QPaintEngine
{
public:
    CommandEngine();

    bool begin(QPaintDevice *device) override;
    bool end() override;
    void updateState(const QPaintEngineState &state) override;
    void drawPixmap(const QRectF &, const QPixmap &, const QRectF &) override;
    Type type() const override { return User; }
};
```

这只是接口骨架。可工作的后端还必须正确处理状态脏标志、至少一个多边形绘制重载、目标度量、图像与文本回退，以及所声明的能力。

### 3. 为性能选择专用图元实现

默认实现会把部分图元转换后再绘制，例如椭圆可退化为多边形，整数矩形/线可转为浮点版本，文本可转成路径。对偶尔绘制这通常足够；自定义后端若大量绘制某类图元，应重写相应函数以避免转换与大量小调用。

## 核心模型与边界

### 引擎由绘制设备拥有

Qt 文档规定，`QPaintEngine` 由创建它的 `QPaintDevice` 创建并拥有。`QPaintDevice::paintEngine()` 返回的指针不转移所有权：

```cpp
QPaintEngine *engine = device->paintEngine();
// 不要 delete engine;
```

设备销毁、重建底层表面或结束绘制时，引擎的可用性都可能随之改变。应用代码不应缓存该指针，更不能让一个引擎服务于多个互不兼容的设备。

### `begin()` / `end()` 的生命周期

`begin(pdev)` 在目标设备上开始绘制时初始化后端，成功返回 `true`，失败返回 `false`。`end()` 结束当前绘制并同样以布尔值报告结果。

通常由 `QPainter::begin()`、构造 `QPainter(device)` 和 `QPainter::end()` 驱动它们。应用或引擎外部管理代码不应绕过 `QPainter` 手工调用 `begin()` / `end()`，否则可能破坏 painter、device 和 engine 的活动状态同步。

### `updateState()` 必须同步每个 dirty 状态

当 Qt 调用：

```cpp
void CommandEngine::updateState(const QPaintEngineState &state)
{
    const auto dirty = state.state();

    if (dirty.testFlag(QPaintEngine::DirtyPen))
        backendSetPen(state.pen());
    if (dirty.testFlag(QPaintEngine::DirtyTransform))
        backendSetTransform(state.transform());
}
```

引擎必须检查 `state.state()`，并更新每一个被置位的属性。忽略某个 dirty flag 会导致后续图元继续使用过时的笔、裁剪、透明度或变换；无条件同步全部状态则会增加后端状态切换开销。

详细 getter 与 flag 的对应关系见 `QPaintEngineState` 笔记。`AllDirty` 到来时，应当按完整状态重建后端上下文。

### 能力标志是承诺，不是愿望清单

构造函数接收 `PaintEngineFeatures`，`hasFeature()` 据此回答引擎是否原生支持某项能力。Qt 对大多数不支持的特性会尽力模拟：例如先在 `QImage` 中得到结果，再把 alpha 混合后的图像交给引擎。

但 `AlphaBlend` 和 `PorterDuff` 不能依赖这种通用模拟。若自定义后端实际无法正确实现它们，不能宣称支持；若业务依赖它们，后端必须给出正确结果或明确限制。

`hasFeature(features)` 的底层实现是按位相交判断。传入多个 flag 时，返回 `true` 表示**至少有一个**指定 bit 被支持，不表示“所有 flag 都支持”。需要验证多个能力时应逐项检查：

```cpp
const bool supportsPaths = engine->hasFeature(QPaintEngine::PainterPaths);
const bool supportsAA = engine->hasFeature(QPaintEngine::Antialiasing);
```

### 图元函数的最小实现要求

以下函数是纯虚函数，派生引擎必须实现：

- `begin(QPaintDevice *)`
- `end()`
- `updateState(const QPaintEngineState &)`
- `drawPixmap(const QRectF &, const QPixmap &, const QRectF &)`
- `type() const`

此外，Qt 文档要求两个 `drawPolygon()` 重载中至少重写一个。`drawPath()` 的基类默认实现会直接忽略路径；如果引擎要处理路径，或声明 `PainterPaths` 能力，就必须实现它或提供等价正确的分发。

### 线程与平台资源

引擎的线程规则来自其 `QPaintDevice` 和底层 API：窗口、`QPixmap`、打印机、OpenGL / Direct3D 上下文等通常必须在各自所属线程使用。`QPaintEngine` 本身不是跨线程命令队列；不要在一个线程更新状态、另一个线程调用绘制函数。

若后端需要后台渲染，建立清晰的命令缓冲和线程交接机制，而不是共享同一个活动 `QPainter` / `QPaintEngine`。

## 枚举与能力

### `DirtyFlag` / `DirtyFlags`

`DirtyFlags` 是可按位组合的 `QFlags<DirtyFlag>`，表示 painter 自上次同步后改变的状态：

| 标志 | 需要同步的状态 |
| --- | --- |
| `DirtyPen` | `QPaintEngineState::pen()` |
| `DirtyBrush` | `brush()` |
| `DirtyBrushOrigin` | `brushOrigin()` |
| `DirtyFont` | `font()` |
| `DirtyBackground` | `backgroundBrush()` |
| `DirtyBackgroundMode` | `backgroundMode()` |
| `DirtyTransform` | `transform()` |
| `DirtyClipRegion` | `clipRegion()` 与 `clipOperation()` |
| `DirtyClipPath` | `clipPath()` 与 `clipOperation()` |
| `DirtyHints` | `renderHints()` |
| `DirtyCompositionMode` | `compositionMode()` |
| `DirtyClipEnabled` | `isClipEnabled()` |
| `DirtyOpacity` | `opacity()` |
| `AllDirty` | 所有常规状态均须同步的便利组合。 |

### `PaintEngineFeature` / `PaintEngineFeatures`

| 能力组 | 枚举项 | 表示什么 |
| --- | --- | --- |
| 变换 | `PrimitiveTransform`、`PatternTransform`、`PixmapTransform`、`PerspectiveTransform` | 原生处理图元、图案、像素图或透视变换。 |
| 填充 | `PatternBrush`、`MaskedBrush`、`LinearGradientFill`、`RadialGradientFill`、`ConicalGradientFill`、`ObjectBoundingModeGradients` | 原生处理纹理、带 alpha 遮罩和多种渐变。 |
| 路径与描边 | `PainterPaths`、`BrushStroke` | 支持路径绘制 / 裁剪，以及以 brush 填充的笔划。 |
| 合成 | `AlphaBlend`、`PorterDuff`、`BlendModes`、`ConstantOpacity`、`RasterOpModes` | 支持 alpha、Porter-Duff、扩展混合模式、全局透明度和逻辑光栅操作。 |
| 质量与事件 | `Antialiasing`、`PaintOutsidePaintEvent` | 原生抗锯齿；或允许在 paint event 之外绘制。 |
| 便利项 | `AllFeatures` | 所有特性 bit 的组合。 |

未声明的能力不必然让绘制失败，Qt 可能通过 `QImage` 回退模拟；但模拟可能改变性能、精度、颜色管理或可用图像格式。

### `PolygonDrawMode`

| 模式 | 表示 |
| --- | --- |
| `OddEvenMode` | 使用奇偶填充规则绘制多边形。 |
| `WindingMode` | 使用 winding 填充规则绘制多边形。 |
| `ConvexMode` | 多边形为凸多边形，可用专门快路径。 |
| `PolylineMode` | 绘制折线，不进行填充。 |

### `Type`

`type()` 返回引擎类别，例如 `Raster`、`OpenGL`、`Pdf`、`SVG`、`Picture`、`Direct2D`。其中 `X11`、`Windows`、`QuickDraw`、`CoreGraphics` 等历史 / 平台类型不应被新业务代码当作功能检测依据。

自定义引擎可在 `User` 到 `MaxUser` 的用户类型范围中选择标识。真正的能力判断优先用 `hasFeature()`，而不是猜测某个平台类型一定支持某种混合或路径功能。

## 关键图元分发语义

| 函数族 | 基类行为与实现建议 |
| --- | --- |
| `drawRects()` | 默认可按能力将矩形转为路径或多边形；批量矩形很多时建议后端原生实现。 |
| `drawLines()` | 默认会把线逐条分发为路径或多边形；大量线段应重写以批处理。 |
| `drawEllipse()` | 浮点重载默认调用 `drawPolygon()`；整数重载默认转到浮点重载。 |
| `drawPath()` | 基类默认什么也不做。要支持 `QPainterPath` 必须重写。 |
| `drawPoints()` | 整数重载默认转成浮点重载；后端可重写以避免临时转换。 |
| `drawPolygon()` | 至少实现一个重载；承载填充规则和 polyline 语义。 |
| `drawPixmap()` | 纯虚，必须把源矩形映射到目标矩形。 |
| `drawImage()` | 应处理图像源区域、目标区域与转换 flags；必要时转为后端可用图像 / pixmap。 |
| `drawTextItem()` | 基类可把文字转为路径再绘制；原生文本后端应重写以获得字形质量与性能。 |
| `drawTiledPixmap()` | 从指定起点重复图像直到填满目标矩形；纹理后端可原生实现。 |

## 框架协作 API 的边界

下列成员是公开的，但主要由 `QPainter` 与 Qt 绘制系统协作使用：

- `setPaintDevice()` / `paintDevice()`
- `setSystemClip()` / `systemClip()`
- `setSystemRect()` / `systemRect()`
- `coordinateOffset()`
- `syncState()`、`testDirty()`、`setDirty()`、`clearDirty()`
- `isExtended()`、`createPixmap()`、`createPixmapFromImage()`

普通应用代码不要用它们替代 `QPainter` 公共 API。自定义引擎也应只有在明确理解 Qt 管线约定时才改写或调用；尤其不能随意重置系统裁剪，它通常承载窗口暴露区等平台限制。

## 常见错误

### 只实现纯虚函数，忽略多边形和路径

`drawPath()` 默认不绘制任何东西，且至少一个 `drawPolygon()` 重载必须实现。测试只画 pixmap 时看似正常，一旦应用画圆、路径、文本或矩形就可能无输出。

### 宣称支持实际不支持的 feature

错误的 `PaintEngineFeatures` 会使 Qt 选择不该走的快速路径，结果可能是没有抗锯齿、渐变错误或合成失真。能力标志必须保守且真实。

### 只更新部分 dirty state

例如忽略 `DirtyOpacity` 或 `DirtyClipEnabled`，会产生“前一个图元的透明度 / 裁剪泄漏到后一个图元”的难查问题。把所有 `DirtyFlag` 纳入 `updateState()` 的测试矩阵。

### 直接 delete `paintEngine()`

引擎归 `QPaintDevice` 所有。手动释放会造成设备再次开始绘制时使用悬空指针。

### 用 `type()` 作为功能探测

同为 `Raster` 或 `OpenGL` 并不保证同样的后端约束。需要能力探测时逐项 `hasFeature()`；需要业务兼容性时建立自己的后端能力层。

## API 速查表

### 生命周期与状态

| API | 说明 | 使用时重点 |
| --- | --- | --- |
| `QPaintEngine(PaintEngineFeatures caps = {})` | 构造引擎并声明原生能力。 | 只声明已正确实现的能力。 |
| `~QPaintEngine()` | 虚析构函数。 | 一般由拥有它的 `QPaintDevice` 销毁。 |
| `begin(QPaintDevice *pdev)` | 开始在 `pdev` 上绘制并初始化后端。纯虚。 | 成功返回 `true`；通常由 `QPainter` 调用。 |
| `end()` | 结束当前设备的绘制并完成后端收尾。纯虚。 | 成功返回 `true`；与 `begin()` 成对。 |
| `isActive() const` | 当前引擎是否正处于绘制活动期。 | 用于诊断生命周期，不替代后端资源状态检查。 |
| `setActive(bool state)` | 设置引擎活动标志。 | Qt 管线 / 引擎实现协作 API，应用不应手动切换。 |
| `updateState(const QPaintEngineState &state)` | 同步 painter 改变的状态。纯虚。 | 检查每个 dirty flag 并同步其对应值。 |
| `painter() const` | 返回关联的 painter 指针。 | 不拥有且不应跨绘制会话缓存。 |
| `paintDevice() const` | 返回当前正在绘制的设备；不活动时为 `nullptr`。 | 不拥有；只在活动期使用。 |
| `setPaintDevice(QPaintDevice *device)` | 设置当前绘制设备。 | 框架协作 API；不要从普通应用代码调用。 |
| `syncState()` | 请求同步当前 painter 状态。 | 高级框架辅助，不要当作应用级刷新函数。 |

### 能力、类型与系统约束

| API | 说明 | 使用时重点 |
| --- | --- | --- |
| `hasFeature(PaintEngineFeatures feature) const` | 查询是否支持指定能力 bit。 | 多个 bit 的参数是“任一命中”，想要全部支持必须逐项检查。 |
| `type() const` | 返回引擎类型。纯虚。 | 自定义引擎在 `User` 到 `MaxUser` 范围选值；不作为功能探测主手段。 |
| `setSystemClip(const QRegion &clip)` | 设置系统级裁剪。 | 保留窗口 / 平台暴露区域约束，通常仅 Qt 内部使用。 |
| `systemClip() const` | 返回系统级裁剪区域。 | 与应用设置的 painter clip 概念不同。 |
| `setSystemRect(const QRect &rect)` | 设置系统级矩形。 | 高级平台协作状态。 |
| `systemRect() const` | 返回系统级矩形。 | 不替代 `QPainter` 的 viewport / window。 |
| `coordinateOffset() const` | 返回后端坐标偏移。可重写。 | 用于后端坐标映射，不是应用层平移 API。 |
| `isExtended() const` | 是否属于扩展绘制引擎实现。 | Qt 内部能力判断。 |

### 图元绘制

| API | 说明 | 使用时重点 |
| --- | --- | --- |
| `drawRects(const QRect *rects, int count)` | 绘制整数矩形数组。 | 默认转到浮点或其他图元；批量场景可优化。 |
| `drawRects(const QRectF *rects, int count)` | 绘制浮点矩形数组。 | 基类可分发到 path / polygon。 |
| `drawLines(const QLine *lines, int count)` | 绘制整数线段数组。 | 默认转浮点；大量线建议批处理实现。 |
| `drawLines(const QLineF *lines, int count)` | 绘制浮点线段数组。 | 基类可能逐条转 path / polygon。 |
| `drawEllipse(const QRect &rect)` | 绘制内接整数矩形的椭圆。 | 默认转至浮点重载。 |
| `drawEllipse(const QRectF &rect)` | 绘制内接浮点矩形的椭圆。 | 默认调用 `drawPolygon()`。 |
| `drawPath(const QPainterPath &path)` | 绘制路径。 | 基类默认不做事；支持路径时必须重写。 |
| `drawPoints(const QPoint *points, int count)` | 绘制整数点数组。 | 默认转浮点重载。 |
| `drawPoints(const QPointF *points, int count)` | 绘制浮点点数组。 | 后端按当前 pen / transform 绘制。 |
| `drawPolygon(const QPoint *points, int count, PolygonDrawMode mode)` | 绘制整数多边形或折线。 | 两个重载至少实现一个。 |
| `drawPolygon(const QPointF *points, int count, PolygonDrawMode mode)` | 绘制浮点多边形或折线。 | 正确处理填充规则与 `PolylineMode`。 |
| `drawPixmap(const QRectF &target, const QPixmap &pixmap, const QRectF &source)` | 把像素图源区域绘制到目标矩形。纯虚。 | 处理裁剪、变换、DPR 和源/目标比例。 |
| `drawImage(const QRectF &target, const QImage &image, const QRectF &source, Qt::ImageConversionFlags flags)` | 把图像源区域绘制到目标矩形。 | 遵从颜色转换 flags；必要时转换为后端资源。 |
| `drawTextItem(const QPointF &position, const QTextItem &text)` | 绘制排版后的文本项。 | 默认转路径；原生文字后端应重写。 |
| `drawTiledPixmap(const QRectF &rect, const QPixmap &pixmap, const QPointF &origin)` | 重复像素图填满矩形。 | `origin` 决定平铺起点，不是只画一次。 |

### 高级资源辅助

| API | 说明 | 使用时重点 |
| --- | --- | --- |
| `createPixmap(QSize size)` | 创建供该引擎使用的像素图资源。可重写。 | 高级后端资源工厂，普通绘制使用 `QPixmap` API。 |
| `createPixmapFromImage(QImage image, Qt::ImageConversionFlags flags)` | 从图像创建引擎适配的像素图资源。可重写。 | 正确处理转换 flags 和资源归属。 |
| `testDirty(DirtyFlags flags)` | 检查内部 state 是否含指定脏标志。 | 引擎内部辅助；`updateState()` 通常直接读参数 `state.state()`。 |
| `setDirty(DirtyFlags flags)` | 设置内部脏标志。 | Qt 内部状态管理。 |
| `clearDirty(DirtyFlags flags)` | 清除内部脏标志。 | Qt 内部状态管理；不要与 painter 状态同步脱节。 |

## 与相邻类型的分工

| 类型 | 职责 |
| --- | --- |
| `QPainter` | 应用层绘制命令与绘制状态设置。 |
| `QPaintDevice` | 提供实际目标的尺寸、DPI 与 engine 指针。 |
| `QPaintEngine` | 将 painter 命令翻译为特定后端操作。 |
| `QPaintEngineState` | 在状态同步时提供 dirty flags 与当前值。 |
| `QImage` / `QPixmap` / `QPrinter` | 常用的具体绘制目标。 |

一句话记忆：`QPaintEngine` 是 Qt 绘制系统的后端适配层；普通应用让 `QPainter` 管它，自定义后端则必须把生命周期、状态同步、能力声明和图元实现一起做对。
