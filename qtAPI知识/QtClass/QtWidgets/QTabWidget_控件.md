# Qt QTabWidget 深入笔记

> 适用版本：Qt 6 Widgets（本文按 Qt 6.11.1 API 整理）  
> 头文件：`#include <QTabWidget>`  
> 所属模块：`Qt6::Widgets`  
> 继承：`QWidget -> QTabWidget`  
> 常见搭档：`QTabBar`、`QStackedWidget`、`QStackedLayout`

## 1. QTabWidget 解决什么问题

`QTabWidget` 用“标签页 + 页面区域”管理多个相关页面，同一时间只显示当前页面。它适合把一个复杂窗口拆成几个用户可以切换的功能区。

典型场景：

- 设置对话框：常规、外观、网络、快捷键；
- 编辑器：多个文档页；
- 数据工具：数据、结构、日志；
- 设备配置：基本参数、高级参数、诊断。

它内部主要由两个对象协作：

```text
QTabWidget
├─ QTabBar          顶部/底部/左右的标签入口
└─ QStackedWidget   页面堆叠区，同一时间显示一个 page
```

`QTabWidget` 负责把这两部分接起来。大多数时候直接使用 `QTabWidget` 即可；只有需要完全自定义标签导航时，才考虑单独使用 `QStackedWidget` 或 `QStackedLayout`。

## 2. 最小可用代码

```cpp
#include <QLabel>
#include <QTabWidget>
#include <QVBoxLayout>
#include <QWidget>

auto *tabs = new QTabWidget;

auto *generalPage = new QWidget;
auto *generalLayout = new QVBoxLayout(generalPage);
generalLayout->addWidget(new QLabel(tr("General settings")));

auto *networkPage = new QWidget;
auto *networkLayout = new QVBoxLayout(networkPage);
networkLayout->addWidget(new QLabel(tr("Network settings")));

tabs->addTab(generalPage, tr("&General"));
tabs->addTab(networkPage, tr("&Network"));
tabs->resize(500, 300);
tabs->show();
```

标签文本中的 `&` 可以创建键盘助记符，例如 `&General` 通常对应 `Alt+G`。

## 3. page 的创建和所有权

推荐先创建没有 parent 的 page，在 page 内部完成布局，再交给 `QTabWidget`：

```cpp
auto *page = new QWidget;
auto *layout = new QFormLayout(page);
layout->addRow(tr("Name:"), new QLineEdit);

int index = tabs->addTab(page, tr("User"));
```

调用 `addTab()` 或 `insertTab()` 后，page 的所有权转给 `QTabWidget`。页面不是标签本身，而是标签背后的真实 `QWidget`。

`QTabWidget` 只显示当前 page，其余 page 会被隐藏。切换标签时，当前 page 会改变，`currentChanged(int)` 会发出。

## 4. 添加、插入、切换和查询

### 4.1 添加和插入

```cpp
int last = tabs->addTab(page, tr("Last"));
int index = tabs->insertTab(0, page, tr("First"));
```

`addTab()` 总是追加，`insertTab()` 在指定索引插入。索引越界时，`insertTab()` 会追加到末尾并返回实际索引。

如果 tab widget 原来为空，新 page 会成为当前页面。向当前索引之前插入页面时，当前索引可能增加，但当前 page 保持不变。

### 4.2 切换页面

```cpp
tabs->setCurrentIndex(1);
tabs->setCurrentWidget(networkPage);

int index = tabs->currentIndex();
QWidget *page = tabs->currentWidget();
```

`setCurrentWidget()` 要求传入的 widget 已经是该 tab widget 中的 page；传入其他 widget 不会成为合法页面。

### 4.3 查询页面

```cpp
QWidget *page = tabs->widget(index);
int index = tabs->indexOf(page);
int total = tabs->count();
```

无效索引返回 `nullptr` 或 `-1`，具体取决于函数。

## 5. 修改 tab 的文字、图标和提示

```cpp
tabs->setTabText(index, tr("Advanced"));
tabs->setTabIcon(index, QIcon(":/icons/settings.svg"));
tabs->setTabToolTip(index, tr("Advanced settings"));
tabs->setTabWhatsThis(index, tr("Configure advanced options"));
```

读取对应信息：

```cpp
QString text = tabs->tabText(index);
QIcon icon = tabs->tabIcon(index);
QString tip = tabs->tabToolTip(index);
QString help = tabs->tabWhatsThis(index);
```

`setTabText()` 中的 `&` 会建立或替换该 tab 的快捷键；如果需要显示真实的 `&`，使用 `&&`。

图标尺寸由 `iconSize` 控制，但它是最大尺寸，图标不会被强行放大到比自身更大：

```cpp
tabs->setIconSize(QSize(20, 20));
```

## 6. 启用、隐藏和关闭 tab

### 6.1 禁用 tab

```cpp
tabs->setTabEnabled(index, false);
```

禁用后，标签会呈现禁用样式，用户不能通过点击选择它。但 page 仍然可能是当前可见页面；禁用 tab 不等于自动隐藏 page。

### 6.2 隐藏 tab

```cpp
tabs->setTabVisible(index, false);
```

隐藏 tab 入口和禁用 tab 是两件事：隐藏后用户看不到标签，但页面对象仍然保留在 tab widget 中。

### 6.3 添加关闭按钮

```cpp
tabs->setTabsClosable(true);
connect(tabs, &QTabWidget::tabCloseRequested,
        tabs, [tabs](int index) {
            QWidget *page = tabs->widget(index);
            tabs->removeTab(index);
            page->deleteLater();
        });
```

`setTabsClosable(true)` 只是让 tab bar 显示关闭按钮。点击后 `tabCloseRequested(index)` 发信号，`QTabWidget` 不会替你删除 page。

## 7. removeTab 和 clear 的所有权陷阱

```cpp
QWidget *page = tabs->widget(index);
tabs->removeTab(index);
page->deleteLater();
```

`removeTab(index)` 只从 tab stack 中移除标签，page 本身不会被删除。  
`clear()` 等价于重复移除所有 tab，同样不会删除页面。

如果想把页面移出后继续使用，可以重新设置 parent 或交给另一个容器；如果不再使用，就明确调用 `deleteLater()`。

不要把下面两个概念混在一起：

- tab 被移除：标签入口和页面关联关系消失；
- page 被删除：页面对象及其子控件释放。

## 8. 标签位置、形状和显示方式

### 8.1 标签位置

```cpp
tabs->setTabPosition(QTabWidget::North);
```

可选位置：

| 枚举 | 含义 |
| --- | --- |
| `North` | 页面上方，默认位置。 |
| `South` | 页面下方。 |
| `West` | 页面左侧。 |
| `East` | 页面右侧。 |

### 8.2 标签形状

```cpp
tabs->setTabShape(QTabWidget::Rounded);
```

- `Rounded`：圆角风格，默认；
- `Triangular`：三角风格。

最终外观仍会受到当前 `QStyle` 影响。

### 8.3 文本省略和滚动按钮

```cpp
tabs->setElideMode(Qt::ElideRight);
tabs->setUsesScrollButtons(true);
```

当 tab 很多、空间不足时：

- `elideMode` 决定标签文字如何省略；
- `usesScrollButtons` 决定 tab bar 是否使用左右滚动按钮。

这两个属性通常根据平台 style 有默认值。固定写死前，先确认你的 UI 是否真的需要统一表现。

## 9. documentMode、movable 和自动隐藏

### 9.1 documentMode

```cpp
tabs->setDocumentMode(true);
```

`documentMode` 让标签栏更像文档编辑器的页面标签，通常会减少传统 tab widget 的边框感。它是外观语义，不会改变页面切换逻辑。

### 9.2 movable

```cpp
tabs->setMovable(true);
```

启用后，用户可以在 tab bar 内拖动标签改变顺序。它不会自动把标签拖到另一个 `QTabWidget` 中；如果需要跨控件拖放，要另外实现拖放逻辑。

### 9.3 tabBarAutoHide

```cpp
tabs->setTabBarAutoHide(true);
```

启用后，当 tab 数少于 2 个时，标签栏自动隐藏。适合“平时像单页，打开第二个页面后才显示标签”的文档界面。

## 10. cornerWidget 和内部 QTabBar

```cpp
auto *extraButton = new QPushButton(tr("Options"));
tabs->setCornerWidget(extraButton, Qt::TopRightCorner);
```

角落控件适合放添加按钮、设置按钮或页面操作入口。它主要适合 `North` / `South` 标签位置；标签在左右侧时，角落控件的表现可能不符合预期。

`setCornerWidget(nullptr, corner)` 可以不再显示角落控件。之前设置的角落控件会被隐藏；若不重新设置 parent，通常由 tab widget 在销毁时负责清理。

需要直接控制标签行为时，可以取到底层 `QTabBar`：

```cpp
QTabBar *bar = tabs->tabBar();
bar->setExpanding(false);
```

如果要替换 tab bar，必须在添加任何 tab 之前调用受保护的 `setTabBar()`；之后再替换会导致未定义行为。

## API 速查表
### 11.1 类型、构造和页面管理

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 类型 | `TabPosition` | 定义标签栏位于页面上、下、左还是右。 | 具体绘制仍受当前 `QStyle` 影响。 |
| 枚举值 | `North` / `South` / `West` / `East` | 分别表示上、下、左、右四种标签位置。 | 默认是 `North`；左右标签下 corner widget 的布局要单独测试。 |
| 类型 | `TabShape` | 定义标签页外形类别。 | 只描述形状，不保证不同平台的像素外观完全一致。 |
| 枚举值 | `Rounded` / `Triangular` | 分别表示圆角和三角形标签。 | `Rounded` 是常见默认值。 |
| 构造 | `QTabWidget(QWidget *parent = nullptr)` | 创建标签页控件及其内部标签栏、页面堆叠区。 | 大多数场景直接使用它，不必自己拼 `QTabBar + QStackedWidget`。 |
| 析构 | `~QTabWidget()` | 销毁标签页控件。 | 仍由控件管理的 page 会随对象树清理。 |
| 添加页面 | `addTab(QWidget *widget, const QString &label)` | 在末尾追加一个带文字的页面，返回索引。 | 页面交给 `QTabWidget` 管理；移除 tab 后页面不会自动删除。 |
| 添加页面 | `addTab(QWidget *widget, const QIcon &icon, const QString &label)` | 在末尾追加带图标和文字的页面。 | 图标实际大小受 `iconSize` 和 style 影响。 |
| 插入页面 | `insertTab(int index, QWidget *widget, const QString &label)` | 在指定索引插入文字页面。 | 索引越界时会追加，返回实际索引。 |
| 插入页面 | `insertTab(int index, QWidget *widget, const QIcon &icon, const QString &label)` | 在指定索引插入带图标页面。 | 插入当前页之前可能改变当前索引，但当前 page 通常保持不变。 |
| 移除页面 | `removeTab(int index)` | 移除 tab 与 page 的关联。 | 不删除 page；不再使用时要自行 `deleteLater()` 或交给其他容器。 |
| 清空 | `clear()` | 移除所有 tab。 | 同样不会替你删除被移除的 page。 |

### 11.2 当前页面和索引

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 查询 | `count() const` | 返回当前 tab/page 数量。 | 没有页面时为 0。 |
| 当前页 | `currentIndex() const` / `setCurrentIndex(int index)` | 读取或按索引切换当前页面。 | 无页面时通常为 -1；切换会发出 `currentChanged`。 |
| 当前页 | `currentWidget() const` | 返回当前正在显示的 page。 | 没有当前页时返回空指针。 |
| 当前页 | `setCurrentWidget(QWidget *widget)` | 按 page 指针切换当前页面。 | 传入的 widget 必须已经属于本 tab widget。 |
| 页面查询 | `widget(int index) const` | 按索引取得 page。 | 无效索引返回空指针。 |
| 页面查询 | `indexOf(const QWidget *widget) const` | 查询某个 page 对应的 tab 索引。 | 找不到返回 -1。 |

### 11.3 tab 内容和交互

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 标签文本 | `tabText(int index) const` / `setTabText(int index, const QString &text)` | 读取或设置 tab 标题。 | 文本中的 `&` 会创建键盘助记符，显示真实 `&` 要写成 `&&`。 |
| 标签图标 | `tabIcon(int index) const` / `setTabIcon(int index, const QIcon &icon)` | 读取或设置 tab 图标。 | 不会保证图标被放大到 `iconSize`，小图标仍可能保持原尺寸。 |
| 标签提示 | `tabToolTip(int index) const` / `setTabToolTip(int index, const QString &tip)` | 读取或设置鼠标悬停提示。 | 只适合补充说明，不要把关键操作写在 tooltip 里。 |
| What's This | `tabWhatsThis(int index) const` / `setTabWhatsThis(int index, const QString &text)` | 读取或设置帮助模式文本。 | 需要启用 Qt What's This 功能。 |
| 可用状态 | `isTabEnabled(int index) const` / `setTabEnabled(int index, bool enabled)` | 控制用户是否能选择某个 tab。 | 禁用不等于隐藏；当前页即使被禁用也不一定自动消失。 |
| 可见状态 | `isTabVisible(int index) const` / `setTabVisible(int index, bool visible)` | 控制 tab 入口是否显示。 | 隐藏只影响标签入口，page 仍然属于控件。 |
| 关闭入口 | `tabsClosable() const` / `setTabsClosable(bool closeable)` | 控制 tab bar 是否显示关闭按钮。 | 点击只发 `tabCloseRequested`，页面移除和销毁由业务负责。 |
| 拖动排序 | `isMovable() const` / `setMovable(bool movable)` | 控制用户是否能在当前 tab bar 内拖动排序。 | 不会自动支持跨 `QTabWidget` 拖放。 |

### 11.4 外观和布局属性

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 标签位置 | `tabPosition() const` / `setTabPosition(TabPosition position)` | 读取或设置标签栏位于页面哪一边。 | 左右标签时要重新检查页面宽度和 corner widget 的布局。 |
| 标签形状 | `tabShape() const` / `setTabShape(TabShape shape)` | 读取或设置标签绘制形状。 | 只选语义风格，具体视觉仍由 style 决定。 |
| 文本省略 | `elideMode() const` / `setElideMode(Qt::TextElideMode mode)` | 控制标题过长时从哪一侧省略。 | 多文档标签和窗口较窄时很有用。 |
| 图标尺寸 | `iconSize() const` / `setIconSize(const QSize &size)` | 读取或设置 tab 图标的最大尺寸。 | 是尺寸上限，不会强制放大过小图标。 |
| 滚动按钮 | `usesScrollButtons() const` / `setUsesScrollButtons(bool useButtons)` | 控制标签过多时是否显示滚动按钮。 | 默认通常由当前 style 决定。 |
| 文档外观 | `documentMode() const` / `setDocumentMode(bool set)` | 切换更接近文档编辑器的 tab 外观。 | 不改变页面切换和所有权逻辑。 |
| 自动隐藏 | `tabBarAutoHide() const` / `setTabBarAutoHide(bool enabled)` | 当 tab 少于两个时自动隐藏标签栏。 | 适合“单页时不显示 tab，多页时才出现”的界面。 |
| 角落控件 | `setCornerWidget(QWidget *widget, Qt::Corner corner = Qt::TopRightCorner)` | 在标签栏角落放置额外控件。 | 主要适合 North/South；控件所有权和隐藏行为要明确。 |
| 角落控件 | `cornerWidget(Qt::Corner corner = Qt::TopRightCorner) const` | 查询某个角落的控件。 | 没有时返回空指针。 |
| 底层标签栏 | `tabBar() const` | 返回内部 `QTabBar`。 | 适合做更细粒度的标签配置；替换 tab bar 要用受保护接口且必须提前完成。 |
| 尺寸 | `sizeHint() const` / `minimumSizeHint() const` | 返回推荐尺寸和最小推荐尺寸。 | 通常由布局调用，不要把返回值当成固定窗口尺寸。 |
| 尺寸协商 | `hasHeightForWidth() const` / `heightForWidth(int width) const` | 支持根据宽度推导高度。 | 主要由布局系统使用。 |

### 11.5 信号和扩展点

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 信号 | `currentChanged(int index)` | 当前页面发生变化时通知。 | 清空或移除页面后 `index` 可能为 -1。 |
| 信号 | `tabCloseRequested(int index)` | 用户点击 tab 关闭按钮时通知。 | 槽函数里要自行 `removeTab()`，并决定是否销毁 page。 |
| 信号 | `tabBarClicked(int index)` | 用户点击标签栏时通知。 | 点击空白区域时 index 可能为 -1。 |
| 信号 | `tabBarDoubleClicked(int index)` | 用户双击标签栏时通知。 | 可用于重命名、创建新页或弹出操作菜单。 |
| 扩展点 | `tabInserted(int index)` | 页面插入完成后调用的虚函数。 | 派生类维护额外 tab 元数据时重写。 |
| 扩展点 | `tabRemoved(int index)` | 页面移除完成后调用的虚函数。 | 适合清理和 tab 关联的业务状态。 |
| 扩展点 | `setTabBar(QTabBar *tabBar)` | 替换内部标签栏。 | 受保护函数，必须在添加任何 tab 之前调用。 |
| 样式 | `initStyleOption(QStyleOptionTabWidgetFrame *option) const` | 填充 tab widget 框架绘制所需状态。 | 自定义绘制时调用，避免漏掉当前页、边框等状态。 |
| 事件 | `showEvent(QShowEvent *event)` | 处理控件首次显示和显示相关布局。 | 重写时通常要调用基类。 |
| 事件 | `resizeEvent(QResizeEvent *event)` | 在尺寸变化时调整标签栏与页面区域。 | 一般不需要重写，除非有特殊布局需求。 |
| 事件 | `keyPressEvent(QKeyEvent *event)` | 处理标签页键盘导航。 | 高级快捷键定制时重写。 |
| 绘制 | `paintEvent(QPaintEvent *event)` | 绘制 tab widget 框架和页面区域外观。 | 优先使用 `QStyle`，不要轻易覆盖整套绘制。 |
| 事件 | `changeEvent(QEvent *event)` | 响应字体、样式、语言等变化。 | 主题或翻译运行时切换时会用到。 |
| 事件 | `event(QEvent *event)` | tab widget 的统一事件入口。 | 只在确实需要处理特殊事件时重写。 |

## 12. 常见误区

### 12.1 removeTab 后页面不见了就以为被删除

`removeTab()` 只解除 tab 关系，不删除 page。不要把它和 `delete` 混为一谈。

### 12.2 tabsClosable 会自动关闭页面

它只显示关闭按钮并发出 `tabCloseRequested`。页面的移除和释放必须由你的槽函数负责。

### 12.3 禁用 tab 等于隐藏页面

禁用 tab 会阻止用户选择，但已经可见的 page 可能继续显示。需要隐藏入口用 `setTabVisible()`，需要隐藏页面则处理 page 的可见性。

### 12.4 页面直接用 QTabWidget 当 parent 创建

这样会让页面先成为 tab widget 的普通子控件，再由内部堆叠管理，容易让所有权和布局关系变得不清楚。更稳妥的方式是先创建 page、设置内部布局，再调用 `addTab()`。

### 12.5 添加 tab 后再替换 QTabBar

`setTabBar()` 必须在添加任何页面之前调用。已经建立 tab 后再换 tab bar，行为未定义。

---

### 一句话总结

`QTabWidget` 把多个 QWidget 页面组织成可切换的标签页：用 `addTab/insertTab` 接管页面，用 `currentIndex/currentWidget` 切换，用 `setTabEnabled/setTabVisible` 控制入口状态，用 `tabCloseRequested` 自己实现关闭和页面销毁。
