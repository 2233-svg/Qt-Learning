# QOpenGLFunctions_3_1 类笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QOpenGLFunctions_3_1>`  
> 所属模块：`Qt6::OpenGL`  
> 继承：`QAbstractOpenGLFunctions`  
> 可用性：桌面 OpenGL 3.1 函数集；类保留兼容性继承成员，OpenGL 3.2+ Core profile 中不可使用其中的 deprecated 接口

## 它解决什么问题

`QOpenGLFunctions_3_1` 在 3.0 的 FBO、VAO 和 transform-feedback 基础上，提供 OpenGL 3.1 的关键资源与批量绘制能力：uniform buffer object 的反射和绑定、instanced draw、texture buffer、buffer-to-buffer copy 以及 primitive restart。

这几个功能共同解决了早期 shader renderer 的三个现实问题：一组共享参数不必重复写入每个 program 的普通 uniform；同一网格可被大量实例复用而无需重复 draw；GPU 数据可以在 buffer、texture 和 index stream 之间以更高效方式组织。它是 OpenGL 3.x Core 工作流真正开始成型的一步。

本类仍是桌面版本函数包装，而非自动资源管理框架。Qt 中可用 `QOpenGLBuffer` 等类承担对象生命周期，但 UBO block layout、binding point 分配、instance count、buffer range 对齐和 shader link 前后时序仍由调用者负责。

## 实际使用场景

- 将相机、光照或 per-frame 参数放入 UBO，由多个 shader program 共用；
- 用 `glDrawArraysInstanced()`/`glDrawElementsInstanced()` 绘制大量相同网格；
- 用 texture buffer 将大规模只读标量/查找数据暴露给 shader；
- 在 GPU 内复制 buffer 子段，或用 primitive restart 把多段 strip/fan 组织进一段 index buffer；
- 检查一个已链接 program 的 uniform block、成员 offset/stride 等反射信息。

## 初始化与最小示例

```cpp
#include <QOpenGLFunctions_3_1>

QOpenGLFunctions_3_1 gl;

void drawInstances(GLuint vao, GLsizei vertexCount, GLsizei instanceCount)
{
    gl.glBindVertexArray(vao);
    gl.glDrawArraysInstanced(GL_TRIANGLES, 0, vertexCount, instanceCount);
}
```

调用前必须成功执行 `initializeOpenGLFunctions()`，并让对应 context 在当前线程 current。实例化只重复同一组顶点输入；每个实例的不同数据仍需通过 instance attribute、uniform/UBO、texture buffer 或其他 shader 可见资源提供。

## 3.1 新增能力如何使用

### Uniform buffer object 与 program 反射

GLSL 的 `uniform BlockName { ... };` 会在 link 后形成 uniform block。用 `glGetUniformBlockIndex()` 找到 block index，查询 `glGetActiveUniformBlockiv()`/`glGetActiveUniformBlockName()` 获取 block 信息，再用 `glUniformBlockBinding()` 将该 block 关联到一个应用自行管理的 binding point。之后用 `glBindBufferBase()` 或 `glBindBufferRange()` 将 `GL_UNIFORM_BUFFER` 绑定到同一 binding point。

`glGetUniformIndices()`、`glGetActiveUniformsiv()`、`glGetActiveUniformName()` 用于从成员名称查询 uniform index 以及 `GL_UNIFORM_OFFSET`、array stride、matrix stride 等布局信息。不要凭 C++ struct 的自然 padding 猜测 UBO 布局；必须遵循 GLSL block layout，例如显式 `std140`，并按反射数据或严格的布局规则打包。

### Instanced draw

`glDrawArraysInstanced()` 和 `glDrawElementsInstanced()` 按同一顶点/索引范围重复绘制 `instancecount` 次。它们只提供“重复 draw”本身；3.3 前没有 core 的 `glVertexAttribDivisor()`，因此实例差异通常通过 `gl_InstanceID`、uniform 数组、texture buffer 或 transform feedback 数据建立，而不能假设通用 per-instance attribute divisor 已可用。

`glDrawElementsInstanced()` 的 indices 仍遵循 EBO 语义：绑定 `GL_ELEMENT_ARRAY_BUFFER` 时是字节 offset，否则是 CPU 指针。`instancecount` 为零时不会绘制；过大的实例数据访问会由 shader/resource 布局问题表现出来，而不是由 API 自动保护。

### Texture buffer 与 buffer copy

`glTexBuffer()` 将一个 buffer object 的存储附着到 `GL_TEXTURE_BUFFER`，让 shader 通过 buffer texture 访问。它适合大而只读、按元素索引的数据，例如调色板、实例参数或查找表；internal format 决定每个 texel 的解释。

`glCopyBufferSubData()` 在 `GL_COPY_READ_BUFFER` 与 `GL_COPY_WRITE_BUFFER` 或其他绑定 target 间复制 GPU buffer 子范围。源/目标 range 不能越界，重叠复制的行为也不应靠猜测；对于写入后立即被不同管线阶段读取的场景，仍需按 OpenGL 命令顺序和必要的同步规则设计。

### Primitive restart

启用 `GL_PRIMITIVE_RESTART` 后，索引流中的 restart index 会结束当前 strip/fan 并开始新 primitive；`glPrimitiveRestartIndex()` 设置该保留值。它能让多条 strip 共用一个 index buffer，减少 draw call。

restart 值必须不会与真实索引冲突，也必须能用当前 index type 表示。它不能替代理解 primitive mode，三角形列表等不需要自动分段的模式通常没有收益。

## 关键边界

### UBO 的 block index 和 binding point 不是同一个编号

block index 是某个 program link 后的内部标识；binding point 是应用层可跨 program 复用的槽位。正确流程是“program block index -> `glUniformBlockBinding` -> binding point -> `glBindBufferBase/Range`”，不要把两者直接当成相同整数。

### `glBindBufferRange()` 要满足范围与对齐约束

它绑定的 offset/size 必须在 buffer 范围内，并可能受 `GL_UNIFORM_BUFFER_OFFSET_ALIGNMENT` 限制。使用一个大环形 UBO 时，所有分片起始 offset 都要按该对齐值向上取整。

### 实例化减少 CPU draw 开销，不自动减少 shader 工作

若每个实例都执行昂贵 shader、产生大量过度绘制，实例化本身不会解决 GPU 瓶颈。应把它与 culling、批处理、LOD 和合理的实例数据读取策略结合。

### 类的 compatibility inheritance 仍不能在 Core path 中混用

3.1 新增功能可服务现代 Core 渲染，但本类还继承 1.x legacy 成员。编译通过不代表旧固定管线在 3.2+ Core context 可运行；应建立清晰的 Core-only 调用边界。

## API 速查表

| 功能族（成员 API） | 是做什么的 | 使用时重点注意 |
| --- | --- | --- |
| `initializeOpenGLFunctions()` | 为 current desktop OpenGL context 解析 3.1 与继承函数。 | context/profile 必须匹配；初始化失败后不得调用成员。 |
| `glGetUniformBlockIndex`, `glGetActiveUniformBlockiv`, `glGetActiveUniformBlockName` | 查询 program 中 uniform block 的 index、属性和名称。 | block index 只对该已链接 program 有效；buffer/字符串容量须足够。 |
| `glGetUniformIndices`, `glGetActiveUniformsiv`, `glGetActiveUniformName` | 查询 block 内 uniform 的 index、offset、stride、类型和名称。 | 用反射结果或标准布局打包，不能猜 struct padding。 |
| `glUniformBlockBinding` | 将 program 的 uniform block 指到应用选择的 binding point。 | block index 与 binding point 不同；调用后还要绑定实际 UBO。 |
| `glBindBufferBase`, `glBindBufferRange` | 把 buffer 的完整存储或指定范围绑定到 indexed target。 | 对 `GL_UNIFORM_BUFFER` 的 range offset 要满足对齐要求。 |
| `glDrawArraysInstanced`, `glDrawElementsInstanced` | 重复绘制同一顶点/索引范围若干实例。 | 实例差异数据仍要由 shader/resources 提供；索引指针遵循 EBO offset 语义。 |
| `glTexBuffer` | 让 buffer object 作为 `GL_TEXTURE_BUFFER` 的存储。 | internal format 决定 texel 解释；buffer texture 适合大规模索引读取数据。 |
| `glCopyBufferSubData` | 在两个 buffer binding target 间复制子范围。 | read/write offset 与 size 必须有效；避免依赖重叠 range 行为。 |
| `glPrimitiveRestartIndex` | 设置 primitive restart 的保留 index 值。 | 须启用 `GL_PRIMITIVE_RESTART`；值不得与真实索引冲突。 |
| 继承的 3.0 FBO/VAO：`glGenFramebuffers`, `glBindFramebuffer`, `glCheckFramebufferStatus`, `glFramebufferTexture*`, `glRenderbufferStorage*`, `glBlitFramebuffer`, `glGenVertexArrays`, `glBindVertexArray`, `glMapBufferRange`, `glFlushMappedBufferRange` | 离屏目标、VAO 和细粒度 buffer 映射。 | FBO 完整后仍要匹配 viewport/outputs；VAO 不拥有 VBO。 |
| 继承的 3.0 shader data flow：`glBeginTransformFeedback`, `glEndTransformFeedback`, `glTransformFeedbackVaryings`, `glGetTransformFeedbackVarying`, `glVertexAttribIPointer`, `glUniform*ui`, `glTexParameterI*`, `glClearBuffer*`, `glColorMaski`, `glEnablei` | transform feedback、整数 attribute/uniform 和 indexed state。 | varyings 要在 link 前设置；整数类型必须使用匹配的输入/clear API。 |
| 继承的 2.1/2.0：`glCreateShader`, `glCompileShader`, `glLinkProgram`, `glUseProgram`, `glVertexAttribPointer`, `glUniform*`, `glUniformMatrix*x*fv`, `glDrawBuffers`, `glBlend*Separate`, `glStencil*Separate` | 基础 GLSL、顶点输入、uniform 与多目标输出。 | program/link 和 buffer layout 必须检查；uniform location 不跨 program。 |
| 继承的 1.x 资源与 compatibility：`glGenBuffers`, `glBufferData`, `glMapBuffer`, `glGenQueries`, `glActiveTexture`, `glTexImage*`, `glDrawArrays`, `glDrawElements`, `glMatrixMode`, `glBegin`, `glEnd`, `glLight*`, `glTexEnv*` | buffer/query/texture 与旧 fixed-function 调用。 | legacy 成员不用于 Core/ES；查询和读回避免阻塞热路径。 |

## 常见误区

### 把 uniform block index 当作全局 binding point

不同 program 对同名 block 的内部 index 可能不同。要用各自的 index 调用 `glUniformBlockBinding()`，但让它们都映射到同一个应用定义的 binding point，才可以共享一个 UBO。

### UBO C++ 结构体看起来对齐，实际却不符合 `std140`

`vec3`、矩阵数组和结构体嵌套都容易触发额外 padding。用反射验证 offset，或采用经过严格 `std140` 对齐设计的显式字段，避免仅靠 `sizeof` 判断。

### 以为 3.1 实例化已经支持任意 per-instance attribute

draw instanced 只是重复 draw。`glVertexAttribDivisor()` 是 OpenGL 3.3 的能力；在 3.1 最低版本目标上，实例数据传递策略必须另行设计。

## 一句话总结

`QOpenGLFunctions_3_1` 把 UBO、实例化、texture buffer 与 primitive restart 引入 Qt 的版本化桌面 GL 调用中；它适合建立可批处理的数据路径，但最大的坑是混淆 program block index、binding point、buffer range 对齐和实例数据来源。
