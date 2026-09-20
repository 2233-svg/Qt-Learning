# QWindowCapture
> Qt 6.11.1 · Qt Multimedia · 来自 `QWindowCapture`

## 作用定位

`QWindowCapture` 捕获某个窗口内容并接入 Qt 多媒体管线。相比 `QScreenCapture`，它关注单个窗口，适合会议共享某应用窗口、窗口录制和局部内容采集。

## 类说明

- 头文件：`#include <QWindowCapture>`
- CMake：链接 `Qt6::Multimedia`
- 继承：`QObject`

## API 速查

| API | 说明 |
| --- | --- |
| `setWindow()` / `window()` | 设置要捕获的窗口。 |
| `start()` / `stop()` | 开始或停止捕获。 |
| `isActive()` | 是否正在捕获。 |
| `error()` / `errorString()` | 捕获错误。 |
| `capturableWindows()` | 获取可捕获窗口列表。 |
| `activeChanged()` / `errorOccurred()` | 状态和错误通知。 |

## 使用场景

| 场景 | 说明 |
| --- | --- |
| 会议共享 | 用户选择一个窗口共享。 |
| 应用窗口录制 | 只录目标程序，不录整个桌面。 |
| 自动化预览 | 把窗口内容送入视频处理管线。 |

## 常见坑与经验
- 可捕获窗口列表受平台、权限和窗口系统限制。
- 目标窗口关闭、最小化或被系统保护时，捕获可能停止或输出空帧。
- 捕获窗口不包含麦克风/系统声音，音频要单独接入 session。

## 知识点覆盖

- 单窗口捕获
- 可捕获窗口枚举
- 窗口系统权限差异
- 与录制/预览管线协作
