# QGraphicsVideoItem
> Qt 6.11.1 · Qt Multimedia · 来自 `QGraphicsVideoItem`

## 作用定位

`QGraphicsVideoItem` 是 Graphics View 框架中的视频显示项。它让视频画面作为 `QGraphicsItem` 进入场景，可参与 Graphics View 的变换、层级和布局。

## 类说明

- 头文件：`#include <QGraphicsVideoItem>`
- CMake：链接 `Qt6::MultimediaWidgets`
- 继承：`QGraphicsObject`

## API 速查

| API | 说明 |
| --- | --- |
| `videoSink()` | 获取底层视频帧接收器。 |
| `setSize()` / `size()` | 设置显示尺寸。 |
| `nativeSize()` | 视频原始尺寸。 |
| `aspectRatioMode` | 控制缩放比例策略。 |
| `nativeSizeChanged()` | 原始尺寸变化。 |

## 使用场景
- 旧项目使用 QGraphicsScene/QGraphicsView，需要嵌入视频。
- 视频画面要参与场景变换、叠加其他 graphics item。
- 快速把播放器输出接到 Graphics View。

## 常见坑与经验
- 新 UI 通常优先考虑 Qt Quick 或普通 `QVideoWidget`；Graphics View 视频更多是兼容旧架构。
- 复杂场景叠加和高分辨率视频可能有性能压力。
- 播放控制仍由 `QMediaPlayer`，item 只是显示端。

## 知识点覆盖

- Graphics View 视频显示
- 原始尺寸和缩放策略
- `QGraphicsVideoItem` 与 `QVideoSink`
