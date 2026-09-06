# QMediaTimeRange

> Qt 6.11.1 · Qt Multimedia

## 1. 先建立直觉

**一句话定位：** `QMediaTimeRange` 是 Qt Multimedia 的“媒体TimeRange”类型，参与媒体源、设备、格式、播放/采集状态或音视频数据处理。

**模块背景：** Qt Multimedia 提供音频、视频、摄像头、媒体会话和设备访问能力。

### 这是什么

`QMediaTimeRange` 是 多媒体设备与会话机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 多媒体类型通常把设备、媒体会话、格式、播放状态和异步错误分开。硬件能力、平台后端、权限和资源状态会影响结果；请求成功发起不等于设备已准备好。

**适用场景：** 先检查平台能力和权限，再创建会话/设备，设置格式和源，连接状态与错误信号，执行开始/暂停/停止并在结束后清理。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要假设所有平台支持相同编解码器和格式；不要忽略权限和后端错误；不要在状态未准备好时连续调用控制 API；媒体对象销毁前先停止使用。

## 2. 依赖与对象关系

- 头文件：`#include <QMediaTimeRange>`
- 继承自：未在类页中列出
- 直接派生类：未在类页中列出

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Multimedia)
target_link_libraries(mytarget PRIVATE Qt6::Multimedia)
```

**继承带来的规则：** 它是值类型或不直接使用 QObject 对象模型，重点放在数据语义、拷贝/移动成本和参数有效性。

### 工作机制

多媒体类型通常把设备、媒体会话、格式、播放状态和异步错误分开。硬件能力、平台后端、权限和资源状态会影响结果；请求成功发起不等于设备已准备好。

### 状态、生命周期和线程

**生命周期：** 设备或媒体对象要在使用期间保持有效，开始前配置输入/输出和格式，停止后释放会话或解除设备占用。状态、媒体状态和错误信号共同决定下一步操作。

**状态与结果：** 区分无媒体、加载中、已加载、播放中、暂停、停止、结束和错误。进度、时长、缓冲和设备可用性不是同一个状态，不能只用一个 bool 表示。

**线程与事件循环：** 媒体对象通常依赖事件循环和平台线程边界；GUI 展示对象在 GUI 线程，后台处理要使用类明确支持的线程模型。

## 3. 直接使用

先检查平台能力和权限，再创建会话/设备，设置格式和源，连接状态与错误信号，执行开始/暂停/停止并在结束后清理。 使用时通常按这个过程组织：准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 公有类型

- `struct Interval`

### 公有函数

- `QMediaTimeRange()`
- `QMediaTimeRange(const QMediaTimeRange::Interval &interval)`
- `QMediaTimeRange(qint64 start, qint64 end)`
- `QMediaTimeRange(const QMediaTimeRange &range)`
- `QMediaTimeRange(QMediaTimeRange &&other)`
- `~QMediaTimeRange()`
- `void addInterval(const QMediaTimeRange::Interval &interval)`
- `void addInterval(qint64 start, qint64 end)`
- `void addTimeRange(const QMediaTimeRange &range)`
- `void clear()`
- `bool contains(qint64 time) const`
- `qint64 earliestTime() const`
- `QList<QMediaTimeRange::Interval> intervals() const`
- `bool isContinuous() const`
- `bool isEmpty() const`
- `qint64 latestTime() const`
- `void removeInterval(const QMediaTimeRange::Interval &interval)`
- `void removeInterval(qint64 start, qint64 end)`
- `void removeTimeRange(const QMediaTimeRange &range)`
- `void swap(QMediaTimeRange &other)`
- `QMediaTimeRange & operator+=(const QMediaTimeRange &other)`
- `QMediaTimeRange & operator+=(const QMediaTimeRange::Interval &interval)`
- `QMediaTimeRange & operator-=(const QMediaTimeRange &other)`
- `QMediaTimeRange & operator-=(const QMediaTimeRange::Interval &interval)`
- `QMediaTimeRange & operator=(QMediaTimeRange &&other)`
- `QMediaTimeRange & operator=(const QMediaTimeRange &other)`
- `QMediaTimeRange & operator=(const QMediaTimeRange::Interval &interval)`

### 相关非成员函数

- `bool operator!=(const QMediaTimeRange &lhs, const QMediaTimeRange &rhs)`
- `QMediaTimeRange operator+(const QMediaTimeRange &r1, const QMediaTimeRange &r2)`
- `QMediaTimeRange operator-(const QMediaTimeRange &r1, const QMediaTimeRange &r2)`
- `bool operator==(const QMediaTimeRange &lhs, const QMediaTimeRange &rhs)`

## 5. API 逐个说明

这里直接说明每个公开成员解决什么问题、参数代表什么、返回什么、会改变什么以及使用时容易出现什么问题。每一个公开签名都会有对应的中文解释。

本类共整理 32 个公开成员条目；没有独立长描述的 API 也会根据签名、类型和所属机制给出使用说明。

### `QMediaTimeRange::QMediaTimeRange()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QMediaTimeRange` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QMediaTimeRange::QMediaTimeRange(const QMediaTimeRange::Interval &interval)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QMediaTimeRange` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `interval`：类型为 `const QMediaTimeRange::Interval &`。没有默认值，调用时必须提供。时间间隔，Qt 定时器通常使用毫秒；要检查 0、负数和超出范围时的语义。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[explicit] QMediaTimeRange::QMediaTimeRange(qint64 start, qint64 end)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QMediaTimeRange` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `start`：类型为 `qint64`。没有默认值，调用时必须提供。传入 `qint64` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `end`：类型为 `qint64`。没有默认值，调用时必须提供。传入 `qint64` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] QMediaTimeRange::QMediaTimeRange(const QMediaTimeRange &range)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QMediaTimeRange` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `range`：类型为 `const QMediaTimeRange &`。没有默认值，调用时必须提供。传入 `const QMediaTimeRange &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[constexpr noexcept] QMediaTimeRange::QMediaTimeRange(QMediaTimeRange &&other)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QMediaTimeRange` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `other`：类型为 `QMediaTimeRange &&`。没有默认值，调用时必须提供。参与比较、合并或交换的另一个对象；要确认它与当前对象属于同一类型或兼容协议。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] QMediaTimeRange::~QMediaTimeRange()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QMediaTimeRange` 的析构函数。对象销毁时资源、子对象和连接会按 Qt 规则释放；异步对象要先停止任务或使用 deleteLater，避免回调访问已经不存在的实例。

**签名拆解：**

- 返回值：析构函数，无返回值。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QMediaTimeRange::addInterval(const QMediaTimeRange::Interval &interval)`

**API 类别：** 成员函数说明

**中文解读：** 这是向 `QMediaTimeRange` 添加依赖、数据或子对象的 API `addInterval`。注意对象所有权、重复添加和添加后的通知；如果对应有 remove/take 接口，要明确谁负责移除后的生命周期。

**签名拆解：**

- 返回值：`void`。
- 参数 `interval`：类型为 `const QMediaTimeRange::Interval &`。没有默认值，调用时必须提供。时间间隔，Qt 定时器通常使用毫秒；要检查 0、负数和超出范围时的语义。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QMediaTimeRange::addInterval(qint64 start, qint64 end)`

**API 类别：** 成员函数说明

**中文解读：** 这是向 `QMediaTimeRange` 添加依赖、数据或子对象的 API `addInterval`。注意对象所有权、重复添加和添加后的通知；如果对应有 remove/take 接口，要明确谁负责移除后的生命周期。

**签名拆解：**

- 返回值：`void`。
- 参数 `start`：类型为 `qint64`。没有默认值，调用时必须提供。传入 `qint64` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `end`：类型为 `qint64`。没有默认值，调用时必须提供。传入 `qint64` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QMediaTimeRange::addTimeRange(const QMediaTimeRange &range)`

**API 类别：** 成员函数说明

**中文解读：** 这是向 `QMediaTimeRange` 添加依赖、数据或子对象的 API `addTimeRange`。注意对象所有权、重复添加和添加后的通知；如果对应有 remove/take 接口，要明确谁负责移除后的生命周期。

**签名拆解：**

- 返回值：`void`。
- 参数 `range`：类型为 `const QMediaTimeRange &`。没有默认值，调用时必须提供。传入 `const QMediaTimeRange &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QMediaTimeRange::clear()`

**API 类别：** 成员函数说明

**中文解读：** 这是状态清理或重置 API `clear`。调用后原有数据、索引、缓存或绑定可能失效；使用前先确认它影响的是当前对象、子对象还是底层共享资源，之后重新检查状态。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QMediaTimeRange::contains(qint64 time) const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `contains`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数 `time`：类型为 `qint64`。没有默认值，调用时必须提供。传入 `qint64` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `qint64 QMediaTimeRange::earliestTime() const`

**API 类别：** 成员函数说明

**中文解读：** `QMediaTimeRange::earliestTime` 用于计算、查询或取得与“earliest、时间”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `qint64`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`qint64`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QList<QMediaTimeRange::Interval> QMediaTimeRange::intervals() const`

**API 类别：** 成员函数说明

**中文解读：** `QMediaTimeRange::intervals` 用于计算、查询或取得与“intervals”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QList<QMediaTimeRange::Interval>`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QList<QMediaTimeRange::Interval>`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QMediaTimeRange::isContinuous() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `isContinuous`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QMediaTimeRange::isEmpty() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `isEmpty`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `qint64 QMediaTimeRange::latestTime() const`

**API 类别：** 成员函数说明

**中文解读：** `QMediaTimeRange::latestTime` 用于计算、查询或取得与“latest、时间”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `qint64`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`qint64`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QMediaTimeRange::removeInterval(const QMediaTimeRange::Interval &interval)`

**API 类别：** 成员函数说明

**中文解读：** 这是结束/释放/取消 API `removeInterval`。它会改变对象状态或资源所有权，调用后不要继续使用已经失效的句柄、reply、索引或设备，并确认异步完成信号是否仍会到达。

**签名拆解：**

- 返回值：`void`。
- 参数 `interval`：类型为 `const QMediaTimeRange::Interval &`。没有默认值，调用时必须提供。时间间隔，Qt 定时器通常使用毫秒；要检查 0、负数和超出范围时的语义。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QMediaTimeRange::removeInterval(qint64 start, qint64 end)`

**API 类别：** 成员函数说明

**中文解读：** 这是结束/释放/取消 API `removeInterval`。它会改变对象状态或资源所有权，调用后不要继续使用已经失效的句柄、reply、索引或设备，并确认异步完成信号是否仍会到达。

**签名拆解：**

- 返回值：`void`。
- 参数 `start`：类型为 `qint64`。没有默认值，调用时必须提供。传入 `qint64` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `end`：类型为 `qint64`。没有默认值，调用时必须提供。传入 `qint64` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QMediaTimeRange::removeTimeRange(const QMediaTimeRange &range)`

**API 类别：** 成员函数说明

**中文解读：** 这是结束/释放/取消 API `removeTimeRange`。它会改变对象状态或资源所有权，调用后不要继续使用已经失效的句柄、reply、索引或设备，并确认异步完成信号是否仍会到达。

**签名拆解：**

- 返回值：`void`。
- 参数 `range`：类型为 `const QMediaTimeRange &`。没有默认值，调用时必须提供。传入 `const QMediaTimeRange &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] void QMediaTimeRange::swap(QMediaTimeRange &other)`

**API 类别：** 成员函数说明

**中文解读：** `QMediaTimeRange::swap` 用于执行与“swap”相关的操作。调用时要先确认当前状态和 `other` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `other`：类型为 `QMediaTimeRange &`。没有默认值，调用时必须提供。参与比较、合并或交换的另一个对象；要确认它与当前对象属于同一类型或兼容协议。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QMediaTimeRange &QMediaTimeRange::operator+=(const QMediaTimeRange &other)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QMediaTimeRange` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QMediaTimeRange &`。
- 参数 `other`：类型为 `const QMediaTimeRange &`。没有默认值，调用时必须提供。参与比较、合并或交换的另一个对象；要确认它与当前对象属于同一类型或兼容协议。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QMediaTimeRange &QMediaTimeRange::operator+=(const QMediaTimeRange::Interval &interval)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QMediaTimeRange` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QMediaTimeRange &`。
- 参数 `interval`：类型为 `const QMediaTimeRange::Interval &`。没有默认值，调用时必须提供。时间间隔，Qt 定时器通常使用毫秒；要检查 0、负数和超出范围时的语义。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QMediaTimeRange &QMediaTimeRange::operator-=(const QMediaTimeRange &other)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QMediaTimeRange` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QMediaTimeRange &`。
- 参数 `other`：类型为 `const QMediaTimeRange &`。没有默认值，调用时必须提供。参与比较、合并或交换的另一个对象；要确认它与当前对象属于同一类型或兼容协议。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QMediaTimeRange &QMediaTimeRange::operator-=(const QMediaTimeRange::Interval &interval)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QMediaTimeRange` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QMediaTimeRange &`。
- 参数 `interval`：类型为 `const QMediaTimeRange::Interval &`。没有默认值，调用时必须提供。时间间隔，Qt 定时器通常使用毫秒；要检查 0、负数和超出范围时的语义。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] QMediaTimeRange &QMediaTimeRange::operator=(QMediaTimeRange &&other)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QMediaTimeRange` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QMediaTimeRange &`。
- 参数 `other`：类型为 `QMediaTimeRange &&`。没有默认值，调用时必须提供。参与比较、合并或交换的另一个对象；要确认它与当前对象属于同一类型或兼容协议。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] QMediaTimeRange &QMediaTimeRange::operator=(const QMediaTimeRange &other)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QMediaTimeRange` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QMediaTimeRange &`。
- 参数 `other`：类型为 `const QMediaTimeRange &`。没有默认值，调用时必须提供。参与比较、合并或交换的另一个对象；要确认它与当前对象属于同一类型或兼容协议。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QMediaTimeRange &QMediaTimeRange::operator=(const QMediaTimeRange::Interval &interval)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QMediaTimeRange` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QMediaTimeRange &`。
- 参数 `interval`：类型为 `const QMediaTimeRange::Interval &`。没有默认值，调用时必须提供。时间间隔，Qt 定时器通常使用毫秒；要检查 0、负数和超出范围时的语义。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool operator!=(const QMediaTimeRange &lhs, const QMediaTimeRange &rhs)`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QMediaTimeRange` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`bool`。
- 参数 `lhs`：类型为 `const QMediaTimeRange &`。没有默认值，调用时必须提供。运算符左侧的值；要注意返回新值还是修改当前对象。
- 参数 `rhs`：类型为 `const QMediaTimeRange &`。没有默认值，调用时必须提供。运算符右侧的另一个值；通常不会被当前 API 接管所有权。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QMediaTimeRange operator+(const QMediaTimeRange &r1, const QMediaTimeRange &r2)`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QMediaTimeRange` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QMediaTimeRange`。
- 参数 `r1`：类型为 `const QMediaTimeRange &`。没有默认值，调用时必须提供。传入 `const QMediaTimeRange &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `r2`：类型为 `const QMediaTimeRange &`。没有默认值，调用时必须提供。传入 `const QMediaTimeRange &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QMediaTimeRange operator-(const QMediaTimeRange &r1, const QMediaTimeRange &r2)`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QMediaTimeRange` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QMediaTimeRange`。
- 参数 `r1`：类型为 `const QMediaTimeRange &`。没有默认值，调用时必须提供。传入 `const QMediaTimeRange &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `r2`：类型为 `const QMediaTimeRange &`。没有默认值，调用时必须提供。传入 `const QMediaTimeRange &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool operator==(const QMediaTimeRange &lhs, const QMediaTimeRange &rhs)`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QMediaTimeRange` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`bool`。
- 参数 `lhs`：类型为 `const QMediaTimeRange &`。没有默认值，调用时必须提供。运算符左侧的值；要注意返回新值还是修改当前对象。
- 参数 `rhs`：类型为 `const QMediaTimeRange &`。没有默认值，调用时必须提供。运算符右侧的另一个值；通常不会被当前 API 接管所有权。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `struct Interval`

**API 类别：** 公有类型

**中文解读：** 这是 `QMediaTimeRange` 的 `间隔` 成员声明。它通常作为其他 API 的类型、常量或配置入口使用；先确认可用值和适用状态，再结合本类的创建、核心操作和清理流程使用。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

## 6. 深入实践与常见坑

### 生命周期和资源边界

设备或媒体对象要在使用期间保持有效，开始前配置输入/输出和格式，停止后释放会话或解除设备占用。状态、媒体状态和错误信号共同决定下一步操作。

### 状态和错误边界

区分无媒体、加载中、已加载、播放中、暂停、停止、结束和错误。进度、时长、缓冲和设备可用性不是同一个状态，不能只用一个 bool 表示。

### 线程边界

媒体对象通常依赖事件循环和平台线程边界；GUI 展示对象在 GUI 线程，后台处理要使用类明确支持的线程模型。

### 最容易出现的错误

不要假设所有平台支持相同编解码器和格式；不要忽略权限和后端错误；不要在状态未准备好时连续调用控制 API；媒体对象销毁前先停止使用。

### 版本和平台

本文档以 Qt 6.11.1 为依据。涉及平台后端、编解码器、数据库驱动、窗口风格、编译器特性或标注了版本号的 API 时，要把版本条件当作使用约束，而不是只看函数是否能补全。

## 7. 使用边界

`QMediaTimeRange` 所属机制类型：多媒体设备与会话机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
