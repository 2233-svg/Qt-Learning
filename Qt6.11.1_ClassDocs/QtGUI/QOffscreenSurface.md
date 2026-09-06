# QOffscreenSurface

> Qt 6.11.1 · Qt GUI

## 1. 先建立直觉

**一句话定位：** `QOffscreenSurface` 是 Qt 对象机制 中的类型，负责把这一机制中的数据、状态或资源交给其他 Qt 对象使用。

**模块背景：** Qt GUI 负责窗口系统集成、绘制、颜色、字体、图像、输入事件和底层 GUI 资源。

### 这是什么

`QOffscreenSurface` 是 Qt 对象机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 这类对象通常参与 Qt 元对象系统。类声明中的 `Q_OBJECT`、信号、槽、属性和可调用函数会被元对象注册；Qt 可以据此完成类型查询、信号槽连接、属性访问和事件分发。对象还带有线程归属，事件和 queued connection 会投递到对象所属线程的事件循环。

**适用场景：** 使用这类对象时，先创建并确定 parent/线程归属，再配置属性和连接信号，最后调用产生异步或状态变化的函数。耗时工作不要塞进 GUI 线程的槽函数；退出时先停止异步操作，再销毁对象。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不能复制 QObject；不能把属于其他线程的对象当作普通值直接操作；不能在信号回调中阻塞事件循环；`deleteLater()` 依赖事件循环，线程即将退出时要安排好退出和清理顺序。

## 2. 依赖与对象关系

- 头文件：`#include <QOffscreenSurface>`
- 继承自：QObject、QSurface
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

### 公有函数

- `QOffscreenSurface(QScreen *targetScreen = nullptr, QObject *parent = nullptr)`
- `virtual ~QOffscreenSurface()`
- `void create()`
- `void destroy()`
- `bool isValid() const`
- `QNativeInterface * nativeInterface() const`
- `QSurfaceFormat requestedFormat() const`
- `QScreen * screen() const`
- `void setFormat(const QSurfaceFormat &format)`
- `void setScreen(QScreen *newScreen)`

### 重实现的公有函数

- `virtual QSurfaceFormat format() const override`
- `virtual QSize size() const override`
- `virtual QSurface::SurfaceType surfaceType() const override`

### 信号

- `void screenChanged(QScreen *screen)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `[explicit] QOffscreenSurface::QOffscreenSurface(QScreen *targetScreen = nullptr, QObject *parent = nullptr)`

**作用与语义：**

用给定的`parent`为`targetScreen`创建一个屏幕外的表面。
底层平台表面直到`create()`被调用后才会形成。

### `[virtual noexcept] QOffscreenSurface::~QOffscreenSurface()`

**作用与语义：**

破坏了幕外的表面。

### `void QOffscreenSurface::create()`

**作用与语义：**

分配与屏幕外表面相关的平台资源。
此时，使用`setFormat()`的曲面格式被解析为实际的原生曲面。
如有必要，`destroy()`释放平台资源。
注意：有些平台要求在主线（GUI）线程中调用该函数。

### `void QOffscreenSurface::destroy()`

**作用与语义：**

释放与该幕外表面相关的原生平台资源。

### `[override virtual] QSurfaceFormat QOffscreenSurface::format() const`

**作用与语义：**

重装：`QSurface::format()` const.
返回这个屏幕外表面的实际格式。
创建出屏外表面后，该函数会返回实际的表面格式。如果平台无法满足请求的格式，它可能会与请求的格式不同。
返回表面的格式。

### `bool QOffscreenSurface::isValid() const`

**作用与语义：**

如果该屏幕外表面有效，返回`true`;否则返回`false`。
如果平台资源已成功分配，屏幕外的表面是有效的。

### `template <typename QNativeInterface> QNativeInterface *QOffscreenSurface::nativeInterface() const`

**作用与语义：**

返回该表面的本地接口。
该功能提供访问 QOffScreenSurface 的平台特定功能，定义在 `QNativeInterface` 命名空间中：
- `QNativeInterface::QAndroidOffscreenSurface`：Android屏幕外表面的原生接口
如果请求的接口不可用，则返回`nullptr`。

### `QSurfaceFormat QOffscreenSurface::requestedFormat() const`

**作用与语义：**

返回该屏幕外表面的请求表面格式。
如果请求的格式未被平台实现支持，requestedFormat 将与实际的屏幕外表面格式不同。
这是与`setFormat()`值的集合。

### `QScreen *QOffscreenSurface::screen() const`

**作用与语义：**

返回连接屏幕外表面的屏幕。

### `[signal] void QOffscreenSurface::screenChanged(QScreen *screen)`

**作用与语义：**

当屏幕外表面的`screen`发生变化时，该信号会发出，无论是通过显式设置`setScreen()`，还是在窗口屏幕移除时自动触发。

### `void QOffscreenSurface::setFormat(const QSurfaceFormat &format)`

**作用与语义：**

设定了幕后表面`format`。
曲面格式将在`create()`函数中解析。在`create()`后调用该函数不会重新解析本地曲面的曲面格式。

### `void QOffscreenSurface::setScreen(QScreen *newScreen)`

**作用与语义：**

设置屏幕外表面连接的屏幕。
如果屏幕外的表面已经创建，它会在`newScreen`上重新创建。

### `[override virtual] QSize QOffscreenSurface::size() const`

**作用与语义：**

重装：`QSurface::size()` const.
返回屏幕外表面的大小。
返回表面的像素大小。

### `[override virtual] QSurface::SurfaceType QOffscreenSurface::surfaceType() const`

**作用与语义：**

重装：`QSurface::surfaceType()` const.
返回屏幕外表面的表面类型。
屏幕外表面的表面类型总是`QSurface::OpenGLSurface`。
返回表面类型。

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

`QOffscreenSurface` 所属机制类型：Qt 对象机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
