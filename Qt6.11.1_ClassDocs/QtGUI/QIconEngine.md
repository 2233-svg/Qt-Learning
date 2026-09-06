# QIconEngine

> Qt 6.11.1 · Qt GUI

## 1. 先建立直觉

**一句话定位：** 这是 GUI 基础类型，常用于绘制、输入、图像、字体或窗口系统集成。

**模块背景：** Qt GUI 负责窗口系统集成、绘制、颜色、字体、图像、输入事件和底层 GUI 资源。

### 这是什么

`QIconEngine` 是 Qt 类型机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 这个类的行为由它的继承关系、构造参数、公开状态和成员函数协议共同决定。使用时要把创建、配置、核心操作、结果/通知和清理看成一条闭环，而不是孤立调用某个函数。

**适用场景：** 围绕这个类的核心职责建立最小闭环：准备依赖 -> 创建/取得对象 -> 设置必要配置 -> 调用核心 API -> 检查返回值和状态 -> 处理结果/错误 -> 结束时清理。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要忽略构造失败、空返回、默认值和版本限制；不要把异步 API 当同步 API；不要在没有确认所有权和线程的情况下保存指针或跨线程调用。

## 2. 依赖与对象关系

- 头文件：`#include <QIconEngine>`
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

- `struct ScaledPixmapArgument`
- `enum IconEngineHook { IsNullHook, ScaledPixmapHook }`

### 公有函数

- `QIconEngine()`
- `virtual ~QIconEngine()`
- `virtual QSize actualSize(const QSize &size, QIcon::Mode mode, QIcon::State state)`
- `virtual void addFile(const QString &fileName, const QSize &size, QIcon::Mode mode, QIcon::State state)`
- `virtual void addPixmap(const QPixmap &pixmap, QIcon::Mode mode, QIcon::State state)`
- `virtual QList<QSize> availableSizes(QIcon::Mode mode = QIcon::Normal, QIcon::State state = QIcon::Off)`
- `virtual QIconEngine * clone() const = 0`
- `virtual QString iconName()`
- `virtual bool isNull()`
- `virtual QString key() const`
- `virtual void paint(QPainter *painter, const QRect &rect, QIcon::Mode mode, QIcon::State state) = 0`
- `virtual QPixmap pixmap(const QSize &size, QIcon::Mode mode, QIcon::State state)`
- `virtual bool read(QDataStream &in)`
- `virtual QPixmap scaledPixmap(const QSize &size, QIcon::Mode mode, QIcon::State state, qreal scale)`
- `virtual void virtual_hook(int id, void *data)`
- `virtual bool write(QDataStream &out) const`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `enum QIconEngine::IconEngineHook`

**作用与语义：**

这些枚举值用于`virtual_hook()`允许对图标引擎进行额外查询而不破坏二进制兼容性。
- `QIconEngine::IsNullHook`：`3`;允许查询该引擎是否代表空图标。`virtual_hook()`的`data`参数是一个指向布尔的指针，如果图标为空，则可设为真。该枚举值是在Qt 5.7中添加的。
- `QIconEngine::ScaledPixmapHook`：`4`;提供一种根据给定比例（通常等于设备像素比）缩放的像素映射的方法。`virtual_hook()`函数的`data`参数是一个包含输入和输出参数的`ScaledPixmapArgument`指针。该枚举值是在Qt 5.9中添加的。

### `QIconEngine::QIconEngine()`

**作用与语义：**

构建图标引擎。

### `[virtual noexcept] QIconEngine::~QIconEngine()`

**作用与语义：**

摧毁图标引擎。

### `[virtual] QSize QIconEngine::actualSize(const QSize &size, QIcon::Mode mode, QIcon::State state)`

**作用与语义：**

返回引擎为请求的`size`、`mode`和`state`提供的实际图标大小。默认实现返回给定的`size`。
返回的尺寸以设备无关像素为单位（这对高DPI像素映射很重要）。

### `[virtual] void QIconEngine::addFile(const QString &fileName, const QSize &size, QIcon::Mode mode, QIcon::State state)`

**作用与语义：**

由`QIcon::addFile()`调用。从文件中添加一个带有指定`fileName`、`size`、`mode`和`state`的专用像素映射。默认基于像素地图的引擎会存储所有提供的文件名，并且如果像素地图大小与请求图标大小相匹配，它会按需加载像素地图，而不是使用缩放后的像素映射。实现可缩放矢量格式的自定义图标引擎可以自由忽略任何额外的文件。

### `[virtual] void QIconEngine::addPixmap(const QPixmap &pixmap, QIcon::Mode mode, QIcon::State state)`

**作用与语义：**

由`QIcon::addPixmap()`调用。为给定的 `mode` 和 `state` 添加了专用的`pixmap`。默认基于像素地图的引擎存储所有提供的像素地图，如果像素地图的大小与请求的图标大小相匹配，它会使用像素地图代替缩放像素地图。实现可扩展矢量格式的自定义图标引擎可以自由忽略任何额外的像素地图。

### `[virtual] QList<QSize> QIconEngine::availableSizes(QIcon::Mode mode = QIcon::Normal, QIcon::State state = QIcon::Off)`

**作用与语义：**

返回引擎中针对特定`mode`和`state`包含的所有图像尺寸。

### `[pure virtual] QIconEngine *QIconEngine::clone() const`

**作用与语义：**

重新实现此方法以返回该图标引擎的克隆。

### `[virtual] QString QIconEngine::iconName()`

**作用与语义：**

如果有，返回创建引擎时使用的名称。

### `[virtual] bool QIconEngine::isNull()`

**作用与语义：**

如果该图标引擎代表空`QIcon`，则返回为真。
注意：如果图标引擎不重新实现此功能，实际工作由`virtual_hook()`方法完成，因此该方法依赖图标引擎支持，可能不适用于所有图标引擎。

### `[virtual] QString QIconEngine::key() const`

**作用与语义：**

返回一个识别该图标引擎的密钥。

### `[pure virtual] void QIconEngine::paint(QPainter *painter, const QRect &rect, QIcon::Mode mode, QIcon::State state)`

**作用与语义：**

用给定的`painter`给图标涂上所需的`mode`，并`state`到矩形`rect`。

### `[virtual] QPixmap QIconEngine::pixmap(const QSize &size, QIcon::Mode mode, QIcon::State state)`

**作用与语义：**

返回图标为带有所需 `size`、`mode` 和 `state` 的像素映射。默认实现会创建一个新的像素映射并调用 `paint()` 来填充它。

### `[virtual] bool QIconEngine::read(QDataStream &in)`

**作用与语义：**

从`QDataStream` `in`读取图标引擎内容。如果内容被读取，则返回为真;否则返回`false`。
`QIconEngine` 的默认实现总是返回 false。

### `[virtual] QPixmap QIconEngine::scaledPixmap(const QSize &size, QIcon::Mode mode, QIcon::State state, qreal scale)`

**作用与语义：**

返回给定`size`、`mode`、`state`和`scale`的像素映射。
`scale`参数通常等于显示器的设备像素比。尺寸以设备无关像素表示。
注意：如果图标引擎不重新实现该功能，实际工作由`virtual_hook()`方法完成，因此该方法依赖图标引擎支持，可能不适用于所有图标引擎。
注意：有些引擎可能会将`scale`铸造为整数。

### `[virtual] void QIconEngine::virtual_hook(int id, void *data)`

**作用与语义：**

另一种方法，允许扩展`QIconEngine`而不添加新的虚拟方法（且不破坏二进制兼容性）。`data`的实际动作和格式依赖于`id`参数，而该参数实际上是枚举`IconEngineHook`常数。

### `[virtual] bool QIconEngine::write(QDataStream &out) const`

**作用与语义：**

将该引擎的内容写入`QDataStream` `out`。如果内容写入，返回`true`;否则返回`false`。
`QIconEngine` 的默认实现总是返回 false。

### `struct ScaledPixmapArgument`

**作用与语义：**

当`id`参数`QIconEngine::ScaledPixmapHook`时，该结构表示`virtual_hook()`函数的参数。
该结构体为通过`QIcon::fromTheme()`创建的图标提供了一种方式，能够返回为当前设备像素比例设计的像素映射。此类图标的缩放可以通过相应`index.theme`文件中的缩放目录键来指定。
通过其他方法创建的图标会返回与调用`pixmap()`相同的结果，并且继续受益于 Qt 的高 DPI 语法@nx。

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

`QIconEngine` 所属机制类型：Qt 类型机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
