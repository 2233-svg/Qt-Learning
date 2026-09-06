# QMovie

> Qt 6.11.1 · Qt GUI

## 1. 先建立直觉

**一句话定位：** `QMovie` 是 Qt 对象机制 中的类型，负责把这一机制中的数据、状态或资源交给其他 Qt 对象使用。

**模块背景：** Qt GUI 负责窗口系统集成、绘制、颜色、字体、图像、输入事件和底层 GUI 资源。

### 这是什么

`QMovie` 是 Qt 对象机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 这类对象通常参与 Qt 元对象系统。类声明中的 `Q_OBJECT`、信号、槽、属性和可调用函数会被元对象注册；Qt 可以据此完成类型查询、信号槽连接、属性访问和事件分发。对象还带有线程归属，事件和 queued connection 会投递到对象所属线程的事件循环。

**适用场景：** 使用这类对象时，先创建并确定 parent/线程归属，再配置属性和连接信号，最后调用产生异步或状态变化的函数。耗时工作不要塞进 GUI 线程的槽函数；退出时先停止异步操作，再销毁对象。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不能复制 QObject；不能把属于其他线程的对象当作普通值直接操作；不能在信号回调中阻塞事件循环；`deleteLater()` 依赖事件循环，线程即将退出时要安排好退出和清理顺序。

## 2. 依赖与对象关系

- 头文件：`#include <QMovie>`
- 继承自：QObject
- 直接派生类：未在类页中列出

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Gui)
target_link_libraries(mytarget PRIVATE Qt6::Gui)
```

**继承带来的规则：** 它属于 QObject 对象模型（直接或间接继承 QObject），因此父对象、信号与槽、事件循环和线程归属是使用主线。

### 工作机制

这类对象通常参与 Qt 元对象系统。类声明中的 `Q_OBJECT`、信号、槽、属性和可调用函数会被元对象注册；Qt 可以据此完成类型查询、信号槽连接、属性访问和事件分发。对象还带有线程归属，事件和 queued connection 会投递到对象所属线程的事件循环。

### 状态、生命周期和线程

**生命周期：** 先确定对象由谁拥有：设置 parent 后，父对象析构会递归销毁子对象；没有 parent 时可放在栈上或显式使用 `deleteLater()`。跨线程对象不能随意直接删除、移动或调用其依赖线程的成员。异步回调应使用 context 或连接到对象生命周期。

**状态与结果：** QObject 派生对象的状态通常通过属性、状态查询函数和信号变化共同表达。信号是通知，不是返回值；收到通知后应读取当前状态并处理异常路径，不能假设每个信号只会出现一次。

**线程与事件循环：** QObject 本身属于一个线程，但它的成员函数不会因为继承 QObject 就自动变成线程安全。直接调用仍在调用者线程执行；跨线程通信应使用 queued connection、信号槽或明确的同步机制。目标线程必须有事件循环，定时器和异步 I/O 才能工作。

## 3. 直接使用

使用这类对象时，先创建并确定 parent/线程归属，再配置属性和连接信号，最后调用产生异步或状态变化的函数。耗时工作不要塞进 GUI 线程的槽函数；退出时先停止异步操作，再销毁对象。 使用时通常按这个过程组织：准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 公有类型

- `enum CacheMode { CacheNone, CacheAll }`
- `enum MovieState { NotRunning, Paused, Running }`

### 属性

- `cacheMode : CacheMode`
- `speed : int`

### 公有函数

- `QMovie(QObject *parent = nullptr)`
- `QMovie(QIODevice *device, const QByteArray &format = QByteArray(), QObject *parent = nullptr)`
- `QMovie(const QString &fileName, const QByteArray &format = QByteArray(), QObject *parent = nullptr)`
- `virtual ~QMovie()`
- `QColor backgroundColor() const`
- `QBindable<QMovie::CacheMode> bindableCacheMode()`
- `QBindable<int> bindableSpeed()`
- `QMovie::CacheMode cacheMode() const`
- `int currentFrameNumber() const`
- `QImage currentImage() const`
- `QPixmap currentPixmap() const`
- `QIODevice * device() const`
- `QString fileName() const`
- `QByteArray format() const`
- `int frameCount() const`
- `QRect frameRect() const`
- `bool isValid() const`
- `bool jumpToFrame(int frameNumber)`
- `QImageReader::ImageReaderError lastError() const`
- `QString lastErrorString() const`
- `int loopCount() const`
- `int nextFrameDelay() const`
- `QSize scaledSize()`
- `void setBackgroundColor(const QColor &color)`
- `void setCacheMode(QMovie::CacheMode mode)`
- `void setDevice(QIODevice *device)`
- `void setFileName(const QString &fileName)`
- `void setFormat(const QByteArray &format)`
- `void setScaledSize(const QSize &size)`
- `int speed() const`
- `QMovie::MovieState state() const`

### 公有槽函数

- `bool jumpToNextFrame()`
- `void setPaused(bool paused)`
- `void setSpeed(int percentSpeed)`
- `void start()`
- `void stop()`

### 信号

- `void error(QImageReader::ImageReaderError error)`
- `void finished()`
- `void frameChanged(int frameNumber)`
- `void resized(const QSize &size)`
- `void started()`
- `void stateChanged(QMovie::MovieState state)`
- `void updated(const QRect &rect)`

### 静态公有成员

- `QList<QByteArray> supportedFormats()`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `enum QMovie::CacheMode`

**作用与语义：**

本枚举描述了`QMovie`的不同缓存模式。
- `QMovie::CacheNone`：`0`;默认情况下不缓存帧。
- `QMovie::CacheAll`：`1`;所有帧均被缓存。

### `enum QMovie::MovieState`

**作用与语义：**

这个枚举描述了`QMovie`的不同状态。
- `QMovie::NotRunning`：`0`;电影未运行。这是`QMovie`的初始状态，以及`stop()`被调用或电影结束后进入的状态。
- `QMovie::Paused`：`1`;电影暂停，`QMovie`停止发出`updated()`或`resized()`。该状态是在调用pause()或`setPaused`（true）后进入的。保持当前帧号，当unpause()或`setPaused`（false）被调用时，电影会继续进入下一帧。
- `QMovie::Running`：`2`;电影正在播放。

### `[bindable] cacheMode : CacheMode`

**作用与语义：**

注意：该特性支持`QProperty`绑定。
该属性保留电影的缓存模式。
当`QMovie`依赖的底层动画格式处理程序不支持跳转到动画中的特定帧，甚至不支持“倒带”动画（用于循环）时，缓存帧非常有用。此外，如果图像数据来自顺序设备，底层动画处理器无法回溯到已被读取数据的帧（使得循环完全不可能）。
为应对这种情况，可以指示`QMovie`对象缓存帧，但这会增加内存成本，即在对象生命周期内保持帧。
默认情况下，该属性设置为`CacheNone`。

**如何使用：** 调用 `cacheMode()` 读取当前值；它不会修改应用状态。

### `[bindable] speed : int`

**作用与语义：**

注意：该特性支持`QProperty`绑定。
这一特性保持了电影的节奏。
速度以原始电影速度的百分比来衡量。默认速度是100%。示例：

**如何使用：** 调用 `speed()` 读取当前值；它不会修改应用状态。

**官方示例：**

```cpp
 QMovie movie("racecar.gif");
 movie.setSpeed(200); // 2x speed
```

### `[explicit] QMovie::QMovie(QObject *parent = nullptr)`

**作用与语义：**

构造一个QMovie对象，将`parent`对象传递给`QObject`的构造函数。

### `[explicit] QMovie::QMovie(QIODevice *device, const QByteArray &format = QByteArray(), QObject *parent = nullptr)`

**作用与语义：**

构建一个QMovie对象。QMovie会使用`device`的读取图像数据，假设这些数据是开放且可读的。如果`format`不是空的，QMovie会用图像格式`format`来解码图像数据。否则，QMovie会尝试猜测格式。
`parent`对象会传递给`QObject`的构造函数。

### `[explicit] QMovie::QMovie(const QString &fileName, const QByteArray &format = QByteArray(), QObject *parent = nullptr)`

**作用与语义：**

构建一个QMovie对象。QMovie将使用`fileName`的读取图像数据。如果`format`非空，QMovie将使用图像格式`format`来解码图像数据。否则，QMovie将尝试猜测格式。
`parent`对象传递给`QObject`的构造函数。

### `[virtual noexcept] QMovie::~QMovie()`

**作用与语义：**

摧毁`QMovie`物体。

### `QColor QMovie::backgroundColor() const`

**作用与语义：**

返回电影的背景色。如果没有分配背景色，则返回无效`QColor`。

### `int QMovie::currentFrameNumber() const`

**作用与语义：**

返回当前帧的序列号。电影中第一帧的编号为0。

### `QImage QMovie::currentImage() const`

**作用与语义：**

返回当前帧作为`QImage`。

### `QPixmap QMovie::currentPixmap() const`

**作用与语义：**

返回当前帧作为`QPixmap`。

### `QIODevice *QMovie::device() const`

**作用与语义：**

返回读取图像数据`QMovie`设备的设备。如果目前没有分配设备，则返回`nullptr`。

### `[signal] void QMovie::error(QImageReader::ImageReaderError error)`

**作用与语义：**

当播放过程中出现错误`error`时，`QMovie`会发出这个信号。`QMovie`会停止电影，进入`QMovie::NotRunning`状态。

### `QString QMovie::fileName() const`

**作用与语义：**

返回`QMovie`读取图像数据的文件名称。如果没有分配文件名，或者被分配的设备不是文件，则返回空`QString`。

### `[signal] void QMovie::finished()`

**作用与语义：**

该信号在电影结束后发出。

### `QByteArray QMovie::format() const`

**作用与语义：**

返回解码图像数据时使用的格式`QMovie`。如果没有分配格式，则返回空的QByteArray()。

### `[signal] void QMovie::frameChanged(int frameNumber)`

**作用与语义：**

当帧号变为`frameNumber`时，会发出该信号。你可以调用`currentImage()`或 `currentPixmap()` 获取该帧的副本。

### `int QMovie::frameCount() const`

**作用与语义：**

返回电影中的帧数。
某些动画格式不支持此功能，此时返回为0。

### `QRect QMovie::frameRect() const`

**作用与语义：**

返回上一帧的rect。如果尚无帧更新，则返回无效`QRect`。

### `bool QMovie::isValid() const`

**作用与语义：**

如果电影有效（例如图像数据可读且支持图像格式），返回`true`;否则返回`false`。
关于为什么这部电影不有效，请参见`lastError()`。

### `bool QMovie::jumpToFrame(int frameNumber)`

**作用与语义：**

跳转到第`frameNumber`帧。成功时返回`true`;否则返回`false`。

### `[slot] bool QMovie::jumpToNextFrame()`

**作用与语义：**

跳到下一帧。成功时返回`true`;否则返回`false`。

### `QImageReader::ImageReaderError QMovie::lastError() const`

**作用与语义：**

返回尝试读取图像数据时发生的最新错误。

### `QString QMovie::lastErrorString() const`

**作用与语义：**

返回一个人类可读的最近错误表示，该错误在尝试读取图像数据时发生。

### `int QMovie::loopCount() const`

**作用与语义：**

返回电影结束前循环的次数。如果电影只播放一次（无循环），循环计数返回0。如果电影循环无限，循环计数返回-1。
注意，如果图像数据来自顺序设备（例如套接字），`QMovie`只能在`cacheMode`设置为`QMovie::CacheAll`时循环播放电影。

### `int QMovie::nextFrameDelay() const`

**作用与语义：**

返回毫秒数`QMovie`等待动画下一帧。

### `[signal] void QMovie::resized(const QSize &size)`

**作用与语义：**

当当前帧被调整为`size`时，会发出该信号。这种效果有时在动画中被用作替换帧的替代方案。你可以调用`currentImage()`或`currentPixmap()`获取更新后的帧副本。

### `QSize QMovie::scaledSize()`

**作用与语义：**

返回帧的缩放尺寸。

### `void QMovie::setBackgroundColor(const QColor &color)`

**作用与语义：**

对于支持该格式的图像格式，该函数将背景色设置为`color`。

### `void QMovie::setDevice(QIODevice *device)`

**作用与语义：**

将当前设备设置为`device`。`QMovie`会在电影播放时读取该设备的图像数据。

### `void QMovie::setFileName(const QString &fileName)`

**作用与语义：**

将`QMovie`读取图像数据的文件名设置为`fileName`。

### `void QMovie::setFormat(const QByteArray &format)`

**作用与语义：**

将`QMovie`解码图像数据时使用的格式设置为`format`。默认情况下，`QMovie`会尝试猜测图像数据的格式。
你可以致电`supportedFormats()`获取完整的格式`QMovie`支持列表。

### `[slot] void QMovie::setPaused(bool paused)`

**作用与语义：**

如果`paused`为真，`QMovie`将进入`Paused`状态并发出`stateChanged`（暂停）;否则将进入`Running`状态并发出`stateChanged`（运行）。

### `void QMovie::setScaledSize(const QSize &size)`

**作用与语义：**

将缩放后的帧大小设置为`size`。

### `[slot] void QMovie::start()`

**作用与语义：**

电影开始。`QMovie`会进入`Running`状态，随着电影推进开始发出`updated()`和`resized()`。
如果`QMovie`处于`Paused`状态，该函数等价于调用`setPaused`（false）。如果`QMovie`已经处于`Running`状态，该函数则不做任何事。

### `[signal] void QMovie::started()`

**作用与语义：**

该信号是在`QMovie::start()`被调用后发出，`QMovie`进入`QMovie::Running`状态后。

### `QMovie::MovieState QMovie::state() const`

**作用与语义：**

返回当前状态`QMovie`。

### `[signal] void QMovie::stateChanged(QMovie::MovieState state)`

**作用与语义：**

每当电影状态发生变化时，都会发出这个信号。新状态由`state`指定。

### `[slot] void QMovie::stop()`

**作用与语义：**

停止电影。`QMovie`进入`NotRunning`状态，停止发出`updated()`和 `resized()`。如果再次调用`start()`，电影将从头重新开始。
如果`QMovie`已经处于`NotRunning`态，这个函数就不做任何事。

### `[static] QList<QByteArray> QMovie::supportedFormats()`

**作用与语义：**

返回`QMovie`支持的图像格式列表。

### `[signal] void QMovie::updated(const QRect &rect)`

**作用与语义：**

当当前帧中的rect `rect`被更新时，会发出这个信号。你可以致电`currentImage()`或`currentPixmap()`获取更新帧的副本。

### `QBindable<QMovie::CacheMode> bindableCacheMode()`

**作用与语义：**

注意：该特性支持`QProperty`绑定。
该属性保留电影的缓存模式。
当`QMovie`依赖的底层动画格式处理程序不支持跳转到动画中的特定帧，甚至不支持“倒带”动画（用于循环）时，缓存帧非常有用。此外，如果图像数据来自顺序设备，底层动画处理器无法回溯到已被读取数据的帧（使得循环完全不可能）。
为应对这种情况，可以指示`QMovie`对象缓存帧，但这会增加内存成本，即在对象生命周期内保持帧。
默认情况下，该属性设置为`CacheNone`。

**如何使用：** 调用 `bindableCacheMode()` 取得 `cacheMode` 的 `QBindable`，用于建立属性绑定；只读取当前值时直接使用普通 getter。

### `QBindable<int> bindableSpeed()`

**作用与语义：**

注意：该特性支持`QProperty`绑定。
这一特性保持了电影的节奏。
速度以原始电影速度的百分比来衡量。默认速度是100%。示例：

**如何使用：** 调用 `bindableSpeed()` 取得 `speed` 的 `QBindable`，用于建立属性绑定；只读取当前值时直接使用普通 getter。

**官方示例：**

```cpp
 QMovie movie("racecar.gif");
 movie.setSpeed(200); // 2x speed
```

### `QMovie::CacheMode cacheMode() const`

**作用与语义：**

注意：该特性支持`QProperty`绑定。
该属性保留电影的缓存模式。
当`QMovie`依赖的底层动画格式处理程序不支持跳转到动画中的特定帧，甚至不支持“倒带”动画（用于循环）时，缓存帧非常有用。此外，如果图像数据来自顺序设备，底层动画处理器无法回溯到已被读取数据的帧（使得循环完全不可能）。
为应对这种情况，可以指示`QMovie`对象缓存帧，但这会增加内存成本，即在对象生命周期内保持帧。
默认情况下，该属性设置为`CacheNone`。

**如何使用：** 调用 `cacheMode()` 读取当前值；它不会修改应用状态。

### `void setCacheMode(QMovie::CacheMode mode)`

**作用与语义：**

注意：该特性支持`QProperty`绑定。
该属性保留电影的缓存模式。
当`QMovie`依赖的底层动画格式处理程序不支持跳转到动画中的特定帧，甚至不支持“倒带”动画（用于循环）时，缓存帧非常有用。此外，如果图像数据来自顺序设备，底层动画处理器无法回溯到已被读取数据的帧（使得循环完全不可能）。
为应对这种情况，可以指示`QMovie`对象缓存帧，但这会增加内存成本，即在对象生命周期内保持帧。
默认情况下，该属性设置为`CacheNone`。

**如何使用：** 调用 `setCacheMode(...)` 修改 `cacheMode`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `int speed() const`

**作用与语义：**

注意：该特性支持`QProperty`绑定。
这一特性保持了电影的节奏。
速度以原始电影速度的百分比来衡量。默认速度是100%。示例：

**如何使用：** 调用 `speed()` 读取当前值；它不会修改应用状态。

**官方示例：**

```cpp
 QMovie movie("racecar.gif");
 movie.setSpeed(200); // 2x speed
```

### `void setSpeed(int percentSpeed)`

**作用与语义：**

注意：该特性支持`QProperty`绑定。
这一特性保持了电影的节奏。
速度以原始电影速度的百分比来衡量。默认速度是100%。示例：

**如何使用：** 调用 `setSpeed(...)` 修改 `speed`；传入的新值会成为后续查询和相关界面行为所使用的值。

**官方示例：**

```cpp
 QMovie movie("racecar.gif");
 movie.setSpeed(200); // 2x speed
```

## 6. 深入实践与常见坑

### 生命周期和资源边界

先确定对象由谁拥有：设置 parent 后，父对象析构会递归销毁子对象；没有 parent 时可放在栈上或显式使用 `deleteLater()`。跨线程对象不能随意直接删除、移动或调用其依赖线程的成员。异步回调应使用 context 或连接到对象生命周期。

### 状态和错误边界

QObject 派生对象的状态通常通过属性、状态查询函数和信号变化共同表达。信号是通知，不是返回值；收到通知后应读取当前状态并处理异常路径，不能假设每个信号只会出现一次。

### 线程边界

QObject 本身属于一个线程，但它的成员函数不会因为继承 QObject 就自动变成线程安全。直接调用仍在调用者线程执行；跨线程通信应使用 queued connection、信号槽或明确的同步机制。目标线程必须有事件循环，定时器和异步 I/O 才能工作。

### 最容易出现的错误

不能复制 QObject；不能把属于其他线程的对象当作普通值直接操作；不能在信号回调中阻塞事件循环；`deleteLater()` 依赖事件循环，线程即将退出时要安排好退出和清理顺序。

### 版本和平台

本文档以 Qt 6.11.1 为依据。涉及平台后端、编解码器、数据库驱动、窗口风格、编译器特性或标注了版本号的 API 时，要把版本条件当作使用约束，而不是只看函数是否能补全。

## 7. 使用边界

`QMovie` 所属机制类型：Qt 对象机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
