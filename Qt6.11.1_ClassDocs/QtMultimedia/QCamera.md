# QCamera
> Qt 6.11.1 · Qt Multimedia · 来自 `QCamera`

## 作用定位

`QCamera` 控制摄像头设备：启动/停止、选择格式、曝光、对焦、闪光、白平衡、变焦等。它通常接入 `QMediaCaptureSession`，再由 session 连接预览、拍照或录像输出。

## 类说明

- 头文件：`#include <QCamera>`
- CMake：链接 `Qt6::Multimedia`
- 继承：`QObject`

## API 速查

| API | 说明 |
| --- | --- |
| `start()` / `stop()` | 打开或关闭摄像头。 |
| `isActive()` / `activeChanged()` | 摄像头是否正在工作。 |
| `setCameraDevice()` / `cameraDevice()` | 指定物理摄像头。 |
| `setCameraFormat()` / `cameraFormat()` | 设置分辨率、帧率、像素格式组合。 |
| `error()` / `errorString()` | 摄像头错误。 |
| `setFocusMode()` / `focusMode()` | 自动/连续/手动对焦等。 |
| `setZoomFactor()` / `zoomFactor()` | 数字/光学变焦因子。 |
| `setExposureMode()` / `setExposureCompensation()` | 曝光模式和补偿。 |
| `setWhiteBalanceMode()` | 白平衡模式。 |
| `isFlashModeSupported()` / `setFlashMode()` | 闪光灯能力和模式。 |
| `isTorchModeSupported()` / `setTorchMode()` | 常亮补光灯能力和模式。 |

## 使用场景
- 摄像头预览、拍照、扫码、录像。
- 移动端控制对焦、曝光、闪光灯。
- 桌面应用选择 USB 摄像头并设置格式。

## 常见坑与经验
- 摄像头权限、设备占用、后端支持是启动失败三大来源。
- 格式要从 `QCameraDevice::videoFormats()` 里选，不要凭空设置。
- 拍照用 `QImageCapture`，录像用 `QMediaRecorder`，预览用 video output，它们都通过 capture session 接起来。
- 手动对焦/曝光/闪光不是每个设备都支持，先查能力。

## 知识点覆盖

- 摄像头设备控制
- 格式、对焦、曝光、白平衡
- 预览/拍照/录像管线
- 权限和硬件能力差异
