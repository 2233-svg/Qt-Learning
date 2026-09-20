# QOpenGLFramebufferObjectFormat 类笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QOpenGLFramebufferObjectFormat>`  
> 所属模块：`Qt6::OpenGL`  
> 类型：FBO 创建参数的值类型

## 它解决什么问题

离屏 framebuffer 不只需要宽高。是否开启多重采样、要不要 depth/stencil、颜色附件用什么 internal format、纹理 target 是什么，都会影响内存占用、可采样性和驱动兼容性。

`QOpenGLFramebufferObjectFormat` 是创建 `QOpenGLFramebufferObject` 前用于收集这些要求的轻量值对象。它自身不创建任何 OpenGL 资源，也不要求 current context；真正创建 FBO 时才会由驱动决定哪些要求能够兑现。

它控制四类参数：

- 每像素采样数 `samples`；
- depth/stencil 附件 `attachment`；
- 颜色附件的纹理 target；
- 颜色纹理或多重采样颜色 renderbuffer 的 internal format；
- 是否为单采样颜色纹理分配 mipmap 层级。

## 实际使用场景

### 创建带 depth/stencil 的离屏画布

希望使用 depth test、stencil test 或让 `QPainter` 正常渲染时，先设置 `CombinedDepthStencil`，再把 format 传给 FBO 构造函数。

### 创建 MSAA 离屏渲染目标

设置大于 0 的 `samples`。得到的 FBO 不能直接以普通纹理采样，通常应 resolve 到单采样 FBO。

### 选择高精度或特殊颜色格式

通过 `setInternalTextureFormat()` 请求例如 `GL_RGBA16F`、`GL_RGB10_A2` 等内部格式，用于 HDR、中间缓冲或特定输出格式。实际支持情况必须在 FBO 创建后验证。

## 构建与最小示例

```cmake
find_package(Qt6 REQUIRED COMPONENTS OpenGL)
target_link_libraries(mytarget PRIVATE Qt6::OpenGL)
```

```cpp
#include <QOpenGLFramebufferObject>
#include <QOpenGLFramebufferObjectFormat>

QOpenGLFramebufferObjectFormat format;
format.setAttachment(QOpenGLFramebufferObject::CombinedDepthStencil);
format.setSamples(4);
format.setInternalTextureFormat(GL_RGBA8);

// 这里才需要 current OpenGL context。
QOpenGLFramebufferObject fbo(QSize(1280, 720), format);
if (!fbo.isValid())
    return;

const QOpenGLFramebufferObjectFormat actual = fbo.format();
qDebug() << "requested samples:" << format.samples()
         << "actual samples:" << actual.samples();
```

## 默认值

默认 `QOpenGLFramebufferObjectFormat` 表示：

- `samples() == 0`，即非多重采样；
- `attachment() == QOpenGLFramebufferObject::NoAttachment`；
- `textureTarget() == GL_TEXTURE_2D`；
- desktop OpenGL 下 internal format 为 `GL_RGBA8`；
- OpenGL ES 下 internal format 为 `GL_RGBA`；
- mipmapping 关闭。

默认格式适合最简单的颜色离屏纹理，但不适合依赖 depth/stencil 的渲染，也不提供抗锯齿。

## 请求与实际格式不是一回事

format 是请求，不是强制配置。驱动可能不支持某个 samples 数、attachment 组合或颜色格式。Qt 文档建议在构造 FBO 后调用 `QOpenGLFramebufferObject::format()`，以检查实际使用的格式。

尤其要注意：

- `setSamples(n)` 请求的 n 若不支持，驱动可能使用可支持的最大值；
- `samples > 0` 需要 framebuffer multisample 支持；
- 多重采样 FBO 不能作为普通 texture 直接绑定采样；
- `setTextureTarget()` 对多重采样 FBO 会被忽略；
- `setMipmap(true)` 不能用于多重采样 FBO。

## 各参数之间的关系

### samples 与纹理可采样性

`samples == 0` 时，颜色附件通常是 texture，能通过 `QOpenGLFramebufferObject::texture()` 取出并采样。

`samples > 0` 时，颜色附件是 multisample renderbuffer。它改善边缘抗锯齿，但不能直接作为常规 texture 使用，需要 blit/resolve 到单采样 FBO。

### mipmap 与 samples

启用 mipmap 会为颜色纹理分配额外层级，增加显存。内容变化后，调用方需绑定该纹理并调用 `glGenerateMipmap()` 更新层级。多重采样 FBO 不支持 mipmapping。

### attachment

`NoAttachment` 不提供 depth/stencil；`Depth` 提供深度；`CombinedDepthStencil` 尽量同时提供深度和模板。是否能够满足打包 depth/stencil 取决于环境能力。

### texture target

`setTextureTarget()` 用于指定普通 FBO 颜色纹理的 target，默认是 `GL_TEXTURE_2D`。多重采样场景下没有普通颜色纹理，因此该参数会被忽略。

## 值语义和比较

format 是可复制的值类型。复制、赋值和比较只处理配置参数，不会复制或操作任何 GPU 资源。

`operator==` 只有在所有 options 都相同才返回 `true`；`operator!=` 是其反面。适合用来判断“请求是否改变”，但不能据此推断驱动最后创建出的实际 FBO 是否等价。

## 逐项 API 说明

### 构造、复制和销毁

#### `QOpenGLFramebufferObjectFormat::QOpenGLFramebufferObjectFormat()`

创建默认 FBO 配置：无 multisample、无 depth/stencil、`GL_TEXTURE_2D`、desktop 为 `GL_RGBA8`、OpenGL ES 为 `GL_RGBA`，且不启用 mipmap。

#### `QOpenGLFramebufferObjectFormat::QOpenGLFramebufferObjectFormat(const QOpenGLFramebufferObjectFormat &other)`

复制 `other` 的全部配置，不涉及 GPU 资源。

#### `QOpenGLFramebufferObjectFormat::~QOpenGLFramebufferObjectFormat() noexcept`

销毁值对象，不会销毁已经由它创建出来的 FBO。

#### `QOpenGLFramebufferObjectFormat &operator=(const QOpenGLFramebufferObjectFormat &other)`

复制赋值全部配置。

#### `bool operator==(const QOpenGLFramebufferObjectFormat &other) const`

所有 format 选项都相同时返回 `true`。

#### `bool operator!=(const QOpenGLFramebufferObjectFormat &other) const`

任一选项不同时返回 `true`。

### 多重采样

#### `void setSamples(int samples)`

请求每像素 sample 数。`0` 表示常规单采样 FBO；大于 0 请求 multisample FBO。

不支持请求值时，硬件可能使用可用最大 sample 数。创建后应通过 `fbo.format().samples()` 确认实际值。

#### `int samples() const`

返回请求的 sample 数；对实际 FBO 格式则返回实际 sample 数。`0` 表示非多重采样。

### Mipmap

#### `void setMipmap(bool enabled)`

启用或关闭颜色纹理的 mipmap 分配。默认关闭；启用会增加内存。生成/更新 mipmap 内容需要调用方执行相应 OpenGL 操作。

多重采样 FBO 不支持 mipmap，不能把这个开关与 `samples > 0` 组合为可用功能。

#### `bool mipmap() const`

返回是否请求 mipmap。

### Depth/stencil 附件

#### `void setAttachment(QOpenGLFramebufferObject::Attachment attachment)`

设置创建 FBO 时的 depth/stencil 需求：无附件、仅 depth 或组合 depth/stencil。

#### `QOpenGLFramebufferObject::Attachment attachment() const`

返回配置中的 attachment，默认 `NoAttachment`。

### 纹理 target 与颜色格式

#### `void setTextureTarget(GLenum target)`

设置普通 FBO 颜色纹理的 OpenGL target。多重采样 FBO 中该设置被忽略。

#### `GLenum textureTarget() const`

返回请求的颜色纹理 target，默认 `GL_TEXTURE_2D`。多重采样情况下返回值不代表实际 renderbuffer。

#### `void setInternalTextureFormat(GLenum internalTextureFormat)`

设置颜色纹理，或多重采样颜色 renderbuffer 的 internal format。选择必须与后续 shader、readback 和平台能力兼容。

#### `GLenum internalTextureFormat() const`

返回请求的 internal format；默认 desktop 为 `GL_RGBA8`，OpenGL ES 为 `GL_RGBA`。

## 常见误区

### 把 format 的 samples 当作最终值

它是请求。必须查看 `fbo.format().samples()`，特别是在不同显卡和远程桌面/OpenGL ES 环境中。

### 同时开启 samples 和 mipmap 并期望纹理可采样

多重采样 FBO 不提供可直接采样的普通 texture，也不支持 mipmap。应使用两个 FBO：一个 MSAA 渲染目标，一个单采样纹理目标。

### 忘记设置 depth/stencil

默认 `NoAttachment`。如果渲染路径启用 depth test 或 stencil test，必须显式选择适当 attachment。

### 只修改 format，却试图改变已创建 FBO

`QOpenGLFramebufferObjectFormat` 是创建参数。修改它不会重新配置已经创建的 FBO；需要按新 format 创建新 FBO，或使用 FBO 的有限运行时附件接口。

## API 速查表

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造 | `QOpenGLFramebufferObjectFormat()` | 创建默认 FBO 请求。 | 默认无 depth/stencil、无 MSAA、无 mipmap。 |
| 值语义 | 拷贝构造、析构、`operator=` | 复制或销毁配置值。 | 不操作 GPU 资源。 |
| 比较 | `operator==` / `operator!=` | 比较全部请求选项。 | 相等不代表驱动实际创建结果一定相同。 |
| MSAA | `setSamples(int)` | 请求每像素 sample 数。 | `0` 是单采样；驱动可降级，创建后检查 `fbo.format()`。 |
| MSAA | `samples()` | 读取请求/实际 sample 数。 | 多重采样 FBO 不能直接采样为 texture。 |
| Mipmap | `setMipmap(bool)` | 为单采样颜色纹理请求 mipmap。 | 增加显存；内容更新后需生成 mipmap；MSAA 不支持。 |
| Mipmap | `mipmap()` | 查询 mipmap 请求。 | 仅描述 format，不代表已生成 mipmap 内容。 |
| 附件 | `setAttachment(Attachment)` | 请求 depth/stencil 配置。 | 默认无附件；`QPainter` 场景通常选组合附件。 |
| 附件 | `attachment()` | 查询附件请求。 | 创建后从 `fbo.format()` 确认实际结果。 |
| 目标 | `setTextureTarget(GLenum)` | 设置普通 FBO 颜色纹理 target。 | 对 MSAA FBO 忽略。 |
| 目标 | `textureTarget()` | 查询请求 target。 | 默认 `GL_TEXTURE_2D`；MSAA 下不代表实际附件。 |
| 格式 | `setInternalTextureFormat(GLenum)` | 请求颜色 texture/renderbuffer 内部格式。 | 平台支持不同；创建后核验实际 format。 |
| 格式 | `internalTextureFormat()` | 查询请求的内部格式。 | 默认 desktop `GL_RGBA8`、ES `GL_RGBA`。 |

### 一句话总结

`QOpenGLFramebufferObjectFormat` 是创建 FBO 前的配置请求：它决定 samples、附件、target、颜色格式和 mipmap，但最终必须从实际创建出的 `QOpenGLFramebufferObject::format()` 确认驱动支持结果。
