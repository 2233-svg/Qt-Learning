# Qt QSemaphore：按许可数量控制并发资源

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QSemaphore>`  
> 所属模块：`Qt6::Core`  
> 类型性质：不可复制、线程安全的计数信号量

## 1. 它解决什么问题

`QSemaphore` 用一个非负许可计数表示“当前有多少个同类资源可用”。线程通过 `acquire(n)` 取得 `n` 个许可，工作完成后通过 `release(n)` 归还。

```cpp
QSemaphore slots(3);

slots.acquire();  // 可用许可：2
useOneResource();
slots.release();  // 可用许可：3
```

它适合：

- 限制同时运行的任务数量；
- 保护固定数量的连接、缓冲区、设备槽位或并发请求；
- 实现生产者/消费者队列中的“空槽数量”和“已有项目数量”；
- 需要一次取得多个同类资源的场景。

它和 `QMutex` 的区别是：mutex 通常只有“一个人持有”的状态，semaphore 可以同时允许多个线程持有不同许可。

## 2. 许可计数模型

```text
QSemaphore(5)       -> available() == 5
acquire(3)           -> available() == 2
acquire(2)           -> available() == 0
release(5)           -> available() == 5
release(5)           -> available() == 10
```

`release(n)` 不要求一定对应之前的 `acquire(n)`，因此它也可以“创建”新的可用许可。但在资源池协议里，通常应让取得和归还严格配对，否则计数会失真。

所有公开函数都是线程安全的，但 `available()` 只是某一时刻的观察值，读取后计数可能立即被其他线程改变，不能把它当成预留承诺。

## 3. 阻塞取得：`acquire()`

```cpp
semaphore.acquire(2);
```

如果当前可用许可少于 `n`，调用会阻塞，直到足够许可被释放。成功返回时，调用者已经取得全部请求数量；它不会“先给一部分”。

把阻塞调用放在工作线程、线程池任务或明确允许等待的服务线程中。不要在 GUI 线程用无限等待代替响应式流程，也不要在持有其他锁时等待可能由被阻塞线程才能释放的 semaphore。

## 4. 非阻塞取得：`tryAcquire()`

```cpp
if (semaphore.tryAcquire(2)) {
    processTwoSlots();
    semaphore.release(2);
}
```

无超时重载立即返回：

- 资源足够：取得全部 `n` 个许可，返回 `true`；
- 资源不足：不取得任何许可，返回 `false`。

这是“全有或全无”的操作。失败后不能假设已经拿到一部分资源。

## 5. 超时重载

### 5.1 毫秒

```cpp
if (semaphore.tryAcquire(1, 200)) {
    QSemaphoreReleaser releaseOnExit(semaphore);
    work();
}
```

最多等待 `timeout` 毫秒。`timeout == 0` 表示立即尝试；负值等价于 `acquire()`，即无限等待。

### 5.2 `QDeadlineTimer`

```cpp
if (semaphore.tryAcquire(2, QDeadlineTimer(500))) {
    useResources();
    semaphore.release(2);
}
```

Qt 6.6 起提供 `QDeadlineTimer` 重载，适合多个等待步骤共享同一个绝对截止时间，避免每一步都重新计算相对剩余时间。

### 5.3 `std::chrono`

```cpp
using namespace std::chrono_literals;

if (semaphore.tryAcquire(1, 100ms)) {
    useResource();
    semaphore.release();
}
```

Qt 6.3 起提供 chrono 重载。它只是超时表达方式的适配，不改变 semaphore 的全有或全无语义。

### 5.4 标准库兼容 API

```cpp
if (semaphore.try_acquire()) {
    useResource();
    semaphore.release();
}

if (semaphore.try_acquire_for(50ms)) {
    useResource();
    semaphore.release();
}

auto deadline = std::chrono::steady_clock::now() + 50ms;
if (semaphore.try_acquire_until(deadline)) {
    useResource();
    semaphore.release();
}
```

这些 API 是为了兼容 `std::counting_semaphore` 风格；它们每次只取得一个许可。

## 6. 归还许可与 RAII

```cpp
if (!semaphore.tryAcquire(3))
    return false;

QSemaphoreReleaser releaser(semaphore, 3);
return processBatch();
```

`QSemaphoreReleaser` 只负责析构时 `release(n)`，不负责 acquire。成功取得许可后应立即创建它，避免后续异常或早退泄漏许可。

如果使用手工释放，也要保证所有路径都归还：

```cpp
semaphore.acquire();
try {
    work();
} catch (...) {
    semaphore.release();
    throw;
}
semaphore.release();
```

## 7. 生产者/消费者模型

固定容量的循环缓冲区常用两个 semaphore：

```text
emptySlots：初始为缓冲区容量
usedSlots：初始为 0

生产者：emptySlots.acquire() -> 写入 -> usedSlots.release()
消费者：usedSlots.acquire()  -> 读取 -> emptySlots.release()
```

semaphore 只协调数量，不保护缓冲区索引和内存本身。如果多个线程会同时修改索引或容器，仍需要 mutex、原子变量或单生产者/单消费者的明确约束。

## 8. 生命周期和计数边界

销毁正在使用中的 `QSemaphore` 可能导致未定义行为。销毁前要停止新的 acquire/release，并等待所有线程退出相关临界区。

初始值和操作数量应表达有效的资源数量。不要传入负数，也不要让整数溢出；许可计数必须由业务协议约束在合理范围内。

`available()` 返回值永远不会是负数，但它不是事务操作：

```cpp
if (semaphore.available() > 0) {
    // 这里不能保证下一行一定能 acquire
}
```

如果需要原子地“检查并取得”，直接使用 `tryAcquire()`。

## 9. 常见错误

### 9.1 把 semaphore 当 mutex

取得一个许可不等于获得对所有共享数据的独占访问。需要互斥时用 `QMutex`。

### 9.2 失败后释放许可

`tryAcquire(n)` 失败时一个许可也没有取得；不要无条件 `release(n)`。

### 9.3 部分取得的错误假设

Qt 的 acquire 操作要么取得请求的全部许可，要么在 tryAcquire 失败时一个都不取得。

### 9.4 忘记归还

成功 acquire 后应立即用 `QSemaphoreReleaser` 或建立清晰的异常安全释放路径。

### 9.5 用 `available()` 做预留

读取和后续 acquire 之间可能被其他线程抢先改变。要取得资源直接调用 `tryAcquire()`。

### 9.6 持有 mutex 时等待 semaphore

如果归还许可的线程需要同一把 mutex，就会形成锁等待环。调整锁顺序或缩小临界区。

## 10. 逐项 API 语义

| API | 语义 | 边界 |
| --- | --- | --- |
| `explicit QSemaphore(int n = 0)` | 创建信号量并设置初始许可数。 | 默认没有可用许可；使用非负资源数量。 |
| `~QSemaphore()` | 销毁信号量。 | 正在使用或仍有线程等待时可能未定义。 |
| `void acquire(int n = 1)` | 阻塞直到取得 `n` 个许可。 | 取得全部后才返回；不要在不允许阻塞的线程调用。 |
| `bool tryAcquire(int n = 1)` | 立即尝试取得 `n` 个许可。 | 失败时一个都不取得。 |
| `bool tryAcquire(int n, int timeout)` | 最多等待毫秒数。 | 负 timeout 等价于无限等待。 |
| `bool tryAcquire(int n, QDeadlineTimer timeout)` | 等到截止时间。 | Qt 6.6 起；适合共享剩余预算。 |
| `bool tryAcquire(int n, std::chrono::duration<Rep, Period> timeout)` | chrono 相对超时。 | Qt 6.3 起。 |
| `void release(int n = 1)` | 增加 `n` 个可用许可。 | 可以创建新许可；业务上要防止计数失真。 |
| `int available() const` | 返回当前可用许可数。 | 只是瞬时观察值，不是预留。 |
| `bool try_acquire()` | 标准兼容地立即取得一个许可。 | Qt 6.3 起。 |
| `try_acquire_for(duration)` | 标准兼容地按相对时间取得一个许可。 | Qt 6.3 起。 |
| `try_acquire_until(time_point)` | 标准兼容地按时间点取得一个许可。 | Qt 6.3 起。 |

## API 速查表
| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 初始化 | `QSemaphore(n)` | 设置初始许可数。 | 许可数应是有效的非负资源数量。 |
| 阻塞 | `acquire(n)` | 等待并取得全部 `n` 个许可。 | 不要在 GUI 或持锁状态下无限等待。 |
| 立即尝试 | `tryAcquire(n)` | 不等待地取得全部许可。 | 失败时一个都不取得。 |
| 超时 | `tryAcquire(n, timeout)` | 在毫秒、deadline 或 chrono 时间内等待。 | 负毫秒值表示无限等待。 |
| 归还 | `release(n)` | 增加可用许可。 | 可“创建”许可，必须维护计数协议。 |
| 观察 | `available()` | 查询当前可用数量。 | 不能代替原子 acquire。 |
| RAII | `QSemaphoreReleaser` | 作用域结束时自动归还许可。 | 先成功 acquire，再创建 releaser。 |
| 标准兼容 | `try_acquire*()` | 对接 C++ counting semaphore 风格。 | 每次只处理一个许可。 |

---

### 一句话总结

`QSemaphore` 用许可计数限制并发资源：`acquire` 要么取得全部请求数量，要么阻塞/失败，成功后必须准确 `release`，最好用 `QSemaphoreReleaser` 管理归还。
