# QOpenGLExtraFunctions

> Qt 6.11.1 · Qt GUI

## 1. 先建立直觉

**一句话定位：** 这是 GUI 基础类型，常用于绘制、输入、图像、字体或窗口系统集成。

**模块背景：** Qt GUI 负责窗口系统集成、绘制、颜色、字体、图像、输入事件和底层 GUI 资源。

### 这是什么

`QOpenGLExtraFunctions` 是 Qt 类型机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 这个类的行为由它的继承关系、构造参数、公开状态和成员函数协议共同决定。使用时要把创建、配置、核心操作、结果/通知和清理看成一条闭环，而不是孤立调用某个函数。

**适用场景：** 围绕这个类的核心职责建立最小闭环：准备依赖 -> 创建/取得对象 -> 设置必要配置 -> 调用核心 API -> 检查返回值和状态 -> 处理结果/错误 -> 结束时清理。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要忽略构造失败、空返回、默认值和版本限制；不要把异步 API 当同步 API；不要在没有确认所有权和线程的情况下保存指针或跨线程调用。

## 2. 依赖与对象关系

- 头文件：`#include <QOpenGLExtraFunctions>`
- 继承自：QOpenGLFunctions
- 直接派生类：未在类页中列出

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

### 公有函数

- `QOpenGLExtraFunctions()`
- `QOpenGLExtraFunctions(QOpenGLContext *context)`
- `void glActiveShaderProgram(GLuint pipeline, GLuint program)`
- `void glBeginQuery(GLenum target, GLuint id)`
- `void glBeginTransformFeedback(GLenum primitiveMode)`
- `void glBindBufferBase(GLenum target, GLuint index, GLuint buffer)`
- `void glBindBufferRange(GLenum target, GLuint index, GLuint buffer, GLintptr offset, GLsizeiptr size)`
- `void glBindImageTexture(GLuint unit, GLuint texture, GLint level, GLboolean layered, GLint layer, GLenum access, GLenum format)`
- `void glBindProgramPipeline(GLuint pipeline)`
- `void glBindSampler(GLuint unit, GLuint sampler)`
- `void glBindTransformFeedback(GLenum target, GLuint id)`
- `void glBindVertexArray(GLuint array)`
- `void glBindVertexBuffer(GLuint bindingindex, GLuint buffer, GLintptr offset, GLsizei stride)`
- `void glBlendBarrier()`
- `void glBlendEquationSeparatei(GLuint buf, GLenum modeRGB, GLenum modeAlpha)`
- `void glBlendEquationi(GLuint buf, GLenum mode)`
- `void glBlendFuncSeparatei(GLuint buf, GLenum srcRGB, GLenum dstRGB, GLenum srcAlpha, GLenum dstAlpha)`
- `void glBlendFunci(GLuint buf, GLenum src, GLenum dst)`
- `void glBlitFramebuffer(GLint srcX0, GLint srcY0, GLint srcX1, GLint srcY1, GLint dstX0, GLint dstY0, GLint dstX1, GLint dstY1, GLbitfield mask, GLenum filter)`
- `void glClearBufferfi(GLenum buffer, GLint drawbuffer, GLfloat depth, GLint stencil)`
- `void glClearBufferfv(GLenum buffer, GLint drawbuffer, const GLfloat *value)`
- `void glClearBufferiv(GLenum buffer, GLint drawbuffer, const GLint *value)`
- `void glClearBufferuiv(GLenum buffer, GLint drawbuffer, const GLuint *value)`
- `GLenum glClientWaitSync(GLsync sync, GLbitfield flags, GLuint64 timeout)`
- `void glColorMaski(GLuint index, GLboolean r, GLboolean g, GLboolean b, GLboolean a)`
- `void glCompressedTexImage3D(GLenum target, GLint level, GLenum internalformat, GLsizei width, GLsizei height, GLsizei depth, GLint border, GLsizei imageSize, const void *data)`
- `void glCompressedTexSubImage3D(GLenum target, GLint level, GLint xoffset, GLint yoffset, GLint zoffset, GLsizei width, GLsizei height, GLsizei depth, GLenum format, GLsizei imageSize, const void *data)`
- `void glCopyBufferSubData(GLenum readTarget, GLenum writeTarget, GLintptr readOffset, GLintptr writeOffset, GLsizeiptr size)`
- `void glCopyImageSubData(GLuint srcName, GLenum srcTarget, GLint srcLevel, GLint srcX, GLint srcY, GLint srcZ, GLuint dstName, GLenum dstTarget, GLint dstLevel, GLint dstX, GLint dstY, GLint dstZ, GLsizei srcWidth, GLsizei srcHeight, GLsizei srcDepth)`
- `void glCopyTexSubImage3D(GLenum target, GLint level, GLint xoffset, GLint yoffset, GLint zoffset, GLint x, GLint y, GLsizei width, GLsizei height)`
- `GLuint glCreateShaderProgramv(GLenum type, GLsizei count, const GLchar *const *strings)`
- `void glDebugMessageCallback(GLDEBUGPROC callback, const void *userParam)`
- `void glDebugMessageControl(GLenum source, GLenum type, GLenum severity, GLsizei count, const GLuint *ids, GLboolean enabled)`
- `void glDebugMessageInsert(GLenum source, GLenum type, GLuint id, GLenum severity, GLsizei length, const GLchar *buf)`
- `void glDeleteProgramPipelines(GLsizei n, const GLuint *pipelines)`
- `void glDeleteQueries(GLsizei n, const GLuint *ids)`
- `void glDeleteSamplers(GLsizei count, const GLuint *samplers)`
- `void glDeleteSync(GLsync sync)`
- `void glDeleteTransformFeedbacks(GLsizei n, const GLuint *ids)`
- `void glDeleteVertexArrays(GLsizei n, const GLuint *arrays)`
- `void glDisablei(GLenum target, GLuint index)`
- `void glDispatchCompute(GLuint num_groups_x, GLuint num_groups_y, GLuint num_groups_z)`
- `void glDispatchComputeIndirect(GLintptr indirect)`
- `void glDrawArraysIndirect(GLenum mode, const void *indirect)`
- `void glDrawArraysInstanced(GLenum mode, GLint first, GLsizei count, GLsizei instancecount)`
- `void glDrawBuffers(GLsizei n, const GLenum *bufs)`
- `void glDrawElementsBaseVertex(GLenum mode, GLsizei count, GLenum type, const void *indices, GLint basevertex)`
- `void glDrawElementsIndirect(GLenum mode, GLenum type, const void *indirect)`
- `void glDrawElementsInstanced(GLenum mode, GLsizei count, GLenum type, const void *indices, GLsizei instancecount)`
- `void glDrawElementsInstancedBaseVertex(GLenum mode, GLsizei count, GLenum type, const void *indices, GLsizei instancecount, GLint basevertex)`
- `void glDrawRangeElements(GLenum mode, GLuint start, GLuint end, GLsizei count, GLenum type, const void *indices)`
- `void glDrawRangeElementsBaseVertex(GLenum mode, GLuint start, GLuint end, GLsizei count, GLenum type, const void *indices, GLint basevertex)`
- `void glEnablei(GLenum target, GLuint index)`
- `void glEndQuery(GLenum target)`
- `void glEndTransformFeedback()`
- `GLsync glFenceSync(GLenum condition, GLbitfield flags)`
- `void glFlushMappedBufferRange(GLenum target, GLintptr offset, GLsizeiptr length)`
- `void glFramebufferParameteri(GLenum target, GLenum pname, GLint param)`
- `void glFramebufferTexture(GLenum target, GLenum attachment, GLuint texture, GLint level)`
- `void glFramebufferTextureLayer(GLenum target, GLenum attachment, GLuint texture, GLint level, GLint layer)`
- `void glGenProgramPipelines(GLsizei n, GLuint *pipelines)`
- `void glGenQueries(GLsizei n, GLuint *ids)`
- `void glGenSamplers(GLsizei count, GLuint *samplers)`
- `void glGenTransformFeedbacks(GLsizei n, GLuint *ids)`
- `void glGenVertexArrays(GLsizei n, GLuint *arrays)`
- `void glGetActiveUniformBlockName(GLuint program, GLuint uniformBlockIndex, GLsizei bufSize, GLsizei *length, GLchar *uniformBlockName)`
- `void glGetActiveUniformBlockiv(GLuint program, GLuint uniformBlockIndex, GLenum pname, GLint *params)`
- `void glGetActiveUniformsiv(GLuint program, GLsizei uniformCount, const GLuint *uniformIndices, GLenum pname, GLint *params)`
- `void glGetBooleani_v(GLenum target, GLuint index, GLboolean *data)`
- `void glGetBufferParameteri64v(GLenum target, GLenum pname, GLint64 *params)`
- `void glGetBufferPointerv(GLenum target, GLenum pname, void **params)`
- `GLuint glGetDebugMessageLog(GLuint count, GLsizei bufSize, GLenum *sources, GLenum *types, GLuint *ids, GLenum *severities, GLsizei *lengths, GLchar *messageLog)`
- `GLint glGetFragDataLocation(GLuint program, const GLchar *name)`
- `void glGetFramebufferParameteriv(GLenum target, GLenum pname, GLint *params)`
- `GLenum glGetGraphicsResetStatus()`
- `void glGetInteger64i_v(GLenum target, GLuint index, GLint64 *data)`
- `void glGetInteger64v(GLenum pname, GLint64 *data)`
- `void glGetIntegeri_v(GLenum target, GLuint index, GLint *data)`
- `void glGetInternalformativ(GLenum target, GLenum internalformat, GLenum pname, GLsizei bufSize, GLint *params)`
- `void glGetMultisamplefv(GLenum pname, GLuint index, GLfloat *val)`
- `void glGetObjectLabel(GLenum identifier, GLuint name, GLsizei bufSize, GLsizei *length, GLchar *label)`
- `void glGetObjectPtrLabel(const void *ptr, GLsizei bufSize, GLsizei *length, GLchar *label)`
- `void glGetPointerv(GLenum pname, void **params)`
- `void glGetProgramBinary(GLuint program, GLsizei bufSize, GLsizei *length, GLenum *binaryFormat, void *binary)`
- `void glGetProgramInterfaceiv(GLuint program, GLenum programInterface, GLenum pname, GLint *params)`
- `void glGetProgramPipelineInfoLog(GLuint pipeline, GLsizei bufSize, GLsizei *length, GLchar *infoLog)`
- `void glGetProgramPipelineiv(GLuint pipeline, GLenum pname, GLint *params)`
- `GLuint glGetProgramResourceIndex(GLuint program, GLenum programInterface, const GLchar *name)`
- `GLint glGetProgramResourceLocation(GLuint program, GLenum programInterface, const GLchar *name)`
- `void glGetProgramResourceName(GLuint program, GLenum programInterface, GLuint index, GLsizei bufSize, GLsizei *length, GLchar *name)`
- `void glGetProgramResourceiv(GLuint program, GLenum programInterface, GLuint index, GLsizei propCount, const GLenum *props, GLsizei bufSize, GLsizei *length, GLint *params)`
- `void glGetQueryObjectuiv(GLuint id, GLenum pname, GLuint *params)`
- `void glGetQueryiv(GLenum target, GLenum pname, GLint *params)`
- `void glGetSamplerParameterIiv(GLuint sampler, GLenum pname, GLint *params)`
- `void glGetSamplerParameterIuiv(GLuint sampler, GLenum pname, GLuint *params)`
- `void glGetSamplerParameterfv(GLuint sampler, GLenum pname, GLfloat *params)`
- `void glGetSamplerParameteriv(GLuint sampler, GLenum pname, GLint *params)`
- `const GLubyte * glGetStringi(GLenum name, GLuint index)`
- `void glGetSynciv(GLsync sync, GLenum pname, GLsizei bufSize, GLsizei *length, GLint *values)`
- `void glGetTexLevelParameterfv(GLenum target, GLint level, GLenum pname, GLfloat *params)`
- `void glGetTexLevelParameteriv(GLenum target, GLint level, GLenum pname, GLint *params)`
- `void glGetTexParameterIiv(GLenum target, GLenum pname, GLint *params)`
- `void glGetTexParameterIuiv(GLenum target, GLenum pname, GLuint *params)`
- `void glGetTransformFeedbackVarying(GLuint program, GLuint index, GLsizei bufSize, GLsizei *length, GLsizei *size, GLenum *type, GLchar *name)`
- `GLuint glGetUniformBlockIndex(GLuint program, const GLchar *uniformBlockName)`
- `void glGetUniformIndices(GLuint program, GLsizei uniformCount, const GLchar *const *uniformNames, GLuint *uniformIndices)`
- `void glGetUniformuiv(GLuint program, GLint location, GLuint *params)`
- `void glGetVertexAttribIiv(GLuint index, GLenum pname, GLint *params)`
- `void glGetVertexAttribIuiv(GLuint index, GLenum pname, GLuint *params)`
- `void glGetnUniformfv(GLuint program, GLint location, GLsizei bufSize, GLfloat *params)`
- `void glGetnUniformiv(GLuint program, GLint location, GLsizei bufSize, GLint *params)`
- `void glGetnUniformuiv(GLuint program, GLint location, GLsizei bufSize, GLuint *params)`
- `void glInvalidateFramebuffer(GLenum target, GLsizei numAttachments, const GLenum *attachments)`
- `void glInvalidateSubFramebuffer(GLenum target, GLsizei numAttachments, const GLenum *attachments, GLint x, GLint y, GLsizei width, GLsizei height)`
- `GLboolean glIsEnabledi(GLenum target, GLuint index)`
- `GLboolean glIsProgramPipeline(GLuint pipeline)`
- `GLboolean glIsQuery(GLuint id)`
- `GLboolean glIsSampler(GLuint sampler)`
- `GLboolean glIsSync(GLsync sync)`
- `GLboolean glIsTransformFeedback(GLuint id)`
- `GLboolean glIsVertexArray(GLuint array)`
- `void * glMapBufferRange(GLenum target, GLintptr offset, GLsizeiptr length, GLbitfield access)`
- `void glMemoryBarrier(GLbitfield barriers)`
- `void glMemoryBarrierByRegion(GLbitfield barriers)`
- `void glMinSampleShading(GLfloat value)`
- `void glObjectLabel(GLenum identifier, GLuint name, GLsizei length, const GLchar *label)`
- `void glObjectPtrLabel(const void *ptr, GLsizei length, const GLchar *label)`
- `void glPatchParameteri(GLenum pname, GLint value)`
- `void glPauseTransformFeedback()`
- `void glPopDebugGroup()`
- `void glPrimitiveBoundingBox(GLfloat minX, GLfloat minY, GLfloat minZ, GLfloat minW, GLfloat maxX, GLfloat maxY, GLfloat maxZ, GLfloat maxW)`
- `void glProgramBinary(GLuint program, GLenum binaryFormat, const void *binary, GLsizei length)`
- `void glProgramParameteri(GLuint program, GLenum pname, GLint value)`
- `void glProgramUniform1f(GLuint program, GLint location, GLfloat v0)`
- `void glProgramUniform1fv(GLuint program, GLint location, GLsizei count, const GLfloat *value)`
- `void glProgramUniform1i(GLuint program, GLint location, GLint v0)`
- `void glProgramUniform1iv(GLuint program, GLint location, GLsizei count, const GLint *value)`
- `void glProgramUniform1ui(GLuint program, GLint location, GLuint v0)`
- `void glProgramUniform1uiv(GLuint program, GLint location, GLsizei count, const GLuint *value)`
- `void glProgramUniform2f(GLuint program, GLint location, GLfloat v0, GLfloat v1)`
- `void glProgramUniform2fv(GLuint program, GLint location, GLsizei count, const GLfloat *value)`
- `void glProgramUniform2i(GLuint program, GLint location, GLint v0, GLint v1)`
- `void glProgramUniform2iv(GLuint program, GLint location, GLsizei count, const GLint *value)`
- `void glProgramUniform2ui(GLuint program, GLint location, GLuint v0, GLuint v1)`
- `void glProgramUniform2uiv(GLuint program, GLint location, GLsizei count, const GLuint *value)`
- `void glProgramUniform3f(GLuint program, GLint location, GLfloat v0, GLfloat v1, GLfloat v2)`
- `void glProgramUniform3fv(GLuint program, GLint location, GLsizei count, const GLfloat *value)`
- `void glProgramUniform3i(GLuint program, GLint location, GLint v0, GLint v1, GLint v2)`
- `void glProgramUniform3iv(GLuint program, GLint location, GLsizei count, const GLint *value)`
- `void glProgramUniform3ui(GLuint program, GLint location, GLuint v0, GLuint v1, GLuint v2)`
- `void glProgramUniform3uiv(GLuint program, GLint location, GLsizei count, const GLuint *value)`
- `void glProgramUniform4f(GLuint program, GLint location, GLfloat v0, GLfloat v1, GLfloat v2, GLfloat v3)`
- `void glProgramUniform4fv(GLuint program, GLint location, GLsizei count, const GLfloat *value)`
- `void glProgramUniform4i(GLuint program, GLint location, GLint v0, GLint v1, GLint v2, GLint v3)`
- `void glProgramUniform4iv(GLuint program, GLint location, GLsizei count, const GLint *value)`
- `void glProgramUniform4ui(GLuint program, GLint location, GLuint v0, GLuint v1, GLuint v2, GLuint v3)`
- `void glProgramUniform4uiv(GLuint program, GLint location, GLsizei count, const GLuint *value)`
- `void glProgramUniformMatrix2fv(GLuint program, GLint location, GLsizei count, GLboolean transpose, const GLfloat *value)`
- `void glProgramUniformMatrix2x3fv(GLuint program, GLint location, GLsizei count, GLboolean transpose, const GLfloat *value)`
- `void glProgramUniformMatrix2x4fv(GLuint program, GLint location, GLsizei count, GLboolean transpose, const GLfloat *value)`
- `void glProgramUniformMatrix3fv(GLuint program, GLint location, GLsizei count, GLboolean transpose, const GLfloat *value)`
- `void glProgramUniformMatrix3x2fv(GLuint program, GLint location, GLsizei count, GLboolean transpose, const GLfloat *value)`
- `void glProgramUniformMatrix3x4fv(GLuint program, GLint location, GLsizei count, GLboolean transpose, const GLfloat *value)`
- `void glProgramUniformMatrix4fv(GLuint program, GLint location, GLsizei count, GLboolean transpose, const GLfloat *value)`
- `void glProgramUniformMatrix4x2fv(GLuint program, GLint location, GLsizei count, GLboolean transpose, const GLfloat *value)`
- `void glProgramUniformMatrix4x3fv(GLuint program, GLint location, GLsizei count, GLboolean transpose, const GLfloat *value)`
- `void glPushDebugGroup(GLenum source, GLuint id, GLsizei length, const GLchar *message)`
- `void glReadBuffer(GLenum src)`
- `void glReadnPixels(GLint x, GLint y, GLsizei width, GLsizei height, GLenum format, GLenum type, GLsizei bufSize, void *data)`
- `void glRenderbufferStorageMultisample(GLenum target, GLsizei samples, GLenum internalformat, GLsizei width, GLsizei height)`
- `void glResumeTransformFeedback()`
- `void glSampleMaski(GLuint maskNumber, GLbitfield mask)`
- `void glSamplerParameterIiv(GLuint sampler, GLenum pname, const GLint *param)`
- `void glSamplerParameterIuiv(GLuint sampler, GLenum pname, const GLuint *param)`
- `void glSamplerParameterf(GLuint sampler, GLenum pname, GLfloat param)`
- `void glSamplerParameterfv(GLuint sampler, GLenum pname, const GLfloat *param)`
- `void glSamplerParameteri(GLuint sampler, GLenum pname, GLint param)`
- `void glSamplerParameteriv(GLuint sampler, GLenum pname, const GLint *param)`
- `void glTexBuffer(GLenum target, GLenum internalformat, GLuint buffer)`
- `void glTexBufferRange(GLenum target, GLenum internalformat, GLuint buffer, GLintptr offset, GLsizeiptr size)`
- `void glTexImage3D(GLenum target, GLint level, GLint internalformat, GLsizei width, GLsizei height, GLsizei depth, GLint border, GLenum format, GLenum type, const void *pixels)`
- `void glTexParameterIiv(GLenum target, GLenum pname, const GLint *params)`
- `void glTexParameterIuiv(GLenum target, GLenum pname, const GLuint *params)`
- `void glTexStorage2D(GLenum target, GLsizei levels, GLenum internalformat, GLsizei width, GLsizei height)`
- `void glTexStorage2DMultisample(GLenum target, GLsizei samples, GLenum internalformat, GLsizei width, GLsizei height, GLboolean fixedsamplelocations)`
- `void glTexStorage3D(GLenum target, GLsizei levels, GLenum internalformat, GLsizei width, GLsizei height, GLsizei depth)`
- `void glTexStorage3DMultisample(GLenum target, GLsizei samples, GLenum internalformat, GLsizei width, GLsizei height, GLsizei depth, GLboolean fixedsamplelocations)`
- `void glTexSubImage3D(GLenum target, GLint level, GLint xoffset, GLint yoffset, GLint zoffset, GLsizei width, GLsizei height, GLsizei depth, GLenum format, GLenum type, const void *pixels)`
- `void glTransformFeedbackVaryings(GLuint program, GLsizei count, const GLchar *const *varyings, GLenum bufferMode)`
- `void glUniform1ui(GLint location, GLuint v0)`
- `void glUniform1uiv(GLint location, GLsizei count, const GLuint *value)`
- `void glUniform2ui(GLint location, GLuint v0, GLuint v1)`
- `void glUniform2uiv(GLint location, GLsizei count, const GLuint *value)`
- `void glUniform3ui(GLint location, GLuint v0, GLuint v1, GLuint v2)`
- `void glUniform3uiv(GLint location, GLsizei count, const GLuint *value)`
- `void glUniform4ui(GLint location, GLuint v0, GLuint v1, GLuint v2, GLuint v3)`
- `void glUniform4uiv(GLint location, GLsizei count, const GLuint *value)`
- `void glUniformBlockBinding(GLuint program, GLuint uniformBlockIndex, GLuint uniformBlockBinding)`
- `void glUniformMatrix2x3fv(GLint location, GLsizei count, GLboolean transpose, const GLfloat *value)`
- `void glUniformMatrix2x4fv(GLint location, GLsizei count, GLboolean transpose, const GLfloat *value)`
- `void glUniformMatrix3x2fv(GLint location, GLsizei count, GLboolean transpose, const GLfloat *value)`
- `void glUniformMatrix3x4fv(GLint location, GLsizei count, GLboolean transpose, const GLfloat *value)`
- `void glUniformMatrix4x2fv(GLint location, GLsizei count, GLboolean transpose, const GLfloat *value)`
- `void glUniformMatrix4x3fv(GLint location, GLsizei count, GLboolean transpose, const GLfloat *value)`
- `GLboolean glUnmapBuffer(GLenum target)`
- `void glUseProgramStages(GLuint pipeline, GLbitfield stages, GLuint program)`
- `void glValidateProgramPipeline(GLuint pipeline)`
- `void glVertexAttribBinding(GLuint attribindex, GLuint bindingindex)`
- `void glVertexAttribDivisor(GLuint index, GLuint divisor)`
- `void glVertexAttribFormat(GLuint attribindex, GLint size, GLenum type, GLboolean normalized, GLuint relativeoffset)`
- `void glVertexAttribI4i(GLuint index, GLint x, GLint y, GLint z, GLint w)`
- `void glVertexAttribI4iv(GLuint index, const GLint *v)`
- `void glVertexAttribI4ui(GLuint index, GLuint x, GLuint y, GLuint z, GLuint w)`
- `void glVertexAttribI4uiv(GLuint index, const GLuint *v)`
- `void glVertexAttribIFormat(GLuint attribindex, GLint size, GLenum type, GLuint relativeoffset)`
- `void glVertexAttribIPointer(GLuint index, GLint size, GLenum type, GLsizei stride, const void *pointer)`
- `void glVertexBindingDivisor(GLuint bindingindex, GLuint divisor)`
- `void glWaitSync(GLsync sync, GLbitfield flags, GLuint64 timeout)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `QOpenGLExtraFunctions::QOpenGLExtraFunctions()`

**作用与语义：**

构造一个默认函数解析器。解析器必须先调用`initializeOpenGLFunctions()`指定上下文。

### `QOpenGLExtraFunctions::QOpenGLExtraFunctions(QOpenGLContext *context)`

**作用与语义：**

构造一个函数解析器以实现上下文。如果`context` `nullptr`，则为当前`QOpenGLContext`创建该解析器。
该群体中的上下文或其他上下文必须是当前的。
以这种方式构建的对象只能与上下文及其他共享上下文一起使用。使用`initializeOpenGLFunctions()`来更改对象的上下文关联。

### `void QOpenGLExtraFunctions::glActiveShaderProgram(GLuint pipeline, GLuint program)`

**作用与语义：**

调用glActiveShaderProgram（`pipeline`， `program`）的便利函数。
该函数仅在 OpenGL ES 3.x 或 OpenGL 3.x 或 4.x 上下文中可用。在运行纯 OpenGL 时，该函数仅在该配置文件和版本中包含该函数核心或扩展时可用。
欲了解更多信息，请参阅 OpenGL ES 3.x 关于 glActiveShaderProgram() 的文档。

### `void QOpenGLExtraFunctions::glBeginQuery(GLenum target, GLuint id)`

**作用与语义：**

调用 glBeginQuery（`target`， `id`） 的便利函数。
该函数仅在 OpenGL ES 3.x 或 OpenGL 3.x 或 4.x 上下文中可用。在运行纯 OpenGL 时，该函数仅在该配置文件和版本中包含该函数核心或扩展时可用。
欲了解更多信息，请参阅 OpenGL ES 3.x 关于 glBeginQuery() 的文档。

### `void QOpenGLExtraFunctions::glBeginTransformFeedback(GLenum primitiveMode)`

**作用与语义：**

调用 glBeginTransformFeedback（`primitiveMode`） 的便利函数。
该函数仅在 OpenGL ES 3.x 或 OpenGL 3.x 或 4.x 上下文中可用。在运行纯 OpenGL 时，该函数仅在该配置文件和版本中包含该函数核心或扩展时可用。
更多信息请参见 OpenGL ES 3.x 关于 glBeginTransformFeedback() 的文档。

### `void QOpenGLExtraFunctions::glBindBufferBase(GLenum target, GLuint index, GLuint buffer)`

**作用与语义：**

调用glBindBufferBase（`target`， `index`， `buffer`）的便利函数。
该函数仅在 OpenGL ES 3.x 或 OpenGL 3.x 或 4.x 上下文中可用。在运行纯 OpenGL 时，该函数仅在该配置文件和版本中包含该函数核心或扩展时可用。
更多信息请参见 OpenGL ES 3.x 关于 glBindBufferBase() 的文档。

### `void QOpenGLExtraFunctions::glBindBufferRange(GLenum target, GLuint index, GLuint buffer, GLintptr offset, GLsizeiptr size)`

**作用与语义：**

调用glBindBufferRange（`target`， `index`， `buffer`， `offset`， `size`的便利函数）。
该函数仅在 OpenGL ES 3.x 或 OpenGL 3.x 或 4.x 上下文中可用。在运行纯 OpenGL 时，该函数仅在该配置文件和版本中包含该函数核心或扩展时可用。
欲了解更多信息，请参阅 OpenGL ES 3.x 关于 glBindBufferRange() 的文档。

### `void QOpenGLExtraFunctions::glBindImageTexture(GLuint unit, GLuint texture, GLint level, GLboolean layered, GLint layer, GLenum access, GLenum format)`

**作用与语义：**

调用 glBindImageTexture（`unit`， `texture`， `level`， `layered`， `layer`， `access`， `format` 的便利函数。
该函数仅在 OpenGL ES 3.x 或 OpenGL 3.x 或 4.x 上下文中可用。在运行纯 OpenGL 时，该函数仅在该配置文件和版本中包含该函数核心或扩展时可用。
更多信息请参见 OpenGL ES 3.x 关于 glBindImageTexture（ 的文档）。

### `void QOpenGLExtraFunctions::glBindProgramPipeline(GLuint pipeline)`

**作用与语义：**

调用 glBindProgramPipeline（`pipeline`） 的便利函数。
该函数仅在 OpenGL ES 3.x 或 OpenGL 3.x 或 4.x 上下文中可用。在运行纯 OpenGL 时，该函数仅在该配置文件和版本中包含该函数核心或扩展时可用。
欲了解更多信息，请参阅 OpenGL ES 3.x 关于 glBindProgramPipeline() 的文档。

### `void QOpenGLExtraFunctions::glBindSampler(GLuint unit, GLuint sampler)`

**作用与语义：**

调用glBindSampler（`unit`， `sampler`）的便利函数。
该函数仅在 OpenGL ES 3.x 或 OpenGL 3.x 或 4.x 上下文中可用。在运行纯 OpenGL 时，该函数仅在该配置文件和版本中包含该函数核心或扩展时可用。
更多信息请参见 OpenGL ES 3.x 关于 glBindSampler() 的文档。

### `void QOpenGLExtraFunctions::glBindTransformFeedback(GLenum target, GLuint id)`

**作用与语义：**

调用 glBindTransformFeedback（`target`， `id`） 的便利函数。
该函数仅在 OpenGL ES 3.x 或 OpenGL 3.x 或 4.x 上下文中可用。在运行纯 OpenGL 时，该函数仅在该配置文件和版本中包含该函数核心或扩展时可用。
更多信息请参见 OpenGL ES 3.x 关于 glBindTransformFeedback() 的文档。

### `void QOpenGLExtraFunctions::glBindVertexArray(GLuint array)`

**作用与语义：**

调用glBindVertexArray（`array`）的便利函数。
该函数仅在 OpenGL ES 3.x 或 OpenGL 3.x 或 4.x 上下文中可用。在运行纯 OpenGL 时，该函数仅在该配置文件和版本中包含该函数核心或扩展时可用。
更多信息请参见 OpenGL ES 3.x 关于 glBindVertexArray() 的文档。

### `void QOpenGLExtraFunctions::glBindVertexBuffer(GLuint bindingindex, GLuint buffer, GLintptr offset, GLsizei stride)`

**作用与语义：**

调用 glBindVertexBuffer（`bindingindex`， `buffer`， `offset`， `stride` 的便利函数）。
该函数仅在 OpenGL ES 3.x 或 OpenGL 3.x 或 4.x 上下文中可用。在运行纯 OpenGL 时，该函数仅在该配置文件和版本中包含该函数核心或扩展时可用。
欲了解更多信息，请参阅 OpenGL ES 3.x 关于 glBindVertexBuffer() 的文档。

### `void QOpenGLExtraFunctions::glBlendBarrier()`

**作用与语义：**

调用 glBlendBarrier() 的便利函数。
该函数仅在 OpenGL ES 3.x 或 OpenGL 3.x 或 4.x 上下文中可用。在运行纯 OpenGL 时，该函数仅在该配置文件和版本中包含该函数核心或扩展时可用。
欲了解更多信息，请参阅 glBlendBarrier() 的 OpenGL ES 3.X 文档。

### `void QOpenGLExtraFunctions::glBlendEquationSeparatei(GLuint buf, GLenum modeRGB, GLenum modeAlpha)`

**作用与语义：**

调用glBlendEquationSeparatei（`buf`， `modeRGB`， `modeAlpha`）的便利函数。
该函数仅在 OpenGL ES 3.x 或 OpenGL 3.x 或 4.x 上下文中可用。在运行纯 OpenGL 时，该函数仅在该配置文件和版本中包含该函数核心或扩展时可用。
更多信息请参见 OpenGL ES 3.X 关于 glBlendEquationSeparatei() 的文档。

### `void QOpenGLExtraFunctions::glBlendEquationi(GLuint buf, GLenum mode)`

**作用与语义：**

调用glBlendEquationi（`buf`， `mode`）的便利函数。
该函数仅在 OpenGL ES 3.x 或 OpenGL 3.x 或 4.x 上下文中可用。在运行纯 OpenGL 时，该函数仅在该配置文件和版本中包含该函数核心或扩展时可用。
更多信息请参见 OpenGL ES 3.X 关于 glBlendEquationi() 的文档。

### `void QOpenGLExtraFunctions::glBlendFuncSeparatei(GLuint buf, GLenum srcRGB, GLenum dstRGB, GLenum srcAlpha, GLenum dstAlpha)`

**作用与语义：**

调用glBlendFuncSeparatei（`buf`， `srcRGB`， `dstRGB`， `srcAlpha`， `dstAlpha`）的便利函数。
该函数仅在 OpenGL ES 3.x 或 OpenGL 3.x 或 4.x 上下文中可用。在运行纯 OpenGL 时，该函数仅在该配置文件和版本中包含该函数核心或扩展时可用。
欲了解更多信息，请参阅 OpenGL ES 3.X 关于 glBlendFuncSeparatei() 的文档。

### `void QOpenGLExtraFunctions::glBlendFunci(GLuint buf, GLenum src, GLenum dst)`

**作用与语义：**

调用glBlendFunci（`buf`， `src`， `dst`）的便利函数。
该函数仅在 OpenGL ES 3.x 或 OpenGL 3.x 或 4.x 上下文中可用。在运行纯 OpenGL 时，该函数仅在该配置文件和版本中包含该函数核心或扩展时可用。
更多信息请参见 glBlendFunci() 的 OpenGL ES 3.X 文档。

### `void QOpenGLExtraFunctions::glBlitFramebuffer(GLint srcX0, GLint srcY0, GLint srcX1, GLint srcY1, GLint dstX0, GLint dstY0, GLint dstX1, GLint dstY1, GLbitfield mask, GLenum filter)`

**作用与语义：**

方便函数调用glBlitFramebuffer（`srcX0`、`srcY0`、`srcX1`、`srcY1`、`dstX0`、`dstY0`、`dstX1`、`dstY1`、`mask`、`filter`）。
该函数仅在 OpenGL ES 3.x 或 OpenGL 3.x 或 4.x 上下文中可用。在运行纯 OpenGL 时，该函数仅在该配置文件和版本中包含该函数核心或扩展时可用。
欲了解更多信息，请参阅 OpenGL ES 3.x 关于 glBlitFramebuffer() 的文档。

### `void QOpenGLExtraFunctions::glClearBufferfi(GLenum buffer, GLint drawbuffer, GLfloat depth, GLint stencil)`

**作用与语义：**

调用glClearBufferfi（`buffer`， `drawbuffer`， `depth`， `stencil`的便利函数）。
该函数仅在 OpenGL ES 3.x 或 OpenGL 3.x 或 4.x 上下文中可用。在运行纯 OpenGL 时，该函数仅在该配置文件和版本中包含该函数核心或扩展时可用。
更多信息请参见 OpenGL ES 3.x 关于 glClearBufferfi() 的文档。

### `void QOpenGLExtraFunctions::glClearBufferfv(GLenum buffer, GLint drawbuffer, const GLfloat *value)`

**作用与语义：**

调用glClearBufferfv（`buffer`， `drawbuffer`， `value`）的便利函数。
该函数仅在 OpenGL ES 3.x 或 OpenGL 3.x 或 4.x 上下文中可用。在运行纯 OpenGL 时，该函数仅在该配置文件和版本中包含该函数核心或扩展时可用。
更多信息请参见 OpenGL ES 3.x 关于 glClearBufferfv() 的文档。

### `void QOpenGLExtraFunctions::glClearBufferiv(GLenum buffer, GLint drawbuffer, const GLint *value)`

**作用与语义：**

调用glClearBufferiv（`buffer`， `drawbuffer`， `value`）的便利函数。
该函数仅在 OpenGL ES 3.x 或 OpenGL 3.x 或 4.x 上下文中可用。在运行纯 OpenGL 时，该函数仅在该配置文件和版本中包含该函数核心或扩展时可用。
更多信息请参见 OpenGL ES 3.x 关于 glClearBufferiv() 的文档。

### `void QOpenGLExtraFunctions::glClearBufferuiv(GLenum buffer, GLint drawbuffer, const GLuint *value)`

**作用与语义：**

调用glClearBufferuiv（`buffer`， `drawbuffer`， `value`）的便利函数。
该函数仅在 OpenGL ES 3.x 或 OpenGL 3.x 或 4.x 上下文中可用。在运行纯 OpenGL 时，该函数仅在该配置文件和版本中包含该函数核心或扩展时可用。
更多信息请参见 OpenGL ES 3.x 关于 glClearBufferuiv() 的文档。

### `GLenum QOpenGLExtraFunctions::glClientWaitSync(GLsync sync, GLbitfield flags, GLuint64 timeout)`

**作用与语义：**

调用 glClientWaitSync（`sync`， `flags`， `timeout` 的便利函数）。
该函数仅在 OpenGL ES 3.x 或 OpenGL 3.x 或 4.x 上下文中可用。在运行纯 OpenGL 时，该函数仅在该配置文件和版本中包含该函数核心或扩展时可用。
欲了解更多信息，请参阅 OpenGL ES 3.x 关于 glClientWaitSync() 的文档。

### `void QOpenGLExtraFunctions::glColorMaski(GLuint index, GLboolean r, GLboolean g, GLboolean b, GLboolean a)`

**作用与语义：**

调用glColorMaski（`index`、`r`、`g`、`b`、`a`）的便利函数。
该函数仅在 OpenGL ES 3.x 或 OpenGL 3.x 或 4.x 上下文中可用。在运行纯 OpenGL 时，该函数仅在该配置文件和版本中包含该函数核心或扩展时可用。
欲了解更多信息，请参阅 glColorMaski() 的 OpenGL ES 3.X 文档。

### `void QOpenGLExtraFunctions::glCompressedTexImage3D(GLenum target, GLint level, GLenum internalformat, GLsizei width, GLsizei height, GLsizei depth, GLint border, GLsizei imageSize, const void *data)`

**作用与语义：**

调用 glCompressedTexImage3D（`target`， `level`， `internalformat`， `width`， `height`， `depth`， `border`， `imageSize`， `data` 的便利函数。
该函数仅在 OpenGL ES 3.x 或 OpenGL 3.x 或 4.x 上下文中可用。在运行纯 OpenGL 时，该函数仅在该配置文件和版本中包含该函数核心或扩展时可用。
欲了解更多信息，请参阅 glCompressedTexImage3D() 的 OpenGL ES 3.x 文档。

### `void QOpenGLExtraFunctions::glCompressedTexSubImage3D(GLenum target, GLint level, GLint xoffset, GLint yoffset, GLint zoffset, GLsizei width, GLsizei height, GLsizei depth, GLenum format, GLsizei imageSize, const void *data)`

**作用与语义：**

方便函数调用 glComCompressedTexSubImage3D（`target`， `level`， `xoffset`， `yoffset`， `zoffset`， `width`， `height`， `depth`， `format`， `imageSize`， `data`）。
该函数仅在 OpenGL ES 3.x 或 OpenGL 3.x 或 4.x 上下文中可用。在运行纯 OpenGL 时，该函数仅在该配置文件和版本中包含该函数核心或扩展时可用。
更多信息请参见 glCompressedTexSubImage3D() 的 OpenGL ES 3.x 文档。

### `void QOpenGLExtraFunctions::glCopyBufferSubData(GLenum readTarget, GLenum writeTarget, GLintptr readOffset, GLintptr writeOffset, GLsizeiptr size)`

**作用与语义：**

调用glCopyBufferSubData（`readTarget`、`writeTarget`、`readOffset`、`writeOffset`、`size`）的便利函数。
该函数仅在 OpenGL ES 3.x 或 OpenGL 3.x 或 4.x 上下文中可用。在运行纯 OpenGL 时，该函数仅在该配置文件和版本中包含该函数核心或扩展时可用。
欲了解更多信息，请参见 OpenGL ES 3.x 关于 glCopyBufferSubData() 的文档。

### `void QOpenGLExtraFunctions::glCopyImageSubData(GLuint srcName, GLenum srcTarget, GLint srcLevel, GLint srcX, GLint srcY, GLint srcZ, GLuint dstName, GLenum dstTarget, GLint dstLevel, GLint dstX, GLint dstY, GLint dstZ, GLsizei srcWidth, GLsizei srcHeight, GLsizei srcDepth)`

**作用与语义：**

调用 glCopyImageSubData（`srcName`、`srcTarget`、`srcLevel`、`srcX`、`srcY`、`srcZ`、`dstName`、`dstTarget`、`dstLevel`、`dstX`、`dstY`、`dstZ`、`srcWidth`、`srcHeight`、`srcDepth`）的便利函数。
该函数仅在 OpenGL ES 3.x 或 OpenGL 3.x 或 4.x 上下文中可用。在运行纯 OpenGL 时，该函数仅在该配置文件和版本中包含该函数核心或扩展时可用。
欲了解更多信息，请参阅 OpenGL ES 3.X 关于 glCopyImageSubData() 的文档。

### `void QOpenGLExtraFunctions::glCopyTexSubImage3D(GLenum target, GLint level, GLint xoffset, GLint yoffset, GLint zoffset, GLint x, GLint y, GLsizei width, GLsizei height)`

**作用与语义：**

调用glCopyTexSubImage3D（`target`、`level`、`xoffset`、`yoffset`、`zoffset`、`x`、`y`、`width`、`height`）的便利功能。
该函数仅在 OpenGL ES 3.x 或 OpenGL 3.x 或 4.x 上下文中可用。在运行纯 OpenGL 时，该函数仅在该配置文件和版本中包含该函数核心或扩展时可用。
更多信息请参见 OpenGL ES 3.x 关于 glCopyTexSubImage3D() 的文档。

### `GLuint QOpenGLExtraFunctions::glCreateShaderProgramv(GLenum type, GLsizei count, const GLchar *const *strings)`

**作用与语义：**

调用glCreateShaderProgramv（`type`， `count`， `strings`）的便利函数。
该函数仅在 OpenGL ES 3.x 或 OpenGL 3.x 或 4.x 上下文中可用。在运行纯 OpenGL 时，该函数仅在该配置文件和版本中包含该函数核心或扩展时可用。
更多信息请参见 glCreateShaderProgramv() 的 OpenGL ES 3.x 文档。

### `void QOpenGLExtraFunctions::glDebugMessageCallback(GLDEBUGPROC callback, const void *userParam)`

**作用与语义：**

调用glDebugMessageCallback（`callback`， `userParam`）的便利函数。
该函数仅在 OpenGL ES 3.x 或 OpenGL 3.x 或 4.x 上下文中可用。在运行纯 OpenGL 时，该函数仅在该配置文件和版本中包含该函数核心或扩展时可用。
更多信息请参阅 OpenGL ES 3.X 关于 glDebugMessageCallback() 的文档。

### `void QOpenGLExtraFunctions::glDebugMessageControl(GLenum source, GLenum type, GLenum severity, GLsizei count, const GLuint *ids, GLboolean enabled)`

**作用与语义：**

调用glDebugMessageControl（`source`、`type`、`severity`、`count`、`ids`、`enabled`）的便利函数。
该函数仅在 OpenGL ES 3.x 或 OpenGL 3.x 或 4.x 上下文中可用。在运行纯 OpenGL 时，该函数仅在该配置文件和版本中包含该函数核心或扩展时可用。
欲了解更多信息，请参阅 OpenGL ES 3.X 关于 glDebugMessageContro() 的文档。

### `void QOpenGLExtraFunctions::glDebugMessageInsert(GLenum source, GLenum type, GLuint id, GLenum severity, GLsizei length, const GLchar *buf)`

**作用与语义：**

调用 glDebugMessageInsert（`source`， `type`， `id`， `severity`， `length`， `buf` 的便利函数。
该函数仅在 OpenGL ES 3.x 或 OpenGL 3.x 或 4.x 上下文中可用。在运行纯 OpenGL 时，该函数仅在该配置文件和版本中包含该函数核心或扩展时可用。
欲了解更多信息，请参阅 OpenGL ES 3.X 关于 glDebugMessageInsert() 的文档。

### `void QOpenGLExtraFunctions::glDeleteProgramPipelines(GLsizei n, const GLuint *pipelines)`

**作用与语义：**

调用glDeleteProgramPipelines（`n`， `pipelines`）的便利函数。
该函数仅在 OpenGL ES 3.x 或 OpenGL 3.x 或 4.x 上下文中可用。在运行纯 OpenGL 时，该函数仅在该配置文件和版本中包含该函数核心或扩展时可用。
欲了解更多信息，请参见 OpenGL ES 3.x 关于 glDeleteProgramPipelines() 的文档。

### `void QOpenGLExtraFunctions::glDeleteQueries(GLsizei n, const GLuint *ids)`

**作用与语义：**

调用glDeleteQueries（`n`， `ids`）的便利函数。
该函数仅在 OpenGL ES 3.x 或 OpenGL 3.x 或 4.x 上下文中可用。在运行纯 OpenGL 时，该函数仅在该配置文件和版本中包含该函数核心或扩展时可用。
更多信息请参见 OpenGL ES 3.x 关于 glDeleteQueries() 的文档。

### `void QOpenGLExtraFunctions::glDeleteSamplers(GLsizei count, const GLuint *samplers)`

**作用与语义：**

调用glDeleteSamplers（`count`， `samplers`）的便利函数。
该函数仅在 OpenGL ES 3.x 或 OpenGL 3.x 或 4.x 上下文中可用。在运行纯 OpenGL 时，该函数仅在该配置文件和版本中包含该函数核心或扩展时可用。
欲了解更多信息，请参阅 OpenGL ES 3.x 关于 glDeleteSamplers() 的文档。

### `void QOpenGLExtraFunctions::glDeleteSync(GLsync sync)`

**作用与语义：**

调用glDeleteSync（`sync`）的便利函数。
该函数仅在 OpenGL ES 3.x 或 OpenGL 3.x 或 4.x 上下文中可用。在运行纯 OpenGL 时，该函数仅在该配置文件和版本中包含该函数核心或扩展时可用。
更多信息请参见 OpenGL ES 3.x 关于 glDeleteSync() 的文档。

### `void QOpenGLExtraFunctions::glDeleteTransformFeedbacks(GLsizei n, const GLuint *ids)`

**作用与语义：**

调用 glDeleteTransformFeedbacks（`n`， `ids`）的便利函数。
该函数仅在 OpenGL ES 3.x 或 OpenGL 3.x 或 4.x 上下文中可用。在运行纯 OpenGL 时，该函数仅在该配置文件和版本中包含该函数核心或扩展时可用。
欲了解更多信息，请参阅 OpenGL ES 3.x 关于 glDeleteTransformFeedbacks() 的文档。

### `void QOpenGLExtraFunctions::glDeleteVertexArrays(GLsizei n, const GLuint *arrays)`

**作用与语义：**

调用glDeleteVertexArrays（`n`， `arrays`）的便利函数。
该函数仅在 OpenGL ES 3.x 或 OpenGL 3.x 或 4.x 上下文中可用。在运行纯 OpenGL 时，该函数仅在该配置文件和版本中包含该函数核心或扩展时可用。
欲了解更多信息，请参阅 OpenGL ES 3.x 关于 glDeleteVertexArrays() 的文档。

### `void QOpenGLExtraFunctions::glDisablei(GLenum target, GLuint index)`

**作用与语义：**

调用 glDisablei（`target`， `index`） 的便利函数。
该函数仅在 OpenGL ES 3.x 或 OpenGL 3.x 或 4.x 上下文中可用。在运行纯 OpenGL 时，该函数仅在该配置文件和版本中包含该函数核心或扩展时可用。
更多信息请参见 glDisablei() 的 OpenGL ES 3.X 文档。

### `void QOpenGLExtraFunctions::glDispatchCompute(GLuint num_groups_x, GLuint num_groups_y, GLuint num_groups_z)`

**作用与语义：**

调用glDispatchCompute（`num_groups_x`， `num_groups_y`， `num_groups_z`）的便利函数。
该函数仅在 OpenGL ES 3.x 或 OpenGL 3.x 或 4.x 上下文中可用。在运行纯 OpenGL 时，该函数仅在该配置文件和版本中包含该函数核心或扩展时可用。
欲了解更多信息，请参阅 glDispatchCompute() 的 OpenGL ES 3.x 文档。

### `void QOpenGLExtraFunctions::glDispatchComputeIndirect(GLintptr indirect)`

**作用与语义：**

调用glDispatchComputeIndirect（`indirect`）的便利函数。
该函数仅在 OpenGL ES 3.x 或 OpenGL 3.x 或 4.x 上下文中可用。在运行纯 OpenGL 时，该函数仅在该配置文件和版本中包含该函数核心或扩展时可用。
欲了解更多信息，请参阅 glDispatchComputeIndirect() 的 OpenGL ES 3.x 文档。

### `void QOpenGLExtraFunctions::glDrawArraysIndirect(GLenum mode, const void *indirect)`

**作用与语义：**

调用glDrawArraysIndirect（`mode`， `indirect`）的便利函数。
该函数仅在 OpenGL ES 3.x 或 OpenGL 3.x 或 4.x 上下文中可用。在运行纯 OpenGL 时，该函数仅在该配置文件和版本中包含该函数核心或扩展时可用。
更多信息请参见 OpenGL ES 3.x 关于 glDrawArraysIndirect() 的文档。

### `void QOpenGLExtraFunctions::glDrawArraysInstanced(GLenum mode, GLint first, GLsizei count, GLsizei instancecount)`

**作用与语义：**

调用glDrawArraysInstanced（`mode`， `first`， `count`， `instancecount`的便利函数）。
该函数仅在 OpenGL ES 3.x 或 OpenGL 3.x 或 4.x 上下文中可用。在运行纯 OpenGL 时，该函数仅在该配置文件和版本中包含该函数核心或扩展时可用。
欲了解更多信息，请参阅 OpenGL ES 3.x 关于 glDrawArraysInstanced() 的文档。

### `void QOpenGLExtraFunctions::glDrawBuffers(GLsizei n, const GLenum *bufs)`

**作用与语义：**

调用glDrawBuffers（`n`， `bufs`）的便利函数。
该函数仅在 OpenGL ES 3.x 或 OpenGL 3.x 或 4.x 上下文中可用。在运行纯 OpenGL 时，该函数仅在该配置文件和版本中包含该函数核心或扩展时可用。
更多信息请参见 OpenGL ES 3.x 关于 glDrawBuffers() 的文档。

### `void QOpenGLExtraFunctions::glDrawElementsBaseVertex(GLenum mode, GLsizei count, GLenum type, const void *indices, GLint basevertex)`

**作用与语义：**

调用 glDrawElementsBaseVertex（`mode`， `count`， `type`， `indices`， `basevertex` 的便利函数）。
该函数仅在 OpenGL ES 3.x 或 OpenGL 3.x 或 4.x 上下文中可用。在运行纯 OpenGL 时，该函数仅在该配置文件和版本中包含该函数核心或扩展时可用。
更多信息请参见 OpenGL ES 3.X 关于 glDrawElementsBaseVerte() 的文档。

### `void QOpenGLExtraFunctions::glDrawElementsIndirect(GLenum mode, GLenum type, const void *indirect)`

**作用与语义：**

调用glDrawElementsIndirect（`mode`， `type`， `indirect`）的便利函数。
该函数仅在 OpenGL ES 3.x 或 OpenGL 3.x 或 4.x 上下文中可用。在运行纯 OpenGL 时，该函数仅在该配置文件和版本中包含该函数核心或扩展时可用。
更多信息请参见 OpenGL ES 3.x 关于 glDrawElementsIndirect() 的文档。

### `void QOpenGLExtraFunctions::glDrawElementsInstanced(GLenum mode, GLsizei count, GLenum type, const void *indices, GLsizei instancecount)`

**作用与语义：**

调用 glDrawElementsInstanced（`mode`， `count`， `type`， `indices`， `instancecount` 的便利函数。
该函数仅在 OpenGL ES 3.x 或 OpenGL 3.x 或 4.x 上下文中可用。在运行纯 OpenGL 时，该函数仅在该配置文件和版本中包含该函数核心或扩展时可用。
更多信息请参见 OpenGL ES 3.x 关于 glDrawElementsInstanced() 的文档。

### `void QOpenGLExtraFunctions::glDrawElementsInstancedBaseVertex(GLenum mode, GLsizei count, GLenum type, const void *indices, GLsizei instancecount, GLint basevertex)`

**作用与语义：**

调用 glDrawElementsInstancedBaseVertex（`mode`， `count`， `type`， `indices`， `instancecount`， `basevertex` 的便利函数。
该函数仅在 OpenGL ES 3.x 或 OpenGL 3.x 或 4.x 上下文中可用。在运行纯 OpenGL 时，该函数仅在该配置文件和版本中包含该函数核心或扩展时可用。
欲了解更多信息，请参阅 OpenGL ES 3.X 关于 glDrawElementsInstancedBaseVerte() 的文档。

### `void QOpenGLExtraFunctions::glDrawRangeElements(GLenum mode, GLuint start, GLuint end, GLsizei count, GLenum type, const void *indices)`

**作用与语义：**

调用 glDrawRangeElements（`mode`， `start`， `end`， `count`， `type`， `indices` 的便利函数。
该函数仅在 OpenGL ES 3.x 或 OpenGL 3.x 或 4.x 上下文中可用。在运行纯 OpenGL 时，该函数仅在该配置文件和版本中包含该函数核心或扩展时可用。
更多信息请参阅 OpenGL ES 3.x 关于 glDrawRangeElements() 的文档。

### `void QOpenGLExtraFunctions::glDrawRangeElementsBaseVertex(GLenum mode, GLuint start, GLuint end, GLsizei count, GLenum type, const void *indices, GLint basevertex)`

**作用与语义：**

调用 glDrawRangeElementsBaseVertex（`mode`， `start`， `end`， `count`， `type`， `indices`， `basevertex` 的便利函数）。
该函数仅在 OpenGL ES 3.x 或 OpenGL 3.x 或 4.x 上下文中可用。在运行纯 OpenGL 时，该函数仅在该配置文件和版本中包含该函数核心或扩展时可用。
更多信息请参见 OpenGL ES 3.X 关于 glDrawRangeElementsBaseVerte() 的文档。

### `void QOpenGLExtraFunctions::glEnablei(GLenum target, GLuint index)`

**作用与语义：**

调用 glEnablei（`target`， `index`） 的便利函数。
该函数仅在 OpenGL ES 3.x 或 OpenGL 3.x 或 4.x 上下文中可用。在运行纯 OpenGL 时，该函数仅在该配置文件和版本中包含该函数核心或扩展时可用。
更多信息请参见 OpenGL ES 3.X 关于 glEnablei() 的文档。

### `void QOpenGLExtraFunctions::glEndQuery(GLenum target)`

**作用与语义：**

调用 glEndQuery（`target`） 的便利函数。
该函数仅在 OpenGL ES 3.x 或 OpenGL 3.x 或 4.x 上下文中可用。在运行纯 OpenGL 时，该函数仅在该配置文件和版本中包含该函数核心或扩展时可用。
欲了解更多信息，请参阅 OpenGL ES 3.x 关于 glEndQuery() 的文档。

### `void QOpenGLExtraFunctions::glEndTransformFeedback()`

**作用与语义：**

调用glEndTransformFeedback()的便利函数。
该函数仅在 OpenGL ES 3.x 或 OpenGL 3.x 或 4.x 上下文中可用。在运行纯 OpenGL 时，该函数仅在该配置文件和版本中包含该函数核心或扩展时可用。
更多信息请参见 OpenGL ES 3.x 关于 glEndTransformFeedback() 的文档。

### `GLsync QOpenGLExtraFunctions::glFenceSync(GLenum condition, GLbitfield flags)`

**作用与语义：**

调用 glFenceSync（`condition`， `flags`） 的便利功能。
该函数仅在 OpenGL ES 3.x 或 OpenGL 3.x 或 4.x 上下文中可用。在运行纯 OpenGL 时，该函数仅在该配置文件和版本中包含该函数核心或扩展时可用。
欲了解更多信息，请参阅 openGL ES 3.x 关于 glFenceSync() 的文档。

### `void QOpenGLExtraFunctions::glFlushMappedBufferRange(GLenum target, GLintptr offset, GLsizeiptr length)`

**作用与语义：**

调用glFlushMappedBufferRange（`target`， `offset`， `length`）的便利函数。
该函数仅在 OpenGL ES 3.x 或 OpenGL 3.x 或 4.x 上下文中可用。在运行纯 OpenGL 时，该函数仅在该配置文件和版本中包含该函数核心或扩展时可用。
更多信息请参见 OpenGL ES 3.x 关于 glFlushMappedBufferRange() 的文档。

### `void QOpenGLExtraFunctions::glFramebufferParameteri(GLenum target, GLenum pname, GLint param)`

**作用与语义：**

调用 glFramebufferParameteri（`target`， `pname`， `param` 的便利函数）。
该函数仅在 OpenGL ES 3.x 或 OpenGL 3.x 或 4.x 上下文中可用。在运行纯 OpenGL 时，该函数仅在该配置文件和版本中包含该函数核心或扩展时可用。
欲了解更多信息，请参阅 OpenGL ES 3.x 关于 glFramebufferParameteri() 的文档。

### `void QOpenGLExtraFunctions::glFramebufferTexture(GLenum target, GLenum attachment, GLuint texture, GLint level)`

**作用与语义：**

调用glFramebufferTexture（`target`， `attachment`， `texture`， `level`的便利函数）。
该函数仅在 OpenGL ES 3.x 或 OpenGL 3.x 或 4.x 上下文中可用。在运行纯 OpenGL 时，该函数仅在该配置文件和版本中包含该函数核心或扩展时可用。
更多信息请参见 OpenGL ES 3.X 关于 glFrameBufferTexture() 的文档。

### `void QOpenGLExtraFunctions::glFramebufferTextureLayer(GLenum target, GLenum attachment, GLuint texture, GLint level, GLint layer)`

**作用与语义：**

调用 glFrameBufferTextureLayer（`target`， `attachment`， `texture`， `level`， `layer` 的便利函数）。
该函数仅在 OpenGL ES 3.x 或 OpenGL 3.x 或 4.x 上下文中可用。在运行纯 OpenGL 时，该函数仅在该配置文件和版本中包含该函数核心或扩展时可用。
欲了解更多信息，请参阅 OpenGL ES 3.x 关于 glFrameFrameBufferTextureLayer() 的文档。

### `void QOpenGLExtraFunctions::glGenProgramPipelines(GLsizei n, GLuint *pipelines)`

**作用与语义：**

调用glGenProgramPipelines（`n`， `pipelines`）的便利函数。
该函数仅在 OpenGL ES 3.x 或 OpenGL 3.x 或 4.x 上下文中可用。在运行纯 OpenGL 时，该函数仅在该配置文件和版本中包含该函数核心或扩展时可用。
更多信息请参见 glGenProgramPipelines() 的 OpenGL ES 3.x 文档。

### `void QOpenGLExtraFunctions::glGenQueries(GLsizei n, GLuint *ids)`

**作用与语义：**

调用glGenQueries（`n`， `ids`）的便利函数。
该函数仅在 OpenGL ES 3.x 或 OpenGL 3.x 或 4.x 上下文中可用。在运行纯 OpenGL 时，该函数仅在该配置文件和版本中包含该函数核心或扩展时可用。
更多信息请参见 OpenGL ES 3.x 关于 glGenQueries() 的文档。

### `void QOpenGLExtraFunctions::glGenSamplers(GLsizei count, GLuint *samplers)`

**作用与语义：**

调用glGenSamplers（`count`， `samplers`）的便利函数。
该函数仅在 OpenGL ES 3.x 或 OpenGL 3.x 或 4.x 上下文中可用。在运行纯 OpenGL 时，该函数仅在该配置文件和版本中包含该函数核心或扩展时可用。
更多信息请参见 OpenGL ES 3.x 关于 glGenSamplers() 的文档。

### `void QOpenGLExtraFunctions::glGenTransformFeedbacks(GLsizei n, GLuint *ids)`

**作用与语义：**

调用glGenTransformFeedbacks（`n`， `ids`）的便利函数。
该函数仅在 OpenGL ES 3.x 或 OpenGL 3.x 或 4.x 上下文中可用。在运行纯 OpenGL 时，该函数仅在该配置文件和版本中包含该函数核心或扩展时可用。
更多信息请参见 OpenGL ES 3.x 关于 glGenTransformFeedbacks() 的文档。

### `void QOpenGLExtraFunctions::glGenVertexArrays(GLsizei n, GLuint *arrays)`

**作用与语义：**

调用glGenVertexArrays（`n`， `arrays`）的便利函数。
该函数仅在 OpenGL ES 3.x 或 OpenGL 3.x 或 4.x 上下文中可用。在运行纯 OpenGL 时，该函数仅在该配置文件和版本中包含该函数核心或扩展时可用。
欲了解更多信息，请参阅 OpenGL ES 3.x 关于 glGenVertexArrays() 的文档。

### `void QOpenGLExtraFunctions::glGetActiveUniformBlockName(GLuint program, GLuint uniformBlockIndex, GLsizei bufSize, GLsizei *length, GLchar *uniformBlockName)`

**作用与语义：**

调用 glGetActiveUniformBlockName（`program`， `uniformBlockIndex`， `bufSize`， `length`， `uniformBlockName` 的便利函数）。
该函数仅在 OpenGL ES 3.x 或 OpenGL 3.x 或 4.x 上下文中可用。在运行纯 OpenGL 时，该函数仅在该配置文件和版本中包含该函数核心或扩展时可用。
更多信息请参见 OpenGL ES 3.x 关于 glGetActiveUniformBlockName() 的文档。

### `void QOpenGLExtraFunctions::glGetActiveUniformBlockiv(GLuint program, GLuint uniformBlockIndex, GLenum pname, GLint *params)`

**作用与语义：**

调用glGetActiveUniformBlockiv（`program`， `uniformBlockIndex`， `pname`， `params`）的便利函数。
该函数仅在 OpenGL ES 3.x 或 OpenGL 3.x 或 4.x 上下文中可用。在运行纯 OpenGL 时，该函数仅在该配置文件和版本中包含该函数核心或扩展时可用。
欲了解更多信息，请参阅 OpenGL ES 3.x 关于 glGetActiveUniformBlockiv() 的文档。

### `void QOpenGLExtraFunctions::glGetActiveUniformsiv(GLuint program, GLsizei uniformCount, const GLuint *uniformIndices, GLenum pname, GLint *params)`

**作用与语义：**

调用glGetActiveUniformsiv（`program`， `uniformCount`， `uniformIndices`， `pname`， `params`）的便利函数。
该函数仅在 OpenGL ES 3.x 或 OpenGL 3.x 或 4.x 上下文中可用。在运行纯 OpenGL 时，该函数仅在该配置文件和版本中包含该函数核心或扩展时可用。
更多信息请参见 OpenGL ES 3.x 关于 glGetActiveUniformsiv() 的文档。

### `void QOpenGLExtraFunctions::glGetBooleani_v(GLenum target, GLuint index, GLboolean *data)`

**作用与语义：**

调用glGetBooleani_v（`target`， `index`， `data`）的便利函数。
该函数仅在 OpenGL ES 3.x 或 OpenGL 3.x 或 4.x 上下文中可用。在运行纯 OpenGL 时，该函数仅在该配置文件和版本中包含该函数核心或扩展时可用。
欲了解更多信息，请参阅 OpenGL ES 3.x 文档中的 glGetBooleani_v()。

### `void QOpenGLExtraFunctions::glGetBufferParameteri64v(GLenum target, GLenum pname, GLint64 *params)`

**作用与语义：**

调用glGetBufferParameteri64v（`target`， `pname`， `params`）的便利函数。
该函数仅在 OpenGL ES 3.x 或 OpenGL 3.x 或 4.x 上下文中可用。在运行纯 OpenGL 时，该函数仅在该配置文件和版本中包含该函数核心或扩展时可用。
欲了解更多信息，请参阅 OpenGL ES 3.x 关于 glGetBufferParameteri64v() 的文档。

### `void QOpenGLExtraFunctions::glGetBufferPointerv(GLenum target, GLenum pname, void **params)`

**作用与语义：**

调用glGetBufferPointerv（`target`， `pname`， `params`）的便利函数。
该函数仅在 OpenGL ES 3.x 或 OpenGL 3.x 或 4.x 上下文中可用。在运行纯 OpenGL 时，该函数仅在该配置文件和版本中包含该函数核心或扩展时可用。
欲了解更多信息，请参阅 OpenGL ES 3.x 关于 glGetBufferPointerv() 的文档。

### `GLuint QOpenGLExtraFunctions::glGetDebugMessageLog(GLuint count, GLsizei bufSize, GLenum *sources, GLenum *types, GLuint *ids, GLenum *severities, GLsizei *lengths, GLchar *messageLog)`

**作用与语义：**

调用glGetDebugMessageLog（`count`、`bufSize`、`sources`、`types`、`ids`、`severities`、`lengths`、`messageLog`）的便利函数。
该函数仅在 OpenGL ES 3.x 或 OpenGL 3.x 或 4.x 上下文中可用。在运行纯 OpenGL 时，该函数仅在该配置文件和版本中包含该函数核心或扩展时可用。
欲了解更多信息，请参阅 OpenGL ES 3.X 关于 glGetDebugMessageLog() 的文档。

### `GLint QOpenGLExtraFunctions::glGetFragDataLocation(GLuint program, const GLchar *name)`

**作用与语义：**

调用glGetFragDataLocation（`program`， `name`）的便利函数。
该函数仅在 OpenGL ES 3.x 或 OpenGL 3.x 或 4.x 上下文中可用。在运行纯 OpenGL 时，该函数仅在该配置文件和版本中包含该函数核心或扩展时可用。
欲了解更多信息，请参阅 OpenGL ES 3.x 关于 glGetFragDataLocation() 的文档。

### `void QOpenGLExtraFunctions::glGetFramebufferParameteriv(GLenum target, GLenum pname, GLint *params)`

**作用与语义：**

调用glGetFramebufferParameteriv（`target`， `pname`， `params`）的便利函数。
该函数仅在 OpenGL ES 3.x 或 OpenGL 3.x 或 4.x 上下文中可用。在运行纯 OpenGL 时，该函数仅在该配置文件和版本中包含该函数核心或扩展时可用。
更多信息请参见 OpenGL ES 3.x 关于 glGetFramebufferParameteriv() 的文档。

### `GLenum QOpenGLExtraFunctions::glGetGraphicsResetStatus()`

**作用与语义：**

调用glGetGraphicsResetStatus()的便利函数。
该函数仅在 OpenGL ES 3.x 或 OpenGL 3.x 或 4.x 上下文中可用。在运行纯 OpenGL 时，该函数仅在该配置文件和版本中包含该函数核心或扩展时可用。
更多信息请参见 OpenGL ES 3.X 关于 glGetGraphicsResetStatus() 的文档。

### `void QOpenGLExtraFunctions::glGetInteger64i_v(GLenum target, GLuint index, GLint64 *data)`

**作用与语义：**

调用 glGetInteger64i_v（`target`， `index`， `data` 的便利函数）。
该函数仅在 OpenGL ES 3.x 或 OpenGL 3.x 或 4.x 上下文中可用。在运行纯 OpenGL 时，该函数仅在该配置文件和版本中包含该函数核心或扩展时可用。
欲了解更多信息，请参阅 OpenGL ES 3.x 文档中的 glGetInteger64i_v()。

### `void QOpenGLExtraFunctions::glGetInteger64v(GLenum pname, GLint64 *data)`

**作用与语义：**

调用glGetInteger64v（`pname`， `data`）的便利函数。
该函数仅在 OpenGL ES 3.x 或 OpenGL 3.x 或 4.x 上下文中可用。在运行纯 OpenGL 时，该函数仅在该配置文件和版本中包含该函数核心或扩展时可用。
更多信息请参见 OpenGL ES 3.x 关于 glGetInteger64v() 的文档。

### `void QOpenGLExtraFunctions::glGetIntegeri_v(GLenum target, GLuint index, GLint *data)`

**作用与语义：**

调用glGetIntegeri_v（`target`， `index`， `data`）的便利函数。
该函数仅在 OpenGL ES 3.x 或 OpenGL 3.x 或 4.x 上下文中可用。在运行纯 OpenGL 时，该函数仅在该配置文件和版本中包含该函数核心或扩展时可用。
更多信息请参阅 OpenGL ES 3.x 文档中的 glGetIntegeri_v()。

### `void QOpenGLExtraFunctions::glGetInternalformativ(GLenum target, GLenum internalformat, GLenum pname, GLsizei bufSize, GLint *params)`

**作用与语义：**

调用glGetInternalformativ（`target`， `internalformat`， `pname`， `bufSize`， `params`）的便利函数。
该函数仅在 OpenGL ES 3.x 或 OpenGL 3.x 或 4.x 上下文中可用。在运行纯 OpenGL 时，该函数仅在该配置文件和版本中包含该函数核心或扩展时可用。
更多信息请参见 OpenGL ES 3.x 关于 glGetInternalformativ() 的文档。

### `void QOpenGLExtraFunctions::glGetMultisamplefv(GLenum pname, GLuint index, GLfloat *val)`

**作用与语义：**

调用glGetMultisamplefv（`pname`， `index`， `val`）的便利函数。
该函数仅在 OpenGL ES 3.x 或 OpenGL 3.x 或 4.x 上下文中可用。在运行纯 OpenGL 时，该函数仅在该配置文件和版本中包含该函数核心或扩展时可用。
更多信息请参见 OpenGL ES 3.x 关于 glGetMultisamplefv() 的文档。

### `void QOpenGLExtraFunctions::glGetObjectLabel(GLenum identifier, GLuint name, GLsizei bufSize, GLsizei *length, GLchar *label)`

**作用与语义：**

调用glGetObjectLabel（`identifier`， `name`， `bufSize`， `length`， `label`）的便利函数。
该函数仅在 OpenGL ES 3.x 或 OpenGL 3.x 或 4.x 上下文中可用。在运行纯 OpenGL 时，该函数仅在该配置文件和版本中包含该函数核心或扩展时可用。
更多信息请参见 OpenGL ES 3.X 关于 glGetObjectLabe() 的文档。

### `void QOpenGLExtraFunctions::glGetObjectPtrLabel(const void *ptr, GLsizei bufSize, GLsizei *length, GLchar *label)`

**作用与语义：**

调用glGetObjectPtrLabel（`ptr`， `bufSize`， `length`， `label`）的便利函数。
该函数仅在 OpenGL ES 3.x 或 OpenGL 3.x 或 4.x 上下文中可用。在运行纯 OpenGL 时，该函数仅在该配置文件和版本中包含该函数核心或扩展时可用。
欲了解更多信息，请参阅 OpenGL ES 3.X 关于 glGetObjectPtrLabe() 的文档。

### `void QOpenGLExtraFunctions::glGetPointerv(GLenum pname, void **params)`

**作用与语义：**

调用glGetPointerv（`pname`， `params`）的便利函数。
该函数仅在 OpenGL ES 3.x 或 OpenGL 3.x 或 4.x 上下文中可用。在运行纯 OpenGL 时，该函数仅在该配置文件和版本中包含该函数核心或扩展时可用。
更多信息请参见 OpenGL ES 3.X 关于 glGetPointerv() 的文档。

### `void QOpenGLExtraFunctions::glGetProgramBinary(GLuint program, GLsizei bufSize, GLsizei *length, GLenum *binaryFormat, void *binary)`

**作用与语义：**

调用glGetProgramBinary（`program`， `bufSize`， `length`， `binaryFormat`， `binary`）的便利函数。
该函数仅在 OpenGL ES 3.x 或 OpenGL 3.x 或 4.x 上下文中可用。在运行纯 OpenGL 时，该函数仅在该配置文件和版本中包含该函数核心或扩展时可用。
更多信息请参见 OpenGL ES 3.x 关于 glGetProgramBinary() 的文档。

### `void QOpenGLExtraFunctions::glGetProgramInterfaceiv(GLuint program, GLenum programInterface, GLenum pname, GLint *params)`

**作用与语义：**

调用glGetProgramInterfaceiv（`program`， `programInterface`， `pname`， `params`的便利函数）。
该函数仅在 OpenGL ES 3.x 或 OpenGL 3.x 或 4.x 上下文中可用。在运行纯 OpenGL 时，该函数仅在该配置文件和版本中包含该函数核心或扩展时可用。
欲了解更多信息，请参阅 OpenGL ES 3.x 关于 glGetProgramInterfaceiv() 的文档。

### `void QOpenGLExtraFunctions::glGetProgramPipelineInfoLog(GLuint pipeline, GLsizei bufSize, GLsizei *length, GLchar *infoLog)`

**作用与语义：**

调用glGetProgramPipelineInfoLog（`pipeline`， `bufSize`， `length`， `infoLog`）的便利函数。
该函数仅在 OpenGL ES 3.x 或 OpenGL 3.x 或 4.x 上下文中可用。在运行纯 OpenGL 时，该函数仅在该配置文件和版本中包含该函数核心或扩展时可用。
更多信息请参阅 OpenGL ES 3.x 关于 glGetProgramPipelineInfoLog() 的文档。

### `void QOpenGLExtraFunctions::glGetProgramPipelineiv(GLuint pipeline, GLenum pname, GLint *params)`

**作用与语义：**

调用glGetProgramPipelineiv（`pipeline`， `pname`， `params`）的便利函数。
该函数仅在 OpenGL ES 3.x 或 OpenGL 3.x 或 4.x 上下文中可用。在运行纯 OpenGL 时，该函数仅在该配置文件和版本中包含该函数核心或扩展时可用。
更多信息请参见 OpenGL ES 3.x 关于 glGetProgramPipelineiv() 的文档。

### `GLuint QOpenGLExtraFunctions::glGetProgramResourceIndex(GLuint program, GLenum programInterface, const GLchar *name)`

**作用与语义：**

调用glGetProgramResourceIndex（`program`， `programInterface`， `name`）的便利函数。
该函数仅在 OpenGL ES 3.x 或 OpenGL 3.x 或 4.x 上下文中可用。在运行纯 OpenGL 时，该函数仅在该配置文件和版本中包含该函数核心或扩展时可用。
欲了解更多信息，请参阅 OpenGL ES 3.x 关于 glGetProgramResourceIndex() 的文档。

### `GLint QOpenGLExtraFunctions::glGetProgramResourceLocation(GLuint program, GLenum programInterface, const GLchar *name)`

**作用与语义：**

调用glGetProgramResourceLocation（`program`， `programInterface`， `name`）的便利函数。
该函数仅在 OpenGL ES 3.x 或 OpenGL 3.x 或 4.x 上下文中可用。在运行纯 OpenGL 时，该函数仅在该配置文件和版本中包含该函数核心或扩展时可用。
欲了解更多信息，请参阅 OpenGL ES 3.x 关于 glGetProgramResourceLocation() 的文档。

### `void QOpenGLExtraFunctions::glGetProgramResourceName(GLuint program, GLenum programInterface, GLuint index, GLsizei bufSize, GLsizei *length, GLchar *name)`

**作用与语义：**

调用glGetProgramResourceName（`program`， `programInterface`， `index`， `bufSize`， `length`， `name`）的便利函数。
该函数仅在 OpenGL ES 3.x 或 OpenGL 3.x 或 4.x 上下文中可用。在运行纯 OpenGL 时，该函数仅在该配置文件和版本中包含该函数核心或扩展时可用。
欲了解更多信息，请参阅 OpenGL ES 3.x 关于 glGetProgramResourceName() 的文档。

### `void QOpenGLExtraFunctions::glGetProgramResourceiv(GLuint program, GLenum programInterface, GLuint index, GLsizei propCount, const GLenum *props, GLsizei bufSize, GLsizei *length, GLint *params)`

**作用与语义：**

调用glGetProgramResourceiv（`program`、`programInterface`、`index`、`propCount`、`props`、`bufSize`、`length`、`params`）的便利函数。
该函数仅在 OpenGL ES 3.x 或 OpenGL 3.x 或 4.x 上下文中可用。在运行纯 OpenGL 时，该函数仅在该配置文件和版本中包含该函数核心或扩展时可用。
更多信息请参见 glGetProgramResourceiv() 的 OpenGL ES 3.x 文档。

### `void QOpenGLExtraFunctions::glGetQueryObjectuiv(GLuint id, GLenum pname, GLuint *params)`

**作用与语义：**

调用glGetQueryObjectuiv（`id`， `pname`， `params`）的便利函数。
该函数仅在 OpenGL ES 3.x 或 OpenGL 3.x 或 4.x 上下文中可用。在运行纯 OpenGL 时，该函数仅在该配置文件和版本中包含该函数核心或扩展时可用。
更多信息请参见 OpenGL ES 3.x 关于 glGetQueryObjectuiv() 的文档。

### `void QOpenGLExtraFunctions::glGetQueryiv(GLenum target, GLenum pname, GLint *params)`

**作用与语义：**

调用glGetQueryiv（`target`， `pname`， `params`）的便利函数。
该函数仅在 OpenGL ES 3.x 或 OpenGL 3.x 或 4.x 上下文中可用。在运行纯 OpenGL 时，该函数仅在该配置文件和版本中包含该函数核心或扩展时可用。
欲了解更多信息，请参阅 OpenGL ES 3.x 关于 glGetQueryiv() 的文档。

### `void QOpenGLExtraFunctions::glGetSamplerParameterIiv(GLuint sampler, GLenum pname, GLint *params)`

**作用与语义：**

调用glGetSamplerParameterIiv（`sampler`， `pname`， `params`）的便利函数。
该函数仅在 OpenGL ES 3.x 或 OpenGL 3.x 或 4.x 上下文中可用。在运行纯 OpenGL 时，该函数仅在该配置文件和版本中包含该函数核心或扩展时可用。
更多信息请参见 OpenGL ES 3.X 关于 glGetSamplerParameterIiv() 的文档。

### `void QOpenGLExtraFunctions::glGetSamplerParameterIuiv(GLuint sampler, GLenum pname, GLuint *params)`

**作用与语义：**

调用glGetSamplerParameterIuiv（`sampler`， `pname`， `params`）的便利函数。
该函数仅在 OpenGL ES 3.x 或 OpenGL 3.x 或 4.x 上下文中可用。在运行纯 OpenGL 时，该函数仅在该配置文件和版本中包含该函数核心或扩展时可用。
更多信息请参见 OpenGL ES 3.X 关于 glGetSamplerParameterIuiv() 的文档。

### `void QOpenGLExtraFunctions::glGetSamplerParameterfv(GLuint sampler, GLenum pname, GLfloat *params)`

**作用与语义：**

调用glGetSamplerParameterfv（`sampler`， `pname`， `params`）的便利函数。
该函数仅在 OpenGL ES 3.x 或 OpenGL 3.x 或 4.x 上下文中可用。在运行纯 OpenGL 时，该函数仅在该配置文件和版本中包含该函数核心或扩展时可用。
欲了解更多信息，请参阅 OpenGL ES 3.x 关于 glGetSamplerParameterfv() 的文档。

### `void QOpenGLExtraFunctions::glGetSamplerParameteriv(GLuint sampler, GLenum pname, GLint *params)`

**作用与语义：**

调用glGetSamplerParameteriv（`sampler`， `pname`， `params`）的便利函数。
该函数仅在 OpenGL ES 3.x 或 OpenGL 3.x 或 4.x 上下文中可用。在运行纯 OpenGL 时，该函数仅在该配置文件和版本中包含该函数核心或扩展时可用。
欲了解更多信息，请参阅 OpenGL ES 3.x 关于 glGetSamplerParameteriv() 的文档。

### `const GLubyte *QOpenGLExtraFunctions::glGetStringi(GLenum name, GLuint index)`

**作用与语义：**

调用glGetStringi（`name`， `index`）的便利函数。
该函数仅在 OpenGL ES 3.x 或 OpenGL 3.x 或 4.x 上下文中可用。在运行纯 OpenGL 时，该函数仅在该配置文件和版本中包含该函数核心或扩展时可用。
欲了解更多信息，请参阅 OpenGL ES 3.x 关于 glGetStringi() 的文档。

### `void QOpenGLExtraFunctions::glGetSynciv(GLsync sync, GLenum pname, GLsizei bufSize, GLsizei *length, GLint *values)`

**作用与语义：**

调用glGetSynciv（`sync`， `pname`， `bufSize`， `length`， `values`）的便利函数。
该函数仅在 OpenGL ES 3.x 或 OpenGL 3.x 或 4.x 上下文中可用。在运行纯 OpenGL 时，该函数仅在该配置文件和版本中包含该函数核心或扩展时可用。
欲了解更多信息，请参阅 OpenGL ES 3.x 关于 glGetSynciv() 的文档。

### `void QOpenGLExtraFunctions::glGetTexLevelParameterfv(GLenum target, GLint level, GLenum pname, GLfloat *params)`

**作用与语义：**

调用glGetTexLevelParameterfv（`target`， `level`， `pname`， `params`）的便利函数。
该函数仅在 OpenGL ES 3.x 或 OpenGL 3.x 或 4.x 上下文中可用。在运行纯 OpenGL 时，该函数仅在该配置文件和版本中包含该函数核心或扩展时可用。
欲了解更多信息，请参阅 OpenGL ES 3.x 关于 glGetTexLevelParameterfv() 的文档。

### `void QOpenGLExtraFunctions::glGetTexLevelParameteriv(GLenum target, GLint level, GLenum pname, GLint *params)`

**作用与语义：**

调用glGetTexLevelParameteriv（`target`， `level`， `pname`， `params`）的便利函数。
该函数仅在 OpenGL ES 3.x 或 OpenGL 3.x 或 4.x 上下文中可用。在运行纯 OpenGL 时，该函数仅在该配置文件和版本中包含该函数核心或扩展时可用。
欲了解更多信息，请参阅 OpenGL ES 3.x 关于 glGetTexLevelParameteriv() 的文档。

### `void QOpenGLExtraFunctions::glGetTexParameterIiv(GLenum target, GLenum pname, GLint *params)`

**作用与语义：**

调用glGetTexParameterIiv（`target`， `pname`， `params`的便利函数）。
该函数仅在 OpenGL ES 3.x 或 OpenGL 3.x 或 4.x 上下文中可用。在运行纯 OpenGL 时，该函数仅在该配置文件和版本中包含该函数核心或扩展时可用。
更多信息请参见 OpenGL ES 3.X 关于 glGetTexParameterIiv() 的文档。

### `void QOpenGLExtraFunctions::glGetTexParameterIuiv(GLenum target, GLenum pname, GLuint *params)`

**作用与语义：**

调用glGetTexParameterIuiv（`target`， `pname`， `params`）的便利函数。
该函数仅在 OpenGL ES 3.x 或 OpenGL 3.x 或 4.x 上下文中可用。在运行纯 OpenGL 时，该函数仅在该配置文件和版本中包含该函数核心或扩展时可用。
更多信息请参见 OpenGL ES 3.X 关于 glGetTexParameterIuiv() 的文档。

### `void QOpenGLExtraFunctions::glGetTransformFeedbackVarying(GLuint program, GLuint index, GLsizei bufSize, GLsizei *length, GLsizei *size, GLenum *type, GLchar *name)`

**作用与语义：**

调用glGetTransformFeedbackVarying（`program`、`index`、`bufSize`、`length`、`size`、`type`、`name`）的便利函数。
该函数仅在 OpenGL ES 3.x 或 OpenGL 3.x 或 4.x 上下文中可用。在运行纯 OpenGL 时，该函数仅在该配置文件和版本中包含该函数核心或扩展时可用。
更多信息请参见 OpenGL ES 3.x 关于 glGetTransformFeedbackVarying() 的文档。

### `GLuint QOpenGLExtraFunctions::glGetUniformBlockIndex(GLuint program, const GLchar *uniformBlockName)`

**作用与语义：**

调用glGetUniformBlockIndex（`program`， `uniformBlockName`）的便利函数。
该函数仅在 OpenGL ES 3.x 或 OpenGL 3.x 或 4.x 上下文中可用。在运行纯 OpenGL 时，该函数仅在该配置文件和版本中包含该函数核心或扩展时可用。
更多信息请参见 OpenGL ES 3.x 关于 glGetUniformBlockIndex() 的文档。

### `void QOpenGLExtraFunctions::glGetUniformIndices(GLuint program, GLsizei uniformCount, const GLchar *const *uniformNames, GLuint *uniformIndices)`

**作用与语义：**

调用glGetUniformIndices（`program`， `uniformCount`， `uniformNames`， `uniformIndices`）的便利函数。
该函数仅在 OpenGL ES 3.x 或 OpenGL 3.x 或 4.x 上下文中可用。在运行纯 OpenGL 时，该函数仅在该配置文件和版本中包含该函数核心或扩展时可用。
更多信息请参见 OpenGL ES 3.x 关于 glGetUniformIndices() 的文档。

### `void QOpenGLExtraFunctions::glGetUniformuiv(GLuint program, GLint location, GLuint *params)`

**作用与语义：**

调用glGetUniformuiv（`program`， `location`， `params`）的便利函数。
该函数仅在 OpenGL ES 3.x 或 OpenGL 3.x 或 4.x 上下文中可用。在运行纯 OpenGL 时，该函数仅在该配置文件和版本中包含该函数核心或扩展时可用。
欲了解更多信息，请参阅 glGetUniformuiv() 的 OpenGL ES 3.x 文档。

### `void QOpenGLExtraFunctions::glGetVertexAttribIiv(GLuint index, GLenum pname, GLint *params)`

**作用与语义：**

调用glGetVertexAttribIiv（`index`， `pname`， `params`）的便利函数。
该函数仅在 OpenGL ES 3.x 或 OpenGL 3.x 或 4.x 上下文中可用。在运行纯 OpenGL 时，该函数仅在该配置文件和版本中包含该函数核心或扩展时可用。
欲了解更多信息，请参阅 OpenGL ES 3.x 关于 glGetVertexAttribIiv() 的文档。

### `void QOpenGLExtraFunctions::glGetVertexAttribIuiv(GLuint index, GLenum pname, GLuint *params)`

**作用与语义：**

调用 glGetVertexAttribIuiv（`index`， `pname`， `params`） 的便利函数。
该函数仅在 OpenGL ES 3.x 或 OpenGL 3.x 或 4.x 上下文中可用。在运行纯 OpenGL 时，该函数仅在该配置文件和版本中包含该函数核心或扩展时可用。
更多信息请参见 glGetVertexAttribIuiv() 的 OpenGL ES 3.x 文档。

### `void QOpenGLExtraFunctions::glGetnUniformfv(GLuint program, GLint location, GLsizei bufSize, GLfloat *params)`

**作用与语义：**

调用glGetnUniformfv（`program`， `location`， `bufSize`， `params`）的便利函数。
该函数仅在 OpenGL ES 3.x 或 OpenGL 3.x 或 4.x 上下文中可用。在运行纯 OpenGL 时，该函数仅在该配置文件和版本中包含该函数核心或扩展时可用。
更多信息请参见 OpenGL ES 3.X 关于 glGetnUniformfv() 的文档。

### `void QOpenGLExtraFunctions::glGetnUniformiv(GLuint program, GLint location, GLsizei bufSize, GLint *params)`

**作用与语义：**

调用glGetnUniformiv（`program`， `location`， `bufSize`， `params`）的便利函数。
该函数仅在 OpenGL ES 3.x 或 OpenGL 3.x 或 4.x 上下文中可用。在运行纯 OpenGL 时，该函数仅在该配置文件和版本中包含该函数核心或扩展时可用。
更多信息请参见 glGetnUniformiv() 的 OpenGL ES 3.X 文档。

### `void QOpenGLExtraFunctions::glGetnUniformuiv(GLuint program, GLint location, GLsizei bufSize, GLuint *params)`

**作用与语义：**

调用glGetnUniformuiv（`program`， `location`， `bufSize`， `params`的便利函数）。
该函数仅在 OpenGL ES 3.x 或 OpenGL 3.x 或 4.x 上下文中可用。在运行纯 OpenGL 时，该函数仅在该配置文件和版本中包含该函数核心或扩展时可用。
更多信息请参见 glGetnUniformuiv() 的 OpenGL ES 3.X 文档。

### `void QOpenGLExtraFunctions::glInvalidateFramebuffer(GLenum target, GLsizei numAttachments, const GLenum *attachments)`

**作用与语义：**

调用 glInvalidateFramebuffer（`target`， `numAttachments`， `attachments`）的便利函数。
该函数仅在 OpenGL ES 3.x 或 OpenGL 3.x 或 4.x 上下文中可用。在运行纯 OpenGL 时，该函数仅在该配置文件和版本中包含该函数核心或扩展时可用。
欲了解更多信息，请参阅 OpenGL ES 3.x 关于 glInvalidateFramebuffer() 的文档。

### `void QOpenGLExtraFunctions::glInvalidateSubFramebuffer(GLenum target, GLsizei numAttachments, const GLenum *attachments, GLint x, GLint y, GLsizei width, GLsizei height)`

**作用与语义：**

调用 glInvalidateSubFramebuffer（`target`、`numAttachments`、`attachments`、`x`、`y`、`width`、`height`）的便利函数。
该函数仅在 OpenGL ES 3.x 或 OpenGL 3.x 或 4.x 上下文中可用。在运行纯 OpenGL 时，该函数仅在该配置文件和版本中包含该函数核心或扩展时可用。
更多信息请参见 OpenGL ES 3.x 关于 glInvalidateSubFramebuffer() 的文档。

### `GLboolean QOpenGLExtraFunctions::glIsEnabledi(GLenum target, GLuint index)`

**作用与语义：**

调用 glIsEnabledi（`target`， `index`） 的便利函数。
该函数仅在 OpenGL ES 3.x 或 OpenGL 3.x 或 4.x 上下文中可用。在运行纯 OpenGL 时，该函数仅在该配置文件和版本中包含该函数核心或扩展时可用。
更多信息请参见 OpenGL ES 3.X 关于 glIsEnabledi() 的文档。

### `GLboolean QOpenGLExtraFunctions::glIsProgramPipeline(GLuint pipeline)`

**作用与语义：**

调用 glIsProgramPipeline（`pipeline`） 的便利函数。
该函数仅在 OpenGL ES 3.x 或 OpenGL 3.x 或 4.x 上下文中可用。在运行纯 OpenGL 时，该函数仅在该配置文件和版本中包含该函数核心或扩展时可用。
欲了解更多信息，请参阅 OpenGL ES 3.x 关于 glIsProgramPipeline() 的文档。

### `GLboolean QOpenGLExtraFunctions::glIsQuery(GLuint id)`

**作用与语义：**

调用 glIsQuery（`id`） 的便利函数。
该函数仅在 OpenGL ES 3.x 或 OpenGL 3.x 或 4.x 上下文中可用。在运行纯 OpenGL 时，该函数仅在该配置文件和版本中包含该函数核心或扩展时可用。
更多信息请参见 OpenGL ES 3.x 关于 glIsQuery() 的文档。

### `GLboolean QOpenGLExtraFunctions::glIsSampler(GLuint sampler)`

**作用与语义：**

调用glIsSampler（`sampler`）的便利函数。
该函数仅在 OpenGL ES 3.x 或 OpenGL 3.x 或 4.x 上下文中可用。在运行纯 OpenGL 时，该函数仅在该配置文件和版本中包含该函数核心或扩展时可用。
更多信息请参见 OpenGL ES 3.x 关于 glIsSampler() 的文档。

### `GLboolean QOpenGLExtraFunctions::glIsSync(GLsync sync)`

**作用与语义：**

调用 glIsSync（`sync`） 的便利功能。
该函数仅在 OpenGL ES 3.x 或 OpenGL 3.x 或 4.x 上下文中可用。在运行纯 OpenGL 时，该函数仅在该配置文件和版本中包含该函数核心或扩展时可用。
更多信息请参见 OpenGL ES 3.x 关于 glIsSync() 的文档。

### `GLboolean QOpenGLExtraFunctions::glIsTransformFeedback(GLuint id)`

**作用与语义：**

调用 glIsTransformFeedback（`id`） 的便利函数。
该函数仅在 OpenGL ES 3.x 或 OpenGL 3.x 或 4.x 上下文中可用。在运行纯 OpenGL 时，该函数仅在该配置文件和版本中包含该函数核心或扩展时可用。
欲了解更多信息，请参阅 OpenGL ES 3.x 关于 glIsTransformFeedback() 的文档。

### `GLboolean QOpenGLExtraFunctions::glIsVertexArray(GLuint array)`

**作用与语义：**

调用 glIsVertexArray（`array`） 的便利函数。
该函数仅在 OpenGL ES 3.x 或 OpenGL 3.x 或 4.x 上下文中可用。在运行纯 OpenGL 时，该函数仅在该配置文件和版本中包含该函数核心或扩展时可用。
欲了解更多信息，请参阅 OpenGL ES 3.x 关于 glIsVertexArray() 的文档。

### `void *QOpenGLExtraFunctions::glMapBufferRange(GLenum target, GLintptr offset, GLsizeiptr length, GLbitfield access)`

**作用与语义：**

调用glMapBufferRange（`target`， `offset`， `length`， `access`的便利函数）。
该函数仅在 OpenGL ES 3.x 或 OpenGL 3.x 或 4.x 上下文中可用。在运行纯 OpenGL 时，该函数仅在该配置文件和版本中包含该函数核心或扩展时可用。
更多信息请参见 OpenGL ES 3.x 关于 glMapBufferRange() 的文档。

### `void QOpenGLExtraFunctions::glMemoryBarrier(GLbitfield barriers)`

**作用与语义：**

调用glMemoryBarrier（`barriers`）的便利函数。
该函数仅在 OpenGL ES 3.x 或 OpenGL 3.x 或 4.x 上下文中可用。在运行纯 OpenGL 时，该函数仅在该配置文件和版本中包含该函数核心或扩展时可用。
更多信息请参见 OpenGL ES 3.x 关于 glMemoryBarrier() 的文档。

### `void QOpenGLExtraFunctions::glMemoryBarrierByRegion(GLbitfield barriers)`

**作用与语义：**

调用 glMemoryBarrierByRegion（`barriers`） 的便利函数。
该函数仅在 OpenGL ES 3.x 或 OpenGL 3.x 或 4.x 上下文中可用。在运行纯 OpenGL 时，该函数仅在该配置文件和版本中包含该函数核心或扩展时可用。
更多信息请参阅 OpenGL ES 3.x 关于 glMemoryBarrierByRegion() 的文档。

### `void QOpenGLExtraFunctions::glMinSampleShading(GLfloat value)`

**作用与语义：**

调用glMinSampleShading（`value`）的便利函数。
该函数仅在 OpenGL ES 3.x 或 OpenGL 3.x 或 4.x 上下文中可用。在运行纯 OpenGL 时，该函数仅在该配置文件和版本中包含该函数核心或扩展时可用。
更多信息请参见 OpenGL ES 3.X 关于 glMinSampleShading() 的文档。

### `void QOpenGLExtraFunctions::glObjectLabel(GLenum identifier, GLuint name, GLsizei length, const GLchar *label)`

**作用与语义：**

调用glObjectLabel（`identifier`， `name`， `length`， `label`）的便利函数。
该函数仅在 OpenGL ES 3.x 或 OpenGL 3.x 或 4.x 上下文中可用。在运行纯 OpenGL 时，该函数仅在该配置文件和版本中包含该函数核心或扩展时可用。
欲了解更多信息，请参阅 OpenGL ES 3.X 关于 glObjectLabe() 的文档。

### `void QOpenGLExtraFunctions::glObjectPtrLabel(const void *ptr, GLsizei length, const GLchar *label)`

**作用与语义：**

调用glObjectPtrLabel（`ptr`， `length`， `label`）的便利函数。
该函数仅在 OpenGL ES 3.x 或 OpenGL 3.x 或 4.x 上下文中可用。在运行纯 OpenGL 时，该函数仅在该配置文件和版本中包含该函数核心或扩展时可用。
更多信息请参见 OpenGL ES 3.X 关于 glObjectPtrLabe() 的文档。

### `void QOpenGLExtraFunctions::glPatchParameteri(GLenum pname, GLint value)`

**作用与语义：**

调用 glPatchParameteri（`pname`， `value`） 的便利函数。
该函数仅在 OpenGL ES 3.x 或 OpenGL 3.x 或 4.x 上下文中可用。在运行纯 OpenGL 时，该函数仅在该配置文件和版本中包含该函数核心或扩展时可用。
欲了解更多信息，请参阅 OpenGL ES 3.X 关于 glPatchParameteri() 的文档。

### `void QOpenGLExtraFunctions::glPauseTransformFeedback()`

**作用与语义：**

调用 glPauseTransformFeedback() 的便利函数。
该函数仅在 OpenGL ES 3.x 或 OpenGL 3.x 或 4.x 上下文中可用。在运行纯 OpenGL 时，该函数仅在该配置文件和版本中包含该函数核心或扩展时可用。
欲了解更多信息，请参阅 OpenGL ES 3.x 关于 glPauseTransformFeedback() 的文档。

### `void QOpenGLExtraFunctions::glPopDebugGroup()`

**作用与语义：**

调用glPopDebugGroup()的便利函数。
该函数仅在 OpenGL ES 3.x 或 OpenGL 3.x 或 4.x 上下文中可用。在运行纯 OpenGL 时，该函数仅在该配置文件和版本中包含该函数核心或扩展时可用。
欲了解更多信息，请参阅 glPopDebugGroup() 的 OpenGL ES 3.X 文档。

### `void QOpenGLExtraFunctions::glPrimitiveBoundingBox(GLfloat minX, GLfloat minY, GLfloat minZ, GLfloat minW, GLfloat maxX, GLfloat maxY, GLfloat maxZ, GLfloat maxW)`

**作用与语义：**

方便函数调用 glPrimitiveBoundingBox（`minX`， `minY`， `minZ`， `minW`， `maxX`， `maxY`， `maxZ`， `maxW`）。
该函数仅在 OpenGL ES 3.x 或 OpenGL 3.x 或 4.x 上下文中可用。在运行纯 OpenGL 时，该函数仅在该配置文件和版本中包含该函数核心或扩展时可用。
更多信息请参见 glPrimitiveBoundingBo() 的 OpenGL ES 3.X 文档。

### `void QOpenGLExtraFunctions::glProgramBinary(GLuint program, GLenum binaryFormat, const void *binary, GLsizei length)`

**作用与语义：**

调用glProgramBinary（`program`， `binaryFormat`， `binary`， `length`）的便利函数。
该函数仅在 OpenGL ES 3.x 或 OpenGL 3.x 或 4.x 上下文中可用。在运行纯 OpenGL 时，该函数仅在该配置文件和版本中包含该函数核心或扩展时可用。
更多信息请参见 OpenGL ES 3.x 关于 glProgramBinary() 的文档。

### `void QOpenGLExtraFunctions::glProgramParameteri(GLuint program, GLenum pname, GLint value)`

**作用与语义：**

调用glProgramParameteri（`program`， `pname`， `value`）的便利函数。
该函数仅在 OpenGL ES 3.x 或 OpenGL 3.x 或 4.x 上下文中可用。在运行纯 OpenGL 时，该函数仅在该配置文件和版本中包含该函数核心或扩展时可用。
欲了解更多信息，请参阅 OpenGL ES 3.x 关于 glProgramParameteri() 的文档。

### `void QOpenGLExtraFunctions::glProgramUniform1f(GLuint program, GLint location, GLfloat v0)`

**作用与语义：**

调用glProgramUniform1f（`program`， `location`， `v0`）的便利函数。
该函数仅在 OpenGL ES 3.x 或 OpenGL 3.x 或 4.x 上下文中可用。在运行纯 OpenGL 时，该函数仅在该配置文件和版本中包含该函数核心或扩展时可用。
欲了解更多信息，请参阅 glProgramUniform1f() 的 OpenGL ES 3.x 文档。

### `void QOpenGLExtraFunctions::glProgramUniform1fv(GLuint program, GLint location, GLsizei count, const GLfloat *value)`

**作用与语义：**

调用 glProgramUniform1fv（`program`， `location`， `count`， `value` 的便利函数）。
该函数仅在 OpenGL ES 3.x 或 OpenGL 3.x 或 4.x 上下文中可用。在运行纯 OpenGL 时，该函数仅在该配置文件和版本中包含该函数核心或扩展时可用。
欲了解更多信息，请参阅 glProgramUniform1fv() 的 OpenGL ES 3.x 文档。

### `void QOpenGLExtraFunctions::glProgramUniform1i(GLuint program, GLint location, GLint v0)`

**作用与语义：**

调用 glProgramUniform1i（`program`， `location`， `v0` 的便利函数）。
该函数仅在 OpenGL ES 3.x 或 OpenGL 3.x 或 4.x 上下文中可用。在运行纯 OpenGL 时，该函数仅在该配置文件和版本中包含该函数核心或扩展时可用。
欲了解更多信息，请参阅 OpenGL ES 3.x 关于 glProgramUniform1i() 的文档。

### `void QOpenGLExtraFunctions::glProgramUniform1iv(GLuint program, GLint location, GLsizei count, const GLint *value)`

**作用与语义：**

调用glProgramUniform1iv（`program`， `location`， `count`， `value`）的便利函数。
该函数仅在 OpenGL ES 3.x 或 OpenGL 3.x 或 4.x 上下文中可用。在运行纯 OpenGL 时，该函数仅在该配置文件和版本中包含该函数核心或扩展时可用。
更多信息请参见 OpenGL ES 3.x 关于 glProgramUniform1iv() 的文档。

### `void QOpenGLExtraFunctions::glProgramUniform1ui(GLuint program, GLint location, GLuint v0)`

**作用与语义：**

调用glProgramUniform1ui（`program`， `location`， `v0`）的便利函数。
该函数仅在 OpenGL ES 3.x 或 OpenGL 3.x 或 4.x 上下文中可用。在运行纯 OpenGL 时，该函数仅在该配置文件和版本中包含该函数核心或扩展时可用。
更多信息请参见 OpenGL ES 3.x 关于 glProgramUniform1ui() 的文档。

### `void QOpenGLExtraFunctions::glProgramUniform1uiv(GLuint program, GLint location, GLsizei count, const GLuint *value)`

**作用与语义：**

调用glProgramUniform1uiv（`program`， `location`， `count`， `value`）的便利函数。
该函数仅在 OpenGL ES 3.x 或 OpenGL 3.x 或 4.x 上下文中可用。在运行纯 OpenGL 时，该函数仅在该配置文件和版本中包含该函数核心或扩展时可用。
欲了解更多信息，请参阅 OpenGL ES 3.x 关于 glProgramUniform1uiv() 的文档。

### `void QOpenGLExtraFunctions::glProgramUniform2f(GLuint program, GLint location, GLfloat v0, GLfloat v1)`

**作用与语义：**

调用 glProgramUniform2f（`program`， `location`， `v0`， `v1` 的便利函数）。
该函数仅在 OpenGL ES 3.x 或 OpenGL 3.x 或 4.x 上下文中可用。在运行纯 OpenGL 时，该函数仅在该配置文件和版本中包含该函数核心或扩展时可用。
更多信息请参见 glProgramUniform2f() 的 OpenGL ES 3.x 文档。

### `void QOpenGLExtraFunctions::glProgramUniform2fv(GLuint program, GLint location, GLsizei count, const GLfloat *value)`

**作用与语义：**

调用glProgramUniform2fv（`program`， `location`， `count`， `value`）的便利函数。
该函数仅在 OpenGL ES 3.x 或 OpenGL 3.x 或 4.x 上下文中可用。在运行纯 OpenGL 时，该函数仅在该配置文件和版本中包含该函数核心或扩展时可用。
欲了解更多信息，请参阅 OpenGL ES 3.x 关于 glProgramUniform2fv() 的文档。

### `void QOpenGLExtraFunctions::glProgramUniform2i(GLuint program, GLint location, GLint v0, GLint v1)`

**作用与语义：**

调用 glProgramUniform2i（`program`， `location`， `v0`， `v1` 的便利函数）。
该函数仅在 OpenGL ES 3.x 或 OpenGL 3.x 或 4.x 上下文中可用。在运行纯 OpenGL 时，该函数仅在该配置文件和版本中包含该函数核心或扩展时可用。
欲了解更多信息，请参阅 OpenGL ES 3.x 关于 glProgramUniform2i() 的文档。

### `void QOpenGLExtraFunctions::glProgramUniform2iv(GLuint program, GLint location, GLsizei count, const GLint *value)`

**作用与语义：**

调用glProgramUniform2iv（`program`， `location`， `count`， `value`）的便利函数。
该函数仅在 OpenGL ES 3.x 或 OpenGL 3.x 或 4.x 上下文中可用。在运行纯 OpenGL 时，该函数仅在该配置文件和版本中包含该函数核心或扩展时可用。
欲了解更多信息，请参阅 glProgramUniform2iv() 的 OpenGL ES 3.x 文档。

### `void QOpenGLExtraFunctions::glProgramUniform2ui(GLuint program, GLint location, GLuint v0, GLuint v1)`

**作用与语义：**

调用glProgramUniform2ui（`program`， `location`， `v0`， `v1`）的便利函数。
该函数仅在 OpenGL ES 3.x 或 OpenGL 3.x 或 4.x 上下文中可用。在运行纯 OpenGL 时，该函数仅在该配置文件和版本中包含该函数核心或扩展时可用。
欲了解更多信息，请参阅 OpenGL ES 3.x 关于 glProgramUniform2ui() 的文档。

### `void QOpenGLExtraFunctions::glProgramUniform2uiv(GLuint program, GLint location, GLsizei count, const GLuint *value)`

**作用与语义：**

调用glProgramUniform2uiv（`program`， `location`， `count`， `value`）的便利函数。
该函数仅在 OpenGL ES 3.x 或 OpenGL 3.x 或 4.x 上下文中可用。在运行纯 OpenGL 时，该函数仅在该配置文件和版本中包含该函数核心或扩展时可用。
欲了解更多信息，请参阅 glProgramUniform2uiv() 的 OpenGL ES 3.x 文档。

### `void QOpenGLExtraFunctions::glProgramUniform3f(GLuint program, GLint location, GLfloat v0, GLfloat v1, GLfloat v2)`

**作用与语义：**

调用glProgramUniform3f（`program`， `location`， `v0`， `v1`， `v2`）的便利函数。
该函数仅在 OpenGL ES 3.x 或 OpenGL 3.x 或 4.x 上下文中可用。在运行纯 OpenGL 时，该函数仅在该配置文件和版本中包含该函数核心或扩展时可用。
更多信息请参见 glProgramUniform3f() 的 OpenGL ES 3.x 文档。

### `void QOpenGLExtraFunctions::glProgramUniform3fv(GLuint program, GLint location, GLsizei count, const GLfloat *value)`

**作用与语义：**

调用glProgramUniform3fv（`program`， `location`， `count`， `value`）的便利函数。
该函数仅在 OpenGL ES 3.x 或 OpenGL 3.x 或 4.x 上下文中可用。在运行纯 OpenGL 时，该函数仅在该配置文件和版本中包含该函数核心或扩展时可用。
更多信息请参见 glProgramUniform3fv() 的 OpenGL ES 3.x 文档。

### `void QOpenGLExtraFunctions::glProgramUniform3i(GLuint program, GLint location, GLint v0, GLint v1, GLint v2)`

**作用与语义：**

调用glProgramUniform3i（`program`， `location`， `v0`， `v1`， `v2`）的便利函数。
该函数仅在 OpenGL ES 3.x 或 OpenGL 3.x 或 4.x 上下文中可用。在运行纯 OpenGL 时，该函数仅在该配置文件和版本中包含该函数核心或扩展时可用。
更多信息请参见 OpenGL ES 3.x 关于 glProgramUniform3i() 的文档。

### `void QOpenGLExtraFunctions::glProgramUniform3iv(GLuint program, GLint location, GLsizei count, const GLint *value)`

**作用与语义：**

调用 glProgramUniform3iv（`program`， `location`， `count`， `value` 的便利函数）。
该函数仅在 OpenGL ES 3.x 或 OpenGL 3.x 或 4.x 上下文中可用。在运行纯 OpenGL 时，该函数仅在该配置文件和版本中包含该函数核心或扩展时可用。
更多信息请参见 glProgramUniform3iv() 的 OpenGL ES 3.x 文档。

### `void QOpenGLExtraFunctions::glProgramUniform3ui(GLuint program, GLint location, GLuint v0, GLuint v1, GLuint v2)`

**作用与语义：**

调用 glProgramUniform3ui（`program`， `location`， `v0`， `v1`， `v2` 的便利函数）。
该函数仅在 OpenGL ES 3.x 或 OpenGL 3.x 或 4.x 上下文中可用。在运行纯 OpenGL 时，该函数仅在该配置文件和版本中包含该函数核心或扩展时可用。
欲了解更多信息，请参阅 glProgramUniform3ui() 的 OpenGL ES 3.x 文档。

### `void QOpenGLExtraFunctions::glProgramUniform3uiv(GLuint program, GLint location, GLsizei count, const GLuint *value)`

**作用与语义：**

调用 glProgramUniform3uiv（`program`， `location`， `count`， `value` 的便利函数）。
该函数仅在 OpenGL ES 3.x 或 OpenGL 3.x 或 4.x 上下文中可用。在运行纯 OpenGL 时，该函数仅在该配置文件和版本中包含该函数核心或扩展时可用。
更多信息请参见 glProgramUniform3uiv() 的 OpenGL ES 3.x 文档。

### `void QOpenGLExtraFunctions::glProgramUniform4f(GLuint program, GLint location, GLfloat v0, GLfloat v1, GLfloat v2, GLfloat v3)`

**作用与语义：**

调用 glProgramUniform4f（`program`， `location`， `v0`， `v1`， `v2`， `v3` 的便利函数。
该函数仅在 OpenGL ES 3.x 或 OpenGL 3.x 或 4.x 上下文中可用。在运行纯 OpenGL 时，该函数仅在该配置文件和版本中包含该函数核心或扩展时可用。
欲了解更多信息，请参阅 OpenGL ES 3.x 关于 glProgramUniform4f() 的文档。

### `void QOpenGLExtraFunctions::glProgramUniform4fv(GLuint program, GLint location, GLsizei count, const GLfloat *value)`

**作用与语义：**

调用glProgramUniform4fv（`program`， `location`， `count`， `value`）的便利函数。
该函数仅在 OpenGL ES 3.x 或 OpenGL 3.x 或 4.x 上下文中可用。在运行纯 OpenGL 时，该函数仅在该配置文件和版本中包含该函数核心或扩展时可用。
欲了解更多信息，请参阅 glProgramUniform4fv() 的 OpenGL ES 3.x 文档。

### `void QOpenGLExtraFunctions::glProgramUniform4i(GLuint program, GLint location, GLint v0, GLint v1, GLint v2, GLint v3)`

**作用与语义：**

调用glProgramUniform4i（`program`、`location`、`v0`、`v1`、`v2`、`v3`）的便利函数。
该函数仅在 OpenGL ES 3.x 或 OpenGL 3.x 或 4.x 上下文中可用。在运行纯 OpenGL 时，该函数仅在该配置文件和版本中包含该函数核心或扩展时可用。
更多信息请参见 glProgramUniform4i() 的 OpenGL ES 3.x 文档。

### `void QOpenGLExtraFunctions::glProgramUniform4iv(GLuint program, GLint location, GLsizei count, const GLint *value)`

**作用与语义：**

调用 glProgramUniform4iv（`program`， `location`， `count`， `value` 的便利函数）。
该函数仅在 OpenGL ES 3.x 或 OpenGL 3.x 或 4.x 上下文中可用。在运行纯 OpenGL 时，该函数仅在该配置文件和版本中包含该函数核心或扩展时可用。
更多信息请参见 glProgramUniform4iv() 的 OpenGL ES 3.x 文档。

### `void QOpenGLExtraFunctions::glProgramUniform4ui(GLuint program, GLint location, GLuint v0, GLuint v1, GLuint v2, GLuint v3)`

**作用与语义：**

调用 glProgramUniform4ui（`program`、`location`、`v0`、`v1`、`v2`、`v3`）的便利函数。
该函数仅在 OpenGL ES 3.x 或 OpenGL 3.x 或 4.x 上下文中可用。在运行纯 OpenGL 时，该函数仅在该配置文件和版本中包含该函数核心或扩展时可用。
更多信息请参见 OpenGL ES 3.x 关于 glProgramUniform4ui() 的文档。

### `void QOpenGLExtraFunctions::glProgramUniform4uiv(GLuint program, GLint location, GLsizei count, const GLuint *value)`

**作用与语义：**

调用glProgramUniform4uiv（`program`， `location`， `count`， `value`）的便利函数。
该函数仅在 OpenGL ES 3.x 或 OpenGL 3.x 或 4.x 上下文中可用。在运行纯 OpenGL 时，该函数仅在该配置文件和版本中包含该函数核心或扩展时可用。
欲了解更多信息，请参阅 OpenGL ES 3.x 关于 glProgramUniform4uiv() 的文档。

### `void QOpenGLExtraFunctions::glProgramUniformMatrix2fv(GLuint program, GLint location, GLsizei count, GLboolean transpose, const GLfloat *value)`

**作用与语义：**

调用glProgramUniformMatrix2fv（`program`， `location`， `count`， `transpose`， `value`）的便利函数。
该函数仅在 OpenGL ES 3.x 或 OpenGL 3.x 或 4.x 上下文中可用。在运行纯 OpenGL 时，该函数仅在该配置文件和版本中包含该函数核心或扩展时可用。
更多信息请参见 glProgramUniformMatrix2fv() 的 OpenGL ES 3.x 文档。

### `void QOpenGLExtraFunctions::glProgramUniformMatrix2x3fv(GLuint program, GLint location, GLsizei count, GLboolean transpose, const GLfloat *value)`

**作用与语义：**

调用glProgramUniformMatrix2x3fv（`program`， `location`， `count`， `transpose`， `value`的便利函数）。
该函数仅在 OpenGL ES 3.x 或 OpenGL 3.x 或 4.x 上下文中可用。在运行纯 OpenGL 时，该函数仅在该配置文件和版本中包含该函数核心或扩展时可用。
欲了解更多信息，请参阅 OpenGL ES 3.x 关于 glProgramUniformMatrix2x3fv() 的文档。

### `void QOpenGLExtraFunctions::glProgramUniformMatrix2x4fv(GLuint program, GLint location, GLsizei count, GLboolean transpose, const GLfloat *value)`

**作用与语义：**

调用 glProgramUniformMatrix2x4fv（`program`， `location`， `count`， `transpose`， `value` 的便利函数）。
该函数仅在 OpenGL ES 3.x 或 OpenGL 3.x 或 4.x 上下文中可用。在运行纯 OpenGL 时，该函数仅在该配置文件和版本中包含该函数核心或扩展时可用。
更多信息请参见 OpenGL ES 3.x 关于 glProgramUniformMatrix2x4fv() 的文档。

### `void QOpenGLExtraFunctions::glProgramUniformMatrix3fv(GLuint program, GLint location, GLsizei count, GLboolean transpose, const GLfloat *value)`

**作用与语义：**

调用glProgramUniformMatrix3fv（`program`， `location`， `count`， `transpose`， `value`）的便利函数。
该函数仅在 OpenGL ES 3.x 或 OpenGL 3.x 或 4.x 上下文中可用。在运行纯 OpenGL 时，该函数仅在该配置文件和版本中包含该函数核心或扩展时可用。
更多信息请参见 OpenGL ES 3.x 关于 glProgramUniformMatrix3fv() 的文档。

### `void QOpenGLExtraFunctions::glProgramUniformMatrix3x2fv(GLuint program, GLint location, GLsizei count, GLboolean transpose, const GLfloat *value)`

**作用与语义：**

调用 glProgramUniformMatrix3x2fv（`program`， `location`， `count`， `transpose`， `value` 的便利函数）。
该函数仅在 OpenGL ES 3.x 或 OpenGL 3.x 或 4.x 上下文中可用。在运行纯 OpenGL 时，该函数仅在该配置文件和版本中包含该函数核心或扩展时可用。
欲了解更多信息，请参阅 glProgramUniformMatrix3x2fv() 的 OpenGL ES 3.x 文档。

### `void QOpenGLExtraFunctions::glProgramUniformMatrix3x4fv(GLuint program, GLint location, GLsizei count, GLboolean transpose, const GLfloat *value)`

**作用与语义：**

调用glProgramUniformMatrix3x4fv的便利函数（`program`， `location`， `count`， `transpose`， `value`）。
该函数仅在 OpenGL ES 3.x 或 OpenGL 3.x 或 4.x 上下文中可用。在运行纯 OpenGL 时，该函数仅在该配置文件和版本中包含该函数核心或扩展时可用。
更多信息请参见 glProgramUniformMatrix3x4fv() 的 OpenGL ES 3.x 文档。

### `void QOpenGLExtraFunctions::glProgramUniformMatrix4fv(GLuint program, GLint location, GLsizei count, GLboolean transpose, const GLfloat *value)`

**作用与语义：**

调用glProgramUniformMatrix4fv（`program`， `location`， `count`， `transpose`， `value`）的便利函数。
该函数仅在 OpenGL ES 3.x 或 OpenGL 3.x 或 4.x 上下文中可用。在运行纯 OpenGL 时，该函数仅在该配置文件和版本中包含该函数核心或扩展时可用。
更多信息请参见 glProgramUniformMatrix4fv() 的 OpenGL ES 3.x 文档。

### `void QOpenGLExtraFunctions::glProgramUniformMatrix4x2fv(GLuint program, GLint location, GLsizei count, GLboolean transpose, const GLfloat *value)`

**作用与语义：**

调用glProgramUniformMatrix4x2fv（`program`， `location`， `count`， `transpose`， `value`）的便利函数。
该函数仅在 OpenGL ES 3.x 或 OpenGL 3.x 或 4.x 上下文中可用。在运行纯 OpenGL 时，该函数仅在该配置文件和版本中包含该函数核心或扩展时可用。
欲了解更多信息，请参阅 OpenGL ES 3.x 关于 glProgramUniformMatrix4x2fv() 的文档。

### `void QOpenGLExtraFunctions::glProgramUniformMatrix4x3fv(GLuint program, GLint location, GLsizei count, GLboolean transpose, const GLfloat *value)`

**作用与语义：**

调用glProgramUniformMatrix4x3fv（`program`， `location`， `count`， `transpose`， `value`）的便利函数。
该函数仅在 OpenGL ES 3.x 或 OpenGL 3.x 或 4.x 上下文中可用。在运行纯 OpenGL 时，该函数仅在该配置文件和版本中包含该函数核心或扩展时可用。
更多信息请参见 OpenGL ES 3.x 关于 glProgramUniformMatrix4x3fv() 的文档。

### `void QOpenGLExtraFunctions::glPushDebugGroup(GLenum source, GLuint id, GLsizei length, const GLchar *message)`

**作用与语义：**

调用glPushDebugGroup（`source`， `id`， `length`， `message`）的便利函数。
该函数仅在 OpenGL ES 3.x 或 OpenGL 3.x 或 4.x 上下文中可用。在运行纯 OpenGL 时，该函数仅在该配置文件和版本中包含该函数核心或扩展时可用。
更多信息请参见 OpenGL ES 3.X 关于 glPushDebugGroup 的文档。

### `void QOpenGLExtraFunctions::glReadBuffer(GLenum src)`

**作用与语义：**

调用glReadBuffer（`src`）的便利函数。
该函数仅在 OpenGL ES 3.x 或 OpenGL 3.x 或 4.x 上下文中可用。在运行纯 OpenGL 时，该函数仅在该配置文件和版本中包含该函数核心或扩展时可用。
欲了解更多信息，请参阅 OpenGL ES 3.x 关于 glReadBuffer() 的文档。

### `void QOpenGLExtraFunctions::glReadnPixels(GLint x, GLint y, GLsizei width, GLsizei height, GLenum format, GLenum type, GLsizei bufSize, void *data)`

**作用与语义：**

调用glReadnPixels（`x`、`y`、`width`、`height`、`format`、`type`、`bufSize`、`data`）的便利函数。
该函数仅在 OpenGL ES 3.x 或 OpenGL 3.x 或 4.x 上下文中可用。在运行纯 OpenGL 时，该函数仅在该配置文件和版本中包含该函数核心或扩展时可用。
更多信息请参见 OpenGL ES 3.X 关于 glReadnPixels() 的文档。

### `void QOpenGLExtraFunctions::glRenderbufferStorageMultisample(GLenum target, GLsizei samples, GLenum internalformat, GLsizei width, GLsizei height)`

**作用与语义：**

调用 glRenderbufferStorageMultisample（`target`， `samples`， `internalformat`， `width`， `height` 的便利函数）。
该函数仅在 OpenGL ES 3.x 或 OpenGL 3.x 或 4.x 上下文中可用。在运行纯 OpenGL 时，该函数仅在该配置文件和版本中包含该函数核心或扩展时可用。
欲了解更多信息，请参阅 OpenGL ES 3.x 关于 glRenderbufferStorageMultisample() 的文档。

### `void QOpenGLExtraFunctions::glResumeTransformFeedback()`

**作用与语义：**

调用glResumeTransformFeedback()的便利函数。
该函数仅在 OpenGL ES 3.x 或 OpenGL 3.x 或 4.x 上下文中可用。在运行纯 OpenGL 时，该函数仅在该配置文件和版本中包含该函数核心或扩展时可用。
欲了解更多信息，请参阅 OpenGL ES 3.x 关于 glResumeTransformFeedback() 的文档。

### `void QOpenGLExtraFunctions::glSampleMaski(GLuint maskNumber, GLbitfield mask)`

**作用与语义：**

调用glSampleMaski（`maskNumber`， `mask`）的便利函数。
该函数仅在 OpenGL ES 3.x 或 OpenGL 3.x 或 4.x 上下文中可用。在运行纯 OpenGL 时，该函数仅在该配置文件和版本中包含该函数核心或扩展时可用。
更多信息请参见 glSampleMaski() 的 OpenGL ES 3.x 文档。

### `void QOpenGLExtraFunctions::glSamplerParameterIiv(GLuint sampler, GLenum pname, const GLint *param)`

**作用与语义：**

调用glSamplerParameterIiv（`sampler`， `pname`， `param`）的便利函数。
该函数仅在 OpenGL ES 3.x 或 OpenGL 3.x 或 4.x 上下文中可用。在运行纯 OpenGL 时，该函数仅在该配置文件和版本中包含该函数核心或扩展时可用。
更多信息请参见 OpenGL ES 3.X 关于 glSamplerParameterIiv() 的文档。

### `void QOpenGLExtraFunctions::glSamplerParameterIuiv(GLuint sampler, GLenum pname, const GLuint *param)`

**作用与语义：**

调用glSamplerParameterIuiv（`sampler`， `pname`， `param`）的便利函数。
该函数仅在 OpenGL ES 3.x 或 OpenGL 3.x 或 4.x 上下文中可用。在运行纯 OpenGL 时，该函数仅在该配置文件和版本中包含该函数核心或扩展时可用。
更多信息请参见 OpenGL ES 3.X 关于 glSamplerParameterIuiv() 的文档。

### `void QOpenGLExtraFunctions::glSamplerParameterf(GLuint sampler, GLenum pname, GLfloat param)`

**作用与语义：**

调用glSamplerParameterf（`sampler`， `pname`， `param`）的便利函数。
该函数仅在 OpenGL ES 3.x 或 OpenGL 3.x 或 4.x 上下文中可用。在运行纯 OpenGL 时，该函数仅在该配置文件和版本中包含该函数核心或扩展时可用。
更多信息请参见 OpenGL ES 3.x 关于 glSamplerParameterf() 的文档。

### `void QOpenGLExtraFunctions::glSamplerParameterfv(GLuint sampler, GLenum pname, const GLfloat *param)`

**作用与语义：**

调用glSamplerParameterfv（`sampler`， `pname`， `param`）的便利函数。
该函数仅在 OpenGL ES 3.x 或 OpenGL 3.x 或 4.x 上下文中可用。在运行纯 OpenGL 时，该函数仅在该配置文件和版本中包含该函数核心或扩展时可用。
更多信息请参见 OpenGL ES 3.x 关于 glSamplerParameterfv() 的文档。

### `void QOpenGLExtraFunctions::glSamplerParameteri(GLuint sampler, GLenum pname, GLint param)`

**作用与语义：**

调用glSamplerParameteri（`sampler`， `pname`， `param`）的便利函数。
该函数仅在 OpenGL ES 3.x 或 OpenGL 3.x 或 4.x 上下文中可用。在运行纯 OpenGL 时，该函数仅在该配置文件和版本中包含该函数核心或扩展时可用。
欲了解更多信息，请参阅 OpenGL ES 3.x 关于 glSamplerParameteri() 的文档。

### `void QOpenGLExtraFunctions::glSamplerParameteriv(GLuint sampler, GLenum pname, const GLint *param)`

**作用与语义：**

调用glSamplerParameteriv（`sampler`， `pname`， `param`）的便利函数。
该函数仅在 OpenGL ES 3.x 或 OpenGL 3.x 或 4.x 上下文中可用。在运行纯 OpenGL 时，该函数仅在该配置文件和版本中包含该函数核心或扩展时可用。
更多信息请参见 OpenGL ES 3.x 关于 glSamplerParameteriv() 的文档。

### `void QOpenGLExtraFunctions::glTexBuffer(GLenum target, GLenum internalformat, GLuint buffer)`

**作用与语义：**

调用glTexBuffer（`target`， `internalformat`， `buffer`）的便利函数。
该函数仅在 OpenGL ES 3.x 或 OpenGL 3.x 或 4.x 上下文中可用。在运行纯 OpenGL 时，该函数仅在该配置文件和版本中包含该函数核心或扩展时可用。
更多信息请参见 OpenGL ES 3.X 关于 glTexBuffer() 的文档。

### `void QOpenGLExtraFunctions::glTexBufferRange(GLenum target, GLenum internalformat, GLuint buffer, GLintptr offset, GLsizeiptr size)`

**作用与语义：**

调用glTexBufferRange（`target`， `internalformat`， `buffer`， `offset`， `size`）的便利函数。
该函数仅在 OpenGL ES 3.x 或 OpenGL 3.x 或 4.x 上下文中可用。在运行纯 OpenGL 时，该函数仅在该配置文件和版本中包含该函数核心或扩展时可用。
更多信息请参见 OpenGL ES 3.X 关于 glTexBufferRange() 的文档。

### `void QOpenGLExtraFunctions::glTexImage3D(GLenum target, GLint level, GLint internalformat, GLsizei width, GLsizei height, GLsizei depth, GLint border, GLenum format, GLenum type, const void *pixels)`

**作用与语义：**

调用glTexImage3D（`target`、`level`、`internalformat`、`width`、`height`、`depth`、`border`、`format`、`type`、`pixels`）的便利函数。
该函数仅在 OpenGL ES 3.x 或 OpenGL 3.x 或 4.x 上下文中可用。在运行纯 OpenGL 时，该函数仅在该配置文件和版本中包含该函数核心或扩展时可用。
欲了解更多信息，请参阅 OpenGL ES 3.x 关于 glTexImage3D() 的文档。

### `void QOpenGLExtraFunctions::glTexParameterIiv(GLenum target, GLenum pname, const GLint *params)`

**作用与语义：**

调用glTexParameterIiv（`target`， `pname`， `params`）的便利函数。
该函数仅在 OpenGL ES 3.x 或 OpenGL 3.x 或 4.x 上下文中可用。在运行纯 OpenGL 时，该函数仅在该配置文件和版本中包含该函数核心或扩展时可用。
欲了解更多信息，请参阅 glTexParameterIiv() 的 OpenGL ES 3.X 文档。

### `void QOpenGLExtraFunctions::glTexParameterIuiv(GLenum target, GLenum pname, const GLuint *params)`

**作用与语义：**

调用glTexParameterIuiv（`target`， `pname`， `params`）的便利函数。
该函数仅在 OpenGL ES 3.x 或 OpenGL 3.x 或 4.x 上下文中可用。在运行纯 OpenGL 时，该函数仅在该配置文件和版本中包含该函数核心或扩展时可用。
更多信息请参见 OpenGL ES 3.X 关于 glTexParameterIuiv() 的文档。

### `void QOpenGLExtraFunctions::glTexStorage2D(GLenum target, GLsizei levels, GLenum internalformat, GLsizei width, GLsizei height)`

**作用与语义：**

调用glTexStorage2D（`target`， `levels`， `internalformat`， `width`， `height`）的便利函数。
该函数仅在 OpenGL ES 3.x 或 OpenGL 3.x 或 4.x 上下文中可用。在运行纯 OpenGL 时，该函数仅在该配置文件和版本中包含该函数核心或扩展时可用。
更多信息请参见 OpenGL ES 3.x 关于 glTexStorage2D() 的文档。

### `void QOpenGLExtraFunctions::glTexStorage2DMultisample(GLenum target, GLsizei samples, GLenum internalformat, GLsizei width, GLsizei height, GLboolean fixedsamplelocations)`

**作用与语义：**

调用glTexStorage2DMultisample（`target`， `samples`， `internalformat`， `width`， `height`， `fixedsamplelocations`）的便利函数。
该函数仅在 OpenGL ES 3.x 或 OpenGL 3.x 或 4.x 上下文中可用。在运行纯 OpenGL 时，该函数仅在该配置文件和版本中包含该函数核心或扩展时可用。
欲了解更多信息，请参阅 OpenGL ES 3.x 关于 glTexStorage2DMultisample() 的文档。

### `void QOpenGLExtraFunctions::glTexStorage3D(GLenum target, GLsizei levels, GLenum internalformat, GLsizei width, GLsizei height, GLsizei depth)`

**作用与语义：**

调用glTexStorage3D（`target`、`levels`、`internalformat`、`width`、`height`、`depth`的便利函数）。
该函数仅在 OpenGL ES 3.x 或 OpenGL 3.x 或 4.x 上下文中可用。在运行纯 OpenGL 时，该函数仅在该配置文件和版本中包含该函数核心或扩展时可用。
欲了解更多信息，请参阅 OpenGL ES 3.x 关于 glTexStorage3D() 的文档。

### `void QOpenGLExtraFunctions::glTexStorage3DMultisample(GLenum target, GLsizei samples, GLenum internalformat, GLsizei width, GLsizei height, GLsizei depth, GLboolean fixedsamplelocations)`

**作用与语义：**

调用glTexStorage3DMultisample（`target`、`samples`、`internalformat`、`width`、`height`、`depth`、`fixedsamplelocations`）的便利函数。
该函数仅在 OpenGL ES 3.x 或 OpenGL 3.x 或 4.x 上下文中可用。在运行纯 OpenGL 时，该函数仅在该配置文件和版本中包含该函数核心或扩展时可用。
欲了解更多信息，请参阅 OpenGL ES 3.X 关于 glTexStorage3DMultisample() 的文档。

### `void QOpenGLExtraFunctions::glTexSubImage3D(GLenum target, GLint level, GLint xoffset, GLint yoffset, GLint zoffset, GLsizei width, GLsizei height, GLsizei depth, GLenum format, GLenum type, const void *pixels)`

**作用与语义：**

调用glTexSubImage3D（`target`、`level`、`xoffset`、`yoffset`、`zoffset`、`width`、`height`、`depth`、`format`、`type`、`pixels`的便利函数。
该函数仅在 OpenGL ES 3.x 或 OpenGL 3.x 或 4.x 上下文中可用。在运行纯 OpenGL 时，该函数仅在该配置文件和版本中包含该函数核心或扩展时可用。
更多信息请参见 OpenGL ES 3.x 关于 glTexSubImage3D() 的文档。

### `void QOpenGLExtraFunctions::glTransformFeedbackVaryings(GLuint program, GLsizei count, const GLchar *const *varyings, GLenum bufferMode)`

**作用与语义：**

调用glTransformFeedbackVaryings（`program`， `count`， `varyings`， `bufferMode`的便利函数）。
该函数仅在 OpenGL ES 3.x 或 OpenGL 3.x 或 4.x 上下文中可用。在运行纯 OpenGL 时，该函数仅在该配置文件和版本中包含该函数核心或扩展时可用。
更多信息请参阅 OpenGL ES 3.x 关于 glTransformFeedbackVaryings() 的文档。

### `void QOpenGLExtraFunctions::glUniform1ui(GLint location, GLuint v0)`

**作用与语义：**

调用glUniform1ui（`location`， `v0`）的便利函数。
该函数仅在 OpenGL ES 3.x 或 OpenGL 3.x 或 4.x 上下文中可用。在运行纯 OpenGL 时，该函数仅在该配置文件和版本中包含该函数核心或扩展时可用。
更多信息请参见 OpenGL ES 3.x 关于 glUniform1ui() 的文档。

### `void QOpenGLExtraFunctions::glUniform1uiv(GLint location, GLsizei count, const GLuint *value)`

**作用与语义：**

调用glUniform1uiv（`location`， `count`， `value`）的便利函数。
该函数仅在 OpenGL ES 3.x 或 OpenGL 3.x 或 4.x 上下文中可用。在运行纯 OpenGL 时，该函数仅在该配置文件和版本中包含该函数核心或扩展时可用。
欲了解更多信息，请参阅 glUniform1uiv() 的 OpenGL ES 3.x 文档。

### `void QOpenGLExtraFunctions::glUniform2ui(GLint location, GLuint v0, GLuint v1)`

**作用与语义：**

调用 glUniform2ui（`location`， `v0`， `v1`）的便利函数。
该函数仅在 OpenGL ES 3.x 或 OpenGL 3.x 或 4.x 上下文中可用。在运行纯 OpenGL 时，该函数仅在该配置文件和版本中包含该函数核心或扩展时可用。
更多信息请参见 OpenGL ES 3.x 关于 glUniform2ui() 的文档。

### `void QOpenGLExtraFunctions::glUniform2uiv(GLint location, GLsizei count, const GLuint *value)`

**作用与语义：**

调用glUniform2uiv（`location`， `count`， `value`）的便利函数。
该函数仅在 OpenGL ES 3.x 或 OpenGL 3.x 或 4.x 上下文中可用。在运行纯 OpenGL 时，该函数仅在该配置文件和版本中包含该函数核心或扩展时可用。
更多信息请参见 OpenGL ES 3.x 关于 glUniform2uiv() 的文档。

### `void QOpenGLExtraFunctions::glUniform3ui(GLint location, GLuint v0, GLuint v1, GLuint v2)`

**作用与语义：**

调用 glUniform3ui（`location`， `v0`， `v1`， `v2` 的便利函数）。
该函数仅在 OpenGL ES 3.x 或 OpenGL 3.x 或 4.x 上下文中可用。在运行纯 OpenGL 时，该函数仅在该配置文件和版本中包含该函数核心或扩展时可用。
更多信息请参见 OpenGL ES 3.x 关于 glUniform3ui() 的文档。

### `void QOpenGLExtraFunctions::glUniform3uiv(GLint location, GLsizei count, const GLuint *value)`

**作用与语义：**

调用glUniform3uiv（`location`， `count`， `value`）的便利函数。
该函数仅在 OpenGL ES 3.x 或 OpenGL 3.x 或 4.x 上下文中可用。在运行纯 OpenGL 时，该函数仅在该配置文件和版本中包含该函数核心或扩展时可用。
更多信息请参见 glUniform3uiv() 的 OpenGL ES 3.x 文档。

### `void QOpenGLExtraFunctions::glUniform4ui(GLint location, GLuint v0, GLuint v1, GLuint v2, GLuint v3)`

**作用与语义：**

调用 glUniform4ui（`location`， `v0`， `v1`， `v2`， `v3` 的便利函数）。
该函数仅在 OpenGL ES 3.x 或 OpenGL 3.x 或 4.x 上下文中可用。在运行纯 OpenGL 时，该函数仅在该配置文件和版本中包含该函数核心或扩展时可用。
更多信息请参见 glUniform4ui() 的 OpenGL ES 3.x 文档。

### `void QOpenGLExtraFunctions::glUniform4uiv(GLint location, GLsizei count, const GLuint *value)`

**作用与语义：**

调用 glUniform4uiv（`location`， `count`， `value` 的便利函数）。
该函数仅在 OpenGL ES 3.x 或 OpenGL 3.x 或 4.x 上下文中可用。在运行纯 OpenGL 时，该函数仅在该配置文件和版本中包含该函数核心或扩展时可用。
更多信息请参见 OpenGL ES 3.x 关于 glUniform4uiv() 的文档。

### `void QOpenGLExtraFunctions::glUniformBlockBinding(GLuint program, GLuint uniformBlockIndex, GLuint uniformBlockBinding)`

**作用与语义：**

调用glUniformBlockBinding（`program`， `uniformBlockIndex`， `uniformBlockBinding`）的便利函数。
该函数仅在 OpenGL ES 3.x 或 OpenGL 3.x 或 4.x 上下文中可用。在运行纯 OpenGL 时，该函数仅在该配置文件和版本中包含该函数核心或扩展时可用。
欲了解更多信息，请参阅 OpenGL ES 3.x 关于 glUniformBlockBinding() 的文档。

### `void QOpenGLExtraFunctions::glUniformMatrix2x3fv(GLint location, GLsizei count, GLboolean transpose, const GLfloat *value)`

**作用与语义：**

调用glUniformMatrix2x3fv（`location`， `count`， `transpose`， `value`）的便利函数。
该函数仅在 OpenGL ES 3.x 或 OpenGL 3.x 或 4.x 上下文中可用。在运行纯 OpenGL 时，该函数仅在该配置文件和版本中包含该函数核心或扩展时可用。
欲了解更多信息，请参见 OpenGL ES 3.x 关于 glUniformMatrix2x3fv() 的文档。

### `void QOpenGLExtraFunctions::glUniformMatrix2x4fv(GLint location, GLsizei count, GLboolean transpose, const GLfloat *value)`

**作用与语义：**

调用 glUniformMatrix2x4fv（`location`， `count`， `transpose`， `value` 的便利函数）。
该函数仅在 OpenGL ES 3.x 或 OpenGL 3.x 或 4.x 上下文中可用。在运行纯 OpenGL 时，该函数仅在该配置文件和版本中包含该函数核心或扩展时可用。
更多信息请参见 OpenGL ES 3.x 关于 glUniformMatrix2x4fv() 的文档。

### `void QOpenGLExtraFunctions::glUniformMatrix3x2fv(GLint location, GLsizei count, GLboolean transpose, const GLfloat *value)`

**作用与语义：**

调用glUniformMatrix3x2fv（`location`， `count`， `transpose`， `value`）的便利函数。
该函数仅在 OpenGL ES 3.x 或 OpenGL 3.x 或 4.x 上下文中可用。在运行纯 OpenGL 时，该函数仅在该配置文件和版本中包含该函数核心或扩展时可用。
更多信息请参见 OpenGL ES 3.x 关于 glUniformMatrix3x2fv() 的文档。

### `void QOpenGLExtraFunctions::glUniformMatrix3x4fv(GLint location, GLsizei count, GLboolean transpose, const GLfloat *value)`

**作用与语义：**

调用glUniformMatrix3x4fv（`location`， `count`， `transpose`， `value`的便利函数）。
该函数仅在 OpenGL ES 3.x 或 OpenGL 3.x 或 4.x 上下文中可用。在运行纯 OpenGL 时，该函数仅在该配置文件和版本中包含该函数核心或扩展时可用。
更多信息请参见 OpenGL ES 3.x 关于 glUniformMatrix3x4fv() 的文档。

### `void QOpenGLExtraFunctions::glUniformMatrix4x2fv(GLint location, GLsizei count, GLboolean transpose, const GLfloat *value)`

**作用与语义：**

调用glUniformMatrix4x2fv（`location`， `count`， `transpose`， `value`的便利函数）。
该函数仅在 OpenGL ES 3.x 或 OpenGL 3.x 或 4.x 上下文中可用。在运行纯 OpenGL 时，该函数仅在该配置文件和版本中包含该函数核心或扩展时可用。
更多信息请参见 OpenGL ES 3.x 关于 glUniformMatrix4x2fv() 的文档。

### `void QOpenGLExtraFunctions::glUniformMatrix4x3fv(GLint location, GLsizei count, GLboolean transpose, const GLfloat *value)`

**作用与语义：**

调用glUniformMatrix4x3fv（`location`， `count`， `transpose`， `value`）的便利函数。
该函数仅在 OpenGL ES 3.x 或 OpenGL 3.x 或 4.x 上下文中可用。在运行纯 OpenGL 时，该函数仅在该配置文件和版本中包含该函数核心或扩展时可用。
更多信息请参见 glUniformMatrix4x3fv() 的 OpenGL ES 3.x 文档。

### `GLboolean QOpenGLExtraFunctions::glUnmapBuffer(GLenum target)`

**作用与语义：**

调用glUnmapBuffer（`target`）的便利函数。
该函数仅在 OpenGL ES 3.x 或 OpenGL 3.x 或 4.x 上下文中可用。在运行纯 OpenGL 时，该函数仅在该配置文件和版本中包含该函数核心或扩展时可用。
更多信息请参见 OpenGL ES 3.x 关于 glUnmapBuffer() 的文档。

### `void QOpenGLExtraFunctions::glUseProgramStages(GLuint pipeline, GLbitfield stages, GLuint program)`

**作用与语义：**

调用 glUseProgramStages（`pipeline`， `stages`， `program` 的便利函数）。
该函数仅在 OpenGL ES 3.x 或 OpenGL 3.x 或 4.x 上下文中可用。在运行纯 OpenGL 时，该函数仅在该配置文件和版本中包含该函数核心或扩展时可用。
更多信息请参见 OpenGL ES 3.x 关于 glUseProgramStages() 的文档。

### `void QOpenGLExtraFunctions::glValidateProgramPipeline(GLuint pipeline)`

**作用与语义：**

调用 glValidateProgramPipeline（`pipeline`） 的便利函数。
该函数仅在 OpenGL ES 3.x 或 OpenGL 3.x 或 4.x 上下文中可用。在运行纯 OpenGL 时，该函数仅在该配置文件和版本中包含该函数核心或扩展时可用。
欲了解更多信息，请参阅 OpenGL ES 3.x 关于 glValidateProgramPipeline() 的文档。

### `void QOpenGLExtraFunctions::glVertexAttribBinding(GLuint attribindex, GLuint bindingindex)`

**作用与语义：**

调用glVertexAttribBinding（`attribindex`， `bindingindex`）的便利函数。
该函数仅在 OpenGL ES 3.x 或 OpenGL 3.x 或 4.x 上下文中可用。在运行纯 OpenGL 时，该函数仅在该配置文件和版本中包含该函数核心或扩展时可用。
更多信息请参见 OpenGL ES 3.x 关于 glVertexAttribBinding() 的文档。

### `void QOpenGLExtraFunctions::glVertexAttribDivisor(GLuint index, GLuint divisor)`

**作用与语义：**

调用glVertexAttribDivisor（`index`， `divisor`）的便利函数。
该函数仅在 OpenGL ES 3.x 或 OpenGL 3.x 或 4.x 上下文中可用。在运行纯 OpenGL 时，该函数仅在该配置文件和版本中包含该函数核心或扩展时可用。
更多信息请参见 OpenGL ES 3.x 关于 glVertexAttribDivisor() 的文档。

### `void QOpenGLExtraFunctions::glVertexAttribFormat(GLuint attribindex, GLint size, GLenum type, GLboolean normalized, GLuint relativeoffset)`

**作用与语义：**

调用glVertexAttribFormat（`attribindex`， `size`， `type`， `normalized`， `relativeoffset`）的便利函数。
该函数仅在 OpenGL ES 3.x 或 OpenGL 3.x 或 4.x 上下文中可用。在运行纯 OpenGL 时，该函数仅在该配置文件和版本中包含该函数核心或扩展时可用。
更多信息请参见 OpenGL ES 3.x 关于 glVertexAttribFormat() 的文档。

### `void QOpenGLExtraFunctions::glVertexAttribI4i(GLuint index, GLint x, GLint y, GLint z, GLint w)`

**作用与语义：**

调用glVertexAttribI4i（`index`， `x`， `y`， `z`， `w`）的便利函数。
该函数仅在 OpenGL ES 3.x 或 OpenGL 3.x 或 4.x 上下文中可用。在运行纯 OpenGL 时，该函数仅在该配置文件和版本中包含该函数核心或扩展时可用。
欲了解更多信息，请参阅 OpenGL ES 3.x 关于 glVertexAttribI4i() 的文档。

### `void QOpenGLExtraFunctions::glVertexAttribI4iv(GLuint index, const GLint *v)`

**作用与语义：**

调用glVertexAttribI4iv（`index`， `v`）的便利函数。
该函数仅在 OpenGL ES 3.x 或 OpenGL 3.x 或 4.x 上下文中可用。在运行纯 OpenGL 时，该函数仅在该配置文件和版本中包含该函数核心或扩展时可用。
更多信息请参见 OpenGL ES 3.x 关于 glVertexAttribI4iv() 的文档。

### `void QOpenGLExtraFunctions::glVertexAttribI4ui(GLuint index, GLuint x, GLuint y, GLuint z, GLuint w)`

**作用与语义：**

调用glVertexAttribI4ui（`index`， `x`， `y`， `z`， `w`）的便利函数。
该函数仅在 OpenGL ES 3.x 或 OpenGL 3.x 或 4.x 上下文中可用。在运行纯 OpenGL 时，该函数仅在该配置文件和版本中包含该函数核心或扩展时可用。
更多信息请参见 OpenGL ES 3.x 关于 glVertexAttribI4ui() 的文档。

### `void QOpenGLExtraFunctions::glVertexAttribI4uiv(GLuint index, const GLuint *v)`

**作用与语义：**

调用glVertexAttribI4uiv（`index`， `v`）的便利函数。
该函数仅在 OpenGL ES 3.x 或 OpenGL 3.x 或 4.x 上下文中可用。在运行纯 OpenGL 时，该函数仅在该配置文件和版本中包含该函数核心或扩展时可用。
更多信息请参见 glVertexAttribI4uiv() 的 OpenGL ES 3.x 文档。

### `void QOpenGLExtraFunctions::glVertexAttribIFormat(GLuint attribindex, GLint size, GLenum type, GLuint relativeoffset)`

**作用与语义：**

调用glVertexAttribIFormat（`attribindex`， `size`， `type`， `relativeoffset`的便利函数）。
该函数仅在 OpenGL ES 3.x 或 OpenGL 3.x 或 4.x 上下文中可用。在运行纯 OpenGL 时，该函数仅在该配置文件和版本中包含该函数核心或扩展时可用。
欲了解更多信息，请参阅 glVertexAttribIFormat() 的 OpenGL ES 3.x 文档。

### `void QOpenGLExtraFunctions::glVertexAttribIPointer(GLuint index, GLint size, GLenum type, GLsizei stride, const void *pointer)`

**作用与语义：**

调用glVertexAttribIPointer（`index`， `size`， `type`， `stride`， `pointer`）的便利函数。
该函数仅在 OpenGL ES 3.x 或 OpenGL 3.x 或 4.x 上下文中可用。在运行纯 OpenGL 时，该函数仅在该配置文件和版本中包含该函数核心或扩展时可用。
更多信息请参见 glVertexAttribIPointer() 的 OpenGL ES 3.x 文档。

### `void QOpenGLExtraFunctions::glVertexBindingDivisor(GLuint bindingindex, GLuint divisor)`

**作用与语义：**

调用glVertexBindingDivisor（`bindingindex`， `divisor`）的便利函数。
该函数仅在 OpenGL ES 3.x 或 OpenGL 3.x 或 4.x 上下文中可用。在运行纯 OpenGL 时，该函数仅在该配置文件和版本中包含该函数核心或扩展时可用。
更多信息请参见 OpenGL ES 3.x 关于 glVertexBindingDivisor() 的文档。

### `void QOpenGLExtraFunctions::glWaitSync(GLsync sync, GLbitfield flags, GLuint64 timeout)`

**作用与语义：**

调用 glWaitSync（`sync`， `flags`， `timeout` 的便利功能）。
该函数仅在 OpenGL ES 3.x 或 OpenGL 3.x 或 4.x 上下文中可用。在运行纯 OpenGL 时，该函数仅在该配置文件和版本中包含该函数核心或扩展时可用。
更多信息请参见 OpenGL ES 3.x 关于 glWaitSync() 的文档。

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

`QOpenGLExtraFunctions` 所属机制类型：Qt 类型机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
