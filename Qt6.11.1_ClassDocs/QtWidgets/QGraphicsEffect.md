# QGraphicsEffect

> Qt 6.11.1 · Qt Widgets

## 1. 先建立直觉

**一句话定位：** `QGraphicsEffect` 是 图形场景与项目机制 中的类型，负责把这一机制中的数据、状态或资源交给其他 Qt 对象使用。

**模块背景：** Qt Widgets 提供传统桌面应用的控件、布局、模型/视图、窗口和交互组件。

### 这是什么

`QGraphicsEffect` 是 Qt Widgets 界面体系中的组件，负责一段可见 UI 或交互行为。

**内部模型：** 先区分它是顶层窗口、容器、输入控件、显示控件还是视图；再理解 parent、layout、model、signals 和事件之间的关系。

**适用场景：** 需要桌面控件、布局、用户输入、选择或模型/视图展示时使用。

**典型调用链：** 创建并设置 parent -> 配置属性和布局 -> connect 用户动作信号 -> show -> 按需处理事件/更新状态。

**先记住的坑：** 优先用 layout 管理几何；控件只能在 GUI 线程访问；自定义绘制放在 paintEvent；不要阻塞信号槽回调。

## 2. 依赖与对象关系

- 头文件：`#include <QGraphicsEffect>`
- 继承自：QObject
- 直接派生类：QGraphicsBlurEffect、QGraphicsColorizeEffect、QGraphicsDropShadowEffect,、QGraphicsOpacityEffect

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

### 公有类型

- `enum ChangeFlag { SourceAttached, SourceDetached, SourceBoundingRectChanged, SourceInvalidated }`
- `flags ChangeFlags`
- `enum PixmapPadMode { NoPad, PadToTransparentBorder, PadToEffectiveBoundingRect }`

### 属性

- `enabled : bool`

### 公有函数

- `QGraphicsEffect(QObject *parent = nullptr)`
- `virtual ~QGraphicsEffect()`
- `QRectF boundingRect() const`
- `virtual QRectF boundingRectFor(const QRectF &rect) const`
- `bool isEnabled() const`

### 公有槽函数

- `void setEnabled(bool enable)`
- `void update()`

### 信号

- `void enabledChanged(bool enabled)`

### 保护函数

- `virtual void draw(QPainter *painter) = 0`
- `void drawSource(QPainter *painter)`
- `QRectF sourceBoundingRect(Qt::CoordinateSystem system = Qt::LogicalCoordinates) const`
- `virtual void sourceChanged(QGraphicsEffect::ChangeFlags flags)`
- `bool sourceIsPixmap() const`
- `QPixmap sourcePixmap(Qt::CoordinateSystem system = Qt::LogicalCoordinates, QPoint *offset = nullptr, QGraphicsEffect::PixmapPadMode mode = PadToEffectiveBoundingRect) const`
- `void updateBoundingRect()`

## 5. API 逐个说明

这里直接说明每个公开成员解决什么问题、参数代表什么、返回什么、会改变什么以及使用时容易出现什么问题。每一个公开签名都会有对应的中文解释。

本类共整理 20 个公开成员条目；没有独立长描述的 API 也会根据签名、类型和所属机制给出使用说明。

### `enum QGraphicsEffect::ChangeFlagflags QGraphicsEffect::ChangeFlags`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QGraphicsEffect` 暴露的类型声明 `Change、Flagflags`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 属性类型：`:ChangeFlagflags QGraphicsEffect::ChangeFlags`。
- 属性名：`QGraphicsEffect`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `enum QGraphicsEffect::PixmapPadMode`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QGraphicsEffect` 暴露的类型声明 `Pixmap、Pad、模式`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 属性类型：`:PixmapPadMode`。
- 属性名：`QGraphicsEffect`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `enabled : bool`

**API 类别：** 属性说明

**中文解读：** 这是 `QGraphicsEffect` 的配置属性。初始化或状态切换时通过 `setEnabled(...)` 设置，之后用 `enabled()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`bool`。
- 属性名：`enabled`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QGraphicsEffect::QGraphicsEffect(QObject *parent = nullptr)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QGraphicsEffect` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `parent`：类型为 `QObject *`。默认值为 `nullptr`。父对象。设置后通常由父对象负责销毁子对象；只有在对象确实应挂入这棵对象树时才传入。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual noexcept] QGraphicsEffect::~QGraphicsEffect()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QGraphicsEffect` 的析构函数。对象销毁时资源、子对象和连接会按 Qt 规则释放；异步对象要先停止任务或使用 deleteLater，避免回调访问已经不存在的实例。

**签名拆解：**

- 返回值：析构函数，无返回值。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QRectF QGraphicsEffect::boundingRect() const`

**API 类别：** 成员函数说明

**中文解读：** `QGraphicsEffect::boundingRect` 用于计算、查询或取得与“bounding、Rect”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QRectF`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QRectF`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual] QRectF QGraphicsEffect::boundingRectFor(const QRectF &rect) const`

**API 类别：** 成员函数说明

**中文解读：** `QGraphicsEffect::boundingRectFor` 用于计算、查询或取得与“bounding、Rect、For”相关的操作。调用时要先确认当前状态和 `rect` 的有效范围；返回类型是 `QRectF`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QRectF`。
- 参数 `rect`：类型为 `const QRectF &`。没有默认值，调用时必须提供。矩形区域；要确认坐标系、是否包含右下边界以及空矩形的语义。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[pure virtual protected] void QGraphicsEffect::draw(QPainter *painter)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QGraphicsEffect` 的核心操作 `draw`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`void`。
- 参数 `painter`：类型为 `QPainter *`。没有默认值，调用时必须提供。绘制上下文。要确认它已经绑定有效绘制设备，并处于允许绘制的阶段。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[protected] void QGraphicsEffect::drawSource(QPainter *painter)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QGraphicsEffect` 的核心操作 `drawSource`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`void`。
- 参数 `painter`：类型为 `QPainter *`。没有默认值，调用时必须提供。绘制上下文。要确认它已经绑定有效绘制设备，并处于允许绘制的阶段。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[signal] void QGraphicsEffect::enabledChanged(bool enabled)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QGraphicsEffect` 发出的通知信号 `enabledChanged`。应用代码通常只连接它，不直接调用它；信号参数描述发生了什么，槽函数中读取相关状态并尽快返回。异步类的完成、错误和状态变化通常都从信号开始处理。

**签名拆解：**

- 返回值：`void`。
- 参数 `enabled`：类型为 `bool`。没有默认值，调用时必须提供。传入 `bool` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[protected] QRectF QGraphicsEffect::sourceBoundingRect(Qt::CoordinateSystem system = Qt::LogicalCoordinates) const`

**API 类别：** 成员函数说明

**中文解读：** `QGraphicsEffect::sourceBoundingRect` 用于计算、查询或取得与“来源、Bounding、Rect”相关的操作。调用时要先确认当前状态和 `system` 的有效范围；返回类型是 `QRectF`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QRectF`。
- 参数 `system`：类型为 `Qt::CoordinateSystem`。默认值为 `Qt::LogicalCoordinates`。传入 `Qt::CoordinateSystem` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual protected] void QGraphicsEffect::sourceChanged(QGraphicsEffect::ChangeFlags flags)`

**API 类别：** 成员函数说明

**中文解读：** 这是状态变化通知 `sourceChanged`。应用代码通常连接它而不是直接调用它；收到通知后读取当前值并更新依赖对象，不要假设通知一定只发一次或已经代表业务操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `flags`：类型为 `QGraphicsEffect::ChangeFlags`。没有默认值，调用时必须提供。标志位组合。可以用按位或组合，调用前确认哪些标志互斥、哪些标志需要同时出现。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[protected] bool QGraphicsEffect::sourceIsPixmap() const`

**API 类别：** 成员函数说明

**中文解读：** `QGraphicsEffect::sourceIsPixmap` 用于计算、查询或取得与“来源、状态判断、Pixmap”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[protected] QPixmap QGraphicsEffect::sourcePixmap(Qt::CoordinateSystem system = Qt::LogicalCoordinates, QPoint *offset = nullptr, QGraphicsEffect::PixmapPadMode mode = PadToEffectiveBoundingRect) const`

**API 类别：** 成员函数说明

**中文解读：** `QGraphicsEffect::sourcePixmap` 用于计算、查询或取得与“来源、Pixmap”相关的操作。调用时要先确认当前状态和 `system`、`offset`、`mode` 的有效范围；返回类型是 `QPixmap`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QPixmap`。
- 参数 `system`：类型为 `Qt::CoordinateSystem`。默认值为 `Qt::LogicalCoordinates`。传入 `Qt::CoordinateSystem` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `offset`：类型为 `QPoint *`。默认值为 `nullptr`。传入 `QPoint *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `mode`：类型为 `QGraphicsEffect::PixmapPadMode`。默认值为 `PadToEffectiveBoundingRect`。模式枚举或位标志。它通常决定对象后续允许的操作和状态转换。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[slot] void QGraphicsEffect::update()`

**API 类别：** 成员函数说明

**中文解读：** 这是可被信号连接或元对象调用的槽 `update`。它适合作为一次动作或状态响应的入口；如果调用可能耗时，不要直接阻塞 GUI 事件循环，应把工作拆分或移动到 worker。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[protected] void QGraphicsEffect::updateBoundingRect()`

**API 类别：** 成员函数说明

**中文解读：** `QGraphicsEffect::updateBoundingRect` 用于执行与“更新、Bounding、Rect”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `enum ChangeFlag { SourceAttached, SourceDetached, SourceBoundingRectChanged, SourceInvalidated }`

**API 类别：** 公有类型

**中文解读：** 这是 `QGraphicsEffect` 暴露的类型声明 `Change、Flag`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 这是供该类其他 API 使用的枚举/标志类型；传值前要确认枚举值的语义和适用状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `flags ChangeFlags`

**API 类别：** 公有类型

**中文解读：** 这是 `QGraphicsEffect` 的 `标志` 成员声明。它通常作为其他 API 的类型、常量或配置入口使用；先确认可用值和适用状态，再结合本类的创建、核心操作和清理流程使用。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool isEnabled() const`

**API 类别：** 公有函数

**中文解读：** 这是查询 API `isEnabled`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void setEnabled(bool enable)`

**API 类别：** 公有槽函数

**中文解读：** 这是可被信号连接或元对象调用的槽 `setEnabled`。它适合作为一次动作或状态响应的入口；如果调用可能耗时，不要直接阻塞 GUI 事件循环，应把工作拆分或移动到 worker。

**签名拆解：**

- 返回值：`void`。
- 参数 `enable`：类型为 `bool`。没有默认值，调用时必须提供。传入 `bool` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

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

`QGraphicsEffect` 所属机制类型：图形场景与项目机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
