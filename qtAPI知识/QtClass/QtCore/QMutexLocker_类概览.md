# Qt QMutexLocker：互斥锁的作用域管理

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QMutexLocker>`  
> 所属模块：`Qt6::Core`  
> 类型性质：模板化 RAII 锁管理器  
> 相关类型：`QMutex`、`QRecursiveMutex`

## 1. 它解决什么问题

手工调用 `lock()` / `unlock()` 最容易出错的地方，不是加锁本身，而是函数中途出现：

- `return`；
- 异常；
- 多个分支；
- 新增的早退出路径；
- 后续维护者忘记补 `unlock()`。

`QMutexLocker` 把“获得锁”和“离开作用域时释放锁”绑定在一个对象的生命周期上：

```cpp
QMutex mutex;

void updateValue(int &value)
{
    QMutexLocker<QMutex> locker(&mutex);
    ++value;
} // locker 析构，自动 unlock()
```

因此它适合保护一个明确的临界区，尤其适合有多个返回路径的函数。它管理的是锁的使用状态，不拥有 `QMutex` 对象本身。

## 2. 它不是什么

`QMutexLocker` 不是：

- `QMutex` 的替代品；
- 互斥量的所有权容器；
- 自动创建或销毁 mutex 的智能指针；
- 可复制的锁句柄；
- 读写锁升级工具；
- 解决锁顺序、跨线程对象生命周期或业务死锁的万能机制。

传入的 `Mutex *` 必须在 locker 的整个使用期间保持有效。locker 析构只调用 `unlock()`，不会 `delete` 这个指针。

## 3. 构建与包含

```cmake
find_package(Qt6 REQUIRED COMPONENTS Core)
target_link_libraries(mytarget PRIVATE Qt6::Core)
```

```cpp
#include <QMutexLocker>
```

`QMutexLocker` 是类模板。实际使用时通常让编译器从 `Mutex *` 推导模板参数，也可以显式写出 `QMutexLocker<QMutex>`。

## 4. 最小可用代码

```cpp
#include <QMutex>
#include <QMutexLocker>

class Counter
{
public:
    void increment()
    {
        QMutexLocker locker(&mutex);
        ++value;
    }

    int read() const
    {
        QMutexLocker locker(&mutex);
        return value;
    }

private:
    mutable QMutex mutex;
    int value = 0;
};
```

这里的两个函数都有自动释放路径。`read()` 使用 `mutable` mutex，是因为 const 成员函数仍然需要保护可变的同步状态。

## 5. 核心语义：构造即加锁，析构即解锁

### 5.1 构造函数会立即尝试锁定

```cpp
QMutexLocker locker(&mutex);
```

对非空指针，构造函数调用 `mutex->lock()`。如果 mutex 已被其他线程持有，构造过程会阻塞，直到获得锁。

这意味着 locker 的构造点就是潜在阻塞点。不要在持有另一个锁时随意构造它，除非整个项目已经明确规定了锁顺序。

### 5.2 析构函数只在当前状态为已锁定时解锁

locker 记录自己的 `m_isLocked` 状态。正常构造后为已锁定，调用 `unlock()` 后变为未锁定，析构时只对仍然锁定的对象执行解锁。

因此这种写法是安全的：

```cpp
QMutexLocker locker(&mutex);

if (!ready())
    return; // 析构时仍会解锁

locker.unlock();
doWorkWithoutLock();
```

但解锁后如果还要继续访问受保护数据，必须先 `relock()`；否则临界区已经结束。

### 5.3 `nullptr` 是“非活动 locker”，不是有效锁

```cpp
QMutexLocker<QMutex> locker(nullptr);
Q_ASSERT(!locker.isLocked());
Q_ASSERT(locker.mutex() == nullptr);
```

构造函数对空指针不调用锁操作。这个行为可以用于可选锁，但不应把它误认为已经保护了数据。对这种 locker 调用 `relock()` 会尝试使用空的 mutex 指针，不能这样写。

## 6. 生命周期、所有权和移动语义

### 6.1 locker 不拥有 mutex

```cpp
QMutex mutex;
{
    QMutexLocker locker(&mutex);
    // mutex 必须至少活到 locker 析构
}
```

不要把 locker 返回给调用方，同时让它引用函数内部的局部 mutex。也不要在 locker 仍然存在时销毁或移动它所引用的 mutex。

### 6.2 不可复制，只能移动

复制 locker 会产生两个对象都以为自己负责同一个解锁动作，因此复制构造和复制赋值被禁用。Qt 6.4 起提供移动构造和移动赋值，用于转移“当前关联 mutex + 是否已锁定”的状态。

```cpp
QMutexLocker first(&mutex);
QMutexLocker second(std::move(first));

Q_ASSERT(!first.isLocked());
Q_ASSERT(first.mutex() == nullptr);
Q_ASSERT(second.isLocked());
```

移动后，源 locker 处于空、未锁定状态；目标 locker 接管解锁责任。不要继续把 moved-from 对象当作原来的锁管理器使用。

### 6.3 移动赋值会先处理目标对象的旧状态

```cpp
QMutexLocker first(&mutexA);
QMutexLocker second(&mutexB);

second = std::move(first);
```

移动赋值通过交换和临时对象处理当前目标状态。目标原先管理的锁不能因此泄漏，临时对象析构时会释放旧锁。实际代码中仍应尽量让一个 locker 对应一个清晰的作用域，避免在复杂控制流里频繁转移。

## 7. 手动暂停和恢复临界区

### 7.1 `unlock()`：提前释放

```cpp
QMutexLocker locker(&mutex);
prepareProtectedData();

locker.unlock();
callSlowOrReentrantCode();
```

`unlock()` 要求当前 locker 处于已锁定状态。Qt 头文件通过断言检查这一前置条件；重复调用不是可依赖的幂等操作。

调用后：

- `isLocked()` 返回 `false`；
- `mutex()` 仍返回原 mutex 指针；
- 析构函数不会再次解锁；
- 临界区已经结束，不能继续无保护地读写共享状态。

### 7.2 `relock()`：重新取得同一个 mutex

```cpp
locker.unlock();
// 不访问共享状态
locker.relock();
```

`relock()` 要求 locker 当前未锁定，并再次调用保存的 `Mutex *` 的 `lock()`。如果 locker 原本由 `nullptr` 构造，就没有可重锁的对象；不要对这种 locker 调用 `relock()`。

`relock()` 可能阻塞。它不是 `tryLock()`，也没有超时参数。

### 7.3 不提供锁升级或降级

`QMutexLocker<QMutex>` 只调用 `Mutex::lock()` / `unlock()`。它不会把普通 mutex 变成读写锁，也不能把 `QReadLocker` 升级为写锁。读写场景应直接使用 `QReadLocker`、`QWriteLocker` 或底层 `QReadWriteLock`。

## 8. 模板参数和可用锁类型

模板参数 `Mutex` 至少要提供与 locker 所需操作兼容的接口：

```cpp
mutex->lock();
mutex->unlock();
```

常见类型包括：

```cpp
QMutex mutex;
QMutexLocker<QMutex> locker(&mutex);

QRecursiveMutex recursiveMutex;
QMutexLocker<QRecursiveMutex> recursiveLocker(&recursiveMutex);
```

`QRecursiveMutex` 允许同一线程重复取得同一把锁，但这不会让普通 `QMutex` 变成递归锁，也不会自动修复递归调用造成的设计问题。

构造和 `relock()` 的异常规格取决于 `Mutex::lock()` 是否不抛异常；`unlock()` 和状态查询在 Qt 头文件中按不抛异常路径实现。自定义 Mutex 类型应保持清晰的 `lock()` / `unlock()` 契约，不要在锁管理器已认为成功后让 `unlock()` 抛出异常。

## 9. 并发边界和常见死锁

### 9.1 临界区越小越好

锁住共享状态的读写即可，不要把网络请求、磁盘 I/O、长时间计算或用户回调无条件放在锁内。

### 9.2 统一锁顺序

如果线程 A 按 `mutexA -> mutexB` 加锁，线程 B 按 `mutexB -> mutexA` 加锁，两个 `QMutexLocker` 仍然会形成死锁。RAII 只保证释放路径，不决定锁顺序。

### 9.3 不要在持锁期间等待依赖当前锁的事件

例如持锁后等待另一个线程完成，而另一个线程需要同一把锁才能结束；这种等待与 locker 的析构都无法自动打破死锁。

### 9.4 不要把 `mutex()` 返回的指针当作所有权

`mutex()` 只是返回关联对象地址。它不增加引用计数，也不延长对象生命周期。

## 10. 逐项 API 语义

### 10.1 `QMutexLocker(Mutex *mutex)`

```cpp
explicit QMutexLocker(Mutex *mutex) noexcept(...);
```

- 保存传入的 mutex 指针；
- 指针非空时立即调用 `lock()`；
- 成功进入构造后的状态是已锁定；
- 传入 `nullptr` 时构造一个未锁定的非活动 locker；
- 不取得 mutex 所有权；
- mutex 必须在 locker 使用期间保持有效。

它没有默认构造函数。需要“暂不关联锁”时只能传 `nullptr`，但这样创建的对象不能安全地通过 `relock()` 变成有效锁。

### 10.2 `QMutexLocker(QMutexLocker &&other)`

```cpp
QMutexLocker(QMutexLocker &&other) noexcept;
```

移动 mutex 指针和锁定状态。移动后的 `other` 不再负责解锁，通常表现为 `mutex() == nullptr` 且 `isLocked() == false`。

### 10.3 `~QMutexLocker()`

```cpp
~QMutexLocker();
```

如果当前状态为已锁定，析构时调用 `unlock()`；否则不做解锁。它不销毁 mutex，也不改变其他 locker 的状态。

### 10.4 `isLocked() const`

```cpp
bool isLocked() const noexcept;
```

返回当前 locker 是否认为自己持有锁。它反映 locker 的状态，不是对 mutex 全局状态的查询，也不表示其他线程是否等待该 mutex。

### 10.5 `mutex() const`

```cpp
Mutex *mutex() const;
```

返回关联的 mutex 指针。解锁后仍返回该指针；移动源对象通常返回 `nullptr`。返回值不转移所有权。

### 10.6 `unlock()`

```cpp
void unlock() noexcept;
```

释放当前 locker 持有的锁，并把 `isLocked()` 设为 `false`。前置条件是 locker 当前已锁定；重复调用违反前置条件。

### 10.7 `relock()`

```cpp
void relock() noexcept(...);
```

对同一个关联 mutex 再次调用 `lock()`，并把状态设为已锁定。前置条件是当前未锁定且 `mutex()` 非空；可能阻塞，没有超时或失败返回值。

### 10.8 `swap(QMutexLocker &other)`

```cpp
void swap(QMutexLocker &other) noexcept;
```

交换两个 locker 的 mutex 指针和锁定状态。它不执行新的加锁或解锁动作，交换后每个 locker 接管另一方原先的管理责任。

### 10.9 `operator=(QMutexLocker &&other)`

```cpp
QMutexLocker &operator=(QMutexLocker &&other) noexcept;
```

移动赋值。复制赋值不可用。目标对象原先管理的锁会通过内部的交换和临时对象清理，源对象转为非活动状态。

## 11. 实际使用模式

### 11.1 多个返回路径

```cpp
bool Cache::remove(const QString &key)
{
    QMutexLocker locker(&mutex);
    const auto it = values.find(key);
    if (it == values.end())
        return false;

    values.erase(it);
    return true;
}
```

### 11.2 只保护快照，锁外执行慢操作

```cpp
QByteArray Snapshot::take()
{
    QMutexLocker locker(&mutex);
    const QByteArray result = data;
    return result;
}
```

返回前析构会解锁；复制或移动快照本身不需要继续持锁。

### 11.3 使用 `std::unique_lock` 风格的手动控制

如果业务需要“先锁住、暂时解锁、再锁回”，可以使用 `unlock()` / `relock()`，但应让这段状态机保持短小可读。需要超时获取锁时，改用 `QMutex::tryLock()`，而不是先构造 `QMutexLocker` 再想办法取消阻塞。

## 12. 常见错误

### 12.1 传入局部 mutex 后返回 locker

```cpp
// 错误：返回后 mutex 已销毁
QMutexLocker<QMutex> badLocker()
{
    QMutex local;
    return QMutexLocker<QMutex>(&local);
}
```

locker 返回时引用已经失效的对象，后续析构或操作都是未定义行为。

### 12.2 解锁后继续读写共享数据

`unlock()` 只是结束保护，不会冻结数据。解锁后必须把数据复制到局部快照，或者先 `relock()` 再访问。

### 12.3 对空 locker 调用 `relock()`

传入 `nullptr` 只适合表达“当前没有锁”。它不提供可重新关联 mutex 的 API；需要关联新 mutex 时应销毁旧 locker 并创建新对象。

### 12.4 误以为 `isLocked()` 表示全局锁状态

它只表示当前 locker 的布尔状态。另一个线程是否持有同一个 mutex、是否有等待者，都不能通过它判断。

### 12.5 让锁跨越用户回调

持锁调用可能再次进入本对象或调用外部代码，容易出现死锁、递归锁依赖或观察到半更新状态。先复制必要数据，再在锁外回调通常更稳妥。

## API 速查表
| API | 作用 | 使用时重点注意 |
| --- | --- | --- |
| `QMutexLocker(Mutex *mutex)` | 保存 mutex，并在非空时立即加锁 | 构造点可能阻塞；locker 不拥有 mutex；`nullptr` 产生非活动 locker |
| `QMutexLocker(QMutexLocker &&other)` | 转移 mutex 指针和锁定责任 | Qt 6.4 起提供；源对象不再负责解锁 |
| `~QMutexLocker()` | 对仍锁定的 locker 自动解锁 | 不销毁 mutex；依赖关联 mutex 仍然有效 |
| `isLocked()` | 查询当前 locker 是否处于已锁定状态 | 不是 mutex 的全局状态查询 |
| `mutex()` | 返回关联的 `Mutex *` | 不转移所有权；解锁后通常仍返回原指针 |
| `unlock()` | 提前释放当前锁 | 要求当前已锁定；调用后临界区结束 |
| `relock()` | 重新锁定同一个 mutex | 要求未锁定且 mutex 非空；可能阻塞，无超时 |
| `swap(other)` | 交换两套管理状态 | 不新建锁关系，但会交换解锁责任 |
| `operator=(QMutexLocker &&)` | 移动赋值并清理目标旧状态 | 不可复制；目标原锁不能泄漏 |

## 14. 一句话总结

`QMutexLocker` 是“构造即锁定、析构即释放”的互斥锁作用域管理器：它借用而不拥有 mutex，只能移动不能复制；使用时最重要的是保证 mutex 生命周期、控制临界区范围、遵守锁顺序，并正确理解 `unlock()` / `relock()` 的状态前置条件。
