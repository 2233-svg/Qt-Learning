# QQueue：以 FIFO 语义操作 QList

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QQueue>`  
> 模块：`Qt6::Core`  
> 模板：`template <typename T>`  
> 基类：`QList<T>`；隐式共享；成员函数可重入

## 它解决什么问题

`QQueue<T>` 是 Qt 的先进先出（FIFO）队列容器：新元素从队尾进入，旧元素从队首取出。它不是独立的队列实现，而是继承 `QList<T>` 并给三个常用队列动作起了明确名字：

- `enqueue(t)` 等价于 `append(t)`；
- `dequeue()` 等价于 `takeFirst()`；
- `head()` 等价于 `first()`。

适合表达“按到达顺序处理”的数据流，例如：

- GUI 线程中排队的待处理任务；
- 协议解析后等待消费的消息；
- 广度优先搜索的待访问节点；
- 单线程生产/消费流程中的命令队列。

```cpp
#include <QQueue>

QQueue<QString> pending;
pending.enqueue("load");
pending.enqueue("render");

while (!pending.isEmpty()) {
    const QString task = pending.dequeue();
    runTask(task);
}
```

`QQueue` 不是线程安全队列。它的“可重入”表示不同实例可在不同线程独立使用，不表示同一个队列允许一个线程入队、另一个线程同时出队而无需同步。

## FIFO 语义和真实边界

```text
enqueue(A) -> [A]
enqueue(B) -> [A, B]
head()     -> A，队列仍为 [A, B]
dequeue()  -> A，队列变为 [B]
```

`head()` 返回队首的引用，不删除；`dequeue()` 按值返回队首并删除。两者都要求队列非空，先用 `isEmpty()` 或 `empty()` 检查。

```cpp
std::optional<Job> tryTake(QQueue<Job> &queue)
{
    if (queue.isEmpty())
        return std::nullopt;
    return queue.dequeue();
}
```

不要把 `head()` 返回的引用跨越 `dequeue()`、`clear()`、`swap()`、其他结构性修改或队列销毁保存。该元素一旦被取走，引用立即失效。

## QQueue 不是严格封装

由于公开继承 `QList<T>`，你仍可调用 `prepend()`、`insert()`、`removeAt()`、按索引访问等基类 API。这很灵活，但也意味着 `QQueue` 不能强制维护业务层面的 FIFO 纪律。

```cpp
QQueue<int> queue;
queue.enqueue(2);
queue.prepend(1); // 合法，但调用点绕过了队列抽象
```

在代码评审中，若一个容器被命名为“工作队列”或“消息队列”，尽量只使用 `enqueue()`、`dequeue()`、`head()`、`isEmpty()`、`size()` 等队列语义 API。需要按位置插入、删除或随机访问时，变量类型更应该是 `QList<T>`。

## 值类型、隐式共享和移动

元素类型 `T` 必须可赋值，通常也应可复制或可移动。不能把不可复制的 `QWidget` 等 QObject 子类按值放进去；应保存指针、智能指针或轻量标识符，并明确被指向对象的生命周期。

```cpp
QQueue<std::unique_ptr<Task>> tasks;
tasks.enqueue(std::make_unique<Task>());

std::unique_ptr<Task> task = tasks.dequeue();
```

`enqueue(const T &)` 复制元素，`enqueue(T &&)` 移动元素。容器自身是隐式共享值类型：复制队列通常先共享数据，任一副本写入时可能发生分离。迭代器、指针和引用在分离或结构修改后都不应继续依赖。

```cpp
QQueue<int> a;
a.enqueue(1);
QQueue<int> b = a; // 可能共享存储
b.enqueue(2);      // b 修改时可能分离；a 仍保持原队列内容
```

不要借隐式共享把一个队列当作并发共享机制。跨线程传递副本没有问题，但并发访问同一实例仍需锁。

## 性能选择

`QQueue` 的实现直接委托 `QList`，所以性能特征随 Qt 的 `QList` 实现和元素类型而变化。它为代码提供 FIFO 可读性，不是“无条件 O(1) 环形缓冲区”的性能承诺。

对于常规 UI、消息和任务队列，`QQueue` 往往足够。若处于极高频生产/消费路径，或需要无锁并发、容量上限、阻塞等待、优先级调度，应选择专门的数据结构并实测。

`swap(other)` 交换两个队列，Qt 文档保证该操作很快且不失败。它可用于高效清空当前批次并在局部变量中处理：

```cpp
QQueue<Event> batch;
batch.swap(pendingEvents);

while (!batch.isEmpty())
    dispatch(batch.dequeue());
```

交换后两个队列的内容整体互换；此前指向元素的引用、指针和迭代器不应再按旧队列归属理解。

## 线程与生命周期

`QQueue` 不继承 `QObject`，没有父子所有权和线程亲和性。它是普通值类型：

- 局部队列在作用域结束时销毁其中的值；
- 存储裸指针时，销毁队列不会删除被指向对象；
- 存储智能指针时，元素被出队或队列销毁会触发相应资源释放；
- 同一实例的并发 `enqueue()`、`dequeue()`、`head()`、遍历必须由调用方同步。

常见的线程间设计是：生产方用 `QMutex` 保护队列并通过 `QWaitCondition` 通知，或直接把任务作为 queued signal 发送给消费对象。后者往往比手写共享队列更符合 Qt 的对象模型。

## 常见错误

### 空队列上调用 `dequeue()` 或 `head()`

这两个函数的前置条件是非空。不要把断言或偶然的发布版行为当作错误处理；先检查 `isEmpty()`。

### 用 `head()` 取得引用后再修改队列

```cpp
const QString &first = queue.head();
queue.dequeue();
use(first); // 错误：first 已失效
```

需要稍后使用时复制或移动出值。

### 以为 QQueue 自动同步

“一个线程 enqueue，另一个线程 dequeue”仍然是共享可变状态。加锁、使用条件变量，或改为 Qt 事件队列。

### 通过基类 API 破坏顺序

`prepend()`、`insert()`、`removeAt()` 全都可用，但可能使队列行为不再是 FIFO。需要这种能力时，选 `QList` 更诚实。

## API 速查表

| API | 作用 | 语义与边界 |
| --- | --- | --- |
| `enqueue(const T &t)` | 复制元素到队尾 | 等价于 `append()`；适合可复制值。 |
| `enqueue(T &&t)` | 移动元素到队尾 | 等价于移动 `append()`；实参随后处于有效但未指定状态。 |
| `dequeue()` | 取走并返回队首 | 等价于 `takeFirst()`；队列不能为空，返回值按值取得。 |
| `head()` | 读取/修改队首 | 返回 `T &`；队列不能为空；任何结构修改后引用可能失效。 |
| `head() const` | 只读队首 | 返回 `const T &`；队列不能为空。 |
| `swap(QQueue<T> &other)` | 交换两个队列 | `noexcept`，很快；元素整体互换。 |
| 继承的 `isEmpty()` / `empty()` | 判断是否为空 | 在 `dequeue()` / `head()` 前使用。 |
| 继承的 `size()` / `count()` | 查询元素数 | 返回 `qsizetype`。 |
| 继承的 `clear()` | 清空队列 | 销毁元素；存裸指针不会 delete 目标对象。 |
| 继承的迭代器 API | 遍历队列 | 遍历顺序为队首到队尾；写入和分离会影响迭代器有效性。 |
| 继承的 `append()` / `takeFirst()` / `first()` | 同义底层操作 | 可用但弱化 FIFO 意图；队列代码优先用对应的队列名称。 |

## 选择建议

| 需求 | 建议 |
| --- | --- |
| 单线程或已同步的 FIFO 待处理项 | `QQueue<T>` |
| 需要随机访问、按位置增删 | `QList<T>` |
| 后进先出 | `QStack<T>` |
| 跨线程投递工作 | queued signal/slot，或加锁的队列加条件变量 |
| 高吞吐无锁/有界阻塞队列 | 专用并发队列，先定义背压与关闭语义 |

一句话记忆：`QQueue` 是带 FIFO 名称的 `QList`；先检查非空，再从 `head()` 看、用 `dequeue()` 取，别把它误当成并发队列或严格封装。
