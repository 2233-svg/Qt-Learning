# QSGVertexColorMaterial：使用顶点自身颜色绘制几何

> Qt 6.11.1 · `#include <QSGVertexColorMaterial>` · 模块：`Qt6::Quick` · 继承：`QSGMaterial`

`QSGVertexColorMaterial` 是场景图内置材质，用于“颜色随顶点变化”的几何。它不保存单一颜色属性，而是读取顶点数据中的颜色 attribute，并在像素之间线性插值。

## 适用场景

渐变多边形、热力图网格、彩色折线、每个顶点透明度不同的粒子形状，都适合用它。相比给每个三角形单独创建材质，顶点颜色能把颜色变化放进一批几何数据中，减少状态切换。

它需要几何布局满足固定约定：attribute 0 是顶点位置，attribute 1 是 RGBA 颜色四元组。颜色可以是 `0..1` 的浮点，也可以是 `0..255` 的无符号字节。最省心的方式是用 `QSGGeometry::defaultAttributes_ColoredPoint2D()` 和 `QSGGeometry::ColoredPoint2D`。

## 关键边界

该材质会尊重当前矩阵和当前继承透明度，因此挂在 `QSGTransformNode` 或 `QSGOpacityNode` 下时会自然组合。若直接改顶点数组中的颜色或坐标，必须对几何节点调用 `markDirty(QSGNode::DirtyGeometry)`，否则渲染器可能继续使用旧数据。

它只负责按顶点颜色着色，不提供纹理采样、描边、光照或任意 shader 逻辑。需要自定义效果时，应转向 `QSGMaterial` 与 `QSGMaterialShader`。

## API 速查表

| API | 语义与边界 |
|---|---|
| `QSGVertexColorMaterial()` | 创建顶点颜色材质，没有额外公开属性需要设置。 |
| `QSGGeometry::defaultAttributes_ColoredPoint2D()` | 推荐的兼容 attribute 布局：位置在 attribute 0，RGBA 颜色在 attribute 1。 |
| `QSGGeometry::ColoredPoint2D` | 常用顶点结构，包含位置与颜色。 |
| 继承的 `QSGMaterial::type()` | 由内置实现返回材质类型，场景图据此缓存 shader。 |
| 继承的 `QSGMaterial::createShader()` | 由内置实现创建对应 shader；应用代码通常不直接调用。 |
| `QSGNode::DirtyGeometry` | 修改顶点位置或颜色后应标记的脏状态。 |
