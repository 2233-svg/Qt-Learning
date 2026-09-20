# QAudioSource
> Qt 6.11.1 · Qt Multimedia · 来自 `QAudioSource`

## 作用定位

`QAudioSource` 是低层原始音频采集类。它直接从输入设备读取 PCM 数据，返回 `QIODevice` 或写入你提供的设备。它面向实时录音、音频分析、语音识别前端等场景。

如果你只是想让 `QMediaRecorder` 录麦克风，使用高层 `QAudioInput`。

## 类说明

- 头文件：`#include <QAudioSource>`
- CMake：链接 `Qt6::Multimedia`
- 继承：`QObject`

## API 速查

| API | 说明 |
| --- | --- |
| 构造函数 | 用设备和 `QAudioFormat` 创建采集源。 |
| `start()` | 开始采集并返回可读 `QIODevice`，或把数据写入指定 device。 |
| `stop()` / `reset()` / `suspend()` / `resume()` | 控制采集状态。 |
| `state()` / `stateChanged()` | 查询和监听状态。 |
| `error()` | 读取设备/格式/IO 错误。 |
| `bytesAvailable()` | 当前可读字节数。 |
| `bufferSize()` / `setBufferSize()` | 配置内部缓冲。 |
| `processedUSecs()` / `elapsedUSecs()` | 已处理音频时长和运行时间。 |
| `format()` | 当前采集格式。 |

## 使用场景

- 实时录音到内存或文件。
- 麦克风音量检测、波形、频谱。
- 语音识别、降噪、回声消除前处理。
- 自定义低延迟音频采集。

## 常见坑与经验

- 格式必须先和设备协商，优先用 `QAudioDevice::isFormatSupported()`。
- 采集回调/readyRead 里不要做重计算，否则会丢数据。
- buffer 过小延迟低但更容易 underrun/overrun；过大更稳但延迟高。
- 权限和默认输入设备变化是实际产品里最常见故障源。

## 知识点覆盖

- 原始 PCM 采集
- QIODevice 拉取/推送模式
- 音频状态机和错误处理
- 缓冲、延迟和实时处理
