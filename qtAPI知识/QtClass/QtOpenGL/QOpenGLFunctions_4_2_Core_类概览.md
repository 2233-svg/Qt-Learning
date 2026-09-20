# QOpenGLFunctions_4_2_Core 类笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QOpenGLFunctions_4_2_Core>`  
> 所属模块：`Qt6::OpenGL`  
> 继承：`QAbstractOpenGLFunctions`  
> 可用性：桌面 OpenGL 4.2 Core profile；不包含 Compatibility/fixed-function API

## 它解决什么问题

`QOpenGLFunctions_4_2_Core` 为 Qt 程序提供 OpenGL 4.2 Core profile 的函数入口。4.2 的核心是让 shader 与纹理/内存资源更直接地协作：immutable texture storage、image load/store、memory barrier、atomic counter 查询、base-instance 绘制和 transform-feedback instanced draw 都成为 core 能力。

这类函数适合已经拥有 4.x Core 渲染架构的项目：资源生命周期清晰，shader 使用 image/atomic/SSBO 前的同步概念也能被明确管理。它不适合只想“多几个 texture API”的简单渲染器；一旦使用 image load/store，就必须认真处理内存可见性和访问顺序。

## 实际使用场景

- 用 `glTexStorage*()` 一次性分配完整 mipmap 链，避免后续重新定义纹理格式；
- 在 shader 中通过 image unit 随机读写纹理或进行 unordered 写入；
- 使用 memory barrier 明确 shader 写入何时对后续采样、image、buffer 或 framebuffer 操作可见；
- 利用 base-instance 将实例 ID 与实例数据数组偏移解耦；
- 查询 internal format 能力，按驱动支持选择渲染目标或 image format。

## 初始化与最小示例

```cpp
#include <QOpenGLFunctions_4_2_Core>

QOpenGLFunctions_4_2_Core gl;

bool allocateImmutableTexture(GLuint texture, int width, int height)
{
    if (!gl.initializeOpenGLFunctions())
        return false;

    gl.glBindTexture(GL_TEXTURE_2D, texture);
    gl.glTexStorage2D(GL_TEXTURE_2D, 1, GL_RGBA8, width, height);
    return true;
}
```

`glTexStorage*()` 分配后，纹理的层级数、尺寸和 internal format 不能再用 `glTexImage*()` 重新定义；只能用 `glTexSubImage*()` 更新内容。这个不可变性正是它减少错误和驱动重新分配的价值。

## 4.2 Core 的关键能力

### Immutable texture storage

`glTexStorage1D()`、`glTexStorage2D()`、`glTexStorage3D()` 一次性定义指定 target 的全部 mip level 存储。相比逐级 `glTexImage*()`，它让纹理格式和层级在创建期固定，便于驱动优化，也避免“某个 level 没定义导致纹理不完整”的老问题。

levels 必须与实际 mip 需求匹配；尺寸会按 mip 链规则逐级缩小。分配后不能改 internal format，因此纹理创建参数要在资源系统中提前确定。

### Image unit 与 memory barrier

`glBindImageTexture()` 将 texture level/layer 绑定到 image unit，shader 可通过 image load/store/atomic 访问。`glMemoryBarrier()` 指定前面 shader 写入对后续哪些类型的读取/写入可见。

这是 4.2 最容易出错的部分。image access 的 `GL_READ_ONLY`、`GL_WRITE_ONLY`、`GL_READ_WRITE` 和 format 要与 shader 中的 image uniform 声明一致。写入后若马上采样、读取 image、作为 vertex 数据或 framebuffer 使用，必须选择正确 barrier bit；过少会读到旧数据，过多会降低并行度。

### Atomic counter 查询

`glGetActiveAtomicCounterBufferiv()` 查询 program 中 atomic counter buffer 的绑定、大小、活跃计数器数量等信息。atomic counter 适合计数、分配索引或统计，但不是通用随机写数据结构的替代品。

多 shader invocation 对同一 counter 的竞争会影响性能。需要更丰富的数据结构时，通常要结合 image load/store 或后续版本的 shader storage buffer。

### Base-instance 和 transform feedback instanced draw

`glDrawArraysInstancedBaseInstance()`、`glDrawElementsInstancedBaseInstance()`、`glDrawElementsInstancedBaseVertexBaseInstance()` 让实例绘制带有 `baseinstance`，shader 中的 `gl_InstanceID` 仍从 0 开始，但 instanced attribute 读取会加上 base instance 偏移。它非常适合把多个批次实例数据放在同一个 buffer 中。

`glDrawTransformFeedbackInstanced()` 和 `glDrawTransformFeedbackStreamInstanced()` 则按捕获的 transform feedback 顶点数做实例化绘制。使用前要确保 transform feedback 对象捕获完成，且 primitive mode 匹配。

### Internal format 查询

`glGetInternalformativ()` 查询某种 internal format 在某 target 下的支持、样本数或其他能力。它适合在启动或资源选择阶段做 capability probing，而不是每帧调用。

## 关键边界

### Barrier 是 API 语义的一部分

使用 image store、atomic 或 shader 写入后，不写 barrier 往往不是“偶尔慢”，而是数据可见性未定义。将 barrier 写在资源流转边界，而不是事后靠 `glFinish()` 掩盖问题。

### Image format 必须与 shader 声明一致

`glBindImageTexture()` 的 format 与 GLSL `layout(rgba8, binding=...) uniform image2D` 等声明不一致，会导致错误或未定义结果。资源系统应集中管理 image format。

### Immutable storage 不能重定义

如果资源尺寸或格式要变化，应删除/重建 texture，或另建新对象，而不是尝试对已 immutable 的纹理重新 `glTexImage*()`。

## API 速查表

| 功能族（成员 API） | 是做什么的 | 使用时重点注意 |
| --- | --- | --- |
| `initializeOpenGLFunctions()` | 解析 current OpenGL 4.2 Core profile 函数。 | context 版本/profile 必须匹配；失败后不能调用成员。 |
| `glTexStorage1D`, `glTexStorage2D`, `glTexStorage3D` | 一次性分配不可变纹理存储。 | 分配后不能重定义格式/层级；内容用 `glTexSubImage*` 更新。 |
| `glBindImageTexture` | 将 texture level/layer 绑定到 image unit 供 shader image 访问。 | access 和 format 要匹配 shader image uniform 声明。 |
| `glMemoryBarrier` | 声明 shader/image/buffer/framebuffer 等写入对后续操作可见。 | 按资源流转选择 barrier bit；不要用 `glFinish` 替代。 |
| `glGetActiveAtomicCounterBufferiv` | 查询 program 中 atomic counter buffer 的属性。 | program link 后查询；counter 竞争会影响性能。 |
| `glGetInternalformativ` | 查询 internal format 在 target 上的能力。 | 适合初始化/选择资源格式；不要放入热路径。 |
| `glDrawArraysInstancedBaseInstance`, `glDrawElementsInstancedBaseInstance`, `glDrawElementsInstancedBaseVertexBaseInstance` | 带 base instance 的实例化绘制。 | instanced attribute 偏移受 baseinstance 影响；indices 仍遵守 EBO offset 语义。 |
| `glDrawTransformFeedbackInstanced`, `glDrawTransformFeedbackStreamInstanced` | 按 transform feedback 捕获结果进行实例化绘制。 | 捕获对象必须完成且 primitive mode 匹配。 |
| 继承的 4.1：`glGenProgramPipelines`, `glUseProgramStages`, `glProgramUniform*`, `glViewportArrayv`, `glScissorArrayv`, `glDepthRangeArrayv`, `glProgramBinary`, `glVertexAttribLPointer` | Program pipeline、direct uniform、多 viewport、program binary 和 double attribute。 | pipeline interface、uniform location 和 binary cache 边界要管理清楚。 |
| 继承的 4.0/3.x：`glPatchParameter*`, `glDraw*Indirect`, `glBlend*i`, `glGenSamplers`, `glVertexAttribDivisor`, `glFenceSync`, `glUniformBlockBinding`, `glBindVertexArray`, `glBindFramebuffer`, `glMapBufferRange` | tessellation、indirect draw、sampler、instancing、sync、UBO、VAO/FBO。 | 状态和资源同步仍由调用者负责。 |

## 常见误区

### image store 后直接采样同一纹理

需要 `glMemoryBarrier(GL_TEXTURE_FETCH_BARRIER_BIT)` 或适合下一步访问类型的 barrier。没有 barrier 时读到旧内容并不奇怪。

### 以为 `glTexStorage2D()` 后还能换格式

immutable storage 的格式不可变。需要新格式就创建新 texture object。

### 把 base instance 当作 `gl_InstanceID` 初值

`gl_InstanceID` 仍从 0 开始；base instance 影响 instanced attribute 的索引推进。需要 shader 中知道全局实例编号时，要自己传入或用其他机制计算。

## 一句话总结

`QOpenGLFunctions_4_2_Core` 把不可变纹理、image load/store、memory barrier 和 base-instance 绘制纳入 Qt 的 Core GL 入口；它让 GPU 侧读写更强大，也要求你把资源可见性和格式契约写得更明确。
