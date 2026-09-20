# QMediaDevices：枚举当前媒体设备并监听设备变化

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QMediaDevices>`  
> 所属模块：`Qt6::Multimedia`  
> 继承：`QObject`

## 它解决什么问题

`QMediaDevices` 提供 Qt Multimedia 能看到的媒体设备清单和默认设备查询：

- 音频输入设备，例如麦克风；
- 音频输出设备，例如扬声器、耳机；
- 视频输入设备，例如摄像头；
- 当前默认的音频输入、音频输出和视频输入。

它把平台枚举、默认设备选择和设备插拔变化统一为 Qt API。应用不需要直接调用 Windows、macOS、Linux 或移动平台的设备发现接口。

它只负责发现和描述设备，不负责打开设备、不负责申请全部隐私权限，也不负责开始采集或播放。找到 `QAudioDevice` 或 `QCameraDevice` 后，仍要把它交给 `QAudioInput`、`QAudioOutput` 或 `QCamera`。

## 真实使用场景

- 设置页面显示麦克风、扬声器和摄像头下拉列表；
- 启动视频会议时选择默认摄像头和默认麦克风；
- 用户插入耳机后刷新输出设备并切换路由；
- 设备被拔出后提示用户重新选择；
- 在 WebAssembly 或需要权限的环境中等待异步设备列表可用。

## 基本用法

```cpp
const auto cameras = QMediaDevices::videoInputs();
const auto microphones = QMediaDevices::audioInputs();
const auto speakers = QMediaDevices::audioOutputs();

if (!cameras.isEmpty()) {
    auto *camera = new QCamera(cameras.first(), this);
    camera->start();
}
```

若只需要默认设备，可以直接查询：

```cpp
const QCameraDevice cameraDevice =
        QMediaDevices::defaultVideoInput();
const QAudioDevice inputDevice =
        QMediaDevices::defaultAudioInput();
const QAudioDevice outputDevice =
        QMediaDevices::defaultAudioOutput();
```

在界面中长期显示设备列表时，应创建一个 `QMediaDevices` 对象并连接变化信号：

```cpp
auto *devices = new QMediaDevices(this);

connect(devices, &QMediaDevices::audioInputsChanged,
        this, &Controller::reloadMicrophones);
connect(devices, &QMediaDevices::audioOutputsChanged,
        this, &Controller::reloadSpeakers);
connect(devices, &QMediaDevices::videoInputsChanged,
        this, &Controller::reloadCameras);
```

## 静态查询和实例对象的分工

`audioInputs()`、`audioOutputs()`、`videoInputs()` 以及三个 `default...()` 函数都是静态函数。它们返回当时的设备快照；返回的列表不会自动随着系统插拔变化而更新。

`QMediaDevices` 实例主要用于接收变化信号。它不代表某一个硬件设备，也不需要为每个摄像头或麦克风各创建一个实例。通常一个应用控制器持有一个实例即可。

设备值类型通常可以复制并放入模型，但复制的是设备描述，不是已经打开的设备会话。把列表中的设备传给 `QCamera` 或音频对象后，仍要处理设备消失、权限拒绝和后端打开失败。

## 三类列表和默认设备

### `audioInputs()`

返回可作为输入的音频设备列表，通常包括内置麦克风、USB 麦克风和蓝牙输入端点。列表中的每个 `QAudioDevice` 还包含设备名称、唯一 ID、默认格式和格式能力等信息。

空列表可能表示当前没有设备、权限尚未准备好、后端尚未初始化或平台不提供可枚举的输入。不要把空列表简单解释为“硬件一定不存在”。

### `audioOutputs()`

返回可作为输出的音频设备列表，例如扬声器、耳机和外接音频接口。默认输出会随着系统路由变化，例如插入耳机或切换系统音频设备。

### `videoInputs()`

返回可作为视频输入的摄像头设备列表。列表项是 `QCameraDevice`，其中包含前置/后置、位置、摄像头特性和支持格式等描述。

### 默认设备

`defaultAudioInput()`、`defaultAudioOutput()` 和 `defaultVideoInput()` 返回当前系统默认设备的描述。如果没有默认设备，可能得到无效的设备值。调用方应检查相应值的 `isNull()` 或 `isValid()`，并准备好默认设备在运行期间变化。

默认设备不是永久绑定。系统设置、蓝牙连接、USB 插拔、摄像头权限变化和平台路由策略都可能改变默认设备。对应的列表变化信号也用于通知默认设备可能改变：

- 默认音频输入变化：`audioInputsChanged()`；
- 默认音频输出变化：`audioOutputsChanged()`；
- 默认视频输入变化：`videoInputsChanged()`。

收到通知后应重新调用 `default...()`，不要继续使用旧快照推断默认设备。

## 设备变化的处理策略

设备变化信号只表示相关设备集合或默认选择可能改变，不携带新增、移除或替换项。正确处理方式是重新调用对应的静态列表函数，再用设备 ID 或设备值更新模型。

如果当前正在使用的设备消失：

1. 重新读取设备列表和默认设备；
2. 判断当前 `QAudioDevice` 或 `QCameraDevice` 是否仍在列表中；
3. 停止或重新配置对应的输入/输出对象；
4. 向用户说明设备已不可用，或切换到新的默认设备；
5. 继续监听后续变化。

不要在变化信号槽中只修改 UI 文本而不更新实际的 `QCamera`、`QAudioInput` 或 `QAudioOutput`；否则界面显示的设备和媒体管线使用的设备会分离。

## 异步枚举、权限和平台边界

设备枚举可能受到操作系统隐私权限和媒体后端初始化影响。尤其在 WebAssembly 平台，设备列表具有异步性质：文档明确说明，列表要等到相应的 `audioInputsChanged`、`audioOutputsChanged` 或 `videoInputsChanged` 通知后才可用。

因此，应用启动时可以先读取一次列表，但不能把第一次读取结果当作最终结果。在需要权限的系统上，应按平台要求触发权限流程，并在通知到达后重新枚举。设备列表非空也不保证之后一定能成功打开，创建 `QCamera` 或音频对象时仍需处理错误状态。

设备变化信号由对象的 Qt 事件循环交付。要接收它们，`QMediaDevices` 实例必须存活，所属线程必须有运行中的事件循环。不要在临时对象上连接信号后立即销毁对象，也不要阻塞其线程等待设备列表同步出现。

## 所有权、线程和快照有效期

`QMediaDevices` 是 `QObject`，父对象可以管理它的生命周期，但它不拥有系统设备，也不会因为析构而关闭其他媒体对象正在使用的设备。

`QAudioDevice` 和 `QCameraDevice` 是设备描述值，不是 `QObject`。将它们复制到工作线程只复制描述信息；实际创建和操作 `QCamera`、`QAudioInput`、`QAudioOutput` 仍应遵守这些对象的线程归属。平台设备状态可能在值复制后变化，因此使用前要重新检查可用性。

设备 ID 适合在当前运行期间识别设备，但不应无条件当作跨机器、跨系统安装都稳定不变的持久主键。应用可以保存用户偏好 ID，恢复时仍要在当前列表中匹配，匹配不到就回退默认设备或让用户重新选择。

## 常见误区

- 把 `QMediaDevices` 当作摄像头或声卡对象，直接期待它能开始采集。
- 认为静态列表会自动更新；每次变化都要重新查询。
- 只在应用启动时读取一次默认设备。
- 收到变化信号后只刷新下拉框，不重配正在使用的媒体对象。
- 把第一次空列表当成“没有硬件”，忽略权限和异步初始化。
- 在 WebAssembly 上同步读取列表并假设已经完成枚举。
- 把设备描述值的复制当成设备资源的复制或锁定。
- 保存设备名称作为稳定标识，而不使用当前列表中的设备 ID/值匹配。
- 只处理设备发现，不处理创建媒体对象后的权限、格式和后端错误。

## API 速查表

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造 | `QMediaDevices(QObject *parent = nullptr)` | 创建设备变化通知对象。 | 不代表某个硬件；通常全局/控制器持有一个。 |
| 析构 | `~QMediaDevices() override` | 销毁通知对象。 | 不关闭或销毁系统设备。 |
| 查询 | `static QList<QAudioDevice> audioInputs()` | 返回当前音频输入设备快照。 | 变化后需重新调用；可能为空。 |
| 查询 | `static QList<QAudioDevice> audioOutputs()` | 返回当前音频输出设备快照。 | 不会自动随插拔更新。 |
| 查询 | `static QList<QCameraDevice> videoInputs()` | 返回当前摄像头设备快照。 | 可能受权限和后端初始化影响。 |
| 默认 | `static QAudioDevice defaultAudioInput()` | 返回当前默认音频输入。 | 默认设备会变化；使用前检查有效性。 |
| 默认 | `static QAudioDevice defaultAudioOutput()` | 返回当前默认音频输出。 | 耳机、蓝牙和系统路由可能改变它。 |
| 默认 | `static QCameraDevice defaultVideoInput()` | 返回当前默认摄像头。 | 可能为空或随摄像头变化而改变。 |
| 通知 | `void audioInputsChanged()` | 音频输入列表或默认输入可能变化。 | 槽中重新调用 `audioInputs()` 和 `defaultAudioInput()`。 |
| 通知 | `void audioOutputsChanged()` | 音频输出列表或默认输出可能变化。 | 槽中重新调用 `audioOutputs()` 和 `defaultAudioOutput()`。 |
| 通知 | `void videoInputsChanged()` | 摄像头列表或默认摄像头可能变化。 | 槽中重新调用 `videoInputs()` 和 `defaultVideoInput()`。 |
| 保护扩展 | `void connectNotify(const QMetaMethod &signal) override` | Qt 内部按需建立设备变化监听。 | 主要供框架实现；应用通常不需要重写。 |

## 一句话总结

`QMediaDevices` 给应用的是“当前设备描述快照加变化通知”：用静态函数取得设备，用实例信号监听变化，真正打开、使用和恢复设备则交给 `QCamera`、`QAudioInput` 和 `QAudioOutput` 完成。
