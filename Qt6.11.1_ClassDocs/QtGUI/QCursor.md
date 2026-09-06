# QCursor

> Qt 6.11.1 · Qt GUI

## 1. 先建立直觉

**一句话定位：** 这是 GUI 基础类型，常用于绘制、输入、图像、字体或窗口系统集成。

**模块背景：** Qt GUI 负责窗口系统集成、绘制、颜色、字体、图像、输入事件和底层 GUI 资源。

### 这是什么

`QCursor` 是 Qt 类型机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 这个类的行为由它的继承关系、构造参数、公开状态和成员函数协议共同决定。使用时要把创建、配置、核心操作、结果/通知和清理看成一条闭环，而不是孤立调用某个函数。

**适用场景：** 围绕这个类的核心职责建立最小闭环：准备依赖 -> 创建/取得对象 -> 设置必要配置 -> 调用核心 API -> 检查返回值和状态 -> 处理结果/错误 -> 结束时清理。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要忽略构造失败、空返回、默认值和版本限制；不要把异步 API 当同步 API；不要在没有确认所有权和线程的情况下保存指针或跨线程调用。

## 2. 依赖与对象关系

- 头文件：`#include <QCursor>`
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

### 公有函数

- `QCursor()`
- `QCursor(Qt::CursorShape shape)`
- `QCursor(const QPixmap &pixmap, int hotX = -1, int hotY = -1)`
- `QCursor(const QBitmap &bitmap, const QBitmap &mask, int hotX = -1, int hotY = -1)`
- `QCursor(const QCursor &c)`
- `QCursor(QCursor &&other)`
- `~QCursor()`
- `QBitmap bitmap() const`
- `QPoint hotSpot() const`
- `QBitmap mask() const`
- `QPixmap pixmap() const`
- `void setShape(Qt::CursorShape shape)`
- `Qt::CursorShape shape() const`
- `void swap(QCursor &other)`
- `operator QVariant() const`
- `QCursor & operator=(QCursor &&other)`
- `QCursor & operator=(const QCursor &c)`

### 静态公有成员

- `QPoint pos()`
- `QPoint pos(const QScreen *screen)`
- `void setPos(int x, int y)`
- `void setPos(QScreen *screen, int x, int y)`
- `void setPos(const QPoint &p)`
- `void setPos(QScreen *screen, const QPoint &p)`

### 相关非成员函数

- `bool operator!=(const QCursor &lhs, const QCursor &rhs)`
- `QDataStream & operator<<(QDataStream &stream, const QCursor &cursor)`
- `bool operator==(const QCursor &lhs, const QCursor &rhs)`
- `QDataStream & operator>>(QDataStream &stream, QCursor &cursor)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `QCursor::QCursor()`

**作用与语义：**

构建一个默认箭头形状的光标。

### `QCursor::QCursor(Qt::CursorShape shape)`

**作用与语义：**

构造带有指定`shape`的光标。
请参见`Qt::CursorShape`中的形状列表。

### `[explicit] QCursor::QCursor(const QPixmap &pixmap, int hotX = -1, int hotY = -1)`

**作用与语义：**

构建自定义像素地图光标。
`pixmap` 是图像。通常会给它一个遮罩（用 `QPixmap::setMask()` 设置）。`hotX` 和 `hotY` 定义光标的热点。
如果`hotX`为负，则为`pixmap().width()/2`。`hotY`为负，则为`pixmap().height()/2`。
有效的光标大小取决于显示硬件（或底层窗口系统）。我们建议使用32 x 32光标，因为该尺寸在所有平台上都支持。部分平台还支持16 x 16、48 x 48和64 x 64光标。

### `QCursor::QCursor(const QBitmap &bitmap, const QBitmap &mask, int hotX = -1, int hotY = -1)`

**作用与语义：**

构建自定义位图光标。
`bitmap`和`mask`组成了位图。`hotX`和`hotY`定义了光标的热点。
如果`hotX`为负，则设为`bitmap().width()/2`。如果`hotY`为负，则设为`bitmap().height()/2`。
光标`bitmap` （B） 和 `mask` （M） 位的组合如下：
- B=1，M=1，则得到黑色。
- B=0且M=1，得到白色。
- B=0 和 M=0 表示透明。
- B=1 和 M=0 在 Windows 下给出 XOR 结果，在其他平台上则未定义。
使用全局Qt颜色`Qt::color0`绘制0像素，`Qt::color1`绘制1像素。
有效的光标大小取决于显示硬件（或底层窗口系统）。我们建议使用32 x 32光标，因为该尺寸在所有平台上都支持。部分平台还支持16 x 16、48 x 48和64 x 64光标。

### `QCursor::QCursor(const QCursor &c)`

**作用与语义：**

构建光标`c`的副本。

### `[noexcept] QCursor::QCursor(QCursor &&other)`

**作用与语义：**

Move从`other`构造一个光标。从移动后，`other`唯一有效的操作是销毁和（移动和复制）赋值。调用其他成员函数对移动的实例的影响未定义。

### `[noexcept] QCursor::~QCursor()`

**作用与语义：**

摧毁光标。

### `QBitmap QCursor::bitmap() const`

**作用与语义：**

返回光标位图，或者如果是标准光标，则返回空位图。

### `QPoint QCursor::hotSpot() const`

**作用与语义：**

返回光标热点，或者如果是标准光标之一，则返回（0， 0）。

### `QBitmap QCursor::mask() const`

**作用与语义：**

返回光标位图掩码，或者如果是标准光标，则返回空位图。

### `QPixmap QCursor::pixmap() const`

**作用与语义：**

返回光标pixmap。只有当光标是pixmap光标时，这才有效。

### `[static] QPoint QCursor::pos()`

**作用与语义：**

返回主屏幕光标（热点）在全局屏幕坐标中的位置。
你可以调用`QWidget::mapFromGlobal()`将其转换为控件坐标。
注意：位置是从窗口系统查询的。如果鼠标事件是通过其他方式生成的（例如单元测试中的QWindowSystemInterface），这些假鼠标移动不会反映在返回的值中。
注意：在没有窗口系统或光标不可用的平台上，返回的位置基于通过QWindowSystemInterface生成的鼠标移动事件。

### `[static] QPoint QCursor::pos(const QScreen *screen)`

**作用与语义：**

返回`screen`光标（热点）在全局屏幕坐标中的位置。
你可以调用`QWidget::mapFromGlobal()`将其转换为控件坐标。

### `[static] void QCursor::setPos(int x, int y)`

**作用与语义：**

将主屏幕的光标（热点）移动到全局屏幕位置（`x`，`y`）。
你可以调用`QWidget::mapToGlobal()`将控件坐标转换为全局屏幕坐标。

### `[static] void QCursor::setPos(QScreen *screen, int x, int y)`

**作用与语义：**

将`screen`的光标（热点）移动到全局屏幕位置（`x`，`y`）。
你可以调用`QWidget::mapToGlobal()`将控件坐标转换为全局屏幕坐标。
注意：调用该函数会通过窗口系统改变光标位置。窗口系统通常会通过向应用程序窗口发送鼠标事件来响应。这意味着在单元测试以及所有通过 QWindowSystemInterface 注入假鼠标事件的地方应避免使用该函数，因为窗口系统的鼠标状态（例如按钮）可能与应用程序生成事件中的状态不匹配。
注意：在没有窗口系统或没有光标的平台上，这个功能可能无效。

### `[static] void QCursor::setPos(const QPoint &p)`

**作用与语义：**

将光标（热点）移动到全局屏幕位置，位于`p`点。

### `[static] void QCursor::setPos(QScreen *screen, const QPoint &p)`

**作用与语义：**

将光标（热点）移动到`screen`的全局屏幕位置，位于`p`点。

### `void QCursor::setShape(Qt::CursorShape shape)`

**作用与语义：**

将光标设置为`shape`识别的形状。
光标形状列表请参见 `Qt::CursorShape`。

### `Qt::CursorShape QCursor::shape() const`

**作用与语义：**

返回光标形状标识符。

### `[noexcept] void QCursor::swap(QCursor &other)`

**作用与语义：**

将光标与`other`互换。这个操作非常快，从未失败过。

### `QCursor::operator QVariant() const`

**作用与语义：**

返回光标作为`QVariant`。

### `[noexcept] QCursor &QCursor::operator=(QCursor &&other)`

**作用与语义：**

Move-assign `other` 到该`QCursor`实例。

### `QCursor &QCursor::operator=(const QCursor &c)`

**作用与语义：**

将`c`分配到该光标并返回对该光标的引用。

### `[noexcept] bool operator!=(const QCursor &lhs, const QCursor &rhs)`

**作用与语义：**

不等式算子。返回等价的！（`lhs` == `rhs`）。

### `QDataStream &operator<<(QDataStream &stream, const QCursor &cursor)`

**作用与语义：**

写`cursor`给`stream`。

### `[noexcept] bool operator==(const QCursor &lhs, const QCursor &rhs)`

**作用与语义：**

等号算符。如果`lhs`和`rhs`具有相同的`shape()`，且位图光标的 `hotSpot()`相同，且`pixmap()`相同或`bitmap()`和`mask()`相同，则返回 `true`。
注意：在比较位图光标时，该函数只比较位图的缓存键，而非每个像素。

### `QDataStream &operator>>(QDataStream &stream, QCursor &cursor)`

**作用与语义：**

从`stream`上读`cursor`。

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

`QCursor` 所属机制类型：Qt 类型机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
