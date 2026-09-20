# QOpenGLFunctions_1_2 类笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QOpenGLFunctions_1_2>`  
> 所属模块：`Qt6::OpenGL`  
> 继承：`QAbstractOpenGLFunctions`  
> 可用性：桌面 OpenGL 1.2 compatibility API；Qt 以 OpenGL ES 2 构建时不可用，也不适用于只提供 Core profile 的 context

## 它解决什么问题

`QOpenGLFunctions_1_2` 将 OpenGL 1.2 及此前版本的函数入口封装为成员函数。它的核心价值不是创造一套新的渲染抽象，而是让遗留桌面 OpenGL 程序通过 `initializeOpenGLFunctions()` 为当前 `QOpenGLContext` 解析函数地址，不必自行处理平台差异和函数指针。

相比 `QOpenGLFunctions_1_1`，它加入了 3D 纹理、`glDrawRangeElements()`、独立的混合常量色/混合方程，并暴露 1.2 imaging subset 的 color table、卷积、直方图和 minmax 接口。后一个子集以及此前的固定管线、client array、立即模式等，均属于 compatibility 时代功能。

它适合接手和分析旧渲染器，不是现代 OpenGL 新项目的起点。新代码应按目标 context 选择 `QOpenGLFunctions`、`QOpenGLExtraFunctions` 或匹配 Core profile 的版本函数类，并使用 shader、VBO 和 VAO。

## 实际使用场景

- 维护仍需要 `GL_TEXTURE_3D` 的旧桌面可视化、体数据查看器或体素编辑器；
- 迁移 1.1/1.2 时代的 fixed-function 渲染代码，同时先保留原有纹理与混合逻辑；
- 排查老程序中的颜色表、卷积滤镜或直方图路径为何在新机器和 Core context 中失效；
- 需要把一段明确要求 desktop compatibility context 的插件代码放入 Qt OpenGL 生命周期中。

## 初始化与最小示例

```cmake
find_package(Qt6 REQUIRED COMPONENTS OpenGL)
target_link_libraries(mytarget PRIVATE Qt6::OpenGL)
```

```cpp
#include <QOpenGLFunctions_1_2>

QOpenGLFunctions_1_2 gl;

bool initializeLegacyVolumePath()
{
    // 调用前，目标 QOpenGLContext 必须已经在本线程 current。
    if (!gl.initializeOpenGLFunctions())
        return false;

    GLuint texture = 0;
    gl.glGenTextures(1, &texture);
    gl.glBindTexture(GL_TEXTURE_3D, texture);
    gl.glTexParameteri(GL_TEXTURE_3D, GL_TEXTURE_MIN_FILTER, GL_LINEAR);
    gl.glTexParameteri(GL_TEXTURE_3D, GL_TEXTURE_MAG_FILTER, GL_LINEAR);
    return true;
}
```

初始化成功只表示 Qt 已为当前 context 解析到该函数集合；它不解除 profile、纹理尺寸、像素格式、状态机和资源共享规则。切换到不兼容 context 后，应重新初始化相应函数对象，不能把它当成可随意跨 context 复用的全局单例。

## 1.2 新增能力如何使用

### 3D 纹理

`glTexImage3D()` 分配一个 3D texture level，`glTexSubImage3D()` 更新其子体积，`glCopyTexSubImage3D()` 从当前 read buffer 复制二维区域到某个 z slice。体绘制、三维查找表和体素数据是这套接口的典型历史用途。

上传前须绑定正确 target，并检查 `GL_MAX_3D_TEXTURE_SIZE`。源内存排布仍受 `GL_UNPACK_ALIGNMENT`、`GL_UNPACK_ROW_LENGTH` 等 unpack state 影响；紧凑的单通道体素数据常需要把 `GL_UNPACK_ALIGNMENT` 改为 1。3D 纹理不会自动解决体渲染问题，采样、梯度、传递函数和透明度组合仍应由现代 fragment shader 处理。

### 混合方程与常量混合色

`glBlendEquation()` 决定源/目标因子相乘后怎样组合，例如加法、减法或反向减法；`glBlendColor()` 设置 `GL_CONSTANT_COLOR`、`GL_ONE_MINUS_CONSTANT_COLOR`、`GL_CONSTANT_ALPHA` 等 blend factor 使用的常量 RGBA 值。它们补齐了早期 `glBlendFunc()` 只能指定因子的限制。

它们只修改当前 context 的全局 blend state。实际生效还需要启用 `GL_BLEND`，并让 `glBlendFunc()` 的 factor 使用常量色；混合仍发生在 framebuffer 的颜色格式和颜色空间约束下，不能把它误当作通用的图像合成 API。

### `glDrawRangeElements()`

该函数与 `glDrawElements()` 一样按索引绘制，但额外给出最小/最大顶点索引范围，供旧驱动进行缓存优化。`start` 和 `end` 是提示参数，不是自动验证器；它们必须涵盖实际 indices 的范围。

在现代驱动上未必带来可测优势。更重要的是弄清 `indices` 的解释：没有 element array buffer 时是 CPU 指针；绑定了 EBO 时是 buffer 内字节偏移。

### Imaging subset

OpenGL 1.2 的 color table、convolution、histogram、minmax 与 separable filter 是固定功能像素处理管线。它们对维护古老科学可视化代码有意义，但不属于现代 Core OpenGL，支持面和性能都不应假设。新实现通常用 shader、compute shader 或 CPU 图像库替换。

这些 API 的查询和取回函数可能导致 GPU/CPU 同步；调用前还要为结果缓冲区按像素 format/type 与目标宽度分配足够空间。

## 关键边界

### 这是兼容性包装，而非“支持任意 OpenGL 1.2 调用”的承诺

该类只在非 OpenGL ES 的 Qt 构建中定义，并包含大量 deprecated 成员。请求 OpenGL 3.2+ Core profile 后，固定管线、矩阵栈、client state、imaging subset 等调用不应使用，即便某些历史符号在编译期可见。

### 资源属于 context 的共享组

纹理 ID 不是进程级对象。可共享的 context 可以访问同一纹理；无共享关系的 context 不可以。删除纹理后，旧绑定和延迟执行命令的行为也必须按 OpenGL 对象生命周期理解。

### 上传和读回都受 pixel store 状态影响

`glTexImage3D()`、`glTexSubImage3D()`、`glReadPixels()`、color-table 和 imaging 读写都不是只看裸指针。行对齐、行长度、跳过像素/行/图像等全局 state 会改变内存解释，调试花屏先检查 pack/unpack state。

### 不要在每帧同步查询

`glGet*()`、`glGetTexImage()`、`glGetHistogram()`、`glGetMinmax()` 和 `glFinish()` 可能迫使 CPU 等待 GPU。将它们放进逐帧路径通常会抹掉异步流水线；应只在初始化、诊断或明确的读回点调用。

## API 速查表

同一操作有 `f`、`d`、`i`、向量指针等数值变体时，下表按操作族列出成员名；变体改变输入类型或传入形式，不改变状态语义。本类完整继承 1.0 和 1.1 的成员，表中将它们按用途归纳。

| 功能族（成员 API） | 是做什么的 | 使用时重点注意 |
| --- | --- | --- |
| `initializeOpenGLFunctions()` | 为 current desktop compatibility context 解析 1.2 及继承函数。 | 仅能在兼容 context current 时调用；失败后不得调用成员。 |
| `glTexImage3D`, `glTexSubImage3D`, `glCopyTexSubImage3D` | 分配、局部更新或从 read buffer 复制 3D 纹理内容。 | 绑定 `GL_TEXTURE_3D`；检查尺寸限制、mip 边界及 unpack state。 |
| `glDrawRangeElements` | 用索引绘制并提供顶点索引范围提示。 | `start/end` 必须覆盖实际索引；indices 是指针还是 EBO offset 取决于绑定。 |
| `glBlendColor`, `glBlendEquation` | 设置常量混合色和颜色组合方程。 | 仍需 `glEnable(GL_BLEND)` 与匹配的 `glBlendFunc`；状态会影响后续绘制。 |
| `glColorTable`, `glColorSubTable`, `glColorTableParameter*`, `glCopyColorTable`, `glCopyColorSubTable`, `glGetColorTable*` | 定义、更新、复制、查询 palette/color table。 | 1.2 imaging subset，已废弃；缓冲区大小须匹配 format/type 与表宽。 |
| `glConvolutionFilter1D`, `glConvolutionFilter2D`, `glConvolutionParameter*`, `glCopyConvolutionFilter*`, `glGetConvolution*` | 配置、复制、查询固定功能卷积滤镜。 | compatibility-only；现代代码使用 shader 或图像处理库。 |
| `glHistogram`, `glGetHistogram*`, `glResetHistogram` | 收集、读取和清空像素直方图。 | 读回可同步；正确分配结果数组并明确 `sink` 是否继续传递像素。 |
| `glMinmax`, `glGetMinmax*`, `glResetMinmax` | 收集、读取和清空像素各通道最小/最大值。 | 同为 legacy imaging API；读取前确认输出 format/type。 |
| `glSeparableFilter2D`, `glGetSeparableFilter` | 使用行/列核定义或取回可分离二维滤镜。 | row、column、span 的内存布局和容量必须匹配。 |
| 继承的纹理对象：`glGenTextures`, `glDeleteTextures`, `glBindTexture`, `glIsTexture`, `glTexImage1D`, `glTexImage2D`, `glTexSubImage1D`, `glTexSubImage2D`, `glTexParameter*`, `glGetTex*`, `glCopyTexImage*`, `glCopyTexSubImage1D`, `glCopyTexSubImage2D` | 管理 1D/2D 纹理及从 framebuffer 复制。 | 对象归 shared context group；读回/复制受当前 framebuffer、format 和 pixel-store state 影响。 |
| 继承的数组绘制：`glDrawArrays`, `glDrawElements`, `glVertexPointer`, `glColorPointer`, `glNormalPointer`, `glTexCoordPointer`, `glIndexPointer`, `glEdgeFlagPointer`, `glEnableClientState`, `glDisableClientState`, `glInterleavedArrays`, `glArrayElement`, `glPushClientAttrib`, `glPopClientAttrib` | 使用旧 client-side vertex array 提交几何。 | deprecated；CPU 指针必须在 draw 时有效，Core/ES 不适用。 |
| 继承的帧缓冲状态：`glViewport`, `glScissor`, `glEnable`, `glDisable`, `glClear*`, `glClear`, `glColorMask`, `glDepth*`, `glStencil*`, `glBlendFunc`, `glLogicOp`, `glCullFace`, `glFrontFace`, `glPolygonOffset`, `glFlush`, `glFinish` | 设置 raster、depth、stencil、blend、clear 和提交状态。 | 状态是 current context 全局状态；避免每帧 `glFinish`。 |
| 继承的查询与像素操作：`glGet*`, `glGetString`, `glGetError`, `glReadPixels`, `glReadBuffer`, `glDrawBuffer`, `glPixelStore*`, `glPixelTransfer*`, `glPixelMap*`, `glDrawPixels`, `glCopyPixels`, `glPixelZoom` | 查询状态，配置并执行传统像素路径。 | 查询/读回可同步；严格处理 pack/unpack alignment 与输出缓冲区容量。 |
| 继承的 fixed pipeline：`glMatrixMode`, `glLoad*`, `glMultMatrix*`, `glTranslate*`, `glRotate*`, `glScale*`, `glFrustum`, `glOrtho`, `glLight*`, `glMaterial*`, `glFog*`, `glTexEnv*`, `glTexGen*`, `glBegin`, `glEnd`, `glVertex*`, `glColor*`, `glNormal*`, `glTexCoord*` | 固定变换、光照、纹理环境和立即模式。 | 都是 compatibility API；新代码改用 shader、uniform、VBO/VAO。 |
| 继承的其他 legacy：`glMap*`, `glEval*`, `glNewList`, `glCallList*`, `glRenderMode`, `glSelectBuffer`, `glFeedbackBuffer`, `glPushAttrib`, `glPopAttrib`, `glAccum` | evaluator、display list、selection/feedback、状态栈和 accumulation buffer。 | 不适用于现代 Core/ES；仅限维护与迁移场景。 |

## 常见误区

### 把 3D texture 上传当作连续字节复制

默认的四字节 unpack alignment 会让某些体素行的步长与实际数据不一致。尤其是单通道、宽度不是 4 的倍数的体数据，上传前要显式设定并在完成后恢复需要的 `GL_UNPACK_ALIGNMENT`。

### 以为 `glBlendColor()` 已开启常量色混合

它只写入一个 state 值；只有 blend 已启用，且 `glBlendFunc()` 选用了对应 `GL_CONSTANT_*` factor，常量色才参与运算。

### 用 imaging subset 写新图像滤镜

它是历史固定功能管线，功能、跨平台一致性和性能都不适合作为新代码依赖。用 shader 实现通常可控得多，也能在现代 Core context 上运行。

## 一句话总结

`QOpenGLFunctions_1_2` 是接入 OpenGL 1.2 兼容性代码的版本化函数入口：它补齐 3D 纹理、混合方程/常量色和 imaging subset，但真正可靠的使用前提始终是 current 的桌面 compatibility context 与对 legacy 状态机边界的清醒认识。
