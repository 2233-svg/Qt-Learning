# QNativeInterface::QWaylandScreen：取得 QScreen 对应的 wl_output

> 适用版本：Qt 6.7 起  
> 头文件：`#include <QWaylandScreen>`  
> 模块：`Qt6::Gui`  
> 关联类型：`QScreen`、`wl_output`  
> 条件：Qt 构建启用了 Wayland 客户端平台插件

## 它解决什么问题

`QScreen` 用跨平台方式表示一块屏幕，提供几何、DPI、方向和屏幕变化通知。Wayland 的输出设备由 `wl_output` 表示，某些协议扩展需要它来识别目标输出。`QNativeInterface::QWaylandScreen` 将两者关联起来：从一个 Qt `QScreen` 取得底层 `wl_output *`。

典型使用场景：

- 原生 Wayland 协议扩展需要绑定或指定某个输出；
- 将 Qt 当前选择的屏幕映射给仅接受 `wl_output` 的库；
- 在平台适配层读取 Qt 未公开封装的输出协议信息。

窗口选屏、可用区域、DPI 和屏幕热插拔应继续使用 `QScreen`。不要为了得到常规显示器信息而直接操作 Wayland 输出协议。

## 使用方式

```cpp
#include <QScreen>

wl_output *outputFor(QScreen *screen)
{
#if QT_CONFIG(wayland)
    if (!screen)
        return nullptr;

    auto *wayland =
        screen->nativeInterface<QNativeInterface::QWaylandScreen>();
    return wayland ? wayland->output() : nullptr;
#else
    return nullptr;
#endif
}
```

`nativeInterface<T>()` 可能返回 `nullptr`：程序也许未运行在 Wayland QPA 平台插件上，或当前对象没有可用的原生接口。`wl_output` 声明来自 Wayland 客户端头文件；若只是把指针传给适配层，可保持这一依赖不向业务层扩散。

## `output()` 的语义

`output()` 返回**此 `QScreen`** 对应的 `wl_output *`。它不是：

- `QGuiApplication::screens()` 中的下标；
- 一个稳定的物理显示器序列号；
- `QWindow` 的 surface；
- 用来替代 `QScreen` 几何和 DPI API 的通用句柄。

该指针由 Qt 的 Wayland 平台插件管理，只能借用。不要调用 `wl_output_destroy()`，也不要在 `QScreen` 已被移除、Wayland 连接结束或应用退出后继续使用它。输出热插拔或合成器配置变化后，应从仍有效的 `QScreen` 重新查询。

## 线程与 Wayland 事件循环

`QScreen` 是 GUI 对象，应在 GUI 线程访问。Qt 同时驱动自己的 Wayland 客户端事件循环；不要从工作线程直接向 Qt 拥有的 `wl_output` 注册会改变生命周期的逻辑，或自行在同一连接上进行竞争性 dispatch。需要后台计算时，先由 GUI 线程提取普通数据，再传给工作线程。

`wl_output` 的模式、缩放和几何协议事件会由 Qt 转换为 `QScreen` 状态。正常界面逻辑应监听 Qt 的 `QScreen` 信号；只有专有协议没有 Qt 对应抽象时才在这一层补充处理。

## 常见错误

### 把 `wl_output` 当作永久屏幕 ID

它是 Wayland 连接中的协议对象，不能作为跨会话或热插拔后的持久标识。业务持久化应使用更高层、明确稳定的标识策略。

### 绕过 QScreen 读取普通显示器信息

使用 `QScreen::geometry()`、`availableGeometry()`、`logicalDotsPerInch()` 等 API 更可移植，也不会与 Qt 的 Wayland 状态同步发生冲突。

### 手动销毁 `output()`

返回值并不转移所有权。销毁会破坏 Qt 平台插件仍在使用的 Wayland proxy。

## API 速查表

| 类别 | API | 语义 | 边界与注意点 |
| --- | --- | --- | --- |
| 获取接口 | `screen->nativeInterface<QNativeInterface::QWaylandScreen>()` | 从 Qt 屏幕查询 Wayland 原生屏幕接口。 | 需要 Wayland QPA；可能为 `nullptr`；接口由 Qt 管理。 |
| 成员函数 | `wl_output *output() const` | 返回该 `QScreen` 背后的 Wayland 输出对象。 | 借用指针；不得 destroy 或长期缓存；不等同于屏幕列表下标和持久 ID。 |

## 一句话总结

`QWaylandScreen` 仅在原生协议确实需要 `wl_output` 时，将一个 `QScreen` 映射到它；常规屏幕逻辑应仍留在 Qt 的 `QScreen` API 中。
