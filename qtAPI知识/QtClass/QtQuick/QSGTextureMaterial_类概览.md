# QSGTextureMaterial：遵守 item 树透明度的通用贴图材质

> Qt 6.11.1 | `#include <QSGTextureMaterial>` | CMake: `Qt6::Quick`

`QSGTextureMaterial` 是 `QSGOpaqueTextureMaterial` 的透明度感知版本，用一个 `QSGTexture` 填充 geometry，并正确应用 scene graph 的累计 opacity。它适合绝大多数自定义贴图内容：图片、视频帧、离屏渲染结果、带 alpha 的图标，以及需要随父 item 淡入淡出的纹理节点。

它复用父类的 texture、filtering、mipmap、wrap 和 anisotropy API，差别只在 material/shader 选择：此类会尊重纹理 alpha 和 item tree 传下来的透明度，因此是一般场景的默认选择；确认节点永远不需要累计 opacity 时才改用 `QSGOpaqueTextureMaterial` 争取更轻的路径。

该便利类仅适用于 Qt Quick 默认 scene graph backend。它不拥有传入的 `QSGTexture`，并且与所有 QSG 对象一样只在 scene graph 渲染线程使用。

## 最小使用方式

```cpp
auto *geometry = new QSGGeometry(
    QSGGeometry::defaultAttributes_TexturedPoint2D(), 4);
QSGGeometry::updateTexturedRectGeometry(
    geometry, boundingRect(), texture->normalizedTextureSubRect());

auto *material = new QSGTextureMaterial;
material->setTexture(texture);
material->setFiltering(QSGTexture::Linear);

node->setGeometry(geometry);
node->setMaterial(material);
node->setFlag(QSGNode::OwnsGeometry);
node->setFlag(QSGNode::OwnsMaterial);
```

顶点必须在 location 0 提供二维位置、在 location 1 提供二维浮点 UV，内置 `defaultAttributes_TexturedPoint2D()` 正好满足。texture 需要在 geometry node 被绘制前设置；对于 atlas texture，用 `normalizedTextureSubRect()`，避免将完整 `0..1` UV 错误映射到整张图集。

采样状态由继承 API 在 texture 绑定前应用，因此同一 texture 被不同材质以不同参数共享时，应意识到状态可能按 draw 切换。Mipmap filtering 只有 texture 实际具备 mipmap 才能改善缩小采样。

## API 速查表

| API | 语义 | 关键边界 |
|---|---|---|
| `QSGTextureMaterial()` | 创建遵守累计 opacity 的贴图材质 | 仅 Qt Quick 默认 backend；适合一般带 alpha 内容 |
| 继承的 `setTexture()` / `texture()` | 设置或取得 `QSGTexture` | material 不拥有 texture；绘制前不能为空 |
| 继承的 `setFiltering()` / `filtering()` | 配置 `Nearest` 或 `Linear` 主采样 | 平滑缩放使用 `Linear`，像素风使用 `Nearest` |
| 继承的 `setMipmapFiltering()` / `mipmapFiltering()` | 配置 mipmap 采样 | texture 无 mipmap 时无效果 |
| 继承的 `setHorizontalWrapMode()` / `setVerticalWrapMode()` | 配置 UV 边界采样 | 默认 `ClampToEdge`；atlas texture 不应随意 repeat |
| 继承的 `setAnisotropyLevel()` | 配置倾斜采样品质 | 是否生效取决于后端 |
| 累积 opacity | 应用父级 `Opacity` node 和 item tree 透明度 | 与 `QSGOpaqueTextureMaterial` 的决定性差异 |
| `defaultAttributes_TexturedPoint2D()` | 此材质要求的顶点布局 | location 0 为 position、location 1 为二维 UV |
| `QSGTexture::normalizedTextureSubRect()` | 取 atlas/子纹理正确 UV | 绘制 texture atlas 中的子图时优先使用 |
