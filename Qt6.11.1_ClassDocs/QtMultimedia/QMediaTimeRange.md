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

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `QMediaTimeRange::QMediaTimeRange()`

**作用与语义：**

构建一个空的时间范围。

### `QMediaTimeRange::QMediaTimeRange(const QMediaTimeRange::Interval &interval)`

**作用与语义：**

构造包含初始区间`interval`的时间范围。
如果`interval`不`normal`，所得时间范围将为空。

### `[explicit] QMediaTimeRange::QMediaTimeRange(qint64 start, qint64 end)`

**作用与语义：**

构建包含从`start`到`end`包含的初始区间的时间范围。
如果区间不`normal`，所得时间区间将为空。

### `[noexcept] QMediaTimeRange::QMediaTimeRange(const QMediaTimeRange &range)`

**作用与语义：**

通过复制另一个时间`range`构建时间范围。

### `[constexpr noexcept] QMediaTimeRange::QMediaTimeRange(QMediaTimeRange &&other)`

**作用与语义：**

通过从`other`开始构建时间范围。

### `[noexcept] QMediaTimeRange::~QMediaTimeRange()`

**作用与语义：**

毁灭者。

### `void QMediaTimeRange::addInterval(const QMediaTimeRange::Interval &interval)`

**作用与语义：**

将指定`interval`添加到时间范围内。
添加不`normal`的区间无效，将被忽略。
如果指定的区间与时间范围内的现有区间相邻或重叠，这些区间将合并。
该操作需要线性时间。

### `void QMediaTimeRange::addInterval(qint64 start, qint64 end)`

**作用与语义：**

将`start`和`end`指定的区间加到时间范围上。

### `void QMediaTimeRange::addTimeRange(const QMediaTimeRange &range)`

**作用与语义：**

将`range`中的每个音程加到该时间范围。
相当于对每个区间调用`addInterval()` `range`。

### `void QMediaTimeRange::clear()`

**作用与语义：**

移除时间范围内的所有音程。

### `bool QMediaTimeRange::contains(qint64 time) const`

**作用与语义：**

如果指定的`time`在时间范围内，则返回为真。

### `qint64 QMediaTimeRange::earliestTime() const`

**作用与语义：**

在时间范围内最早返回。
对于空时间区间，这个值等于零。

### `QList<QMediaTimeRange::Interval> QMediaTimeRange::intervals() const`

**作用与语义：**

返回该时间区间覆盖的区间列表。

### `bool QMediaTimeRange::isContinuous() const`

**作用与语义：**

如果时间区间包含连续区间，则返回为真。即在时间区间内存在一个或更少不相交的区间。

### `bool QMediaTimeRange::isEmpty() const`

**作用与语义：**

如果时间范围内没有区间，则返回为真。

### `qint64 QMediaTimeRange::latestTime() const`

**作用与语义：**

返回时间范围内的最晚时间。
对于空时间区间，这个值等于零。

### `void QMediaTimeRange::removeInterval(const QMediaTimeRange::Interval &interval)`

**作用与语义：**

将指定`interval`从时间范围内移除。
移除不`normal`的区间无效，将被忽略。
时间范围内的区间将被裁剪、拆分或删除，使得该区间内不包含目标区间的任何部分。
该操作需要线性时间。

### `void QMediaTimeRange::removeInterval(qint64 start, qint64 end)`

**作用与语义：**

将`start`和`end`指定的时间区间从时间范围内移除。

### `void QMediaTimeRange::removeTimeRange(const QMediaTimeRange &range)`

**作用与语义：**

从该时间范围内移除`range`中的每个音程。
相当于对每个区间调用`removeInterval()` `range`。

### `[noexcept] void QMediaTimeRange::swap(QMediaTimeRange &other)`

**作用与语义：**

将当前实例与`other`交换。

### `QMediaTimeRange &QMediaTimeRange::operator+=(const QMediaTimeRange &other)`

**作用与语义：**

将`other`中的每个区间相加到时间区间，并返回结果。

### `QMediaTimeRange &QMediaTimeRange::operator+=(const QMediaTimeRange::Interval &interval)`

**作用与语义：**

将指定`interval`加到时间范围，返回结果。

### `QMediaTimeRange &QMediaTimeRange::operator-=(const QMediaTimeRange &other)`

**作用与语义：**

从时间区间中移除`other`中的每个区间，返回结果。

### `QMediaTimeRange &QMediaTimeRange::operator-=(const QMediaTimeRange::Interval &interval)`

**作用与语义：**

从时间范围内移除指定`interval`并返回结果。

### `[noexcept] QMediaTimeRange &QMediaTimeRange::operator=(QMediaTimeRange &&other)`

**作用与语义：**

`other`进入这个时间范围。

### `[noexcept] QMediaTimeRange &QMediaTimeRange::operator=(const QMediaTimeRange &other)`

**作用与语义：**

会拿一份`other`时间范围的副本，然后自己返回。

### `QMediaTimeRange &QMediaTimeRange::operator=(const QMediaTimeRange::Interval &interval)`

**作用与语义：**

将时间范围设定为一个连续的区间，`interval`。

### `bool operator!=(const QMediaTimeRange &lhs, const QMediaTimeRange &rhs)`

**作用与语义：**

如果`lhs`中的一个或多个区间不存在于`rhs`，则返回为真。

### `QMediaTimeRange operator+(const QMediaTimeRange &r1, const QMediaTimeRange &r2)`

**作用与语义：**

返回包含`r1`与 `r2` 并集的时间范围。

### `QMediaTimeRange operator-(const QMediaTimeRange &r1, const QMediaTimeRange &r2)`

**作用与语义：**

返回包含`r2`从`r1`中减去的时间范围。

### `bool operator==(const QMediaTimeRange &lhs, const QMediaTimeRange &rhs)`

**作用与语义：**

如果`lhs`中的所有区间都存在于`rhs`中，则返回为真。

### `struct Interval`

**作用与语义：**

QMediaTimeRange：：Interval 类表示整数精度的时间区间。
区间由包含`start()`和`end()`时间指定。这些必须在构造函数中设置，因为这是一个不可变类。该类所表示的具体时间单位尚未定义——它适用于任何可以用带符号64位整数表示的时间。
`isNormal()`方法判断时间区间是否为正规（正常时间区间为 `start()` <= `end()`）。通过调用`normalized()`方法，可以从异常区间获得正常区间。
`contains()`方法确定指定时间是否在该时间区间内。
`translated()`方法返回一个时间区间，该区间通过指定的偏移向前或向后平移。

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
