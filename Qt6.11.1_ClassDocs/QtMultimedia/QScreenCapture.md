# QScreenCapture
> Qt 6.11.1 · Qt Multimedia · 来自 `QScreenCapture`

## 作用定位

`QScreenCapture` 是屏幕捕获输入源，用于把整个屏幕或显示器内容接入 `QMediaCaptureSession`，再预览或录制。它适合录屏、屏幕共享、监控类应用。

## 类说明

- 头文件：`#include <QScreenCapture>`
- CMake：链接 `Qt6::Multimedia`
- 继承：`QObject`

## API 速查

| API | 说明 |
| --- | --- |
| `setScreen()` / `screen()` | 选择要捕获的 `QScreen`。 |
| `start()` / `stop()` | 开始或停止捕获。 |
| `isActive()` | 是否正在捕获。 |
| `error()` / `errorString()` | 捕获错误。 |
| `activeChanged()` / `errorOccurred()` | 状态和错误通知。 |

## 使用场景
- 录制整个屏幕。
- 屏幕共享预览。
- 多屏系统选择指定显示器捕获。

## 常见坑与经验
- 屏幕捕获权限在 macOS、Wayland、移动/沙盒环境中特别关键。
- 捕获帧率和分辨率可能受系统限制，不能按普通摄像头格式完全控制。
- 和 recorder 组合时，音频要另外接 `QAudioInput` 或 buffer input。

## 知识点覆盖

- 屏幕捕获输入源
- 多屏选择
- 权限和平台后端差异
- 与录制器/预览输出协作
