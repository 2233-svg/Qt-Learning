# QAudioSink
> Qt 6.11.1 · Qt Multimedia · 来自 `QAudioSink`

## 作用定位

`QAudioSink` 是低层原始音频播放类。你提供 PCM 数据，它把数据送到输出设备播放。它适合合成器、游戏音频、实时处理输出、网络语音播放等需要自己掌控音频数据的场景。

播放媒体文件时更常用 `QMediaPlayer` + `QAudioOutput`。

## 类说明

- 头文件：`#include <QAudioSink>`
- CMake：链接 `Qt6::Multimedia`
- 继承：`QObject`

## API 速查

| API | 说明 |
| --- | --- |
| 构造函数 | 用输出设备和 `QAudioFormat` 创建 sink。 |
| `start()` | 开始播放，返回可写 `QIODevice`，或从指定 device 拉取数据。 |
| `stop()` / `reset()` / `suspend()` / `resume()` | 控制播放状态。 |
| `state()` / `stateChanged()` | 查询和监听状态。 |
| `error()` | 读取设备或格式错误。 |
| `bytesFree()` | 当前还能写入多少字节。 |
| `bufferSize()` / `setBufferSize()` | 配置缓冲区大小。 |
| `processedUSecs()` / `elapsedUSecs()` | 已播放音频时长和运行时间。 |
| `setVolume()` / `volume()` | 设置播放音量。 |
| `format()` | 当前播放格式。 |

## 使用场景

- 生成 PCM 后实时播放。
- 网络流解码后自定义播放。
- 需要低层控制缓冲、延迟和格式的音频输出。
- 写简单音频合成器或提示音混音器。

## 常见坑与经验

- 写入数据的格式必须和 `QAudioFormat` 完全一致；Qt 不会替你自动重采样所有情况。
- `bytesFree()` 是节流依据，写太快只会堆积或失败。
- buffer 越小延迟越低但越容易断音；要按平台测试。
- `IdleState` 可能表示数据耗尽，不一定是错误；结合 `error()` 判断。

## 知识点覆盖

- 原始 PCM 播放
- 音频缓冲和低延迟
- QIODevice 写入/拉取模式
- `QAudioSink` 与 `QAudioOutput` 区别
