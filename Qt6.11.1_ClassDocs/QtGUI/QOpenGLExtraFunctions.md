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

这里直接说明每个公开成员解决什么问题、参数代表什么、返回什么、会改变什么以及使用时容易出现什么问题。每一个公开签名都会有对应的中文解释。

本类共整理 218 个公开成员条目；没有独立长描述的 API 也会根据签名、类型和所属机制给出使用说明。

### `QOpenGLExtraFunctions::QOpenGLExtraFunctions()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QOpenGLExtraFunctions` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QOpenGLExtraFunctions::QOpenGLExtraFunctions(QOpenGLContext *context)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QOpenGLExtraFunctions` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `context`：类型为 `QOpenGLContext *`。没有默认值，调用时必须提供。上下文对象，用于限定回调连接的生命周期或解析/执行环境。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLExtraFunctions::glActiveShaderProgram(GLuint pipeline, GLuint program)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLExtraFunctions::glActiveShaderProgram` 用于执行与“gl、活动状态、Shader、Program”相关的操作。调用时要先确认当前状态和 `pipeline`、`program` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `pipeline`：类型为 `GLuint`。没有默认值，调用时必须提供。传入 `GLuint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `program`：类型为 `GLuint`。没有默认值，调用时必须提供。传入 `GLuint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLExtraFunctions::glBeginQuery(GLenum target, GLuint id)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLExtraFunctions::glBeginQuery` 用于执行与“gl、起始位置、查询”相关的操作。调用时要先确认当前状态和 `target`、`id` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `target`：类型为 `GLenum`。没有默认值，调用时必须提供。目标对象、目标属性或目标资源。要确认它在操作期间仍然有效，并支持所需能力。
- 参数 `id`：类型为 `GLuint`。没有默认值，调用时必须提供。传入 `GLuint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLExtraFunctions::glBeginTransformFeedback(GLenum primitiveMode)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLExtraFunctions::glBeginTransformFeedback` 用于执行与“gl、起始位置、Transform、Feedback”相关的操作。调用时要先确认当前状态和 `primitiveMode` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `primitiveMode`：类型为 `GLenum`。没有默认值，调用时必须提供。枚举或标志参数。先确认可用枚举值、互斥关系和默认值，必要时用按位或组合标志。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLExtraFunctions::glBindBufferBase(GLenum target, GLuint index, GLuint buffer)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLExtraFunctions::glBindBufferBase` 用于执行与“gl、绑定、Buffer、Base”相关的操作。调用时要先确认当前状态和 `target`、`index`、`buffer` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `target`：类型为 `GLenum`。没有默认值，调用时必须提供。目标对象、目标属性或目标资源。要确认它在操作期间仍然有效，并支持所需能力。
- 参数 `index`：类型为 `GLuint`。没有默认值，调用时必须提供。项目或数据索引。先确认索引基于 0 还是 1、是否允许越界/负数，以及调用后索引是否仍然有效。
- 参数 `buffer`：类型为 `GLuint`。没有默认值，调用时必须提供。传入 `GLuint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLExtraFunctions::glBindBufferRange(GLenum target, GLuint index, GLuint buffer, GLintptr offset, GLsizeiptr size)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLExtraFunctions::glBindBufferRange` 用于执行与“gl、绑定、Buffer、Range”相关的操作。调用时要先确认当前状态和 `target`、`index`、`buffer`、`offset`、`size` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `target`：类型为 `GLenum`。没有默认值，调用时必须提供。目标对象、目标属性或目标资源。要确认它在操作期间仍然有效，并支持所需能力。
- 参数 `index`：类型为 `GLuint`。没有默认值，调用时必须提供。项目或数据索引。先确认索引基于 0 还是 1、是否允许越界/负数，以及调用后索引是否仍然有效。
- 参数 `buffer`：类型为 `GLuint`。没有默认值，调用时必须提供。传入 `GLuint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `offset`：类型为 `GLintptr`。没有默认值，调用时必须提供。传入 `GLintptr` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `size`：类型为 `GLsizeiptr`。没有默认值，调用时必须提供。尺寸或长度，单位通常是像素、字节、元素数或时间，必须结合类型和类的上下文确认。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLExtraFunctions::glBindImageTexture(GLuint unit, GLuint texture, GLint level, GLboolean layered, GLint layer, GLenum access, GLenum format)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLExtraFunctions::glBindImageTexture` 用于执行与“gl、绑定、Image、Texture”相关的操作。调用时要先确认当前状态和 `unit`、`texture`、`level`、`layered`、`layer`、`access`、`format` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `unit`：类型为 `GLuint`。没有默认值，调用时必须提供。传入 `GLuint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `texture`：类型为 `GLuint`。没有默认值，调用时必须提供。传入 `GLuint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `level`：类型为 `GLint`。没有默认值，调用时必须提供。传入 `GLint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `layered`：类型为 `GLboolean`。没有默认值，调用时必须提供。传入 `GLboolean` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `layer`：类型为 `GLint`。没有默认值，调用时必须提供。传入 `GLint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `access`：类型为 `GLenum`。没有默认值，调用时必须提供。枚举或标志参数。先确认可用枚举值、互斥关系和默认值，必要时用按位或组合标志。
- 参数 `format`：类型为 `GLenum`。没有默认值，调用时必须提供。数据格式或显示格式。格式通常会影响解析、像素布局、精度、编码或兼容性。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLExtraFunctions::glBindProgramPipeline(GLuint pipeline)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLExtraFunctions::glBindProgramPipeline` 用于执行与“gl、绑定、Program、Pipeline”相关的操作。调用时要先确认当前状态和 `pipeline` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `pipeline`：类型为 `GLuint`。没有默认值，调用时必须提供。传入 `GLuint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLExtraFunctions::glBindSampler(GLuint unit, GLuint sampler)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLExtraFunctions::glBindSampler` 用于执行与“gl、绑定、Sampler”相关的操作。调用时要先确认当前状态和 `unit`、`sampler` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `unit`：类型为 `GLuint`。没有默认值，调用时必须提供。传入 `GLuint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `sampler`：类型为 `GLuint`。没有默认值，调用时必须提供。传入 `GLuint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLExtraFunctions::glBindTransformFeedback(GLenum target, GLuint id)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLExtraFunctions::glBindTransformFeedback` 用于执行与“gl、绑定、Transform、Feedback”相关的操作。调用时要先确认当前状态和 `target`、`id` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `target`：类型为 `GLenum`。没有默认值，调用时必须提供。目标对象、目标属性或目标资源。要确认它在操作期间仍然有效，并支持所需能力。
- 参数 `id`：类型为 `GLuint`。没有默认值，调用时必须提供。传入 `GLuint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLExtraFunctions::glBindVertexArray(GLuint array)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLExtraFunctions::glBindVertexArray` 用于执行与“gl、绑定、Vertex、Array”相关的操作。调用时要先确认当前状态和 `array` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `array`：类型为 `GLuint`。没有默认值，调用时必须提供。传入 `GLuint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLExtraFunctions::glBindVertexBuffer(GLuint bindingindex, GLuint buffer, GLintptr offset, GLsizei stride)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLExtraFunctions::glBindVertexBuffer` 用于执行与“gl、绑定、Vertex、Buffer”相关的操作。调用时要先确认当前状态和 `bindingindex`、`buffer`、`offset`、`stride` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `bindingindex`：类型为 `GLuint`。没有默认值，调用时必须提供。传入 `GLuint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `buffer`：类型为 `GLuint`。没有默认值，调用时必须提供。传入 `GLuint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `offset`：类型为 `GLintptr`。没有默认值，调用时必须提供。传入 `GLintptr` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `stride`：类型为 `GLsizei`。没有默认值，调用时必须提供。传入 `GLsizei` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLExtraFunctions::glBlendBarrier()`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLExtraFunctions::glBlendBarrier` 用于执行与“gl、Blend、Barrier”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLExtraFunctions::glBlendEquationSeparatei(GLuint buf, GLenum modeRGB, GLenum modeAlpha)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLExtraFunctions::glBlendEquationSeparatei` 用于执行与“gl、Blend、Equation、Separatei”相关的操作。调用时要先确认当前状态和 `buf`、`modeRGB`、`modeAlpha` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `buf`：类型为 `GLuint`。没有默认值，调用时必须提供。传入 `GLuint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `modeRGB`：类型为 `GLenum`。没有默认值，调用时必须提供。枚举或标志参数。先确认可用枚举值、互斥关系和默认值，必要时用按位或组合标志。
- 参数 `modeAlpha`：类型为 `GLenum`。没有默认值，调用时必须提供。枚举或标志参数。先确认可用枚举值、互斥关系和默认值，必要时用按位或组合标志。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLExtraFunctions::glBlendEquationi(GLuint buf, GLenum mode)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLExtraFunctions::glBlendEquationi` 用于执行与“gl、Blend、Equationi”相关的操作。调用时要先确认当前状态和 `buf`、`mode` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `buf`：类型为 `GLuint`。没有默认值，调用时必须提供。传入 `GLuint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `mode`：类型为 `GLenum`。没有默认值，调用时必须提供。模式枚举或位标志。它通常决定对象后续允许的操作和状态转换。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLExtraFunctions::glBlendFuncSeparatei(GLuint buf, GLenum srcRGB, GLenum dstRGB, GLenum srcAlpha, GLenum dstAlpha)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLExtraFunctions::glBlendFuncSeparatei` 用于执行与“gl、Blend、Func、Separatei”相关的操作。调用时要先确认当前状态和 `buf`、`srcRGB`、`dstRGB`、`srcAlpha`、`dstAlpha` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `buf`：类型为 `GLuint`。没有默认值，调用时必须提供。传入 `GLuint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `srcRGB`：类型为 `GLenum`。没有默认值，调用时必须提供。枚举或标志参数。先确认可用枚举值、互斥关系和默认值，必要时用按位或组合标志。
- 参数 `dstRGB`：类型为 `GLenum`。没有默认值，调用时必须提供。枚举或标志参数。先确认可用枚举值、互斥关系和默认值，必要时用按位或组合标志。
- 参数 `srcAlpha`：类型为 `GLenum`。没有默认值，调用时必须提供。枚举或标志参数。先确认可用枚举值、互斥关系和默认值，必要时用按位或组合标志。
- 参数 `dstAlpha`：类型为 `GLenum`。没有默认值，调用时必须提供。枚举或标志参数。先确认可用枚举值、互斥关系和默认值，必要时用按位或组合标志。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLExtraFunctions::glBlendFunci(GLuint buf, GLenum src, GLenum dst)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLExtraFunctions::glBlendFunci` 用于执行与“gl、Blend、Funci”相关的操作。调用时要先确认当前状态和 `buf`、`src`、`dst` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `buf`：类型为 `GLuint`。没有默认值，调用时必须提供。传入 `GLuint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `src`：类型为 `GLenum`。没有默认值，调用时必须提供。枚举或标志参数。先确认可用枚举值、互斥关系和默认值，必要时用按位或组合标志。
- 参数 `dst`：类型为 `GLenum`。没有默认值，调用时必须提供。枚举或标志参数。先确认可用枚举值、互斥关系和默认值，必要时用按位或组合标志。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLExtraFunctions::glBlitFramebuffer(GLint srcX0, GLint srcY0, GLint srcX1, GLint srcY1, GLint dstX0, GLint dstY0, GLint dstX1, GLint dstY1, GLbitfield mask, GLenum filter)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLExtraFunctions::glBlitFramebuffer` 用于执行与“gl、Blit、Framebuffer”相关的操作。调用时要先确认当前状态和 `srcX0`、`srcY0`、`srcX1`、`srcY1`、`dstX0`、`dstY0`、`dstX1`、`dstY1`、`mask`、`filter` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `srcX0`：类型为 `GLint`。没有默认值，调用时必须提供。传入 `GLint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `srcY0`：类型为 `GLint`。没有默认值，调用时必须提供。传入 `GLint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `srcX1`：类型为 `GLint`。没有默认值，调用时必须提供。传入 `GLint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `srcY1`：类型为 `GLint`。没有默认值，调用时必须提供。传入 `GLint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `dstX0`：类型为 `GLint`。没有默认值，调用时必须提供。传入 `GLint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `dstY0`：类型为 `GLint`。没有默认值，调用时必须提供。传入 `GLint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `dstX1`：类型为 `GLint`。没有默认值，调用时必须提供。传入 `GLint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `dstY1`：类型为 `GLint`。没有默认值，调用时必须提供。传入 `GLint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `mask`：类型为 `GLbitfield`。没有默认值，调用时必须提供。传入 `GLbitfield` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `filter`：类型为 `GLenum`。没有默认值，调用时必须提供。过滤条件、匹配器或过滤标志；要确认它作用于显示结果、输入数据还是事件传播。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLExtraFunctions::glClearBufferfi(GLenum buffer, GLint drawbuffer, GLfloat depth, GLint stencil)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLExtraFunctions::glClearBufferfi` 用于执行与“gl、清空、Bufferfi”相关的操作。调用时要先确认当前状态和 `buffer`、`drawbuffer`、`depth`、`stencil` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `buffer`：类型为 `GLenum`。没有默认值，调用时必须提供。枚举或标志参数。先确认可用枚举值、互斥关系和默认值，必要时用按位或组合标志。
- 参数 `drawbuffer`：类型为 `GLint`。没有默认值，调用时必须提供。传入 `GLint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `depth`：类型为 `GLfloat`。没有默认值，调用时必须提供。传入 `GLfloat` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `stencil`：类型为 `GLint`。没有默认值，调用时必须提供。传入 `GLint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLExtraFunctions::glClearBufferfv(GLenum buffer, GLint drawbuffer, const GLfloat *value)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLExtraFunctions::glClearBufferfv` 用于执行与“gl、清空、Bufferfv”相关的操作。调用时要先确认当前状态和 `buffer`、`drawbuffer`、`value` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `buffer`：类型为 `GLenum`。没有默认值，调用时必须提供。枚举或标志参数。先确认可用枚举值、互斥关系和默认值，必要时用按位或组合标志。
- 参数 `drawbuffer`：类型为 `GLint`。没有默认值，调用时必须提供。传入 `GLint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `value`：类型为 `const GLfloat *`。没有默认值，调用时必须提供。要读取或写入的值。要确认类型转换、默认值、所有权以及写入后是否触发通知。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLExtraFunctions::glClearBufferiv(GLenum buffer, GLint drawbuffer, const GLint *value)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLExtraFunctions::glClearBufferiv` 用于执行与“gl、清空、Bufferiv”相关的操作。调用时要先确认当前状态和 `buffer`、`drawbuffer`、`value` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `buffer`：类型为 `GLenum`。没有默认值，调用时必须提供。枚举或标志参数。先确认可用枚举值、互斥关系和默认值，必要时用按位或组合标志。
- 参数 `drawbuffer`：类型为 `GLint`。没有默认值，调用时必须提供。传入 `GLint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `value`：类型为 `const GLint *`。没有默认值，调用时必须提供。要读取或写入的值。要确认类型转换、默认值、所有权以及写入后是否触发通知。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLExtraFunctions::glClearBufferuiv(GLenum buffer, GLint drawbuffer, const GLuint *value)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLExtraFunctions::glClearBufferuiv` 用于执行与“gl、清空、Bufferuiv”相关的操作。调用时要先确认当前状态和 `buffer`、`drawbuffer`、`value` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `buffer`：类型为 `GLenum`。没有默认值，调用时必须提供。枚举或标志参数。先确认可用枚举值、互斥关系和默认值，必要时用按位或组合标志。
- 参数 `drawbuffer`：类型为 `GLint`。没有默认值，调用时必须提供。传入 `GLint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `value`：类型为 `const GLuint *`。没有默认值，调用时必须提供。要读取或写入的值。要确认类型转换、默认值、所有权以及写入后是否触发通知。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `GLenum QOpenGLExtraFunctions::glClientWaitSync(GLsync sync, GLbitfield flags, GLuint64 timeout)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLExtraFunctions::glClientWaitSync` 用于计算、查询或取得与“gl、Client、等待、Sync”相关的操作。调用时要先确认当前状态和 `sync`、`flags`、`timeout` 的有效范围；返回类型是 `GLenum`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`GLenum`。
- 参数 `sync`：类型为 `GLsync`。没有默认值，调用时必须提供。传入 `GLsync` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `flags`：类型为 `GLbitfield`。没有默认值，调用时必须提供。标志位组合。可以用按位或组合，调用前确认哪些标志互斥、哪些标志需要同时出现。
- 参数 `timeout`：类型为 `GLuint64`。没有默认值，调用时必须提供。超时时间或超时对象，可能表示等待时长，也可能表示 QNetworkReply/QTimer 等异步对象，不能只看名称判断。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLExtraFunctions::glColorMaski(GLuint index, GLboolean r, GLboolean g, GLboolean b, GLboolean a)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLExtraFunctions::glColorMaski` 用于执行与“gl、Color、Maski”相关的操作。调用时要先确认当前状态和 `index`、`r`、`g`、`b`、`a` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `index`：类型为 `GLuint`。没有默认值，调用时必须提供。项目或数据索引。先确认索引基于 0 还是 1、是否允许越界/负数，以及调用后索引是否仍然有效。
- 参数 `r`：类型为 `GLboolean`。没有默认值，调用时必须提供。传入 `GLboolean` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `g`：类型为 `GLboolean`。没有默认值，调用时必须提供。传入 `GLboolean` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `b`：类型为 `GLboolean`。没有默认值，调用时必须提供。传入 `GLboolean` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `a`：类型为 `GLboolean`。没有默认值，调用时必须提供。传入 `GLboolean` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLExtraFunctions::glCompressedTexImage3D(GLenum target, GLint level, GLenum internalformat, GLsizei width, GLsizei height, GLsizei depth, GLint border, GLsizei imageSize, const void *data)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLExtraFunctions::glCompressedTexImage3D` 用于执行与“gl、Compressed、Tex、Image、3、D”相关的操作。调用时要先确认当前状态和 `target`、`level`、`internalformat`、`width`、`height`、`depth`、`border`、`imageSize`、`data` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `target`：类型为 `GLenum`。没有默认值，调用时必须提供。目标对象、目标属性或目标资源。要确认它在操作期间仍然有效，并支持所需能力。
- 参数 `level`：类型为 `GLint`。没有默认值，调用时必须提供。传入 `GLint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `internalformat`：类型为 `GLenum`。没有默认值，调用时必须提供。枚举或标志参数。先确认可用枚举值、互斥关系和默认值，必要时用按位或组合标志。
- 参数 `width`：类型为 `GLsizei`。没有默认值，调用时必须提供。宽度，通常以像素、字符数或元素数量表示；要确认是否允许 0、负数和超出最大值。
- 参数 `height`：类型为 `GLsizei`。没有默认值，调用时必须提供。高度，通常以像素、字符数或元素数量表示；要确认是否允许 0、负数和超出最大值。
- 参数 `depth`：类型为 `GLsizei`。没有默认值，调用时必须提供。传入 `GLsizei` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `border`：类型为 `GLint`。没有默认值，调用时必须提供。传入 `GLint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `imageSize`：类型为 `GLsizei`。没有默认值，调用时必须提供。传入 `GLsizei` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `data`：类型为 `const void *`。没有默认值，调用时必须提供。数据载荷或要读取的数据。要确认编码、所有权、大小和是否允许为空。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLExtraFunctions::glCompressedTexSubImage3D(GLenum target, GLint level, GLint xoffset, GLint yoffset, GLint zoffset, GLsizei width, GLsizei height, GLsizei depth, GLenum format, GLsizei imageSize, const void *data)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLExtraFunctions::glCompressedTexSubImage3D` 用于执行与“gl、Compressed、Tex、Sub、Image、3、D”相关的操作。调用时要先确认当前状态和 `target`、`level`、`xoffset`、`yoffset`、`zoffset`、`width`、`height`、`depth`、`format`、`imageSize`、`data` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `target`：类型为 `GLenum`。没有默认值，调用时必须提供。目标对象、目标属性或目标资源。要确认它在操作期间仍然有效，并支持所需能力。
- 参数 `level`：类型为 `GLint`。没有默认值，调用时必须提供。传入 `GLint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `xoffset`：类型为 `GLint`。没有默认值，调用时必须提供。传入 `GLint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `yoffset`：类型为 `GLint`。没有默认值，调用时必须提供。传入 `GLint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `zoffset`：类型为 `GLint`。没有默认值，调用时必须提供。传入 `GLint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `width`：类型为 `GLsizei`。没有默认值，调用时必须提供。宽度，通常以像素、字符数或元素数量表示；要确认是否允许 0、负数和超出最大值。
- 参数 `height`：类型为 `GLsizei`。没有默认值，调用时必须提供。高度，通常以像素、字符数或元素数量表示；要确认是否允许 0、负数和超出最大值。
- 参数 `depth`：类型为 `GLsizei`。没有默认值，调用时必须提供。传入 `GLsizei` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `format`：类型为 `GLenum`。没有默认值，调用时必须提供。数据格式或显示格式。格式通常会影响解析、像素布局、精度、编码或兼容性。
- 参数 `imageSize`：类型为 `GLsizei`。没有默认值，调用时必须提供。传入 `GLsizei` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `data`：类型为 `const void *`。没有默认值，调用时必须提供。数据载荷或要读取的数据。要确认编码、所有权、大小和是否允许为空。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLExtraFunctions::glCopyBufferSubData(GLenum readTarget, GLenum writeTarget, GLintptr readOffset, GLintptr writeOffset, GLsizeiptr size)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLExtraFunctions::glCopyBufferSubData` 用于执行与“gl、Copy、Buffer、Sub、数据访问”相关的操作。调用时要先确认当前状态和 `readTarget`、`writeTarget`、`readOffset`、`writeOffset`、`size` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `readTarget`：类型为 `GLenum`。没有默认值，调用时必须提供。枚举或标志参数。先确认可用枚举值、互斥关系和默认值，必要时用按位或组合标志。
- 参数 `writeTarget`：类型为 `GLenum`。没有默认值，调用时必须提供。枚举或标志参数。先确认可用枚举值、互斥关系和默认值，必要时用按位或组合标志。
- 参数 `readOffset`：类型为 `GLintptr`。没有默认值，调用时必须提供。传入 `GLintptr` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `writeOffset`：类型为 `GLintptr`。没有默认值，调用时必须提供。传入 `GLintptr` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `size`：类型为 `GLsizeiptr`。没有默认值，调用时必须提供。尺寸或长度，单位通常是像素、字节、元素数或时间，必须结合类型和类的上下文确认。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLExtraFunctions::glCopyImageSubData(GLuint srcName, GLenum srcTarget, GLint srcLevel, GLint srcX, GLint srcY, GLint srcZ, GLuint dstName, GLenum dstTarget, GLint dstLevel, GLint dstX, GLint dstY, GLint dstZ, GLsizei srcWidth, GLsizei srcHeight, GLsizei srcDepth)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLExtraFunctions::glCopyImageSubData` 用于执行与“gl、Copy、Image、Sub、数据访问”相关的操作。调用时要先确认当前状态和 `srcName`、`srcTarget`、`srcLevel`、`srcX`、`srcY`、`srcZ`、`dstName`、`dstTarget`、`dstLevel`、`dstX`、`dstY`、`dstZ`、`srcWidth`、`srcHeight`、`srcDepth` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `srcName`：类型为 `GLuint`。没有默认值，调用时必须提供。传入 `GLuint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `srcTarget`：类型为 `GLenum`。没有默认值，调用时必须提供。枚举或标志参数。先确认可用枚举值、互斥关系和默认值，必要时用按位或组合标志。
- 参数 `srcLevel`：类型为 `GLint`。没有默认值，调用时必须提供。传入 `GLint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `srcX`：类型为 `GLint`。没有默认值，调用时必须提供。传入 `GLint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `srcY`：类型为 `GLint`。没有默认值，调用时必须提供。传入 `GLint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `srcZ`：类型为 `GLint`。没有默认值，调用时必须提供。传入 `GLint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `dstName`：类型为 `GLuint`。没有默认值，调用时必须提供。传入 `GLuint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `dstTarget`：类型为 `GLenum`。没有默认值，调用时必须提供。枚举或标志参数。先确认可用枚举值、互斥关系和默认值，必要时用按位或组合标志。
- 参数 `dstLevel`：类型为 `GLint`。没有默认值，调用时必须提供。传入 `GLint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `dstX`：类型为 `GLint`。没有默认值，调用时必须提供。传入 `GLint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `dstY`：类型为 `GLint`。没有默认值，调用时必须提供。传入 `GLint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `dstZ`：类型为 `GLint`。没有默认值，调用时必须提供。传入 `GLint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `srcWidth`：类型为 `GLsizei`。没有默认值，调用时必须提供。传入 `GLsizei` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `srcHeight`：类型为 `GLsizei`。没有默认值，调用时必须提供。传入 `GLsizei` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `srcDepth`：类型为 `GLsizei`。没有默认值，调用时必须提供。传入 `GLsizei` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLExtraFunctions::glCopyTexSubImage3D(GLenum target, GLint level, GLint xoffset, GLint yoffset, GLint zoffset, GLint x, GLint y, GLsizei width, GLsizei height)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLExtraFunctions::glCopyTexSubImage3D` 用于执行与“gl、Copy、Tex、Sub、Image、3、D”相关的操作。调用时要先确认当前状态和 `target`、`level`、`xoffset`、`yoffset`、`zoffset`、`x`、`y`、`width`、`height` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `target`：类型为 `GLenum`。没有默认值，调用时必须提供。目标对象、目标属性或目标资源。要确认它在操作期间仍然有效，并支持所需能力。
- 参数 `level`：类型为 `GLint`。没有默认值，调用时必须提供。传入 `GLint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `xoffset`：类型为 `GLint`。没有默认值，调用时必须提供。传入 `GLint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `yoffset`：类型为 `GLint`。没有默认值，调用时必须提供。传入 `GLint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `zoffset`：类型为 `GLint`。没有默认值，调用时必须提供。传入 `GLint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `x`：类型为 `GLint`。没有默认值，调用时必须提供。传入 `GLint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `y`：类型为 `GLint`。没有默认值，调用时必须提供。传入 `GLint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `width`：类型为 `GLsizei`。没有默认值，调用时必须提供。宽度，通常以像素、字符数或元素数量表示；要确认是否允许 0、负数和超出最大值。
- 参数 `height`：类型为 `GLsizei`。没有默认值，调用时必须提供。高度，通常以像素、字符数或元素数量表示；要确认是否允许 0、负数和超出最大值。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `GLuint QOpenGLExtraFunctions::glCreateShaderProgramv(GLenum type, GLsizei count, const GLchar *const *strings)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLExtraFunctions::glCreateShaderProgramv` 用于计算、查询或取得与“gl、创建、Shader、Programv”相关的操作。调用时要先确认当前状态和 `type`、`count`、`strings` 的有效范围；返回类型是 `GLuint`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`GLuint`。
- 参数 `type`：类型为 `GLenum`。没有默认值，调用时必须提供。类型、格式或策略枚举。要确认枚举值的适用范围和平台支持情况。
- 参数 `count`：类型为 `GLsizei`。没有默认值，调用时必须提供。传入 `GLsizei` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `strings`：类型为 `const GLchar *const *`。没有默认值，调用时必须提供。传入 `const GLchar *const *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLExtraFunctions::glDebugMessageCallback(GLDEBUGPROC callback, const void *userParam)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLExtraFunctions::glDebugMessageCallback` 用于执行与“gl、调试输出、Message、Callback”相关的操作。调用时要先确认当前状态和 `callback`、`userParam` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `callback`：类型为 `GLDEBUGPROC`。没有默认值，调用时必须提供。回调或函数对象。要确认可调用签名、捕获对象生命周期和执行线程，不要在回调中做长时间阻塞工作。
- 参数 `userParam`：类型为 `const void *`。没有默认值，调用时必须提供。传入 `const void *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLExtraFunctions::glDebugMessageControl(GLenum source, GLenum type, GLenum severity, GLsizei count, const GLuint *ids, GLboolean enabled)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLExtraFunctions::glDebugMessageControl` 用于执行与“gl、调试输出、Message、Control”相关的操作。调用时要先确认当前状态和 `source`、`type`、`severity`、`count`、`ids`、`enabled` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `source`：类型为 `GLenum`。没有默认值，调用时必须提供。源对象、源索引或源数据；它通常决定操作的输入，转换后要确认源的生命周期和线程归属。
- 参数 `type`：类型为 `GLenum`。没有默认值，调用时必须提供。类型、格式或策略枚举。要确认枚举值的适用范围和平台支持情况。
- 参数 `severity`：类型为 `GLenum`。没有默认值，调用时必须提供。枚举或标志参数。先确认可用枚举值、互斥关系和默认值，必要时用按位或组合标志。
- 参数 `count`：类型为 `GLsizei`。没有默认值，调用时必须提供。传入 `GLsizei` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `ids`：类型为 `const GLuint *`。没有默认值，调用时必须提供。传入 `const GLuint *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `enabled`：类型为 `GLboolean`。没有默认值，调用时必须提供。传入 `GLboolean` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLExtraFunctions::glDebugMessageInsert(GLenum source, GLenum type, GLuint id, GLenum severity, GLsizei length, const GLchar *buf)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLExtraFunctions::glDebugMessageInsert` 用于执行与“gl、调试输出、Message、插入”相关的操作。调用时要先确认当前状态和 `source`、`type`、`id`、`severity`、`length`、`buf` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `source`：类型为 `GLenum`。没有默认值，调用时必须提供。源对象、源索引或源数据；它通常决定操作的输入，转换后要确认源的生命周期和线程归属。
- 参数 `type`：类型为 `GLenum`。没有默认值，调用时必须提供。类型、格式或策略枚举。要确认枚举值的适用范围和平台支持情况。
- 参数 `id`：类型为 `GLuint`。没有默认值，调用时必须提供。传入 `GLuint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `severity`：类型为 `GLenum`。没有默认值，调用时必须提供。枚举或标志参数。先确认可用枚举值、互斥关系和默认值，必要时用按位或组合标志。
- 参数 `length`：类型为 `GLsizei`。没有默认值，调用时必须提供。传入 `GLsizei` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `buf`：类型为 `const GLchar *`。没有默认值，调用时必须提供。传入 `const GLchar *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLExtraFunctions::glDeleteProgramPipelines(GLsizei n, const GLuint *pipelines)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLExtraFunctions::glDeleteProgramPipelines` 用于执行与“gl、删除、Program、Pipelines”相关的操作。调用时要先确认当前状态和 `n`、`pipelines` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `n`：类型为 `GLsizei`。没有默认值，调用时必须提供。传入 `GLsizei` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `pipelines`：类型为 `const GLuint *`。没有默认值，调用时必须提供。传入 `const GLuint *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLExtraFunctions::glDeleteQueries(GLsizei n, const GLuint *ids)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLExtraFunctions::glDeleteQueries` 用于执行与“gl、删除、Queries”相关的操作。调用时要先确认当前状态和 `n`、`ids` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `n`：类型为 `GLsizei`。没有默认值，调用时必须提供。传入 `GLsizei` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `ids`：类型为 `const GLuint *`。没有默认值，调用时必须提供。传入 `const GLuint *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLExtraFunctions::glDeleteSamplers(GLsizei count, const GLuint *samplers)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLExtraFunctions::glDeleteSamplers` 用于执行与“gl、删除、Samplers”相关的操作。调用时要先确认当前状态和 `count`、`samplers` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `count`：类型为 `GLsizei`。没有默认值，调用时必须提供。传入 `GLsizei` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `samplers`：类型为 `const GLuint *`。没有默认值，调用时必须提供。传入 `const GLuint *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLExtraFunctions::glDeleteSync(GLsync sync)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLExtraFunctions::glDeleteSync` 用于执行与“gl、删除、Sync”相关的操作。调用时要先确认当前状态和 `sync` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `sync`：类型为 `GLsync`。没有默认值，调用时必须提供。传入 `GLsync` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLExtraFunctions::glDeleteTransformFeedbacks(GLsizei n, const GLuint *ids)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLExtraFunctions::glDeleteTransformFeedbacks` 用于执行与“gl、删除、Transform、Feedbacks”相关的操作。调用时要先确认当前状态和 `n`、`ids` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `n`：类型为 `GLsizei`。没有默认值，调用时必须提供。传入 `GLsizei` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `ids`：类型为 `const GLuint *`。没有默认值，调用时必须提供。传入 `const GLuint *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLExtraFunctions::glDeleteVertexArrays(GLsizei n, const GLuint *arrays)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLExtraFunctions::glDeleteVertexArrays` 用于执行与“gl、删除、Vertex、Arrays”相关的操作。调用时要先确认当前状态和 `n`、`arrays` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `n`：类型为 `GLsizei`。没有默认值，调用时必须提供。传入 `GLsizei` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `arrays`：类型为 `const GLuint *`。没有默认值，调用时必须提供。传入 `const GLuint *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLExtraFunctions::glDisablei(GLenum target, GLuint index)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLExtraFunctions::glDisablei` 用于执行与“gl、Disablei”相关的操作。调用时要先确认当前状态和 `target`、`index` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `target`：类型为 `GLenum`。没有默认值，调用时必须提供。目标对象、目标属性或目标资源。要确认它在操作期间仍然有效，并支持所需能力。
- 参数 `index`：类型为 `GLuint`。没有默认值，调用时必须提供。项目或数据索引。先确认索引基于 0 还是 1、是否允许越界/负数，以及调用后索引是否仍然有效。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLExtraFunctions::glDispatchCompute(GLuint num_groups_x, GLuint num_groups_y, GLuint num_groups_z)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLExtraFunctions::glDispatchCompute` 用于执行与“gl、Dispatch、Compute”相关的操作。调用时要先确认当前状态和 `num_groups_x`、`num_groups_y`、`num_groups_z` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `num_groups_x`：类型为 `GLuint`。没有默认值，调用时必须提供。传入 `GLuint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `num_groups_y`：类型为 `GLuint`。没有默认值，调用时必须提供。传入 `GLuint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `num_groups_z`：类型为 `GLuint`。没有默认值，调用时必须提供。传入 `GLuint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLExtraFunctions::glDispatchComputeIndirect(GLintptr indirect)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLExtraFunctions::glDispatchComputeIndirect` 用于执行与“gl、Dispatch、Compute、Indirect”相关的操作。调用时要先确认当前状态和 `indirect` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `indirect`：类型为 `GLintptr`。没有默认值，调用时必须提供。传入 `GLintptr` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLExtraFunctions::glDrawArraysIndirect(GLenum mode, const void *indirect)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLExtraFunctions::glDrawArraysIndirect` 用于执行与“gl、绘制、Arrays、Indirect”相关的操作。调用时要先确认当前状态和 `mode`、`indirect` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `mode`：类型为 `GLenum`。没有默认值，调用时必须提供。模式枚举或位标志。它通常决定对象后续允许的操作和状态转换。
- 参数 `indirect`：类型为 `const void *`。没有默认值，调用时必须提供。传入 `const void *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLExtraFunctions::glDrawArraysInstanced(GLenum mode, GLint first, GLsizei count, GLsizei instancecount)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLExtraFunctions::glDrawArraysInstanced` 用于执行与“gl、绘制、Arrays、Instanced”相关的操作。调用时要先确认当前状态和 `mode`、`first`、`count`、`instancecount` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `mode`：类型为 `GLenum`。没有默认值，调用时必须提供。模式枚举或位标志。它通常决定对象后续允许的操作和状态转换。
- 参数 `first`：类型为 `GLint`。没有默认值，调用时必须提供。传入 `GLint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `count`：类型为 `GLsizei`。没有默认值，调用时必须提供。传入 `GLsizei` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `instancecount`：类型为 `GLsizei`。没有默认值，调用时必须提供。传入 `GLsizei` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLExtraFunctions::glDrawBuffers(GLsizei n, const GLenum *bufs)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLExtraFunctions::glDrawBuffers` 用于执行与“gl、绘制、Buffers”相关的操作。调用时要先确认当前状态和 `n`、`bufs` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `n`：类型为 `GLsizei`。没有默认值，调用时必须提供。传入 `GLsizei` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `bufs`：类型为 `const GLenum *`。没有默认值，调用时必须提供。枚举或标志参数。先确认可用枚举值、互斥关系和默认值，必要时用按位或组合标志。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLExtraFunctions::glDrawElementsBaseVertex(GLenum mode, GLsizei count, GLenum type, const void *indices, GLint basevertex)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLExtraFunctions::glDrawElementsBaseVertex` 用于执行与“gl、绘制、Elements、Base、Vertex”相关的操作。调用时要先确认当前状态和 `mode`、`count`、`type`、`indices`、`basevertex` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `mode`：类型为 `GLenum`。没有默认值，调用时必须提供。模式枚举或位标志。它通常决定对象后续允许的操作和状态转换。
- 参数 `count`：类型为 `GLsizei`。没有默认值，调用时必须提供。传入 `GLsizei` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `type`：类型为 `GLenum`。没有默认值，调用时必须提供。类型、格式或策略枚举。要确认枚举值的适用范围和平台支持情况。
- 参数 `indices`：类型为 `const void *`。没有默认值，调用时必须提供。传入 `const void *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `basevertex`：类型为 `GLint`。没有默认值，调用时必须提供。传入 `GLint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLExtraFunctions::glDrawElementsIndirect(GLenum mode, GLenum type, const void *indirect)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLExtraFunctions::glDrawElementsIndirect` 用于执行与“gl、绘制、Elements、Indirect”相关的操作。调用时要先确认当前状态和 `mode`、`type`、`indirect` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `mode`：类型为 `GLenum`。没有默认值，调用时必须提供。模式枚举或位标志。它通常决定对象后续允许的操作和状态转换。
- 参数 `type`：类型为 `GLenum`。没有默认值，调用时必须提供。类型、格式或策略枚举。要确认枚举值的适用范围和平台支持情况。
- 参数 `indirect`：类型为 `const void *`。没有默认值，调用时必须提供。传入 `const void *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLExtraFunctions::glDrawElementsInstanced(GLenum mode, GLsizei count, GLenum type, const void *indices, GLsizei instancecount)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLExtraFunctions::glDrawElementsInstanced` 用于执行与“gl、绘制、Elements、Instanced”相关的操作。调用时要先确认当前状态和 `mode`、`count`、`type`、`indices`、`instancecount` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `mode`：类型为 `GLenum`。没有默认值，调用时必须提供。模式枚举或位标志。它通常决定对象后续允许的操作和状态转换。
- 参数 `count`：类型为 `GLsizei`。没有默认值，调用时必须提供。传入 `GLsizei` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `type`：类型为 `GLenum`。没有默认值，调用时必须提供。类型、格式或策略枚举。要确认枚举值的适用范围和平台支持情况。
- 参数 `indices`：类型为 `const void *`。没有默认值，调用时必须提供。传入 `const void *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `instancecount`：类型为 `GLsizei`。没有默认值，调用时必须提供。传入 `GLsizei` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLExtraFunctions::glDrawElementsInstancedBaseVertex(GLenum mode, GLsizei count, GLenum type, const void *indices, GLsizei instancecount, GLint basevertex)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLExtraFunctions::glDrawElementsInstancedBaseVertex` 用于执行与“gl、绘制、Elements、Instanced、Base、Vertex”相关的操作。调用时要先确认当前状态和 `mode`、`count`、`type`、`indices`、`instancecount`、`basevertex` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `mode`：类型为 `GLenum`。没有默认值，调用时必须提供。模式枚举或位标志。它通常决定对象后续允许的操作和状态转换。
- 参数 `count`：类型为 `GLsizei`。没有默认值，调用时必须提供。传入 `GLsizei` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `type`：类型为 `GLenum`。没有默认值，调用时必须提供。类型、格式或策略枚举。要确认枚举值的适用范围和平台支持情况。
- 参数 `indices`：类型为 `const void *`。没有默认值，调用时必须提供。传入 `const void *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `instancecount`：类型为 `GLsizei`。没有默认值，调用时必须提供。传入 `GLsizei` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `basevertex`：类型为 `GLint`。没有默认值，调用时必须提供。传入 `GLint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLExtraFunctions::glDrawRangeElements(GLenum mode, GLuint start, GLuint end, GLsizei count, GLenum type, const void *indices)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLExtraFunctions::glDrawRangeElements` 用于执行与“gl、绘制、Range、Elements”相关的操作。调用时要先确认当前状态和 `mode`、`start`、`end`、`count`、`type`、`indices` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `mode`：类型为 `GLenum`。没有默认值，调用时必须提供。模式枚举或位标志。它通常决定对象后续允许的操作和状态转换。
- 参数 `start`：类型为 `GLuint`。没有默认值，调用时必须提供。传入 `GLuint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `end`：类型为 `GLuint`。没有默认值，调用时必须提供。传入 `GLuint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `count`：类型为 `GLsizei`。没有默认值，调用时必须提供。传入 `GLsizei` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `type`：类型为 `GLenum`。没有默认值，调用时必须提供。类型、格式或策略枚举。要确认枚举值的适用范围和平台支持情况。
- 参数 `indices`：类型为 `const void *`。没有默认值，调用时必须提供。传入 `const void *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLExtraFunctions::glDrawRangeElementsBaseVertex(GLenum mode, GLuint start, GLuint end, GLsizei count, GLenum type, const void *indices, GLint basevertex)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLExtraFunctions::glDrawRangeElementsBaseVertex` 用于执行与“gl、绘制、Range、Elements、Base、Vertex”相关的操作。调用时要先确认当前状态和 `mode`、`start`、`end`、`count`、`type`、`indices`、`basevertex` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `mode`：类型为 `GLenum`。没有默认值，调用时必须提供。模式枚举或位标志。它通常决定对象后续允许的操作和状态转换。
- 参数 `start`：类型为 `GLuint`。没有默认值，调用时必须提供。传入 `GLuint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `end`：类型为 `GLuint`。没有默认值，调用时必须提供。传入 `GLuint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `count`：类型为 `GLsizei`。没有默认值，调用时必须提供。传入 `GLsizei` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `type`：类型为 `GLenum`。没有默认值，调用时必须提供。类型、格式或策略枚举。要确认枚举值的适用范围和平台支持情况。
- 参数 `indices`：类型为 `const void *`。没有默认值，调用时必须提供。传入 `const void *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `basevertex`：类型为 `GLint`。没有默认值，调用时必须提供。传入 `GLint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLExtraFunctions::glEnablei(GLenum target, GLuint index)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLExtraFunctions::glEnablei` 用于执行与“gl、Enablei”相关的操作。调用时要先确认当前状态和 `target`、`index` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `target`：类型为 `GLenum`。没有默认值，调用时必须提供。目标对象、目标属性或目标资源。要确认它在操作期间仍然有效，并支持所需能力。
- 参数 `index`：类型为 `GLuint`。没有默认值，调用时必须提供。项目或数据索引。先确认索引基于 0 还是 1、是否允许越界/负数，以及调用后索引是否仍然有效。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLExtraFunctions::glEndQuery(GLenum target)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLExtraFunctions::glEndQuery` 用于执行与“gl、结束、查询”相关的操作。调用时要先确认当前状态和 `target` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `target`：类型为 `GLenum`。没有默认值，调用时必须提供。目标对象、目标属性或目标资源。要确认它在操作期间仍然有效，并支持所需能力。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLExtraFunctions::glEndTransformFeedback()`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLExtraFunctions::glEndTransformFeedback` 用于执行与“gl、结束、Transform、Feedback”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `GLsync QOpenGLExtraFunctions::glFenceSync(GLenum condition, GLbitfield flags)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLExtraFunctions::glFenceSync` 用于计算、查询或取得与“gl、Fence、Sync”相关的操作。调用时要先确认当前状态和 `condition`、`flags` 的有效范围；返回类型是 `GLsync`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`GLsync`。
- 参数 `condition`：类型为 `GLenum`。没有默认值，调用时必须提供。枚举或标志参数。先确认可用枚举值、互斥关系和默认值，必要时用按位或组合标志。
- 参数 `flags`：类型为 `GLbitfield`。没有默认值，调用时必须提供。标志位组合。可以用按位或组合，调用前确认哪些标志互斥、哪些标志需要同时出现。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLExtraFunctions::glFlushMappedBufferRange(GLenum target, GLintptr offset, GLsizeiptr length)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLExtraFunctions::glFlushMappedBufferRange` 用于执行与“gl、刷新、Mapped、Buffer、Range”相关的操作。调用时要先确认当前状态和 `target`、`offset`、`length` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `target`：类型为 `GLenum`。没有默认值，调用时必须提供。目标对象、目标属性或目标资源。要确认它在操作期间仍然有效，并支持所需能力。
- 参数 `offset`：类型为 `GLintptr`。没有默认值，调用时必须提供。传入 `GLintptr` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `length`：类型为 `GLsizeiptr`。没有默认值，调用时必须提供。传入 `GLsizeiptr` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLExtraFunctions::glFramebufferParameteri(GLenum target, GLenum pname, GLint param)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLExtraFunctions::glFramebufferParameteri` 用于执行与“gl、Framebuffer、Parameteri”相关的操作。调用时要先确认当前状态和 `target`、`pname`、`param` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `target`：类型为 `GLenum`。没有默认值，调用时必须提供。目标对象、目标属性或目标资源。要确认它在操作期间仍然有效，并支持所需能力。
- 参数 `pname`：类型为 `GLenum`。没有默认值，调用时必须提供。枚举或标志参数。先确认可用枚举值、互斥关系和默认值，必要时用按位或组合标志。
- 参数 `param`：类型为 `GLint`。没有默认值，调用时必须提供。传入 `GLint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLExtraFunctions::glFramebufferTexture(GLenum target, GLenum attachment, GLuint texture, GLint level)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLExtraFunctions::glFramebufferTexture` 用于执行与“gl、Framebuffer、Texture”相关的操作。调用时要先确认当前状态和 `target`、`attachment`、`texture`、`level` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `target`：类型为 `GLenum`。没有默认值，调用时必须提供。目标对象、目标属性或目标资源。要确认它在操作期间仍然有效，并支持所需能力。
- 参数 `attachment`：类型为 `GLenum`。没有默认值，调用时必须提供。枚举或标志参数。先确认可用枚举值、互斥关系和默认值，必要时用按位或组合标志。
- 参数 `texture`：类型为 `GLuint`。没有默认值，调用时必须提供。传入 `GLuint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `level`：类型为 `GLint`。没有默认值，调用时必须提供。传入 `GLint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLExtraFunctions::glFramebufferTextureLayer(GLenum target, GLenum attachment, GLuint texture, GLint level, GLint layer)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLExtraFunctions::glFramebufferTextureLayer` 用于执行与“gl、Framebuffer、Texture、Layer”相关的操作。调用时要先确认当前状态和 `target`、`attachment`、`texture`、`level`、`layer` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `target`：类型为 `GLenum`。没有默认值，调用时必须提供。目标对象、目标属性或目标资源。要确认它在操作期间仍然有效，并支持所需能力。
- 参数 `attachment`：类型为 `GLenum`。没有默认值，调用时必须提供。枚举或标志参数。先确认可用枚举值、互斥关系和默认值，必要时用按位或组合标志。
- 参数 `texture`：类型为 `GLuint`。没有默认值，调用时必须提供。传入 `GLuint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `level`：类型为 `GLint`。没有默认值，调用时必须提供。传入 `GLint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `layer`：类型为 `GLint`。没有默认值，调用时必须提供。传入 `GLint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLExtraFunctions::glGenProgramPipelines(GLsizei n, GLuint *pipelines)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLExtraFunctions::glGenProgramPipelines` 用于执行与“gl、Gen、Program、Pipelines”相关的操作。调用时要先确认当前状态和 `n`、`pipelines` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `n`：类型为 `GLsizei`。没有默认值，调用时必须提供。传入 `GLsizei` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `pipelines`：类型为 `GLuint *`。没有默认值，调用时必须提供。传入 `GLuint *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLExtraFunctions::glGenQueries(GLsizei n, GLuint *ids)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLExtraFunctions::glGenQueries` 用于执行与“gl、Gen、Queries”相关的操作。调用时要先确认当前状态和 `n`、`ids` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `n`：类型为 `GLsizei`。没有默认值，调用时必须提供。传入 `GLsizei` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `ids`：类型为 `GLuint *`。没有默认值，调用时必须提供。传入 `GLuint *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLExtraFunctions::glGenSamplers(GLsizei count, GLuint *samplers)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLExtraFunctions::glGenSamplers` 用于执行与“gl、Gen、Samplers”相关的操作。调用时要先确认当前状态和 `count`、`samplers` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `count`：类型为 `GLsizei`。没有默认值，调用时必须提供。传入 `GLsizei` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `samplers`：类型为 `GLuint *`。没有默认值，调用时必须提供。传入 `GLuint *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLExtraFunctions::glGenTransformFeedbacks(GLsizei n, GLuint *ids)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLExtraFunctions::glGenTransformFeedbacks` 用于执行与“gl、Gen、Transform、Feedbacks”相关的操作。调用时要先确认当前状态和 `n`、`ids` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `n`：类型为 `GLsizei`。没有默认值，调用时必须提供。传入 `GLsizei` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `ids`：类型为 `GLuint *`。没有默认值，调用时必须提供。传入 `GLuint *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLExtraFunctions::glGenVertexArrays(GLsizei n, GLuint *arrays)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLExtraFunctions::glGenVertexArrays` 用于执行与“gl、Gen、Vertex、Arrays”相关的操作。调用时要先确认当前状态和 `n`、`arrays` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `n`：类型为 `GLsizei`。没有默认值，调用时必须提供。传入 `GLsizei` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `arrays`：类型为 `GLuint *`。没有默认值，调用时必须提供。传入 `GLuint *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLExtraFunctions::glGetActiveUniformBlockName(GLuint program, GLuint uniformBlockIndex, GLsizei bufSize, GLsizei *length, GLchar *uniformBlockName)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLExtraFunctions::glGetActiveUniformBlockName` 用于执行与“gl、Get、活动状态、Uniform、阻塞或屏蔽、名称”相关的操作。调用时要先确认当前状态和 `program`、`uniformBlockIndex`、`bufSize`、`length`、`uniformBlockName` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `program`：类型为 `GLuint`。没有默认值，调用时必须提供。传入 `GLuint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `uniformBlockIndex`：类型为 `GLuint`。没有默认值，调用时必须提供。传入 `GLuint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `bufSize`：类型为 `GLsizei`。没有默认值，调用时必须提供。传入 `GLsizei` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `length`：类型为 `GLsizei *`。没有默认值，调用时必须提供。传入 `GLsizei *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `uniformBlockName`：类型为 `GLchar *`。没有默认值，调用时必须提供。传入 `GLchar *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLExtraFunctions::glGetActiveUniformBlockiv(GLuint program, GLuint uniformBlockIndex, GLenum pname, GLint *params)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLExtraFunctions::glGetActiveUniformBlockiv` 用于执行与“gl、Get、活动状态、Uniform、Blockiv”相关的操作。调用时要先确认当前状态和 `program`、`uniformBlockIndex`、`pname`、`params` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `program`：类型为 `GLuint`。没有默认值，调用时必须提供。传入 `GLuint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `uniformBlockIndex`：类型为 `GLuint`。没有默认值，调用时必须提供。传入 `GLuint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `pname`：类型为 `GLenum`。没有默认值，调用时必须提供。枚举或标志参数。先确认可用枚举值、互斥关系和默认值，必要时用按位或组合标志。
- 参数 `params`：类型为 `GLint *`。没有默认值，调用时必须提供。传入 `GLint *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLExtraFunctions::glGetActiveUniformsiv(GLuint program, GLsizei uniformCount, const GLuint *uniformIndices, GLenum pname, GLint *params)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLExtraFunctions::glGetActiveUniformsiv` 用于执行与“gl、Get、活动状态、Uniformsiv”相关的操作。调用时要先确认当前状态和 `program`、`uniformCount`、`uniformIndices`、`pname`、`params` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `program`：类型为 `GLuint`。没有默认值，调用时必须提供。传入 `GLuint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `uniformCount`：类型为 `GLsizei`。没有默认值，调用时必须提供。传入 `GLsizei` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `uniformIndices`：类型为 `const GLuint *`。没有默认值，调用时必须提供。传入 `const GLuint *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `pname`：类型为 `GLenum`。没有默认值，调用时必须提供。枚举或标志参数。先确认可用枚举值、互斥关系和默认值，必要时用按位或组合标志。
- 参数 `params`：类型为 `GLint *`。没有默认值，调用时必须提供。传入 `GLint *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLExtraFunctions::glGetBooleani_v(GLenum target, GLuint index, GLboolean *data)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLExtraFunctions::glGetBooleani_v` 用于执行与“gl、Get、Booleani、v”相关的操作。调用时要先确认当前状态和 `target`、`index`、`data` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `target`：类型为 `GLenum`。没有默认值，调用时必须提供。目标对象、目标属性或目标资源。要确认它在操作期间仍然有效，并支持所需能力。
- 参数 `index`：类型为 `GLuint`。没有默认值，调用时必须提供。项目或数据索引。先确认索引基于 0 还是 1、是否允许越界/负数，以及调用后索引是否仍然有效。
- 参数 `data`：类型为 `GLboolean *`。没有默认值，调用时必须提供。数据载荷或要读取的数据。要确认编码、所有权、大小和是否允许为空。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLExtraFunctions::glGetBufferParameteri64v(GLenum target, GLenum pname, GLint64 *params)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLExtraFunctions::glGetBufferParameteri64v` 用于执行与“gl、Get、Buffer、Parameteri、64、v”相关的操作。调用时要先确认当前状态和 `target`、`pname`、`params` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `target`：类型为 `GLenum`。没有默认值，调用时必须提供。目标对象、目标属性或目标资源。要确认它在操作期间仍然有效，并支持所需能力。
- 参数 `pname`：类型为 `GLenum`。没有默认值，调用时必须提供。枚举或标志参数。先确认可用枚举值、互斥关系和默认值，必要时用按位或组合标志。
- 参数 `params`：类型为 `GLint64 *`。没有默认值，调用时必须提供。传入 `GLint64 *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLExtraFunctions::glGetBufferPointerv(GLenum target, GLenum pname, void **params)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLExtraFunctions::glGetBufferPointerv` 用于执行与“gl、Get、Buffer、Pointerv”相关的操作。调用时要先确认当前状态和 `target`、`pname`、`params` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `target`：类型为 `GLenum`。没有默认值，调用时必须提供。目标对象、目标属性或目标资源。要确认它在操作期间仍然有效，并支持所需能力。
- 参数 `pname`：类型为 `GLenum`。没有默认值，调用时必须提供。枚举或标志参数。先确认可用枚举值、互斥关系和默认值，必要时用按位或组合标志。
- 参数 `params`：类型为 `void **`。没有默认值，调用时必须提供。传入 `void **` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `GLuint QOpenGLExtraFunctions::glGetDebugMessageLog(GLuint count, GLsizei bufSize, GLenum *sources, GLenum *types, GLuint *ids, GLenum *severities, GLsizei *lengths, GLchar *messageLog)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLExtraFunctions::glGetDebugMessageLog` 用于计算、查询或取得与“gl、Get、调试输出、Message、Log”相关的操作。调用时要先确认当前状态和 `count`、`bufSize`、`sources`、`types`、`ids`、`severities`、`lengths`、`messageLog` 的有效范围；返回类型是 `GLuint`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`GLuint`。
- 参数 `count`：类型为 `GLuint`。没有默认值，调用时必须提供。传入 `GLuint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `bufSize`：类型为 `GLsizei`。没有默认值，调用时必须提供。传入 `GLsizei` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `sources`：类型为 `GLenum *`。没有默认值，调用时必须提供。枚举或标志参数。先确认可用枚举值、互斥关系和默认值，必要时用按位或组合标志。
- 参数 `types`：类型为 `GLenum *`。没有默认值，调用时必须提供。枚举或标志参数。先确认可用枚举值、互斥关系和默认值，必要时用按位或组合标志。
- 参数 `ids`：类型为 `GLuint *`。没有默认值，调用时必须提供。传入 `GLuint *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `severities`：类型为 `GLenum *`。没有默认值，调用时必须提供。枚举或标志参数。先确认可用枚举值、互斥关系和默认值，必要时用按位或组合标志。
- 参数 `lengths`：类型为 `GLsizei *`。没有默认值，调用时必须提供。传入 `GLsizei *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `messageLog`：类型为 `GLchar *`。没有默认值，调用时必须提供。传入 `GLchar *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `GLint QOpenGLExtraFunctions::glGetFragDataLocation(GLuint program, const GLchar *name)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLExtraFunctions::glGetFragDataLocation` 用于计算、查询或取得与“gl、Get、Frag、数据访问、Location”相关的操作。调用时要先确认当前状态和 `program`、`name` 的有效范围；返回类型是 `GLint`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`GLint`。
- 参数 `program`：类型为 `GLuint`。没有默认值，调用时必须提供。传入 `GLuint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `name`：类型为 `const GLchar *`。没有默认值，调用时必须提供。名称或键。通常是稳定的 API/配置标识，不应随意使用显示文本替代。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLExtraFunctions::glGetFramebufferParameteriv(GLenum target, GLenum pname, GLint *params)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLExtraFunctions::glGetFramebufferParameteriv` 用于执行与“gl、Get、Framebuffer、Parameteriv”相关的操作。调用时要先确认当前状态和 `target`、`pname`、`params` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `target`：类型为 `GLenum`。没有默认值，调用时必须提供。目标对象、目标属性或目标资源。要确认它在操作期间仍然有效，并支持所需能力。
- 参数 `pname`：类型为 `GLenum`。没有默认值，调用时必须提供。枚举或标志参数。先确认可用枚举值、互斥关系和默认值，必要时用按位或组合标志。
- 参数 `params`：类型为 `GLint *`。没有默认值，调用时必须提供。传入 `GLint *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `GLenum QOpenGLExtraFunctions::glGetGraphicsResetStatus()`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLExtraFunctions::glGetGraphicsResetStatus` 用于计算、查询或取得与“gl、Get、Graphics、重置、状态”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `GLenum`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`GLenum`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLExtraFunctions::glGetInteger64i_v(GLenum target, GLuint index, GLint64 *data)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLExtraFunctions::glGetInteger64i_v` 用于执行与“gl、Get、Integer、64、i、v”相关的操作。调用时要先确认当前状态和 `target`、`index`、`data` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `target`：类型为 `GLenum`。没有默认值，调用时必须提供。目标对象、目标属性或目标资源。要确认它在操作期间仍然有效，并支持所需能力。
- 参数 `index`：类型为 `GLuint`。没有默认值，调用时必须提供。项目或数据索引。先确认索引基于 0 还是 1、是否允许越界/负数，以及调用后索引是否仍然有效。
- 参数 `data`：类型为 `GLint64 *`。没有默认值，调用时必须提供。数据载荷或要读取的数据。要确认编码、所有权、大小和是否允许为空。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLExtraFunctions::glGetInteger64v(GLenum pname, GLint64 *data)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLExtraFunctions::glGetInteger64v` 用于执行与“gl、Get、Integer、64、v”相关的操作。调用时要先确认当前状态和 `pname`、`data` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `pname`：类型为 `GLenum`。没有默认值，调用时必须提供。枚举或标志参数。先确认可用枚举值、互斥关系和默认值，必要时用按位或组合标志。
- 参数 `data`：类型为 `GLint64 *`。没有默认值，调用时必须提供。数据载荷或要读取的数据。要确认编码、所有权、大小和是否允许为空。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLExtraFunctions::glGetIntegeri_v(GLenum target, GLuint index, GLint *data)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLExtraFunctions::glGetIntegeri_v` 用于执行与“gl、Get、Integeri、v”相关的操作。调用时要先确认当前状态和 `target`、`index`、`data` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `target`：类型为 `GLenum`。没有默认值，调用时必须提供。目标对象、目标属性或目标资源。要确认它在操作期间仍然有效，并支持所需能力。
- 参数 `index`：类型为 `GLuint`。没有默认值，调用时必须提供。项目或数据索引。先确认索引基于 0 还是 1、是否允许越界/负数，以及调用后索引是否仍然有效。
- 参数 `data`：类型为 `GLint *`。没有默认值，调用时必须提供。数据载荷或要读取的数据。要确认编码、所有权、大小和是否允许为空。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLExtraFunctions::glGetInternalformativ(GLenum target, GLenum internalformat, GLenum pname, GLsizei bufSize, GLint *params)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLExtraFunctions::glGetInternalformativ` 用于执行与“gl、Get、Internalformativ”相关的操作。调用时要先确认当前状态和 `target`、`internalformat`、`pname`、`bufSize`、`params` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `target`：类型为 `GLenum`。没有默认值，调用时必须提供。目标对象、目标属性或目标资源。要确认它在操作期间仍然有效，并支持所需能力。
- 参数 `internalformat`：类型为 `GLenum`。没有默认值，调用时必须提供。枚举或标志参数。先确认可用枚举值、互斥关系和默认值，必要时用按位或组合标志。
- 参数 `pname`：类型为 `GLenum`。没有默认值，调用时必须提供。枚举或标志参数。先确认可用枚举值、互斥关系和默认值，必要时用按位或组合标志。
- 参数 `bufSize`：类型为 `GLsizei`。没有默认值，调用时必须提供。传入 `GLsizei` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `params`：类型为 `GLint *`。没有默认值，调用时必须提供。传入 `GLint *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLExtraFunctions::glGetMultisamplefv(GLenum pname, GLuint index, GLfloat *val)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLExtraFunctions::glGetMultisamplefv` 用于执行与“gl、Get、Multisamplefv”相关的操作。调用时要先确认当前状态和 `pname`、`index`、`val` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `pname`：类型为 `GLenum`。没有默认值，调用时必须提供。枚举或标志参数。先确认可用枚举值、互斥关系和默认值，必要时用按位或组合标志。
- 参数 `index`：类型为 `GLuint`。没有默认值，调用时必须提供。项目或数据索引。先确认索引基于 0 还是 1、是否允许越界/负数，以及调用后索引是否仍然有效。
- 参数 `val`：类型为 `GLfloat *`。没有默认值，调用时必须提供。传入 `GLfloat *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLExtraFunctions::glGetObjectLabel(GLenum identifier, GLuint name, GLsizei bufSize, GLsizei *length, GLchar *label)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLExtraFunctions::glGetObjectLabel` 用于执行与“gl、Get、Object、Label”相关的操作。调用时要先确认当前状态和 `identifier`、`name`、`bufSize`、`length`、`label` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `identifier`：类型为 `GLenum`。没有默认值，调用时必须提供。枚举或标志参数。先确认可用枚举值、互斥关系和默认值，必要时用按位或组合标志。
- 参数 `name`：类型为 `GLuint`。没有默认值，调用时必须提供。名称或键。通常是稳定的 API/配置标识，不应随意使用显示文本替代。
- 参数 `bufSize`：类型为 `GLsizei`。没有默认值，调用时必须提供。传入 `GLsizei` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `length`：类型为 `GLsizei *`。没有默认值，调用时必须提供。传入 `GLsizei *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `label`：类型为 `GLchar *`。没有默认值，调用时必须提供。传入 `GLchar *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLExtraFunctions::glGetObjectPtrLabel(const void *ptr, GLsizei bufSize, GLsizei *length, GLchar *label)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLExtraFunctions::glGetObjectPtrLabel` 用于执行与“gl、Get、Object、Ptr、Label”相关的操作。调用时要先确认当前状态和 `ptr`、`bufSize`、`length`、`label` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `ptr`：类型为 `const void *`。没有默认值，调用时必须提供。传入 `const void *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `bufSize`：类型为 `GLsizei`。没有默认值，调用时必须提供。传入 `GLsizei` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `length`：类型为 `GLsizei *`。没有默认值，调用时必须提供。传入 `GLsizei *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `label`：类型为 `GLchar *`。没有默认值，调用时必须提供。传入 `GLchar *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLExtraFunctions::glGetPointerv(GLenum pname, void **params)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLExtraFunctions::glGetPointerv` 用于执行与“gl、Get、Pointerv”相关的操作。调用时要先确认当前状态和 `pname`、`params` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `pname`：类型为 `GLenum`。没有默认值，调用时必须提供。枚举或标志参数。先确认可用枚举值、互斥关系和默认值，必要时用按位或组合标志。
- 参数 `params`：类型为 `void **`。没有默认值，调用时必须提供。传入 `void **` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLExtraFunctions::glGetProgramBinary(GLuint program, GLsizei bufSize, GLsizei *length, GLenum *binaryFormat, void *binary)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLExtraFunctions::glGetProgramBinary` 用于执行与“gl、Get、Program、Binary”相关的操作。调用时要先确认当前状态和 `program`、`bufSize`、`length`、`binaryFormat`、`binary` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `program`：类型为 `GLuint`。没有默认值，调用时必须提供。传入 `GLuint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `bufSize`：类型为 `GLsizei`。没有默认值，调用时必须提供。传入 `GLsizei` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `length`：类型为 `GLsizei *`。没有默认值，调用时必须提供。传入 `GLsizei *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `binaryFormat`：类型为 `GLenum *`。没有默认值，调用时必须提供。枚举或标志参数。先确认可用枚举值、互斥关系和默认值，必要时用按位或组合标志。
- 参数 `binary`：类型为 `void *`。没有默认值，调用时必须提供。传入 `void *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLExtraFunctions::glGetProgramInterfaceiv(GLuint program, GLenum programInterface, GLenum pname, GLint *params)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLExtraFunctions::glGetProgramInterfaceiv` 用于执行与“gl、Get、Program、Interfaceiv”相关的操作。调用时要先确认当前状态和 `program`、`programInterface`、`pname`、`params` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `program`：类型为 `GLuint`。没有默认值，调用时必须提供。传入 `GLuint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `programInterface`：类型为 `GLenum`。没有默认值，调用时必须提供。枚举或标志参数。先确认可用枚举值、互斥关系和默认值，必要时用按位或组合标志。
- 参数 `pname`：类型为 `GLenum`。没有默认值，调用时必须提供。枚举或标志参数。先确认可用枚举值、互斥关系和默认值，必要时用按位或组合标志。
- 参数 `params`：类型为 `GLint *`。没有默认值，调用时必须提供。传入 `GLint *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLExtraFunctions::glGetProgramPipelineInfoLog(GLuint pipeline, GLsizei bufSize, GLsizei *length, GLchar *infoLog)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLExtraFunctions::glGetProgramPipelineInfoLog` 用于执行与“gl、Get、Program、Pipeline、Info、Log”相关的操作。调用时要先确认当前状态和 `pipeline`、`bufSize`、`length`、`infoLog` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `pipeline`：类型为 `GLuint`。没有默认值，调用时必须提供。传入 `GLuint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `bufSize`：类型为 `GLsizei`。没有默认值，调用时必须提供。传入 `GLsizei` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `length`：类型为 `GLsizei *`。没有默认值，调用时必须提供。传入 `GLsizei *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `infoLog`：类型为 `GLchar *`。没有默认值，调用时必须提供。传入 `GLchar *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLExtraFunctions::glGetProgramPipelineiv(GLuint pipeline, GLenum pname, GLint *params)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLExtraFunctions::glGetProgramPipelineiv` 用于执行与“gl、Get、Program、Pipelineiv”相关的操作。调用时要先确认当前状态和 `pipeline`、`pname`、`params` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `pipeline`：类型为 `GLuint`。没有默认值，调用时必须提供。传入 `GLuint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `pname`：类型为 `GLenum`。没有默认值，调用时必须提供。枚举或标志参数。先确认可用枚举值、互斥关系和默认值，必要时用按位或组合标志。
- 参数 `params`：类型为 `GLint *`。没有默认值，调用时必须提供。传入 `GLint *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `GLuint QOpenGLExtraFunctions::glGetProgramResourceIndex(GLuint program, GLenum programInterface, const GLchar *name)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLExtraFunctions::glGetProgramResourceIndex` 用于计算、查询或取得与“gl、Get、Program、Resource、索引”相关的操作。调用时要先确认当前状态和 `program`、`programInterface`、`name` 的有效范围；返回类型是 `GLuint`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`GLuint`。
- 参数 `program`：类型为 `GLuint`。没有默认值，调用时必须提供。传入 `GLuint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `programInterface`：类型为 `GLenum`。没有默认值，调用时必须提供。枚举或标志参数。先确认可用枚举值、互斥关系和默认值，必要时用按位或组合标志。
- 参数 `name`：类型为 `const GLchar *`。没有默认值，调用时必须提供。名称或键。通常是稳定的 API/配置标识，不应随意使用显示文本替代。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `GLint QOpenGLExtraFunctions::glGetProgramResourceLocation(GLuint program, GLenum programInterface, const GLchar *name)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLExtraFunctions::glGetProgramResourceLocation` 用于计算、查询或取得与“gl、Get、Program、Resource、Location”相关的操作。调用时要先确认当前状态和 `program`、`programInterface`、`name` 的有效范围；返回类型是 `GLint`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`GLint`。
- 参数 `program`：类型为 `GLuint`。没有默认值，调用时必须提供。传入 `GLuint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `programInterface`：类型为 `GLenum`。没有默认值，调用时必须提供。枚举或标志参数。先确认可用枚举值、互斥关系和默认值，必要时用按位或组合标志。
- 参数 `name`：类型为 `const GLchar *`。没有默认值，调用时必须提供。名称或键。通常是稳定的 API/配置标识，不应随意使用显示文本替代。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLExtraFunctions::glGetProgramResourceName(GLuint program, GLenum programInterface, GLuint index, GLsizei bufSize, GLsizei *length, GLchar *name)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLExtraFunctions::glGetProgramResourceName` 用于执行与“gl、Get、Program、Resource、名称”相关的操作。调用时要先确认当前状态和 `program`、`programInterface`、`index`、`bufSize`、`length`、`name` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `program`：类型为 `GLuint`。没有默认值，调用时必须提供。传入 `GLuint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `programInterface`：类型为 `GLenum`。没有默认值，调用时必须提供。枚举或标志参数。先确认可用枚举值、互斥关系和默认值，必要时用按位或组合标志。
- 参数 `index`：类型为 `GLuint`。没有默认值，调用时必须提供。项目或数据索引。先确认索引基于 0 还是 1、是否允许越界/负数，以及调用后索引是否仍然有效。
- 参数 `bufSize`：类型为 `GLsizei`。没有默认值，调用时必须提供。传入 `GLsizei` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `length`：类型为 `GLsizei *`。没有默认值，调用时必须提供。传入 `GLsizei *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `name`：类型为 `GLchar *`。没有默认值，调用时必须提供。名称或键。通常是稳定的 API/配置标识，不应随意使用显示文本替代。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLExtraFunctions::glGetProgramResourceiv(GLuint program, GLenum programInterface, GLuint index, GLsizei propCount, const GLenum *props, GLsizei bufSize, GLsizei *length, GLint *params)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLExtraFunctions::glGetProgramResourceiv` 用于执行与“gl、Get、Program、Resourceiv”相关的操作。调用时要先确认当前状态和 `program`、`programInterface`、`index`、`propCount`、`props`、`bufSize`、`length`、`params` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `program`：类型为 `GLuint`。没有默认值，调用时必须提供。传入 `GLuint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `programInterface`：类型为 `GLenum`。没有默认值，调用时必须提供。枚举或标志参数。先确认可用枚举值、互斥关系和默认值，必要时用按位或组合标志。
- 参数 `index`：类型为 `GLuint`。没有默认值，调用时必须提供。项目或数据索引。先确认索引基于 0 还是 1、是否允许越界/负数，以及调用后索引是否仍然有效。
- 参数 `propCount`：类型为 `GLsizei`。没有默认值，调用时必须提供。传入 `GLsizei` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `props`：类型为 `const GLenum *`。没有默认值，调用时必须提供。枚举或标志参数。先确认可用枚举值、互斥关系和默认值，必要时用按位或组合标志。
- 参数 `bufSize`：类型为 `GLsizei`。没有默认值，调用时必须提供。传入 `GLsizei` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `length`：类型为 `GLsizei *`。没有默认值，调用时必须提供。传入 `GLsizei *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `params`：类型为 `GLint *`。没有默认值，调用时必须提供。传入 `GLint *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLExtraFunctions::glGetQueryObjectuiv(GLuint id, GLenum pname, GLuint *params)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLExtraFunctions::glGetQueryObjectuiv` 用于执行与“gl、Get、查询、Objectuiv”相关的操作。调用时要先确认当前状态和 `id`、`pname`、`params` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `id`：类型为 `GLuint`。没有默认值，调用时必须提供。传入 `GLuint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `pname`：类型为 `GLenum`。没有默认值，调用时必须提供。枚举或标志参数。先确认可用枚举值、互斥关系和默认值，必要时用按位或组合标志。
- 参数 `params`：类型为 `GLuint *`。没有默认值，调用时必须提供。传入 `GLuint *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLExtraFunctions::glGetQueryiv(GLenum target, GLenum pname, GLint *params)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLExtraFunctions::glGetQueryiv` 用于执行与“gl、Get、Queryiv”相关的操作。调用时要先确认当前状态和 `target`、`pname`、`params` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `target`：类型为 `GLenum`。没有默认值，调用时必须提供。目标对象、目标属性或目标资源。要确认它在操作期间仍然有效，并支持所需能力。
- 参数 `pname`：类型为 `GLenum`。没有默认值，调用时必须提供。枚举或标志参数。先确认可用枚举值、互斥关系和默认值，必要时用按位或组合标志。
- 参数 `params`：类型为 `GLint *`。没有默认值，调用时必须提供。传入 `GLint *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLExtraFunctions::glGetSamplerParameterIiv(GLuint sampler, GLenum pname, GLint *params)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLExtraFunctions::glGetSamplerParameterIiv` 用于执行与“gl、Get、Sampler、Parameter、Iiv”相关的操作。调用时要先确认当前状态和 `sampler`、`pname`、`params` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `sampler`：类型为 `GLuint`。没有默认值，调用时必须提供。传入 `GLuint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `pname`：类型为 `GLenum`。没有默认值，调用时必须提供。枚举或标志参数。先确认可用枚举值、互斥关系和默认值，必要时用按位或组合标志。
- 参数 `params`：类型为 `GLint *`。没有默认值，调用时必须提供。传入 `GLint *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLExtraFunctions::glGetSamplerParameterIuiv(GLuint sampler, GLenum pname, GLuint *params)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLExtraFunctions::glGetSamplerParameterIuiv` 用于执行与“gl、Get、Sampler、Parameter、Iuiv”相关的操作。调用时要先确认当前状态和 `sampler`、`pname`、`params` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `sampler`：类型为 `GLuint`。没有默认值，调用时必须提供。传入 `GLuint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `pname`：类型为 `GLenum`。没有默认值，调用时必须提供。枚举或标志参数。先确认可用枚举值、互斥关系和默认值，必要时用按位或组合标志。
- 参数 `params`：类型为 `GLuint *`。没有默认值，调用时必须提供。传入 `GLuint *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLExtraFunctions::glGetSamplerParameterfv(GLuint sampler, GLenum pname, GLfloat *params)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLExtraFunctions::glGetSamplerParameterfv` 用于执行与“gl、Get、Sampler、Parameterfv”相关的操作。调用时要先确认当前状态和 `sampler`、`pname`、`params` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `sampler`：类型为 `GLuint`。没有默认值，调用时必须提供。传入 `GLuint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `pname`：类型为 `GLenum`。没有默认值，调用时必须提供。枚举或标志参数。先确认可用枚举值、互斥关系和默认值，必要时用按位或组合标志。
- 参数 `params`：类型为 `GLfloat *`。没有默认值，调用时必须提供。传入 `GLfloat *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLExtraFunctions::glGetSamplerParameteriv(GLuint sampler, GLenum pname, GLint *params)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLExtraFunctions::glGetSamplerParameteriv` 用于执行与“gl、Get、Sampler、Parameteriv”相关的操作。调用时要先确认当前状态和 `sampler`、`pname`、`params` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `sampler`：类型为 `GLuint`。没有默认值，调用时必须提供。传入 `GLuint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `pname`：类型为 `GLenum`。没有默认值，调用时必须提供。枚举或标志参数。先确认可用枚举值、互斥关系和默认值，必要时用按位或组合标志。
- 参数 `params`：类型为 `GLint *`。没有默认值，调用时必须提供。传入 `GLint *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `const GLubyte *QOpenGLExtraFunctions::glGetStringi(GLenum name, GLuint index)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLExtraFunctions::glGetStringi` 用于计算、查询或取得与“gl、Get、Stringi”相关的操作。调用时要先确认当前状态和 `name`、`index` 的有效范围；返回类型是 `const GLubyte *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`const GLubyte *`。
- 参数 `name`：类型为 `GLenum`。没有默认值，调用时必须提供。名称或键。通常是稳定的 API/配置标识，不应随意使用显示文本替代。
- 参数 `index`：类型为 `GLuint`。没有默认值，调用时必须提供。项目或数据索引。先确认索引基于 0 还是 1、是否允许越界/负数，以及调用后索引是否仍然有效。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLExtraFunctions::glGetSynciv(GLsync sync, GLenum pname, GLsizei bufSize, GLsizei *length, GLint *values)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLExtraFunctions::glGetSynciv` 用于执行与“gl、Get、Synciv”相关的操作。调用时要先确认当前状态和 `sync`、`pname`、`bufSize`、`length`、`values` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `sync`：类型为 `GLsync`。没有默认值，调用时必须提供。传入 `GLsync` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `pname`：类型为 `GLenum`。没有默认值，调用时必须提供。枚举或标志参数。先确认可用枚举值、互斥关系和默认值，必要时用按位或组合标志。
- 参数 `bufSize`：类型为 `GLsizei`。没有默认值，调用时必须提供。传入 `GLsizei` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `length`：类型为 `GLsizei *`。没有默认值，调用时必须提供。传入 `GLsizei *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `values`：类型为 `GLint *`。没有默认值，调用时必须提供。传入 `GLint *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLExtraFunctions::glGetTexLevelParameterfv(GLenum target, GLint level, GLenum pname, GLfloat *params)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLExtraFunctions::glGetTexLevelParameterfv` 用于执行与“gl、Get、Tex、Level、Parameterfv”相关的操作。调用时要先确认当前状态和 `target`、`level`、`pname`、`params` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `target`：类型为 `GLenum`。没有默认值，调用时必须提供。目标对象、目标属性或目标资源。要确认它在操作期间仍然有效，并支持所需能力。
- 参数 `level`：类型为 `GLint`。没有默认值，调用时必须提供。传入 `GLint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `pname`：类型为 `GLenum`。没有默认值，调用时必须提供。枚举或标志参数。先确认可用枚举值、互斥关系和默认值，必要时用按位或组合标志。
- 参数 `params`：类型为 `GLfloat *`。没有默认值，调用时必须提供。传入 `GLfloat *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLExtraFunctions::glGetTexLevelParameteriv(GLenum target, GLint level, GLenum pname, GLint *params)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLExtraFunctions::glGetTexLevelParameteriv` 用于执行与“gl、Get、Tex、Level、Parameteriv”相关的操作。调用时要先确认当前状态和 `target`、`level`、`pname`、`params` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `target`：类型为 `GLenum`。没有默认值，调用时必须提供。目标对象、目标属性或目标资源。要确认它在操作期间仍然有效，并支持所需能力。
- 参数 `level`：类型为 `GLint`。没有默认值，调用时必须提供。传入 `GLint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `pname`：类型为 `GLenum`。没有默认值，调用时必须提供。枚举或标志参数。先确认可用枚举值、互斥关系和默认值，必要时用按位或组合标志。
- 参数 `params`：类型为 `GLint *`。没有默认值，调用时必须提供。传入 `GLint *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLExtraFunctions::glGetTexParameterIiv(GLenum target, GLenum pname, GLint *params)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLExtraFunctions::glGetTexParameterIiv` 用于执行与“gl、Get、Tex、Parameter、Iiv”相关的操作。调用时要先确认当前状态和 `target`、`pname`、`params` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `target`：类型为 `GLenum`。没有默认值，调用时必须提供。目标对象、目标属性或目标资源。要确认它在操作期间仍然有效，并支持所需能力。
- 参数 `pname`：类型为 `GLenum`。没有默认值，调用时必须提供。枚举或标志参数。先确认可用枚举值、互斥关系和默认值，必要时用按位或组合标志。
- 参数 `params`：类型为 `GLint *`。没有默认值，调用时必须提供。传入 `GLint *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLExtraFunctions::glGetTexParameterIuiv(GLenum target, GLenum pname, GLuint *params)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLExtraFunctions::glGetTexParameterIuiv` 用于执行与“gl、Get、Tex、Parameter、Iuiv”相关的操作。调用时要先确认当前状态和 `target`、`pname`、`params` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `target`：类型为 `GLenum`。没有默认值，调用时必须提供。目标对象、目标属性或目标资源。要确认它在操作期间仍然有效，并支持所需能力。
- 参数 `pname`：类型为 `GLenum`。没有默认值，调用时必须提供。枚举或标志参数。先确认可用枚举值、互斥关系和默认值，必要时用按位或组合标志。
- 参数 `params`：类型为 `GLuint *`。没有默认值，调用时必须提供。传入 `GLuint *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLExtraFunctions::glGetTransformFeedbackVarying(GLuint program, GLuint index, GLsizei bufSize, GLsizei *length, GLsizei *size, GLenum *type, GLchar *name)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLExtraFunctions::glGetTransformFeedbackVarying` 用于执行与“gl、Get、Transform、Feedback、Varying”相关的操作。调用时要先确认当前状态和 `program`、`index`、`bufSize`、`length`、`size`、`type`、`name` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `program`：类型为 `GLuint`。没有默认值，调用时必须提供。传入 `GLuint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `index`：类型为 `GLuint`。没有默认值，调用时必须提供。项目或数据索引。先确认索引基于 0 还是 1、是否允许越界/负数，以及调用后索引是否仍然有效。
- 参数 `bufSize`：类型为 `GLsizei`。没有默认值，调用时必须提供。传入 `GLsizei` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `length`：类型为 `GLsizei *`。没有默认值，调用时必须提供。传入 `GLsizei *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `size`：类型为 `GLsizei *`。没有默认值，调用时必须提供。尺寸或长度，单位通常是像素、字节、元素数或时间，必须结合类型和类的上下文确认。
- 参数 `type`：类型为 `GLenum *`。没有默认值，调用时必须提供。类型、格式或策略枚举。要确认枚举值的适用范围和平台支持情况。
- 参数 `name`：类型为 `GLchar *`。没有默认值，调用时必须提供。名称或键。通常是稳定的 API/配置标识，不应随意使用显示文本替代。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `GLuint QOpenGLExtraFunctions::glGetUniformBlockIndex(GLuint program, const GLchar *uniformBlockName)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLExtraFunctions::glGetUniformBlockIndex` 用于计算、查询或取得与“gl、Get、Uniform、阻塞或屏蔽、索引”相关的操作。调用时要先确认当前状态和 `program`、`uniformBlockName` 的有效范围；返回类型是 `GLuint`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`GLuint`。
- 参数 `program`：类型为 `GLuint`。没有默认值，调用时必须提供。传入 `GLuint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `uniformBlockName`：类型为 `const GLchar *`。没有默认值，调用时必须提供。传入 `const GLchar *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLExtraFunctions::glGetUniformIndices(GLuint program, GLsizei uniformCount, const GLchar *const *uniformNames, GLuint *uniformIndices)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLExtraFunctions::glGetUniformIndices` 用于执行与“gl、Get、Uniform、Indices”相关的操作。调用时要先确认当前状态和 `program`、`uniformCount`、`uniformNames`、`uniformIndices` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `program`：类型为 `GLuint`。没有默认值，调用时必须提供。传入 `GLuint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `uniformCount`：类型为 `GLsizei`。没有默认值，调用时必须提供。传入 `GLsizei` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `uniformNames`：类型为 `const GLchar *const *`。没有默认值，调用时必须提供。传入 `const GLchar *const *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `uniformIndices`：类型为 `GLuint *`。没有默认值，调用时必须提供。传入 `GLuint *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLExtraFunctions::glGetUniformuiv(GLuint program, GLint location, GLuint *params)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLExtraFunctions::glGetUniformuiv` 用于执行与“gl、Get、Uniformuiv”相关的操作。调用时要先确认当前状态和 `program`、`location`、`params` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `program`：类型为 `GLuint`。没有默认值，调用时必须提供。传入 `GLuint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `location`：类型为 `GLint`。没有默认值，调用时必须提供。传入 `GLint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `params`：类型为 `GLuint *`。没有默认值，调用时必须提供。传入 `GLuint *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLExtraFunctions::glGetVertexAttribIiv(GLuint index, GLenum pname, GLint *params)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLExtraFunctions::glGetVertexAttribIiv` 用于执行与“gl、Get、Vertex、Attrib、Iiv”相关的操作。调用时要先确认当前状态和 `index`、`pname`、`params` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `index`：类型为 `GLuint`。没有默认值，调用时必须提供。项目或数据索引。先确认索引基于 0 还是 1、是否允许越界/负数，以及调用后索引是否仍然有效。
- 参数 `pname`：类型为 `GLenum`。没有默认值，调用时必须提供。枚举或标志参数。先确认可用枚举值、互斥关系和默认值，必要时用按位或组合标志。
- 参数 `params`：类型为 `GLint *`。没有默认值，调用时必须提供。传入 `GLint *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLExtraFunctions::glGetVertexAttribIuiv(GLuint index, GLenum pname, GLuint *params)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLExtraFunctions::glGetVertexAttribIuiv` 用于执行与“gl、Get、Vertex、Attrib、Iuiv”相关的操作。调用时要先确认当前状态和 `index`、`pname`、`params` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `index`：类型为 `GLuint`。没有默认值，调用时必须提供。项目或数据索引。先确认索引基于 0 还是 1、是否允许越界/负数，以及调用后索引是否仍然有效。
- 参数 `pname`：类型为 `GLenum`。没有默认值，调用时必须提供。枚举或标志参数。先确认可用枚举值、互斥关系和默认值，必要时用按位或组合标志。
- 参数 `params`：类型为 `GLuint *`。没有默认值，调用时必须提供。传入 `GLuint *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLExtraFunctions::glGetnUniformfv(GLuint program, GLint location, GLsizei bufSize, GLfloat *params)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLExtraFunctions::glGetnUniformfv` 用于执行与“gl、Getn、Uniformfv”相关的操作。调用时要先确认当前状态和 `program`、`location`、`bufSize`、`params` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `program`：类型为 `GLuint`。没有默认值，调用时必须提供。传入 `GLuint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `location`：类型为 `GLint`。没有默认值，调用时必须提供。传入 `GLint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `bufSize`：类型为 `GLsizei`。没有默认值，调用时必须提供。传入 `GLsizei` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `params`：类型为 `GLfloat *`。没有默认值，调用时必须提供。传入 `GLfloat *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLExtraFunctions::glGetnUniformiv(GLuint program, GLint location, GLsizei bufSize, GLint *params)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLExtraFunctions::glGetnUniformiv` 用于执行与“gl、Getn、Uniformiv”相关的操作。调用时要先确认当前状态和 `program`、`location`、`bufSize`、`params` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `program`：类型为 `GLuint`。没有默认值，调用时必须提供。传入 `GLuint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `location`：类型为 `GLint`。没有默认值，调用时必须提供。传入 `GLint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `bufSize`：类型为 `GLsizei`。没有默认值，调用时必须提供。传入 `GLsizei` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `params`：类型为 `GLint *`。没有默认值，调用时必须提供。传入 `GLint *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLExtraFunctions::glGetnUniformuiv(GLuint program, GLint location, GLsizei bufSize, GLuint *params)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLExtraFunctions::glGetnUniformuiv` 用于执行与“gl、Getn、Uniformuiv”相关的操作。调用时要先确认当前状态和 `program`、`location`、`bufSize`、`params` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `program`：类型为 `GLuint`。没有默认值，调用时必须提供。传入 `GLuint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `location`：类型为 `GLint`。没有默认值，调用时必须提供。传入 `GLint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `bufSize`：类型为 `GLsizei`。没有默认值，调用时必须提供。传入 `GLsizei` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `params`：类型为 `GLuint *`。没有默认值，调用时必须提供。传入 `GLuint *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLExtraFunctions::glInvalidateFramebuffer(GLenum target, GLsizei numAttachments, const GLenum *attachments)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLExtraFunctions::glInvalidateFramebuffer` 用于执行与“gl、Invalidate、Framebuffer”相关的操作。调用时要先确认当前状态和 `target`、`numAttachments`、`attachments` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `target`：类型为 `GLenum`。没有默认值，调用时必须提供。目标对象、目标属性或目标资源。要确认它在操作期间仍然有效，并支持所需能力。
- 参数 `numAttachments`：类型为 `GLsizei`。没有默认值，调用时必须提供。传入 `GLsizei` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `attachments`：类型为 `const GLenum *`。没有默认值，调用时必须提供。枚举或标志参数。先确认可用枚举值、互斥关系和默认值，必要时用按位或组合标志。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLExtraFunctions::glInvalidateSubFramebuffer(GLenum target, GLsizei numAttachments, const GLenum *attachments, GLint x, GLint y, GLsizei width, GLsizei height)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLExtraFunctions::glInvalidateSubFramebuffer` 用于执行与“gl、Invalidate、Sub、Framebuffer”相关的操作。调用时要先确认当前状态和 `target`、`numAttachments`、`attachments`、`x`、`y`、`width`、`height` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `target`：类型为 `GLenum`。没有默认值，调用时必须提供。目标对象、目标属性或目标资源。要确认它在操作期间仍然有效，并支持所需能力。
- 参数 `numAttachments`：类型为 `GLsizei`。没有默认值，调用时必须提供。传入 `GLsizei` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `attachments`：类型为 `const GLenum *`。没有默认值，调用时必须提供。枚举或标志参数。先确认可用枚举值、互斥关系和默认值，必要时用按位或组合标志。
- 参数 `x`：类型为 `GLint`。没有默认值，调用时必须提供。传入 `GLint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `y`：类型为 `GLint`。没有默认值，调用时必须提供。传入 `GLint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `width`：类型为 `GLsizei`。没有默认值，调用时必须提供。宽度，通常以像素、字符数或元素数量表示；要确认是否允许 0、负数和超出最大值。
- 参数 `height`：类型为 `GLsizei`。没有默认值，调用时必须提供。高度，通常以像素、字符数或元素数量表示；要确认是否允许 0、负数和超出最大值。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `GLboolean QOpenGLExtraFunctions::glIsEnabledi(GLenum target, GLuint index)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLExtraFunctions::glIsEnabledi` 用于计算、查询或取得与“gl、状态判断、Enabledi”相关的操作。调用时要先确认当前状态和 `target`、`index` 的有效范围；返回类型是 `GLboolean`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`GLboolean`。
- 参数 `target`：类型为 `GLenum`。没有默认值，调用时必须提供。目标对象、目标属性或目标资源。要确认它在操作期间仍然有效，并支持所需能力。
- 参数 `index`：类型为 `GLuint`。没有默认值，调用时必须提供。项目或数据索引。先确认索引基于 0 还是 1、是否允许越界/负数，以及调用后索引是否仍然有效。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `GLboolean QOpenGLExtraFunctions::glIsProgramPipeline(GLuint pipeline)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLExtraFunctions::glIsProgramPipeline` 用于计算、查询或取得与“gl、状态判断、Program、Pipeline”相关的操作。调用时要先确认当前状态和 `pipeline` 的有效范围；返回类型是 `GLboolean`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`GLboolean`。
- 参数 `pipeline`：类型为 `GLuint`。没有默认值，调用时必须提供。传入 `GLuint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `GLboolean QOpenGLExtraFunctions::glIsQuery(GLuint id)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLExtraFunctions::glIsQuery` 用于计算、查询或取得与“gl、状态判断、查询”相关的操作。调用时要先确认当前状态和 `id` 的有效范围；返回类型是 `GLboolean`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`GLboolean`。
- 参数 `id`：类型为 `GLuint`。没有默认值，调用时必须提供。传入 `GLuint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `GLboolean QOpenGLExtraFunctions::glIsSampler(GLuint sampler)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLExtraFunctions::glIsSampler` 用于计算、查询或取得与“gl、状态判断、Sampler”相关的操作。调用时要先确认当前状态和 `sampler` 的有效范围；返回类型是 `GLboolean`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`GLboolean`。
- 参数 `sampler`：类型为 `GLuint`。没有默认值，调用时必须提供。传入 `GLuint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `GLboolean QOpenGLExtraFunctions::glIsSync(GLsync sync)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLExtraFunctions::glIsSync` 用于计算、查询或取得与“gl、状态判断、Sync”相关的操作。调用时要先确认当前状态和 `sync` 的有效范围；返回类型是 `GLboolean`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`GLboolean`。
- 参数 `sync`：类型为 `GLsync`。没有默认值，调用时必须提供。传入 `GLsync` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `GLboolean QOpenGLExtraFunctions::glIsTransformFeedback(GLuint id)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLExtraFunctions::glIsTransformFeedback` 用于计算、查询或取得与“gl、状态判断、Transform、Feedback”相关的操作。调用时要先确认当前状态和 `id` 的有效范围；返回类型是 `GLboolean`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`GLboolean`。
- 参数 `id`：类型为 `GLuint`。没有默认值，调用时必须提供。传入 `GLuint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `GLboolean QOpenGLExtraFunctions::glIsVertexArray(GLuint array)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLExtraFunctions::glIsVertexArray` 用于计算、查询或取得与“gl、状态判断、Vertex、Array”相关的操作。调用时要先确认当前状态和 `array` 的有效范围；返回类型是 `GLboolean`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`GLboolean`。
- 参数 `array`：类型为 `GLuint`。没有默认值，调用时必须提供。传入 `GLuint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void *QOpenGLExtraFunctions::glMapBufferRange(GLenum target, GLintptr offset, GLsizeiptr length, GLbitfield access)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLExtraFunctions::glMapBufferRange` 用于计算、查询或取得与“gl、映射、Buffer、Range”相关的操作。调用时要先确认当前状态和 `target`、`offset`、`length`、`access` 的有效范围；返回类型是 `void *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void *`。
- 参数 `target`：类型为 `GLenum`。没有默认值，调用时必须提供。目标对象、目标属性或目标资源。要确认它在操作期间仍然有效，并支持所需能力。
- 参数 `offset`：类型为 `GLintptr`。没有默认值，调用时必须提供。传入 `GLintptr` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `length`：类型为 `GLsizeiptr`。没有默认值，调用时必须提供。传入 `GLsizeiptr` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `access`：类型为 `GLbitfield`。没有默认值，调用时必须提供。传入 `GLbitfield` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLExtraFunctions::glMemoryBarrier(GLbitfield barriers)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLExtraFunctions::glMemoryBarrier` 用于执行与“gl、Memory、Barrier”相关的操作。调用时要先确认当前状态和 `barriers` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `barriers`：类型为 `GLbitfield`。没有默认值，调用时必须提供。传入 `GLbitfield` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLExtraFunctions::glMemoryBarrierByRegion(GLbitfield barriers)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLExtraFunctions::glMemoryBarrierByRegion` 用于执行与“gl、Memory、Barrier、By、Region”相关的操作。调用时要先确认当前状态和 `barriers` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `barriers`：类型为 `GLbitfield`。没有默认值，调用时必须提供。传入 `GLbitfield` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLExtraFunctions::glMinSampleShading(GLfloat value)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLExtraFunctions::glMinSampleShading` 用于执行与“gl、Min、Sample、Shading”相关的操作。调用时要先确认当前状态和 `value` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `value`：类型为 `GLfloat`。没有默认值，调用时必须提供。要读取或写入的值。要确认类型转换、默认值、所有权以及写入后是否触发通知。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLExtraFunctions::glObjectLabel(GLenum identifier, GLuint name, GLsizei length, const GLchar *label)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLExtraFunctions::glObjectLabel` 用于执行与“gl、Object、Label”相关的操作。调用时要先确认当前状态和 `identifier`、`name`、`length`、`label` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `identifier`：类型为 `GLenum`。没有默认值，调用时必须提供。枚举或标志参数。先确认可用枚举值、互斥关系和默认值，必要时用按位或组合标志。
- 参数 `name`：类型为 `GLuint`。没有默认值，调用时必须提供。名称或键。通常是稳定的 API/配置标识，不应随意使用显示文本替代。
- 参数 `length`：类型为 `GLsizei`。没有默认值，调用时必须提供。传入 `GLsizei` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `label`：类型为 `const GLchar *`。没有默认值，调用时必须提供。传入 `const GLchar *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLExtraFunctions::glObjectPtrLabel(const void *ptr, GLsizei length, const GLchar *label)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLExtraFunctions::glObjectPtrLabel` 用于执行与“gl、Object、Ptr、Label”相关的操作。调用时要先确认当前状态和 `ptr`、`length`、`label` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `ptr`：类型为 `const void *`。没有默认值，调用时必须提供。传入 `const void *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `length`：类型为 `GLsizei`。没有默认值，调用时必须提供。传入 `GLsizei` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `label`：类型为 `const GLchar *`。没有默认值，调用时必须提供。传入 `const GLchar *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLExtraFunctions::glPatchParameteri(GLenum pname, GLint value)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLExtraFunctions::glPatchParameteri` 用于执行与“gl、Patch、Parameteri”相关的操作。调用时要先确认当前状态和 `pname`、`value` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `pname`：类型为 `GLenum`。没有默认值，调用时必须提供。枚举或标志参数。先确认可用枚举值、互斥关系和默认值，必要时用按位或组合标志。
- 参数 `value`：类型为 `GLint`。没有默认值，调用时必须提供。要读取或写入的值。要确认类型转换、默认值、所有权以及写入后是否触发通知。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLExtraFunctions::glPauseTransformFeedback()`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLExtraFunctions::glPauseTransformFeedback` 用于执行与“gl、暂停、Transform、Feedback”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLExtraFunctions::glPopDebugGroup()`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLExtraFunctions::glPopDebugGroup` 用于执行与“gl、Pop、调试输出、Group”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLExtraFunctions::glPrimitiveBoundingBox(GLfloat minX, GLfloat minY, GLfloat minZ, GLfloat minW, GLfloat maxX, GLfloat maxY, GLfloat maxZ, GLfloat maxW)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLExtraFunctions::glPrimitiveBoundingBox` 用于执行与“gl、Primitive、Bounding、Box”相关的操作。调用时要先确认当前状态和 `minX`、`minY`、`minZ`、`minW`、`maxX`、`maxY`、`maxZ`、`maxW` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `minX`：类型为 `GLfloat`。没有默认值，调用时必须提供。传入 `GLfloat` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `minY`：类型为 `GLfloat`。没有默认值，调用时必须提供。传入 `GLfloat` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `minZ`：类型为 `GLfloat`。没有默认值，调用时必须提供。传入 `GLfloat` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `minW`：类型为 `GLfloat`。没有默认值，调用时必须提供。传入 `GLfloat` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `maxX`：类型为 `GLfloat`。没有默认值，调用时必须提供。传入 `GLfloat` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `maxY`：类型为 `GLfloat`。没有默认值，调用时必须提供。传入 `GLfloat` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `maxZ`：类型为 `GLfloat`。没有默认值，调用时必须提供。传入 `GLfloat` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `maxW`：类型为 `GLfloat`。没有默认值，调用时必须提供。传入 `GLfloat` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLExtraFunctions::glProgramBinary(GLuint program, GLenum binaryFormat, const void *binary, GLsizei length)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLExtraFunctions::glProgramBinary` 用于执行与“gl、Program、Binary”相关的操作。调用时要先确认当前状态和 `program`、`binaryFormat`、`binary`、`length` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `program`：类型为 `GLuint`。没有默认值，调用时必须提供。传入 `GLuint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `binaryFormat`：类型为 `GLenum`。没有默认值，调用时必须提供。枚举或标志参数。先确认可用枚举值、互斥关系和默认值，必要时用按位或组合标志。
- 参数 `binary`：类型为 `const void *`。没有默认值，调用时必须提供。传入 `const void *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `length`：类型为 `GLsizei`。没有默认值，调用时必须提供。传入 `GLsizei` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLExtraFunctions::glProgramParameteri(GLuint program, GLenum pname, GLint value)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLExtraFunctions::glProgramParameteri` 用于执行与“gl、Program、Parameteri”相关的操作。调用时要先确认当前状态和 `program`、`pname`、`value` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `program`：类型为 `GLuint`。没有默认值，调用时必须提供。传入 `GLuint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `pname`：类型为 `GLenum`。没有默认值，调用时必须提供。枚举或标志参数。先确认可用枚举值、互斥关系和默认值，必要时用按位或组合标志。
- 参数 `value`：类型为 `GLint`。没有默认值，调用时必须提供。要读取或写入的值。要确认类型转换、默认值、所有权以及写入后是否触发通知。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLExtraFunctions::glProgramUniform1f(GLuint program, GLint location, GLfloat v0)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLExtraFunctions::glProgramUniform1f` 用于执行与“gl、Program、Uniform、1、f”相关的操作。调用时要先确认当前状态和 `program`、`location`、`v0` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `program`：类型为 `GLuint`。没有默认值，调用时必须提供。传入 `GLuint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `location`：类型为 `GLint`。没有默认值，调用时必须提供。传入 `GLint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `v0`：类型为 `GLfloat`。没有默认值，调用时必须提供。传入 `GLfloat` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLExtraFunctions::glProgramUniform1fv(GLuint program, GLint location, GLsizei count, const GLfloat *value)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLExtraFunctions::glProgramUniform1fv` 用于执行与“gl、Program、Uniform、1、fv”相关的操作。调用时要先确认当前状态和 `program`、`location`、`count`、`value` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `program`：类型为 `GLuint`。没有默认值，调用时必须提供。传入 `GLuint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `location`：类型为 `GLint`。没有默认值，调用时必须提供。传入 `GLint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `count`：类型为 `GLsizei`。没有默认值，调用时必须提供。传入 `GLsizei` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `value`：类型为 `const GLfloat *`。没有默认值，调用时必须提供。要读取或写入的值。要确认类型转换、默认值、所有权以及写入后是否触发通知。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLExtraFunctions::glProgramUniform1i(GLuint program, GLint location, GLint v0)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLExtraFunctions::glProgramUniform1i` 用于执行与“gl、Program、Uniform、1、i”相关的操作。调用时要先确认当前状态和 `program`、`location`、`v0` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `program`：类型为 `GLuint`。没有默认值，调用时必须提供。传入 `GLuint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `location`：类型为 `GLint`。没有默认值，调用时必须提供。传入 `GLint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `v0`：类型为 `GLint`。没有默认值，调用时必须提供。传入 `GLint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLExtraFunctions::glProgramUniform1iv(GLuint program, GLint location, GLsizei count, const GLint *value)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLExtraFunctions::glProgramUniform1iv` 用于执行与“gl、Program、Uniform、1、iv”相关的操作。调用时要先确认当前状态和 `program`、`location`、`count`、`value` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `program`：类型为 `GLuint`。没有默认值，调用时必须提供。传入 `GLuint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `location`：类型为 `GLint`。没有默认值，调用时必须提供。传入 `GLint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `count`：类型为 `GLsizei`。没有默认值，调用时必须提供。传入 `GLsizei` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `value`：类型为 `const GLint *`。没有默认值，调用时必须提供。要读取或写入的值。要确认类型转换、默认值、所有权以及写入后是否触发通知。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLExtraFunctions::glProgramUniform1ui(GLuint program, GLint location, GLuint v0)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLExtraFunctions::glProgramUniform1ui` 用于执行与“gl、Program、Uniform、1、ui”相关的操作。调用时要先确认当前状态和 `program`、`location`、`v0` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `program`：类型为 `GLuint`。没有默认值，调用时必须提供。传入 `GLuint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `location`：类型为 `GLint`。没有默认值，调用时必须提供。传入 `GLint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `v0`：类型为 `GLuint`。没有默认值，调用时必须提供。传入 `GLuint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLExtraFunctions::glProgramUniform1uiv(GLuint program, GLint location, GLsizei count, const GLuint *value)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLExtraFunctions::glProgramUniform1uiv` 用于执行与“gl、Program、Uniform、1、uiv”相关的操作。调用时要先确认当前状态和 `program`、`location`、`count`、`value` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `program`：类型为 `GLuint`。没有默认值，调用时必须提供。传入 `GLuint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `location`：类型为 `GLint`。没有默认值，调用时必须提供。传入 `GLint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `count`：类型为 `GLsizei`。没有默认值，调用时必须提供。传入 `GLsizei` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `value`：类型为 `const GLuint *`。没有默认值，调用时必须提供。要读取或写入的值。要确认类型转换、默认值、所有权以及写入后是否触发通知。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLExtraFunctions::glProgramUniform2f(GLuint program, GLint location, GLfloat v0, GLfloat v1)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLExtraFunctions::glProgramUniform2f` 用于执行与“gl、Program、Uniform、2、f”相关的操作。调用时要先确认当前状态和 `program`、`location`、`v0`、`v1` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `program`：类型为 `GLuint`。没有默认值，调用时必须提供。传入 `GLuint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `location`：类型为 `GLint`。没有默认值，调用时必须提供。传入 `GLint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `v0`：类型为 `GLfloat`。没有默认值，调用时必须提供。传入 `GLfloat` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `v1`：类型为 `GLfloat`。没有默认值，调用时必须提供。传入 `GLfloat` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLExtraFunctions::glProgramUniform2fv(GLuint program, GLint location, GLsizei count, const GLfloat *value)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLExtraFunctions::glProgramUniform2fv` 用于执行与“gl、Program、Uniform、2、fv”相关的操作。调用时要先确认当前状态和 `program`、`location`、`count`、`value` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `program`：类型为 `GLuint`。没有默认值，调用时必须提供。传入 `GLuint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `location`：类型为 `GLint`。没有默认值，调用时必须提供。传入 `GLint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `count`：类型为 `GLsizei`。没有默认值，调用时必须提供。传入 `GLsizei` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `value`：类型为 `const GLfloat *`。没有默认值，调用时必须提供。要读取或写入的值。要确认类型转换、默认值、所有权以及写入后是否触发通知。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLExtraFunctions::glProgramUniform2i(GLuint program, GLint location, GLint v0, GLint v1)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLExtraFunctions::glProgramUniform2i` 用于执行与“gl、Program、Uniform、2、i”相关的操作。调用时要先确认当前状态和 `program`、`location`、`v0`、`v1` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `program`：类型为 `GLuint`。没有默认值，调用时必须提供。传入 `GLuint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `location`：类型为 `GLint`。没有默认值，调用时必须提供。传入 `GLint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `v0`：类型为 `GLint`。没有默认值，调用时必须提供。传入 `GLint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `v1`：类型为 `GLint`。没有默认值，调用时必须提供。传入 `GLint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLExtraFunctions::glProgramUniform2iv(GLuint program, GLint location, GLsizei count, const GLint *value)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLExtraFunctions::glProgramUniform2iv` 用于执行与“gl、Program、Uniform、2、iv”相关的操作。调用时要先确认当前状态和 `program`、`location`、`count`、`value` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `program`：类型为 `GLuint`。没有默认值，调用时必须提供。传入 `GLuint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `location`：类型为 `GLint`。没有默认值，调用时必须提供。传入 `GLint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `count`：类型为 `GLsizei`。没有默认值，调用时必须提供。传入 `GLsizei` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `value`：类型为 `const GLint *`。没有默认值，调用时必须提供。要读取或写入的值。要确认类型转换、默认值、所有权以及写入后是否触发通知。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLExtraFunctions::glProgramUniform2ui(GLuint program, GLint location, GLuint v0, GLuint v1)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLExtraFunctions::glProgramUniform2ui` 用于执行与“gl、Program、Uniform、2、ui”相关的操作。调用时要先确认当前状态和 `program`、`location`、`v0`、`v1` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `program`：类型为 `GLuint`。没有默认值，调用时必须提供。传入 `GLuint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `location`：类型为 `GLint`。没有默认值，调用时必须提供。传入 `GLint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `v0`：类型为 `GLuint`。没有默认值，调用时必须提供。传入 `GLuint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `v1`：类型为 `GLuint`。没有默认值，调用时必须提供。传入 `GLuint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLExtraFunctions::glProgramUniform2uiv(GLuint program, GLint location, GLsizei count, const GLuint *value)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLExtraFunctions::glProgramUniform2uiv` 用于执行与“gl、Program、Uniform、2、uiv”相关的操作。调用时要先确认当前状态和 `program`、`location`、`count`、`value` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `program`：类型为 `GLuint`。没有默认值，调用时必须提供。传入 `GLuint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `location`：类型为 `GLint`。没有默认值，调用时必须提供。传入 `GLint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `count`：类型为 `GLsizei`。没有默认值，调用时必须提供。传入 `GLsizei` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `value`：类型为 `const GLuint *`。没有默认值，调用时必须提供。要读取或写入的值。要确认类型转换、默认值、所有权以及写入后是否触发通知。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLExtraFunctions::glProgramUniform3f(GLuint program, GLint location, GLfloat v0, GLfloat v1, GLfloat v2)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLExtraFunctions::glProgramUniform3f` 用于执行与“gl、Program、Uniform、3、f”相关的操作。调用时要先确认当前状态和 `program`、`location`、`v0`、`v1`、`v2` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `program`：类型为 `GLuint`。没有默认值，调用时必须提供。传入 `GLuint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `location`：类型为 `GLint`。没有默认值，调用时必须提供。传入 `GLint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `v0`：类型为 `GLfloat`。没有默认值，调用时必须提供。传入 `GLfloat` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `v1`：类型为 `GLfloat`。没有默认值，调用时必须提供。传入 `GLfloat` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `v2`：类型为 `GLfloat`。没有默认值，调用时必须提供。传入 `GLfloat` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLExtraFunctions::glProgramUniform3fv(GLuint program, GLint location, GLsizei count, const GLfloat *value)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLExtraFunctions::glProgramUniform3fv` 用于执行与“gl、Program、Uniform、3、fv”相关的操作。调用时要先确认当前状态和 `program`、`location`、`count`、`value` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `program`：类型为 `GLuint`。没有默认值，调用时必须提供。传入 `GLuint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `location`：类型为 `GLint`。没有默认值，调用时必须提供。传入 `GLint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `count`：类型为 `GLsizei`。没有默认值，调用时必须提供。传入 `GLsizei` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `value`：类型为 `const GLfloat *`。没有默认值，调用时必须提供。要读取或写入的值。要确认类型转换、默认值、所有权以及写入后是否触发通知。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLExtraFunctions::glProgramUniform3i(GLuint program, GLint location, GLint v0, GLint v1, GLint v2)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLExtraFunctions::glProgramUniform3i` 用于执行与“gl、Program、Uniform、3、i”相关的操作。调用时要先确认当前状态和 `program`、`location`、`v0`、`v1`、`v2` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `program`：类型为 `GLuint`。没有默认值，调用时必须提供。传入 `GLuint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `location`：类型为 `GLint`。没有默认值，调用时必须提供。传入 `GLint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `v0`：类型为 `GLint`。没有默认值，调用时必须提供。传入 `GLint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `v1`：类型为 `GLint`。没有默认值，调用时必须提供。传入 `GLint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `v2`：类型为 `GLint`。没有默认值，调用时必须提供。传入 `GLint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLExtraFunctions::glProgramUniform3iv(GLuint program, GLint location, GLsizei count, const GLint *value)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLExtraFunctions::glProgramUniform3iv` 用于执行与“gl、Program、Uniform、3、iv”相关的操作。调用时要先确认当前状态和 `program`、`location`、`count`、`value` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `program`：类型为 `GLuint`。没有默认值，调用时必须提供。传入 `GLuint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `location`：类型为 `GLint`。没有默认值，调用时必须提供。传入 `GLint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `count`：类型为 `GLsizei`。没有默认值，调用时必须提供。传入 `GLsizei` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `value`：类型为 `const GLint *`。没有默认值，调用时必须提供。要读取或写入的值。要确认类型转换、默认值、所有权以及写入后是否触发通知。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLExtraFunctions::glProgramUniform3ui(GLuint program, GLint location, GLuint v0, GLuint v1, GLuint v2)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLExtraFunctions::glProgramUniform3ui` 用于执行与“gl、Program、Uniform、3、ui”相关的操作。调用时要先确认当前状态和 `program`、`location`、`v0`、`v1`、`v2` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `program`：类型为 `GLuint`。没有默认值，调用时必须提供。传入 `GLuint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `location`：类型为 `GLint`。没有默认值，调用时必须提供。传入 `GLint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `v0`：类型为 `GLuint`。没有默认值，调用时必须提供。传入 `GLuint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `v1`：类型为 `GLuint`。没有默认值，调用时必须提供。传入 `GLuint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `v2`：类型为 `GLuint`。没有默认值，调用时必须提供。传入 `GLuint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLExtraFunctions::glProgramUniform3uiv(GLuint program, GLint location, GLsizei count, const GLuint *value)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLExtraFunctions::glProgramUniform3uiv` 用于执行与“gl、Program、Uniform、3、uiv”相关的操作。调用时要先确认当前状态和 `program`、`location`、`count`、`value` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `program`：类型为 `GLuint`。没有默认值，调用时必须提供。传入 `GLuint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `location`：类型为 `GLint`。没有默认值，调用时必须提供。传入 `GLint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `count`：类型为 `GLsizei`。没有默认值，调用时必须提供。传入 `GLsizei` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `value`：类型为 `const GLuint *`。没有默认值，调用时必须提供。要读取或写入的值。要确认类型转换、默认值、所有权以及写入后是否触发通知。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLExtraFunctions::glProgramUniform4f(GLuint program, GLint location, GLfloat v0, GLfloat v1, GLfloat v2, GLfloat v3)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLExtraFunctions::glProgramUniform4f` 用于执行与“gl、Program、Uniform、4、f”相关的操作。调用时要先确认当前状态和 `program`、`location`、`v0`、`v1`、`v2`、`v3` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `program`：类型为 `GLuint`。没有默认值，调用时必须提供。传入 `GLuint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `location`：类型为 `GLint`。没有默认值，调用时必须提供。传入 `GLint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `v0`：类型为 `GLfloat`。没有默认值，调用时必须提供。传入 `GLfloat` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `v1`：类型为 `GLfloat`。没有默认值，调用时必须提供。传入 `GLfloat` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `v2`：类型为 `GLfloat`。没有默认值，调用时必须提供。传入 `GLfloat` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `v3`：类型为 `GLfloat`。没有默认值，调用时必须提供。传入 `GLfloat` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLExtraFunctions::glProgramUniform4fv(GLuint program, GLint location, GLsizei count, const GLfloat *value)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLExtraFunctions::glProgramUniform4fv` 用于执行与“gl、Program、Uniform、4、fv”相关的操作。调用时要先确认当前状态和 `program`、`location`、`count`、`value` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `program`：类型为 `GLuint`。没有默认值，调用时必须提供。传入 `GLuint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `location`：类型为 `GLint`。没有默认值，调用时必须提供。传入 `GLint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `count`：类型为 `GLsizei`。没有默认值，调用时必须提供。传入 `GLsizei` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `value`：类型为 `const GLfloat *`。没有默认值，调用时必须提供。要读取或写入的值。要确认类型转换、默认值、所有权以及写入后是否触发通知。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLExtraFunctions::glProgramUniform4i(GLuint program, GLint location, GLint v0, GLint v1, GLint v2, GLint v3)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLExtraFunctions::glProgramUniform4i` 用于执行与“gl、Program、Uniform、4、i”相关的操作。调用时要先确认当前状态和 `program`、`location`、`v0`、`v1`、`v2`、`v3` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `program`：类型为 `GLuint`。没有默认值，调用时必须提供。传入 `GLuint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `location`：类型为 `GLint`。没有默认值，调用时必须提供。传入 `GLint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `v0`：类型为 `GLint`。没有默认值，调用时必须提供。传入 `GLint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `v1`：类型为 `GLint`。没有默认值，调用时必须提供。传入 `GLint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `v2`：类型为 `GLint`。没有默认值，调用时必须提供。传入 `GLint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `v3`：类型为 `GLint`。没有默认值，调用时必须提供。传入 `GLint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLExtraFunctions::glProgramUniform4iv(GLuint program, GLint location, GLsizei count, const GLint *value)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLExtraFunctions::glProgramUniform4iv` 用于执行与“gl、Program、Uniform、4、iv”相关的操作。调用时要先确认当前状态和 `program`、`location`、`count`、`value` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `program`：类型为 `GLuint`。没有默认值，调用时必须提供。传入 `GLuint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `location`：类型为 `GLint`。没有默认值，调用时必须提供。传入 `GLint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `count`：类型为 `GLsizei`。没有默认值，调用时必须提供。传入 `GLsizei` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `value`：类型为 `const GLint *`。没有默认值，调用时必须提供。要读取或写入的值。要确认类型转换、默认值、所有权以及写入后是否触发通知。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLExtraFunctions::glProgramUniform4ui(GLuint program, GLint location, GLuint v0, GLuint v1, GLuint v2, GLuint v3)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLExtraFunctions::glProgramUniform4ui` 用于执行与“gl、Program、Uniform、4、ui”相关的操作。调用时要先确认当前状态和 `program`、`location`、`v0`、`v1`、`v2`、`v3` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `program`：类型为 `GLuint`。没有默认值，调用时必须提供。传入 `GLuint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `location`：类型为 `GLint`。没有默认值，调用时必须提供。传入 `GLint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `v0`：类型为 `GLuint`。没有默认值，调用时必须提供。传入 `GLuint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `v1`：类型为 `GLuint`。没有默认值，调用时必须提供。传入 `GLuint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `v2`：类型为 `GLuint`。没有默认值，调用时必须提供。传入 `GLuint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `v3`：类型为 `GLuint`。没有默认值，调用时必须提供。传入 `GLuint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLExtraFunctions::glProgramUniform4uiv(GLuint program, GLint location, GLsizei count, const GLuint *value)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLExtraFunctions::glProgramUniform4uiv` 用于执行与“gl、Program、Uniform、4、uiv”相关的操作。调用时要先确认当前状态和 `program`、`location`、`count`、`value` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `program`：类型为 `GLuint`。没有默认值，调用时必须提供。传入 `GLuint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `location`：类型为 `GLint`。没有默认值，调用时必须提供。传入 `GLint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `count`：类型为 `GLsizei`。没有默认值，调用时必须提供。传入 `GLsizei` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `value`：类型为 `const GLuint *`。没有默认值，调用时必须提供。要读取或写入的值。要确认类型转换、默认值、所有权以及写入后是否触发通知。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLExtraFunctions::glProgramUniformMatrix2fv(GLuint program, GLint location, GLsizei count, GLboolean transpose, const GLfloat *value)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLExtraFunctions::glProgramUniformMatrix2fv` 用于执行与“gl、Program、Uniform、Matrix、2、fv”相关的操作。调用时要先确认当前状态和 `program`、`location`、`count`、`transpose`、`value` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `program`：类型为 `GLuint`。没有默认值，调用时必须提供。传入 `GLuint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `location`：类型为 `GLint`。没有默认值，调用时必须提供。传入 `GLint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `count`：类型为 `GLsizei`。没有默认值，调用时必须提供。传入 `GLsizei` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `transpose`：类型为 `GLboolean`。没有默认值，调用时必须提供。传入 `GLboolean` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `value`：类型为 `const GLfloat *`。没有默认值，调用时必须提供。要读取或写入的值。要确认类型转换、默认值、所有权以及写入后是否触发通知。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLExtraFunctions::glProgramUniformMatrix2x3fv(GLuint program, GLint location, GLsizei count, GLboolean transpose, const GLfloat *value)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLExtraFunctions::glProgramUniformMatrix2x3fv` 用于执行与“gl、Program、Uniform、Matrix、2、x、3、fv”相关的操作。调用时要先确认当前状态和 `program`、`location`、`count`、`transpose`、`value` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `program`：类型为 `GLuint`。没有默认值，调用时必须提供。传入 `GLuint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `location`：类型为 `GLint`。没有默认值，调用时必须提供。传入 `GLint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `count`：类型为 `GLsizei`。没有默认值，调用时必须提供。传入 `GLsizei` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `transpose`：类型为 `GLboolean`。没有默认值，调用时必须提供。传入 `GLboolean` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `value`：类型为 `const GLfloat *`。没有默认值，调用时必须提供。要读取或写入的值。要确认类型转换、默认值、所有权以及写入后是否触发通知。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLExtraFunctions::glProgramUniformMatrix2x4fv(GLuint program, GLint location, GLsizei count, GLboolean transpose, const GLfloat *value)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLExtraFunctions::glProgramUniformMatrix2x4fv` 用于执行与“gl、Program、Uniform、Matrix、2、x、4、fv”相关的操作。调用时要先确认当前状态和 `program`、`location`、`count`、`transpose`、`value` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `program`：类型为 `GLuint`。没有默认值，调用时必须提供。传入 `GLuint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `location`：类型为 `GLint`。没有默认值，调用时必须提供。传入 `GLint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `count`：类型为 `GLsizei`。没有默认值，调用时必须提供。传入 `GLsizei` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `transpose`：类型为 `GLboolean`。没有默认值，调用时必须提供。传入 `GLboolean` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `value`：类型为 `const GLfloat *`。没有默认值，调用时必须提供。要读取或写入的值。要确认类型转换、默认值、所有权以及写入后是否触发通知。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLExtraFunctions::glProgramUniformMatrix3fv(GLuint program, GLint location, GLsizei count, GLboolean transpose, const GLfloat *value)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLExtraFunctions::glProgramUniformMatrix3fv` 用于执行与“gl、Program、Uniform、Matrix、3、fv”相关的操作。调用时要先确认当前状态和 `program`、`location`、`count`、`transpose`、`value` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `program`：类型为 `GLuint`。没有默认值，调用时必须提供。传入 `GLuint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `location`：类型为 `GLint`。没有默认值，调用时必须提供。传入 `GLint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `count`：类型为 `GLsizei`。没有默认值，调用时必须提供。传入 `GLsizei` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `transpose`：类型为 `GLboolean`。没有默认值，调用时必须提供。传入 `GLboolean` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `value`：类型为 `const GLfloat *`。没有默认值，调用时必须提供。要读取或写入的值。要确认类型转换、默认值、所有权以及写入后是否触发通知。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLExtraFunctions::glProgramUniformMatrix3x2fv(GLuint program, GLint location, GLsizei count, GLboolean transpose, const GLfloat *value)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLExtraFunctions::glProgramUniformMatrix3x2fv` 用于执行与“gl、Program、Uniform、Matrix、3、x、2、fv”相关的操作。调用时要先确认当前状态和 `program`、`location`、`count`、`transpose`、`value` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `program`：类型为 `GLuint`。没有默认值，调用时必须提供。传入 `GLuint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `location`：类型为 `GLint`。没有默认值，调用时必须提供。传入 `GLint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `count`：类型为 `GLsizei`。没有默认值，调用时必须提供。传入 `GLsizei` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `transpose`：类型为 `GLboolean`。没有默认值，调用时必须提供。传入 `GLboolean` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `value`：类型为 `const GLfloat *`。没有默认值，调用时必须提供。要读取或写入的值。要确认类型转换、默认值、所有权以及写入后是否触发通知。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLExtraFunctions::glProgramUniformMatrix3x4fv(GLuint program, GLint location, GLsizei count, GLboolean transpose, const GLfloat *value)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLExtraFunctions::glProgramUniformMatrix3x4fv` 用于执行与“gl、Program、Uniform、Matrix、3、x、4、fv”相关的操作。调用时要先确认当前状态和 `program`、`location`、`count`、`transpose`、`value` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `program`：类型为 `GLuint`。没有默认值，调用时必须提供。传入 `GLuint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `location`：类型为 `GLint`。没有默认值，调用时必须提供。传入 `GLint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `count`：类型为 `GLsizei`。没有默认值，调用时必须提供。传入 `GLsizei` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `transpose`：类型为 `GLboolean`。没有默认值，调用时必须提供。传入 `GLboolean` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `value`：类型为 `const GLfloat *`。没有默认值，调用时必须提供。要读取或写入的值。要确认类型转换、默认值、所有权以及写入后是否触发通知。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLExtraFunctions::glProgramUniformMatrix4fv(GLuint program, GLint location, GLsizei count, GLboolean transpose, const GLfloat *value)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLExtraFunctions::glProgramUniformMatrix4fv` 用于执行与“gl、Program、Uniform、Matrix、4、fv”相关的操作。调用时要先确认当前状态和 `program`、`location`、`count`、`transpose`、`value` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `program`：类型为 `GLuint`。没有默认值，调用时必须提供。传入 `GLuint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `location`：类型为 `GLint`。没有默认值，调用时必须提供。传入 `GLint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `count`：类型为 `GLsizei`。没有默认值，调用时必须提供。传入 `GLsizei` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `transpose`：类型为 `GLboolean`。没有默认值，调用时必须提供。传入 `GLboolean` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `value`：类型为 `const GLfloat *`。没有默认值，调用时必须提供。要读取或写入的值。要确认类型转换、默认值、所有权以及写入后是否触发通知。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLExtraFunctions::glProgramUniformMatrix4x2fv(GLuint program, GLint location, GLsizei count, GLboolean transpose, const GLfloat *value)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLExtraFunctions::glProgramUniformMatrix4x2fv` 用于执行与“gl、Program、Uniform、Matrix、4、x、2、fv”相关的操作。调用时要先确认当前状态和 `program`、`location`、`count`、`transpose`、`value` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `program`：类型为 `GLuint`。没有默认值，调用时必须提供。传入 `GLuint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `location`：类型为 `GLint`。没有默认值，调用时必须提供。传入 `GLint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `count`：类型为 `GLsizei`。没有默认值，调用时必须提供。传入 `GLsizei` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `transpose`：类型为 `GLboolean`。没有默认值，调用时必须提供。传入 `GLboolean` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `value`：类型为 `const GLfloat *`。没有默认值，调用时必须提供。要读取或写入的值。要确认类型转换、默认值、所有权以及写入后是否触发通知。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLExtraFunctions::glProgramUniformMatrix4x3fv(GLuint program, GLint location, GLsizei count, GLboolean transpose, const GLfloat *value)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLExtraFunctions::glProgramUniformMatrix4x3fv` 用于执行与“gl、Program、Uniform、Matrix、4、x、3、fv”相关的操作。调用时要先确认当前状态和 `program`、`location`、`count`、`transpose`、`value` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `program`：类型为 `GLuint`。没有默认值，调用时必须提供。传入 `GLuint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `location`：类型为 `GLint`。没有默认值，调用时必须提供。传入 `GLint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `count`：类型为 `GLsizei`。没有默认值，调用时必须提供。传入 `GLsizei` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `transpose`：类型为 `GLboolean`。没有默认值，调用时必须提供。传入 `GLboolean` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `value`：类型为 `const GLfloat *`。没有默认值，调用时必须提供。要读取或写入的值。要确认类型转换、默认值、所有权以及写入后是否触发通知。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLExtraFunctions::glPushDebugGroup(GLenum source, GLuint id, GLsizei length, const GLchar *message)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLExtraFunctions::glPushDebugGroup` 用于执行与“gl、Push、调试输出、Group”相关的操作。调用时要先确认当前状态和 `source`、`id`、`length`、`message` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `source`：类型为 `GLenum`。没有默认值，调用时必须提供。源对象、源索引或源数据；它通常决定操作的输入，转换后要确认源的生命周期和线程归属。
- 参数 `id`：类型为 `GLuint`。没有默认值，调用时必须提供。传入 `GLuint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `length`：类型为 `GLsizei`。没有默认值，调用时必须提供。传入 `GLsizei` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `message`：类型为 `const GLchar *`。没有默认值，调用时必须提供。传入 `const GLchar *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLExtraFunctions::glReadBuffer(GLenum src)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLExtraFunctions::glReadBuffer` 用于执行与“gl、读取、Buffer”相关的操作。调用时要先确认当前状态和 `src` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `src`：类型为 `GLenum`。没有默认值，调用时必须提供。枚举或标志参数。先确认可用枚举值、互斥关系和默认值，必要时用按位或组合标志。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLExtraFunctions::glReadnPixels(GLint x, GLint y, GLsizei width, GLsizei height, GLenum format, GLenum type, GLsizei bufSize, void *data)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLExtraFunctions::glReadnPixels` 用于执行与“gl、Readn、Pixels”相关的操作。调用时要先确认当前状态和 `x`、`y`、`width`、`height`、`format`、`type`、`bufSize`、`data` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `x`：类型为 `GLint`。没有默认值，调用时必须提供。传入 `GLint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `y`：类型为 `GLint`。没有默认值，调用时必须提供。传入 `GLint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `width`：类型为 `GLsizei`。没有默认值，调用时必须提供。宽度，通常以像素、字符数或元素数量表示；要确认是否允许 0、负数和超出最大值。
- 参数 `height`：类型为 `GLsizei`。没有默认值，调用时必须提供。高度，通常以像素、字符数或元素数量表示；要确认是否允许 0、负数和超出最大值。
- 参数 `format`：类型为 `GLenum`。没有默认值，调用时必须提供。数据格式或显示格式。格式通常会影响解析、像素布局、精度、编码或兼容性。
- 参数 `type`：类型为 `GLenum`。没有默认值，调用时必须提供。类型、格式或策略枚举。要确认枚举值的适用范围和平台支持情况。
- 参数 `bufSize`：类型为 `GLsizei`。没有默认值，调用时必须提供。传入 `GLsizei` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `data`：类型为 `void *`。没有默认值，调用时必须提供。数据载荷或要读取的数据。要确认编码、所有权、大小和是否允许为空。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLExtraFunctions::glRenderbufferStorageMultisample(GLenum target, GLsizei samples, GLenum internalformat, GLsizei width, GLsizei height)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLExtraFunctions::glRenderbufferStorageMultisample` 用于执行与“gl、Renderbuffer、Storage、Multisample”相关的操作。调用时要先确认当前状态和 `target`、`samples`、`internalformat`、`width`、`height` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `target`：类型为 `GLenum`。没有默认值，调用时必须提供。目标对象、目标属性或目标资源。要确认它在操作期间仍然有效，并支持所需能力。
- 参数 `samples`：类型为 `GLsizei`。没有默认值，调用时必须提供。传入 `GLsizei` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `internalformat`：类型为 `GLenum`。没有默认值，调用时必须提供。枚举或标志参数。先确认可用枚举值、互斥关系和默认值，必要时用按位或组合标志。
- 参数 `width`：类型为 `GLsizei`。没有默认值，调用时必须提供。宽度，通常以像素、字符数或元素数量表示；要确认是否允许 0、负数和超出最大值。
- 参数 `height`：类型为 `GLsizei`。没有默认值，调用时必须提供。高度，通常以像素、字符数或元素数量表示；要确认是否允许 0、负数和超出最大值。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLExtraFunctions::glResumeTransformFeedback()`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLExtraFunctions::glResumeTransformFeedback` 用于执行与“gl、恢复运行、Transform、Feedback”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLExtraFunctions::glSampleMaski(GLuint maskNumber, GLbitfield mask)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLExtraFunctions::glSampleMaski` 用于执行与“gl、Sample、Maski”相关的操作。调用时要先确认当前状态和 `maskNumber`、`mask` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `maskNumber`：类型为 `GLuint`。没有默认值，调用时必须提供。传入 `GLuint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `mask`：类型为 `GLbitfield`。没有默认值，调用时必须提供。传入 `GLbitfield` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLExtraFunctions::glSamplerParameterIiv(GLuint sampler, GLenum pname, const GLint *param)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLExtraFunctions::glSamplerParameterIiv` 用于执行与“gl、Sampler、Parameter、Iiv”相关的操作。调用时要先确认当前状态和 `sampler`、`pname`、`param` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `sampler`：类型为 `GLuint`。没有默认值，调用时必须提供。传入 `GLuint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `pname`：类型为 `GLenum`。没有默认值，调用时必须提供。枚举或标志参数。先确认可用枚举值、互斥关系和默认值，必要时用按位或组合标志。
- 参数 `param`：类型为 `const GLint *`。没有默认值，调用时必须提供。传入 `const GLint *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLExtraFunctions::glSamplerParameterIuiv(GLuint sampler, GLenum pname, const GLuint *param)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLExtraFunctions::glSamplerParameterIuiv` 用于执行与“gl、Sampler、Parameter、Iuiv”相关的操作。调用时要先确认当前状态和 `sampler`、`pname`、`param` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `sampler`：类型为 `GLuint`。没有默认值，调用时必须提供。传入 `GLuint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `pname`：类型为 `GLenum`。没有默认值，调用时必须提供。枚举或标志参数。先确认可用枚举值、互斥关系和默认值，必要时用按位或组合标志。
- 参数 `param`：类型为 `const GLuint *`。没有默认值，调用时必须提供。传入 `const GLuint *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLExtraFunctions::glSamplerParameterf(GLuint sampler, GLenum pname, GLfloat param)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLExtraFunctions::glSamplerParameterf` 用于执行与“gl、Sampler、Parameterf”相关的操作。调用时要先确认当前状态和 `sampler`、`pname`、`param` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `sampler`：类型为 `GLuint`。没有默认值，调用时必须提供。传入 `GLuint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `pname`：类型为 `GLenum`。没有默认值，调用时必须提供。枚举或标志参数。先确认可用枚举值、互斥关系和默认值，必要时用按位或组合标志。
- 参数 `param`：类型为 `GLfloat`。没有默认值，调用时必须提供。传入 `GLfloat` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLExtraFunctions::glSamplerParameterfv(GLuint sampler, GLenum pname, const GLfloat *param)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLExtraFunctions::glSamplerParameterfv` 用于执行与“gl、Sampler、Parameterfv”相关的操作。调用时要先确认当前状态和 `sampler`、`pname`、`param` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `sampler`：类型为 `GLuint`。没有默认值，调用时必须提供。传入 `GLuint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `pname`：类型为 `GLenum`。没有默认值，调用时必须提供。枚举或标志参数。先确认可用枚举值、互斥关系和默认值，必要时用按位或组合标志。
- 参数 `param`：类型为 `const GLfloat *`。没有默认值，调用时必须提供。传入 `const GLfloat *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLExtraFunctions::glSamplerParameteri(GLuint sampler, GLenum pname, GLint param)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLExtraFunctions::glSamplerParameteri` 用于执行与“gl、Sampler、Parameteri”相关的操作。调用时要先确认当前状态和 `sampler`、`pname`、`param` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `sampler`：类型为 `GLuint`。没有默认值，调用时必须提供。传入 `GLuint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `pname`：类型为 `GLenum`。没有默认值，调用时必须提供。枚举或标志参数。先确认可用枚举值、互斥关系和默认值，必要时用按位或组合标志。
- 参数 `param`：类型为 `GLint`。没有默认值，调用时必须提供。传入 `GLint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLExtraFunctions::glSamplerParameteriv(GLuint sampler, GLenum pname, const GLint *param)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLExtraFunctions::glSamplerParameteriv` 用于执行与“gl、Sampler、Parameteriv”相关的操作。调用时要先确认当前状态和 `sampler`、`pname`、`param` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `sampler`：类型为 `GLuint`。没有默认值，调用时必须提供。传入 `GLuint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `pname`：类型为 `GLenum`。没有默认值，调用时必须提供。枚举或标志参数。先确认可用枚举值、互斥关系和默认值，必要时用按位或组合标志。
- 参数 `param`：类型为 `const GLint *`。没有默认值，调用时必须提供。传入 `const GLint *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLExtraFunctions::glTexBuffer(GLenum target, GLenum internalformat, GLuint buffer)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLExtraFunctions::glTexBuffer` 用于执行与“gl、Tex、Buffer”相关的操作。调用时要先确认当前状态和 `target`、`internalformat`、`buffer` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `target`：类型为 `GLenum`。没有默认值，调用时必须提供。目标对象、目标属性或目标资源。要确认它在操作期间仍然有效，并支持所需能力。
- 参数 `internalformat`：类型为 `GLenum`。没有默认值，调用时必须提供。枚举或标志参数。先确认可用枚举值、互斥关系和默认值，必要时用按位或组合标志。
- 参数 `buffer`：类型为 `GLuint`。没有默认值，调用时必须提供。传入 `GLuint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLExtraFunctions::glTexBufferRange(GLenum target, GLenum internalformat, GLuint buffer, GLintptr offset, GLsizeiptr size)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLExtraFunctions::glTexBufferRange` 用于执行与“gl、Tex、Buffer、Range”相关的操作。调用时要先确认当前状态和 `target`、`internalformat`、`buffer`、`offset`、`size` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `target`：类型为 `GLenum`。没有默认值，调用时必须提供。目标对象、目标属性或目标资源。要确认它在操作期间仍然有效，并支持所需能力。
- 参数 `internalformat`：类型为 `GLenum`。没有默认值，调用时必须提供。枚举或标志参数。先确认可用枚举值、互斥关系和默认值，必要时用按位或组合标志。
- 参数 `buffer`：类型为 `GLuint`。没有默认值，调用时必须提供。传入 `GLuint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `offset`：类型为 `GLintptr`。没有默认值，调用时必须提供。传入 `GLintptr` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `size`：类型为 `GLsizeiptr`。没有默认值，调用时必须提供。尺寸或长度，单位通常是像素、字节、元素数或时间，必须结合类型和类的上下文确认。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLExtraFunctions::glTexImage3D(GLenum target, GLint level, GLint internalformat, GLsizei width, GLsizei height, GLsizei depth, GLint border, GLenum format, GLenum type, const void *pixels)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLExtraFunctions::glTexImage3D` 用于执行与“gl、Tex、Image、3、D”相关的操作。调用时要先确认当前状态和 `target`、`level`、`internalformat`、`width`、`height`、`depth`、`border`、`format`、`type`、`pixels` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `target`：类型为 `GLenum`。没有默认值，调用时必须提供。目标对象、目标属性或目标资源。要确认它在操作期间仍然有效，并支持所需能力。
- 参数 `level`：类型为 `GLint`。没有默认值，调用时必须提供。传入 `GLint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `internalformat`：类型为 `GLint`。没有默认值，调用时必须提供。传入 `GLint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `width`：类型为 `GLsizei`。没有默认值，调用时必须提供。宽度，通常以像素、字符数或元素数量表示；要确认是否允许 0、负数和超出最大值。
- 参数 `height`：类型为 `GLsizei`。没有默认值，调用时必须提供。高度，通常以像素、字符数或元素数量表示；要确认是否允许 0、负数和超出最大值。
- 参数 `depth`：类型为 `GLsizei`。没有默认值，调用时必须提供。传入 `GLsizei` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `border`：类型为 `GLint`。没有默认值，调用时必须提供。传入 `GLint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `format`：类型为 `GLenum`。没有默认值，调用时必须提供。数据格式或显示格式。格式通常会影响解析、像素布局、精度、编码或兼容性。
- 参数 `type`：类型为 `GLenum`。没有默认值，调用时必须提供。类型、格式或策略枚举。要确认枚举值的适用范围和平台支持情况。
- 参数 `pixels`：类型为 `const void *`。没有默认值，调用时必须提供。传入 `const void *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLExtraFunctions::glTexParameterIiv(GLenum target, GLenum pname, const GLint *params)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLExtraFunctions::glTexParameterIiv` 用于执行与“gl、Tex、Parameter、Iiv”相关的操作。调用时要先确认当前状态和 `target`、`pname`、`params` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `target`：类型为 `GLenum`。没有默认值，调用时必须提供。目标对象、目标属性或目标资源。要确认它在操作期间仍然有效，并支持所需能力。
- 参数 `pname`：类型为 `GLenum`。没有默认值，调用时必须提供。枚举或标志参数。先确认可用枚举值、互斥关系和默认值，必要时用按位或组合标志。
- 参数 `params`：类型为 `const GLint *`。没有默认值，调用时必须提供。传入 `const GLint *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLExtraFunctions::glTexParameterIuiv(GLenum target, GLenum pname, const GLuint *params)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLExtraFunctions::glTexParameterIuiv` 用于执行与“gl、Tex、Parameter、Iuiv”相关的操作。调用时要先确认当前状态和 `target`、`pname`、`params` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `target`：类型为 `GLenum`。没有默认值，调用时必须提供。目标对象、目标属性或目标资源。要确认它在操作期间仍然有效，并支持所需能力。
- 参数 `pname`：类型为 `GLenum`。没有默认值，调用时必须提供。枚举或标志参数。先确认可用枚举值、互斥关系和默认值，必要时用按位或组合标志。
- 参数 `params`：类型为 `const GLuint *`。没有默认值，调用时必须提供。传入 `const GLuint *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLExtraFunctions::glTexStorage2D(GLenum target, GLsizei levels, GLenum internalformat, GLsizei width, GLsizei height)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLExtraFunctions::glTexStorage2D` 用于执行与“gl、Tex、Storage、2、D”相关的操作。调用时要先确认当前状态和 `target`、`levels`、`internalformat`、`width`、`height` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `target`：类型为 `GLenum`。没有默认值，调用时必须提供。目标对象、目标属性或目标资源。要确认它在操作期间仍然有效，并支持所需能力。
- 参数 `levels`：类型为 `GLsizei`。没有默认值，调用时必须提供。传入 `GLsizei` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `internalformat`：类型为 `GLenum`。没有默认值，调用时必须提供。枚举或标志参数。先确认可用枚举值、互斥关系和默认值，必要时用按位或组合标志。
- 参数 `width`：类型为 `GLsizei`。没有默认值，调用时必须提供。宽度，通常以像素、字符数或元素数量表示；要确认是否允许 0、负数和超出最大值。
- 参数 `height`：类型为 `GLsizei`。没有默认值，调用时必须提供。高度，通常以像素、字符数或元素数量表示；要确认是否允许 0、负数和超出最大值。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLExtraFunctions::glTexStorage2DMultisample(GLenum target, GLsizei samples, GLenum internalformat, GLsizei width, GLsizei height, GLboolean fixedsamplelocations)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLExtraFunctions::glTexStorage2DMultisample` 用于执行与“gl、Tex、Storage、2、D、Multisample”相关的操作。调用时要先确认当前状态和 `target`、`samples`、`internalformat`、`width`、`height`、`fixedsamplelocations` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `target`：类型为 `GLenum`。没有默认值，调用时必须提供。目标对象、目标属性或目标资源。要确认它在操作期间仍然有效，并支持所需能力。
- 参数 `samples`：类型为 `GLsizei`。没有默认值，调用时必须提供。传入 `GLsizei` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `internalformat`：类型为 `GLenum`。没有默认值，调用时必须提供。枚举或标志参数。先确认可用枚举值、互斥关系和默认值，必要时用按位或组合标志。
- 参数 `width`：类型为 `GLsizei`。没有默认值，调用时必须提供。宽度，通常以像素、字符数或元素数量表示；要确认是否允许 0、负数和超出最大值。
- 参数 `height`：类型为 `GLsizei`。没有默认值，调用时必须提供。高度，通常以像素、字符数或元素数量表示；要确认是否允许 0、负数和超出最大值。
- 参数 `fixedsamplelocations`：类型为 `GLboolean`。没有默认值，调用时必须提供。传入 `GLboolean` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLExtraFunctions::glTexStorage3D(GLenum target, GLsizei levels, GLenum internalformat, GLsizei width, GLsizei height, GLsizei depth)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLExtraFunctions::glTexStorage3D` 用于执行与“gl、Tex、Storage、3、D”相关的操作。调用时要先确认当前状态和 `target`、`levels`、`internalformat`、`width`、`height`、`depth` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `target`：类型为 `GLenum`。没有默认值，调用时必须提供。目标对象、目标属性或目标资源。要确认它在操作期间仍然有效，并支持所需能力。
- 参数 `levels`：类型为 `GLsizei`。没有默认值，调用时必须提供。传入 `GLsizei` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `internalformat`：类型为 `GLenum`。没有默认值，调用时必须提供。枚举或标志参数。先确认可用枚举值、互斥关系和默认值，必要时用按位或组合标志。
- 参数 `width`：类型为 `GLsizei`。没有默认值，调用时必须提供。宽度，通常以像素、字符数或元素数量表示；要确认是否允许 0、负数和超出最大值。
- 参数 `height`：类型为 `GLsizei`。没有默认值，调用时必须提供。高度，通常以像素、字符数或元素数量表示；要确认是否允许 0、负数和超出最大值。
- 参数 `depth`：类型为 `GLsizei`。没有默认值，调用时必须提供。传入 `GLsizei` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLExtraFunctions::glTexStorage3DMultisample(GLenum target, GLsizei samples, GLenum internalformat, GLsizei width, GLsizei height, GLsizei depth, GLboolean fixedsamplelocations)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLExtraFunctions::glTexStorage3DMultisample` 用于执行与“gl、Tex、Storage、3、D、Multisample”相关的操作。调用时要先确认当前状态和 `target`、`samples`、`internalformat`、`width`、`height`、`depth`、`fixedsamplelocations` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `target`：类型为 `GLenum`。没有默认值，调用时必须提供。目标对象、目标属性或目标资源。要确认它在操作期间仍然有效，并支持所需能力。
- 参数 `samples`：类型为 `GLsizei`。没有默认值，调用时必须提供。传入 `GLsizei` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `internalformat`：类型为 `GLenum`。没有默认值，调用时必须提供。枚举或标志参数。先确认可用枚举值、互斥关系和默认值，必要时用按位或组合标志。
- 参数 `width`：类型为 `GLsizei`。没有默认值，调用时必须提供。宽度，通常以像素、字符数或元素数量表示；要确认是否允许 0、负数和超出最大值。
- 参数 `height`：类型为 `GLsizei`。没有默认值，调用时必须提供。高度，通常以像素、字符数或元素数量表示；要确认是否允许 0、负数和超出最大值。
- 参数 `depth`：类型为 `GLsizei`。没有默认值，调用时必须提供。传入 `GLsizei` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `fixedsamplelocations`：类型为 `GLboolean`。没有默认值，调用时必须提供。传入 `GLboolean` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLExtraFunctions::glTexSubImage3D(GLenum target, GLint level, GLint xoffset, GLint yoffset, GLint zoffset, GLsizei width, GLsizei height, GLsizei depth, GLenum format, GLenum type, const void *pixels)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLExtraFunctions::glTexSubImage3D` 用于执行与“gl、Tex、Sub、Image、3、D”相关的操作。调用时要先确认当前状态和 `target`、`level`、`xoffset`、`yoffset`、`zoffset`、`width`、`height`、`depth`、`format`、`type`、`pixels` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `target`：类型为 `GLenum`。没有默认值，调用时必须提供。目标对象、目标属性或目标资源。要确认它在操作期间仍然有效，并支持所需能力。
- 参数 `level`：类型为 `GLint`。没有默认值，调用时必须提供。传入 `GLint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `xoffset`：类型为 `GLint`。没有默认值，调用时必须提供。传入 `GLint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `yoffset`：类型为 `GLint`。没有默认值，调用时必须提供。传入 `GLint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `zoffset`：类型为 `GLint`。没有默认值，调用时必须提供。传入 `GLint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `width`：类型为 `GLsizei`。没有默认值，调用时必须提供。宽度，通常以像素、字符数或元素数量表示；要确认是否允许 0、负数和超出最大值。
- 参数 `height`：类型为 `GLsizei`。没有默认值，调用时必须提供。高度，通常以像素、字符数或元素数量表示；要确认是否允许 0、负数和超出最大值。
- 参数 `depth`：类型为 `GLsizei`。没有默认值，调用时必须提供。传入 `GLsizei` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `format`：类型为 `GLenum`。没有默认值，调用时必须提供。数据格式或显示格式。格式通常会影响解析、像素布局、精度、编码或兼容性。
- 参数 `type`：类型为 `GLenum`。没有默认值，调用时必须提供。类型、格式或策略枚举。要确认枚举值的适用范围和平台支持情况。
- 参数 `pixels`：类型为 `const void *`。没有默认值，调用时必须提供。传入 `const void *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLExtraFunctions::glTransformFeedbackVaryings(GLuint program, GLsizei count, const GLchar *const *varyings, GLenum bufferMode)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLExtraFunctions::glTransformFeedbackVaryings` 用于执行与“gl、Transform、Feedback、Varyings”相关的操作。调用时要先确认当前状态和 `program`、`count`、`varyings`、`bufferMode` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `program`：类型为 `GLuint`。没有默认值，调用时必须提供。传入 `GLuint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `count`：类型为 `GLsizei`。没有默认值，调用时必须提供。传入 `GLsizei` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `varyings`：类型为 `const GLchar *const *`。没有默认值，调用时必须提供。传入 `const GLchar *const *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `bufferMode`：类型为 `GLenum`。没有默认值，调用时必须提供。枚举或标志参数。先确认可用枚举值、互斥关系和默认值，必要时用按位或组合标志。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLExtraFunctions::glUniform1ui(GLint location, GLuint v0)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLExtraFunctions::glUniform1ui` 用于执行与“gl、Uniform、1、ui”相关的操作。调用时要先确认当前状态和 `location`、`v0` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `location`：类型为 `GLint`。没有默认值，调用时必须提供。传入 `GLint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `v0`：类型为 `GLuint`。没有默认值，调用时必须提供。传入 `GLuint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLExtraFunctions::glUniform1uiv(GLint location, GLsizei count, const GLuint *value)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLExtraFunctions::glUniform1uiv` 用于执行与“gl、Uniform、1、uiv”相关的操作。调用时要先确认当前状态和 `location`、`count`、`value` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `location`：类型为 `GLint`。没有默认值，调用时必须提供。传入 `GLint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `count`：类型为 `GLsizei`。没有默认值，调用时必须提供。传入 `GLsizei` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `value`：类型为 `const GLuint *`。没有默认值，调用时必须提供。要读取或写入的值。要确认类型转换、默认值、所有权以及写入后是否触发通知。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLExtraFunctions::glUniform2ui(GLint location, GLuint v0, GLuint v1)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLExtraFunctions::glUniform2ui` 用于执行与“gl、Uniform、2、ui”相关的操作。调用时要先确认当前状态和 `location`、`v0`、`v1` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `location`：类型为 `GLint`。没有默认值，调用时必须提供。传入 `GLint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `v0`：类型为 `GLuint`。没有默认值，调用时必须提供。传入 `GLuint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `v1`：类型为 `GLuint`。没有默认值，调用时必须提供。传入 `GLuint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLExtraFunctions::glUniform2uiv(GLint location, GLsizei count, const GLuint *value)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLExtraFunctions::glUniform2uiv` 用于执行与“gl、Uniform、2、uiv”相关的操作。调用时要先确认当前状态和 `location`、`count`、`value` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `location`：类型为 `GLint`。没有默认值，调用时必须提供。传入 `GLint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `count`：类型为 `GLsizei`。没有默认值，调用时必须提供。传入 `GLsizei` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `value`：类型为 `const GLuint *`。没有默认值，调用时必须提供。要读取或写入的值。要确认类型转换、默认值、所有权以及写入后是否触发通知。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLExtraFunctions::glUniform3ui(GLint location, GLuint v0, GLuint v1, GLuint v2)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLExtraFunctions::glUniform3ui` 用于执行与“gl、Uniform、3、ui”相关的操作。调用时要先确认当前状态和 `location`、`v0`、`v1`、`v2` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `location`：类型为 `GLint`。没有默认值，调用时必须提供。传入 `GLint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `v0`：类型为 `GLuint`。没有默认值，调用时必须提供。传入 `GLuint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `v1`：类型为 `GLuint`。没有默认值，调用时必须提供。传入 `GLuint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `v2`：类型为 `GLuint`。没有默认值，调用时必须提供。传入 `GLuint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLExtraFunctions::glUniform3uiv(GLint location, GLsizei count, const GLuint *value)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLExtraFunctions::glUniform3uiv` 用于执行与“gl、Uniform、3、uiv”相关的操作。调用时要先确认当前状态和 `location`、`count`、`value` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `location`：类型为 `GLint`。没有默认值，调用时必须提供。传入 `GLint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `count`：类型为 `GLsizei`。没有默认值，调用时必须提供。传入 `GLsizei` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `value`：类型为 `const GLuint *`。没有默认值，调用时必须提供。要读取或写入的值。要确认类型转换、默认值、所有权以及写入后是否触发通知。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLExtraFunctions::glUniform4ui(GLint location, GLuint v0, GLuint v1, GLuint v2, GLuint v3)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLExtraFunctions::glUniform4ui` 用于执行与“gl、Uniform、4、ui”相关的操作。调用时要先确认当前状态和 `location`、`v0`、`v1`、`v2`、`v3` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `location`：类型为 `GLint`。没有默认值，调用时必须提供。传入 `GLint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `v0`：类型为 `GLuint`。没有默认值，调用时必须提供。传入 `GLuint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `v1`：类型为 `GLuint`。没有默认值，调用时必须提供。传入 `GLuint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `v2`：类型为 `GLuint`。没有默认值，调用时必须提供。传入 `GLuint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `v3`：类型为 `GLuint`。没有默认值，调用时必须提供。传入 `GLuint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLExtraFunctions::glUniform4uiv(GLint location, GLsizei count, const GLuint *value)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLExtraFunctions::glUniform4uiv` 用于执行与“gl、Uniform、4、uiv”相关的操作。调用时要先确认当前状态和 `location`、`count`、`value` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `location`：类型为 `GLint`。没有默认值，调用时必须提供。传入 `GLint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `count`：类型为 `GLsizei`。没有默认值，调用时必须提供。传入 `GLsizei` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `value`：类型为 `const GLuint *`。没有默认值，调用时必须提供。要读取或写入的值。要确认类型转换、默认值、所有权以及写入后是否触发通知。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLExtraFunctions::glUniformBlockBinding(GLuint program, GLuint uniformBlockIndex, GLuint uniformBlockBinding)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLExtraFunctions::glUniformBlockBinding` 用于执行与“gl、Uniform、阻塞或屏蔽、Binding”相关的操作。调用时要先确认当前状态和 `program`、`uniformBlockIndex`、`uniformBlockBinding` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `program`：类型为 `GLuint`。没有默认值，调用时必须提供。传入 `GLuint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `uniformBlockIndex`：类型为 `GLuint`。没有默认值，调用时必须提供。传入 `GLuint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `uniformBlockBinding`：类型为 `GLuint`。没有默认值，调用时必须提供。传入 `GLuint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLExtraFunctions::glUniformMatrix2x3fv(GLint location, GLsizei count, GLboolean transpose, const GLfloat *value)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLExtraFunctions::glUniformMatrix2x3fv` 用于执行与“gl、Uniform、Matrix、2、x、3、fv”相关的操作。调用时要先确认当前状态和 `location`、`count`、`transpose`、`value` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `location`：类型为 `GLint`。没有默认值，调用时必须提供。传入 `GLint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `count`：类型为 `GLsizei`。没有默认值，调用时必须提供。传入 `GLsizei` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `transpose`：类型为 `GLboolean`。没有默认值，调用时必须提供。传入 `GLboolean` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `value`：类型为 `const GLfloat *`。没有默认值，调用时必须提供。要读取或写入的值。要确认类型转换、默认值、所有权以及写入后是否触发通知。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLExtraFunctions::glUniformMatrix2x4fv(GLint location, GLsizei count, GLboolean transpose, const GLfloat *value)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLExtraFunctions::glUniformMatrix2x4fv` 用于执行与“gl、Uniform、Matrix、2、x、4、fv”相关的操作。调用时要先确认当前状态和 `location`、`count`、`transpose`、`value` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `location`：类型为 `GLint`。没有默认值，调用时必须提供。传入 `GLint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `count`：类型为 `GLsizei`。没有默认值，调用时必须提供。传入 `GLsizei` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `transpose`：类型为 `GLboolean`。没有默认值，调用时必须提供。传入 `GLboolean` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `value`：类型为 `const GLfloat *`。没有默认值，调用时必须提供。要读取或写入的值。要确认类型转换、默认值、所有权以及写入后是否触发通知。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLExtraFunctions::glUniformMatrix3x2fv(GLint location, GLsizei count, GLboolean transpose, const GLfloat *value)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLExtraFunctions::glUniformMatrix3x2fv` 用于执行与“gl、Uniform、Matrix、3、x、2、fv”相关的操作。调用时要先确认当前状态和 `location`、`count`、`transpose`、`value` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `location`：类型为 `GLint`。没有默认值，调用时必须提供。传入 `GLint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `count`：类型为 `GLsizei`。没有默认值，调用时必须提供。传入 `GLsizei` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `transpose`：类型为 `GLboolean`。没有默认值，调用时必须提供。传入 `GLboolean` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `value`：类型为 `const GLfloat *`。没有默认值，调用时必须提供。要读取或写入的值。要确认类型转换、默认值、所有权以及写入后是否触发通知。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLExtraFunctions::glUniformMatrix3x4fv(GLint location, GLsizei count, GLboolean transpose, const GLfloat *value)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLExtraFunctions::glUniformMatrix3x4fv` 用于执行与“gl、Uniform、Matrix、3、x、4、fv”相关的操作。调用时要先确认当前状态和 `location`、`count`、`transpose`、`value` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `location`：类型为 `GLint`。没有默认值，调用时必须提供。传入 `GLint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `count`：类型为 `GLsizei`。没有默认值，调用时必须提供。传入 `GLsizei` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `transpose`：类型为 `GLboolean`。没有默认值，调用时必须提供。传入 `GLboolean` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `value`：类型为 `const GLfloat *`。没有默认值，调用时必须提供。要读取或写入的值。要确认类型转换、默认值、所有权以及写入后是否触发通知。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLExtraFunctions::glUniformMatrix4x2fv(GLint location, GLsizei count, GLboolean transpose, const GLfloat *value)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLExtraFunctions::glUniformMatrix4x2fv` 用于执行与“gl、Uniform、Matrix、4、x、2、fv”相关的操作。调用时要先确认当前状态和 `location`、`count`、`transpose`、`value` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `location`：类型为 `GLint`。没有默认值，调用时必须提供。传入 `GLint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `count`：类型为 `GLsizei`。没有默认值，调用时必须提供。传入 `GLsizei` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `transpose`：类型为 `GLboolean`。没有默认值，调用时必须提供。传入 `GLboolean` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `value`：类型为 `const GLfloat *`。没有默认值，调用时必须提供。要读取或写入的值。要确认类型转换、默认值、所有权以及写入后是否触发通知。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLExtraFunctions::glUniformMatrix4x3fv(GLint location, GLsizei count, GLboolean transpose, const GLfloat *value)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLExtraFunctions::glUniformMatrix4x3fv` 用于执行与“gl、Uniform、Matrix、4、x、3、fv”相关的操作。调用时要先确认当前状态和 `location`、`count`、`transpose`、`value` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `location`：类型为 `GLint`。没有默认值，调用时必须提供。传入 `GLint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `count`：类型为 `GLsizei`。没有默认值，调用时必须提供。传入 `GLsizei` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `transpose`：类型为 `GLboolean`。没有默认值，调用时必须提供。传入 `GLboolean` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `value`：类型为 `const GLfloat *`。没有默认值，调用时必须提供。要读取或写入的值。要确认类型转换、默认值、所有权以及写入后是否触发通知。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `GLboolean QOpenGLExtraFunctions::glUnmapBuffer(GLenum target)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLExtraFunctions::glUnmapBuffer` 用于计算、查询或取得与“gl、Unmap、Buffer”相关的操作。调用时要先确认当前状态和 `target` 的有效范围；返回类型是 `GLboolean`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`GLboolean`。
- 参数 `target`：类型为 `GLenum`。没有默认值，调用时必须提供。目标对象、目标属性或目标资源。要确认它在操作期间仍然有效，并支持所需能力。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLExtraFunctions::glUseProgramStages(GLuint pipeline, GLbitfield stages, GLuint program)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLExtraFunctions::glUseProgramStages` 用于执行与“gl、Use、Program、Stages”相关的操作。调用时要先确认当前状态和 `pipeline`、`stages`、`program` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `pipeline`：类型为 `GLuint`。没有默认值，调用时必须提供。传入 `GLuint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `stages`：类型为 `GLbitfield`。没有默认值，调用时必须提供。传入 `GLbitfield` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `program`：类型为 `GLuint`。没有默认值，调用时必须提供。传入 `GLuint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLExtraFunctions::glValidateProgramPipeline(GLuint pipeline)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLExtraFunctions::glValidateProgramPipeline` 用于执行与“gl、Validate、Program、Pipeline”相关的操作。调用时要先确认当前状态和 `pipeline` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `pipeline`：类型为 `GLuint`。没有默认值，调用时必须提供。传入 `GLuint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLExtraFunctions::glVertexAttribBinding(GLuint attribindex, GLuint bindingindex)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLExtraFunctions::glVertexAttribBinding` 用于执行与“gl、Vertex、Attrib、Binding”相关的操作。调用时要先确认当前状态和 `attribindex`、`bindingindex` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `attribindex`：类型为 `GLuint`。没有默认值，调用时必须提供。传入 `GLuint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `bindingindex`：类型为 `GLuint`。没有默认值，调用时必须提供。传入 `GLuint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLExtraFunctions::glVertexAttribDivisor(GLuint index, GLuint divisor)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLExtraFunctions::glVertexAttribDivisor` 用于执行与“gl、Vertex、Attrib、Divisor”相关的操作。调用时要先确认当前状态和 `index`、`divisor` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `index`：类型为 `GLuint`。没有默认值，调用时必须提供。项目或数据索引。先确认索引基于 0 还是 1、是否允许越界/负数，以及调用后索引是否仍然有效。
- 参数 `divisor`：类型为 `GLuint`。没有默认值，调用时必须提供。传入 `GLuint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLExtraFunctions::glVertexAttribFormat(GLuint attribindex, GLint size, GLenum type, GLboolean normalized, GLuint relativeoffset)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLExtraFunctions::glVertexAttribFormat` 用于执行与“gl、Vertex、Attrib、格式化”相关的操作。调用时要先确认当前状态和 `attribindex`、`size`、`type`、`normalized`、`relativeoffset` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `attribindex`：类型为 `GLuint`。没有默认值，调用时必须提供。传入 `GLuint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `size`：类型为 `GLint`。没有默认值，调用时必须提供。尺寸或长度，单位通常是像素、字节、元素数或时间，必须结合类型和类的上下文确认。
- 参数 `type`：类型为 `GLenum`。没有默认值，调用时必须提供。类型、格式或策略枚举。要确认枚举值的适用范围和平台支持情况。
- 参数 `normalized`：类型为 `GLboolean`。没有默认值，调用时必须提供。传入 `GLboolean` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `relativeoffset`：类型为 `GLuint`。没有默认值，调用时必须提供。传入 `GLuint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLExtraFunctions::glVertexAttribI4i(GLuint index, GLint x, GLint y, GLint z, GLint w)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLExtraFunctions::glVertexAttribI4i` 用于执行与“gl、Vertex、Attrib、I、4、i”相关的操作。调用时要先确认当前状态和 `index`、`x`、`y`、`z`、`w` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `index`：类型为 `GLuint`。没有默认值，调用时必须提供。项目或数据索引。先确认索引基于 0 还是 1、是否允许越界/负数，以及调用后索引是否仍然有效。
- 参数 `x`：类型为 `GLint`。没有默认值，调用时必须提供。传入 `GLint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `y`：类型为 `GLint`。没有默认值，调用时必须提供。传入 `GLint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `z`：类型为 `GLint`。没有默认值，调用时必须提供。传入 `GLint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `w`：类型为 `GLint`。没有默认值，调用时必须提供。传入 `GLint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLExtraFunctions::glVertexAttribI4iv(GLuint index, const GLint *v)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLExtraFunctions::glVertexAttribI4iv` 用于执行与“gl、Vertex、Attrib、I、4、iv”相关的操作。调用时要先确认当前状态和 `index`、`v` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `index`：类型为 `GLuint`。没有默认值，调用时必须提供。项目或数据索引。先确认索引基于 0 还是 1、是否允许越界/负数，以及调用后索引是否仍然有效。
- 参数 `v`：类型为 `const GLint *`。没有默认值，调用时必须提供。传入 `const GLint *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLExtraFunctions::glVertexAttribI4ui(GLuint index, GLuint x, GLuint y, GLuint z, GLuint w)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLExtraFunctions::glVertexAttribI4ui` 用于执行与“gl、Vertex、Attrib、I、4、ui”相关的操作。调用时要先确认当前状态和 `index`、`x`、`y`、`z`、`w` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `index`：类型为 `GLuint`。没有默认值，调用时必须提供。项目或数据索引。先确认索引基于 0 还是 1、是否允许越界/负数，以及调用后索引是否仍然有效。
- 参数 `x`：类型为 `GLuint`。没有默认值，调用时必须提供。传入 `GLuint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `y`：类型为 `GLuint`。没有默认值，调用时必须提供。传入 `GLuint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `z`：类型为 `GLuint`。没有默认值，调用时必须提供。传入 `GLuint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `w`：类型为 `GLuint`。没有默认值，调用时必须提供。传入 `GLuint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLExtraFunctions::glVertexAttribI4uiv(GLuint index, const GLuint *v)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLExtraFunctions::glVertexAttribI4uiv` 用于执行与“gl、Vertex、Attrib、I、4、uiv”相关的操作。调用时要先确认当前状态和 `index`、`v` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `index`：类型为 `GLuint`。没有默认值，调用时必须提供。项目或数据索引。先确认索引基于 0 还是 1、是否允许越界/负数，以及调用后索引是否仍然有效。
- 参数 `v`：类型为 `const GLuint *`。没有默认值，调用时必须提供。传入 `const GLuint *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLExtraFunctions::glVertexAttribIFormat(GLuint attribindex, GLint size, GLenum type, GLuint relativeoffset)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLExtraFunctions::glVertexAttribIFormat` 用于执行与“gl、Vertex、Attrib、I、格式化”相关的操作。调用时要先确认当前状态和 `attribindex`、`size`、`type`、`relativeoffset` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `attribindex`：类型为 `GLuint`。没有默认值，调用时必须提供。传入 `GLuint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `size`：类型为 `GLint`。没有默认值，调用时必须提供。尺寸或长度，单位通常是像素、字节、元素数或时间，必须结合类型和类的上下文确认。
- 参数 `type`：类型为 `GLenum`。没有默认值，调用时必须提供。类型、格式或策略枚举。要确认枚举值的适用范围和平台支持情况。
- 参数 `relativeoffset`：类型为 `GLuint`。没有默认值，调用时必须提供。传入 `GLuint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLExtraFunctions::glVertexAttribIPointer(GLuint index, GLint size, GLenum type, GLsizei stride, const void *pointer)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLExtraFunctions::glVertexAttribIPointer` 用于执行与“gl、Vertex、Attrib、I、Pointer”相关的操作。调用时要先确认当前状态和 `index`、`size`、`type`、`stride`、`pointer` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `index`：类型为 `GLuint`。没有默认值，调用时必须提供。项目或数据索引。先确认索引基于 0 还是 1、是否允许越界/负数，以及调用后索引是否仍然有效。
- 参数 `size`：类型为 `GLint`。没有默认值，调用时必须提供。尺寸或长度，单位通常是像素、字节、元素数或时间，必须结合类型和类的上下文确认。
- 参数 `type`：类型为 `GLenum`。没有默认值，调用时必须提供。类型、格式或策略枚举。要确认枚举值的适用范围和平台支持情况。
- 参数 `stride`：类型为 `GLsizei`。没有默认值，调用时必须提供。传入 `GLsizei` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `pointer`：类型为 `const void *`。没有默认值，调用时必须提供。传入 `const void *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLExtraFunctions::glVertexBindingDivisor(GLuint bindingindex, GLuint divisor)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLExtraFunctions::glVertexBindingDivisor` 用于执行与“gl、Vertex、Binding、Divisor”相关的操作。调用时要先确认当前状态和 `bindingindex`、`divisor` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `bindingindex`：类型为 `GLuint`。没有默认值，调用时必须提供。传入 `GLuint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `divisor`：类型为 `GLuint`。没有默认值，调用时必须提供。传入 `GLuint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QOpenGLExtraFunctions::glWaitSync(GLsync sync, GLbitfield flags, GLuint64 timeout)`

**API 类别：** 成员函数说明

**中文解读：** `QOpenGLExtraFunctions::glWaitSync` 用于执行与“gl、等待、Sync”相关的操作。调用时要先确认当前状态和 `sync`、`flags`、`timeout` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `sync`：类型为 `GLsync`。没有默认值，调用时必须提供。传入 `GLsync` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `flags`：类型为 `GLbitfield`。没有默认值，调用时必须提供。标志位组合。可以用按位或组合，调用前确认哪些标志互斥、哪些标志需要同时出现。
- 参数 `timeout`：类型为 `GLuint64`。没有默认值，调用时必须提供。超时时间或超时对象，可能表示等待时长，也可能表示 QNetworkReply/QTimer 等异步对象，不能只看名称判断。

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

`QOpenGLExtraFunctions` 所属机制类型：Qt 类型机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
