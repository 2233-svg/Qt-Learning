# QTabWidget

> Qt 6.11.1 · Qt Widgets · 来自 `QTabWidget`

## 1. 先建立直觉

### 这是什么

`QTabWidget` 是带标签栏的多页面容器。它把一个 `QTabBar` 和一个页面区域组合起来：用户点击标签切换页面，程序通过索引或页面指针管理每一页。

如果 `QStackedWidget` 是“无导航页面栈”，`QTabWidget` 就是“自带标签导航的页面栈”。它适合用户需要随时看到并切换多个并列页面的场景。

### 适合使用的场景

- 设置对话框的多个分类页。
- 编辑器或文档多标签页。
- 属性面板中少量并列页面。
- 需要可关闭、可移动、带图标或 tooltip 的标签页。

### 不适合的场景

- 流程式下一步/上一步页面，用 `QWizard` 或 `QStackedWidget` 加导航。
- 页面数量很多且需要树状分类，用侧边导航 + `QStackedWidget`。
- 页面只是局部折叠内容，不必上升到 tab。

## 2. 依赖与对象关系

- 头文件：`#include <QTabWidget>`
- 模块：Qt Widgets
- CMake：`find_package(Qt6 REQUIRED COMPONENTS Widgets)`，并链接 `Qt6::Widgets`
- 继承自：`QWidget`
- 直接派生类：类页未列出

`QTabWidget` 内部有 `QTabBar` 和页面栈。加入的 page 会成为 tab widget 管理的页面；`removeTab()` 只移除页面，不自动删除页面对象。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `enum TabPosition` | 标签栏位置：上、下、左、右。 |
| `enum TabShape` | 标签形状：圆角或三角。 |
| `count : int` | 标签页数量。 |
| `currentIndex : int` | 当前页索引。 |
| `documentMode : bool` | 文档式标签外观。 |
| `elideMode : Qt::TextElideMode` | 标签文本过长时省略方式。 |
| `iconSize : QSize` | 标签图标尺寸。 |
| `movable : bool` | 用户是否可拖动重排标签。 |
| `tabBarAutoHide : bool` | 少于两个标签时是否自动隐藏标签栏。 |
| `tabPosition : TabPosition` | 标签栏方位。 |
| `tabShape : TabShape` | 标签形状。 |
| `tabsClosable : bool` | 是否显示关闭按钮。 |
| `usesScrollButtons : bool` | 标签过多时是否使用滚动按钮。 |
| `addTab()` / `insertTab()` | 添加或插入页面，可带图标。 |
| `removeTab(int)` / `clear()` | 移除单页或清空所有页。 |
| `widget(int)` / `currentWidget()` / `indexOf()` | 页面索引和指针转换。 |
| `setCurrentIndex()` / `setCurrentWidget()` | 切换当前页。 |
| `setTabText()` / `tabText()` | 设置或读取标签文本。 |
| `setTabIcon()` / `tabIcon()` | 设置或读取标签图标。 |
| `setTabToolTip()` / `tabToolTip()` | 设置或读取标签 tooltip。 |
| `setTabWhatsThis()` / `tabWhatsThis()` | 设置或读取 What’s This 帮助。 |
| `setTabEnabled()` / `isTabEnabled()` | 启用或禁用标签页。 |
| `setTabVisible()` / `isTabVisible()` | 显示或隐藏标签页。 |
| `setCornerWidget()` / `cornerWidget()` | 在标签栏角落放额外控件。 |
| `tabBar()` / `setTabBar()` | 访问或替换底层 `QTabBar`。 |
| `currentChanged(int)` | 当前页变化时发出。 |
| `tabBarClicked(int)` / `tabBarDoubleClicked(int)` | 标签被点击/双击时发出。 |
| `tabCloseRequested(int)` | 用户请求关闭标签时发出。 |
| `tabInserted(int)` / `tabRemoved(int)` | 子类钩子：标签插入/移除。 |
| `sizeHint()` / `minimumSizeHint()` / `heightForWidth()` | 布局尺寸计算。 |
| `initStyleOption(QStyleOptionTabWidgetFrame *)` | 为绘制 frame 准备 style option。 |

## 4. API 逐项说明

### `TabPosition` / `tabPosition`

标签栏可放在北、南、西、东四侧。顶部标签最常见，左侧标签适合分类多但页面标题较短的设置面板。

侧边标签会受到平台 style 和文字方向影响，长文本可读性不一定好。

### `TabShape` / `tabShape`

控制标签外观是圆角还是三角。现代平台通常由 style 决定整体观感。

除非产品视觉明确要求，否则保持默认最稳。

### `count` / `currentIndex`

页面数量和当前索引。无页面时当前索引通常为 `-1`。

索引会随着插入、移除、移动变化。长期业务逻辑不要只保存 index，最好保存页面指针或文档 id。

### `documentMode`

启用文档模式后，标签外观更像文档编辑器标签，具体效果取决于平台 style。

多文档界面、编辑器类应用可以考虑；普通设置页通常不需要。

### `elideMode` / `iconSize`

标签文本过长时用 `elideMode` 控制省略方式；`iconSize` 控制标签图标尺寸。

标签标题要短。靠省略模式处理很长标题，只是兜底，不是主要设计。

### `movable`

允许用户拖动重排标签。适合文档标签页，不适合固定设置页。

标签可移动时，业务层不要假设第 0 页永远是某个功能。用页面指针或 id 做映射。

### `tabBarAutoHide`

标签数少于两个时自动隐藏标签栏。适合文档界面：只有一个文档时减少视觉噪声。

设置页不一定适合自动隐藏，因为标签栏本身也提供页面类别提示。

### `tabsClosable`

显示关闭按钮。点击关闭按钮只发出 `tabCloseRequested(int)`，不会自动关闭或删除页面。

这很重要：你必须在槽里决定是否允许关闭、保存未保存内容、调用 `removeTab()`，以及是否删除页面。

### `usesScrollButtons`

标签太多放不下时，是否显示滚动按钮。另一种方式是让标签省略或多行，但平台支持和观感不同。

若标签经常很多，可能需要重新考虑导航结构。

### `addTab()` / `insertTab()`

添加或插入页面，返回页面索引。可以只有文本，也可以图标加文本。

如果在已显示后大量添加标签，为减少闪烁，可先暂停更新或批量构建后再显示。

### `removeTab()` / `clear()`

移除标签页。移除不等于删除页面对象；页面对象仍需你决定复用或销毁。

关闭文档页时通常流程是：确认保存 -> `removeTab(index)` -> `page->deleteLater()`。

### 页面查询与切换

`widget(index)` 取页面，`currentWidget()` 取当前页，`indexOf(widget)` 查索引。`setCurrentIndex()` 和 `setCurrentWidget()` 切换页面。

切换页面不会自动刷新数据。需要激活逻辑时连接 `currentChanged()`。

### 标签元数据

`setTabText()`、`setTabIcon()`、`setTabToolTip()`、`setTabWhatsThis()` 管理每个标签显示和帮助信息。

tooltip 适合放完整路径或被省略的长标题；WhatsThis 适合解释复杂页面用途。

### 启用与可见性

`setTabEnabled()` 禁用标签页，用户不能进入但仍看得见；`setTabVisible()` 隐藏标签页。

禁用适合“当前条件下不可用但存在”；隐藏适合“当前模式完全不相关”。

### 角落控件

`setCornerWidget()` 可在标签栏角落放按钮或小工具，例如新建标签、设置菜单。角落受 tab position 和 style 影响。

不要在角落塞复杂表单，它只适合轻量操作。

### `tabBar()` / `setTabBar()`

访问或替换底层 `QTabBar`。替换 tab bar 要在添加标签前做，避免状态迁移复杂。

需要更深层的标签交互，例如自定义关闭按钮、拖放、上下文菜单，可以直接操作 `QTabBar`。

### 信号

`currentChanged()` 响应页面切换；`tabBarClicked()` 和 `tabBarDoubleClicked()` 响应标签交互；`tabCloseRequested()` 表示用户请求关闭。

关闭信号只是请求，不是动作完成。槽里必须明确处理。

### 绘制、尺寸和子类钩子

`initStyleOption()`、`paintEvent()`、`resizeEvent()`、`showEvent()` 管理外观和布局；`tabInserted()`、`tabRemoved()` 是子类扩展点。

普通业务不需要重写；先尝试通过属性、tab bar 和样式完成需求。

## 5. 深入实践与常见坑

### removeTab 不删除页面

这是最常见坑。移除后如果页面不再需要，调用 `deleteLater()`。

### 关闭按钮只发请求

`tabsClosable` 只是显示关闭按钮。真正关闭、保存确认、删除页面，都要在 `tabCloseRequested()` 槽里写。

### 固定功能页不要 movable

设置页、属性页这类固定结构不适合让用户重排。文档页、编辑器页才适合 movable。

### 页面多到滚动时，要考虑换导航

标签页适合少量并列页面。过多标签会让发现和切换都变差，侧边栏或文档列表可能更好。
