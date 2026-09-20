# Qt QObjectCleanupHandler：集中清理一组 QObject

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QObjectCleanupHandler>`  
> 所属模块：`Qt6::Core`  
> 继承：`QObject -> QObjectCleanupHandler`  
> 类型性质：监视并在清理时删除 QObject 的管理对象

## 1. 它解决什么问题

`QObjectCleanupHandler` 用来收集一组 QObject 指针，并在 handler 被清空或销毁时删除这些对象。同时，如果被管理对象先在别处销毁，handler 会通过 `destroyed(QObject *)` 通知把它从内部列表中移除。

```cpp
QObjectCleanupHandler cleanup;

QObject *temporary = new QObject;
cleanup.add(temporary);

cleanup.clear(); // 删除 temporary，并清空列表
```

它适合：

- 临时创建一批 QObject，稍后统一销毁；
- 插件、脚本或动态 UI 创建对象后交给一个清理点；
- 需要“对象自行销毁时列表自动更新”的集中管理；
- 某个作用域结束时删除多个没有 parent 或不适合挂 parent 的对象。

它和 `QPointer` 的方向相反：`QPointer` 只观察且不删除对象；`QObjectCleanupHandler` 是清理者，会在自身清理时删除已加入的对象。

## 2. 它不是什么

`QObjectCleanupHandler` 不是：

- QObject parent-child 机制的替代品；
- 通用智能指针；
- 异步取消器；
- 跨线程安全删除工具；
- 非 QObject 对象的容器；
- 只观察不删除的弱引用列表。

加入 handler 后，应明确：这个对象可能在 `clear()` 或 handler 析构时被 `delete`。如果对象还有其他 owner，必须避免重复删除。

## 3. 构建与最小示例

```cmake
find_package(Qt6 REQUIRED COMPONENTS Core)
target_link_libraries(mytarget PRIVATE Qt6::Core)
```

```cpp
#include <QObjectCleanupHandler>

void createTemporaryObjects()
{
    QObjectCleanupHandler cleanup;

    cleanup.add(new QObject);
    cleanup.add(new QObject);

    // 函数返回时 cleanup 析构，仍在列表中的对象被删除。
}
```

`QObjectCleanupHandler` 本身是 QObject，可以有 parent；parent 只管理 handler 的生命周期。handler 管理的是通过 `add()` 加入的对象。

## 4. 所有权语义

### 4.1 `add()` 表示纳入清理责任

```cpp
QObject *object = new QObject;
cleanup.add(object);
```

加入后，handler 会在 `clear()` 或析构时删除该对象，除非对象已经先自行销毁或被 `remove()` 移除。

不要再同时用 `std::unique_ptr`、`QScopedPointer` 或另一个清理 handler 管理同一个对象的删除。QObject parent 也会删除子对象，因此把有 parent 的对象加入 cleanup 需要格外确认销毁顺序，避免同一对象被两个 owner 竞争删除。

### 4.2 对象先销毁时自动移除

```cpp
QObject *object = new QObject;
cleanup.add(object);

delete object;
Q_ASSERT(cleanup.isEmpty());
```

handler 通过 QObject 的销毁通知更新内部列表。因此它不会在之后再次尝试删除同一个对象。

这并不意味着你可以随意在不同线程删除对象。QObject 的销毁仍应发生在符合其线程亲和性和事件循环规则的位置。

### 4.3 `remove()` 只取消清理，不删除对象

```cpp
QObject *object = cleanup.add(new QObject);
cleanup.remove(object);
delete object; // 现在由调用方负责
```

`remove()` 是“从 cleanup 列表移除”，不是“删除”。移除后对象还活着，后续由调用方、parent 或其他 owner 负责销毁。

### 4.4 `clear()` 会删除所有当前对象

```cpp
cleanup.clear();
```

`clear()` 会清理列表中的对象。调用它之前，必须确认没有其他代码仍会使用这些对象。对象析构可能发出 `destroyed()`、触发连接断开和子对象析构，回调中不要假设列表仍保持调用前状态。

## 5. 与 QObject parent-child 的关系

多数 QObject 生命周期可以直接用 parent 管理：

```cpp
auto *child = new QObject(parent);
```

`QObjectCleanupHandler` 更适合“清理者不是对象树 parent”的场景：

- 统一删除一批临时对象，但不想改变它们 parent；
- 对象可能属于不同 parent 或没有 parent；
- handler 需要跟踪对象是否已经被外部销毁；
- 作用域内创建多个对象，任意创建失败后统一清理。

不要为了“方便统一删除”把已经由 parent 明确拥有的对象又交给 cleanup，除非非常清楚 parent 与 cleanup 的析构顺序。

## 6. 线程和事件循环边界

`QObjectCleanupHandler` 是 QObject，内部通过信号槽跟踪被管理对象销毁。实践中应让 handler 和被管理对象处在可预期的线程关系中：

- `add()`、`remove()`、`clear()` 应在安全的对象管理线程调用；
- 不要从另一个线程直接删除仍属于 GUI 线程的 QObject；
- 需要跨线程销毁时优先让对象在自身线程 `deleteLater()`，或通过 queued 调用回到所属线程；
- `clear()` 直接删除对象，可能不适合必须 deferred delete 的对象。

如果对象必须延迟到事件循环安全点删除，`QObjectCleanupHandler` 不是最合适的唯一工具；可以改用 parent、`deleteLater()` 或专门的生命周期协议。

## 7. 常见使用场景

### 7.1 函数内批量创建，失败时统一回滚

```cpp
QObjectCleanupHandler cleanup;

auto *first = cleanup.add(new QObject);
auto *second = cleanup.add(new QObject);

if (!initialize(first, second))
    return; // cleanup 析构删除已创建对象

cleanup.remove(first);
cleanup.remove(second);
adoptObjects(first, second);
```

初始化成功后用 `remove()` 把对象交给新的 owner；失败路径由 cleanup 自动删除。

### 7.2 管理动态扩展对象

```cpp
class PluginRuntime
{
public:
    QObject *track(QObject *object)
    {
        return m_cleanup.add(object);
    }

    void unload()
    {
        m_cleanup.clear();
    }

private:
    QObjectCleanupHandler m_cleanup;
};
```

卸载时统一删除仍存活的动态对象。若对象已自行销毁，handler 中不会留下悬空指针。

### 7.3 与 `QPointer` 配合

```cpp
QPointer<QObject> watched = cleanup.add(new QObject);
cleanup.clear();
Q_ASSERT(watched.isNull());
```

`QObjectCleanupHandler` 负责删除，`QPointer` 负责外部观察是否仍存在。两者语义互补，但不要用 `QPointer` 误以为自己拥有对象。

## 8. 常见错误

### 8.1 把有明确 parent 的对象又加入 cleanup

如果 parent 和 handler 都可能删除对象，销毁顺序必须绝对清楚。更简单的做法是只保留一个 owner。

### 8.2 以为 `remove()` 会删除

`remove()` 只移除跟踪关系。对象仍然存在。

### 8.3 以为 `clear()` 只是清空列表

`clear()` 会删除仍在列表中的对象。只想放弃管理某个对象时用 `remove()`。

### 8.4 跨线程直接 clear GUI 对象

GUI QObject 必须在 GUI 线程销毁。跨线程清理要用 queued 调用或对象自己的线程机制。

### 8.5 加入非 QObject 或栈对象

API 只接受 `QObject *`，但栈上 QObject 被加入后，handler 清理时会尝试删除它，导致未定义行为。只加入能由 handler 删除的堆对象。

### 8.6 清理时还有外部裸指针使用

`clear()` 或析构可能让外部裸指针悬空。外部观察者使用 `QPointer` 或在清理前断开/停止相关流程。

## 9. 逐项 API 语义

### `QObjectCleanupHandler()`

创建空的清理 handler。它本身是 QObject，但构造后没有任何被管理对象。

### `~QObjectCleanupHandler()`

销毁 handler，并清理仍在列表中的对象。对象的实际析构会按 QObject 删除规则发生，期间可能触发 `destroyed()` 和连接断开。

### `add(QObject *object)`

把对象加入清理列表并返回同一个指针。加入后，handler 会跟踪对象销毁，并在 `clear()` 或析构时删除仍存活对象。`nullptr` 没有可管理对象；调用方应避免把空指针当作成功创建。

### `remove(QObject *object)`

从清理列表移除对象，不删除它。移除后销毁责任回到其他 owner 或调用方。

### `isEmpty() const`

判断当前列表是否为空。对象自行销毁会使列表自动更新，因此它可以用于诊断是否还有对象由 handler 管理。它是瞬时状态，不能替代并发生命周期同步。

### `clear()`

删除当前管理的所有对象并清空列表。它不是简单丢弃指针；调用前必须确认删除时机正确。

## API 速查表
| 类别 | API | 作用 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造 | `QObjectCleanupHandler()` | 创建空清理器。 | 本身是 QObject；无默认管理对象。 |
| 生命周期 | `~QObjectCleanupHandler()` | 删除仍在列表中的对象并销毁 handler。 | 不能让其他 owner 同时删除同一对象。 |
| 加入 | `add(QObject *)` | 纳入清理列表并返回该对象。 | 只加入可由 handler 删除的堆上 QObject。 |
| 移除 | `remove(QObject *)` | 取消跟踪但不删除对象。 | 移除后由调用方、parent 或其他 owner 负责生命周期。 |
| 查询 | `isEmpty()` | 判断当前是否无被管理对象。 | 对象自行销毁会自动更新；只是瞬时状态。 |
| 清理 | `clear()` | 删除所有仍被管理的对象。 | 不是只清空列表；注意线程和外部裸指针。 |
| 协作 | `destroyed(QObject *)` | 被管理对象销毁时，handler 自动移除记录。 | 私有槽机制，普通代码不直接调用。 |

## 11. 一句话总结

`QObjectCleanupHandler` 是一组 QObject 的集中清理者：`add()` 纳入删除责任，`remove()` 只放弃管理，`clear()` 和析构会删除仍存活对象。它能自动忘记先行销毁的对象，但不替代 parent、线程亲和性和明确的所有权设计。
