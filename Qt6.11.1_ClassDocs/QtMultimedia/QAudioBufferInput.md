# QAudioBufferInput
> Qt 6.11.1 · Qt Multimedia · 来自 `QAudioBufferInput`

## 作用定位

`QAudioBufferInput` 用来把应用自己生成或处理后的 `QAudioBuffer` 喂入 Qt 多媒体采集/录制管线。它属于高层媒体管线节点，适合“我已经有音频 buffer，希望交给 recorder 或 capture session 继续编码/封装”的场景。

## 类说明

- 头文件：`#include <QAudioBufferInput>`
- CMake：链接 `Qt6::Multimedia`
- 继承：`QObject`
- 常用协作：`QMediaCaptureSession`、`QMediaRecorder`、`QAudioBuffer`

## API 速查

| API | 说明 |
| --- | --- |
| 构造函数 | 创建 buffer 输入节点，可指定音频格式。 |
| `format()` | 返回期望/当前 buffer 格式。 |
| `sendAudioBuffer(buffer)` | 向媒体管线提交一块音频 buffer。 |
| `readyToSendAudioBuffer()` | 管线准备好接收下一块 buffer 时通知。 |

## 使用场景

| 场景 | 说明 |
| --- | --- |
| 自定义音频源录制 | 合成、网络接收或算法输出的 PCM 进入 recorder。 |
| 音频处理后再编码 | 先降噪/混音，再交给 Qt 录制。 |
| 测试媒体录制 | 用固定 buffer 驱动录制流程。 |

## 常见坑与经验

- 提交的 buffer 格式要与输入节点/录制管线预期一致。
- 关注 `readyToSendAudioBuffer()` 做背压，不要无限推送。
- buffer 时间戳和连续性会影响最终媒体同步效果。
- 它不是麦克风采集类；麦克风进管线用 `QAudioInput`。

## 知识点覆盖

- 自定义音频源进入媒体管线
- buffer 背压
- 录制/编码前音频处理
- 与 `QAudioSource` 的层级区别
