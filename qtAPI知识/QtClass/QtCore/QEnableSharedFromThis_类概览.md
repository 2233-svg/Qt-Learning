# Qt QEnableSharedFromThis 深入笔记

> 适用版本：Qt 6.11.1  
> 模板：`template <typename T> class QEnableSharedFromThis`  
> 头文件：`#include <QEnableSharedFromThis>`  
> 所属模块：`Qt6::Core`  
> 关键协作类型：`QSharedPointer<T>`、`QWeakPointer<T>`

## 1. 它解决什么问题

`QEnableSharedFromThis<T>` 用来解决一个很具体的所有权问题：对象已经由 `QSharedPointer` 管理，但对象内部只有 `this` 裸指针时，如何取得一个**共享同一控制块**的 `QSharedPointer`。

下面这种写法看起来直观，但不能使用：

```cpp
QSharedPointer<T> self()
{
    return QSharedPointer<T>(this); // 错误
}
```

`QSharedPointer<T>(this)` 会把同一个裸指针包装进一个新的引用计数控制块。原来的 `QSharedPointer` 和新返回的 `QSharedPointer` 不知道彼此的存在，最后很可能对同一个对象执行两次销毁，或者在其中一个指针释放后留下悬空访问。

继承 `QEnableSharedFromThis<T>` 后，`sharedFromThis()` 会从 Qt 记录的弱引用中恢复共享指针。返回的新指针与原来的 `QSharedPointer` 共享所有权和生命周期，不会创建第二套引用计数。

它只负责“从已经存在的共享所有权中取回一个共享指针”，不负责把栈对象、普通裸指针或其他所有权系统自动变成安全的 `QSharedPointer`。

## 2. 所有权模型

典型关系可以画成：

```text
QSharedPointer<Worker> p
        |
        v
      Worker
        ^
        |
sharedFromThis() 返回另一个 QSharedPointer<Worker>
```

两个 `QSharedPointer` 指向同一个对象，也共享同一个控制块。只要其中任意一个仍然存活，对象就不会因为另一个指针离开作用域而被销毁。

对象必须先进入 `QSharedPointer` 的管理范围，`sharedFromThis()` 才能成功：

```cpp
class Worker : public QEnableSharedFromThis<Worker>
{
public:
    QSharedPointer<Worker> self()
    {
        return sharedFromThis();
    }
};

QSharedPointer<Worker> owner(new Worker);
QSharedPointer<Worker> same = owner->self();

Q_ASSERT(!same.isNull());
Q_ASSERT(owner == same);
```

相反，下面的对象没有共享控制块，因此返回空指针：

```cpp
Worker stackObject;
Q_ASSERT(stackObject.sharedFromThis().isNull());

Worker *rawObject = new Worker;
Q_ASSERT(rawObject->sharedFromThis().isNull());
delete rawObject;
```

这里的 `rawObject` 在被 `QSharedPointer` 接管之前只是普通裸指针。不能因为类型继承了 `QEnableSharedFromThis`，就认为它已经拥有共享生命周期。

## 3. 构建与包含

```cmake
find_package(Qt6 REQUIRED COMPONENTS Core)
target_link_libraries(mytarget PRIVATE Qt6::Core)
```

```cpp
#include <functional>
#include <QEnableSharedFromThis>
#include <QSharedPointer>
```

`qmake` 工程使用：

```text
QT += core
```

这是模板辅助基类，没有需要调用的公共构造参数，也没有单独的 `create()` 工厂。对象通常由 `QSharedPointer<T>(new T)` 或 `QSharedPointer<T>::create()` 创建。

## 4. 最小可用模式

```cpp
#include <QEnableSharedFromThis>
#include <QSharedPointer>

class Worker : public QEnableSharedFromThis<Worker>
{
public:
    QSharedPointer<Worker> self()
    {
        return sharedFromThis();
    }

    QSharedPointer<const Worker> constSelf() const
    {
        return sharedFromThis();
    }
};

void useWorker()
{
    auto worker = QSharedPointer<Worker>::create();
    auto copyOfOwnership = worker->self();

    Q_ASSERT(worker == copyOfOwnership);
    Q_ASSERT(worker->constSelf());
}
```

`worker->self()` 返回的不是“复制出一个新的 `Worker`”，而是复制了共享指针的所有权句柄。对象数据本身仍然只有一份。

## 5. 实际使用场景

### 5.1 异步回调延长对象生命周期

对象把自身交给异步任务时，捕获一个 `QSharedPointer` 可以确保任务执行期间对象仍然存在：

```cpp
class Worker : public QEnableSharedFromThis<Worker>
{
public:
    void submit(std::function<void(QSharedPointer<Worker>)> enqueue)
    {
        enqueue(sharedFromThis());
    }
};
```

调用方可以把这个指针交给线程池、任务队列或异步回调。真正的任务接口可能要求由外部保存 `QSharedPointer<Worker>`，此时 `sharedFromThis()` 可以避免把 `this` 裸指针交给异步代码。

要注意，调用 `submit()` 时对象必须已经由 `QSharedPointer` 管理。尤其不要在构造函数中调用 `sharedFromThis()`：构造函数执行期间，外层 `QSharedPointer` 通常还没有完成对对象的注册，结果会是空指针。

### 5.2 回调或脚本接口只传递裸指针

某些元对象、脚本或旧式回调接口只能接收 `Y *`。如果 `Y` 继承了 `QEnableSharedFromThis<Y>`，接收端可以把这个裸指针安全地转回共享所有权：

```cpp
class ScriptInterface : public QObject
{
    Q_OBJECT

public slots:
    void calledByScript(Worker *worker)
    {
        if (auto owner = worker->sharedFromThis()) {
            // 这里可以调用只接受 QSharedPointer<Worker> 的内部 API。
        }
    }
};
```

这段代码的前提仍然是：传入的 `worker` 确实来自一个仍然有效的 `QSharedPointer` 管理对象。`QEnableSharedFromThis` 不是对任意悬空裸指针的安全检查器。

### 5.3 对象内部创建需要共享所有权的后续操作

一个成员函数可能需要把自己交给另一个长期保存的组件。如果直接传 `this`，调用方无法表达生命周期；如果重新用 `this` 构造 `QSharedPointer`，又会破坏引用计数。`sharedFromThis()` 正好表达“把现有共享所有权再交给一个使用者”。

## 6. 关键语义与边界

### 6.1 `sharedFromThis()` 返回的是共享控制块中的别名

返回值与现有 `QSharedPointer` 共享控制块。它不会复制对象，也不会启动新的删除器。

因此这两种写法的意义完全不同：

```cpp
return sharedFromThis();        // 正确：复用现有共享所有权
return QSharedPointer<T>(this); // 错误：创建独立控制块
```

永远不要从同一个裸指针构造多个互不关联的 `QSharedPointer`。如果对象已经由共享指针管理，就通过复制原指针、`sharedFromThis()` 或从 `QWeakPointer` 提升来共享同一所有权。

### 6.2 未被管理时返回空指针

非 const 和 const 重载在对象未被 `QSharedPointer` 管理时都返回 null：

```cpp
Worker local;
Q_ASSERT(!local.sharedFromThis());

const Worker constLocal;
Q_ASSERT(!constLocal.sharedFromThis());
```

生产代码如果不能证明对象的所有权来源，应检查返回值。不要对返回的空 `QSharedPointer` 直接解引用。

### 6.3 const 重载保留对象的只读性

在 `const` 成员函数或 `const Worker *` 上调用时，返回的是 `QSharedPointer<const Worker>`。它可以延长生命周期，但不能通过该指针修改对象：

```cpp
QSharedPointer<const Worker> readOnly = worker->constSelf();
```

这和通过非 const `Worker` 调用得到的 `QSharedPointer<Worker>` 是两个不同的类型；需要修改时必须从非 const 对象路径取得共享指针，并且业务上确实拥有可写权限。

### 6.4 继承方式与模板参数必须匹配

通常使用公开继承，并让模板参数写成实际派生类：

```cpp
class Worker : public QEnableSharedFromThis<Worker>
{
};
```

不要把无关的基类写进模板参数，也不要在同一个对象层次中随意重复继承多个 `QEnableSharedFromThis` 基类。这样会让 `QSharedPointer` 初始化哪一个共享来源变得不清晰。

### 6.5 它不替代对象状态同步

共享指针只管理对象生命周期，不会自动保护 `Worker` 内部字段。多个线程可以各自持有共享指针，但对象状态的并发读写仍然需要互斥量、消息传递或其他同步策略。

## 7. 与相似方案的区别

| 方案 | 所有权含义 | 主要风险或特点 |
| --- | --- | --- |
| `sharedFromThis()` | 复用已有 `QSharedPointer` 控制块 | 对象必须已经被共享指针管理，否则返回 null |
| `QSharedPointer<T>(this)` | 为裸指针创建新的控制块 | 与原控制块分离，可能 double delete |
| `QWeakPointer<T>` | 只观察已有控制块，不延长生命周期 | 需要 `toStrongRef()`，提升失败时返回空 |
| 裸指针 `T *` | 不表达所有权 | 适合短暂借用，不能单独保证异步生命周期 |
| `std::enable_shared_from_this` | C++ 标准库对应机制 | 只能与 `std::shared_ptr` 控制块协作，不能和 `QSharedPointer` 混用 |

## 8. API 逐项说明

### `QSharedPointer<T> sharedFromThis()`

从当前对象关联的共享控制块构造一个 `QSharedPointer<T>`。

- 当前对象已经由 `QSharedPointer` 管理：返回指向当前对象的非 const 共享指针；
- 当前对象未被管理：返回 null `QSharedPointer<T>`；
- 返回值与原来的共享指针共享所有权；
- 不会复制 `T`，也不会创建第二个独立删除器。

### `QSharedPointer<const T> sharedFromThis() const`

这是 const 重载。它同样要求当前对象已经由 `QSharedPointer` 管理，但返回 `QSharedPointer<const T>`，通过返回值只能以 const 方式访问对象。

## API 速查表
| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 模板 | `template <typename T> class QEnableSharedFromThis` | 为 `T` 保存从共享所有权恢复 `QSharedPointer` 所需的内部弱引用 | 通常公开继承，并把 `T` 写成实际派生类 |
| 成员函数 | `QSharedPointer<T> sharedFromThis()` | 返回指向当前对象的非 const 共享指针 | 对象未由 `QSharedPointer` 管理时返回 null；不要用 `QSharedPointer<T>(this)` 替代 |
| 成员函数 | `QSharedPointer<const T> sharedFromThis() const` | 返回指向当前对象的只读共享指针 | 返回值仍会延长生命周期，但不能通过它修改 `T` |
| 所有权前提 | `QSharedPointer<T>::create()` / `QSharedPointer<T>(new T)` | 创建并注册对象的共享控制块 | 在控制块建立前调用 `sharedFromThis()`，例如构造函数中调用，通常得到 null |

## 10. 一句话总结

`QEnableSharedFromThis<T>` 让已由 `QSharedPointer` 管理的对象安全地把自己重新表示为共享指针；核心规则是复用原控制块、检查未管理时的 null，并绝不从同一个裸指针重复构造独立的 `QSharedPointer`。
