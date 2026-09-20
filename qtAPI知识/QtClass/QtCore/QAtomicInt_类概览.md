# QAtomicInt 深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QAtomicInt>`  
> 模块：`Qt6::Core`  
> 继承：`QAtomicInteger<int> -> QAtomicInt`  
> 定位：固定为 `int` 的跨平台原子整数

## 它解决什么问题

`QAtomicInt` 是 `QAtomicInteger<int>` 的便捷类型。它让多个线程可以对同一个 `int` 做不可分割的读取、写入、加减、比较并交换等操作，不需要先为“单个整数状态”加一把互斥锁。

它适合表示简单的并发状态：

- 取消标记、停止标记、一次性初始化状态。
- 并发任务数、正在运行的工作数、无锁统计计数器。
- 自己实现的隐式共享对象引用计数。
- 简单自旋协议中的状态字。

它不解决多个字段必须一起保持一致的问题。例如 `count` 和 `sum` 要同时更新、检查后再执行、从队列取元素并修改其他状态，单独给两个 `QAtomicInt` 并不能保证整体原子性；这类业务不变量仍需要互斥锁、条件变量或经过完整设计的无锁算法。

```text
QAtomicInteger<int>
  └─ QAtomicInt
```

Qt 文档对 `QAtomicInt` 的定义非常直接：它等价于 `QAtomicInteger<int>`。除了构造函数名称以外，其余能力和内存序语义都来自基类。

## 最小使用：发布一个停止请求

```cpp
#include <QAtomicInt>

class Worker
{
public:
    void requestStop()
    {
        m_stopRequested.storeRelease(1);
    }

    void run()
    {
        while (!m_stopRequested.loadAcquire()) {
            doOneUnitOfWork();
        }
    }

private:
    QAtomicInt m_stopRequested = 0;
};
```

这里 `storeRelease(1)` 先发布停止请求前的写入，`loadAcquire()` 在读取到该值后阻止后续读取被重排到原子读取之前。若状态只作为独立计数、不携带其他数据的发布关系，`loadRelaxed()`、`fetchAndAddRelaxed()` 往往已足够，但必须由并发设计证明这一点。

## 原子性不等于完整线程安全

下面的写法没有数据竞争，但仍可能违反业务逻辑：

```cpp
if (tickets.loadRelaxed() > 0)
    tickets.fetchAndSubRelaxed(1);
```

两个线程都可能先读到正数，然后都减一。要表达“仅当当前值大于 0 时减一”，需要 `testAndSet...()` 组成 compare-and-swap 循环：

```cpp
bool tryTakeTicket(QAtomicInt &tickets)
{
    int current = tickets.loadAcquire();
    while (current > 0) {
        if (tickets.testAndSetOrdered(current, current - 1, current))
            return true;
        // 失败时 current 已被更新为实际观察到的值，继续判断。
    }
    return false;
}
```

这类循环仍要考虑公平性、饥饿、异常路径和高竞争下的性能。能用 `QMutex` 把业务逻辑写得更清晰时，锁通常是更好的工程选择。

## 内存序：四个词分别是什么意思

`QAtomicInt` 的低层 API 用后缀表达内存序：

- `Relaxed`：只保证这一次整数读写本身原子，不建立与其他内存读写的先后关系。
- `Acquire`：当前原子操作之后的内存访问不能被重排到它之前；常用于读取发布标记。
- `Release`：当前原子操作之前的内存访问不能被重排到它之后；常用于写入发布标记。
- `Ordered`：同时具备 Acquire 与 Release 约束。

`ref()`、`deref()` 采用 ordered 语义。普通运算符和赋值会尽量使用顺序一致语义，平台做不到时使用其文档规定的较强可用替代语义；需要精确控制时，应直接调用带内存序后缀的函数。

不要把 `Acquire` 理解为“原子加载更安全”、把 `Release` 理解为“原子存储更安全”。它们解决的是与**其他内存访问**的可见性和重排序关系，必须成对地服务于一个明确的发布/获取协议。

## 常见操作怎么选

### 读取与写入

```cpp
int value = counter.loadRelaxed();
counter.storeRelease(0);
```

- 独立统计值：通常使用 relaxed。
- 发布初始化完成、停止请求、指针或对象状态前后存在额外数据依赖：使用 release 写、acquire 读。

### fetch-and-add：拿到旧值再更新

```cpp
const int previous = pending.fetchAndAddRelaxed(1);
```

返回的是**更新前**的值。若只需要自增后的新值，可以用 `++pending`；若需要给本线程分配唯一序号，旧值正是想要的结果。

`fetchAndSub...`、`fetchAndOr...`、`fetchAndAnd...`、`fetchAndXor...` 同理：先返回旧值，再完成相应的原子运算。

### `ref()` / `deref()`：只用于引用计数协议

```cpp
if (!data->ref.deref())
    delete data;
```

`deref()` 返回的是“递减后是否仍非零”。因此返回 `false` 表示刚刚变成零，当前线程负责销毁对象。引用计数初值、增加和减少必须遵循同一套所有权协议；原子计数本身不会阻止对象在某个线程删除后，另一个线程继续通过旧裸指针访问它。

## 平台能力与 wait-free

所有公开原子 API 都能提供原子语义，但平台实现不一定都是单条硬件指令，也不保证 wait-free。静态函数如 `isFetchAndAddNative()`、`isTestAndSetWaitFree()` 可用于查询当前 `int` 操作是否原生或 wait-free。

- **native**：处理器或平台原生支持该类原子操作。
- **wait-free**：操作在有界步骤内完成，不通过锁或无界重试循环等待。

这些能力查询只在你写高频无锁基础设施、跨架构性能代码时才有价值。普通应用不应根据它们随意切换到不正确的非原子备选实现。

## 常见误区

- 把 `QAtomicInt` 当成“任何并发代码都不需要锁”的替代品。
- 使用 `load()` 后再普通计算和 `store()`，却期待整个读改写仍原子；应使用 fetch 操作或 CAS 循环。
- 用 relaxed 标志发布复杂对象，然后在另一个线程读取对象字段；这缺少建立可见性的 acquire/release 协议。
- 将引用计数减到零后删除对象，却仍让其他线程保留无保护裸指针。
- 在高竞争无限自旋中不做退让、退避或阻塞，导致浪费 CPU；需要时结合 `qYieldCpu()` 或改用锁。

## API 速查表

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造 | `QAtomicInt(int value = 0)` | 以给定初值构造原子 `int`。 | 默认是 0；做引用计数时通常应显式初始化为 1，而不是依赖默认值。 |
| 读取 | `loadRelaxed()` | 以 relaxed 内存序原子读取当前值。 | 只适合独立计数或已由其他同步机制建立可见性的场景。 |
| 读取 | `loadAcquire()` | 以 acquire 内存序原子读取当前值。 | 常与另一个线程的 `storeRelease()` 配对，读取发布标记后再读取关联数据。 |
| 写入 | `storeRelaxed(int)` | 以 relaxed 内存序原子写入新值。 | 不发布此前普通内存写入。 |
| 写入 | `storeRelease(int)` | 以 release 内存序原子写入新值。 | 用于发布状态；读取方需使用 acquire 或更强语义。 |
| 便利运算 | `operator int()`、`operator=(int)` | 读取或写入原子值的简写。 | 内存序不如显式 API 一目了然；并发协议复杂时优先写出 `load...` / `store...`。 |
| 引用计数 | `ref()`、`deref()` | 原子增加或减少引用计数，并返回递增/递减后是否非零。 | `deref()` 返回 `false` 时通常删除对象；必须另行保证不会发生悬挂访问。 |
| 比较并交换 | `testAndSetRelaxed()`、`testAndSetAcquire()`、`testAndSetRelease()`、`testAndSetOrdered()` | 当前值等于期望值时原子替换为新值。 | 是“检查并更新”协议的核心；失败时不会写入，需在循环中重试或处理失败。 |
| 比较并交换 | `testAndSet...(expected, desired, currentValue)` | CAS 失败时把实际观察到的值写回 `currentValue`。 | 适合高效重试循环；循环体每次都要根据更新后的实际值重新判断条件。 |
| 取旧值再加减 | `fetchAndAdd...()`、`fetchAndSub...()` | 原子加减并返回更新前的值。 | 后缀有 Relaxed、Acquire、Release、Ordered 四种内存序；分配序号常用返回的旧值。 |
| 取旧值再位运算 | `fetchAndOr...()`、`fetchAndAnd...()`、`fetchAndXor...()` | 原子位或、位与、位异或并返回更新前的值。 | 适合位标志集合；不要把不同位的业务不变量误当成完整事务。 |
| 便利加减 | `++`、`--`、`+=`、`-=` | 原子更新并返回更新后的值。 | 需要旧值时改用 `fetchAndAdd...` 或 `fetchAndSub...`。 |
| 便利位运算 | 按位或赋值、`&=`、`^=` | 原子位运算并返回更新后的值。 | 适合简单 flag；复杂状态转换仍应采用明确 CAS 协议。 |
| 能力查询 | `isReferenceCountingNative()`、`isReferenceCountingWaitFree()` | 查询引用计数操作的原生和 wait-free 能力。 | 仅优化底层并发库时使用，不改变操作本身的原子正确性。 |
| 能力查询 | `isTestAndSetNative()`、`isTestAndSetWaitFree()` | 查询 CAS 操作的原生和 wait-free 能力。 | 不要以此决定是否省略同步；它是实现性能特征，不是正确性开关。 |
| 能力查询 | `isFetchAndStoreNative()`、`isFetchAndStoreWaitFree()` | 查询原子交换操作的原生和 wait-free 能力。 | 需要针对多个 CPU 架构优化时再检查。 |
| 能力查询 | `isFetchAndAddNative()`、`isFetchAndAddWaitFree()` | 查询原子加法类操作的原生和 wait-free 能力。 | 对于 `int` 可作为诊断信息，普通业务代码通常无需分支。 |
| 继承关系 | `QAtomicInteger<int>` | 提供本类除构造外的全部原子 API。 | 精确的每个内存序重载及宏说明见 `QAtomicInteger`；`QAtomicInt` 只固定模板参数为 `int`。 |

## 一句话总结

`QAtomicInt` 是最方便的原子 `int` 入口：用它保护单个计数器或状态字，用 acquire/release 表达明确的发布协议；一旦涉及多个状态的一致性、对象生命周期或复杂等待，就应把同步设计提升到锁、条件变量或完整无锁算法层面。
