# Qt Spatial Audio：空间声源、监听者与房间声学

Qt Spatial Audio 根据声源和监听者在三维空间中的相对位置计算方向、距离衰减和房间反射，再输出为立体声、耳机双耳或环绕声。它适合 3D 应用、导航提示、游戏和沉浸式展示，但不是完整的数字音频工作站，也不替代 Qt Multimedia 的通用媒体播放。

核心对象是 `QAudioEngine`、`QAudioListener`、`QSpatialSound`、`QAmbientSound` 和 `QAudioRoom`。

## 1. CMake 配置

```cmake
find_package(Qt6 REQUIRED COMPONENTS Core Gui Multimedia SpatialAudio)

target_link_libraries(mytarget PRIVATE
    Qt6::Core
    Qt6::Gui
    Qt6::Multimedia
    Qt6::SpatialAudio
)
```

QML/Quick 3D 项目还需链接 `Qt6::Quick3D` 并导入空间音频 QML 模块。部署时必须带上音频后端插件和支持的解码器。

## 2. 最小 C++ 空间音频

```cpp
#include <QAudioEngine>
#include <QAudioListener>
#include <QSpatialSound>
#include <QUrl>

QAudioEngine engine;
engine.setOutputMode(QAudioEngine::Headphone);

QAudioListener listener(&engine);
listener.setPosition(QVector3D(0, 0, 0));

QSpatialSound sound(&engine);
sound.setSource(QUrl::fromLocalFile("audio/bell.wav"));
sound.setPosition(QVector3D(2, 0, -4));
sound.setVolume(0.8f);

engine.start();
sound.play();
```

引擎必须在声源和监听者之后保持存活。不要把 `QAudioEngine` 创建为局部临时对象后返回；其析构会终止混音和输出。

## 3. 坐标与单位

所有空间对象必须使用同一坐标约定。Qt 的三维坐标通常以 `QVector3D` 表示，但“一个单位等于一米”由应用决定。建议明确规定：

```text
+X：右
+Y：上
-Z：前
1 场景单位 = 1 米
```

若视觉场景使用厘米，音频位置却直接当作米传入，距离衰减会严重失真。建立一个集中转换函数：

```cpp
QVector3D sceneToAudio(const QVector3D &scenePosition)
{
    constexpr float centimetersPerMeter = 100.0f;
    return scenePosition / centimetersPerMeter;
}
```

## 4. 监听者 `QAudioListener`

监听者表示用户的头部或相机：

```cpp
QAudioListener listener(&engine);
listener.setPosition(cameraPosition);
listener.setRotation(cameraOrientation);
```

只有位置不够，旋转决定“前、后、左、右”。相机旋转若用欧拉角，先转换为 `QQuaternion` 再传给监听者，避免轴顺序和万向锁问题。

视觉相机和监听者最好由同一个状态源驱动，而不是每帧互相读取。这样暂停渲染或切换相机时仍能明确控制音频方向。

## 5. 空间声源 `QSpatialSound`

### 5.1 基本播放控制

```cpp
QSpatialSound sound(&engine);
sound.setSource(QUrl("qrc:/audio/machine.wav"));
sound.setLoops(QSpatialSound::Infinite);
sound.setVolume(0.55f);
sound.setPosition(QVector3D(4, 1, -8));
sound.play();
```

`volume` 是声源增益，不等同于距离后的最终响度。避免把多个声源都设为最大音量，否则混音叠加可能削波。

### 5.2 声源方向与锥体

有方向性的声源（扬声器、发动机排气口）可设置旋转、内外锥角和锥外增益。监听者位于声源背面时，声音会按配置衰减。无方向环境声则使用 `QAmbientSound` 更合适。

### 5.3 声源大小

```cpp
sound.setSize(1.5f);
```

`size` 描述声源的空间尺寸。接近点声源时，非零尺寸可以避免方向在穿过中心点时突然翻转，也使大型机器或瀑布更自然。

## 6. 距离衰减模型

`QSpatialSound::DistanceModel` 提供三种策略：

| 模式 | 特点 | 适用场景 |
| --- | --- | --- |
| `Logarithmic` | 接近真实声学，近处变化明显 | 通用 3D 场景 |
| `Linear` | 在设定范围内均匀下降 | UI 化、可预测的提示音 |
| `ManualAttenuation` | 应用自行计算增益 | 特殊业务或非物理地图 |

```cpp
sound.setDistanceModel(QSpatialSound::DistanceModel::Logarithmic);
sound.setNearDistance(1.0f);
sound.setFarDistance(25.0f);
```

近距离表示开始明显衰减的尺度，远距离用于限制影响范围。参数名和具体曲线应以 Qt 6.11.1 文档为准，并用实际耳机/扬声器试听，不要仅看数值。

手动衰减模式：

```cpp
sound.setDistanceModel(QSpatialSound::DistanceModel::ManualAttenuation);
sound.setManualAttenuation(0.35f);
```

应用若每帧计算衰减，应进行平滑，避免位置采样抖动产生响度颤动。

## 7. 环境声 `QAmbientSound`

环境声没有单一空间位置，适合背景音乐、风声或全局提示：

```cpp
#include <QAmbientSound>

QAmbientSound ambience(&engine);
ambience.setSource(QUrl("qrc:/audio/room-tone.wav"));
ambience.setLoops(QAmbientSound::Infinite);
ambience.setVolume(0.25f);
ambience.play();
```

不要用一个放得很远的 `QSpatialSound` 模拟背景音乐，因为它仍会受方向、距离和房间处理影响。

## 8. 房间声学 `QAudioRoom`

### 8.1 创建房间

```cpp
#include <QAudioRoom>

QAudioRoom room(&engine);
room.setPosition(QVector3D(0, 1.5f, 0));
room.setDimensions(QVector3D(8, 3, 12));

room.setWallMaterial(QAudioRoom::Floor,
                     QAudioRoom::WoodPanel);
room.setWallMaterial(QAudioRoom::Ceiling,
                     QAudioRoom::AcousticCeilingTiles);

engine.setRoomEffectsEnabled(true);
```

房间六个表面可分别指定材料。材料决定不同频段的吸收与反射特性。房间尺寸和位置必须与视觉空间一致，否则用户离开可见房间后仍可能听到错误反射。

### 8.2 混响与反射参数

房间还提供反射、混响增益和时间等调节项。优先从真实尺寸与墙面材料开始，再微调这些参数；把混响增益直接拉满通常会掩盖语音清晰度。

### 8.3 多房间边界

多个房间相邻时，明确监听者当前属于哪一个房间，并在切换时平滑过渡。短时间同时启用多个强房间效果会产生不自然的能量叠加。

## 9. 输出模式与设备

```cpp
engine.setOutputMode(QAudioEngine::Stereo);
// 还可选择 Headphone 或 Surround
```

- `Headphone` 使用适合双耳定位的输出。
- `Stereo` 面向普通双声道扬声器。
- `Surround` 需要实际设备和通道布局支持。

使用 `QMediaDevices::audioOutputs()` 枚举设备，再传给引擎：

```cpp
const auto outputs = QMediaDevices::audioOutputs();
if (!outputs.isEmpty())
    engine.setOutputDevice(outputs.first());
```

监听设备变化信号。蓝牙耳机断开、默认设备切换或采样率变化时，应给用户可恢复的状态，而不是继续显示“正在播放”。

## 10. QML 与 Quick 3D 集成

```qml
import QtQuick
import QtQuick3D
import QtQuick3D.SpatialAudio

AudioEngine {
    id: audioEngine
    outputMode: AudioEngine.Headphone
}

AudioListener {
    engine: audioEngine
    position: camera.scenePosition
    rotation: camera.sceneRotation
}

SpatialSound {
    engine: audioEngine
    source: "qrc:/audio/bell.wav"
    position: bellModel.scenePosition
    loops: SpatialSound.Infinite
}
```

具体模块 URI 和属性连接以 Qt 6.11.1 QML 文档为准。视觉节点位置若频繁变化，避免创建新的向量对象和复杂绑定链；可以在动画或物理更新点同步音频变换。

## 11. 资源格式与流式播放

短音效适合解码后缓存，长环境声适合流式读取。选择格式时考虑：

- WAV 解码开销小但体积大。
- 压缩格式体积小但增加 CPU 和启动延迟。
- 所有目标平台未必支持同一编解码器。
- 高频触发的短音效应避免每次重新打开文件。

在目标平台查询实际支持格式，不要把开发机安装的系统编解码器当作部署保证。

## 12. 性能与响度管理

空间声源数量增加会带来解码、空间化和混音成本。建议：

1. 对远处、遮挡或低优先级声源做虚拟化，只保留播放时间而不完整混音。
2. 设置同时发声上限，同类短音效采用 voice stealing。
3. 静态声源不必每帧重复设置位置。
4. 房间效果只在需要时启用。
5. 用总线或业务分组控制音乐、环境、语音和效果音音量。

最终混音要留出余量。多个 0.8 增益声源叠加并不保证不会削波。

## 13. 线程与生命周期

音频对象是 QObject，遵守线程亲和性。不要从渲染线程或工作线程直接修改 GUI 线程创建的声源；通过信号槽或集中音频控制器提交更新。

销毁顺序建议为：先停止声源和房间更新，再销毁声源/监听者，最后停止并销毁引擎。回调中使用 `QPointer` 防止设备变化或页面退出后访问已销毁对象。

## 14. 测试与排查

### 左右方向相反

检查视觉坐标到音频坐标的 Z 轴方向、四元数乘法顺序和相机父节点变换。用固定左、右、前、后四个声源逐一试听。

### 距离变化不明显

检查单位比例、near/far distance、声源 size 和 distance model。临时关闭房间效果，先验证直接声。

### 没有声音

检查引擎是否启动、输出设备是否有效、源 URL 是否可访问、格式是否受支持、音量是否为零以及对象是否仍存活。

### 自动化测试

音频主观质量难以完全自动化，但可测试对象状态、设备切换、播放结束、取消和资源失败。关键版本还应进行耳机与扬声器人工试听，覆盖空间方向、房间大小和响度一致性。

## 15. 速查表

| 目标 | 类/API |
| --- | --- |
| 混音与输出 | `QAudioEngine` |
| 用户/相机位置 | `QAudioListener` |
| 有位置的声音 | `QSpatialSound` |
| 全局背景声 | `QAmbientSound` |
| 房间反射和混响 | `QAudioRoom` |
| 输出设备 | `QMediaDevices`、`setOutputDevice()` |
| 距离模型 | `QSpatialSound::DistanceModel` |

空间音频的质量取决于统一坐标、正确监听者方向、受控距离曲线和可靠设备管理。先让这些基础行为可测，再增加房间混响和大量动态声源。
