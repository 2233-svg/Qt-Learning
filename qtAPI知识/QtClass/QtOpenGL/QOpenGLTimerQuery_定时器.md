# QOpenGLTimerQuery 定时器笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QOpenGLTimerQuery>`  
> 所属模块：`Qt6::OpenGL`  
> 继承：`QObject`  
> 定位：包装单个 OpenGL timer query，用 GPU 时间测量渲染命令耗时

## 它解决什么问题

`QOpenGLTimerQuery` 用 OpenGL 的 timer query 对象测量 GPU 执行命令的时间。CPU 侧的 `QElapsedTimer` 只能测“提交命令花了多久”，而现代 GPU 是深度流水线执行的，提交快并不代表 GPU 工作快。timer query 让你得到 GPU 时间戳或某段命令在 GPU 上的耗时。

它适合做渲染性能分析、pass 级耗时统计、动态画质调节依据。它不适合做每帧同步等待，因为读取结果可能阻塞 CPU，破坏原本要测量的性能。

## 实际使用场景

- 测一个 shadow pass、post-process pass 或 draw batch 的 GPU 耗时；
- 记录 GPU 时间戳，和下一帧/后几帧结果配对分析；
- 开发性能 HUD 时异步查询最近可用结果；
- 判断某个渲染路径是否比另一个路径真的更省 GPU 时间。

## 使用模型

```cpp
#include <QOpenGLTimerQuery>

void drawMeasured(QOpenGLTimerQuery &query)
{
    if (!query.isCreated())
        query.create();

    query.begin();
    // issue OpenGL draw calls here
    query.end();

    if (query.isResultAvailable()) {
        const GLuint64 ns = query.waitForResult();
        // ns is GPU elapsed time in nanoseconds
    }
}
```

`create()` 需要当前线程有有效且支持 timer query 的 OpenGL context。OpenGL ES 2/3 不提供这些 timer query 支持；桌面 OpenGL 3.3+ 完整支持，OpenGL 3.2 加 `ARB_timer_query` 也完整支持，更老版本只有 `EXT_timer_query` 时不能查询 GPU timestamp。

## 核心语义

### GPU 时间不是 CPU 时间

timer query 测的是命令到达 GPU 后的执行时间或 GPU 时间戳。它不会告诉你 CPU 生成命令、驱动验证、资源上传或等待同步花了多久。完整性能分析通常要同时看 CPU 和 GPU。

### 结果不会立刻可用

GPU 可能在 CPU 后面排队执行，查询结果常常要晚 1 到 5 帧才可用。`waitForResult()` 和 `waitForTimestamp()` 会阻塞直到结果返回；实时渲染中通常先用 `isResultAvailable()` 检查。

### `begin()`/`end()` 不能嵌套或交错

OpenGL 不允许多个 elapsed-time timer query 嵌套或交错。简单测一个区间可以用 `begin()`/`end()`；复杂多段统计更适合使用多个 query 和 `recordTimestamp()`，或者直接用 `QOpenGLTimeMonitor`。

### 时间单位是纳秒

OpenGL 用 64 位整数表示时间，粒度为 1 ns。返回值是 `GLuint64`，适合表示实时渲染中的长短区间。

## API 速查表

| API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- |
| `QOpenGLTimerQuery(QObject *parent = nullptr)` | 创建 Qt 包装对象。 | 还没有底层 OpenGL query；使用前必须 `create()`。 |
| `~QOpenGLTimerQuery()` | 销毁对象和底层资源。 | 资源清理依赖相关 context；显式 `destroy()` 更可控。 |
| `create()` | 创建底层 OpenGL timer query。 | 需要 current context 且平台支持 query；OpenGL ES 不支持此类。 |
| `destroy()` | 销毁底层 OpenGL query。 | 调用时应让创建时的 context current。 |
| `isCreated() const` | 查询底层 query 是否已创建。 | `true` 还不代表结果可读，只代表可发起查询。 |
| `objectId() const` | 返回底层 OpenGL query id。 | 需要和原生 OpenGL API 配合时使用。 |
| `begin()` | 标记要测量区间的开始。 | 不能和其他 timer query 嵌套/交错；更复杂场景用 timestamp。 |
| `end()` | 标记测量区间结束。 | 与 `begin()` 配对；结果稍后才可用。 |
| `recordTimestamp()` | 在命令队列中插入 GPU 时间戳记录点。 | 非阻塞；后续用 availability/result API 读取。 |
| `isResultAvailable() const` | 非阻塞查询结果是否可读。 | 推荐先检查，避免 `wait*()` 卡住渲染线程。 |
| `waitForResult() const` | 等待并返回 elapsed-time query 结果。 | 会阻塞 CPU；返回纳秒。 |
| `waitForTimestamp() const` | 等待并返回 GPU timestamp。 | 需要完整 timer query 支持；会阻塞。 |

## 常见误区

### 每帧立即 `waitForResult()`

这会强迫 CPU 等 GPU，严重扭曲性能。更好的做法是保存几帧 query，等 `isResultAvailable()` 为真再读。

### 用一个 query 测多段嵌套 pass

`begin()`/`end()` 不能嵌套。要测多个区间，用多个 `QOpenGLTimerQuery` 或 `QOpenGLTimeMonitor`。

### 拿 CPU profiler 结果和 GPU timer 直接比较

二者测的是不同管线位置。CPU 提交耗时短、GPU 执行耗时长是很常见的现象。

## 一句话总结

`QOpenGLTimerQuery` 是单段 GPU 计时工具；它能告诉你渲染命令真正占用 GPU 多久，但读取结果要异步处理，避免为了测量而把管线卡住。
