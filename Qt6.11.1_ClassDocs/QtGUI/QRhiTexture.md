# QRhiTexture

> Qt 6.11.1 · Qt GUI Private · 来自 `QRhiTexture`

## 1. 先建立直觉

`QRhiTexture` 是 RHI 中的 GPU 图像资源。它可以作为 shader 采样输入、render target 颜色/深度附件、transfer copy/readback 源、storage image、mipmap 容器、cubemap、texture array、3D texture 或 VRS map。纹理最重要的不是“有一张图”，而是 **创建前声明它将如何被使用**。

例如：要渲染到纹理，必须带 `RenderTarget`；要读回或复制出，必须带 `UsedAsTransferSource`；要 compute image load/store，必须带 `UsedWithLoadStore`；要生成 mip，必须同时考虑 `MipMapped` 和 `UsedWithGenerateMips`。

## 2. 类说明

- 头文件：`#include <rhi/qrhi.h>`
- CMake：`Qt6::GuiPrivate`
- 继承自：`QRhiResource`
- 创建入口：`QRhi::newTexture()` / `newTextureArray()`
- 相关对象：`QRhiSampler`、`QRhiTextureRenderTarget`、`QRhiResourceUpdateBatch`

纹理的 format、pixel size、sample count、flags、array size、depth、view format 通常都要在 `create()` 前设置。改变后需重新 `create()`。

## 3. API 速查

| API / 族 | 作用 |
| --- | --- |
| `create()` | 创建底层纹理。 |
| `createFrom(NativeTexture)` | 导入外部 native texture；RHI 不拥有外部对象。 |
| `nativeTexture()` | 暴露后端 native texture，可能不可用。 |
| `Format` | 纹理像素格式，如 `RGBA8`、`BGRA8`、`R8`、`RGBA16F`、深度格式、压缩格式、整数格式。 |
| `RenderTarget` | 允许 texture 作为 texture render target 附件。 |
| `MipMapped` | 纹理拥有 mip 链。 |
| `sRGB` | 使用 sRGB 格式/视图语义。 |
| `UsedAsTransferSource` | 允许作为 texture copy 或 readback 源。 |
| `UsedWithGenerateMips` | 允许 `generateMips()`。 |
| `UsedWithLoadStore` | 允许 storage image 的 image load/store。 |
| `CubeMap` | 6 个面组成 cubemap。 |
| `TextureArray` | 由多个同尺寸 2D layer 组成。 |
| `ThreeDimensional` | 3D texture，layer 对应 Z slice。 |
| `OneDimensional` | 1D texture，后端支持有限。 |
| `ExternalOES` / `TextureRectangleGL` | OpenGL 特殊原生纹理目标。 |
| `UsedAsShadingRateMap` | 用作 VRS shading rate map 的纹理。 |
| `setPixelSize()` / `pixelSize()` | 设置/读取宽高。 |
| `setDepth()` / `depth()` | 设置/读取 3D texture 深度。 |
| `setArraySize()` / `arraySize()` | 设置/读取 texture array 层数。 |
| `setArrayRange()` | Qt 6.8 起限制对 shader 暴露的数组层范围，需 feature 支持。 |
| `setSampleCount()` / `sampleCount()` | 设置/读取 MSAA sample count。 |
| `setReadViewFormat()` / `setWriteViewFormat()` | Qt 6.8 起设置读取/写入视图格式，需 `TextureViewFormat` 支持。 |
| `setNativeLayout()` | 声明外部 native layout，主要用于互操作。 |

## 4. 格式速查

| 格式类别 | 典型格式 | 适用场景 |
| --- | --- | --- |
| 常规颜色 | `RGBA8`、`BGRA8` | 通用贴图、UI、渲染颜色附件。 |
| 单/双通道 | `R8`、`RG8`、`R16`、`RG16` | mask、数据图、法线/参数编码。 |
| 浮点 | `RGBA16F`、`RGBA32F`、`R16F`、`R32F` | HDR、滤镜、中间渲染结果。 |
| 深度/模板 | `D16`、`D24`、`D24S8`、`D32F`、`D32FS8` | depth test、shadow map、stencil。 |
| 整数 | `R8UI`、`R32UI`、`RGBA32UI` 等 | ID buffer、compute 数据、VRS map。 |
| 压缩 | BC、ETC2、ASTC 系列 | 体积/带宽优化，需检查后端支持。 |

## 5. 关键用法

### 普通可采样纹理

```cpp
QRhiTexture *tex = rhi->newTexture(QRhiTexture::RGBA8, image.size());
tex->create();

QRhiResourceUpdateBatch *u = rhi->nextResourceUpdateBatch();
u->uploadTexture(tex, image);
```

上传图片时格式要兼容。纹理创建成功不等于图片数据已上传，上传操作会在 batch 提交后执行。

### 离屏渲染后再采样

```cpp
QRhiTexture *color = rhi->newTexture(
    QRhiTexture::RGBA16F, size, 1, QRhiTexture::RenderTarget);
color->create();
```

此纹理可以放进 `QRhiTextureRenderTarget` 的 color attachment，随后作为 `sampledTexture` 给下一个 pass 使用。

### 可读回纹理

```cpp
QRhiTexture *capture = rhi->newTexture(
    QRhiTexture::RGBA8, size, 1,
    QRhiTexture::RenderTarget | QRhiTexture::UsedAsTransferSource);
```

如果后续需要 screenshot/readback，必须在创建时就声明 `UsedAsTransferSource`。

## 6. 常见坑与经验

- **usage flags 要在 create 前声明。** 后端可能无法把“普通采样纹理”临时变成 render target 或 transfer source。
- **MSAA texture 不能有 mipmap，也不能直接 readback。** 常见方案是 resolve 到 sampleCount 为 1 的 texture。
- **格式支持不是假设。** 使用浮点、深度、压缩、整数格式前调用 `isTextureFormatSupported()`。
- **cubemap/array/3D 的 layer 语义不同。** copy、upload、attachment、readback 的 layer 要按对应纹理类型理解。
- **导入 native texture 不转移所有权。** 尺寸、格式、flags、sample count 也必须由调用方正确填写。
- **sRGB 是颜色空间语义。** sRGB texture 的采样/写入转换要和 shader、render target、图片资源的色彩管理配套。
- **view format 是高级互操作。** Qt 6.8 起的 read/write view format 受后端格式兼容规则限制，先检查 feature。

## 7. 知识点覆盖

- texture format、颜色/深度/整数/压缩纹理
- render target、sampling、transfer、readback、storage image 用途声明
- mipmap、MSAA、resolve、sRGB、HDR
- cubemap、texture array、3D/1D texture
- native texture 导入与 view format
- texture 生命周期、上传和跨后端能力查询
