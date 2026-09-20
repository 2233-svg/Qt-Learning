# Qt QScopeGuard：作用域退出动作

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QScopeGuard>`  
> 所属模块：`Qt6::Core`  
> 类型性质：模板化、只移动的 RAII 回调守卫  
> 相关 API：`qScopeGuard()`、`QScopedValueRollback`

## 1. 它解决什么问题

有些清理动作不属于某个 Qt 资源类的专用析构函数，例如：

- 函数返回前恢复一个外部状态；
- 失败路径删除临时文件；
- 离开作用域时关闭一段手工事务；
- 在多条早退出路径上执行同一段撤销代码；
- 调试期间保证成对的“开始/结束”操作。

`QScopeGuard` 把一个可调用对象保存起来，在 guard 仍然有效时，于析构阶段执行它：

```cpp
auto guard = qScopeGuard([&] {
    rollbackTemporaryState();
});

doWork();
```

如果 `doWork()` 提前返回，或者抛出异常，guard 仍会在离开作用域时执行回调。

## 2. 它不是什么

`QScopeGuard` 不是：

- 事务系统；
- 异常安全的自动回滚数据库；
- 可复制的回调对象；
- 自动捕获所有局部变量生命周期的机制；
- 可以安全抛异常的析构对象；
- “成功后自动取消”的守卫。

它只负责在当前作用域结束时调用保存的函数。回调捕获的引用、指针和 QObject 必须在 guard 执行前仍然有效。

## 3. 构建与包含

```cmake
find_package(Qt6 REQUIRED COMPONENTS Core)
target_link_libraries(mytarget PRIVATE Qt6::Core)
```

```cpp
#include <QScopeGuard>
```

Qt 6.11.1 提供 `qScopeGuard()` 工厂函数，也可以显式构造 `QScopeGuard<F>`。日常代码优先使用工厂函数，让 lambda 的类型由编译器推导。

## 4. 最小可用代码

```cpp
#include <QScopeGuard>

bool update()
{
    beginUpdate();
    const auto guard = qScopeGuard([] {
        endUpdate();
    });

    if (!prepare())
        return false;
    if (!apply())
        return false;

    guard.dismiss();
    endUpdate();
    return true;
}
```

这里用 `dismiss()` 表示成功路径已经手动完成收尾，因此析构时不再调用 `endUpdate()`。

更常见的写法是直接让 guard 负责唯一一次收尾：

```cpp
bool update()
{
    beginUpdate();
    const auto guard = qScopeGuard([] {
        endUpdate();
    });

    return prepare() && apply();
}
```

## 5. 核心状态机

一个新构造的 guard 处于“待调用”状态。它有三种重要转移：

```text
构造
  |
  v
待调用 ---- dismiss() ----> 已取消
  |
  +---- commit() ----------> 立即调用并变为已取消
  |
  +---- 析构 --------------> 调用并变为结束
```

### 5.1 正常析构会调用回调

析构函数检查内部 `m_invoke` 标志。如果仍为 `true`，就调用保存的函数。析构发生在所有早退出路径上，因此它能覆盖 `return` 和异常展开。

### 5.2 `dismiss()` 只取消，不执行

```cpp
auto guard = qScopeGuard([&] {
    cleanup();
});

if (cleanupWasDoneElsewhere())
    guard.dismiss();
```

调用 `dismiss()` 后析构不会再调用回调。它不会执行清理，也不会销毁被捕获的外部资源，只是关闭 guard 的自动调用状态。

重复 `dismiss()` 仍然只是保持取消状态。

### 5.3 `commit()` 是“现在执行一次”，不是“取消”

Qt 6.11.1 新增：

```cpp
guard.commit();
```

实现会先把 guard 标记为不再调用，再立即执行回调。因此：

- 回调在 `commit()` 调用点执行；
- 之后析构不会再次调用；
- 如果回调抛出异常，guard 已经处于不再调用状态；
- `commit()` 的异常规格取决于回调是否可能抛出。

如果只是想让析构不执行，应使用 `dismiss()`，不要把 `commit()` 当作 `dismiss()` 的别名。

## 6. 回调异常和析构边界

### 6.1 析构阶段的回调不能抛出

`QScopeGuard` 的析构函数是 `noexcept`。如果回调在析构阶段抛出异常，程序会进入终止流程，而不是把异常继续传播给调用方。

因此用于析构自动执行的回调应设计为不抛出：

```cpp
auto guard = qScopeGuard([&] noexcept {
    closeNoexcept();
});
```

如果清理动作确实可能失败，应在回调内部记录、转换或延迟错误，而不是让异常穿过析构函数。

### 6.2 `commit()` 可以传播回调异常

`commit()` 先关闭自动调用状态，再直接调用回调。如果回调可能抛出，异常可以从 `commit()` 调用点传播；但 guard 不会在之后析构时重复调用。

这使 `commit()` 适合“在明确的成功阶段立即执行一次收尾”，但调用方仍需理解它可能抛出。

## 7. 生命周期、捕获和移动语义

### 7.1 捕获引用必须覆盖 guard 生命周期

```cpp
QScopeGuard makeBadGuard()
{
    QString local = QStringLiteral("temporary");
    return qScopeGuard([&] {
        qDebug() << local; // 错误：local 已销毁
    });
}
```

正确做法是让 guard 在被捕获对象之前销毁，或者按值捕获需要的数据：

```cpp
QString value = QStringLiteral("temporary");
auto guard = qScopeGuard([value] {
    qDebug() << value;
});
```

### 7.2 声明顺序会影响析构顺序

C++ 按声明的逆序析构局部对象。若 guard 需要访问某个资源，通常应先声明资源，再声明 guard，这样 guard 会先析构：

```cpp
Resource resource;
auto guard = qScopeGuard([&] {
    resource.finish();
});
```

### 7.3 只移动，不能复制

`QScopeGuard` 禁用复制，提供移动构造。移动会把回调和“是否调用”状态转移给目标对象，并让源对象失效：

```cpp
auto first = qScopeGuard([] { cleanup(); });
auto second = std::move(first);
```

之后由 `second` 负责执行，`first` 不应再被当作有效 guard 使用。移动后的 guard 如果再被销毁，不会重复调用。

### 7.4 返回 guard 时注意捕获方式

返回一个按值捕获数据的 guard 可以安全；返回捕获局部引用的 guard 通常不安全。guard 的生命周期和捕获对象必须作为一个整体设计。

## 8. `qScopeGuard()` 工厂函数

```cpp
template <typename F>
QScopeGuard<std::decay_t<F>> qScopeGuard(F &&f);
```

工厂函数：

- 对传入的 lambda、函数对象或函数指针做 `decay`；
- 转发并保存可调用对象；
- 返回一个只移动的 `QScopeGuard`；
- 带有 `[[nodiscard]]` 语义，不能无视返回值。

下面的写法没有意义：

```cpp
qScopeGuard([&] { cleanup(); }); // 临时 guard 立即析构，马上执行
```

应把结果绑定到局部变量，让守卫覆盖实际临界区：

```cpp
const auto guard = qScopeGuard([&] { cleanup(); });
```

## 9. 与 `QScopedValueRollback` 的选择

如果要恢复一个普通变量的旧值，`QScopedValueRollback<T>` 更直接：

```cpp
QScopedValueRollback<int> rollback(state, Busy);
```

如果要执行任意动作，或清理动作不是简单的变量赋值，使用 `QScopeGuard`：

```cpp
auto guard = qScopeGuard([&] {
    restoreExternalState();
});
```

两者都不提供线程同步。它们只管理当前对象的作用域行为。

## 10. 逐项 API 语义

### 10.1 `QScopeGuard(F &&f)`

```cpp
explicit QScopeGuard(F &&f) noexcept;
```

移动保存右值可调用对象，并把 guard 设置为待调用状态。构造本身不执行回调。

### 10.2 `QScopeGuard(const F &f)`

```cpp
explicit QScopeGuard(const F &f) noexcept;
```

复制保存左值可调用对象。`F` 必须能被复制构造。构造本身不执行回调。

### 10.3 `QScopeGuard(QScopeGuard &&other)`

```cpp
QScopeGuard(QScopeGuard &&other) noexcept;
```

移动回调和调用状态。源 guard 被置为不再调用，目标 guard 接管一次性调用责任。

### 10.4 `~QScopeGuard()`

```cpp
~QScopeGuard() noexcept;
```

若 guard 仍处于待调用状态，就调用回调；否则什么也不做。回调不能让异常穿过该析构函数。

### 10.5 `dismiss()`

```cpp
void dismiss() noexcept;
```

取消析构时的自动调用。它不执行回调，适合表示调用方已经完成成功收尾或决定不再需要清理。

### 10.6 `commit()`

```cpp
void commit() noexcept(std::is_nothrow_invocable_v<F>);
```

立即调用回调，并先关闭析构调用状态。Qt 6.11 起提供。它不是取消函数，也不是事务提交协议。

### 10.7 `qScopeGuard(F &&f)`

```cpp
template <typename F>
QScopeGuard<std::decay_t<F>> qScopeGuard(F &&f);
```

创建并返回对应的 guard。结果应保存到有名字的局部对象中；临时返回值会在完整表达式结束时析构。

## 11. 实际使用模式

### 11.1 失败回滚

```cpp
bool Importer::run()
{
    createTemporaryFile();
    const auto rollback = qScopeGuard([&] noexcept {
        removeTemporaryFile();
    });

    if (!writeHeader())
        return false;
    if (!writeBody())
        return false;

    rollback.dismiss();
    return true;
}
```

### 11.2 成功路径立即收尾

```cpp
void Session::finish()
{
    beginFinalization();
    auto guard = qScopeGuard([&] noexcept {
        endFinalization();
    });

    prepareReply();
    guard.commit();
}
```

### 11.3 不要让 guard 跨越线程转移资源

guard 本身可以移动，但它捕获的资源是否可以跨线程使用，取决于资源的线程约束。移动 guard 不会自动迁移 QObject、事件循环或线程亲和性。

## 12. 常见错误

### 12.1 忽略 `[[nodiscard]]`

立即丢弃工厂返回值会在完整表达式结束时执行回调，通常不是想要的作用域保护。

### 12.2 把 `commit()` 当作取消

`commit()` 会现在调用一次；需要禁用析构调用时使用 `dismiss()`。

### 12.3 让析构回调抛异常

析构回调抛异常会触发终止。清理路径应使用不抛异常函数，或者在回调内部处理错误。

### 12.4 捕获已经销毁的局部引用

guard 不能延长引用对象生命周期。捕获引用时，确保 guard 比被引用对象更早析构。

### 12.5 用它代替锁

`QScopeGuard` 不提供互斥、内存序或线程安全。它只能包住你已经决定好的清理动作。

## API 速查表
| API | 作用 | 使用时重点注意 |
| --- | --- | --- |
| `QScopeGuard(F &&)` | 移动保存右值可调用对象，启用作用域退出调用 | 构造不执行回调；对象只移动不可复制 |
| `QScopeGuard(const F &)` | 复制保存左值可调用对象 | `F` 必须可复制；构造不执行回调 |
| `QScopeGuard(QScopeGuard &&)` | 转移回调和一次性调用状态 | 源对象不再负责执行 |
| `~QScopeGuard()` | 在未取消时执行回调 | `noexcept`；回调抛异常会终止程序 |
| `dismiss()` | 取消未来的自动调用 | 不执行回调；重复调用无额外效果 |
| `commit()` | 立即调用一次并取消析构调用 | Qt 6.11 起提供；可能传播回调异常 |
| `qScopeGuard(f)` | 推导并创建 guard | 必须保存返回值，不能丢弃临时对象 |

## 14. 一句话总结

`QScopeGuard` 是任意作用域退出动作的只移动 RAII 守卫：默认在析构时调用，`dismiss()` 取消，Qt 6.11 起 `commit()` 会立即调用一次。使用时最重要的是保证捕获对象和回调生命周期有效，并让析构路径保持不抛异常。
