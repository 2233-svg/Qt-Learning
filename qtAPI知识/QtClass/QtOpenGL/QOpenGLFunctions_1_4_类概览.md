# QOpenGLFunctions_1_4 类笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QOpenGLFunctions_1_4>`  
> 所属模块：`Qt6::OpenGL`  
> 继承：`QAbstractOpenGLFunctions`  
> 可用性：桌面 OpenGL 1.4 compatibility API；Qt 以 OpenGL ES 2 构建时不可用，也不适用于只提供 Core profile 的 context

## 它解决什么问题

`QOpenGLFunctions_1_4` 把 OpenGL 1.4 及其前代规范的函数包装为对象成员。对 Qt 程序而言，它把“当前 context 是否有这组桌面兼容 API、怎样加载调用入口”收束到 `initializeOpenGLFunctions()`，使遗留代码不用直接面对平台函数加载差异。

它的 1.4 增量很有时代特征：`glMultiDraw*()` 试图减少多个 draw call 的驱动调用开销，`glBlendFuncSeparate()` 让 RGB 和 Alpha 采用不同混合因子，point parameter 则补充点精灵/衰减相关状态。与此同时它仍带着窗口光栅位置、第二颜色、独立雾坐标等 fixed-function 功能。

这套包装适用于维护和迁移旧 renderer。它不是 Core OpenGL 或 OpenGL ES 的兼容层；新项目应使用 programmable pipeline 和更高版本的 Core functions。

## 实际使用场景

- 修改仍用多批 client array 数据绘制同种 primitive 的老可视化程序；
- 修复半透明粒子或 UI 叠加中 RGB/Alpha 应采用不同 blend factor 的旧路径；
- 接收使用 window raster position、secondary color 或 fog coordinate 的历史模型查看器；
- 在可控的 compatibility context 中逐段替换 fixed-function 调用，避免一口气重写整个渲染器。

## 初始化与最小示例

```cpp
#include <QOpenGLFunctions_1_4>

QOpenGLFunctions_1_4 gl;

bool initializeLegacyRenderer()
{
    // 调用前，目标 QOpenGLContext 必须在当前线程 current。
    if (!gl.initializeOpenGLFunctions())
        return false;

    gl.glEnable(GL_BLEND);
    gl.glBlendFuncSeparate(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA,
                           GL_ONE, GL_ONE_MINUS_SRC_ALPHA);
    return true;
}
```

同一个函数对象不应在不兼容的 context 间任意复用。context 必须在调用线程 current；其资源与状态属于 context 或共享组，而不是普通 C++ 全局状态。

## 1.4 新增能力如何使用

### 多次绘制

`glMultiDrawArrays()` 将 `first[]`、`count[]` 中的多个连续顶点区间合并为一次 API 调用；`glMultiDrawElements()` 对多个 index range 做同样的事。它们并不会自动合并材质、纹理、uniform 或 primitive mode，调用期间所有 draw 共享同一套 OpenGL 状态。

`drawcount` 决定数组项数，`first`、`count`、`indices` 必须至少有这么多元素。对于 `glMultiDrawElements()`，每个 `indices[i]` 在未绑定 element array buffer 时是 CPU 地址；绑定 EBO 时是该 buffer 内的字节偏移。这是维护旧代码时最容易出错的语义分岔。

### 分离 RGB/Alpha 混合因子

`glBlendFuncSeparate()` 分别设置 RGB 与 Alpha 的 source/destination factor。普通 alpha 合成常见的一种组合是 RGB 使用 `GL_SRC_ALPHA` / `GL_ONE_MINUS_SRC_ALPHA`，Alpha 使用 `GL_ONE` / `GL_ONE_MINUS_SRC_ALPHA`；具体选择仍取决于 framebuffer 是否存 alpha、素材是否 premultiplied，以及后续合成链路。

它只改写 blend state，仍需 `glEnable(GL_BLEND)`。对 premultiplied-alpha 内容若仍使用非预乘因子，边缘通常会发黑或发亮。

### 点参数

`glPointParameter*()` 设置 `GL_POINT_SIZE_MIN`、`GL_POINT_SIZE_MAX`、`GL_POINT_DISTANCE_ATTENUATION`、`GL_POINT_FADE_THRESHOLD_SIZE` 等点光栅化状态。它主要服务于早期点精灵和固定管线粒子效果。

真实可见的点大小还受硬件 `GL_ALIASED_POINT_SIZE_RANGE` 或实现限制。现代粒子系统多由 shader 输出 `gl_PointSize` 或绘制 billboard quad，不能依赖这些旧状态在各平台呈现一致结果。

### 1.4 的兼容性扩展

`glWindowPos2*`/`glWindowPos3*` 直接设置用于 `glDrawPixels()`、`glBitmap()` 的窗口光栅位置，绕开传统 `glRasterPos*()` 的变换/裁剪失败问题。`glSecondaryColor3*()` 与 `glSecondaryColorPointer()` 为固定管线提供第二颜色，`glFogCoord*()` 与 `glFogCoordPointer()` 提供逐顶点雾坐标。

三组函数均属 deprecated compatibility path。它们的迁移目标分别是屏幕空间 shader 绘制、普通 vertex color attribute，以及由 vertex/fragment shader 显式计算的雾因子。

## 关键边界

### API 版本不等于 context profile

类包含此前版本的大量 deprecated 成员，只代表 Qt 能为兼容 context 暴露包装。在 Core profile 上，不应调用矩阵栈、立即模式、client arrays、secondary color 指针、fog coordinate 指针或 window raster path。

### `glMultiDraw*()` 不会让数据自动变成 GPU 资源

它降低的是多次 API 调用的表层开销。若数据仍来自 client-side array，CPU 指针的生命周期、内存布局和线程边界问题依然存在；现代高吞吐路径仍应使用 VBO/VAO、instancing 或更高版本的 indirect draw。

### 分离混合因子必须同输出格式一起考虑

写入没有 alpha 通道的目标时，单独配置 alpha factor 没有可见价值。sRGB framebuffer、premultiplied alpha 与多重渲染目标也会改变最终组合方式，不能只复制某组常量。

## API 速查表

该类完整继承 OpenGL 1.0--1.3 成员；下表按真正的操作族列出 1.4 新增接口，并归纳继承能力。数值类型和向量指针重载不重复拆分为多行。

| 功能族（成员 API） | 是做什么的 | 使用时重点注意 |
| --- | --- | --- |
| `initializeOpenGLFunctions()` | 为 current desktop compatibility context 解析 1.4 与继承函数。 | 初始化失败后不得调用任何 `gl*` 成员；切换 context 后重新确认兼容性。 |
| `glPointParameterf`, `glPointParameterfv`, `glPointParameteri`, `glPointParameteriv` | 设置点大小衰减、最小/最大大小与点淡出参数。 | 仅影响旧点光栅化状态；最终点大小受实现限制。 |
| `glMultiDrawArrays` | 用多个 `first/count` 区间发出同一 primitive mode 的多批 array draw。 | 数组长度至少为 `drawcount`；所有批次共享当前状态与顶点数组。 |
| `glMultiDrawElements` | 用多个 count/index range 发出多批 indexed draw。 | 未绑定 EBO 时 entries 是地址，绑定时是字节 offset；每批 index type 相同。 |
| `glBlendFuncSeparate` | 分别指定 RGB 和 Alpha 的 source/destination blend factor。 | 需先启用 `GL_BLEND`；选择要与 straight/premultiplied alpha 及目标格式匹配。 |
| `glWindowPos2*`, `glWindowPos3*` | 直接设置传统 pixel/bitmap path 的窗口光栅位置。 | deprecated；只影响 raster operations，不是现代屏幕空间坐标 API。 |
| `glSecondaryColor3*`, `glSecondaryColorPointer` | 设置/定义 fixed-function 的第二颜色属性。 | compatibility-only；新代码用通用顶点属性并在 shader 中计算。 |
| `glFogCoordf`, `glFogCoordfv`, `glFogCoordd`, `glFogCoorddv`, `glFogCoordPointer` | 设置/定义逐顶点雾坐标。 | 仅固定管线雾使用；指针的数据必须在 draw 时有效。 |
| 继承的 1.3 纹理功能：`glActiveTexture`, `glCompressedTexImage*`, `glCompressedTexSubImage*`, `glGetCompressedTexImage`, `glSampleCoverage` | 选择纹理单元，处理压缩纹理并控制 sample coverage。 | active unit 是隐式状态；compressed data 和子区域须满足格式/块对齐限制。 |
| 继承的 1.3 legacy 多纹理：`glClientActiveTexture`, `glMultiTexCoord1*`, `glMultiTexCoord2*`, `glMultiTexCoord3*`, `glMultiTexCoord4*`, `glLoadTransposeMatrix*`, `glMultTransposeMatrix*` | 支持 fixed-function 多纹理坐标和旧矩阵栈。 | 已废弃；现代代码使用 attribute、sampler 和 uniform。 |
| 继承的 1.2 功能：`glTexImage3D`, `glTexSubImage3D`, `glCopyTexSubImage3D`, `glDrawRangeElements`, `glBlendColor`, `glBlendEquation`, `glColorTable*`, `glConvolution*`, `glHistogram*`, `glMinmax*`, `glSeparableFilter2D` | 3D texture、范围索引绘制、独立混合与 imaging subset。 | imaging subset 为 legacy；上传/读回依赖 pixel-store state，查询可能同步。 |
| 继承的纹理与数组：`glGenTextures`, `glDeleteTextures`, `glBindTexture`, `glTexImage1D`, `glTexImage2D`, `glTexSubImage*`, `glTexParameter*`, `glDrawArrays`, `glDrawElements`, `glVertexPointer`, `glColorPointer`, `glNormalPointer`, `glTexCoordPointer`, `glEnableClientState` | 早期纹理对象和 client-side vertex arrays。 | 资源属于 context 共享组；client pointer 不可跨生命周期保存，Core/ES 不可用。 |
| 继承的状态与查询：`glViewport`, `glScissor`, `glEnable`, `glDisable`, `glClear*`, `glDepth*`, `glStencil*`, `glBlendFunc`, `glGet*`, `glGetError`, `glReadPixels`, `glPixelStore*`, `glFlush`, `glFinish` | 配置 output state、查询状态和传统像素传输。 | 状态作用于 current context；读回和强同步不要放进热路径。 |
| 继承的 fixed pipeline：`glMatrixMode`, `glLoad*`, `glBegin`, `glEnd`, `glVertex*`, `glColor*`, `glNormal*`, `glTexCoord*`, `glLight*`, `glMaterial*`, `glFog*`, `glTexEnv*`, `glTexGen*`, `glMap*`, `glEval*`, `glNewList`, `glCallList*` | 固定变换、光照、立即模式和其他 legacy 功能。 | 仅为维护存在；迁移到 shader、VBO/VAO 与现代 resource API。 |

## 常见误区

### 误把 `glMultiDrawElements()` 的索引数组当作二维连续索引

参数是“指针数组”，每个元素表示一批的 index 起点。它既不是一大段 indices 的自动分片，也不会替你检查每批 count 是否越界。

### 让 straight-alpha 贴图走 premultiplied 混合规则

RGB 和 Alpha 分离后更容易掩盖组合错误。应先确认图片资源是否已预乘，再为 RGB 和 Alpha 各自选择 factor，并在目标 framebuffer 上实际验证边缘。

### 使用第二颜色和雾坐标，期待 shader 自动接收

这些是 fixed-function 语义。shader pipeline 不会把它们自动翻译为你的 vertex input；需要显式定义 attribute location、数据布局和计算逻辑。

## 一句话总结

`QOpenGLFunctions_1_4` 是维护旧多批绘制和旧混合/点渲染路径的 Qt 包装层。它的价值在于清晰加载和隔离 compatibility API，而不是把 fixed-function 时代的状态机延续为现代渲染架构。
