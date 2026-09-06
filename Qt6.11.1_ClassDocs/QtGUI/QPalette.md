# QPalette

> Qt 6.11.1 · Qt GUI

## 1. 先建立直觉

**一句话定位：** 这是 GUI 基础类型，常用于绘制、输入、图像、字体或窗口系统集成。

**模块背景：** Qt GUI 负责窗口系统集成、绘制、颜色、字体、图像、输入事件和底层 GUI 资源。

### 这是什么

`QPalette` 是 Qt 类型机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 这个类的行为由它的继承关系、构造参数、公开状态和成员函数协议共同决定。使用时要把创建、配置、核心操作、结果/通知和清理看成一条闭环，而不是孤立调用某个函数。

**适用场景：** 围绕这个类的核心职责建立最小闭环：准备依赖 -> 创建/取得对象 -> 设置必要配置 -> 调用核心 API -> 检查返回值和状态 -> 处理结果/错误 -> 结束时清理。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要忽略构造失败、空返回、默认值和版本限制；不要把异步 API 当同步 API；不要在没有确认所有权和线程的情况下保存指针或跨线程调用。

## 2. 依赖与对象关系

- 头文件：`#include <QPalette>`
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

- `enum ColorGroup { Disabled, Active, Inactive, Normal }`
- `enum ColorRole { Window, WindowText, Base, AlternateBase, ToolTipBase, …, NoRole }`

### 公有函数

- `QPalette()`
- `QPalette(Qt::GlobalColor button)`
- `QPalette(const QColor &button)`
- `QPalette(const QColor &button, const QColor &window)`
- `QPalette(const QBrush &windowText, const QBrush &button, const QBrush &light, const QBrush &dark, const QBrush &mid, const QBrush &text, const QBrush &bright_text, const QBrush &base, const QBrush &window)`
- `QPalette(const QPalette &p)`
- `QPalette(QPalette &&other)`
- `~QPalette()`
- `(since 6.6) const QBrush & accent() const`
- `const QBrush & alternateBase() const`
- `const QBrush & base() const`
- `const QBrush & brightText() const`
- `const QBrush & brush(QPalette::ColorGroup group, QPalette::ColorRole role) const`
- `const QBrush & brush(QPalette::ColorRole role) const`
- `const QBrush & button() const`
- `const QBrush & buttonText() const`
- `qint64 cacheKey() const`
- `const QColor & color(QPalette::ColorGroup group, QPalette::ColorRole role) const`
- `const QColor & color(QPalette::ColorRole role) const`
- `QPalette::ColorGroup currentColorGroup() const`
- `const QBrush & dark() const`
- `const QBrush & highlight() const`
- `const QBrush & highlightedText() const`
- `bool isBrushSet(QPalette::ColorGroup cg, QPalette::ColorRole cr) const`
- `bool isCopyOf(const QPalette &p) const`
- `bool isEqual(QPalette::ColorGroup cg1, QPalette::ColorGroup cg2) const`
- `const QBrush & light() const`
- `const QBrush & link() const`
- `const QBrush & linkVisited() const`
- `const QBrush & mid() const`
- `const QBrush & midlight() const`
- `const QBrush & placeholderText() const`
- `QPalette resolve(const QPalette &other) const`
- `void setBrush(QPalette::ColorRole role, const QBrush &brush)`
- `void setBrush(QPalette::ColorGroup group, QPalette::ColorRole role, const QBrush &brush)`
- `void setColor(QPalette::ColorGroup group, QPalette::ColorRole role, const QColor &color)`
- `void setColor(QPalette::ColorRole role, const QColor &color)`
- `void setColorGroup(QPalette::ColorGroup cg, const QBrush &windowText, const QBrush &button, const QBrush &light, const QBrush &dark, const QBrush &mid, const QBrush &text, const QBrush &bright_text, const QBrush &base, const QBrush &window)`
- `void setCurrentColorGroup(QPalette::ColorGroup cg)`
- `const QBrush & shadow() const`
- `void swap(QPalette &other)`
- `const QBrush & text() const`
- `const QBrush & toolTipBase() const`
- `const QBrush & toolTipText() const`
- `const QBrush & window() const`
- `const QBrush & windowText() const`
- `operator QVariant() const`
- `bool operator!=(const QPalette &p) const`
- `QPalette & operator=(QPalette &&other)`
- `QPalette & operator=(const QPalette &p)`
- `(since 6.6) bool operator==(const QPalette &p) const`

### 相关非成员函数

- `QDataStream & operator<<(QDataStream &s, const QPalette &p)`
- `QDataStream & operator>>(QDataStream &s, QPalette &p)`

## 5. API 逐个说明

这里直接说明每个公开成员解决什么问题、参数代表什么、返回什么、会改变什么以及使用时容易出现什么问题。每一个公开签名都会有对应的中文解释。

本类共整理 55 个公开成员条目；没有独立长描述的 API 也会根据签名、类型和所属机制给出使用说明。

### `enum QPalette::ColorRole`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QPalette` 暴露的类型声明 `Color、角色`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 属性类型：`:ColorRole`。
- 属性名：`QPalette`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QPalette::QPalette()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QPalette` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QPalette::QPalette(Qt::GlobalColor button)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QPalette` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `button`：类型为 `Qt::GlobalColor`。没有默认值，调用时必须提供。传入 `Qt::GlobalColor` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QPalette::QPalette(const QColor &button)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QPalette` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `button`：类型为 `const QColor &`。没有默认值，调用时必须提供。传入 `const QColor &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QPalette::QPalette(const QColor &button, const QColor &window)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QPalette` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `button`：类型为 `const QColor &`。没有默认值，调用时必须提供。传入 `const QColor &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `window`：类型为 `const QColor &`。没有默认值，调用时必须提供。传入 `const QColor &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QPalette::QPalette(const QBrush &windowText, const QBrush &button, const QBrush &light, const QBrush &dark, const QBrush &mid, const QBrush &text, const QBrush &bright_text, const QBrush &base, const QBrush &window)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QPalette` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `windowText`：类型为 `const QBrush &`。没有默认值，调用时必须提供。传入 `const QBrush &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `button`：类型为 `const QBrush &`。没有默认值，调用时必须提供。传入 `const QBrush &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `light`：类型为 `const QBrush &`。没有默认值，调用时必须提供。传入 `const QBrush &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `dark`：类型为 `const QBrush &`。没有默认值，调用时必须提供。传入 `const QBrush &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `mid`：类型为 `const QBrush &`。没有默认值，调用时必须提供。传入 `const QBrush &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `text`：类型为 `const QBrush &`。没有默认值，调用时必须提供。文本内容。要区分 Unicode 字符串和 UTF-8/本地编码字节，必要时明确转换。
- 参数 `bright_text`：类型为 `const QBrush &`。没有默认值，调用时必须提供。传入 `const QBrush &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `base`：类型为 `const QBrush &`。没有默认值，调用时必须提供。传入 `const QBrush &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `window`：类型为 `const QBrush &`。没有默认值，调用时必须提供。传入 `const QBrush &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QPalette::QPalette(const QPalette &p)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QPalette` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `p`：类型为 `const QPalette &`。没有默认值，调用时必须提供。传入 `const QPalette &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] QPalette::QPalette(QPalette &&other)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QPalette` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `other`：类型为 `QPalette &&`。没有默认值，调用时必须提供。参与比较、合并或交换的另一个对象；要确认它与当前对象属于同一类型或兼容协议。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] QPalette::~QPalette()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QPalette` 的析构函数。对象销毁时资源、子对象和连接会按 Qt 规则释放；异步对象要先停止任务或使用 deleteLater，避免回调访问已经不存在的实例。

**签名拆解：**

- 返回值：析构函数，无返回值。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.6] const QBrush &QPalette::accent() const`

**API 类别：** 成员函数说明

**中文解读：** `QPalette::accent` 用于计算、查询或取得与“accent”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `const QBrush &`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`const QBrush &`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `const QBrush &QPalette::alternateBase() const`

**API 类别：** 成员函数说明

**中文解读：** `QPalette::alternateBase` 用于计算、查询或取得与“alternate、Base”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `const QBrush &`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`const QBrush &`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `const QBrush &QPalette::base() const`

**API 类别：** 成员函数说明

**中文解读：** `QPalette::base` 用于计算、查询或取得与“base”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `const QBrush &`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`const QBrush &`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `const QBrush &QPalette::brightText() const`

**API 类别：** 成员函数说明

**中文解读：** `QPalette::brightText` 用于计算、查询或取得与“bright、文本”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `const QBrush &`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`const QBrush &`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `const QBrush &QPalette::brush(QPalette::ColorGroup group, QPalette::ColorRole role) const`

**API 类别：** 成员函数说明

**中文解读：** `QPalette::brush` 用于计算、查询或取得与“brush”相关的操作。调用时要先确认当前状态和 `group`、`role` 的有效范围；返回类型是 `const QBrush &`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`const QBrush &`。
- 参数 `group`：类型为 `QPalette::ColorGroup`。没有默认值，调用时必须提供。传入 `QPalette::ColorGroup` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `role`：类型为 `QPalette::ColorRole`。没有默认值，调用时必须提供。数据角色，决定模型返回的是显示文本、编辑值、装饰、用户数据还是其他语义。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `const QBrush &QPalette::brush(QPalette::ColorRole role) const`

**API 类别：** 成员函数说明

**中文解读：** `QPalette::brush` 用于计算、查询或取得与“brush”相关的操作。调用时要先确认当前状态和 `role` 的有效范围；返回类型是 `const QBrush &`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`const QBrush &`。
- 参数 `role`：类型为 `QPalette::ColorRole`。没有默认值，调用时必须提供。数据角色，决定模型返回的是显示文本、编辑值、装饰、用户数据还是其他语义。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `const QBrush &QPalette::button() const`

**API 类别：** 成员函数说明

**中文解读：** `QPalette::button` 用于计算、查询或取得与“button”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `const QBrush &`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`const QBrush &`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `const QBrush &QPalette::buttonText() const`

**API 类别：** 成员函数说明

**中文解读：** `QPalette::buttonText` 用于计算、查询或取得与“button、文本”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `const QBrush &`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`const QBrush &`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `qint64 QPalette::cacheKey() const`

**API 类别：** 成员函数说明

**中文解读：** `QPalette::cacheKey` 用于计算、查询或取得与“cache、Key”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `qint64`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`qint64`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `const QColor &QPalette::color(QPalette::ColorGroup group, QPalette::ColorRole role) const`

**API 类别：** 成员函数说明

**中文解读：** `QPalette::color` 用于计算、查询或取得与“color”相关的操作。调用时要先确认当前状态和 `group`、`role` 的有效范围；返回类型是 `const QColor &`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`const QColor &`。
- 参数 `group`：类型为 `QPalette::ColorGroup`。没有默认值，调用时必须提供。传入 `QPalette::ColorGroup` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `role`：类型为 `QPalette::ColorRole`。没有默认值，调用时必须提供。数据角色，决定模型返回的是显示文本、编辑值、装饰、用户数据还是其他语义。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `const QColor &QPalette::color(QPalette::ColorRole role) const`

**API 类别：** 成员函数说明

**中文解读：** `QPalette::color` 用于计算、查询或取得与“color”相关的操作。调用时要先确认当前状态和 `role` 的有效范围；返回类型是 `const QColor &`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`const QColor &`。
- 参数 `role`：类型为 `QPalette::ColorRole`。没有默认值，调用时必须提供。数据角色，决定模型返回的是显示文本、编辑值、装饰、用户数据还是其他语义。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QPalette::ColorGroup QPalette::currentColorGroup() const`

**API 类别：** 成员函数说明

**中文解读：** `QPalette::currentColorGroup` 用于计算、查询或取得与“当前、Color、Group”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QPalette::ColorGroup`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QPalette::ColorGroup`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `const QBrush &QPalette::dark() const`

**API 类别：** 成员函数说明

**中文解读：** `QPalette::dark` 用于计算、查询或取得与“dark”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `const QBrush &`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`const QBrush &`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `const QBrush &QPalette::highlight() const`

**API 类别：** 成员函数说明

**中文解读：** `QPalette::highlight` 用于计算、查询或取得与“highlight”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `const QBrush &`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`const QBrush &`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `const QBrush &QPalette::highlightedText() const`

**API 类别：** 成员函数说明

**中文解读：** `QPalette::highlightedText` 用于计算、查询或取得与“highlighted、文本”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `const QBrush &`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`const QBrush &`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QPalette::isBrushSet(QPalette::ColorGroup cg, QPalette::ColorRole cr) const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `isBrushSet`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数 `cg`：类型为 `QPalette::ColorGroup`。没有默认值，调用时必须提供。传入 `QPalette::ColorGroup` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `cr`：类型为 `QPalette::ColorRole`。没有默认值，调用时必须提供。传入 `QPalette::ColorRole` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QPalette::isCopyOf(const QPalette &p) const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `isCopyOf`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数 `p`：类型为 `const QPalette &`。没有默认值，调用时必须提供。传入 `const QPalette &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QPalette::isEqual(QPalette::ColorGroup cg1, QPalette::ColorGroup cg2) const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `isEqual`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数 `cg1`：类型为 `QPalette::ColorGroup`。没有默认值，调用时必须提供。传入 `QPalette::ColorGroup` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `cg2`：类型为 `QPalette::ColorGroup`。没有默认值，调用时必须提供。传入 `QPalette::ColorGroup` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `const QBrush &QPalette::light() const`

**API 类别：** 成员函数说明

**中文解读：** `QPalette::light` 用于计算、查询或取得与“light”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `const QBrush &`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`const QBrush &`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `const QBrush &QPalette::link() const`

**API 类别：** 成员函数说明

**中文解读：** `QPalette::link` 用于计算、查询或取得与“link”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `const QBrush &`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`const QBrush &`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `const QBrush &QPalette::linkVisited() const`

**API 类别：** 成员函数说明

**中文解读：** `QPalette::linkVisited` 用于计算、查询或取得与“link、Visited”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `const QBrush &`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`const QBrush &`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `const QBrush &QPalette::mid() const`

**API 类别：** 成员函数说明

**中文解读：** `QPalette::mid` 用于计算、查询或取得与“mid”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `const QBrush &`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`const QBrush &`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `const QBrush &QPalette::midlight() const`

**API 类别：** 成员函数说明

**中文解读：** `QPalette::midlight` 用于计算、查询或取得与“midlight”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `const QBrush &`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`const QBrush &`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `const QBrush &QPalette::placeholderText() const`

**API 类别：** 成员函数说明

**中文解读：** `QPalette::placeholderText` 用于计算、查询或取得与“placeholder、文本”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `const QBrush &`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`const QBrush &`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QPalette QPalette::resolve(const QPalette &other) const`

**API 类别：** 成员函数说明

**中文解读：** `QPalette::resolve` 用于计算、查询或取得与“resolve”相关的操作。调用时要先确认当前状态和 `other` 的有效范围；返回类型是 `QPalette`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QPalette`。
- 参数 `other`：类型为 `const QPalette &`。没有默认值，调用时必须提供。参与比较、合并或交换的另一个对象；要确认它与当前对象属于同一类型或兼容协议。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QPalette::setBrush(QPalette::ColorRole role, const QBrush &brush)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setBrush`。调用它会改变 `QPalette` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `role`：类型为 `QPalette::ColorRole`。没有默认值，调用时必须提供。数据角色，决定模型返回的是显示文本、编辑值、装饰、用户数据还是其他语义。
- 参数 `brush`：类型为 `const QBrush &`。没有默认值，调用时必须提供。传入 `const QBrush &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QPalette::setBrush(QPalette::ColorGroup group, QPalette::ColorRole role, const QBrush &brush)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setBrush`。调用它会改变 `QPalette` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `group`：类型为 `QPalette::ColorGroup`。没有默认值，调用时必须提供。传入 `QPalette::ColorGroup` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `role`：类型为 `QPalette::ColorRole`。没有默认值，调用时必须提供。数据角色，决定模型返回的是显示文本、编辑值、装饰、用户数据还是其他语义。
- 参数 `brush`：类型为 `const QBrush &`。没有默认值，调用时必须提供。传入 `const QBrush &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QPalette::setColor(QPalette::ColorGroup group, QPalette::ColorRole role, const QColor &color)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setColor`。调用它会改变 `QPalette` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `group`：类型为 `QPalette::ColorGroup`。没有默认值，调用时必须提供。传入 `QPalette::ColorGroup` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `role`：类型为 `QPalette::ColorRole`。没有默认值，调用时必须提供。数据角色，决定模型返回的是显示文本、编辑值、装饰、用户数据还是其他语义。
- 参数 `color`：类型为 `const QColor &`。没有默认值，调用时必须提供。传入 `const QColor &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QPalette::setColor(QPalette::ColorRole role, const QColor &color)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setColor`。调用它会改变 `QPalette` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `role`：类型为 `QPalette::ColorRole`。没有默认值，调用时必须提供。数据角色，决定模型返回的是显示文本、编辑值、装饰、用户数据还是其他语义。
- 参数 `color`：类型为 `const QColor &`。没有默认值，调用时必须提供。传入 `const QColor &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QPalette::setColorGroup(QPalette::ColorGroup cg, const QBrush &windowText, const QBrush &button, const QBrush &light, const QBrush &dark, const QBrush &mid, const QBrush &text, const QBrush &bright_text, const QBrush &base, const QBrush &window)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setColorGroup`。调用它会改变 `QPalette` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `cg`：类型为 `QPalette::ColorGroup`。没有默认值，调用时必须提供。传入 `QPalette::ColorGroup` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `windowText`：类型为 `const QBrush &`。没有默认值，调用时必须提供。传入 `const QBrush &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `button`：类型为 `const QBrush &`。没有默认值，调用时必须提供。传入 `const QBrush &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `light`：类型为 `const QBrush &`。没有默认值，调用时必须提供。传入 `const QBrush &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `dark`：类型为 `const QBrush &`。没有默认值，调用时必须提供。传入 `const QBrush &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `mid`：类型为 `const QBrush &`。没有默认值，调用时必须提供。传入 `const QBrush &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `text`：类型为 `const QBrush &`。没有默认值，调用时必须提供。文本内容。要区分 Unicode 字符串和 UTF-8/本地编码字节，必要时明确转换。
- 参数 `bright_text`：类型为 `const QBrush &`。没有默认值，调用时必须提供。传入 `const QBrush &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `base`：类型为 `const QBrush &`。没有默认值，调用时必须提供。传入 `const QBrush &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `window`：类型为 `const QBrush &`。没有默认值，调用时必须提供。传入 `const QBrush &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QPalette::setCurrentColorGroup(QPalette::ColorGroup cg)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setCurrentColorGroup`。调用它会改变 `QPalette` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `cg`：类型为 `QPalette::ColorGroup`。没有默认值，调用时必须提供。传入 `QPalette::ColorGroup` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `const QBrush &QPalette::shadow() const`

**API 类别：** 成员函数说明

**中文解读：** `QPalette::shadow` 用于计算、查询或取得与“shadow”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `const QBrush &`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`const QBrush &`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] void QPalette::swap(QPalette &other)`

**API 类别：** 成员函数说明

**中文解读：** `QPalette::swap` 用于执行与“swap”相关的操作。调用时要先确认当前状态和 `other` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `other`：类型为 `QPalette &`。没有默认值，调用时必须提供。参与比较、合并或交换的另一个对象；要确认它与当前对象属于同一类型或兼容协议。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `const QBrush &QPalette::text() const`

**API 类别：** 成员函数说明

**中文解读：** `QPalette::text` 用于计算、查询或取得与“文本”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `const QBrush &`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`const QBrush &`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `const QBrush &QPalette::toolTipBase() const`

**API 类别：** 成员函数说明

**中文解读：** 这是转换/映射 API `toolTipBase`。它通常在不同表示、坐标系、编码或 Qt 类型之间建立边界；转换前确认格式和所有权，转换后检查是否丢失精度、编码或上下文。

**签名拆解：**

- 返回值：`const QBrush &`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `const QBrush &QPalette::toolTipText() const`

**API 类别：** 成员函数说明

**中文解读：** 这是转换/映射 API `toolTipText`。它通常在不同表示、坐标系、编码或 Qt 类型之间建立边界；转换前确认格式和所有权，转换后检查是否丢失精度、编码或上下文。

**签名拆解：**

- 返回值：`const QBrush &`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `const QBrush &QPalette::window() const`

**API 类别：** 成员函数说明

**中文解读：** `QPalette::window` 用于计算、查询或取得与“window”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `const QBrush &`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`const QBrush &`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `const QBrush &QPalette::windowText() const`

**API 类别：** 成员函数说明

**中文解读：** `QPalette::windowText` 用于计算、查询或取得与“window、文本”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `const QBrush &`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`const QBrush &`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QPalette::operator QVariant() const`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QPalette` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`由运算符声明决定`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QPalette::operator!=(const QPalette &p) const`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QPalette` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`bool`。
- 参数 `p`：类型为 `const QPalette &`。没有默认值，调用时必须提供。传入 `const QPalette &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] QPalette &QPalette::operator=(QPalette &&other)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QPalette` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QPalette &`。
- 参数 `other`：类型为 `QPalette &&`。没有默认值，调用时必须提供。参与比较、合并或交换的另一个对象；要确认它与当前对象属于同一类型或兼容协议。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QPalette &QPalette::operator=(const QPalette &p)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QPalette` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QPalette &`。
- 参数 `p`：类型为 `const QPalette &`。没有默认值，调用时必须提供。传入 `const QPalette &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.6] bool QPalette::operator==(const QPalette &p) const`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QPalette` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`bool`。
- 参数 `p`：类型为 `const QPalette &`。没有默认值，调用时必须提供。传入 `const QPalette &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QDataStream &operator<<(QDataStream &s, const QPalette &p)`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QPalette` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QDataStream &`。
- 参数 `s`：类型为 `QDataStream &`。没有默认值，调用时必须提供。传入 `QDataStream &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `p`：类型为 `const QPalette &`。没有默认值，调用时必须提供。传入 `const QPalette &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QDataStream &operator>>(QDataStream &s, QPalette &p)`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QPalette` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QDataStream &`。
- 参数 `s`：类型为 `QDataStream &`。没有默认值，调用时必须提供。传入 `QDataStream &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `p`：类型为 `QPalette &`。没有默认值，调用时必须提供。传入 `QPalette &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `enum ColorGroup { Disabled, Active, Inactive, Normal }`

**API 类别：** 公有类型

**中文解读：** 这是 `QPalette` 暴露的类型声明 `Color、Group`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

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

`QPalette` 所属机制类型：Qt 类型机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
