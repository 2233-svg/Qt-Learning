# QAmbientSound
> Qt 6.11.1 · Qt Spatial Audio · 来自 `QAmbientSound`

## 1. 先建立直觉

`QAmbientSound` 是没有空间定位的声音层。它不会因为 listener 转头而跑到左边或右边，也不会因为距离变远而自动变小；它更像场景底噪、氛围铺底或背景循环。

在 Spatial Audio 里，它和 `QSpatialSound` 搭配使用：ambient 负责“这个地方整体听起来像什么”，spatial sound 负责“某个具体物体在哪里发声”。

## 2. 类说明

保留类说明：这些 API 来自 `QAmbientSound`，属于 Qt Spatial Audio 模块，用于播放非定位的环境声音。

它仍然挂在 `QAudioEngine` 上，受引擎暂停、停止、主音量和输出设备影响。但它不需要设置位置、旋转、距离模型或遮挡。

## 3. API 速查

| API | 用来做什么 |
| --- | --- |
| `QAmbientSound(QAudioEngine *engine)` | 在指定引擎中创建环境声。 |
| `setSource(QUrl)` / `source()` | 设置音频资源 URL。 |
| `play()` / `pause()` / `stop()` | 控制播放。 |
| `setAutoPlay(bool)` / `autoPlay()` | source 设置后是否自动播放。 |
| `setLoops(int)` / `loops()` | 设置循环次数，适合风声、雨声、机械底噪。 |
| `setVolume(float)` / `volume()` | 设置环境声自身音量。 |
| `engine() const` | 返回所属音频引擎。 |
| `Loops` | 循环次数相关枚举。 |
| `...Changed()` signals | 属性变化通知。 |

## 4. 典型流程

```cpp
auto *rain = new QAmbientSound(engine);
rain->setLoops(QAmbientSound::Infinite);
rain->setVolume(0.35f);
rain->setSource(QUrl("qrc:/audio/rain-bed.wav"));
rain->play();
```

如果不同区域需要不同氛围，可以交叉淡入淡出两个 `QAmbientSound`，不要硬切：

```cpp
forest->setVolume(forestGain);
cave->setVolume(caveGain);
```

## 5. 使用场景

| 场景 | 为什么用 ambient |
| --- | --- |
| 雨声、风声、城市底噪 | 用户不需要定位到单个发声点。 |
| 背景音乐或氛围 pad | 希望稳定覆盖整个声场。 |
| 区域环境切换 | 进入森林、洞穴、工厂时换声音底色。 |
| 与空间声源混合 | ambient 打底，`QSpatialSound` 提供具体事件。 |

## 6. 常见坑与经验

环境声最容易越叠越吵。多个循环铺底同时播放时，即使每个 `volume` 不高，总能量也会堆起来。项目里最好给 ambient 分配清晰的混音层级。

`QAmbientSound` 不做空间衰减。如果你想要“远处瀑布走近变大”，那应该用 `QSpatialSound`；如果你想要“整个关卡都被雨声包围”，才用 ambient。

循环素材要处理好首尾无缝，否则 `loops` 再正确也会每一轮听到咔哒或节奏断点。这个问题通常要在音频素材制作阶段解决，而不是靠 API 弥补。

`autoPlay` 适合资源固定的场景，但动态换 source 时要小心：新素材一加载就播可能打断淡出流程。需要转场控制时，手动 `play()` 更稳。

## 7. 知识点覆盖

- 环境声和空间定位声源的职责分工。
- 循环播放、自动播放、音量混合。
- 引擎全局状态对 ambient sound 的影响。
- 区域氛围切换和交叉淡入淡出设计。
- 音频素材无缝循环与 API 控制边界。
