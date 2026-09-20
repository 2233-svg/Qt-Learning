# QOpenGLFunctions_4_0_Compatibility 类笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QOpenGLFunctions_4_0_Compatibility>`  
> 所属模块：`Qt6::OpenGL`  
> 继承：`QAbstractOpenGLFunctions`  
> 可用性：桌面 OpenGL 4.0 Compatibility profile；同时包含 4.0 Core API 与旧 fixed-function/legacy 接口

## 它解决什么问题

`QOpenGLFunctions_4_0_Compatibility` 让 Qt 程序在 OpenGL 4.0 Compatibility context 中同时访问现代 4.0 能力和历史 OpenGL 接口。它可以让一个旧 renderer 保留 `glBegin()`、矩阵栈、固定光照、display list、client array 等路径，同时逐步加入 tessellation、indirect draw、transform feedback object、sampler object 和 sync fence。

这类对象最适合“旧系统迁移期”。它不是给新代码使用 fixed-function 的理由；相反，它应该帮助你把旧代码圈起来，再把新功能写成 Core 子集，最终切换到 `QOpenGLFunctions_4_0_Core` 或更低的 3.3 Core 基线。

## 实际使用场景

- 维护历史 CAD/可视化软件，其中部分模块仍依赖 display list 或矩阵栈；
- 旧 renderer 需要加入 GPU 计时、transform feedback 或 tessellation，但短期不能重写全部绘制；
- 在迁移过程中用 Compatibility profile 对比旧路径和新 Core 路径的画面/性能；
- 为插件系统保留旧接口，同时要求新插件只走 shader/VBO/FBO。

## 初始化与隔离方式

```cpp
#include <QOpenGLFunctions_4_0_Compatibility>

QOpenGLFunctions_4_0_Compatibility gl;

bool initializeBridge()
{
    if (!gl.initializeOpenGLFunctions())
        return false;

    gl.glPatchParameteri(GL_PATCH_VERTICES, 3);
    return true;
}
```

Compatibility context 必须明确创建成功。建议在代码结构上区分 `LegacyGL` 和 `CoreGL`：旧模块可以暂时使用 fixed-function，新模块只允许使用 shader、buffer、VAO/FBO、sampler、UBO 等现代 API。

## 4.0 能力怎样帮助迁移

### Tessellation 与 indirect draw

`glPatchParameteri()`/`glPatchParameterfv()` 打开 tessellation patch 工作流；`glDrawArraysIndirect()`/`glDrawElementsIndirect()` 让 draw 参数来自 command buffer。它们适合新渲染路径，不应与旧矩阵栈和固定光照绑定在一起。

### Transform feedback object

`glGenTransformFeedbacks()`、`glBindTransformFeedback()`、`glPauseTransformFeedback()`、`glResumeTransformFeedback()`、`glDrawTransformFeedback()` 让 GPU 生成/捕获的数据更容易被复用。旧项目可先把 CPU 生成的粒子或可见列表逐步迁移到 GPU。

### Subroutine、double uniform 与 per-buffer blend

Subroutine API 用于 shader stage 内函数选择；double uniform 处理需要双精度的 GLSL 数据；`glBlendFunci()` 等 per-buffer blending 让多渲染目标合成更精确。这些都属于 shader/FBO 现代路径，对 fixed-function 部分没有直接帮助。

## Compatibility 边界

### 新旧状态共享同一个 context

Compatibility profile 的风险在于全局状态非常多。旧代码可能留下 matrix mode、client state、active texture、pixel store、blend/stencil、display list side effect 等状态，影响后续 Core 绘制。每个阶段进入时都应显式设置所需状态。

### 4.0 版本号不提升 legacy API 的可移植性

`glBegin()`、selection、feedback、fixed lighting、imaging subset 仍然不适用于 Core profile、OpenGL ES 或许多现代部署约束。它们只是“还可用”，不是“推荐继续扩展”。

### Tessellation/indirect draw 需要现代 shader 资源模型

把它们塞进旧 fixed-function 代码旁边会制造更难维护的混合路径。更健康的做法是让这些能力成为新 renderer 的一部分，并逐步替代旧模块。

## API 速查表

| 功能族（成员 API） | 是做什么的 | 使用时重点注意 |
| --- | --- | --- |
| `initializeOpenGLFunctions()` | 解析 current 4.0 Compatibility profile 函数。 | profile 必须匹配；失败后不得调用成员。 |
| 4.0 tessellation：`glPatchParameteri`, `glPatchParameterfv` | 设置 patch 控制点数和默认细分 level。 | 仅 `GL_PATCHES` + tessellation shader 有意义。 |
| 4.0 transform feedback：`glGenTransformFeedbacks`, `glDeleteTransformFeedbacks`, `glIsTransformFeedback`, `glBindTransformFeedback`, `glPauseTransformFeedback`, `glResumeTransformFeedback`, `glDrawTransformFeedback`, `glDrawTransformFeedbackStream` | 管理 transform feedback object 并重放捕获结果。 | varyings 在 link 前设置；buffer 容量和访问顺序要正确。 |
| 4.0 indexed query：`glBeginQueryIndexed`, `glEndQueryIndexed`, `glGetQueryIndexediv` | 按 index 管理 query target。 | 查询结果仍是异步，避免立即阻塞读取。 |
| 4.0 subroutine：`glGetProgramStageiv`, `glGetSubroutineIndex`, `glGetSubroutineUniformLocation`, `glGetActiveSubroutineName`, `glGetActiveSubroutineUniformName`, `glGetActiveSubroutineUniformiv`, `glGetUniformSubroutineuiv`, `glUniformSubroutinesuiv` | 查询并选择 shader stage 内 subroutine 实现。 | program/stage 相关；切换 program 后不能复用旧 index/location。 |
| 4.0 double uniform：`glUniform1d`, `glUniform2d`, `glUniform3d`, `glUniform4d`, `glUniform*dv`, `glUniformMatrix*dv`, `glGetUniformdv` | 上传/查询 GLSL double 标量、向量和矩阵。 | 只对 double 类型 uniform 合适；成本高于 float。 |
| 4.0 indirect/per-buffer：`glDrawArraysIndirect`, `glDrawElementsIndirect`, `glBlendFunci`, `glBlendFuncSeparatei`, `glBlendEquationi`, `glBlendEquationSeparatei`, `glMinSampleShading` | command-buffer 绘制、逐 draw-buffer 混合和 sample shading。 | indirect command 布局必须精确；sample shading 增加片段成本。 |
| 继承的现代 Core 子集：`glGenSamplers`, `glBindSampler`, `glVertexAttribDivisor`, `glQueryCounter`, `glFenceSync`, `glTexImage*Multisample`, `glUniformBlockBinding`, `glBindVertexArray`, `glBindFramebuffer`, `glMapBufferRange`, `glCreateShader`, `glUseProgram` | sampler、实例化、计时、同步、UBO、VAO/FBO 和 GLSL。 | 新代码优先只使用这些能力，保持未来可切 Core。 |
| legacy 几何/矩阵：`glBegin`, `glEnd`, `glVertex*`, `glColor*`, `glNormal*`, `glTexCoord*`, `glMatrixMode`, `glLoad*`, `glMultMatrix*`, `glTranslate*`, `glRotate*`, `glScale*` | 立即模式与固定矩阵栈。 | 仅维护旧模块；迁移到 VBO/VAO + shader uniform。 |
| legacy 光照/像素/显示列表：`glLight*`, `glMaterial*`, `glFog*`, `glTexEnv*`, `glTexGen*`, `glVertexPointer`, `glEnableClientState`, `glDrawPixels`, `glColorTable*`, `glConvolution*`, `glNewList`, `glCallList*`, `glSelectBuffer`, `glFeedbackBuffer` | 固定管线、client arrays、imaging、display list 和反馈模式。 | 不适用于 Core/ES；状态污染和同步开销都很高。 |

## 常见误区

### 用 4.0 Compatibility 新写 fixed-function 功能

这会把项目锁死在不可移植路径上。新功能应使用 shader、VAO/VBO、FBO 和现代 texture/sampler。

### 把 indirect draw command 当成普通 C++ 对象随意布局

只要结构字段或对齐不符合规范，GPU 读取的命令就是错的。必须集中定义 command 格式，并验证大小。

### 旧路径和新路径之间不清状态

Compatibility 中最难的问题往往不是 API 不存在，而是隐式状态太多。让每个 pass 自己设置完整状态，少依赖“前一个 pass 已经设好了”。

## 一句话总结

`QOpenGLFunctions_4_0_Compatibility` 是旧桌面 GL 代码迈向 4.0 能力的过渡层；它能让遗留路径继续运行，但真正值得新增的功能都应写成 Core 风格，并逐步把 fixed-function 代码移出主渲染链。
