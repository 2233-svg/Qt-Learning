# Qt QEventLoopLocker 深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QEventLoopLocker>`  
> 所属模块：`Qt6::Core`  
> 类型性质：控制事件循环退出时机的 RAII 保护对象  
> 相关类型：`QCoreApplication`、`QEventLoop`、`QThread`

## 1. 它解决什么问题

`QEventLoopLocker` 用对象生命周期表示“这里还有异步工作，目标事件循环暂时不能因为没有其他 locker 而退出”。

它可以针对三种目标：

1. 默认构造：当前 `QCoreApplication`；
2. `QEventLoop *` 构造：某个局部事件循环；
3. `QThread *` 构造：某个线程的事件循环。

当目标上的最后一个 `QEventLoopLocker` 被销毁时，Qt 会尝试让目标退出：

- 对 `QCoreApplication`，在 `isQuitLockEnabled()` 为 true 时尝试退出应用；
- 对 `QEventLoop`，尝试调用该局部循环的退出逻辑；
- 对 `QThread`，尝试让该线程的事件循环退出。

它是一种“退出保护”，不是数据锁：

- 不保护共享变量；
- 不阻塞当前线程；
- 不自动启动事件循环；
- 不提供 `lock()`/`unlock()`；
- 不等待异步任务完成；
- 不保证退出请求一定立刻或一定成功。

### 1.1 用一句话理解

```text
还有 QEventLoopLocker 存活  ->  目标保持可运行
最后一个 QEventLoopLocker 销毁 ->  Qt 尝试让目标退出
```

## 2. 实际使用场景

### 2.1 主窗口关闭后仍完成后台任务

GUI 应用通常会在最后一个窗口关闭后尝试退出。网络上传、保存设置或后台同步可能仍未完成，此时可以让每个任务持有一个默认构造的 locker：

```cpp
class UploadJob : public QObject
{
    Q_OBJECT

public:
    explicit UploadJob(QObject *parent = nullptr)
        : QObject(parent)
    {
    }

private:
    QEventLoopLocker m_quitGuard;
};
```

只要 `UploadJob` 还活着，应用级 quit lock 计数就不会归零。任务结束后销毁 job，最后一个 locker 被销毁，Qt 才会尝试退出应用。

这适合：

- 最后一个窗口关闭后仍要完成网络上传；
- 后台保存或日志刷盘；
- 异步任务由对象生命周期表示完成状态。

### 2.2 一批任务共享一个局部事件循环

某些命令行程序、测试辅助程序或同步封装会创建局部 `QEventLoop`，直到一批异步 job 全部结束才退出。可以把 `QEventLoopLocker` 放在每个 job 中，并让 job 结束时释放它。

```cpp
class BatchJob : public QObject
{
    Q_OBJECT

public:
    explicit BatchJob(QEventLoop *loop, QObject *parent = nullptr)
        : QObject(parent), m_loopGuard(loop)
    {
    }

private:
    QEventLoopLocker m_loopGuard;
};
```

这个模式的重点是：局部循环不靠某个调用点猜测“什么时候最后一个任务结束”，而是由每个任务的 RAII 生命周期共同决定。

### 2.3 让工作线程在最后一个工作对象释放后退出

```cpp
QThread worker;
{
    QEventLoopLocker threadGuard(&worker);
    worker.start();

    // 向 worker 投递任务，或创建归属于 worker 的异步对象。
    // guard 存活期间，worker 的事件循环不会因 locker 计数归零而退出。
}

worker.wait();
```

线程退出请求是异步的。`QEventLoopLocker` 析构后要不要调用 `wait()`，取决于程序是否需要在离开当前作用域前确认线程已经停止；销毁 `QThread` 前必须遵守 `QThread` 的生命周期规则。

### 2.4 把退出保护放进任务对象

这是最自然的设计：

```cpp
class NetworkTask : public QObject
{
    Q_OBJECT

public:
    explicit NetworkTask(QObject *parent = nullptr)
        : QObject(parent)
    {
    }

public slots:
    void finish()
    {
        deleteLater(); // 对象销毁时释放 m_guard
    }

private:
    QEventLoopLocker m_guard;
};
```

任务的完成路径只需要销毁任务对象，退出保护会自动释放。不要额外维护一套容易和对象状态不一致的全局任务计数。

## 3. 构建与最小示例

`QEventLoopLocker` 属于 Qt Core：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Core)
target_link_libraries(mytarget PRIVATE Qt6::Core)
```

默认构造针对 `QCoreApplication`：

```cpp
#include <QCoreApplication>
#include <QEventLoopLocker>

int main(int argc, char **argv)
{
    QCoreApplication app(argc, argv);

    {
        QEventLoopLocker guard;
        // 异步工作仍在进行，应用级 quit lock 不会归零。
    }

    return app.exec();
}
```

这个示例只展示生命周期关系。实际程序中，locker 应该由真正代表异步工作的对象持有，不能用一个永不销毁的全局 locker 把应用永久留在事件循环里。

## 4. 三种目标的语义差异

### 4.1 默认构造：应用级 quit lock

```cpp
QEventLoopLocker guard;
```

它针对当前 `QCoreApplication`。当应用上没有其他 `QEventLoopLocker` 时，且 `QCoreApplication::isQuitLockEnabled()` 为 true，Qt 会尝试退出应用。

这个“尝试退出”仍可能不导致应用真正退出，例如：

- 仍有打开的窗口；
- `QEvent::Quit` 被忽略；
- 应用或平台逻辑阻止退出；
- 事件循环尚未运行或正在处理其他退出条件。

应用级 locker 不能替代显式的 `QCoreApplication::quit()`，它的意义是把“应用可以退出”的判断绑定到异步工作对象生命周期。

### 4.2 `QEventLoop *`：局部事件循环

```cpp
QEventLoop loop;
QEventLoopLocker guard(&loop);
```

它只影响传入的这个局部 `QEventLoop`，不影响主应用事件循环，也不影响其他局部循环。

目标 loop 必须在 locker 之前创建，并且必须比 locker 活得更久。不要把指向已经销毁的 loop 的指针交给 locker。

### 4.3 `QThread *`：线程事件循环

```cpp
QThread thread;
QEventLoopLocker guard(&thread);
```

它针对传入线程的事件循环。最后一个针对该线程的 locker 消失后，Qt 会尝试让该线程退出。

这不会：

- 强制终止线程；
- 中断正在执行的任意函数；
- 等待线程结束；
- 替代 `QThread::quit()`、`requestInterruption()` 或 `wait()` 的其他语义。

如果线程正在执行不可中断的长函数，退出请求要等到线程重新回到事件循环或主动处理退出逻辑后才会产生效果。

## 5. 典型批处理结构

### 5.1 每个任务持有一个 guard

```cpp
class Job : public QObject
{
    Q_OBJECT

public:
    explicit Job(QEventLoop *loop, QObject *parent = nullptr)
        : QObject(parent), m_guard(loop)
    {
    }

    void complete()
    {
        deleteLater();
    }

private:
    QEventLoopLocker m_guard;
};
```

如果同时创建多个 `Job`，局部事件循环会在最后一个 job 的 guard 释放后收到退出请求。

### 5.2 需要异步启动局部循环时的顺序

推荐顺序是：

1. 创建 `QEventLoop`；
2. 创建持有 locker 的任务对象；
3. 启动异步工作；
4. 调用 `loop.exec()`；
5. 让最后一个任务在完成路径释放自己的 locker；
6. `exec()` 返回后清理剩余对象。

不要在调用 `exec()` 的同一作用域中持有一个永远到 `exec()` 返回后才析构的唯一 locker，否则它本身会把 loop 一直保护住，形成逻辑上的“自己阻止自己退出”。

### 5.3 应用级任务的退出条件

应用级 guard 适合由任务对象持有：

```cpp
class UploadTask : public QObject
{
    Q_OBJECT

public:
    explicit UploadTask(QObject *parent = nullptr)
        : QObject(parent)
    {
    }

signals:
    void finished();

private:
    QEventLoopLocker m_applicationGuard;
};
```

发出 `finished()` 并不自动销毁对象，也就不会自动释放 locker。必须由明确的所有权关系、`deleteLater()` 或智能指针生命周期完成最终释放。

## 6. RAII 和移动语义

### 6.1 不可复制

`QEventLoopLocker` 禁用拷贝构造和拷贝赋值。复制一个 locker 会错误地暗示“是否增加一次退出保护计数”可以用普通值复制表达，因此 Qt 不允许这样做。

下面的代码不能编译：

```cpp
QEventLoopLocker first;
QEventLoopLocker second = first; // 禁止复制
```

如果需要把责任转移给另一个对象，使用 Qt 6.7 起的移动构造或移动赋值。

### 6.2 移动构造

```cpp
QEventLoopLocker first;
QEventLoopLocker second = std::move(first);
```

移动后：

- `second` 接管原来的退出保护责任；
- `first` 的析构函数变成 no-op；
- 目标对象上的保护计数不会因为移动而增加一份；
- 不要再把 moved-from 对象当成仍然持有 guard 的对象。

### 6.3 移动赋值

```cpp
QEventLoopLocker first;
QEventLoopLocker second;
second = std::move(first);
```

移动赋值会让 `second` 接管 `first` 的状态。`second` 原先持有的保护状态会被正确释放或交换处理，不应再把它当成原先的目标。

Qt 6.7 之前不能依赖这些移动 API；如果项目需要兼容旧 Qt，应通过对象指针、成员生命周期或其他旧版本可用的结构组织所有权。

### 6.4 `swap()`

`swap()` 交换两个 locker 持有的内部目标和状态：

```cpp
QEventLoopLocker applicationGuard;
QEventLoop loop;
QEventLoopLocker loopGuard(&loop);

applicationGuard.swap(loopGuard);
```

交换不会复制保护计数，通常是快速且不会失败的操作。交换之后每个对象保护的目标发生变化，代码必须仍能清楚表达其生命周期。

## 7. 与 QCoreApplication 的 quit lock 配合

### 7.1 `isQuitLockEnabled`

应用是否允许 `QEventLoopLocker` 的最后一个 guard 触发退出，由 `QCoreApplication::isQuitLockEnabled()` 控制。

如果该属性为 false：

- 默认构造的 locker 仍然可以存在；
- locker 计数仍然反映任务生命周期；
- 释放最后一个 locker 不会通过这个机制尝试退出应用。

这适合由应用框架统一管理退出时机的场景。不要在库代码中随意改变全局 quit lock 配置，否则可能影响宿主应用的退出策略。

### 7.2 locker 不会覆盖其他退出阻止条件

即使最后一个 locker 释放并触发退出尝试，应用也可能因为窗口、事件过滤器、忽略的 `QEvent::Quit` 或平台策略而继续运行。相反，存在 locker 也不意味着应用绝对不会被显式 `quit()` 或 `exit()` 终止。

它表达的是“自然退出条件中的一个保护计数”，不是强制关机开关。

## 8. 生命周期和线程边界

### 8.1 目标对象必须活得更久

对于 `QEventLoop *` 和 `QThread *` 构造的 locker，目标对象必须在 locker 析构前保持有效：

```cpp
QEventLoopLocker *guard;
{
    QEventLoop loop;
    guard = new QEventLoopLocker(&loop);
} // loop 已销毁，但 guard 仍存在：错误的生命周期
```

正确做法是让 guard 成为目标对象作用域中的局部变量，或让 guard 成为目标仍然存活的任务对象成员。

### 8.2 不要把它当成线程同步原语

多个线程可以各自创建 locker，但 `QEventLoopLocker` 不负责保护你的任务列表、计数器或结果对象。若多个线程同时读写任务状态，仍需使用信号槽、互斥锁、原子类型或其他同步设计。

### 8.3 线程结束和对象销毁顺序

持有 `QEventLoopLocker(QThread *)` 时，线程对象必须保持有效。退出请求发出后，如果程序要销毁 `QThread`，应确认线程已结束：

```cpp
thread.quit();
thread.wait();
```

具体是让最后一个 locker 触发 quit，还是显式调用 `quit()`，由线程管理策略决定；两者不是互相替代的强制终止机制。

### 8.4 异常和提前返回

locker 是 RAII 对象，作用域提前离开时也会析构。这是它的主要价值：

```cpp
void runTask()
{
    QEventLoopLocker guard;
    if (!prepare())
        return; // 自动释放退出保护

    execute();
}
```

但提前释放也可能触发最后一个 guard 的退出尝试。因此任务对象的析构时机必须和“工作确实完成或取消”保持一致。

## 9. API 逐项说明

### 9.1 `QEventLoopLocker()`

构造一个针对当前 `QCoreApplication` 的 locker。只要应用上仍有一个或多个 locker，且 quit lock 功能开启，应用就不会因为 locker 计数归零而自然退出。

建议在 `QCoreApplication` 已构造后使用。不要在全局静态对象中创建它并让其跨越应用对象生命周期。

### 9.2 `explicit QEventLoopLocker(QEventLoop *loop)`

构造一个针对指定局部事件循环的 locker。最后一个针对该 loop 的 locker 销毁时，Qt 会尝试让该 loop 退出。

`loop` 应指向仍然存活的 `QEventLoop`。这个构造不把 loop 的所有权转交给 locker；locker 只记录目标和保护状态。

### 9.3 `explicit QEventLoopLocker(QThread *thread)`

构造一个针对指定线程事件循环的 locker。最后一个针对该线程的 locker 销毁时，Qt 会尝试让线程退出。

它不拥有 `QThread`，也不等待线程结束。目标线程和 `QThread` 对象都必须满足各自的 Qt 生命周期约束。

### 9.4 `QEventLoopLocker(QEventLoopLocker &&other)`

Qt 6.7 起提供的移动构造。把 `other` 的保护责任转移到新对象，移动后的 `other` 析构不再释放这份责任。

### 9.5 `~QEventLoopLocker()`

销毁 locker 并释放它持有的退出保护。若这是目标上的最后一个 locker，可能触发退出尝试。

析构本身不保证目标已经退出；应用或线程仍需运行事件循环来处理退出逻辑。

### 9.6 `void swap(QEventLoopLocker &other)`

Qt 6.7 起提供。交换两个 locker 的内部状态和目标，操作快速且不会失败。

### 9.7 `QEventLoopLocker &operator=(QEventLoopLocker &&other)`

Qt 6.7 起提供的移动赋值。当前对象接管 `other` 的保护责任，`other` 变成无操作析构状态。当前对象原本持有的状态会被正确替换。

### 9.8 `swap(QEventLoopLocker &lhs, QEventLoopLocker &rhs)`

Qt 6.7 起的非成员 `swap()`，调用成员 `swap()` 交换两个 locker。它适合泛型代码和标准库风格的交换操作。

## 10. 常见误区和排查顺序

### 10.1 把 locker 当成互斥锁

`QEventLoopLocker` 不会阻止两个线程同时访问同一对象，也不会让代码进入临界区。共享状态仍需独立同步。

### 10.2 期待构造 locker 后自动启动事件循环

构造 locker 只增加退出保护，不会调用 `exec()`、`QThread::start()` 或 `QCoreApplication::exec()`。

### 10.3 guard 一直活着，应用不退出

检查：

1. 是否有全局或静态 locker；
2. 是否有任务对象未销毁；
3. 是否只发出了 `finished()` 信号但没有释放对象；
4. 是否把 locker 放在比任务更长的管理对象中；
5. 是否误以为 `deleteLater()` 已经立即执行，但目标线程事件循环没有处理它。

### 10.4 没有 locker，应用过早退出

如果最后一个窗口关闭后后台工作仍要继续，确认每个尚未完成的异步任务都持有应用级 locker，并且任务的析构时机确实对应完成。

### 10.5 `isQuitLockEnabled` 被关闭

应用级 locker 释放后没有退出尝试，检查 `QCoreApplication::isQuitLockEnabled()`。库代码不要擅自改变此全局应用属性。

### 10.6 目标对象先析构

`QEventLoop` 或 `QThread` 先于 locker 销毁会留下悬空目标。重新安排作用域，让目标活得比 guard 久。

### 10.7 把退出请求当成强制停止

locker 释放只会尝试退出事件循环。正在执行的长函数、阻塞系统调用或不响应事件循环的代码不会因此自动中断。

### 10.8 误用移动后的对象

移动构造或移动赋值后，源 locker 仍是有效 C++ 对象，但不再持有原保护责任。不要在源对象上推断“仍然阻止退出”。

## API 速查表
### 11.1 构造和析构

| API | 作用 | 关键边界 |
|---|---|---|
| `QEventLoopLocker()` | 保护当前 `QCoreApplication` 不因 locker 计数归零而自然退出 | 依赖 `isQuitLockEnabled()`；不启动应用 |
| `QEventLoopLocker(QEventLoop *loop)` | 保护指定局部事件循环 | loop 不转移所有权，必须比 locker 活得久 |
| `QEventLoopLocker(QThread *thread)` | 保护指定线程的事件循环 | 不停止/启动/等待线程，thread 必须有效 |
| `QEventLoopLocker(QEventLoopLocker &&)` | 移动保护责任 | Qt 6.7；源对象析构 no-op |
| `~QEventLoopLocker()` | 释放退出保护 | 最后一个 locker 可能触发退出尝试，不保证立即退出 |
| copy constructor/assignment | 拷贝 | 被禁用，不可复制 |

### 11.2 移动和交换

| API | 作用 | 关键边界 |
|---|---|---|
| `operator=(QEventLoopLocker &&)` | 移动赋值保护状态 | Qt 6.7；源对象不再持有责任 |
| `swap(QEventLoopLocker &other)` | 交换两个 locker 状态 | Qt 6.7；快速且不会失败 |
| `swap(lhs, rhs)` | 非成员交换 | Qt 6.7；适合泛型代码 |

### 11.3 相关控制点

| API/概念 | 作用 | 关键边界 |
|---|---|---|
| `QCoreApplication::isQuitLockEnabled()` | 查询应用是否允许 locker 释放触发退出尝试 | 只影响应用级默认构造 locker |
| `QCoreApplication::setQuitLockEnabled(bool)` | 开关应用级 quit lock 机制 | 影响全局应用策略，库代码慎用 |
| `QEventLoop::exec()` | 运行局部事件循环 | locker 不会自动调用它 |
| `QEventLoop::quit()` | 请求局部循环退出 | locker 只是让最后一个保护释放时自动尝试 |
| `QThread::quit()` | 请求线程事件循环退出 | locker 不等待线程结束 |
| `QThread::wait()` | 等待线程结束 | 需要确认线程生命周期时显式调用 |

### 11.4 语义选择

| 需求 | 选择 |
|---|---|
| 最后窗口关闭后仍完成后台任务 | 默认构造 `QEventLoopLocker`，放在任务对象中 |
| 一批 job 结束后退出局部 loop | `QEventLoopLocker(QEventLoop *)`，每个 job 持有一个 |
| 最后一个线程任务释放后退出线程 loop | `QEventLoopLocker(QThread *)` |
| 保护共享数据 | 使用 `QMutexLocker` 等同步工具，不使用本类 |
| 强制中止工作线程 | 设计可取消任务、`requestInterruption()` 或其他线程控制，不依赖本类 |

## 12. 选型结论

把 `QEventLoopLocker` 当成“用 RAII 管理事件循环退出许可的计数型保护对象”最准确：

- 它保护的是事件循环不因任务计数归零而过早退出；
- 它不保护数据、不启动循环、不等待线程、不强杀任务；
- 默认构造保护应用，指针构造分别保护局部 `QEventLoop` 或 `QThread`；
- 最后一个 locker 析构时只是发起退出尝试，最终结果仍由目标事件循环和 Qt 的其他退出条件决定；
- 把它放进真正代表异步任务生命周期的对象中，通常比手工维护全局计数更可靠。
