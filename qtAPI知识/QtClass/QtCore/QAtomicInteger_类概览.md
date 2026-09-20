# QAtomicInteger 深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QAtomicInteger>`  
> 模块：`Qt6::Core`  
> 定位：跨平台整数原子操作模板  
> 常用便捷类型：`QAtomicInt`，即 `QAtomicInteger<int>`

## 它解决什么问题

`QAtomicInteger<T>` 为一个整数提供不可分割的读取、写入、比较交换、加减和位运算。它解决的是“多个线程同时访问**同一个整数状态**时，不发生数据竞争，也不会把一次读改写拆开”的问题。

典型用途包括：

- 任务取消标志、初始化状态、简单状态机。
- 并发统计、分配连续序号。
- 隐式共享类的引用计数。
- 位标志的原子置位、清位和交换。
- 无锁算法中的 compare-and-swap 循环。

它不是数据结构或事务系统。原子地更新一个 `int` 不会让“检查库存、扣库存、写订单”变成整体原子，也不能自动保护由多个字段构成的不变量。此类需求应使用 `QMutex`、`QReadWriteLock`、消息队列，或经过严格验证的无锁算法。

## 可用的整数类型与可移植性

模板参数 `T` 必须是 C++ 整数类型，例如 `bool`、有符号/无符号整数、`qint8` 到 `qint64`、`char8_t`、`char16_t`、`char32_t`、`qintptr` 等。

Qt 保证 8 位、16 位、32 位和指针大小的实例在所有平台都可用。64 位以及依赖平台的 `long` 是否可用，受编译器和 CPU 架构影响；特别是在 32 位目标上，编译前应检查 `Q_ATOMIC_INT64_IS_SUPPORTED`。

```cpp
QAtomicInteger<quint32> flags = 0;
QAtomicInteger<qintptr> handleBits = 0;
QAtomicInt pending = 0; // QAtomicInteger<int> 的便捷类型
```

## 最小使用：用 release/acquire 发布状态

```cpp
#include <QAtomicInteger>

struct SharedResult
{
    QByteArray payload;
    QAtomicInteger<int> ready = 0;
};

void producer(SharedResult &result)
{
    result.payload = "finished";
    result.ready.storeRelease(1);
}

bool consumer(SharedResult &result)
{
    if (!result.ready.loadAcquire())
        return false;

    use(result.payload);
    return true;
}
```

生产者先写 `payload`，再 release 写入 `ready`；消费者 acquire 读取到 `ready == 1` 后，才读取 `payload`。这种配对表达的是一个清晰的发布/获取协议。

若整数只是独立统计值，例如“已完成任务数”，并不借它发布其他对象状态，`fetchAndAddRelaxed(1)` 通常更合适。不要因为 acquire/release 名称听起来更强就到处使用它们，正确内存序取决于数据依赖。

## 四种内存序

- `Relaxed`：只保证该整数读写不可分割，不约束周围普通内存访问的重排。
- `Acquire`：本操作之后的内存访问不能移到它之前，通常用于观察到发布状态后读取数据。
- `Release`：本操作之前的内存访问不能移到它之后，通常用于发布状态。
- `Ordered`：同时具备 acquire 和 release 的约束。

所有 CAS、fetch 操作都提供这四种后缀。`ref()` 与 `deref()` 使用 ordered 语义。普通运算符尽力使用顺序一致语义，无法做到时采用文档定义的较强替代；协议复杂时直接写明 `Relaxed`、`Acquire`、`Release` 或 `Ordered` 更容易评审。

## 核心操作模型

### 1. 比较交换：把“检查后修改”合成一次原子操作

```cpp
bool tryClaim(QAtomicInteger<int> &state)
{
    int expected = 0;
    return state.testAndSetAcquire(expected, 1);
}
```

只有当前值仍为 `0` 时，才会写入 `1` 并返回 `true`。带 `currentValue` 参数的重载在失败时会把实际观察到的值写回该变量，适合循环重试：

```cpp
int current = counter.loadRelaxed();
while (current > 0) {
    if (counter.testAndSetOrdered(current, current - 1, current))
        return;
}
```

### 2. fetch 操作：返回旧值，再完成更新

```cpp
const int ticket = nextTicket.fetchAndAddRelaxed(1);
```

`fetchAndAdd...()` 返回加法前的旧值，因此适合分配唯一编号。`fetchAndStore...()` 返回旧值再写新值；`fetchAndSub...()`、`fetchAndOr...()`、`fetchAndAnd...()`、`fetchAndXor...()` 同样返回更新前的值。

若只关心更新后的值，`++atomic`、`atomic += value` 等便利运算符可读性更好；需要保留旧值时使用 fetch 版本。

### 3. 引用计数：原子计数不是生存期证明

```cpp
if (!data->ref.deref())
    delete data;
```

`ref()` 递增后返回是否非零；`deref()` 递减后返回是否仍非零。通常 `deref()` 返回 `false` 表示刚减到零，当前线程承担销毁责任。

这只解决计数的竞争，不自动阻止其他线程在对象被删除后使用历史裸指针。实现共享对象时还必须设计指针发布、引用获取和析构之间的完整生命周期协议。

## native 与 wait-free

`is...Native()` 表示当前平台是否原生支持某类原子操作；`is...WaitFree()` 表示该类操作是否可在有界步骤内完成，不依赖锁或无界重试。

这些查询面向跨 CPU 架构的底层并发库优化。Qt 仍保证 API 的原子正确性，即使某项不是 native 或 wait-free；普通业务代码不应该以“不是 wait-free”为由退回普通非原子变量。

编译期宏形式为：

```text
Q_ATOMIC_INTnn_OPERATION_IS_HOW
```

其中 `nn` 是位数，`OPERATION` 是 `REFERENCE_COUNTING`、`TEST_AND_SET`、`FETCH_AND_STORE` 或 `FETCH_AND_ADD`，`HOW` 为 `ALWAYS_NATIVE`、`SOMETIMES_NATIVE`、`NOT_NATIVE` 或 `WAIT_FREE`。同一操作的前三个 native 宏中恰有一个会被定义；空 `nn` 的旧宏等价于 32 位版本。

## 自旋与 `qYieldCpu()`

Qt 6.7 引入 `qYieldCpu()`。它向处理器发出短暂的硬件层退让提示，但不会像 `QThread::yieldCurrentThread()` 那样把线程交还给操作系统调度器。

它只适合高吞吐、预期另一个线程很快修改原子变量的短自旋循环。长时间等待应使用 `QWaitCondition`、事件循环或其他阻塞机制；无限自旋会浪费核心并造成饥饿。

## 常见误区

- 先 `load()` 再普通 `store()`，却以为整个读改写原子。使用 fetch 操作或 CAS。
- 在没有数据发布关系时随意换成 acquire/release，或反过来用 relaxed 发布复杂对象。
- 把 `deref() == false` 当作“所有线程都不可能再访问对象”的证明。
- 以为原子变量天然适合多字段业务一致性。
- 在竞争循环里无上限自旋，不做退避、让步或阻塞。
- 把 native/wait-free 查询当作正确性的前置条件。

## API 速查表

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造 | `QAtomicInteger(T value = 0)` | 以初值构造原子整数。 | 默认值为 0；引用计数通常要显式从 1 开始。 |
| 拷贝构造 | `QAtomicInteger(const QAtomicInteger<T> &other)` | 从另一个原子整数读取值并构造新对象。 | 复制的是当时观察到的数值，不会让两个原子对象共享存储。 |
| 赋值 | `operator=(const QAtomicInteger<T> &other)` | 原子读取 `other` 后写入当前对象。 | 同样只是值复制；不要误解为链接两个同步状态。 |
| 读取 | `loadRelaxed()` | 以 relaxed 内存序读取当前值。 | 适合独立计数，不能借此观察其他线程发布的数据。 |
| 读取 | `loadAcquire()` | 以 acquire 内存序读取当前值。 | 通常与另一线程的 release 写入配对。 |
| 写入 | `storeRelaxed(T)` | 以 relaxed 内存序存入新值。 | 不建立其他普通内存读写的可见性。 |
| 写入 | `storeRelease(T)` | 以 release 内存序存入新值。 | 用于发布状态；读取方需 acquire 或更强语义。 |
| 便利转换 | `operator T() const` | 以便利形式读取原子值。 | 复杂协议中优先使用显式 `load...()`，让内存序可见。 |
| 便利赋值 | `operator=(T)` | 以便利形式原子写入值。 | 需要明确发布语义时改用 `storeRelease()` 或其他显式 API。 |
| 引用计数 | `ref()` | 原子递增，并返回递增后是否非零。 | 使用 ordered 语义；应只用于一致的引用计数协议。 |
| 引用计数 | `refRelaxed()` | 以 relaxed 语义原子递增。 | 仅在外部已保证对象可见性和生命周期时使用。 |
| 引用计数 | `deref()` | 原子递减，并返回递减后是否非零。 | 返回 `false` 通常表示当前线程负责销毁最后一个引用。 |
| CAS | `testAndSetRelaxed(expected, desired)` | 值相等时以 relaxed 语义替换。 | 只适合不发布其他数据的状态转换。 |
| CAS | `testAndSetAcquire(expected, desired)` | 值相等时以 acquire 语义替换。 | 成功后要读取关联数据时使用。 |
| CAS | `testAndSetRelease(expected, desired)` | 值相等时以 release 语义替换。 | 成功时发布此前的数据写入。 |
| CAS | `testAndSetOrdered(expected, desired)` | 值相等时以 acquire+release 语义替换。 | 用于既读取旧状态又发布新状态的 CAS 协议。 |
| CAS 重载 | `testAndSetRelaxed/Acquire/Release/Ordered(expected, desired, currentValue)` | CAS 失败时把实际值写回 `currentValue`。 | 适合重试循环；每次失败后都要重新判断更新后的值。 |
| 交换 | `fetchAndStoreRelaxed/Acquire/Release/Ordered(T newValue)` | 原子写入 `newValue` 并返回旧值。 | 四个后缀只差内存序；不要把返回的旧值误作新值。 |
| 加法 | `fetchAndAddRelaxed/Acquire/Release/Ordered(T valueToAdd)` | 原子加法并返回旧值。 | 分配序号常用 relaxed 版本；发布协议按依赖选择后缀。 |
| 减法 | `fetchAndSubRelaxed/Acquire/Release/Ordered(T valueToSub)` | 原子减法并返回旧值。 | 不会阻止减到负数；需要下限约束时使用 CAS 循环。 |
| 位或 | `fetchAndOrRelaxed/Acquire/Release/Ordered(T valueToOr)` | 原子按位或并返回旧值。 | 适合置位 flag；不同 bit 的组合不自动构成事务。 |
| 位与 | `fetchAndAndRelaxed/Acquire/Release/Ordered(T valueToAnd)` | 原子按位与并返回旧值。 | 常用于清位或掩码收缩；确认掩码不会误清其他状态。 |
| 位异或 | `fetchAndXorRelaxed/Acquire/Release/Ordered(T valueToXor)` | 原子按位异或并返回旧值。 | 适合翻转状态；并发重复翻转的最终结果可能不直观。 |
| 便利加减 | `operator++()`、`operator++(int)`、`operator--()`、`operator--(int)`、`operator+=()`、`operator-=()` | 原子更新并返回更新后的或更新前的值，语义与普通前后置运算一致。 | 需要精确旧值与内存序时使用 `fetchAndAdd...` 或 `fetchAndSub...`。 |
| 便利位运算 | 按位或赋值、`operator&=()`、`operator^=()` | 原子位运算并返回更新后的值。 | 本行的“按位或赋值”对应 C++ 的竖线赋值运算符，避免在 Markdown 表格中被误解析。 |
| 能力查询 | `isReferenceCountingNative()`、`isReferenceCountingWaitFree()` | 查询引用计数操作的原生和 wait-free 能力。 | 性能特征，不影响 Qt 已保证的原子语义。 |
| 能力查询 | `isTestAndSetNative()`、`isTestAndSetWaitFree()` | 查询 CAS 操作的原生和 wait-free 能力。 | 用于跨架构底层优化，不替代算法正确性验证。 |
| 能力查询 | `isFetchAndStoreNative()`、`isFetchAndStoreWaitFree()` | 查询原子交换操作的原生和 wait-free 能力。 | 只在性能敏感基础设施中据此调整策略。 |
| 能力查询 | `isFetchAndAddNative()`、`isFetchAndAddWaitFree()` | 查询加减和位运算类操作的原生和 wait-free 能力。 | 不要因结果为 false 改用普通非原子变量。 |
| 非成员 | `qYieldCpu()` | 对短暂自旋循环发出硬件层 CPU 退让提示。 | Qt 6.7 引入；不是阻塞等待，也不是 `QThread::yieldCurrentThread()`。 |
| 宏 | `Q_ATOMIC_INTnn_IS_SUPPORTED` | 表示指定位宽的原子整数是否受当前编译器与架构支持。 | 8、16、32 位始终可用；32 位目标上的 64 位尤其需要检查。 |
| 宏 | `Q_ATOMIC_INTnn_REFERENCE_COUNTING_IS_ALWAYS_NATIVE`、`...SOMETIMES_NATIVE`、`...NOT_NATIVE`、`...WAIT_FREE` | 描述引用计数原子操作的平台能力。 | `nn` 是 8、16、32、64；前三个 native 宏中恰有一个定义。 |
| 宏 | `Q_ATOMIC_INTnn_TEST_AND_SET_IS_ALWAYS_NATIVE`、`...SOMETIMES_NATIVE`、`...NOT_NATIVE`、`...WAIT_FREE` | 描述比较交换操作的平台能力。 | 仅作为编译期性能特征查询，不改变 API 可调用性。 |
| 宏 | `Q_ATOMIC_INTnn_FETCH_AND_STORE_IS_ALWAYS_NATIVE`、`...SOMETIMES_NATIVE`、`...NOT_NATIVE`、`...WAIT_FREE` | 描述原子交换操作的平台能力。 | 空 `nn` 的旧式宏等价于 32 位版本。 |
| 宏 | `Q_ATOMIC_INTnn_FETCH_AND_ADD_IS_ALWAYS_NATIVE`、`...SOMETIMES_NATIVE`、`...NOT_NATIVE`、`...WAIT_FREE` | 描述原子加法及相关 fetch 运算的平台能力。 | wait-free 宏只有在 always-native 且操作 wait-free 时定义。 |

## 一句话总结

`QAtomicInteger<T>` 是单个整数状态的原子工具箱：用 fetch 操作做不可分割更新，用 CAS 处理“检查后修改”，用 acquire/release 建立明确的跨线程发布关系。它很锋利，但不能代替业务锁、对象生命周期设计或完整的并发协议。
