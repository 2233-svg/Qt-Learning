# Qt QAmbientSound 深入笔记：不随位置变化的背景立体声

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QAmbientSound>`  
> 所属模块：`Qt6::SpatialAudio`  
> 继承：`QObject -> QAmbientSound`  
> 状态：Qt Spatial Audio 在该版本文档中标为 Technology Preview

`QAmbientSound` 是挂在 `QAudioEngine` 上的一层**立体声叠加音**。它不参与三维距离衰减、方向定位或 listener 朝向计算，因此特别适合背景音乐、固定 UI 氛围声、旁白底音等“无论玩家走到哪里、转向哪里都不该在左右耳间移动”的声音。

它解决的问题是：项目已经有三维空间声场，但还需要一条不受空间坐标影响的稳定音频层。把这类声音硬塞进 `QSpatialSound`，往往会得到不必要的距离衰减和声像移动。

```text
QAudioEngine
├─ QSpatialSound：位置、朝向、距离衰减、遮挡
└─ QAmbientSound：与位置、listener 朝向无关的立体声叠加层
```

## 1. 最小可用代码

```cmake
find_package(Qt6 REQUIRED COMPONENTS SpatialAudio)
target_link_libraries(mytarget PRIVATE Qt6::SpatialAudio)
```

```cpp
#include <QAmbientSound>
#include <QAudioEngine>
#include <QUrl>

QAudioEngine engine;

QAmbientSound music(&engine);
music.setSource(QUrl("qrc:/audio/ambient.ogg"));
music.setLoops(QAmbientSound::Infinite);
music.setVolume(0.35f);

engine.start(); // autoPlay 默认为 true，设定 source 后可自动开始
```

若希望完全由业务流程控制播放时机，先关闭自动播放：

```cpp
music.setAutoPlay(false);
music.setSource(QUrl("qrc:/audio/ambient.ogg"));

engine.start();
music.play();
```

## 2. 和 `QSpatialSound` 的选择

| 需求 | 应选类型 | 原因 |
| --- | --- | --- |
| 世界中的风扇、脚步、车辆、角色说话 | `QSpatialSound` | 音量和声像应随距离、方向和 listener 改变 |
| BGM、菜单音乐、整体环境底噪 | `QAmbientSound` | 不应因为相机移动或转头而改变左右位置 |
| 需要随房间、墙面和距离变化的声音 | `QSpatialSound` + 可选 `QAudioRoom` | 需要参与空间声场计算 |
| 想要一个普通媒体播放器 | 视需求选择 Qt Multimedia | `QAmbientSound` 的定位是空间音频引擎中的叠加层，不是完整播放器 UI |

不要因为文件本身是双声道，就默认选择 `QAmbientSound`。判断标准是**听感是否应该与听者在 3D 世界里的位置和朝向无关**。

## 3. 播放状态：自动开始、暂停和停止的区别

### 3.1 `autoPlay`

`autoPlay` 默认为 `true`。当设置了 `source` 后，声音会自动开始播放。它适合“资源一到位就播放”的背景音乐或场景常驻氛围声。

如果加载来源、淡入、用户音量设置和引擎启动需要按明确顺序完成，应设为 `false`，最后显式调用 `play()`。

### 3.2 `pause()` 与 `stop()`

```text
正在播放
  ├─ pause() -> 暂停在当前位置
  │               └─ play() -> 从暂停位置继续
  └─ stop()  -> 停止，并把当前位置和当前循环计数重置
                  └─ play() -> 从文件开头重新开始
```

这一区别会直接影响“游戏暂停”与“切换场景后重新播放”的体验：

- 游戏进入暂停菜单：通常用 `pause()`。
- 用户点击“从头播放”或资源切换：通常用 `stop()` 后再 `play()`。
- `play()` 在已经播放时不会重复启动第二次同一声音。

## 4. 循环与音量

### 4.1 `loops`

`loops` 决定文件在停止前播放多少次：

- `QAmbientSound::Once`（值为 `1`）：播放一次，默认值。
- `QAmbientSound::Infinite`（值为 `-1`）：无限循环。
- 正整数：按指定次数播放。

循环 BGM 应显式设置 `Infinite`，不要依赖资源长度或在外部用定时器不断重启。外部定时器会在事件循环延迟、切歌和暂停恢复时积累边界问题。

### 4.2 `volume`

`volume` 是该声音自己的增益：

- `0` 到 `1`：衰减；
- 大于 `1`：额外增益。

它不等于 `QAudioEngine::masterVolume`。前者只调这一条背景音，后者调整个声场的总输出。通常把用户“音乐音量”映射到 ambient sound 的 `volume`，把“总音量”映射到 engine 的 master volume。

## 5. 生命周期与常见错误

构造 `QAmbientSound` 时必须传入有效 `QAudioEngine *`。先创建 engine，并确保 engine 在声音对象工作期间仍有效：

```cpp
QAudioEngine engine;
QAmbientSound music(&engine);
```

### 把 BGM 做成空间声源

当 listener 移动或转头时，BGM 不应该向某侧漂移或突然变小。该需求应该用 `QAmbientSound`，不是把 `QSpatialSound` 固定在 listener 旁边。

### 依赖 `autoPlay` 却没有控制加载顺序

默认自动播放适合简单场景；但如果要先设置音量、循环次数或淡入逻辑，应先关掉 `autoPlay`，配置完整后再 `play()`。

### 用 `stop()` 实现短暂停顿

`stop()` 会重置播放位置和循环计数。需要继续播放时使用 `pause()`，不是 stop。

## API 速查表
| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 循环枚举 | `QAmbientSound::Infinite` | 表示无限循环播放 | 值为 `-1`；适合 BGM 和常驻氛围声 |
| 循环枚举 | `QAmbientSound::Once` | 表示只播放一次 | 值为 `1`，也是默认循环次数 |
| 构造 | `QAmbientSound(QAudioEngine *engine)` | 为指定空间音频引擎创建一条立体声叠加音 | `engine` 必须有效，并应在该声音之前创建、之后销毁 |
| 关联引擎 | `engine() const` | 返回关联的 `QAudioEngine` | 返回的是已有引擎，不转移所有权 |
| 自动播放读取 | `autoPlay() const` | 查询设置 source 后是否会自动播放 | 默认是 `true`；复杂加载流程应显式设置而不是猜默认值 |
| 自动播放设置 | `setAutoPlay(bool)` | 打开或关闭 source 设置后的自动播放 | 要手动控制开始时机时先设为 `false` |
| 自动播放通知 | `autoPlayChanged()` | 在自动播放设置改变时发出 | 连接 lambda 时提供 context，避免对象销毁后仍访问捕获对象 |
| 循环次数读取 | `loops() const` | 返回当前循环次数 | `-1` 表示无限循环，不要当作普通负数错误值处理 |
| 循环次数设置 | `setLoops(int loops)` | 设置停止前的播放次数 | BGM 常设为 `Infinite`；一次性提示音通常保留 `Once` |
| 循环次数通知 | `loopsChanged()` | 在循环次数改变时发出 | 只通知设置变化，不代表当前循环已经播放完成 |
| 来源读取 | `source() const` | 返回当前要播放的音频文件 URL | 用于检查当前资源；不要通过字符串猜测资源是否已实际开始播放 |
| 来源设置 | `setSource(const QUrl &url)` | 设置要播放的音频来源 | `autoPlay` 为 true 时会触发自动开始；替换资源前要设计好是否需要 stop 或淡出 |
| 来源通知 | `sourceChanged()` | 在 source 改变时发出 | 这是配置变化信号，不是“文件已加载完成”信号 |
| 音量读取 | `volume() const` | 返回这一条 ambient sound 的增益 | 与 `QAudioEngine::masterVolume` 分工不同：一个调单声源，一个调总输出 |
| 音量设置 | `setVolume(float volume)` | 设置这一条背景音的增益 | `0..1` 为衰减，大于 `1` 会额外增益；混音时留意削波风险 |
| 音量通知 | `volumeChanged()` | 在该声音音量改变时发出 | 适合同步音量滑块或配置模型 |
| 暂停 | `pause()` | 暂停当前播放位置 | 后续 `play()` 会继续播放，而不是从头开始 |
| 播放 | `play()` | 开始播放或从暂停位置继续 | 已在播放时不会重复启动第二次同一声音 |
| 停止 | `stop()` | 停止播放并重置播放位置和当前循环计数 | 后续 `play()` 会从文件开头开始 |

---

### 一句话总结

`QAmbientSound` 用于不受 listener 位置和朝向影响的立体声背景层：用 `source` 指定资源，用 `loops` 管循环，用 `volume` 做单声源混音，并根据要继续还是重头开始选择 `pause()` 或 `stop()`。
