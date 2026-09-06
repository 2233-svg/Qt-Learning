# QPageSize

> Qt 6.11.1 · Qt GUI

## 1. 先建立直觉

**一句话定位：** 这是 GUI 基础类型，常用于绘制、输入、图像、字体或窗口系统集成。

**模块背景：** Qt GUI 负责窗口系统集成、绘制、颜色、字体、图像、输入事件和底层 GUI 资源。

### 这是什么

`QPageSize` 是 Qt 类型机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 这个类的行为由它的继承关系、构造参数、公开状态和成员函数协议共同决定。使用时要把创建、配置、核心操作、结果/通知和清理看成一条闭环，而不是孤立调用某个函数。

**适用场景：** 围绕这个类的核心职责建立最小闭环：准备依赖 -> 创建/取得对象 -> 设置必要配置 -> 调用核心 API -> 检查返回值和状态 -> 处理结果/错误 -> 结束时清理。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要忽略构造失败、空返回、默认值和版本限制；不要把异步 API 当同步 API；不要在没有确认所有权和线程的情况下保存指针或跨线程调用。

## 2. 依赖与对象关系

- 头文件：`#include <QPageSize>`
- 继承自：未在类页中列出
- 直接派生类：未在类页中列出

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Gui)
target_link_libraries(mytarget PRIVATE Qt6::Gui)
```

**继承带来的规则：** 它是值类型或不直接使用 QObject 对象模型，重点放在数据语义、拷贝/移动成本和参数有效性。

### 工作机制

这个类的行为由它的继承关系、构造参数、公开状态和成员函数协议共同决定。使用时要把创建、配置、核心操作、结果/通知和清理看成一条闭环，而不是孤立调用某个函数。

### 状态、生命周期和线程

**生命周期：** 先确认对象是值类型还是 QObject 派生对象，再确定所有权、有效期、拷贝成本和销毁方式。返回的句柄、索引、reply、设备或迭代器可能有独立的有效期，不能只看 C++ 指针是否非空。

**状态与结果：** 把返回值、状态查询、错误信息和通知信号分开判断。调用成功可能只表示请求被接受，真正完成还要等待状态变化或完成信号；读取数据前先检查对象和结果是否有效。

**线程与事件循环：** 如果类型直接或间接参与 QObject、GUI、设备或异步框架，就必须确认线程归属和事件循环；值类型虽然可以复制，也要注意内部指针、共享数据和并发写入。

## 3. 直接使用

围绕这个类的核心职责建立最小闭环：准备依赖 -> 创建/取得对象 -> 设置必要配置 -> 调用核心 API -> 检查返回值和状态 -> 处理结果/错误 -> 结束时清理。 使用时通常按这个过程组织：准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 公有类型

- `enum PageSizeId { A0, A1, A2, A3, A4, …, LastPageSize }`
- `enum SizeMatchPolicy { FuzzyMatch, FuzzyOrientationMatch, ExactMatch }`
- `enum Unit { Millimeter, Point, Inch, Pica, Didot, Cicero }`

### 公有函数

- `QPageSize()`
- `QPageSize(QPageSize::PageSizeId pageSize)`
- `QPageSize(const QSize &pointSize, const QString &name = QString(), QPageSize::SizeMatchPolicy matchPolicy = FuzzyMatch)`
- `QPageSize(const QSizeF &size, QPageSize::Unit units, const QString &name = QString(), QPageSize::SizeMatchPolicy matchPolicy = FuzzyMatch)`
- `QPageSize(const QPageSize &other)`
- `~QPageSize()`
- `QSizeF definitionSize() const`
- `QPageSize::Unit definitionUnits() const`
- `QPageSize::PageSizeId id() const`
- `bool isEquivalentTo(const QPageSize &other) const`
- `bool isValid() const`
- `QString key() const`
- `QString name() const`
- `QRectF rect(QPageSize::Unit units) const`
- `QRect rectPixels(int resolution) const`
- `QRect rectPoints() const`
- `QSizeF size(QPageSize::Unit units) const`
- `QSize sizePixels(int resolution) const`
- `QSize sizePoints() const`
- `void swap(QPageSize &other)`
- `int windowsId() const`
- `QPageSize & operator=(QPageSize &&other)`
- `QPageSize & operator=(const QPageSize &other)`

### 静态公有成员

- `QSizeF definitionSize(QPageSize::PageSizeId pageSizeId)`
- `QPageSize::Unit definitionUnits(QPageSize::PageSizeId pageSizeId)`
- `QPageSize::PageSizeId id(int windowsId)`
- `QPageSize::PageSizeId id(const QSize &pointSize, QPageSize::SizeMatchPolicy matchPolicy = FuzzyMatch)`
- `QPageSize::PageSizeId id(const QSizeF &size, QPageSize::Unit units, QPageSize::SizeMatchPolicy matchPolicy = FuzzyMatch)`
- `QString key(QPageSize::PageSizeId pageSizeId)`
- `QString name(QPageSize::PageSizeId pageSizeId)`
- `QSizeF size(QPageSize::PageSizeId pageSizeId, QPageSize::Unit units)`
- `QSize sizePixels(QPageSize::PageSizeId pageSizeId, int resolution)`
- `QSize sizePoints(QPageSize::PageSizeId pageSizeId)`
- `int windowsId(QPageSize::PageSizeId pageSizeId)`

### 相关非成员函数

- `bool operator!=(const QPageSize &lhs, const QPageSize &rhs)`
- `bool operator==(const QPageSize &lhs, const QPageSize &rhs)`

## 5. API 逐个说明

这里直接说明每个公开成员解决什么问题、参数代表什么、返回什么、会改变什么以及使用时容易出现什么问题。每一个公开签名都会有对应的中文解释。

本类共整理 39 个公开成员条目；没有独立长描述的 API 也会根据签名、类型和所属机制给出使用说明。

### `enum QPageSize::PageSizeId`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QPageSize` 暴露的类型声明 `Page、尺寸或数量、Id`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 属性类型：`:PageSizeId`。
- 属性名：`QPageSize`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `enum QPageSize::Unit`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QPageSize` 暴露的类型声明 `Unit`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 属性类型：`:Unit`。
- 属性名：`QPageSize`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QPageSize::QPageSize()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QPageSize` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QPageSize::QPageSize(QPageSize::PageSizeId pageSize)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QPageSize` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `pageSize`：类型为 `QPageSize::PageSizeId`。没有默认值，调用时必须提供。传入 `QPageSize::PageSizeId` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[explicit] QPageSize::QPageSize(const QSize &pointSize, const QString &name = QString(), QPageSize::SizeMatchPolicy matchPolicy = FuzzyMatch)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QPageSize` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `pointSize`：类型为 `const QSize &`。没有默认值，调用时必须提供。传入 `const QSize &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `name`：类型为 `const QString &`。默认值为 `QString()`。名称或键。通常是稳定的 API/配置标识，不应随意使用显示文本替代。
- 参数 `matchPolicy`：类型为 `QPageSize::SizeMatchPolicy`。默认值为 `FuzzyMatch`。传入 `QPageSize::SizeMatchPolicy` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[explicit] QPageSize::QPageSize(const QSizeF &size, QPageSize::Unit units, const QString &name = QString(), QPageSize::SizeMatchPolicy matchPolicy = FuzzyMatch)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QPageSize` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `size`：类型为 `const QSizeF &`。没有默认值，调用时必须提供。尺寸或长度，单位通常是像素、字节、元素数或时间，必须结合类型和类的上下文确认。
- 参数 `units`：类型为 `QPageSize::Unit`。没有默认值，调用时必须提供。传入 `QPageSize::Unit` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `name`：类型为 `const QString &`。默认值为 `QString()`。名称或键。通常是稳定的 API/配置标识，不应随意使用显示文本替代。
- 参数 `matchPolicy`：类型为 `QPageSize::SizeMatchPolicy`。默认值为 `FuzzyMatch`。传入 `QPageSize::SizeMatchPolicy` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QPageSize::QPageSize(const QPageSize &other)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QPageSize` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `other`：类型为 `const QPageSize &`。没有默认值，调用时必须提供。参与比较、合并或交换的另一个对象；要确认它与当前对象属于同一类型或兼容协议。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] QPageSize::~QPageSize()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QPageSize` 的析构函数。对象销毁时资源、子对象和连接会按 Qt 规则释放；异步对象要先停止任务或使用 deleteLater，避免回调访问已经不存在的实例。

**签名拆解：**

- 返回值：析构函数，无返回值。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QSizeF QPageSize::definitionSize() const`

**API 类别：** 成员函数说明

**中文解读：** `QPageSize::definitionSize` 用于计算、查询或取得与“definition、尺寸或数量”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QSizeF`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QSizeF`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] QSizeF QPageSize::definitionSize(QPageSize::PageSizeId pageSizeId)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `definitionSize`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QSizeF`。
- 参数 `pageSizeId`：类型为 `QPageSize::PageSizeId`。没有默认值，调用时必须提供。传入 `QPageSize::PageSizeId` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QPageSize::Unit QPageSize::definitionUnits() const`

**API 类别：** 成员函数说明

**中文解读：** `QPageSize::definitionUnits` 用于计算、查询或取得与“definition、Units”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QPageSize::Unit`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QPageSize::Unit`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] QPageSize::Unit QPageSize::definitionUnits(QPageSize::PageSizeId pageSizeId)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `definitionUnits`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QPageSize::Unit`。
- 参数 `pageSizeId`：类型为 `QPageSize::PageSizeId`。没有默认值，调用时必须提供。传入 `QPageSize::PageSizeId` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QPageSize::PageSizeId QPageSize::id() const`

**API 类别：** 成员函数说明

**中文解读：** `QPageSize::id` 用于计算、查询或取得与“id”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QPageSize::PageSizeId`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QPageSize::PageSizeId`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] QPageSize::PageSizeId QPageSize::id(int windowsId)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `id`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QPageSize::PageSizeId`。
- 参数 `windowsId`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] QPageSize::PageSizeId QPageSize::id(const QSize &pointSize, QPageSize::SizeMatchPolicy matchPolicy = FuzzyMatch)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `id`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QPageSize::PageSizeId`。
- 参数 `pointSize`：类型为 `const QSize &`。没有默认值，调用时必须提供。传入 `const QSize &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `matchPolicy`：类型为 `QPageSize::SizeMatchPolicy`。默认值为 `FuzzyMatch`。传入 `QPageSize::SizeMatchPolicy` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] QPageSize::PageSizeId QPageSize::id(const QSizeF &size, QPageSize::Unit units, QPageSize::SizeMatchPolicy matchPolicy = FuzzyMatch)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `id`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QPageSize::PageSizeId`。
- 参数 `size`：类型为 `const QSizeF &`。没有默认值，调用时必须提供。尺寸或长度，单位通常是像素、字节、元素数或时间，必须结合类型和类的上下文确认。
- 参数 `units`：类型为 `QPageSize::Unit`。没有默认值，调用时必须提供。传入 `QPageSize::Unit` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `matchPolicy`：类型为 `QPageSize::SizeMatchPolicy`。默认值为 `FuzzyMatch`。传入 `QPageSize::SizeMatchPolicy` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QPageSize::isEquivalentTo(const QPageSize &other) const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `isEquivalentTo`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数 `other`：类型为 `const QPageSize &`。没有默认值，调用时必须提供。参与比较、合并或交换的另一个对象；要确认它与当前对象属于同一类型或兼容协议。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QPageSize::isValid() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `isValid`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString QPageSize::key() const`

**API 类别：** 成员函数说明

**中文解读：** `QPageSize::key` 用于计算、查询或取得与“key”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QString`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QString`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] QString QPageSize::key(QPageSize::PageSizeId pageSizeId)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `key`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QString`。
- 参数 `pageSizeId`：类型为 `QPageSize::PageSizeId`。没有默认值，调用时必须提供。传入 `QPageSize::PageSizeId` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString QPageSize::name() const`

**API 类别：** 成员函数说明

**中文解读：** `QPageSize::name` 用于计算、查询或取得与“名称”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QString`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QString`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] QString QPageSize::name(QPageSize::PageSizeId pageSizeId)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `name`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QString`。
- 参数 `pageSizeId`：类型为 `QPageSize::PageSizeId`。没有默认值，调用时必须提供。传入 `QPageSize::PageSizeId` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QRectF QPageSize::rect(QPageSize::Unit units) const`

**API 类别：** 成员函数说明

**中文解读：** `QPageSize::rect` 用于计算、查询或取得与“rect”相关的操作。调用时要先确认当前状态和 `units` 的有效范围；返回类型是 `QRectF`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QRectF`。
- 参数 `units`：类型为 `QPageSize::Unit`。没有默认值，调用时必须提供。传入 `QPageSize::Unit` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QRect QPageSize::rectPixels(int resolution) const`

**API 类别：** 成员函数说明

**中文解读：** `QPageSize::rectPixels` 用于计算、查询或取得与“rect、Pixels”相关的操作。调用时要先确认当前状态和 `resolution` 的有效范围；返回类型是 `QRect`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QRect`。
- 参数 `resolution`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QRect QPageSize::rectPoints() const`

**API 类别：** 成员函数说明

**中文解读：** `QPageSize::rectPoints` 用于计算、查询或取得与“rect、Points”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QRect`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QRect`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QSizeF QPageSize::size(QPageSize::Unit units) const`

**API 类别：** 成员函数说明

**中文解读：** 这是尺寸/数量查询 API `size`，返回 `QPageSize` 当前元素数、字节数、容量或可用空间。它是某一时刻的快照，不能替代并发同步或后续操作的边界检查。

**签名拆解：**

- 返回值：`QSizeF`。
- 参数 `units`：类型为 `QPageSize::Unit`。没有默认值，调用时必须提供。传入 `QPageSize::Unit` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] QSizeF QPageSize::size(QPageSize::PageSizeId pageSizeId, QPageSize::Unit units)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `size`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QSizeF`。
- 参数 `pageSizeId`：类型为 `QPageSize::PageSizeId`。没有默认值，调用时必须提供。传入 `QPageSize::PageSizeId` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `units`：类型为 `QPageSize::Unit`。没有默认值，调用时必须提供。传入 `QPageSize::Unit` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QSize QPageSize::sizePixels(int resolution) const`

**API 类别：** 成员函数说明

**中文解读：** `QPageSize::sizePixels` 用于计算、查询或取得与“尺寸或数量、Pixels”相关的操作。调用时要先确认当前状态和 `resolution` 的有效范围；返回类型是 `QSize`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QSize`。
- 参数 `resolution`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] QSize QPageSize::sizePixels(QPageSize::PageSizeId pageSizeId, int resolution)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `sizePixels`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QSize`。
- 参数 `pageSizeId`：类型为 `QPageSize::PageSizeId`。没有默认值，调用时必须提供。传入 `QPageSize::PageSizeId` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `resolution`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QSize QPageSize::sizePoints() const`

**API 类别：** 成员函数说明

**中文解读：** `QPageSize::sizePoints` 用于计算、查询或取得与“尺寸或数量、Points”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QSize`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QSize`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] QSize QPageSize::sizePoints(QPageSize::PageSizeId pageSizeId)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `sizePoints`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QSize`。
- 参数 `pageSizeId`：类型为 `QPageSize::PageSizeId`。没有默认值，调用时必须提供。传入 `QPageSize::PageSizeId` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] void QPageSize::swap(QPageSize &other)`

**API 类别：** 成员函数说明

**中文解读：** `QPageSize::swap` 用于执行与“swap”相关的操作。调用时要先确认当前状态和 `other` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `other`：类型为 `QPageSize &`。没有默认值，调用时必须提供。参与比较、合并或交换的另一个对象；要确认它与当前对象属于同一类型或兼容协议。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `int QPageSize::windowsId() const`

**API 类别：** 成员函数说明

**中文解读：** `QPageSize::windowsId` 用于计算、查询或取得与“windows、Id”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `int`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`int`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] int QPageSize::windowsId(QPageSize::PageSizeId pageSizeId)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `windowsId`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`int`。
- 参数 `pageSizeId`：类型为 `QPageSize::PageSizeId`。没有默认值，调用时必须提供。传入 `QPageSize::PageSizeId` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] QPageSize &QPageSize::operator=(QPageSize &&other)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QPageSize` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QPageSize &`。
- 参数 `other`：类型为 `QPageSize &&`。没有默认值，调用时必须提供。参与比较、合并或交换的另一个对象；要确认它与当前对象属于同一类型或兼容协议。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QPageSize &QPageSize::operator=(const QPageSize &other)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QPageSize` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QPageSize &`。
- 参数 `other`：类型为 `const QPageSize &`。没有默认值，调用时必须提供。参与比较、合并或交换的另一个对象；要确认它与当前对象属于同一类型或兼容协议。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool operator!=(const QPageSize &lhs, const QPageSize &rhs)`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QPageSize` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`bool`。
- 参数 `lhs`：类型为 `const QPageSize &`。没有默认值，调用时必须提供。运算符左侧的值；要注意返回新值还是修改当前对象。
- 参数 `rhs`：类型为 `const QPageSize &`。没有默认值，调用时必须提供。运算符右侧的另一个值；通常不会被当前 API 接管所有权。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool operator==(const QPageSize &lhs, const QPageSize &rhs)`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QPageSize` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`bool`。
- 参数 `lhs`：类型为 `const QPageSize &`。没有默认值，调用时必须提供。运算符左侧的值；要注意返回新值还是修改当前对象。
- 参数 `rhs`：类型为 `const QPageSize &`。没有默认值，调用时必须提供。运算符右侧的另一个值；通常不会被当前 API 接管所有权。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `enum SizeMatchPolicy { FuzzyMatch, FuzzyOrientationMatch, ExactMatch }`

**API 类别：** 公有类型

**中文解读：** 这是 `QPageSize` 暴露的类型声明 `尺寸或数量、匹配、Policy`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 这是供该类其他 API 使用的枚举/标志类型；传值前要确认枚举值的语义和适用状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

## 6. 深入实践与常见坑

### 生命周期和资源边界

先确认对象是值类型还是 QObject 派生对象，再确定所有权、有效期、拷贝成本和销毁方式。返回的句柄、索引、reply、设备或迭代器可能有独立的有效期，不能只看 C++ 指针是否非空。

### 状态和错误边界

把返回值、状态查询、错误信息和通知信号分开判断。调用成功可能只表示请求被接受，真正完成还要等待状态变化或完成信号；读取数据前先检查对象和结果是否有效。

### 线程边界

如果类型直接或间接参与 QObject、GUI、设备或异步框架，就必须确认线程归属和事件循环；值类型虽然可以复制，也要注意内部指针、共享数据和并发写入。

### 最容易出现的错误

不要忽略构造失败、空返回、默认值和版本限制；不要把异步 API 当同步 API；不要在没有确认所有权和线程的情况下保存指针或跨线程调用。

### 版本和平台

本文档以 Qt 6.11.1 为依据。涉及平台后端、编解码器、数据库驱动、窗口风格、编译器特性或标注了版本号的 API 时，要把版本条件当作使用约束，而不是只看函数是否能补全。

## 7. 使用边界

`QPageSize` 所属机制类型：Qt 类型机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
