# QImageCapture

> Qt 6.11.1 · Qt Multimedia

## 1. 先建立直觉

**一句话定位：** `QImageCapture` 是 Qt Multimedia 的“图像采集”类型，参与媒体源、设备、格式、播放/采集状态或音视频数据处理。

**模块背景：** Qt Multimedia 提供音频、视频、摄像头、媒体会话和设备访问能力。

### 这是什么

`QImageCapture` 是 多媒体设备与会话机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 多媒体类型通常把设备、媒体会话、格式、播放状态和异步错误分开。硬件能力、平台后端、权限和资源状态会影响结果；请求成功发起不等于设备已准备好。

**适用场景：** 先检查平台能力和权限，再创建会话/设备，设置格式和源，连接状态与错误信号，执行开始/暂停/停止并在结束后清理。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要假设所有平台支持相同编解码器和格式；不要忽略权限和后端错误；不要在状态未准备好时连续调用控制 API；媒体对象销毁前先停止使用。

## 2. 依赖与对象关系

- 头文件：`#include <QImageCapture>`
- 继承自：QObject
- 直接派生类：未在类页中列出

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Multimedia)
target_link_libraries(mytarget PRIVATE Qt6::Multimedia)
```

**继承带来的规则：** 它属于 QObject 对象模型（直接或间接继承 QObject），因此父对象、信号与槽、事件循环和线程归属是使用主线。

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

- `enum Error { NoError, NotReadyError, ResourceError, OutOfSpaceError, NotSupportedFeatureError, FormatError }`
- `enum FileFormat { UnspecifiedFormat, JPEG, PNG, WebP, Tiff }`
- `enum Quality { VeryLowQuality, LowQuality, NormalQuality, HighQuality, VeryHighQuality }`

### 属性

- `error : Error`
- `errorString : QString`
- `fileFormat : FileFormat`
- `metaData : QMediaMetaData`
- `quality : Quality`
- `readyForCapture : bool`
- `supportedFormats : const QList<FileFormat>`

### 公有函数

- `QImageCapture(QObject *parent = nullptr)`
- `virtual ~QImageCapture() override`
- `void addMetaData(const QMediaMetaData &metaData)`
- `QMediaCaptureSession * captureSession() const`
- `QImageCapture::Error error() const`
- `QString errorString() const`
- `QImageCapture::FileFormat fileFormat() const`
- `bool isAvailable() const`
- `bool isReadyForCapture() const`
- `QMediaMetaData metaData() const`
- `QImageCapture::Quality quality() const`
- `QSize resolution() const`
- `void setFileFormat(QImageCapture::FileFormat format)`
- `void setMetaData(const QMediaMetaData &metaData)`
- `void setQuality(QImageCapture::Quality quality)`
- `void setResolution(const QSize &resolution)`
- `void setResolution(int width, int height)`

### 公有槽函数

- `int capture()`
- `int captureToFile(const QString &file = QString())`

### 信号

- `void errorChanged()`
- `void errorOccurred(int id, QImageCapture::Error error, const QString &errorString)`
- `void fileFormatChanged()`
- `void imageAvailable(int id, const QVideoFrame &frame)`
- `void imageCaptured(int id, const QImage &preview)`
- `void imageExposed(int id)`
- `void imageMetadataAvailable(int id, const QMediaMetaData &metaData)`
- `void imageSaved(int id, const QString &fileName)`
- `void metaDataChanged()`
- `void qualityChanged()`
- `void readyForCaptureChanged(bool ready)`
- `void resolutionChanged()`

### 静态公有成员

- `QString fileFormatDescription(QImageCapture::FileFormat f)`
- `QString fileFormatName(QImageCapture::FileFormat f)`
- `QList<QImageCapture::FileFormat> supportedFormats()`

## 5. API 逐个说明

这里直接说明每个公开成员解决什么问题、参数代表什么、返回什么、会改变什么以及使用时容易出现什么问题。每一个公开签名都会有对应的中文解释。

本类共整理 44 个公开成员条目；没有独立长描述的 API 也会根据签名、类型和所属机制给出使用说明。

### `enum QImageCapture::FileFormat`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QImageCapture` 暴露的类型声明 `File、格式化`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 属性类型：`:FileFormat`。
- 属性名：`QImageCapture`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `enum QImageCapture::Quality`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QImageCapture` 暴露的类型声明 `Quality`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 属性类型：`:Quality`。
- 属性名：`QImageCapture`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[read-only] error : Error`

**API 类别：** 属性说明

**中文解读：** 这是 `QImageCapture` 的状态/能力属性。通常通过 `error()` 查询；它主要用于决定后续操作是否可执行，不能把查询结果当成永久事实，状态变化要结合对应的 `...Changed` 信号或文档说明。

**签名拆解：**

- 属性类型：`Error`。
- 属性名：`error`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[read-only] errorString : QString`

**API 类别：** 属性说明

**中文解读：** 这是 `QImageCapture` 的状态/能力属性。通常通过 `errorString()` 查询；它主要用于决定后续操作是否可执行，不能把查询结果当成永久事实，状态变化要结合对应的 `...Changed` 信号或文档说明。

**签名拆解：**

- 属性类型：`QString`。
- 属性名：`errorString`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `fileFormat : FileFormat`

**API 类别：** 属性说明

**中文解读：** 这是 `QImageCapture` 的配置属性。初始化或状态切换时通过 `setFileFormat(...)` 设置，之后用 `fileFormat()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`FileFormat`。
- 属性名：`fileFormat`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `metaData : QMediaMetaData`

**API 类别：** 属性说明

**中文解读：** 这是 `QImageCapture` 的配置属性。初始化或状态切换时通过 `setMetaData(...)` 设置，之后用 `metaData()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`QMediaMetaData`。
- 属性名：`metaData`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `quality : Quality`

**API 类别：** 属性说明

**中文解读：** 这是 `QImageCapture` 的配置属性。初始化或状态切换时通过 `setQuality(...)` 设置，之后用 `quality()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`Quality`。
- 属性名：`quality`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[read-only] readyForCapture : bool`

**API 类别：** 属性说明

**中文解读：** 这是 `QImageCapture` 的状态/能力属性。通常通过 `readyForCapture()` 查询；它主要用于决定后续操作是否可执行，不能把查询结果当成永久事实，状态变化要结合对应的 `...Changed` 信号或文档说明。

**签名拆解：**

- 属性类型：`bool`。
- 属性名：`readyForCapture`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[read-only] supportedFormats : const QList<FileFormat>`

**API 类别：** 属性说明

**中文解读：** 这是 `QImageCapture` 的状态/能力属性。通常通过 `supportedFormats()` 查询；它主要用于决定后续操作是否可执行，不能把查询结果当成永久事实，状态变化要结合对应的 `...Changed` 信号或文档说明。

**签名拆解：**

- 属性类型：`const QList<FileFormat>`。
- 属性名：`supportedFormats`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[explicit] QImageCapture::QImageCapture(QObject *parent = nullptr)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QImageCapture` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `parent`：类型为 `QObject *`。默认值为 `nullptr`。父对象。设置后通常由父对象负责销毁子对象；只有在对象确实应挂入这棵对象树时才传入。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual noexcept] QImageCapture::~QImageCapture()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QImageCapture` 的析构函数。对象销毁时资源、子对象和连接会按 Qt 规则释放；异步对象要先停止任务或使用 deleteLater，避免回调访问已经不存在的实例。

**签名拆解：**

- 返回值：析构函数，无返回值。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QImageCapture::addMetaData(const QMediaMetaData &metaData)`

**API 类别：** 成员函数说明

**中文解读：** 这是向 `QImageCapture` 添加依赖、数据或子对象的 API `addMetaData`。注意对象所有权、重复添加和添加后的通知；如果对应有 remove/take 接口，要明确谁负责移除后的生命周期。

**签名拆解：**

- 返回值：`void`。
- 参数 `metaData`：类型为 `const QMediaMetaData &`。没有默认值，调用时必须提供。传入 `const QMediaMetaData &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[slot] int QImageCapture::capture()`

**API 类别：** 成员函数说明

**中文解读：** 这是可被信号连接或元对象调用的槽 `capture`。它适合作为一次动作或状态响应的入口；如果调用可能耗时，不要直接阻塞 GUI 事件循环，应把工作拆分或移动到 worker。

**签名拆解：**

- 返回值：`int`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QMediaCaptureSession *QImageCapture::captureSession() const`

**API 类别：** 成员函数说明

**中文解读：** `QImageCapture::captureSession` 用于计算、查询或取得与“capture、Session”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QMediaCaptureSession *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QMediaCaptureSession *`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[slot] int QImageCapture::captureToFile(const QString &file = QString())`

**API 类别：** 成员函数说明

**中文解读：** 这是可被信号连接或元对象调用的槽 `captureToFile`。它适合作为一次动作或状态响应的入口；如果调用可能耗时，不要直接阻塞 GUI 事件循环，应把工作拆分或移动到 worker。

**签名拆解：**

- 返回值：`int`。
- 参数 `file`：类型为 `const QString &`。默认值为 `QString()`。文件或设备对象。要确认打开状态、读写模式、当前位置和错误状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[signal] void QImageCapture::errorOccurred(int id, QImageCapture::Error error, const QString &errorString)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QImageCapture` 发出的通知信号 `errorOccurred`。应用代码通常只连接它，不直接调用它；信号参数描述发生了什么，槽函数中读取相关状态并尽快返回。异步类的完成、错误和状态变化通常都从信号开始处理。

**签名拆解：**

- 返回值：`void`。
- 参数 `id`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `error`：类型为 `QImageCapture::Error`。没有默认值，调用时必须提供。错误输出对象或错误状态。解析/执行后要检查它，而不能只看主返回值。
- 参数 `errorString`：类型为 `const QString &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] QString QImageCapture::fileFormatDescription(QImageCapture::FileFormat f)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `fileFormatDescription`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QString`。
- 参数 `f`：类型为 `QImageCapture::FileFormat`。没有默认值，调用时必须提供。传入 `QImageCapture::FileFormat` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] QString QImageCapture::fileFormatName(QImageCapture::FileFormat f)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `fileFormatName`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QString`。
- 参数 `f`：类型为 `QImageCapture::FileFormat`。没有默认值，调用时必须提供。传入 `QImageCapture::FileFormat` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[signal] void QImageCapture::imageAvailable(int id, const QVideoFrame &frame)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QImageCapture` 发出的通知信号 `imageAvailable`。应用代码通常只连接它，不直接调用它；信号参数描述发生了什么，槽函数中读取相关状态并尽快返回。异步类的完成、错误和状态变化通常都从信号开始处理。

**签名拆解：**

- 返回值：`void`。
- 参数 `id`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `frame`：类型为 `const QVideoFrame &`。没有默认值，调用时必须提供。传入 `const QVideoFrame &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[signal] void QImageCapture::imageCaptured(int id, const QImage &preview)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QImageCapture` 发出的通知信号 `imageCaptured`。应用代码通常只连接它，不直接调用它；信号参数描述发生了什么，槽函数中读取相关状态并尽快返回。异步类的完成、错误和状态变化通常都从信号开始处理。

**签名拆解：**

- 返回值：`void`。
- 参数 `id`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `preview`：类型为 `const QImage &`。没有默认值，调用时必须提供。传入 `const QImage &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[signal] void QImageCapture::imageExposed(int id)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QImageCapture` 发出的通知信号 `imageExposed`。应用代码通常只连接它，不直接调用它；信号参数描述发生了什么，槽函数中读取相关状态并尽快返回。异步类的完成、错误和状态变化通常都从信号开始处理。

**签名拆解：**

- 返回值：`void`。
- 参数 `id`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[signal] void QImageCapture::imageMetadataAvailable(int id, const QMediaMetaData &metaData)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QImageCapture` 发出的通知信号 `imageMetadataAvailable`。应用代码通常只连接它，不直接调用它；信号参数描述发生了什么，槽函数中读取相关状态并尽快返回。异步类的完成、错误和状态变化通常都从信号开始处理。

**签名拆解：**

- 返回值：`void`。
- 参数 `id`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `metaData`：类型为 `const QMediaMetaData &`。没有默认值，调用时必须提供。传入 `const QMediaMetaData &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[signal] void QImageCapture::imageSaved(int id, const QString &fileName)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QImageCapture` 发出的通知信号 `imageSaved`。应用代码通常只连接它，不直接调用它；信号参数描述发生了什么，槽函数中读取相关状态并尽快返回。异步类的完成、错误和状态变化通常都从信号开始处理。

**签名拆解：**

- 返回值：`void`。
- 参数 `id`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `fileName`：类型为 `const QString &`。没有默认值，调用时必须提供。文件名或路径。优先使用 Qt 的路径 API 拼接和规范化，不要手写平台分隔符。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QImageCapture::isAvailable() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `isAvailable`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[signal] void QImageCapture::readyForCaptureChanged(bool ready)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QImageCapture` 发出的通知信号 `readyForCaptureChanged`。应用代码通常只连接它，不直接调用它；信号参数描述发生了什么，槽函数中读取相关状态并尽快返回。异步类的完成、错误和状态变化通常都从信号开始处理。

**签名拆解：**

- 返回值：`void`。
- 参数 `ready`：类型为 `bool`。没有默认值，调用时必须提供。传入 `bool` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QSize QImageCapture::resolution() const`

**API 类别：** 成员函数说明

**中文解读：** `QImageCapture::resolution` 用于计算、查询或取得与“resolution”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QSize`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QSize`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[signal] void QImageCapture::resolutionChanged()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QImageCapture` 发出的通知信号 `resolutionChanged`。应用代码通常只连接它，不直接调用它；信号参数描述发生了什么，槽函数中读取相关状态并尽快返回。异步类的完成、错误和状态变化通常都从信号开始处理。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QImageCapture::setFileFormat(QImageCapture::FileFormat format)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setFileFormat`。调用它会改变 `QImageCapture` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `format`：类型为 `QImageCapture::FileFormat`。没有默认值，调用时必须提供。数据格式或显示格式。格式通常会影响解析、像素布局、精度、编码或兼容性。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QImageCapture::setMetaData(const QMediaMetaData &metaData)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setMetaData`。调用它会改变 `QImageCapture` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `metaData`：类型为 `const QMediaMetaData &`。没有默认值，调用时必须提供。传入 `const QMediaMetaData &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QImageCapture::setQuality(QImageCapture::Quality quality)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setQuality`。调用它会改变 `QImageCapture` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `quality`：类型为 `QImageCapture::Quality`。没有默认值，调用时必须提供。传入 `QImageCapture::Quality` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QImageCapture::setResolution(const QSize &resolution)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setResolution`。调用它会改变 `QImageCapture` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `resolution`：类型为 `const QSize &`。没有默认值，调用时必须提供。传入 `const QSize &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QImageCapture::setResolution(int width, int height)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setResolution`。调用它会改变 `QImageCapture` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `width`：类型为 `int`。没有默认值，调用时必须提供。宽度，通常以像素、字符数或元素数量表示；要确认是否允许 0、负数和超出最大值。
- 参数 `height`：类型为 `int`。没有默认值，调用时必须提供。高度，通常以像素、字符数或元素数量表示；要确认是否允许 0、负数和超出最大值。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] QList<QImageCapture::FileFormat> QImageCapture::supportedFormats()`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `supportedFormats`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QList<QImageCapture::FileFormat>`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `enum Error { NoError, NotReadyError, ResourceError, OutOfSpaceError, NotSupportedFeatureError, FormatError }`

**API 类别：** 公有类型

**中文解读：** 这是 `QImageCapture` 暴露的类型声明 `错误`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 这是供该类其他 API 使用的枚举/标志类型；传值前要确认枚举值的语义和适用状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QImageCapture::Error error() const`

**API 类别：** 公有函数

**中文解读：** `QImageCapture::error` 用于计算、查询或取得与“错误”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QImageCapture::Error`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QImageCapture::Error`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString errorString() const`

**API 类别：** 公有函数

**中文解读：** `QImageCapture::errorString` 用于计算、查询或取得与“错误、字符串”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QString`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QString`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QImageCapture::FileFormat fileFormat() const`

**API 类别：** 公有函数

**中文解读：** `QImageCapture::fileFormat` 用于计算、查询或取得与“file、格式化”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QImageCapture::FileFormat`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QImageCapture::FileFormat`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool isReadyForCapture() const`

**API 类别：** 公有函数

**中文解读：** 这是查询 API `isReadyForCapture`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QMediaMetaData metaData() const`

**API 类别：** 公有函数

**中文解读：** `QImageCapture::metaData` 用于计算、查询或取得与“meta、数据访问”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QMediaMetaData`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QMediaMetaData`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QImageCapture::Quality quality() const`

**API 类别：** 公有函数

**中文解读：** `QImageCapture::quality` 用于计算、查询或取得与“quality”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QImageCapture::Quality`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QImageCapture::Quality`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void errorChanged()`

**API 类别：** 信号

**中文解读：** 这是状态变化通知 `errorChanged`。应用代码通常连接它而不是直接调用它；收到通知后读取当前值并更新依赖对象，不要假设通知一定只发一次或已经代表业务操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void fileFormatChanged()`

**API 类别：** 信号

**中文解读：** 这是状态变化通知 `fileFormatChanged`。应用代码通常连接它而不是直接调用它；收到通知后读取当前值并更新依赖对象，不要假设通知一定只发一次或已经代表业务操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void metaDataChanged()`

**API 类别：** 信号

**中文解读：** 这是状态变化通知 `metaDataChanged`。应用代码通常连接它而不是直接调用它；收到通知后读取当前值并更新依赖对象，不要假设通知一定只发一次或已经代表业务操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void qualityChanged()`

**API 类别：** 信号

**中文解读：** 这是状态变化通知 `qualityChanged`。应用代码通常连接它而不是直接调用它；收到通知后读取当前值并更新依赖对象，不要假设通知一定只发一次或已经代表业务操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

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

`QImageCapture` 所属机制类型：多媒体设备与会话机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
