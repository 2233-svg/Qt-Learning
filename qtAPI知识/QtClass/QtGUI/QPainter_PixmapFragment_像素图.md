# QPainter::PixmapFragment：为批量精灵图绘制描述单个片段

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QPainter>`  
> 所属类型：`QPainter`  
> 相关 API：`QPainter::drawPixmapFragments()`、`QPixmap`

`QPainter::PixmapFragment` 是一个轻量数据结构，用于和 `QPainter::drawPixmapFragments()` 配合，描述同一张 `QPixmap` 中的一个源矩形应如何绘制到目标位置。每个 fragment 可独立指定源区域、位置、缩放、旋转和不透明度，而一批 fragment 共用同一张 pixmap。

它主要用于精灵图、图标图集、粒子系统、地图标记和列表装饰等“同一纹理要绘制很多次”的场景。与循环调用大量 `drawPixmap()` 相比，批量接口让后端有机会合并状态切换，因此通常更高效。

## 它解决的问题

假设一张图集包含几十个 sprite，需要在一帧中绘制几百个实例。逐个调用 `drawPixmap()` 意味着每次都重复传递源矩形、目标位置、缩放、旋转和透明度。`PixmapFragment` 把每个实例的变换参数整理为连续数组：

```cpp
QVector<QPainter::PixmapFragment> fragments;
fragments.reserve(items.size());

for (const Item &item : items) {
    fragments.append(QPainter::PixmapFragment::create(
        item.center,
        item.sourceRect,
        item.scale,
        item.scale,
        item.rotation,
        item.opacity));
}

painter.drawPixmapFragments(fragments.constData(),
                            fragments.size(),
                            spriteAtlas);
```

后端知道这批内容都来自同一张 `spriteAtlas`，可以减少纹理、图像或绘制状态的重复配置。

## 实际使用场景

### 1. 从精灵图批量绘制单位图标

```cpp
const QRectF unitSprite(0, 0, 32, 32);

QVector<QPainter::PixmapFragment> fragments;
fragments.reserve(units.size());

for (const Unit &unit : units) {
    fragments.append(QPainter::PixmapFragment::create(
        unit.position,
        unitSprite,
        unit.zoom,
        unit.zoom,
        unit.headingDegrees,
        unit.visible ? 1.0 : 0.35));
}

painter.drawPixmapFragments(fragments.constData(),
                            fragments.size(),
                            atlas);
```

`position` 是每个目标矩形的中心，而不是左上角。源矩形 `unitSprite` 则在图集自身坐标中指定。

### 2. 同一图标以不同角度和透明度绘制

```cpp
const auto fragment = QPainter::PixmapFragment::create(
    QPointF(200, 120),
    QRectF(64, 0, 24, 24),
    1.5,
    1.5,
    45.0,
    0.6);

painter.drawPixmapFragments(&fragment, 1, atlas);
```

目标尺寸先由源矩形宽高乘以 `scaleX` / `scaleY` 得到，再围绕中心点旋转 `rotation` 度。这里的目标未旋转尺寸是 36 x 36。

### 3. 确认所有片段确实不透明时使用提示

```cpp
painter.drawPixmapFragments(fragments.constData(),
                            fragments.size(),
                            opaqueAtlas,
                            QPainter::OpaqueHint);
```

只有在 pixmap 源内容和每个 fragment 的 `opacity` 都保证不透明时才给出 `OpaqueHint`。该提示允许后端采用可能更快的绘制路径；若实际含有 alpha 或 `opacity < 1`，不要为了性能错误声明它。

## 核心几何语义

### 源矩形

`sourceLeft`、`sourceTop`、`width`、`height` 共同定义传给 `drawPixmapFragments()` 的 pixmap 内的源矩形：

```text
sourceRect = QRectF(sourceLeft, sourceTop, width, height)
```

`width` 和 `height` 同时也构成未缩放目标矩形的基础尺寸。一个 fragment 没有单独的 target width / target height 字段。

### 目标矩形

`x`、`y` 是目标矩形的**中心点**，不是左上角：

```text
targetSize = (width * scaleX, height * scaleY)
targetCenter = (x, y)
```

随后目标矩形围绕 `(x, y)` 旋转 `rotation` 度。将左上角误当成中心会使所有片段偏移半个缩放后的宽高，旋转后偏移会更加明显。

### 变换顺序

对单个 fragment，概念顺序为：

1. 从 pixmap 取出源矩形；
2. 按 `scaleX`、`scaleY` 调整目标尺寸；
3. 将目标矩形放到中心点 `(x, y)`；
4. 围绕该中心旋转 `rotation` 度；
5. 按 `opacity` 与当前 painter 状态进行合成。

当前 `QPainter` 自身的 world transform、clip、composition mode 和全局 opacity 仍会参与最终结果。fragment 的 `opacity` 不是对 painter 全局透明度的替代，而是每个实例自己的额外参数。

### 透明度和缩放边界

文档定义 `opacity` 的语义为 `0.0` 完全透明、`1.0` 完全不透明。业务代码应限制值在该区间内，以保持不同绘制后端行为一致。

负缩放可形成翻转效果的几何含义，但它会改变方向、采样边缘和旋转组合的可读性。需要镜像 sprite 时，优先通过明确的变换规则测试目标后端；不要假定每种平台引擎对负尺度的像素对齐都相同。

### 生命周期与线程

`PixmapFragment` 本身是可按值存放的 plain data，不拥有 pixmap，也不依赖事件循环。传给 `drawPixmapFragments()` 的数组必须在该函数调用期间有效即可。

`QPixmap` 通常与 GUI / 平台图形资源相关，应在 GUI 线程使用。若后台线程要准备实例数据，可以在那里构造 `PixmapFragment` 数组，但应把实际 `QPixmap` 绘制交回合适的 GUI 线程。后台像素生成优先使用 `QImage`。

## `create()` 与手动填字段

推荐使用工厂函数：

```cpp
const auto fragment = QPainter::PixmapFragment::create(
    QPointF(100, 80),
    QRectF(32, 64, 16, 16),
    2.0, 1.0,
    30.0,
    0.75);
```

它按参数初始化所有字段，避免漏写 `scaleX`、`scaleY` 或透明度。需要复用数组槽位时也可以手动赋值，但必须为每个提交绘制的元素正确设置全部字段：

```cpp
QPainter::PixmapFragment fragment;
fragment.x = 100;
fragment.y = 80;
fragment.sourceLeft = 32;
fragment.sourceTop = 64;
fragment.width = 16;
fragment.height = 16;
fragment.scaleX = 2;
fragment.scaleY = 1;
fragment.rotation = 30;
fragment.opacity = 0.75;
```

## 常见错误

### 把 `x`、`y` 当作左上角

目标位置是中心点。若已有左上角 `topLeft` 和目标尺寸 `targetSize`，应先转换：

```cpp
const QPointF center = topLeft + QPointF(targetSize.width() / 2,
                                         targetSize.height() / 2);
```

### 混淆 source width 与缩放后的目标宽度

`width` / `height` 是源矩形尺寸，也是未缩放目标尺寸基准。目标尺寸由它们乘缩放得到；不要先把缩放后的目标宽高写入字段、又设置 `scaleX` / `scaleY`，否则会重复缩放。

### 为每个 fragment 换一张 pixmap

批量 API 的优势来自共享一个 `QPixmap`。不同图集应按 pixmap 分组，多次批量调用；不要把不同源图混进同一数组后期待函数自动识别。

### 错用 `OpaqueHint`

`OpaqueHint` 是真实性声明，不是“尽量快一点”的通用选项。只要图集含透明像素、fragment 透明度小于 1，或当前合成方式依赖 alpha，就不要设置。

### 小批量或静态单图也强行批处理

对于一两个普通图标，直接 `drawPixmap()` 更直观。`PixmapFragment` 的价值在于一次调用中绘制大量同源实例，并减少重复状态处理。

## API 速查表

### 工厂函数

| API | 说明 | 使用时重点 |
| --- | --- | --- |
| `static PixmapFragment create(const QPointF &pos, const QRectF &sourceRect, qreal scaleX = 1, qreal scaleY = 1, qreal rotation = 0, qreal opacity = 1)` | 创建并初始化一个 fragment。 | `pos` 是目标中心；源矩形来自共享 pixmap；缩放后再绕中心旋转。 |

### 公共字段

| 字段 | 含义 | 使用时重点 |
| --- | --- | --- |
| `x` | 目标矩形中心的 X 坐标。 | 不是左边界。 |
| `y` | 目标矩形中心的 Y 坐标。 | 不是上边界。 |
| `sourceLeft` | pixmap 源矩形左边界。 | 与 `sourceTop`、`width`、`height` 一起定义图集裁剪区域。 |
| `sourceTop` | pixmap 源矩形上边界。 | 使用图集本地坐标。 |
| `width` | 源矩形宽度，也是未缩放目标宽度。 | 最终目标宽度为 `width * scaleX`。 |
| `height` | 源矩形高度，也是未缩放目标高度。 | 最终目标高度为 `height * scaleY`。 |
| `scaleX` | 目标矩形的水平缩放倍率。 | `1` 为原宽；高频动画避免无意义地反复改动。 |
| `scaleY` | 目标矩形的垂直缩放倍率。 | 与 `scaleX` 不同会产生非等比缩放。 |
| `rotation` | 目标矩形绕中心的旋转角度，单位为度。 | 在缩放后执行；正负方向遵循当前 painter 坐标系。 |
| `opacity` | 此 fragment 的不透明度。 | 语义范围为 0 到 1；与 painter 全局 opacity 共同影响最终结果。 |

### 配套 QPainter API

| API | 说明 | 使用时重点 |
| --- | --- | --- |
| `drawPixmapFragments(const PixmapFragment *fragments, int count, const QPixmap &pixmap, PixmapFragmentHints hints = {})` | 以同一 pixmap 批量绘制 fragment 数组。 | 数组在调用期间必须有效；不同 pixmap 分批调用。 |
| `QPainter::OpaqueHint` | 表示待绘制 fragment 均不透明。 | 仅在真实满足时使用，后端可能因此优化。 |
| `QPainter::PixmapFragmentHints` | `PixmapFragmentHint` 的 flags 类型。 | 可传入多个提示 bit；当前公开提示为 `OpaqueHint`。 |

## 与相邻 API 的选择

| 需求 | 推荐 API |
| --- | --- |
| 画一张完整图或少量图标 | `QPainter::drawPixmap()` |
| 同一图集批量画许多实例，每个实例可缩放、旋转、淡入淡出 | `drawPixmapFragments()` + `PixmapFragment` |
| 后台生成像素数据 | `QImage`，而不是 GUI 资源型 `QPixmap` |
| 多图集批量绘制 | 先按 `QPixmap` 分组，每组调用一次 `drawPixmapFragments()` |

一句话记忆：`PixmapFragment` 描述“从同一张图集裁哪一块、放到哪个中心、怎么缩放旋转和透明”，为 `drawPixmapFragments()` 的批量绘制而生。
