# QSGGeometry::Point2D：纯二维位置顶点

> Qt 6.11.1 | `#include <QSGGeometry>` | CMake: `Qt6::Quick`

`QSGGeometry::Point2D` 是最简单的内置顶点结构，只包含 `float x` 和 `float y`。它适合纯色矩形、多边形、线段等只需位置、不需 UV 或顶点颜色的数据，并与 `QSGGeometry::defaultAttributes_Point2D()` 配套。

它是 `QSGGeometry` 缓冲中的内存布局，不是 `QPointF` 的替代品。`QPointF` 适合业务和几何计算；当需要把数据写入 scene graph 顶点缓冲时，才通过 `vertexDataAsPoint2D()` 取得这一结构数组。

```cpp
auto *vertices = geometry->vertexDataAsPoint2D();
vertices[0].set(0.0f, 0.0f);
vertices[1].set(width(), 0.0f);
vertices[2].set(0.0f, height());
node->markDirty(QSGNode::DirtyGeometry);
```

顶点数组长度取决于创建 geometry 时的 `vertexCount`。更新位置不会自动触发上传或重绘：对所属 node 标记 `DirtyGeometry`；若 geometry 使用非默认数据模式，还要标记 vertex data dirty。

## API 速查表

| API | 语义 | 关键边界 |
|---|---|---|
| `x`, `y` | 顶点二维位置 | `float`，数值以当前 item/geometry 坐标系解释 |
| `set(x, y)` | 写入顶点位置 | 不进行边界或 NaN 校验 |
| `defaultAttributes_Point2D()` | 对应此结构的标准布局 | 只有匹配时才能使用快捷访问器 |
| `vertexDataAsPoint2D()` | 把 geometry 顶点内存作为 `Point2D` 数组 | 布局不匹配会断言失败 |
| `QSGNode::DirtyGeometry` | 通知 renderer 顶点内容改变 | 改写任意顶点后都需要对所属 node 标记 |
