# QAtomicScopedValueRollback 深入笔记

> 适用版本：Qt 6.7 及之后（本文按 Qt 6.11.1 编写）  
> 头文件：`#include <QAtomicScopedValueRollback>`  
> 模块：`Qt6::Core`  
> 定位：原子变量的作用域值恢复器

## 它解决什么问题

`QAtomicScopedValueRollback<T>` 是 `QScopedValueRollback` 的原子变量版本。它在构造时记录一个原子变量的旧值，在离开作用域时自动把该值写回。无论函数正常返回、提前 `return` 还是抛出异常，析构函数都会执行恢复。

它适合把“临时改变一个原子状态，结束时必须恢复”写成 RAII：

```cpp
QAtomicInt mode = 0;

void inspectTemporarily()
{
    QAtomicScopedValueRollback restore(mode, 1);
    // 此作用域内 mode 是 1。
    inspectSubsystem();
} // 自动恢复为进入函数前的 mode 值
```

它支持 `std::atomic<T>`、`QBasicAtomicInteger<T>`、`QAtomicInteger<T>`、`QAtomicInt`、`QBasicAtomicPointer<U>` 与 `QAtomicPointer<U>`。

注意这个类解决的是**异常安全的值恢复**，不是互斥、事务或“独占修改权”。原子读写不会阻止其他线程同时修改同一个变量。

## 它内部等价于什么

不指定临时值的构造大致等价于：

```cpp
T oldValue = var.load(memoryOrder);
// 析构时：
var.store(oldValue, memoryOrder);
```

指定临时值的构造大致等价于：

```cpp
T oldValue = var.exchange(temporaryValue, memoryOrder);
// 析构时：
var.store(oldValue, memoryOrder);
```

因此，第二种构造能原子地完成“保存旧值并设置临时值”；不要把它拆成普通 `load()` 加 `store()`，否则其他线程可能在两步之间观察到不完整状态。

## 最小使用：临时切换状态

```cpp
#include <QAtomicInt>
#include <QAtomicScopedValueRollback>

QAtomicInt traceMode = 0;

void collectDiagnostics()
{
    QAtomicScopedValueRollback restore(traceMode, 1);

    collectMemoryInfo();
    collectThreadInfo();
} // traceMode 恢复为进入函数前的值
```

使用类模板参数推导（CTAD）即可。不要显式写 `QAtomicScopedValueRollback<int>`；Qt 文档明确建议让编译器根据传入的原子变量自动推导 `T`。

## `commit()` 的真实含义

`commit()` 很容易被名字误导。它不会让回滚器停止工作，也不会承诺保留当前值到作用域外；它只是把“析构时要恢复的保存值”刷新为**调用 `commit()` 当下的原子变量值**。

```cpp
QAtomicInt phase = 0;

void changePhase()
{
    QAtomicScopedValueRollback restore(phase, 1);
    phase.storeRelaxed(2);

    restore.commit(); // 析构时将恢复为 2，而不是最初的 0

    phase.storeRelaxed(3);
} // 最终写回 2
```

这个语义适合“前一阶段的改动应保留，之后的临时改动仍需撤销”的流程。若你的意图是“成功后完全不回滚”，应改用更直白的控制结构或 `QScopeGuard`，而不是把 `commit()` 当作 `dismiss()`。

## 最大风险：会覆盖其他线程的更新

下面的时间线会丢失更新：

1. 线程 A 构造回滚器，记录旧值 `0`，并将变量临时设为 `1`。
2. 线程 B 将同一原子变量更新为 `2`。
3. 线程 A 离开作用域，析构函数无条件 `store(0)`。

线程 B 的 `2` 被覆盖了。调用 `commit()` 只能改变回滚目标，不会把“读取当前值”和“最后恢复”合并成事务，也不能阻止其他线程穿插写入。

因此，此类通常应满足至少一个条件：

- 变量在该作用域内逻辑上只有当前线程会修改。
- 外层已经用锁或协议保证没有其他写入者。
- 即使覆盖并发写入，业务语义也明确允许。

若要表达“仅当变量仍是我设置的临时值时才恢复”，需要使用 `testAndSet...()` 自己实现比较交换协议，不能依赖本类析构。

## 内存序如何处理

构造参数默认是 `std::memory_order_seq_cst`。该值同时用于初始读或 exchange、`commit()` 的读以及析构时的 store，但单纯 load/store 不接受每种内存序：

- 读取时传入 `release` 会降为 relaxed；传入 acquire-release 会降为 acquire。
- 写入时传入 `acquire` 会降为 relaxed；传入 acquire-release 会降为 release。
- `consume` 用于读取时保持 consume 语义。

对普通“单线程逻辑上的临时状态”场景，默认顺序一致语义最容易审查。只有在已有明确并发协议时才改用更弱内存序，并确保恢复写入也符合该协议。

## 与 `QScopedValueRollback` 的区别

- `QScopedValueRollback<T>`：管理普通变量引用；没有原子读写和内存序。
- `QAtomicScopedValueRollback<T>`：管理原子变量；构造、`commit()`、析构都通过原子 load、exchange、store 完成。

两者都不提供锁。若状态是普通局部变量，优先使用更简单的 `QScopedValueRollback`；只有被管理变量确实需要原子访问时才使用本类。

## 常见误区

- 把它当作“回滚事务”。它只恢复一个原子值，不撤销其他副作用。
- 认为 `commit()` 会禁用析构恢复。它只是更新恢复目标。
- 让多个线程在守卫存活期间随意写同一变量，最后被析构写回覆盖。
- 显式指定模板参数，导致指针与整数重载选择更难读；使用 CTAD。
- 把原子恢复当成对象生命周期保护。恢复 `QAtomicPointer` 的地址不代表指向对象仍存活。
- 在需要“条件恢复”时依赖无条件析构 store。

## API 速查表

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造 | `QAtomicScopedValueRollback(std::atomic<T> &var, std::memory_order mo = std::memory_order_seq_cst)` | 记录 `std::atomic<T>` 当前值，析构时恢复。 | 仅快照，不会立即修改 `var`；使用 CTAD，不显式写模板实参。 |
| 构造 | `QAtomicScopedValueRollback(QBasicAtomicInteger<T> &var, std::memory_order mo = std::memory_order_seq_cst)` | 记录 Qt 原子整数当前值，析构时恢复。 | `QAtomicInteger<T>` 与 `QAtomicInt` 都可匹配该重载。 |
| 构造 | `QAtomicScopedValueRollback(QBasicAtomicPointer<std::remove_pointer_t<T>> &var, std::memory_order mo = std::memory_order_seq_cst)` | 记录 Qt 原子指针当前地址，析构时恢复。 | 只恢复地址值，不管理该地址所指对象的生存期。 |
| 构造并设值 | `QAtomicScopedValueRollback(std::atomic<T> &var, T value, std::memory_order mo = std::memory_order_seq_cst)` | 原子交换为 `value`，并保存交换前的值供析构恢复。 | 适合标准库原子变量的临时状态；其他线程写入仍可能在析构时丢失。 |
| 构造并设值 | `QAtomicScopedValueRollback(QBasicAtomicInteger<T> &var, T value, std::memory_order mo = std::memory_order_seq_cst)` | 原子交换 Qt 整数变量为临时值，并保存旧值。 | 不要拆成单独 load/store；构造函数的 exchange 才是不可分割操作。 |
| 构造并设值 | `QAtomicScopedValueRollback(QBasicAtomicPointer<std::remove_pointer_t<T>> &var, T value, std::memory_order mo = std::memory_order_seq_cst)` | 原子交换 Qt 指针变量为临时地址，并保存旧地址。 | 指针恢复与对象回收无关；旧新对象都必须由外部管理。 |
| 析构 | `~QAtomicScopedValueRollback()` | 将构造时或最近一次 `commit()` 时保存的值写回原子变量。 | 无条件 store；可能覆盖其他线程在守卫期间的更新。 |
| 更新回滚点 | `commit()` | 读取当前原子值，并把它设为析构时新的恢复目标。 | 不会取消回滚；之后对变量的新修改仍会在析构时被撤销到这个新值。 |
| 版本 | `QAtomicScopedValueRollback` | Qt 6.7 引入的原子作用域回滚器。 | 面向同时使用 Qt 原子类与 `std::atomic` 的现代 Qt 代码。 |

## 一句话总结

`QAtomicScopedValueRollback` 用 RAII 保证原子变量在离开作用域时恢复到指定检查点。它很适合临时状态和异常安全清理，但不会隔离并发写入；只要其他线程可能同时修改，就必须先设计好谁有权恢复、谁负责避免丢失更新。
