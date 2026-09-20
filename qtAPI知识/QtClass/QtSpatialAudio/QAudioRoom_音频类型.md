# Qt QAudioRoom 深入笔记：空间声场中的房间反射与混响

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QAudioRoom>`  
> 所属模块：`Qt6::SpatialAudio`  
> 继承：`QObject -> QAudioRoom`  
> 状态：Qt Spatial Audio 在该版本文档中标为 Technology Preview

`QAudioRoom` 为 `QAudioEngine` 描述一个盒状三维房间：它的中心位置、尺寸、旋转、六个墙面的材质，以及反射和混响的整体调节参数。listener 位于这个房间内部时，引擎会把一阶反射和与房间属性对应的混响加入声场。

它解决的不是普通“角色是否进入区域”的逻辑，而是“同一批空间声源在卧室、走廊、空旷大厅里为什么应当听起来不同”。

## 1. 最小可用代码

```cmake
find_package(Qt6 REQUIRED COMPONENTS SpatialAudio)
target_link_libraries(mytarget PRIVATE Qt6::SpatialAudio)
```

```cpp
#include <QAudioEngine>
#include <QAudioRoom>
#include <QVector3D>

QAudioEngine engine;
engine.setRoomEffectsEnabled(true);
engine.setDistanceScale(QAudioEngine::DistanceScaleMeter);

QAudioRoom room(&engine);
room.setPosition(QVector3D(0.0f, 1.5f, 0.0f));
room.setDimensions(QVector3D(8.0f, 3.0f, 6.0f));
room.setWallMaterial(QAudioRoom::Floor, QAudioRoom::WoodPanel);
room.setWallMaterial(QAudioRoom::Ceiling,
                     QAudioRoom::AcousticCeilingTiles);
room.setWallMaterial(QAudioRoom::FrontWall, QAudioRoom::BrickBare);
room.setReverbGain(0.7f);
room.setReflectionGain(0.8f);
```

上例将坐标尺度统一为米。若没有 `setDistanceScale(QAudioEngine::DistanceScaleMeter)`，`position` 和 `dimensions` 默认按厘米解释，这个“8 x 3 x 6”会变成非常小的空间。

## 2. 房间效果何时真正生效

`QAudioRoom` 本身不直接发声。要听到它的效果，需要同时满足：

1. `QAudioEngine::setRoomEffectsEnabled(true)` 已启用。
2. engine 中存在至少一个 room。
3. `QAudioListener` 当前位于某个 room 内。
4. 空间声源、listener 与 room 使用同一坐标尺度。

如果多个 room 覆盖 listener 的当前位置，引擎会选择**体积最小**的 room。这会影响房间嵌套设计：例如大楼大厅内又放了一个小隔音间，listener 位于小隔音间内时，应当由小房间的声学参数主导。

## 3. 空间几何：中心、尺寸和旋转

### 3.1 `position`

`position` 是房间中心，而不是左下角或某个入口点。通过中心坐标和 `dimensions`，引擎确定 room 覆盖的空间范围。

### 3.2 `dimensions`

`dimensions` 是房间在 x、y、z 三个方向的尺寸。它用于判断 listener 是否在室内，也影响房间总体体积。不要用视觉模型的 bounding box 直接照抄，除非视觉坐标、单位和旋转都与音频空间完全一致。

### 3.3 `rotation`

`rotation` 是房间在三维世界里的朝向。房间被旋转后，`LeftWall`、`FrontWall` 等墙面仍对应 room 的本地坐标方向，再由 quaternion 映射到世界中。

这让走廊、斜放的会议室等场景可以沿自身方向摆放。若你只改了视觉模型旋转、没有同步 room rotation，listener 的“在不在房间里”及墙面反射方向都会错位。

## 4. 六面墙与材质

`Wall` 将房间的六个面固定命名为：

| 枚举值 | 本地轴方向 |
| --- | --- |
| `LeftWall` / `RightWall` | 负 x / 正 x |
| `Floor` / `Ceiling` | 负 y / 正 y |
| `FrontWall` / `BackWall` | 负 z / 正 z |

每个面可通过 `setWallMaterial()` 单独指定材质。材质不是装饰标签，而是影响反射和混响频率特征的预设。

常用选择可以这样理解：

| 材质 | 声学含义 |
| --- | --- |
| `Transparent` | 这一面视为开放，不贡献反射或混响 |
| `AcousticCeilingTiles` | 大部分反射和混响被抑制 |
| `CurtainHeavy` | 主要保留较低频反射 |
| `FiberGlassInsulation` | 只保留很低频的反射 |
| `BrickBare`、`ConcreteBlockCoarse`、`Metal` | 较硬的表面，适合明显反射的空间 |
| `WoodPanel`、`WoodCeiling` | 木质面预设 |
| `UniformMaterial` | 人工均匀反射材质，适合测试或不想区分频段时 |

材质选择不用追求物理仿真级精确，但应表达空间类型。没有墙的门洞或开放侧面应使用 `Transparent`，而不是用一面实体墙再把 `reverbGain` 压低。

## 5. 三个全局声学旋钮

### 5.1 `reflectionGain`

控制一阶反射的增益：

- `0..1`：衰减反射；
- 大于 `1`：增强反射；
- 默认 `1`；
- `0`：关闭反射；
- 负数会被映射到 `0`。

它适合做“反射整体更强或更弱”的调节，不替代墙面材质。

### 5.2 `reverbGain`

控制 room 生成的混响增益，规则与 `reflectionGain` 类似：默认 `1`，`0` 关闭混响，负数映射为 `0`。

### 5.3 `reverbBrightness` 与 `reverbTime`

- `reverbBrightness`：正值提高混响高频并削弱低频；负值相反。默认 `0`。
- `reverbTime`：整体拉长或缩短混响时长；值越大，空间听起来越大。默认 `1`，负数映射为 `0`。

这两个参数一起调时，先确定材质和 room 几何，再调 gain，最后才调 brightness/time。否则很难判断是墙面预设、空间尺寸还是后期增益造成的听感。

## 6. 常见错误

### 创建 room 后没有启用 engine 的房间效果

`QAudioRoom` 不会自动打开 `QAudioEngine::roomEffectsEnabled`。没有启用时，room 参数存在但不会参与房间效果渲染。

### listener 不在 room 内

房间效果以 listener 位置为准，不是以声源位置为准。声源位于 room 内、listener 在门外时，不应期待听到该 room 的完整室内效果。

### 房间重叠时不知道哪个生效

不是最后创建的 room 覆盖前一个，而是体积最小的 room 被使用。设计房间嵌套时要把这个规则纳入场景配置。

## API 速查表
| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 墙面枚举 | `LeftWall` / `RightWall` | 表示 room 本地 x 轴负向和正向的两面墙 | room 旋转后仍按 room 本地坐标理解，不要直接按世界坐标猜 |
| 墙面枚举 | `Floor` / `Ceiling` | 表示 room 本地 y 轴负向和正向的地面与天花板 | 用于单独设置地板、天花板材质 |
| 墙面枚举 | `FrontWall` / `BackWall` | 表示 room 本地 z 轴负向和正向的前后墙 | 和场景模型的前向约定保持一致 |
| 材质枚举 | `Material` | 定义各类墙面声学预设 | 预设影响反射与混响频率特征，不只是名字标签 |
| 材质枚举 | `Transparent` | 表示开放面，不产生反射和混响贡献 | 适合门洞、开放侧面，而不是实体墙 |
| 材质枚举 | `AcousticCeilingTiles` | 表示强吸收的声学吊顶材质 | 适合希望明显压低反射的天花板 |
| 材质枚举 | `CurtainHeavy` / `FiberGlassInsulation` | 表示强吸收面，主要保留低频反射 | 适合窗帘、吸音材料一类场景 |
| 材质枚举 | `BrickBare` / `ConcreteBlockCoarse` / `Metal` | 表示较硬、反射更明显的表面 | 用于工业或硬质空间；听感仍受 gain 和尺寸共同影响 |
| 材质枚举 | `WoodPanel` / `WoodCeiling` / `UniformMaterial` | 表示木质面或均匀反射测试材质 | `UniformMaterial` 适合调试基线，不代表真实建筑材质 |
| 构造 | `QAudioRoom(QAudioEngine *engine)` | 为指定 engine 创建一个房间声学对象 | 必须传入有效 engine；先创建 engine 并保持其存活 |
| 生命周期 | `~QAudioRoom()` | 销毁房间对象 | 删除或移动 room 前要确认 listener 所处的其他 room 配置 |
| 几何读取 | `dimensions() const` | 返回 room 的 x/y/z 尺寸 | 单位受 engine 的 `distanceScale` 影响 |
| 几何设置 | `setDimensions(QVector3D dim)` | 设置 room 三维尺寸 | 与视觉场景统一单位；尺寸也影响 room 体积与重叠选择 |
| 几何通知 | `dimensionsChanged()` | room 尺寸改变时发出 | 适合同步场景编辑器或配置模型 |
| 位置读取 | `position() const` | 返回 room 中心位置 | 它不是房间角点位置 |
| 位置设置 | `setPosition(QVector3D pos)` | 设置 room 中心位置 | listener 是否在 room 内由中心、尺寸和旋转共同决定 |
| 位置通知 | `positionChanged()` | room 中心位置改变时发出 | 动态场景中避免无意义的逐帧重复设置 |
| 旋转读取 | `rotation() const` | 返回 room 的三维朝向 | 决定各本地墙面在世界中的方向 |
| 旋转设置 | `setRotation(const QQuaternion &q)` | 设置 room 的三维朝向 | 应与可视房间模型同步，优先使用同一个 quaternion |
| 旋转通知 | `rotationChanged()` | room 朝向改变时发出 | 用于同步编辑器或场景状态 |
| 反射读取 | `reflectionGain() const` | 返回一阶反射增益 | 默认 `1`；`0` 关闭反射 |
| 反射设置 | `setReflectionGain(float factor)` | 设置一阶反射整体增益 | `0..1` 衰减，超过 `1` 增强，负数会映射为 `0` |
| 反射通知 | `reflectionGainChanged()` | 反射增益改变时发出 | 只通知参数变化，不表示立刻验证了听感 |
| 混响读取 | `reverbGain() const` | 返回房间混响增益 | 不等于全局 master volume |
| 混响设置 | `setReverbGain(float factor)` | 设置房间混响整体增益 | `0` 关闭混响，负数映射为 `0` |
| 混响通知 | `reverbGainChanged()` | 混响增益改变时发出 | 适合配置界面同步 |
| 混响亮度读取 | `reverbBrightness() const` | 返回混响高低频倾向参数 | `0` 为默认中性倾向 |
| 混响亮度设置 | `setReverbBrightness(float factor)` | 调整混响高频相对低频的亮暗感 | 正值偏亮，负值偏暗；先完成材质与 gain 设置再微调 |
| 混响亮度通知 | `reverbBrightnessChanged()` | 混响亮度改变时发出 | 适合实时参数面板 |
| 混响时长读取 | `reverbTime() const` | 返回混响时长比例 | 值越大通常听起来空间越大 |
| 混响时长设置 | `setReverbTime(float factor)` | 设置整体混响时长比例 | 默认 `1`，负数映射为 `0`；不要用它代替正确的 room 尺寸 |
| 混响时长通知 | `reverbTimeChanged()` | 混响时长比例改变时发出 | 用于同步参数状态 |
| 墙面材质设置 | `setWallMaterial(Wall wall, Material material)` | 为某一面墙指定声学材质 | 六面可分别设置；开放面选 `Transparent` |
| 墙面材质查询 | `wallMaterial(Wall wall) const` | 返回指定墙当前使用的材质 | 传入的是 room 本地墙面枚举 |
| 墙面材质通知 | `wallsChanged()` | 任一墙面材质改变时发出 | 不提供哪一面墙的参数，接收方需要重新查询 |

---

### 一句话总结

`QAudioRoom` 用一个可旋转的盒状区域描述 listener 所在空间的声学特征：先让 engine 启用 room effects，再用位置、尺寸、墙面材质和反射/混响参数把视觉房间与听觉房间对齐。
