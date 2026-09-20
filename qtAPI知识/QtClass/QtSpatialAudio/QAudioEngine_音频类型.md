# Qt QAudioEngine 深入笔记：三维声场的总控制器

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QAudioEngine>`  
> 所属模块：`Qt6::SpatialAudio`  
> 继承：`QObject -> QAudioEngine`  
> 状态：Qt Spatial Audio 在该版本文档中标为 Technology Preview

`QAudioEngine` 管理一个三维声场。它不是某个音频文件的播放器，而是把 listener、空间声源、背景叠加声、输出设备和可选房间效果组织到一起的渲染中心。

```text
QAudioEngine
├─ QAudioListener：听者的位置和朝向
├─ QSpatialSound：有位置和方向的声源
├─ QAmbientSound：与位置无关的背景立体声
├─ QAudioRoom：反射、混响和墙面材质
└─ QAudioDevice：最终输出设备
```

它解决的是“如何把一组 3D 声源按当前听者、设备与输出模式混成最后的音频”，而不是单独解决文件解码、播放列表或媒体控制界面。

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
engine.setOutputMode(QAudioEngine::Headphone);
engine.setMasterVolume(0.8f);
engine.setDistanceScale(QAudioEngine::DistanceScaleMeter);

QAudioListener listener(&engine);
listener.setPosition(QVector3D(0.0f, 1.7f, 0.0f));

QSpatialSound source(&engine);
source.setSource(QUrl("qrc:/audio/engine.wav"));
source.setPosition(QVector3D(3.0f, 1.7f, -2.0f));

engine.start();
source.play();
```

上例统一使用米：`DistanceScaleMeter == 100.0f`。如果不设置它，Qt 默认按厘米解释 `QAudioListener`、`QSpatialSound` 和 `QAudioRoom` 的坐标、尺寸与距离阈值。

## 2. 一个 engine 解决哪些事情

### 2.1 声场关系

引擎拿到 listener 和 `QSpatialSound` 后，会根据两者的相对位置与方向渲染空间感。`QSpatialSound` 决定声源在哪里、衰减模型和定向；listener 决定“谁在听、朝哪里听”。

`QAmbientSound` 则绕开位置和方向定位，作为稳定的立体声叠加层参与同一个 engine 的总混音。

### 2.2 输出模式

`OutputMode` 决定引擎把声场映射到输出设备的方式：

| 模式 | 含义 | 适用场景 |
| --- | --- | --- |
| `Surround` | 按输出设备的扬声器配置渲染，常见为立体声或环绕声 | 默认扬声器、家庭影院、系统多声道设备 |
| `Stereo` | 只用左右两个通道渲染，忽略额外扬声器 | 需要强制双声道输出或稳定的立体声结果 |
| `Headphone` | 使用耳机空间化渲染，模拟三维听感 | 耳机体验、沉浸式演示 |

不要只根据“当前设备是不是耳机”猜模式。应用应明确决定体验目标，再设置 `outputMode`；输出设备切换时也应重新检查这一策略。

### 2.3 采样率与重采样

默认构造时，engine 使用 `44100` Hz。传入自定义 `sampleRate` 后，采样率不匹配的声音会在引擎处理时被重采样。

默认值对多数项目足够。只有当项目大部分音频资源本来就采用另一采样率，并且测量确认重采样成本值得规避时，才需要构造时自定义：

```cpp
QAudioEngine engine(48000);
```

采样率是构造配置，不是播放过程中用来随意切换的旋钮。

## 3. 坐标单位：最容易被忽略的全局设置

`distanceScale` 是整个声场坐标系的比例。Qt 默认值 `DistanceScaleCentimeter` 为 `1.0f`，即把数值解释为厘米；`DistanceScaleMeter` 为 `100.0f`，使数值按米使用。

它会影响所有依赖距离的内容：

- listener 和空间声源的位置；
- `QSpatialSound::size`、`distanceCutoff` 等距离参数；
- `QAudioRoom` 的 position 与 dimensions。

最常见的错误是：场景模型使用米，但 Spatial Audio 仍按厘米工作。结果不是轻微偏差，而是距离衰减和房间边界都缩放错一百倍。

## 4. 房间效果不是只开一个开关

`setRoomEffectsEnabled(true)` 会启用回声和混响一类房间效果，但效果真正生效还需要：

1. 创建至少一个 `QAudioRoom`。
2. listener 处于某个 room 内。
3. room 的尺寸、位置、旋转和墙面材质与场景一致。

多个 room 覆盖同一位置时，Qt 选择体积最小的 room。若“明明创建了房间却没有混响”，先检查 listener 是否在 room 内，而不是先把 `reverbGain` 拉高。

## 5. 启动、暂停与停止

```text
未启动 -- start() --> 运行
运行 -- pause() / setPaused(true) --> 暂停
暂停 -- resume() / setPaused(false) --> 继续
运行或暂停 -- stop() --> engine 停止
```

- `start()`：启动整个声场引擎。
- `pause()`：暂停播放，相当于 `setPaused(true)`。
- `resume()`：继续播放，相当于 `setPaused(false)`。
- `stop()`：停止 engine。

对全局“游戏暂停”使用 `pause()`；对关闭场景、释放音频会话或重新初始化使用 `stop()`。单个背景音或单个空间声源的播放控制，应调用对应 `QAmbientSound` 或 `QSpatialSound` 的 `pause`、`play`、`stop`。

## 6. 生命周期与线程边界

所有 `QSpatialSound`、`QAmbientSound`、`QAudioListener` 和 `QAudioRoom` 都围绕 engine 工作。创建顺序通常是：

```cpp
QAudioEngine engine;
QAudioListener listener(&engine);
QSpatialSound source(&engine);
QAudioRoom room(&engine);
```

先创建 engine，最后销毁 engine。不要让仍在使用的空间音频对象保存已经失效的 engine 指针。

`QAudioEngine` 是 QObject。属性和控制 API 应在其所属线程调用；多线程场景通过 queued signal/slot 或 `QMetaObject::invokeMethod()` 把命令投递回正确线程，而不是从渲染、I/O 或工作线程直接改 engine。

## API 速查表
| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造 | `QAudioEngine()` | 以默认 44100 Hz 创建空间音频引擎 | 默认采样率适合多数项目；创建后再组织 listener、声源和房间 |
| 构造 | `QAudioEngine(QObject *parent)` | 创建带 QObject 父对象的默认采样率 engine | parent 管 QObject 生命周期，但仍要先停止正在使用的业务流程 |
| 构造 | `QAudioEngine(int sampleRate, QObject *parent = nullptr)` | 指定采样率创建 engine | 资源采样率不匹配会被重采样；只在明确需要时改默认 44100 Hz |
| 生命周期 | `~QAudioEngine()` | 销毁整个空间音频引擎 | 先让依赖的 listener、sound 和 room 停止参与业务更新 |
| 输出模式 | `QAudioEngine::Surround` | 按输出设备扬声器配置渲染 | 适合默认扬声器或多声道设备 |
| 输出模式 | `QAudioEngine::Stereo` | 强制使用左右双声道渲染 | 会忽略额外扬声器通道 |
| 输出模式 | `QAudioEngine::Headphone` | 用耳机空间化方式渲染三维听感 | 适合耳机体验，不等于自动检测到耳机 |
| 输出模式 | `outputMode() const` | 读取当前输出模式 | 设备或用户设置改变后重新检查实际策略 |
| 输出模式 | `setOutputMode(OutputMode mode)` | 设置声场映射到输出设备的方式 | 要和目标设备及体验目标匹配 |
| 输出模式 | `outputModeChanged()` | 输出模式改变时发出 | 适合同步设置界面；连接 lambda 时提供 context |
| 输出设备 | `outputDevice() const` | 读取当前用于播放的 `QAudioDevice` | 返回设备描述值，不表示设备一定仍可用 |
| 输出设备 | `setOutputDevice(const QAudioDevice &device)` | 设置声场输出设备 | 设备切换与系统热插拔都要有降级策略 |
| 输出设备 | `outputDeviceChanged()` | 输出设备设置改变时发出 | 这是配置变化，不是“设备已成功发声”的保证 |
| 总音量 | `masterVolume() const` | 读取整个声场的总输出增益 | 它不同于某个 sound 自己的 `volume` |
| 总音量 | `setMasterVolume(float volume)` | 设置整个声场的总输出增益 | 管总音量；单条 BGM 或声源音量应在各自对象上设置 |
| 总音量 | `masterVolumeChanged()` | 总输出增益改变时发出 | 可用于同步全局音量滑块 |
| 暂停状态 | `paused() const` | 查询 engine 是否处于暂停状态 | 表示全局 engine 状态，不是单个 sound 的暂停状态 |
| 暂停状态 | `setPaused(bool paused)` | 设置 engine 的暂停状态 | `true` 等价于 `pause()`，`false` 等价于 `resume()` |
| 暂停状态 | `pausedChanged()` | 暂停状态改变时发出 | 适合同步暂停 UI 和业务状态 |
| 距离尺度 | `DistanceScaleCentimeter` | 表示默认的厘米坐标尺度，值为 `1.0f` | 整个声场都必须采用同一单位 |
| 距离尺度 | `DistanceScaleMeter` | 表示米坐标尺度，值为 `100.0f` | 切换到米后 listener、source、room 的数值都按米填写 |
| 距离尺度 | `distanceScale() const` | 读取当前坐标尺度 | 调试距离衰减或房间范围异常时先检查它 |
| 距离尺度 | `setDistanceScale(float scale)` | 设置整个空间声场的坐标尺度 | 统一在初始化时设定，避免运行中让已有空间参数失去一致性 |
| 距离尺度 | `distanceScaleChanged()` | 距离尺度改变时发出 | 用于同步场景配置，不代表各对象坐标会自动重写 |
| 房间效果 | `roomEffectsEnabled() const` | 查询回声、反射和混响效果是否启用 | 仅开启开关不够；listener 必须进入已创建的 room |
| 房间效果 | `setRoomEffectsEnabled(bool enabled)` | 启用或关闭房间效果 | 多个 room 覆盖 listener 时，引擎选择体积最小的 room |
| 采样率 | `sampleRate() const` | 返回构造时配置的 engine 采样率 | 音频资源不匹配时会发生重采样 |
| 运行控制 | `start()` | 启动空间音频引擎 | 先完成声场对象和输出配置，再启动更易控制 |
| 运行控制 | `stop()` | 停止空间音频引擎 | 用于结束或重新初始化声场，不是单一声源的暂停 API |
| 运行控制 | `pause()` | 暂停整个 engine 的播放 | 等价于 `setPaused(true)` |
| 运行控制 | `resume()` | 恢复整个 engine 的播放 | 等价于 `setPaused(false)` |

---

### 一句话总结

`QAudioEngine` 是空间音频系统的中心：它统一坐标尺度、输出设备与模式、总音量、全局暂停和房间效果，并把 listener、空间声源、背景声与 room 组合成一个可渲染的三维声场。
