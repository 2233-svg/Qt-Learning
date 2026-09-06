# QPageLayout

> Qt 6.11.1 · Qt GUI

## 1. 先建立直觉

**一句话定位：** `QPageLayout` 是 Qt Widgets 界面机制 中的类型，负责把这一机制中的数据、状态或资源交给其他 Qt 对象使用。

**模块背景：** Qt GUI 负责窗口系统集成、绘制、颜色、字体、图像、输入事件和底层 GUI 资源。

### 这是什么

`QPageLayout` 是 Qt Widgets 界面机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** Widgets 通过父子控件树、布局系统、事件分发和重绘请求组成界面。控件的可见区域、sizeHint、sizePolicy、字体和平台 style 共同影响最终几何；用户输入先进入 Qt 事件系统，再由控件的事件函数、信号或快捷键处理。

**适用场景：** 创建 QApplication 后创建控件，设置 parent 或把控件加入布局，连接用户操作信号，再显示顶层窗口。复合界面用布局嵌套；控件尺寸异常时同时检查 sizePolicy、minimum/maximum size、layout stretch、margins 和 spacing。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要用固定坐标拼接响应式界面；不要给已经加入布局的控件反复 `setGeometry()`；不要在 `paintEvent()` 中修改业务状态；不要忘记窗口关闭、对象销毁和应用退出是三个不同事件。

## 2. 依赖与对象关系

- 头文件：`#include <QPageLayout>`
- 继承自：未在类页中列出
- 直接派生类：未在类页中列出

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Gui)
target_link_libraries(mytarget PRIVATE Qt6::Gui)
```

**继承带来的规则：** 它是值类型或不直接使用 QObject 对象模型，重点放在数据语义、拷贝/移动成本和参数有效性。

### 工作机制

Widgets 通过父子控件树、布局系统、事件分发和重绘请求组成界面。控件的可见区域、sizeHint、sizePolicy、字体和平台 style 共同影响最终几何；用户输入先进入 Qt 事件系统，再由控件的事件函数、信号或快捷键处理。

### 状态、生命周期和线程

**生命周期：** 控件有 parent 时通常由父控件管理销毁；顶层窗口可以放在栈上，也可以由应用对象或业务对象持有。隐藏控件仍然存在，关闭窗口也不一定等于删除对象或退出应用，必须明确 `WA_DeleteOnClose`、parent 和应用退出策略。

**状态与结果：** 控件状态由属性、焦点、启用/禁用、可见性、选择状态和模型数据共同决定。改变属性可能触发重新布局或重绘；需要刷新界面时通常调用 `update()`，需要重新计算几何时让布局系统处理，不要直接调用 `paintEvent()`。

**线程与事件循环：** 所有 QWidget 的创建、访问、布局和绘制都应在 GUI 线程完成。后台线程通过信号把结果投递回来；不要从 worker 线程直接修改控件，也不要在 GUI 线程用 `waitFor...` 或长循环阻塞事件循环。

## 3. 直接使用

创建 QApplication 后创建控件，设置 parent 或把控件加入布局，连接用户操作信号，再显示顶层窗口。复合界面用布局嵌套；控件尺寸异常时同时检查 sizePolicy、minimum/maximum size、layout stretch、margins 和 spacing。 使用时通常按这个过程组织：准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 公有类型

- `enum Mode { StandardMode, FullPageMode }`
- `enum Orientation { Portrait, Landscape }`
- `(since 6.8) enum class OutOfBoundsPolicy { Reject, Clamp }`
- `enum Unit { Millimeter, Point, Inch, Pica, Didot, Cicero }`

### 公有函数

- `QPageLayout()`
- `QPageLayout(const QPageSize &pageSize, QPageLayout::Orientation orientation, const QMarginsF &margins, QPageLayout::Unit units = Point, const QMarginsF &minMargins = QMarginsF(0, 0, 0, 0))`
- `QPageLayout(const QPageLayout &other)`
- `~QPageLayout()`
- `QRectF fullRect() const`
- `QRectF fullRect(QPageLayout::Unit units) const`
- `QRect fullRectPixels(int resolution) const`
- `QRect fullRectPoints() const`
- `bool isEquivalentTo(const QPageLayout &other) const`
- `bool isValid() const`
- `QMarginsF margins() const`
- `QMarginsF margins(QPageLayout::Unit units) const`
- `QMargins marginsPixels(int resolution) const`
- `QMargins marginsPoints() const`
- `QMarginsF maximumMargins() const`
- `QMarginsF minimumMargins() const`
- `QPageLayout::Mode mode() const`
- `QPageLayout::Orientation orientation() const`
- `QPageSize pageSize() const`
- `QRectF paintRect() const`
- `QRectF paintRect(QPageLayout::Unit units) const`
- `QRect paintRectPixels(int resolution) const`
- `QRect paintRectPoints() const`
- `bool setBottomMargin(qreal bottomMargin, QPageLayout::OutOfBoundsPolicy outOfBoundsPolicy = OutOfBoundsPolicy::Reject)`
- `bool setLeftMargin(qreal leftMargin, QPageLayout::OutOfBoundsPolicy outOfBoundsPolicy = OutOfBoundsPolicy::Reject)`
- `bool setMargins(const QMarginsF &margins, QPageLayout::OutOfBoundsPolicy outOfBoundsPolicy = OutOfBoundsPolicy::Reject)`
- `void setMinimumMargins(const QMarginsF &minMargins)`
- `void setMode(QPageLayout::Mode mode)`
- `void setOrientation(QPageLayout::Orientation orientation)`
- `void setPageSize(const QPageSize &pageSize, const QMarginsF &minMargins = QMarginsF(0, 0, 0, 0))`
- `bool setRightMargin(qreal rightMargin, QPageLayout::OutOfBoundsPolicy outOfBoundsPolicy = OutOfBoundsPolicy::Reject)`
- `bool setTopMargin(qreal topMargin, QPageLayout::OutOfBoundsPolicy outOfBoundsPolicy = OutOfBoundsPolicy::Reject)`
- `void setUnits(QPageLayout::Unit units)`
- `void swap(QPageLayout &other)`
- `QPageLayout::Unit units() const`
- `QPageLayout & operator=(QPageLayout &&other)`
- `QPageLayout & operator=(const QPageLayout &other)`

### 相关非成员函数

- `bool operator!=(const QPageLayout &lhs, const QPageLayout &rhs)`
- `bool operator==(const QPageLayout &lhs, const QPageLayout &rhs)`

## 5. API 逐个说明

这里直接说明每个公开成员解决什么问题、参数代表什么、返回什么、会改变什么以及使用时容易出现什么问题。每一个公开签名都会有对应的中文解释。

本类共整理 43 个公开成员条目；没有独立长描述的 API 也会根据签名、类型和所属机制给出使用说明。

### `enum QPageLayout::Mode`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QPageLayout` 暴露的类型声明 `模式`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 属性类型：`:Mode`。
- 属性名：`QPageLayout`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `enum QPageLayout::Orientation`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QPageLayout` 暴露的类型声明 `Orientation`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 属性类型：`:Orientation`。
- 属性名：`QPageLayout`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.8] enum class QPageLayout::OutOfBoundsPolicy`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QPageLayout` 暴露的类型声明 `class`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 属性类型：`:OutOfBoundsPolicy`。
- 属性名：`QPageLayout`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `enum QPageLayout::Unit`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QPageLayout` 暴露的类型声明 `Unit`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 属性类型：`:Unit`。
- 属性名：`QPageLayout`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QPageLayout::QPageLayout()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QPageLayout` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QPageLayout::QPageLayout(const QPageSize &pageSize, QPageLayout::Orientation orientation, const QMarginsF &margins, QPageLayout::Unit units = Point, const QMarginsF &minMargins = QMarginsF(0, 0, 0, 0))`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QPageLayout` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `pageSize`：类型为 `const QPageSize &`。没有默认值，调用时必须提供。传入 `const QPageSize &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `orientation`：类型为 `QPageLayout::Orientation`。没有默认值，调用时必须提供。传入 `QPageLayout::Orientation` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `margins`：类型为 `const QMarginsF &`。没有默认值，调用时必须提供。传入 `const QMarginsF &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `units`：类型为 `QPageLayout::Unit`。默认值为 `Point`。传入 `QPageLayout::Unit` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `minMargins`：类型为 `const QMarginsF &`。默认值为 `QMarginsF(0, 0, 0, 0)`。传入 `const QMarginsF &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QPageLayout::QPageLayout(const QPageLayout &other)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QPageLayout` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `other`：类型为 `const QPageLayout &`。没有默认值，调用时必须提供。参与比较、合并或交换的另一个对象；要确认它与当前对象属于同一类型或兼容协议。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] QPageLayout::~QPageLayout()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QPageLayout` 的析构函数。对象销毁时资源、子对象和连接会按 Qt 规则释放；异步对象要先停止任务或使用 deleteLater，避免回调访问已经不存在的实例。

**签名拆解：**

- 返回值：析构函数，无返回值。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QRectF QPageLayout::fullRect() const`

**API 类别：** 成员函数说明

**中文解读：** `QPageLayout::fullRect` 用于计算、查询或取得与“full、Rect”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QRectF`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QRectF`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QRectF QPageLayout::fullRect(QPageLayout::Unit units) const`

**API 类别：** 成员函数说明

**中文解读：** `QPageLayout::fullRect` 用于计算、查询或取得与“full、Rect”相关的操作。调用时要先确认当前状态和 `units` 的有效范围；返回类型是 `QRectF`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QRectF`。
- 参数 `units`：类型为 `QPageLayout::Unit`。没有默认值，调用时必须提供。传入 `QPageLayout::Unit` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QRect QPageLayout::fullRectPixels(int resolution) const`

**API 类别：** 成员函数说明

**中文解读：** `QPageLayout::fullRectPixels` 用于计算、查询或取得与“full、Rect、Pixels”相关的操作。调用时要先确认当前状态和 `resolution` 的有效范围；返回类型是 `QRect`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QRect`。
- 参数 `resolution`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QRect QPageLayout::fullRectPoints() const`

**API 类别：** 成员函数说明

**中文解读：** `QPageLayout::fullRectPoints` 用于计算、查询或取得与“full、Rect、Points”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QRect`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QRect`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QPageLayout::isEquivalentTo(const QPageLayout &other) const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `isEquivalentTo`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数 `other`：类型为 `const QPageLayout &`。没有默认值，调用时必须提供。参与比较、合并或交换的另一个对象；要确认它与当前对象属于同一类型或兼容协议。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QPageLayout::isValid() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `isValid`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QMarginsF QPageLayout::margins() const`

**API 类别：** 成员函数说明

**中文解读：** `QPageLayout::margins` 用于计算、查询或取得与“margins”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QMarginsF`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QMarginsF`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QMarginsF QPageLayout::margins(QPageLayout::Unit units) const`

**API 类别：** 成员函数说明

**中文解读：** `QPageLayout::margins` 用于计算、查询或取得与“margins”相关的操作。调用时要先确认当前状态和 `units` 的有效范围；返回类型是 `QMarginsF`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QMarginsF`。
- 参数 `units`：类型为 `QPageLayout::Unit`。没有默认值，调用时必须提供。传入 `QPageLayout::Unit` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QMargins QPageLayout::marginsPixels(int resolution) const`

**API 类别：** 成员函数说明

**中文解读：** `QPageLayout::marginsPixels` 用于计算、查询或取得与“margins、Pixels”相关的操作。调用时要先确认当前状态和 `resolution` 的有效范围；返回类型是 `QMargins`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QMargins`。
- 参数 `resolution`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QMargins QPageLayout::marginsPoints() const`

**API 类别：** 成员函数说明

**中文解读：** `QPageLayout::marginsPoints` 用于计算、查询或取得与“margins、Points”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QMargins`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QMargins`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QMarginsF QPageLayout::maximumMargins() const`

**API 类别：** 成员函数说明

**中文解读：** `QPageLayout::maximumMargins` 用于计算、查询或取得与“最大值、Margins”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QMarginsF`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QMarginsF`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QMarginsF QPageLayout::minimumMargins() const`

**API 类别：** 成员函数说明

**中文解读：** `QPageLayout::minimumMargins` 用于计算、查询或取得与“最小值、Margins”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QMarginsF`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QMarginsF`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QPageLayout::Mode QPageLayout::mode() const`

**API 类别：** 成员函数说明

**中文解读：** `QPageLayout::mode` 用于计算、查询或取得与“模式”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QPageLayout::Mode`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QPageLayout::Mode`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QPageLayout::Orientation QPageLayout::orientation() const`

**API 类别：** 成员函数说明

**中文解读：** `QPageLayout::orientation` 用于计算、查询或取得与“orientation”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QPageLayout::Orientation`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QPageLayout::Orientation`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QPageSize QPageLayout::pageSize() const`

**API 类别：** 成员函数说明

**中文解读：** `QPageLayout::pageSize` 用于计算、查询或取得与“page、尺寸或数量”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QPageSize`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QPageSize`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QRectF QPageLayout::paintRect() const`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QPageLayout` 的核心操作 `paintRect`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`QRectF`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QRectF QPageLayout::paintRect(QPageLayout::Unit units) const`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QPageLayout` 的核心操作 `paintRect`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`QRectF`。
- 参数 `units`：类型为 `QPageLayout::Unit`。没有默认值，调用时必须提供。传入 `QPageLayout::Unit` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QRect QPageLayout::paintRectPixels(int resolution) const`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QPageLayout` 的核心操作 `paintRectPixels`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`QRect`。
- 参数 `resolution`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QRect QPageLayout::paintRectPoints() const`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QPageLayout` 的核心操作 `paintRectPoints`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`QRect`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QPageLayout::setBottomMargin(qreal bottomMargin, QPageLayout::OutOfBoundsPolicy outOfBoundsPolicy = OutOfBoundsPolicy::Reject)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setBottomMargin`。调用它会改变 `QPageLayout` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`bool`。
- 参数 `bottomMargin`：类型为 `qreal`。没有默认值，调用时必须提供。传入 `qreal` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `outOfBoundsPolicy`：类型为 `QPageLayout::OutOfBoundsPolicy`。默认值为 `OutOfBoundsPolicy::Reject`。传入 `QPageLayout::OutOfBoundsPolicy` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QPageLayout::setLeftMargin(qreal leftMargin, QPageLayout::OutOfBoundsPolicy outOfBoundsPolicy = OutOfBoundsPolicy::Reject)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setLeftMargin`。调用它会改变 `QPageLayout` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`bool`。
- 参数 `leftMargin`：类型为 `qreal`。没有默认值，调用时必须提供。传入 `qreal` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `outOfBoundsPolicy`：类型为 `QPageLayout::OutOfBoundsPolicy`。默认值为 `OutOfBoundsPolicy::Reject`。传入 `QPageLayout::OutOfBoundsPolicy` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QPageLayout::setMargins(const QMarginsF &margins, QPageLayout::OutOfBoundsPolicy outOfBoundsPolicy = OutOfBoundsPolicy::Reject)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setMargins`。调用它会改变 `QPageLayout` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`bool`。
- 参数 `margins`：类型为 `const QMarginsF &`。没有默认值，调用时必须提供。传入 `const QMarginsF &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `outOfBoundsPolicy`：类型为 `QPageLayout::OutOfBoundsPolicy`。默认值为 `OutOfBoundsPolicy::Reject`。传入 `QPageLayout::OutOfBoundsPolicy` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QPageLayout::setMinimumMargins(const QMarginsF &minMargins)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setMinimumMargins`。调用它会改变 `QPageLayout` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `minMargins`：类型为 `const QMarginsF &`。没有默认值，调用时必须提供。传入 `const QMarginsF &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QPageLayout::setMode(QPageLayout::Mode mode)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setMode`。调用它会改变 `QPageLayout` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `mode`：类型为 `QPageLayout::Mode`。没有默认值，调用时必须提供。模式枚举或位标志。它通常决定对象后续允许的操作和状态转换。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QPageLayout::setOrientation(QPageLayout::Orientation orientation)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setOrientation`。调用它会改变 `QPageLayout` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `orientation`：类型为 `QPageLayout::Orientation`。没有默认值，调用时必须提供。传入 `QPageLayout::Orientation` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QPageLayout::setPageSize(const QPageSize &pageSize, const QMarginsF &minMargins = QMarginsF(0, 0, 0, 0))`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setPageSize`。调用它会改变 `QPageLayout` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `pageSize`：类型为 `const QPageSize &`。没有默认值，调用时必须提供。传入 `const QPageSize &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `minMargins`：类型为 `const QMarginsF &`。默认值为 `QMarginsF(0, 0, 0, 0)`。传入 `const QMarginsF &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QPageLayout::setRightMargin(qreal rightMargin, QPageLayout::OutOfBoundsPolicy outOfBoundsPolicy = OutOfBoundsPolicy::Reject)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setRightMargin`。调用它会改变 `QPageLayout` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`bool`。
- 参数 `rightMargin`：类型为 `qreal`。没有默认值，调用时必须提供。传入 `qreal` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `outOfBoundsPolicy`：类型为 `QPageLayout::OutOfBoundsPolicy`。默认值为 `OutOfBoundsPolicy::Reject`。传入 `QPageLayout::OutOfBoundsPolicy` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QPageLayout::setTopMargin(qreal topMargin, QPageLayout::OutOfBoundsPolicy outOfBoundsPolicy = OutOfBoundsPolicy::Reject)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setTopMargin`。调用它会改变 `QPageLayout` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`bool`。
- 参数 `topMargin`：类型为 `qreal`。没有默认值，调用时必须提供。传入 `qreal` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `outOfBoundsPolicy`：类型为 `QPageLayout::OutOfBoundsPolicy`。默认值为 `OutOfBoundsPolicy::Reject`。传入 `QPageLayout::OutOfBoundsPolicy` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QPageLayout::setUnits(QPageLayout::Unit units)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setUnits`。调用它会改变 `QPageLayout` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `units`：类型为 `QPageLayout::Unit`。没有默认值，调用时必须提供。传入 `QPageLayout::Unit` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] void QPageLayout::swap(QPageLayout &other)`

**API 类别：** 成员函数说明

**中文解读：** `QPageLayout::swap` 用于执行与“swap”相关的操作。调用时要先确认当前状态和 `other` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `other`：类型为 `QPageLayout &`。没有默认值，调用时必须提供。参与比较、合并或交换的另一个对象；要确认它与当前对象属于同一类型或兼容协议。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QPageLayout::Unit QPageLayout::units() const`

**API 类别：** 成员函数说明

**中文解读：** `QPageLayout::units` 用于计算、查询或取得与“units”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QPageLayout::Unit`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QPageLayout::Unit`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] QPageLayout &QPageLayout::operator=(QPageLayout &&other)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QPageLayout` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QPageLayout &`。
- 参数 `other`：类型为 `QPageLayout &&`。没有默认值，调用时必须提供。参与比较、合并或交换的另一个对象；要确认它与当前对象属于同一类型或兼容协议。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QPageLayout &QPageLayout::operator=(const QPageLayout &other)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QPageLayout` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QPageLayout &`。
- 参数 `other`：类型为 `const QPageLayout &`。没有默认值，调用时必须提供。参与比较、合并或交换的另一个对象；要确认它与当前对象属于同一类型或兼容协议。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool operator!=(const QPageLayout &lhs, const QPageLayout &rhs)`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QPageLayout` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`bool`。
- 参数 `lhs`：类型为 `const QPageLayout &`。没有默认值，调用时必须提供。运算符左侧的值；要注意返回新值还是修改当前对象。
- 参数 `rhs`：类型为 `const QPageLayout &`。没有默认值，调用时必须提供。运算符右侧的另一个值；通常不会被当前 API 接管所有权。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool operator==(const QPageLayout &lhs, const QPageLayout &rhs)`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QPageLayout` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`bool`。
- 参数 `lhs`：类型为 `const QPageLayout &`。没有默认值，调用时必须提供。运算符左侧的值；要注意返回新值还是修改当前对象。
- 参数 `rhs`：类型为 `const QPageLayout &`。没有默认值，调用时必须提供。运算符右侧的另一个值；通常不会被当前 API 接管所有权。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

## 6. 深入实践与常见坑

### 生命周期和资源边界

控件有 parent 时通常由父控件管理销毁；顶层窗口可以放在栈上，也可以由应用对象或业务对象持有。隐藏控件仍然存在，关闭窗口也不一定等于删除对象或退出应用，必须明确 `WA_DeleteOnClose`、parent 和应用退出策略。

### 状态和错误边界

控件状态由属性、焦点、启用/禁用、可见性、选择状态和模型数据共同决定。改变属性可能触发重新布局或重绘；需要刷新界面时通常调用 `update()`，需要重新计算几何时让布局系统处理，不要直接调用 `paintEvent()`。

### 线程边界

所有 QWidget 的创建、访问、布局和绘制都应在 GUI 线程完成。后台线程通过信号把结果投递回来；不要从 worker 线程直接修改控件，也不要在 GUI 线程用 `waitFor...` 或长循环阻塞事件循环。

### 最容易出现的错误

不要用固定坐标拼接响应式界面；不要给已经加入布局的控件反复 `setGeometry()`；不要在 `paintEvent()` 中修改业务状态；不要忘记窗口关闭、对象销毁和应用退出是三个不同事件。

### 版本和平台

本文档以 Qt 6.11.1 为依据。涉及平台后端、编解码器、数据库驱动、窗口风格、编译器特性或标注了版本号的 API 时，要把版本条件当作使用约束，而不是只看函数是否能补全。

## 7. 使用边界

`QPageLayout` 所属机制类型：Qt Widgets 界面机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
