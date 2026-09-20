# QAtomicPointer 深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QAtomicPointer>`  
> 模块：`Qt6::Core`  
> 定位：跨平台原子读写裸指针值的模板

## 它解决什么问题

`QAtomicPointer<T>` 让多个线程可以原子地读取、替换或比较一个 `T *` 指针值。它适合实现“当前对象指针”“一次性初始化指针”“无锁结构的 head 指针”“环形缓冲区读写游标”等低层并发状态。

它只保证**指针槽位中的地址值**以原子方式变化：

```text
QAtomicPointer<Config>
  └─ 原子保存一个 Config * 地址
```

它不拥有 `T`，不增加引用计数，不会在替换指针时自动删除旧对象，也不保证 `loadAcquire()` 得到的对象仍会存活到下一行代码。对象生存期、回收策略和 ABA 防护必须由调用方另行设计。

这一区别很关键：原子指针不是智能指针，也不是自动线程安全的对象访问器。

## 典型场景

- 发布初始化完成后的只读配置或查找表。
- 使用固定生命周期对象的全局服务指针。
- 无锁算法中的比较并交换（CAS）状态。
- 指向数组元素的原子游标，配合 `fetchAndAdd...()` 分配位置。
- 需要替换当前对象地址，但旧对象由其他明确机制回收的系统。

不适合的场景：

- 希望“读到指针就自动拥有对象”。用 `QSharedPointer`、锁或专门的 epoch/hazard-pointer 回收机制。
- 普通 QObject 生命周期管理。QObject 父子关系和线程归属不能被原子指针替代。
- 未经验证的无锁栈、队列或链表。CAS 只是构件，ABA 与内存回收往往才是难点。

## 最小使用：发布一个长期存活的对象

```cpp
#include <QAtomicPointer>

struct LookupTable
{
    int lookup(int key) const;
};

QAtomicPointer<LookupTable> currentTable = nullptr;

void publishTable(LookupTable *table)
{
    // table 的字段必须先全部初始化。
    currentTable.storeRelease(table);
}

int lookup(int key)
{
    LookupTable *table = currentTable.loadAcquire();
    return table ? table->lookup(key) : -1;
}
```

这段代码仅在 `LookupTable` 在所有读取线程用完前始终存活时才成立，例如对象进程期不回收，或外层持有读锁、引用计数、epoch 保护。若发布线程随后 `delete oldTable`，另一个线程可能刚取得旧地址就解引用，形成悬挂访问；release/acquire 不能修复这个问题。

## 最重要的边界：原子地址不等于安全对象

以下代码仍然危险：

```cpp
Widget *widget = currentWidget.loadAcquire();
delete widget; // 另一个线程此刻可能也刚 load 到相同地址
```

即使把 `delete` 前的槽位清为 `nullptr`，已经读取旧地址的线程也不会自动知道对象将被释放。常见安全方案包括：

- 所有读取和销毁都受同一把锁保护。
- 使用引用计数智能指针，并设计安全的“取得一份引用”流程。
- 使用 epoch-based reclamation、hazard pointer 或 RCU 类方案延迟回收。
- 对象固定到应用结束时才释放。

此外，CAS 只比较地址。如果地址先从 A 变成 B，又因内存复用变回 A，CAS 可能误以为状态从未改变，这就是 ABA 问题。需要无锁删除节点时，通常要结合版本号、标记指针或专用内存回收方案。

## 内存序与 `QAtomicInteger` 相同

`QAtomicPointer` 的 `Relaxed`、`Acquire`、`Release`、`Ordered` 含义与 `QAtomicInteger` 一致：

- `Relaxed`：仅保证地址读取或替换本身原子。
- `Acquire`：读取到发布指针后，后续内存读取不会被重排到原子读取之前。
- `Release`：指针发布前的内存写入不会被重排到原子写入之后。
- `Ordered`：同时具有 acquire 与 release 约束。

`storeRelease(pointer)` 配合 `loadAcquire()` 是常见发布模式；它使读者在观察到新指针后能看到发布前对该对象做的初始化。它仍不提供对象回收保障。

## `testAndSet...()`：比较指针再替换

```cpp
Node *expected = head.loadAcquire();
for (;;) {
    Node *next = makeCandidate(expected);
    if (head.testAndSetOrdered(expected, next, expected))
        break;
    delete next; // 此候选基于过期 expected 构造，重新计算
}
```

当当前指针等于 `expected` 时，`testAndSet...()` 原子写入新地址并返回 `true`；否则不写入并返回 `false`。带 `currentValue` 引用参数的重载会在失败时把实际值写回，避免循环中额外 `load()` 一次。

不过示例只展示 CAS 的重试形状，不代表链表节点的回收已安全。若 `makeCandidate()` 或其他线程会访问、删除旧节点，仍要处理生命周期和 ABA。

## `fetchAndStore...()`：替换并取得旧指针

```cpp
Connection *old = currentConnection.fetchAndStoreRelease(replacement);
```

它会原子写入 `replacement`，并返回替换前的旧指针。旧指针的所有权不会自动转移给某个人，也不会自动删除；是否能立即释放完全取决于读取方是否还可能使用它。

这类 API 常用于“交换当前版本”，但安全回收往往比交换动作本身复杂。若没有成熟回收协议，优先用锁把读取、替换、销毁放在同一个受保护区域。

## `fetchAndAdd...()`：原子移动数组指针

```cpp
QAtomicPointer<int> cursor(buffer);
int *slot = cursor.fetchAndAddRelaxed(1);
*slot = value;
```

该系列先返回旧指针，再按 `qptrdiff valueToAdd` 做指针加法。它只应作用于真实数组内的元素位置，并确保不会越过有效数组范围。不能把它当作任意对象地址的“字节偏移器”，也不负责检查容量或协调多线程对数组元素的写入。

## 平台能力宏

`isTestAndSetNative()`、`isFetchAndStoreNative()`、`isFetchAndAddNative()` 及对应的 `WaitFree` 函数用于查询平台特征。编译期也提供三类宏：

- `Q_ATOMIC_POINTER_TEST_AND_SET_IS_...`
- `Q_ATOMIC_POINTER_FETCH_AND_STORE_IS_...`
- `Q_ATOMIC_POINTER_FETCH_AND_ADD_IS_...`

每类都有 `ALWAYS_NATIVE`、`SOMETIMES_NATIVE`、`NOT_NATIVE` 和 `WAIT_FREE` 变体。它们适用于跨平台并发基础设施的性能决策，不影响 Qt 对操作原子性的保证。

## 常见误区

- 把 `QAtomicPointer<T>` 当成拥有 `T` 的智能指针。
- `loadAcquire()` 后立刻解引用，却没有任何防止对象被另一线程销毁的机制。
- 用 release/acquire 解决对象回收问题。它只处理可见性与重排序。
- 在链表 CAS 中忽略 ABA 和节点复用。
- 对单个非数组对象调用 `fetchAndAdd...()`，或让指针越过数组边界。
- 用 `fetchAndStore...()` 替换后立刻删除旧对象，没有确认读者是否还持有旧地址。

## API 速查表

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造 | `QAtomicPointer(T *value = nullptr)` | 以初始地址构造原子指针槽位。 | 不取得 `value` 所指对象的所有权；默认值为 `nullptr`。 |
| 拷贝构造 | `QAtomicPointer(const QAtomicPointer<T> &other)` | 原子读取 `other` 的当前地址并构造新槽位。 | 复制的是地址值，不是对象，也不增加对象引用计数。 |
| 赋值 | `operator=(const QAtomicPointer<T> &other)` | 原子读取另一个槽位地址后写入当前槽位。 | 不会转移或共享对象所有权。 |
| 读取 | `loadRelaxed()` | 以 relaxed 内存序原子读取地址。 | 地址读取后仍可能被其他线程替换或回收，不能直接视为安全对象句柄。 |
| 读取 | `loadAcquire()` | 以 acquire 内存序原子读取地址。 | 可配对 `storeRelease()` 观察初始化数据，但不延长对象生命周期。 |
| 写入 | `storeRelaxed(T *newValue)` | 以 relaxed 内存序原子写入地址。 | 不发布对象初始化，也不回收被替换的旧对象。 |
| 写入 | `storeRelease(T *newValue)` | 以 release 内存序原子发布地址。 | 读取端应使用 acquire；对象回收需要额外同步。 |
| CAS | `testAndSetRelaxed(expected, desired)` | 当前地址等于期望地址时，以 relaxed 语义替换。 | 仅适合独立地址状态，不建立对象字段可见性。 |
| CAS | `testAndSetAcquire(expected, desired)` | 成功时以 acquire 语义替换地址。 | 成功后要读取与旧状态关联的数据时使用。 |
| CAS | `testAndSetRelease(expected, desired)` | 成功时以 release 语义替换地址。 | 用于发布 `desired` 指向且已初始化的对象。 |
| CAS | `testAndSetOrdered(expected, desired)` | 成功时以 acquire+release 语义替换地址。 | 适合同时消费旧状态并发布新状态的 CAS 协议。 |
| CAS 重载 | `testAndSetRelaxed/Acquire/Release/Ordered(expected, desired, currentValue)` | CAS 失败时将实际地址写回 `currentValue`。 | 重试循环优先使用，避免额外 load；失败路径的内存序由所选重载决定。 |
| 原子交换 | `fetchAndStoreRelaxed/Acquire/Release/Ordered(T *newValue)` | 原子写入新地址并返回旧地址。 | 返回旧地址不代表可立即 delete；必须先完成读者安全回收。 |
| 原子指针加法 | `fetchAndAddRelaxed/Acquire/Release/Ordered(qptrdiff valueToAdd)` | 原子按元素偏移移动指针并返回旧地址。 | 仅用于合法数组范围内的 `T *` 算术；检查容量和元素并发访问。 |
| 能力查询 | `isTestAndSetNative()`、`isTestAndSetWaitFree()` | 查询 CAS 是否原生或 wait-free。 | 是性能特征，不解决 ABA、回收或算法正确性。 |
| 能力查询 | `isFetchAndStoreNative()`、`isFetchAndStoreWaitFree()` | 查询原子交换是否原生或 wait-free。 | 对普通应用通常无需据此分支。 |
| 能力查询 | `isFetchAndAddNative()`、`isFetchAndAddWaitFree()` | 查询原子指针加法是否原生或 wait-free。 | 仅在跨架构底层优化时使用。 |
| 宏 | `Q_ATOMIC_POINTER_TEST_AND_SET_IS_ALWAYS_NATIVE`、`...SOMETIMES_NATIVE`、`...NOT_NATIVE`、`...WAIT_FREE` | 描述 CAS 的编译期平台能力。 | 三个 native 状态宏中恰有一个定义；wait-free 另行表示。 |
| 宏 | `Q_ATOMIC_POINTER_FETCH_AND_STORE_IS_ALWAYS_NATIVE`、`...SOMETIMES_NATIVE`、`...NOT_NATIVE`、`...WAIT_FREE` | 描述原子交换的编译期平台能力。 | 不改变 API 对地址原子读写的语义保证。 |
| 宏 | `Q_ATOMIC_POINTER_FETCH_AND_ADD_IS_ALWAYS_NATIVE`、`...SOMETIMES_NATIVE`、`...NOT_NATIVE`、`...WAIT_FREE` | 描述原子指针加法的编译期平台能力。 | 仍须由调用方保证指针算术与数组边界合法。 |

## 一句话总结

`QAtomicPointer<T>` 能原子地发布和替换地址，但它不管理对象。用它之前先回答两个比 API 更重要的问题：读取线程如何保证对象还活着，旧地址何时才能安全回收；没有这两个答案，原子指针只会把竞态藏得更深。
