# QStatusBar

> Qt 6.11.1 · Qt Widgets · 来自 `QStatusBar`

## 1. 先建立直觉

`QStatusBar` 是主窗口底部的状态区域，用来显示临时提示、当前状态和少量长期状态控件。它最适合回答“刚才发生了什么”和“当前处于什么状态”。

典型内容包括保存成功提示、鼠标悬停命令说明、坐标/页码、连接状态、进度小部件、当前编码。它不适合承载复杂操作，也不应该代替日志面板。

## 2. 类说明

- 头文件：`#include <QStatusBar>`
- 模块：`Qt6::Widgets`
- 继承自：`QWidget`
- 直接派生类：类页未列出

```cmake
find_package(Qt6 REQUIRED COMPONENTS Widgets)
target_link_libraries(mytarget PRIVATE Qt6::Widgets)
```

在 `QMainWindow` 中通常通过 `statusBar()` 获取并使用。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `QStatusBar(parent)` | 创建状态栏。 |
| `showMessage(message, timeout)` | 显示临时消息，timeout 为 0 表示一直显示到清除。 |
| `clearMessage()` | 清除当前临时消息。 |
| `currentMessage()` | 读取当前临时消息。 |
| `addWidget(widget, stretch)` | 添加普通状态控件，可能被临时消息遮挡。 |
| `insertWidget(index, widget, stretch)` | 在指定位置插入普通控件。 |
| `addPermanentWidget(widget, stretch)` | 添加永久控件，不被临时消息遮挡，通常靠右。 |
| `insertPermanentWidget(index, widget, stretch)` | 插入永久控件。 |
| `removeWidget(widget)` | 从状态栏移除控件。 |
| `setSizeGripEnabled()` / `isSizeGripEnabled()` | 是否显示右下角尺寸拖拽柄。 |
| `messageChanged(message)` | 临时消息变化信号。 |
| `reformat()` / `hideOrShow()` | 子类化时调整内部显示。 |

## 4. 关键用法

### 临时消息用于反馈动作

保存成功、复制完成、加载失败这类短反馈适合 `showMessage("Saved", 3000)`。消息应短，不要放长日志。超时后会自动清除，也可以用 `clearMessage()` 立即清除。

### 普通控件和永久控件不同

`addWidget()` 添加的控件可能被临时消息遮挡；`addPermanentWidget()` 添加的控件一直显示，适合连接状态、光标位置、缩放比例这类持续状态。把所有东西都做成永久控件会让状态栏拥挤。

### 和 QAction 状态提示配合

`QAction::statusTip` 可以在用户悬停菜单或工具栏命令时显示到状态栏。这是状态栏最经典的用途之一：解释当前命令，而不是弹 tooltip 打断视线。

### size grip

普通顶层窗口右下角可能显示 `QSizeGrip`。现代平台常由窗口边框负责调整尺寸，是否保留 size grip 取决于界面风格和窗口类型。

## 5. 常见坑与经验

- 状态栏消息不是错误处理机制，重要错误仍要有明确提示或日志入口。
- 永久控件太多会抢占临时消息空间。
- 添加 widget 后状态栏会重设 parent；不要再把同一 widget 放到其他布局。
- `timeout` 单位是毫秒。
- `currentMessage()` 只代表临时消息，不包含永久控件文本。
