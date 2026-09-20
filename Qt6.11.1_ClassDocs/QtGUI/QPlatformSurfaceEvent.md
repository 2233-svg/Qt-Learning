# QPlatformSurfaceEvent

> Qt 6.11.1 · Qt GUI · 来自 `QPlatformSurfaceEvent`

## 1. 先建立直觉

`QPlatformSurfaceEvent` 通知窗口底层的原生 surface 已创建，或即将被销毁。这里的 surface 是平台窗口系统、OpenGL/EGL、Vulkan swapchain 等渲染资源依赖的原生承载面，不等同于 C++ `QWindow` 对象本身。

它最重要的时刻是 `SurfaceAboutToBeDestroyed`：事件返回后原生 surface 可能立刻失效。渲染器必须在这之前停止提交帧、释放依赖 surface 的资源，不能等到窗口对象析构时再做。

## 2. 类说明

`QPlatformSurfaceEvent` 继承自 `QEvent`。通常通过 `QWindow::event()`、事件过滤器或底层渲染窗口代码接收；普通 Widgets 应用一般无需直接处理。

类说明只用于表明这些 API 来自 `QPlatformSurfaceEvent`：它描述 surface 生命周期边界，渲染上下文、swapchain、帧缓冲和 GPU 资源如何创建或销毁由具体图形后端决定。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `enum SurfaceEventType` | 区分原生 surface 已创建与即将销毁。 |
| `QPlatformSurfaceEvent(surfaceEventType)` | 构造 surface 生命周期事件。 |
| `surfaceEventType() const` | 返回事件的具体 surface 生命周期阶段。 |
| `type()` | 来自 `QEvent`，平台 surface 事件通常为 `QEvent::PlatformSurface`。 |

`SurfaceEventType` 主要包含：

| 枚举值 | 说明 |
| --- | --- |
| `SurfaceCreated` | 底层原生 surface 已可用，可以准备依赖该 surface 的渲染资源。 |
| `SurfaceAboutToBeDestroyed` | 原生 surface 即将失效，必须停止提交并释放依赖资源。 |

## 4. 关键用法

### 在销毁前停止渲染

```cpp
bool RenderWindow::event(QEvent *event)
{
    if (event->type() == QEvent::PlatformSurface) {
        auto *surfaceEvent = static_cast<QPlatformSurfaceEvent *>(event);

        if (surfaceEvent->surfaceEventType()
            == QPlatformSurfaceEvent::SurfaceAboutToBeDestroyed) {
            stopRenderLoop();
            releaseSwapchainResources();
        }
    }

    return QWindow::event(event);
}
```

不能把 `SurfaceAboutToBeDestroyed` 当作“将来某个时候再清理”。它就是最后的同步清理窗口。

### 在创建后延迟初始化依赖资源

```cpp
if (surfaceEvent->surfaceEventType()
    == QPlatformSurfaceEvent::SurfaceCreated) {
    recreateSurfaceResources();
    requestRender();
}
```

不同后端的实际资源创建时机可能还要结合 `QWindow::isExposed()`、当前尺寸和图形上下文状态判断。surface 创建不必然代表已经适合立刻呈现一帧。

## 5. 使用场景

`QPlatformSurfaceEvent` 适合 OpenGL 窗口、Vulkan 渲染器、QRhi 窗口、视频渲染、游戏编辑器、原生图形 API 集成和多窗口 GPU 资源管理。

窗口最小化、平台 surface 重建、屏幕变化、嵌入式窗口重挂等情况下，表面对象可能比 `QWindow` 更早或更频繁地变化，因此渲染器必须将其生命周期单独管理。

## 6. 常见坑与经验

不要在 `SurfaceAboutToBeDestroyed` 后继续调用 swap 或 present。原生句柄可能已经无效，结果通常是驱动错误、崩溃或黑屏。

不要只在窗口析构时销毁 swapchain。surface 可以在窗口对象仍然存在时被销毁和重建。

不要把 SurfaceCreated 等同于 exposed。创建完成后窗口仍可能不可见，渲染调度应继续看 `isExposed()`。

不要在 GUI 线程之外随意销毁与窗口 surface 绑定的图形资源。具体后端对线程和当前上下文有严格要求。

## 7. 知识点覆盖

学习 `QPlatformSurfaceEvent` 应覆盖原生 surface 生命周期、SurfaceCreated、SurfaceAboutToBeDestroyed、swapchain、图形上下文、OpenGL/Vulkan/QRhi、窗口最小化、surface 重建、渲染线程和资源释放顺序。
