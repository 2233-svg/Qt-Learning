# QAudioEngine
> Qt 6.11.1 · Qt Spatial Audio · 来自 `QAudioEngine`

## 1. 先建立直觉

`QAudioEngine` 是 Qt Spatial Audio 的“声场引擎”。`QSpatialSound`、`QAmbientSound`、`QAudioRoom`、`QAudioListener` 都围绕它工作：声音源交给它混合，听者位置由它关联，房间效果也由它统一计算。

你可以把它看成一个小型 3D 音频世界的运行时。创建声音对象前先有 engine，配置采样率、输出设备、输出模式和主音量，然后启动或暂停整个音频世界。

## 2. 类说明

保留类说明：这些 API 来自 `QAudioEngine`，属于 Qt Spatial Audio 模块，用于管理空间音频播放、输出和全局状态。

`QAudioEngine` 和普通 `QAudioSink` 不同：后者更像“把 PCM 写到设备”，前者强调“多个空间声源如何在听者位置被感知”。如果你只播放一段普通背景音乐，`QMediaPlayer` 或 `QAudioSink` 可能更直接；如果声音位置、方向、遮挡和房间反射重要，才是它的主场。

## 3. API 速查

| API | 用来做什么 |
| --- | --- |
| `QAudioEngine(int sampleRate, QObject *parent = nullptr)` | 以指定采样率创建引擎。 |
| `QAudioEngine(QObject *parent = nullptr)` | 使用默认采样率创建引擎。 |
| `start()` | 启动音频处理和输出。 |
| `stop()` | 停止引擎输出。 |
| `pause()` / `resume()` | 暂停或恢复整个引擎。 |
| `setPaused(bool)` / `paused()` | 用属性形式控制/读取暂停状态。 |
| `setMasterVolume(float)` / `masterVolume()` | 设置全局音量倍率。 |
| `setDistanceScale(float)` / `distanceScale()` | 设置世界单位到距离模型的缩放关系。 |
| `setOutputDevice(QAudioDevice)` / `outputDevice()` | 选择音频输出设备。 |
| `setOutputMode(OutputMode)` / `outputMode()` | 选择 surround、stereo 或 headphone 输出模式。 |
| `sampleRate()` | 查询引擎采样率。 |
| `setRoomEffectsEnabled(bool)` / `roomEffectsEnabled()` | 开关房间反射/混响效果。 |
| `OutputMode` | 输出模式枚举：`Surround`、`Stereo`、`Headphone`。 |
| `...Changed()` signals | 属性变化通知，供 QML/binding/状态面板使用。 |

## 4. 典型流程

```cpp
auto *engine = new QAudioEngine(48000, this);
engine->setOutputMode(QAudioEngine::Headphone);
engine->setMasterVolume(0.8f);
engine->start();

auto *listener = new QAudioListener(engine);
listener->setPosition(QVector3D(0, 1.7f, 0));

auto *sound = new QSpatialSound(engine);
sound->setSource(QUrl("qrc:/audio/door.wav"));
sound->setPosition(QVector3D(2, 1, -4));
sound->play();
```

引擎本身只提供世界和输出，具体“听者在哪里”由 `QAudioListener` 表示，“声音从哪里来”由 `QSpatialSound` 表示。

## 5. 使用场景

| 场景 | 为什么适合 |
| --- | --- |
| 游戏、仿真、VR/AR 声场 | 声源和听者都在 3D 空间移动。 |
| 工业或医疗训练软件 | 空间提示音能帮助用户判断事件方向。 |
| 展馆、多媒体装置 | 需要多声源、房间感、耳机模式等输出策略。 |
| 交互式编辑器预览空间音效 | 引擎提供统一播放上下文，便于实时调整参数。 |

## 6. 常见坑与经验

`distanceScale` 会影响所有距离衰减的主观结果。项目里要先定单位：1 个世界单位到底是 1 米、1 厘米还是一个格子。单位没定清，后面调 `distanceCutoff`、房间尺寸和声源大小都会变成凭感觉乱调。

输出模式要按设备选择。耳机上使用 `Headphone` 往往比普通 stereo 更符合空间音频预期；环绕声设备则需要确认系统和后端确实能提供对应声道。

切换输出设备不是纯 UI 状态变化，可能涉及后端重新打开设备。真实应用里要处理设备消失、默认设备变化、权限失败和静音策略。

房间效果不是自动“更高级”。小房间、强反射、高混响时间叠在一起很容易糊成一片。先把干声、距离和方向调准，再逐步加 room effects。

## 7. 知识点覆盖

- Spatial Audio 对象关系：engine、listener、spatial sound、ambient sound、room。
- 采样率、输出设备、输出模式和主音量。
- 距离单位缩放和空间衰减的全局影响。
- 引擎暂停/恢复与单个 sound 播放状态的区别。
- 房间效果、输出后端和平台设备差异。
