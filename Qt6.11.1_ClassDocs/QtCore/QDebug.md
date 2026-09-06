# QDebug

> Qt 6.11.1 · Qt Core

## 1. 先建立直觉

**一句话定位：** `QDebug` 是 Qt 日志与诊断体系中的类型，用于按类别输出调试、信息、警告或错误消息。

**模块背景：** Qt Core 提供对象模型、事件循环、容器、字符串、文件、线程、时间和元对象系统等基础能力。

### 这是什么

`QDebug` 是 Qt 日志与诊断机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** Qt 日志 API 把消息级别、类别、源文件/行号上下文和最终处理器分开。`qDebug`、`qInfo`、`qWarning`、`qCritical` 负责产生消息，分类规则和 message handler 决定输出到哪里、是否过滤或持久化。

**适用场景：** 用分类定义稳定的日志边界，使用合适级别记录状态和错误，必要时安装 handler 写入文件或诊断系统；敏感信息、token、密码不要输出。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要用 qFatal 代替普通错误处理；不要在 handler 里再次触发同类日志；不要把日志文本当作稳定的程序接口；注意 release 构建中的上下文宏和过滤规则。

## 2. 依赖与对象关系

- 头文件：`#include <QDebug>`
- 继承自：QIODeviceBase
- 直接派生类：QQmlInfo

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Core)
target_link_libraries(mytarget PRIVATE Qt6::Core)
```

**继承带来的规则：** 它是值类型或不直接使用 QObject 对象模型，重点放在数据语义、拷贝/移动成本和参数有效性。

### 工作机制

Qt 日志 API 把消息级别、类别、源文件/行号上下文和最终处理器分开。`qDebug`、`qInfo`、`qWarning`、`qCritical` 负责产生消息，分类规则和 message handler 决定输出到哪里、是否过滤或持久化。

### 状态、生命周期和线程

**生命周期：** 日志上下文通常是一次消息表达式的临时对象；自定义 message handler 的安装和卸载要覆盖整个使用期，处理器内部不要递归调用会再次触发日志的代码。

**状态与结果：** 日志是否输出受级别、类别规则、编译宏和运行时过滤影响。看到某条消息缺失时，要区分代码没有执行、日志级别被过滤、上下文被关闭和 handler 改写输出。

**线程与事件循环：** 日志可能来自多个线程，handler 必须考虑并发、输出原子性和不能阻塞业务线程；不要在 handler 中访问未加锁的 GUI 控件。

## 3. 直接使用

用分类定义稳定的日志边界，使用合适级别记录状态和错误，必要时安装 handler 写入文件或诊断系统；敏感信息、token、密码不要输出。 使用时通常按这个过程组织：准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

```cpp
#include <QDebug>

qInfo() << "operation started";
qWarning() << "operation failed";
```
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 公有类型

- `enum VerbosityLevel { MinimumVerbosity, DefaultVerbosity, MaximumVerbosity }`

### 公有函数

- `(since 6.9) QDebug(QByteArray *byteArray)`
- `QDebug(QIODevice *device)`
- `QDebug(QString *string)`
- `QDebug(QtMsgType t)`
- `QDebug(const QDebug &o)`
- `~QDebug()`
- `bool autoInsertSpaces() const`
- `QDebug & maybeQuote(char c = '"')`
- `QDebug & maybeSpace()`
- `QDebug & noquote()`
- `QDebug & nospace()`
- `QDebug & quote()`
- `(since 6.7) bool quoteStrings() const`
- `QDebug & resetFormat()`
- `void setAutoInsertSpaces(bool b)`
- `(since 6.7) void setQuoteStrings(bool b)`
- `void setVerbosity(int verbosityLevel)`
- `QDebug & space()`
- `void swap(QDebug &other)`
- `int verbosity() const`
- `QDebug & verbosity(int verbosityLevel)`
- `(since 6.0) QDebug & operator<<(QByteArrayView t)`
- `QDebug & operator<<(QChar t)`
- `QDebug & operator<<(QLatin1StringView t)`
- `QDebug & operator<<(QStringView s)`
- `(since 6.0) QDebug & operator<<(QUtf8StringView s)`
- `(since 6.7) QDebug & operator<<(T i)`
- `QDebug & operator<<(bool t)`
- `QDebug & operator<<(char t)`
- `QDebug & operator<<(char16_t t)`
- `QDebug & operator<<(char32_t t)`
- `QDebug & operator<<(const QByteArray &t)`
- `QDebug & operator<<(const QString &t)`
- `QDebug & operator<<(const char *t)`
- `(since 6.0) QDebug & operator<<(const char16_t *t)`
- `(since 6.5) QDebug & operator<<(const std::basic_string<Char, Args...> &s)`
- `(since 6.7) QDebug & operator<<(const std::optional<T> &opt)`
- `(since 6.9) QDebug & operator<<(const std::tuple<Ts...> &tuple)`
- `QDebug & operator<<(const void *t)`
- `QDebug & operator<<(double t)`
- `QDebug & operator<<(float t)`
- `QDebug & operator<<(int t)`
- `QDebug & operator<<(long t)`
- `QDebug & operator<<(qint64 t)`
- `QDebug & operator<<(quint64 t)`
- `QDebug & operator<<(short t)`
- `(since 6.5) QDebug & operator<<(std::basic_string_view<Char, Args...> s)`
- `(since 6.6) QDebug & operator<<(std::chrono::duration<Rep, Period> duration)`
- `(since 6.7) QDebug & operator<<(std::nullopt_t)`
- `QDebug & operator<<(unsigned int t)`
- `QDebug & operator<<(unsigned long t)`
- `QDebug & operator<<(unsigned short t)`
- `QDebug & operator=(const QDebug &other)`

### 静态公有成员

- `(since 6.9) QByteArray toBytes(const T &object)`
- `(since 6.0) QString toString(const T &object)`

### 相关非成员函数

- `QDebug operator<<(QDebug debug, const QList<T> &list)`
- `QDebug operator<<(QDebug debug, const QMap<Key, T> &map)`
- `QDebug operator<<(QDebug debug, const QMultiHash<Key, T> &hash)`
- `QDebug operator<<(QDebug debug, const QMultiMap<Key, T> &map)`
- `QDebug operator<<(QDebug debug, const QSet<T> &set)`
- `(since 6.3) QDebug operator<<(QDebug debug, const QVarLengthArray<T, P> &array)`
- `(since 6.9) QDebug operator<<(QDebug debug, const std::array<T, N> &array)`
- `QDebug operator<<(QDebug debug, const std::list<T, Alloc> &vec)`
- `QDebug operator<<(QDebug debug, const std::map<Key, T, Compare, Alloc> &map)`
- `QDebug operator<<(QDebug debug, const std::multimap<Key, T, Compare, Alloc> &map)`
- `(since 6.9) QDebug operator<<(QDebug debug, const std::multiset<Key, Compare, Alloc> &multiset)`
- `QDebug operator<<(QDebug debug, const std::pair<T1, T2> &pair)`
- `(since 6.9) QDebug operator<<(QDebug debug, const std::set<Key, Compare, Alloc> &set)`
- `(since 6.9) QDebug operator<<(QDebug debug, const std::unordered_map<Key, T, Hash, KeyEqual, Alloc> &map)`
- `(since 6.9) QDebug operator<<(QDebug debug, const std::unordered_set<Key, Hash, KeyEqual, Alloc> &unordered_set)`
- `QDebug operator<<(QDebug debug, const std::vector<T, Alloc> &vec)`
- `(since 6.9) QDebug operator<<(QDebug debug, T t)`
- `QDebug operator<<(QDebug debug, const QContiguousCache<T> &cache)`
- `QDebug operator<<(QDebug debug, const QFlags<T> &flags)`
- `QDebug operator<<(QDebug debug, const QHash<Key, T> &hash)`

### 公开宏

- `QDebug qCritical()`
- `QDebug qDebug()`
- `QDebug qFatal()`
- `QDebug qInfo()`
- `QDebug qWarning()`

## 5. API 逐个说明

这里直接说明每个公开成员解决什么问题、参数代表什么、返回什么、会改变什么以及使用时容易出现什么问题。每一个公开签名都会有对应的中文解释。

本类共整理 81 个公开成员条目；没有独立长描述的 API 也会根据签名、类型和所属机制给出使用说明。

### `enum QDebug::VerbosityLevel`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QDebug` 暴露的类型声明 `Verbosity、Level`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 属性类型：`:VerbosityLevel`。
- 属性名：`QDebug`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[explicit, since 6.9] QDebug::QDebug(QByteArray *byteArray)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QDebug` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `byteArray`：类型为 `QByteArray *`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[explicit] QDebug::QDebug(QIODevice *device)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QDebug` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `device`：类型为 `QIODevice *`。没有默认值，调用时必须提供。QIODevice 或绘制设备。调用前要确认已经打开、支持所需模式，或处于合法绘制阶段。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[explicit] QDebug::QDebug(QString *string)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QDebug` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `string`：类型为 `QString *`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[explicit] QDebug::QDebug(QtMsgType t)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QDebug` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `t`：类型为 `QtMsgType`。没有默认值，调用时必须提供。传入 `QtMsgType` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QDebug::QDebug(const QDebug &o)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QDebug` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `o`：类型为 `const QDebug &`。没有默认值，调用时必须提供。传入 `const QDebug &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] QDebug::~QDebug()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QDebug` 的析构函数。对象销毁时资源、子对象和连接会按 Qt 规则释放；异步对象要先停止任务或使用 deleteLater，避免回调访问已经不存在的实例。

**签名拆解：**

- 返回值：析构函数，无返回值。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QDebug::autoInsertSpaces() const`

**API 类别：** 成员函数说明

**中文解读：** `QDebug::autoInsertSpaces` 用于计算、查询或取得与“auto、插入、Spaces”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QDebug &QDebug::maybeQuote(char c = '"')`

**API 类别：** 成员函数说明

**中文解读：** `QDebug::maybeQuote` 用于计算、查询或取得与“maybe、Quote”相关的操作。调用时要先确认当前状态和 `c` 的有效范围；返回类型是 `QDebug &`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QDebug &`。
- 参数 `c`：类型为 `char`。默认值为 `'"'`。传入 `char` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QDebug &QDebug::maybeSpace()`

**API 类别：** 成员函数说明

**中文解读：** `QDebug::maybeSpace` 用于计算、查询或取得与“maybe、Space”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QDebug &`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QDebug &`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QDebug &QDebug::noquote()`

**API 类别：** 成员函数说明

**中文解读：** `QDebug::noquote` 用于计算、查询或取得与“noquote”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QDebug &`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QDebug &`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QDebug &QDebug::nospace()`

**API 类别：** 成员函数说明

**中文解读：** `QDebug::nospace` 用于计算、查询或取得与“nospace”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QDebug &`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QDebug &`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QDebug &QDebug::quote()`

**API 类别：** 成员函数说明

**中文解读：** `QDebug::quote` 用于计算、查询或取得与“quote”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QDebug &`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QDebug &`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept, since 6.7] bool QDebug::quoteStrings() const`

**API 类别：** 成员函数说明

**中文解读：** `QDebug::quoteStrings` 用于计算、查询或取得与“quote、Strings”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QDebug &QDebug::resetFormat()`

**API 类别：** 成员函数说明

**中文解读：** `QDebug::resetFormat` 用于计算、查询或取得与“重置、格式化”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QDebug &`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QDebug &`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QDebug::setAutoInsertSpaces(bool b)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setAutoInsertSpaces`。调用它会改变 `QDebug` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `b`：类型为 `bool`。没有默认值，调用时必须提供。传入 `bool` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.7] void QDebug::setQuoteStrings(bool b)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setQuoteStrings`。调用它会改变 `QDebug` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `b`：类型为 `bool`。没有默认值，调用时必须提供。传入 `bool` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QDebug::setVerbosity(int verbosityLevel)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setVerbosity`。调用它会改变 `QDebug` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `verbosityLevel`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QDebug &QDebug::space()`

**API 类别：** 成员函数说明

**中文解读：** `QDebug::space` 用于计算、查询或取得与“space”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QDebug &`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QDebug &`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] void QDebug::swap(QDebug &other)`

**API 类别：** 成员函数说明

**中文解读：** `QDebug::swap` 用于执行与“swap”相关的操作。调用时要先确认当前状态和 `other` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `other`：类型为 `QDebug &`。没有默认值，调用时必须提供。参与比较、合并或交换的另一个对象；要确认它与当前对象属于同一类型或兼容协议。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static, since 6.9] template <typename T> QByteArray QDebug::toBytes(const T &object)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `toBytes`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`template <typename T> QByteArray`。
- 参数 `object`：类型为 `const T &`。没有默认值，调用时必须提供。传入 `const T &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static, since 6.0] template <typename T> QString QDebug::toString(const T &object)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `toString`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`template <typename T> QString`。
- 参数 `object`：类型为 `const T &`。没有默认值，调用时必须提供。传入 `const T &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `int QDebug::verbosity() const`

**API 类别：** 成员函数说明

**中文解读：** `QDebug::verbosity` 用于计算、查询或取得与“verbosity”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `int`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`int`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QDebug &QDebug::verbosity(int verbosityLevel)`

**API 类别：** 成员函数说明

**中文解读：** `QDebug::verbosity` 用于计算、查询或取得与“verbosity”相关的操作。调用时要先确认当前状态和 `verbosityLevel` 的有效范围；返回类型是 `QDebug &`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QDebug &`。
- 参数 `verbosityLevel`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.0] QDebug &QDebug::operator<<(QByteArrayView t)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QDebug` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QDebug &`。
- 参数 `t`：类型为 `QByteArrayView`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QDebug &QDebug::operator<<(QChar t)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QDebug` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QDebug &`。
- 参数 `t`：类型为 `QChar`。没有默认值，调用时必须提供。传入 `QChar` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QDebug &QDebug::operator<<(QLatin1StringView t)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QDebug` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QDebug &`。
- 参数 `t`：类型为 `QLatin1StringView`。没有默认值，调用时必须提供。传入 `QLatin1StringView` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QDebug &QDebug::operator<<(QStringView s)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QDebug` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QDebug &`。
- 参数 `s`：类型为 `QStringView`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.0] QDebug &QDebug::operator<<(QUtf8StringView s)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QDebug` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QDebug &`。
- 参数 `s`：类型为 `QUtf8StringView`。没有默认值，调用时必须提供。传入 `QUtf8StringView` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.7] template <typename T, QDebug::if_quint128<T> = true> QDebug &QDebug::operator<<(T i)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QDebug` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`template <typename T, QDebug::if_quint128<T> = true> QDebug &`。
- 参数 `i`：类型为 `T`。没有默认值，调用时必须提供。传入 `T` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QDebug &QDebug::operator<<(bool t)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QDebug` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QDebug &`。
- 参数 `t`：类型为 `bool`。没有默认值，调用时必须提供。传入 `bool` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QDebug &QDebug::operator<<(char t)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QDebug` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QDebug &`。
- 参数 `t`：类型为 `char`。没有默认值，调用时必须提供。传入 `char` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QDebug &QDebug::operator<<(char16_t t)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QDebug` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QDebug &`。
- 参数 `t`：类型为 `char16_t`。没有默认值，调用时必须提供。传入 `char16_t` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QDebug &QDebug::operator<<(char32_t t)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QDebug` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QDebug &`。
- 参数 `t`：类型为 `char32_t`。没有默认值，调用时必须提供。传入 `char32_t` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QDebug &QDebug::operator<<(const QByteArray &t)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QDebug` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QDebug &`。
- 参数 `t`：类型为 `const QByteArray &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QDebug &QDebug::operator<<(const QString &t)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QDebug` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QDebug &`。
- 参数 `t`：类型为 `const QString &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QDebug &QDebug::operator<<(const char *t)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QDebug` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QDebug &`。
- 参数 `t`：类型为 `const char *`。没有默认值，调用时必须提供。传入 `const char *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.0] QDebug &QDebug::operator<<(const char16_t *t)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QDebug` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QDebug &`。
- 参数 `t`：类型为 `const char16_t *`。没有默认值，调用时必须提供。传入 `const char16_t *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.5] template <typename Char, typename... Args> QDebug &QDebug::operator<<(std::basic_string_view<Char, Args...> s)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QDebug` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`template <typename Char, typename... Args> QDebug &`。
- 参数 `s`：类型为 `std::basic_string_view<Char, Args...>`。没有默认值，调用时必须提供。传入 `std::basic_string_view<Char, Args...>` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.7] template <typename T, QDebug::if_streamable<T> = true> QDebug &QDebug::operator<<(const std::optional<T> &opt)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QDebug` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`template <typename T, QDebug::if_streamable<T> = true> QDebug &`。
- 参数 `opt`：类型为 `const std::optional<T> &`。没有默认值，调用时必须提供。传入 `const std::optional<T> &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.9] template <typename... Ts, QDebug::if_streamable<Ts...> = true> QDebug &QDebug::operator<<(const std::tuple<Ts...> &tuple)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QDebug` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`template <typename... Ts, QDebug::if_streamable<Ts...> = true> QDebug &`。
- 参数 `tuple`：类型为 `const std::tuple<Ts...> &`。没有默认值，调用时必须提供。传入 `const std::tuple<Ts...> &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QDebug &QDebug::operator<<(const void *t)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QDebug` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QDebug &`。
- 参数 `t`：类型为 `const void *`。没有默认值，调用时必须提供。传入 `const void *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QDebug &QDebug::operator<<(double t)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QDebug` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QDebug &`。
- 参数 `t`：类型为 `double`。没有默认值，调用时必须提供。传入 `double` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QDebug &QDebug::operator<<(float t)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QDebug` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QDebug &`。
- 参数 `t`：类型为 `float`。没有默认值，调用时必须提供。传入 `float` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QDebug &QDebug::operator<<(int t)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QDebug` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QDebug &`。
- 参数 `t`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QDebug &QDebug::operator<<(long t)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QDebug` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QDebug &`。
- 参数 `t`：类型为 `long`。没有默认值，调用时必须提供。传入 `long` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QDebug &QDebug::operator<<(qint64 t)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QDebug` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QDebug &`。
- 参数 `t`：类型为 `qint64`。没有默认值，调用时必须提供。传入 `qint64` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QDebug &QDebug::operator<<(quint64 t)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QDebug` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QDebug &`。
- 参数 `t`：类型为 `quint64`。没有默认值，调用时必须提供。传入 `quint64` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QDebug &QDebug::operator<<(short t)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QDebug` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QDebug &`。
- 参数 `t`：类型为 `short`。没有默认值，调用时必须提供。传入 `short` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.6] template <typename Rep, typename Period> QDebug &QDebug::operator<<(std::chrono::duration<Rep, Period> duration)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QDebug` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`template <typename Rep, typename Period> QDebug &`。
- 参数 `duration`：类型为 `std::chrono::duration<Rep, Period>`。没有默认值，调用时必须提供。持续时间，通常以毫秒表示；要确认 0、负数、循环和平台精度。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.7] QDebug &QDebug::operator<<(std::nullopt_t)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QDebug` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QDebug &`。
- 参数 `nullopt_t`：类型为 `std::`。没有默认值，调用时必须提供。传入 `std::` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QDebug &QDebug::operator<<(unsigned int t)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QDebug` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QDebug &`。
- 参数 `t`：类型为 `unsigned int`。没有默认值，调用时必须提供。传入 `unsigned int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QDebug &QDebug::operator<<(unsigned long t)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QDebug` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QDebug &`。
- 参数 `t`：类型为 `unsigned long`。没有默认值，调用时必须提供。传入 `unsigned long` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QDebug &QDebug::operator<<(unsigned short t)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QDebug` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QDebug &`。
- 参数 `t`：类型为 `unsigned short`。没有默认值，调用时必须提供。传入 `unsigned short` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QDebug &QDebug::operator=(const QDebug &other)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QDebug` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QDebug &`。
- 参数 `other`：类型为 `const QDebug &`。没有默认值，调用时必须提供。参与比较、合并或交换的另一个对象；要确认它与当前对象属于同一类型或兼容协议。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `template <typename T> QDebug operator<<(QDebug debug, const QList<T> &list)`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QDebug` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`template <typename T> QDebug`。
- 参数 `debug`：类型为 `QDebug`。没有默认值，调用时必须提供。传入 `QDebug` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `list`：类型为 `const QList<T> &`。没有默认值，调用时必须提供。传入 `const QList<T> &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `template <typename Key, typename T> QDebug operator<<(QDebug debug, const QMap<Key, T> &map)`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QDebug` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`template <typename Key, typename T> QDebug`。
- 参数 `debug`：类型为 `QDebug`。没有默认值，调用时必须提供。传入 `QDebug` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `map`：类型为 `const QMap<Key, T> &`。没有默认值，调用时必须提供。传入 `const QMap<Key, T> &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `template <typename Key, typename T> QDebug operator<<(QDebug debug, const QMultiHash<Key, T> &hash)`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QDebug` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`template <typename Key, typename T> QDebug`。
- 参数 `debug`：类型为 `QDebug`。没有默认值，调用时必须提供。传入 `QDebug` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `hash`：类型为 `const QMultiHash<Key, T> &`。没有默认值，调用时必须提供。传入 `const QMultiHash<Key, T> &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `template <typename Key, typename T> QDebug operator<<(QDebug debug, const QMultiMap<Key, T> &map)`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QDebug` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`template <typename Key, typename T> QDebug`。
- 参数 `debug`：类型为 `QDebug`。没有默认值，调用时必须提供。传入 `QDebug` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `map`：类型为 `const QMultiMap<Key, T> &`。没有默认值，调用时必须提供。传入 `const QMultiMap<Key, T> &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `template <typename T> QDebug operator<<(QDebug debug, const QSet<T> &set)`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QDebug` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`template <typename T> QDebug`。
- 参数 `debug`：类型为 `QDebug`。没有默认值，调用时必须提供。传入 `QDebug` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `set`：类型为 `const QSet<T> &`。没有默认值，调用时必须提供。传入 `const QSet<T> &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.3] template <typename T, qsizetype P> QDebug operator<<(QDebug debug, const QVarLengthArray<T, P> &array)`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QDebug` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`template <typename T, qsizetype P> QDebug`。
- 参数 `debug`：类型为 `QDebug`。没有默认值，调用时必须提供。传入 `QDebug` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `array`：类型为 `const QVarLengthArray<T, P> &`。没有默认值，调用时必须提供。传入 `const QVarLengthArray<T, P> &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.9] template <typename T, std::size_t N> QDebug operator<<(QDebug debug, const std::array<T, N> &array)`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QDebug` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`template <typename T, std::size_t N> QDebug`。
- 参数 `debug`：类型为 `QDebug`。没有默认值，调用时必须提供。传入 `QDebug` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `array`：类型为 `const std::array<T, N> &`。没有默认值，调用时必须提供。传入 `const std::array<T, N> &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `template <typename T, typename Alloc> QDebug operator<<(QDebug debug, const std::list<T, Alloc> &vec)`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QDebug` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`template <typename T, typename Alloc> QDebug`。
- 参数 `debug`：类型为 `QDebug`。没有默认值，调用时必须提供。传入 `QDebug` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `vec`：类型为 `const std::list<T, Alloc> &`。没有默认值，调用时必须提供。传入 `const std::list<T, Alloc> &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `template < typename Key, typename T, typename Compare, typename Alloc > QDebug operator<<(QDebug debug, const std::map<Key, T, Compare, Alloc> &map)`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QDebug` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`template < typename Key, typename T, typename Compare, typename Alloc > QDebug`。
- 参数 `debug`：类型为 `QDebug`。没有默认值，调用时必须提供。传入 `QDebug` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `map`：类型为 `const std::map<Key, T, Compare, Alloc> &`。没有默认值，调用时必须提供。传入 `const std::map<Key, T, Compare, Alloc> &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `template < typename Key, typename T, typename Compare, typename Alloc > QDebug operator<<(QDebug debug, const std::multimap<Key, T, Compare, Alloc> &map)`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QDebug` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`template < typename Key, typename T, typename Compare, typename Alloc > QDebug`。
- 参数 `debug`：类型为 `QDebug`。没有默认值，调用时必须提供。传入 `QDebug` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `map`：类型为 `const std::multimap<Key, T, Compare, Alloc> &`。没有默认值，调用时必须提供。传入 `const std::multimap<Key, T, Compare, Alloc> &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.9] template < typename Key, typename Compare, typename Alloc > QDebug operator<<(QDebug debug, const std::multiset<Key, Compare, Alloc> &multiset)`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QDebug` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`template < typename Key, typename Compare, typename Alloc > QDebug`。
- 参数 `debug`：类型为 `QDebug`。没有默认值，调用时必须提供。传入 `QDebug` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `multiset`：类型为 `const std::multiset<Key, Compare, Alloc> &`。没有默认值，调用时必须提供。传入 `const std::multiset<Key, Compare, Alloc> &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `template <typename T1, typename T2> QDebug operator<<(QDebug debug, const std::pair<T1, T2> &pair)`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QDebug` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`template <typename T1, typename T2> QDebug`。
- 参数 `debug`：类型为 `QDebug`。没有默认值，调用时必须提供。传入 `QDebug` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `pair`：类型为 `const std::pair<T1, T2> &`。没有默认值，调用时必须提供。传入 `const std::pair<T1, T2> &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.9] template < typename Key, typename Compare, typename Alloc > QDebug operator<<(QDebug debug, const std::set<Key, Compare, Alloc> &set)`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QDebug` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`template < typename Key, typename Compare, typename Alloc > QDebug`。
- 参数 `debug`：类型为 `QDebug`。没有默认值，调用时必须提供。传入 `QDebug` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `set`：类型为 `const std::set<Key, Compare, Alloc> &`。没有默认值，调用时必须提供。传入 `const std::set<Key, Compare, Alloc> &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.9] template < typename Key, typename T, typename Hash, typename KeyEqual, typename Alloc > QDebug operator<<(QDebug debug, const std::unordered_map<Key, T, Hash, KeyEqual, Alloc> &map)`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QDebug` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`template < typename Key, typename T, typename Hash, typename KeyEqual, typename Alloc > QDebug`。
- 参数 `debug`：类型为 `QDebug`。没有默认值，调用时必须提供。传入 `QDebug` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `map`：类型为 `const std::unordered_map<Key, T, Hash, KeyEqual, Alloc> &`。没有默认值，调用时必须提供。传入 `const std::unordered_map<Key, T, Hash, KeyEqual, Alloc> &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.9] template < typename Key, typename Hash, typename KeyEqual, typename Alloc > QDebug operator<<(QDebug debug, const std::unordered_set<Key, Hash, KeyEqual, Alloc> &unordered_set)`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QDebug` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`template < typename Key, typename Hash, typename KeyEqual, typename Alloc > QDebug`。
- 参数 `debug`：类型为 `QDebug`。没有默认值，调用时必须提供。传入 `QDebug` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `unordered_set`：类型为 `const std::unordered_set<Key, Hash, KeyEqual, Alloc> &`。没有默认值，调用时必须提供。传入 `const std::unordered_set<Key, Hash, KeyEqual, Alloc> &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `template <typename T, typename Alloc> QDebug operator<<(QDebug debug, const std::vector<T, Alloc> &vec)`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QDebug` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`template <typename T, typename Alloc> QDebug`。
- 参数 `debug`：类型为 `QDebug`。没有默认值，调用时必须提供。传入 `QDebug` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `vec`：类型为 `const std::vector<T, Alloc> &`。没有默认值，调用时必须提供。传入 `const std::vector<T, Alloc> &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.9] template <typename T, QDebug::if_ordering_type<T> = true> QDebug operator<<(QDebug debug, T t)`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QDebug` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`template <typename T, QDebug::if_ordering_type<T> = true> QDebug`。
- 参数 `debug`：类型为 `QDebug`。没有默认值，调用时必须提供。传入 `QDebug` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `t`：类型为 `T`。没有默认值，调用时必须提供。传入 `T` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `template <typename T> QDebug operator<<(QDebug debug, const QContiguousCache<T> &cache)`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QDebug` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`template <typename T> QDebug`。
- 参数 `debug`：类型为 `QDebug`。没有默认值，调用时必须提供。传入 `QDebug` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `cache`：类型为 `const QContiguousCache<T> &`。没有默认值，调用时必须提供。传入 `const QContiguousCache<T> &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `template <typename T> QDebug operator<<(QDebug debug, const QFlags<T> &flags)`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QDebug` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`template <typename T> QDebug`。
- 参数 `debug`：类型为 `QDebug`。没有默认值，调用时必须提供。传入 `QDebug` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `flags`：类型为 `const QFlags<T> &`。没有默认值，调用时必须提供。标志位组合。可以用按位或组合，调用前确认哪些标志互斥、哪些标志需要同时出现。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `template <typename Key, typename T> QDebug operator<<(QDebug debug, const QHash<Key, T> &hash)`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QDebug` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`template <typename Key, typename T> QDebug`。
- 参数 `debug`：类型为 `QDebug`。没有默认值，调用时必须提供。传入 `QDebug` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `hash`：类型为 `const QHash<Key, T> &`。没有默认值，调用时必须提供。传入 `const QHash<Key, T> &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QDebug qCritical()`

**API 类别：** 宏说明

**中文解读：** `QDebug::qCritical` 用于计算、查询或取得与“q、Critical”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QDebug`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QDebug`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QDebug qDebug()`

**API 类别：** 宏说明

**中文解读：** `QDebug::qDebug` 用于计算、查询或取得与“q、调试输出”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QDebug`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QDebug`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QDebug qFatal()`

**API 类别：** 宏说明

**中文解读：** `QDebug::qFatal` 用于计算、查询或取得与“q、Fatal”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QDebug`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QDebug`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QDebug qInfo()`

**API 类别：** 宏说明

**中文解读：** `QDebug::qInfo` 用于计算、查询或取得与“q、Info”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QDebug`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QDebug`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QDebug qWarning()`

**API 类别：** 宏说明

**中文解读：** `QDebug::qWarning` 用于计算、查询或取得与“q、Warning”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QDebug`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QDebug`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `(since 6.5) QDebug & operator<<(const std::basic_string<Char, Args...> &s)`

**API 类别：** 公有函数

**中文解读：** 这是 `QDebug` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QDebug &`。
- 参数 `s`：类型为 `const std::basic_string<Char, Args...> &`。没有默认值，调用时必须提供。传入 `const std::basic_string<Char, Args...> &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

## 6. 深入实践与常见坑

### 生命周期和资源边界

日志上下文通常是一次消息表达式的临时对象；自定义 message handler 的安装和卸载要覆盖整个使用期，处理器内部不要递归调用会再次触发日志的代码。

### 状态和错误边界

日志是否输出受级别、类别规则、编译宏和运行时过滤影响。看到某条消息缺失时，要区分代码没有执行、日志级别被过滤、上下文被关闭和 handler 改写输出。

### 线程边界

日志可能来自多个线程，handler 必须考虑并发、输出原子性和不能阻塞业务线程；不要在 handler 中访问未加锁的 GUI 控件。

### 最容易出现的错误

不要用 qFatal 代替普通错误处理；不要在 handler 里再次触发同类日志；不要把日志文本当作稳定的程序接口；注意 release 构建中的上下文宏和过滤规则。

### 版本和平台

本文档以 Qt 6.11.1 为依据。涉及平台后端、编解码器、数据库驱动、窗口风格、编译器特性或标注了版本号的 API 时，要把版本条件当作使用约束，而不是只看函数是否能补全。

## 7. 使用边界

`QDebug` 所属机制类型：Qt 日志与诊断机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
