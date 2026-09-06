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

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `enum QPixelFormat::AlphaPosition`

**作用与语义：**

该枚举描述了像素格式的α位置。
- `QPixelFormat::AtBeginning`：`0`;alpha 通道会放在彩色通道前面。例如 ARGB。
- `QPixelFormat::AtEnd`：`1`;alpha通道会放在彩色通道的后部。例如RGBA。

### `enum QPixelFormat::AlphaPremultiplied`

**作用与语义：**

该枚举描述了像素格式的阿尔法通道是否`premultiplied`入色彩通道。
- `QPixelFormat::NotPremultiplied`：`0`;α通道不与颜色通道相乘。
- `QPixelFormat::Premultiplied`：`1`;阿尔法通道被乘以颜色通道。

### `enum QPixelFormat::AlphaUsage`

**作用与语义：**

该枚举描述了像素格式的 alpha 使用情况。
- `QPixelFormat::IgnoresAlpha`：`1`;不使用阿尔法通道。
- `QPixelFormat::UsesAlpha`：`0`;使用阿尔法通道。

### `enum QPixelFormat::ByteOrder`

**作用与语义：**

该枚举描述了像素格式的字节顺序。
- `QPixelFormat::LittleEndian`：`0`;字节序为小端序。
- `QPixelFormat::BigEndian`：`1`;字节序为大端序。
- `QPixelFormat::CurrentSystemEndian`：`2`;该枚举不会被存储，而是在构造器中转换为与当前系统枚举匹配的端序枚举。

### `enum QPixelFormat::ColorModel`

**作用与语义：**

该枚举描述了像素格式的颜色模型。
- `QPixelFormat::RGB`：`0`;颜色模型为RGB。
- `QPixelFormat::BGR`：`1`;这逻辑上是RGB的相反端序版本。不过，为了便于使用，它有自己的型号。
- `QPixelFormat::Indexed`：`2`;色彩模型使用色彩调色板。
- `QPixelFormat::Grayscale`：`3`;彩色模型为灰度。
- `QPixelFormat::CMYK`：`4`;彩色模型为CMYK。
- `QPixelFormat::HSL`：`5`;颜色模型为HSL。
- `QPixelFormat::HSV`：`6`;颜色模型为HSV。
- `QPixelFormat::YUV`：`7`;颜色模型为YUV。
- `QPixelFormat::Alpha`：`8`;[自5.5版本起]没有彩色模型，仅使用alpha。

### `enum QPixelFormat::TypeInterpretation`

**作用与语义：**

该枚举描述了像素格式的类型解释。
- `QPixelFormat::UnsignedInteger`：`0`;像素应被读取为一个或多个`unsigned int`。
- `QPixelFormat::UnsignedShort`：`1`;像素应被读取为一个或多个`unsigned short`。
- `QPixelFormat::UnsignedByte`：`2`;像素应被读取为一个或多个`byte`。
- `QPixelFormat::FloatingPoint`：`3`;像素应被读取为一个或多个浮点数，具体类型由颜色/阿尔法通道定义，即`qfloat16` 用于16位半浮点格式，`float`用于32位全浮点格式。

### `enum QPixelFormat::YUVLayout`

**作用与语义：**

该枚举描述了像素格式的YUV布局，前提是它具有`QPixelFormat::YUV`的颜色模型。
- `QPixelFormat::YUV444`：`0`
- `QPixelFormat::YUV422`：`1`
- `QPixelFormat::YUV411`：`2`
- `QPixelFormat::YUV420P`：`3`
- `QPixelFormat::YUV420SP`：`4`
- `QPixelFormat::YV12`：`5`
- `QPixelFormat::UYVY`：`6`
- `QPixelFormat::YUYV`：`7`
- `QPixelFormat::NV12`：`8`
- `QPixelFormat::NV21`：`9`
- `QPixelFormat::IMC1`：`10`
- `QPixelFormat::IMC2`：`11`
- `QPixelFormat::IMC3`：`12`
- `QPixelFormat::IMC4`：`13`
- `QPixelFormat::Y8`：`14`
- `QPixelFormat::Y16`：`15`

### `[constexpr noexcept] QPixelFormat::QPixelFormat()`

**作用与语义：**

创建空像素格式。该格式映射到`QImage::Format_Invalid`。

### `[constexpr noexcept] QPixelFormat::QPixelFormat(QPixelFormat::ColorModel colorModel, uchar firstSize, uchar secondSize, uchar thirdSize, uchar fourthSize, uchar fifthSize, uchar alphaSize, QPixelFormat::AlphaUsage alphaUsage, QPixelFormat::AlphaPosition alphaPosition, QPixelFormat::AlphaPremultiplied premultiplied, QPixelFormat::TypeInterpretation typeInterpretation, QPixelFormat::ByteOrder byteOrder = CurrentSystemEndian, uchar subEnum = 0)`

**作用与语义：**

创建QPixel格式，将数据分配给属性。`colorModel`会被放入一个4位的缓冲区。
`firstSize` `secondSize` `thirdSize` `fourthSize` `fifthSize` `alphaSize` 都用来表示通道的大小。通道会根据`colorModel`的不同用途被使用。对于 RGB 来说，firstSize 代表红色通道。在 CMYK 中，它代表青色通道的数值。
`alphaUsage`表示是否使用了阿尔法通道。
`alphaPosition` 是阿尔法通道的位置。
`premultiplied`表示阿尔法通道是否已经与颜色通道相乘。
`typeInterpretation`像素是如何被解读的。
`byteOrder`表示像素格式的端序。默认为`CurrentSystemEndian`，非字节顺序格式的端序解析为系统的端序，`QPixelFormat::UnsignedByte`则`QPixelFormat::BigEndian`。
`subEnum`用于需要存储额外信息并提供额外枚举的colorModels。YUV用它来存储YUV类型，默认值为0。
注意：BGR格式有自己的色彩模型，不应使用RGB格式相反的端序来描述。

### `[constexpr noexcept] QPixelFormat::AlphaPosition QPixelFormat::alphaPosition() const`

**作用与语义：**

Accessor 函数用于 alpha 通道相对于颜色通道的位置。
对于单个通道映射到单个单元的格式，alpha位置相对于这些单元。例如，对于alpha位置为`QPixelFormat::AtEnd`的`QImage::Format_RGBA16FPx4`，alpha是最后读取的`qfloat16`。
对于将多个通道打包在一个单元中的格式，`QPixelFormat::AtBeginning`和`QPixelFormat::AtEnd`值映射到打包单元中相对于格式自身`byteOrder()`的最高有效和最低有效位。
例如，对于`QImage::Format_ARGB32`，其类型解释为`QPixelFormat::UnsignedInteger`，且 `byteOrder()`总是与宿主系统匹配，α 位置 `QPixelFormat::AtBeginning` 意味着 alpha 总能在 `0xFF000000` 处找到。
如果像素格式和主机端序不匹配，必须注意将像素格式布局正确映射到主机内存布局。

### `[constexpr noexcept] uchar QPixelFormat::alphaSize() const`

**作用与语义：**

Alpha通道大小的访问器功能。

### `[constexpr noexcept] QPixelFormat::AlphaUsage QPixelFormat::alphaUsage() const`

**作用与语义：**

访问器功能用于判断是否使用阿尔法通道。
有时像素格式会保留一个alpha通道的位置，因此`alphaSize()`会返回0>，但alpha通道不会被使用或忽略。
例如，对于`QImage::Format_RGB32`，`bitsPerPixel()`是32，因为alpha信道大小为8，但alphaUsage()反映了`QPixelFormat::IgnoresAlpha`。
注意，在这种情况下，未使用的阿尔法通道的 `position` 仍然很重要，因为它会影响色彩通道的位置。

### `[constexpr noexcept] uchar QPixelFormat::bitsPerPixel() const`

**作用与语义：**

访问器函数，用于每像素使用的比特。该函数返回所有颜色通道的总和，大小为阿尔法通道大小。

### `[constexpr noexcept] uchar QPixelFormat::blackSize() const`

**作用与语义：**

黑色/主色通道的访问器功能。

### `[constexpr noexcept] uchar QPixelFormat::blueSize() const`

**作用与语义：**

蓝色通道大小的附件函数。

### `[constexpr noexcept] uchar QPixelFormat::brightnessSize() const`

**作用与语义：**

用于亮度通道大小的访问器功能。

### `[constexpr noexcept] QPixelFormat::ByteOrder QPixelFormat::byteOrder() const`

**作用与语义：**

像素格式的字节顺序决定了各个类型单元的内存布局，如 `typeInterpretation()` 所描述。 这个函数永远不会返回 `QPixelFormat::CurrentSystemEndian`，因为该值在构造函数中被转换为系统的字节序值。 对于带有 `typeInterpretation()` `QPixelFormat::UnsignedByte` 的像素格式，这通常会是 `QPixelFormat::BigEndian`，而其他类型解释通常会反映当前系统的字节序。 如果像素格式的字节顺序与当前系统匹配，则可以使用相同的位掩码和操作读取和操作各个类型单元，而不管主机系统的字节序。例如，对于 `QImage::Format_ARGB32`，其类型解释为 `QPixelFormat::UnsignedInteger`，总是可以通过 `0xFF000000` 掩码读取 alpha，无论主机字节序如何。 如果像素格式与主机字节序不匹配，则必须小心处理。像 `QImage` 这样的类在这些情况下不会交换内部位以匹配主机系统的字节序。

### `[constexpr noexcept] uchar QPixelFormat::channelCount() const`

**作用与语义：**

通道计数的访问器功能。
信道计数表示大小为0的信道（颜色和阿尔法），>。

### `[constexpr noexcept] QPixelFormat::ColorModel QPixelFormat::colorModel() const`

**作用与语义：**

颜色模型的附件功能。
注意，对于`QPixelFormat::YUV`，单个宏像素无法描述。取而代之的是提供YUV格式列表，`bitsPerPixel()`值是从YUV布局中推导出来的。

### `[constexpr noexcept] uchar QPixelFormat::cyanSize() const`

**作用与语义：**

青色通道的访问器功能。

### `[constexpr noexcept] uchar QPixelFormat::greenSize() const`

**作用与语义：**

绿色通道大小的访问器函数。

### `[constexpr noexcept] uchar QPixelFormat::hueSize() const`

**作用与语义：**

Hue通道大小的访问器功能。

### `[constexpr noexcept] uchar QPixelFormat::lightnessSize() const`

**作用与语义：**

用于通道大小的访问器功能。

### `[constexpr noexcept] uchar QPixelFormat::magentaSize() const`

**作用与语义：**

Megenta色彩通道的访问器功能。

### `[constexpr noexcept] QPixelFormat::AlphaPremultiplied QPixelFormat::premultiplied() const`

**作用与语义：**

访问器函数用于判断 alpha 通道是否乘入彩色通道。

### `[constexpr noexcept] uchar QPixelFormat::redSize() const`

**作用与语义：**

用于红色通道大小的访问器函数。

### `[constexpr noexcept] uchar QPixelFormat::saturationSize() const`

**作用与语义：**

用于实现饱和通道大小的访问函数。

### `[constexpr noexcept] QPixelFormat::TypeInterpretation QPixelFormat::typeInterpretation() const`

**作用与语义：**

类型解释决定了每个像素应如何读取。
每个像素被表示为给定类型的一个或多个单元，按顺序在内存中排列。
注意：像素格式的字节顺序和主机系统的字节序只影响每个被读取单元的内存布局，而不影响单元的相对顺序。
例如，`QImage::Format_Mono` 具有每像素 1 位的像素格式和 `QPixelFormat::UnsignedByte` 类型的解释，应当作为单一`byte`读取。同样，`QImage::Format_RGB888` 的像素格式为每像素 24 位，并采用 `QPixelFormat::UnsignedByte` 类型解释，应将其读取为三个连续的 `byte`。
许多`QImage` `formats`是32位，类型解释为`QPixelFormat::UnsignedInteger`，应当作为单一`unsigned int`读取。
对于`QImage::Format_RGBA16FPx4`或`QImage::Format_RGBA32FPx4`等`QPixelFormat::FloatingPoint`格式，类型根据单个颜色/alpha通道的大小决定，16位半浮点格式为`qfloat16`，32位全浮点格式为`float`。

### `[constexpr noexcept] uchar QPixelFormat::yellowSize() const`

**作用与语义：**

黄色通道的访问器功能。

### `[constexpr noexcept] QPixelFormat::YUVLayout QPixelFormat::yuvLayout() const`

**作用与语义：**

`YUVLayout`的访问器功能。由于YUV色彩模型使用宏像素，描述YUV像素格式的颜色通道较为困难。因此，像素的布局被存储为枚举。

### `[constexpr noexcept] QPixelFormat qPixelFormatAlpha(uchar channelSize, QPixelFormat::TypeInterpretation typeInterpretation = QPixelFormat::UnsignedInteger)`

**作用与语义：**

用于创建Alpha格式的构造函数。掩码格式可以通过传递1到`channelSize`来描述。也可以用双重来描述每个像素，将8作为`channelSize`，将`FloatingPoint`作为`typeInterpretation`来定义非常精确的α格式。

### `[constexpr noexcept] QPixelFormat qPixelFormatCmyk(uchar channelSize, uchar alphaSize = 0, QPixelFormat::AlphaUsage alphaUsage = QPixelFormat::IgnoresAlpha, QPixelFormat::AlphaPosition alphaPosition = QPixelFormat::AtBeginning, QPixelFormat::TypeInterpretation typeInterpretation = QPixelFormat::UnsignedInteger)`

**作用与语义：**

用于创建CMYK格式的构造函数。通道数将根据`alphaSize`是否大于零而为4或5。CMYK的色彩通道将全部设置为`channelSize`值。
`alphaUsage` `alphaPosition`和`typeInterpretation`都可以通过同名的访问器访问。

### `[constexpr noexcept] QPixelFormat qPixelFormatGrayscale(uchar channelSize, QPixelFormat::TypeInterpretation typeInterpretation = QPixelFormat::UnsignedInteger)`

**作用与语义：**

用于创建灰度格式的构造函数。单色格式可以通过将1传给`channelSize`来描述。也可以用双倍来描述每个像素，将8转为`channelSize`，`FloatingPoint`转为`typeInterpretation`来定义非常精确的灰阶格式。

### `[constexpr noexcept] QPixelFormat qPixelFormatHsl(uchar channelSize, uchar alphaSize = 0, QPixelFormat::AlphaUsage alphaUsage = QPixelFormat::IgnoresAlpha, QPixelFormat::AlphaPosition alphaPosition = QPixelFormat::AtBeginning, QPixelFormat::TypeInterpretation typeInterpretation = QPixelFormat::FloatingPoint)`

**作用与语义：**

用于创建HSL格式的构造函数。信道数会根据`alphaSize`是否大于0而变为3或4。
`channelSize`会将`hueSize` `saturationSize`和`lightnessSize`设为相同的值。
`alphaUsage` `alphaPosition`和`typeInterpretation`都可以通过同名的访问器访问。

### `[constexpr noexcept] QPixelFormat qPixelFormatHsv(uchar channelSize, uchar alphaSize = 0, QPixelFormat::AlphaUsage alphaUsage = QPixelFormat::IgnoresAlpha, QPixelFormat::AlphaPosition alphaPosition = QPixelFormat::AtBeginning, QPixelFormat::TypeInterpretation typeInterpretation = QPixelFormat::FloatingPoint)`

**作用与语义：**

用于创建HSV格式的构造函数。信道数量会根据`alphaSize`是否大于0而为3或4。
`channelSize`会将`hueSize` `saturationSize`和`brightnessSize`设为相同的值。
`alphaUsage` `alphaPosition`和`typeInterpretation`都可以通过同名的访问器访问。

### `[constexpr noexcept] QPixelFormat qPixelFormatRgba(uchar redSize, uchar greenSize, uchar blueSize, uchar alphaSize, QPixelFormat::AlphaUsage alphaUsage, QPixelFormat::AlphaPosition alphaPosition, QPixelFormat::AlphaPremultiplied premultiplied = QPixelFormat::NotPremultiplied, QPixelFormat::TypeInterpretation typeInterpretation = QPixelFormat::UnsignedInteger)`

**作用与语义：**

构造函数生成RGB像素格式。`redSize` `greenSize` `blueSize`表示每个颜色通道的大小。`alphaSize`描述了alpha通道大小，其位置用`alphaPosition`描述。`alphaUsage`用于判断是否使用α通道。将alpha通道大小设置为8，`alphaUsage`设置为`IgnoresAlpha`，可以创建32位格式，其中RGB通道仅使用24位的总和。`premultiplied` `typeInterpretation` 可用同名的访问器访问。

### `QPixelFormat qPixelFormatYuv(QPixelFormat::YUVLayout yuvLayout, uchar alphaSize = 0, QPixelFormat::AlphaUsage alphaUsage = QPixelFormat::IgnoresAlpha, QPixelFormat::AlphaPosition alphaPosition = QPixelFormat::AtBeginning, QPixelFormat::AlphaPremultiplied premultiplied = QPixelFormat::NotPremultiplied, QPixelFormat::TypeInterpretation typeInterpretation = QPixelFormat::UnsignedByte, QPixelFormat::ByteOrder byteOrder = QPixelFormat::BigEndian)`

**作用与语义：**

构造函数，用于创建描述YUV格式的`QPixelFormat`，`yuvLayout`。`alphaSize`描述潜在Alpha通道的大小，其位置用`alphaPosition`描述。“第一”、“第二”......“第五”通道均设为0。`alphaUsage` `premultiplied` `typeInterpretation`和`byteOrder`将与其他格式相同工作。

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
