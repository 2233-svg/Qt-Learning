# Qt OpenGL（下）：纹理、FBO、离屏渲染与线程

## 1. QOpenGLTexture

```cpp
QOpenGLTexture texture(QImage(QStringLiteral(":/images/logo.png")));
texture.setMinificationFilter(QOpenGLTexture::LinearMipMapLinear);
texture.setMagnificationFilter(QOpenGLTexture::Linear);
texture.setWrapMode(QOpenGLTexture::ClampToEdge);
```

纹理创建必须在当前上下文中完成。图片格式、颜色空间和垂直方向要与 shader 的采样约定一致；上传大纹理会阻塞，应在初始化或后台准备阶段完成。

```cpp
program.bind();
texture.bind(0);
program.setUniformValue("tex", 0);
glDrawElements(GL_TRIANGLES, indexCount, GL_UNSIGNED_INT, nullptr);
texture.release();
program.release();
```

纹理单元是上下文状态，绘制前显式绑定，避免依赖上一帧的残留状态。

## 2. QOpenGLFramebufferObject

FBO 将绘制目标从窗口切换到纹理/渲染缓冲，可用于后处理、截图、阴影和离屏计算：

```cpp
QOpenGLFramebufferObjectFormat format;
format.setAttachment(QOpenGLFramebufferObject::CombinedDepthStencil);
QOpenGLFramebufferObject fbo(QSize(1024, 768), format);

fbo.bind();
glViewport(0, 0, fbo.width(), fbo.height());
glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
renderScene();
fbo.release();
```

绘制到 FBO 后要恢复默认帧缓冲和窗口视口。`QOpenGLFramebufferObject::toImage()` 可读取结果，但会触发 GPU 到 CPU 的同步，频繁调用会很慢。

## 3. 多重采样和解析

```cpp
QOpenGLFramebufferObjectFormat format;
format.setSamples(4);
format.setAttachment(QOpenGLFramebufferObject::CombinedDepthStencil);
QOpenGLFramebufferObject msaa(size, format);
```

多重采样 FBO 不能直接当作普通纹理采样，通常需要 blit/resolve 到单采样 FBO。Qt 提供 `QOpenGLFramebufferObject::blitFramebuffer()`，但源、目标尺寸和格式必须兼容。

## 4. 离屏渲染与资源读取

```cpp
QOpenGLContext context;
context.setFormat(format);
context.create();

QOffscreenSurface surface;
surface.setFormat(context.format());
surface.create();

context.makeCurrent(&surface);
// 创建共享纹理、FBO 或执行离屏绘制
context.doneCurrent();
```

`QOffscreenSurface` 只提供可使上下文当前化的表面，不保证有可见窗口。它的格式应与上下文匹配，且通常要在使用它的线程创建或移动到该线程。

## 5. 上下文与线程

一个 `QOpenGLContext` 一次只能在一个线程中当前化。将上下文移动到工作线程前，先在原线程 `doneCurrent()`；目标线程需要有自己的事件循环和兼容的表面。

```cpp
context.doneCurrent();
context.moveToThread(workerThread);

// 在 workerThread 中
context.makeCurrent(&offscreenSurface);
uploadData();
context.doneCurrent();
```

`QOpenGLWidget` 的上下文由 GUI 线程管理，不应在工作线程直接调用其 OpenGL 函数。后台线程可以准备 CPU 数据，或使用共享上下文上传资源，但必须明确同步和所有权。

## 6. 共享上下文和同步

共享上下文可以共享纹理、缓冲等对象，但不是所有状态都共享。创建共享上下文时设置 `setShareContext()`，并使用 `glFenceSync`、Qt 信号或线程同步原语协调生产者和消费者。

不要在一个线程删除另一个线程仍在使用的纹理。最简单的策略是由创建线程统一销毁，或用引用计数和明确的“停止上传→等待 GPU→销毁”协议。

## 7. 读取像素与截图

```cpp
QImage image(size, QImage::Format_RGBA8888);
glReadPixels(0, 0, size.width(), size.height(),
             GL_RGBA, GL_UNSIGNED_BYTE, image.bits());
image = image.mirrored(); // OpenGL 原点通常在左下
```

`glReadPixels` 是同步操作，可能等待 GPU 完成。截图功能不应放在每帧路径；导出时暂停动画、降低分辨率或使用异步 PBO（若后端支持）减少卡顿。

## 8. 与 Qt Quick 场景图互操作

Qt Quick 使用 RHI 抽象层，默认后端不一定是 OpenGL。需要在 Qt Quick 中插入 OpenGL 内容时，应评估 `QQuickFramebufferObject`、`QQuickRhiItem` 或 RHI 原生接口，并遵循场景图渲染线程规则。

不要假设 `QQuickWindow` 永远使用 OpenGL；Vulkan、Metal、Direct3D 和软件后端都可能被选择。跨后端功能应优先使用 RHI，而不是直接调用 OpenGL。

## 9. 调试 OpenGL

```cpp
QOpenGLDebugLogger logger;
if (logger.initialize()) {
    connect(&logger, &QOpenGLDebugLogger::messageLogged,
            [](const QOpenGLDebugMessage &message) {
        qWarning() << message;
    });
    logger.startLogging();
}
```

调试 logger 需要驱动支持。还应在开发环境检查 `glGetString(GL_VENDOR)`、`GL_RENDERER` 和版本，记录实际 GPU 与后端，方便复现驱动相关问题。

## 10. 资源重建策略

窗口最小化、屏幕切换或驱动重置可能导致上下文资源失效。把资源创建集中在 `initializeGL()` 或独立的 `createResources()`，把销毁集中在 `cleanup()`，并允许重复调用：

```cpp
void Renderer::recreate()
{
    cleanup();
    createResources();
}
```

创建函数应检查 shader、纹理、FBO 和 VAO 状态，失败时返回明确错误而不是继续绘制半初始化资源。

## 11. Qt 6 图形后端选择

Qt 6 的 Qt Quick 默认使用 RHI；Widgets 的 `QOpenGLWidget` 仍直接使用 OpenGL。Windows 上 OpenGL-proper 是直接 OpenGL 路径，不能依赖 Qt 5 时代的 ANGLE 自动回退。若目标设备 OpenGL 能力不稳定，应评估 RHI 或纯软件绘制方案。

## 12. 常见问题

| 现象 | 原因 | 处理 |
| --- | --- | --- |
| FBO 绘制结果为空 | 未绑定、视口仍是窗口尺寸或未恢复 | 检查 bind/release 与 viewport |
| 纹理上下颠倒 | OpenGL 原点在左下 | 在上传或显示阶段统一翻转约定 |
| 后台上传崩溃 | QOpenGLWidget 上下文跨线程使用 | 使用共享上下文和明确线程协议 |
| 截图卡顿 | glReadPixels 同步等待 | 降低频率、分辨率或采用异步读取 |
| QML OpenGL 内容失效 | Qt Quick 改用非 OpenGL RHI 后端 | 使用 RHI 接口或强制并验证后端 |
| shader 在一台机器失败 | GLSL 版本/扩展不一致 | 检查实际上下文格式并提供备用 shader |

## 13. 自测题

1. FBO 适合解决什么问题？
2. 为什么 QOffscreenSurface 不代表可见窗口？
3. QOpenGLContext 跨线程移动前需要做什么？
4. glReadPixels 为什么不适合每帧调用？
5. Qt Quick 中为什么不能假设底层永远是 OpenGL？

### 参考答案

1. 离屏绘制、后处理、截图和把场景渲染到纹理。
2. 它只提供上下文当前化所需的离屏表面，没有窗口显示能力。
3. 在原线程 `doneCurrent()`，再移动到目标线程并在目标线程重新 current。
4. 它会同步等待 GPU 完成并复制数据到 CPU，容易阻塞渲染。
5. Qt 6 Quick 使用 RHI，可选择 Vulkan、Metal、Direct3D、OpenGL 或软件后端。

## 14. 小结

OpenGL 高级开发的关键是把资源、上下文、线程和后端选择分开管理。纹理与 FBO 提供离屏能力，共享上下文解决部分后台上传需求，但必须配合同步协议；Qt Quick 场景图则应优先使用 RHI 抽象，以保持跨后端能力。
