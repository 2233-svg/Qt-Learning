# QOpenGLFunctions_4_4_Core 类笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QOpenGLFunctions_4_4_Core>`  
> 所属模块：`Qt6::OpenGL`  
> 继承：`QAbstractOpenGLFunctions`  
> 可用性：桌面 OpenGL 4.4 Core profile；不包含 Compatibility/fixed-function API

## 它解决什么问题

`QOpenGLFunctions_4_4_Core` 为 Qt 程序提供 OpenGL 4.4 Core profile 的版本化函数入口。4.4 的核心不是扩展 shader 语言，而是让资源分配与绑定更适合高吞吐渲染：`glBufferStorage()` 提供不可变 buffer 存储和持久映射基础，`glClearTexImage()` 可直接初始化纹理内容，multi-bind API 可成批设置资源绑定点。

这组能力解决的是传统 OpenGL 中两个常见瓶颈：频繁 map/unmap 或重分配 buffer 造成同步，以及绘制前逐个调用 `glBindTexture()`、`glBindSampler()`、`glBindBufferRange()` 产生大量 CPU 驱动调用。它适合已有 Core 资源管理层的 renderer，不是为小型单 draw 程序增加复杂度。

## 实际使用场景

- 为每帧更新的 vertex/instance/indirect command 数据建立持久映射环形 buffer；
- 在创建 render target 后直接将整个 texture 或某个 subimage 清为初值；
- 一次性绑定一组 UBO/SSBO、纹理、sampler、image unit 或 vertex buffer；
- 将 render graph 中某个 pass 的资源绑定从大量小调用收束成几个批量调用；
- 在 GPU-driven renderer 中降低命令准备阶段的 CPU 开销。

## 初始化与最小示例

```cpp
#include <QOpenGLFunctions_4_4_Core>

QOpenGLFunctions_4_4_Core gl;

bool allocateStaticBuffer(GLsizeiptr bytes)
{
    if (!gl.initializeOpenGLFunctions())
        return false;

    GLuint buffer = 0;
    gl.glGenBuffers(1, &buffer);
    gl.glBindBuffer(GL_ARRAY_BUFFER, buffer);
    gl.glBufferStorage(GL_ARRAY_BUFFER, bytes, nullptr, GL_DYNAMIC_STORAGE_BIT);
    return true;
}
```

`glBufferStorage()` 创建的是不可变存储。它不能用 `glBufferData()` 重新分配；之后可以按创建 flags 决定是否允许 `glBufferSubData()`、映射、持久映射或 coherent mapping。

## 4.4 Core 的关键能力

### Immutable buffer storage

`glBufferStorage(target, size, data, flags)` 为当前绑定 target 的 buffer 一次性分配不可变存储。`GL_DYNAMIC_STORAGE_BIT` 允许后续 `glBufferSubData()` 更新；`GL_MAP_READ_BIT`、`GL_MAP_WRITE_BIT` 控制映射权限；`GL_MAP_PERSISTENT_BIT` 允许映射指针跨多个 GL 调用持续存在；`GL_MAP_COHERENT_BIT` 使某些 CPU 写入自动对 GPU 可见。

持久映射并不会自动解决并发。CPU 不能覆盖 GPU 尚在读取的 ring-buffer 区段；需要用 fence、帧延迟或显式分段管理。非 coherent 映射还可能需要 `glFlushMappedBufferRange()`，并依赖创建时的 `GL_MAP_FLUSH_EXPLICIT_BIT`。

### Clear texture

`glClearTexImage()` 清空一个完整 mip level，`glClearTexSubImage()` 清空指定子区域。它们避免了为清零纹理创建临时 FBO 或上传大块 CPU 数据，适合初始化 tile、volume texture、纹理池和部分延迟渲染资源。

`format`、`type` 与 `data` 描述传入的单个 clear value；`data = nullptr` 代表对应分量为零。它们必须与 texture 的 internal format 和目标清除语义兼容。清除后的结果若立即被 shader/image 访问，仍按后续访问路径处理可见性。

### Multi-bind

`glBindBuffersBase()`、`glBindBuffersRange()` 批量绑定 UBO、SSBO、atomic counter 等 indexed buffer target。`glBindTextures()`、`glBindSamplers()`、`glBindImageTextures()` 批量绑定 texture unit 的对象；`glBindVertexBuffers()` 批量配置 VAO 的 vertex buffer binding。

这些 API 主要减少调用数量，不会推断资源用途。数组中每一项都要与相应 target/index 合法匹配；传 0 通常解除对应绑定。用 multi-bind 前最好让资源表按 binding slot 连续布局，避免为了批量绑定而制造更复杂的槽位映射。

## 关键边界

### 不可变 storage 是生命周期约束

创建后不能靠 `glBufferData()` 改大小或 flags。资源重建路径要显式创建新 buffer，旧 buffer 的销毁要等到 GPU 不再使用它。

### Persistent mapping 需要同步设计

持久指针的有效性不等于内容何时可安全覆盖。必须为每块 ring segment 建立 fence 或足够的帧延迟策略，不能每帧重写同一个仍在飞行的区域。

### Multi-bind 不会替你绑定 program 或更新 uniform

它只批量修改资源绑定状态。shader 仍需使用相应 binding layout 或由应用设置正确的 binding point；texture unit 与 sampler uniform 的关系也仍需保持一致。

## API 速查表

| 功能族（成员 API） | 是做什么的 | 使用时重点注意 |
| --- | --- | --- |
| `initializeOpenGLFunctions()` | 解析 current OpenGL 4.4 Core profile 函数。 | context 版本/profile 必须匹配；失败后不得调用成员。 |
| `glBufferStorage` | 为当前 buffer target 分配不可变存储，并指定映射/更新 flags。 | 之后不能用 `glBufferData` 重定义；persistent/coherent mapping 仍需同步管理。 |
| `glClearTexImage` | 用一个 clear value 初始化完整 texture mip level。 | format/type/data 必须与内部格式兼容；`nullptr` 为零值。 |
| `glClearTexSubImage` | 清空 texture 指定 level 的子区域。 | offset/extent 不可越界；层、深度和压缩格式限制要匹配。 |
| `glBindBuffersBase`, `glBindBuffersRange` | 批量绑定完整 buffer 或 buffer range 到 indexed target。 | target、slot、offset、size 和对齐要求必须全部正确。 |
| `glBindTextures`, `glBindSamplers`, `glBindImageTextures` | 批量绑定 texture、sampler 或 image texture 到连续 unit。 | texture data、sampler state、image access/format 仍是独立契约。 |
| `glBindVertexBuffers` | 批量设置 VAO 的 vertex buffer binding、offset 和 stride。 | binding index 不等于 attribute location；attribute-to-binding 映射须已配置。 |
| 继承的 4.3：`glDispatchCompute`, `glShaderStorageBlockBinding`, `glMemoryBarrier`, `glMultiDraw*Indirect`, `glBindVertexBuffer`, `glVertexAttrib*Format`, `glTextureView`, `glCopyImageSubData`, `glInvalidate*`, `glDebugMessage*`, `glObjectLabel` | compute/SSBO、GPU-driven draw、分离顶点绑定、资源视图和调试工具。 | 按资源流转插入正确 barrier；VAO 状态与资源生命周期要集中管理。 |
| 继承的 4.2/4.1/4.0：`glTexStorage*`, `glBindImageTexture`, `glProgramUniform*`, `glGenProgramPipelines`, `glPatchParameter*`, `glDraw*Indirect`, `glGenSamplers`, `glFenceSync` | 不可变纹理、image、program pipeline、tessellation、indirect draw、sampler 与 sync。 | 不同资源模型的 binding 与同步边界不能混淆。 |
| 继承的 3.x Core：`glBindVertexArray`, `glBindFramebuffer`, `glBufferData`, `glMapBufferRange`, `glUniformBlockBinding`, `glCreateShader`, `glUseProgram`, `glDrawArrays`, `glDrawElements` | VAO/FBO、buffer、GLSL 和基础绘制。 | Core 路径没有 fixed-function fallback；状态均属于 current context。 |

## 常见误区

### 持久映射后每帧覆盖同一段数据

即使写入不崩溃，GPU 也可能仍在读取旧内容。必须分段并以 fence 或帧序控制复用时机。

### 用 `glClearTexImage()` 清纹理后立刻把它当 image 或 sampler 读取

清除是命令流的一部分，后续访问仍要遵守对应的可见性规则。按实际消费路径插入必要 barrier。

### 为了用 multi-bind 而让 binding slot 设计失去规律

批量调用只是优化手段。优先保持稳定、可读的资源槽位表，连续绑定只是其自然结果。

## 一句话总结

`QOpenGLFunctions_4_4_Core` 让 Qt 的 OpenGL 资源层更接近现代高吞吐工作方式：不可变 buffer、持久映射基础、直接纹理清零和 multi-bind 都能减少同步与调用开销，但前提是生命周期、fence 和 binding 表设计足够清晰。
