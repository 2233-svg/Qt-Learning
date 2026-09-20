# QSGGeometry：为 scene graph 提供顶点、索引和图元拓扑

> Qt 6.11.1 | `#include <QSGGeometry>` | CMake: `Qt6::Quick`

`QSGGeometry` 是 `QSGGeometryNode` 绘制的 CPU 侧几何缓冲：它保存顶点数据、可选索引数据、顶点布局和图元拓扑。它适合在 `QQuickItem::updatePaintNode()` 中实现曲线、网格、波形、带纹理四边形等自定义 2D 图形。

它不是通用 GPU buffer，也不自动把内存修改告诉 renderer。所有 QSG 操作发生在 scene graph 渲染线程；更改几何后，至少需要对所属 node 调用 `markDirty(QSGNode::DirtyGeometry)`。是否还需要调用 `markVertexDataDirty()`/`markIndexDataDirty()`，取决于数据模式。

## 先固定顶点布局，再写入数据

```cpp
auto *geometry = new QSGGeometry(
    QSGGeometry::defaultAttributes_Point2D(), 4);
geometry->setDrawingMode(QSGGeometry::DrawTriangleStrip);
QSGGeometry::updateRectGeometry(geometry, QRectF(0, 0, width(), height()));

node->setGeometry(geometry);
node->setFlag(QSGNode::OwnsGeometry);
```

构造函数保存的是 `AttributeSet` 的**引用**，而不是副本；该 `AttributeSet` 以及它引用的 `Attribute` 数组必须在 `QSGGeometry` 整个生命期内保持有效。内置 `defaultAttributes_*()` 返回的静态布局可安全使用；自定义布局应定义为静态或与 geometry 同寿命的对象，不能把局部数组传入后立即离开作用域。

默认绘制模式是 `DrawTriangleStrip`。常用拓扑有 points、lines、line strip、triangles、triangle strip；尽管枚举仍有 `DrawLineLoop` 和 `DrawTriangleFan`，Qt 6 的跨后端 scene graph 不在运行时支持它们。

## 扩容、计数和脏标记

`allocate(vertexCount, indexCount)` 会调整缓冲大小并使所有 vertex/index 内容失效，因此必须完整重写数据，再标记 node 的 `DirtyGeometry`。Qt 6.10 的 `setVertexCount()`、`setIndexCount()` 只改变本次绘制使用的数量，不重分配；传入值不会校验，必须位于已分配容量范围内，仍要标记 node。

`AlwaysUploadPattern` 是默认值，修改数据后不必额外调用 geometry 的 `mark*DataDirty()`。选择 `StreamPattern`、`DynamicPattern` 或 `StaticPattern` 是给 renderer 的性能提示，是否采纳由后端决定；此时每次改顶点/索引数据都要分别 `markVertexDataDirty()`/`markIndexDataDirty()`，并且仍要 `node->markDirty(DirtyGeometry)`。

## 常用布局和辅助函数

`defaultAttributes_Point2D()` 对应 `Point2D { float x, y; }`，`defaultAttributes_TexturedPoint2D()` 对应 position + normalized UV，`defaultAttributes_ColoredPoint2D()` 对应 position + 四个 `uchar` 颜色分量。`vertexDataAsPoint2D()` 等快捷访问器只适用于完全匹配的内置布局，布局不符时断言失败；自定义 vertex struct 应通过 `vertexData()` 转换。

`updateRectGeometry()`、`updateTexturedRectGeometry()`、`updateColoredRectGeometry()` 都假设特定的四顶点 triangle strip 布局。尤其纹理矩形必须是归一化 UV；对 atlas texture 通常传入 `normalizedTextureSubRect()`。

## API 速查表

| API | 语义 | 关键边界 |
|---|---|---|
| `QSGGeometry(attributes, vertexCount, indexCount, indexType)` | 以固定顶点布局创建 geometry | `attributes` 及其数组必须比 geometry 活得久；默认拓扑是 `DrawTriangleStrip` |
| `AttributeSet` / `Attribute` | 描述每个顶点的 stride 和 shader attribute | 只在构造时确定，后续不能更换布局 |
| `defaultAttributes_Point2D()` | 返回位置二维顶点的标准布局 | 配合 `Point2D` 与纯色几何 |
| `defaultAttributes_TexturedPoint2D()` | 返回位置加 UV 的标准布局 | 配合 `TexturedPoint2D` 与纹理几何 |
| `defaultAttributes_ColoredPoint2D()` | 返回位置加 RGBA 字节颜色的标准布局 | 配合 `ColoredPoint2D` |
| `setDrawingMode()` / `drawingMode()` | 设置/读取图元拓扑 | Qt 6 不支持运行时使用 `DrawLineLoop`、`DrawTriangleFan` |
| `allocate(vertices, indices)` | 重分配顶点和索引缓冲 | 旧数据全部失效，必须完整重写并标记 node `DirtyGeometry` |
| `setVertexCount()` / `setIndexCount()` | 改变实际绘制数量 | Qt 6.10 起；不校验上限、不重分配，仍需标记 node |
| `vertexData()` / `indexData()` | 取得原始可写顶点/索引内存 | 仅按既定布局转换；索引类型创建后不可变 |
| `vertexDataAsPoint2D()` 等 | 以内置顶点结构访问数据 | 仅布局完全匹配时可用 |
| `indexDataAsUShort()` / `indexDataAsUInt()` | 以 16/32 位索引访问数据 | 索引类型不匹配会触发断言 |
| `vertexCount()` / `indexCount()` / `indexType()` | 查询本次绘制的数量与索引类型 | `vertexCount` 是可绘制/可被索引访问的顶点数量 |
| `setVertexDataPattern()` / `setIndexDataPattern()` | 提示数据更新频率 | 非默认模式下改数据后还需相应 `mark*DataDirty()` |
| `AlwaysUploadPattern` | 每次自动上传的默认模式 | 改数据时不需 geometry 级 dirty，但 node 仍要 `DirtyGeometry` |
| `StreamPattern` / `DynamicPattern` / `StaticPattern` | 频繁/重复/一次修改的性能提示 | 后端可忽略；必须显式标记对应数据 dirty |
| `markVertexDataDirty()` / `markIndexDataDirty()` | 标记 CPU 数据需重新上传 | 只对非默认 pattern 有意义；不替代 node 的 `DirtyGeometry` |
| `updateRectGeometry()` | 写入四个 `Point2D` 的矩形 triangle strip | geometry 必须匹配该布局 |
| `updateTexturedRectGeometry()` | 写入四个 `TexturedPoint2D` 的矩形和 UV | UV 必须归一化，geometry 必须是四顶点 strip |
| `updateColoredRectGeometry()` | 写入四个 `ColoredPoint2D` 的矩形 | geometry 必须匹配该布局 |
| `setLineWidth()` / `lineWidth()` | 设置线或点的宽度 | 仅 line/point 拓扑有效；除 `1.0` 外的支持依后端而定 |
| `sizeOfVertex()` / `sizeOfIndex()` / `attributeCount()` / `attributes()` | 查询布局和元素大小 | 用于自定义 vertex struct 的 stride 校验与调试 |
