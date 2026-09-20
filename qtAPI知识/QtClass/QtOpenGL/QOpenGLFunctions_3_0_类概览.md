# QOpenGLFunctions_3_0 类笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QOpenGLFunctions_3_0>`  
> 所属模块：`Qt6::OpenGL`  
> 继承：`QAbstractOpenGLFunctions`  
> 可用性：桌面 OpenGL 3.0 函数集；类仍含兼容性成员，OpenGL 3.2+ Core profile 中不可使用其中的 deprecated 接口

## 它解决什么问题

`QOpenGLFunctions_3_0` 为 current `QOpenGLContext` 提供 OpenGL 3.0 及前代 API 的版本化成员包装。3.0 是现代桌面 OpenGL 资源与渲染工作流成形的重要节点：framebuffer object、renderbuffer、多重采样存储、VAO、映射 buffer range、整数 attribute/uniform、transform feedback 和 indexed state 都被纳入 core。

它解决的实际问题是把“离屏渲染、顶点布局、流式 buffer 更新、多渲染目标与 GPU 生成数据”的低层语义放在一个可初始化函数对象中。Qt 已为 FBO、buffer、VAO 提供较高层类，但直接使用该类能精确控制 attachment、同步和状态，也便于维护既有 OpenGL 代码。

注意：此类不是纯 Core wrapper。它同时保留前代 fixed-function/deprecated 函数，以服务 OpenGL 3.0 时代的兼容路径。若 context 是 3.2+ Core profile，应使用对应的 `QOpenGLFunctions_3_2_Core` 或更高版本 Core 类。

## 实际使用场景

- 创建 texture/renderbuffer attachment 的离屏 FBO，用于后处理、拾取、阴影或渲染到纹理；
- 使用 VAO 固化顶点 attribute 和 EBO 绑定，避免每次 draw 重设布局；
- 用 `glMapBufferRange()` 做受控的 buffer 子范围更新；
- 用 transform feedback 捕获顶点 shader 输出，或用 conditional render 利用先前 query 控制绘制；
- 为整数纹理、整数 vertex input 和无符号 uniform 建立正确的数据路径。

## 初始化与最小示例

```cpp
#include <QOpenGLFunctions_3_0>

QOpenGLFunctions_3_0 gl;

bool createRenderTarget(int width, int height)
{
    if (!gl.initializeOpenGLFunctions())
        return false;

    GLuint fbo = 0;
    GLuint depth = 0;
    gl.glGenFramebuffers(1, &fbo);
    gl.glBindFramebuffer(GL_FRAMEBUFFER, fbo);
    gl.glGenRenderbuffers(1, &depth);
    gl.glBindRenderbuffer(GL_RENDERBUFFER, depth);
    gl.glRenderbufferStorage(GL_RENDERBUFFER, GL_DEPTH24_STENCIL8, width, height);
    gl.glFramebufferRenderbuffer(GL_FRAMEBUFFER, GL_DEPTH_STENCIL_ATTACHMENT,
                                 GL_RENDERBUFFER, depth);
    return gl.glCheckFramebufferStatus(GL_FRAMEBUFFER) == GL_FRAMEBUFFER_COMPLETE;
}
```

这只是 attachment 流程的一部分，示例未附加 color texture。每次改变 attachment、尺寸或样本数后都应检查 FBO completeness；调用结束后还应恢复需要的 framebuffer/renderbuffer binding。

## 3.0 新增能力如何使用

### FBO、renderbuffer 与 multisample

`glGenFramebuffers()`/`glBindFramebuffer()` 管理 FBO，`glFramebufferTexture*()` 或 `glFramebufferRenderbuffer()` 连接 attachment，`glCheckFramebufferStatus()` 判断组合是否完整。renderbuffer 适合只作为渲染目标的深度、模板或颜色存储；texture attachment 可在后续 shader 中采样。

`glRenderbufferStorageMultisample()` 分配多重采样 renderbuffer，`glBlitFramebuffer()` 可在 read/draw framebuffer 之间复制或 resolve。多重采样颜色通常需要 resolve 到单采样 texture 后才能作为普通 sampler 输入；blit 的 filter、mask、坐标方向和源/目标格式都有约束。

### VAO 与顶点输入

`glGenVertexArrays()`、`glBindVertexArray()`、`glDeleteVertexArrays()` 将通用 vertex attribute 配置归档到 VAO。VAO 记录 attribute enable、format/pointer 以及 element array buffer 绑定，适合把“一个 mesh 的顶点布局”固定在初始化阶段。

VAO 不保存所有 OpenGL 状态，也不拥有 VBO 的内存。配置 `glVertexAttribPointer()` 时仍需正确绑定 `GL_ARRAY_BUFFER`；顶点 buffer 或 index buffer 被删除/换绑后，VAO 的语义依然要按对象生命周期和 binding 规则理解。

### Map range

`glMapBufferRange()` 只映射指定 offset/length，access flags 可声明读、写、invalidate、unsynchronized 或 explicit flush；`glFlushMappedBufferRange()` 仅对使用 `GL_MAP_FLUSH_EXPLICIT_BIT` 的映射范围提交修改。它比 1.5 的整块 `glMapBuffer()` 更适合流式更新。

`GL_MAP_UNSYNCHRONIZED_BIT` 不是性能魔法：它意味着应用自行保证不覆盖 GPU 尚在读取的数据。若不能证明生命周期，宁愿采用多 buffer、ring buffer 或让驱动同步。

### Transform feedback 与 conditional render

`glTransformFeedbackVaryings()` 必须在 `glLinkProgram()` 前声明要捕获的 varying；`glBeginTransformFeedback()`/`glEndTransformFeedback()` 在绘制时把 shader 输出写入绑定的 transform-feedback buffer。它适合旧式 GPU 粒子、几何变形或数据流更新。

`glBeginConditionalRender()`/`glEndConditionalRender()` 根据 query result 条件化后续绘制。它减少无意义 draw 的机会，但查询可用性与 GPU 异步仍要管理，不应刚结束 query 就在 CPU 端强行读取结果。

### 整数数据与 indexed state

整数 attribute 要使用 `glVertexAttribIPointer()`，不能用会做归一化/float 转换的 `glVertexAttribPointer()`；无符号 uniform 用 `glUniform*ui`/`glUniform*uiv`。`glTexParameterI*()` 则以整数形式设置/查询整型纹理参数。

`glEnablei()`、`glDisablei()`、`glIsEnabledi()`、`glColorMaski()` 和 indexed 查询函数为特定 draw buffer 等 indexed target 设置状态。它们不是“给任意 state 加数组下标”，必须使用规范允许的 target/index 组合。

## 关键边界

### FBO 完整不等于渲染结果正确

`GL_FRAMEBUFFER_COMPLETE` 只说明 attachment 组合可渲染，不保证 shader output 与 draw buffer 对应、viewport 已匹配实际尺寸，也不保证 color/depth/stencil 格式满足业务需求。离屏画面为空时，先检查 FBO status、viewport、draw buffers、clear 和 shader 输出。

### VAO 是状态容器，不是资源所有者

删除 VAO 不会删除关联 buffer；删除 buffer 也不等于自动修复已配置的 attribute。用 Qt 包装类或自定义 RAII 时，应让 VAO、VBO、EBO 的销毁都发生在可用的同一共享组 context 中。

### 变换反馈与普通绘制的状态不可随意交叉

开始 transform feedback 后 primitive mode 要符合要求，捕获目标 buffer 不能被冲突方式使用。需要重新使用被写入的数据时，应明确 buffer binding 与必要同步，避免读取未完成 GPU 写入。

### 3.0 仍处于 compatibility 过渡期

本类含 1.x legacy 成员。不要因为使用了 FBO 或 VAO，就继续混用 `glBegin()`、矩阵栈和 client state；混搭会使 renderer 难以迁移到 Core profile。

## API 速查表

下表按 3.0 新增操作族列出实际成员，并归纳继承能力。数值/指针变体合并说明，但每个 Qt 成员名称均在相应操作族中出现。

| 功能族（成员 API） | 是做什么的 | 使用时重点注意 |
| --- | --- | --- |
| `initializeOpenGLFunctions()` | 为 current desktop OpenGL context 解析 3.0 与继承函数。 | 先确认 context/profile；失败后不能调用成员。 |
| `glGenVertexArrays`, `glDeleteVertexArrays`, `glBindVertexArray`, `glIsVertexArray` | 创建、删除、绑定和检查 VAO。 | VAO 记录 attribute 与 EBO 绑定，不拥有 VBO；Core draw 通常需要有效 VAO。 |
| `glGenFramebuffers`, `glDeleteFramebuffers`, `glBindFramebuffer`, `glIsFramebuffer`, `glCheckFramebufferStatus` | 管理并验证 framebuffer object。 | attachment 修改后检查 status；read/draw/default framebuffer target 不要混淆。 |
| `glGenRenderbuffers`, `glDeleteRenderbuffers`, `glBindRenderbuffer`, `glIsRenderbuffer`, `glRenderbufferStorage`, `glRenderbufferStorageMultisample`, `glGetRenderbufferParameteriv` | 管理普通或多重采样 renderbuffer 存储。 | renderbuffer 不可直接采样；尺寸、format、samples 要与 FBO attachment 匹配。 |
| `glFramebufferTexture1D`, `glFramebufferTexture2D`, `glFramebufferTexture3D`, `glFramebufferTextureLayer`, `glFramebufferRenderbuffer`, `glGetFramebufferAttachmentParameteriv` | 将 texture layer 或 renderbuffer 连接到 FBO attachment。 | target/attachment/level/layer 必须有效；depth-stencil 格式与 attachment 点匹配。 |
| `glBlitFramebuffer`, `glGenerateMipmap` | FBO 间复制/resolve，或为绑定纹理生成 mipmap。 | blit 坐标和 filter 受格式限制；mipmap 需完整且 target 合法。 |
| `glMapBufferRange`, `glFlushMappedBufferRange` | 映射 buffer 子范围并按需显式 flush。 | access flags 决定承诺；unsynchronized/invalidate 需要应用保证数据安全。 |
| `glBeginTransformFeedback`, `glEndTransformFeedback`, `glBindBufferBase`, `glBindBufferRange`, `glTransformFeedbackVaryings`, `glGetTransformFeedbackVarying` | 配置并捕获 shader varying 到 buffer。 | varyings 必须在 link 前声明；begin/end 配对，buffer 绑定点和输出容量正确。 |
| `glBeginConditionalRender`, `glEndConditionalRender` | 根据 query result 条件控制 GPU 后续绘制。 | 依赖之前 query；不要为立即读取结果而破坏异步流水线。 |
| `glVertexAttribIPointer`, `glGetVertexAttribIiv`, `glGetVertexAttribIuiv` | 定义/查询整数顶点属性。 | 整数 shader input 用此接口；不要用普通 attrib pointer 做隐式数值转换。 |
| `glUniform1ui`, `glUniform2ui`, `glUniform3ui`, `glUniform4ui`, `glUniform1uiv`, `glUniform2uiv`, `glUniform3uiv`, `glUniform4uiv`, `glGetUniformuiv` | 设置或查询无符号整数 uniform。 | location 属当前 program；GLSL 类型必须是 `uint`/`uvec*` 等匹配类型。 |
| `glTexParameterIiv`, `glTexParameterIuiv`, `glGetTexParameterIiv`, `glGetTexParameterIuiv` | 设置/查询整数纹理参数。 | 面向整数语义参数；绑定正确 target 与 active unit。 |
| `glBindFragDataLocation`, `glGetFragDataLocation`, `glClearBufferiv`, `glClearBufferuiv`, `glClearBufferfv`, `glClearBufferfi` | 绑定/查询 fragment output location，或按类型清除指定缓冲。 | output binding 在 link 前设置；clear 类型要匹配 attachment 的整数/浮点格式。 |
| `glGetStringi`, `glColorMaski`, `glGetBooleani_v`, `glGetIntegeri_v`, `glEnablei`, `glDisablei`, `glIsEnabledi`, `glClampColor` | 枚举扩展并管理 indexed state 或颜色钳制。 | `glGetStringi` 结合 `GL_NUM_EXTENSIONS`；index/target 组合必须合法。 |
| 继承的 2.1/2.0：`glUniformMatrix*x*fv`, `glCreateShader`, `glCompileShader`, `glLinkProgram`, `glUseProgram`, `glVertexAttribPointer`, `glUniform*`, `glDrawBuffers`, `glBlendEquationSeparate`, `glStencil*Separate` | 非方阵矩阵、shader/program、普通 attribute/uniform 与多输出状态。 | 检查 compile/link log；program/location、VBO offset 和 FBO outputs 必须一致。 |
| 继承的 1.5--1.0：`glGenBuffers`, `glBufferData`, `glMapBuffer`, `glGenQueries`, `glActiveTexture`, `glTexImage*`, `glDrawArrays`, `glDrawElements`, `glMatrixMode`, `glBegin`, `glEnd`, `glLight*`, `glTexEnv*`, `glNewList` | buffer/query/texture 与早期 compatibility API。 | client/fixed-function 成员不能用于现代 Core/ES；查询/读回避免热路径。 |

## 常见误区

### 创建了 FBO 却忘记设 viewport

viewport 不会随着 FBO attachment 尺寸自动改变。后处理目标大小与窗口不同的时候，这是最常见的画面裁剪、空白或分辨率错位来源。

### 给整数 shader 输入使用 `glVertexAttribPointer()`

该接口会按 floating-point attribute 规则解释数据。GLSL `ivec*`/`uvec*` 输入必须使用 `glVertexAttribIPointer()`，否则 ID、骨骼索引或分类数据会失真。

### `GL_MAP_UNSYNCHRONIZED_BIT` 后重写正在被 GPU 读取的区域

该 flag 只是取消驱动替你等待，不提供自动保护。除非 buffer 分段和 fence/帧延迟策略已经设计好，否则会出现随机闪烁和数据竞争。

## 一句话总结

`QOpenGLFunctions_3_0` 把 FBO、VAO、细粒度 buffer 映射和 GPU 数据流带入 Qt 的版本化 OpenGL 调用中；它适合建立真正现代的资源路径，但需要主动切断其继承的 compatibility API，才能平稳进入 Core profile。
