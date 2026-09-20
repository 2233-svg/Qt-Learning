# QOpenGLFunctions_ES2 类笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QOpenGLFunctions_ES2>`  
> 所属模块：`Qt6::OpenGL`  
> 继承：`QAbstractOpenGLFunctions`  
> 定位：OpenGL ES 2.0 函数入口包装

## 它解决什么问题

`QOpenGLFunctions_ES2` 把 OpenGL ES 2.0 的函数集合包装成一个 Qt 类，让代码通过成员函数调用 ES 2.0 API，而不是直接依赖平台上的函数指针、扩展加载器或头文件宏。它本身不管理 shader、buffer、texture 或 framebuffer；它解决的是“在当前 Qt OpenGL context 中安全取得并调用一组确定版本的函数”。

它适合需要明确以 OpenGL ES 2.0 为目标的代码：移动端、嵌入式、WebAssembly、ANGLE，或者希望 desktop OpenGL 与 ES 后端共享渲染路径的项目。和 `QOpenGLFunctions` 相比，它的能力边界更明确：只暴露 ES 2.0 函数，不把更新版本、桌面 profile 或扩展 API 混进来。

## 实际使用场景

- 写一个只依赖 ES 2.0 的渲染器，在 `QOpenGLWidget::initializeGL()` 中初始化函数，然后在 `paintGL()` 里调用；
- 跨 Windows/ANGLE、Linux Mesa、移动 GPU 时，避免手写函数指针加载和条件编译；
- 为旧设备或保守图形管线维护一套 shader-based renderer；
- 在库代码中显式声明“只需要 ES 2.0”，让调用方更容易判断平台兼容性。

## 初始化与最小示例

```cpp
#include <QOpenGLFunctions_ES2>
#include <QOpenGLWidget>

class View : public QOpenGLWidget, protected QOpenGLFunctions_ES2
{
    void initializeGL() override
    {
        initializeOpenGLFunctions();
        glClearColor(0.08f, 0.09f, 0.11f, 1.0f);
    }

    void paintGL() override
    {
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
    }
};
```

`initializeOpenGLFunctions()` 必须在目标 `QOpenGLContext` 已经 current 之后调用。若对象会在多个 context 间复用，不要假设一次初始化能覆盖所有 context；OpenGL 函数解析和资源生命周期都要按实际 current context 处理。

## 核心使用模型

### 它是函数表，不是资源对象

`QOpenGLFunctions_ES2` 只提供 `gl*` 成员函数。它不会记住你的 VAO、VBO、纹理、program，也不会自动恢复 OpenGL 状态。调用成员函数后，改变的是当前 context 的 OpenGL 状态。

### 它对应 ES 2.0 能力边界

ES 2.0 没有固定管线，也没有 geometry/tessellation/compute shader、SSBO、debug output、direct state access、多数不可变存储和现代同步工具。典型工作流是：编译 vertex/fragment shader，绑定 attribute/uniform，上传 buffer/texture，然后发 draw call。

### 它仍受 Qt context 生命周期约束

所有调用都依赖当前线程有 current 的 `QOpenGLContext`。在 `QOpenGLWidget` 中通常放在 `initializeGL()`、`resizeGL()`、`paintGL()`；在 `QOpenGLWindow` 或手写 surface 中，需要自己调用 `makeCurrent()`。

## 关键 API 语义与边界

### 初始化

`initializeOpenGLFunctions()` 来自 `QAbstractOpenGLFunctions`，负责把当前 context 中 ES 2.0 函数解析到对象内部。返回 `false` 表示当前 context 不满足需求或函数解析失败；失败后继续调用 `gl*` 成员没有意义。

### Shader 与 program

ES 2.0 只支持 vertex shader 和 fragment shader。相关成员包括 `glCreateShader()`、`glShaderSource()`、`glCompileShader()`、`glGetShaderiv()`、`glCreateProgram()`、`glAttachShader()`、`glLinkProgram()`、`glUseProgram()`。编译和链接失败需要读取 info log，而不是只看 OpenGL 错误码。

### Buffer、attribute 与 draw

`glGenBuffers()`、`glBindBuffer()`、`glBufferData()` 管理 buffer；`glVertexAttribPointer()` 描述 attribute 布局；`glEnableVertexAttribArray()` 启用 attribute；`glDrawArrays()` 和 `glDrawElements()` 发起绘制。ES 2.0 没有 Core profile 那种标准 VAO 作为基础能力，因此 attribute 状态通常更容易被其他绘制代码污染。

### Texture 与 framebuffer

`glTexImage2D()`、`glTexSubImage2D()`、`glTexParameteri()` 配置 2D/cubemap 纹理；`glGenFramebuffers()`、`glFramebufferTexture2D()`、`glCheckFramebufferStatus()` 构建离屏渲染目标。ES 2.0 对纹理格式、NPOT 纹理、mipmap 和 wrap mode 的限制比现代桌面 OpenGL 更保守，遇到黑屏要优先查 format/filter/wrap 组合。

### 状态查询与错误处理

`glGetError()` 只能告诉你 OpenGL 错误状态，不会解释 shader 编译、program 链接或 framebuffer completeness 的具体原因。实际排查要结合 `glGetShaderInfoLog()`、`glGetProgramInfoLog()`、`glCheckFramebufferStatus()` 和平台调试输出。

## API 速查表

| 功能族（成员 API） | 是做什么的 | 使用时重点注意 |
| --- | --- | --- |
| `initializeOpenGLFunctions()` | 解析当前 context 的 ES 2.0 函数入口。 | 必须在 context current 后调用；返回 `false` 时不要继续调用 `gl*` 成员。 |
| Shader：`glCreateShader`, `glShaderSource`, `glCompileShader`, `glGetShaderiv`, `glGetShaderInfoLog`, `glDeleteShader` | 创建、编译、查询和释放 vertex/fragment shader。 | ES 2.0 只覆盖 vertex/fragment；失败原因看 info log。 |
| Program：`glCreateProgram`, `glAttachShader`, `glBindAttribLocation`, `glLinkProgram`, `glUseProgram`, `glGetProgramiv`, `glGetProgramInfoLog`, `glDeleteProgram` | 把 shader 链接成可用 program 并绑定到管线。 | `glBindAttribLocation()` 要在 link 前；link 后 uniform/attribute 位置可能变化。 |
| Uniform/attribute：`glGetUniformLocation`, `glUniform*`, `glGetAttribLocation`, `glVertexAttribPointer`, `glEnableVertexAttribArray`, `glDisableVertexAttribArray` | 向 shader 传参并描述顶点输入。 | `-1` 表示变量无效或被优化掉；attribute 指针解释依赖当前绑定的 array buffer。 |
| Buffer：`glGenBuffers`, `glBindBuffer`, `glBufferData`, `glBufferSubData`, `glDeleteBuffers` | 管理顶点/索引数据存储。 | ES 2.0 只有有限 target；更新策略要避免频繁同步。 |
| Texture：`glGenTextures`, `glBindTexture`, `glTexImage2D`, `glTexSubImage2D`, `glTexParameteri`, `glGenerateMipmap`, `glActiveTexture`, `glDeleteTextures` | 创建、上传、采样和释放纹理。 | NPOT、mipmap、wrap mode 和格式组合是常见兼容性边界。 |
| Framebuffer/renderbuffer：`glGenFramebuffers`, `glBindFramebuffer`, `glFramebufferTexture2D`, `glCheckFramebufferStatus`, `glGenRenderbuffers`, `glRenderbufferStorage`, `glDeleteFramebuffers`, `glDeleteRenderbuffers` | 构建离屏渲染目标和深度/模板附件。 | 附件后必须检查 completeness；尺寸、格式、采样配置要一致。 |
| Render state：`glViewport`, `glScissor`, `glEnable`, `glDisable`, `glBlendFunc`, `glDepthFunc`, `glCullFace`, `glColorMask`, `glDepthMask`, `glStencil*` | 控制当前 context 的渲染状态。 | 状态是全局的；库代码应显式设置自己依赖的状态。 |
| Draw/clear/read：`glClear`, `glClearColor`, `glClearDepthf`, `glDrawArrays`, `glDrawElements`, `glReadPixels`, `glFlush`, `glFinish` | 清屏、绘制、读回和提交命令。 | `glReadPixels()`/`glFinish()` 可能强制同步 GPU。 |
| Query/error：`glGetError`, `glGetString`, `glGetIntegerv`, `glIs*` | 查询错误、能力和对象状态。 | 错误码只说明 API 层错误；shader/FBO 需要各自的专用 log/status。 |

## 常见误区

### 把 ES2 当作桌面 OpenGL 2.0

二者相近但并不等价。ES 2.0 删除了固定管线，并且纹理格式、扩展、精度限定符和默认 framebuffer 行为都有平台差异。

### 初始化时没有 current context

`QOpenGLFunctions_ES2` 不是全局静态函数库。初始化和调用都以当前线程的 current context 为准，在构造函数里直接初始化通常太早。

### 依赖“别人留下的状态”

ES 2.0 状态量很多，尤其是 bound program、active texture unit、array buffer、element array buffer、blend/depth/scissor。可维护的渲染代码应在每个 pass 明确设置关键状态。

## 一句话总结

`QOpenGLFunctions_ES2` 是 Qt 提供的 OpenGL ES 2.0 函数表；它让跨平台调用变稳，但资源、状态、同步和兼容性仍然要由渲染器自己管理。
