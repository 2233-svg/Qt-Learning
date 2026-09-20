# QSGBasicGeometryNode：几何节点与裁剪节点的共享基类

> Qt 6.11.1 | `#include <QSGBasicGeometryNode>` | CMake: `Qt6::Quick`

`QSGBasicGeometryNode` 只封装“一个 scene graph node 关联一份 `QSGGeometry`”的共同部分，供 `QSGGeometryNode` 和 `QSGClipNode` 使用。它的构造函数受保护，不应单独实例化；实际绘制请用 `QSGGeometryNode`，实际裁剪请用 `QSGClipNode`。

使用场景通常在 `QQuickItem::updatePaintNode()`：保留旧节点、取得其 geometry、改写顶点数据并标脏。所有 `QSG*` 类型只属于 scene graph 渲染线程，因此 geometry 的创建、写入和销毁都不能放进普通 GUI 线程逻辑。

## 几何指针和所有权

```cpp
auto *node = oldNode ? static_cast<QSGGeometryNode *>(oldNode)
                     : new QSGGeometryNode;

if (!node->geometry()) {
    auto *geometry = new QSGGeometry(QSGGeometry::defaultAttributes_Point2D(), 4);
    node->setGeometry(geometry);
    node->setFlag(QSGNode::OwnsGeometry);
}
```

`setGeometry()` 仅关联指针，默认不接管 geometry。设置 `QSGNode::OwnsGeometry` 后，节点析构或换入另一 geometry 时会删除当前对象；未设置该标志则必须由调用方管理生命期。不要混用两种模式，否则容易泄漏或二次释放。

已经绑定的 geometry 被原地修改时，必须调用 `node->markDirty(QSGNode::DirtyGeometry)`，否则 renderer 可以继续使用之前上传的顶点/索引数据。仅替换指针时使用 `setGeometry()` 本身即可表达关联变化。

`matrix()` 与 `clipList()` 是 renderer 为该节点计算的内部状态，供 scene graph 实现使用，不应由普通派生代码存储或修改。

## API 速查表

| API | 语义 | 关键边界 |
|---|---|---|
| 构造函数 | 建立几何 node 的共享基类部分 | 受保护；不直接实例化 |
| `setGeometry(QSGGeometry *)` | 关联 node 的 geometry | 默认不取得所有权；原地改数据后另行标记 `DirtyGeometry` |
| `geometry()` | 返回当前 geometry 指针 | 默认是 `nullptr`；在使用顶点数据前检查或创建 |
| `QSGNode::OwnsGeometry` | 让 node 自动删除关联 geometry | 只能在明确独占时设置，避免外部重复释放 |
| `matrix()` | 返回 renderer 计算出的变换矩阵 | renderer 内部状态，不是应用侧变换入口 |
| `clipList()` | 返回作用于节点的 clip 链 | renderer 内部状态，不手工修改 |
