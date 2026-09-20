# QSGGeometry::ColoredPoint2D：带每顶点 RGBA 的二维顶点

> Qt 6.11.1 | `#include <QSGGeometry>` | CMake: `Qt6::Quick`

`QSGGeometry::ColoredPoint2D` 是内置的顶点结构，按顺序存储 `float x, y` 与四个 `uchar` 颜色通道。它用于同一几何内需要渐变、分段色或顶点着色的图形，例如热力图色带、波形填充、带颜色插值的三角形。

它必须与 `QSGGeometry::defaultAttributes_ColoredPoint2D()` 一起使用；把它强行写到 `Point2D` 或纹理布局的 geometry 内存中会破坏 stride 与 attribute 解释。颜色分量是 0 到 255 的字节，不是 0 到 1 的 float。

```cpp
auto *vertices = geometry->vertexDataAsColoredPoint2D();
vertices[0].set(0.0f, 0.0f, 255, 64, 64, 255);
vertices[1].set(80.0f, 0.0f, 64, 128, 255, 255);
node->markDirty(QSGNode::DirtyGeometry);
```

在预乘 alpha 的合成上下文中，若材质和渲染路径要求预乘颜色，半透明 RGB 应与 alpha 的约定一致；此结构只是传递原始分量，不会自动修正混合方式。

## API 速查表

| API | 语义 | 关键边界 |
|---|---|---|
| `x`, `y` | 顶点二维位置 | `float`，坐标系由所在 item/geometry 决定 |
| `r`, `g`, `b`, `a` | 顶点颜色通道 | `uchar`，范围为 0 到 255 |
| `set(x, y, r, g, b, a)` | 一次写入位置与 RGBA | 不校验颜色范围；调用后仍须标记所属 node `DirtyGeometry` |
| `defaultAttributes_ColoredPoint2D()` | 对应此内存布局的标准 attribute set | 仅该布局可用 `vertexDataAsColoredPoint2D()` |
| `vertexDataAsColoredPoint2D()` | 将 geometry 内存作为此顶点数组访问 | geometry 布局不匹配会断言失败 |
