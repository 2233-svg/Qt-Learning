# QOpenGLExtraFunctions

> Qt 6.11.1 · Qt GUI · 来自 `QOpenGLExtraFunctions`

## 1. 先建立直觉

`QOpenGLExtraFunctions` 扩展了 `QOpenGLFunctions`，提供更多 OpenGL ES 3.x、OpenGL 3.x/4.x 以及部分扩展函数入口。它适合需要 VAO、sampler object、transform feedback、query、sync、debug output、compute shader、program pipeline、buffer mapping 等现代 OpenGL 能力的代码。

它只负责把函数解析出来，不保证每个函数在当前 context 上合法。真正能不能调用，仍取决于 `QOpenGLContext::format()` 的版本/profile、是否 OpenGL ES、以及扩展支持。

## 2. 类说明

- 头文件：`#include <QOpenGLExtraFunctions>`
- CMake：`target_link_libraries(mytarget PRIVATE Qt6::Gui)`
- 继承：`QOpenGLFunctions`
- 获取方式：常用 `QOpenGLContext::extraFunctions()`。

通过 `context->extraFunctions()` 取得的对象已经初始化；自己构造时仍要在 context current 后初始化。

## 3. API 速查

| 函数组 | 用途 |
|---|---|
| 构造与初始化 | `QOpenGLExtraFunctions()`、`QOpenGLExtraFunctions(context)`，继承 `initializeOpenGLFunctions()`。 |
| VAO 与顶点绑定 | `glGenVertexArrays`、`glBindVertexArray`、`glVertexAttribFormat`、`glBindVertexBuffer`、`glVertexBindingDivisor`。 |
| 实例化绘制 | `glDrawArraysInstanced`、`glDrawElementsInstanced`、`glVertexAttribDivisor`。 |
| 间接绘制 | `glDrawArraysIndirect`、`glDrawElementsIndirect`。 |
| 多渲染目标/独立状态 | `glDrawBuffers`、`glBlendFunci`、`glColorMaski`、`glEnablei`。 |
| 3D/不可变纹理 | `glTexImage3D`、`glTexStorage2D`、`glTexStorage3D`、`glTexSubImage3D`。 |
| FBO 扩展 | `glBlitFramebuffer`、`glFramebufferTexture`、`glFramebufferTextureLayer`、`glInvalidateFramebuffer`。 |
| Sampler 对象 | `glGenSamplers`、`glBindSampler`、`glSamplerParameter*`。 |
| UBO/Uniform 查询 | `glGetUniformBlockIndex`、`glUniformBlockBinding`、`glGetActiveUniformBlock*`。 |
| Program pipeline | `glGenProgramPipelines`、`glUseProgramStages`、`glBindProgramPipeline`、`glValidateProgramPipeline`。 |
| Transform feedback | `glBeginTransformFeedback`、`glTransformFeedbackVaryings`、`glBindTransformFeedback`。 |
| Query 对象 | `glGenQueries`、`glBeginQuery`、`glEndQuery`、`glGetQueryObjectuiv`。 |
| Sync 对象 | `glFenceSync`、`glClientWaitSync`、`glWaitSync`、`glDeleteSync`。 |
| Buffer mapping | `glMapBufferRange`、`glUnmapBuffer`、`glFlushMappedBufferRange`。 |
| Compute shader | `glDispatchCompute`、`glMemoryBarrier`、`glBindImageTexture`。 |
| Debug output | `glDebugMessageCallback`、`glDebugMessageControl`、`glPushDebugGroup`、`glObjectLabel`。 |
| Robustness/安全读取 | `glGetGraphicsResetStatus`、`glReadnPixels`、`glGetnUniform*`。 |

## 4. 关键用法

### 获取 extra 函数入口

```cpp
if (context->makeCurrent(surface)) {
    QOpenGLExtraFunctions *gl = context->extraFunctions();
    gl->glGenVertexArrays(1, &vao);
    gl->glBindVertexArray(vao);
}
```

入口对象来自 context，所以必须在对应 context 或共享 context current 时使用。不要把一个 context 的 extra 函数对象长期拿到另一个不共享 context 的渲染路径里。

### 调用前验证版本或扩展

```cpp
const QSurfaceFormat fmt = context->format();
const bool canUseCompute =
    !context->isOpenGLES() && fmt.version() >= qMakePair(4, 3);
```

`QOpenGLExtraFunctions` 包含很多函数名，但 OpenGL 运行时可能不支持。对 compute、debug output、program pipeline、texture storage 等功能，务必按目标平台检查版本和扩展。

## 5. 使用场景

| 场景 | 建议 |
|---|---|
| 现代 OpenGL 渲染器 | 用 VAO、UBO、sampler、instancing 等函数组织状态。 |
| 离屏后处理 | 用 FBO blit、多个 render target、texture storage。 |
| GPU 粒子/计算 | 用 compute shader、image load/store、memory barrier。 |
| 性能分析 | 用 query、sync 和 debug label 分析 GPU 时间与对象。 |
| 跨 OpenGL ES 和桌面 GL | 只使用共同支持子集，并做运行时能力分支。 |

## 6. 常见坑与经验

- extra 函数“可调用入口”与“当前 context 支持”是两件事。调用不支持的函数仍会失败或产生 GL 错误。
- `glMemoryBarrier()` 是 compute/image/SSBO 等路径正确性的关键，缺失时结果可能偶发错误。
- `glMapBufferRange()` 返回的指针只在映射有效期间使用；必须按访问标志和同步规则处理。
- Debug callback 需要合适的 debug context 或扩展支持；没有回调不代表没有错误。
- Program pipeline、separable program 与传统 `glUseProgram()` 路径语义不同，不要混合后不清理状态。
- 多线程渲染时，同步对象只解决 GPU 队列同步，不解决 CPU 侧 QObject/context 线程归属问题。

## 7. 知识点覆盖

- OpenGL ES 3.x / OpenGL 3.x/4.x 额外函数入口
- VAO、实例化、间接绘制、UBO、sampler 和 texture storage
- Query、sync、debug output 和 robustness
- Compute shader、image 绑定和 memory barrier
- 版本/profile/扩展检查与跨平台降级策略
