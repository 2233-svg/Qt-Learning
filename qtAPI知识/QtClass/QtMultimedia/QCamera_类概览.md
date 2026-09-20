# QCamera：控制系统摄像头的采集设备

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QCamera>`  
> 所属模块：`Qt6::Multimedia`  
> 继承：`QObject`  
> 相关类型：`QCameraDevice`、`QCameraFormat`、`QMediaCaptureSession`、`QCameraPermission`

## 1. 它解决什么问题

`QCamera` 是 Qt Multimedia 中对“一个正在被应用控制的摄像头设备”的抽象。它负责选择物理摄像头、打开或关闭摄像头，并向底层设备提交分辨率、帧率、对焦、曝光、白平衡、闪光灯和手电筒等控制参数。

`QCamera` 本身不是视频帧接收器，也不是照片或视频文件的保存器。典型的采集链路是：

```text
QCameraDevice
        |
        v
     QCamera -----> QMediaCaptureSession -----> QVideoSink
                                              \-> QImageCapture
                                              \-> QMediaRecorder
```

实际项目中通常这样分工：

- `QMediaDevices` 枚举系统中的摄像头；
- `QCameraDevice` 描述某一个摄像头及其可用格式；
- `QCamera` 控制该摄像头的运行状态和成像参数；
- `QMediaCaptureSession` 把摄像头连接到预览、拍照或录像输出；
- `QImageCapture` 拍照；
- `QMediaRecorder` 录制视频；
- `QVideoSink` 接收原始视频帧并自行处理。

因此，单独创建并启动 `QCamera`，并不会自动在界面上显示画面。必须把它连接到 `QMediaCaptureSession`，再给 session 设置视频输出或其它采集对象。

## 2. 典型使用场景

### 2.1 摄像头预览

桌面应用可以把 `QCamera` 接到 `QMediaCaptureSession`，再接到 `QVideoWidget`、`QVideoSink` 或其它视频输出对象。启动摄像头后，视频帧沿 session 流向输出。

### 2.2 拍照和录像

同一个摄像头可以同时连接 `QImageCapture` 和 `QMediaRecorder`，由 session 把实时视频分别送往拍照和录像管线。闪光灯模式只对通过 `QImageCapture` 拍照有实际作用；它不是一个通用的视频照明开关。

### 2.3 扫码、视觉检测和自定义图像处理

把 session 的视频输出接到 `QVideoSink`，在 `videoFrameChanged` 中取得 `QVideoFrame`，再交给二维码识别、目标检测或 OpenCV 等处理模块。处理模块需要自己考虑帧格式、映射、线程和处理耗时，不能让 UI 线程长期阻塞。

### 2.4 手机端的对焦和曝光控制

移动设备通常需要在运行时取得摄像头权限。权限通过后，才适合把 `active` 设为 `true`。对焦点、手动焦距、ISO、曝光时间和色温是否可用，要以当前设备的 `supportedFeatures()` 和各项 `is...Supported()` 查询结果为准。

## 3. 构建与最小连接

```cmake
find_package(Qt6 REQUIRED COMPONENTS Multimedia)
target_link_libraries(mytarget PRIVATE Qt6::Multimedia)
```

```cpp
#include <QCamera>
#include <QCameraPermission>
#include <QMediaCaptureSession>
#include <QMediaDevices>

auto *camera = new QCamera(this);
auto *session = new QMediaCaptureSession(this);

session->setCamera(camera);

connect(camera, &QCamera::errorOccurred,
        this, [](QCamera::Error error, const QString &message) {
            qWarning() << error << message;
        });

// 真实应用应先请求 QCameraPermission，再启动 camera。
camera->start();
```

如果要明确选择设备：

```cpp
const QList<QCameraDevice> devices = QMediaDevices::videoInputs();
if (!devices.isEmpty()) {
    auto *camera = new QCamera(devices.first(), this);
    session->setCamera(camera);
}
```

默认构造的 `QCameraDevice` 表示系统默认摄像头。使用 `QCameraDevice::Position` 构造 `QCamera` 时，Qt 会选择对应位置的摄像头；如果没有匹配设备，仍然要通过 `isAvailable()`、`error()` 和 `errorOccurred()` 检查结果。

## 4. 生命周期、连接和权限边界

### 4.1 `QCamera` 的所有权

`QCamera` 是 `QObject`，不可复制。给它设置 parent 后，父对象负责销毁它。`QCameraDevice` 和 `QCameraFormat` 是值类型，复制它们只复制描述信息，不会复制一个正在运行的摄像头。

`QMediaCaptureSession::setCamera()` 连接的是摄像头对象指针。应用应保证 camera 在 session 使用期间仍然存在。最简单的做法是让 camera 和 session 使用同一个父对象，或者让 session 的生命周期短于 camera。

### 4.2 连接关系不是所有权转移

把 camera 设置到 session 中不会把 camera 的所有权转给 session。切换或解除连接时，session 会更新自己的管线，但摄像头对象仍由原来的所有者管理。

`captureSession()` 返回当前连接的 session；如果没有连接，返回 `nullptr`。连接关系应通过 `QMediaCaptureSession::setCamera()` 建立，而不是尝试直接修改 `QCamera` 内部状态。

### 4.3 权限必须先处理

多数平台要求用户授予摄像头权限。建议在启动摄像头前请求 `QCameraPermission`，并只在回调确认 `Qt::PermissionStatus::Granted` 后调用 `setActive(true)`、`start()` 或其它依赖设备打开的操作。

权限拒绝、系统隐私开关关闭、摄像头被其它程序占用或设备临时不可用，都可能导致启动失败。错误处理至少应同时观察：

- `isAvailable()`：当前设备是否可用；
- `isActive()`：Qt 当前是否认为摄像头已激活；
- `error()`：错误分类；
- `errorString()`：人类可读的错误说明；
- `errorOccurred(...)`：异步错误通知。

WebAssembly 的设备枚举是异步的。不能假定应用创建时 `QMediaDevices::videoInputs()` 已经是最终列表，应响应 `videoInputsChanged()`，并在安全的 HTTPS 上下文中处理权限。

### 4.4 激活是异步资源操作

`start()` 等价于 `setActive(true)`，`stop()` 等价于 `setActive(false)`。调用启动函数只表示发起操作，不应把函数返回当成“摄像头已经稳定出帧”。界面状态应连接 `activeChanged`，错误应连接 `errorOccurred`。

## 5. 设备、格式和状态机

### 5.1 选择设备

`cameraDevice` 保存当前绑定的 `QCameraDevice`。设置默认构造的 `QCameraDevice{}` 会切换到系统默认摄像头。切换设备时，Qt 会重新计算当前摄像头的能力：

- 新设备支持的控制项，会尽量沿用原来的属性值；
- 新设备仍支持该控制项但有效范围变化时，值会被钳制到新范围；
- 新设备不支持该控制项时，属性会恢复默认值，并且不会把该值提交给设备。

因此，切换设备后应重新读取 `supportedFeatures()`、缩放范围、ISO 范围、曝光时间范围和各项模式支持情况，不要继续使用旧设备的缓存能力。

### 5.2 选择格式

`cameraFormat` 由 `QCameraFormat` 描述分辨率、像素格式和最小/最大帧率。可用格式来自 `QCameraDevice::videoFormats()`。建议只从该列表中选择格式，再调用 `setCameraFormat()`。

格式改变可能影响后续预览、拍照和录像管线。格式不是对视频帧做后处理的缩放参数，而是要求摄像头或后端以该采集规格工作。

在 Android 的 FFmpeg 后端中，请求 `YUV420P` 可能得到完整平面 YUV420P，也可能得到半平面 NV12/NV21，具体取决于设备厂商实现。使用 `QVideoFrame` 时应根据实际 `pixelFormat()` 和平面布局处理，不要只根据请求值假定内存布局。

### 5.3 可用性和激活状态

`isAvailable()` 表示摄像头当前能否使用；`isActive()` 表示 camera 当前是否处于激活状态。前者是设备可用性，后者是对象运行状态，二者不是同一个概念。

一个设备可能在枚举时可用，但由于权限、独占占用或后端初始化失败而不能成功激活。因此启动之后仍需处理 `errorOccurred`。

## 6. 成像控制的共同规则

### 6.1 先查询能力，再设置属性

摄像头硬件能力差异很大。不要因为某个平台支持某个模式，就把同一调用无条件地发给所有设备。使用以下两层检查：

1. 用 `supportedFeatures()` 检查色温、曝光补偿、ISO、手动曝光时间、自定义对焦点和手动焦距；
2. 用 `isFocusModeSupported()`、`isExposureModeSupported()`、`isFlashModeSupported()`、`isTorchModeSupported()` 和 `isWhiteBalanceModeSupported()` 检查具体枚举模式。

对不支持的属性赋值通常没有效果，某些值仍可能保存在 `QCamera` 的控制状态中，直到设备或模式变得可用。应用应以相应的 changed 信号和重新读取的属性值确认结果。

### 6.2 自动值、手动值和当前值不同

以下三类 API 不要混为一谈：

- `exposureTime()`、`isoSensitivity()`：摄像头当前实际使用的值；
- `manualExposureTime()`、`manualIsoSensitivity()`：应用请求的手动值；
- `minimum...()`、`maximum...()`：设备支持范围。

自动模式下，当前曝光时间和 ISO 会随场景变化。手动属性不代表当前硬件已经使用该值；是否生效还取决于设备能力、曝光模式和合法范围。

### 6.3 坐标是相对视频帧坐标

`customFocusPoint` 和 `focusPoint` 使用相对帧坐标：

- `(0, 0)` 是视频帧左上角；
- `(0.5, 0.5)` 是视频帧中心；
- `(1, 1)` 是视频帧右下角。

如果用户点击的是经过旋转、镜像、裁剪或缩放后的预览控件，必须先把控件坐标转换回摄像头帧坐标。不能直接把窗口像素坐标传给 `setCustomFocusPoint()`。

## 7. 对焦

### 7.1 对焦模式

`FocusModeAuto`、`FocusModeAutoNear` 和 `FocusModeAutoFar` 都属于连续自动对焦；区别在于自动系统倾向于选择普通、近处或远处目标。

`FocusModeHyperfocal` 把镜头调到超焦距位置，以取得较大的景深；从超焦距一半到无穷远的物体通常都能获得可接受清晰度。

`FocusModeInfinity` 严格对焦到无穷远。

`FocusModeManual` 锁定镜头位置，并使用 `focusDistance` 指定焦距位置。文档规定，如果手动对焦模式被报告为支持，则 `Feature::FocusDistance` 也视为支持。

给 `focusMode` 设置设备不支持的模式没有效果。切换到手动模式前，应先读取或设置合法的 `focusDistance`。

### 7.2 `focusPoint` 与 `customFocusPoint`

`focusPoint` 是自动对焦系统当前实际使用的点，只读。它可能随自动对焦算法变化。

`customFocusPoint` 是应用指定的点。要使用它，设备必须包含 `Feature::CustomFocusPoint`。这个属性表达的是输入帧上的归一化位置，不是屏幕坐标。

### 7.3 手动焦距

`focusDistance` 的合法范围是 `[0, 1]`：

- `0` 表示设备允许的最近焦距；
- `1` 表示设备允许的最远焦距，通常接近无穷远，但不保证所有设备都如此。

如果当前不是 `FocusModeManual`，设置值可以被 camera 保存，但不会立即影响镜头，直到切换到手动模式。超出 `[0, 1]` 的值没有效果；设备不支持 `Feature::FocusDistance` 时，设置会被忽略。自动对焦模式下，camera 不会用自动算法反向更新这个属性。

## 8. 缩放

`minimumZoomFactor()` 和 `maximumZoomFactor()` 给出当前设备的缩放范围。没有缩放能力的设备通常两个值都为 `1.0`。

`zoomFactor` 会被限制在这个范围内。`setZoomFactor(factor)` 使用每秒 1 倍因子的默认速度完成缩放；`zoomTo(factor, rate)` 允许指定速度，`rate` 的单位是每秒变化的二进制幂。

例如，从 1 倍缩放到 4 倍，`rate == 1` 时理论上需要 2 秒，因为每秒按乘以 2 的方式变化。并不是所有摄像头支持指定速率；不支持时，后端会尽可能快地完成缩放。

## 9. 曝光和 ISO

### 9.1 曝光模式

`ExposureMode` 描述摄像头使用的曝光策略：

- `ExposureAuto`：自动曝光；
- `ExposureManual`：手动曝光；
- `ExposurePortrait`：人像；
- `ExposureNight`：夜景；
- `ExposureSports`：运动；
- `ExposureSnow`：雪景；
- `ExposureBeach`：海滩；
- `ExposureAction`：动作；
- `ExposureLandscape`：风景；
- `ExposureNightPortrait`：夜间人像；
- `ExposureTheatre`：剧院；
- `ExposureSunset`：日落；
- `ExposureSteadyPhoto`：稳定拍照；
- `ExposureFireworks`：烟花；
- `ExposureParty`：聚会；
- `ExposureCandlelight`：烛光；
- `ExposureBarcode`：条码。

具体设备通常只实现其中一部分。设置前使用 `isExposureModeSupported()`。

### 9.2 曝光时间

`exposureTime()` 返回摄像头当前曝光时间，单位是秒。`minimumExposureTime()` 和 `maximumExposureTime()` 返回当前设备的支持范围。

`setManualExposureTime(seconds)` 请求手动曝光时间。它只在设备支持 `Feature::ManualExposureTime` 时有意义，且参数应在最小值和最大值之间。`setAutoExposureTime()` 恢复自动计算曝光时间。

`manualExposureTime()` 在使用自动曝光时间时返回 `-1`；这表示“当前没有手动曝光时间”，不是一个可以拿来作为正常曝光秒数使用的值。

### 9.3 ISO

`isoSensitivity()` 返回当前实际使用的 ISO。自动 ISO 下，它可能随着光线变化。

`minimumIsoSensitivity()` 和 `maximumIsoSensitivity()` 返回设备范围。`setManualIsoSensitivity(iso)` 请求固定 ISO，必须先确认 `Feature::IsoSensitivity`。`setAutoIsoSensitivity()` 恢复自动 ISO。

`manualIsoSensitivity()` 的默认值是 `-1`；`-1` 表示摄像头自动调整 ISO。不要把它当作设备支持的 ISO 值。

### 9.4 曝光补偿

`exposureCompensation` 使用 EV 单位，只用于调整自动计算的曝光。它不是直接指定快门时间，也不是手动曝光模式的替代品。

只有设备支持 `Feature::ExposureCompensation` 时，设置才有意义。可接受范围由设备和后端决定，应用应在设置后重新读取属性并监听 `exposureCompensationChanged`。

## 10. 闪光灯、手电筒、白平衡

### 10.1 闪光灯

`flashMode` 有三种模式：

- `FlashOff`：拍照时关闭闪光灯；
- `FlashOn`：拍照时强制使用闪光灯；
- `FlashAuto`：由设备根据场景决定。

不支持的模式赋值没有效果。闪光灯模式只对使用 `QImageCapture` 的图像捕获有作用。`isFlashReady()` 表示闪光灯是否已经充电并可以使用，`flashReady(bool)` 在准备状态变化时通知。

### 10.2 手电筒

`torchMode` 控制连续光源，适合低光照视频录制。开启手电筒通常会覆盖当前的闪光灯模式，两者不是可以独立叠加的两盏灯。

使用前查询 `isTorchModeSupported()`。支持的枚举是 `TorchOff`、`TorchOn` 和 `TorchAuto`。

### 10.3 白平衡和色温

`whiteBalanceMode` 控制图像处理阶段的白平衡。可选模式包括自动、手动、日光、阴天、阴影、钨丝灯、荧光灯、闪光灯和日落。

`setColorTemperature(kelvin)` 的单位是 Kelvin，并且用于手动白平衡。设置大于 0 的色温会自动切换到 `WhiteBalanceManual`；设置为 `0` 会恢复 `WhiteBalanceAuto`。只有 `WhiteBalanceManual` 被设备支持时，色温设置才会产生效果。

`colorTemperature()` 只有在当前白平衡模式为 `WhiteBalanceManual` 时才有定义；其它模式下返回值未定义，不能拿来显示为可靠的当前色温。

## 11. API 逐项说明

### 11.1 枚举和标志

#### `enum QCamera::Error`

| 枚举值 | 含义 |
| --- | --- |
| `NoError` | 没有错误。 |
| `CameraError` | 摄像头发生错误；详细原因通过 `errorString()` 或 `errorOccurred()` 获取。 |

#### `enum QCamera::FocusMode`

| 枚举值 | 含义 |
| --- | --- |
| `FocusModeAuto` | 连续自动对焦。 |
| `FocusModeAutoNear` | 连续自动对焦，并偏向近处目标。 |
| `FocusModeAutoFar` | 连续自动对焦，并偏向远处目标。 |
| `FocusModeHyperfocal` | 对焦到超焦距位置，取得较大景深。 |
| `FocusModeInfinity` | 严格对焦到无穷远。 |
| `FocusModeManual` | 根据 `focusDistance` 锁定镜头焦距。 |

#### `enum QCamera::FlashMode`

| 枚举值 | 含义 |
| --- | --- |
| `FlashOff` | 拍照时关闭闪光灯。 |
| `FlashOn` | 拍照时强制使用闪光灯。 |
| `FlashAuto` | 由摄像头自动决定是否使用闪光灯。 |

#### `enum QCamera::TorchMode`

| 枚举值 | 含义 |
| --- | --- |
| `TorchOff` | 关闭连续光源。 |
| `TorchOn` | 打开连续光源。 |
| `TorchAuto` | 由摄像头自动决定连续光源状态。 |

#### `enum QCamera::ExposureMode`

| 枚举值 | 含义 |
| --- | --- |
| `ExposureAuto` | 自动曝光。 |
| `ExposureManual` | 手动曝光。 |
| `ExposurePortrait` | 人像场景。 |
| `ExposureNight` | 夜景场景。 |
| `ExposureSports` | 运动场景。 |
| `ExposureSnow` | 雪景场景。 |
| `ExposureBeach` | 海滩场景。 |
| `ExposureAction` | 动作场景。 |
| `ExposureLandscape` | 风景场景。 |
| `ExposureNightPortrait` | 夜间人像场景。 |
| `ExposureTheatre` | 剧院场景。 |
| `ExposureSunset` | 日落场景。 |
| `ExposureSteadyPhoto` | 稳定拍照场景。 |
| `ExposureFireworks` | 烟花场景。 |
| `ExposureParty` | 聚会场景。 |
| `ExposureCandlelight` | 烛光场景。 |
| `ExposureBarcode` | 条码场景。 |

#### `enum QCamera::WhiteBalanceMode`

| 枚举值 | 含义 |
| --- | --- |
| `WhiteBalanceAuto` | 自动白平衡。 |
| `WhiteBalanceManual` | 手动白平衡，配合 `setColorTemperature()`。 |
| `WhiteBalanceSunlight` | 日光。 |
| `WhiteBalanceCloudy` | 阴天。 |
| `WhiteBalanceShade` | 阴影。 |
| `WhiteBalanceTungsten` | 钨丝灯或白炽灯。 |
| `WhiteBalanceFluorescent` | 荧光灯。 |
| `WhiteBalanceFlash` | 闪光灯。 |
| `WhiteBalanceSunset` | 日落。 |

#### `enum class QCamera::Feature` 与 `QCamera::Features`

`Features` 是 `QFlags<Feature>`，可以用按位或组合多个能力：

| 标志 | 值 | 表示支持 |
| --- | --- | --- |
| `Feature::ColorTemperature` | `0x1` | 设置自定义 `colorTemperature`。 |
| `Feature::ExposureCompensation` | `0x2` | 设置 `exposureCompensation`。 |
| `Feature::IsoSensitivity` | `0x4` | 设置手动 ISO。 |
| `Feature::ManualExposureTime` | `0x8` | 设置手动曝光时间。 |
| `Feature::CustomFocusPoint` | `0x10` | 设置 `customFocusPoint`。 |
| `Feature::FocusDistance` | `0x20` | 设置 `focusDistance`。 |

### 11.2 属性

#### `active : bool`

描述摄像头是否处于激活状态。使用 `isActive()` 读取，使用 `setActive()`、`start()` 或 `stop()` 控制。激活涉及平台资源操作，结果通过 `activeChanged` 和错误信号异步反映。

#### `cameraDevice : QCameraDevice`

返回或设置当前物理摄像头。设置默认构造的设备对象选择系统默认设备。切换设备会重新计算能力，并可能钳制或重置焦距、缩放和其它控制属性。

#### `cameraFormat : QCameraFormat`

返回或设置当前采集格式。应优先从 `QCameraDevice::videoFormats()` 中选择。格式决定采集分辨率、像素格式和帧率范围。

#### `error : QCamera::Error`

只读错误分类。错误发生时结合 `errorString()` 和 `errorOccurred()` 使用。清除或重新启动对象不代表底层权限、占用或格式问题已经解决。

#### `errorString : QString`

只读的人类可读错误说明。适合写入日志或显示给用户，不应依赖字符串内容做程序逻辑判断。

#### `focusMode : FocusMode`

当前对焦模式。自动模式会持续对焦；手动模式根据 `focusDistance` 锁定焦点。不支持的模式赋值没有效果。

#### `focusPoint : QPointF`

只读的自动对焦系统当前使用点，坐标为相对于视频帧的归一化坐标。它不是预览控件坐标。

#### `customFocusPoint : QPointF`

应用指定的对焦点，坐标范围通常按 `[0, 1] x [0, 1]` 使用。设备必须支持 `Feature::CustomFocusPoint`。点击预览后应先做旋转、镜像和裁剪坐标转换。

#### `focusDistance : float`

手动对焦位置，合法范围是 `[0, 1]`。只有手动对焦模式和 `Feature::FocusDistance` 都满足时才会影响镜头；越界赋值没有效果。

#### `minimumZoomFactor : float`

只读的最小缩放倍数。不支持缩放的设备通常返回 `1.0`。

#### `maximumZoomFactor : float`

只读的最大缩放倍数。不支持缩放的设备通常返回 `1.0`。

#### `zoomFactor : float`

当前缩放倍数。设置值会被限制在最小和最大缩放范围内。

#### `exposureTime : float`

只读的当前曝光时间，单位为秒。自动曝光时会随环境变化。

#### `manualExposureTime : float`

应用请求的手动曝光时间，单位为秒。自动曝光时间时返回 `-1`。它只有在设备支持手动曝光且处于适合的模式时才会实际影响采集。

#### `isoSensitivity : int`

只读的当前实际 ISO。自动 ISO 时会动态变化。

#### `manualIsoSensitivity : int`

应用请求的手动 ISO。默认值 `-1` 表示自动 ISO。

#### `exposureCompensation : float`

以 EV 为单位调整自动曝光。它改变自动曝光的偏置，不等于直接指定曝光时间；设备必须支持 `Feature::ExposureCompensation`。

#### `exposureMode : ExposureMode`

当前曝光策略。应先用 `isExposureModeSupported()` 检查目标模式。

#### `flashReady : bool`

只读，表示闪光灯是否已经充电并准备好。只适用于有闪光灯的设备。

#### `flashMode : FlashMode`

拍照时使用的闪光灯模式。不支持的模式无效；该属性只对 `QImageCapture` 的图像捕获有作用。

#### `torchMode : TorchMode`

连续光源模式，主要用于低光照视频。打开手电筒通常会覆盖闪光灯模式。

#### `whiteBalanceMode : WhiteBalanceMode`

当前白平衡模式。手动模式下使用 `setColorTemperature()` 指定 Kelvin 色温。

#### `colorTemperature : int`

手动白平衡色温，单位 Kelvin。大于 0 的值会切换到手动白平衡，0 会恢复自动白平衡；非手动模式下读取结果未定义。

#### `supportedFeatures : Features`

只读，返回当前摄像头支持的可选控制能力。切换 camera device 后应重新读取。

### 11.3 构造、查询和设备配置

#### `QCamera(QObject *parent = nullptr)`

创建一个使用系统默认摄像头的 camera 对象。默认摄像头仍可能不可用或需要权限。

#### `QCamera(QCameraDevice::Position position, QObject *parent = nullptr)`

创建一个使用指定物理位置摄像头的对象，例如前置或后置位置。设备不存在时要检查可用性和错误。

#### `QCamera(const QCameraDevice &cameraDevice, QObject *parent = nullptr)`

创建一个绑定到指定 `QCameraDevice` 的对象。设备描述是值语义，camera 会据此连接物理设备。

#### `~QCamera()`

销毁 camera 并释放其平台资源。销毁前不需要手动释放 session 中的连接对象，但相关 QObject 的生命周期仍由各自所有者负责。

#### `bool isAvailable() const`

返回摄像头当前是否可以使用。它不是对启动成功的保证，权限、占用和后端初始化仍可能在激活时失败。

#### `bool isActive() const`

返回当前 camera 是否已激活。

#### `QMediaCaptureSession *captureSession() const`

返回当前连接的 capture session；未连接时返回 `nullptr`。连接应通过 `QMediaCaptureSession::setCamera()` 建立。

#### `QCameraDevice cameraDevice() const`

返回当前使用的摄像头设备描述。

#### `void setCameraDevice(const QCameraDevice &cameraDevice)`

切换物理摄像头。传入默认构造的 `QCameraDevice` 选择系统默认摄像头。切换后能力、属性范围和默认值可能变化。

#### `QCameraFormat cameraFormat() const`

返回当前采集格式。

#### `void setCameraFormat(const QCameraFormat &format)`

请求摄像头使用指定采集格式。建议只传入当前设备 `videoFormats()` 中的格式，并在改变后重新验证输出管线的实际帧格式。

#### `QCamera::Error error() const`

返回当前错误分类。

#### `QString errorString() const`

返回当前错误的人类可读描述。

#### `QCamera::Features supportedFeatures() const`

返回当前设备支持的可选控制能力组合。

#### `QCamera::FocusMode focusMode() const`

返回当前对焦模式。

#### `bool isFocusModeSupported(QCamera::FocusMode mode) const`

查询指定对焦模式是否支持。该函数是 `Q_INVOKABLE`，也可由元对象系统和 QML 调用。支持手动对焦时，手动焦距能力视为支持。

#### `QPointF focusPoint() const`

返回自动对焦当前使用的归一化帧坐标。

#### `QPointF customFocusPoint() const`

返回应用保存的自定义对焦点。

#### `float focusDistance() const`

返回当前手动焦距位置。

#### `float minimumZoomFactor() const`

返回最小缩放倍数。

#### `float maximumZoomFactor() const`

返回最大缩放倍数。

#### `float zoomFactor() const`

返回当前缩放倍数。

#### `QCamera::FlashMode flashMode() const`

返回当前闪光灯模式。

#### `bool isFlashModeSupported(QCamera::FlashMode mode) const`

查询指定闪光灯模式是否支持。该函数是 `Q_INVOKABLE`。

#### `bool isFlashReady() const`

返回闪光灯是否已充电并准备好。该函数是 `Q_INVOKABLE`。

#### `QCamera::TorchMode torchMode() const`

返回当前手电筒模式。

#### `bool isTorchModeSupported(QCamera::TorchMode mode) const`

查询指定手电筒模式是否支持。该函数是 `Q_INVOKABLE`。

#### `QCamera::ExposureMode exposureMode() const`

返回当前曝光模式。

#### `bool isExposureModeSupported(QCamera::ExposureMode mode) const`

查询指定曝光模式是否支持。该函数是 `Q_INVOKABLE`。

#### `float exposureCompensation() const`

返回当前自动曝光补偿值，单位 EV。

#### `int isoSensitivity() const`

返回当前实际 ISO。

#### `int manualIsoSensitivity() const`

返回手动 ISO 请求值；`-1` 表示自动。

#### `float exposureTime() const`

返回当前实际曝光时间，单位秒。

#### `float manualExposureTime() const`

返回手动曝光时间请求值；自动曝光时间时为 `-1`。

#### `int minimumIsoSensitivity() const`

返回设备支持的最小 ISO。

#### `int maximumIsoSensitivity() const`

返回设备支持的最大 ISO。

#### `float minimumExposureTime() const`

返回设备支持的最小曝光时间，单位秒。

#### `float maximumExposureTime() const`

返回设备支持的最大曝光时间，单位秒。

#### `QCamera::WhiteBalanceMode whiteBalanceMode() const`

返回当前白平衡模式。

#### `bool isWhiteBalanceModeSupported(QCamera::WhiteBalanceMode mode) const`

查询指定白平衡模式是否支持。该函数是 `Q_INVOKABLE`。

#### `int colorTemperature() const`

返回手动白平衡色温。当前模式不是 `WhiteBalanceManual` 时，返回值未定义。

### 11.4 槽和控制操作

#### `void setActive(bool active)`

激活或停用摄像头。`true` 等价于启动，`false` 等价于停止。调用是资源操作，不应省略异步错误处理。

#### `void start()`

启动摄像头，等价于 `setActive(true)`。启动失败时发出 `errorOccurred()`。

#### `void stop()`

停止摄像头，等价于 `setActive(false)`。

#### `void setFocusMode(QCamera::FocusMode mode)`

设置对焦模式。不支持的模式不会生效。

#### `void setCustomFocusPoint(const QPointF &point)`

设置归一化视频帧坐标中的自定义对焦点。设备不支持 `Feature::CustomFocusPoint` 时会忽略设置。

#### `void setFocusDistance(float d)`

设置手动焦距位置。合法范围是 `[0, 1]`，且需要手动对焦和 `Feature::FocusDistance`。

#### `void setZoomFactor(float factor)`

设置目标缩放倍数，使用每秒 1 倍因子的默认缩放速度。目标值会被钳制到设备范围。

#### `void zoomTo(float factor, float rate)`

以指定速率缩放到目标倍数。`rate` 使用每秒二进制幂的语义；后端不支持精确速率时会尽快完成。

#### `void setFlashMode(QCamera::FlashMode mode)`

设置拍照时的闪光灯模式。不支持的模式无效果，只对 `QImageCapture` 生效。

#### `void setTorchMode(QCamera::TorchMode mode)`

设置连续光源模式。不支持的模式无效果；开启时通常会覆盖闪光灯设置。

#### `void setExposureMode(QCamera::ExposureMode mode)`

设置曝光策略。不支持的模式无效果。

#### `void setExposureCompensation(float ev)`

设置自动曝光补偿，单位 EV。设备必须支持 `Feature::ExposureCompensation`。

#### `void setManualIsoSensitivity(int iso)`

请求手动 ISO。参数应位于 `minimumIsoSensitivity()` 和 `maximumIsoSensitivity()` 范围内，并且设备需要支持 `Feature::IsoSensitivity`。

#### `void setAutoIsoSensitivity()`

恢复自动 ISO。恢复后 `manualIsoSensitivity()` 应为 `-1`。

#### `void setManualExposureTime(float seconds)`

请求手动曝光时间，单位秒。设备需要支持 `Feature::ManualExposureTime`，参数应在设备曝光时间范围内。

#### `void setAutoExposureTime()`

恢复自动曝光时间。恢复后 `manualExposureTime()` 返回 `-1`。

#### `void setWhiteBalanceMode(QCamera::WhiteBalanceMode mode)`

设置白平衡模式。不支持的模式无效果。

#### `void setColorTemperature(int colorTemperature)`

设置手动白平衡色温，单位 Kelvin。大于 0 会切换到手动白平衡，0 会切换回自动白平衡；设备必须支持手动白平衡。

### 11.5 信号

#### `void activeChanged(bool active)`

摄像头激活状态改变时发出。

#### `void errorChanged()`

错误状态或错误说明改变时发出。

#### `void errorOccurred(QCamera::Error error, const QString &errorString)`

摄像头发生错误时发出，同时提供错误分类和人类可读说明。

#### `void cameraDeviceChanged()`

当前物理摄像头改变时发出。

#### `void cameraFormatChanged()`

当前采集格式改变时发出。

#### `void supportedFeaturesChanged()`

当前设备支持的可选能力改变时发出，常见于切换摄像头设备。

#### `void focusModeChanged()`

对焦模式改变时发出。

#### `void zoomFactorChanged(float factor)`

当前缩放倍数改变时发出。

#### `void minimumZoomFactorChanged(float factor)`

最小缩放倍数改变时发出。

#### `void maximumZoomFactorChanged(float factor)`

最大缩放倍数改变时发出。

#### `void focusDistanceChanged(float distance)`

手动焦距位置改变时发出。

#### `void focusPointChanged()`

自动对焦当前使用点改变时发出。

#### `void customFocusPointChanged()`

自定义对焦点改变时发出。

#### `void flashReady(bool ready)`

闪光灯准备状态改变时发出。

#### `void flashModeChanged()`

闪光灯模式改变时发出。

#### `void torchModeChanged()`

手电筒模式改变时发出。

#### `void exposureTimeChanged(float speed)`

当前实际曝光时间改变时发出。参数名为 `speed`，语义是新的曝光时间值，单位秒。

#### `void manualExposureTimeChanged(float speed)`

手动曝光时间请求值改变时发出。自动模式下相关值可回到 `-1`。

#### `void isoSensitivityChanged(int value)`

当前实际 ISO 改变时发出。

#### `void manualIsoSensitivityChanged(int value)`

手动 ISO 请求值改变时发出。

#### `void exposureCompensationChanged(float value)`

曝光补偿值改变时发出。

#### `void exposureModeChanged()`

曝光模式改变时发出。

#### `void whiteBalanceModeChanged() const`

白平衡模式改变时发出。Qt 6 中声明为 `const` 信号。

#### `void colorTemperatureChanged() const`

色温改变时发出。Qt 6 中声明为 `const` 信号。

#### `void brightnessChanged()`

底层亮度控制改变时发出。该信号在 Qt 6.11 的公开头文件中存在，但没有对应的公开读写属性或设置函数。

#### `void contrastChanged()`

底层对比度控制改变时发出。该信号在 Qt 6.11 的公开头文件中存在，但没有对应的公开读写属性或设置函数。

#### `void saturationChanged()`

底层饱和度控制改变时发出。该信号在 Qt 6.11 的公开头文件中存在，但没有对应的公开读写属性或设置函数。

#### `void hueChanged()`

底层色相控制改变时发出。该信号在 Qt 6.11 的公开头文件中存在，但没有对应的公开读写属性或设置函数。

## 12. 常见误区与排查顺序

1. 先请求 `QCameraPermission`，再启动 camera。
2. 先用 `QMediaDevices::videoInputs()` 选择设备，再读取该设备的 `videoFormats()`。
3. 先把 camera 设置到 `QMediaCaptureSession`，再配置预览、拍照或录像输出。
4. 每次切换 `cameraDevice` 后重新读取能力、格式、缩放范围和 ISO/曝光范围。
5. 自定义对焦点必须使用视频帧归一化坐标，不能直接使用窗口像素坐标。
6. 手动焦距、手动 ISO、手动曝光和色温都要先检查能力与合法范围。
7. `exposureTime()` 和 `isoSensitivity()` 是当前实际值，不是应用最后一次请求的值。
8. `manualExposureTime() == -1` 和 `manualIsoSensitivity() == -1` 表示自动控制。
9. 闪光灯用于 `QImageCapture` 拍照；视频低光照应考虑 `torchMode`。
10. 不要只根据 `start()` 返回判断启动成功，要处理 `activeChanged` 和 `errorOccurred`。

## API 速查表

| 类别 | API | 语义 | 边界与注意 |
| --- | --- | --- | --- |
| 类型 | `enum QCamera::Error` | 表示无错误或摄像头错误。 | 详细原因看 `errorString()` 和 `errorOccurred()`。 |
| 类型 | `enum QCamera::FocusMode` | 选择自动、超焦距、无穷远或手动对焦。 | 先用 `isFocusModeSupported()` 查询。 |
| 类型 | `enum QCamera::FlashMode` | 选择关闭、强制开启或自动闪光。 | 只对 `QImageCapture` 拍照有作用。 |
| 类型 | `enum QCamera::TorchMode` | 选择连续光源的关闭、开启或自动模式。 | 通常会覆盖闪光灯模式。 |
| 类型 | `enum QCamera::ExposureMode` | 选择自动、手动和场景曝光策略。 | 设备只支持其中一部分。 |
| 类型 | `enum QCamera::WhiteBalanceMode` | 选择自动、手动和预设白平衡。 | 手动模式配合 Kelvin 色温。 |
| 类型 | `enum class QCamera::Feature` | 描述单项可选控制能力。 | 与 `Features` 按位组合。 |
| 类型 | `QCamera::Features` | `QFlags<Feature>` 能力集合。 | 设备切换后要重新读取。 |
| 属性 | `active : bool` | 摄像头是否已激活。 | 激活是资源操作，监听状态和错误。 |
| 属性 | `cameraDevice : QCameraDevice` | 当前物理摄像头描述。 | 切换会改变能力和属性范围。 |
| 属性 | `cameraFormat : QCameraFormat` | 当前采集格式。 | 优先从 `videoFormats()` 选择。 |
| 属性 | `error : Error` | 当前错误分类。 | 只读。 |
| 属性 | `errorString : QString` | 当前错误的人类可读说明。 | 只读，不要依赖字符串做逻辑判断。 |
| 属性 | `focusMode : FocusMode` | 当前对焦模式。 | 不支持的模式赋值没有效果。 |
| 属性 | `focusPoint : QPointF` | 自动对焦当前点。 | 只读；是归一化帧坐标。 |
| 属性 | `customFocusPoint : QPointF` | 应用指定的对焦点。 | 需要 `Feature::CustomFocusPoint`。 |
| 属性 | `focusDistance : float` | 手动焦距位置。 | 有效范围 `[0, 1]`，需要手动对焦。 |
| 属性 | `minimumZoomFactor : float` | 最小缩放倍数。 | 不支持缩放时通常为 `1.0`。 |
| 属性 | `maximumZoomFactor : float` | 最大缩放倍数。 | 不支持缩放时通常为 `1.0`。 |
| 属性 | `zoomFactor : float` | 当前缩放倍数。 | 设置值会被范围钳制。 |
| 属性 | `exposureTime : float` | 当前实际曝光时间，单位秒。 | 只读；自动模式会变化。 |
| 属性 | `manualExposureTime : float` | 手动曝光时间请求值。 | 自动时为 `-1`。 |
| 属性 | `isoSensitivity : int` | 当前实际 ISO。 | 只读；自动 ISO 会变化。 |
| 属性 | `manualIsoSensitivity : int` | 手动 ISO 请求值。 | `-1` 表示自动。 |
| 属性 | `exposureCompensation : float` | 自动曝光补偿，单位 EV。 | 需要 `Feature::ExposureCompensation`。 |
| 属性 | `exposureMode : ExposureMode` | 当前曝光策略。 | 先查询模式支持。 |
| 属性 | `flashReady : bool` | 闪光灯是否已充电。 | 只读。 |
| 属性 | `flashMode : FlashMode` | 拍照闪光灯模式。 | 只对 `QImageCapture` 生效。 |
| 属性 | `torchMode : TorchMode` | 连续光源模式。 | 低光照视频使用。 |
| 属性 | `whiteBalanceMode : WhiteBalanceMode` | 当前白平衡模式。 | 手动模式配合色温。 |
| 属性 | `colorTemperature : int` | 手动白平衡色温，单位 Kelvin。 | 非手动模式读取未定义；0 恢复自动。 |
| 属性 | `supportedFeatures : Features` | 当前设备的可选能力集合。 | 只读；换设备后重新读取。 |
| 构造 | `QCamera(QObject *parent = nullptr)` | 创建默认设备 camera。 | 仍需权限和可用性检查。 |
| 构造 | `QCamera(QCameraDevice::Position position, QObject *parent = nullptr)` | 按前后置位置选择 camera。 | 位置不存在时可能不可用。 |
| 构造 | `QCamera(const QCameraDevice &cameraDevice, QObject *parent = nullptr)` | 使用指定设备创建 camera。 | 描述值可复制，物理资源不复制。 |
| 析构 | `~QCamera()` | 释放 camera 平台资源。 | QObject parent 管理生命周期。 |
| 查询 | `isAvailable()` | 查询摄像头当前是否可用。 | 不保证激活一定成功。 |
| 查询 | `isActive()` | 查询 camera 是否已激活。 | 通过 `activeChanged` 观察变化。 |
| 查询 | `captureSession()` | 返回连接的 session。 | 未连接返回 `nullptr`。 |
| 查询 | `cameraDevice()` | 返回当前设备描述。 | 值类型返回。 |
| 设置 | `setCameraDevice(...)` | 切换物理摄像头。 | 能力、范围和控制值可能重置。 |
| 查询 | `cameraFormat()` | 返回当前采集格式。 | 读取实际选择值。 |
| 设置 | `setCameraFormat(...)` | 请求分辨率、帧率和像素格式。 | 优先使用设备支持列表。 |
| 查询 | `error()` | 返回错误分类。 | 与 `errorString()` 一起处理。 |
| 查询 | `errorString()` | 返回错误说明。 | 适合日志和用户提示。 |
| 查询 | `supportedFeatures()` | 返回可选控制能力。 | 不同设备结果不同。 |
| 查询 | `focusMode()` | 返回对焦模式。 | 读取实际状态。 |
| 查询 | `isFocusModeSupported(...)` | 查询对焦模式能力。 | `Q_INVOKABLE`，支持 QML。 |
| 查询 | `focusPoint()` | 返回自动对焦点。 | 归一化帧坐标。 |
| 查询 | `customFocusPoint()` | 返回自定义对焦点。 | 不等于控件坐标。 |
| 查询 | `focusDistance()` | 返回手动焦距位置。 | 自动模式下不会被自动系统更新。 |
| 查询 | `minimumZoomFactor()` | 返回最小缩放倍数。 | 无缩放通常为 `1.0`。 |
| 查询 | `maximumZoomFactor()` | 返回最大缩放倍数。 | 无缩放通常为 `1.0`。 |
| 查询 | `zoomFactor()` | 返回当前缩放倍数。 | 结合范围读取。 |
| 查询 | `flashMode()` | 返回闪光灯模式。 | 只影响拍照。 |
| 查询 | `isFlashModeSupported(...)` | 查询闪光灯模式能力。 | `Q_INVOKABLE`。 |
| 查询 | `isFlashReady()` | 查询闪光灯是否准备好。 | `Q_INVOKABLE`；不代表一定有闪光灯。 |
| 查询 | `torchMode()` | 返回手电筒模式。 | 连续光源。 |
| 查询 | `isTorchModeSupported(...)` | 查询手电筒模式能力。 | `Q_INVOKABLE`。 |
| 查询 | `exposureMode()` | 返回曝光模式。 | 读取实际状态。 |
| 查询 | `isExposureModeSupported(...)` | 查询曝光模式能力。 | `Q_INVOKABLE`。 |
| 查询 | `exposureCompensation()` | 返回 EV 补偿。 | 是自动曝光偏置。 |
| 查询 | `isoSensitivity()` | 返回当前实际 ISO。 | 自动模式会动态变化。 |
| 查询 | `manualIsoSensitivity()` | 返回手动 ISO 请求值。 | `-1` 表示自动。 |
| 查询 | `exposureTime()` | 返回当前实际曝光时间。 | 单位秒。 |
| 查询 | `manualExposureTime()` | 返回手动曝光请求值。 | 自动时为 `-1`。 |
| 查询 | `minimumIsoSensitivity()` | 返回最小 ISO。 | 设备相关。 |
| 查询 | `maximumIsoSensitivity()` | 返回最大 ISO。 | 设备相关。 |
| 查询 | `minimumExposureTime()` | 返回最小曝光时间。 | 单位秒，设备相关。 |
| 查询 | `maximumExposureTime()` | 返回最大曝光时间。 | 单位秒，设备相关。 |
| 查询 | `whiteBalanceMode()` | 返回白平衡模式。 | 设备只支持部分模式。 |
| 查询 | `isWhiteBalanceModeSupported(...)` | 查询白平衡模式能力。 | `Q_INVOKABLE`。 |
| 查询 | `colorTemperature()` | 返回手动色温。 | 非手动模式时未定义。 |
| 槽 | `setActive(bool)` | 激活或停用摄像头。 | 权限、占用和后端错误需异步处理。 |
| 槽 | `start()` | 启动 camera。 | 等价于 `setActive(true)`。 |
| 槽 | `stop()` | 停止 camera。 | 等价于 `setActive(false)`。 |
| 设置 | `setFocusMode(...)` | 设置对焦模式。 | 不支持时无效果。 |
| 设置 | `setCustomFocusPoint(...)` | 设置归一化帧对焦点。 | 需要自定义对焦能力。 |
| 设置 | `setFocusDistance(float)` | 设置手动焦距。 | 范围 `[0, 1]`。 |
| 设置 | `setZoomFactor(float)` | 设置缩放倍数。 | 范围自动钳制。 |
| 槽 | `zoomTo(float, float)` | 以指定速率缩放。 | 速率支持取决于后端。 |
| 槽 | `setFlashMode(...)` | 设置拍照闪光灯模式。 | 只对图像捕获生效。 |
| 槽 | `setTorchMode(...)` | 设置连续光源模式。 | 可能覆盖 flash 设置。 |
| 槽 | `setExposureMode(...)` | 设置曝光策略。 | 不支持时无效果。 |
| 槽 | `setExposureCompensation(float)` | 设置自动曝光 EV 补偿。 | 需要对应 Feature。 |
| 槽 | `setManualIsoSensitivity(int)` | 请求手动 ISO。 | 需要支持且处于合法范围。 |
| 槽 | `setAutoIsoSensitivity()` | 恢复自动 ISO。 | 手动 ISO 回到 `-1`。 |
| 槽 | `setManualExposureTime(float)` | 请求手动曝光时间。 | 单位秒，需要支持且在范围内。 |
| 槽 | `setAutoExposureTime()` | 恢复自动曝光时间。 | 手动曝光回到 `-1`。 |
| 槽 | `setWhiteBalanceMode(...)` | 设置白平衡模式。 | 不支持时无效果。 |
| 槽 | `setColorTemperature(int)` | 设置 Kelvin 色温。 | 大于 0 手动，0 自动。 |
| 信号 | `activeChanged(bool)` | 通知激活状态改变。 | 不等于视频帧已到达。 |
| 信号 | `errorChanged()` | 通知错误状态改变。 | 读取 error 和 errorString。 |
| 信号 | `errorOccurred(Error, const QString &)` | 通知摄像头错误。 | 启动失败等异步错误入口。 |
| 信号 | `cameraDeviceChanged()` | 通知设备改变。 | 重新读取能力。 |
| 信号 | `cameraFormatChanged()` | 通知采集格式改变。 | 输出帧格式可能变化。 |
| 信号 | `supportedFeaturesChanged()` | 通知可选能力改变。 | 常见于换设备。 |
| 信号 | `focusModeChanged()` | 通知对焦模式改变。 | 读取 `focusMode()`。 |
| 信号 | `zoomFactorChanged(float)` | 通知缩放改变。 | 读取实际值。 |
| 信号 | `minimumZoomFactorChanged(float)` | 通知最小缩放范围改变。 | 设备相关。 |
| 信号 | `maximumZoomFactorChanged(float)` | 通知最大缩放范围改变。 | 设备相关。 |
| 信号 | `focusDistanceChanged(float)` | 通知手动焦距改变。 | 只在相关能力下有意义。 |
| 信号 | `focusPointChanged()` | 通知自动对焦点改变。 | 是帧坐标。 |
| 信号 | `customFocusPointChanged()` | 通知自定义对焦点改变。 | 是应用设置的值。 |
| 信号 | `flashReady(bool)` | 通知闪光灯准备状态改变。 | 拍照前可检查。 |
| 信号 | `flashModeChanged()` | 通知闪光灯模式改变。 | 只关联拍照。 |
| 信号 | `torchModeChanged()` | 通知手电筒模式改变。 | 连续光源状态。 |
| 信号 | `exposureTimeChanged(float)` | 通知当前曝光时间改变。 | 参数单位秒。 |
| 信号 | `manualExposureTimeChanged(float)` | 通知手动曝光请求值改变。 | 自动模式可为 `-1`。 |
| 信号 | `isoSensitivityChanged(int)` | 通知当前实际 ISO 改变。 | 自动模式常变化。 |
| 信号 | `manualIsoSensitivityChanged(int)` | 通知手动 ISO 请求值改变。 | `-1` 表示自动。 |
| 信号 | `exposureCompensationChanged(float)` | 通知 EV 补偿改变。 | 只影响自动曝光。 |
| 信号 | `exposureModeChanged()` | 通知曝光模式改变。 | 读取实际模式。 |
| 信号 | `whiteBalanceModeChanged() const` | 通知白平衡模式改变。 | Qt 6 声明为 const 信号。 |
| 信号 | `colorTemperatureChanged() const` | 通知色温改变。 | 手动白平衡时读取才有定义。 |
| 信号 | `brightnessChanged()` | 通知底层亮度控制改变。 | Qt 6.11 公开信号，无对应公开 setter。 |
| 信号 | `contrastChanged()` | 通知底层对比度控制改变。 | Qt 6.11 公开信号，无对应公开 setter。 |
| 信号 | `saturationChanged()` | 通知底层饱和度控制改变。 | Qt 6.11 公开信号，无对应公开 setter。 |
| 信号 | `hueChanged()` | 通知底层色相控制改变。 | Qt 6.11 公开信号，无对应公开 setter。 |

### 一句话总结

`QCamera` 负责控制摄像头，不负责承接或保存视频。理解它时要把“权限、设备、格式、session 连接、激活状态和硬件能力”放在同一条采集链路里看。
