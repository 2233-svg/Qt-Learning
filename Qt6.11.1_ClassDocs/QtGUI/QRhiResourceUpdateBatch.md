# QRhiResourceUpdateBatch

> Qt 6.11.1 · Qt GUI

## 1. 先建立直觉

**一句话定位：** 这是 GUI 基础类型，常用于绘制、输入、图像、字体或窗口系统集成。

**模块背景：** Qt GUI 负责窗口系统集成、绘制、颜色、字体、图像、输入事件和底层 GUI 资源。

### 这是什么

`QRhiResourceUpdateBatch` 是 Qt 类型机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

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

### 公有函数

- `void copyTexture(QRhiTexture *dst, QRhiTexture *src, const QRhiTextureCopyDescription &desc = QRhiTextureCopyDescription())`
- `void generateMips(QRhiTexture *tex)`
- `bool hasOptimalCapacity() const`
- `void merge(QRhiResourceUpdateBatch *other)`
- `void readBackBuffer(QRhiBuffer *buf, quint32 offset, quint32 size, QRhiReadbackResult *result)`
- `void readBackTexture(const QRhiReadbackDescription &rb, QRhiReadbackResult *result)`
- `void release()`
- `void updateDynamicBuffer(QRhiBuffer *buf, quint32 offset, quint32 size, const void *data)`
- `(since 6.10) void updateDynamicBuffer(QRhiBuffer *buf, quint32 offset, QByteArray data)`
- `void uploadStaticBuffer(QRhiBuffer *buf, quint32 offset, quint32 size, const void *data)`
- `(since 6.10) void uploadStaticBuffer(QRhiBuffer *buf, QByteArray data)`
- `void uploadStaticBuffer(QRhiBuffer *buf, const void *data)`
- `(since 6.10) void uploadStaticBuffer(QRhiBuffer *buf, quint32 offset, QByteArray data)`
- `void uploadTexture(QRhiTexture *tex, const QImage &image)`
- `void uploadTexture(QRhiTexture *tex, const QRhiTextureUploadDescription &desc)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `void QRhiResourceUpdateBatch::copyTexture(QRhiTexture *dst, QRhiTexture *src, const QRhiTextureCopyDescription &desc = QRhiTextureCopyDescription())`

**作用与语义：**

按照`desc`描述，将纹理间的纹理复制操作从`src`放入`dst`。
注意：源纹理`src`必须用`QRhiTexture::UsedAsTransferSource`创建。
注意：纹理的格式必须一致。大多数图形API数据是按原样复制的，没有任何格式转换。如果`dst`和`src`使用不同格式创建，可能会出现未说明的问题。

### `void QRhiResourceUpdateBatch::generateMips(QRhiTexture *tex)`

**作用与语义：**

为指定的纹理`tex`排入一个 mipmap 生成操作。
支持2D和立方体纹理。
注意：纹理必须用`QRhiTexture::MipMapped`和`QRhiTexture::UsedWithGenerateMips`来制作。
警告：`QRhi`无法保证所有支持的纹理格式都能生成mipmap。例如，`QRhiTexture::RGBA32F`在OpenGL ES 3.0和iOS上的Metal中不是`filterable`格式，因此mipmap生成请求可能会失败。RGBA8和RGBA16F通常可过滤，因此建议在需要生成mipmap时使用这些格式。

### `bool QRhiResourceUpdateBatch::hasOptimalCapacity() const`

**作用与语义：**

返回为真，直到该批次中排队的缓冲区和纹理操作数量低于合理限制。
当该批次添加的缓冲区和/或纹理操作数量达到或即将达到某个上限时，返回值为假。批处理完后也完全正常，但可能需要分配额外内存。因此，如果渲染器在准备帧时会在单一批中收集大量缓冲区和纹理更新，可能需要考虑提交批次并在该函数返回 false 时重新开始新批次。

### `void QRhiResourceUpdateBatch::merge(QRhiResourceUpdateBatch *other)`

**作用与语义：**

将`other`批次中所有排队操作复制到该批次中。
注意：合并操作后`other`可能不再包含有效数据，且不得提交，但仍需通过调用`release()`释放数据。
这提供了方便的模式，即在初始化步骤中已知的资源更新被收集成一个批次，然后在开始首次渲染时合并到另一个批次中：

**官方示例：**

```cpp
 void init()
 {
     initialUpdates = rhi->nextResourceUpdateBatch();
     initialUpdates->uploadStaticBuffer(vbuf, vertexData);
     initialUpdates->uploadStaticBuffer(ibuf, indexData);
     // ...
 }

 void render()
 {
     QRhiResourceUpdateBatch *resUpdates = rhi->nextResourceUpdateBatch();
     if (initialUpdates) {
         resUpdates->merge(initialUpdates);
         initialUpdates->release();
         initialUpdates = nullptr;
     }
     // resUpdates->updateDynamicBuffer(...);
     cb->beginPass(rt, clearCol, clearDs, resUpdates);
 }
```

### `void QRhiResourceUpdateBatch::readBackBuffer(QRhiBuffer *buf, quint32 offset, quint32 size, QRhiReadbackResult *result)`

**作用与语义：**

排队读取`QRhiBuffer` `buf`的某个区域。该区域的大小由`size`字节表示，`offset`是开始读取的偏移量（字节数）。
回读是异步的。`result`包含一个回调，操作完成后调用。数据以`QRhiReadbackResult::data`形式提供。成功完成时，该`QByteArray`大小将为`size`。失败时，`QByteArray`将为空。
注意：只有当`QRhi::ReadBackNonUniformBuffer`功能被报告为支持时，才支持读取使用量与`QRhiBuffer::UniformBuffer`不同的缓冲区。
注意：当满足以下条件之一时，异步回读保证完成：`finish()`已调用;或者至少`N`帧已被`submitted`，包括发出回读操作的帧，并且已开始新帧录制，其中`N`是`QRhi::MaxAsyncReadbackFrames`返回的资源限制值。

### `void QRhiResourceUpdateBatch::readBackTexture(const QRhiReadbackDescription &rb, QRhiReadbackResult *result)`

**作用与语义：**

按照`rb`描述，将纹理复制到主机的复制操作排队。
通常`rb`会指定一个`QRhiTexture`作为源。然而，当当前帧中的交换链是用`QRhiSwapChain::UsedAsTransferSource`创建的，它也可以是读取的来源。为此，`rb`中纹理设置为空。
与其他操作不同，这里的结果需要由应用程序处理。因此，`result`不仅提供数据，还提供回调功能，因为批处理的操作本质上是异步的：
注意：纹理必须用`QRhiTexture::UsedAsTransferSource`制作。
注意：多采样纹理无法读取。
注意：读回返回原始字节数据，以便应用程序以任何他们认为合适的方式解释。注意渲染代码的混合设置：如果混合设置为依赖预乘法 alpha，则读回结果也必须被解释为预乘法。
注意：在解读所得原始数据时，请注意回读采用字节排序格式。因此，`RGBA8`纹理映射到字节排序的`QImage`格式，如`QImage::Format_RGBA8888`。
注意：当满足以下条件之一时，异步回读保证完成：`finish()` 已被调用;或者至少已`N`帧被 `submitted`，包括发出回读操作的帧，并且已开始新帧记录，其中 `N` 是返回的资源限制值`QRhi::MaxAsyncReadbackFrames`。
单次读回操作一次复制一个图层（立方体映射、面或三维切片或纹理数组元素）的一级 mip。层级和层由 `rb` 中的相应字段指定。

**官方示例：**

```cpp
 rhi->beginFrame(swapchain);
 cb->beginPass(swapchain->currentFrameRenderTarget(), colorClear, dsClear);
 // ...
 QRhiReadbackResult *rbResult = new QRhiReadbackResult;
 rbResult->completed = [rbResult] {
     {
         const QImage::Format fmt = QImage::Format_RGBA8888_Premultiplied; // fits QRhiTexture::RGBA8
         const uchar *p = reinterpret_cast<const uchar *>(rbResult->data.constData());
         QImage image(p, rbResult->pixelSize.width(), rbResult->pixelSize.height(), fmt);
         image.save("result.png");
     }
     delete rbResult;
 };
 QRhiResourceUpdateBatch *u = nextResourceUpdateBatch();
 QRhiReadbackDescription rb; // no texture -> uses the current backbuffer of sc
 u->readBackTexture(rb, rbResult);
 cb->endPass(u);
 rhi->endFrame(swapchain);
```

### `void QRhiResourceUpdateBatch::release()`

**作用与语义：**

将批次返回池。只有当批次未传递给`QRhiCommandBuffer::beginPass()`、`QRhiCommandBuffer::endPass()`或`QRhiCommandBuffer::resourceUpdate()`时，才应使用，因为这些实例隐式调用了destroy()。
注意：`QRhiResourceUpdateBatch`实例绝不能被应用程序 `deleted`。

### `void QRhiResourceUpdateBatch::updateDynamicBuffer(QRhiBuffer *buf, quint32 offset, quint32 size, const void *data)`

**作用与语义：**

Enqueue 更新了类型为 `QRhiBuffer::Dynamic` 的创建的`QRhiBuffer` `buf`区域。
区域指定为`offset`和`size`。实际写入的字节由`data`指定，且）至少有`size`字节可用。
`data`会被复制，一旦该函数恢复，就可以安全地销毁或更改。
注意：如果涉及主机写入，通常如updateDynamicBuffer()，因为此类缓冲区在大多数后端中由主机可见内存支持，写入可能会在帧内累积。因此，第一遍读取被批处理到第二遍的区域时，可能会看到第二遍更新批处理中指定的更改。
注意：`QRhi`透明地管理双重缓冲，以防止图形流水线停滞。使用`QRhi`和 `QRhiResourceUpdateBatch` 时，`QRhiBuffer`底下可能有多个原生缓冲对象的事实可以被安全忽略。

### `[since 6.10] void QRhiResourceUpdateBatch::updateDynamicBuffer(QRhiBuffer *buf, quint32 offset, QByteArray data)`

**作用与语义：**

排队更新以类型为 `QRhiBuffer::Dynamic` 创建的`QRhiBuffer` `buf`区域。
`data`被移入批处理中，而不是用这种重载复制。

### `void QRhiResourceUpdateBatch::uploadStaticBuffer(QRhiBuffer *buf, quint32 offset, quint32 size, const void *data)`

**作用与语义：**

Enqueue 更新以类型为 `QRhiBuffer::Immutable` 或 `QRhiBuffer::Static` 创建的`QRhiBuffer` `buf`区域。
区域指定为`offset`和 `size`。实际写入的字节由`data`指定，且必须至少有`size`字节可用。
`data`会被复制，一旦该函数恢复，就可以安全地销毁或更改。

### `[since 6.10] void QRhiResourceUpdateBatch::uploadStaticBuffer(QRhiBuffer *buf, QByteArray data)`

**作用与语义：**

用类型`QRhiBuffer::Immutable`或`QRhiBuffer::Static`创建的整个`QRhiBuffer` `buf`的队列。
`data`被移入批次，而不是用这种重载复制。
`data`大小必须等于`buf`的大小。

### `void QRhiResourceUpdateBatch::uploadStaticBuffer(QRhiBuffer *buf, const void *data)`

**作用与语义：**

更新整个 `QRhiBuffer` `buf` 的队列类型为 `QRhiBuffer::Immutable` 或 `QRhiBuffer::Static`。

### `[since 6.10] void QRhiResourceUpdateBatch::uploadStaticBuffer(QRhiBuffer *buf, quint32 offset, QByteArray data)`

**作用与语义：**

Enqueue 更新以类型为 `QRhiBuffer::Immutable` 或 `QRhiBuffer::Static` 创建的`QRhiBuffer` `buf`区域。
`data`被移入批处理中，而不是用这种重载复制。

### `void QRhiResourceUpdateBatch::uploadTexture(QRhiTexture *tex, const QImage &image)`

**作用与语义：**

在纹理`tex`第0层的MIP级上传图像数据时，会排队。
`tex`必须是未压缩格式。其格式还必须与`image`的 `QImage::format()`兼容。源数据以`image`形式提供。

### `void QRhiResourceUpdateBatch::uploadTexture(QRhiTexture *tex, const QRhiTextureUploadDescription &desc)`

**作用与语义：**

排队上传一个或多个 mip 级别的图像数据，分布在纹理`tex`的一层或多层。
复制的细节（源码`QImage`或压缩纹理数据、区域、目标图层和关卡）在`desc`中描述。

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

`QRhiResourceUpdateBatch` 所属机制类型：Qt 类型机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
