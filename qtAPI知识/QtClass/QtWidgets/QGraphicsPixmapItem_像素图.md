<!-- 依据 Qt 6.11.1 头文件 qgraphicsitem.h 整理。 -->

# QGraphicsPixmapItem 深入笔记

> 头文件：`#include <QGraphicsPixmapItem>`  
> 模块：`Qt6::Widgets`  
> 继承：`QGraphicsItem -> QGraphicsPixmapItem`

## 1. 它解决什么问题

`QGraphicsPixmapItem` 将一个 `QPixmap` 放入 Graphics View 场景，并提供变换、透明区域命中、偏移和绘制质量策略。它是图标、贴图、精灵、缩略图和图片标注的基础图元。

它适合：

- 场景中的图片、图标、精灵和缩略图。
- 图像编辑器中的贴纸、标记、可拖动图片。
- 带透明背景的 PNG 图标，需要按不透明像素点击。

它不适合：

- 富文本或可编辑文字：用 `QGraphicsTextItem`。
- 高频逐像素修改的动态图像：先在 `QImage` 中处理，再按节奏更新 pixmap；不要把每个像素变化都变成一次 scene 图元重建。
- 海量静态小图：需要评估 scene item 数量、纹理/像素缓存和视图缩放成本。

## 2. 最小使用路径

```cpp
#include <QGraphicsPixmapItem>
#include <QPixmap>

QPixmap icon(":/icons/pin.png");
auto *pin = new QGraphicsPixmapItem(icon);
pin->setOffset(-icon.width() / 2.0, -icon.height());
pin->setPos(320, 180);
scene->addItem(pin);
```

这里把 pixmap 的底部中心设为图元原点，因此 `pin->setPos()` 可以直接使用地图坐标或节点锚点坐标。这个模式特别适合地图图钉、角色脚底、流程图端口图标。

`QPixmap` 面向 GUI 绘制资源，创建、读取和设置 pixmap item 应放在 GUI 线程；后台解码或处理图片时，优先用 `QImage`，完成后把结果交回 GUI 线程转换或设置。

## 3. `offset` 是像素图相对图元原点的位置

`QGraphicsPixmapItem` 没有 `rect()`；pixmap 的本地绘制位置由 `offset` 决定：

```text
item 的本地原点 (0, 0)
       ↓ offset
pixmap 左上角
```

默认 offset 是 `(0, 0)`，即 pixmap 左上角与图元原点重合。

```cpp
item->setOffset(0, 0);                    // 左上角锚定
item->setOffset(-w / 2.0, -h / 2.0);      // 中心锚定
item->setOffset(-w / 2.0, -h);            // 底部中心锚定
```

不要为了“把图片的中心对准某坐标”去修改 `setPos()` 后再手工补一半宽高；把锚点语义固定在 `offset`，后续换图、缩放、旋转和附加子图元时更不容易出错。

## 4. `ShapeMode`：透明像素能不能被点中

`shapeMode` 决定 `shape()`、`contains()`、碰撞检测和部分 scene 查询怎样从 pixmap 推导有效区域。默认是 `MaskShape`。

| 模式 | 命中区域 | 性能与适用场景 |
| --- | --- | --- |
| `MaskShape` | 依据 pixmap 的 alpha/mask 得到较精确的非透明轮廓。 | 透明 PNG 图标、角色精灵等需要避开透明区域的交互；成本最高。 |
| `BoundingRectShape` | 整张 pixmap 的矩形范围。 | 缩略图、背景、普通图片；最快且通常足够。 |
| `HeuristicMaskShape` | 根据启发式掩码近似不透明轮廓。 | 希望减少明显透明误点，又不能承受完整 mask 成本时。 |

例如一个圆形 PNG 图标：

```cpp
iconItem->setShapeMode(QGraphicsPixmapItem::MaskShape);
```

这样四个透明角通常不会命中。若图标仅用于展示、不会精确点击：

```cpp
iconItem->setShapeMode(QGraphicsPixmapItem::BoundingRectShape);
```

用 shape mode 优化前先明确需求。`BoundingRectShape` 并不表示图片没有透明像素，它只表示透明像素仍算作交互区域。

## 5. 缩放质量：`transformationMode`

当 item 或 view 对 pixmap 做非原始比例变换时，`transformationMode` 控制采样策略：

| 模式 | 结果 | 适用场景 |
| --- | --- | --- |
| `Qt::FastTransformation` | 速度优先，放大/旋转时可能出现锯齿。 | 快速缩放、拖动预览、像素风素材。 |
| `Qt::SmoothTransformation` | 画质优先，通常更平滑但更耗时。 | 静态图片、照片、停留状态的高质量显示。 |

```cpp
item->setTransformationMode(Qt::SmoothTransformation);
```

它只决定**绘制时**如何变换，不会重新生成或永久改变 `pixmap()` 内容。若持续对大图做大倍率缩放，预先生成合适分辨率的 pixmap、限制缩放范围或使用缓存策略，往往比单纯切换 `SmoothTransformation` 更有效。

## 6. `setPixmap()` 会改变几何

```cpp
item->setPixmap(QPixmap(":/images/cover.png"));
```

pixmap 尺寸和 offset 共同决定 `boundingRect()`。换成不同尺寸图片后，场景重绘范围、命中范围和依赖该图元的编辑控点位置都可能改变。

`pixmap()` 返回值；对得到的 `QPixmap` 做变换不会自动影响图元，必须再调用 `setPixmap()` 回写：

```cpp
QPixmap changed = item->pixmap().scaled(
    96, 96, Qt::KeepAspectRatio,
    Qt::SmoothTransformation);
item->setPixmap(changed);
```

注意区分两件事：

- 想改变图片**资源尺寸**：生成新 pixmap 后 `setPixmap()`。
- 想改变图元在 scene 中的**几何变换**：用 `setScale()`、`setRotation()` 等 QGraphicsItem API。

二者的清晰度、内存占用和命中范围表现不同。

## 7. 边界、透明度和绘制流程

```text
pixmap + offset        原始本地像素区域
boundingRect()         scene 索引和重绘范围
shape()                ShapeMode 决定的命中路径
contains(localPoint)   判断本地点命中
opaqueArea()           已知不透明区域，用于遮挡优化
```

透明背景图片的 `opaqueArea()` 不能代替点击判断，也不应通过 `isObscuredBy()` 判断图片是否与另一图重叠。这两项服务 scene 的绘制优化。

`paint()` 已由标准类实现。业务代码改变图片、offset、shape mode 或 transformation mode 后，让 Graphics View 调度重绘；不要自行调用 `paint()`。

## 8. 类型和扩展接口

`type()` 返回 `QGraphicsPixmapItem::Type`，值为 `7`，可用于异构 `QGraphicsItem *` 容器中的类型分派。

`supportsExtension()`、`setExtension()`、`extension()` 是受保护框架扩展接口。标准 pixmap item 为框架兼容性重写，普通应用不直接调用。

## API 速查表
| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 类型 | `enum ShapeMode` | 选择从 pixmap 得到命中区域的策略。 | 默认 `MaskShape`；精度与成本必须按交互需求选。 |
| 枚举值 | `MaskShape` | 使用像素 alpha/mask 推导较精确轮廓。 | 透明图标精确点击适用，计算和内存成本较高。 |
| 枚举值 | `BoundingRectShape` | 使用整个 pixmap 矩形作为 shape。 | 最快，但透明像素也会命中。 |
| 枚举值 | `HeuristicMaskShape` | 使用启发式掩码近似轮廓。 | 精度和成本介于前两者之间。 |
| 类型常量 | `QGraphicsPixmapItem::Type = 7` | 标识 pixmap 图元的运行时类型。 | 用 `type()` 确认后再 `static_cast`。 |
| 构造 | `explicit QGraphicsPixmapItem(QGraphicsItem *parent = nullptr)` | 创建空 pixmap 图元。 | 后续用 `setPixmap()` 设置图像。 |
| 构造 | `explicit QGraphicsPixmapItem(const QPixmap &pixmap, QGraphicsItem *parent = nullptr)` | 用 pixmap 创建图元。 | pixmap 属于 GUI 资源，应在 GUI 线程中设置。 |
| 析构 | `~QGraphicsPixmapItem()` | 销毁 pixmap 图元。 | 由 scene 或图元父子树处理所有权。 |
| 图像读取 | `QPixmap pixmap() const` | 返回当前 pixmap。 | 返回值修改后要 `setPixmap()` 回写。 |
| 图像设置 | `void setPixmap(const QPixmap &pixmap)` | 替换显示的 pixmap。 | 尺寸变化会影响边界、命中和相关编辑控点。 |
| 偏移读取 | `QPointF offset() const` | 返回 pixmap 左上角相对 item 原点的偏移。 | 用于检查当前锚点语义。 |
| 偏移设置 | `void setOffset(const QPointF &offset)` | 设置二维偏移。 | 中心/底部锚定应通过 offset 表达。 |
| 偏移设置 | `void setOffset(qreal x, qreal y)` | 用数值设置二维偏移。 | 是 `QPointF` setter 的便捷重载。 |
| 缩放质量 | `Qt::TransformationMode transformationMode() const` | 返回 pixmap 变换采样模式。 | 仅影响绘制质量，不改变 pixmap 数据。 |
| 缩放质量 | `void setTransformationMode(Qt::TransformationMode mode)` | 设置快速或平滑采样。 | 动态大图缩放先评估性能。 |
| 命中模式 | `ShapeMode shapeMode() const` | 返回当前 shape 推导模式。 | 用于诊断透明像素为何会或不会命中。 |
| 命中模式 | `void setShapeMode(ShapeMode mode)` | 设置 shape 推导模式。 | `BoundingRectShape` 适合展示优先场景。 |
| 绘制边界 | `QRectF boundingRect() const` | 返回 pixmap+offset 的 scene 索引/重绘范围。 | 图片大小或 offset 改变后结果会变化。 |
| 命中 | `QPainterPath shape() const` | 返回由 ShapeMode 决定的命中路径。 | 对透明 PNG 的精确度与性能取决于 mode。 |
| 命中 | `bool contains(const QPointF &point) const` | 判断本地点是否命中图片区域。 | scene 点须先 `mapFromScene()`。 |
| 绘制 | `void paint(QPainter *painter, const QStyleOptionGraphicsItem *option, QWidget *widget)` | 绘制 pixmap。 | 由 Graphics View 调用，业务代码不直接调用。 |
| 遮挡优化 | `bool isObscuredBy(const QGraphicsItem *item) const` | 判断其它 item 是否遮住本图。 | 不等同于图片相交或点击检测。 |
| 遮挡优化 | `QPainterPath opaqueArea() const` | 返回已知完全不透明区域。 | 用于 scene 绘制优化。 |
| 类型查询 | `int type() const` | 返回 `QGraphicsPixmapItem::Type`。 | 用于异构 item 集合的类型分派。 |
| 受保护扩展 | `bool supportsExtension(Extension extension) const` | 查询是否支持指定图元扩展。 | Qt 框架协议，普通应用不调用。 |
| 受保护扩展 | `void setExtension(Extension extension, const QVariant &variant)` | 写入扩展数据。 | 仅框架级自定义图元实现时使用。 |
| 受保护扩展 | `QVariant extension(const QVariant &variant) const` | 读取扩展数据。 | 参数和返回语义由具体扩展决定。 |

## 10. 排查清单

1. 圆形 PNG 的透明角也可点击：将 `shapeMode` 设为 `MaskShape` 或根据需求使用启发式模式。
2. 精确点击导致大量图片场景变慢：对非交互图片改用 `BoundingRectShape`。
3. 图片中心无法对准节点：用 `setOffset(-w/2, -h/2)`，而不是反复修正 `setPos()`。
4. 缩放大图模糊：尝试 `SmoothTransformation`，并评估是否该预生成合适分辨率。
5. 改了 `pixmap()` 的副本却没显示：调用 `setPixmap()` 回写。

### 一句话总结

`QGraphicsPixmapItem` 把 GUI pixmap 放入 scene；`offset` 决定锚点，`ShapeMode` 决定透明像素交互与成本，`transformationMode` 决定缩放质量。选对这三项，图片图元才既好点、又不拖慢场景。
