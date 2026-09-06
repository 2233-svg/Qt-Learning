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

这里直接说明每个公开成员解决什么问题、参数代表什么、返回什么、会改变什么以及使用时容易出现什么问题。每一个公开签名都会有对应的中文解释。

本类共整理 47 个公开成员条目；没有独立长描述的 API 也会根据签名、类型和所属机制给出使用说明。

### `[since 6.8] enum class QColorSpace::ColorModel`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QColorSpace` 暴露的类型声明 `class`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 属性类型：`:ColorModel`。
- 属性名：`QColorSpace`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `enum QColorSpace::NamedColorSpace`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QColorSpace` 暴露的类型声明 `Named、Color、Space`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 属性类型：`:NamedColorSpace`。
- 属性名：`QColorSpace`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `enum class QColorSpace::Primaries`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QColorSpace` 暴露的类型声明 `class`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 属性类型：`:Primaries`。
- 属性名：`QColorSpace`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `enum class QColorSpace::TransferFunction`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QColorSpace` 暴露的类型声明 `class`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 属性类型：`:TransferFunction`。
- 属性名：`QColorSpace`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.8] enum class QColorSpace::TransformModel`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QColorSpace` 暴露的类型声明 `class`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 属性类型：`:TransformModel`。
- 属性名：`QColorSpace`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[constexpr noexcept] QColorSpace::QColorSpace()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QColorSpace` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QColorSpace::QColorSpace(QColorSpace::NamedColorSpace namedColorSpace)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QColorSpace` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `namedColorSpace`：类型为 `QColorSpace::NamedColorSpace`。没有默认值，调用时必须提供。传入 `QColorSpace::NamedColorSpace` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.1] QColorSpace::QColorSpace(QColorSpace::Primaries gamut, const QList<uint16_t> &transferFunctionTable)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QColorSpace` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `gamut`：类型为 `QColorSpace::Primaries`。没有默认值，调用时必须提供。传入 `QColorSpace::Primaries` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `transferFunctionTable`：类型为 `const QList<uint16_t> &`。没有默认值，调用时必须提供。传入 `const QList<uint16_t> &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QColorSpace::QColorSpace(QColorSpace::Primaries primaries, float gamma)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QColorSpace` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `primaries`：类型为 `QColorSpace::Primaries`。没有默认值，调用时必须提供。传入 `QColorSpace::Primaries` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `gamma`：类型为 `float`。没有默认值，调用时必须提供。传入 `float` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[explicit, since 6.8] QColorSpace::QColorSpace(QPointF whitePoint, const QList<uint16_t> &transferFunctionTable)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QColorSpace` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `whitePoint`：类型为 `QPointF`。没有默认值，调用时必须提供。传入 `QPointF` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `transferFunctionTable`：类型为 `const QList<uint16_t> &`。没有默认值，调用时必须提供。传入 `const QList<uint16_t> &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QColorSpace::QColorSpace(QColorSpace::Primaries primaries, QColorSpace::TransferFunction transferFunction, float gamma = 0.0f)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QColorSpace` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `primaries`：类型为 `QColorSpace::Primaries`。没有默认值，调用时必须提供。传入 `QColorSpace::Primaries` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `transferFunction`：类型为 `QColorSpace::TransferFunction`。没有默认值，调用时必须提供。传入 `QColorSpace::TransferFunction` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `gamma`：类型为 `float`。默认值为 `0.0f`。传入 `float` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[explicit, since 6.8] QColorSpace::QColorSpace(QPointF whitePoint, QColorSpace::TransferFunction transferFunction, float gamma = 0.0f)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QColorSpace` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `whitePoint`：类型为 `QPointF`。没有默认值，调用时必须提供。传入 `QPointF` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `transferFunction`：类型为 `QColorSpace::TransferFunction`。没有默认值，调用时必须提供。传入 `QColorSpace::TransferFunction` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `gamma`：类型为 `float`。默认值为 `0.0f`。传入 `float` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.9] QColorSpace::QColorSpace(const QColorSpace::PrimaryPoints &primaryPoints, QColorSpace::TransferFunction transferFunction, float gamma = 0.0f)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QColorSpace` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `primaryPoints`：类型为 `const QColorSpace::PrimaryPoints &`。没有默认值，调用时必须提供。传入 `const QColorSpace::PrimaryPoints &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `transferFunction`：类型为 `QColorSpace::TransferFunction`。没有默认值，调用时必须提供。传入 `QColorSpace::TransferFunction` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `gamma`：类型为 `float`。默认值为 `0.0f`。传入 `float` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.1] QColorSpace::QColorSpace(const QPointF &whitePoint, const QPointF &redPoint, const QPointF &greenPoint, const QPointF &bluePoint, const QList<uint16_t> &transferFunctionTable)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QColorSpace` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `whitePoint`：类型为 `const QPointF &`。没有默认值，调用时必须提供。传入 `const QPointF &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `redPoint`：类型为 `const QPointF &`。没有默认值，调用时必须提供。传入 `const QPointF &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `greenPoint`：类型为 `const QPointF &`。没有默认值，调用时必须提供。传入 `const QPointF &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `bluePoint`：类型为 `const QPointF &`。没有默认值，调用时必须提供。传入 `const QPointF &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `transferFunctionTable`：类型为 `const QList<uint16_t> &`。没有默认值，调用时必须提供。传入 `const QList<uint16_t> &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QColorSpace::QColorSpace(const QPointF &whitePoint, const QPointF &redPoint, const QPointF &greenPoint, const QPointF &bluePoint, QColorSpace::TransferFunction transferFunction, float gamma = 0.0f)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QColorSpace` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `whitePoint`：类型为 `const QPointF &`。没有默认值，调用时必须提供。传入 `const QPointF &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `redPoint`：类型为 `const QPointF &`。没有默认值，调用时必须提供。传入 `const QPointF &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `greenPoint`：类型为 `const QPointF &`。没有默认值，调用时必须提供。传入 `const QPointF &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `bluePoint`：类型为 `const QPointF &`。没有默认值，调用时必须提供。传入 `const QPointF &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `transferFunction`：类型为 `QColorSpace::TransferFunction`。没有默认值，调用时必须提供。传入 `QColorSpace::TransferFunction` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `gamma`：类型为 `float`。默认值为 `0.0f`。传入 `float` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.1] QColorSpace::QColorSpace(const QPointF &whitePoint, const QPointF &redPoint, const QPointF &greenPoint, const QPointF &bluePoint, const QList<uint16_t> &redTransferFunctionTable, const QList<uint16_t> &greenTransferFunctionTable, const QList<uint16_t> &blueTransferFunctionTable)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QColorSpace` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `whitePoint`：类型为 `const QPointF &`。没有默认值，调用时必须提供。传入 `const QPointF &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `redPoint`：类型为 `const QPointF &`。没有默认值，调用时必须提供。传入 `const QPointF &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `greenPoint`：类型为 `const QPointF &`。没有默认值，调用时必须提供。传入 `const QPointF &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `bluePoint`：类型为 `const QPointF &`。没有默认值，调用时必须提供。传入 `const QPointF &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `redTransferFunctionTable`：类型为 `const QList<uint16_t> &`。没有默认值，调用时必须提供。传入 `const QList<uint16_t> &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `greenTransferFunctionTable`：类型为 `const QList<uint16_t> &`。没有默认值，调用时必须提供。传入 `const QList<uint16_t> &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `blueTransferFunctionTable`：类型为 `const QList<uint16_t> &`。没有默认值，调用时必须提供。传入 `const QList<uint16_t> &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept, since 6.8] QColorSpace::ColorModel QColorSpace::colorModel() const`

**API 类别：** 成员函数说明

**中文解读：** `QColorSpace::colorModel` 用于计算、查询或取得与“color、Model”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QColorSpace::ColorModel`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QColorSpace::ColorModel`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept, since 6.2] QString QColorSpace::description() const`

**API 类别：** 成员函数说明

**中文解读：** `QColorSpace::description` 用于计算、查询或取得与“description”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QString`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QString`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] QColorSpace QColorSpace::fromIccProfile(const QByteArray &iccProfile)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `fromIccProfile`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QColorSpace`。
- 参数 `iccProfile`：类型为 `const QByteArray &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] float QColorSpace::gamma() const`

**API 类别：** 成员函数说明

**中文解读：** `QColorSpace::gamma` 用于计算、查询或取得与“gamma”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `float`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`float`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QByteArray QColorSpace::iccProfile() const`

**API 类别：** 成员函数说明

**中文解读：** `QColorSpace::iccProfile` 用于计算、查询或取得与“icc、Profile”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QByteArray`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QByteArray`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] bool QColorSpace::isValid() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `isValid`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept, since 6.8] bool QColorSpace::isValidTarget() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `isValidTarget`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] QColorSpace::Primaries QColorSpace::primaries() const`

**API 类别：** 成员函数说明

**中文解读：** `QColorSpace::primaries` 用于计算、查询或取得与“primaries”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QColorSpace::Primaries`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QColorSpace::Primaries`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.9] QColorSpace::PrimaryPoints QColorSpace::primaryPoints() const`

**API 类别：** 成员函数说明

**中文解读：** `QColorSpace::primaryPoints` 用于计算、查询或取得与“primary、Points”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QColorSpace::PrimaryPoints`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QColorSpace::PrimaryPoints`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.2] void QColorSpace::setDescription(const QString &description)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setDescription`。调用它会改变 `QColorSpace` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `description`：类型为 `const QString &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QColorSpace::setPrimaries(QColorSpace::Primaries primariesId)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setPrimaries`。调用它会改变 `QColorSpace` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `primariesId`：类型为 `QColorSpace::Primaries`。没有默认值，调用时必须提供。传入 `QColorSpace::Primaries` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QColorSpace::setPrimaries(const QPointF &whitePoint, const QPointF &redPoint, const QPointF &greenPoint, const QPointF &bluePoint)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setPrimaries`。调用它会改变 `QColorSpace` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `whitePoint`：类型为 `const QPointF &`。没有默认值，调用时必须提供。传入 `const QPointF &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `redPoint`：类型为 `const QPointF &`。没有默认值，调用时必须提供。传入 `const QPointF &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `greenPoint`：类型为 `const QPointF &`。没有默认值，调用时必须提供。传入 `const QPointF &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `bluePoint`：类型为 `const QPointF &`。没有默认值，调用时必须提供。传入 `const QPointF &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.9] void QColorSpace::setPrimaryPoints(const QColorSpace::PrimaryPoints &primaryPoints)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setPrimaryPoints`。调用它会改变 `QColorSpace` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `primaryPoints`：类型为 `const QColorSpace::PrimaryPoints &`。没有默认值，调用时必须提供。传入 `const QColorSpace::PrimaryPoints &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.1] void QColorSpace::setTransferFunction(const QList<uint16_t> &transferFunctionTable)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setTransferFunction`。调用它会改变 `QColorSpace` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `transferFunctionTable`：类型为 `const QList<uint16_t> &`。没有默认值，调用时必须提供。传入 `const QList<uint16_t> &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QColorSpace::setTransferFunction(QColorSpace::TransferFunction transferFunction, float gamma = 0.0f)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setTransferFunction`。调用它会改变 `QColorSpace` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `transferFunction`：类型为 `QColorSpace::TransferFunction`。没有默认值，调用时必须提供。传入 `QColorSpace::TransferFunction` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `gamma`：类型为 `float`。默认值为 `0.0f`。传入 `float` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.1] void QColorSpace::setTransferFunctions(const QList<uint16_t> &redTransferFunctionTable, const QList<uint16_t> &greenTransferFunctionTable, const QList<uint16_t> &blueTransferFunctionTable)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setTransferFunctions`。调用它会改变 `QColorSpace` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `redTransferFunctionTable`：类型为 `const QList<uint16_t> &`。没有默认值，调用时必须提供。传入 `const QList<uint16_t> &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `greenTransferFunctionTable`：类型为 `const QList<uint16_t> &`。没有默认值，调用时必须提供。传入 `const QList<uint16_t> &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `blueTransferFunctionTable`：类型为 `const QList<uint16_t> &`。没有默认值，调用时必须提供。传入 `const QList<uint16_t> &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.8] void QColorSpace::setWhitePoint(QPointF whitePoint)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setWhitePoint`。调用它会改变 `QColorSpace` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `whitePoint`：类型为 `QPointF`。没有默认值，调用时必须提供。传入 `QPointF` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] void QColorSpace::swap(QColorSpace &other)`

**API 类别：** 成员函数说明

**中文解读：** `QColorSpace::swap` 用于执行与“swap”相关的操作。调用时要先确认当前状态和 `other` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `other`：类型为 `QColorSpace &`。没有默认值，调用时必须提供。参与比较、合并或交换的另一个对象；要确认它与当前对象属于同一类型或兼容协议。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] QColorSpace::TransferFunction QColorSpace::transferFunction() const`

**API 类别：** 成员函数说明

**中文解读：** `QColorSpace::transferFunction` 用于计算、查询或取得与“transfer、Function”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QColorSpace::TransferFunction`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QColorSpace::TransferFunction`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept, since 6.8] QColorSpace::TransformModel QColorSpace::transformModel() const`

**API 类别：** 成员函数说明

**中文解读：** `QColorSpace::transformModel` 用于计算、查询或取得与“transform、Model”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QColorSpace::TransformModel`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QColorSpace::TransformModel`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QColorTransform QColorSpace::transformationToColorSpace(const QColorSpace &colorspace) const`

**API 类别：** 成员函数说明

**中文解读：** `QColorSpace::transformationToColorSpace` 用于计算、查询或取得与“transformation、转换输出、Color、Space”相关的操作。调用时要先确认当前状态和 `colorspace` 的有效范围；返回类型是 `QColorTransform`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QColorTransform`。
- 参数 `colorspace`：类型为 `const QColorSpace &`。没有默认值，调用时必须提供。传入 `const QColorSpace &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.8] QPointF QColorSpace::whitePoint() const`

**API 类别：** 成员函数说明

**中文解读：** `QColorSpace::whitePoint` 用于计算、查询或取得与“white、Point”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QPointF`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QPointF`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.1] QColorSpace QColorSpace::withTransferFunction(const QList<uint16_t> &transferFunctionTable) const`

**API 类别：** 成员函数说明

**中文解读：** `QColorSpace::withTransferFunction` 用于计算、查询或取得与“with、Transfer、Function”相关的操作。调用时要先确认当前状态和 `transferFunctionTable` 的有效范围；返回类型是 `QColorSpace`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QColorSpace`。
- 参数 `transferFunctionTable`：类型为 `const QList<uint16_t> &`。没有默认值，调用时必须提供。传入 `const QList<uint16_t> &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QColorSpace QColorSpace::withTransferFunction(QColorSpace::TransferFunction transferFunction, float gamma = 0.0f) const`

**API 类别：** 成员函数说明

**中文解读：** `QColorSpace::withTransferFunction` 用于计算、查询或取得与“with、Transfer、Function”相关的操作。调用时要先确认当前状态和 `transferFunction`、`gamma` 的有效范围；返回类型是 `QColorSpace`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QColorSpace`。
- 参数 `transferFunction`：类型为 `QColorSpace::TransferFunction`。没有默认值，调用时必须提供。传入 `QColorSpace::TransferFunction` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `gamma`：类型为 `float`。默认值为 `0.0f`。传入 `float` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.1] QColorSpace QColorSpace::withTransferFunctions(const QList<uint16_t> &redTransferFunctionTable, const QList<uint16_t> &greenTransferFunctionTable, const QList<uint16_t> &blueTransferFunctionTable) const`

**API 类别：** 成员函数说明

**中文解读：** `QColorSpace::withTransferFunctions` 用于计算、查询或取得与“with、Transfer、Functions”相关的操作。调用时要先确认当前状态和 `redTransferFunctionTable`、`greenTransferFunctionTable`、`blueTransferFunctionTable` 的有效范围；返回类型是 `QColorSpace`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QColorSpace`。
- 参数 `redTransferFunctionTable`：类型为 `const QList<uint16_t> &`。没有默认值，调用时必须提供。传入 `const QList<uint16_t> &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `greenTransferFunctionTable`：类型为 `const QList<uint16_t> &`。没有默认值，调用时必须提供。传入 `const QList<uint16_t> &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `blueTransferFunctionTable`：类型为 `const QList<uint16_t> &`。没有默认值，调用时必须提供。传入 `const QList<uint16_t> &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QColorSpace::operator QVariant() const`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QColorSpace` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`由运算符声明决定`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool operator!=(const QColorSpace &colorSpace1, const QColorSpace &colorSpace2)`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QColorSpace` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`bool`。
- 参数 `colorSpace1`：类型为 `const QColorSpace &`。没有默认值，调用时必须提供。传入 `const QColorSpace &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `colorSpace2`：类型为 `const QColorSpace &`。没有默认值，调用时必须提供。传入 `const QColorSpace &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QDataStream &operator<<(QDataStream &stream, const QColorSpace &colorSpace)`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QColorSpace` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QDataStream &`。
- 参数 `stream`：类型为 `QDataStream &`。没有默认值，调用时必须提供。传入 `QDataStream &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `colorSpace`：类型为 `const QColorSpace &`。没有默认值，调用时必须提供。传入 `const QColorSpace &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool operator==(const QColorSpace &colorSpace1, const QColorSpace &colorSpace2)`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QColorSpace` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`bool`。
- 参数 `colorSpace1`：类型为 `const QColorSpace &`。没有默认值，调用时必须提供。传入 `const QColorSpace &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `colorSpace2`：类型为 `const QColorSpace &`。没有默认值，调用时必须提供。传入 `const QColorSpace &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QDataStream &operator>>(QDataStream &stream, QColorSpace &colorSpace)`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QColorSpace` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QDataStream &`。
- 参数 `stream`：类型为 `QDataStream &`。没有默认值，调用时必须提供。传入 `QDataStream &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `colorSpace`：类型为 `QColorSpace &`。没有默认值，调用时必须提供。传入 `QColorSpace &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `(since 6.9) struct PrimaryPoints`

**API 类别：** 公有类型

**中文解读：** 这是 `QColorSpace` 的 `Primary、Points` 成员声明。它通常作为其他 API 的类型、常量或配置入口使用；先确认可用值和适用状态，再结合本类的创建、核心操作和清理流程使用。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

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

`QColorSpace` 所属机制类型：Qt 类型机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
