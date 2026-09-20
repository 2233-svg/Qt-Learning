# QOpenGLFunctions_4_0_Core 类笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QOpenGLFunctions_4_0_Core>`  
> 所属模块：`Qt6::OpenGL`  
> 继承：`QAbstractOpenGLFunctions`  
> 可用性：桌面 OpenGL 4.0 Core profile；不包含旧 fixed-function 或 Compatibility API

## 它解决什么问题

`QOpenGLFunctions_4_0_Core` 为 Qt 程序提供 OpenGL 4.0 Core profile 的版本化函数入口。4.0 的主题是把 GPU 管线进一步显式化：tessellation patch 参数、transform feedback object、indirect draw、shader subroutine、双精度 uniform、indexed query、per-buffer blending 和 sample shading 都进入可直接使用的 core 能力。

它适合已经完成 3.3 Core 基础设施的 renderer：你有 VAO/VBO/FBO/shader/UBO/sampler object，并且需要更复杂的 GPU 驱动绘制、曲面细分、GPU 数据回灌或多 render target 独立混合。它不适合仍依赖矩阵栈、立即模式或固定光照的新代码；这些接口在 Core 版中不可见。

## 实际使用场景

- 使用 tessellation control/evaluation shader 绘制曲面、地形或自适应细分网格；
- 捕获 transform feedback 结果并以对象形式暂停、恢复、重放；
- 让 GPU/CPU 写好的 indirect command buffer 驱动 draw，减少 CPU 调用组织；
- 对不同 MRT 颜色附件设置不同 blend equation/factor；
- 在 shader 中用 subroutine 选择算法分支，或上传 `double`/`dvec`/`dmat` uniform。

## 初始化与最小示例

```cpp
#include <QOpenGLFunctions_4_0_Core>

QOpenGLFunctions_4_0_Core gl;

bool initializeTessellationPath()
{
    if (!gl.initializeOpenGLFunctions())
        return false;

    gl.glPatchParameteri(GL_PATCH_VERTICES, 3);
    return true;
}
```

初始化要求 current context 是 OpenGL 4.0 Core profile 或兼容的更高 Core profile。若你只需要 3.3 的 sampler/instancing/timer query，则无需提升到 4.0；提升版本会减少可覆盖硬件范围。

## 4.0 Core 的关键能力

### Tessellation patch state

`glPatchParameteri()` 设置每个 patch 的控制点数量，`glPatchParameterfv()` 可设置默认 outer/inner tessellation level。只有使用 tessellation shader 并以 `GL_PATCHES` 绘制时，这些状态才有意义。

常见错误是忘记把 primitive mode 改为 `GL_PATCHES`，或 patch vertex 数量与 tessellation control shader 的 layout 不一致。patch 状态是 context state，切换不同 tessellation program 前要显式设置。

### Transform feedback object 与 stream draw

`glGenTransformFeedbacks()`、`glBindTransformFeedback()`、`glPauseTransformFeedback()`、`glResumeTransformFeedback()`、`glDrawTransformFeedback()` 和 `glDrawTransformFeedbackStream()` 让 transform feedback 从一组松散绑定状态变为可复用对象，并支持按捕获结果直接绘制。

这适合 GPU 粒子、裁剪结果复用或可见性预处理。捕获前仍要在 link 前设置 varyings，绑定足够大的 buffer，并保证暂停/恢复与 draw 之间的 buffer 访问顺序正确。

### Indirect draw

`glDrawArraysIndirect()` 和 `glDrawElementsIndirect()` 从绑定的 indirect buffer 或客户端地址读取 draw command。它们让绘制参数可以由 CPU 批量写入，或由 GPU 前一阶段生成。

命令结构体布局必须严格匹配 OpenGL 规范。绑定 `GL_DRAW_INDIRECT_BUFFER` 时，`indirect` 是字节偏移；未绑定时才是 CPU 指针。GPU 生成命令后进入 indirect draw 前，需要保证写入对 draw command 读取可见。

### Shader subroutine 与 double uniform

Subroutine API 允许在 shader stage 内从多个已声明函数实现中选择一个：用 `glGetSubroutineIndex()`、`glGetSubroutineUniformLocation()` 查询，再用 `glUniformSubroutinesuiv()` 设置当前 stage 的选择。它适合少量算法变体，但不是替代普通 uniform 分支或多 program 架构的银弹。

`glUniform*d()`、`glUniform*dv()`、`glUniformMatrix*dv()` 和 `glGetUniformdv()` 为 GLSL double 类型服务。只有 shader 真实使用 `double`/`dvec`/`dmat` 时才需要；许多渲染数据使用 float 足够，double 可能增加带宽和 ALU 成本。

### Per-buffer blend 与 sample shading

`glBlendFunci()`、`glBlendFuncSeparatei()`、`glBlendEquationi()`、`glBlendEquationSeparatei()` 允许为不同 draw buffer 配置不同 blending。它们常用于复杂 G-buffer 或多目标合成。

`glMinSampleShading()` 影响每像素样本级 shader 执行比例，提升 MSAA 中的 shading 精度，但会增加片段成本。只有在多重采样且确实需要 per-sample shading 时才启用。

## 关键边界

### 4.0 Core 不是“自动更快”

Indirect draw、subroutine、tessellation 和 per-sample shading 都可能让架构更清晰，也可能增加同步、shader 复杂度或 GPU 成本。应围绕实际瓶颈引入，而不是只因版本更高而使用。

### Subroutine 状态按 shader stage 设置

`glUniformSubroutinesuiv()` 的 `count` 必须匹配对应 stage 的 active subroutine uniform 数量。切换 program 后，需要重新理解该 program 的 subroutine index/location，不能跨 program 复用。

### Indirect command buffer 是二进制契约

字段顺序、类型和对齐必须精确。维护跨语言或 GPU 写入 command 的代码时，应把结构定义集中，并用静态断言或测试验证大小。

## API 速查表

| 功能族（成员 API） | 是做什么的 | 使用时重点注意 |
| --- | --- | --- |
| `initializeOpenGLFunctions()` | 解析 current OpenGL 4.0 Core profile 函数。 | context 版本/profile 必须匹配；失败后不能调用成员。 |
| `glPatchParameteri`, `glPatchParameterfv` | 配置 tessellation patch 控制点数和默认细分级别。 | 仅 `GL_PATCHES` 与 tessellation shader 路径有效。 |
| `glGenTransformFeedbacks`, `glDeleteTransformFeedbacks`, `glIsTransformFeedback`, `glBindTransformFeedback`, `glPauseTransformFeedback`, `glResumeTransformFeedback`, `glDrawTransformFeedback`, `glDrawTransformFeedbackStream` | 管理 transform feedback object，并按捕获结果绘制。 | varyings 在 link 前指定；buffer 容量和暂停/恢复顺序要正确。 |
| `glBeginQueryIndexed`, `glEndQueryIndexed`, `glGetQueryIndexediv` | 对支持 indexed query 的目标按索引开始、结束和查询状态。 | target/index 组合必须合法；结果读取仍遵守 query 异步规则。 |
| `glDrawArraysIndirect`, `glDrawElementsIndirect` | 从 indirect command 结构读取绘制参数。 | 绑定 indirect buffer 时参数是 offset；命令布局必须严格匹配规范。 |
| `glGetProgramStageiv`, `glGetSubroutineIndex`, `glGetSubroutineUniformLocation`, `glGetActiveSubroutineName`, `glGetActiveSubroutineUniformName`, `glGetActiveSubroutineUniformiv`, `glGetUniformSubroutineuiv`, `glUniformSubroutinesuiv` | 查询并设置 shader subroutine。 | index/location 只对对应 program/stage 有效；count 要匹配 stage。 |
| `glUniform1d`, `glUniform2d`, `glUniform3d`, `glUniform4d`, `glUniform1dv`, `glUniform2dv`, `glUniform3dv`, `glUniform4dv`, `glUniformMatrix2dv`, `glUniformMatrix3dv`, `glUniformMatrix4dv`, `glUniformMatrix2x3dv`, `glUniformMatrix3x2dv`, `glUniformMatrix2x4dv`, `glUniformMatrix4x2dv`, `glUniformMatrix3x4dv`, `glUniformMatrix4x3dv`, `glGetUniformdv` | 设置或查询 double 标量、向量和矩阵 uniform。 | 只用于 GLSL double 类型；location 属当前 program。 |
| `glBlendFunci`, `glBlendFuncSeparatei`, `glBlendEquationi`, `glBlendEquationSeparatei` | 为单个 draw buffer 设置 blend factor/equation。 | buffer index 要小于实现限制；与 MRT attachment 格式配套验证。 |
| `glMinSampleShading` | 请求每像素至少一定比例样本执行 fragment shader。 | 只对 multisample 有意义；可能显著增加片段成本。 |
| 继承的 3.3：`glGenSamplers`, `glBindSampler`, `glSamplerParameter*`, `glVertexAttribDivisor`, `glQueryCounter`, `glGetQueryObject*i64v`, `glBindFragDataLocationIndexed`, `glVertexAttribP*` | sampler object、实例 attribute、timer query、dual-source blending 和 packed attribute。 | sampler 绑定 unit；divisor 随 VAO 保存；query 延迟读取。 |
| 继承的 3.2/3.1/3.0：`glTexImage*Multisample`, `glFenceSync`, `glDrawElementsBaseVertex`, `glFramebufferTexture`, `glDraw*Instanced`, `glTexBuffer`, `glUniformBlockBinding`, `glBindVertexArray`, `glBindFramebuffer`, `glMapBufferRange` | MSAA texture、sync、base-vertex、UBO、VAO/FBO 与 buffer range。 | 同步、binding、对齐和 FBO 完整性仍是主要边界。 |
| 继承的基础 Core：`glCreateShader`, `glCompileShader`, `glLinkProgram`, `glUseProgram`, `glVertexAttribPointer`, `glUniform*`, `glGenBuffers`, `glBufferData`, `glBindTexture`, `glTexImage*`, `glDrawArrays`, `glDrawElements`, `glViewport`, `glClear*` | GLSL、buffer、texture 和基础绘制状态。 | 无 legacy fixed-function；所有渲染语义由 shader 与资源绑定明确表达。 |

## 常见误区

### 使用 tessellation shader，却仍以 `GL_TRIANGLES` 绘制

细分阶段只处理 patch primitive。必须用 `GL_PATCHES`，并设置与 shader layout 匹配的 patch vertex 数量。

### indirect draw 的结构体字段顺序写错

这类错误通常不会在编译期暴露，而是表现为不绘制或越界绘制。把 draw command 定义集中，并确保字节布局与规范一致。

### 为每个材质都用 subroutine

Subroutine 灵活，但不一定比多 program、uniform 分支或专门 shader variant 更简单/更快。只在确实需要 stage 内函数选择时使用。

## 一句话总结

`QOpenGLFunctions_4_0_Core` 把 Qt 的桌面 GL 入口推进到 tessellation、indirect draw、subroutine 和更细粒度 MRT/MSAA 控制；它适合成熟 Core renderer 增强 GPU 驱动流程，而不是用来掩盖旧管线问题。
