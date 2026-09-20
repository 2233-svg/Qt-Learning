# QSoundEffect
> Qt 6.11.1 · Qt Multimedia · 来自 `QSoundEffect`

## 作用定位

`QSoundEffect` 是短音效播放类，适合按钮声、提示音、游戏小音效。它通常把短 WAV 等资源预加载到内存，追求低延迟触发；长音乐、流媒体和复杂控制应使用 `QMediaPlayer`。

## 类说明

- 头文件：`#include <QSoundEffect>`
- CMake：链接 `Qt6::Multimedia`
- 继承：`QObject`

## API 速查

| API | 说明 |
| --- | --- |
| `setSource()` / `source()` | 设置音效资源 URL。 |
| `setAudioDevice()` / `audioDevice()` | 选择输出设备。 |
| `play()` / `stop()` | 播放或停止音效。 |
| `setLoopCount()` / `loopCount()` | 设置循环次数。 |
| `loopsRemaining()` | 剩余循环次数。 |
| `setVolume()` / `volume()` | 设置音量。 |
| `setMuted()` / `isMuted()` | 静音控制。 |
| `status()` | 加载、就绪、错误等状态。 |
| `isLoaded()` / `isPlaying()` | 是否已加载、是否正在播放。 |
| `supportedMimeTypes()` | 查询支持的音效 MIME 类型。 |

## 使用场景
- UI 点击音、通知音。
- 游戏中短促、频繁触发的效果音。
- 需要比 `QMediaPlayer` 更轻的音效播放。

## 常见坑与经验
- 不适合长音频或流式播放；长内容用 `QMediaPlayer`。
- 播放前等 `status()` 到 Ready，避免第一次触发延迟或失败。
- 同一个 `QSoundEffect` 同时重叠播放能力有限；需要叠音时可创建多个实例或做混音。
- 支持格式受后端影响，WAV/PCM 通常最稳。

## 知识点覆盖

- 短音效低延迟播放
- 预加载与状态
- 循环、音量、静音
- 与媒体播放器的边界
