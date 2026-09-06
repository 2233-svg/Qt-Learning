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

这里直接说明每个公开成员解决什么问题、参数代表什么、返回什么、会改变什么以及使用时容易出现什么问题。每一个公开签名都会有对应的中文解释。

本类共整理 151 个公开成员条目；没有独立长描述的 API 也会根据签名、类型和所属机制给出使用说明。

### `enum QOpenGLFunctions::OpenGLFeatureflags QOpenGLFunctions::OpenGLFeatures`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QOpenGLFunctions` 暴露的类型声明 `打开、GL、Featureflags`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 属性类型：`:OpenGLFeatureflags QOpenGLFunctions::OpenGLFeatures`。
- 属性名：`QOpenGLFunctions`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QOpenGLFunctions::QOpenGLFunctions()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QOpenGLFunctions` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[explicit] QOpenGLFunctions::QOpenGLFunctions(QOpenGLContext *context)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QOpenGLFunctions` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `context`：类型为 `QOpenGLContext *`。没有默认值，调用时必须提供。上下文对象，用于限定回调连接的生命周期或解析/执行环境。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] QOpenGLFunctions::~QOpenGLFunctions()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QOpenGLFunctions` 的析构函数。对象销毁时资源、子对象和连接会按 Qt 规则释放；异步对象要先停止任务或使用 deleteLater，避免回调访问已经不存在的实例。

**签名拆解：**

- 返回值：析构函数，无返回值。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLFunctions::glActiveTexture(GLenum texture)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLFunctions::glActiveTexture` 用于执行与“gl、活动状态、Texture”相关的操作。调用时要先确认当前状态和 `texture` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `texture`：类型为 `GLenum`。没有默认值，调用时必须提供。枚举或标志参数。先确认可用枚举值、互斥关系和默认值，必要时用按位或组合标志。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLFunctions::glAttachShader(GLuint program, GLuint shader)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLFunctions::glAttachShader` 用于执行与“gl、Attach、Shader”相关的操作。调用时要先确认当前状态和 `program`、`shader` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `program`：类型为 `GLuint`。没有默认值，调用时必须提供。传入 `GLuint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `shader`：类型为 `GLuint`。没有默认值，调用时必须提供。传入 `GLuint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLFunctions::glBindAttribLocation(GLuint program, GLuint index, const char *name)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLFunctions::glBindAttribLocation` 用于执行与“gl、绑定、Attrib、Location”相关的操作。调用时要先确认当前状态和 `program`、`index`、`name` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `program`：类型为 `GLuint`。没有默认值，调用时必须提供。传入 `GLuint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `index`：类型为 `GLuint`。没有默认值，调用时必须提供。项目或数据索引。先确认索引基于 0 还是 1、是否允许越界/负数，以及调用后索引是否仍然有效。
- 参数 `name`：类型为 `const char *`。没有默认值，调用时必须提供。名称或键。通常是稳定的 API/配置标识，不应随意使用显示文本替代。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLFunctions::glBindBuffer(GLenum target, GLuint buffer)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLFunctions::glBindBuffer` 用于执行与“gl、绑定、Buffer”相关的操作。调用时要先确认当前状态和 `target`、`buffer` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `target`：类型为 `GLenum`。没有默认值，调用时必须提供。目标对象、目标属性或目标资源。要确认它在操作期间仍然有效，并支持所需能力。
- 参数 `buffer`：类型为 `GLuint`。没有默认值，调用时必须提供。传入 `GLuint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLFunctions::glBindFramebuffer(GLenum target, GLuint framebuffer)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLFunctions::glBindFramebuffer` 用于执行与“gl、绑定、Framebuffer”相关的操作。调用时要先确认当前状态和 `target`、`framebuffer` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `target`：类型为 `GLenum`。没有默认值，调用时必须提供。目标对象、目标属性或目标资源。要确认它在操作期间仍然有效，并支持所需能力。
- 参数 `framebuffer`：类型为 `GLuint`。没有默认值，调用时必须提供。传入 `GLuint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLFunctions::glBindRenderbuffer(GLenum target, GLuint renderbuffer)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLFunctions::glBindRenderbuffer` 用于执行与“gl、绑定、Renderbuffer”相关的操作。调用时要先确认当前状态和 `target`、`renderbuffer` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `target`：类型为 `GLenum`。没有默认值，调用时必须提供。目标对象、目标属性或目标资源。要确认它在操作期间仍然有效，并支持所需能力。
- 参数 `renderbuffer`：类型为 `GLuint`。没有默认值，调用时必须提供。传入 `GLuint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLFunctions::glBindTexture(GLenum target, GLuint texture)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLFunctions::glBindTexture` 用于执行与“gl、绑定、Texture”相关的操作。调用时要先确认当前状态和 `target`、`texture` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `target`：类型为 `GLenum`。没有默认值，调用时必须提供。目标对象、目标属性或目标资源。要确认它在操作期间仍然有效，并支持所需能力。
- 参数 `texture`：类型为 `GLuint`。没有默认值，调用时必须提供。传入 `GLuint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLFunctions::glBlendColor(GLclampf red, GLclampf green, GLclampf blue, GLclampf alpha)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLFunctions::glBlendColor` 用于执行与“gl、Blend、Color”相关的操作。调用时要先确认当前状态和 `red`、`green`、`blue`、`alpha` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `red`：类型为 `GLclampf`。没有默认值，调用时必须提供。传入 `GLclampf` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `green`：类型为 `GLclampf`。没有默认值，调用时必须提供。传入 `GLclampf` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `blue`：类型为 `GLclampf`。没有默认值，调用时必须提供。传入 `GLclampf` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `alpha`：类型为 `GLclampf`。没有默认值，调用时必须提供。传入 `GLclampf` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLFunctions::glBlendEquation(GLenum mode)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLFunctions::glBlendEquation` 用于执行与“gl、Blend、Equation”相关的操作。调用时要先确认当前状态和 `mode` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `mode`：类型为 `GLenum`。没有默认值，调用时必须提供。模式枚举或位标志。它通常决定对象后续允许的操作和状态转换。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLFunctions::glBlendEquationSeparate(GLenum modeRGB, GLenum modeAlpha)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLFunctions::glBlendEquationSeparate` 用于执行与“gl、Blend、Equation、Separate”相关的操作。调用时要先确认当前状态和 `modeRGB`、`modeAlpha` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `modeRGB`：类型为 `GLenum`。没有默认值，调用时必须提供。枚举或标志参数。先确认可用枚举值、互斥关系和默认值，必要时用按位或组合标志。
- 参数 `modeAlpha`：类型为 `GLenum`。没有默认值，调用时必须提供。枚举或标志参数。先确认可用枚举值、互斥关系和默认值，必要时用按位或组合标志。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLFunctions::glBlendFunc(GLenum sfactor, GLenum dfactor)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLFunctions::glBlendFunc` 用于执行与“gl、Blend、Func”相关的操作。调用时要先确认当前状态和 `sfactor`、`dfactor` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `sfactor`：类型为 `GLenum`。没有默认值，调用时必须提供。枚举或标志参数。先确认可用枚举值、互斥关系和默认值，必要时用按位或组合标志。
- 参数 `dfactor`：类型为 `GLenum`。没有默认值，调用时必须提供。枚举或标志参数。先确认可用枚举值、互斥关系和默认值，必要时用按位或组合标志。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLFunctions::glBlendFuncSeparate(GLenum srcRGB, GLenum dstRGB, GLenum srcAlpha, GLenum dstAlpha)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLFunctions::glBlendFuncSeparate` 用于执行与“gl、Blend、Func、Separate”相关的操作。调用时要先确认当前状态和 `srcRGB`、`dstRGB`、`srcAlpha`、`dstAlpha` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `srcRGB`：类型为 `GLenum`。没有默认值，调用时必须提供。枚举或标志参数。先确认可用枚举值、互斥关系和默认值，必要时用按位或组合标志。
- 参数 `dstRGB`：类型为 `GLenum`。没有默认值，调用时必须提供。枚举或标志参数。先确认可用枚举值、互斥关系和默认值，必要时用按位或组合标志。
- 参数 `srcAlpha`：类型为 `GLenum`。没有默认值，调用时必须提供。枚举或标志参数。先确认可用枚举值、互斥关系和默认值，必要时用按位或组合标志。
- 参数 `dstAlpha`：类型为 `GLenum`。没有默认值，调用时必须提供。枚举或标志参数。先确认可用枚举值、互斥关系和默认值，必要时用按位或组合标志。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLFunctions::glBufferData(GLenum target, qopengl_GLsizeiptr size, const void *data, GLenum usage)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLFunctions::glBufferData` 用于执行与“gl、Buffer、数据访问”相关的操作。调用时要先确认当前状态和 `target`、`size`、`data`、`usage` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `target`：类型为 `GLenum`。没有默认值，调用时必须提供。目标对象、目标属性或目标资源。要确认它在操作期间仍然有效，并支持所需能力。
- 参数 `size`：类型为 `qopengl_GLsizeiptr`。没有默认值，调用时必须提供。尺寸或长度，单位通常是像素、字节、元素数或时间，必须结合类型和类的上下文确认。
- 参数 `data`：类型为 `const void *`。没有默认值，调用时必须提供。数据载荷或要读取的数据。要确认编码、所有权、大小和是否允许为空。
- 参数 `usage`：类型为 `GLenum`。没有默认值，调用时必须提供。枚举或标志参数。先确认可用枚举值、互斥关系和默认值，必要时用按位或组合标志。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLFunctions::glBufferSubData(GLenum target, qopengl_GLintptr offset, qopengl_GLsizeiptr size, const void *data)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLFunctions::glBufferSubData` 用于执行与“gl、Buffer、Sub、数据访问”相关的操作。调用时要先确认当前状态和 `target`、`offset`、`size`、`data` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `target`：类型为 `GLenum`。没有默认值，调用时必须提供。目标对象、目标属性或目标资源。要确认它在操作期间仍然有效，并支持所需能力。
- 参数 `offset`：类型为 `qopengl_GLintptr`。没有默认值，调用时必须提供。传入 `qopengl_GLintptr` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `size`：类型为 `qopengl_GLsizeiptr`。没有默认值，调用时必须提供。尺寸或长度，单位通常是像素、字节、元素数或时间，必须结合类型和类的上下文确认。
- 参数 `data`：类型为 `const void *`。没有默认值，调用时必须提供。数据载荷或要读取的数据。要确认编码、所有权、大小和是否允许为空。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `GLenum QOpenGLFunctions::glCheckFramebufferStatus(GLenum target)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLFunctions::glCheckFramebufferStatus` 用于计算、查询或取得与“gl、Check、Framebuffer、状态”相关的操作。调用时要先确认当前状态和 `target` 的有效范围；返回类型是 `GLenum`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`GLenum`。
- 参数 `target`：类型为 `GLenum`。没有默认值，调用时必须提供。目标对象、目标属性或目标资源。要确认它在操作期间仍然有效，并支持所需能力。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLFunctions::glClear(GLbitfield mask)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLFunctions::glClear` 用于执行与“gl、清空”相关的操作。调用时要先确认当前状态和 `mask` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `mask`：类型为 `GLbitfield`。没有默认值，调用时必须提供。传入 `GLbitfield` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLFunctions::glClearColor(GLclampf red, GLclampf green, GLclampf blue, GLclampf alpha)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLFunctions::glClearColor` 用于执行与“gl、清空、Color”相关的操作。调用时要先确认当前状态和 `red`、`green`、`blue`、`alpha` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `red`：类型为 `GLclampf`。没有默认值，调用时必须提供。传入 `GLclampf` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `green`：类型为 `GLclampf`。没有默认值，调用时必须提供。传入 `GLclampf` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `blue`：类型为 `GLclampf`。没有默认值，调用时必须提供。传入 `GLclampf` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `alpha`：类型为 `GLclampf`。没有默认值，调用时必须提供。传入 `GLclampf` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLFunctions::glClearDepthf(GLclampf depth)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLFunctions::glClearDepthf` 用于执行与“gl、清空、Depthf”相关的操作。调用时要先确认当前状态和 `depth` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `depth`：类型为 `GLclampf`。没有默认值，调用时必须提供。传入 `GLclampf` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLFunctions::glClearStencil(GLint s)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLFunctions::glClearStencil` 用于执行与“gl、清空、Stencil”相关的操作。调用时要先确认当前状态和 `s` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `s`：类型为 `GLint`。没有默认值，调用时必须提供。传入 `GLint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLFunctions::glColorMask(GLboolean red, GLboolean green, GLboolean blue, GLboolean alpha)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLFunctions::glColorMask` 用于执行与“gl、Color、Mask”相关的操作。调用时要先确认当前状态和 `red`、`green`、`blue`、`alpha` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `red`：类型为 `GLboolean`。没有默认值，调用时必须提供。传入 `GLboolean` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `green`：类型为 `GLboolean`。没有默认值，调用时必须提供。传入 `GLboolean` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `blue`：类型为 `GLboolean`。没有默认值，调用时必须提供。传入 `GLboolean` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `alpha`：类型为 `GLboolean`。没有默认值，调用时必须提供。传入 `GLboolean` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLFunctions::glCompileShader(GLuint shader)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLFunctions::glCompileShader` 用于执行与“gl、Compile、Shader”相关的操作。调用时要先确认当前状态和 `shader` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `shader`：类型为 `GLuint`。没有默认值，调用时必须提供。传入 `GLuint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLFunctions::glCompressedTexImage2D(GLenum target, GLint level, GLenum internalformat, GLsizei width, GLsizei height, GLint border, GLsizei imageSize, const void *data)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLFunctions::glCompressedTexImage2D` 用于执行与“gl、Compressed、Tex、Image、2、D”相关的操作。调用时要先确认当前状态和 `target`、`level`、`internalformat`、`width`、`height`、`border`、`imageSize`、`data` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `target`：类型为 `GLenum`。没有默认值，调用时必须提供。目标对象、目标属性或目标资源。要确认它在操作期间仍然有效，并支持所需能力。
- 参数 `level`：类型为 `GLint`。没有默认值，调用时必须提供。传入 `GLint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `internalformat`：类型为 `GLenum`。没有默认值，调用时必须提供。枚举或标志参数。先确认可用枚举值、互斥关系和默认值，必要时用按位或组合标志。
- 参数 `width`：类型为 `GLsizei`。没有默认值，调用时必须提供。宽度，通常以像素、字符数或元素数量表示；要确认是否允许 0、负数和超出最大值。
- 参数 `height`：类型为 `GLsizei`。没有默认值，调用时必须提供。高度，通常以像素、字符数或元素数量表示；要确认是否允许 0、负数和超出最大值。
- 参数 `border`：类型为 `GLint`。没有默认值，调用时必须提供。传入 `GLint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `imageSize`：类型为 `GLsizei`。没有默认值，调用时必须提供。传入 `GLsizei` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `data`：类型为 `const void *`。没有默认值，调用时必须提供。数据载荷或要读取的数据。要确认编码、所有权、大小和是否允许为空。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLFunctions::glCompressedTexSubImage2D(GLenum target, GLint level, GLint xoffset, GLint yoffset, GLsizei width, GLsizei height, GLenum format, GLsizei imageSize, const void *data)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLFunctions::glCompressedTexSubImage2D` 用于执行与“gl、Compressed、Tex、Sub、Image、2、D”相关的操作。调用时要先确认当前状态和 `target`、`level`、`xoffset`、`yoffset`、`width`、`height`、`format`、`imageSize`、`data` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `target`：类型为 `GLenum`。没有默认值，调用时必须提供。目标对象、目标属性或目标资源。要确认它在操作期间仍然有效，并支持所需能力。
- 参数 `level`：类型为 `GLint`。没有默认值，调用时必须提供。传入 `GLint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `xoffset`：类型为 `GLint`。没有默认值，调用时必须提供。传入 `GLint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `yoffset`：类型为 `GLint`。没有默认值，调用时必须提供。传入 `GLint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `width`：类型为 `GLsizei`。没有默认值，调用时必须提供。宽度，通常以像素、字符数或元素数量表示；要确认是否允许 0、负数和超出最大值。
- 参数 `height`：类型为 `GLsizei`。没有默认值，调用时必须提供。高度，通常以像素、字符数或元素数量表示；要确认是否允许 0、负数和超出最大值。
- 参数 `format`：类型为 `GLenum`。没有默认值，调用时必须提供。数据格式或显示格式。格式通常会影响解析、像素布局、精度、编码或兼容性。
- 参数 `imageSize`：类型为 `GLsizei`。没有默认值，调用时必须提供。传入 `GLsizei` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `data`：类型为 `const void *`。没有默认值，调用时必须提供。数据载荷或要读取的数据。要确认编码、所有权、大小和是否允许为空。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLFunctions::glCopyTexImage2D(GLenum target, GLint level, GLenum internalformat, GLint x, GLint y, GLsizei width, GLsizei height, GLint border)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLFunctions::glCopyTexImage2D` 用于执行与“gl、Copy、Tex、Image、2、D”相关的操作。调用时要先确认当前状态和 `target`、`level`、`internalformat`、`x`、`y`、`width`、`height`、`border` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `target`：类型为 `GLenum`。没有默认值，调用时必须提供。目标对象、目标属性或目标资源。要确认它在操作期间仍然有效，并支持所需能力。
- 参数 `level`：类型为 `GLint`。没有默认值，调用时必须提供。传入 `GLint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `internalformat`：类型为 `GLenum`。没有默认值，调用时必须提供。枚举或标志参数。先确认可用枚举值、互斥关系和默认值，必要时用按位或组合标志。
- 参数 `x`：类型为 `GLint`。没有默认值，调用时必须提供。传入 `GLint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `y`：类型为 `GLint`。没有默认值，调用时必须提供。传入 `GLint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `width`：类型为 `GLsizei`。没有默认值，调用时必须提供。宽度，通常以像素、字符数或元素数量表示；要确认是否允许 0、负数和超出最大值。
- 参数 `height`：类型为 `GLsizei`。没有默认值，调用时必须提供。高度，通常以像素、字符数或元素数量表示；要确认是否允许 0、负数和超出最大值。
- 参数 `border`：类型为 `GLint`。没有默认值，调用时必须提供。传入 `GLint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLFunctions::glCopyTexSubImage2D(GLenum target, GLint level, GLint xoffset, GLint yoffset, GLint x, GLint y, GLsizei width, GLsizei height)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLFunctions::glCopyTexSubImage2D` 用于执行与“gl、Copy、Tex、Sub、Image、2、D”相关的操作。调用时要先确认当前状态和 `target`、`level`、`xoffset`、`yoffset`、`x`、`y`、`width`、`height` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `target`：类型为 `GLenum`。没有默认值，调用时必须提供。目标对象、目标属性或目标资源。要确认它在操作期间仍然有效，并支持所需能力。
- 参数 `level`：类型为 `GLint`。没有默认值，调用时必须提供。传入 `GLint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `xoffset`：类型为 `GLint`。没有默认值，调用时必须提供。传入 `GLint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `yoffset`：类型为 `GLint`。没有默认值，调用时必须提供。传入 `GLint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `x`：类型为 `GLint`。没有默认值，调用时必须提供。传入 `GLint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `y`：类型为 `GLint`。没有默认值，调用时必须提供。传入 `GLint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `width`：类型为 `GLsizei`。没有默认值，调用时必须提供。宽度，通常以像素、字符数或元素数量表示；要确认是否允许 0、负数和超出最大值。
- 参数 `height`：类型为 `GLsizei`。没有默认值，调用时必须提供。高度，通常以像素、字符数或元素数量表示；要确认是否允许 0、负数和超出最大值。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `GLuint QOpenGLFunctions::glCreateProgram()`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLFunctions::glCreateProgram` 用于计算、查询或取得与“gl、创建、Program”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `GLuint`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`GLuint`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `GLuint QOpenGLFunctions::glCreateShader(GLenum type)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLFunctions::glCreateShader` 用于计算、查询或取得与“gl、创建、Shader”相关的操作。调用时要先确认当前状态和 `type` 的有效范围；返回类型是 `GLuint`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`GLuint`。
- 参数 `type`：类型为 `GLenum`。没有默认值，调用时必须提供。类型、格式或策略枚举。要确认枚举值的适用范围和平台支持情况。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLFunctions::glCullFace(GLenum mode)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLFunctions::glCullFace` 用于执行与“gl、Cull、Face”相关的操作。调用时要先确认当前状态和 `mode` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `mode`：类型为 `GLenum`。没有默认值，调用时必须提供。模式枚举或位标志。它通常决定对象后续允许的操作和状态转换。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLFunctions::glDeleteBuffers(GLsizei n, const GLuint *buffers)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLFunctions::glDeleteBuffers` 用于执行与“gl、删除、Buffers”相关的操作。调用时要先确认当前状态和 `n`、`buffers` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `n`：类型为 `GLsizei`。没有默认值，调用时必须提供。传入 `GLsizei` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `buffers`：类型为 `const GLuint *`。没有默认值，调用时必须提供。传入 `const GLuint *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLFunctions::glDeleteFramebuffers(GLsizei n, const GLuint *framebuffers)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLFunctions::glDeleteFramebuffers` 用于执行与“gl、删除、Framebuffers”相关的操作。调用时要先确认当前状态和 `n`、`framebuffers` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `n`：类型为 `GLsizei`。没有默认值，调用时必须提供。传入 `GLsizei` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `framebuffers`：类型为 `const GLuint *`。没有默认值，调用时必须提供。传入 `const GLuint *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLFunctions::glDeleteProgram(GLuint program)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLFunctions::glDeleteProgram` 用于执行与“gl、删除、Program”相关的操作。调用时要先确认当前状态和 `program` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `program`：类型为 `GLuint`。没有默认值，调用时必须提供。传入 `GLuint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLFunctions::glDeleteRenderbuffers(GLsizei n, const GLuint *renderbuffers)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLFunctions::glDeleteRenderbuffers` 用于执行与“gl、删除、Renderbuffers”相关的操作。调用时要先确认当前状态和 `n`、`renderbuffers` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `n`：类型为 `GLsizei`。没有默认值，调用时必须提供。传入 `GLsizei` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `renderbuffers`：类型为 `const GLuint *`。没有默认值，调用时必须提供。传入 `const GLuint *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLFunctions::glDeleteShader(GLuint shader)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLFunctions::glDeleteShader` 用于执行与“gl、删除、Shader”相关的操作。调用时要先确认当前状态和 `shader` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `shader`：类型为 `GLuint`。没有默认值，调用时必须提供。传入 `GLuint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLFunctions::glDeleteTextures(GLsizei n, const GLuint *textures)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLFunctions::glDeleteTextures` 用于执行与“gl、删除、Textures”相关的操作。调用时要先确认当前状态和 `n`、`textures` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `n`：类型为 `GLsizei`。没有默认值，调用时必须提供。传入 `GLsizei` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `textures`：类型为 `const GLuint *`。没有默认值，调用时必须提供。传入 `const GLuint *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLFunctions::glDepthFunc(GLenum func)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLFunctions::glDepthFunc` 用于执行与“gl、Depth、Func”相关的操作。调用时要先确认当前状态和 `func` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `func`：类型为 `GLenum`。没有默认值，调用时必须提供。枚举或标志参数。先确认可用枚举值、互斥关系和默认值，必要时用按位或组合标志。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLFunctions::glDepthMask(GLboolean flag)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLFunctions::glDepthMask` 用于执行与“gl、Depth、Mask”相关的操作。调用时要先确认当前状态和 `flag` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `flag`：类型为 `GLboolean`。没有默认值，调用时必须提供。枚举或标志参数。先确认可用枚举值、互斥关系和默认值，必要时用按位或组合标志。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLFunctions::glDepthRangef(GLclampf zNear, GLclampf zFar)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLFunctions::glDepthRangef` 用于执行与“gl、Depth、Rangef”相关的操作。调用时要先确认当前状态和 `zNear`、`zFar` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `zNear`：类型为 `GLclampf`。没有默认值，调用时必须提供。传入 `GLclampf` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `zFar`：类型为 `GLclampf`。没有默认值，调用时必须提供。传入 `GLclampf` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLFunctions::glDetachShader(GLuint program, GLuint shader)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLFunctions::glDetachShader` 用于执行与“gl、Detach、Shader”相关的操作。调用时要先确认当前状态和 `program`、`shader` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `program`：类型为 `GLuint`。没有默认值，调用时必须提供。传入 `GLuint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `shader`：类型为 `GLuint`。没有默认值，调用时必须提供。传入 `GLuint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLFunctions::glDisable(GLenum cap)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLFunctions::glDisable` 用于执行与“gl、Disable”相关的操作。调用时要先确认当前状态和 `cap` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `cap`：类型为 `GLenum`。没有默认值，调用时必须提供。枚举或标志参数。先确认可用枚举值、互斥关系和默认值，必要时用按位或组合标志。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLFunctions::glDisableVertexAttribArray(GLuint index)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLFunctions::glDisableVertexAttribArray` 用于执行与“gl、Disable、Vertex、Attrib、Array”相关的操作。调用时要先确认当前状态和 `index` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `index`：类型为 `GLuint`。没有默认值，调用时必须提供。项目或数据索引。先确认索引基于 0 还是 1、是否允许越界/负数，以及调用后索引是否仍然有效。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLFunctions::glDrawArrays(GLenum mode, GLint first, GLsizei count)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLFunctions::glDrawArrays` 用于执行与“gl、绘制、Arrays”相关的操作。调用时要先确认当前状态和 `mode`、`first`、`count` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `mode`：类型为 `GLenum`。没有默认值，调用时必须提供。模式枚举或位标志。它通常决定对象后续允许的操作和状态转换。
- 参数 `first`：类型为 `GLint`。没有默认值，调用时必须提供。传入 `GLint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `count`：类型为 `GLsizei`。没有默认值，调用时必须提供。传入 `GLsizei` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLFunctions::glDrawElements(GLenum mode, GLsizei count, GLenum type, const GLvoid *indices)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLFunctions::glDrawElements` 用于执行与“gl、绘制、Elements”相关的操作。调用时要先确认当前状态和 `mode`、`count`、`type`、`indices` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `mode`：类型为 `GLenum`。没有默认值，调用时必须提供。模式枚举或位标志。它通常决定对象后续允许的操作和状态转换。
- 参数 `count`：类型为 `GLsizei`。没有默认值，调用时必须提供。传入 `GLsizei` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `type`：类型为 `GLenum`。没有默认值，调用时必须提供。类型、格式或策略枚举。要确认枚举值的适用范围和平台支持情况。
- 参数 `indices`：类型为 `const GLvoid *`。没有默认值，调用时必须提供。传入 `const GLvoid *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLFunctions::glEnable(GLenum cap)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLFunctions::glEnable` 用于执行与“gl、Enable”相关的操作。调用时要先确认当前状态和 `cap` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `cap`：类型为 `GLenum`。没有默认值，调用时必须提供。枚举或标志参数。先确认可用枚举值、互斥关系和默认值，必要时用按位或组合标志。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLFunctions::glEnableVertexAttribArray(GLuint index)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLFunctions::glEnableVertexAttribArray` 用于执行与“gl、Enable、Vertex、Attrib、Array”相关的操作。调用时要先确认当前状态和 `index` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `index`：类型为 `GLuint`。没有默认值，调用时必须提供。项目或数据索引。先确认索引基于 0 还是 1、是否允许越界/负数，以及调用后索引是否仍然有效。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLFunctions::glFinish()`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLFunctions::glFinish` 用于执行与“gl、Finish”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLFunctions::glFlush()`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLFunctions::glFlush` 用于执行与“gl、刷新”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLFunctions::glFramebufferRenderbuffer(GLenum target, GLenum attachment, GLenum renderbuffertarget, GLuint renderbuffer)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLFunctions::glFramebufferRenderbuffer` 用于执行与“gl、Framebuffer、Renderbuffer”相关的操作。调用时要先确认当前状态和 `target`、`attachment`、`renderbuffertarget`、`renderbuffer` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `target`：类型为 `GLenum`。没有默认值，调用时必须提供。目标对象、目标属性或目标资源。要确认它在操作期间仍然有效，并支持所需能力。
- 参数 `attachment`：类型为 `GLenum`。没有默认值，调用时必须提供。枚举或标志参数。先确认可用枚举值、互斥关系和默认值，必要时用按位或组合标志。
- 参数 `renderbuffertarget`：类型为 `GLenum`。没有默认值，调用时必须提供。枚举或标志参数。先确认可用枚举值、互斥关系和默认值，必要时用按位或组合标志。
- 参数 `renderbuffer`：类型为 `GLuint`。没有默认值，调用时必须提供。传入 `GLuint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLFunctions::glFramebufferTexture2D(GLenum target, GLenum attachment, GLenum textarget, GLuint texture, GLint level)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLFunctions::glFramebufferTexture2D` 用于执行与“gl、Framebuffer、Texture、2、D”相关的操作。调用时要先确认当前状态和 `target`、`attachment`、`textarget`、`texture`、`level` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `target`：类型为 `GLenum`。没有默认值，调用时必须提供。目标对象、目标属性或目标资源。要确认它在操作期间仍然有效，并支持所需能力。
- 参数 `attachment`：类型为 `GLenum`。没有默认值，调用时必须提供。枚举或标志参数。先确认可用枚举值、互斥关系和默认值，必要时用按位或组合标志。
- 参数 `textarget`：类型为 `GLenum`。没有默认值，调用时必须提供。枚举或标志参数。先确认可用枚举值、互斥关系和默认值，必要时用按位或组合标志。
- 参数 `texture`：类型为 `GLuint`。没有默认值，调用时必须提供。传入 `GLuint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `level`：类型为 `GLint`。没有默认值，调用时必须提供。传入 `GLint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLFunctions::glFrontFace(GLenum mode)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLFunctions::glFrontFace` 用于执行与“gl、开头、Face”相关的操作。调用时要先确认当前状态和 `mode` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `mode`：类型为 `GLenum`。没有默认值，调用时必须提供。模式枚举或位标志。它通常决定对象后续允许的操作和状态转换。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLFunctions::glGenBuffers(GLsizei n, GLuint *buffers)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLFunctions::glGenBuffers` 用于执行与“gl、Gen、Buffers”相关的操作。调用时要先确认当前状态和 `n`、`buffers` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `n`：类型为 `GLsizei`。没有默认值，调用时必须提供。传入 `GLsizei` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `buffers`：类型为 `GLuint *`。没有默认值，调用时必须提供。传入 `GLuint *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLFunctions::glGenFramebuffers(GLsizei n, GLuint *framebuffers)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLFunctions::glGenFramebuffers` 用于执行与“gl、Gen、Framebuffers”相关的操作。调用时要先确认当前状态和 `n`、`framebuffers` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `n`：类型为 `GLsizei`。没有默认值，调用时必须提供。传入 `GLsizei` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `framebuffers`：类型为 `GLuint *`。没有默认值，调用时必须提供。传入 `GLuint *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLFunctions::glGenRenderbuffers(GLsizei n, GLuint *renderbuffers)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLFunctions::glGenRenderbuffers` 用于执行与“gl、Gen、Renderbuffers”相关的操作。调用时要先确认当前状态和 `n`、`renderbuffers` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `n`：类型为 `GLsizei`。没有默认值，调用时必须提供。传入 `GLsizei` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `renderbuffers`：类型为 `GLuint *`。没有默认值，调用时必须提供。传入 `GLuint *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLFunctions::glGenTextures(GLsizei n, GLuint *textures)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLFunctions::glGenTextures` 用于执行与“gl、Gen、Textures”相关的操作。调用时要先确认当前状态和 `n`、`textures` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `n`：类型为 `GLsizei`。没有默认值，调用时必须提供。传入 `GLsizei` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `textures`：类型为 `GLuint *`。没有默认值，调用时必须提供。传入 `GLuint *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLFunctions::glGenerateMipmap(GLenum target)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLFunctions::glGenerateMipmap` 用于执行与“gl、Generate、Mipmap”相关的操作。调用时要先确认当前状态和 `target` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `target`：类型为 `GLenum`。没有默认值，调用时必须提供。目标对象、目标属性或目标资源。要确认它在操作期间仍然有效，并支持所需能力。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLFunctions::glGetActiveAttrib(GLuint program, GLuint index, GLsizei bufsize, GLsizei *length, GLint *size, GLenum *type, char *name)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLFunctions::glGetActiveAttrib` 用于执行与“gl、Get、活动状态、Attrib”相关的操作。调用时要先确认当前状态和 `program`、`index`、`bufsize`、`length`、`size`、`type`、`name` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `program`：类型为 `GLuint`。没有默认值，调用时必须提供。传入 `GLuint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `index`：类型为 `GLuint`。没有默认值，调用时必须提供。项目或数据索引。先确认索引基于 0 还是 1、是否允许越界/负数，以及调用后索引是否仍然有效。
- 参数 `bufsize`：类型为 `GLsizei`。没有默认值，调用时必须提供。传入 `GLsizei` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `length`：类型为 `GLsizei *`。没有默认值，调用时必须提供。传入 `GLsizei *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `size`：类型为 `GLint *`。没有默认值，调用时必须提供。尺寸或长度，单位通常是像素、字节、元素数或时间，必须结合类型和类的上下文确认。
- 参数 `type`：类型为 `GLenum *`。没有默认值，调用时必须提供。类型、格式或策略枚举。要确认枚举值的适用范围和平台支持情况。
- 参数 `name`：类型为 `char *`。没有默认值，调用时必须提供。名称或键。通常是稳定的 API/配置标识，不应随意使用显示文本替代。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLFunctions::glGetActiveUniform(GLuint program, GLuint index, GLsizei bufsize, GLsizei *length, GLint *size, GLenum *type, char *name)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLFunctions::glGetActiveUniform` 用于执行与“gl、Get、活动状态、Uniform”相关的操作。调用时要先确认当前状态和 `program`、`index`、`bufsize`、`length`、`size`、`type`、`name` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `program`：类型为 `GLuint`。没有默认值，调用时必须提供。传入 `GLuint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `index`：类型为 `GLuint`。没有默认值，调用时必须提供。项目或数据索引。先确认索引基于 0 还是 1、是否允许越界/负数，以及调用后索引是否仍然有效。
- 参数 `bufsize`：类型为 `GLsizei`。没有默认值，调用时必须提供。传入 `GLsizei` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `length`：类型为 `GLsizei *`。没有默认值，调用时必须提供。传入 `GLsizei *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `size`：类型为 `GLint *`。没有默认值，调用时必须提供。尺寸或长度，单位通常是像素、字节、元素数或时间，必须结合类型和类的上下文确认。
- 参数 `type`：类型为 `GLenum *`。没有默认值，调用时必须提供。类型、格式或策略枚举。要确认枚举值的适用范围和平台支持情况。
- 参数 `name`：类型为 `char *`。没有默认值，调用时必须提供。名称或键。通常是稳定的 API/配置标识，不应随意使用显示文本替代。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLFunctions::glGetAttachedShaders(GLuint program, GLsizei maxcount, GLsizei *count, GLuint *shaders)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLFunctions::glGetAttachedShaders` 用于执行与“gl、Get、Attached、Shaders”相关的操作。调用时要先确认当前状态和 `program`、`maxcount`、`count`、`shaders` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `program`：类型为 `GLuint`。没有默认值，调用时必须提供。传入 `GLuint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `maxcount`：类型为 `GLsizei`。没有默认值，调用时必须提供。传入 `GLsizei` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `count`：类型为 `GLsizei *`。没有默认值，调用时必须提供。传入 `GLsizei *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `shaders`：类型为 `GLuint *`。没有默认值，调用时必须提供。传入 `GLuint *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `GLint QOpenGLFunctions::glGetAttribLocation(GLuint program, const char *name)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLFunctions::glGetAttribLocation` 用于计算、查询或取得与“gl、Get、Attrib、Location”相关的操作。调用时要先确认当前状态和 `program`、`name` 的有效范围；返回类型是 `GLint`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`GLint`。
- 参数 `program`：类型为 `GLuint`。没有默认值，调用时必须提供。传入 `GLuint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `name`：类型为 `const char *`。没有默认值，调用时必须提供。名称或键。通常是稳定的 API/配置标识，不应随意使用显示文本替代。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLFunctions::glGetBooleanv(GLenum pname, GLboolean *params)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLFunctions::glGetBooleanv` 用于执行与“gl、Get、Booleanv”相关的操作。调用时要先确认当前状态和 `pname`、`params` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `pname`：类型为 `GLenum`。没有默认值，调用时必须提供。枚举或标志参数。先确认可用枚举值、互斥关系和默认值，必要时用按位或组合标志。
- 参数 `params`：类型为 `GLboolean *`。没有默认值，调用时必须提供。传入 `GLboolean *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLFunctions::glGetBufferParameteriv(GLenum target, GLenum pname, GLint *params)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLFunctions::glGetBufferParameteriv` 用于执行与“gl、Get、Buffer、Parameteriv”相关的操作。调用时要先确认当前状态和 `target`、`pname`、`params` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `target`：类型为 `GLenum`。没有默认值，调用时必须提供。目标对象、目标属性或目标资源。要确认它在操作期间仍然有效，并支持所需能力。
- 参数 `pname`：类型为 `GLenum`。没有默认值，调用时必须提供。枚举或标志参数。先确认可用枚举值、互斥关系和默认值，必要时用按位或组合标志。
- 参数 `params`：类型为 `GLint *`。没有默认值，调用时必须提供。传入 `GLint *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `GLenum QOpenGLFunctions::glGetError()`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLFunctions::glGetError` 用于计算、查询或取得与“gl、Get、错误”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `GLenum`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`GLenum`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLFunctions::glGetFloatv(GLenum pname, GLfloat *params)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLFunctions::glGetFloatv` 用于执行与“gl、Get、Floatv”相关的操作。调用时要先确认当前状态和 `pname`、`params` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `pname`：类型为 `GLenum`。没有默认值，调用时必须提供。枚举或标志参数。先确认可用枚举值、互斥关系和默认值，必要时用按位或组合标志。
- 参数 `params`：类型为 `GLfloat *`。没有默认值，调用时必须提供。传入 `GLfloat *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLFunctions::glGetFramebufferAttachmentParameteriv(GLenum target, GLenum attachment, GLenum pname, GLint *params)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLFunctions::glGetFramebufferAttachmentParameteriv` 用于执行与“gl、Get、Framebuffer、Attachment、Parameteriv”相关的操作。调用时要先确认当前状态和 `target`、`attachment`、`pname`、`params` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `target`：类型为 `GLenum`。没有默认值，调用时必须提供。目标对象、目标属性或目标资源。要确认它在操作期间仍然有效，并支持所需能力。
- 参数 `attachment`：类型为 `GLenum`。没有默认值，调用时必须提供。枚举或标志参数。先确认可用枚举值、互斥关系和默认值，必要时用按位或组合标志。
- 参数 `pname`：类型为 `GLenum`。没有默认值，调用时必须提供。枚举或标志参数。先确认可用枚举值、互斥关系和默认值，必要时用按位或组合标志。
- 参数 `params`：类型为 `GLint *`。没有默认值，调用时必须提供。传入 `GLint *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLFunctions::glGetIntegerv(GLenum pname, GLint *params)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLFunctions::glGetIntegerv` 用于执行与“gl、Get、Integerv”相关的操作。调用时要先确认当前状态和 `pname`、`params` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `pname`：类型为 `GLenum`。没有默认值，调用时必须提供。枚举或标志参数。先确认可用枚举值、互斥关系和默认值，必要时用按位或组合标志。
- 参数 `params`：类型为 `GLint *`。没有默认值，调用时必须提供。传入 `GLint *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLFunctions::glGetProgramInfoLog(GLuint program, GLsizei bufsize, GLsizei *length, char *infolog)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLFunctions::glGetProgramInfoLog` 用于执行与“gl、Get、Program、Info、Log”相关的操作。调用时要先确认当前状态和 `program`、`bufsize`、`length`、`infolog` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `program`：类型为 `GLuint`。没有默认值，调用时必须提供。传入 `GLuint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `bufsize`：类型为 `GLsizei`。没有默认值，调用时必须提供。传入 `GLsizei` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `length`：类型为 `GLsizei *`。没有默认值，调用时必须提供。传入 `GLsizei *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `infolog`：类型为 `char *`。没有默认值，调用时必须提供。传入 `char *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLFunctions::glGetProgramiv(GLuint program, GLenum pname, GLint *params)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLFunctions::glGetProgramiv` 用于执行与“gl、Get、Programiv”相关的操作。调用时要先确认当前状态和 `program`、`pname`、`params` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `program`：类型为 `GLuint`。没有默认值，调用时必须提供。传入 `GLuint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `pname`：类型为 `GLenum`。没有默认值，调用时必须提供。枚举或标志参数。先确认可用枚举值、互斥关系和默认值，必要时用按位或组合标志。
- 参数 `params`：类型为 `GLint *`。没有默认值，调用时必须提供。传入 `GLint *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLFunctions::glGetRenderbufferParameteriv(GLenum target, GLenum pname, GLint *params)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLFunctions::glGetRenderbufferParameteriv` 用于执行与“gl、Get、Renderbuffer、Parameteriv”相关的操作。调用时要先确认当前状态和 `target`、`pname`、`params` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `target`：类型为 `GLenum`。没有默认值，调用时必须提供。目标对象、目标属性或目标资源。要确认它在操作期间仍然有效，并支持所需能力。
- 参数 `pname`：类型为 `GLenum`。没有默认值，调用时必须提供。枚举或标志参数。先确认可用枚举值、互斥关系和默认值，必要时用按位或组合标志。
- 参数 `params`：类型为 `GLint *`。没有默认值，调用时必须提供。传入 `GLint *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLFunctions::glGetShaderInfoLog(GLuint shader, GLsizei bufsize, GLsizei *length, char *infolog)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLFunctions::glGetShaderInfoLog` 用于执行与“gl、Get、Shader、Info、Log”相关的操作。调用时要先确认当前状态和 `shader`、`bufsize`、`length`、`infolog` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `shader`：类型为 `GLuint`。没有默认值，调用时必须提供。传入 `GLuint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `bufsize`：类型为 `GLsizei`。没有默认值，调用时必须提供。传入 `GLsizei` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `length`：类型为 `GLsizei *`。没有默认值，调用时必须提供。传入 `GLsizei *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `infolog`：类型为 `char *`。没有默认值，调用时必须提供。传入 `char *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLFunctions::glGetShaderPrecisionFormat(GLenum shadertype, GLenum precisiontype, GLint *range, GLint *precision)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLFunctions::glGetShaderPrecisionFormat` 用于执行与“gl、Get、Shader、Precision、格式化”相关的操作。调用时要先确认当前状态和 `shadertype`、`precisiontype`、`range`、`precision` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `shadertype`：类型为 `GLenum`。没有默认值，调用时必须提供。枚举或标志参数。先确认可用枚举值、互斥关系和默认值，必要时用按位或组合标志。
- 参数 `precisiontype`：类型为 `GLenum`。没有默认值，调用时必须提供。枚举或标志参数。先确认可用枚举值、互斥关系和默认值，必要时用按位或组合标志。
- 参数 `range`：类型为 `GLint *`。没有默认值，调用时必须提供。传入 `GLint *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `precision`：类型为 `GLint *`。没有默认值，调用时必须提供。精度或舍入策略；它可能影响数值转换和数据库结果，不能只按显示位数理解。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLFunctions::glGetShaderSource(GLuint shader, GLsizei bufsize, GLsizei *length, char *source)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLFunctions::glGetShaderSource` 用于执行与“gl、Get、Shader、来源”相关的操作。调用时要先确认当前状态和 `shader`、`bufsize`、`length`、`source` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `shader`：类型为 `GLuint`。没有默认值，调用时必须提供。传入 `GLuint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `bufsize`：类型为 `GLsizei`。没有默认值，调用时必须提供。传入 `GLsizei` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `length`：类型为 `GLsizei *`。没有默认值，调用时必须提供。传入 `GLsizei *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `source`：类型为 `char *`。没有默认值，调用时必须提供。源对象、源索引或源数据；它通常决定操作的输入，转换后要确认源的生命周期和线程归属。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLFunctions::glGetShaderiv(GLuint shader, GLenum pname, GLint *params)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLFunctions::glGetShaderiv` 用于执行与“gl、Get、Shaderiv”相关的操作。调用时要先确认当前状态和 `shader`、`pname`、`params` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `shader`：类型为 `GLuint`。没有默认值，调用时必须提供。传入 `GLuint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `pname`：类型为 `GLenum`。没有默认值，调用时必须提供。枚举或标志参数。先确认可用枚举值、互斥关系和默认值，必要时用按位或组合标志。
- 参数 `params`：类型为 `GLint *`。没有默认值，调用时必须提供。传入 `GLint *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `const GLubyte *QOpenGLFunctions::glGetString(GLenum name)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLFunctions::glGetString` 用于计算、查询或取得与“gl、Get、字符串”相关的操作。调用时要先确认当前状态和 `name` 的有效范围；返回类型是 `const GLubyte *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`const GLubyte *`。
- 参数 `name`：类型为 `GLenum`。没有默认值，调用时必须提供。名称或键。通常是稳定的 API/配置标识，不应随意使用显示文本替代。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLFunctions::glGetTexParameterfv(GLenum target, GLenum pname, GLfloat *params)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLFunctions::glGetTexParameterfv` 用于执行与“gl、Get、Tex、Parameterfv”相关的操作。调用时要先确认当前状态和 `target`、`pname`、`params` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `target`：类型为 `GLenum`。没有默认值，调用时必须提供。目标对象、目标属性或目标资源。要确认它在操作期间仍然有效，并支持所需能力。
- 参数 `pname`：类型为 `GLenum`。没有默认值，调用时必须提供。枚举或标志参数。先确认可用枚举值、互斥关系和默认值，必要时用按位或组合标志。
- 参数 `params`：类型为 `GLfloat *`。没有默认值，调用时必须提供。传入 `GLfloat *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLFunctions::glGetTexParameteriv(GLenum target, GLenum pname, GLint *params)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLFunctions::glGetTexParameteriv` 用于执行与“gl、Get、Tex、Parameteriv”相关的操作。调用时要先确认当前状态和 `target`、`pname`、`params` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `target`：类型为 `GLenum`。没有默认值，调用时必须提供。目标对象、目标属性或目标资源。要确认它在操作期间仍然有效，并支持所需能力。
- 参数 `pname`：类型为 `GLenum`。没有默认值，调用时必须提供。枚举或标志参数。先确认可用枚举值、互斥关系和默认值，必要时用按位或组合标志。
- 参数 `params`：类型为 `GLint *`。没有默认值，调用时必须提供。传入 `GLint *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `GLint QOpenGLFunctions::glGetUniformLocation(GLuint program, const char *name)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLFunctions::glGetUniformLocation` 用于计算、查询或取得与“gl、Get、Uniform、Location”相关的操作。调用时要先确认当前状态和 `program`、`name` 的有效范围；返回类型是 `GLint`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`GLint`。
- 参数 `program`：类型为 `GLuint`。没有默认值，调用时必须提供。传入 `GLuint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `name`：类型为 `const char *`。没有默认值，调用时必须提供。名称或键。通常是稳定的 API/配置标识，不应随意使用显示文本替代。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLFunctions::glGetUniformfv(GLuint program, GLint location, GLfloat *params)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLFunctions::glGetUniformfv` 用于执行与“gl、Get、Uniformfv”相关的操作。调用时要先确认当前状态和 `program`、`location`、`params` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `program`：类型为 `GLuint`。没有默认值，调用时必须提供。传入 `GLuint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `location`：类型为 `GLint`。没有默认值，调用时必须提供。传入 `GLint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `params`：类型为 `GLfloat *`。没有默认值，调用时必须提供。传入 `GLfloat *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLFunctions::glGetUniformiv(GLuint program, GLint location, GLint *params)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLFunctions::glGetUniformiv` 用于执行与“gl、Get、Uniformiv”相关的操作。调用时要先确认当前状态和 `program`、`location`、`params` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `program`：类型为 `GLuint`。没有默认值，调用时必须提供。传入 `GLuint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `location`：类型为 `GLint`。没有默认值，调用时必须提供。传入 `GLint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `params`：类型为 `GLint *`。没有默认值，调用时必须提供。传入 `GLint *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLFunctions::glGetVertexAttribPointerv(GLuint index, GLenum pname, void **pointer)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLFunctions::glGetVertexAttribPointerv` 用于执行与“gl、Get、Vertex、Attrib、Pointerv”相关的操作。调用时要先确认当前状态和 `index`、`pname`、`pointer` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `index`：类型为 `GLuint`。没有默认值，调用时必须提供。项目或数据索引。先确认索引基于 0 还是 1、是否允许越界/负数，以及调用后索引是否仍然有效。
- 参数 `pname`：类型为 `GLenum`。没有默认值，调用时必须提供。枚举或标志参数。先确认可用枚举值、互斥关系和默认值，必要时用按位或组合标志。
- 参数 `pointer`：类型为 `void **`。没有默认值，调用时必须提供。传入 `void **` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLFunctions::glGetVertexAttribfv(GLuint index, GLenum pname, GLfloat *params)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLFunctions::glGetVertexAttribfv` 用于执行与“gl、Get、Vertex、Attribfv”相关的操作。调用时要先确认当前状态和 `index`、`pname`、`params` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `index`：类型为 `GLuint`。没有默认值，调用时必须提供。项目或数据索引。先确认索引基于 0 还是 1、是否允许越界/负数，以及调用后索引是否仍然有效。
- 参数 `pname`：类型为 `GLenum`。没有默认值，调用时必须提供。枚举或标志参数。先确认可用枚举值、互斥关系和默认值，必要时用按位或组合标志。
- 参数 `params`：类型为 `GLfloat *`。没有默认值，调用时必须提供。传入 `GLfloat *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLFunctions::glGetVertexAttribiv(GLuint index, GLenum pname, GLint *params)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLFunctions::glGetVertexAttribiv` 用于执行与“gl、Get、Vertex、Attribiv”相关的操作。调用时要先确认当前状态和 `index`、`pname`、`params` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `index`：类型为 `GLuint`。没有默认值，调用时必须提供。项目或数据索引。先确认索引基于 0 还是 1、是否允许越界/负数，以及调用后索引是否仍然有效。
- 参数 `pname`：类型为 `GLenum`。没有默认值，调用时必须提供。枚举或标志参数。先确认可用枚举值、互斥关系和默认值，必要时用按位或组合标志。
- 参数 `params`：类型为 `GLint *`。没有默认值，调用时必须提供。传入 `GLint *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLFunctions::glHint(GLenum target, GLenum mode)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLFunctions::glHint` 用于执行与“gl、Hint”相关的操作。调用时要先确认当前状态和 `target`、`mode` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `target`：类型为 `GLenum`。没有默认值，调用时必须提供。目标对象、目标属性或目标资源。要确认它在操作期间仍然有效，并支持所需能力。
- 参数 `mode`：类型为 `GLenum`。没有默认值，调用时必须提供。模式枚举或位标志。它通常决定对象后续允许的操作和状态转换。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `GLboolean QOpenGLFunctions::glIsBuffer(GLuint buffer)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLFunctions::glIsBuffer` 用于计算、查询或取得与“gl、状态判断、Buffer”相关的操作。调用时要先确认当前状态和 `buffer` 的有效范围；返回类型是 `GLboolean`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`GLboolean`。
- 参数 `buffer`：类型为 `GLuint`。没有默认值，调用时必须提供。传入 `GLuint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `GLboolean QOpenGLFunctions::glIsEnabled(GLenum cap)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLFunctions::glIsEnabled` 用于计算、查询或取得与“gl、状态判断、启用状态”相关的操作。调用时要先确认当前状态和 `cap` 的有效范围；返回类型是 `GLboolean`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`GLboolean`。
- 参数 `cap`：类型为 `GLenum`。没有默认值，调用时必须提供。枚举或标志参数。先确认可用枚举值、互斥关系和默认值，必要时用按位或组合标志。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `GLboolean QOpenGLFunctions::glIsFramebuffer(GLuint framebuffer)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLFunctions::glIsFramebuffer` 用于计算、查询或取得与“gl、状态判断、Framebuffer”相关的操作。调用时要先确认当前状态和 `framebuffer` 的有效范围；返回类型是 `GLboolean`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`GLboolean`。
- 参数 `framebuffer`：类型为 `GLuint`。没有默认值，调用时必须提供。传入 `GLuint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `GLboolean QOpenGLFunctions::glIsProgram(GLuint program)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLFunctions::glIsProgram` 用于计算、查询或取得与“gl、状态判断、Program”相关的操作。调用时要先确认当前状态和 `program` 的有效范围；返回类型是 `GLboolean`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`GLboolean`。
- 参数 `program`：类型为 `GLuint`。没有默认值，调用时必须提供。传入 `GLuint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `GLboolean QOpenGLFunctions::glIsRenderbuffer(GLuint renderbuffer)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLFunctions::glIsRenderbuffer` 用于计算、查询或取得与“gl、状态判断、Renderbuffer”相关的操作。调用时要先确认当前状态和 `renderbuffer` 的有效范围；返回类型是 `GLboolean`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`GLboolean`。
- 参数 `renderbuffer`：类型为 `GLuint`。没有默认值，调用时必须提供。传入 `GLuint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `GLboolean QOpenGLFunctions::glIsShader(GLuint shader)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLFunctions::glIsShader` 用于计算、查询或取得与“gl、状态判断、Shader”相关的操作。调用时要先确认当前状态和 `shader` 的有效范围；返回类型是 `GLboolean`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`GLboolean`。
- 参数 `shader`：类型为 `GLuint`。没有默认值，调用时必须提供。传入 `GLuint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `GLboolean QOpenGLFunctions::glIsTexture(GLuint texture)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLFunctions::glIsTexture` 用于计算、查询或取得与“gl、状态判断、Texture”相关的操作。调用时要先确认当前状态和 `texture` 的有效范围；返回类型是 `GLboolean`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`GLboolean`。
- 参数 `texture`：类型为 `GLuint`。没有默认值，调用时必须提供。传入 `GLuint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLFunctions::glLineWidth(GLfloat width)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLFunctions::glLineWidth` 用于执行与“gl、行、宽度”相关的操作。调用时要先确认当前状态和 `width` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `width`：类型为 `GLfloat`。没有默认值，调用时必须提供。宽度，通常以像素、字符数或元素数量表示；要确认是否允许 0、负数和超出最大值。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLFunctions::glLinkProgram(GLuint program)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLFunctions::glLinkProgram` 用于执行与“gl、Link、Program”相关的操作。调用时要先确认当前状态和 `program` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `program`：类型为 `GLuint`。没有默认值，调用时必须提供。传入 `GLuint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLFunctions::glPixelStorei(GLenum pname, GLint param)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLFunctions::glPixelStorei` 用于执行与“gl、Pixel、Storei”相关的操作。调用时要先确认当前状态和 `pname`、`param` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `pname`：类型为 `GLenum`。没有默认值，调用时必须提供。枚举或标志参数。先确认可用枚举值、互斥关系和默认值，必要时用按位或组合标志。
- 参数 `param`：类型为 `GLint`。没有默认值，调用时必须提供。传入 `GLint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLFunctions::glPolygonOffset(GLfloat factor, GLfloat units)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLFunctions::glPolygonOffset` 用于执行与“gl、Polygon、Offset”相关的操作。调用时要先确认当前状态和 `factor`、`units` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `factor`：类型为 `GLfloat`。没有默认值，调用时必须提供。传入 `GLfloat` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `units`：类型为 `GLfloat`。没有默认值，调用时必须提供。传入 `GLfloat` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLFunctions::glReadPixels(GLint x, GLint y, GLsizei width, GLsizei height, GLenum format, GLenum type, GLvoid *pixels)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLFunctions::glReadPixels` 用于执行与“gl、读取、Pixels”相关的操作。调用时要先确认当前状态和 `x`、`y`、`width`、`height`、`format`、`type`、`pixels` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `x`：类型为 `GLint`。没有默认值，调用时必须提供。传入 `GLint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `y`：类型为 `GLint`。没有默认值，调用时必须提供。传入 `GLint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `width`：类型为 `GLsizei`。没有默认值，调用时必须提供。宽度，通常以像素、字符数或元素数量表示；要确认是否允许 0、负数和超出最大值。
- 参数 `height`：类型为 `GLsizei`。没有默认值，调用时必须提供。高度，通常以像素、字符数或元素数量表示；要确认是否允许 0、负数和超出最大值。
- 参数 `format`：类型为 `GLenum`。没有默认值，调用时必须提供。数据格式或显示格式。格式通常会影响解析、像素布局、精度、编码或兼容性。
- 参数 `type`：类型为 `GLenum`。没有默认值，调用时必须提供。类型、格式或策略枚举。要确认枚举值的适用范围和平台支持情况。
- 参数 `pixels`：类型为 `GLvoid *`。没有默认值，调用时必须提供。传入 `GLvoid *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLFunctions::glReleaseShaderCompiler()`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLFunctions::glReleaseShaderCompiler` 用于执行与“gl、释放、Shader、Compiler”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLFunctions::glRenderbufferStorage(GLenum target, GLenum internalformat, GLsizei width, GLsizei height)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLFunctions::glRenderbufferStorage` 用于执行与“gl、Renderbuffer、Storage”相关的操作。调用时要先确认当前状态和 `target`、`internalformat`、`width`、`height` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `target`：类型为 `GLenum`。没有默认值，调用时必须提供。目标对象、目标属性或目标资源。要确认它在操作期间仍然有效，并支持所需能力。
- 参数 `internalformat`：类型为 `GLenum`。没有默认值，调用时必须提供。枚举或标志参数。先确认可用枚举值、互斥关系和默认值，必要时用按位或组合标志。
- 参数 `width`：类型为 `GLsizei`。没有默认值，调用时必须提供。宽度，通常以像素、字符数或元素数量表示；要确认是否允许 0、负数和超出最大值。
- 参数 `height`：类型为 `GLsizei`。没有默认值，调用时必须提供。高度，通常以像素、字符数或元素数量表示；要确认是否允许 0、负数和超出最大值。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLFunctions::glSampleCoverage(GLclampf value, GLboolean invert)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLFunctions::glSampleCoverage` 用于执行与“gl、Sample、Coverage”相关的操作。调用时要先确认当前状态和 `value`、`invert` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `value`：类型为 `GLclampf`。没有默认值，调用时必须提供。要读取或写入的值。要确认类型转换、默认值、所有权以及写入后是否触发通知。
- 参数 `invert`：类型为 `GLboolean`。没有默认值，调用时必须提供。传入 `GLboolean` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLFunctions::glScissor(GLint x, GLint y, GLsizei width, GLsizei height)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLFunctions::glScissor` 用于执行与“gl、Scissor”相关的操作。调用时要先确认当前状态和 `x`、`y`、`width`、`height` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `x`：类型为 `GLint`。没有默认值，调用时必须提供。传入 `GLint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `y`：类型为 `GLint`。没有默认值，调用时必须提供。传入 `GLint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `width`：类型为 `GLsizei`。没有默认值，调用时必须提供。宽度，通常以像素、字符数或元素数量表示；要确认是否允许 0、负数和超出最大值。
- 参数 `height`：类型为 `GLsizei`。没有默认值，调用时必须提供。高度，通常以像素、字符数或元素数量表示；要确认是否允许 0、负数和超出最大值。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLFunctions::glShaderBinary(GLint n, const GLuint *shaders, GLenum binaryformat, const void *binary, GLint length)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLFunctions::glShaderBinary` 用于执行与“gl、Shader、Binary”相关的操作。调用时要先确认当前状态和 `n`、`shaders`、`binaryformat`、`binary`、`length` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `n`：类型为 `GLint`。没有默认值，调用时必须提供。传入 `GLint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `shaders`：类型为 `const GLuint *`。没有默认值，调用时必须提供。传入 `const GLuint *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `binaryformat`：类型为 `GLenum`。没有默认值，调用时必须提供。枚举或标志参数。先确认可用枚举值、互斥关系和默认值，必要时用按位或组合标志。
- 参数 `binary`：类型为 `const void *`。没有默认值，调用时必须提供。传入 `const void *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `length`：类型为 `GLint`。没有默认值，调用时必须提供。传入 `GLint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLFunctions::glShaderSource(GLuint shader, GLsizei count, const char **string, const GLint *length)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLFunctions::glShaderSource` 用于执行与“gl、Shader、来源”相关的操作。调用时要先确认当前状态和 `shader`、`count`、`string`、`length` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `shader`：类型为 `GLuint`。没有默认值，调用时必须提供。传入 `GLuint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `count`：类型为 `GLsizei`。没有默认值，调用时必须提供。传入 `GLsizei` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `string`：类型为 `const char **`。没有默认值，调用时必须提供。传入 `const char **` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `length`：类型为 `const GLint *`。没有默认值，调用时必须提供。传入 `const GLint *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLFunctions::glStencilFunc(GLenum func, GLint ref, GLuint mask)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLFunctions::glStencilFunc` 用于执行与“gl、Stencil、Func”相关的操作。调用时要先确认当前状态和 `func`、`ref`、`mask` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `func`：类型为 `GLenum`。没有默认值，调用时必须提供。枚举或标志参数。先确认可用枚举值、互斥关系和默认值，必要时用按位或组合标志。
- 参数 `ref`：类型为 `GLint`。没有默认值，调用时必须提供。传入 `GLint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `mask`：类型为 `GLuint`。没有默认值，调用时必须提供。传入 `GLuint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLFunctions::glStencilFuncSeparate(GLenum face, GLenum func, GLint ref, GLuint mask)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLFunctions::glStencilFuncSeparate` 用于执行与“gl、Stencil、Func、Separate”相关的操作。调用时要先确认当前状态和 `face`、`func`、`ref`、`mask` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `face`：类型为 `GLenum`。没有默认值，调用时必须提供。枚举或标志参数。先确认可用枚举值、互斥关系和默认值，必要时用按位或组合标志。
- 参数 `func`：类型为 `GLenum`。没有默认值，调用时必须提供。枚举或标志参数。先确认可用枚举值、互斥关系和默认值，必要时用按位或组合标志。
- 参数 `ref`：类型为 `GLint`。没有默认值，调用时必须提供。传入 `GLint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `mask`：类型为 `GLuint`。没有默认值，调用时必须提供。传入 `GLuint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLFunctions::glStencilMask(GLuint mask)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLFunctions::glStencilMask` 用于执行与“gl、Stencil、Mask”相关的操作。调用时要先确认当前状态和 `mask` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `mask`：类型为 `GLuint`。没有默认值，调用时必须提供。传入 `GLuint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLFunctions::glStencilMaskSeparate(GLenum face, GLuint mask)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLFunctions::glStencilMaskSeparate` 用于执行与“gl、Stencil、Mask、Separate”相关的操作。调用时要先确认当前状态和 `face`、`mask` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `face`：类型为 `GLenum`。没有默认值，调用时必须提供。枚举或标志参数。先确认可用枚举值、互斥关系和默认值，必要时用按位或组合标志。
- 参数 `mask`：类型为 `GLuint`。没有默认值，调用时必须提供。传入 `GLuint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLFunctions::glStencilOp(GLenum fail, GLenum zfail, GLenum zpass)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLFunctions::glStencilOp` 用于执行与“gl、Stencil、Op”相关的操作。调用时要先确认当前状态和 `fail`、`zfail`、`zpass` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `fail`：类型为 `GLenum`。没有默认值，调用时必须提供。枚举或标志参数。先确认可用枚举值、互斥关系和默认值，必要时用按位或组合标志。
- 参数 `zfail`：类型为 `GLenum`。没有默认值，调用时必须提供。枚举或标志参数。先确认可用枚举值、互斥关系和默认值，必要时用按位或组合标志。
- 参数 `zpass`：类型为 `GLenum`。没有默认值，调用时必须提供。枚举或标志参数。先确认可用枚举值、互斥关系和默认值，必要时用按位或组合标志。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLFunctions::glStencilOpSeparate(GLenum face, GLenum fail, GLenum zfail, GLenum zpass)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLFunctions::glStencilOpSeparate` 用于执行与“gl、Stencil、Op、Separate”相关的操作。调用时要先确认当前状态和 `face`、`fail`、`zfail`、`zpass` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `face`：类型为 `GLenum`。没有默认值，调用时必须提供。枚举或标志参数。先确认可用枚举值、互斥关系和默认值，必要时用按位或组合标志。
- 参数 `fail`：类型为 `GLenum`。没有默认值，调用时必须提供。枚举或标志参数。先确认可用枚举值、互斥关系和默认值，必要时用按位或组合标志。
- 参数 `zfail`：类型为 `GLenum`。没有默认值，调用时必须提供。枚举或标志参数。先确认可用枚举值、互斥关系和默认值，必要时用按位或组合标志。
- 参数 `zpass`：类型为 `GLenum`。没有默认值，调用时必须提供。枚举或标志参数。先确认可用枚举值、互斥关系和默认值，必要时用按位或组合标志。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLFunctions::glTexImage2D(GLenum target, GLint level, GLint internalformat, GLsizei width, GLsizei height, GLint border, GLenum format, GLenum type, const GLvoid *pixels)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLFunctions::glTexImage2D` 用于执行与“gl、Tex、Image、2、D”相关的操作。调用时要先确认当前状态和 `target`、`level`、`internalformat`、`width`、`height`、`border`、`format`、`type`、`pixels` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `target`：类型为 `GLenum`。没有默认值，调用时必须提供。目标对象、目标属性或目标资源。要确认它在操作期间仍然有效，并支持所需能力。
- 参数 `level`：类型为 `GLint`。没有默认值，调用时必须提供。传入 `GLint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `internalformat`：类型为 `GLint`。没有默认值，调用时必须提供。传入 `GLint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `width`：类型为 `GLsizei`。没有默认值，调用时必须提供。宽度，通常以像素、字符数或元素数量表示；要确认是否允许 0、负数和超出最大值。
- 参数 `height`：类型为 `GLsizei`。没有默认值，调用时必须提供。高度，通常以像素、字符数或元素数量表示；要确认是否允许 0、负数和超出最大值。
- 参数 `border`：类型为 `GLint`。没有默认值，调用时必须提供。传入 `GLint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `format`：类型为 `GLenum`。没有默认值，调用时必须提供。数据格式或显示格式。格式通常会影响解析、像素布局、精度、编码或兼容性。
- 参数 `type`：类型为 `GLenum`。没有默认值，调用时必须提供。类型、格式或策略枚举。要确认枚举值的适用范围和平台支持情况。
- 参数 `pixels`：类型为 `const GLvoid *`。没有默认值，调用时必须提供。传入 `const GLvoid *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLFunctions::glTexParameterf(GLenum target, GLenum pname, GLfloat param)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLFunctions::glTexParameterf` 用于执行与“gl、Tex、Parameterf”相关的操作。调用时要先确认当前状态和 `target`、`pname`、`param` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `target`：类型为 `GLenum`。没有默认值，调用时必须提供。目标对象、目标属性或目标资源。要确认它在操作期间仍然有效，并支持所需能力。
- 参数 `pname`：类型为 `GLenum`。没有默认值，调用时必须提供。枚举或标志参数。先确认可用枚举值、互斥关系和默认值，必要时用按位或组合标志。
- 参数 `param`：类型为 `GLfloat`。没有默认值，调用时必须提供。传入 `GLfloat` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLFunctions::glTexParameterfv(GLenum target, GLenum pname, const GLfloat *params)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLFunctions::glTexParameterfv` 用于执行与“gl、Tex、Parameterfv”相关的操作。调用时要先确认当前状态和 `target`、`pname`、`params` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `target`：类型为 `GLenum`。没有默认值，调用时必须提供。目标对象、目标属性或目标资源。要确认它在操作期间仍然有效，并支持所需能力。
- 参数 `pname`：类型为 `GLenum`。没有默认值，调用时必须提供。枚举或标志参数。先确认可用枚举值、互斥关系和默认值，必要时用按位或组合标志。
- 参数 `params`：类型为 `const GLfloat *`。没有默认值，调用时必须提供。传入 `const GLfloat *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLFunctions::glTexParameteri(GLenum target, GLenum pname, GLint param)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLFunctions::glTexParameteri` 用于执行与“gl、Tex、Parameteri”相关的操作。调用时要先确认当前状态和 `target`、`pname`、`param` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `target`：类型为 `GLenum`。没有默认值，调用时必须提供。目标对象、目标属性或目标资源。要确认它在操作期间仍然有效，并支持所需能力。
- 参数 `pname`：类型为 `GLenum`。没有默认值，调用时必须提供。枚举或标志参数。先确认可用枚举值、互斥关系和默认值，必要时用按位或组合标志。
- 参数 `param`：类型为 `GLint`。没有默认值，调用时必须提供。传入 `GLint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLFunctions::glTexParameteriv(GLenum target, GLenum pname, const GLint *params)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLFunctions::glTexParameteriv` 用于执行与“gl、Tex、Parameteriv”相关的操作。调用时要先确认当前状态和 `target`、`pname`、`params` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `target`：类型为 `GLenum`。没有默认值，调用时必须提供。目标对象、目标属性或目标资源。要确认它在操作期间仍然有效，并支持所需能力。
- 参数 `pname`：类型为 `GLenum`。没有默认值，调用时必须提供。枚举或标志参数。先确认可用枚举值、互斥关系和默认值，必要时用按位或组合标志。
- 参数 `params`：类型为 `const GLint *`。没有默认值，调用时必须提供。传入 `const GLint *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLFunctions::glTexSubImage2D(GLenum target, GLint level, GLint xoffset, GLint yoffset, GLsizei width, GLsizei height, GLenum format, GLenum type, const GLvoid *pixels)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLFunctions::glTexSubImage2D` 用于执行与“gl、Tex、Sub、Image、2、D”相关的操作。调用时要先确认当前状态和 `target`、`level`、`xoffset`、`yoffset`、`width`、`height`、`format`、`type`、`pixels` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `target`：类型为 `GLenum`。没有默认值，调用时必须提供。目标对象、目标属性或目标资源。要确认它在操作期间仍然有效，并支持所需能力。
- 参数 `level`：类型为 `GLint`。没有默认值，调用时必须提供。传入 `GLint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `xoffset`：类型为 `GLint`。没有默认值，调用时必须提供。传入 `GLint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `yoffset`：类型为 `GLint`。没有默认值，调用时必须提供。传入 `GLint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `width`：类型为 `GLsizei`。没有默认值，调用时必须提供。宽度，通常以像素、字符数或元素数量表示；要确认是否允许 0、负数和超出最大值。
- 参数 `height`：类型为 `GLsizei`。没有默认值，调用时必须提供。高度，通常以像素、字符数或元素数量表示；要确认是否允许 0、负数和超出最大值。
- 参数 `format`：类型为 `GLenum`。没有默认值，调用时必须提供。数据格式或显示格式。格式通常会影响解析、像素布局、精度、编码或兼容性。
- 参数 `type`：类型为 `GLenum`。没有默认值，调用时必须提供。类型、格式或策略枚举。要确认枚举值的适用范围和平台支持情况。
- 参数 `pixels`：类型为 `const GLvoid *`。没有默认值，调用时必须提供。传入 `const GLvoid *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLFunctions::glUniform1f(GLint location, GLfloat x)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLFunctions::glUniform1f` 用于执行与“gl、Uniform、1、f”相关的操作。调用时要先确认当前状态和 `location`、`x` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `location`：类型为 `GLint`。没有默认值，调用时必须提供。传入 `GLint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `x`：类型为 `GLfloat`。没有默认值，调用时必须提供。传入 `GLfloat` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLFunctions::glUniform1fv(GLint location, GLsizei count, const GLfloat *v)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLFunctions::glUniform1fv` 用于执行与“gl、Uniform、1、fv”相关的操作。调用时要先确认当前状态和 `location`、`count`、`v` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `location`：类型为 `GLint`。没有默认值，调用时必须提供。传入 `GLint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `count`：类型为 `GLsizei`。没有默认值，调用时必须提供。传入 `GLsizei` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `v`：类型为 `const GLfloat *`。没有默认值，调用时必须提供。传入 `const GLfloat *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLFunctions::glUniform1i(GLint location, GLint x)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLFunctions::glUniform1i` 用于执行与“gl、Uniform、1、i”相关的操作。调用时要先确认当前状态和 `location`、`x` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `location`：类型为 `GLint`。没有默认值，调用时必须提供。传入 `GLint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `x`：类型为 `GLint`。没有默认值，调用时必须提供。传入 `GLint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLFunctions::glUniform1iv(GLint location, GLsizei count, const GLint *v)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLFunctions::glUniform1iv` 用于执行与“gl、Uniform、1、iv”相关的操作。调用时要先确认当前状态和 `location`、`count`、`v` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `location`：类型为 `GLint`。没有默认值，调用时必须提供。传入 `GLint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `count`：类型为 `GLsizei`。没有默认值，调用时必须提供。传入 `GLsizei` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `v`：类型为 `const GLint *`。没有默认值，调用时必须提供。传入 `const GLint *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLFunctions::glUniform2f(GLint location, GLfloat x, GLfloat y)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLFunctions::glUniform2f` 用于执行与“gl、Uniform、2、f”相关的操作。调用时要先确认当前状态和 `location`、`x`、`y` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `location`：类型为 `GLint`。没有默认值，调用时必须提供。传入 `GLint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `x`：类型为 `GLfloat`。没有默认值，调用时必须提供。传入 `GLfloat` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `y`：类型为 `GLfloat`。没有默认值，调用时必须提供。传入 `GLfloat` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLFunctions::glUniform2fv(GLint location, GLsizei count, const GLfloat *v)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLFunctions::glUniform2fv` 用于执行与“gl、Uniform、2、fv”相关的操作。调用时要先确认当前状态和 `location`、`count`、`v` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `location`：类型为 `GLint`。没有默认值，调用时必须提供。传入 `GLint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `count`：类型为 `GLsizei`。没有默认值，调用时必须提供。传入 `GLsizei` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `v`：类型为 `const GLfloat *`。没有默认值，调用时必须提供。传入 `const GLfloat *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLFunctions::glUniform2i(GLint location, GLint x, GLint y)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLFunctions::glUniform2i` 用于执行与“gl、Uniform、2、i”相关的操作。调用时要先确认当前状态和 `location`、`x`、`y` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `location`：类型为 `GLint`。没有默认值，调用时必须提供。传入 `GLint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `x`：类型为 `GLint`。没有默认值，调用时必须提供。传入 `GLint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `y`：类型为 `GLint`。没有默认值，调用时必须提供。传入 `GLint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLFunctions::glUniform2iv(GLint location, GLsizei count, const GLint *v)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLFunctions::glUniform2iv` 用于执行与“gl、Uniform、2、iv”相关的操作。调用时要先确认当前状态和 `location`、`count`、`v` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `location`：类型为 `GLint`。没有默认值，调用时必须提供。传入 `GLint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `count`：类型为 `GLsizei`。没有默认值，调用时必须提供。传入 `GLsizei` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `v`：类型为 `const GLint *`。没有默认值，调用时必须提供。传入 `const GLint *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLFunctions::glUniform3f(GLint location, GLfloat x, GLfloat y, GLfloat z)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLFunctions::glUniform3f` 用于执行与“gl、Uniform、3、f”相关的操作。调用时要先确认当前状态和 `location`、`x`、`y`、`z` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `location`：类型为 `GLint`。没有默认值，调用时必须提供。传入 `GLint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `x`：类型为 `GLfloat`。没有默认值，调用时必须提供。传入 `GLfloat` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `y`：类型为 `GLfloat`。没有默认值，调用时必须提供。传入 `GLfloat` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `z`：类型为 `GLfloat`。没有默认值，调用时必须提供。传入 `GLfloat` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLFunctions::glUniform3fv(GLint location, GLsizei count, const GLfloat *v)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLFunctions::glUniform3fv` 用于执行与“gl、Uniform、3、fv”相关的操作。调用时要先确认当前状态和 `location`、`count`、`v` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `location`：类型为 `GLint`。没有默认值，调用时必须提供。传入 `GLint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `count`：类型为 `GLsizei`。没有默认值，调用时必须提供。传入 `GLsizei` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `v`：类型为 `const GLfloat *`。没有默认值，调用时必须提供。传入 `const GLfloat *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLFunctions::glUniform3i(GLint location, GLint x, GLint y, GLint z)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLFunctions::glUniform3i` 用于执行与“gl、Uniform、3、i”相关的操作。调用时要先确认当前状态和 `location`、`x`、`y`、`z` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `location`：类型为 `GLint`。没有默认值，调用时必须提供。传入 `GLint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `x`：类型为 `GLint`。没有默认值，调用时必须提供。传入 `GLint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `y`：类型为 `GLint`。没有默认值，调用时必须提供。传入 `GLint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `z`：类型为 `GLint`。没有默认值，调用时必须提供。传入 `GLint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLFunctions::glUniform3iv(GLint location, GLsizei count, const GLint *v)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLFunctions::glUniform3iv` 用于执行与“gl、Uniform、3、iv”相关的操作。调用时要先确认当前状态和 `location`、`count`、`v` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `location`：类型为 `GLint`。没有默认值，调用时必须提供。传入 `GLint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `count`：类型为 `GLsizei`。没有默认值，调用时必须提供。传入 `GLsizei` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `v`：类型为 `const GLint *`。没有默认值，调用时必须提供。传入 `const GLint *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLFunctions::glUniform4f(GLint location, GLfloat x, GLfloat y, GLfloat z, GLfloat w)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLFunctions::glUniform4f` 用于执行与“gl、Uniform、4、f”相关的操作。调用时要先确认当前状态和 `location`、`x`、`y`、`z`、`w` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `location`：类型为 `GLint`。没有默认值，调用时必须提供。传入 `GLint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `x`：类型为 `GLfloat`。没有默认值，调用时必须提供。传入 `GLfloat` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `y`：类型为 `GLfloat`。没有默认值，调用时必须提供。传入 `GLfloat` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `z`：类型为 `GLfloat`。没有默认值，调用时必须提供。传入 `GLfloat` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `w`：类型为 `GLfloat`。没有默认值，调用时必须提供。传入 `GLfloat` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLFunctions::glUniform4fv(GLint location, GLsizei count, const GLfloat *v)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLFunctions::glUniform4fv` 用于执行与“gl、Uniform、4、fv”相关的操作。调用时要先确认当前状态和 `location`、`count`、`v` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `location`：类型为 `GLint`。没有默认值，调用时必须提供。传入 `GLint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `count`：类型为 `GLsizei`。没有默认值，调用时必须提供。传入 `GLsizei` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `v`：类型为 `const GLfloat *`。没有默认值，调用时必须提供。传入 `const GLfloat *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLFunctions::glUniform4i(GLint location, GLint x, GLint y, GLint z, GLint w)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLFunctions::glUniform4i` 用于执行与“gl、Uniform、4、i”相关的操作。调用时要先确认当前状态和 `location`、`x`、`y`、`z`、`w` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `location`：类型为 `GLint`。没有默认值，调用时必须提供。传入 `GLint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `x`：类型为 `GLint`。没有默认值，调用时必须提供。传入 `GLint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `y`：类型为 `GLint`。没有默认值，调用时必须提供。传入 `GLint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `z`：类型为 `GLint`。没有默认值，调用时必须提供。传入 `GLint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `w`：类型为 `GLint`。没有默认值，调用时必须提供。传入 `GLint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLFunctions::glUniform4iv(GLint location, GLsizei count, const GLint *v)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLFunctions::glUniform4iv` 用于执行与“gl、Uniform、4、iv”相关的操作。调用时要先确认当前状态和 `location`、`count`、`v` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `location`：类型为 `GLint`。没有默认值，调用时必须提供。传入 `GLint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `count`：类型为 `GLsizei`。没有默认值，调用时必须提供。传入 `GLsizei` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `v`：类型为 `const GLint *`。没有默认值，调用时必须提供。传入 `const GLint *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLFunctions::glUniformMatrix2fv(GLint location, GLsizei count, GLboolean transpose, const GLfloat *value)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLFunctions::glUniformMatrix2fv` 用于执行与“gl、Uniform、Matrix、2、fv”相关的操作。调用时要先确认当前状态和 `location`、`count`、`transpose`、`value` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `location`：类型为 `GLint`。没有默认值，调用时必须提供。传入 `GLint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `count`：类型为 `GLsizei`。没有默认值，调用时必须提供。传入 `GLsizei` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `transpose`：类型为 `GLboolean`。没有默认值，调用时必须提供。传入 `GLboolean` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `value`：类型为 `const GLfloat *`。没有默认值，调用时必须提供。要读取或写入的值。要确认类型转换、默认值、所有权以及写入后是否触发通知。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLFunctions::glUniformMatrix3fv(GLint location, GLsizei count, GLboolean transpose, const GLfloat *value)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLFunctions::glUniformMatrix3fv` 用于执行与“gl、Uniform、Matrix、3、fv”相关的操作。调用时要先确认当前状态和 `location`、`count`、`transpose`、`value` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `location`：类型为 `GLint`。没有默认值，调用时必须提供。传入 `GLint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `count`：类型为 `GLsizei`。没有默认值，调用时必须提供。传入 `GLsizei` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `transpose`：类型为 `GLboolean`。没有默认值，调用时必须提供。传入 `GLboolean` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `value`：类型为 `const GLfloat *`。没有默认值，调用时必须提供。要读取或写入的值。要确认类型转换、默认值、所有权以及写入后是否触发通知。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLFunctions::glUniformMatrix4fv(GLint location, GLsizei count, GLboolean transpose, const GLfloat *value)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLFunctions::glUniformMatrix4fv` 用于执行与“gl、Uniform、Matrix、4、fv”相关的操作。调用时要先确认当前状态和 `location`、`count`、`transpose`、`value` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `location`：类型为 `GLint`。没有默认值，调用时必须提供。传入 `GLint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `count`：类型为 `GLsizei`。没有默认值，调用时必须提供。传入 `GLsizei` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `transpose`：类型为 `GLboolean`。没有默认值，调用时必须提供。传入 `GLboolean` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `value`：类型为 `const GLfloat *`。没有默认值，调用时必须提供。要读取或写入的值。要确认类型转换、默认值、所有权以及写入后是否触发通知。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLFunctions::glUseProgram(GLuint program)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLFunctions::glUseProgram` 用于执行与“gl、Use、Program”相关的操作。调用时要先确认当前状态和 `program` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `program`：类型为 `GLuint`。没有默认值，调用时必须提供。传入 `GLuint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLFunctions::glValidateProgram(GLuint program)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLFunctions::glValidateProgram` 用于执行与“gl、Validate、Program”相关的操作。调用时要先确认当前状态和 `program` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `program`：类型为 `GLuint`。没有默认值，调用时必须提供。传入 `GLuint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLFunctions::glVertexAttrib1f(GLuint indx, GLfloat x)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLFunctions::glVertexAttrib1f` 用于执行与“gl、Vertex、Attrib、1、f”相关的操作。调用时要先确认当前状态和 `indx`、`x` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `indx`：类型为 `GLuint`。没有默认值，调用时必须提供。传入 `GLuint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `x`：类型为 `GLfloat`。没有默认值，调用时必须提供。传入 `GLfloat` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLFunctions::glVertexAttrib1fv(GLuint indx, const GLfloat *values)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLFunctions::glVertexAttrib1fv` 用于执行与“gl、Vertex、Attrib、1、fv”相关的操作。调用时要先确认当前状态和 `indx`、`values` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `indx`：类型为 `GLuint`。没有默认值，调用时必须提供。传入 `GLuint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `values`：类型为 `const GLfloat *`。没有默认值，调用时必须提供。传入 `const GLfloat *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLFunctions::glVertexAttrib2f(GLuint indx, GLfloat x, GLfloat y)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLFunctions::glVertexAttrib2f` 用于执行与“gl、Vertex、Attrib、2、f”相关的操作。调用时要先确认当前状态和 `indx`、`x`、`y` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `indx`：类型为 `GLuint`。没有默认值，调用时必须提供。传入 `GLuint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `x`：类型为 `GLfloat`。没有默认值，调用时必须提供。传入 `GLfloat` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `y`：类型为 `GLfloat`。没有默认值，调用时必须提供。传入 `GLfloat` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLFunctions::glVertexAttrib2fv(GLuint indx, const GLfloat *values)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLFunctions::glVertexAttrib2fv` 用于执行与“gl、Vertex、Attrib、2、fv”相关的操作。调用时要先确认当前状态和 `indx`、`values` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `indx`：类型为 `GLuint`。没有默认值，调用时必须提供。传入 `GLuint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `values`：类型为 `const GLfloat *`。没有默认值，调用时必须提供。传入 `const GLfloat *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLFunctions::glVertexAttrib3f(GLuint indx, GLfloat x, GLfloat y, GLfloat z)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLFunctions::glVertexAttrib3f` 用于执行与“gl、Vertex、Attrib、3、f”相关的操作。调用时要先确认当前状态和 `indx`、`x`、`y`、`z` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `indx`：类型为 `GLuint`。没有默认值，调用时必须提供。传入 `GLuint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `x`：类型为 `GLfloat`。没有默认值，调用时必须提供。传入 `GLfloat` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `y`：类型为 `GLfloat`。没有默认值，调用时必须提供。传入 `GLfloat` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `z`：类型为 `GLfloat`。没有默认值，调用时必须提供。传入 `GLfloat` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLFunctions::glVertexAttrib3fv(GLuint indx, const GLfloat *values)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLFunctions::glVertexAttrib3fv` 用于执行与“gl、Vertex、Attrib、3、fv”相关的操作。调用时要先确认当前状态和 `indx`、`values` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `indx`：类型为 `GLuint`。没有默认值，调用时必须提供。传入 `GLuint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `values`：类型为 `const GLfloat *`。没有默认值，调用时必须提供。传入 `const GLfloat *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLFunctions::glVertexAttrib4f(GLuint indx, GLfloat x, GLfloat y, GLfloat z, GLfloat w)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLFunctions::glVertexAttrib4f` 用于执行与“gl、Vertex、Attrib、4、f”相关的操作。调用时要先确认当前状态和 `indx`、`x`、`y`、`z`、`w` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `indx`：类型为 `GLuint`。没有默认值，调用时必须提供。传入 `GLuint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `x`：类型为 `GLfloat`。没有默认值，调用时必须提供。传入 `GLfloat` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `y`：类型为 `GLfloat`。没有默认值，调用时必须提供。传入 `GLfloat` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `z`：类型为 `GLfloat`。没有默认值，调用时必须提供。传入 `GLfloat` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `w`：类型为 `GLfloat`。没有默认值，调用时必须提供。传入 `GLfloat` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLFunctions::glVertexAttrib4fv(GLuint indx, const GLfloat *values)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLFunctions::glVertexAttrib4fv` 用于执行与“gl、Vertex、Attrib、4、fv”相关的操作。调用时要先确认当前状态和 `indx`、`values` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `indx`：类型为 `GLuint`。没有默认值，调用时必须提供。传入 `GLuint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `values`：类型为 `const GLfloat *`。没有默认值，调用时必须提供。传入 `const GLfloat *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLFunctions::glVertexAttribPointer(GLuint indx, GLint size, GLenum type, GLboolean normalized, GLsizei stride, const void *ptr)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLFunctions::glVertexAttribPointer` 用于执行与“gl、Vertex、Attrib、Pointer”相关的操作。调用时要先确认当前状态和 `indx`、`size`、`type`、`normalized`、`stride`、`ptr` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `indx`：类型为 `GLuint`。没有默认值，调用时必须提供。传入 `GLuint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `size`：类型为 `GLint`。没有默认值，调用时必须提供。尺寸或长度，单位通常是像素、字节、元素数或时间，必须结合类型和类的上下文确认。
- 参数 `type`：类型为 `GLenum`。没有默认值，调用时必须提供。类型、格式或策略枚举。要确认枚举值的适用范围和平台支持情况。
- 参数 `normalized`：类型为 `GLboolean`。没有默认值，调用时必须提供。传入 `GLboolean` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `stride`：类型为 `GLsizei`。没有默认值，调用时必须提供。传入 `GLsizei` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `ptr`：类型为 `const void *`。没有默认值，调用时必须提供。传入 `const void *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLFunctions::glViewport(GLint x, GLint y, GLsizei width, GLsizei height)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLFunctions::glViewport` 用于执行与“gl、Viewport”相关的操作。调用时要先确认当前状态和 `x`、`y`、`width`、`height` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `x`：类型为 `GLint`。没有默认值，调用时必须提供。传入 `GLint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `y`：类型为 `GLint`。没有默认值，调用时必须提供。传入 `GLint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `width`：类型为 `GLsizei`。没有默认值，调用时必须提供。宽度，通常以像素、字符数或元素数量表示；要确认是否允许 0、负数和超出最大值。
- 参数 `height`：类型为 `GLsizei`。没有默认值，调用时必须提供。高度，通常以像素、字符数或元素数量表示；要确认是否允许 0、负数和超出最大值。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QOpenGLFunctions::hasOpenGLFeature(QOpenGLFunctions::OpenGLFeature feature) const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `hasOpenGLFeature`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数 `feature`：类型为 `QOpenGLFunctions::OpenGLFeature`。没有默认值，调用时必须提供。传入 `QOpenGLFunctions::OpenGLFeature` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLFunctions::initializeOpenGLFunctions()`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLFunctions::initializeOpenGLFunctions` 用于执行与“initialize、打开、GL、Functions”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QOpenGLFunctions::OpenGLFeatures QOpenGLFunctions::openGLFeatures() const`

**API 类别：** 成员函数说明

**中文解读：** 这是启动/建立资源的 API `openGLFeatures`。调用前准备依赖和参数，调用后检查返回值或状态信号；成功后通常需要配套的 stop/close/end/disconnect 或释放操作。

**签名拆解：**

- 返回值：`QOpenGLFunctions::OpenGLFeatures`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `enum OpenGLFeature { Multitexture, Shaders, Buffers, Framebuffers, BlendColor, …, MultipleRenderTargets }`

**API 类别：** 公有类型

**中文解读：** 这是 `QOpenGLFunctions` 暴露的类型声明 `打开、GL、Feature`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 这是供该类其他 API 使用的枚举/标志类型；传值前要确认枚举值的语义和适用状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `flags OpenGLFeatures`

**API 类别：** 公有类型

**中文解读：** 这是 `QOpenGLFunctions` 的 `标志` 成员声明。它通常作为其他 API 的类型、常量或配置入口使用；先确认可用值和适用状态，再结合本类的创建、核心操作和清理流程使用。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

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
