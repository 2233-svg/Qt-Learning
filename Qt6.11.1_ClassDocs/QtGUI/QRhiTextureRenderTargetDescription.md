# QRhiTextureRenderTargetDescription

> Qt 6.11.1 · Qt GUI

## 1. 先建立直觉

**一句话定位：** 这是 GUI 基础类型，常用于绘制、输入、图像、字体或窗口系统集成。

**模块背景：** Qt GUI 负责窗口系统集成、绘制、颜色、字体、图像、输入事件和底层 GUI 资源。

### 这是什么

`QRhiTextureRenderTargetDescription` 是 Qt 类型机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

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

- `QRhiTextureRenderTargetDescription()`
- `QRhiTextureRenderTargetDescription(const QRhiColorAttachment &colorAttachment)`
- `QRhiTextureRenderTargetDescription(const QRhiColorAttachment &colorAttachment, QRhiRenderBuffer *depthStencilBuffer)`
- `QRhiTextureRenderTargetDescription(const QRhiColorAttachment &colorAttachment, QRhiTexture *depthTexture)`
- `const QRhiColorAttachment * cbeginColorAttachments() const`
- `const QRhiColorAttachment * cendColorAttachments() const`
- `const QRhiColorAttachment * colorAttachmentAt(qsizetype index) const`
- `qsizetype colorAttachmentCount() const`
- `(since 6.8) QRhiTexture * depthResolveTexture() const`
- `QRhiRenderBuffer * depthStencilBuffer() const`
- `QRhiTexture * depthTexture() const`
- `void setColorAttachments(std::initializer_list<QRhiColorAttachment> list)`
- `void setColorAttachments(InputIterator first, InputIterator last)`
- `(since 6.8) void setDepthResolveTexture(QRhiTexture *tex)`
- `void setDepthStencilBuffer(QRhiRenderBuffer *renderBuffer)`
- `void setDepthTexture(QRhiTexture *texture)`
- `(since 6.9) void setShadingRateMap(QRhiShadingRateMap *map)`
- `(since 6.9) QRhiShadingRateMap * shadingRateMap() const`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `[constexpr noexcept] QRhiTextureRenderTargetDescription::QRhiTextureRenderTargetDescription()`

**作用与语义：**

构建一个空的纹理渲染目标描述。

### `QRhiTextureRenderTargetDescription::QRhiTextureRenderTargetDescription(const QRhiColorAttachment &colorAttachment)`

**作用与语义：**

构建一个纹理渲染目标描述，包含`colorAttachment`描述的一个附件。

### `QRhiTextureRenderTargetDescription::QRhiTextureRenderTargetDescription(const QRhiColorAttachment &colorAttachment, QRhiRenderBuffer *depthStencilBuffer)`

**作用与语义：**

构建带有两个附件的纹理渲染目标描述，颜色附件由`colorAttachment`描述，以及深度/模板附件，带`depthStencilBuffer`。

### `QRhiTextureRenderTargetDescription::QRhiTextureRenderTargetDescription(const QRhiColorAttachment &colorAttachment, QRhiTexture *depthTexture)`

**作用与语义：**

构建带有两个附件的纹理渲染目标描述，颜色附件由`colorAttachment`描述，深度附件由`depthTexture`描述。
注意：`depthTexture`必须有合适的格式，比如 `QRhiTexture::D16` 或 `QRhiTexture::D32F`。

### `const QRhiColorAttachment *QRhiTextureRenderTargetDescription::cbeginColorAttachments() const`

**作用与语义：**

返回指向附件列表中第一个项的const迭代子。

### `const QRhiColorAttachment *QRhiTextureRenderTargetDescription::cendColorAttachments() const`

**作用与语义：**

返回一个 const 迭代器，指向附件列表中最后一个项目之后。

### `const QRhiColorAttachment *QRhiTextureRenderTargetDescription::colorAttachmentAt(qsizetype index) const`

**作用与语义：**

返回指定 `index` 的颜色附件。

### `qsizetype QRhiTextureRenderTargetDescription::colorAttachmentCount() const`

**作用与语义：**

返回当前设置的颜色附件数量。

### `[since 6.8] QRhiTexture *QRhiTextureRenderTargetDescription::depthResolveTexture() const`

**作用与语义：**

返回多采样深度（或深度模板）纹理（或纹理数组）解析的纹理。`nullptr`如果没有纹理，这是最常见的情况。

### `QRhiRenderBuffer *QRhiTextureRenderTargetDescription::depthStencilBuffer() const`

**作用与语义：**

返回用作深度模板缓冲区的渲染缓冲区，若未设置则返回`nullptr`。

### `QRhiTexture *QRhiTextureRenderTargetDescription::depthTexture() const`

**作用与语义：**

返回当前参考的深度纹理，如果没有设置，则返回`nullptr`。

### `void QRhiTextureRenderTargetDescription::setColorAttachments(std::initializer_list<QRhiColorAttachment> list)`

**作用与语义：**

设置颜色附件的安装`list`。

### `template <typename InputIterator> void QRhiTextureRenderTargetDescription::setColorAttachments(InputIterator first, InputIterator last)`

**作用与语义：**

通过迭代器 `first` 和 `last` 设置颜色附件列表。

### `[since 6.8] void QRhiTextureRenderTargetDescription::setDepthResolveTexture(QRhiTexture *tex)`

**作用与语义：**

设置深度（或深度模板）分辨率纹理`tex`。
`tex`通常是一个二维纹理或二维纹理数组，其格式与纹理集通过`setDepthTexture()`匹配。
注意：解析深度（或深度模板）数据只有在运行时报告支持`QRhi::ResolveDepthStencil`功能时才可行。深度模板解析并非图形API中普遍支持。因此，假设深度模板解析无条件可用的设计是不可移植的，应避免使用。
注意：作为 OpenGL ES 的额外限制，设置深度解析纹理可能只能与 `setDepthTexture()` 结合使用，而不能与 `setDepthStencilBuffer()` 结合。

### `void QRhiTextureRenderTargetDescription::setDepthStencilBuffer(QRhiRenderBuffer *renderBuffer)`

**作用与语义：**

设置深度模板的`renderBuffer`。不是强制的，例如当该渲染目标的任何渲染通道中没有使用深度测试/写入或模板相关功能时，可以保持为`nullptr`。
注意：`depthStencilBuffer()` 和 `depthTexture()` 不能同时被集合（不能同时非零）。
使用`QRhiRenderBuffer`代替二维`QRhiTexture`作为深度或深度/模板缓冲区非常常见，也是应用推荐的方法。使用`setDepthTexture()` `QRhiTexture`，因此如果深度数据需要事后访问（例如在着色器中采样），或者涉及多视图渲染（因为深度纹理必须是纹理数组），使用就变得相关。

### `void QRhiTextureRenderTargetDescription::setDepthTexture(QRhiTexture *texture)`

**作用与语义：**

设置深度模板的`texture`。这是`setDepthStencilBuffer()`的替代方案，后者提供一个具有合适类型（例如`QRhiTexture::D32F`）的`QRhiTexture`代替`QRhiRenderBuffer`。
注意：`depthStencilBuffer()` 和 `depthTexture()` 不能同时被设定（也不能同时非空的）。
`texture`可以是2D纹理，也可以是2D纹理数组（当纹理数组支持时）。指定纹理数组在多视图渲染中尤为重要。
注意：如果`texture`格式包含模板组件，如`QRhiTexture::D24S8`，它也将作为模板缓冲区。

### `[since 6.9] void QRhiTextureRenderTargetDescription::setShadingRateMap(QRhiShadingRateMap *map)`

**作用与语义：**

与指定的`QRhiShadingRateMap` `map`关联。只有当`QRhi::VariableRateShadingMap`功能被报告为支持时，这才有效。
当`QRhiCommandBuffer::setShadingRate()`也被调用时，每个图块使用较高的着色率。目前无法控制组合器行为。
注意：当渲染目标已经构建完成（create() 成功调用时），设置着色率映射意味着需要一个新的 `QRhiRenderPassDescriptor`，因此需要重建。再次调用 setRenderPassDescriptor()（渲染过程外），然后通过调用 create()重建。这还会产生其他滚动后果，例如图形管线：这些也需要与新`QRhiRenderPassDescriptor`关联，然后重建。请参见`QRhiRenderPassDescriptor::serializedFormat()`，了解一些处理建议。记得也要设置 `QRhiGraphicsPipeline::UsesShadingRate` 标志。

### `[since 6.9] QRhiShadingRateMap *QRhiTextureRenderTargetDescription::shadingRateMap() const`

**作用与语义：**

返回当前设置的`QRhiShadingRateMap`。默认情况下，这是`nullptr`。

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

`QRhiTextureRenderTargetDescription` 所属机制类型：Qt 类型机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
