# Qt QTabBar 深入笔记

> 适用版本：Qt 6 Widgets（本文按 Qt 6.11.1 API 整理）
> 头文件：`#include <QTabBar>`
> 所属模块：`Qt6::Widgets`
> 继承：`QWidget -> QTabBar`
> 常见搭档：`QTabWidget`、`QStackedWidget`、`QStackedLayout`

## 1. QTabBar 解决什么问题

`QTabBar` 只负责显示和管理“一排标签”。它知道有哪些 tab、哪个 tab 当前选中、tab 的文字和图标是什么、tab 能不能拖动或关闭，但它**不负责管理标签背后的页面**。

这点要和 `QTabWidget` 分清：

```text
QTabBar       只管理标签条
QStackedWidget 只管理页面
QTabWidget     把两者组合起来
```

适合单独使用 `QTabBar` 的场景：

- 自己设计页面切换逻辑；
- 标签条和页面区域不在同一个布局位置；
- 多个视图共享一个 tab 导航条；
- 做文档编辑器、浏览器式标签页；
- 需要完全控制 tab 的拖动、关闭和自定义按钮。

如果只是常规的“上面标签、下面页面”，优先使用 `QTabWidget`；如果标签和页面需要解耦，才直接使用 `QTabBar`。

## 2. 最小可用代码

### 2.1 CMake

```cmake
find_package(Qt6 REQUIRED COMPONENTS Widgets)
target_link_libraries(mytarget PRIVATE Qt6::Widgets)
```

### 2.2 QTabBar + QStackedWidget

```cpp
#include <QApplication>
#include <QLabel>
#include <QStackedWidget>
#include <QTabBar>
#include <QVBoxLayout>
#include <QWidget>

int main(int argc, char *argv[])
{
    QApplication app(argc, argv);

    QWidget window;
    auto *tabs = new QTabBar;
    auto *pages = new QStackedWidget;

    pages->addWidget(new QLabel("General"));
    pages->addWidget(new QLabel("Network"));

    tabs->addTab("General");
    tabs->addTab("Network");

    QObject::connect(tabs, &QTabBar::currentChanged,
                     pages, &QStackedWidget::setCurrentIndex);

    auto *layout = new QVBoxLayout(&window);
    layout->addWidget(tabs);
    layout->addWidget(pages);
    window.show();
    return app.exec();
}
```

这里 `QTabBar` 发出的是索引变化，页面切换由外部对象完成。也就是说，tab 的索引是两者之间的协议。

## 3. tab 的生命周期和索引

### 3.1 添加和插入

```cpp
int index = tabs->addTab(QIcon(":/icons/file.png"), "main.cpp");
int inserted = tabs->insertTab(0, "Welcome");
```

返回值是实际插入位置。后续如果在前面插入或删除 tab，原来的索引可能变化，因此不要把索引永久当作业务 ID。

如果需要稳定标识，应使用：

```cpp
tabs->setTabData(index, documentId);
```

### 3.2 删除和移动

```cpp
tabs->removeTab(index);
tabs->moveTab(from, to);
```

`QTabBar` 只删除或移动标签本身，不会替你删除页面对象，因为它根本不知道页面是谁。页面生命周期要由 `QStackedWidget` 或业务层管理。

### 3.3 当前 tab

```cpp
int index = tabs->currentIndex();
tabs->setCurrentIndex(index);
```

当前索引变化会发出 `currentChanged(int)`。当 tab 被删除时，`selectionBehaviorOnRemove` 决定应该选左边、右边还是之前的 tab。

## 4. tab 的外观和交互

### 4.1 文本、图标和附加数据

```cpp
tabs->setTabText(index, "Settings");
tabs->setTabIcon(index, QIcon(":/icons/settings.png"));
tabs->setTabData(index, QVariant::fromValue(documentId));
```

每个 tab 都可以保存：

- 文本；
- 图标；
- 工具提示；
- What's This 文本；
- 自定义 `QVariant` 数据；
- 文字颜色。

### 4.2 禁用和隐藏

```cpp
tabs->setTabEnabled(index, false);
tabs->setTabVisible(index, false);
```

禁用是“看得到但不能正常交互”，隐藏是“标签入口不显示”。两者都不会自动删除关联页面。

### 4.3 关闭按钮

```cpp
tabs->setTabsClosable(true);
QObject::connect(tabs, &QTabBar::tabCloseRequested,
                 tabs, [tabs](int index) {
                     tabs->removeTab(index);
                 });
```

`setTabsClosable(true)` 只负责显示关闭按钮；真正删除 tab 需要你响应 `tabCloseRequested()`。

### 4.4 自定义 tab 两侧按钮

```cpp
tabs->setTabButton(index, QTabBar::RightSide,
                   new QPushButton(QStringLiteral("x")));
```

这适合做文档关闭按钮、状态标记、未保存提示等。按钮是 `QWidget`，加入后由 tab bar 接管其归属，替换或移除时要明确它的生命周期。

## 5. 拖动、滚动和尺寸

```cpp
tabs->setMovable(true);
tabs->setUsesScrollButtons(true);
tabs->setExpanding(false);
tabs->setElideMode(Qt::ElideRight);
```

- `movable`：用户能否拖动重排；
- `usesScrollButtons`：tab 太多时是否显示滚动按钮；
- `expanding`：是否把 tab 拉伸到填满空间；
- `elideMode`：文字太长时如何省略。

如果用户拖动 tab，`tabMoved(from, to)` 会发出。这个信号是同步业务顺序的关键。

## 6. 常见误区

### 6.1 不要把 QTabBar 当成页面容器

`QTabBar` 没有 `widget(index)`、`removeTab()` 也不会处理页面对象。页面切换必须自己和 `QStackedWidget`、`QStackedLayout` 或其它视图连接。

### 6.2 不要把 index 当永久 ID

插入、删除、移动都会改变索引。文档编辑器应该把文档 ID 放到 `tabData()`，而不是把当前 index 写进业务对象。

### 6.3 关闭按钮不会自动删除 tab

`tabCloseRequested()` 是请求信号，不是自动删除动作。你可以在信号里询问“是否保存”，确认后再删除。

## API 速查表
| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造 | `QTabBar(QWidget *parent = nullptr)` | 创建一个空的标签条。 | 不会自动创建页面容器。 |
| 析构 | `~QTabBar()` | 销毁标签条。 | 标签按钮等子控件随对象树处理。 |
| 枚举 | `Shape` | 定义圆角或三角形 tab 的方向和形状。 | 影响绘制方向。 |
| 枚举 | `ButtonPosition` | 指定 tab 按钮放左侧还是右侧。 | 用于 `setTabButton()`。 |
| 枚举 | `SelectionBehavior` | 指定删除当前 tab 后选择哪一个 tab。 | `SelectPreviousTab` 对编辑器体验常更自然。 |
| 属性 | `shape : Shape` | 设置 tab 的整体形状方向。 | 北/南/东/西方向都支持。 |
| 属性 | `currentIndex : int` | 当前选中的 tab 索引。 | 变化时发出 `currentChanged`。 |
| 属性 | `count : int` | tab 总数。 | 只读。 |
| 属性 | `drawBase : bool` | 是否绘制 tab bar 基础线。 | 常用于配合自定义页面外观。 |
| 属性 | `iconSize : QSize` | tab 图标的最大尺寸。 | 影响所有 tab 的图标显示。 |
| 属性 | `elideMode : Qt::TextElideMode` | 文字过长时的省略方式。 | 影响长标题可读性。 |
| 属性 | `usesScrollButtons : bool` | tab 太多时是否显示滚动按钮。 | 移动端或窄窗口常用。 |
| 属性 | `tabsClosable : bool` | 是否显示 tab 关闭按钮。 | 仍需处理 `tabCloseRequested`。 |
| 属性 | `selectionBehaviorOnRemove : SelectionBehavior` | 删除当前 tab 后选择哪一项。 | 决定关闭页面后的焦点体验。 |
| 属性 | `expanding : bool` | 是否让 tab 扩展填满可用空间。 | 文档型 tab 通常可关闭。 |
| 属性 | `movable : bool` | 用户是否可以拖动 tab。 | 配合 `tabMoved` 保存顺序。 |
| 属性 | `documentMode : bool` | 使用更接近文档编辑器的外观。 | 主要影响样式表现。 |
| 属性 | `autoHide : bool` | tab 数量不足时是否自动隐藏 tab bar。 | 适合可选标签页。 |
| 属性 | `changeCurrentOnDrag : bool` | 拖动经过 tab 时是否切换当前 tab。 | 多文档拖动时可改善体验。 |
| 查询 | `shape() const` | 返回 tab 形状。 | 与样式方向有关。 |
| 修改 | `setShape(Shape shape)` | 设置 tab 形状。 | 改变整体绘制方向。 |
| 修改 | `addTab(const QString &text)` | 追加一个文字 tab。 | 返回实际索引。 |
| 修改 | `addTab(const QIcon &icon, const QString &text)` | 追加带图标 tab。 | 图标尺寸受 `iconSize` 影响。 |
| 修改 | `insertTab(int index, const QString &text)` | 在指定位置插入 tab。 | 插入会改变后续索引。 |
| 修改 | `insertTab(int index, const QIcon &icon, const QString &text)` | 在指定位置插入带图标 tab。 | 返回实际索引。 |
| 修改 | `removeTab(int index)` | 删除指定 tab。 | 不负责删除页面对象。 |
| 修改 | `moveTab(int from, int to)` | 移动 tab 位置。 | 会发出 `tabMoved`。 |
| 查询 | `isTabEnabled(int index) const` | 查询 tab 是否启用。 | 禁用不等于隐藏。 |
| 修改 | `setTabEnabled(int index, bool enabled)` | 启用或禁用 tab。 | 禁用后仍保留 tab。 |
| 查询 | `isTabVisible(int index) const` | 查询 tab 是否可见。 | 只反映入口显示状态。 |
| 修改 | `setTabVisible(int index, bool visible)` | 显示或隐藏 tab。 | 不会删除页面。 |
| 查询 | `tabText(int index) const` | 获取 tab 标题。 | 标题可包含助记符标记。 |
| 修改 | `setTabText(int index, const QString &text)` | 设置 tab 标题。 | 长文本会受 `elideMode` 影响。 |
| 查询 | `tabTextColor(int index) const` | 获取 tab 文字颜色。 | 可用于表示未保存、警告等状态。 |
| 修改 | `setTabTextColor(int index, const QColor &color)` | 设置 tab 文字颜色。 | 不要用颜色替代无障碍状态表达。 |
| 查询 | `tabIcon(int index) const` | 获取 tab 图标。 | 返回值是图标对象的副本。 |
| 修改 | `setTabIcon(int index, const QIcon &icon)` | 设置 tab 图标。 | 常用于文档类型标识。 |
| 查询 | `elideMode() const` | 查询文字省略策略。 | 与长标题显示有关。 |
| 修改 | `setElideMode(Qt::TextElideMode mode)` | 设置文字省略策略。 | 常用 `Qt::ElideRight`。 |
| 修改 | `setTabToolTip(int index, const QString &tip)` | 设置 tab 工具提示。 | 长标题和状态说明很适合。 |
| 查询 | `tabToolTip(int index) const` | 获取 tab 工具提示。 | 依赖 tooltip 功能。 |
| 修改 | `setTabWhatsThis(int index, const QString &text)` | 设置 What's This 帮助文本。 | 需要启用相应功能。 |
| 查询 | `tabWhatsThis(int index) const` | 获取 What's This 文本。 | 用于上下文帮助。 |
| 修改 | `setTabData(int index, const QVariant &data)` | 给 tab 保存自定义数据。 | 适合存稳定业务 ID。 |
| 查询 | `tabData(int index) const` | 读取 tab 自定义数据。 | 不要用 index 代替它。 |
| 查询 | `tabRect(int index) const` | 获取 tab 的矩形区域。 | 自定义定位和命中测试常用。 |
| 查询 | `tabAt(const QPoint &pos) const` | 根据位置找 tab 索引。 | 鼠标交互和拖放常用。 |
| 查询 | `currentIndex() const` | 获取当前 tab 索引。 | 没有 tab 时通常为无效索引。 |
| 查询 | `count() const` | 获取 tab 数量。 | 用于边界检查。 |
| 查询 | `sizeHint() const` | 推荐控件尺寸。 | 布局系统会参考它。 |
| 查询 | `minimumSizeHint() const` | 推荐最小尺寸。 | 和滚动按钮、文字省略有关。 |
| 修改 | `setDrawBase(bool drawTheBase)` | 控制是否画基础线。 | 自定义界面时常调整。 |
| 查询 | `drawBase() const` | 查询基础线开关。 | 只反映当前配置。 |
| 查询 | `iconSize() const` | 获取图标尺寸。 | 影响所有 tab。 |
| 修改 | `setIconSize(const QSize &size)` | 设置图标尺寸。 | 过大可能挤压标题。 |
| 查询 | `usesScrollButtons() const` | 查询滚动按钮开关。 | tab 太多时很重要。 |
| 修改 | `setUsesScrollButtons(bool useButtons)` | 设置是否使用滚动按钮。 | 影响窄空间下的可用性。 |
| 查询 | `tabsClosable() const` | 查询是否显示关闭按钮。 | 不代表已经处理关闭逻辑。 |
| 修改 | `setTabsClosable(bool closable)` | 显示或隐藏关闭按钮。 | 配合 `tabCloseRequested`。 |
| 修改 | `setTabButton(int index, ButtonPosition position, QWidget *widget)` | 在 tab 一侧放置自定义控件。 | tab bar 接管传入 widget 的归属。 |
| 查询 | `tabButton(int index, ButtonPosition position) const` | 获取 tab 一侧的自定义控件。 | 没有按钮时返回空指针。 |
| 查询 | `selectionBehaviorOnRemove() const` | 查询删除后的选择策略。 | 影响编辑器式交互。 |
| 修改 | `setSelectionBehaviorOnRemove(SelectionBehavior behavior)` | 设置删除后的选择策略。 | 左、右或前一个 tab。 |
| 查询 | `expanding() const` | 查询是否扩展填充。 | 影响每个 tab 的宽度。 |
| 修改 | `setExpanding(bool enabled)` | 设置是否扩展填充。 | 适合导航型 tab。 |
| 查询 | `isMovable() const` | 查询是否可拖动。 | 只反映开关。 |
| 修改 | `setMovable(bool movable)` | 开启或关闭拖动重排。 | 顺序变化要监听 `tabMoved`。 |
| 查询 | `documentMode() const` | 查询文档模式。 | 主要影响样式。 |
| 修改 | `setDocumentMode(bool set)` | 开启或关闭文档模式。 | 文档编辑器常用。 |
| 查询 | `autoHide() const` | 查询是否自动隐藏。 | 只有 tab 数不足时才体现。 |
| 修改 | `setAutoHide(bool hide)` | 设置是否自动隐藏 tab bar。 | 适合可选导航。 |
| 查询 | `changeCurrentOnDrag() const` | 查询拖动经过 tab 是否切换当前项。 | 多文档拖动时有用。 |
| 修改 | `setChangeCurrentOnDrag(bool change)` | 设置拖动经过时是否切换。 | 影响拖动体验。 |
| 查询 | `accessibleTabName(int index) const` | 读取 tab 的无障碍名称。 | 需要启用 accessibility。 |
| 修改 | `setAccessibleTabName(int index, const QString &name)` | 设置 tab 的无障碍名称。 | 当可见标题不够清楚时使用。 |
| 槽 | `setCurrentIndex(int index)` | 设置当前 tab。 | 会触发 `currentChanged`。 |
| 信号 | `currentChanged(int index)` | 当前 tab 改变时发出。 | 连接页面切换逻辑。 |
| 信号 | `tabCloseRequested(int index)` | 用户请求关闭 tab。 | 需要业务层决定是否真正关闭。 |
| 信号 | `tabMoved(int from, int to)` | tab 被移动后发出。 | 同步文档顺序。 |
| 信号 | `tabBarClicked(int index)` | 用户点击 tab 时发出。 | 与当前变化信号不同，点击未选中的也会发。 |
| 信号 | `tabBarDoubleClicked(int index)` | 用户双击 tab 时发出。 | 可用于重命名或新建行为。 |
| 受保护函数 | `tabSizeHint(int index) const` | 返回指定 tab 的推荐尺寸。 | 自定义 tab 尺寸时重写。 |
| 受保护函数 | `minimumTabSizeHint(int index) const` | 返回指定 tab 的最小尺寸。 | 与压缩和滚动有关。 |
| 受保护函数 | `tabInserted(int index)` | 通知 tab 已插入。 | 派生类维护附加状态。 |
| 受保护函数 | `tabRemoved(int index)` | 通知 tab 已移除。 | 清理派生类数据。 |
| 受保护函数 | `tabLayoutChange()` | 通知 tab 布局变化。 | 自定义绘制或缓存时使用。 |
| 受保护函数 | `initStyleOption(QStyleOptionTab *option, int tabIndex) const` | 初始化某个 tab 的样式选项。 | 自定义绘制前先调用或参考它。 |
| 受保护函数 | `event(QEvent *)` | 处理通用事件。 | 影响 tab 交互。 |
| 受保护函数 | `resizeEvent(QResizeEvent *)` | 处理尺寸变化。 | 影响 tab 布局。 |
| 受保护函数 | `showEvent(QShowEvent *)` | 处理显示事件。 | 初始化可见状态。 |
| 受保护函数 | `hideEvent(QHideEvent *)` | 处理隐藏事件。 | 自动隐藏时可能触发。 |
| 受保护函数 | `paintEvent(QPaintEvent *)` | 绘制标签条。 | 自定义外观的底层入口。 |
| 受保护函数 | `mousePressEvent(QMouseEvent *)` | 处理鼠标按下。 | 点击、拖动和关闭按钮相关。 |
| 受保护函数 | `mouseMoveEvent(QMouseEvent *)` | 处理鼠标移动。 | 拖动重排相关。 |
| 受保护函数 | `mouseReleaseEvent(QMouseEvent *)` | 处理鼠标释放。 | 完成点击或拖动。 |
| 受保护函数 | `mouseDoubleClickEvent(QMouseEvent *)` | 处理双击。 | 触发双击信号。 |
| 受保护函数 | `wheelEvent(QWheelEvent *)` | 处理滚轮。 | 滚动 tab 列表。 |
| 受保护函数 | `keyPressEvent(QKeyEvent *)` | 处理键盘导航。 | 左右键、快捷操作会用到。 |
| 受保护函数 | `changeEvent(QEvent *)` | 处理样式等变化。 | 语言、字体、样式更新相关。 |
| 受保护函数 | `timerEvent(QTimerEvent *)` | 处理内部定时事件。 | 通常不需要业务层重写。 |

### 一句话总结

`QTabBar` 是标签导航条，不是页面容器；它负责 tab 的索引、外观和交互，页面切换与页面生命周期必须由外部对象管理。
