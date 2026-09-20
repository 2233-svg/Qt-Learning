# QMdiArea

> Qt 6.11.1 · Qt Widgets · 来自 `QMdiArea`

## 1. 先建立直觉

`QMdiArea` 是多文档界面的工作区。它在一个主窗口内部管理多个子窗口，让用户同时打开、排列、切换多个文档或视图。

它有两种典型形态：`SubWindowView` 像传统桌面里的窗口套窗口，可以平铺、层叠、拖动；`TabbedView` 更像现代 IDE 的标签页。选择哪一种，不只是视觉偏好，而是工作流选择：需要并排比较就用子窗口，主要一次编辑一个文档就用标签页。

## 2. 类说明

`QMdiArea` 继承自 `QAbstractScrollArea`，内部管理多个 `QMdiSubWindow`。你可以把普通 `QWidget` 通过 `addSubWindow()` 加进去，Qt 会为它包装一个 MDI 子窗口；也可以自己创建 `QMdiSubWindow` 以便定制窗口菜单、状态和行为。

MDI 的价值在复杂桌面软件中很直接：一个主窗口统一菜单、工具栏和停靠面板，多个文档在中央区域独立存在，并能通过激活窗口同步当前工具状态。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `addSubWindow(QWidget *, Qt::WindowFlags)` | 把一个页面控件加入 MDI，并返回包装后的 `QMdiSubWindow`。 |
| `removeSubWindow(QWidget *)` | 从 MDI 移除子窗口或其内部 widget，不一定负责业务对象保存。 |
| `activeSubWindow()` | 返回当前激活子窗口，适合菜单命令作用于当前文档。 |
| `currentSubWindow()` | 返回当前子窗口；和 active 的差别在焦点/激活细节上需要留意。 |
| `subWindowList(WindowOrder)` | 按创建、堆叠或激活历史顺序获取子窗口列表。 |
| `setActiveSubWindow(QMdiSubWindow *)` | 程序化切换当前文档。 |
| `setViewMode(SubWindowView/TabbedView)` | 在传统子窗口和标签页模式之间切换。 |
| `tileSubWindows()` | 平铺所有子窗口，适合比较多个视图。 |
| `cascadeSubWindows()` | 层叠排列子窗口，适合快速整理窗口。 |
| `closeActiveSubWindow()` / `closeAllSubWindows()` | 关闭当前或全部子窗口。 |
| `activateNextSubWindow()` / `activatePreviousSubWindow()` | 在文档之间循环切换。 |
| `setActivationOrder(WindowOrder)` | 控制切换和列表顺序采用创建顺序、堆叠顺序还是激活历史。 |
| `setTabsClosable()` / `setTabsMovable()` | TabbedView 下控制标签关闭和拖动排序。 |
| `setDocumentMode(bool)` | TabbedView 下使用更像文档标签的视觉风格。 |
| `subWindowActivated(QMdiSubWindow *)` | 当前子窗口变化时发出，用于刷新菜单、标题和属性面板。 |

## 4. 关键用法

```cpp
auto *mdi = new QMdiArea(this);
setCentralWidget(mdi);

auto *editor = new DocumentEditor;
auto *sub = mdi->addSubWindow(editor);
sub->setWindowTitle(editor->documentTitle());
sub->show();
```

菜单命令通常作用于当前子窗口：

```cpp
if (auto *sub = mdi->activeSubWindow()) {
    if (auto *editor = qobject_cast<DocumentEditor *>(sub->widget()))
        editor->save();
}
```

如果产品采用现代标签页风格：

```cpp
mdi->setViewMode(QMdiArea::TabbedView);
mdi->setTabsClosable(true);
mdi->setTabsMovable(true);
mdi->setDocumentMode(true);
```

## 5. 使用场景

适合 CAD、EDA、统计分析、数据库客户端、老牌办公软件、图像处理器、工程配置工具，以及“一个主框架，多份可并排文档”的应用。

不适合移动式简单界面，也不适合只有两三个固定页面的设置工具。那种场景 `QTabWidget`、`QStackedWidget` 或普通导航更清楚。

## 6. 常见坑与经验

关闭子窗口前要处理未保存状态。`closeAllSubWindows()` 会触发每个子窗口关闭流程，但你的文档确认逻辑需要放在合适的 `closeEvent()` 或业务层。

`addSubWindow()` 返回的是 `QMdiSubWindow`，不是原始 editor。需要访问内容时用 `sub->widget()`，并做好类型转换。

TabbedView 下很多用户会把它理解成普通标签页，所以关闭、拖动、当前文档标题和快捷键行为要和主流标签应用保持一致。
