# QRhiRenderBuffer

> Qt 6.11.1 · Qt GUI

## 1. 先建立直觉

**一句话定位：** 这是 GUI 基础类型，常用于绘制、输入、图像、字体或窗口系统集成。

**模块背景：** Qt GUI 负责窗口系统集成、绘制、颜色、字体、图像、输入事件和底层 GUI 资源。

### 这是什么

`QRhiRenderBuffer` 是 Qt 类型机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

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

- `struct NativeRenderBuffer`
- `enum Flag { UsedWithSwapChainOnly }`
- `flags Flags`
- `enum Type { DepthStencil, Color }`

### 公有函数

- `virtual bool create() = 0`
- `virtual bool createFrom(QRhiRenderBuffer::NativeRenderBuffer src)`
- `QRhiRenderBuffer::Flags flags() const`
- `QSize pixelSize() const`
- `int sampleCount() const`
- `void setFlags(QRhiRenderBuffer::Flags f)`
- `void setPixelSize(const QSize &sz)`
- `void setSampleCount(int s)`
- `void setType(QRhiRenderBuffer::Type t)`
- `QRhiRenderBuffer::Type type() const`

### 重实现的公有函数

- `virtual QRhiResource::Type resourceType() const override`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `enum QRhiRenderBuffer::Flagflags QRhiRenderBuffer::Flags`

**作用与语义：**

旗值用于`flags()`和`setFlags()`。
- `QRhiRenderBuffer::UsedWithSwapChainOnly`：`1 << 0`;对于`DepthStencil`渲染缓冲区，这表明渲染缓冲区仅与`QRhiSwapChain`结合使用，绝不以其他方式使用。这提供了自动的大小调整和资源重建，因此在设置该标志时无需调用`setPixelSize()`或`create()`。该标志值也可能触发后端特定行为，例如在OpenGL中，使用独立的窗口系统接口API（如EGL、GLX等），该标志尤为重要，因为它避免创建实际的渲染缓冲区资源，因为已有窗口系统根据`QSurfaceFormat`的要求提供深度/模板缓冲区。
Flags 类型是 QFlags 的 typedef<Flag>。它存储 Flag 值的 OR 组合。

### `enum QRhiRenderBuffer::Type`

**作用与语义：**

指定渲染缓冲器的类型。
- `QRhiRenderBuffer::DepthStencil`：`0`;深度/模板合成
- `QRhiRenderBuffer::Color`：`1`;颜色

### `[pure virtual] bool QRhiRenderBuffer::create()`

**作用与语义：**

创建对应的本地图形资源。如果由于之前的 create() 存在资源且没有相应的`destroy()`，则 `destroy()` 会先隐式调用。
成功时返回`true`，`false`图形操作失败时返回。无论返回值如何，调用`destroy()`始终安全。

### `[virtual] bool QRhiRenderBuffer::createFrom(QRhiRenderBuffer::NativeRenderBuffer src)`

**作用与语义：**

类似于`create()`，但不会创建新的原生渲染缓冲对象。取而代之的是使用`src`指定的原生渲染缓冲对象。
这允许从外部图形引擎导入现有的渲染缓冲区对象（该对象必须属于同一设备或共享上下文，具体取决于图形API）。
注意：目前仅适用于 OpenGL。该函数仅用于导入绑定到某些特殊外部对象（如 EGLImageKHR）的渲染缓冲对象。一旦应用程序执行了 glEGLImageTargetRenderbufferStorageOES 调用，渲染缓冲对象可以传递给该函数以创建包裹`QRhiRenderBuffer`，然后作为颜色附件传递到`QRhiTextureRenderTarget`上，从而实现向 EGLImage 的渲染。
注意：`pixelSize()`、`sampleCount()`和`flags()`仍需正确设置。将错误的大小和其他值传递给`QRhi::newRenderBuffer()`，然后再用createFrom()，期望仅凭本地渲染缓冲对象推断这些值，这是错误的，会导致问题。
注意：`QRhiRenderBuffer`不拥有本地对象的所有权，`destroy()`也不会释放该对象。
注意：该函数仅在`QRhi::RenderBufferImport`特性报告为`supported`时实现。否则，函数不做任何操作，返回值为`false`。
成功时`true`退货，`false`不支持时退货。

### `QRhiRenderBuffer::Flags QRhiRenderBuffer::flags() const`

**作用与语义：**

还旗子。

### `QSize QRhiRenderBuffer::pixelSize() const`

**作用与语义：**

返回像素大小。

### `[override virtual] QRhiResource::Type QRhiRenderBuffer::resourceType() const`

**作用与语义：**

重装：`QRhiResource::resourceType()` const.
返回资源类型。
返回资源类型。

### `int QRhiRenderBuffer::sampleCount() const`

**作用与语义：**

返回采样计数。1表示没有多采样抗锯齿。

### `void QRhiRenderBuffer::setFlags(QRhiRenderBuffer::Flags f)`

**作用与语义：**

把标志设为`f`。

### `void QRhiRenderBuffer::setPixelSize(const QSize &sz)`

**作用与语义：**

将像素大小设置为`sz`。

### `void QRhiRenderBuffer::setSampleCount(int s)`

**作用与语义：**

将样本计数设置为`s`。

### `void QRhiRenderBuffer::setType(QRhiRenderBuffer::Type t)`

**作用与语义：**

将类型设置为`t`。

### `QRhiRenderBuffer::Type QRhiRenderBuffer::type() const`

**作用与语义：**

返回渲染缓冲区类型。

### `struct NativeRenderBuffer`

**作用与语义：**

包裹一个原生渲染缓冲对象。

### `enum Flag { UsedWithSwapChainOnly }`

**作用与语义：**

旗值用于`flags()`和`setFlags()`。
- `QRhiRenderBuffer::UsedWithSwapChainOnly`：`1 << 0`;对于`DepthStencil`渲染缓冲区，这表明渲染缓冲区仅与`QRhiSwapChain`结合使用，绝不以其他方式使用。这提供了自动的大小调整和资源重建，因此在设置该标志时无需调用`setPixelSize()`或`create()`。该标志值也可能触发后端特定行为，例如在OpenGL中，使用独立的窗口系统接口API（如EGL、GLX等），该标志尤为重要，因为它避免创建实际的渲染缓冲区资源，因为已有窗口系统根据`QSurfaceFormat`的要求提供深度/模板缓冲区。
Flags 类型是 QFlags 的 typedef<Flag>。它存储 Flag 值的 OR 组合。

### `flags Flags`

**作用与语义：**

旗值用于`flags()`和`setFlags()`。
- `QRhiRenderBuffer::UsedWithSwapChainOnly`：`1 << 0`;对于`DepthStencil`渲染缓冲区，这表明渲染缓冲区仅与`QRhiSwapChain`结合使用，绝不以其他方式使用。这提供了自动的大小调整和资源重建，因此在设置该标志时无需调用`setPixelSize()`或`create()`。该标志值也可能触发后端特定行为，例如在OpenGL中，使用独立的窗口系统接口API（如EGL、GLX等），该标志尤为重要，因为它避免创建实际的渲染缓冲区资源，因为已有窗口系统根据`QSurfaceFormat`的要求提供深度/模板缓冲区。
Flags 类型是 QFlags 的 typedef<Flag>。它存储 Flag 值的 OR 组合。

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

`QRhiRenderBuffer` 所属机制类型：Qt 类型机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
