# QNativeInterface::QWaylandApplication：访问 Qt 使用的 Wayland 客户端对象

> 适用版本：Qt 6.5 起；本文按 Qt 6.11.1 说明  
> 头文件：`#include <QGuiApplication>`  
> 模块：`Qt6::Gui`  
> 关联类型：`QGuiApplication`、`wl_display`、`wl_seat`、`wl_pointer`、`wl_keyboard`、`wl_touch`  
> 条件：Qt 构建启用了 Wayland 客户端平台插件

## 它解决什么问题

应用运行在 Wayland 平台插件上时，`QGuiApplication` 已经建立了与合成器的连接，并维护输入 seat、指针、键盘和触摸设备。大多数应用完全不需要接触它们：窗口、剪贴板、拖放和输入事件都应使用 Qt API。

少数 Wayland 协议扩展或原生库需要 Qt 正在使用的 `wl_display`、`wl_compositor` 或最近输入事件的 serial。`QNativeInterface::QWaylandApplication` 提供对这些对象的受控访问，而无需再建立第二条 Wayland 连接。

它不是应用应派生的类。Qt Wayland 平台插件提供实现，应用从 `QGuiApplication` 查询该接口。

常见的合理使用场景：

- 为 Qt 尚未覆盖的 Wayland 协议扩展绑定 registry/global；
- 原生协议请求明确要求来自用户输入的 serial；
- 在已有 Qt Wayland 连接上接入专业输入、显示或 shell 扩展。

## 取得接口

```cpp
#include <QGuiApplication>

void inspectWaylandConnection()
{
#if QT_CONFIG(wayland)
    auto *wayland =
        qGuiApp->nativeInterface<QNativeInterface::QWaylandApplication>();
    if (!wayland)
        return;

    wl_display *display = wayland->display();
    wl_compositor *compositor = wayland->compositor();
    // display 和 compositor 均由 Qt 的 Wayland 平台插件管理。
#endif
}
```

这段代码需要相应的 Wayland 客户端声明，例如 `<wayland-client.h>`。即使 Qt 编译时带有 Wayland，运行时也可能选择 XCB 或其它 QPA 平台插件，因此 `nativeInterface<T>()` 仍可能返回 `nullptr`。

所有返回的 `wl_*` 指针都是借用对象。不要对 Qt 管理的 `wl_display` 调用 `wl_display_disconnect()`，也不要销毁 Qt 创建的 `wl_compositor`、`wl_seat`、`wl_pointer`、`wl_keyboard` 或 `wl_touch`。原生协议对象和回调也应在 Qt 的 GUI/Wayland 事件循环语境中使用，避免自行对同一连接并发 dispatch。

## 输入对象与 serial

Wayland 将“用户刚刚执行的输入动作”用 serial 绑定到特权请求中，例如某些拖放、激活或弹出操作。此接口提供：

- `seat()`：默认输入设备关联的 `wl_seat`；
- `keyboard()`、`pointer()`、`touch()`：属于默认 seat 的对应设备；不可用时可为 `nullptr`；
- `lastInputSeat()`：最近一次输入事件所在的 seat；
- `lastInputSerial()`：任一 seat 最近一次输入事件的 serial。

serial 不是时间戳，也不是可缓存的全局权限令牌。它应只用于与触发操作对应的短时原生请求，并且应与正确的 seat 配对。跨越事件循环、窗口焦点变化或另一个输入事件后再复用旧 serial，合成器可能拒绝请求。对具有用户手势要求的功能，优先在处理 Qt 输入事件的当下提取和使用所需信息。

`xkbContext()` 只有 Qt 构建启用了 xkbcommon 时才会声明；它是 Qt 使用的 `xkb_context`，可用于与 xkbcommon 集成，但不要销毁或替换它。

## 各组 API 的含义

### Wayland 连接和全局对象

- `display()` 返回应用实际使用的 `wl_display`，即到合成器的客户端连接。
- `compositor()` 返回该连接的 `wl_compositor` global，可用于创建协议定义的 surface 对象。

它们不是 `QScreen` 或 `QWindow` 的替代品。Qt 窗口操作依然应通过 `QWindow` 进行；只有协议扩展需要原生对象时才使用它们。

### 输入设备对象

默认 seat 不必包含所有输入能力。无键盘、无指针或无触摸设备时，`keyboard()`、`pointer()`、`touch()` 可以为空。多 seat 环境中，`lastInputSeat()` 也不一定等于 `seat()`。

## 生命周期、线程与兼容性

- 先创建 `QGuiApplication`，并在 GUI 线程查询该接口。
- Wayland globals 可因合成器配置而变化；不要在应用结束、平台插件卸载或连接断开后使用缓存指针。
- Qt 驱动它所拥有的 Wayland 事件循环。直接在错误线程 dispatch、roundtrip 或破坏性断开连接，可能导致竞态、重入或卡死。
- Qt native interface API 可能随版本发生源码/二进制变化。将协议代码隔离在一个 Wayland 适配模块内。

## 常见错误

### 为协议扩展另开一个 wl_display 连接

第二条连接会有不同的对象、输入 serial 与权限上下文。若扩展需要与 Qt 窗口协作，通常应使用此接口返回的连接。

### 将 `lastInputSerial()` 当成永久有效的授权

它只表示最近输入事件的序列号。必须在合适的事件时机并与正确 seat 一起使用。

### 在没有设备时解引用 keyboard/pointer/touch

这些接口的“没有对应能力”是正常状态。每次使用前检查空指针。

## API 速查表

| 类别 | API | 语义 | 边界与注意点 |
| --- | --- | --- | --- |
| 获取接口 | `qGuiApp->nativeInterface<QNativeInterface::QWaylandApplication>()` | 从 Qt GUI 应用查询 Wayland 客户端接口。 | 仅 Wayland QPA；可能为 `nullptr`；接口由 Qt 管理。 |
| 连接 | `wl_display *display() const` | 返回应用使用的 Wayland 连接。 | 借用指针；不得 disconnect；避免手动并发 dispatch。 |
| 全局对象 | `wl_compositor *compositor() const` | 返回应用使用的 compositor global。 | 借用对象；仅用于确有必要的原生协议调用。 |
| 默认输入 | `wl_seat *seat() const` | 返回默认输入设备关联的 seat。 | 多 seat 环境不等于最近输入 seat；可能不可用于特定设备能力。 |
| 默认键盘 | `wl_keyboard *keyboard() const` | 返回默认 seat 的键盘对象。 | 无键盘能力时为 `nullptr`；不得销毁。 |
| 默认指针 | `wl_pointer *pointer() const` | 返回默认 seat 的指针对象。 | 无指针能力时为 `nullptr`；不得销毁。 |
| 默认触摸 | `wl_touch *touch() const` | 返回默认 seat 的触摸对象。 | 无触摸能力时为 `nullptr`；不得销毁。 |
| 最近输入 | `uint lastInputSerial() const` | 返回任一 seat 最近输入事件的 serial。 | 不是时间戳或长期 token；只在对应用户手势的短时请求中使用。 |
| 最近输入 | `wl_seat *lastInputSeat() const` | 返回最近输入事件所属的 seat。 | 应与所用 serial 的事件语义一并考虑；可能不同于 `seat()`。 |
| 键盘映射 | `xkb_context *xkbContext() const` | 返回 Qt 使用的 xkbcommon context。 | 仅 Qt 启用 xkbcommon 时可用；借用指针，不得销毁。 |

## 一句话总结

`QWaylandApplication` 让原生协议扩展复用 Qt 的 Wayland 连接和输入上下文；借用而不接管这些对象，并把 serial 的使用紧贴实际输入事件。
