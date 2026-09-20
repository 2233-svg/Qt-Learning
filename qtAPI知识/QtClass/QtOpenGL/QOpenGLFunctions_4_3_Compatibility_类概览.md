# QOpenGLFunctions_4_3_Compatibility 类笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QOpenGLFunctions_4_3_Compatibility>`  
> 所属模块：`Qt6::OpenGL`  
> 继承：`QAbstractOpenGLFunctions`  
> 可用性：桌面 OpenGL 4.3 Compatibility profile；包含 4.3 Core API 与旧 fixed-function/legacy 接口

## 它解决什么问题

`QOpenGLFunctions_4_3_Compatibility` 让 Qt 程序在 OpenGL 4.3 Compatibility context 中同时访问 compute shader、SSBO、program resource reflection、multi-draw indirect、texture view、copy image、invalidate 等现代能力，以及历史 fixed-function API。

它的合理定位是大型旧渲染器的迁移阶段：老模块可以继续运行，新模块可以用 compute/SSBO/GPU-driven draw 建立更现代的管线。但这也意味着同一个 context 中同时存在最旧和较新的状态模型，必须靠架构隔离来避免互相污染。

## 实际使用场景

- 老式 CAD 或可视化程序保留旧绘制路径，同时新加入 compute culling 或 GPU 粒子；
- 用 program resource reflection 自动绑定新 shader 资源，但仍兼容旧插件；
- 把大量旧 draw call 逐步改造成 multi-draw indirect；
- 用 texture view/copy image 重构资源系统，同时保留旧 UI overlay。

## 初始化与隔离建议

```cpp
#include <QOpenGLFunctions_4_3_Compatibility>

QOpenGLFunctions_4_3_Compatibility gl;

bool initializeComputeBridge()
{
    if (!gl.initializeOpenGLFunctions())
        return false;

    // 新模块使用 Core 子集；旧模块集中在单独入口。
    return true;
}
```

建议让新 4.3 功能只依赖 VAO/FBO/shader/buffer/image/SSBO 等 Core 子集。旧 fixed-function 模块进入和退出时显式清理或重设状态，避免影响 compute 输出、image binding、indirect buffer 和 framebuffer。

## 4.3 能力如何帮助迁移

### Compute 与 SSBO

`glDispatchCompute()`、`glShaderStorageBlockBinding()` 和继承的 memory barrier 能将旧 CPU 预处理、粒子更新、剔除或统计逐步移到 GPU。旧模块使用这些结果前，必须通过明确 buffer/texture 交接和 barrier 保证可见。

### Program resource reflection

`glGetProgramResource*()` 系列能统一查询 shader 资源，适合替换旧项目中硬编码 location/binding 的散乱写法。它只对已链接 program 有效，shader relink 后缓存失效。

### Multi-draw indirect 与 separate attribute binding

multi-draw indirect 可把大量对象绘制聚合到 command buffer。separate attribute binding 让旧 mesh 数据布局迁移更平滑：先稳定 attribute format，再逐步切换 buffer 来源和实例化布局。

## Compatibility 边界

### Compute/SSBO 与 legacy 像素路径更需要阶段边界

旧的 `glDrawPixels()`、pixel transfer、color table 等会修改或依赖大量隐式状态。现代 image/SSBO 路径又需要 barrier 和绑定点管理。二者混用时，阶段之间必须显式重设资源和状态。

### Debug 难度来自“可用 API 太多”

Compatibility profile 允许旧函数继续存在，但它们不会变得更可控。把 legacy 调用集中封装，避免它们散落到 compute 或 indirect draw 代码里。

### Core-only 部署仍会失败

OpenGL 4.3 版本号不保证 compatibility profile 在目标平台可用。要支持 Core-only 环境，就要把新路径写成 Core 子集，并逐步替代旧路径。

## API 速查表

| 功能族（成员 API） | 是做什么的 | 使用时重点注意 |
| --- | --- | --- |
| `initializeOpenGLFunctions()` | 解析 current 4.3 Compatibility profile 函数。 | profile 必须匹配；失败后不能调用成员。 |
| 4.3 compute/SSBO：`glDispatchCompute`, `glDispatchComputeIndirect`, `glShaderStorageBlockBinding` | 启动 compute shader，并绑定 shader storage block。 | 写入后按后续访问设置 barrier；SSBO 需要明确 binding point。 |
| 4.3 program reflection：`glGetProgramInterfaceiv`, `glGetProgramResourceIndex`, `glGetProgramResourceName`, `glGetProgramResourceiv`, `glGetProgramResourceLocation`, `glGetProgramResourceLocationIndex` | 统一查询 shader program 资源。 | 仅对 linked program 有效；relink 后刷新缓存。 |
| 4.3 indirect/buffer：`glMultiDrawArraysIndirect`, `glMultiDrawElementsIndirect`, `glClearBufferData`, `glClearBufferSubData` | 批量 indirect draw 和 buffer 清空。 | command 结构和 buffer 格式必须精确。 |
| 4.3 vertex binding：`glBindVertexBuffer`, `glVertexAttribFormat`, `glVertexAttribIFormat`, `glVertexAttribLFormat`, `glVertexAttribBinding`, `glVertexBindingDivisor` | 分离 attribute 格式和 buffer binding。 | 状态保存在 VAO；区分 attribute index 和 binding index。 |
| 4.3 texture/FBO：`glTextureView`, `glCopyImageSubData`, `glTexBufferRange`, `glTexStorage2DMultisample`, `glTexStorage3DMultisample`, `glFramebufferParameteri`, `glGetFramebufferParameteriv`, `glGetInternalformati64v` | texture view、图像复制、buffer texture 子范围、多重采样不可变存储和查询。 | format compatibility、范围和样本数必须合法。 |
| 4.3 invalidate：`glInvalidateTexImage`, `glInvalidateTexSubImage`, `glInvalidateBufferData`, `glInvalidateBufferSubData`, `glInvalidateFramebuffer`, `glInvalidateSubFramebuffer` | 告诉驱动资源旧内容可丢弃。 | 只在后续不再依赖旧内容时使用。 |
| 继承的现代 Core 子集：`glTexStorage*`, `glBindImageTexture`, `glMemoryBarrier`, `glGenProgramPipelines`, `glProgramUniform*`, `glPatchParameter*`, `glGenSamplers`, `glVertexAttribDivisor`, `glFenceSync`, `glBindVertexArray`, `glBindFramebuffer` | 不可变纹理、image/barrier、program pipeline、tessellation、sampler、instancing、sync、VAO/FBO。 | 新模块优先使用这些，保持可迁移到 Core。 |
| legacy 几何/矩阵：`glBegin`, `glEnd`, `glVertex*`, `glColor*`, `glNormal*`, `glTexCoord*`, `glMatrixMode`, `glLoad*`, `glTranslate*`, `glRotate*`, `glScale*` | 立即模式与固定矩阵栈。 | 只留在旧模块；不要与 compute/SSBO 路径混写。 |
| legacy 光照/像素/反馈：`glLight*`, `glMaterial*`, `glFog*`, `glTexEnv*`, `glTexGen*`, `glVertexPointer`, `glDrawPixels`, `glColorTable*`, `glConvolution*`, `glNewList`, `glCallList*`, `glSelectBuffer`, `glFeedbackBuffer` | 固定管线、client arrays、传统像素、display list 与反馈模式。 | 不适用于 Core/ES；状态污染和同步风险高。 |

## 常见误区

### compute 生成数据后让 legacy 路径直接读

旧路径不会自动等待或获得可见性。用合适 barrier，并明确资源绑定和格式。

### 在 Compatibility 中随手调用旧 API 调试

调试时临时的 matrix、texture environment 或 client state 修改可能污染后续现代 pass。临时调试代码也要隔离。

### 把 multi-draw indirect 当作简单循环替代

它要求 command buffer、VAO、shader resource 和可见性全部正确。迁移前先让单个 indirect draw 稳定，再批量化。

## 一句话总结

`QOpenGLFunctions_4_3_Compatibility` 能让旧 Qt OpenGL 项目引入 compute、SSBO 和 GPU-driven 绘制，但它也最容易把新旧状态混成一团；可靠做法是把现代 Core 子集和 legacy 模块清楚分层。
