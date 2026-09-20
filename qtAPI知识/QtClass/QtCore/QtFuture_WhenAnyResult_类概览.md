# Qt QtFuture::WhenAnyResult whenAny 结果

> 适用版本：Qt 6.11.1  
> 头文件：`#include <WhenAnyResult>`（文档列出的类页头文件；实际项目通常随 `QFuture` / `QtFuture` 相关头一同使用）  
> 所属模块：`Qt6::Core`  
> 首次引入：Qt 6.3  
> 定位：`QtFuture::whenAny(first, last)` 的结果包装结构体

## 它解决什么问题

`QtFuture::whenAny()` 用来把多个 `QFuture` 合成一个“谁先完成就先返回谁”的 future。对于参数包形式：

```cpp
QtFuture::whenAny(futureA, futureB, futureC)
```

参与的 future 可以有不同类型，所以结果用 `std::variant<QFuture<...>, ...>` 表示。

而对于迭代器区间形式：

```cpp
QtFuture::whenAny(first, last)
```

区间里的 future 都包装同一种 `T`。这时结果不需要 variant，只需要告诉你：

- 第一个完成的是区间中的第几个。
- 那个完成的 `QFuture<T>` 是哪一个。

`QtFuture::WhenAnyResult<T>` 就是这个小包装。

```cpp
template <typename T>
struct QtFuture::WhenAnyResult
{
    qsizetype index = -1;
    QFuture<T> future;
};
```

它没有成员函数、信号或隐藏状态；可读性来自两个公开字段的语义。

## 实际使用场景

- 向多个镜像源、服务端或后台任务发起同类请求，先处理最快完成的那个。
- 对一组相同结果类型的计算使用 `QList<QFuture<T>>` 管理，并在任意一个完成时更新 UI。
- 多个候选算法同时跑，谁先给出可用结果就先进入下一步。
- 需要知道“哪个 future 赢了”，而不只是拿到一个完成信号。

如果参与的 future 类型不同，使用参数包版 `whenAny()` 并处理 `std::variant`。如果需要等待全部完成，使用 `QtFuture::whenAll()`。

## 构建与包含

```cmake
find_package(Qt6 REQUIRED COMPONENTS Core)
target_link_libraries(mytarget PRIVATE Qt6::Core)
```

```cpp
#include <QFuture>
```

Qt 文档的结构体类页列出 `#include <WhenAnyResult>`，但日常代码通常是通过使用 `QFuture` / `QtFuture::whenAny()` 的头文件获得该模板定义。

## 最小可用示例

```cpp
#include <QFuture>
#include <QList>

void handleFirst(QList<QFuture<int>> futures, QObject *context)
{
    QtFuture::whenAny(futures.begin(), futures.end())
            .then(context, [](const QtFuture::WhenAnyResult<int> &result) {
                if (result.index < 0)
                    return;

                const qsizetype winner = result.index;
                const QFuture<int> firstFinished = result.future;

                // firstFinished may be finished normally, canceled, or failed.
                Q_UNUSED(winner);
                Q_UNUSED(firstFinished);
            });
}
```

`whenAny()` 返回的外层 future 会在第一个输入 future 完成时成功完成。注意这里的“成功”只说明“已经知道哪个先完成”，不代表那个输入 future 一定正常产生了结果。

## 关键语义

### 只用于同类型 future 的区间版 whenAny

`WhenAnyResult<T>` 来自：

```cpp
QtFuture::whenAny(InputIt first, InputIt last)
```

其中 `[first, last)` 是一段 `QFuture<T>` 序列。结果类型是：

```cpp
QFuture<QtFuture::WhenAnyResult<T>>
```

如果你调用的是可变参数版 `whenAny(f1, f2, ...)`，结果不是 `WhenAnyResult`，而是 `std::variant`。

### index 是原序列下标

`index` 表示第一个完成的 future 在输入区间中的位置，从 `0` 开始。它不是 `QFuture` 的结果索引，也不是完成顺序计数。

空序列是特殊情况：`whenAny(first, last)` 在 `first == last` 时返回一个已经就绪的 future，其中：

- `index == -1`
- `future` 是默认构造的 `QFuture<T>`

文档说明默认构造的 `QFuture` 是一个处于 canceled 状态的已完成 future。因此处理结果时应先判断 `index < 0`。

### future 是第一个完成 future 的副本

`future` 字段保存第一个完成的 `QFuture<T>` 的副本。复制 `QFuture` 不会复制实际任务；它共享同一异步状态。你可以继续读取状态、结果、取消状态或异常状态，但要按 `QFuture` 自身规则处理。

### 取消和异常也算“完成”

`whenAny()` 不要求第一个 future 正常成功。第一个完成的 future 即使是 canceled 或带异常，外层 `whenAny()` future 也会成功完成，并把那个 future 包进 `WhenAnyResult`。后续代码必须检查 `result.future` 的状态，而不能直接假定 `result.future.result()` 安全。

### 回调线程不固定

如果输入 futures 在不同线程完成，`whenAny()` 返回的 future 会在第一个输入 future 完成的线程里完成。因此挂在外层 future 上的 continuation 不能假定运行在哪个线程。需要回到特定对象线程时，使用带 context 的 `.then(context, ...)` 重载。

## 常见误区

- 把 `WhenAnyResult` 用在可变参数版 `whenAny(f1, f2, ...)` 上；那一版返回 `std::variant`。
- 看到外层 future 成功完成，就认为内部 `future` 一定有正常结果。
- 忘记处理空序列，直接用 `index` 访问原列表。
- 在 `.then()` 中直接更新 UI，却没有使用 context 控制回调线程。
- 把 `index` 当成 `QFuture` 里的 result index；它只是输入序列下标。
- 认为 `future` 字段是任务的深拷贝。它是 `QFuture` 句柄副本，共享异步状态。

## 字段说明

### `qsizetype index`

第一个完成的 future 在传入区间中的下标。正常情况下从 `0` 开始；空区间时为 `-1`。

### `QFuture<T> future`

第一个完成的 future 的副本。它可能正常完成，也可能取消或携带异常；读取结果前先检查对应状态。

## API 速查表

| API | 作用 | 重点边界 |
| --- | --- | --- |
| `QtFuture::WhenAnyResult<T>` | 包装区间版 `whenAny()` 的赢家信息 | 只用于同类型 `QFuture<T>` 序列 |
| `index` | 第一个完成 future 的输入序列下标 | 空区间为 `-1`；从 `0` 开始 |
| `future` | 第一个完成的 `QFuture<T>` 副本 | 可能取消或失败；读取结果前检查状态 |
| CTAD 推导指引 | 支持从 `(qsizetype, QFuture<T>)` 推导 `WhenAnyResult<T>` | 通常由 Qt 内部创建，业务代码很少手写 |

## 一句话总结

`QtFuture::WhenAnyResult<T>` 是区间版 `QtFuture::whenAny()` 的小结果包：`index` 告诉你谁先完成，`future` 给你那个完成的 future，但是否成功、有无异常、回调在哪个线程运行，都还要按 `QFuture` 规则继续判断。
