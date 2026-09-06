# QRhiSampler

> Qt 6.11.1 · Qt GUI

## 1. 先建立直觉

**一句话定位：** 这是 GUI 基础类型，常用于绘制、输入、图像、字体或窗口系统集成。

**模块背景：** Qt GUI 负责窗口系统集成、绘制、颜色、字体、图像、输入事件和底层 GUI 资源。

### 这是什么

`QRhiSampler` 是 Qt 类型机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

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

- `enum AddressMode { Repeat, ClampToEdge, Mirror }`
- `enum CompareOp { Never, Less, Equal, LessOrEqual, Greater, …, Always }`
- `enum Filter { None, Nearest, Linear }`

### 公有函数

- `QRhiSampler::AddressMode addressU() const`
- `QRhiSampler::AddressMode addressV() const`
- `QRhiSampler::AddressMode addressW() const`
- `QRhiSampler::Filter magFilter() const`
- `QRhiSampler::Filter minFilter() const`
- `QRhiSampler::Filter mipmapMode() const`
- `void setAddressU(QRhiSampler::AddressMode mode)`
- `void setAddressV(QRhiSampler::AddressMode mode)`
- `void setAddressW(QRhiSampler::AddressMode mode)`
- `void setMagFilter(QRhiSampler::Filter f)`
- `void setMinFilter(QRhiSampler::Filter f)`
- `void setMipmapMode(QRhiSampler::Filter f)`
- `void setTextureCompareOp(QRhiSampler::CompareOp op)`
- `QRhiSampler::CompareOp textureCompareOp() const`

### 重实现的公有函数

- `virtual QRhiResource::Type resourceType() const override`

## 5. API 逐个说明

这里直接说明每个公开成员解决什么问题、参数代表什么、返回什么、会改变什么以及使用时容易出现什么问题。每一个公开签名都会有对应的中文解释。

本类共整理 18 个公开成员条目；没有独立长描述的 API 也会根据签名、类型和所属机制给出使用说明。

### `enum QRhiSampler::AddressMode`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QRhiSampler` 暴露的类型声明 `Address、模式`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 属性类型：`:AddressMode`。
- 属性名：`QRhiSampler`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `enum QRhiSampler::CompareOp`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QRhiSampler` 暴露的类型声明 `比较、Op`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 属性类型：`:CompareOp`。
- 属性名：`QRhiSampler`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `enum QRhiSampler::Filter`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QRhiSampler` 暴露的类型声明 `Filter`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 属性类型：`:Filter`。
- 属性名：`QRhiSampler`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QRhiSampler::AddressMode QRhiSampler::addressU() const`

**API 类别：** 成员函数说明

**中文解读：** 这是向 `QRhiSampler` 添加依赖、数据或子对象的 API `addressU`。注意对象所有权、重复添加和添加后的通知；如果对应有 remove/take 接口，要明确谁负责移除后的生命周期。

**签名拆解：**

- 返回值：`QRhiSampler::AddressMode`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QRhiSampler::AddressMode QRhiSampler::addressV() const`

**API 类别：** 成员函数说明

**中文解读：** 这是向 `QRhiSampler` 添加依赖、数据或子对象的 API `addressV`。注意对象所有权、重复添加和添加后的通知；如果对应有 remove/take 接口，要明确谁负责移除后的生命周期。

**签名拆解：**

- 返回值：`QRhiSampler::AddressMode`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QRhiSampler::AddressMode QRhiSampler::addressW() const`

**API 类别：** 成员函数说明

**中文解读：** 这是向 `QRhiSampler` 添加依赖、数据或子对象的 API `addressW`。注意对象所有权、重复添加和添加后的通知；如果对应有 remove/take 接口，要明确谁负责移除后的生命周期。

**签名拆解：**

- 返回值：`QRhiSampler::AddressMode`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QRhiSampler::Filter QRhiSampler::magFilter() const`

**API 类别：** 成员函数说明

**中文解读：** `QRhiSampler::magFilter` 用于计算、查询或取得与“mag、Filter”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QRhiSampler::Filter`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QRhiSampler::Filter`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QRhiSampler::Filter QRhiSampler::minFilter() const`

**API 类别：** 成员函数说明

**中文解读：** `QRhiSampler::minFilter` 用于计算、查询或取得与“min、Filter”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QRhiSampler::Filter`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QRhiSampler::Filter`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QRhiSampler::Filter QRhiSampler::mipmapMode() const`

**API 类别：** 成员函数说明

**中文解读：** `QRhiSampler::mipmapMode` 用于计算、查询或取得与“mipmap、模式”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QRhiSampler::Filter`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QRhiSampler::Filter`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual] QRhiResource::Type QRhiSampler::resourceType() const`

**API 类别：** 成员函数说明

**中文解读：** `QRhiSampler::resourceType` 用于计算、查询或取得与“resource、类型”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QRhiResource::Type`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QRhiResource::Type`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QRhiSampler::setAddressU(QRhiSampler::AddressMode mode)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setAddressU`。调用它会改变 `QRhiSampler` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `mode`：类型为 `QRhiSampler::AddressMode`。没有默认值，调用时必须提供。模式枚举或位标志。它通常决定对象后续允许的操作和状态转换。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QRhiSampler::setAddressV(QRhiSampler::AddressMode mode)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setAddressV`。调用它会改变 `QRhiSampler` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `mode`：类型为 `QRhiSampler::AddressMode`。没有默认值，调用时必须提供。模式枚举或位标志。它通常决定对象后续允许的操作和状态转换。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QRhiSampler::setAddressW(QRhiSampler::AddressMode mode)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setAddressW`。调用它会改变 `QRhiSampler` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `mode`：类型为 `QRhiSampler::AddressMode`。没有默认值，调用时必须提供。模式枚举或位标志。它通常决定对象后续允许的操作和状态转换。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QRhiSampler::setMagFilter(QRhiSampler::Filter f)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setMagFilter`。调用它会改变 `QRhiSampler` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `f`：类型为 `QRhiSampler::Filter`。没有默认值，调用时必须提供。传入 `QRhiSampler::Filter` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QRhiSampler::setMinFilter(QRhiSampler::Filter f)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setMinFilter`。调用它会改变 `QRhiSampler` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `f`：类型为 `QRhiSampler::Filter`。没有默认值，调用时必须提供。传入 `QRhiSampler::Filter` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QRhiSampler::setMipmapMode(QRhiSampler::Filter f)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setMipmapMode`。调用它会改变 `QRhiSampler` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `f`：类型为 `QRhiSampler::Filter`。没有默认值，调用时必须提供。传入 `QRhiSampler::Filter` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QRhiSampler::setTextureCompareOp(QRhiSampler::CompareOp op)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setTextureCompareOp`。调用它会改变 `QRhiSampler` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `op`：类型为 `QRhiSampler::CompareOp`。没有默认值，调用时必须提供。传入 `QRhiSampler::CompareOp` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QRhiSampler::CompareOp QRhiSampler::textureCompareOp() const`

**API 类别：** 成员函数说明

**中文解读：** `QRhiSampler::textureCompareOp` 用于计算、查询或取得与“texture、比较、Op”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QRhiSampler::CompareOp`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QRhiSampler::CompareOp`。
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

`QRhiSampler` 所属机制类型：Qt 类型机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
