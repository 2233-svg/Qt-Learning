# QWindowCapture

> Qt 6.11.1 · Qt Multimedia

## 1. 先建立直觉

**一句话定位：** `QWindowCapture` 是 Qt Multimedia 的“窗口采集”类型，参与媒体源、设备、格式、播放/采集状态或音视频数据处理。

**模块背景：** Qt Multimedia 提供音频、视频、摄像头、媒体会话和设备访问能力。

### 这是什么

`QWindowCapture` 是 多媒体设备与会话机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 多媒体类型通常把设备、媒体会话、格式、播放状态和异步错误分开。硬件能力、平台后端、权限和资源状态会影响结果；请求成功发起不等于设备已准备好。

**适用场景：** 先检查平台能力和权限，再创建会话/设备，设置格式和源，连接状态与错误信号，执行开始/暂停/停止并在结束后清理。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要假设所有平台支持相同编解码器和格式；不要忽略权限和后端错误；不要在状态未准备好时连续调用控制 API；媒体对象销毁前先停止使用。

## 2. 依赖与对象关系

- 头文件：`#include <QWindowCapture>`
- 继承自：QObject
- 直接派生类：未在类页中列出

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Multimedia)
target_link_libraries(mytarget PRIVATE Qt6::Multimedia)
```

**继承带来的规则：** 它属于 QObject 对象模型（直接或间接继承 QObject），因此父对象、信号与槽、事件循环和线程归属是使用主线。

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

- `enum Error { NoError, InternalError, CapturingNotSupported, CaptureFailed, NotFound }`

### 属性

- `active : bool`
- `error : Error`
- `errorString : QString`
- `window : QCapturableWindow`

### 公有函数

- `QWindowCapture(QObject *parent = nullptr)`
- `virtual ~QWindowCapture() override`
- `QWindowCapture::Error error() const`
- `QString errorString() const`
- `bool isActive() const`
- `void setWindow(QCapturableWindow window)`
- `QCapturableWindow window() const`

### 公有槽函数

- `void setActive(bool active)`
- `void start()`
- `void stop()`

### 信号

- `void activeChanged(bool)`
- `void errorChanged()`
- `void errorOccurred(QWindowCapture::Error error, const QString &errorString)`
- `void windowChanged(QCapturableWindow window)`

### 静态公有成员

- `QList<QCapturableWindow> capturableWindows()`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `enum QWindowCapture::Error`

**作用与语义：**

枚举可由`QWindowCapture`类信号的错误代码。`errorString()`提供错误原因的详细信息。
- `QWindowCapture::NoError`：`0`;无错误
- `QWindowCapture::InternalError`：`1`;内部窗口捕获驱动错误
- `QWindowCapture::CapturingNotSupported`：`2`;不支持窗口捕获
- `QWindowCapture::CaptureFailed`：`4`;捕获窗口失败
- `QWindowCapture::NotFound`：`5`;未找到选定窗口

### `active : bool`

**作用与语义：**

该属性决定捕获是否当前有效。

**如何使用：** 调用 `active()` 读取当前值；它不会修改应用状态。

### `[read-only] error : Error`

**作用与语义：**

该属性包含最后一次错误的代码。

**如何使用：** 调用 `error()` 读取当前值；它不会修改应用状态。

### `[read-only] errorString : QString`

**作用与语义：**

该属性包含一个人类可读的字符串，描述错误原因。

**如何使用：** 调用 `errorString()` 读取当前值；它不会修改应用状态。

### `window : QCapturableWindow`

**作用与语义：**

该属性为捕获提供了窗口。

**如何使用：** 调用 `window()` 读取当前值；它不会修改应用状态。

### `[explicit] QWindowCapture::QWindowCapture(QObject *parent = nullptr)`

**作用与语义：**

构造一个新的QWindowCapture对象，`parent`。

### `[override virtual noexcept] QWindowCapture::~QWindowCapture()`

**作用与语义：**

摧毁了该物体。

### `[static invokable] QList<QCapturableWindow> QWindowCapture::capturableWindows()`

**作用与语义：**

返回可捕获的`QCapturableWindow`对象列表。
注意：该函数可通过元对象系统和QML调用。参见`Q_INVOKABLE`。

### `[signal] void QWindowCapture::errorOccurred(QWindowCapture::Error error, const QString &errorString)`

**作用与语义：**

当`error`发生时，以及`errorString`。

### `[slot] void QWindowCapture::start()`

**作用与语义：**

开始捕捉`window`。
这等同于将`active`属性设置为 true。

### `[slot] void QWindowCapture::stop()`

**作用与语义：**

停止捕捉。
这等同于将`active`属性设置为false。

### `QWindowCapture::Error error() const`

**作用与语义：**

该属性包含最后一次错误的代码。

**如何使用：** 调用 `error()` 读取当前值；它不会修改应用状态。

### `QString errorString() const`

**作用与语义：**

该属性包含一个人类可读的字符串，描述错误原因。

**如何使用：** 调用 `errorString()` 读取当前值；它不会修改应用状态。

### `bool isActive() const`

**作用与语义：**

该属性决定捕获是否当前有效。

**如何使用：** 调用 `isActive()` 读取当前值；它不会修改应用状态。

### `void setWindow(QCapturableWindow window)`

**作用与语义：**

该属性为捕获提供了窗口。

**如何使用：** 调用 `setWindow(...)` 修改 `window`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `QCapturableWindow window() const`

**作用与语义：**

该属性为捕获提供了窗口。

**如何使用：** 调用 `window()` 读取当前值；它不会修改应用状态。

### `void setActive(bool active)`

**作用与语义：**

该属性决定捕获是否当前有效。

**如何使用：** 调用 `setActive(...)` 修改 `active`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void activeChanged(bool)`

**作用与语义：**

该属性决定捕获是否当前有效。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `active` 的变化，不要把它当作普通函数主动调用。

### `void errorChanged()`

**作用与语义：**

该属性包含最后一次错误的代码。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `error` 的变化，不要把它当作普通函数主动调用。

### `void windowChanged(QCapturableWindow window)`

**作用与语义：**

该属性为捕获提供了窗口。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `window` 的变化，不要把它当作普通函数主动调用。

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

`QWindowCapture` 所属机制类型：多媒体设备与会话机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
