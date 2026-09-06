# QOpenGLContext

> Qt 6.11.1 · Qt GUI

## 1. 先建立直觉

**一句话定位：** `QOpenGLContext` 是 Qt 对象机制 中的类型，负责把这一机制中的数据、状态或资源交给其他 Qt 对象使用。

**模块背景：** Qt GUI 负责窗口系统集成、绘制、颜色、字体、图像、输入事件和底层 GUI 资源。

### 这是什么

`QOpenGLContext` 是 Qt 对象机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 这类对象通常参与 Qt 元对象系统。类声明中的 `Q_OBJECT`、信号、槽、属性和可调用函数会被元对象注册；Qt 可以据此完成类型查询、信号槽连接、属性访问和事件分发。对象还带有线程归属，事件和 queued connection 会投递到对象所属线程的事件循环。

**适用场景：** 使用这类对象时，先创建并确定 parent/线程归属，再配置属性和连接信号，最后调用产生异步或状态变化的函数。耗时工作不要塞进 GUI 线程的槽函数；退出时先停止异步操作，再销毁对象。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不能复制 QObject；不能把属于其他线程的对象当作普通值直接操作；不能在信号回调中阻塞事件循环；`deleteLater()` 依赖事件循环，线程即将退出时要安排好退出和清理顺序。

## 2. 依赖与对象关系

- 头文件：`#include <QOpenGLContext>`
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

- `enum OpenGLModuleType { LibGL, LibGLES }`

### 公有函数

- `QOpenGLContext(QObject *parent = nullptr)`
- `virtual ~QOpenGLContext()`
- `bool create()`
- `GLuint defaultFramebufferObject() const`
- `void doneCurrent()`
- `QSet<QByteArray> extensions() const`
- `QOpenGLExtraFunctions * extraFunctions() const`
- `QSurfaceFormat format() const`
- `QOpenGLFunctions * functions() const`
- `QFunctionPointer getProcAddress(const QByteArray &procName) const`
- `QFunctionPointer getProcAddress(const char *procName) const`
- `bool hasExtension(const QByteArray &extension) const`
- `bool isOpenGLES() const`
- `bool isValid() const`
- `bool makeCurrent(QSurface *surface)`
- `QNativeInterface * nativeInterface() const`
- `QScreen * screen() const`
- `void setFormat(const QSurfaceFormat &format)`
- `void setScreen(QScreen *screen)`
- `void setShareContext(QOpenGLContext *shareContext)`
- `QOpenGLContext * shareContext() const`
- `QOpenGLContextGroup * shareGroup() const`
- `QSurface * surface() const`
- `void swapBuffers(QSurface *surface)`

### 信号

- `void aboutToBeDestroyed()`

### 静态公有成员

- `bool areSharing(QOpenGLContext *first, QOpenGLContext *second)`
- `QOpenGLContext * currentContext()`
- `QOpenGLContext * globalShareContext()`
- `QOpenGLContext::OpenGLModuleType openGLModuleType()`
- `bool supportsThreadedOpenGL()`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `enum QOpenGLContext::OpenGLModuleType`

**作用与语义：**

该枚举定义了底层OpenGL实现的类型。
- `QOpenGLContext::LibGL`：`0`;OpenGL
- `QOpenGLContext::LibGLES`：`1`;OpenGL ES 2.0 或更高版本

### `[explicit] QOpenGLContext::QOpenGLContext(QObject *parent = nullptr)`

**作用与语义：**

创建一个带有父对象`parent`的新OpenGL上下文实例。
在使用之前，你需要设置正确的格式并调用`create()`。

### `[virtual noexcept] QOpenGLContext::~QOpenGLContext()`

**作用与语义：**

摧毁`QOpenGLContext`物体。
如果这是当前线程上下文，`doneCurrent()`也会被调用。

### `[signal] void QOpenGLContext::aboutToBeDestroyed()`

**作用与语义：**

该信号在底层原生 OpenGL 上下文被破坏之前发出，用户可以清理可能在共享 OpenGL 环境中被搁置的资源。
如果你想让上下文保持电流以便进行清理，确保只通过直接连接连接到信号。
注意：在 Qt for Python 中，由于 Python 实例已被销毁，从`QOpenGLWidget`或 `QOpenGLWindow` 的解构器发出该信号时，信号将无法接收。我们建议改用 `QWidget::hideEvent()` 进行清理。

### `[static] bool QOpenGLContext::areSharing(QOpenGLContext *first, QOpenGLContext *second)`

**作用与语义：**

如果 `first` 和 `second` 上下文共享 OpenGL 资源，则返回 `true`。

### `bool QOpenGLContext::create()`

**作用与语义：**

尝试用当前配置创建 OpenGL 上下文。
当前配置包括格式、共享上下文和屏幕。
如果你系统上的 OpenGL 实现不支持请求的 OpenGL 上下文版本，`QOpenGLContext` 会尝试创建最接近的版本。实际创建的上下文属性可以通过 `format()` 函数返回的`QSurfaceFormat`查询。例如，如果你请求一个支持 OpenGL 4.3 核心配置文件的上下文，但驱动程序和/或硬件只支持 3.2 版本核心配置文件上下文，那么你会得到一个 3.2 核心配置文件上下文。
返回 `true` 是否已成功创建本地上下文，并准备好与 `makeCurrent()`、`swapBuffers()` 等一起使用。
注意：如果上下文已经存在，这个函数会先销毁现有上下文，然后创建一个新的上下文。

### `[static] QOpenGLContext *QOpenGLContext::currentContext()`

**作用与语义：**

返回当前线程中调用`makeCurrent`的最后一个上下文，若无当前上下文则返回`nullptr`。

### `GLuint QOpenGLContext::defaultFramebufferObject() const`

**作用与语义：**

调用此函数以获取当前表面的默认帧缓冲对象。在某些平台（例如 iOS）上，默认帧缓冲对象依赖于被渲染的表面，可能与 0 不同。因此，如果希望应用能跨不同 Qt 平台工作，而不是调用 glBindFramebuffer(0)，应调用 glBindFramebuffer(ctx->defaultFramebufferObject())。如果在 `QOpenGLFunctions` 中使用 glBindFramebuffer()，则无需担心此问题，因为当传递 0 时，它会自动绑定当前上下文的 defaultFramebufferObject()。注意：通过帧缓冲对象进行渲染的小部件，例如 `QOpenGLWidget` 和 `QQuickWidget`，在绘制时会覆盖此函数返回的值，因为此时正确的“默认”帧缓冲是小部件关联的后台帧缓冲，而不是属于顶层窗口表面的平台特定帧缓冲。这确保了本函数及其他依赖它的类（例如 `QOpenGLFramebufferObject::bindDefault()` 或 `QOpenGLFramebufferObject::release()`）能够正常工作。

### `void QOpenGLContext::doneCurrent()`

**作用与语义：**

方便函数，用于调用 0 曲面的 `makeCurrent`。
这会导致当前讨论中没有上下文是最新的。

### `QSet<QByteArray> QOpenGLContext::extensions() const`

**作用与语义：**

返回该上下文支持的 OpenGL 扩展集合。
上下文或共享上下文必须是最新的。

### `QOpenGLExtraFunctions *QOpenGLContext::extraFunctions() const`

**作用与语义：**

获取`QOpenGLExtraFunctions`实例来理解这个背景。
`QOpenGLContext`提供这种便捷方式，无需手动管理即可访问`QOpenGLExtraFunctions`。
上下文或共享上下文必须是最新的。
返回的`QOpenGLExtraFunctions`实例已准备好使用，无需调用初始化OpenGLFunctions()。
注意：`QOpenGLExtraFunctions`包含不保证运行时可用的功能。运行时可用性取决于平台、图形驱动以及应用程序请求的OpenGL版本。

### `QSurfaceFormat QOpenGLContext::format() const`

**作用与语义：**

如果`create()`被调用，返回底层平台上下文的格式。
否则，返回请求的格式。
请求的格式和实际格式可能不同。请求给定的 OpenGL 版本并不意味着最终的上下文会精确定位该请求版本。只要驱动程序能够提供这样的上下文，就保证所创建上下文的版本/配置文件/选项组合与请求兼容。
例如，请求 OpenGL 3.x 核心配置文件上下文，可能会生成 OpenGL 4.x 核心配置文件上下文。同样，请求 OpenGL 2.1 可能生成启用弃用函数的 OpenGL 3.0 上下文。最后，根据驱动程序不同，不支持版本可能导致上下文创建失败，或上下文支持最高版本。
缓冲区大小也可能存在类似差异，例如，最终上下文的深度缓冲区可能比请求的更大。这是完全正常的。

### `QOpenGLFunctions *QOpenGLContext::functions() const`

**作用与语义：**

获取`QOpenGLFunctions`实例来了解这个背景。
`QOpenGLContext`提供这种便捷方式，无需手动管理即可访问`QOpenGLFunctions`。
上下文或共享上下文必须是最新的。
返回的`QOpenGLFunctions`实例已准备好使用，无需初始化OpenGLFunctions()即可调用。

### `QFunctionPointer QOpenGLContext::getProcAddress(const QByteArray &procName) const`

**作用与语义：**

解析函数指针指向一个 OpenGL 扩展函数，该函数由 `procName` 标识。
使用此函数访问OpenGL扩展函数或核心函数，这些函数可能并非所有平台都以链接符号形式提供。
返回的指针可能依赖于平台。有些系统可能返回的指针不`nullptr`，即使该函数无效或不支持。
为了可靠地检查函数可用性，可以通过调用`QOpenGLContext::hasExtension()`来测试扩展支持。对于核心函数，通过 `QOpenGLContext::format()` 返回的 `QSurfaceFormat` 中的 `version()` 检查当前上下文的版本。

### `QFunctionPointer QOpenGLContext::getProcAddress(const char *procName) const`

**作用与语义：**

解析函数指针指向一个 OpenGL 扩展函数，该函数由 `procName` 标识。
使用此函数访问OpenGL扩展函数或核心函数，这些函数可能并非所有平台都以链接符号形式提供。
返回的指针可能依赖于平台。有些系统可能返回的指针不`nullptr`，即使该函数无效或不支持。
为了可靠地检查函数可用性，可以通过调用`QOpenGLContext::hasExtension()`来测试扩展支持。对于核心函数，通过 `QOpenGLContext::format()` 返回的 `QSurfaceFormat` 中的 `version()` 检查当前上下文的版本。

### `[static] QOpenGLContext *QOpenGLContext::globalShareContext()`

**作用与语义：**

如果存在，返回全应用共享的OpenGL上下文。否则，返回`nullptr`。
如果你需要在创建或展示`QOpenGLWidget`或 `QQuickWidget`之前上传 OpenGL 对象（缓冲区、纹理等）时，这非常有用。
警告：请勿尝试让该函数返回的上下文在任何表面上保持当前状态。相反，你可以创建一个与全局上下文共享的新上下文，然后使新上下文保持当前状态。

### `bool QOpenGLContext::hasExtension(const QByteArray &extension) const`

**作用与语义：**

返回`true`该 OpenGL 上下文是否支持指定的 OpenGL `extension`，`false`否则。
上下文或共享上下文必须是最新的。

### `bool QOpenGLContext::isOpenGLES() const`

**作用与语义：**

如果上下文是 OpenGL ES 上下文，则返回为真。
如果上下文尚未创建，结果基于通过`setFormat()`设置的请求格式。

### `bool QOpenGLContext::isValid() const`

**作用与语义：**

如果该上下文有效，即成功创建，则返回。
在某些平台上，之前成功创建的上下文返回`false`值表明该OpenGL上下文已丢失。
处理应用中上下文丢失场景的典型方法是通过该函数检查`makeCurrent()`失败并返回`false`。如果该函数返回`false`，则通过调用`create()`重建底层的原生OpenGL上下文，再次调用`makeCurrent()`，然后重新初始化所有OpenGL资源。
在某些平台上，上下文丢失的情况无法避免。但在其他平台上，可能需要选择加入。这可以通过在`QSurfaceFormat`中启用`ResetNotification`实现。这将导致在底层的原生OpenGL环境中设置`RESET_NOTIFICATION_STRATEGY_EXT`为`LOSE_CONTEXT_ON_RESET_EXT`。`QOpenGLContext`随后会通过每个`makeCurrent()`中的`glGetGraphicsResetStatusEXT()`监控状态。

### `bool QOpenGLContext::makeCurrent(QSurface *surface)`

**作用与语义：**

使上下文在当前线程中保持当前状态，且符合给定`surface`。成功时返回`true`;否则返回`false`。后者可能发生在表面未被暴露，或图形硬件因应用程序暂停等原因不可用时。
如果`surface` `nullptr`，这等同于调用`doneCurrent()`。
避免从该实例所在线程以外的线程调用该函数`QOpenGLContext`。如果你想从不同线程使用`QOpenGLContext`，应先确认当前线程中没有当前线程，必要时调用 `doneCurrent()`。然后在另一个线程中使用之前，先调用 moveToThread（otherThread）。
默认情况下，Qt 会对线程亲和性进行强制执行上述条件的检查。仍然可以通过设置 `Qt::AA_DontCheckOpenGLContextThreadAffinity` 应用属性来禁用该检查。请务必理解从 QObject 线程亲和性文档中解释的，使用其所在线程之外的 QObject 的后果。

### `template <typename QNativeInterface> QNativeInterface *QOpenGLContext::nativeInterface() const`

**作用与语义：**

返回上下文中给定类型的本地接口。
该功能提供访问`QOpenGLContext`特定平台的功能，定义在`QNativeInterface`命名空间中：
- `QNativeInterface::QCocoaGLContext`：macOS 上 NSOpenGLContext 的原生接口
- `QNativeInterface::QEGLContext`：与 EGL 上下文的本地接口
- `QNativeInterface::QGLXContext`：GLX 上下文的本地接口
- `QNativeInterface::QWGLContext`：Windows上的WGL上下文的本地接口
如果请求的接口不可用，则返回`nullptr`。

### `[static] QOpenGLContext::OpenGLModuleType QOpenGLContext::openGLModuleType()`

**作用与语义：**

返回底层的OpenGL实现类型。
在OpenGL实现未动态加载的平台上，返回值在编译时确定，且永远不会改变。
注意：桌面OpenGL实现也可能能够创建兼容ES的上下文。因此，在大多数情况下，更合适的做法是检查`QSurfaceFormat::renderableType()`或使用便利函数`isOpenGLES()`。
注意：该函数要求`QGuiApplication`实例已经被创建。

### `QScreen *QOpenGLContext::screen() const`

**作用与语义：**

返回上下文创建的屏幕。

### `void QOpenGLContext::setFormat(const QSurfaceFormat &format)`

**作用与语义：**

设置了OpenGL上下文应兼容的`format`。你需要调用`create()`才能生效。
当该函数未明确设置格式时，将使用`QSurfaceFormat::defaultFormat()`返回的格式。这意味着当有多个上下文时，单个调用该函数可以被一个调用替换，然后再创建一个上下文`QSurfaceFormat::setDefaultFormat()`。

### `void QOpenGLContext::setScreen(QScreen *screen)`

**作用与语义：**

它设置了OpenGL上下文应有效的适用`screen`。你需要调用`create()`才能生效。

### `void QOpenGLContext::setShareContext(QOpenGLContext *shareContext)`

**作用与语义：**

它让这个上下文与`shareContext`共享纹理、着色器和其他OpenGL资源。你需要调用`create()`才能生效。

### `QOpenGLContext *QOpenGLContext::shareContext() const`

**作用与语义：**

返回创建该上下文时使用的共享上下文。
如果底层平台无法支持请求的共享，则返回0。

### `QOpenGLContextGroup *QOpenGLContext::shareGroup() const`

**作用与语义：**

返回该上下文所属的共享组。

### `[static] bool QOpenGLContext::supportsThreadedOpenGL()`

**作用与语义：**

如果平台支持主线程（GUI）之外的OpenGL渲染，返回`true`。
该值由所使用的平台插件控制，也可能取决于图形驱动程序。

### `QSurface *QOpenGLContext::surface() const`

**作用与语义：**

返回上下文所更新的表面。
这就是作为论据传递给`makeCurrent()`的表面。

### `void QOpenGLContext::swapBuffers(QSurface *surface)`

**作用与语义：**

把`surface`的前后缓冲区互换。
调用它以完成一帧 OpenGL 渲染，并在发出任何后续 OpenGL 命令前（例如作为新帧的一部分）再次调用 `makeCurrent()`。

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

`QOpenGLContext` 所属机制类型：Qt 对象机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
