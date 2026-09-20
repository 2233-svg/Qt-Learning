# QAudioInput
> Qt 6.11.1 · Qt Multimedia · 来自 `QAudioInput`

## 作用定位

`QAudioInput` 是录制/采集管线里的“音频输入端”。它通常连接到 `QMediaCaptureSession`，作为相机录制、屏幕录制或音频录制的麦克风来源。它不负责让你直接读取原始 PCM；原始采集请看 `QAudioSource`。

## 类说明

- 头文件：`#include <QAudioInput>`
- CMake：链接 `Qt6::Multimedia`
- 继承：`QObject`
- 常用协作：`QMediaCaptureSession`、`QMediaRecorder`、`QMediaDevices`

## API 速查

| API | 说明 |
| --- | --- |
| `QAudioInput(parent)` | 创建采集管线用音频输入。 |
| `setDevice()` / `device()` | 选择麦克风或系统输入设备。 |
| `setVolume()` / `volume()` | 设置输入增益/音量。 |
| `setMuted()` / `isMuted()` | 控制输入静音。 |
| `deviceChanged()` | 输入设备变化通知。 |
| `volumeChanged()` | 输入音量变化通知。 |
| `mutedChanged()` | 静音变化通知。 |

## 使用场景

- `QMediaRecorder` 录制麦克风音频。
- 录屏或摄像时把麦克风作为音轨。
- 给用户提供输入设备选择和麦克风静音。

## 常见坑与经验

- `QAudioInput` 是高层采集管线节点，不直接给你音频 buffer。
- 麦克风权限在移动端、桌面沙盒环境里可能导致设备可见但无法采集。
- 输入音量含义受平台和后端影响，不能假设每个平台都是硬件增益。
- 切换设备时，正在录制的会话可能需要重启或重新配置。

## 知识点覆盖

- 多媒体采集管线
- 麦克风设备选择
- 输入静音与音量
- `QAudioInput` 与 `QAudioSource` 区别
