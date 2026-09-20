# QAudioInput：在媒体采集会话中选择和控制音频输入

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QAudioInput>`  
> 所属模块：`Qt6::Multimedia`  
> 继承：`QObject`  
> 相关类型：`QAudioDevice`、`QMediaDevices`、`QMediaCaptureSession`

## 1. 它解决什么问题

`QAudioInput` 表示媒体采集会话中的一个“物理音频输入通道”。它不负责把 PCM 数据读进 `QIODevice`，也不负责编码或保存文件；它负责告诉 `QMediaCaptureSession` 应该使用哪个麦克风，以及控制这个输入通道是否静音、音量是多少。

典型用途是：

- 摄像头预览或录制时选择笔记本内置麦克风、USB 麦克风；
- 视频会议中切换输入设备、暂时静音；
- 在 `QMediaCaptureSession` 中把摄像头和麦克风组合成录制源；
- 在设备列表变化后，把当前输入切换到仍然可用的设备。

如果目标是直接采集原始 PCM 数据并由应用自行处理，应使用 `QAudioSource`。`QAudioInput` 更像是媒体会话的“音频输入配置对象”，通常与 `QMediaRecorder`、`QCamera` 和 `QMediaCaptureSession` 一起使用。

## 2. 实际使用场景与最小用法

```cmake
find_package(Qt6 REQUIRED COMPONENTS Multimedia)
target_link_libraries(mytarget PRIVATE Qt6::Multimedia)
```

```cpp
#include <QAudioInput>
#include <QMediaCaptureSession>
#include <QMediaDevices>

auto *audioInput = new QAudioInput(this);
auto *session = new QMediaCaptureSession(this);
session->setAudioInput(audioInput);

connect(audioInput, &QAudioInput::mutedChanged,
        this, [](bool muted) {
            qDebug() << "microphone muted:" << muted;
        });
```

默认构造使用系统默认音频输入。选择具体设备时，从 `QMediaDevices::audioInputs()` 获取一个 `QAudioDevice`，再传给构造函数或 `setDevice()`。

## 3. 生命周期、设备和异步边界

### 3.1 对象所有权

`QAudioInput` 是 `QObject`。将它作为 `QMediaCaptureSession` 或控制器的子对象，可以由父对象自动销毁。`QAudioInput` 不可复制，应用代码应保存指针或引用语义对象，不要尝试按值复制。

对象销毁会解除它与媒体会话的关联并释放平台侧音频输入资源。通常不需要手动释放其内部平台句柄。

### 3.2 设备选择

`device` 属性接受 `QAudioDevice`。传入从 `QMediaDevices::audioInputs()` 得到的设备可选择具体麦克风；传入默认构造的 `QAudioDevice` 表示回到系统默认输入。

设备描述是运行时快照。物理麦克风可能被拔出、禁用或权限改变，因此保存设备对象后，仍应在设备列表变化时重新检查。设备切换是否立即影响正在运行的录制流程，由后端和媒体会话决定；需要确定行为时，应在切换后检查会话或录制器状态。

### 3.3 WebAssembly 和权限

在 WebAssembly 中，音频设备枚举是异步的。应等待 `QMediaDevices::audioInputsChanged()`，不要假定应用启动后同步就能得到完整设备列表。浏览器还要求用户授权，并且只能在安全的 HTTPS 上下文中工作。

桌面和移动平台也可能需要麦克风权限。权限请求属于应用启动/业务流程的一部分，不应把“创建 `QAudioInput` 成功”误认为“已经获准访问麦克风”。

## 4. 属性语义

### 4.1 `device`

表示当前输入通道连接的物理音频设备。

- 取值来自 `QMediaDevices::audioInputs()`，也可以是默认构造的 `QAudioDevice`；
- 默认构造的设备对象表示系统默认麦克风；
- 设备列表变化后，旧设备对象可能不再可用；
- 改变它只改变媒体会话使用的输入选择，不会把数据转换成另一种音频格式；
- 设备变化通过 `deviceChanged()` 通知。

### 4.2 `muted`

表示当前媒体输入是否静音。`true` 时输入通道被静音，`false` 时恢复输入。

静音是通道控制，不等于撤销麦克风权限，也不等于从 `QMediaCaptureSession` 移除音频输入。应用可用它实现会议软件的麦克风按钮，同时保留音频输入对象和录制链路。

### 4.3 `volume`

表示该输入通道的线性音量，范围是 `0.0` 到 `1.0`，默认值为 `1.0`。超出范围的值会被钳制。

这个音量是当前音频流的音量，不是系统全局麦克风音量。某些平台或设备不支持调整输入音量，此时设置可能没有实际效果；具体行为应以 getter 返回值和平台能力为准。

用户界面的音量滑块通常不应直接把百分比线性映射到听感。若要表现更自然的响度变化，可以使用 `QtAudio::convertVolume()` 在 UI 值和线性值之间转换。

## 5. API 逐项说明

### 构造与析构

#### `QAudioInput(QObject *parent = nullptr)`

创建一个音频输入通道，并使用系统默认输入设备。`parent` 用于 QObject 父子对象所有权管理。

#### `QAudioInput(const QAudioDevice &deviceInfo, QObject *parent = nullptr)`

创建一个音频输入通道，并连接到 `deviceInfo` 描述的设备。传入默认构造的 `QAudioDevice` 等价于选择系统默认输入。

#### `~QAudioInput()`

销毁输入通道并释放平台侧资源。若它仍被媒体会话使用，应先解除会话关系或让会话在对象销毁时同步处理关联。

### Getter

#### `QAudioDevice device() const`

返回当前连接的输入设备描述。它返回的是设备描述值，不是可直接读 PCM 的句柄。

#### `float volume() const`

返回当前输入流音量，正常范围为 `[0.0, 1.0]`。不支持输入音量控制的设备通常返回 `1.0`。

#### `bool isMuted() const`

返回当前输入是否静音。

### Setter 槽

#### `void setDevice(const QAudioDevice &device)`

切换当前输入设备。传入默认构造的 `QAudioDevice` 选择系统默认设备。建议只从当前 `QMediaDevices::audioInputs()` 列表中选择设备，并在设备列表变化后重新验证。

#### `void setVolume(float volume)`

设置当前输入通道音量。值按 `0.0` 到 `1.0` 线性解释并钳制到该范围；它不修改系统全局音量。平台不支持时，设置可能被忽略。

#### `void setMuted(bool muted)`

设置输入通道的静音状态。它适合会议中的临时静音，不会释放输入设备，也不会撤销权限。

### 信号

#### `void deviceChanged()`

当前输入设备发生变化时发出。信号不携带新设备参数，需要在槽中调用 `device()` 读取最新值。

#### `void volumeChanged(float volume)`

输入音量变化时发出，参数是变化后的线性音量值。除了应用主动设置外，平台设备控制面板或后端也可能触发变化。

#### `void mutedChanged(bool muted)`

静音状态变化时发出，参数表示变化后的状态。更新 UI 时应直接使用该参数，而不是假定调用 `setMuted()` 一定成功。

## 6. 常见误区

- 把 `QAudioInput` 和 `QAudioSource` 混用：前者配置媒体会话输入，后者才提供原始音频读取接口。
- 把 `volume` 当成系统全局音量：它只作用于当前输入流。
- 创建对象后立即枚举并使用浏览器麦克风：WebAssembly 需要等待异步设备列表和权限。
- 设备拔出后继续使用旧 `QAudioDevice`：应响应 `QMediaDevices::audioInputsChanged()` 并重新选择。
- 只连接 `mutedChanged` 而不保存当前状态：初始化 UI 时仍应先读取 `isMuted()`。

## API 速查表

| 类别 | API | 语义 | 边界与注意 |
| --- | --- | --- | --- |
| 构造 | `QAudioInput(QObject *parent = nullptr)` | 使用系统默认输入创建设备通道。 | `parent` 管理 QObject 生命周期。 |
| 构造 | `QAudioInput(const QAudioDevice &deviceInfo, QObject *parent = nullptr)` | 使用指定输入设备创建通道。 | 默认构造的 `QAudioDevice` 表示系统默认设备。 |
| 析构 | `~QAudioInput()` | 释放平台音频输入资源。 | 不可复制；注意媒体会话中的关联。 |
| Getter | `QAudioDevice device() const` | 返回当前输入设备描述。 | 不返回 PCM 读取句柄。 |
| Getter | `float volume() const` | 返回输入流线性音量。 | 范围 `[0, 1]`；不支持硬件控制时通常为 `1`。 |
| Getter | `bool isMuted() const` | 查询输入是否静音。 | 静音不等于移除设备或撤销权限。 |
| 槽 | `void setDevice(const QAudioDevice &device)` | 切换输入设备。 | 设备可能已拔出；配合设备列表变化重新验证。 |
| 槽 | `void setVolume(float volume)` | 设置输入流音量。 | 越界钳制；不改变系统全局音量。 |
| 槽 | `void setMuted(bool muted)` | 设置通道静音。 | 适合临时静音，仍保留采集链路。 |
| 信号 | `void deviceChanged()` | 通知设备选择变化。 | 无参数，槽中调用 `device()`。 |
| 信号 | `void volumeChanged(float volume)` | 通知输入音量变化。 | 参数是变化后的线性值。 |
| 信号 | `void mutedChanged(bool muted)` | 通知静音状态变化。 | 参数是变化后的布尔值。 |
