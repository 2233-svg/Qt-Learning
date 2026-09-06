# QSvgGenerator

> Qt 6.11.1 · Qt SVG

## 1. 先建立直觉

**一句话定位：** 这是 Qt SVG 中围绕“SvgGenerator”职责设计的公开 C++ 类型，先从输入、输出、生命周期和它与相邻类型的协作关系入手。

**模块背景：** Qt SVG 提供 SVG 文档读取、渲染和 SVG 图形组件。

### 这是什么

`QSvgGenerator` 是 Qt 类型机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 这个类的行为由它的继承关系、构造参数、公开状态和成员函数协议共同决定。使用时要把创建、配置、核心操作、结果/通知和清理看成一条闭环，而不是孤立调用某个函数。

**适用场景：** 围绕这个类的核心职责建立最小闭环：准备依赖 -> 创建/取得对象 -> 设置必要配置 -> 调用核心 API -> 检查返回值和状态 -> 处理结果/错误 -> 结束时清理。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要忽略构造失败、空返回、默认值和版本限制；不要把异步 API 当同步 API；不要在没有确认所有权和线程的情况下保存指针或跨线程调用。

## 2. 依赖与对象关系

- 头文件：`#include <QSvgGenerator>`
- 继承自：QPaintDevice
- 直接派生类：未在类页中列出

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Svg)
target_link_libraries(mytarget PRIVATE Qt6::Svg)
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

- `(since 6.5) enum class SvgVersion { SvgTiny12, Svg11 }`

### 属性

- `description : QString`
- `fileName : QString`
- `outputDevice : QIODevice*`
- `resolution : int`
- `size : QSize`
- `title : QString`
- `viewBox : QRectF`

### 公有函数

- `QSvgGenerator()`
- `(since 6.5) QSvgGenerator(QSvgGenerator::SvgVersion version)`
- `virtual ~QSvgGenerator()`
- `QString description() const`
- `QString fileName() const`
- `QIODevice * outputDevice() const`
- `int resolution() const`
- `void setDescription(const QString &description)`
- `void setFileName(const QString &fileName)`
- `void setOutputDevice(QIODevice *outputDevice)`
- `void setResolution(int dpi)`
- `void setSize(const QSize &size)`
- `void setTitle(const QString &title)`
- `void setViewBox(const QRect &viewBox)`
- `void setViewBox(const QRectF &viewBox)`
- `QSize size() const`
- `(since 6.5) QSvgGenerator::SvgVersion svgVersion() const`
- `QString title() const`
- `QRect viewBox() const`
- `QRectF viewBoxF() const`

### 重实现的保护函数

- `(since 6.11) virtual void initPainter(QPainter *painter) const override`
- `virtual int metric(QPaintDevice::PaintDeviceMetric metric) const override`
- `virtual QPaintEngine * paintEngine() const override`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `[since 6.5] enum class QSvgGenerator::SvgVersion`

**作用与语义：**

该枚举描述了生成器SVG输出的版本。
- `QSvgGenerator::SvgVersion::SvgTiny12`：`0`;生成的文档遵循 SVG Tiny 1.2 规范。
- `QSvgGenerator::SvgVersion::Svg11`：`1`;生成的文档遵循 SVG 1.1 规范。
这个枚举是在Qt 6.5引入的。

### `description : QString`

**作用与语义：**

此属性保存生成的 SVG 绘图的描述。

**如何使用：** 调用 `description()` 读取当前值；它不会修改应用状态。

### `fileName : QString`

**作用与语义：**

该属性包含生成SVG图纸的目标文件名。

**如何使用：** 调用 `fileName()` 读取当前值；它不会修改应用状态。

### `outputDevice : QIODevice*`

**作用与语义：**

该特性包含生成SVG图纸的输出设备。
如果同时指定输出设备和文件名，输出设备将优先。

**如何使用：** 调用 `outputDevice()` 读取当前值；它不会修改应用状态。

### `resolution : int`

**作用与语义：**

该属性决定了生成输出的分辨率。
分辨率以每英寸点数表示，用于计算SVG图纸的物理尺寸。

**如何使用：** 调用 `resolution()` 读取当前值；它不会修改应用状态。

### `size : QSize`

**作用与语义：**

该属性表示生成的SVG图纸的大小。
默认情况下，该属性设置为`QSize(-1, -1)`，表明生成器不应输出`<svg>`元素的宽度和高度属性。
注意：在发生器上有`QPainter`激活时，无法更改该属性。

**如何使用：** 调用 `size()` 读取当前值；它不会修改应用状态。

### `title : QString`

**作用与语义：**

该属性为生成的SVG图纸标题。

**如何使用：** 调用 `title()` 读取当前值；它不会修改应用状态。

### `viewBox : QRectF`

**作用与语义：**

该属性保留了生成SVG图纸的viewBox。
默认情况下，该属性设置为 `QRect(0, 0, -1, -1)`，表示生成器不应输出 `<svg>` 元素的 viewBox 属性。
注意：在`QPainter`处于激活状态时，无法更改该属性。

**如何使用：** 调用 `viewBox()` 读取当前值；它不会修改应用状态。

### `QSvgGenerator::QSvgGenerator()`

**作用与语义：**

使用 SVG Tiny 1.2 配置文件构建了一个新的生成器。

### `[explicit, since 6.5] QSvgGenerator::QSvgGenerator(QSvgGenerator::SvgVersion version)`

**作用与语义：**

构建了一个使用SVG版本`version`的新生成器。

### `[virtual noexcept] QSvgGenerator::~QSvgGenerator()`

**作用与语义：**

摧毁了发电机。

### `[override virtual protected, since 6.11] void QSvgGenerator::initPainter(QPainter *painter) const`

**作用与语义：**

当 `QPainter` 开始在此 SVG 生成器上绘制时，由 Qt 调用这个受保护钩子来初始化画笔状态。它是 Qt 6.11 起对 `QPaintDevice` 的内部重实现，应用代码不应直接调用；正常用法是 `QPainter painter(&generator)`。

### `[override virtual protected] int QSvgGenerator::metric(QPaintDevice::PaintDeviceMetric metric) const`

**作用与语义：**

重实现自：`QPaintDevice::metric`（QPaintDevice：:P aintDeviceMetric metric） const.

### `[override virtual protected] QPaintEngine *QSvgGenerator::paintEngine() const`

**作用与语义：**

重装：`QPaintDevice::paintEngine()` const.
返回用于渲染图像转换为SVG格式信息的绘图引擎。

### `[since 6.5] QSvgGenerator::SvgVersion QSvgGenerator::svgVersion() const`

**作用与语义：**

返回该生成器生成的SVG文档版本。

### `QRect QSvgGenerator::viewBox() const`

**作用与语义：**

返回 `viewBoxF()`.toRect()。

### `QString description() const`

**作用与语义：**

此属性保存生成的 SVG 绘图的描述。

**如何使用：** 调用 `description()` 读取当前值；它不会修改应用状态。

### `QString fileName() const`

**作用与语义：**

该属性包含生成SVG图纸的目标文件名。

**如何使用：** 调用 `fileName()` 读取当前值；它不会修改应用状态。

### `QIODevice * outputDevice() const`

**作用与语义：**

该特性包含生成SVG图纸的输出设备。
如果同时指定输出设备和文件名，输出设备将优先。

**如何使用：** 调用 `outputDevice()` 读取当前值；它不会修改应用状态。

### `int resolution() const`

**作用与语义：**

该属性决定了生成输出的分辨率。
分辨率以每英寸点数表示，用于计算SVG图纸的物理尺寸。

**如何使用：** 调用 `resolution()` 读取当前值；它不会修改应用状态。

### `void setDescription(const QString &description)`

**作用与语义：**

此属性保存生成的 SVG 绘图的描述。

**如何使用：** 调用 `setDescription(...)` 修改 `description`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setFileName(const QString &fileName)`

**作用与语义：**

该属性包含生成SVG图纸的目标文件名。

**如何使用：** 调用 `setFileName(...)` 修改 `fileName`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setOutputDevice(QIODevice *outputDevice)`

**作用与语义：**

该特性包含生成SVG图纸的输出设备。
如果同时指定输出设备和文件名，输出设备将优先。

**如何使用：** 调用 `setOutputDevice(...)` 修改 `outputDevice`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setResolution(int dpi)`

**作用与语义：**

该属性决定了生成输出的分辨率。
分辨率以每英寸点数表示，用于计算SVG图纸的物理尺寸。

**如何使用：** 调用 `setResolution(...)` 修改 `resolution`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setSize(const QSize &size)`

**作用与语义：**

该属性表示生成的SVG图纸的大小。
默认情况下，该属性设置为`QSize(-1, -1)`，表明生成器不应输出`<svg>`元素的宽度和高度属性。
注意：在发生器上有`QPainter`激活时，无法更改该属性。

**如何使用：** 调用 `setSize(...)` 修改 `size`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setTitle(const QString &title)`

**作用与语义：**

该属性为生成的SVG图纸标题。

**如何使用：** 调用 `setTitle(...)` 修改 `title`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setViewBox(const QRect &viewBox)`

**作用与语义：**

该属性保留了生成SVG图纸的viewBox。
默认情况下，该属性设置为 `QRect(0, 0, -1, -1)`，表示生成器不应输出 `<svg>` 元素的 viewBox 属性。
注意：在`QPainter`处于激活状态时，无法更改该属性。

**如何使用：** 调用 `setViewBox(...)` 修改 `viewBox`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setViewBox(const QRectF &viewBox)`

**作用与语义：**

该属性保留了生成SVG图纸的viewBox。
默认情况下，该属性设置为 `QRect(0, 0, -1, -1)`，表示生成器不应输出 `<svg>` 元素的 viewBox 属性。
注意：在`QPainter`处于激活状态时，无法更改该属性。

**如何使用：** 调用 `setViewBox(...)` 修改 `viewBox`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `QSize size() const`

**作用与语义：**

该属性表示生成的SVG图纸的大小。
默认情况下，该属性设置为`QSize(-1, -1)`，表明生成器不应输出`<svg>`元素的宽度和高度属性。
注意：在发生器上有`QPainter`激活时，无法更改该属性。

**如何使用：** 调用 `size()` 读取当前值；它不会修改应用状态。

### `QString title() const`

**作用与语义：**

该属性为生成的SVG图纸标题。

**如何使用：** 调用 `title()` 读取当前值；它不会修改应用状态。

### `QRectF viewBoxF() const`

**作用与语义：**

该属性保留了生成SVG图纸的viewBox。
默认情况下，该属性设置为 `QRect(0, 0, -1, -1)`，表示生成器不应输出 `<svg>` 元素的 viewBox 属性。
注意：在`QPainter`处于激活状态时，无法更改该属性。

**如何使用：** 调用 `viewBoxF()` 读取当前值；它不会修改应用状态。

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

`QSvgGenerator` 所属机制类型：Qt 类型机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
