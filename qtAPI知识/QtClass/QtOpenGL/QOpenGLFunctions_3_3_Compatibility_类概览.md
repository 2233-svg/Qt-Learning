# QOpenGLFunctions_3_3_Compatibility 类笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QOpenGLFunctions_3_3_Compatibility>`  
> 所属模块：`Qt6::OpenGL`  
> 继承：`QAbstractOpenGLFunctions`  
> 可用性：桌面 OpenGL 3.3 Compatibility profile；包含 3.3 Core API 与旧 fixed-function/legacy 接口

## 它解决什么问题

`QOpenGLFunctions_3_3_Compatibility` 是 Qt 对 OpenGL 3.3 Compatibility profile 的函数包装。它让一个仍依赖旧 OpenGL 状态机的程序也能使用 3.3 时代的 sampler object、attribute divisor、timer query、UBO、FBO、VAO 和 sync fence。

它的定位是“迁移桥”，不是新 renderer 的默认选择。Compatibility profile 允许 `glBegin()`、矩阵栈、固定光照、client arrays、display list 等历史接口继续存在；同时也带来状态污染、平台覆盖和 Core-only 部署失败的风险。新代码应限制在 Core 子集内，旧代码应被封装在单独模块并逐步替换。

## 什么时候使用

- 第三方或历史渲染器仍使用 fixed-function API，但你需要在 Qt 6 中让它继续工作；
- 旧场景图想逐步加入 3.3 的实例化、sampler object 或 timer query；
- 正在把 CAD/科学可视化/模型查看器从 display list、client array、immediate mode 迁移到 VBO/VAO/shader。

如果项目目标是新桌面渲染器，优先选择 `QOpenGLFunctions_3_3_Core`，让错误的 legacy 调用在类型层面不可见。

## 初始化与隔离建议

```cpp
#include <QOpenGLFunctions_3_3_Compatibility>

QOpenGLFunctions_3_3_Compatibility gl;

bool initializeCompatibilityRenderer()
{
    if (!gl.initializeOpenGLFunctions())
        return false;

    gl.glEnable(GL_DEPTH_TEST);
    gl.glDisable(GL_CULL_FACE);
    return true;
}
```

Compatibility context 必须由 `QSurfaceFormat` 明确请求并成功创建。推荐把旧绘制封装为 `drawLegacy()`，把现代绘制封装为 `drawCorePath()`，两者进入前都显式设定所需状态，避免旧矩阵、client state、texture environment 或 display list 残留影响 shader 路径。

## 3.3 现代能力如何进入旧项目

### Sampler object

`glGenSamplers()`、`glBindSampler()` 和 `glSamplerParameter*()` 允许把采样参数从 texture object 分离出来。旧项目常把同一纹理在多个 pass 中反复改 wrap/filter；sampler object 可以把这些状态变成可复用对象，减少隐式修改。

### Instanced attribute

`glVertexAttribDivisor()` 配合 instanced draw，让每实例矩阵、颜色、ID 等数据按实例推进。它是替代“循环里多次 draw 同一网格并改 uniform”的重要步骤，也是从旧 display list / immediate mode 迁移到批处理的切入点。

### Timer query

`glQueryCounter()` 与 `glGetQueryObject*i64v()` 适合衡量旧 pass 改造前后的 GPU 时间。但读回必须延迟，否则测到的多半是同步等待而非真实 GPU 工作量。

### Dual-source blending 与 packed attribute

`glBindFragDataLocationIndexed()` 支持 dual-source blending 布局；`glVertexAttribP*()` 支持打包属性值。它们适合优化现代 shader 路径，不应拿来延续固定管线的颜色/法线状态。

## Compatibility 边界

### 它不是 Core 的无风险超集

Compatibility 让更多函数可见，也让更多隐式状态有机会影响渲染结果。旧 API 与 shader API 在同一 context 中共享 texture binding、buffer binding、blend/depth/stencil、viewport、pixel store 等状态；调试时必须把状态归因范围缩小。

### Legacy API 仍不能面向 OpenGL ES 或 Core-only 平台

`glBegin()`、display list、固定光照、client arrays、selection/feedback 和 imaging subset 都没有现代跨平台保障。部署前应明确检测 profile，并给不支持 Compatibility 的平台提供替代路径。

### 迁移目标要写在代码结构里

如果旧函数散落在新渲染代码中，后续很难切到 Core profile。更好的做法是将 Compatibility-only 调用集中在少数文件和接口中，逐步用 VBO/VAO/shader/FBO 替代。

## API 速查表

| 功能族（成员 API） | 是做什么的 | 使用时重点注意 |
| --- | --- | --- |
| `initializeOpenGLFunctions()` | 解析 current 3.3 Compatibility profile 函数。 | profile 必须匹配；初始化失败后不能调用成员。 |
| 3.3 sampler：`glGenSamplers`, `glDeleteSamplers`, `glIsSampler`, `glBindSampler`, `glSamplerParameteri`, `glSamplerParameteriv`, `glSamplerParameterf`, `glSamplerParameterfv`, `glSamplerParameterIiv`, `glSamplerParameterIuiv`, `glGetSamplerParameter*` | 创建并管理独立采样状态。 | sampler 绑定到 texture unit；shader sampler uniform 仍写 unit 编号。 |
| 3.3 instancing：`glVertexAttribDivisor` | 设置 attribute 按实例推进。 | 状态随 VAO 保存；与 `glDraw*Instanced` 和实例 buffer 配合。 |
| 3.3 timer/query：`glQueryCounter`, `glGetQueryObjecti64v`, `glGetQueryObjectui64v` | 插入 GPU 时间戳并读取 64 位结果。 | 延迟读取，避免 CPU/GPU 同步污染测量。 |
| 3.3 output/packed attribute：`glBindFragDataLocationIndexed`, `glGetFragDataIndex`, `glVertexAttribP1ui`, `glVertexAttribP2ui`, `glVertexAttribP3ui`, `glVertexAttribP4ui`, `glVertexAttribP1uiv`, `glVertexAttribP2uiv`, `glVertexAttribP3uiv`, `glVertexAttribP4uiv` | dual-source blending 输出绑定和 packed attribute 当前值。 | output 绑定需在 link 前；packed 类型要与 shader 输入匹配。 |
| 继承的 3.2 现代 API：`glTexImage2DMultisample`, `glTexImage3DMultisample`, `glFenceSync`, `glClientWaitSync`, `glDrawElementsBaseVertex`, `glFramebufferTexture`, `glProvokingVertex` | MSAA texture、sync fence、base-vertex draw 和通用 FBO attachment。 | MSAA 需 resolve 或 sample fetch；fence 不应无限等待。 |
| 继承的 3.1/3.0 现代 API：`glDrawArraysInstanced`, `glDrawElementsInstanced`, `glTexBuffer`, `glCopyBufferSubData`, `glGetUniformBlockIndex`, `glUniformBlockBinding`, `glBindVertexArray`, `glBindFramebuffer`, `glMapBufferRange`, `glBeginTransformFeedback` | UBO、VAO/FBO、实例化、buffer texture 和 transform feedback。 | 新代码优先使用这些 Core 子集；检查 binding、对齐和 FBO 完整性。 |
| 继承的 GLSL/buffer/texture：`glCreateShader`, `glCompileShader`, `glLinkProgram`, `glUseProgram`, `glVertexAttribPointer`, `glUniform*`, `glGenBuffers`, `glBufferData`, `glActiveTexture`, `glTexImage*`, `glDrawArrays`, `glDrawElements` | shader program、VBO、纹理和基础绘制。 | compile/link 与 attribute layout 必须检查；资源属于 context 共享组。 |
| legacy 几何与矩阵：`glBegin`, `glEnd`, `glVertex*`, `glColor*`, `glNormal*`, `glTexCoord*`, `glMatrixMode`, `glLoad*`, `glMultMatrix*`, `glTranslate*`, `glRotate*`, `glScale*` | 立即模式与固定矩阵栈。 | 只为旧代码保留；迁移到 VBO/VAO 与 shader uniform。 |
| legacy 光照/纹理/像素：`glLight*`, `glMaterial*`, `glFog*`, `glTexEnv*`, `glTexGen*`, `glMultiTexCoord*`, `glClientActiveTexture`, `glVertexPointer`, `glEnableClientState`, `glDrawPixels`, `glColorTable*`, `glConvolution*`, `glHistogram*` | 固定管线材质、纹理组合、client arrays 与 imaging subset。 | 不适用于 Core/ES；pixel-store 和 CPU 指针生命周期很容易出错。 |
| legacy 管理与反馈：`glNewList`, `glCallList*`, `glMap*`, `glEval*`, `glRenderMode`, `glSelectBuffer`, `glFeedbackBuffer`, `glPushAttrib`, `glPopAttrib` | display list、evaluator、selection/feedback 和状态栈。 | 逐步替换；不要让新模块继续依赖。 |

## 常见误区

### 在 Compatibility 中写新功能，继续调用固定管线矩阵

这会让代码永远无法切到 Core。即使 context 允许，也应把新功能写成 shader + buffer + uniform 路径。

### 旧路径改了全局状态，新路径没有恢复

典型例子是 client state、active texture、pixel store、blend/stencil 和矩阵模式。进入每个渲染阶段前显式设定必要状态，退出时恢复或让下一阶段自给自足。

### 以为 3.3 Compatibility 在所有 3.3 硬件上都可用

版本号和 profile 是两个维度。驱动或平台可能只给 Core；初始化失败时要有明确降级或禁用策略。

## 一句话总结

`QOpenGLFunctions_3_3_Compatibility` 是把旧 OpenGL 渲染器带到 3.3 时代的桥接层；它能同时访问现代 3.3 能力和历史 API，但健康的使用方式是把 legacy 隔离住，并持续向 `QOpenGLFunctions_3_3_Core` 风格收敛。
