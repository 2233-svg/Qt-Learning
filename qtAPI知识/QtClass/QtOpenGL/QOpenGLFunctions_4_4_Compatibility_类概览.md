# QOpenGLFunctions_4_4_Compatibility 类笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QOpenGLFunctions_4_4_Compatibility>`  
> 所属模块：`Qt6::OpenGL`  
> 继承：`QAbstractOpenGLFunctions`  
> 可用性：桌面 OpenGL 4.4 Compatibility profile；包含 4.4 Core API 与旧 fixed-function/legacy 接口

## 它解决什么问题

`QOpenGLFunctions_4_4_Compatibility` 让 Qt 程序在 OpenGL 4.4 Compatibility context 中同时使用不可变 buffer storage、纹理清零和 multi-bind 等资源管理能力，以及旧 fixed-function、client array、display list、传统像素路径。

它适合仍有历史模块无法立即剥离的项目：新渲染 pass 可以用 4.4 Core 子集建设高吞吐资源系统，旧模块继续被限制在兼容入口。它不应让新代码继续使用矩阵栈或立即模式，因为那些调用仍然阻碍 Core-only 部署。

## 实际使用场景

- 老 renderer 的主场景已迁移到 VBO/VAO/SSBO，但遗留网格或 overlay 仍使用旧状态机；
- 用持久映射 ring buffer 加速现代 instance/indirect 数据，同时保留旧插件渲染；
- 用 multi-bind 统一新 pass 的资源表，减少逐个绑定；
- 将旧纹理初始化路径逐步替换为 `glClearTexImage()` 和 immutable storage。

## 初始化与隔离建议

```cpp
#include <QOpenGLFunctions_4_4_Compatibility>

QOpenGLFunctions_4_4_Compatibility gl;

bool initializeResourceLayer()
{
    if (!gl.initializeOpenGLFunctions())
        return false;

    // 4.4 新资源路径使用 Core 子集。
    return true;
}
```

在 Compatibility profile 中，旧模块和新模块共享同一 OpenGL 状态。资源表、VAO/FBO、texture/sampler/image binding、pixel store 和 blend/depth/stencil 必须由每个 pass 显式建立，不能假定旧模块没有留下副作用。

## 4.4 能力如何帮助迁移

### Buffer storage 作为资源层基础

`glBufferStorage()` 可以让新的 buffer 分配策略固定下来：创建时决定是否允许动态子更新、持久映射和 coherent mapping。旧模块仍可使用自己的 VBO，但新模块应由统一的 ring buffer/allocator 管理，避免两套生命周期规则互相干扰。

### Multi-bind 收束状态修改

`glBindBuffersBase/Range()`、`glBindTextures()`、`glBindSamplers()`、`glBindImageTextures()`、`glBindVertexBuffers()` 适合把 render pass 所需绑定从许多分散调用集中为资源表。即使 Compatibility 允许更多全局状态，现代 pass 也可以由自己的绑定表获得更可预测的行为。

### Clear texture 替代部分传统像素初始化

`glClearTexImage()`/`glClearTexSubImage()` 是创建或复用 texture 后清空内容的现代方式。它比通过固定管线绘制一个全屏 quad 或传统 pixel path 更直接，也更容易与 FBO/compute/image 工作流衔接。

## Compatibility 边界

### 持久映射无法保护旧模块的错误访问

一个 legacy draw 也可能仍在读取 buffer。新 ring buffer 复用区段前必须用 fence 管理 GPU 完成时序，不能因为上下文是 Compatibility 就降低同步要求。

### Multi-bind 不会重置 legacy 状态

它批量绑定资源，但不会重置矩阵栈、client state、texture environment、pixel transfer、display list 或其他旧状态。新 pass 仍需要完整的 Core 风格状态设置。

### 旧 API 不能随 4.4 一起移植

Compatibility profile 的旧函数并不能在 Core/OpenGL ES 中使用。每保留一处 legacy 调用，就应明确它的替换计划。

## API 速查表

| 功能族（成员 API） | 是做什么的 | 使用时重点注意 |
| --- | --- | --- |
| `initializeOpenGLFunctions()` | 解析 current 4.4 Compatibility profile 函数。 | profile 必须匹配；失败后不得调用成员。 |
| 4.4 buffer：`glBufferStorage` | 分配不可变 buffer storage，并设置更新/映射 flags。 | 不能用 `glBufferData` 重定义；persistent mapping 需 fence/分段管理。 |
| 4.4 texture clear：`glClearTexImage`, `glClearTexSubImage` | 清空完整 texture level 或子区域。 | clear value 的 format/type 要兼容内部格式；区域不可越界。 |
| 4.4 multi-bind：`glBindBuffersBase`, `glBindBuffersRange`, `glBindTextures`, `glBindSamplers`, `glBindImageTextures`, `glBindVertexBuffers` | 批量绑定 indexed buffer、texture、sampler、image 和 vertex buffer。 | 资源 slot、offset、size、format、VAO 映射仍需逐项正确。 |
| 继承的 4.3 Core 子集：`glDispatchCompute`, `glShaderStorageBlockBinding`, `glMemoryBarrier`, `glMultiDraw*Indirect`, `glBindVertexBuffer`, `glVertexAttrib*Format`, `glTextureView`, `glCopyImageSubData`, `glInvalidate*`, `glDebugMessage*` | compute/SSBO、GPU-driven draw、分离顶点绑定、资源视图和调试。 | 新模块优先使用这些 Core 风格接口；按资源流转处理 barrier。 |
| 继承的 4.2--3.x Core 子集：`glTexStorage*`, `glBindImageTexture`, `glProgramUniform*`, `glGenProgramPipelines`, `glGenSamplers`, `glVertexAttribDivisor`, `glFenceSync`, `glBindVertexArray`, `glBindFramebuffer`, `glCreateShader` | immutable texture、program pipeline、sampler、instancing、sync、VAO/FBO 与 GLSL。 | 把它们作为新渲染层的唯一依赖，便于后续切 Core。 |
| legacy 几何与矩阵：`glBegin`, `glEnd`, `glVertex*`, `glColor*`, `glNormal*`, `glTexCoord*`, `glMatrixMode`, `glLoad*`, `glMultMatrix*`, `glTranslate*`, `glRotate*`, `glScale*` | 立即模式与固定矩阵栈。 | 只保留在隔离的遗留模块；不要出现在新 pass。 |
| legacy 光照/像素/显示列表：`glLight*`, `glMaterial*`, `glFog*`, `glTexEnv*`, `glTexGen*`, `glVertexPointer`, `glEnableClientState`, `glDrawPixels`, `glColorTable*`, `glConvolution*`, `glNewList`, `glCallList*`, `glSelectBuffer`, `glFeedbackBuffer` | 固定管线、client arrays、传统像素、display list 与反馈模式。 | 不适用于 Core/ES；会引入隐式状态与同步风险。 |

## 常见误区

### 使用 persistent mapping，却忘了旧 draw 也会访问同一 buffer

不论调用来自新模块还是 legacy 模块，只要 GPU 尚在读取该段数据，CPU 就不能覆盖。用统一 fence 策略管理所有使用者。

### 以为 multi-bind 能让状态自动整洁

它只批量设置部分绑定点。Compatibility 的其他状态仍可能残留，现代 pass 必须自给自足。

### 用新 texture clear 包装继续维持旧像素管线

`glClearTexImage()` 的优势是让资源初始化脱离固定管线。应借此机会把后续操作迁移到 FBO/shader/compute，而不是给传统像素路径加一层包装。

## 一句话总结

`QOpenGLFunctions_4_4_Compatibility` 是遗留 Qt OpenGL 项目采用不可变 buffer、批量绑定和直接纹理清零的过渡层；新资源系统可以由 4.4 Core 子集驱动，但必须严格隔离旧状态机并持续向 Core profile 收敛。
