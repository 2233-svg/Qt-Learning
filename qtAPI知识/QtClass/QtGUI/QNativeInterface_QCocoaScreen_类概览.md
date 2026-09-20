# QNativeInterface::QCocoaScreen：取得 QScreen 对应的 NSScreen

> 适用版本：Qt 6.11 起  
> 头文件：`#include <QCocoaScreen>`  
> 模块：`Qt6::Gui`  
> 关联类型：`QScreen`、`NSScreen`  
> 平台：仅 macOS

## 它解决什么问题

`QScreen` 负责 Qt 视角的屏幕信息：可用区域、物理尺寸、方向、DPI 和屏幕变化通知。macOS 的 AppKit API 则以 `NSScreen *` 为参数或返回值。`QNativeInterface::QCocoaScreen` 让应用从一个 `QScreen` 找到同一块物理或逻辑显示器对应的 Cocoa `NSScreen`。

实际用途通常是：

- 调用只能接受 `NSScreen *` 的 AppKit 或 macOS SDK；
- 将 Qt 选中的屏幕与原生窗口、菜单栏、演示或显示器配置逻辑关联；
- 在 Objective-C++ 适配层中读取 Qt 未抽象的 macOS 特定屏幕属性。

若需求只是显示窗口、读取分辨率或响应屏幕热插拔，应使用 `QScreen` 本身。引入 `NSScreen` 会锁定 macOS，且其坐标和单位语义不应默认等同于 Qt 的几何数据。

## 使用方式

从当前有效的 `QScreen` 查询接口，而不是构造 `QCocoaScreen`：

```cpp
#include <QScreen>

#if defined(Q_OS_MACOS)
NSScreen *nativeScreenFor(QScreen *screen)
{
    if (!screen)
        return nullptr;

    auto *cocoa =
        screen->nativeInterface<QNativeInterface::QCocoaScreen>();
    return cocoa ? cocoa->nativeScreen() : nullptr;
}
#endif
```

`nativeInterface<T>()` 可能返回 `nullptr`，即使代码处于 macOS 分支中也不能省略检查。AppKit 方法调用应放在 `.mm` 文件中；业务层最好只接收自己的平台无关数据，而不传播 `NSScreen *`。

## `nativeScreen()` 的语义与边界

`nativeScreen()` 返回此 `QScreen` 背后的 `NSScreen *`。它回答的是“这一个 Qt 屏幕所对应的 Cocoa 屏幕对象”，而不是：

- `QGuiApplication::screens()` 中的数组下标；
- `QWindow::winId()` 或原生窗口句柄；
- 可永久保存的显示器业务 ID；
- 可替代 `QScreen::geometry()` 的跨平台坐标数据。

返回的 `NSScreen *` 由系统和 Qt 平台集成管理，调用方只借用它。不要释放它，也不要在 `QScreen` 被移除后继续使用。显示器热插拔、睡眠恢复或配置变化后，应从当前 `QScreen` 重新取得指针。

Qt 与 AppKit 的屏幕坐标原点、缩放和可用区域定义可能不同。需要在两套坐标之间换算时，使用 AppKit 推荐的转换 API 并明确是点、像素还是 Qt 逻辑坐标；不要依据“主屏高度减 Y”之类的固定公式猜测。

## 生命周期与线程

`QScreen` 是 GUI 运行时对象，应在拥有 GUI 对象的线程中访问。把 `NSScreen *` 带到工作线程并不能绕开 AppKit 的线程约束；工作线程只应收到已经提取出的普通值。

本接口属于 Qt native interface API，未来 Qt 升级可能改变源码或二进制兼容性。建议将它封装为 macOS 专用函数，不要让 `NSScreen *` 进入跨平台模块的公开接口。

## 常见错误

### 在普通屏幕逻辑中依赖 `NSScreen`

屏幕列表、窗口迁移和 DPI 处理都已有 `QScreen` API。只有原生 API 明确要求 `NSScreen *` 时才查询它。

### 缓存返回指针以跨越显示器变化

屏幕对象集合可以变化。通过 `QGuiApplication::screenAdded`、`screenRemoved` 和 `QWindow::screenChanged` 跟踪 Qt 层变化，并在需要时重新查询。

### 误把 Qt 与 AppKit 坐标直接混用

两边都可能使用“点”，但坐标系与可用区域规则仍可能不同。转换前写清楚源坐标系和目标坐标系。

## API 速查表

| 类别 | API | 语义 | 边界与注意点 |
| --- | --- | --- | --- |
| 获取接口 | `screen->nativeInterface<QNativeInterface::QCocoaScreen>()` | 从 `QScreen` 查询 macOS 原生屏幕接口。 | 仅 macOS；可能为 `nullptr`；接口由 Qt 管理。 |
| 成员函数 | `NSScreen *nativeScreen() const` | 返回该 Qt 屏幕对应的 Cocoa `NSScreen`。 | 借用指针；不得释放或长期缓存；不要将坐标、缩放语义直接等同于 Qt。 |

## 一句话总结

`QCocoaScreen` 只在必须调用 AppKit 时把 `QScreen` 映射为 `NSScreen`；正常屏幕功能继续用 `QScreen`，并把 Cocoa 指针限制在 macOS 适配层。
