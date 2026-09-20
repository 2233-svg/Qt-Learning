# Qt QMdiArea 深入笔记

> 适用版本：Qt 6 Widgets（本文按 Qt 6.11.1 API 整理）
> 头文件：`#include <QMdiArea>`
> 所属模块：`Qt6::Widgets`
> 继承：`QAbstractScrollArea -> QMdiArea`
> 常见搭档：`QMdiSubWindow`、`QMainWindow`、`QTabWidget`

## 1. QMdiArea 解决什么问题

`QMdiArea` 用来在一个主窗口里管理多个“内部窗口”。它不是普通的控件排版容器，而是一个多文档工作区：每个子窗口都能移动、缩放、最小化、最大化，用户可以在同一个应用里同时处理多个文档。

常见场景：

- 编辑器里同时打开多个文件；
- 设计器、图像工具、数据库工具的多工作区；
- 需要“平铺 / 层叠 / 切换上一个窗口”这类 MDI 操作；
- 想在“自由子窗口”和“标签页”之间切换显示方式。

它和 `QSplitter`、`QTabWidget` 的区别很明确：

| 类 | 主要职责 |
| --- | --- |
| `QSplitter` | 拖动分隔条调整区域大小。 |
| `QTabWidget` | 多个页面中一次只显示一个。 |
| `QMdiArea` | 管理一组可独立当窗口使用的文档子窗。 |

## 2. 最小可用代码

```cpp
#include <QApplication>
#include <QMainWindow>
#include <QMdiArea>
#include <QTextEdit>

int main(int argc, char *argv[])
{
    QApplication app(argc, argv);

    QMainWindow window;
    auto *mdiArea = new QMdiArea(&window);
    window.setCentralWidget(mdiArea);

    auto *editor = new QTextEdit;
    editor->setWindowTitle(QObject::tr("文档 1"));
    QMdiSubWindow *subWindow = mdiArea->addSubWindow(editor);
    subWindow->show();

    window.resize(1000, 700);
    window.show();
    return app.exec();
}
```

`addSubWindow(editor)` 会把普通 `QWidget` 包装成 `QMdiSubWindow`。这个返回值通常就是你后面控制标题、状态和关闭行为的入口。

## 3. 子窗口从哪里来

### 3.1 `addSubWindow`

```cpp
QMdiSubWindow *subWindow = mdiArea->addSubWindow(new QTextEdit);
subWindow->show();
```

这是最常见的入口。你给它一个普通 widget，`QMdiArea` 会替你创建内部窗口包装层。

如果你自己创建了 `QMdiSubWindow`，也可以直接加进去，但要自己管好关闭后的销毁：

```cpp
auto *subWindow = new QMdiSubWindow;
subWindow->setAttribute(Qt::WA_DeleteOnClose);
subWindow->setWidget(new QTextEdit);
mdiArea->addSubWindow(subWindow);
subWindow->show();
```

### 3.2 `removeSubWindow`

```cpp
mdiArea->removeSubWindow(subWindow);
subWindow->deleteLater();
```

`removeSubWindow()` 只负责从 MDI 区域摘掉，不负责删除对象。

它有两个容易踩坑的点：

- 传入 `QMdiSubWindow` 时，只是从区域移除，对象不会自动 delete；
- 传入内部 widget 时，只会把内部 widget 从包装层摘下，包装窗口本身不会因此消失。

所以动态关闭文档时，`removeSubWindow()` 之后要明确是否还要保留对象。

### 3.3 当前窗口

```cpp
QMdiSubWindow *active = mdiArea->activeSubWindow();
QMdiSubWindow *current = mdiArea->currentSubWindow();
QList<QMdiSubWindow *> list = mdiArea->subWindowList();
```

- `activeSubWindow()`：当前活动窗口；
- `currentSubWindow()`：当前内部页，通常和活动窗口一致；
- `subWindowList()`：按指定顺序返回所有子窗口，适合做窗口菜单。

## 4. 两种视图模式

```cpp
mdiArea->setViewMode(QMdiArea::SubWindowView);
mdiArea->setViewMode(QMdiArea::TabbedView);
```

`SubWindowView` 是传统 MDI，子窗口显示完整标题栏和边框。  
`TabbedView` 则把子窗口用标签页组织起来，适合编辑器式界面。

标签页模式下常配合这些设置：

```cpp
mdiArea->setDocumentMode(true);
mdiArea->setTabsClosable(true);
mdiArea->setTabsMovable(true);
mdiArea->setTabPosition(QTabWidget::North);
```

注意：这只是显示方式的切换，内部仍然是 `QMdiSubWindow`，不是把内容真变成 `QTabWidget` 页面。

## 5. 激活和排列

```cpp
mdiArea->setActivationOrder(QMdiArea::ActivationHistoryOrder);
mdiArea->tileSubWindows();
mdiArea->cascadeSubWindows();
mdiArea->activateNextSubWindow();
mdiArea->activatePreviousSubWindow();
mdiArea->closeActiveSubWindow();
mdiArea->closeAllSubWindows();
```

`WindowOrder` 的三种顺序分别是：

- `CreationOrder`：按创建顺序；
- `StackingOrder`：按堆叠顺序；
- `ActivationHistoryOrder`：按最近激活历史。

`ActivationHistoryOrder` 最适合实现 `Ctrl+Tab` 一类的切换。

## 6. 背景、选项和信号

```cpp
mdiArea->setBackground(QBrush(Qt::darkGray));
mdiArea->setOption(QMdiArea::DontMaximizeSubWindowOnActivation, true);

connect(mdiArea, &QMdiArea::subWindowActivated,
        [](QMdiSubWindow *window) {
            if (window)
                qDebug() << window->windowTitle();
        });
```

`DontMaximizeSubWindowOnActivation` 用来阻止“当前窗口最大化时，下一个激活窗口也跟着最大化”的默认行为。

`subWindowActivated` 是同步主窗口标题栏、工具栏、菜单状态的关键信号。窗口全关掉时参数可能是 `nullptr`。

## 7. 什么时候该用它

适合：

- 文档之间需要并排、层叠、快速切换；
- 用户明确知道自己在“多窗口工作区”里操作；
- 需要保留每个文档自己的窗口状态。

不适合：

- 只是想显示几个页面：用 `QStackedWidget` 或 `QTabWidget`；
- 只是想拖动分栏：用 `QSplitter`；
- 子内容只是普通表单：用布局就够了。

## API 速查表
### 8.1 类型、构造和基础属性

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 类型 | `AreaOption` | 描述 MDI 区域行为的单个选项。 | 当前最常用的是 `DontMaximizeSubWindowOnActivation`。 |
| 类型 | `AreaOptions` | `AreaOption` 的 flags 集合。 | 多个选项用 `|` 组合；查询时可用 `testOption()`。 |
| 选项 | `DontMaximizeSubWindowOnActivation` | 阻止激活下一个子窗口时自动把它最大化。 | 适合希望每个文档保留自己窗口状态的工作区。 |
| 类型 | `WindowOrder` | 指定子窗口列表和激活顺序的排序方式。 | 包括创建顺序、堆叠顺序和激活历史顺序。 |
| 类型 | `ViewMode` | 指定子窗口采用自由内部窗口还是标签页显示。 | `TabbedView` 是 MDI 的标签化呈现，不等价于普通 `QTabWidget`。 |
| 构造 | `QMdiArea(QWidget *parent = nullptr)` | 创建一个多文档工作区。 | 常作为 `QMainWindow` 的 central widget；它自己不创建文档内容。 |
| 析构 | `~QMdiArea()` | 销毁 MDI 工作区及其对象树关系。 | 关闭或销毁区域时，子窗口的清理要结合实际 parent 和关闭属性理解。 |
| 尺寸 | `sizeHint()` / `minimumSizeHint()` | 向外层布局提供工作区的推荐和最小尺寸。 | 影响主窗口初始化和工作区被压缩时的下限。 |
| 背景 | `background()` / `setBackground(const QBrush &)` | 读取或设置子窗口之间空白区域的背景画刷。 | 只影响 MDI 工作区背景，不会直接改变每个文档内容。 |

### 8.2 子窗口查找、创建和移除

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 当前窗口 | `currentSubWindow()` | 返回当前被认为是当前页面的子窗口。 | 在标签模式下通常就是当前标签；没有窗口时返回空指针。 |
| 活动窗口 | `activeSubWindow()` | 返回当前获得激活状态的子窗口。 | 可能为空；主窗口菜单和工具栏同步前要做空判断。 |
| 列表 | `subWindowList(WindowOrder order = CreationOrder)` | 按指定顺序返回全部 MDI 子窗口。 | 做“窗口”菜单、批量操作和最近窗口切换时很有用。 |
| 创建 | `addSubWindow(QWidget *, Qt::WindowFlags)` | 把普通内容 widget 包装成 `QMdiSubWindow` 并加入工作区。 | 返回的是窗口壳；内容 widget 和窗口壳要分别理解，通常还要显式 `show()`。 |
| 移除 | `removeSubWindow(QWidget *)` | 把指定的子窗口或其内容 widget 从 MDI 工作区摘下。 | 只改变归属和布局，不代表自动删除；之后要明确是复用还是 `deleteLater()`。 |

### 8.3 激活顺序、显示模式和标签属性

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 顺序 | `activationOrder()` / `setActivationOrder(WindowOrder)` | 读取或设置子窗口列表和切换操作采用的顺序策略。 | `ActivationHistoryOrder` 很适合实现类似 `Ctrl+Tab` 的最近使用切换。 |
| 模式 | `viewMode()` / `setViewMode(ViewMode)` | 读取或切换自由子窗口模式与标签模式。 | 切换显示模式不会把内容 widget 变成普通 `QTabWidget` 页面。 |
| 标签外观 | `documentMode()` / `setDocumentMode(bool)` | 控制标签模式是否采用更接近文档页的外观。 | 只在 Qt 构建包含 tabbar 功能时可用。 |
| 标签关闭 | `tabsClosable()` / `setTabsClosable(bool)` | 读取或设置标签上是否显示关闭按钮。 | 关闭按钮只提供 UI 入口，真正关闭前仍应处理未保存文档确认。 |
| 标签移动 | `tabsMovable()` / `setTabsMovable(bool)` | 读取或设置用户能否拖动标签改变顺序。 | 只改变标签顺序，不改变文档内容对象。 |
| 标签形状 | `tabShape()` / `setTabShape(...)` | 读取或设置标签的形状风格。 | 只影响标签模式下的 MDI 标签，不影响独立的 `QTabWidget`。 |
| 标签位置 | `tabPosition()` / `setTabPosition(...)` | 读取或设置标签位于顶部、底部、左侧还是右侧。 | 左右位置还会受到样式和平台表现影响。 |

### 8.4 操作子窗口和信号

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 选中 | `setActiveSubWindow(QMdiSubWindow *)` | 主动激活指定子窗口。 | 传入空指针可取消当前活动窗口；传入的窗口必须属于这个 MDI 区域。 |
| 排列 | `tileSubWindows()` | 把所有子窗口平铺排列。 | 适合窗口菜单；窗口很多时平铺后单个文档可能变得很小。 |
| 排列 | `cascadeSubWindows()` | 把所有子窗口层叠排列。 | 适合快速恢复传统 MDI 的可见标题栏布局。 |
| 切换 | `activateNextSubWindow()` / `activatePreviousSubWindow()` | 按激活顺序切换到下一个或上一个子窗口。 | 配合快捷键时要先设置合适的 `activationOrder`。 |
| 关闭 | `closeActiveSubWindow()` | 请求关闭当前活动子窗口。 | 会经过子窗口的关闭流程，内容 widget 可以拒绝关闭。 |
| 关闭 | `closeAllSubWindows()` | 依次请求关闭全部子窗口。 | 未保存文档可能中断关闭流程，不能简单当成无条件删除。 |
| 信号 | `subWindowActivated(QMdiSubWindow *)` | 子窗口激活状态变化时通知外部。 | 参数可能是 `nullptr`；常用来更新主窗口标题、菜单、工具栏和属性面板。 |

### 一句话总结

`QMdiArea` 管的是一组真正“像窗口”的文档页：把内容交给 `addSubWindow()`，把切换交给激活槽，把显示样式交给 `viewMode`，把对象生命周期和关闭结果分清，MDI 界面就会很顺。
