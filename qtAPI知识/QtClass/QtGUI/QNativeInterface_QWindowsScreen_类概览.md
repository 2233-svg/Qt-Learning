# QNativeInterface::QWindowsScreen：取得 QScreen 对应的 HMONITOR

> 适用版本：Qt 6.7 起  
> 头文件：`#include <QWindowsScreen>`  
> 模块：`Qt6::Gui`  
> 关联类型：`QScreen`、`HMONITOR`  
> 平台：仅 Windows

## 它解决什么问题

Qt 的 `QScreen` 是跨平台的显示器对象，负责屏幕几何、DPI、可用区域和热插拔信号。Windows 的许多显示器 API，例如 `GetMonitorInfo()`，则以 `HMONITOR` 为参数。`QNativeInterface::QWindowsScreen` 负责将一个 `QScreen` 映射为对应的 Windows 监视器句柄。

典型场景：

- 调用只接受 `HMONITOR` 的 Win32 显示器 API；
- 将 Qt 中选定的屏幕传给 Windows 专有的色彩、HDR、显示模式或窗口定位功能；
- 在 Windows 平台适配层获取 Qt 没有直接封装的显示器信息。

普通多屏逻辑仍应使用 `QScreen`。它更可移植，也会自然跟随 Qt 的高 DPI 和屏幕变更模型。

## 使用方式

```cpp
#include <QScreen>

#if defined(Q_OS_WIN)
HMONITOR monitorFor(QScreen *screen)
{
    if (!screen)
        return nullptr;

    auto *windows =
        screen->nativeInterface<QNativeInterface::QWindowsScreen>();
    return windows ? windows->handle() : nullptr;
}
#endif
```

`nativeInterface<T>()` 可能为空，调用前要检查。返回的 `HMONITOR` 可以传给 `GetMonitorInfo()` 等只读或查询性质的 Win32 API，但不代表所有权转移。

## `handle()` 的语义

`handle()` 返回当前 `QScreen` 背后的 `HMONITOR`。它不是：

- `QGuiApplication::screens()` 中的索引；
- 窗口的 `HWND`；
- 可以跨热插拔、驱动重置或应用重启永久保存的显示器 ID；
- 取代 `QScreen::geometry()` 的跨平台坐标对象。

Windows 句柄由系统管理，Qt 的 `QScreen` 又会随显示配置变化而增删。不要缓存 `HMONITOR` 跨越 `screenRemoved`、显示器重连或应用销毁；每次需要与当前 Qt 屏幕对应的原生监视器时重新查询。

Windows 的物理像素、DPI awareness 上下文和 Qt 逻辑坐标不总是一一对应。使用原生 API 返回的矩形去定位 Qt 窗口前，先明确其坐标单位与当前进程的 DPI awareness；日常布局优先用 Qt 的 `QScreen` 几何 API。

## 生命周期与线程

`QScreen` 属于 GUI 层对象，应在 GUI 线程读取。可以将已获取的数值性结果交给后台任务，但不要让后台线程保留或依赖 Qt `QScreen` 的生命周期。

此类属于 Qt native interface，未来 Qt 升级可能产生源码或二进制兼容变化。把 `HMONITOR` 的操作限制在 Windows 平台模块，以免向跨平台代码泄漏 Win32 类型。

## 常见错误

### 将 HMONITOR 当作 HWND

二者分别代表显示器和窗口。窗口 API 常需要 `HWND`，显示器 API 常需要 `HMONITOR`，不能互换。

### 用屏幕列表下标代替 `handle()`

Qt 屏幕枚举顺序不是 Windows 监视器句柄，也不保证与系统显示器编号稳定对应。

### 在屏幕变化后继续使用旧句柄

订阅 Qt 的屏幕变化信号，并在新的 `QScreen` 上重新查询原生句柄。

## API 速查表

| 类别 | API | 语义 | 边界与注意点 |
| --- | --- | --- | --- |
| 获取接口 | `screen->nativeInterface<QNativeInterface::QWindowsScreen>()` | 从 Qt 屏幕查询 Windows 原生屏幕接口。 | 仅 Windows；可能为 `nullptr`；接口由 Qt 管理。 |
| 成员函数 | `HMONITOR handle() const` | 返回该 `QScreen` 对应的监视器句柄。 | 借用系统句柄；不是 `HWND` 或屏幕列表下标；不应跨显示器配置变化缓存。 |

## 一句话总结

`QWindowsScreen` 让 Windows 专有 API 精确定位到 Qt 的某个 `QScreen`；日常屏幕逻辑仍用 Qt，`HMONITOR` 只在平台适配层短暂使用。
