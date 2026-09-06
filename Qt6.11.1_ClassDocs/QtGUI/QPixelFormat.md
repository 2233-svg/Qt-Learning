# QPixelFormat

> Qt 6.11.1 · Qt GUI

## 1. 先建立直觉

**一句话定位：** 这是格式或能力描述类型，重点关注可用格式、属性查询和与实际数据对象之间的转换。

**模块背景：** Qt GUI 负责窗口系统集成、绘制、颜色、字体、图像、输入事件和底层 GUI 资源。

### 这是什么

`QPixelFormat` 是 Qt 类型机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 这个类的行为由它的继承关系、构造参数、公开状态和成员函数协议共同决定。使用时要把创建、配置、核心操作、结果/通知和清理看成一条闭环，而不是孤立调用某个函数。

**适用场景：** 围绕这个类的核心职责建立最小闭环：准备依赖 -> 创建/取得对象 -> 设置必要配置 -> 调用核心 API -> 检查返回值和状态 -> 处理结果/错误 -> 结束时清理。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要忽略构造失败、空返回、默认值和版本限制；不要把异步 API 当同步 API；不要在没有确认所有权和线程的情况下保存指针或跨线程调用。

## 2. 依赖与对象关系

- 头文件：`#include <QPixelFormat>`
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

- `enum AlphaPosition { AtBeginning, AtEnd }`
- `enum AlphaPremultiplied { NotPremultiplied, Premultiplied }`
- `enum AlphaUsage { IgnoresAlpha, UsesAlpha }`
- `enum ByteOrder { LittleEndian, BigEndian, CurrentSystemEndian }`
- `enum ColorModel { RGB, BGR, Indexed, Grayscale, CMYK, …, Alpha }`
- `enum TypeInterpretation { UnsignedInteger, UnsignedShort, UnsignedByte, FloatingPoint }`
- `enum YUVLayout { YUV444, YUV422, YUV411, YUV420P, YUV420SP, …, Y16 }`

### 公有函数

- `QPixelFormat()`
- `QPixelFormat(QPixelFormat::ColorModel colorModel, uchar firstSize, uchar secondSize, uchar thirdSize, uchar fourthSize, uchar fifthSize, uchar alphaSize, QPixelFormat::AlphaUsage alphaUsage, QPixelFormat::AlphaPosition alphaPosition, QPixelFormat::AlphaPremultiplied premultiplied, QPixelFormat::TypeInterpretation typeInterpretation, QPixelFormat::ByteOrder byteOrder = CurrentSystemEndian, uchar subEnum = 0)`
- `QPixelFormat::AlphaPosition alphaPosition() const`
- `uchar alphaSize() const`
- `QPixelFormat::AlphaUsage alphaUsage() const`
- `uchar bitsPerPixel() const`
- `uchar blackSize() const`
- `uchar blueSize() const`
- `uchar brightnessSize() const`
- `QPixelFormat::ByteOrder byteOrder() const`
- `uchar channelCount() const`
- `QPixelFormat::ColorModel colorModel() const`
- `uchar cyanSize() const`
- `uchar greenSize() const`
- `uchar hueSize() const`
- `uchar lightnessSize() const`
- `uchar magentaSize() const`
- `QPixelFormat::AlphaPremultiplied premultiplied() const`
- `uchar redSize() const`
- `uchar saturationSize() const`
- `QPixelFormat::TypeInterpretation typeInterpretation() const`
- `uchar yellowSize() const`
- `QPixelFormat::YUVLayout yuvLayout() const`

### 相关非成员函数

- `QPixelFormat qPixelFormatAlpha(uchar channelSize, QPixelFormat::TypeInterpretation typeInterpretation = QPixelFormat::UnsignedInteger)`
- `QPixelFormat qPixelFormatCmyk(uchar channelSize, uchar alphaSize = 0, QPixelFormat::AlphaUsage alphaUsage = QPixelFormat::IgnoresAlpha, QPixelFormat::AlphaPosition alphaPosition = QPixelFormat::AtBeginning, QPixelFormat::TypeInterpretation typeInterpretation = QPixelFormat::UnsignedInteger)`
- `QPixelFormat qPixelFormatGrayscale(uchar channelSize, QPixelFormat::TypeInterpretation typeInterpretation = QPixelFormat::UnsignedInteger)`
- `QPixelFormat qPixelFormatHsl(uchar channelSize, uchar alphaSize = 0, QPixelFormat::AlphaUsage alphaUsage = QPixelFormat::IgnoresAlpha, QPixelFormat::AlphaPosition alphaPosition = QPixelFormat::AtBeginning, QPixelFormat::TypeInterpretation typeInterpretation = QPixelFormat::FloatingPoint)`
- `QPixelFormat qPixelFormatHsv(uchar channelSize, uchar alphaSize = 0, QPixelFormat::AlphaUsage alphaUsage = QPixelFormat::IgnoresAlpha, QPixelFormat::AlphaPosition alphaPosition = QPixelFormat::AtBeginning, QPixelFormat::TypeInterpretation typeInterpretation = QPixelFormat::FloatingPoint)`
- `QPixelFormat qPixelFormatRgba(uchar redSize, uchar greenSize, uchar blueSize, uchar alphaSize, QPixelFormat::AlphaUsage alphaUsage, QPixelFormat::AlphaPosition alphaPosition, QPixelFormat::AlphaPremultiplied premultiplied = QPixelFormat::NotPremultiplied, QPixelFormat::TypeInterpretation typeInterpretation = QPixelFormat::UnsignedInteger)`
- `QPixelFormat qPixelFormatYuv(QPixelFormat::YUVLayout yuvLayout, uchar alphaSize = 0, QPixelFormat::AlphaUsage alphaUsage = QPixelFormat::IgnoresAlpha, QPixelFormat::AlphaPosition alphaPosition = QPixelFormat::AtBeginning, QPixelFormat::AlphaPremultiplied premultiplied = QPixelFormat::NotPremultiplied, QPixelFormat::TypeInterpretation typeInterpretation = QPixelFormat::UnsignedByte, QPixelFormat::ByteOrder byteOrder = QPixelFormat::BigEndian)`

## 5. API 逐个说明

这里直接说明每个公开成员解决什么问题、参数代表什么、返回什么、会改变什么以及使用时容易出现什么问题。每一个公开签名都会有对应的中文解释。

本类共整理 37 个公开成员条目；没有独立长描述的 API 也会根据签名、类型和所属机制给出使用说明。

### `enum QPixelFormat::AlphaPosition`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QPixelFormat` 暴露的类型声明 `Alpha、Position`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 属性类型：`:AlphaPosition`。
- 属性名：`QPixelFormat`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `enum QPixelFormat::AlphaPremultiplied`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QPixelFormat` 暴露的类型声明 `Alpha、Premultiplied`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 属性类型：`:AlphaPremultiplied`。
- 属性名：`QPixelFormat`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `enum QPixelFormat::AlphaUsage`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QPixelFormat` 暴露的类型声明 `Alpha、Usage`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 属性类型：`:AlphaUsage`。
- 属性名：`QPixelFormat`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `enum QPixelFormat::ByteOrder`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QPixelFormat` 暴露的类型声明 `Byte、Order`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 属性类型：`:ByteOrder`。
- 属性名：`QPixelFormat`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `enum QPixelFormat::ColorModel`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QPixelFormat` 暴露的类型声明 `Color、Model`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 属性类型：`:ColorModel`。
- 属性名：`QPixelFormat`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `enum QPixelFormat::TypeInterpretation`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QPixelFormat` 暴露的类型声明 `类型、Interpretation`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 属性类型：`:TypeInterpretation`。
- 属性名：`QPixelFormat`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `enum QPixelFormat::YUVLayout`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QPixelFormat` 暴露的类型声明 `YUV、Layout`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 属性类型：`:YUVLayout`。
- 属性名：`QPixelFormat`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[constexpr noexcept] QPixelFormat::QPixelFormat()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QPixelFormat` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[constexpr noexcept] QPixelFormat::QPixelFormat(QPixelFormat::ColorModel colorModel, uchar firstSize, uchar secondSize, uchar thirdSize, uchar fourthSize, uchar fifthSize, uchar alphaSize, QPixelFormat::AlphaUsage alphaUsage, QPixelFormat::AlphaPosition alphaPosition, QPixelFormat::AlphaPremultiplied premultiplied, QPixelFormat::TypeInterpretation typeInterpretation, QPixelFormat::ByteOrder byteOrder = CurrentSystemEndian, uchar subEnum = 0)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QPixelFormat` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `colorModel`：类型为 `QPixelFormat::ColorModel`。没有默认值，调用时必须提供。传入 `QPixelFormat::ColorModel` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `firstSize`：类型为 `uchar`。没有默认值，调用时必须提供。传入 `uchar` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `secondSize`：类型为 `uchar`。没有默认值，调用时必须提供。传入 `uchar` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `thirdSize`：类型为 `uchar`。没有默认值，调用时必须提供。传入 `uchar` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `fourthSize`：类型为 `uchar`。没有默认值，调用时必须提供。传入 `uchar` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `fifthSize`：类型为 `uchar`。没有默认值，调用时必须提供。传入 `uchar` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `alphaSize`：类型为 `uchar`。没有默认值，调用时必须提供。传入 `uchar` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `alphaUsage`：类型为 `QPixelFormat::AlphaUsage`。没有默认值，调用时必须提供。传入 `QPixelFormat::AlphaUsage` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `alphaPosition`：类型为 `QPixelFormat::AlphaPosition`。没有默认值，调用时必须提供。传入 `QPixelFormat::AlphaPosition` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `premultiplied`：类型为 `QPixelFormat::AlphaPremultiplied`。没有默认值，调用时必须提供。传入 `QPixelFormat::AlphaPremultiplied` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `typeInterpretation`：类型为 `QPixelFormat::TypeInterpretation`。没有默认值，调用时必须提供。传入 `QPixelFormat::TypeInterpretation` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `byteOrder`：类型为 `QPixelFormat::ByteOrder`。默认值为 `CurrentSystemEndian`。传入 `QPixelFormat::ByteOrder` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `subEnum`：类型为 `uchar`。默认值为 `0`。传入 `uchar` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[constexpr noexcept] QPixelFormat::AlphaPosition QPixelFormat::alphaPosition() const`

**API 类别：** 成员函数说明

**中文解读：** `QPixelFormat::alphaPosition` 用于计算、查询或取得与“alpha、Position”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QPixelFormat::AlphaPosition`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QPixelFormat::AlphaPosition`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[constexpr noexcept] uchar QPixelFormat::alphaSize() const`

**API 类别：** 成员函数说明

**中文解读：** `QPixelFormat::alphaSize` 用于计算、查询或取得与“alpha、尺寸或数量”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `uchar`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`uchar`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[constexpr noexcept] QPixelFormat::AlphaUsage QPixelFormat::alphaUsage() const`

**API 类别：** 成员函数说明

**中文解读：** `QPixelFormat::alphaUsage` 用于计算、查询或取得与“alpha、Usage”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QPixelFormat::AlphaUsage`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QPixelFormat::AlphaUsage`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[constexpr noexcept] uchar QPixelFormat::bitsPerPixel() const`

**API 类别：** 成员函数说明

**中文解读：** `QPixelFormat::bitsPerPixel` 用于计算、查询或取得与“bits、Per、Pixel”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `uchar`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`uchar`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[constexpr noexcept] uchar QPixelFormat::blackSize() const`

**API 类别：** 成员函数说明

**中文解读：** `QPixelFormat::blackSize` 用于计算、查询或取得与“black、尺寸或数量”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `uchar`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`uchar`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[constexpr noexcept] uchar QPixelFormat::blueSize() const`

**API 类别：** 成员函数说明

**中文解读：** `QPixelFormat::blueSize` 用于计算、查询或取得与“blue、尺寸或数量”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `uchar`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`uchar`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[constexpr noexcept] uchar QPixelFormat::brightnessSize() const`

**API 类别：** 成员函数说明

**中文解读：** `QPixelFormat::brightnessSize` 用于计算、查询或取得与“brightness、尺寸或数量”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `uchar`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`uchar`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[constexpr noexcept] QPixelFormat::ByteOrder QPixelFormat::byteOrder() const`

**API 类别：** 成员函数说明

**中文解读：** `QPixelFormat::byteOrder` 用于计算、查询或取得与“byte、Order”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QPixelFormat::ByteOrder`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QPixelFormat::ByteOrder`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[constexpr noexcept] uchar QPixelFormat::channelCount() const`

**API 类别：** 成员函数说明

**中文解读：** `QPixelFormat::channelCount` 用于计算、查询或取得与“channel、数量统计”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `uchar`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`uchar`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[constexpr noexcept] QPixelFormat::ColorModel QPixelFormat::colorModel() const`

**API 类别：** 成员函数说明

**中文解读：** `QPixelFormat::colorModel` 用于计算、查询或取得与“color、Model”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QPixelFormat::ColorModel`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QPixelFormat::ColorModel`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[constexpr noexcept] uchar QPixelFormat::cyanSize() const`

**API 类别：** 成员函数说明

**中文解读：** `QPixelFormat::cyanSize` 用于计算、查询或取得与“cyan、尺寸或数量”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `uchar`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`uchar`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[constexpr noexcept] uchar QPixelFormat::greenSize() const`

**API 类别：** 成员函数说明

**中文解读：** `QPixelFormat::greenSize` 用于计算、查询或取得与“green、尺寸或数量”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `uchar`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`uchar`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[constexpr noexcept] uchar QPixelFormat::hueSize() const`

**API 类别：** 成员函数说明

**中文解读：** `QPixelFormat::hueSize` 用于计算、查询或取得与“hue、尺寸或数量”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `uchar`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`uchar`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[constexpr noexcept] uchar QPixelFormat::lightnessSize() const`

**API 类别：** 成员函数说明

**中文解读：** `QPixelFormat::lightnessSize` 用于计算、查询或取得与“lightness、尺寸或数量”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `uchar`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`uchar`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[constexpr noexcept] uchar QPixelFormat::magentaSize() const`

**API 类别：** 成员函数说明

**中文解读：** `QPixelFormat::magentaSize` 用于计算、查询或取得与“magenta、尺寸或数量”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `uchar`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`uchar`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[constexpr noexcept] QPixelFormat::AlphaPremultiplied QPixelFormat::premultiplied() const`

**API 类别：** 成员函数说明

**中文解读：** `QPixelFormat::premultiplied` 用于计算、查询或取得与“premultiplied”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QPixelFormat::AlphaPremultiplied`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QPixelFormat::AlphaPremultiplied`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[constexpr noexcept] uchar QPixelFormat::redSize() const`

**API 类别：** 成员函数说明

**中文解读：** `QPixelFormat::redSize` 用于计算、查询或取得与“red、尺寸或数量”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `uchar`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`uchar`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[constexpr noexcept] uchar QPixelFormat::saturationSize() const`

**API 类别：** 成员函数说明

**中文解读：** `QPixelFormat::saturationSize` 用于计算、查询或取得与“saturation、尺寸或数量”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `uchar`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`uchar`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[constexpr noexcept] QPixelFormat::TypeInterpretation QPixelFormat::typeInterpretation() const`

**API 类别：** 成员函数说明

**中文解读：** `QPixelFormat::typeInterpretation` 用于计算、查询或取得与“类型、Interpretation”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QPixelFormat::TypeInterpretation`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QPixelFormat::TypeInterpretation`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[constexpr noexcept] uchar QPixelFormat::yellowSize() const`

**API 类别：** 成员函数说明

**中文解读：** `QPixelFormat::yellowSize` 用于计算、查询或取得与“yellow、尺寸或数量”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `uchar`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`uchar`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[constexpr noexcept] QPixelFormat::YUVLayout QPixelFormat::yuvLayout() const`

**API 类别：** 成员函数说明

**中文解读：** `QPixelFormat::yuvLayout` 用于计算、查询或取得与“yuv、Layout”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QPixelFormat::YUVLayout`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QPixelFormat::YUVLayout`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[constexpr noexcept] QPixelFormat qPixelFormatAlpha(uchar channelSize, QPixelFormat::TypeInterpretation typeInterpretation = QPixelFormat::UnsignedInteger)`

**API 类别：** 相关非成员函数

**中文解读：** `QPixelFormat::qPixelFormatAlpha` 用于计算、查询或取得与“q、Pixel、格式化、Alpha”相关的操作。调用时要先确认当前状态和 `channelSize`、`typeInterpretation` 的有效范围；返回类型是 `QPixelFormat`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QPixelFormat`。
- 参数 `channelSize`：类型为 `uchar`。没有默认值，调用时必须提供。传入 `uchar` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `typeInterpretation`：类型为 `QPixelFormat::TypeInterpretation`。默认值为 `QPixelFormat::UnsignedInteger`。传入 `QPixelFormat::TypeInterpretation` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[constexpr noexcept] QPixelFormat qPixelFormatCmyk(uchar channelSize, uchar alphaSize = 0, QPixelFormat::AlphaUsage alphaUsage = QPixelFormat::IgnoresAlpha, QPixelFormat::AlphaPosition alphaPosition = QPixelFormat::AtBeginning, QPixelFormat::TypeInterpretation typeInterpretation = QPixelFormat::UnsignedInteger)`

**API 类别：** 相关非成员函数

**中文解读：** `QPixelFormat::qPixelFormatCmyk` 用于计算、查询或取得与“q、Pixel、格式化、Cmyk”相关的操作。调用时要先确认当前状态和 `channelSize`、`alphaSize`、`alphaUsage`、`alphaPosition`、`typeInterpretation` 的有效范围；返回类型是 `QPixelFormat`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QPixelFormat`。
- 参数 `channelSize`：类型为 `uchar`。没有默认值，调用时必须提供。传入 `uchar` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `alphaSize`：类型为 `uchar`。默认值为 `0`。传入 `uchar` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `alphaUsage`：类型为 `QPixelFormat::AlphaUsage`。默认值为 `QPixelFormat::IgnoresAlpha`。传入 `QPixelFormat::AlphaUsage` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `alphaPosition`：类型为 `QPixelFormat::AlphaPosition`。默认值为 `QPixelFormat::AtBeginning`。传入 `QPixelFormat::AlphaPosition` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `typeInterpretation`：类型为 `QPixelFormat::TypeInterpretation`。默认值为 `QPixelFormat::UnsignedInteger`。传入 `QPixelFormat::TypeInterpretation` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[constexpr noexcept] QPixelFormat qPixelFormatGrayscale(uchar channelSize, QPixelFormat::TypeInterpretation typeInterpretation = QPixelFormat::UnsignedInteger)`

**API 类别：** 相关非成员函数

**中文解读：** `QPixelFormat::qPixelFormatGrayscale` 用于计算、查询或取得与“q、Pixel、格式化、Grayscale”相关的操作。调用时要先确认当前状态和 `channelSize`、`typeInterpretation` 的有效范围；返回类型是 `QPixelFormat`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QPixelFormat`。
- 参数 `channelSize`：类型为 `uchar`。没有默认值，调用时必须提供。传入 `uchar` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `typeInterpretation`：类型为 `QPixelFormat::TypeInterpretation`。默认值为 `QPixelFormat::UnsignedInteger`。传入 `QPixelFormat::TypeInterpretation` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[constexpr noexcept] QPixelFormat qPixelFormatHsl(uchar channelSize, uchar alphaSize = 0, QPixelFormat::AlphaUsage alphaUsage = QPixelFormat::IgnoresAlpha, QPixelFormat::AlphaPosition alphaPosition = QPixelFormat::AtBeginning, QPixelFormat::TypeInterpretation typeInterpretation = QPixelFormat::FloatingPoint)`

**API 类别：** 相关非成员函数

**中文解读：** `QPixelFormat::qPixelFormatHsl` 用于计算、查询或取得与“q、Pixel、格式化、Hsl”相关的操作。调用时要先确认当前状态和 `channelSize`、`alphaSize`、`alphaUsage`、`alphaPosition`、`typeInterpretation` 的有效范围；返回类型是 `QPixelFormat`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QPixelFormat`。
- 参数 `channelSize`：类型为 `uchar`。没有默认值，调用时必须提供。传入 `uchar` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `alphaSize`：类型为 `uchar`。默认值为 `0`。传入 `uchar` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `alphaUsage`：类型为 `QPixelFormat::AlphaUsage`。默认值为 `QPixelFormat::IgnoresAlpha`。传入 `QPixelFormat::AlphaUsage` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `alphaPosition`：类型为 `QPixelFormat::AlphaPosition`。默认值为 `QPixelFormat::AtBeginning`。传入 `QPixelFormat::AlphaPosition` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `typeInterpretation`：类型为 `QPixelFormat::TypeInterpretation`。默认值为 `QPixelFormat::FloatingPoint`。传入 `QPixelFormat::TypeInterpretation` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[constexpr noexcept] QPixelFormat qPixelFormatHsv(uchar channelSize, uchar alphaSize = 0, QPixelFormat::AlphaUsage alphaUsage = QPixelFormat::IgnoresAlpha, QPixelFormat::AlphaPosition alphaPosition = QPixelFormat::AtBeginning, QPixelFormat::TypeInterpretation typeInterpretation = QPixelFormat::FloatingPoint)`

**API 类别：** 相关非成员函数

**中文解读：** `QPixelFormat::qPixelFormatHsv` 用于计算、查询或取得与“q、Pixel、格式化、Hsv”相关的操作。调用时要先确认当前状态和 `channelSize`、`alphaSize`、`alphaUsage`、`alphaPosition`、`typeInterpretation` 的有效范围；返回类型是 `QPixelFormat`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QPixelFormat`。
- 参数 `channelSize`：类型为 `uchar`。没有默认值，调用时必须提供。传入 `uchar` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `alphaSize`：类型为 `uchar`。默认值为 `0`。传入 `uchar` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `alphaUsage`：类型为 `QPixelFormat::AlphaUsage`。默认值为 `QPixelFormat::IgnoresAlpha`。传入 `QPixelFormat::AlphaUsage` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `alphaPosition`：类型为 `QPixelFormat::AlphaPosition`。默认值为 `QPixelFormat::AtBeginning`。传入 `QPixelFormat::AlphaPosition` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `typeInterpretation`：类型为 `QPixelFormat::TypeInterpretation`。默认值为 `QPixelFormat::FloatingPoint`。传入 `QPixelFormat::TypeInterpretation` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[constexpr noexcept] QPixelFormat qPixelFormatRgba(uchar redSize, uchar greenSize, uchar blueSize, uchar alphaSize, QPixelFormat::AlphaUsage alphaUsage, QPixelFormat::AlphaPosition alphaPosition, QPixelFormat::AlphaPremultiplied premultiplied = QPixelFormat::NotPremultiplied, QPixelFormat::TypeInterpretation typeInterpretation = QPixelFormat::UnsignedInteger)`

**API 类别：** 相关非成员函数

**中文解读：** `QPixelFormat::qPixelFormatRgba` 用于计算、查询或取得与“q、Pixel、格式化、Rgba”相关的操作。调用时要先确认当前状态和 `redSize`、`greenSize`、`blueSize`、`alphaSize`、`alphaUsage`、`alphaPosition`、`premultiplied`、`typeInterpretation` 的有效范围；返回类型是 `QPixelFormat`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QPixelFormat`。
- 参数 `redSize`：类型为 `uchar`。没有默认值，调用时必须提供。传入 `uchar` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `greenSize`：类型为 `uchar`。没有默认值，调用时必须提供。传入 `uchar` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `blueSize`：类型为 `uchar`。没有默认值，调用时必须提供。传入 `uchar` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `alphaSize`：类型为 `uchar`。没有默认值，调用时必须提供。传入 `uchar` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `alphaUsage`：类型为 `QPixelFormat::AlphaUsage`。没有默认值，调用时必须提供。传入 `QPixelFormat::AlphaUsage` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `alphaPosition`：类型为 `QPixelFormat::AlphaPosition`。没有默认值，调用时必须提供。传入 `QPixelFormat::AlphaPosition` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `premultiplied`：类型为 `QPixelFormat::AlphaPremultiplied`。默认值为 `QPixelFormat::NotPremultiplied`。传入 `QPixelFormat::AlphaPremultiplied` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `typeInterpretation`：类型为 `QPixelFormat::TypeInterpretation`。默认值为 `QPixelFormat::UnsignedInteger`。传入 `QPixelFormat::TypeInterpretation` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QPixelFormat qPixelFormatYuv(QPixelFormat::YUVLayout yuvLayout, uchar alphaSize = 0, QPixelFormat::AlphaUsage alphaUsage = QPixelFormat::IgnoresAlpha, QPixelFormat::AlphaPosition alphaPosition = QPixelFormat::AtBeginning, QPixelFormat::AlphaPremultiplied premultiplied = QPixelFormat::NotPremultiplied, QPixelFormat::TypeInterpretation typeInterpretation = QPixelFormat::UnsignedByte, QPixelFormat::ByteOrder byteOrder = QPixelFormat::BigEndian)`

**API 类别：** 相关非成员函数

**中文解读：** `QPixelFormat::qPixelFormatYuv` 用于计算、查询或取得与“q、Pixel、格式化、Yuv”相关的操作。调用时要先确认当前状态和 `yuvLayout`、`alphaSize`、`alphaUsage`、`alphaPosition`、`premultiplied`、`typeInterpretation`、`byteOrder` 的有效范围；返回类型是 `QPixelFormat`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QPixelFormat`。
- 参数 `yuvLayout`：类型为 `QPixelFormat::YUVLayout`。没有默认值，调用时必须提供。Qt 对象参数。要确认对象有效、线程归属、所有权和该 API 是否只处理直接子对象。
- 参数 `alphaSize`：类型为 `uchar`。默认值为 `0`。传入 `uchar` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `alphaUsage`：类型为 `QPixelFormat::AlphaUsage`。默认值为 `QPixelFormat::IgnoresAlpha`。传入 `QPixelFormat::AlphaUsage` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `alphaPosition`：类型为 `QPixelFormat::AlphaPosition`。默认值为 `QPixelFormat::AtBeginning`。传入 `QPixelFormat::AlphaPosition` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `premultiplied`：类型为 `QPixelFormat::AlphaPremultiplied`。默认值为 `QPixelFormat::NotPremultiplied`。传入 `QPixelFormat::AlphaPremultiplied` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `typeInterpretation`：类型为 `QPixelFormat::TypeInterpretation`。默认值为 `QPixelFormat::UnsignedByte`。传入 `QPixelFormat::TypeInterpretation` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `byteOrder`：类型为 `QPixelFormat::ByteOrder`。默认值为 `QPixelFormat::BigEndian`。传入 `QPixelFormat::ByteOrder` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

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

`QPixelFormat` 所属机制类型：Qt 类型机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
