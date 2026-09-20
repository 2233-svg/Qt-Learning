# QOpenGLFunctions_1_1 类笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QOpenGLFunctions_1_1>`  
> 所属模块：`Qt6::OpenGL`  
> 继承：`QAbstractOpenGLFunctions`  
> 可用性：桌面 OpenGL 1.1 compatibility API；不适用于 OpenGL ES 2 构建和 Core-only context

## 它解决什么问题

`QOpenGLFunctions_1_1` 在 `QOpenGLFunctions_1_0` 的完整 1.0 与 legacy API 之上，增加 OpenGL 1.1 的纹理对象、子区域纹理更新、数组绘制和 client-side vertex array 接口。它将这些调用的运行时函数解析放入 `initializeOpenGLFunctions()`，避免手工处理函数指针。

从现代视角看，这仍是一套兼容性工具：OpenGL 1.1 新增的 `glGenTextures()`、`glBindTexture()`、`glDrawArrays()`、`glDrawElements()` 仍有维护遗留代码的价值，但 client state / fixed-function 部分不适用于现代 Core profile 或 OpenGL ES 2+ 渲染路径。

## 实际使用场景

- 维护基于 `glVertexPointer()`、`glDrawArrays()`、`glDrawElements()` 的老桌面渲染器；
- 把旧式纹理 ID 和纹理子更新调用纳入 Qt 的版本化函数对象；
- 分阶段迁移：先从立即模式迁移到 vertex array，再迁移到 VBO/VAO、shader 与现代 Core profile。

新代码不应以 client-side arrays 为目标架构。它们依赖旧式 client state，且 CPU 指针的生命周期与图形调用严格耦合。

## 初始化与最小示例

```cpp
#include <QOpenGLFunctions_1_1>

QOpenGLFunctions_1_1 gl;

bool initialize()
{
    if (!gl.initializeOpenGLFunctions())
        return false;

    GLuint texture = 0;
    gl.glGenTextures(1, &texture);
    gl.glBindTexture(GL_TEXTURE_2D, texture);
    return true;
}
```

初始化以及后续调用都要求兼容的桌面 OpenGL context 在当前线程 current。`QOpenGLFunctions_1_1` 继承了 1.0 的所有接口与风险。

## 相比 1.0 新增了什么

### 纹理对象和局部更新

1.1 引入显式纹理对象管理：`glGenTextures()`、`glDeleteTextures()`、`glBindTexture()` 和 `glIsTexture()`。它还支持 `glTexSubImage*()` 局部上传，以及 `glCopyTexImage*()`/`glCopyTexSubImage*()` 从 framebuffer 复制内容到纹理。

纹理对象 ID 与 context/共享组关联。删除 ID 后不要继续绑定或采样；上传时同样要正确设置 pixel unpack state。

### 批量绘制

`glDrawArrays()` 以连续顶点范围提交，`glDrawElements()` 通过索引数组提交。两者是从立即模式迁出的早期一步，但传入的 pointer 在旧 client array 模型中仍通常是 CPU 内存地址。

### Client-side vertex arrays

`glVertexPointer()`、`glColorPointer()`、`glNormalPointer()`、`glTexCoordPointer()` 等定义属性数组，`glEnableClientState()` 启用它们。它们是 deprecated compatibility API，且 `pointer` 指向的数据必须在 draw 调用返回前保持有效。

## 关键边界

### 不要把 client array 指针当作持久 GPU 资源

当未使用 buffer object 时，`pointer` 是进程地址。渲染线程、异步绘制、临时容器重分配或函数返回都可能让它失效。现代代码应上传数据到 VBO 并用顶点属性 API。

### `glDrawElements()` 的 indices 解释依赖绑定状态

在传统 client array 模式下 `indices` 是 CPU 指针；在后来绑定 element array buffer 的路径中，同一个参数会被解释为 buffer 内字节偏移。维护混合年代代码时必须明确当前 buffer binding，避免误把地址当 offset。

### `glCopyTex*()` 读取当前 read buffer

从 framebuffer 复制纹理时，来源由当前读取状态、视口和坐标决定，常受像素格式、FBO、scissor 和同步影响。需要离屏渲染时，优先考虑 FBO + blit 或 shader copy。

### `glPolygonOffset()` 不是万能消除 z-fighting 的开关

offset 与深度斜率及单位相关，对不同投影、深度格式和驱动的结果不同。它应只在真正的 coplanar depth conflict 场景中局部启用。

## API 速查表

`QOpenGLFunctions_1_1` 包含下表的 1.1 新增操作，并完整继承 `QOpenGLFunctions_1_0` 的操作族。为避免把同一函数的数值类型重载拆成数百行，表内同一操作族明确列出每个成员名称。

| 功能族（成员 API） | 是做什么的 | 使用时重点注意 |
| --- | --- | --- |
| `initializeOpenGLFunctions()` | 解析 current context 的 1.1 compatibility 函数地址。 | 初始化失败后不能调用 1.1 或继承的 1.0 成员。 |
| `glIndexub`, `glIndexubv` | 设置无符号字节 color index。 | 属颜色索引旧式渲染模型，现代 RGBA 渲染无需使用。 |
| `glGenTextures`, `glDeleteTextures`, `glBindTexture`, `glIsTexture` | 创建、删除、绑定和检查纹理对象。 | ID 属 context 共享组；删除后不可继续使用；绑定 target 必须一致。 |
| `glTexSubImage1D`, `glTexSubImage2D` | 更新已有纹理的局部区域。 | 目标 mip level 与区域必须已存在；注意 unpack alignment、格式和边界。 |
| `glCopyTexImage1D`, `glCopyTexImage2D` | 从当前 read buffer 创建/覆盖完整纹理 level。 | 读取来源是当前 framebuffer；可能受格式转换、裁剪和同步影响。 |
| `glCopyTexSubImage1D`, `glCopyTexSubImage2D` | 从当前 read buffer 复制到已有纹理的子区域。 | 目标区域必须存在；坐标按 OpenGL framebuffer 原点解释。 |
| `glPolygonOffset` | 对多边形深度值加基于斜率/单位的偏移。 | 仅用于局部解决 coplanar z-fighting；须配合 `GL_POLYGON_OFFSET_*` 开关。 |
| `glDrawArrays` | 以连续顶点序列批量绘制。 | 依赖已启用的 client state / 旧顶点数组；first/count 不可越过数据范围。 |
| `glDrawElements` | 根据索引数组批量绘制。 | indices 是 CPU 指针还是 element buffer offset 取决于绑定状态；type/count 必须正确。 |
| `glGetPointerv` | 查询 client array 指针等旧状态。 | 得到的是旧 client-state 信息，不适合构建现代资源管理。 |
| `glVertexPointer`, `glColorPointer`, `glNormalPointer`, `glTexCoordPointer`, `glIndexPointer`, `glEdgeFlagPointer` | 定义旧 client-side attribute arrays。 | pointer 内存必须在 draw 前有效；接口已废弃，Core/ES 不可用。 |
| `glEnableClientState`, `glDisableClientState`, `glPushClientAttrib`, `glPopClientAttrib` | 启用、禁用、保存或恢复 client-side state。 | push/pop 必须平衡；client state 与 Core profile/现代 VAO 模型不兼容。 |
| `glInterleavedArrays` | 一次性定义固定格式的交错 client arrays。 | 格式固定且限制多，适合遗留数据布局，不适合可演化的现代顶点布局。 |
| `glArrayElement` | 从当前数组状态发出单个数组元素。 | 仍是固定管线/legacy 调用，批量 `glDraw*` 通常更合适。 |
| 继承的查询与同步：`glGet*`, `glIsEnabled`, `glGetError`, `glFlush`, `glFinish` | 查询状态、提交命令和调试错误。 | `glGet*`/`glFinish` 可能同步；避免高频路径。 |
| 继承的输出状态：`glViewport`, `glClear*`, `glClear`, `glDepth*`, `glStencil*`, `glBlendFunc`, `glEnable`, `glDisable`, `glScissor`, `glCullFace`, `glFrontFace` | 配置 raster/depth/stencil/blend 与清屏。 | 状态属于 current context，调用次序会影响后续所有绘制。 |
| 继承的纹理与像素：`glTexImage1D`, `glTexImage2D`, `glTexParameter*`, `glGetTex*`, `glReadPixels`, `glPixelStore*`, `glPixelTransfer*`, `glDrawPixels`, `glCopyPixels` | 分配/配置纹理及传统像素路径。 | 读回和像素转换昂贵；严格匹配 pack/unpack 与数据行跨度。 |
| 继承的 legacy fixed pipeline：`glMatrixMode`, `glLoad*`, `glMultMatrix*`, `glTranslate*`, `glRotate*`, `glScale*`, `glBegin`, `glEnd`, `glVertex*`, `glColor*`, `glNormal*`, `glTexCoord*`, `glLight*`, `glMaterial*`, `glFog*`, `glTexEnv*`, `glTexGen*` | 固定变换、光照、纹理环境和立即模式。 | 不可用于 Core profile/ES；迁移目标是 shader、uniform、VBO 与 VAO。 |
| 继承的其他 legacy：`glMap*`, `glEval*`, `glNewList`, `glCallList*`, `glRenderMode`, `glSelectBuffer`, `glFeedbackBuffer`, `glPushAttrib`, `glPopAttrib` | evaluator、display list、selection/feedback 和状态栈。 | 都是兼容性 API，应限制在维护场景并规划替代方案。 |

## 常见误区

### 只从 `glBegin/glEnd` 换成 `glDrawArrays`，却继续使用临时内存

`glDrawArrays` 会在调用时读取已启用数组指针，但这不让 CPU 内存成为 GPU 资源。跨帧、跨线程或异步场景应迁移到 VBO。

### 忽略纹理子更新的 unpack 状态

图像行宽不是默认 4 字节对齐时，需要设置 `GL_UNPACK_ALIGNMENT`；否则 `glTexSubImage2D` 会出现错行、花屏或越界读取。

### 在 Core profile 上尝试 client state

`glEnableClientState` 和 `glVertexPointer` 等 API 不属于 Core profile。请求了 Core context 时应选择现代函数类和现代顶点属性接口。

## 一句话总结

`QOpenGLFunctions_1_1` 为遗留桌面 OpenGL 代码提供了纹理对象、局部纹理更新和数组绘制入口，但它仍属于 compatibility 时代；最有价值的使用方式是安全维护旧代码并逐步迁移到 VBO/VAO/shader。
