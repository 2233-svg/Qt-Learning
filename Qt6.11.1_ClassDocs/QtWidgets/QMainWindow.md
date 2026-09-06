# QMainWindow

> Qt 6.11.1 · Qt Widgets

## 1. 先建立直觉

**一句话定位：** `QMainWindow` 是桌面应用主窗口框架，集中管理中央控件、菜单栏、工具栏、状态栏和停靠窗口。

**模块背景：** Qt Widgets 提供传统桌面应用的控件、布局、模型/视图、窗口和交互组件。

### 这是什么

`QMainWindow` 是桌面应用主窗口框架，集中管理中央控件、菜单栏、工具栏、状态栏和停靠窗口。

**内部模型：** QMainWindow 有自己的特殊布局，中央区域只能通过 setCentralWidget 设置；工具栏和停靠窗口不是普通 layout 子项。把内容控件、命令 QAction 和窗口框架分开设计，后续扩展更稳定。

**适用场景：** 有菜单、工具栏、状态栏、多个编辑区或可停靠面板的桌面应用使用；只有一个简单控件的窗口可以直接用 QWidget。

**典型调用链：** 构造主窗口 -> 创建 QAction -> addMenu/addToolBar -> setCentralWidget -> addDockWidget -> statusBar()->showMessage -> saveState/restoreState。

**先记住的坑：** 不要给 QMainWindow 直接 setLayout；中央控件只能有一个；saveState/restoreState 要配合稳定的 objectName；工具栏和 dock 的所有权通常由主窗口接管。

## 2. 依赖与对象关系

- 头文件：`#include <QMainWindow>`
- 继承自：QWidget
- 直接派生类：未在类页中列出

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Widgets)
target_link_libraries(mytarget PRIVATE Qt6::Widgets)
```

**继承带来的规则：** 它属于 QObject 对象模型（直接或间接继承 QObject），因此父对象、信号与槽、事件循环和线程归属是使用主线。

### 工作机制

QMainWindow 有自己的特殊布局，中央区域只能通过 setCentralWidget 设置；工具栏和停靠窗口不是普通 layout 子项。把内容控件、命令 QAction 和窗口框架分开设计，后续扩展更稳定。

### 状态、生命周期和线程

**生命周期：** 控件有 parent 时通常由父控件管理销毁；顶层窗口可以放在栈上，也可以由应用对象或业务对象持有。隐藏控件仍然存在，关闭窗口也不一定等于删除对象或退出应用，必须明确 `WA_DeleteOnClose`、parent 和应用退出策略。

**状态与结果：** 控件状态由属性、焦点、启用/禁用、可见性、选择状态和模型数据共同决定。改变属性可能触发重新布局或重绘；需要刷新界面时通常调用 `update()`，需要重新计算几何时让布局系统处理，不要直接调用 `paintEvent()`。

**线程与事件循环：** 所有 QWidget 的创建、访问、布局和绘制都应在 GUI 线程完成。后台线程通过信号把结果投递回来；不要从 worker 线程直接修改控件，也不要在 GUI 线程用 `waitFor...` 或长循环阻塞事件循环。

## 3. 直接使用

有菜单、工具栏、状态栏、多个编辑区或可停靠面板的桌面应用使用；只有一个简单控件的窗口可以直接用 QWidget。 使用时通常按这个过程组织：构造主窗口 -> 创建 QAction -> addMenu/addToolBar -> setCentralWidget -> addDockWidget -> statusBar()->showMessage -> saveState/restoreState。

```cpp
#include <QApplication>
#include <QLabel>
#include <QMainWindow>

int main(int argc, char *argv[])
{
    QApplication app(argc, argv);
    QMainWindow window;
    window.setWindowTitle(QStringLiteral("Main Window"));
    window.setCentralWidget(new QLabel(QStringLiteral("Content"), &window));
    window.show();
    return app.exec();
}
```
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 公有类型

- `enum DockOption { AnimatedDocks, AllowNestedDocks, AllowTabbedDocks, ForceTabbedDocks, VerticalTabs, GroupedDragging }`
- `flags DockOptions`

### 属性

- `animated : bool`
- `dockNestingEnabled : bool`
- `dockOptions : DockOptions`
- `documentMode : bool`
- `iconSize : QSize`
- `tabShape : QTabWidget::TabShape`
- `toolButtonStyle : Qt::ToolButtonStyle`
- `unifiedTitleAndToolBarOnMac : bool`

### 公有函数

- `QMainWindow(QWidget *parent = nullptr, Qt::WindowFlags flags = Qt::WindowFlags())`
- `virtual ~QMainWindow()`
- `void addDockWidget(Qt::DockWidgetArea area, QDockWidget *dockwidget)`
- `void addDockWidget(Qt::DockWidgetArea area, QDockWidget *dockwidget, Qt::Orientation orientation)`
- `void addToolBar(Qt::ToolBarArea area, QToolBar *toolbar)`
- `void addToolBar(QToolBar *toolbar)`
- `QToolBar * addToolBar(const QString &title)`
- `void addToolBarBreak(Qt::ToolBarArea area = Qt::TopToolBarArea)`
- `QWidget * centralWidget() const`
- `Qt::DockWidgetArea corner(Qt::Corner corner) const`
- `virtual QMenu * createPopupMenu()`
- `QMainWindow::DockOptions dockOptions() const`
- `Qt::DockWidgetArea dockWidgetArea(QDockWidget *dockwidget) const`
- `bool documentMode() const`
- `QSize iconSize() const`
- `void insertToolBar(QToolBar *before, QToolBar *toolbar)`
- `void insertToolBarBreak(QToolBar *before)`
- `bool isAnimated() const`
- `bool isDockNestingEnabled() const`
- `QMenuBar * menuBar() const`
- `QWidget * menuWidget() const`
- `void removeDockWidget(QDockWidget *dockwidget)`
- `void removeToolBar(QToolBar *toolbar)`
- `void removeToolBarBreak(QToolBar *before)`
- `void resizeDocks(const QList<QDockWidget *> &docks, const QList<int> &sizes, Qt::Orientation orientation)`
- `bool restoreDockWidget(QDockWidget *dockwidget)`
- `bool restoreState(const QByteArray &state, int version = 0)`
- `QByteArray saveState(int version = 0) const`
- `void setCentralWidget(QWidget *widget)`
- `void setCorner(Qt::Corner corner, Qt::DockWidgetArea area)`
- `void setDockOptions(QMainWindow::DockOptions options)`
- `void setDocumentMode(bool enabled)`
- `void setIconSize(const QSize &iconSize)`
- `void setMenuBar(QMenuBar *menuBar)`
- `void setMenuWidget(QWidget *menuBar)`
- `void setStatusBar(QStatusBar *statusbar)`
- `void setTabPosition(Qt::DockWidgetAreas areas, QTabWidget::TabPosition tabPosition)`
- `void setTabShape(QTabWidget::TabShape tabShape)`
- `void setToolButtonStyle(Qt::ToolButtonStyle toolButtonStyle)`
- `void splitDockWidget(QDockWidget *first, QDockWidget *second, Qt::Orientation orientation)`
- `QStatusBar * statusBar() const`
- `QTabWidget::TabPosition tabPosition(Qt::DockWidgetArea area) const`
- `QTabWidget::TabShape tabShape() const`
- `QList<QDockWidget *> tabifiedDockWidgets(QDockWidget *dockwidget) const`
- `void tabifyDockWidget(QDockWidget *first, QDockWidget *second)`
- `QWidget * takeCentralWidget()`
- `Qt::ToolBarArea toolBarArea(const QToolBar *toolbar) const`
- `bool toolBarBreak(QToolBar *toolbar) const`
- `Qt::ToolButtonStyle toolButtonStyle() const`
- `bool unifiedTitleAndToolBarOnMac() const`

### 公有槽函数

- `void setAnimated(bool enabled)`
- `void setDockNestingEnabled(bool enabled)`
- `void setUnifiedTitleAndToolBarOnMac(bool set)`

### 信号

- `void iconSizeChanged(const QSize &iconSize)`
- `void tabifiedDockWidgetActivated(QDockWidget *dockWidget)`
- `void toolButtonStyleChanged(Qt::ToolButtonStyle toolButtonStyle)`

### 重实现的保护函数

- `virtual void contextMenuEvent(QContextMenuEvent *event) override`
- `virtual bool event(QEvent *event) override`

## 5. API 逐个说明

这里直接说明每个公开成员解决什么问题、参数代表什么、返回什么、会改变什么以及使用时容易出现什么问题。每一个公开签名都会有对应的中文解释。

本类共整理 69 个公开成员条目；没有独立长描述的 API 也会根据签名、类型和所属机制给出使用说明。

### `enum QMainWindow::DockOptionflags QMainWindow::DockOptions`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QMainWindow` 暴露的类型声明 `Dock、Optionflags`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 属性类型：`:DockOptionflags QMainWindow::DockOptions`。
- 属性名：`QMainWindow`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `animated : bool`

**API 类别：** 属性说明

**中文解读：** 这是 `QMainWindow` 的配置属性。初始化或状态切换时通过 `setAnimated(...)` 设置，之后用 `animated()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`bool`。
- 属性名：`animated`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `dockNestingEnabled : bool`

**API 类别：** 属性说明

**中文解读：** 这是 `QMainWindow` 的配置属性。初始化或状态切换时通过 `setDockNestingEnabled(...)` 设置，之后用 `dockNestingEnabled()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`bool`。
- 属性名：`dockNestingEnabled`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `dockOptions : DockOptions`

**API 类别：** 属性说明

**中文解读：** 这是 `QMainWindow` 的配置属性。初始化或状态切换时通过 `setDockOptions(...)` 设置，之后用 `dockOptions()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`DockOptions`。
- 属性名：`dockOptions`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `documentMode : bool`

**API 类别：** 属性说明

**中文解读：** 这是 `QMainWindow` 的配置属性。初始化或状态切换时通过 `setDocumentMode(...)` 设置，之后用 `documentMode()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`bool`。
- 属性名：`documentMode`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `iconSize : QSize`

**API 类别：** 属性说明

**中文解读：** 这是 `QMainWindow` 的配置属性。初始化或状态切换时通过 `setIconSize(...)` 设置，之后用 `iconSize()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`QSize`。
- 属性名：`iconSize`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `tabShape : QTabWidget::TabShape`

**API 类别：** 属性说明

**中文解读：** 这是 `QMainWindow` 的配置属性。初始化或状态切换时通过 `setTabShape(...)` 设置，之后用 `TabShape()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`QTabWidget::TabShape`。
- 属性名：`tabShape`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `toolButtonStyle : Qt::ToolButtonStyle`

**API 类别：** 属性说明

**中文解读：** 这是 `QMainWindow` 的配置属性。初始化或状态切换时通过 `setToolButtonStyle(...)` 设置，之后用 `ToolButtonStyle()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`Qt::ToolButtonStyle`。
- 属性名：`toolButtonStyle`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `unifiedTitleAndToolBarOnMac : bool`

**API 类别：** 属性说明

**中文解读：** 这是 `QMainWindow` 的配置属性。初始化或状态切换时通过 `setUnifiedTitleAndToolBarOnMac(...)` 设置，之后用 `unifiedTitleAndToolBarOnMac()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`bool`。
- 属性名：`unifiedTitleAndToolBarOnMac`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[explicit] QMainWindow::QMainWindow(QWidget *parent = nullptr, Qt::WindowFlags flags = Qt::WindowFlags())`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QMainWindow` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `parent`：类型为 `QWidget *`。默认值为 `nullptr`。父对象。设置后通常由父对象负责销毁子对象；只有在对象确实应挂入这棵对象树时才传入。
- 参数 `flags`：类型为 `Qt::WindowFlags`。默认值为 `Qt::WindowFlags()`。标志位组合。可以用按位或组合，调用前确认哪些标志互斥、哪些标志需要同时出现。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual noexcept] QMainWindow::~QMainWindow()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QMainWindow` 的析构函数。对象销毁时资源、子对象和连接会按 Qt 规则释放；异步对象要先停止任务或使用 deleteLater，避免回调访问已经不存在的实例。

**签名拆解：**

- 返回值：析构函数，无返回值。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QMainWindow::addDockWidget(Qt::DockWidgetArea area, QDockWidget *dockwidget)`

**API 类别：** 成员函数说明

**中文解读：** 这是向 `QMainWindow` 添加依赖、数据或子对象的 API `addDockWidget`。注意对象所有权、重复添加和添加后的通知；如果对应有 remove/take 接口，要明确谁负责移除后的生命周期。

**签名拆解：**

- 返回值：`void`。
- 参数 `area`：类型为 `Qt::DockWidgetArea`。没有默认值，调用时必须提供。传入 `Qt::DockWidgetArea` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `dockwidget`：类型为 `QDockWidget *`。没有默认值，调用时必须提供。传入 `QDockWidget *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QMainWindow::addDockWidget(Qt::DockWidgetArea area, QDockWidget *dockwidget, Qt::Orientation orientation)`

**API 类别：** 成员函数说明

**中文解读：** 这是向 `QMainWindow` 添加依赖、数据或子对象的 API `addDockWidget`。注意对象所有权、重复添加和添加后的通知；如果对应有 remove/take 接口，要明确谁负责移除后的生命周期。

**签名拆解：**

- 返回值：`void`。
- 参数 `area`：类型为 `Qt::DockWidgetArea`。没有默认值，调用时必须提供。传入 `Qt::DockWidgetArea` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `dockwidget`：类型为 `QDockWidget *`。没有默认值，调用时必须提供。传入 `QDockWidget *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `orientation`：类型为 `Qt::Orientation`。没有默认值，调用时必须提供。传入 `Qt::Orientation` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QMainWindow::addToolBar(Qt::ToolBarArea area, QToolBar *toolbar)`

**API 类别：** 成员函数说明

**中文解读：** 这是向 `QMainWindow` 添加依赖、数据或子对象的 API `addToolBar`。注意对象所有权、重复添加和添加后的通知；如果对应有 remove/take 接口，要明确谁负责移除后的生命周期。

**签名拆解：**

- 返回值：`void`。
- 参数 `area`：类型为 `Qt::ToolBarArea`。没有默认值，调用时必须提供。传入 `Qt::ToolBarArea` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `toolbar`：类型为 `QToolBar *`。没有默认值，调用时必须提供。传入 `QToolBar *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QMainWindow::addToolBar(QToolBar *toolbar)`

**API 类别：** 成员函数说明

**中文解读：** 这是向 `QMainWindow` 添加依赖、数据或子对象的 API `addToolBar`。注意对象所有权、重复添加和添加后的通知；如果对应有 remove/take 接口，要明确谁负责移除后的生命周期。

**签名拆解：**

- 返回值：`void`。
- 参数 `toolbar`：类型为 `QToolBar *`。没有默认值，调用时必须提供。传入 `QToolBar *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QToolBar *QMainWindow::addToolBar(const QString &title)`

**API 类别：** 成员函数说明

**中文解读：** 这是向 `QMainWindow` 添加依赖、数据或子对象的 API `addToolBar`。注意对象所有权、重复添加和添加后的通知；如果对应有 remove/take 接口，要明确谁负责移除后的生命周期。

**签名拆解：**

- 返回值：`QToolBar *`。
- 参数 `title`：类型为 `const QString &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QMainWindow::addToolBarBreak(Qt::ToolBarArea area = Qt::TopToolBarArea)`

**API 类别：** 成员函数说明

**中文解读：** 这是向 `QMainWindow` 添加依赖、数据或子对象的 API `addToolBarBreak`。注意对象所有权、重复添加和添加后的通知；如果对应有 remove/take 接口，要明确谁负责移除后的生命周期。

**签名拆解：**

- 返回值：`void`。
- 参数 `area`：类型为 `Qt::ToolBarArea`。默认值为 `Qt::TopToolBarArea`。传入 `Qt::ToolBarArea` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QWidget *QMainWindow::centralWidget() const`

**API 类别：** 成员函数说明

**中文解读：** `QMainWindow::centralWidget` 用于计算、查询或取得与“central、Widget”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QWidget *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QWidget *`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual protected] void QMainWindow::contextMenuEvent(QContextMenuEvent *event)`

**API 类别：** 成员函数说明

**中文解读：** `QMainWindow::contextMenuEvent` 用于执行与“context、Menu、Event”相关的操作。调用时要先确认当前状态和 `event` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `event`：类型为 `QContextMenuEvent *`。没有默认值，调用时必须提供。事件对象。通常只在事件处理函数执行期间有效，应读取类型和字段后决定 accept/ignore，不能长期保存指针。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `Qt::DockWidgetArea QMainWindow::corner(Qt::Corner corner) const`

**API 类别：** 成员函数说明

**中文解读：** `QMainWindow::corner` 用于计算、查询或取得与“corner”相关的操作。调用时要先确认当前状态和 `corner` 的有效范围；返回类型是 `Qt::DockWidgetArea`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`Qt::DockWidgetArea`。
- 参数 `corner`：类型为 `Qt::Corner`。没有默认值，调用时必须提供。传入 `Qt::Corner` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual] QMenu *QMainWindow::createPopupMenu()`

**API 类别：** 成员函数说明

**中文解读：** `QMainWindow::createPopupMenu` 用于计算、查询或取得与“创建、Popup、Menu”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QMenu *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QMenu *`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `Qt::DockWidgetArea QMainWindow::dockWidgetArea(QDockWidget *dockwidget) const`

**API 类别：** 成员函数说明

**中文解读：** `QMainWindow::dockWidgetArea` 用于计算、查询或取得与“dock、Widget、Area”相关的操作。调用时要先确认当前状态和 `dockwidget` 的有效范围；返回类型是 `Qt::DockWidgetArea`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`Qt::DockWidgetArea`。
- 参数 `dockwidget`：类型为 `QDockWidget *`。没有默认值，调用时必须提供。传入 `QDockWidget *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual protected] bool QMainWindow::event(QEvent *event)`

**API 类别：** 成员函数说明

**中文解读：** `QMainWindow::event` 用于计算、查询或取得与“event”相关的操作。调用时要先确认当前状态和 `event` 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数 `event`：类型为 `QEvent *`。没有默认值，调用时必须提供。事件对象。通常只在事件处理函数执行期间有效，应读取类型和字段后决定 accept/ignore，不能长期保存指针。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[signal] void QMainWindow::iconSizeChanged(const QSize &iconSize)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QMainWindow` 发出的通知信号 `iconSizeChanged`。应用代码通常只连接它，不直接调用它；信号参数描述发生了什么，槽函数中读取相关状态并尽快返回。异步类的完成、错误和状态变化通常都从信号开始处理。

**签名拆解：**

- 返回值：`void`。
- 参数 `iconSize`：类型为 `const QSize &`。没有默认值，调用时必须提供。传入 `const QSize &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QMainWindow::insertToolBar(QToolBar *before, QToolBar *toolbar)`

**API 类别：** 成员函数说明

**中文解读：** 这是向 `QMainWindow` 添加依赖、数据或子对象的 API `insertToolBar`。注意对象所有权、重复添加和添加后的通知；如果对应有 remove/take 接口，要明确谁负责移除后的生命周期。

**签名拆解：**

- 返回值：`void`。
- 参数 `before`：类型为 `QToolBar *`。没有默认值，调用时必须提供。传入 `QToolBar *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `toolbar`：类型为 `QToolBar *`。没有默认值，调用时必须提供。传入 `QToolBar *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QMainWindow::insertToolBarBreak(QToolBar *before)`

**API 类别：** 成员函数说明

**中文解读：** 这是向 `QMainWindow` 添加依赖、数据或子对象的 API `insertToolBarBreak`。注意对象所有权、重复添加和添加后的通知；如果对应有 remove/take 接口，要明确谁负责移除后的生命周期。

**签名拆解：**

- 返回值：`void`。
- 参数 `before`：类型为 `QToolBar *`。没有默认值，调用时必须提供。传入 `QToolBar *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QMenuBar *QMainWindow::menuBar() const`

**API 类别：** 成员函数说明

**中文解读：** `QMainWindow::menuBar` 用于计算、查询或取得与“menu、Bar”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QMenuBar *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QMenuBar *`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QWidget *QMainWindow::menuWidget() const`

**API 类别：** 成员函数说明

**中文解读：** `QMainWindow::menuWidget` 用于计算、查询或取得与“menu、Widget”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QWidget *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QWidget *`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QMainWindow::removeDockWidget(QDockWidget *dockwidget)`

**API 类别：** 成员函数说明

**中文解读：** 这是结束/释放/取消 API `removeDockWidget`。它会改变对象状态或资源所有权，调用后不要继续使用已经失效的句柄、reply、索引或设备，并确认异步完成信号是否仍会到达。

**签名拆解：**

- 返回值：`void`。
- 参数 `dockwidget`：类型为 `QDockWidget *`。没有默认值，调用时必须提供。传入 `QDockWidget *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QMainWindow::removeToolBar(QToolBar *toolbar)`

**API 类别：** 成员函数说明

**中文解读：** 这是结束/释放/取消 API `removeToolBar`。它会改变对象状态或资源所有权，调用后不要继续使用已经失效的句柄、reply、索引或设备，并确认异步完成信号是否仍会到达。

**签名拆解：**

- 返回值：`void`。
- 参数 `toolbar`：类型为 `QToolBar *`。没有默认值，调用时必须提供。传入 `QToolBar *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QMainWindow::removeToolBarBreak(QToolBar *before)`

**API 类别：** 成员函数说明

**中文解读：** 这是结束/释放/取消 API `removeToolBarBreak`。它会改变对象状态或资源所有权，调用后不要继续使用已经失效的句柄、reply、索引或设备，并确认异步完成信号是否仍会到达。

**签名拆解：**

- 返回值：`void`。
- 参数 `before`：类型为 `QToolBar *`。没有默认值，调用时必须提供。传入 `QToolBar *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QMainWindow::resizeDocks(const QList<QDockWidget *> &docks, const QList<int> &sizes, Qt::Orientation orientation)`

**API 类别：** 成员函数说明

**中文解读：** `QMainWindow::resizeDocks` 用于执行与“调整尺寸、Docks”相关的操作。调用时要先确认当前状态和 `docks`、`sizes`、`orientation` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `docks`：类型为 `const QList<QDockWidget *> &`。没有默认值，调用时必须提供。传入 `const QList<QDockWidget *> &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `sizes`：类型为 `const QList<int> &`。没有默认值，调用时必须提供。传入 `const QList<int> &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `orientation`：类型为 `Qt::Orientation`。没有默认值，调用时必须提供。传入 `Qt::Orientation` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QMainWindow::restoreDockWidget(QDockWidget *dockwidget)`

**API 类别：** 成员函数说明

**中文解读：** `QMainWindow::restoreDockWidget` 用于计算、查询或取得与“恢复、Dock、Widget”相关的操作。调用时要先确认当前状态和 `dockwidget` 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数 `dockwidget`：类型为 `QDockWidget *`。没有默认值，调用时必须提供。传入 `QDockWidget *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QMainWindow::restoreState(const QByteArray &state, int version = 0)`

**API 类别：** 成员函数说明

**中文解读：** `QMainWindow::restoreState` 用于计算、查询或取得与“恢复、State”相关的操作。调用时要先确认当前状态和 `state`、`version` 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数 `state`：类型为 `const QByteArray &`。没有默认值，调用时必须提供。状态值或状态对象；它描述调用时的阶段，不能把某个状态下有效的 API 用到其他阶段。
- 参数 `version`：类型为 `int`。默认值为 `0`。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QByteArray QMainWindow::saveState(int version = 0) const`

**API 类别：** 成员函数说明

**中文解读：** `QMainWindow::saveState` 用于计算、查询或取得与“保存、State”相关的操作。调用时要先确认当前状态和 `version` 的有效范围；返回类型是 `QByteArray`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QByteArray`。
- 参数 `version`：类型为 `int`。默认值为 `0`。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QMainWindow::setCentralWidget(QWidget *widget)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setCentralWidget`。调用它会改变 `QMainWindow` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `widget`：类型为 `QWidget *`。没有默认值，调用时必须提供。参与操作的 QWidget。要确认它是否为空、是否已被其他布局/容器管理，以及函数是否只查找直接子项。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QMainWindow::setCorner(Qt::Corner corner, Qt::DockWidgetArea area)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setCorner`。调用它会改变 `QMainWindow` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `corner`：类型为 `Qt::Corner`。没有默认值，调用时必须提供。传入 `Qt::Corner` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `area`：类型为 `Qt::DockWidgetArea`。没有默认值，调用时必须提供。传入 `Qt::DockWidgetArea` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QMainWindow::setMenuBar(QMenuBar *menuBar)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setMenuBar`。调用它会改变 `QMainWindow` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `menuBar`：类型为 `QMenuBar *`。没有默认值，调用时必须提供。传入 `QMenuBar *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QMainWindow::setMenuWidget(QWidget *menuBar)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setMenuWidget`。调用它会改变 `QMainWindow` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `menuBar`：类型为 `QWidget *`。没有默认值，调用时必须提供。Qt 对象参数。要确认对象有效、线程归属、所有权和该 API 是否只处理直接子对象。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QMainWindow::setStatusBar(QStatusBar *statusbar)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setStatusBar`。调用它会改变 `QMainWindow` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `statusbar`：类型为 `QStatusBar *`。没有默认值，调用时必须提供。传入 `QStatusBar *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QMainWindow::setTabPosition(Qt::DockWidgetAreas areas, QTabWidget::TabPosition tabPosition)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setTabPosition`。调用它会改变 `QMainWindow` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `areas`：类型为 `Qt::DockWidgetAreas`。没有默认值，调用时必须提供。传入 `Qt::DockWidgetAreas` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `tabPosition`：类型为 `QTabWidget::TabPosition`。没有默认值，调用时必须提供。传入 `QTabWidget::TabPosition` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QMainWindow::splitDockWidget(QDockWidget *first, QDockWidget *second, Qt::Orientation orientation)`

**API 类别：** 成员函数说明

**中文解读：** `QMainWindow::splitDockWidget` 用于执行与“split、Dock、Widget”相关的操作。调用时要先确认当前状态和 `first`、`second`、`orientation` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `first`：类型为 `QDockWidget *`。没有默认值，调用时必须提供。传入 `QDockWidget *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `second`：类型为 `QDockWidget *`。没有默认值，调用时必须提供。传入 `QDockWidget *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `orientation`：类型为 `Qt::Orientation`。没有默认值，调用时必须提供。传入 `Qt::Orientation` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QStatusBar *QMainWindow::statusBar() const`

**API 类别：** 成员函数说明

**中文解读：** `QMainWindow::statusBar` 用于计算、查询或取得与“状态、Bar”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QStatusBar *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QStatusBar *`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QTabWidget::TabPosition QMainWindow::tabPosition(Qt::DockWidgetArea area) const`

**API 类别：** 成员函数说明

**中文解读：** `QMainWindow::tabPosition` 用于计算、查询或取得与“tab、Position”相关的操作。调用时要先确认当前状态和 `area` 的有效范围；返回类型是 `QTabWidget::TabPosition`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QTabWidget::TabPosition`。
- 参数 `area`：类型为 `Qt::DockWidgetArea`。没有默认值，调用时必须提供。传入 `Qt::DockWidgetArea` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[signal] void QMainWindow::tabifiedDockWidgetActivated(QDockWidget *dockWidget)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QMainWindow` 发出的通知信号 `tabifiedDockWidgetActivated`。应用代码通常只连接它，不直接调用它；信号参数描述发生了什么，槽函数中读取相关状态并尽快返回。异步类的完成、错误和状态变化通常都从信号开始处理。

**签名拆解：**

- 返回值：`void`。
- 参数 `dockWidget`：类型为 `QDockWidget *`。没有默认值，调用时必须提供。传入 `QDockWidget *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QList<QDockWidget *> QMainWindow::tabifiedDockWidgets(QDockWidget *dockwidget) const`

**API 类别：** 成员函数说明

**中文解读：** `QMainWindow::tabifiedDockWidgets` 用于计算、查询或取得与“tabified、Dock、Widgets”相关的操作。调用时要先确认当前状态和 `dockwidget` 的有效范围；返回类型是 `QList<QDockWidget *>`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QList<QDockWidget *>`。
- 参数 `dockwidget`：类型为 `QDockWidget *`。没有默认值，调用时必须提供。传入 `QDockWidget *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QMainWindow::tabifyDockWidget(QDockWidget *first, QDockWidget *second)`

**API 类别：** 成员函数说明

**中文解读：** `QMainWindow::tabifyDockWidget` 用于执行与“tabify、Dock、Widget”相关的操作。调用时要先确认当前状态和 `first`、`second` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `first`：类型为 `QDockWidget *`。没有默认值，调用时必须提供。传入 `QDockWidget *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `second`：类型为 `QDockWidget *`。没有默认值，调用时必须提供。传入 `QDockWidget *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QWidget *QMainWindow::takeCentralWidget()`

**API 类别：** 成员函数说明

**中文解读：** `QMainWindow::takeCentralWidget` 用于计算、查询或取得与“取出、Central、Widget”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QWidget *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QWidget *`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `Qt::ToolBarArea QMainWindow::toolBarArea(const QToolBar *toolbar) const`

**API 类别：** 成员函数说明

**中文解读：** 这是转换/映射 API `toolBarArea`。它通常在不同表示、坐标系、编码或 Qt 类型之间建立边界；转换前确认格式和所有权，转换后检查是否丢失精度、编码或上下文。

**签名拆解：**

- 返回值：`Qt::ToolBarArea`。
- 参数 `toolbar`：类型为 `const QToolBar *`。没有默认值，调用时必须提供。传入 `const QToolBar *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QMainWindow::toolBarBreak(QToolBar *toolbar) const`

**API 类别：** 成员函数说明

**中文解读：** 这是转换/映射 API `toolBarBreak`。它通常在不同表示、坐标系、编码或 Qt 类型之间建立边界；转换前确认格式和所有权，转换后检查是否丢失精度、编码或上下文。

**签名拆解：**

- 返回值：`bool`。
- 参数 `toolbar`：类型为 `QToolBar *`。没有默认值，调用时必须提供。传入 `QToolBar *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[signal] void QMainWindow::toolButtonStyleChanged(Qt::ToolButtonStyle toolButtonStyle)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QMainWindow` 发出的通知信号 `toolButtonStyleChanged`。应用代码通常只连接它，不直接调用它；信号参数描述发生了什么，槽函数中读取相关状态并尽快返回。异步类的完成、错误和状态变化通常都从信号开始处理。

**签名拆解：**

- 返回值：`void`。
- 参数 `toolButtonStyle`：类型为 `Qt::ToolButtonStyle`。没有默认值，调用时必须提供。传入 `Qt::ToolButtonStyle` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `enum DockOption { AnimatedDocks, AllowNestedDocks, AllowTabbedDocks, ForceTabbedDocks, VerticalTabs, GroupedDragging }`

**API 类别：** 公有类型

**中文解读：** 这是 `QMainWindow` 暴露的类型声明 `Dock、Option`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 这是供该类其他 API 使用的枚举/标志类型；传值前要确认枚举值的语义和适用状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `flags DockOptions`

**API 类别：** 公有类型

**中文解读：** 这是 `QMainWindow` 的 `标志` 成员声明。它通常作为其他 API 的类型、常量或配置入口使用；先确认可用值和适用状态，再结合本类的创建、核心操作和清理流程使用。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QMainWindow::DockOptions dockOptions() const`

**API 类别：** 公有函数

**中文解读：** `QMainWindow::dockOptions` 用于计算、查询或取得与“dock、Options”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QMainWindow::DockOptions`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QMainWindow::DockOptions`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool documentMode() const`

**API 类别：** 公有函数

**中文解读：** `QMainWindow::documentMode` 用于计算、查询或取得与“document、模式”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QSize iconSize() const`

**API 类别：** 公有函数

**中文解读：** `QMainWindow::iconSize` 用于计算、查询或取得与“icon、尺寸或数量”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QSize`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QSize`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool isAnimated() const`

**API 类别：** 公有函数

**中文解读：** 这是查询 API `isAnimated`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool isDockNestingEnabled() const`

**API 类别：** 公有函数

**中文解读：** 这是查询 API `isDockNestingEnabled`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void setDockOptions(QMainWindow::DockOptions options)`

**API 类别：** 公有函数

**中文解读：** 这是配置/写入操作 `setDockOptions`。调用它会改变 `QMainWindow` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `options`：类型为 `QMainWindow::DockOptions`。没有默认值，调用时必须提供。传入 `QMainWindow::DockOptions` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void setDocumentMode(bool enabled)`

**API 类别：** 公有函数

**中文解读：** 这是配置/写入操作 `setDocumentMode`。调用它会改变 `QMainWindow` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `enabled`：类型为 `bool`。没有默认值，调用时必须提供。传入 `bool` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void setIconSize(const QSize &iconSize)`

**API 类别：** 公有函数

**中文解读：** 这是配置/写入操作 `setIconSize`。调用它会改变 `QMainWindow` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `iconSize`：类型为 `const QSize &`。没有默认值，调用时必须提供。传入 `const QSize &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void setTabShape(QTabWidget::TabShape tabShape)`

**API 类别：** 公有函数

**中文解读：** 这是配置/写入操作 `setTabShape`。调用它会改变 `QMainWindow` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `tabShape`：类型为 `QTabWidget::TabShape`。没有默认值，调用时必须提供。传入 `QTabWidget::TabShape` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void setToolButtonStyle(Qt::ToolButtonStyle toolButtonStyle)`

**API 类别：** 公有函数

**中文解读：** 这是配置/写入操作 `setToolButtonStyle`。调用它会改变 `QMainWindow` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `toolButtonStyle`：类型为 `Qt::ToolButtonStyle`。没有默认值，调用时必须提供。传入 `Qt::ToolButtonStyle` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QTabWidget::TabShape tabShape() const`

**API 类别：** 公有函数

**中文解读：** `QMainWindow::tabShape` 用于计算、查询或取得与“tab、Shape”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QTabWidget::TabShape`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QTabWidget::TabShape`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `Qt::ToolButtonStyle toolButtonStyle() const`

**API 类别：** 公有函数

**中文解读：** 这是转换/映射 API `toolButtonStyle`。它通常在不同表示、坐标系、编码或 Qt 类型之间建立边界；转换前确认格式和所有权，转换后检查是否丢失精度、编码或上下文。

**签名拆解：**

- 返回值：`Qt::ToolButtonStyle`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool unifiedTitleAndToolBarOnMac() const`

**API 类别：** 公有函数

**中文解读：** `QMainWindow::unifiedTitleAndToolBarOnMac` 用于计算、查询或取得与“unified、Title、And、Tool、Bar、On、Mac”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void setAnimated(bool enabled)`

**API 类别：** 公有槽函数

**中文解读：** 这是可被信号连接或元对象调用的槽 `setAnimated`。它适合作为一次动作或状态响应的入口；如果调用可能耗时，不要直接阻塞 GUI 事件循环，应把工作拆分或移动到 worker。

**签名拆解：**

- 返回值：`void`。
- 参数 `enabled`：类型为 `bool`。没有默认值，调用时必须提供。传入 `bool` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void setDockNestingEnabled(bool enabled)`

**API 类别：** 公有槽函数

**中文解读：** 这是可被信号连接或元对象调用的槽 `setDockNestingEnabled`。它适合作为一次动作或状态响应的入口；如果调用可能耗时，不要直接阻塞 GUI 事件循环，应把工作拆分或移动到 worker。

**签名拆解：**

- 返回值：`void`。
- 参数 `enabled`：类型为 `bool`。没有默认值，调用时必须提供。传入 `bool` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void setUnifiedTitleAndToolBarOnMac(bool set)`

**API 类别：** 公有槽函数

**中文解读：** 这是可被信号连接或元对象调用的槽 `setUnifiedTitleAndToolBarOnMac`。它适合作为一次动作或状态响应的入口；如果调用可能耗时，不要直接阻塞 GUI 事件循环，应把工作拆分或移动到 worker。

**签名拆解：**

- 返回值：`void`。
- 参数 `set`：类型为 `bool`。没有默认值，调用时必须提供。传入 `bool` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

## 6. 深入实践与常见坑

### 生命周期和资源边界

控件有 parent 时通常由父控件管理销毁；顶层窗口可以放在栈上，也可以由应用对象或业务对象持有。隐藏控件仍然存在，关闭窗口也不一定等于删除对象或退出应用，必须明确 `WA_DeleteOnClose`、parent 和应用退出策略。

### 状态和错误边界

控件状态由属性、焦点、启用/禁用、可见性、选择状态和模型数据共同决定。改变属性可能触发重新布局或重绘；需要刷新界面时通常调用 `update()`，需要重新计算几何时让布局系统处理，不要直接调用 `paintEvent()`。

### 线程边界

所有 QWidget 的创建、访问、布局和绘制都应在 GUI 线程完成。后台线程通过信号把结果投递回来；不要从 worker 线程直接修改控件，也不要在 GUI 线程用 `waitFor...` 或长循环阻塞事件循环。

### 最容易出现的错误

不要给 QMainWindow 直接 setLayout；中央控件只能有一个；saveState/restoreState 要配合稳定的 objectName；工具栏和 dock 的所有权通常由主窗口接管。

### 版本和平台

本文档以 Qt 6.11.1 为依据。涉及平台后端、编解码器、数据库驱动、窗口风格、编译器特性或标注了版本号的 API 时，要把版本条件当作使用约束，而不是只看函数是否能补全。

## 7. 使用边界

`QMainWindow` 所属机制类型：Qt Widgets 界面机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
