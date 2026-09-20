# QOpenGLFunctions_2_0 类笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QOpenGLFunctions_2_0>`  
> 所属模块：`Qt6::OpenGL`  
> 继承：`QAbstractOpenGLFunctions`  
> 可用性：桌面 OpenGL 2.0 compatibility API；Qt 以 OpenGL ES 2 构建时不可用，且其继承的 legacy 成员不适用于 Core-only context

## 它解决什么问题

`QOpenGLFunctions_2_0` 把 OpenGL 2.0 与此前版本的函数地址装配成依赖 current `QOpenGLContext` 的成员函数。OpenGL 2.0 的真正分水岭是可编程着色器：应用可以创建 vertex/fragment shader、编译并链接 program、声明 vertex attribute、设置 uniform，而不是完全依赖矩阵栈、固定光照与纹理环境。

这使它成为旧 OpenGL 代码由 fixed-function 向 programmable pipeline 迁移时很有价值的版本函数类。它仍继承 1.x 的大量 compatibility 接口，所以不能把“对象能初始化”误解成“所有成员都适合现代 profile”；程序应当选择 shader/attribute 路径，逐步停止使用立即模式、client state 和固定管线状态。

Qt 中较高层的常用组合是 `QOpenGLShaderProgram` 管理 shader/program，`QOpenGLBuffer` 管理 buffer，`QOpenGLVertexArrayObject` 管理顶点状态。本类适用于需要直接控制原始 GL 语义、维护 C 风格渲染器，或理解这些高层类底层行为时。

## 实际使用场景

- 将旧的 `glMatrixMode()`、`glLight*()`、`glTexEnv*()` 渐进替换为 shader uniform；
- 手工编译和诊断 GLSL，读取编译日志/链接日志；
- 在一个 program 中定义 vertex attribute 布局，并以 VBO 数据驱动绘制；
- 配置 MRT、分离 RGB/Alpha 混合方程或双面不同 stencil state 的传统 deferred/合成路径。

## 初始化与最小示例

```cpp
#include <QOpenGLFunctions_2_0>

QOpenGLFunctions_2_0 gl;

bool initializeProgram()
{
    if (!gl.initializeOpenGLFunctions())
        return false;

    const char *source = R"(
        attribute vec3 position;
        void main() { gl_Position = vec4(position, 1.0); }
    )";

    const GLuint shader = gl.glCreateShader(GL_VERTEX_SHADER);
    gl.glShaderSource(shader, 1, &source, nullptr);
    gl.glCompileShader(shader);
    return true;
}
```

示例只展示调用顺序。生产代码必须检查 `GL_COMPILE_STATUS`、`GL_LINK_STATUS`，在失败时读取 info log，并在不再需要时删除 shader/program。初始化、编译、链接和 draw 都要求相同或共享的 OpenGL context 在当前线程 current。

## 2.0 新增能力如何使用

### Shader 与 program 生命周期

典型顺序是：`glCreateShader()` -> `glShaderSource()` -> `glCompileShader()` -> 检查 shader 状态；再 `glCreateProgram()` -> `glAttachShader()` -> 可选 `glBindAttribLocation()` -> `glLinkProgram()` -> 检查 program 状态 -> `glUseProgram()`。链接成功后可 `glDetachShader()` 和 `glDeleteShader()`；已链接的 program 会保留所需编译结果。

`glShaderSource()` 的 `length` 为 null 时，源字符串必须以 NUL 结尾；传入多个字符串时，`count`、指针数组和可选长度数组必须对应。日志缓冲区先通过 `GL_INFO_LOG_LENGTH` 查询尺寸，避免截断真正的失败原因。

### Attribute 与 VBO 数据布局

`glGetAttribLocation()` 查询链接后 attribute 的位置，或在链接前用 `glBindAttribLocation()` 固定名称到 index。`glVertexAttribPointer()` 定义 index 对应的格式、stride、normalization 和数据起点，`glEnableVertexAttribArray()` 启用该数组。

这里的 `pointer` 具有 buffer 语义：绑定 `GL_ARRAY_BUFFER` 时是 VBO 内字节偏移；没有绑定时才是 CPU 地址。shader attribute 位置并不是数组自动启用的，忘记 `glEnableVertexAttribArray()` 或将布局与 GLSL 类型不匹配，常会造成全零、错位或随机顶点数据。

### Uniform

`glGetUniformLocation()` 获取已链接、未被编译器优化掉的 uniform 位置；`glUniform*()` 和 `glUniformMatrix*()` 为当前 `glUseProgram()` 选中的 program 写值。location 为 `-1` 时，按规范写入会被忽略，常见原因是名称不存在或该 uniform 未参与最终程序。

sampler uniform 的值是纹理单元编号 `0`、`1`、`2`，不是 `GL_TEXTURE0` 枚举值。矩阵函数的 `transpose` 在桌面 GL 可用，但跨桌面/ES 的代码应统一使用 column-major 上传约定并传 `GL_FALSE`。

### 独立输出、混合和 stencil

`glDrawBuffers()` 为多个颜色输出选择目标 buffer；`glBlendEquationSeparate()` 分别设置 RGB/Alpha 的组合方程；`glStencilFuncSeparate()`、`glStencilMaskSeparate()`、`glStencilOpSeparate()` 为前/背面配置不同 stencil state。它们用于多 render target、复杂合成和阴影体等路径。

实际可用的输出数量与 framebuffer/driver 限制有关。使用 MRT 时，fragment shader 输出、`glDrawBuffers()` 数组和绑定 framebuffer 的 color attachment 必须彼此对应；仅配置函数调用并不会自动创建 FBO 附件。

## 关键边界

### GLSL 编译成功不代表 program 可用

shader 可单独编译成功，但在 link 时因 varying/interface、attribute 绑定、版本或资源限制而失败。调用 `glValidateProgram()` 只能用于检查“在当前 state 下是否可执行”，不能取代 compile/link 状态检查，也不应放在每帧路径。

### Program 与 uniform state 绑定当前 context

`glUseProgram()` 改变 current context 的状态。uniform 写入的是当前使用的 program；切换 program 后同一 location 通常没有相同含义。缓存 location 时要以 program 为键，relink 后必须重新查询。

### 2.0 的 shader 不等于今天的 Core 设计

OpenGL 2.0 已支持 programmable shader，但本类仍含 compatibility inheritance。它没有现代 VAO、UBO、instancing、transform feedback 等后续资源模型。新项目要么使用更高的 Core profile 函数类，要么用 `QOpenGLFunctions`/`QOpenGLExtraFunctions` 建立与目标平台匹配的能力层。

## API 速查表

下表先列出 2.0 的全部新增操作族，再归纳 1.x 继承成员。数值类型和向量/数组重载合并在同一行，以保留真实语义而不把 API 表拆成重复列表。

| 功能族（成员 API） | 是做什么的 | 使用时重点注意 |
| --- | --- | --- |
| `initializeOpenGLFunctions()` | 为 current desktop context 解析 2.0 与继承函数。 | 先确认 context/profile；失败后不能调用成员。 |
| `glCreateShader`, `glDeleteShader`, `glIsShader`, `glShaderSource`, `glCompileShader`, `glGetShaderiv`, `glGetShaderInfoLog`, `glGetShaderSource` | 创建、提供源码、编译、查询和删除 shader。 | 检查 `GL_COMPILE_STATUS`；源码长度、日志缓冲区和 shader 生命周期都要明确。 |
| `glCreateProgram`, `glDeleteProgram`, `glIsProgram`, `glAttachShader`, `glDetachShader`, `glLinkProgram`, `glUseProgram`, `glValidateProgram`, `glGetProgramiv`, `glGetProgramInfoLog`, `glGetAttachedShaders` | 组装、链接、使用、验证和检查 program。 | 检查 `GL_LINK_STATUS`；`glValidateProgram` 不是 per-frame 检查；uniform 属当前 program。 |
| `glBindAttribLocation`, `glGetAttribLocation` | 在 link 前绑定或在 link 后查询 attribute 位置。 | 手工绑定必须在 `glLinkProgram` 前；relink 后 location 可能改变。 |
| `glVertexAttribPointer`, `glEnableVertexAttribArray`, `glDisableVertexAttribArray`, `glGetVertexAttrib*`, `glGetVertexAttribPointerv` | 定义、启用和查询通用顶点 attribute 数组。 | VBO 绑定时 pointer 是字节 offset；布局、stride、normalized 必须匹配 shader 输入。 |
| `glGetUniformLocation`, `glGetActiveUniform`, `glGetUniformfv`, `glGetUniformiv` | 查询 uniform 的位置、活动信息和当前值。 | 位置只对对应 program 有效；未使用 uniform 可能得到 `-1`。 |
| `glUniform1f`, `glUniform2f`, `glUniform3f`, `glUniform4f`, `glUniform1i`, `glUniform2i`, `glUniform3i`, `glUniform4i`, `glUniform1fv`, `glUniform2fv`, `glUniform3fv`, `glUniform4fv`, `glUniform1iv`, `glUniform2iv`, `glUniform3iv`, `glUniform4iv`, `glUniformMatrix2fv`, `glUniformMatrix3fv`, `glUniformMatrix4fv` | 为当前 program 设置标量、向量、数组和方阵 uniform。 | 先 `glUseProgram`；sampler 写 unit 编号而非 `GL_TEXTURE0`；矩阵布局要统一。 |
| `glDrawBuffers` | 指定多个颜色输出写入哪些 draw buffer。 | 输出数组须与绑定 framebuffer 的 attachment 和 shader output 对齐。 |
| `glBlendEquationSeparate` | 独立设置 RGB 和 Alpha 的混合方程。 | 仍需启用 blending；与 `glBlendFuncSeparate` 和颜色格式一起验证。 |
| `glStencilFuncSeparate`, `glStencilMaskSeparate`, `glStencilOpSeparate` | 分别设置前/背面 stencil 比较、写掩码和操作。 | face、ref、mask 与 depth/stencil attachment 格式必须正确。 |
| 继承的 1.5 资源：`glGenBuffers`, `glDeleteBuffers`, `glBindBuffer`, `glBufferData`, `glBufferSubData`, `glMapBuffer`, `glUnmapBuffer`, `glGetBuffer*`, `glGenQueries`, `glBeginQuery`, `glEndQuery`, `glGetQuery*` | 管理 VBO/EBO 和异步 query。 | buffer pointer/offset 语义取决于 binding；立即取 query result 可能阻塞。 |
| 继承的 1.4--1.2：`glMultiDraw*`, `glBlendFuncSeparate`, `glPointParameter*`, `glActiveTexture`, `glCompressedTex*`, `glTexImage3D`, `glBlendColor`, `glBlendEquation`, `glColorTable*`, `glConvolution*`, `glHistogram*`, `glMinmax*` | 多批绘制、纹理单元、压缩/3D 纹理和历史 imaging 功能。 | imaging/fixed-function 支持仅限 compatibility；纹理上传受 pixel-store state 影响。 |
| 继承的 1.1--1.0 legacy：`glDrawArrays`, `glDrawElements`, `glVertexPointer`, `glEnableClientState`, `glMatrixMode`, `glBegin`, `glEnd`, `glLight*`, `glMaterial*`, `glTexEnv*`, `glTexGen*`, `glNewList`, `glCallList*` | 旧顶点数组、固定管线和 display list 等。 | 不适用于 Core/ES；迁移时优先改为 shader + VBO/VAO。 |

## 常见误区

### 编译完成后不检查 link log

顶点和片段 shader 可以各自通过编译，却在链接阶段发现 interface 或资源冲突。必须分别检查 compile 与 link status，并保留完整 info log。

### 把 sampler uniform 写成 `GL_TEXTURE0`

sampler 要的是逻辑单元索引，例如 `0`；`GL_TEXTURE0` 是传给 `glActiveTexture()` 的枚举常量。两者混用会让 shader 去读取不存在的纹理单元。

### 在无 VBO 绑定和有 VBO 绑定之间切换，却不改 attribute pointer

同一个参数在两种状态下分别代表地址和 offset。应把 VAO/布局设置集中管理，不要让 draw 代码依赖不透明的历史 binding。

## 一句话总结

`QOpenGLFunctions_2_0` 是 Qt 中承接早期 GLSL 的版本函数入口：它让 shader、program、attribute 和 uniform 进入旧渲染器，但可靠使用的关键是严格管理 compile/link、program state、VBO offset 和 compatibility API 的退出边界。
