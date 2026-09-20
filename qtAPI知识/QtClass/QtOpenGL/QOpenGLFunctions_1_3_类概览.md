# QOpenGLFunctions_1_3 类笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QOpenGLFunctions_1_3>`  
> 所属模块：`Qt6::OpenGL`  
> 继承：`QAbstractOpenGLFunctions`  
> 可用性：桌面 OpenGL 1.3 compatibility API；Qt 以 OpenGL ES 2 构建时不可用，也不适用于只提供 Core profile 的 context

## 它解决什么问题

`QOpenGLFunctions_1_3` 把 OpenGL 1.3 与此前版本的入口组织成依赖 current `QOpenGLContext` 的成员函数。通过 `initializeOpenGLFunctions()`，Qt 为这组历史桌面 OpenGL 调用解析函数地址，避免应用直接承担平台相关的函数加载工作。

OpenGL 1.3 的核心增量包括多纹理单元选择、压缩纹理上传/读回和 multisample coverage 控制；同时该类还保留 `glClientActiveTexture()`、`glMultiTexCoord*()` 以及转置矩阵函数等 fixed-function compatibility 接口。它因此非常适合读懂或维护旧多纹理渲染器，却不适合作为新 renderer 的设计目标。

新项目应使用 programmable pipeline。多张纹理应在 shader 中通过 sampler uniform 管理；数据压缩选择、mipmap 和采样状态则由现代纹理对象 API 与显卡格式能力共同决定。

## 实际使用场景

- 修复依赖 `GL_TEXTURE0 + n`、`glActiveTexture()` 的旧多贴图材质代码；
- 维护使用 S3TC 等硬件压缩纹理，并依赖 `glCompressedTexImage*()` 的旧资源系统；
- 在 Qt 中承接早期 multisample coverage 逻辑，逐步迁移到 FBO、multisample texture 或现代渲染路径；
- 将仍使用 fixed-function 多纹理坐标的模型查看器改造成可控的 context 初始化与兼容性检测流程。

## 初始化与最小示例

```cpp
#include <QOpenGLFunctions_1_3>

QOpenGLFunctions_1_3 gl;

bool initializeLegacyMultitexture()
{
    // 目标 QOpenGLContext 已在当前线程 current。
    if (!gl.initializeOpenGLFunctions())
        return false;

    gl.glActiveTexture(GL_TEXTURE0);
    gl.glBindTexture(GL_TEXTURE_2D, m_baseColorTexture);
    gl.glActiveTexture(GL_TEXTURE1);
    gl.glBindTexture(GL_TEXTURE_2D, m_detailTexture);
    return true;
}
```

函数对象必须与调用时的 desktop compatibility context 相匹配。不要在 GUI 线程初始化后，直接从另一个线程或另一个不共享 context 调用它；OpenGL context 只能在一个线程中 current，资源可见性也由共享组决定。

## 1.3 新增能力如何使用

### `glActiveTexture()` 和多纹理单元

`glActiveTexture(GL_TEXTURE0 + unit)` 选择随后 `glBindTexture()`、`glTexParameter*()`、`glTexImage*()` 等纹理操作作用的 server-side texture unit。它不会自动绑定多张纹理，也不设置 shader sampler 的 unit；在现代代码中，这两项分别通过 texture binding 与 `glUniform1i()` 或 DSA 风格接口完成。

先用 `glGetIntegerv(GL_MAX_TEXTURE_UNITS, ...)` 或在更现代的路径查询对应限制，再选择合法 unit。维护 fixed-function 程序时还要区分它和 `glClientActiveTexture()`：前者选择 server-side 纹理状态，后者只选择 client-side texture-coordinate array。

### 压缩纹理

`glCompressedTexImage1D/2D/3D()` 直接上传已压缩的 texture level；`glCompressedTexSubImage*()` 局部替换其中区域；`glGetCompressedTexImage()` 把压缩数据取回。它们不会把任意图片自动压缩为 GPU 格式，调用者必须提供目标 format 所需的块编码数据与正确的 `imageSize`。

支持的压缩 internal format 依赖驱动扩展、平台和 context。块压缩格式的子区域通常有块对齐约束；不要把普通 RGBA 内存传给 compressed API。若运行时需要跨设备适配，优先保留多种资源格式或使用可验证的转码方案。

### `glSampleCoverage()`

此函数设置 multisample coverage 的 value 和是否反转 coverage mask。它只有在 multisampling 生效时才有意义，通常还需启用 `GL_SAMPLE_COVERAGE`；它影响的是覆盖样本选择，不等同于 alpha blending，也不是抗锯齿质量的通用调节旋钮。

实际 sample buffer 的数量由当前 drawable 或 FBO 附件决定。没有 multisample buffer 时，调整 coverage 不会产生预期画面变化。

### Legacy 多纹理坐标与转置矩阵

`glMultiTexCoord1*` 到 `glMultiTexCoord4*` 直接为指定纹理单元写 fixed-function 当前纹理坐标；`glClientActiveTexture()` 选择某个 client texture-coordinate array；`glLoadTransposeMatrix*()` 和 `glMultTransposeMatrix*()` 以转置形式写入旧矩阵栈。这些是历史 fixed pipeline 的辅助接口。

现代渲染器应把纹理坐标作为 vertex attribute，把矩阵通过 uniform/buffer 交给 shader。转置问题应由数据布局和 uniform 上传时的约定解决，而不是在矩阵栈上堆叠 legacy 调用。

## 关键边界

### 兼容性 profile 是硬前提

本类在 Qt 的头文件中被排除于 OpenGL ES 2 构建。并且它继承的 1.0--1.2 成员包含大量 deprecated API；在 OpenGL Core profile 上，立即模式、client state、imaging subset 与 1.3 的 legacy 多纹理坐标均不应使用。

### 纹理单元 state 是隐式的

`glActiveTexture()` 修改全局状态，任何后续 texture bind、上传和参数设置都作用于选中的 unit/target。调试“贴图串台”时，除了检查 texture ID，也要检查 active unit、目标和 sampler 指向的整数 unit 是否一致。

### 压缩数据的边界不是字节对齐那么简单

对于块压缩格式，宽高和 `xoffset/yoffset` 常需按块宽高对齐，除非操作正好触及 mip level 边缘。`imageSize` 必须精确匹配格式、维度和块数，否则驱动会报错或产生损坏纹理。

### 多重采样状态无法替代正确的缓冲配置

`glSampleCoverage()` 只控制已存在的 samples。窗口 surface format 或 FBO 没有配置 multisample attachment 时，它不会为渲染目标凭空增加采样数。

## API 速查表

`QOpenGLFunctions_1_3` 包含下表中的 1.3 增量，并完整继承 1.0、1.1、1.2 的函数。数值类型或向量参数变体以同一操作族归纳，避免把相同语义拆成数百行。

| 功能族（成员 API） | 是做什么的 | 使用时重点注意 |
| --- | --- | --- |
| `initializeOpenGLFunctions()` | 为 current desktop compatibility context 解析 1.3 及继承函数。 | 初始化失败后不得调用；切换不兼容 context 需重新初始化。 |
| `glActiveTexture` | 选择后续 server-side 纹理操作使用的 texture unit。 | 参数为 `GL_TEXTURE0 + unit`；它不设置 shader sampler。 |
| `glSampleCoverage` | 设置 multisample coverage value 与 invert 标志。 | 仅对 multisample target 有效，通常需配合 `GL_SAMPLE_COVERAGE`。 |
| `glCompressedTexImage1D`, `glCompressedTexImage2D`, `glCompressedTexImage3D` | 上传一个已压缩的完整 texture level。 | 数据必须符合 compressed internal format，`imageSize` 要精确。 |
| `glCompressedTexSubImage1D`, `glCompressedTexSubImage2D`, `glCompressedTexSubImage3D` | 替换已有压缩纹理 level 的局部区域。 | 块压缩格式通常要求 offset/extent 块对齐；目标 level 必须存在。 |
| `glGetCompressedTexImage` | 读回压缩纹理 level 的块编码数据。 | 输出缓冲区按查询到的 `GL_TEXTURE_COMPRESSED_IMAGE_SIZE` 分配；读回可能同步。 |
| `glClientActiveTexture` | 选择 client-side texture-coordinate array 所属纹理单元。 | 仅 fixed-function/client array compatibility 路径使用；不是 `glActiveTexture` 的替代。 |
| `glMultiTexCoord1*`, `glMultiTexCoord2*`, `glMultiTexCoord3*`, `glMultiTexCoord4*` | 为指定 unit 设置 fixed-function 当前纹理坐标。 | 已废弃；现代代码使用顶点属性和 shader sampler。 |
| `glLoadTransposeMatrixf`, `glLoadTransposeMatrixd`, `glMultTransposeMatrixf`, `glMultTransposeMatrixd` | 以转置布局装载或相乘旧矩阵栈。 | fixed-function only；新代码统一矩阵内存布局与 uniform 上传约定。 |
| 继承的 1.2 纹理/混合：`glTexImage3D`, `glTexSubImage3D`, `glCopyTexSubImage3D`, `glDrawRangeElements`, `glBlendColor`, `glBlendEquation` | 支持 3D texture、范围索引绘制和独立混合状态。 | 纹理上传依赖 unpack state；indices 解释依 EBO binding；blend 是全局 state。 |
| 继承的 1.2 imaging：`glColorTable*`, `glColorSubTable`, `glCopyColorTable`, `glCopyColorSubTable`, `glConvolutionFilter*`, `glConvolutionParameter*`, `glCopyConvolutionFilter*`, `glGetConvolution*`, `glHistogram`, `glGetHistogram*`, `glResetHistogram`, `glMinmax`, `glGetMinmax*`, `glResetMinmax`, `glSeparableFilter2D`, `glGetSeparableFilter` | color table、卷积、统计和可分离滤镜固定功能像素处理。 | 全部为 compatibility/legacy；查询与读回可产生同步。 |
| 继承的纹理对象：`glGenTextures`, `glDeleteTextures`, `glBindTexture`, `glIsTexture`, `glTexImage1D`, `glTexImage2D`, `glTexSubImage1D`, `glTexSubImage2D`, `glTexParameter*`, `glGetTex*`, `glCopyTexImage*`, `glCopyTexSubImage1D`, `glCopyTexSubImage2D` | 管理 1D/2D 纹理和传统 framebuffer copy。 | 资源属于 context 共享组；确认 active unit、target 和 pixel-store state。 |
| 继承的批量/数组绘制：`glDrawArrays`, `glDrawElements`, `glVertexPointer`, `glColorPointer`, `glNormalPointer`, `glTexCoordPointer`, `glIndexPointer`, `glEdgeFlagPointer`, `glEnableClientState`, `glDisableClientState`, `glInterleavedArrays`, `glArrayElement` | 使用旧 client-side vertex arrays 绘制。 | deprecated；CPU 指针要在 draw 时有效，Core/ES 不可用。 |
| 继承的输出和查询：`glViewport`, `glScissor`, `glEnable`, `glDisable`, `glClear*`, `glClear`, `glDepth*`, `glStencil*`, `glBlendFunc`, `glColorMask`, `glCullFace`, `glFrontFace`, `glGet*`, `glGetError`, `glReadPixels`, `glPixelStore*`, `glFlush`, `glFinish` | 配置 render state、查询状态、像素传输与同步。 | state 属 current context；查询和读回不宜放在热路径。 |
| 继承的 fixed pipeline：`glMatrixMode`, `glLoad*`, `glMultMatrix*`, `glTranslate*`, `glRotate*`, `glScale*`, `glBegin`, `glEnd`, `glVertex*`, `glColor*`, `glNormal*`, `glTexCoord*`, `glLight*`, `glMaterial*`, `glFog*`, `glTexEnv*`, `glTexGen*` | 固定变换、立即模式、光照和纹理环境。 | compatibility-only；迁移目标是 shader、uniform、VBO 和 VAO。 |
| 继承的其他 legacy：`glMap*`, `glEval*`, `glNewList`, `glCallList*`, `glRenderMode`, `glSelectBuffer`, `glFeedbackBuffer`, `glPushAttrib`, `glPopAttrib`, `glPushClientAttrib`, `glPopClientAttrib`, `glAccum` | evaluator、display list、selection/feedback 和状态栈。 | 不适用于现代 Core/ES；只用于维护或逐步替换。 |

## 常见误区

### 只调用 `glActiveTexture()`，却没有让 sampler 指向相同 unit

绑定发生在哪个 unit 与 shader sampler 读取哪个 unit 是两件事。固定管线会使用其自身的 texture environment；shader 管线则需要让 sampler uniform 的整数值与 `GL_TEXTURE0 + unit` 中的 `unit` 对齐。

### 把未压缩 RGBA 数据传给 `glCompressedTexImage2D()`

compressed API 不替你编码。它要求已经按目标压缩格式组织好的 block 数据和精确字节数；普通像素数据应使用 `glTexImage2D()`，或先经过可靠的离线/运行时转码。

### 用 `glClientActiveTexture()` 选择 shader 采样纹理

它只影响旧 client texture-coordinate arrays，不改变 server-side texture binding，也不改变 shader uniform。对于现代 shader，它通常完全不需要出现。

## 一句话总结

`QOpenGLFunctions_1_3` 是旧桌面多纹理与压缩纹理代码的 Qt 函数包装层；它能让遗留路径在正确的 compatibility context 中继续工作，但 active texture 的隐式状态、压缩块格式的严格边界和 fixed-function API 的淘汰状态都必须被明确管理。
