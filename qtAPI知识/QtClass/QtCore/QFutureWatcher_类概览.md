# Qt QFutureWatcher 深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QFutureWatcher>`  
> 所属模块：`Qt6::Core`  
> 继承：`QObject`  
> 类型性质：把 `QFuture` 状态转成信号、槽和便捷查询的观察器  
> 相关类型：`QFuture`、`QPromise`、`QtConcurrent`

## 1. 它解决什么问题

`QFuture` 适合保存异步任务的状态和结果，但它本身不是 `QObject`，不能直接发出 Qt 信号。`QFutureWatcher<T>` 正好补上这一层：

- 观察一个 `QFuture<T>` 的启动、完成、取消和暂停；
- 接收进度范围、进度值和进度文本；
- 在结果索引就绪时收到 `resultReadyAt` 或 `resultsReadyAt`；
- 从 GUI 线程响应后台任务，而不需要轮询；
- 通过槽发出取消、暂停和恢复请求；
- 对尚未处理的结果信号设置上限，反向节流生产者。

它不是任务本身，也不是线程池。`setFuture()` 只把 watcher 连接到一个已有的 future 状态；真正执行计算的仍然是 `QtConcurrent`、`QPromise` 或其他生产者。

## 2. 实际使用场景

### 2.1 GUI 中显示进度并在完成后读取结果

```cpp
auto *watcher = new QFutureWatcher<QString>(this);

connect(watcher, &QFutureWatcher<QString>::progressRangeChanged,
        progressBar, &QProgressBar::setRange);
connect(watcher, &QFutureWatcher<QString>::progressValueChanged,
        progressBar, &QProgressBar::setValue);
connect(watcher, &QFutureWatcher<QString>::finished,
        this, [this, watcher] {
            resultLabel->setText(watcher->result());
            watcher->deleteLater();
        });

watcher->setFuture(startWork());
```

关键顺序是：先连接信号，再调用 `setFuture()`。如果 future 在 `setFuture()` 前已经运行甚至完成，watcher 会同步补发当前状态；连接晚了就可能错过这些初始通知。

### 2.2 多结果任务逐项更新界面

```cpp
connect(watcher, &QFutureWatcher<QImage>::resultReadyAt,
        this, [watcher](int index) {
            const QImage image = watcher->resultAt(index);
            consumeImage(index, image);
        });
```

`resultReadyAt(index)` 的索引可能乱序。界面要按原顺序展示时，应把索引放入模型，而不是按信号到达顺序直接追加。

### 2.3 取消或暂停用户发起的任务

```cpp
connect(cancelButton, &QPushButton::clicked,
        watcher, &QFutureWatcherBase::cancel);
connect(pauseButton, &QPushButton::clicked,
        watcher, &QFutureWatcherBase::suspend);
connect(resumeButton, &QPushButton::clicked,
        watcher, &QFutureWatcherBase::resume);
```

这些槽发送的是异步请求。`cancel()` 不保证后台代码立即停止，`suspend()` 也不保证调用返回时已经暂停；用 `canceled`、`finished`、`suspending` 和 `suspended` 区分不同阶段。

### 2.4 生产速度高于 UI 处理速度

图像解码、日志解析或批量网络结果可能很快地产生大量结果。可以设置：

```cpp
watcher->setPendingResultsLimit(32);
```

当尚未投递的 `resultReadyAt` / `resultsReadyAt` 信号超过限制时，计算会自动节流；信号被消费到限制以下后，计算继续。

## 3. 构建和最小示例

`QFutureWatcher` 属于 Core；若 future 来自 `QtConcurrent::run()`，还需要 Concurrent：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Core Concurrent)
target_link_libraries(mytarget PRIVATE Qt6::Core Qt6::Concurrent)
```

```cpp
#include <QFutureWatcher>
#include <QtConcurrentRun>

void Controller::start()
{
    auto *watcher = new QFutureWatcher<int>(this);

    connect(watcher, &QFutureWatcher<int>::finished,
            this, [watcher] {
                qDebug() << watcher->result();
            });

    const QFuture<int> future = QtConcurrent::run([] {
        return 42;
    });

    watcher->setFuture(future);
}
```

如果 `future` 已经完成，`setFuture()` 仍可能在调用过程中发出 `started`、结果、`finished` 等初始信号，所以连接必须位于它之前。

## 4. 生命周期和线程模型

### 4.1 watcher 不拥有计算

`QFutureWatcher` 保存的是一个 `QFuture<T>` 句柄。销毁 watcher 会断开它与 future 输出接口的连接，但不会替 future 取消任务，也不会等待任务结束。只要还有其他句柄或生产者保持状态，后台计算仍可继续。

如果对象销毁前必须确保任务结束，应显式：

```cpp
watcher->cancel();
watcher->waitForFinished();
```

但这会阻塞调用线程。更常见的做法是让 watcher 有合适的 QObject parent，并在 `finished` 或 `canceled` 后释放它。

### 4.2 `QObject` 线程归属决定信号接收环境

watcher 是 `QObject`，应在需要接收信号的线程创建或移动，并让该线程运行事件循环。后台生产者通过 watcher 的输出接口投递状态通知，信号槽的连接类型和 watcher、接收对象的线程归属仍然遵守 QObject 规则。

不要把 watcher 当成可以随意跨线程直接操作的普通值对象。跨线程控制优先使用信号连接到它的槽，或者把调用排入 watcher 所在线程。

文档将其函数标为 reentrant，表示不同对象可以并发使用；这不等于同一个 watcher 的所有成员都能被多个线程无同步地同时调用。

### 4.3 `setFuture()` 的同步补发

`setFuture()` 在绑定一个已经启动的 future 时，会把已知状态补发给监听者。文档给出的可能顺序是：

1. `started`
2. `progressRangeChanged`
3. `progressValueChanged`
4. `progressTextChanged`
5. 一次或多次 `resultsReadyAt`
6. 一次或多次 `resultReadyAt`
7. `suspending`
8. `suspended`
9. `canceled`
10. `finished`

不是每个信号都一定出现；结果信号可能重复覆盖已有结果，进度值和文本只补发最新状态。连接完成后再 `setFuture()`，才能接收到这批状态。

### 4.4 没有 future 时的初始状态

构造 watcher 后、调用 `setFuture()` 前：

- `isStarted()` 返回 `true`；
- `isCanceled()` 返回 `true`；
- `isFinished()` 返回 `true`；
- `isRunning()` 不表示有一个真实任务在运行；
- `future()` 返回默认的 empty/canceled future。

这些值是“没有被监视对象”的便捷初始语义，不应拿来判断某个实际计算已经成功完成。

## 5. 结果和信号的边界

### 5.1 `resultReadyAt` 可能乱序

多结果生产者可以先报告高索引结果。因此：

- 信号参数是结果索引，不是计数器；
- 不要假设下一个信号索引等于上一个加一；
- 需要顺序时使用索引填充模型；
- 收到信号后用 `resultAt(index)` 读取相应结果。

`resultAt()` 在结果尚未立即可用时会阻塞。正常情况下 `resultReadyAt` 代表对应结果已经可读，但任务取消、对象切换和跨线程事件处理会让业务代码仍应避免在持锁状态下取结果。

### 5.2 `resultsReadyAt` 表示一个结果区间

`resultsReadyAt(beginIndex, endIndex)` 一次通知一段已就绪结果。它适合批量处理，但不要把两个参数误解成“结果个数”和“最后一个索引”；它们都是结果索引边界。

### 5.3 进度信号可能被限频

`progressValueChanged` 为避免压满 GUI 事件循环会限频。监听者可能收不到生产者报告的每一个中间进度值，但最后一个达到最大值的进度更新会保证投递。

因此：

- 进度条不应依赖每一次回调做增量计算；
- 需要精确的业务事件时，使用独立结果或自定义信号；
- `progressTextChanged` 也只代表 watcher 投递到的文本状态，不是日志流。

### 5.4 取消会停止一组通知

`cancel()` 后，watcher 不再发送新的进度和结果就绪信号，包括：

- `progressValueChanged`
- `progressRangeChanged`
- `progressTextChanged`
- `resultReadyAt`
- `resultsReadyAt`

已经排队或已经在执行的工作仍可能存在；`canceled` 和最终 `finished` 用来收尾。需要等待彻底结束时调用 `waitForFinished()`。

## 6. 暂停状态机

`setSuspended(true)`、`suspend()` 发出暂停请求后，状态可能经历：

```text
运行
  -> suspending：已请求，仍有工作运行
  -> suspended：暂停真正生效
```

恢复后发出 `resumed`。注意：

- `suspending` 只说明请求已发出；
- `suspended` 才说明没有运行中的计算，之后不应再有 result/progress 信号；
- 暂停前已经启动的计算可能完成并交付信号；
- `QtConcurrent::run()` 返回的 future 不能暂停，`mappedReduced()` 等可以支持暂停的 future 才会响应；
- 对不支持暂停的生产者，调用槽不会凭空制造可暂停能力。

Qt 6.0 之前的 `paused` 信号和 paused 槽已弃用。新代码使用 `suspending`、`suspended` 和 suspended API。

## 7. `QFutureWatcher<void>`

`QFutureWatcher<void>` 被特化为不提供 `result()` 和 `resultAt()`。它仍然可以观察 `QFuture<T>`，适合只需要：

- 完成通知；
- 取消和暂停控制；
- 进度；
- 不读取实际结果的数据处理器。

如果需要结果，使用 `QFutureWatcher<T>`。不要为了减少一个模板参数而把值结果塞进 `QFutureWatcher<void>` 后再尝试读取。

## 8. 逐项 API 说明

### 构造和当前 future

#### `[explicit] QFutureWatcher::QFutureWatcher(QObject *parent = nullptr)`

构造 watcher 并设置 QObject 父对象。在调用 `setFuture()` 前，它处于“没有被监视 future”的初始状态。

#### `[virtual] QFutureWatcher::~QFutureWatcher()`

销毁 watcher 并断开 future 输出连接。不会自动取消或等待计算；需要同步结束时必须显式处理。

#### `QFuture<T> QFutureWatcher::future() const`

返回当前被监视的 future 句柄。返回值是一个共享句柄副本，不是独占所有权，也不是结果副本。

### 状态查询

#### `bool QFutureWatcher::isStarted() const`

返回被监视计算是否已经启动。没有设置 future 时按文档返回 `true`，所以它不能单独用来判断 watcher 是否已绑定任务。

#### `bool QFutureWatcher::isRunning() const`

返回被监视计算当前是否运行。暂停、完成和没有真实 future 时不应视为运行中。

#### `bool QFutureWatcher::isFinished() const`

返回计算是否完成。没有设置 future 时返回 `true`；取消请求发出后，只有实际收尾完成才算 finished。

#### `bool QFutureWatcher::isCanceled() const`

返回计算是否已取消，或者 watcher 当前没有设置 future。返回 `true` 不代表后台工作立即停止。

#### `[since 6.0] bool QFutureWatcher::isSuspending() const`

返回是否已请求暂停但尚未完全生效。此时仍可能收到暂停请求发出前已经在途的结果或进度。

#### `[since 6.0] bool QFutureWatcher::isSuspended() const`

返回暂停是否已经生效。生效后不应再期待新的结果就绪或进度报告。

### 进度查询

#### `int QFutureWatcher::progressMinimum() const`

返回当前进度下限。具体范围由 future 生产者报告，不要固定假设为 0。

#### `int QFutureWatcher::progressMaximum() const`

返回当前进度上限。达到上限通常是最后一次进度更新，但完成仍由 `finished` 或 `isFinished()` 表示。

#### `int QFutureWatcher::progressValue() const`

返回当前进度值。它是状态查询，不保证每一个生产者的中间进度都曾通过信号交付。

#### `QString QFutureWatcher::progressText() const`

返回可选文本进度。生产者没有报告文本时返回空字符串。

### 结果读取

#### `T QFutureWatcher::result() const`

返回被监视 future 的第一个结果，等价于 `resultAt(0)`。如果结果还不可用会阻塞。`QFutureWatcher<void>` 不提供此函数。

#### `T QFutureWatcher::resultAt(int index) const`

返回指定索引的结果。结果未就绪时会等待；多结果信号可能乱序，所以应使用信号给出的索引。

### 绑定和节流

#### `void QFutureWatcher::setFuture(const QFuture<T> &future)`

开始监视给定 future。若 future 已启动或已完成，会同步补发当前可用状态。必须先连接信号，再调用此函数。

如果传入与当前共享同一底层状态的 future，头文件实现会直接返回，不会重新绑定或重新播放一轮状态。若需要重新触发一轮 UI 初始化，先明确切换到另一个状态再绑定。

传入默认构造的 future 可以解除对原状态的监视，但不会自动取消原任务；原任务是否继续由其他句柄和生产者决定。

#### `void QFutureWatcher::setPendingResultsLimit(int limit)`

设置尚未投递的结果就绪信号数量上限。超过限制时，future 对应的计算会被自动节流；待积压信号下降后继续。

它控制的是 `resultReadyAt` / `resultsReadyAt` 的待处理通知，不是结果总数上限，也不是所有线程间消息的通用队列大小。

#### `void QFutureWatcher::waitForFinished()`

阻塞当前线程，直到被监视计算真正结束，包括已经取消但仍在收尾的计算。它不等价于发送取消，也不替代 `finished` 信号。

### 控制槽

#### `[slot] void QFutureWatcher::cancel()`

异步请求取消被监视的 future。当前已经可用的结果仍可能读取，但不会再有新的进度和结果就绪信号。生产者必须支持取消，调用才有实质效果。

#### `[slot, since 6.0] void QFutureWatcher::setSuspended(bool suspend)`

传入 `true` 请求暂停，传入 `false` 请求恢复。调用返回时可能仍处于 `isSuspending()`，要等 `suspended` 或 `resumed` 信号确认阶段。

#### `[slot, since 6.0] void QFutureWatcher::suspend()`

`setSuspended(true)` 的便捷槽。它只发出暂停请求，不保证立即停止已经运行的工作。

#### `[slot] void QFutureWatcher::resume()`

`setSuspended(false)` 的便捷槽。恢复后通过 `resumed` 信号通知。

#### `[slot, since 6.0] void QFutureWatcher::toggleSuspended()`

如果当前处于暂停请求中或已暂停则恢复，否则请求暂停。它适合绑定一个切换按钮，但复杂界面通常应直接使用 `setSuspended(bool)`，让按钮状态和业务状态明确对应。

#### `[deprecated since 6.0] void QFutureWatcher::setPaused(bool paused)`

旧暂停槽。使用 `setSuspended()`。

#### `[deprecated since 6.0] void QFutureWatcher::pause()`

旧暂停便捷槽。使用 `suspend()`。

#### `[deprecated since 6.0] void QFutureWatcher::togglePaused()`

旧暂停切换槽。使用 `toggleSuspended()`。

### 状态信号

#### `[signal] void QFutureWatcher::started()`

watcher 开始监视通过 `setFuture()` 设置的 future 时发出。它表示 watcher 已开始观察，不应单独解读成后台函数刚刚在某个线程启动。

#### `[signal] void QFutureWatcher::finished()`

被监视 future 完成时发出。取消的计算也会在最终收尾后发出 `finished`；需要区分取消状态时同时检查 `isCanceled()` 或连接 `canceled`。

#### `[signal] void QFutureWatcher::canceled()`

被监视 future 被取消时发出。它表示取消状态已报告，不等于所有底层代码已经立刻停止；最终收尾仍以 `finished` 为准。

#### `[signal, since 6.0] void QFutureWatcher::suspending()`

暂停请求被记录时发出。此时仍可能有运行中的工作，仍可能收到在途结果或进度信号。

#### `[signal, since 6.0] void QFutureWatcher::suspended()`

暂停真正生效、没有运行中的计算时发出。收到它后，不应再等待新的结果或进度报告，除非先恢复。

#### `[signal] void QFutureWatcher::resumed()`

被监视 future 从暂停状态恢复时发出。

### 结果信号

#### `[signal] void QFutureWatcher::resultReadyAt(int index)`

索引 `index` 的结果可用时发出。多个结果可以乱序报告；处理器应使用传入索引调用 `resultAt(index)`，不要依赖到达顺序。

#### `[signal] void QFutureWatcher::resultsReadyAt(int beginIndex, int endIndex)`

一段结果索引已经就绪时发出。适合批量读取对应索引范围；如果业务需要严格顺序或处理时间较长，应结合 `setPendingResultsLimit()` 控制积压。

### 进度信号

#### `[signal] void QFutureWatcher::progressRangeChanged(int minimum, int maximum)`

future 报告的进度范围发生变化时发出。范围是生产者语义，进度条应使用两个参数而不是固定写死范围。

#### `[signal] void QFutureWatcher::progressValueChanged(int progressValue)`

future 报告进度变化时发出。为避免压垮 GUI 事件循环，信号会限频，监听者可能错过中间值，但最大值对应的最后更新会交付。

#### `[signal] void QFutureWatcher::progressTextChanged(const QString &progressText)`

future 报告文本进度时发出。文本是可选信息，不应假设每个 future 都会发出，空字符串也可能是正常值。

## API 速查表
| API | 作用 | 关键边界 |
|---|---|---|
| `QFutureWatcher(parent)` | 创建 QObject 观察器 | 未设置 future 前状态是便捷初始值 |
| `~QFutureWatcher()` | 销毁观察器 | 断开观察，不取消、不等待 |
| `future()` | 返回当前 future 句柄 | 返回共享副本，不转移所有权 |
| `setFuture(future)` | 开始监视 future | 先连接信号；可能同步补发状态 |
| `isStarted()` | 查询是否启动 | 无 future 时也返回 true |
| `isRunning()` | 查询是否运行 | 不能替代完成和暂停状态判断 |
| `isFinished()` | 查询是否完成 | 无 future 时返回 true |
| `isCanceled()` | 查询是否取消 | 无 future 时也返回 true |
| `isSuspending()` | 查询暂停请求中 | Qt 6.0；仍可能有在途工作 |
| `isSuspended()` | 查询暂停已生效 | Qt 6.0 |
| `progressMinimum()` | 查询进度下限 | 由生产者定义 |
| `progressMaximum()` | 查询进度上限 | 不等于 finished |
| `progressValue()` | 查询当前进度 | 中间值可能被限频 |
| `progressText()` | 查询文本进度 | 可能为空 |
| `result()` | 读取第一个结果 | 未就绪会阻塞；`void` 无此 API |
| `resultAt(i)` | 读取指定结果 | 未就绪会阻塞 |
| `setPendingResultsLimit(n)` | 限制待处理结果信号 | 只节流结果信号，不限制结果总数 |
| `waitForFinished()` | 阻塞等待真正结束 | 包括取消后的收尾 |
| `cancel()` | 请求取消 | 异步；生产者可能不支持 |
| `setSuspended(bool)` | 请求暂停/恢复 | Qt 6.0；请求与生效分离 |
| `suspend()` | 请求暂停 | Qt 6.0 |
| `resume()` | 请求恢复 | 通过 `resumed` 确认 |
| `toggleSuspended()` | 切换暂停状态 | Qt 6.0 |
| `started()` | watcher 开始监视 | 可能是 `setFuture()` 的同步补发 |
| `finished()` | future 真正完成 | 取消任务也会最终发出 |
| `canceled()` | future 被取消 | 不等于后台线程立刻停止 |
| `suspending()` | 已请求暂停 | 仍可能有在途信号 |
| `suspended()` | 暂停已生效 | 之后不应有新结果/进度信号 |
| `resumed()` | 恢复完成 | 表示从暂停恢复 |
| `resultReadyAt(i)` | 某索引结果就绪 | 索引可能乱序 |
| `resultsReadyAt(a, b)` | 一段结果就绪 | 参数是索引边界 |
| `progressRangeChanged(a, b)` | 进度范围变化 | 使用动态范围 |
| `progressValueChanged(v)` | 进度变化 | 会限频，最大值更新保证交付 |
| `progressTextChanged(text)` | 文本进度变化 | 文本可选 |

## 10. 版本迁移提示

- Qt 6.0：`setSuspended()`、`suspend()`、`isSuspending()`、`isSuspended()`、`suspending()`、`suspended()`、`toggleSuspended()` 可用；paused API 开始弃用。
- Qt 6.1 及以后：`QFuture` 的 context continuation 与错误/取消处理器可用于把回调安排到指定 QObject 线程；watcher 的核心 API不依赖这一版本点。
- Qt 6.10：`QFuture::cancelChain()` 新增，但 `QFutureWatcher` 没有对应的整链取消槽；需要从链的 future 上调用。
- 迁移旧代码时，不能把 `paused` / `pause()` 机械替换成“调用后立即停止”；应改成观察 `suspending` 和 `suspended` 两个阶段。

## 11. 常见误区和排查顺序

1. 信号没有收到：检查是否先连接再调用 `setFuture()`，以及 watcher 所在线程是否有事件循环。
2. `finished` 已收到但界面没有结果：检查 `QFuture<T>` 是否真的有值，`QFutureWatcher<void>` 不提供结果 API。
3. `resultReadyAt` 顺序不对：这是允许的，按信号索引写入模型。
4. 取消后任务仍占 CPU：确认生产者是否支持取消，再等待 `finished`；watcher 不能强杀任意线程。
5. 暂停后仍收到几个结果：区分 `suspending` 与 `suspended`，这些结果可能在暂停请求前已经开始计算。
6. 进度条跳跃：`progressValueChanged` 会限频，不能当作每一步的完整日志。
7. 结果处理拖慢生产者：设置 `setPendingResultsLimit()`，并缩短槽处理时间或把重活转移出去。
8. 销毁 watcher 后后台仍在跑：这是正常的观察器语义；需要停止任务时显式取消并等待，或保持 future 句柄直到收尾。
