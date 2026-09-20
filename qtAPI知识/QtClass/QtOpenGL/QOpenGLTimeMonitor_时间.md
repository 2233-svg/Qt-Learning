# QOpenGLTimeMonitor 时间笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QOpenGLTimeMonitor>`  
> 所属模块：`Qt6::OpenGL`  
> 继承：`QObject`  
> 定位：用一组 OpenGL timer query 记录多个 GPU 时间采样点

## 它解决什么问题

`QOpenGLTimeMonitor` 是 `QOpenGLTimerQuery` 的多点封装。单个 timer query 适合测一个区间，而真实渲染帧通常由多个阶段组成：G-buffer、shadow、lighting、post-process、UI。这个类用一组 query 依次记录 GPU timestamp，然后帮你算出相邻采样点之间的时间间隔。

它解决的是“在一帧里测多个 GPU 区间”这个问题。你不需要手工管理多个 query id 和时间戳差值，只要设置采样点数量、依次 `recordSample()`，等结果可用后取 samples 或 intervals。

## 实际使用场景

- 给渲染帧打多个时间点，得到每个 pass 的 GPU 耗时；
- 开发性能 HUD，显示最近几帧的 shadow/lighting/post-process 时间；
- 根据 GPU 区间耗时动态调整分辨率、阴影质量或后处理开关；
- 对渲染算法改动做分段对比，而不是只看整帧时间。

## 使用模型

```cpp
#include <QOpenGLTimeMonitor>

void renderFrame(QOpenGLTimeMonitor &monitor)
{
    monitor.recordSample(); // frame/pass 0 start
    // draw shadow pass
    monitor.recordSample(); // shadow end, lighting start
    // draw lighting pass
    monitor.recordSample(); // lighting end

    if (monitor.isResultAvailable()) {
        const QList<GLuint64> intervals = monitor.waitForIntervals();
        monitor.reset();
    }
}
```

如果设置 `sampleCount` 为 3，会得到 3 个 GPU timestamp 和 2 个 interval。`setSampleCount()` 后要再调用 `create()` 才会按新的数量创建底层 timer query。

## 核心语义

### sample 和 interval 的关系

采样点是时间戳，区间是相邻时间戳的差。`N` 个 sample 只能产生 `N - 1` 个 interval。默认 sample count 是 2，也就是测一个区间。

### 结果读取会阻塞

`waitForSamples()` 和 `waitForIntervals()` 都会阻塞直到 GPU 结果可用。渲染循环中应先用 `isResultAvailable()` 判断，或者延迟几帧读取。

### 每轮使用后要 `reset()`

读取结果后、下一帧第一次 `recordSample()` 前，应调用 `reset()`。它会清掉缓存结果，并把内部索引回到第一个 query。

### 平台支持跟 timer query 一样

这个类依赖 OpenGL timer query。OpenGL 3.3+ 完整支持；OpenGL 3.2 加 `ARB_timer_query` 完整支持；只有 `EXT_timer_query` 的旧环境不能拿 GPU timestamp；OpenGL ES 2/3 不支持。

## API 速查表

| API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- |
| `QOpenGLTimeMonitor(QObject *parent = nullptr)` | 创建多点计时包装对象。 | 使用前设置 sample count 并 `create()`。 |
| `~QOpenGLTimeMonitor()` | 销毁对象和底层 query 资源。 | 资源清理依赖相关 OpenGL context。 |
| `setSampleCount(int sampleCount)` | 设置要记录的采样点数量。 | 至少为 2；设置后必须重新 `create()` 才生成 query 对象。 |
| `sampleCount() const` | 返回请求或实际可用的采样点数量。 | `create()` 成功后表示实际可用数量；默认是 2。 |
| `create()` | 创建 `sampleCount()` 个底层 timer query。 | 需要 current context 和 timer query 支持。 |
| `destroy()` | 销毁底层 query 对象。 | 清理时应让相关 context current。 |
| `isCreated() const` | 查询底层 query 是否已创建。 | `true` 后才能记录 sample。 |
| `objectIds() const` | 返回所有底层 OpenGL query id。 | 主要用于调试或与原生 API 配合。 |
| `recordSample()` | 在当前命令队列位置记录一个 GPU timestamp。 | 按调用顺序使用内部 query；返回当前采样索引。 |
| `isResultAvailable() const` | 查询所有结果是否可读。 | 非阻塞；建议读结果前先调用。 |
| `waitForSamples() const` | 等待并返回所有原始 GPU timestamp。 | 会阻塞；需要完整 timestamp 支持。 |
| `waitForIntervals() const` | 等待并返回相邻采样点之间的纳秒间隔。 | 会阻塞；返回数量比 sample 数少 1。 |
| `reset()` | 清理上一轮结果并重置内部采样索引。 | 每帧或每轮测量结束后、下一轮开始前调用。 |

## 常见误区

### 把 sampleCount 当成区间数量

`sampleCount = 4` 得到的是 4 个点、3 个区间。如果要测 4 个 pass，通常需要 5 个采样点。

### 忘记 reset

上一轮结果读取后不 `reset()`，下一轮记录会混用旧状态或索引位置，统计结果就不可信。

### 在同一帧立即等待结果

GPU 查询结果经常晚几帧才可用。立即 `waitForIntervals()` 会让 CPU 等 GPU，反而降低帧率。

## 一句话总结

`QOpenGLTimeMonitor` 是多段 GPU 性能计时器；它让一帧内多个渲染阶段的耗时统计更省心，但仍要异步读取并在每轮后重置。
