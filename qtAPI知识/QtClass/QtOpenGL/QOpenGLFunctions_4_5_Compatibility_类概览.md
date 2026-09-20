# QOpenGLFunctions_4_5_Compatibility 类笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QOpenGLFunctions_4_5_Compatibility>`  
> 所属模块：`Qt6::OpenGL`  
> 继承：`QAbstractOpenGLFunctions`  
> 可用性：桌面 OpenGL 4.5 Compatibility profile；包含 4.5 Core API 与旧 fixed-function/legacy 接口

## 它解决什么问题

`QOpenGLFunctions_4_5_Compatibility` 让 Qt 程序在 OpenGL 4.5 Compatibility context 中使用 Direct State Access、clip control、robust readback、texture barrier 等现代 4.5 能力，同时仍保留旧 fixed-function 和 deprecated API。

它适合非常典型的“长期大型遗留项目”：新资源系统希望用 DSA 降低全局绑定错误，旧模块仍需要矩阵栈、display list、client array 或传统像素路径。这个类能让两者共存，但共存不是终点；新代码应只使用 Core 子集，旧调用应被隔离并逐步替换。

## 实际使用场景

- 用 `glCreate*`/`glNamed*` 逐步改造旧资源管理器，减少 bind-to-edit 错误；
- 新 renderer 使用 DSA 配置 FBO/VAO/texture，旧 overlay 暂时保留固定管线；
- 在 Compatibility context 中加入 robust readback 和 graphics reset 检测；
- 迁移到跨 API 坐标系统时使用 `glClipControl()`，同时保留旧场景模块。

## 初始化与隔离建议

```cpp
#include <QOpenGLFunctions_4_5_Compatibility>

QOpenGLFunctions_4_5_Compatibility gl;

bool initializeDsaBridge()
{
    if (!gl.initializeOpenGLFunctions())
        return false;

    GLuint vao = 0;
    gl.glCreateVertexArrays(1, &vao);
    return true;
}
```

在 Compatibility profile 下使用 DSA，最好把新资源层完全写成 Core 风格：对象创建、配置、绑定关系都显式描述；旧 fixed-function 绘制只通过狭窄入口调用，并在进入/退出时处理状态。

## 4.5 能力如何帮助迁移

### DSA 降低旧代码的隐式状态依赖

旧 OpenGL 代码常因“当前绑定对象”出错。`glCreateBuffers()`、`glNamedBufferStorage()`、`glCreateTextures()`、`glTextureStorage*()`、`glCreateFramebuffers()`、`glNamedFramebufferTexture()`、`glCreateVertexArrays()`、`glVertexArray*()` 等接口能把资源构建从全局 binding 中解耦。

### Robust readback 更适合维护工具

`glReadnPixels()`、`glGetnTexImage()`、`glGetnUniform*()`、`glGetGraphicsResetStatus()` 有助于调试、截图、诊断和容错。它们不会解决读回性能问题，但能让输出缓冲边界更明确。

### Clip control 是全局渲染约定

使用 `glClipControl()` 统一坐标约定时，旧固定管线矩阵和新 shader 投影矩阵都要遵守同一深度/原点规则。Compatibility 项目尤其要避免新旧模块各自假设不同 NDC。

## Compatibility 边界

### DSA 不会清理 legacy 状态

DSA 只让对象配置更直接。旧模块留下的矩阵栈、client state、texture environment、pixel store、display list 副作用仍可能影响后续绘制。

### 新资源层应避免依赖 Compatibility-only 能力

如果 DSA 资源系统中混入 `glBegin()` 或固定管线状态，未来无法切 Core。保持新资源层和 draw path 都在 Core 子集中。

### 读回和同步依旧昂贵

bounded readback、named buffer readback、texture subimage readback 都可能让 CPU 等待 GPU。维护工具可以用，实时路径要谨慎。

## API 速查表

| 功能族（成员 API） | 是做什么的 | 使用时重点注意 |
| --- | --- | --- |
| `initializeOpenGLFunctions()` | 解析 current 4.5 Compatibility profile 函数。 | profile 必须匹配；失败后不得调用成员。 |
| DSA 创建/对象：`glCreateBuffers`, `glCreateTextures`, `glCreateFramebuffers`, `glCreateRenderbuffers`, `glCreateVertexArrays`, `glCreateQueries`, `glCreateSamplers`, `glCreateProgramPipelines`, `glCreateTransformFeedbacks` | 直接创建对象名。 | 对象仍属于 context/share group；不是跨 API 资源。 |
| Named buffer：`glNamedBufferStorage`, `glNamedBufferData`, `glNamedBufferSubData`, `glCopyNamedBufferSubData`, `glMapNamedBuffer*`, `glUnmapNamedBuffer`, `glFlushMappedNamedBufferRange`, `glClearNamedBuffer*`, `glGetNamedBuffer*` | 直接操作 buffer 存储、映射、清空和查询。 | 与旧 draw 共用 buffer 时更要用 fence 管理生命周期。 |
| Texture/FBO/VAO DSA：`glTextureStorage*`, `glTextureSubImage*`, `glTextureParameter*`, `glBindTextureUnit`, `glGenerateTextureMipmap`, `glNamedFramebuffer*`, `glCheckNamedFramebufferStatus`, `glBlitNamedFramebuffer`, `glNamedRenderbufferStorage*`, `glVertexArray*`, `glEnableVertexArrayAttrib`, `glDisableVertexArrayAttrib` | 直接配置 texture、FBO/renderbuffer 和 VAO。 | 减少绑定错误，但 attachment/layout/format 规则不变。 |
| Robust/clip：`glReadnPixels`, `glGetnTexImage`, `glGetnCompressedTexImage`, `glGetnUniform*`, `glGetTextureSubImage`, `glGetCompressedTextureSubImage`, `glGetGraphicsResetStatus`, `glClipControl`, `glTextureBarrier`, `glMemoryBarrierByRegion` | 安全边界读回、reset 查询、clip 约定和受限 barrier。 | 读回仍同步；clip control 要全局一致。 |
| 继承的现代 Core 子集：`glBufferStorage`, `glBindTextures`, `glDispatchCompute`, `glShaderStorageBlockBinding`, `glMemoryBarrier`, `glProgramUniform*`, `glGenSamplers`, `glFenceSync`, `glDebugMessage*`, `glObjectLabel` | 不可变 buffer、多绑定、compute/SSBO、program pipeline、sampler、sync 和调试。 | 新模块应使用这些 Core 风格接口组织资源。 |
| legacy 几何/矩阵：`glBegin`, `glEnd`, `glVertex*`, `glColor*`, `glNormal*`, `glTexCoord*`, `glMatrixMode`, `glLoad*`, `glTranslate*`, `glRotate*`, `glScale*` | 立即模式与固定矩阵栈。 | 只留在旧模块；新 DSA 资源层不应依赖。 |
| legacy 光照/像素/反馈：`glLight*`, `glMaterial*`, `glFog*`, `glTexEnv*`, `glTexGen*`, `glVertexPointer`, `glDrawPixels`, `glColorTable*`, `glConvolution*`, `glNewList`, `glCallList*`, `glSelectBuffer`, `glFeedbackBuffer` | 固定管线、client arrays、传统像素、display list 与反馈模式。 | 不适用于 Core/ES；状态污染和同步风险高。 |

## 常见误区

### 以为 DSA 可以和旧状态机随意混用

DSA 只是配置对象更直接。draw 时仍然会受当前 program、VAO、FBO、blend/depth/stencil、texture unit 和 legacy 状态影响。

### 新旧模块对 clip control 有不同假设

一旦改变 origin/depth mode，所有投影和屏幕空间 pass 都必须按同一约定更新。旧矩阵栈路径也不例外。

### 用 `glReadnPixels()` 频繁截图或拾取

它防止越界，不防止同步。实时拾取优先考虑异步 PBO、ID buffer 延迟读取或 GPU picking 设计。

## 一句话总结

`QOpenGLFunctions_4_5_Compatibility` 是遗留 Qt OpenGL 项目接入 DSA 的最高版本过渡层；它能显著改善新资源层的清晰度，但只有把 legacy 调用隔离住，才能真正享受到 Core 风格的可靠性。
