# QAbstractScrollArea

> Qt 6.11.1 · Qt Widgets

## 1. 先建立直觉

**一句话定位：** `QAbstractScrollArea` 是 Qt Widgets 界面机制 中的类型，负责把这一机制中的数据、状态或资源交给其他 Qt 对象使用。

**模块背景：** Qt Widgets 提供传统桌面应用的控件、布局、模型/视图、窗口和交互组件。

### 这是什么

`QAbstractScrollArea` 是 Qt Widgets 中的抽象协议类型，通常通过具体子类、模型、插件或工厂来使用。

**内部模型：** 抽象类的核心不是直接创建对象，而是理解它规定的虚函数、状态和通知协议。阅读时先列出必须实现的纯虚函数，再看框架何时调用它们。

**适用场景：** 当 Qt 的现成子类不能满足需求，需要自定义数据源、渲染器、处理器或插件时继承它。

**典型调用链：** 选择合适的具体抽象基类 -> 实现纯虚函数和必要通知 -> 交给 Qt 框架注册/绑定 -> 遵守生命周期和线程约束。

**先记住的坑：** 不要绕过 begin/end 或状态通知；纯虚函数返回值和调用线程要按文档约定；抽象对象通常不能直接实例化。

## 2. 依赖与对象关系

- 头文件：`#include <QAbstractScrollArea>`
- 继承自：QFrame
- 直接派生类：QAbstractItemView、QGraphicsView、QMdiArea、QPlainTextEdit、QScrollArea,、QTextEdit

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Widgets)
target_link_libraries(mytarget PRIVATE Qt6::Widgets)
```

**继承带来的规则：** 它属于 QObject 对象模型（直接或间接继承 QObject），因此父对象、信号与槽、事件循环和线程归属是使用主线。

### 工作机制

抽象类的核心不是直接创建对象，而是理解它规定的虚函数、状态和通知协议。阅读时先列出必须实现的纯虚函数，再看框架何时调用它们。

### 状态、生命周期和线程

**生命周期：** 控件有 parent 时通常由父控件管理销毁；顶层窗口可以放在栈上，也可以由应用对象或业务对象持有。隐藏控件仍然存在，关闭窗口也不一定等于删除对象或退出应用，必须明确 `WA_DeleteOnClose`、parent 和应用退出策略。

**状态与结果：** 控件状态由属性、焦点、启用/禁用、可见性、选择状态和模型数据共同决定。改变属性可能触发重新布局或重绘；需要刷新界面时通常调用 `update()`，需要重新计算几何时让布局系统处理，不要直接调用 `paintEvent()`。

**线程与事件循环：** 所有 QWidget 的创建、访问、布局和绘制都应在 GUI 线程完成。后台线程通过信号把结果投递回来；不要从 worker 线程直接修改控件，也不要在 GUI 线程用 `waitFor...` 或长循环阻塞事件循环。

## 3. 直接使用

当 Qt 的现成子类不能满足需求，需要自定义数据源、渲染器、处理器或插件时继承它。 使用时通常按这个过程组织：选择合适的具体抽象基类 -> 实现纯虚函数和必要通知 -> 交给 Qt 框架注册/绑定 -> 遵守生命周期和线程约束。
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 公有类型

- `enum SizeAdjustPolicy { AdjustIgnored, AdjustToContents, AdjustToContentsOnFirstShow }`

### 属性

- `horizontalScrollBarPolicy : Qt::ScrollBarPolicy`
- `sizeAdjustPolicy : SizeAdjustPolicy`
- `verticalScrollBarPolicy : Qt::ScrollBarPolicy`

### 公有函数

- `QAbstractScrollArea(QWidget *parent = nullptr)`
- `virtual ~QAbstractScrollArea()`
- `void addScrollBarWidget(QWidget *widget, Qt::Alignment alignment)`
- `QWidget * cornerWidget() const`
- `QScrollBar * horizontalScrollBar() const`
- `Qt::ScrollBarPolicy horizontalScrollBarPolicy() const`
- `QSize maximumViewportSize() const`
- `QWidgetList scrollBarWidgets(Qt::Alignment alignment)`
- `void setCornerWidget(QWidget *widget)`
- `void setHorizontalScrollBar(QScrollBar *scrollBar)`
- `void setHorizontalScrollBarPolicy(Qt::ScrollBarPolicy)`
- `void setSizeAdjustPolicy(QAbstractScrollArea::SizeAdjustPolicy policy)`
- `void setVerticalScrollBar(QScrollBar *scrollBar)`
- `void setVerticalScrollBarPolicy(Qt::ScrollBarPolicy)`
- `void setViewport(QWidget *widget)`
- `virtual void setupViewport(QWidget *viewport)`
- `QAbstractScrollArea::SizeAdjustPolicy sizeAdjustPolicy() const`
- `QScrollBar * verticalScrollBar() const`
- `Qt::ScrollBarPolicy verticalScrollBarPolicy() const`
- `QWidget * viewport() const`

### 重实现的公有函数

- `virtual QSize minimumSizeHint() const override`
- `virtual QSize sizeHint() const override`

### 保护函数

- `virtual void scrollContentsBy(int dx, int dy)`
- `void setViewportMargins(const QMargins &margins)`
- `void setViewportMargins(int left, int top, int right, int bottom)`
- `virtual bool viewportEvent(QEvent *event)`
- `QMargins viewportMargins() const`
- `virtual QSize viewportSizeHint() const`

### 重实现的保护函数

- `virtual void contextMenuEvent(QContextMenuEvent *e) override`
- `virtual void dragEnterEvent(QDragEnterEvent *event) override`
- `virtual void dragLeaveEvent(QDragLeaveEvent *event) override`
- `virtual void dragMoveEvent(QDragMoveEvent *event) override`
- `virtual void dropEvent(QDropEvent *event) override`
- `virtual bool event(QEvent *event) override`
- `virtual void keyPressEvent(QKeyEvent *e) override`
- `virtual void mouseDoubleClickEvent(QMouseEvent *e) override`
- `virtual void mouseMoveEvent(QMouseEvent *e) override`
- `virtual void mousePressEvent(QMouseEvent *e) override`
- `virtual void mouseReleaseEvent(QMouseEvent *e) override`
- `virtual void paintEvent(QPaintEvent *event) override`
- `virtual void resizeEvent(QResizeEvent *event) override`
- `virtual void wheelEvent(QWheelEvent *e) override`

## 5. API 逐个说明

这里直接说明每个公开成员解决什么问题、参数代表什么、返回什么、会改变什么以及使用时容易出现什么问题。每一个公开签名都会有对应的中文解释。

本类共整理 46 个公开成员条目；没有独立长描述的 API 也会根据签名、类型和所属机制给出使用说明。

### `enum QAbstractScrollArea::SizeAdjustPolicy`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QAbstractScrollArea` 暴露的类型声明 `尺寸或数量、Adjust、Policy`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 属性类型：`:SizeAdjustPolicy`。
- 属性名：`QAbstractScrollArea`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `horizontalScrollBarPolicy : Qt::ScrollBarPolicy`

**API 类别：** 属性说明

**中文解读：** 这是 `QAbstractScrollArea` 的配置属性。初始化或状态切换时通过 `setScrollBarPolicy(...)` 设置，之后用 `ScrollBarPolicy()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`Qt::ScrollBarPolicy`。
- 属性名：`horizontalScrollBarPolicy`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `sizeAdjustPolicy : SizeAdjustPolicy`

**API 类别：** 属性说明

**中文解读：** 这是 `QAbstractScrollArea` 的配置属性。初始化或状态切换时通过 `setSizeAdjustPolicy(...)` 设置，之后用 `sizeAdjustPolicy()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`SizeAdjustPolicy`。
- 属性名：`sizeAdjustPolicy`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `verticalScrollBarPolicy : Qt::ScrollBarPolicy`

**API 类别：** 属性说明

**中文解读：** 这是 `QAbstractScrollArea` 的配置属性。初始化或状态切换时通过 `setScrollBarPolicy(...)` 设置，之后用 `ScrollBarPolicy()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`Qt::ScrollBarPolicy`。
- 属性名：`verticalScrollBarPolicy`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[explicit] QAbstractScrollArea::QAbstractScrollArea(QWidget *parent = nullptr)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QAbstractScrollArea` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `parent`：类型为 `QWidget *`。默认值为 `nullptr`。父对象。设置后通常由父对象负责销毁子对象；只有在对象确实应挂入这棵对象树时才传入。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual noexcept] QAbstractScrollArea::~QAbstractScrollArea()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QAbstractScrollArea` 的析构函数。对象销毁时资源、子对象和连接会按 Qt 规则释放；异步对象要先停止任务或使用 deleteLater，避免回调访问已经不存在的实例。

**签名拆解：**

- 返回值：析构函数，无返回值。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QAbstractScrollArea::addScrollBarWidget(QWidget *widget, Qt::Alignment alignment)`

**API 类别：** 成员函数说明

**中文解读：** 这是向 `QAbstractScrollArea` 添加依赖、数据或子对象的 API `addScrollBarWidget`。注意对象所有权、重复添加和添加后的通知；如果对应有 remove/take 接口，要明确谁负责移除后的生命周期。

**签名拆解：**

- 返回值：`void`。
- 参数 `widget`：类型为 `QWidget *`。没有默认值，调用时必须提供。参与操作的 QWidget。要确认它是否为空、是否已被其他布局/容器管理，以及函数是否只查找直接子项。
- 参数 `alignment`：类型为 `Qt::Alignment`。没有默认值，调用时必须提供。对齐标志的组合，例如 `Qt::AlignLeft | Qt::AlignVCenter`；它描述内容在已分配区域中的位置，不负责分配剩余空间。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual protected] void QAbstractScrollArea::contextMenuEvent(QContextMenuEvent *e)`

**API 类别：** 成员函数说明

**中文解读：** `QAbstractScrollArea::contextMenuEvent` 用于执行与“context、Menu、Event”相关的操作。调用时要先确认当前状态和 `e` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `e`：类型为 `QContextMenuEvent *`。没有默认值，调用时必须提供。传入 `QContextMenuEvent *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QWidget *QAbstractScrollArea::cornerWidget() const`

**API 类别：** 成员函数说明

**中文解读：** `QAbstractScrollArea::cornerWidget` 用于计算、查询或取得与“corner、Widget”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QWidget *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QWidget *`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual protected] void QAbstractScrollArea::dragEnterEvent(QDragEnterEvent *event)`

**API 类别：** 成员函数说明

**中文解读：** `QAbstractScrollArea::dragEnterEvent` 用于执行与“drag、Enter、Event”相关的操作。调用时要先确认当前状态和 `event` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `event`：类型为 `QDragEnterEvent *`。没有默认值，调用时必须提供。事件对象。通常只在事件处理函数执行期间有效，应读取类型和字段后决定 accept/ignore，不能长期保存指针。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual protected] void QAbstractScrollArea::dragLeaveEvent(QDragLeaveEvent *event)`

**API 类别：** 成员函数说明

**中文解读：** `QAbstractScrollArea::dragLeaveEvent` 用于执行与“drag、Leave、Event”相关的操作。调用时要先确认当前状态和 `event` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `event`：类型为 `QDragLeaveEvent *`。没有默认值，调用时必须提供。事件对象。通常只在事件处理函数执行期间有效，应读取类型和字段后决定 accept/ignore，不能长期保存指针。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual protected] void QAbstractScrollArea::dragMoveEvent(QDragMoveEvent *event)`

**API 类别：** 成员函数说明

**中文解读：** `QAbstractScrollArea::dragMoveEvent` 用于执行与“drag、移动、Event”相关的操作。调用时要先确认当前状态和 `event` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `event`：类型为 `QDragMoveEvent *`。没有默认值，调用时必须提供。事件对象。通常只在事件处理函数执行期间有效，应读取类型和字段后决定 accept/ignore，不能长期保存指针。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual protected] void QAbstractScrollArea::dropEvent(QDropEvent *event)`

**API 类别：** 成员函数说明

**中文解读：** `QAbstractScrollArea::dropEvent` 用于执行与“drop、Event”相关的操作。调用时要先确认当前状态和 `event` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `event`：类型为 `QDropEvent *`。没有默认值，调用时必须提供。事件对象。通常只在事件处理函数执行期间有效，应读取类型和字段后决定 accept/ignore，不能长期保存指针。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual protected] bool QAbstractScrollArea::event(QEvent *event)`

**API 类别：** 成员函数说明

**中文解读：** `QAbstractScrollArea::event` 用于计算、查询或取得与“event”相关的操作。调用时要先确认当前状态和 `event` 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数 `event`：类型为 `QEvent *`。没有默认值，调用时必须提供。事件对象。通常只在事件处理函数执行期间有效，应读取类型和字段后决定 accept/ignore，不能长期保存指针。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QScrollBar *QAbstractScrollArea::horizontalScrollBar() const`

**API 类别：** 成员函数说明

**中文解读：** `QAbstractScrollArea::horizontalScrollBar` 用于计算、查询或取得与“水平、Scroll、Bar”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QScrollBar *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QScrollBar *`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual protected] void QAbstractScrollArea::keyPressEvent(QKeyEvent *e)`

**API 类别：** 成员函数说明

**中文解读：** `QAbstractScrollArea::keyPressEvent` 用于执行与“key、Press、Event”相关的操作。调用时要先确认当前状态和 `e` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `e`：类型为 `QKeyEvent *`。没有默认值，调用时必须提供。传入 `QKeyEvent *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QSize QAbstractScrollArea::maximumViewportSize() const`

**API 类别：** 成员函数说明

**中文解读：** `QAbstractScrollArea::maximumViewportSize` 用于计算、查询或取得与“最大值、Viewport、尺寸或数量”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QSize`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QSize`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual] QSize QAbstractScrollArea::minimumSizeHint() const`

**API 类别：** 成员函数说明

**中文解读：** `QAbstractScrollArea::minimumSizeHint` 用于计算、查询或取得与“最小值、尺寸或数量、Hint”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QSize`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QSize`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual protected] void QAbstractScrollArea::mouseDoubleClickEvent(QMouseEvent *e)`

**API 类别：** 成员函数说明

**中文解读：** `QAbstractScrollArea::mouseDoubleClickEvent` 用于执行与“mouse、Double、Click、Event”相关的操作。调用时要先确认当前状态和 `e` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `e`：类型为 `QMouseEvent *`。没有默认值，调用时必须提供。传入 `QMouseEvent *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual protected] void QAbstractScrollArea::mouseMoveEvent(QMouseEvent *e)`

**API 类别：** 成员函数说明

**中文解读：** `QAbstractScrollArea::mouseMoveEvent` 用于执行与“mouse、移动、Event”相关的操作。调用时要先确认当前状态和 `e` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `e`：类型为 `QMouseEvent *`。没有默认值，调用时必须提供。传入 `QMouseEvent *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual protected] void QAbstractScrollArea::mousePressEvent(QMouseEvent *e)`

**API 类别：** 成员函数说明

**中文解读：** `QAbstractScrollArea::mousePressEvent` 用于执行与“mouse、Press、Event”相关的操作。调用时要先确认当前状态和 `e` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `e`：类型为 `QMouseEvent *`。没有默认值，调用时必须提供。传入 `QMouseEvent *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual protected] void QAbstractScrollArea::mouseReleaseEvent(QMouseEvent *e)`

**API 类别：** 成员函数说明

**中文解读：** `QAbstractScrollArea::mouseReleaseEvent` 用于执行与“mouse、释放、Event”相关的操作。调用时要先确认当前状态和 `e` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `e`：类型为 `QMouseEvent *`。没有默认值，调用时必须提供。传入 `QMouseEvent *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual protected] void QAbstractScrollArea::paintEvent(QPaintEvent *event)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QAbstractScrollArea` 的核心操作 `paintEvent`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`void`。
- 参数 `event`：类型为 `QPaintEvent *`。没有默认值，调用时必须提供。事件对象。通常只在事件处理函数执行期间有效，应读取类型和字段后决定 accept/ignore，不能长期保存指针。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual protected] void QAbstractScrollArea::resizeEvent(QResizeEvent *event)`

**API 类别：** 成员函数说明

**中文解读：** `QAbstractScrollArea::resizeEvent` 用于执行与“调整尺寸、Event”相关的操作。调用时要先确认当前状态和 `event` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `event`：类型为 `QResizeEvent *`。没有默认值，调用时必须提供。事件对象。通常只在事件处理函数执行期间有效，应读取类型和字段后决定 accept/ignore，不能长期保存指针。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QWidgetList QAbstractScrollArea::scrollBarWidgets(Qt::Alignment alignment)`

**API 类别：** 成员函数说明

**中文解读：** `QAbstractScrollArea::scrollBarWidgets` 用于计算、查询或取得与“scroll、Bar、Widgets”相关的操作。调用时要先确认当前状态和 `alignment` 的有效范围；返回类型是 `QWidgetList`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QWidgetList`。
- 参数 `alignment`：类型为 `Qt::Alignment`。没有默认值，调用时必须提供。对齐标志的组合，例如 `Qt::AlignLeft | Qt::AlignVCenter`；它描述内容在已分配区域中的位置，不负责分配剩余空间。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual protected] void QAbstractScrollArea::scrollContentsBy(int dx, int dy)`

**API 类别：** 成员函数说明

**中文解读：** `QAbstractScrollArea::scrollContentsBy` 用于执行与“scroll、Contents、By”相关的操作。调用时要先确认当前状态和 `dx`、`dy` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `dx`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `dy`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QAbstractScrollArea::setCornerWidget(QWidget *widget)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setCornerWidget`。调用它会改变 `QAbstractScrollArea` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `widget`：类型为 `QWidget *`。没有默认值，调用时必须提供。参与操作的 QWidget。要确认它是否为空、是否已被其他布局/容器管理，以及函数是否只查找直接子项。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QAbstractScrollArea::setHorizontalScrollBar(QScrollBar *scrollBar)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setHorizontalScrollBar`。调用它会改变 `QAbstractScrollArea` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `scrollBar`：类型为 `QScrollBar *`。没有默认值，调用时必须提供。传入 `QScrollBar *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QAbstractScrollArea::setVerticalScrollBar(QScrollBar *scrollBar)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setVerticalScrollBar`。调用它会改变 `QAbstractScrollArea` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `scrollBar`：类型为 `QScrollBar *`。没有默认值，调用时必须提供。传入 `QScrollBar *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QAbstractScrollArea::setViewport(QWidget *widget)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setViewport`。调用它会改变 `QAbstractScrollArea` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `widget`：类型为 `QWidget *`。没有默认值，调用时必须提供。参与操作的 QWidget。要确认它是否为空、是否已被其他布局/容器管理，以及函数是否只查找直接子项。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[protected] void QAbstractScrollArea::setViewportMargins(const QMargins &margins)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setViewportMargins`。调用它会改变 `QAbstractScrollArea` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `margins`：类型为 `const QMargins &`。没有默认值，调用时必须提供。传入 `const QMargins &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[protected] void QAbstractScrollArea::setViewportMargins(int left, int top, int right, int bottom)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setViewportMargins`。调用它会改变 `QAbstractScrollArea` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `left`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `top`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `right`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `bottom`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual] void QAbstractScrollArea::setupViewport(QWidget *viewport)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setupViewport`。调用它会改变 `QAbstractScrollArea` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `viewport`：类型为 `QWidget *`。没有默认值，调用时必须提供。Qt 对象参数。要确认对象有效、线程归属、所有权和该 API 是否只处理直接子对象。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual] QSize QAbstractScrollArea::sizeHint() const`

**API 类别：** 成员函数说明

**中文解读：** `QAbstractScrollArea::sizeHint` 用于计算、查询或取得与“尺寸或数量、Hint”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QSize`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QSize`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QScrollBar *QAbstractScrollArea::verticalScrollBar() const`

**API 类别：** 成员函数说明

**中文解读：** `QAbstractScrollArea::verticalScrollBar` 用于计算、查询或取得与“垂直、Scroll、Bar”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QScrollBar *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QScrollBar *`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QWidget *QAbstractScrollArea::viewport() const`

**API 类别：** 成员函数说明

**中文解读：** `QAbstractScrollArea::viewport` 用于计算、查询或取得与“viewport”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QWidget *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QWidget *`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual protected] bool QAbstractScrollArea::viewportEvent(QEvent *event)`

**API 类别：** 成员函数说明

**中文解读：** `QAbstractScrollArea::viewportEvent` 用于计算、查询或取得与“viewport、Event”相关的操作。调用时要先确认当前状态和 `event` 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数 `event`：类型为 `QEvent *`。没有默认值，调用时必须提供。事件对象。通常只在事件处理函数执行期间有效，应读取类型和字段后决定 accept/ignore，不能长期保存指针。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[protected] QMargins QAbstractScrollArea::viewportMargins() const`

**API 类别：** 成员函数说明

**中文解读：** `QAbstractScrollArea::viewportMargins` 用于计算、查询或取得与“viewport、Margins”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QMargins`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QMargins`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual protected] QSize QAbstractScrollArea::viewportSizeHint() const`

**API 类别：** 成员函数说明

**中文解读：** `QAbstractScrollArea::viewportSizeHint` 用于计算、查询或取得与“viewport、尺寸或数量、Hint”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QSize`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QSize`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual protected] void QAbstractScrollArea::wheelEvent(QWheelEvent *e)`

**API 类别：** 成员函数说明

**中文解读：** `QAbstractScrollArea::wheelEvent` 用于执行与“wheel、Event”相关的操作。调用时要先确认当前状态和 `e` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `e`：类型为 `QWheelEvent *`。没有默认值，调用时必须提供。传入 `QWheelEvent *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `Qt::ScrollBarPolicy horizontalScrollBarPolicy() const`

**API 类别：** 公有函数

**中文解读：** `QAbstractScrollArea::horizontalScrollBarPolicy` 用于计算、查询或取得与“水平、Scroll、Bar、Policy”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `Qt::ScrollBarPolicy`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`Qt::ScrollBarPolicy`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void setHorizontalScrollBarPolicy(Qt::ScrollBarPolicy)`

**API 类别：** 公有函数

**中文解读：** 这是配置/写入操作 `setHorizontalScrollBarPolicy`。调用它会改变 `QAbstractScrollArea` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `ScrollBarPolicy`：类型为 `Qt::`。没有默认值，调用时必须提供。传入 `Qt::` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void setSizeAdjustPolicy(QAbstractScrollArea::SizeAdjustPolicy policy)`

**API 类别：** 公有函数

**中文解读：** 这是配置/写入操作 `setSizeAdjustPolicy`。调用它会改变 `QAbstractScrollArea` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `policy`：类型为 `QAbstractScrollArea::SizeAdjustPolicy`。没有默认值，调用时必须提供。传入 `QAbstractScrollArea::SizeAdjustPolicy` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void setVerticalScrollBarPolicy(Qt::ScrollBarPolicy)`

**API 类别：** 公有函数

**中文解读：** 这是配置/写入操作 `setVerticalScrollBarPolicy`。调用它会改变 `QAbstractScrollArea` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `ScrollBarPolicy`：类型为 `Qt::`。没有默认值，调用时必须提供。传入 `Qt::` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QAbstractScrollArea::SizeAdjustPolicy sizeAdjustPolicy() const`

**API 类别：** 公有函数

**中文解读：** `QAbstractScrollArea::sizeAdjustPolicy` 用于计算、查询或取得与“尺寸或数量、Adjust、Policy”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QAbstractScrollArea::SizeAdjustPolicy`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QAbstractScrollArea::SizeAdjustPolicy`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `Qt::ScrollBarPolicy verticalScrollBarPolicy() const`

**API 类别：** 公有函数

**中文解读：** `QAbstractScrollArea::verticalScrollBarPolicy` 用于计算、查询或取得与“垂直、Scroll、Bar、Policy”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `Qt::ScrollBarPolicy`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`Qt::ScrollBarPolicy`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

## 6. 深入实践与常见坑

### 生命周期和资源边界

控件有 parent 时通常由父控件管理销毁；顶层窗口可以放在栈上，也可以由应用对象或业务对象持有。隐藏控件仍然存在，关闭窗口也不一定等于删除对象或退出应用，必须明确 `WA_DeleteOnClose`、parent 和应用退出策略。

### 状态和错误边界

控件状态由属性、焦点、启用/禁用、可见性、选择状态和模型数据共同决定。改变属性可能触发重新布局或重绘；需要刷新界面时通常调用 `update()`，需要重新计算几何时让布局系统处理，不要直接调用 `paintEvent()`。

### 线程边界

所有 QWidget 的创建、访问、布局和绘制都应在 GUI 线程完成。后台线程通过信号把结果投递回来；不要从 worker 线程直接修改控件，也不要在 GUI 线程用 `waitFor...` 或长循环阻塞事件循环。

### 最容易出现的错误

不要绕过 begin/end 或状态通知；纯虚函数返回值和调用线程要按文档约定；抽象对象通常不能直接实例化。

### 版本和平台

本文档以 Qt 6.11.1 为依据。涉及平台后端、编解码器、数据库驱动、窗口风格、编译器特性或标注了版本号的 API 时，要把版本条件当作使用约束，而不是只看函数是否能补全。

## 7. 使用边界

`QAbstractScrollArea` 所属机制类型：Qt Widgets 界面机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
