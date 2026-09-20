# QOpenGLFunctions

> Qt 6.11.1 · Qt GUI · 来自 `QOpenGLFunctions`

## 1. 先建立直觉

`QOpenGLFunctions` 是 Qt 提供的基础 OpenGL 函数入口集合。它把一组在桌面 OpenGL 和 OpenGL ES 之间较常用、较可移植的函数解析成可调用成员，避免你直接处理平台函数指针差异。

它不是 OpenGL 教程，也不是状态管理器。调用 `glBindBuffer()`、`glUseProgram()`、`glDrawArrays()` 等函数后，改变的是当前 OpenGL 上下文的状态；Qt 不会替你恢复、检查或解释这些状态。

## 2. 类说明

- 头文件：`#include <QOpenGLFunctions>`
- CMake：`target_link_libraries(mytarget PRIVATE Qt6::Gui)`
- 派生：`QOpenGLExtraFunctions`
- 获取方式：常用 `QOpenGLContext::functions()`，也可构造后调用 `initializeOpenGLFunctions()`。

函数对象与初始化时的 context 或共享组相关。使用前必须保证对应 context 或共享 context 在当前线程中 current。

## 3. API 速查

| API / 函数组 | 用途 |
|---|---|
| `QOpenGLFunctions()` | 创建未绑定上下文的函数对象，需要初始化。 |
| `QOpenGLFunctions(context)` | 绑定到指定 context 或当前 context 的函数对象。 |
| `initializeOpenGLFunctions()` | 在当前 context 下解析函数入口。 |
| `openGLFeatures()` / `hasOpenGLFeature()` | 查询 Qt 归纳的功能集合。 |
| `glClear*`、`glColorMask`、`glDepth*`、`glStencil*` | 清屏、颜色/深度/模板状态。 |
| `glViewport`、`glScissor` | 设置视口和裁剪区域。 |
| `glEnable` / `glDisable` / `glIsEnabled` | 开关 GL 功能状态。 |
| `glGen*`、`glDelete*`、`glIs*` | 生成、删除、验证纹理/缓冲/FBO/RBO/Shader/Program。 |
| `glBindTexture`、`glTexImage2D`、`glTexSubImage2D`、`glTexParameter*` | 2D 纹理创建、更新与采样参数。 |
| `glBindBuffer`、`glBufferData`、`glBufferSubData` | 顶点/索引缓冲数据管理。 |
| `glCreateShader`、`glShaderSource`、`glCompileShader` | 着色器对象创建与编译。 |
| `glCreateProgram`、`glAttachShader`、`glLinkProgram`、`glUseProgram` | Program 链接与使用。 |
| `glGetShaderiv`、`glGetShaderInfoLog`、`glGetProgramiv`、`glGetProgramInfoLog` | 编译/链接错误诊断。 |
| `glGetUniformLocation`、`glUniform*`、`glUniformMatrix*` | Uniform 查询与上传。 |
| `glVertexAttribPointer`、`glEnableVertexAttribArray`、`glVertexAttrib*` | 顶点属性布局与输入。 |
| `glDrawArrays`、`glDrawElements` | 发起绘制。 |
| `glBindFramebuffer`、`glFramebufferTexture2D`、`glCheckFramebufferStatus` | FBO 绑定、附件和完整性检查。 |
| `glReadPixels` | 从 framebuffer 读回像素。 |
| `glGetError`、`glGetString`、`glGet*` | 错误、字符串和状态查询。 |

## 4. 关键用法

### 从当前 context 取得函数入口

```cpp
if (context->makeCurrent(window)) {
    QOpenGLFunctions *gl = context->functions();
    gl->glViewport(0, 0, window->width(), window->height());
    gl->glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
}
```

通过 `QOpenGLContext::functions()` 得到的对象已经初始化，不需要再调用 `initializeOpenGLFunctions()`。如果你自己持有 `QOpenGLFunctions` 成员，则必须在 context current 后初始化。

### 编译着色器时要查日志

```cpp
GLuint shader = gl->glCreateShader(GL_VERTEX_SHADER);
gl->glShaderSource(shader, 1, &source, nullptr);
gl->glCompileShader(shader);

GLint ok = GL_FALSE;
gl->glGetShaderiv(shader, GL_COMPILE_STATUS, &ok);
if (!ok) {
    char log[2048] = {};
    gl->glGetShaderInfoLog(shader, sizeof(log), nullptr, log);
}
```

这些函数只是 OpenGL 调用入口，不会把 GL 错误转换成 C++ 异常。着色器、program、FBO、纹理上传等关键步骤都应显式检查状态。

### 绑定默认 framebuffer

`QOpenGLFunctions::glBindFramebuffer()` 对传入 0 有 Qt 适配：它会绑定当前 context 的 `defaultFramebufferObject()`。这让 `QOpenGLWidget`、移动平台和普通窗口代码更一致。

## 5. 功能枚举速查

| Feature | 说明 |
|---|---|
| `Multitexture` | `glActiveTexture()` 等多纹理单元。 |
| `Shaders` | 可编译/链接 shader program。 |
| `Buffers` | VBO/IBO 等 buffer object。 |
| `Framebuffers` | FBO 与 renderbuffer。 |
| `BlendColor` / `BlendEquation*` / `BlendFuncSeparate` | 高级混合控制。 |
| `CompressedTextures` | 压缩纹理上传。 |
| `Multisample` | 多重采样相关能力。 |
| `StencilSeparate` | 正反面模板状态分离。 |
| `NPOTTextures` / `NPOTTextureRepeat` | 非 2 次幂纹理及重复寻址。 |
| `FixedFunctionPipeline` | 固定管线是否可用，核心 profile 常不可用。 |
| `TextureRGFormats` | `GL_RED` / `GL_RG` 格式。 |
| `MultipleRenderTargets` | 多颜色附件渲染。 |

## 6. 常见坑与经验

- 每个函数都要求正确 context 在当前线程 current；函数对象存在不代表 GL 状态可用。
- `QOpenGLFunctions` 覆盖的是基础集合，不等于当前驱动支持的全部 GL API。更高版本功能用版本化函数类或 `QOpenGLExtraFunctions`。
- `hasOpenGLFeature()` 是 Qt 的功能摘要；精确判断某个扩展或核心版本仍应查 context 版本和扩展。
- OpenGL 对象名是当前上下文/共享组的资源，跨不共享 context 使用会失败。
- `glGetError()` 只能告诉你 GL 错误队列，不会指出是哪一行；调试时配合 debug output 更有效。
- 指针参数生命周期由调用的 GL 函数语义决定。上传函数通常复制数据，顶点指针在 VBO 未绑定时可能引用客户端内存，需格外小心。

## 7. 知识点覆盖

- Qt OpenGL 函数解析与 current context
- 纹理、缓冲、着色器、program、FBO、绘制调用
- 基础功能枚举和运行时能力查询
- 默认 framebuffer 的 Qt 适配
- GL 状态机、错误检查和共享组资源边界
