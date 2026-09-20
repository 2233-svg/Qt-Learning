# Qt QMenu 深入笔记

> 适用版本：Qt 6 Widgets（本文按 Qt 6.11.1 API 整理）  
> 头文件：`#include <QMenu>`  
> 所属模块：`Qt6::Widgets`  
> 继承：`QWidget -> QMenu`  
> 定位：由 `QAction` 组成的弹出菜单或菜单栏菜单

## 1. QMenu 解决什么问题

`QMenu` 是“动作列表的可视化容器”。它不是一个普通面板，而是把一组 `QAction` 纵向排开，让用户通过点击、悬停、快捷键或子菜单完成选择。

它常见于三种地方：

- 菜单栏里的下拉菜单；
- 右键弹出的上下文菜单；
- 工具栏按钮带的弹出菜单。

你可以把它理解成：

```text
QAction  ->  QMenu  ->  用户可见的菜单项
```

菜单里的真正动作通常还是 `QAction`，`QMenu` 只是展示、分组、触发和层级组织这些动作。

## 2. 菜单怎么显示

`QMenu` 不能靠 `show()` 当普通窗口那样用。要显示它，应该用：

```cpp
menu.exec(QCursor::pos());
// 或
menu.popup(widget->mapToGlobal(QPoint(0, 0)));
```

两者区别：

- `exec()`：同步，等用户选完再返回；
- `popup()`：异步，不阻塞当前代码。

`exec()` 适合临时上下文菜单；`popup()` 更适合非阻塞显示。  
显示时不要依赖当前 `size()`，应使用 `sizeHint()` 或让 Qt 自己计算位置，因为菜单会按内容动态调整尺寸。

## 3. 菜单的基本构成

### 3.1 Action

```cpp
menu.addAction(tr("保存"), this, &MainWindow::saveFile);
```

菜单项本质上是 `QAction`。  
`triggered(QAction *)` 会告诉你到底是哪一个动作被选中了；如果是一组相关动作，可以把它们连到同一个槽里。

### 3.2 Submenu

```cpp
QMenu *recent = menu.addMenu(tr("最近文件"));
recent->addAction("a.txt");
```

`addMenu()` 既能接一个已有 `QMenu*`，也能直接创建新子菜单。子菜单本身也由 `QAction` 表示，可以被塞进菜单栏或工具栏。

### 3.3 Separator 和 Section

```cpp
menu.addSeparator();
menu.addSection(tr("导入导出"));
```

`addSeparator()` 是纯分隔线。  
`addSection()` 是“带标题的分组线”，本质上也是一个 `QAction::isSeparator() == true` 的动作，只是带了文本和可选图标提示。样式是否绘制标题，取决于平台和 `QStyle`。

`separatorsCollapsible` 默认是 `true`，会把连续分隔线、首尾分隔线折叠掉。这个属性很实用，能避免菜单看起来像一堆空白切口。

## 4. 重要行为：menuAction、触发和可见性

每个 `QMenu` 都有一个关联动作：

```cpp
QAction *act = menu.menuAction();
```

这个 action 很重要，因为：

- 它能被加入别的菜单，作为子菜单入口；
- 它能被插入菜单栏或工具栏；
- 它的 `text` 对应菜单标题；
- 它的 `icon` 对应菜单图标。

如果要在菜单栏里隐藏或禁用菜单，通常改的是 `menuAction()`，而不是直接对 `QMenu` 调 `show()/hide()`。

`triggered(QAction *)` 和 `hovered(QAction *)` 都是菜单级信号：

- `triggered`：用户最终点了哪一项；
- `hovered`：用户悬停到了哪一项，常用于状态栏提示。

## 5. 面板化行为：tear-off

```cpp
menu.setTearOffEnabled(true);
```

启用后，菜单顶部会出现一个 tear-off 句柄，用户可以把菜单“扯”成一个独立窗口。  
这个功能更像老式桌面应用的快捷面板，Qt 仍保留它，但现代项目里通常更常见的是工具栏。

相关 API：

- `isTearOffEnabled()` / `setTearOffEnabled()`：开关功能；
- `showTearOffMenu()`：强制显示 torn-off 菜单；
- `hideTearOffMenu()`：强制隐藏；
- `isTearOffMenuVisible()`：查询当前是否处于 torn-off 状态。

## 6. 默认动作与活动动作

```cpp
menu.setDefaultAction(openRecent);
menu.setActiveAction(saveAct);
```

`defaultAction()` 是“默认发生什么”的动作，`QStyle` 可能给它额外提示；  
`activeAction()` 是当前高亮项，常和键盘导航、鼠标悬停相关。

它们不是同一个概念：

- 默认动作偏语义；
- 活动动作偏当前交互状态。

## 7. 右键菜单与状态菜单

```cpp
void MainWindow::contextMenuEvent(QContextMenuEvent *e)
{
    menu.exec(e->globalPos());
}
```

`QMainWindow::createPopupMenu()` 默认会为工具栏和 dock 生成一个可见性菜单。  
如果你想统一做“视图”菜单，菜单项里通常放 `QDockWidget::toggleViewAction()` 和 `QToolBar::toggleViewAction()`。

## 8. macOS 和原生菜单

`toNSMenu()`、`setAsDockMenu()`、`setPlatformMenu()`、`platformMenu()` 这些接口主要是平台集成相关。  
如果你不是在做 macOS 原生菜单联动，通常不用碰它们。

`menuInAction(const QAction *)` 可以从一个 action 取回其中的菜单，适合处理“某个 action 实际挂着子菜单”的情况。

## 9. 级联与布局

```cpp
QAction *at = menu.actionAt(point);
QRect r = menu.actionGeometry(at);
```

这两类函数适合做自定义交互和调试：

- `actionAt()`：点到了哪个动作；
- `actionGeometry()`：该动作在菜单中的几何区域。

`columnCount()` 是受保护接口，表示菜单需要几列才能完整显示。它主要用于菜单放不下屏幕时的自动排版。

## API 速查表
### 10.1 属性与构造

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 图标 | `icon() const` / `setIcon(const QIcon &icon)` | 读取或设置菜单标题图标。 | 等价于操作 `menuAction()->icon()`；显示效果受平台风格影响。 |
| 分隔线 | `separatorsCollapsible() const` / `setSeparatorsCollapsible(bool collapse)` | 控制连续、首尾分隔线是否自动折叠。 | 默认通常开启，动态菜单里可避免出现多余空白。 |
| 扯出菜单 | `isTearOffEnabled() const` / `setTearOffEnabled(bool)` | 查询或开关用户把菜单扯成独立面板的能力。 | 现代界面较少用，启用前要考虑平台体验。 |
| 标题 | `title() const` / `setTitle(const QString &title)` | 读取或设置菜单标题。 | 标题也会同步到 `menuAction()->text()`。 |
| 动作提示 | `toolTipsVisible() const` / `setToolTipsVisible(bool visible)` | 控制菜单项 action 的提示显示。 | 默认关闭；关键说明更适合状态栏或菜单文本。 |
| 构造 | `QMenu(QWidget *parent = nullptr)` | 创建一个空菜单。 | 可作为上下文菜单、子菜单或工具按钮弹出菜单。 |
| 构造 | `QMenu(const QString &title, QWidget *parent = nullptr)` | 创建并设置标题的菜单。 | 作为菜单栏顶层菜单时常用。 |
| 析构 | `~QMenu()` | 销毁菜单及由其管理的资源。 | 已加入其他容器但不属于菜单的 action 生命周期要单独确认。 |

### 10.2 动作管理

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| Action | `addAction(...)` | 向菜单追加一个命令 action。 | 菜单内容的核心是 action，不是子 widget；Qt 6.4 起优先使用新的重载形式。 |
| 子菜单 | `addMenu(QMenu *menu)` | 把已有子菜单加入当前菜单，并返回其 `menuAction()`。 | 已有菜单的所有权不一定转移，要按创建方式管理生命周期。 |
| 子菜单 | `addMenu(const QString &title)` / `addMenu(const QIcon &icon, const QString &title)` | 创建并加入一个新子菜单。 | 新子菜单会纳入当前菜单的对象树管理。 |
| 分隔线 | `addSeparator()` | 添加纯视觉分隔线。 | 动态菜单可配合 `separatorsCollapsible` 避免首尾空线。 |
| 分组 | `addSection(const QString &text)` / `addSection(const QIcon &icon, const QString &text)` | 添加带标题的分组区段。 | 本质仍是 separator action，是否显示标题由 style 决定。 |
| 插入 | `insertMenu(QAction *before, QMenu *menu)` | 在指定 action 前插入子菜单。 | `before` 必须属于当前菜单；返回子菜单的 menu action。 |
| 插入 | `insertSeparator(QAction *before)` | 在指定 action 前插入分隔线。 | 返回新建的 separator action。 |
| 插入 | `insertSection(QAction *before, ...)` | 在指定 action 前插入带标题的分组。 | 适合动态构建菜单。 |
| 清空 | `clear()` | 移除菜单中的 action。 | 菜单拥有且未被其他 widget 使用的 action 可能被删除，外部共享 action 要谨慎。 |
| 查询 | `isEmpty() const` | 判断菜单是否没有可显示的有效动作。 | 不完全等价于 `actions().isEmpty()`，因为 separator/隐藏 action 会影响判断。 |

### 10.3 显示、选择与导航

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 异步显示 | `popup(const QPoint &pos, QAction *at = nullptr)` | 在指定全局坐标非阻塞弹出菜单。 | 适合右键菜单、工具按钮菜单和不希望阻塞当前函数的场景。 |
| 同步显示 | `exec()` / `exec(const QPoint &pos, QAction *at = nullptr)` | 同步弹出菜单并等待用户选择。 | 会运行局部事件循环；不要在复杂状态锁持有期间调用。 |
| 临时显示 | `QMenu::exec(const QList<QAction *> &actions, const QPoint &pos, QAction *at = nullptr, QWidget *parent = nullptr)` | 用一组 action 临时弹出菜单。 | 适合一次性上下文菜单，不必长期创建 QMenu。 |
| 扯出菜单 | `showTearOffMenu()` / `showTearOffMenu(const QPoint &pos)` | 显示可独立存在的扯出菜单。 | 只有启用 tear-off 后才有明确意义。 |
| 扯出菜单 | `hideTearOffMenu()` / `isTearOffMenuVisible() const` | 隐藏或查询扯出菜单状态。 | 扯出窗口仍受菜单对象生命周期影响。 |
| 默认动作 | `setDefaultAction(QAction *action)` / `defaultAction() const` | 设置或读取菜单的默认 action。 | 默认动作是语义提示，不等于当前高亮或立即触发。 |
| 当前动作 | `setActiveAction(QAction *action)` / `activeAction() const` | 设置或读取当前高亮 action。 | 常由键盘和鼠标导航维护。 |
| 命中测试 | `actionAt(const QPoint &point) const` | 查询菜单局部坐标对应的 action。 | 空白位置返回空指针。 |
| 几何查询 | `actionGeometry(QAction *action) const` | 查询 action 在菜单中的矩形。 | 自定义提示、定位和调试时使用。 |

### 10.4 信号

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 信号 | `aboutToShow()` | 菜单即将显示时通知。 | 动态填充最近文件、上下文操作时最常用。 |
| 信号 | `aboutToHide()` | 菜单即将隐藏时通知。 | 可清理临时 action、高亮和悬停状态。 |
| 信号 | `hovered(QAction *action)` | 用户悬停或键盘高亮某个 action 时通知。 | 常把 action 的 status tip 显示到状态栏。 |
| 信号 | `triggered(QAction *action)` | 菜单中的 action 被触发时通知。 | 适合菜单级统一分派；复杂业务仍可直接连接 action。 |

### 10.5 受保护和平台相关接口

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 布局 | `columnCount() const` | 返回菜单在屏幕高度不足时需要排成的列数。 | 主要由菜单内部布局使用。 |
| 样式 | `initStyleOption(QStyleOptionMenuItem *option, const QAction *action) const` | 填充单个菜单项的绘制状态。 | 自定义绘制时调用基类，保留禁用、勾选和快捷键状态。 |
| 事件 | `changeEvent(...)` / `keyPressEvent(...)` | 响应样式变化和键盘导航。 | 菜单的键盘可访问性依赖默认实现。 |
| 鼠标 | `mousePressEvent(...)` / `mouseMoveEvent(...)` / `mouseReleaseEvent(...)` | 处理按下、悬停和触发动作。 | 一般不重写，避免破坏子菜单和 action 状态。 |
| 滚轮 | `wheelEvent(QWheelEvent *event)` | 菜单项很多时处理滚轮浏览。 | 只在自定义菜单交互时关注。 |
| 生命周期 | `enterEvent(...)` / `leaveEvent(...)` / `hideEvent(...)` | 维护进入、离开和隐藏状态。 | 清理自定义状态时要和默认菜单生命周期一致。 |
| 绘制 | `paintEvent(QPaintEvent *event)` | 绘制菜单本体。 | 优先依赖 QStyle 和 style option。 |
| Action 事件 | `actionEvent(QActionEvent *event)` | 响应菜单 action 增删改。 | 动态菜单派生类要保留布局更新。 |
| 定时/事件 | `timerEvent(...)` / `event(...)` / `focusNextPrevChild(bool next)` | 处理延迟弹出、统一事件和焦点移动。 | 高级定制才重写，通常调用基类。 |
| macOS | `setAsDockMenu()` / `toNSMenu()` | 把菜单接入 macOS Dock 或取得原生菜单对象。 | 仅 macOS 平台。 |
| 关联查询 | `menuInAction(const QAction *action)` | 从 action 反查它关联的子菜单。 | 工具栏按钮、菜单入口排查层级关系时有用。 |

## 11. 常见误区

### 11.1 直接 `show()` 菜单

菜单应该用 `popup()` 或 `exec()` 弹出。`show()` 不是菜单的正常使用方式。

### 11.2 把菜单项当普通控件管理

菜单的语义核心是 `QAction`，不是子控件树。要动态控制可见性、勾选状态、快捷键和文本，改的是 `QAction`。

### 11.3 忽略 `menuAction()`

子菜单、菜单栏和工具栏都围绕 `menuAction()` 运行。很多“菜单不显示/不隐藏”的问题，本质上是改错对象了。

### 11.4 重复插入同一个菜单

尤其在 macOS 和原生菜单体系里，同一个 `QMenu` 不能随便到处插。需要时应创建新的菜单对象。

---

### 一句话总结

`QMenu` 是动作的弹出容器：用 `QAction` 组成内容，用 `popup/exec` 显示，用 `menuAction()` 接入别的菜单或工具栏，用 `aboutToShow/triggered/hovered` 驱动动态行为。
