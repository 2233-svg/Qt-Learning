# QCamera

> Qt 6.11.1 · Qt Multimedia

## 1. 先建立直觉

**一句话定位：** `QCamera` 是 Qt Multimedia 的“摄像头”类型，参与媒体源、设备、格式、播放/采集状态或音视频数据处理。

**模块背景：** Qt Multimedia 提供音频、视频、摄像头、媒体会话和设备访问能力。

### 这是什么

`QCamera` 是 多媒体设备与会话机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 多媒体类型通常把设备、媒体会话、格式、播放状态和异步错误分开。硬件能力、平台后端、权限和资源状态会影响结果；请求成功发起不等于设备已准备好。

**适用场景：** 先检查平台能力和权限，再创建会话/设备，设置格式和源，连接状态与错误信号，执行开始/暂停/停止并在结束后清理。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要假设所有平台支持相同编解码器和格式；不要忽略权限和后端错误；不要在状态未准备好时连续调用控制 API；媒体对象销毁前先停止使用。

## 2. 依赖与对象关系

- 头文件：`#include <QCamera>`
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

- `enum Error { NoError, CameraError }`
- `enum ExposureMode { ExposureAuto, ExposureManual, ExposurePortrait, ExposureNight, ExposureSports, …, ExposureBarcode }`
- `enum class Feature { ColorTemperature, ExposureCompensation, IsoSensitivity, ManualExposureTime, CustomFocusPoint, FocusDistance }`
- `flags Features`
- `enum FlashMode { FlashOff, FlashOn, FlashAuto }`
- `enum FocusMode { FocusModeAuto, FocusModeAutoNear, FocusModeAutoFar, FocusModeHyperfocal, FocusModeInfinity, FocusModeManual }`
- `enum TorchMode { TorchOff, TorchOn, TorchAuto }`
- `enum WhiteBalanceMode { WhiteBalanceAuto, WhiteBalanceManual, WhiteBalanceSunlight, WhiteBalanceCloudy, WhiteBalanceShade, …, WhiteBalanceSunset }`

### 属性

- `active : bool`
- `cameraDevice : QCameraDevice`
- `cameraFormat : QCameraFormat`
- `colorTemperature : int`
- `customFocusPoint : QPointF`
- `error : Error`
- `errorString : QString`
- `exposureCompensation : float`
- `exposureMode : QCamera::ExposureMode`
- `exposureTime : float`
- `flashMode : QCamera::FlashMode`
- `flashReady : bool`
- `focusDistance : float`
- `focusMode : FocusMode`
- `focusPoint : QPointF`
- `isoSensitivity : int`
- `manualExposureTime : float`
- `manualIsoSensitivity : int`
- `maximumZoomFactor : float`
- `minimumZoomFactor : float`
- `supportedFeatures : Features`
- `torchMode : QCamera::TorchMode`
- `whiteBalanceMode : WhiteBalanceMode`
- `zoomFactor : float`

### 公有函数

- `QCamera(QObject *parent = nullptr)`
- `QCamera(QCameraDevice::Position position, QObject *parent = nullptr)`
- `QCamera(const QCameraDevice &cameraDevice, QObject *parent = nullptr)`
- `virtual ~QCamera() override`
- `QCameraDevice cameraDevice() const`
- `QCameraFormat cameraFormat() const`
- `QMediaCaptureSession * captureSession() const`
- `int colorTemperature() const`
- `QPointF customFocusPoint() const`
- `QCamera::Error error() const`
- `QString errorString() const`
- `float exposureCompensation() const`
- `QCamera::ExposureMode exposureMode() const`
- `float exposureTime() const`
- `QCamera::FlashMode flashMode() const`
- `float focusDistance() const`
- `QCamera::FocusMode focusMode() const`
- `QPointF focusPoint() const`
- `bool isActive() const`
- `bool isAvailable() const`
- `bool isExposureModeSupported(QCamera::ExposureMode mode) const`
- `bool isFlashModeSupported(QCamera::FlashMode mode) const`
- `bool isFlashReady() const`
- `bool isFocusModeSupported(QCamera::FocusMode mode) const`
- `bool isTorchModeSupported(QCamera::TorchMode mode) const`
- `bool isWhiteBalanceModeSupported(QCamera::WhiteBalanceMode mode) const`
- `int isoSensitivity() const`
- `float manualExposureTime() const`
- `int manualIsoSensitivity() const`
- `float maximumExposureTime() const`
- `int maximumIsoSensitivity() const`
- `float maximumZoomFactor() const`
- `float minimumExposureTime() const`
- `int minimumIsoSensitivity() const`
- `float minimumZoomFactor() const`
- `void setCameraDevice(const QCameraDevice &cameraDevice)`
- `void setCameraFormat(const QCameraFormat &format)`
- `void setCustomFocusPoint(const QPointF &point)`
- `void setFocusDistance(float d)`
- `void setFocusMode(QCamera::FocusMode mode)`
- `void setZoomFactor(float factor)`
- `QCamera::Features supportedFeatures() const`
- `QCamera::TorchMode torchMode() const`
- `QCamera::WhiteBalanceMode whiteBalanceMode() const`
- `float zoomFactor() const`

### 公有槽函数

- `void setActive(bool active)`
- `void setAutoExposureTime()`
- `void setAutoIsoSensitivity()`
- `void setColorTemperature(int colorTemperature)`
- `void setExposureCompensation(float ev)`
- `void setExposureMode(QCamera::ExposureMode mode)`
- `void setFlashMode(QCamera::FlashMode mode)`
- `void setManualExposureTime(float seconds)`
- `void setManualIsoSensitivity(int iso)`
- `void setTorchMode(QCamera::TorchMode mode)`
- `void setWhiteBalanceMode(QCamera::WhiteBalanceMode mode)`
- `void start()`
- `void stop()`
- `void zoomTo(float factor, float rate)`

### 信号

- `void activeChanged(bool)`
- `void cameraDeviceChanged()`
- `void cameraFormatChanged()`
- `void colorTemperatureChanged() const`
- `void customFocusPointChanged()`
- `void errorChanged()`
- `void errorOccurred(QCamera::Error error, const QString &errorString)`
- `void exposureCompensationChanged(float value)`
- `void exposureModeChanged()`
- `void exposureTimeChanged(float speed)`
- `void flashModeChanged()`
- `void flashReady(bool ready)`
- `void focusDistanceChanged(float)`
- `void focusModeChanged()`
- `void focusPointChanged()`
- `void isoSensitivityChanged(int value)`
- `void manualExposureTimeChanged(float speed)`
- `void manualIsoSensitivityChanged(int)`
- `void maximumZoomFactorChanged(float)`
- `void minimumZoomFactorChanged(float)`
- `void supportedFeaturesChanged()`
- `void torchModeChanged()`
- `void whiteBalanceModeChanged() const`
- `void zoomFactorChanged(float)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `enum QCamera::Error`

**作用与语义：**

该枚举包含最后一个错误代码。
- `QCamera::NoError`：`0`;未发生错误。
- `QCamera::CameraError`：`1`;发生了错误。

### `enum class QCamera::Featureflags QCamera::Features`

**作用与语义：**

描述相机支持的一组特征。返回的值可以是以下组合：
- `QCamera::Feature::ColorTemperature`：`0x1`;相机支持设置自定义 `colorTemperature`。
- `QCamera::Feature::ExposureCompensation`：`0x2`;相机支持设置自定义`exposureCompensation`。
- `QCamera::Feature::IsoSensitivity`：`0x4`;相机支持设置自定义`isoSensitivity`。
- `QCamera::Feature::ManualExposureTime`：`0x8`;相机支持手动设置曝光时间。
- `QCamera::Feature::CustomFocusPoint`：`0x10`;相机支持设置自定义焦点。
- `QCamera::Feature::FocusDistance`：`0x20`;相机支持设置`focusDistance`属性。
特征类型是QFlag的typedef<Feature>。它存储了特征值的或组合。

### `active : bool`

**作用与语义：**

描述摄像头当前是否处于激活状态。

**如何使用：** 调用 `active()` 读取当前值；它不会修改应用状态。

### `cameraDevice : QCameraDevice`

**作用与语义：**

返回与该相机关联的`QCameraDevice`对象。
切换摄像头设备时，`QCamera`的功能会更新。此外，`QCamera`的控制属性（如`focusMode`、`flashMode`、`focusDistance`、`zoomFactor`）也会更新如下：
- 如果新设备支持某属性，则该属性值应用到摄像头设备上。
- 如果支持某属性但其有效值范围被更改，该属性会被夹在新范围并应用到摄像机设备上。
- 如果新摄像头设备不支持某个属性，属性值将重置为默认值，摄像头设备不做任何更改。

**如何使用：** 调用 `cameraDevice()` 读取当前值；它不会修改应用状态。

### `cameraFormat : QCameraFormat`

**作用与语义：**

返回相机当前使用的相机格式。
注意：在Android目标设备上使用FFMPEG后端时，如果你请求YUV420P格式，你会得到一个全平面的4：2：0 YUV420P或半平面的NV12/NV21。这取决于设备OEM实现的编解码器。
注意：在macOS上，摄像头设备在操作系统的多个应用程序间共享。这意味着其他应用程序可能会覆盖该属性所设定的格式。应用开发者应考虑接收到的视频帧分辨率、像素格式和帧率与该属性描述的不同。该特性在设备格式被其他应用修改时不会改变。该特性描述的格式可以通过重新激活`QCamera`重新应用到设备上。

**如何使用：** 调用 `cameraFormat()` 读取当前值；它不会修改应用状态。

### `colorTemperature : int`

**作用与语义：**

如果当前白平衡模式为`WhiteBalanceManual`，则返回当前色温。对于其他模式，返回值未定义。

**如何使用：** 调用 `colorTemperature()` 读取当前值；它不会修改应用状态。

### `customFocusPoint : QPointF`

**作用与语义：**

该属性表示自定义焦点的位置，在相对帧坐标中：左上帧点`QPointF`（0,0），帧中心`QPointF`（0.5,0.5）。
您可以通过查询带有 Feature.`CustomFocusPoint` 标志的 `supportedFeatures()` 来检查是否支持自定义焦点点。

**如何使用：** 调用 `customFocusPoint()` 读取当前值；它不会修改应用状态。

### `[read-only] error : Error`

**作用与语义：**

返回相机的错误状态。

**如何使用：** 调用 `error()` 读取当前值；它不会修改应用状态。

### `[read-only] errorString : QString`

**作用与语义：**

返回一个人类可读的字符串，描述相机的错误状态。

**如何使用：** 调用 `errorString()` 读取当前值；它不会修改应用状态。

### `exposureCompensation : float`

**作用与语义：**

电动汽车中的暴露补偿。
暴露补偿特性允许调整自动计算的暴露。

**如何使用：** 调用 `exposureCompensation()` 读取当前值；它不会修改应用状态。

### `exposureMode : QCamera::ExposureMode`

**作用与语义：**

该属性决定了所使用的曝光模式。

**如何使用：** 调用 `exposureMode()` 读取当前值；它不会修改应用状态。

### `[read-only] exposureTime : float`

**作用与语义：**

相机曝光时间以秒计。

**如何使用：** 调用 `exposureTime()` 读取当前值；它不会修改应用状态。

### `flashMode : QCamera::FlashMode`

**作用与语义：**

该特性决定了所使用的闪光模式。
如果相机有闪光灯，可以启用特定的闪光灯模式。
给该属性赋予不支持模式无效。
这一特性仅在使用`QImageCapture`捕捉图像时有效。

**如何使用：** 调用 `flashMode()` 读取当前值；它不会修改应用状态。

### `[read-only] flashReady : bool`

**作用与语义：**

提示闪光灯是否已充满电并准备使用。
注意：该函数可通过元对象系统和QML调用。参见`Q_INVOKABLE`。

**如何使用：** 调用 `flashReady()` 读取当前值；它不会修改应用状态。

### `focusDistance : float`

**作用与语义：**

该特性定义了相机设备在手动对焦模式下工作的镜头对焦距离。有效值范围为0到1,0是最近的对焦距离，1是最远的对焦距离。最远点通常在无穷远处，但并非所有设备都如此。
该属性仅在`focusMode`设置为`FocusModeManual`时应用，且`supportedFeatures`包含`Feature::FocusDistance`标志。
如果你在`focusMode`未设置为`QCamera::FocusModeManual`时赋予该属性值，该属性会存储该值，但直到`QCamera::FocusModeManual`激活前不会影响设备。
赋值超出有效范围 [0， 1] 不会影响该属性。
如果`supportedFeatures`不包含`FocusDistance`标志，任何设置该属性的尝试都会被忽略。
当相机处于自动对焦模式时，这一特性不会被更新。
默认值是1。

**如何使用：** 调用 `focusDistance()` 读取当前值；它不会修改应用状态。

### `focusMode : FocusMode`

**作用与语义：**

该特性保留了当前相机的对焦模式。
该特性控制相机设备的对焦模式。在所有自动对焦模式下，相机设备都会持续对焦。
要检查相机设备是否支持特定对焦模式，将相应的`FocusMode`值作为参数传递给`isFocusModeSupported`函数。如果不支持对焦模式值，函数返回为false。为该属性赋予不支持模式则无效。
如果你把对焦模式属性设为`QCamera::FocusModeManual`，镜头会根据`focusDistance`锁定对焦。

**如何使用：** 调用 `focusMode()` 读取当前值；它不会修改应用状态。

### `[read-only] focusPoint : QPointF`

**作用与语义：**

返回自动对焦系统当前用来对焦的点。

**如何使用：** 调用 `focusPoint()` 读取当前值；它不会修改应用状态。

### `[read-only] isoSensitivity : int`

**作用与语义：**

该特性保持传感器ISO的灵敏度。
描述相机当前使用的ISO感光度。

**如何使用：** 调用 `isoSensitivity()` 读取当前值；它不会修改应用状态。

### `manualExposureTime : float`

**作用与语义：**

手动曝光时间设置为`seconds`。

**如何使用：** 调用 `manualExposureTime()` 读取当前值；它不会修改应用状态。

### `manualIsoSensitivity : int`

**作用与语义：**

描述了手动设置的ISO灵敏度。
将此属性设置为-1（默认值），意味着相机会自动调节ISO感光度。

**如何使用：** 调用 `manualIsoSensitivity()` 读取当前值；它不会修改应用状态。

### `[read-only] maximumZoomFactor : float`

**作用与语义：**

返回最大变焦因子。
这会`1.0`在不支持变焦的摄像头上。

**如何使用：** 调用 `maximumZoomFactor()` 读取当前值；它不会修改应用状态。

### `[read-only] minimumZoomFactor : float`

**作用与语义：**

返回最小的缩放因子。
这在不支持变焦的摄像头上会`1.0`。

**如何使用：** 调用 `minimumZoomFactor()` 读取当前值；它不会修改应用状态。

### `[read-only] supportedFeatures : Features`

**作用与语义：**

恢复了这台相机支持的功能。

**如何使用：** 调用 `supportedFeatures()` 读取当前值；它不会修改应用状态。

### `torchMode : QCamera::TorchMode`

**作用与语义：**

该属性表示了所使用的火炬模式。
手电筒是一种持续的光源。它可以在低光环境下用于视频录制。启用手电模式通常会覆盖当前设置的任何闪光灯模式。

**如何使用：** 调用 `torchMode()` 读取当前值；它不会修改应用状态。

### `whiteBalanceMode : WhiteBalanceMode`

**作用与语义：**

返回正在使用的白平衡模式。

**如何使用：** 调用 `whiteBalanceMode()` 读取当前值；它不会修改应用状态。

### `zoomFactor : float`

**作用与语义：**

该属性表示当前的缩放因子。
获取或设置当前的缩放因子。数值会夹在`minimumZoomFactor`和`maximumZoomFactor`之间。

**如何使用：** 调用 `zoomFactor()` 读取当前值；它不会修改应用状态。

### `[explicit] QCamera::QCamera(QObject *parent = nullptr)`

**作用与语义：**

构建一个带有`parent`的QCamera。
如果系统中有多台摄像头可用，则选择默认摄像头。

### `[explicit] QCamera::QCamera(QCameraDevice::Position position, QObject *parent = nullptr)`

**作用与语义：**

构建一个QCamera，使用位于指定`position`的硬件摄像头。
例如，在手机上，它可以轻松选择前置和后置摄像头。
如果指定`position`没有摄像头可用，或者`position` `QCameraDevice::UnspecifiedPosition`，则使用默认摄像头。

### `[explicit] QCamera::QCamera(const QCameraDevice &cameraDevice, QObject *parent = nullptr)`

**作用与语义：**

根据相机描述`cameraDevice`和`parent`构建一个QCamera。

### `[override virtual noexcept] QCamera::~QCamera()`

**作用与语义：**

摧毁了摄像机对象。

### `QMediaCaptureSession *QCamera::captureSession() const`

**作用与语义：**

返回该摄像机所连接的捕获会话，若摄像机未连接捕获会话则返回nullptr。
用`QMediaCaptureSession::setCamera()`把摄像头连接到一个会话。

### `[signal] void QCamera::errorOccurred(QCamera::Error error, const QString &errorString)`

**作用与语义：**

当误差状态变为`error`时，该信号会发出。误差的描述如下为`errorString`。

### `[signal] void QCamera::exposureCompensationChanged(float value)`

**作用与语义：**

电动汽车中的暴露补偿。
暴露补偿特性允许调整自动计算的暴露。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `exposureCompensation` 的变化，不要把它当作普通函数主动调用。

### `float QCamera::exposureTime() const`

**作用与语义：**

返回当前曝光时间（秒数）。
注意：物业暴露时间的获取函数。

### `[signal] void QCamera::exposureTimeChanged(float speed)`

**作用与语义：**

相机曝光时间以秒计。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `exposureTime` 的变化，不要把它当作普通函数主动调用。

### `[signal] void QCamera::flashReady(bool ready)`

**作用与语义：**

提示闪光`ready`状态发生变化。
注意：属性闪存准备的通知信号。

### `[signal] void QCamera::focusModeChanged()`

**作用与语义：**

该特性保留了当前相机的对焦模式。
该特性控制相机设备的对焦模式。在所有自动对焦模式下，相机设备都会持续对焦。
要检查相机设备是否支持特定对焦模式，将相应的`FocusMode`值作为参数传递给`isFocusModeSupported`函数。如果不支持对焦模式值，函数返回为false。为该属性赋予不支持模式则无效。
如果你把对焦模式属性设为`QCamera::FocusModeManual`，镜头会根据`focusDistance`锁定对焦。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `focusMode` 的变化，不要把它当作普通函数主动调用。

### `bool QCamera::isActive() const`

**作用与语义：**

描述摄像头当前是否处于激活状态。

**如何使用：** 调用 `isActive()` 读取当前值；它不会修改应用状态。

### `bool QCamera::isAvailable() const`

**作用与语义：**

如果可以使用摄像机，则返回为真。

### `[invokable] bool QCamera::isExposureModeSupported(QCamera::ExposureMode mode) const`

**作用与语义：**

如果支持曝光`mode`，返回为真。
注意：该函数可通过元对象系统和QML调用。参见`Q_INVOKABLE`。

### `[invokable] bool QCamera::isFlashModeSupported(QCamera::FlashMode mode) const`

**作用与语义：**

如果支持闪光`mode`，则返回为true。
注意：该函数可通过元对象系统和QML调用。参见`Q_INVOKABLE`。

### `[invokable] bool QCamera::isFlashReady() const`

**作用与语义：**

提示闪光灯是否已充满电并准备使用。
注意：该函数可通过元对象系统和QML调用。参见`Q_INVOKABLE`。

**如何使用：** 调用 `isFlashReady()` 读取当前值；它不会修改应用状态。

### `[invokable] bool QCamera::isFocusModeSupported(QCamera::FocusMode mode) const`

**作用与语义：**

如果相机支持对焦`mode`，返回`true`。
如果`FocusModeManual`被报告为支持，则该功能`Feature::FocusDistance`也被暗示支持。
注意：该函数可通过元对象系统和QML调用。参见`Q_INVOKABLE`。

### `[invokable] bool QCamera::isTorchModeSupported(QCamera::TorchMode mode) const`

**作用与语义：**

如果支持火炬`mode`，返回为真。
注意：该函数可通过元对象系统和QML调用。参见`Q_INVOKABLE`。

### `[invokable] bool QCamera::isWhiteBalanceModeSupported(QCamera::WhiteBalanceMode mode) const`

**作用与语义：**

如果支持白平衡`mode`，则返回为真。
注意：该函数可通过元对象系统和QML调用。参见`Q_INVOKABLE`。

### `[signal] void QCamera::isoSensitivityChanged(int value)`

**作用与语义：**

该特性保持传感器ISO的灵敏度。
描述相机当前使用的ISO感光度。

**如何使用：** 调用 `isoSensitivityChanged()` 读取当前值；它不会修改应用状态。

### `float QCamera::manualExposureTime() const`

**作用与语义：**

手动曝光时间以秒数返回，如果相机使用自动曝光时间则返回-1秒。
注意：ExposureTime的获取器功能。

### `float QCamera::maximumExposureTime() const`

**作用与语义：**

最大曝光时间也在几秒内。

### `int QCamera::maximumIsoSensitivity() const`

**作用与语义：**

返回相机支持的最大ISO感光度。

### `float QCamera::minimumExposureTime() const`

**作用与语义：**

几秒钟的最小曝光时间。

### `int QCamera::minimumIsoSensitivity() const`

**作用与语义：**

返回相机支持的最低ISO感光度。

### `[slot] void QCamera::setActive(bool active)`

**作用与语义：**

描述摄像头当前是否处于激活状态。

**如何使用：** 调用 `setActive(...)` 修改 `active`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `[slot] void QCamera::setAutoExposureTime()`

**作用与语义：**

使用自动计算的曝光时间。

### `[slot] void QCamera::setAutoIsoSensitivity()`

**作用与语义：**

开启自动灵敏度。

### `void QCamera::setCameraDevice(const QCameraDevice &cameraDevice)`

**作用与语义：**

返回与该相机关联的`QCameraDevice`对象。
切换摄像头设备时，`QCamera`的功能会更新。此外，`QCamera`的控制属性（如`focusMode`、`flashMode`、`focusDistance`、`zoomFactor`）也会更新如下：
- 如果新设备支持某属性，则该属性值应用到摄像头设备上。
- 如果支持某属性但其有效值范围被更改，该属性会被夹在新范围并应用到摄像机设备上。
- 如果新摄像头设备不支持某个属性，属性值将重置为默认值，摄像头设备不做任何更改。

**如何使用：** 调用 `setCameraDevice(...)` 修改 `cameraDevice`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void QCamera::setCameraFormat(const QCameraFormat &format)`

**作用与语义：**

返回相机当前使用的相机格式。
注意：在Android目标设备上使用FFMPEG后端时，如果你请求YUV420P格式，你会得到一个全平面的4：2：0 YUV420P或半平面的NV12/NV21。这取决于设备OEM实现的编解码器。
注意：在macOS上，摄像头设备在操作系统的多个应用程序间共享。这意味着其他应用程序可能会覆盖该属性所设定的格式。应用开发者应考虑接收到的视频帧分辨率、像素格式和帧率与该属性描述的不同。该特性在设备格式被其他应用修改时不会改变。该特性描述的格式可以通过重新激活`QCamera`重新应用到设备上。

**如何使用：** 调用 `setCameraFormat(...)` 修改 `cameraFormat`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `[slot] void QCamera::setColorTemperature(int colorTemperature)`

**作用与语义：**

如果当前白平衡模式为`WhiteBalanceManual`，则返回当前色温。对于其他模式，返回值未定义。

**如何使用：** 调用 `setColorTemperature(...)` 修改 `colorTemperature`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `[slot] void QCamera::setWhiteBalanceMode(QCamera::WhiteBalanceMode mode)`

**作用与语义：**

返回正在使用的白平衡模式。

**如何使用：** 调用 `setWhiteBalanceMode(...)` 修改 `whiteBalanceMode`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void QCamera::setZoomFactor(float factor)`

**作用与语义：**

该属性表示当前的缩放因子。
获取或设置当前的缩放因子。数值会夹在`minimumZoomFactor`和`maximumZoomFactor`之间。

**如何使用：** 调用 `setZoomFactor(...)` 修改 `zoomFactor`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `[slot] void QCamera::start()`

**作用与语义：**

开始摄像机。
和`setActive`一样（没错）。
如果相机因某种原因无法启动，`errorOccurred()`信号就会发出。

### `[slot] void QCamera::stop()`

**作用与语义：**

停止摄像机。和`setActive`一样（错误）。

### `[slot] void QCamera::zoomTo(float factor, float rate)`

**作用与语义：**

`factor`使用`rate`，可以缩放到缩放因子。
`rate`以每秒2的幂次方表示。以1的速率，从1的变焦因子到4需要2秒。
注意：并非所有相机都支持使用特定变焦率。如果不支持，变焦会尽可能快地进行。

### `enum ExposureMode { ExposureAuto, ExposureManual, ExposurePortrait, ExposureNight, ExposureSports, …, ExposureBarcode }`

**作用与语义：**

- `QCamera::ExposureAuto`：`0`;自动模式。
- `QCamera::ExposureManual`：`1`;手动模式。
- `QCamera::ExposurePortrait`：`2`;人像曝光模式。
- `QCamera::ExposureNight`：`3`;夜间模式。
- `QCamera::ExposureSports`：`4`;点曝光模式。
- `QCamera::ExposureSnow`：`5`;雪暴露模式。
- `QCamera::ExposureBeach`：`6`;海滩暴露模式。
- `QCamera::ExposureAction`：`7`;动作模式。自5.5版本起
- `QCamera::ExposureLandscape`：`8`;横屏模式。自5.5版本起
- `QCamera::ExposureNightPortrait`：`9`;夜间人像模式。自5.5版本起
- `QCamera::ExposureTheatre`：`10`;剧院模式。自5.5版本起
- `QCamera::ExposureSunset`：`11`;日落模式。自5.5起
- `QCamera::ExposureSteadyPhoto`：`12`;稳定拍照模式。自5.5版本起
- `QCamera::ExposureFireworks`：`13`;烟花模式。自5.5版本起
- `QCamera::ExposureParty`：`14`;派对模式。自5.5版本起
- `QCamera::ExposureCandlelight`：`15`;烛光模式。自5.5版本起
- `QCamera::ExposureBarcode`：`16`;条形码模式。自5.5版本起

### `enum class Feature { ColorTemperature, ExposureCompensation, IsoSensitivity, ManualExposureTime, CustomFocusPoint, FocusDistance }`

**作用与语义：**

描述相机支持的一组特征。返回的值可以是以下组合：
- `QCamera::Feature::ColorTemperature`：`0x1`;相机支持设置自定义 `colorTemperature`。
- `QCamera::Feature::ExposureCompensation`：`0x2`;相机支持设置自定义`exposureCompensation`。
- `QCamera::Feature::IsoSensitivity`：`0x4`;相机支持设置自定义`isoSensitivity`。
- `QCamera::Feature::ManualExposureTime`：`0x8`;相机支持手动设置曝光时间。
- `QCamera::Feature::CustomFocusPoint`：`0x10`;相机支持设置自定义焦点。
- `QCamera::Feature::FocusDistance`：`0x20`;相机支持设置`focusDistance`属性。
特征类型是QFlag的typedef<Feature>。它存储了特征值的或组合。

### `flags Features`

**作用与语义：**

描述相机支持的一组特征。返回的值可以是以下组合：
- `QCamera::Feature::ColorTemperature`：`0x1`;相机支持设置自定义 `colorTemperature`。
- `QCamera::Feature::ExposureCompensation`：`0x2`;相机支持设置自定义`exposureCompensation`。
- `QCamera::Feature::IsoSensitivity`：`0x4`;相机支持设置自定义`isoSensitivity`。
- `QCamera::Feature::ManualExposureTime`：`0x8`;相机支持手动设置曝光时间。
- `QCamera::Feature::CustomFocusPoint`：`0x10`;相机支持设置自定义焦点。
- `QCamera::Feature::FocusDistance`：`0x20`;相机支持设置`focusDistance`属性。
特征类型是QFlag的typedef<Feature>。它存储了特征值的或组合。

### `enum FlashMode { FlashOff, FlashOn, FlashAuto }`

**作用与语义：**

- `QCamera::FlashOff`：`0`;闪光灯关闭。
- `QCamera::FlashOn`：`1`;闪光灯亮起。
- `QCamera::FlashAuto`：`2`;自动闪光灯。

### `enum FocusMode { FocusModeAuto, FocusModeAutoNear, FocusModeAutoFar, FocusModeHyperfocal, FocusModeInfinity, FocusModeManual }`

**作用与语义：**

- `QCamera::FocusModeAuto`：`0`;连续自动对焦模式。
- `QCamera::FocusModeAutoNear`：`1`;近距离物体的连续自动对焦模式。
- `QCamera::FocusModeAutoFar`：`2`;远处物体的连续自动对焦模式。
- `QCamera::FocusModeHyperfocal`：`3`;聚焦至超焦距，达到最大景深。从该距离的一半到无限远的所有物体均为可接受的锐利度。
- `QCamera::FocusModeInfinity`：`4`;严格聚焦至无限远。
- `QCamera::FocusModeManual`：`5`;相机镜头对焦距离根据`focusDistance`锁定。

### `enum TorchMode { TorchOff, TorchOn, TorchAuto }`

**作用与语义：**

- `QCamera::TorchOff`：`0`;火炬熄灭。
- `QCamera::TorchOn`：`1`;火炬点燃。
- `QCamera::TorchAuto`：`2`;自动喷灯。

### `enum WhiteBalanceMode { WhiteBalanceAuto, WhiteBalanceManual, WhiteBalanceSunlight, WhiteBalanceCloudy, WhiteBalanceShade, …, WhiteBalanceSunset }`

**作用与语义：**

- `QCamera::WhiteBalanceAuto`：`0`;自动白平衡模式。
- `QCamera::WhiteBalanceManual`：`1`;手动白平衡。在此模式下白平衡应设置为`setColorTemperature()`
- `QCamera::WhiteBalanceSunlight`：`2`;阳光白平衡模式。
- `QCamera::WhiteBalanceCloudy`：`3`;云层白平衡模式。
- `QCamera::WhiteBalanceShade`：`4`;阴影白平衡模式。
- `QCamera::WhiteBalanceTungsten`：`5`;钨（白炽）白平衡模式。
- `QCamera::WhiteBalanceFluorescent`：`6`;荧光白平衡模式。
- `QCamera::WhiteBalanceFlash`：`7`;闪光白平衡模式。
- `QCamera::WhiteBalanceSunset`：`8`;日落白平衡模式。

### `QCameraDevice cameraDevice() const`

**作用与语义：**

返回与该相机关联的`QCameraDevice`对象。
切换摄像头设备时，`QCamera`的功能会更新。此外，`QCamera`的控制属性（如`focusMode`、`flashMode`、`focusDistance`、`zoomFactor`）也会更新如下：
- 如果新设备支持某属性，则该属性值应用到摄像头设备上。
- 如果支持某属性但其有效值范围被更改，该属性会被夹在新范围并应用到摄像机设备上。
- 如果新摄像头设备不支持某个属性，属性值将重置为默认值，摄像头设备不做任何更改。

**如何使用：** 调用 `cameraDevice()` 读取当前值；它不会修改应用状态。

### `QCameraFormat cameraFormat() const`

**作用与语义：**

返回相机当前使用的相机格式。
注意：在Android目标设备上使用FFMPEG后端时，如果你请求YUV420P格式，你会得到一个全平面的4：2：0 YUV420P或半平面的NV12/NV21。这取决于设备OEM实现的编解码器。
注意：在macOS上，摄像头设备在操作系统的多个应用程序间共享。这意味着其他应用程序可能会覆盖该属性所设定的格式。应用开发者应考虑接收到的视频帧分辨率、像素格式和帧率与该属性描述的不同。该特性在设备格式被其他应用修改时不会改变。该特性描述的格式可以通过重新激活`QCamera`重新应用到设备上。

**如何使用：** 调用 `cameraFormat()` 读取当前值；它不会修改应用状态。

### `int colorTemperature() const`

**作用与语义：**

如果当前白平衡模式为`WhiteBalanceManual`，则返回当前色温。对于其他模式，返回值未定义。

**如何使用：** 调用 `colorTemperature()` 读取当前值；它不会修改应用状态。

### `QPointF customFocusPoint() const`

**作用与语义：**

该属性表示自定义焦点的位置，在相对帧坐标中：左上帧点`QPointF`（0,0），帧中心`QPointF`（0.5,0.5）。
您可以通过查询带有 Feature.`CustomFocusPoint` 标志的 `supportedFeatures()` 来检查是否支持自定义焦点点。

**如何使用：** 调用 `customFocusPoint()` 读取当前值；它不会修改应用状态。

### `QCamera::Error error() const`

**作用与语义：**

返回相机的错误状态。

**如何使用：** 调用 `error()` 读取当前值；它不会修改应用状态。

### `QString errorString() const`

**作用与语义：**

返回一个人类可读的字符串，描述相机的错误状态。

**如何使用：** 调用 `errorString()` 读取当前值；它不会修改应用状态。

### `float exposureCompensation() const`

**作用与语义：**

电动汽车中的暴露补偿。
暴露补偿特性允许调整自动计算的暴露。

**如何使用：** 调用 `exposureCompensation()` 读取当前值；它不会修改应用状态。

### `QCamera::ExposureMode exposureMode() const`

**作用与语义：**

该属性决定了所使用的曝光模式。

**如何使用：** 调用 `exposureMode()` 读取当前值；它不会修改应用状态。

### `QCamera::FlashMode flashMode() const`

**作用与语义：**

该特性决定了所使用的闪光模式。
如果相机有闪光灯，可以启用特定的闪光灯模式。
给该属性赋予不支持模式无效。
这一特性仅在使用`QImageCapture`捕捉图像时有效。

**如何使用：** 调用 `flashMode()` 读取当前值；它不会修改应用状态。

### `float focusDistance() const`

**作用与语义：**

该特性定义了相机设备在手动对焦模式下工作的镜头对焦距离。有效值范围为0到1,0是最近的对焦距离，1是最远的对焦距离。最远点通常在无穷远处，但并非所有设备都如此。
该属性仅在`focusMode`设置为`FocusModeManual`时应用，且`supportedFeatures`包含`Feature::FocusDistance`标志。
如果你在`focusMode`未设置为`QCamera::FocusModeManual`时赋予该属性值，该属性会存储该值，但直到`QCamera::FocusModeManual`激活前不会影响设备。
赋值超出有效范围 [0， 1] 不会影响该属性。
如果`supportedFeatures`不包含`FocusDistance`标志，任何设置该属性的尝试都会被忽略。
当相机处于自动对焦模式时，这一特性不会被更新。
默认值是1。

**如何使用：** 调用 `focusDistance()` 读取当前值；它不会修改应用状态。

### `QCamera::FocusMode focusMode() const`

**作用与语义：**

该特性保留了当前相机的对焦模式。
该特性控制相机设备的对焦模式。在所有自动对焦模式下，相机设备都会持续对焦。
要检查相机设备是否支持特定对焦模式，将相应的`FocusMode`值作为参数传递给`isFocusModeSupported`函数。如果不支持对焦模式值，函数返回为false。为该属性赋予不支持模式则无效。
如果你把对焦模式属性设为`QCamera::FocusModeManual`，镜头会根据`focusDistance`锁定对焦。

**如何使用：** 调用 `focusMode()` 读取当前值；它不会修改应用状态。

### `QPointF focusPoint() const`

**作用与语义：**

返回自动对焦系统当前用来对焦的点。

**如何使用：** 调用 `focusPoint()` 读取当前值；它不会修改应用状态。

### `int isoSensitivity() const`

**作用与语义：**

该特性保持传感器ISO的灵敏度。
描述相机当前使用的ISO感光度。

**如何使用：** 调用 `isoSensitivity()` 读取当前值；它不会修改应用状态。

### `int manualIsoSensitivity() const`

**作用与语义：**

描述了手动设置的ISO灵敏度。
将此属性设置为-1（默认值），意味着相机会自动调节ISO感光度。

**如何使用：** 调用 `manualIsoSensitivity()` 读取当前值；它不会修改应用状态。

### `float maximumZoomFactor() const`

**作用与语义：**

返回最大变焦因子。
这会`1.0`在不支持变焦的摄像头上。

**如何使用：** 调用 `maximumZoomFactor()` 读取当前值；它不会修改应用状态。

### `float minimumZoomFactor() const`

**作用与语义：**

返回最小的缩放因子。
这在不支持变焦的摄像头上会`1.0`。

**如何使用：** 调用 `minimumZoomFactor()` 读取当前值；它不会修改应用状态。

### `void setCustomFocusPoint(const QPointF &point)`

**作用与语义：**

该属性表示自定义焦点的位置，在相对帧坐标中：左上帧点`QPointF`（0,0），帧中心`QPointF`（0.5,0.5）。
您可以通过查询带有 Feature.`CustomFocusPoint` 标志的 `supportedFeatures()` 来检查是否支持自定义焦点点。

**如何使用：** 调用 `setCustomFocusPoint(...)` 修改 `customFocusPoint`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setFocusDistance(float d)`

**作用与语义：**

该特性定义了相机设备在手动对焦模式下工作的镜头对焦距离。有效值范围为0到1,0是最近的对焦距离，1是最远的对焦距离。最远点通常在无穷远处，但并非所有设备都如此。
该属性仅在`focusMode`设置为`FocusModeManual`时应用，且`supportedFeatures`包含`Feature::FocusDistance`标志。
如果你在`focusMode`未设置为`QCamera::FocusModeManual`时赋予该属性值，该属性会存储该值，但直到`QCamera::FocusModeManual`激活前不会影响设备。
赋值超出有效范围 [0， 1] 不会影响该属性。
如果`supportedFeatures`不包含`FocusDistance`标志，任何设置该属性的尝试都会被忽略。
当相机处于自动对焦模式时，这一特性不会被更新。
默认值是1。

**如何使用：** 调用 `setFocusDistance(...)` 修改 `focusDistance`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setFocusMode(QCamera::FocusMode mode)`

**作用与语义：**

该特性保留了当前相机的对焦模式。
该特性控制相机设备的对焦模式。在所有自动对焦模式下，相机设备都会持续对焦。
要检查相机设备是否支持特定对焦模式，将相应的`FocusMode`值作为参数传递给`isFocusModeSupported`函数。如果不支持对焦模式值，函数返回为false。为该属性赋予不支持模式则无效。
如果你把对焦模式属性设为`QCamera::FocusModeManual`，镜头会根据`focusDistance`锁定对焦。

**如何使用：** 调用 `setFocusMode(...)` 修改 `focusMode`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `QCamera::Features supportedFeatures() const`

**作用与语义：**

恢复了这台相机支持的功能。

**如何使用：** 调用 `supportedFeatures()` 读取当前值；它不会修改应用状态。

### `QCamera::TorchMode torchMode() const`

**作用与语义：**

该属性表示了所使用的火炬模式。
手电筒是一种持续的光源。它可以在低光环境下用于视频录制。启用手电模式通常会覆盖当前设置的任何闪光灯模式。

**如何使用：** 调用 `torchMode()` 读取当前值；它不会修改应用状态。

### `QCamera::WhiteBalanceMode whiteBalanceMode() const`

**作用与语义：**

返回正在使用的白平衡模式。

**如何使用：** 调用 `whiteBalanceMode()` 读取当前值；它不会修改应用状态。

### `float zoomFactor() const`

**作用与语义：**

该属性表示当前的缩放因子。
获取或设置当前的缩放因子。数值会夹在`minimumZoomFactor`和`maximumZoomFactor`之间。

**如何使用：** 调用 `zoomFactor()` 读取当前值；它不会修改应用状态。

### `void setExposureCompensation(float ev)`

**作用与语义：**

电动汽车中的暴露补偿。
暴露补偿特性允许调整自动计算的暴露。

**如何使用：** 调用 `setExposureCompensation(...)` 修改 `exposureCompensation`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setExposureMode(QCamera::ExposureMode mode)`

**作用与语义：**

该属性决定了所使用的曝光模式。

**如何使用：** 调用 `setExposureMode(...)` 修改 `exposureMode`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setFlashMode(QCamera::FlashMode mode)`

**作用与语义：**

该特性决定了所使用的闪光模式。
如果相机有闪光灯，可以启用特定的闪光灯模式。
给该属性赋予不支持模式无效。
这一特性仅在使用`QImageCapture`捕捉图像时有效。

**如何使用：** 调用 `setFlashMode(...)` 修改 `flashMode`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setManualExposureTime(float seconds)`

**作用与语义：**

手动曝光时间设置为`seconds`。

**如何使用：** 调用 `setManualExposureTime(...)` 修改 `manualExposureTime`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setManualIsoSensitivity(int iso)`

**作用与语义：**

描述了手动设置的ISO灵敏度。
将此属性设置为-1（默认值），意味着相机会自动调节ISO感光度。

**如何使用：** 调用 `setManualIsoSensitivity(...)` 修改 `manualIsoSensitivity`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setTorchMode(QCamera::TorchMode mode)`

**作用与语义：**

该属性表示了所使用的火炬模式。
手电筒是一种持续的光源。它可以在低光环境下用于视频录制。启用手电模式通常会覆盖当前设置的任何闪光灯模式。

**如何使用：** 调用 `setTorchMode(...)` 修改 `torchMode`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void activeChanged(bool)`

**作用与语义：**

描述摄像头当前是否处于激活状态。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `active` 的变化，不要把它当作普通函数主动调用。

### `void cameraDeviceChanged()`

**作用与语义：**

返回与该相机关联的`QCameraDevice`对象。
切换摄像头设备时，`QCamera`的功能会更新。此外，`QCamera`的控制属性（如`focusMode`、`flashMode`、`focusDistance`、`zoomFactor`）也会更新如下：
- 如果新设备支持某属性，则该属性值应用到摄像头设备上。
- 如果支持某属性但其有效值范围被更改，该属性会被夹在新范围并应用到摄像机设备上。
- 如果新摄像头设备不支持某个属性，属性值将重置为默认值，摄像头设备不做任何更改。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `cameraDevice` 的变化，不要把它当作普通函数主动调用。

### `void cameraFormatChanged()`

**作用与语义：**

返回相机当前使用的相机格式。
注意：在Android目标设备上使用FFMPEG后端时，如果你请求YUV420P格式，你会得到一个全平面的4：2：0 YUV420P或半平面的NV12/NV21。这取决于设备OEM实现的编解码器。
注意：在macOS上，摄像头设备在操作系统的多个应用程序间共享。这意味着其他应用程序可能会覆盖该属性所设定的格式。应用开发者应考虑接收到的视频帧分辨率、像素格式和帧率与该属性描述的不同。该特性在设备格式被其他应用修改时不会改变。该特性描述的格式可以通过重新激活`QCamera`重新应用到设备上。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `cameraFormat` 的变化，不要把它当作普通函数主动调用。

### `void colorTemperatureChanged() const`

**作用与语义：**

如果当前白平衡模式为`WhiteBalanceManual`，则返回当前色温。对于其他模式，返回值未定义。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `colorTemperature` 的变化，不要把它当作普通函数主动调用。

### `void customFocusPointChanged()`

**作用与语义：**

该属性表示自定义焦点的位置，在相对帧坐标中：左上帧点`QPointF`（0,0），帧中心`QPointF`（0.5,0.5）。
您可以通过查询带有 Feature.`CustomFocusPoint` 标志的 `supportedFeatures()` 来检查是否支持自定义焦点点。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `customFocusPoint` 的变化，不要把它当作普通函数主动调用。

### `void errorChanged()`

**作用与语义：**

返回相机的错误状态。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `error` 的变化，不要把它当作普通函数主动调用。

### `void exposureModeChanged()`

**作用与语义：**

该属性决定了所使用的曝光模式。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `exposureMode` 的变化，不要把它当作普通函数主动调用。

### `void flashModeChanged()`

**作用与语义：**

该特性决定了所使用的闪光模式。
如果相机有闪光灯，可以启用特定的闪光灯模式。
给该属性赋予不支持模式无效。
这一特性仅在使用`QImageCapture`捕捉图像时有效。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `flashMode` 的变化，不要把它当作普通函数主动调用。

### `void focusDistanceChanged(float)`

**作用与语义：**

该特性定义了相机设备在手动对焦模式下工作的镜头对焦距离。有效值范围为0到1,0是最近的对焦距离，1是最远的对焦距离。最远点通常在无穷远处，但并非所有设备都如此。
该属性仅在`focusMode`设置为`FocusModeManual`时应用，且`supportedFeatures`包含`Feature::FocusDistance`标志。
如果你在`focusMode`未设置为`QCamera::FocusModeManual`时赋予该属性值，该属性会存储该值，但直到`QCamera::FocusModeManual`激活前不会影响设备。
赋值超出有效范围 [0， 1] 不会影响该属性。
如果`supportedFeatures`不包含`FocusDistance`标志，任何设置该属性的尝试都会被忽略。
当相机处于自动对焦模式时，这一特性不会被更新。
默认值是1。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `focusDistance` 的变化，不要把它当作普通函数主动调用。

### `void focusPointChanged()`

**作用与语义：**

返回自动对焦系统当前用来对焦的点。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `focusPoint` 的变化，不要把它当作普通函数主动调用。

### `void manualExposureTimeChanged(float speed)`

**作用与语义：**

手动曝光时间设置为`seconds`。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `manualExposureTime` 的变化，不要把它当作普通函数主动调用。

### `void manualIsoSensitivityChanged(int)`

**作用与语义：**

描述了手动设置的ISO灵敏度。
将此属性设置为-1（默认值），意味着相机会自动调节ISO感光度。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `manualIsoSensitivity` 的变化，不要把它当作普通函数主动调用。

### `void maximumZoomFactorChanged(float)`

**作用与语义：**

返回最大变焦因子。
这会`1.0`在不支持变焦的摄像头上。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `maximumZoomFactor` 的变化，不要把它当作普通函数主动调用。

### `void minimumZoomFactorChanged(float)`

**作用与语义：**

返回最小的缩放因子。
这在不支持变焦的摄像头上会`1.0`。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `minimumZoomFactor` 的变化，不要把它当作普通函数主动调用。

### `void supportedFeaturesChanged()`

**作用与语义：**

恢复了这台相机支持的功能。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `supportedFeatures` 的变化，不要把它当作普通函数主动调用。

### `void torchModeChanged()`

**作用与语义：**

该属性表示了所使用的火炬模式。
手电筒是一种持续的光源。它可以在低光环境下用于视频录制。启用手电模式通常会覆盖当前设置的任何闪光灯模式。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `torchMode` 的变化，不要把它当作普通函数主动调用。

### `void whiteBalanceModeChanged() const`

**作用与语义：**

返回正在使用的白平衡模式。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `whiteBalanceMode` 的变化，不要把它当作普通函数主动调用。

### `void zoomFactorChanged(float)`

**作用与语义：**

该属性表示当前的缩放因子。
获取或设置当前的缩放因子。数值会夹在`minimumZoomFactor`和`maximumZoomFactor`之间。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `zoomFactor` 的变化，不要把它当作普通函数主动调用。

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

`QCamera` 所属机制类型：多媒体设备与会话机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
