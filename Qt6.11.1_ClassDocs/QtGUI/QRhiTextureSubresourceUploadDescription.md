# QRhiTextureSubresourceUploadDescription

> Qt 6.11.1 · Qt GUI

## 1. 先建立直觉

**一句话定位：** 这是 GUI 基础类型，常用于绘制、输入、图像、字体或窗口系统集成。

**模块背景：** Qt GUI 负责窗口系统集成、绘制、颜色、字体、图像、输入事件和底层 GUI 资源。

### 这是什么

`QRhiTextureSubresourceUploadDescription` 是 Qt 类型机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

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

- `QRhiTextureSubresourceUploadDescription()`
- `QRhiTextureSubresourceUploadDescription(const QByteArray &data)`
- `QRhiTextureSubresourceUploadDescription(const QImage &image)`
- `QRhiTextureSubresourceUploadDescription(const void *data, quint32 size)`
- `QByteArray data() const`
- `quint32 dataStride() const`
- `QPoint destinationTopLeft() const`
- `QImage image() const`
- `void setData(const QByteArray &data)`
- `void setDataStride(quint32 stride)`
- `void setDestinationTopLeft(const QPoint &p)`
- `void setImage(const QImage &image)`
- `void setSourceSize(const QSize &size)`
- `void setSourceTopLeft(const QPoint &p)`
- `QSize sourceSize() const`
- `QPoint sourceTopLeft() const`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `[noexcept] QRhiTextureSubresourceUploadDescription::QRhiTextureSubresourceUploadDescription()`

**作用与语义：**

构建一个空的子资源描述。
注意：空的 QRhiTextureSubresourceUploadDescription 单独无用，不应提交给`QRhiTextureUploadEntry`。至少必须先设置图像或数据。

### `[explicit] QRhiTextureSubresourceUploadDescription::QRhiTextureSubresourceUploadDescription(const QByteArray &data)`

**作用与语义：**

用`data`指定的图像数据构建MIP级描述。这也适用于浮点和压缩格式。

### `[explicit] QRhiTextureSubresourceUploadDescription::QRhiTextureSubresourceUploadDescription(const QImage &image)`

**作用与语义：**

构建一个带有`image`的MIP级描述。
`image` 的 `size`必须与 mip 级别的大小相匹配。对于 level 0，那就是纹理大小。
`image`的位深必须与纹理格式兼容。
关于部分上传，请在之后打电话`setSourceSize()`、`setSourceTopLeft()`或`setDestinationTopLeft()`。

### `QRhiTextureSubresourceUploadDescription::QRhiTextureSubresourceUploadDescription(const void *data, quint32 size)`

**作用与语义：**

构建一个由`data`和`size`指定的图像数据的MIP级描述。这也适用于浮点和压缩格式。
`data`功能恢复后可以安全地销毁或更改。

### `QByteArray QRhiTextureSubresourceUploadDescription::data() const`

**作用与语义：**

返回当前设置的原始像素数据。

### `quint32 QRhiTextureSubresourceUploadDescription::dataStride() const`

**作用与语义：**

返回当前设置的数据步幅。

### `QPoint QRhiTextureSubresourceUploadDescription::destinationTopLeft() const`

**作用与语义：**

返回当前设置的目标左上角位置。默认为（0， 0）。

### `QImage QRhiTextureSubresourceUploadDescription::image() const`

**作用与语义：**

返回当前设定的`QImage`。

### `void QRhiTextureSubresourceUploadDescription::setData(const QByteArray &data)`

**作用与语义：**

`data`。
注意：`image()`和`data()`不能同时设置。

### `void QRhiTextureSubresourceUploadDescription::setDataStride(quint32 stride)`

**作用与语义：**

将数据`stride`设置为字节。默认情况下，这个数值为0，且并不总是相关。当提供原始的 `data()`，且步幅未通过 setDataStride() 指定时，所提供数据的步幅（行的音高，行长（字节单位）必须等于 `width * pixelSize`，其中 `pixelSize` 是每个像素所用的字节数，行之间不得有额外的填充。否则，如果行间有额外空格，则设置非零的 `stride`。所有这些仅适用于提供原始图像数据时，且在工作`QImage`时不必要，因为原始数据本身具有`stride`价值。
注意：通过 setDataStride() 设置步进仅在报告为`supported`时`QRhi::ImageDataStride`才有效。
注意：当给出`QImage`时，`QImage::bytesPerLine()`返回的步长会自动被考虑，因此无需手动设置数据步幅。

### `void QRhiTextureSubresourceUploadDescription::setDestinationTopLeft(const QPoint &p)`

**作用与语义：**

将目的地设置在左上角的位置`p`。
注意：在从`QImage`获取图像数据最常见的情况下，当目标位置的源尺寸大于目标纹理子资源大小（即给定的MIP级别大小）时，Qt会对无效纹理上传大小进行夹持。在这种情况下，调试输出上还会印有`qWarning()`消息。这样做是为了避免在底层3D API崩溃时产生混淆，导致后续提交命令时GPU设备被移除。无论如何，开发者被鼓励始终启用Vulkan、D3D12或Metal验证/调试层来验证应用程序，因为这些层对API使用进行了更广泛的检查。

### `void QRhiTextureSubresourceUploadDescription::setImage(const QImage &image)`

**作用与语义：**

设置`image`。在纹理加载时，图像数据将被原样读取，不会进行格式转换。
注意：`image()`和`data()`不能同时设置。

### `void QRhiTextureSubresourceUploadDescription::setSourceSize(const QSize &size)`

**作用与语义：**

将源码设置成像素`size`。
注意：根据格式和后端，设置`sourceSize()`或`sourceTopLeft()`可能会在内部触发`QImage`副本。

### `void QRhiTextureSubresourceUploadDescription::setSourceTopLeft(const QPoint &p)`

**作用与语义：**

将源头左上角的位置设为`p`。
注意：设置`sourceSize()`或`sourceTopLeft()`可能会在内部触发`QImage`副本，具体取决于格式和后端。

### `QSize QRhiTextureSubresourceUploadDescription::sourceSize() const`

**作用与语义：**

返回以像素为单位的源尺寸。默认为默认构造的`QSize`，表示整个子资源。

### `QPoint QRhiTextureSubresourceUploadDescription::sourceTopLeft() const`

**作用与语义：**

返回当前设置的左上角源位置。默认为（0， 0）。

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

`QRhiTextureSubresourceUploadDescription` 所属机制类型：Qt 类型机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
