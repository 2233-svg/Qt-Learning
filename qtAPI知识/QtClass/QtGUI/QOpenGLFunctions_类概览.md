# Qt QOpenGLFunctions 深入笔记

> 适用版本：Qt 6.11.1
> 头文件：`#include <QOpenGLFunctions>`
> 所属模块：`Qt6::Gui`
> 继承：无

## 它解决什么问题

`QOpenGLFunctions` 提供一组由 Qt 按当前 `QOpenGLContext` 解析好的 OpenGL 函数入口。它覆盖 OpenGL ES 2 与桌面 OpenGL 的常用公共子集，让代码不必直接处理平台差异、函数指针加载和某些头文件宏冲突。

它不是 OpenGL 状态管理器，也不会替你创建 context、shader、buffer 或 framebuffer。它只是一个“已绑定到某个 OpenGL context 能力集的函数表”。调用这些函数之前，必须让对应或兼容的 `QOpenGLContext` current，并调用过 `initializeOpenGLFunctions()`。

## 实际使用场景

- 在 `QOpenGLWidget::initializeGL()` 中初始化函数表，然后在 `paintGL()` 调用 `gl*` 函数。
- 编写兼容 OpenGL ES 2 的渲染器，避免直接依赖桌面 OpenGL 扩展加载库。
- 在 Qt 的 OpenGL context 体系中查询当前实现支持哪些基础特性。
- 写跨平台 OpenGL 教学、工具、可视化或轻量渲染代码。

如果你需要 OpenGL 3+、ES 3、debug output、compute、VAO、sampler object 等更高版本入口，使用 `QOpenGLExtraFunctions` 或版本化函数类。

## 初始化与 context 边界

有两种典型用法：

- 继承 `QOpenGLFunctions`，在 `initializeGL()` 里调用 `initializeOpenGLFunctions()`。
- 创建 `QOpenGLFunctions funcs(context)`，或从 `context->functions()` 获取。

函数表与 OpenGL context 能力有关。context 不 current 时调用 OpenGL 函数没有意义；context 被销毁后继续使用函数对象同样不安全。多个 context 共享资源不等于共享当前状态，调用前仍要确保正确 context current。

## 能力查询

`openGLFeatures()` 和 `hasOpenGLFeature()` 查询当前函数表认为可用的基础能力，例如 shader、buffer、framebuffer、多重纹理、压缩纹理、NPOT 纹理、多重渲染目标等。

这些能力是写兼容路径的入口，但不要把它们当成完整扩展数据库。涉及具体格式、最大尺寸、uniform 数量、FBO 附着限制等，仍要调用对应 `glGet*` 查询。

## 函数家族怎么读

`QOpenGLFunctions` 的成员名与 OpenGL C API 基本一致。理解时不要逐个背函数，而是按资源和管线阶段分组：

- 清屏和状态：`glClear*`、`glEnable`、`glDisable`、`glBlend*`、`glDepth*`、`glStencil*`。
- 纹理：`glGenTextures`、`glBindTexture`、`glTexImage2D`、`glTexSubImage2D`、`glTexParameter*`、`glGenerateMipmap`。
- buffer：`glGenBuffers`、`glBindBuffer`、`glBufferData`、`glBufferSubData`。
- shader/program：`glCreateShader`、`glShaderSource`、`glCompileShader`、`glCreateProgram`、`glAttachShader`、`glLinkProgram`、`glUseProgram`。
- uniform/attribute：`glGetUniformLocation`、`glUniform*`、`glVertexAttrib*`、`glVertexAttribPointer`。
- framebuffer/renderbuffer：`glGenFramebuffers`、`glBindFramebuffer`、`glFramebufferTexture2D`、`glCheckFramebufferStatus`。
- draw/readback：`glDrawArrays`、`glDrawElements`、`glReadPixels`。

## 常见误区

- 只包含头文件不等于函数可用；必须初始化函数表。
- 不要在没有 current context 的线程调用这些函数。
- 不要把 `QOpenGLFunctions` 当作 RAII 资源对象；OpenGL 对象生命周期仍由 glDelete 或更高层包装类管理。
- 桌面 OpenGL 上能跑的枚举和格式，不一定在 ES 2 路径可用。
- `glGetError()` 只能读取 OpenGL 错误状态，不会告诉你 Qt 函数表是否初始化正确。

## API 速查表

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造 | `QOpenGLFunctions()` | 创建未显式绑定 context 的函数对象。 | current context 存在后调用 `initializeOpenGLFunctions()`。 |
| 构造 | `QOpenGLFunctions(QOpenGLContext *context)` | 用指定 context 初始化函数表。 | context 必须有效；调用函数时仍要有合适 context current。 |
| 析构 | `~QOpenGLFunctions()` | 销毁函数表对象。 | 不删除任何 OpenGL buffer、texture、shader 等资源。 |
| 初始化 | `void initializeOpenGLFunctions()` | 按当前 context 解析函数入口。 | 一般在 `initializeGL()` 或 context current 后调用一次。 |
| 能力 | `OpenGLFeatures openGLFeatures() const` | 返回基础 OpenGL 能力标志集合。 | 用于选择兼容路径，不替代具体 `glGet*` 限制查询。 |
| 能力 | `bool hasOpenGLFeature(OpenGLFeature feature) const` | 查询某项基础能力是否可用。 | 判断 shader、buffer、FBO、NPOT 等路径前使用。 |
| 枚举 | `OpenGLFeature` / `OpenGLFeatures` | 描述 Qt 封装的基础功能特性。 | 常见值包括 `Shaders`、`Buffers`、`Framebuffers`、`CompressedTextures`、`NPOTTextures`。 |
| 纹理对象 | `glGenTextures` / `glDeleteTextures` / `glIsTexture` | 创建、删除、检查 texture name。 | texture name 属于 context share group；删除也需要合适 context。 |
| 纹理绑定 | `glBindTexture` / `glActiveTexture` | 选择纹理目标和纹理单元。 | OpenGL 全局状态，跨模块渲染要明确恢复或统一管理。 |
| 纹理数据 | `glTexImage2D` / `glTexSubImage2D` / `glCopyTexImage2D` / `glCopyTexSubImage2D` | 分配、上传或从 framebuffer 拷贝 2D 纹理数据。 | internal format、pixel format、pixel type 必须符合当前实现支持。 |
| 压缩纹理 | `glCompressedTexImage2D` / `glCompressedTexSubImage2D` | 上传压缩纹理数据。 | 依赖压缩格式扩展；imageSize 必须准确。 |
| 纹理参数 | `glTexParameterf[v]` / `glTexParameteri[v]` / `glGetTexParameter*` | 设置或读取 filter、wrap 等参数。 | 参数作用于当前绑定的 texture target。 |
| mipmap | `glGenerateMipmap` | 为当前纹理生成 mip 链。 | base level 内容和尺寸必须有效。 |
| buffer 对象 | `glGenBuffers` / `glDeleteBuffers` / `glIsBuffer` | 创建、删除、检查 buffer name。 | 对应 VBO、IBO、UBO 等基础资源。 |
| buffer 绑定 | `glBindBuffer` | 把 buffer 绑定到目标。 | 后续 `glBufferData`、vertex pointer 等读取当前绑定。 |
| buffer 数据 | `glBufferData` / `glBufferSubData` / `glGetBufferParameteriv` | 分配、更新和查询 buffer 存储。 | usage 只是优化提示，不是访问权限保证。 |
| shader 创建 | `glCreateShader` / `glDeleteShader` / `glIsShader` | 创建、删除、检查 shader 对象。 | shader object 与 program 链接后仍可按需删除引用。 |
| shader 源码 | `glShaderSource` / `glCompileShader` / `glGetShaderiv` / `glGetShaderInfoLog` / `glGetShaderSource` | 设置、编译和诊断 shader。 | 编译失败要读 info log，而不是只看返回值。 |
| program | `glCreateProgram` / `glDeleteProgram` / `glIsProgram` | 创建、删除、检查 program。 | program 是 shader 链接后的可执行管线对象。 |
| program 链接 | `glAttachShader` / `glDetachShader` / `glBindAttribLocation` / `glLinkProgram` / `glValidateProgram` / `glUseProgram` | 组装并使用 program。 | attribute location 要在 link 前绑定。 |
| program 查询 | `glGetProgramiv` / `glGetProgramInfoLog` / `glGetAttachedShaders` / `glGetActiveAttrib` / `glGetActiveUniform` | 查询链接状态、日志和反射信息。 | uniform/attribute 查询结果只对当前 program 链接状态有效。 |
| uniform 位置 | `glGetUniformLocation` | 按名称查 uniform location。 | 编译器可优化未使用 uniform，返回 -1 是正常情况。 |
| uniform 设置 | `glUniform1*` / `glUniform2*` / `glUniform3*` / `glUniform4*` / `glUniformMatrix*` | 给当前 program 写 uniform。 | 目标 program 必须已 `glUseProgram`。 |
| attribute 设置 | `glVertexAttrib*` / `glVertexAttribPointer` | 设置顶点属性常量或数组解释方式。 | pointer 相对当前 array buffer 绑定解释，容易因状态污染出错。 |
| attribute 开关 | `glEnableVertexAttribArray` / `glDisableVertexAttribArray` / `glGetVertexAttrib*` | 启用、关闭和查询顶点属性数组。 | ES 2 没有 VAO 时，属性状态要由渲染器自己维护。 |
| framebuffer | `glGenFramebuffers` / `glDeleteFramebuffers` / `glIsFramebuffer` / `glBindFramebuffer` | 管理 framebuffer object。 | 绘制目标由当前绑定 FBO 决定。 |
| framebuffer 附着 | `glFramebufferTexture2D` / `glFramebufferRenderbuffer` / `glGetFramebufferAttachmentParameteriv` | 给 FBO 附着纹理或 renderbuffer。 | 需要用 `glCheckFramebufferStatus` 验证完整性。 |
| framebuffer 状态 | `glCheckFramebufferStatus` | 检查当前 FBO 是否可渲染。 | 不完整时不能可靠绘制。 |
| renderbuffer | `glGenRenderbuffers` / `glDeleteRenderbuffers` / `glIsRenderbuffer` / `glBindRenderbuffer` / `glRenderbufferStorage` | 管理 renderbuffer 存储。 | 常用于 depth/stencil 或不可采样颜色缓冲。 |
| 清屏 | `glClear` / `glClearColor` / `glClearDepthf` / `glClearStencil` | 设置清除值并清除缓冲。 | 清除受当前 framebuffer、scissor、color mask 等状态影响。 |
| 视口裁剪 | `glViewport` / `glScissor` | 设置 NDC 到像素的映射和裁剪区域。 | resize 后通常必须更新 viewport。 |
| 深度模板 | `glDepthFunc` / `glDepthMask` / `glStencilFunc` / `glStencilMask` / `glStencilOp` / `glStencil*Separate` | 控制深度和模板测试。 | 状态持久存在，切换渲染 pass 时要显式设置。 |
| 混合 | `glBlendFunc` / `glBlendColor` / `glBlendEquation` / `glBlendFuncSeparate` / `glBlendEquationSeparate` | 控制颜色混合。 | 预乘 alpha 与普通 alpha 需要不同 blend 参数。 |
| 光栅状态 | `glEnable` / `glDisable` / `glIsEnabled` / `glCullFace` / `glFrontFace` / `glLineWidth` / `glPolygonOffset` / `glSampleCoverage` | 控制管线开关和光栅化细节。 | OpenGL 状态全局持久，避免依赖默认值。 |
| 绘制 | `glDrawArrays` / `glDrawElements` | 发起非索引或索引绘制。 | 当前 program、buffer、attribute、FBO 状态都必须已准备好。 |
| 读回 | `glReadPixels` | 从当前 framebuffer 读取像素。 | 同步成本高；格式和 pack alignment 要正确。 |
| 查询 | `glGetBooleanv` / `glGetFloatv` / `glGetIntegerv` / `glGetString` / `glGetError` | 查询 OpenGL 状态、实现信息和错误。 | `glGet*` 可能较慢，不适合热路径频繁调用。 |
| 同步 | `glFlush` / `glFinish` | 提交或等待 OpenGL 命令。 | `glFinish` 会强同步，通常只用于诊断或资源交接边界。 |
| 杂项 | `glHint` / `glPixelStorei` / `glReleaseShaderCompiler` / `glShaderBinary` / `glGetShaderPrecisionFormat` | 配置提示、像素打包、shader 编译器和精度查询。 | 像素上传前尤其注意 `glPixelStorei` 的 pack/unpack alignment。 |

## 一句话总结

`QOpenGLFunctions` 是 Qt 给当前 OpenGL context 准备好的基础函数表：先初始化，再按 OpenGL 状态机规则使用，资源生命周期仍由你负责。
