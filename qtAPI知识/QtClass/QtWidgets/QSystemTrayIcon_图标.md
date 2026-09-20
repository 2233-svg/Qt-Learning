# Qt QSystemTrayIcon 深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QSystemTrayIcon>`  
> 所属模块：`Qt6::Widgets`  
> 继承：`QObject -> QSystemTrayIcon`  
> 定位：系统托盘入口

## 1. QSystemTrayIcon 解决什么问题

`QSystemTrayIcon` 用来把应用放进操作系统的系统托盘、通知区域或菜单栏。它让应用在主窗口隐藏后仍然可以通过托盘图标提供入口、上下文菜单和通知。

它常见于：

- 常驻后台的同步工具；
- 下载、备份、监控程序；
- 需要“关闭窗口但不退出进程”的桌面应用；
- 通过托盘菜单快速恢复主窗口的工具。

```text
QApplication
   │
   └─ QSystemTrayIcon
        ├─ 图标和提示文本
        ├─ 上下文菜单
        └─ activated / messageClicked
```

它不是一个 QWidget，不应该把它放进布局。它是依赖 GUI 事件循环工作的 `QObject`。

## 2. 最小可用代码

### 2.1 CMake

```cmake
find_package(Qt6 REQUIRED COMPONENTS Widgets)
target_link_libraries(mytarget PRIVATE Qt6::Widgets)
```

### 2.2 创建托盘图标和菜单

```cpp
#include <QAction>
#include <QApplication>
#include <QIcon>
#include <QMenu>
#include <QSystemTrayIcon>

int main(int argc, char *argv[])
{
    QApplication app(argc, argv);

    QMenu menu;
    QAction quitAction("退出", &menu);
    menu.addAction(&quitAction);

    QSystemTrayIcon tray(QIcon(":/icons/app.png"));
    tray.setToolTip("后台同步");
    tray.setContextMenu(&menu);
    tray.show();

    QObject::connect(&quitAction, &QAction::triggered,
                     &app, &QCoreApplication::quit);

    return app.exec();
}
```

使用前先检查环境：

```cpp
if (!QSystemTrayIcon::isSystemTrayAvailable()) {
    // 当前平台没有可用托盘
}
```

## 3. 核心使用模型

### 3.1 `show()` 只是显示托盘图标

构造对象、设置图标和菜单后，还要调用 `show()` 或 `setVisible(true)`。对象存在不代表托盘图标已经显示。

### 3.2 托盘菜单由你管理

`setContextMenu()` 只是把菜单关联到托盘图标。菜单对象的生命周期仍然要由父对象或调用方负责。常见做法是让菜单和托盘对象拥有同一个长期生命周期。

### 3.3 `activated()` 要按原因区分行为

```cpp
connect(&tray, &QSystemTrayIcon::activated,
        [&](QSystemTrayIcon::ActivationReason reason) {
    if (reason == QSystemTrayIcon::Trigger)
        mainWindow.showNormal();
});
```

不同平台对单击、双击、中键和右键的触发方式可能不同，不要只依赖某一种 reason 就假设所有系统一致。

### 3.4 气泡消息不是所有平台都支持

```cpp
if (QSystemTrayIcon::supportsMessages()) {
    tray.showMessage("同步完成", "文件已经同步。");
}
```

系统可能忽略超时时间，也可能不显示消息，具体取决于平台通知服务和用户设置。

### 3.5 托盘对象必须活到事件循环结束

如果在局部函数里创建一个栈对象，函数返回后托盘图标就会消失。它通常应该和应用或主窗口保持相同生命周期。

## 4. 适合用在哪里

- 最小化到托盘；
- 后台任务状态提示；
- 常驻服务的快速控制；
- 不希望主窗口一直占据任务栏的工具。

如果应用只是普通一次性窗口，不要为了“看起来像后台程序”强行加入托盘图标。

## 5. 常见误区

### 5.1 用 QCoreApplication 创建托盘图标

托盘图标属于 GUI/Widgets 能力，应该使用 `QApplication`。

### 5.2 创建后马上让对象销毁

托盘图标依赖对象生命周期和事件循环，局部对象离开作用域后图标就会消失。

### 5.3 不检查托盘是否可用

某些 Linux 桌面环境、远程会话或特殊窗口系统可能没有托盘实现。

### 5.4 把 `showMessage()` 当作可靠通知

它是“尽力显示”的平台通知，不是必达消息通道。关键消息仍应在主窗口或日志里保留。

### 5.5 把托盘图标和主窗口生命周期混在一起

关闭主窗口不一定应该退出应用；常见做法是重写关闭行为，隐藏窗口而保留托盘对象。

## API 速查表
| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造 | `QSystemTrayIcon(QObject *parent = nullptr)` | 创建一个没有初始图标的托盘对象。 | 后续要用 `setIcon()` 设置图标。 |
| 构造 | `QSystemTrayIcon(const QIcon &icon, QObject *parent = nullptr)` | 创建并设置初始图标的托盘对象。 | 对象仍需保持长期生命周期。 |
| 析构 | `~QSystemTrayIcon()` | 移除托盘图标并销毁对象。 | 销毁时托盘入口会消失。 |
| 菜单 | `setContextMenu(QMenu *menu)` | 设置托盘图标的右键菜单。 | 通常不把菜单所有权转给托盘对象，要自行保证菜单存活。 |
| 菜单 | `contextMenu() const` | 返回当前关联的上下文菜单。 | 未设置时返回 `nullptr`。 |
| 图标 | `icon() const` | 返回当前托盘图标。 | 图标应准备适合平台显示的尺寸。 |
| 图标 | `setIcon(const QIcon &icon)` | 设置托盘图标。 | 图标为空时平台上可能不显示有效入口。 |
| 提示 | `toolTip() const` | 返回鼠标悬停时的提示文本。 | 文本由平台托盘展示。 |
| 提示 | `setToolTip(const QString &tip)` | 设置鼠标悬停提示。 | 适合显示当前后台任务状态。 |
| 能力查询 | `isSystemTrayAvailable()` | 查询当前平台是否有可用系统托盘。 | 创建界面前应先检查。 |
| 能力查询 | `supportsMessages()` | 查询平台是否支持托盘消息。 | 支持不代表用户一定会看到通知。 |
| 几何 | `geometry() const` | 返回托盘图标在屏幕中的几何区域。 | 没有显示或平台不支持时结果可能无效。 |
| 状态 | `isVisible() const` | 查询托盘图标当前是否显示。 | 不等同于平台通知是否可用。 |
| 槽 | `setVisible(bool visible)` | 显示或隐藏托盘图标。 | `show()`/`hide()` 是便捷包装。 |
| 槽 | `show()` | 显示托盘图标。 | 必须有有效图标和事件循环。 |
| 槽 | `hide()` | 隐藏托盘图标。 | 隐藏后对象仍然存在。 |
| 通知 | `showMessage(const QString &, const QString &, const QIcon &, int msecs = 10000)` | 请求平台显示一条带图标的托盘通知。 | 是否显示、实际时长由平台和用户设置决定。 |
| 通知 | `showMessage(const QString &, const QString &, MessageIcon icon = Information, int msecs = 10000)` | 请求平台显示一条带标准类型图标的托盘通知。 | 需要先考虑 `supportsMessages()`。 |
| 信号 | `activated(ActivationReason reason)` | 托盘图标被用户激活时发出。 | 要根据 `Context`、`Trigger`、`DoubleClick` 等 reason 分支处理。 |
| 信号 | `messageClicked()` | 用户点击托盘通知时发出。 | 平台不支持通知或不提供点击事件时不会触发。 |
| 事件 | `event(QEvent *event)` | 处理托盘对象收到的通用事件。 | 通常由 Qt 内部调用。 |
| 枚举 | `ActivationReason` | 表示托盘图标被激活的原因。 | `Unknown`、`Context`、`DoubleClick`、`Trigger`、`MiddleClick`。 |
| 枚举 | `MessageIcon` | 表示托盘通知的标准图标类型。 | `NoIcon`、`Information`、`Warning`、`Critical`。 |

## 7. 一句话总结

`QSystemTrayIcon` 是桌面应用的系统托盘入口，重点是长期生命周期、平台能力检查、菜单管理和激活原因处理。
