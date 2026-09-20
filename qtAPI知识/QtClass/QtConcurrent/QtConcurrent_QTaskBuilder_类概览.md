# QtConcurrent::QTaskBuilder 深入笔记：配置异步任务，再显式提交执行

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QTaskBuilder>`  
> 常用入口：`#include <QtConcurrentTask>`  
> 所属模块：`Qt6::Concurrent`  
> 自 Qt 6.0 起提供

`QtConcurrent::QTaskBuilder` 是 `QtConcurrent::task(...)` 返回的临时配置对象。它解决的不是“怎么写线程函数”，而是“一个任务提交给线程池前，怎样连续指定参数、线程池和优先级，并明确选择是否需要 `QFuture` 结果”。

它采用 fluent interface（链式配置）：

```text
QtConcurrent::task(callable)
    .withArguments(...)
    .onThreadPool(pool)
    .withPriority(priority)
    .spawn();
```

真正把任务提交出去的是最后的 `spawn()`。在这之前，builder 只是在保存任务和启动参数。

## 1. 最小可用代码

```cmake
find_package(Qt6 REQUIRED COMPONENTS Concurrent)
target_link_libraries(mytarget PRIVATE Qt6::Concurrent)
```

```cpp
#include <QtConcurrentTask>
#include <QFuture>
#include <QString>

auto future = QtConcurrent::task([](QString text) {
    return text.toUpper();
}).withArguments(QString("hello"))
  .withPriority(5)
  .spawn();

const QString result = future.result(); // "HELLO"
```

这段代码中：

1. `QtConcurrent::task(...)` 接收 callable，返回 `QTaskBuilder`。
2. `withArguments(...)` 把执行参数保存到任务中。
3. `withPriority(5)` 记录提交优先级。
4. `spawn()` 非阻塞地提交任务，立刻返回 `QFuture<QString>`。

`spawn()` 返回不代表任务已经开始，更不代表任务已经完成；线程池可能仍在排队。

## 2. 为什么不直接用 `QtConcurrent::run`

只需把一个函数丢到默认线程池时，`QtConcurrent::run(...)` 更短：

```cpp
auto future = QtConcurrent::run([] { return calculate(); });
```

当需要额外配置时再使用 `task()` / `QTaskBuilder`：

- 指定私有 `QThreadPool`，隔离 CPU 密集任务；
- 设置任务优先级；
- 先把参数绑定为一个可读的链式调用；
- 决定是否返回 `QFuture`；
- 使用 `QFuture`、`QFutureWatcher` 或 `QPromise` 配合后续流程。

它不是 `QThread` 的替代品。任务运行在池线程，不能假设固定线程身份，也不能在任务中直接操作 GUI。

## 3. 参数绑定：默认复制，引用必须显式承担生命周期

`withArguments(...)` 调用时会复制每一个参数。任务实际开始时使用的是这份保存的值：

```cpp
QString name = "Ada";

auto future = QtConcurrent::task([](const QString &value) {
    return value + " Lovelace";
}).withArguments(name)
  .spawn();

name = "Grace"; // 不会影响已经绑定到任务的参数
```

这通常是正确默认值：调用栈返回、原变量修改或 UI 输入变化，都不会让后台任务看到悬空引用或半更新数据。

若 callable 明确要求引用，必须使用 `std::ref` / `std::cref`：

```cpp
#include <functional>

QString output;

auto future = QtConcurrent::task([](QString &value) {
    value = "done";
}).withArguments(std::ref(output))
  .spawn();

future.waitForFinished();
```

此时 `output` 必须活得比任务久，而且并发读写仍要自行同步。`std::ref` 只改变传参方式，不会让共享数据自动线程安全。

`withArguments(...)` 只能调用一次，并且至少要传一个参数；第二次调用或传入零参数会在编译期报错。需要复杂参数时，先组装一个请求对象，再一次性传入。

## 4. 线程池与优先级

### 4.1 `onThreadPool`

默认任务进入全局线程池。应用中已有多个模块时，CPU 密集导入、缩略图生成或批量计算长期占满全局池，会影响其他 Qt Concurrent 工作。

```cpp
QThreadPool importPool;
importPool.setMaxThreadCount(2);

auto future = QtConcurrent::task([files] {
    return importFiles(files);
}).onThreadPool(importPool)
  .spawn();
```

传入的是 `QThreadPool &`。因此 pool 必须在任务排队和运行期间保持存活；不要传入即将离开作用域的局部 pool。

### 4.2 `withPriority`

优先级影响线程池中等待任务的调度倾向：

```cpp
QtConcurrent::task([] { rebuildPreview(); })
    .withPriority(10)
    .spawn(QtConcurrent::FutureResult::Ignore);
```

它不是实时调度保证，也不会抢占已经运行的低优先级任务。优先级只是在资源紧张时帮助线程池决定先取哪项工作；不能把它当成修复阻塞、死锁或过大任务粒度的手段。

## 5. 两种 `spawn`

### 5.1 `spawn()`: 需要结果、完成状态或等待能力

```cpp
QFuture<int> future = QtConcurrent::task([] {
    return 42;
}).spawn();
```

返回的 future 可用于：

- `result()` 获取结果；
- `waitForFinished()` 等待完成；
- 交给 `QFutureWatcher` 在 QObject 事件循环中接收完成通知；
- 按任务类型配合取消、进度或多结果工作流。

注意：在 GUI 线程直接调用 `future.result()` 或 `waitForFinished()` 会阻塞界面。GUI 中优先使用 `QFutureWatcher` 或异步继续处理。

### 5.2 `spawn(QtConcurrent::FutureResult::Ignore)`: 不需要 future

```cpp
QtConcurrent::task([] {
    writeTelemetry();
}).spawn(QtConcurrent::FutureResult::Ignore);
```

它仍然是非阻塞提交，只是不会创建并返回 `QFuture`。因此调用方失去通过 future 查询完成状态和取得结果的入口。只适合真正不需要结果、不需要同步等待的后台动作。

## 6. `InvokeResultType` 是什么

`InvokeResultType` 表示 task 被指定参数调用后的返回类型，概念上接近：

```cpp
std::invoke_result_t<std::decay_t<Task>,
                     std::decay_t<Args>...>
```

Qt 还会在编译期检查 callable 是否真的能接受这些参数。于是下面的问题会尽早暴露为编译错误，而不是在线程池运行后才出错：

- 函数参数数量不匹配；
- 传入类型无法转换；
- 非 const 成员函数需要对象却没有提供；
- move-only 参数的传递方式不正确。

## 7. 常见误区

### 手动构造 `QTaskBuilder`

不能。它没有给用户直接创建的普通构造路径，应从 `QtConcurrent::task(callable)` 开始。

### 以为 `spawn()` 已经开始执行

它只保证提交非阻塞完成。任务可能因为线程池繁忙而稍后才开始。

### 用 `std::ref` 避免复制，却忘了对象生命周期

后台任务可能晚于当前函数返回。引用包装的对象一旦先销毁，就会产生未定义行为；并发访问还需要锁、原子操作或其他同步机制。

### 在 GUI 线程调用 `future.result()`

这会等待任务结束并冻结界面。使用 `QFutureWatcher` 把结果处理留在事件循环中。

## API 速查表
| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 创建入口 | `QtConcurrent::task(callable)` | 创建并返回 `QTaskBuilder`，开始配置一个尚未提交的任务 | `QTaskBuilder` 不能手动构造；只需默认提交时可直接考虑 `QtConcurrent::run` |
| 参数绑定 | `withArguments(ExtraArgs &&...args)` | 一次性设置 callable 实际执行时接收的参数，并返回新的 builder | 调用时默认复制参数；只能调用一次且至少传一个参数 |
| 参数绑定 | `std::ref` / `std::cref` | 显式让任务按引用接收参数 | 被引用对象必须活得比任务久，且共享访问仍需自行同步 |
| 线程池 | `onThreadPool(QThreadPool &newThreadPool)` | 指定任务应提交到哪个线程池 | 传入引用，pool 必须覆盖任务排队和运行期；适合隔离重任务 |
| 优先级 | `withPriority(int newPriority)` | 设置任务提交给线程池时的优先级 | 影响排队倾向，不保证立刻执行，也不抢占已运行任务 |
| 提交并取结果 | `spawn()` | 非阻塞提交任务并立即返回 `QFuture<InvokeResultType>` | 任务不保证立刻开始；不要在 GUI 线程同步等待 future |
| 提交但忽略结果 | `spawn(QtConcurrent::FutureResult::Ignore)` | 非阻塞提交任务，但不创建/返回 future 句柄 | 之后无法通过 future 取得结果、等待完成或跟踪状态 |
| 结果类型 | `QtConcurrent::InvokeResultType` | 表示 task 与绑定参数实际调用后的返回类型 | Qt 会在编译期检查 callable 能否按这些参数被调用 |

---

### 一句话总结

`QTaskBuilder` 是 `QtConcurrent::task()` 的提交前配置器：用它绑定稳定参数、选择线程池和优先级，再用 `spawn()` 把任务非阻塞地交给线程池，并按是否需要 `QFuture` 选择保留还是忽略执行结果。
