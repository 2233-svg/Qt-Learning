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

这里直接说明每个公开成员解决什么问题、参数代表什么、返回什么、会改变什么以及使用时容易出现什么问题。每一个公开签名都会有对应的中文解释。

本类共整理 18 个公开成员条目；没有独立长描述的 API 也会根据签名、类型和所属机制给出使用说明。

### `[constexpr noexcept] QRhiTextureRenderTargetDescription::QRhiTextureRenderTargetDescription()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QRhiTextureRenderTargetDescription` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QRhiTextureRenderTargetDescription::QRhiTextureRenderTargetDescription(const QRhiColorAttachment &colorAttachment)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QRhiTextureRenderTargetDescription` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `colorAttachment`：类型为 `const QRhiColorAttachment &`。没有默认值，调用时必须提供。传入 `const QRhiColorAttachment &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QRhiTextureRenderTargetDescription::QRhiTextureRenderTargetDescription(const QRhiColorAttachment &colorAttachment, QRhiRenderBuffer *depthStencilBuffer)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QRhiTextureRenderTargetDescription` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `colorAttachment`：类型为 `const QRhiColorAttachment &`。没有默认值，调用时必须提供。传入 `const QRhiColorAttachment &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `depthStencilBuffer`：类型为 `QRhiRenderBuffer *`。没有默认值，调用时必须提供。传入 `QRhiRenderBuffer *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QRhiTextureRenderTargetDescription::QRhiTextureRenderTargetDescription(const QRhiColorAttachment &colorAttachment, QRhiTexture *depthTexture)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QRhiTextureRenderTargetDescription` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `colorAttachment`：类型为 `const QRhiColorAttachment &`。没有默认值，调用时必须提供。传入 `const QRhiColorAttachment &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `depthTexture`：类型为 `QRhiTexture *`。没有默认值，调用时必须提供。传入 `QRhiTexture *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `const QRhiColorAttachment *QRhiTextureRenderTargetDescription::cbeginColorAttachments() const`

**API 类别：** 成员函数说明

**中文解读：** `QRhiTextureRenderTargetDescription::cbeginColorAttachments` 用于计算、查询或取得与“cbegin、Color、Attachments”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `const QRhiColorAttachment *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`const QRhiColorAttachment *`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `const QRhiColorAttachment *QRhiTextureRenderTargetDescription::cendColorAttachments() const`

**API 类别：** 成员函数说明

**中文解读：** `QRhiTextureRenderTargetDescription::cendColorAttachments` 用于计算、查询或取得与“cend、Color、Attachments”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `const QRhiColorAttachment *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`const QRhiColorAttachment *`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `const QRhiColorAttachment *QRhiTextureRenderTargetDescription::colorAttachmentAt(qsizetype index) const`

**API 类别：** 成员函数说明

**中文解读：** `QRhiTextureRenderTargetDescription::colorAttachmentAt` 用于计算、查询或取得与“color、Attachment、按位置访问”相关的操作。调用时要先确认当前状态和 `index` 的有效范围；返回类型是 `const QRhiColorAttachment *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`const QRhiColorAttachment *`。
- 参数 `index`：类型为 `qsizetype`。没有默认值，调用时必须提供。项目或数据索引。先确认索引基于 0 还是 1、是否允许越界/负数，以及调用后索引是否仍然有效。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `qsizetype QRhiTextureRenderTargetDescription::colorAttachmentCount() const`

**API 类别：** 成员函数说明

**中文解读：** `QRhiTextureRenderTargetDescription::colorAttachmentCount` 用于计算、查询或取得与“color、Attachment、数量统计”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `qsizetype`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`qsizetype`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.8] QRhiTexture *QRhiTextureRenderTargetDescription::depthResolveTexture() const`

**API 类别：** 成员函数说明

**中文解读：** `QRhiTextureRenderTargetDescription::depthResolveTexture` 用于计算、查询或取得与“depth、Resolve、Texture”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QRhiTexture *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QRhiTexture *`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QRhiRenderBuffer *QRhiTextureRenderTargetDescription::depthStencilBuffer() const`

**API 类别：** 成员函数说明

**中文解读：** `QRhiTextureRenderTargetDescription::depthStencilBuffer` 用于计算、查询或取得与“depth、Stencil、Buffer”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QRhiRenderBuffer *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QRhiRenderBuffer *`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QRhiTexture *QRhiTextureRenderTargetDescription::depthTexture() const`

**API 类别：** 成员函数说明

**中文解读：** `QRhiTextureRenderTargetDescription::depthTexture` 用于计算、查询或取得与“depth、Texture”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QRhiTexture *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QRhiTexture *`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QRhiTextureRenderTargetDescription::setColorAttachments(std::initializer_list<QRhiColorAttachment> list)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setColorAttachments`。调用它会改变 `QRhiTextureRenderTargetDescription` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `list`：类型为 `std::initializer_list<QRhiColorAttachment>`。没有默认值，调用时必须提供。传入 `std::initializer_list<QRhiColorAttachment>` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `template <typename InputIterator> void QRhiTextureRenderTargetDescription::setColorAttachments(InputIterator first, InputIterator last)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setColorAttachments`。调用它会改变 `QRhiTextureRenderTargetDescription` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`template <typename InputIterator> void`。
- 参数 `first`：类型为 `InputIterator`。没有默认值，调用时必须提供。传入 `InputIterator` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `last`：类型为 `InputIterator`。没有默认值，调用时必须提供。传入 `InputIterator` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.8] void QRhiTextureRenderTargetDescription::setDepthResolveTexture(QRhiTexture *tex)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setDepthResolveTexture`。调用它会改变 `QRhiTextureRenderTargetDescription` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `tex`：类型为 `QRhiTexture *`。没有默认值，调用时必须提供。传入 `QRhiTexture *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QRhiTextureRenderTargetDescription::setDepthStencilBuffer(QRhiRenderBuffer *renderBuffer)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setDepthStencilBuffer`。调用它会改变 `QRhiTextureRenderTargetDescription` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `renderBuffer`：类型为 `QRhiRenderBuffer *`。没有默认值，调用时必须提供。传入 `QRhiRenderBuffer *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QRhiTextureRenderTargetDescription::setDepthTexture(QRhiTexture *texture)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setDepthTexture`。调用它会改变 `QRhiTextureRenderTargetDescription` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `texture`：类型为 `QRhiTexture *`。没有默认值，调用时必须提供。传入 `QRhiTexture *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.9] void QRhiTextureRenderTargetDescription::setShadingRateMap(QRhiShadingRateMap *map)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setShadingRateMap`。调用它会改变 `QRhiTextureRenderTargetDescription` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `map`：类型为 `QRhiShadingRateMap *`。没有默认值，调用时必须提供。传入 `QRhiShadingRateMap *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.9] QRhiShadingRateMap *QRhiTextureRenderTargetDescription::shadingRateMap() const`

**API 类别：** 成员函数说明

**中文解读：** `QRhiTextureRenderTargetDescription::shadingRateMap` 用于计算、查询或取得与“shading、Rate、映射”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QRhiShadingRateMap *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QRhiShadingRateMap *`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

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
