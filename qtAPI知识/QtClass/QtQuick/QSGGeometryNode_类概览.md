# QSGGeometryNode：把网格和材质组合为一条 scene graph 绘制项

> Qt 6.11.1 | `#include <QSGGeometryNode>` | CMake: `Qt6::Quick`

`QSGGeometryNode` 是自定义 scene graph 绘制最常用的节点：`QSGGeometry` 决定顶点、索引和图元拓扑，`QSGMaterial` 决定这些图元怎样填充。纯色矩形、折线、纹理四边形和自定义 shader 结果最终都以这个组合进入 renderer。

典型使用点是 `QQuickItem::updatePaintNode()`：首次创建 node、geometry、material 并设定所有权；后续复用 node，只更新发生变化的缓冲或材质参数并标记对应 dirty state。所有对象都只能在 scene graph 渲染线程操作。

## 入树前的最低条件

```cpp
auto *node = new QSGGeometryNode;
auto *geometry = new QSGGeometry(QSGGeometry::defaultAttributes_Point2D(), 4);
auto *material = new QSGFlatColorMaterial;

node->setGeometry(geometry);
node->setMaterial(material);
node->setFlag(QSGNode::OwnsGeometry);
node->setFlag(QSGNode::OwnsMaterial);
```

加入 scene graph 前，node 必须同时具备 geometry 和普通 material。`opaqueMaterial` 只是一个可选的快速路径，不能代替 `material`。更新已有 geometry 的顶点数据后标记 `DirtyGeometry`；原地改 material 参数后标记 `DirtyMaterial`。

## 不透明材质的含义

当 node 的继承 opacity 为 `1` 且设置了 `opaqueMaterial` 时，renderer 会优先选它。它用于让同一几何在“整个 item tree 完全不透明”时走更有利的材质路径，而 normal material 继续处理有 opacity 的情况。

这里的 opaque 指 scene graph 累积 opacity，不代表材质绝不能开启 `QSGMaterial::Blending` 或输出透明像素。提供与 normal material 逻辑不一致的 opaque material 会造成视觉差异，因此只有确实理解两条路径时才设置。

## API 速查表

| API | 语义 | 关键边界 |
|---|---|---|
| `QSGGeometryNode()` | 创建 geometry 与 material 的组合节点 | 入树前必须设置 geometry 和普通 `material` |
| `setGeometry()` / `geometry()` | 关联或取得网格数据 | 默认不接管所有权；原地改顶点后标记 `DirtyGeometry` |
| `setMaterial()` / `material()` | 设置或取得常规材质 | 不能为空才能绘制；原地改参数后标记 `DirtyMaterial` |
| `setOpaqueMaterial()` / `opaqueMaterial()` | 设置或取得 opacity 为 1 时优先使用的材质 | 可选，不能代替常规 material |
| `activeMaterial()` | 返回 renderer 在当前 opacity 条件下会使用的材质 | 由继承 opacity 和 opaque material 是否存在决定 |
| `setRenderOrder()` / `renderOrder()` | 指定节点相对绘制顺序 | 仅在确有排序需求时改动，可能影响 batching |
| `setInheritedOpacity()` / `inheritedOpacity()` | 供 renderer 传递累计透明度 | scene graph 内部状态，应用通常不手工设置 |
| `QSGNode::OwnsGeometry` / `OwnsMaterial` | 让 node 自动删除关联对象 | 仅在对象独占时使用，避免双重释放 |
| `QSGNode::DirtyGeometry` / `DirtyMaterial` | 通知 renderer 几何或材质已原地变化 | 修改已有对象后必须调用 `markDirty()` |
