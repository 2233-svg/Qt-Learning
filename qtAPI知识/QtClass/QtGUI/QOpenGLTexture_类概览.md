# Qt QOpenGLTexture 深入笔记

> 适用版本：Qt 6.11.1
> 头文件：`#include <QOpenGLTexture>`
> 所属模块：`Qt6::OpenGL`
> 继承：无，禁止拷贝的 OpenGL 资源包装类

## 它解决什么问题

`QOpenGLTexture` 封装 OpenGL texture object，把纹理目标、内部格式、尺寸、mipmap、array layer、cube face、采样参数、wrap、swizzle、上传数据和绑定纹理单元等操作集中到一个 C++ 对象里。它解决的是“不要在业务代码每处手写 `glTexImage*`、`glTexStorage*`、`glTexParameter*` 和纹理名生命周期”的问题。

它不是 CPU 图像容器。纹理内容位于 GPU，创建、上传、绑定和销毁都要求有兼容的 OpenGL context current。构造自 `QImage` 只是便利入口，真正的资源仍是 OpenGL 纹理名。

## 实际使用场景

- 把图片上传为 2D 纹理供 shader 采样。
- 创建 cube map、array texture、3D volume texture、LUT 或 shadow map。
- 创建多采样纹理或 FBO 附着纹理。
- 使用压缩纹理、sRGB 纹理、深度/模板纹理。
- 在 Qt OpenGL 渲染器中统一管理纹理参数和销毁时机。

如果只是普通界面图片显示，`QPixmap`、`QImage` 或 Qt Quick 图片项更合适。`QOpenGLTexture` 是给直接写 OpenGL 渲染路径用的。

## 生命周期和状态机

一个可靠流程通常是：

1. 构造时选定 `Target`，例如 `Target2D`、`TargetCubeMap` 或 `Target3D`。
2. 在分配存储前设置结构性描述：`setFormat()`、`setSize()`、`setLayers()`、`setMipLevels()`、`setSamples()`。
3. 在兼容 context current 时调用 `create()` 或 `allocateStorage()`。
4. 用 `setData()` 上传像素，或把纹理接到 FBO 由渲染写入。
5. 设置 filter、wrap、comparison、swizzle、LOD 等采样参数。
6. 渲染时 `bind()` 到纹理单元，用完按需要 `release()`。
7. 在 context 仍可用时 `destroy()`，或者确保析构发生在可访问共享组的时机。

分配存储后，内部格式、尺寸、层数、mip 层数和采样数这些结构性属性不能靠 setter 原地变更。要改变它们，通常应销毁并重新创建纹理。

## 格式：内部格式和上传格式别混

`TextureFormat` 是 GPU 侧内部存储格式，例如 `RGBA8_UNorm`、`SRGB8_Alpha8`、`RGBA16F`、`D24S8` 或压缩格式。它决定纹理在显存中如何保存。

`PixelFormat` 和 `PixelType` 描述 CPU 上传缓冲区的排列，例如 RGBA + UInt8、BGRA + UInt8、Depth + Float32。`setData(RGBA, UInt8, data)` 不会把纹理内部格式改成 `RGBA8_UNorm`；内部格式仍由 `setFormat()` 和存储分配决定。

## 目标和能力边界

`Target` 选错通常无法补救：2D、3D、array、cube map、multisample、rectangle、buffer texture 的 OpenGL 语义不同。某些目标和格式依赖 OpenGL 版本或扩展，使用前可以通过 `hasFeature()` 做能力分支。

常见边界：

- 使用 mipmap filter 前必须存在完整 mip 链，可手动上传或调用 `generateMipMaps()`。
- 多采样纹理不能像普通 2D 纹理那样随意上传 level 数据，通常由 FBO 渲染写入并 resolve。
- rectangle texture 使用非归一化坐标，wrap 和 mipmap 能力也不同。
- NPOT texture 在旧实现上可能不能 repeat 或 mipmap，应检查特性或降低要求。
- 纹理名属于创建它的 context share group；不共享的 context 不能直接使用。

## 销毁时机

OpenGL 资源销毁也需要 context。最稳妥的方式是在 `QOpenGLContext::aboutToBeDestroyed` 的 direct 连接中手动 `destroy()`，或把纹理对象的生命周期限制在渲染对象拥有的 context 生命周期内。不要指望程序退出时任意析构顺序都能安全释放 GPU 资源。

## API 速查表

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造 | `QOpenGLTexture(Target target)` | 创建指定目标类型的纹理包装对象。 | target 之后不能像普通参数那样切换。 |
| 构造 | `QOpenGLTexture(const QImage &image, MipMapGeneration genMipMaps = GenerateMipMaps)` | 从 `QImage` 创建普通 2D 纹理并上传数据。 | 需要 current context；复杂格式或 array/cube map 不适合这个便利构造。 |
| 析构 | `~QOpenGLTexture()` | 销毁 C++ 包装对象并释放纹理资源。 | 析构时最好仍有兼容 context current；否则显式 `destroy()` 更可控。 |
| 目标 | `Target target() const` | 返回纹理目标。 | 决定后续所有上传、绑定和采样语义。 |
| 创建 | `bool create()` | 创建底层 OpenGL texture name。 | 需要 current context；失败后检查 context 和 OpenGL 支持。 |
| 销毁 | `void destroy()` | 删除底层 texture object。 | 在创建它的共享组中调用最安全。 |
| 创建状态 | `bool isCreated() const` | 查询是否已有 OpenGL texture name。 | 不等于已经分配存储或上传数据。 |
| 纹理名 | `GLuint textureId() const` | 返回 OpenGL texture id。 | 只在与 Qt 管理配合时借用；不要手动 `glDeleteTextures`。 |
| 绑定 | `void bind()` | 绑定到当前 active texture unit。 | 依赖 OpenGL 全局状态，调用前确认 active unit。 |
| 绑定 | `void bind(uint unit, TextureUnitReset reset = DontResetTextureUnit)` | 绑定到指定纹理单元。 | `reset` 决定是否恢复之前 active unit。 |
| 解绑 | `void release()` | 从当前目标解绑。 | 影响当前 active unit 的 OpenGL 状态。 |
| 解绑 | `void release(uint unit, TextureUnitReset reset = DontResetTextureUnit)` | 从指定纹理单元解绑。 | 跨渲染模块时要明确纹理单元管理策略。 |
| 绑定状态 | `bool isBound() const` / `bool isBound(uint unit)` | 查询当前或指定单元是否绑定。 | 只是即时 OpenGL 状态，不适合作为长期同步依据。 |
| 绑定查询 | `static GLuint boundTextureId(BindingTarget target)` | 查询当前单元某 target 绑定的纹理 id。 | 直接读取 OpenGL 状态，调试和互操作时有用。 |
| 绑定查询 | `static GLuint boundTextureId(uint unit, BindingTarget target)` | 查询指定单元的绑定纹理 id。 | 注意 unit 和 target 必须匹配。 |
| 存储描述 | `void setFormat(TextureFormat format)` / `TextureFormat format() const` | 设置或查询 GPU 内部格式。 | 必须在存储分配前设置；影响显存格式和采样类型。 |
| 存储描述 | `void setSize(int width, int height = 1, int depth = 1)` | 设置纹理尺寸。 | 1D/2D/3D 目标解释不同；分配后改变无效或需重建。 |
| 尺寸查询 | `width()` / `height()` / `depth()` | 查询配置的尺寸。 | 对 array/cube map 不包含 layer/face 含义。 |
| mipmap | `void setMipLevels(int levels)` / `int mipLevels() const` | 设置或查询 mip 层数。 | 使用 mipmap filter 前要有完整可用层。 |
| mipmap | `int maximumMipLevels() const` | 返回当前尺寸可支持的最大 mip 层数。 | 适合自动决定 `setMipLevels()`。 |
| array | `void setLayers(int layers)` / `int layers() const` | 设置或查询 array layer 数。 | 只对 array/cube map array 等目标有意义。 |
| cube | `int faces() const` | 返回 face 数。 | cube map 通常是 6。 |
| 多采样 | `void setSamples(int samples)` / `int samples() const` | 设置或查询 MSAA 样本数。 | 只适合 multisample 目标；分配前设置。 |
| 多采样 | `void setFixedSamplePositions(bool)` / `bool isFixedSamplePositions() const` | 控制多采样位置是否固定。 | 影响 multisample 存储创建。 |
| 存储分配 | `void allocateStorage()` | 按当前描述分配 GPU 存储。 | 分配后结构性描述基本固定。 |
| 存储分配 | `void allocateStorage(PixelFormat, PixelType)` | 用上传格式提示来分配存储。 | 仍不等于上传数据，只是帮助选择兼容存储。 |
| 存储状态 | `bool isStorageAllocated() const` | 查询是否已分配纹理存储。 | 不表示内容完整或采样状态正确。 |
| 数据上传 | `setData(...)` 系列 | 上传整张、某一层、某一 mip、某个 cube face 或子区域数据。 | CPU 数据格式由 `PixelFormat`/`PixelType` 决定；注意 row alignment 和像素传输选项。 |
| 图像上传 | `void setData(const QImage &, MipMapGeneration = GenerateMipMaps)` | 上传 QImage。 | 会做图像格式转换；高频路径要评估成本。 |
| 能力 | `static bool hasFeature(Feature feature)` | 查询当前平台是否支持某类纹理能力。 | 对 array、3D、rectangle、view、anisotropic 等特性先查再用。 |
| 纹理视图 | `createTextureView(...)` / `isTextureView()` | 基于已有存储创建 view。 | 依赖 texture view 特性；format class 必须兼容。 |
| mip 范围 | `setMipBaseLevel()` / `setMipMaxLevel()` / `setMipLevelRange()` | 限制采样可见的 mip 层范围。 | OpenGL ES 2 构建中不可依赖这些能力。 |
| mip 生成 | `setAutoMipMapGenerationEnabled()` / `isAutoMipMapGenerationEnabled()` | 控制数据更新后是否自动生成 mipmap。 | 高频更新纹理时自动生成可能很贵。 |
| mip 生成 | `generateMipMaps()` / `generateMipMaps(int baseLevel, bool resetBaseLevel = true)` | 立即生成 mipmap。 | level 0 必须有有效内容。 |
| swizzle | `setSwizzleMask()` / `swizzleMask()` | 调整采样时通道映射。 | 常用于单通道纹理映射到 RGBA。 |
| 深度模板 | `setDepthStencilMode()` / `depthStencilMode()` | 选择 depth/stencil 纹理采样分量。 | 只对深度模板格式有意义。 |
| 深度比较 | `setComparisonMode()` / `comparisonMode()` | 设置普通采样还是参考值比较。 | shadow sampler 通常需要 `CompareRefToTexture`。 |
| 比较函数 | `setComparisonFunction()` / `comparisonFunction()` | 设置深度比较函数。 | 与 shader sampler 类型和纹理格式配套。 |
| 过滤 | `setMinificationFilter()` / `minificationFilter()` | 设置缩小时采样过滤。 | mipmap filter 要求 mip 链完整。 |
| 过滤 | `setMagnificationFilter()` / `magnificationFilter()` | 设置放大时采样过滤。 | 放大过滤只支持 nearest/linear 语义。 |
| 过滤 | `setMinMagFilters()` / `minMagFilters()` | 一次设置或读取 min/mag filter。 | 保持两个方向策略一致时更清晰。 |
| 各向异性 | `setMaximumAnisotropy()` / `maximumAnisotropy()` | 设置各向异性过滤强度。 | 先确认 `AnisotropicFiltering` 特性。 |
| wrap | `setWrapMode(WrapMode)` | 设置所有方向 wrap 模式。 | `Repeat` 对旧 NPOT 或 rectangle texture 可能受限。 |
| wrap | `setWrapMode(CoordinateDirection, WrapMode)` / `wrapMode()` | 单独设置 S/T/R 方向 wrap。 | 3D 和 cube map 要分别考虑方向。 |
| 边框色 | `setBorderColor()` / `borderColor()` | 设置或读取 clamp-to-border 使用的边框颜色。 | 不同类型重载对应 float/int/uint 颜色。 |
| LOD | `setMinimumLevelOfDetail()` / `setMaximumLevelOfDetail()` | 限制可采样的 LOD 范围。 | 主要用于细调 mipmap 选择。 |
| LOD | `setLevelOfDetailRange()` / `levelOfDetailRange()` | 一次设置或查询 LOD 范围。 | 与 mip level range 不是同一层概念。 |
| LOD | `setLevelofDetailBias()` / `levelofDetailBias()` | 设置 mip 选择偏移。 | 注意函数名中的 `of` 小写拼写。 |
| 枚举 | `Target` / `BindingTarget` | 描述纹理目标和对应绑定查询目标。 | target 是对象结构；binding target 用于查询 OpenGL 状态。 |
| 枚举 | `TextureFormat` | 描述 GPU 内部格式。 | 包含 normalized、integer、float、packed、depth/stencil、compressed、sRGB、ES2 格式。 |
| 枚举 | `PixelFormat` / `PixelType` | 描述 CPU 上传数据布局。 | 与内部格式相关但不是同一个概念。 |
| 枚举 | `Filter` / `WrapMode` | 描述采样过滤和坐标越界策略。 | 采样器状态会影响 shader 最终读到的值。 |
| 枚举 | `Feature` / `Features` | 描述运行环境支持的纹理能力。 | 不能只凭桌面 OpenGL 经验假设移动端也支持。 |

## 一句话总结

`QOpenGLTexture` 是 OpenGL 纹理资源的 Qt 包装：在分配前把结构说清楚，在 current context 中上传和绑定，并在 context 还活着时释放。
