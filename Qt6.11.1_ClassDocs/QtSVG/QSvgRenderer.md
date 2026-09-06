# QSvgRenderer

> Qt 6.11.1 · Qt SVG

## 1. 先建立直觉

**一句话定位：** `QSvgRenderer` 是 Qt 对象机制 中的类型，负责把这一机制中的数据、状态或资源交给其他 Qt 对象使用。

**模块背景：** Qt SVG 提供 SVG 文档读取、渲染和 SVG 图形组件。

### 这是什么

`QSvgRenderer` 是 Qt 对象机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 这类对象通常参与 Qt 元对象系统。类声明中的 `Q_OBJECT`、信号、槽、属性和可调用函数会被元对象注册；Qt 可以据此完成类型查询、信号槽连接、属性访问和事件分发。对象还带有线程归属，事件和 queued connection 会投递到对象所属线程的事件循环。

**适用场景：** 使用这类对象时，先创建并确定 parent/线程归属，再配置属性和连接信号，最后调用产生异步或状态变化的函数。耗时工作不要塞进 GUI 线程的槽函数；退出时先停止异步操作，再销毁对象。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不能复制 QObject；不能把属于其他线程的对象当作普通值直接操作；不能在信号回调中阻塞事件循环；`deleteLater()` 依赖事件循环，线程即将退出时要安排好退出和清理顺序。

## 2. 依赖与对象关系

- 头文件：`#include <QSvgRenderer>`
- 继承自：QObject
- 直接派生类：未在类页中列出

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Svg)
target_link_libraries(mytarget PRIVATE Qt6::Svg)
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

### 属性

- `(since 6.7) animationEnabled : bool`
- `aspectRatioMode : Qt::AspectRatioMode`
- `framesPerSecond : int`
- `(since 6.7) options : QtSvg::Options`
- `viewBox : QRectF`

### 公有函数

- `QSvgRenderer(QObject *parent = nullptr)`
- `QSvgRenderer(QXmlStreamReader *contents, QObject *parent = nullptr)`
- `QSvgRenderer(const QByteArray &contents, QObject *parent = nullptr)`
- `QSvgRenderer(const QString &filename, QObject *parent = nullptr)`
- `virtual ~QSvgRenderer()`
- `bool animated() const`
- `Qt::AspectRatioMode aspectRatioMode() const`
- `QRectF boundsOnElement(const QString &id) const`
- `QSize defaultSize() const`
- `bool elementExists(const QString &id) const`
- `int framesPerSecond() const`
- `bool isAnimationEnabled() const`
- `bool isValid() const`
- `QtSvg::Options options() const`
- `void setAnimationEnabled(bool enable)`
- `void setAspectRatioMode(Qt::AspectRatioMode mode)`
- `void setFramesPerSecond(int num)`
- `void setOptions(QtSvg::Options flags)`
- `void setViewBox(const QRect &viewbox)`
- `void setViewBox(const QRectF &viewbox)`
- `QTransform transformForElement(const QString &id) const`
- `QRect viewBox() const`
- `QRectF viewBoxF() const`

### 公有槽函数

- `bool load(QXmlStreamReader *contents)`
- `bool load(const QByteArray &contents)`
- `bool load(const QString &filename)`
- `void render(QPainter *painter)`
- `void render(QPainter *painter, const QRectF &bounds)`
- `void render(QPainter *painter, const QString &elementId, const QRectF &bounds = QRectF())`

### 信号

- `void repaintNeeded()`

### 静态公有成员

- `(since 6.8) void setDefaultOptions(QtSvg::Options flags)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `[since 6.7] animationEnabled : bool`

**作用与语义：**

该属性决定了如果 SVG 被动画化，动画是否应该运行。
将属性设置为false会停止动画计时器。将属性设置为true则动画计时器启动，前提是SVG包含动画元素。
如果SVG没有动画，该属性将无效。否则，属性默认为true。

**如何使用：** 调用 `animationEnabled()` 读取当前值；它不会修改应用状态。

### `aspectRatioMode : Qt::AspectRatioMode`

**作用与语义：**

渲染如何遵循SVG视框的宽高比。
被接受的模式有：
- `Qt::IgnoreAspectRatio`（默认）：忽略宽高比，渲染拉伸至目标边界。
- `Qt::KeepAspectRatio`：渲染在目标范围内居中并尽可能放大，同时保持宽高比。

**如何使用：** 调用 `aspectRatioMode()` 读取当前值；它不会修改应用状态。

### `framesPerSecond : int`

**作用与语义：**

此属性保存每秒显示的帧数。
如果当前文档不是动画，则每秒帧数为 0。

**如何使用：** 调用 `framesPerSecond()` 读取当前值；它不会修改应用状态。

### `[since 6.7] options : QtSvg::Options`

**作用与语义：**

该属性包含一组`QtSvg::Option`标志，可用于启用或禁用 SVG 文件解析和渲染的各种功能。
要生效，执行`before` `load()`必须设置该属性。注意，构建器在构建过程中会执行加载，而这些构造器会在构建过程中进行加载。

**如何使用：** 调用 `options()` 读取当前值；它不会修改应用状态。

### `viewBox : QRectF`

**作用与语义：**

该属性包含了指定文档可见区域的矩形，该区域在逻辑坐标中。

**如何使用：** 调用 `viewBox()` 读取当前值；它不会修改应用状态。

### `QSvgRenderer::QSvgRenderer(QObject *parent = nullptr)`

**作用与语义：**

用给定的`parent`构建一个新的渲染器。

### `QSvgRenderer::QSvgRenderer(QXmlStreamReader *contents, QObject *parent = nullptr)`

**作用与语义：**

用给定的 `parent` 构建一个新的渲染器，并使用 `contents` 指定的流读取器加载 SVG 数据。

### `QSvgRenderer::QSvgRenderer(const QByteArray &contents, QObject *parent = nullptr)`

**作用与语义：**

构建一个新的渲染器，使用给定的`parent`，并从`contents`指定的字节数组加载SVG数据。

### `QSvgRenderer::QSvgRenderer(const QString &filename, QObject *parent = nullptr)`

**作用与语义：**

用给定的`parent`构建一个新的渲染器，并用指定`filename`加载SVG文件的内容。

### `[virtual noexcept] QSvgRenderer::~QSvgRenderer()`

**作用与语义：**

会破坏渲染器。

### `bool QSvgRenderer::animated() const`

**作用与语义：**

如果当前文档包含动画元素，则返回真;否则返回假。

### `QRectF QSvgRenderer::boundsOnElement(const QString &id) const`

**作用与语义：**

返回具有给定`id`的有界矩形。父元素的变换矩阵不影响元素的边界。

### `QSize QSvgRenderer::defaultSize() const`

**作用与语义：**

返回文档内容的默认大小。

### `bool QSvgRenderer::elementExists(const QString &id) const`

**作用与语义：**

如果当前解析的SVG文件中存在该`id`元素且是可渲染元素，则返回为true。
注意：该方法仅对可渲染的元素返回为真。这意味着被视为填充/笔画风格属性的元素，例如带有“id”属性的径向渐变，也不会被该方法找到。

### `bool QSvgRenderer::isValid() const`

**作用与语义：**

如果存在有效的当前文档，则返回真;否则返回假。

### `[slot] bool QSvgRenderer::load(QXmlStreamReader *contents)`

**作用与语义：**

加载指定的SVG以`contents`形式，如果内容解析成功，则返回true;否则返回false。
读卡器将从当前位置使用。如果`contents` `null`，行为则未定义。
注意：该槽位已超载。连接该槽位：


使用 qOverload 连接：
connect（sender， &SenderClass：：signal，。
svgRenderer， qOverload（&QSvgRenderer：：load））;

或者用lambda作为包装器：
connect（sender， &SenderClass：：signal，。
svgRenderer， [receiver = svgRenderer]（QXmlStreamReader *contents） { receiver->load（contents）; }）;


更多示例和方法，请参见连接超载槽位。

### `[slot] bool QSvgRenderer::load(const QByteArray &contents)`

**作用与语义：**

加载指定的SVG格式`contents`，如果内容解析成功，则返回true;否则返回false。
注意：该槽位已超载。连接该槽位：


使用 qOverload 连接：
connect（sender， &SenderClass：：signal，。
svgRenderer， qOverload（&QSvgRenderer：：load））;

或者用lambda作为包装器：
connect（sender， &SenderClass：：signal，。
svgRenderer， [receiver = svgRenderer]（const QByteArray &contents） { receiver->load（contents）; }）;


更多示例和方法，请参见连接超载槽位。

### `[slot] bool QSvgRenderer::load(const QString &filename)`

**作用与语义：**

加载`filename`指定的SVG文件，如果内容解析成功，则返回true;否则返回false。
注意：该槽位已超载。连接该槽位：


使用 qOverload 连接：
connect（sender， &SenderClass：：signal，。
svgRenderer， qOverload（&QSvgRenderer：：load））;

或者用lambda作为包装器：
connect（sender， &SenderClass：：signal，。
svgRenderer， [receiver = svgRenderer]（const QString &filename） { receiver->load（filename）; }）;


更多示例和方法，请参见连接超载槽位。

### `[slot] void QSvgRenderer::render(QPainter *painter)`

**作用与语义：**

使用给定的 `painter` 渲染当前文档或动画文档的当前帧。
注意：该槽位已超载。连接该槽位：


使用 qOverload 连接：
connect（sender， &SenderClass：：signal，。
svgRenderer， qOverload（&QSvgRenderer：：render））;

或者用lambda作为包装器：
connect（sender， &SenderClass：：signal，。
svgRenderer， [receiver = svgRenderer]（QPainter *painter） { receiver->render（painter）; }）;


更多示例和方法，请参见连接超载槽位。

### `[slot] void QSvgRenderer::render(QPainter *painter, const QRectF &bounds)`

**作用与语义：**

在画家中使用指定`bounds`的指定`painter`渲染当前文档或当前画面。如果`bounds`未空，输出将被缩放以填充，忽略SVG暗示的任何宽高比。
注意：该槽位已超载。连接该槽位：


使用 qOverload 连接：
connect（sender， &SenderClass：：signal，。
svgRenderer， qOverload（&QSvgRenderer：：render））;

或者用lambda作为包装器：
connect（sender， &SenderClass：：signal，。
svgRenderer， [receiver = svgRenderer]（QPainter *painter， const QRectF &bounds） { receiver->render（painter， bounds）; }）;


更多示例和方法，请参见连接超载槽位。

### `[slot] void QSvgRenderer::render(QPainter *painter, const QString &elementId, const QRectF &bounds = QRectF())`

**作用与语义：**

用指定`painter`在指定`bounds`上渲染给定元素并`elementId`。如果未指定边界矩形，SVG元素会映射到整个绘图设备。
注意：该槽位已超载。连接该槽位：


使用 qOverload 连接：
connect（sender， &SenderClass：：signal，。
svgRenderer， qOverload（&QSvgRenderer：：render））;

或者用lambda作为包装器：
connect（sender， &SenderClass：：signal，。
svgRenderer， [receiver = svgRenderer]（QPainter *painter， const QString &elementId， const QRectF &bounds） { receiver->render（painter， elementId， bounds）; }）;


更多示例和方法，请参见连接超载槽位。

### `[signal] void QSvgRenderer::repaintNeeded()`

**作用与语义：**

每当文档渲染需要更新时，通常用于动画效果，都会发出该信号。

### `[static, since 6.8] void QSvgRenderer::setDefaultOptions(QtSvg::Options flags)`

**作用与语义：**

设置渲染器创建时的选项标志为`flags`。默认情况下，不会设置任何标志。
运行时，该变量可以被 QT_SVG_DEFAULT_OPTIONS 环境变量覆盖。

### `QTransform QSvgRenderer::transformForElement(const QString &id) const`

**作用与语义：**

返回具有给定`id`的元素的变换矩阵。矩阵是元素父元变换的乘积。不包含元素本身的变换。
要在逻辑坐标下找到元素的边界矩形，可以对返回`boundsOnElement()`矩形的矩阵进行应用。

### `QRect QSvgRenderer::viewBox() const`

**作用与语义：**

返回 `viewBoxF()`.toRect()。

### `Qt::AspectRatioMode aspectRatioMode() const`

**作用与语义：**

渲染如何遵循SVG视框的宽高比。
被接受的模式有：
- `Qt::IgnoreAspectRatio`（默认）：忽略宽高比，渲染拉伸至目标边界。
- `Qt::KeepAspectRatio`：渲染在目标范围内居中并尽可能放大，同时保持宽高比。

**如何使用：** 调用 `aspectRatioMode()` 读取当前值；它不会修改应用状态。

### `int framesPerSecond() const`

**作用与语义：**

此属性保存每秒显示的帧数。
如果当前文档不是动画，则每秒帧数为 0。

**如何使用：** 调用 `framesPerSecond()` 读取当前值；它不会修改应用状态。

### `bool isAnimationEnabled() const`

**作用与语义：**

该属性决定了如果 SVG 被动画化，动画是否应该运行。
将属性设置为false会停止动画计时器。将属性设置为true则动画计时器启动，前提是SVG包含动画元素。
如果SVG没有动画，该属性将无效。否则，属性默认为true。

**如何使用：** 调用 `isAnimationEnabled()` 读取当前值；它不会修改应用状态。

### `QtSvg::Options options() const`

**作用与语义：**

该属性包含一组`QtSvg::Option`标志，可用于启用或禁用 SVG 文件解析和渲染的各种功能。
要生效，执行`before` `load()`必须设置该属性。注意，构建器在构建过程中会执行加载，而这些构造器会在构建过程中进行加载。

**如何使用：** 调用 `options()` 读取当前值；它不会修改应用状态。

### `void setAnimationEnabled(bool enable)`

**作用与语义：**

该属性决定了如果 SVG 被动画化，动画是否应该运行。
将属性设置为false会停止动画计时器。将属性设置为true则动画计时器启动，前提是SVG包含动画元素。
如果SVG没有动画，该属性将无效。否则，属性默认为true。

**如何使用：** 调用 `setAnimationEnabled(...)` 修改 `animationEnabled`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setAspectRatioMode(Qt::AspectRatioMode mode)`

**作用与语义：**

渲染如何遵循SVG视框的宽高比。
被接受的模式有：
- `Qt::IgnoreAspectRatio`（默认）：忽略宽高比，渲染拉伸至目标边界。
- `Qt::KeepAspectRatio`：渲染在目标范围内居中并尽可能放大，同时保持宽高比。

**如何使用：** 调用 `setAspectRatioMode(...)` 修改 `aspectRatioMode`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setFramesPerSecond(int num)`

**作用与语义：**

此属性保存每秒显示的帧数。
如果当前文档不是动画，则每秒帧数为 0。

**如何使用：** 调用 `setFramesPerSecond(...)` 修改 `framesPerSecond`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setOptions(QtSvg::Options flags)`

**作用与语义：**

该属性包含一组`QtSvg::Option`标志，可用于启用或禁用 SVG 文件解析和渲染的各种功能。
要生效，执行`before` `load()`必须设置该属性。注意，构建器在构建过程中会执行加载，而这些构造器会在构建过程中进行加载。

**如何使用：** 调用 `setOptions(...)` 修改 `options`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setViewBox(const QRect &viewbox)`

**作用与语义：**

该属性包含了指定文档可见区域的矩形，该区域在逻辑坐标中。

**如何使用：** 调用 `setViewBox(...)` 修改 `viewBox`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setViewBox(const QRectF &viewbox)`

**作用与语义：**

该属性包含了指定文档可见区域的矩形，该区域在逻辑坐标中。

**如何使用：** 调用 `setViewBox(...)` 修改 `viewBox`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `QRectF viewBoxF() const`

**作用与语义：**

该属性包含了指定文档可见区域的矩形，该区域在逻辑坐标中。

**如何使用：** 调用 `viewBoxF()` 读取当前值；它不会修改应用状态。

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

`QSvgRenderer` 所属机制类型：Qt 对象机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
