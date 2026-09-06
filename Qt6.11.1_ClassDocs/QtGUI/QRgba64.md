# QRgba64

> Qt 6.11.1 · Qt GUI

## 1. 先建立直觉

**一句话定位：** 这是 GUI 基础类型，常用于绘制、输入、图像、字体或窗口系统集成。

**模块背景：** Qt GUI 负责窗口系统集成、绘制、颜色、字体、图像、输入事件和底层 GUI 资源。

### 这是什么

`QRgba64` 是 Qt 类型机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 这个类的行为由它的继承关系、构造参数、公开状态和成员函数协议共同决定。使用时要把创建、配置、核心操作、结果/通知和清理看成一条闭环，而不是孤立调用某个函数。

**适用场景：** 围绕这个类的核心职责建立最小闭环：准备依赖 -> 创建/取得对象 -> 设置必要配置 -> 调用核心 API -> 检查返回值和状态 -> 处理结果/错误 -> 结束时清理。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要忽略构造失败、空返回、默认值和版本限制；不要把异步 API 当同步 API；不要在没有确认所有权和线程的情况下保存指针或跨线程调用。

## 2. 依赖与对象关系

- 头文件：`#include <QRgba64>`
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

- `quint8 alpha8() const`
- `quint16 alpha() const`
- `quint8 blue8() const`
- `quint16 blue() const`
- `quint8 green8() const`
- `quint16 green() const`
- `bool isOpaque() const`
- `bool isTransparent() const`
- `QRgba64 premultiplied() const`
- `quint8 red8() const`
- `quint16 red() const`
- `void setAlpha(quint16 alpha)`
- `void setBlue(quint16 blue)`
- `void setGreen(quint16 green)`
- `void setRed(quint16 red)`
- `uint toArgb32() const`
- `ushort toRgb16() const`
- `QRgba64 unpremultiplied() const`
- `operator quint64() const`
- `QRgba64 & operator=(quint64 rgba)`

### 静态公有成员

- `QRgba64 fromArgb32(uint rgb)`
- `QRgba64 fromRgba64(quint64 c)`
- `QRgba64 fromRgba64(quint16 r, quint16 g, quint16 b, quint16 a)`
- `QRgba64 fromRgba(quint8 red, quint8 green, quint8 blue, quint8 alpha)`

### 相关非成员函数

- `(since 6.11.1) size_t qHash(QRgba64 key, size_t seed = 0)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `[constexpr] quint8 QRgba64::alpha8() const`

**作用与语义：**

将alpha通道返回为8位。

### `[constexpr] quint16 QRgba64::alpha() const`

**作用与语义：**

返回16位alpha通道。

### `[constexpr] quint8 QRgba64::blue8() const`

**作用与语义：**

将蓝色分量返回为8位。

### `[constexpr] quint16 QRgba64::blue() const`

**作用与语义：**

返回16位蓝色分量。

### `[static constexpr] QRgba64 QRgba64::fromArgb32(uint rgb)`

**作用与语义：**

从32位ARGB值`rgb`构造`QRgba64`值。

### `[static constexpr] QRgba64 QRgba64::fromRgba64(quint64 c)`

**作用与语义：**

`c`以`QRgba64`结构体的形式返回。

### `[static constexpr] QRgba64 QRgba64::fromRgba64(quint16 r, quint16 g, quint16 b, quint16 a)`

**作用与语义：**

返回`QRgba64`四胞胎（`r`、`g`、`b`、`a`）。

### `[static constexpr] QRgba64 QRgba64::fromRgba(quint8 red, quint8 green, quint8 blue, quint8 alpha)`

**作用与语义：**

从四个8位色彩通道`red`、`green`、`blue`和`alpha`构建`QRgba64`值。

### `[constexpr] quint8 QRgba64::green8() const`

**作用与语义：**

返回绿色分量为8位。

### `[constexpr] quint16 QRgba64::green() const`

**作用与语义：**

返回16位绿色分量。

### `[constexpr] bool QRgba64::isOpaque() const`

**作用与语义：**

返回颜色是否完全不透明。

### `[constexpr] bool QRgba64::isTransparent() const`

**作用与语义：**

返回颜色是否透明。

### `[constexpr] QRgba64 QRgba64::premultiplied() const`

**作用与语义：**

返回带有预乘数的颜色。

### `[constexpr] quint8 QRgba64::red8() const`

**作用与语义：**

红色分量以8位返回。

### `[constexpr] quint16 QRgba64::red() const`

**作用与语义：**

返回16位红色分量。

### `void QRgba64::setAlpha(quint16 alpha)`

**作用与语义：**

将该颜色的α值设为`alpha`。

### `void QRgba64::setBlue(quint16 blue)`

**作用与语义：**

将该颜色的蓝色分量设置为`blue`。

### `void QRgba64::setGreen(quint16 green)`

**作用与语义：**

将该颜色的绿色分量设置为`green`。

### `void QRgba64::setRed(quint16 red)`

**作用与语义：**

将该颜色的红色分量设置为`red`。

### `[constexpr] uint QRgba64::toArgb32() const`

**作用与语义：**

返回颜色的 32 位 ARGB 值。

### `[constexpr] ushort QRgba64::toRgb16() const`

**作用与语义：**

返回颜色的 16 位 RGB 值。

### `[constexpr] QRgba64 QRgba64::unpremultiplied() const`

**作用与语义：**

返回带有未预代乘的alpha的颜色。

### `[constexpr] QRgba64::operator quint64() const`

**作用与语义：**

返回颜色的 64 位无符号整数值。

### `[noexcept] QRgba64 &QRgba64::operator=(quint64 rgba)`

**作用与语义：**

将`rgba`值赋予该`QRgba64`实例并返回。

### `[constexpr noexcept, since 6.11.1] size_t qHash(QRgba64 key, size_t seed = 0)`

**作用与语义：**

返回 `key` 的哈希值，使用 `seed` 来做种计算。
在 6.11.1 之前的 Qt 版本中，该类型通过隐式转换为 quint64 实现了可哈希。这种显式的 qHash() 重载保持了与隐式 qHash() 的兼容性。

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

`QRgba64` 所属机制类型：Qt 类型机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
