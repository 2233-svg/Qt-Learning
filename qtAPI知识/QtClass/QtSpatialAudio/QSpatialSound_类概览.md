# Qt QSpatialSound 深入笔记：有位置、方向与遮挡的三维声源

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QSpatialSound>`  
> 所属模块：`Qt6::SpatialAudio`  
> 继承：`QObject -> QSpatialSound`  
> 状态：Qt Spatial Audio 在该版本文档中标为 Technology Preview

`QSpatialSound` 表示三维世界中的一个声源。它把音频文件放到一个位置上，并提供距离衰减、声源朝向、近场增益、遮挡、循环和音量等参数。`QAudioEngine` 再结合 `QAudioListener` 的位置与朝向，把它渲染成听者实际听到的空间声。

它解决的是“这个声音在世界里的哪里、朝哪里发声、离远后怎样变小、被墙挡住后怎样变闷”，而不是普通背景音乐播放。

```text
QAudioEngine
├─ QAudioListener：听者位置与朝向
├─ QSpatialSound：空间中的声源
│  ├─ source：播放哪个文件
│  ├─ position / rotation：在哪里、朝哪里
│  ├─ size / distanceCutoff：距离范围
│  ├─ distanceModel：怎样随距离衰减
│  ├─ directivity：是否像喇叭一样定向发声
│  └─ occlusionIntensity：被遮挡时怎样削弱直达声
└─ QAudioRoom：可选的房间反射与混响
```

## 1. 最小可用代码

```cmake
find_package(Qt6 REQUIRED COMPONENTS SpatialAudio)
target_link_libraries(mytarget PRIVATE Qt6::SpatialAudio)
```

```cpp
#include <QAudioEngine>
#include <QAudioListener>
#include <QSpatialSound>
#include <QUrl>
#include <QVector3D>

QAudioEngine engine;
engine.setDistanceScale(QAudioEngine::DistanceScaleMeter);

QAudioListener listener(&engine);
listener.setPosition(QVector3D(0.0f, 1.7f, 0.0f));

QSpatialSound machine(&engine);
machine.setSource(QUrl("qrc:/audio/machine.wav"));
machine.setPosition(QVector3D(4.0f, 0.0f, -3.0f));
machine.setSize(0.5f);
machine.setDistanceCutoff(25.0f);
machine.setDistanceModel(QSpatialSound::DistanceModel::Logarithmic);
machine.setLoops(QSpatialSound::Infinite);

engine.start();
machine.play();
```

这段代码使用米。没有把 engine 的 `distanceScale` 设为 `DistanceScaleMeter` 时，`4.0f` 会被解释成 4 厘米，而不是 4 米。

## 2. 什么时候该用它，什么时候不该用

| 声音需求 | 推荐类型 | 原因 |
| --- | --- | --- |
| 机器、脚步、门、车辆、NPC 说话 | `QSpatialSound` | 听感应随 listener 的距离与方向变化 |
| 背景音乐、菜单音乐、全局环境底音 | `QAmbientSound` | 不应该因玩家移动或转头而漂移 |
| 房间回声、墙面材质造成的混响变化 | `QAudioRoom` 配合 `QSpatialSound` | room 描述声场环境，sound 描述声源 |

只要“听者离开声源越远，声音应越小；转头后声像应改变”，就应该考虑 `QSpatialSound`。

## 3. 距离衰减：`size`、`distanceCutoff` 与 `distanceModel`

这三个参数需要一起理解：

```text
listener 到声源距离

0 -------- size ----------- distanceCutoff -------->
|            |                    |
| 音量保持    | 按模型开始衰减      | 音量为 0，听不到
```

- `size`：听者比这个距离更近时，音量保持不变；它还参与大型声源的部分遮挡计算。
- `distanceCutoff`：超过这个距离后，声源不再可听。
- `distanceModel`：在 `size` 到 `distanceCutoff` 之间按哪种曲线衰减。

`DistanceModel` 的三种选择：

| 模型 | 含义 | 适用场景 |
| --- | --- | --- |
| `Logarithmic` | 音量随距离按对数下降 | 较自然的普通环境声，通常是优先尝试的选择 |
| `Linear` | 音量在有效距离区间线性下降 | 需要可预测、易调参的演示或游戏规则 |
| `ManualAttenuation` | 不按距离曲线自动计算，直接使用 `manualAttenuation` | 外部系统已经算好遮挡、脚本化音量或自定义混音逻辑 |

把 `distanceModel` 设成 `ManualAttenuation` 才会让 `manualAttenuation` 成为核心控制量。只设置 `manualAttenuation`、却仍使用 Logarithmic 或 Linear，是常见的“参数看起来没有效果”原因。

## 4. 定向声源：`rotation`、`directivity` 与 `directivityOrder`

默认 `directivity == 0`，即声源向所有方向均匀发声，像点声源。把它提高到 `1` 后，声音主要沿声源前向发射，更接近扬声器、排气口、角色嘴部或舞台音箱。

`directivityOrder` 控制声锥的锐利程度：

- 最小值和默认值为 `1`。
- 值越高，声锥越集中，听者偏离前方时衰减更明显。

只有同步设置 `rotation` 才能让定向有可解释的世界方向：

```cpp
speaker.setRotation(actor.mouthRotation());
speaker.setDirectivity(0.8f);
speaker.setDirectivityOrder(2.0f);
```

`rotation` 是 `QQuaternion`。它描述的是**声源**朝向；`QAudioListener::rotation` 描述的是**听者**朝向，二者不要混用。

## 5. 近场、遮挡与大型声源

### 5.1 `nearFieldGain`

取值范围是 `0..1`。值为 `1` 时，听者非常靠近声源会获得约 20 dB 的额外增益。它适合强调贴近耳边、靠近机器或靠近角色嘴边时的存在感。

它不是普通音量调节。整体音量使用 `volume`；近距离才更响的效果使用 `nearFieldGain`。

### 5.2 `occlusionIntensity`

`occlusionIntensity` 描述声源被其他对象遮挡的程度：

- `0`：不遮挡，默认值。
- `1`：完全遮挡。
- 大于 `1`：进一步压低来自声源的直达声。

完全遮挡不等于静音。Qt 仍让它参与 room 的混响和反射，但会特别削弱高频，让声音更闷。这更接近“隔着墙听到声音”的感觉。

Qt 不会替你的物理场景自动算墙体遮挡。你需要根据射线检测、导航网格、游戏逻辑或场景关系更新该值。

### 5.3 `size`

`size` 不只是“声音有多大”。听者位于 size 半径内时音量保持恒定；此外，大声源可以被一面墙部分遮挡，而不是被当成数学点完全挡住。

例如大风机、长列车或舞台幕墙可使用更大的 size；手持道具、按钮提示音适合较小 size。

## 6. 资源、循环与播放控制

`source` 是要播放的文件 URL。`autoPlay` 默认 `true`，因此设置 source 后会自动开始播放；需要由加载流程、淡入或交互控制时，先设 `setAutoPlay(false)`。

循环规则：

- `Once`：播放一次，默认值。
- `Infinite`：无限循环。
- 正整数：播放指定次数。

播放控制的差异：

```text
play()  ：开始播放；已经播放时不重复启动
pause() ：暂停当前位置；之后 play() 从这里继续
stop()  ：停止并重置当前位置和当前循环计数；之后 play() 从开头开始
```

## 7. 常见错误与排查顺序

### 声音没有距离变化

依次检查：

1. 是否使用了 `QSpatialSound`，而不是 `QAmbientSound`。
2. listener 与 sound 是否都设置到了同一坐标系。
3. `QAudioEngine::distanceScale` 是否与场景单位一致。
4. `size` 是否大得让 listener 始终在恒定音量区。
5. `distanceCutoff` 是否设置得过大或过小。

### 定向参数没有效果

确认 `directivity` 大于 0，并且同步了 `rotation`。只提高 `directivityOrder` 而 `directivity` 仍为 0，不会把全向声源变成定向扬声器。

### 遮挡后完全没声音

`occlusionIntensity == 1` 并不设计为静音。若完全没有声音，还要检查 volume、距离 cutoff、source、engine 状态，以及是否误把声源停掉了。

### 设置 source 后比预期更早播放

默认 `autoPlay` 为 true。需要明确播放时机时，先 `setAutoPlay(false)`，再设置 source。

## API 速查表
| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 距离模型 | `DistanceModel::Logarithmic` | 让音量在有效距离区间按对数曲线下降 | 常用于较自然的空间声；仍受 `size` 与 `distanceCutoff` 限制 |
| 距离模型 | `DistanceModel::Linear` | 让音量在有效距离区间线性下降 | 适合想要可预测距离规则的场景 |
| 距离模型 | `DistanceModel::ManualAttenuation` | 使用 `manualAttenuation` 作为外部指定的衰减控制 | 只在该模式下手动衰减参数才是核心 |
| 循环枚举 | `Infinite` / `Once` | 分别表示无限循环与播放一次 | `Infinite == -1`，`Once == 1`，默认循环次数为一次 |
| 构造 | `QSpatialSound(QAudioEngine *engine)` | 为指定 engine 创建一个可放入 3D 世界的声源 | 必须传入有效 engine，并确保其在 sound 使用期间存活 |
| 生命周期 | `~QSpatialSound()` | 销毁声源对象 | 删除后不要继续从场景同步位置、旋转或播放命令 |
| 关联引擎 | `engine() const` | 返回关联的 `QAudioEngine` | 返回已有对象，不转移所有权 |
| 资源 | `source()` / `setSource(const QUrl &)` / `sourceChanged()` | 读取、设置并通知要播放的音频文件 URL | 默认 `autoPlay` 为 true；`sourceChanged()` 只说明配置改变，不代表文件已播放 |
| 自动播放 | `autoPlay()` / `setAutoPlay(bool)` / `autoPlayChanged()` | 控制设置 source 后是否自动开始播放 | 默认 true；需要精确控制加载和淡入时机时设为 false |
| 循环 | `loops()` / `setLoops(int)` / `loopsChanged()` | 读取、设置并通知停止前的播放次数 | `-1` 是无限循环；不要用外部定时器模拟循环 |
| 空间位置 | `position()` / `setPosition(QVector3D)` / `positionChanged()` | 读取、设置并通知声源三维位置 | 单位由 engine 的 `distanceScale` 决定，默认厘米；与 listener 使用同一坐标系 |
| 空间朝向 | `rotation()` / `setRotation(const QQuaternion &)` / `rotationChanged()` | 读取、设置并通知声源的三维朝向 | 主要与 directivity 配合；它不是 listener 的朝向 |
| 普通音量 | `volume()` / `setVolume(float)` / `volumeChanged()` | 读取、设置并通知这一条声源的增益 | `0..1` 衰减，大于 1 额外增益；与 engine master volume 分工不同 |
| 衰减模型 | `distanceModel()` / `setDistanceModel(DistanceModel)` / `distanceModelChanged()` | 读取、设置并通知距离衰减的计算方式 | 自动模型在 `size` 到 `distanceCutoff` 区间工作；手动模式配合 `manualAttenuation` |
| 恒定音量区 | `size()` / `setSize(float)` / `sizeChanged()` | 定义近距离内保持恒定音量的声源大小 | 也参与部分遮挡计算；过大可能使距离衰减看起来失效 |
| 最远距离 | `distanceCutoff()` / `setDistanceCutoff(float)` / `distanceCutoffChanged()` | 定义超出后不再可听的距离 | 需要和场景单位、size 以及关卡尺度一起设置 |
| 手动衰减 | `manualAttenuation()` / `setManualAttenuation(float)` / `manualAttenuationChanged()` | 读取、设置并通知外部指定的衰减因子 | 只有 `ManualAttenuation` 距离模型时才应把它作为主控制量 |
| 遮挡 | `occlusionIntensity()` / `setOcclusionIntensity(float)` / `occlusionIntensityChanged()` | 读取、设置并通知声源被遮挡的程度 | 0 不遮挡，1 完全遮挡但仍可能听到混响/反射；大于 1 可进一步削弱直达声 |
| 定向程度 | `directivity()` / `setDirectivity(float)` / `directivityChanged()` | 控制声源从全向到主要向前发声的程度 | 有效范围 0..1，默认 0；要先大于 0 才会有定向效果 |
| 声锥锐度 | `directivityOrder()` / `setDirectivityOrder(float)` / `directivityOrderChanged()` | 控制定向声锥的集中程度 | 最小值和默认值为 1；越大越尖锐，需与 rotation 一起调试 |
| 近场增益 | `nearFieldGain()` / `setNearFieldGain(float)` / `nearFieldGainChanged()` | 控制听者非常靠近声源时的额外增益 | 有效范围 0..1；值 1 在极近距离约可增加 20 dB |
| 播放 | `play()` | 开始播放或从暂停位置继续 | 已在播放时不会重复启动第二个同源播放 |
| 暂停 | `pause()` | 暂停当前播放位置 | 之后 `play()` 会继续，而不是从开头播放 |
| 停止 | `stop()` | 停止播放并重置当前位置与当前循环计数 | 之后 `play()` 会从文件开头开始 |

---

### 一句话总结

`QSpatialSound` 是可放进三维世界的声源：用 position、rotation 和 directivity 决定“在哪里、朝哪里响”，用 size、cutoff 和 distanceModel 决定“多远还能听到”，再用遮挡、近场增益和 room 让听感更接近真实空间。
