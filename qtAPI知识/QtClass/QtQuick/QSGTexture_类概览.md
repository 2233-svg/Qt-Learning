# QSGTexture：场景图材质使用的纹理与采样状态

> Qt 6.11.1 · `#include <QSGTexture>` · 模块：`Qt6::Quick` · 继承：`QObject`

`QSGTexture` 是 Qt Quick 场景图中的纹理抽象。它把图片、视频帧、alpha 蒙版等像素来源统一交给材质采样，并附带过滤、环绕和各向异性等采样状态；默认实现通常由 `QQuickWindow` 的工厂函数创建。

## 解决的问题与实际场景

自定义 Item 想显示 `QImage` 时，应在场景图生命周期内通过 `QQuickWindow::createTextureFromImage()` 创建纹理，再交给图像节点或自定义材质。视频渲染、相机帧或动态 alpha 图也可派生 `QSGTexture` 实现自己的来源，但必须提供尺寸、alpha、mipmap、比较键等核心信息。

纹理不是简单的原生句柄包装。Qt Quick 可能将小图打入 atlas，以提升排序和批处理效率；材质代码不能把 `(0, 0, 1, 1)` 一律视为有效完整区域，应通过 `normalizedTextureSubRect()` 或 `convertToNormalizedSourceRect()` 处理坐标。

## 生命周期与后端边界

所有 `QSGTexture` API 仅应在场景图渲染线程使用。不要把 `rhiTexture()` 的结果、原生接口指针或图集外拷贝跨帧缓存为永久资源：图形设备、渲染目标与底层实现都可能在设备丢失或场景图重建后失效。

`QSGTexture` 不区分 image 与 sampler；设置过滤和环绕模式后，Qt/QRhi 按当前后端创建需要的 sampler。各向异性是请求而非保证，目标图形 API 或硬件可能忽略它。mipmap 过滤在纹理没有 mipmap 时没有效果。

## 图集、比较与上传

材质排序应使用 `comparisonKey()`，不能只比较 `QSGTexture *`，因为两个对象可能对应同一原生纹理。若图集妨碍第三方 API 使用，可在渲染线程调用 `removedFromAtlas()` 获得非图集副本；返回空表示原纹理本就不在图集内。默认纹理上传实现通过 `commitTextureOperations()` 把待上传操作加入 `QRhiResourceUpdateBatch`，自定义采样材质通常在 `updateSampledImage()` 中调用它。

## API 速查表

| API | 语义与边界 |
|---|---|
| `QQuickWindow::createTextureFromImage()` | 创建默认 RGBA 纹理的常用入口，优于尝试直接构造默认实现。 |
| `comparisonKey()` | 纯虚函数；供材质比较与批处理排序使用，只能在渲染线程调用。 |
| `textureSize()` | 纯虚函数；返回像素尺寸。 |
| `hasAlphaChannel()` / `hasMipmaps()` | 纯虚函数；分别说明是否包含 alpha 与 mipmap 层级。 |
| `rhiTexture()` | Qt 6.0 起返回底层 `QRhiTexture`，未创建或当前后端不适用时为空；不负责创建。 |
| `nativeInterface<T>()` | 查询特定原生纹理接口；当前后端不支持时返回空。 |
| `commitTextureOperations(rhi, updates)` | 将待上传数据排入更新批；自定义纹理材质通常从 `updateSampledImage()` 调用。 |
| `normalizedTextureSubRect()` | 返回纹理在底层图像内的归一化子区域；atlas 纹理尤为重要。 |
| `convertToNormalizedSourceRect(rect)` | 将像素源区域换算为考虑子区域后的归一化纹理坐标。 |
| `isAtlasTexture()` | 判断纹理是否位于 atlas；默认实现为 `false`。 |
| `removedFromAtlas(updates)` | 为 atlas 纹理生成非图集副本；非 atlas 时返回空，只能在渲染线程调用。 |
| `setFiltering()` / `filtering()` | 设置或读取主采样方式：`Nearest` 保留像素感，`Linear` 平滑插值。 |
| `setMipmapFiltering()` / `mipmapFiltering()` | 设置或读取 mipmap 采样方式；无 mipmap 时无效果，`None` 仅用于此项。 |
| `setHorizontalWrapMode()` / `horizontalWrapMode()` | 设置或读取水平方向 `Repeat`、`ClampToEdge` 或 `MirroredRepeat`。 |
| `setVerticalWrapMode()` / `verticalWrapMode()` | 设置或读取垂直方向环绕方式。 |
| `setAnisotropyLevel()` / `anisotropyLevel()` | 请求各向异性采样级别；图形 API 可以忽略该请求。 |
| `AnisotropyNone` 至 `Anisotropy16x` | 纹理相对屏幕倾斜时的采样质量级别。 |
