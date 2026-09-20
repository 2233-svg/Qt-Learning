# QOpenGLFunctions_4_5_Core 类笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QOpenGLFunctions_4_5_Core>`  
> 所属模块：`Qt6::OpenGL`  
> 继承：`QAbstractOpenGLFunctions`  
> 可用性：桌面 OpenGL 4.5 Core profile；不包含 Compatibility/fixed-function API

## 它解决什么问题

`QOpenGLFunctions_4_5_Core` 是 Qt 对 OpenGL 4.5 Core profile 的函数包装。4.5 的核心价值是 Direct State Access：大量对象可以被“按名字直接操作”，不必先绑定到全局 target 再修改。它同时引入 clip control、robustness 风格的 bounded readback、texture barrier，以及更多 create/get/named object API。

这解决了传统 OpenGL 大型代码库最痛的隐式状态问题：纹理、buffer、FBO、VAO、renderbuffer、transform feedback 可以在资源系统中直接创建和配置，减少“当前绑定了谁”导致的错误。它适合成熟 Core renderer，而不是简单渲染示例。

## 实际使用场景

- 资源管理器用 `glCreateBuffers()`、`glNamedBufferStorage()`、`glCreateTextures()`、`glTextureStorage*()` 创建对象，不污染全局绑定；
- FBO builder 用 `glCreateFramebuffers()`、`glNamedFramebufferTexture()`、`glCheckNamedFramebufferStatus()` 直接配置离屏目标；
- VAO layout 系统用 `glCreateVertexArrays()` 和 `glVertexArray*()` 系列直接写指定 VAO；
- 使用 `glClipControl()` 统一 NDC 深度范围和 framebuffer 原点，以适配 Vulkan/D3D 风格坐标；
- 用 `glReadnPixels()`、`glGetnTexImage()` 等限定输出缓冲大小，降低越界风险。

## 初始化与最小示例

```cpp
#include <QOpenGLFunctions_4_5_Core>

QOpenGLFunctions_4_5_Core gl;

bool createTexture(int width, int height)
{
    if (!gl.initializeOpenGLFunctions())
        return false;

    GLuint texture = 0;
    gl.glCreateTextures(GL_TEXTURE_2D, 1, &texture);
    gl.glTextureStorage2D(texture, 1, GL_RGBA8, width, height);
    gl.glTextureParameteri(texture, GL_TEXTURE_MIN_FILTER, GL_LINEAR);
    gl.glBindTextureUnit(0, texture);
    return true;
}
```

DSA 让创建和配置更直接，但不改变对象生命周期、context 共享组和同步规则。对象仍必须在有效 context 中创建、使用和销毁。

## 4.5 Core 的关键能力

### Direct State Access

`glCreate*()` 系列直接创建已初始化对象名；`glNamed*()`、`glTexture*()`、`glVertexArray*()`、`glGetNamed*()` 直接操作指定对象，而不是操作当前绑定 target。这样资源构建代码可以局部化，减少意外修改全局 binding 的机会。

DSA 不是新对象模型。对象仍属于 context/share group，FBO completeness、texture format、buffer storage flags、VAO attribute layout 等规则完全不变。

### Named buffer/FBO/texture/VAO 操作

Buffer 侧有 `glNamedBufferStorage()`、`glMapNamedBufferRange()`、`glClearNamedBufferData()`、`glCopyNamedBufferSubData()`；texture 侧有 `glTextureStorage*()`、`glTextureSubImage*()`、`glBindTextureUnit()`、`glGenerateTextureMipmap()`；FBO 侧有 `glNamedFramebufferTexture()`、`glNamedFramebufferDrawBuffers()`、`glBlitNamedFramebuffer()`；VAO 侧有 `glVertexArrayAttribFormat()`、`glVertexArrayVertexBuffer()`、`glEnableVertexArrayAttrib()`。

这些接口让资源系统更清楚，但也要求你维护对象之间的显式关系：FBO 附件指向哪个 texture level/layer，VAO attribute 指向哪个 binding index，buffer mapping 是否与 GPU 使用区段冲突。

### Robust readback 与 graphics reset

`glReadnPixels()`、`glGetnTexImage()`、`glGetnCompressedTexImage()`、`glGetnUniform*()`、`glGetTextureSubImage()`、`glGetCompressedTextureSubImage()` 都带 `bufSize`，减少输出越界风险。`glGetGraphicsResetStatus()` 可检查图形上下文 reset 状态。

这些 API 不是性能捷径。读回仍可能同步 GPU；它们的优势是边界更明确。

### Clip control 与 texture barrier

`glClipControl()` 控制 clip space 原点和深度范围，有助于统一跨图形 API 的投影和深度约定。`glTextureBarrier()` 支持某些 framebuffer 写后采样的受限场景，但不能替代完整的 image/SSBO memory barrier 设计。

## 关键边界

### DSA 减少绑定错误，不减少同步责任

直接操作对象不会自动等待 GPU。持久映射、buffer 更新、FBO 写后读、texture copy 后采样仍需同步或 barrier。

### 对象关系仍要显式建模

DSA 代码看起来“无状态”，但 FBO、VAO、texture unit、sampler、UBO/SSBO binding point 都仍是状态或关系。建议用资源描述结构集中生成。

### Clip control 会影响整个渲染约定

改 origin/depth mode 后，投影矩阵、清深度、深度比较、屏幕空间 pass 都要一致。不要在局部 pass 随意切换。

## API 速查表

| 功能族（成员 API） | 是做什么的 | 使用时重点注意 |
| --- | --- | --- |
| `initializeOpenGLFunctions()` | 解析 current OpenGL 4.5 Core profile 函数。 | context 版本/profile 必须匹配；失败后不得调用成员。 |
| DSA 创建：`glCreateBuffers`, `glCreateTextures`, `glCreateFramebuffers`, `glCreateRenderbuffers`, `glCreateVertexArrays`, `glCreateQueries`, `glCreateSamplers`, `glCreateProgramPipelines`, `glCreateTransformFeedbacks` | 直接创建对象名。 | 对象仍属于 context/share group；销毁和使用要有有效 context。 |
| Named buffer：`glNamedBufferStorage`, `glNamedBufferData`, `glNamedBufferSubData`, `glCopyNamedBufferSubData`, `glMapNamedBuffer`, `glMapNamedBufferRange`, `glUnmapNamedBuffer`, `glFlushMappedNamedBufferRange`, `glClearNamedBufferData`, `glClearNamedBufferSubData`, `glGetNamedBuffer*` | 直接分配、更新、映射、清空和查询 buffer。 | storage flags 与映射/更新方式必须匹配；同步仍需 fence/barrier。 |
| Texture DSA：`glCreateTextures`, `glTextureStorage1D`, `glTextureStorage2D`, `glTextureStorage3D`, `glTextureStorage2DMultisample`, `glTextureStorage3DMultisample`, `glTextureSubImage*`, `glCompressedTextureSubImage*`, `glCopyTextureSubImage*`, `glTextureParameter*`, `glGenerateTextureMipmap`, `glBindTextureUnit`, `glGetTexture*`, `glGetTextureSubImage`, `glGetCompressedTextureSubImage`, `glTextureBuffer`, `glTextureBufferRange` | 直接配置、上传、查询和绑定 texture。 | 不再依赖当前 texture binding，但 format/level/layer/size 规则不变。 |
| FBO/renderbuffer DSA：`glCreateFramebuffers`, `glNamedFramebufferTexture`, `glNamedFramebufferTextureLayer`, `glNamedFramebufferRenderbuffer`, `glNamedFramebufferDrawBuffer`, `glNamedFramebufferDrawBuffers`, `glNamedFramebufferReadBuffer`, `glNamedFramebufferParameteri`, `glCheckNamedFramebufferStatus`, `glBlitNamedFramebuffer`, `glClearNamedFramebuffer*`, `glInvalidateNamedFramebuffer*`, `glCreateRenderbuffers`, `glNamedRenderbufferStorage*` | 直接构建、清除、查询和 blit framebuffer/renderbuffer。 | attachment 后仍检查 completeness；viewport/draw buffers 仍要匹配。 |
| VAO DSA：`glCreateVertexArrays`, `glVertexArrayVertexBuffer`, `glVertexArrayVertexBuffers`, `glVertexArrayElementBuffer`, `glVertexArrayAttribFormat`, `glVertexArrayAttribIFormat`, `glVertexArrayAttribLFormat`, `glVertexArrayAttribBinding`, `glVertexArrayBindingDivisor`, `glEnableVertexArrayAttrib`, `glDisableVertexArrayAttrib`, `glGetVertexArray*` | 直接配置 VAO 的 buffer binding、attribute format 和启用状态。 | 区分 attribute index、binding index、relative offset、stride、divisor。 |
| Robust/readback：`glReadnPixels`, `glGetnTexImage`, `glGetnCompressedTexImage`, `glGetnUniformfv`, `glGetnUniformiv`, `glGetnUniformuiv`, `glGetnUniformdv`, `glGetGraphicsResetStatus` | 带输出缓冲大小的读回和 reset 状态查询。 | 读回仍可能同步；`bufSize` 防越界不防性能问题。 |
| 其他 4.5：`glClipControl`, `glTextureBarrier`, `glMemoryBarrierByRegion` | 控制 clip 原点/深度、受限纹理读写反馈和区域 barrier。 | Clip 约定全局影响投影/深度；barrier 类型不要混用。 |
| 继承的 4.4/4.3 Core：`glBufferStorage`, `glBindTextures`, `glBindSamplers`, `glBindImageTextures`, `glDispatchCompute`, `glShaderStorageBlockBinding`, `glMultiDraw*Indirect`, `glDebugMessage*`, `glObjectLabel` | 不可变 buffer、多绑定、compute/SSBO、GPU-driven draw 和调试输出。 | DSA 不替代这些资源的 barrier、binding 与调试策略。 |

## 常见误区

### 以为 DSA 彻底没有状态

DSA 减少“先 bind 再改”的状态依赖，但 draw 使用的 program、VAO、FBO、texture unit、sampler、buffer binding 仍然是状态。它是更清楚，不是完全无状态。

### 修改 clip control 后只改投影矩阵

深度范围、清深度、depth func、屏幕空间 pass 和后处理采样都可能受影响。应把 clip/depth 约定作为 renderer 全局配置。

### 用 bounded readback 当性能优化

`glReadnPixels()` 防止写越界，但读回依旧可能阻塞 GPU。性能问题要用异步 PBO、延迟读取或减少读回解决。

## 一句话总结

`QOpenGLFunctions_4_5_Core` 是 Qt OpenGL 中最完整的 Core 资源管理入口；Direct State Access 让对象配置更局部、更可靠，但同步、binding 关系和全局渲染约定仍要由你的资源系统认真管理。
