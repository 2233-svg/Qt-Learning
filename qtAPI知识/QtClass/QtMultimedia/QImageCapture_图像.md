# QImageCapture：从媒体会话异步拍照并取得图像结果

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QImageCapture>`  
> 所属模块：`Qt6::Multimedia`  
> 继承：`QObject`

## 它解决什么问题

`QImageCapture` 把摄像头视频流中的“一次拍照”建模成独立的异步操作。它负责向当前 `QMediaCaptureSession` 请求拍照，并按需要：

- 只把结果交给应用，供预览、图像处理或上传；
- 把结果编码后保存到文件；
- 通过信号报告曝光、预览图、元数据、视频帧和保存完成；
- 通过整数 ID 把并发或排队中的一次拍照与后续结果对应起来。

它不是摄像头设备本身，也不是连续视频帧回调接口。摄像头由 `QCamera` 提供，`QImageCapture` 通过 `QMediaCaptureSession` 使用该摄像头：

```text
QCamera
   |
   v
QMediaCaptureSession ---- QImageCapture
   |                           |
   v                           v
预览输出                    imageCaptured / imageSaved
```

## 典型使用场景

- 相机应用点击快门后同时显示预览并保存原图；
- 扫描应用拍摄文档，收到 `imageCaptured` 后裁剪、矫正和 OCR；
- 需要保留平台提供的原始 `QVideoFrame`，交给 GPU 或自定义处理器；
- 拍照后把 `QMediaMetaData` 中的拍摄信息写入业务记录；
- 连续点击快门时，用返回的 ID 区分每次请求的完成和失败。

## 基本接入方式

```cpp
auto *session = new QMediaCaptureSession(this);
auto *camera = new QCamera(QMediaDevices::defaultVideoInput(), this);
auto *capture = new QImageCapture(this);

session->setCamera(camera);
session->setImageCapture(capture);

connect(capture, &QImageCapture::imageCaptured,
        this, [](int id, const QImage &preview) {
    qDebug() << "preview for capture" << id << preview.size();
});

connect(capture, &QImageCapture::imageSaved,
        this, [](int id, const QString &fileName) {
    qDebug() << "saved" << id << fileName;
});

connect(capture, &QImageCapture::errorOccurred,
        this, [](int id, QImageCapture::Error error,
                 const QString &message) {
    qWarning() << "capture failed" << id << error << message;
});

if (capture->isReadyForCapture())
    capture->captureToFile(QStringLiteral("photo.jpg"));
```

调用 `capture()` 时只请求图像结果，不指定保存路径。调用 `captureToFile()` 时请求结果并保存；两者都应按异步操作处理，不能把返回的整数当作成功标志。

## 生命周期、所有权和会话关系

`QImageCapture` 是 `QObject`，由父对象树管理其生命周期；但它不会拥有 `QCamera` 或 `QMediaCaptureSession`。`QMediaCaptureSession::setImageCapture()` 只是把对象接入会话，替换或销毁 session 不会自动销毁外部创建的 `QImageCapture`。实际工程中通常把相机、session 和 capture 都挂到同一个控制器对象下。

一个 `QImageCapture` 同一时间只属于一个媒体会话。设置到新的 session 时，应同步处理旧 session 的连接关系和正在进行的拍照。销毁 capture 或其会话后，尚未完成的请求不应再被业务代码等待；不要保留指向其结果信号的裸状态。

拍照必须有可用的媒体后端和已连接的相机。`isAvailable()` 表示当前功能是否由后端提供；`isReadyForCapture()` 表示当前可以接受拍照请求。相机存在不等于已经可以拍照，权限、相机启动状态、初始化延迟和后端状态都会影响这两个判断。

## 拍照请求和结果顺序

### `capture()` 与 `captureToFile()`

这两个槽函数返回一个整数 capture ID。ID 用于匹配：

- `imageExposed(id)`：相机已为这次请求曝光；
- `imageCaptured(id, preview)`：得到可供应用使用的 `QImage` 预览；
- `imageMetadataAvailable(id, metaData)`：得到这次图像的元数据；
- `imageAvailable(id, frame)`：得到 `QVideoFrame`；
- `imageSaved(id, fileName)`：文件保存完成；
- `errorOccurred(id, error, errorString)`：这次请求失败。

返回 ID 只代表请求被编号和提交，不能证明图像已经拍到或文件已经写完。若调用时未准备好，后端可能立即报告 `NotReadyError`；调用方仍应以 `errorOccurred` 和状态信号为准。

`captureToFile()` 的参数是文件位置：

- 传空字符串时，由相机后端选择系统默认目录和命名方式；
- 只传文件名、不传完整路径时，图像会保存到默认目录；
- `imageCaptured` 和 `imageSaved` 会报告最终使用的完整路径；
- 路径不可写、空间不足、格式不支持或编码失败时，应处理错误信号。

文件保存是异步的。收到 `imageCaptured` 只能说明图像已经可供应用使用，不能把它当作文件已经落盘；需要持久化完成的业务应等待 `imageSaved`。

### 可能收到哪些信号

后端能力和请求类型会影响信号组合。`imageExposed`、`imageCaptured`、`imageAvailable`、`imageMetadataAvailable` 和 `imageSaved` 不应被假设为每次都全部发出，也不应假设它们在所有平台上拥有完全相同的时间间隔。错误可能在流程中止前或代替某个成功结果发出。

如果应用只关心“拍照成功后得到图像”，连接 `imageCaptured`；如果关心原始视频帧，连接 `imageAvailable`；如果关心文件已经保存，连接 `imageSaved`。不要在多个信号中重复执行业务动作，除非明确需要预览和落盘两个阶段。

## 图像、帧和元数据的边界

`imageCaptured` 给出 `QImage` 预览参数。它适合立即显示、转换或复制保存，但不应把预览尺寸误认为摄像头传感器输出的完整原图尺寸。后端可能提供经过缩放或转换的图像。

`imageAvailable` 给出 `QVideoFrame`。信号参数是常量引用，槽函数若要在信号返回后继续使用，应按 `QVideoFrame` 的值语义复制或立即映射处理。映射、像素格式、内存类型和可读性由帧本身及后端决定，不要假定一定能直接取得 CPU 图像。

`imageMetadataAvailable` 报告后端能提供的拍摄元数据。它可能为空、部分存在或晚于图像信号到达。`QImageCapture::metaData()` 是应用为后续拍摄配置的元数据，不能用来代替每一张图像实际返回的 `imageMetadataAvailable`。

## 格式、质量和分辨率

### 文件格式

`FileFormat` 包括：

| 枚举值 | 含义 |
| --- | --- |
| `UnspecifiedFormat` | 不强制指定，由文件名、后端或默认策略决定。 |
| `JPEG` | JPEG 编码。 |
| `PNG` | PNG 编码。 |
| `WebP` | WebP 编码。 |
| `Tiff` | TIFF 编码。 |

`supportedFormats()` 返回当前 Qt 构建和图像后端支持的格式列表。枚举值存在不代表当前平台一定支持，设置前应检查列表。`setFileFormat()` 只设置编码偏好；不能把不支持的格式变成可用格式。

如果格式未指定，文件扩展名可能参与格式选择，但应用不应只靠扩展名推断最终编码。对跨平台结果有要求时，显式设置一个出现在 `supportedFormats()` 中的格式，并检查错误信号。

### 质量

`Quality` 从 `VeryLowQuality` 到 `VeryHighQuality`。它是编码质量偏好，不是对所有编码器都具有相同数值含义的质量百分比。JPEG、WebP 等有损格式通常更明显地受到影响；无损或特定后端可能忽略部分质量设置。

### 分辨率

`setResolution(const QSize &)` 和 `setResolution(width, height)` 设置拍照分辨率偏好。它不是任意缩放器：摄像头和后端可能选择最接近的受支持尺寸，也可能忽略不支持的尺寸。负数或空尺寸没有可依赖的有效拍摄意义，应使用正的宽高，并通过实际结果验证最终尺寸。

分辨率设置通常应在开始拍照前完成。若拍摄已经进行，再修改配置，修改何时生效由后端决定；不要把它当作对已经提交的请求的即时修改。

## 拍摄元数据的设置

`setMetaData()` 用给定的 `QMediaMetaData` 替换待拍摄图像的元数据配置；`addMetaData()` 把给定项合并到现有配置中。它们影响后续拍摄，不会回写已经完成的图像，也不会保证所有平台都能保存每一种元数据项。

元数据是否写入文件还取决于文件格式和编码器。即使 `imageMetadataAvailable` 报告了某项信息，最终保存文件也可能因格式限制而不包含它。需要可靠保存时，应在应用层额外记录关键字段。

## 错误模型和就绪状态

### `Error`

| 枚举值 | 含义 |
| --- | --- |
| `NoError` | 没有错误。 |
| `NotReadyError` | 当前尚未准备好接受或完成拍照。 |
| `ResourceError` | 摄像头或其他媒体资源不可用。 |
| `OutOfSpaceError` | 保存位置没有足够空间。 |
| `NotSupportedFeatureError` | 当前后端不支持所请求的功能。 |
| `FormatError` | 图像格式或编码参数有问题。 |

`error()` 和 `errorString()` 表示当前错误状态；`errorOccurred()` 带有具体请求 ID，适合在多次拍照同时进行时处理。错误字符串用于展示或日志，不应拿来做程序逻辑判断。

### `readyForCapture`

`readyForCaptureChanged(bool)` 只表示当前是否适合提交新的拍照请求。它不表示上一张图像已经保存，也不保证下一次请求一定成功。界面快门按钮可以据此启用，但仍必须处理异步错误。

## 线程和异步边界

`QImageCapture` 是 `QObject`，应在所属线程调用其槽、读取属性并连接相关对象。媒体后端通常通过 Qt 事件循环异步返回信号，因此必须保持事件循环运行；阻塞所属线程会延迟结果交付，甚至使设备状态无法推进。

图像处理很重时，可以在收到 `imageCaptured` 或 `imageAvailable` 后把值复制到工作线程处理，但不要把 `QImageCapture`、`QCamera` 或 `QMediaCaptureSession` 本身跨线程直接操作。槽中的 `QImage` 和 `QVideoFrame` 参数只在调用期间由信号提供，异步处理应建立自己的数据所有权。

## 常见误区

- 把 `capture()` 的返回值当成成功/失败布尔值；它是请求 ID。
- 未检查 `isReadyForCapture()` 就连续提交请求，导致 `NotReadyError` 或后端排队行为。
- 收到 `imageCaptured` 就认为文件已经保存；落盘应等待 `imageSaved`。
- 假设每次一定收到全部图像信号；不同后端能力不同。
- 把预览 `QImage` 当成传感器的原始完整分辨率。
- 只设置文件扩展名，不检查 `supportedFormats()` 和编码错误。
- 认为 `setMetaData()` 可以保证所有元数据写入所有格式。
- 在工作线程直接调用媒体对象或阻塞媒体对象所属线程。

## API 速查表

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造 | `QImageCapture(QObject *parent = nullptr)` | 创建拍照控制对象。 | 不自动连接摄像头；通常交给父对象管理。 |
| 状态 | `bool isAvailable() const` | 查询当前后端是否提供图像拍摄能力。 | 可用不等于已经连接相机或已经就绪。 |
| 关系 | `QMediaCaptureSession *captureSession() const` | 返回当前所属媒体会话。 | 不转移 session 所有权；可能为空。 |
| 状态 | `Error error() const` | 返回当前错误枚举。 | 多请求场景用 `errorOccurred` 的 ID 关联具体请求。 |
| 状态 | `QString errorString() const` | 返回当前错误说明。 | 适合日志和展示，不要解析文本。 |
| 状态 | `bool isReadyForCapture() const` | 查询当前是否可以提交拍照。 | 仍需处理异步失败。 |
| 设置/查询 | `FileFormat fileFormat() const` | 返回当前文件格式偏好。 | `UnspecifiedFormat` 由后端或文件名决定。 |
| 设置 | `void setFileFormat(FileFormat format)` | 设置保存图像时的编码格式偏好。 | 先检查 `supportedFormats()`。 |
| 查询 | `static QList<FileFormat> supportedFormats()` | 返回当前可用文件格式。 | 平台和构建环境可能不同。 |
| 展示 | `static QString fileFormatName(FileFormat f)` | 返回格式名称。 | 用于界面或日志，不是编码能力检查。 |
| 展示 | `static QString fileFormatDescription(FileFormat f)` | 返回格式描述。 | 适合向用户解释格式。 |
| 设置/查询 | `QSize resolution() const` | 返回请求的拍照分辨率。 | 实际结果可能被后端调整。 |
| 设置 | `void setResolution(const QSize &resolution)` | 设置拍照分辨率偏好。 | 不保证任意尺寸都被支持。 |
| 设置 | `void setResolution(int width, int height)` | 以宽高设置拍照分辨率偏好。 | 使用正数；实际尺寸以结果为准。 |
| 设置/查询 | `Quality quality() const` | 返回编码质量偏好。 | 不是跨编码器统一的质量百分比。 |
| 设置 | `void setQuality(Quality quality)` | 设置编码质量偏好。 | 某些格式或后端可能忽略。 |
| 设置/查询 | `QMediaMetaData metaData() const` | 返回待拍摄图像的元数据配置。 | 不是某张已拍图像的实际元数据。 |
| 设置 | `void setMetaData(const QMediaMetaData &metaData)` | 替换待拍摄图像的元数据配置。 | 只影响后续请求。 |
| 设置 | `void addMetaData(const QMediaMetaData &metaData)` | 合并待拍摄图像的元数据配置。 | 格式和平台可能限制最终写入。 |
| 请求 | `int capture()` | 异步拍照并提供图像结果。 | 返回 capture ID，不是完成结果。 |
| 请求 | `int captureToFile(const QString &location = QString())` | 异步拍照并保存到指定位置。 | 空路径由后端选择；保存完成等 `imageSaved`。 |
| 通知 | `void errorChanged()` | 当前错误属性变化时发出。 | 不携带请求 ID。 |
| 通知 | `void errorOccurred(int id, Error error, const QString &errorString)` | 报告某次拍照请求失败。 | 用 ID 关联具体请求。 |
| 通知 | `void readyForCaptureChanged(bool ready)` | 可拍状态变化时发出。 | 不表示文件已保存。 |
| 通知 | `void metaDataChanged()` | 待拍摄元数据配置变化时发出。 | 不代表实际文件元数据已变化。 |
| 通知 | `void fileFormatChanged()` | 文件格式偏好变化时发出。 | 不代表格式一定被后端接受。 |
| 通知 | `void qualityChanged()` | 质量偏好变化时发出。 | 质量实际效果取决于编码器。 |
| 通知 | `void resolutionChanged()` | 分辨率偏好变化时发出。 | 实际帧可能采用其他受支持尺寸。 |
| 结果 | `void imageExposed(int id)` | 报告指定请求已完成曝光阶段。 | 不等于图像已交付或文件已保存。 |
| 结果 | `void imageCaptured(int id, const QImage &preview)` | 提供拍照得到的 `QImage` 预览。 | 预览尺寸和格式由后端决定。 |
| 结果 | `void imageMetadataAvailable(int id, const QMediaMetaData &metaData)` | 提供该请求的实际元数据。 | 可能为空、部分存在或晚到。 |
| 结果 | `void imageAvailable(int id, const QVideoFrame &frame)` | 提供该请求的 `QVideoFrame`。 | 需要按帧的内存类型和像素格式处理。 |
| 结果 | `void imageSaved(int id, const QString &fileName)` | 报告图像已保存并给出最终文件名。 | 这是确认落盘流程完成的主要信号。 |

## 一句话总结

`QImageCapture` 是连接相机与一次性照片结果的异步控制器：先确认后端和会话就绪，再提交请求并保存 ID，最后分别用图像、元数据、帧、保存和错误信号完成对应的业务阶段。
