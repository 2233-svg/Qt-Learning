# QSoundEffect：低延迟播放短音效

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QSoundEffect>`  
> 所属模块：`Qt6::Multimedia`  
> 继承：`QObject`  
> 类型性质：可复用的短音效播放器

## 它解决什么问题

`QSoundEffect` 面向“用户动作发生后要立刻响一下”的音频，而不是通用媒体播放。它通常预加载未压缩的 WAV 音频，让按钮反馈、键盘声、提示音和游戏音效尽量降低启动延迟。

它和 `QMediaPlayer` 的分工不同：

| 需求 | 更适合的类 |
| --- | --- |
| 鼠标点击、键盘输入、命中、弹窗反馈 | `QSoundEffect` |
| 长音乐、视频伴音、网络流、多种封装格式 | `QMediaPlayer` |
| 原始 PCM 设备读写和自定义音频管线 | `QAudioSink` / `QAudioSource` |

低延迟的代价是资源占用更高，平台也可能限制同时播放的音效数量。

## 推荐的使用方式：长期复用对象

不要每次点击按钮都新建一个 `QSoundEffect`。正确方向是创建一次，提前设置来源，让加载和准备工作发生在用户动作之前：

```cpp
class SoundController : public QObject
{
public:
    explicit SoundController(QObject *parent = nullptr)
        : QObject(parent)
    {
        m_click.setSource(
                QUrl::fromLocalFile(":/sounds/click.wav"));
        m_click.setVolume(0.35f);
    }

    void playClick()
    {
        if (m_click.status() == QSoundEffect::Ready)
            m_click.play();
    }

private:
    QSoundEffect m_click;
};
```

加载是异步的。如果应用必须保证第一次触发也能播放，应监听 `loadedChanged` 或 `statusChanged`，在 `Ready` 后再允许触发，而不是把 `setSource()` 后立即视为已经准备好。

## source 和加载状态

`setSource()` 只设置 URL 并发起加载。源文件必须存在，应用还必须对指定目录有读取权限。空 URL 或无法读取的文件通常会让状态停留在 `Null` 或进入 `Error`。

状态含义：

- `Null`：没有设置源，或源为空；
- `Loading`：正在加载和准备音频；
- `Ready`：源已加载，可以播放；
- `Error`：加载或其它操作失败。

`isLoaded()` 表示加载是否完成，`status()` 则能区分成功和失败。工程上通常以 `status() == Ready` 作为可播放条件，并保留 `Error` 的日志信息。

`QSoundEffect` 主要针对 WAV 等未压缩音频。实际可用 MIME 类型由平台决定，可通过 `supportedMimeTypes()` 查询，不能凭文件扩展名猜测所有平台都支持。

## 循环次数的语义

`loopCount()` 是一次 `play()` 请求的总播放次数，`loopsRemaining()` 是当前播放尚未完成的次数。

边界很容易写错：

- `0` 或 `1` 都表示只播放一次；
- `QSoundEffect::Infinite` 的值是 `-2`，表示无限循环；
- 播放过程中修改 `loopCount` 会更新剩余循环；
- `stop()` 会立即停止，不会等待当前循环自然结束。

```cpp
effect.setLoopCount(QSoundEffect::Infinite);
effect.play();

// 后续某个时刻：
effect.setLoopCount(2); // 将当前播放改为有限次数的策略
```

如果业务需要“同一音效叠加播放多个实例”，不能通过一个对象简单地连续调用 `play()` 来获得任意数量的重叠声部；应按平台资源限制复用少量对象，或设计音效池。

## 音量、静音和音频设备

`volume` 是线性浮点值，范围为 `[0.0, 1.0]`，超出范围会被截断到边界。默认值为 `1.0`。它是振幅/音量控制的线性标尺，不一定符合用户对“响度”的线性感受。滑块常用 `QtAudio::convertVolume()` 做非线性换算。

`muted` 会静音当前播放，但不改变保存的 `volume`。取消静音后会恢复原音量：

```cpp
effect.setVolume(0.25f);
effect.setMuted(true);
// ...
effect.setMuted(false); // 恢复 0.25
```

可以通过构造函数或 `setAudioDevice()` 选择输出设备。设备是 `QAudioDevice` 值对象；设备拔出、系统默认设备变化和平台重路由仍可能影响实际输出，应用应监听 `audioDeviceChanged` 并在必要时重新选择。

## 播放控制和异步信号

`play()` 请求开始播放，`stop()` 停止当前播放。它们没有返回错误码，能否真正发声要结合 `status()`、`playing` 和平台音频状态判断。

常用信号：

- `loadedChanged`：加载完成状态变化；
- `statusChanged`：`Null`、`Loading`、`Ready`、`Error` 变化；
- `playingChanged`：是否正在播放变化；
- `loopsRemainingChanged`：剩余循环变化；
- `sourceChanged`、`volumeChanged`、`mutedChanged`：对应属性变化；
- `audioDeviceChanged`：输出设备变化。

这些信号只报告对象状态，不保证扬声器已经在物理上发出声音。系统静音、设备独占、平台音频焦点和硬件限制都可能影响最终听感。

## 格式、资源和平台限制

低延迟播放器会为快速播放保留更多资源，因此平台可能限制同时播放的 `QSoundEffect` 数量。短音效应尽量复用对象，避免在大量 UI 事件中创建和销毁对象。

Qt 文档建议音效使用单声道或立体声文件，采样率接近平台原生设备格式通常更容易获得稳定结果。若需要播放长音乐、复杂封装或网络资源，使用 `QMediaPlayer` 更合适。

## 常见误区

- 用 `QSoundEffect` 播放整首音乐或网络视频音轨；
- `setSource()` 后立刻假设音频已经加载完成；
- 把 `loopCount = 0` 理解成“不播放”；
- 忽略 `Infinite = -2` 的特殊值；
- 把 `volume` 直接当成用户感知响度；
- 每次点击都创建新对象，导致延迟和资源压力；
- 以为 `play()` 返回成功就一定能听到声音；
- 不查询平台支持的 MIME 类型；
- 在一个对象上追求大量同时重叠声部，忽略平台并发限制。

## API 速查表

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 枚举 | `enum Loop` | 定义循环特殊值。 | 目前公开值为 `Infinite`。 |
| 枚举值 | `Infinite = -2` | 让音效无限循环。 | 传给 `setLoopCount()`。 |
| 枚举 | `enum Status` | 表示音效加载和操作状态。 | 用于区分未加载、加载中、就绪和错误。 |
| 枚举值 | `Null` | 没有源或源为空。 | 不能据此播放。 |
| 枚举值 | `Loading` | 正在加载源。 | 监听 `statusChanged` 或 `loadedChanged`。 |
| 枚举值 | `Ready` | 源已经加载，可请求播放。 | 适合启用播放操作。 |
| 枚举值 | `Error` | 加载或操作发生错误。 | 记录源路径和平台信息。 |
| 构造 | `QSoundEffect(QObject *parent = nullptr)` | 创建使用默认音频设备的音效对象。 | 不自动加载源。 |
| 构造 | `QSoundEffect(const QAudioDevice &, QObject *parent = nullptr)` | 创建并指定输出设备。 | 设备变化后仍需处理重路由。 |
| 析构 | `~QSoundEffect() override` | 销毁音效对象。 | 会结束当前播放并释放准备资源。 |
| 静态查询 | `static QStringList supportedMimeTypes()` | 返回当前平台支持的音效 MIME 类型。 | 平台相关；不等于所有媒体格式。 |
| 源 | `QUrl source() const` | 返回当前音频源 URL。 | 只表示配置的 URL，不表示加载成功。 |
| 源 | `void setSource(const QUrl &url)` | 设置并异步加载音频源。 | 文件必须存在且可读。 |
| 循环 | `int loopCount() const` | 返回一次播放请求的总播放次数。 | `0` 和 `1` 都只播放一次。 |
| 循环 | `void setLoopCount(int loopCount)` | 设置播放次数。 | `Infinite` 表示无限循环；播放中修改会更新剩余次数。 |
| 循环 | `int loopsRemaining() const` | 返回当前尚未完成的循环次数。 | 无限循环时返回 `Infinite`。 |
| 设备 | `QAudioDevice audioDevice()` | 返回当前输出设备。 | 返回值对象，不拥有平台设备。 |
| 设备 | `void setAudioDevice(const QAudioDevice &device)` | 设置输出设备。 | 可能触发设备重建或状态变化。 |
| 音量 | `float volume() const` | 返回当前线性音量。 | 范围是 `[0, 1]`。 |
| 音量 | `void setVolume(float volume)` | 设置线性音量。 | 越界会 clamp；UI 宜使用非线性刻度。 |
| 静音 | `bool isMuted() const` | 查询是否静音。 | 静音不修改保存的音量值。 |
| 静音 | `void setMuted(bool muted)` | 设置静音状态。 | 取消静音后恢复原音量。 |
| 状态 | `bool isLoaded() const` | 查询源是否完成加载。 | 完成不一定代表播放设备可用。 |
| 状态 | `bool isPlaying() const` | 查询是否正在播放。 | 不代表扬声器一定已经发声。 |
| 状态 | `Status status() const` | 返回当前状态枚举。 | `Ready` 是最常用的可播放判断。 |
| 控制 | `void play()` | 开始按当前循环次数播放。 | 无返回错误码；监听状态信号。 |
| 控制 | `void stop()` | 停止当前播放。 | 不等待当前循环结束。 |
| 信号 | `void sourceChanged()` | 源 URL 变化时通知。 | 重新加载通常是异步的。 |
| 信号 | `void loopCountChanged()` | 总循环次数变化时通知。 | 播放中可能伴随剩余次数变化。 |
| 信号 | `void loopsRemainingChanged()` | 剩余循环变化时通知。 | 可用于更新 UI 或播放状态。 |
| 信号 | `void volumeChanged()` | 音量变化时通知。 | 读取 `volume()` 获取新值。 |
| 信号 | `void mutedChanged()` | 静音状态变化时通知。 | 读取 `isMuted()` 获取新值。 |
| 信号 | `void loadedChanged()` | 加载完成状态变化时通知。 | 还应读取 `status()` 判断是否成功。 |
| 信号 | `void playingChanged()` | 播放状态变化时通知。 | 适合更新播放按钮。 |
| 信号 | `void statusChanged()` | 状态枚举变化时通知。 | 处理 `Error` 和 `Ready`。 |
| 信号 | `void audioDeviceChanged()` | 输出设备变化时通知。 | 设备热插拔时重新检查路由。 |

## 一句话总结

`QSoundEffect` 是为短音效准备的低延迟播放器：提前加载、长期复用、按 `Ready` 状态播放，并用 `loopCount`、线性音量和平台设备限制来管理实际行为；长媒体播放应交给 `QMediaPlayer`。
