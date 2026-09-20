# QTaskTree：运行一棵声明式异步任务树

> Qt 6.11.1 · `#include <qtasktree.h>` · 模块：`Qt6::TaskTree` · 继承：`QObject`

`QTaskTree` 是 QtTaskTree recipe 的运行器。`Group`、`QCustomTask`、`For`、`When` 等类型只描述“要怎样跑”；真正创建任务实例、推进子节点、发出进度、处理取消和最终结果的是 `QTaskTree`。

## 解决的问题

传统 Qt 异步流程常会散落在多个 signal/slot、lambda 和状态变量里：网络请求完成后启动解析，解析成功后再保存，中途用户取消还要清理每一层。`QTaskTree` 把这些步骤放进一个声明式 recipe，然后用一个对象统一启动、取消、观察结果和进度。

它适合有明确生命周期的流程：导入项目、批量下载、构建索引、按顺序执行初始化步骤、并行启动几个可取消任务。若只是一次普通函数调用，`QSyncTask` 或直接调用函数通常更简单。

## 启动与事件循环

`start()` 依赖 Qt 事件循环推进异步节点。它也可能在调用栈内同步完成，比如 recipe 为空、全是同步成功项，或 setup handler 直接停止。因此连接 `done()`、`progressValueChanged()` 这类信号要放在 `start()` 之前。

同一个 `QTaskTree` 运行期间不要重新 `setRecipe()` 或再次 `start()`。需要“最新请求覆盖旧请求”时，用 `QSingleTaskTreeRunner`；需要队列时，用 `QSequentialTaskTreeRunner`。

## 取消、析构与回调边界

`cancel()` 是同步取消：它会停止运行中的任务和组，调用任务/组 done handler，结果为 `DoneWith::Cancel`，并发出相应进度与 `done()` 信号。不要在正在运行的 task handler 或 `QTaskTree` 自己的信号处理函数里直接调用 `cancel()`，容易重入同一棵树。

析构行为更硬：如果树还在运行，析构会立即取消内部任务，但不会调用 handler，也不会发 `done()`、进度等信号。也不要在 task handler 或树信号里直接删除正在运行的树；需要销毁时使用 `deleteLater()` 或交给 runner 管理。

## 阻塞运行

`runBlocking()` 会启动一个本地事件循环，并使用 `ExcludeUserInputEvents`。它主要用于非 GUI 主线程或自动化测试；在主线程里用它会让界面输入被排除，且更容易制造嵌套事件循环问题。支持 future 的重载可把外部取消源接入阻塞等待。

## API 速查表

| API | 语义与边界 |
|---|---|
| `QTaskTree(QObject *parent = nullptr)` | 构造空树；未设置 recipe 时启动没有实际任务。 |
| `QTaskTree(const Group &recipe, QObject *parent = nullptr)` | 用 recipe 构造可运行树；recipe 是描述，任务实例在运行时创建。 |
| `~QTaskTree()` | 运行中析构会立即取消内部任务，但不调用 done handlers，也不发 `done()`。 |
| `setRecipe(const Group &recipe)` | 设置下一次运行的 recipe；不要在树正在运行时替换。 |
| `start()` | 启动任务树；可能同步完成，信号连接应先于调用。 |
| `cancel()` | 同步取消运行中的树；会调用相关 done handlers，最终结果是 `DoneWith::Cancel`。 |
| `isRunning() const` | 判断树是否仍在运行；同步完成的 recipe 可能在 `start()` 返回前已变回 false。 |
| `runBlocking()` | 本地事件循环阻塞等待当前 recipe 完成；不建议在 GUI 主线程使用。 |
| `runBlocking(const Group &recipe)` | 便捷静态版本，构造临时树并阻塞运行。 |
| `runBlocking(const QFuture<void> &future)` | future 取消时联动取消任务树；仅在 Qt future 功能启用时可用。 |
| `asyncCount() const` | 统计控制权返回事件循环的异步链次数；`asyncCountChanged(0)` 会在初始启动阶段发出。 |
| `taskCount() const` | 统计 recipe 中可观察的异步任务数；`QSyncTask` 不计入，`withTimeout()` 会额外增加任务。 |
| `progressMaximum() const` | 等同于 `taskCount()`，可直接接进进度条最大值。 |
| `progressValue() const` | 已完成、已取消、已跳过的任务数量；不把组节点本身计入。 |
| `onStorageSetup(storage, handler)` | storage 实例创建后调用，handler 接收 `StorageStruct &`。 |
| `onStorageDone(storage, handler)` | storage 销毁前调用，handler 接收 `const StorageStruct &`；取消路径也会调用。 |
| `started()` | 树开始运行时发出。 |
| `done(DoneWith)` | 树完成、出错或取消时发出；析构强制取消不会发出。 |
| `asyncCountChanged(qsizetype)` | 异步链计数变化时发出，可用来观察任务是否又让出到事件循环。 |
| `progressValueChanged(qsizetype)` | 每当任务完成、取消或跳过时发出。 |
