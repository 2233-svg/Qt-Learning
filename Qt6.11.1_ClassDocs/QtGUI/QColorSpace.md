# QColorSpace

> Qt 6.11.1 · Qt GUI

## 1. 先建立直觉

**一句话定位：** 这是 GUI 基础类型，常用于绘制、输入、图像、字体或窗口系统集成。

**模块背景：** Qt GUI 负责窗口系统集成、绘制、颜色、字体、图像、输入事件和底层 GUI 资源。

### 这是什么

`QColorSpace` 是 Qt 类型机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 这个类的行为由它的继承关系、构造参数、公开状态和成员函数协议共同决定。使用时要把创建、配置、核心操作、结果/通知和清理看成一条闭环，而不是孤立调用某个函数。

**适用场景：** 围绕这个类的核心职责建立最小闭环：准备依赖 -> 创建/取得对象 -> 设置必要配置 -> 调用核心 API -> 检查返回值和状态 -> 处理结果/错误 -> 结束时清理。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要忽略构造失败、空返回、默认值和版本限制；不要把异步 API 当同步 API；不要在没有确认所有权和线程的情况下保存指针或跨线程调用。

## 2. 依赖与对象关系

- 头文件：`#include <QColorSpace>`
- 继承自：未在类页中列出
- 直接派生类：未在类页中列出

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Gui)
target_link_libraries(mytarget PRIVATE Qt6::Gui)
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

- `(since 6.9) struct PrimaryPoints`
- `(since 6.8) enum class ColorModel { Undefined, Rgb, Gray, Cmyk }`
- `enum NamedColorSpace { SRgb, SRgbLinear, AdobeRgb, DisplayP3, ProPhotoRgb, …, Bt2100Hlg }`
- `enum class Primaries { Custom, SRgb, AdobeRgb, DciP3D65, ProPhotoRgb, Bt2020 }`
- `enum class TransferFunction { Custom, Linear, Gamma, SRgb, ProPhotoRgb, …, Hlg }`
- `(since 6.8) enum class TransformModel { ThreeComponentMatrix, ElementListProcessing }`

### 公有函数

- `QColorSpace()`
- `QColorSpace(QColorSpace::NamedColorSpace namedColorSpace)`
- `(since 6.1) QColorSpace(QColorSpace::Primaries gamut, const QList<uint16_t> &transferFunctionTable)`
- `QColorSpace(QColorSpace::Primaries primaries, float gamma)`
- `(since 6.8) QColorSpace(QPointF whitePoint, const QList<uint16_t> &transferFunctionTable)`
- `QColorSpace(QColorSpace::Primaries primaries, QColorSpace::TransferFunction transferFunction, float gamma = 0.0f)`
- `(since 6.8) QColorSpace(QPointF whitePoint, QColorSpace::TransferFunction transferFunction, float gamma = 0.0f)`
- `(since 6.9) QColorSpace(const QColorSpace::PrimaryPoints &primaryPoints, QColorSpace::TransferFunction transferFunction, float gamma = 0.0f)`
- `(since 6.1) QColorSpace(const QPointF &whitePoint, const QPointF &redPoint, const QPointF &greenPoint, const QPointF &bluePoint, const QList<uint16_t> &transferFunctionTable)`
- `QColorSpace(const QPointF &whitePoint, const QPointF &redPoint, const QPointF &greenPoint, const QPointF &bluePoint, QColorSpace::TransferFunction transferFunction, float gamma = 0.0f)`
- `(since 6.1) QColorSpace(const QPointF &whitePoint, const QPointF &redPoint, const QPointF &greenPoint, const QPointF &bluePoint, const QList<uint16_t> &redTransferFunctionTable, const QList<uint16_t> &greenTransferFunctionTable, const QList<uint16_t> &blueTransferFunctionTable)`
- `(since 6.8) QColorSpace::ColorModel colorModel() const`
- `(since 6.2) QString description() const`
- `float gamma() const`
- `QByteArray iccProfile() const`
- `bool isValid() const`
- `(since 6.8) bool isValidTarget() const`
- `QColorSpace::Primaries primaries() const`
- `(since 6.9) QColorSpace::PrimaryPoints primaryPoints() const`
- `(since 6.2) void setDescription(const QString &description)`
- `void setPrimaries(QColorSpace::Primaries primariesId)`
- `void setPrimaries(const QPointF &whitePoint, const QPointF &redPoint, const QPointF &greenPoint, const QPointF &bluePoint)`
- `(since 6.9) void setPrimaryPoints(const QColorSpace::PrimaryPoints &primaryPoints)`
- `(since 6.1) void setTransferFunction(const QList<uint16_t> &transferFunctionTable)`
- `void setTransferFunction(QColorSpace::TransferFunction transferFunction, float gamma = 0.0f)`
- `(since 6.1) void setTransferFunctions(const QList<uint16_t> &redTransferFunctionTable, const QList<uint16_t> &greenTransferFunctionTable, const QList<uint16_t> &blueTransferFunctionTable)`
- `(since 6.8) void setWhitePoint(QPointF whitePoint)`
- `void swap(QColorSpace &other)`
- `QColorSpace::TransferFunction transferFunction() const`
- `(since 6.8) QColorSpace::TransformModel transformModel() const`
- `QColorTransform transformationToColorSpace(const QColorSpace &colorspace) const`
- `(since 6.8) QPointF whitePoint() const`
- `(since 6.1) QColorSpace withTransferFunction(const QList<uint16_t> &transferFunctionTable) const`
- `QColorSpace withTransferFunction(QColorSpace::TransferFunction transferFunction, float gamma = 0.0f) const`
- `(since 6.1) QColorSpace withTransferFunctions(const QList<uint16_t> &redTransferFunctionTable, const QList<uint16_t> &greenTransferFunctionTable, const QList<uint16_t> &blueTransferFunctionTable) const`
- `operator QVariant() const`

### 静态公有成员

- `QColorSpace fromIccProfile(const QByteArray &iccProfile)`

### 相关非成员函数

- `bool operator!=(const QColorSpace &colorSpace1, const QColorSpace &colorSpace2)`
- `QDataStream & operator<<(QDataStream &stream, const QColorSpace &colorSpace)`
- `bool operator==(const QColorSpace &colorSpace1, const QColorSpace &colorSpace2)`
- `QDataStream & operator>>(QDataStream &stream, QColorSpace &colorSpace)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `[since 6.8] enum class QColorSpace::ColorModel`

**作用与语义：**

定义色彩空间数据所使用的颜色模型。
- `QColorSpace::ColorModel::Undefined`：`0`;无彩色模型
- `QColorSpace::ColorModel::Rgb`：`1`;一个包含红色、绿色和蓝色的RGB色彩模型。可应用于RGB和灰度数据。
- `QColorSpace::ColorModel::Gray`：`2`;灰度色彩模型。只能应用于灰度数据。
- `QColorSpace::ColorModel::Cmyk`：`3`;只能表示由青色、品红、黄色和黑色定义的颜色数据。实际上仅有QImage：：Format_CMYK32。注意，Cmyk色彩空间将被`TransformModel::ElementListProcessing`。
这个枚举是在Qt 6.8引入的。

### `enum QColorSpace::NamedColorSpace`

**作用与语义：**

预定义的色彩空间。
- `QColorSpace::SRgb`：`1`;sRGB 色彩空间，Qt 默认在该色域中工作。它近似大多数经典显示器的工作方式，也是大多数软硬件支持的模式。sRGB 的 ICC 注册。
- `QColorSpace::SRgbLinear`：`2`;带有线性伽马的sRGB色彩空间。适用于伽马校正混合。
- `QColorSpace::AdobeRgb`：`3`;Adobe RGB 色彩空间是一种经典的宽色域色彩空间，采用 2.2 的伽马值。Adobe RGB 的 ICC 注册（1998）
- `QColorSpace::DisplayP3`：`4`;采用DCI-P3的原色，但白点和传递函数为sRGB。常见于现代广色域屏幕。DCI-P3的ICC注册
- `QColorSpace::ProPhotoRgb`：`5`;Pro Photo RGB 色彩空间，也称为 ROMM RGB，是一种非常宽色域的色彩空间。ICC 对 ROMM RGB 的配准
- `QColorSpace::Bt2020 (since Qt 6.8)`：`6`;BT.2020，也称为Rec.2020，是HDR电视的基本色域。BT.2020的ICC注册
- `QColorSpace::Bt2100Pq (since Qt 6.8)`：`7`;BT.2100（PQ），也称为Rec.2100或HDR10，是一种HDR编码，原色与Bt2020相同，但使用感知量化器传递函数。BT.2100的ICC注册
- `QColorSpace::Bt2100Hlg (since Qt 6.8)`：`8`;BT.2100（HLG）是一种HDR编码，主编码与Bt2020相同，但采用混合对数-伽马传递函数。

### `enum class QColorSpace::Primaries`

**作用与语义：**

预设的原色集合。
- `QColorSpace::Primaries::Custom`：`0`;这些初级是未定义的，或者与任何预定义的集合不匹配。
- `QColorSpace::Primaries::SRgb`：`1`;sRGB 初级
- `QColorSpace::Primaries::AdobeRgb`：`2`;Adobe RGB 主色
- `QColorSpace::Primaries::DciP3D65`：`3`;DCI-P3初选，采用D65白点灯
- `QColorSpace::Primaries::ProPhotoRgb`：`4`;ProPhoto RGB主色配D50白点
- `QColorSpace::Primaries::Bt2020 (since Qt 6.8)`：`5`;BT.2020主射器配备D65白点瞄准镜

### `enum class QColorSpace::TransferFunction`

**作用与语义：**

预定义的传递函数或伽马曲线。
- `QColorSpace::TransferFunction::Custom`：`0`;自定义或空传递函数
- `QColorSpace::TransferFunction::Linear`：`1`;线性传递函数
- `QColorSpace::TransferFunction::Gamma`：`2`;基于 的值的实伽马曲线传递函数`gamma()`
- `QColorSpace::TransferFunction::SRgb`：`3`;sRGB传递函数，由线性和伽马部分组成
- `QColorSpace::TransferFunction::ProPhotoRgb`：`4`;ProPhoto RGB传递函数，由线性和伽马部分组成
- `QColorSpace::TransferFunction::Bt2020 (since Qt 6.8)`：`5`;BT.2020传递函数，由线性和伽马部分组成
- `QColorSpace::TransferFunction::St2084 (since Qt 6.8)`：`6`;SMPTE ST 2084传递函数，也称为感知量子器（PQ）。
- `QColorSpace::TransferFunction::Hlg (since Qt 6.8)`：`7`;混合对数-伽马传递函数。

### `[since 6.8] enum class QColorSpace::TransformModel`

**作用与语义：**

定义用于色彩空间变换的处理模型。
- `QColorSpace::TransformModel::ThreeComponentMatrix`：`0`;变换由每个色道的主色和传递函数集合计算的矩阵组成。该矩阵速度非常快，适用于所有预定义色域。该形式上的任何色域均可逆，且始终有效且目标源均有效。
- `QColorSpace::TransformModel::ElementListProcessing`：`1`;变换是一两个处理元素列表，每个列表只能处理连接色彩空间或从连接色彩空间处理。这非常灵活，但速度较慢，只能通过读取ICC配置文件来设置（参见`fromIccProfile()`）。由于两个列表是分开的，该形式的颜色空间可以是有效的源，但不一定也是有效的目标。当该类型颜色空间的主色或传递函数时，颜色空间会重置为空的三分量矩阵形式。
这个枚举是在Qt 6.8引入的。

### `[constexpr noexcept] QColorSpace::QColorSpace()`

**作用与语义：**

创建一个新的色彩空间对象，表示一个未定义且无效的色彩空间。

### `QColorSpace::QColorSpace(QColorSpace::NamedColorSpace namedColorSpace)`

**作用与语义：**

创建一个新的色彩空间对象，代表一个`namedColorSpace`。

### `[since 6.1] QColorSpace::QColorSpace(QColorSpace::Primaries gamut, const QList<uint16_t> &transferFunctionTable)`

**作用与语义：**

使用`transferFunctionTable`描述的自定义传递函数，创建带有主色`gamut`的自定义色彩空间。
该表应至少包含两个值，并包含一个从0到65535单调递增的值列表。

### `QColorSpace::QColorSpace(QColorSpace::Primaries primaries, float gamma)`

**作用与语义：**

利用`gamma`的伽马传递函数创建带有主色的自定义色彩空间`primaries`。

### `[explicit, since 6.8] QColorSpace::QColorSpace(QPointF whitePoint, const QList<uint16_t> &transferFunctionTable)`

**作用与语义：**

创建带有白点`whitePoint`的自定义灰度色彩空间，并使用`transferFunctionTable`描述的自定义传递函数。

### `QColorSpace::QColorSpace(QColorSpace::Primaries primaries, QColorSpace::TransferFunction transferFunction, float gamma = 0.0f)`

**作用与语义：**

使用传递函数`transferFunction`创建带有主色`primaries`的自定义色彩空间，并可选择`gamma`。

### `[explicit, since 6.8] QColorSpace::QColorSpace(QPointF whitePoint, QColorSpace::TransferFunction transferFunction, float gamma = 0.0f)`

**作用与语义：**

利用传递函数`transferFunction`创建带有白点`whitePoint`的自定义灰阶色彩空间，可选择`gamma`。

### `[since 6.9] QColorSpace::QColorSpace(const QColorSpace::PrimaryPoints &primaryPoints, QColorSpace::TransferFunction transferFunction, float gamma = 0.0f)`

**作用与语义：**

基于`primaryPoints`原色的色度创建自定义色彩空间，使用传递函数`transferFunction`，可选择`gamma`。

### `[since 6.1] QColorSpace::QColorSpace(const QPointF &whitePoint, const QPointF &redPoint, const QPointF &greenPoint, const QPointF &bluePoint, const QList<uint16_t> &transferFunctionTable)`

**作用与语义：**

基于原色`whitePoint`、`redPoint`、`greenPoint`和`bluePoint`的色度，并使用`transferFunctionTable`描述的自定义传递函数，创建带有原色的自定义色彩空间。

### `QColorSpace::QColorSpace(const QPointF &whitePoint, const QPointF &redPoint, const QPointF &greenPoint, const QPointF &bluePoint, QColorSpace::TransferFunction transferFunction, float gamma = 0.0f)`

**作用与语义：**

基于原色`whitePoint`、`redPoint`、`greenPoint`和`bluePoint`的色度，并使用传递函数`transferFunction`，可选择`gamma`，创建自定义色彩空间。

### `[since 6.1] QColorSpace::QColorSpace(const QPointF &whitePoint, const QPointF &redPoint, const QPointF &greenPoint, const QPointF &bluePoint, const QList<uint16_t> &redTransferFunctionTable, const QList<uint16_t> &greenTransferFunctionTable, const QList<uint16_t> &blueTransferFunctionTable)`

**作用与语义：**

基于原色`whitePoint`、`redPoint`、`greenPoint`和`bluePoint`的色度，并使用`redTransferFunctionTable`、`greenTransferFunctionTable`和`blueTransferFunctionTable`描述的自定义传递函数，创建带有原色的自定义色彩空间。

### `[noexcept, since 6.8] QColorSpace::ColorModel QColorSpace::colorModel() const`

**作用与语义：**

返回该颜色空间能够表示的颜色模型。

### `[noexcept, since 6.2] QString QColorSpace::description() const`

**作用与语义：**

返回名称或简短描述。如果 `setDescription()` 中没有给出描述，若配置文件未修改，则返回原始配置文件名称;如果配置文件被识别为已知色彩空间，返回猜测名称;否则返回空字符串。

### `[static] QColorSpace QColorSpace::fromIccProfile(const QByteArray &iccProfile)`

**作用与语义：**

从ICC配置文件`iccProfile`创建`QColorSpace`。
注意：并非所有ICC配置文件都支持。`QColorSpace`只支持RGB或灰色ICC配置文件。
如果不支持ICC配置文件，会返回一个无效`QColorSpace`，你仍可以用`iccProfile()`读取原始ICC配置文件。

### `[noexcept] float QColorSpace::gamma() const`

**作用与语义：**

返回色彩空间的伽马值，`TransferFunction::Gamma`，是其他预定义色彩空间的近似伽马值，若无近似伽马则返回0.0。

### `QByteArray QColorSpace::iccProfile() const`

**作用与语义：**

返回一个代表色彩空间的ICC配置文件。
如果色彩空间是从ICC配置文件生成的，则返回该配置文件，否则生成一个配置文件。
注意：即使是无效色彩空间，如果它们是从某个颜色空间生成的，也可能返回ICC配置文件，以便应用程序自行实现更广泛的支持。

### `[noexcept] bool QColorSpace::isValid() const`

**作用与语义：**

如果颜色空间有效，返回`true`。对于颜色空间 ，`TransformModel::ThreeComponentMatrix` 表示主色和传递函数都设置为 ，并蕴含 `isValidTarget()`。对于色彩空间 `TransformModel::ElementListProcessing`，表示它有有效的源变换，检查它是否也是有效的目标色彩空间，可以使用`isValidTarget()`。

### `[noexcept, since 6.8] bool QColorSpace::isValidTarget() const`

**作用与语义：**

如果颜色空间是有效的目标颜色空间，返回`true`。

### `[noexcept] QColorSpace::Primaries QColorSpace::primaries() const`

**作用与语义：**

如果颜色空间或`primaries::Custom`与任何一个不匹配，则返回预定义的原色。

### `[since 6.9] QColorSpace::PrimaryPoints QColorSpace::primaryPoints() const`

**作用与语义：**

返回主色度，如果未定义，则返回零点。

### `[since 6.2] void QColorSpace::setDescription(const QString &description)`

**作用与语义：**

将颜色空间的名称或简短描述设置为`description`。
如果设置为空`description()`则返回原始或猜测的描述。

### `void QColorSpace::setPrimaries(QColorSpace::Primaries primariesId)`

**作用与语义：**

将初选设置为`primariesId`集的主选。

### `void QColorSpace::setPrimaries(const QPointF &whitePoint, const QPointF &redPoint, const QPointF &greenPoint, const QPointF &bluePoint)`

**作用与语义：**

将原色设定为`whitePoint`、`redPoint`、`greenPoint`和`bluePoint`的色度。

### `[since 6.9] void QColorSpace::setPrimaryPoints(const QColorSpace::PrimaryPoints &primaryPoints)`

**作用与语义：**

将所有原色设定为`primaryPoints`的色数。

### `[since 6.1] void QColorSpace::setTransferFunction(const QList<uint16_t> &transferFunctionTable)`

**作用与语义：**

将传递函数设为`transferFunctionTable`。

### `void QColorSpace::setTransferFunction(QColorSpace::TransferFunction transferFunction, float gamma = 0.0f)`

**作用与语义：**

将传递函数设置为`transferFunction`和 `gamma`。

### `[since 6.1] void QColorSpace::setTransferFunctions(const QList<uint16_t> &redTransferFunctionTable, const QList<uint16_t> &greenTransferFunctionTable, const QList<uint16_t> &blueTransferFunctionTable)`

**作用与语义：**

将传递函数设置为`redTransferFunctionTable`、`greenTransferFunctionTable`和 `blueTransferFunctionTable`。

### `[since 6.8] void QColorSpace::setWhitePoint(QPointF whitePoint)`

**作用与语义：**

将该色彩空间的白色点设置为`whitePoint`。

### `[noexcept] void QColorSpace::swap(QColorSpace &other)`

**作用与语义：**

将色彩空间与`other`交换。这个操作非常快，且从未失败。

### `[noexcept] QColorSpace::TransferFunction QColorSpace::transferFunction() const`

**作用与语义：**

如果颜色空间或`TransferFunction::Custom`不匹配，返回预定义的传递函数。

### `[noexcept, since 6.8] QColorSpace::TransformModel QColorSpace::transformModel() const`

**作用与语义：**

返回用于该色彩空间的transfrom处理模型。

### `QColorTransform QColorSpace::transformationToColorSpace(const QColorSpace &colorspace) const`

**作用与语义：**

生成并返回从该色彩空间到`colorspace`的色彩空间变换。

### `[since 6.8] QPointF QColorSpace::whitePoint() const`

**作用与语义：**

返回用于该色彩空间的白点。如果未定义，返回空`QPointF`。

### `[since 6.1] QColorSpace QColorSpace::withTransferFunction(const QList<uint16_t> &transferFunctionTable) const`

**作用与语义：**

返回该色彩空间的副本，但使用`transferFunctionTable`描述的传递函数。

### `QColorSpace QColorSpace::withTransferFunction(QColorSpace::TransferFunction transferFunction, float gamma = 0.0f) const`

**作用与语义：**

返回该色彩空间的副本，但使用传递函数`transferFunction`和`gamma`。

### `[since 6.1] QColorSpace QColorSpace::withTransferFunctions(const QList<uint16_t> &redTransferFunctionTable, const QList<uint16_t> &greenTransferFunctionTable, const QList<uint16_t> &blueTransferFunctionTable) const`

**作用与语义：**

返回该色彩空间的副本，但使用`redTransferFunctionTable`、`greenTransferFunctionTable`和`blueTransferFunctionTable`描述的传递函数。

### `QColorSpace::operator QVariant() const`

**作用与语义：**

返回色彩空间为`QVariant`。

### `bool operator!=(const QColorSpace &colorSpace1, const QColorSpace &colorSpace2)`

**作用与语义：**

如果色彩空间 `colorSpace1` 不等于色彩空间 `colorSpace2`，则返回 `true`；否则返回 `false`。

### `QDataStream &operator<<(QDataStream &stream, const QColorSpace &colorSpace)`

**作用与语义：**

将给定`colorSpace`写入给定`stream`，作为ICC配置文件。

### `bool operator==(const QColorSpace &colorSpace1, const QColorSpace &colorSpace2)`

**作用与语义：**

如果颜色空间 `colorSpace1` 等于颜色空间 `colorSpace2`，则返回 `true`；否则返回 `false`。

### `QDataStream &operator>>(QDataStream &stream, QColorSpace &colorSpace)`

**作用与语义：**

从给定`stream`读取色彩空间并将其存储在给定`colorSpace`中。

### `(since 6.9) struct PrimaryPoints`

**作用与语义：**

PrimaryPoints 结构包含四个原色空间点。
描述RGB色域的四个CIE XY色域点;红、绿、蓝、白。

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

`QColorSpace` 所属机制类型：Qt 类型机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
