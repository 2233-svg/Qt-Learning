# QtConcurrent::QTaskBuilder
> Qt 6.11.1 · Qt Concurrent · 来自 `QtConcurrent::QTaskBuilder`

## 1. 先建立直觉

`QTaskBuilder` 是 `QtConcurrent::task()` 返回的任务装配器。它不负责“写并发算法”，而是把一个普通 callable 包装成可提交到 Qt 线程池的任务：选择线程池、传入参数、设定优先级，然后决定是拿到 `QFuture` 观察结果，还是只把任务丢出去执行。

它适合处理“我有一个明确函数，想把它异步跑起来”的场景；如果要做 map/filter/reduce 一类批处理，`QtConcurrent::mapped()`、`filtered()`、`run()` 等接口通常更直接。`QTaskBuilder` 的价值在于把任务配置拆成链式步骤，可读性比把所有参数塞进一个调用强。

## 2. 类说明

`QTaskBuilder<Task, Args...>` 是模板类，`Task` 是被执行的函数对象，`Args...` 是最终交给任务的实参类型。对象本身只是“待提交任务”的描述，真正的执行发生在 `spawn()` 之后。

| 对象 | 关系 |
| --- | --- |
| `QtConcurrent::task(callable)` | 创建 `QTaskBuilder` 的入口。 |
| `QThreadPool` | 决定任务交给哪个线程池排队执行。 |
| `QFuture<T>` | `spawn()` 返回的结果/状态句柄。 |
| `QFutureWatcher<T>` | 在 GUI 或 QObject 世界里接收任务完成、进度、结果信号。 |

## 3. API 速查

| API | 用来做什么 |
| --- | --- |
| `withArguments(Args &&...args)` | 给任务绑定实参。只应该调用一次；没有参数时不要调用它。 |
| `onThreadPool(QThreadPool &threadPool)` | 指定任务提交到哪个线程池，而不是使用全局线程池。 |
| `withPriority(int newPriority)` | 设置线程池队列优先级；影响排队顺序，不等于操作系统线程优先级。 |
| `spawn()` | 提交任务并返回 `QFuture<InvokeResultType>`，可观察完成、取消、结果。 |
| `spawn(QtConcurrent::FutureResult)` | 提交任务但不要求保存普通返回值，适合 fire-and-forget 工作。 |
| `InvokeResultType` | 任务调用表达式的返回类型，也就是 `QFuture` 里的结果类型。 |

## 4. 关键用法

```cpp
auto future = QtConcurrent::task(parseFile)
        .withArguments(fileName)
        .onThreadPool(workerPool)
        .withPriority(1)
        .spawn();
```

当任务要把结果送回界面，不要在任务线程直接操作 widget 或 QML 对象。更稳的方式是用 `QFutureWatcher` 连接 `finished()`，在接收者所属线程读取结果：

```cpp
auto *watcher = new QFutureWatcher<Result>(this);
connect(watcher, &QFutureWatcher<Result>::finished, this, [this, watcher] {
    showResult(watcher->result());
    watcher->deleteLater();
});
watcher->setFuture(QtConcurrent::task(loadResult).withArguments(path).spawn());
```

## 5. 使用场景

| 场景 | 为什么适合 |
| --- | --- |
| 后台解析文件、压缩图片、生成索引 | 输入明确，输出单一，天然是一个 callable。 |
| 插件或工具中给不同任务指定独立线程池 | `onThreadPool()` 能避免把全局线程池占满。 |
| 把“配置任务”和“提交任务”分开写 | 链式 API 让优先级、线程池、参数一眼可见。 |
| 临时 fire-and-forget 后台工作 | 可以提交无需直接返回给调用处的任务，但仍要设计好生命周期。 |

## 6. 常见坑与经验

`spawn()` 只是提交任务，不保证马上开始执行。线程池满了、优先级低、最大线程数受限时，任务会排队。

`withArguments()` 绑定的是任务执行时要使用的参数。跨线程后最怕悬空引用：传引用、指针、`QStringView`、外部 buffer 时，要确认被引用对象活得比任务久；不确定就传值或移动拥有数据的对象。

`QFuture` 不是“强制停止按钮”。取消能否生效，取决于任务代码是否检查取消状态，或者使用的 Qt Concurrent 算法是否支持取消。普通 lambda 里写死一个长循环，调用取消并不会自动中断 CPU 指令。

优先级只影响 `QThreadPool` 内部队列调度。它不会让已经运行的任务让出 CPU，也不应该拿来做实时音视频、低延迟输入这类硬实时保证。

## 7. 知识点覆盖

- `QtConcurrent::task()` 与 `QTaskBuilder` 的关系。
- `QThreadPool` 全局池和自定义池的取舍。
- `QFuture`/`QFutureWatcher` 的结果观察模型。
- C++ callable、lambda 捕获、移动语义和引用生命周期。
- GUI 线程边界：后台计算可以并发，界面对象不能随便跨线程改。
- 任务取消、排队、优先级和线程池容量之间的区别。
