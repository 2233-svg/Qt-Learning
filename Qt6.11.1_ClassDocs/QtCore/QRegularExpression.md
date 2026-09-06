# QRegularExpression

> Qt 6.11.1 · Qt Core

## 1. 先建立直觉

**一句话定位：** 正则表达式模式对象，负责编译匹配规则并创建匹配结果。

**模块背景：** Qt Core 提供对象模型、事件循环、容器、字符串、文件、线程、时间和元对象系统等基础能力。

### 这是什么

`QRegularExpression`：正则表达式模式对象，负责编译匹配规则并创建匹配结果。

**内部模型：** 这类类型通常可以按值传递、复制和返回。许多 Qt 容器、字符串和图像采用隐式共享：复制时共享数据，发生写操作时才 detach。这样便于 API 传值，但获取原始指针或长期持有引用时必须考虑对象修改和生命周期。

**适用场景：** 先确认值的有效性和表示格式，再调用查询、转换或修改 API；处理文本时区分 Unicode 和字节编码，处理图像时确认 format，处理 URL/路径时使用 Qt 的解析 API 而不是手写字符串规则。

**典型调用链：** 构造或取得有效对象 -> 检查初始状态 -> 调用与本类职责对应的 API -> 验证返回值/通知 -> 处理无效值和资源边界。

**先记住的坑：** 不要把空值当成业务成功；不要保存临时对象的内部指针；不要把 QString 当二进制缓冲区；不要假定隐式共享让并发写入自动安全。

## 2. 依赖与对象关系

- 头文件：`#include <QRegularExpression>`
- 继承自：未在类页中列出
- 直接派生类：未在类页中列出

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Core)
target_link_libraries(mytarget PRIVATE Qt6::Core)
```

**继承带来的规则：** 它是值类型或不直接使用 QObject 对象模型，重点放在数据语义、拷贝/移动成本和参数有效性。

### 工作机制

这类类型通常可以按值传递、复制和返回。许多 Qt 容器、字符串和图像采用隐式共享：复制时共享数据，发生写操作时才 detach。这样便于 API 传值，但获取原始指针或长期持有引用时必须考虑对象修改和生命周期。

### 状态、生命周期和线程

**生命周期：** 值对象由作用域、容器或调用者管理，不使用 parent 和 deleteLater。跨线程传递副本通常比传递 QObject 安全，但共享数据在写入时仍可能发生复制，性能和内存峰值要结合数据规模判断。

**状态与结果：** 重点区分空值、无效值、默认值和已初始化值。例如空字符串、空 URL、null 图像和无效索引不一定表示同一件事；转换函数的失败结果要通过对应的状态查询确认。

**线程与事件循环：** 值类型本身通常可以复制后跨线程传递；不要把 data()/bits()/constData() 得到的指针当成跨线程长期有效的所有权。大对象频繁写入会触发 detach，应避免不必要的复制和格式转换。

## 3. 直接使用

先确认值的有效性和表示格式，再调用查询、转换或修改 API；处理文本时区分 Unicode 和字节编码，处理图像时确认 format，处理 URL/路径时使用 Qt 的解析 API 而不是手写字符串规则。 使用时通常按这个过程组织：构造或取得有效对象 -> 检查初始状态 -> 调用与本类职责对应的 API -> 验证返回值/通知 -> 处理无效值和资源边界。
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 公有类型

- `enum MatchOption { NoMatchOption, AnchoredMatchOption, AnchorAtOffsetMatchOption, DontCheckSubjectStringMatchOption }`
- `flags MatchOptions`
- `enum MatchType { NormalMatch, PartialPreferCompleteMatch, PartialPreferFirstMatch, NoMatch }`
- `enum PatternOption { NoPatternOption, CaseInsensitiveOption, DotMatchesEverythingOption, MultilineOption, ExtendedPatternSyntaxOption, …, UseUnicodePropertiesOption }`
- `flags PatternOptions`
- `(since 6.0) enum WildcardConversionOption { DefaultWildcardConversion, UnanchoredWildcardConversion, NonPathWildcardConversion }`
- `flags WildcardConversionOptions`

### 公有函数

- `QRegularExpression()`
- `QRegularExpression(const QString &pattern, QRegularExpression::PatternOptions options = NoPatternOption)`
- `QRegularExpression(const QRegularExpression &re)`
- `(since 6.1) QRegularExpression(QRegularExpression &&re)`
- `~QRegularExpression()`
- `int captureCount() const`
- `QString errorString() const`
- `QRegularExpressionMatchIterator globalMatch(const QString &subject, qsizetype offset = 0, QRegularExpression::MatchType matchType = NormalMatch, QRegularExpression::MatchOptions matchOptions = NoMatchOption) const`
- `(since 6.5) QRegularExpressionMatchIterator globalMatchView(QStringView subjectView, qsizetype offset = 0, QRegularExpression::MatchType matchType = NormalMatch, QRegularExpression::MatchOptions matchOptions = NoMatchOption) const`
- `bool isValid() const`
- `QRegularExpressionMatch match(const QString &subject, qsizetype offset = 0, QRegularExpression::MatchType matchType = NormalMatch, QRegularExpression::MatchOptions matchOptions = NoMatchOption) const`
- `(since 6.5) QRegularExpressionMatch matchView(QStringView subjectView, qsizetype offset = 0, QRegularExpression::MatchType matchType = NormalMatch, QRegularExpression::MatchOptions matchOptions = NoMatchOption) const`
- `QStringList namedCaptureGroups() const`
- `void optimize() const`
- `QString pattern() const`
- `qsizetype patternErrorOffset() const`
- `QRegularExpression::PatternOptions patternOptions() const`
- `void setPattern(const QString &pattern)`
- `void setPatternOptions(QRegularExpression::PatternOptions options)`
- `void swap(QRegularExpression &other)`
- `QRegularExpression & operator=(QRegularExpression &&re)`
- `QRegularExpression & operator=(const QRegularExpression &re)`

### 静态公有成员

- `QString anchoredPattern(QStringView expression)`
- `QString anchoredPattern(const QString &expression)`
- `QString escape(QStringView str)`
- `QString escape(const QString &str)`
- `(since 6.0) QRegularExpression fromWildcard(QStringView pattern, Qt::CaseSensitivity cs = Qt::CaseInsensitive, QRegularExpression::WildcardConversionOptions options = DefaultWildcardConversion)`
- `QString wildcardToRegularExpression(QStringView pattern, QRegularExpression::WildcardConversionOptions options = DefaultWildcardConversion)`
- `QString wildcardToRegularExpression(const QString &pattern, QRegularExpression::WildcardConversionOptions options = DefaultWildcardConversion)`

### 相关非成员函数

- `size_t qHash(const QRegularExpression &key, size_t seed = 0)`
- `bool operator!=(const QRegularExpression &lhs, const QRegularExpression &rhs)`
- `QDataStream & operator<<(QDataStream &out, const QRegularExpression &re)`
- `QDebug operator<<(QDebug debug, QRegularExpression::PatternOptions patternOptions)`
- `QDebug operator<<(QDebug debug, const QRegularExpression &re)`
- `bool operator==(const QRegularExpression &lhs, const QRegularExpression &rhs)`
- `QDataStream & operator>>(QDataStream &in, QRegularExpression &re)`

## 5. API 逐个说明

这里直接说明每个公开成员解决什么问题、参数代表什么、返回什么、会改变什么以及使用时容易出现什么问题。每一个公开签名都会有对应的中文解释。

本类共整理 46 个公开成员条目；没有独立长描述的 API 也会根据签名、类型和所属机制给出使用说明。

### `enum QRegularExpression::MatchOptionflags QRegularExpression::MatchOptions`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QRegularExpression` 暴露的类型声明 `匹配、Optionflags`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 属性类型：`:MatchOptionflags QRegularExpression::MatchOptions`。
- 属性名：`QRegularExpression`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `enum QRegularExpression::MatchType`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QRegularExpression` 暴露的类型声明 `匹配、类型`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 属性类型：`:MatchType`。
- 属性名：`QRegularExpression`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `enum QRegularExpression::PatternOptionflags QRegularExpression::PatternOptions`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QRegularExpression` 暴露的类型声明 `Pattern、Optionflags`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 属性类型：`:PatternOptionflags QRegularExpression::PatternOptions`。
- 属性名：`QRegularExpression`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.0] enum QRegularExpression::WildcardConversionOptionflags QRegularExpression::WildcardConversionOptions`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QRegularExpression` 暴露的类型声明 `Wildcard、Conversion、Optionflags`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 属性类型：`:WildcardConversionOptionflags QRegularExpression::WildcardConversionOptions`。
- 属性名：`QRegularExpression`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QRegularExpression::QRegularExpression()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QRegularExpression` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[explicit] QRegularExpression::QRegularExpression(const QString &pattern, QRegularExpression::PatternOptions options = NoPatternOption)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QRegularExpression` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `pattern`：类型为 `const QString &`。没有默认值，调用时必须提供。匹配模式或格式模板；要确认转义规则、大小写策略和编译失败时的状态。
- 参数 `options`：类型为 `QRegularExpression::PatternOptions`。默认值为 `NoPatternOption`。传入 `QRegularExpression::PatternOptions` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] QRegularExpression::QRegularExpression(const QRegularExpression &re)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QRegularExpression` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `re`：类型为 `const QRegularExpression &`。没有默认值，调用时必须提供。传入 `const QRegularExpression &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[constexpr noexcept, since 6.1] QRegularExpression::QRegularExpression(QRegularExpression &&re)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QRegularExpression` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `re`：类型为 `QRegularExpression &&`。没有默认值，调用时必须提供。传入 `QRegularExpression &&` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] QRegularExpression::~QRegularExpression()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QRegularExpression` 的析构函数。对象销毁时资源、子对象和连接会按 Qt 规则释放；异步对象要先停止任务或使用 deleteLater，避免回调访问已经不存在的实例。

**签名拆解：**

- 返回值：析构函数，无返回值。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] QString QRegularExpression::anchoredPattern(QStringView expression)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `anchoredPattern`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QString`。
- 参数 `expression`：类型为 `QStringView`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] QString QRegularExpression::anchoredPattern(const QString &expression)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `anchoredPattern`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QString`。
- 参数 `expression`：类型为 `const QString &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `int QRegularExpression::captureCount() const`

**API 类别：** 成员函数说明

**中文解读：** `QRegularExpression::captureCount` 用于计算、查询或取得与“capture、数量统计”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `int`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`int`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString QRegularExpression::errorString() const`

**API 类别：** 成员函数说明

**中文解读：** `QRegularExpression::errorString` 用于计算、查询或取得与“错误、字符串”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QString`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QString`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] QString QRegularExpression::escape(QStringView str)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `escape`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QString`。
- 参数 `str`：类型为 `QStringView`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] QString QRegularExpression::escape(const QString &str)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `escape`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QString`。
- 参数 `str`：类型为 `const QString &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static, since 6.0] QRegularExpression QRegularExpression::fromWildcard(QStringView pattern, Qt::CaseSensitivity cs = Qt::CaseInsensitive, QRegularExpression::WildcardConversionOptions options = DefaultWildcardConversion)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `fromWildcard`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QRegularExpression`。
- 参数 `pattern`：类型为 `QStringView`。没有默认值，调用时必须提供。匹配模式或格式模板；要确认转义规则、大小写策略和编译失败时的状态。
- 参数 `cs`：类型为 `Qt::CaseSensitivity`。默认值为 `Qt::CaseInsensitive`。传入 `Qt::CaseSensitivity` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `options`：类型为 `QRegularExpression::WildcardConversionOptions`。默认值为 `DefaultWildcardConversion`。传入 `QRegularExpression::WildcardConversionOptions` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QRegularExpressionMatchIterator QRegularExpression::globalMatch(const QString &subject, qsizetype offset = 0, QRegularExpression::MatchType matchType = NormalMatch, QRegularExpression::MatchOptions matchOptions = NoMatchOption) const`

**API 类别：** 成员函数说明

**中文解读：** `QRegularExpression::globalMatch` 用于计算、查询或取得与“global、匹配”相关的操作。调用时要先确认当前状态和 `subject`、`offset`、`matchType`、`matchOptions` 的有效范围；返回类型是 `QRegularExpressionMatchIterator`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QRegularExpressionMatchIterator`。
- 参数 `subject`：类型为 `const QString &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。
- 参数 `offset`：类型为 `qsizetype`。默认值为 `0`。传入 `qsizetype` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `matchType`：类型为 `QRegularExpression::MatchType`。默认值为 `NormalMatch`。传入 `QRegularExpression::MatchType` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `matchOptions`：类型为 `QRegularExpression::MatchOptions`。默认值为 `NoMatchOption`。传入 `QRegularExpression::MatchOptions` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.5] QRegularExpressionMatchIterator QRegularExpression::globalMatchView(QStringView subjectView, qsizetype offset = 0, QRegularExpression::MatchType matchType = NormalMatch, QRegularExpression::MatchOptions matchOptions = NoMatchOption) const`

**API 类别：** 成员函数说明

**中文解读：** `QRegularExpression::globalMatchView` 用于计算、查询或取得与“global、匹配、View”相关的操作。调用时要先确认当前状态和 `subjectView`、`offset`、`matchType`、`matchOptions` 的有效范围；返回类型是 `QRegularExpressionMatchIterator`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QRegularExpressionMatchIterator`。
- 参数 `subjectView`：类型为 `QStringView`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。
- 参数 `offset`：类型为 `qsizetype`。默认值为 `0`。传入 `qsizetype` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `matchType`：类型为 `QRegularExpression::MatchType`。默认值为 `NormalMatch`。传入 `QRegularExpression::MatchType` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `matchOptions`：类型为 `QRegularExpression::MatchOptions`。默认值为 `NoMatchOption`。传入 `QRegularExpression::MatchOptions` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QRegularExpression::isValid() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `isValid`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QRegularExpressionMatch QRegularExpression::match(const QString &subject, qsizetype offset = 0, QRegularExpression::MatchType matchType = NormalMatch, QRegularExpression::MatchOptions matchOptions = NoMatchOption) const`

**API 类别：** 成员函数说明

**中文解读：** `QRegularExpression::match` 用于计算、查询或取得与“匹配”相关的操作。调用时要先确认当前状态和 `subject`、`offset`、`matchType`、`matchOptions` 的有效范围；返回类型是 `QRegularExpressionMatch`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QRegularExpressionMatch`。
- 参数 `subject`：类型为 `const QString &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。
- 参数 `offset`：类型为 `qsizetype`。默认值为 `0`。传入 `qsizetype` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `matchType`：类型为 `QRegularExpression::MatchType`。默认值为 `NormalMatch`。传入 `QRegularExpression::MatchType` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `matchOptions`：类型为 `QRegularExpression::MatchOptions`。默认值为 `NoMatchOption`。传入 `QRegularExpression::MatchOptions` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.5] QRegularExpressionMatch QRegularExpression::matchView(QStringView subjectView, qsizetype offset = 0, QRegularExpression::MatchType matchType = NormalMatch, QRegularExpression::MatchOptions matchOptions = NoMatchOption) const`

**API 类别：** 成员函数说明

**中文解读：** `QRegularExpression::matchView` 用于计算、查询或取得与“匹配、View”相关的操作。调用时要先确认当前状态和 `subjectView`、`offset`、`matchType`、`matchOptions` 的有效范围；返回类型是 `QRegularExpressionMatch`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QRegularExpressionMatch`。
- 参数 `subjectView`：类型为 `QStringView`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。
- 参数 `offset`：类型为 `qsizetype`。默认值为 `0`。传入 `qsizetype` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `matchType`：类型为 `QRegularExpression::MatchType`。默认值为 `NormalMatch`。传入 `QRegularExpression::MatchType` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `matchOptions`：类型为 `QRegularExpression::MatchOptions`。默认值为 `NoMatchOption`。传入 `QRegularExpression::MatchOptions` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QStringList QRegularExpression::namedCaptureGroups() const`

**API 类别：** 成员函数说明

**中文解读：** `QRegularExpression::namedCaptureGroups` 用于计算、查询或取得与“named、Capture、Groups”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QStringList`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QStringList`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QRegularExpression::optimize() const`

**API 类别：** 成员函数说明

**中文解读：** `QRegularExpression::optimize` 用于执行与“optimize”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString QRegularExpression::pattern() const`

**API 类别：** 成员函数说明

**中文解读：** `QRegularExpression::pattern` 用于计算、查询或取得与“pattern”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QString`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QString`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `qsizetype QRegularExpression::patternErrorOffset() const`

**API 类别：** 成员函数说明

**中文解读：** `QRegularExpression::patternErrorOffset` 用于计算、查询或取得与“pattern、错误、Offset”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `qsizetype`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`qsizetype`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QRegularExpression::PatternOptions QRegularExpression::patternOptions() const`

**API 类别：** 成员函数说明

**中文解读：** `QRegularExpression::patternOptions` 用于计算、查询或取得与“pattern、Options”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QRegularExpression::PatternOptions`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QRegularExpression::PatternOptions`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QRegularExpression::setPattern(const QString &pattern)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setPattern`。调用它会改变 `QRegularExpression` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `pattern`：类型为 `const QString &`。没有默认值，调用时必须提供。匹配模式或格式模板；要确认转义规则、大小写策略和编译失败时的状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QRegularExpression::setPatternOptions(QRegularExpression::PatternOptions options)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setPatternOptions`。调用它会改变 `QRegularExpression` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `options`：类型为 `QRegularExpression::PatternOptions`。没有默认值，调用时必须提供。传入 `QRegularExpression::PatternOptions` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] void QRegularExpression::swap(QRegularExpression &other)`

**API 类别：** 成员函数说明

**中文解读：** `QRegularExpression::swap` 用于执行与“swap”相关的操作。调用时要先确认当前状态和 `other` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `other`：类型为 `QRegularExpression &`。没有默认值，调用时必须提供。参与比较、合并或交换的另一个对象；要确认它与当前对象属于同一类型或兼容协议。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] QString QRegularExpression::wildcardToRegularExpression(QStringView pattern, QRegularExpression::WildcardConversionOptions options = DefaultWildcardConversion)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `wildcardToRegularExpression`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QString`。
- 参数 `pattern`：类型为 `QStringView`。没有默认值，调用时必须提供。匹配模式或格式模板；要确认转义规则、大小写策略和编译失败时的状态。
- 参数 `options`：类型为 `QRegularExpression::WildcardConversionOptions`。默认值为 `DefaultWildcardConversion`。传入 `QRegularExpression::WildcardConversionOptions` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] QString QRegularExpression::wildcardToRegularExpression(const QString &pattern, QRegularExpression::WildcardConversionOptions options = DefaultWildcardConversion)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `wildcardToRegularExpression`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QString`。
- 参数 `pattern`：类型为 `const QString &`。没有默认值，调用时必须提供。匹配模式或格式模板；要确认转义规则、大小写策略和编译失败时的状态。
- 参数 `options`：类型为 `QRegularExpression::WildcardConversionOptions`。默认值为 `DefaultWildcardConversion`。传入 `QRegularExpression::WildcardConversionOptions` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] QRegularExpression &QRegularExpression::operator=(QRegularExpression &&re)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QRegularExpression` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QRegularExpression &`。
- 参数 `re`：类型为 `QRegularExpression &&`。没有默认值，调用时必须提供。传入 `QRegularExpression &&` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] QRegularExpression &QRegularExpression::operator=(const QRegularExpression &re)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QRegularExpression` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QRegularExpression &`。
- 参数 `re`：类型为 `const QRegularExpression &`。没有默认值，调用时必须提供。传入 `const QRegularExpression &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] size_t qHash(const QRegularExpression &key, size_t seed = 0)`

**API 类别：** 相关非成员函数

**中文解读：** `QRegularExpression::qHash` 用于计算、查询或取得与“q、Hash”相关的操作。调用时要先确认当前状态和 `key`、`seed` 的有效范围；返回类型是 `size_t`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`size_t`。
- 参数 `key`：类型为 `const QRegularExpression &`。没有默认值，调用时必须提供。键、字段名或索引键；应确认编码、大小写规则和键不存在时的返回值。
- 参数 `seed`：类型为 `size_t`。默认值为 `0`。传入 `size_t` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] bool operator!=(const QRegularExpression &lhs, const QRegularExpression &rhs)`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QRegularExpression` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`bool`。
- 参数 `lhs`：类型为 `const QRegularExpression &`。没有默认值，调用时必须提供。运算符左侧的值；要注意返回新值还是修改当前对象。
- 参数 `rhs`：类型为 `const QRegularExpression &`。没有默认值，调用时必须提供。运算符右侧的另一个值；通常不会被当前 API 接管所有权。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QDataStream &operator<<(QDataStream &out, const QRegularExpression &re)`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QRegularExpression` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QDataStream &`。
- 参数 `out`：类型为 `QDataStream &`。没有默认值，调用时必须提供。传入 `QDataStream &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `re`：类型为 `const QRegularExpression &`。没有默认值，调用时必须提供。传入 `const QRegularExpression &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QDebug operator<<(QDebug debug, QRegularExpression::PatternOptions patternOptions)`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QRegularExpression` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QDebug`。
- 参数 `debug`：类型为 `QDebug`。没有默认值，调用时必须提供。传入 `QDebug` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `patternOptions`：类型为 `QRegularExpression::PatternOptions`。没有默认值，调用时必须提供。传入 `QRegularExpression::PatternOptions` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QDebug operator<<(QDebug debug, const QRegularExpression &re)`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QRegularExpression` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QDebug`。
- 参数 `debug`：类型为 `QDebug`。没有默认值，调用时必须提供。传入 `QDebug` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `re`：类型为 `const QRegularExpression &`。没有默认值，调用时必须提供。传入 `const QRegularExpression &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] bool operator==(const QRegularExpression &lhs, const QRegularExpression &rhs)`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QRegularExpression` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`bool`。
- 参数 `lhs`：类型为 `const QRegularExpression &`。没有默认值，调用时必须提供。运算符左侧的值；要注意返回新值还是修改当前对象。
- 参数 `rhs`：类型为 `const QRegularExpression &`。没有默认值，调用时必须提供。运算符右侧的另一个值；通常不会被当前 API 接管所有权。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QDataStream &operator>>(QDataStream &in, QRegularExpression &re)`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QRegularExpression` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QDataStream &`。
- 参数 `in`：类型为 `QDataStream &`。没有默认值，调用时必须提供。传入 `QDataStream &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `re`：类型为 `QRegularExpression &`。没有默认值，调用时必须提供。传入 `QRegularExpression &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `enum MatchOption { NoMatchOption, AnchoredMatchOption, AnchorAtOffsetMatchOption, DontCheckSubjectStringMatchOption }`

**API 类别：** 公有类型

**中文解读：** 这是 `QRegularExpression` 暴露的类型声明 `匹配、Option`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 这是供该类其他 API 使用的枚举/标志类型；传值前要确认枚举值的语义和适用状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `flags MatchOptions`

**API 类别：** 公有类型

**中文解读：** 这是 `QRegularExpression` 的 `标志` 成员声明。它通常作为其他 API 的类型、常量或配置入口使用；先确认可用值和适用状态，再结合本类的创建、核心操作和清理流程使用。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `enum PatternOption { NoPatternOption, CaseInsensitiveOption, DotMatchesEverythingOption, MultilineOption, ExtendedPatternSyntaxOption, …, UseUnicodePropertiesOption }`

**API 类别：** 公有类型

**中文解读：** 这是 `QRegularExpression` 暴露的类型声明 `Pattern、Option`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 这是供该类其他 API 使用的枚举/标志类型；传值前要确认枚举值的语义和适用状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `flags PatternOptions`

**API 类别：** 公有类型

**中文解读：** 这是 `QRegularExpression` 的 `标志` 成员声明。它通常作为其他 API 的类型、常量或配置入口使用；先确认可用值和适用状态，再结合本类的创建、核心操作和清理流程使用。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `(since 6.0) enum WildcardConversionOption { DefaultWildcardConversion, UnanchoredWildcardConversion, NonPathWildcardConversion }`

**API 类别：** 公有类型

**中文解读：** 这是 `QRegularExpression` 暴露的类型声明 `Wildcard、Conversion、Option`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 这是供该类其他 API 使用的枚举/标志类型；传值前要确认枚举值的语义和适用状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `flags WildcardConversionOptions`

**API 类别：** 公有类型

**中文解读：** 这是 `QRegularExpression` 的 `标志` 成员声明。它通常作为其他 API 的类型、常量或配置入口使用；先确认可用值和适用状态，再结合本类的创建、核心操作和清理流程使用。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

## 6. 深入实践与常见坑

### 生命周期和资源边界

值对象由作用域、容器或调用者管理，不使用 parent 和 deleteLater。跨线程传递副本通常比传递 QObject 安全，但共享数据在写入时仍可能发生复制，性能和内存峰值要结合数据规模判断。

### 状态和错误边界

重点区分空值、无效值、默认值和已初始化值。例如空字符串、空 URL、null 图像和无效索引不一定表示同一件事；转换函数的失败结果要通过对应的状态查询确认。

### 线程边界

值类型本身通常可以复制后跨线程传递；不要把 data()/bits()/constData() 得到的指针当成跨线程长期有效的所有权。大对象频繁写入会触发 detach，应避免不必要的复制和格式转换。

### 最容易出现的错误

不要把空值当成业务成功；不要保存临时对象的内部指针；不要把 QString 当二进制缓冲区；不要假定隐式共享让并发写入自动安全。

### 版本和平台

本文档以 Qt 6.11.1 为依据。涉及平台后端、编解码器、数据库驱动、窗口风格、编译器特性或标注了版本号的 API 时，要把版本条件当作使用约束，而不是只看函数是否能补全。

## 7. 使用边界

`QRegularExpression` 所属机制类型：Qt 值类型与隐式共享机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
