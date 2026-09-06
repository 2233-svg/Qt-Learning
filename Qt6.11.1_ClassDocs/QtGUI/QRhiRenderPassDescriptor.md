# QRhiRenderPassDescriptor

> Qt 6.11.1 · Qt GUI

## 1. 先建立直觉

**一句话定位：** 这是 GUI 基础类型，常用于绘制、输入、图像、字体或窗口系统集成。

**模块背景：** Qt GUI 负责窗口系统集成、绘制、颜色、字体、图像、输入事件和底层 GUI 资源。

### 这是什么

`QRhiRenderPassDescriptor` 是 Qt 类型机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

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

- `virtual bool isCompatible(const QRhiRenderPassDescriptor *other) const = 0`
- `virtual const QRhiNativeHandles * nativeHandles()`
- `virtual QRhiRenderPassDescriptor * newCompatibleRenderPassDescriptor() const = 0`
- `virtual QVector<quint32> serializedFormat() const = 0`

### 重实现的公有函数

- `virtual QRhiResource::Type resourceType() const override`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `[pure virtual] bool QRhiRenderPassDescriptor::isCompatible(const QRhiRenderPassDescriptor *other) const`

**作用与语义：**

如果`other` `QRhiRenderPassDescriptor`与该兼容，则返回为真，意味着`this`和`other`可以在`QRhiGraphicsPipeline::setRenderPassDescriptor()`中互换使用。
renderpass 描述符的兼容性概念类似于`QRhiShaderResourceBindings`实例的布局兼容性。它们允许更好地重用`QRhiGraphicsPipeline`实例：例如，`QRhiGraphicsPipeline`实例缓存应利用这些函数寻找匹配的流水线，而不仅仅是比较指针，从而允许在流水线中使用不同的`QRhiRenderPassDescriptor`和`QRhiShaderResourceBindings`，只要它们兼容即可。
兼容性的具体细节取决于底层图形API。来自同一`QRhiTextureRenderTarget`的两个renderpass描述符`created`始终兼容。
与`QRhiShaderResourceBindings`类似，也可以在没有两个现有对象的情况下测试兼容性。通过调用`serializedFormat()`提取不透明的斑点，可以通过将返回的向量与其他`QRhiRenderPassDescriptor`的`serializedFormat()`进行比较来测试兼容性。这在某些情况下有好处，因为即使流水线最初构建的`QRhiRenderPassDescriptor`已不可用（但从`serializedFormat()`返回的数据仍然存在），也能测试`QRhiRenderPassDescriptor`与`QRhiGraphicsPipeline`的兼容性。

### `[virtual] const QRhiNativeHandles *QRhiRenderPassDescriptor::nativeHandles()`

**作用与语义：**

返回指向后端特定`QRhiNativeHandles`子类的指针，如`QRhiVulkanRenderPassNativeHandles`。当后端不支持暴露底层原生资源时，返回的值`nullptr`。

### `[pure virtual] QRhiRenderPassDescriptor *QRhiRenderPassDescriptor::newCompatibleRenderPassDescriptor() const`

**作用与语义：**

返回一个新的 `QRhiRenderPassDescriptor`，它是与此对象兼容的 `compatible`。 该函数允许克隆一个 `QRhiRenderPassDescriptor`。返回的对象可直接使用，并且所有权转移给调用者。在存储与图形管线相关的数据结构中时，克隆一个 `QRhiRenderPassDescriptor` 对象可能非常有用（以便创建新的管线，而这通常需要渲染通道描述符对象），并且从渲染目标创建的渲染通道描述符的生命周期可能比管线短（例如，因为引擎会与创建渲染通道的纹理和渲染目标一起管理和销毁渲染通道）。在这种情况下，将克隆的版本存储在数据结构中，并转移所有权，将会很有益。

### `[override virtual] QRhiResource::Type QRhiRenderPassDescriptor::resourceType() const`

**作用与语义：**

重装：`QRhiResource::resourceType()` const.
返回资源类型。
返回资源类型。

### `[pure virtual] QVector<quint32> QRhiRenderPassDescriptor::serializedFormat() const`

**作用与语义：**

返回一个整数向量，包含一个不透明的斑点，描述与`compatibility`相关的数据。
给定两个`QRhiRenderPassDescriptor`对象`rp1`和`rp2`，如果该函数返回的数据相同，则`rp1->isCompatible(rp2)`，反之亦然。
注意：返回的数据用于存储内存和在对象所属`QRhi`生命周期内进行比较。它不用于存储在磁盘上、在进程间重复使用，或用于多个可能拥有不同后端的`QRhi`实例。
注意：调用该函数预计是一项廉价操作，因为后端不应计算该函数中的数据，而是返回已计算出的数据序列。
当作为库的一部分创建可复用组件时，图形管线是在针对库客户端管理的`QRhiRenderTarget`（无论是交换链还是纹理）时创建和维护，组件必须能够应对变化的 `QRhiRenderPassDescriptor`。例如，因为渲染目标发生变化，导致之前的`QRhiRenderPassDescriptor`失效（至少对新渲染目标而言），原因是颜色格式和附件可能不同。或者因为动态使用了可变速率着色。一个简单的模式是对每一帧执行以下检查，以识别何时需要将流水线关联到新的`QRhiRenderPassDescriptor`，因为渲染目标现在与早期帧有所不同：

**官方示例：**

```cpp
 QRhiRenderPassDescriptor *rp = m_renderTarget->renderPassDescriptor();
 if (m_pipeline && rp->serializedFormat() != m_renderPassFormat) {
     m_pipeline->setRenderPassDescriptor(rp);
     m_renderPassFormat = rp->serializedFormat();
     m_pipeline->create();
 }
 // remember to store m_renderPassFormat also when creating m_pipeline the first time
```

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

`QRhiRenderPassDescriptor` 所属机制类型：Qt 类型机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
