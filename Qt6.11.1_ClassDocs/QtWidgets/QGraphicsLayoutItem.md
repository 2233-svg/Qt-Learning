# QGraphicsLayoutItem

> Qt 6.11.1 · Qt Widgets

## 1. 先建立直觉

**一句话定位：** `QGraphicsLayoutItem` 是 图形场景与项目机制 中的类型，负责把这一机制中的数据、状态或资源交给其他 Qt 对象使用。

**模块背景：** Qt Widgets 提供传统桌面应用的控件、布局、模型/视图、窗口和交互组件。

### 这是什么

`QGraphicsLayoutItem` 是 Qt Widgets 界面体系中的组件，负责一段可见 UI 或交互行为。

**内部模型：** 先区分它是顶层窗口、容器、输入控件、显示控件还是视图；再理解 parent、layout、model、signals 和事件之间的关系。

**适用场景：** 需要桌面控件、布局、用户输入、选择或模型/视图展示时使用。

**典型调用链：** 创建并设置 parent -> 配置属性和布局 -> connect 用户动作信号 -> show -> 按需处理事件/更新状态。

**先记住的坑：** 优先用 layout 管理几何；控件只能在 GUI 线程访问；自定义绘制放在 paintEvent；不要阻塞信号槽回调。

## 2. 依赖与对象关系

- 头文件：`#include <QGraphicsLayoutItem>`
- 继承自：未在类页中列出
- 直接派生类：QGraphicsLayout、QGraphicsWidget

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Widgets)
target_link_libraries(mytarget PRIVATE Qt6::Widgets)
```

**继承带来的规则：** 它属于 QObject 对象模型（直接或间接继承 QObject），因此父对象、信号与槽、事件循环和线程归属是使用主线。

### 工作机制

先区分它是顶层窗口、容器、输入控件、显示控件还是视图；再理解 parent、layout、model、signals 和事件之间的关系。

### 状态、生命周期和线程

**生命周期：** 场景或父项目通常管理子项目，但视图只是观察者，不一定拥有场景。删除项目、改变父项目或切换场景时要确认索引、指针、选中状态和布局关系是否仍有效。

**状态与结果：** 区分局部坐标、场景坐标、视图/窗口坐标，区分选中、悬停、焦点、可见和碰撞状态。改变几何、变换或数据后通常请求更新，而不是手动强制调用绘制函数。

**线程与事件循环：** 图形对象通常只能在其所属 GUI/场景线程操作；后台线程负责数据准备，结果通过信号投递后再更新场景对象。

## 3. 直接使用

需要桌面控件、布局、用户输入、选择或模型/视图展示时使用。 使用时通常按这个过程组织：创建并设置 parent -> 配置属性和布局 -> connect 用户动作信号 -> show -> 按需处理事件/更新状态。
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 公有函数

- `QGraphicsLayoutItem(QGraphicsLayoutItem *parent = nullptr, bool isLayout = false)`
- `virtual ~QGraphicsLayoutItem()`
- `QRectF contentsRect() const`
- `QSizeF effectiveSizeHint(Qt::SizeHint which, const QSizeF &constraint = QSizeF()) const`
- `QRectF geometry() const`
- `virtual void getContentsMargins(qreal *left, qreal *top, qreal *right, qreal *bottom) const`
- `QGraphicsItem * graphicsItem() const`
- `(since 6.0) virtual bool isEmpty() const`
- `bool isLayout() const`
- `qreal maximumHeight() const`
- `QSizeF maximumSize() const`
- `qreal maximumWidth() const`
- `qreal minimumHeight() const`
- `QSizeF minimumSize() const`
- `qreal minimumWidth() const`
- `bool ownedByLayout() const`
- `QGraphicsLayoutItem * parentLayoutItem() const`
- `qreal preferredHeight() const`
- `QSizeF preferredSize() const`
- `qreal preferredWidth() const`
- `virtual void setGeometry(const QRectF &rect)`
- `void setMaximumHeight(qreal height)`
- `void setMaximumSize(const QSizeF &size)`
- `void setMaximumSize(qreal w, qreal h)`
- `void setMaximumWidth(qreal width)`
- `void setMinimumHeight(qreal height)`
- `void setMinimumSize(const QSizeF &size)`
- `void setMinimumSize(qreal w, qreal h)`
- `void setMinimumWidth(qreal width)`
- `void setParentLayoutItem(QGraphicsLayoutItem *parent)`
- `void setPreferredHeight(qreal height)`
- `void setPreferredSize(const QSizeF &size)`
- `void setPreferredSize(qreal w, qreal h)`
- `void setPreferredWidth(qreal width)`
- `void setSizePolicy(const QSizePolicy &policy)`
- `void setSizePolicy(QSizePolicy::Policy hPolicy, QSizePolicy::Policy vPolicy, QSizePolicy::ControlType controlType = QSizePolicy::DefaultType)`
- `QSizePolicy sizePolicy() const`
- `virtual void updateGeometry()`

### 保护函数

- `void setGraphicsItem(QGraphicsItem *item)`
- `void setOwnedByLayout(bool ownership)`
- `virtual QSizeF sizeHint(Qt::SizeHint which, const QSizeF &constraint = QSizeF()) const = 0`

## 5. API 逐个说明

这里直接说明每个公开成员解决什么问题、参数代表什么、返回什么、会改变什么以及使用时容易出现什么问题。每一个公开签名都会有对应的中文解释。

本类共整理 41 个公开成员条目；没有独立长描述的 API 也会根据签名、类型和所属机制给出使用说明。

### `QGraphicsLayoutItem::QGraphicsLayoutItem(QGraphicsLayoutItem *parent = nullptr, bool isLayout = false)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QGraphicsLayoutItem` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `parent`：类型为 `QGraphicsLayoutItem *`。默认值为 `nullptr`。父对象。设置后通常由父对象负责销毁子对象；只有在对象确实应挂入这棵对象树时才传入。
- 参数 `isLayout`：类型为 `bool`。默认值为 `false`。传入 `bool` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual noexcept] QGraphicsLayoutItem::~QGraphicsLayoutItem()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QGraphicsLayoutItem` 的析构函数。对象销毁时资源、子对象和连接会按 Qt 规则释放；异步对象要先停止任务或使用 deleteLater，避免回调访问已经不存在的实例。

**签名拆解：**

- 返回值：析构函数，无返回值。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QRectF QGraphicsLayoutItem::contentsRect() const`

**API 类别：** 成员函数说明

**中文解读：** `QGraphicsLayoutItem::contentsRect` 用于计算、查询或取得与“contents、Rect”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QRectF`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QRectF`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QSizeF QGraphicsLayoutItem::effectiveSizeHint(Qt::SizeHint which, const QSizeF &constraint = QSizeF()) const`

**API 类别：** 成员函数说明

**中文解读：** `QGraphicsLayoutItem::effectiveSizeHint` 用于计算、查询或取得与“effective、尺寸或数量、Hint”相关的操作。调用时要先确认当前状态和 `which`、`constraint` 的有效范围；返回类型是 `QSizeF`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QSizeF`。
- 参数 `which`：类型为 `Qt::SizeHint`。没有默认值，调用时必须提供。传入 `Qt::SizeHint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `constraint`：类型为 `const QSizeF &`。默认值为 `QSizeF()`。传入 `const QSizeF &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QRectF QGraphicsLayoutItem::geometry() const`

**API 类别：** 成员函数说明

**中文解读：** `QGraphicsLayoutItem::geometry` 用于计算、查询或取得与“几何区域”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QRectF`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QRectF`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual] void QGraphicsLayoutItem::getContentsMargins(qreal *left, qreal *top, qreal *right, qreal *bottom) const`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QGraphicsLayoutItem` 的核心操作 `getContentsMargins`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`void`。
- 参数 `left`：类型为 `qreal *`。没有默认值，调用时必须提供。传入 `qreal *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `top`：类型为 `qreal *`。没有默认值，调用时必须提供。传入 `qreal *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `right`：类型为 `qreal *`。没有默认值，调用时必须提供。传入 `qreal *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `bottom`：类型为 `qreal *`。没有默认值，调用时必须提供。传入 `qreal *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QGraphicsItem *QGraphicsLayoutItem::graphicsItem() const`

**API 类别：** 成员函数说明

**中文解读：** `QGraphicsLayoutItem::graphicsItem` 用于计算、查询或取得与“graphics、项目访问”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QGraphicsItem *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QGraphicsItem *`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual, since 6.0] bool QGraphicsLayoutItem::isEmpty() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `isEmpty`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QGraphicsLayoutItem::isLayout() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `isLayout`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `qreal QGraphicsLayoutItem::maximumHeight() const`

**API 类别：** 成员函数说明

**中文解读：** `QGraphicsLayoutItem::maximumHeight` 用于计算、查询或取得与“最大值、高度”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `qreal`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`qreal`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QSizeF QGraphicsLayoutItem::maximumSize() const`

**API 类别：** 成员函数说明

**中文解读：** `QGraphicsLayoutItem::maximumSize` 用于计算、查询或取得与“最大值、尺寸或数量”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QSizeF`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QSizeF`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `qreal QGraphicsLayoutItem::maximumWidth() const`

**API 类别：** 成员函数说明

**中文解读：** `QGraphicsLayoutItem::maximumWidth` 用于计算、查询或取得与“最大值、宽度”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `qreal`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`qreal`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `qreal QGraphicsLayoutItem::minimumHeight() const`

**API 类别：** 成员函数说明

**中文解读：** `QGraphicsLayoutItem::minimumHeight` 用于计算、查询或取得与“最小值、高度”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `qreal`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`qreal`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QSizeF QGraphicsLayoutItem::minimumSize() const`

**API 类别：** 成员函数说明

**中文解读：** `QGraphicsLayoutItem::minimumSize` 用于计算、查询或取得与“最小值、尺寸或数量”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QSizeF`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QSizeF`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `qreal QGraphicsLayoutItem::minimumWidth() const`

**API 类别：** 成员函数说明

**中文解读：** `QGraphicsLayoutItem::minimumWidth` 用于计算、查询或取得与“最小值、宽度”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `qreal`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`qreal`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QGraphicsLayoutItem::ownedByLayout() const`

**API 类别：** 成员函数说明

**中文解读：** `QGraphicsLayoutItem::ownedByLayout` 用于计算、查询或取得与“owned、By、Layout”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QGraphicsLayoutItem *QGraphicsLayoutItem::parentLayoutItem() const`

**API 类别：** 成员函数说明

**中文解读：** `QGraphicsLayoutItem::parentLayoutItem` 用于计算、查询或取得与“父对象、Layout、项目访问”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QGraphicsLayoutItem *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QGraphicsLayoutItem *`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `qreal QGraphicsLayoutItem::preferredHeight() const`

**API 类别：** 成员函数说明

**中文解读：** `QGraphicsLayoutItem::preferredHeight` 用于计算、查询或取得与“preferred、高度”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `qreal`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`qreal`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QSizeF QGraphicsLayoutItem::preferredSize() const`

**API 类别：** 成员函数说明

**中文解读：** `QGraphicsLayoutItem::preferredSize` 用于计算、查询或取得与“preferred、尺寸或数量”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QSizeF`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QSizeF`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `qreal QGraphicsLayoutItem::preferredWidth() const`

**API 类别：** 成员函数说明

**中文解读：** `QGraphicsLayoutItem::preferredWidth` 用于计算、查询或取得与“preferred、宽度”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `qreal`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`qreal`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual] void QGraphicsLayoutItem::setGeometry(const QRectF &rect)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setGeometry`。调用它会改变 `QGraphicsLayoutItem` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `rect`：类型为 `const QRectF &`。没有默认值，调用时必须提供。矩形区域；要确认坐标系、是否包含右下边界以及空矩形的语义。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[protected] void QGraphicsLayoutItem::setGraphicsItem(QGraphicsItem *item)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setGraphicsItem`。调用它会改变 `QGraphicsLayoutItem` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `item`：类型为 `QGraphicsItem *`。没有默认值，调用时必须提供。容器、布局或模型中的一个项目；要确认加入后所有权是否转移以及项目是否允许为空。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QGraphicsLayoutItem::setMaximumHeight(qreal height)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setMaximumHeight`。调用它会改变 `QGraphicsLayoutItem` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `height`：类型为 `qreal`。没有默认值，调用时必须提供。高度，通常以像素、字符数或元素数量表示；要确认是否允许 0、负数和超出最大值。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QGraphicsLayoutItem::setMaximumSize(const QSizeF &size)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setMaximumSize`。调用它会改变 `QGraphicsLayoutItem` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `size`：类型为 `const QSizeF &`。没有默认值，调用时必须提供。尺寸或长度，单位通常是像素、字节、元素数或时间，必须结合类型和类的上下文确认。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QGraphicsLayoutItem::setMaximumSize(qreal w, qreal h)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setMaximumSize`。调用它会改变 `QGraphicsLayoutItem` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `w`：类型为 `qreal`。没有默认值，调用时必须提供。传入 `qreal` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `h`：类型为 `qreal`。没有默认值，调用时必须提供。传入 `qreal` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QGraphicsLayoutItem::setMaximumWidth(qreal width)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setMaximumWidth`。调用它会改变 `QGraphicsLayoutItem` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `width`：类型为 `qreal`。没有默认值，调用时必须提供。宽度，通常以像素、字符数或元素数量表示；要确认是否允许 0、负数和超出最大值。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QGraphicsLayoutItem::setMinimumHeight(qreal height)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setMinimumHeight`。调用它会改变 `QGraphicsLayoutItem` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `height`：类型为 `qreal`。没有默认值，调用时必须提供。高度，通常以像素、字符数或元素数量表示；要确认是否允许 0、负数和超出最大值。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QGraphicsLayoutItem::setMinimumSize(const QSizeF &size)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setMinimumSize`。调用它会改变 `QGraphicsLayoutItem` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `size`：类型为 `const QSizeF &`。没有默认值，调用时必须提供。尺寸或长度，单位通常是像素、字节、元素数或时间，必须结合类型和类的上下文确认。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QGraphicsLayoutItem::setMinimumSize(qreal w, qreal h)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setMinimumSize`。调用它会改变 `QGraphicsLayoutItem` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `w`：类型为 `qreal`。没有默认值，调用时必须提供。传入 `qreal` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `h`：类型为 `qreal`。没有默认值，调用时必须提供。传入 `qreal` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QGraphicsLayoutItem::setMinimumWidth(qreal width)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setMinimumWidth`。调用它会改变 `QGraphicsLayoutItem` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `width`：类型为 `qreal`。没有默认值，调用时必须提供。宽度，通常以像素、字符数或元素数量表示；要确认是否允许 0、负数和超出最大值。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[protected] void QGraphicsLayoutItem::setOwnedByLayout(bool ownership)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setOwnedByLayout`。调用它会改变 `QGraphicsLayoutItem` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `ownership`：类型为 `bool`。没有默认值，调用时必须提供。传入 `bool` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QGraphicsLayoutItem::setParentLayoutItem(QGraphicsLayoutItem *parent)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setParentLayoutItem`。调用它会改变 `QGraphicsLayoutItem` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `parent`：类型为 `QGraphicsLayoutItem *`。没有默认值，调用时必须提供。父对象。设置后通常由父对象负责销毁子对象；只有在对象确实应挂入这棵对象树时才传入。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QGraphicsLayoutItem::setPreferredHeight(qreal height)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setPreferredHeight`。调用它会改变 `QGraphicsLayoutItem` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `height`：类型为 `qreal`。没有默认值，调用时必须提供。高度，通常以像素、字符数或元素数量表示；要确认是否允许 0、负数和超出最大值。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QGraphicsLayoutItem::setPreferredSize(const QSizeF &size)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setPreferredSize`。调用它会改变 `QGraphicsLayoutItem` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `size`：类型为 `const QSizeF &`。没有默认值，调用时必须提供。尺寸或长度，单位通常是像素、字节、元素数或时间，必须结合类型和类的上下文确认。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QGraphicsLayoutItem::setPreferredSize(qreal w, qreal h)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setPreferredSize`。调用它会改变 `QGraphicsLayoutItem` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `w`：类型为 `qreal`。没有默认值，调用时必须提供。传入 `qreal` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `h`：类型为 `qreal`。没有默认值，调用时必须提供。传入 `qreal` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QGraphicsLayoutItem::setPreferredWidth(qreal width)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setPreferredWidth`。调用它会改变 `QGraphicsLayoutItem` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `width`：类型为 `qreal`。没有默认值，调用时必须提供。宽度，通常以像素、字符数或元素数量表示；要确认是否允许 0、负数和超出最大值。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QGraphicsLayoutItem::setSizePolicy(const QSizePolicy &policy)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setSizePolicy`。调用它会改变 `QGraphicsLayoutItem` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `policy`：类型为 `const QSizePolicy &`。没有默认值，调用时必须提供。传入 `const QSizePolicy &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QGraphicsLayoutItem::setSizePolicy(QSizePolicy::Policy hPolicy, QSizePolicy::Policy vPolicy, QSizePolicy::ControlType controlType = QSizePolicy::DefaultType)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setSizePolicy`。调用它会改变 `QGraphicsLayoutItem` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `hPolicy`：类型为 `QSizePolicy::Policy`。没有默认值，调用时必须提供。传入 `QSizePolicy::Policy` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `vPolicy`：类型为 `QSizePolicy::Policy`。没有默认值，调用时必须提供。传入 `QSizePolicy::Policy` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `controlType`：类型为 `QSizePolicy::ControlType`。默认值为 `QSizePolicy::DefaultType`。传入 `QSizePolicy::ControlType` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[pure virtual protected] QSizeF QGraphicsLayoutItem::sizeHint(Qt::SizeHint which, const QSizeF &constraint = QSizeF()) const`

**API 类别：** 成员函数说明

**中文解读：** `QGraphicsLayoutItem::sizeHint` 用于计算、查询或取得与“尺寸或数量、Hint”相关的操作。调用时要先确认当前状态和 `which`、`constraint` 的有效范围；返回类型是 `QSizeF`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QSizeF`。
- 参数 `which`：类型为 `Qt::SizeHint`。没有默认值，调用时必须提供。传入 `Qt::SizeHint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `constraint`：类型为 `const QSizeF &`。默认值为 `QSizeF()`。传入 `const QSizeF &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QSizePolicy QGraphicsLayoutItem::sizePolicy() const`

**API 类别：** 成员函数说明

**中文解读：** `QGraphicsLayoutItem::sizePolicy` 用于计算、查询或取得与“尺寸或数量、Policy”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QSizePolicy`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QSizePolicy`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual] void QGraphicsLayoutItem::updateGeometry()`

**API 类别：** 成员函数说明

**中文解读：** `QGraphicsLayoutItem::updateGeometry` 用于执行与“更新、几何区域”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

## 6. 深入实践与常见坑

### 生命周期和资源边界

场景或父项目通常管理子项目，但视图只是观察者，不一定拥有场景。删除项目、改变父项目或切换场景时要确认索引、指针、选中状态和布局关系是否仍有效。

### 状态和错误边界

区分局部坐标、场景坐标、视图/窗口坐标，区分选中、悬停、焦点、可见和碰撞状态。改变几何、变换或数据后通常请求更新，而不是手动强制调用绘制函数。

### 线程边界

图形对象通常只能在其所属 GUI/场景线程操作；后台线程负责数据准备，结果通过信号投递后再更新场景对象。

### 最容易出现的错误

优先用 layout 管理几何；控件只能在 GUI 线程访问；自定义绘制放在 paintEvent；不要阻塞信号槽回调。

### 版本和平台

本文档以 Qt 6.11.1 为依据。涉及平台后端、编解码器、数据库驱动、窗口风格、编译器特性或标注了版本号的 API 时，要把版本条件当作使用约束，而不是只看函数是否能补全。

## 7. 使用边界

`QGraphicsLayoutItem` 所属机制类型：图形场景与项目机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
