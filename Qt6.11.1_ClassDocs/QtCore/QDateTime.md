# QDateTime

> Qt 6.11.1 · Qt Core

## 1. 先建立直觉

**一句话定位：** 日期加时间值类型，负责时间点、时区、时间戳、比较、解析和格式化。

**模块背景：** Qt Core 提供对象模型、事件循环、容器、字符串、文件、线程、时间和元对象系统等基础能力。

### 这是什么

`QDateTime`：日期加时间值类型，负责时间点、时区、时间戳、比较、解析和格式化。

**内部模型：** 这类类型通常可以按值传递、复制和返回。许多 Qt 容器、字符串和图像采用隐式共享：复制时共享数据，发生写操作时才 detach。这样便于 API 传值，但获取原始指针或长期持有引用时必须考虑对象修改和生命周期。

**适用场景：** 先确认值的有效性和表示格式，再调用查询、转换或修改 API；处理文本时区分 Unicode 和字节编码，处理图像时确认 format，处理 URL/路径时使用 Qt 的解析 API 而不是手写字符串规则。

**典型调用链：** 构造或取得有效对象 -> 检查初始状态 -> 调用与本类职责对应的 API -> 验证返回值/通知 -> 处理无效值和资源边界。

**先记住的坑：** 不要把空值当成业务成功；不要保存临时对象的内部指针；不要把 QString 当二进制缓冲区；不要假定隐式共享让并发写入自动安全。

## 2. 依赖与对象关系

- 头文件：`#include <QDateTime>`
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

- `(since 6.7) enum class TransitionResolution { Reject, RelativeToBefore, RelativeToAfter, PreferBefore, PreferAfter, …, PreferDaylightSaving }`
- `enum class YearRange { First, Last }`

### 公有函数

- `QDateTime(QDate date, QTime time, const QTimeZone &timeZone, QDateTime::TransitionResolution resolve = TransitionResolution::LegacyBehavior)`
- `QDateTime()`
- `(since 6.5) QDateTime(QDate date, QTime time, QDateTime::TransitionResolution resolve = TransitionResolution::LegacyBehavior)`
- `QDateTime(const QDateTime &other)`
- `QDateTime(QDateTime &&other)`
- `~QDateTime()`
- `QDateTime addDays(qint64 ndays) const`
- `(since 6.4) QDateTime addDuration(std::chrono::milliseconds msecs) const`
- `QDateTime addMSecs(qint64 msecs) const`
- `QDateTime addMonths(int nmonths) const`
- `QDateTime addSecs(qint64 s) const`
- `QDateTime addYears(int nyears) const`
- `QDate date() const`
- `qint64 daysTo(const QDateTime &other) const`
- `bool isDaylightTime() const`
- `bool isNull() const`
- `bool isValid() const`
- `qint64 msecsTo(const QDateTime &other) const`
- `int offsetFromUtc() const`
- `qint64 secsTo(const QDateTime &other) const`
- `void setDate(QDate date, QDateTime::TransitionResolution resolve = TransitionResolution::LegacyBehavior)`
- `void setMSecsSinceEpoch(qint64 msecs)`
- `void setSecsSinceEpoch(qint64 secs)`
- `void setTime(QTime time, QDateTime::TransitionResolution resolve = TransitionResolution::LegacyBehavior)`
- `void setTimeZone(const QTimeZone &toZone, QDateTime::TransitionResolution resolve = TransitionResolution::LegacyBehavior)`
- `void swap(QDateTime &other)`
- `QTime time() const`
- `(since 6.5) QTimeZone timeRepresentation() const`
- `Qt::TimeSpec timeSpec() const`
- `QTimeZone timeZone() const`
- `QString timeZoneAbbreviation() const`
- `CFDateRef toCFDate() const`
- `QDateTime toLocalTime() const`
- `qint64 toMSecsSinceEpoch() const`
- `NSDate * toNSDate() const`
- `QDateTime toOffsetFromUtc(int offsetSeconds) const`
- `qint64 toSecsSinceEpoch() const`
- `(since 6.4) std::chrono::sys_time<std::chrono::milliseconds> toStdSysMilliseconds() const`
- `(since 6.4) std::chrono::sys_seconds toStdSysSeconds() const`
- `QString toString(const QString &format, QCalendar cal) const`
- `QString toString(QStringView format) const`
- `QString toString(Qt::DateFormat format = Qt::TextDate) const`
- `QString toString(const QString &format) const`
- `QString toString(QStringView format, QCalendar cal) const`
- `QDateTime toTimeZone(const QTimeZone &timeZone) const`
- `QDateTime toUTC() const`
- `(since 6.4) QDateTime & operator+=(std::chrono::milliseconds duration)`
- `(since 6.4) QDateTime & operator-=(std::chrono::milliseconds duration)`
- `QDateTime & operator=(const QDateTime &other)`

### 静态公有成员

- `(since 6.5) QDateTime currentDateTime(const QTimeZone &zone)`
- `QDateTime currentDateTime()`
- `QDateTime currentDateTimeUtc()`
- `qint64 currentMSecsSinceEpoch()`
- `qint64 currentSecsSinceEpoch()`
- `QDateTime fromCFDate(CFDateRef date)`
- `QDateTime fromMSecsSinceEpoch(qint64 msecs, const QTimeZone &timeZone)`
- `QDateTime fromMSecsSinceEpoch(qint64 msecs)`
- `QDateTime fromNSDate(const NSDate *date)`
- `QDateTime fromSecsSinceEpoch(qint64 secs, const QTimeZone &timeZone)`
- `QDateTime fromSecsSinceEpoch(qint64 secs)`
- `(since 6.4) QDateTime fromStdLocalTime(const std::chrono::local_time<std::chrono::milliseconds> &time)`
- `(since 6.4) QDateTime fromStdTimePoint(const std::chrono::time_point<Clock, Duration> &time)`
- `(since 6.4) QDateTime fromStdTimePoint(const std::chrono::local_time<std::chrono::milliseconds> &time)`
- `(since 6.4) QDateTime fromStdTimePoint(std::chrono::time_point<std::chrono::system_clock, std::chrono::milliseconds> time)`
- `(since 6.4) QDateTime fromStdZonedTime(const int &time)`
- `QDateTime fromString(const QString &string, const QString &format, int baseYear, QCalendar cal)`
- `(since 6.0) QDateTime fromString(QStringView string, Qt::DateFormat format = Qt::TextDate)`
- `QDateTime fromString(const QString &string, Qt::DateFormat format = Qt::TextDate)`
- `(since 6.0) QDateTime fromString(QStringView string, QStringView format, QCalendar cal)`
- `(since 6.7) QDateTime fromString(QStringView string, QStringView format, int baseYear = QLocale::DefaultTwoDigitBaseYear)`
- `(since 6.0) QDateTime fromString(const QString &string, QStringView format, QCalendar cal)`
- `(since 6.7) QDateTime fromString(const QString &string, QStringView format, int baseYear = QLocale::DefaultTwoDigitBaseYear)`
- `QDateTime fromString(const QString &string, const QString &format, QCalendar cal)`
- `(since 6.7) QDateTime fromString(const QString &string, const QString &format, int baseYear = QLocale::DefaultTwoDigitBaseYear)`
- `(since 6.7) QDateTime fromString(QStringView string, QStringView format, int baseYear, QCalendar cal)`
- `(since 6.0) QDateTime fromString(const QString &string, QStringView format, int baseYear, QCalendar cal)`

### 相关非成员函数

- `bool operator!=(const QDateTime &lhs, const QDateTime &rhs)`
- `(since 6.4) QDateTime operator+(const QDateTime &dateTime, std::chrono::milliseconds duration)`
- `(since 6.4) QDateTime operator+(std::chrono::milliseconds duration, const QDateTime &dateTime)`
- `(since 6.4) std::chrono::milliseconds operator-(const QDateTime &lhs, const QDateTime &rhs)`
- `(since 6.4) QDateTime operator-(const QDateTime &dateTime, std::chrono::milliseconds duration)`
- `bool operator<(const QDateTime &lhs, const QDateTime &rhs)`
- `QDataStream & operator<<(QDataStream &out, const QDateTime &dateTime)`
- `bool operator<=(const QDateTime &lhs, const QDateTime &rhs)`
- `bool operator==(const QDateTime &lhs, const QDateTime &rhs)`
- `bool operator>(const QDateTime &lhs, const QDateTime &rhs)`
- `bool operator>=(const QDateTime &lhs, const QDateTime &rhs)`
- `QDataStream & operator>>(QDataStream &in, QDateTime &dateTime)`

## 5. API 逐个说明

这里直接说明每个公开成员解决什么问题、参数代表什么、返回什么、会改变什么以及使用时容易出现什么问题。每一个公开签名都会有对应的中文解释。

本类共整理 90 个公开成员条目；没有独立长描述的 API 也会根据签名、类型和所属机制给出使用说明。

### `[since 6.7] enum class QDateTime::TransitionResolution`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QDateTime` 暴露的类型声明 `class`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 属性类型：`:TransitionResolution`。
- 属性名：`QDateTime`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `enum class QDateTime::YearRange`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QDateTime` 暴露的类型声明 `class`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 属性类型：`:YearRange`。
- 属性名：`QDateTime`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QDateTime::QDateTime(QDate date, QTime time, const QTimeZone &timeZone, QDateTime::TransitionResolution resolve = TransitionResolution::LegacyBehavior)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QDateTime` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `date`：类型为 `QDate`。没有默认值，调用时必须提供。传入 `QDate` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `time`：类型为 `QTime`。没有默认值，调用时必须提供。传入 `QTime` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `timeZone`：类型为 `const QTimeZone &`。没有默认值，调用时必须提供。传入 `const QTimeZone &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `resolve`：类型为 `QDateTime::TransitionResolution`。默认值为 `TransitionResolution::LegacyBehavior`。传入 `QDateTime::TransitionResolution` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] QDateTime::QDateTime()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QDateTime` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.5] QDateTime::QDateTime(QDate date, QTime time, QDateTime::TransitionResolution resolve = TransitionResolution::LegacyBehavior)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QDateTime` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `date`：类型为 `QDate`。没有默认值，调用时必须提供。传入 `QDate` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `time`：类型为 `QTime`。没有默认值，调用时必须提供。传入 `QTime` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `resolve`：类型为 `QDateTime::TransitionResolution`。默认值为 `TransitionResolution::LegacyBehavior`。传入 `QDateTime::TransitionResolution` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] QDateTime::QDateTime(const QDateTime &other)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QDateTime` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `other`：类型为 `const QDateTime &`。没有默认值，调用时必须提供。参与比较、合并或交换的另一个对象；要确认它与当前对象属于同一类型或兼容协议。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] QDateTime::QDateTime(QDateTime &&other)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QDateTime` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `other`：类型为 `QDateTime &&`。没有默认值，调用时必须提供。参与比较、合并或交换的另一个对象；要确认它与当前对象属于同一类型或兼容协议。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] QDateTime::~QDateTime()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QDateTime` 的析构函数。对象销毁时资源、子对象和连接会按 Qt 规则释放；异步对象要先停止任务或使用 deleteLater，避免回调访问已经不存在的实例。

**签名拆解：**

- 返回值：析构函数，无返回值。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QDateTime QDateTime::addDays(qint64 ndays) const`

**API 类别：** 成员函数说明

**中文解读：** 这是向 `QDateTime` 添加依赖、数据或子对象的 API `addDays`。注意对象所有权、重复添加和添加后的通知；如果对应有 remove/take 接口，要明确谁负责移除后的生命周期。

**签名拆解：**

- 返回值：`QDateTime`。
- 参数 `ndays`：类型为 `qint64`。没有默认值，调用时必须提供。传入 `qint64` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.4] QDateTime QDateTime::addDuration(std::chrono::milliseconds msecs) const`

**API 类别：** 成员函数说明

**中文解读：** 这是向 `QDateTime` 添加依赖、数据或子对象的 API `addDuration`。注意对象所有权、重复添加和添加后的通知；如果对应有 remove/take 接口，要明确谁负责移除后的生命周期。

**签名拆解：**

- 返回值：`QDateTime`。
- 参数 `msecs`：类型为 `std::chrono::milliseconds`。没有默认值，调用时必须提供。传入 `std::chrono::milliseconds` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QDateTime QDateTime::addMSecs(qint64 msecs) const`

**API 类别：** 成员函数说明

**中文解读：** 这是向 `QDateTime` 添加依赖、数据或子对象的 API `addMSecs`。注意对象所有权、重复添加和添加后的通知；如果对应有 remove/take 接口，要明确谁负责移除后的生命周期。

**签名拆解：**

- 返回值：`QDateTime`。
- 参数 `msecs`：类型为 `qint64`。没有默认值，调用时必须提供。传入 `qint64` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QDateTime QDateTime::addMonths(int nmonths) const`

**API 类别：** 成员函数说明

**中文解读：** 这是向 `QDateTime` 添加依赖、数据或子对象的 API `addMonths`。注意对象所有权、重复添加和添加后的通知；如果对应有 remove/take 接口，要明确谁负责移除后的生命周期。

**签名拆解：**

- 返回值：`QDateTime`。
- 参数 `nmonths`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QDateTime QDateTime::addSecs(qint64 s) const`

**API 类别：** 成员函数说明

**中文解读：** 这是向 `QDateTime` 添加依赖、数据或子对象的 API `addSecs`。注意对象所有权、重复添加和添加后的通知；如果对应有 remove/take 接口，要明确谁负责移除后的生命周期。

**签名拆解：**

- 返回值：`QDateTime`。
- 参数 `s`：类型为 `qint64`。没有默认值，调用时必须提供。传入 `qint64` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QDateTime QDateTime::addYears(int nyears) const`

**API 类别：** 成员函数说明

**中文解读：** 这是向 `QDateTime` 添加依赖、数据或子对象的 API `addYears`。注意对象所有权、重复添加和添加后的通知；如果对应有 remove/take 接口，要明确谁负责移除后的生命周期。

**签名拆解：**

- 返回值：`QDateTime`。
- 参数 `nyears`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static, since 6.5] QDateTime QDateTime::currentDateTime(const QTimeZone &zone)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `currentDateTime`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QDateTime`。
- 参数 `zone`：类型为 `const QTimeZone &`。没有默认值，调用时必须提供。传入 `const QTimeZone &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] QDateTime QDateTime::currentDateTime()`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `currentDateTime`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QDateTime`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] QDateTime QDateTime::currentDateTimeUtc()`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `currentDateTimeUtc`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QDateTime`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static noexcept] qint64 QDateTime::currentMSecsSinceEpoch()`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `currentMSecsSinceEpoch`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`qint64`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static noexcept] qint64 QDateTime::currentSecsSinceEpoch()`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `currentSecsSinceEpoch`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`qint64`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QDate QDateTime::date() const`

**API 类别：** 成员函数说明

**中文解读：** `QDateTime::date` 用于计算、查询或取得与“日期”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QDate`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QDate`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `qint64 QDateTime::daysTo(const QDateTime &other) const`

**API 类别：** 成员函数说明

**中文解读：** `QDateTime::daysTo` 用于计算、查询或取得与“天数、转换输出”相关的操作。调用时要先确认当前状态和 `other` 的有效范围；返回类型是 `qint64`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`qint64`。
- 参数 `other`：类型为 `const QDateTime &`。没有默认值，调用时必须提供。参与比较、合并或交换的另一个对象；要确认它与当前对象属于同一类型或兼容协议。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] QDateTime QDateTime::fromCFDate(CFDateRef date)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `fromCFDate`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QDateTime`。
- 参数 `date`：类型为 `CFDateRef`。没有默认值，调用时必须提供。传入 `CFDateRef` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] QDateTime QDateTime::fromMSecsSinceEpoch(qint64 msecs, const QTimeZone &timeZone)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `fromMSecsSinceEpoch`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QDateTime`。
- 参数 `msecs`：类型为 `qint64`。没有默认值，调用时必须提供。传入 `qint64` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `timeZone`：类型为 `const QTimeZone &`。没有默认值，调用时必须提供。传入 `const QTimeZone &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] QDateTime QDateTime::fromMSecsSinceEpoch(qint64 msecs)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `fromMSecsSinceEpoch`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QDateTime`。
- 参数 `msecs`：类型为 `qint64`。没有默认值，调用时必须提供。传入 `qint64` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] QDateTime QDateTime::fromNSDate(const NSDate *date)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `fromNSDate`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QDateTime`。
- 参数 `date`：类型为 `const NSDate *`。没有默认值，调用时必须提供。传入 `const NSDate *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] QDateTime QDateTime::fromSecsSinceEpoch(qint64 secs, const QTimeZone &timeZone)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `fromSecsSinceEpoch`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QDateTime`。
- 参数 `secs`：类型为 `qint64`。没有默认值，调用时必须提供。传入 `qint64` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `timeZone`：类型为 `const QTimeZone &`。没有默认值，调用时必须提供。传入 `const QTimeZone &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] QDateTime QDateTime::fromSecsSinceEpoch(qint64 secs)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `fromSecsSinceEpoch`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QDateTime`。
- 参数 `secs`：类型为 `qint64`。没有默认值，调用时必须提供。传入 `qint64` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static, since 6.4] QDateTime QDateTime::fromStdLocalTime(const std::chrono::local_time<std::chrono::milliseconds> &time)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `fromStdLocalTime`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QDateTime`。
- 参数 `time`：类型为 `const std::chrono::local_time<std::chrono::milliseconds> &`。没有默认值，调用时必须提供。传入 `const std::chrono::local_time<std::chrono::milliseconds> &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static, since 6.4] template <typename Clock, typename Duration> QDateTime QDateTime::fromStdTimePoint(const std::chrono::time_point<Clock, Duration> &time)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `fromStdTimePoint`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`template <typename Clock, typename Duration> QDateTime`。
- 参数 `time`：类型为 `const std::chrono::time_point<Clock, Duration> &`。没有默认值，调用时必须提供。传入 `const std::chrono::time_point<Clock, Duration> &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static, since 6.4] QDateTime QDateTime::fromStdTimePoint(const std::chrono::local_time<std::chrono::milliseconds> &time)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `fromStdTimePoint`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QDateTime`。
- 参数 `time`：类型为 `const std::chrono::local_time<std::chrono::milliseconds> &`。没有默认值，调用时必须提供。传入 `const std::chrono::local_time<std::chrono::milliseconds> &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static, since 6.4] QDateTime QDateTime::fromStdTimePoint(std::chrono::time_point<std::chrono::system_clock, std::chrono::milliseconds> time)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `fromStdTimePoint`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QDateTime`。
- 参数 `time`：类型为 `std::chrono::time_point<std::chrono::system_clock, std::chrono::milliseconds>`。没有默认值，调用时必须提供。传入 `std::chrono::time_point<std::chrono::system_clock, std::chrono::milliseconds>` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static, since 6.4] QDateTime QDateTime::fromStdZonedTime(const int &time)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `fromStdZonedTime`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QDateTime`。
- 参数 `time`：类型为 `const int &`。没有默认值，调用时必须提供。传入 `const int &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] QDateTime QDateTime::fromString(const QString &string, const QString &format, int baseYear, QCalendar cal)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `fromString`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QDateTime`。
- 参数 `string`：类型为 `const QString &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。
- 参数 `format`：类型为 `const QString &`。没有默认值，调用时必须提供。数据格式或显示格式。格式通常会影响解析、像素布局、精度、编码或兼容性。
- 参数 `baseYear`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `cal`：类型为 `QCalendar`。没有默认值，调用时必须提供。传入 `QCalendar` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static, since 6.0] QDateTime QDateTime::fromString(QStringView string, Qt::DateFormat format = Qt::TextDate)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `fromString`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QDateTime`。
- 参数 `string`：类型为 `QStringView`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。
- 参数 `format`：类型为 `Qt::DateFormat`。默认值为 `Qt::TextDate`。数据格式或显示格式。格式通常会影响解析、像素布局、精度、编码或兼容性。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] QDateTime QDateTime::fromString(const QString &string, Qt::DateFormat format = Qt::TextDate)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `fromString`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QDateTime`。
- 参数 `string`：类型为 `const QString &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。
- 参数 `format`：类型为 `Qt::DateFormat`。默认值为 `Qt::TextDate`。数据格式或显示格式。格式通常会影响解析、像素布局、精度、编码或兼容性。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static, since 6.0] QDateTime QDateTime::fromString(QStringView string, QStringView format, QCalendar cal)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `fromString`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QDateTime`。
- 参数 `string`：类型为 `QStringView`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。
- 参数 `format`：类型为 `QStringView`。没有默认值，调用时必须提供。数据格式或显示格式。格式通常会影响解析、像素布局、精度、编码或兼容性。
- 参数 `cal`：类型为 `QCalendar`。没有默认值，调用时必须提供。传入 `QCalendar` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static, since 6.7] QDateTime QDateTime::fromString(QStringView string, QStringView format, int baseYear = QLocale::DefaultTwoDigitBaseYear)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `fromString`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QDateTime`。
- 参数 `string`：类型为 `QStringView`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。
- 参数 `format`：类型为 `QStringView`。没有默认值，调用时必须提供。数据格式或显示格式。格式通常会影响解析、像素布局、精度、编码或兼容性。
- 参数 `baseYear`：类型为 `int`。默认值为 `QLocale::DefaultTwoDigitBaseYear`。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static, since 6.0] QDateTime QDateTime::fromString(const QString &string, QStringView format, QCalendar cal)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `fromString`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QDateTime`。
- 参数 `string`：类型为 `const QString &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。
- 参数 `format`：类型为 `QStringView`。没有默认值，调用时必须提供。数据格式或显示格式。格式通常会影响解析、像素布局、精度、编码或兼容性。
- 参数 `cal`：类型为 `QCalendar`。没有默认值，调用时必须提供。传入 `QCalendar` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static, since 6.7] QDateTime QDateTime::fromString(const QString &string, QStringView format, int baseYear = QLocale::DefaultTwoDigitBaseYear)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `fromString`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QDateTime`。
- 参数 `string`：类型为 `const QString &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。
- 参数 `format`：类型为 `QStringView`。没有默认值，调用时必须提供。数据格式或显示格式。格式通常会影响解析、像素布局、精度、编码或兼容性。
- 参数 `baseYear`：类型为 `int`。默认值为 `QLocale::DefaultTwoDigitBaseYear`。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] QDateTime QDateTime::fromString(const QString &string, const QString &format, QCalendar cal)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `fromString`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QDateTime`。
- 参数 `string`：类型为 `const QString &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。
- 参数 `format`：类型为 `const QString &`。没有默认值，调用时必须提供。数据格式或显示格式。格式通常会影响解析、像素布局、精度、编码或兼容性。
- 参数 `cal`：类型为 `QCalendar`。没有默认值，调用时必须提供。传入 `QCalendar` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static, since 6.7] QDateTime QDateTime::fromString(const QString &string, const QString &format, int baseYear = QLocale::DefaultTwoDigitBaseYear)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `fromString`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QDateTime`。
- 参数 `string`：类型为 `const QString &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。
- 参数 `format`：类型为 `const QString &`。没有默认值，调用时必须提供。数据格式或显示格式。格式通常会影响解析、像素布局、精度、编码或兼容性。
- 参数 `baseYear`：类型为 `int`。默认值为 `QLocale::DefaultTwoDigitBaseYear`。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static, since 6.7] QDateTime QDateTime::fromString(QStringView string, QStringView format, int baseYear, QCalendar cal)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `fromString`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QDateTime`。
- 参数 `string`：类型为 `QStringView`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。
- 参数 `format`：类型为 `QStringView`。没有默认值，调用时必须提供。数据格式或显示格式。格式通常会影响解析、像素布局、精度、编码或兼容性。
- 参数 `baseYear`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `cal`：类型为 `QCalendar`。没有默认值，调用时必须提供。传入 `QCalendar` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static, since 6.0] QDateTime QDateTime::fromString(const QString &string, QStringView format, int baseYear, QCalendar cal)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `fromString`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QDateTime`。
- 参数 `string`：类型为 `const QString &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。
- 参数 `format`：类型为 `QStringView`。没有默认值，调用时必须提供。数据格式或显示格式。格式通常会影响解析、像素布局、精度、编码或兼容性。
- 参数 `baseYear`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `cal`：类型为 `QCalendar`。没有默认值，调用时必须提供。传入 `QCalendar` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QDateTime::isDaylightTime() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `isDaylightTime`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QDateTime::isNull() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `isNull`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QDateTime::isValid() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `isValid`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `qint64 QDateTime::msecsTo(const QDateTime &other) const`

**API 类别：** 成员函数说明

**中文解读：** `QDateTime::msecsTo` 用于计算、查询或取得与“毫秒数、转换输出”相关的操作。调用时要先确认当前状态和 `other` 的有效范围；返回类型是 `qint64`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`qint64`。
- 参数 `other`：类型为 `const QDateTime &`。没有默认值，调用时必须提供。参与比较、合并或交换的另一个对象；要确认它与当前对象属于同一类型或兼容协议。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `int QDateTime::offsetFromUtc() const`

**API 类别：** 成员函数说明

**中文解读：** `QDateTime::offsetFromUtc` 用于计算、查询或取得与“offset、转换进入、Utc”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `int`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`int`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `qint64 QDateTime::secsTo(const QDateTime &other) const`

**API 类别：** 成员函数说明

**中文解读：** `QDateTime::secsTo` 用于计算、查询或取得与“secs、转换输出”相关的操作。调用时要先确认当前状态和 `other` 的有效范围；返回类型是 `qint64`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`qint64`。
- 参数 `other`：类型为 `const QDateTime &`。没有默认值，调用时必须提供。参与比较、合并或交换的另一个对象；要确认它与当前对象属于同一类型或兼容协议。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QDateTime::setDate(QDate date, QDateTime::TransitionResolution resolve = TransitionResolution::LegacyBehavior)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setDate`。调用它会改变 `QDateTime` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `date`：类型为 `QDate`。没有默认值，调用时必须提供。传入 `QDate` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `resolve`：类型为 `QDateTime::TransitionResolution`。默认值为 `TransitionResolution::LegacyBehavior`。传入 `QDateTime::TransitionResolution` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QDateTime::setMSecsSinceEpoch(qint64 msecs)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setMSecsSinceEpoch`。调用它会改变 `QDateTime` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `msecs`：类型为 `qint64`。没有默认值，调用时必须提供。传入 `qint64` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QDateTime::setSecsSinceEpoch(qint64 secs)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setSecsSinceEpoch`。调用它会改变 `QDateTime` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `secs`：类型为 `qint64`。没有默认值，调用时必须提供。传入 `qint64` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QDateTime::setTime(QTime time, QDateTime::TransitionResolution resolve = TransitionResolution::LegacyBehavior)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setTime`。调用它会改变 `QDateTime` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `time`：类型为 `QTime`。没有默认值，调用时必须提供。传入 `QTime` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `resolve`：类型为 `QDateTime::TransitionResolution`。默认值为 `TransitionResolution::LegacyBehavior`。传入 `QDateTime::TransitionResolution` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QDateTime::setTimeZone(const QTimeZone &toZone, QDateTime::TransitionResolution resolve = TransitionResolution::LegacyBehavior)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setTimeZone`。调用它会改变 `QDateTime` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `toZone`：类型为 `const QTimeZone &`。没有默认值，调用时必须提供。传入 `const QTimeZone &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `resolve`：类型为 `QDateTime::TransitionResolution`。默认值为 `TransitionResolution::LegacyBehavior`。传入 `QDateTime::TransitionResolution` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] void QDateTime::swap(QDateTime &other)`

**API 类别：** 成员函数说明

**中文解读：** `QDateTime::swap` 用于执行与“swap”相关的操作。调用时要先确认当前状态和 `other` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `other`：类型为 `QDateTime &`。没有默认值，调用时必须提供。参与比较、合并或交换的另一个对象；要确认它与当前对象属于同一类型或兼容协议。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QTime QDateTime::time() const`

**API 类别：** 成员函数说明

**中文解读：** `QDateTime::time` 用于计算、查询或取得与“时间”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QTime`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QTime`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.5] QTimeZone QDateTime::timeRepresentation() const`

**API 类别：** 成员函数说明

**中文解读：** `QDateTime::timeRepresentation` 用于计算、查询或取得与“时间、Representation”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QTimeZone`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QTimeZone`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `Qt::TimeSpec QDateTime::timeSpec() const`

**API 类别：** 成员函数说明

**中文解读：** `QDateTime::timeSpec` 用于计算、查询或取得与“时间、Spec”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `Qt::TimeSpec`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`Qt::TimeSpec`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QTimeZone QDateTime::timeZone() const`

**API 类别：** 成员函数说明

**中文解读：** `QDateTime::timeZone` 用于计算、查询或取得与“时间、Zone”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QTimeZone`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QTimeZone`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString QDateTime::timeZoneAbbreviation() const`

**API 类别：** 成员函数说明

**中文解读：** `QDateTime::timeZoneAbbreviation` 用于计算、查询或取得与“时间、Zone、Abbreviation”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QString`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QString`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `CFDateRef QDateTime::toCFDate() const`

**API 类别：** 成员函数说明

**中文解读：** 这是转换/映射 API `toCFDate`。它通常在不同表示、坐标系、编码或 Qt 类型之间建立边界；转换前确认格式和所有权，转换后检查是否丢失精度、编码或上下文。

**签名拆解：**

- 返回值：`CFDateRef`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QDateTime QDateTime::toLocalTime() const`

**API 类别：** 成员函数说明

**中文解读：** 这是转换/映射 API `toLocalTime`。它通常在不同表示、坐标系、编码或 Qt 类型之间建立边界；转换前确认格式和所有权，转换后检查是否丢失精度、编码或上下文。

**签名拆解：**

- 返回值：`QDateTime`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `qint64 QDateTime::toMSecsSinceEpoch() const`

**API 类别：** 成员函数说明

**中文解读：** 这是转换/映射 API `toMSecsSinceEpoch`。它通常在不同表示、坐标系、编码或 Qt 类型之间建立边界；转换前确认格式和所有权，转换后检查是否丢失精度、编码或上下文。

**签名拆解：**

- 返回值：`qint64`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `NSDate *QDateTime::toNSDate() const`

**API 类别：** 成员函数说明

**中文解读：** 这是转换/映射 API `toNSDate`。它通常在不同表示、坐标系、编码或 Qt 类型之间建立边界；转换前确认格式和所有权，转换后检查是否丢失精度、编码或上下文。

**签名拆解：**

- 返回值：`NSDate *`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QDateTime QDateTime::toOffsetFromUtc(int offsetSeconds) const`

**API 类别：** 成员函数说明

**中文解读：** 这是转换/映射 API `toOffsetFromUtc`。它通常在不同表示、坐标系、编码或 Qt 类型之间建立边界；转换前确认格式和所有权，转换后检查是否丢失精度、编码或上下文。

**签名拆解：**

- 返回值：`QDateTime`。
- 参数 `offsetSeconds`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `qint64 QDateTime::toSecsSinceEpoch() const`

**API 类别：** 成员函数说明

**中文解读：** 这是转换/映射 API `toSecsSinceEpoch`。它通常在不同表示、坐标系、编码或 Qt 类型之间建立边界；转换前确认格式和所有权，转换后检查是否丢失精度、编码或上下文。

**签名拆解：**

- 返回值：`qint64`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.4] std::chrono::sys_time<std::chrono::milliseconds> QDateTime::toStdSysMilliseconds() const`

**API 类别：** 成员函数说明

**中文解读：** 这是转换/映射 API `toStdSysMilliseconds`。它通常在不同表示、坐标系、编码或 Qt 类型之间建立边界；转换前确认格式和所有权，转换后检查是否丢失精度、编码或上下文。

**签名拆解：**

- 返回值：`std::chrono::sys_time<std::chrono::milliseconds>`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.4] std::chrono::sys_seconds QDateTime::toStdSysSeconds() const`

**API 类别：** 成员函数说明

**中文解读：** 这是转换/映射 API `toStdSysSeconds`。它通常在不同表示、坐标系、编码或 Qt 类型之间建立边界；转换前确认格式和所有权，转换后检查是否丢失精度、编码或上下文。

**签名拆解：**

- 返回值：`std::chrono::sys_seconds`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString QDateTime::toString(QStringView format, QCalendar cal) const`

**API 类别：** 成员函数说明

**中文解读：** 这是转换/映射 API `toString`。它通常在不同表示、坐标系、编码或 Qt 类型之间建立边界；转换前确认格式和所有权，转换后检查是否丢失精度、编码或上下文。

**签名拆解：**

- 返回值：`QString`。
- 参数 `format`：类型为 `QStringView`。没有默认值，调用时必须提供。数据格式或显示格式。格式通常会影响解析、像素布局、精度、编码或兼容性。
- 参数 `cal`：类型为 `QCalendar`。没有默认值，调用时必须提供。传入 `QCalendar` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString QDateTime::toString(QStringView format) const`

**API 类别：** 成员函数说明

**中文解读：** 这是转换/映射 API `toString`。它通常在不同表示、坐标系、编码或 Qt 类型之间建立边界；转换前确认格式和所有权，转换后检查是否丢失精度、编码或上下文。

**签名拆解：**

- 返回值：`QString`。
- 参数 `format`：类型为 `QStringView`。没有默认值，调用时必须提供。数据格式或显示格式。格式通常会影响解析、像素布局、精度、编码或兼容性。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString QDateTime::toString(Qt::DateFormat format = Qt::TextDate) const`

**API 类别：** 成员函数说明

**中文解读：** 这是转换/映射 API `toString`。它通常在不同表示、坐标系、编码或 Qt 类型之间建立边界；转换前确认格式和所有权，转换后检查是否丢失精度、编码或上下文。

**签名拆解：**

- 返回值：`QString`。
- 参数 `format`：类型为 `Qt::DateFormat`。默认值为 `Qt::TextDate`。数据格式或显示格式。格式通常会影响解析、像素布局、精度、编码或兼容性。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString QDateTime::toString(const QString &format) const`

**API 类别：** 成员函数说明

**中文解读：** 这是转换/映射 API `toString`。它通常在不同表示、坐标系、编码或 Qt 类型之间建立边界；转换前确认格式和所有权，转换后检查是否丢失精度、编码或上下文。

**签名拆解：**

- 返回值：`QString`。
- 参数 `format`：类型为 `const QString &`。没有默认值，调用时必须提供。数据格式或显示格式。格式通常会影响解析、像素布局、精度、编码或兼容性。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QDateTime QDateTime::toTimeZone(const QTimeZone &timeZone) const`

**API 类别：** 成员函数说明

**中文解读：** 这是转换/映射 API `toTimeZone`。它通常在不同表示、坐标系、编码或 Qt 类型之间建立边界；转换前确认格式和所有权，转换后检查是否丢失精度、编码或上下文。

**签名拆解：**

- 返回值：`QDateTime`。
- 参数 `timeZone`：类型为 `const QTimeZone &`。没有默认值，调用时必须提供。传入 `const QTimeZone &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QDateTime QDateTime::toUTC() const`

**API 类别：** 成员函数说明

**中文解读：** 这是转换/映射 API `toUTC`。它通常在不同表示、坐标系、编码或 Qt 类型之间建立边界；转换前确认格式和所有权，转换后检查是否丢失精度、编码或上下文。

**签名拆解：**

- 返回值：`QDateTime`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.4] QDateTime &QDateTime::operator+=(std::chrono::milliseconds duration)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QDateTime` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QDateTime &`。
- 参数 `duration`：类型为 `std::chrono::milliseconds`。没有默认值，调用时必须提供。持续时间，通常以毫秒表示；要确认 0、负数、循环和平台精度。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.4] QDateTime &QDateTime::operator-=(std::chrono::milliseconds duration)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QDateTime` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QDateTime &`。
- 参数 `duration`：类型为 `std::chrono::milliseconds`。没有默认值，调用时必须提供。持续时间，通常以毫秒表示；要确认 0、负数、循环和平台精度。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] QDateTime &QDateTime::operator=(const QDateTime &other)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QDateTime` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QDateTime &`。
- 参数 `other`：类型为 `const QDateTime &`。没有默认值，调用时必须提供。参与比较、合并或交换的另一个对象；要确认它与当前对象属于同一类型或兼容协议。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] bool operator!=(const QDateTime &lhs, const QDateTime &rhs)`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QDateTime` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`bool`。
- 参数 `lhs`：类型为 `const QDateTime &`。没有默认值，调用时必须提供。运算符左侧的值；要注意返回新值还是修改当前对象。
- 参数 `rhs`：类型为 `const QDateTime &`。没有默认值，调用时必须提供。运算符右侧的另一个值；通常不会被当前 API 接管所有权。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.4] QDateTime operator+(std::chrono::milliseconds duration, const QDateTime &dateTime)`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QDateTime` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QDateTime`。
- 参数 `duration`：类型为 `std::chrono::milliseconds`。没有默认值，调用时必须提供。持续时间，通常以毫秒表示；要确认 0、负数、循环和平台精度。
- 参数 `dateTime`：类型为 `const QDateTime &`。没有默认值，调用时必须提供。传入 `const QDateTime &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.4] std::chrono::milliseconds operator-(const QDateTime &lhs, const QDateTime &rhs)`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QDateTime` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`std::chrono::milliseconds`。
- 参数 `lhs`：类型为 `const QDateTime &`。没有默认值，调用时必须提供。运算符左侧的值；要注意返回新值还是修改当前对象。
- 参数 `rhs`：类型为 `const QDateTime &`。没有默认值，调用时必须提供。运算符右侧的另一个值；通常不会被当前 API 接管所有权。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.4] QDateTime operator-(const QDateTime &dateTime, std::chrono::milliseconds duration)`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QDateTime` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QDateTime`。
- 参数 `dateTime`：类型为 `const QDateTime &`。没有默认值，调用时必须提供。传入 `const QDateTime &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `duration`：类型为 `std::chrono::milliseconds`。没有默认值，调用时必须提供。持续时间，通常以毫秒表示；要确认 0、负数、循环和平台精度。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] bool operator<(const QDateTime &lhs, const QDateTime &rhs)`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QDateTime` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`bool`。
- 参数 `lhs`：类型为 `const QDateTime &`。没有默认值，调用时必须提供。运算符左侧的值；要注意返回新值还是修改当前对象。
- 参数 `rhs`：类型为 `const QDateTime &`。没有默认值，调用时必须提供。运算符右侧的另一个值；通常不会被当前 API 接管所有权。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QDataStream &operator<<(QDataStream &out, const QDateTime &dateTime)`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QDateTime` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QDataStream &`。
- 参数 `out`：类型为 `QDataStream &`。没有默认值，调用时必须提供。传入 `QDataStream &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `dateTime`：类型为 `const QDateTime &`。没有默认值，调用时必须提供。传入 `const QDateTime &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] bool operator<=(const QDateTime &lhs, const QDateTime &rhs)`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QDateTime` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`bool`。
- 参数 `lhs`：类型为 `const QDateTime &`。没有默认值，调用时必须提供。运算符左侧的值；要注意返回新值还是修改当前对象。
- 参数 `rhs`：类型为 `const QDateTime &`。没有默认值，调用时必须提供。运算符右侧的另一个值；通常不会被当前 API 接管所有权。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] bool operator==(const QDateTime &lhs, const QDateTime &rhs)`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QDateTime` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`bool`。
- 参数 `lhs`：类型为 `const QDateTime &`。没有默认值，调用时必须提供。运算符左侧的值；要注意返回新值还是修改当前对象。
- 参数 `rhs`：类型为 `const QDateTime &`。没有默认值，调用时必须提供。运算符右侧的另一个值；通常不会被当前 API 接管所有权。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] bool operator>(const QDateTime &lhs, const QDateTime &rhs)`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QDateTime` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`bool`。
- 参数 `lhs`：类型为 `const QDateTime &`。没有默认值，调用时必须提供。运算符左侧的值；要注意返回新值还是修改当前对象。
- 参数 `rhs`：类型为 `const QDateTime &`。没有默认值，调用时必须提供。运算符右侧的另一个值；通常不会被当前 API 接管所有权。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] bool operator>=(const QDateTime &lhs, const QDateTime &rhs)`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QDateTime` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`bool`。
- 参数 `lhs`：类型为 `const QDateTime &`。没有默认值，调用时必须提供。运算符左侧的值；要注意返回新值还是修改当前对象。
- 参数 `rhs`：类型为 `const QDateTime &`。没有默认值，调用时必须提供。运算符右侧的另一个值；通常不会被当前 API 接管所有权。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QDataStream &operator>>(QDataStream &in, QDateTime &dateTime)`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QDateTime` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QDataStream &`。
- 参数 `in`：类型为 `QDataStream &`。没有默认值，调用时必须提供。传入 `QDataStream &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `dateTime`：类型为 `QDateTime &`。没有默认值，调用时必须提供。传入 `QDateTime &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString toString(const QString &format, QCalendar cal) const`

**API 类别：** 公有函数

**中文解读：** 这是转换/映射 API `toString`。它通常在不同表示、坐标系、编码或 Qt 类型之间建立边界；转换前确认格式和所有权，转换后检查是否丢失精度、编码或上下文。

**签名拆解：**

- 返回值：`QString`。
- 参数 `format`：类型为 `const QString &`。没有默认值，调用时必须提供。数据格式或显示格式。格式通常会影响解析、像素布局、精度、编码或兼容性。
- 参数 `cal`：类型为 `QCalendar`。没有默认值，调用时必须提供。传入 `QCalendar` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `(since 6.4) QDateTime operator+(const QDateTime &dateTime, std::chrono::milliseconds duration)`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QDateTime` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QDateTime`。
- 参数 `dateTime`：类型为 `const QDateTime &`。没有默认值，调用时必须提供。传入 `const QDateTime &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `duration`：类型为 `std::chrono::milliseconds`。没有默认值，调用时必须提供。持续时间，通常以毫秒表示；要确认 0、负数、循环和平台精度。

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

`QDateTime` 所属机制类型：Qt 值类型与隐式共享机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
