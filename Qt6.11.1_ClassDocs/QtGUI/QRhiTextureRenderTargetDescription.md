# QRhiTextureRenderTargetDescription
> Qt 6.11.1 · Qt GUI [Private] · 来自 `QRhiTextureRenderTargetDescription`

## 1. 先建立直觉

`QRhiTextureRenderTargetDescription` 是离屏渲染目标的附件清单。它本身不创建 GPU 对象，而是告诉 `QRhiTextureRenderTarget`：颜色写到哪些 `QRhiColorAttachment`，深度模板用 `QRhiRenderBuffer` 还是 `QRhiTexture`，是否需要深度 resolve 或 shading rate map。

可以把它理解为“render target 的结构描述”。结构一变，兼容的 render pass descriptor 和 graphics pipeline 往往也要跟着变。

## 2. 类说明

- 头文件：`#include <rhi/qrhi.h>`
- CMake：`target_link_libraries(mytarget PRIVATE Qt6::GuiPrivate)`
- 类型：轻量值类型，保存附件指针和附件描述
- 归属：RHI 私有接口，来自 `QRhiTextureRenderTargetDescription`

它不拥有传入的纹理、render buffer 或 shading rate map。调用者要保证这些资源活得比使用它创建的 render target 更久，并且在 render target `create()` 前已经创建。

## 3. API 速查

| API | 作用 |
| --- | --- |
| 默认构造 | 创建空描述，之后手动设置附件 |
| `QRhiTextureRenderTargetDescription(color)` | 单颜色附件 |
| `QRhiTextureRenderTargetDescription(color, depthStencilBuffer)` | 颜色附件加深度/模板 render buffer |
| `QRhiTextureRenderTargetDescription(color, depthTexture)` | 颜色附件加可采样深度纹理 |
| `setColorAttachments(...)` | 设置一个或多个颜色附件 |
| `colorAttachmentCount()` / `colorAttachmentAt()` | 查询颜色附件数量和指定附件 |
| `cbeginColorAttachments()` / `cendColorAttachments()` | 遍历颜色附件 |
| `setDepthStencilBuffer()` / `depthStencilBuffer()` | 使用 render buffer 作为深度/模板附件 |
| `setDepthTexture()` / `depthTexture()` | 使用纹理作为深度/模板附件 |
| `setDepthResolveTexture()` / `depthResolveTexture()` | Qt 6.8 起设置 MSAA 深度 resolve 目标 |
| `setShadingRateMap()` / `shadingRateMap()` | Qt 6.9 起绑定 variable rate shading map |

## 4. 关键用法

最常见的描述是一个颜色附件加一个深度 render buffer：

```cpp
QRhiTextureRenderTargetDescription desc(
    QRhiColorAttachment(colorTexture),
    depthStencilRenderBuffer);
```

如果后续要把深度当纹理采样，例如屏幕空间效果、阴影可视化、深度金字塔，就改用 depth texture：

```cpp
desc.setDepthTexture(depthTexture);
```

`setDepthStencilBuffer()` 和 `setDepthTexture()` 二选一。render buffer 更适合“只给本次 pass 做深度测试”，纹理更适合“pass 后还要读”。这不是语法偏好，而是内存布局、性能和跨后端能力的选择。

多颜色附件用于 MRT：

```cpp
desc.setColorAttachments({
    QRhiColorAttachment(albedoTexture),
    QRhiColorAttachment(normalTexture),
    QRhiColorAttachment(materialTexture)
});
```

shader 的输出 location、pipeline 的 color attachment count、render target description 必须互相对齐。

## 5. 使用场景

- 单纹理离屏渲染：UI 截图、缩略图、视频帧合成、后处理输入。
- G-buffer：多个颜色附件一次写入不同材质数据。
- MSAA resolve：颜色或深度先写多采样资源，再解析到可采样纹理。
- 多视图渲染：深度纹理数组比普通 render buffer 更有意义。
- 可变着色率：`setShadingRateMap()` 把 shading rate map 纳入 render pass 兼容性。

## 6. 常见坑与经验

- `depthStencilBuffer()` 和 `depthTexture()` 不能同时非空。两者代表不同资源路径，不是备用关系。
- depth texture 的格式必须适合深度用途，例如 `D16`、`D32F` 或包含 stencil 的格式；普通颜色纹理不能凑数。
- `setDepthResolveTexture()` 依赖 `QRhi::ResolveDepthStencil`，不是所有后端都支持，OpenGL ES 上限制尤其多。
- Qt 6.9 的 shading rate map 会改变 render pass 兼容性。已经创建过 target 后再设置它，需要新的 descriptor、target `create()`、pipeline 重建。
- `setColorAttachments(first, last)` 只是复制附件描述，不拥有底层纹理；底层资源生命周期仍然由调用者管理。

## 7. 知识点覆盖

本页覆盖：颜色附件列表、深度/模板资源选择、深度纹理与 render buffer 的取舍、MRT、MSAA 深度 resolve、VRS shading rate map、render pass descriptor 兼容性、资源生命周期。
