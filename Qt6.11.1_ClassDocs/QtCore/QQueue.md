# QQueue
> Qt 6.11.1 · Qt Core · 来自 `QQueue<T>`

## 作用定位
`QQueue<T>` 是基于 `QList<T>` 的先进先出队列。它用 `enqueue()` 把任务放到尾部，用 `dequeue()` 从头部取走最早进入的任务，使调用点能直接表达“排队处理”的意图。

它是值容器，不是线程安全队列，也不提供阻塞等待。多线程生产/消费需要另加 `QMutex`、`QWaitCondition` 或选择专门的并发设计。

## API 速查
| API | 是做什么的 |
|---|---|
| `enqueue(const T &)` | 将元素复制到队尾。 |
| `enqueue(T &&)` | 将元素移动到队尾，减少大对象复制。 |
| `dequeue()` | 取出并移除队头元素；队列不能为空。 |
| `head()` | 取得队头元素引用但不移除；队列不能为空。 |
| `swap(other)` | 常数时间交换两个队列的内容。 |
| 继承的 `isEmpty()` / `size()` | 入队前后检查队列状态。 |
| 继承的 `clear()` | 丢弃所有待处理元素。 |

## 使用场景

### 单线程事件批处理
```cpp
QQueue<Job> pending;
pending.enqueue(makeJob());

while (!pending.isEmpty()) {
    const Job job = pending.dequeue();
    process(job);
}
```
将“是否还有工作”显式写在循环条件里。`dequeue()` 对空队列没有安全兜底；如果队列可能被别的代码清空，先检查或统一由一个所有者消费。

### 需要查看下一个任务但不取走
```cpp
if (!pending.isEmpty() && canRun(pending.head()))
    start(pending.dequeue());
```
`head()` 返回的是内部元素引用。下一次入队、出队、detach 或销毁容器后都不应继续保存这个引用。

## 常见坑与经验
- `QQueue` 的 FIFO 语义来自命名和 `enqueue/dequeue`，底层仍是 `QList`；不要把它当固定容量环形缓冲区。
- 容器的隐式共享降低了复制开销，但任何共享实例的并发读写仍是数据竞争。
- `dequeue()` 返回值可能发生复制或移动；任务对象很大时优先让 `T` 可移动，或存储智能指针。
- 需要优先级调度时使用 `std::priority_queue`、排序容器或显式调度器，不能靠插入顺序凑优先级。
- 遍历队列时不要同时出队；要消费就使用 `while (!isEmpty())`。

## 知识点覆盖
FIFO、值语义、隐式共享、移动语义、引用失效、生产者消费者、任务调度、容器复杂度与线程同步。
