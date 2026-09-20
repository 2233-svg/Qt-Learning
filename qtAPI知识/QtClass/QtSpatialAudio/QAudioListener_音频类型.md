# Qt QAudioListener 深入笔记：三维声场中的听者位置与朝向

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QAudioListener>`  
> 所属模块：`Qt6::SpatialAudio`  
> 继承：`QObject -> QAudioListener`  
> 状态：Qt Spatial Audio 在该版本文档中标为 Technology Preview

`QAudioListener` 表示“正在听这个三维声场的人”。它不播放音频，也不保存房间声学参数；它只把听者的**位置**和**朝向**交给 `QAudioEngine`。引擎再根据 listener 与每个 `QSpatialSound` 的相对距离、相对方向、输出模式和房间效果，决定音量、左右声道或耳机空间化结果。

它解决的问题不是“让声音移动”，而是“同一个声源为什么会因为听者移动或转头而听起来不同”。

```text
QAudioEngine
├─ QSpatialSound：声源在哪里、朝哪里、衰减怎样算
├─ QAmbientSound：不随空间位置变化的背景叠加声
├─ QAudioRoom：房间边界、墙面材质、反射与混响
└─ QAudioListener：听者在哪里、朝哪里
```

## 1. 最小可用代码

```cmake
find_package(Qt6 REQUIRED COMPONENTS SpatialAudio)
target_link_libraries(mytarget PRIVATE Qt6::SpatialAudio)
```

```cpp
#include <QAudioEngine>
#include <QAudioListener>
#include <QQuaternion>
#include <QSpatialSound>
#include <QUrl>
#include <QVector3D>

QAudioEngine engine;

QAudioListener listener(&engine);
listener.setPosition(QVector3D(0.0f, 170.0f, 0.0f));
listener.setRotation(QQuaternion());

QSpatialSound bell(&engine);
bell.setSource(QUrl("qrc:/audio/bell.wav"));
bell.setPosition(QVector3D(300.0f, 170.0f, -200.0f));

engine.start();
bell.play();
```

这里的位置默认以**厘米**为单位。上例中声源大致位于听者右前方；若项目采用米作为世界单位，应先统一 `QAudioEngine::distanceScale`，不能只给 listener 改成“米”而让声源仍按“厘米”填写。

## 2. 它在声场中到底负责什么

### 2.1 `position` 决定距离和相对方向

listener 的位置与 `QSpatialSound::position` 使用同一套三维坐标系。引擎据此计算：

1. 声源离听者多远，从而应用距离衰减。
2. 声源在听者的前、后、左、右哪个方向。
3. 听者是否位于 `QAudioRoom` 内部，以便启用该房间的反射和混响。

因此，镜头、角色和 listener 是否共用坐标系，是接入时最先要确认的事情。3D 场景中的模型位置若已经是米，而 listener 仍按 Qt 默认厘米解释，听感会被放大或缩小一百倍。

### 2.2 `rotation` 决定“前方”朝哪里

`rotation` 是一个 `QQuaternion`。它表示听者在世界坐标系中的朝向，而不是欧拉角数组。听者转向右边时，原来在右侧的声源会相对变到前方或左侧，引擎据此重新渲染空间声像。

如果渲染系统已有相机或角色的 quaternion，通常直接同步它，而不要把欧拉角逐帧拆开再拼回 quaternion：

```cpp
listener.setPosition(camera.position());
listener.setRotation(camera.rotation());
```

这样可以避免欧拉角顺序、角度/弧度和万向节锁带来的额外问题。

## 3. 使用场景

### 第一人称或第三人称场景

把 listener 绑定到相机或玩家头部。第一人称一般同步相机位置和旋转；第三人称则要先明确声音应以镜头位置、角色头部还是观众位置为准。

### 室内声场演示

listener 进入 `QAudioRoom` 后，引擎才会把该房间的反射和混响纳入渲染。调试时先确认 listener 的位置确实落在 room 内，再怀疑 `reflectionGain` 或墙面材质。

### 非交互式 3D 音频

即使听者不移动，也需要一个 `QAudioListener` 给引擎定义参考点和朝向。固定展台、展馆导览和空间音频测试程序都常把它固定在原点。

## 4. 生命周期与同步边界

构造函数要求传入有效的 `QAudioEngine *`。实践中应先创建 engine，再创建 listener，并确保 engine 在 listener 的整个使用期内有效：

```cpp
QAudioEngine engine;
QAudioListener listener(&engine);
```

一个 `QAudioEngine` 的声场围绕一个 listener 计算。不要把 `QAudioListener` 当成多人同时监听同一声场的容器；多人独立听感通常需要分别组织引擎或更高层的音频架构。

`QAudioListener` 继承 QObject，因此跨线程更新位置或旋转时仍要遵守 QObject 线程亲和性。游戏循环、Qt Quick 3D 同步和音频对象若不在同一线程，应用 queued 调用或受控同步，不要从任意工作线程直接写属性。

## 5. 常见误区

### 只移动声源，不更新 listener

如果相机或玩家移动而 listener 保持原地，空间声会仍以旧听者位置计算。表现通常是角色已经走近声源，声音却像仍在远处。

### 把 `position` 单位当成米

默认距离单位与 Qt Quick 3D 一致，是厘米。项目世界单位为米时使用 `QAudioEngine::setDistanceScale()` 统一换算。

### 把 `rotation` 当成声源朝向

listener 的 rotation 改变的是“听者面向哪里”；声源定向则由 `QSpatialSound::rotation`、`directivity` 等 API 控制。两者共同决定听感，但职责不同。

## API 速查表
| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造 | `QAudioListener(QAudioEngine *engine)` | 为指定空间音频引擎创建一个听者 | `engine` 必须有效，并应在 listener 使用期间保持存活 |
| 生命周期 | `~QAudioListener()` | 销毁 listener | 先停止或销毁依赖它的上层场景逻辑，避免继续向已销毁对象同步相机数据 |
| 关联引擎 | `engine() const` | 返回此 listener 所属的 `QAudioEngine` | 返回的是关联对象，不是新的 engine；不要据此推断或接管所有权 |
| 位置读取 | `position() const` | 返回听者当前三维位置 | 坐标单位由 `QAudioEngine::distanceScale` 统一解释，默认厘米 |
| 位置设置 | `setPosition(QVector3D pos)` | 设置听者在声场中的位置 | 与 `QSpatialSound`、`QAudioRoom` 使用同一坐标系；通常每帧或场景同步时更新 |
| 朝向读取 | `rotation() const` | 返回听者当前的三维朝向 quaternion | 它描述听者面向方向，不是声源方向 |
| 朝向设置 | `setRotation(const QQuaternion &q)` | 设置听者在声场中的朝向 | 优先直接同步相机/角色 quaternion；避免把不一致的欧拉角约定混入 |

---

### 一句话总结

`QAudioListener` 是 `QAudioEngine` 声场中的听者参考系：用 `position` 决定距离和相对方位，用 `rotation` 决定“前方”方向，并始终让它与声源、房间和渲染场景使用同一套坐标单位。
