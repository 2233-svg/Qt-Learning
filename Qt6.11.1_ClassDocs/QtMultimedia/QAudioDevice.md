# QAudioDevice
> Qt 6.11.1 · Qt Multimedia · 来自 `QAudioDevice`

## 作用定位

`QAudioDevice` 描述一个音频输入或输出设备：设备 ID、描述、默认格式、支持的采样率/通道数/采样格式等。它是设备信息值对象，通常由 `QMediaDevices` 枚举得到，再交给 `QAudioInput`、`QAudioOutput`、`QAudioSource` 或 `QAudioSink`。

## 类说明

- 头文件：`#include <QAudioDevice>`
- CMake：链接 `Qt6::Multimedia`
- 继承：无公开 QObject 继承，值类型

## API 速查

| API | 说明 |
| --- | --- |
| `id()` | 后端设备标识，适合保存短期选择，不保证永久稳定。 |
| `description()` | 面向用户显示的设备名称。 |
| `isDefault()` | 是否是当前默认输入/输出设备。 |
| `mode()` | 设备方向：输入或输出。 |
| `preferredFormat()` | 后端建议的默认音频格式。 |
| `isFormatSupported(format)` | 检查采样格式是否可用。 |
| `minimumSampleRate()` / `maximumSampleRate()` | 支持采样率范围。 |
| `minimumChannelCount()` / `maximumChannelCount()` | 支持通道数范围。 |
| `supportedSampleFormats()` | 支持的样本格式列表。 |

## 使用场景

- 枚举麦克风和扬声器并显示给用户。
- 为 `QAudioSink/Source` 选择格式前做兼容性检查。
- 设备热插拔后重新匹配用户偏好。

## 常见坑与经验

- 设备 ID 不适合长期配置文件里无条件信任；系统更新和后端变化可能改变它。
- `preferredFormat()` 是建议，不一定符合你的算法需求；需要重采样时要自己处理。
- 输入设备和输出设备都用同一个类表示，使用前看 `mode()`。
- `isFormatSupported()` 只说明后端接受，不代表延迟、质量或性能符合需求。

## 知识点覆盖

- 音频设备枚举
- 采样率、通道数、样本格式
- 默认设备和热插拔
- 格式协商
