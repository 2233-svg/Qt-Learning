# QOpenGLFunctions_4_1_Core 类笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QOpenGLFunctions_4_1_Core>`  
> 所属模块：`Qt6::OpenGL`  
> 继承：`QAbstractOpenGLFunctions`  
> 可用性：桌面 OpenGL 4.1 Core profile；不包含 Compatibility/fixed-function API

## 它解决什么问题

`QOpenGLFunctions_4_1_Core` 为 Qt 程序提供 OpenGL 4.1 Core profile 的函数入口。4.1 的重点不是再增加一种绘制 primitive，而是让大型 renderer 的 shader 和 viewport 组织更模块化：separable program 与 program pipeline、直接写指定 program 的 uniform、viewport/scissor/depth range 数组、shader/program binary、双精度 vertex attribute 都进入 core。

它适合需要拆分 shader stage、管理多个 viewport、复用 program binary 或把 uniform 更新从当前 `glUseProgram()` 状态中解耦的桌面渲染器。若项目仍依赖 `glBegin()`、矩阵栈或固定光照，应使用 Compatibility 版作为迁移桥，而不是在 Core 版中寻找这些入口。

## 实际使用场景

- 将 vertex、fragment、geometry、tessellation stage 作为 separable program 组合进 program pipeline；
- 对多个 viewport/scissor/depth range 做一次 draw 的分层输出准备；
- 不绑定 program 就用 `glProgramUniform*()` 更新其 uniform；
- 保存/加载 program binary，减少启动期 shader 编译开销；
- 需要 `double` 顶点属性或跨桌面/ES 风格的 shader precision 查询。

## 初始化与最小示例

```cpp
#include <QOpenGLFunctions_4_1_Core>

QOpenGLFunctions_4_1_Core gl;

bool initializePipeline(GLuint vertexProgram, GLuint fragmentProgram)
{
    if (!gl.initializeOpenGLFunctions())
        return false;

    GLuint pipeline = 0;
    gl.glGenProgramPipelines(1, &pipeline);
    gl.glUseProgramStages(pipeline, GL_VERTEX_SHADER_BIT, vertexProgram);
    gl.glUseProgramStages(pipeline, GL_FRAGMENT_SHADER_BIT, fragmentProgram);
    gl.glBindProgramPipeline(pipeline);
    return true;
}
```

Pipeline 模型要求 program 以 separable 方式创建或设置 `GL_PROGRAM_SEPARABLE` 后链接。传统 monolithic program 仍可使用，但不能直接当作任意 stage 塞进 pipeline。

## 4.1 Core 的关键能力

### Program pipeline 与 separable program

`glProgramParameteri(program, GL_PROGRAM_SEPARABLE, GL_TRUE)` 使 program 可分离；`glCreateShaderProgramv()` 可从单个 stage 源码快速创建 separable program；`glGenProgramPipelines()`、`glBindProgramPipeline()`、`glUseProgramStages()`、`glActiveShaderProgram()` 负责组合和激活 pipeline。

pipeline 的链接/验证问题与传统 program 不同。`glValidateProgramPipeline()` 和 `glGetProgramPipelineInfoLog()` 用于检查 stage 组合是否能一起工作。各 stage interface、varying、输出输入匹配仍然需要你设计清楚。

### Direct program uniform

`glProgramUniform*()` 直接向指定 program 写 uniform，不要求该 program 当前被 `glUseProgram()` 绑定。这减少了状态切换，也让资源更新系统可以按 program 对象组织。

location 仍来自目标 program，relink 后仍需重新查询。`glProgramUniform*()` 不会自动验证你传的 location 属于哪个 program；缓存时必须以 program 为键。

### Viewport/scissor/depth range array

`glViewportArrayv()`、`glViewportIndexedf()`、`glScissorArrayv()`、`glScissorIndexed()`、`glDepthRangeArrayv()`、`glDepthRangeIndexed()` 让多个 viewport 相关状态同时存在。结合 geometry shader 或 later viewport index 输出，可用于多视图、层渲染、立方体贴图面等工作流。

数组 index 受 `GL_MAX_VIEWPORTS` 限制。viewport、scissor、depth range 是三组相关但独立的 indexed state；只设置 viewport 不会自动设置 scissor。

### Program binary 与 shader binary

`glGetProgramBinary()`/`glProgramBinary()` 保存和恢复已链接 program 的实现相关二进制；`glShaderBinary()`、`glReleaseShaderCompiler()` 面向 shader binary/编译器资源管理。二进制格式与驱动、硬件、版本高度相关，不适合作为跨机器资产格式。

实际使用时必须保存 `binaryFormat`、驱动/版本特征和失败 fallback。加载失败时重新从 GLSL 编译，而不是把缓存当成唯一来源。

### Double attribute 与 float depth helpers

`glVertexAttribLPointer()` 与 `glVertexAttribL*d[v]()` 服务 `double`/`dvec` 顶点属性。`glClearDepthf()`、`glDepthRangef()` 和 `glGetShaderPrecisionFormat()` 与 OpenGL ES 兼容风格相关，在跨 API 抽象层中有价值。

double attribute 成本高，且只在 shader 真正需要双精度输入时使用。多数渲染属性仍应使用 float 或压缩格式。

## 关键边界

### Pipeline 不等于“随便拼 shader”

各 stage 的 interface、版本、layout、资源限制和 separable 设置都必须匹配。pipeline 验证失败时读 info log，不要只检查单个 program 的 link status。

### Direct uniform 不绕过 program 生命周期

它只是省掉 `glUseProgram()`，并不让 location 变成全局编号，也不允许向未链接或已删除 program 写入可靠数据。

### Program binary 是缓存，不是发布格式

驱动更新后缓存可能失效。必须有源码重新编译路径，并把二进制缓存视为性能优化。

## API 速查表

| 功能族（成员 API） | 是做什么的 | 使用时重点注意 |
| --- | --- | --- |
| `initializeOpenGLFunctions()` | 解析 current OpenGL 4.1 Core profile 函数。 | context 版本/profile 必须匹配；失败后不能调用成员。 |
| `glGenProgramPipelines`, `glDeleteProgramPipelines`, `glIsProgramPipeline`, `glBindProgramPipeline`, `glUseProgramStages`, `glActiveShaderProgram`, `glCreateShaderProgramv`, `glProgramParameteri`, `glValidateProgramPipeline`, `glGetProgramPipelineiv`, `glGetProgramPipelineInfoLog` | 创建、组合、绑定和验证 separable program pipeline。 | program 需 separable；stage interface 不匹配时读 pipeline log。 |
| `glProgramUniform1i`, `glProgramUniform2i`, `glProgramUniform3i`, `glProgramUniform4i`, `glProgramUniform1ui`, `glProgramUniform2ui`, `glProgramUniform3ui`, `glProgramUniform4ui`, `glProgramUniform1f`, `glProgramUniform2f`, `glProgramUniform3f`, `glProgramUniform4f`, `glProgramUniform1d`, `glProgramUniform2d`, `glProgramUniform3d`, `glProgramUniform4d` | 直接向指定 program 写标量/向量 uniform。 | location 仍属于该 program；relink 后重新查询。 |
| `glProgramUniform1iv`, `glProgramUniform2iv`, `glProgramUniform3iv`, `glProgramUniform4iv`, `glProgramUniform1uiv`, `glProgramUniform2uiv`, `glProgramUniform3uiv`, `glProgramUniform4uiv`, `glProgramUniform1fv`, `glProgramUniform2fv`, `glProgramUniform3fv`, `glProgramUniform4fv`, `glProgramUniform1dv`, `glProgramUniform2dv`, `glProgramUniform3dv`, `glProgramUniform4dv` | 直接向指定 program 写数组 uniform。 | `count` 是向量个数，不是基础元素个数。 |
| `glProgramUniformMatrix2fv`, `glProgramUniformMatrix3fv`, `glProgramUniformMatrix4fv`, `glProgramUniformMatrix2x3fv`, `glProgramUniformMatrix3x2fv`, `glProgramUniformMatrix2x4fv`, `glProgramUniformMatrix4x2fv`, `glProgramUniformMatrix3x4fv`, `glProgramUniformMatrix4x3fv`, `glProgramUniformMatrix2dv`, `glProgramUniformMatrix3dv`, `glProgramUniformMatrix4dv`, `glProgramUniformMatrix2x3dv`, `glProgramUniformMatrix3x2dv`, `glProgramUniformMatrix2x4dv`, `glProgramUniformMatrix4x2dv`, `glProgramUniformMatrix3x4dv`, `glProgramUniformMatrix4x3dv` | 直接写 float/double 方阵与非方阵矩阵 uniform。 | 默认 column-major；非方阵名称是列 x 行。 |
| `glViewportArrayv`, `glViewportIndexedf`, `glViewportIndexedfv`, `glScissorArrayv`, `glScissorIndexed`, `glScissorIndexedv`, `glDepthRangeArrayv`, `glDepthRangeIndexed`, `glGetFloati_v`, `glGetDoublei_v` | 配置/查询 indexed viewport、scissor 和 depth range。 | index 受 `GL_MAX_VIEWPORTS` 限制；三组状态互不自动同步。 |
| `glVertexAttribL1d`, `glVertexAttribL2d`, `glVertexAttribL3d`, `glVertexAttribL4d`, `glVertexAttribL1dv`, `glVertexAttribL2dv`, `glVertexAttribL3dv`, `glVertexAttribL4dv`, `glVertexAttribLPointer`, `glGetVertexAttribLdv` | 设置/定义/查询 double 类型顶点 attribute。 | 用于 GLSL `double`/`dvec` 输入；成本高于 float。 |
| `glProgramBinary`, `glGetProgramBinary`, `glShaderBinary`, `glReleaseShaderCompiler`, `glGetShaderPrecisionFormat` | 管理 program/shader binary 与 shader 精度查询。 | binary 是驱动相关缓存；必须保留源码编译 fallback。 |
| `glClearDepthf`, `glDepthRangef` | 使用 float 参数设置 depth clear/range。 | 便于与 ES 风格抽象统一；语义仍是当前 context depth state。 |
| 继承的 4.0：`glPatchParameter*`, `glDraw*Indirect`, `glGenTransformFeedbacks`, `glBindTransformFeedback`, `glDrawTransformFeedback*`, `glUniform*d*`, `glBlend*i`, `glMinSampleShading`, `glUniformSubroutinesuiv` | tessellation、indirect draw、transform feedback object、double uniform、per-buffer blend 与 subroutine。 | 这些功能各有严格状态/布局要求，不自动提升性能。 |
| 继承的 3.x Core：`glGenSamplers`, `glBindSampler`, `glVertexAttribDivisor`, `glFenceSync`, `glTexImage*Multisample`, `glUniformBlockBinding`, `glBindVertexArray`, `glBindFramebuffer`, `glMapBufferRange` | sampler、实例化、sync、MSAA texture、UBO、VAO/FBO。 | 仍需管理 binding、同步、对齐和 FBO completeness。 |

## 常见误区

### 把非 separable program 放进 pipeline

传统 link 成功不代表可以被 pipeline 分 stage 使用。创建或链接前要设置 `GL_PROGRAM_SEPARABLE`，并验证 pipeline。

### `glProgramUniform*()` 用了另一个 program 的 location

location 不是全局句柄。把 location 缓存和 program ID 绑定在一起，relink 后更新缓存。

### 把 program binary 当作跨机器发布资源

它通常只适合本机缓存。驱动、GPU、版本变化后可能失效；加载失败必须回退到 GLSL 编译。

## 一句话总结

`QOpenGLFunctions_4_1_Core` 让 Qt renderer 可以用 program pipeline、direct uniform 和 viewport array 组织更大的 Core 渲染系统；核心收益是降低状态耦合，但前提是把 program 生命周期、pipeline interface 和二进制缓存边界管理清楚。
