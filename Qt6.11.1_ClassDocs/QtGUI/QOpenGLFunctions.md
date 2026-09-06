# QOpenGLFunctions

> Qt 6.11.1 · Qt GUI

## 1. 先建立直觉

**一句话定位：** 这是 GUI 基础类型，常用于绘制、输入、图像、字体或窗口系统集成。

**模块背景：** Qt GUI 负责窗口系统集成、绘制、颜色、字体、图像、输入事件和底层 GUI 资源。

### 这是什么

`QOpenGLFunctions` 是 Qt 类型机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 这个类的行为由它的继承关系、构造参数、公开状态和成员函数协议共同决定。使用时要把创建、配置、核心操作、结果/通知和清理看成一条闭环，而不是孤立调用某个函数。

**适用场景：** 围绕这个类的核心职责建立最小闭环：准备依赖 -> 创建/取得对象 -> 设置必要配置 -> 调用核心 API -> 检查返回值和状态 -> 处理结果/错误 -> 结束时清理。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要忽略构造失败、空返回、默认值和版本限制；不要把异步 API 当同步 API；不要在没有确认所有权和线程的情况下保存指针或跨线程调用。

## 2. 依赖与对象关系

- 头文件：`#include <QOpenGLFunctions>`
- 继承自：未在类页中列出
- 直接派生类：QOpenGLExtraFunctions

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Gui)
target_link_libraries(mytarget PRIVATE Qt6::Gui)
```

**继承带来的规则：** 它是值类型或不直接使用 QObject 对象模型，重点放在数据语义、拷贝/移动成本和参数有效性。

### 工作机制

这个类的行为由它的继承关系、构造参数、公开状态和成员函数协议共同决定。使用时要把创建、配置、核心操作、结果/通知和清理看成一条闭环，而不是孤立调用某个函数。

### 状态、生命周期和线程

**生命周期：** 先确认对象是值类型还是 QObject 派生对象，再确定所有权、有效期、拷贝成本和销毁方式。返回的句柄、索引、reply、设备或迭代器可能有独立的有效期，不能只看 C++ 指针是否非空。

**状态与结果：** 把返回值、状态查询、错误信息和通知信号分开判断。调用成功可能只表示请求被接受，真正完成还要等待状态变化或完成信号；读取数据前先检查对象和结果是否有效。

**线程与事件循环：** 如果类型直接或间接参与 QObject、GUI、设备或异步框架，就必须确认线程归属和事件循环；值类型虽然可以复制，也要注意内部指针、共享数据和并发写入。

## 3. 直接使用

围绕这个类的核心职责建立最小闭环：准备依赖 -> 创建/取得对象 -> 设置必要配置 -> 调用核心 API -> 检查返回值和状态 -> 处理结果/错误 -> 结束时清理。 使用时通常按这个过程组织：准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 公有类型

- `enum OpenGLFeature { Multitexture, Shaders, Buffers, Framebuffers, BlendColor, …, MultipleRenderTargets }`
- `flags OpenGLFeatures`

### 公有函数

- `QOpenGLFunctions()`
- `QOpenGLFunctions(QOpenGLContext *context)`
- `~QOpenGLFunctions()`
- `void glActiveTexture(GLenum texture)`
- `void glAttachShader(GLuint program, GLuint shader)`
- `void glBindAttribLocation(GLuint program, GLuint index, const char *name)`
- `void glBindBuffer(GLenum target, GLuint buffer)`
- `void glBindFramebuffer(GLenum target, GLuint framebuffer)`
- `void glBindRenderbuffer(GLenum target, GLuint renderbuffer)`
- `void glBindTexture(GLenum target, GLuint texture)`
- `void glBlendColor(GLclampf red, GLclampf green, GLclampf blue, GLclampf alpha)`
- `void glBlendEquation(GLenum mode)`
- `void glBlendEquationSeparate(GLenum modeRGB, GLenum modeAlpha)`
- `void glBlendFunc(GLenum sfactor, GLenum dfactor)`
- `void glBlendFuncSeparate(GLenum srcRGB, GLenum dstRGB, GLenum srcAlpha, GLenum dstAlpha)`
- `void glBufferData(GLenum target, qopengl_GLsizeiptr size, const void *data, GLenum usage)`
- `void glBufferSubData(GLenum target, qopengl_GLintptr offset, qopengl_GLsizeiptr size, const void *data)`
- `GLenum glCheckFramebufferStatus(GLenum target)`
- `void glClear(GLbitfield mask)`
- `void glClearColor(GLclampf red, GLclampf green, GLclampf blue, GLclampf alpha)`
- `void glClearDepthf(GLclampf depth)`
- `void glClearStencil(GLint s)`
- `void glColorMask(GLboolean red, GLboolean green, GLboolean blue, GLboolean alpha)`
- `void glCompileShader(GLuint shader)`
- `void glCompressedTexImage2D(GLenum target, GLint level, GLenum internalformat, GLsizei width, GLsizei height, GLint border, GLsizei imageSize, const void *data)`
- `void glCompressedTexSubImage2D(GLenum target, GLint level, GLint xoffset, GLint yoffset, GLsizei width, GLsizei height, GLenum format, GLsizei imageSize, const void *data)`
- `void glCopyTexImage2D(GLenum target, GLint level, GLenum internalformat, GLint x, GLint y, GLsizei width, GLsizei height, GLint border)`
- `void glCopyTexSubImage2D(GLenum target, GLint level, GLint xoffset, GLint yoffset, GLint x, GLint y, GLsizei width, GLsizei height)`
- `GLuint glCreateProgram()`
- `GLuint glCreateShader(GLenum type)`
- `void glCullFace(GLenum mode)`
- `void glDeleteBuffers(GLsizei n, const GLuint *buffers)`
- `void glDeleteFramebuffers(GLsizei n, const GLuint *framebuffers)`
- `void glDeleteProgram(GLuint program)`
- `void glDeleteRenderbuffers(GLsizei n, const GLuint *renderbuffers)`
- `void glDeleteShader(GLuint shader)`
- `void glDeleteTextures(GLsizei n, const GLuint *textures)`
- `void glDepthFunc(GLenum func)`
- `void glDepthMask(GLboolean flag)`
- `void glDepthRangef(GLclampf zNear, GLclampf zFar)`
- `void glDetachShader(GLuint program, GLuint shader)`
- `void glDisable(GLenum cap)`
- `void glDisableVertexAttribArray(GLuint index)`
- `void glDrawArrays(GLenum mode, GLint first, GLsizei count)`
- `void glDrawElements(GLenum mode, GLsizei count, GLenum type, const GLvoid *indices)`
- `void glEnable(GLenum cap)`
- `void glEnableVertexAttribArray(GLuint index)`
- `void glFinish()`
- `void glFlush()`
- `void glFramebufferRenderbuffer(GLenum target, GLenum attachment, GLenum renderbuffertarget, GLuint renderbuffer)`
- `void glFramebufferTexture2D(GLenum target, GLenum attachment, GLenum textarget, GLuint texture, GLint level)`
- `void glFrontFace(GLenum mode)`
- `void glGenBuffers(GLsizei n, GLuint *buffers)`
- `void glGenFramebuffers(GLsizei n, GLuint *framebuffers)`
- `void glGenRenderbuffers(GLsizei n, GLuint *renderbuffers)`
- `void glGenTextures(GLsizei n, GLuint *textures)`
- `void glGenerateMipmap(GLenum target)`
- `void glGetActiveAttrib(GLuint program, GLuint index, GLsizei bufsize, GLsizei *length, GLint *size, GLenum *type, char *name)`
- `void glGetActiveUniform(GLuint program, GLuint index, GLsizei bufsize, GLsizei *length, GLint *size, GLenum *type, char *name)`
- `void glGetAttachedShaders(GLuint program, GLsizei maxcount, GLsizei *count, GLuint *shaders)`
- `GLint glGetAttribLocation(GLuint program, const char *name)`
- `void glGetBooleanv(GLenum pname, GLboolean *params)`
- `void glGetBufferParameteriv(GLenum target, GLenum pname, GLint *params)`
- `GLenum glGetError()`
- `void glGetFloatv(GLenum pname, GLfloat *params)`
- `void glGetFramebufferAttachmentParameteriv(GLenum target, GLenum attachment, GLenum pname, GLint *params)`
- `void glGetIntegerv(GLenum pname, GLint *params)`
- `void glGetProgramInfoLog(GLuint program, GLsizei bufsize, GLsizei *length, char *infolog)`
- `void glGetProgramiv(GLuint program, GLenum pname, GLint *params)`
- `void glGetRenderbufferParameteriv(GLenum target, GLenum pname, GLint *params)`
- `void glGetShaderInfoLog(GLuint shader, GLsizei bufsize, GLsizei *length, char *infolog)`
- `void glGetShaderPrecisionFormat(GLenum shadertype, GLenum precisiontype, GLint *range, GLint *precision)`
- `void glGetShaderSource(GLuint shader, GLsizei bufsize, GLsizei *length, char *source)`
- `void glGetShaderiv(GLuint shader, GLenum pname, GLint *params)`
- `const GLubyte * glGetString(GLenum name)`
- `void glGetTexParameterfv(GLenum target, GLenum pname, GLfloat *params)`
- `void glGetTexParameteriv(GLenum target, GLenum pname, GLint *params)`
- `GLint glGetUniformLocation(GLuint program, const char *name)`
- `void glGetUniformfv(GLuint program, GLint location, GLfloat *params)`
- `void glGetUniformiv(GLuint program, GLint location, GLint *params)`
- `void glGetVertexAttribPointerv(GLuint index, GLenum pname, void **pointer)`
- `void glGetVertexAttribfv(GLuint index, GLenum pname, GLfloat *params)`
- `void glGetVertexAttribiv(GLuint index, GLenum pname, GLint *params)`
- `void glHint(GLenum target, GLenum mode)`
- `GLboolean glIsBuffer(GLuint buffer)`
- `GLboolean glIsEnabled(GLenum cap)`
- `GLboolean glIsFramebuffer(GLuint framebuffer)`
- `GLboolean glIsProgram(GLuint program)`
- `GLboolean glIsRenderbuffer(GLuint renderbuffer)`
- `GLboolean glIsShader(GLuint shader)`
- `GLboolean glIsTexture(GLuint texture)`
- `void glLineWidth(GLfloat width)`
- `void glLinkProgram(GLuint program)`
- `void glPixelStorei(GLenum pname, GLint param)`
- `void glPolygonOffset(GLfloat factor, GLfloat units)`
- `void glReadPixels(GLint x, GLint y, GLsizei width, GLsizei height, GLenum format, GLenum type, GLvoid *pixels)`
- `void glReleaseShaderCompiler()`
- `void glRenderbufferStorage(GLenum target, GLenum internalformat, GLsizei width, GLsizei height)`
- `void glSampleCoverage(GLclampf value, GLboolean invert)`
- `void glScissor(GLint x, GLint y, GLsizei width, GLsizei height)`
- `void glShaderBinary(GLint n, const GLuint *shaders, GLenum binaryformat, const void *binary, GLint length)`
- `void glShaderSource(GLuint shader, GLsizei count, const char **string, const GLint *length)`
- `void glStencilFunc(GLenum func, GLint ref, GLuint mask)`
- `void glStencilFuncSeparate(GLenum face, GLenum func, GLint ref, GLuint mask)`
- `void glStencilMask(GLuint mask)`
- `void glStencilMaskSeparate(GLenum face, GLuint mask)`
- `void glStencilOp(GLenum fail, GLenum zfail, GLenum zpass)`
- `void glStencilOpSeparate(GLenum face, GLenum fail, GLenum zfail, GLenum zpass)`
- `void glTexImage2D(GLenum target, GLint level, GLint internalformat, GLsizei width, GLsizei height, GLint border, GLenum format, GLenum type, const GLvoid *pixels)`
- `void glTexParameterf(GLenum target, GLenum pname, GLfloat param)`
- `void glTexParameterfv(GLenum target, GLenum pname, const GLfloat *params)`
- `void glTexParameteri(GLenum target, GLenum pname, GLint param)`
- `void glTexParameteriv(GLenum target, GLenum pname, const GLint *params)`
- `void glTexSubImage2D(GLenum target, GLint level, GLint xoffset, GLint yoffset, GLsizei width, GLsizei height, GLenum format, GLenum type, const GLvoid *pixels)`
- `void glUniform1f(GLint location, GLfloat x)`
- `void glUniform1fv(GLint location, GLsizei count, const GLfloat *v)`
- `void glUniform1i(GLint location, GLint x)`
- `void glUniform1iv(GLint location, GLsizei count, const GLint *v)`
- `void glUniform2f(GLint location, GLfloat x, GLfloat y)`
- `void glUniform2fv(GLint location, GLsizei count, const GLfloat *v)`
- `void glUniform2i(GLint location, GLint x, GLint y)`
- `void glUniform2iv(GLint location, GLsizei count, const GLint *v)`
- `void glUniform3f(GLint location, GLfloat x, GLfloat y, GLfloat z)`
- `void glUniform3fv(GLint location, GLsizei count, const GLfloat *v)`
- `void glUniform3i(GLint location, GLint x, GLint y, GLint z)`
- `void glUniform3iv(GLint location, GLsizei count, const GLint *v)`
- `void glUniform4f(GLint location, GLfloat x, GLfloat y, GLfloat z, GLfloat w)`
- `void glUniform4fv(GLint location, GLsizei count, const GLfloat *v)`
- `void glUniform4i(GLint location, GLint x, GLint y, GLint z, GLint w)`
- `void glUniform4iv(GLint location, GLsizei count, const GLint *v)`
- `void glUniformMatrix2fv(GLint location, GLsizei count, GLboolean transpose, const GLfloat *value)`
- `void glUniformMatrix3fv(GLint location, GLsizei count, GLboolean transpose, const GLfloat *value)`
- `void glUniformMatrix4fv(GLint location, GLsizei count, GLboolean transpose, const GLfloat *value)`
- `void glUseProgram(GLuint program)`
- `void glValidateProgram(GLuint program)`
- `void glVertexAttrib1f(GLuint indx, GLfloat x)`
- `void glVertexAttrib1fv(GLuint indx, const GLfloat *values)`
- `void glVertexAttrib2f(GLuint indx, GLfloat x, GLfloat y)`
- `void glVertexAttrib2fv(GLuint indx, const GLfloat *values)`
- `void glVertexAttrib3f(GLuint indx, GLfloat x, GLfloat y, GLfloat z)`
- `void glVertexAttrib3fv(GLuint indx, const GLfloat *values)`
- `void glVertexAttrib4f(GLuint indx, GLfloat x, GLfloat y, GLfloat z, GLfloat w)`
- `void glVertexAttrib4fv(GLuint indx, const GLfloat *values)`
- `void glVertexAttribPointer(GLuint indx, GLint size, GLenum type, GLboolean normalized, GLsizei stride, const void *ptr)`
- `void glViewport(GLint x, GLint y, GLsizei width, GLsizei height)`
- `bool hasOpenGLFeature(QOpenGLFunctions::OpenGLFeature feature) const`
- `void initializeOpenGLFunctions()`
- `QOpenGLFunctions::OpenGLFeatures openGLFeatures() const`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `enum QOpenGLFunctions::OpenGLFeatureflags QOpenGLFunctions::OpenGLFeatures`

**作用与语义：**

该枚举定义了OpenGL和OpenGL ES特性，其存在可能取决于实现。
- `QOpenGLFunctions::Multitexture`：`0x0001`;`glActiveTexture()`功能可用。
- `QOpenGLFunctions::Shaders`：`0x0002`;提供着色器功能。
- `QOpenGLFunctions::Buffers`：`0x0004`;顶点和索引缓冲区功能可用。
- `QOpenGLFunctions::Framebuffers`：`0x0008`;提供帧缓冲对象函数。
- `QOpenGLFunctions::BlendColor`：`0x0010`;`glBlendColor()` 可用。
- `QOpenGLFunctions::BlendEquation`：`0x0020`;`glBlendEquation()` 有。
- `QOpenGLFunctions::BlendEquationSeparate`：`0x0040`;`glBlendEquationSeparate()` 有。
- `QOpenGLFunctions::BlendEquationAdvanced`：`0x20000`;提供高级混合方程。
- `QOpenGLFunctions::BlendFuncSeparate`：`0x0080`;`glBlendFuncSeparate()` 可用。
- `QOpenGLFunctions::BlendSubtract`：`0x0100`;支持混合减法模式。
- `QOpenGLFunctions::CompressedTextures`：`0x0200`;提供压缩纹理函数。
- `QOpenGLFunctions::Multisample`：`0x0400`;`glSampleCoverage()`功能可用。
- `QOpenGLFunctions::StencilSeparate`：`0x0800`;提供独立的模板功能。
- `QOpenGLFunctions::NPOTTextures`：`0x1000`;两种纹理的幂次均可用。
- `QOpenGLFunctions::NPOTTextureRepeat`：`0x2000`;两纹理的非幂可以用GL_REPEAT作为包裹参数。
- `QOpenGLFunctions::FixedFunctionPipeline`：`0x4000`;固定函数流水线可用。
- `QOpenGLFunctions::TextureRGFormats`：`0x8000`;提供GL_RED和GL_RG纹理格式。
- `QOpenGLFunctions::MultipleRenderTargets`：`0x10000`;帧缓冲对象可获得多色附加。
OpenGLFeatures 类型是 QFlags 的 typedef<OpenGLFeature>。它存储 OpenGLFeature 值的 OR 组合。

### `QOpenGLFunctions::QOpenGLFunctions()`

**作用与语义：**

构造一个默认函数解析器。解析器必须先调用`initializeOpenGLFunctions()`指定上下文。

### `[explicit] QOpenGLFunctions::QOpenGLFunctions(QOpenGLContext *context)`

**作用与语义：**

构造一个函数解析器 `context`。如果 `context` `nullptr`，则将为当前`QOpenGLContext`创建该解析器。
该群体中的上下文或其他上下文必须是当前的。
以这种方式构建的对象只能与`context`及其他共享其上下文一起使用。使用`initializeOpenGLFunctions()`来更改对象的上下文关联。

### `[noexcept] QOpenGLFunctions::~QOpenGLFunctions()`

**作用与语义：**

会破坏这个函数解析器。

### `void QOpenGLFunctions::glActiveTexture(GLenum texture)`

**作用与语义：**

调用 glActiveTexture（`texture`） 的便利函数。
更多信息请参见 OpenGL ES 3.X 关于 glActiveTexture() 的文档。

### `void QOpenGLFunctions::glAttachShader(GLuint program, GLuint shader)`

**作用与语义：**

调用glAttachShader（`program`， `shader`）的便利函数。
欲了解更多信息，请参阅 OpenGL ES 3.X 关于 glAttachShader() 的文档。
这个便利功能在 OpenGL ES 1.x 系统上没有任何作用。

### `void QOpenGLFunctions::glBindAttribLocation(GLuint program, GLuint index, const char *name)`

**作用与语义：**

调用glBindAttribLocation（`program`， `index`， `name`）的便利函数。
更多信息请参见 OpenGL ES 3.X 关于 glBindAttribLocation() 的文档。
这个便利功能在 OpenGL ES 1.x 系统上没有任何作用。

### `void QOpenGLFunctions::glBindBuffer(GLenum target, GLuint buffer)`

**作用与语义：**

调用glBindBuffer（`target`， `buffer`）的便利函数。
更多信息请参见 OpenGL ES 3.X 关于 glBindBuffer() 的文档。

### `void QOpenGLFunctions::glBindFramebuffer(GLenum target, GLuint framebuffer)`

**作用与语义：**

调用glBindFramebuffer（`target`， `framebuffer`）的便利函数。
注意，Qt 会将当前绑定的 `framebuffer` `QOpenGLContext` 的 0 参数转换为当前绑定的  的 defaultFrameBufferObject()。
更多信息请参见 OpenGL ES 3.X 关于 glBindFramebuffer() 的文档。

### `void QOpenGLFunctions::glBindRenderbuffer(GLenum target, GLuint renderbuffer)`

**作用与语义：**

调用glBindRenderbuffer（`target`， `renderbuffer`）的便利函数。
更多信息请参见 OpenGL ES 3.X 关于 glBindRenderbuffer() 的文档。

### `void QOpenGLFunctions::glBindTexture(GLenum target, GLuint texture)`

**作用与语义：**

调用glBindTexture（`target`， `texture`）的便利函数。
更多信息请参见 OpenGL ES 3.X 关于 glBindTexture() 的文档。

### `void QOpenGLFunctions::glBlendColor(GLclampf red, GLclampf green, GLclampf blue, GLclampf alpha)`

**作用与语义：**

调用glBlendColor（`red`， `green`， `blue`， `alpha`的便利函数）。
更多信息请参见 OpenGL ES 3.X 关于 glBlendColor() 的文档。

### `void QOpenGLFunctions::glBlendEquation(GLenum mode)`

**作用与语义：**

调用glBlendEquation（`mode`）的便利函数。
欲了解更多信息，请参阅 OpenGL ES 3.X 关于 glBlendEquation() 的文档。

### `void QOpenGLFunctions::glBlendEquationSeparate(GLenum modeRGB, GLenum modeAlpha)`

**作用与语义：**

调用glBlendEquationSeparate（`modeRGB`， `modeAlpha`）的便利函数。
更多信息请参阅 OpenGL ES 3.X 关于 glBlendEquationSeparate() 的文档。

### `void QOpenGLFunctions::glBlendFunc(GLenum sfactor, GLenum dfactor)`

**作用与语义：**

调用 glBlendFunc（`sfactor`， `dfactor`）的便利函数。
更多信息请参见 OpenGL ES 3.X 关于 glBlendFunc() 的文档。

### `void QOpenGLFunctions::glBlendFuncSeparate(GLenum srcRGB, GLenum dstRGB, GLenum srcAlpha, GLenum dstAlpha)`

**作用与语义：**

调用glBlendFuncSeparate（`srcRGB`， `dstRGB`， `srcAlpha`， `dstAlpha`）的便利函数。
更多信息请参见 OpenGL ES 3.X 关于 glBlendFuncSeparate() 的文档。

### `void QOpenGLFunctions::glBufferData(GLenum target, qopengl_GLsizeiptr size, const void *data, GLenum usage)`

**作用与语义：**

调用glBufferData（`target`， `size`， `data`， `usage`的便利函数）。
更多信息请参见 OpenGL ES 3.X 关于 glBufferData() 的文档。

### `void QOpenGLFunctions::glBufferSubData(GLenum target, qopengl_GLintptr offset, qopengl_GLsizeiptr size, const void *data)`

**作用与语义：**

调用glBufferSubData（`target`， `offset`， `size`， `data`的便利函数）。
欲了解更多信息，请参阅 OpenGL ES 3.X 关于 glBufferSubData() 的文档。

### `GLenum QOpenGLFunctions::glCheckFramebufferStatus(GLenum target)`

**作用与语义：**

调用glCheckFramebufferStatus（`target`）的便利函数。
更多信息请参见 OpenGL ES 3.X 关于 glCheckFrameBufferStatus() 的文档。

### `void QOpenGLFunctions::glClear(GLbitfield mask)`

**作用与语义：**

调用glClear（`mask`）的便利函数。
欲了解更多信息，请参阅 glClear() 的 OpenGL ES 3.X 文档。

### `void QOpenGLFunctions::glClearColor(GLclampf red, GLclampf green, GLclampf blue, GLclampf alpha)`

**作用与语义：**

调用glClearColor（`red`， `green`， `blue`， `alpha`）的便利函数。
欲了解更多信息，请参阅 OpenGL ES 3.X 关于 glClearColor() 的文档。

### `void QOpenGLFunctions::glClearDepthf(GLclampf depth)`

**作用与语义：**

方便功能，在桌面 OpenGL 系统上调用 glClearDepth（`depth`），在嵌入式 OpenGL ES 系统调用 glClearDepthf（`depth`）。
更多信息请参见 OpenGL ES 3.X 关于 glClearDepthf() 的文档。

### `void QOpenGLFunctions::glClearStencil(GLint s)`

**作用与语义：**

调用 glClearStencil（`s`） 的便利函数。
更多信息请参见 glClearStencil() 的 OpenGL ES 3.X 文档。

### `void QOpenGLFunctions::glColorMask(GLboolean red, GLboolean green, GLboolean blue, GLboolean alpha)`

**作用与语义：**

调用glColorMask（`red`， `green`， `blue`， `alpha`）的便利函数。
更多信息请参见 OpenGL ES 3.X 关于 glColorMask() 的文档。

### `void QOpenGLFunctions::glCompileShader(GLuint shader)`

**作用与语义：**

调用glCompileShader（`shader`）的便利函数。
更多信息请参见 OpenGL ES 3.X 关于 glCompileShader() 的文档。
这个便利功能在 OpenGL ES 1.x 系统上没有任何作用。

### `void QOpenGLFunctions::glCompressedTexImage2D(GLenum target, GLint level, GLenum internalformat, GLsizei width, GLsizei height, GLint border, GLsizei imageSize, const void *data)`

**作用与语义：**

调用 glComCompressedTexImage2D（`target`、`level`、`internalformat`、`width`、`height`、`border`、`imageSize`、`data`）的便利功能。
更多信息请参见 OpenGL ES 3.X 关于 glComCompressedTexImage2D() 的文档。

### `void QOpenGLFunctions::glCompressedTexSubImage2D(GLenum target, GLint level, GLint xoffset, GLint yoffset, GLsizei width, GLsizei height, GLenum format, GLsizei imageSize, const void *data)`

**作用与语义：**

方便函数调用 glCompressedTexSubImage2D（`target`， `level`， `xoffset`， `yoffset`， `width`， `height`， `format`， `imageSize`， `data`）。
欲了解更多信息，请参阅 glCompressedTexSubImage2D() 的 OpenGL ES 3.X 文档。

### `void QOpenGLFunctions::glCopyTexImage2D(GLenum target, GLint level, GLenum internalformat, GLint x, GLint y, GLsizei width, GLsizei height, GLint border)`

**作用与语义：**

调用glCopyTexImage2D（`target`、`level`、`internalformat`、`x`、`y`、`width`、`height`、`border`）的便利函数。
更多信息请参见 glCopyTexImage2D() 的 OpenGL ES 3.X 文档。

### `void QOpenGLFunctions::glCopyTexSubImage2D(GLenum target, GLint level, GLint xoffset, GLint yoffset, GLint x, GLint y, GLsizei width, GLsizei height)`

**作用与语义：**

调用glCopyTexSubImage2D（`target`、`level`、`xoffset`、`yoffset`、`x`、`y`、`width`、`height`）的便利函数。
欲了解更多信息，请参阅 OpenGL ES 3.X 关于 glCopyTexSubImage2D() 的文档。

### `GLuint QOpenGLFunctions::glCreateProgram()`

**作用与语义：**

调用 glCreateProgram() 的便利函数。
更多信息请参见 OpenGL ES 3.X 关于 glCreateProgram() 的文档。
这个便利功能在 OpenGL ES 1.x 系统上没有任何作用。

### `GLuint QOpenGLFunctions::glCreateShader(GLenum type)`

**作用与语义：**

调用glCreateShader（`type`）的便利函数。
欲了解更多信息，请参阅 OpenGL ES 3.X 关于 glCreateShader() 的文档。
这个便利功能在 OpenGL ES 1.x 系统上没有任何作用。

### `void QOpenGLFunctions::glCullFace(GLenum mode)`

**作用与语义：**

调用glCullFace（`mode`）的便利函数。
更多信息请参见 OpenGL ES 3.X 关于 glCullFace() 的文档。

### `void QOpenGLFunctions::glDeleteBuffers(GLsizei n, const GLuint *buffers)`

**作用与语义：**

调用glDeleteBuffers（`n`， `buffers`）的便利函数。
欲了解更多信息，请参见 OpenGL ES 3.X 关于 glDeleteBuffers() 的文档。

### `void QOpenGLFunctions::glDeleteFramebuffers(GLsizei n, const GLuint *framebuffers)`

**作用与语义：**

调用glDeleteFramebuffers（`n`， `framebuffers`）的便利函数。
更多信息请参见 OpenGL ES 3.X 关于 glDeleteFramebuffers() 的文档。

### `void QOpenGLFunctions::glDeleteProgram(GLuint program)`

**作用与语义：**

调用glDeleteProgram（`program`）的便利函数。
欲了解更多信息，请参阅 OpenGL ES 3.X 关于 glDeleteProgram 的文档。
这个便利功能在 OpenGL ES 1.x 系统上没有任何作用。

### `void QOpenGLFunctions::glDeleteRenderbuffers(GLsizei n, const GLuint *renderbuffers)`

**作用与语义：**

调用glDeleteRenderbuffers（`n`， `renderbuffers`）的便利函数。
更多信息请参见 OpenGL ES 3.X 关于 glDeleteRenderbuffers() 的文档。

### `void QOpenGLFunctions::glDeleteShader(GLuint shader)`

**作用与语义：**

调用 glDeleteShader（`shader`） 的便利函数。
更多信息请参见 OpenGL ES 3.X 关于 glDeleteShader() 的文档。
这个便利功能在 OpenGL ES 1.x 系统上没有任何作用。

### `void QOpenGLFunctions::glDeleteTextures(GLsizei n, const GLuint *textures)`

**作用与语义：**

调用glDeleteTextures（`n`， `textures`）的便利函数。
欲了解更多信息，请参阅 OpenGL ES 3.X 关于 glDeleteTextures() 的文档。

### `void QOpenGLFunctions::glDepthFunc(GLenum func)`

**作用与语义：**

调用 glDepthFunc（`func`） 的便利函数。
更多信息请参见 OpenGL ES 3.X 关于 glDepthFunc() 的文档。

### `void QOpenGLFunctions::glDepthMask(GLboolean flag)`

**作用与语义：**

调用glDepthMask（`flag`）的便利函数。
欲了解更多信息，请参阅 OpenGL ES 3.X 关于 glDepthMask() 的文档。

### `void QOpenGLFunctions::glDepthRangef(GLclampf zNear, GLclampf zFar)`

**作用与语义：**

方便功能，在桌面 OpenGL 系统上调用 glDepthRange（`zNear`， `zFar`），在嵌入式 OpenGL ES 系统调用 glDepthRangef（`zNear`， `zFar`）。
更多信息请参见 OpenGL ES 3.X 关于 glDepthRangef() 的文档。

### `void QOpenGLFunctions::glDetachShader(GLuint program, GLuint shader)`

**作用与语义：**

调用glDetachShader（`program`， `shader`）的便利函数。
更多信息请参见 glDetachShader() 的 OpenGL ES 3.X 文档。
这个便利功能在 OpenGL ES 1.x 系统上没有任何作用。

### `void QOpenGLFunctions::glDisable(GLenum cap)`

**作用与语义：**

调用 glDisable（`cap`） 的便利函数。
欲了解更多信息，请参阅 OpenGL ES 3.X 关于 glDisable() 的文档。

### `void QOpenGLFunctions::glDisableVertexAttribArray(GLuint index)`

**作用与语义：**

调用 glDisableVertexAttribArray（`index`） 的便利函数。
更多信息请参见 OpenGL ES 3.X 关于 glDisableVertexAttribArray() 的文档。
这个便利功能在 OpenGL ES 1.x 系统上没有任何作用。

### `void QOpenGLFunctions::glDrawArrays(GLenum mode, GLint first, GLsizei count)`

**作用与语义：**

调用glDrawArrays（`mode`， `first`， `count`）的便利函数。
欲了解更多信息，请参阅 OpenGL ES 3.X 关于 glDrawArrays() 的文档。

### `void QOpenGLFunctions::glDrawElements(GLenum mode, GLsizei count, GLenum type, const GLvoid *indices)`

**作用与语义：**

调用 glDrawElements（`mode`， `count`， `type`， `indices` 的便利函数）。
欲了解更多信息，请参阅 OpenGL ES 3.X 关于 glDrawElements() 的文档。

### `void QOpenGLFunctions::glEnable(GLenum cap)`

**作用与语义：**

调用glEnable（`cap`）的便利函数。
欲了解更多信息，请参阅 OpenGL ES 3.X 关于 glEnable() 的文档。

### `void QOpenGLFunctions::glEnableVertexAttribArray(GLuint index)`

**作用与语义：**

调用glEnableVertexAttribArray（`index`）的便利函数。
欲了解更多信息，请参阅 OpenGL ES 3.X 关于 glEnableVertexAttribArray() 的文档。
这个便利功能在 OpenGL ES 1.x 系统上没有任何作用。

### `void QOpenGLFunctions::glFinish()`

**作用与语义：**

调用 glFinish() 的便利函数。
更多信息请参见 OpenGL ES 3.X 关于 glFinish() 的文档。

### `void QOpenGLFunctions::glFlush()`

**作用与语义：**

调用glFlush()的便利函数。
更多信息请参见 glFlush() 的 OpenGL ES 3.X 文档。

### `void QOpenGLFunctions::glFramebufferRenderbuffer(GLenum target, GLenum attachment, GLenum renderbuffertarget, GLuint renderbuffer)`

**作用与语义：**

调用 glFrameBufferRenderbuffer（`target`， `attachment`， `renderbuffertarget`， `renderbuffer` 的便利函数）。
欲了解更多信息，请参阅 OpenGL ES 3.X 关于 glFrameFrameRenderbuffer() 的文档。

### `void QOpenGLFunctions::glFramebufferTexture2D(GLenum target, GLenum attachment, GLenum textarget, GLuint texture, GLint level)`

**作用与语义：**

调用 glFrameBufferTexture2D（`target`， `attachment`， `textarget`， `texture`， `level` 的便利函数）。
欲了解更多信息，请参阅 OpenGL ES 3.X 关于 glFrameFrameTexture2D() 的文档。

### `void QOpenGLFunctions::glFrontFace(GLenum mode)`

**作用与语义：**

调用 glFrontFace（`mode`） 的便利函数。
更多信息请参见 glFrontFace() 的 OpenGL ES 3.X 文档。

### `void QOpenGLFunctions::glGenBuffers(GLsizei n, GLuint *buffers)`

**作用与语义：**

调用glGenBuffers（`n`， `buffers`）的便利函数。
更多信息请参见 OpenGL ES 3.X 关于 glGenBuffers() 的文档。

### `void QOpenGLFunctions::glGenFramebuffers(GLsizei n, GLuint *framebuffers)`

**作用与语义：**

调用glGenFramebuffers（`n`， `framebuffers`）的便利函数。
欲了解更多信息，请参阅 OpenGL ES 3.X 关于 glGenFramebuffers() 的文档。

### `void QOpenGLFunctions::glGenRenderbuffers(GLsizei n, GLuint *renderbuffers)`

**作用与语义：**

调用glGenRenderbuffers（`n`， `renderbuffers`）的便利函数。
更多信息请参见 OpenGL ES 3.X 关于 glGenRenderbuffers() 的文档。

### `void QOpenGLFunctions::glGenTextures(GLsizei n, GLuint *textures)`

**作用与语义：**

调用glGenTextures（`n`， `textures`）的便利函数。
更多信息请参见 OpenGL ES 3.X 关于 glGenTextures() 的文档。

### `void QOpenGLFunctions::glGenerateMipmap(GLenum target)`

**作用与语义：**

调用 glGenerateMipmap（`target`） 的便利函数。
更多信息请参见 OpenGL ES 3.X 关于 glGenerateMipmap() 的文档。

### `void QOpenGLFunctions::glGetActiveAttrib(GLuint program, GLuint index, GLsizei bufsize, GLsizei *length, GLint *size, GLenum *type, char *name)`

**作用与语义：**

调用 glGetActiveAttrib（`program`， `index`， `bufsize`， `length`， `size`， `type`， `name` 的便利函数。
更多信息请参阅 OpenGL ES 3.X 关于 glGetActiveAttrib() 的文档。
这个便利功能在 OpenGL ES 1.x 系统上没有任何作用。

### `void QOpenGLFunctions::glGetActiveUniform(GLuint program, GLuint index, GLsizei bufsize, GLsizei *length, GLint *size, GLenum *type, char *name)`

**作用与语义：**

调用glGetActiveUniform（`program`、`index`、`bufsize`、`length`、`size`、`type`、`name`）的便利函数。
欲了解更多信息，请参阅 OpenGL ES 3.X 关于 glGetActiveUniform() 的文档。
这个便利功能在 OpenGL ES 1.x 系统上没有任何作用。

### `void QOpenGLFunctions::glGetAttachedShaders(GLuint program, GLsizei maxcount, GLsizei *count, GLuint *shaders)`

**作用与语义：**

调用glGetAttachedShaders（`program`， `maxcount`， `count`， `shaders`）的便利函数。
欲了解更多信息，请参阅 OpenGL ES 3.X 关于 glGetAttachedShaders() 的文档。
这个便利功能在 OpenGL ES 1.x 系统上没有任何作用。

### `GLint QOpenGLFunctions::glGetAttribLocation(GLuint program, const char *name)`

**作用与语义：**

调用glGetAttribLocation（`program`， `name`）的便利函数。
更多信息请参见 OpenGL ES 3.X 关于 glGetAttribLocation() 的文档。
这个便利功能在 OpenGL ES 1.x 系统上没有任何作用。

### `void QOpenGLFunctions::glGetBooleanv(GLenum pname, GLboolean *params)`

**作用与语义：**

调用glGetBooleanv（`pname`， `params`）的便利函数。
更多信息请参见 OpenGL ES 3.X 关于 glGetBooleanv() 的文档。

### `void QOpenGLFunctions::glGetBufferParameteriv(GLenum target, GLenum pname, GLint *params)`

**作用与语义：**

调用glGetBufferParameteriv（`target`， `pname`， `params`）的便利函数。
更多信息请参见 OpenGL ES 3.X 关于 glGetBufferParameteriv() 的文档。

### `GLenum QOpenGLFunctions::glGetError()`

**作用与语义：**

调用glGetError()的便利函数。
欲了解更多信息，请参阅 OpenGL ES 3.X 关于 glGetError() 的文档。

### `void QOpenGLFunctions::glGetFloatv(GLenum pname, GLfloat *params)`

**作用与语义：**

调用glGetFloatv（`pname`， `params`）的便利函数。
更多信息请参见 OpenGL ES 3.X 关于 glGetFloatv() 的文档。

### `void QOpenGLFunctions::glGetFramebufferAttachmentParameteriv(GLenum target, GLenum attachment, GLenum pname, GLint *params)`

**作用与语义：**

调用glGetFramebufferAttachmentParameteriv（`target`， `attachment`， `pname`， `params`）的便利函数。
更多信息请参见 OpenGL ES 3.X 关于 glGetFrameBufferAttachmentParameteriv() 的文档。

### `void QOpenGLFunctions::glGetIntegerv(GLenum pname, GLint *params)`

**作用与语义：**

调用glGetIntegerv（`pname`， `params`）的便利函数。
欲了解更多信息，请参阅 OpenGL ES 3.X 关于 glGetIntegerv() 的文档。

### `void QOpenGLFunctions::glGetProgramInfoLog(GLuint program, GLsizei bufsize, GLsizei *length, char *infolog)`

**作用与语义：**

调用glGetProgramInfoLog（`program`， `bufsize`， `length`， `infolog`）的便利函数。
更多信息请参见 glGetProgramInfoLog() 的 OpenGL ES 3.X 文档。
这个便利功能在 OpenGL ES 1.x 系统上没有任何作用。

### `void QOpenGLFunctions::glGetProgramiv(GLuint program, GLenum pname, GLint *params)`

**作用与语义：**

调用glGetProgramiv（`program`， `pname`， `params`）的便利函数。
欲了解更多信息，请参阅 OpenGL ES 3.X 关于 glGetProgramiv() 的文档。
这个便利功能在 OpenGL ES 1.x 系统上没有任何作用。

### `void QOpenGLFunctions::glGetRenderbufferParameteriv(GLenum target, GLenum pname, GLint *params)`

**作用与语义：**

调用glGetRenderbufferParameteriv（`target`， `pname`， `params`）的便利函数。
更多信息请参见 OpenGL ES 3.X 关于 glGetRenderbufferParameteriv() 的文档。

### `void QOpenGLFunctions::glGetShaderInfoLog(GLuint shader, GLsizei bufsize, GLsizei *length, char *infolog)`

**作用与语义：**

调用glGetShaderInfoLog（`shader`， `bufsize`， `length`， `infolog`的便利函数）。
欲了解更多信息，请参阅 OpenGL ES 3.X 关于 glGetShaderInfoLog() 的文档。
这个便利功能在 OpenGL ES 1.x 系统上没有任何作用。

### `void QOpenGLFunctions::glGetShaderPrecisionFormat(GLenum shadertype, GLenum precisiontype, GLint *range, GLint *precision)`

**作用与语义：**

调用glGetShaderPrecisionFormat（`shadertype`， `precisiontype`， `range`， `precision`）的便利函数。
欲了解更多信息，请参阅 OpenGL ES 3.X 关于 glGetShaderPrecisionFormat() 的文档。
这个便利功能在 OpenGL ES 1.x 系统上没有任何作用。

### `void QOpenGLFunctions::glGetShaderSource(GLuint shader, GLsizei bufsize, GLsizei *length, char *source)`

**作用与语义：**

调用glGetShaderSource（`shader`， `bufsize`， `length`， `source`）的便利函数。
更多信息请参见 OpenGL ES 3.X 关于 glGetShaderSource() 的文档。
这个便利功能在 OpenGL ES 1.x 系统上没有任何作用。

### `void QOpenGLFunctions::glGetShaderiv(GLuint shader, GLenum pname, GLint *params)`

**作用与语义：**

调用glGetShaderiv（`shader`， `pname`， `params`）的便利函数。
更多信息请参见 glGetShaderiv() 的 OpenGL ES 3.X 文档。
这个便利功能在 OpenGL ES 1.x 系统上没有任何作用。

### `const GLubyte *QOpenGLFunctions::glGetString(GLenum name)`

**作用与语义：**

调用glGetString（`name`）的便利函数。
更多信息请参见 OpenGL ES 3.X 关于 glGetString() 的文档。

### `void QOpenGLFunctions::glGetTexParameterfv(GLenum target, GLenum pname, GLfloat *params)`

**作用与语义：**

调用glGetTexParameterfv（`target`， `pname`， `params`）的便利函数。
更多信息请参见 OpenGL ES 3.X 关于 glGetTexParameterfv() 的文档。

### `void QOpenGLFunctions::glGetTexParameteriv(GLenum target, GLenum pname, GLint *params)`

**作用与语义：**

调用glGetTexParameteriv（`target`， `pname`， `params`）的便利函数。
更多信息请参见 OpenGL ES 3.X 关于 glGetTexParameteriv() 的文档。

### `GLint QOpenGLFunctions::glGetUniformLocation(GLuint program, const char *name)`

**作用与语义：**

调用glGetUniformLocation（`program`， `name`）的便利函数。
欲了解更多信息，请参阅 OpenGL ES 3.X 关于 glGetUniformLocation() 的文档。
这个便利功能在 OpenGL ES 1.x 系统上没有任何作用。

### `void QOpenGLFunctions::glGetUniformfv(GLuint program, GLint location, GLfloat *params)`

**作用与语义：**

调用glGetUniformfv（`program`， `location`， `params`）的便利函数。
更多信息请参见 glGetUniformfv() 的 OpenGL ES 3.X 文档。
这个便利功能在 OpenGL ES 1.x 系统上没有任何作用。

### `void QOpenGLFunctions::glGetUniformiv(GLuint program, GLint location, GLint *params)`

**作用与语义：**

调用glGetUniformiv（`program`， `location`， `params`）的便利函数。
欲了解更多信息，请参阅 OpenGL ES 3.X 关于 glGetUniformiv() 的文档。
这个便利功能在 OpenGL ES 1.x 系统上没有任何作用。

### `void QOpenGLFunctions::glGetVertexAttribPointerv(GLuint index, GLenum pname, void **pointer)`

**作用与语义：**

调用glGetVertexAttribPointerv（`index`， `pname`， `pointer`的便利函数）。
欲了解更多信息，请参阅 OpenGL ES 3.X 关于 glGetVertexAttribPointerv() 的文档。
这个便利功能在 OpenGL ES 1.x 系统上没有任何作用。

### `void QOpenGLFunctions::glGetVertexAttribfv(GLuint index, GLenum pname, GLfloat *params)`

**作用与语义：**

调用glGetVertexAttribfv（`index`， `pname`， `params`）的便利函数。
更多信息请参见 OpenGL ES 3.X 关于 glGetVertexAttribfv() 的文档。
这个便利功能在 OpenGL ES 1.x 系统上没有任何作用。

### `void QOpenGLFunctions::glGetVertexAttribiv(GLuint index, GLenum pname, GLint *params)`

**作用与语义：**

调用glGetVertexAttribiv（`index`， `pname`， `params`）的便利函数。
更多信息请参见 OpenGL ES 3.X 关于 glGetVertexAttribiv() 的文档。
这个便利功能在 OpenGL ES 1.x 系统上没有任何作用。

### `void QOpenGLFunctions::glHint(GLenum target, GLenum mode)`

**作用与语义：**

调用glHint（`target`， `mode`）的便利函数。
欲了解更多信息，请参阅 OpenGL ES 3.X 关于 glHint() 的文档。

### `GLboolean QOpenGLFunctions::glIsBuffer(GLuint buffer)`

**作用与语义：**

调用glIsBuffer（`buffer`）的便利函数。
更多信息请参见 OpenGL ES 3.X 关于 glIsBuffer() 的文档。

### `GLboolean QOpenGLFunctions::glIsEnabled(GLenum cap)`

**作用与语义：**

调用 glIsEnabled（`cap`） 的便利函数。
欲了解更多信息，请参阅 OpenGL ES 3.X 关于 glIsEnabled() 的文档。

### `GLboolean QOpenGLFunctions::glIsFramebuffer(GLuint framebuffer)`

**作用与语义：**

调用 glIsFramebuffer（`framebuffer`） 的便利函数。
欲了解更多信息，请参阅 OpenGL ES 3.X 关于 glIsFramebuffer() 的文档。

### `GLboolean QOpenGLFunctions::glIsProgram(GLuint program)`

**作用与语义：**

调用 glIsProgram（`program`） 的便利函数。
欲了解更多信息，请参阅 OpenGL ES 3.X 关于 glIsProgram 的文档。
这个便利功能在 OpenGL ES 1.x 系统上没有任何作用。

### `GLboolean QOpenGLFunctions::glIsRenderbuffer(GLuint renderbuffer)`

**作用与语义：**

调用 glIsRenderbuffer（`renderbuffer`） 的便利函数。
欲了解更多信息，请参阅 OpenGL ES 3.X 关于 glIsRenderbuffer() 的文档。

### `GLboolean QOpenGLFunctions::glIsShader(GLuint shader)`

**作用与语义：**

调用 glIsShader（`shader`） 的便利函数。
更多信息请参见 OpenGL ES 3.X 关于 glIsShader() 的文档。
这个便利功能在 OpenGL ES 1.x 系统上没有任何作用。

### `GLboolean QOpenGLFunctions::glIsTexture(GLuint texture)`

**作用与语义：**

调用 glIsTexture（`texture`） 的便利函数。
更多信息请参见 OpenGL ES 3.X 关于 glIsTexture() 的文档。

### `void QOpenGLFunctions::glLineWidth(GLfloat width)`

**作用与语义：**

调用glLineWidth（`width`）的便利函数。
更多信息请参见 OpenGL ES 3.X 关于 glLineWidth() 的文档。

### `void QOpenGLFunctions::glLinkProgram(GLuint program)`

**作用与语义：**

调用 glLinkProgram（`program`） 的便利函数。
欲了解更多信息，请参阅 OpenGL ES 3.X 关于 glLinkProgram() 的文档。
这个便利功能在 OpenGL ES 1.x 系统上没有任何作用。

### `void QOpenGLFunctions::glPixelStorei(GLenum pname, GLint param)`

**作用与语义：**

调用glPixelStorei（`pname`， `param`）的便利函数。
欲了解更多信息，请参阅 glPixelStorei() 的 OpenGL ES 3.X 文档。

### `void QOpenGLFunctions::glPolygonOffset(GLfloat factor, GLfloat units)`

**作用与语义：**

调用glPolygonOffset（`factor`， `units`）的便利函数。
更多信息请参见 OpenGL ES 3.X 关于 glPolygonOffset() 的文档。

### `void QOpenGLFunctions::glReadPixels(GLint x, GLint y, GLsizei width, GLsizei height, GLenum format, GLenum type, GLvoid *pixels)`

**作用与语义：**

调用glReadPixels（`x`、`y`、`width`、`height`、`format`、`type`、`pixels`）的便利函数。
更多信息请参见 OpenGL ES 3.X 关于 glReadPixels() 的文档。

### `void QOpenGLFunctions::glReleaseShaderCompiler()`

**作用与语义：**

调用 glReleaseShaderCompiler() 的便利函数。
更多信息请参见 OpenGL ES 3.X 关于 glReleaseShaderCompiler() 的文档。
这个便利功能在 OpenGL ES 1.x 系统上没有任何作用。

### `void QOpenGLFunctions::glRenderbufferStorage(GLenum target, GLenum internalformat, GLsizei width, GLsizei height)`

**作用与语义：**

调用glRenderbufferStorage（`target`， `internalformat`， `width`， `height`）的便利函数。
欲了解更多信息，请参阅 OpenGL ES 3.X 关于 glRenderbufferStorage() 的文档。

### `void QOpenGLFunctions::glSampleCoverage(GLclampf value, GLboolean invert)`

**作用与语义：**

调用glSampleCoverage（`value`， `invert`）的便利函数。
欲了解更多信息，请参阅 OpenGL ES 3.X 关于 glSampleCoverage() 的文档。

### `void QOpenGLFunctions::glScissor(GLint x, GLint y, GLsizei width, GLsizei height)`

**作用与语义：**

调用 glScissor（`x`， `y`， `width`， `height` 的便利函数）。
更多信息请参见 OpenGL ES 3.X 关于 glScissor() 的文档。

### `void QOpenGLFunctions::glShaderBinary(GLint n, const GLuint *shaders, GLenum binaryformat, const void *binary, GLint length)`

**作用与语义：**

调用 glShaderBinary（`n`， `shaders`， `binaryformat`， `binary`， `length` 的便利函数）。
欲了解更多信息，请参阅 OpenGL ES 3.X 关于 glShaderBinary() 的文档。
这个便利功能在 OpenGL ES 1.x 系统上没有任何作用。

### `void QOpenGLFunctions::glShaderSource(GLuint shader, GLsizei count, const char **string, const GLint *length)`

**作用与语义：**

调用glShaderSource（`shader`， `count`， `string`， `length`的便利函数）。
更多信息请参见 glShaderSource() 的 OpenGL ES 3.X 文档。
这个便利功能在 OpenGL ES 1.x 系统上没有任何作用。

### `void QOpenGLFunctions::glStencilFunc(GLenum func, GLint ref, GLuint mask)`

**作用与语义：**

调用 glStencilFunc（`func`， `ref`， `mask` 的便利函数）。
更多信息请参见 OpenGL ES 3.X 关于 glStencilFunc() 的文档。

### `void QOpenGLFunctions::glStencilFuncSeparate(GLenum face, GLenum func, GLint ref, GLuint mask)`

**作用与语义：**

调用glStencilFuncSeparate（`face`， `func`， `ref`， `mask`）的便利函数。
更多信息请参见 OpenGL ES 3.X 关于 glStencilfFuncSeparate() 的文档。

### `void QOpenGLFunctions::glStencilMask(GLuint mask)`

**作用与语义：**

调用glStencilMask（`mask`）的便利函数。
更多信息请参见 OpenGL ES 3.X 关于 glStencilMask() 的文档。

### `void QOpenGLFunctions::glStencilMaskSeparate(GLenum face, GLuint mask)`

**作用与语义：**

调用glStencilMaskSeparate（`face`， `mask`）的便利函数。
更多信息请参见 OpenGL ES 3.X 关于 glStencilMaskSeparate() 的文档。

### `void QOpenGLFunctions::glStencilOp(GLenum fail, GLenum zfail, GLenum zpass)`

**作用与语义：**

调用glStencilOp（`fail`， `zfail`， `zpass`）的便利函数。
更多信息请参见 OpenGL ES 3.X 关于 glStenciOp() 的文档。

### `void QOpenGLFunctions::glStencilOpSeparate(GLenum face, GLenum fail, GLenum zfail, GLenum zpass)`

**作用与语义：**

调用glStencilOpSeparate（`face`， `fail`， `zfail`， `zpass`的便利函数）。
更多信息请参见 OpenGL ES 3.X 关于 glStencilOpSeparate() 的文档。

### `void QOpenGLFunctions::glTexImage2D(GLenum target, GLint level, GLint internalformat, GLsizei width, GLsizei height, GLint border, GLenum format, GLenum type, const GLvoid *pixels)`

**作用与语义：**

方便函数调用glTexImage2D（`target`、`level`、`internalformat`、`width`、`height`、`border`、`format`、`type`、`pixels`）。
更多信息请参见 glTexImage2D() 的 OpenGL ES 3.X 文档。

### `void QOpenGLFunctions::glTexParameterf(GLenum target, GLenum pname, GLfloat param)`

**作用与语义：**

调用glTexParameterf（`target`， `pname`， `param`）的便利函数。
欲了解更多信息，请参阅 OpenGL ES 3.X 关于 glTexParameterf() 的文档。

### `void QOpenGLFunctions::glTexParameterfv(GLenum target, GLenum pname, const GLfloat *params)`

**作用与语义：**

调用glTexParameterfv（`target`， `pname`， `params`）的便利函数。
更多信息请参见 OpenGL ES 3.X 关于 glTexParameterfv() 的文档。

### `void QOpenGLFunctions::glTexParameteri(GLenum target, GLenum pname, GLint param)`

**作用与语义：**

调用glTexParameteri（`target`， `pname`， `param`）的便利函数。
更多信息请参见 OpenGL ES 3.X 关于 glTexParameteri() 的文档。

### `void QOpenGLFunctions::glTexParameteriv(GLenum target, GLenum pname, const GLint *params)`

**作用与语义：**

调用glTexParameteriv（`target`， `pname`， `params`）的便利函数。
更多信息请参见 OpenGL ES 3.X 关于 glTexParameteriv() 的文档。

### `void QOpenGLFunctions::glTexSubImage2D(GLenum target, GLint level, GLint xoffset, GLint yoffset, GLsizei width, GLsizei height, GLenum format, GLenum type, const GLvoid *pixels)`

**作用与语义：**

调用glTexSubImage2D（`target`、`level`、`xoffset`、`yoffset`、`width`、`height`、`format`、`type`、`pixels`）的便利函数。
更多信息请参见 OpenGL ES 3.X 关于 glTexSubImage2D() 的文档。

### `void QOpenGLFunctions::glUniform1f(GLint location, GLfloat x)`

**作用与语义：**

调用 glUniform1f（`location`， `x`） 的便利函数。
欲了解更多信息，请参阅 OpenGL ES 3.X 关于 glUniform1f() 的文档。
这个便利功能在 OpenGL ES 1.x 系统上没有任何作用。

### `void QOpenGLFunctions::glUniform1fv(GLint location, GLsizei count, const GLfloat *v)`

**作用与语义：**

调用glUniform1fv（`location`， `count`， `v`）的便利函数。
更多信息请参见 OpenGL ES 3.X 关于 glUniform1fv() 的文档。
这个便利功能在 OpenGL ES 1.x 系统上没有任何作用。

### `void QOpenGLFunctions::glUniform1i(GLint location, GLint x)`

**作用与语义：**

调用glUniform1i（`location`， `x`）的便利函数。
欲了解更多信息，请参阅 OpenGL ES 3.X 关于 glUniform1i() 的文档。
这个便利功能在 OpenGL ES 1.x 系统上没有任何作用。

### `void QOpenGLFunctions::glUniform1iv(GLint location, GLsizei count, const GLint *v)`

**作用与语义：**

调用glUniform1iv（`location`， `count`， `v`）的便利函数。
欲了解更多信息，请参阅 OpenGL ES 3.X 关于 glUniform1iv() 的文档。
这个便利功能在 OpenGL ES 1.x 系统上没有任何作用。

### `void QOpenGLFunctions::glUniform2f(GLint location, GLfloat x, GLfloat y)`

**作用与语义：**

调用 glUniform2f（`location`， `x`， `y` 的便利函数）。
更多信息请参见 OpenGL ES 3.X 关于 glUniform2f() 的文档。
这个便利功能在 OpenGL ES 1.x 系统上没有任何作用。

### `void QOpenGLFunctions::glUniform2fv(GLint location, GLsizei count, const GLfloat *v)`

**作用与语义：**

调用glUniform2fv（`location`， `count`， `v`）的便利函数。
更多信息请参见 glUniform2fv() 的 OpenGL ES 3.X 文档。
这个便利功能在 OpenGL ES 1.x 系统上没有任何作用。

### `void QOpenGLFunctions::glUniform2i(GLint location, GLint x, GLint y)`

**作用与语义：**

调用glUniform2i（`location`， `x`， `y`）的便利函数。
欲了解更多信息，请参阅 OpenGL ES 3.X 关于 glUniform2i() 的文档。
这个便利功能在 OpenGL ES 1.x 系统上没有任何作用。

### `void QOpenGLFunctions::glUniform2iv(GLint location, GLsizei count, const GLint *v)`

**作用与语义：**

调用 glUniform2iv（`location`， `count`， `v`）的便利函数。
欲了解更多信息，请参阅 glUniform2iv() 的 OpenGL ES 3.X 文档。
这个便利功能在 OpenGL ES 1.x 系统上没有任何作用。

### `void QOpenGLFunctions::glUniform3f(GLint location, GLfloat x, GLfloat y, GLfloat z)`

**作用与语义：**

调用glUniform3f（`location`， `x`， `y`， `z`）的便利函数。
更多信息请参见 glUniform3f() 的 OpenGL ES 3.X 文档。
这个便利功能在 OpenGL ES 1.x 系统上没有任何作用。

### `void QOpenGLFunctions::glUniform3fv(GLint location, GLsizei count, const GLfloat *v)`

**作用与语义：**

调用glUniform3fv（`location`， `count`， `v`）的便利函数。
更多信息请参见 OpenGL ES 3.X 关于 glUniform3fv() 的文档。
这个便利功能在 OpenGL ES 1.x 系统上没有任何作用。

### `void QOpenGLFunctions::glUniform3i(GLint location, GLint x, GLint y, GLint z)`

**作用与语义：**

调用glUniform3i（`location`， `x`， `y`， `z`的便利函数）。
欲了解更多信息，请参阅 OpenGL ES 3.X 关于 glUniform3i() 的文档。
这个便利功能在 OpenGL ES 1.x 系统上没有任何作用。

### `void QOpenGLFunctions::glUniform3iv(GLint location, GLsizei count, const GLint *v)`

**作用与语义：**

调用glUniform3iv（`location`， `count`， `v`）的便利函数。
更多信息请参见 OpenGL ES 3.X 关于 glUniform3iv() 的文档。
这个便利功能在 OpenGL ES 1.x 系统上没有任何作用。

### `void QOpenGLFunctions::glUniform4f(GLint location, GLfloat x, GLfloat y, GLfloat z, GLfloat w)`

**作用与语义：**

调用glUniform4f（`location`， `x`， `y`， `z`， `w`）的便利函数。
更多信息请参见 OpenGL ES 3.X 关于 glUniform4f() 的文档。
这个便利功能在 OpenGL ES 1.x 系统上没有任何作用。

### `void QOpenGLFunctions::glUniform4fv(GLint location, GLsizei count, const GLfloat *v)`

**作用与语义：**

调用glUniform4fv（`location`， `count`， `v`）的便利函数。
更多信息请参见 OpenGL ES 3.X 关于 glUniform4fv() 的文档。
这个便利功能在 OpenGL ES 1.x 系统上没有任何作用。

### `void QOpenGLFunctions::glUniform4i(GLint location, GLint x, GLint y, GLint z, GLint w)`

**作用与语义：**

调用 glUniform4i（`location`， `x`， `y`， `z`， `w` 的便利函数）。
欲了解更多信息，请参阅 glUniform4i() 的 OpenGL ES 3.X 文档。
这个便利功能在 OpenGL ES 1.x 系统上没有任何作用。

### `void QOpenGLFunctions::glUniform4iv(GLint location, GLsizei count, const GLint *v)`

**作用与语义：**

调用glUniform4iv（`location`， `count`， `v`）的便利函数。
欲了解更多信息，请参阅 OpenGL ES 3.X 关于 glUniform4iv() 的文档。
这个便利功能在 OpenGL ES 1.x 系统上没有任何作用。

### `void QOpenGLFunctions::glUniformMatrix2fv(GLint location, GLsizei count, GLboolean transpose, const GLfloat *value)`

**作用与语义：**

调用glUniformMatrix2fv（`location`， `count`， `transpose`， `value`）的便利函数。
欲了解更多信息，请参见 OpenGL ES 3.X 关于 glUniformMatrix2fv() 的文档。
这个便利功能在 OpenGL ES 1.x 系统上没有任何作用。

### `void QOpenGLFunctions::glUniformMatrix3fv(GLint location, GLsizei count, GLboolean transpose, const GLfloat *value)`

**作用与语义：**

调用 glUniformMatrix3fv（`location`， `count`， `transpose`， `value` 的便利函数）。
欲了解更多信息，请参阅 OpenGL ES 3.X 关于 glUniformMatrix3fv() 的文档。
这个便利功能在 OpenGL ES 1.x 系统上没有任何作用。

### `void QOpenGLFunctions::glUniformMatrix4fv(GLint location, GLsizei count, GLboolean transpose, const GLfloat *value)`

**作用与语义：**

调用glUniformMatrix4fv（`location`， `count`， `transpose`， `value`）的便利函数。
更多信息请参见 OpenGL ES 3.X 关于 glUniformMatrix4fv() 的文档。
这个便利功能在 OpenGL ES 1.x 系统上没有任何作用。

### `void QOpenGLFunctions::glUseProgram(GLuint program)`

**作用与语义：**

调用 glUseProgram（`program`） 的便利函数。
更多信息请参见 OpenGL ES 3.X 关于 glUseProgram() 的文档。
这个便利功能在 OpenGL ES 1.x 系统上没有任何作用。

### `void QOpenGLFunctions::glValidateProgram(GLuint program)`

**作用与语义：**

调用 glValidateProgram（`program`） 的便利函数。
欲了解更多信息，请参阅 OpenGL ES 3.X 关于 glValidateProgram() 的文档。
这个便利功能在 OpenGL ES 1.x 系统上没有任何作用。

### `void QOpenGLFunctions::glVertexAttrib1f(GLuint indx, GLfloat x)`

**作用与语义：**

调用glVertexAttrib1f（`indx`， `x`）的便利函数。
欲了解更多信息，请参阅 OpenGL ES 3.X 关于 glVertexAttrib1f() 的文档。
这个便利功能在 OpenGL ES 1.x 系统上没有任何作用。

### `void QOpenGLFunctions::glVertexAttrib1fv(GLuint indx, const GLfloat *values)`

**作用与语义：**

调用glVertexAttrib1fv（`indx`， `values`）的便利函数。
更多信息请参阅 OpenGL ES 3.X 关于 glVertexAttrib1fv() 的文档。
这个便利功能在 OpenGL ES 1.x 系统上没有任何作用。

### `void QOpenGLFunctions::glVertexAttrib2f(GLuint indx, GLfloat x, GLfloat y)`

**作用与语义：**

调用glVertexAttrib2f（`indx`， `x`， `y`）的便利函数。
更多信息请参见 glVertexAttrib2f() 的 OpenGL ES 3.X 文档。
这个便利功能在 OpenGL ES 1.x 系统上没有任何作用。

### `void QOpenGLFunctions::glVertexAttrib2fv(GLuint indx, const GLfloat *values)`

**作用与语义：**

调用glVertexAttrib2fv（`indx`， `values`）的便利函数。
更多信息请参见 OpenGL ES 3.X 关于 glVertexAttrib2fv() 的文档。
这个便利功能在 OpenGL ES 1.x 系统上没有任何作用。

### `void QOpenGLFunctions::glVertexAttrib3f(GLuint indx, GLfloat x, GLfloat y, GLfloat z)`

**作用与语义：**

调用glVertexAttrib3f（`indx`， `x`， `y`， `z`）的便利函数。
更多信息请参见 OpenGL ES 3.X 关于 glVertexAttrib3f() 的文档。
这个便利功能在 OpenGL ES 1.x 系统上没有任何作用。

### `void QOpenGLFunctions::glVertexAttrib3fv(GLuint indx, const GLfloat *values)`

**作用与语义：**

调用glVertexAttrib3fv（`indx`， `values`）的便利函数。
更多信息请参见 OpenGL ES 3.X 关于 glVertexAttrib3fv() 的文档。
这个便利功能在 OpenGL ES 1.x 系统上没有任何作用。

### `void QOpenGLFunctions::glVertexAttrib4f(GLuint indx, GLfloat x, GLfloat y, GLfloat z, GLfloat w)`

**作用与语义：**

调用glVertexAttrib4f（`indx`， `x`， `y`， `z`， `w`）的便利函数。
更多信息请参见 OpenGL ES 3.X 关于 glVertexAttrib4f() 的文档。
这个便利功能在 OpenGL ES 1.x 系统上没有任何作用。

### `void QOpenGLFunctions::glVertexAttrib4fv(GLuint indx, const GLfloat *values)`

**作用与语义：**

调用glVertexAttrib4fv（`indx`， `values`）的便利函数。
更多信息请参见 OpenGL ES 3.X 关于 glVertexAttrib4fv() 的文档。
这个便利功能在 OpenGL ES 1.x 系统上没有任何作用。

### `void QOpenGLFunctions::glVertexAttribPointer(GLuint indx, GLint size, GLenum type, GLboolean normalized, GLsizei stride, const void *ptr)`

**作用与语义：**

调用 glVertexAttribPointer（`indx`， `size`， `type`， `normalized`， `stride`， `ptr` 的便利函数。
更多信息请参见 OpenGL ES 3.X 关于 glVertexAttribPointer() 的文档。
这个便利功能在 OpenGL ES 1.x 系统上没有任何作用。

### `void QOpenGLFunctions::glViewport(GLint x, GLint y, GLsizei width, GLsizei height)`

**作用与语义：**

调用glViewport（`x`， `y`， `width`， `height`）的便利函数。
更多信息请参见 OpenGL ES 3.X 关于 glViewport() 的文档。

### `bool QOpenGLFunctions::hasOpenGLFeature(QOpenGLFunctions::OpenGLFeature feature) const`

**作用与语义：**

如果此系统的 OpenGL 实现中存在 `feature`，则返回 `true`；否则返回 false。假设与此函数解析器关联的 `QOpenGLContext` 是当前的。

### `void QOpenGLFunctions::initializeOpenGLFunctions()`

**作用与语义：**

初始化当前上下文下的OpenGL函数解析。
调用该函数后，`QOpenGLFunctions`对象只能与当前上下文及共享上下文的其他上下文一起使用。再次调用初始化OpenGLFunctions()以更改对象的上下文关联。

### `QOpenGLFunctions::OpenGLFeatures QOpenGLFunctions::openGLFeatures() const`

**作用与语义：**

返回该系统OpenGL实现中存在的功能集合。
假设与该函数解析器关联的 `QOpenGLContext`是电流的。

### `enum OpenGLFeature { Multitexture, Shaders, Buffers, Framebuffers, BlendColor, …, MultipleRenderTargets }`

**作用与语义：**

该枚举定义了OpenGL和OpenGL ES特性，其存在可能取决于实现。
- `QOpenGLFunctions::Multitexture`：`0x0001`;`glActiveTexture()`功能可用。
- `QOpenGLFunctions::Shaders`：`0x0002`;提供着色器功能。
- `QOpenGLFunctions::Buffers`：`0x0004`;顶点和索引缓冲区功能可用。
- `QOpenGLFunctions::Framebuffers`：`0x0008`;提供帧缓冲对象函数。
- `QOpenGLFunctions::BlendColor`：`0x0010`;`glBlendColor()` 可用。
- `QOpenGLFunctions::BlendEquation`：`0x0020`;`glBlendEquation()` 有。
- `QOpenGLFunctions::BlendEquationSeparate`：`0x0040`;`glBlendEquationSeparate()` 有。
- `QOpenGLFunctions::BlendEquationAdvanced`：`0x20000`;提供高级混合方程。
- `QOpenGLFunctions::BlendFuncSeparate`：`0x0080`;`glBlendFuncSeparate()` 可用。
- `QOpenGLFunctions::BlendSubtract`：`0x0100`;支持混合减法模式。
- `QOpenGLFunctions::CompressedTextures`：`0x0200`;提供压缩纹理函数。
- `QOpenGLFunctions::Multisample`：`0x0400`;`glSampleCoverage()`功能可用。
- `QOpenGLFunctions::StencilSeparate`：`0x0800`;提供独立的模板功能。
- `QOpenGLFunctions::NPOTTextures`：`0x1000`;两种纹理的幂次均可用。
- `QOpenGLFunctions::NPOTTextureRepeat`：`0x2000`;两纹理的非幂可以用GL_REPEAT作为包裹参数。
- `QOpenGLFunctions::FixedFunctionPipeline`：`0x4000`;固定函数流水线可用。
- `QOpenGLFunctions::TextureRGFormats`：`0x8000`;提供GL_RED和GL_RG纹理格式。
- `QOpenGLFunctions::MultipleRenderTargets`：`0x10000`;帧缓冲对象可获得多色附加。
OpenGLFeatures 类型是 QFlags 的 typedef<OpenGLFeature>。它存储 OpenGLFeature 值的 OR 组合。

### `flags OpenGLFeatures`

**作用与语义：**

该枚举定义了OpenGL和OpenGL ES特性，其存在可能取决于实现。
- `QOpenGLFunctions::Multitexture`：`0x0001`;`glActiveTexture()`功能可用。
- `QOpenGLFunctions::Shaders`：`0x0002`;提供着色器功能。
- `QOpenGLFunctions::Buffers`：`0x0004`;顶点和索引缓冲区功能可用。
- `QOpenGLFunctions::Framebuffers`：`0x0008`;提供帧缓冲对象函数。
- `QOpenGLFunctions::BlendColor`：`0x0010`;`glBlendColor()` 可用。
- `QOpenGLFunctions::BlendEquation`：`0x0020`;`glBlendEquation()` 有。
- `QOpenGLFunctions::BlendEquationSeparate`：`0x0040`;`glBlendEquationSeparate()` 有。
- `QOpenGLFunctions::BlendEquationAdvanced`：`0x20000`;提供高级混合方程。
- `QOpenGLFunctions::BlendFuncSeparate`：`0x0080`;`glBlendFuncSeparate()` 可用。
- `QOpenGLFunctions::BlendSubtract`：`0x0100`;支持混合减法模式。
- `QOpenGLFunctions::CompressedTextures`：`0x0200`;提供压缩纹理函数。
- `QOpenGLFunctions::Multisample`：`0x0400`;`glSampleCoverage()`功能可用。
- `QOpenGLFunctions::StencilSeparate`：`0x0800`;提供独立的模板功能。
- `QOpenGLFunctions::NPOTTextures`：`0x1000`;两种纹理的幂次均可用。
- `QOpenGLFunctions::NPOTTextureRepeat`：`0x2000`;两纹理的非幂可以用GL_REPEAT作为包裹参数。
- `QOpenGLFunctions::FixedFunctionPipeline`：`0x4000`;固定函数流水线可用。
- `QOpenGLFunctions::TextureRGFormats`：`0x8000`;提供GL_RED和GL_RG纹理格式。
- `QOpenGLFunctions::MultipleRenderTargets`：`0x10000`;帧缓冲对象可获得多色附加。
OpenGLFeatures 类型是 QFlags 的 typedef<OpenGLFeature>。它存储 OpenGLFeature 值的 OR 组合。

## 6. 深入实践与常见坑

### 生命周期和资源边界

先确认对象是值类型还是 QObject 派生对象，再确定所有权、有效期、拷贝成本和销毁方式。返回的句柄、索引、reply、设备或迭代器可能有独立的有效期，不能只看 C++ 指针是否非空。

### 状态和错误边界

把返回值、状态查询、错误信息和通知信号分开判断。调用成功可能只表示请求被接受，真正完成还要等待状态变化或完成信号；读取数据前先检查对象和结果是否有效。

### 线程边界

如果类型直接或间接参与 QObject、GUI、设备或异步框架，就必须确认线程归属和事件循环；值类型虽然可以复制，也要注意内部指针、共享数据和并发写入。

### 最容易出现的错误

不要忽略构造失败、空返回、默认值和版本限制；不要把异步 API 当同步 API；不要在没有确认所有权和线程的情况下保存指针或跨线程调用。

### 版本和平台

本文档以 Qt 6.11.1 为依据。涉及平台后端、编解码器、数据库驱动、窗口风格、编译器特性或标注了版本号的 API 时，要把版本条件当作使用约束，而不是只看函数是否能补全。

## 7. 使用边界

`QOpenGLFunctions` 所属机制类型：Qt 类型机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
