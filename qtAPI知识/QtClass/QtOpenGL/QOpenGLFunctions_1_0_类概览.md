# QOpenGLFunctions_1_0 类笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QOpenGLFunctions_1_0>`  
> 所属模块：`Qt6::OpenGL`  
> 继承：`QAbstractOpenGLFunctions`  
> 可用性：桌面 OpenGL 的旧式兼容 API；不适用于 OpenGL ES 2 构建，也不适用于只提供 Core profile 的 context

## 它解决什么问题

`QOpenGLFunctions_1_0` 把 OpenGL 1.0 规范的函数地址包装为 C++ 成员函数。它的用途是避免在 Windows 等平台手工解析 OpenGL 函数指针，并将“当前 context 是否支持这套旧式 API”集中到 `initializeOpenGLFunctions()` 的返回值。

这不是现代着色器渲染 API。该类除了早期的 OpenGL 1.0 core 函数，还暴露了 fixed-function pipeline、立即模式、矩阵栈、display list、selection/feedback、光照和 evaluator 等历史接口。它们在 OpenGL 3.1 后被移除，在 Core profile 与 OpenGL ES 中不可用。

## 什么时候使用

- 维护依赖 `glBegin()` / `glEnd()`、`glMatrixMode()`、固定管线光照的旧桌面应用；
- 需要在 Qt 中把旧式桌面 OpenGL 调用走版本化函数对象，而非裸函数指针；
- 做遗留渲染代码的迁移和诊断。

新项目应优先使用 `QOpenGLFunctions`、`QOpenGLExtraFunctions` 或与所请求 Core profile 匹配的 `QOpenGLFunctions_<版本>_Core`，使用 VAO/VBO、shader 和 programmable pipeline。

## 初始化与最小示例

```cmake
find_package(Qt6 REQUIRED COMPONENTS OpenGL)
target_link_libraries(mytarget PRIVATE Qt6::OpenGL)
```

```cpp
#include <QOpenGLFunctions_1_0>

QOpenGLFunctions_1_0 gl;

void initializeLegacyRenderer()
{
    if (!gl.initializeOpenGLFunctions()) {
        // 当前 context 不是可兼容的桌面 OpenGL legacy context。
        return;
    }

    gl.glClearColor(0.1f, 0.1f, 0.1f, 1.0f);
    gl.glEnable(GL_DEPTH_TEST);
}
```

调用初始化与任一 `gl*` 成员时，正确的 `QOpenGLContext` 必须在调用线程 current。对象不能跨不兼容 context 复用。

## 关键边界

### 旧式 API 需要兼容性 context

类中 `glBegin`、矩阵栈、固定管线光照、client state、display list 等函数都依赖已废弃的 OpenGL 功能。OpenGL 3.2+ 的 Core profile、macOS 的 Core-only 路径与 OpenGL ES 不应使用此类。

### 同一类同时含“核心”和“deprecated”接口

Qt 头文件将其分为 OpenGL 1.0 core 函数与 1.0 deprecated 函数。不要因为对象能成功初始化，就忽略实际 context/profile 对 legacy 调用的限制；迁移代码时优先替换 deprecated 部分。

### `glFinish()` 是同步栅栏

`glFlush()` 只保证命令送出，`glFinish()` 会等待所有先前 OpenGL 命令完成，极易阻塞 CPU/GPU 并发。调试或极少数同步交互场景外，不应放在每帧路径。

### 像素读回与即时模式都很昂贵

`glReadPixels()`、`glGetTexImage()` 可能触发 GPU->CPU 同步；`glBegin()`/`glEnd()` 与逐顶点函数会产生大量驱动调用。它们适合维护遗留代码，不适合现代高吞吐渲染。

## 使用模型

1. 创建 legacy/compatibility desktop context 并令其 current；
2. `initializeOpenGLFunctions()` 并检查返回值；
3. 设置 viewport、clear、depth/stencil、blend/cull 等状态；
4. 使用纹理、固定矩阵/光照或立即模式进行旧式绘制；
5. 用 `glGetError()` 在调试阶段排查错误，避免把它作为高频业务控制流；
6. 逐步迁移到 shader、buffer object 和现代函数类。

## API 速查表

下表按一个实际 OpenGL 操作族逐项列出此类的全部成员名字。后缀 `f`、`d`、`i`、`s`、`b`、`ub` 只表示参数数值类型或向量指针变体；它们改变精度/输入形式，不改变该操作族的状态语义。

| 功能族（成员 API） | 是做什么的 | 使用时重点注意 |
| --- | --- | --- |
| `initializeOpenGLFunctions()` | 解析当前 context 的 1.0/legacy 函数地址。 | 必须有兼容的 current desktop context；失败后不得调用任何成员。 |
| `glGetString`, `glGetIntegerv`, `glGetFloatv`, `glGetDoublev`, `glGetBooleanv`, `glIsEnabled`, `glGetError` | 查询驱动、限制和状态。 | 输出指针须有足够空间；`glGetError` 会消费错误队列。 |
| `glViewport`, `glScissor`, `glEnable`, `glDisable`, `glHint`, `glFlush`, `glFinish` | 设定视口、裁剪、能力开关、提示与提交。 | scissor 仅在 `GL_SCISSOR_TEST` 启用时生效；避免每帧 `glFinish`。 |
| `glClearColor`, `glClearDepth`, `glClearStencil`, `glClearIndex`, `glClearAccum`, `glClear`, `glColorMask`, `glDepthMask`, `glStencilMask`, `glIndexMask` | 设置 clear 值、清空缓冲并限制写掩码。 | 写掩码会影响 `glClear`；使用 FBO 时清的是当前绑定目标。 |
| `glDepthRange`, `glDepthFunc`, `glStencilFunc`, `glStencilOp`, `glLogicOp`, `glBlendFunc`, `glAlphaFunc` | 配置深度、模板、逻辑运算、混合和 alpha test。 | alpha test/logic op 属旧式路径；blend factor 与 premultiplied alpha 要匹配。 |
| `glFrontFace`, `glCullFace`, `glPolygonMode`, `glPolygonStipple`, `glPointSize`, `glLineWidth`, `glLineStipple` | 配置面剔除和栅格化外观。 | `glPolygonMode`、line stipple 等在 Core/ES 不可用；线宽常被驱动限制。 |
| `glReadBuffer`, `glDrawBuffer`, `glReadPixels`, `glDrawPixels`, `glCopyPixels`, `glPixelStorei`, `glPixelStoref`, `glPixelTransferi`, `glPixelTransferf`, `glPixelZoom`, `glPixelMap*` | 设置像素打包/解包并进行读回、绘制、复制和转换。 | `glReadPixels` 易触发同步；`GL_PACK_ALIGNMENT`/`GL_UNPACK_ALIGNMENT` 必须和行跨度一致。 |
| `glTexImage1D`, `glTexImage2D`, `glTexParameter{f,i,fv,iv}`, `glGetTexParameter{fv,iv}`, `glGetTexLevelParameter{fv,iv}`, `glGetTexImage` | 分配、配置、查询和读回 1D/2D 纹理。 | 先绑定正确 target；旧硬件/旧 profile 对非 2 次幂纹理有限制；读回开销高。 |
| `glTexEnv{f,i,fv,iv}`, `glGetTexEnv{fv,iv}`, `glTexGen{d,f,i,dv,fv,iv}`, `glGetTexGen{dv,fv,iv}` | 设置固定管线纹理环境与自动坐标生成。 | 都是 fixed-function API；现代渲染改用 shader uniform/attribute。 |
| `glMatrixMode`, `glLoadIdentity`, `glLoadMatrix{f,d}`, `glMultMatrix{f,d}`, `glTranslate{f,d}`, `glRotate{f,d}`, `glScale{f,d}`, `glFrustum`, `glOrtho`, `glPushMatrix`, `glPopMatrix` | 操作 model-view/projection/texture 矩阵栈。 | 仅 compatibility；矩阵栈深度有限，push/pop 必须平衡。 |
| `glLight{f,i,fv,iv}`, `glLightModel{f,i,fv,iv}`, `glMaterial{f,i,fv,iv}`, `glColorMaterial`, `glShadeModel`, `glFog{f,i,fv,iv}`, `glClipPlane` | 固定管线光照、材质、雾和裁剪平面。 | 仅 compatibility；新代码把这些数据传给 shader。 |
| `glBegin`, `glEnd`, `glVertex2*`, `glVertex3*`, `glVertex4*`, `glColor3*`, `glColor4*`, `glNormal3*`, `glTexCoord1*`, `glTexCoord2*`, `glTexCoord3*`, `glTexCoord4*`, `glEdgeFlag*`, `glRect*` | 立即模式逐顶点提交与当前顶点属性。 | 只能在 `glBegin`/`glEnd` 间调用允许的顶点属性函数；禁止用于现代/Core/ES。 |
| `glRasterPos2*`, `glRasterPos3*`, `glRasterPos4*`, `glBitmap` | 设置 raster position 和位图像素操作位置。 | 属遗留像素栅格路径；会受裁剪与变换状态影响。 |
| `glMap1{f,d}`, `glMap2{f,d}`, `glMapGrid1{f,d}`, `glMapGrid2{f,d}`, `glEvalCoord1*`, `glEvalCoord2*`, `glEvalPoint1`, `glEvalPoint2`, `glEvalMesh1`, `glEvalMesh2`, `glGetMap{fv,iv,dv}` | 配置并评估多项式曲线/曲面。 | evaluator 仅 compatibility，需校验 control point 的 stride/order。 |
| `glNewList`, `glEndList`, `glCallList`, `glCallLists`, `glGenLists`, `glDeleteLists`, `glIsList`, `glListBase` | 创建、调用与管理 display list。 | display list 是旧式 GPU 命令缓存，资源生命周期与 context 绑定，现代代码改用 VBO/VAO。 |
| `glRenderMode`, `glSelectBuffer`, `glFeedbackBuffer`, `glInitNames`, `glLoadName`, `glPushName`, `glPopName`, `glPassThrough` | selection/feedback 旧式几何反馈模式。 | 容易溢出，且已被现代 GPU picking/transform feedback 等方案取代。 |
| `glAccum` | 操作 accumulation buffer。 | 旧式功能，现代硬件/驱动支持与性能均不可假设。 |
| `glPushAttrib`, `glPopAttrib` | 保存/恢复服务器端状态集合。 | 仅 compatibility；掩码与栈深度限制需要匹配。 |

### 一句话总结

`QOpenGLFunctions_1_0` 是把完整 OpenGL 1.0 与其 legacy compatibility 功能封装为可初始化成员函数的过渡工具；它适合维护和迁移旧代码，不适合作为现代 OpenGL 渲染架构的起点。
