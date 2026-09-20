# QPlatformSurfaceEvent：在原生 surface 创建或销毁前后同步收到通知

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QPlatformSurfaceEvent>`  
> 所属模块：`Qt6::Gui`  
> 继承：`QEvent`

`QPlatformSurfaceEvent` 用来通知窗口或离屏 surface 的底层原生平台 surface 发生了关键生命周期变化。它只有两种状态：原生 surface 已创建，以及原生 surface 即将被销毁。

这类事件解决的是一个很具体但很重要的问题：Qt 对象可能已经存在，但对应的 HWND、X11 Window、Cocoa surface、EGL surface 或其他平台资源并不一定在整个对象生命周期内都存在。OpenGL、Vulkan、Direct3D 或自定义平台接口若需要依赖这些资源，就必须知道何时可以创建关联资源、何时必须停止使用并释放关联资源。

## 事件什么时候到达

平台窗口事件会**同步**发送给窗口和离屏 surface：

- `SurfaceCreated`：底层原生 surface 已经创建，可以开始依赖它的初始化。
- `SurfaceAboutToBeDestroyed`：底层原生 surface 将在此事件之后立即销毁，应在处理事件期间停止使用它。

常规应用不直接构造这个事件，而是在 `QWindow::event()`、`QObject::eventFilter()` 或自定义窗口类中识别它：

```cpp
bool RenderWindow::event(QEvent *event)
{
    if (event->type() == QEvent::PlatformSurface) {
        auto *surfaceEvent =
            static_cast<QPlatformSurfaceEvent *>(event);

        if (surfaceEvent->surfaceEventType()
            == QPlatformSurfaceEvent::SurfaceAboutToBeDestroyed) {
            releaseNativeRenderingResources();
        } else {
            createNativeRenderingResources();
        }
    }

    return QWindow::event(event);
}
```

如果只处理销毁事件，仍应把其他事件交给基类。事件接收对象通常是 `QWindow` 或 `QOffscreenSurface` 对应的 QObject；不要把它当成普通绘图事件转发给任意业务对象。

## 它和 `QWindow`、`QOffscreenSurface` 的关系

`QWindow` 的 Qt 对象生命周期和原生窗口 surface 生命周期不是一回事。窗口可以在隐藏、重建、屏幕切换、窗口系统状态变化或销毁过程中经历原生 surface 的创建和再次销毁。

`QOffscreenSurface` 也可能有平台相关的原生资源生命周期。它常用于让 OpenGL context 在没有可见窗口时拥有可绑定的 surface。只有收到 `SurfaceCreated` 后，才应假定对应平台 surface 已存在；收到 `SurfaceAboutToBeDestroyed` 后，不要继续调用依赖该 surface 的平台接口。

不要把 `QWindow::winId()`、`QNativeInterface` 返回的原生句柄或图形 API 的 surface 对象永久缓存为“永远有效”。平台资源重建后，旧句柄和旧关联对象可能已经失效，需要按新创建事件重新获取。

## OpenGL/Vulkan 资源管理的典型模式

在渲染窗口中，`SurfaceAboutToBeDestroyed` 适合做以下工作：

- 停止提交新的帧。
- 解除或销毁依赖窗口 surface 的 swapchain、framebuffer、EGL surface 或 framebuffer 绑定。
- 让图形上下文与 surface 的关联失效。
- 清理仍持有旧原生句柄的缓存。

它不表示整个 `QWindow` 对象已析构，也不表示所有 Qt 图形资源都必须销毁。只释放与该原生 surface 强绑定的资源；可以跨 surface 重用的设备级资源按各自生命周期管理。

处理事件时还要遵守图形 API 的线程规则。事件通常在窗口所属线程同步交付，但某些图形资源的销毁可能要求特定 context 或渲染线程。必要时，将“收到销毁通知”和“实际 GPU 资源释放”通过项目自己的渲染同步协议连接起来，不能只凭事件类型绕过图形 API 的线程要求。

## 自定义事件与生命周期

构造器是公开的，因此测试代码或框架代码可以构造一个指定类型的事件：

```cpp
QPlatformSurfaceEvent event(
    QPlatformSurfaceEvent::SurfaceCreated);
QCoreApplication::sendEvent(window, &event);
```

但手动发送并不会真正创建或销毁操作系统 surface，也不会让 `QWindow` 的平台句柄变得有效。它只能测试接收方对事件的响应逻辑。生产代码应让 Qt 的窗口系统触发真实事件。

事件对象只在同步处理期间有效。不要保存 `QPlatformSurfaceEvent *`，也不要把 `surfaceEventType()` 之外的假设延伸成某个具体平台的资源状态。

## 平台差异

事件的语义是跨平台的，但触发次数、原生资源重建原因、具体句柄类型和底层图形 API 行为由平台插件与窗口系统决定。代码应对“创建/即将销毁”做幂等处理：

- 创建时如果资源已存在，先确认是否属于当前 surface，再决定复用或重建。
- 销毁时即使部分资源已经被提前释放，也不要重复销毁底层对象。
- 不要依赖某一个平台一定只发送一次 `SurfaceCreated`。

如果程序只使用 `QPainter` 绘制 QWidget 或普通窗口，通常不需要直接处理此事件。它主要服务于原生窗口句柄、OpenGL/Vulkan/Direct3D、平台输入法 surface 或其他低层互操作。

## 常见错误

- 收到 `SurfaceAboutToBeDestroyed` 后才开始释放，而释放动作需要已经失效的原生句柄：应在事件处理期间完成解除和准备。
- 把 `SurfaceAboutToBeDestroyed` 当成 `QWindow` 即将析构：窗口对象可能继续存在并稍后创建新 surface。
- 缓存一次 `winId()` 或平台 surface 句柄并跨越重建继续使用。
- 在任意线程手动删除图形资源，忽略 OpenGL context、Vulkan queue 或渲染线程约束。
- 手动构造事件后以为系统 surface 已创建/销毁：测试事件不会改变平台状态。
- 处理事件后不调用基类事件处理，导致窗口自身的生命周期逻辑被跳过。

## API 速查表

| API | 语义与使用边界 |
| --- | --- |
| `QPlatformSurfaceEvent(SurfaceEventType)` | 构造指定类型的平台 surface 事件；手工构造只适合测试或框架代码，不会改变真实平台资源。 |
| `surfaceEventType()` | 返回 `SurfaceCreated` 或 `SurfaceAboutToBeDestroyed`。 |
| `SurfaceEventType` | 描述底层原生 surface 的生命周期阶段。 |
| `SurfaceCreated` | 原生 surface 已创建；此时可以初始化依赖它的资源。 |
| `SurfaceAboutToBeDestroyed` | 原生 surface 将在事件后立即销毁；应停止使用并释放强绑定资源。 |
| `QEvent::PlatformSurface` | 通过 `event->type()` 识别此类事件。 |
| `QWindow::event()` / `QObject::eventFilter()` | 常见接收入口；处理完自定义逻辑后按需交给基类或原过滤链。 |
