# QOpenGLFunctions_3_2_Compatibility 类笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QOpenGLFunctions_3_2_Compatibility>`  
> 所属模块：`Qt6::OpenGL`  
> 继承：`QAbstractOpenGLFunctions`  
> 可用性：仅匹配桌面 OpenGL 3.2 Compatibility profile；包含 OpenGL 3.2 Core 函数及 1.x--3.1 的遗留 fixed-function 接口

## 它解决什么问题

`QOpenGLFunctions_3_2_Compatibility` 为当前 OpenGL 3.2 Compatibility context 提供完整的版本化函数包装。它既包含 Core 版的 VAO、FBO、UBO、实例化、multisample texture 和 sync fence，也保留了旧程序依赖的立即模式、矩阵栈、固定光照、client state、display list、selection/feedback 与 imaging subset。

它解决的是“无法一次性重写的遗留 renderer 如何在 Qt 中继续运行并逐步迁移”的问题。与 Core 版不同，Compatibility 版允许旧函数存在；但这只是迁移缓冲，不是推荐的新架构。新代码应只使用与 `QOpenGLFunctions_3_2_Core` 重叠的现代成员，把 legacy 调用局限在隔离模块。

## 什么时候选择它

- 正在维护 `glBegin()`、`glMatrixMode()`、`glLight*()` 或 `glVertexPointer()` 的桌面插件；
- 旧渲染路径需要 3.2 的 FBO/sync/multisample 能力，但暂时不能剥离 fixed pipeline；
- 需要为历史 CAD、科学可视化或模型查看器建立可控的迁移边界。

请求了 Core profile、运行在只支持 Core 的系统路径，或计划支持 OpenGL ES 时，不应使用本类。

## 初始化与迁移式使用

```cpp
#include <QOpenGLFunctions_3_2_Compatibility>

QOpenGLFunctions_3_2_Compatibility gl;

bool initializeLegacyBridge()
{
    if (!gl.initializeOpenGLFunctions())
        return false;

    // 旧路径可暂时存在，但新绘制应走 VAO/VBO/shader。
    gl.glEnable(GL_DEPTH_TEST);
    return true;
}
```

初始化必须发生在匹配的 Compatibility context current 时。不要以“函数对象包含 legacy 成员”为理由让新模块继续写 fixed-function 代码；应标记旧入口并逐步迁移为 shader、buffer、VAO 和 Core profile。

## Core 与 Compatibility 的实际差异

两类 3.2 函数对象共享 OpenGL 3.2 及此前所有 Core API，例如 `glFenceSync()`、`glTexImage2DMultisample()`、`glFramebufferTexture()`、`glBindVertexArray()`、UBO 和 GLSL API。

区别在于本类还暴露 deprecated 后端：`glBegin`/`glEnd`、`glVertex*`、`glColor*`、`glNormal*`、矩阵栈、fixed-function light/material/fog、client array、display list、evaluator、selection/feedback、color table/convolution/histogram/minmax、多纹理坐标和 window raster path。它们在 Core 类中不存在。

迁移顺序通常是：先把几何提交从立即模式/client array 转为 VBO + generic attribute；再把矩阵、光照和纹理组合转到 shader；最后移除 display list、pixel/imaging 与 selection 等旧状态机，改用明确的 FBO、GPU picking 或 CPU 逻辑。

## 3.2 Core 功能的关键边界

### 多重采样与 FBO

`glTexImage2DMultisample()`、`glTexImage3DMultisample()`、`glSampleMaski()`、`glGetMultisamplefv()` 配置 MSAA texture；`glFramebufferTexture()` 把 texture level 连接到 FBO。多重采样结果通常需要 `glBlitFramebuffer()` resolve 后才能作为普通纹理采样。

### Fence 与 base-vertex

`glFenceSync()`、`glClientWaitSync()`、`glWaitSync()`、`glDeleteSync()` 管理 GPU 命令完成点；`glDrawElementsBaseVertex()` 及其 range/instanced/multi-draw 变体让子网格用局部索引复用大顶点 buffer。等待 fence 不应无限阻塞；base vertex 加索引后的最终地址不可越界。

### Legacy 状态与现代状态会互相污染

Compatibility context 允许旧 state，但它仍是同一个全局 OpenGL 状态机。固定管线 texture environment、matrix mode、client state 和 shader/VAO 路径混用时，问题常来自隐式绑定和不可见状态残留。把两条路径分为独立 draw 函数，显式设定所需状态。

## API 速查表

| 功能族（成员 API） | 是做什么的 | 使用时重点注意 |
| --- | --- | --- |
| `initializeOpenGLFunctions()` | 解析 current 3.2 Compatibility profile 函数。 | profile 不匹配时会失败；该对象不能替代 Core profile 检查。 |
| 3.2 multisample：`glTexImage2DMultisample`, `glTexImage3DMultisample`, `glSampleMaski`, `glGetMultisamplefv` | 创建/控制 multisample texture。 | MSAA texture 需 resolve 或显式 sample fetch，不能当普通 filtered texture。 |
| 3.2 sync：`glFenceSync`, `glIsSync`, `glDeleteSync`, `glClientWaitSync`, `glWaitSync`, `glGetSynciv`, `glGetInteger64v` | 建立并等待 GPU 完成点。 | 优先非阻塞或有限超时；它不代替 CPU 线程同步。 |
| 3.2 indexed draw：`glDrawElementsBaseVertex`, `glDrawRangeElementsBaseVertex`, `glDrawElementsInstancedBaseVertex`, `glMultiDrawElementsBaseVertex` | 在 index 基础上叠加 base vertex 绘制。 | EBO 绑定时 indices 是字节 offset；所有结果索引必须有效。 |
| 3.2 FBO/状态：`glFramebufferTexture`, `glProvokingVertex`, `glGetBufferParameteri64v`, `glGetInteger64i_v` | 通用 texture attachment、flat varying 来源和 64 位状态查询。 | attachment 后检查 FBO；provoking vertex 只影响 flat interpolation。 |
| 继承的现代资源：`glGenVertexArrays`, `glBindVertexArray`, `glGenFramebuffers`, `glBindFramebuffer`, `glFramebufferTexture*`, `glRenderbufferStorage*`, `glBlitFramebuffer`, `glMapBufferRange`, `glBeginTransformFeedback`, `glDraw*Instanced`, `glTexBuffer` | VAO/FBO、映射 buffer、transform feedback、实例化和 buffer texture。 | 新代码应优先只使用这一组及 shader/UBO API。 |
| 继承的 GLSL/UBO：`glCreateShader`, `glCompileShader`, `glLinkProgram`, `glUseProgram`, `glVertexAttribPointer`, `glUniform*`, `glGetUniformBlockIndex`, `glUniformBlockBinding`, `glBindBufferBase`, `glBindBufferRange` | 构建 shader、顶点输入和 uniform buffer 数据流。 | compile/link 要检查；block index 与 binding point 不同，range 有对齐限制。 |
| legacy 几何与矩阵：`glBegin`, `glEnd`, `glVertex*`, `glColor*`, `glNormal*`, `glTexCoord*`, `glMatrixMode`, `glLoad*`, `glMultMatrix*`, `glTranslate*`, `glRotate*`, `glScale*` | 立即模式与固定矩阵栈。 | 只能在 compatibility context；新路径迁移到 VBO/VAO、shader uniform。 |
| legacy 光照/纹理：`glLight*`, `glMaterial*`, `glFog*`, `glTexEnv*`, `glTexGen*`, `glMultiTexCoord*`, `glClientActiveTexture` | 固定管线光照、雾与多纹理。 | 不可用于 Core/ES；不要与 shader 状态混杂依赖。 |
| legacy 数组/像素：`glVertexPointer`, `glColorPointer`, `glTexCoordPointer`, `glEnableClientState`, `glDrawPixels`, `glCopyPixels`, `glColorTable*`, `glConvolution*`, `glHistogram*`, `glMinmax*` | client arrays 与传统像素/imaging 路径。 | CPU 指针生命周期和 pixel-store 易出错；查询/读回会同步。 |
| legacy 其他：`glNewList`, `glCallList*`, `glMap*`, `glEval*`, `glRenderMode`, `glSelectBuffer`, `glFeedbackBuffer`, `glPushAttrib`, `glPopAttrib` | display list、evaluator、selection/feedback 与状态栈。 | 仅为遗留维护；逐步替换，不让新模块依赖。 |

## 常见误区

### 把 Compatibility 当作“Core 的超集，所以新旧调用随便混”

两套调用共享全局状态，混搭使调试成本迅速上升。Compatibility 的正确用法是给旧代码一个隔离区，同时让新代码坚持 Core 风格。

### 为了 legacy 保留 Compatibility profile，却在 Core-only 平台上部署

某些平台路径只提供 Core context。应在启动期明确检测 format/profile，必要时禁用旧 renderer 或走替代实现。

### 用 fence 修复所有渲染错误

fence 只解决命令完成时序，不会修复错误的 attachment、attribute layout、资源共享或 legacy state 污染。

## 一句话总结

`QOpenGLFunctions_3_2_Compatibility` 是让遗留 OpenGL 代码在 Qt 中继续运行并逐步迁移的过渡包装；它的价值在于隔离旧状态机，而真正长期的目标仍应是 `QOpenGLFunctions_3_2_Core` 所代表的纯现代管线。
