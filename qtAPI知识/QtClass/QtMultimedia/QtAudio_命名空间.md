# QtAudio：音频状态、错误与音量标尺

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QtAudio>`  
> 所属模块：`Qt6::Multimedia`  
> 类型性质：命名空间，包含公开枚举和自由函数

## 它解决什么问题

音频类需要共享一组稳定的概念：设备是否正在处理数据、启动或 I/O 是否失败、音量值使用哪一种标尺。`QtAudio` 集中提供这些枚举和 `convertVolume()`，供 `QAudioSink`、`QAudioSource`、`QAudioOutput`、`QAudioInput`、`QMediaPlayer` 等类使用。

它不是对象，也没有构造函数、父对象或信号。状态仍由具体音频对象产生，`QtAudio` 只定义状态值和解释方式。

## `QAudio` 与 `QtAudio`

Qt 6.7 起文档和新 API 使用 `QtAudio` 命名空间。头文件中仍保留 `QAudio` 兼容名称，并提供类型别名和枚举常量。

新代码优先写：

```cpp
QtAudio::State state = sink->state();
if (state == QtAudio::ActiveState) {
    // 正在处理音频
}
```

旧代码中的 `QAudio::State`、`QAudio::ActiveState` 在 Qt 6.11 仍可能可用，但应避免在新代码中继续扩大旧名称的使用范围。

## 实际使用场景

- 根据 `QAudioSink::stateChanged()` 更新播放缓冲状态。
- 区分音频设备打开失败、设备断开和不可恢复错误。
- 把 UI 滑块的对数音量转换成 Qt 音频类使用的线性音量。
- 在录音或播放管线中识别 `IdleState`，定位数据供应或读取不及时问题。

## `Error`：错误状态

| 枚举值 | 含义 | 处理重点 |
| --- | --- | --- |
| `NoError` | 没有错误 | 正常状态，不代表设备一定已经启动 |
| `OpenError` | 打开音频设备失败 | 检查设备、格式、权限和占用情况 |
| `IOError` | 读写设备过程中发生 I/O 错误 | 可能是外部声卡或设备断开 |
| `UnderrunError` | 旧式欠载错误 | Qt 6.11 已弃用，Qt 不再发出，观察 `IdleState` |
| `FatalError` | 不可恢复错误 | 当前设备不可用，通常需要停止并重新建立管线 |

`error()` 的返回值通常应与 `state()` 一起判断。`StoppedState` 可能只是主动停止，也可能是错误导致停止，不能只凭状态区分。

## `State`：音频处理状态

### `ActiveState`

设备已启动并正在处理音频数据。对 sink 来说通常意味着正在消费输入；对 source 来说通常意味着设备数据正在进入应用可读缓冲。

### `SuspendedState`

音频流被暂停，可能来自显式 `suspend()`，也可能是平台把设备控制权交给了另一条流。通常由用户操作触发 `resume()`，不要把它当成普通短暂欠载。

### `StoppedState`

设备已关闭或流已停止，不再处理音频。发生打开错误、I/O 错误或显式 `stop()` 后都可能处于此状态。

### `IdleState`

音频系统因缓冲条件暂时没有可处理的数据：

- `QAudioSink`：应用提供给 `QIODevice` 的数据不够；
- `QAudioSource`：应用没有及时从输入 `QIODevice` 读取，环形缓冲区已满，继续到达的输入可能被丢弃。

`IdleState` 不是“没有错误”的保证，也不是可以无限等待的正常播放状态。应检查生产者或消费者是否及时运行。

## `VolumeScale`：音量数值的标尺

Qt Multimedia 的音量属性通常使用线性标尺：`0.0` 表示静音，`1.0` 表示满音量。用户感知的响度却接近对数关系，所以 UI 滑块通常更适合先使用对数标尺，再转换成线性值。

| 标尺 | 常用范围 | 特点 |
| --- | --- | --- |
| `LinearVolumeScale` | `0.0` 到 `1.0` | Qt 音频对象常用的内部标尺 |
| `CubicVolumeScale` | `0.0` 到 `1.0` | 用立方关系近似对数控制，计算便宜 |
| `LogarithmicVolumeScale` | `0.0` 到 `1.0` | 更贴近普通 UI 的响度感受 |
| `DecibelVolumeScale` | `-200` 到 `0` | 分贝振幅标尺，`-200` 近似静音，`0` 为满音量 |

数值超出对应标尺的推荐范围时，不应依赖跨标尺转换的隐式钳制行为。应用应在传入前按 UI 和业务规则限制范围。

## `convertVolume()`

```cpp
const float linear = QtAudio::convertVolume(
    sliderValue / 100.0f,
    QtAudio::LogarithmicVolumeScale,
    QtAudio::LinearVolumeScale);

audioOutput->setVolume(linear);
```

这个函数只转换数值标尺，不改变任何设备或播放器属性。`from` 和 `to` 相同时，结果等价于原标尺中的输入值。

应明确 UI 值属于哪一种标尺。把 0 到 100 的整数直接当作线性浮点值，会把满音量变成远超预期的值；通常先除以 100，再从对数或分贝标尺转换到线性标尺。

## Qt 6.11 的弃用边界

`QtAudio::UnderrunError` 在 Qt 6.11 被标记为弃用，并且 Qt 不再发出这个错误值。检测供应不足时，应观察 `QtAudio::IdleState`，再结合 `bytesFree()`、`processedUSecs()`、输入读取速度或输出写入速度定位原因。

## 常见误区

- 把 `QtAudio` 当作可实例化的控制对象。
- 只判断 `StoppedState`，却不读取具体 `error()`。
- 把 `IdleState` 当作永久暂停或一定是设备故障。
- 继续等待 `UnderrunError` 信号或把它当作 Qt 6.11 的可靠错误通知。
- 把线性音量直接当成人耳感知的线性响度。
- 把分贝值直接传给 `QAudioOutput::setVolume()`，却没有转回线性范围。
- 认为 `convertVolume()` 会自动修改播放器、钳制所有非法输入或解决设备音量策略。

## API 速查表

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 错误 | `QtAudio::Error` | 描述音频设备或 I/O 错误。 | 与具体对象的 `error()` 一起使用。 |
| 错误 | `NoError` | 表示没有错误。 | 不等价于设备已经启动。 |
| 错误 | `OpenError` | 表示打开设备失败。 | 检查设备、格式和权限。 |
| 错误 | `IOError` | 表示读写设备失败。 | 可能是设备断开。 |
| 错误 | `UnderrunError` | 旧式欠载错误枚举。 | Qt 6.11 弃用且不再发出。 |
| 错误 | `FatalError` | 表示不可恢复错误。 | 通常停止并重建管线。 |
| 状态 | `QtAudio::State` | 描述音频流当前处理状态。 | 由 sink/source 对象返回。 |
| 状态 | `ActiveState` | 正在处理音频数据。 | 不代表应用没有延迟。 |
| 状态 | `SuspendedState` | 流被暂停或暂时失去设备控制权。 | 用户恢复时调用 `resume()`。 |
| 状态 | `StoppedState` | 设备关闭或流停止。 | 结合 `error()` 判断原因。 |
| 状态 | `IdleState` | 因缓冲条件暂时无数据可处理。 | 可能伴随丢帧或断音。 |
| 标尺 | `QtAudio::VolumeScale` | 描述音量数值的解释方式。 | 转换前后必须明确范围。 |
| 标尺 | `LinearVolumeScale` | 线性音量标尺。 | Qt Multimedia 属性通常使用它。 |
| 标尺 | `CubicVolumeScale` | 立方近似对数标尺。 | 适合低成本 UI 映射。 |
| 标尺 | `LogarithmicVolumeScale` | 对数音量标尺。 | 常用于用户滑块。 |
| 标尺 | `DecibelVolumeScale` | 分贝振幅标尺。 | 常用范围约为 `-200` 到 `0`。 |
| 转换 | `float convertVolume(float, VolumeScale, VolumeScale)` | 在不同音量标尺之间转换。 | 不修改播放器或设备状态。 |
| 兼容 | `QAudio::Error` / `QAudio::State` | QtAudio 类型的旧名称。 | 新代码优先使用 `QtAudio`。 |

### 一句话总结

`QtAudio` 统一了音频对象共享的错误、状态和音量标尺；它定义语义，不负责创建设备或推动音频数据。
