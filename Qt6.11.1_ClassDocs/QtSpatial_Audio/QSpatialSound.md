# QSpatialSound
> Qt 6.11.1 · Qt Spatial Audio · 来自 `QSpatialSound`

## 1. 先建立直觉

`QSpatialSound` 是一个有位置、有方向、会随距离衰减的声音源。脚步声、门响、车辆、机器、飞过的物体，都更像 `QSpatialSound`，而不是普通背景音乐。

它需要挂在 `QAudioEngine` 上工作，并且听感会受 `QAudioListener` 的位置、引擎输出模式、距离模型、房间效果等因素影响。

## 2. 类说明

保留类说明：这些 API 来自 `QSpatialSound`，属于 Qt Spatial Audio 模块，用于播放空间定位声源。

`QSpatialSound` 不是万能播放器。它强调短音效、循环环境源、3D 定位和衰减；复杂媒体播放控制、视频同步、流媒体协议等需求仍应看 `QMediaPlayer` 或更底层音频 API。

## 3. API 速查

| API | 用来做什么 |
| --- | --- |
| `QSpatialSound(QAudioEngine *engine)` | 在指定引擎中创建空间声源。 |
| `setSource(QUrl)` / `source()` | 设置音频资源 URL。 |
| `play()` / `pause()` / `stop()` | 控制播放。 |
| `setAutoPlay(bool)` / `autoPlay()` | source 就绪后是否自动播放。 |
| `setLoops(int)` / `loops()` | 设置循环次数，含 `Infinite` 等特殊值。 |
| `setVolume(float)` / `volume()` | 控制声源自身音量。 |
| `setPosition(QVector3D)` / `position()` | 设置声源位置。 |
| `setRotation(QQuaternion)` / `rotation()` | 设置声源朝向。 |
| `setSize(float)` / `size()` | 设置声源尺寸，用于近场/体积感计算。 |
| `setDistanceModel(DistanceModel)` / `distanceModel()` | 选择距离衰减模型。 |
| `setDistanceCutoff(float)` / `distanceCutoff()` | 设置衰减距离边界。 |
| `setManualAttenuation(float)` / `manualAttenuation()` | 手动衰减模型下设置衰减值。 |
| `setOcclusionIntensity(float)` / `occlusionIntensity()` | 设置遮挡强度。 |
| `setDirectivity(float)` / `directivity()` | 设置方向性强度。 |
| `setDirectivityOrder(float)` / `directivityOrder()` | 设置方向性曲线阶数。 |
| `setNearFieldGain(float)` / `nearFieldGain()` | 调整近场增益。 |
| `engine() const` | 返回所属音频引擎。 |
| `DistanceModel` | 距离衰减模型：对数、线性、手动衰减。 |
| `Loops` | 循环次数相关枚举。 |
| `...Changed()` signals | 属性变化通知。 |

## 4. 典型流程

```cpp
auto *door = new QSpatialSound(engine);
door->setSource(QUrl("qrc:/audio/door-close.wav"));
door->setPosition(QVector3D(3.0f, 1.0f, -2.0f));
door->setDistanceModel(QSpatialSound::Logarithmic);
door->setDistanceCutoff(20.0f);
door->setVolume(0.9f);
door->play();
```

循环声源通常设置 `loops` 和 `autoPlay`，例如机器嗡鸣、火焰、瀑布：

```cpp
fan->setLoops(QSpatialSound::Infinite);
fan->setAutoPlay(true);
fan->setSource(QUrl("qrc:/audio/fan-loop.wav"));
```

## 5. 使用场景

| 场景 | 关注点 |
| --- | --- |
| 一次性音效 | `source`、`position`、`play()`，注意对象生命周期。 |
| 循环环境声源 | `loops`、`volume`、距离 cutoff，避免多个循环叠太吵。 |
| 有方向的设备或喇叭 | `rotation`、`directivity`、`directivityOrder`。 |
| 遮挡或隔墙效果 | `occlusionIntensity` 配合场景检测或房间效果。 |
| 近距离大物体 | `size`、`nearFieldGain`，避免声源像一个无限小点。 |

## 6. 常见坑与经验

距离模型要按体验选。对数衰减更接近很多自然听感；线性衰减容易调得直观；手动衰减适合你已经有一套游戏/仿真声学规则，不想让 Qt 自动算。

`volume` 是声源音量，`masterVolume` 是引擎总音量，距离衰减和遮挡还会继续改变最终输出。排查“为什么没声音”时，要从 source 是否加载、engine 是否 start、listener 距离、音量链路、输出设备逐项看。

方向性只在声源朝向有意义时才值得调。一个警报器可以有强方向性；一团火、雨声、普通脚步声通常不需要。

动态移动声源时，属性更新要平滑。每帧大幅跳位置会产生明显听感抖动；网络同步场景尤其需要插值。

## 7. 知识点覆盖

- 空间声源与环境声源的区别。
- 位置、旋转、尺寸、方向性、近场增益。
- 距离模型、cutoff、手动衰减和遮挡。
- 循环播放、自动播放和对象生命周期。
- 与 listener、engine、room effects 的组合调试。
