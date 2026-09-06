# QRhiVertexInputAttribute

> Qt 6.11.1 · Qt GUI

## 1. 先建立直觉

**一句话定位：** 这是 GUI 基础类型，常用于绘制、输入、图像、字体或窗口系统集成。

**模块背景：** Qt GUI 负责窗口系统集成、绘制、颜色、字体、图像、输入事件和底层 GUI 资源。

### 这是什么

`QRhiVertexInputAttribute` 是 Qt 类型机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 这个类的行为由它的继承关系、构造参数、公开状态和成员函数协议共同决定。使用时要把创建、配置、核心操作、结果/通知和清理看成一条闭环，而不是孤立调用某个函数。

**适用场景：** 围绕这个类的核心职责建立最小闭环：准备依赖 -> 创建/取得对象 -> 设置必要配置 -> 调用核心 API -> 检查返回值和状态 -> 处理结果/错误 -> 结束时清理。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要忽略构造失败、空返回、默认值和版本限制；不要把异步 API 当同步 API；不要在没有确认所有权和线程的情况下保存指针或跨线程调用。

## 2. 依赖与对象关系

- 头文件：`#include <rhi/qrhi.h>`
- 继承自：未在类页中列出
- 直接派生类：未在类页中列出

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS GuiPrivate)
target_link_libraries(mytarget PRIVATE Qt6::GuiPrivate)
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

- `enum Format { Float4, Float3, Float2, Float, UNormByte4, …, SShort }`

### 公有函数

- `QRhiVertexInputAttribute()`
- `QRhiVertexInputAttribute(int binding, int location, QRhiVertexInputAttribute::Format format, quint32 offset, int matrixSlice = -1)`
- `int binding() const`
- `QRhiVertexInputAttribute::Format format() const`
- `int location() const`
- `int matrixSlice() const`
- `quint32 offset() const`
- `void setBinding(int b)`
- `void setFormat(QRhiVertexInputAttribute::Format f)`
- `void setLocation(int loc)`
- `void setMatrixSlice(int slice)`
- `void setOffset(quint32 ofs)`

### 相关非成员函数

- `size_t qHash(const QRhiVertexInputAttribute &key, size_t seed = 0)`
- `bool operator!=(const QRhiVertexInputAttribute &a, const QRhiVertexInputAttribute &b)`
- `bool operator==(const QRhiVertexInputAttribute &a, const QRhiVertexInputAttribute &b)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `enum QRhiVertexInputAttribute::Format`

**作用与语义：**

指定元素数据的类型。
- `QRhiVertexInputAttribute::Float4`：`0`;四分量浮点矢量
- `QRhiVertexInputAttribute::Float3`：`1`;三分量浮子矢量
- `QRhiVertexInputAttribute::Float2`：`2`;双分量浮子矢量
- `QRhiVertexInputAttribute::Float`：`3`;浮游
- `QRhiVertexInputAttribute::UNormByte4`：`4`;四分量归一化的无符号字节向量
- `QRhiVertexInputAttribute::UNormByte2`：`5`;双分量归一化的无符号字节向量
- `QRhiVertexInputAttribute::UNormByte`：`6`;归一化的无符号字节
- `QRhiVertexInputAttribute::UInt4`：`7`;四分量无符号整数矢量
- `QRhiVertexInputAttribute::UInt3`：`8`;三分量无符号整数向量
- `QRhiVertexInputAttribute::UInt2`：`9`;两分量无符号整数矢量
- `QRhiVertexInputAttribute::UInt`：`10`;无符号整数
- `QRhiVertexInputAttribute::SInt4`：`11`;四分量带符号整数向量
- `QRhiVertexInputAttribute::SInt3`：`12`;三分量带符号整数矢量
- `QRhiVertexInputAttribute::SInt2`：`13`;两分量带符号整数矢量
- `QRhiVertexInputAttribute::SInt`：`14`;带符号整数
- `QRhiVertexInputAttribute::Half4`：`15`;四分量半精度（16位）浮点向量
- `QRhiVertexInputAttribute::Half3`：`16`;三分量半精度（16位）浮点向量
- `QRhiVertexInputAttribute::Half2`：`17`;两分量半精度（16位）浮点向量
- `QRhiVertexInputAttribute::Half`：`18`;半精度（16位）浮点
- `QRhiVertexInputAttribute::UShort4`：`19`;四分量无符号短（16位）整数矢量
- `QRhiVertexInputAttribute::UShort3`：`20`;三分量无符号短（16位）整数矢量
- `QRhiVertexInputAttribute::UShort2`：`21`;两分量无符号短（16位）整数向量
- `QRhiVertexInputAttribute::UShort`：`22`;无符号短（16位）整数
- `QRhiVertexInputAttribute::SShort4`：`23`;四分量带符号短（16位）整数矢量
- `QRhiVertexInputAttribute::SShort3`：`24`;三分量带符号短（16位）整数矢量
- `QRhiVertexInputAttribute::SShort2`：`25`;两分量带符号短（16位）整数矢量
- `QRhiVertexInputAttribute::SShort`：`26`;带符号短（16位）整数
注意：运行时通过`QRhi::Feature::HalfAttributes`功能标志表示对半精度浮点属性的支持。


注意：Direct3D 11/12 支持16位输入属性，但不支持 Half3、UShort3 或 SShort3 类型。D3D 后端通过 Half3 为 Half4，UShort3 作为 UShort4，SShort3 作为 SShort4。为确保跨平台兼容性，16 位输入应填充为 8 字节。

### `[constexpr noexcept] QRhiVertexInputAttribute::QRhiVertexInputAttribute()`

**作用与语义：**

构建默认顶点输入属性描述。

### `QRhiVertexInputAttribute::QRhiVertexInputAttribute(int binding, int location, QRhiVertexInputAttribute::Format format, quint32 offset, int matrixSlice = -1)`

**作用与语义：**

构造一个顶点输入属性描述，包含指定的`binding`号、`location`、`format`和`offset`。
除非该属性对应矩阵的行或列（例如，一个4x4矩阵变成4个vec4，消耗4个连续顶点输入位置），否则`matrixSlice`应为-1，此时该属性应为该行或列的索引。`location - matrixSlice`必须始终等于展开矩阵第一行或第一列的 `location`。

### `int QRhiVertexInputAttribute::binding() const`

**作用与语义：**

返回绑定点索引。

### `QRhiVertexInputAttribute::Format QRhiVertexInputAttribute::format() const`

**作用与语义：**

返回顶点输入元素的格式。

### `int QRhiVertexInputAttribute::location() const`

**作用与语义：**

返回顶点输入元素的位置。

### `int QRhiVertexInputAttribute::matrixSlice() const`

**作用与语义：**

如果输入元素对应矩阵的行或列，则返回矩阵片;如果不相关，则返回-1。

### `quint32 QRhiVertexInputAttribute::offset() const`

**作用与语义：**

返回输入元素的字节偏移量。

### `void QRhiVertexInputAttribute::setBinding(int b)`

**作用与语义：**

将绑定点索引设置为`b`。默认情况下，索引设置为0。

### `void QRhiVertexInputAttribute::setFormat(QRhiVertexInputAttribute::Format f)`

**作用与语义：**

将顶点输入元素的格式设置为`f`。默认情况下，该格式设置为 Float4。

### `void QRhiVertexInputAttribute::setLocation(int loc)`

**作用与语义：**

将顶点输入元素的位置设为`loc`。默认情况下，这个位置设为0。

### `void QRhiVertexInputAttribute::setMatrixSlice(int slice)`

**作用与语义：**

设置矩阵`slice`。默认情况下，这个值设置为-1，只有当该属性对应矩阵的行或列时（例如，一个4x4矩阵变成4个vec4，消耗4个连续顶点输入位置），此时应设置为>= 0，此时它是该行或列的索引。`location - matrixSlice`必须始终等于展开矩阵第一行或第一列的`location`。

### `void QRhiVertexInputAttribute::setOffset(quint32 ofs)`

**作用与语义：**

将输入元素的字节偏移设置为`ofs`。

### `[noexcept] size_t qHash(const QRhiVertexInputAttribute &key, size_t seed = 0)`

**作用与语义：**

返回`key`的哈希值，使用`seed`来做种。

### `[noexcept] bool operator!=(const QRhiVertexInputAttribute &a, const QRhiVertexInputAttribute &b)`

**作用与语义：**

如果两个 `QRhiVertexInputAttribute` 对象 `a` 和 `b` 中的值相等，则返回 `false`；否则返回 `true`。

### `[noexcept] bool operator==(const QRhiVertexInputAttribute &a, const QRhiVertexInputAttribute &b)`

**作用与语义：**

如果两个`QRhiVertexInputAttribute`对象`a`和`b`的值相等，返回`true`。

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

`QRhiVertexInputAttribute` 所属机制类型：Qt 类型机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
