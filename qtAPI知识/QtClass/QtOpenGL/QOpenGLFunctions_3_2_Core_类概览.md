# QOpenGLFunctions_3_2_Core 类笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QOpenGLFunctions_3_2_Core>`  
> 所属模块：`Qt6::OpenGL`  
> 继承：`QAbstractOpenGLFunctions`  
> 可用性：仅匹配桌面 OpenGL 3.2 Core profile；不提供 fixed-function、立即模式、client state 或其他 Compatibility API

## 它解决什么问题

`QOpenGLFunctions_3_2_Core` 是 Qt 对 OpenGL 3.2 Core profile 的函数包装。它为当前 `QOpenGLContext` 解析纯 Core 函数集，最重要的意义不是“比 3.1 多几个函数”，而是明确切断旧式 OpenGL 的调用入口：没有矩阵栈、`glBegin()`、固定光照、display list，也没有 client-side vertex array。

它适合把 Qt renderer 约束在可迁移、可验证的现代管线中。OpenGL 3.2 新增的 multisample texture、sync fence、base-vertex draw、完整 texture attachment 和 provoking vertex 等能力，解决了 MSAA 资源、GPU/CPU 协作、共享索引网格和 flat shading 控制中的低层问题。

当项目可以选择 profile 时，Core 版本应优先于 Compatibility 版本。只有无法修改的旧渲染代码必须使用 fixed-function API 时，才选择 `QOpenGLFunctions_3_2_Compatibility`。

## 实际使用场景

- 创建 OpenGL 3.2 Core context，并让 renderer 在 macOS 等 Core-only 环境保持可运行；
- 构建 multisample texture/FBO 路径，用 resolve 后的纹理做后处理；
- 用 `GLsync` fence 保护 buffer 重用、读回或跨帧资源循环；
- 一套顶点数据配合不同 index base 绘制多个子网格；
- 强制团队代码不再混入 deprecated GL 1.x 状态机。

## 初始化与最小示例

```cpp
#include <QOpenGLFunctions_3_2_Core>

QOpenGLFunctions_3_2_Core gl;

bool initializeCoreRenderer()
{
    // QSurfaceFormat 请求的 profile 必须与此类匹配，且 context 已 current。
    if (!gl.initializeOpenGLFunctions())
        return false;

    GLuint vao = 0;
    gl.glGenVertexArrays(1, &vao);
    gl.glBindVertexArray(vao);
    return true;
}
```

`initializeOpenGLFunctions()` 失败通常意味着 current context 的版本或 profile 不匹配。不要在失败后退回调用裸 OpenGL 符号；应选择匹配的 Qt 函数类或调整 `QSurfaceFormat`。

## 3.2 Core 的关键能力

### Multisample texture 与 sample mask

`glTexImage2DMultisample()` 和 `glTexImage3DMultisample()` 分配多重采样 texture 存储；sample 不能像普通 texture 那样通过过滤采样，通常由 `sampler2DMS`/`sampler2DMSArray` 和 `texelFetch` 按 sample index 读取。`glSampleMaski()` 控制 sample mask，`glGetMultisamplefv()` 查询 sample position。

MSAA 不等于“自动有抗锯齿结果”。多重采样 attachment 常需用 `glBlitFramebuffer()` resolve 到单采样 texture，之后才能按普通后处理路径采样。实际 samples 还受 `GL_MAX_SAMPLES` 和 format/FBO 限制。

### Sync object

`glFenceSync()` 在命令流中插入 fence；`glClientWaitSync()` 允许 CPU 有超时地等待，`glWaitSync()` 让 GPU 等待，`glGetSynciv()` 查询状态，`glDeleteSync()` 释放对象。它是管理环形 buffer、异步纹理上传和分帧读回的基础工具。

fence 只保证它之前命令的完成顺序，不会替应用修复资源所有权和数据竞争。CPU 侧应优先使用有限或零超时轮询，并设计多个资源槽位；无限等待会把异步 GPU 管线变成同步阻塞。

### Base-vertex 绘制

`glDrawElementsBaseVertex()`、`glDrawRangeElementsBaseVertex()`、`glDrawElementsInstancedBaseVertex()` 和 `glMultiDrawElementsBaseVertex()` 在 indices 解释结果上再加 `basevertex`。它允许多个子网格共用一个大顶点 buffer，同时各自保持局部索引。

base vertex 会参与最终顶点索引计算，不能让结果越过 VBO 的有效范围。EBO 绑定时 `indices` 依旧是字节偏移；多绘制版本的 `basevertex[]`、count[] 和 indices[] 数组长度必须与 `drawcount` 对齐。

### `glFramebufferTexture()` 与 provoking vertex

`glFramebufferTexture()` 比旧的 `glFramebufferTexture2D()` 更通用，可将 texture 的指定 level 作为 attachment，由 GL 按 texture 类型处理。`glProvokingVertex()` 决定 flat-qualified varying 从 primitive 的第一个还是最后一个顶点取得值，避免 flat shading/primitive ID 类效果在不同 primitive 组织下含糊。

前者不替代 FBO completeness 检查；后者只影响 flat interpolation，不能修复 attribute 或 shader interface 的其他错误。

## 核心边界

### Core profile 是契约，不是性能选项

Core context 中调用 legacy API 不会“慢一点”，而是根本不属于可用函数集。以 `QOpenGLFunctions_3_2_Core` 作为唯一 GL 入口能让这类误用在代码结构上更明显。

### `GLsync` 不是跨 context 的通用锁

sync object 与 OpenGL context/share group 相关；跨线程使用之前，需要先确保资源共享关系和 context current 规则成立。它也不会代替 Qt 线程同步原语来保护普通 CPU 数据。

### 多重采样 texture 不可按普通纹理过滤

不能把 `GL_TEXTURE_2D_MULTISAMPLE` 当作 `GL_TEXTURE_2D` 配上 `GL_LINEAR` 后直接采样。resolve、shader sample fetch 和 attachment 设计必须从一开始就配套。

## API 速查表

| 功能族（成员 API） | 是做什么的 | 使用时重点注意 |
| --- | --- | --- |
| `initializeOpenGLFunctions()` | 解析 current OpenGL 3.2 Core profile 函数。 | 当前 context 必须是匹配的 Core profile；失败后不要继续调用。 |
| `glTexImage2DMultisample`, `glTexImage3DMultisample` | 分配 2D/3D 多重采样 texture 存储。 | samples/format/尺寸受实现限制；MS texture 不能按普通 filtered texture 使用。 |
| `glSampleMaski`, `glGetMultisamplefv` | 设置 sample mask、查询 sample position。 | 只在 multisample 路径有意义；index 和 bitmask 要符合实现支持范围。 |
| `glFenceSync`, `glIsSync`, `glDeleteSync`, `glClientWaitSync`, `glWaitSync`, `glGetSynciv`, `glGetInteger64v` | 创建、等待、查询和释放 GPU sync fence。 | 避免无限 CPU 等待；同步对象与 context/shared resources 生命周期一致。 |
| `glDrawElementsBaseVertex`, `glDrawRangeElementsBaseVertex`, `glDrawElementsInstancedBaseVertex`, `glMultiDrawElementsBaseVertex` | 在 index 结果上叠加 base vertex 进行单次/实例化/多批绘制。 | indices 仍是 EBO offset；最终 index 与所有参数数组不可越界。 |
| `glProvokingVertex` | 选择 flat varying 由 first 或 last vertex 提供。 | 仅影响 flat interpolation；应与 shader 和 primitive 拓扑一起验证。 |
| `glFramebufferTexture` | 通用地把 texture level 附加到 FBO。 | 改 attachment 后检查 `glCheckFramebufferStatus`；确认层/level 与 shader 使用方式。 |
| `glGetBufferParameteri64v`, `glGetInteger64i_v` | 查询 64 位 buffer 或 indexed state 限制/值。 | 输出类型是 `GLint64`；用于能力查询，不应频繁调用。 |
| 继承的 3.1：`glDraw*Instanced`, `glTexBuffer`, `glCopyBufferSubData`, `glPrimitiveRestartIndex`, `glGetUniformBlockIndex`, `glGetActiveUniform*`, `glUniformBlockBinding`, `glBindBufferBase`, `glBindBufferRange` | 实例化、buffer texture、UBO 和 primitive restart。 | UBO block index 与 binding point 不同；3.1 无 core vertex divisor。 |
| 继承的 3.0：`glGenVertexArrays`, `glBindVertexArray`, `glGenFramebuffers`, `glBindFramebuffer`, `glFramebufferTexture*`, `glRenderbufferStorage*`, `glBlitFramebuffer`, `glMapBufferRange`, `glBeginTransformFeedback`, `glVertexAttribIPointer` | VAO、FBO、map range、transform feedback 与整数顶点输入。 | Core draw 需 VAO；FBO 还要匹配 viewport、outputs 与 attachment。 |
| 继承的 2.x：`glCreateShader`, `glCompileShader`, `glLinkProgram`, `glUseProgram`, `glVertexAttribPointer`, `glUniform*`, `glDrawBuffers`, `glBlend*Separate`, `glStencil*Separate` | GLSL、顶点输入、uniform 和多输出状态。 | 检查 compile/link log；attribute 数据布局和 program state 必须对应。 |
| 继承的 1.x Core 成员：`glGenBuffers`, `glBufferData`, `glBindTexture`, `glTexImage*`, `glDrawArrays`, `glDrawElements`, `glViewport`, `glClear*`, `glDepth*`, `glBlendFunc` | 基础 buffer、texture、draw 和输出状态。 | 不包含任何 deprecated fixed-function 函数；资源和状态属于 current context。 |

## 常见误区

### 用 Compatibility context 初始化 Core 函数对象

这两类函数对象表达的 profile 要求不同。应让 `QSurfaceFormat` 的版本、profile 与函数类保持一致，而不是依赖某台机器“碰巧也能跑”。

### fence 创建后每帧无限等待

这会抵消多缓冲带来的并行优势。更合理的是延迟复用、零超时检查和多个 in-flight 资源槽。

### 将多重采样 texture 当作可直接采样的后处理输入

普通 sampler 不能读取它。先 resolve 到单采样 texture，或在 shader 中按 sample 显式 fetch/resolve。

## 一句话总结

`QOpenGLFunctions_3_2_Core` 是 Qt 中建立严格现代 OpenGL 管线的起点：它明确排除 legacy API，并用 multisample texture、fence 与 base-vertex draw 处理更真实的资源和同步问题。
