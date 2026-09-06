# QRhiBuffer

> Qt 6.11.1 · Qt GUI

## 1. 先建立直觉

**一句话定位：** 这是 GUI 基础类型，常用于绘制、输入、图像、字体或窗口系统集成。

**模块背景：** Qt GUI 负责窗口系统集成、绘制、颜色、字体、图像、输入事件和底层 GUI 资源。

### 这是什么

`QRhiBuffer` 是 Qt 类型机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

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

### 公有类型

- `struct NativeBuffer`
- `enum Type { Immutable, Static, Dynamic }`
- `enum UsageFlag { VertexBuffer, IndexBuffer, UniformBuffer, StorageBuffer }`
- `flags UsageFlags`

### 公有函数

- `virtual char * beginFullDynamicBufferUpdateForCurrentFrame()`
- `virtual bool create() = 0`
- `virtual void endFullDynamicBufferUpdateForCurrentFrame()`
- `virtual QRhiBuffer::NativeBuffer nativeBuffer()`
- `void setSize(quint32 sz)`
- `void setType(QRhiBuffer::Type t)`
- `void setUsage(QRhiBuffer::UsageFlags u)`
- `quint32 size() const`
- `QRhiBuffer::Type type() const`
- `QRhiBuffer::UsageFlags usage() const`

### 重实现的公有函数

- `virtual QRhiResource::Type resourceType() const override`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `enum QRhiBuffer::Type`

**作用与语义：**

指定缓冲资源的存储类型。
- `QRhiBuffer::Immutable`：`0`;表示数据在初始上传后预计不会再发生变化。底层，这些缓冲区资源通常被放置在设备本地（GPU）内存中（如适用的系统中）。上传新数据是可能的，但可能成本高昂。上传通常通过复制到一个独立的主机可见暂存缓冲区，从该缓冲区发送GPU缓冲区到仅限GPU缓冲区的缓存。
- `QRhiBuffer::Static`：`1`;表示数据预计变化频率较低。通常放置在设备本地（GPU）内存中（如适用）。在后端使用主机可见的预留缓冲区进行上传时，保留此类临时缓冲区，不同于不可变系统，因此后续上传不会影响性能。应避免频繁更新，尤其是连续帧更新。
- `QRhiBuffer::Dynamic`：`2`;表示数据预计会频繁变化。不建议用于大型缓冲区。通常由主机可见内存备份为两份备份，以便更改时不会阻碍图形流水线。双重缓冲对应用程序透明管理，API中不以任何形式暴露。这是推荐的类型，也是某些后端唯一可能的类型，用于`UniformBuffer`用途的缓冲区。

### `enum QRhiBuffer::UsageFlagflags QRhiBuffer::UsageFlags`

**作用与语义：**

标志值用于指定缓冲区的使用方式。
- `QRhiBuffer::VertexBuffer`: `1 << 0`；顶点缓冲区。这允许在`setVertexInput()`中使用`QRhiBuffer`。
- `QRhiBuffer::IndexBuffer`: `1 << 1`；索引缓冲区。这允许在`setVertexInput()`中使用`QRhiBuffer`。
- `QRhiBuffer::UniformBuffer`: `1 << 2`；统一缓冲区（也称为常量缓冲区）。这允许 `QRhiBuffer` 与 `UniformBuffer` 结合使用。当报告 `NonDynamicUniformBuffers` 不受支持时，此用法只能与 Dynamic 类型结合使用。
- `QRhiBuffer::StorageBuffer`: `1 << 3`；存储缓冲区。这允许 `QRhiBuffer` 与 `BufferLoad`、`BufferStore` 或 `BufferLoadStore` 结合使用。此用法只能与 Immutable 或 Static 类型结合，并且仅在计算功能被报告为支持时可用。
UsageFlags 类型是 QFlags<UsageFlag> 的 typedef。它存储 UsageFlag 值的 OR 组合。

### `[virtual] char *QRhiBuffer::beginFullDynamicBufferUpdateForCurrentFrame()`

**作用与语义：**

返回一个指向带有主机可见缓冲区数据的内存块的指针。
这是中大型动态均匀缓冲区的捷径，这些缓冲区的全部内容（或至少当前帧中着色器读取的所有区域）在每帧中都会发生变化，基于`QRhiResourceUpdateBatch`的更新机制因大量数据复制而显得过于繁重。
调用该函数后，必须先调用 endFullDynamicUniformBufferUpdateForCurrentFrame()，然后才能记录依赖该缓冲区的任何渲染或计算过程。
警告：通过这种方法更新数据与基于`QRhiResourceUpdateBatch`的更新和回读不兼容。当尝试将两个更新模型合并为同一缓冲区时，可能会出现意外行为。同样，这种直接更新的数据可能不会被readBackBuffer操作看到，具体取决于后端。
警告：通过此方法更新缓冲区数据时，必须在每个帧内进行更新，否则执行双重或三重缓冲资源的后端可能会出现意外行为。
警告：这种方法无法进行部分更新，因为有些后端可能会选择在调用该函数时丢失缓冲区的先前内容。数据必须写入当前准备帧中所有被着色器读取的区域。
警告：此函数只能在录制帧时调用，因此在`QRhi::beginFrame()`和`QRhi::endFrame()`之间。
警告：该函数只能在动态缓冲区上调用。

### `[pure virtual] bool QRhiBuffer::create()`

**作用与语义：**

创建对应的本地图形资源。如果由于之前的 create() 存在资源且没有相应的`destroy()`，则 `destroy()` 会先隐式调用。
成功时返回`true`，`false`图形操作失败时返回。无论返回值如何，调用`destroy()`始终安全。

### `[virtual] void QRhiBuffer::endFullDynamicBufferUpdateForCurrentFrame()`

**作用与语义：**

当缓冲区数据的全部内容更新后，返回`beginFullDynamicBufferUpdateForCurrentFrame()`的内存块中，才会被调用。

### `[virtual] QRhiBuffer::NativeBuffer QRhiBuffer::nativeBuffer()`

**作用与语义：**

返回该缓冲区的底层本地资源。如果后端不支持暴露底层本地资源，返回的值将为空。
一个`QRhiBuffer`可能由多个本地缓冲对象支持，具体取决于所用`type()`和`QRhi`后端。在这种情况下，所有缓冲区都会返回到返回结构体中的对象数组中，slotCount 指定本地缓冲对象的数量。在录制帧时，`QRhi::currentFrameSlot()` 可以用来确定`QRhi`在记录帧内从该`QRhiBuffer`读取或写入操作的本地缓冲区。
在某些情况下，`QRhiBuffer`根本没有原生缓冲对象支持。此时 slotCount 将设为 0，且不会返回有效的原生对象。这不是错误，当某个后端不为某些类型或用途的 QRhiBuffer 使用原生缓冲区时，这是完全合理的。
注意：请注意，`QRhi`后端可能会采用各种缓冲区更新策略。与纹理不同，纹理上传图像数据总是意味着在命令缓冲区上记录缓冲区到图像（或类似）复制命令，缓冲区，尤其是动态缓冲区和`UniformBuffer`缓冲区，可以有多种不同的工作方式。例如，使用类型为`UniformBuffer`的`QRhiBuffer`，如果后端和图形API不使用或支持统一缓冲区，可能根本没有原生缓冲对象支持。数据写入缓冲区的方式和备份存储器的类型也存在差异。对于由主机可见内存支持的缓冲区，调用该函数可以保证所有返回的原生缓冲区都能执行待处理的主机写入。

### `[override virtual] QRhiResource::Type QRhiBuffer::resourceType() const`

**作用与语义：**

重装：`QRhiResource::resourceType()` const.
返回资源类型。
返回资源类型。

### `void QRhiBuffer::setSize(quint32 sz)`

**作用与语义：**

设置缓冲区的大小（字节单位）。大小通常在`QRhi::newBuffer()`中指定，因此该函数仅在需要更改大小时使用。与其他设置器一样，大小仅在调用`create()`时生效，对于已创建的缓冲区，这意味着释放之前的原生资源并在内部创建新的资源。
后端可能会选择分配大于`sz`的缓冲区以满足对齐要求。这对应用程序是隐藏的，`size()`总是会报告`sz`中请求的大小。

### `void QRhiBuffer::setType(QRhiBuffer::Type t)`

**作用与语义：**

将缓冲区类型设置为`t`。

### `void QRhiBuffer::setUsage(QRhiBuffer::UsageFlags u)`

**作用与语义：**

将缓冲区的使用标志设置为`u`。

### `quint32 QRhiBuffer::size() const`

**作用与语义：**

返回缓冲区的大小（字节单位）。
这始终是传递给`setSize()`或 `QRhi::newBuffer()` 的值。内部，如果底层图形 API 需要，原生缓冲区可能会更大。

### `QRhiBuffer::Type QRhiBuffer::type() const`

**作用与语义：**

返回缓冲区类型。

### `QRhiBuffer::UsageFlags QRhiBuffer::usage() const`

**作用与语义：**

返回缓冲区的使用标志。

### `struct NativeBuffer`

**作用与语义：**

包含缓冲区底层原生资源的信息。

### `enum UsageFlag { VertexBuffer, IndexBuffer, UniformBuffer, StorageBuffer }`

**作用与语义：**

标志值用于指定缓冲区的使用方式。
- `QRhiBuffer::VertexBuffer`: `1 << 0`；顶点缓冲区。这允许在`setVertexInput()`中使用`QRhiBuffer`。
- `QRhiBuffer::IndexBuffer`: `1 << 1`；索引缓冲区。这允许在`setVertexInput()`中使用`QRhiBuffer`。
- `QRhiBuffer::UniformBuffer`: `1 << 2`；统一缓冲区（也称为常量缓冲区）。这允许 `QRhiBuffer` 与 `UniformBuffer` 结合使用。当报告 `NonDynamicUniformBuffers` 不受支持时，此用法只能与 Dynamic 类型结合使用。
- `QRhiBuffer::StorageBuffer`: `1 << 3`；存储缓冲区。这允许 `QRhiBuffer` 与 `BufferLoad`、`BufferStore` 或 `BufferLoadStore` 结合使用。此用法只能与 Immutable 或 Static 类型结合，并且仅在计算功能被报告为支持时可用。
UsageFlags 类型是 QFlags<UsageFlag> 的 typedef。它存储 UsageFlag 值的 OR 组合。

### `flags UsageFlags`

**作用与语义：**

标志值用于指定缓冲区的使用方式。
- `QRhiBuffer::VertexBuffer`: `1 << 0`；顶点缓冲区。这允许在`setVertexInput()`中使用`QRhiBuffer`。
- `QRhiBuffer::IndexBuffer`: `1 << 1`；索引缓冲区。这允许在`setVertexInput()`中使用`QRhiBuffer`。
- `QRhiBuffer::UniformBuffer`: `1 << 2`；统一缓冲区（也称为常量缓冲区）。这允许 `QRhiBuffer` 与 `UniformBuffer` 结合使用。当报告 `NonDynamicUniformBuffers` 不受支持时，此用法只能与 Dynamic 类型结合使用。
- `QRhiBuffer::StorageBuffer`: `1 << 3`；存储缓冲区。这允许 `QRhiBuffer` 与 `BufferLoad`、`BufferStore` 或 `BufferLoadStore` 结合使用。此用法只能与 Immutable 或 Static 类型结合，并且仅在计算功能被报告为支持时可用。
UsageFlags 类型是 QFlags<UsageFlag> 的 typedef。它存储 UsageFlag 值的 OR 组合。

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

`QRhiBuffer` 所属机制类型：Qt 类型机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
