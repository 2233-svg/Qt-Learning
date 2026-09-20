# QTabBar

> Qt 6.11.1 · Qt Widgets · 来自 `QTabBar`

## 1. 先建立直觉

`QTabBar` 是“标签条”，只负责显示和管理一排 tab：文字、图标、当前项、关闭按钮、拖动排序、滚动按钮。它不管理每个 tab 对应的页面内容。

`QTabWidget` 是标签条加页面栈的组合控件；`QTabBar` 是其中可单独使用、可替换、可深度定制的那一层。需要完整分页界面时用 `QTabWidget`；需要自己控制页面容器、标签行为或做 IDE 式标签栏时，直接用 `QTabBar` 更灵活。

## 2. 类说明

`QTabBar` 继承自 `QWidget`。每个 tab 有索引、文本、图标、tooltip、What's This、可见性、启用状态、自定义数据和可选的左右侧按钮。

它有很多视觉属性，例如形状、是否文档模式、文字省略、是否扩展填满空间。大型应用中，`QTabBar` 往往承载文档标签、页面导航、可关闭页面和拖拽重排，属于用户工作区的核心控件。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `addTab(text/icon, text)` | 在末尾添加标签，返回新 tab 索引。 |
| `insertTab(index, ...)` | 在指定位置插入标签。适合按业务顺序维护 tab。 |
| `removeTab(int)` | 删除标签，不会自动删除你自己的页面对象。 |
| `moveTab(from, to)` | 移动标签位置。配合 `movable` 或持久化顺序使用。 |
| `count()` | 当前 tab 数量。 |
| `setCurrentIndex(int)` / `currentIndex()` | 设置或读取当前标签。 |
| `tabAt(const QPoint &)` | 根据坐标找 tab，常用于右键菜单或拖放处理。 |
| `tabRect(int)` | 获取 tab 的几何区域，适合定位浮层或按钮。 |
| `setTabText()` / `tabText()` | 设置或读取标签文字。 |
| `setTabIcon()` / `tabIcon()` | 设置或读取标签图标。 |
| `setTabData()` / `tabData()` | 给 tab 存业务对象 id、路径、指针包装等数据。 |
| `setTabEnabled()` / `isTabEnabled()` | 控制 tab 是否可选。 |
| `setTabVisible()` / `isTabVisible()` | 控制 tab 是否显示。 |
| `setTabsClosable(bool)` | 显示内置关闭按钮。 |
| `tabCloseRequested(int)` | 用户点击关闭按钮时发出，应用需要自己决定是否关闭。 |
| `setMovable(bool)` | 允许用户拖动重排 tab。 |
| `tabMoved(int, int)` | tab 被移动后发出，用于同步模型顺序。 |
| `setElideMode(Qt::TextElideMode)` | 标签文字过长时如何省略。 |
| `setUsesScrollButtons(bool)` | tab 太多时是否使用滚动按钮。 |
| `setSelectionBehaviorOnRemove(...)` | 删除当前 tab 后选择左边、右边或上一个 tab。 |
| `setTabButton(index, position, widget)` | 在 tab 左侧或右侧放自定义小控件。 |
| `currentChanged(int)` | 当前标签变化时发出。 |

## 4. 关键用法

手写页面栈时，`QTabBar` 常和 `QStackedWidget` 配合：

```cpp
auto *tabs = new QTabBar(this);
auto *pages = new QStackedWidget(this);

connect(tabs, &QTabBar::currentChanged,
        pages, &QStackedWidget::setCurrentIndex);
```

可关闭标签页要把“请求关闭”和“真正关闭”分开：

```cpp
tabs->setTabsClosable(true);

connect(tabs, &QTabBar::tabCloseRequested, this, [=](int index) {
    if (maybeSaveDocument(index)) {
        closeDocument(index);
        tabs->removeTab(index);
    }
});
```

右键菜单常用 `tabAt()` 找目标：

```cpp
const int index = tabs->tabAt(event->pos());
if (index >= 0) {
    showTabContextMenu(index, tabs->mapToGlobal(event->pos()));
}
```

## 5. 使用场景

适合文档标签、设置页导航、日志/终端多标签、浏览器式页面、IDE 编辑器区域、仪表盘多视图切换，以及需要自定义关闭按钮、拖动排序、右键菜单的工作区。

如果每个 tab 只是对应一个普通页面，并且不需要特殊行为，`QTabWidget` 更省心。`QTabBar` 适合你想自己掌控页面管理、生命周期和标签行为的场景。

## 6. 常见坑与经验

tab 索引会变化。删除、插入、移动后，不要把旧 index 当作长期身份。长期身份应放在 `tabData()` 中。

`tabCloseRequested()` 只是请求。真正关闭前要处理未保存内容、后台任务、引用关系，然后再删 tab 和对应页面。

tab 太多时，不要无限压缩到看不清。设置 `elideMode`、启用滚动按钮，或者提供搜索/列表入口，比把所有标签挤成同样宽度更可用。
