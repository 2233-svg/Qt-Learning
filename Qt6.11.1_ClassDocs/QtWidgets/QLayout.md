# QLayout

> Qt 6.11.1 · Qt Widgets

## 1. 先建立直觉

**一句话定位：** `QLayout` 是 布局管理机制 中的类型，负责把这一机制中的数据、状态或资源交给其他 Qt 对象使用。

**模块背景：** Qt Widgets 提供传统桌面应用的控件、布局、模型/视图、窗口和交互组件。

### 这是什么

`QLayout` 是 Qt Widgets 界面体系中的组件，负责一段可见 UI 或交互行为。

**内部模型：** 先区分它是顶层窗口、容器、输入控件、显示控件还是视图；再理解 parent、layout、model、signals 和事件之间的关系。

**适用场景：** 需要桌面控件、布局、用户输入、选择或模型/视图展示时使用。

**典型调用链：** 创建并设置 parent -> 配置属性和布局 -> connect 用户动作信号 -> show -> 按需处理事件/更新状态。

**先记住的坑：** 优先用 layout 管理几何；控件只能在 GUI 线程访问；自定义绘制放在 paintEvent；不要阻塞信号槽回调。

## 2. 依赖与对象关系

- 头文件：`#include <QLayout>`
- 继承自：QObject、QLayoutItem
- 直接派生类：QBoxLayout、QFormLayout、QGridLayout,、QStackedLayout

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

### 公有类型

- `enum SizeConstraint { SetDefaultConstraint, SetFixedSize, SetMinimumSize, SetMaximumSize, SetMinAndMaxSize, SetNoConstraint }`

### 属性

- `contentsMargins : QMargins`
- `(since 6.10) horizontalSizeConstraint : SizeConstraint`
- `sizeConstraint : SizeConstraint`
- `spacing : int`
- `(since 6.10) verticalSizeConstraint : SizeConstraint`

### 公有函数

- `QLayout(QWidget *parent = nullptr)`
- `bool activate()`
- `virtual void addItem(QLayoutItem *item) = 0`
- `void addWidget(QWidget *w)`
- `QMargins contentsMargins() const`
- `QRect contentsRect() const`
- `virtual int count() const = 0`
- `void getContentsMargins(int *left, int *top, int *right, int *bottom) const`
- `QLayout::SizeConstraint horizontalSizeConstraint() const`
- `virtual int indexOf(const QLayoutItem *layoutItem) const`
- `virtual int indexOf(const QWidget *widget) const`
- `bool isEnabled() const`
- `virtual QLayoutItem * itemAt(int index) const = 0`
- `QWidget * menuBar() const`
- `QWidget * parentWidget() const`
- `void removeItem(QLayoutItem *item)`
- `void removeWidget(QWidget *widget)`
- `virtual QLayoutItem * replaceWidget(QWidget *from, QWidget *to, Qt::FindChildOptions options = Qt::FindChildrenRecursively)`
- `bool setAlignment(QWidget *w, Qt::Alignment alignment)`
- `bool setAlignment(QLayout *l, Qt::Alignment alignment)`
- `void setContentsMargins(const QMargins &margins)`
- `void setContentsMargins(int left, int top, int right, int bottom)`
- `void setEnabled(bool enable)`
- `void setHorizontalSizeConstraint(QLayout::SizeConstraint constraint)`
- `void setMenuBar(QWidget *widget)`
- `void setSizeConstraint(QLayout::SizeConstraint constraint)`
- `(since 6.10) void setSizeConstraints(QLayout::SizeConstraint horizontal, QLayout::SizeConstraint vertical)`
- `virtual void setSpacing(int)`
- `void setVerticalSizeConstraint(QLayout::SizeConstraint constraint)`
- `QLayout::SizeConstraint sizeConstraint() const`
- `virtual int spacing() const`
- `virtual QLayoutItem * takeAt(int index) = 0`
- `(since 6.1) void unsetContentsMargins()`
- `void update()`
- `QLayout::SizeConstraint verticalSizeConstraint() const`

### 重实现的公有函数

- `virtual QSizePolicy::ControlTypes controlTypes() const override`
- `virtual Qt::Orientations expandingDirections() const override`
- `virtual QRect geometry() const override`
- `virtual void invalidate() override`
- `virtual bool isEmpty() const override`
- `virtual QLayout * layout() override`
- `virtual QSize maximumSize() const override`
- `virtual QSize minimumSize() const override`
- `virtual void setGeometry(const QRect &r) override`

### 静态公有成员

- `QSize closestAcceptableSize(const QWidget *widget, const QSize &size)`

### 保护函数

- `void addChildLayout(QLayout *childLayout)`
- `void addChildWidget(QWidget *w)`
- `QRect alignmentRect(const QRect &r) const`

### 重实现的保护函数

- `virtual void childEvent(QChildEvent *e) override`

## 5. API 逐个说明

这里直接说明每个公开成员解决什么问题、参数代表什么、返回什么、会改变什么以及使用时容易出现什么问题。每一个公开签名都会有对应的中文解释。

本类共整理 55 个公开成员条目；没有独立长描述的 API 也会根据签名、类型和所属机制给出使用说明。

### `enum QLayout::SizeConstraint`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QLayout` 暴露的类型声明 `尺寸或数量、Constraint`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 属性类型：`:SizeConstraint`。
- 属性名：`QLayout`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `contentsMargins : QMargins`

**API 类别：** 属性说明

**中文解读：** 这是 `QLayout` 的配置属性。初始化或状态切换时通过 `setContentsMargins(...)` 设置，之后用 `contentsMargins()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`QMargins`。
- 属性名：`contentsMargins`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.10] horizontalSizeConstraint : SizeConstraint`

**API 类别：** 属性说明

**中文解读：** 这是 `QLayout` 的配置属性。初始化或状态切换时通过 `setHorizontalSizeConstraint(...)` 设置，之后用 `horizontalSizeConstraint()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`SizeConstraint`。
- 属性名：`horizontalSizeConstraint`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `sizeConstraint : SizeConstraint`

**API 类别：** 属性说明

**中文解读：** 这是 `QLayout` 的配置属性。初始化或状态切换时通过 `setSizeConstraint(...)` 设置，之后用 `sizeConstraint()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`SizeConstraint`。
- 属性名：`sizeConstraint`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `spacing : int`

**API 类别：** 属性说明

**中文解读：** 这是 `QLayout` 的配置属性。初始化或状态切换时通过 `setSpacing(...)` 设置，之后用 `spacing()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`int`。
- 属性名：`spacing`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.10] verticalSizeConstraint : SizeConstraint`

**API 类别：** 属性说明

**中文解读：** 这是 `QLayout` 的配置属性。初始化或状态切换时通过 `setVerticalSizeConstraint(...)` 设置，之后用 `verticalSizeConstraint()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`SizeConstraint`。
- 属性名：`verticalSizeConstraint`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[explicit] QLayout::QLayout(QWidget *parent = nullptr)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QLayout` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `parent`：类型为 `QWidget *`。默认值为 `nullptr`。父对象。设置后通常由父对象负责销毁子对象；只有在对象确实应挂入这棵对象树时才传入。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QLayout::activate()`

**API 类别：** 成员函数说明

**中文解读：** `QLayout::activate` 用于计算、查询或取得与“activate”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[protected] void QLayout::addChildLayout(QLayout *childLayout)`

**API 类别：** 成员函数说明

**中文解读：** 这是向 `QLayout` 添加依赖、数据或子对象的 API `addChildLayout`。注意对象所有权、重复添加和添加后的通知；如果对应有 remove/take 接口，要明确谁负责移除后的生命周期。

**签名拆解：**

- 返回值：`void`。
- 参数 `childLayout`：类型为 `QLayout *`。没有默认值，调用时必须提供。传入 `QLayout *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[protected] void QLayout::addChildWidget(QWidget *w)`

**API 类别：** 成员函数说明

**中文解读：** 这是向 `QLayout` 添加依赖、数据或子对象的 API `addChildWidget`。注意对象所有权、重复添加和添加后的通知；如果对应有 remove/take 接口，要明确谁负责移除后的生命周期。

**签名拆解：**

- 返回值：`void`。
- 参数 `w`：类型为 `QWidget *`。没有默认值，调用时必须提供。Qt 对象参数。要确认对象有效、线程归属、所有权和该 API 是否只处理直接子对象。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[pure virtual] void QLayout::addItem(QLayoutItem *item)`

**API 类别：** 成员函数说明

**中文解读：** 这是向 `QLayout` 添加依赖、数据或子对象的 API `addItem`。注意对象所有权、重复添加和添加后的通知；如果对应有 remove/take 接口，要明确谁负责移除后的生命周期。

**签名拆解：**

- 返回值：`void`。
- 参数 `item`：类型为 `QLayoutItem *`。没有默认值，调用时必须提供。容器、布局或模型中的一个项目；要确认加入后所有权是否转移以及项目是否允许为空。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QLayout::addWidget(QWidget *w)`

**API 类别：** 成员函数说明

**中文解读：** 这是向 `QLayout` 添加依赖、数据或子对象的 API `addWidget`。注意对象所有权、重复添加和添加后的通知；如果对应有 remove/take 接口，要明确谁负责移除后的生命周期。

**签名拆解：**

- 返回值：`void`。
- 参数 `w`：类型为 `QWidget *`。没有默认值，调用时必须提供。Qt 对象参数。要确认对象有效、线程归属、所有权和该 API 是否只处理直接子对象。

**正确调用组合：** 通常与 `setContentsMargins()`、`setSpacing()` 和 stretch 一起使用；stretch 分配主方向剩余空间，alignment 控制控件在自身区域中的位置。

### `[protected] QRect QLayout::alignmentRect(const QRect &r) const`

**API 类别：** 成员函数说明

**中文解读：** `QLayout::alignmentRect` 用于计算、查询或取得与“对齐方式、Rect”相关的操作。调用时要先确认当前状态和 `r` 的有效范围；返回类型是 `QRect`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QRect`。
- 参数 `r`：类型为 `const QRect &`。没有默认值，调用时必须提供。传入 `const QRect &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual protected] void QLayout::childEvent(QChildEvent *e)`

**API 类别：** 成员函数说明

**中文解读：** `QLayout::childEvent` 用于执行与“child、Event”相关的操作。调用时要先确认当前状态和 `e` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `e`：类型为 `QChildEvent *`。没有默认值，调用时必须提供。传入 `QChildEvent *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] QSize QLayout::closestAcceptableSize(const QWidget *widget, const QSize &size)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `closestAcceptableSize`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QSize`。
- 参数 `widget`：类型为 `const QWidget *`。没有默认值，调用时必须提供。参与操作的 QWidget。要确认它是否为空、是否已被其他布局/容器管理，以及函数是否只查找直接子项。
- 参数 `size`：类型为 `const QSize &`。没有默认值，调用时必须提供。尺寸或长度，单位通常是像素、字节、元素数或时间，必须结合类型和类的上下文确认。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QMargins QLayout::contentsMargins() const`

**API 类别：** 成员函数说明

**中文解读：** `QLayout::contentsMargins` 用于计算、查询或取得与“contents、Margins”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QMargins`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QMargins`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QRect QLayout::contentsRect() const`

**API 类别：** 成员函数说明

**中文解读：** `QLayout::contentsRect` 用于计算、查询或取得与“contents、Rect”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QRect`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QRect`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual] QSizePolicy::ControlTypes QLayout::controlTypes() const`

**API 类别：** 成员函数说明

**中文解读：** `QLayout::controlTypes` 用于计算、查询或取得与“control、Types”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QSizePolicy::ControlTypes`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QSizePolicy::ControlTypes`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[pure virtual] int QLayout::count() const`

**API 类别：** 成员函数说明

**中文解读：** 这是尺寸/数量查询 API `count`，返回 `QLayout` 当前元素数、字节数、容量或可用空间。它是某一时刻的快照，不能替代并发同步或后续操作的边界检查。

**签名拆解：**

- 返回值：`int`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual] Qt::Orientations QLayout::expandingDirections() const`

**API 类别：** 成员函数说明

**中文解读：** `QLayout::expandingDirections` 用于计算、查询或取得与“expanding、Directions”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `Qt::Orientations`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`Qt::Orientations`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual] QRect QLayout::geometry() const`

**API 类别：** 成员函数说明

**中文解读：** `QLayout::geometry` 用于计算、查询或取得与“几何区域”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QRect`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QRect`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QLayout::getContentsMargins(int *left, int *top, int *right, int *bottom) const`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QLayout` 的核心操作 `getContentsMargins`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`void`。
- 参数 `left`：类型为 `int *`。没有默认值，调用时必须提供。传入 `int *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `top`：类型为 `int *`。没有默认值，调用时必须提供。传入 `int *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `right`：类型为 `int *`。没有默认值，调用时必须提供。传入 `int *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `bottom`：类型为 `int *`。没有默认值，调用时必须提供。传入 `int *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual] int QLayout::indexOf(const QLayoutItem *layoutItem) const`

**API 类别：** 成员函数说明

**中文解读：** `QLayout::indexOf` 用于计算、查询或取得与“索引、Of”相关的操作。调用时要先确认当前状态和 `layoutItem` 的有效范围；返回类型是 `int`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`int`。
- 参数 `layoutItem`：类型为 `const QLayoutItem *`。没有默认值，调用时必须提供。传入 `const QLayoutItem *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual] int QLayout::indexOf(const QWidget *widget) const`

**API 类别：** 成员函数说明

**中文解读：** `QLayout::indexOf` 用于计算、查询或取得与“索引、Of”相关的操作。调用时要先确认当前状态和 `widget` 的有效范围；返回类型是 `int`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`int`。
- 参数 `widget`：类型为 `const QWidget *`。没有默认值，调用时必须提供。参与操作的 QWidget。要确认它是否为空、是否已被其他布局/容器管理，以及函数是否只查找直接子项。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual] void QLayout::invalidate()`

**API 类别：** 成员函数说明

**中文解读：** 这是状态清理或重置 API `invalidate`。调用后原有数据、索引、缓存或绑定可能失效；使用前先确认它影响的是当前对象、子对象还是底层共享资源，之后重新检查状态。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual] bool QLayout::isEmpty() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `isEmpty`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QLayout::isEnabled() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `isEnabled`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[pure virtual] QLayoutItem *QLayout::itemAt(int index) const`

**API 类别：** 成员函数说明

**中文解读：** 这是数据访问 API `itemAt`，用于取得 `QLayout` 当前的元素、字段或底层存储。读取前确认索引/键有效；如果返回引用或指针，不要让它跨越对象修改、容器扩容或临时对象生命周期。

**签名拆解：**

- 返回值：`QLayoutItem *`。
- 参数 `index`：类型为 `int`。没有默认值，调用时必须提供。项目或数据索引。先确认索引基于 0 还是 1、是否允许越界/负数，以及调用后索引是否仍然有效。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual] QLayout *QLayout::layout()`

**API 类别：** 成员函数说明

**中文解读：** `QLayout::layout` 用于计算、查询或取得与“layout”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QLayout *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QLayout *`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual] QSize QLayout::maximumSize() const`

**API 类别：** 成员函数说明

**中文解读：** `QLayout::maximumSize` 用于计算、查询或取得与“最大值、尺寸或数量”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QSize`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QSize`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QWidget *QLayout::menuBar() const`

**API 类别：** 成员函数说明

**中文解读：** `QLayout::menuBar` 用于计算、查询或取得与“menu、Bar”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QWidget *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QWidget *`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual] QSize QLayout::minimumSize() const`

**API 类别：** 成员函数说明

**中文解读：** `QLayout::minimumSize` 用于计算、查询或取得与“最小值、尺寸或数量”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QSize`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QSize`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QWidget *QLayout::parentWidget() const`

**API 类别：** 成员函数说明

**中文解读：** `QLayout::parentWidget` 用于计算、查询或取得与“父对象、Widget”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QWidget *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QWidget *`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QLayout::removeItem(QLayoutItem *item)`

**API 类别：** 成员函数说明

**中文解读：** 这是结束/释放/取消 API `removeItem`。它会改变对象状态或资源所有权，调用后不要继续使用已经失效的句柄、reply、索引或设备，并确认异步完成信号是否仍会到达。

**签名拆解：**

- 返回值：`void`。
- 参数 `item`：类型为 `QLayoutItem *`。没有默认值，调用时必须提供。容器、布局或模型中的一个项目；要确认加入后所有权是否转移以及项目是否允许为空。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QLayout::removeWidget(QWidget *widget)`

**API 类别：** 成员函数说明

**中文解读：** 这是结束/释放/取消 API `removeWidget`。它会改变对象状态或资源所有权，调用后不要继续使用已经失效的句柄、reply、索引或设备，并确认异步完成信号是否仍会到达。

**签名拆解：**

- 返回值：`void`。
- 参数 `widget`：类型为 `QWidget *`。没有默认值，调用时必须提供。参与操作的 QWidget。要确认它是否为空、是否已被其他布局/容器管理，以及函数是否只查找直接子项。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual] QLayoutItem *QLayout::replaceWidget(QWidget *from, QWidget *to, Qt::FindChildOptions options = Qt::FindChildrenRecursively)`

**API 类别：** 成员函数说明

**中文解读：** `QLayout::replaceWidget` 用于计算、查询或取得与“替换、Widget”相关的操作。调用时要先确认当前状态和 `from`、`to`、`options` 的有效范围；返回类型是 `QLayoutItem *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QLayoutItem *`。
- 参数 `from`：类型为 `QWidget *`。没有默认值，调用时必须提供。Qt 对象参数。要确认对象有效、线程归属、所有权和该 API 是否只处理直接子对象。
- 参数 `to`：类型为 `QWidget *`。没有默认值，调用时必须提供。Qt 对象参数。要确认对象有效、线程归属、所有权和该 API 是否只处理直接子对象。
- 参数 `options`：类型为 `Qt::FindChildOptions`。默认值为 `Qt::FindChildrenRecursively`。传入 `Qt::FindChildOptions` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QLayout::setAlignment(QWidget *w, Qt::Alignment alignment)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setAlignment`。调用它会改变 `QLayout` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`bool`。
- 参数 `w`：类型为 `QWidget *`。没有默认值，调用时必须提供。Qt 对象参数。要确认对象有效、线程归属、所有权和该 API 是否只处理直接子对象。
- 参数 `alignment`：类型为 `Qt::Alignment`。没有默认值，调用时必须提供。对齐标志的组合，例如 `Qt::AlignLeft | Qt::AlignVCenter`；它描述内容在已分配区域中的位置，不负责分配剩余空间。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QLayout::setAlignment(QLayout *l, Qt::Alignment alignment)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setAlignment`。调用它会改变 `QLayout` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`bool`。
- 参数 `l`：类型为 `QLayout *`。没有默认值，调用时必须提供。传入 `QLayout *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `alignment`：类型为 `Qt::Alignment`。没有默认值，调用时必须提供。对齐标志的组合，例如 `Qt::AlignLeft | Qt::AlignVCenter`；它描述内容在已分配区域中的位置，不负责分配剩余空间。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QLayout::setContentsMargins(const QMargins &margins)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setContentsMargins`。调用它会改变 `QLayout` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `margins`：类型为 `const QMargins &`。没有默认值，调用时必须提供。传入 `const QMargins &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QLayout::setContentsMargins(int left, int top, int right, int bottom)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setContentsMargins`。调用它会改变 `QLayout` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `left`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `top`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `right`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `bottom`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QLayout::setEnabled(bool enable)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setEnabled`。调用它会改变 `QLayout` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `enable`：类型为 `bool`。没有默认值，调用时必须提供。传入 `bool` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual] void QLayout::setGeometry(const QRect &r)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setGeometry`。调用它会改变 `QLayout` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `r`：类型为 `const QRect &`。没有默认值，调用时必须提供。传入 `const QRect &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QLayout::setMenuBar(QWidget *widget)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setMenuBar`。调用它会改变 `QLayout` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `widget`：类型为 `QWidget *`。没有默认值，调用时必须提供。参与操作的 QWidget。要确认它是否为空、是否已被其他布局/容器管理，以及函数是否只查找直接子项。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.10] void QLayout::setSizeConstraints(QLayout::SizeConstraint horizontal, QLayout::SizeConstraint vertical)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setSizeConstraints`。调用它会改变 `QLayout` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `horizontal`：类型为 `QLayout::SizeConstraint`。没有默认值，调用时必须提供。传入 `QLayout::SizeConstraint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `vertical`：类型为 `QLayout::SizeConstraint`。没有默认值，调用时必须提供。传入 `QLayout::SizeConstraint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[pure virtual] QLayoutItem *QLayout::takeAt(int index)`

**API 类别：** 成员函数说明

**中文解读：** `QLayout::takeAt` 用于计算、查询或取得与“取出、按位置访问”相关的操作。调用时要先确认当前状态和 `index` 的有效范围；返回类型是 `QLayoutItem *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QLayoutItem *`。
- 参数 `index`：类型为 `int`。没有默认值，调用时必须提供。项目或数据索引。先确认索引基于 0 还是 1、是否允许越界/负数，以及调用后索引是否仍然有效。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.1] void QLayout::unsetContentsMargins()`

**API 类别：** 成员函数说明

**中文解读：** `QLayout::unsetContentsMargins` 用于执行与“unset、Contents、Margins”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QLayout::update()`

**API 类别：** 成员函数说明

**中文解读：** `QLayout::update` 用于执行与“更新”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QLayout::SizeConstraint horizontalSizeConstraint() const`

**API 类别：** 公有函数

**中文解读：** `QLayout::horizontalSizeConstraint` 用于计算、查询或取得与“水平、尺寸或数量、Constraint”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QLayout::SizeConstraint`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QLayout::SizeConstraint`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void setHorizontalSizeConstraint(QLayout::SizeConstraint constraint)`

**API 类别：** 公有函数

**中文解读：** 这是配置/写入操作 `setHorizontalSizeConstraint`。调用它会改变 `QLayout` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `constraint`：类型为 `QLayout::SizeConstraint`。没有默认值，调用时必须提供。传入 `QLayout::SizeConstraint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void setSizeConstraint(QLayout::SizeConstraint constraint)`

**API 类别：** 公有函数

**中文解读：** 这是配置/写入操作 `setSizeConstraint`。调用它会改变 `QLayout` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `constraint`：类型为 `QLayout::SizeConstraint`。没有默认值，调用时必须提供。传入 `QLayout::SizeConstraint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `virtual void setSpacing(int)`

**API 类别：** 公有函数

**中文解读：** 这是配置/写入操作 `setSpacing`。调用它会改变 `QLayout` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `int`：类型为 `未标注`。没有默认值，调用时必须提供。传入 `对应类型` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 与 `setContentsMargins()` 配合控制内部间隔和外部边距，不能用一个替代另一个。

### `void setVerticalSizeConstraint(QLayout::SizeConstraint constraint)`

**API 类别：** 公有函数

**中文解读：** 这是配置/写入操作 `setVerticalSizeConstraint`。调用它会改变 `QLayout` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `constraint`：类型为 `QLayout::SizeConstraint`。没有默认值，调用时必须提供。传入 `QLayout::SizeConstraint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QLayout::SizeConstraint sizeConstraint() const`

**API 类别：** 公有函数

**中文解读：** `QLayout::sizeConstraint` 用于计算、查询或取得与“尺寸或数量、Constraint”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QLayout::SizeConstraint`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QLayout::SizeConstraint`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `virtual int spacing() const`

**API 类别：** 公有函数

**中文解读：** `QLayout::spacing` 用于计算、查询或取得与“spacing”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `int`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`int`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QLayout::SizeConstraint verticalSizeConstraint() const`

**API 类别：** 公有函数

**中文解读：** `QLayout::verticalSizeConstraint` 用于计算、查询或取得与“垂直、尺寸或数量、Constraint”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QLayout::SizeConstraint`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QLayout::SizeConstraint`。
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

`QLayout` 所属机制类型：布局管理机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
