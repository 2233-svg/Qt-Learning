# Qt QFutureIterator 深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QFutureIterator>`  
> 所属模块：`Qt6::Core`  
> 类型性质：Java 风格的只读 future 迭代器  
> 相关类型：`QFuture`、`QFuture::const_iterator`

## 1. 它解决什么问题

`QFutureIterator<T>` 为 `QFuture<T>` 提供 Qt 传统的 Java 风格遍历接口。它把迭代器位置放在两个结果之间，而不是直接指向一个结果：

```text
front | result[0] | result[1] | ... | result[n - 1] | back
```

调用 `next()` 会返回当前位置右侧的结果，然后把位置向后移动；调用 `previous()` 则返回左侧结果并向前移动。

它解决的是“以 Qt Java-style iterator 风格逐项读取异步结果”的问题，尤其适合已有代码大量使用 `hasNext()` / `next()` 的项目。它只读，不提供修改 `QFuture` 结果的能力。

## 2. 实际使用场景

### 2.1 顺序消费多个结果

```cpp
QFuture<QString> future = startManyResults();
QFutureIterator<QString> iterator(future);

while (iterator.hasNext()) {
    const QString value = iterator.next();
    consume(value);
}
```

`next()` 在结果尚未可用时会等待，因此这段代码的总耗时可能包含后台计算时间。

### 2.2 反向遍历

```cpp
QFutureIterator<QString> iterator(future);
iterator.toBack();

while (iterator.hasPrevious())
    consume(iterator.previous());
```

反向遍历适合结果已经完成或需要从后往前搜索的场景。

### 2.3 查找多个匹配值

```cpp
iterator.toFront();
while (iterator.findNext(target))
    qDebug() << "found";
```

`findNext()` 找到后会把位置放到匹配结果之后，所以循环可以继续查找下一个匹配项。

## 3. 和 STL 风格迭代器的区别

`QFuture` 同时支持：

- Java 风格：`QFutureIterator<T>`，位置在结果之间，方法名是 `hasNext()` / `next()`；
- STL 风格：`QFuture<T>::const_iterator`，支持 `begin()` / `end()` 和 range-for。

Java 风格接口更高层、更直观，但通常效率略低。需要 STL 算法或 range-for 时使用 `QFuture::const_iterator`；需要 Qt 旧式迭代器接口时使用 `QFutureIterator`。

`QFuture` 没有可修改迭代器，`QFutureIterator` 也不会改变结果。

## 4. 迭代位置和阻塞边界

### 4.1 构造后位于 front

构造函数接收一个 `QFuture<T>`，迭代器初始位置在第一个结果之前。此时：

- `hasNext()` 可能为 `true`；
- `hasPrevious()` 为 `false`；
- `next()` 返回第一个结果并移动到第一个、第二个结果之间。

### 4.2 `next()` 和查找可能等待

future 仍在生产结果时，`next()` 可能等待下一个结果出现。`peekNext()`、`findNext()` 等需要检查后续结果的操作也可能等待或推进读取。

不要在 GUI 线程、持锁区域或需要持续处理事件的线程中把它当成无阻塞遍历器。若需要事件驱动的逐项处理，优先使用 `QFutureWatcher::resultReadyAt()`。

### 4.3 越界调用是未定义行为

在 back 位置调用 `next()` 或 `peekNext()`，以及在 front 位置调用 `previous()` 或 `peekPrevious()`，都会导致未定义结果。总是先检查：

```cpp
if (iterator.hasNext())
    use(iterator.next());
```

### 4.4 异步结果和“没有下一个结果”

`hasNext()` 表示当前位置后面至少有一个结果；对仍在运行、尚未产生下一结果的 future，不要仅凭一次 `false` 就设计出复杂的“任务已经失败”结论。任务结束、取消和结果到达应通过 future 状态或 watcher 信号确认。

## 5. future 的快照语义

构造和赋值都会让迭代器操作某个 `QFuture` 句柄。多个迭代器可以同时遍历同一个 future。

如果外部把一个共享 future 句柄重新赋值为另一个状态，已经存在的 `QFutureIterator` 继续遍历原来绑定的 future，不会自动切换到修改后的副本。这使得迭代过程不会因为外部重新赋值而突然改变目标。

迭代器保存的是共享 future 语义，不是把所有结果复制成一个独立的 `QList`。结果对象的生命周期和共享 future 状态仍需由异步生产者保证。

## 6. 逐项 API 说明

### 构造和赋值

#### `QFutureIterator::QFutureIterator(const QFuture<T> &future)`

为 `future` 创建只读 Java 风格迭代器，初始位置在结果列表 front，即第一个结果之前。

future 的句柄会被共享；构造不会启动一个新的计算，也不会复制后台任务。

#### `QFutureIterator<T> &QFutureIterator::operator=(const QFuture<T> &future)`

让迭代器改为操作另一个 future，并把位置重置到 front。它不是给迭代器复制另一个迭代器，而是重新绑定 future。

### 位置查询

#### `bool QFutureIterator::hasNext() const`

判断当前位置后方是否存在至少一个结果。为 `false` 时不要调用 `next()` 或 `peekNext()`。

#### `bool QFutureIterator::hasPrevious() const`

判断当前位置前方是否存在至少一个结果。为 `false` 时不要调用 `previous()` 或 `peekPrevious()`。

#### `void QFutureIterator::toFront()`

把迭代器移动到 front，即第一个结果之前。调用后 `hasPrevious()` 为 `false`。

#### `void QFutureIterator::toBack()`

把迭代器移动到 back，即最后一个结果之后。调用后 `hasNext()` 为 `false`。

### 正向读取

#### `const T &QFutureIterator::next()`

返回下一个结果，并把位置向后移动一个结果。结果尚未可用时会等待。

在 back 位置调用会产生未定义结果。返回的是对 future 内部结果的只读引用，若需要独立保存，应立即复制到自己的对象中。

#### `const T &QFutureIterator::peekNext() const`

返回下一个结果但不移动位置。调用前必须确认 `hasNext()`，否则在 back 位置使用会产生未定义结果。

它可能等待目标结果可用，不能当作无阻塞探测。

#### `bool QFutureIterator::findNext(const T &value)`

从当前位置向前查找与 `value` 相等的结果：

- 找到时返回 `true`，位置放到匹配结果之后；
- 找不到时返回 `false`，位置移动到 back。

它要求 `T` 支持与 `value` 比较。搜索过程中可能等待后续结果。

### 反向读取

#### `const T &QFutureIterator::previous()`

返回前一个结果，并把位置向前移动一个结果。调用前必须确认 `hasPrevious()`。

在 front 位置调用会产生未定义结果。返回的是内部结果的只读引用。

#### `const T &QFutureIterator::peekPrevious() const`

返回前一个结果但不移动位置。调用前必须确认 `hasPrevious()`，否则在 front 位置使用会产生未定义结果。

#### `bool QFutureIterator::findPrevious(const T &value)`

从当前位置向后查找与 `value` 相等的结果：

- 找到时返回 `true`，位置放到匹配结果之前；
- 找不到时返回 `false`，位置移动到 front。

## API 速查表
| API | 作用 | 关键边界 |
|---|---|---|
| `QFutureIterator(future)` | 创建只读迭代器 | 初始在 front；共享 future 句柄 |
| `operator=(future)` | 绑定新 future 并回到 front | 不复制结果 |
| `hasNext()` | 查询后方是否有结果 | false 时不能 `next()` |
| `hasPrevious()` | 查询前方是否有结果 | false 时不能 `previous()` |
| `next()` | 返回后一个结果并前进 | 可能等待；back 位置 UB |
| `previous()` | 返回前一个结果并后退 | 可能等待；front 位置 UB |
| `peekNext()` | 查看后一个结果不移动 | back 位置 UB |
| `peekPrevious()` | 查看前一个结果不移动 | front 位置 UB |
| `findNext(value)` | 向前找匹配项 | 成功后在匹配项之后；失败到 back |
| `findPrevious(value)` | 向后找匹配项 | 成功后在匹配项之前；失败到 front |
| `toFront()` | 移到第一个结果之前 | `hasPrevious()` 为 false |
| `toBack()` | 移到最后一个结果之后 | `hasNext()` 为 false |

## 8. 选择建议

- 需要 range-for、STL 算法或更直接的异步索引：使用 `QFuture::const_iterator`。
- 需要 Qt Java 风格 API：使用 `QFutureIterator`。
- 需要在结果到达时更新 UI：使用 `QFutureWatcher`，不要在主线程循环调用 `next()`。
- 需要移动提取 move-only 结果：使用 `QFuture::takeResult()`；`QFutureIterator` 返回的是 `const T &`，不能移动出内部结果。

## 9. 排查顺序

1. 读到崩溃或异常值，检查是否在 `hasNext()` / `hasPrevious()` 为 false 时读取。
2. 界面卡顿，检查 `next()`、`previous()`、`findNext()` 是否在 GUI 线程等待后台结果。
3. 迭代目标似乎没有跟着外部 future 变化，确认这是迭代器绑定原 future 的预期快照语义。
4. 需要实时显示进度或每项到达时间时，改用 `QFutureWatcher`。
5. 需要修改结果时，重新设计生产者或在读出后修改副本；该迭代器始终只读。
