# QOpenGLFunctions_3_3_Core 类笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QOpenGLFunctions_3_3_Core>`  
> 所属模块：`Qt6::OpenGL`  
> 继承：`QAbstractOpenGLFunctions`  
> 可用性：桌面 OpenGL 3.3 Core profile；不包含 fixed-function、立即模式、display list 或 client-side legacy API

## 它解决什么问题

`QOpenGLFunctions_3_3_Core` 为 Qt 程序提供 OpenGL 3.3 Core profile 的版本化函数入口。3.3 Core 是许多跨平台桌面 OpenGL renderer 的常见最低目标：它已经具备 VAO/VBO、FBO、UBO、实例化、sampler object、timer query、base-vertex draw、sync fence 和明确的 shader 管线，同时剥离了旧 fixed-function 状态机。

这个类解决的是“在 Qt 中建立一个足够现代、又比 4.x 更容易覆盖旧硬件的 Core 渲染后端”。与 `QOpenGLFunctions` 的通用 ES2 风格接口相比，它暴露更多桌面 3.x 资源控制；与 Compatibility 版本相比，它能把错误的 legacy 调用排除在结构之外。

## 实际使用场景

- 建立以 OpenGL 3.3 Core 为最低要求的桌面渲染器；
- 用 `glVertexAttribDivisor()` 实现 per-instance attribute；
- 用 sampler object 将采样状态从 texture object 中拆出来复用；
- 用 `glQueryCounter()` 和 64 位 query result 做 GPU 时间戳；
- 用 dual-source blending、packed vertex attribute 或 base-vertex draw 优化现有数据流。

## 初始化与最小示例

```cpp
#include <QOpenGLFunctions_3_3_Core>

QOpenGLFunctions_3_3_Core gl;

bool initializeRenderer()
{
    if (!gl.initializeOpenGLFunctions())
        return false;

    GLuint sampler = 0;
    gl.glGenSamplers(1, &sampler);
    gl.glSamplerParameteri(sampler, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR);
    gl.glSamplerParameteri(sampler, GL_TEXTURE_MAG_FILTER, GL_LINEAR);
    gl.glBindSampler(0, sampler);
    return true;
}
```

调用前要让匹配的 OpenGL 3.3 Core context 在当前线程 current。若应用通过 `QSurfaceFormat` 请求了 Compatibility profile 或低版本 context，本类初始化可能失败。

## 3.3 Core 的关键能力

### Sampler object

`glGenSamplers()`、`glBindSampler()`、`glSamplerParameter*()` 和 `glGetSamplerParameter*()` 将 wrap、filter、compare mode、LOD 等采样状态从 texture object 中独立出来。一个 texture 存储可以在不同 draw 中配合不同 sampler 使用，例如同一阴影图一处做 depth compare，另一处调试显示原始深度。

sampler 绑定到 texture unit，而不是 texture object。shader sampler uniform 仍然写逻辑 unit 编号；`glBindTexture()` 提供数据，`glBindSampler()` 提供采样规则。解绑 sampler 后会回到 texture object 自身的采样参数。

### Instanced attribute divisor

`glVertexAttribDivisor(index, divisor)` 让某个 vertex attribute 按实例而不是按顶点推进。`divisor = 1` 是最常见的 per-instance 数据；更大的值表示每 N 个实例推进一次。它与 `glDrawArraysInstanced()`、`glDrawElementsInstanced()` 配合，构成 3.3 Core 中完整的实例化数据路径。

divisor 状态属于当前 VAO 中的 attribute 配置。若切换 VAO 后实例数据错乱，先检查该 attribute 是否启用、pointer 是否指向实例 buffer、divisor 是否随 VAO 保存。

### Timer query 与 64 位 query result

`glQueryCounter(id, GL_TIMESTAMP)` 在命令流中插入 GPU 时间戳；`glGetQueryObjecti64v()`/`glGetQueryObjectui64v()` 读取 64 位结果。它比 CPU 计时更接近 GPU 实际执行顺序，适合做渲染 pass 性能分析。

不要刚插入 timestamp 就读取 `GL_QUERY_RESULT`。先查询可用性，或延迟几帧读取，否则计时工具本身会把 GPU/CPU 强行同步，结果失真。

### Packed attribute 与 dual-source blending

`glVertexAttribP*()` 允许把打包格式数据作为 generic attribute 设置，适合压缩颜色、法线或小向量。`glBindFragDataLocationIndexed()` 与 `glGetFragDataIndex()` 服务 dual-source blending：一个 fragment shader 输出可以带 color index 和 source index，供特殊混合公式使用。

打包属性的 type、normalized 和 shader 输入类型必须匹配；dual-source blending 受实现可用输出数量限制，也会影响 fragment output 布局设计。

## Core 边界

### 3.3 Core 是现代管线，不是“兼容所有桌面 GL”

它不提供 fixed-function fallback。所有几何必须通过 buffer/VAO/attribute，所有变换和材质逻辑必须进 shader，所有离屏路径都要显式管理 FBO 和 attachment。

### Sampler 与 texture unit 是两层状态

同一个 unit 同时有 texture binding 和 sampler binding。排查“贴图数据正确但过滤/wrap 不对”时，要同时检查两者；删除 sampler 前也要确保不再绑定使用。

### Timer query 是异步工具

正确用法通常是双缓冲或环形 query 对象，下一帧/几帧后读回。把它放进每个 draw 后立即读取，会造成大面积同步。

## API 速查表

| 功能族（成员 API） | 是做什么的 | 使用时重点注意 |
| --- | --- | --- |
| `initializeOpenGLFunctions()` | 解析 current OpenGL 3.3 Core profile 函数。 | context 必须版本/profile 匹配；失败后不得调用成员。 |
| `glGenSamplers`, `glDeleteSamplers`, `glIsSampler`, `glBindSampler` | 创建、删除、检查并将 sampler object 绑定到 texture unit。 | sampler 绑定的是 unit；texture 数据仍由 `glBindTexture` 提供。 |
| `glSamplerParameteri`, `glSamplerParameteriv`, `glSamplerParameterf`, `glSamplerParameterfv`, `glSamplerParameterIiv`, `glSamplerParameterIuiv`, `glGetSamplerParameteriv`, `glGetSamplerParameterfv`, `glGetSamplerParameterIiv`, `glGetSamplerParameterIuiv` | 设置/查询 sampler 的过滤、wrap、LOD、compare 等采样状态。 | 参数类型要匹配；解绑 sampler 后回到 texture object 参数。 |
| `glVertexAttribDivisor` | 设置 attribute 按实例推进的频率。 | 状态随 VAO 保存；配合 instanced draw 和实例 buffer 使用。 |
| `glQueryCounter`, `glGetQueryObjecti64v`, `glGetQueryObjectui64v` | 插入 GPU 时间戳并读取 64 位 query 结果。 | 延迟读取，避免 `GL_QUERY_RESULT` 立即同步。 |
| `glVertexAttribP1ui`, `glVertexAttribP2ui`, `glVertexAttribP3ui`, `glVertexAttribP4ui`, `glVertexAttribP1uiv`, `glVertexAttribP2uiv`, `glVertexAttribP3uiv`, `glVertexAttribP4uiv` | 以 packed integer 格式设置当前 generic attribute 值。 | type/normalized 要与打包格式和 shader 输入匹配。 |
| `glBindFragDataLocationIndexed`, `glGetFragDataIndex` | 绑定或查询 fragment output 的 color number 和 index。 | 主要用于 dual-source blending；在 program link 前绑定。 |
| 继承的 3.2：`glTexImage2DMultisample`, `glTexImage3DMultisample`, `glFenceSync`, `glClientWaitSync`, `glWaitSync`, `glDrawElementsBaseVertex`, `glDrawElementsInstancedBaseVertex`, `glFramebufferTexture`, `glProvokingVertex` | MSAA texture、sync fence、base-vertex draw 与通用 FBO attachment。 | MSAA 需 resolve 或显式 fetch；fence 避免无限等待。 |
| 继承的 3.1：`glDrawArraysInstanced`, `glDrawElementsInstanced`, `glTexBuffer`, `glCopyBufferSubData`, `glPrimitiveRestartIndex`, `glGetUniformBlockIndex`, `glUniformBlockBinding`, `glBindBufferBase`, `glBindBufferRange` | 实例化绘制、buffer texture、UBO 与 GPU buffer copy。 | UBO range 有对齐要求；3.3 divisor 才补齐 per-instance attribute。 |
| 继承的 3.0：`glGenVertexArrays`, `glBindVertexArray`, `glGenFramebuffers`, `glBindFramebuffer`, `glBlitFramebuffer`, `glMapBufferRange`, `glBeginTransformFeedback`, `glVertexAttribIPointer`, `glClearBuffer*` | VAO/FBO、精细 buffer 映射、transform feedback、整数属性。 | Core draw 依赖 VAO；FBO status、viewport 和 draw buffers 都要匹配。 |
| 继承的 2.x/1.x Core：`glCreateShader`, `glCompileShader`, `glLinkProgram`, `glUseProgram`, `glVertexAttribPointer`, `glUniform*`, `glGenBuffers`, `glBufferData`, `glBindTexture`, `glTexImage*`, `glDrawArrays`, `glDrawElements`, `glViewport`, `glClear*` | GLSL、buffer、texture 与基础绘制状态。 | 无 legacy fixed-function；所有材质/矩阵/光照逻辑由 shader 明确实现。 |

## 常见误区

### 绑定了 sampler，却忘了设置 shader sampler uniform

sampler object 只决定采样规则，不决定 shader 读哪个 unit。uniform 仍要写 `0`、`1` 这类 texture unit 编号。

### `glVertexAttribDivisor()` 配好了，但换 VAO 后消失

divisor 是 VAO 记录的 attribute 状态。每个 VAO 都需要在初始化时设置对应 attribute pointer、enable 和 divisor。

### 用 timer query 读到了“很慢”的假结果

如果每个 timestamp 之后马上读结果，慢的是同步等待。把结果延迟几帧读取，才能得到可用的 GPU 时间线数据。

## 一句话总结

`QOpenGLFunctions_3_3_Core` 是 Qt 中很实用的现代桌面 OpenGL 基线：sampler object、attribute divisor 和 timer query 让资源复用、实例化与性能测量都更完整，同时 Core profile 强制你远离旧状态机。
