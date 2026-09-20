# QSGImageNode：由当前 scene graph 后端实现的贴图几何节点

> Qt 6.11.1 | `#include <QSGImageNode>` | CMake: `Qt6::Quick`

`QSGImageNode` 是贴图绘制的抽象接口，继承 `QSGGeometryNode`。它把目标区域、源区域、纹理、采样方式、镜像和纹理所有权组合起来，同时由当前 scene graph backend 提供真正实现。通常不直接派生或 `new` 它，而是在 `updatePaintNode()` 中调用 `window()->createImageNode()`。

它适合自定义 item 显示 `QSGTexture`、对一个纹理做裁切、缩放和镜像，或包装来自 image provider、离屏渲染、视频帧的纹理。加入 scene graph 前必须设置 texture，否则没有可绘制内容。

## 创建并配置一个 image node

```cpp
auto *node = window()->createImageNode();
node->setTexture(texture);
node->setRect(boundingRect());
node->setSourceRect(QRectF(0, 0, texture->textureSize().width(),
                           texture->textureSize().height()));
node->setFiltering(QSGTexture::Linear);
node->setOwnsTexture(true);
```

`rect` 是 item 坐标系中的目标区域；`sourceRect` 选择 texture 中要显示的源区域。纹理来自 atlas 或 source origin 与 Quick 不同时，不要手改随机 UV：使用 `setTextureCoordinatesTransform()` 的水平/垂直镜像标志，或让 `rebuildGeometry()` 结合 texture 的规范化子区域重建几何。

默认 node 不拥有 texture。若 texture 是此次创建后仅由该 node 使用，设置 `setOwnsTexture(true)`；若由 texture provider、缓存或多个 node 共用，就保持 false，并在外部统一管理生命期。

## 采样选择

`Nearest` 适合像素风、整数倍缩放和不希望模糊的图标；`Linear` 用于平滑缩放。mipmap filtering 只有 texture 实际带 mipmap 时才有意义。各向异性等级通常只在纹理以很大倾角采样时考虑，具体效果受后端支持限制。

## API 速查表

| API | 语义 | 关键边界 |
|---|---|---|
| `QQuickWindow::createImageNode()` | 创建当前 backend 对应的 image node | 在 scene graph 渲染线程调用；不要直接实例化抽象类 |
| `setTexture()` / `texture()` | 设置或取得待显示的 `QSGTexture` | 入树绘制前必须有 texture；默认不取得所有权 |
| `setOwnsTexture()` / `ownsTexture()` | 设定 node 是否删除 texture | 仅独占 texture 才设 true，避免共享纹理被提前释放 |
| `setRect()` / `rect()` | 设置纹理映射到 item 内的目标矩形 | 使用 item 局部坐标；仅缩放/定位，不改变 texture 内容 |
| `setSourceRect()` / `sourceRect()` | 设置 texture 内的源区域 | 选择区域时应与 `textureSize()` 和 atlas 子区域规则一致 |
| `setFiltering()` / `filtering()` | 设置主纹理采样为 `Nearest` 或 `Linear` | `Linear` 平滑缩放，`Nearest` 保持像素边缘 |
| `setMipmapFiltering()` / `mipmapFiltering()` | 设置 mipmap 层级间采样方式 | 纹理无 mipmap 时没有实际收益 |
| `setAnisotropyLevel()` / `anisotropyLevel()` | 设置各向异性采样等级 | 效果及可用等级取决于后端和纹理使用方式 |
| `setTextureCoordinatesTransform()` | 设置水平或垂直纹理坐标镜像 | 用于方向差异；不改 texture 像素本身 |
| `NoTransform` / `MirrorHorizontally` / `MirrorVertically` | 纹理坐标变换标志 | 可组合镜像方向，不替代正确的源区域设定 |
| `rebuildGeometry()` | 依据 texture、目标/源区域和变换模式重建贴图 geometry | 适合实现 backend image node；参数与 texture/atlas 状态需一致 |
