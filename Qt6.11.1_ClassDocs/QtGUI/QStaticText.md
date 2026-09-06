# QStaticText

> Qt 6.11.1 · Qt GUI

## 1. 先建立直觉

**一句话定位：** 这是 GUI 基础类型，常用于绘制、输入、图像、字体或窗口系统集成。

**模块背景：** Qt GUI 负责窗口系统集成、绘制、颜色、字体、图像、输入事件和底层 GUI 资源。

### 这是什么

`QStaticText` 是 Qt 类型机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 这个类的行为由它的继承关系、构造参数、公开状态和成员函数协议共同决定。使用时要把创建、配置、核心操作、结果/通知和清理看成一条闭环，而不是孤立调用某个函数。

**适用场景：** 围绕这个类的核心职责建立最小闭环：准备依赖 -> 创建/取得对象 -> 设置必要配置 -> 调用核心 API -> 检查返回值和状态 -> 处理结果/错误 -> 结束时清理。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要忽略构造失败、空返回、默认值和版本限制；不要把异步 API 当同步 API；不要在没有确认所有权和线程的情况下保存指针或跨线程调用。

## 2. 依赖与对象关系

- 头文件：`#include <QStaticText>`
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

- `enum PerformanceHint { ModerateCaching, AggressiveCaching }`

### 公有函数

- `QStaticText()`
- `QStaticText(const QString &text)`
- `QStaticText(const QStaticText &other)`
- `~QStaticText()`
- `QStaticText::PerformanceHint performanceHint() const`
- `void prepare(const QTransform &matrix = QTransform(), const QFont &font = QFont())`
- `void setPerformanceHint(QStaticText::PerformanceHint performanceHint)`
- `void setText(const QString &text)`
- `void setTextFormat(Qt::TextFormat textFormat)`
- `void setTextOption(const QTextOption &textOption)`
- `void setTextWidth(qreal textWidth)`
- `QSizeF size() const`
- `void swap(QStaticText &other)`
- `QString text() const`
- `Qt::TextFormat textFormat() const`
- `QTextOption textOption() const`
- `qreal textWidth() const`
- `bool operator!=(const QStaticText &other) const`
- `QStaticText & operator=(const QStaticText &other)`
- `bool operator==(const QStaticText &other) const`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `enum QStaticText::PerformanceHint`

**作用与语义：**

这个枚举表示可以在 `QStaticText` 上设置的不同性能提示。这些提示可以用来指示 `QStaticText` 如果可能的话应使用额外的缓存，以提高性能，但会占用更多内存。特别是，在 `QStaticText` 上设置 AggressiveCaching 性能提示，将在使用 OpenGL 图形系统或绘制到 `QOpenGLWidget` 时提高性能。
- `QStaticText::ModerateCaching`: `0`; 进行基本缓存，以在低内存成本下获得高性能。
- `QStaticText::AggressiveCaching`: `1`; 在可用时使用额外缓存。这可能会以更高的内存成本提高性能。

### `QStaticText::QStaticText()`

**作用与语义：**

构造一个空的QStaticText。

### `[explicit] QStaticText::QStaticText(const QString &text)`

**作用与语义：**

构造一个带有给定`text`的QStaticText对象。

### `QStaticText::QStaticText(const QStaticText &other)`

**作用与语义：**

构建一个QStaticText对象，该对象是`other`的副本。

### `[noexcept] QStaticText::~QStaticText()`

**作用与语义：**

毁掉`QStaticText`。

### `QStaticText::PerformanceHint QStaticText::performanceHint() const`

**作用与语义：**

返回`QStaticText`设置的性能提示。

### `void QStaticText::prepare(const QTransform &matrix = QTransform(), const QFont &font = QFont())`

**作用与语义：**

准备`QStaticText`对象以给定的 `matrix` 和给定的 `font` 来绘制，以避免实际 drawStaticText() 调用时产生的开销。
当调用 drawStaticText() 时，如果`QStaticText`对象的某部分自上次绘制以来发生变化，`QStaticText`的布局会被重新计算。如果画家的字体与`QStaticText`上次绘制时不同，或者在除 OpenGL2 引擎外的其他绘图引擎中，画家的矩阵自静态文本上次绘制后发生了变化，也会重新计算。
为了避免第一次绘制`QStaticText`时创建布局的额外负担，你可以使用prepare()函数，输入你预期绘制文本时使用的 `matrix`和`font`。

### `void QStaticText::setPerformanceHint(QStaticText::PerformanceHint performanceHint)`

**作用与语义：**

根据提供的`performanceHint`设定`QStaticText`的性能提示。`performanceHint`用于自定义内部缓存的程度，以提升性能。
默认是`QStaticText::ModerateCaching`。
注意：此功能会导致文本布局需要重新计算。

### `void QStaticText::setText(const QString &text)`

**作用与语义：**

将`QStaticText`文本设置为`text`。
注意：此功能会导致文本布局需要重新计算。

### `void QStaticText::setTextFormat(Qt::TextFormat textFormat)`

**作用与语义：**

将`QStaticText`的文本格式设置为`textFormat`。如果`textFormat`设置为`Qt::AutoText`（默认），文本格式将尝试通过函数 `Qt::mightBeRichText()`来确定。如果文本格式是`Qt::PlainText`，则文本将按原样显示;而如果格式`Qt::RichText`，则会被解释为 HTML。`QStaticText` 支持修改文本字体、颜色或布局的 HTML 标签。
注意：此功能会导致文本布局需要重新计算。

### `void QStaticText::setTextOption(const QTextOption &textOption)`

**作用与语义：**

将控制布局过程的文本选项结构设置为给定的`textOption`。

### `void QStaticText::setTextWidth(qreal textWidth)`

**作用与语义：**

设置该`QStaticText`的首选宽度。如果文本宽度大于指定宽度，则会被拆分成多行并垂直增长。如果无法分割成多行，则会大于指定`textWidth`。
将首选文本宽度设置为负数，文本将被无限限制。
用`size()`来获取文本的实际大小。
注意：此功能会导致文本布局需要重新计算。

### `QSizeF QStaticText::size() const`

**作用与语义：**

返回该`QStaticText`的边界矩形体大小。

### `[noexcept] void QStaticText::swap(QStaticText &other)`

**作用与语义：**

将静态文本实例与`other`交换。该操作非常快且从未失败。

### `QString QStaticText::text() const`

**作用与语义：**

返回`QStaticText`文本。

### `Qt::TextFormat QStaticText::textFormat() const`

**作用与语义：**

返回`QStaticText`的文本格式。

### `QTextOption QStaticText::textOption() const`

**作用与语义：**

返回当前用于控制布局过程的文本选项。

### `qreal QStaticText::textWidth() const`

**作用与语义：**

返回该`QStaticText`的首选宽度。

### `bool QStaticText::operator!=(const QStaticText &other) const`

**作用与语义：**

将 `other` 与此 `QStaticText` 进行比较。如果文本、字体或最大尺寸不同，则返回 `true`。

### `QStaticText &QStaticText::operator=(const QStaticText &other)`

**作用与语义：**

分配`other`到这个`QStaticText`。

### `bool QStaticText::operator==(const QStaticText &other) const`

**作用与语义：**

将 `other` 与此 `QStaticText` 进行比较。如果文本、字体和文本宽度相等，则返回 `true`。

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

`QStaticText` 所属机制类型：Qt 类型机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
