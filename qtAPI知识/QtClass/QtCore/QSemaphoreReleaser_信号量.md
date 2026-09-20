# Qt QSemaphoreReleaser：作用域结束时归还信号量许可

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QSemaphoreReleaser>`  
> 所属模块：`Qt6::Core`  
> 类型性质：不可复制、可移动的 RAII 信号量释放器  
> 相关类型：`QSemaphore`

## 1. 它解决什么问题

`QSemaphore` 的 `acquire(n)` 会消耗 `n` 个许可。函数如果在处理过程中提前返回或抛出异常，手工调用 `release(n)` 很容易遗漏，最终造成许可泄漏，后续线程永久等待。

`QSemaphoreReleaser` 把“归还许可”绑定到作用域：

```cpp
bool process(QSemaphore &semaphore)
{
    if (!semaphore.tryAcquire(3))
        return false;

    QSemaphoreReleaser releaser(semaphore, 3);
    return doWork();
} // 自动 release(3)
```

它不负责取得许可，只负责在仍然关联信号量时，于析构阶段调用 `release(n)`。

## 2. 它不是什么

`QSemaphoreReleaser` 不是：

- `QSemaphore` 本身；
- 自动 acquire 的锁；
- 计数器快照；
- 信号量对象的所有权容器；
- 可以复制的共享释放责任；
- 事务回滚器。

它保存一个裸 `QSemaphore *` 和一个释放数量。信号量必须在 releaser 析构前保持有效，releaser 不会删除它。

## 3. 构建与包含

```cmake
find_package(Qt6 REQUIRED COMPONENTS Core)
target_link_libraries(mytarget PRIVATE Qt6::Core)
```

```cpp
#include <QSemaphoreReleaser>
```

它通常和 `QSemaphore::acquire()` 或成功的 `tryAcquire()` 成对出现。

## 4. 最小可用代码

```cpp
#include <QSemaphore>
#include <QSemaphoreReleaser>

bool consumeOne(QSemaphore &slots)
{
    if (!slots.tryAcquire())
        return false;

    QSemaphoreReleaser releaseOnExit(slots);
    return consume();
}
```

无论 `consume()` 返回什么，成功取得的一个许可都会在作用域结束时归还。

## 5. 正确配对 acquire 和 release

### 5.1 先成功取得，再创建 releaser

```cpp
if (!semaphore.tryAcquire(count))
    return false;

QSemaphoreReleaser releaser(semaphore, count);
```

如果 acquire 失败，就没有许可需要归还，不应提前创建一个活动 releaser。

### 5.2 释放数量必须与实际取得数量匹配

```cpp
const int count = 4;
semaphore.acquire(count);
QSemaphoreReleaser releaser(semaphore, count);
```

释放少于取得的数量会泄漏许可；释放多于取得的数量会人为增加可用许可，破坏信号量计数协议。`QSemaphoreReleaser` 不知道你实际 acquire 了多少，也不会自动校验。

### 5.3 `release(n)` 的参数前置条件仍然适用

Qt 头文件中的 releaser 构造函数只保存 `n`，不验证它。析构时直接调用 `QSemaphore::release(m_n)`。因此应传入满足 `QSemaphore::release()` 契约的有效数量，通常为非负且表示实际要归还的许可数；不要依赖 releaser 修正负数或溢出。

## 6. 析构、空状态和 `cancel()`

### 6.1 析构只释放仍关联的信号量

```cpp
{
    QSemaphoreReleaser releaser(semaphore, 2);
} // semaphore.release(2)
```

如果内部指针为空，析构不执行释放。默认构造的对象、已经 `cancel()` 的对象和移动后的源对象都属于这种非活动状态。

### 6.2 默认构造是空 releaser

```cpp
QSemaphoreReleaser releaser;
Q_ASSERT(releaser.semaphore() == nullptr);
```

默认构造不会取得或释放任何许可。它可以作为之后通过移动赋值接收责任的空对象，但不能通过公开成员重新绑定信号量。

### 6.3 `cancel()` 放弃未来释放

```cpp
QSemaphoreReleaser releaser(semaphore, 2);
QSemaphore *old = releaser.cancel();
Q_ASSERT(old == &semaphore);
```

`cancel()` 返回原来保存的信号量指针，并把内部指针设为 `nullptr`。它不调用 `release()`，也不返回释放数量。调用后析构不会归还许可。

使用 `cancel()` 前必须确认你已经在其他路径正确处理了这批许可；否则就是有意制造许可泄漏。

## 7. 移动和交换语义

### 7.1 不可复制，只能移动

复制会造成两个对象都在析构时调用 `release(n)`，导致许可被归还两次，因此复制构造和复制赋值被禁用。

```cpp
QSemaphoreReleaser first(semaphore, 2);
QSemaphoreReleaser second(std::move(first));

Q_ASSERT(first.semaphore() == nullptr);
Q_ASSERT(second.semaphore() == &semaphore);
```

移动构造把信号量指针和释放责任转移给目标对象；源对象不再释放。

### 7.2 移动赋值会清理目标原责任

```cpp
QSemaphoreReleaser first(semaphoreA, 1);
QSemaphoreReleaser second(semaphoreB, 2);
second = std::move(first);
```

Qt 通过移动和交换实现赋值。`second` 原先负责的 `semaphoreB.release(2)` 不会泄漏，临时对象析构时会完成旧责任；之后 `second` 接管 `first` 的释放责任。

实际代码应尽量让一个 releaser 对应一个清晰的 acquire 作用域，减少复杂的责任转移。

### 7.3 `swap()` 交换数量和指针

```cpp
releaserA.swap(releaserB);
```

交换的不只是信号量指针，还有释放数量。交换后每个对象负责另一方原来的释放动作。

## 8. 生命周期和并发边界

### 8.1 信号量必须比 releaser 活得久

```cpp
QSemaphoreReleaser badReleaser()
{
    QSemaphore local(1);
    return QSemaphoreReleaser(local, 1);
}
```

返回后 `local` 已销毁，releaser 析构时会访问悬空指针。应让信号量由外层对象拥有，并保证整个 releaser 生命周期都覆盖在内。

### 8.2 `release()` 可能唤醒等待线程

releaser 析构调用 `QSemaphore::release(n)`，可能让等待许可的线程继续执行。析构点不只是普通的内存清理点，它可能产生并发可见的同步效果。

因此不要在一个尚未完成必要状态发布的临界点提前销毁 releaser；让释放许可的时机与业务资源真正可用的时机一致。

### 8.3 不替代数据同步

信号量可以协调许可数量，但不会自动保护其他共享字段。若处理逻辑同时读写共享数据，仍需要互斥锁、原子变量或消息传递协议。

## 9. 实际使用模式

### 9.1 处理固定数量的资源槽

```cpp
bool Worker::run(Task task)
{
    if (!slots.tryAcquire())
        return false;

    QSemaphoreReleaser releaseSlot(slots);
    return execute(task);
}
```

### 9.2 批量占用和归还

```cpp
bool BufferPool::use(int count)
{
    if (!available.tryAcquire(count))
        return false;

    QSemaphoreReleaser releaseBuffers(available, count);
    fillBuffers(count);
    return true;
}
```

### 9.3 成功转移责任后取消自动归还

```cpp
bool submit(QSemaphore &slots)
{
    if (!slots.tryAcquire())
        return false;

    QSemaphoreReleaser releaser(slots);
    if (!queueOwnsSlot())
        return false;

    releaser.cancel();
    return true;
}
```

这里表示许可的释放责任已经转移给队列或其他协议。只有在确实存在后续释放者时才应调用 `cancel()`。

## 10. 逐项 API 语义

### 10.1 `QSemaphoreReleaser()`

```cpp
QSemaphoreReleaser() = default;
```

构造空对象，内部信号量指针为空、释放数量为零，不产生任何信号量操作。

### 10.2 `QSemaphoreReleaser(QSemaphore &sem, int n = 1)`

```cpp
explicit QSemaphoreReleaser(QSemaphore &sem, int n = 1) noexcept;
```

保存 `&sem` 和 `n`。构造时不调用 acquire 或 release；析构时若未取消，则调用 `sem.release(n)`。

### 10.3 `QSemaphoreReleaser(QSemaphore *sem, int n = 1)`

```cpp
explicit QSemaphoreReleaser(QSemaphore *sem, int n = 1) noexcept;
```

保存传入指针和数量。`sem == nullptr` 时构造空责任，不会在析构时释放。

### 10.4 `QSemaphoreReleaser(QSemaphoreReleaser &&other)`

```cpp
QSemaphoreReleaser(QSemaphoreReleaser &&other) noexcept;
```

转移信号量指针和释放责任。源对象通过 `cancel()` 变为空，目标对象在析构时负责原来的 release。

### 10.5 `~QSemaphoreReleaser()`

```cpp
~QSemaphoreReleaser();
```

如果内部指针非空，调用 `m_sem->release(m_n)`；否则不执行操作。它不等待、不 acquire，也不验证数量是否与历史 acquire 匹配。

### 10.6 `swap(QSemaphoreReleaser &other)`

```cpp
void swap(QSemaphoreReleaser &other) noexcept;
```

交换两个对象的信号量指针和释放数量，不调用 release。交换后释放责任随状态一起转移。

### 10.7 `semaphore() const`

```cpp
QSemaphore *semaphore() const noexcept;
```

返回当前关联的信号量指针。默认构造、取消或移动后的源对象返回 `nullptr`。它不返回释放数量，也不转移所有权。

### 10.8 `cancel()`

```cpp
QSemaphore *cancel() noexcept;
```

返回当前信号量指针并清空内部指针，使析构不再 release。重复调用返回 `nullptr`，不会重新建立责任。

### 10.9 `operator=(QSemaphoreReleaser &&other)`

```cpp
QSemaphoreReleaser &operator=(QSemaphoreReleaser &&other) noexcept;
```

移动赋值并处理目标对象原先的释放责任。复制赋值不可用。

## 11. 常见错误

### 11.1 acquire 失败仍创建活动 releaser

如果 `tryAcquire()` 返回 `false`，不应创建带有效信号量的 releaser，否则析构会凭空增加许可。

### 11.2 释放数量和取得数量不一致

releaser 不记录 acquire 历史。数量错误会破坏信号量协议，尤其是批量资源池。

### 11.3 `cancel()` 后没有后续释放者

`cancel()` 不会归还许可。只有在责任已经明确转交给其他对象或业务路径时才使用。

### 11.4 信号量先销毁

releaser 保存的是裸指针，不会跟踪信号量生命周期。确保信号量比 releaser 活得久。

### 11.5 把 `QSemaphoreReleaser` 当成自动 acquire

构造函数从不取得许可。它只能保护一批已经成功取得的许可。

## API 速查表
| API | 作用 | 使用时重点注意 |
| --- | --- | --- |
| `QSemaphoreReleaser()` | 构造空释放器 | 不 acquire，不 release；可通过移动赋值接收责任 |
| `QSemaphoreReleaser(QSemaphore &, int)` | 记录信号量和释放数量 | 构造不操作信号量；析构默认 release |
| `QSemaphoreReleaser(QSemaphore *, int)` | 指针版本记录释放责任 | `nullptr` 形成空对象；不拥有信号量 |
| `QSemaphoreReleaser(QSemaphoreReleaser &&)` | 转移释放责任 | 源对象不再释放；不可复制 |
| `~QSemaphoreReleaser()` | 在仍活动时调用 `release(n)` | 释放数量必须和实际 acquire 匹配 |
| `swap(other)` | 交换信号量指针和数量 | 不立即 release；责任整体交换 |
| `semaphore()` | 查询当前信号量指针 | 不返回数量，不转移所有权 |
| `cancel()` | 放弃未来 release 并返回原指针 | 不释放许可；必须已有后续释放协议 |
| `operator=(QSemaphoreReleaser &&)` | 移动赋值 | 目标旧责任会被清理 |

## 13. 一句话总结

`QSemaphoreReleaser` 只负责“成功 acquire 后，作用域结束时 release 同样数量”：它不取得许可、不拥有信号量、不可复制但可移动；`cancel()` 会彻底放弃自动释放，因此只有在责任已明确转移时才应使用。
