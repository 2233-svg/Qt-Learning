# QCameraDevice
> Qt 6.11.1 · Qt Multimedia · 来自 `QCameraDevice`

## 作用定位

`QCameraDevice` 描述一个摄像头设备，包括设备 ID、描述、位置、是否默认、支持的拍摄格式和照片分辨率。它是 `QMediaDevices::videoInputs()` 返回的值对象。

## 类说明

- 头文件：`#include <QCameraDevice>`
- CMake：链接 `Qt6::Multimedia`
- 继承：无公开 QObject 继承，值类型

## API 速查

| API | 说明 |
| --- | --- |
| `id()` | 设备标识。 |
| `description()` | 显示名称。 |
| `isDefault()` | 是否默认摄像头。 |
| `position()` | 前置、后置或未指定。 |
| `videoFormats()` | 支持的视频格式列表。 |
| `photoResolutions()` | 支持的照片分辨率。 |

## 使用场景

- 枚举摄像头并提供选择 UI。
- 在移动端区分前置/后置摄像头。
- 选择合适分辨率、帧率和像素格式。

## 常见坑与经验

- 设备 ID 不保证永久稳定，保存偏好时要有 fallback。
- 设备支持的录像格式和照片分辨率不一定一致。
- 选择最高分辨率可能导致帧率低、启动慢、发热高。

## 知识点覆盖

- 摄像头设备枚举
- 前后摄像头位置
- 视频格式和照片分辨率
- 设备选择策略
