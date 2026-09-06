# QDirListing

> Qt 6.11.1 · Qt Core

## 1. 先建立直觉

**一句话定位：** `QDirListing` 是 文件、设备与流机制 中的类型，负责把这一机制中的数据、状态或资源交给其他 Qt 对象使用。

**模块背景：** Qt Core 提供对象模型、事件循环、容器、字符串、文件、线程、时间和元对象系统等基础能力。

### 这是什么

`QDirListing` 是 文件、设备与流机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 文件和 I/O 类型把路径/设备描述与打开后的读写状态分开。打开模式决定可执行的操作，当前位置、缓冲区、文本编码、权限和错误状态共同决定一次读写是否正确。

**适用场景：** 构造稳定路径，选择正确的 OpenMode，检查 open 和 errorString，按数据规模使用流式读写或分块处理，明确文本编码，完成后关闭并处理失败。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要手写平台分隔符；不要默认相对路径指向程序目录；不要把本地编码、UTF-8 和二进制混在一起；写文件时要考虑临时文件、覆盖、权限和原子替换。

## 2. 依赖与对象关系

- 头文件：`#include <QDirListing>`
- 继承自：未在类页中列出
- 直接派生类：未在类页中列出

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Core)
target_link_libraries(mytarget PRIVATE Qt6::Core)
```

**继承带来的规则：** 它是值类型或不直接使用 QObject 对象模型，重点放在数据语义、拷贝/移动成本和参数有效性。

### 工作机制

文件和 I/O 类型把路径/设备描述与打开后的读写状态分开。打开模式决定可执行的操作，当前位置、缓冲区、文本编码、权限和错误状态共同决定一次读写是否正确。

### 状态、生命周期和线程

**生命周期：** 先设置路径或设备，再 open，成功后读写/定位/刷新，最后 close；析构通常会关闭设备，但关键写入应显式 flush/close 并检查错误。相对路径依赖当前工作目录，资源路径和用户文件路径要区分。

**状态与结果：** 区分设备未打开、打开成功、到达 EOF、暂时无数据、读写失败和写入尚未落盘。`readAll()` 方便小数据但可能占用大量内存，大文件应分块处理并检查返回值。

**线程与事件循环：** 同一个打开设备不要跨线程并发使用，除非类明确保证线程安全；后台 I/O 通过 worker 或异步设备处理，GUI 线程只接收结果。

## 3. 直接使用

构造稳定路径，选择正确的 OpenMode，检查 open 和 errorString，按数据规模使用流式读写或分块处理，明确文本编码，完成后关闭并处理失败。 使用时通常按这个过程组织：准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

```cpp
QFile file(path);
if (file.open(QIODevice::ReadOnly | QIODevice::Text)) {
    const QByteArray data = file.readAll();
}
```
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 公有类型

- `class DirEntry`
- `(since 6.8) class const_iterator`
- `(since 6.8) class sentinel`
- `enum class IteratorFlag { Default, ExcludeFiles, ExcludeDirs, ExcludeOther, ResolveSymlinks, …, FollowDirSymlinks }`
- `flags IteratorFlags`

### 公有函数

- `QDirListing(const QString &path, QDirListing::IteratorFlags flags = IteratorFlag::Default)`
- `QDirListing(const QString &path, const QStringList &nameFilters, QDirListing::IteratorFlags flags = IteratorFlag::Default)`
- `QDirListing(QDirListing &&other)`
- `~QDirListing()`
- `QDirListing::const_iterator begin() const`
- `QDirListing::const_iterator cbegin() const`
- `QDirListing::sentinel cend() const`
- `QDirListing::sentinel end() const`
- `QDirListing::IteratorFlags iteratorFlags() const`
- `QString iteratorPath() const`
- `QStringList nameFilters() const`
- `QDirListing & operator=(QDirListing &&other)`

## 5. API 逐个说明

这里直接说明每个公开成员解决什么问题、参数代表什么、返回什么、会改变什么以及使用时容易出现什么问题。每一个公开签名都会有对应的中文解释。

本类共整理 18 个公开成员条目；没有独立长描述的 API 也会根据签名、类型和所属机制给出使用说明。

### `enum class QDirListing::IteratorFlagflags QDirListing::IteratorFlags`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QDirListing` 暴露的类型声明 `class`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 属性类型：`:IteratorFlagflags QDirListing::IteratorFlags`。
- 属性名：`QDirListing`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[explicit] QDirListing::QDirListing(const QString &path, QDirListing::IteratorFlags flags = IteratorFlag::Default)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QDirListing` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `path`：类型为 `const QString &`。没有默认值，调用时必须提供。路径字符串。要确认是相对路径还是绝对路径，以及它相对于哪个工作目录。
- 参数 `flags`：类型为 `QDirListing::IteratorFlags`。默认值为 `IteratorFlag::Default`。标志位组合。可以用按位或组合，调用前确认哪些标志互斥、哪些标志需要同时出现。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[explicit] QDirListing::QDirListing(const QString &path, const QStringList &nameFilters, QDirListing::IteratorFlags flags = IteratorFlag::Default)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QDirListing` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `path`：类型为 `const QString &`。没有默认值，调用时必须提供。路径字符串。要确认是相对路径还是绝对路径，以及它相对于哪个工作目录。
- 参数 `nameFilters`：类型为 `const QStringList &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。
- 参数 `flags`：类型为 `QDirListing::IteratorFlags`。默认值为 `IteratorFlag::Default`。标志位组合。可以用按位或组合，调用前确认哪些标志互斥、哪些标志需要同时出现。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] QDirListing::QDirListing(QDirListing &&other)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QDirListing` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `other`：类型为 `QDirListing &&`。没有默认值，调用时必须提供。参与比较、合并或交换的另一个对象；要确认它与当前对象属于同一类型或兼容协议。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] QDirListing::~QDirListing()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QDirListing` 的析构函数。对象销毁时资源、子对象和连接会按 Qt 规则释放；异步对象要先停止任务或使用 deleteLater，避免回调访问已经不存在的实例。

**签名拆解：**

- 返回值：析构函数，无返回值。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QDirListing::sentinel QDirListing::cend() const`

**API 类别：** 成员函数说明

**中文解读：** `QDirListing::cend` 用于计算、查询或取得与“cend”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QDirListing::sentinel`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QDirListing::sentinel`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QDirListing::IteratorFlags QDirListing::iteratorFlags() const`

**API 类别：** 成员函数说明

**中文解读：** `QDirListing::iteratorFlags` 用于计算、查询或取得与“iterator、标志”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QDirListing::IteratorFlags`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QDirListing::IteratorFlags`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString QDirListing::iteratorPath() const`

**API 类别：** 成员函数说明

**中文解读：** `QDirListing::iteratorPath` 用于计算、查询或取得与“iterator、Path”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QString`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QString`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QStringList QDirListing::nameFilters() const`

**API 类别：** 成员函数说明

**中文解读：** `QDirListing::nameFilters` 用于计算、查询或取得与“名称、Filters”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QStringList`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QStringList`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] QDirListing &QDirListing::operator=(QDirListing &&other)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QDirListing` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QDirListing &`。
- 参数 `other`：类型为 `QDirListing &&`。没有默认值，调用时必须提供。参与比较、合并或交换的另一个对象；要确认它与当前对象属于同一类型或兼容协议。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `class DirEntry`

**API 类别：** 公有类型

**中文解读：** 这是 `QDirListing` 暴露的类型声明 `Dir、Entry`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `(since 6.8) class const_iterator`

**API 类别：** 公有类型

**中文解读：** 这是 `QDirListing` 暴露的类型声明 `const、iterator`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `(since 6.8) class sentinel`

**API 类别：** 公有类型

**中文解读：** 这是 `QDirListing` 暴露的类型声明 `sentinel`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `enum class IteratorFlag { Default, ExcludeFiles, ExcludeDirs, ExcludeOther, ResolveSymlinks, …, FollowDirSymlinks }`

**API 类别：** 公有类型

**中文解读：** 这是 `QDirListing` 暴露的类型声明 `class`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 这是供该类其他 API 使用的枚举/标志类型；传值前要确认枚举值的语义和适用状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `flags IteratorFlags`

**API 类别：** 公有类型

**中文解读：** 这是 `QDirListing` 的 `标志` 成员声明。它通常作为其他 API 的类型、常量或配置入口使用；先确认可用值和适用状态，再结合本类的创建、核心操作和清理流程使用。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QDirListing::const_iterator begin() const`

**API 类别：** 公有函数

**中文解读：** 这是启动/建立资源的 API `begin`。调用前准备依赖和参数，调用后检查返回值或状态信号；成功后通常需要配套的 stop/close/end/disconnect 或释放操作。

**签名拆解：**

- 返回值：`QDirListing::const_iterator`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QDirListing::const_iterator cbegin() const`

**API 类别：** 公有函数

**中文解读：** `QDirListing::cbegin` 用于计算、查询或取得与“cbegin”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QDirListing::const_iterator`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QDirListing::const_iterator`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QDirListing::sentinel end() const`

**API 类别：** 公有函数

**中文解读：** 这是结束/释放/取消 API `end`。它会改变对象状态或资源所有权，调用后不要继续使用已经失效的句柄、reply、索引或设备，并确认异步完成信号是否仍会到达。

**签名拆解：**

- 返回值：`QDirListing::sentinel`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

## 6. 深入实践与常见坑

### 生命周期和资源边界

先设置路径或设备，再 open，成功后读写/定位/刷新，最后 close；析构通常会关闭设备，但关键写入应显式 flush/close 并检查错误。相对路径依赖当前工作目录，资源路径和用户文件路径要区分。

### 状态和错误边界

区分设备未打开、打开成功、到达 EOF、暂时无数据、读写失败和写入尚未落盘。`readAll()` 方便小数据但可能占用大量内存，大文件应分块处理并检查返回值。

### 线程边界

同一个打开设备不要跨线程并发使用，除非类明确保证线程安全；后台 I/O 通过 worker 或异步设备处理，GUI 线程只接收结果。

### 最容易出现的错误

不要手写平台分隔符；不要默认相对路径指向程序目录；不要把本地编码、UTF-8 和二进制混在一起；写文件时要考虑临时文件、覆盖、权限和原子替换。

### 版本和平台

本文档以 Qt 6.11.1 为依据。涉及平台后端、编解码器、数据库驱动、窗口风格、编译器特性或标注了版本号的 API 时，要把版本条件当作使用约束，而不是只看函数是否能补全。

## 7. 使用边界

`QDirListing` 所属机制类型：文件、设备与流机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
