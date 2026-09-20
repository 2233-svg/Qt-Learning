# Qt Multimedia（下）：采集、录制、帧处理与可靠性

> 本篇承接媒体播放基础，重点是“采集会话”这条生产链路：设备输入进入 `QMediaCaptureSession`，再连接预览、图片捕获或媒体录制器。最后讨论权限、编码能力、背压和错误恢复。

## 1. 采集会话的总体结构

```text
QCamera / QAudioInput / QScreenCapture
                 |
       QMediaCaptureSession
          |       |       |
    QVideoWidget  QImageCapture  QMediaRecorder
```

同一个会话可以连接多个输出，但每个输出的资源消耗不同。预览、编码和逐帧分析同时运行时，应评估 CPU、GPU、内存和设备带宽。

## 2. 录音

### 2.1 最小录音链路

```cpp
#include <QAudioInput>
#include <QMediaCaptureSession>
#include <QMediaRecorder>

QMediaCaptureSession session;
QAudioInput audioInput;
QMediaRecorder recorder;

session.setAudioInput(&audioInput);
session.setRecorder(&recorder);
recorder.setOutputLocation(QUrl::fromLocalFile("recordings/sample.m4a"));
recorder.record();
```

调用 `record()` 后，录制状态通过 `recorderStateChanged` 反馈；停止使用 `stop()`，暂停使用 `pause()`（后端支持时）。输出位置应使用 `QUrl::fromLocalFile()`，避免把 Windows 路径误当成网络 URL。

### 2.2 编码和容器格式

```cpp
QMediaFormat format;
format.setFileFormat(QMediaFormat::MPEG4);
format.setAudioCodec(QMediaFormat::AudioCodec::AAC);
recorder.setMediaFormat(format);
recorder.setQuality(QMediaRecorder::HighQuality);
```

编码器和容器受平台后端影响。设置格式前可用 `QMediaFormat::supportedFileFormats()`、`supportedAudioCodecs()` 等 API 检查支持列表；不支持时回退到后端默认格式或提示用户。

## 3. 摄像头录像和图像捕获

### 3.1 录像

```cpp
QMediaCaptureSession session;
QCamera camera(QMediaDevices::defaultVideoInput());
QMediaRecorder recorder;

session.setCamera(&camera);
session.setRecorder(&recorder);
recorder.setOutputLocation(QUrl::fromLocalFile("videos/clip.mp4"));
camera.start();
recorder.record();
```

录像前应确认摄像头设备有效、权限已授予、输出目录可写。摄像头停止时，录制器可能自动结束或进入错误状态，业务层必须监听并关闭文件句柄。

### 3.2 捕获静态图片

```cpp
#include <QImageCapture>

QImageCapture imageCapture;
session.setImageCapture(&imageCapture);

QObject::connect(&imageCapture, &QImageCapture::imageSaved,
                 [](int id, const QString &fileName) {
    qDebug() << "saved" << id << fileName;
});

imageCapture.setFileFormat(QImageCapture::Jpeg);
imageCapture.captureToFile(QStringLiteral("photos/photo.jpg"));
```

`capture()` 请求由后端决定保存位置；`captureToFile()` 指定文件名。图像捕获是异步的，使用 `imageCaptured` 获取内存图像或 `imageSaved` 确认文件已落盘。不要把 `captureToFile()` 的返回 ID 当作文件已写完。

## 4. QML CaptureSession

```qml
import QtMultimedia

CaptureSession {
    camera: Camera {
        cameraDevice: MediaDevices.defaultVideoInput
    }
    videoOutput: VideoOutput {
        anchors.fill: parent
    }
    imageCapture: ImageCapture { }
}
```

录制时增加 `MediaRecorder`：

```qml
MediaRecorder {
    id: recorder
    mediaFormat.fileFormat: MediaFormat.MPEG4
    onErrorOccurred: console.warn(errorString)
}
```

QML 中的 `CaptureSession`、`Camera`、`ImageCapture` 和 `MediaRecorder` 与 C++ 类一一对应，属性绑定适合将权限、设备状态和按钮启用状态连接起来。

## 5. 摄像头能力和设置

### 5.1 设备与格式

```cpp
const QCameraDevice device = QMediaDevices::defaultVideoInput();
for (const QCameraFormat &format : device.videoFormats()) {
    qDebug() << format.resolution()
             << format.minFrameRate() << format.maxFrameRate()
             << format.pixelFormat();
}
```

选择格式时综合分辨率、帧率和像素格式。高分辨率不一定更好：编码、预览和分析的总成本可能超过设备能力。

```cpp
QCamera camera(device);
if (!device.videoFormats().isEmpty())
    camera.setCameraFormat(device.videoFormats().first());
```

### 5.2 对焦、曝光和缩放

`QCamera` 可设置 `FocusMode`、曝光模式、白平衡、手电筒和缩放。先检查设备是否支持对应功能，再设置；不支持时 API 可能忽略请求或发出错误。

```cpp
if (camera.minimumZoomFactor() < camera.maximumZoomFactor())
    camera.setZoomFactor(2.0);
```

连续滑块值应限制在 `minimumZoomFactor()` 和 `maximumZoomFactor()` 之间。自动对焦和曝光通常是异步的，UI 应显示正在调整而不是立即假设成功。

## 6. 原始视频帧处理

### 6.1 QVideoSink

```cpp
QVideoSink sink;
session.setVideoOutput(&sink);

QObject::connect(&sink, &QVideoSink::videoFrameChanged,
                 [&](const QVideoFrame &frame) {
    if (!frame.isValid())
        return;
    QVideoFrame copy = frame;
    if (copy.map(QVideoFrame::ReadOnly)) {
        const QSize size = copy.size();
        // 只提取必要数据，避免长期持有映射
        copy.unmap();
        qDebug() << size;
    }
});
```

`map()` 成功后才能访问平面数据；无论处理是否成功都要 `unmap()`。帧到达速度可能高于分析速度，应使用丢帧策略、环形缓冲或工作线程，而不是无限排队。

### 6.2 QVideoFrameInput

在需要把自定义视频帧送入录制器或输出时，可以使用 `QVideoFrameInput`：

```cpp
QVideoFrameInput frameInput;
session.setVideoFrameInput(&frameInput);

if (!frameInput.sendVideoFrame(frame)) {
    // 目标未准备好或队列已满，等待 readyToSendVideoFrame
}
```

发送失败不代表永久错误，可能只是下游背压。监听 `readyToSendVideoFrame` 后再尝试发送；生产者必须能够暂停或丢弃帧。

## 7. 原始音频缓冲

`QAudioBufferInput` 可把自定义音频缓冲送入 `QMediaRecorder`；`QAudioBufferOutput` 可从 `QMediaPlayer` 获取解码后的音频。与视频帧一样，必须处理队列容量和时钟同步。

```cpp
QAudioBufferInput input;
session.setAudioBufferInput(&input);
if (!input.sendAudioBuffer(buffer))
    qWarning() << "audio buffer rejected";
```

音频采样格式、采样率和声道数应与 `QAudioFormat` 匹配。跨设备混音时需要明确重采样和声道布局，不能只比较字节数。

## 8. 权限与隐私

摄像头和麦克风属于敏感设备。应用应遵循：

1. 在真正开始采集前请求权限；
2. 向用户说明用途；
3. 拒绝时显示降级路径；
4. 不使用时停止设备并释放会话；
5. 不把原始帧或录音写入不受控日志。

桌面平台可能由系统设置统一管理权限；移动平台需要应用清单和运行时请求。权限状态变化要驱动 UI，而不是只在启动时检查一次。

## 9. 状态机和错误恢复

建议把录制流程建模为：

```text
Idle -> Preparing -> Recording -> Stopping -> Finished
  |          |           |
  +------ Error <--------+
```

每个状态对应可用按钮和清理动作。收到 `errorOccurred` 时保存错误码、消息、设备 ID 和输出 URL；停止录制后等待 `recorderStateChanged` 进入 `StoppedState`，再允许开始下一次录制。

```cpp
QObject::connect(&recorder, &QMediaRecorder::errorOccurred,
                 [&](QMediaRecorder::Error error, const QString &message) {
    qWarning() << error << message;
    if (recorder.recorderState() != QMediaRecorder::StoppedState)
        recorder.stop();
});
```

不要在错误信号中递归调用 `record()`；先释放失败会话或切换到可验证的备用格式。

## 10. 时间戳和同步

音视频同步依赖后端时间戳。自定义帧输入时必须保持单调递增的时间基；把处理耗时误当作帧时间会导致音画漂移。录制暂停/恢复时，确认后端如何处理时间戳间隙，并在回放中验证。

## 11. 编解码与 FFmpeg 后端排查

Qt Multimedia 在部分平台使用 FFmpeg。遇到特定编码失败时，可以打开 Qt Multimedia 日志或 `QT_FFMPEG_DEBUG` 检查可用编解码器。日志只用于诊断，不应在生产环境默认开启，因为可能暴露文件路径和设备信息。

## 12. 常见问题

| 现象 | 原因 | 处理 |
| --- | --- | --- |
| 录音文件为 0 字节 | 未等待录制器完成或目录不可写 | 监听 stopped/error 并检查路径权限 |
| 图片 ID 返回但文件不存在 | 捕获是异步的 | 等 `imageSaved` 再使用文件 |
| 帧处理越来越延迟 | 下游处理速度低于输入 | 丢帧、限长队列或移到工作线程 |
| 自定义帧发送失败 | 队列满或录制未开始 | 等 `readyToSendVideoFrame` 并处理背压 |
| 设置分辨率无效 | 设备不支持该格式 | 枚举 `videoFormats()` 后选择能力范围内值 |
| 录制异常后无法再次开始 | 会话或 reply 状态未清理 | 等待 StoppedState，必要时重建对象 |
| 移动端无权限 | 清单或运行时请求缺失 | 完成平台配置并处理拒绝分支 |

## 13. 自测题

1. QMediaCaptureSession 在采集链路中扮演什么角色？
2. 为什么 `imageSaved` 比 `captureToFile()` 的返回值更适合确认文件完成？
3. QVideoFrameInput 返回 false 时应该立即报永久错误吗？
4. `QVideoFrame::map()` 和 `unmap()` 为什么必须成对出现？
5. 录制错误恢复时为什么不能直接在 error 信号里重新 record？

### 参考答案

1. 它把摄像头、音频输入等源连接到预览、图片捕获和录制器等输出。
2. 捕获请求是异步的，返回 ID 只表示请求已提交；`imageSaved` 才表示后端完成保存。
3. 不应，可能只是下游队列已满，应等待 ready 信号或执行丢帧策略。
4. map 建立 CPU 访问帧数据的映射，unmap 释放资源并让后端继续复用帧缓冲。
5. 失败会话可能仍处于 Preparing/Stopping 状态，直接重录会造成状态冲突和资源泄漏。

## 14. 小结

可靠的 Multimedia 采集程序需要同时关注四件事：设备能力、异步生命周期、数据背压和隐私权限。用 `QMediaCaptureSession` 组织链路，用状态机管理开始/停止/错误，用信号确认文件和帧的真实进度，再根据平台能力选择格式，才能把“能录”提升为可交付的录制功能。
