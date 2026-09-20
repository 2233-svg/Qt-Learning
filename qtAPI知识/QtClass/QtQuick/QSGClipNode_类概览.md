# QSGClipNode：限制子树绘制范围的 scene graph 节点

> Qt 6.11.1 | `#include <QSGClipNode>` | CMake: `Qt6::Quick`

`QSGClipNode` 用一份 `QSGGeometry` 定义裁剪形状，并将裁剪作用于它的整个子树。多个 clip node 嵌套时，renderer 取各自几何区域的交集；实现通常依赖 stencil buffer，因此裁剪不是免费操作。

它适合 `updatePaintNode()` 中的自定义 item：例如让任意形状的自绘子内容只出现在圆角区域内，或把自定义几何与视觉节点分成“裁剪父节点 + 被裁剪的子节点”。普通矩形 `Item { clip: true }` 已能覆盖的需求通常没有必要手写此类。

## 先有 geometry，才能放进树

```cpp
auto *clip = new QSGClipNode;
auto *geometry = new QSGGeometry(QSGGeometry::defaultAttributes_Point2D(), 4);
QSGGeometry::updateRectGeometry(geometry, QRectF(0, 0, width(), height()));

clip->setGeometry(geometry);
clip->setFlag(QSGNode::OwnsGeometry);
clip->setClipRect(QRectF(0, 0, width(), height()));
clip->setIsRectangular(true);
clip->appendChildNode(contentNode);
```

clip node 在加入 scene graph 前必须已关联 geometry。`clipRect` 是对裁剪区域的矩形描述；若实际裁剪形状确实是轴对齐矩形，同时设 `setIsRectangular(true)`，renderer 有机会使用更快的裁剪策略。这个布尔值是性能提示，不会自动把任意 geometry 变成矩形。

更新 geometry 顶点后要按基类规则 `markDirty(QSGNode::DirtyGeometry)`。设置 `OwnsGeometry` 时由 clip node 释放 geometry；没有设置时由外部负责，不能两边都 delete。

## API 速查表

| API | 语义 | 关键边界 |
|---|---|---|
| `QSGClipNode()` | 创建裁剪节点 | 加入树前必须通过 `setGeometry()` 赋予几何 |
| `setGeometry()` / `geometry()` | 设置或取得裁剪几何 | 默认不拥有 geometry；原地修改后标记 `DirtyGeometry` |
| `setClipRect(rect)` / `clipRect()` | 设置或读取裁剪矩形描述 | 应与实际 geometry 的范围保持一致 |
| `setIsRectangular(true)` / `isRectangular()` | 告诉 renderer 裁剪形状为矩形 | 仅在确为矩形时设置，便于优化 |
| `appendChildNode()` 等继承接口 | 把待裁剪内容置于此节点子树 | 裁剪只影响子树，可嵌套并与外层裁剪求交 |
| `QSGNode::OwnsGeometry` | 让节点回收裁剪几何 | 仅在独占 geometry 时使用 |
