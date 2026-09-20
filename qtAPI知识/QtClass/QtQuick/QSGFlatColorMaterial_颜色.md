# QSGFlatColorMaterial：绘制单一颜色几何的默认后端材质

> Qt 6.11.1 | `#include <QSGFlatColorMaterial>` | CMake: `Qt6::Quick`

`QSGFlatColorMaterial` 是给 `QSGGeometryNode` 使用的现成材质：不采样纹理、不处理每顶点颜色，只用一个 `QColor` 绘制整份 geometry。它适合自定义 item 中的纯色矩形、折线填充、多边形背景和简单调试形状，省去实现 `QSGMaterial`、shader 和 uniform 的成本。

它不是通用可移植材质。官方限定该工具类仅在 Qt Quick scene graph 的默认 backend 下工作；选择自定义 scene graph backend 时，不应依赖它。所有 QSG material 和 node 的创建、修改也只应发生在 scene graph 渲染线程。

## 与几何节点一起使用

```cpp
auto *node = new QSGGeometryNode;
auto *material = new QSGFlatColorMaterial;
material->setColor(QColor("#2f80ed"));

node->setMaterial(material);
node->setFlag(QSGNode::OwnsMaterial);
```

材质只描述颜色，形状仍由 `QSGGeometry` 决定。修改颜色时对 node 调用 `markDirty(QSGNode::DirtyMaterial)`，否则 renderer 可能继续使用已提交的材质状态。设置 `OwnsMaterial` 后 node 在析构或替换材质时回收该 material；未设置时由外部所有者负责。

带透明度的颜色会进入混合路径。若内容确实完全不透明，使用 alpha 为 255 的颜色并避免不必要的透明覆盖，有利于 renderer batching 和合成。

## API 速查表

| API | 语义 | 关键边界 |
|---|---|---|
| `QSGFlatColorMaterial()` | 创建默认白色的纯色材质 | 仅默认 scene graph backend 有效 |
| `setColor(color)` | 设置整份几何使用的颜色 | 改完后对所属 node 标记 `DirtyMaterial` |
| `color()` | 返回当前颜色 | 默认白色 |
| `QSGGeometryNode::setMaterial()` | 将材质挂到几何节点 | 仍需为 node 设置 geometry 才能绘制 |
| `QSGNode::OwnsMaterial` | 让 node 自动删除材质 | 仅当 material 为该 node 独占时设置 |
| `QSGNode::DirtyMaterial` | 通知 renderer 材质参数变动 | 原地改变颜色后必须标记 |
