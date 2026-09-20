# Qt QFutureSynchronizer 深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QFutureSynchronizer>`  
> 所属模块：`Qt6::Core`  
> 类型性质：模板 RAII 同步器  
> 相关类型：`QFuture`、`QFutureWatcher`、`QtConcurrent`

## 1. 它解决什么问题

`QFutureSynchronizer<T>` 管理一组 `QFuture<T>`，让调用方可以在作用域结束时自动等待这些异步任务完成。它的核心价值不是创建任务，而是把“这组任务必须在离开函数前收尾”表达成一个 C++ 对象生命周期约束。

它主要解决三类问题：

- 函数启动多个后台任务后，需要统一等待；
- 函数中途有多条返回路径，仍必须保证任务完成；
- 需要在等待前统一发出取消请求，再等待任务真正收尾。

它不是 `QFutureWatcher` 的替代品：

- `QFutureSynchronizer` 只做同步等待，没有信号、进度和 GUI 通知；
- `QFutureWatcher` 把单个 future 转成 QObject 信号；
- 一个 synchronizer 管理的是同一 `T` 类型的一组 future。

## 2. 实际使用场景

### 2.1 函数退出前等待多个后台任务

```cpp
void rebuildIndexes(const QStringList &files)
{
    QFutureSynchronizer<void> synchronizer;

    for (const QString &file : files) {
        synchronizer.addFuture(QtConcurrent::run([file] {
            rebuildOne(file);
        }));
    }

    // 这里的 return、异常或其他退出路径都会经过 synchronizer 析构。
}
```

析构函数会调用 `waitForFinished()`，因此函数返回前这些 future 都已经完成。

### 2.2 需要取消后再等待

```cpp
void stopAndJoin(QFuture<void> future)
{
    QFutureSynchronizer<void> synchronizer(future);
    synchronizer.setCancelOnWait(true);
}
```

作用域结束时，synchronizer 先取消所管理的 future，再等待它们结束。取消是否有效仍由 future 的生产者决定。

### 2.3 动态添加一组同类型任务

`addFuture()` 适合持续追加任务；`futures()` 可用于检查当前管理集合或把句柄交给其他协调逻辑。但返回的是 future 句柄列表，不是结果列表。

## 3. 构建与最小示例

类属于 Core；如果任务来自 Qt Concurrent，还要链接 Concurrent：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Core Concurrent)
target_link_libraries(mytarget PRIVATE Qt6::Core Qt6::Concurrent)
```

```cpp
#include <QFutureSynchronizer>
#include <QtConcurrentRun>

void runTwoJobs()
{
    QFutureSynchronizer<void> synchronizer;
    synchronizer.addFuture(QtConcurrent::run([] { stepA(); }));
    synchronizer.addFuture(QtConcurrent::run([] { stepB(); }));

    synchronizer.waitForFinished();
}
```

显式调用 `waitForFinished()` 后，析构时仍会再次等待，但此时通常已经没有实际等待成本。

## 4. 生命周期模型

### 4.1 synchronizer 持有的是句柄

`addFuture()` 把 `QFuture<T>` 句柄加入内部列表。它不取得任务的独占所有权，也不复制后台计算。原 future 仍可在其他地方使用，取消和完成状态通过共享底层状态同步。

### 4.2 析构会阻塞

和普通容器不同，`QFutureSynchronizer` 的析构不是轻量操作：

- 析构先调用 `waitForFinished()`；
- 默认只等待，不自动取消；
- 如果开启 `cancelOnWait`，析构会先取消再等待；
- 如果某个 future 永远不完成，析构也会一直阻塞。

因此不要把它作为 GUI 控件成员而不加考虑，也不要在持有互斥锁时让 synchronizer 析构，否则可能在析构等待期间造成死锁或长时间卡顿。

### 4.3 `clearFutures()` 不等于等待

`clearFutures()` 只清空内部保存的句柄。它不会主动等待，也不会调用 `cancel()`。清空后，如果没有其他句柄，future 句柄的析构也不会替你同步后台计算；任务是否继续由生产者状态决定。

如果目标是安全收尾，应先 `waitForFinished()`，再清空。

### 4.4 `setFuture()` 会先处理旧集合

`setFuture(future)` 的语义不是“把一个元素替换到列表末尾”，而是：

1. 调用 `waitForFinished()` 等待旧集合；
2. 清空旧集合；
3. 把新 future 作为唯一受管理对象加入。

如果启用了 `cancelOnWait`，第一步会先取消旧集合。因此在任务切换频繁的路径上，`setFuture()` 可能是阻塞操作。

## 5. 取消和等待的边界

### 5.1 等待的是“真正完成”

`waitForFinished()` 会对列表中的每个 future 调用 `QFuture::waitForFinished()`。即使某个 future 已经取消，只要底层计算仍在收尾，synchronizer 仍会等待它结束。

### 5.2 生产者可能不支持取消

`setCancelOnWait(true)` 只保证 synchronizer 在等待前调用每个 future 的 `cancel()`。它不能强制停止不支持取消的任务，例如普通 `QtConcurrent::run()` 任务可能仍会运行到函数返回。

### 5.3 空集合和重复等待

空 synchronizer 的 `waitForFinished()` 立即返回。已经等待完成后再次调用也安全；它会重新检查当前列表，只有仍有未完成 future 时才阻塞。

### 5.4 不适合做超时等待

类没有超时参数。需要超时、进度或可取消 UI 时，保留 future，使用 watcher、计时器和显式状态控制；不要把 synchronizer 当作带超时的 join。

## 6. 逐项 API 说明

### 构造和析构

#### `QFutureSynchronizer::QFutureSynchronizer()`

构造一个空 synchronizer，`cancelOnWait` 默认是 `false`，内部没有受管理的 future。

#### `[explicit] QFutureSynchronizer::QFutureSynchronizer(QFuture<T> future)`

构造 synchronizer，并立即把传入 future 加入管理列表。它等价于先默认构造，再调用 `addFuture()`。

参数按值传入，传入的只是共享 future 句柄，不会复制后台计算。

#### `QFutureSynchronizer::~QFutureSynchronizer()`

析构时调用 `waitForFinished()`，确保列表中的 future 已完成后才返回。析构可能阻塞；如果 `cancelOnWait()` 为 `true`，还会先请求取消。

该类禁用拷贝构造和拷贝赋值，避免两个 synchronizer 对同一管理列表产生不清晰的析构等待语义。

### 管理集合

#### `void QFutureSynchronizer::addFuture(QFuture<T> future)`

把 future 追加到管理列表。它不会等待、取消或替换已有 future，也不会去重。

如果传入的是已经完成的 future，加入操作本身通常立即返回；如果传入默认或无效 future，等待它不会产生一个有用的结果，但该句柄仍会被加入列表。

#### `void QFutureSynchronizer::setFuture(QFuture<T> future)`

把 future 设置为唯一受管理对象。调用前会先等待旧列表，然后清空旧列表，再添加新 future。因此它可能阻塞，且不是轻量 setter。

#### `QList<QFuture<T>> QFutureSynchronizer::futures() const`

返回当前管理的 future 句柄列表副本。列表元素仍共享原来的底层异步状态；修改返回列表不会修改 synchronizer 内部列表。

#### `void QFutureSynchronizer::clearFutures()`

移除所有管理句柄，不等待、不取消。需要在清空前保证任务结束时，显式调用 `waitForFinished()`。

### 等待策略

#### `void QFutureSynchronizer::setCancelOnWait(bool enabled)`

设置等待前是否先对所有管理的 future 调用 `cancel()`：

- `true`：`waitForFinished()` 先请求取消，再等待；
- `false`：只等待，不主动取消。

它只改变 synchronizer 的策略，不改变已经加入的 future 生产者能力。

#### `bool QFutureSynchronizer::cancelOnWait() const`

返回当前是否启用“等待前取消”。它不表示 future 当前是否已经取消，也不触发任何操作。

#### `void QFutureSynchronizer::waitForFinished()`

等待所有管理的 future 完成。若 `cancelOnWait()` 为 `true`，先逐个请求取消，再逐个等待。

调用会阻塞当前线程，没有超时参数。不要在 GUI 线程或持锁区域无条件调用。

## API 速查表
| API | 作用 | 关键边界 |
|---|---|---|
| `QFutureSynchronizer()` | 创建空同步器 | `cancelOnWait` 默认关闭 |
| `QFutureSynchronizer(future)` | 创建并加入一个 future | 等价于构造后 `addFuture()` |
| `~QFutureSynchronizer()` | 等待全部 future 后析构 | 会阻塞，不会默认取消 |
| `addFuture(future)` | 追加管理句柄 | 不等待、不取消、不去重 |
| `setFuture(future)` | 等待旧集合并替换为一个 future | 可能阻塞；旧集合先处理 |
| `futures()` | 返回句柄列表副本 | 不是结果列表，不改变内部集合 |
| `clearFutures()` | 清空管理列表 | 不等待、不取消 |
| `setCancelOnWait(enabled)` | 配置等待前是否取消 | 只发送取消请求 |
| `cancelOnWait()` | 查询取消策略 | 不查询 future 实际取消状态 |
| `waitForFinished()` | 等待所有 future 完成 | 无超时；可能长时间阻塞 |

## 8. 和相邻类型如何选择

- 只等待一个 future：直接调用 `future.waitForFinished()`。
- 多个 future 需要作用域收尾：使用 `QFutureSynchronizer<T>`。
- 需要 UI 进度和信号：使用 `QFutureWatcher<T>`。
- 需要在不阻塞的情况下串接异步步骤：使用 `QFuture::then()`。
- 需要超时或复杂取消策略：保留 future，自行组合 watcher、计时器和状态机。

## 9. 排查顺序

1. 析构卡住时，先查是否忘记了 synchronizer 会自动等待。
2. 开启 `cancelOnWait` 后任务仍占用线程，确认生产者是否支持取消。
3. `setFuture()` 卡住时，检查旧集合是否还有未完成任务；它会先等待旧任务。
4. `clearFutures()` 后任务仍在跑，确认是否误以为清空句柄等于取消。
5. GUI 无响应时，搜索析构、`setFuture()` 和 `waitForFinished()` 是否发生在主线程。
6. 需要进度或单项结果时，不要继续扩展 synchronizer，改用 `QFutureWatcher`。
