# QNativeInterface::QAndroidScreen：取得 Android 显示器标识

> 适用版本：Qt 6.7 起；本文按 Qt 6.11.1 说明  
> 头文件：`#include <QAndroidScreen>`  
> 模块：`Qt6::Gui`  
> 关联类型：`QScreen`、`QGuiApplication`  
> 平台：仅 Android

## 它解决什么问题

Qt 的 `QScreen` 用统一接口描述屏幕：几何尺寸、DPI、方向、刷新率等。Android 某些系统 API 或厂商 SDK 却要求一个平台显示器编号，而不是 `QScreen *`。`QNativeInterface::QAndroidScreen` 正是这层桥接：从某个 Qt 屏幕取得其 Android `displayId()`。

这不是供应用继承实现的抽象基类。Qt 的 Android 平台插件在内部提供实现；应用代码只在确实需要调用 Android 原生显示 API 时，通过 `QScreen::nativeInterface<T>()` 查询它。

典型场景包括：

- 将 `QWindow` 所在的 `QScreen` 对应到 Android 的指定显示器；
- 调用需要 display ID 的 Android NDK/JNI 或第三方 SDK；
- 多显示器、外接显示器或演示屏方案中，将 Qt 的屏幕选择同步给原生层。

若只是列出屏幕、判断窗口在哪块屏幕、读取逻辑 DPI 或屏幕尺寸，应继续使用 `QScreen`。为了获取普通屏幕信息而进入 native interface，会给代码带来不必要的平台耦合。

## 如何取得接口

接口由 `QScreen` 提供，不自行构造：

```cpp
#include <QGuiApplication>
#include <QScreen>

#if defined(Q_OS_ANDROID)
#  include <QAndroidScreen>
#endif

int androidDisplayIdForPrimaryScreen()
{
#if defined(Q_OS_ANDROID)
    QScreen *screen = QGuiApplication::primaryScreen();
    if (!screen)
        return -1;

    auto *androidScreen =
        screen->nativeInterface<QNativeInterface::QAndroidScreen>();
    return androidScreen ? androidScreen->displayId() : -1;
#else
    return -1;
#endif
}
```

`nativeInterface<T>()` 的返回值可能是空指针。原因可以是当前并非 Android、所选 Qt 版本或平台插件未提供该接口，或者对象已不处于可查询状态。不能把“在 Android 编译成功”误当成“查询必然成功”。

不要把上例中的 `-1` 当作 Qt 规定的“无效 display ID”。它只是调用方自行选择的失败结果；原生 API 对无效 ID 的约定应由调用方单独处理。

## 使用边界

### 只在 Android 构建和调用

`QAndroidScreen` 仅在 Android 条件下声明。头文件包含、类型名和调用点都应处于 `#if defined(Q_OS_ANDROID)` 内，或封装在独立的 Android 平台适配文件中。这样桌面构建不会因为未知类型失败，也不会把平台分支散落在业务代码里。

### 接口指针不拥有屏幕

`nativeInterface<T>()` 返回的是 Qt 管理的借用接口。不要 `delete` 它，也不要在 `QScreen` 已失效后缓存和使用它。屏幕配置改变时，`QGuiApplication::screens()` 中的对象集合也可能变化；需要长期使用时，应在每次实际调用前重新从当前 `QScreen` 查询。

### 仍遵守 GUI 对象的线程规则

`QScreen` 属于 GUI 运行时对象。应在创建 `QGuiApplication` 后、拥有该 GUI 对象的线程中查询接口；不要让工作线程直接访问或持有 `QScreen`。工作线程需要 display ID 时，可由 GUI 线程提取一个 `int` 后以普通数据传递。

### 原生接口不是长期稳定 ABI 承诺

Qt 原生接口头文件明确提示：使用它可能造成未来 Qt 版本之间的源码或二进制兼容性问题。把访问集中在很小的 Android 适配层，向其余工程暴露自己的稳定函数，例如 `currentDisplayId()`，可把后续升级的修改范围控制在一处。

## 关键 API 语义

### `displayId()`

`displayId()` 返回此 `QScreen` 映射到的 Android display ID。它回答的是“这个 Qt 屏幕在 Android 原生显示体系中的编号是什么”，不返回：

- Qt 屏幕在 `QGuiApplication::screens()` 列表中的下标；
- `QWindow::winId()`；
- 分辨率、DPI 或物理显示器名称；
- 一个可跨设备、跨启动持久保存的业务主键。

因此，不能以 `screens().indexOf(screen)` 替代 `displayId()`，也不应假设 ID 与屏幕枚举顺序相同。若系统重配显示器，重新根据当前 `QScreen` 取得 ID。

## 常见错误

### 直接包含头文件后在桌面平台引用类型

问题通常表现为非 Android 构建报类型不存在。用 `Q_OS_ANDROID` 包住包含和实现，或将 Android 代码放入平台专用源文件。

### 没有判空就调用 `displayId()`

`nativeInterface<T>()` 不是强制成功的转换。先判断返回指针，再进入原生 API。

### 将 `displayId()` 当作 Qt 屏幕索引

Android 的显示 ID 由系统定义，Qt 屏幕列表的排序由 Qt 运行时决定，两者没有可依赖的数值关系。

### 用它替代 `QScreen`

显示器的日常状态和变化通知应由 `QScreen` 负责。只有 Android 原生调用的参数确实要求 display ID 时，才查询此接口。

## API 速查表

| 类别 | API | 语义 | 边界与注意点 |
| --- | --- | --- | --- |
| 获取接口 | `screen->nativeInterface<QNativeInterface::QAndroidScreen>()` | 从指定 `QScreen` 查询 Android 原生屏幕接口。 | 仅 Android；可能返回 `nullptr`；返回值由 Qt 管理。 |
| 成员函数 | `int displayId() const` | 返回该 `QScreen` 的 Android display ID。 | 不是 Qt 屏幕列表下标，也不是窗口 ID；仅传给需要 Android display ID 的原生 API。 |

## 一句话总结

`QNativeInterface::QAndroidScreen` 只解决“把 `QScreen` 映射为 Android display ID”这一件事；优先使用 `QScreen`，并把这条原生通道隔离在带平台判断的适配层中。
