# QVideoFrameFormat

> Qt 6.11.1 · Qt Multimedia

## 1. 先建立直觉

**一句话定位：** `QVideoFrameFormat` 是 Qt Multimedia 的“视频帧格式”类型，参与媒体源、设备、格式、播放/采集状态或音视频数据处理。

**模块背景：** Qt Multimedia 提供音频、视频、摄像头、媒体会话和设备访问能力。

### 这是什么

`QVideoFrameFormat` 是 多媒体设备与会话机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 多媒体类型通常把设备、媒体会话、格式、播放状态和异步错误分开。硬件能力、平台后端、权限和资源状态会影响结果；请求成功发起不等于设备已准备好。

**适用场景：** 先检查平台能力和权限，再创建会话/设备，设置格式和源，连接状态与错误信号，执行开始/暂停/停止并在结束后清理。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要假设所有平台支持相同编解码器和格式；不要忽略权限和后端错误；不要在状态未准备好时连续调用控制 API；媒体对象销毁前先停止使用。

## 2. 依赖与对象关系

- 头文件：`#include <QVideoFrameFormat>`
- 继承自：未在类页中列出
- 直接派生类：未在类页中列出

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Multimedia)
target_link_libraries(mytarget PRIVATE Qt6::Multimedia)
```

**继承带来的规则：** 它是值类型或不直接使用 QObject 对象模型，重点放在数据语义、拷贝/移动成本和参数有效性。

### 工作机制

多媒体类型通常把设备、媒体会话、格式、播放状态和异步错误分开。硬件能力、平台后端、权限和资源状态会影响结果；请求成功发起不等于设备已准备好。

### 状态、生命周期和线程

**生命周期：** 设备或媒体对象要在使用期间保持有效，开始前配置输入/输出和格式，停止后释放会话或解除设备占用。状态、媒体状态和错误信号共同决定下一步操作。

**状态与结果：** 区分无媒体、加载中、已加载、播放中、暂停、停止、结束和错误。进度、时长、缓冲和设备可用性不是同一个状态，不能只用一个 bool 表示。

**线程与事件循环：** 媒体对象通常依赖事件循环和平台线程边界；GUI 展示对象在 GUI 线程，后台处理要使用类明确支持的线程模型。

## 3. 直接使用

先检查平台能力和权限，再创建会话/设备，设置格式和源，连接状态与错误信号，执行开始/暂停/停止并在结束后清理。 使用时通常按这个过程组织：准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 公有类型

- `enum ColorRange { ColorRange_Unknown, ColorRange_Video, ColorRange_Full }`
- `enum ColorSpace { ColorSpace_Undefined, ColorSpace_BT601, ColorSpace_BT709, ColorSpace_AdobeRgb, ColorSpace_BT2020 }`
- `enum ColorTransfer { ColorTransfer_Unknown, ColorTransfer_BT709, ColorTransfer_BT601, ColorTransfer_Linear, ColorTransfer_Gamma22, …, ColorTransfer_STD_B67 }`
- `enum Direction { TopToBottom, BottomToTop }`
- `enum PixelFormat { Format_Invalid, Format_ARGB8888, Format_ARGB8888_Premultiplied, Format_XRGB8888, Format_BGRA8888, …, Format_YUV420P10 }`

### 公有函数

- `QVideoFrameFormat()`
- `QVideoFrameFormat(const QSize &size, QVideoFrameFormat::PixelFormat format)`
- `QVideoFrameFormat(const QVideoFrameFormat &other)`
- `QVideoFrameFormat(QVideoFrameFormat &&other)`
- `~QVideoFrameFormat()`
- `QVideoFrameFormat::ColorRange colorRange() const`
- `QVideoFrameFormat::ColorSpace colorSpace() const`
- `QVideoFrameFormat::ColorTransfer colorTransfer() const`
- `int frameHeight() const`
- `qreal frameRate() const`
- `QSize frameSize() const`
- `int frameWidth() const`
- `bool isMirrored() const`
- `bool isValid() const`
- `QVideoFrameFormat::PixelFormat pixelFormat() const`
- `int planeCount() const`
- `QtVideo::Rotation rotation() const`
- `QVideoFrameFormat::Direction scanLineDirection() const`
- `void setColorRange(QVideoFrameFormat::ColorRange range)`
- `void setColorSpace(QVideoFrameFormat::ColorSpace colorSpace)`
- `void setColorTransfer(QVideoFrameFormat::ColorTransfer colorTransfer)`
- `void setFrameRate(qreal rate)`
- `void setFrameSize(const QSize &size)`
- `void setFrameSize(int width, int height)`
- `void setMaxLuminance(float lum)`
- `void setMirrored(bool mirrored)`
- `void setRotation(QtVideo::Rotation angle)`
- `void setScanLineDirection(QVideoFrameFormat::Direction direction)`
- `void setStreamFrameRate(qreal rate)`
- `void setViewport(const QRect &viewport)`
- `qreal streamFrameRate() const`
- `void swap(QVideoFrameFormat &other)`
- `QRect viewport() const`
- `bool operator!=(const QVideoFrameFormat &other) const`
- `QVideoFrameFormat & operator=(QVideoFrameFormat &&other)`
- `QVideoFrameFormat & operator=(const QVideoFrameFormat &other)`
- `bool operator==(const QVideoFrameFormat &other) const`

### 静态公有成员

- `QImage::Format imageFormatFromPixelFormat(QVideoFrameFormat::PixelFormat format)`
- `QVideoFrameFormat::PixelFormat pixelFormatFromImageFormat(QImage::Format format)`
- `QString pixelFormatToString(QVideoFrameFormat::PixelFormat pixelFormat)`

## 5. API 逐个说明

这里直接说明每个公开成员解决什么问题、参数代表什么、返回什么、会改变什么以及使用时容易出现什么问题。每一个公开签名都会有对应的中文解释。

本类共整理 45 个公开成员条目；没有独立长描述的 API 也会根据签名、类型和所属机制给出使用说明。

### `enum QVideoFrameFormat::ColorRange`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QVideoFrameFormat` 暴露的类型声明 `Color、Range`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 属性类型：`:ColorRange`。
- 属性名：`QVideoFrameFormat`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `enum QVideoFrameFormat::ColorSpace`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QVideoFrameFormat` 暴露的类型声明 `Color、Space`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 属性类型：`:ColorSpace`。
- 属性名：`QVideoFrameFormat`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `enum QVideoFrameFormat::Direction`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QVideoFrameFormat` 暴露的类型声明 `Direction`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 属性类型：`:Direction`。
- 属性名：`QVideoFrameFormat`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `enum QVideoFrameFormat::PixelFormat`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QVideoFrameFormat` 暴露的类型声明 `Pixel、格式化`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 属性类型：`:PixelFormat`。
- 属性名：`QVideoFrameFormat`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QVideoFrameFormat::QVideoFrameFormat()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QVideoFrameFormat` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QVideoFrameFormat::QVideoFrameFormat(const QSize &size, QVideoFrameFormat::PixelFormat format)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QVideoFrameFormat` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `size`：类型为 `const QSize &`。没有默认值，调用时必须提供。尺寸或长度，单位通常是像素、字节、元素数或时间，必须结合类型和类的上下文确认。
- 参数 `format`：类型为 `QVideoFrameFormat::PixelFormat`。没有默认值，调用时必须提供。数据格式或显示格式。格式通常会影响解析、像素布局、精度、编码或兼容性。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QVideoFrameFormat::QVideoFrameFormat(const QVideoFrameFormat &other)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QVideoFrameFormat` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `other`：类型为 `const QVideoFrameFormat &`。没有默认值，调用时必须提供。参与比较、合并或交换的另一个对象；要确认它与当前对象属于同一类型或兼容协议。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[constexpr noexcept] QVideoFrameFormat::QVideoFrameFormat(QVideoFrameFormat &&other)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QVideoFrameFormat` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `other`：类型为 `QVideoFrameFormat &&`。没有默认值，调用时必须提供。参与比较、合并或交换的另一个对象；要确认它与当前对象属于同一类型或兼容协议。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] QVideoFrameFormat::~QVideoFrameFormat()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QVideoFrameFormat` 的析构函数。对象销毁时资源、子对象和连接会按 Qt 规则释放；异步对象要先停止任务或使用 deleteLater，避免回调访问已经不存在的实例。

**签名拆解：**

- 返回值：析构函数，无返回值。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QVideoFrameFormat::ColorRange QVideoFrameFormat::colorRange() const`

**API 类别：** 成员函数说明

**中文解读：** `QVideoFrameFormat::colorRange` 用于计算、查询或取得与“color、Range”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QVideoFrameFormat::ColorRange`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QVideoFrameFormat::ColorRange`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QVideoFrameFormat::ColorSpace QVideoFrameFormat::colorSpace() const`

**API 类别：** 成员函数说明

**中文解读：** `QVideoFrameFormat::colorSpace` 用于计算、查询或取得与“color、Space”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QVideoFrameFormat::ColorSpace`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QVideoFrameFormat::ColorSpace`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QVideoFrameFormat::ColorTransfer QVideoFrameFormat::colorTransfer() const`

**API 类别：** 成员函数说明

**中文解读：** `QVideoFrameFormat::colorTransfer` 用于计算、查询或取得与“color、Transfer”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QVideoFrameFormat::ColorTransfer`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QVideoFrameFormat::ColorTransfer`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `int QVideoFrameFormat::frameHeight() const`

**API 类别：** 成员函数说明

**中文解读：** `QVideoFrameFormat::frameHeight` 用于计算、查询或取得与“frame、高度”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `int`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`int`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `qreal QVideoFrameFormat::frameRate() const`

**API 类别：** 成员函数说明

**中文解读：** `QVideoFrameFormat::frameRate` 用于计算、查询或取得与“frame、Rate”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `qreal`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`qreal`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QSize QVideoFrameFormat::frameSize() const`

**API 类别：** 成员函数说明

**中文解读：** `QVideoFrameFormat::frameSize` 用于计算、查询或取得与“frame、尺寸或数量”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QSize`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QSize`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `int QVideoFrameFormat::frameWidth() const`

**API 类别：** 成员函数说明

**中文解读：** `QVideoFrameFormat::frameWidth` 用于计算、查询或取得与“frame、宽度”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `int`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`int`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] QImage::Format QVideoFrameFormat::imageFormatFromPixelFormat(QVideoFrameFormat::PixelFormat format)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `imageFormatFromPixelFormat`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QImage::Format`。
- 参数 `format`：类型为 `QVideoFrameFormat::PixelFormat`。没有默认值，调用时必须提供。数据格式或显示格式。格式通常会影响解析、像素布局、精度、编码或兼容性。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QVideoFrameFormat::isMirrored() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `isMirrored`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QVideoFrameFormat::isValid() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `isValid`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QVideoFrameFormat::PixelFormat QVideoFrameFormat::pixelFormat() const`

**API 类别：** 成员函数说明

**中文解读：** `QVideoFrameFormat::pixelFormat` 用于计算、查询或取得与“pixel、格式化”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QVideoFrameFormat::PixelFormat`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QVideoFrameFormat::PixelFormat`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] QVideoFrameFormat::PixelFormat QVideoFrameFormat::pixelFormatFromImageFormat(QImage::Format format)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `pixelFormatFromImageFormat`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QVideoFrameFormat::PixelFormat`。
- 参数 `format`：类型为 `QImage::Format`。没有默认值，调用时必须提供。数据格式或显示格式。格式通常会影响解析、像素布局、精度、编码或兼容性。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] QString QVideoFrameFormat::pixelFormatToString(QVideoFrameFormat::PixelFormat pixelFormat)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `pixelFormatToString`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QString`。
- 参数 `pixelFormat`：类型为 `QVideoFrameFormat::PixelFormat`。没有默认值，调用时必须提供。传入 `QVideoFrameFormat::PixelFormat` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `int QVideoFrameFormat::planeCount() const`

**API 类别：** 成员函数说明

**中文解读：** `QVideoFrameFormat::planeCount` 用于计算、查询或取得与“plane、数量统计”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `int`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`int`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QtVideo::Rotation QVideoFrameFormat::rotation() const`

**API 类别：** 成员函数说明

**中文解读：** `QVideoFrameFormat::rotation` 用于计算、查询或取得与“rotation”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QtVideo::Rotation`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QtVideo::Rotation`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QVideoFrameFormat::Direction QVideoFrameFormat::scanLineDirection() const`

**API 类别：** 成员函数说明

**中文解读：** `QVideoFrameFormat::scanLineDirection` 用于计算、查询或取得与“scan、行、Direction”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QVideoFrameFormat::Direction`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QVideoFrameFormat::Direction`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QVideoFrameFormat::setColorRange(QVideoFrameFormat::ColorRange range)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setColorRange`。调用它会改变 `QVideoFrameFormat` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `range`：类型为 `QVideoFrameFormat::ColorRange`。没有默认值，调用时必须提供。传入 `QVideoFrameFormat::ColorRange` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QVideoFrameFormat::setColorSpace(QVideoFrameFormat::ColorSpace colorSpace)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setColorSpace`。调用它会改变 `QVideoFrameFormat` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `colorSpace`：类型为 `QVideoFrameFormat::ColorSpace`。没有默认值，调用时必须提供。传入 `QVideoFrameFormat::ColorSpace` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QVideoFrameFormat::setColorTransfer(QVideoFrameFormat::ColorTransfer colorTransfer)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setColorTransfer`。调用它会改变 `QVideoFrameFormat` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `colorTransfer`：类型为 `QVideoFrameFormat::ColorTransfer`。没有默认值，调用时必须提供。传入 `QVideoFrameFormat::ColorTransfer` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QVideoFrameFormat::setFrameRate(qreal rate)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setFrameRate`。调用它会改变 `QVideoFrameFormat` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `rate`：类型为 `qreal`。没有默认值，调用时必须提供。传入 `qreal` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QVideoFrameFormat::setFrameSize(const QSize &size)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setFrameSize`。调用它会改变 `QVideoFrameFormat` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `size`：类型为 `const QSize &`。没有默认值，调用时必须提供。尺寸或长度，单位通常是像素、字节、元素数或时间，必须结合类型和类的上下文确认。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QVideoFrameFormat::setFrameSize(int width, int height)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setFrameSize`。调用它会改变 `QVideoFrameFormat` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `width`：类型为 `int`。没有默认值，调用时必须提供。宽度，通常以像素、字符数或元素数量表示；要确认是否允许 0、负数和超出最大值。
- 参数 `height`：类型为 `int`。没有默认值，调用时必须提供。高度，通常以像素、字符数或元素数量表示；要确认是否允许 0、负数和超出最大值。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QVideoFrameFormat::setMaxLuminance(float lum)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setMaxLuminance`。调用它会改变 `QVideoFrameFormat` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `lum`：类型为 `float`。没有默认值，调用时必须提供。传入 `float` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QVideoFrameFormat::setMirrored(bool mirrored)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setMirrored`。调用它会改变 `QVideoFrameFormat` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `mirrored`：类型为 `bool`。没有默认值，调用时必须提供。传入 `bool` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QVideoFrameFormat::setRotation(QtVideo::Rotation angle)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setRotation`。调用它会改变 `QVideoFrameFormat` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `angle`：类型为 `QtVideo::Rotation`。没有默认值，调用时必须提供。传入 `QtVideo::Rotation` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QVideoFrameFormat::setScanLineDirection(QVideoFrameFormat::Direction direction)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setScanLineDirection`。调用它会改变 `QVideoFrameFormat` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `direction`：类型为 `QVideoFrameFormat::Direction`。没有默认值，调用时必须提供。方向枚举，决定排列、遍历或坐标增长方向；要结合该类定义的枚举值判断实际方向。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QVideoFrameFormat::setStreamFrameRate(qreal rate)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setStreamFrameRate`。调用它会改变 `QVideoFrameFormat` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `rate`：类型为 `qreal`。没有默认值，调用时必须提供。传入 `qreal` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QVideoFrameFormat::setViewport(const QRect &viewport)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setViewport`。调用它会改变 `QVideoFrameFormat` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `viewport`：类型为 `const QRect &`。没有默认值，调用时必须提供。传入 `const QRect &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `qreal QVideoFrameFormat::streamFrameRate() const`

**API 类别：** 成员函数说明

**中文解读：** `QVideoFrameFormat::streamFrameRate` 用于计算、查询或取得与“stream、Frame、Rate”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `qreal`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`qreal`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] void QVideoFrameFormat::swap(QVideoFrameFormat &other)`

**API 类别：** 成员函数说明

**中文解读：** `QVideoFrameFormat::swap` 用于执行与“swap”相关的操作。调用时要先确认当前状态和 `other` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `other`：类型为 `QVideoFrameFormat &`。没有默认值，调用时必须提供。参与比较、合并或交换的另一个对象；要确认它与当前对象属于同一类型或兼容协议。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QRect QVideoFrameFormat::viewport() const`

**API 类别：** 成员函数说明

**中文解读：** `QVideoFrameFormat::viewport` 用于计算、查询或取得与“viewport”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QRect`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QRect`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QVideoFrameFormat::operator!=(const QVideoFrameFormat &other) const`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QVideoFrameFormat` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`bool`。
- 参数 `other`：类型为 `const QVideoFrameFormat &`。没有默认值，调用时必须提供。参与比较、合并或交换的另一个对象；要确认它与当前对象属于同一类型或兼容协议。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] QVideoFrameFormat &QVideoFrameFormat::operator=(QVideoFrameFormat &&other)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QVideoFrameFormat` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QVideoFrameFormat &`。
- 参数 `other`：类型为 `QVideoFrameFormat &&`。没有默认值，调用时必须提供。参与比较、合并或交换的另一个对象；要确认它与当前对象属于同一类型或兼容协议。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QVideoFrameFormat &QVideoFrameFormat::operator=(const QVideoFrameFormat &other)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QVideoFrameFormat` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QVideoFrameFormat &`。
- 参数 `other`：类型为 `const QVideoFrameFormat &`。没有默认值，调用时必须提供。参与比较、合并或交换的另一个对象；要确认它与当前对象属于同一类型或兼容协议。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QVideoFrameFormat::operator==(const QVideoFrameFormat &other) const`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QVideoFrameFormat` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`bool`。
- 参数 `other`：类型为 `const QVideoFrameFormat &`。没有默认值，调用时必须提供。参与比较、合并或交换的另一个对象；要确认它与当前对象属于同一类型或兼容协议。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `enum ColorTransfer { ColorTransfer_Unknown, ColorTransfer_BT709, ColorTransfer_BT601, ColorTransfer_Linear, ColorTransfer_Gamma22, …, ColorTransfer_STD_B67 }`

**API 类别：** 公有类型

**中文解读：** 这是 `QVideoFrameFormat` 暴露的类型声明 `Color、Transfer`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 这是供该类其他 API 使用的枚举/标志类型；传值前要确认枚举值的语义和适用状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

## 6. 深入实践与常见坑

### 生命周期和资源边界

设备或媒体对象要在使用期间保持有效，开始前配置输入/输出和格式，停止后释放会话或解除设备占用。状态、媒体状态和错误信号共同决定下一步操作。

### 状态和错误边界

区分无媒体、加载中、已加载、播放中、暂停、停止、结束和错误。进度、时长、缓冲和设备可用性不是同一个状态，不能只用一个 bool 表示。

### 线程边界

媒体对象通常依赖事件循环和平台线程边界；GUI 展示对象在 GUI 线程，后台处理要使用类明确支持的线程模型。

### 最容易出现的错误

不要假设所有平台支持相同编解码器和格式；不要忽略权限和后端错误；不要在状态未准备好时连续调用控制 API；媒体对象销毁前先停止使用。

### 版本和平台

本文档以 Qt 6.11.1 为依据。涉及平台后端、编解码器、数据库驱动、窗口风格、编译器特性或标注了版本号的 API 时，要把版本条件当作使用约束，而不是只看函数是否能补全。

## 7. 使用边界

`QVideoFrameFormat` 所属机制类型：多媒体设备与会话机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
