# Qt QStatusBar 深入笔记

> 适用版本：Qt 6 Widgets（本文按 Qt 6.11.1 API 整理）  
> 头文件：`#include <QStatusBar>`  
> 所属模块：`Qt6::Widgets`  
> 继承：`QWidget -> QStatusBar`  
> 定位：主窗口底部的状态信息区域

## 1. QStatusBar 解决什么问题

`QStatusBar` 是应用窗口底部的状态信息区。它解决的是“在哪里显示短暂提示、当前状态和重要模式指示”的问题。

它常见于：

- 鼠标悬停菜单或工具按钮时显示说明；
- 编辑器里显示行号、列号、编码、缩放比例；
- 长任务时显示进度条；
- 显示 Caps Lock、连接状态、只读模式等常驻标记。

在 `QMainWindow` 中通常这样拿到它：

```cpp
statusBar()->showMessage(tr("Ready"), 2000);
```

`QMainWindow::statusBar()` 会按需创建状态栏；如果你要换成自己的状态栏，用 `setStatusBar(new QStatusBar(this))`。

## 2. 三类状态信息

`QStatusBar` 的核心不是“底部一个 QLabel”，而是把信息分成三类：

| 类型 | 显示方式 | 用来解决什么问题 |
| --- | --- | --- |
| Temporary 临时消息 | `showMessage()` 显示，占据状态栏大部分区域。 | 菜单说明、工具提示、操作结果这类短暂信息。 |
| Normal 普通控件 | `addWidget()` / `insertWidget()` 加入。 | 行号、页码、缩放等常规状态；可能被临时消息遮住。 |
| Permanent 永久控件 | `addPermanentWidget()` / `insertPermanentWidget()` 加入。 | 重要模式和警告；临时消息出现时也不被遮住。 |

这个分类非常重要。比如“已保存”适合 `showMessage("Saved", 1500)`；“第 12 行，第 8 列”适合 `addWidget(QLabel*)`；“离线/在线状态”适合 `addPermanentWidget(QLabel*)`。

## 3. 最小可用示例

```cpp
#include <QLabel>
#include <QMainWindow>
#include <QProgressBar>
#include <QStatusBar>

class MainWindow final : public QMainWindow
{
public:
    MainWindow()
    {
        auto *position = new QLabel(tr("Ln 1, Col 1"));
        statusBar()->addWidget(position);

        auto *progress = new QProgressBar;
        progress->setRange(0, 100);
        progress->setValue(25);
        statusBar()->addPermanentWidget(progress);

        statusBar()->showMessage(tr("Ready"), 2000);
    }
};
```

`addWidget()` 和 `addPermanentWidget()` 都会把 widget reparent 到状态栏；销毁状态栏时，通常也会由对象树清理这些子控件。

## 4. 临时消息：showMessage、clearMessage、currentMessage

```cpp
statusBar()->showMessage(tr("File saved"), 1500);
```

`showMessage(message, timeout)` 显示临时消息，单位是毫秒：

- `timeout > 0`：到时间后自动清除；
- `timeout == 0`：一直显示，直到调用 `clearMessage()` 或再次 `showMessage()`；
- 临时消息会隐藏普通控件，但不会隐藏永久控件。

读取当前临时消息：

```cpp
QString message = statusBar()->currentMessage();
```

清除当前临时消息：

```cpp
statusBar()->clearMessage();
```

注意：`showMessage(..., 0)` 仍然是临时消息，不是永久消息。Qt 自己也会用它显示工具提示或状态提示，所以重要常驻信息应该做成 widget，再用 `addPermanentWidget()` 加进去。

## 5. 普通控件和永久控件

### 5.1 普通控件

```cpp
auto *cursorLabel = new QLabel(tr("Ln 1, Col 1"));
statusBar()->addWidget(cursorLabel);
```

普通控件位于第一个永久控件的左侧。临时消息出现时，它可能被遮住。适合显示“有用但不紧急”的状态。

### 5.2 永久控件

```cpp
auto *modeLabel = new QLabel(tr("INS"));
statusBar()->addPermanentWidget(modeLabel);
```

永久控件位于状态栏最右侧，不会被临时消息遮住。适合显示模式、连接状态、后台任务进度等用户不能错过的信息。

### 5.3 stretch 的含义

`stretch` 决定状态栏变宽或变窄时，该控件如何参与空间分配：

```cpp
statusBar()->addWidget(pathLabel, 1);
statusBar()->addPermanentWidget(modeLabel, 0);
```

值越大，越容易吸收剩余空间。通常文本路径、搜索状态可以给 `1`；短小图标、模式标识保持 `0`。

## 6. 插入和移除

动态状态栏常用插入函数控制顺序：

```cpp
int index = statusBar()->insertWidget(0, cursorLabel);
statusBar()->insertPermanentWidget(0, connectionLabel);
```

如果 `index` 越界，Qt 会追加到末尾，并返回实际索引。

移除控件：

```cpp
statusBar()->removeWidget(cursorLabel);
cursorLabel->deleteLater();
```

`removeWidget()` 不删除控件，而是把它从状态栏移走并隐藏。以后要加回来，需要再次 `addWidget()`，然后对控件调用 `show()`。

## 7. sizeGripEnabled：右下角调整手柄

默认情况下，状态栏右下角会有一个 `QSizeGrip`，让用户拖拽调整顶层窗口大小：

```cpp
statusBar()->setSizeGripEnabled(false);
```

是否保留它取决于窗口形态：

- 普通桌面主窗口：通常保留；
- 固定大小工具窗、无边框窗口、自定义缩放区：常关闭；
- macOS 或某些平台外观下，实际显示会受系统风格影响。

## 8. 和 QAction::statusTip 的配合

菜单和工具栏 action 可以设置状态提示：

```cpp
openAct->setStatusTip(tr("Open an existing file"));
```

当 action 被菜单、工具栏等控件悬停时，Qt 会通过状态提示机制把说明显示到状态栏。  
这也是为什么临时消息不适合承载“永久状态”：用户移动鼠标时，它可能被新的状态提示覆盖。

## 9. 自定义状态栏时的扩展点

通常不用继承 `QStatusBar`。如果确实需要特殊外观或特殊隐藏规则，才考虑保护函数：

- `hideOrShow()`：根据临时消息状态，保证普通/永久控件的可见性正确；
- `reformat()`：控件集合或外观变化后重新整理状态栏；
- `paintEvent()`：绘制临时消息；
- `resizeEvent()`：窗口尺寸变化后调整内部区域；
- `showEvent()`：显示时同步内部状态；
- `event()`：统一事件入口。

普通业务代码更应该通过添加小控件、设置 stretch、响应 `messageChanged()` 来完成。

## API 速查表
### 10.1 构造、属性和临时消息

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造 | `QStatusBar(QWidget *parent = nullptr)` | 创建主窗口底部的状态栏容器。 | 默认通常带右下角 `QSizeGrip`；在 `QMainWindow` 中一般直接用 `statusBar()`。 |
| 析构 | `~QStatusBar()` | 销毁状态栏及仍由它管理的子控件。 | 已移除的控件不再由状态栏负责。 |
| 临时消息 | `showMessage(const QString &text, int timeout = 0)` | 显示一条临时状态消息。 | timeout 单位为毫秒；普通控件可能被临时消息遮住。 |
| 临时消息 | `clearMessage()` | 清除当前临时消息。 | 清除后被遮住的普通控件重新显示。 |
| 临时消息 | `currentMessage() const` | 读取当前临时消息文本。 | 没有临时消息时返回空字符串。 |
| 信号 | `messageChanged(const QString &text)` | 临时消息内容发生变化时通知。 | 参数为空通常表示消息被清除。 |
| 尺寸手柄 | `isSizeGripEnabled() const` / `setSizeGripEnabled(bool)` | 查询或开关右下角窗口缩放手柄。 | 固定大小、无边框或自定义缩放窗口常关闭。 |

### 10.2 普通控件和永久控件

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 普通控件 | `addWidget(QWidget *widget, int stretch = 0)` | 把一个普通状态控件加入状态栏。 | 位于永久控件左侧，可能被临时消息暂时遮住。 |
| 普通控件 | `insertWidget(int index, QWidget *widget, int stretch = 0)` | 在指定位置插入普通状态控件。 | 越界时追加并返回实际索引；状态栏会接管 parent。 |
| 永久控件 | `addPermanentWidget(QWidget *widget, int stretch = 0)` | 把重要的常驻状态控件加入右侧区域。 | 临时消息出现时也保持可见，适合连接状态和模式指示。 |
| 永久控件 | `insertPermanentWidget(int index, QWidget *widget, int stretch = 0)` | 在永久区域指定位置插入控件。 | stretch 越大越容易吸收剩余空间。 |
| 所有权 | `removeWidget(QWidget *widget)` | 从状态栏移除并隐藏控件。 | 不删除控件；之后重新加入并显示前要确认其生命周期。 |

### 10.3 保护函数和事件

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 内部布局 | `hideOrShow()` | 根据当前临时消息状态切换普通控件的显示。 | 主要由状态栏内部调用，派生类极少直接使用。 |
| 内部布局 | `reformat()` | 按控件集合、stretch 和当前样式重新整理状态栏。 | 自定义状态栏布局时才可能需要。 |
| 绘制 | `paintEvent(QPaintEvent *event)` | 绘制状态栏背景和临时消息区域。 | 普通外观优先交给 style。 |
| 尺寸 | `resizeEvent(QResizeEvent *event)` | 窗口大小变化时调整内部区域。 | 重写时要保留默认布局计算。 |
| 显示 | `showEvent(QShowEvent *event)` | 状态栏显示时同步内部状态。 | 派生类重写应调用基类。 |
| 事件 | `event(QEvent *event)` | 状态栏统一事件入口。 | 只有高级事件定制才需要重写。 |

## 11. 常见误区

### 11.1 把 showMessage 当永久状态

`showMessage(..., 0)` 只是“不会自动消失的临时消息”。它仍然会遮住普通控件，也可能被新的临时提示替换。

### 11.2 removeWidget 后以为对象已删除

`removeWidget()` 不删除对象。长期不用的控件要自己 `deleteLater()`；只是临时拿掉，则以后重新添加并 `show()`。

### 11.3 所有状态都塞成文本

进度、连接、模式、错误级别常常更适合 `QProgressBar`、`QLabel`、`QToolButton` 或自定义小控件。状态栏是 widget 容器，不只是字符串输出框。

### 11.4 忽略临时消息会遮住普通控件

如果信息非常重要，不要用 `addWidget()`，用 `addPermanentWidget()`。

---

### 一句话总结

`QStatusBar` 把底部状态分成临时消息、普通控件和永久控件：短提示用 `showMessage()`，常规状态用 `addWidget()`，关键模式和进度用 `addPermanentWidget()`，移除控件时记得它只会被隐藏而不会被删除。
