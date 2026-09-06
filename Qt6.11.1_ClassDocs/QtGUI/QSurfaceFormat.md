# QSurfaceFormat

> Qt 6.11.1 · Qt GUI

## 1. 先建立直觉

**一句话定位：** 这是格式或能力描述类型，重点关注可用格式、属性查询和与实际数据对象之间的转换。

**模块背景：** Qt GUI 负责窗口系统集成、绘制、颜色、字体、图像、输入事件和底层 GUI 资源。

### 这是什么

`QSurfaceFormat` 是 Qt 类型机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 这个类的行为由它的继承关系、构造参数、公开状态和成员函数协议共同决定。使用时要把创建、配置、核心操作、结果/通知和清理看成一条闭环，而不是孤立调用某个函数。

**适用场景：** 围绕这个类的核心职责建立最小闭环：准备依赖 -> 创建/取得对象 -> 设置必要配置 -> 调用核心 API -> 检查返回值和状态 -> 处理结果/错误 -> 结束时清理。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要忽略构造失败、空返回、默认值和版本限制；不要把异步 API 当同步 API；不要在没有确认所有权和线程的情况下保存指针或跨线程调用。

## 2. 依赖与对象关系

- 头文件：`#include <QSurfaceFormat>`
- 继承自：未在类页中列出
- 直接派生类：未在类页中列出

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Gui)
target_link_libraries(mytarget PRIVATE Qt6::Gui)
```

**继承带来的规则：** 它是值类型或不直接使用 QObject 对象模型，重点放在数据语义、拷贝/移动成本和参数有效性。

### 工作机制

这个类的行为由它的继承关系、构造参数、公开状态和成员函数协议共同决定。使用时要把创建、配置、核心操作、结果/通知和清理看成一条闭环，而不是孤立调用某个函数。

### 状态、生命周期和线程

**生命周期：** 先确认对象是值类型还是 QObject 派生对象，再确定所有权、有效期、拷贝成本和销毁方式。返回的句柄、索引、reply、设备或迭代器可能有独立的有效期，不能只看 C++ 指针是否非空。

**状态与结果：** 把返回值、状态查询、错误信息和通知信号分开判断。调用成功可能只表示请求被接受，真正完成还要等待状态变化或完成信号；读取数据前先检查对象和结果是否有效。

**线程与事件循环：** 如果类型直接或间接参与 QObject、GUI、设备或异步框架，就必须确认线程归属和事件循环；值类型虽然可以复制，也要注意内部指针、共享数据和并发写入。

## 3. 直接使用

围绕这个类的核心职责建立最小闭环：准备依赖 -> 创建/取得对象 -> 设置必要配置 -> 调用核心 API -> 检查返回值和状态 -> 处理结果/错误 -> 结束时清理。 使用时通常按这个过程组织：准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 公有类型

- `enum FormatOption { StereoBuffers, DebugContext, DeprecatedFunctions, ResetNotification, ProtectedContent }`
- `flags FormatOptions`
- `enum OpenGLContextProfile { NoProfile, CoreProfile, CompatibilityProfile }`
- `enum RenderableType { DefaultRenderableType, OpenGL, OpenGLES, OpenVG }`
- `enum SwapBehavior { DefaultSwapBehavior, SingleBuffer, DoubleBuffer, TripleBuffer }`

### 公有函数

- `QSurfaceFormat()`
- `QSurfaceFormat(QSurfaceFormat::FormatOptions options)`
- `QSurfaceFormat(const QSurfaceFormat &other)`
- `~QSurfaceFormat()`
- `int alphaBufferSize() const`
- `int blueBufferSize() const`
- `const QColorSpace & colorSpace() const`
- `int depthBufferSize() const`
- `int greenBufferSize() const`
- `bool hasAlpha() const`
- `int majorVersion() const`
- `int minorVersion() const`
- `QSurfaceFormat::FormatOptions options() const`
- `QSurfaceFormat::OpenGLContextProfile profile() const`
- `int redBufferSize() const`
- `QSurfaceFormat::RenderableType renderableType() const`
- `int samples() const`
- `void setAlphaBufferSize(int size)`
- `void setBlueBufferSize(int size)`
- `(since 6.0) void setColorSpace(const QColorSpace &colorSpace)`
- `void setDepthBufferSize(int size)`
- `void setGreenBufferSize(int size)`
- `void setMajorVersion(int major)`
- `void setMinorVersion(int minor)`
- `void setOption(QSurfaceFormat::FormatOption option, bool on = true)`
- `void setOptions(QSurfaceFormat::FormatOptions options)`
- `void setProfile(QSurfaceFormat::OpenGLContextProfile profile)`
- `void setRedBufferSize(int size)`
- `void setRenderableType(QSurfaceFormat::RenderableType type)`
- `void setSamples(int numSamples)`
- `void setStencilBufferSize(int size)`
- `void setStereo(bool enable)`
- `void setSwapBehavior(QSurfaceFormat::SwapBehavior behavior)`
- `void setSwapInterval(int interval)`
- `void setVersion(int major, int minor)`
- `int stencilBufferSize() const`
- `bool stereo() const`
- `QSurfaceFormat::SwapBehavior swapBehavior() const`
- `int swapInterval() const`
- `bool testOption(QSurfaceFormat::FormatOption option) const`
- `std::pair<int, int> version() const`
- `QSurfaceFormat & operator=(const QSurfaceFormat &other)`

### 静态公有成员

- `QSurfaceFormat defaultFormat()`
- `void setDefaultFormat(const QSurfaceFormat &format)`

### 相关非成员函数

- `bool operator!=(const QSurfaceFormat &lhs, const QSurfaceFormat &rhs)`
- `bool operator==(const QSurfaceFormat &lhs, const QSurfaceFormat &rhs)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `enum QSurfaceFormat::FormatOptionflags QSurfaceFormat::FormatOptions`

**作用与语义：**

该枚举包含用于与`QSurfaceFormat`的格式选项。
- `QSurfaceFormat::StereoBuffers`：`0x0001`;用于请求表面格式的立体声缓冲。
- `QSurfaceFormat::DebugContext`：`0x0002`;用于请求带有额外调试信息的调试上下文。
- `QSurfaceFormat::DeprecatedFunctions`：`0x0004`;用于请求将弃用函数包含在 OpenGL 上下文配置文件中。如果未指定，你应获得一个前向兼容的上下文，且没有支持功能，标记为弃用。这需要 OpenGL 3.0 或更高版本。
- `QSurfaceFormat::ResetNotification`：`0x0008`;启用关于 OpenGL 上下文重置的通知。状态随后可通过上下文的 `isValid()` 函数查询。注意，未设置该标志并不保证上下文状态丢失永远不会发生。此外，某些实现可能选择报告上下文丢失，尽管该标志存在。支持动态支持上下文丢失监控的平台，如 Windows 的 WGL，或 Linux/X11（xcb）的 GLX，会监控每次调用 `makeCurrent()` 的状态。详见`isValid()`相关信息。
- `QSurfaceFormat::ProtectedContent`：`0x0010`;允许访问受保护内容。这使得GPU能够操作受保护的资源（表面、缓冲区、纹理），例如受DRM保护的视频内容。目前仅为EGL实现。
FormatOptions 类型是 QFlags 的 typedef<FormatOption>。它存储 FormatOption 值的 OR 组合。

### `enum QSurfaceFormat::OpenGLContextProfile`

**作用与语义：**

该枚举用于指定OpenGL上下文配置文件，配合`QSurfaceFormat::setMajorVersion()`和`QSurfaceFormat::setMinorVersion()`。
配置文件在 OpenGL 3.2 及以上版本中公开，用于在受限核心配置文件和可能包含已废弃支持功能的兼容性配置文件之间进行选择。
注意，核心配置文件可能仍包含已弃用并在更高版本中计划移除的功能。要访问该核心配置文件的弃用功能，可以在设置的OpenGL版本中使用`QSurfaceFormat`格式选项`QSurfaceFormat::DeprecatedFunctions`。
- `QSurfaceFormat::NoProfile`：`0`;OpenGL 版本低于 3.2。对于 3.2 及以后版本，这与 CoreProfile 相同。
- `QSurfaceFormat::CoreProfile`：`1`;OpenGL 3.0 版本中弃用的功能不可用。
- `QSurfaceFormat::CompatibilityProfile`：`2`;可用早期 OpenGL 版本的功能。

### `enum QSurfaceFormat::RenderableType`

**作用与语义：**

该枚举指定了该表面的渲染后端。
- `QSurfaceFormat::DefaultRenderableType`：`0x0`;默认的未指定渲染方法
- `QSurfaceFormat::OpenGL`：`0x1`;桌面OpenGL渲染
- `QSurfaceFormat::OpenGLES`：`0x2`;OpenGL ES 2.0 渲染
- `QSurfaceFormat::OpenVG`：`0x4`;开放矢量图形渲染

### `enum QSurfaceFormat::SwapBehavior`

**作用与语义：**

`QSurfaceFormat`用该枚举来指定曲面的交换行为。交换行为对应用程序来说大多透明，但它会影响渲染延迟和吞吐量等因素。
- `QSurfaceFormat::DefaultSwapBehavior`：`0`;平台默认的、未指定掉期行为。
- `QSurfaceFormat::SingleBuffer`：`1`;用于请求单缓冲，当OpenGL直接渲染到屏幕且没有中间屏外缓冲时，可能导致闪烁。
- `QSurfaceFormat::DoubleBuffer`：`2`;这通常是桌面平台上默认的交换行为，由一个后缓冲区和一个前缓冲区组成。渲染先对后缓冲区进行，然后交换后缓冲区和前缓冲区，或者根据实现方式将后缓冲区内容复制到前缓冲区。
- `QSurfaceFormat::TripleBuffer`：`3`;这种交换行为有时用于降低在渲染率勉强跟上屏幕刷新率时跳帧的风险。根据平台，由于流水线行为的改进，这也可能带来GPU的稍微更高效利用。三重缓冲会以额外的一帧内存使用和延迟为代价，且根据底层平台可能不支持。

### `QSurfaceFormat::QSurfaceFormat()`

**作用与语义：**

构建默认初始化的QSurfaceFormat。
注意：默认情况下请求使用 OpenGL 2.0，因为它提供了平台与 OpenGL 实现之间最高级别的可移植性。

### `QSurfaceFormat::QSurfaceFormat(QSurfaceFormat::FormatOptions options)`

**作用与语义：**

构造一个QSurfaceFormat，格式为`options`。

### `QSurfaceFormat::QSurfaceFormat(const QSurfaceFormat &other)`

**作用与语义：**

复制了`other`。

### `[noexcept] QSurfaceFormat::~QSurfaceFormat()`

**作用与语义：**

毁掉`QSurfaceFormat`。

### `int QSurfaceFormat::alphaBufferSize() const`

**作用与语义：**

获取颜色缓冲区α通道的比特大小。

### `int QSurfaceFormat::blueBufferSize() const`

**作用与语义：**

获取颜色缓冲区蓝色通道的比特大小。

### `const QColorSpace &QSurfaceFormat::colorSpace() const`

**作用与语义：**

返回色彩空间。

### `[static] QSurfaceFormat QSurfaceFormat::defaultFormat()`

**作用与语义：**

返回全局默认表面格式。
当未调用`setDefaultFormat()`时，这就是默认构造的`QSurfaceFormat`。

### `int QSurfaceFormat::depthBufferSize() const`

**作用与语义：**

返回深度缓冲区大小。

### `int QSurfaceFormat::greenBufferSize() const`

**作用与语义：**

获取颜色缓冲区绿色通道的比特大小。

### `bool QSurfaceFormat::hasAlpha() const`

**作用与语义：**

如果 alpha 缓冲区大小大于零，返回 `true`。
这意味着表面可能会被用来实现每像素的半透明效果。

### `int QSurfaceFormat::majorVersion() const`

**作用与语义：**

回归主要的OpenGL版本。
默认版本是2.0。

### `int QSurfaceFormat::minorVersion() const`

**作用与语义：**

返回了次要的OpenGL版本。

### `QSurfaceFormat::FormatOptions QSurfaceFormat::options() const`

**作用与语义：**

返回当前设置的格式选项。

### `QSurfaceFormat::OpenGLContextProfile QSurfaceFormat::profile() const`

**作用与语义：**

获取配置好的OpenGL上下文配置文件。
如果请求的OpenGL版本小于3.2，则忽略该设置。

### `int QSurfaceFormat::redBufferSize() const`

**作用与语义：**

获取颜色缓冲区红色通道的位数。

### `QSurfaceFormat::RenderableType QSurfaceFormat::renderableType() const`

**作用与语义：**

它得到了可渲染类型。
在桌面OpenGL、OpenGL ES和 `OpenVG` 之间选择。

### `int QSurfaceFormat::samples() const`

**作用与语义：**

启用多重采样时返回每像素采样的采样数，禁用多采样时返回`-1`。默认返回值为`-1`。

### `void QSurfaceFormat::setAlphaBufferSize(int size)`

**作用与语义：**

设置颜色缓冲区α通道的比特为单位的期望`size`。

### `void QSurfaceFormat::setBlueBufferSize(int size)`

**作用与语义：**

设置颜色缓冲区蓝色通道的比特为单位的期望`size`。

### `[since 6.0] void QSurfaceFormat::setColorSpace(const QColorSpace &colorSpace)`

**作用与语义：**

设置首选`colorSpace`。
例如，这允许在支持sRGB的平台上请求默认帧缓冲区的窗口。
注意：当平台不支持请求的色彩空间时，请求将被忽略。创建窗口后查询`QSurfaceFormat`，以确认颜色空间请求是否能被接受。
注意：该设置控制窗口默认帧缓冲区是否能够在特定色彩空间中更新和混合。它本身不会改变应用程序的输出。应用程序的渲染代码仍需通过相应的OpenGL调用选择加入，以启用在给定色彩空间内进行更新和混合，而非使用标准线性操作。

### `[static] void QSurfaceFormat::setDefaultFormat(const QSurfaceFormat &format)`

**作用与语义：**

设置全局默认表面`format`。
该格式默认用于`QOpenGLContext`、`QWindow`、`QOpenGLWidget`等类。
它总可以通过使用该类自身的 setFormat() 函数在每个实例上覆盖。不过，通常在应用程序开始时一次性设置所有窗口的格式会更方便。它还保证了在需要共享上下文的情况下的正确行为，因为通过该函数设置格式保证所有上下文和表面，即使是由 Qt 内部创建的，也将使用相同的格式。

### `void QSurfaceFormat::setDepthBufferSize(int size)`

**作用与语义：**

将最小深度缓冲区大小设置为`size`。

### `void QSurfaceFormat::setGreenBufferSize(int size)`

**作用与语义：**

设置颜色缓冲区绿色通道的比特为单位的期望`size`。

### `void QSurfaceFormat::setMajorVersion(int major)`

**作用与语义：**

设置目标`major` OpenGL版本。

### `void QSurfaceFormat::setMinorVersion(int minor)`

**作用与语义：**

设置目标`minor` OpenGL版本。
默认版本是2.0。

### `void QSurfaceFormat::setOption(QSurfaceFormat::FormatOption option, bool on = true)`

**作用与语义：**

如果 `on`为真，设置格式选项为 `option`;否则，清除该选项。
为了验证选项是否被尊重，可以在生成表面/上下文后将实际格式与请求的格式进行比较。

### `void QSurfaceFormat::setOptions(QSurfaceFormat::FormatOptions options)`

**作用与语义：**

将格式选项设置为`options`。
为了验证选项是否被尊重，可以在生成表面/上下文后将实际格式与请求的格式进行比较。

### `void QSurfaceFormat::setProfile(QSurfaceFormat::OpenGLContextProfile profile)`

**作用与语义：**

设置所需的OpenGL上下文`profile`。
如果请求的OpenGL版本小于3.2，则忽略该设置。

### `void QSurfaceFormat::setRedBufferSize(int size)`

**作用与语义：**

设置颜色缓冲区红色通道的比特为单位的期望`size`。

### `void QSurfaceFormat::setRenderableType(QSurfaceFormat::RenderableType type)`

**作用与语义：**

设置所需的可渲染`type`。
可以在桌面版OpenGL、OpenGL ES和`OpenVG`之间选择。

### `void QSurfaceFormat::setSamples(int numSamples)`

**作用与语义：**

当启用多重采样时，将每像素的首选采样数设置为`numSamples`。默认情况下，多重采样是被禁用的。

### `void QSurfaceFormat::setStencilBufferSize(int size)`

**作用与语义：**

将首选模板缓冲区大小设置为`size`位。

### `void QSurfaceFormat::setStereo(bool enable)`

**作用与语义：**

如果`enable`为真，则启用立体声缓冲;否则禁用立体声缓冲。
立体声缓冲默认是禁用的。
立体缓冲提供额外的颜色缓冲区，用于生成左眼和右眼图像。

### `void QSurfaceFormat::setSwapBehavior(QSurfaceFormat::SwapBehavior behavior)`

**作用与语义：**

把交换`behavior`设在表面。
交换行为指定了需要单缓冲、双缓冲还是三缓冲。默认设置`DefaultSwapBehavior`显示平台默认交换行为。

### `void QSurfaceFormat::setSwapInterval(int interval)`

**作用与语义：**

设置首选的交换间隔。交换间隔指定了缓冲区交换发生前显示的最小视频帧数。这可以用来将窗口中的GL绘制与屏幕的垂直刷新同步。
将`interval`值设为0会关闭垂直刷新同步，任何高于0的值都会开启垂直同步。将`interval`设为更高的值，例如10，则每次缓冲区交换之间会有10次垂直回扫。
默认间隔为1。
底层平台可能不支持更改交换间隔。在这种情况下，请求将被无声忽略。

### `void QSurfaceFormat::setVersion(int major, int minor)`

**作用与语义：**

设置所需的`major`和`minor` OpenGL版本。
默认版本是2.0。

### `int QSurfaceFormat::stencilBufferSize() const`

**作用与语义：**

返回模板缓冲区大小（比特）。

### `bool QSurfaceFormat::stereo() const`

**作用与语义：**

如果启用立体声缓冲，返回`true`;否则返回false。立体声缓冲默认被禁用。

### `QSurfaceFormat::SwapBehavior QSurfaceFormat::swapBehavior() const`

**作用与语义：**

返回配置中的交换行为。

### `int QSurfaceFormat::swapInterval() const`

**作用与语义：**

返回交换间隔。

### `bool QSurfaceFormat::testOption(QSurfaceFormat::FormatOption option) const`

**作用与语义：**

如果设置了格式选项`option`，则返回true;否则返回false。

### `std::pair<int, int> QSurfaceFormat::version() const`

**作用与语义：**

返回一个 std：:p air<int， int>，代表 OpenGL 版本。
用于版本检查，例如 format.version() >= std：:p air（3， 2）。

### `QSurfaceFormat &QSurfaceFormat::operator=(const QSurfaceFormat &other)`

**作用与语义：**

为该对象分配`other`。

### `[noexcept] bool operator!=(const QSurfaceFormat &lhs, const QSurfaceFormat &rhs)`

**作用与语义：**

如果两个 `QSurfaceFormat` 对象 `lhs` 和 `rhs` 的所有选项都相等，则返回 `lhs`；否则返回 `true`。

### `[noexcept] bool operator==(const QSurfaceFormat &lhs, const QSurfaceFormat &rhs)`

**作用与语义：**

如果两个`QSurfaceFormat`对象`lhs`和`rhs`的所有选项相等，返回`true`。

### `enum FormatOption { StereoBuffers, DebugContext, DeprecatedFunctions, ResetNotification, ProtectedContent }`

**作用与语义：**

该枚举包含用于与`QSurfaceFormat`的格式选项。
- `QSurfaceFormat::StereoBuffers`：`0x0001`;用于请求表面格式的立体声缓冲。
- `QSurfaceFormat::DebugContext`：`0x0002`;用于请求带有额外调试信息的调试上下文。
- `QSurfaceFormat::DeprecatedFunctions`：`0x0004`;用于请求将弃用函数包含在 OpenGL 上下文配置文件中。如果未指定，你应获得一个前向兼容的上下文，且没有支持功能，标记为弃用。这需要 OpenGL 3.0 或更高版本。
- `QSurfaceFormat::ResetNotification`：`0x0008`;启用关于 OpenGL 上下文重置的通知。状态随后可通过上下文的 `isValid()` 函数查询。注意，未设置该标志并不保证上下文状态丢失永远不会发生。此外，某些实现可能选择报告上下文丢失，尽管该标志存在。支持动态支持上下文丢失监控的平台，如 Windows 的 WGL，或 Linux/X11（xcb）的 GLX，会监控每次调用 `makeCurrent()` 的状态。详见`isValid()`相关信息。
- `QSurfaceFormat::ProtectedContent`：`0x0010`;允许访问受保护内容。这使得GPU能够操作受保护的资源（表面、缓冲区、纹理），例如受DRM保护的视频内容。目前仅为EGL实现。
FormatOptions 类型是 QFlags 的 typedef<FormatOption>。它存储 FormatOption 值的 OR 组合。

### `flags FormatOptions`

**作用与语义：**

该枚举包含用于与`QSurfaceFormat`的格式选项。
- `QSurfaceFormat::StereoBuffers`：`0x0001`;用于请求表面格式的立体声缓冲。
- `QSurfaceFormat::DebugContext`：`0x0002`;用于请求带有额外调试信息的调试上下文。
- `QSurfaceFormat::DeprecatedFunctions`：`0x0004`;用于请求将弃用函数包含在 OpenGL 上下文配置文件中。如果未指定，你应获得一个前向兼容的上下文，且没有支持功能，标记为弃用。这需要 OpenGL 3.0 或更高版本。
- `QSurfaceFormat::ResetNotification`：`0x0008`;启用关于 OpenGL 上下文重置的通知。状态随后可通过上下文的 `isValid()` 函数查询。注意，未设置该标志并不保证上下文状态丢失永远不会发生。此外，某些实现可能选择报告上下文丢失，尽管该标志存在。支持动态支持上下文丢失监控的平台，如 Windows 的 WGL，或 Linux/X11（xcb）的 GLX，会监控每次调用 `makeCurrent()` 的状态。详见`isValid()`相关信息。
- `QSurfaceFormat::ProtectedContent`：`0x0010`;允许访问受保护内容。这使得GPU能够操作受保护的资源（表面、缓冲区、纹理），例如受DRM保护的视频内容。目前仅为EGL实现。
FormatOptions 类型是 QFlags 的 typedef<FormatOption>。它存储 FormatOption 值的 OR 组合。

## 6. 深入实践与常见坑

### 生命周期和资源边界

先确认对象是值类型还是 QObject 派生对象，再确定所有权、有效期、拷贝成本和销毁方式。返回的句柄、索引、reply、设备或迭代器可能有独立的有效期，不能只看 C++ 指针是否非空。

### 状态和错误边界

把返回值、状态查询、错误信息和通知信号分开判断。调用成功可能只表示请求被接受，真正完成还要等待状态变化或完成信号；读取数据前先检查对象和结果是否有效。

### 线程边界

如果类型直接或间接参与 QObject、GUI、设备或异步框架，就必须确认线程归属和事件循环；值类型虽然可以复制，也要注意内部指针、共享数据和并发写入。

### 最容易出现的错误

不要忽略构造失败、空返回、默认值和版本限制；不要把异步 API 当同步 API；不要在没有确认所有权和线程的情况下保存指针或跨线程调用。

### 版本和平台

本文档以 Qt 6.11.1 为依据。涉及平台后端、编解码器、数据库驱动、窗口风格、编译器特性或标注了版本号的 API 时，要把版本条件当作使用约束，而不是只看函数是否能补全。

## 7. 使用边界

`QSurfaceFormat` 所属机制类型：Qt 类型机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
