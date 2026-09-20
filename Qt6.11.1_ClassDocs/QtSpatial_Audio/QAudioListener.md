# QAudioListener
> Qt 6.11.1 · Qt Spatial Audio · 来自 `QAudioListener`

## 1. 先建立直觉

`QAudioListener` 表示空间音频世界里的“耳朵”。所有 `QSpatialSound` 的左右、远近、前后、方向感，最终都要相对于 listener 的位置和朝向来计算。

在 3D 应用里，它通常跟摄像机或玩家头部绑定；在普通 2.5D 场景里，它可以固定在屏幕中心或用户角色位置。

## 2. 类说明

保留类说明：这些 API 来自 `QAudioListener`，属于 Qt Spatial Audio 模块，用于描述听者的空间位置和方向。

一个 `QAudioListener` 总是和某个 `QAudioEngine` 一起使用。没有 engine，它没有独立播放能力；没有正确更新位置和旋转，空间声源就会像“世界动了但耳朵没动”一样失真。

## 3. API 速查

| API | 用来做什么 |
| --- | --- |
| `QAudioListener(QAudioEngine *engine)` | 为指定引擎创建听者。 |
| `engine() const` | 返回所属音频引擎。 |
| `setPosition(QVector3D)` / `position()` | 设置或读取听者在 3D 世界中的位置。 |
| `setRotation(QQuaternion)` / `rotation()` | 设置或读取听者朝向。 |
| `positionChanged()` | 位置变化信号。 |
| `rotationChanged()` | 朝向变化信号。 |

## 4. 典型流程

```cpp
auto *listener = new QAudioListener(engine);

void SceneAudio::syncFromCamera(const Camera &camera)
{
    listener->setPosition(camera.position());
    listener->setRotation(camera.orientation());
}
```

同步时要确认坐标系一致。图形场景常见 `-Z` 为前方，而音频参数如果按另一个前向约定理解，左右和前后会反过来。

## 5. 使用场景

| 场景 | 用法 |
| --- | --- |
| 第一人称视角 | listener 绑定玩家头部或摄像机。 |
| 第三人称游戏 | listener 可在摄像机和角色之间折中，避免镜头太远导致声音距离怪异。 |
| 2D 地图或编辑器 | listener 固定在观察点，声源按场景坐标移动。 |
| VR/AR | listener 需要高频同步头显姿态，对延迟更敏感。 |

## 6. 常见坑与经验

位置更新频率要和场景运动匹配。角色高速移动但 listener 每秒只更新几次，会出现声音跳变；相反，没变也每帧发 changed 信号，会增加无意义计算。

旋转建议使用归一化的 `QQuaternion`。从欧拉角反复转换时要注意轴顺序和单位，尤其是 yaw/pitch/roll 的定义在引擎或项目中可能不同。

listener 不等于摄像机，但经常绑定摄像机。第三人称游戏里完全绑定摄像机可能让角色脚步声变远；完全绑定角色又可能让镜头外危险声不符合用户视觉。要按交互体验选择。

## 7. 知识点覆盖

- 听者位置/朝向对空间音频的基准作用。
- `QVector3D` 坐标和 `QQuaternion` 旋转。
- 图形坐标系与音频坐标系一致性。
- 摄像机、角色、头显与 listener 的绑定策略。
- 属性变化信号和更新频率控制。
