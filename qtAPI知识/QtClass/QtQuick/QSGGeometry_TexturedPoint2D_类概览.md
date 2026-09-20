# QSGGeometry::TexturedPoint2D：位置与归一化 UV 组成的二维顶点

> Qt 6.11.1 | `#include <QSGGeometry>` | CMake: `Qt6::Quick`

`QSGGeometry::TexturedPoint2D` 是 Qt Quick 的标准贴图顶点：`x`、`y` 是位置，`tx`、`ty` 是纹理坐标。它适合自定义 image node、视频帧、图集子区域、离屏纹理或任何“把一张纹理映射到四边形/网格”的场景。

它必须配合 `QSGGeometry::defaultAttributes_TexturedPoint2D()` 使用。UV 通常是归一化坐标 `0..1`，但图集纹理不可假定完整范围：应从 `QSGTexture::normalizedTextureSubRect()` 取实际 UV 区域，再传给 `updateTexturedRectGeometry()` 或手写顶点。

```cpp
auto *vertices = geometry->vertexDataAsTexturedPoint2D();
vertices[0].set(0.0f, 0.0f, 0.0f, 0.0f);
vertices[1].set(width(), 0.0f, 1.0f, 0.0f);
vertices[2].set(0.0f, height(), 0.0f, 1.0f);
node->markDirty(QSGNode::DirtyGeometry);
```

坐标是否需要上下翻转取决于 texture 的方向约定和材质；不要通过猜测交换 `ty` 来“修正”所有纹理。优先使用纹理的规范化子矩形及对应的 texture-coordinate transform，让 atlas、镜像和后端差异得到正确处理。

## API 速查表

| API | 语义 | 关键边界 |
|---|---|---|
| `x`, `y` | 顶点二维位置 | `float`，由所属 item 的局部坐标系解释 |
| `tx`, `ty` | 顶点纹理坐标 | 通常是归一化 UV，不一定总是完整 `0..1` |
| `set(x, y, tx, ty)` | 一次写入位置与 UV | 不做归一化或方向校正；改写后标记 node `DirtyGeometry` |
| `defaultAttributes_TexturedPoint2D()` | 对应此内存布局的标准 attribute set | 只有匹配时可调用快捷访问器 |
| `vertexDataAsTexturedPoint2D()` | 将 geometry 内存作为此顶点数组访问 | 布局不匹配会断言失败 |
| `updateTexturedRectGeometry()` | 以四顶点 triangle strip 更新矩形和 UV | `textureRect` 必须是归一化坐标 |
| `QSGTexture::normalizedTextureSubRect()` | 取得 atlas/子纹理实际的 UV 区域 | 图集纹理不要硬编码完整 `0..1` 区域 |
