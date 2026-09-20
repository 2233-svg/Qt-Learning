# QAudioRoom
> Qt 6.11.1 · Qt Spatial Audio · 来自 `QAudioRoom`

## 1. 先建立直觉

`QAudioRoom` 描述空间音频里的房间：房间在哪里、多大、墙面是什么材质、反射和混响有多强。它不会自己播放声音，而是让 `QAudioEngine` 在计算声源时加入“声音在这个空间里传播”的感觉。

没有 room 时，空间音频主要体现方向和距离；有 room 后，声音会带上墙面反射、空间大小和材质造成的尾音差异。

## 2. 类说明

保留类说明：这些 API 来自 `QAudioRoom`，属于 Qt Spatial Audio 模块，用于描述房间几何和声学属性。

`QAudioRoom` 依赖 `QAudioEngine`。它和 `QSpatialSound`、`QAudioListener` 的关系不是父子控制，而是共同参与同一个引擎的声场计算。

## 3. API 速查

| API | 用来做什么 |
| --- | --- |
| `QAudioRoom(QAudioEngine *engine)` | 在指定引擎中创建房间。 |
| `setDimensions(QVector3D)` / `dimensions()` | 设置房间长宽高。 |
| `setPosition(QVector3D)` / `position()` | 设置房间中心或参考位置。 |
| `setRotation(QQuaternion)` / `rotation()` | 设置房间朝向。 |
| `setWallMaterial(Wall, Material)` | 指定某一面墙的材料。 |
| `wallMaterial(Wall)` | 查询某一面墙材料。 |
| `setReflectionGain(float)` / `reflectionGain()` | 控制早期反射强度。 |
| `setReverbGain(float)` / `reverbGain()` | 控制混响强度。 |
| `setReverbTime(float)` / `reverbTime()` | 控制混响衰减时间。 |
| `setReverbBrightness(float)` / `reverbBrightness()` | 控制混响明亮程度。 |
| `Material` | 墙面材质枚举，如透明、砖、玻璃、金属、木材等。 |
| `Wall` | 墙面枚举，用来区分 left/right/front/back/floor/ceiling。 |
| `wallsChanged()` | 墙面材料整体变化通知。 |
| `...Changed()` signals | 房间属性变化通知。 |

## 4. 典型流程

```cpp
auto *room = new QAudioRoom(engine);
room->setDimensions(QVector3D(6.0f, 3.0f, 8.0f));
room->setPosition(QVector3D(0, 1.5f, 0));
room->setWallMaterial(QAudioRoom::Floor, QAudioRoom::Wood);
room->setWallMaterial(QAudioRoom::Ceiling, QAudioRoom::AcousticCeilingTiles);
room->setReflectionGain(0.4f);
room->setReverbGain(0.25f);
```

房间参数最好和场景单位一致。若 `QAudioEngine::distanceScale()` 改了，房间尺寸也要重新检查。

## 5. 使用场景

| 场景 | 重点参数 |
| --- | --- |
| 室内漫游、建筑预览 | `dimensions`、墙面材质、`reverbTime`。 |
| 游戏房间/走廊/大厅切换 | 不同 room 配置随区域改变。 |
| 音频编辑器预览环境 | 让用户实时听到材质和空间大小变化。 |
| 训练模拟器 | 用空间混响提示用户所处环境。 |

## 6. 常见坑与经验

混响不是越多越真实。小空间里过大的 `reverbTime` 会让台词和提示音糊掉；金属、玻璃等高反射材质也要配合较低的 gain 做平衡。

墙面材质只是一组声学近似，不等于真实声学仿真。它适合交互应用里的可信效果，不适合拿来做严肃建筑声学计算。

房间是否生效还取决于 engine 的 room effects 设置，以及 listener、声源和房间的空间关系。只创建 `QAudioRoom` 但没打开 room effects，或者坐标根本不重合，听感可能没有变化。

旋转房间时要确认墙面枚举的语义仍符合你的关卡数据。特别是从建模工具导入房间时，轴向、单位和中心点经常需要转换。

## 7. 知识点覆盖

- 房间几何、材质、早期反射和混响的区别。
- `QAudioEngine` 房间效果开关与 room 对象的关系。
- 世界单位、房间尺寸、listener/声源位置之间的一致性。
- 材质枚举与真实声学模型的边界。
- 动态环境切换时的参数平滑与听感控制。
