# Qt QThreadStorage：每个线程一份独立数据

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QThreadStorage>`  
> 所属模块：`Qt6::Core`  
> 类型性质：按线程隔离数据的模板容器  
> 关联类型：`QThread`、C++ `thread_local`

## 1. 它解决什么问题

`QThreadStorage<T>` 为每个线程保存一份独立的 `T`。多个线程访问同一个 `QThreadStorage<T>` 对象时，读到和修改的是各自线程的槽位，不需要用锁保护这些槽位之间的隔离：

```cpp
QThreadStorage<QByteArray> scratch;

void appendLocal(QByteArray part)
{
    scratch.localData().append(part);
}
```

如果线程 A 和线程 B 都调用 `appendLocal()`，它们不会修改同一个 `QByteArray`；每个线程第一次访问时得到自己的值。

适合场景：

- 每个线程独立的临时缓存；
- 线程局部解析器、格式化缓冲和统计计数；
- 不希望把上下文参数层层传递的基础设施代码；
- 需要使用 Qt 线程退出清理语义的线程局部对象。

它不是线程间共享容器，也不是同步工具。需要在线程之间交换数据时，使用消息传递、锁、信号槽或并发容器。

## 2. `QThreadStorage<T>` 与 `thread_local` 的选择

| 需求 | 更合适的选择 |
| --- | --- |
| 固定类型、编译期确定、简单线程局部变量 | C++ `thread_local` |
| 需要 Qt 线程局部生命周期和 Qt 旧代码兼容 | `QThreadStorage<T>` |
| 每个线程延迟创建一个可复用对象 | `QThreadStorage<T>::localData()` |
| 线程之间共享同一个状态 | `QMutex`、`QReadWriteLock`、消息传递或并发容器 |

Qt 头文件对“平凡的非指针类型”可能给出建议使用 `thread_local` 的警告。对简单整数或结构体，不要为了习惯而强行使用 `QThreadStorage`。

## 3. 构建与最小示例

```cmake
find_package(Qt6 REQUIRED COMPONENTS Core)
target_link_libraries(mytarget PRIVATE Qt6::Core)
```

```cpp
#include <QThreadStorage>
#include <QString>

class ThreadContext
{
public:
    void setRequestId(QString id)
    {
        m_requestId.localData() = std::move(id);
    }

    QString requestId() const
    {
        return m_requestId.localData();
    }

private:
    QThreadStorage<QString> m_requestId;
};
```

`QThreadStorage` 对象本身可以由多个线程访问；它内部按当前调用线程选择槽位。宿主 `QThreadStorage` 必须活得足够久，覆盖所有线程对它的访问。

## 4. 值类型和指针类型是两种语义

### 4.1 非指针 `T`：按值存储

```cpp
QThreadStorage<QString> storage;

QString &text = storage.localData(); // 当前线程第一次调用时默认构造
text += "local";
```

非 const `localData()` 在当前线程没有数据时会创建一个默认构造的 `T`。const `localData()` 在没有数据时返回一个默认构造的 `T` 值，不会创建槽位。

### 4.2 指针 `T *`：存储指针值并负责删除指向对象

```cpp
QThreadStorage<Cache *> caches;

if (!caches.hasLocalData())
    caches.setLocalData(new Cache);

Cache *cache = caches.localData();
```

对指针特化，`QThreadStorage<T *>` 保存的是每个线程的裸指针，并在线程局部数据被清理时执行 `delete`。因此传入的指针必须来自可由 `delete` 释放的对象，不能是栈地址、静态对象地址、由其他 owner 管理的对象或数组指针。

如果不希望由 `QThreadStorage` 删除对象，存储一个非拥有句柄或改用明确的生命周期方案；不要把任意裸指针放进指针特化。

### 4.3 线程局部对象的析构

线程结束时，Qt 会清理该线程在 `QThreadStorage` 中的数据。非指针类型销毁对应的 `T`，指针特化删除指针指向的 `T`。析构函数不应依赖已经退出的线程服务或访问已销毁的全局对象。

## 5. `localData()` 的创建规则

### 5.1 非 const 版本会惰性创建

```cpp
if (!storage.hasLocalData()) {
    // 这里只查询，不创建
}

T &value = storage.localData(); // 没有时创建
```

这是一个重要边界：如果只是想知道当前线程是否已经初始化，不要用非 const `localData()`，因为它会改变状态。

### 5.2 const 版本返回副本

```cpp
const QThreadStorage<QString> storage = ...;
QString copy = storage.localData();
```

const `localData()` 返回 `T` 值，而不是当前线程槽位的可修改引用。没有局部数据时返回默认构造的 `T`。

对大型对象，频繁通过 const 版本读取会复制；如果确实需要引用，应在受控设计中使用非 const storage，但同时明确其是否允许初始化当前线程槽位。

### 5.3 指针特化的 const 版本

对 `QThreadStorage<T *>`，const `localData()` 返回当前线程的 `T *` 值。没有数据时返回 `nullptr`，不会分配对象。

## 6. 设置和替换局部数据

```cpp
storage.setLocalData(value);
```

对值类型，Qt 为当前线程保存一份 `T` 的副本；对指针类型，保存指针值并将旧的局部对象按指针特化的删除规则清理。

不要用同一个指针值同时交给多个线程的 `QThreadStorage<T *>` 槽位，除非对象有明确的共享所有权和删除协议。指针特化默认认为每个槽位对它保存的指针拥有删除责任，重复保存同一个地址会导致重复释放。

## 7. 线程安全边界

`QThreadStorage` 的“局部”是按调用线程划分的：

- 同一个 `QThreadStorage` 可由多个线程访问；
- 不同线程访问不同槽位；
- 同一线程的多个调用访问同一个槽位；
- 它不自动保护同一线程内的重入、递归或多个对象之间的业务不变量；
- 宿主 `QThreadStorage` 自身的析构不能与其他线程的访问并发进行。

如果一个线程把自己的局部对象指针传给另一个线程，那个对象就不再自动变成“对方线程的局部数据”；跨线程访问仍需遵守对象的线程安全规则。

## 8. 实际使用场景

### 8.1 每线程复用解析器

```cpp
QThreadStorage<QRegularExpression> parser;

const QRegularExpression &regex()
{
    QRegularExpression &value = parser.localData();
    if (value.pattern().isEmpty())
        value.setPattern(R"(\w+)");
    return value;
}
```

每个线程拥有自己的正则对象，避免共享可变配置和不必要的锁。若模式固定且可共享，直接使用一个 const `QRegularExpression` 可能更简单。

### 8.2 每线程缓存

```cpp
QThreadStorage<QCache<QString, QByteArray> *> caches;

QCache<QString, QByteArray> *cache()
{
    if (!caches.hasLocalData())
        caches.setLocalData(new QCache<QString, QByteArray>);
    return caches.localData();
}
```

这里必须确保 `QCache` 只被创建它的线程使用，并接受线程结束时自动删除的所有权语义。

### 8.3 线程局部统计

```cpp
QThreadStorage<quint64> requests;

void recordRequest()
{
    ++requests.localData();
}
```

如果只需要一个简单的线程局部计数器，C++ `thread_local quint64` 可能更直接，且不需要通过 Qt 模板访问。

## 9. 生命周期和销毁顺序

### 9.1 storage 必须覆盖工作线程访问期

```cpp
QThreadStorage<Cache *> storage;
QThread worker;
// worker 使用 storage
```

必须先让 worker 停止并退出，再销毁 `storage`。如果 storage 已经析构，工作线程仍调用 `localData()`，行为未定义。

### 9.2 全局/静态 storage 的退出顺序

静态 `QThreadStorage` 可能遇到 C++ 静态析构顺序问题：线程仍在退出、另一个静态对象的析构函数还在访问 storage，都会产生复杂依赖。优先让应用明确控制线程停止顺序，避免在静态析构阶段执行新的线程局部操作。

### 9.3 不能跨线程“收集”局部值

`QThreadStorage` 没有遍历所有线程槽位的公共 API。需要汇总时，让每个线程主动发送自己的结果，或使用共享统计对象和适当同步。

## 10. 常见错误

### 10.1 把它当共享变量

线程 A 写入不会让线程 B 的 `localData()` 读到同一值。每个线程有独立槽位。

### 10.2 用非 const `localData()` 做存在性检查

它会惰性创建默认对象。只检查是否已经有数据时使用 `hasLocalData()`。

### 10.3 指针特化放入栈地址

线程结束时 Qt 会 `delete` 该指针，栈地址会导致未定义行为。

### 10.4 多个槽位保存同一个裸指针

指针特化默认删除各自保存的对象，重复地址会造成重复释放。需要共享对象时使用明确的共享所有权。

### 10.5 storage 析构早于工作线程

这是最危险的生命周期错误之一。先停止访问线程，再销毁 storage。

### 10.6 误以为局部对象可以跨线程直接使用

从一个线程取得的 `T &` 或 `T *` 交给另一个线程后，它就是普通跨线程对象访问，不再享受局部隔离。

## 11. 逐项 API 语义

### `QThreadStorage()`

创建一个没有任何线程局部数据的 storage。对每个线程，数据槽位独立维护。

### `~QThreadStorage()`

销毁 storage 及其管理的线程局部数据。调用时必须确保没有其他线程仍在访问该 storage。

### `hasLocalData() const`

查询当前调用线程是否已经有局部数据。它不会为非指针 `T` 创建默认值，也不会改变当前线程槽位。

### `T &localData()`

返回当前线程局部数据的可修改引用。没有数据时惰性创建一个默认构造的 `T`；指针特化则会建立当前槽位并返回指针引用/值的对应语义。调用后当前线程会拥有一个局部数据槽位。

### `T localData() const`

返回当前线程局部数据的值副本。没有局部数据时返回默认构造的 `T`；不会通过 const 查询创建槽位。

### `setLocalData(T data)`

替换当前线程的局部数据。值类型按值保存；指针特化保存指针并负责按其删除规则清理旧数据和线程结束时的数据。

## API 速查表
| 类别 | API | 作用 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造 | `QThreadStorage()` | 创建线程局部存储容器。 | 每个线程独立槽位；storage 自身必须覆盖所有访问期。 |
| 生命周期 | `~QThreadStorage()` | 销毁 storage 和局部数据。 | 先停止所有工作线程，再销毁；指针特化会删除指向对象。 |
| 查询 | `hasLocalData()` | 判断当前线程是否已有槽位。 | 不创建默认值，适合纯查询。 |
| 访问 | `T &localData()` | 取得当前线程可修改的局部数据。 | 非 const 版本会惰性创建；指针特化的裸指针有删除责任。 |
| 访问 | `T localData() const` | 取得当前线程局部数据的副本。 | 无槽位返回默认值；大型值可能产生复制。 |
| 设置 | `setLocalData(T)` | 替换当前线程的局部数据。 | 指针特化不要重复保存同一裸指针；旧值会按特化规则清理。 |
| 语义 | `QThreadStorage<T *>` | 为每个线程保存一个指针槽位。 | Qt 在线程清理时删除指针指向对象；不要放栈地址或其他 owner 管理的地址。 |
| 语义 | `QThreadStorage<T>` | 为每个线程保存一个值对象。 | 非 const 访问惰性默认构造，const 访问返回副本。 |

## 13. 一句话总结

`QThreadStorage<T>` 让同一个 storage 在每个线程拥有独立数据：非 const `localData()` 会惰性创建，const 版本只返回副本，指针特化默认负责删除对象。它解决线程隔离，不解决线程间共享、同步和 storage 的销毁顺序。
