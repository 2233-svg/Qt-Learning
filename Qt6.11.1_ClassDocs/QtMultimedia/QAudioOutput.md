# QAudioOutput
> Qt 6.11.1 · Qt Multimedia · 来自 `QAudioOutput`

## 作用定位

`QAudioOutput` 是媒体播放管线里的“音频输出端”。它通常交给 `QMediaPlayer::setAudioOutput()` 使用，用来选择播放设备、设置音量和静音。它不负责你手动写 PCM 数据；原始音频播放请看 `QAudioSink`。

## 类说明

- 头文件：`#include <QAudioOutput>`
- CMake：链接 `Qt6::Multimedia`
- 继承：`QObject`
- 常用协作：`QMediaPlayer`、`QMediaDevices`、`QAudioDevice`

## API 速查

| API | 说明 |
| --- | --- |
| `QAudioOutput(parent)` | 创建媒体播放用音频输出对象。 |
| `setDevice()` / `device()` | 指定或读取输出设备；默认设备变化时可重新设置。 |
| `setVolume()` / `volume()` | 设置线性音量，通常范围 0.0 到 1.0。 |
| `setMuted()` / `isMuted()` | 静音开关，不改变保存的音量值。 |
| `deviceChanged()` | 输出设备变化通知。 |
| `volumeChanged()` | 音量变化通知。 |
| `mutedChanged()` | 静音状态变化通知。 |

## 使用场景

- 播放文件、流媒体或 URL 时控制声音输出。
- 给用户提供输出设备选择、音量条、静音按钮。
- `QMediaPlayer` 多实例时，每个播放器使用不同输出配置。

## 常见坑与经验

- `QAudioOutput` 不提供 `start(QIODevice*)`，不能直接写 PCM；那是 `QAudioSink` 的职责。
- 静音和音量是两个状态，解除静音后会回到原音量。
- 设备列表来自 `QMediaDevices::audioOutputs()`，热插拔后要处理设备失效。
- 音量是线性值，UI slider 如需贴近人耳感受，可以自己做分贝/曲线映射。

## 知识点覆盖

- 媒体播放管线音频输出
- 输出设备热插拔
- 音量、静音与播放器协作
- `QAudioOutput` 与 `QAudioSink` 区别
