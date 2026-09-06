# QRhiShaderResourceBindings

> Qt 6.11.1 · Qt GUI

## 1. 先建立直觉

**一句话定位：** 这是 GUI 基础类型，常用于绘制、输入、图像、字体或窗口系统集成。

**模块背景：** Qt GUI 负责窗口系统集成、绘制、颜色、字体、图像、输入事件和底层 GUI 资源。

### 这是什么

`QRhiShaderResourceBindings` 是 Qt 类型机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 这个类的行为由它的继承关系、构造参数、公开状态和成员函数协议共同决定。使用时要把创建、配置、核心操作、结果/通知和清理看成一条闭环，而不是孤立调用某个函数。

**适用场景：** 围绕这个类的核心职责建立最小闭环：准备依赖 -> 创建/取得对象 -> 设置必要配置 -> 调用核心 API -> 检查返回值和状态 -> 处理结果/错误 -> 结束时清理。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要忽略构造失败、空返回、默认值和版本限制；不要把异步 API 当同步 API；不要在没有确认所有权和线程的情况下保存指针或跨线程调用。

## 2. 依赖与对象关系

- 头文件：`#include <rhi/qrhi.h>`
- 继承自：QRhiResource
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

### 公有函数

- `const QRhiShaderResourceBinding * bindingAt(qsizetype index) const`
- `qsizetype bindingCount() const`
- `const QRhiShaderResourceBinding * cbeginBindings() const`
- `const QRhiShaderResourceBinding * cendBindings() const`
- `virtual bool create() = 0`
- `bool isLayoutCompatible(const QRhiShaderResourceBindings *other) const`
- `QVector<quint32> serializedLayoutDescription() const`
- `void setBindings(std::initializer_list<QRhiShaderResourceBinding> list)`
- `void setBindings(InputIterator first, InputIterator last)`

### 重实现的公有函数

- `virtual QRhiResource::Type resourceType() const override`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `const QRhiShaderResourceBinding *QRhiShaderResourceBindings::bindingAt(qsizetype index) const`

**作用与语义：**

在指定的`index`返回绑定。

### `qsizetype QRhiShaderResourceBindings::bindingCount() const`

**作用与语义：**

返回绑定数量。

### `const QRhiShaderResourceBinding *QRhiShaderResourceBindings::cbeginBindings() const`

**作用与语义：**

返回一个 const 迭代器，指向绑定列表中的第一个项。

### `const QRhiShaderResourceBinding *QRhiShaderResourceBindings::cendBindings() const`

**作用与语义：**

返回一个连接迭代器，指向绑定列表最后一项之后。

### `[pure virtual] bool QRhiShaderResourceBindings::create()`

**作用与语义：**

创建对应的资源绑定集。根据底层的图形API，这可能需要创建本地图形资源，因此不应假设这是一项廉价操作。
如果之前调用过create()，且没有对应的`destroy()`，那么`destroy()`会先隐式调用。
成功时返回`true`，失败时返回`false`。无论返回值如何，调用`destroy()`始终是安全的。

### `bool QRhiShaderResourceBindings::isLayoutCompatible(const QRhiShaderResourceBindings *other) const`

**作用与语义：**

如果布局与`other`兼容，返回`true`。布局不包含实际资源（如缓冲区或纹理）及相关参数（如偏移或大小）。但它包含绑定点、流水线阶段和资源类型。绑定的数量和顺序也必须匹配，才能兼容。
当用该`QRhiShaderResourceBindings`创建`QRhiGraphicsPipeline`且函数返回`true`时，`other`就可以安全地传递给`QRhiCommandBuffer::setShaderResources()`，从而与管道一起替代该`QRhiShaderResourceBindings`。
注意：该函数必须在成功`create()`后调用，因为它依赖于底层数据结构烘焙过程中生成的数据。这样，函数可以实现比通过两个绑定列表并调用每对`QRhiShaderResourceBinding::isLayoutCompatible()`更高效的比较方法。这在该函数被高频调用时尤为重要。

### `[override virtual] QRhiResource::Type QRhiShaderResourceBindings::resourceType() const`

**作用与语义：**

重装：`QRhiResource::resourceType()` const.
返回资源类型。
返回资源类型。

### `QVector<quint32> QRhiShaderResourceBindings::serializedLayoutDescription() const`

**作用与语义：**

返回一个整数向量，包含一个不透明的斑点，描述了绑定列表的布局，即与布局兼容性测试相关的数据。
给定两个对象`srb1`和`srb2`，如果该函数返回的数据相同，则`srb1->isLayoutCompatible(srb2)`，反之亦然。
注意：返回的数据用于存储在内存中，并在对象所属`QRhi`的生命周期内进行比较。它不用于存储在磁盘上、在进程间重复使用，或与多个可能拥有不同后端的`QRhi`实例使用。

### `void QRhiShaderResourceBindings::setBindings(std::initializer_list<QRhiShaderResourceBinding> list)`

**作用与语义：**

设定绑定`list`。

### `template <typename InputIterator> void QRhiShaderResourceBindings::setBindings(InputIterator first, InputIterator last)`

**作用与语义：**

设置迭代器 `first` 和 `last` 的绑定列表。

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

`QRhiShaderResourceBindings` 所属机制类型：Qt 类型机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
