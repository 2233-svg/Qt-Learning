# QGraphicsAnchorLayout

> Qt 6.11.1 · Qt Widgets

## 1. 先建立直觉

**一句话定位：** `QGraphicsAnchorLayout` 是 布局管理机制 中的类型，负责把这一机制中的数据、状态或资源交给其他 Qt 对象使用。

**模块背景：** Qt Widgets 提供传统桌面应用的控件、布局、模型/视图、窗口和交互组件。

### 这是什么

`QGraphicsAnchorLayout` 是 Qt Widgets 界面体系中的组件，负责一段可见 UI 或交互行为。

**内部模型：** 先区分它是顶层窗口、容器、输入控件、显示控件还是视图；再理解 parent、layout、model、signals 和事件之间的关系。

**适用场景：** 需要桌面控件、布局、用户输入、选择或模型/视图展示时使用。

**典型调用链：** 创建并设置 parent -> 配置属性和布局 -> connect 用户动作信号 -> show -> 按需处理事件/更新状态。

**先记住的坑：** 优先用 layout 管理几何；控件只能在 GUI 线程访问；自定义绘制放在 paintEvent；不要阻塞信号槽回调。

## 2. 依赖与对象关系

- 头文件：`#include <QGraphicsAnchorLayout>`
- 继承自：QGraphicsLayout
- 直接派生类：未在类页中列出

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Widgets)
target_link_libraries(mytarget PRIVATE Qt6::Widgets)
```

**继承带来的规则：** 它属于 QObject 对象模型（直接或间接继承 QObject），因此父对象、信号与槽、事件循环和线程归属是使用主线。

### 工作机制

先区分它是顶层窗口、容器、输入控件、显示控件还是视图；再理解 parent、layout、model、signals 和事件之间的关系。

### 状态、生命周期和线程

**生命周期：** 顶层布局可以在构造时绑定到 QWidget，也可以通过 `setLayout()` 安装；嵌套布局加入父布局后所有权交给父布局。布局析构不会自动销毁普通 QWidget，动态移除项目时要分别处理控件、子布局和 spacer。

**状态与结果：** 布局的项目索引会随着 add、insert、remove 和 takeAt 改变；索引既包括控件，也包括子布局、固定空白和 stretch。修改项目或尺寸参数后 Qt 会使布局失效并重新计算。

**线程与事件循环：** 布局只应在 GUI 线程操作，因为它直接改变 QWidget 几何和可见界面。布局系统不负责业务线程同步，也不会把手动的跨线程控件访问变安全。

## 3. 直接使用

需要桌面控件、布局、用户输入、选择或模型/视图展示时使用。 使用时通常按这个过程组织：创建并设置 parent -> 配置属性和布局 -> connect 用户动作信号 -> show -> 按需处理事件/更新状态。
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 公有函数

- `QGraphicsAnchorLayout(QGraphicsLayoutItem *parent = nullptr)`
- `virtual ~QGraphicsAnchorLayout()`
- `QGraphicsAnchor * addAnchor(QGraphicsLayoutItem *firstItem, Qt::AnchorPoint firstEdge, QGraphicsLayoutItem *secondItem, Qt::AnchorPoint secondEdge)`
- `void addAnchors(QGraphicsLayoutItem *firstItem, QGraphicsLayoutItem *secondItem, Qt::Orientations orientations = Qt::Horizontal | Qt::Vertical)`
- `void addCornerAnchors(QGraphicsLayoutItem *firstItem, Qt::Corner firstCorner, QGraphicsLayoutItem *secondItem, Qt::Corner secondCorner)`
- `QGraphicsAnchor * anchor(QGraphicsLayoutItem *firstItem, Qt::AnchorPoint firstEdge, QGraphicsLayoutItem *secondItem, Qt::AnchorPoint secondEdge)`
- `qreal horizontalSpacing() const`
- `void setHorizontalSpacing(qreal spacing)`
- `void setSpacing(qreal spacing)`
- `void setVerticalSpacing(qreal spacing)`
- `qreal verticalSpacing() const`

### 重实现的公有函数

- `virtual int count() const override`
- `virtual void invalidate() override`
- `virtual QGraphicsLayoutItem * itemAt(int index) const override`
- `virtual void removeAt(int index) override`
- `virtual void setGeometry(const QRectF &geom) override`

### 重实现的保护函数

- `virtual QSizeF sizeHint(Qt::SizeHint which, const QSizeF &constraint = QSizeF()) const override`

## 5. API 逐个说明

这里直接说明每个公开成员解决什么问题、参数代表什么、返回什么、会改变什么以及使用时容易出现什么问题。每一个公开签名都会有对应的中文解释。

本类共整理 17 个公开成员条目；没有独立长描述的 API 也会根据签名、类型和所属机制给出使用说明。

### `QGraphicsAnchorLayout::QGraphicsAnchorLayout(QGraphicsLayoutItem *parent = nullptr)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QGraphicsAnchorLayout` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `parent`：类型为 `QGraphicsLayoutItem *`。默认值为 `nullptr`。父对象。设置后通常由父对象负责销毁子对象；只有在对象确实应挂入这棵对象树时才传入。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual noexcept] QGraphicsAnchorLayout::~QGraphicsAnchorLayout()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QGraphicsAnchorLayout` 的析构函数。对象销毁时资源、子对象和连接会按 Qt 规则释放；异步对象要先停止任务或使用 deleteLater，避免回调访问已经不存在的实例。

**签名拆解：**

- 返回值：析构函数，无返回值。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QGraphicsAnchor *QGraphicsAnchorLayout::addAnchor(QGraphicsLayoutItem *firstItem, Qt::AnchorPoint firstEdge, QGraphicsLayoutItem *secondItem, Qt::AnchorPoint secondEdge)`

**API 类别：** 成员函数说明

**中文解读：** 这是向 `QGraphicsAnchorLayout` 添加依赖、数据或子对象的 API `addAnchor`。注意对象所有权、重复添加和添加后的通知；如果对应有 remove/take 接口，要明确谁负责移除后的生命周期。

**签名拆解：**

- 返回值：`QGraphicsAnchor *`。
- 参数 `firstItem`：类型为 `QGraphicsLayoutItem *`。没有默认值，调用时必须提供。传入 `QGraphicsLayoutItem *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `firstEdge`：类型为 `Qt::AnchorPoint`。没有默认值，调用时必须提供。传入 `Qt::AnchorPoint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `secondItem`：类型为 `QGraphicsLayoutItem *`。没有默认值，调用时必须提供。传入 `QGraphicsLayoutItem *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `secondEdge`：类型为 `Qt::AnchorPoint`。没有默认值，调用时必须提供。传入 `Qt::AnchorPoint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QGraphicsAnchorLayout::addAnchors(QGraphicsLayoutItem *firstItem, QGraphicsLayoutItem *secondItem, Qt::Orientations orientations = Qt::Horizontal | Qt::Vertical)`

**API 类别：** 成员函数说明

**中文解读：** 这是向 `QGraphicsAnchorLayout` 添加依赖、数据或子对象的 API `addAnchors`。注意对象所有权、重复添加和添加后的通知；如果对应有 remove/take 接口，要明确谁负责移除后的生命周期。

**签名拆解：**

- 返回值：`void`。
- 参数 `firstItem`：类型为 `QGraphicsLayoutItem *`。没有默认值，调用时必须提供。传入 `QGraphicsLayoutItem *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `secondItem`：类型为 `QGraphicsLayoutItem *`。没有默认值，调用时必须提供。传入 `QGraphicsLayoutItem *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `orientations`：类型为 `Qt::Orientations`。默认值为 `Qt::Horizontal | Qt::Vertical`。传入 `Qt::Orientations` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QGraphicsAnchorLayout::addCornerAnchors(QGraphicsLayoutItem *firstItem, Qt::Corner firstCorner, QGraphicsLayoutItem *secondItem, Qt::Corner secondCorner)`

**API 类别：** 成员函数说明

**中文解读：** 这是向 `QGraphicsAnchorLayout` 添加依赖、数据或子对象的 API `addCornerAnchors`。注意对象所有权、重复添加和添加后的通知；如果对应有 remove/take 接口，要明确谁负责移除后的生命周期。

**签名拆解：**

- 返回值：`void`。
- 参数 `firstItem`：类型为 `QGraphicsLayoutItem *`。没有默认值，调用时必须提供。传入 `QGraphicsLayoutItem *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `firstCorner`：类型为 `Qt::Corner`。没有默认值，调用时必须提供。传入 `Qt::Corner` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `secondItem`：类型为 `QGraphicsLayoutItem *`。没有默认值，调用时必须提供。传入 `QGraphicsLayoutItem *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `secondCorner`：类型为 `Qt::Corner`。没有默认值，调用时必须提供。传入 `Qt::Corner` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QGraphicsAnchor *QGraphicsAnchorLayout::anchor(QGraphicsLayoutItem *firstItem, Qt::AnchorPoint firstEdge, QGraphicsLayoutItem *secondItem, Qt::AnchorPoint secondEdge)`

**API 类别：** 成员函数说明

**中文解读：** `QGraphicsAnchorLayout::anchor` 用于计算、查询或取得与“anchor”相关的操作。调用时要先确认当前状态和 `firstItem`、`firstEdge`、`secondItem`、`secondEdge` 的有效范围；返回类型是 `QGraphicsAnchor *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QGraphicsAnchor *`。
- 参数 `firstItem`：类型为 `QGraphicsLayoutItem *`。没有默认值，调用时必须提供。传入 `QGraphicsLayoutItem *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `firstEdge`：类型为 `Qt::AnchorPoint`。没有默认值，调用时必须提供。传入 `Qt::AnchorPoint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `secondItem`：类型为 `QGraphicsLayoutItem *`。没有默认值，调用时必须提供。传入 `QGraphicsLayoutItem *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `secondEdge`：类型为 `Qt::AnchorPoint`。没有默认值，调用时必须提供。传入 `Qt::AnchorPoint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual] int QGraphicsAnchorLayout::count() const`

**API 类别：** 成员函数说明

**中文解读：** 这是尺寸/数量查询 API `count`，返回 `QGraphicsAnchorLayout` 当前元素数、字节数、容量或可用空间。它是某一时刻的快照，不能替代并发同步或后续操作的边界检查。

**签名拆解：**

- 返回值：`int`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `qreal QGraphicsAnchorLayout::horizontalSpacing() const`

**API 类别：** 成员函数说明

**中文解读：** `QGraphicsAnchorLayout::horizontalSpacing` 用于计算、查询或取得与“水平、Spacing”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `qreal`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`qreal`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual] void QGraphicsAnchorLayout::invalidate()`

**API 类别：** 成员函数说明

**中文解读：** 这是状态清理或重置 API `invalidate`。调用后原有数据、索引、缓存或绑定可能失效；使用前先确认它影响的是当前对象、子对象还是底层共享资源，之后重新检查状态。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual] QGraphicsLayoutItem *QGraphicsAnchorLayout::itemAt(int index) const`

**API 类别：** 成员函数说明

**中文解读：** 这是数据访问 API `itemAt`，用于取得 `QGraphicsAnchorLayout` 当前的元素、字段或底层存储。读取前确认索引/键有效；如果返回引用或指针，不要让它跨越对象修改、容器扩容或临时对象生命周期。

**签名拆解：**

- 返回值：`QGraphicsLayoutItem *`。
- 参数 `index`：类型为 `int`。没有默认值，调用时必须提供。项目或数据索引。先确认索引基于 0 还是 1、是否允许越界/负数，以及调用后索引是否仍然有效。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual] void QGraphicsAnchorLayout::removeAt(int index)`

**API 类别：** 成员函数说明

**中文解读：** 这是结束/释放/取消 API `removeAt`。它会改变对象状态或资源所有权，调用后不要继续使用已经失效的句柄、reply、索引或设备，并确认异步完成信号是否仍会到达。

**签名拆解：**

- 返回值：`void`。
- 参数 `index`：类型为 `int`。没有默认值，调用时必须提供。项目或数据索引。先确认索引基于 0 还是 1、是否允许越界/负数，以及调用后索引是否仍然有效。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual] void QGraphicsAnchorLayout::setGeometry(const QRectF &geom)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setGeometry`。调用它会改变 `QGraphicsAnchorLayout` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `geom`：类型为 `const QRectF &`。没有默认值，调用时必须提供。传入 `const QRectF &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QGraphicsAnchorLayout::setHorizontalSpacing(qreal spacing)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setHorizontalSpacing`。调用它会改变 `QGraphicsAnchorLayout` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `spacing`：类型为 `qreal`。没有默认值，调用时必须提供。相邻项目之间的间隔，通常以像素表示；它通常不等于外边距。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QGraphicsAnchorLayout::setSpacing(qreal spacing)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setSpacing`。调用它会改变 `QGraphicsAnchorLayout` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `spacing`：类型为 `qreal`。没有默认值，调用时必须提供。相邻项目之间的间隔，通常以像素表示；它通常不等于外边距。

**正确调用组合：** 与 `setContentsMargins()` 配合控制内部间隔和外部边距，不能用一个替代另一个。

### `void QGraphicsAnchorLayout::setVerticalSpacing(qreal spacing)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setVerticalSpacing`。调用它会改变 `QGraphicsAnchorLayout` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `spacing`：类型为 `qreal`。没有默认值，调用时必须提供。相邻项目之间的间隔，通常以像素表示；它通常不等于外边距。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual protected] QSizeF QGraphicsAnchorLayout::sizeHint(Qt::SizeHint which, const QSizeF &constraint = QSizeF()) const`

**API 类别：** 成员函数说明

**中文解读：** `QGraphicsAnchorLayout::sizeHint` 用于计算、查询或取得与“尺寸或数量、Hint”相关的操作。调用时要先确认当前状态和 `which`、`constraint` 的有效范围；返回类型是 `QSizeF`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QSizeF`。
- 参数 `which`：类型为 `Qt::SizeHint`。没有默认值，调用时必须提供。传入 `Qt::SizeHint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `constraint`：类型为 `const QSizeF &`。默认值为 `QSizeF()`。传入 `const QSizeF &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `qreal QGraphicsAnchorLayout::verticalSpacing() const`

**API 类别：** 成员函数说明

**中文解读：** `QGraphicsAnchorLayout::verticalSpacing` 用于计算、查询或取得与“垂直、Spacing”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `qreal`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`qreal`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

## 6. 深入实践与常见坑

### 生命周期和资源边界

顶层布局可以在构造时绑定到 QWidget，也可以通过 `setLayout()` 安装；嵌套布局加入父布局后所有权交给父布局。布局析构不会自动销毁普通 QWidget，动态移除项目时要分别处理控件、子布局和 spacer。

### 状态和错误边界

布局的项目索引会随着 add、insert、remove 和 takeAt 改变；索引既包括控件，也包括子布局、固定空白和 stretch。修改项目或尺寸参数后 Qt 会使布局失效并重新计算。

### 线程边界

布局只应在 GUI 线程操作，因为它直接改变 QWidget 几何和可见界面。布局系统不负责业务线程同步，也不会把手动的跨线程控件访问变安全。

### 最容易出现的错误

优先用 layout 管理几何；控件只能在 GUI 线程访问；自定义绘制放在 paintEvent；不要阻塞信号槽回调。

### 版本和平台

本文档以 Qt 6.11.1 为依据。涉及平台后端、编解码器、数据库驱动、窗口风格、编译器特性或标注了版本号的 API 时，要把版本条件当作使用约束，而不是只看函数是否能补全。

## 7. 使用边界

`QGraphicsAnchorLayout` 所属机制类型：布局管理机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
