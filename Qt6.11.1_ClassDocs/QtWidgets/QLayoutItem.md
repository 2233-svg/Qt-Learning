# QLayoutItem

> Qt 6.11.1 · Qt Widgets

## 1. 先建立直觉

**一句话定位：** `QLayoutItem` 是 布局管理机制 中的类型，负责把这一机制中的数据、状态或资源交给其他 Qt 对象使用。

**模块背景：** Qt Widgets 提供传统桌面应用的控件、布局、模型/视图、窗口和交互组件。

### 这是什么

`QLayoutItem` 是 Qt Widgets 界面体系中的组件，负责一段可见 UI 或交互行为。

**内部模型：** 先区分它是顶层窗口、容器、输入控件、显示控件还是视图；再理解 parent、layout、model、signals 和事件之间的关系。

**适用场景：** 需要桌面控件、布局、用户输入、选择或模型/视图展示时使用。

**典型调用链：** 创建并设置 parent -> 配置属性和布局 -> connect 用户动作信号 -> show -> 按需处理事件/更新状态。

**先记住的坑：** 优先用 layout 管理几何；控件只能在 GUI 线程访问；自定义绘制放在 paintEvent；不要阻塞信号槽回调。

## 2. 依赖与对象关系

- 头文件：`#include <QLayoutItem>`
- 继承自：未在类页中列出
- 直接派生类：QLayout、QSpacerItem,、QWidgetItem

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

- `QLayoutItem(Qt::Alignment alignment = Qt::Alignment())`
- `virtual ~QLayoutItem()`
- `Qt::Alignment alignment() const`
- `virtual QSizePolicy::ControlTypes controlTypes() const`
- `virtual Qt::Orientations expandingDirections() const = 0`
- `virtual QRect geometry() const = 0`
- `virtual bool hasHeightForWidth() const`
- `virtual int heightForWidth(int) const`
- `virtual void invalidate()`
- `virtual bool isEmpty() const = 0`
- `virtual QLayout * layout()`
- `virtual QSize maximumSize() const = 0`
- `virtual int minimumHeightForWidth(int w) const`
- `virtual QSize minimumSize() const = 0`
- `void setAlignment(Qt::Alignment alignment)`
- `virtual void setGeometry(const QRect &r) = 0`
- `virtual QSize sizeHint() const = 0`
- `virtual QSpacerItem * spacerItem()`
- `virtual QWidget * widget() const`

## 5. API 逐个说明

这里直接说明每个公开成员解决什么问题、参数代表什么、返回什么、会改变什么以及使用时容易出现什么问题。每一个公开签名都会有对应的中文解释。

本类共整理 19 个公开成员条目；没有独立长描述的 API 也会根据签名、类型和所属机制给出使用说明。

### `[explicit] QLayoutItem::QLayoutItem(Qt::Alignment alignment = Qt::Alignment())`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QLayoutItem` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `alignment`：类型为 `Qt::Alignment`。默认值为 `Qt::Alignment()`。对齐标志的组合，例如 `Qt::AlignLeft | Qt::AlignVCenter`；它描述内容在已分配区域中的位置，不负责分配剩余空间。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual noexcept] QLayoutItem::~QLayoutItem()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QLayoutItem` 的析构函数。对象销毁时资源、子对象和连接会按 Qt 规则释放；异步对象要先停止任务或使用 deleteLater，避免回调访问已经不存在的实例。

**签名拆解：**

- 返回值：析构函数，无返回值。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `Qt::Alignment QLayoutItem::alignment() const`

**API 类别：** 成员函数说明

**中文解读：** `QLayoutItem::alignment` 用于计算、查询或取得与“对齐方式”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `Qt::Alignment`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`Qt::Alignment`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual] QSizePolicy::ControlTypes QLayoutItem::controlTypes() const`

**API 类别：** 成员函数说明

**中文解读：** `QLayoutItem::controlTypes` 用于计算、查询或取得与“control、Types”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QSizePolicy::ControlTypes`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QSizePolicy::ControlTypes`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[pure virtual] Qt::Orientations QLayoutItem::expandingDirections() const`

**API 类别：** 成员函数说明

**中文解读：** `QLayoutItem::expandingDirections` 用于计算、查询或取得与“expanding、Directions”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `Qt::Orientations`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`Qt::Orientations`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[pure virtual] QRect QLayoutItem::geometry() const`

**API 类别：** 成员函数说明

**中文解读：** `QLayoutItem::geometry` 用于计算、查询或取得与“几何区域”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QRect`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QRect`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual] bool QLayoutItem::hasHeightForWidth() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `hasHeightForWidth`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual] int QLayoutItem::heightForWidth(int) const`

**API 类别：** 成员函数说明

**中文解读：** `QLayoutItem::heightForWidth` 用于计算、查询或取得与“高度、For、宽度”相关的操作。调用时要先确认当前状态和 `int` 的有效范围；返回类型是 `int`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`int`。
- 参数 `int`：类型为 `未标注`。没有默认值，调用时必须提供。传入 `对应类型` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual] void QLayoutItem::invalidate()`

**API 类别：** 成员函数说明

**中文解读：** 这是状态清理或重置 API `invalidate`。调用后原有数据、索引、缓存或绑定可能失效；使用前先确认它影响的是当前对象、子对象还是底层共享资源，之后重新检查状态。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[pure virtual] bool QLayoutItem::isEmpty() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `isEmpty`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual] QLayout *QLayoutItem::layout()`

**API 类别：** 成员函数说明

**中文解读：** `QLayoutItem::layout` 用于计算、查询或取得与“layout”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QLayout *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QLayout *`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[pure virtual] QSize QLayoutItem::maximumSize() const`

**API 类别：** 成员函数说明

**中文解读：** `QLayoutItem::maximumSize` 用于计算、查询或取得与“最大值、尺寸或数量”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QSize`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QSize`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual] int QLayoutItem::minimumHeightForWidth(int w) const`

**API 类别：** 成员函数说明

**中文解读：** `QLayoutItem::minimumHeightForWidth` 用于计算、查询或取得与“最小值、高度、For、宽度”相关的操作。调用时要先确认当前状态和 `w` 的有效范围；返回类型是 `int`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`int`。
- 参数 `w`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[pure virtual] QSize QLayoutItem::minimumSize() const`

**API 类别：** 成员函数说明

**中文解读：** `QLayoutItem::minimumSize` 用于计算、查询或取得与“最小值、尺寸或数量”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QSize`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QSize`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QLayoutItem::setAlignment(Qt::Alignment alignment)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setAlignment`。调用它会改变 `QLayoutItem` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `alignment`：类型为 `Qt::Alignment`。没有默认值，调用时必须提供。对齐标志的组合，例如 `Qt::AlignLeft | Qt::AlignVCenter`；它描述内容在已分配区域中的位置，不负责分配剩余空间。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[pure virtual] void QLayoutItem::setGeometry(const QRect &r)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setGeometry`。调用它会改变 `QLayoutItem` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `r`：类型为 `const QRect &`。没有默认值，调用时必须提供。传入 `const QRect &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[pure virtual] QSize QLayoutItem::sizeHint() const`

**API 类别：** 成员函数说明

**中文解读：** `QLayoutItem::sizeHint` 用于计算、查询或取得与“尺寸或数量、Hint”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QSize`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QSize`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual] QSpacerItem *QLayoutItem::spacerItem()`

**API 类别：** 成员函数说明

**中文解读：** `QLayoutItem::spacerItem` 用于计算、查询或取得与“spacer、项目访问”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QSpacerItem *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QSpacerItem *`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual] QWidget *QLayoutItem::widget() const`

**API 类别：** 成员函数说明

**中文解读：** `QLayoutItem::widget` 用于计算、查询或取得与“widget”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QWidget *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QWidget *`。
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

`QLayoutItem` 所属机制类型：布局管理机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
