# QOpenGLFunctions_4_3_Core 类笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QOpenGLFunctions_4_3_Core>`  
> 所属模块：`Qt6::OpenGL`  
> 继承：`QAbstractOpenGLFunctions`  
> 可用性：桌面 OpenGL 4.3 Core profile；不包含 Compatibility/fixed-function API

## 它解决什么问题

`QOpenGLFunctions_4_3_Core` 为 Qt 程序提供 OpenGL 4.3 Core profile 的函数入口。4.3 是桌面 GL 中非常重要的一步：compute shader、shader storage buffer object、program resource 统一反射、multi-draw indirect、separate vertex attribute binding、texture view、copy image、buffer clear 和 invalidate 都进入 core。

它解决的是“让 GPU 不只负责传统 draw，而能承担计算、批量命令和复杂资源视图”的问题。使用它时，renderer 通常已经是完整 Core 架构：资源绑定点、内存 barrier、shader 反射、VAO 布局和调试工具都需要被系统化管理。

## 实际使用场景

- 用 compute shader 做粒子更新、光照列表、图像处理或 GPU culling；
- 用 SSBO 存储可变长或结构化数据，替代 UBO 的容量和布局限制；
- 通过 program resource API 统一查询 uniform、storage block、input/output 等反射信息；
- 使用 multi-draw indirect 批量提交 GPU/CPU 生成的 draw command；
- 用 texture view 和 copy image 在不同格式/层级视图之间复用存储或复制图像。

## 初始化与最小示例

```cpp
#include <QOpenGLFunctions_4_3_Core>

QOpenGLFunctions_4_3_Core gl;

void dispatchWork(GLuint groupsX, GLuint groupsY)
{
    gl.glDispatchCompute(groupsX, groupsY, 1);
    gl.glMemoryBarrier(GL_SHADER_STORAGE_BARRIER_BIT | GL_TEXTURE_FETCH_BARRIER_BIT);
}
```

Compute dispatch 后的 barrier 要按后续访问类型选择。示例中假设 compute 写了 SSBO，并且后续 pass 可能采样由 compute 影响的数据；真实代码应选择最窄但正确的 barrier bits。

## 4.3 Core 的关键能力

### Compute shader 与 SSBO

`glDispatchCompute()`/`glDispatchComputeIndirect()` 启动 compute shader work groups。`glShaderStorageBlockBinding()` 将 shader storage block 绑定到应用选择的 binding point；实际 buffer 仍通过继承的 `glBindBufferBase()`/`glBindBufferRange()` 绑定到 `GL_SHADER_STORAGE_BUFFER`。

SSBO 比 UBO 更大、更灵活，也允许 shader 写入，但这意味着你必须处理同步与竞争。写入后被 draw、compute、image、texture 或 CPU 读取时，都需要对应 barrier 或同步策略。

### Program resource reflection

`glGetProgramInterfaceiv()`、`glGetProgramResourceIndex()`、`glGetProgramResourceName()`、`glGetProgramResourceiv()`、`glGetProgramResourceLocation()`、`glGetProgramResourceLocationIndex()` 提供统一反射入口，用于查询 shader storage block、uniform block、program input/output 等资源。

这比早期分散的 `glGetActiveUniform*()` 更适合自动化 shader 绑定系统。查询结果仍只对当前 linked program 有效，relink 后必须刷新缓存。

### Multi-draw indirect

`glMultiDrawArraysIndirect()` 和 `glMultiDrawElementsIndirect()` 从一段 command buffer 连续读取多个 draw command。它是 GPU-driven rendering 的基础之一，常与 compute culling 和 indirect command 生成配合。

`stride` 为 0 表示命令紧密排列，否则是命令间字节跨度。命令格式必须逐字段符合规范；GPU 写完 command 后要用合适 barrier 让 indirect draw 可见。

### Separate vertex attribute binding

`glBindVertexBuffer()`、`glVertexAttribFormat()`、`glVertexAttribIFormat()`、`glVertexAttribLFormat()`、`glVertexAttribBinding()`、`glVertexBindingDivisor()` 将“attribute 格式”和“buffer binding”拆开。相比旧 `glVertexAttribPointer()`，这更利于多 mesh 复用布局、切换 buffer 和组织实例数据。

这些状态仍记录在 VAO 内。binding index、attribute index 和 relative offset 是三套不同概念，混淆后会出现顶点错读。

### Texture view、copy image、invalidate 与 buffer clear

`glTextureView()` 让一个 texture object 以不同 target/format/level/layer 视图引用另一个 texture 的存储。`glCopyImageSubData()` 在纹理/渲染缓冲图像间复制区域，不需要通过 framebuffer blit。`glInvalidate*()` 告诉驱动某些内容不再需要，减少 tile/带宽成本。`glClearBufferData()`/`glClearBufferSubData()` 用指定格式清空 buffer 内容。

这些都是资源系统工具。view 的 format compatibility、level/layer 范围，copy 的目标尺寸/格式，以及 invalidate 的时机都必须明确。

## 关键边界

### Compute shader 不自动同步图形管线

compute 写入后马上绘制使用同一数据时，barrier 是正确性条件。不同访问路径需要不同 barrier bit，不能只靠 draw 顺序。

### SSBO 灵活但不免费

随机写、原子操作和大量不连续访问会影响性能。SSBO 适合结构化大数据，不代表所有 uniform 都应迁移进去。

### Separate attribute binding 降低耦合，也增加索引层次

attribute location、binding index、buffer object、relative offset、stride 和 divisor 都要一起管理。建议用小型布局描述结构统一生成 VAO 状态。

## API 速查表

| 功能族（成员 API） | 是做什么的 | 使用时重点注意 |
| --- | --- | --- |
| `initializeOpenGLFunctions()` | 解析 current OpenGL 4.3 Core profile 函数。 | context 版本/profile 必须匹配；失败后不能调用成员。 |
| `glDispatchCompute`, `glDispatchComputeIndirect` | 启动 compute shader 工作组。 | 维度受实现限制；indirect 参数来自 buffer offset 时需保证可见性。 |
| `glShaderStorageBlockBinding` | 将 shader storage block 绑定到指定 binding point。 | 还要用 `glBindBufferBase/Range(GL_SHADER_STORAGE_BUFFER, ...)` 绑定实际 buffer。 |
| `glGetProgramInterfaceiv`, `glGetProgramResourceIndex`, `glGetProgramResourceName`, `glGetProgramResourceiv`, `glGetProgramResourceLocation`, `glGetProgramResourceLocationIndex` | 统一查询 program 资源反射信息。 | 结果只对 linked program 有效；relink 后刷新缓存。 |
| `glMultiDrawArraysIndirect`, `glMultiDrawElementsIndirect` | 从 indirect command buffer 批量提交多个 draw。 | command 布局、stride 和 barrier 必须正确。 |
| `glBindVertexBuffer`, `glVertexAttribFormat`, `glVertexAttribIFormat`, `glVertexAttribLFormat`, `glVertexAttribBinding`, `glVertexBindingDivisor` | 分离 attribute 格式与 vertex buffer binding。 | 状态属于 VAO；不要混淆 attribute index 与 binding index。 |
| `glTextureView`, `glCopyImageSubData` | 创建 texture storage 视图，或在 image 对象间复制区域。 | format compatibility、level/layer 范围和尺寸要合法。 |
| `glInvalidateTexImage`, `glInvalidateTexSubImage`, `glInvalidateBufferData`, `glInvalidateBufferSubData`, `glInvalidateFramebuffer`, `glInvalidateSubFramebuffer` | 声明资源内容不再需要。 | 只能在确实不会再读旧内容时使用。 |
| `glClearBufferData`, `glClearBufferSubData` | 按格式清空整个 buffer 或子范围。 | target 当前绑定的 buffer 有效；format/type/data 要匹配 internalformat。 |
| `glTexBufferRange`, `glTexStorage2DMultisample`, `glTexStorage3DMultisample`, `glFramebufferParameteri`, `glGetFramebufferParameteriv`, `glGetInternalformati64v` | buffer texture 子范围、多重采样不可变存储和 FBO/格式查询。 | range/format/样本数受实现限制。 |
| 继承的 4.2：`glTexStorage*`, `glBindImageTexture`, `glMemoryBarrier`, `glDraw*BaseInstance`, `glGetActiveAtomicCounterBufferiv` | 不可变纹理、image unit、barrier、base-instance 和 atomic counter 反射。 | image/SSBO 写入后按后续访问设置 barrier。 |
| 继承的 4.1/4.0/3.x：`glGenProgramPipelines`, `glProgramUniform*`, `glPatchParameter*`, `glDraw*Indirect`, `glGenSamplers`, `glVertexAttribDivisor`, `glFenceSync`, `glBindVertexArray`, `glBindFramebuffer` | pipeline、direct uniform、tessellation、indirect draw、sampler、instancing、sync、VAO/FBO。 | Core 状态仍需显式组织和验证。 |

## 常见误区

### compute 写了 SSBO，下一次 draw 直接读

需要 `glMemoryBarrier(GL_SHADER_STORAGE_BARRIER_BIT)` 或更精确的后续访问 barrier。没有 barrier 时，数据可见性未定义。

### 把 binding index 当 attribute location

`glVertexAttribBinding(attrib, binding)` 才建立二者关系。只绑定 vertex buffer 到某个 binding index，不会自动让 shader attribute 读取它。

### invalidate 了后面还要读的 attachment

invalidate 是告诉驱动旧内容可丢弃。若后面还依赖该内容，结果就不可靠。

## 一句话总结

`QOpenGLFunctions_4_3_Core` 让 Qt OpenGL renderer 进入 compute/SSBO/GPU-driven 绘制阶段；它的力量来自显式资源访问，而稳定性也取决于你是否正确管理反射、barrier 和顶点绑定层次。
