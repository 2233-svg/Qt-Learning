# QRgbaFloat

> Qt 6.11.1 · Qt GUI

## 1. 先建立直觉

**一句话定位：** 这是 GUI 基础类型，常用于绘制、输入、图像、字体或窗口系统集成。

**模块背景：** Qt GUI 负责窗口系统集成、绘制、颜色、字体、图像、输入事件和底层 GUI 资源。

### 这是什么

`QRgbaFloat` 是 Qt 类型机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 这个类的行为由它的继承关系、构造参数、公开状态和成员函数协议共同决定。使用时要把创建、配置、核心操作、结果/通知和清理看成一条闭环，而不是孤立调用某个函数。

**适用场景：** 围绕这个类的核心职责建立最小闭环：准备依赖 -> 创建/取得对象 -> 设置必要配置 -> 调用核心 API -> 检查返回值和状态 -> 处理结果/错误 -> 结束时清理。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要忽略构造失败、空返回、默认值和版本限制；不要把异步 API 当同步 API；不要在没有确认所有权和线程的情况下保存指针或跨线程调用。

## 2. 依赖与对象关系

- 头文件：`#include <QRgbaFloat>`
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

- `FastType`

### 公有函数

- `quint8 alpha8() const`
- `quint16 alpha16() const`
- `float alpha() const`
- `float alphaNormalized() const`
- `quint8 blue8() const`
- `quint16 blue16() const`
- `float blue() const`
- `float blueNormalized() const`
- `quint8 green8() const`
- `quint16 green16() const`
- `float green() const`
- `float greenNormalized() const`
- `bool isOpaque() const`
- `bool isTransparent() const`
- `QRgbaFloat<T> premultiplied() const`
- `quint8 red8() const`
- `quint16 red16() const`
- `float red() const`
- `float redNormalized() const`
- `void setAlpha(float alpha)`
- `void setBlue(float blue)`
- `void setGreen(float green)`
- `void setRed(float red)`
- `uint toArgb32() const`
- `QRgbaFloat<T> unpremultiplied() const`

### 静态公有成员

- `QRgbaFloat<T> fromArgb32(uint rgb)`
- `QRgbaFloat<T> fromRgba64(quint16 red, quint16 green, quint16 blue, quint16 alpha)`
- `QRgbaFloat<T> fromRgba(quint8 red, quint8 green, quint8 blue, quint8 alpha)`

### 相关非成员函数

- `QRgbaFloat16`
- `QRgbaFloat32`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `[alias] QRgbaFloat::FastType`

**作用与语义：**

浮水的别名。

### `[constexpr] quint8 QRgbaFloat::alpha8() const`

**作用与语义：**

将alpha通道返回为8位。

### `[constexpr] quint16 QRgbaFloat::alpha16() const`

**作用与语义：**

返回阿尔法通道为16位整数。

### `[constexpr] float QRgbaFloat::alpha() const`

**作用与语义：**

返回阿尔法通道。

### `[constexpr] float QRgbaFloat::alphaNormalized() const`

**作用与语义：**

返回归一化为`0.0f`到`1.0f`之间的α通道。

### `[constexpr] quint8 QRgbaFloat::blue8() const`

**作用与语义：**

将蓝色分量返回为8位。

### `[constexpr] quint16 QRgbaFloat::blue16() const`

**作用与语义：**

返回蓝色分量为16位整数。

### `[constexpr] float QRgbaFloat::blue() const`

**作用与语义：**

返回蓝色分量。

### `[constexpr] float QRgbaFloat::blueNormalized() const`

**作用与语义：**

返回归一化为`0.0f`到`1.0f`之间的蓝色分量。

### `[static constexpr] QRgbaFloat<T> QRgbaFloat::fromArgb32(uint rgb)`

**作用与语义：**

从32位ARGB值`rgb`构造`QRgbaFloat`值。

### `[static constexpr] QRgbaFloat<T> QRgbaFloat::fromRgba64(quint16 red, quint16 green, quint16 blue, quint16 alpha)`

**作用与语义：**

从四个16位整数色彩通道`red`、`green`、`blue`和`alpha`构建`QRgbaFloat`值。

### `[static constexpr] QRgbaFloat<T> QRgbaFloat::fromRgba(quint8 red, quint8 green, quint8 blue, quint8 alpha)`

**作用与语义：**

从四个8位色彩通道 `red`、`green`、`blue` 和 `alpha` 构建`QRgbaFloat`值。

### `[constexpr] quint8 QRgbaFloat::green8() const`

**作用与语义：**

返回绿色分量为8位。

### `[constexpr] quint16 QRgbaFloat::green16() const`

**作用与语义：**

返回绿色分量为16位整数。

### `[constexpr] float QRgbaFloat::green() const`

**作用与语义：**

返回绿色分量。

### `[constexpr] float QRgbaFloat::greenNormalized() const`

**作用与语义：**

返回归一化为`0.0f`到`1.0f`之间的绿色分量。

### `[constexpr] bool QRgbaFloat::isOpaque() const`

**作用与语义：**

返回颜色是否完全不透明。

### `[constexpr] bool QRgbaFloat::isTransparent() const`

**作用与语义：**

返回颜色是否完全透明。

### `[constexpr] QRgbaFloat<T> QRgbaFloat::premultiplied() const`

**作用与语义：**

返回带有预乘数的颜色。

### `[constexpr] quint8 QRgbaFloat::red8() const`

**作用与语义：**

红色分量以8位返回。

### `[constexpr] quint16 QRgbaFloat::red16() const`

**作用与语义：**

返回红色分量为16位整数。

### `[constexpr] float QRgbaFloat::red() const`

**作用与语义：**

返回红色分量。

### `[constexpr] float QRgbaFloat::redNormalized() const`

**作用与语义：**

返回红色分量，归一化为`0.0f`到`1.0f`之间的值。

### `void QRgbaFloat::setAlpha(float alpha)`

**作用与语义：**

将该颜色的α值设为`alpha`。

### `void QRgbaFloat::setBlue(float blue)`

**作用与语义：**

将该颜色的蓝色分量设置为`blue`。

### `void QRgbaFloat::setGreen(float green)`

**作用与语义：**

将该颜色的绿色分量设置为`green`。

### `void QRgbaFloat::setRed(float red)`

**作用与语义：**

将该颜色的红色分量设置为`red`。

### `[constexpr] uint QRgbaFloat::toArgb32() const`

**作用与语义：**

返回颜色的 32 位 ARGB 值。

### `[constexpr] QRgbaFloat<T> QRgbaFloat::unpremultiplied() const`

**作用与语义：**

返回带有未预代乘的alpha的颜色。

### `QRgbaFloat16`

**作用与语义：**

一个64位数据结构，包含四个16位浮点色彩通道：红、绿、蓝和阿尔法。

### `QRgbaFloat32`

**作用与语义：**

一个128位数据结构，包含四个32位浮点色彩通道：红、绿、蓝和阿尔法。

### `FastType`

**作用与语义：**

浮水的别名。

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

`QRgbaFloat` 所属机制类型：Qt 类型机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
