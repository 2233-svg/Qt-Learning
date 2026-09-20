# QSystemTrayIcon

> Qt 6.11.1 · Qt Widgets · 来自 `QSystemTrayIcon`

## 1. 先建立直觉

`QSystemTrayIcon` 在系统托盘/通知区域放一个应用图标，提供后台状态、快速菜单和桌面通知。它常用于常驻工具、同步客户端、即时通讯、下载器、监控程序。

它不是 QWidget，不会出现在你的布局里。它是 QObject，靠系统托盘服务显示；不同桌面环境对点击、通知、菜单和图标尺寸的支持差异很大。

## 2. 类说明

- 头文件：`#include <QSystemTrayIcon>`
- 模块：`Qt6::Widgets`
- 继承自：`QObject`
- 直接派生类：类页未列出

```cmake
find_package(Qt6 REQUIRED COMPONENTS Widgets)
target_link_libraries(mytarget PRIVATE Qt6::Widgets)
```

使用前通常检查 `isSystemTrayAvailable()`，并准备一个右键菜单。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `QSystemTrayIcon(parent)` / `QSystemTrayIcon(icon, parent)` | 创建托盘图标对象，初始不可见。 |
| `setIcon()` / `icon()` | 设置或读取托盘图标。 |
| `setToolTip()` / `toolTip()` | 设置或读取悬停提示。 |
| `show()` / `hide()` / `setVisible()` | 显示或隐藏托盘图标。 |
| `isVisible()` | 查询当前是否可见。 |
| `setContextMenu()` / `contextMenu()` | 设置右键菜单；托盘图标不拥有菜单。 |
| `geometry()` | 返回托盘图标屏幕几何，平台可能不可靠。 |
| `showMessage(title, message, icon, timeout)` | 显示系统通知/气泡消息。 |
| `showMessage(title, message, QIcon, timeout)` | 使用自定义图标显示通知。 |
| `activated(reason)` | 用户点击、双击、中键、请求菜单等激活信号。 |
| `messageClicked()` | 用户点击通知消息。 |
| `isSystemTrayAvailable()` | 静态查询当前系统托盘是否可用。 |
| `supportsMessages()` | 静态查询是否支持托盘消息。 |

## 4. 关键用法

### 先准备菜单和退出路径

常驻托盘应用应至少提供“显示主窗口”和“退出”。如果主窗口关闭只是隐藏到托盘，必须让用户知道应用仍在运行，并能从托盘真正退出。

`setContextMenu()` 不转移菜单所有权。通常把菜单设为主窗口或应用对象的子对象，保证托盘存在期间菜单也存在。

### 平台行为不要假设一致

Windows、macOS、不同 Linux 桌面环境对单击、双击、右键、通知点击支持不完全一致。`activated()` 的 `ActivationReason` 要写得宽容，例如把 `Trigger` 和 `DoubleClick` 都当成“显示/隐藏主窗口”的入口。

### 通知不是可靠任务队列

`showMessage()` 是提醒用户，不保证每个平台都显示，也不保证显示时长完全遵守 timeout。重要错误和必须确认的操作不要只靠托盘通知。

### 图标要适配小尺寸

托盘图标通常很小。准备清晰的 16x16、22x22 或高 DPI 图标资源，不要直接缩放复杂大图。深浅主题下也要可见。

## 5. 常见坑与经验

- `show()` 前设置 icon，否则可能没有可见效果。
- 托盘不可用时，如果稍后可用，已 visible 的图标可能自动加入；仍要设计无托盘降级路径。
- macOS 上设置上下文菜单会影响双击信号表现。
- `geometry()` 在某些系统上可能返回空或不精确。
- 不要用托盘图标隐藏关键状态，主窗口内也应有状态入口。
