# QNativeInterface::QX11Application：复用 Qt 的 X11/XCB 连接

> 适用版本：Qt 6.2 起；本文按 Qt 6.11.1 说明  
> 头文件：`#include <QGuiApplication>`  
> 模块：`Qt6::Gui`  
> 关联类型：`QGuiApplication`、`Display`、`xcb_connection_t`  
> 条件：Qt 构建启用了 XCB 平台插件

## 它解决什么问题

Qt 在 X11/XCB 平台插件中已经建立并维护应用的 X 服务器连接。某些 Xlib、XCB 扩展或遗留窗口管理协议需要原生 `Display *` 或 `xcb_connection_t *`，重新开一条连接会得到不同的资源、事件队列和窗口上下文。

`QNativeInterface::QX11Application` 让这类集成复用 Qt 正在使用的连接：

- `display()` 面向 Xlib API；
- `connection()` 面向 XCB API。

这是原生互操作入口，不是应用应派生的类型。创建窗口、读取剪贴板、处理输入和大多数 EWMH/窗口状态需求，应先查 Qt 是否已有跨平台 API。

## 取得接口

```cpp
#include <QGuiApplication>

void inspectX11Connection()
{
#if QT_CONFIG(xcb)
    auto *x11 =
        qGuiApp->nativeInterface<QNativeInterface::QX11Application>();
    if (!x11)
        return;

    Display *display = x11->display();
    xcb_connection_t *connection = x11->connection();
    // 两者均代表 Qt 正在使用的 X 连接，且生命周期由 Qt 管理。
#endif
}
```

调用点还需包含所用库的声明，例如 Xlib 的 `<X11/Xlib.h>` 或 XCB 的 `<xcb/xcb.h>`。即使 Qt 构建时带 XCB，运行时也可能选择 Wayland 或其它 QPA 后端，因此查询接口后仍要判空。

## 何时选择 Xlib，何时选择 XCB

### `display()`

`display()` 返回应用的 `Display *`，用于只提供 Xlib API 的库，例如部分传统扩展、窗口属性工具或 IME 集成。它不是 Qt `QDisplay`，也不是屏幕对象。

### `connection()`

`connection()` 返回同一应用的 `xcb_connection_t *`，用于 XCB API。XCB 的请求、cookie 和事件模型与 Xlib 不同；选择一个库风格并保持局部一致，通常比在同一功能中交织 Xlib 与 XCB 更容易维护。

两条访问路径都借用 Qt 持有的连接。不要调用 `XCloseDisplay()` 或 `xcb_disconnect()`，也不要将其当作自己创建的连接来改变全局事件队列归属。Qt 需要继续处理窗口、输入和平台事件。

## 事件循环与线程边界

Qt 管理该 X11 连接的事件处理。对 Qt 连接手动抢占事件、阻塞式等待或从其它线程无序发送和 flush 请求，可能造成事件丢失、重入或死锁。原生交互应尽量是短小的查询/请求，并在 GUI 线程或受控的同步点执行。

如果第三方库要求完全控制 `Display *` 的事件循环，通常不适合直接把 Qt 的连接交给它；应改用该库的嵌入模式、单独连接，或把功能隔离到不需要与 Qt 窗口共享资源的场景。

这些指针只在 `QGuiApplication` 存活且 XCB 平台插件保持运行期间有效。程序退出、平台切换或错误断开后都不应继续使用。Qt native interface API 也不承诺永久 ABI 稳定，建议集中封装。

## 常见错误

### 关闭 Qt 的 X 连接

`Display *` 和 `xcb_connection_t *` 都不是调用方所有。关闭任一连接会使 Qt 的后续平台操作失效。

### 只根据 DISPLAY 环境变量就假设可用

环境变量存在不表示 Qt 当前运行在 XCB 后端。以 `nativeInterface<T>()` 的实际返回值为准。

### 手动接管 Qt 的事件队列

Qt 必须读取和分派它自己的 X 事件。第三方代码若要大量消费事件，需采用不会与 Qt 争夺该连接的设计。

## API 速查表

| 类别 | API | 语义 | 边界与注意点 |
| --- | --- | --- | --- |
| 获取接口 | `qGuiApp->nativeInterface<QNativeInterface::QX11Application>()` | 从 GUI 应用查询 X11/XCB 原生接口。 | 需要 XCB QPA；可能为 `nullptr`；接口由 Qt 管理。 |
| 成员函数 | `Display *display() const` | 返回应用的 Xlib `Display`。 | 借用指针；供 Xlib API 使用；不得 `XCloseDisplay()` 或接管 Qt 事件循环。 |
| 成员函数 | `xcb_connection_t *connection() const` | 返回应用的 XCB 连接。 | 借用指针；供 XCB API 使用；不得 `xcb_disconnect()` 或破坏 Qt 的事件处理。 |

## 一句话总结

`QX11Application` 为不可避免的 Xlib/XCB 集成提供 Qt 当前连接的借用访问；可以发起必要的原生请求，但连接、事件循环和最终关闭始终归 Qt 管理。
