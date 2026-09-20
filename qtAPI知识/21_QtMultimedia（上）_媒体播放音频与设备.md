# Qt Multimedia（上）：媒体播放、音频与设备

> Qt Multimedia 将媒体源、解码器、输出设备和采集会话拆成可组合对象。掌握“播放器 + 输出”“设备枚举 + 能力选择”两条链路后，再处理录制、摄像头和原始帧会更自然。

## 1. 模块与基本链路

### 1.1 CMake 配置片段

```cmake
find_package(Qt6 REQUIRED COMPONENTS Core Multimedia MultimediaWidgets)
target_link_libraries(mytarget PRIVATE
    Qt6::Core
    Qt6::Multimedia
    Qt6::MultimediaWidgets
)
```

QML 项目通常链接 `Qt6::Multimedia`，Widgets 项目显示视频时额外使用 `Qt6::MultimediaWidgets`。

### 1.2 播放器和输出对象

`QMediaPlayer` 负责媒体加载、解码和播放状态；它本身不是音频设备。要听到声音，必须连接 `QAudioOutput`：

```cpp
#include <QAudioOutput>
#include <QMediaPlayer>
#include <QUrl>

QMediaPlayer player;
QAudioOutput audioOutput;

player.setAudioOutput(&audioOutput);
player.setSource(QUrl(QStringLiteral("qrc:/audio/notify.mp3")));
audioOutput.setVolume(0.8); // 0.0 到 1.0 的线性音量
player.play();
```

播放器的生命周期必须覆盖异步加载和播放过程。局部临时对象在函数返回后销毁，会导致“没有声音”或回调失效。

## 2. QMediaPlayer 的状态和信号

```cpp
QObject::connect(&player, &QMediaPlayer::mediaStatusChanged,
                 [](QMediaPlayer::MediaStatus status) {
    qDebug() << "media status" << status;
});

QObject::connect(&player, &QMediaPlayer::errorOccurred,
                 [](QMediaPlayer::Error error, const QString &message) {
    qWarning() << error << message;
});
```

常用属性和信号：

- `playbackStateChanged`：Stopped、Playing、Paused；
- `positionChanged`、`durationChanged`：进度条和总时长；
- `bufferProgressChanged`：网络媒体缓冲比例；
- `mediaStatusChanged`：加载、缓冲、结束和无媒体状态；
- `errorOccurred`：解码、网络或格式错误。

用户界面应根据状态启用/禁用按钮，并在错误时显示可理解的提示。不要把 `duration == 0` 单独当作失败，流媒体或尚未解析完成时它可能暂时为零。

## 3. 进度控制和播放策略

```cpp
QObject::connect(&player, &QMediaPlayer::positionChanged,
                 slider, &QSlider::setValue);
QObject::connect(slider, &QSlider::sliderMoved,
                 &player, &QMediaPlayer::setPosition);
```

拖动滑块时应暂时停止由 `positionChanged` 驱动的视觉更新，避免用户拖动和播放器回调互相抢值。设置位置是否精确取决于媒体格式和后端，界面应允许短暂等待。

循环播放可通过 `setLoops(QMediaPlayer::Infinite)` 或有限次数实现。结束信号到达后再更新 UI，不要在定时器中不断轮询播放器状态。

## 4. 播放视频

### 4.1 QVideoWidget

```cpp
#include <QVideoWidget>

QVideoWidget videoWidget;
player.setVideoOutput(&videoWidget);
videoWidget.resize(640, 360);
videoWidget.show();
```

`QVideoWidget` 用于 Widgets 界面显示视频；同一个播放器可以设置音频输出和视频输出。某些平台插件（例如 `eglfs`）不支持 QVideoWidget，嵌入式场景应评估 QML 或自定义渲染方案。

### 4.2 QVideoSink 获取原始帧

```cpp
QVideoSink sink;
player.setVideoSink(&sink);

QObject::connect(&sink, &QVideoSink::videoFrameChanged,
                 [](const QVideoFrame &frame) {
    if (!frame.isValid())
        return;
    // 需要像素数据时再 map，处理完及时 unmap
});
```

`QVideoSink` 逐帧发出 `videoFrameChanged`，适合二维码识别、分析和自定义渲染。不要在 GUI 线程中对每帧执行昂贵算法；必要时复制轻量数据后交给工作线程，并注意 `QVideoFrame` 映射和生命周期。

## 5. 设备发现：QMediaDevices

```cpp
#include <QMediaDevices>

const QList<QAudioDevice> outputs = QMediaDevices::audioOutputs();
for (const QAudioDevice &device : outputs)
    qDebug() << device.description() << device.id();

const QAudioDevice defaultOutput = QMediaDevices::defaultAudioOutput();
```

可发现的设备包括音频输入/输出和视频输入。默认设备可能在应用运行期间因用户插拔而改变，应监听 `audioOutputsChanged`、`audioInputsChanged`、`videoInputsChanged`。

```cpp
QObject::connect(&devices, &QMediaDevices::audioOutputsChanged,
                 [] { qDebug() << "音频设备列表已更新"; });
```

桌面系统中设备名称并不稳定，持久化时优先保存 `QAudioDevice::id()`，并在设备消失后回退到默认设备。

## 6. 选择音频设备和格式

```cpp
QAudioDevice device = QMediaDevices::defaultAudioOutput();
QAudioOutput output(device);
output.setVolume(0.6);
player.setAudioOutput(&output);
```

对低层音频 I/O，使用 `QAudioFormat` 检查采样率、声道数和采样格式是否支持：

```cpp
QAudioFormat format;
format.setSampleRate(48000);
format.setChannelCount(2);
format.setSampleFormat(QAudioFormat::Float);

if (!device.isFormatSupported(format))
    format = device.preferredFormat();
```

不要假设所有平台都支持固定格式。让设备提供 `preferredFormat()`，或在应用层加入明确的转换步骤。

## 7. QSoundEffect：低延迟短音效

```cpp
#include <QSoundEffect>

QSoundEffect effect;
effect.setSource(QUrl(QStringLiteral("qrc:/sounds/click.wav")));
effect.setVolume(0.4);
effect.play();
```

`QSoundEffect` 适合 WAV 格式的短促反馈音，目标是低延迟而不是复杂媒体播放。频繁创建对象会增加加载延迟，应复用已加载的音效实例；监听 `statusChanged` 确认资源已就绪。

## 8. QML 中的 MediaPlayer

```qml
import QtMultimedia

MediaPlayer {
    id: player
    source: "qrc:/audio/intro.mp3"
    audioOutput: AudioOutput {
        volume: 0.8
    }
    onErrorOccurred: console.warn(errorString)
}

Button {
    text: player.playbackState === MediaPlayer.PlayingState
          ? qsTr("暂停") : qsTr("播放")
    onClicked: player.playbackState === MediaPlayer.PlayingState
               ? player.pause() : player.play()
}
```

QML 属性绑定可直接把进度和状态连接到控件。视频播放时，为 `MediaPlayer` 设置 `VideoOutput {}` 并将其放入布局；不要在每次点击时重新创建播放器。

## 9. 摄像头预览的基本组成

```cpp
#include <QCamera>
#include <QMediaCaptureSession>
#include <QMediaDevices>
#include <QVideoWidget>

QMediaCaptureSession session;
const QCameraDevice cameraDevice = QMediaDevices::defaultVideoInput();
QCamera camera(cameraDevice);
QVideoWidget preview;

session.setCamera(&camera);
session.setVideoOutput(&preview);
camera.start();
```

启动前检查 `QMediaDevices::videoInputs()` 是否为空。设备可能在启动后断开，监听 `QCamera::errorOccurred` 并允许用户重新选择设备。

## 10. 权限、平台和部署

摄像头、麦克风和某些移动平台功能需要运行时权限。权限请求流程由平台决定，应用应在开始采集前给出用途说明，并在拒绝后提供降级功能。

媒体后端依赖平台插件和编解码器。Windows、Linux、Android、iOS 的可用格式不同；发布包必须包含对应 Qt Multimedia 插件和所需系统组件。遇到“文件存在但无法播放”，先检查后端日志、容器格式和编解码器，而不是只检查 URL。

## 11. 常见问题

| 现象 | 原因 | 处理 |
| --- | --- | --- |
| 播放无声 | 没有设置 QAudioOutput 或对象提前销毁 | 保持输出对象生命周期并检查音量 |
| 视频黑屏 | 未设置视频输出或后端不支持 | 设置 QVideoWidget/QVideoSink 并检查平台 |
| 设备列表为空 | 没有设备或权限未授予 | 检查设备、权限和平台日志 |
| 进度条跳动 | 拖动时仍被 positionChanged 覆盖 | 拖动期间暂停视觉同步 |
| 音效延迟大 | 每次播放都重新加载资源 | 复用 QSoundEffect 并预加载 WAV |
| 摄像头启动失败 | 默认设备不可用或被占用 | 枚举设备、处理错误并允许重试 |

## 12. 自测题

1. QMediaPlayer 为什么还需要 QAudioOutput？
2. QMediaDevices 的默认设备会不会永久不变？
3. QVideoSink 适合哪些场景？
4. QSoundEffect 与 QMediaPlayer 如何分工？
5. 摄像头预览至少需要哪几个对象连接起来？

### 参考答案

1. 播放器负责解码和播放状态，QAudioOutput 才代表音频输出通道和音量。
2. 不会，用户插拔或系统设置变化都可能使默认设备改变。
3. 逐帧处理、分析、识别或自定义渲染。
4. QSoundEffect 用于低延迟短 WAV 音效，QMediaPlayer 用于编码媒体和视频。
5. QMediaCaptureSession、QCamera 和视频输出（如 QVideoWidget 或 QVideoSink）。

## 13. 小结

Qt Multimedia 的基础思维是把“源、处理、输出”分开：播放器连接音频/视频输出，设备对象描述能力，捕获会话连接摄像头、麦克风和录制器。只要在运行时检查设备与后端能力、正确处理异步状态和生命周期，跨平台媒体功能就有稳定的基础。
