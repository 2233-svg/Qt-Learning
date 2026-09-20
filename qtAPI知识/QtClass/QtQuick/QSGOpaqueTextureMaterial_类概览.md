# QSGOpaqueTextureMaterial：不参与 scene graph 累积透明度的贴图材质

> Qt 6.11.1 | `#include <QSGOpaqueTextureMaterial>` | CMake: `Qt6::Quick`

`QSGOpaqueTextureMaterial` 是为带纹理 geometry 准备的现成材质，使用位置在 attribute location 0、二维 UV 在 location 1 的布局。它适合已知不受父级透明度影响的纹理内容，例如固定不透明的背景面、内部渲染目标或不参与 item opacity 动画的专用节点。

“Opaque”最容易被误读：它并不强制纹理没有 alpha，也仍会采样 alpha 通道；它的核心差异是**忽略 scene graph 累积 opacity**。因此把它放进带 `Opacity` 父节点、`Item::opacity` 动画或其他需要整体淡入淡出的子树，会出现该纹理不随父级透明度淡出的结果。需要遵守积累 opacity 时使用 `QSGTextureMaterial`。

该工具类仅在 Qt Quick 默认 scene graph backend 中工作。和其他 QSG material 一样，只能在 scene graph 渲染线程配置和使用。

## 典型配置

```cpp
auto *material = new QSGOpaqueTextureMaterial;
material->setTexture(texture);
material->setFiltering(QSGTexture::Linear);
material->setMipmapFiltering(QSGTexture::Linear);
material->setHorizontalWrapMode(QSGTexture::ClampToEdge);
material->setVerticalWrapMode(QSGTexture::ClampToEdge);
```

geometry 必须采用 `QSGGeometry::defaultAttributes_TexturedPoint2D()` 兼容的布局。material 不接管 `texture` 的所有权，须由 node、texture provider 或其他明确所有者管理。

过滤、mipmap、wrap 和 anisotropy 设置会在 texture 绑定前应用到 texture 实例。共享同一个 `QSGTexture` 给多个材质并配置不同采样状态虽然可以工作，但不能把 texture 自身当前的采样状态当成永久不变；必要时避免共享或统一设置。

## API 速查表

| API | 语义 | 关键边界 |
|---|---|---|
| `QSGOpaqueTextureMaterial()` | 创建不使用累积 opacity 的贴图材质 | 默认 filtering/mipmap 为 `Nearest`，wrap 为 `ClampToEdge` |
| `setTexture()` / `texture()` | 设置或取得采样纹理 | 入树前必须设置；material 不取得 texture 所有权 |
| `setFiltering()` / `filtering()` | 设置主采样过滤 | `Nearest` 保持像素边缘，`Linear` 平滑缩放 |
| `setMipmapFiltering()` / `mipmapFiltering()` | 设置 mipmap 层级间过滤 | 无 mipmap texture 时无效果 |
| `setHorizontalWrapMode()` / `horizontalWrapMode()` | 设置 U 方向 wrap | 默认 `ClampToEdge`；图集 texture 通常不应使用 repeat |
| `setVerticalWrapMode()` / `verticalWrapMode()` | 设置 V 方向 wrap | 默认 `ClampToEdge` |
| `setAnisotropyLevel()` / `anisotropyLevel()` | 设置各向异性采样等级 | 受后端支持限制，通常仅斜角采样时有意义 |
| 默认 backend 限制 | 使用 Qt Quick 内建默认 scene graph 实现 | 自定义 backend 下不能依赖该便利类 |
| 忽略累积 opacity | 不应用父 `Opacity` node 和 item tree 的透明度 | 仅当此行为符合视觉预期时使用 |
| `defaultAttributes_TexturedPoint2D()` | 此材质要求的位置 + 二维 UV 布局 | 顶点位置必须为 location 0、UV 为 location 1 |
