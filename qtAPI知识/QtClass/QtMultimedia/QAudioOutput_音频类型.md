# QAudioOutput：为播放与采集会话配置音频输出

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QAudioOutput>`  
> 所属模块：`Qt6::Multimedia`  
> 继承：`QObject`  
> 相关类型：`QAudioDevice`、`QMediaDevices`、`QMediaPlayer`、`QMediaCaptureSession`

## 1. 它解决什么问题

`QAudioOutput` 表示媒体播放或媒体会话中的一个物理音频输出通道。它负责选择扬声器、耳机或 HDMI 音频设备，并控制当前媒体流的静音和音量；它不负责读取音频文件，也不负责把 PCM 写入声卡。

常见场景包括：

- `QMediaPlayer` 播放视频或音频时选择输出设备；
- 视频会议中把远端声音切换到耳机；
- 录制/预览应用中配置 `QMediaCaptureSession` 的监听输出；
- 在应用内部实现静音、音量滑块和设备切换。

如果应用需要把自己生成的 PCM 数据直接送入声卡，应使用 `QAudioSink`。`QAudioOutput` 是媒体框架的输出配置对象，`QAudioSink` 是原始音频输出接口。

## 2. 构建与最小用法

```cmake
find_package(Qt6 REQUIRED COMPONENTS Multimedia)
target_link_libraries(mytarget PRIVATE Qt6::Multimedia)
```

```cpp
#include <QAudioOutput>
#include <QMediaPlayer>

auto *player = new QMediaPlayer(this);
auto *output = new QAudioOutput(this);
player->setAudioOutput(output);
player->setSource(QUrl("qrc:/audio/intro.wav"));

connect(output, &QAudioOutput::volumeChanged,
        this, [](float volume) {
            qDebug() << "stream volume:" << volume;
        });
```

默认构造使用系统默认输出设备。若要选择具体设备，从 `QMediaDevices::audioOutputs()` 获取 `QAudioDevice` 后传入构造函数或 `setDevice()`。

## 3. 生命周期、设备和异步边界

### 3.1 所有权

`QAudioOutput` 是 `QObject`，不可复制。将它作为播放器、控制器或窗口的子对象可自动管理生命周期。销毁对象会释放平台输出资源，并由 `QMediaPlayer` 或 `QMediaCaptureSession` 解除关联。

一个输出对象通常只服务于一个媒体对象。多个播放器需要独立控制音量或设备时，分别创建输出对象更清晰。

### 3.2 设备选择和热插拔

`device` 属性可使用 `QMediaDevices::audioOutputs()` 列表中的设备。传入默认构造的 `QAudioDevice` 表示系统默认输出。

蓝牙耳机、USB 声卡和 HDMI 设备可能在运行中出现或消失。设备列表改变时，应重新读取输出列表并确认当前设备仍然有效。切换输出设备不会改变媒体源本身，但播放器可能经历短暂重连或后端状态变化。

### 3.3 WebAssembly 和权限

在 WebAssembly 中，音频输出设备枚举是异步的。应等待 `QMediaDevices::audioOutputsChanged()` 后再填充设备选择 UI。浏览器权限和安全 HTTPS 上下文同样适用。

## 4. 属性语义

### 4.1 `device`

表示当前输出通道连接的物理音频设备。

- 可从 `QMediaDevices::audioOutputs()` 选择具体设备；
- 设置默认构造的 `QAudioDevice` 可回到系统默认输出；
- 它是设备描述，不是媒体播放器对象；
- 设备变更通过 `deviceChanged()` 通知。

### 4.2 `muted`

表示当前输出媒体流是否静音。静音只影响该 `QAudioOutput` 连接的媒体流，不会把系统主音量或其他应用静音。

它适合实现播放器的静音按钮。若需要恢复用户原先音量，通常应保留 `volume()`，而不是把音量直接改成零，因为静音与音量是两个不同状态。

### 4.3 `volume`

音量按线性值解释，范围 `0.0` 到 `1.0`，默认 `1.0`。超出范围的值会被钳制。该值只影响当前音频流，不修改系统全局音量。

听感上的响度不是线性的。UI 滑块通常应使用对数或 `QtAudio::convertVolume()` 转换，以免滑块前半段听起来几乎没有变化、后半段变化过于集中。

## 5. API 逐项说明

### 构造与析构

#### `QAudioOutput(QObject *parent = nullptr)`

创建输出通道并使用系统默认音频输出设备。`parent` 用于 QObject 父子对象管理。

#### `QAudioOutput(const QAudioDevice &device, QObject *parent = nullptr)`

创建输出通道并选择 `device` 描述的物理输出设备。传入默认构造的 `QAudioDevice` 表示系统默认输出。

#### `~QAudioOutput()`

销毁输出对象并释放平台资源。若播放器仍在使用它，应先停止或替换播放器的音频输出连接。

### Getter

#### `QAudioDevice device() const`

返回当前输出设备描述。它不是 `QIODevice`，也不能直接用于写入原始音频。

#### `float volume() const`

返回当前输出流音量，范围为 `[0.0, 1.0]`。

#### `bool isMuted() const`

返回当前输出流是否静音。

### Setter 槽

#### `void setDevice(const QAudioDevice &device)`

切换输出设备。默认构造的 `QAudioDevice` 选择系统默认输出。设备不再存在时，后端可能回退或无法打开，应结合设备列表和播放器状态处理。

#### `void setVolume(float volume)`

设置当前媒体流音量。值按线性范围解释并钳制到 `[0.0, 1.0]`；不影响系统全局音量。

#### `void setMuted(bool muted)`

设置当前输出流的静音状态。它不会停止 `QMediaPlayer`，也不会清空播放位置。

### 信号

#### `void deviceChanged()`

通知输出设备发生变化。信号没有参数，槽中调用 `device()` 获取新值。

#### `void volumeChanged(float volume)`

通知流音量变为指定值。可用于同步滑块、数字显示或状态保存。

#### `void mutedChanged(bool muted)`

通知静音状态变化。参数表示新状态。

## 6. 常见误区

- 把 `QAudioOutput` 当成原始 PCM 输出接口：原始音频应使用 `QAudioSink`。
- 把 `setVolume()` 当成系统音量控制：它只影响当前媒体流。
- 用音量为零代替所有静音逻辑：这样会丢失用户原来的音量状态。
- 把设备列表当成永久不变：蓝牙、USB、HDMI 都可能热插拔。
- 在 WebAssembly 中同步读取完整输出设备列表：需要等待 `audioOutputsChanged()`。

## API 速查表

| 类别 | API | 语义 | 边界与注意 |
| --- | --- | --- | --- |
| 构造 | `QAudioOutput(QObject *parent = nullptr)` | 使用系统默认输出创建设备通道。 | `parent` 管理 QObject 生命周期。 |
| 构造 | `QAudioOutput(const QAudioDevice &device, QObject *parent = nullptr)` | 使用指定输出设备创建通道。 | 默认构造的 `QAudioDevice` 表示系统默认设备。 |
| 析构 | `~QAudioOutput()` | 释放平台音频输出资源。 | 先处理播放器或媒体会话的关联。 |
| Getter | `QAudioDevice device() const` | 返回当前输出设备描述。 | 不返回 PCM 写入句柄。 |
| Getter | `float volume() const` | 返回输出流线性音量。 | 范围 `[0, 1]`。 |
| Getter | `bool isMuted() const` | 查询当前输出流是否静音。 | 不影响系统其他应用。 |
| 槽 | `void setDevice(const QAudioDevice &device)` | 切换物理输出设备。 | 设备可能热插拔或暂时不可用。 |
| 槽 | `void setVolume(float volume)` | 设置当前流音量。 | 越界钳制；不改变全局音量。 |
| 槽 | `void setMuted(bool muted)` | 静音或恢复当前流。 | 不停止播放、不改变播放位置。 |
| 信号 | `void deviceChanged()` | 通知设备选择变化。 | 无参数，槽中调用 `device()`。 |
| 信号 | `void volumeChanged(float volume)` | 通知音量变化。 | 参数是新的线性值。 |
| 信号 | `void mutedChanged(bool muted)` | 通知静音状态变化。 | 参数是新的布尔值。 |
