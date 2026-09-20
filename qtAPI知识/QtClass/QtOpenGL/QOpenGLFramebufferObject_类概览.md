# QOpenGLFramebufferObject 类笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QOpenGLFramebufferObject>`  
> 所属模块：`Qt6::OpenGL`  
> 类型：离屏渲染目标（FBO）

## 它解决什么问题

默认 framebuffer 是窗口系统提供的最终显示目标。很多渲染流程需要先把内容画到屏幕外：后处理、阴影贴图、反射、缩略图、GPU 生成纹理、或让 `QPainter` 与原生 OpenGL 混合绘制。`QOpenGLFramebufferObject`（FBO）封装了一个 OpenGL framebuffer object 及其颜色、深度和模板附件。

它让一块离屏渲染表面可以：

- `bind()` 成为当前绘制目标；
- 以纹理形式被后续 pass 采样；
- 具备可选 depth/stencil 附件；
- 添加多个 color attachment，构成 MRT（multiple render targets）；
- 与另一个 FBO 或默认 framebuffer 进行 blit；
- 读回为 `QImage`，用于截图、离线保存或 CPU 后处理。

FBO 是 GPU 资源，不是纯配置对象。构造时就需要 current OpenGL context，最终有效性也取决于该 context 及共享 context 的生命周期。

## 实际使用场景

### 后处理

先绑定 FBO，绘制场景；再回到默认 framebuffer，把 FBO 的颜色纹理绑定到全屏三角形/四边形并执行 blur、tonemap、FXAA 等 shader。

### 阴影贴图或反射贴图

FBO 的颜色附件可作为后续 shader 的纹理输入。若是深度相关渲染，要按实际目标选择合适的 depth/stencil attachment 和 internal format。

### `QPainter` 绘制到 OpenGL 纹理

将 FBO 与 `QOpenGLPaintDevice` 配合，能把 Qt 的 `QPainter` 输出写进纹理。此类场景通常要求 `CombinedDepthStencil`，否则 depth/stencil 相关行为会不完整。

### 多渲染目标

使用 `addColorAttachment()` 添加 `GL_COLOR_ATTACHMENT1`、`2` 等，由 shader 的多个 fragment output 同时写入不同附件。

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
format.setInternalTextureFormat(GL_RGBA8);

// 必须在有 current QOpenGLContext 时构造。
QOpenGLFramebufferObject fbo(QSize(1024, 1024), format);
if (!fbo.isValid()) {
    // 当前驱动或附件组合不受支持，不能继续渲染。
    return;
}

if (!fbo.bind())
    return;

// 在此执行 OpenGL 绘制。

fbo.release();  // 回到默认 framebuffer。
const GLuint colorTexture = fbo.texture();
```

对于需要 multisample anti-aliasing 的 FBO，应设置 format 的 `samples > 0`。此时颜色附件是 renderbuffer，而不是可直接采样的 texture；需要先 blit 到普通 FBO。

## 核心模型：FBO、附件和纹理

普通单采样 FBO 默认创建一个 `GL_TEXTURE_2D` 颜色纹理，并附着到 `GL_COLOR_ATTACHMENT0`。该纹理 ID 由 `texture()` 返回，可在后续 OpenGL 代码中按普通纹理绑定。

多重采样 FBO 使用 color renderbuffer。它可作为渲染目标，却不能直接作为普通纹理采样。因此常见工作流为：

1. 渲染到 multisample FBO；
2. `blitFramebuffer()` 解析/复制到单采样 FBO；
3. 使用单采样 FBO 的 `texture()` 作为后处理输入。

调用 `addColorAttachment()` 可以设置多个颜色输出。所有 color attachment 尺寸最好一致；文档允许不同尺寸，但实际渲染区域会被限制到所有附件共同覆盖的范围，且部分驱动处理不一致尺寸时并不可靠。

## context 与生命周期边界

### 构造时必须有 current context

构造函数会创建 OpenGL server 资源。没有 current context 时初始化失败，`isValid()` 返回 `false`。

### context 销毁会使 FBO 失效

如果创建 FBO 的 `QOpenGLContext` 被销毁，并且没有可接管资源的共享 context，FBO 会失效。GUI 销毁、渲染线程退出、或手动管理 context 时，必须让 FBO 的生命周期落在合适范围内。

### FBO 不可拷贝

与底层资源一一对应，`QOpenGLFramebufferObject` 禁止拷贝。需要共享使用时传递指针/引用，或明确由某个渲染资源管理对象持有。

### `handle()` 不是所有权转移

`handle()` 返回 FBO 的 OpenGL ID，供高级代码附加自定义图像/缓冲。拿到 ID 后自行附加的资源由调用方负责清理；Qt 只管理它自己创建和已知的附件。

## 附件和恢复策略

### `Attachment`

| 取值 | 含义 | 使用边界 |
| --- | --- | --- |
| `NoAttachment` | 没有 depth/stencil 附件。 | depth/stencil 测试无法正常工作；默认值。 |
| `CombinedDepthStencil` | 优先添加打包 depth + stencil；缺少相应扩展时退化为仅 depth。 | 与 `QPainter` 配合时通常应选它。 |
| `Depth` | 只添加 depth。 | 不需要 stencil 时使用。 |

`setAttachment()` 可在已有 FBO 上释放或重新附加 depth/stencil，但它会改变当前 framebuffer 绑定状态；调用后应重新确认调用方依赖的绑定。

### `FramebufferRestorePolicy`

| 取值 | `blitFramebuffer()` 返回前的绑定行为 |
| --- | --- |
| `DontRestoreFramebufferBinding` | 不恢复，调用方自行跟踪绑定状态；额外查询最少。 |
| `RestoreFramebufferBindingToDefault` | 绑定默认 framebuffer。 |
| `RestoreFrameBufferBinding` | 恢复调用前绑定的 FBO；需要查询当前状态，某些驱动上可能造成 pipeline stall。 |

性能敏感绘制路径通常可以自行管理 binding，选 `DontRestoreFramebufferBinding`；只有需要封装调用并保留外部状态时才付出恢复成本。

## 关键 API 语义与边界

### `bind()` / `release()` / `bindDefault()`

`bind()` 将 FBO 设为当前绘制目标。`release()` 与静态 `bindDefault()` 切回窗口系统的默认 framebuffer。三者均返回 `bool`，失败时不能继续假设绑定已切换。

`isBound()` 只检查此 FBO 是否正绑定到**当前 context**，它不是跨线程或跨 context 的资源可用性检查。

### `texture()`、`textures()` 与 `takeTexture()`

`texture()` 返回默认 color attachment 的 texture ID；使用多附件时返回第一个。`textures()` 返回所有颜色纹理。

多重采样 FBO 不含普通颜色纹理，`texture()` 返回值无效，`textures()` 返回空列表。

`takeTexture()` 的含义是**所有权转移**：

- 先返回颜色纹理 ID；
- 若 FBO 正绑定，会隐式 `release()`；
- 后续再次 `bind()` 时，Qt 会为 FBO 新建颜色纹理；
- 调用方必须最终通过 OpenGL 删除接管到的纹理；
- multisample 或不完整 FBO 无有效纹理时返回 `0`。

不要在 `takeTexture()` 后还认为该 ID 会随 FBO 析构自动删除。

### `toImage()`

将指定颜色附件读回为 `QImage`。默认 `flipped = true`，把 OpenGL 原点方向翻转为通常的 raster 坐标。

单采样 FBO 的读回依赖 `glReadPixels`，这是可能导致同步和性能下降的 GPU -> CPU 操作，不应放在每帧主循环中。多重采样 FBO 读回依赖 framebuffer blit 扩展；缺少支持时结果未定义。

返回图像通常为 premultiplied ARGB32/RGB32，特定 internal format 可能产生其它 Qt 图像格式。若原始渲染数据不是预乘 alpha，保存或处理前需按实际 alpha 语义处理，避免错误非预乘。

### `blitFramebuffer()`

在 source rect 和 target rect 之间复制/缩放 framebuffer 内容。`source` 或 `target` 为 `nullptr` 时表示默认 framebuffer。

- `buffers` 一般是 `GL_COLOR_BUFFER_BIT`，也可包含 depth/stencil 位；
- `filter` 常用 `GL_NEAREST`；不是任意附件/缓冲组合都适合线性过滤；
- 启用了 scissor test 时，blit 区域会被裁剪；
- 多附件时，用 `readColorAttachmentIndex` 和 `drawColorAttachmentIndex` 明确源/目标颜色附件；
- 调用前可用 `hasOpenGLFramebufferBlit()` 检查能力。

## 常见误区

### 认为多重采样 FBO 能直接作为纹理

不能。多重采样颜色附件是 renderbuffer。必须 resolve/blit 到普通单采样 FBO 后，才能拿到可采样的 texture。

### 每帧调用 `toImage()`

这会频繁触发 readback，常导致 GPU pipeline stall。截图、诊断或离线导出才适合使用。

### 用 `NoAttachment` 却启用 depth/stencil 测试

此时测试没有相应附着缓冲，渲染结果通常不符合预期。需要 depth 时选 `Depth` 或 `CombinedDepthStencil`。

### `takeTexture()` 后忘记删除纹理

调用后 texture ownership 已转移；FBO 不再管理这个 ID。

## 逐项 API 说明

### 构造与销毁

#### `QOpenGLFramebufferObject(const QSize &size, GLenum target = GL_TEXTURE_2D)`

构造单采样 FBO，并创建尺寸为 `size` 的颜色纹理。默认没有 depth/stencil，desktop OpenGL 默认 internal format 为 `GL_RGBA8`，OpenGL ES 为 `GL_RGBA`。需要 current context。

#### `QOpenGLFramebufferObject(int width, int height, GLenum target = GL_TEXTURE_2D)`

与 `QSize` 重载语义相同。

#### `QOpenGLFramebufferObject(const QSize &size, Attachment attachment, GLenum target = GL_TEXTURE_2D, GLenum internalFormat = 0)`

构造并指定 depth/stencil attachment、texture target 和 internal format。`internalFormat == 0` 表示采用平台默认值。

#### `QOpenGLFramebufferObject(int width, int height, Attachment attachment, GLenum target = GL_TEXTURE_2D, GLenum internalFormat = 0)`

与上一个构造函数语义相同，使用宽高参数。

#### `QOpenGLFramebufferObject(const QSize &size, const QOpenGLFramebufferObjectFormat &format)`

根据 `format` 请求创建 FBO。驱动可能降级不支持的 samples/attachment；创建后用 `format()` 检查实际格式。

#### `QOpenGLFramebufferObject(int width, int height, const QOpenGLFramebufferObjectFormat &format)`

与 `QSize` 版相同。

#### `virtual ~QOpenGLFramebufferObject()`

销毁 FBO 及 Qt 所管理的附件资源。销毁时 context 生命周期必须仍合理；不要留下外部代码继续使用 `handle()`、`texture()` 返回的资源。

### 附件、绑定与查询

#### `void addColorAttachment(const QSize &size, GLenum internalFormat = 0)`

添加新的 color attachment，从 `GL_COLOR_ATTACHMENT1` 起递增。多采样 FBO 添加 renderbuffer，普通 FBO 添加 texture；尺寸/格式需与渲染路径兼容。

#### `void addColorAttachment(int width, int height, GLenum internalFormat = 0)`

与 `QSize` 重载相同。

#### `Attachment attachment() const`

返回当前 depth/stencil 附件配置。

#### `void setAttachment(Attachment attachment)`

释放或重新附加 depth/stencil。会改变当前 framebuffer binding。

#### `bool bind()`

将此 FBO 绑定为当前绘制目标。失败时不可继续假定输出写入该 FBO。

#### `bool release()`

切回默认、窗口系统提供的 framebuffer。

#### `static bool bindDefault()`

不依赖具体对象地绑定默认 framebuffer，常用于恢复窗口输出目标。

#### `bool isBound() const`

检查此 FBO 是否当前绑定在 current context。

#### `bool isValid() const`

检查 FBO 是否完整有效。创建失败、附件不完整、context 销毁且无共享 context 接管等情况下返回 `false`。

#### `QOpenGLFramebufferObjectFormat format() const`

返回实际创建出的格式。尤其要用它验证 samples、附件和 internal format 是否被驱动降级。

#### `GLuint handle() const`

返回 OpenGL FBO ID。可用于高级附件操作；调用方对自行增加的资源负责。

#### `QSize size() const` / `int width() const` / `int height() const`

返回主附件尺寸。

#### `QList<QSize> sizes() const`

返回全部颜色附件尺寸，用于多渲染目标检查。

### 纹理与读回

#### `GLuint texture() const`

返回默认颜色纹理 ID。多重采样 FBO 上无效；多附件时是第一个纹理。

#### `QList<GLuint> textures() const`

返回全部颜色纹理 ID。多重采样 FBO 返回空列表。

#### `GLuint takeTexture()`

转移第一个颜色纹理的所有权；无纹理/不完整 FBO 时返回 `0`。调用方负责删除该纹理。

#### `GLuint takeTexture(int colorAttachmentIndex)`

转移指定颜色附件的 texture ownership。索引 0 与无参版本等效。

#### `QImage toImage(bool flipped = true) const`

读回第一个颜色附件。`flipped` 用于在 OpenGL 与 Qt raster 坐标之间转换；操作可能昂贵。

#### `QImage toImage(bool flipped, int colorAttachmentIndex) const`

读回指定颜色附件。只有实现支持 MRT 时多附件读取才完整可用。

### 静态能力与 blit

#### `static bool hasOpenGLFramebufferObjects()`

查询系统是否支持 framebuffer object 能力。

#### `static bool hasOpenGLFramebufferBlit()`

查询系统是否支持 framebuffer blit 能力。

#### `static void blitFramebuffer(...)`

四个重载用于从 source 复制到 target。最完整重载可指定矩形、缓冲位、滤镜、源/目标 color attachment 索引及 framebuffer 绑定恢复策略；简化重载用于全尺寸颜色复制或使用默认恢复行为。

## API 速查表

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 类型 | `Attachment` | 选择 depth/stencil 附件。 | `NoAttachment` 无 depth/stencil；`QPainter` 通常需要 `CombinedDepthStencil`。 |
| 类型 | `FramebufferRestorePolicy` | 决定 blit 后绑定状态如何处理。 | 恢复原绑定可能查询 GL 状态并造成性能成本。 |
| 构造 | 6 个 `QOpenGLFramebufferObject(...)` 重载 | 在 current context 中创建离屏渲染目标。 | 无 current context 会失败；format 请求可能被驱动降级。 |
| 生命周期 | `~QOpenGLFramebufferObject()` | 释放 Qt 管理的 FBO/附件资源。 | context 销毁后资源可能已经失效。 |
| 附件 | `addColorAttachment()` 两个重载 | 增加 MRT 颜色输出。 | 尺寸不同会限制有效绘制区域；需驱动支持。 |
| 附件 | `attachment()` / `setAttachment()` | 查询或调整 depth/stencil。 | `setAttachment()` 改变当前 binding。 |
| 绑定 | `bind()` / `release()` / `bindDefault()` | 切换 FBO 与默认 framebuffer。 | 检查返回值；绑定状态属于 current context。 |
| 状态 | `isBound()` / `isValid()` | 查询绑定或完整性。 | 有效性受附件、context 与共享关系影响。 |
| 查询 | `format()` | 获取实际 FBO 格式。 | 用它确认 samples/attachment/format 是否真的被兑现。 |
| 查询 | `handle()` | 获取底层 FBO ID。 | 自行附加的外部资源由调用方删除。 |
| 查询 | `size()` / `width()` / `height()` / `sizes()` | 查询主附件或各颜色附件尺寸。 | MRT 时关注附件尺寸是否一致。 |
| 纹理 | `texture()` / `textures()` | 获取颜色纹理 ID。 | 多重采样 FBO 不提供可直接采样的 texture。 |
| 所有权 | `takeTexture()` 两个重载 | 转移颜色纹理所有权。 | 返回后调用方必须删除纹理；无有效纹理时为 `0`。 |
| 读回 | `toImage()` 两个重载 | 将颜色附件读回为 `QImage`。 | GPU->CPU readback 昂贵；默认会翻转图像。 |
| 能力 | `hasOpenGLFramebufferObjects()` | 检查 FBO 支持。 | 在创建依赖能力的资源前检查。 |
| 能力 | `hasOpenGLFramebufferBlit()` | 检查 blit 支持。 | 多重采样 resolve、`toImage()` 可能依赖它。 |
| 复制 | `blitFramebuffer()` 4 个重载 | 在 FBO/default framebuffer 间复制或 resolve。 | 留意 scissor、附件索引、filter 和恢复策略。 |

### 一句话总结

`QOpenGLFramebufferObject` 把离屏 GPU 渲染目标包装为可绑定、可采样、可多附件和可读回的对象；真正要盯住的是 current context、单采样/多重采样差异、binding 状态与纹理所有权转移。
