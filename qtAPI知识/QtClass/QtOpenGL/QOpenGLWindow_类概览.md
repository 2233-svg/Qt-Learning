# QOpenGLWindow 类笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QOpenGLWindow>`  
> 所属模块：`Qt6::OpenGL`  
> 继承：`QPaintDeviceWindow`  
> 定位：用于 OpenGL 渲染的 `QWindow` 便捷子类，API 风格接近 `QOpenGLWidget`

## 它解决什么问题

`QOpenGLWindow` 是一个专门做 OpenGL 绘制的窗口类。它比手写 `QWindow + QOpenGLContext` 少很多样板代码，又不像 `QOpenGLWidget` 那样依赖 Widgets 模块。它自动管理 OpenGL context、paint 事件、buffer swap，并提供 `initializeGL()`、`resizeGL()`、`paintGL()` 这些熟悉的扩展点。

它适合独立 OpenGL 窗口、工具预览窗口、高性能渲染视图，以及不想引入 Widgets 的 Qt GUI 应用。它不是 scene graph，也不是自动渲染循环；何时重绘仍由 `update()`、暴露事件、vsync 后续调度等机制决定。

## 实际使用场景

- 写一个纯 OpenGL 的独立窗口，而不是嵌在 QWidget 布局中；
- 复用类似 `QOpenGLWidget` 的初始化/resize/paint 结构，但减少 Widgets 依赖；
- 用 `QPainter` 在 OpenGL 窗口上叠加 2D 内容；
- 通过 `frameSwapped()` 信号驱动下一次 `update()`，让动画跟随垂直刷新；
- 需要 partial update 模式，保留上一帧 FBO 内容并只增量重绘一小块。

## 基本结构

```cpp
#include <QOpenGLWindow>
#include <QOpenGLFunctions>

class View : public QOpenGLWindow, protected QOpenGLFunctions
{
    void initializeGL() override
    {
        initializeOpenGLFunctions();
        glClearColor(0.08f, 0.09f, 0.11f, 1.0f);
    }

    void resizeGL(int w, int h) override
    {
        glViewport(0, 0, w, h);
    }

    void paintGL() override
    {
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
    }
};
```

如需深度/模板缓冲，创建原生窗口前用 `setFormat()` 请求，例如深度 24、模板 8。没有请求非零 depth/stencil buffer 时，平台不保证这些缓冲存在。

## 核心生命周期

### `initializeGL()`

第一次 `paintGL()` 或 `resizeGL()` 前调用一次。调用时 context 已 current，因此适合创建 shader、buffer、texture 等 OpenGL 资源。若使用 partial update，内部额外 FBO 在此时未必可用，因此不要在这里发绘制命令，绘制放到 `paintGL()`。

### `resizeGL(int w, int h)`

窗口尺寸变化时调用。它是为了兼容 `QOpenGLWidget` 风格提供的便利钩子；派生类也可以改重写 `resizeEvent()`。文档提醒：这里不一定有 current context；若必须发 OpenGL 命令，先调用 `makeCurrent()`。

### `paintGL()`

真正的 OpenGL 绘制入口。调用前 Qt 已经让 context current、绑定必要 framebuffer，并设置 viewport。除此之外，不会替你清屏或设置 OpenGL 状态。你要自己清除颜色/深度、绑定 program、VAO、texture 等。

### `paintUnderGL()` / `paintOverGL()`

这两个函数分别在 `paintGL()` 前后调用。它们始终绘制到窗口默认 framebuffer。partial update 模式下，`paintGL()` 可能绘制到额外 FBO，再由 Qt blit/blend 到窗口；因此 under/over 和 paintGL 的目标可能不同。

## UpdateBehavior 语义

- `NoPartialUpdate`：默认模式。每次更新都应重绘整个窗口，不额外创建 FBO，行为接近普通 OpenGL `QWindow`，性能最好；
- `PartialUpdateBlit`：内部创建额外 FBO，`paintGL()` 画到该 FBO，随后 blit 到窗口。适合 `QPainter` 增量绘制、希望保留旧内容的场景，但会牺牲性能；
- `PartialUpdateBlend`：类似 `PartialUpdateBlit`，但用带 blending 的纹理四边形把额外 FBO 合成到窗口。支持 alpha 混合，也适用于没有 `glBlitFramebuffer` 的情况，通常比 blit 慢。

大多数实时 OpenGL 渲染应使用默认 `NoPartialUpdate`，每帧完整绘制。partial update 更像 `QOpenGLWidget` 的工作方式，主要服务增量 `QPainter` 绘制。

## 资源清理边界

`QOpenGLWindow` 析构时会让自己的 context current，以便释放资源。但如果你的派生类有 `QOpenGLBuffer`、`QOpenGLShaderProgram` 等成员，它们会在派生类析构阶段结束后、基类析构前按 C++ 规则销毁。文档特别提醒：你可能需要在派生类析构函数里先调用 `makeCurrent()`，再显式销毁这些成员资源。

`makeCurrent()` 即使底层平台窗口已经销毁，也会使用 offscreen surface 帮助资源清理，因此适合在析构路径中调用。

## API 速查表

| API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- |
| `enum UpdateBehavior` | 指定窗口更新策略。 | 默认 `NoPartialUpdate` 最适合完整重绘；partial 模式会引入额外 FBO。 |
| `QOpenGLWindow(UpdateBehavior updateBehavior = NoPartialUpdate, QWindow *parent = nullptr)` | 创建 OpenGL 窗口。 | 创建前可用 `setFormat()` 请求版本、profile、depth/stencil。 |
| `QOpenGLWindow(QOpenGLContext *shareContext, UpdateBehavior updateBehavior = NoPartialUpdate, QWindow *parent = nullptr)` | 创建与指定 context 共享资源的窗口。 | 共享只覆盖可共享 OpenGL 资源；仍要注意 context 生命周期。 |
| `~QOpenGLWindow()` | 销毁窗口并释放资源。 | 派生类成员资源可能要在派生析构中先 `makeCurrent()` 后显式销毁。 |
| `updateBehavior() const` | 返回更新策略。 | 用于判断默认 framebuffer/FBO 语义。 |
| `isValid() const` | 查询 OpenGL 资源是否初始化成功。 | 窗口 expose/show 之前总是 `false`。 |
| `makeCurrent()` | 让窗口 context current，并绑定必要 framebuffer。 | 普通 `paintGL()` 中不需要；高级线程/清理场景使用。 |
| `doneCurrent()` | 释放当前 context。 | 一般由窗口自动处理。 |
| `context() const` | 返回窗口使用的 `QOpenGLContext`。 | 未初始化前可能为 null。 |
| `shareContext() const` | 返回请求共享的 context。 | 表示构造时传入的共享对象，不等于所有资源都可用。 |
| `defaultFramebufferObject() const` | 返回窗口当前默认绘制目标 id。 | `NoPartialUpdate` 通常是平台默认 framebuffer；partial 模式可能是额外 FBO。 |
| `grabFramebuffer()` | 读取 framebuffer 内容为 `QImage`。 | 使用 `glReadPixels()`，可能很慢并阻塞 GPU；`NoPartialUpdate` 下 swap 后内容可能不是屏幕内容。 |
| `frameSwapped()` | buffer swap 完成后发出。 | 连续动画可在该信号中再次 `update()`，跟随 vsync。 |
| `initializeGL()` | 初始化 OpenGL 资源。 | 调用时 context 已 current；partial FBO 还不可用于绘制。 |
| `resizeGL(int w, int h)` | 处理尺寸变化。 | 不一定有 current context；发 GL 命令前先 `makeCurrent()`。 |
| `paintGL()` | 绘制 OpenGL 内容。 | Qt 只保证 context/FBO/viewport；其他状态和清屏由你负责。 |
| `paintUnderGL()` | 在 `paintGL()` 前绘制到底层窗口 framebuffer。 | `PartialUpdateBlit` 下可能被后续 blit 覆盖。 |
| `paintOverGL()` | 在 `paintGL()` 和 partial 合成后绘制到窗口 framebuffer。 | 适合最终 overlay；目标始终是窗口默认 framebuffer。 |
| `paintEvent(QPaintEvent *)` | Qt paint 事件入口，内部调用 `paintGL()`。 | 通常不重写；优先重写 `paintGL()`。 |
| `resizeEvent(QResizeEvent *)` | Qt resize 事件入口，内部调用 `resizeGL()`。 | 需要完全自定义 resize 逻辑时再重写。 |

## 常见误区

### 在 `resizeGL()` 里直接发 OpenGL 命令

`resizeGL()` 不保证 context current。只更新 CPU 侧矩阵/尺寸最稳；必须调用 GL 时先 `makeCurrent()`。

### 以为 `update()` 会立刻调用 `paintGL()`

`update()` 只是调度重绘，多次连续调用不会强制多次立即绘制。连续动画建议用 `frameSwapped()` 后再 `update()`，配合 swap interval/vsync。

### 没请求 depth/stencil buffer

默认 format 不保证有深度或模板缓冲。需要深度测试、模板操作时，在窗口创建前 `setFormat()` 设置 buffer size。

### 在 `grabFramebuffer()` 上做实时截图循环

它依赖 `glReadPixels()`，可能造成 GPU pipeline stall。只适合低频截图、调试或用户主动导出。

## 一句话总结

`QOpenGLWindow` 是独立 OpenGL 窗口的便捷基类；它处理 context 和绘制调度，但渲染状态、资源清理、buffer 格式和 partial update 成本仍需要应用自己掌控。
