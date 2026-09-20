# QMediaDevices
> Qt 6.11.1 · Qt Multimedia · 来自 `QMediaDevices`

## 作用定位

`QMediaDevices` 是多媒体设备中心，负责枚举音频输入、音频输出、摄像头，并在设备热插拔或默认设备变化时发信号。它通常作为设备选择 UI 和自动恢复逻辑的入口。

## 类说明

- 头文件：`#include <QMediaDevices>`
- CMake：链接 `Qt6::Multimedia`
- 继承：`QObject`

## API 速查

| API | 说明 |
| --- | --- |
| `audioInputs()` / `defaultAudioInput()` | 枚举麦克风和默认输入。 |
| `audioOutputs()` / `defaultAudioOutput()` | 枚举扬声器/耳机和默认输出。 |
| `videoInputs()` / `defaultVideoInput()` | 枚举摄像头和默认摄像头。 |
| `audioInputsChanged()` | 输入设备列表变化。 |
| `audioOutputsChanged()` | 输出设备列表变化。 |
| `videoInputsChanged()` | 摄像头列表变化。 |

## 使用场景

- 设置页列出麦克风、扬声器和摄像头。
- 默认设备变化时自动切换。
- 热插拔 USB 摄像头、蓝牙耳机后刷新 UI。

## 常见坑与经验

- 设备权限会影响列表或使用结果，尤其是摄像头和麦克风。
- 默认设备变化不代表你已有对象自动切换，可能需要重新设置 device。
- 保存用户选择时，设备 ID 可能随系统变化失效，要有 fallback 到默认设备的逻辑。

## 知识点覆盖

- 多媒体设备枚举
- 默认设备和热插拔
- 音频设备与摄像头设备类型
- 设备选择 UI
