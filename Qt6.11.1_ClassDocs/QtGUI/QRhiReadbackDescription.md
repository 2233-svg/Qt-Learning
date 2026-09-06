# QRhiReadbackDescription

> Qt 6.11.1 · Qt GUI

## 1. 先建立直觉

**一句话定位：** 这是 GUI 基础类型，常用于绘制、输入、图像、字体或窗口系统集成。

**模块背景：** Qt GUI 负责窗口系统集成、绘制、颜色、字体、图像、输入事件和底层 GUI 资源。

### 这是什么

`QRhiReadbackDescription` 是 Qt 类型机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

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

- `QRhiReadbackDescription()`
- `QRhiReadbackDescription(QRhiTexture *texture)`
- `int layer() const`
- `int level() const`
- `(since 6.10) QRect rect() const`
- `void setLayer(int layer)`
- `void setLevel(int level)`
- `(since 6.10) void setRect(const QRect &rectangle)`
- `void setTexture(QRhiTexture *tex)`
- `QRhiTexture * texture() const`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `[constexpr noexcept] QRhiReadbackDescription::QRhiReadbackDescription()`

**作用与语义：**

构建一个空的纹理读回描述。
注意：源纹理默认为空，这仍然是有效的回读：它指定要读取当前交换链的回缓冲区。（当前指的是提交带有纹理回读时帧目标交换`QRhiResourceUpdateBatch`链的目标交换链）。

### `QRhiReadbackDescription::QRhiReadbackDescription(QRhiTexture *texture)`

**作用与语义：**

构建一个纹理读回描述，指定要读回`texture`第0层的0级。
注意：`texture`也可以是空的，此时该构造函数与无参数变体相同。

### `int QRhiReadbackDescription::layer() const`

**作用与语义：**

返回当前设置的数组图层（立方体映射面，数组索引）。默认值为0。
仅适用于读取源为`QRhiTexture`时。

### `int QRhiReadbackDescription::level() const`

**作用与语义：**

返回当前设置的MIP电平。默认为0。
仅适用于读取源为`QRhiTexture`时。

### `[since 6.10] QRect QRhiReadbackDescription::rect() const`

**作用与语义：**

返回矩形以返回读取。默认为无效矩形。
如果无效，则会读取整个纹理或交换链回缓冲区。

### `void QRhiReadbackDescription::setLayer(int layer)`

**作用与语义：**

设置数组`layer`读取回传。

### `void QRhiReadbackDescription::setLevel(int level)`

**作用与语义：**

设置 mip `level` 来读取。

### `[since 6.10] void QRhiReadbackDescription::setRect(const QRect &rectangle)`

**作用与语义：**

设置回读的 `rectangle`。

### `void QRhiReadbackDescription::setTexture(QRhiTexture *tex)`

**作用与语义：**

将纹理`tex`设置为回读操作的源。
设置`nullptr`也是有效的，此时使用当前掉期链的当前回缓冲区。（但此时读回不能在非基于掉期链的帧中发出）。
注意：多采样纹理无法被读取。不过，多采样交换链缓冲区支持回读。
注意：读回中使用的纹理必须用`QRhiTexture::UsedAsTransferSource`创建。
注意：用于阅读回溯的交换链必须用`QRhiSwapChain::UsedAsTransferSource`创建。

### `QRhiTexture *QRhiReadbackDescription::texture() const`

**作用与语义：**

返回被读取的`QRhiTexture`。可以设置为`nullptr`，表示将使用当前掉期链的回缓冲区。

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

`QRhiReadbackDescription` 所属机制类型：Qt 类型机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
