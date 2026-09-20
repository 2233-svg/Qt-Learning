# QOpenGLFunctions_4_1_Compatibility 类笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QOpenGLFunctions_4_1_Compatibility>`  
> 所属模块：`Qt6::OpenGL`  
> 继承：`QAbstractOpenGLFunctions`  
> 可用性：桌面 OpenGL 4.1 Compatibility profile；包含 4.1 Core API 与旧 fixed-function/legacy 接口

## 它解决什么问题

`QOpenGLFunctions_4_1_Compatibility` 让 Qt 程序在 OpenGL 4.1 Compatibility context 中同时访问 program pipeline、direct program uniform、viewport array、program binary 等 4.1 现代能力，以及 `glBegin()`、矩阵栈、固定光照、client array、display list 等历史接口。

它的价值在于迁移：旧项目可以逐步把渲染系统拆成 separable program、VAO/FBO、UBO 和 sampler object，同时让暂时不能重写的固定管线模块继续工作。它不应成为新代码继续扩展 fixed-function 的理由。

## 实际使用场景

- 老式桌面应用需要保留部分 Compatibility 绘制，同时新渲染 pass 使用 program pipeline；
- 插件体系中既有旧 GL 插件，也有新 Core 风格插件，需要在同一 Qt context 策略下管理；
- 迁移大型 renderer 时，先把 uniform 更新改成 `glProgramUniform*()`，减少对 `glUseProgram()` 的隐式依赖；
- 为多视口或分层渲染加入 viewport/scissor/depth range array，但仍保留旧 UI overlay。

## 初始化与隔离策略

```cpp
#include <QOpenGLFunctions_4_1_Compatibility>

QOpenGLFunctions_4_1_Compatibility gl;

bool initializeCompatibilityPipeline()
{
    if (!gl.initializeOpenGLFunctions())
        return false;

    GLuint pipeline = 0;
    gl.glGenProgramPipelines(1, &pipeline);
    gl.glBindProgramPipeline(pipeline);
    return true;
}
```

在 Compatibility profile 下，旧状态和新状态共享一个 context。建议把旧接口集中在少量文件，并为新路径建立“只使用 Core 子集”的约束；每个 pass 进入时显式设置 viewport、scissor、program/pipeline、VAO、FBO、blend/depth/stencil 和 texture/sampler 状态。

## 4.1 能力如何帮助旧项目迁移

### Program pipeline

`glProgramParameteri()`、`glCreateShaderProgramv()`、`glUseProgramStages()` 和 `glBindProgramPipeline()` 让 shader stage 可分离组合。旧项目可逐步将固定管线光照、材质、纹理环境替换为独立 fragment/vertex shader stage，而不必一次性重建所有 program 组合。

### Direct program uniform

`glProgramUniform*()` 直接写目标 program，适合将旧的“绑定 program 后到处写 uniform”改造成集中资源更新。这样做能减少 Compatibility context 中全局状态带来的串扰。

### Viewport array 与 program binary

viewport/scissor/depth range array 有助于多视图、cubemap、分屏和层渲染。program binary 可以改善启动期 shader 编译成本，但只能作为本机缓存；Compatibility 项目尤其要保留源码编译 fallback，因为驱动环境更不可控。

## Compatibility 边界

### Program pipeline 不会隔离旧 fixed-function 状态

pipeline 只管理 shader stage 组合。旧路径留下的 blend、depth、stencil、pixel store、active texture、buffer binding 和 FBO 状态仍会影响新路径。

### 4.1 不让 legacy API 变得现代

display list、selection、imaging subset、固定光照和矩阵栈依旧不可移植到 Core/ES。它们应被视为要替换的旧模块。

### Binary cache 不能替代源码

驱动更新、GPU 变化或 profile 差异都可能让 program binary 失效。旧项目引入二进制缓存时，一定要保留 GLSL 源码编译、日志和 fallback。

## API 速查表

| 功能族（成员 API） | 是做什么的 | 使用时重点注意 |
| --- | --- | --- |
| `initializeOpenGLFunctions()` | 解析 current 4.1 Compatibility profile 函数。 | profile 必须匹配；失败后不能调用成员。 |
| 4.1 pipeline：`glGenProgramPipelines`, `glDeleteProgramPipelines`, `glIsProgramPipeline`, `glBindProgramPipeline`, `glUseProgramStages`, `glActiveShaderProgram`, `glCreateShaderProgramv`, `glProgramParameteri`, `glValidateProgramPipeline`, `glGetProgramPipelineiv`, `glGetProgramPipelineInfoLog` | 管理 separable program pipeline。 | program 要 separable；stage interface 需验证。 |
| 4.1 direct uniform：`glProgramUniform1*`, `glProgramUniform2*`, `glProgramUniform3*`, `glProgramUniform4*`, `glProgramUniformMatrix*` | 不绑定 program，直接写指定 program 的 uniform。 | location 仍归属该 program；relink 后重新查询。 |
| 4.1 viewport array：`glViewportArrayv`, `glViewportIndexedf`, `glViewportIndexedfv`, `glScissorArrayv`, `glScissorIndexed`, `glScissorIndexedv`, `glDepthRangeArrayv`, `glDepthRangeIndexed`, `glGetFloati_v`, `glGetDoublei_v` | 配置/查询多 viewport、scissor 和 depth range。 | index 受 `GL_MAX_VIEWPORTS` 限制；三组状态独立。 |
| 4.1 double attrib/binary：`glVertexAttribL*`, `glVertexAttribLPointer`, `glGetVertexAttribLdv`, `glProgramBinary`, `glGetProgramBinary`, `glShaderBinary`, `glReleaseShaderCompiler`, `glGetShaderPrecisionFormat`, `glClearDepthf`, `glDepthRangef` | 双精度 attribute、program/shader binary 与 ES 风格辅助。 | binary 是缓存；double attribute 成本高。 |
| 继承的现代 Core 子集：`glPatchParameter*`, `glDraw*Indirect`, `glGenTransformFeedbacks`, `glBlend*i`, `glMinSampleShading`, `glGenSamplers`, `glVertexAttribDivisor`, `glFenceSync`, `glUniformBlockBinding`, `glBindVertexArray`, `glBindFramebuffer`, `glCreateShader`, `glUseProgram` | tessellation、indirect draw、sampler、instancing、sync、UBO、VAO/FBO 和 GLSL。 | 新代码优先使用这一组，保持可迁移到 Core。 |
| legacy 几何/矩阵：`glBegin`, `glEnd`, `glVertex*`, `glColor*`, `glNormal*`, `glTexCoord*`, `glMatrixMode`, `glLoad*`, `glMultMatrix*`, `glTranslate*`, `glRotate*`, `glScale*` | 立即模式和固定矩阵栈。 | 仅用于旧模块；新代码用 VBO/VAO 与 shader uniform。 |
| legacy 光照/像素/显示列表：`glLight*`, `glMaterial*`, `glFog*`, `glTexEnv*`, `glTexGen*`, `glVertexPointer`, `glEnableClientState`, `glDrawPixels`, `glColorTable*`, `glConvolution*`, `glNewList`, `glCallList*`, `glSelectBuffer`, `glFeedbackBuffer` | 固定管线、client arrays、imaging、display list 与反馈模式。 | 不适用于 Core/ES；会带来隐式状态和同步成本。 |

## 常见误区

### 用 pipeline 后以为旧状态不会影响新 pass

pipeline 只替换 shader program 组合，不会重置 framebuffer、texture、pixel store 或 blend/depth/stencil。新 pass 必须设置完整所需状态。

### 在新代码里继续写矩阵栈

Compatibility 允许这样做，但会阻断迁移。新 shader 代码应该使用 uniform/UBO/SSBO 等现代数据路径。

### Program binary 失败后没有 fallback

二进制缓存失效很常见。没有源码 fallback 的渲染器会在驱动更新后突然无法启动。

## 一句话总结

`QOpenGLFunctions_4_1_Compatibility` 是旧 Qt OpenGL 项目引入 program pipeline 和 direct uniform 的过渡层；它能降低新路径的状态耦合，但只有把 legacy 调用隔离起来，才不会继续被 fixed-function 状态机拖住。
