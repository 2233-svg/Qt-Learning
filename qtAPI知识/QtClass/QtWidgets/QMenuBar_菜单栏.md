# Qt QMenuBar 深入笔记

> 适用版本：Qt 6 Widgets（本文按 Qt 6.11.1 API 整理）  
> 头文件：`#include <QMenuBar>`  
> 所属模块：`Qt6::Widgets`  
> 继承：`QWidget -> QMenuBar`  
> 定位：主窗口顶部的菜单入口容器

## 1. QMenuBar 解决什么问题

`QMenuBar` 负责把一组顶层菜单横向放在窗口顶部，比如“文件、编辑、视图、帮助”。它本身不执行业务逻辑，真正的命令通常放在 `QAction` 中；顶层入口通常是 `QMenu` 的 `menuAction()`。

可以把关系理解成：

```text
QMenuBar
├─ QAction / QMenu::menuAction()   顶层菜单入口
│  └─ QMenu
│     └─ QAction                   菜单里的具体命令
└─ cornerWidget                    菜单栏左/右角落的小控件
```

大多数 `QMainWindow` 程序不需要手动摆放菜单栏，直接用：

```cpp
QMenu *fileMenu = menuBar()->addMenu(tr("&File"));
fileMenu->addAction(openAct);
```

`QMainWindow::menuBar()` 会创建并管理菜单栏。只有在普通 `QWidget` 窗口里自己搭菜单，或者需要一个无父对象的全局菜单栏时，才直接创建 `QMenuBar`。

## 2. 最小可用代码

```cpp
#include <QAction>
#include <QApplication>
#include <QMainWindow>
#include <QMenu>
#include <QMenuBar>
#include <QStatusBar>

class MainWindow final : public QMainWindow
{
public:
    MainWindow()
    {
        auto *openAct = new QAction(tr("&Open"), this);
        openAct->setShortcut(QKeySequence::Open);

        auto *fileMenu = menuBar()->addMenu(tr("&File"));
        fileMenu->addAction(openAct);
        fileMenu->addSeparator();
        fileMenu->addAction(tr("E&xit"), qApp, &QApplication::quit);

        connect(menuBar(), &QMenuBar::hovered, this, [this](QAction *action) {
            statusBar()->showMessage(action->statusTip(), 1500);
        });
    }
};
```

`&File` 里的 `&` 会生成键盘助记符，常见效果是按 `Alt+F` 打开文件菜单。要显示真正的 `&`，写成 `&&`。

## 3. 菜单栏不是普通布局容器

`QMenuBar` 继承自 `QWidget`，但它不是给你随便 `addWidget()` 的横向布局。菜单栏的主要内容是 `QAction`：

- 用 `addMenu()` 添加 `QMenu`；
- 用继承自 `QWidget` 的 `addAction()` 添加普通顶层 action；
- 用 `addSeparator()` 做顶层分隔；
- 用 `removeAction()` 移除菜单项；
- 用 `clear()` 清空 action 列表。

在 `QMainWindow` 中，菜单栏的位置和尺寸由主窗口内部布局管理。官方文档也特别强调：菜单栏不需要你手动布局，它会自动贴在父窗口顶部并随父窗口调整。

## 4. QMenu、QAction 和 menuAction

`addMenu(QMenu *menu)` 返回的是这个菜单的 `menuAction()`：

```cpp
QMenu *viewMenu = new QMenu(tr("&View"), this);
QAction *viewEntry = menuBar()->addMenu(viewMenu);
viewEntry->setVisible(false);
```

这个返回值很有用，因为隐藏、禁用顶层菜单入口时，操作的通常是 `QAction`：

```cpp
viewMenu->menuAction()->setEnabled(false);
```

几个所有权规则要分清：

- `addMenu(QMenu *menu)`：菜单栏不接管已有菜单的所有权；
- `addMenu(const QString &title)`：菜单栏创建新菜单并接管所有权；
- `addMenu(const QIcon &, const QString &)`：同上，只是顶层入口带图标；
- `insertMenu(before, menu)`：把已有菜单插到指定 action 前面，也返回 `menuAction()`。

## 5. 高亮、触发和命中测试

菜单栏有自己的交互状态：

```cpp
QAction *current = menuBar()->activeAction();
menuBar()->setActiveAction(fileMenu->menuAction());
```

`activeAction()` 是当前高亮的顶层 action，偏“交互状态”；它不等于用户已经触发了某个命令。

如果要统一处理菜单栏中的菜单项：

```cpp
connect(menuBar(), &QMenuBar::triggered,
        this, &MainWindow::onMenuActionTriggered);
```

注意：`triggered(QAction *)` 针对属于该菜单栏的菜单里被鼠标触发的 action。日常开发中，更常见也更清晰的方式仍然是给每个业务 action 自己连接 `QAction::triggered()`。

`actionAt(point)` 和 `actionGeometry(action)` 适合调试或自定义交互：

- `actionAt()`：某个菜单栏局部坐标下是哪一个 action；点到空白或分隔符返回 `nullptr`；
- `actionGeometry()`：某个 action 在菜单栏中的矩形区域。

## 6. defaultUp：让菜单默认向上弹

默认情况下，菜单从菜单栏向下弹出。`defaultUp` 改的是默认弹出方向：

```cpp
menuBar->setDefaultUp(true);
```

它适合菜单栏放在内容下方的界面，比如某些底部控制条。  
这不是硬性保证：如果屏幕空间不足，Qt 会自动换到能放得下的方向。

## 7. nativeMenuBar：原生/全局菜单栏

`nativeMenuBar` 决定在支持的平台上，菜单栏是否交给系统原生菜单栏显示：

```cpp
menuBar()->setNativeMenuBar(false);
```

典型影响：

- macOS：菜单栏通常出现在屏幕顶部，而不是窗口内部；
- 部分 Linux 桌面：可能通过全局菜单栏服务显示；
- Windows 等不支持的平台：设置没有实际效果，读取通常为 `false`。

默认值跟应用属性 `Qt::AA_DontUseNativeMenuBar` 有关。显式调用 `setNativeMenuBar()` 会覆盖应用属性带来的默认策略。

macOS 还有菜单合并规则：`About`、`Preferences`、`Quit` 等 action 可能按 `QAction::menuRole` 被移动到系统应用菜单里。被移动后，槽函数仍然会按原 action 触发；如果不想自动合并，可把相关 action 的 `menuRole` 设为 `QAction::NoRole`。

如果要让 macOS 应用的多个窗口共享一个菜单栏，需要创建没有 parent 的 `QMenuBar`；不要用 `QMainWindow::menuBar()` 创建共享菜单栏，因为那样菜单栏会属于某一个主窗口。

## 8. cornerWidget：菜单栏角落控件

```cpp
auto *search = new QLineEdit;
search->setPlaceholderText(tr("Search"));
menuBar()->setCornerWidget(search, Qt::TopRightCorner);
```

角落控件适合放搜索框、用户按钮、同步状态之类的小控件。它显示在最后一个菜单项右侧，或者第一个菜单项左侧。

需要注意：

- 只支持 `Qt::TopRightCorner` 和 `Qt::TopLeftCorner`，其他角会产生警告；
- 菜单栏会把传入 widget reparent 到自己名下；
- 如果该角落原来已有 widget，旧 widget 不再由菜单栏管理，但仍可能是菜单栏的可见子控件，需要你自己隐藏、删除或重新安排。

## 9. 自定义绘制和扩展

普通应用不应该重写菜单栏的鼠标、键盘、绘制事件。平台风格、原生菜单、快捷键和可访问性都依赖 Qt 内部实现。

只有在做自定义菜单栏外观时，才考虑：

```cpp
void MyMenuBar::paintEvent(QPaintEvent *event)
{
    Q_UNUSED(event);
    // 使用 QStyleOptionMenuItem + QStyle 绘制，而不是硬画全部细节
}
```

`initStyleOption(QStyleOptionMenuItem *, const QAction *)` 是这里最有价值的保护函数：它能把菜单栏当前状态和 action 信息填进样式选项，避免自定义绘制漏掉选中、禁用、快捷键等状态。

## API 速查表
### 10.1 构造、属性与平台行为

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造 | `QMenuBar(QWidget *parent = nullptr)` | 创建顶层菜单入口容器。 | `QMainWindow` 中通常使用 `menuBar()` 获取现成对象。 |
| 析构 | `~QMenuBar()` | 销毁菜单栏。 | 菜单栏不会因为销毁而自动删除不属于它的已有菜单。 |
| 弹出方向 | `isDefaultUp() const` / `setDefaultUp(bool)` | 查询或设置菜单默认向上弹出。 | 屏幕空间不足时 Qt 仍可能自动改变方向。 |
| 平台行为 | `isNativeMenuBar() const` / `setNativeMenuBar(bool)` | 查询或设置是否使用系统原生/全局菜单栏。 | macOS 和部分 Linux 有实际效果，Windows 通常没有。 |
| 平台对象 | `platformMenuBar()` | 取得底层平台菜单栏对象。 | 只适合平台集成，不是普通业务菜单入口。 |
| macOS | `toNSMenu()` | 取得 macOS 原生 `NSMenu`。 | 仅 macOS；平台资源和 Qt 菜单生命周期要一起考虑。 |

### 10.2 菜单项管理

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 添加菜单 | `addMenu(QMenu *menu)` | 把已有菜单加入菜单栏，并返回它的 `menuAction()`。 | 菜单栏不接管已有菜单所有权；需要保证菜单活得足够久。 |
| 添加菜单 | `addMenu(const QString &title)` | 创建并追加一个带标题的菜单。 | 新建菜单由菜单栏的 Qt 对象树管理。 |
| 添加菜单 | `addMenu(const QIcon &icon, const QString &title)` | 创建并追加带图标的顶层菜单。 | 图标是否显示明显取决于平台菜单风格。 |
| 插入菜单 | `insertMenu(QAction *before, QMenu *menu)` | 把已有菜单插入到指定 action 前。 | 返回菜单的 `menuAction()`，`before` 应属于当前菜单栏。 |
| 分隔线 | `addSeparator()` / `insertSeparator(QAction *before)` | 添加顶层分隔 action。 | 顶层菜单通常少用，复杂菜单栏才需要。 |
| 清空 | `clear()` | 移除菜单栏中的所有 action。 | macOS 原生菜单合并后的项目可能受平台规则影响。 |
| Action | `QWidget::addAction(...)` | 添加普通顶层 action。 | 菜单栏主要承载 action，不要把它当普通布局。 |
| Action | `QWidget::removeAction(QAction *action)` | 移除某个顶层 action。 | 只解除关联，不等于删除 action。 |

### 10.3 交互状态与命中测试

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 交互状态 | `activeAction() const` / `setActiveAction(QAction *action)` | 读取或设置当前高亮的顶层 action。 | 高亮不等于已经触发，通常由键盘或鼠标导航维护。 |
| 命中测试 | `actionAt(const QPoint &point) const` | 根据菜单栏局部坐标查找 action。 | 空白或分隔线位置可能返回空指针。 |
| 几何查询 | `actionGeometry(QAction *action) const` | 返回 action 在菜单栏中的矩形区域。 | 适合自定义提示、定位和调试。 |
| 尺寸 | `sizeHint() const` / `minimumSizeHint() const` | 返回菜单栏推荐尺寸和最小推荐尺寸。 | 通常由主窗口布局系统调用。 |
| 尺寸协商 | `heightForWidth(int width) const` | 根据宽度计算所需高度。 | 菜单项很多时可能换行，由布局系统使用。 |
| 显示 | `setVisible(bool visible)` | 显示或隐藏菜单栏。 | 原生菜单栏平台的视觉结果可能由系统菜单机制决定。 |

### 10.4 角落控件

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 角落控件 | `setCornerWidget(QWidget *widget, Qt::Corner corner = Qt::TopRightCorner)` | 在菜单栏左上或右上角放置一个小控件。 | 只支持 `TopLeftCorner` 和 `TopRightCorner`；菜单栏会重新设置 parent。 |
| 角落控件 | `cornerWidget(Qt::Corner corner = Qt::TopRightCorner) const` | 查询指定角落当前控件。 | 替换前要明确旧控件的隐藏、复用或删除策略。 |

### 10.5 信号与扩展点

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 信号 | `hovered(QAction *action)` | 顶层菜单 action 被高亮时通知。 | 常用于把 `QAction::statusTip()` 显示到状态栏。 |
| 信号 | `triggered(QAction *action)` | 菜单栏体系中的 action 被触发时通知。 | 业务命令更推荐直接连接各自 `QAction::triggered()`。 |
| 样式 | `initStyleOption(QStyleOptionMenuItem *option, const QAction *action) const` | 填充某个菜单项绘制所需状态。 | 自定义绘制时调用基类，保留禁用、选中和助记符状态。 |
| Action 事件 | `actionEvent(QActionEvent *event)` | 响应 action 增删改并更新菜单栏布局。 | 派生重写要保持基类布局逻辑。 |
| 状态变化 | `changeEvent(QEvent *event)` | 响应字体、语言、样式等变化。 | 主题或翻译切换时可能触发。 |
| 键盘 | `keyPressEvent(QKeyEvent *event)` | 处理 Alt 助记符和方向键导航。 | 自定义快捷键不要破坏默认菜单可访问性。 |
| 鼠标 | `mousePressEvent(...)` / `mouseMoveEvent(...)` / `mouseReleaseEvent(...)` | 处理菜单入口按下、悬停和触发。 | 通常交给 Qt，只有深度交互定制才重写。 |
| 焦点 | `focusInEvent(...)` / `focusOutEvent(...)` / `leaveEvent(...)` | 维护菜单栏的键盘焦点和 hover 状态。 | 自定义时要保证焦点离开后菜单状态能恢复。 |
| 绘制 | `paintEvent(QPaintEvent *event)` | 绘制菜单栏外观。 | 优先使用 `QStyle` 和样式选项。 |
| 尺寸 | `resizeEvent(QResizeEvent *event)` | 尺寸变化后重新安排 action。 | 通常不需要业务侧重写。 |
| 定时/事件 | `timerEvent(...)` / `eventFilter(...)` / `event(...)` | 处理内部延迟、高亮、平台菜单和统一事件。 | 高级平台集成时才碰，优先保留基类。 |

## 11. 常见误区

### 11.1 给 QMainWindow 再手动 setLayout

`QMainWindow` 已经有自己的布局结构。菜单栏应该通过 `menuBar()`、`setMenuBar()` 或 `setMenuWidget()` 接入。

### 11.2 忽略 QAction 才是菜单入口

顶层菜单在菜单栏中也是一个 action。要隐藏或禁用某个菜单，改 `menu->menuAction()` 往往比改 `QMenu` 本身更准确。

### 11.3 在 macOS 上疑惑菜单项“跑了”

`About`、`Preferences`、`Quit` 这类菜单项可能被系统菜单合并规则移动。检查 `QAction::menuRole`，必要时设置为 `NoRole`。

### 11.4 用 cornerWidget 替代工具栏

`cornerWidget` 适合少量轻控件，不适合塞一排复杂按钮。高频操作应放 `QToolBar`，复杂筛选区域应放中央控件或 dock。

---

### 一句话总结

`QMenuBar` 是顶层菜单入口容器：用 `QMenu/QAction` 组织命令，用 `menuAction()` 控制菜单入口，用 `defaultUp/nativeMenuBar` 处理弹出方向和平台菜单，用 `cornerWidget` 放少量角落控件。
